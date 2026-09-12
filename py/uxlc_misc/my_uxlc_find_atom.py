"""Find an atom of a UXLC verse by its Hebrew text.

Exports find_atom, AtomNotFound, strip_heb.

Moved here on 2026-09-10 from py/main_uxlc_estimate_atom_loc.py, with its
behavior unchanged, so that py/main_verse_links.py finds an atom the same way.

Word-finding here is kept in sync with the two "find word"
utilities, which are in THIS repo now rather than in sibling repos:

  py/py_ac_word_image_helper/linebreak_search.py   (Aleppo Codex)
  py/py_cam1753_word_image/linebreak_search.py     (Cambridge Add. 1753)

They were codex-index-aleppo's py/py_ac_word_image_helper/ and
codex-index-cam1753's py_cam1753_word_image/ until Phase 3 of
doc/PLAN-evacuate-python-from-codex-index-trio.md, 2026-08-22; both of
those repos now hold manuscript data and no code at all.  Keeping the
three in sync is therefore a same-repo job, not a cross-repo one.

Shared conventions:
  - CLI argument order: <book> <c:v> <word>  (c:v colon-separated)
  - Match strategy: exact first, then stripped (vowels/accents removed
    via unicodedata category, same logic as hebrew_metrics.strip_heb
    in those packages).  Only Mn and Cf go, so a sof pasuq (Po) or a
    maqaf (Pd) survives the stripping: a bare consonantal form matches
    a mid-verse atom and not a verse-final or maqaf-final one.
  - Ambiguity: raises ValueError("Ambiguous: N matches ...") when a
    word matches more than one position, rather than silently picking
    one.  The caller must disambiguate.

On no match at all, find_atom raises AtomNotFound, which carries the
verse's atoms; the linebreak_search modules return a None-tuple instead.

The atom number is 1-based over the verse as uxlc_misc.my_uxlc.read_all_books
builds it -- one entry per <w> and per <q>, a ketiv (<k>) not counted -- which
is the numbering the Leningrad estimator, uxlc_misc.my_uxlc_location, takes.
py/main_estimate_uxlc_locations.py's docstring sets out the other two
numberings in play.
"""

import unicodedata


class AtomNotFound(ValueError):
    """No atom of the verse matches the word, exactly or stripped."""

    def __init__(self, word, book_id, chapter, verse, words):
        super().__init__(f"Word {word!r} not found in {book_id} {chapter}:{verse}")
        self.words = words


def strip_heb(s):
    """Strip cantillation marks, vowels, and format chars from Hebrew text."""
    out = []
    for ch in s:
        cat = unicodedata.category(ch)
        if cat not in ("Mn", "Cf"):
            out.append(ch)
    return "".join(out)


def find_atom(uxlc, book_id, chapter, verse, word):
    """Find the 1-based atom index of *word* in the given verse.

    Tries exact match first, then stripped (no vowels/accents).  Returns
    (atom, "exact" or "stripped", the UXLC's form of that atom).  Raises
    ValueError if the word matches more than one atom, and AtomNotFound if
    it matches none.
    """
    words = uxlc[book_id][chapter - 1][verse - 1]
    word_stripped = strip_heb(word)
    # Exact matches
    exact = [i + 1 for i, w in enumerate(words) if w == word]
    if len(exact) == 1:
        return exact[0], "exact", word
    if len(exact) > 1:
        raise ValueError(
            f"Ambiguous: {len(exact)} exact matches for {word!r} "
            f"in {book_id} {chapter}:{verse} (atoms {exact})"
        )
    # Stripped matches
    stripped = [
        (i + 1, w) for i, w in enumerate(words) if strip_heb(w) == word_stripped
    ]
    if len(stripped) == 1:
        return stripped[0][0], "stripped", stripped[0][1]
    if len(stripped) > 1:
        atoms = [idx for idx, _ in stripped]
        raise ValueError(
            f"Ambiguous: {len(stripped)} stripped matches for {word!r} "
            f"in {book_id} {chapter}:{verse} (atoms {atoms})"
        )
    raise AtomNotFound(word, book_id, chapter, verse, words)
