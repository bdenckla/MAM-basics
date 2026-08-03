"""Exports load_descriptions: index each noted atom's recorded letters by citation.

UXLC's ``<x>`` element carries only a one-letter code; the change that added the
note records the word it applied to. clc_collect joins notes onto atoms by the
integer ``position`` (1-based atom index within the verse, counting <w>/<q>/<k>),
but that key is fragile: if atoms are ever merged or split, positions shift and
the join would silently land on the wrong atom. So we index, per citation, the
letter-only form of each change's word, which clc_collect asserts the current
atom against (_check_atom_consistency). A collision needs *both* the position and
the letter-string to match the wrong atom -- vanishingly unlikely outside an
immediately-repeated identical word.

The citation key is ``(book_id, chnu, vrnu, position)``, matching UXLC's own
change-citation positions and the atom enumeration in clc_read.

(The note *prose* shown to readers comes from the downloaded tanach.us note page,
not from here -- see clc_note_pages.)
"""

import xml.etree.ElementTree as ET

import mb_cmn.hebrew_letters as hl
import uxlc_misc.my_uxlc_changes as my_uxlc_changes
import uxlc_misc.my_uxlc_book_abbreviations as bka
import uxlc_paths


def load_descriptions():
    """Map (book_id, chnu, vrnu, position) -> list of ``{"letters": ...}``.

    ``letters`` is the letter-only form of the change's word, used by clc_collect
    as the backup consistency check for the fragile position-based join.
    """
    index = {}
    for filename in my_uxlc_changes.FILENAMES:
        path = uxlc_paths.uxlc_misc_dir() / filename
        # FILENAMES includes a fake/placeholder that may be absent
        if path.exists():
            _index_one_file(index, path)
    return index


def _index_one_file(index, path):
    root = ET.parse(path).getroot()
    for change in root.iter("change"):
        key = _citation_key(change)
        if key is None:
            continue
        descriptor = {"letters": _word_letters(change)}
        index.setdefault(key, []).append(descriptor)


def _word_letters(change):
    # The change's word as letters only, for the backup consistency check.
    # Prefer the "after" text (changetext); fall back to "before" (reftext),
    # since note-only changes sometimes leave changetext empty in the XML.
    changetext_letters = hl.letters(change.findtext("changetext") or "")
    return changetext_letters or hl.letters(change.findtext("reftext") or "")


def _citation_key(change):
    citation = change.find("citation")
    if citation is None:
        return None
    book_id = bka.BKNA_MAP_UXLC_TO_STD.get(citation.findtext("book"))
    if book_id is None:
        return None
    try:
        chnu = int(citation.findtext("c"))
        vrnu = int(citation.findtext("v"))
        position = int(citation.findtext("position"))
    except (TypeError, ValueError):
        return None
    return book_id, chnu, vrnu, position
