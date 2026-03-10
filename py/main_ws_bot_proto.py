from pycmn import bib_locales as tbn
from pycmn import file_io
from pyws import ws_get_bk_in_both_fmts as wsin
from pyws import ws_bot_edit as wbe
from py_misc.my_utils_for_mainish import show_progress_g
from pycmn.my_utils import dv_map
from pycmn.my_utils import dkv_map


def main():
    """
    Prototypes the bot by using local file I/O rather than server I/O.
    """
    for bk39id in tbn.ALL_BK39_IDS:
        show_progress_g(__file__, "book", bk39id)
        wsf2_book = wsin.get_bk_in_fmt_2(_IN_PATH, bk39id)
        out_book = dkv_map(wbe.edit_cif2, wsf2_book)
        osdf = tbn.ordered_short_dash_full_39(bk39id)
        _write_book_lines(osdf, out_book)
        _write_book_fmt_2(osdf, out_book)


_IN_PATH = "in/mam-ws"
_OUT_PATH_LINES = "out/mam-ws-bot-proto"
_OUT_PATH_FMT_2 = "out/mam-ws-bot-proto-fmt-2"


def _write_book_lines(osdf, dic_from_hcn_to_book_pair):
    dic_from_hcn_to_lines = dv_map(_splitlines, dic_from_hcn_to_book_pair)
    out_path = f"{_OUT_PATH_LINES}/{osdf}.json"
    file_io.json_dump_to_file_path(dic_from_hcn_to_lines, out_path)


def _write_book_fmt_2(osdf, dic_from_hcn_to_book_pair):
    dic_from_hcn_to_fmt_2 = dv_map(_fmt_2, dic_from_hcn_to_book_pair)
    out_path_fmt_2 = f"{_OUT_PATH_FMT_2}/{osdf}.json"
    file_io.json_dump_to_file_path(dic_from_hcn_to_fmt_2, out_path_fmt_2)


def _splitlines(book_pair):
    out_cif2, big_str = book_pair
    return big_str.splitlines()


def _fmt_2(book_pair):
    out_cif2, _big_str = book_pair
    return out_cif2


if __name__ == "__main__":
    main()
