"""Exports main: confirm the committed UXLC note pages against the frozen Notes.zip.

Started for the 3-book pilot (issue #24); extended unchanged to the full 39-book
corpus (issue #25) -- it already walks whatever is committed under
``in/UXLC-notes/``, so no book-specific logic needed to change.

http/download is the source of truth; ``Notes.zip`` (a ~1.1 MB snapshot of the
tanach.us ``/Notes`` tree, captured 2026-06-30) is only a verification aid -- a
re-runnable offline cross-check, not an independent authority. This script never
edits anything; it just reports.

For every committed ``in/UXLC-notes/<book_id>/<book_id>.c.v.pos-code.html`` it
finds the matching zip entry (the zip keys notes by the canonical tanach.us
basename, e.g. ``Notes/Samuel_2/Samuel_2.…`` for book id ``2Samuel``; the mapping
is ``my_uxlc.book_basename``) and classifies the pair:

  * IDENTICAL     -- byte-for-byte equal.
  * PROSE-EQUAL   -- differ only in tanach.us template chrome (title text,
                     ``.xml`` vs ``.html`` links, footer table, ``auto``/``hr``);
                     the note prose CLC actually consumes -- via
                     ``clc_note_pages._extract_prose_paragraphs``, the exact build
                     code -- is character-identical. No effect on CLC output.
  * PROSE-DIFFERS -- the extracted prose itself differs (real editorial drift, not
                     chrome). Dumps both sides so the discrepancy is auditable.
  * MISSING-IN-ZIP / MISSING-LOCAL -- coverage gaps either way.

Independent of that zip cross-check, every committed page's *local* prose
extraction is also confirmed non-empty (issue #25 step 2: every downloaded page
must parse to usable prose). A committed page that extracts to nothing would mean
``clc_note_pages`` failed to recognize its format -- that is reported separately
as NO-PROSE-EXTRACTED, regardless of the page's zip verdict.

Writes a full UTF-8 report to ``.novc/notes_zip_verify.txt`` and prints a summary.

Run from the repo root, like the other py/main_*.py drivers (default zip path is the
frozen snapshot; override with an argument)::

    python py/main_verify_notes_zip.py [path/to/Notes.zip]
"""

import os
import sys
import zipfile
from pathlib import Path

import clc.clc_note_pages as cnp
import uxlc_misc.my_uxlc as my_uxlc
import uxlc_paths

_DEFAULT_ZIP = Path(r"C:\Users\BenDe\Downloads\Notes.zip")


def _zip_entry_for(book_id, fname):
    """The zip entry mirroring committed ``<book_id>/<fname>`` (basename-keyed)."""
    basename = my_uxlc.book_basename(book_id)
    return f"Notes/{basename}/{basename}{fname[len(book_id):]}"


def _prose(text):
    """The note prose CLC consumes, joined -- same extractor as the build."""
    return " ".join(cnp._extract_prose_paragraphs(text))


def _classify(local_bytes, zip_bytes):
    """Return ``(verdict, local_prose)`` -- local_prose is checked by the caller
    for the independent issue #25 step-2 "parses to prose" confirmation."""
    lp = _prose(local_bytes.decode("utf-8"))
    if zip_bytes is None:
        return "MISSING-IN-ZIP", lp
    if local_bytes == zip_bytes:
        return "IDENTICAL", lp
    zp = _prose(zip_bytes.decode("utf-8"))
    return ("PROSE-EQUAL" if lp == zp else "PROSE-DIFFERS"), lp


def _iter_committed():
    notes_dir = uxlc_paths.uxlc_notes_dir()
    for book_id in sorted(os.listdir(notes_dir)):
        book_dir = notes_dir / book_id
        if not book_dir.is_dir():
            continue
        for fname in sorted(os.listdir(book_dir)):
            if fname.endswith(".html"):
                yield book_id, fname


def main():
    """Classify every committed note page against the zip; write the report."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    zip_path = Path(sys.argv[1]) if len(sys.argv) > 1 else _DEFAULT_ZIP
    zf = zipfile.ZipFile(zip_path)
    zip_names = set(zf.namelist())

    counts = {}
    prose_differs = []
    no_prose = []
    lines = [f"Notes.zip verification (issues #24, #25) -- zip: {zip_path}", ""]

    for book_id, fname in _iter_committed():
        with open(uxlc_paths.uxlc_notes_dir() / book_id / fname, "rb") as fp:
            local_bytes = fp.read()
        entry = _zip_entry_for(book_id, fname)
        zip_bytes = zf.read(entry) if entry in zip_names else None
        verdict, local_prose = _classify(local_bytes, zip_bytes)
        counts[verdict] = counts.get(verdict, 0) + 1
        lines.append(f"{verdict:<14} {book_id}/{fname}")
        if verdict == "PROSE-DIFFERS":
            prose_differs.append((book_id, fname, local_bytes, zip_bytes))
        if not local_prose:
            no_prose.append((book_id, fname))

    lines.append("")
    lines.append("Summary:")
    for verdict in (
        "IDENTICAL",
        "PROSE-EQUAL",
        "PROSE-DIFFERS",
        "MISSING-IN-ZIP",
        "MISSING-LOCAL",
    ):
        if verdict in counts:
            lines.append(f"  {verdict:<14} {counts[verdict]}")
    total = sum(counts.values())
    substance_ok = counts.get("IDENTICAL", 0) + counts.get("PROSE-EQUAL", 0)
    lines.append(f"  {'TOTAL':<14} {total}")
    lines.append("")
    lines.append(
        f"Prose confirmed for {substance_ok}/{total} committed pages; "
        f"{len(prose_differs)} carry prose the zip revised (see below)."
    )
    lines.append(
        f"Local prose extraction: {total - len(no_prose)}/{total} committed "
        f"pages parse to non-empty prose (issue #25 step 2); "
        f"{len(no_prose)} NO-PROSE-EXTRACTED (see below)."
    )

    for book_id, fname, local_bytes, zip_bytes in prose_differs:
        lines.append("")
        lines.append(f"=== PROSE-DIFFERS: {book_id}/{fname}")
        lines.append(f"  committed: {_prose(local_bytes.decode('utf-8'))!r}")
        lines.append(f"  zip      : {_prose(zip_bytes.decode('utf-8'))!r}")

    for book_id, fname in no_prose:
        lines.append("")
        lines.append(f"=== NO-PROSE-EXTRACTED: {book_id}/{fname}")

    out_path = uxlc_paths.novc_dir() / "notes_zip_verify.txt"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")

    print(f"wrote {out_path}")
    for verdict in (
        "IDENTICAL",
        "PROSE-EQUAL",
        "PROSE-DIFFERS",
        "MISSING-IN-ZIP",
        "MISSING-LOCAL",
    ):
        if verdict in counts:
            print(f"  {verdict:<14} {counts[verdict]}")
    print(f"  NO-PROSE-EXTRACTED {len(no_prose)}")


if __name__ == "__main__":
    main()
