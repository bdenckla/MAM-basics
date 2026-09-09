"""Run ``git_worktree_cleanup`` across every repo in a workspace file.

WHY A CROSS-REPO SWEEP EXISTS AT ALL. The per-repo home for this is a repo's own
``py/main_repo_maintenance.py`` step, and that is still the right place for a repo
that has one. But an agent session leaves a worktree behind in whatever repo it
ran in, and plenty of the repos in ``all-repos.code-workspace`` have no Python and
so can have no maintenance script -- wlc-utils above all, which was emptied of
Python on 2026-08-01 while agents go on editing its ``doc/`` and ``gh-pages/``.
Without this action its worktrees and ``claude/*`` branches would accrue with
nothing anywhere able to remove them.

Everything conservative about the removal lives in ``git_worktree_cleanup`` and is
unchanged here: this module chooses the repos and prints, it does not decide what
is safe to delete. A repo whose cleanup errors is named at the end and sets the
exit status, in the same shape ``run_black.py`` uses, rather than being passed over
in silence -- but a worktree SPARED for any of the reasons that module documents is
not an error and does not count.

``STRANDED_BRANCH_COUNT=`` is the exception to that shape, and deliberately so. It
names remote ``claude/*`` branches holding work no local clone has -- the end state
of a cloud session, which can only push its own branch -- and those are reported,
never removed, so the line is information and touches neither ``report.errors`` nor
the exit status. ``STRANDED_CHECK_STALE_REPOS=`` follows it when a repo's fetch
failed, because a zero read off refs that could not be refreshed is not the same
fact as a zero read off current ones. Both appear only when they have something to
say; the per-repo lines say which refs each check read either way.
"""

from __future__ import annotations

from repo_util import git_worktree_cleanup
from repo_util.repo_selection import RepoInfo


def problem_repos(reports: list[tuple[str, list[str]]]) -> list[str]:
    """Names of repos whose cleanup reported an error, in report order."""
    return [name for name, errors in reports if errors]


def run_clean_worktrees_across_repos(
    repo_infos: list[RepoInfo],
) -> list[tuple[str, list[str]]]:
    reports: list[tuple[str, list[str]]] = []
    # One entry per stranded remote branch, holding the repo it is in: the count
    # and the repo names both fall out of it, in report order. Kept out of
    # `reports` on purpose -- `reports` feeds `problem_repos`, and a stranded
    # branch must not set the sweep's exit status.
    stranded: list[str] = []
    stale_remote: list[str] = []

    for repo_info in repo_infos:
        # EVERY SWEEP PRINTS THIS LINE, AND THIS IS THE COPY THE OTHERS CITE.
        # Until 2026-08-11 this sweep was the only one of the five that did, and
        # the silence of the other four cost a real session: on that day a phase
        # of the private-repo evacuation read --check-repo-standards' five
        # minutes of no output as a hang and stopped the run, which was neither
        # hung nor unusually slow. A sweep that prints nothing until it finishes
        # is indistinguishable from a hung one from outside.
        #
        # flush=True is not decoration. Python block-buffers stdout whenever it
        # is redirected to a file or captured by a tool, which is exactly the
        # case that misread the silence, so without the flush these lines would
        # sit in the buffer and arrive with the summary at the end -- present in
        # the transcript, useless as progress.
        #
        # The KEY=value summary lines below are unaffected: "=== <repo> ===" is
        # not a KEY=value pair, and this sweep has printed it alongside
        # REPO_COUNT= since long before the other four followed.
        print(f"=== {repo_info.name} ===", flush=True)
        try:
            report = git_worktree_cleanup.clean_worktrees(repo_info.path)
        except (RuntimeError, OSError) as exc:
            # An unreadable repo is reported like any other failure rather than
            # ending the sweep: one wedged repo must not stop the rest.
            print(f"worktrees: ERROR {exc}")
            reports.append((repo_info.name, [str(exc)]))
            continue
        git_worktree_cleanup.print_report(report)
        reports.append((repo_info.name, list(report.errors)))
        stranded.extend(repo_info.name for _ in report.stranded_branches)
        if report.remote_refs_stale:
            stale_remote.append(repo_info.name)

    print(f"REPO_COUNT={len(reports)}")
    problems = problem_repos(reports)
    if problems:
        print(f"WORKTREE_PROBLEM_COUNT={len(problems)}; REPOS={', '.join(problems)}")
    if stranded:
        # Information, not a failure: nothing here touches the exit status. The
        # count is of branches and REPOS names where they are, so one repo
        # holding two of them reads correctly.
        names = ", ".join(dict.fromkeys(stranded))
        print(f"STRANDED_BRANCH_COUNT={len(stranded)}; REPOS={names}")
    if stale_remote:
        # Printed only when a fetch was attempted and failed, so a zero above is
        # a zero as of that repo's last fetch rather than as of now.
        print(f"STRANDED_CHECK_STALE_REPOS={', '.join(stale_remote)}")

    return reports
