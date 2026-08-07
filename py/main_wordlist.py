"""Generate a JSON list of the qere (read-aloud) words in MAM."""

from mb_cmn import file_io
from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from py_misc.wordlist import get_sorted_words_wt


def almost_main():
    """Generate a JSON list of the qere words in MAM"""
    books_mpu = plus.read_parsed_plus_bk39s(mam_parsed_path=paths.mam_parsed_path())
    sorted_words_wt = get_sorted_words_wt(books_mpu)
    file_io.json_dump_to_file_path(sorted_words_wt, "out/mam-qere-words.json")


def main():
    """Generate a JSON list of the qere words in MAM"""
    almost_main()


if __name__ == "__main__":
    main()
