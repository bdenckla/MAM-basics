"""
Load MAM-parsed-plus JSON from git revisions and extract EP column body text.

Exports:
    diff_all_books — compare all books between two revisions
"""

import json

from mb_diff_mpu import mpplus_revisions
from mb_cmn import template_names as tmpln
from mb_cmn import ws_tmpl2
from mb_diff_mpu.mpplus_file_matching import (
    book39_ids_for_stem,
    get_he_to_int,
    matched_plus_file_pairs,
)
from mb_diff_mpu.mpplus_flatten import (
    find_relevant_docnote,
    flatten_ep_with_docnote_for_diff,
    flatten_ep_for_diff,
    flatten_ep_words_only_for_diff,
)
from mb_diff_mpu.mpplus_param_access import MISSING, get_param
from mb_diff_mpu.mpplus_structure import (
    structural_signature,
    template_name_counter,
)

_DROP = object()


def _git_show(rev, path):
    """Read a stored or Git-backed plus input; an absent input is a hard error."""
    return mpplus_revisions.resolve(rev).read(path.removeprefix("plus/"))


def _canonicalize_template_names(node):
    """Rewrite every ``tmpl_name`` in place to its canonical gershayim spelling.

    MAM-parsed-plus stores the canonical spelling directly, and can be compared raw
    -- but only since MAM-parsed 2993dbd of 2026-05-09, "Use g2 not q2 in tmpl
    names".  This module is the one place that reads plus data from ARBITRARY git
    revisions, and every range the change log pins predates that rename, so what it
    loads still carries the ASCII double quote that raw wikitext uses as a shorthand
    for the gershayim (mb_cmn/template_names.py's QUOTE MARKS note).

    Left unnormalized, a historical name misses every constant it is compared
    against downstream.  ``mpplus_flatten.is_std_kq_template`` was the expensive
    one: a ketiv/qere template whose name did not match fell through to the generic
    tail that emits param 1, so the diff compared the KETIV, and a change confined to
    the qere was invisible.  That silently dropped four real qere changes from the
    published change log (1 Samuel 12:10, 2 Kings 22:5, Ezekiel 28:3 and
    Lamentations 4:3).  The same mismatch hit the retired special-kq names.

    Normalizing here rather than at each of the two dozen comparison sites is
    deliberate: a name spelled as a bare literal at each site is what let half of
    this very rename look finished once already (0d23f0e).
    """
    if isinstance(node, dict):
        if isinstance(node.get("tmpl_name"), str):
            node["tmpl_name"] = ws_tmpl2.template_name(node)
        for value in node.values():
            _canonicalize_template_names(value)
    elif isinstance(node, list):
        for item in node:
            _canonicalize_template_names(item)
    return node


def _git_show_json(rev, path):
    return _canonicalize_template_names(json.loads(_git_show(rev, path)))


def _targeted_scrdff_note_values(node):
    """Return the note values held by targeted scroll-difference templates."""
    values = []
    if isinstance(node, list):
        for item in node:
            values.extend(_targeted_scrdff_note_values(item))
        return values
    if not isinstance(node, dict):
        return values
    if node.get("tmpl_name") == tmpln.SCRDFF_TAR:
        note_value = get_param(node, "2")
        if note_value is not MISSING:
            values.append(note_value)
    for value in node.values():
        values.extend(_targeted_scrdff_note_values(value))
    return values


def _drop_redundant_non_targeted_scrdff_notes(node, targeted_note_values):
    """Copy ``node`` without redundant non-targeted scroll-difference notes.

    Until MAM-parsed commit 8a254bf of 2026-05-13, plus data retained a
    non-targeted scroll-difference note beside the targeted note that already
    held the same note content.  The non-targeted template's parameter 1 is
    not biblical body text, so retaining that duplicate makes the change log
    report a false text addition or deletion.  Remove only a non-targeted
    note whose parameter 1 is present in a targeted note in the same EP; an
    unpaired historical note remains comparable data.
    """
    if isinstance(node, list):
        copied_items = [
            _drop_redundant_non_targeted_scrdff_notes(item, targeted_note_values)
            for item in node
        ]
        return [item for item in copied_items if item is not _DROP]
    if not isinstance(node, dict):
        return node
    if node.get("tmpl_name") == tmpln.SCRDFF_NO_TAR:
        note_value = get_param(node, "1")
        if note_value is not MISSING and note_value in targeted_note_values:
            return _DROP
    copied = {}
    for key, value in node.items():
        copied_value = _drop_redundant_non_targeted_scrdff_notes(
            value, targeted_note_values
        )
        if copied_value is not _DROP:
            copied[key] = copied_value
    return copied


def _ep_without_redundant_scrdff_notes(ep):
    """Return EP data with paired redundant scroll-difference notes omitted."""
    targeted_note_values = _targeted_scrdff_note_values(ep)
    if not targeted_note_values:
        return ep
    normalized = _drop_redundant_non_targeted_scrdff_notes(ep, targeted_note_values)
    assert isinstance(normalized, list)
    return normalized


def _list_plus_files(rev):
    """List plus JSON inputs; an unreadable or empty revision is a hard error."""
    return mpplus_revisions.resolve(rev).filenames()


def _diff_one_file(old_json, new_json, canonical_stem, old_rev, new_rev):
    """Compare two revisions of a single plus/ JSON file.

    Handles both old format (Hebrew numeral keys) and new format (numeric keys),
    including chapters and verses present at only one revision.
    """
    diffs = []
    book39_ids = book39_ids_for_stem(canonical_stem)
    old_he_to_int = get_he_to_int(old_json) if old_json is not None else {}
    new_he_to_int = get_he_to_int(new_json) if new_json is not None else {}
    old_book39s = _checked_book39s(old_json, canonical_stem, old_rev)
    new_book39s = _checked_book39s(new_json, canonical_stem, new_rev)
    for book39_index, book39id in enumerate(book39_ids):
        old_chapters_raw = old_book39s[book39_index]["chapters"] if old_book39s else {}
        new_chapters_raw = new_book39s[book39_index]["chapters"] if new_book39s else {}
        old_chapters = _normalized_key_mapping(
            old_chapters_raw,
            old_he_to_int,
            f"{old_rev} {book39id} chapters",
        )
        new_chapters = _normalized_key_mapping(
            new_chapters_raw,
            new_he_to_int,
            f"{new_rev} {book39id} chapters",
        )
        for chapter in sorted(old_chapters.keys() | new_chapters.keys()):
            old_verses_raw = old_chapters.get(chapter, {})
            new_verses_raw = new_chapters.get(chapter, {})
            old_verses = _normalized_key_mapping(
                old_verses_raw,
                old_he_to_int,
                f"{old_rev} {book39id} {chapter} verses",
            )
            new_verses = _normalized_key_mapping(
                new_verses_raw,
                new_he_to_int,
                f"{new_rev} {book39id} {chapter} verses",
            )
            for verse in sorted(old_verses.keys() | new_verses.keys()):
                old_verse = old_verses.get(verse)
                new_verse = new_verses.get(verse)
                old_ep = old_verse[2] if old_verse is not None else []
                new_ep = new_verse[2] if new_verse is not None else []
                diff = _diff_ep(old_ep, new_ep, book39id, chapter, verse)
                if diff is not None:
                    diffs.append(diff)
    return diffs


def _checked_book39s(book_json, canonical_stem, rev):
    """Return a present file's book39 list after checking its canonical roster."""
    if book_json is None:
        return []
    book39s = book_json["book39s"]
    expected_count = len(book39_ids_for_stem(canonical_stem))
    if len(book39s) != expected_count:
        raise ValueError(
            f"{rev} plus/{canonical_stem}.json has {len(book39s)} book39 "
            f"structures; expected {expected_count}."
        )
    return book39s


def _normalized_key_mapping(mapping, he_to_int, context):
    """Index a chapter or verse mapping by checked normalized integer keys."""
    normalized = {}
    raw_keys = {}
    for raw_key, value in mapping.items():
        number = _normalize_key_to_int(raw_key, he_to_int)
        if number is None:
            continue
        if number in normalized:
            raise ValueError(
                f"Duplicate normalized key in {context}: {number}: "
                f"{raw_keys[number]!r}, {raw_key!r}."
            )
        normalized[number] = value
        raw_keys[number] = raw_key
    return normalized


def _normalize_key_to_int(key, he_to_int):
    """Convert a key to integer, handling Hebrew numerals, numeric strings, or ints.

    Args:
        key: Hebrew numeral string, numeric string ("1", "21"), or integer
        he_to_int: Mapping from Hebrew numerals to integers (may be empty for new format)

    Returns:
        Integer value, or None if the key is a pseudo-verse ("0", "תתת")
    """
    if key in ("0", "תתת"):
        return None
    if isinstance(key, int):
        return key
    if not isinstance(key, str):
        raise ValueError(f"Unsupported chapter or verse key type: {key!r}")
    # String key - try numeric string first, then Hebrew numeral
    try:
        return int(key)
    except ValueError:
        if key in he_to_int:
            return he_to_int[key]
        raise ValueError(f"Unmapped nonnumeric chapter or verse key: {key!r}")


def _diff_ep(old_ep, new_ep, book39id, chapter, verse):
    """Compare two EP columns. Returns a diff dict or None.

    Compares flattened body text first (catches real text changes),
    then template structure (catches both count-changing and same-count
    structural changes like legarmeih -> paseq or reordered templates).
    Ignores format differences like tmpl_args vs tmpl_params.
    """
    old_ep = _ep_without_redundant_scrdff_notes(old_ep)
    new_ep = _ep_without_redundant_scrdff_notes(new_ep)
    old_text = flatten_ep_for_diff(old_ep)
    new_text, new_docnote = flatten_ep_with_docnote_for_diff(new_ep)
    text_changed = old_text != new_text
    if text_changed:
        old_words_only = flatten_ep_words_only_for_diff(old_ep)
        new_words_only = flatten_ep_words_only_for_diff(new_ep)
        if old_words_only == new_words_only:
            if template_name_counter(old_ep) == template_name_counter(new_ep):
                text_changed = False
    if not text_changed:
        old_counts = template_name_counter(old_ep)
        new_counts = template_name_counter(new_ep)
        if old_counts == new_counts:
            if structural_signature(old_ep) == structural_signature(new_ep):
                return None  # No meaningful change
    docnote_notes = find_relevant_docnote(old_text, new_text, new_docnote, text_changed)
    return {
        "book": book39id,
        "chapter": chapter,
        "verse": verse,
        "old_text": old_text,
        "new_text": new_text,
        "old_ep": old_ep,
        "new_ep": new_ep,
        "text_changed": text_changed,
        "docnote_notes": docnote_notes,
    }


def diff_all_books(old_rev, new_rev):
    """Compare all plus/ books between two git revisions.

    Matches files across historical renames by normalising each filename
    to its canonical OSDF-24 stem before pairing.

    Returns a list of diff dicts, sorted in reading order.
    """
    old_files = _list_plus_files(old_rev)
    new_files = _list_plus_files(new_rev)
    all_diffs = []
    for stem, old_filename, new_filename in matched_plus_file_pairs(
        old_files, new_files
    ):
        old_json = (
            _git_show_json(old_rev, f"plus/{old_filename}")
            if old_filename is not None
            else None
        )
        new_json = (
            _git_show_json(new_rev, f"plus/{new_filename}")
            if new_filename is not None
            else None
        )
        all_diffs.extend(_diff_one_file(old_json, new_json, stem, old_rev, new_rev))
    return all_diffs
