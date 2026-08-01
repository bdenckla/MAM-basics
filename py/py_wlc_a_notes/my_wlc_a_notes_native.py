"""Exports write_native_to_html."""

import py_html.wlc_utils_html as wlc_utils_html
import py_html.my_html_for_img as img
import wlc_paths


def write_to_html(native, record):
    """Write XML (represented as a native Python dict) to an HTML file."""
    rows = list(map(_make_key_value_row, native.items()))
    #
    body_contents = []
    if html_for_i := img.html_for_imgs(record):
        body_contents.extend(html_for_i)
    body_contents.append(wlc_utils_html.table(rows, {"class": "limited-width"}))
    ucp_n = int(native["n"])
    ucp_n_str_02 = f"{ucp_n:02d}"
    title = f"UXLC change proposal {ucp_n}"
    path = f"ucp/uxlc_change_proposal_{ucp_n_str_02}.html"
    write_ctx = wlc_utils_html.WriteCtx(
        title, str(wlc_paths.gh_pages_dir() / "wlc-a-notes" / path), centered=True
    )
    wlc_utils_html.write_html_to_file(body_contents, write_ctx, "../../")
    return path


def _make_key_value_row(kv_pair):
    key, value = kv_pair
    cell_for_key = wlc_utils_html.table_datum(key)
    if key in ("reftext", "changetext"):
        attr = {"lang": "hbo", "dir": "rtl"}
    else:
        attr = None
    cell_for_value = wlc_utils_html.table_datum(value, attr)
    return wlc_utils_html.table_row([cell_for_key, cell_for_value])
