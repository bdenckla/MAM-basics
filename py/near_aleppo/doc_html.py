"""HTML helpers for near-aleppo's documentation page.

The page is built as MAM-basics builds its pages, from the element trees of the
shared ``mb_misc/mb_html.py``. This module adds what the page needs on top of that:
Hebrew runs, verse references, and figures.

- A Hebrew run is a ``<bdi>`` with ``lang="hbo"``, so that it is isolated from the
  English around it without CSS ``unicode-bidi``: ``pointed`` for a pointed form,
  which the stylesheet sets at 20pt, and ``name`` for the unpointed name of a
  template or parameter.
- A verse reference is written in English, from the name ``main_build.py`` gives a
  verse's book, and links its verse in the edition, ``edition/<book file>#c<C>v<V>``,
  the anchor MAM-with-doc gives each verse. ``verse_refs`` is the one place that
  makes such a link; a reference typed in the prose stays plain text.
- Every figure the page states goes through Numbers, which formats it and records
  where it came from: the build's population file,
  ``in/near-aleppo/build-populations.json``, read by exact key so that a renamed key
  raises, or a figure ``doc_figures.py`` computes. The page's modules state no count
  as a literal.
"""

import re
import urllib.parse

from mb_cmn import bib_locales as tbn
from mb_cmn.mam_bknas_and_std_bknas import MAM_HBNP_TO_BK39ID
from mb_misc import mb_html
from py_misc import mwd_utils as mwdu

# The English name of each of the dataset's 39 books, keyed as main_build.py names
# a verse's book: the book file's stem, followed in a file of several books by a
# space and the sub-book's name.
_ENGLISH_BOOK = {
    "A1-Genesis": "Genesis",
    "A2-Exodus": "Exodus",
    "A3-Levit": "Leviticus",
    "A4-Numbers": "Numbers",
    "A5-Deuter": "Deuteronomy",
    "B1-Joshua": "Joshua",
    "B2-Judges": "Judges",
    'BA-Samuel שמ"א': "1 Samuel",
    'BA-Samuel שמ"ב': "2 Samuel",
    'BC-Kings מל"א': "1 Kings",
    'BC-Kings מל"ב': "2 Kings",
    "C1-Isaiah": "Isaiah",
    "C2-Jeremiah": "Jeremiah",
    "C3-Ezekiel": "Ezekiel",
    "CA-The-12-Minor-Prophets הושע": "Hosea",
    "CA-The-12-Minor-Prophets יואל": "Joel",
    "CA-The-12-Minor-Prophets עמוס": "Amos",
    "CA-The-12-Minor-Prophets עבדיה": "Obadiah",
    "CA-The-12-Minor-Prophets יונה": "Jonah",
    "CA-The-12-Minor-Prophets מיכה": "Micah",
    "CA-The-12-Minor-Prophets נחום": "Nahum",
    "CA-The-12-Minor-Prophets חבקוק": "Habakkuk",
    "CA-The-12-Minor-Prophets צפניה": "Zephaniah",
    "CA-The-12-Minor-Prophets חגי": "Haggai",
    "CA-The-12-Minor-Prophets זכריה": "Zechariah",
    "CA-The-12-Minor-Prophets מלאכי": "Malachi",
    "D1-Psalms": "Psalms",
    "D2-Proverbs": "Proverbs",
    "D3-Job": "Job",
    "E1-Song of Songs": "Song of Songs",
    "E2-Ruth": "Ruth",
    "E3-Lamentations": "Lamentations",
    "E4-Ecclesiastes": "Ecclesiastes",
    "E5-Esther": "Esther",
    "F1-Daniel": "Daniel",
    "FA-Ezra-Nexemiah עזרא": "Ezra",
    "FA-Ezra-Nexemiah נחמיה": "Nehemiah",
    'FC-Chronicles דה"א': "1 Chronicles",
    'FC-Chronicles דה"ב': "2 Chronicles",
}


def english_book(book):
    """The English name of ``book``, named as main_build.py names a verse's book."""
    return _ENGLISH_BOOK[book]


def verse_key(verse):
    """``verse`` as a (book, chapter, verse) tuple.

    It is a tuple or list, as main_build.py and the snapshot's site lists name a
    verse, or a string ``book|chapter|verse``, as a page's require_sites call may.
    """
    if isinstance(verse, str):
        parts = verse.split("|")
    else:
        parts = list(verse)
    if len(parts) != 3:
        raise ValueError(f"not a verse: {verse!r}")
    return tuple(parts)


def verse_refs(verses):
    """A run of references, grouped by book in the order met, each linked to its
    verse in the edition, as a list of contents.

    Within a book the references are joined by commas, and books by semicolons, as
    in "Psalms 7:1, 25:21; Proverbs 19:26", where the first reference of each book
    carries its name. A verse named twice or more is written once, with the number
    of times in words after the link.
    """
    counts = {}
    for verse in verses:
        key = verse_key(verse)
        counts[key] = counts.get(key, 0) + 1
    out = []
    previous_book = None
    for (book, chapter, number), times in counts.items():
        if times > 1 and times not in _TIMES:
            raise ValueError(f"{book} {chapter}:{number} is named {times} times")
        text = f"{chapter}:{number}"
        if book == previous_book:
            out.append(", ")
        else:
            if previous_book is not None:
                out.append("; ")
            text = f"{english_book(book)} {text}"
        out.append(link(text, edition_href(book, chapter, number)))
        if times > 1:
            out.append(_TIMES[times])
        previous_book = book
    return out


_TIMES = {2: " (twice)", 3: " (three times)"}


def edition_href(book, chapter, number):
    """The address, from the documentation, of a verse in the edition."""
    page = mwdu.filename_for_bkid(_BK39[book])
    return f"edition/{urllib.parse.quote(page)}#c{chapter}v{number}"


def _bk39_by_book():
    """The renderer's id of each book, keyed as main_build.py names a verse's book."""
    out = {}
    for (_book24_name, sub_book_name), bk39id in MAM_HBNP_TO_BK39ID.items():
        stem = tbn.ordered_short_dash_full_24(tbn.bk24id(bk39id))
        out[stem if sub_book_name is None else f"{stem} {sub_book_name}"] = bk39id
    if set(out) != set(_ENGLISH_BOOK):
        raise AssertionError("the renderer's books are not the documentation's")
    return out


_BK39 = _bk39_by_book()


def he_pointed(text):
    """A pointed Hebrew form, isolated and set at the size pointed Hebrew takes."""
    return mb_html.bdi(text, {"lang": "hbo", "class": "pointed"})


def he_name(text):
    """The unpointed Hebrew name of a template or a parameter, isolated."""
    return mb_html.bdi(text, {"lang": "hbo", "class": "name"})


def he_display(text):
    """A centered pointed example outside running prose, preserving its text."""
    return mb_html.para(he_pointed(text), {"dir": "rtl", "class": "display-example"})


def code(text):
    """An ASCII name, such as a parameter or a path, as code."""
    return mb_html.code(text)


# A Hebrew run inside English prose held as one string: a Hebrew letter, then Hebrew
# letters and marks, gereshes, colons, hyphens and digits, and further such words
# after single spaces, as in the names מ:הערה-2 and נוסח למקרא על פי המסורה.
_LETTERS = "\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}"
_IN_RUN = (
    "\N{HEBREW ACCENT ETNAHTA}-\N{HEBREW LETTER TAV}"
    "\N{HEBREW PUNCTUATION GERESH}\N{HEBREW PUNCTUATION GERSHAYIM}:0-9-"
)
_HEBREW_RUN = re.compile(f"[{_LETTERS}][{_IN_RUN}]*(?: [{_LETTERS}][{_IN_RUN}]*)*")


def isolated(text):
    """``text`` with each Hebrew run isolated as a name, as the consumer notice's rules
    and the choices register's rows, which are strings, need."""
    out = []
    position = 0
    for match in _HEBREW_RUN.finditer(text):
        out.append(text[position : match.start()])
        out.append(he_name(match.group(0)))
        position = match.end()
    out.append(text[position:])
    return [part for part in out if part != ""]


def link(contents, href):
    return mb_html.anchor(contents, {"href": href})


def itm():
    return mb_html.abbr("ITM", {"title": "Introduction to the Tiberian Masorah"})


def table(headings, rows, cell_attrs):
    """A table of ``rows`` under ``headings``, wrapped so it can scroll on its own.

    ``cell_attrs`` gives each column's cell attributes, the same for every row, so
    that a column holding Hebrew is declared ``dir="rtl"`` in every cell.
    """
    header = mb_html.table_row_of_headers(headings)
    body = tuple(mb_html.table_row_of_data(row, cell_attrs) for row in rows)
    return mb_html.div(mb_html.table((header,) + body), {"class": "table-wrap"})


HEBREW_CELL = {"dir": "rtl"}
BCV_CELL = {"class": "bcv"}
NUMBER_CELL = {"class": "num"}


class Numbers:
    """The page's figures, each formatted and recorded with its source.

    ``snapshot`` is the build's snapshot as build_expectations.load() returns it, and
    ``figures`` the figures doc_figures.py computes. ``trace`` lists each figure the
    page states, formatted as the page has it, with its source.
    """

    def __init__(self, snapshot, figures):
        self._snapshot = snapshot
        self._figures = figures
        self.trace = []

    def snap(self, section, key):
        """A count of the snapshot, formatted."""
        return self.record(self.snap_value(section, key), f"{section}: {key}")

    def snap_value(self, section, key):
        """A count of the snapshot, as a number, recorded by the caller if stated."""
        value = self._snapshot[section][key]
        if not isinstance(value, int):
            raise TypeError(f"{section}: {key} is not a count")
        return value

    def snap_sites(self, section, key):
        """A site list of the snapshot, as the snapshot names each verse."""
        return self._snapshot[section][key]

    def require_sites(self, section, keys, verses):
        """Raise unless each of ``verses``, which the prose names, is a site of one of
        the snapshot's lists ``keys`` in ``section``."""
        sites = {
            verse_key(site) for key in keys for site in self.snap_sites(section, key)
        }
        missing = [verse for verse in verses if verse_key(verse) not in sites]
        if missing:
            raise AssertionError(f"the page names sites the snapshot lacks: {missing}")

    def fig(self, name):
        """A figure doc_figures.py computes, formatted."""
        return self.record(self.fig_value(name), f"doc_figures: {name}")

    def fig_value(self, name):
        return self._figures[name]

    def record(self, value, source):
        """Format ``value``, a count or a percentage, and record it with ``source``."""
        if isinstance(value, int):
            text = f"{value:,}"
        elif isinstance(value, str):
            text = value
        else:
            raise TypeError(f"{source}: {value!r} is neither a count nor text")
        self.trace.append((text, source))
        return text

    def percent(self, part, whole, source):
        """``part`` as a percentage of ``whole``, to one decimal place, recorded."""
        return self.record(f"{100 * part / whole:.1f}%", source)
