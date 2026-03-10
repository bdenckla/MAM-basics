"""
Match human-authored Google Sheets change-log entries to programmatically
detected Go-Go diffs, producing a joined report for review.
"""

from pycmn import file_io
from pymgc import mgc_input
from pymgc import mgc_join
from main_diff_gogo import FIOI_DIFF_OUTPUT_ALT_CUR_JSON


def _make_multi_dic(records, key_key):
    multi_dic = {}
    for record in records:
        key = record[key_key]
        if key in multi_dic:
            multi_dic[key].append(record)
        else:
            multi_dic[key] = [record]
    return multi_dic


def _dump_cles(cles):
    out_path = "/".join(("out", "diff_go_go", "change_log_entries_2023-04-06.json"))
    file_io.json_dump_to_file_path(cles, out_path)


def _dump_out_rows(out_rows):
    out_path = "/".join(
        ("out", "diff_go_go", "match_change_log_entries_2023-04-06.json")
    )
    file_io.json_dump_to_file_path(out_rows, out_path)


def almost_main():
    """
    Tries to match (join) the rows of the "changes" tab of Google Sheet
    with the rows of Go-Go diffs.
    """
    # diffs: Go-Go diffs (Google-to-Google diffs)
    # cles: Google change log entries
    diffs, cles = mgc_input.get_diffs_and_cles(FIOI_DIFF_OUTPUT_ALT_CUR_JSON)
    #
    _dump_cles(cles)
    #
    multi_dic_of_diffs = _make_multi_dic(diffs, "bcv")
    multi_dic_of_cles = _make_multi_dic(cles, "where2")
    #
    out_rows = mgc_join.join(multi_dic_of_diffs, multi_dic_of_cles)
    _dump_out_rows(out_rows)


def main():
    """
    Tries to match (join) the rows of the "changes" tab of Google Sheet
    with the rows of Go-Go diffs.
    """
    almost_main()


if __name__ == "__main__":
    main()
