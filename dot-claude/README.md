# dot-claude

Tracked copies of the machine-level Claude Code configuration that lives outside any project
repo, in `~/.claude/` (`C:/Users/BenDe/.claude/` on Windows). The Claude instruction file is a
minimal wrapper around the single common user-level body in `dot-Codex`.

Full clone forests and their own environments follow `doc/clone-forests.md`. Canonical
configuration deployment runs from any full MAM-basics clone after the changes are pushed.
Codex's `dot-Codex/retired-skills.txt` declares explicit live skill removals; checks report
remaining retired destinations, and deployment includes removal in its verified rollback
transaction. Other personal skills remain untouched.

| Path in here | Live location |
| --- | --- |
| `user-wide-CLAUDE.md` | `~/.claude/CLAUDE.md` |
| `skills/<name>/` | `~/.claude/skills/<name>/`; shared skills also deploy to `~/.agents/skills/<name>/` for Codex |

**This directory is storage, not something MAM-basics loads.** Nothing here is read by a session
merely because it sits in this repository. Claude Code loads the deployed wrapper at
`~/.claude/CLAUDE.md`; that wrapper imports the deployed common body at `~/.codex/AGENTS.md`.
The version-controlled sources are `dot-claude/user-wide-CLAUDE.md` for the wrapper and
`dot-Codex/user-wide-AGENTS.md` for the common body. The wrapper is tracked with the
`user-wide-` prefix because a nested file named `CLAUDE.md` would auto-load beside MAM-basics'
own repository wrapper; the same reasoning keeps the common body from being tracked as a second
nested `AGENTS.md`. A skill is kept out of `.claude/skills/` for a related reason: a personal
skill shadows a project skill of the same name, so a copy there would be inert on every machine
that has `~/.claude/skills/hebrew-prose/` and would run only in the cloud — the copy you never see
being the one that executes.

**These trees lived in `github-misc` until 2026-09-09**, beside its `dot-emacs` and
`dot-gitconfig` files, which is the precedent that put them there — `f1078d5` of 2026-07-25
gives that precedent and the absence of any version control as the reasons, and privacy as
none of them. They moved because a Claude cloud session reaches only the repositories attached
to it: `github-misc` is private and unattached, so a session on MAM-basics cannot clone it,
while MAM-basics itself arrives with the session. See
`doc/user-level-config-in-cloud-sessions.md` for the measurement and for how a cloud session
installs these files. The commits stay in `github-misc`'s history, so a `github-misc <sha>`
citation in any of these files is right as written and must not be repointed.

`user-wide-CLAUDE.md` contains exactly `@~/.codex/AGENTS.md` plus a final newline. The imported
common body holds the user-level instructions that load in every repository and session. The
wrapper never becomes a second instruction body, and the common body never imports the wrapper.

`skills/` holds **user-level Claude Code skills** — `~/.claude/skills/<name>/SKILL.md` plus
whatever `references/` files it carries. Unlike the common body imported by `CLAUDE.md`, a skill
does not load every session: Claude reads its frontmatter `description` and pulls the body in
only when the work matches. That makes a skill the right home for a long specialized procedure
that would bloat the common body if it loaded unconditionally.

Tracked so far:

| Skill | What it is |
| --- | --- |
| `github-issues` | The rules for touching a GitHub issue in Ben's repositories — reading one in full, filing one, commenting on one, correcting a stale fact in an open issue's body with MAM-basics' `py/main_github_issue_edit.py`, closing, reopening, relabelling or reassigning one with a comment saying why, and citing issues. Took over the former user-wide section "Never change an issue's state without a comment saying why" and two MAM-basics memory notes; the common body's "Load task-specific skills" section now routes issue work here. Added and shared with Codex by Ben's 2026-09-14 decisions. Ben superseded that day's cloud exclusion on 2026-09-29: install the rules with explicit transport limits, including the current body-editor restriction. |
| `hebrew-prose` | The canonical, on-demand consolidation of the rules for writing and editing prose about Hebrew accentuation and cantillation (atom vs. chanted word, the one-scale maqaf rule, corpus choice, primary-source locations, verification). Supersedes the former scattered copies in the old full `~/.claude/CLAUDE.md`, `wlc-utils/CLAUDE.md`, `printed_decalogue_strands.py`'s docstring and the wlc-utils auto-memory — current instruction bodies keep routing pointers, and a rule change goes into the skill first. |
| `iterative-document-editing` | The shared workflow for evolving multi-turn or multi-session documents, including cumulative revisions, planning and execution separation, and one-writer handoff. |
| `mam-repository-topology` | The on-demand rules for GitRepos setup and maintenance, evacuated repositories, redirect hosts and frozen manifests, sibling-repository locations, and clone-retirement traps. The repository keeps a short routing pointer in `AGENTS.md`; detailed current and historical dispositions live with the skill. |
| `mam-wikisource-refresh` | The safe end-to-end workflow for refreshing MAM book data from Hebrew Wikisource, including the dependent refresh after a live bot run, auditing generated products, and regenerating change logs only after the refreshed data has been committed. |
| `prune-claude-state` | A manual review of this repository's global Claude draft plans against live tracked state and complete relevant issues; deletes only an exact approved list. |
| `verse-links` | Runs MAM-basics' `py/main_verse_links.py` for every link Ben asks for when he looks a verse or an atom up — mgketer.org, MAM-with-doc, MAM on Wikisource, masoretica.org for the Aleppo and Leningrad codices, mechon-mamre.org, tanach.us, Sefaria's image of the Leningrad Codex folio with the estimator's column and line, and Chabad's CTR where MAM-basics records the chapter — and says how to present them. Added 2026-09-10 and shared with Codex, both Ben's decisions of that day. |

## Windows desktop diagnostics

An old AppData redirection observation is stale until reproduced. If the observation is useful
to a current diagnosis, record the runtime, date, reproduction and configuration home. Do not
turn the observation into permanent installation policy.

## Main-sourced deployment and check

The common body, wrapper, and skills have tracked canonical copies, and Claude Code loads their
deployed destinations. Ben's decision, 2026-09-13: **edit the tracked canonical copy, never the
live copy.** Commit the edit in its MAM-basics development checkout, integrate it into `main`,
and push `main`. Then run the deployment from any full MAM-basics clone with its own environment:

```powershell
./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config
```

The command fetches `origin` and uses only the freshly updated
`refs/remotes/origin/main`. A fetch failure or invalid source stops before any live write. The
source includes the common instruction body, the Claude wrapper, the user-level Codex hook,
every Claude-specific and Codex-specific skill, and both destinations of every shared skill. The
operation generates the hook's expected user-wide-AGENTS fingerprint from the same `origin/main`
source. The operation validates all sources first, stages all changed destinations, replaces
complete skill directories instead of nesting them, and rolls earlier replacements back if a
later replacement fails.

The read-only form uses the same fresh source and reports `clean`, `drift`, or `not installed` for
every destination:

```powershell
./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check
```

Ordinary `py/main_repo_maintenance.py` runs that check automatically, verifies the installed
Codex hook and fingerprint, and runs the hook's instruction-size check in maintenance mode. A
failed check changes no live configuration and does not stop the maintenance script's later
steps.

The cloud SessionStart hook is the explicit exception. A cloud session gets the user-level
configuration from its checked-out branch, not from `main` unless `main` is the checked-out
branch. The hook remains network-free and does not overwrite a file already present in the cloud
home. By Ben's 2026-09-29 decision it reads `shared-skills.txt` and installs all six declared
shared skill trees, including their references. It fills missing files in an incomplete tree
while preserving existing files, and reports each resource independently. Claude-only pruning
and Codex-only skills remain outside its inventory. Installation supplies rules, without
provisioning environments, siblings, credentials or permissions. The skills require the
available Linux runtime, complete issue reads through supported transport and the full private
dependency loop before a chapter refresh. The current issue-body helper remains unavailable
under the restricted cloud proxy; installation does not bypass that helper.

The former procedure was live-first from 2026-09-09 through 2026-09-13. That procedure could put
branch-only text into files every local session loads and twice left Codex's shared-skill home
behind. The main-sourced operation replaces that procedure rather than adding another direction
to it.

Deliberately **not** tracked here: `~/.claude/settings.json` and `settings.local.json`
(they carry per-machine permission allowlists), `projects/` (per-project session transcripts and
auto-memory), and anything else under `~/.claude/` that is state rather than authored
configuration.

## Shared skills deploy to Claude and Codex

`dot-claude/skills/` is the canonical source for Claude skills. Every directory there deploys to
`~/.claude/skills/`. `dot-claude/shared-skills.txt` names the skills that also deploy to
`~/.agents/skills/`; the declaration currently names `github-issues`, `hebrew-prose`,
`iterative-document-editing`, `mam-repository-topology`, `mam-wikisource-refresh` and
`verse-links`.
`dot-Codex/skills/` is the canonical source for Codex-specific skills and deploys only to
`~/.agents/skills/`.

Do not copy a shared skill separately. The complete `--sync-user-config` operation deploys every
declared home in one transaction, and `--check` compares every declared home. Adding a skill
requires adding its canonical directory; adding a Codex destination for a Claude skill also
requires adding that skill's directory name to `dot-claude/shared-skills.txt`. The cloud hook
also consumes that declaration. Audit a new shared skill's cloud applicability and runtime
requirements before declaring it; installation alone does not make its operations available.
