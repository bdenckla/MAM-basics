"""Exports read_all_books, read."""

import xml.etree.ElementTree

import mb_cmn.bib_locales as tbn
import uxlc_paths

UXLC_HOST = "tanach.us"
"""The host UXLC is published on, and the host every rendered-page URL names.

This is NOT where the downloads come from: see UXLC_DOWNLOAD_HOST below.  One constant
served both jobs until 2026-08-12, for the good reason that the two were the same
string; a URL on a rendered page has always been meant to name the published site,
whatever host a run happened to fetch from.
"""

UXLC_DOWNLOAD_HOST = "hcanat.us"
"""The host the two downloaders fetch from by default; ``--host`` overrides it.

Not tanach.us, as of 2026-08-12.  tanach.us' robots.txt had disallowed every path for
every user agent since 2026-08-02, and mb_cmn.polite_download obeys it, so a download
from tanach.us raised RobotsDisallowedError before making a request.  Chris Kimball
opened hcanat.us instead of reopening tanach.us -- the same tree on the same address,
under a robots.txt of its own, cut at 15:53 GMT that day to a single MJ12bot stanza
that permitted every URL either downloader fetches.  Ben's decision the same day:
treat that as the answer and fetch from hcanat.us.

robots.txt no longer tells the two hosts apart.  One GET of each on 2026-10-19, at
15:43 GMT, found both still on one address, 68.169.52.176, and serving the same 92
bytes, last modified on 2026-10-18 (11:09:33 GMT on hcanat.us, 11:22:11 GMT on
tanach.us): "User-agent: *" and "User-agent: MJ12bot" each with "Disallow: /", and
"User-agent: Claude-User" with "Allow: /".  Under their own user agents, both
downloaders were disallowed every URL on both hosts.  They now obey robots.txt as
UXLC_ROBOTS_USER_AGENT, whose group allows every path on either host.  Ben's decision
the same day: keep fetching from hcanat.us.

The two hosts do not serve identical bytes everywhere -- as last compared, on
2026-08-12 -- so this default is not a pure relabeling:

  * ``/Books/`` and ``/Changes/`` agree.  A full ``main_uxlc_download_changes --host
    hcanat.us`` run on 2026-08-12 produced 39 of 39 core-XML files, 7 of 7 under
    in/UXLC-rest and 16 of 17 change logs byte-identical to what is tracked, the
    seventeenth ("2023.07.04 - Changes.xml") differing only in line endings, which
    .gitattributes normalizes.

  * ``/Notes/`` does NOT.  hcanat.us builds note pages from a newer template than the
    477 stored under ``uxlc/in/UXLC-notes/*.json`` -- attribution and change-log
    link in a <table>, links ending .html rather than .xml, a trailing "auto"
    marker -- so main_clc_download_notes run against this default adds pages that
    do not match the existing entries.  clc_note_pages parses what is committed;
    mixing the two templates remains a decision nobody has made.
"""

UXLC_ROBOTS_USER_AGENT = "Claude-User"
"""The user agent the two downloaders obey robots.txt as on UXLC_HOST and
UXLC_DOWNLOAD_HOST; each still sends its own User-Agent header.

On 2026-10-19 both hosts' robots.txt allowed only Claude-User: see
UXLC_DOWNLOAD_HOST.  Ben's permission that day: these programs may act as
Claude-User, whether or not they advertise it, because his email with Chris Kimball
authorizes the downloads -- he is "satisfied that I (and my scripts) are authorized"
-- and he would rather not keep asking Kimball to adjust robots.txt.  His choice the
same day: each program keeps its own User-Agent header and obeys robots.txt as
Claude-User.  A robots.txt that closed to Claude-User any path these programs fetch
would therefore still stop them.  The permission rests on Kimball's authorization,
so robots_user_agent applies it to his two hosts only.
"""


def robots_user_agent(host):
    """The robots_user_agent of a downloader's config for fetching from host.

    UXLC_ROBOTS_USER_AGENT on UXLC_HOST and UXLC_DOWNLOAD_HOST.  Anywhere else, as
    through ``--host``, None, which leaves a downloader obeying robots.txt under its
    own user agent.
    """
    if host in (UXLC_HOST, UXLC_DOWNLOAD_HOST):
        return UXLC_ROBOTS_USER_AGENT
    return None


def canonical_xml_path(book_id):
    """Absolute path to book_id's canonical UXLC core-XML file.

    A function rather than the old ``UXLC_CANONICAL_DIR = "in/UXLC-39"`` constant:
    a module-level string is fixed at import time and was cwd-relative, so it
    resolved only while the process ran from the repo root, and a caller wanting
    to run elsewhere had to overwrite the constant or chdir.
    """
    return uxlc_paths.uxlc_39_dir() / f"{book_basename(book_id)}.xml"


def read_all_books(handlers=None):
    return {bkid: read(bkid, handlers) for bkid in tbn.ALL_BK39_IDS}


def book_basename(book_id):
    """The canonical UXLC/tanach.us file name for book_id, e.g. "Samuel_2".

    This is the name tanach.us uses for the book in both its core-XML filenames
    and its note-page URLs (``/Notes/<basename>/<basename>.c.v.pos-code.html``),
    which is *not* always the CLC bk39 id (e.g. id "2Samuel" -> "Samuel_2").
    """
    return _UXLC_BOOK_FILE_NAMES[book_id]


def note_page_url(book_id, ch, v, position, code, host=UXLC_HOST):
    """The note-page URL for one (atom, code), by canonical book name.

    Defaults to UXLC_HOST, the PUBLISHED host, because every caller that puts a URL
    on a rendered page leaves it at its default.  main_clc_download_notes always
    passes a host explicitly, and the host it passes is UXLC_DOWNLOAD_HOST.
    """
    name = book_basename(book_id)
    return f"https://{host}/Notes/{name}/{name}.{ch}.{v}.{position}-{code}.html"


def read(book_id, handlers=None):
    """Read book with id book_id into a list of chapters."""
    handlers = handlers or _VERSE_CHILD_HANDLERS
    xml_path = canonical_xml_path(book_id)
    tree = xml.etree.ElementTree.parse(xml_path)
    root = tree.getroot()
    chapters = []
    for chapter in root.iter("c"):
        verses = []
        for verse in chapter.iter("v"):
            words = []
            for verse_child in verse:
                dispatch_on_tag(words, verse_child, handlers)
            verses.append(words)
        chapters.append(verses)
    return chapters


def handle_xc_ignore(_1, _2):  # xc means vc or wc (verse child or word child)
    return


def dispatch_on_tag(accum, xml_element, handlers):
    fn_for_tag = handlers[xml_element.tag]
    fn_for_tag(accum, xml_element)


def _stripped_text(value):
    return value.strip() if value else ""


def _handle_wc_s(accum, word_child_s):
    # The <s> element implements small, large, and suspended letters.
    # E.g. <s t="large">וֹ</s>.
    accum[-1] += _stripped_text(word_child_s.text)


def _handle_vc_wq(accum, verse_child_wq):
    accum.append(_stripped_text(verse_child_wq.text))
    for word_child in verse_child_wq:
        dispatch_on_tag(accum, word_child, _WORD_CHILD_HANDLERS)
        accum[-1] += _stripped_text(word_child.tail)


_WORD_CHILD_HANDLERS = {
    "x": handle_xc_ignore,
    "s": _handle_wc_s,
}
_VERSE_CHILD_HANDLERS = {
    "w": _handle_vc_wq,
    "q": _handle_vc_wq,
    "k": handle_xc_ignore,
    "x": handle_xc_ignore,
    "pe": handle_xc_ignore,
    "samekh": handle_xc_ignore,
    "reversednun": handle_xc_ignore,
}
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
CANONICAL_XML_FILE_NAMES = frozenset(
    f"{basename}.xml" for basename in _UXLC_BOOK_FILE_NAMES.values()
)
