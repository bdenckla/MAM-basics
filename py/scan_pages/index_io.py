"""Read and write the tracked per-edition index JSONs."""

import json

from mb_cmn import file_io
from mb_cmn import provenance
from scan_pages import editions

# The page-level half of lci_recs.json's column dictionary, carried here so an index
# file explains itself to a reader who has never seen the Leningrad one.  The line and
# column fields that file has as nulls are absent rather than null: this index is
# deliberately page-level, and a null column would read as "not filled in yet".
REC_FIELDS = {
    "page": "the file name of the page this record is about (str)",
    "bkid": "book ID, e.g. 'Levit' (see py/mb_cmn/bib_locales.py) (str)",
    "startc": "start chapter (int or null)",
    "startv": "start verse (int or null)",
    "startp": "start atom within the verse, 1-based (int or null)",
    "stopc": "stop chapter (int or null)",
    "stopv": "stop verse (int or null)",
    "stopp": "stop atom within the verse, 1-based (int or null)",
    "start_phrase": "letters-only phrase read off the top of the page (str or null)",
    "stop_phrase": "letters-only phrase read off the foot of the page (str or null)",
    "note": "free-form text (str or null)",
}

_HEADER_NOTE = (
    "Page-level index of one scanned printed edition. The plan, the findings and the"
    " conventions are doc/scan-pages.md. A page may carry more than one record: a page"
    " where one book ends and the next begins gets one record per book."
)


def make_index(edition_id, pages, recs, segments):
    """Return one edition's index, ready to be written."""
    return {
        "edition": edition_id,
        "folder": editions.folder_name(edition_id),
        "note": _HEADER_NOTE,
        "rec-fields": REC_FIELDS,
        "pages": pages,
        "segments": segments,
        "recs": recs,
    }


def write_index(edition_id, index):
    """Write one edition's index to its tracked path."""
    out_path = editions.index_path(edition_id)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # The logical repo name is passed rather than left to default, so that the
    # breadcrumb says MAM-basics even when the generator runs from a worktree, whose
    # directory name would otherwise be baked into a tracked file.
    dumpable = provenance.with_json_provenance(index, __file__, "MAM-basics")
    file_io.json_dump_to_file_path(dumpable, str(out_path))


def read_index(edition_id):
    """Read one edition's tracked index."""
    with editions.index_path(edition_id).open(encoding="utf-8") as in_fp:
        return json.load(in_fp)
