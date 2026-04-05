"""Canonical plus-file matching and book-id mapping for MPP diffs.

Exports:
    _book39_ids_for_stem    — map a canonical plus stem to one or more bk39 ids
    _get_he_to_int          — return or synthesize the Hebrew numeral lookup table
    _matched_plus_file_pairs — match old/new plus filenames across historical renames
"""

from pycmn import bib_locales as tbn
from pycmn import hebrew_verse_numerals as hvn

_CANONICAL_STEM_TO_BOOK39_IDS = {
    tbn.ordered_short_dash_full_24(bk24id): tbn.bk39ids_of_bk24(bk24id)
    for bk24id in tbn.ALL_BK24_IDS
}

_BARE_NAME_TO_CANONICAL = {
    stem.partition("-")[2]: stem for stem in _CANONICAL_STEM_TO_BOOK39_IDS
}


def _canonical_stem(filename):
    """Normalize any historical plus/ filename to its canonical OSDF-24 stem."""
    stem = filename.removesuffix(".json").replace("ḥ", "x")
    if stem in _CANONICAL_STEM_TO_BOOK39_IDS:
        return stem
    return _BARE_NAME_TO_CANONICAL[stem]


def _matched_plus_file_pairs(old_files, new_files):
    """Match old/new plus filenames across historical renames.

    Returns tuples of (canonical_stem, old_filename, new_filename) sorted in
    reading order by canonical stem.
    """
    old_by_stem = {_canonical_stem(filename): filename for filename in old_files}
    new_by_stem = {_canonical_stem(filename): filename for filename in new_files}
    common_stems = sorted(old_by_stem.keys() & new_by_stem.keys())
    return [(stem, old_by_stem[stem], new_by_stem[stem]) for stem in common_stems]


def _book39_ids_for_stem(canonical):
    """Return the canonical bk39 ids for a canonical plus stem."""
    return _CANONICAL_STEM_TO_BOOK39_IDS[canonical]


def _get_he_to_int(book_json):
    """Return the he_to_int mapping, building it on the fly if absent."""
    he_to_int = book_json["header"].get("he_to_int")
    if he_to_int is not None:
        return he_to_int
    he_keys = set()
    for bk39 in book_json["book39s"]:
        for he_ch, ch_contents in bk39["chapters"].items():
            he_keys.add(he_ch)
            for he_vr in ch_contents:
                he_keys.add(he_vr)
    return {he: hvn.STR_TO_INT_DIC[he] for he in he_keys}
