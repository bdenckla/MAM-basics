"""Census of MAM's doc-notes in Psalms, each with its chapter and verse, written to
``out/mam_psalms_docnotes.tsv``.

A doc-note is a נוסח template. The census reads ``MAM-parsed/plus/D1-Psalms.json`` as it
stands, cell by cell of each verse's minirow, and finds the doc-notes in each cell with
``explicit_xataf.extract.find_docnote_tmpls``, this repository's closed dispatch for
doc-note discovery: it validates every other template against
``mb_cmn.template_names.CURRENT_PLUS_PARAM_POLICY`` and raises on one it does not know. A
doc-note is credited to the verse whose minirow holds it, so one in a verse's first cell,
before the verse's text, counts toward that verse.

Until 2026-09-26 the census walked every parameter of every template itself and took any
template whose name contains הערה, which caught the 8 מ:קישור בהערה link templates that sit
inside notes: 628 rows where there are 620 doc-notes.
"""

import json

from explicit_xataf import extract
from hbce_psalms import hbce_paths

HEADER = "path\ttmpl\ttarget\tnote\tother"


def _psalms_chapters() -> dict:
    """The chapters of the one book in D1-Psalms.json, checking the file's shape."""
    data = json.loads(hbce_paths.mpplus_psalms_json().read_text(encoding="utf-8"))
    (book,) = data["book39s"]
    expected = {"book24_name", "sub_book_name", "good_ending_plus", "chapters"}
    if set(book) != expected:
        raise ValueError(f"unexpected keys in D1-Psalms.json's book: {sorted(book)}")
    if book["sub_book_name"] is not None or book["good_ending_plus"] is not None:
        raise ValueError("D1-Psalms.json has a sub-book name or a good ending")
    return book["chapters"]


def docnote_rows() -> list[str]:
    """One TSV line per doc-note, in the order the file has them."""
    rows = []
    for chapter, verses in _psalms_chapters().items():
        for verse, minirow in verses.items():
            if not isinstance(minirow, list) or len(minirow) != 3:
                raise ValueError(f"Psalms {chapter}:{verse} has no three-cell minirow")
            for cell in minirow:
                for tmpl in extract.find_docnote_tmpls(cell):
                    params = tmpl.get("tmpl_params", {})
                    target = params.get("1", "")
                    note = json.dumps(params.get("2", ""), ensure_ascii=False)
                    other = {k: v for k, v in params.items() if k not in ("1", "2")}
                    other_json = json.dumps(other, ensure_ascii=False) if other else ""
                    rows.append(
                        f"{chapter}.{verse}\t{tmpl['tmpl_name']}\t{target}\t{note}"
                        f"\t{other_json}"
                    )
    return rows


def write_docnotes() -> int:
    """Write ``out/mam_psalms_docnotes.tsv``; return the number of doc-notes."""
    rows = docnote_rows()
    text = "".join(line + "\n" for line in [HEADER, *rows])
    path = hbce_paths.out_dir() / "mam_psalms_docnotes.tsv"
    path.write_text(text, encoding="utf-8", newline="\n")
    return len(rows)
