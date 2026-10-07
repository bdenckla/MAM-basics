# Full clone forests and dependency constraints

State: runbook. Ben approved the forest and pinning policy on 2026-09-29.

`in/repo_maintenance_policy.json`, `clone_forests`, declares the layout. Each machine's
`$HOME/GitRepos` is its primary forest; optional `$HOME/GitRepos<N>` forests have integer N
at least 2. Every forest holds the canonical repository names in `all-repos.code-workspace`
with matching origins. No machine or forest is globally primary. Forest creation is separate
from worktree retirement; an existing forest is not a disposable task directory.

## Synchronization

Run these commands from a full MAM-basics clone with its own environment. The complete roster
always comes from `all-repos.code-workspace`; sweep selection flags do not narrow a forest.

```powershell
./.venv/Scripts/python.exe py/main_repo_util.py --sync-forest $HOME/GitRepos2 --check
```

This fetches remote refs and reports clone, branch, local-change, Git-operation and environment
state. It does not clone, merge or install packages. A missing clone or environment, a dirty
checkout, a branch other than `main`, a Git operation in progress or one of five named Git lock
files (`index.lock`, `HEAD.lock`, `config.lock`, `refs/heads/main.lock` and
`refs/remotes/origin/main.lock`), history behind, ahead of or diverged from `origin/main`, or
dependency drift returns failure. Runtime occupancy is reported separately; checking an
occupied clone is permitted.

```powershell
./.venv/Scripts/python.exe py/main_repo_util.py --sync-forest $HOME/GitRepos2
```

The write form clones missing repositories from each verified source sibling's origin. Source
siblings are beside the invoking checkout's home clone, including for linked worktrees. A
missing source sibling or origin fails loudly rather than guessing a URL. Initial machine
bootstrap therefore creates the roster clones using `gitrepos_setup_rule` before this operation
can use their origins; the synchronizer can then hydrate that primary forest or build another.

Existing targets must be independent full clones with matching origins, clean `main`, no Git
operation or lock, no unpushed/diverged commits and no active writer evidence. Eligible clones
are fetched and fast-forwarded. A clone that is dirty, off `main`, mid-operation, locked or
occupied is refused before any fetch. A clone refused only because its history is ahead of or
diverged from `origin/main` is fetched first: the fetch adds any missing objects, rewrites
`FETCH_HEAD`, and creates or fast-forwards `refs/remotes/origin/main`. A clone whose
`origin/main` history was rewritten is fetched and refused with that ref retained. Every refused
clone keeps its local branches, checkout and environments; other roster entries continue. The
command never resets, stashes, switches branches, forces refs, deletes paths or replaces an
existing environment. It does not commit or push a repository.

One occupied clone is skipped rather than refused, even when it is dirty, off `main`,
mid-operation or locked: the clone that only the calling Claude session occupies. The write form
recognizes that session when the `CLAUDE_CODE_SESSION_ID` and `CLAUDE_PID` variables that Claude
Code gives its tool processes match the `sessionId` and `pid` of a session record whose working
directory is in the clone. The write form reports that clone
as `FOREST_REPO_SKIPPED`, leaves it unfetched and untouched, and does not count it as a problem,
so the command exits 0 when every other clone succeeds. The session updates its own clone with
ordinary Git. A calling session that works in a linked worktree under the clone, such as one
under `.claude/worktrees/`, also counts as that worktree's occupancy, so the write form refuses
the clone. Any other session, lease or worktree occupancy in the same clone keeps the refusal.

```powershell
./.venv/Scripts/python.exe py/main_repo_util.py --forest-status
```

This discovers the primary and numbered secondary forests under the account home, checks each,
and attributes registered external worktree sessions to their home forest. Runtime formats
can change; unreadable installed records block writes rather than proving inactivity.

## Environments

Each tracked development `requirements.txt` has a tracked sibling `constraints.txt` and an
independent `.venv` beside it. MAM-basics' distributed product directories, declared in
`py/product_scopes.py`, contain consumer inputs rather than extra development environments.
For example, `MAM-simple/requirements.txt` is excluded from hydration. Requirements name
direct dependencies; constraints pin direct and indirect
versions selected from a validated environment. Matching checkouts use the same tracked pins;
versions do not vary by forest policy. A constraints entry does not require installation of an
otherwise unnecessary package. Verification requires the direct requirements, installed
version agreement, no unpinned installed application packages, no system-site dependencies,
and `pip check` success. Requirements use named packages with optional version ranges and
environment markers; extras and direct URLs are unsupported and fail before hydration.

Missing environments are freshly created and installed with `-r requirements.txt -c constraints.txt`.
Existing environments are inspected; incomplete or drifting environments are reported for
deliberate repair. A failed install leaves its partial directory visible and is never reported
as complete. Git and Python subprocesses have bounded execution time and noninteractive settings.

From a full MAM-basics clone, the Windows setup is:

```powershell
pwsh -File ./misc/requirements-venv-setup-windows.ps1
```

Linked worktrees normally have no environment. They run their own scripts from their own roots
with their home clone's interpreter named by absolute path. Never copy or junction an environment.

To deliberately regenerate pins after validating a dependency change, capture the owning
environment's `-m pip freeze` output in a uniquely named scratch script and write
`constraints.txt` explicitly as UTF-8 with LF line endings. Review and commit the new
constraints; reinstall corresponding environments deliberately.
`pip freeze` records installed packages and is not a cross-platform lockfile. Check each intended
Python/platform combination rather than claiming Windows verification also proves cloud setup.
MAM-private and hbofonts document their own environment setup. Forest synchronization never
reinstalls an existing environment or silently regenerates its constraints.

## Work and verification

Ordinary work in any full clone commits on `main`. Fetch and merge moved `origin/main`, run the
checks owed by the merged changes, and push normally; repeat if the push is refused. A worktree
integrates into its own home clone through the repository's verified fast-forward procedure.
Only pushed tracked state moves through `origin`. A task needing checkout-local untracked inputs
stays in its checkout; external inputs are user level: the scan archive at its default location,
which `BOOK_SCANS_ROOT` overrides, and explicit account configuration such as pywikibot's.

After building a secondary forest, use that forest's MAM-basics environment to run the suite
and mega. Require no unexplained tracked output change, then check `--forest-status` and
`--sync-user-config --check`. A current suite or mega result belongs to its exact checkout and
commit; it does not establish that a different forest has been verified.
