"""Edit other named pages of MAM on Hebrew Wikisource through the bot account.

Usage (run from the repository root):
    .venv/Scripts/python.exe py/main_ws_bot.py pages --edits path.json -dir:path/to/.pywikibot --no-save
    .venv/Scripts/python.exe py/main_ws_bot.py pages --edits path.json -dir:path/to/.pywikibot

The chapter bot, `main_ws_bot.py real`, selects chapters by book, and `intro` selects the
introduction's pages by their in/mam-ws-intro/manifest.json keys. This bot edits pages
that neither selects, such as the index pages of the Torah, the Prophets and the
Writings, naming each by its exact title. Its edit file has three keys:
  "summary"   : the Wikisource edit summary
  "edit-kind" : "explicit-replacement", its only kind
  "pages"     : a dict mapping a page key, made of lowercase ASCII letters, digits and
                hyphens, to an object with three keys: "title", the page's exact title;
                "base-revid", the revision that its edits were cut from; and "edits", a
                list of edit objects, each with "old", which must occur exactly once in
                the page, "new", and an optional "comment"

It refuses a redirect, a chapter page that in/mam-ws-revisions.json records, which `real`
edits, and an introduction page, which `intro` edits, since each of those modes refreshes
its mirror after a save.

Every run reads each page's latest revision through the API, uncached and byte for byte,
and refuses unless it is the page's "base-revid". It applies the edits to that text and
writes the base and edited texts to the run's base/ and pages/ directories, in a fresh
directory under .novc/mam-ws-bot-pages-runs/. `--no-save` saves nothing and, like the
other modes' dry runs, exits non-zero, listing each page that a save would change. A
saving run saves each changed page with nocreate, giving its base revision as baserevid
and that revision's time as basetimestamp, so that an edit made since makes MediaWiki
detect a conflict. It then reads each saved revision back through the API, uncached,
requires its bytes to equal the edited text's, records each page's old and new revision
ids and its diff link in misc/saved-pages.json, and exits non-zero on any mismatch.

There is no post-run download. A saved page that in/mam-ws-special/manifest.json records
leaves that mirror behind the wiki until `py/main_download.py fr-wikisource` refreshes
it, and the run ends by naming each such page.
"""

import json
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
from subcommands import download_wikisource_intro
from subcommands import ws_bot_real
from ws import ws_revision_api


def run(edits_path, pywikibot_args, no_save=False):
    """Apply an edit file of named pages, saving every changed page unless no_save."""
    ws_bot_real.assert_pywikibot_dir_configured(pywikibot_args)
    spec = _read_spec(edits_path)
    pages = spec["pages"]
    run_root = os.path.join(_RUNS_ROOT, datetime.now(NEW_YORK).strftime(_STAMP))
    my_utils_fm.show_progress_g(__file__, "run-artifacts", run_root)
    bases = _base_revisions(pages)
    file_io.json_dump_to_file_path(
        {
            key: {name: value for name, value in base.items() if name != "content"}
            for key, base in bases.items()
        },
        os.path.join(run_root, "misc", "bases.json"),
    )
    texts, changed = {}, []
    for key, page in pages.items():
        base_text = bases[key]["content"].decode("utf-8")
        texts[key] = _edited(key, base_text, page["edits"])
        _write_text_file(run_root, "base", key, base_text)
        _write_text_file(run_root, "pages", key, texts[key])
        if texts[key] != base_text:
            changed.append(key)
    saved, failures = [], []
    saved_path = os.path.join(run_root, "misc", "saved-pages.json")
    try:
        if not no_save:
            site = pywikibot.Site("he", "wikisource", "BDencklaBot")
            for key in changed:
                try:
                    saved.append(
                        _save(site, key, bases[key], texts[key], spec["summary"])
                    )
                except pywikibot.exceptions.Error as error:
                    failures.append(f"{key}: the save failed: {error!r}")
                    break
    finally:
        # Preserve known saved revision IDs if verification raises.
        file_io.json_dump_to_file_path(saved, saved_path)
        if saved:
            failures.extend(_verify(saved, texts))
        file_io.json_dump_to_file_path(saved, saved_path)
    _report_special_pages(saved)
    if failures:
        raise SystemExit(
            "pages run failed:\n" + "\n".join(f"- {line}" for line in failures)
        )
    if no_save and changed:
        raise SystemExit(
            "no-save run found pages that would change:\n"
            + "\n".join(f"- {key} ({pages[key]['title']})" for key in changed)
        )


def _read_spec(edits_path):
    with open(edits_path, "r", encoding="utf-8") as edits_fp:
        spec = json.load(edits_fp)
    _require(
        isinstance(spec, dict) and set(spec) == {"summary", "edit-kind", "pages"},
        "The edit file's keys are not summary, edit-kind and pages",
    )
    if spec["edit-kind"] != "explicit-replacement":
        raise SystemExit(f"Unknown pages edit kind: {spec['edit-kind']!r}")
    _require(
        isinstance(spec["summary"], str) and spec["summary"],
        "The edit file has no summary",
    )
    pages = spec["pages"]
    _require(isinstance(pages, dict) and pages, "The edit file names no page")
    for key, page in pages.items():
        _require(
            _KEY_RE.fullmatch(key),
            f"Page key {key!r} is not made of lowercase ASCII letters, digits and hyphens",
        )
        _require(
            isinstance(page, dict) and set(page) == {"title", "base-revid", "edits"},
            f"Page {key}'s keys are not title, base-revid and edits",
        )
        _require(
            isinstance(page["title"], str) and page["title"], f"Page {key} has no title"
        )
        _require(
            type(page["base-revid"]) is int and page["base-revid"] > 0,
            f"Page {key}'s base-revid is not a revision id",
        )
        _require(
            isinstance(page["edits"], list) and page["edits"], f"Page {key} has no edit"
        )
        for edit in page["edits"]:
            _require(
                isinstance(edit, dict)
                and {"old", "new"} <= set(edit) <= {"old", "new", "comment"}
                and isinstance(edit["old"], str)
                and edit["old"]
                and isinstance(edit["new"], str),
                f"Page {key} has an edit that is not an old, a new and an optional comment",
            )
    titles = [page["title"] for page in pages.values()]
    _require(len(set(titles)) == len(titles), "The edit file names a title twice")
    return spec


def _require(condition, message):
    if not condition:
        raise SystemExit(message)


def _base_revisions(pages):
    """Each page's latest revision, its content as exact bytes, once no refusal applies."""
    keys = {page["title"]: key for key, page in pages.items()}
    intro_titles = {
        page["title"]
        for page in download_wikisource_intro.read_manifest()["pages"].values()
    }
    if names := sorted(set(keys) & intro_titles):
        raise SystemExit(f"Refused: introduction pages, which `intro` edits: {names}")
    chapter_page_ids = _chapter_page_ids()
    bases = {}
    with polite_download.PoliteDownloader(_CHECK_CONFIG) as downloader:
        client = ws_revision_api.ChapterClient(downloader, _API_PHP)
        identities = []
        for batch in ws_revision_api.batches(list(keys), _MAX_METADATA_TITLES):
            results = client.by_titles(batch, content=False)
            identities.extend(identity for identity, _lines in results.values())
        for identity in identities:
            title = identity["requested_title"]
            base_revid = pages[keys[title]]["base-revid"]
            if identity["resolved_title"] != title:
                raise SystemExit(
                    f"Refused: {title} resolves to {identity['resolved_title']}"
                )
            if identity["page_id"] in chapter_page_ids:
                raise SystemExit(
                    f"Refused: {title} is a chapter page, which `real` edits"
                )
            if identity["revision_id"] != base_revid:
                raise SystemExit(
                    f"Refused: the latest revision of {title} is"
                    f" {identity['revision_id']}, not its base-revid {base_revid}"
                )
        for batch in ws_revision_api.batches(identities, _MAX_CONTENT_TITLES):
            for title, (identity, revision) in client.by_raw_revisions(batch).items():
                bases[keys[title]] = {
                    "title": title,
                    "page_id": identity["page_id"],
                    **revision,
                }
    return {key: bases[key] for key in pages}


def _chapter_page_ids():
    with open(_CHAPTER_METADATA_PATH, "r", encoding="utf-8") as metadata_fp:
        metadata = json.load(metadata_fp)
    assert metadata["endpoint"] == _API_PHP, metadata["endpoint"]
    return {
        record["page_id"]
        for chapters in metadata["books"].values()
        for record in chapters.values()
    }


def _edited(key, text, edits):
    for edit in edits:
        count = text.count(edit["old"])
        assert (
            count == 1
        ), f"Expected 1 occurrence of {edit['old']!r} in {key}, found {count}"
        text = text.replace(edit["old"], edit["new"])
    return text


def _save(site, key, base, text, summary):
    page = pywikibot.Page(site, base["title"])
    page.text = text
    # Whatever pywikibot's configuration says, the text goes out exactly as edited, and
    # the guards stay tied to the revision whose text was edited, not to one that
    # pywikibot may fetch while building its request.
    page.save(
        summary,
        minor=True,
        apply_cosmetic_changes=False,
        nocreate=True,
        baserevid=base["revision_id"],
        basetimestamp=base["revision_timestamp"],
    )
    newrevid = page.latest_revision_id
    return {
        "key": key,
        "title": base["title"],
        "pageid": base["page_id"],
        "oldrevid": base["revision_id"],
        "newrevid": newrevid,
        "diff": he_diff_url(base["title"], newrevid, base["revision_id"]),
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
                failures.append(f"{record['key']}: no saved revision to read: {error}")
                continue
            if content == texts[record["key"]].encode("utf-8"):
                record["verified"] = True
            else:
                failures.append(f"{record['key']}: the saved text is not the text sent")
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


def _report_special_pages(saved):
    with open(_SPECIAL_MANIFEST_PATH, "r", encoding="utf-8") as manifest_fp:
        records = json.load(manifest_fp)["pages"]
    slugs = {record["page_id"]: slug for slug, record in records.items()}
    for record in saved:
        if (slug := slugs.get(record["pageid"])) is not None:
            print(
                f"in/mam-ws-special/{slug}.mediawiki is now behind revision"
                f" {record['newrevid']} of {record['title']};"
                " py/main_download.py fr-wikisource refreshes it"
            )


def _write_text_file(run_root, sub_dir, key, text):
    path = os.path.join(run_root, sub_dir, f"{key}.mediawiki")
    my_utils_fm.show_progress_g(__file__, path)
    file_io.with_tmp_openw(path, {}, _write_text, text)


def _write_text(text, outfp):
    outfp.write(text)


_KEY_RE = re.compile(r"[a-z0-9-]+")
_RUNS_ROOT = ".novc/mam-ws-bot-pages-runs"
_STAMP = "%Y%m%d-%H%M%S-%f%z"
_API_PHP = "https://he.wikisource.org/w/api.php"
_CHAPTER_METADATA_PATH = "in/mam-ws-revisions.json"
_SPECIAL_MANIFEST_PATH = "in/mam-ws-special/manifest.json"
_MAX_METADATA_TITLES = 50
_MAX_CONTENT_TITLES = 20
# The waits before each further read of a saved revision; None ends the reads.
_REREAD_WAITS_S = (5.0, 10.0, 20.0, None)
_CHECK_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent="MAM-basics pages bot check (https://github.com/bdenckla/MAM-basics)",
    throttle=polite_download.ThrottleConfig(min_delay_s=1.5),
)
