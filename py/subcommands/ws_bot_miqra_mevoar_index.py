"""Complete Miqra Mevoar's base-chapter index on Hebrew Wikisource through the bot account.

Usage (run from the repository root):
    .venv/Scripts/python.exe py/main_ws_bot.py miqra-mevoar-index --no-save -dir:path/to/.pywikibot
    .venv/Scripts/python.exe py/main_ws_bot.py miqra-mevoar-index --base-revid <revision id> --summary "..." -dir:path/to/.pywikibot

Every run reads the index, מקרא מבואר/פרקי בסיס, at its latest revision through the API,
uncached and byte for byte, and generates the new text from it with
py/miqra_mevoar/index_page.py's page_text: the framing and the category line keep their
bytes, and the book sections link every chapter that MAM-simple has. The run writes the
old text, the new text and their unified diff to old.wiki, new.wiki and index.diff, and
the base revision's facts to misc/index-run.json, in a fresh directory under
.novc/mam-ws-bot-miqra-mevoar-index-runs/. It prints the base revision id and the number
of links.

`--no-save` saves nothing and, like the other modes' dry runs, exits non-zero if the
index would change. A saving run needs `--base-revid`, the revision whose diff was
reviewed, and `--summary`. It refuses unless that revision is still the index's latest.
It saves with nocreate, giving that revision as baserevid and its time as basetimestamp,
so that an edit made since then makes MediaWiki detect a conflict. It then reads the
saved revision back through the API, uncached, requires its bytes to equal the generated
text's, records the old and new revision ids and the diff link in misc/saved-pages.json,
and exits non-zero on a mismatch. No MAM page changes, so there is no post-run download.
"""

import difflib
import os
import time
from datetime import datetime

import pywikibot

from mb_cmn import file_io
from mb_cmn import polite_download
from mb_cmn.he_wikisource_url import he_diff_url
from mb_cmn.new_york_time import NEW_YORK
from mb_misc import my_utils_for_mainish as my_utils_fm
from miqra_mevoar import index_page
from miqra_mevoar import wikitext
from subcommands import ws_bot_real
from ws import ws_revision_api


def run(pywikibot_args, base_revid=None, summary=None, no_save=False):
    """Complete the index from its latest revision, saving nothing if no_save."""
    ws_bot_real.assert_pywikibot_dir_configured(pywikibot_args)
    if not no_save and (base_revid is None or not summary):
        raise SystemExit("A saving run needs --base-revid and --summary")
    run_root = os.path.join(_RUNS_ROOT, datetime.now(NEW_YORK).strftime(_STAMP))
    my_utils_fm.show_progress_g(__file__, "run-artifacts", run_root)
    identity, base = _latest_revision()
    old_text = base["content"].decode("utf-8")
    new_text = index_page.page_text(old_text)
    facts = _facts(identity, base, old_text, new_text)
    _write_artifacts(run_root, old_text, new_text, facts)
    print(
        f"base revision {facts['base-revid']} of {facts['base-timestamp']};"
        f" {facts['new-links']} links in {facts['new-sections']} sections, against"
        f" {facts['old-links']} in {facts['old-sections']}; diff +{facts['diff-added']}"
        f" -{facts['diff-removed']} lines, {facts['old-bytes']} to {facts['new-bytes']}"
        " bytes"
    )
    if new_text == old_text:
        print(f"unchanged {wikitext.INDEX_TITLE}")
        return
    if no_save:
        raise SystemExit(
            f"miqra-mevoar-index run found that the index would change: {run_root}"
        )
    if facts["base-revid"] != base_revid:
        raise SystemExit(
            f"Refused: the index's latest revision is {facts['base-revid']},"
            f" not --base-revid {base_revid}"
        )
    saved = _save(identity, base, new_text, summary)
    saved_path = os.path.join(run_root, "misc", "saved-pages.json")
    # Preserve known saved revision IDs if verification raises.
    file_io.json_dump_to_file_path([saved], saved_path)
    failure = _verify(saved, new_text)
    file_io.json_dump_to_file_path([saved], saved_path)
    print(f"saved revision {saved['newrevid']}: {saved['diff']}")
    if failure is not None:
        raise SystemExit(f"miqra-mevoar-index run: {wikitext.INDEX_TITLE}: {failure}")


def _latest_revision():
    """The index's identity and its latest revision, its content as exact bytes."""
    title = wikitext.INDEX_TITLE
    with polite_download.PoliteDownloader(_CHECK_CONFIG) as downloader:
        client = ws_revision_api.ChapterClient(downloader, _API_PHP)
        identity, _lines = client.by_titles([title], content=False)[title]
        if identity["resolved_title"] != title:
            raise SystemExit(f"{title} resolves to {identity['resolved_title']}")
        _identity, revision = client.by_raw_revisions([identity])[title]
    return identity, revision


def _facts(identity, base, old_text, new_text):
    old_sections = index_page.page_sections(old_text)
    new_sections = index_page.page_sections(new_text)
    diff = _diff_lines(old_text, new_text)
    return {
        "title": wikitext.INDEX_TITLE,
        "pageid": identity["page_id"],
        "base-revid": base["revision_id"],
        "base-timestamp": base["revision_timestamp"],
        "old-bytes": base["byte_size"],
        "new-bytes": len(new_text.encode("utf-8")),
        "old-sections": len(old_sections),
        "new-sections": len(new_sections),
        "old-links": _link_count(old_sections),
        "new-links": _link_count(new_sections),
        "diff-added": sum(1 for line in diff[2:] if line.startswith("+")),
        "diff-removed": sum(1 for line in diff[2:] if line.startswith("-")),
    }


def _link_count(book_sections):
    return sum(len(part.links) for section in book_sections for part in section.runs)


def _diff_lines(old_text, new_text):
    return list(
        difflib.unified_diff(
            old_text.split("\n"),
            new_text.split("\n"),
            "old.wiki",
            "new.wiki",
            lineterm="",
        )
    )


def _write_artifacts(run_root, old_text, new_text, facts):
    for name, text in (
        ("old.wiki", old_text),
        ("new.wiki", new_text),
        (
            "index.diff",
            "".join(f"{line}\n" for line in _diff_lines(old_text, new_text)),
        ),
    ):
        path = os.path.join(run_root, name)
        my_utils_fm.show_progress_g(__file__, path)
        file_io.with_tmp_openw(path, {}, _write_text, text)
    file_io.json_dump_to_file_path(
        facts, os.path.join(run_root, "misc", "index-run.json")
    )


def _write_text(text, outfp):
    outfp.write(text)


def _save(identity, base, text, summary):
    site = pywikibot.Site("he", "wikisource", "BDencklaBot")
    page = pywikibot.Page(site, wikitext.INDEX_TITLE)
    page.text = text
    # Whatever pywikibot's configuration says, the text goes out exactly as generated,
    # and the guards stay tied to the revision whose diff was reviewed, not to one that
    # pywikibot may fetch while building its request.
    page.save(
        summary,
        minor=False,
        apply_cosmetic_changes=False,
        nocreate=True,
        baserevid=base["revision_id"],
        basetimestamp=base["revision_timestamp"],
    )
    newrevid = page.latest_revision_id
    return {
        "title": wikitext.INDEX_TITLE,
        "outcome": "update",
        "pageid": identity["page_id"],
        "oldrevid": base["revision_id"],
        "newrevid": newrevid,
        "diff": he_diff_url(wikitext.INDEX_TITLE, newrevid, base["revision_id"]),
        "verified": False,
    }


def _verify(record, text):
    """Read the saved revision through the API, uncached; mark it verified or say why not."""
    identity = {
        "requested_title": record["title"],
        "resolved_title": record["title"],
        "page_id": record["pageid"],
        "revision_id": record["newrevid"],
    }
    with polite_download.PoliteDownloader(_CHECK_CONFIG) as downloader:
        client = ws_revision_api.ChapterClient(downloader, _API_PHP)
        # The waits before each further read of the saved revision, in case a replica
        # has not yet seen it; None ends the reads.
        for wait_s in _REREAD_WAITS_S:
            try:
                _identity, revision = client.by_raw_revisions([identity])[
                    record["title"]
                ]
                break
            except ws_revision_api.ChapterResponseError as error:
                if wait_s is None:
                    return f"no saved revision to read: {error}"
                time.sleep(wait_s)
    if revision["content"] != text.encode("utf-8"):
        return "the saved text is not the text sent"
    record["verified"] = True
    return None


_RUNS_ROOT = ".novc/mam-ws-bot-miqra-mevoar-index-runs"
_STAMP = "%Y%m%d-%H%M%S-%f%z"
_API_PHP = "https://he.wikisource.org/w/api.php"
_REREAD_WAITS_S = (5.0, 10.0, 20.0, None)
_CHECK_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent="MAM-basics Miqra Mevoar bot check (https://github.com/bdenckla/MAM-basics)",
    throttle=polite_download.ThrottleConfig(min_delay_s=1.5),
)
