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
"""

import os
import re
from pathlib import Path

_THIS_FILE = Path(__file__).resolve()


def repo_root() -> Path:
    """Return the MAM-basics repo root (parent of the py/ directory)."""
    return _THIS_FILE.parents[2]


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
