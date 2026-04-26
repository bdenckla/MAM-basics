"""
Edit Hebrew Wikisource pages using a pywikibot-based automation bot.

Usage (run from repo root):
    .venv/Scripts/python.exe py/main_ws_bot.py --edits path.json -dir:path/to/.pywikibot
    $env:PYWIKIBOT_DIR="$env:USERPROFILE/.pywikibot"; .venv/Scripts/python.exe py/main_ws_bot.py --edits path.json
    .venv/Scripts/python.exe py/main_ws_bot.py --edits path.json -dir:... --book39 Deuter
    .venv/Scripts/python.exe py/main_ws_bot.py --edits path.json -dir:... --section6 SifEm
"""

import argparse
import os

import pywikibot

from py_misc import my_utils_for_mainish as my_utils_fm
from py_misc import get_wikisource_plan as wsplan
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import bib_locales as tbn
from pycmn import file_io
from ws import ws_bot_edit as wbe
from ws import ws_download_selector as wsds


def main():
    """Use a bot to process chapters of Hebrew Wikisource"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--edits", required=True)  # path to JSON edit spec
    wsds.add_selector_opts(parser)
    args, pywikibot_args = parser.parse_known_args()
    wsds.validate_selector_args(args, parser)
    _assert_pywikibot_dir_configured(parser, pywikibot_args)
    edits_ctx = wbe.load_edits(args.edits)
    summary = edits_ctx["summary"]
    assert summary
    site = pywikibot.Site("he", "wikisource", "BDencklaBot")
    botctx = {
        "botctx-site": site,
        "botctx-summary": summary,
        "botctx-edits-ctx": edits_ctx,
    }
    book_plans = wsds.selected_book_plans(args)
    for book_plan in book_plans:
        _run_bot_on_book(botctx, book_plan)
    wbe.write_warnings(edits_ctx, _OUT_PATH_WARNINGS)
    wbe.write_modified_chapters(edits_ctx, _OUT_PATH_MODIFIED_CHAPTERS)


def _run_bot_on_chapter(botctx, bk39id, out_book_contents, chapter_plan):
    he_chnu, title = chapter_plan
    site = botctx["botctx-site"]
    summary = botctx["botctx-summary"]
    edits_ctx = botctx["botctx-edits-ctx"]
    page = pywikibot.Page(site, title)
    orig_text = page.text
    page.text = wbe.edit_page_text(edits_ctx, bk39id, he_chnu, page.text)
    if page.text != orig_text:
        edits_ctx["modified-chapters"].append((bk39id, he_chnu))
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


def _assert_pywikibot_dir_configured(parser, pywikibot_args):
    pywikibot_dir = _resolve_pywikibot_dir(pywikibot_args)
    if not pywikibot_dir:
        parser.error(
            "Missing pywikibot config directory. Pass -dir:<path-to-.pywikibot> "
            "or set PYWIKIBOT_DIR. See py/ws/pywikibot-setup.md"
        )
    _assert_pywikibot_auth_files_present(parser, pywikibot_dir)


def _has_dir_arg(pywikibot_args):
    return _dir_from_pywikibot_args(pywikibot_args) is not None


def _has_pywikibot_dir_env():
    return bool(os.environ.get("PYWIKIBOT_DIR")) or bool(
        os.environ.get("PYWIKIBOT_DIR_PWB")
    )


def _resolve_pywikibot_dir(pywikibot_args):
    dir_arg = _dir_from_pywikibot_args(pywikibot_args)
    if dir_arg:
        return _normalize_path(dir_arg)
    env_dir = os.environ.get("PYWIKIBOT_DIR")
    if env_dir:
        return _normalize_path(env_dir)
    env_dir_pwb = os.environ.get("PYWIKIBOT_DIR_PWB")
    if env_dir_pwb:
        return _normalize_path(env_dir_pwb)
    return None


def _dir_from_pywikibot_args(pywikibot_args):
    for idx, arg in enumerate(pywikibot_args):
        if arg.startswith("-dir:"):
            return arg.split(":", 1)[1]
        if arg == "-dir" and idx + 1 < len(pywikibot_args):
            return pywikibot_args[idx + 1]
    return None


def _normalize_path(path):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


def _assert_pywikibot_auth_files_present(parser, pywikibot_dir):
    user_config_path = os.path.join(pywikibot_dir, "user-config.py")
    password_path = os.path.join(pywikibot_dir, "password.py")
    if not os.path.isfile(user_config_path):
        parser.error(f"Missing {user_config_path}. See py/ws/pywikibot-setup.md")
    if not os.path.isfile(password_path):
        parser.error(f"Missing {password_path}. See py/ws/pywikibot-setup.md")


_OUT_PATH_MISC = "out/mam-ws-bot-misc"
_OUT_PATH_WARNINGS = f"{_OUT_PATH_MISC}/warnings.json"
_OUT_PATH_MODIFIED_CHAPTERS = f"{_OUT_PATH_MISC}/modified-chapters.json"


if __name__ == "__main__":
    main()
