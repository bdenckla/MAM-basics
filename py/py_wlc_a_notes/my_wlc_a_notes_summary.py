"""Exports write_html."""

import mb_cmn.my_utils as my_utils
import py_html.wlc_utils_html as wlc_utils_html
import py_wlc.my_wlc_bcv_str as my_wlc_bcv_str
import py_wlc_a_notes.my_wlc_a_notes_intro as my_wlc_a_notes_intro
from mb_cmn import paths


def write(records, xml_out_path, no_ucp=False):
    """Writes WLC a-notes records to index.html and other HTML files."""
    index_dot_html = "index-no-ucp.html" if no_ucp else "index.html"
    dis_dot_html = (
        "table-of-BHLA-disagreements-no-ucp.html"
        if no_ucp
        else "table-of-BHLA-disagreements.html"
    )
    wlc_order_dot_html = (
        "table-in-wlc-order-no-ucp.html" if no_ucp else "table-in-wlc-order.html"
    )
    intro = [
        *my_wlc_a_notes_intro.intro(no_ucp),
        *([] if no_ucp else [_intro_to_xml_out(xml_out_path)]),
        *([] if no_ucp else [_intro_to_no_ucp()]),
        _intro_to_wlc_order(wlc_order_dot_html),
        _intro_to_bhla_dis(dis_dot_html),
    ]
    _write2(records, intro, "WLC a-notes", index_dot_html, no_ucp)
    records_filtered_to_bhla_dis = list(filter(_disagrees_with_bhla, records))
    _write2(
        records_filtered_to_bhla_dis,
        [],
        "WLC a-notes disagreeing with BHLA",
        dis_dot_html,
        no_ucp,
    )
    records_in_wlc_order = sorted(records, key=_get_wlc_index)
    _write2(
        records_in_wlc_order, [], "WLC a-notes in WLC order", wlc_order_dot_html, no_ucp
    )


def _intro_to_xml_out(xml_out_path):
    return wlc_utils_html.para(
        [
            "Here is ",
            wlc_utils_html.anchor("a single XML file", {"href": xml_out_path}),
            " " "that has all 37 UXLC change proposals in it.",
        ]
    )


def _intro_to_no_ucp():
    """The one link into the no-ucp trio, which nothing pointed at until 2026-08-31.

    index-no-ucp.html links its own two tables and nothing linked IT, so all three were
    unreachable from gh-pages/index.html by any number of clicks -- and unreachable is
    what Ben objects to, placement on the landing page being optional.  Note that
    check_html_syntax_and_sanity.py's orphan check found only index-no-ucp.html: it asks
    whether SOME page links a page, so a cluster that links itself hides from it.  All
    three are also frozen targets in in/wlc_redirect_pages.json, so deleting them was
    never an option -- a stub would 404 and test_wlc_redirect_manifest.py would fail.

    Emitted only on the UCP page, since the no-ucp page linking back would make a pair
    reachable only from each other, which is the same strand one page wider.
    """
    return wlc_utils_html.para(
        [
            "This page is also available ",
            wlc_utils_html.anchor(
                "without the UXLC change proposal links",
                {"href": "index-no-ucp.html"},
            ),
            ".",
        ]
    )


def _intro_to_wlc_order(wlc_order_dot_html):
    return wlc_utils_html.para(
        [
            "The table below is also available ",
            wlc_utils_html.anchor("in WLC order", {"href": wlc_order_dot_html}),
            ". " "(The table below is in thematic order rather than in WLC order.)",
        ]
    )


def _intro_to_bhla_dis(dis_dot_html):
    return wlc_utils_html.para(
        [
            "The table below is also available ",
            wlc_utils_html.anchor(
                "filtered down to disagreements with BHLA", {"href": dis_dot_html}
            ),
            ".",
        ]
    )


def _write2(records, intro, title, path, no_ucp=False):
    rows_for_data = my_utils.sl_map((_rec_to_row, no_ucp), records)
    rows = [_row_for_header(), *rows_for_data]
    table = wlc_utils_html.table(rows)
    body_contents = [*intro, table]
    write_ctx = wlc_utils_html.WriteCtx(
        title, str(paths.wlc_pages_dir() / "wlc-a-notes" / path), centered=True
    )
    wlc_utils_html.write_html_to_file(body_contents, write_ctx, "../")


def _get_wlc_index(record):
    return record["wlc-index"]


def _disagrees_with_bhla(record):
    if dotan := record.get("Dotan"):
        assert dotan == "UXLC disagrees with BHL Appendix A"
        return True
    return False


_REC_KEY_FROM_HDR_STR = {
    "WLC qere": "qere",
    "AI": "at issue",
    "AIC": "summary",
}
_HBO_VALS = {
    "אֻ/אוּ": True,
    "הּ": True,
    "עֲ/עַ": True,
}


def _row_cell_for_hdr_str(no_ucp, record, hdr_str):
    rec_key = _REC_KEY_FROM_HDR_STR.get(hdr_str) or hdr_str
    val = record[rec_key]
    if rec_key == "remarks":
        assert isinstance(val, list)
        assert len(val) in (0, 1)
        anchors = _get_anchors_to_full_and_ucp(record, no_ucp)
        if val:
            datum_contents = [*anchors, "; ", *val]
        else:
            datum_contents = anchors
        return wlc_utils_html.table_datum(datum_contents)
    assert isinstance(val, str)
    if rec_key == "bcv":
        href = my_wlc_bcv_str.get_tanach_dot_us_url(val)
        anchor = wlc_utils_html.anchor(val, {"href": href})
        return wlc_utils_html.table_datum(anchor)
    if rec_key in ("qere", "MPK", "at issue") or _HBO_VALS.get(val):
        attr = {"lang": "hbo", "dir": "rtl"}
    else:
        attr = None
    return wlc_utils_html.table_datum(val, attr)


def _get_anchors_to_full_and_ucp(record, no_ucp):
    path_to_full = record["path-to-full"]
    anchor_to_full = wlc_utils_html.anchor("full", {"href": path_to_full})
    if no_ucp:
        return [anchor_to_full]
    path_to_ucp = record.get("path-to-ucp")
    if path_to_ucp:
        something_for_ucp = wlc_utils_html.anchor("UCP", {"href": path_to_ucp})
    else:
        something_for_ucp = "(no UCP)"
    return [anchor_to_full, "; ", something_for_ucp]


def _rec_to_row(no_ucp, record):
    row_cells = my_utils.sl_map(
        (_row_cell_for_hdr_str, no_ucp, record), strs_for_cells_for_header
    )
    return wlc_utils_html.table_row(row_cells)


def _row_for_header():
    cells_for_header = list(map(wlc_utils_html.table_header, strs_for_cells_for_header))
    return wlc_utils_html.table_row(cells_for_header)


strs_for_cells_for_header = ["bcv", "MPK", "WLC qere", "AI", "AIC", "remarks"]
