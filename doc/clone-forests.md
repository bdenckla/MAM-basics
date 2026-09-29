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
checkout, a branch other than `main`, ahead/diverged history or dependency drift returns failure.
Runtime occupancy is reported separately; checking an occupied clone is permitted.

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
are fetched and fast-forwarded. Ineligible clones and their environments stay untouched; other
roster entries continue. The command never resets, stashes, switches branches, forces refs,
deletes paths or replaces an existing environment. It does not commit or push a repository.

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
stays in its checkout; external inputs use explicit user-level account configuration.

After building a secondary forest, use that forest's MAM-basics environment to run the suite
and mega. Require no unexplained tracked output change, then check `--forest-status` and
`--sync-user-config --check`. A current suite or mega result belongs to its exact checkout and
commit; it does not establish that a different forest has been verified.
