"""Mirror the MAM introduction from Hebrew Wikisource into ``in/mam-ws-intro/``.

Usage (run from repo root):
    .venv/Scripts/python.exe py/main_download.py fr-ws-intro

WHY A LOCAL MIRROR EXISTS.  ``doc/sigil-decoding.md`` names
``ויקיטקסט:מבוא למקרא על פי המסורה/נספחים`` as the first and heaviest of its sigil
sources, and recorded that no copy of it was mirrored anywhere in the local repos, so
it had to be fetched every time -- and that a summarizing fetch is not good enough for
it.  On 2026-08-06 one such fetch reported the siglum ``ו`` as "Leningrad Codex,
Washington Pentateuch", having merged ``ו`` with the neighbouring ``ל`` entry.  The
introduction is also what ``py/author_misc/he_ws_intro_to_mam_pasleg.py`` and
``he_ws_intro_to_mam_gray_maqaf_1.py`` adapt; the first of those already kept a
hand-saved copy of its one source section beside it, as
``he_ws_intro_to_mam_pasleg.mediawiki``, for exactly this reason.  This module
generalizes that one file to the whole introduction.

WHAT IS MIRRORED, AND WHY THE SET IS DECLARED RATHER THAN DISCOVERED.  The thirteen
pages of ``_SLUG_TO_TITLE`` below, which on 2026-08-31 were the whole of the
introduction: 1,852,837 bytes of wikitext, the committed manifest's sum (this line said
1,852,439 until 2026-09-01 -- a drafting-time fetch predating upstream edits of
2026-08-30 and -31 to ch4 and the appendices).  The set is written out here so the slugs
can be ASCII and stable, and ``_assert_declared_set_is_live_set`` then FAILS if the
live set has gained or lost a page -- which is a finding about the introduction, and
wants a human to choose a slug for the new page, not a silently-widened mirror.

THE TWO MIRRORED MANUSCRIPT INDEX PAGES ARE NOT THE GENERATORS' OUTPUT, AND ARE NOT
MEANT TO MATCH IT. ``py/main_ac_wikisource_page.py`` writes ``index.wiki`` in the sibling
codex-index-aleppo, and ``py/main_lenin_wikisource_page.py`` writes the Leningrad
index at ``leningrad/lenin-wiki/index.wiki``. Ben, 2026-08-31, on those two files:
they "were only ever intended to be starting
points for manual work on Wikisource."  ``index-aleppo`` and ``index-leningrad`` here
are that manual work as published.  So the difference between generator and page is the
intended transformation rather than drift; there is no sync to maintain in either
direction, and NOTHING SHOULD COMPARE THE TWO -- an earlier draft of this docstring
called the mirror a drift check between them, which was wrong.  The scale settles it:
26 of the Aleppo generator's 700 lines reach the live page (4%), and 94 of the
Leningrad generator's 1,135 (8%).

WHAT IS WRITTEN.  One ``<slug>.mediawiki`` per page, holding the page's wikitext
VERBATIM -- no normalization of any kind, which for Hebrew is the standing rule of
``CLAUDE.md`` and here is also the entire point: this is hand-authored wiki prose, so
clusters in Unicode-normal rather than MAM-normal order are what the source says and
are not defects.  Do not run ``uni_check`` or ``has_std_mark_order`` over this tree.
Alongside them, ``manifest.json`` records each page's Hebrew title, revision id,
revision timestamp and byte size, so a reader can see how stale a copy is without a
network call.

THE MIRROR IS A CONVENIENCE AND CAN BE STALE, which matters more here than for the
books under ``in/mam-ws/``: those move when Ben edits them, the introduction moves when
Avi Kadish does, without notice.  Five of the thirteen pages were edited in August 2026
alone (the manifest's count; this said four until 2026-09-01, for the same
drafting-time-fetch reason as the byte figure above).  Read ``manifest.json``'s
timestamps before treating a copy as current.

A REFRESH OVER AN UNCHANGED WIKI PRODUCES NO DIFF, so any diff a refresh does produce is
a real edit on Wikisource and is worth reading.  Verified 2026-08-31 by running this
subcommand twice: the second run rewrote all fourteen files and left a clean working
tree.  Nothing here is time-varying -- the manifest's provenance line is stable, the page
order follows ``_SLUG_TO_TITLE``, and the wikitext is written byte for byte as fetched
-- and that is a property to preserve, since it is what makes a post-refresh diff
legible.
"""

import json

from mb_cmn import file_io
from mb_cmn import paths
from mb_cmn import polite_download
from mb_misc import my_utils_for_mainish as my_utils_fm
from mb_misc import ws_urls

_ROOT_TITLE = "ויקיטקסט:מבוא למקרא על פי המסורה"

# Slug -> Hebrew Wikisource title.  The slugs are the mirror's filenames, so they are
# ASCII and are not renamed once published; the titles are what the wiki actually calls
# the pages, and _assert_declared_set_is_live_set checks them against it on every run.
_SLUG_TO_TITLE = {
    "root": _ROOT_TITLE,
    "summary": f"{_ROOT_TITLE}/תקציר",
    "ch1": f"{_ROOT_TITLE}/פרק א",
    "ch2": f"{_ROOT_TITLE}/פרק ב",
    "ch3": f"{_ROOT_TITLE}/פרק ג",
    "ch4": f"{_ROOT_TITLE}/פרק ד",
    "ch5": f"{_ROOT_TITLE}/פרק ה",
    "appendices": f"{_ROOT_TITLE}/נספחים",
    "index-aleppo": f"{_ROOT_TITLE}/מפתח לכתר ארם צובה",
    "index-leningrad": f'{_ROOT_TITLE}/מפתח לכתי"ל',
    "westminster-typing": f"{_ROOT_TITLE}/מידע טכני על הקלדת וסטמינסטר",
    "data-sheet-guide": f"{_ROOT_TITLE}/מדריך טכני לגיליון הנתונים",
    "technical-guide": f"{_ROOT_TITLE}/מדריך טכני",
}


def run() -> None:
    """Download the MAM introduction from Hebrew Wikisource and write the mirror."""
    with polite_download.PoliteDownloader(_DOWNLOAD_CONFIG) as downloader:
        _assert_declared_set_is_live_set(downloader)
        slugs_to_revisions = _download_revisions(downloader)
    _write_mirror(slugs_to_revisions)


def run_from_args(_args) -> None:
    """Entry point for ``main_download.py``, whose subcommand takes no options."""
    run()


def _assert_declared_set_is_live_set(downloader) -> None:
    """Fail unless the live introduction is exactly the declared thirteen pages.

    A page added to or removed from the introduction is a finding: the new page wants an
    ASCII slug chosen for it, and a removed one wants its mirrored file deleted.  Neither
    is a decision this module can make, so it raises rather than quietly mirroring a
    different set than the one its docstring describes.
    """
    live_titles = set(_live_subpage_titles(downloader))
    declared_titles = set(_SLUG_TO_TITLE.values())
    assert live_titles == declared_titles, (
        "the introduction's page set has changed on Wikisource;"
        " update _SLUG_TO_TITLE and this module's docstring",
        sorted(live_titles - declared_titles),
        sorted(declared_titles - live_titles),
    )


def _live_subpage_titles(downloader):
    """Every page in the Wikisource-project namespace under the introduction's prefix."""
    titles = []
    continuation = {}
    while True:
        params = {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "maxlag": 1,
            "list": "allpages",
            "apnamespace": _WIKISOURCE_PROJECT_NAMESPACE,
            "apprefix": _ROOT_TITLE.split(":", 1)[1],
            "aplimit": _MAX_TITLES_PER_REQUEST,
            **continuation,
        }
        response_json = downloader.get_json(_WIKISOURCE_API_PHP, params=params)
        assert "error" not in response_json, response_json["error"]
        titles.extend(page["title"] for page in response_json["query"]["allpages"])
        if "continue" not in response_json:
            return titles
        continuation = response_json["continue"]


def _download_revisions(downloader):
    """Slug -> the page's current revision, as a dict of content and revision facts."""
    slugs_to_revisions = {}
    for slugs in _slug_batches():
        slugs_to_revisions.update(_download_revision_batch(slugs, downloader))
    return slugs_to_revisions


def _slug_batches():
    slugs = list(_SLUG_TO_TITLE)
    batch_size = _MAX_TITLES_PER_REQUEST
    return [slugs[i : i + batch_size] for i in range(0, len(slugs), batch_size)]


def _download_revision_batch(slugs, downloader):
    titles = [_SLUG_TO_TITLE[slug] for slug in slugs]
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "maxlag": 1,
        "prop": "revisions",
        "rvprop": "content|ids|timestamp|size",
        "rvslots": "main",
        "titles": "|".join(titles),
    }
    # No redirects=1, unlike the book downloader: a redirect page in the introduction is
    # mirrored as the redirect it is, rather than silently as its target.
    response_json = downloader.get_json(_WIKISOURCE_API_PHP, params=params)
    titles_to_revisions = _revisions_from_response_json(response_json, titles)
    return {slug: titles_to_revisions[_SLUG_TO_TITLE[slug]] for slug in slugs}


def _revisions_from_response_json(response_json, requested_titles):
    assert "error" not in response_json, response_json["error"]
    query = response_json.get("query")
    assert query is not None, response_json
    alias_to_requested_title = _alias_to_requested_title(query, requested_titles)
    pages = query.get("pages")
    assert isinstance(pages, list), response_json
    titles_to_revisions = {}
    for page in pages:
        assert "missing" not in page, page
        requested_title = alias_to_requested_title.get(page["title"])
        assert requested_title is not None, page
        assert requested_title not in titles_to_revisions, page
        titles_to_revisions[requested_title] = _revision_of_page(page)
    assert set(titles_to_revisions) == set(requested_titles), sorted(
        titles_to_revisions
    )
    return titles_to_revisions


def _alias_to_requested_title(query, requested_titles):
    """Map each title the API answers with back to the title we asked for.

    MediaWiki normalizes a title before answering, and reports what it did.  Our titles
    are already in canonical form, so nothing is expected here -- but a normalization we
    did not anticipate would otherwise surface as a missing page rather than as itself.
    """
    alias_to_requested_title = {title: title for title in requested_titles}
    for normalized in query.get("normalized", []):
        requested_title = alias_to_requested_title.get(normalized["from"])
        assert requested_title is not None, normalized
        alias_to_requested_title[normalized["to"]] = requested_title
    return alias_to_requested_title


def _revision_of_page(page):
    revisions = page.get("revisions")
    assert revisions, page
    revision = revisions[0]
    content = revision["slots"]["main"].get("content")
    assert content is not None, page
    return {
        "title": page["title"],
        "revid": revision["revid"],
        "timestamp": revision["timestamp"],
        "size": revision["size"],
        "content": content,
    }


def _write_mirror(slugs_to_revisions) -> None:
    out_dir = paths.in_dir() / _MIRROR_DIR_NAME
    manifest_pages = {}
    for slug, revision in slugs_to_revisions.items():
        out_path = str(out_dir / f"{slug}.mediawiki")
        my_utils_fm.show_progress_g(__file__, out_path)
        file_io.with_tmp_openw(out_path, {}, _write_wikitext, revision["content"])
        manifest_pages[slug] = {
            key: revision[key] for key in ("title", "revid", "timestamp", "size")
        }
    file_io.json_dump_to_file_path(
        {"pages": manifest_pages},
        str(out_dir / _MANIFEST_NAME),
        generator_file=__file__,
    )
    my_utils_fm.show_progress_g(__file__, str(out_dir / _MANIFEST_NAME))


def _write_wikitext(content, out_fp) -> None:
    out_fp.write(content)


def read_manifest():
    """The mirror's manifest, for a reader wanting each page's title and staleness."""
    manifest_path = paths.in_dir() / _MIRROR_DIR_NAME / _MANIFEST_NAME
    with open(manifest_path, "r", encoding="utf-8") as manifest_fp:
        return json.load(manifest_fp)


def page_path(slug):
    """The mirrored wikitext of one declared page."""
    assert slug in _SLUG_TO_TITLE, sorted(_SLUG_TO_TITLE)
    return paths.in_dir() / _MIRROR_DIR_NAME / f"{slug}.mediawiki"


_MIRROR_DIR_NAME = "mam-ws-intro"
_MANIFEST_NAME = "manifest.json"
_WIKISOURCE_USER_PAGE = ws_urls.he_url("משתמש:Bdenckla")
_MAX_TITLES_PER_REQUEST = 20
_WIKISOURCE_API_PHP = "https://he.wikisource.org/w/api.php"
# 4 is the Wikisource-project namespace, spelled ויקיטקסט: in a title.
_WIKISOURCE_PROJECT_NAMESPACE = 4
_DOWNLOAD_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent=f"Denckla-Dowload-MAM-Bot/1.1 ({_WIKISOURCE_USER_PAGE})",
    default_timeout_s=30.0,
    throttle=polite_download.ThrottleConfig(min_delay_s=1.5, mean_delay_s=3.0),
    retry=polite_download.RetryConfig(max_attempts=4),
    cache=polite_download.CacheConfig(dir_path=".novc/http-cache/wikisource"),
    obey_robots_txt=False,
)
