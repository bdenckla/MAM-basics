"""Create the base chapters of Miqra Mevoar on Hebrew Wikisource through the bot account.

Usage (run from the repository root):
    .venv/Scripts/python.exe py/main_ws_bot.py miqra-mevoar --book yehoshua --chapters 1-2 --no-save -dir:path/to/.pywikibot
    .venv/Scripts/python.exe py/main_ws_bot.py miqra-mevoar --book yehoshua --chapters 1-2 --summary "..." -dir:path/to/.pywikibot

Each selected chapter's page is generated from the tracked JSON, in/miqra-mevoar/, by the
converter's own function, py/miqra_mevoar/wikitext.py's chapter_wikitext, and compared
with the live page. The chapter then has one of four outcomes:
  create     the page does not exist. It is saved with createonly, so that a page someone
             else made in the meantime is not overwritten.
  unchanged  the live text equals the generated text. Nothing is done.
  update     the texts differ and every revision of the page is BDencklaBot's. It is
             saved with nocreate.
  refuse     the texts differ and someone else has edited the page. Nothing is saved for
             it; the run lists the page with the other editors' revisions and exits
             non-zero when it ends. People, not the bot, reconcile a revision from Rabbi
             Kokhav with an edit made on Wikisource.

Every run writes each generated page to its pages/ directory and each chapter's outcome
to misc/outcomes.json. `--no-save` saves nothing and, like the other modes' dry runs,
exits non-zero if any page would be created or updated. A saving run then reads each
saved page again from the API, uncached, by its new revision id, requires its bytes to
equal the generated text's, records each page's old and new revision ids and its diff
link in misc/saved-pages.json, and exits non-zero on any mismatch. No MAM page changes,
so there is no post-run download. Each run's artifacts go to a fresh directory under
.novc/mam-ws-bot-miqra-mevoar-runs/.
"""

import os
import re
import time
from datetime import datetime

import pywikibot

from mb_cmn import file_io
from mb_cmn import polite_download
from mb_cmn.he_wikisource_url import he_diff_url
from mb_cmn.new_york_time import NEW_YORK
from mb_misc import my_utils_for_mainish as my_utils_fm
from miqra_mevoar import books
from miqra_mevoar import tracked
from miqra_mevoar import wikitext
from subcommands import ws_bot_real
from ws import ws_revision_api


def run(stems, chapter_range, pywikibot_args, summary=None, no_save=False):
    """Create or update the selected chapters' pages, saving nothing if no_save."""
    ws_bot_real.assert_pywikibot_dir_configured(pywikibot_args)
    if not no_save and not summary:
        raise SystemExit("A saving run needs --summary")
    selected = _selected_chapters(stems, chapter_range)
    run_root = os.path.join(_RUNS_ROOT, datetime.now(NEW_YORK).strftime(_STAMP))
    my_utils_fm.show_progress_g(__file__, "run-artifacts", run_root)
    site = pywikibot.Site("he", "wikisource", "BDencklaBot")
    outcomes, saved, texts, failures = [], [], {}, []
    try:
        for book, chapter in selected:
            title = wikitext.page_title(book, chapter["chapter"])
            texts[title] = wikitext.chapter_wikitext(chapter)
            _write_text_file(run_root, "pages", book.stem, chapter, texts[title])
            page = pywikibot.Page(site, title)
            outcome, others = _outcome(page, texts[title])
            outcomes.append(
                {
                    "stem": book.stem,
                    "chapter": chapter["chapter"],
                    "title": title,
                    "outcome": outcome,
                    "other-revisions": others,
                }
            )
            print(f"{outcome:<9} {title}")
            if no_save or outcome in ("unchanged", "refuse"):
                continue
            try:
                saved.append(_save(page, title, texts[title], outcome, summary))
            except pywikibot.exceptions.Error as error:
                failures.append(f"{title}: the save failed: {error!r}")
                break
    finally:
        file_io.json_dump_to_file_path(
            outcomes, os.path.join(run_root, "misc", "outcomes.json")
        )
        if saved:
            failures.extend(_verify(saved, texts))
        file_io.json_dump_to_file_path(
            saved, os.path.join(run_root, "misc", "saved-pages.json")
        )
    _exit_if_any(outcomes, failures, no_save)


def _selected_chapters(stems, chapter_range):
    """(book, chapter record) for each selected chapter, in the order selected."""
    if len(set(stems)) != len(stems):
        raise SystemExit(f"A --book is given twice: {stems}")
    if chapter_range is not None and len(stems) != 1:
        raise SystemExit("--chapters selects chapters of one --book only")
    if unknown := sorted(set(stems) - set(books.BOOKS)):
        raise SystemExit(f"No --book {unknown}; the books are {sorted(books.BOOKS)}")
    selected = []
    for stem in stems:
        book = books.book_of_stem(stem)
        chapters = tracked.read_record(book)["chapters"]
        if chapter_range is not None:
            first, last = _range(chapter_range, len(chapters))
            chapters = chapters[first - 1 : last]
        selected.extend((book, chapter) for chapter in chapters)
    return selected


def _range(text, count):
    match = re.fullmatch(r"([0-9]+)-([0-9]+)", text)
    if match is None:
        raise SystemExit(f"--chapters takes FIRST-LAST, not {text!r}")
    first, last = int(match.group(1)), int(match.group(2))
    if not 1 <= first <= last <= count:
        raise SystemExit(f"--chapters {text} is not within the book's {count} chapters")
    return first, last


def _outcome(page, text):
    """The chapter's outcome, and the revisions of editors other than the bot."""
    if not page.exists():
        return "create", []
    if page.text == text:
        return "unchanged", []
    others = [
        {
            "revid": revision.revid,
            "user": revision.user,
            "timestamp": revision.timestamp.isoformat(),
        }
        for revision in page.revisions()
        if revision.user != _BOT
    ]
    return ("refuse", others) if others else ("update", [])


def _save(page, title, text, outcome, summary):
    oldrevid = None if outcome == "create" else page.latest_revision_id
    page.text = text
    # Whatever pywikibot's configuration says, the text goes out exactly as generated.
    page.save(
        summary,
        minor=False,
        apply_cosmetic_changes=False,
        createonly=outcome == "create",
        nocreate=outcome == "update",
    )
    newrevid = page.latest_revision_id
    return {
        "title": title,
        "outcome": outcome,
        "pageid": page.pageid,
        "oldrevid": oldrevid,
        "newrevid": newrevid,
        "diff": he_diff_url(title, newrevid, "prev" if oldrevid is None else oldrevid),
        "verified": False,
    }


def _verify(saved, texts):
    """Read each saved revision through the API, uncached; mark it verified or fail."""
    failures = []
    with polite_download.PoliteDownloader(_CHECK_CONFIG) as downloader:
        client = ws_revision_api.ChapterClient(downloader, _API_PHP)
        for record in saved:
            identity = {
                "requested_title": record["title"],
                "resolved_title": record["title"],
                "page_id": record["pageid"],
                "revision_id": record["newrevid"],
            }
            try:
                content = _saved_content(client, identity)
            except ws_revision_api.ChapterResponseError as error:
                failures.append(
                    f"{record['title']}: no saved revision to read: {error}"
                )
                continue
            if content == texts[record["title"]].encode("utf-8"):
                record["verified"] = True
            else:
                failures.append(
                    f"{record['title']}: the saved text is not the text sent"
                )
    return failures


def _saved_content(client, identity):
    """The saved revision's bytes, waiting out a replica that has not yet seen it."""
    for wait_s in _REREAD_WAITS_S:
        try:
            _identity, revision = client.by_raw_revisions([identity])[
                identity["requested_title"]
            ]
            return revision["content"]
        except ws_revision_api.ChapterResponseError:
            if wait_s is None:
                raise
            time.sleep(wait_s)
    raise AssertionError("unreachable")


def _exit_if_any(outcomes, failures, no_save):
    refused = [entry for entry in outcomes if entry["outcome"] == "refuse"]
    lines = [f"- {line}" for line in failures]
    for entry in refused:
        lines.append(f"- refused, edited by others: {entry['title']}")
        lines.extend(
            f"    revision {revision['revid']} by {revision['user'] or '(hidden)'}"
            f" at {revision['timestamp']}"
            for revision in entry["other-revisions"]
        )
    if no_save:
        lines.extend(
            f"- would {entry['outcome']}: {entry['title']}"
            for entry in outcomes
            if entry["outcome"] in ("create", "update")
        )
    if lines:
        raise SystemExit("miqra-mevoar run found pages to report:\n" + "\n".join(lines))


def _write_text_file(run_root, sub_dir, stem, chapter, text):
    path = os.path.join(run_root, sub_dir, stem, f"{chapter['chapter']:02d}.wiki")
    my_utils_fm.show_progress_g(__file__, path)
    file_io.with_tmp_openw(path, {}, _write_text, text)


def _write_text(text, outfp):
    outfp.write(text)


_BOT = "BDencklaBot"
_RUNS_ROOT = ".novc/mam-ws-bot-miqra-mevoar-runs"
_STAMP = "%Y%m%d-%H%M%S-%f%z"
_API_PHP = "https://he.wikisource.org/w/api.php"
# The waits before each further read of a saved revision; None ends the reads.
_REREAD_WAITS_S = (5.0, 10.0, 20.0, None)
_CHECK_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent="MAM-basics Miqra Mevoar bot check (https://github.com/bdenckla/MAM-basics)",
    throttle=polite_download.ThrottleConfig(min_delay_s=1.5),
)
