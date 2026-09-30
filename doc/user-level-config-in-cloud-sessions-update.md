# Updates to `Getting ~/.claude/ into a cloud session`

State: open, first entry 2026-09-13.

## The local deployment is main-sourced; the cloud hook remains branch-sourced

Recorded by Codex on 2026-09-13. This entry corrects the passage beginning
“`dot-claude/` and `dot-Codex/` are **storage**” under “Storage is not load scope, and the layout
says so.” The source document describes the current cloud-session setup and is kept true in place.
This dated entry records the earlier correction rather than freezing the source document.

Ben's four decisions of 2026-09-13 replace the report's live-first local deployment procedure.
For persistent configuration on Ben's machines, edit the tracked canonical copy in a MAM-basics
development checkout, integrate and push the commit, then run
`py/main_repo_util.py --sync-user-config` from the primary MAM-basics clone. The command fetches
`origin`, fails before any live write if the fetch or source validation fails, and deploys both
instruction files and every tracked user-level skill only from the freshly updated
`refs/remotes/origin/main`. `--sync-user-config --check` compares every destination without
changing live configuration, and ordinary `py/main_repo_maintenance.py` runs that check.

The Claude cloud SessionStart hook remains branch-sourced. It uses the user-level configuration
from the cloud session's checked-out branch, not from `main` unless `main` is the checked-out
branch. The hook remains network-free, installs only absent Claude files, and does not install
Codex configuration.

The local deployment and the cloud bootstrap reach no MAM generator or product. Local deployment
replaces files and directories outside Git and is therefore a hard-to-undo act; its complete
source validation, staged replacements and rollback address that risk. The cloud hook writes
only inside its ephemeral container, and its code path cannot be exercised on this machine.

## The cloud hook prepositions the Codex import target beside the current Claude files

Recorded by Codex on 2026-09-14 while implementing MAM-basics issue 274. This entry supersedes the
previous entry's statement that the cloud hook "installs only absent Claude files, and does not
install Codex configuration." The symmetric user-level arrangement gives Claude Code a minimal wrapper that imports the
common instructions from `~/.codex/AGENTS.md`, so a fresh cloud container needs the import target,
the Claude user-level file and the shared `hebrew-prose` skill. The hook prepositions all three
resources. The wrapper conversion was completed by `d695966be8daea270f85424cb77d06f3b92a873d`
on 2026-09-16.

The branch-sourced cloud hook now installs three independently checked resources:

1. `dot-Codex/user-wide-AGENTS.md` to `~/.codex/AGENTS.md`.
2. `dot-claude/user-wide-CLAUDE.md` to `~/.claude/CLAUDE.md`.
3. `dot-claude/skills/hebrew-prose/` to `~/.claude/skills/hebrew-prose/`.

An existing destination remains untouched. In particular, an existing Claude user-level file no longer
makes a missing `~/.codex/AGENTS.md` acceptable, and an existing common file does not suppress
installation of a missing Claude file or skill. The already-present, missing-source, successful-install
and partial-install banners name all three resources. Source validation applies only to a resource
whose destination is absent, so an existing file does not create a needless dependency on its
source during a resumed session.

Local verification used Git Bash's absolute executable path because `bash` is not on this
PowerShell session's `PATH`. `bash -n` accepted the hook. A throwaway harness under `.novc/`
passed the local no-op, empty-home, all-present, Claude-file-present, common-file-present,
incomplete-skill-directory, missing-source, missing-common-source-with-Claude-files-present,
common-source-not-needed, repository-fallback and partial-install cases. The harness compared the
installed files and complete skill tree with their tracked sources and confirmed that pre-existing
sentinel files were not overwritten. This verifies the Windows-hosted fake-home behavior; a real
fresh Claude cloud container must still verify the SessionStart loading behavior, so the cloud code
path remains explicitly cloud-unverified.

The canonical `py/main_test.py` suite then passed with 987 tests passed and 5 semantic skips. The
sandbox account required a per-process Git `safe.directory` value for this worktree and a writable
temporary directory outside the repository; the runner passed both only to the test subprocess and
changed no global Git or Python configuration.

Local `main` advanced by seven New York time-zone commits during that verification. After merging
those commits into the worktree branch, the hook syntax check and every fake-home case passed again,
and the merged tree's canonical suite passed with 988 tests passed and 5 semantic skips.

The hook and documentation reach no declared MAM-basics product. The hook is executable setup code,
so it carries test-breakage risk and receives targeted checks in this worktree. The eventual push
to `main` is outward-facing, and the cloud code path cannot be exercised on this machine; neither
fact changes the product scope.

## 2026-09-28: the wrapper conversion is completed

Recorded by ChatGPT-Codex on 2026-09-28, New York time. **Corrected above.** The source passage
beginning “The symmetric user-level arrangement will give Claude Code a minimal wrapper”
described a future conversion. The conversion landed at
`d695966be8daea270f85424cb77d06f3b92a873d` on September 16, so the retained update now describes
the completed common-body arrangement. This correction performs no new cloud-session check.

## 2026-09-29: all six shared skills approved for cloud installation

Recorded by Codex. **Approved and implemented:** Ben chose to install all six shared skills
with explicit cloud limits, superseding the 2026-09-14 `github-issues` exclusion for
instruction installation. `.claude/hooks/install-user-config.sh` reads the validated
`dot-claude/shared-skills.txt` inventory and copies complete trees, including references.
The common body and Claude wrapper remain independent resources. Existing files are
preserved; available source trees fill missing references. Invalid inventory and resource
failures are reported in session context, and ordinary failure paths exit zero.

The hook remains local-no-op, branch-sourced and network-free. It refuses linked destination
parents, stages missing files and verifies their bytes before publishing without clobbering,
so a failed copy cannot become an accepted partial file on resume. It installs no runtime,
credentials, permissions or sibling clones. Claude-only pruning and Codex-only skills remain
excluded.

Canonical skill guidance now distinguishes portable rules from available workflows. Linux
commands use the selected checkout's environment. Private source claims stay limited by
available evidence. Issue reads capture every comment page through REST; body editing remains
pending under the restricted proxy while the existing helper lacks REST transport. Chapter
downloads require the complete private dependency loop before starting. The detailed approval,
implementation and verification record is
`PLAN-checkout-kinds-and-portable-knowledge-update.md`.

**Local verification passed:** hook syntax, 26 disposable fake-home scenarios, complete
tree and preservation comparisons, REST-recipe capture against an independent comment-page
oracle and the canonical suite (1011 passed, 5 skipped). Linked-parent checks used disposable
Windows junctions because this account lacked native symlink privilege. No product or
workflow executable changed, so no mega was owed.

**Cloud runtime remains unverified:** no real Claude cloud startup or live API operation was
performed on this Windows machine. The historical 2026-09-09 loading measurement above does
not establish loading of the expanded inventory.

**Integrated and deployed:** implementation
`4d3ebf6670295495d715eb3b082026218090979c` was merged with moved documentation-only
`origin/main` and pushed at `50374e651a2a9392e98e8ddfb8c1e0d216311aad`. The merged diff
and receipt-update-link lint passed. Complete canonical deployment changed 12 mappings;
the subsequent fetched comparison reported all 21 mappings clean with zero problems.
The local deployment copies common instructions and skills. The project cloud hook itself
arrives through the checkout and remains subject to the unverified real-cloud limits above.
