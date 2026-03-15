"""
Edit Hebrew Wikisource pages using a pywikibot-based automation bot.

Usage (run from repo root):
    .venv/Scripts/python.exe py/main_ws_bot.py --edits path.json -dir:path/to/.pywikibot
    .venv/Scripts/python.exe py/main_ws_bot.py --edits path.json -dir:... --book39 Deuter
    .venv/Scripts/python.exe py/main_ws_bot.py --edits path.json -dir:... --section6 SifEm
"""

import argparse

import pywikibot

from py_misc import my_utils_for_mainish as my_utils_fm
from py_misc import get_wikisource_plan as wsplan
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import bib_locales as tbn
from pycmn import file_io
from pyws import ws_bot_edit as wbe


def main():
    """Use a bot to process chapters of Hebrew Wikisource"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--edits", required=True)  # path to JSON edit spec
    parser.add_argument("--book39")  # e.g. Deuter, Joshua (not I Samuel)
    parser.add_argument("--section6")  # e.g. SifEm
    args, _pywikibot_args = parser.parse_known_args()
    edits_ctx = wbe.load_edits(args.edits)
    summary = edits_ctx["summary"]
    assert summary
    site = pywikibot.Site("he", "wikisource", "BDencklaBot")
    botctx = {
        "botctx-site": site,
        "botctx-summary": summary,
        "botctx-edits-ctx": edits_ctx,
    }
    book_plans = wsplan.get_book_plans(args.book39, args.section6)
    for book_plan in book_plans:
        _run_bot_on_book(botctx, book_plan)


def _run_bot_on_chapter(botctx, bk39id, out_book_contents, chapter_plan):
    he_chnu, title = chapter_plan
    site = botctx["botctx-site"]
    summary = botctx["botctx-summary"]
    edits_ctx = botctx["botctx-edits-ctx"]
    page = pywikibot.Page(site, title)
    orig_text = page.text
    page.text = wbe.edit_page_text(edits_ctx, bk39id, he_chnu, page.text)
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
    he_bn_sbn, _he_chnus = book_plan
    bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
    book_contents = {}
    for chapter_plan in wsplan.get_chapter_plans(book_plan):
        _run_bot_on_chapter(botctx, bk39id, book_contents, chapter_plan)
    _write_book(book_contents, he_bn_sbn)


if __name__ == "__main__":
    main()
