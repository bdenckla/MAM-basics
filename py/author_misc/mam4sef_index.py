"""The encoding of MAM for Sefaria: writes ``gh-pages/MAM-for-Sefaria/index.html``.

Ben's decision of 2026-10-24, which ``doc/PLAN-rewrite-MAM-for-Sefaria-encoding-page.md``
records, was to rewrite this page "from fresh perspective of just documenting what MAM for
Sefaria contains".  Until then it was a hand-authored page that documented MAM-for-Sefaria by
its differences from Sefaria's earlier Tanakh, with the figures of Sefaria's 2021 copy of MAM.
Now it describes the files as they are, and compares them with no other text.

WHERE EVERYTHING COMES FROM.  ``mam4sef_survey`` reads the product's tracked files with closed
dispatch and counts what they have; every count, list and example here comes from it.  An
example is a lookup that must match exactly one place in the files, by a reference and the
letters of its atoms, as ``accgram.maqaf_nonfinal_accents_page._find_span`` and
``author_site.post_stress_meteg_post_silluq_data._source_focus_word`` look forms up, so no
pointed Hebrew on the page is typed here.  ``_pin_claims`` defends the sentences whose truth the
data could overturn, and raises rather than warns.

POINTED HEBREW KEEPS ITS VOWELS HERE.  The house rule shows a form by its letters and accents
alone (the ``hebrew-prose`` skill's ``core-rules.md``, "Show it in Unicode").  This page
documents how the files encode every mark, vowels among them, which is the exception that rule
allows where the vowel is the point.

NEVER A FORM WITHOUT ITS CGJ.  ``_guard_two_vowels`` refuses to write the page if any Hebrew on
it has two vowels on one letter, except where the files have them, with the COMBINING
GRAPHEME JOINER between them that keeps their order.  The old page's table of Sefaria's earlier
Exodus 20:4 had such a letter with no CGJ, and how it looked depended on the font.

THE FONT.  The page loads ``woff2/Taamey_D.woff2`` beside it, a copy of ``doc/woff2/``'s that
``mb_misc.report_stylesheet.copy_report_font`` keeps byte-identical, under the family name
"Taamey D WOFF2", so a reader sees MAM-basics' Taamey D with nothing installed and no locally
installed Taamey D takes its place.

``py/tests/test_sefaria_silluq_documentation.py`` parses the meteg-after-silluq table that
``_meteg_after_silluq`` writes, and checks it against MAM-simple and both exporters' handlers:
keep its id, its ``data-osis-id`` column headers, its two ``data-version`` rows and their labels.
"""

import re

from mb_author import author
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import paths
from mb_cmn import str_defs as sd
from mb_cmn import unicode_data
from mb_cmn import bib_locales as tbn
from mb_misc import mb_html
from mb_misc import report_stylesheet
from author_misc import mam4sef_survey as ms

_FNAME = "index.html"
_TITLE = "The encoding of MAM for Sefaria"
_AUTHOR = "Author: Ben Denckla"
_REVISION = "Revision: 2026-10-26"
_CSS_HREFS = ("../document.css", "styles.css")

_GITHUB = "https://github.com/bdenckla/MAM-basics"
_PRODUCT_URL = f"{_GITHUB}/tree/main/MAM-for-Sefaria"
_README_URL = f"{_GITHUB}/blob/main/MAM-for-Sefaria/README.md"
_HANDLERS_URL = f"{_GITHUB}/blob/main/py/mb_sefaria/mam4sef_handlers.py"
_MARK_ORDER_URL = f"{_GITHUB}/blob/main/doc/mam-normal-mark-order.md"
_MAM_SIMPLE_GUIDE = "../MAM-simple/reading-mam-simple-json.html"
_VERSIFICATION = "../MAM-simple/versification-differences.html"
_GRAY_MAQAF = "../MAM-with-doc/misc/he_ws_intro_to_mam_gray_maqaf_1.html"

_PATAH = "\N{HEBREW POINT PATAH}"
_QAMATS = "\N{HEBREW POINT QAMATS}"
_HIRIQ = "\N{HEBREW POINT HIRIQ}"
_SHEVA = "\N{HEBREW POINT SHEVA}"
_LAMED = "\N{HEBREW LETTER LAMED}"
_QAMATS_QATAN = "\N{HEBREW POINT QAMATS QATAN}"
_HOLAM_HASER_FOR_VAV = "\N{HEBREW POINT HOLAM HASER FOR VAV}"
_EDGE = "[א-ת֑-ׇֽֿׁׂׅׄ͏]"

# THE EXAMPLES, each a lookup that must match exactly one place: a reference as the files
# write it, and the parts of the text there, each part either the letters of one atom or the
# literal characters between atoms.  Letters fix the grouping as well as the letters.
_EX_LEGARMEH = ("Genesis 2:5", ("וכל", sd.THSP + hpu.PASOLEG + " ", "שיח"))
_EX_PASEQ = ("Genesis 1:5", ("אלהים", sd.THSP + hpu.PASOLEG + sd.THSP, "לאור"))
_EX_IMPLICIT_MAQAF = ("Psalms 1:1", ("אשרי", hpu.MAQ, "האיש"))
_EX_TRIVIAL = ("Genesis 13:3", ("אהלה",))
_EX_LETTER_SIZES = (
    ("Daniel 6:20", ("בשפרפרא",), "a small letter and a large one"),
    ("Job 38:13", ("רשעים",), "a hung letter"),
)
_EX_LISTING = "Genesis 1:5"
# A ketiv/qere pair: a reference, the letters of each word of the ketiv, and those of the qere.
_EX_SMALL_IN_KETIV = ("Job 7:5", ("וגיש",), ("וגוש",))
_EX_KQ = {
    ("ketiv first", "space", 1, 1): ("Genesis 8:17", ("הוצא",), ("היצא",)),
    ("qere first", "space", 1, 1): ("Genesis 36:5", ("יעיש",), ("יעוש",)),
    ("ketiv first", "space", 2, 1): ("Judges 16:25", ("כי", "טוב"), ("כטוב",)),
    ("ketiv first", "space", 1, 2): ("Genesis 30:11", ("בגד",), ("בא", "גד")),
    ("ketiv first", "space", 2, 2): (
        "II Samuel 5:2",
        ("הייתה", "מוציא"),
        ("היית", "המוציא"),
    ),
    ("qere first", "space", 1, 2): ("II Kings 18:27", ("שניהם",), ("מימי", "רגליהם")),
    ("ketiv first", "space", 3, 3): (
        "II Samuel 21:12",
        ("תלום", "שם", "הפלשתים"),
        ("תלאום", "שמה", "פלשתים"),
    ),
    ("ketiv first", "maqaf", 1, 1): ("Isaiah 26:20", ("יעבור",), ("יעבר",)),
    ("ketiv first", "maqaf", 1, 2): ("I Chronicles 9:4", ("בנימן",), ("בני", "מן")),
}
_EX_KETIV_VELO_QERE = ("Ruth 3:12", "אם")
_EX_QERE_VELO_KETIV = ("Ruth 3:17", "אלי")
_EX_OWN_CODE_POINT = {
    _QAMATS_QATAN: ("Genesis 1:26", ("ובכל", hpu.MAQ, "הרמש")),
    _HOLAM_HASER_FOR_VAV: ("Genesis 4:13", ("עוני",)),
    hpo.RAFE: ("Exodus 2:3", ("ותחמרה",)),
    hpu.UPDOT: ("Numbers 3:39", ("ואהרן",)),
    hpu.LODOT: ("Psalms 27:13", ("לולא",)),
}
_EX_ZARQA = (("Genesis 19:4", ("טרם",)), ("Leviticus 4:2", ("ישראל",)))
# One example of each kind of Jerusalem atom, by the lamed's own vowel and the orphaned vowel.
_EX_JERUSALEM = {
    (_PATAH, _HIRIQ): ("Judges 1:7", ("ירושלם",)),
    (_QAMATS, _HIRIQ): ("Joshua 15:8", ("ירושלם",)),
    (_PATAH, _SHEVA): ("Isaiah 36:2", ("ירושלמה",)),
    (_QAMATS, _SHEVA): ("II Kings 9:28", ("ירושלמה",)),
}


# SMALL HELPERS --------------------------------------------------------------------------------


def _num(count: int) -> str:
    return f"{count:,}"


def _p(*contents, attr=None):
    return author.para(list(contents), attr)


def _code(text: str):
    return mb_html.code(text)


def _he(contents):
    return author.hbo(contents)


def _rom(text: str):
    """A romanized name with no ``$`` key in ``mb_author.author``; see ``_SILLUQ``."""
    return mb_html.span_c(text, "romanized")


# author.py has no key for silluq by design: U+05BD is silluq only on a verse-final atom, so
# no code point names it.  On this page MAM's annotation identifies each silluq it names.
_SILLUQ = _rom("silluq")


def _uname(char: str, *, full: bool = False):
    """A code point's Unicode name in small capitals, the whole name on hover if shortened."""
    name = unicode_data.name(char)
    shown = name if full else ms.short_name(char)
    attr = {"class": "unicode-code-point-name"}
    if shown != name:
        attr["title"] = name
    return mb_html.span(shown, attr)


def _cgj():
    return mb_html.span(
        "CGJ", {"class": "unicode-code-point-name", "title": unicode_data.name(sd.CGJ)}
    )


def _join(items: list, last: str = "and") -> list:
    """``items`` in an English list: a, b and c."""
    if len(items) == 1:
        return [items[0]]
    out = []
    for index, item in enumerate(items):
        if index == len(items) - 1:
            out.append(f" {last} ")
        elif index:
            out.append(", ")
        out.append(item)
    return out


def _name_list(chars: str) -> list:
    """Code points by name, in order, separated by commas."""
    out = []
    for index, char in enumerate(chars):
        if index:
            out.append(", ")
        out.append(_cgj() if char == sd.CGJ else _uname(char))
    return out


def _table(headers: list, rows: list, attr=None):
    head = mb_html.table_row(
        [mb_html.table_header(author.dollar_sub(h)) for h in headers]
    )
    table_attr = {"class": "data", **(attr or {})}
    return mb_html.div(
        [mb_html.table([head, *rows], table_attr)], {"class": "table-wrap"}
    )


def _tr(cells: list):
    return mb_html.table_row(cells)


def _td(contents, attr=None):
    return mb_html.table_datum(author.dollar_sub(contents), attr)


def _td_he(contents):
    return mb_html.table_datum(contents, {"lang": "hbo", "dir": "rtl"})


def _td_ref(ref: str):
    return mb_html.table_datum(ref, {"class": "bcv"})


def _td_num(count: int):
    return mb_html.table_datum(_num(count), {"class": "num"})


def _refs(refs: list) -> str:
    """References, consecutive verses of one chapter as a range: Exodus 20:24–26."""
    groups = []
    for ref in refs:
        book, cv = ref.rsplit(" ", 1)
        chapter, verse = (int(x) for x in cv.split(":"))
        last = groups[-1] if groups else None
        if last and last[0] == book and last[1] == chapter and last[3] == verse - 1:
            last[3] = verse
        else:
            groups.append([book, chapter, verse, verse])
    by_book = []
    for book, chapter, first, last in groups:
        span = (
            f"{chapter}:{first}"
            if first == last
            else f"{chapter}:{first}\N{EN DASH}{last}"
        )
        if by_book and by_book[-1][0] == book:
            by_book[-1][1].append(span)
        else:
            by_book.append([book, [span]])
    parts = [f"{book} " + "".join(_join(spans)) for book, spans in by_book]
    if len(parts) == 1:
        return parts[0]
    if all(len(spans) == 1 for _book, spans in by_book):
        return "".join(_join(parts))
    if len(parts) == 2:
        return f"{parts[0]}, and {parts[1]}"
    return "; ".join(parts[:-1]) + "; and " + parts[-1]


# LIFTING FORMS FROM THE FILES -----------------------------------------------------------------


def _part_pattern(part: str) -> str:
    if part and set(part) <= set(ms.LETTERS):
        return "".join(re.escape(c) + f"{ms.MARK_CLASS}*" for c in part)
    return re.escape(part)


def _find(text: str, parts: tuple, where: str) -> tuple:
    """The one place in ``text`` that ``parts`` match, as a pair of offsets."""
    pattern = "".join(_part_pattern(p) for p in parts)
    regex = re.compile(f"(?<!{_EDGE}){pattern}(?!{_EDGE})")
    hits = [m.span() for m in regex.finditer(text)]
    if len(hits) != 1:
        raise ValueError(f"{where}: {len(hits)} places match {parts}")
    return hits[0]


def _chanted_words(text: str, start: int, end: int) -> tuple:
    """``start`` and ``end`` widened to the spaces around them, so no chanted word is split."""
    while start > 0 and not text[start - 1].isspace():
        start -= 1
    while end < len(text) and not text[end].isspace():
        end += 1
    return start, end


def _htel(el):
    contents = [_htel(k) if isinstance(k, ms.Element) else k for k in el.kids]
    attr = {"class": el.cls} if el.cls else None
    return mb_html.htel_mk(el.tag, attr, contents or None)


def _snippet(verse, start: int, end: int) -> list:
    """The part of a verse of csv/ from ``start`` to ``end``, with its markup."""
    out = []
    offset = 0
    for kid in verse.top:
        if isinstance(kid, str):
            lo, hi = max(offset, start), min(offset + len(kid), end)
            if lo < hi:
                out.append(kid[lo - offset : hi - offset])
            offset += len(kid)
            continue
        offset = kid.end
        if kid.start == kid.end:
            if start < kid.start <= end:
                out.append(_htel(kid))
        elif kid.end <= start or kid.start >= end:
            continue
        elif start <= kid.start and kid.end <= end:
            out.append(_htel(kid))
        else:
            raise ValueError(f"{verse.ref}: an example would split <{kid.tag}>")
    return out


def _lift(ref: str, parts: tuple, s, *, whole: bool = True) -> list:
    """The form at ``ref`` that ``parts`` match, as csv/ has it, its chanted words whole."""
    verse = s.verse(ref)
    start, end = _find(verse.text, parts, ref)
    if whole:
        start, end = _chanted_words(verse.text, start, end)
    return _snippet(verse, start, end)


def _lift_atom(ref: str, parts: tuple, s) -> str:
    verse = s.verse(ref)
    start, end = _find(verse.text, parts, ref)
    return verse.text[start:end]


def _kq_element(ref: str, ketiv: tuple, qere: tuple, s):
    """The one ketiv/qere pair at ``ref`` with these letters in its two parts."""
    verse = s.verse(ref)

    def words(el):
        return tuple(ms.letters_of(w) for w in el.text()[1:-1].split(" "))

    hits = []
    for el in verse.elements:
        if el.kind == "kq":
            parts = {k.kind: k for k in el.kids if isinstance(k, ms.Element)}
            if words(parts["ketiv"]) == ketiv and words(parts["qere"]) == qere:
                hits.append(el)
    if len(hits) != 1:
        raise ValueError(f"{ref}: {len(hits)} ketiv/qere pairs {ketiv} {qere}")
    return verse, hits[0]


def _lift_element(verse, el, *, whole: bool = True) -> list:
    start, end = el.start, el.end
    if whole:
        start, end = _chanted_words(verse.text, start, end)
    return _snippet(verse, start, end)


def _velo_element(ref: str, kind: str, letters: str, s):
    verse = s.verse(ref)
    hits = [
        el
        for el in verse.elements
        if el.kind == kind
        and el.parent_kind is None
        and ms.letters_of(el.text()) == letters
    ]
    if len(hits) != 1:
        raise ValueError(f"{ref}: {len(hits)} lone {kind} {letters}")
    return verse, hits[0]


def _highlight(atom: str, cluster_index: int) -> list:
    """An atom with one of its letters, and that letter's marks, in the attention color."""
    clusters = list(ms.CLUSTER_RE.finditer(atom))
    a, b = clusters[cluster_index].span()
    parts = [atom[:a], mb_html.span_c(atom[a:b], "attention"), atom[b:]]
    return [part for part in parts if part != ""]


# THE PAGE -------------------------------------------------------------------------------------


def _intro():
    conventions = [
        [
            mb_html.span(
                "Text styled like this", {"title": "an example of hover text"}
            ),
            " reveals more on hover, where the medium allows hovering.",
        ],
        [
            mb_html.span_c("Text styled like this", "attention"),
            " draws attention to letters of a form, as to the ",
            _he("ב"),
            " of ",
            _he(["א", mb_html.span_c("ב", "attention"), "ג"]),
            ".",
        ],
        [
            _uname(ha.ZSH_OR_TSIT),
            " is the name of a Unicode code point, less the words that name its script"
            " and class. Hovering shows the whole name, here ",
            _uname(ha.ZSH_OR_TSIT, full=True),
            ".",
        ],
    ]
    return [
        author.heading_level_2("Introduction", {"id": "introduction"}),
        _p(
            "$MAM (Miqra According to the Masorah) is a digital edition of the Hebrew Bible,"
            " based on the Aleppo Codex and related manuscripts, whose text is on Hebrew"
            " Wikisource. $MAM-for-Sefaria is the extract of $MAM that Sefaria imports and"
            " shows as its default Tanakh. This page describes what the files of"
            " $MAM-for-Sefaria have, and how they encode it.",
        ),
        _p(
            "The files are in the ",
            mb_html.anchor_h(_code("MAM-for-Sefaria"), _PRODUCT_URL),
            " directory of the repository ",
            _code("MAM-basics"),
            ", whose ",
            mb_html.anchor_h("README", _README_URL),
            " says how current they are. Every count, and every example of"
            " $MAM-for-Sefaria, on this page is taken from those files.",
        ),
        _p("This page has three typographic conventions:"),
        author.ordered_list(conventions),
    ]


def _files(s):
    n_books = len(ms.BOOKS)
    rows = [
        _tr(
            [
                _td(_code(f"{ms.FOLDER_CSV}/")),
                _td("Sefaria's"),
                _td_num(len(s.verses)),
                _td(
                    "each verse's reference and its text in HTML, after five header rows"
                ),
            ]
        ),
        _tr(
            [
                _td(_code(f"{ms.FOLDER_AJF}/")),
                _td("$BHS's"),
                _td_num(len(s.ajf_rows)),
                _td(
                    "each verse's reference and plain text, and its two strands where it"
                    " has two cantillations"
                ),
            ]
        ),
        _tr(
            [
                _td(_code(f"{ms.FOLDER_NAMES}/")),
                _td("Sefaria's"),
                _td_num(s.listings["csv verses"]),
                _td(["the code points of each verse of ", _code(f"{ms.FOLDER_CSV}/")]),
            ]
        ),
        _tr(
            [
                _td(_code(f"{ms.FOLDER_NAMES_AJF}/")),
                _td("$BHS's"),
                _td_num(s.listings["ajf verses"]),
                _td(["the code points of each verse of ", _code(f"{ms.FOLDER_AJF}/")]),
            ]
        ),
    ]
    spaced_title = next(book for book in ms.BOOKS if " " in book)
    return [
        author.heading_level_2("The files", {"id": "files"}),
        _p(
            f"$MAM-for-Sefaria has four folders. Each has one file for each of the {n_books}"
            " books, named by the book's title on Sefaria, as ",
            _code(f"{spaced_title}.csv"),
            " is, and a provenance note, ",
            _code(ms.PROVENANCE_NAME),
            ".",
        ),
        _table(["Folder", "Verse numbering", "Verses", "What a file has"], rows),
        *_csv_folder(s),
        *_ajf_folder(s),
        *_listings(s),
        *_numbering(s),
    ]


def _version_notes(html: str) -> list:
    """The header's Version Notes, re-emitted with closed dispatch on its three elements."""
    import html.parser as html_parser

    class Notes(html_parser.HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.stack = [("root", None, [])]

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "br" and not attrs:
                self.stack[-1][2].append(mb_html.line_break())
            elif tag == "i" and not attrs:
                self.stack.append(("i", None, []))
            elif tag == "a" and set(attrs) == {"href"}:
                self.stack.append(("a", attrs["href"], []))
            else:
                raise ValueError(f"Version Notes: unrecognized <{tag} {attrs}>")

        def handle_endtag(self, tag):
            name, href, kids = self.stack.pop()
            if name != tag:
                raise ValueError(f"Version Notes: </{tag}> closes <{name}>")
            el = mb_html.italic(kids) if tag == "i" else mb_html.anchor_h(kids, href)
            self.stack[-1][2].append(el)

        def handle_data(self, data):
            self.stack[-1][2].append(data)

    parser = Notes()
    parser.feed(html)
    parser.close()
    if len(parser.stack) != 1:
        raise ValueError("Version Notes: an unclosed element")
    return parser.stack[0][2]


def _csv_folder(s):
    headers = s.headers
    rows = [
        _tr([_td(_code("Index Title")), _td("the book's title on Sefaria")]),
        _tr([_td(_code("Version Title")), _td(_code(headers["Version Title"]))]),
        _tr([_td(_code("Language")), _td(_code(headers["Language"]))]),
        _tr(
            [
                _td(_code("Version Source")),
                mb_html.table_datum(
                    mb_html.anchor_h(
                        _code(headers["Version Source"]), headers["Version Source"]
                    )
                ),
            ]
        ),
        _tr([_td(_code("Version Notes")), _td("the paragraph of HTML below")]),
    ]
    first = s.verses[0]
    return [
        author.heading_level_3(["The ", _code(f"{ms.FOLDER_CSV}/"), " folder"]),
        _p(
            "Each file of ",
            _code(f"{ms.FOLDER_CSV}/"),
            " is a CSV file in UTF-8, with CRLF line ends and no byte-order mark. Its first"
            " five rows are a header, each row a key and its value. Every file has the same"
            " values, but for the first:",
        ),
        _table(["Key", "Value"], rows),
        _p("The value of ", _code("Version Notes"), ", rendered, is:"),
        mb_html.blockquote(_version_notes(headers["Version Notes"])),
        _p(
            f"After the header, each of the {_num(len(s.verses))} rows is a verse, with two"
            " fields: the verse's reference, such as ",
            _code(first.ref),
            ", and the verse's text, in HTML.",
        ),
    ]


def _ajf_folder(s):
    t = s.ajf_text
    spellings = [
        (
            ["a ", "$samekh", " break"],
            [_uname(sd.NBSP), ", then ", _code("{ס}"), " in a span, then eight more"],
            [_uname(" "), ", ", _code("{ס}"), ", ", _uname(" ")],
        ),
        (
            ["a ", "$pe", " break"],
            [
                _uname(sd.NBSP),
                ", then ",
                _code("{פ}"),
                " in a span, then ",
                _code("<br>"),
            ],
            [_uname(" "), ", ", _code("{פ}"), ", ", _uname(" ")],
        ),
        (
            ["a ", "$legarmeh"],
            [_uname(sd.THSP), ", then ", _uname(hpu.PASOLEG), " in ", _code("<b>")],
            [_uname(hpu.PASOLEG), ", right after its atom"],
        ),
        (
            ["a ", "$paseq"],
            [
                _uname(sd.THSP),
                ", ",
                _uname(hpu.PASOLEG),
                " in ",
                _code("<small>"),
                ", ",
                _uname(sd.THSP),
            ],
            ["two ", _uname(hpu.PASOLEG), " marks, with no space on either side"],
        ),
        (
            ["a space of song spacing"],
            ["eight ", _uname(sd.NBSP), " characters"],
            [_uname(" ")],
        ),
        (
            ["a $ketiv and its $qere"],
            ["in the order $MAM has them"],
            ["the $ketiv first"],
        ),
        (
            ["a trivial pair, an implicit $maqaf, or a small, large or hung letter"],
            ["in a span or element of its own"],
            ["the text alone"],
        ),
    ]
    rows = [
        _tr([_td(what), _td(in_csv), _td(in_ajf)]) for what, in_csv, in_ajf in spellings
    ]
    return [
        author.heading_level_3(["The ", _code(f"{ms.FOLDER_AJF}/"), " folder"]),
        _p(
            "The files of ",
            _code(f"{ms.FOLDER_AJF}/"),
            " are the AJF variant. They are CSV files in UTF-8 with CRLF line ends, as those"
            " of ",
            _code(f"{ms.FOLDER_CSV}/"),
            f" are, but they have no header, and their verses are numbered as in $BHS. Each"
            f" of their {_num(len(s.ajf_rows))} rows has four fields: the verse's reference,"
            " its text, and its ",
            _code("cant-alef"),
            " and ",
            _code("cant-bet"),
            f" strands, which are empty but in the {len(s.dual_cant_refs)} verses that have"
            f" two cantillations: {_refs(s.dual_cant_refs)}.",
        ),
        _p(
            "In those verses the second field has the text that represents both strands, as ",
            _code(f"{ms.FOLDER_CSV}/"),
            " has it too. The third and fourth fields have the strands themselves, which are,"
            " as ",
            mb_html.anchor_h(
                "the guide to MAM-simple's JSON",
                f"{_MAM_SIMPLE_GUIDE}#dual-cantillation-cant-all-three",
            ),
            " says, the ",
            _he("תחתון"),
            " and ",
            _he("עליון"),
            " strands in the Decalogues, and the ",
            _he("פשוטה"),
            " and ",
            _he("מדרשית"),
            " strands at Genesis 35:22.",
        ),
        _p(
            "Their text is plain: it has no HTML, and neither of the two spaces that ",
            _code(f"{ms.FOLDER_CSV}/"),
            " writes as character references. So they spell some things differently:",
        ),
        _table(
            ["", mb_html.code(f"{ms.FOLDER_CSV}/"), mb_html.code(f"{ms.FOLDER_AJF}/")],
            rows,
        ),
        _p(
            "In the text field of ",
            _code(f"{ms.FOLDER_AJF}/"),
            ", each of these has the count it has in ",
            _code(f"{ms.FOLDER_CSV}/"),
            f": {_num(t['combined legarmeh'])} $legarmeh and {_num(t['combined paseq'])}"
            f" $paseq marks, {_num(t['combined samekh'])} $samekh and"
            f" {_num(t['combined pe'])} $pe breaks, and {_num(t['combined pairs'])} pairs of"
            " a $ketiv and its $qere.",
        ),
    ]


def _listings(s):
    verse = s.verse(_EX_LISTING)
    head = f"{verse.bk39id} {verse.chapter}:{verse.verse} in vtrad {tbn.VT_SEF}"
    lines = ms.listing_verse(ms.FOLDER_NAMES, verse.book, head)
    # mb_html wraps a line longer than 100 characters, and refuses two spaces in a row.
    if any(len(line) > 90 or "  " in line for line in lines):
        raise ValueError(
            f"{_EX_LISTING}: a listing line that the page's <pre> would break"
        )
    ajf_row = next(row for row in s.ajf_rows if row.bk39id != row.book)
    ajf_head = (
        f"{ajf_row.bk39id} {ajf_row.chapter}:{ajf_row.verse} in vtrad {tbn.VT_BHS}"
    )
    chars = sorted(s.code_points_csv.keys() | s.code_points_ajf.keys())
    rows = [
        _tr(
            [
                mb_html.table_datum(_code(f"U+{ord(c):04X}")),
                mb_html.table_datum(_uname(c, full=True)),
                mb_html.table_datum(_code(ms.short_name_in_listings(c))),
                _td_num(s.code_points_csv[c]),
                _td_num(s.code_points_ajf[c]),
            ]
        )
        for c in chars
    ]
    return [
        author.heading_level_3("The Unicode-name listings"),
        _p(
            "Each file of ",
            _code(f"{ms.FOLDER_NAMES}/"),
            " lists the code points of one book of ",
            _code(f"{ms.FOLDER_CSV}/"),
            ", and each file of ",
            _code(f"{ms.FOLDER_NAMES_AJF}/"),
            " those of one book of ",
            _code(f"{ms.FOLDER_AJF}/"),
            ". They are text files in UTF-8, with LF line ends. A listing's first line is ",
            _code(f"unicode_names {verse.book}"),
            ", for its book. Then each verse has a line that names it, a line for each run"
            " of its text, and a blank line, but for the last verse.",
        ),
        _p(
            "The line that names a verse has the book's identifier in ",
            _code("MAM-basics"),
            ", the chapter and verse, and the verse numbering, as ",
            _code(head),
            " and ",
            _code(ajf_head),
            " do. Each ",
            _uname(" "),
            " and ",
            _uname(sd.NBSP),
            " has a line of its own, with its name, and so splits the text into runs. A"
            " run's line has its code points, separated by commas, each by the short name"
            " that the table below gives it. In ",
            _code(f"{ms.FOLDER_NAMES}/"),
            ", each HTML element has lines of its own: one with ",
            _code("START"),
            " and the element's tag and class before its contents, and one with ",
            _code("STOP"),
            " after them, or a single line with ",
            _code("START/STOP"),
            " for ",
            _code("br"),
            ", which has no contents. In ",
            _code(f"{ms.FOLDER_NAMES_AJF}/"),
            ", a verse with two cantillations lists each of its three texts after a line"
            " that names it, ",
            _code("rv-cant-combined"),
            ", ",
            _code("rv-cant-alef"),
            " or ",
            _code("rv-cant-bet"),
            ", with the text's lines indented by four spaces.",
        ),
        _p(
            f"For example, {_EX_LISTING} has this text in ",
            _code(f"{ms.FOLDER_CSV}/"),
            ":",
        ),
        mb_html.div(
            [
                mb_html.table(
                    [
                        _tr(
                            [
                                _td_he(_snippet(verse, 0, len(verse.text))),
                                _td_ref(verse.ref),
                            ]
                        )
                    ],
                    {"class": "data"},
                )
            ],
            {"class": "table-wrap"},
        ),
        _p("and these lines in its listing:"),
        mb_html.htel_mk("pre", None, ["\n".join(lines)]),
        _p(
            f"These are all {len(chars)} code points that the files have, with the short name"
            " each has in the listings, and how many times each folder has it:"
        ),
        _table(
            [
                "Code point",
                "Unicode name",
                "In the listings",
                mb_html.code(f"{ms.FOLDER_CSV}/"),
                mb_html.code(f"{ms.FOLDER_AJF}/"),
            ],
            rows,
        ),
    ]


def _numbering(s):
    em_dash_refs = s.em_dash_csv
    return [
        author.heading_level_3("Verse numbering"),
        _p(
            "The verses of ",
            _code(f"{ms.FOLDER_CSV}/"),
            " are numbered as Sefaria numbers them, and those of ",
            _code(f"{ms.FOLDER_AJF}/"),
            " as $BHS numbers them, so a reference can name different text in the two"
            " folders. The page ",
            mb_html.anchor_h(
                "Versification Differences: MAM, BHS, and Sefaria", _VERSIFICATION
            ),
            " lists the differences. Every reference of ",
            _code(f"{ms.FOLDER_CSV}/"),
            " is also in ",
            _code(f"{ms.FOLDER_AJF}/"),
            f", which has {len(s.refs_only_ajf)} more: {_refs(s.refs_only_ajf)}.",
        ),
        _p(
            f"Both numberings have {_refs(em_dash_refs)}, for which $MAM has no text. In"
            " both folders, each of these rows has only an ",
            _uname(ms.EM_DASH),
            " (",
            ms.EM_DASH,
            "), since an empty field would let the text of another version show at that"
            " verse on Sefaria. The files have no other ",
            _uname(ms.EM_DASH),
            ".",
        ),
    ]


def _markup(s):
    c = s.element_counts
    described = {
        ("span", "mam-spi-samekh"): ["a $samekh break, ", _code("{ס}")],
        ("span", "mam-spi-pe"): ["a $pe break, ", _code("{פ}")],
        ("span", "mam-spi-invnun"): ["an inverted $nun, ", _uname(hpu.NUN_HAF)],
        ("span", "mam-implicit-maqaf"): [
            "a gray $maqaf (see ",
            mb_html.anchor_h("Gray maqaf", _GRAY_MAQAF),
            ")",
        ],
        ("span", "mam-kq"): ["a $ketiv and its $qere"],
        ("span", "mam-kq-k"): ["a $ketiv, in parentheses"],
        ("span", "mam-kq-q"): ["a $qere, in square brackets"],
        ("span", "mam-kq-trivial"): ["a trivial $ketiv_qere pair, as one pointed atom"],
        ("span", "k-velo-q-maq"): ["a $maqaf after a $ketiv_velo_qere"],
        ("b", None): ["the ", _uname(hpu.PASOLEG), " of a $legarmeh"],
        ("small", None): [
            "the ",
            _uname(hpu.PASOLEG),
            f" of a $paseq ({_num(c['small paseq'])}), or a small letter"
            f" ({_num(c['small letter'])})",
        ],
        ("big", None): ["a large letter"],
        ("sup", None): ["a hung letter"],
        ("br", None): ["nothing: it follows each $pe break"],
    }
    if set(described) != set(ms.ELEMENT_ORDER):
        raise ValueError(
            "an element of the files that the markup table does not describe"
        )
    kinds = dict(
        zip(ms.ELEMENT_ORDER, (ms._ELEMENT_KINDS[k] for k in ms.ELEMENT_ORDER))
    )
    rows = [
        _tr(
            [
                mb_html.table_datum(_code(tag)),
                mb_html.table_datum(_code(cls) if cls else ""),
                _td_num(c[kinds[(tag, cls)]]),
                _td(described[(tag, cls)]),
            ]
        )
        for tag, cls in ms.ELEMENT_ORDER
    ]
    return [
        author.heading_level_2("Markup", {"id": "markup"}),
        _p(
            "The verse text of ",
            _code(f"{ms.FOLDER_CSV}/"),
            f" is HTML with {len({tag for tag, _ in ms.ELEMENT_ORDER})} elements, of which"
            " only ",
            _code("span"),
            " has an attribute, its class. These are all the elements and classes that the"
            " files have:",
        ),
        _table(["Element", "Class", "Count", "What it holds"], rows),
        *_legarmeh_and_paseq(s),
        *_spaces(s),
        *_breaks(s),
        *_letter_sizes(s),
        *_ketiv_qere(s),
    ]


def _legarmeh_and_paseq(s):
    rows = [
        _tr(
            [
                _td_he(_lift(_EX_LEGARMEH[0], _EX_LEGARMEH[1], s, whole=False)),
                _td_ref(_EX_LEGARMEH[0]),
                _td("$legarmeh"),
                _td(
                    [
                        _uname(sd.THSP),
                        ", then ",
                        _uname(hpu.PASOLEG),
                        " in ",
                        _code("<b>"),
                        ", then the space before the next atom",
                    ]
                ),
                _td_num(s.spacing["legarmeh"]),
            ]
        ),
        _tr(
            [
                _td_he(_lift(_EX_PASEQ[0], _EX_PASEQ[1], s, whole=False)),
                _td_ref(_EX_PASEQ[0]),
                _td("$paseq"),
                _td(
                    [
                        _uname(sd.THSP),
                        ", ",
                        _uname(hpu.PASOLEG),
                        " in ",
                        _code("<small>"),
                        ", ",
                        _uname(sd.THSP),
                        "; no other space comes before the next atom",
                    ]
                ),
                _td_num(s.spacing["paseq"]),
            ]
        ),
    ]
    return [
        author.heading_level_3(["$Legarmeh and $paseq"]),
        _p(
            "A $legarmeh and a $paseq are both the code point ",
            _uname(hpu.PASOLEG),
            ". The files tell them apart by markup and spacing:",
        ),
        _table(["Example", "Reference", "Mark", "Encoding", "Count"], rows),
        _p(
            "So the spacing keeps a $legarmeh with the atom before it, and puts a $paseq"
            " between two atoms.",
        ),
    ]


def _spaces(s):
    sp = s.spacing
    contexts = (
        ("before-break", "one", ["before a $samekh or $pe break"]),
        ("after-samekh", "eight", ["after a $samekh break"]),
        ("after-invnun", "one", ["after an inverted $nun"]),
        ("before-invnun", "one", ["before an inverted $nun"]),
        ("song-layout", "eight", ["a space of song spacing"]),
    )
    rows = [
        _tr([_td(where), _td(run), _td_num(sp[f"nbsp {key}"])])
        for key, run, where in contexts
    ]
    chapters = [
        (key[len("song-layout ") :], count)
        for key, count in sp.items()
        if key.startswith("song-layout ")
    ]
    order = {book: index for index, book in enumerate(ms.BOOKS)}

    def chapter_key(item):
        book, chapter = item[0].rsplit(" ", 1)
        return order[book], int(chapter)

    chapters.sort(key=chapter_key)
    total_runs = sum(sp[f"nbsp {key}"] for key, _run, _where in contexts)
    if total_runs != sum(len(re.findall(f"{sd.NBSP}+", v.text)) for v in s.verses):
        raise ValueError("a run of NO-BREAK SPACE that the table of spaces leaves out")
    return [
        author.heading_level_3("Spaces"),
        _p(
            "The files write ",
            _uname(sd.NBSP),
            " and ",
            _uname(sd.THSP),
            " as the character references ",
            _code("&nbsp;"),
            f" ({_num(s.entities['nbsp'])} times) and ",
            _code("&thinsp;"),
            f" ({_num(s.entities['thinsp'])} times), and have no other character"
            " reference. Each ",
            _uname(sd.THSP),
            " is beside the ",
            _uname(hpu.PASOLEG),
            " of a $legarmeh or a $paseq, as above. A ",
            _uname(sd.NBSP),
            " comes alone or in a run of eight:",
        ),
        _table(["Where", "Run", "Count"], rows),
        _p(
            "Song spacing, $MAM-simple's ",
            _code("shirah-space"),
            ", is in these chapters, with these numbers of spaces: ",
            *_join([f"{chapter} ({_num(count)})" for chapter, count in chapters]),
            ".",
        ),
    ]


def _breaks(s):
    c = s.element_counts
    invnun_refs = [v.ref for v in s.verses for el in v.elements if el.kind == "invnun"]
    return [
        author.heading_level_3(["Breaks and inverted $nun"]),
        _p(
            f"Each of the {_num(c['samekh'])} $samekh breaks is ",
            _code("{ס}"),
            " in a span of class ",
            _code("mam-spi-samekh"),
            ", with a ",
            _uname(sd.NBSP),
            f" before it and eight after it, and each of the {_num(c['pe'])} $pe breaks is ",
            _code("{פ}"),
            " in a span of class ",
            _code("mam-spi-pe"),
            ", with a ",
            _uname(sd.NBSP),
            " before it and a ",
            _code("<br>"),
            f" after it. Most end a verse, but {_num(c['samekh inside a verse'])} $samekh"
            f" and {_num(c['pe inside a verse'])} $pe breaks are inside one.",
        ),
        _p(
            f"Each of the {_num(c['invnun'])} inverted $nun marks is ",
            _he(hpu.NUN_HAF),
            " (",
            _uname(hpu.NUN_HAF),
            ") in a span of class ",
            _code("mam-spi-invnun"),
            f", at {_refs(invnun_refs)}.",
        ),
    ]


def _letter_sizes(s):
    c = s.element_counts
    verse, kq = _kq_element(*_EX_SMALL_IN_KETIV, s)
    rows = [
        _tr([_td_he(_lift(ref, parts, s)), _td_ref(ref), _td(what)])
        for ref, parts, what in _EX_LETTER_SIZES
    ]
    rows.append(
        _tr(
            [
                _td_he(_lift_element(verse, kq)),
                _td_ref(verse.ref),
                _td("a small letter in a $ketiv"),
            ]
        )
    )
    hung_refs = [v.ref for v in s.verses for el in v.elements if el.kind == "hung"]
    return [
        author.heading_level_3("Small, large and hung letters"),
        _p(
            "A small letter is in ",
            _code("<small>"),
            f" ({_num(c['small letter'])} times), a large letter in ",
            _code("<big>"),
            f" ({_num(c['large'])} times) and a hung letter in ",
            _code("<sup>"),
            f" ({_num(c['hung'])} times, at {_refs(hung_refs)}). Each of these elements holds"
            " one letter and its marks:",
        ),
        _table(["Example", "Reference", "What it has"], rows),
    ]


def _ketiv_qere(s):
    shapes = s.kq_shapes
    if set(shapes) != set(_EX_KQ):
        raise ValueError(f"ketiv/qere shapes {sorted(set(shapes) ^ set(_EX_KQ))}")
    order_cells = {"ketiv first": "the $ketiv first", "qere first": "the $qere first"}
    rows = []
    for shape in sorted(_EX_KQ, key=lambda k: (-shapes[k], k)):
        order, separator, words_k, words_q = shape
        verse, el = _kq_element(*_EX_KQ[shape], s)
        rows.append(
            _tr(
                [
                    _td_he(_lift_element(verse, el)),
                    _td_ref(verse.ref),
                    _td(order_cells[order]),
                    _td("a space" if separator == "space" else ["a ", _uname(hpu.MAQ)]),
                    _td(f"{words_k}, {words_q}"),
                    _td_num(shapes[shape]),
                ]
            )
        )
    n_pairs = sum(shapes.values())
    qere_first = sum(n for k, n in shapes.items() if k[0] == "qere first")
    maqaf_separated = sum(n for k, n in shapes.items() if k[1] == "maqaf")
    velo = s.velo
    kvq_ref, kvq_letters = _EX_KETIV_VELO_QERE
    kvq_verse, kvq = _velo_element(kvq_ref, "ketiv", kvq_letters, s)
    qvk_ref, qvk_letters = _EX_QERE_VELO_KETIV
    qvk_verse, qvk = _velo_element(qvk_ref, "qere", qvk_letters, s)
    maq_refs = velo["k-velo-q-maq"]
    maq_verse = s.verse(maq_refs[0])
    maq_el = next(el for el in maq_verse.elements if el.kind == "k-velo-q-maq")
    trivial = _lift(_EX_TRIVIAL[0], _EX_TRIVIAL[1], s)
    velo_rows = [
        _tr(
            [
                _td_he(_lift_element(kvq_verse, kvq)),
                _td_ref(kvq_verse.ref),
                _td("a $ketiv_velo_qere"),
                _td_num(len(velo["ketiv"])),
            ]
        ),
        _tr(
            [
                _td_he(_lift_element(qvk_verse, qvk)),
                _td_ref(qvk_verse.ref),
                _td("a $qere_velo_ketiv"),
                _td_num(len(velo["qere"])),
            ]
        ),
        _tr(
            [
                _td_he(_lift_element(maq_verse, maq_el)),
                _td_ref(maq_verse.ref),
                _td("a $maqaf after a $ketiv_velo_qere"),
                _td_num(len(maq_refs)),
            ]
        ),
        _tr(
            [
                _td_he(trivial),
                _td_ref(_EX_TRIVIAL[0]),
                _td("a trivial pair"),
                _td_num(s.element_counts["trivial"]),
            ]
        ),
    ]
    words_header = mb_html.span(
        "Words", {"title": "the number of words of the ketiv, then of the qere"}
    )
    return [
        author.heading_level_3(["$Ketiv and $qere"]),
        _p(
            f"Each of the {_num(n_pairs)} pairs of a $ketiv and its $qere is a span of class ",
            _code("mam-kq"),
            ", which holds the $ketiv, unpointed and in parentheses, in a span of class ",
            _code("mam-kq-k"),
            ", and the $qere, pointed and in square brackets, in a span of class ",
            _code("mam-kq-q"),
            ", with a separator between them: a space or, in ",
            _num(maqaf_separated),
            " pairs, a ",
            _uname(hpu.MAQ),
            ". The files keep the order that $MAM's pages on Hebrew Wikisource have, which"
            f" puts the $qere first in {_num(qere_first)} pairs,"
            f" {_num(s.kq_qere_first_after_maqaf)} of them right after a $maqaf. By"
            " order, separator, and the words of each part, the pairs are of these shapes:",
        ),
        _table(
            ["Example", "Reference", "Order", "Separator", words_header, "Count"], rows
        ),
        _p(
            "A $ketiv_velo_qere, a $ketiv that is written but not read, is a span of class ",
            _code("mam-kq-k"),
            " with no pair around it, at ",
            _refs([ref for ref, _ in velo["ketiv"]]),
            ". A $qere_velo_ketiv, a $qere that is read but not written, is likewise a span"
            " of class ",
            _code("mam-kq-q"),
            ", at ",
            _refs([ref for ref, _ in velo["qere"]]),
            ". A trivial pair, which ",
            mb_html.anchor_h("the guide to MAM-simple's JSON", _MAM_SIMPLE_GUIDE),
            " describes as a $ketiv_qere \N{LEFT DOUBLE QUOTATION MARK}whose two forms differ"
            " in a way that needs no separate display\N{RIGHT DOUBLE QUOTATION MARK}, is one"
            " pointed atom in a span of class ",
            _code("mam-kq-trivial"),
            ". An example of each, with its count:",
        ),
        _table(["Example", "Reference", "What it is", "Count"], velo_rows),
    ]


def _characters(s):
    return [
        author.heading_level_2("Characters", {"id": "characters"}),
        *_context_marks(s),
        *_own_code_points(s),
        *_geresh_telisha(s),
        *_zarqa(s),
        *_meteg_after_silluq(s),
        *_mark_order(s),
    ]


def _context_marks(s):
    by = s.by_system
    rows_spec = (
        (ha.ZSH_OR_TSIT, "prose", ["the $zarqa's stress helper"]),
        (ha.ZSH_OR_TSIT, "poetic", ["$tsinnorit"]),
        (ha.Z_OR_TSOR, "prose", ["$zarqa"]),
        (ha.Z_OR_TSOR, "poetic", ["$tsinnor"]),
        (hpu.PASOLEG, "b", ["$legarmeh"]),
        (hpu.PASOLEG, "small", ["$paseq"]),
        (ha.YBY, "prose", ["$yby"]),
        (ha.YBY, "poetic", ["$galgal"]),
        (ha.ATN_H, "poetic", ["$ah"]),
        (ha.GER, "prose", ["$geresh"]),
        (ha.GER_M, "poetic", ["$germuq, which with $revia is $revmug"]),
    )
    rows = []
    for char, where, mark in rows_spec:
        if where in ("prose", "poetic"):
            count = by[(char, where)]
            where_cell = f"{where} verses"
        else:
            count = s.spacing["legarmeh" if where == "b" else "paseq"]
            where_cell = ["in ", _code(f"<{where}>")]
        if not count:
            raise ValueError(f"{unicode_data.name(char)} has no {where} row to show")
        rows.append(
            _tr(
                [
                    mb_html.table_datum(_uname(char)),
                    _td(where_cell),
                    _td_num(count),
                    _td(mark),
                ]
            )
        )
    return [
        author.heading_level_3("Code points that stand for more than one mark"),
        _p(
            "Some code points stand for different marks in different places: by the system"
            " of accents of the verse, prose or poetic, or, for ",
            _uname(hpu.PASOLEG),
            ", by its markup. As $MAM-for-Sefaria uses them:",
        ),
        _table(["Code point", "Where", "Count", "Mark"], rows),
        _p(
            _uname(ha.ATN_H),
            " and ",
            _uname(ha.GER_M),
            " are only in poetic verses, and ",
            _uname(ha.GER),
            f" only in prose verses. Each of the {_num(s.zarqa['geresh muqdam with revia'])}"
            " atoms with a ",
            _uname(ha.GER_M),
            " has it on its first letter, and also has a ",
            _uname(ha.REV),
            ".",
        ),
    ]


def _own_code_points(s):
    meanings = {
        _QAMATS_QATAN: ["$qq"],
        _HOLAM_HASER_FOR_VAV: ["$xolam_xaser on a $vav that is a consonant"],
        hpo.RAFE: ["$rafeh"],
        hpu.UPDOT: ["an extraordinary dot above a letter"],
        hpu.LODOT: ["an extraordinary dot below a letter"],
    }
    rows = []
    for char in ms.OWN_CODE_POINT_MARKS:
        ref, parts = _EX_OWN_CODE_POINT[char]
        form = _lift(ref, parts, s)
        rows.append(
            _tr(
                [
                    _td_he(form),
                    _td_ref(ref),
                    mb_html.table_datum(_uname(char)),
                    _td(meanings[char]),
                    _td_num(s.code_points_csv[char]),
                    _td_num(s.atoms[f"with {unicode_data.name(char)}"]),
                ]
            )
        )
    return [
        author.heading_level_3("Marks with code points of their own"),
        _p(
            "$MAM-for-Sefaria has each of these marks as a code point of its own. The counts"
            " are of the marks and of the atoms that have them:"
        ),
        _table(["Example", "Reference", "Code point", "Mark", "Marks", "Atoms"], rows),
    ]


def _geresh_telisha(s):
    rows = []
    for hit in s.geresh_telisha:
        verse = s.verse(hit["ref"])
        names = []
        for cluster in hit["clusters"]:
            if names:
                names.append(mb_html.line_break())
            names.extend(_name_list(cluster))
        start = verse.text.index(hit["atom"])
        if verse.text.count(hit["atom"]) != 1:
            raise ValueError(f"{hit['ref']}: {hit['atom']!r} is there more than once")
        span = _chanted_words(verse.text, start, start + len(hit["atom"]))
        rows.append(
            _tr(
                [
                    _td_he(_snippet(verse, *span)),
                    _td_ref(hit["ref"]),
                    mb_html.table_datum(names),
                ]
            )
        )
    two_letter = sum(1 for hit in s.geresh_telisha if len(hit["clusters"]) == 2)
    return [
        author.heading_level_3(
            ["A letter with $geresh or $gershayim and $telisha_gedolah"]
        ),
        _p(
            f"In {len(s.geresh_telisha)} atoms, a letter has a ",
            _uname(ha.GER),
            " or a ",
            _uname(ha.GER_2),
            " and then a ",
            _uname(ha.TEL_G),
            f"; in {two_letter} of them two letters do. The letters' code points, in order:",
        ),
        _table(["Example", "Reference", "Code points"], rows),
    ]


def _zarqa(s):
    z = s.zarqa
    rows = []
    for ref, parts in _EX_ZARQA:
        atom = _lift_atom(ref, parts, s)
        verse = s.verse(ref)
        start, end = _find(verse.text, parts, ref)
        names = []
        for cluster in ms.CLUSTER_RE.findall(atom):
            if names:
                names.append(mb_html.line_break())
            names.extend(_name_list(cluster))
        rows.append(
            _tr(
                [
                    _td_he(_snippet(verse, *_chanted_words(verse.text, start, end))),
                    _td_ref(ref),
                    mb_html.table_datum(names),
                ]
            )
        )
    return [
        author.heading_level_3(["The $zarqa and its stress helper"]),
        _p(
            f"Each of the {_num(z['z-or-tsor prose'] + z['z-or-tsor poetic'])} ",
            _uname(ha.Z_OR_TSOR),
            " marks is on the last letter of its atom: the $zarqa in prose verses and the"
            " $tsinnor in poetic verses. Of them,"
            f" {_num(z['z-or-tsor prose lamed'] + z['z-or-tsor poetic lamed'])} are on a"
            " $lamed, as at"
            " Leviticus 4:2 below. In prose verses, each of"
            f" the {_num(z['zsh-or-tsit prose'])} ",
            _uname(ha.ZSH_OR_TSIT),
            " marks is the $zarqa's stress helper, on an earlier letter of the atom than its ",
            _uname(ha.Z_OR_TSOR),
            ", as at Genesis 19:4:",
        ),
        _table(["Example", "Reference", "Code points"], rows),
    ]


def _meteg_after_silluq(s):
    cases = s.silluq_cases
    heads = [mb_html.table_header("Version", {"scope": "col"})]
    sefaria_cells = []
    other_cells = []
    for case in cases:
        heads.append(
            mb_html.table_header(
                case["ref"], {"scope": "col", "data-osis-id": case["osis_id"]}
            )
        )
        # The attention color runs from the letter whose meteg the Sefaria form lacks.
        full_clusters = ms.CLUSTER_RE.findall(case["full"])
        dropped = [
            i
            for i, cluster in enumerate(full_clusters)
            if i > case["silluq_index"] and hpo.MTGOSLQ in cluster
        ]
        for atom, cells in (
            (case["sefaria"], sefaria_cells),
            (case["full"], other_cells),
        ):
            cut = list(ms.CLUSTER_RE.finditer(atom))[dropped[0]].start()
            contents = [atom[:cut], mb_html.span_c(atom[cut:], "attention")]
            cells.append(mb_html.table_datum(contents, {"lang": "hbo", "dir": "rtl"}))
    table = mb_html.table(
        [
            mb_html.table_row(heads),
            mb_html.table_row(
                [mb_html.table_header("Sefaria", {"scope": "row"}), *sefaria_cells],
                {"data-version": "sefaria"},
            ),
            mb_html.table_row(
                [
                    mb_html.table_header(
                        author.dollar_sub("other versions of $MAM"), {"scope": "row"}
                    ),
                    *other_cells,
                ],
                {"data-version": "other-mam"},
            ),
        ],
        {"id": "meteg-after-silluq-cases", "class": "data"},
    )
    return [
        author.heading_level_3(
            ["A $meteg after the ", _SILLUQ], {"id": "meteg-after-silluq"}
        ),
        _p(
            f"In {len(cases)} atoms, $MAM's source identifies a ",
            _SILLUQ,
            " that has a $meteg after it, on a later letter of the atom. $MAM-for-Sefaria, in ",
            _code(f"{ms.FOLDER_CSV}/"),
            " and ",
            _code(f"{ms.FOLDER_AJF}/"),
            " alike, has the ",
            _SILLUQ,
            " and every other mark of each atom, but not that $meteg, which other versions"
            " of $MAM, $MAM-simple among them, have:",
        ),
        mb_html.div([table], {"class": "table-wrap"}),
    ]


def _mark_order(s):
    a = s.atoms
    return [
        author.heading_level_3("Mark order"),
        _p(
            "The marks of each letter are in $MAM's order, which is not Unicode's: a ",
            _uname(hpo.SHIND),
            " or ",
            _uname(hpo.SIND),
            " comes first, then a ",
            _uname("\N{HEBREW POINT DAGESH OR MAPIQ}"),
            ", then a ",
            _uname(hpo.RAFE),
            ", and then the other marks, in the order $MAM gives them. A ",
            mb_html.anchor_h("note in MAM-basics", _MARK_ORDER_URL),
            " says more. Unicode normalization puts the marks in Unicode's order, and would"
            f" change the order of the marks of {_num(a['changed by NFC'])} of the"
            f" {_num(a['atoms'])} atoms of ",
            _code(f"{ms.FOLDER_CSV}/"),
            ".",
        ),
    ]


def _left_out(s):
    return [
        author.heading_level_2("What the files leave out", {"id": "left-out"}),
        _p(
            "The handlers of ",
            mb_html.anchor_h(_code("py/mb_sefaria/mam4sef_handlers.py"), _HANDLERS_URL),
            " write nothing for these three things that $MAM-simple has:",
        ),
        author.ordered_list(
            [
                [
                    "Its ",
                    mb_html.anchor_h(
                        "notes on scroll differences",
                        f"{_MAM_SIMPLE_GUIDE}#scroll-differences-scrdfftar",
                    ),
                    " (",
                    _code("sdt-note"),
                    "). The files keep the text that each note is about, and have no"
                    " notes. $MAM's documentation notes, which $MAM-simple does not have"
                    " either, are in $MAM-with-doc, to which the files' ",
                    _code("Version Notes"),
                    " link.",
                ],
                [
                    "The ",
                    mb_html.anchor_h(
                        "verse that four books repeat",
                        f"{_MAM_SIMPLE_GUIDE}#repeated-endings-good-ending",
                    ),
                    " after their last (",
                    _code("good-ending"),
                    ").",
                ],
                [
                    "In ",
                    _code(f"{ms.FOLDER_CSV}/"),
                    ", the ",
                    _code("cant-alef"),
                    " and ",
                    _code("cant-bet"),
                    f" strands of the {len(s.dual_cant_refs)} verses with two cantillations,"
                    " whose text represents both strands at once. ",
                    _code(f"{ms.FOLDER_AJF}/"),
                    " has the strands too.",
                ],
            ]
        ),
    ]


def _cgj_rows_jerusalem(s):
    rows = []
    for kind in ("jerusalem-hiriq", "jerusalem-sheva"):
        by_type = {}
        for hit in s.cgj[kind]:
            by_type.setdefault((hit["before"][0], hit["after"]), []).append(hit)
        for key in sorted(by_type, key=lambda k: (k[1] != _HIRIQ, k[0] != _PATAH)):
            hits = by_type[key]
            ref, parts = _EX_JERUSALEM[key]
            verse = s.verse(ref)
            start, end = _find(verse.text, parts, ref)
            atom = verse.text[start:end]
            example = [h for h in hits if h["ref"] == ref and h["atom"] == atom]
            if len(example) != 1:
                raise ValueError(f"{ref}: the example is not one of its kind's atoms")
            index = len(ms.letters_of(atom)) - (2 if key[1] == _HIRIQ else 3)
            word_start, word_end = _chanted_words(verse.text, start, end)
            form = [
                verse.text[word_start:start],
                *_highlight(atom, index),
                verse.text[end:word_end],
            ]
            bare = sum(1 for h in hits if len(h["before"]) == 1)
            vowel_name = ms.short_name(key[0])
            count = [_num(len(hits))]
            if bare:
                count.extend(
                    [f" ({_num(bare)} with no accent or ", _uname(hpo.MTGOSLQ), ")"]
                )
            rows.append(
                _tr(
                    [
                        _td_he([part for part in form if part != ""]),
                        _td_ref(ref),
                        mb_html.table_datum(_name_list(example[0]["cluster"])),
                        mb_html.table_datum(_name_list(example[0]["normalized"])),
                        mb_html.table_datum(count, {"class": "num"}),
                    ]
                )
            )
            if vowel_name not in ("PATAH", "QAMATS"):
                raise ValueError(f"{ref}: a Jerusalem lamed with {vowel_name}")
    return rows


def _aligned_words(fields: list, position: int) -> list:
    """For aligned texts, the chanted words around atom ``position``, whole in every text."""
    atoms = [list(ms.ATOM_RE.finditer(f)) for f in fields]

    def word_of(field, match):
        return len(re.findall(r"\s+", field[: match.start()].lstrip()))

    word_ids = [[word_of(f, m) for m in found] for f, found in zip(fields, atoms)]
    lo = hi = position
    while True:
        new_lo, new_hi = lo, hi
        for ids in word_ids:
            new_lo = min(new_lo, min(i for i, w in enumerate(ids) if w == ids[lo]))
            new_hi = max(new_hi, max(i for i, w in enumerate(ids) if w == ids[hi]))
        if (new_lo, new_hi) == (lo, hi):
            break
        lo, hi = new_lo, new_hi
    out = []
    for field, found in zip(fields, atoms):
        start, end = _chanted_words(field, found[lo].start(), found[hi].end())
        out.append(field[start:end])
    return out


def _cgj_rows_strands(s, kind):
    by_atom = {}
    for hit in s.cgj[kind]:
        by_atom.setdefault(hit["atom"], []).append(hit)
    rows = []
    for atom, hits in by_atom.items():
        strands = hits[0]["strands"]
        row = s.ajf_row(strands["ref"])
        fields = [row.combined, row.alef, row.bet]
        combined_atoms = [m.group() for m in ms.ATOM_RE.finditer(row.combined)]
        position = combined_atoms.index(atom)
        combined, alef, bet = _aligned_words(fields, position)
        cluster_index = next(
            i for i, c in enumerate(ms.CLUSTER_RE.findall(atom)) if sd.CGJ in c
        )

        def shown(text, strand_atom):
            if text.count(strand_atom) != 1:
                raise ValueError(f"{row.ref}: {strand_atom!r} is not once in {text!r}")
            a = text.index(strand_atom)
            return [
                part
                for part in (
                    text[:a],
                    *_highlight(strand_atom, cluster_index),
                    text[a + len(strand_atom) :],
                )
                if part != ""
            ]

        csv_refs = _refs([h["ref"] for h in hits])
        ajf_refs = _refs([h["strands"]["ref"] for h in hits])
        # The three forms one above the other in one cell, in the order the header names.
        forms = [
            *shown(combined, atom),
            mb_html.line_break(),
            *shown(alef, strands["alef"]),
            mb_html.line_break(),
            *shown(bet, strands["bet"]),
        ]
        rows.append(
            _tr(
                [
                    _td_he(forms),
                    mb_html.table_datum(ajf_refs, {"class": "bcv"}),
                    mb_html.table_datum(csv_refs, {"class": "bcv"}),
                    mb_html.table_datum(_name_list(hits[0]["cluster"])),
                    mb_html.table_datum(_name_list(hits[0]["normalized"])),
                ]
            )
        )
    return rows


def _robust_unicode(s):
    cgj = s.cgj
    total = sum(len(hits) for hits in cgj.values())
    if total != s.code_points_csv[sd.CGJ]:
        raise ValueError("a CGJ of csv/ that no kind accounts for")
    two_vowel_kinds = ("jerusalem-hiriq", "jerusalem-sheva", "qupo")
    two_vowels = sum(len(cgj[k]) for k in two_vowel_kinds)
    if two_vowels != s.atoms["letters with two vowels"]:
        raise ValueError("a letter with two vowels that no CGJ kind accounts for")
    headers_j = [
        "Example",
        "Reference",
        ["The ", "$lamed", "'s code points"],
        "Normalized without the CGJ",
        "Count",
    ]
    headers_s = [
        [
            "Both strands",
            mb_html.line_break(),
            mb_html.code("cant-alef"),
            mb_html.line_break(),
            mb_html.code("cant-bet"),
        ],
        ["In ", mb_html.code(f"{ms.FOLDER_AJF}/")],
        ["In ", mb_html.code(f"{ms.FOLDER_CSV}/")],
        "The letter's code points",
        "Normalized without the CGJ",
    ]
    n_j_hiriq, n_j_sheva = len(cgj["jerusalem-hiriq"]), len(cgj["jerusalem-sheva"])
    n_j_bare = sum(
        1
        for kind in ("jerusalem-hiriq", "jerusalem-sheva")
        for hit in cgj[kind]
        if len(hit["before"]) == 1
    )
    if not 0 < n_j_bare < n_j_hiriq + n_j_sheva:
        raise ValueError(
            "the Jerusalem paragraph's exception has no atom, or every atom"
        )
    return [
        author.heading_level_2("Robust Unicode", {"id": "robust-unicode"}),
        _p(
            "Unicode normalization sorts the marks of each letter by their combining classes."
            " A ",
            _uname(sd.CGJ, full=True),
            " (",
            _cgj(),
            ") has combining class 0, so normalization moves no mark across one."
            f" $MAM-for-Sefaria has {_num(total)} of them, each on a letter whose marks"
            " normalization would otherwise put in another order: it keeps the vowel or ",
            _uname(hpo.MTGOSLQ),
            " after it in place after the marks before it. Every letter of the files that has"
            " two vowels has a ",
            _cgj(),
            " between them. The tables give, for each kind, the code points of the letter in"
            " order, and the order that normalization would give them without the ",
            _cgj(),
            ".",
        ),
        author.heading_level_3("Jerusalem"),
        _p(
            f"{_num(n_j_hiriq + n_j_sheva)} are in atoms spelled ",
            _he("ירושלם"),
            f" ({_num(n_j_hiriq)}) or ",
            _he("ירושלמה"),
            f" ({_num(n_j_sheva)}), with or without a prefix, on the $lamed. It has its own"
            " vowel, ",
            _uname(_PATAH),
            " or ",
            _uname(_QAMATS),
            f", then, in all but {_num(n_j_bare)} of them, an accent or ",
            _uname(hpo.MTGOSLQ),
            ", and after the ",
            _cgj(),
            " an orphaned ",
            _uname(_HIRIQ),
            " or ",
            _uname(_SHEVA),
            ", the vowel of the $yod that the spelling lacks:",
        ),
        _table(headers_j, _cgj_rows_jerusalem(s)),
        author.heading_level_3("Two strands on one letter"),
        _p(
            f"The other {_num(len(cgj['qupo']) + len(cgj['accent-meteg']))} are in verses with"
            " two cantillations, on a letter whose text represents both strands: the marks"
            " before the ",
            _cgj(),
            " are one strand's, and the marks after it are the other's. ",
            _code(f"{ms.FOLDER_AJF}/"),
            " has the strands too, with no ",
            _cgj(),
            " on that letter, which the tables show in the attention color. They give each"
            " atom's references in both folders, since the two"
            " numberings differ in the Decalogues. In"
            f" {_num(len(cgj['qupo']))} atoms, one strand has a ",
            _uname(_QAMATS),
            " and an accent or ",
            _uname(hpo.MTGOSLQ),
            " below the letter, and the other a ",
            _uname(_PATAH),
            " and an accent above it:",
        ),
        _table(headers_s, _cgj_rows_strands(s, "qupo")),
        _p(
            f"In {_num(len(cgj['accent-meteg']))} atoms, one strand has an accent below the"
            " letter, and the other a ",
            _uname(hpo.MTGOSLQ),
            ":",
        ),
        _table(headers_s, _cgj_rows_strands(s, "accent-meteg")),
    ]


def _guard_two_vowels(cbody, s) -> None:
    """Refuse a page with two vowels on one letter, but where the files have them."""
    allowed = {
        hit["cluster"]
        for kind in ("jerusalem-hiriq", "jerusalem-sheva", "qupo")
        for hit in s.cgj[kind]
    }

    def strings(node):
        if isinstance(node, str):
            yield node
        elif isinstance(node, (list, tuple)):
            for item in node:
                yield from strings(item)
        elif mb_html.is_htel(node):
            for value in (node.get("attr") or {}).values():
                yield value
            yield from strings(node.get("contents") or [])

    for text in strings(cbody):
        for cluster in ms.CLUSTER_RE.findall(text):
            if sum(1 for m in cluster if m in ms.VOWELS) > 1 and cluster not in allowed:
                raise ValueError(
                    f"two vowels on one letter, {cluster!r}, with no CGJ kind"
                )


def _pin_claims(s) -> None:
    """Fail the build if the data stops supporting a claim the prose states in words."""
    by = s.by_system
    # "ATNAH HAFUKH and GERESH MUQDAM are only in poetic verses, and GERESH only in prose."
    assert by[(ha.ATN_H, "prose")] == 0 and by[(ha.GER_M, "prose")] == 0
    assert by[(ha.GER, "poetic")] == 0
    # The table of marks by system lists PASEQ by markup; each PASEQ is one of the two.
    assert s.code_points_csv[hpu.PASOLEG] == s.spacing["legarmeh"] + s.spacing["paseq"]
    # "Each atom with a GERESH MUQDAM ... also has a REVIA" (counted per mark in the survey).
    assert s.zarqa["geresh muqdam with revia"] == s.code_points_csv[ha.GER_M]
    # "Every reference of csv/ is also in csv-ajf/."
    assert not s.refs_only_csv
    # "In both folders, each of these rows has only an EM DASH": the same two references.
    assert s.em_dash_csv == s.em_dash_ajf and s.em_dash_csv
    # "Each of the ZINOR marks is on the last letter of its atom": the survey raises otherwise,
    # and here every ZINOR is one of the counted ones.
    assert (
        s.code_points_csv[ha.Z_OR_TSOR]
        == s.zarqa["z-or-tsor prose"] + s.zarqa["z-or-tsor poetic"]
    )
    assert by[(ha.ZSH_OR_TSIT, "prose")] == s.zarqa["zsh-or-tsit prose"]
    # "the qere first in N pairs, M of them right after a maqaf": a part, not the whole.
    qere_first = sum(n for k, n in s.kq_shapes.items() if k[0] == "qere first")
    assert 0 < s.kq_qere_first_after_maqaf < qere_first
    # "The handlers ... write nothing for these three things."
    left_out = ms.check_handlers()
    assert set(left_out) == {"sdt-note", "good-ending", "cant-alef", "cant-bet"}
    # The listings section says each listing lists a verse of its CSV folder.
    assert s.listings["csv verses"] == len(s.verses)
    assert s.listings["ajf verses"] == len(s.ajf_rows)


def gen_html_file():
    """Write the page and its font, and return the page's path."""
    s = ms.survey()
    _pin_claims(s)
    out_dir = paths.gh_pages_dir() / "MAM-for-Sefaria"
    report_stylesheet.copy_report_font(out_dir)
    cbody = [
        author.heading_level_1(_TITLE.replace("MAM", "$MAM")),
        mb_html.para(_AUTHOR),
        mb_html.para(_REVISION),
        *_intro(),
        *_files(s),
        *_markup(s),
        *_characters(s),
        *_left_out(s),
        *_robust_unicode(s),
    ]
    _guard_two_vowels(cbody, s)
    author.help_gen_html_file(
        __file__, (str(out_dir), _CSS_HREFS), _FNAME, _TITLE, cbody, viewport=True
    )
    return out_dir / _FNAME
