"""Exports main

The word-finding is find_atom in py/uxlc_misc/my_uxlc_find_atom.py, moved
there on 2026-09-10 so that py/main_verse_links.py could share it.  That
module's docstring has the conventions it keeps in sync with the two "find
word" utilities for the Aleppo Codex and Cambridge Add. 1753.

One difference from those utilities: on *no match at all* this
script prints the verse's word list and exits (sys.exit(1)), whereas
the linebreak_search modules return a None-tuple to their
callers.  That is because those modules are libraries consumed by
higher-level tools, while this script is a standalone CLI entry point.
"""

import sys
import mb_cmn.bib_locales as tbn
import uxlc_misc.my_uxlc_location as my_uxlc_location
from uxlc_misc.my_uxlc_find_atom import AtomNotFound, find_atom


def main():
    r"""
    Estimate the concrete location of the given word.

    Usage: .venv/Scripts/python.exe py/main_uxlc_estimate_atom_loc.py <book_id> <c:v> <word>
    Example: .venv/Scripts/python.exe py/main_uxlc_estimate_atom_loc.py Genesis 27:7 "צַ֛יִד"
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
    try:
        atom, match_method, uxlc_word = find_atom(uxlc, book_id, chapter, verse, word)
    except AtomNotFound as not_found:
        print(not_found)
        print(f"Words in verse: {not_found.words}")
        sys.exit(1)
    if match_method != "exact":
        print(f"  (matched via {match_method}; UXLC has {uxlc_word!r})")
    std_bcvp_quad = book_id, chapter, verse, atom
    pg = my_uxlc_location.page_and_guesses(uxlc, pbi, std_bcvp_quad)
    print(pg)


if __name__ == "__main__":
    main()
