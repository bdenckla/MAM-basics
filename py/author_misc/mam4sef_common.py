"""What the three pages that document MAM-for-Sefaria share.

``mam4sef_index.py`` writes ``gh-pages/MAM-for-Sefaria/index.html``, "The encoding of MAM for
Sefaria", on the folder ``csv/``.  ``mam4sef_unicode_names_index.py`` writes
``unicode-names/index.html`` beside it, on the listings of ``misc/unicode-names/``, and the
first page links to it.  ``mam4sef_ajf_index.py`` writes ``ajf/index.html``, on the AJF variant,
``csv-ajf/`` and ``misc/unicode-names-ajf/``, and no page of the documentation links to it.
That split is Ben's of 2026-10-26: "Relegate AJF documentation to its own page; don't even
link to it from MAM-for-Sefaria documentation", and the listings to a page of their own that
the first page does link to.

All three read ``mam4sef_survey.survey()`` and take their examples from it with the lookups
here: each must match exactly one place in the files, by a reference and the letters of its
atoms, so no pointed Hebrew on the pages is typed.  A reference is shown with its book's short
name, Gen 2:5 rather than Genesis 2:5, as Ben asked the same day, but where a page quotes what a
file has.

Only pointed Hebrew is in the Hebrew font: ``unpointed`` sets an unpointed form in prose,
``td_he`` leaves a lifted ketiv, break or inverted nun in the surrounding font, and
``write_page`` refuses a page with an unpointed Hebrew token under ``lang="hbo"``.
"""

import re

from mb_author import author
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import paths
from mb_cmn import str_defs as sd
from mb_cmn import unicode_data
from mb_misc import mb_html
from mb_misc import osis_book_abbrevs
from mb_misc import report_stylesheet
from mb_sefaria import sef_cmn
from author_misc import mam4sef_survey as ms

AUTHOR = "Author: Ben Denckla"
REVISION = "Revision: 2026-10-26"
OUT_DIR = "MAM-for-Sefaria"
INDEX_TITLE = "The encoding of MAM for Sefaria"
LISTINGS_TITLE = "The Unicode-name listings of MAM for Sefaria"
LISTINGS_DIR = "unicode-names"
AJF_TITLE = "The AJF variant of MAM for Sefaria"
AJF_DIR = "ajf"

GITHUB = "https://github.com/bdenckla/MAM-basics"
PRODUCT_URL = f"{GITHUB}/tree/main/MAM-for-Sefaria"
README_URL = f"{GITHUB}/blob/main/MAM-for-Sefaria/README.md"
HANDLERS_URL = f"{GITHUB}/blob/main/py/mb_sefaria/mam4sef_handlers.py"
AJF_HANDLERS_URL = f"{GITHUB}/blob/main/py/mb_sefaria/mam4ajf_handlers.py"
MARK_ORDER_URL = f"{GITHUB}/blob/main/doc/mam-normal-mark-order.md"

# A letter or a mark: what may not stand right before or after a matched form.
_EDGE = f"[א-ת{ms.MARK_CLASS[1:-1]}]"
# A token of Hebrew text, as a browser shapes it: letters, marks and the four Hebrew
# punctuation marks the files have, with nothing else between them.
_HEBREW_TOKEN_RE = re.compile(
    f"(?:[א-ת]|{ms.MARK_CLASS}"
    f"|[{re.escape(hpu.MAQ + hpu.PASOLEG + hpu.SOPA + hpu.NUN_HAF)}])+"
)
_MARK_RE = re.compile(ms.MARK_CLASS)
_BK39_OF_TITLE = {title: bk39id for bk39id, title in sef_cmn.SEF_BKNA.items()}


# SMALL HELPERS --------------------------------------------------------------------------------


def num(count: int) -> str:
    return f"{count:,}"


def p(*contents, attr=None):
    return author.para(list(contents), attr)


def code(text: str):
    return mb_html.code(text)


def unpointed(contents):
    """Unpointed Hebrew in prose: isolated for its direction, in the surrounding font.

    Only pointed Hebrew takes ``lang="hbo"``, whose stylesheet rule sets Taamey D at 140%.  Ben
    asked again on 2026-10-26 that "unpointed Hebrew words" not be put "in pointed-Hebrew
    styling", as ``accgram.almost_errors_html_shared.wrap_hebrew_runs`` already leaves them;
    ``write_page`` refuses a page that does.
    """
    return mb_html.bdi(contents)


def rom(text: str):
    """A romanized name with no ``$`` key in ``mb_author.author``."""
    return mb_html.span_c(text, "romanized")


def title_link(title: str, href: str):
    """A link to one of these pages, by its title as the page's heading shows it."""
    return mb_html.anchor_h(author.dollar_sub(title.replace("MAM", "$MAM")), href)


def uname(char: str, *, full: bool = False):
    """A code point's Unicode name in small capitals, the whole name on hover if shortened."""
    name = unicode_data.name(char)
    shown = name if full else ms.short_name(char)
    attr = {"class": "unicode-code-point-name"}
    if shown != name:
        attr["title"] = name
    return mb_html.span(shown, attr)


def cgj():
    return mb_html.span(
        "CGJ", {"class": "unicode-code-point-name", "title": unicode_data.name(sd.CGJ)}
    )


def join(items: list, last: str = "and") -> list:
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


def name_list(chars: str) -> list:
    """Code points by name, in order, separated by commas."""
    out = []
    for index, char in enumerate(chars):
        if index:
            out.append(", ")
        out.append(cgj() if char == sd.CGJ else uname(char))
    return out


def table(headers: list, rows: list, attr=None):
    head = mb_html.table_row(
        [mb_html.table_header(author.dollar_sub(h)) for h in headers]
    )
    table_attr = {"class": "data", **(attr or {})}
    return mb_html.div(
        [mb_html.table([head, *rows], table_attr)], {"class": "table-wrap"}
    )


def tr(cells: list):
    return mb_html.table_row(cells)


def td(contents, attr=None):
    return mb_html.table_datum(author.dollar_sub(contents), attr)


def td_he(contents):
    """A table cell of Hebrew: right to left, and in the Hebrew font where it is pointed.

    A form lifted from csv/ can hold elements whose text is unpointed, a ketiv, a break or an
    inverted nun; those stay in the surrounding font, as ``unpointed`` says, and the rest of
    the cell goes in ``lang="hbo"`` spans.
    """
    nodes = contents if isinstance(contents, list) else [contents]
    if not _has_unpointed(nodes):
        return mb_html.table_datum(nodes, {"lang": "hbo", "dir": "rtl"})
    return mb_html.table_datum(_hbo_groups(nodes), {"dir": "rtl"})


# The classes of the elements of csv/ whose text has no point or accent: a ketiv, the two
# breaks and the inverted nun.
_UNPOINTED_CLASSES = frozenset(
    ("mam-kq-k", "mam-spi-samekh", "mam-spi-pe", "mam-spi-invnun")
)


def _is_unpointed_el(node) -> bool:
    if not mb_html.is_htel(node):
        return False
    return (node.get("attr") or {}).get("class") in _UNPOINTED_CLASSES


def _has_unpointed(nodes: list) -> bool:
    return any(
        _is_unpointed_el(node)
        or (mb_html.is_htel(node) and _has_unpointed(node.get("contents") or []))
        for node in nodes
    )


def _hbo_groups(nodes: list) -> list:
    """``nodes`` with each run of pointed siblings in a ``lang="hbo"`` span.

    An unpointed element is left as it is, and an element that holds one is rebuilt with its
    children grouped the same way.  The spaces at either end of a run stay outside its span.
    """
    out, run = [], []

    def close():
        items = list(run)
        run.clear()
        if not items:
            return
        head = tail = ""
        if isinstance(items[0], str):
            kept = items[0].lstrip()
            head, items[0] = items[0][: len(items[0]) - len(kept)], kept
        if isinstance(items[-1], str):
            kept = items[-1].rstrip()
            tail, items[-1] = items[-1][len(kept) :], kept
        items = [item for item in items if item != ""]
        if head:
            out.append(head)
        if items:
            out.append(mb_html.span(items, {"lang": "hbo"}))
        if tail:
            out.append(tail)

    for node in nodes:
        if _is_unpointed_el(node):
            close()
            out.append(node)
        elif mb_html.is_htel(node) and _has_unpointed(node.get("contents") or []):
            close()
            tag = mb_html.htel_get_tag(node)
            out.append(
                mb_html.htel_mk(tag, node.get("attr"), _hbo_groups(node["contents"]))
            )
        else:
            run.append(node)
    close()
    return out


def td_ref(ref: str):
    return mb_html.table_datum(short_ref(ref), {"class": "bcv"})


def td_refs(ref_list: list):
    return mb_html.table_datum(refs(ref_list), {"class": "bcv"})


def td_num(count: int):
    return mb_html.table_datum(num(count), {"class": "num"})


def conventions(*, attention: bool) -> list:
    """The paragraph and list that name a page's typographic conventions."""
    items = [
        [
            mb_html.span(
                "Text styled like this", {"title": "an example of hover text"}
            ),
            " reveals more on hover, where the medium allows hovering.",
        ],
    ]
    if attention:
        items.append(
            [
                mb_html.span_c("Text styled like this", "attention"),
                " draws attention to letters of a form, as to the ",
                unpointed("ב"),
                " of ",
                unpointed(["א", mb_html.span_c("ב", "attention"), "ג"]),
                ".",
            ]
        )
    items.append(
        [
            uname(ha.ZSH_OR_TSIT),
            " is the name of a Unicode code point, less the words that name its script"
            " and class. Hovering shows the whole name, here ",
            uname(ha.ZSH_OR_TSIT, full=True),
            ".",
        ]
    )
    counts = {2: "two", 3: "three"}
    return [
        p(f"This page has {counts[len(items)]} typographic conventions:"),
        author.ordered_list(items),
    ]


# REFERENCES -----------------------------------------------------------------------------------


def short_book(title: str) -> str:
    """A book's short name, from its title on Sefaria: Gen, 2 Sam, Song."""
    abbrev = osis_book_abbrevs.BOOK_ABBREVS[_BK39_OF_TITLE[title]]
    return f"{abbrev[0]} {abbrev[1:]}" if abbrev[0].isdigit() else abbrev


def short_ref(ref: str) -> str:
    """A reference as the files write it, with its book's short name: Gen 2:5, Exod 15."""
    title, place = ref.rsplit(" ", 1)
    return f"{short_book(title)} {place}"


def refs(ref_list: list) -> str:
    """Short references, consecutive verses as a range: Exod 20:2–6, 8–10 and 13–15."""
    groups = []
    for ref in ref_list:
        book, cv = short_ref(ref).rsplit(" ", 1)
        chapter, verse = (int(x) for x in cv.split(":"))
        last = groups[-1] if groups else None
        if last and last[0] == book and last[1] == chapter and last[3] == verse - 1:
            last[3] = verse
        else:
            groups.append([book, chapter, verse, verse])
    by_book = []
    for book, chapter, first, last in groups:
        verses = f"{first}" if first == last else f"{first}\N{EN DASH}{last}"
        if by_book and by_book[-1][0] == book:
            same_chapter = by_book[-1][2] == chapter
            by_book[-1][1].append(verses if same_chapter else f"{chapter}:{verses}")
            by_book[-1][2] = chapter
        else:
            by_book.append([book, [f"{chapter}:{verses}"], chapter])
    by_book = [(book, spans) for book, spans, _chapter in by_book]
    parts = [f"{book} " + "".join(join(spans)) for book, spans in by_book]
    if len(parts) == 1:
        return parts[0]
    if all(len(spans) == 1 for _book, spans in by_book):
        return "".join(join(parts))
    if len(parts) == 2:
        return f"{parts[0]}, and {parts[1]}"
    return "; ".join(parts[:-1]) + "; and " + parts[-1]


# LIFTING FORMS FROM THE FILES -----------------------------------------------------------------


def _part_pattern(part: str) -> str:
    if part and set(part) <= set(ms.LETTERS):
        return "".join(re.escape(c) + f"{ms.MARK_CLASS}*" for c in part)
    return re.escape(part)


def find(text: str, parts: tuple, where: str) -> tuple:
    """The one place in ``text`` that ``parts`` match, as a pair of offsets.

    Each part is either the letters of one atom or the literal characters between atoms.
    """
    pattern = "".join(_part_pattern(part) for part in parts)
    return _one_place(text, pattern, where, parts)


def find_atom(text: str, atom: str, where: str) -> tuple:
    """The one place in ``text`` that has exactly ``atom``, as a pair of offsets."""
    return _one_place(text, re.escape(atom), where, atom)


def _one_place(text: str, pattern: str, where: str, what) -> tuple:
    regex = re.compile(f"(?<!{_EDGE}){pattern}(?!{_EDGE})")
    hits = [m.span() for m in regex.finditer(text)]
    if len(hits) != 1:
        raise ValueError(f"{where}: {len(hits)} places match {what!r}")
    return hits[0]


def chanted_words(text: str, start: int, end: int) -> tuple:
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


def snippet(verse, start: int, end: int) -> list:
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


def lift(ref: str, parts: tuple, s, *, whole: bool = True) -> list:
    """The form at ``ref`` that ``parts`` match, as csv/ has it, its chanted words whole."""
    verse = s.verse(ref)
    start, end = find(verse.text, parts, ref)
    if whole:
        start, end = chanted_words(verse.text, start, end)
    return snippet(verse, start, end)


def lift_atom(ref: str, parts: tuple, s) -> str:
    verse = s.verse(ref)
    start, end = find(verse.text, parts, ref)
    return verse.text[start:end]


def lift_element(verse, el, *, whole: bool = True) -> list:
    start, end = el.start, el.end
    if whole:
        start, end = chanted_words(verse.text, start, end)
    return snippet(verse, start, end)


def highlight(atom: str, cluster_index: int) -> list:
    """An atom with one of its letters, and that letter's marks, in the attention color."""
    clusters = list(ms.CLUSTER_RE.finditer(atom))
    a, b = clusters[cluster_index].span()
    parts = [atom[:a], mb_html.span_c(atom[a:b], "attention"), atom[b:]]
    return [part for part in parts if part != ""]


def highlight_in(text: str, atom: str, cluster_index: int, where: str) -> list:
    """The chanted words of ``text`` around its one ``atom``, with one letter highlighted."""
    start, end = find_atom(text, atom, where)
    word_start, word_end = chanted_words(text, start, end)
    parts = [
        text[word_start:start],
        *highlight(atom, cluster_index),
        text[end:word_end],
    ]
    return [part for part in parts if part != ""]


def cgj_index(atom: str) -> int:
    """The index of the letter of ``atom`` that has the COMBINING GRAPHEME JOINER."""
    return next(i for i, c in enumerate(ms.CLUSTER_RE.findall(atom)) if sd.CGJ in c)


# WRITING A PAGE -------------------------------------------------------------------------------


def page_head(title: str) -> list:
    """The heading, author and revision that each page opens with."""
    return [
        author.heading_level_1(title.replace("MAM", "$MAM")),
        mb_html.para(AUTHOR),
        mb_html.para(REVISION),
    ]


def _guard_two_vowels(cbody, s) -> None:
    """Refuse a page with two vowels on one letter, but where the files have them.

    The files have them only with a COMBINING GRAPHEME JOINER between the two, which keeps
    their order.  The page that this documentation replaced had a letter with two vowels and
    no CGJ, and how it looked depended on the font.
    """
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


def _guard_unpointed_hbo(cbody) -> None:
    """Refuse a page that sets unpointed Hebrew in the Hebrew font.

    The text of each element with ``lang="hbo"`` is read as a browser shapes it, joined across
    inline elements, and each of its Hebrew tokens with a letter or a NUN HAFUKHA must have a
    point or an accent.  A token of punctuation alone, such as the PASEQ between two pointed
    atoms of an example, needs none.
    """

    def text(node) -> str:
        if isinstance(node, str):
            return node
        if isinstance(node, (list, tuple)):
            return "".join(text(item) for item in node)
        if mb_html.is_htel(node):
            if mb_html.htel_get_tag(node) == "br":
                return " "
            return text(node.get("contents") or [])
        return ""

    def visit(node):
        if isinstance(node, (list, tuple)):
            for item in node:
                visit(item)
        elif mb_html.is_htel(node):
            if (node.get("attr") or {}).get("lang") != "hbo":
                visit(node.get("contents") or [])
                return
            for token in _HEBREW_TOKEN_RE.findall(text(node)):
                based = any(c in ms.LETTERS or c == hpu.NUN_HAF for c in token)
                if based and not _MARK_RE.search(token):
                    raise ValueError(f"unpointed Hebrew, {token!r}, in the Hebrew font")

    visit(cbody)


def write_page(py_file, subdir: str | None, title: str, cbody: list, s):
    """Write one page in ``gh-pages/MAM-for-Sefaria/``, or in a folder in it, and the font.

    The pages share ``styles.css`` and the font copy beside it, which
    ``report_stylesheet.copy_report_font`` keeps byte-identical to ``doc/woff2/``'s.
    """
    _guard_two_vowels(cbody, s)
    _guard_unpointed_hbo(cbody)
    top = paths.gh_pages_dir() / OUT_DIR
    report_stylesheet.copy_report_font(top)
    if subdir is None:
        out_dir, css_hrefs = top, ("../document.css", "styles.css")
    else:
        out_dir, css_hrefs = top / subdir, ("../../document.css", "../styles.css")
        out_dir.mkdir(exist_ok=True)
    fname = "index.html"
    author.help_gen_html_file(
        py_file, (str(out_dir), css_hrefs), fname, title, cbody, viewport=True
    )
    return out_dir / fname
