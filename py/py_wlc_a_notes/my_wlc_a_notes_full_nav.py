"""Exports navs."""

import py_html.wlc_utils_html as wlc_utils_html


def navs(record):
    navs = []
    _maybe_append_nav(navs, record, "prev", "Prev")
    _maybe_append_nav(navs, record, "next", "Next")
    return navs


def _maybe_append_nav(io_navs, record, key, human_readable):
    if pn_rec := record.get(key):  # previous or next rec
        if io_navs:
            io_navs.append(" ")
        io_navs.append(_anchor_for_nav(human_readable, pn_rec))


def _anchor_for_nav(pn_str, record):
    wlc_index = record["wlc-index"]
    return wlc_utils_html.anchor(pn_str, {"href": _filename(wlc_index)})


def _filename(wlc_index):
    return f"wlc_a_note_{wlc_index:02}.html"
