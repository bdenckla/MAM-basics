"""Exports various HTMl utilities."""

from dataclasses import dataclass
from typing import Union

import mb_cmn.file_io as file_io
from mb_misc import mb_html_get_lines


@dataclass
class WriteCtx:
    """Holds info needed to write HTML to a file."""

    title: str
    path: str
    style: Union[str, None] = None
    add_wbr: bool = False
    html_comment: Union[str, None] = None
    # When set, the <body> gets class="centered-page": the content column is centered on the
    # page and wide tables break out of the text measure but stay centered (issue wlc-utils#57).
    centered: bool = False


def write_html_to_file(body_contents, write_ctx: WriteCtx, path_to_style):
    """
    Write HTML to file based on the following inputs:
        * a body contents
        * a "write context" structure containing:
            * a title
            * an output path
    """
    html_el = html_el2(
        write_ctx.title,
        body_contents,
        f"{path_to_style}style.css",
        centered=write_ctx.centered,
    )
    file_io.with_tmp_openw(
        write_ctx.path,
        {},
        _write_callback,
        html_el,
        write_ctx.add_wbr,
        write_ctx.html_comment,
    )


def el_to_str_no_wbr(html_el):
    """Call el_to_str with add_wbr=False."""
    return el_to_str(add_wbr=False, html_el=html_el)


def el_to_str(add_wbr, html_el):
    """Convert an HTML element to a string, unwrapped however long its lines run.

    ONE SERIALIZER, NOT TWO.  This is the same ``mb_html_get_lines`` machinery that
    writes the pages, just with wrapping switched off (``-1``), so an in-memory fragment
    and a written page can never drift apart in how they break or escape.  With wrapping
    off the paragraph model reproduces the ``lb1``/``lb2`` newlines exactly, trailing one
    included.  Callers that render fragments to compare against expected text -- the
    edition-transcription and detangle checks -- rely on that.
    """
    lines = mb_html_get_lines.get_lines_from_html_el(_hgl_opts(add_wbr, -1), html_el)
    return "\n".join(lines)


def _hgl_opts(add_wbr, max_line_len):
    """Options for the shared serializer: THIS repo's break policy, plus the width."""
    return {
        "hgl-add-wbr": add_wbr,
        "hgl-max-line-len": max_line_len,
        "hgl-line-breaks-allowed": True,
        "hgl-lb1": _LB1,
        "hgl-lb2": _LB2,
        "hgl-noclose": _NOCLOSE,
        "hgl-verbatim-tags": _VERBATIM_TAGS,
    }


def html_el2(title_text, body_contents, flex_css_hrefs, centered=False):
    """Make an <html> element."""
    meta = htel_mk("meta", attr={"charset": "utf-8"})
    title = htel_mk("title", flex_contents=(title_text,))
    strict_css_hrefs = _strictify(flex_css_hrefs)
    links_to_css = tuple(map(_link_to_css, strict_css_hrefs))
    head_cont = meta, title, *links_to_css
    _head = htel_mk("head", flex_contents=head_cont)
    body_attr = {"class": "centered-page"} if centered else None
    _body = htel_mk("body", attr=body_attr, flex_contents=body_contents)
    return _html_el1({"lang": "en"}, (_head, _body))


def _strictify(str_or_tuple):
    if isinstance(str_or_tuple, str):
        return (str_or_tuple,)
    assert isinstance(str_or_tuple, tuple)
    return str_or_tuple


def para(contents, attr=None):
    """Make a <p> element."""
    return htel_mk("p", attr, contents)


def blockquote(contents, attr=None):
    """Make a <blockquote> element."""
    return htel_mk("blockquote", attr, contents)


def figure(contents, attr=None):
    """Make a <figure> element."""
    return htel_mk("figure", attr, contents)


def figcaption(contents, attr=None):
    """Make a <figcaption> element."""
    return htel_mk("figcaption", attr, contents)


def img(attr=None):
    """Make an <img> element."""
    return htel_mk("img", attr)


def svg(contents, attr=None):
    """Make an <svg> element."""
    return htel_mk("svg", attr, contents)


def rect(attr=None):
    """Make an <svg> <rect> element.

    Emitted CLOSED (``<rect ...></rect>``), not as a void tag: in HTML5 foreign
    content an unclosed <rect> would swallow the following siblings.
    """
    return htel_mk("rect", attr, ())


def caption(contents):
    """Make a <caption> element."""
    return htel_mk("caption", flex_contents=contents)


def table_row(contents):
    """Make a <tr> element."""
    return htel_mk("tr", flex_contents=contents)


def table_row_of_data(tdconts, tdattrs=None):
    """Make a <tr> element containing <td> elements."""
    if tdattrs is None:
        tdattrs = (None,) * len(tdconts)
    return table_row(tuple(map(table_datum, tdconts, tdattrs)))


def table_row_of_headers(thconts):
    """Make a <tr> element containing <th> elements."""
    return table_row(tuple(map(table_header, thconts)))


def table_datum(contents, attr=None):
    """Make a <td> (table datum cell) element."""
    return htel_mk("td", attr, contents)


def table_header(contents, attr=None):
    """Make a <th> (table header cell) element."""
    return htel_mk("th", attr, contents)


def div(contents, attr=None):
    """Make a <div> element."""
    return htel_mk("div", attr, contents)


def table(contents, attr=None):
    """Make a <table> element."""
    return htel_mk("table", attr, contents)


def unordered_list(liconts, attr=None):
    """Make a <ul> element containing <li> elements."""
    return htel_mk("ul", attr, tuple(map(_list_item, liconts)))


def heading_level_1(contents, attr=None):
    """Make an <h1> element."""
    return htel_mk("h1", attr, contents)


def heading_level_2(contents, attr=None):
    """Make an <h2> element."""
    return htel_mk("h2", attr, contents)


def heading_level_3(contents, attr=None):
    """Make an <h3> element."""
    return htel_mk("h3", attr, contents)


def anchor(contents, attr=None):
    """Make an <a> element."""
    return htel_mk("a", attr, contents)


def colgroup(contents, attr=None):
    """Make a <colgroup> element."""
    return htel_mk("colgroup", attr, contents)


def col(attr=None):
    """Make a <col> element."""
    return htel_mk("col", attr)


def span(contents, attr=None):
    """Make a <span> element."""
    return htel_mk("span", attr, contents)


def code(contents, attr=None):
    """Make a <code> element."""
    return htel_mk("code", attr, contents)


def span_c(contents, the_class=None):
    """Make a <span> element, given a value for the class attr."""
    return span(contents, the_class and {"class": the_class})


def bold(contents, attr=None):
    """Make a <bold> element."""
    return htel_mk("b", attr, contents)


def em(contents, attr=None):
    """Make an <em> element."""
    return htel_mk("em", attr, contents)


def small(contents, attr=None):
    """Make a <small> element."""
    return htel_mk("small", attr, contents)


def abbr(contents, title):
    """Make an <abbr> element: a short form, with the full one revealed on hover."""
    return htel_mk("abbr", {"title": title}, contents)


def big(contents, attr=None):
    """Make a <big> element."""
    return htel_mk("big", attr, contents)


def bdi(contents, attr=None):
    """Make a <bdi> element (bidirectional isolate: keeps a run of opposite-direction text,
    e.g. Hebrew embedded in an English sentence, from disturbing the surrounding order).
    """
    return htel_mk("bdi", attr, contents)


def bdi_multi(*items, conj="and"):
    """Inline nodes for a comma-separated list of opposite-direction items (e.g. Hebrew words in
    English prose), each wrapped in <bdi> so the list keeps its written order however a viewer
    resolves the surrounding bidirectional text -- without this, adjacent RTL items merge across
    their neutral commas and render reversed. Joined by ", " with a serial ", <conj> " before the
    last item (or " <conj> " when there are only two). Each item may be a bare string or a
    prebuilt htel such as an hbo(...) span. Returns a TUPLE of inline nodes -- splice it into a
    contents tuple with ``*``: ``(..., *bdi_multi("א", "ב", "ג"), ...)``. Call it with one item
    per line so the source order is unambiguous however the editor renders the RTL literals.
    """
    assert items, "bdi_multi needs at least one item"
    wrapped = [bdi(item) for item in items]
    last = len(wrapped) - 1
    parts = []
    for i, node in enumerate(wrapped):
        if i == last and i:
            parts.append(f", {conj} " if last >= 2 else f" {conj} ")
        elif i:
            parts.append(", ")
        parts.append(node)
    return tuple(parts)


def sup(contents, attr=None):
    """Make a <sup> (superscript) element."""
    return htel_mk("sup", attr, contents)


def horizontal_rule(attr=None):
    """Make a <hr> element."""
    return htel_mk("hr", attr)


def line_break(attr=None):
    """Make a <br> element."""
    return htel_mk("br", attr)


def word_break_opportunity(attr=None):
    """Make a <wbr> element (a permitted line-break point, no visible glyph)."""
    return htel_mk("wbr", attr)


def htel_mk(tag: str, attr=None, flex_contents=None):
    """Make an HTML element.

    ONE CONSTRUCTOR.  There used to be six: this one plus ``_inline``, ``_inline_nc``,
    ``_nlb1``, ``_nlb1_nc`` and ``_nlb2_nc``, each stamping ``lb1``/``lb2``/``noclose``
    onto the element to tell the serializer how to break around it and whether to close
    it.  All three are now properties of the TAG, read from this module's
    ``_LB1``/``_LB2``/``_NOCLOSE`` tables, so an element carries no break policy at all
    and the variants said nothing this one does not.  Picking a constructor was also the
    only way one tag could end up breaking two different ways in two places -- which is
    exactly what happened; see the table comment below.
    """
    assert isinstance(tag, str)
    assert isinstance(attr, (type(None), dict))
    strict_contents = (
        (flex_contents,) if _is_str_or_htel(flex_contents) else flex_contents
    )
    if isinstance(strict_contents, (tuple, list)):
        for seq_el in strict_contents:
            assert _is_str_or_htel(seq_el)
    else:
        assert strict_contents is None
    opts1 = {"attr": attr, "contents": strict_contents}
    opts2 = {k: v for k, v in opts1.items() if v is not None}
    return {"_htel_tag": tag, **opts2}


def htel_get_tag(html_el):
    """Get the tag of an HTML element."""
    return html_el["_htel_tag"]


def is_htel(obj):
    return isinstance(obj, dict) and htel_get_tag(obj)


def _is_str_or_htel(obj):
    return isinstance(obj, str) or is_htel(obj)


def _write_callback(html_el, add_wbr, html_comment, out_fp):
    """Write one page.  THE ONLY PLACE WRAPPING IS TURNED ON."""
    out_fp.write("<!doctype html>\n")
    if html_comment:
        out_fp.write(f"<!-- {html_comment} -->\n")
    lines = mb_html_get_lines.get_lines_from_html_el(
        _hgl_opts(add_wbr, _MAX_LINE_LEN), html_el
    )
    out_fp.write("\n".join(lines))


def _list_item(contents, attr=None):
    return htel_mk("li", attr, contents)


def _link_to_css(css_href):
    link_to_css_attr = {"rel": "stylesheet", "href": css_href}
    return htel_mk("link", attr=link_to_css_attr)


def _html_el1(attr, contents):
    return htel_mk("html", attr, contents)


# Width the written pages wrap to.  Only _write_callback uses it: el_to_str passes -1,
# leaving in-memory fragments unwrapped.
#
# The point of wrapping is DIFFS.  Unwrapped, a page put each paragraph on one line -- up
# to 1,782 characters -- so changing one word reported the whole paragraph as changed.  100
# matches what MAM-basics, al-hatorah and book-of-job already use.  Wrapping can only ever
# replace a space that was already in the text with a newline: prose reaches the serializer
# HTML-escaped, and an authored newline is kept as a hard break, so no break point is
# invented and no entity is touched.
_MAX_LINE_LEN = 100

# THIS REPO'S OWN LINE-BREAK POLICY, handed to the shared serializer by _hgl_opts.
#
# BY TAG, deliberately, and that is a real (small) change from what came before.  Each row
# below was read off the six now-deleted htel_mk* variants its tags used to be built with,
# and an AST scan of every such call in py/ found no tag built two ways.  (The one that
# was, `br`, took its inline row from `line_break`; the other constructor, `line_break2`,
# had no callers at all and is gone.)
#
# BUT that scan does not see every htel.  The two replayed Psalms-17:14 bodies
# (ps17v14_mam_doc_notes_body, ps17v14_double_tsinnor_body), migrated byte-exactly from
# hand-authored HTML, write their htels as LITERAL dicts.  Those pin lb1/lb2 on inline
# tags but leave block tags unpinned, so h1/p/blockquote/figure/figcaption/img there used
# to take the old el_to_str default of lb1="\n" -- disagreeing with the rows below, which
# give those tags lb1="".  So a tag table cannot reproduce those two pages byte-for-byte,
# and it does not: they lose a newline after those block-level open tags, which no browser
# renders and which brings them into line with the other 151 pages.  Ben took that trade
# knowingly (2026-07-30) rather than keep a per-element override alive for two pages; the
# alternative would have kept the per-element lb1/lb2 fields (the former `HelDetails`)
# load-bearing forever instead of letting them be deleted.  Do not "restore" it.
#
# Also do NOT "harmonize" these with MAM-basics' tables next to its own writer -- they
# genuinely disagree on h2, h3, li, tr and pre, and adopting those values would rewrap all
# 153 tracked pages for no reason.  Two repos sharing one algorithm is the point; sharing a
# break structure was never part of it.
#
# lb1 is the newline (or lack of one) after the OPEN tag, lb2 the one after the CLOSE
# tag.  Both are indexed strictly: a tag missing here raises KeyError at generation time,
# which is how a newly-introduced tag announces that it needs a row.  `strong` is here
# only because one of those literal-dict bodies uses it.
_BOTH_BREAK = (  # <tag>\n contents </tag>\n -- block elements
    "body",
    "colgroup",
    "div",
    "fieldset",
    "h2",
    "h3",
    "h4",
    "head",
    "html",
    "legend",
    "li",
    "rect",
    "script",
    "section",
    "svg",
    "table",
    "ul",
)
_BREAK_AFTER_CLOSE = (  # <tag>contents</tag>\n -- contents kept on the open tag's line
    "blockquote",
    "caption",
    "figcaption",
    "figure",
    "h1",
    "p",
    "title",
    "tr",
)
_INLINE = (  # <tag>contents</tag> -- no newline of its own at all
    "a",
    "abbr",
    "b",
    "bdi",
    "big",
    "code",
    "em",
    "label",
    "pre",
    "small",
    "span",
    "strong",
    "sup",
    "td",
    "th",
)
_INLINE_NOCLOSE = ("br", "hr", "input", "wbr")  # <tag> -- void, no newline
# Void tags followed by a newline.  `img` takes its newline as lb2 and col/link/meta as
# lb1, matching the constructors each is built with -- but a void tag has no close tag
# between the two, so BOTH spellings emit exactly `<tag>\n`.  They are kept apart here
# only so this transcription is faithful and Phase 1's zero-diff gate is testing the
# tables rather than a simplification; Phase 3 can collapse them into one row.
_NOCLOSE_BREAK_AS_LB2 = ("img",)
_NOCLOSE_BREAK_AS_LB1 = ("col", "link", "meta")

_NOCLOSE = {*_INLINE_NOCLOSE, *_NOCLOSE_BREAK_AS_LB2, *_NOCLOSE_BREAK_AS_LB1}

# Emitted raw -- neither escaped nor split for wrapping.  Entities are not decoded inside
# <style> or <script>, so escaping their CSS/JS would break it.  <pre> is here for a
# different reason: its whitespace is significant, so the RUNS OF SPACES in the parse-tree
# text that almost_errors_html_shared and poetic_oddballs fall back to must survive intact
# -- and wrapping would otherwise reflow those lines.  (Its newlines alone would not need
# this: the serializer keeps an authored newline as a hard break wherever it appears.)
_VERBATIM_TAGS = {"pre", "script", "style"}

_LB1 = {
    **{tag: "\n" for tag in _BOTH_BREAK},
    **{tag: "" for tag in _BREAK_AFTER_CLOSE},
    **{tag: "" for tag in _INLINE},
    **{tag: "" for tag in _INLINE_NOCLOSE},
    **{tag: "" for tag in _NOCLOSE_BREAK_AS_LB2},
    **{tag: "\n" for tag in _NOCLOSE_BREAK_AS_LB1},
}
_LB2 = {
    **{tag: "\n" for tag in _BOTH_BREAK},
    **{tag: "\n" for tag in _BREAK_AFTER_CLOSE},
    **{tag: "" for tag in _INLINE},
    **{tag: "" for tag in _INLINE_NOCLOSE},
    **{tag: "\n" for tag in _NOCLOSE_BREAK_AS_LB2},
    **{tag: "" for tag in _NOCLOSE_BREAK_AS_LB1},
}
