"""
Write dual-cantillation (Decalogues and Reuben) data to JSON.

Reads MAM-parsed-plus and records, for each verse that has it, the
dual-cantillation information.
"""

from pydecnreub.decnreub import do_one_book
from pydecnreub.decnreub import flatrow_for_jsondump
from pycmn import file_io
from pycmn import read_books_from_mam_parsed_plus as plus
from pycmn import bib_locales as tbn
from pycmn.my_utils import sl_map
from pycmn.my_utils import sum_of_map

# For Saga of Reuben we consider:
#    * the פשוטה ("simple"?) accent scheme to be analogous to taxton
#    * the מדרשית ("midrashic"?) accent scheme to be analogous to elyon


def almost_main():
    """Write dual cantillation info to a JSON file."""
    # This dual cantillation info includes both the
    # combined cantillation and single cantillation representations
    # of the dual cantillation phrases in the following:
    #    * the Exodus decalogue
    #    * the Deuteronomy decalogue
    #    * the Saga of Reuben
    books_mpp = plus.read_parsed_plus_bk39s(tbn.BK39IDS_OF_BOOKS_WITH_DUALCANT)
    #
    out_rows = sum_of_map(do_one_book, books_mpp.values())
    flatrows = sl_map(flatrow_for_jsondump, out_rows)
    file_io.json_dump_to_file_path(flatrows, "out/mam-decnreub.json")


def main():
    """Write dual cantillation info to a JSON file."""
    almost_main()


if __name__ == "__main__":
    main()
