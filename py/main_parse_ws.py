"""Parse downloaded Wikisource MAM data into two increasingly-structured output formats."""

from py_misc import my_utils_for_mainish as my_utils_fm
from pyws import ws_get_bk_in_both_fmts as wsin
from pycmn import bib_locales as tbn
from pycmn import file_io


def main(argparse=True):
    """
    Read in the 39 per-book JSON files from the Wikisource download and output
    them to two increasingly-parsed formats.
    """
    begin_end = "per-book output (for 39 books)"
    bkids = my_utils_fm.get_bk39_tuple_from_argparse() if argparse else tbn.ALL_BK39_IDS
    my_utils_fm.show_progress_g(__file__, "BEGIN", begin_end)
    for bkid in bkids:
        wsf1_book, wsf2_book = wsin.get_bk_in_both_fmts(_IN_PATH, bkid)
        _write_outfile("out/mam-ws-parsed-fmt-1", bkid, wsf1_book)
        _write_outfile("out/mam-ws-parsed-fmt-2", bkid, wsf2_book)
        my_utils_fm.show_progress_g(__file__, "book", bkid)
    my_utils_fm.show_progress_g(__file__, "END", begin_end)


def _write_outfile(out_path, bkid, book):
    osdf = tbn.ordered_short_dash_full_39(bkid)
    out_path = f"{out_path}/{osdf}.json"
    file_io.json_dump_to_file_path(book, out_path)


_IN_PATH = "in/mam-ws"


if __name__ == "__main__":
    main()
