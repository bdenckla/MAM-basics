"""Print the links a verse is looked up in, and where an atom of it is in the Leningrad Codex.

Run with MAM-basics' interpreter, from any directory -- every path here is
resolved from this file, never from the cwd:

    C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_verse_links.py <book> <c:v> [<word> | --atom N]

<book> is a bk39 id -- Psalms, 2Samuel, Levit, Tsefaniah, "Song of Songs" -- and
an unknown one is refused with the full list.  Name the atom by its Hebrew text,
matched as py/main_uxlc_estimate_atom_loc.py matches it (exactly, then by its
letters alone), or by its number with --atom.  The letters-alone pass drops marks
and format characters only, so a sof pasuq or a maqaf survives it: a bare
consonantal form matches a mid-verse atom and not a verse-final or maqaf-final
one, which wants MAM's pointed form or --atom.  With neither, the Leningrad Codex
line gives the verse's first atom and its last.

Prints one markdown link per line, ready to paste into a reply:

  mgketer, MwD, MAM-ws, tica, MM
      mb_cmn.verse_external_links, in the order the mgketer diff card has them;
      mgketer and MAM-ws are chapter pages, the other three land on the verse.
  UXLC
      the verse at tanach.us, from hkq_cmn.uxlc_external_links.
  tica LC
      the verse at masoretica.org, in the Leningrad Codex.
  LC <folio>
      Sefaria's image of that Leningrad Codex folio, with the atom's estimated
      column and line.
  CTR
      the chapter in Chabad's Complete Tanach with Rashi, where this repository
      records Chabad's URL for it, in in/chabad-ctr/*.json or
      in/accgram/ctr_decalogue.json -- ten chapters on 2026-09-10, Chabad's
      addresses being article ids that nothing here derives.  For any other
      chapter the line gives Chabad's index of the CTR instead.

THE ATOM NUMBER.  --atom counts the verse's atoms as uxlc_misc.my_uxlc reads the
UXLC core XML: one per <w> and per <q>, a ketiv (<k>) not counted.  That is the
estimator's own numbering, and the one this program lists when a word is not
found.  It is neither Holman's count nor the UXLC's count of every verse child;
py/main_estimate_uxlc_locations.py's docstring sets out all three.

THE ESTIMATE.  uxlc_misc.my_uxlc_location interpolates by word count between the
page breaks the UXLC's LC index records, so the folio is looked up and the column
and line are interpolated.  Psalms, Proverbs and Job are written two columns to a
leaf and the rest of the manuscript three, and an estimate that runs past a
leaf's last column is refused, as py/main_estimate_uxlc_locations.py refuses one.

VERSIFICATION.  The reference is used as given for every link.  Where MAM's
versification and the UXLC's differ -- the UXLC's Numbers 25:19 is MAM's 26:1,
the remap py/accgram/rtms_report.py makes -- the MAM links and the Leningrad
lines name different verses, so run this once with each reference.

Exits 1, having printed every link it could, when an atom was named but could
not be placed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

from hkq_cmn import uxlc_external_links
from hkq_cmn.uxlc_manuscript_page import sefaria_image_url
from mb_cmn import bib_locales as tbn
from mb_cmn import paths
from mb_cmn import verse_external_links as vel
from uxlc_misc import my_uxlc_location
from uxlc_misc.my_uxlc_find_atom import find_atom

# The keys in/accgram/ctr_decalogue.json gives its two chapters, which are the
# names py/accgram/ctr_decalogue_fetch.py's _CHAPTERS uses for them.
_CTR_DECALOGUE_BOOKS = {"ex": tbn.BK_EXODUS, "dt": tbn.BK_DEUTER}

# Chabad's index of the CTR, the URL py/mb_author/author.py links it by.
_CTR_INDEX_URL = (
    "https://www.chabad.org/library/bible_cdo/aid/63255/jewish/The-Bible-with-Rashi.htm"
)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = _build_parser()
    args = parser.parse_args()
    if args.book not in tbn.ALL_BK39_IDS:
        parser.error(
            f"unknown book {args.book!r}; give a bk39 id: "
            + ", ".join(tbn.ALL_BK39_IDS)
        )
    cv = re.fullmatch(r"([1-9][0-9]*):([1-9][0-9]*)", args.cv)
    if cv is None:
        parser.error(f"give chapter:verse, e.g. 72:15, not {args.cv!r}")
    if args.word is not None and args.atom is not None:
        parser.error("name the atom by its word or by --atom, not both")
    book, chapter, verse = args.book, int(cv.group(1)), int(cv.group(2))

    lc_lines, lc_placed = _leningrad_lines(book, chapter, verse, args.word, args.atom)
    print(f"{uxlc_external_links.book_display_name(book)} {chapter}:{verse}")
    for link in _links(book, chapter, verse):
        print(f"- [{link.label}]({link.href}): {link.title}")
    for line in lc_lines:
        print(line)
    print(_ctr_line(book, chapter))
    if not lc_placed:
        sys.exit(1)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("book", help="a bk39 id, e.g. Psalms, 2Samuel or Levit")
    parser.add_argument("cv", metavar="c:v", help="chapter and verse, e.g. 72:15")
    parser.add_argument("word", nargs="?", help="the atom's Hebrew text")
    parser.add_argument(
        "--atom", type=int, help="the atom's number, counted as THE ATOM NUMBER says"
    )
    return parser


def _links(book: str, chapter: int, verse: int) -> list:
    """Every link that needs only the reference, in the order printed."""
    links = list(vel.verse_links(book, chapter, verse))
    links += [
        link
        for link in uxlc_external_links.verse_links(book, chapter, verse)
        if link.label == "UXLC"
    ]
    links.append(
        vel.VerseLink(
            "tica LC",
            vel.masoretica_url(book, chapter, verse, manuscript="leningrad"),
            "This verse in the Leningrad Codex at masoretica.org",
        )
    )
    return links


def _leningrad_lines(
    book: str, chapter: int, verse: int, word: str | None, atom: int | None
) -> tuple[list[str], bool]:
    """The Leningrad Codex line or lines, and whether a named atom was placed."""
    uxlc, pbi = my_uxlc_location.prep()
    ref = f"{uxlc_external_links.book_display_name(book)} {chapter}:{verse}"
    try:
        words = uxlc[book][chapter - 1][verse - 1]
    except IndexError:
        return [
            f"- LC: the UXLC has no {ref}; if that is MAM's reference, give the"
            " UXLC's own (VERSIFICATION in --help)"
        ], False
    note = ""
    if word is not None:
        try:
            atom, method, uxlc_word = find_atom(uxlc, book, chapter, verse, word)
        except ValueError as unplaced:  # AtomNotFound, or more than one match
            lines = [f"- LC: {unplaced}. Give the atom's number with --atom:"]
            return lines + _numbered(words), False
        if method == "stripped":
            note = f" (matched by its letters alone; the UXLC has {uxlc_word})"
    if atom is not None:
        if not 1 <= atom <= len(words):
            lines = [f"- LC: the UXLC's {ref} has {len(words)} atoms, not {atom}:"]
            return lines + _numbered(words), False
        guess = _estimate(uxlc, pbi, book, chapter, verse, atom)
        if guess is None:
            return [_off_the_leaf(book, atom)], False
        where = f"atom {atom} of {len(words)}{note} is estimated at {_place(guess)}"
        return [_folio_line(guess["page"], where)], True
    first = _estimate(uxlc, pbi, book, chapter, verse, 1)
    last = _estimate(uxlc, pbi, book, chapter, verse, len(words))
    if first is None or last is None:
        return [_off_the_leaf(book, 1 if first is None else len(words))], True
    if first["page"] == last["page"]:
        where = (
            f"the verse is estimated to run from {_place(first)} (atom 1)"
            f" to {_place(last)} (atom {len(words)})"
        )
        return [_folio_line(first["page"], where)], True
    return [
        _folio_line(
            first["page"], f"the verse's first atom is estimated at {_place(first)}"
        ),
        _folio_line(
            last["page"],
            f"its last atom, {len(words)}, is estimated at {_place(last)}",
        ),
    ], True


def _estimate(uxlc, pbi, book: str, chapter: int, verse: int, atom: int):
    """The estimator's guess for one atom, or None if it runs off the leaf.

    Two columns to a leaf in Psalms, Proverbs and Job and three elsewhere: the
    rule py/main_estimate_uxlc_locations.py's _require_column_on_page applies.
    """
    guess = my_uxlc_location.page_and_guesses(uxlc, pbi, (book, chapter, verse, atom))
    columns = 2 if tbn.get_secid(book) == tbn.SEC_SIF_EM else 3
    return None if guess["column-guess"] > columns else guess


def _place(guess: dict) -> str:
    return f"column {guess['column-guess']}, line {guess['line-guess']}"


def _folio_line(folio: str, where: str) -> str:
    return (
        f"- [LC {folio}]({sefaria_image_url(folio)}): Sefaria's image of Leningrad"
        f" Codex folio {folio}, where {where}"
    )


def _off_the_leaf(book: str, atom: int) -> str:
    return (
        f"- LC: the estimate for atom {atom} runs past the last column of a leaf of"
        f" {book}, so no folio line is given; work out why before trusting it"
    )


def _numbered(words: list[str]) -> list[str]:
    return [f"    {number} {atom}" for number, atom in enumerate(words, start=1)]


def _ctr_line(book: str, chapter: int) -> str:
    url = _ctr_chapter_urls().get((book, chapter))
    if url is None:
        return (
            "- CTR: this repository records no Chabad URL for this chapter;"
            f" Chabad's index of the CTR is {_CTR_INDEX_URL}"
        )
    return f"- [CTR]({url}): This chapter in Chabad's Complete Tanach with Rashi"


def _ctr_chapter_urls() -> dict[tuple[str, int], str]:
    """Each chapter whose Chabad URL this repository records, keyed (bk39 id, chapter)."""
    by_osdf = {tbn.ordered_short_dash_full_39(bk): bk for bk in tbn.ALL_BK39_IDS}
    urls = {}
    for path in sorted((paths.in_dir() / "chabad-ctr").glob("*.json")):
        recorded = json.loads(path.read_text(encoding="utf-8"))["Chabad-chapter-URLs"]
        for chapter, url in recorded.items():
            urls[by_osdf[path.stem], int(chapter)] = url
    decalogue_path = paths.in_dir() / "accgram" / "ctr_decalogue.json"
    decalogue = json.loads(decalogue_path.read_text(encoding="utf-8"))
    for key, entry in decalogue["chapters"].items():
        urls[_CTR_DECALOGUE_BOOKS[key], entry["chapter"]] = entry["url"]
    return urls


if __name__ == "__main__":
    main()
