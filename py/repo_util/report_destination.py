"""Refuse to write a private repo's findings into a public repo's tracked tree.

MAM-basics is public and is where every cross-repo sweep is RUN, so the path of
least resistance for a report is a file under this repo -- which is exactly the
path that publishes a private repo's internals. Three of the repos
all-repos.code-workspace lists are private (MAM-private, github-misc, hbofonts),
and MAM-private in particular holds six whole evacuated trees, so its findings
name paths like ``near-aleppo/census/adonai_census.py:21``. A repo NAME is not
private (Ben's decision, 2026-08-27); a path inside one is.

The rule, in one sentence: a report covering at least one private repo may be
written only where a public repo will not track it. Three destinations satisfy
that, and ``describe_destination`` names which one applies:

- inside a private repo's working tree -- MAM-private/doc/ is the intended home
  for the batched private half, matching the private review series already kept
  at MAM-private/doc/review-findings-*.md;
- a path git ignores in whatever repo contains it -- .novc/ here, which is where
  a scratch report belongs anyway;
- a path inside no repo at all -- the session scratchpad, %TEMP%.

Anything else raises, and the message names both fixes: split the sweep with
--visibility, or move the destination.

WHY A GUARD RATHER THAN A CONVENTION. The convention already existed and was
already being followed -- the review series split into a public one here and a
private one in MAM-private on 2026-08-26 -- and a convention costs nothing until
the one run that forgets it. A report is written once and committed by whatever
comes next, so the forgetting is silent and the publication is permanent. This
is the same reasoning that put the frozen repos in a directory the sweeps cannot
reach rather than a list they are asked to consult (in/repo_maintenance_policy.json's
location_comment): make the wrong thing unreachable, not merely discouraged.

WHAT THIS DOES NOT COVER, deliberately. It guards the ``--report-json`` and
``--report-txt`` destinations of py/main_repo_util.py, which is the write-back
the sweeps themselves perform. It does not read what a human or an agent later
types into a commit message or a doc/ file, and it cannot: judging whether a
sentence about MAM-private is a leak is not decidable. What it does is remove
the mechanical route, leaving only the deliberate one.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from mb_cmn import provenance
from repo_util.common import run_cmd


class ReportDestinationError(RuntimeError):
    """A report covering a private repo aimed at a public repo's tracked tree."""


def containing_repo(path: Path) -> Path | None:
    """The working tree that would track ``path``, or None if no repo would.

    Walks up from the path's parent looking for a .git entry rather than asking
    git, because the path itself normally does not exist yet -- it is about to be
    written -- and `git rev-parse` on a nonexistent path in a nonexistent
    directory answers about the current directory instead, which is the wrong
    repo and the wrong answer.

    ``.exists()`` rather than ``.is_dir()`` ON PURPOSE, so do not "tighten" it: a linked
    worktree's ``.git`` is a FILE, and a worktree is a working tree that really would
    track the path.  What this returns is therefore a working-tree root, which in a
    worktree is not named for the repo -- see ``repo_name`` below, which is where that
    is resolved.
    """
    for candidate in [path.parent, *path.parent.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def repo_name(repo_dir: Path) -> str:
    """The NAME of the repo whose working tree is ``repo_dir``.

    NOT ``repo_dir.name``, which this used at both call sites until 2026-08-27.  In a
    linked worktree the directory is named for the worktree -- "vibrant-mirzakhani-3e2369"
    -- and never for the repo, so a destination inside a PRIVATE repo's worktree was
    matched against the private-repo names under a name that could not be in the list.

    It failed CLOSED, which is why this was a correctness fix rather than an emergency:
    an unrecognized name skips ``describe_destination``'s "private-repo" branch and falls
    through to "public-tracked", which raises rather than permits.  The worst case was a
    false refusal, never a leak, and no private repo had a worktree that day.

    ``provenance.repo_name_of`` is the same derivation ``this_repo_name`` uses, reused
    rather than reimplemented -- b89fe68 fixed py/tests/test_repo_visibility_declared.py
    this way earlier the same day, and deliberately left this module for later.  It
    follows the worktree's ``.git`` file into the main clone's common git dir and prefers
    the ``remote.origin.url`` basename, so it also survives a renamed clone directory,
    and it degrades to the directory name rather than raising.
    """
    return provenance.repo_name_of(repo_dir)


def _git_ignores(repo_dir: Path, path: Path) -> bool:
    result = run_cmd(["git", "-C", str(repo_dir), "check-ignore", "-q", str(path)])
    return result.returncode == 0


def describe_destination(path: Path, private_repo_names: Iterable[str]) -> str:
    """Classify a destination: 'private-repo', 'ignored', 'no-repo' or 'public-tracked'."""
    private = {name.casefold() for name in private_repo_names}
    resolved = path.resolve()
    repo_dir = containing_repo(resolved)
    if repo_dir is None:
        return "no-repo"
    if repo_name(repo_dir).casefold() in private:
        return "private-repo"
    if _git_ignores(repo_dir, resolved):
        return "ignored"
    return "public-tracked"


def assert_report_destination_ok(
    path: Path | None,
    *,
    covered_repo_names: Sequence[str],
    private_repo_names: Iterable[str],
    option_name: str,
) -> None:
    """Raise if ``path`` would publish a private repo's findings.

    A report covering only public repos may go anywhere; there is nothing to
    protect. The check therefore starts from what the sweep actually covers, not
    from where it is being run.
    """
    if path is None:
        return

    private = {name.casefold() for name in private_repo_names}
    covered_private = sorted(
        name for name in covered_repo_names if name.casefold() in private
    )
    if not covered_private:
        return

    kind = describe_destination(path, private_repo_names)
    if kind != "public-tracked":
        return

    repo_dir = containing_repo(path.resolve())
    # The repo's name, not the directory's: in a worktree the message would otherwise
    # name a directory the reader has never heard of as "the PUBLIC repo".
    named = repo_name(repo_dir) if repo_dir is not None else "?"
    raise ReportDestinationError(
        f"{option_name} would write findings about {len(covered_private)} private"
        f" repo(s) -- {', '.join(covered_private)} -- into {path}, which the PUBLIC"
        f" repo {named} tracks.\n"
        "Two ways to proceed:\n"
        "  1. Split the sweep, which is the intended workflow:\n"
        f"       --visibility public  {option_name} <a path in this repo>\n"
        f"       --visibility private {option_name} "
        "C:\\Users\\BenDe\\GitRepos\\MAM-private\\<path>\n"
        "  2. Keep one sweep and send its report somewhere untracked, such as"
        " .novc/ here, which git ignores."
    )
