"""Single __file__-relative source of truth for repo-root paths.

See GitHub issue #75: this replaces both cwd-relative literals
(e.g. "../MAM-parsed") and scattered Path(__file__).resolve().parents[N]
call sites, each of which encoded its own magic depth number. Every
sibling-repo path should be built by /-chaining off repo_root() or
repos_root() instead.

Cross-repo dependencies (MAM-parsed, MAM-simple, MAM-with-doc, MAM-OSIS, wlc-utils,
...) are by default looked up as siblings of this repo under a common parent
directory.  That convention breaks when the repo is checked out somewhere the
siblings are not co-located -- most notably a git worktree, whose root is nested
under ``.../.claude/worktrees/`` rather than next to the sibling repos.  This was not
hypothetical: until 2026-08-01 ``sibling_repo("MAM-parsed")`` in a MAM-basics worktree
resolved to ``.claude/worktrees/MAM-parsed``, a directory that has never existed.

To make sibling lookups overridable without changing default behavior, two kinds
of environment variable are honored, resolved per dependency in this order:

  1. per-repo ``REPO_<NAME>_DIR`` (NAME = the sibling dir name uppercased with
     each run of non-alphanumeric characters replaced by ``_``); else
  2. ``REPOS_ROOT`` joined with the sibling name; else
  3. ``repo_root().parent`` joined with the sibling name (the historical default).

With no environment variables set, resolution is byte-identical to the previous
``repo_root().parent / <name>`` behavior.

The override chain and ``require_sibling`` came from wlc-utils' ``repo_paths.py``,
which was written to fix exactly this and had it working while the module every
MAM-basics program imports stayed broken.  It is absorbed here rather than left in a
wlc-specific file, so one repo's fix is not a second copy of the other's bug.

THE LAYOUT ACCESSORS BELOW -- ``in_dir``, ``out_dir``, ``gh_pages_dir``,
``wlc_pages_dir``, ``novc_dir``, ``scans_dir`` -- and the sibling accessors at the end
of this module arrived from ``py/wlc_paths.py`` on 2026-08-12, when that module was
deleted (Phase 5 of ``doc/PLAN-evacuate-the-rest-of-wlc-utils.md``).  ``wlc_paths`` was
deliberately two-rooted: the code lived in MAM-basics and the corpus it read and wrote
lived in the sibling wlc-utils, so ``wlc_data_root()`` and ``repo_root()`` named
different directories and had to be kept apart by name.  Phase 3 copied that corpus in,
Phase 5 repointed every generator at it, and the two roots became one directory -- which
is why ``wlc_data_root()`` has no successor here.  Every former call site of it says
``repo_root()`` now.
"""

import os
import re
from pathlib import Path

from mb_cmn import provenance

_THIS_FILE = Path(__file__).resolve()


def repo_root() -> Path:
    """Return the MAM-basics repo root (parent of the py/ directory)."""
    return _THIS_FILE.parents[2]


def in_dir() -> Path:
    """This repo's committed-input tree (``<repo_root>/in``)."""
    return repo_root() / "in"


def out_dir() -> Path:
    """This repo's generated-output tree (``<repo_root>/out``)."""
    return repo_root() / "out"


def gh_pages_dir() -> Path:
    """This repo's published-HTML tree (``<repo_root>/gh-pages``).

    THE DEPLOY ROOT, not any one site under it: ``.github/workflows/pages.yml`` hands
    exactly this directory to ``upload-pages-artifact``, so what sits here is what
    ``https://bdenckla.github.io/MAM-basics/`` serves.  A generator writing one section
    of the site wants a subdirectory accessor -- ``wlc_pages_dir`` below is the first --
    rather than this one.
    """
    return repo_root() / "gh-pages"


def wlc_pages_dir() -> Path:
    """The wlc corpus's published pages (``<gh_pages_dir>/wlc``).

    Nested one level under the deploy root, so
    ``bdenckla.github.io/wlc-utils/X`` maps to
    ``bdenckla.github.io/MAM-basics/wlc/X`` by a pure prefix rewrite and this repo's own
    site root stays free.  All 154 pages that arrived from wlc-utils are under here; the
    nesting cost no HTML edit, every internal link in them being relative.
    """
    return gh_pages_dir() / "wlc"


def novc_dir() -> Path:
    """This repo's gitignored scratch tree (``<repo_root>/.novc``).

    Named for the ``.gitignore`` entry rather than for what it holds, because what it
    holds is deliberately unclassified: whatever a run wants to write and nobody wants to
    commit.  An accessor rather than each caller composing ``repo_root() / ".novc"`` -- so
    the string appears once.
    """
    return repo_root() / ".novc"


def scans_dir() -> Path:
    """Where page renderings from the scan archive are written (``<novc_dir>/scans``).

    NOT the scan archive itself, which is a personal collection outside every repo and is
    resolved by ``accgram.scan_page.SCANS`` off ``WLC_SCANS_DIR``.  These are the
    downscaled, cropped derivatives, which are disposable and can be large.
    """
    return novc_dir() / "scans"


def repos_root() -> Path:
    """Base directory under which sibling repos are looked up.

    ``REPOS_ROOT`` if set, else ``repo_root().parent`` -- historically the GitRepos/
    directory holding the sibling MAM-* repos, which is still what it resolves to when
    nothing is set and the checkout is not a worktree.
    """
    override = os.environ.get("REPOS_ROOT")
    if override:
        return Path(override)
    return repo_root().parent


def _env_name(name: str) -> str:
    return "REPO_" + re.sub(r"[^A-Za-z0-9]+", "_", name).upper() + "_DIR"


def sibling_repo(name: str) -> Path:
    """Return the path to a sibling repo, e.g. "MAM-parsed".

    Precedence: per-repo ``REPO_<NAME>_DIR`` -> ``REPOS_ROOT/name`` ->
    ``repo_root().parent/name``.
    """
    per_repo = os.environ.get(_env_name(name))
    if per_repo:
        return Path(per_repo)
    return repos_root() / name


def require_sibling(name: str, path: Path) -> Path:
    """Return ``path``, or raise saying both ways to point this repo at ``name``.

    A MISSING SIBLING IS A MISCONFIGURATION, NOT A REASON TO CHECK LESS.  Nothing runs the
    test suite without the siblings present -- the only CI in these repos is the Pages
    deploy, which runs no tests -- so a cross-repo check that quietly skips on an absent
    sibling reports green having verified nothing.  Fail instead, and make the failure carry
    its own fix: the overrides documented in this module's docstring are the answer, and a
    bare ``FileNotFoundError`` from deep in a loader does not mention them.

    ``path`` is passed in rather than recomputed because a sibling accessor usually wants a
    subtree of the clone (``MAM-parsed/plus``), and the message should name the path actually
    looked for while the override it advertises is keyed to the clone.
    """
    if path.is_dir():
        return path
    # Name the siblings root the lookup actually searches, NOT repo_root(): in
    # the worktree case this override chain exists for, repo_root() is the worktree
    # root, and "clone beside that" is precisely the wrong advice.
    raise FileNotFoundError(
        f"sibling repo {name} not found: no directory at {path}.\n"
        f"Clone {name} under the siblings root, {repos_root()}, or point at it"
        f" explicitly:\n"
        f"  {_env_name(name)}=<path to the {name} clone>\n"
        f"  REPOS_ROOT=<directory holding all the sibling clones>"
    )


def display_path(path) -> str:
    """``path`` as a repo-qualified, machine-independent string, for recording in an artifact.

    ``MAM-basics/out/accgram/prose/_oddballs.json``, ``MAM-simple/json-vtrad-bhs``: the
    repo's name, then the path within it, forward-slashed on every platform.

    AN ABSOLUTE PATH WRITTEN INTO A GENERATED FILE PINS THAT FILE TO ONE MACHINE.
    ``out/accgram/research-oddballs.json`` carried ``C:/Users/BenDe/GitRepos/...``
    in four keys, so it could not regenerate identically anywhere but Ben's laptop -- and
    in a repo where the tracked generated artifact IS the test (CLAUDE.md), that is a test
    nobody else can run.  Found 2026-08-31 by the first cloud run of ``main_0_mega.py``,
    which reproduced all 96 of that file's oddballs and still showed a diff, because the
    four keys now read ``/home/user/...``.

    ``provenance._display_path`` answers the same question for the GENERATOR file and is
    not reusable here: it accepts only paths inside this repo, and a recorded INPUT
    routinely sits in a sibling clone.  The repo NAME still comes from ``provenance`` --
    ``this_repo_name`` for this repo, ``repo_name_of`` for any other -- so a worktree run
    emits the repo's name and not the worktree directory's, which is the bug those two
    functions exist to prevent.

    A path under no repo at all raises.  Falling back to the absolute spelling would
    quietly restore the defect this exists to remove.
    """
    resolved = Path(path).resolve()
    root = repo_root()
    if resolved == root or root in resolved.parents:
        return _repo_qualified(provenance.this_repo_name(), resolved.relative_to(root))
    # Any other repo -- normally a sibling clone, but the ``.git`` search also covers a
    # sibling relocated by REPO_<NAME>_DIR, which no arithmetic off repos_root() would.
    for ancestor in (resolved, *resolved.parents):
        if (ancestor / ".git").exists():
            return _repo_qualified(
                provenance.repo_name_of(ancestor), resolved.relative_to(ancestor)
            )
    raise ValueError(
        f"no machine-independent spelling for {resolved}: it is not under this repo"
        f" ({root}) and no ancestor directory holds a .git"
    )


def _repo_qualified(repo_name: str, relative: Path) -> str:
    """``repo_name`` joined to a repo-relative path, with the repo root itself as bare."""
    rel = relative.as_posix()
    return repo_name if rel == "." else f"{repo_name}/{rel}"


def mam_parsed_path() -> str:
    """Return the MAM-parsed clone, as the string ``read_parsed_plus_bk39s`` wants.

    THE CALLER SUPPLIES THIS PATH BECAUSE THE READER CANNOT.
    ``mb_cmn/read_books_from_mam_parsed_plus.py`` defaults its ``mam_parsed_path``
    argument to the cwd-relative literal ``"../MAM-parsed"``, and that default has to
    stay: the file is vendored verbatim into al-hatorah's ``py/mb_cmn/``, which has no
    ``paths.py`` for it to import, so consulting this module there would be an
    ImportError rather than a policy violation.  The literal is right whenever the repo
    root sits beside its siblings and is the cwd, and wrong in a git worktree, whose
    root is ``.../.claude/worktrees/<name>`` -- so ``"../MAM-parsed"`` resolves to
    ``.claude/worktrees/MAM-parsed``, a directory that has never existed.  Passing the
    path in is what the reader's argument is for, and it puts the override chain this
    module documents back in front of every caller.

    Returned as a ``str`` rather than a ``Path`` because the reader interpolates it into
    ``f"{mam_parsed_path}/plus/{...}.json"``.

    These three lines started as ``scan_pages/check.py``'s own ``mam_parsed_path``, the
    one caller already worktree-correct when the other seventeen were converted on
    2026-08-07; check.py now calls this instead, so there is one copy again.
    """
    clone = sibling_repo("MAM-parsed")
    # Require the subtree the plus reader actually opens, not merely the clone: an
    # empty or half-cloned MAM-parsed should fail here, naming the overrides, rather
    # than as a bare FileNotFoundError on the first book.
    require_sibling("MAM-parsed", clone / "plus")
    return str(clone)


def mam_simple_dir() -> Path:
    """MAM-simple's ``json-vtrad-bhs`` subtree: one JSON per book, verse-element streams."""
    return sibling_repo("MAM-simple") / "json-vtrad-bhs"


def require_mam_simple_dir() -> Path:
    """``mam_simple_dir``, checked -- see ``require_sibling`` for why this is not a skip."""
    return require_sibling("MAM-simple", mam_simple_dir())


def mam_simple_vtrad_mam_dir() -> Path:
    """MAM-simple's ``json-vtrad-mam``: the same text in MAM's native versification.

    ``mam_simple_dir`` above is the BHS versification, which is what this repo's surveys read
    because they are keyed to WLC's refs.  A cross-check against another MAM-derived text numbers
    its verses MAM's way, so it wants this flavour and no remap table.  MAM-simple ships three --
    BHS, Sefaria and MAM native -- and picking the wrong one is what makes versification look like
    a difference between two texts rather than between two numberings of one.
    """
    return sibling_repo("MAM-simple") / "json-vtrad-mam"


def require_mam_simple_vtrad_mam_dir() -> Path:
    """``mam_simple_vtrad_mam_dir``, checked -- see ``require_sibling`` for why this is not a skip."""
    return require_sibling("MAM-simple", mam_simple_vtrad_mam_dir())


def mam_parsed_plus_dir() -> Path:
    """MAM-parsed's ``plus`` subtree: one JSON per book24, minirow cells C/D/E.

    ``mam_parsed_path`` above names the same clone and is not a duplicate of this: it
    returns the clone itself, as the ``str`` that ``read_parsed_plus_bk39s`` interpolates,
    for callers that hand the path to that reader rather than opening files themselves.
    """
    return sibling_repo("MAM-parsed") / "plus"


def require_mam_parsed_plus_dir() -> Path:
    """``mam_parsed_plus_dir``, checked -- see ``require_sibling`` for why this is not a skip."""
    return require_sibling("MAM-parsed", mam_parsed_plus_dir())


def al_hatorah_phonetic_dir() -> Path:
    """al-hatorah's ``io/a01-phonetic-std-set``: Phonetic MAM, one JSON per book.

    Each chanted word has a ``jta`` field whose ``!`` immediately precedes the stressed
    syllable, which is what makes this an independent oracle for ``accgram.final_stress``.  The
    engine behind it is al-hatorah's ``py/aht_phon``, which cannot be imported here -- issue wlc-utils#48
    calls consuming these outputs its second path, and this is that path.

    A subdirectory of MAM-private since 2026-08-10, not a sibling clone of its own: the
    private evacuation programme moved every tracked file of ``bdenckla/al-hatorah``
    under ``MAM-private/al-hatorah/`` and empties that repo to a breadcrumb README
    (``MAM-private/doc/PLAN-evacuate-private-repos.md``, phases R.0-R.4).  So the env
    override that moves this tree is now ``REPO_MAM_PRIVATE_DIR``; ``REPO_AL_HATORAH_DIR``
    no longer reaches it, there being no sibling by that name to resolve.
    """
    return sibling_repo("MAM-private") / "al-hatorah" / "io" / "a01-phonetic-std-set"


def require_al_hatorah_phonetic_dir() -> Path:
    """``al_hatorah_phonetic_dir``, checked -- see ``require_sibling`` for why this is not a skip.

    The clone named is MAM-private, not al-hatorah, so the failure advertises
    ``REPO_MAM_PRIVATE_DIR`` -- the override that actually moves this tree.
    """
    return require_sibling("MAM-private", al_hatorah_phonetic_dir())
