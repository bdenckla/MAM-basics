"""Exports read_all_books, read."""

import xml.etree.ElementTree

import mb_cmn.bib_locales as tbn


# books_dir is REQUIRED, and was a "in/UXLC" default until 2026-08-01.  That default named
# a directory this repo has never had -- the UXLC source lives in in/UXLC-39 and in
# in/Tanach-26.0--UXLC-1.0--2020-04-01/Books -- so it could only ever have resolved against
# some other cwd.  The sole caller, wlc_compare_mdc_with_uxlc.compare, passes the directory
# explicitly, so requiring it costs nothing and removes a path that cannot be right.
def read_all_books(books_dir):
    return {bkid: read(bkid, books_dir) for bkid in tbn.ALL_BK39_IDS}


def read(book_id, books_dir):
    """Read book with id book_id into a list of chapters."""
    basename = _UXLC_BOOK_FILE_NAMES[book_id]
    xml_path = f"{books_dir}/{basename}.xml"
    tree = xml.etree.ElementTree.parse(xml_path)
    root = tree.getroot()
    chapters = []
    for chapter in root.iter("c"):
        verses = []
        for verse in chapter.iter("v"):
            words = []
            for verse_child in verse:
                _dispatch_on_tag(words, verse_child, _VERSE_CHILD_FNS)
            verses.append(words)
        chapters.append(verses)
    return chapters


_UXLC_BOOK_FILE_NAMES = {
    tbn.BK_GENESIS: "Genesis",
    tbn.BK_EXODUS: "Exodus",
    tbn.BK_LEVIT: "Leviticus",
    tbn.BK_NUMBERS: "Numbers",
    tbn.BK_DEUTER: "Deuteronomy",
    tbn.BK_JOSHUA: "Joshua",
    tbn.BK_JUDGES: "Judges",
    tbn.BK_FST_SAM: "Samuel_1",
    tbn.BK_SND_SAM: "Samuel_2",
    tbn.BK_FST_KGS: "Kings_1",
    tbn.BK_SND_KGS: "Kings_2",
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
    tbn.BK_SONG: "Song_of_Songs",
    tbn.BK_RUTH: "Ruth",
    tbn.BK_LAMENT: "Lamentations",
    tbn.BK_QOHELET: "Ecclesiastes",
    tbn.BK_ESTHER: "Esther",
    tbn.BK_DANIEL: "Daniel",
    tbn.BK_EZRA: "Ezra",
    tbn.BK_NEXEM: "Nehemiah",
    tbn.BK_FST_CHR: "Chronicles_1",
    tbn.BK_SND_CHR: "Chronicles_2",
}

# GOs have 6 types:
#    w, a single word;
#    q, a word representing a qere variant;
#    k, a word representing a ketib variant;
#    pe, an empty tag representing an open paragraph marker;
#    samekh, an empty tag representing a closed paragraph marker,
#    reversednun, an empty tag representing a reversed nun.


def _handle_xc_ignore(_1, _2):  # xc means vc or wc (verse child or word child)
    return


def _handle_wc_s(accum, word_child_s):
    # The <s> element implements small, large, and suspended letters.
    # E.g. <s t="large">וֹ</s>.
    accum[-1] += word_child_s.text.strip()


_WORD_CHILD_FNS = {
    "x": _handle_xc_ignore,
    "s": _handle_wc_s,
}


def _handle_vc_wq(accum, verse_child_wq):
    accum.append(verse_child_wq.text.strip())
    for word_child in verse_child_wq:
        _dispatch_on_tag(accum, word_child, _WORD_CHILD_FNS)
        accum[-1] += word_child.tail.strip()


_VERSE_CHILD_FNS = {
    "w": _handle_vc_wq,
    "q": _handle_vc_wq,
    "k": _handle_xc_ignore,
    "x": _handle_xc_ignore,
    "pe": _handle_xc_ignore,
    "samekh": _handle_xc_ignore,
    "reversednun": _handle_xc_ignore,
}


def _dispatch_on_tag(accum, verse_child, fns):
    fn_for_tag = fns[verse_child.tag]
    fn_for_tag(accum, verse_child)
