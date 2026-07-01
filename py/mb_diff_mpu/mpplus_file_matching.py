"""Canonical plus-file matching and book-id mapping for MAM-parsed-plus diffs.

Exports:
    book39_ids_for_stem    — map a canonical plus stem to one or more bk39 ids
    get_he_to_int          — return or synthesize the Hebrew numeral lookup table
    matched_plus_file_pairs — match old/new plus filenames across historical renames

Policy:
    plus/ book files are JSON. The only allowed non-JSON sidecar is
    provenance.md; any other non-JSON filename in plus/ raises ValueError.
"""

from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_verse_numerals as hvn

_CANONICAL_STEM_TO_BOOK39_IDS = {
    tbn.ordered_short_dash_full_24(bk24id): tbn.bk39ids_of_bk24(bk24id)
    for bk24id in tbn.ALL_BK24_IDS
}

_BARE_NAME_TO_CANONICAL = {
    stem.partition("-")[2]: stem for stem in _CANONICAL_STEM_TO_BOOK39_IDS
}

_ALLOWED_PLUS_SIDECARS = {"provenance.md"}


def _json_plus_files_or_raise(filenames, side_label):
    """Return JSON plus files, skipping approved sidecars, else fail fast.

    Args:
        filenames: Iterable of file names relative to plus/.
        side_label: Human-readable source label (for example old_files).
    """
    json_files = []
    unexpected_non_json = []
    for filename in filenames:
        if filename.endswith(".json"):
            json_files.append(filename)
            continue
        if filename in _ALLOWED_PLUS_SIDECARS:
            continue
        unexpected_non_json.append(filename)
    if unexpected_non_json:
        unexpected_display = ", ".join(sorted(unexpected_non_json))
        allowed_display = ", ".join(sorted(_ALLOWED_PLUS_SIDECARS))
        raise ValueError(
            "Unexpected non-JSON plus/ filename(s) in "
            f"{side_label}: {unexpected_display}. "
            f"Allowed non-JSON sidecar(s): {allowed_display}."
        )
    return json_files


def _canonical_stem(filename):
    """Normalize any historical plus/ filename to its canonical OSDF-24 stem."""
    hwdb = "\N{LATIN SMALL LETTER H WITH DOT BELOW}"  # U+1E25 = h-with-dot-below
    stem = filename.removesuffix(".json").replace(hwdb, "x")
    if stem in _CANONICAL_STEM_TO_BOOK39_IDS:
        return stem
    return _BARE_NAME_TO_CANONICAL[stem]


def matched_plus_file_pairs(old_files, new_files):
    """Match old/new plus filenames across historical renames.

    plus/ inputs are expected to be JSON book files plus optional
    provenance.md. Any other non-JSON filename raises ValueError.

    Returns tuples of (canonical_stem, old_filename, new_filename) sorted in
    reading order by canonical stem.
    """
    old_json_files = _json_plus_files_or_raise(old_files, "old_files")
    new_json_files = _json_plus_files_or_raise(new_files, "new_files")
    old_by_stem = {_canonical_stem(filename): filename for filename in old_json_files}
    new_by_stem = {_canonical_stem(filename): filename for filename in new_json_files}
    common_stems = sorted(old_by_stem.keys() & new_by_stem.keys())
    return [(stem, old_by_stem[stem], new_by_stem[stem]) for stem in common_stems]


def book39_ids_for_stem(canonical):
    """Return the canonical bk39 ids for a canonical plus stem."""
    return _CANONICAL_STEM_TO_BOOK39_IDS[canonical]


def get_he_to_int(book_json):
    """Return the he_to_int mapping, building it on the fly if absent.

    Handles both old JSON format (with Hebrew numeral keys) and new format
    (with numeric-string keys like "1", "21").
    """
    he_to_int = book_json["header"].get("he_to_int")
    if he_to_int is not None:
        return he_to_int
    he_keys = set()
    for bk39 in book_json["book39s"]:
        for ch_key, ch_contents in bk39["chapters"].items():
            # Only include Hebrew numeral keys; skip numeric-string keys.
            if isinstance(ch_key, str) and not ch_key.isdigit():
                he_keys.add(ch_key)
                for vr_key in ch_contents:
                    if isinstance(vr_key, str) and not vr_key.isdigit():
                        he_keys.add(vr_key)
    if not he_keys:
        # No Hebrew keys found; this is new format with numeric-string keys.
        return {}
    return {he: hvn.STR_TO_INT_DIC[he] for he in he_keys}
