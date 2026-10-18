"""Edit pages of MAM's introduction on Hebrew Wikisource through the bot account.

Usage (run from the repository root):
    .venv/Scripts/python.exe py/main_ws_bot.py intro --edits path.json -dir:path/to/.pywikibot --no-save
    .venv/Scripts/python.exe py/main_ws_bot.py intro --edits path.json -dir:path/to/.pywikibot

The chapter bot, `main_ws_bot.py real`, selects chapters by book. This bot edits the
introduction's pages, which in/mam-ws-intro/manifest.json names by key. Its edit file
has three keys:
  "summary"   : the Wikisource edit summary
  "edit-kind" : "explicit-replacement", its only kind
  "pages"     : a dict mapping a page key to a list of edit objects, each with
                "old", which must occur exactly once in the page, "new", and an
                optional "comment"

`--no-save` fetches every page the file names, applies its edits in memory, writes the
result to the run's pages/ directory and saves nothing. Like the chapter bot's dry run,
it then exits non-zero, listing each page that a save would change. A saving run saves
each changed page and then refreshes the introduction's mirror, as
`py/main_download.py fr-ws-intro` does, unless `--no-post-download` is given. Each run
writes its artifacts to a fresh directory under .novc/mam-ws-bot-intro-runs/.
"""

import json
import os
from datetime import datetime

import pywikibot

from mb_cmn import file_io
from mb_cmn.he_wikisource_url import he_diff_url
from mb_cmn.new_york_time import NEW_YORK
from mb_misc import my_utils_for_mainish as my_utils_fm
from subcommands import download_wikisource_intro
from subcommands import ws_bot_real


def run(edits_path, pywikibot_args, post_download=True, no_save=False):
    """Apply an introduction edit file, saving every changed page unless no_save."""
    ws_bot_real.assert_pywikibot_dir_configured(pywikibot_args)
    with open(edits_path, "r", encoding="utf-8") as edits_fp:
        spec = json.load(edits_fp)
    if spec["edit-kind"] != "explicit-replacement":
        raise SystemExit(f"Unknown introduction edit kind: {spec['edit-kind']!r}")
    summary = spec["summary"]
    assert summary
    titles = {
        key: page["title"]
        for key, page in download_wikisource_intro.read_manifest()["pages"].items()
    }
    if unknown := sorted(set(spec["pages"]) - set(titles)):
        raise SystemExit(f"The edit file names no introduction page {unknown}")
    run_root = os.path.join(_RUNS_ROOT, datetime.now(NEW_YORK).strftime(_STAMP))
    my_utils_fm.show_progress_g(__file__, "run-artifacts", run_root)
    site = pywikibot.Site("he", "wikisource", "BDencklaBot")
    changed, saved = [], []
    for key, edits in spec["pages"].items():
        page = pywikibot.Page(site, titles[key])
        old_text = page.text
        new_text = _edited(key, old_text, edits)
        _write_page(run_root, key, new_text)
        if new_text == old_text:
            continue
        changed.append(key)
        if no_save:
            continue
        oldrevid = page.latest_revision_id
        assert oldrevid is not None, titles[key]
        page.text = new_text
        page.save(summary)
        saved.append(
            {
                "key": key,
                "title": titles[key],
                "oldrevid": oldrevid,
                "diff": he_diff_url(titles[key], "next", oldrevid),
            }
        )
    file_io.json_dump_to_file_path(
        saved, os.path.join(run_root, "misc", "saved-pages.json")
    )
    if no_save and changed:
        raise SystemExit(
            "no-save run found pages that would change:\n"
            + "\n".join(f"- {key} ({titles[key]})" for key in changed)
        )
    if saved and post_download:
        download_wikisource_intro.run()


def _edited(key, text, edits):
    for edit in edits:
        count = text.count(edit["old"])
        assert (
            count == 1
        ), f"Expected 1 occurrence of {edit['old']!r} in {key}, found {count}"
        text = text.replace(edit["old"], edit["new"])
    return text


def _write_page(run_root, key, text):
    path = os.path.join(run_root, "pages", f"{key}.mediawiki")
    my_utils_fm.show_progress_g(__file__, path)
    file_io.with_tmp_openw(path, {}, _write_text, text)


def _write_text(text, outfp):
    outfp.write(text)


_RUNS_ROOT = ".novc/mam-ws-bot-intro-runs"
_STAMP = "%Y%m%d-%H%M%S-%f%z"
