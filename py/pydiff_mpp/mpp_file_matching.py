"""Canonical plus-file matching and book-name mapping for MPP diffs.

Exports:
    _book39_names_for_stem  — map a canonical plus stem to one or more book names
    _get_he_to_int          — return or synthesize the Hebrew numeral lookup table
    _matched_plus_file_pairs — match old/new plus filenames across historical renames
"""

from pycmn import hebrew_verse_numerals as hvn

# Map canonical plus/ stems (current OSDF-24 naming) to book39 display names.
_CANONICAL_STEM_TO_BOOK39S = {
    "A1-Genesis": ["Genesis"],
    "A2-Exodus": ["Exodus"],
    "A3-Levit": ["Leviticus"],
    "A4-Numbers": ["Numbers"],
    "A5-Deuter": ["Deuteronomy"],
    "B1-Joshua": ["Joshua"],
    "B2-Judges": ["Judges"],
    "BA-Samuel": ["1 Samuel", "2 Samuel"],
    "BC-Kings": ["1 Kings", "2 Kings"],
    "C1-Isaiah": ["Isaiah"],
    "C2-Jeremiah": ["Jeremiah"],
    "C3-Ezekiel": ["Ezekiel"],
    "CA-The-12-Minor-Prophets": [
        "Hosea",
        "Joel",
        "Amos",
        "Obadiah",
        "Jonah",
        "Micah",
        "Nahum",
        "Habakkuk",
        "Zephaniah",
        "Haggai",
        "Zechariah",
        "Malachi",
    ],
    "D1-Psalms": ["Psalms"],
    "D2-Proverbs": ["Proverbs"],
    "D3-Job": ["Job"],
    "E1-Song of Songs": ["Song of Songs"],
    "E2-Ruth": ["Ruth"],
    "E3-Lamentations": ["Lamentations"],
    "E4-Ecclesiastes": ["Ecclesiastes"],
    "E5-Esther": ["Esther"],
    "F1-Daniel": ["Daniel"],
    "FA-Ezra-Nexemiah": ["Ezra", "Nehemiah"],
    "FC-Chronicles": ["1 Chronicles", "2 Chronicles"],
}

_BARE_NAME_TO_CANONICAL = {
    stem.partition("-")[2]: stem for stem in _CANONICAL_STEM_TO_BOOK39S
}


def _canonical_stem(filename):
    """Normalize any historical plus/ filename to its canonical OSDF-24 stem."""
    stem = filename.removesuffix(".json").replace("ḥ", "x")
    if stem in _CANONICAL_STEM_TO_BOOK39S:
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


def _book39_names_for_stem(canonical):
    """Return the display book names for a canonical plus stem."""
    return _CANONICAL_STEM_TO_BOOK39S[canonical]


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
