import pywikibot

from py_misc import my_utils_for_mainish as my_utils_fm
from py_misc import get_wikisource_plan as wsplan
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import bib_locales as tbn
from pycmn import file_io
from pyws import ws_bot_edit as wbe


def main():
    """Use a bot to process chapters of Hebrew Wikisource"""
    site = pywikibot.Site("he", "wikisource", "BDencklaBot")
    summary = ""  # commit this empty to force filling in when run
    assert summary
    botctx = {
        "botctx-site": site,
        "botctx-summary": summary,
    }
    book_plans = wsplan.get_book_plans()
    for book_plan in book_plans:
        _run_bot_on_book(botctx, book_plan)


def _run_bot_on_chapter(botctx, out_book_contents, chapter_plan):
    he_chnu, title = chapter_plan
    site = botctx["botctx-site"]
    summary = botctx["botctx-summary"]
    page = pywikibot.Page(site, title)
    orig_text = page.text
    page.text = wbe.edit_page_text(he_chnu, page.text)
    if page.text != orig_text:
        page.save(summary)
    out_book_contents[he_chnu] = page.text.splitlines()


def _write_book(book_contents, he_bn_sbn):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
    osdf = tbn.ordered_short_dash_full_39(bk39id)
    out_path = f"out/mam-ws-bot/{osdf}.json"
    my_utils_fm.show_progress_g(__file__, out_path)
    file_io.json_dump_to_file_path(book_contents, out_path)


def _run_bot_on_book(botctx, book_plan):
    book_contents = {}
    for chapter_plan in wsplan.get_chapter_plans(book_plan):
        _run_bot_on_chapter(botctx, book_contents, chapter_plan)
    he_bn_sbn, _he_chnus = book_plan
    _write_book(book_contents, he_bn_sbn)


if __name__ == "__main__":
    main()
