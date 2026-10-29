from taamey_d.doc.book_codes import *


def att(full_str, att_substr):
    return to_str(xatt(full_str, att_substr))


def span(spanclass, inside):
    return to_str(xspan(spanclass, inside))


def sup(inside, attrs=None):
    return to_str(xsup(inside, attrs))


def para(inside, attrs=None):
    return to_str(xpara(inside, attrs))


def unordered_list(*items):
    return to_str(xunordered_list(*items))


def anchor(href, inside):
    return to_str(xanchor(href, inside))


def to_str(obj):
    if isinstance(obj, str):
        return obj
    if isinstance(obj, tuple):
        return "".join(map(to_str, obj))
    if isinstance(obj, dict):
        return _el_with_attrs(obj["tag"], to_str(obj["inside"]), obj["attrs"])
    assert False


def _to_tuple(obj):
    if isinstance(obj, tuple):
        return obj
    if isinstance(obj, (str, dict)):
        return (obj,)
    assert False


def _mk_el(tag, inside, attrs=None):
    return dict(tag=tag, inside=inside, attrs=attrs or {})


def xatt(full_str, att_substr):
    pre, mid, post = full_str.partition(att_substr)
    assert mid
    return pre, xspan("attention", mid), post


def xheading2(h2_title, h2_id=None):
    attrs = {"id": h2_id} if h2_id else {}
    return _mk_el("h2", h2_title, attrs)


def xheading3(h3_title, h3_id=None):
    attrs = {"id": h3_id} if h3_id else {}
    return _mk_el("h3", h3_title, attrs)


def xspan(spanclass, inside):
    return _mk_el("span", inside, {"class": spanclass})


def xspan2(inside, attrs):
    return _mk_el("span", inside, attrs)


def xsup(inside, attrs):  # superscript
    return _mk_el("sup", inside, attrs)


def xtable_rtl(header_cells, inside):
    return xtable(header_cells, inside, {"dir": "rtl"})


def xtable(header_cells, inside, attrs=None):
    my_attrs = attrs or {}
    th_els = tuple(map(_xtable_header_cell, header_cells))
    th_els2 = tuple((th_el, "\n    ") for th_el in th_els)
    sum_of_th_els2 = sum(th_els2, tuple())
    pre = "\n    ", xtable_row(sum_of_th_els2)
    inside_with_header = pre + inside + ("\n",)
    return _mk_el("table", inside_with_header, my_attrs)


def xtable_row(inside, attrs=None):
    my_inside = ("\n    ",) + _to_tuple(inside)
    return _mk_el("tr", my_inside, attrs)


def _xtable_header_cell(inside):
    return _mk_el("th", inside)


def xtable_data_cell(inside, attrs=None):
    return _mk_el("td", inside, attrs)


def xtable_row_of_cells(cell_insides, rowspans):
    out = []
    for cell_inside, rowspan in zip(cell_insides, rowspans):
        if rowspan == 0:
            continue
        cell_attrs = {"rowspan": rowspan} if rowspan > 1 else {}
        out.append(xtable_data_cell(cell_inside, cell_attrs))
    return xtable_row(tuple(out))


def _ones(row):
    return (1,) * len(row)


def xtable_rows_of_cells(rows_of_cell_insides, rowspans=None):
    if rowspans is None:
        my_rowspans = list(map(_ones, rows_of_cell_insides))
    else:
        my_rowspans = rowspans
    return tuple(map(xtable_row_of_cells, rows_of_cell_insides, my_rowspans))


def _el_with_attrs(tag, inside, attrs=None):
    my_attrs = attrs or {}
    attrs_strs = tuple(f'{k}="{v}"' for k, v in my_attrs.items())
    tag_with_attrs = " ".join((tag,) + attrs_strs)
    _line_break_tags = frozenset(("ul", "p"))
    mlb = "\n" if tag in _line_break_tags else ""  # maybe line break
    return f"<{tag_with_attrs}>{mlb}{inside}{mlb}</{tag}>{mlb}"


def xpara(inside, attrs=None):
    return _mk_el("p", inside, attrs)


def xcode(inside, attrs=None):
    return _mk_el("code", inside, attrs)


def xunordered_list(*items):
    list_items = tuple(map(_xlist_item, items))
    list_items2 = tuple((list_item, "\n") for list_item in list_items)
    sum_of_list_items2 = sum(list_items2, tuple())
    return _mk_el("ul", sum_of_list_items2[:-1])


def xanchor(href, inside):
    return _mk_el("a", inside, {"href": href})


def xanchor2(inside, attrs):
    return _mk_el("a", inside, attrs)


def _xlist_item(inside):
    return _mk_el("li", inside)


def implicit_maqaf(string):
    return string.replace("־", span("mam-implicit-maqaf", "־"))


def headfun(
    gregorian_document_version="2023-03-13",
    hebrew_document_version="כ׳ בַּאֲדָר תשפ״ג",
    font_version=None,
):
    version_paragraph = (
        f"\n<p>Font version: {font_version}</p>" if font_version is not None else ""
    )
    return (
        """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="Taamey-doc-styles.css">
    <title>$title_in_head_title</title>
</head>
<body>
<h1>$title_in_h1</h1>
<p>Author: Ben Denckla</p>"""
        + version_paragraph
        + """
<!-- Hebrew date below can be gotten from https://www.hebcal.com/converter -->
<p>Document version: """
        + gregorian_document_version
        + """ / """
        + hebrew_document_version
        + """</p>
"""
    )
