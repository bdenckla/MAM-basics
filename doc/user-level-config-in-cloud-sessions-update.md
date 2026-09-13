# Updates to `Getting ~/.claude/ into a cloud session`

State: open, first entry 2026-09-13.

## The local deployment is main-sourced; the cloud hook remains branch-sourced

Recorded by Codex on 2026-09-13. This entry corrects the passage beginning
“`dot-claude/` and `dot-Codex/` are **storage**” under “Storage is not load scope, and the layout
says so.” The source document is a finished dated report and remains unchanged.

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
