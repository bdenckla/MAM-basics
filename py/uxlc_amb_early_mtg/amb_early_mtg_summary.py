"""Exports write_html."""

from mb_cmn import my_utils
import uxlc_misc.uxlc_utils_html as uxlc_utils_html
import uxlc_amb_early_mtg.amb_early_mtg_url_generator as urlg
import uxlc_paths


def write(records, path, title, intro=None):
    """Writes amb-early-mtg records to index.html and other HTML files.

    ``path`` is relative to the published amb-early-mtg directory, because it also
    serves as the in-page link target (main_amb_early_mtg's intro links "dubious.html").
    """
    if intro is None:
        intro = []
    assert isinstance(intro, list)
    rows_for_data = list(map(_rec_to_row, records))
    rows = [_row_for_header(), *rows_for_data]
    table = uxlc_utils_html.table(rows)
    body_contents = [*intro, table]
    write_ctx = uxlc_utils_html.WriteCtx(
        title, uxlc_paths.amb_early_mtg_pages_dir() / path
    )
    uxlc_utils_html.write_html_to_file(body_contents, write_ctx, "../")


def _row_cell_for_hdr_str(record, hdr_str):
    if hdr_str == "remark":
        anchors = _get_anchors_to_full_and_ucp(record)
        if initial_remark := record.get("initial-remark"):
            assert isinstance(initial_remark, str)
            datum_contents = [*anchors, "; ", *initial_remark]
        else:
            datum_contents = anchors
        return uxlc_utils_html.table_datum(datum_contents)
    if hdr_str == "bcv":
        anchor = urlg.bcv_with_link_to_tdu(record)
        return uxlc_utils_html.table_datum(anchor)
    misc_field = record[hdr_str]
    assert isinstance(misc_field, str)
    if hdr_str in ("word",):
        attr = {"lang": "hbo", "dir": "rtl"}
    else:
        assert False
    return uxlc_utils_html.table_datum(misc_field, attr)


def _get_anchors_to_full_and_ucp(record):
    path_to_full = record["path-to-full"]
    anchor_to_full = uxlc_utils_html.anchor("full", {"href": path_to_full})
    return [anchor_to_full]


def _rec_to_row(record):
    row_cells = my_utils.sl_map(
        (_row_cell_for_hdr_str, record), _STRS_FOR_CELLS_FOR_HEADER
    )
    return uxlc_utils_html.table_row(row_cells)


def _row_for_header():
    cells_for_header = list(
        map(uxlc_utils_html.table_header, _STRS_FOR_CELLS_FOR_HEADER)
    )
    return uxlc_utils_html.table_row(cells_for_header)


_STRS_FOR_CELLS_FOR_HEADER = ["bcv", "word", "remark"]
