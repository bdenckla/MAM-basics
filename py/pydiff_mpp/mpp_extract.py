"""
Load MPP plus/ JSON from git revisions and extract EP column body text.

Exports:
    diff_all_books — compare all books between two revisions
"""

import json
import subprocess

from pydiff_mpp.mpp_file_matching import (
    _book39_ids_for_stem,
    _get_he_to_int,
    _matched_plus_file_pairs,
)
from pydiff_mpp.mpp_flatten import (
    _find_relevant_nusach,
    _flatten_ep_with_nusach_for_diff,
    flatten_ep_for_diff,
)
from pydiff_mpp.mpp_structure import (
    _structural_signature,
    _template_name_counter,
)

MAM_PARSED_DIR = "../MAM-parsed"

# ── Git helpers ──────────────────────────────────────────────


def _git_show(rev, path):
    """Read a file from a specific git revision of MAM-parsed."""
    result = subprocess.run(
        ["git", "-C", MAM_PARSED_DIR, "show", f"{rev}:{path}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        return None
    return result.stdout


def _git_show_json(rev, path):
    text = _git_show(rev, path)
    if text is None:
        return None
    return json.loads(text)


def _list_plus_files(rev):
    """List plus/ filenames (without the 'plus/' prefix) at a revision."""
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
    lines = result.stdout.strip().split("\n")
    return [line.strip().removeprefix("plus/") for line in lines if line.strip()]


# ── Book-level diffing ───────────────────────────────────────


def _diff_one_file(old_json, new_json, canonical_stem):
    """Compare two revisions of a single plus/ JSON file."""
    diffs = []
    book39_ids = _book39_ids_for_stem(canonical_stem)
    he_to_int = _get_he_to_int(new_json)
    old_book39s = old_json["book39s"]
    new_book39s = new_json["book39s"]
    for b39_idx, (old_b39, new_b39) in enumerate(zip(old_book39s, new_book39s)):
        book39id = book39_ids[b39_idx]
        old_chapters = old_b39["chapters"]
        new_chapters = new_b39["chapters"]
        for he_ch in old_chapters:
            if he_ch not in new_chapters:
                continue
            int_ch = he_to_int[he_ch]
            old_verses = old_chapters[he_ch]
            new_verses = new_chapters[he_ch]
            for he_vr in old_verses:
                if he_vr not in new_verses:
                    continue
                int_vr = he_to_int[he_vr]
                old_verse = old_verses[he_vr]
                new_verse = new_verses[he_vr]
                old_ep = old_verse[2]
                new_ep = new_verse[2]
                diff = _diff_ep(old_ep, new_ep, book39id, int_ch, int_vr)
                if diff is not None:
                    diffs.append(diff)
    return diffs


def _diff_ep(old_ep, new_ep, book39id, chapter, verse):
    """Compare two EP columns. Returns a diff dict or None.

    Compares flattened body text first (catches real text changes),
    then template structure (catches both count-changing and same-count
    structural changes like legarmeih -> paseq or reordered templates).
    Ignores format differences like tmpl_args vs tmpl_params.
    """
    old_text = flatten_ep_for_diff(old_ep)
    new_text, new_nusach = _flatten_ep_with_nusach_for_diff(new_ep)
    text_changed = old_text != new_text
    if not text_changed:
        old_counts = _template_name_counter(old_ep)
        new_counts = _template_name_counter(new_ep)
        if old_counts == new_counts:
            if _structural_signature(old_ep) == _structural_signature(new_ep):
                return None  # No meaningful change
    nusach_notes = _find_relevant_nusach(old_text, new_text, new_nusach, text_changed)
    return {
        "book": book39id,
        "chapter": chapter,
        "verse": verse,
        "old_text": old_text,
        "new_text": new_text,
        "old_ep": old_ep,
        "new_ep": new_ep,
        "text_changed": text_changed,
        "nusach_notes": nusach_notes,
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
    for stem, old_filename, new_filename in _matched_plus_file_pairs(
        old_files, new_files
    ):
        old_json = _git_show_json(old_rev, f"plus/{old_filename}")
        new_json = _git_show_json(new_rev, f"plus/{new_filename}")
        if old_json is None or new_json is None:
            continue
        all_diffs.extend(_diff_one_file(old_json, new_json, stem))
    return all_diffs
