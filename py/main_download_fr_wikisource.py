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


def _download_chapter_batch(chapter_plans, downloader):
    titles_to_he_chnus = {title: he_chnu for he_chnu, title in chapter_plans}
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "maxlag": 1,
        "prop": "revisions",
        "redirects": 1,
        "rvprop": "content",
        "rvslots": "main",
        "titles": "|".join(titles_to_he_chnus),
    }
    response_json = downloader.get_json(_WIKISOURCE_API_PHP, params=params)
    return _chapter_lines_from_response_json(response_json, chapter_plans)


def _chapter_lines_from_response_json(response_json, chapter_plans):
    query = response_json.get("query")
    assert query is not None, response_json
    assert "error" not in response_json, response_json["error"]
    alias_to_requested_title = _alias_to_requested_title(query, chapter_plans)
    pages = query.get("pages")
    assert isinstance(pages, list), response_json
    requested_titles_to_lines = {}
    for page in pages:
        assert "missing" not in page, page
        page_title = page["title"]
        requested_title = alias_to_requested_title.get(page_title)
        assert requested_title is not None, page
        assert requested_title not in requested_titles_to_lines, page
        requested_titles_to_lines[requested_title] = _lines_of_page(page)
    chapter_lines = {}
    for he_chnu, requested_title in chapter_plans:
        assert requested_title in requested_titles_to_lines, requested_title
        chapter_lines[he_chnu] = requested_titles_to_lines[requested_title]
    return chapter_lines


def _alias_to_requested_title(query, chapter_plans):
    alias_to_requested_title = {title: title for _he_chnu, title in chapter_plans}
    for normalized in query.get("normalized", []):
        _add_title_alias(alias_to_requested_title, normalized["from"], normalized["to"])
    for redirect in query.get("redirects", []):
        _add_title_alias(alias_to_requested_title, redirect["from"], redirect["to"])
    return alias_to_requested_title


def _add_title_alias(alias_to_requested_title, from_title, to_title):
    requested_title = alias_to_requested_title.get(from_title)
    assert requested_title is not None, from_title
    existing_requested_title = alias_to_requested_title.get(to_title)
    assert existing_requested_title in (None, requested_title), to_title
    alias_to_requested_title[to_title] = requested_title


def _lines_of_page(page):
    revisions = page.get("revisions")
    assert revisions, page
    main_slot = revisions[0]["slots"]["main"]
    content = main_slot.get("content")
    assert content is not None, page
    return content.splitlines()


def _chapter_plan_batches(book_plan):
    chapter_plans = list(wsplan.get_chapter_plans(book_plan))
    batch_size = _MAX_TITLES_PER_REQUEST
    return [
        chapter_plans[i : i + batch_size]
        for i in range(0, len(chapter_plans), batch_size)
    ]


def _write_book(book_contents, out_path, he_bn_sbn):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
    out_path = mbkn_a_sbkn.wikisource_book_path_fr_bk39id(out_path, bk39id)
    my_utils_fm.show_progress_g(__file__, out_path)
    file_io.json_dump_to_file_path(book_contents, out_path)


def _download_book(book_plan, out_path, downloader):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    book_contents = {}
    for chapter_plans in _chapter_plan_batches(book_plan):
        book_contents.update(_download_chapter_batch(chapter_plans, downloader))
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
_MAX_TITLES_PER_REQUEST = 20
_WIKISOURCE_API_PHP = "https://he.wikisource.org/w/api.php"
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
