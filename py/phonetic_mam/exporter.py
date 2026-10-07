"""Build the display-only release through a private source adapter subprocess.

The adapter's computation state is transient. Only the closed public display
projection can be written, and only below this checkout's Phonetic-MAM product.
"""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time

from mb_cmn import bib_locales, paths, provenance
from phonetic_mam import (
    display_corrections,
    display_projection,
    display_schema,
    example_display,
    strand_layouts,
)

_ADAPTER_RELATIVE_PATH = Path("al-hatorah/py/main_phonetic_mam_source.py")
_MAX_BOOK_CHARS = 64 * 1024 * 1024
# A failing adapter's error names the end of its standard error, which is kept in
# memory only, so that nothing that may quote private data is written to disk.
_STDERR_TAIL_BYTES = 4096
# The whole export step took 229.2 seconds when this limit was set; a hung adapter
# is stopped rather than blocking the export.
_ADAPTER_TIME_LIMIT_SECONDS = 1800
# A descendant of the adapter that inherited one of its pipes can hold the pipe
# open after the adapter has ended. Once the adapter has ended, or the limit has
# passed, its pipes are waited for at most this long and then left to the threads
# reading them, so that the limit holds whatever the adapter starts.
_PIPE_GRACE_SECONDS = 5


def _tail_text(data):
    """The last ``_STDERR_TAIL_BYTES`` of an adapter's standard error, as text."""
    if not data:
        return "(nothing)"
    if isinstance(data, str):
        data = data.encode("utf-8", "replace")
    tail = bytes(data[-_STDERR_TAIL_BYTES:]).decode("utf-8", "replace").strip()
    return tail or "(nothing)"


class _StderrTail:
    """Drain a child's standard error on a daemon thread, keeping only its tail.

    The thread holds the stream as the child's ``Popen`` gives it, text or binary,
    so that a stream left to the thread is not finalized under its pending read.
    """

    def __init__(self, stream):
        self._stream = stream
        self._tail = bytearray()
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._drain, daemon=True)
        self._thread.start()

    def _drain(self):
        # A text stream is read through its binary buffer.
        read1 = getattr(self._stream, "buffer", self._stream).read1
        try:
            while chunk := read1(65536):
                with self._lock:
                    self._tail += chunk
                    del self._tail[:-_STDERR_TAIL_BYTES]
        except (OSError, ValueError):
            # The pipe was closed under the reader; the tail kept so far stands.
            return

    def reading(self):
        return self._thread.is_alive()

    def join(self, deadline):
        self._thread.join(max(0.0, deadline - time.monotonic()))

    def text(self, deadline):
        self.join(deadline)
        with self._lock:
            return _tail_text(self._tail)


class _PipeReads:
    """Make each blocking read of a child's pipe on a daemon thread.

    A read is waited for only until a deadline. Past it the read is left to its
    thread, which holds the stream until the read ends: a descendant of the
    adapter that inherited the pipe can hold it open after the adapter has
    ended, and the read then ends only with that descendant.
    """

    def __init__(self, stream):
        self._stream = stream
        self._thread = None

    def read(self, deadline, size=-1, *, line=False):
        """What the read returns, or None if the deadline passes first."""
        read = self._stream.readline if line else self._stream.read
        outcome = []

        def run():
            try:
                outcome.append(read(size))
            except Exception as error:  # Raised again in the caller's thread.
                outcome.append(error)

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()
        self._thread.join(max(0.0, deadline - time.monotonic()))
        if not outcome:
            return None
        if isinstance(outcome[0], Exception):
            raise outcome[0]
        return outcome[0]

    def reading(self):
        return self._thread is not None and self._thread.is_alive()


class _Watchdog:
    """Kill a child that outlives the adapter time limit, and remember doing so.

    Its deadline bounds every wait on the child's pipes: the time limit and then
    the grace period, or only the grace period once the child is seen to end,
    after which the watchdog has nothing to stop.
    """

    def __init__(self, process):
        self.fired = False
        self.deadline = (
            time.monotonic() + _ADAPTER_TIME_LIMIT_SECONDS + _PIPE_GRACE_SECONDS
        )
        self._process = process
        self._timer = threading.Timer(_ADAPTER_TIME_LIMIT_SECONDS, self._fire)
        self._timer.daemon = True
        self._timer.start()

    def _fire(self):
        self.fired = True
        self._process.kill()

    def ended(self):
        self.cancel()
        self.deadline = min(self.deadline, time.monotonic() + _PIPE_GRACE_SECONDS)

    def cancel(self):
        self._timer.cancel()


def _adapter_error(process, watchdog, stderr, failure):
    """The release error for a failed streaming run, with its status and stderr tail."""
    if process.poll() is None:
        process.kill()
    status = process.wait()
    watchdog.ended()
    if watchdog.fired:
        failure = (
            f"source adapter exceeded its {_ADAPTER_TIME_LIMIT_SECONDS}-second limit"
            " and was stopped"
        )
    tail = stderr.text(watchdog.deadline)
    return display_schema.PublicReleaseError(
        f"{failure} (exit status {status}); its stderr ended with:\n{tail}"
    )


def _stop(process, watchdog, stdout, stderr):
    """End an adapter run, leaving any pipe still being read to its reader.

    Popen.__exit__ closes both pipes, and closing a stream waits for a read
    pending on another thread, so a pipe that a descendant of the adapter holds
    open past the deadline is taken from the ``Popen`` instead.
    """
    watchdog.cancel()
    # Kill rather than terminate: with the watchdog cancelled, a wait for a
    # child that ignores termination would have no bound.
    if process.poll() is None:
        process.kill()
        process.wait()
    watchdog.ended()
    stderr.join(watchdog.deadline)
    if stdout.reading():
        process.stdout = None
    if stderr.reading():
        process.stderr = None


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        display_schema.require(key not in result, "duplicate adapter JSON field")
        result[key] = value
    return result


def _reject_constant(_value):
    raise display_schema.PublicReleaseError("non-finite adapter JSON number")


def _adapter_location():
    root = paths.require_sibling(
        "MAM-private", paths.sibling_repo("MAM-private")
    ).resolve()
    adapter = root / _ADAPTER_RELATIVE_PATH
    if not adapter.is_file() or not adapter.resolve().is_relative_to(root):
        raise FileNotFoundError(
            "MAM-private display source adapter is absent or outside its root"
        )
    return root, adapter


def _adapter_command(operation):
    root, adapter = _adapter_location()
    home = provenance.home_clone_dir(root) or root
    python_relative = "Scripts/python.exe" if os.name == "nt" else "bin/python"
    interpreter = home / "al-hatorah" / ".venv" / python_relative
    if not interpreter.is_file():
        raise FileNotFoundError(
            "the private adapter's owning Python environment is absent"
        )
    environment = dict(os.environ)
    environment["REPO_MAM_BASICS_DIR"] = str(paths.repo_root())
    environment["REPO_MAM_PARSED_DIR"] = str(paths.mam_parsed_dir())
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        str(interpreter),
        "-B",
        str(adapter),
        operation,
        "--public-python",
        sys.executable,
    ]
    return root, command, environment


def iter_source_books(book_ids=None):
    """Read source inputs unconditionally and project each book immediately.

    A subset is useful for differential checks. A production export always uses
    the complete canonical set. Neither this reader nor its adapter writes data.
    The strand of a layout marker that one strand of a dual-cantillation template
    has alone comes from public MAM-parsed, and the approved corrections of a
    marker's label from in/phonetic_mam_display_corrections.json.
    """
    expected = tuple(bib_locales.ALL_BK39_IDS if book_ids is None else book_ids)
    display_schema.require(
        bool(expected)
        and len(set(expected)) == len(expected)
        and all(book in bib_locales.ALL_BK39_IDS for book in expected),
        "unknown or duplicate requested book",
    )
    layouts = strand_layouts.read(paths.mam_parsed_plus_dir())
    marker_labels = display_corrections.read()["marker_labels"]
    root, command, environment = _adapter_command("books")
    for book in expected:
        command.extend(("--book39", book))
    with subprocess.Popen(
        command,
        cwd=root / "al-hatorah",
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    ) as process:
        stdout = _PipeReads(process.stdout)
        stderr = _StderrTail(process.stderr)
        watchdog = _Watchdog(process)
        try:
            for book_id in expected:
                line = stdout.read(watchdog.deadline, _MAX_BOOK_CHARS + 1, line=True)
                if not (line and len(line) <= _MAX_BOOK_CHARS and line.endswith("\n")):
                    raise _adapter_error(
                        process,
                        watchdog,
                        stderr,
                        "source adapter ended early or exceeded its book limit",
                    )
                value = json.loads(
                    line,
                    object_pairs_hook=_unique_object,
                    parse_constant=_reject_constant,
                )
                book = display_projection.project_book(
                    value, strand_layouts=layouts, marker_labels=marker_labels
                )
                del value
                display_schema.require(
                    book["book"] == book_id, "adapter book sequence differs"
                )
                yield book
            # A read past the deadline returns None and passes this check: the
            # watchdog has fired by then, and the next check names the limit.
            display_schema.require(
                not stdout.read(watchdog.deadline, 1), "unexpected adapter output"
            )
            if process.wait() != 0 or watchdog.fired:
                raise _adapter_error(process, watchdog, stderr, "source adapter failed")
        finally:
            _stop(process, watchdog, stdout, stderr)


def source_test_pages():
    """Parse the adapter's five rendered pages through the public-only parser."""
    root, command, environment = _adapter_command("test-pages")
    # Both pipes are read as bytes: _tail_text decodes stderr with "replace", as the
    # streaming run does, and stdout is decoded strictly only after a clean exit, so
    # that output that is not UTF-8 raises a UnicodeDecodeError.
    with subprocess.Popen(
        command,
        cwd=root / "al-hatorah",
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as process:
        stdout = _PipeReads(process.stdout)
        stderr = _StderrTail(process.stderr)
        watchdog = _Watchdog(process)
        try:
            data = stdout.read(watchdog.deadline)
            status = process.wait()
            watchdog.ended()
            tail = stderr.text(watchdog.deadline)
        finally:
            _stop(process, watchdog, stdout, stderr)
    if data is None or watchdog.fired:
        raise display_schema.PublicReleaseError(
            "test-page source adapter exceeded its"
            f" {_ADAPTER_TIME_LIMIT_SECONDS}-second limit and was stopped;"
            f" its stderr ended with:\n{tail}"
        )
    if status != 0:
        raise display_schema.PublicReleaseError(
            f"test-page source adapter failed (exit status {status});"
            f" its stderr ended with:\n{tail}"
        )
    text = data.decode("utf-8")
    display_schema.require(len(text) <= _MAX_BOOK_CHARS, "test-page input too large")
    value = json.loads(
        text, object_pairs_hook=_unique_object, parse_constant=_reject_constant
    )
    display_schema.require(
        isinstance(value, dict)
        and set(value) == {"schema", "pages"}
        and value["schema"] == "phonetic-mam-test-html-v1",
        "unknown test-page adapter shape",
    )
    display_schema.require(isinstance(value["pages"], list), "missing test-page input")
    by_name = {}
    for page in value["pages"]:
        display_schema.require(
            isinstance(page, dict)
            and set(page) == {"filename", "html"}
            and isinstance(page["html"], str),
            "unknown test-page input shape",
        )
        name = page["filename"]
        display_schema.require(isinstance(name, str), "test-page name must be text")
        display_schema.require(name not in by_name, "duplicate test-page input")
        by_name[name] = example_display.page_from_html(name, page["html"])
    display_schema.require(
        set(by_name) == set(example_display.PAGE_NAMES), "test-page set differs"
    )
    return example_display.validate(
        {
            "schema": example_display.SCHEMA_ID,
            "pages": [by_name[name] for name in example_display.PAGE_NAMES],
        }
    )


def _replace(path, payload):
    descriptor, name = tempfile.mkstemp(dir=path.parent, prefix=".export-")
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def export_release():
    """Replace the complete canonical release after every book passes validation."""
    # The retained values here are already the closed public projection, not a
    # rich intermediate. An adapter failure cannot leave a half-written corpus.
    payloads = {
        book["book"]: display_schema.canonical_bytes(book)
        for book in iter_source_books()
    }
    display_schema.require(
        tuple(payloads) == tuple(bib_locales.ALL_BK39_IDS), "incomplete export"
    )
    test_bytes = example_display.canonical_bytes(source_test_pages())
    output = paths.repo_root() / "Phonetic-MAM" / "data"
    output.mkdir(parents=True, exist_ok=True)
    names = {
        book: bib_locales.ordered_short_dash_full_39(book) + ".json"
        for book in payloads
    }
    display_schema.require(
        {path.name for path in output.iterdir()} <= set(names.values()),
        "unexpected existing release file",
    )
    examples = paths.repo_root() / "Phonetic-MAM" / "examples"
    examples.mkdir(parents=True, exist_ok=True)
    display_schema.require(
        {path.name for path in examples.iterdir()} <= {"display.json"},
        "unexpected existing example file",
    )
    for book, payload in payloads.items():
        _replace(output / names[book], payload)
    _replace(examples / "display.json", test_bytes)
    return (
        *tuple(output / names[book] for book in payloads),
        examples / "display.json",
    )
