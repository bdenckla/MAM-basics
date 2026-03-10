""" Exports main """

from pycmn import file_io
from pycmn import read_books_from_mam_parsed_plus as plus
from py_misc.wordlist import get_sorted_words_wt


def main():
    """Generate a JSON list of the qere words in MAM"""
    books_mpp = plus.read_parsed_plus_bk39s()
    sorted_words_wt = get_sorted_words_wt(books_mpp)
    file_io.json_dump_to_file_path(sorted_words_wt, "out/mam-qere-words.json")


if __name__ == "__main__":
    main()
