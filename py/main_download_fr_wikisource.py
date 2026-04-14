"""
Download MAM data from Hebrew Wikisource and write it to JSON files.

Usage (run from repo root):
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py --book39 1Samuel
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py --section6 SifEm
"""

import argparse

import main_parse_ws
from py_misc import my_utils_for_mainish as my_utils_fm
from py_misc import get_wikisource_plan as wsplan
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import file_io
from pycmn import polite_download


def _download_chapter(out_book_contents, chapter_plan, downloader):
    he_chnu, title = chapter_plan
    params = {"title": title, "action": "raw"}
    text = downloader.get_text(_WIKISOURCE_INDEX_PHP, params=params)
    out_book_contents[he_chnu] = text.splitlines()


def _write_book(book_contents, out_path, he_bn_sbn):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
    out_path = mbkn_a_sbkn.wikisource_book_path_fr_bk39id(out_path, bk39id)
    my_utils_fm.show_progress_g(__file__, out_path)
    file_io.json_dump_to_file_path(book_contents, out_path)


def _download_book(book_plan, out_path, downloader):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    book_contents = {}
    for chapter_plan in wsplan.get_chapter_plans(book_plan):
        _download_chapter(book_contents, chapter_plan, downloader)
    he_bn_sbn, _he_chnus = book_plan
    _write_book(book_contents, out_path, he_bn_sbn)


def main():
    """Download MAM chapters from Hebrew Wikisource"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--book39")  # e.g. 1Samuel not I Samuel
    parser.add_argument("--section6")  # e.g. SifEm
    args = parser.parse_args()
    book_plans = wsplan.get_book_plans(args.book39, args.section6)
    with polite_download.PoliteDownloader(_WIKISOURCE_DOWNLOAD_CONFIG) as downloader:
        for book_plan in book_plans:
            _download_book(book_plan, _OUT_PATH, downloader)
    main_parse_ws.almost_main()


_OUT_PATH = "in/mam-ws"
_WIKISOURCE_USER_PAGE = (
    "https://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Bdenckla"
)
_WIKISOURCE_INDEX_PHP = "https://he.wikisource.org/w/index.php"
_WIKISOURCE_DOWNLOAD_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent=f"Denckla-Dowload-MAM-Bot/1.1 ({_WIKISOURCE_USER_PAGE})",
    default_timeout_s=30.0,
    throttle=polite_download.ThrottleConfig(min_delay_s=1.5, mean_delay_s=3.0),
    retry=polite_download.RetryConfig(max_attempts=4),
    cache=polite_download.CacheConfig(dir_path=".novc/http-cache/wikisource"),
    obey_robots_txt=False,
)


if __name__ == "__main__":
    main()
