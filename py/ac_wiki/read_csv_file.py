import collections
import csv
import re
from mb_cmn import file_io
from mb_cmn.my_utils import sum_of_map
from mb_cmn.my_utils import sl_map


def read_csv_file(csv_in_path, json_out_path):
    with open(csv_in_path, encoding="utf-8") as csv_in_fp:
        rows = sl_map(_ROW._make, csv.reader(csv_in_fp))
    assert rows[0] == _EXPECTED_CSV_HEADER
    data_rows = rows[1:]
    assert len(data_rows) == _EXPECTED_LEN_CSV_DATA
    data_entries = sl_map(_make_data_entry, data_rows)
    file_io.json_dump_to_file_path(_dic_to_dump(data_entries), json_out_path)
    return data_entries


def _dic_to_dump(data_entries):
    json_header = _make_json_header(data_entries)
    dic_to_dump = {
        "header": json_header,
        "body": data_entries,
    }
    return dic_to_dump


_EXPECTED_CSV_HEADER_VALS = (
    "Text Range",
    "Leaf",
    "Page",
    "Bar Hama 2",
    "Gap",
    "Notes",
    "URL-suffix",
)
_ROW_FIELD_NAMES = "text_range,leaf,page,bar_hama_2,gap,notes,url_suffix"
_ROW = collections.namedtuple("_ROW", _ROW_FIELD_NAMES)
_EXPECTED_CSV_HEADER = _ROW._make(_EXPECTED_CSV_HEADER_VALS)
_EXPECTED_LEN_CSV_DATA = 590
_URL_BASE = "https://barhama.com/aleppocodex/?image=ALEPPO_CODEX_"  # append url_suffix
_PATT_FOR_BK = r"((?:[12] )?[A-Z][a-z]+)"  # E.g. "1 Sam", "Deut"
_PATT_FOR_CV = r"(\d+):(\d+)"
_PATT_FOR_BCV = _PATT_FOR_BK + " " + _PATT_FOR_CV
_EN_DASH = "–"
_PATT_FOR_1BK_RANGE = _PATT_FOR_BCV + _EN_DASH + _PATT_FOR_CV
_PATT_FOR_2BK_RANGE = _PATT_FOR_BCV + _EN_DASH + _PATT_FOR_BCV


def _cv_strs_to_ints_3(three):
    bkna, str_chnu, str_vrnu = three
    return bkna, int(str_chnu), int(str_vrnu)


def _cv_strs_to_ints_33(three_and_three):
    assert len(three_and_three) == 2
    return _cv_strs_to_ints_3(three_and_three[0]), _cv_strs_to_ints_3(
        three_and_three[1]
    )


def _parse_text_range(text_range):
    if match := re.fullmatch(_PATT_FOR_1BK_RANGE, text_range):
        # E.g. Deut 28:17–28:45
        groups = match.groups()
        assert len(groups) == 5
        three_and_three = groups[:3], [groups[0], *groups[3:]]
        return _cv_strs_to_ints_33(three_and_three)
    if match := re.fullmatch(_PATT_FOR_2BK_RANGE, text_range):
        # E.g. Judg 21:15–1 Sam 1:13
        groups = match.groups()
        assert len(groups) == 6
        three_and_three = groups[:3], groups[3:]
        return _cv_strs_to_ints_33(three_and_three)
    assert False, text_range


def _make_data_entry(data_row):
    text_range_p = _parse_text_range(data_row.text_range)
    if data_row.url_suffix:
        syn_url = _URL_BASE + data_row.url_suffix
        assert syn_url == data_row.bar_hama_2
    else:
        syn_url = None
        assert data_row.bar_hama_2 == ""
    return {
        "de_text_range": text_range_p,
        "de_leaf": data_row.leaf,
        "de_url": syn_url,
        "de_gap": data_row.gap or None,
    }


def _get_books(data_entry):
    start_bcv, stop_bcv = data_entry["de_text_range"]
    return [start_bcv[0], stop_bcv[0]]


def _op_unique(lis):  # order-preserving unique
    # Normally, we'd just use set() to remove duplicates,
    # and perhaps sort after, to get a stable (and sensible) order.
    # but here we want to preserve order.
    dic = {}
    for elem in lis:
        dic[elem] = True
    return list(dic.keys())


def _lacks_url(data_entry):
    return data_entry["de_url"] is None


def _has_gap(data_entry):
    return data_entry["de_gap"] is not None


def _make_json_header(data_entries):
    rows_sans_url = list(filter(_lacks_url, data_entries))
    rows_with_gap = list(filter(_has_gap, data_entries))
    books = _op_unique(sum_of_map(_get_books, data_entries))
    return {
        "rows_sans_url": rows_sans_url,
        "rows_with_gap": rows_with_gap,
        "books": books,
    }
