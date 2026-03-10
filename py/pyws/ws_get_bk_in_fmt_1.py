import json
from pyws import ws_tmpl_n_tag_parser as ttp
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn.my_utils import dv_map


def get_bk_in_fmt_1(path, bkid):
    """Read in Wikisource book identified by bkid. Return it in format 1."""
    in_path = mbkn_a_sbkn.wikisource_book_path_fr_bk39id(path, bkid)
    with open(in_path, encoding="utf-8") as json_in_fp:
        hcn_to_lines = json.load(json_in_fp)
    # hcn: Hebrew-numeral chapter number
    return dv_map(get_chap_in_fmt_1, hcn_to_lines)


def get_chap_in_fmt_1(lines_as_strings):
    return list(map(ttp.parse, lines_as_strings))
