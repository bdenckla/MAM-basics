from pyws import ws_get_bk_in_fmt_1 as wsin1
from pyws import ws_get_bk_in_fmt_2 as wsin2
from pycmn.my_utils import dkv_map


def get_bk_in_both_fmts(path, bkid):
    """Read in Wikisource book identified by bkid. Return it in formats 1 and 2."""
    bif1 = wsin1.get_bk_in_fmt_1(path, bkid)
    return bif1, _get_bif2_fr_bif1(bkid, bif1)


def get_bk_in_fmt_2(path, bkid):
    return get_bk_in_both_fmts(path, bkid)[1]


def get_chap_in_fmt_2(lines_as_strings):
    cif1 = wsin1.get_chap_in_fmt_1(lines_as_strings)
    return wsin2.get_chap_in_fmt_2(cif1)


def _get_bif2_fr_bif1(bkid, bif1):
    """Convert bif1 (a Wikisource book in format 1) to format 2."""
    return dkv_map((_dkv_get_chap_in_fmt_2, bkid), bif1)


def _dkv_get_chap_in_fmt_2(bkid, he_chnu, parsed_lines):
    return wsin2.get_chap_in_fmt_2(parsed_lines, (bkid, he_chnu))
