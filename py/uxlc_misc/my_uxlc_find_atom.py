"""Find an atom of a UXLC verse by its Hebrew text.

Exports find_atom, AtomNotFound, strip_heb.

Moved here on 2026-09-10 from py/main_uxlc_estimate_atom_loc.py, initially with
its behavior unchanged, so that py/main_verse_links.py finds an atom the same
way.

Ben's decision, 2026-09-13: this matcher's input contract is UXLC-specific.
The Aleppo Codex and Cambridge Add. 1753 linebreak locators solve a different
span-matching problem and are not kept in sync with this matcher:

  py/py_ac_word_image_helper/linebreak_search.py   (Aleppo Codex)
  py/py_cam1753_word_image/linebreak_search.py     (Cambridge Add. 1753)

UXLC matching conventions:
  - CLI argument order: <book> <c:v> <atom>  (c:v colon-separated)
  - Match strategy: exact first, then by Hebrew letters U+05D0 through
    U+05EA only.  Each pass returns a result only when exactly one atom
    matches.  A bare consonantal query always uses the letters-only pass,
    even when it is byte-identical to one unpointed atom, so another atom
    with the same letters makes the query ambiguous.  The letters-only
    pass ignores a sof pasuq and a maqaf as well as vowels, accents and
    format characters.
  - Ambiguity: raises ValueError("Ambiguous: N matches ...") when an
    exact form or a letters-only form matches more than one atom.  The
    caller must disambiguate, normally with an atom number.

On no match at all, find_atom raises AtomNotFound, which carries the
verse's atoms; the linebreak_search modules return a None-tuple instead.

The atom number is 1-based over the verse as uxlc_misc.my_uxlc.read_all_books
builds it -- one entry per <w> and per <q>, a ketiv (<k>) not counted -- which
is the numbering the Leningrad estimator, uxlc_misc.my_uxlc_location, takes.
py/main_estimate_uxlc_locations.py's docstring sets out the other two
numberings in play.
"""


class AtomNotFound(ValueError):
    """No atom of the verse matches the query exactly or by Hebrew letters."""

    def __init__(self, word, book_id, chapter, verse, words):
        super().__init__(f"Atom {word!r} not found in {book_id} {chapter}:{verse}")
        self.words = words


def strip_heb(s):
    """Retain only Hebrew letters U+05D0 through U+05EA."""
    return "".join(
        ch for ch in s if "\N{HEBREW LETTER ALEF}" <= ch <= "\N{HEBREW LETTER TAV}"
    )


def find_atom(uxlc, book_id, chapter, verse, word):
    """Find the 1-based atom index of *word* in the given verse.

    Tries an exact match first, then matches by Hebrew letters alone.  A bare
    consonantal query always uses the letters-only candidates, including when
    one atom is an exact unpointed match.  Returns (atom, "exact" or "letters",
    the UXLC's form of that atom).  Raises ValueError if the applicable pass
    has more than one candidate, and AtomNotFound if neither pass has one.
    """
    words = uxlc[book_id][chapter - 1][verse - 1]
    word_letters = strip_heb(word)
    word_is_bare = word == word_letters
    # Exact matches
    exact = [i + 1 for i, w in enumerate(words) if w == word]
    if len(exact) == 1 and not word_is_bare:
        return exact[0], "exact", word
    if len(exact) > 1:
        raise ValueError(
            f"Ambiguous: {len(exact)} exact matches for {word!r} "
            f"in {book_id} {chapter}:{verse} (atoms {exact})"
        )
    # Letters-only matches
    letter_matches = [
        (i + 1, w) for i, w in enumerate(words) if strip_heb(w) == word_letters
    ]
    if len(letter_matches) == 1:
        return letter_matches[0][0], "letters", letter_matches[0][1]
    if len(letter_matches) > 1:
        atoms = [idx for idx, _ in letter_matches]
        raise ValueError(
            f"Ambiguous: {len(letter_matches)} letters-only matches for {word!r} "
            f"in {book_id} {chapter}:{verse} (atoms {atoms})"
        )
    raise AtomNotFound(word, book_id, chapter, verse, words)
