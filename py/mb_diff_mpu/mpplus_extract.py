"""
Load MAM-parsed-plus JSON from git revisions and extract EP column body text.

Exports:
    diff_all_books — compare all books between two revisions
"""

import json
import subprocess

from mb_cmn import paths
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
from mb_diff_mpu.mpplus_structure import (
    structural_signature,
    template_name_counter,
)

MAM_PARSED_DIR = str(paths.sibling_repo("MAM-parsed"))

# ── Git helpers ──────────────────────────────────────────────


def _git_show(rev, path):
    """Read a file from a specific git revision of MAM-parsed.

    RAISES RATHER THAN RETURNING EMPTY.  Every caller passes a path that
    ``_list_plus_files`` has just listed at this same revision, so the file is in that
    tree and a non-zero exit here means git could not read what it had just enumerated
    -- not that the book is absent from that release.  This returned ``None`` on failure
    until 2026-08-31, and ``diff_all_books`` skipped the pair, which is half of how a
    whole release could be reported as "0 raw changes found"; see ``_list_plus_files``.
    """
    result = subprocess.run(
        ["git", "-C", MAM_PARSED_DIR, "show", f"{rev}:{path}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git show {rev}:{path} failed in {MAM_PARSED_DIR}"
            f" (exit {result.returncode}): {result.stderr.strip()}"
        )
    return result.stdout


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


def _list_plus_files(rev):
    """List plus/ filenames (without the 'plus/' prefix) at a revision.

    AN UNREADABLE REVISION IS A HARD ERROR, NOT AN EMPTY RELEASE.  This ignored
    ``returncode`` until 2026-08-31, so a revision git could not resolve produced no
    output, an empty file list, no matched pairs and therefore no diffs -- and the
    change-log report for that release was written out saying "0 changes found", which
    is indistinguishable from a release that genuinely changed nothing.

    A SHALLOW CLONE IS THE WAY IN, and it is not exotic: the sibling clone in a cloud
    session is made with ``--depth 1``, which puts every release boundary in
    MAM-with-doc's releases.json outside the history.  On 2026-08-31 that wrote five
    falsified reports before an unrelated ``check=True`` two calls later happened to
    stop the run.  The tracked generated artifact is this repo's test (CLAUDE.md), so a
    generator that reports zero when it cannot see is worse than one that crashes.
    """
    result = subprocess.run(
        [
            "git",
            "-C",
            MAM_PARSED_DIR,
            "-c",
            "core.quotePath=false",
            "ls-tree",
            "--name-only",
            rev,
            "plus/",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git ls-tree {rev} plus/ failed in {MAM_PARSED_DIR}"
            f" (exit {result.returncode}): {result.stderr.strip()}\n"
            f"If that clone is shallow, deepen it:"
            f" git -C {MAM_PARSED_DIR} fetch --depth=2000 origin"
        )
    lines = result.stdout.strip().split("\n")
    filenames = [line.strip().removeprefix("plus/") for line in lines if line.strip()]
    if not filenames:
        raise RuntimeError(
            f"no plus/ files at revision {rev} in {MAM_PARSED_DIR}."
            f" That revision resolves but its tree has no plus/ directory,"
            f" so there is nothing to diff against."
        )
    return filenames


# ── Book-level diffing ───────────────────────────────────────


def _diff_one_file(old_json, new_json, canonical_stem):
    """Compare two revisions of a single plus/ JSON file.

    Handles both old format (Hebrew numeral keys) and new format (integer keys).
    """
    diffs = []
    book39_ids = book39_ids_for_stem(canonical_stem)
    he_to_int_old = get_he_to_int(old_json)
    old_book39s = old_json["book39s"]
    new_book39s = new_json["book39s"]
    for b39_idx, (old_b39, new_b39) in enumerate(zip(old_book39s, new_book39s)):
        book39id = book39_ids[b39_idx]
        old_chapters = old_b39["chapters"]
        new_chapters = new_b39["chapters"]
        # Normalize all chapter keys to integers for comparison
        for ch_key in old_chapters:
            int_ch = _normalize_key_to_int(ch_key, he_to_int_old)
            if int_ch is None:
                continue
            # Find matching key in new_chapters (could be string or int)
            new_ch_key = _find_matching_key(ch_key, new_chapters)
            if new_ch_key is None:
                continue
            old_verses = old_chapters[ch_key]
            new_verses = new_chapters[new_ch_key]
            for vr_key in old_verses:
                int_vr = _normalize_key_to_int(vr_key, he_to_int_old)
                if int_vr is None:
                    continue
                # Find matching key in new_verses (could be string or int)
                new_vr_key = _find_matching_key(vr_key, new_verses)
                if new_vr_key is None:
                    continue
                old_verse = old_verses[vr_key]
                new_verse = new_verses[new_vr_key]
                old_ep = old_verse[2]
                new_ep = new_verse[2]
                diff = _diff_ep(old_ep, new_ep, book39id, int_ch, int_vr)
                if diff is not None:
                    diffs.append(diff)
    return diffs


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
    # String key - try numeric string first, then Hebrew numeral
    try:
        return int(key)
    except ValueError:
        # Not a numeric string, try Hebrew numeral mapping
        return he_to_int.get(key)


def _find_matching_key(old_key, new_dict):
    """Find a matching key in new_dict for the given old_key.

    Handles cross-format matching (string to int or int to string).
    """
    if old_key in new_dict:
        return old_key
    # Try to find a matching key with normalized format
    old_int = _normalize_key_to_int(old_key, {})
    if old_int is None:
        return None
    for new_key in new_dict:
        new_int = _normalize_key_to_int(new_key, {})
        if new_int == old_int:
            return new_key
    return None


def _diff_ep(old_ep, new_ep, book39id, chapter, verse):
    """Compare two EP columns. Returns a diff dict or None.

    Compares flattened body text first (catches real text changes),
    then template structure (catches both count-changing and same-count
    structural changes like legarmeih -> paseq or reordered templates).
    Ignores format differences like tmpl_args vs tmpl_params.
    """
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
        # matched_plus_file_pairs yields only stems present at BOTH revisions, and
        # _git_show now raises rather than returning None, so there is no
        # legitimately-absent case left to skip here.
        old_json = _git_show_json(old_rev, f"plus/{old_filename}")
        new_json = _git_show_json(new_rev, f"plus/{new_filename}")
        all_diffs.extend(_diff_one_file(old_json, new_json, stem))
    return all_diffs
