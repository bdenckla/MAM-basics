"""Render and lint redirect stubs for pages evacuated to maintained target sites.

The wlc-utils discussion below is the first redirect host's worked example.

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
``document-index/README.md``, hand written -- which since 2026-08-31 are four entries of
this repo's own ``py/author_site/site_data.py``, checked by
``py/tests/test_site_index_links.py``, so that source is now not merely editable but
LINTED.  A fifth source the list missed,
``UXLC-utils/doc/clc-design.md``, is hand written too.  Ben, 2026-08-22: "The stubs are
for things out of my control."  Those three sources are in his control and want the new
URL, not a redirect.  What is genuinely beyond it is tanach.us: the five citations there
are in change proposals Ben submitted and that site publishes, and the copies vendored
back under ``UXLC-utils/in/UXLC-misc/`` are snapshots of what it publishes, so editing one
would falsify the snapshot and change nothing about the citation.

THE REPOINT IS COMPLETE, WHICH IS WORTH RECORDING AS A NEGATIVE RESULT.  A
``git grep bdenckla.github.io/wlc-utils`` over every clone in ``GitRepos``, run 2026-08-22
after the ten links were repointed, returns only two kinds of hit and no third: prose
*describing* the redirect (this docstring, ``CLAUDE.md``, ``mb_cmn/paths.py``, the plans
under ``doc/``, the ``hebrew-prose`` skill), and the tanach.us snapshots named above --
five citations each in ``UXLC-utils/in/UXLC-misc/`` and ``in/UXLC-misc-fixed/``, their
derived ``out/UXLC-misc/`` copies, and this repo's vendored
``in/UXLC-misc/all_changes.json`` and ``in/accgram/uxlc_accent_changes.json``.  So a hit
found later that is neither is a new citation of a dead site, not one this sweep missed.

THE PAGE LIST IS FROZEN, AND CAN ONLY SHRINK

For the wlc-utils row, ``redirected_pages`` reads ``in/wlc_redirect_pages.json``, the
154 paths wlc-utils published at the 2026-08-17 move.  What earns a stub is having been published under
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

Taamey_D is the first non-prefix row. Its manifest explicitly maps the old
``index.html`` to hbofonts' ``Taamey_D.html``; its source host publishes from ``docs/``
rather than ``gh-pages/``; and its catch-all goes to that fixed document rather than
inventing an hbofonts path from an unknown legacy suffix. The row declares each of those
facts. Manifest shape never chooses semantics.

A directory URL is covered only where the directory has an ``index.html``, which is the
right answer rather than an accident: ``document-index/README.md`` cited ``/420422/`` and
``/wlc-a-notes/``, and both hold one, so both get a stub that a bare directory URL
reaches.  (Its successor, this repo's ``py/author_site/site_data.py``, names the
``index.html`` explicitly -- ``py/check_html_syntax_and_sanity.py`` does not resolve a
trailing slash -- but the stubs answer the OLD URLs, which are the ones with the slash.)  ``/accgram/`` holds no ``index.html`` (issue #230 -- it 404s today, and always
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

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import json
import re
import subprocess
from typing import Literal
from urllib.parse import quote, urlsplit

from mb_cmn import paths
from mb_cmn.git_process import git_command


@dataclass(frozen=True)
class RedirectRepo:
    """One evacuated repository whose old published URLs need forwarding stubs.

    A row exists only after the repository's lane captures its frozen manifest. Callers
    select a row explicitly; table order carries no command-line meaning.
    """

    source_repo: str
    scratch_name: str
    old_path_prefix: str
    manifest_path: str
    clone_url: str
    source_published_dir: str
    target_repo: str
    target_site: str
    target_pages_prefix: str
    manifest_kind: Literal["prefix", "mapping"]
    not_found_target: str | None

    def __post_init__(self) -> None:
        parsed_site = urlsplit(self.target_site)
        if (
            parsed_site.scheme not in {"http", "https"}
            or not parsed_site.netloc
            or parsed_site.query
            or parsed_site.fragment
            or not self.target_site.endswith("/")
        ):
            raise ValueError(
                f"{self.source_repo}: target_site must be an absolute HTTP(S) URL"
                " ending in '/'."
            )
        if not self.old_path_prefix.startswith(
            "/"
        ) or not self.old_path_prefix.endswith("/"):
            raise ValueError(
                f"{self.source_repo}: old_path_prefix must start and end with '/'."
            )
        if self.target_repo not in {"MAM-basics", "hbofonts"}:
            raise ValueError(
                f"{self.source_repo}: unknown target repository {self.target_repo!r}."
            )
        if (
            not self.scratch_name
            or "/" in self.scratch_name
            or "\\" in self.scratch_name
        ):
            raise ValueError(
                f"{self.source_repo}: scratch_name must be one directory name."
            )
        _validate_relative_directory(
            self.source_repo, "source_published_dir", self.source_published_dir
        )
        _validate_relative_directory(
            self.source_repo, "target_pages_prefix", self.target_pages_prefix
        )
        if self.manifest_kind == "prefix":
            if self.not_found_target is not None:
                raise ValueError(
                    f"{self.source_repo}: a prefix manifest must use its incoming path"
                    " for the 404 target."
                )
        elif self.manifest_kind == "mapping":
            if self.not_found_target is None:
                raise ValueError(
                    f"{self.source_repo}: a mapping manifest must declare a fixed"
                    " not_found_target."
                )
            _validate_page_path(
                self.source_repo, "not_found_target", self.not_found_target
            )
        else:
            raise ValueError(
                f"{self.source_repo}: unknown manifest_kind {self.manifest_kind!r}."
            )

    @property
    def new_site(self) -> str:
        return self.target_site

    @property
    def pages_prefix(self) -> str:
        return self.target_pages_prefix


def _validate_relative_directory(repo: str, field: str, value: str) -> None:
    path = PurePosixPath(value[:-1]) if value.endswith("/") else PurePosixPath(value)
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or not value.endswith("/")
        or path.is_absolute()
        or ":" in path.parts[0]
        or path.as_posix() != value[:-1]
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise ValueError(
            f"{repo}: {field} must be a nonempty relative POSIX directory ending in '/'."
        )


def _validate_page_path(repo: str, field: str, value: str) -> None:
    path = PurePosixPath(value)
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or path.is_absolute()
        or ":" in path.parts[0]
        or path.as_posix() != value
        or any(part in {".", ".."} for part in path.parts)
        or path.suffix != ".html"
    ):
        raise ValueError(
            f"{repo}: {field} must be a relative POSIX path ending in '.html',"
            f" got {value!r}."
        )


# The redirect-host table. Each lane adds its row only with a manifest captured at the
# source repo's flip.
REDIRECT_REPOS = (
    RedirectRepo(
        source_repo="MAM-OSIS",
        scratch_name="MAM-OSIS",
        old_path_prefix="/MAM-OSIS/",
        manifest_path="in/mam_osis_redirect_pages.json",
        clone_url="https://github.com/bdenckla/MAM-OSIS.git",
        source_published_dir="gh-pages/",
        target_repo="MAM-basics",
        target_site="https://bdenckla.github.io/MAM-basics/MAM-OSIS/",
        target_pages_prefix="gh-pages/MAM-OSIS/",
        manifest_kind="prefix",
        not_found_target=None,
    ),
    RedirectRepo(
        source_repo="MAM-simple",
        scratch_name="MAM-simple",
        old_path_prefix="/MAM-simple/",
        manifest_path="in/mam_simple_redirect_pages.json",
        clone_url="https://github.com/bdenckla/MAM-simple.git",
        source_published_dir="gh-pages/",
        target_repo="MAM-basics",
        target_site="https://bdenckla.github.io/MAM-basics/MAM-simple/",
        target_pages_prefix="gh-pages/MAM-simple/",
        manifest_kind="prefix",
        not_found_target=None,
    ),
    RedirectRepo(
        source_repo="MAM-parsed",
        scratch_name="MAM-parsed",
        old_path_prefix="/MAM-parsed/",
        manifest_path="in/mam_parsed_redirect_pages.json",
        clone_url="https://github.com/bdenckla/MAM-parsed.git",
        source_published_dir="gh-pages/",
        target_repo="MAM-basics",
        target_site="https://bdenckla.github.io/MAM-basics/MAM-parsed/",
        target_pages_prefix="gh-pages/MAM-parsed/",
        manifest_kind="prefix",
        not_found_target=None,
    ),
    RedirectRepo(
        source_repo="MAM-with-doc",
        scratch_name="MAM-with-doc",
        old_path_prefix="/MAM-with-doc/",
        manifest_path="in/mam_with_doc_redirect_pages.json",
        clone_url="https://github.com/bdenckla/MAM-with-doc.git",
        source_published_dir="gh-pages/",
        target_repo="MAM-basics",
        target_site="https://bdenckla.github.io/MAM-basics/MAM-with-doc/",
        target_pages_prefix="gh-pages/MAM-with-doc/",
        manifest_kind="prefix",
        not_found_target=None,
    ),
    RedirectRepo(
        source_repo="MAM-for-Sefaria",
        scratch_name="MAM-for-Sefaria",
        old_path_prefix="/MAM-for-Sefaria/",
        manifest_path="in/mam_for_sefaria_redirect_pages.json",
        clone_url="https://github.com/bdenckla/MAM-for-Sefaria.git",
        source_published_dir="gh-pages/",
        target_repo="MAM-basics",
        target_site="https://bdenckla.github.io/MAM-basics/MAM-for-Sefaria/",
        target_pages_prefix="gh-pages/MAM-for-Sefaria/",
        manifest_kind="prefix",
        not_found_target=None,
    ),
    RedirectRepo(
        source_repo="wlc-utils",
        scratch_name="wlc",
        old_path_prefix="/wlc-utils/",
        manifest_path="in/wlc_redirect_pages.json",
        clone_url="https://github.com/bdenckla/wlc-utils.git",
        source_published_dir="gh-pages/",
        target_repo="MAM-basics",
        target_site="https://bdenckla.github.io/MAM-basics/wlc/",
        target_pages_prefix="gh-pages/wlc/",
        manifest_kind="prefix",
        not_found_target=None,
    ),
    RedirectRepo(
        source_repo="holman-ketiv-qere",
        scratch_name="holman",
        old_path_prefix="/holman-ketiv-qere/",
        manifest_path="in/holman_ketiv_qere_redirect_pages.json",
        clone_url="https://github.com/bdenckla/holman-ketiv-qere.git",
        source_published_dir="gh-pages/",
        target_repo="MAM-basics",
        target_site="https://bdenckla.github.io/MAM-basics/holman/",
        target_pages_prefix="gh-pages/holman/",
        manifest_kind="prefix",
        not_found_target=None,
    ),
    RedirectRepo(
        source_repo="book-of-job",
        scratch_name="book-of-job",
        old_path_prefix="/book-of-job/",
        manifest_path="in/book_of_job_redirect_pages.json",
        clone_url="https://github.com/bdenckla/book-of-job.git",
        source_published_dir="gh-pages/",
        target_repo="MAM-basics",
        target_site="https://bdenckla.github.io/MAM-basics/book-of-job/",
        target_pages_prefix="gh-pages/book-of-job/",
        manifest_kind="prefix",
        not_found_target=None,
    ),
    RedirectRepo(
        source_repo="UXLC-utils",
        scratch_name="uxlc",
        old_path_prefix="/UXLC-utils/",
        manifest_path="in/uxlc_utils_redirect_pages.json",
        clone_url="https://github.com/bdenckla/UXLC-utils.git",
        source_published_dir="gh-pages/",
        target_repo="MAM-basics",
        target_site="https://bdenckla.github.io/MAM-basics/uxlc/",
        target_pages_prefix="gh-pages/uxlc/",
        manifest_kind="prefix",
        not_found_target=None,
    ),
    RedirectRepo(
        source_repo="codex-index-aleppo",
        scratch_name="aleppo",
        old_path_prefix="/codex-index-aleppo/",
        manifest_path="in/codex_index_aleppo_redirect_pages.json",
        clone_url="https://github.com/bdenckla/codex-index-aleppo.git",
        source_published_dir="gh-pages/",
        target_repo="MAM-basics",
        target_site="https://bdenckla.github.io/MAM-basics/aleppo/",
        target_pages_prefix="gh-pages/aleppo/",
        manifest_kind="prefix",
        not_found_target=None,
    ),
    RedirectRepo(
        source_repo="Taamey_D",
        scratch_name="Taamey_D",
        old_path_prefix="/Taamey_D/",
        manifest_path="in/taamey_d_redirect_pages.json",
        clone_url="https://github.com/bdenckla/Taamey_D.git",
        source_published_dir="docs/",
        target_repo="hbofonts",
        target_site="https://bdenckla.github.io/hbofonts/",
        target_pages_prefix="gh-pages/",
        manifest_kind="mapping",
        not_found_target="Taamey_D.html",
    ),
)


def _validate_redirect_repo_table() -> None:
    for field in ("source_repo", "manifest_path"):
        values = [getattr(repo, field) for repo in REDIRECT_REPOS]
        repeated = sorted({value for value in values if values.count(value) > 1})
        if repeated:
            raise ValueError(f"redirect rows repeat {field}: {repeated}")


_validate_redirect_repo_table()

# The catch-all, which is a stub for no page and so is exempt from the correspondence
# check that every other .html in the tree faces.
NOT_FOUND_NAME = "404.html"

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
<!-- GENERATED by py/main_redirect_stubs.py -- do not edit; run that program again. -->
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to {target_repo}: {path}</title>
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
<!-- GENERATED by py/main_redirect_stubs.py -- do not edit; run that program again. -->
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to {target_repo}</title>
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

_FIXED_NOT_FOUND_TEMPLATE = """<!doctype html>
<!-- GENERATED by py/main_redirect_stubs.py -- do not edit; run that program again. -->
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved to {target_repo}</title>
<script>
location.replace("{target}" + location.search + location.hash);
</script>
</head>
<body>
<p>These pages have moved to <a href="{target}">{target}</a>.</p>
</body>
</html>
"""


def redirect_repo(name: str) -> RedirectRepo:
    """The table row named by ``name``, or an argparse-ready error."""
    for repo in REDIRECT_REPOS:
        if repo.source_repo == name:
            return repo
    choices = ", ".join(repo.source_repo for repo in REDIRECT_REPOS)
    raise ValueError(f"unknown redirect repository {name!r}; choose one of: {choices}")


def redirect_repo_names() -> tuple[str, ...]:
    """The source-repository names suitable for argparse choices."""
    return tuple(repo.source_repo for repo in REDIRECT_REPOS)


def source_pages_dir(repo: RedirectRepo) -> Path:
    """``repo``'s declared published tree in its source clone.

    The row carries both the source repository name and its clone URL, so a missing clone
    says precisely how to create a temporary shallow clone. A redirect host is absent from
    the normal workspace roster; its clone exists only while publishing or linting its
    committed stubs.
    """
    clone = paths.sibling_repo(repo.source_repo)
    try:
        return (
            paths.require_sibling(repo.source_repo, clone) / repo.source_published_dir
        )
    except FileNotFoundError as absent:
        raise FileNotFoundError(
            f"{absent}\n"
            "No machine is expected to hold a clone; to get one:\n"
            f"  git clone --depth 1 {repo.clone_url} {clone}"
        ) from absent


def default_out_dir(repo: RedirectRepo) -> Path:
    """Where ``build`` writes when told neither ``--out`` nor ``--publish``.

    A gitignored scratch directory, so the safe destination is the default one and
    publishing into a source redirect host takes saying so.
    """
    return paths.novc_dir() / f"{repo.scratch_name}-redirect-stubs"


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    out: dict[str, object] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key {key!r}")
        out[key] = value
    return out


def redirect_targets(repo_root: Path, repo: RedirectRepo) -> dict[str, str]:
    """The validated old-path-to-target-path mapping frozen for ``repo``.

    Prefix rows deliberately retain the original list-shaped manifest and expand it
    to an identity mapping. Mapping rows must spell both sides explicitly. Dispatch is
    on the row's declared manifest kind, never on the JSON value's resemblance to one
    of those shapes.
    """
    manifest = repo_root / repo.manifest_path
    try:
        data = json.loads(
            manifest.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_json_object,
        )
    except ValueError as exc:
        raise ValueError(f"{manifest}: {exc}") from exc
    if not isinstance(data, dict) or "pages" not in data:
        raise ValueError(f"{manifest} must be an object with a 'pages' member.")
    raw_pages = data["pages"]
    if repo.manifest_kind == "prefix":
        if not isinstance(raw_pages, list) or not all(
            isinstance(page, str) for page in raw_pages
        ):
            raise ValueError(
                f"{manifest} is declared as a prefix manifest, so 'pages' must be a"
                " list of strings."
            )
        if len(set(raw_pages)) != len(raw_pages):
            raise ValueError(f"{manifest} lists a page more than once.")
        targets = {page: page for page in raw_pages}
    elif repo.manifest_kind == "mapping":
        if not isinstance(raw_pages, dict) or not all(
            isinstance(old, str) and isinstance(target, str)
            for old, target in raw_pages.items()
        ):
            raise ValueError(
                f"{manifest} is declared as a mapping manifest, so 'pages' must be an"
                " object whose keys and values are strings."
            )
        targets = dict(raw_pages)
    else:
        raise ValueError(
            f"{repo.source_repo}: unknown manifest_kind {repo.manifest_kind!r}."
        )
    if not targets:
        raise AssertionError(
            f"{manifest} lists no pages: the old URLs the stubs answer are what this"
            " program exists to write, so a run that wrote none of them would report"
            " having written the catch-all and nothing else."
        )
    for old_path, target_path in targets.items():
        _validate_page_path(repo.source_repo, "old page path", old_path)
        _validate_page_path(repo.source_repo, "target page path", target_path)
        if old_path == NOT_FOUND_NAME:
            raise ValueError(
                f"{manifest}: {NOT_FOUND_NAME} is reserved for the generated catch-all."
            )
    return targets


def redirected_pages(repo_root: Path, repo: RedirectRepo) -> list[str]:
    """``repo``'s frozen old URLs, as paths below its old URL prefix.

    Read from the row's validated manifest rather than derived, because the set records
    what the source repo published at its flip and nothing measurable today says that.
    An empty declaration is a failure rather than an empty run: a build that then wrote
    only ``404.html`` would look like it had worked.
    """
    return sorted(redirect_targets(repo_root, repo))


def _target_repo_root(repo_root: Path, repo: RedirectRepo) -> Path:
    """Resolve the explicitly supported target repository for ``repo``."""
    if repo.target_repo == "MAM-basics":
        return repo_root
    if repo.target_repo == "hbofonts":
        target = paths.sibling_repo("hbofonts")
        return paths.require_sibling("hbofonts", target)
    raise ValueError(
        f"{repo.source_repo}: unknown target repository {repo.target_repo!r}."
    )


def published_pages(repo_root: Path, repo: RedirectRepo) -> list[str]:
    """Every page tracked under ``repo``'s declared target published prefix.

    Where a frozen old URL now resolves to. Used only to find a declared target that is
    no longer published: an empty result is a failure rather than an empty run, because
    it means the site is not where this module thinks it is.
    """
    target_root = _target_repo_root(repo_root, repo)
    result = subprocess.run(
        git_command(target_root, "ls-files", "-z", "--", repo.pages_prefix),
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    pages = sorted(
        entry[len(repo.pages_prefix) :]
        for entry in result.stdout.split("\0")
        if entry.endswith(".html")
    )
    if not pages:
        raise AssertionError(
            f"no .html tracked under {repo.pages_prefix} in {target_root}: the pages the old"
            " URLs now resolve to are not where this module looks for them, so every"
            " stub would be reported as pointing at a page that has gone."
        )
    return pages


def target_url(repo_root: Path, repo: RedirectRepo, page_path: str) -> str:
    """The declared target URL for a stub at ``page_path``."""
    target_path = redirect_targets(repo_root, repo)[page_path]
    return repo.new_site + quote(target_path, safe="/")


def render_stub(repo_root: Path, repo: RedirectRepo, page_path: str) -> str:
    return _STUB_TEMPLATE.format(
        path=page_path,
        target=target_url(repo_root, repo, page_path),
        target_repo=repo.target_repo,
    )


def render_not_found(repo: RedirectRepo) -> str:
    if repo.manifest_kind == "prefix":
        return _NOT_FOUND_TEMPLATE.format(
            old_prefix=repo.old_path_prefix,
            new_site=repo.new_site,
            target_repo=repo.target_repo,
        )
    if repo.manifest_kind == "mapping":
        assert repo.not_found_target is not None
        return _FIXED_NOT_FOUND_TEMPLATE.format(
            target_repo=repo.target_repo,
            target=repo.new_site + quote(repo.not_found_target, safe="/"),
        )
    raise ValueError(
        f"{repo.source_repo}: unknown manifest_kind {repo.manifest_kind!r}."
    )


def write_stubs(repo_root: Path, repo: RedirectRepo, out_dir: Path) -> list[str]:
    """Write a stub per old URL plus ``404.html``; return the paths written, site-relative."""
    written = []
    for page_path in redirected_pages(repo_root, repo):
        destination = out_dir / page_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            render_stub(repo_root, repo, page_path), encoding="utf-8", newline="\n"
        )
        written.append(page_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / NOT_FOUND_NAME).write_text(
        render_not_found(repo), encoding="utf-8", newline="\n"
    )
    return written + [NOT_FOUND_NAME]


def _found_html(stub_dir: Path) -> list[str]:
    return sorted(
        path.relative_to(stub_dir).as_posix()
        for path in stub_dir.rglob("*.html")
        if path.is_file()
    )


def check_problems(repo_root: Path, repo: RedirectRepo, stub_dir: Path) -> list[str]:
    """Every way the tree at ``stub_dir`` fails to be the stub set for the frozen URLs.

    A mechanical lint over generated text, which is the second of the two test shapes
    ``CLAUDE.md`` sanctions.  Three correspondences are checked and a fourth deliberately
    is not:

    * a frozen old URL with no stub -- that URL is cited and would 404 rather than
      redirect;
    * a stub answering no frozen old URL -- it stands in for nothing, the set being one
      that can only shrink;
    * a frozen old URL whose declared target is no longer published under the row's
      target prefix -- the stub still redirects, to a page that is not there;
    * a page published under that target prefix that no stub names is NOT a problem. It
      need not have had a URL in the old source repository, so a stub for it may answer
      nothing.

    Nothing here skips: an absent ``stub_dir``, an empty manifest and an empty published
    set are all failures.
    """
    if not stub_dir.is_dir():
        return [
            f"{stub_dir}: no such directory, so there are no stubs to check."
            " Run `build --out <dir>` first, or name the tree that holds them."
        ]
    targets = redirect_targets(repo_root, repo)
    expected = sorted(targets)
    found = _found_html(stub_dir)
    published = set(published_pages(repo_root, repo))
    problems = [
        f"{page_path}: a frozen {repo.source_repo} URL with no stub at that path in {stub_dir}"
        " -- an old URL that is cited would 404 rather than redirect"
        for page_path in expected
        if page_path not in set(found)
    ]
    problems += [
        f"{stub_path}: a stub in {stub_dir} answering no URL in {repo.manifest_path} --"
        f" delete it, or say there why that URL is one {repo.source_repo} published"
        for stub_path in found
        if stub_path != NOT_FOUND_NAME and stub_path not in set(expected)
    ]
    problems += [
        f"{old_path} -> {target_path}: a frozen {repo.source_repo} URL whose target is no"
        f" longer published by {repo.target_repo} under {repo.pages_prefix} -- its stub"
        " redirects to a page that is not there. Republish the target, or drop the old"
        " URL from the manifest and delete its stub"
        for old_path, target_path in sorted(targets.items())
        if target_path not in published
    ]
    if NOT_FOUND_NAME not in found:
        problems.append(
            f"{NOT_FOUND_NAME}: absent from {stub_dir} -- every path with no stub of its"
            " own, the deleted non-HTML assets included, depends on that catch-all"
        )
    for stub_path in found:
        if stub_path == NOT_FOUND_NAME:
            problems += _not_found_problems(
                repo, (stub_dir / stub_path).read_text(encoding="utf-8")
            )
        elif stub_path in targets:
            problems += _stub_problems(repo_root, repo, stub_dir / stub_path, stub_path)
    return problems


def _stub_problems(
    repo_root: Path, repo: RedirectRepo, path: Path, stub_path: str
) -> list[str]:
    text = path.read_text(encoding="utf-8")
    expected = target_url(repo_root, repo, stub_path)
    expected_carriers = (
        (f'rel="canonical" href="{expected}"', "canonical link"),
        (f'http-equiv="refresh" content="0; url={expected}"', "meta refresh"),
        (f'location.replace("{expected}" +', "script"),
        (f'<a href="{expected}">', "visible fallback link"),
    )
    problems = [
        f"{stub_path}: does not name {expected} in its {description} -- the stub is"
        " incomplete or names the wrong target"
        for fragment, description in expected_carriers
        if fragment not in text
    ]
    named = set(re.findall(r"https?://[^\"'\s<>]*", text))
    if named != {expected}:
        problems.append(
            f"{stub_path}: should name {expected} and nothing else, but names"
            f" {sorted(named) or '(no target URL at all)'} -- the target must come from"
            f" the {repo.manifest_kind} contract in {repo.manifest_path}"
        )
    return problems


def _not_found_problems(repo: RedirectRepo, text: str) -> list[str]:
    """The catch-all requirements, which are not a per-page stub's four.

    It stands in for no one page, so it has neither a canonical link (it answers many
    paths) nor a meta refresh. A prefix row's script preserves the unknown suffix after
    stripping the incoming prefix; a mapping row names its declared fixed target. Both
    forms need a script and visible link.
    """
    if repo.manifest_kind == "prefix":
        problems = [
            f"{NOT_FOUND_NAME}: names the new site in no {description} -- with that missing"
            " it forwards nothing"
            for marker, description in _CARRIERS
            if marker in ("location.replace(", "<a href=") and marker not in text
        ]
        if repo.old_path_prefix not in text:
            problems.append(
                f"{NOT_FOUND_NAME}: does not name {repo.old_path_prefix!r}, the prefix it"
                " has to strip off the incoming path before prepending the new site"
            )
        if repo.new_site not in text:
            problems.append(
                f"{NOT_FOUND_NAME}: does not name {repo.new_site}, so it has nowhere to"
                " send anyone"
            )
        return problems
    if repo.manifest_kind == "mapping":
        assert repo.not_found_target is not None
        expected = repo.new_site + quote(repo.not_found_target, safe="/")
        problems = []
        for fragment, description in (
            (f'location.replace("{expected}" +', "script"),
            (f'<a href="{expected}">', "visible fallback link"),
        ):
            if fragment not in text:
                problems.append(
                    f"{NOT_FOUND_NAME}: does not name {expected} in its {description}"
                )
        named = set(re.findall(r"https?://[^\"'\s<>]*", text))
        if named != {expected}:
            problems.append(
                f"{NOT_FOUND_NAME}: should name {expected} and nothing else, but names"
                f" {sorted(named) or '(no target URL at all)'}"
            )
        return problems
    raise ValueError(
        f"{repo.source_repo}: unknown manifest_kind {repo.manifest_kind!r}."
    )
