"""Text-fragment links from the morphhb-corrections page into Ben's review of the Israel Bible.

Written as an untracked scratch script on 2026-11-14, and tracked since 2026-11-15.  For
each of the review's 56 rows of forms it computes a URL fragment in the syntax of WICG's
"URL Fragment Text Directives",

    #:~:text=[prefix-,]textStart,-suffix

whose match is the row's Where cell: textStart is the verse as that cell writes it, with its
no-break space, and suffix is the cell's "page N".  A prefix, the Israel Bible's form as the
row's first form cell shows it, is added only where the first match would otherwise not be
this row.  Every fragment is checked by simulating the spec's find algorithm on the generated
page (find_directive): its FIRST match in document order must be the row's own Where cell in
each model of build_models, or the script raises.  It also lists the review's footnotes, each
with its anchor and every verse that its text names.

write_links, which morphhb_corrections_index.gen_html_file calls before it builds the page,
reads the generated page, gh-pages/israel-bible-review/index.html, and the review's inputs
through the page's own generator, py/author_misc/israel_bible_review_index.py, and writes
review-links.json and review-links-check.txt into out/morphhb-corrections/.  Every href is
relative to the morphhb-corrections page, gh-pages/morphhb-corrections/index.html.  Every
Hebrew string that it writes is copied by code from the page or from the generator's data;
this file holds no Hebrew and is pure ASCII, which write_links checks.
"""

import bisect
import json
import re
import unicodedata
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote_to_bytes

from author_misc import israel_bible_review_index as ib
from mb_cmn import paths

SCRIPT = Path(__file__).resolve()
ROOT = paths.repo_root()
# The folder of the page whose links these are, and the tracked, unpublished folder of their
# table.
WORK_DIR = paths.gh_pages_dir() / "morphhb-corrections"
OUT_DIR = paths.out_dir() / "morphhb-corrections"

PAGE_REL = "gh-pages/israel-bible-review/index.html"
PAGE = ROOT / PAGE_REL
# Every href is relative to the page in WORK_DIR.
HREF_BASE = "../israel-bible-review/index.html"
NBSP = "\N{NO-BREAK SPACE}"
MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
DECALOGUES = "The Decalogues"
CHECK = "first match is this row"
# Each short book name of the module's SHORT, with its full name.
LONG = {short: full for full, short in ib.SHORT.items()}
assert len(LONG) == len(ib.SHORT)


def plain(s):
    """A cell's verse with plain spaces, for the check's lines."""
    return s.replace(NBSP, " ")


# ---------------------------------------------------------------- the rows, from the module


def md_row(verse, page, ib_form, mam_form):
    """A row of one of review.md's two data tables, its forms as the module shows them
    (data_items passes stripped() of each to units)."""
    m = re.fullmatch(r"(.+) (\d+):(\d+)", verse)
    if not (m and m.group(1) in LONG):
        raise ValueError(f"a verse of review.md that SHORT cannot lengthen: {verse!r}")
    if not re.fullmatch(r"[1-9]\d*", page):
        raise ValueError(f"{verse}: a page that is no page number: {page!r}")
    return dict(
        reference=verse,
        verse=[LONG[m.group(1)], int(m.group(2)), int(m.group(3))],
        # The Where cell's verse, as data_items writes it.
        cell=verse.replace(" ", NBSP),
        page=int(page),
        ib=ib.stripped(ib_form),
        mam=ib.stripped(mam_form),
        label=None,
    )


def module_rows(lines):
    """The review's rows of forms in the page's order, from the module's own data and
    functions: the tour's divisions, as tour_items and tour_divisions order them, then the
    Decalogues' table, which decalogue_table draws in review.md's order.  Also the counts of
    forms.json's rows and of review.md's two tables' rows."""
    json_rows = ib.forms()
    # The tour's rows by their verse with plain spaces: tour_items gives forms.json's verses
    # with no-break spaces (short_ref) but review.md's with plain ones (data_items).
    by_verse = {}

    def add(row):
        if plain(row["cell"]) in by_verse:
            raise ValueError(f"two tour rows with one Where cell: {row['cell']!r}")
        by_verse[plain(row["cell"])] = row

    for r in json_rows:
        book, chapter, verse = ib.bcv(r["reference"])
        add(
            dict(
                reference=r["reference"],
                verse=[book, chapter, verse],
                cell=ib.short_ref(r["reference"]),
                page=r["page"],
                ib=r["israel_bible"],
                mam=r["mam"],
                label=r.get("label"),
            )
        )
    tour_md = ib.data_table_rows(lines, ib.TOUR_ROW_HEADERS)
    for verse, page, ib_form, mam_form, _note in tour_md:
        add(md_row(verse, page, ib_form, mam_form))
    rows = []
    for heading, items in ib.tour_divisions(ib.tour_items(json_rows, lines)):
        for item in items:
            for verse in item[2].split(", "):
                row = by_verse.pop(plain(verse))
                rows.append(dict(row, table="tour", division=heading))
    if by_verse:
        raise ValueError(f"tour rows in no division: {sorted(by_verse)}")
    decalogue = ib.data_table_rows(lines, ib.DECALOGUE_ROW_HEADERS)
    for verse, page, ib_form, mam_form, _note in decalogue:
        rows.append(
            dict(
                md_row(verse, page, ib_form, mam_form),
                table="decalogue",
                division=DECALOGUES,
            )
        )
    counts = (len(json_rows), len(tour_md), len(decalogue))
    if len(rows) != sum(counts):
        raise ValueError(f"{len(rows)} rows, not {sum(counts)}")
    return rows, counts


def is_hebrew_letter(ch):
    return "\N{HEBREW LETTER ALEF}" <= ch <= "\N{HEBREW LETTER TAV}"


def letters_of(form, where):
    """The Hebrew letters of a shown form, final forms kept.  Closed dispatch: a character
    other than a letter, a Hebrew point, a maqaf or a space raises."""
    for ch in form:
        is_mark = (
            "\N{HEBREW ACCENT ETNAHTA}" <= ch <= "\N{HEBREW POINT QAMATS QATAN}"
            and unicodedata.category(ch) == "Mn"
        )
        if not (is_hebrew_letter(ch) or is_mark or ch in (MAQAF, " ")):
            name = unicodedata.name(ch, f"U+{ord(ch):04X}")
            raise ValueError(f"{where}: an unexpected character in a form: {name}")
    return "".join(ch for ch in form if is_hebrew_letter(ch))


# ---------------------------------------------------------------- the page

# Elements whose computed display is block-level in Chrome's sense: each starts its own run of
# text (an inline formatting context), so a term cannot match across its start or end.  Table
# cells are their own block flows in Chrome's find buffer, as each <li> and <summary> is.
BLOCK_TAGS = frozenset(
    "html body h1 h2 h3 h4 h5 h6 p ul ol li table thead tbody tfoot tr th td"
    " details summary section div blockquote".split()
)
INLINE_TAGS = frozenset("span a abbr i b em strong code cite bdi sub sup small".split())
HEADINGS = ("h1", "h2", "h3")


@dataclass
class Element:
    index: int
    tag: str
    attrs: dict
    heading: (
        tuple  # the last h1, h2 or h3 closed before this element starts: (tag, text)
    )
    text: list = field(default_factory=list)  # the data of every text node within it
    events: list = field(default_factory=list)  # its child text nodes' ids, and "br"
    cells: list = field(default_factory=list)  # a <tr>'s cells, as element indices
    tr: int = -1  # a cell's <tr>, as an element index

    def classes(self):
        return frozenset(self.attrs.get("class", "").split())


@dataclass
class TextNode:
    id: int
    data: str
    block: int  # text nodes with one block number are one block's text, in the spec's sense
    ancestors: tuple  # the indices of the elements that hold it, outermost first
    hidden: bool = False  # within a closed <details> but not within its <summary>


class PageParser(HTMLParser):
    """The page as its text nodes in document order, each with its block, for find_directive,
    and as its elements, for finding the rows.  <head> is not rendered; attribute values are
    not text.  Closed dispatch: a tag that the tables above do not name, an end tag that does
    not close the open element, or text outside the elements raises."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.nodes = []
        self.stack = []
        self.block = 0
        self.ids = {}
        self.trs = []
        self.last_heading = None
        self.in_head = False
        self.text_open = False

    def push(self, tag, attrs):
        e = Element(len(self.elements), tag, attrs, self.last_heading)
        self.elements.append(e)
        self.stack.append(e.index)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise ValueError(f"two elements with id {attrs['id']!r}")
            self.ids[attrs["id"]] = e.index
        return e

    def handle_decl(self, decl):
        if decl.lower() != "doctype html":
            raise ValueError(f"an unexpected declaration: {decl!r}")
        self.text_open = False

    def unknown_decl(self, data):
        raise ValueError(f"an unexpected declaration: {data!r}")

    def handle_pi(self, data):
        raise ValueError(f"an unexpected processing instruction: {data!r}")

    def handle_comment(self, data):
        self.text_open = False

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in ("meta", "link", "br", "img"):
            self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs):
        self.text_open = False
        a = dict(attrs)
        if len(a) != len(attrs):
            raise ValueError(f"<{tag}> repeats an attribute")
        if self.in_head:
            if tag == "title":
                self.push(tag, a)
            elif tag not in ("meta", "link"):
                raise ValueError(f"<{tag}> in <head>")
            return
        if tag == "head":
            self.in_head = True
            self.push(tag, a)
            return
        if tag in ("br", "img") and "id" in a:
            raise ValueError(f"<{tag}> with an id")
        if tag == "br":
            # Not a block boundary: the advance over white space skips it as a non-text node.
            self.elements[self.stack[-1]].events.append("br")
            return
        if tag == "img":
            # The page's one image, img.crop, is display: block in the page's style.css.
            if a.get("class") != "crop":
                raise ValueError(f"an <img> this script does not know: {a}")
            self.block += 1
            return
        if tag in BLOCK_TAGS:
            self.block += 1
        elif tag not in INLINE_TAGS:
            raise ValueError(f"a tag this script does not know: <{tag}>")
        tr = None
        if tag in ("td", "th"):
            trs = [k for k in self.stack if self.elements[k].tag == "tr"]
            if not trs:
                raise ValueError(f"<{tag}> outside a <tr>")
            tr = self.elements[trs[-1]]
        e = self.push(tag, a)
        if tr is not None:
            tr.cells.append(e.index)
            e.tr = tr.index
        if tag == "tr":
            self.trs.append(e.index)

    def handle_endtag(self, tag):
        self.text_open = False
        if not self.stack or self.elements[self.stack[-1]].tag != tag:
            raise ValueError(f"</{tag}> closes no open <{tag}>")
        e = self.elements[self.stack.pop()]
        if tag == "head":
            self.in_head = False
        elif self.in_head:
            return
        elif tag in BLOCK_TAGS:
            self.block += 1
        if tag in HEADINGS:
            self.last_heading = (tag, "".join(e.text))

    def handle_data(self, data):
        if self.in_head:
            return
        if not self.stack:
            if data.strip():
                raise ValueError(f"text outside the elements: {data!r}")
            return
        if self.text_open:
            node = self.nodes[-1]
            node.data += data
        else:
            node = TextNode(len(self.nodes), data, self.block, tuple(self.stack))
            self.nodes.append(node)
            self.elements[self.stack[-1]].events.append(node.id)
            self.text_open = True
        for k in node.ancestors:
            self.elements[k].text.append(data)


def parse_page():
    parser = PageParser()
    parser.feed(PAGE.read_text(encoding="utf-8"))
    parser.close()
    if parser.stack:
        raise ValueError("elements left open at the end of the page")
    for node in parser.nodes:
        chain = [parser.elements[k] for k in node.ancestors]
        node.hidden = any(
            e.tag == "details"
            and "open" not in e.attrs
            and (j + 1 == len(chain) or chain[j + 1].tag != "summary")
            for j, e in enumerate(chain)
        )
    return parser


@dataclass
class PageRow:
    where: Element
    verse_node: TextNode
    page_node: TextNode
    ib_nodes: list
    ib_text: str
    mam_text: str


def page_rows(parser):
    """The page's rows of forms in document order, each found by its Where cell,
    <td class="bcv first">, which holds the verse, a <br> and "page N", and stands between
    the first <tr>'s form cell, the Israel Bible's, and its note, if any; MAM's form is the
    next <tr>'s one cell."""
    by_cell = {}
    for node in parser.nodes:
        for k in reversed(node.ancestors):
            if parser.elements[k].tag in ("td", "th"):
                by_cell.setdefault(k, []).append(node)
                break
    rows = []
    for e in parser.elements:
        if e.tag != "td" or "bcv" not in e.classes():
            continue
        if e.classes() != {"bcv", "first"}:
            raise ValueError(f"a Where cell with classes {sorted(e.classes())}")
        ev = e.events
        if not (len(ev) == 3 and ev[1] == "br" and isinstance(ev[0], int)):
            raise ValueError(f"a Where cell that is not verse, <br>, page: {ev}")
        verse_node, page_node = parser.nodes[ev[0]], parser.nodes[ev[2]]
        if by_cell[e.index] != [verse_node, page_node]:
            raise ValueError(f"a Where cell with other text: {ascii(e.text)}")
        tr = parser.elements[e.tr]
        if len(tr.cells) < 2 or tr.cells[1] != e.index:
            raise ValueError(
                f"a Where cell that is not its row's second cell: {e.text}"
            )
        ib_cell = parser.elements[tr.cells[0]]
        next_tr = parser.elements[parser.trs[parser.trs.index(tr.index) + 1]]
        if len(next_tr.cells) != 1:
            raise ValueError(
                f"MAM's <tr> after {e.text} has {len(next_tr.cells)} cells"
            )
        mam_cell = parser.elements[next_tr.cells[0]]
        for cell, classes in ((ib_cell, {"form", "first"}), (mam_cell, {"form"})):
            if cell.classes() != classes or cell.attrs.get("dir") != "rtl":
                raise ValueError(f"a form cell with {cell.attrs} beside {e.text}")
        ib_nodes = by_cell[ib_cell.index]
        rows.append(
            PageRow(
                e,
                verse_node,
                page_node,
                ib_nodes,
                "".join(n.data for n in ib_nodes),
                "".join(n.data for n in by_cell[mam_cell.index]),
            )
        )
    return rows


# ---------------------------------------------------------------- the spec's algorithm

# The White_Space property, which the spec's advance over white space skips.
WHITE_SPACE = frozenset(
    "\t\n\v\f\r \x85"
    "\N{NO-BREAK SPACE}\N{OGHAM SPACE MARK}\N{EN QUAD}\N{EM QUAD}\N{EN SPACE}\N{EM SPACE}"
    "\N{THREE-PER-EM SPACE}\N{FOUR-PER-EM SPACE}\N{SIX-PER-EM SPACE}\N{FIGURE SPACE}"
    "\N{PUNCTUATION SPACE}\N{THIN SPACE}\N{HAIR SPACE}\N{LINE SEPARATOR}"
    "\N{PARAGRAPH SEPARATOR}\N{NARROW NO-BREAK SPACE}\N{MEDIUM MATHEMATICAL SPACE}"
    "\N{IDEOGRAPHIC SPACE}"
)
# CSS's collapsible white space, which the rendered text that browsers search collapses.
COLLAPSIBLE = frozenset(" \t\n\r\f")
# Categories ignorable at the primary level of UTS #10: marks, Hebrew points among them, and
# format characters.
IGNORABLE = frozenset({"Mn", "Me", "Cf"})
FINALS = {
    "\N{HEBREW LETTER FINAL KAF}": "\N{HEBREW LETTER KAF}",
    "\N{HEBREW LETTER FINAL MEM}": "\N{HEBREW LETTER MEM}",
    "\N{HEBREW LETTER FINAL NUN}": "\N{HEBREW LETTER NUN}",
    "\N{HEBREW LETTER FINAL PE}": "\N{HEBREW LETTER PE}",
    "\N{HEBREW LETTER FINAL TSADI}": "\N{HEBREW LETTER TSADI}",
}


def fold_casefold(s):
    """Code points compared case-insensitively.  Returns the folded string and, for each of
    its characters, the index in s of the character it came from."""
    out, where = [], []
    for k, ch in enumerate(s):
        for c in ch.casefold():
            out.append(c)
            where.append(k)
    return "".join(out), where


def fold_primary(fold_finals):
    """The spec's comparison, "the primary level, as defined in [UTS10]", approximately:
    marks and format characters ignored, case ignored, every white space character equal to a
    space and each run of collapsible white space one space, as rendered; with fold_finals,
    each final letter equal to its non-final form too.  Folds as fold_casefold does."""

    def fold(s):
        out, where = [], []
        collapsing = False
        for k, ch in enumerate(s):
            if unicodedata.category(ch) in IGNORABLE:
                continue
            if ch in COLLAPSIBLE:
                if not collapsing:
                    out.append(" ")
                    where.append(k)
                collapsing = True
                continue
            collapsing = False
            if ch in WHITE_SPACE:
                ch = " "
            elif fold_finals:
                ch = FINALS.get(ch, ch)
            for c in ch.casefold():
                out.append(c)
                where.append(k)
        return "".join(out), where

    return fold


EXTEND_LIKE = frozenset({"Extend", "Format", "ZWJ"})
AHLETTER = frozenset({"ALetter", "Hebrew_Letter"})
MID_LETTER_Q = frozenset({"MidLetter", "MidNumLet", "Single_Quote"})
MID_NUM_Q = frozenset({"MidNum", "MidNumLet", "Single_Quote"})
NEWLINES = frozenset({"CR", "LF", "Newline"})
MIDLETTER = frozenset(
    ":\N{MIDDLE DOT}\N{HEBREW PUNCTUATION GERSHAYIM}\N{HYPHENATION POINT}"
    "\N{SMALL COLON}\N{FULLWIDTH COLON}"
)
MIDNUMLET = frozenset(
    ".\N{LEFT SINGLE QUOTATION MARK}\N{RIGHT SINGLE QUOTATION MARK}\N{ONE DOT LEADER}"
    "\N{SMALL FULL STOP}\N{FULLWIDTH APOSTROPHE}\N{FULLWIDTH FULL STOP}"
)
MIDNUM = frozenset(
    ",;\N{GREEK QUESTION MARK}\N{ARABIC COMMA}\N{FRACTION SLASH}\N{SMALL COMMA}"
    "\N{SMALL SEMICOLON}\N{FULLWIDTH COMMA}\N{FULLWIDTH SEMICOLON}"
)
NOT_WSEGSPACE = frozenset({NBSP, "\N{FIGURE SPACE}", "\N{NARROW NO-BREAK SPACE}"})


def wb_class(ch):
    """The character's Word_Break property (UAX #29), as far as this page needs it."""
    if ch == "\r":
        return "CR"
    if ch == "\n":
        return "LF"
    if ch in "\v\f\x85\N{LINE SEPARATOR}\N{PARAGRAPH SEPARATOR}":
        return "Newline"
    if ch == "\N{ZERO WIDTH JOINER}":
        return "ZWJ"
    cat = unicodedata.category(ch)
    if cat in ("Mn", "Me", "Mc"):
        return "Extend"
    if cat == "Cf":
        return "Format"
    if cat[0] == "L":
        hebrew = unicodedata.name(ch, "").startswith("HEBREW ")
        return "Hebrew_Letter" if hebrew else "ALetter"
    if cat == "Nd":
        return "Numeric"
    if ch == "'":
        return "Single_Quote"
    if ch == '"':
        return "Double_Quote"
    if ch in MIDNUMLET:
        return "MidNumLet"
    if ch in MIDLETTER:
        return "MidLetter"
    if ch in MIDNUM:
        return "MidNum"
    if cat == "Pc" or ch == "\N{NARROW NO-BREAK SPACE}":
        return "ExtendNumLet"
    if cat == "Zs" and ch not in NOT_WSEGSPACE:
        return "WSegSpace"
    return "Other"


def base_before(text, k):
    """The index of the last character at or before k that WB4 does not attach to the one
    before it, or -1."""
    while k >= 0 and wb_class(text[k]) in EXTEND_LIKE:
        k -= 1
    return k


def word_boundary(text, i):
    """Whether index i of text is a word boundary by UAX #29's default rules, WB1 to WB13b
    (the emoji, Katakana and regional-indicator rules are not needed here)."""
    if i <= 0 or i >= len(text):
        return True  # WB1, WB2
    a, b = wb_class(text[i - 1]), wb_class(text[i])
    if a == "CR" and b == "LF":
        return False  # WB3
    if a in NEWLINES or b in NEWLINES:
        return True  # WB3a, WB3b
    if a == "WSegSpace" and b == "WSegSpace":
        return False  # WB3d
    if b in EXTEND_LIKE:
        return False  # WB4
    ja = base_before(text, i - 1)
    a = wb_class(text[ja]) if ja >= 0 else None
    jz = base_before(text, ja - 1) if ja >= 0 else -1
    z = wb_class(text[jz]) if jz >= 0 else None
    jc = i + 1
    while jc < len(text) and wb_class(text[jc]) in EXTEND_LIKE:
        jc += 1
    c = wb_class(text[jc]) if jc < len(text) else None
    if a in AHLETTER and b in AHLETTER:
        return False  # WB5
    if a in AHLETTER and b in MID_LETTER_Q and c in AHLETTER:
        return False  # WB6
    if z in AHLETTER and a in MID_LETTER_Q and b in AHLETTER:
        return False  # WB7
    if a == "Hebrew_Letter" and b == "Single_Quote":
        return False  # WB7a
    if a == "Hebrew_Letter" and b == "Double_Quote" and c == "Hebrew_Letter":
        return False  # WB7b
    if z == "Hebrew_Letter" and a == "Double_Quote" and b == "Hebrew_Letter":
        return False  # WB7c
    if a == "Numeric" and b == "Numeric":
        return False  # WB8
    if a in AHLETTER and b == "Numeric":
        return False  # WB9
    if a == "Numeric" and b in AHLETTER:
        return False  # WB10
    if z == "Numeric" and a in MID_NUM_Q and b == "Numeric":
        return False  # WB11
    if a == "Numeric" and b in MID_NUM_Q and c == "Numeric":
        return False  # WB12
    if a in AHLETTER | {"Numeric", "ExtendNumLet"} and b == "ExtendNumLet":
        return False  # WB13a
    if a == "ExtendNumLet" and b in AHLETTER | {"Numeric"}:
        return False  # WB13b
    return True  # WB999


class Model:
    """The page's visible text nodes under one model of comparison.  A boundary point is
    (index into nodes, offset); the document's end is (len(nodes), 0)."""

    def __init__(self, name, nodes, fold, extend):
        self.name = name
        self.nodes = nodes
        self.fold = fold
        # Whether a match extends over the ignorable marks after its last character.
        self.extend = extend
        self.end = (len(nodes), 0)
        # The index of the first node after each node's block.
        self.block_end = [0] * len(nodes)
        for i in range(len(nodes) - 1, -1, -1):
            same = i + 1 < len(nodes) and nodes[i + 1].block == nodes[i].block
            self.block_end[i] = self.block_end[i + 1] if same else i + 1
        self._buffers = {}

    def buffer(self, i):
        """The spec's search buffer from node i to the end of its block, folded."""
        if i not in self._buffers:
            datas = [n.data for n in self.nodes[i : self.block_end[i]]]
            buf = "".join(datas)
            self._buffers[i] = (datas, buf, *self.fold(buf))
        return self._buffers[i]

    def at(self, point):
        """A boundary point as (text node id, offset), or None at the document's end."""
        i, offset = point
        return (self.nodes[i].id, offset) if i < len(self.nodes) else None


def boundary_point(i0, datas, index, is_end):
    """The spec's "get boundary point at index", over the nodes from i0 whose data are datas."""
    counted = 0
    for j, d in enumerate(datas):
        if counted + len(d) + (1 if is_end else 0) > index:
            return (i0 + j, index - counted)
        counted += len(d)
    raise AssertionError((index, is_end))


def find_string(model, query, start, word_start, word_end):
    """The spec's "find a string in range" from boundary point start to the document's end:
    block by block, the first instance of query that is word-start-bounded and
    word-end-bounded as asked, as (start, end) boundary points, or None."""
    fq = model.fold(query)[0]
    if not fq:
        raise ValueError(f"a term with nothing to compare in {model.name}: {query!r}")
    i, offset = start
    while i < len(model.nodes):
        datas, buf, folded, where = model.buffer(i)
        k = bisect.bisect_left(where, offset)
        while (k := folded.find(fq, k)) >= 0:
            s, e = where[k], where[k + len(fq) - 1] + 1
            if model.extend:
                while e < len(buf) and unicodedata.category(buf[e]) in IGNORABLE:
                    e += 1
            if (word_start and not word_boundary(buf, s)) or (
                word_end and not word_boundary(buf, e)
            ):
                k += 1
                continue
            return boundary_point(i, datas, s, False), boundary_point(i, datas, e, True)
        i, offset = model.block_end[i], 0
    return None


def advance(model, point):
    """The spec's "advance a range's start to the next non-whitespace position": across node
    and block boundaries, past every non-text node and white space character."""
    i, offset = point
    while i < len(model.nodes):
        data = model.nodes[i].data
        if offset >= len(data):
            i, offset = i + 1, 0
        elif data.startswith("&nbsp;", offset):
            offset += 6
        elif data.startswith("&nbsp", offset):
            offset += 5
        elif data[offset] not in WHITE_SPACE:
            return (i, offset)
        else:
            offset += 1
    return model.end


def find_directive(model, prefix, start, suffix):
    """The spec's "find a range from a text directive", for a directive with no textEnd: its
    FIRST match in document order, as a dict of the ranges of its textStart, its prefix and
    its suffix, or None."""
    search = (0, 0)
    while search < model.end:
        prefix_match = None
        if prefix is not None:
            prefix_match = find_string(model, prefix, search, True, False)
            if prefix_match is None:
                return None
            search = (prefix_match[0][0], prefix_match[0][1] + 1)
            match_start = advance(model, prefix_match[1])
            if match_start == model.end:
                return None
            potential = find_string(model, start, match_start, False, suffix is None)
            if potential is None:
                return None
            if potential[0] != match_start:
                continue
        else:
            potential = find_string(model, start, search, True, suffix is None)
            if potential is None:
                return None
            search = (potential[0][0], potential[0][1] + 1)
        if suffix is None:
            return dict(start=potential, prefix=prefix_match, suffix=None)
        suffix_start = advance(model, potential[1])
        suffix_match = find_string(model, suffix, suffix_start, False, True)
        if suffix_match is None:
            return None
        if suffix_match[0] == suffix_start:
            return dict(start=potential, prefix=prefix_match, suffix=suffix_match)
        # No textEnd: try the next instance of the prefix or textStart.
    return None


def build_models(nodes):
    """The models of comparison that every fragment is checked in.  The brief's is the
    first: code points compared case-insensitively.  The spec compares at UTS #10's primary
    level, which ignores Hebrew points, so the Israel Bible's form and MAM's are one prefix
    there wherever their letters agree; whether a final letter is primary-equal to its
    non-final form is not settled here, so both are tried.  Chrome searches the text of a
    closed <details> and opens it; a browser that skips such text is modeled too."""
    shown = [n for n in nodes if not n.hidden]
    out = []
    for name, fold, extend in (
        ("code points compared case-insensitively", fold_casefold, False),
        (
            "primary level (marks, format characters and case ignored, a no-break space"
            " equal to a space, white space collapsed as rendered), final letters distinct",
            fold_primary(False),
            True,
        ),
        (
            "primary level as above, each final letter equal to its non-final form",
            fold_primary(True),
            True,
        ),
    ):
        out.append(Model(f"{name}; closed <details> searched", nodes, fold, extend))
        out.append(Model(f"{name}; closed <details> skipped", shown, fold, extend))
    return out


# ---------------------------------------------------------------- fragments


def encode_term(s):
    """A term percent-encoded: every byte of its UTF-8 but ASCII letters and digits, so that
    "-", ",", "&", a space and a no-break space are all encoded."""
    return "".join(
        chr(b) if chr(b).isascii() and chr(b).isalnum() else f"%{b:02X}"
        for b in s.encode("utf-8")
    )


def fragment(prefix, start, suffix):
    terms = [encode_term(start), "-" + encode_term(suffix)]
    if prefix is not None:
        terms.insert(0, encode_term(prefix) + "-")
    return "#:~:text=" + ",".join(terms)


def decode_term(term):
    return unquote_to_bytes(term).decode("utf-8")


def parse_fragment(frag):
    """The fragment's one text directive, parsed as the spec parses one: (prefix, textStart,
    textEnd, suffix), each percent-decoded, or a raise."""
    head = "#:~:text="
    if not frag.startswith(head) or "&" in frag:
        raise ValueError(f"not one text directive: {frag!r}")
    tokens = frag[len(head) :].split(",")
    if not 1 <= len(tokens) <= 4 or "" in tokens:
        raise ValueError(f"a malformed text directive: {frag!r}")
    prefix = suffix = end = None
    if tokens[0].endswith("-"):
        prefix = decode_term(tokens.pop(0)[:-1])
    if tokens and tokens[-1].startswith("-"):
        suffix = decode_term(tokens.pop()[1:])
    if len(tokens) not in (1, 2):
        raise ValueError(f"a malformed text directive: {frag!r}")
    start = decode_term(tokens[0])
    if len(tokens) == 2:
        end = decode_term(tokens[1])
    return prefix, start, end, suffix


def outcome(model, found, row, rows):
    """(True, CHECK) if found, find_directive's match, is row's Where cell, its suffix the
    cell's page and its prefix, if any, the row's Israel Bible form; else (False, what the
    match is)."""
    if found is None:
        return False, "no match"
    start, end = found["start"]
    v = row.verse_node
    if model.at(start) == (v.id, 0) and model.at(end) == (v.id, len(v.data)):
        p = row.page_node
        sx = found["suffix"]
        assert (model.at(sx[0]), model.at(sx[1])) == ((p.id, 0), (p.id, len(p.data)))
        if found["prefix"] is not None:
            first, last = row.ib_nodes[0], row.ib_nodes[-1]
            px = found["prefix"]
            assert (model.at(px[0]), model.at(px[1])) == (
                (first.id, 0),
                (last.id, len(last.data)),
            )
        return True, CHECK
    node = model.nodes[start[0]]
    for k, other in enumerate(rows, 1):
        if other.verse_node.id == node.id:
            where = f"{plain(other.verse_node.data)}, {other.page_node.data}"
            return False, f"the first match is row {k} ({where})"
    return False, f"the first match is in {node.data[start[1] : start[1] + 40]!r}"


def checked(models, prefix, start, suffix, row, rows):
    """A fragment and its outcome in each model, the fragment parsed back as a browser would
    parse it."""
    frag = fragment(prefix, start, suffix)
    terms = parse_fragment(frag)
    if terms != (prefix, start, None, suffix):
        raise ValueError(f"a fragment that does not parse back: {frag}")
    p, s, _end, x = terms
    return frag, [outcome(m, find_directive(m, p, s, x), row, rows) for m in models]


def tally(outcomes, n):
    """Each distinct outcome with the number of models that gave it."""
    texts = [text for _ok, text in outcomes]
    return "; ".join(
        f"{t} in {texts.count(t)} of {n} models" for t in dict.fromkeys(texts)
    )


# ---------------------------------------------------------------- footnotes

VERSE_REF = re.compile(r"(?<![\d:])(\d+):(\d+)(?![\d:])")
BOOK_NAMES = sorted(set(ib.SHORT) | set(LONG), key=len, reverse=True)
MD_LINK = re.compile(r"!?\[([^\]]+)\]\(([^)\s]+)\)")


def verse_refs(text, where):
    """Every verse that text names, as [full book name, chapter, verse], in order.  Closed
    dispatch: a chapter:verse whose book is neither a full nor a short name of SHORT raises.
    """
    out = []
    for m in VERSE_REF.finditer(text):
        before = text[: m.start()]
        for name in BOOK_NAMES:
            if re.search(rf"(?<!\w){re.escape(name)}[ {NBSP}]\Z", before):
                full = name if name in ib.SHORT else LONG[name]
                out.append([full, int(m.group(1)), int(m.group(2))])
                break
        else:
            context = text[max(0, m.start() - 24) : m.end()]
            raise ValueError(
                f"{where}: a verse whose book is not recognized: {context!r}"
            )
    return out


def footnote_defs(lines):
    """review.md's footnotes as [(label, text)], each note's paragraphs and list items joined
    into one text; read as the module's review_html reads them: a line "[^label]: text",
    continued by lines indented four spaces, and after a blank line by a further paragraph or
    list (FOOTNOTE_DEF, NOTE_LIST_ITEM, NOTE_LIST_MORE)."""
    defs = []
    k = 0
    while k < len(lines):
        fd = ib.FOOTNOTE_DEF.fullmatch(lines[k])
        k += 1
        if not fd:
            continue
        label, text = fd.groups()
        paras = [text]
        while k < len(lines):
            ln = lines[k]
            if ln.startswith(ib.NOTE_LIST_ITEM) and isinstance(paras[-1], list):
                paras[-1].append(ln[len(ib.NOTE_LIST_ITEM) :])
                k += 1
            elif (
                ln.startswith(ib.NOTE_LIST_MORE)
                and ln.strip()
                and isinstance(paras[-1], list)
            ):
                paras[-1][-1] += " " + ln.strip()
                k += 1
            elif ln.startswith("    ") and ln.strip():
                if not isinstance(paras[-1], str) or ln.startswith(ib.NOTE_LIST_ITEM):
                    raise ValueError(f"[^{label}]: text against a list: {ln!r}")
                paras[-1] += " " + ln.strip()
                k += 1
            elif (
                not ln.strip()
                and k + 1 < len(lines)
                and lines[k + 1].startswith("    ")
                and lines[k + 1].strip()
            ):
                nxt = lines[k + 1]
                if nxt.startswith(ib.NOTE_LIST_ITEM):
                    paras.append([nxt[len(ib.NOTE_LIST_ITEM) :]])
                else:
                    paras.append(nxt.strip())
                k += 2
            else:
                break
        joined = " ".join(p if isinstance(p, str) else " ".join(p) for p in paras)
        if ib.FOOTNOTE_REF.search(joined):
            raise ValueError(f"[^{label}]: a note within a note")
        defs.append((label, joined))
    labels = [label for label, _text in defs]
    if len(labels) != len(set(labels)):
        raise ValueError(f"a footnote defined twice: {sorted(labels)}")
    return defs


def footnotes(lines, parser):
    """Each footnote, in the page's numbering: its label, number, anchor, href and verses.
    Its verses are read from review.md and, as a differential check, from the page's note.
    """
    on_page = {
        e.attrs["id"][len("fn-") :]: e
        for e in parser.elements
        if e.tag == "li" and e.attrs.get("id", "").startswith("fn-")
    }
    defs = footnote_defs(lines)
    if sorted(on_page) != sorted(label for label, _text in defs):
        raise ValueError(f"the page's notes {sorted(on_page)} are not review.md's")
    out = []
    for label, text in defs:
        anchor = f"fn-{label}"
        if anchor not in parser.ids:
            raise ValueError(f"the page has no element with id {anchor!r}")
        if f"fnref-{label}" not in parser.ids:
            raise ValueError(f"the page has no reference to {anchor!r}")
        ref_text = "".join(parser.elements[parser.ids[f"fnref-{label}"]].text)
        m = re.fullmatch(r"\[([1-9]\d*)\]", ref_text)
        if not m:
            raise ValueError(
                f"{anchor}: a reference that is not a number: {ref_text!r}"
            )
        verses = verse_refs(MD_LINK.sub(r"\1", text), f"review.md's [^{label}]")
        page_verses = verse_refs("".join(on_page[label].text), f"the page's {anchor}")
        if verses != page_verses:
            raise ValueError(
                f"{anchor}: review.md names {verses}, the page {page_verses}"
            )
        out.append(
            dict(
                label=label,
                number=int(m.group(1)),
                anchor=anchor,
                href=f"{HREF_BASE}#{anchor}",
                verses=verses,
            )
        )
    out.sort(key=lambda note: note["number"])
    if [note["number"] for note in out] != list(range(1, len(out) + 1)):
        raise ValueError("the notes are not numbered 1 to n")
    return out


# ---------------------------------------------------------------- write_links


def write_links():
    """Write review-links.json and review-links-check.txt into OUT_DIR, raising if a check
    fails."""
    if not SCRIPT.read_text(encoding="utf-8").isascii():
        raise ValueError("this module holds a character that is not ASCII")
    if (WORK_DIR / HREF_BASE).resolve() != PAGE.resolve():
        raise ValueError(f"{HREF_BASE} does not reach the page from {WORK_DIR}")

    lines = ib.review_lines()
    expected, counts = module_rows(lines)
    parser = parse_page()
    rows = page_rows(parser)
    if len(rows) != len(expected):
        raise ValueError(f"the page has {len(rows)} rows, the module {len(expected)}")
    for k, (exp, row) in enumerate(zip(expected, rows), 1):
        heading = (
            ("h3", exp["division"]) if exp["table"] == "tour" else ("h2", DECALOGUES)
        )
        want = (exp["cell"], f"page {exp['page']}", exp["ib"], exp["mam"], heading)
        got = (
            row.verse_node.data,
            row.page_node.data,
            row.ib_text,
            row.mam_text,
            row.where.heading,
        )
        if got != want:
            raise ValueError(f"row {k}: the page has {got!r}, the module {want!r}")

    models = build_models(parser.nodes)
    n = len(models)
    out_rows, check_lines, prefixed = [], [], []
    for k, (exp, row) in enumerate(zip(expected, rows), 1):
        start, suffix = row.verse_node.data, row.page_node.data
        frag, outcomes = checked(models, None, start, suffix, row, rows)
        reason = None
        if not all(ok for ok, _text in outcomes):
            reason = tally(outcomes, n)
            frag, outcomes = checked(models, row.ib_text, start, suffix, row, rows)
            if not all(ok for ok, _text in outcomes):
                raise ValueError(
                    f"row {k} ({plain(start)}, {suffix}): with a prefix, "
                    f"{tally(outcomes, n)}; without one, {reason}"
                )
            prefixed.append((k, exp, reason))
        out_rows.append(
            dict(
                reference=exp["reference"],
                verse=exp["verse"],
                cell=exp["cell"],
                page=exp["page"],
                table=exp["table"],
                division=exp["division"],
                ib=exp["ib"],
                mam=exp["mam"],
                letters=letters_of(exp["ib"], exp["reference"]),
                label=exp["label"],
                fragment=frag,
                href=HREF_BASE + frag,
                prefix_used=reason is not None,
                check=CHECK,
            )
        )
        letters_of(exp["mam"], exp["reference"])
        line = (
            f"{k:2}. {plain(start):12} {suffix:10} prefix {'yes' if reason else 'no '}"
            f"  {frag}  {tally(outcomes, n)}"
        )
        if reason:
            line += f"; without a prefix, {reason}"
        check_lines.append(line)

    notes = footnotes(lines, parser)
    doc = dict(
        review_page=PAGE_REL,
        hrefs_relative_to=WORK_DIR.relative_to(ROOT).as_posix() + "/",
        rows=out_rows,
        footnotes=notes,
    )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "review-links.json", "w", encoding="utf-8", newline="\n") as fp:
        fp.write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")

    n_forms, n_tour_md, n_decalogue = counts
    prefix_note = ", ".join(
        f"row {k}, {plain(exp['cell'])}, page {exp['page']}" for k, exp, _r in prefixed
    )
    report = [
        f"Text-fragment links into {PAGE_REL}",
        "",
        "Each row's fragment was checked by simulating, on the page, the find algorithm of",
        "WICG's URL Fragment Text Directives: its first match in document order must be the",
        "row's own Where cell, with its suffix that cell's page and its prefix, if any, the",
        "row's Israel Bible form, in each of these models:",
        *(f"  {j}. {m.name}" for j, m in enumerate(models, 1)),
        "",
        f"Rows, in the page's order ({n_forms} of forms.json, {n_tour_md} of review.md's"
        f" tour table, {n_decalogue} of its Decalogues' table):",
        *check_lines,
        "",
        f"{len(out_rows)} rows checked, {len(prefixed)} with a prefix"
        + (f" ({prefix_note})." if prefixed else "."),
        "",
        "Footnotes, in the page's numbering:",
    ]
    for note in notes:
        verses = ", ".join(f"{b} {c}:{v}" for b, c, v in note["verses"]) or "no verses"
        report.append(f"  {note['anchor']} (note {note['number']}): {verses}")
    with open(
        OUT_DIR / "review-links-check.txt", "w", encoding="utf-8", newline="\n"
    ) as fp:
        fp.write("\n".join(report) + "\n")
    print(
        f"{len(out_rows)} rows checked, {len(prefixed)} with a prefix; {len(notes)} notes"
    )
