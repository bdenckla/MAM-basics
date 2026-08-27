"""Bot edit: apply edits described by a JSON specification file.

The JSON file has:
  "summary"   : the Wikisource edit summary string
  "edit-kind" : the type of edit
  "edits"     : a dict mapping bk39id to a list of edit objects
                (used only for per-occurrence kinds; omit or set to {}
                for global-transform kinds)

For "meteg-removal" (a chapter-targeted kind):
  Each edit object has:
    "ch"      : Hebrew chapter key
    "old"     : old string that must appear exactly once in the chapter
    "comment" : (optional) human-readable note
  The replacement removes the first meteg (U+05BD) from old_string.

For "explicit-replacement" (a chapter-targeted kind):
    Each edit object has:
        "ch"      : Hebrew chapter key
        "old"     : old string that must appear exactly once in the chapter
        "new"     : replacement string
        "comment" : (optional) human-readable note

For "kq-trivial-to-kq-trivial-2" (an untargeted kind):
  Replaces every {{קו״כ-אם}} call with {{מ:קו״כ-אם-2}} across all
  chapters, via a full cif2 AST traversal. No per-occurrence entries
  are needed; "edits" may be omitted or set to {}.

For "kq-trivial-2-rename-extra-alef-sug" (an untargeted kind):
    Renames סוג=אל"ף מיותרת to סוג=אל"ף נחה באמצע תיבה ולא נקראת
    on {{מ:קו״כ-אם-2}} calls.

For "kuk-special-callsite-migration" (an untargeted kind):
    Migrates call sites of nine deprecated issue-67 כו״ק template names
    to {{מ:כו״ק מיוחד|...|סוג=...}}, preserving existing params.
    Hard-preflights for רווח=כן and fails fast for manual handling.

For "sigil-b2-to-t451" (an untargeted kind):
    Replaces the manuscript sigil ב2 with ת451, the two being two sigils
    for one manuscript, per MAM-basics#260. Guarded by a per-chapter
    expected-count table -- 32 occurrences over six chapters of Daniel --
    so a chapter the table does not name passes through untouched, and
    by an assertion that the page carries no aliyah |ב2= parameter.

Terminology:
    - chapter-targeted: explicit edit objects keyed by chapter
    - untargeted: no explicit per-chapter edit list; transform runs on each
        selected chapter

See ws_bot_edit_history.md for a record of previous bots.
The immediately preceding bot is preserved as
ws_bot_edit_old_kq_triv_add_type.py.
"""

import json

from mb_cmn import file_io
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import hebrew_points as hpo
from mb_cmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from ws import ws_get_bk_in_both_fmts as wsin
from ws import ws_fmt_2_back_to_wikitext as btw
from ws import ws_bot_edit_kq_triv_rename_extra_alef_sug as kq2_rename
from ws import ws_bot_edit_kq_triv_to_2 as kq2
from ws import ws_bot_edit_kuk_special_callsite_migration as kuk67
from ws import ws_bot_edit_sigil_b2_to_t451 as sigil_b2


def _meteg_removal(entry):
    old = entry["old"]
    return old, old.replace(hpo.MTGOSLQ, "", 1)


def _explicit_replacement(entry):
    return entry["old"], entry["new"]


_CHAPTER_TARGETED_EDIT_KIND_FNS = {
    "meteg-removal": _meteg_removal,
    "explicit-replacement": _explicit_replacement,
}

_UNTARGETED_EDIT_KINDS = {
    "kq-trivial-to-kq-trivial-2": {
        "fn": kq2.edit_page_text,
        "get_warnings": kq2.get_warnings,
    },
    "kq-trivial-2-rename-extra-alef-sug": {
        "fn": kq2_rename.edit_page_text,
        "get_warnings": kq2_rename.get_warnings,
    },
    "kuk-special-callsite-migration": {
        "fn": kuk67.edit_page_text,
        "get_warnings": kuk67.get_warnings,
    },
    "sigil-b2-to-t451": {
        "fn": sigil_b2.edit_page_text,
        "get_warnings": sigil_b2.get_warnings,
    },
}


def _build_edits_by_book_and_chapter(edit_kind_fn, raw_edits):
    """Group (old, new) pairs by (bk39id, chapter_key)."""
    result = {}
    for bk39id, edit_list in raw_edits.items():
        by_chap = {}
        for entry in edit_list:
            old, new = edit_kind_fn(entry)
            by_chap.setdefault(entry["ch"], []).append((old, new))
        result[bk39id] = by_chap
    return result


def _allowed_book_chapter_pairs(edits_by_bk_ch):
    return {
        (bk39id, he_chnu)
        for bk39id, by_chap in edits_by_bk_ch.items()
        for he_chnu in by_chap
    }


def load_edits(json_path):
    """Load edit specification from JSON. Returns an edits context dict."""
    with open(json_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    summary = spec["summary"]
    edit_kind = spec["edit-kind"]
    if edit_kind in _UNTARGETED_EDIT_KINDS:
        gt = _UNTARGETED_EDIT_KINDS[edit_kind]
        return {
            "summary": summary,
            "edits-by-bk-ch": {},
            "is-chapter-targeted": False,
            "allowed-book-chapter-pairs": set(),
            "global-page-transform": gt["fn"],
            "get-warnings": gt["get_warnings"],
            "modified-chapters": [],
        }
    edit_kind_fn = _CHAPTER_TARGETED_EDIT_KIND_FNS[edit_kind]
    edits_by_bk_ch = _build_edits_by_book_and_chapter(edit_kind_fn, spec["edits"])
    return {
        "summary": summary,
        "edits-by-bk-ch": edits_by_bk_ch,
        "is-chapter-targeted": True,
        "allowed-book-chapter-pairs": _allowed_book_chapter_pairs(edits_by_bk_ch),
        "modified-chapters": [],
    }


def no_edits():
    """Return an empty edits context (no-op pass-through)."""
    return {
        "summary": "",
        "edits-by-bk-ch": {},
        "is-chapter-targeted": False,
        "allowed-book-chapter-pairs": set(),
        "modified-chapters": [],
    }


def _selected_book_chapter_pairs(book_plans):
    selected = set()
    for he_bn_sbn, he_chnus in book_plans:
        bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
        for he_chnu in he_chnus:
            selected.add((bk39id, he_chnu))
    return selected


def _pairs_with_int_chapters(pairs):
    return sorted((bk39id, hvn.STR_TO_INT_DIC[he_chnu]) for bk39id, he_chnu in pairs)


def _format_pairs_for_error(pairs, max_show=12):
    pairs_i = _pairs_with_int_chapters(pairs)
    preview = ", ".join(f"{bk39id} {chapter}" for bk39id, chapter in pairs_i[:max_show])
    if len(pairs_i) > max_show:
        preview += f", ... (+{len(pairs_i) - max_show} more)"
    return f"{len(pairs_i)} chapter(s): {preview}"


def assert_book_plans_within_target_set(edits_ctx, book_plans):
    """Fail if a chapter-targeted edit is requested outside its target set."""
    if not edits_ctx.get("is-chapter-targeted", False):
        return
    selected = _selected_book_chapter_pairs(book_plans)
    allowed = edits_ctx["allowed-book-chapter-pairs"]
    outside = selected - allowed
    if not outside:
        return
    outside_txt = _format_pairs_for_error(outside)
    allowed_txt = _format_pairs_for_error(allowed)
    raise SystemExit(
        "Selector includes chapters outside this edit spec target set: "
        f"{outside_txt}. Allowed chapters are: {allowed_txt}"
    )


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
