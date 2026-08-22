from mb_cmn import file_io
from mb_cmn.my_utils import sl_map
from mb_cmn.my_utils import dv_map, my_groupby, sum_of_map


def group_by_book(data_entries, json_out_path):
    assigned = sum_of_map(_assign_to_1_or_2_bks, data_entries)
    grouped = my_groupby(assigned, _get_assigned_book)
    unassigned = dv_map(_unassign, grouped)
    file_io.json_dump_to_file_path(unassigned, json_out_path)
    return unassigned


def _get_assigned_book(ade):  # ade: [book-]assigned data entry
    assigned_book, _data_entry = ade
    return assigned_book


def _assign_to_1_or_2_bks(data_entry):
    start_bcv, stop_bcv = data_entry["de_text_range"]
    if start_bcv[0] == stop_bcv[0]:
        return [(start_bcv[0], data_entry)]
    return [(start_bcv[0], data_entry), (stop_bcv[0], data_entry)]


def _get_data_entry(ade):  # ade: [book-]assigned data entry
    _assigned_book, data_entry = ade
    return data_entry


def _unassign(lis_ade):
    return sl_map(_get_data_entry, lis_ade)
