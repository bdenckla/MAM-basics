"""
Download MAM data from Hebrew Wikisource and write it to JSON files.

Usage (run from repo root):
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py --book39 1Samuel
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py --section6 SifEm
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py --book39 Joshua --chapter 11
    .venv/Scripts/python.exe py/main_download_fr_wikisource.py --book-chapters-json path.json
"""

import main_parse_ws
import json
import os
from mb_misc import my_utils_for_mainish as my_utils_fm
from py_misc import get_wikisource_plan as wsplan
from mb_cmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from mb_cmn import file_io
from mb_cmn import polite_download
from ws import ws_download_selector as wsds


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
    book_path = mbkn_a_sbkn.wikisource_book_path_fr_bk39id(out_path, bk39id)
    my_utils_fm.show_progress_g(__file__, book_path)
    file_io.json_dump_to_file_path(book_contents, book_path)


def _full_book_plan(he_bn_sbn):
    bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
    full_book_plans = list(wsplan.get_book_plans(bk39id, None))
    assert len(full_book_plans) == 1, (bk39id, len(full_book_plans))
    return full_book_plans[0]


def _is_partial_book_plan(book_plan):
    he_bn_sbn, requested_he_chnus = book_plan
    _full_he_bn_sbn, full_he_chnus = _full_book_plan(he_bn_sbn)
    return len(requested_he_chnus) != len(full_he_chnus)


def _read_existing_book(book_path):
    with open(book_path, "r", encoding="utf-8") as json_in_fp:
        existing_book = json.load(json_in_fp)
    assert isinstance(existing_book, dict), book_path
    return existing_book


def _merge_book_contents(book_plan, downloaded_book_contents, out_path):
    he_bn_sbn, _requested_he_chnus = book_plan
    _full_he_bn_sbn, full_he_chnus = _full_book_plan(he_bn_sbn)
    bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
    book_path = mbkn_a_sbkn.wikisource_book_path_fr_bk39id(out_path, bk39id)
    assert os.path.exists(book_path), (
        "partial download requires existing full book file",
        book_path,
    )
    merged_book = _read_existing_book(book_path)
    assert set(full_he_chnus).issubset(merged_book), (
        "existing book file is incomplete",
        book_path,
    )
    merged_book.update(downloaded_book_contents)
    return {he_chnu: merged_book[he_chnu] for he_chnu in full_he_chnus}


def _download_book(book_plan, out_path, downloader):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    downloaded_book_contents = {}
    for chapter_plans in _chapter_plan_batches(book_plan):
        downloaded_book_contents.update(
            _download_chapter_batch(chapter_plans, downloader)
        )
    he_bn_sbn, _he_chnus = book_plan
    if _is_partial_book_plan(book_plan):
        book_contents = _merge_book_contents(
            book_plan, downloaded_book_contents, out_path
        )
    else:
        book_contents = downloaded_book_contents
    _write_book(book_contents, out_path, he_bn_sbn)


def main(argv=None):
    """Download MAM chapters from Hebrew Wikisource"""
    args = wsds.parse_args(argv)
    book_plans = wsds.selected_book_plans(args)
    with polite_download.PoliteDownloader(_WIKISOURCE_DOWNLOAD_CONFIG) as downloader:
        for book_plan in book_plans:
            _download_book(book_plan, _OUT_PATH, downloader)
    main_parse_ws.almost_main(wsds.affected_bkids(book_plans))


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
