"""Exports various HTML utilities."""

from dataclasses import dataclass
from itertools import starmap

import mb_cmn.file_io as file_io
from py_html import legacy_html_lines
from mb_cmn.my_utils import sl_map, sum_of_map


@dataclass
class WriteCtx:
    """Holds info needed to write HTML to a file."""

    title: str
    path: str
    path_to_style: str
    add_wbr: bool = False


def html_text(body_contents, write_ctx: WriteCtx):
    """Return the complete page text, unwritten, for write_html_text_to_file.

    Split from the writer so that a caller can check the page before any file
    is touched.  The inputs are a body contents and a "write context"
    structure holding a title and an output path.
    """
    html_el = _htel_mk_html(
        write_ctx.title, body_contents, f"{write_ctx.path_to_style}style.css"
    )
    lines = legacy_html_lines.get_lines_from_html_el(write_ctx.add_wbr, html_el)
    return "<!doctype html>\n" + "\n".join(lines)


def write_html_text_to_file(text, write_ctx: WriteCtx):
    """Write a page's complete text, as html_text returns it, to write_ctx.path."""
    file_io.with_tmp_openw(write_ctx.path, {}, _write_text_callback, text)


def _htel_mk_html(title_text, body_contents, flex_css_hrefs):
    """Make an <html> element."""
    meta = htel_mk("meta", attr={"charset": "utf-8"})
    title = htel_mk("title", flex_contents=[title_text])
    strict_css_hrefs = _strictify(flex_css_hrefs)
    links_to_css = tuple(map(_link_to_css, strict_css_hrefs))
    head_cont = meta, title, *links_to_css
    _head = htel_mk("head", flex_contents=head_cont)
    _body = htel_mk("body", flex_contents=body_contents)
    return htel_mk("html", {"lang": "en"}, (_head, _body))


def _strictify(str_or_tuple):
    if isinstance(str_or_tuple, str):
        return [str_or_tuple]
    assert isinstance(str_or_tuple, tuple)
    return str_or_tuple


def para(contents, attr=None):
    """Make a <p> element."""
    return htel_mk("p", attr, contents)


def footnote(contents, attr=None):
    """
    Make a (fake) <footnote> element.
    (Fake because there is no such element in HTML.)
    """
    return htel_mk("footnote", attr, contents)


def blockquote(contents, attr=None):
    """Make a <blockquote> element."""
    return htel_mk("blockquote", attr, contents)


def blockquote_p(contents, b_attr=None, p_attr=None):
    """Make a <blockquote> element with a single <p> element inside."""
    return blockquote(para(contents, p_attr), b_attr)


def bdi(contents, attr=None):
    """Make a <bdi> element."""
    return htel_mk("bdi", attr, contents)


def img(attr=None):
    """Make an <img> element."""
    return htel_mk("img", attr)


def caption(contents, attr=None):
    """Make a <caption> element."""
    return htel_mk("caption", attr, contents)


def table_row(contents):
    """Make a <tr> element."""
    return htel_mk("tr", flex_contents=contents)


def table_row_of_data(tdconts, tdattrs=None):
    """Make a <tr> element containing <td> elements."""
    # tdcont: table datum contents
    # tdconts: a sequence where each element is a tdcont
    assert isinstance(tdconts, (tuple, list))
    if tdattrs is None:
        tdattrs = [None] * len(tdconts)
    assert len(tdconts) <= len(tdattrs)
    return table_row(tuple(map(table_datum, tdconts, tdattrs)))


def table_row_of_data2(list_of_cont_attr_pairs):
    """
    Make a <tr> element containing <td> elements.
    The <td> elements have the contents and attributes
    given in the pairs.
    """
    # pairs consists of a tdcont and a tdattr
    # tdcont: table datum contents
    return table_row(tuple(starmap(table_datum, list_of_cont_attr_pairs)))


def table_row_of_headers(thconts):
    """Make a <tr> element containing <th> elements."""
    # thcont: table header contents
    # thconts: a sequence where each element is a thcont
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
    # licont: list item contents
    # liconts: a sequence where each element is a licont
    return htel_mk("ul", attr, tuple(map(_list_item, liconts)))


def ordered_list(liconts, attr=None):
    """Make a <ol> element containing <li> elements."""
    # licont: list item contents
    # liconts: a sequence where each element is a licont
    return htel_mk("ol", attr, tuple(map(_list_item, liconts)))


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


def abbr(contents, attr=None):
    """Make an <abbr> (abbreviation) element."""
    return htel_mk("abbr", attr, contents)


def details(contents, attr=None):
    """Make a <details> element."""
    return htel_mk("details", attr, contents)


def summary(contents, attr=None):
    """Make a <summary> element."""
    return htel_mk("summary", attr, contents)


def detsum(summary_contents, details_contents):
    return details([summary(summary_contents), details_contents])


def code(contents, attr=None):
    """Make a <code> element."""
    return htel_mk("code", attr, contents)


def emphasis(contents, attr=None):
    """Make an <em> element."""
    return htel_mk("em", attr, contents)


def span_c(contents, the_class=None):
    """Make a <span> element, given a value for the "class" attr."""
    return span(contents, the_class and {"class": the_class})


def bold(contents, attr=None):
    """Make a <bold> element."""
    return htel_mk("b", attr, contents)


def small(contents, attr=None):
    """Make a <small> element."""
    return htel_mk("small", attr, contents)


def big(contents, attr=None):
    """Make a <big> element."""
    return htel_mk("big", attr, contents)


def sup(contents, attr=None):
    """Make a <sup> (superscript) element."""
    return htel_mk("sup", attr, contents)


def horizontal_rule(attr=None):
    """
    Make a <hr> element
    """
    return htel_mk("hr", attr)


def line_break(attr=None):
    """
    Make a <br> element
    that is NOT followed by a newline in the source code.
    """
    return htel_mk("br", attr)


def htel_mk(tag: str, attr=None, flex_contents=None, details=None):
    """Make an HTML element"""
    assert isinstance(tag, str)
    assert isinstance(attr, (type(None), dict))
    flat_contents = flatten(flex_contents)
    opts1 = {
        "attr": attr,
        "contents": flat_contents,
    }
    opts2 = {k: v for k, v in opts1.items() if v is not None}
    return {"_htel_tag": tag, **opts2}


def htel_set_contents(htel_old, new_contents):
    return {**htel_old, "contents": new_contents}


def flatten(flex_contents):
    if _is_str_or_htel(flex_contents):
        return [flex_contents]
    if isinstance(flex_contents, (tuple, list)):
        return sum_of_map(flatten, flex_contents)
    assert flex_contents is None, flex_contents
    return None


def flatten_nn(flex_contents):  # nn: not None
    flat = flatten(flex_contents)
    assert flat is not None
    return flat


def maybe_join(as_str, str_or_fns):
    shaped_htobjs = sl_map((_maybe_as_str, as_str), str_or_fns)
    # E.g. [['a', 'b'], 'c']
    flat_htobjs = flatten(shaped_htobjs)
    # E.g. ['a', 'b', 'c']
    if as_str:
        return "".join(flat_htobjs)
    return flat_htobjs


def _maybe_as_str(as_str, str_or_fn):
    if isinstance(str_or_fn, str):
        return str_or_fn
    return str_or_fn(as_str=as_str)


def htel_deref_tag(html_el):
    """Deref the tag of an HTML element."""
    return html_el["_htel_tag"]


def is_htel(obj):
    return isinstance(obj, dict) and "_htel_tag" in obj


###########################################################


def _is_str_or_htel(obj):
    return isinstance(obj, str) or is_htel(obj)


def _write_text_callback(text, out_fp):
    out_fp.write(text)


def _list_item(contents, attr=None):
    return htel_mk("li", attr, contents)


def _link_to_css(css_href):
    link_to_css_attr = {"rel": "stylesheet", "href": css_href}
    return htel_mk("link", attr=link_to_css_attr)
