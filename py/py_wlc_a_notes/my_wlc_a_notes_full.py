"""Exports write_xml."""

import py_html.wlc_utils_html as wlc_utils_html
import py_html.my_html_for_img as img
import py_wlc.my_wlc_bcv_str as my_wlc_bcv_str
import py_wlc_a_notes.my_wlc_a_notes_utils as my_wlc_a_notes_utils
import py_wlc_a_notes.my_wlc_a_notes_full_nav as nav
from mb_cmn import paths


def write(io_records):
    """Write records out in full format."""
    for io_record in io_records:
        io_record["path-to-full"] = _write_record(io_record)


_HBO_RTL = {"lang": "hbo", "dir": "rtl"}


def _make_key_value_row(key, value, hbo=False):
    cell_for_key = wlc_utils_html.table_datum(key)
    attr = _HBO_RTL if hbo else None
    cell_for_value = wlc_utils_html.table_datum(value, attr)
    return wlc_utils_html.table_row([cell_for_key, cell_for_value])


def _write_record(record):
    #
    body_contents = []
    #
    body_contents.append(wlc_utils_html.para(nav.navs(record)))
    #
    if html_for_i := img.html_for_imgs(record):
        body_contents.extend(html_for_i)
    #
    rows = _initial_rows(record)
    ucp = record["uxlc-change-proposal"]
    if isinstance(ucp, str):
        # XXX make this a real link
        rows.append(_make_key_value_row("existing UCP", ucp))
    #
    rows.append(_folio_row(record))
    #
    body_contents.append(wlc_utils_html.table(rows))
    #
    _append_remarks_and_side_notes(body_contents, record)
    #
    wlc_index = record["wlc-index"]
    title = f"WLC a-note {wlc_index}"
    path = f"full-record/wlc_a_note_{wlc_index:02}.html"
    write_ctx = wlc_utils_html.WriteCtx(
        title, str(paths.wlc_pages_dir() / "wlc-a-notes" / path), centered=True
    )
    wlc_utils_html.write_html_to_file(body_contents, write_ctx, "../../")
    return path


def _append_remarks_and_side_notes(io_body_contents, record):
    remarks = record["remarks"]
    for remark in remarks:
        assert not remark.endswith(" ")
        io_body_contents.append(wlc_utils_html.para(remark))
    #
    side_notes = record.get("side-notes") or []
    for side_note in side_notes:
        io_body_contents.append(_side_note_html(side_note))


def _side_note_html(side_note):
    snt, sns = my_wlc_a_notes_utils.side_note_string(side_note)
    assert not sns.endswith(" ")
    hesp = _hebrew_spanify(sns)
    if snt == "sn-blockquote":  # snt: side-note type
        return wlc_utils_html.blockquote(hesp)
    return wlc_utils_html.para(hesp)


def _hebrew_spanify(string: str):
    pre, sep, post = string.partition("@")
    pre_list = [pre] if pre else []
    if not sep:
        assert not post
        assert pre == string
        return pre_list
    return pre_list + _hebrew_spanify2(post)


def _hebrew_spanify2(string: str):
    pre, sep, post = string.partition("#")
    assert sep
    assert sep == "#"
    return [wlc_utils_html.span(pre, {"lang": "hbo"}), *_hebrew_spanify(post)]


def _initial_rows(record):
    anchor = _anchor(record)
    mpk = record["MPK"]
    qere = record["qere"]
    atiss = record["at issue"]
    reason = record.get("at issue English")
    rows = []
    rows.append(_make_key_value_row("bcv (tanach.us)", anchor))
    rows.append(_make_key_value_row("MPK", mpk, hbo=True))
    if qere_c := record.get("qere-context"):
        rows.append(_make_key_value_row("qere-context", qere_c, hbo=True))
    rows.append(_make_key_value_row("qere", qere, hbo=True))
    if qere_a := record.get("qere-atom-at-issue"):
        rows.append(_make_key_value_row("qere-atom-at-issue", qere_a, hbo=True))
    rows.append(_make_key_value_row("at issue", atiss, hbo=True))
    rows.append(_make_key_value_row("at issue English", reason))
    return rows


def _anchor(record):
    bcv = record["bcv"]
    href = my_wlc_bcv_str.get_tanach_dot_us_url(bcv)
    return wlc_utils_html.anchor(bcv, {"href": href})


def _line_str(record):
    if "line" in record:
        return str(record["line"])
    assert "line-excluding-blanks" in record
    assert "line-including-blanks" in record
    leb = record["line-excluding-blanks"]
    lib = record["line-including-blanks"]
    return str(leb) + "/" + str(lib)


def _folio_row(record):
    # XXX make this into a link like:
    # https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F159B.jpg
    #
    prefix = "Folio_"
    assert record["folio"].startswith(prefix)
    folio_short = record["folio"].removeprefix(prefix)
    assert folio_short
    focoli_tuple = folio_short, str(record["column"]), _line_str(record)
    focoli_str = " ".join(focoli_tuple)
    return _make_key_value_row("folio col line", focoli_str)
