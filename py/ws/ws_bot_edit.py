"""Bot edit: apply edits described by a JSON specification file.

The JSON file has:
  "summary"   : the Wikisource edit summary string
  "edit-kind" : the type of edit
  "edits"     : a dict mapping bk39id to a list of edit objects
                (used only for per-occurrence kinds; omit or set to {}
                for global-transform kinds)

For "meteg-removal" (a per-occurrence kind):
  Each edit object has:
    "ch"      : Hebrew chapter key
    "old"     : old string that must appear exactly once in the chapter
    "comment" : (optional) human-readable note
  The replacement removes the first meteg (U+05BD) from old_string.

For "kq-trivial-to-kq-trivial-2" (a global-transform kind):
  Replaces every {{קו"כ-אם}} call with {{מ:קו"כ-אם-2}} across all
  chapters, via a full cif2 AST traversal. No per-occurrence entries
  are needed; "edits" may be omitted or set to {}.

For "kq-trivial-2-add-type-tags" (a global-transform kind):
    Adds סוג=... to {{מ:קו"כ-אם-2}} for five named trivial k/q
    subtypes, while leaving subtype misc untagged.

See ws_bot_edit_history.md for a record of previous bots.
The immediately preceding bot is preserved as
ws_bot_edit_old_kq_triv_to_2.py.
"""

import json

from mb_cmn import file_io
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import hebrew_points as hpo
from ws import ws_get_bk_in_both_fmts as wsin
from ws import ws_fmt_2_back_to_wikitext as btw
from ws import ws_bot_edit_kq_triv_to_2 as kq2
from ws import ws_bot_edit_kq_triv_add_type as kq2_tag


def _meteg_removal(old):
    return old.replace(hpo.MTGOSLQ, "", 1)


_EDIT_KIND_FNS = {
    "meteg-removal": _meteg_removal,
}

_GLOBAL_TRANSFORM_KINDS = {
    "kq-trivial-to-kq-trivial-2": {
        "fn": kq2.edit_page_text,
        "get_warnings": kq2.get_warnings,
    },
    "kq-trivial-2-add-type-tags": {
        "fn": kq2_tag.edit_page_text,
        "get_warnings": kq2_tag.get_warnings,
    },
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
    edit_kind = spec["edit-kind"]
    if edit_kind in _GLOBAL_TRANSFORM_KINDS:
        gt = _GLOBAL_TRANSFORM_KINDS[edit_kind]
        return {
            "summary": summary,
            "edits-by-bk-ch": {},
            "global-page-transform": gt["fn"],
            "get-warnings": gt["get_warnings"],
            "modified-chapters": [],
        }
    edit_kind_fn = _EDIT_KIND_FNS[edit_kind]
    edits_by_bk_ch = _build_edits_by_book_and_chapter(edit_kind_fn, spec["edits"])
    return {
        "summary": summary,
        "edits-by-bk-ch": edits_by_bk_ch,
        "modified-chapters": [],
    }


def no_edits():
    """Return an empty edits context (no-op pass-through)."""
    return {"summary": "", "edits-by-bk-ch": {}, "modified-chapters": []}


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
    if gpt := edits_ctx.get("global-page-transform"):
        page_text = gpt(bk39id, he_chnu, page_text)
    return page_text


def write_warnings(edits_ctx, path):
    """Write accumulated warnings to a JSON file, if any."""
    get_warnings = edits_ctx.get("get-warnings")
    if get_warnings is None:
        return
    warnings = get_warnings()
    file_io.json_dump_to_file_path(warnings, path)


def write_modified_chapters(edits_ctx, path):
    """Write the list of modified book/chapter pairs to a JSON file.

    The output format matches the --book-chapters-json input of
    main_download.py fr-wikisource: a list of {"book39": ..., "chapter": ...}
    objects with integer chapter numbers.
    """
    modified = edits_ctx["modified-chapters"]
    entries = [
        {"book39": bk39id, "chapter": hvn.STR_TO_INT_DIC[he_chnu]}
        for bk39id, he_chnu in modified
    ]
    file_io.json_dump_to_file_path(entries, path)


def edit_cif2(edits_ctx, bk39id, he_chnu, cif2):
    """Apply edits via the format-2 roundtrip."""
    big = btw.big_str(he_chnu, cif2)
    edited = edit_page_text(edits_ctx, bk39id, he_chnu, big)
    if edited != big:
        edits_ctx["modified-chapters"].append((bk39id, he_chnu))
    edited_cif2 = wsin.get_chap_in_fmt_2(edited.splitlines())
    return edited_cif2, edited
