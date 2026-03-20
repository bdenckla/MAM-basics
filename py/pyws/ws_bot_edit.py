"""Bot edit: apply edits described by a JSON specification file.

The JSON file has:
  "summary"   : the Wikisource edit summary string
  "edit-kind" : the type of edit (currently only "meteg-removal")
  "edits"     : a dict mapping bk39id to a list of edit objects

Each edit object has:
  "ch"      : Hebrew chapter key
  "old"     : old string that must appear exactly once in the chapter
  "comment" : (optional) human-readable note

For "meteg-removal", the replacement removes the first meteg (U+05BD)
from old_string.

See ws_bot_edit_history.md for a record of previous bots.
The immediately preceding bot is preserved as
ws_bot_edit_old_joshua_meteg.py.
"""

import json

from pycmn import hebrew_points as hpo
from pyws import ws_get_bk_in_both_fmts as wsin
from pyws import ws_fmt_2_back_to_wikitext as btw


def _meteg_removal(old):
    return old.replace(hpo.MTGOSLQ, "", 1)


_EDIT_KIND_FNS = {
    "meteg-removal": _meteg_removal,
}


def _build_edits_by_book_and_chapter(edit_kind_fn, raw_edits):
    """Group (old, new) pairs by (bk39id, chapter_key)."""
    result = {}
    for bk39id, edit_list in raw_edits.items():
        by_chap = {}
        for entry in edit_list:
            old = entry["old"]
            new = edit_kind_fn(old)
            by_chap.setdefault(entry["ch"], []).append((old, new))
        result[bk39id] = by_chap
    return result


def load_edits(json_path):
    """Load edit specification from JSON. Returns an edits context dict."""
    with open(json_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    summary = spec["summary"]
    edit_kind_fn = _EDIT_KIND_FNS[spec["edit-kind"]]
    edits_by_bk_ch = _build_edits_by_book_and_chapter(edit_kind_fn, spec["edits"])
    return {"summary": summary, "edits-by-bk-ch": edits_by_bk_ch}


def no_edits():
    """Return an empty edits context (no-op pass-through)."""
    return {"summary": "", "edits-by-bk-ch": {}}


def _get_chapter_edits(edits_ctx, bk39id, he_chnu):
    return edits_ctx["edits-by-bk-ch"].get(bk39id, {}).get(he_chnu, [])


def edit_page_text(edits_ctx, bk39id, he_chnu, page_text):
    """Apply edits to a chapter's raw page text."""
    for old, new in _get_chapter_edits(edits_ctx, bk39id, he_chnu):
        count = page_text.count(old)
        assert count == 1, (
            f"Expected 1 occurrence of {old!r} in {bk39id} chapter {he_chnu},"
            f" found {count}"
        )
        page_text = page_text.replace(old, new)
    return page_text


def edit_cif2(edits_ctx, bk39id, he_chnu, cif2):
    """Apply edits via the format-2 roundtrip."""
    big = btw.big_str(he_chnu, cif2)
    edited = edit_page_text(edits_ctx, bk39id, he_chnu, big)
    edited_cif2 = wsin.get_chap_in_fmt_2(edited.splitlines())
    return edited_cif2, edited
