"""Per-verse links to the websites a verse is looked up in, for all 39 books.

This is the shared home that MAM-private's doc/PLAN-share-verse-link-builders.md
designs in its section 3 for five per-verse link builders: mgketer.org,
MAM-with-doc, MAM on Hebrew Wikisource, masoretica.org and mechon-mamre.org. Ben's
decision of 2026-09-10 was to write it then, with py/main_verse_links.py as its
first and only consumer, and to leave the plan's switch-over stages paused. So the
mgketer diff cards in MAM-private and eight modules here -- the plan's section 1
names them -- still build their own copies of some of these links, and until those
stages run, a change to a URL scheme here is a change to make there as well.

Every builder takes a bk39 id (mb_cmn.bib_locales) and serves all 39 books. Two of
the five land on a chapter page rather than on the verse: mgketer_url and
wikisource_url take no verse, and a reader finds the verse on the page.

The two book tables at the bottom are the only data here that no other mb_cmn
table supplies. Both were lifted on 2026-09-10 from the masoretica_name and
mechon_mamre_code columns of MAM-private's mgketer/py/python_modules/book_metadata.py,
at MAM-private commit 55252b8, whose builders make the mgketer diff cards' "tica"
and "MM" links.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote, urlencode

from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn.he_wikisource_url import he_taamim_url
from mb_cmn.mam_bknas_and_std_bknas import he_bk39_name


@dataclass(frozen=True)
class VerseLink:
    """One labelled link, in the shape hkq_cmn.uxlc_external_links introduced."""

    label: str
    href: str
    title: str


def verse_links(bk39id: str, chapter: int, verse: int) -> tuple[VerseLink, ...]:
    """The five links, labelled and in the order the mgketer diff card has them."""
    return (
        VerseLink(
            "mgketer",
            mgketer_url(bk39id, chapter),
            "This chapter at mgketer.org",
        ),
        VerseLink(
            "MwD",
            mam_with_doc_url(bk39id, chapter, verse),
            "This verse in MAM-with-doc",
        ),
        VerseLink(
            "MAM-ws",
            wikisource_url(bk39id, chapter),
            "This chapter of MAM on Hebrew Wikisource",
        ),
        VerseLink(
            "tica",
            masoretica_url(bk39id, chapter, verse),
            "This verse in the Aleppo Codex at masoretica.org",
        ),
        VerseLink(
            "MM",
            mechon_mamre_url(bk39id, chapter, verse),
            "This verse at mechon-mamre.org",
        ),
    )


def mgketer_url(bk39id: str, chapter: int) -> str:
    """mgketer.org's page for the chapter; it numbers the books as bib_locales does."""
    return f"https://www.mgketer.org/mikra/{tbn.get_bknu(bk39id)}/{chapter}/1/mg/106"


def mam_with_doc_url(bk39id: str, chapter: int, verse: int) -> str:
    """The verse in MAM-with-doc, as MAM-basics' GitHub Pages site publishes it."""
    osdf = tbn.ordered_short_dash_full_39(bk39id)
    # quote matters for exactly one osdf: "E1-Song of Songs" has a space in it.
    page = quote(f"{osdf}.html")
    return (
        f"https://bdenckla.github.io/MAM-basics/MAM-with-doc/{page}#c{chapter}v{verse}"
    )


def wikisource_url(bk39id: str, chapter: int) -> str:
    """The chapter's page of MAM on Hebrew Wikisource."""
    return he_taamim_url(he_bk39_name(bk39id), hvn.INT_TO_STR_DIC[chapter])


def masoretica_url(
    bk39id: str, chapter: int, verse: int, manuscript: str = "aleppo"
) -> str:
    """The verse at masoretica.org, in the manuscript its manuscript= value names.

    masoretica.org answers with that manuscript's page and folio for the verse.
    Three of its manuscript= values are recorded in this repository: aleppo, the
    one the mgketer diff cards use; leningrad (leningrad/page-snips/README.md); and
    sassoon, for Codex Sassoon 1053 (doc/ms-snips/README.md).
    """
    query = urlencode(
        {
            "book": _MASORETICA_BOOK[bk39id],
            "chapter": chapter,
            "verse": verse,
            "manuscript": manuscript,
        }
    )
    return f"https://www.masoretica.org/?{query}"


def mechon_mamre_url(bk39id: str, chapter: int, verse: int) -> str:
    """The chapter's page at mechon-mamre.org, anchored at the verse.

    Its cantillated edition is under /c/ct/, one page per chapter, named
    c<book><chapter>.htm. The chapter is two characters with the TENS DIGIT IN
    HEXADECIMAL, which is how two characters reach Psalms 150: chapters 1 to 99 are
    the plain two digits, 100 is a0, 119 is b9 and 150 is f0. Each verse on the
    page is preceded by <A NAME="<verse>">, so the fragment lands on the verse.
    MAM-private's mgketer/py/python_modules/mechon_mamre_url.py, where this scheme
    comes from, records that all 150 Psalms pages and all 39 book codes were
    checked against the site on 2026-08-25.
    """
    page = f"c{_MECHON_MAMRE_BOOK[bk39id]}{chapter // 10:x}{chapter % 10}.htm"
    return f"https://mechon-mamre.org/c/ct/{page}#{verse}"


# masoretica.org's ?book= spelling. Most differ from the bk39 id only by a space
# after a leading digit, but Levit, Deuter and Tsefaniah differ outright, so the
# whole column is spelled out rather than derived.
_MASORETICA_BOOK = {
    tbn.BK_GENESIS: "Genesis",
    tbn.BK_EXODUS: "Exodus",
    tbn.BK_LEVIT: "Leviticus",
    tbn.BK_NUMBERS: "Numbers",
    tbn.BK_DEUTER: "Deuteronomy",
    tbn.BK_JOSHUA: "Joshua",
    tbn.BK_JUDGES: "Judges",
    tbn.BK_FST_SAM: "1 Samuel",
    tbn.BK_SND_SAM: "2 Samuel",
    tbn.BK_FST_KGS: "1 Kings",
    tbn.BK_SND_KGS: "2 Kings",
    tbn.BK_ISAIAH: "Isaiah",
    tbn.BK_JEREM: "Jeremiah",
    tbn.BK_EZEKIEL: "Ezekiel",
    tbn.BK_HOSHEA: "Hosea",
    tbn.BK_JOEL: "Joel",
    tbn.BK_AMOS: "Amos",
    tbn.BK_OVADIAH: "Obadiah",
    tbn.BK_JONAH: "Jonah",
    tbn.BK_MIKHAH: "Micah",
    tbn.BK_NAXUM: "Nahum",
    tbn.BK_XABA: "Habakkuk",
    tbn.BK_TSEF: "Zephaniah",
    tbn.BK_XAGGAI: "Haggai",
    tbn.BK_ZEKHAR: "Zechariah",
    tbn.BK_MALAKHI: "Malachi",
    tbn.BK_PSALMS: "Psalms",
    tbn.BK_PROV: "Proverbs",
    tbn.BK_JOB: "Job",
    tbn.BK_SONG: "Song of Songs",
    tbn.BK_RUTH: "Ruth",
    tbn.BK_LAMENT: "Lamentations",
    tbn.BK_QOHELET: "Ecclesiastes",
    tbn.BK_ESTHER: "Esther",
    tbn.BK_DANIEL: "Daniel",
    tbn.BK_EZRA: "Ezra",
    tbn.BK_NEXEM: "Nehemiah",
    tbn.BK_FST_CHR: "1 Chronicles",
    tbn.BK_SND_CHR: "2 Chronicles",
}

# mechon-mamre.org's book part of a page name: a two-digit number over the 24
# books, plus a sub-book letter for each of the four printed as two (Samuel,
# Kings, Chronicles, and Ezra with Nehemiah). Its Writings follow the Aleppo Codex
# order, which is why Chronicles (25) comes before Psalms (26).
_MECHON_MAMRE_BOOK = {
    tbn.BK_GENESIS: "01",
    tbn.BK_EXODUS: "02",
    tbn.BK_LEVIT: "03",
    tbn.BK_NUMBERS: "04",
    tbn.BK_DEUTER: "05",
    tbn.BK_JOSHUA: "06",
    tbn.BK_JUDGES: "07",
    tbn.BK_FST_SAM: "08a",
    tbn.BK_SND_SAM: "08b",
    tbn.BK_FST_KGS: "09a",
    tbn.BK_SND_KGS: "09b",
    tbn.BK_ISAIAH: "10",
    tbn.BK_JEREM: "11",
    tbn.BK_EZEKIEL: "12",
    tbn.BK_HOSHEA: "13",
    tbn.BK_JOEL: "14",
    tbn.BK_AMOS: "15",
    tbn.BK_OVADIAH: "16",
    tbn.BK_JONAH: "17",
    tbn.BK_MIKHAH: "18",
    tbn.BK_NAXUM: "19",
    tbn.BK_XABA: "20",
    tbn.BK_TSEF: "21",
    tbn.BK_XAGGAI: "22",
    tbn.BK_ZEKHAR: "23",
    tbn.BK_MALAKHI: "24",
    tbn.BK_PSALMS: "26",
    tbn.BK_PROV: "28",
    tbn.BK_JOB: "27",
    tbn.BK_SONG: "30",
    tbn.BK_RUTH: "29",
    tbn.BK_LAMENT: "32",
    tbn.BK_QOHELET: "31",
    tbn.BK_ESTHER: "33",
    tbn.BK_DANIEL: "34",
    tbn.BK_EZRA: "35a",
    tbn.BK_NEXEM: "35b",
    tbn.BK_FST_CHR: "25a",
    tbn.BK_SND_CHR: "25b",
}
