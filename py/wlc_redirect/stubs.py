"""Render the redirect stubs that stand in for wlc-utils' published pages, and lint them.

WHAT A STUB IS FOR

``bdenckla.github.io/wlc-utils/<path>`` is cited where Ben cannot reach the citation, and
that is the whole of what a stub is for: tanach.us's published change list, which cites
``accgram/goerwitz.html`` five times, and the citations nobody can enumerate -- emails
already sent, other people's pages, bookmarks, search indexes.  The pages themselves have
moved to ``bdenckla.github.io/MAM-basics/wlc/<path>``, a pure prefix rewrite, so each old
URL is answered by a stub at its own old path that sends the reader on.  See
``doc/PLAN-evacuate-the-rest-of-wlc-utils.md``, Phases 8 and 9.

A CITATION BEN CAN EDIT IS NOT A REASON FOR A STUB; IT IS A URL TO UPDATE.  This docstring
named three sources as "places Ben cannot edit" until 2026-08-22, and two of the three are
his own: the four deep links carrying fragments in UXLC-utils' generated CLC notes, whose
URL is ``py/clc/clc_render.py``'s ``_LC_CORROBORATED_LINK`` in this repo and so is one
constant and a regeneration away from being right, and the four paths in
``document-index/README.md``, hand written.  A fifth source the list missed,
``UXLC-utils/doc/clc-design.md``, is hand written too.  Ben, 2026-08-22: "The stubs are
for things out of my control."  Those three sources are in his control and want the new
URL, not a redirect.  What is genuinely beyond it is tanach.us: the five citations there
are in change proposals Ben submitted and that site publishes, and the copies vendored
back under ``UXLC-utils/in/UXLC-misc/`` are snapshots of what it publishes, so editing one
would falsify the snapshot and change nothing about the citation.

THE PAGE LIST IS FROZEN, AND CAN ONLY SHRINK

``redirected_pages`` reads ``in/wlc_redirect_pages.json``, the 154 paths wlc-utils
published at the 2026-08-17 move.  What earns a stub is having been published under
``bdenckla.github.io/wlc-utils/`` -- a fact about the past, which no later page can
acquire, since new work is given out as a MAM-basics URL and cited as one.  So a page
added under ``gh-pages/wlc/`` after the move is not a missing stub, and ``check`` says
nothing about it.

That set was derived from the live ``git ls-files gh-pages/wlc`` until 2026-08-22, on the
reasoning that a derived set cannot drift from a hand-maintained one.  It was anchored to
the wrong set: the live pages and the old URLs coincided only because nothing had been
added under ``gh-pages/wlc/`` since ``f99996f`` (2026-08-12), and the first page added
here would have been reported as an old URL that "would 404 rather than redirect" when no
such URL had ever existed.  Ben's decision, 2026-08-22.

The relative path under ``gh-pages/wlc/`` is *both* the old wlc-utils path and the new
MAM-basics suffix, which is what makes the rewrite a prefix rewrite, and the manifest one
string per page rather than a mapping.  ``published_pages`` still reads the live site, for
the one direction the freeze leaves: a frozen page that is no longer published here, whose
stub now sends a reader to a page that is not there.

A directory URL is covered only where the directory has an ``index.html``, which is the
right answer rather than an accident: ``document-index/README.md`` cites ``/420422/`` and
``/wlc-a-notes/``, and both hold one, so both get a stub that a bare directory URL
reaches.  ``/accgram/`` holds no ``index.html`` (issue #230 -- it 404s today, and always
did), so it correctly gets no stub and falls to the ``404.html`` catch-all below.

WITH JAVASCRIPT DISABLED, A FRAGMENT IS LOST -- AND THE JS IS NOT BELT-AND-BRACES

A stub carries the target three times over, and the three are not redundant.  The
``<link rel="canonical">`` tells a search engine which copy is current.  The
``<meta http-equiv="refresh">`` is the no-JavaScript path, and it takes a *fixed* URL.
Only the ``<script>`` can carry the incoming query and fragment, because
``#supplied-dt5v6-bet-atnax`` is arbitrary and is never sent to the server -- it is
readable only in the browser, as ``location.hash``.  So the degradation with JavaScript
off is precise: **UXLC-utils' four deep links land on the right page, at its top rather
than at the anchor.**  The script wins over the meta refresh when both are live, because
it runs synchronously while the document is parsed and the refresh is a scheduled task.

``404.html`` is the catch-all for every path with no stub -- the non-HTML assets Phase 9
deletes, ``/accgram/``, and anything mistyped.  It reads ``location.pathname``, strips the
leading ``/wlc-utils/`` and prepends the new site, so it forwards rather than guesses.
GitHub Pages serves it with an HTTP **404** status whatever it then does, which is exactly
why the per-page stubs exist: a cited URL has to answer 200.

WHAT ``build`` DOES NOT DO

It writes stubs and ``404.html`` and deletes nothing.  Phase 9's removal of wlc-utils'
130 non-HTML assets is a ``git rm``, kept out of a generator that can be pointed at
another repository's tree.  A stub left behind by a page that has since gone is reported
by ``check``, not silently cleaned up.
"""

from __future__ import annotations

from pathlib import Path
import json
import re
import subprocess

from mb_cmn import paths

# The published site the stubs point at, and the path prefix the old site served under.
# Cite these by name rather than by their text: black splits a long string literal across
# adjacent literals to fit 88 columns, so a URL a page carries can appear nowhere in the
# source (Phase 7, finding 1).
NEW_SITE = "https://bdenckla.github.io/MAM-basics/wlc/"
OLD_PATH_PREFIX = "/wlc-utils/"

# The catch-all, which is a stub for no page and so is exempt from the correspondence
# check that every other .html in the tree faces.
NOT_FOUND_NAME = "404.html"

# Where a clone comes from, for the two subcommands that write into one or lint one.
_CLONE_URL = "https://github.com/bdenckla/wlc-utils.git"

# Where the frozen list of old URLs is read from, and where the pages those URLs now
# resolve to are published.  Both relative to this repo's root.
_MANIFEST_PATH = "in/wlc_redirect_pages.json"
_PAGES_PREFIX = "gh-pages/wlc/"

# Any target URL the rendered text carries.  Stops at a quote, a space or a tag bracket,
# which is what bounds it in every one of the four places a stub spells it.
_TARGET_RE = re.compile(re.escape(NEW_SITE) + r"[^\"'\s<>]*")

# The four carriers, each identified by something only it has.  A stub missing one of
# these still redirects, so ``check`` has to look for them by name rather than trust that
# a file naming the right URL is a whole stub.
_CARRIERS = (
    ('rel="canonical"', "canonical link"),
    ('http-equiv="refresh"', "meta refresh"),
    ("location.replace(", "script"),
    ("<a href=", "visible fallback link"),
)

_STUB_TEMPLATE = """<!doctype html>
<!-- GENERATED by py/main_wlc_redirect_stubs.py -- do not edit; run that program again. -->
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to MAM-basics: {path}</title>
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<script>
location.replace("{target}" + location.search + location.hash);
</script>
</head>
<body>
<p>This page has moved to <a href="{target}">{target}</a>.</p>
</body>
</html>
"""

_NOT_FOUND_TEMPLATE = """<!doctype html>
<!-- GENERATED by py/main_wlc_redirect_stubs.py -- do not edit; run that program again. -->
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to MAM-basics</title>
<script>
var wlcPrefix = "{old_prefix}";
var wlcPath = location.pathname;
var wlcRest = wlcPath.indexOf(wlcPrefix) === 0 ? wlcPath.slice(wlcPrefix.length) : "";
location.replace("{new_site}" + wlcRest + location.search + location.hash);
</script>
</head>
<body>
<p>These pages have moved to <a href="{new_site}">{new_site}</a>.</p>
</body>
</html>
"""


def wlc_utils_pages_dir() -> Path:
    """wlc-utils' published tree -- THE LAST REFERENCE TO THAT SIBLING IN THIS TREE.

    Phase 5 repointed every generator at this repo's own root, leaving the redirect stubs
    as the one thing that still has to name wlc-utils: the stubs are what that repository
    holds, and they cannot be written or linted without finding it.  Routed through
    ``require_sibling`` so an absent clone says which two environment overrides point at
    one, rather than dying on a bare ``FileNotFoundError`` deep in a writer.

    AND THERE IS NO CLONE ON THIS DISK.  Ben's decision, 2026-08-22: with the URL list
    frozen, publishing became a never event -- new pages here earn no stub -- so the clone
    was 101 MB standing by for an occasion that arises only if one of the 154 frozen pages
    is renamed or dropped.  Every failure this raises is therefore expected, and the fix
    is a fresh clone rather than an override: the message says so, and shallow is enough,
    neither caller reading history.
    """
    clone = paths.sibling_repo("wlc-utils")
    try:
        return paths.require_sibling("wlc-utils", clone) / "gh-pages"
    except FileNotFoundError as absent:
        raise FileNotFoundError(
            f"{absent}\n"
            "No clone is expected on this disk (2026-08-22); to get one:\n"
            f"  git clone --depth 1 {_CLONE_URL} {clone}"
        ) from absent


def default_out_dir() -> Path:
    """Where ``build`` writes when told neither ``--out`` nor ``--publish``.

    A gitignored scratch directory, so the safe destination is the default one and
    publishing into wlc-utils takes saying so.
    """
    return paths.novc_dir() / "wlc-redirect-stubs"


def redirected_pages(repo_root: Path) -> list[str]:
    """The frozen old URLs, as their paths below ``bdenckla.github.io/wlc-utils/``.

    Read from ``in/wlc_redirect_pages.json`` rather than derived, because what the set
    records is what wlc-utils published on 2026-08-17 and nothing measurable today says
    that.  An empty list is a failure rather than an empty run: a build that then wrote
    only ``404.html`` would look like it had worked.
    """
    manifest = repo_root / _MANIFEST_PATH
    pages = sorted(json.loads(manifest.read_text(encoding="utf-8"))["pages"])
    if not pages:
        raise AssertionError(
            f"{manifest} lists no pages: the old URLs the stubs answer are what this"
            " program exists to write, so a run that wrote none of them would report"
            " having written the catch-all and nothing else."
        )
    return pages


def published_pages(repo_root: Path) -> list[str]:
    """Every page published under ``gh-pages/wlc/``, as its path below that prefix.

    Where a frozen old URL now resolves to.  Used only to find a frozen page that is no
    longer published: an empty result is a failure rather than an empty run, because it
    means the site is not where this module thinks it is, and reporting all 154 stubs as
    pointing at deleted pages would be worse than saying so.
    """
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", _PAGES_PREFIX],
        cwd=repo_root,
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    pages = sorted(
        entry[len(_PAGES_PREFIX) :]
        for entry in result.stdout.split("\0")
        if entry.endswith(".html")
    )
    if not pages:
        raise AssertionError(
            f"no .html tracked under {_PAGES_PREFIX} in {repo_root}: the pages the old"
            " URLs now resolve to are not where this module looks for them, so every"
            " stub would be reported as pointing at a page that has gone."
        )
    return pages


def target_url(page_path: str) -> str:
    """The MAM-basics URL a stub at ``page_path`` sends the reader to."""
    return NEW_SITE + page_path


def render_stub(page_path: str) -> str:
    return _STUB_TEMPLATE.format(path=page_path, target=target_url(page_path))


def render_not_found() -> str:
    return _NOT_FOUND_TEMPLATE.format(old_prefix=OLD_PATH_PREFIX, new_site=NEW_SITE)


def write_stubs(repo_root: Path, out_dir: Path) -> list[str]:
    """Write a stub per old URL plus ``404.html``; return the paths written, site-relative."""
    written = []
    for page_path in redirected_pages(repo_root):
        destination = out_dir / page_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_stub(page_path), encoding="utf-8", newline="\n")
        written.append(page_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / NOT_FOUND_NAME).write_text(
        render_not_found(), encoding="utf-8", newline="\n"
    )
    return written + [NOT_FOUND_NAME]


def _found_html(stub_dir: Path) -> list[str]:
    return sorted(
        path.relative_to(stub_dir).as_posix()
        for path in stub_dir.rglob("*.html")
        if path.is_file()
    )


def check_problems(repo_root: Path, stub_dir: Path) -> list[str]:
    """Every way the tree at ``stub_dir`` fails to be the stub set for the frozen URLs.

    A mechanical lint over generated text, which is the second of the two test shapes
    ``CLAUDE.md`` sanctions.  Three correspondences are checked and a fourth deliberately
    is not:

    * a frozen old URL with no stub -- that URL is cited and would 404 rather than
      redirect;
    * a stub answering no frozen old URL -- it stands in for nothing, the set being one
      that can only shrink;
    * a frozen old URL whose page is no longer published under ``gh-pages/wlc/`` -- the
      stub still redirects, to a page that is not there;
    * a page published under ``gh-pages/wlc/`` that no stub names is NOT a problem.  It
      was published here rather than at the old site, so no citation of it can be a
      wlc-utils URL, and a stub for it would answer nothing.

    Nothing here skips: an absent ``stub_dir``, an empty manifest and an empty published
    set are all failures.
    """
    if not stub_dir.is_dir():
        return [
            f"{stub_dir}: no such directory, so there are no stubs to check."
            " Run `build --out <dir>` first, or name the tree that holds them."
        ]
    expected = redirected_pages(repo_root)
    found = _found_html(stub_dir)
    published = set(published_pages(repo_root))
    problems = [
        f"{page_path}: a frozen wlc-utils URL with no stub at that path in {stub_dir}"
        " -- an old URL that is cited would 404 rather than redirect"
        for page_path in expected
        if page_path not in set(found)
    ]
    problems += [
        f"{stub_path}: a stub in {stub_dir} answering no URL in {_MANIFEST_PATH} --"
        " delete it, or say there why that URL is one wlc-utils published"
        for stub_path in found
        if stub_path != NOT_FOUND_NAME and stub_path not in set(expected)
    ]
    problems += [
        f"{page_path}: a frozen wlc-utils URL whose page is no longer published under"
        f" {_PAGES_PREFIX} -- its stub redirects to a page that is not there. Republish"
        " the page, or drop the URL from the manifest and delete its stub"
        for page_path in expected
        if page_path not in published
    ]
    if NOT_FOUND_NAME not in found:
        problems.append(
            f"{NOT_FOUND_NAME}: absent from {stub_dir} -- every path with no stub of its"
            " own, the deleted non-HTML assets included, depends on that catch-all"
        )
    for stub_path in found:
        problems += _stub_problems(stub_dir / stub_path, stub_path)
    return problems


def _stub_problems(path: Path, stub_path: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if stub_path == NOT_FOUND_NAME:
        return _not_found_problems(text)
    problems = [
        f"{stub_path}: names the target in no {description} -- the stub is incomplete"
        for marker, description in _CARRIERS
        if marker not in text
    ]
    expected = target_url(stub_path)
    named = set(_TARGET_RE.findall(text))
    if named != {expected}:
        problems.append(
            f"{stub_path}: should name {expected} and nothing else, but names"
            f" {sorted(named) or '(no MAM-basics URL at all)'} -- the target has to be"
            " the prefix rewrite of the stub's own path"
        )
    return problems


def _not_found_problems(text: str) -> list[str]:
    """The catch-all's own three requirements, which are not a per-page stub's four.

    It stands in for no one page, so it has neither a canonical link (it answers many
    paths, and each has its own current copy) nor a meta refresh (which takes a fixed URL,
    and the URL here is derived from the path that was asked for).  What it does need is
    the script, the visible link, and the incoming prefix it strips.
    """
    problems = [
        f"{NOT_FOUND_NAME}: names the new site in no {description} -- with that missing"
        " it forwards nothing"
        for marker, description in _CARRIERS
        if marker in ("location.replace(", "<a href=") and marker not in text
    ]
    if OLD_PATH_PREFIX not in text:
        problems.append(
            f"{NOT_FOUND_NAME}: does not name {OLD_PATH_PREFIX!r}, the prefix it has to"
            " strip off the incoming path before prepending the new site"
        )
    if NEW_SITE not in text:
        problems.append(
            f"{NOT_FOUND_NAME}: does not name {NEW_SITE}, so it has nowhere to send"
            " anyone"
        )
    return problems
