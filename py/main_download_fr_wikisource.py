"""
Download MAM data from Hebrew Wikisource and write it to JSON files.

Usage (run from repo root):
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py --book39 1Samuel
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py --section6 SifEm
"""

import argparse

import requests

import main_parse_ws
from py_misc import my_utils_for_mainish as my_utils_fm
from py_misc import get_wikisource_plan as wsplan
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import file_io


def _download_chapter(out_book_contents, chapter_plan):
    he_chnu, title = chapter_plan
    params = {"title": title, "action": "raw"}
    user_page = "https://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Bdenckla"
    headers = {"User-Agent": f"Denckla-Dowload-MAM-Bot/1.1 ({user_page})"}
    index_php = "https://he.wikisource.org/w/index.php"
    get_result = requests.get(index_php, params=params, headers=headers)
    out_book_contents[he_chnu] = get_result.text.splitlines()


def _write_book(book_contents, out_path, he_bn_sbn):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
    out_path = mbkn_a_sbkn.wikisource_book_path_fr_bk39id(out_path, bk39id)
    my_utils_fm.show_progress_g(__file__, out_path)
    file_io.json_dump_to_file_path(book_contents, out_path)


def _download_book(book_plan, out_path):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    book_contents = {}
    for chapter_plan in wsplan.get_chapter_plans(book_plan):
        _download_chapter(book_contents, chapter_plan)
    he_bn_sbn, _he_chnus = book_plan
    _write_book(book_contents, out_path, he_bn_sbn)


def main():
    """Download MAM chapters from Hebrew Wikisource"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--book39")  # e.g. 1Samuel not I Samuel
    parser.add_argument("--section6")  # e.g. SifEm
    args = parser.parse_args()
    book_plans = wsplan.get_book_plans(args.book39, args.section6)
    for book_plan in book_plans:
        _download_book(book_plan, _OUT_PATH)
    main_parse_ws.almost_main()


_OUT_PATH = "in/mam-ws"


if __name__ == "__main__":
    main()
