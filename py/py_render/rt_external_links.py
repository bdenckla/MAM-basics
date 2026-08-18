from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import quote

from mb_cmn import bib_locales as tbn
from mb_cmn.he_wikisource_url import he_taamim_url

VERSE_REFERENCE_RE = re.compile(
    r"^(?P<book>\S+)\s+(?P<chapter>\d+):(?P<verse>\d+)(?:\.\d+)?$"
)

# This repo's dataset is intentionally fixed and currently spans these books.
BOOK_HEBREW_NAMES = {
    "1Chronicles": "דברי הימים א",
    "1Kings": "מלכים א",
    "1Samuel": "שמואל א",
    "2Chronicles": "דברי הימים ב",
    "2Kings": "מלכים ב",
    "2Samuel": "שמואל ב",
    "Ezekiel": "יחזקאל",
    "Isaiah": "ישעיהו",
    "Jeremiah": "ירמיהו",
    "Job": "איוב",
    "Joshua": "יהושע",
    "Judges": "שופטים",
    "Proverbs": "משלי",
    "Psalms": "תהלים",
    "Tsefaniah": "צפניה",
}

_HUNDREDS = ("", "ק")
_TENS = ("", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ")
_ONES = ("", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט")
_SACRED_REMAPS = {
    "יה": "טו",
    "יו": "טז",
    "קיה": "קטו",
    "קיו": "קטז",
}


@dataclass(frozen=True)
class VerseExternalLinks:
    mgketer_url: str
    mwd_url: str
    mam_ws_url: str


def verse_external_links(verse_text: str) -> VerseExternalLinks:
    match = VERSE_REFERENCE_RE.fullmatch(verse_text)
    if match is None:
        raise ValueError(f"Unsupported verse reference format: {verse_text!r}")

    book = match.group("book")
    if book not in BOOK_HEBREW_NAMES:
        raise ValueError(f"Unsupported verse book for report links: {book!r}")

    chapter = int(match.group("chapter"))
    verse = int(match.group("verse"))
    osdf = tbn.ordered_short_dash_full_39(book)
    mgketer_id = tbn.get_bknu(book)
    chapter_he = _int_to_hebrew(chapter)

    return VerseExternalLinks(
        mgketer_url=f"https://www.mgketer.org/mikra/{mgketer_id}/{chapter}/1/mg/106",
        mwd_url=f"https://bdenckla.github.io/MAM-with-doc/{quote(f'{osdf}.html')}#c{chapter}v{verse}",
        mam_ws_url=he_taamim_url(BOOK_HEBREW_NAMES[book], chapter_he),
    )


def _int_to_hebrew(number: int) -> str:
    if not 1 <= number <= 199:
        raise ValueError(f"Hebrew numeral out of supported range: {number}")

    hundreds, remainder = divmod(number, 100)
    tens, ones = divmod(remainder, 10)
    numeral = _HUNDREDS[hundreds] + _TENS[tens] + _ONES[ones]
    return _SACRED_REMAPS.get(numeral, numeral)
