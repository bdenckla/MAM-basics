---
name: mam-repository-topology
description: Ben's repository-topology rules for setting up or synchronizing GitRepos, repository maintenance, evacuated repositories, redirect hosts and frozen redirect manifests, sibling-repository locations, clone retirement, and the historical names wlc-utils, UXLC-utils, holman-ketiv-qere, MAM-OSIS, codex-index-aleppo, codex-index-cam1753, codex-index-leningrad, diffable-pointed-hebrew, al-hatorah, masorah-books, and wlc-koren-12th.
---

# MAM repository topology

Use this skill before deciding that a repository should be cloned, restored, moved, removed,
or treated as a sibling dependency. A directory's presence or absence on one machine is not a
topology decision.

## Sources of truth

1. `MAM-basics/in/repo_maintenance_policy.json` defines `gitrepos_setup_rule`,
   `repos_to_keep_absent`, `frozen_repos`, and repository visibility policy.
2. `MAM-basics/all-repos.code-workspace` is the roster that maintenance sweeps can reach.
3. Frozen old-URL sets live in the named JSON manifests under `MAM-basics/in/` and are checked
   by `py/tests/test_redirect_manifest.py` without a source clone.
4. Read `references/evacuated-repositories.md` for the current disposition, exact explicit
   stub-publication procedure, and historical traps for every evacuated repository.
5. Read `references/repository-maintenance.md` for a maintenance sweep, Black coverage, or
   retirement of completed Codex task folders and disposable cache data.

Apply every clause of `gitrepos_setup_rule`, including its exclusions and its listed gists.
Never reconstruct the roster from `gh repo list` or from a disk set difference. If the request
uses a recency criterion, apply that criterion rather than widening it to every missing clone.

## Current operating rules

- An evacuated public repository can remain live as a Pages redirect host or issue tracker
  while its clone belongs on no machine. Do not restore such a clone for ordinary development,
  tests, issue work, or local previews.
- Explicit redirect-stub publication may require a temporary shallow clone of the named host.
  Follow the repository-specific procedure in `references/evacuated-repositories.md`, publish
  and verify the stubs, then safety-check the clone before retiring it.
- `MAM-private/al-hatorah/` and `MAM-private/masorah-books/` are subtrees of MAM-private, not
  sibling clones. Read the full reference before interpreting old `../al-hatorah` or
  `../masorah-books` paths.
- A directory directly under `GitRepos` can be a linked worktree rather than a repository.
  Inspect `git rev-parse --git-common-dir` or the suspected repository's worktree list before
  treating it as an independent clone. `wlc-koren-12th` was a wlc-utils worktree, never a repo.
- Before retiring any clone or worktree, establish that the working tree is clean and that no
  branch, commit, or object is the only copy of recoverable work. Use the Recycle Bin for
  verified task-folder retirement where the maintenance instructions require it.

## Canonical copy

This skill is canonical at `MAM-basics/dot-claude/skills/mam-repository-topology/` and is
shared with Codex through `dot-claude/shared-skills.txt`. Change the canonical copy first, then
use the deployment procedure in `dot-claude/README.md`.
