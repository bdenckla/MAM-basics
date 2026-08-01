"""Wrap the line editor's export(s) into the committed JSON, and derive the .txt body.

    # a new transcription: both jobs at once
    .venv/Scripts/python.exe py/main_edition_transcription.py build simtan_ex_elyon \
        --export ~/Downloads/simtan_ex_elyon_p350-transcription.json \
        --corrections .novc/ex_elyon_corrections.json

    # after a post-export correction or a header edit: re-derive from the committed JSON
    .venv/Scripts/python.exe py/main_edition_transcription.py build simtan_ex_elyon \
        --derive-only

    # idempotence: re-derive every committed stem and report any that would change
    .venv/Scripts/python.exe py/main_edition_transcription.py build --check

The two jobs of ``doc/edition-transcription-workflow.md`` section 4, which had been done by a
throwaway script rewritten once per transcription -- thirteen of them by the time this was
written (wlc-utils#72).  JOB 1 wraps the editor's downloaded export(s) into the committed
JSON, applying corrections and uncertain readings and adding the ``pages`` wrapper when a
Decalogue spans two printed pages.  JOB 2 derives the .txt body from that JSON through
``edition_transcription.txt_lines``, under the .txt's hand-written header.

THE DUPLICATION WAS NOT HARMLESS, which is why this exists at all.  The last two copies had
already diverged on the trailing-empty-line rule below, and that is a difference in what gets
committed, not in style.  The guarantee that .txt and JSON say the same thing is enforced
mechanically either way (``test_editor_export_and_txt_agree``), so this is ergonomics rather
than safety -- but a rule that lives in a deleted scratch file is a rule the next transcription
has to rediscover.

THE HEADER STAYS IN THE .txt AND IS NEVER REWRITTEN.  Only the body beneath it is derived.
The alternative -- a separate committed header file -- would commit the same prose twice and
invite its own drift, and keeping the header in place is what makes ``--check`` a true
idempotence test: re-derive the body from the committed JSON and the whole file must come back
byte for byte.  ``py/tests/test_edition_transcriptions.py`` runs that check over every stem.

WHERE CORRECTIONS LIVE, and why they are not committed.  ``--corrections`` and ``--uncertain``
take throwaway files (write them in the gitignored ``.novc/``), not a git-tracked sidecar per
stem.  The committed JSON is already the durable record: an applied correction keeps the
superseded reading in ``corrected_from``, so both the new reading and the old one are in the
audit trail, and a tracked sidecar would be a third copy of the same two strings -- the same
argument that keeps the header out of its own file.  The supported re-run is therefore
``--derive-only`` from the committed JSON, not a rebuild from raw Downloads exports; a rebuild
is possible but is a fresh reading of the correction list, not a replay of one.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path

import wlc_paths
from accgram import edition_transcription as et

# A page label is the export stem's last underscore-separated part -- "p298" for
# simtan_dt_taxton_p298 -- which is what transcription_check reports a difference's
# origin as, so a correction is keyed by the same label the check tool named it with.
_PAGE_NUMBER = re.compile(r"^p(\d+)$")


def pages_of(record: dict) -> list[dict]:
    """A multi-page audit trail holds one export per page; a single-page one is its own page."""
    return record.get("pages", [record])


def page_label(page: dict) -> str:
    """The short label for one page's export -- "p298" -- as transcription_check reports it."""
    return page.get("stem", "?").split("_")[-1]


def _page_marker(page: dict) -> str:
    """The ``[p. 298]`` line that opens a second or later page in the .txt body.

    Raises rather than falling back when the export's stem does not end in ``_p<number>``:
    a marker reading ``[p. C246-right]`` would be a positional aside no vocabulary knows,
    and ``load_transcription`` would carry it into the committed file unchallenged.
    """
    label = page_label(page)
    match = _PAGE_NUMBER.match(label)
    if match is None:
        raise ValueError(
            f"export stem {page.get('stem')!r} does not end in _p<number>,"
            f" so its printed page number cannot be read off it"
        )
    return f"[p. {match.group(1)}]"


def body_lines(record: dict) -> list[str]:
    """The .txt body: one line per printed line, a marker where each later page begins.

    TRAILING empty lines are dropped per page, INTERIOR ones kept.  A band that carries no
    accent contributes an empty .txt line, and since the editor is now built over the whole
    page by default (workflow doc section 1), its bands run past the Decalogue's end -- eleven
    of them on p. 298, cleared as out of span.  Those are noise at the foot of a page.  An
    interior empty line is not: it is a printed line that really carries no accent, and
    dropping it would shift every line number after it away from the printed page.
    """
    out: list[str] = []
    for i, page in enumerate(pages_of(record)):
        if i:
            out += ["", _page_marker(page)]
        lines = et.txt_lines([line["text"] for line in page["lines"]])
        while lines and not lines[-1].strip():
            lines.pop()
        out += lines
    return out


def header_lines(text: str) -> list[str]:
    """A committed .txt's header: everything above its first body line.

    The header is prose comments plus ``key: value`` fields, written by hand, and this tool
    never touches it -- so the split has to agree with what ``load_transcription`` treats as a
    field, or a line could be preserved as header AND regenerated as body.  Both call
    ``et.is_header_field``; only blank lines and ``#`` comments are recognized here in
    addition, since neither reaches the parser at all.

    Trailing blank lines are trimmed, the writer putting back exactly one.
    """
    kept: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if (
            stripped
            and not stripped.startswith("#")
            and not et.is_header_field(stripped)
        ):
            break  # the first body line
        kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    return kept


def txt_path(stem: str) -> Path:
    return et.transcriptions_dir() / f"{stem}.txt"


def json_path(stem: str) -> Path:
    return et.transcriptions_dir() / f"{stem}.json"


def rendered(header: list[str], record: dict) -> str:
    """The whole .txt: the header verbatim, one blank line, then the derived body."""
    body = body_lines(record)
    lines = header + [""] + body if header else body
    return "\n".join(lines) + "\n"


def derived_text(stem: str) -> str:
    """What the committed .txt would be, re-derived from the committed JSON beside it.

    The idempotence claim in one function, so the tool's ``--check`` and the test suite make
    the same claim rather than two similar ones.
    """
    record = json.loads(json_path(stem).read_text(encoding="utf-8"))
    return rendered(header_lines(txt_path(stem).read_text(encoding="utf-8")), record)


def _keyed_by_page(path: Path | None, pages: list[dict], what: str) -> dict:
    """Load a ``{page label: {line number: value}}`` file, checked against the actual pages.

    An unknown page label or line number RAISES.  A mis-keyed correction that silently applies
    to nothing is exactly the failure this tool is meant to remove: the reading it was written
    for stays uncorrected in the committed JSON, and nothing says so.
    """
    if path is None:
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    known = {page_label(page): {line["n"] for line in page["lines"]} for page in pages}
    out: dict[tuple[str, int], object] = {}
    for label, entries in raw.items():
        if label not in known:
            raise ValueError(
                f"{path.name}: {what} keyed to page {label!r},"
                f" but the exports given are {sorted(known)}"
            )
        for number, value in entries.items():
            if int(number) not in known[label]:
                raise ValueError(
                    f"{path.name}: {what} keyed to {label} line {number},"
                    f" which that export has no band for"
                )
            out[(label, int(number))] = value
    return out


def wrap(
    export_paths: list[Path], corrections_path: Path | None, uncertain_path: Path | None
) -> dict:
    """Job 1: the downloaded exports, corrected, in page order.

    More than one export gets the ``pages`` wrapper; a single-page Decalogue is committed as
    the bare export, which is how every single-page transcription already stands.  A
    correction moves the superseded reading into ``corrected_from`` rather than replacing it,
    so the audit trail records what it replaced -- including a band cleared as out of span,
    where what was typed is the thing worth keeping.
    """
    pages = [json.loads(path.read_text(encoding="utf-8")) for path in export_paths]
    corrections = _keyed_by_page(corrections_path, pages, "a correction")
    uncertain = _keyed_by_page(uncertain_path, pages, "an uncertain reading")
    for page in pages:
        label = page_label(page)
        print(f"  {label}: {len(page['lines'])} bands")
        for line in page["lines"]:
            fixed = corrections.get((label, line["n"]))
            if fixed is not None:
                if fixed == line["text"]:
                    print(
                        f"    line {line['n']}: already reads as corrected, left alone"
                    )
                else:
                    line["corrected_from"] = line["text"]
                    line["text"] = fixed
                    print(
                        f"    line {line['n']}: {line['corrected_from']!r} -> {fixed!r}"
                    )
            entries = uncertain.get((label, line["n"]))
            if entries:
                line["uncertain"] = entries
    return {"pages": pages} if len(pages) > 1 else pages[0]


def _write(path: Path, text: str) -> None:
    """Write a committed file as LF.

    ``newline="\\n"`` is not optional: .gitattributes pins LF in the WORKDIR too (#50), and
    Path.write_text in text mode would translate to CRLF on Windows.
    """
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(wlc_paths.wlc_data_root())}")


def _warn_dropped_keys(path: Path, record: dict) -> None:
    """Name any top-level key a rebuild would drop from an existing committed JSON.

    A rebuild writes the wrapper this tool knows about and nothing else, so a hand-added
    top-level field would go with it -- simtiq_dt_elyon.json carries a ``note`` and a
    ``stem`` beside its ``pages``.  Printed rather than refused: rebuilding an already
    committed stem is the rare path, and the loss is recoverable from git as long as somebody
    is told it happened.
    """
    if not path.exists():
        return
    dropped = sorted(set(json.loads(path.read_text(encoding="utf-8"))) - set(record))
    if dropped:
        print(f"  NOTE: rebuilding drops top-level key(s) {dropped} from {path.name}")


def _report_uncertain(record: dict) -> None:
    flagged = et.uncertain_readings(pages_of(record))
    print(f"  uncertain readings: {len(flagged)}")
    for entry in flagged:
        print(
            f"    {entry['page']} line {entry['line']}: {entry['word']} = {entry['reading']}"
        )


def check(stems: list[str]) -> int:
    """Re-derive each stem's .txt from its committed JSON and report any that would change."""
    stale = 0
    for stem in stems:
        committed = txt_path(stem).read_text(encoding="utf-8")
        derived = derived_text(stem)
        if derived == committed:
            print(f"  ok    {stem}")
            continue
        stale += 1
        print(f"  STALE {stem}")
        diff = difflib.unified_diff(
            committed.splitlines(),
            derived.splitlines(),
            "committed",
            "derived",
            lineterm="",
        )
        for line in list(diff)[:20]:
            print(f"        {line}")
    print(
        f"{len(stems) - stale}/{len(stems)} committed .txt bodies are the derived ones"
    )
    return 1 if stale else 0


def _committed_stems() -> list[str]:
    return sorted(p.stem for p in et.transcriptions_dir().glob("*.json"))


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    # repo_root is unused: the committed transcriptions are located through
    # ``edition_transcription.transcriptions_dir``, and an export is named on the command
    # line.  The parameter is here so the entry point wires every subcommand the same way.
    del repo_root
    parser.add_argument(
        "stem",
        nargs="?",
        help="transcription stem; omit only with --check, for all of them",
    )
    parser.add_argument(
        "--export",
        type=Path,
        nargs="+",
        help="the line editor's downloaded export(s), one per page, IN PAGE ORDER",
    )
    parser.add_argument(
        "--corrections",
        type=Path,
        help='JSON {"p298": {"15": "<the corrected editor text>"}}; the superseded reading'
        " is kept in the export's corrected_from",
    )
    parser.add_argument(
        "--uncertain",
        type=Path,
        help='JSON {"p298": {"15": [{"word": ..., "reading": ..., "why": ...}]}}',
    )
    parser.add_argument(
        "--derive-only",
        action="store_true",
        help="re-derive the .txt body from the already-committed JSON, writing no JSON",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="write nothing: report whether each committed .txt is its own derived body",
    )


def run(args: argparse.Namespace) -> int:
    """The subcommand, returning the exit code ``--check`` gates on.

    The return value is an int, not None: ``--check`` is an idempotence gate, and the entry
    point's ``raise SystemExit(args.func(args) or 0)`` is what carries a stale stem's 1 out
    to the shell.
    """
    if args.check:
        return check([args.stem] if args.stem else _committed_stems())
    if not args.stem:
        # The two completeness rules were ``parser.error`` calls while this module owned its
        # own parser; as a subcommand it cannot reach the parser, so they are raised the way
        # ``scan_page`` and ``transcription_check`` raise theirs.
        raise SystemExit(
            "build: error: a stem is required unless --check is asking about all of them"
        )
    if args.derive_only:
        record = json.loads(json_path(args.stem).read_text(encoding="utf-8"))
    else:
        if not args.export:
            raise SystemExit("build: error: --export is required unless --derive-only")
        record = wrap(args.export, args.corrections, args.uncertain)
        _warn_dropped_keys(json_path(args.stem), record)
        _write(
            json_path(args.stem),
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
        )

    txt = txt_path(args.stem)
    if not txt.exists():
        print(
            f"  (no {txt.name} yet -- body written with no header, to write one above)"
        )
        header: list[str] = []
    else:
        header = header_lines(txt.read_text(encoding="utf-8"))
    _write(txt, rendered(header, record))
    _report_uncertain(record)
    return 0
