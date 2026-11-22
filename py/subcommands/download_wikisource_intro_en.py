"""Mirror English Wikisource's translation of the MAM introduction into in/mam-ws-intro-en/.

Usage (run from repo root):
    .venv/Scripts/python.exe py/main_download.py fr-ws-intro-en

WHAT IS MIRRORED.  The MAM introduction, which ``download_wikisource_intro`` mirrors
from Hebrew Wikisource into ``in/mam-ws-intro/``, has a partial English translation on
English Wikisource, kept in user space under ``_PREFIX``.  ``_SLUG_TO_TITLE`` declares
its pages: on 2026-11-22 they were every page under that prefix, seven pages with text
and one redirect, and ``in/mam-ws-intro-en/README.md`` says what each one held that day.
``_assert_declared_set_is_live_set`` FAILS if the live set has gained or lost a page, as
its namesake in ``download_wikisource_intro`` does, since a new page wants a human to
choose its Hebrew counterpart.

IN WHAT SENSE THE MIRROR IS PARALLEL.  Each English page is written under the slug of
the Hebrew page it translates, so ``in/mam-ws-intro-en/ch3.mediawiki`` translates part
of ``in/mam-ws-intro/ch3.mediawiki``.  A Hebrew slug with no English page, such as
``ch4``, has no file here.  The pairing is a checked fact rather than a declaration.
``_assert_pairs_are_interlanguage_links`` checks the pages with text: a page of the
Hebrew mirror paired with one must carry exactly one interlanguage link to English
Wikisource, naming its English page or a redirect to it, and every other page of the
Hebrew mirror must carry none.  ``_REDIRECT_SLUG_TO_TARGET_SLUG`` declares the
redirect, which is mirrored as the redirect it is, as the Hebrew mirror mirrors its
own, under the slug of the Hebrew redirect it parallels: ``technical-guide`` is a
redirect on both wikis, and the redirect checks fail unless each leads to its own
wiki's page of ``data-sheet-guide``.  The manifest gives each page the four fields of
the Hebrew manifest, ``title``, ``revid``, ``timestamp`` and ``size``, and adds
``hebrew_title``, the counterpart's title as the Hebrew manifest records it.

HOW IT READS ENGLISH WIKISOURCE.  Through the Action API, with ``ws_revision_api``: one
listing of the prefix; one metadata query for the Hebrew pages' interlanguage targets,
which a ``ChapterClient`` resolves; one for the declared pages as themselves, which
follows no redirect, so that the declared redirect is read as itself; and then one
query for the declared revisions' exact bytes, which a ``ChapterClient`` binds to each
page's identity by revision id.  Wikimedia's robots.txt disallows ``/w/``, and with it
the Action API, to every agent.  Ben chose this transport on 2026-11-22, approving the
recommendation that his decision page gave as 1A: "I concur with all three off your
recommendations on the decision page."  The recommendation's reasons: Wikimedia's
Robot policy has an Action API section that sets the limits of an unauthenticated
client, and the Hebrew mirror already reads Hebrew Wikisource this way under the same
robots.txt.  The requests keep those limits: one request at a time, at least five
seconds apart, titles batched, and ``maxlag=1``.  ``in/mam-ws-intro-en/README.md``,
"How the mirror reads English Wikisource", says more.

WHAT IS WRITTEN.  One ``<slug>.mediawiki`` per page, holding its revision's wikitext
byte for byte, and ``manifest.json``.  Nothing is normalized: the pages quote pointed
Hebrew, whose mark order is the source's, as ``in/mam-ws-intro/README.md`` says of the
Hebrew mirror.  Do not run ``uni_check`` or ``has_std_mark_order`` over this tree.

A REFRESH OVER AN UNCHANGED WIKI PRODUCES NO DIFF, so a diff that a refresh does produce
is an edit on English Wikisource, or a retitled Hebrew page, and is worth reading.
"""

import dataclasses
import re
from pathlib import Path

from mb_cmn import file_io
from mb_cmn import paths
from mb_cmn import polite_download
from mb_misc import my_utils_for_mainish as my_utils_fm
from subcommands import download_wikisource_intro
from ws import ws_revision_api

_PREFIX = "User:Dovi/Miqra according to the Masorah/Introduction"

# Slug -> English Wikisource title.  Each slug is the slug, in in/mam-ws-intro/, of the
# Hebrew page that the English page translates or, for a redirect, parallels; the
# pairing checks test each pair against the Hebrew mirror on every run.
_SLUG_TO_TITLE = {
    "root": _PREFIX,
    "summary": f"{_PREFIX}/Abstract",
    "ch1": f"{_PREFIX}/Chapter 1",
    "ch2": f"{_PREFIX}/Chapter 2",
    "ch3": f"{_PREFIX}/Chapter 3",
    "appendices": f"{_PREFIX}/Appendices",
    "data-sheet-guide": f"{_PREFIX}/Technical Guide to the Spreadsheet",
    "technical-guide": f"{_PREFIX}/Technical Guide",
}
# Slug of each declared redirect -> slug of the declared page with text it leads to.
# The Hebrew page of the same slug is a redirect to that slug's Hebrew page.
_REDIRECT_SLUG_TO_TARGET_SLUG = {"technical-guide": "data-sheet-guide"}


def run() -> None:
    """Download the English introduction from English Wikisource and write the mirror."""
    hebrew_pages = download_wikisource_intro.read_manifest()["pages"]
    hebrew_titles = _hebrew_titles(hebrew_pages)
    interlanguage_targets = _interlanguage_targets(hebrew_pages)
    _assert_hebrew_redirects_pair(hebrew_pages)
    with polite_download.PoliteDownloader(_DOWNLOAD_CONFIG) as downloader:
        _assert_declared_set_is_live_set(downloader)
        _assert_pairs_are_interlanguage_links(downloader, interlanguage_targets)
        slugs_to_revisions = _download_revisions(downloader)
    _assert_english_redirects_pair(slugs_to_revisions)
    _write_mirror(slugs_to_revisions, hebrew_titles)


def run_from_args(_args) -> None:
    """Entry point for ``main_download.py``, whose subcommand takes no options."""
    run()


def text_slugs():
    """The declared slugs whose English pages have text, that is, are not redirects."""
    return [
        slug for slug in _SLUG_TO_TITLE if slug not in _REDIRECT_SLUG_TO_TARGET_SLUG
    ]


def page_path(slug):
    """The mirrored wikitext of one declared English page."""
    assert slug in _SLUG_TO_TITLE, sorted(_SLUG_TO_TITLE)
    return paths.in_dir() / _MIRROR_DIR_NAME / f"{slug}.mediawiki"


def _hebrew_titles(hebrew_pages):
    """Slug -> the Hebrew counterpart's title, as the Hebrew manifest records it."""
    unknown = sorted(set(_SLUG_TO_TITLE) - set(hebrew_pages))
    assert not unknown, ("declared slugs that the Hebrew mirror lacks", unknown)
    return {slug: hebrew_pages[slug]["title"] for slug in _SLUG_TO_TITLE}


def _interlanguage_targets(hebrew_pages):
    """Slug -> the English title that the Hebrew page's interlanguage link names.

    Every page of the Hebrew mirror is read.  A page paired with an English page with
    text must have exactly one such link.  Any other must have none, since a link from
    it would name an English page that this mirror does not pair with it; the Hebrew
    redirect has none, and the redirect checks pair it instead.
    """
    paired_slugs = text_slugs()
    targets = {}
    for slug in hebrew_pages:
        wikitext = download_wikisource_intro.page_path(slug).read_text(encoding="utf-8")
        links = [link.strip() for link in _INTERLANGUAGE_LINK_RE.findall(wikitext)]
        if slug in paired_slugs:
            assert len(links) == 1, (
                "a paired Hebrew page's English links",
                slug,
                links,
            )
            targets[slug] = links[0]
        else:
            assert not links, ("an unpaired Hebrew page links English", slug, links)
    return targets


def _assert_hebrew_redirects_pair(hebrew_pages) -> None:
    """Fail unless each declared redirect's Hebrew page leads to its target's page."""
    for slug, target_slug in _REDIRECT_SLUG_TO_TARGET_SLUG.items():
        path = download_wikisource_intro.page_path(slug)
        target = _redirect_target(
            path.read_text(encoding="utf-8"), _HE_REDIRECT_MAGIC_WORDS
        )
        assert target == hebrew_pages[target_slug]["title"], (slug, target)


def _assert_declared_set_is_live_set(downloader) -> None:
    """Fail unless the pages under _PREFIX are exactly the declared ones."""
    live_titles = set(_live_titles(downloader))
    declared_titles = set(_SLUG_TO_TITLE.values())
    assert live_titles == declared_titles, (
        "the English introduction's page set has changed on English Wikisource;"
        " update _SLUG_TO_TITLE, this module's docstring and the mirror's README",
        sorted(live_titles - declared_titles),
        sorted(declared_titles - live_titles),
    )


def _live_titles(downloader):
    """Every page in the User namespace whose title begins with _PREFIX, redirects too."""
    titles = []
    continuation = {}
    while True:
        params = {
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "maxlag": 1,
            "list": "allpages",
            "apnamespace": _USER_NAMESPACE,
            "apprefix": _PREFIX.split(":", 1)[1],
            "aplimit": "max",
            **continuation,
        }
        response_json = ws_revision_api.get_query_json(
            downloader, _API_PHP, params, allow_cache=False
        )
        assert "error" not in response_json, response_json["error"]
        titles.extend(page["title"] for page in response_json["query"]["allpages"])
        if "continue" not in response_json:
            return titles
        continuation = response_json["continue"]


def _assert_pairs_are_interlanguage_links(downloader, interlanguage_targets) -> None:
    """Fail unless each Hebrew page's interlanguage link leads to its declared page.

    A link may name a redirect, as the root's does, and this query resolves it.  It has
    a client of its own, because a ChapterClient refuses to see one page under two
    requested titles, and the redirect and its target are exactly that.
    """
    paired_slugs = text_slugs()
    client = ws_revision_api.ChapterClient(downloader, _API_PHP)
    targets = [interlanguage_targets[slug] for slug in paired_slugs]
    results = client.by_titles(targets, content=False)
    for slug in paired_slugs:
        identity, _lines = results[interlanguage_targets[slug]]
        assert identity["resolved_title"] == _SLUG_TO_TITLE[slug], (slug, identity)


def _download_revisions(downloader):
    """Slug -> (identity, revision): the declared page's current exact bytes and facts."""
    identities = _identities_as_themselves(downloader, list(_SLUG_TO_TITLE.values()))
    client = ws_revision_api.ChapterClient(downloader, _API_PHP)
    titles_to_revisions = client.by_raw_revisions(identities)
    return {slug: titles_to_revisions[title] for slug, title in _SLUG_TO_TITLE.items()}


def _identities_as_themselves(downloader, titles):
    """Each declared page's identity as itself, the declared redirect included.

    ChapterClient.by_titles follows redirects, so it would give the declared redirect
    the identity of its target, which is declared too, and refuse the pair.  This query
    follows none, and fails unless the pages that the API reports as redirects are
    exactly the declared ones.
    """
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "maxlag": 1,
        "prop": "info",
        "titles": "|".join(titles),
    }
    response_json = ws_revision_api.get_query_json(
        downloader, _API_PHP, params, allow_cache=False
    )
    results = ws_revision_api.title_results(response_json, titles, content=False)
    redirect_titles = {
        page["title"]
        for page in response_json["query"]["pages"]
        if page.get("redirect")
    }
    declared_redirect_titles = {
        _SLUG_TO_TITLE[slug] for slug in _REDIRECT_SLUG_TO_TARGET_SLUG
    }
    assert redirect_titles == declared_redirect_titles, (
        "the English introduction's redirects have changed on English Wikisource",
        sorted(redirect_titles),
        sorted(declared_redirect_titles),
    )
    return [identity for identity, _lines in results.values()]


def _assert_english_redirects_pair(slugs_to_revisions) -> None:
    """Fail unless each declared redirect leads to its target slug's declared page."""
    for slug, target_slug in _REDIRECT_SLUG_TO_TARGET_SLUG.items():
        _identity, revision = slugs_to_revisions[slug]
        target = _redirect_target(
            revision["content"].decode("utf-8"), _EN_REDIRECT_MAGIC_WORDS
        )
        assert target == _SLUG_TO_TITLE[target_slug], (slug, target)


def _redirect_target(wikitext, magic_words):
    """The title that a redirect's wikitext leads to; it fails on any other wikitext."""
    alternatives = "|".join(re.escape(magic_word) for magic_word in magic_words)
    match = re.match(
        rf"\s*(?:{alternatives})\s*\[\[([^\]|#]+)", wikitext, re.IGNORECASE
    )
    assert match is not None, ("not a redirect", wikitext[:200])
    return match.group(1).strip()


def _write_mirror(slugs_to_revisions, hebrew_titles) -> None:
    out_dir = paths.in_dir() / _MIRROR_DIR_NAME
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_pages = {}
    for slug, (identity, revision) in slugs_to_revisions.items():
        out_path = str(out_dir / f"{slug}.mediawiki")
        my_utils_fm.show_progress_g(__file__, out_path)
        file_io.with_tmp_path(out_path, _write_bytes, revision["content"])
        manifest_pages[slug] = {
            "title": identity["resolved_title"],
            "revid": revision["revision_id"],
            "timestamp": revision["revision_timestamp"],
            "size": revision["byte_size"],
            "hebrew_title": hebrew_titles[slug],
        }
    file_io.json_dump_to_file_path(
        {"pages": manifest_pages},
        str(out_dir / _MANIFEST_NAME),
        generator_file=__file__,
    )
    my_utils_fm.show_progress_g(__file__, str(out_dir / _MANIFEST_NAME))


def _write_bytes(content, path) -> None:
    Path(path).write_bytes(content)


_MIRROR_DIR_NAME = "mam-ws-intro-en"
_MANIFEST_NAME = "manifest.json"
_API_PHP = "https://en.wikisource.org/w/api.php"
# 2 is the User namespace, spelled User: in a title.
_USER_NAMESPACE = 2
# An interlanguage link to English Wikisource, wherever it is and however its prefix is
# capitalized, since MediaWiki reads it so.  Each paired page of the Hebrew mirror ends
# with one, alone on its line.  An inline [[:EN:...]] link, whose colon comes first, is
# an ordinary link, and this does not match it.
_INTERLANGUAGE_LINK_RE = re.compile(
    r"\[\[\s*en\s*:([^\]|]+)(?:\|[^\]]*)?\]\]", re.IGNORECASE
)
# The redirect magic words that each wiki's redirect here may begin with: English
# Wikisource's, and on Hebrew Wikisource the same word or Hebrew Wikisource's own.
_EN_REDIRECT_MAGIC_WORDS = ("#REDIRECT",)
_HE_REDIRECT_MAGIC_WORDS = (
    "#REDIRECT",
    "#\N{HEBREW LETTER HE}\N{HEBREW LETTER PE}\N{HEBREW LETTER NUN}"
    "\N{HEBREW LETTER YOD}\N{HEBREW LETTER HE}",
)
# The Hebrew mirror's identity, so that both mirrors name the same bot and contact, with
# at least five seconds from the end of one request to the next: far inside the limits
# that the Robot policy's Action API section sets for an unauthenticated client, one
# request at a time and fewer than five a second.
_DOWNLOAD_CONFIG = dataclasses.replace(
    download_wikisource_intro._DOWNLOAD_CONFIG,
    throttle=polite_download.ThrottleConfig(min_delay_s=5.0, mean_delay_s=6.0),
    cache=polite_download.CacheConfig(),
)
