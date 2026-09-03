"""Exports main

Word-finding behavior here is kept in sync with the two "find word"
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
    in those repos)
  - Ambiguity: raises ValueError("Ambiguous: N matches ...") when a
    word matches more than one position, rather than silently picking
    one.  The caller must disambiguate.

One difference from the sibling repos: on *no match at all* this
script prints the verse's word list and exits (sys.exit(1)), whereas
the sibling linebreak_search modules return a None-tuple to their
callers.  That is because those modules are libraries consumed by
higher-level tools, while this script is a standalone CLI entry point.
"""

import sys
import unicodedata
import mb_cmn.bib_locales as tbn
import uxlc_misc.my_uxlc_location as my_uxlc_location


def _strip_heb(s):
    """Strip cantillation marks, vowels, and format chars from Hebrew text."""
    out = []
    for ch in s:
        cat = unicodedata.category(ch)
        if cat not in ("Mn", "Cf"):
            out.append(ch)
    return "".join(out)


def _find_atom(uxlc, book_id, chapter, verse, word):
    """Find the 1-based atom index of *word* in the given verse.

    Tries exact match first, then stripped (no vowels/accents).
    Raises ValueError if the word matches more than one atom.
    """
    words = uxlc[book_id][chapter - 1][verse - 1]
    word_stripped = _strip_heb(word)
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
        (i + 1, w) for i, w in enumerate(words) if _strip_heb(w) == word_stripped
    ]
    if len(stripped) == 1:
        return stripped[0][0], "stripped", stripped[0][1]
    if len(stripped) > 1:
        atoms = [idx for idx, _ in stripped]
        raise ValueError(
            f"Ambiguous: {len(stripped)} stripped matches for {word!r} "
            f"in {book_id} {chapter}:{verse} (atoms {atoms})"
        )
    print(f"Word {word!r} not found in {book_id} {chapter}:{verse}")
    print(f"Words in verse: {words}")
    sys.exit(1)


def main():
    r"""
    Estimate the concrete location of the given word.

    Usage: .venv/Scripts/python.exe py/main_uxlc_estimate_atom_loc.py <book_id> <c:v> <word>
    Example: .venv/Scripts/python.exe py/main_uxlc_estimate_atom_loc.py Genesis 27:7 "צַ֛יִד"

    That example is the same location example_run() reports: Genesis 27:7, atom 3.
    """
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if len(args) != 3:
        print(
            "Usage: .venv/Scripts/python.exe py/main_uxlc_estimate_atom_loc.py <book_id> <c:v> <word>"
        )
        print('Example: ... Genesis 27:7 "צַ֛יִד"')
        sys.exit(1)

    book_id = args[0]
    if book_id not in tbn.ALL_BK39_IDS:
        print(f"ERROR: unknown book_id {book_id!r}")
        print(f"Valid: {' '.join(tbn.ALL_BK39_IDS)}")
        sys.exit(1)

    cv = args[1]
    if ":" not in cv:
        print(f"ERROR: verse must be in c:v format (e.g. 27:7), got: {cv}")
        sys.exit(1)
    chapter, verse = (int(x) for x in cv.split(":"))

    word = args[2]

    uxlc, pbi = my_uxlc_location.prep()
    atom, match_method, uxlc_word = _find_atom(uxlc, book_id, chapter, verse, word)
    if match_method != "exact":
        print(f"  (matched via {match_method}; UXLC has {uxlc_word!r})")
    std_bcvp_quad = book_id, chapter, verse, atom
    pg = my_uxlc_location.page_and_guesses(uxlc, pbi, std_bcvp_quad)
    print(pg)


def example_run():
    """Do an example run of the program, for main_uxlc_mega.py."""
    std_bcvp_quad = tbn.BK_GENESIS, 27, 7, 3
    _main2(std_bcvp_quad)


def _main2(std_bcvp_quad):
    uxlc, pbi = my_uxlc_location.prep()
    pg = my_uxlc_location.page_and_guesses(uxlc, pbi, std_bcvp_quad)
    print(pg)


if __name__ == "__main__":
    main()
