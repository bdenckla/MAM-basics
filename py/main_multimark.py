"""Record information about letters that carry multiple diacritical marks."""

from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import file_io
from multimark import multimark_1 as mm1
from multimark import multimark_2 as mm2

FIOI_PATH_TO_MULTIMARKS_RAW_JSON = "io/mam-multimarks-raw.json"
# FIOI: file I/O info: this is the output of one program and the input of one or more other programs


def almost_main():
    """Record info about letters with multiple marks on them."""
    books_mpu = plus.read_parsed_plus_bk39s()
    raw_data_wt = mm1.get_raw_data_wt(books_mpu)
    file_io.json_dump_to_file_path(raw_data_wt, FIOI_PATH_TO_MULTIMARKS_RAW_JSON)
    mm2.phase_2(FIOI_PATH_TO_MULTIMARKS_RAW_JSON)


def main():
    """Record info about letters with multiple marks on them."""
    almost_main()


if __name__ == "__main__":
    main()
