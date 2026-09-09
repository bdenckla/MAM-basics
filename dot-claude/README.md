# dot-claude

Tracked copies of the machine-level Claude Code configuration that lives outside any
project repo, in `~/.claude/` (`C:/Users/BenDe/.claude/` on Windows).

| Path in here | Live location |
| --- | --- |
| `user-wide-CLAUDE.md` | `~/.claude/CLAUDE.md` |
| `skills/<name>/` | `~/.claude/skills/<name>/`; shared skills also deploy to `~/.agents/skills/<name>/` for Codex |

**This directory is storage, not something MAM-basics loads.** Nothing here is read by a
session merely because it sits in this repository: the live copies under `~/.claude/` are what
Claude Code loads, and these are the version-controlled originals they are deployed from. That
is why the instruction file is tracked as `user-wide-CLAUDE.md` rather than `CLAUDE.md` —
Claude Code auto-loads a nested `CLAUDE.md` from a directory being worked in, so a file of that
name here would start loading itself beside MAM-basics' own `CLAUDE.md`, which is the confusion
this rename exists to prevent. The same reasoning gives `dot-Codex/user-wide-AGENTS.md` its
prefix. A skill is kept out of `.claude/skills/` for a related reason: a personal skill
shadows a project skill of the same name, so a copy there would be inert on every machine that
has `~/.claude/skills/hebrew-prose/` and would run only in the cloud — the copy you never see
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

`user-wide-CLAUDE.md` holds the user-level instructions that load in **every** repo, every session:
git/commit habits, the no-inline-one-liners rule, black formatting, the Hebrew-accentuation
terminology entries (paseq vs. legarmeh, silluq vs. meteg), Unicode conventions, and the
testing rule. It is the only channel that reaches repos with no `CLAUDE.md` of their own,
and it is where a convention goes when a project's own copy is stranded in a disabled file
(as MAM-basics' black section was).

`skills/` holds **user-level Claude Code skills** — `~/.claude/skills/<name>/SKILL.md` plus
whatever `references/` files it carries. Unlike `CLAUDE.md`, a skill does not load every
session: Claude reads its frontmatter `description` and pulls the body in only when the work
matches. That makes a skill the right home for a long body of rules that would bloat
`CLAUDE.md` if it loaded unconditionally.

Tracked so far:

| Skill | What it is |
| --- | --- |
| `hebrew-prose` | The canonical, on-demand consolidation of the rules for writing and editing prose about Hebrew accentuation and cantillation (atom vs. chanted word, the one-scale maqaf rule, corpus choice, primary-source locations, verification). Supersedes the scattered copies in `~/.claude/CLAUDE.md`, `wlc-utils/CLAUDE.md`, `printed_decalogue_strands.py`'s docstring and the wlc-utils auto-memory — those stay as pointers, and a rule change goes into the skill first. |
| `prune-claude-state` | A manual hygiene pass over Claude Code's *own* persisted state for the current repo — the per-repo auto-memory directory and that repo's slice of the global `~/.claude/plans/`. Cross-checks each file against live GitHub issue state and proposes stale ones for deletion, never deleting without explicit confirmation. Both directories live outside git, so there is no undo. |

## This is the canonical copy; `~/.claude/` is the live working copy

The versions here are canonical — that is what `~/.claude/CLAUDE.md` says of itself, in its
own opening lines — but Claude Code only ever loads what is in `~/.claude/`, and **nothing
syncs the two**. After editing a live file, re-copy it here and commit, or the canonical
copy silently goes stale. This applies to the skills exactly as it does to `CLAUDE.md`:

```powershell
Copy-Item "$HOME/.claude/CLAUDE.md" "$HOME/GitRepos/MAM-basics/dot-claude/user-wide-CLAUDE.md" -Force
```

```powershell
$s = "hebrew-prose"; Remove-Item -Recurse -Force "$HOME/GitRepos/MAM-basics/dot-claude/skills/$s" -ErrorAction Ignore; Copy-Item "$HOME/.claude/skills/$s" "$HOME/GitRepos/MAM-basics/dot-claude/skills/$s" -Recurse
```

The `Remove-Item` is not optional. A plain `Copy-Item <src> <dst> -Recurse -Force` where `<dst>`
**already exists** does not replace it — it copies the source *inside* it, producing
`skills/hebrew-prose/hebrew-prose/`. That works the first time and silently nests on every
re-copy afterwards, which is exactly when you are least likely to look. Deleting first makes the
command idempotent; git will show the real diff either way.

To check whether they have drifted:

```powershell
(Get-FileHash "$HOME/.claude/CLAUDE.md").Hash -eq (Get-FileHash "$HOME/GitRepos/MAM-basics/dot-claude/user-wide-CLAUDE.md").Hash
```

**A shared skill has a third home and this command does not reach it.** `~/.agents/skills/<name>/`
is Codex's live copy, and a two-way check between here and `~/.claude/` passes while Codex reads
something else — which has happened twice, both times to `hebrew-prose`. "Shared-skill deployment
to Claude and Codex" below is the full four-step procedure and both comparisons.

A directory needs a recursive comparison rather than one hash — this reports every file that
differs, is only here, or is only there, and prints nothing when the two are identical:

```powershell
$a = "$HOME/.claude/skills/hebrew-prose"; $b = "$HOME/GitRepos/MAM-basics/dot-claude/skills/hebrew-prose"; Compare-Object (Get-ChildItem -Recurse -File $a | ForEach-Object { "$($_.FullName.Substring($a.Length)) $((Get-FileHash $_).Hash)" }) (Get-ChildItem -Recurse -File $b | ForEach-Object { "$($_.FullName.Substring($b.Length)) $((Get-FileHash $_).Hash)" })
```

Deliberately **not** tracked here: `~/.claude/settings.json` and `settings.local.json`
(they carry per-machine permission allowlists), `projects/` (per-project session
transcripts and auto-memory), and anything else under `~/.claude/` that is state rather
than authored configuration.

## Shared-skill deployment to Claude and Codex

`dot-claude/skills/` is the **single canonical source** for skills shared with Codex.
`~/.claude/skills/<name>/` is the live copy Claude Code loads, `~/.agents/skills/<name>/` is the
live copy Codex loads. Neither live directory is an independent source, and a change has to reach
all three homes.

**Edit the live Claude copy and copy it outwards. Four steps, in this order.** Ben's decision,
2026-09-09, settling a contradiction rather than expressing a preference: this section used to
say "make an edit here first, then deploy the complete canonical skill directory to both live
locations before committing", which is the reverse of what the section above prescribes for a
live file, the reverse of what `~/.claude/CLAUDE.md`'s own opening prescribes for itself, and the
reverse of what sessions do — commit `1925699` of 2026-09-07 and the five of 2026-09-09 that
followed it each edited `~/.claude/skills/hebrew-prose/` and copied outwards from there. Which
order is chosen is fairly arbitrary; that one is specified is not.

1. **Edit `~/.claude/skills/<name>/`**, which is the copy an editing session has actually loaded
   and read.
2. **Copy that directory here**, with the `Remove-Item` guard the section above explains.
3. **Copy it to `~/.agents/skills/<name>/`** as well, with the same guard:

   ```powershell
   $s = "hebrew-prose"; Remove-Item -Recurse -Force "$HOME/.agents/skills/$s" -ErrorAction Ignore; Copy-Item "$HOME/.claude/skills/$s" "$HOME/.agents/skills/$s" -Recurse
   ```

4. **Run both comparisons below, and commit only on a clean result.** They print the differences
   and return a nonzero status when the copies differ:

```powershell
git diff --no-index -- "$HOME/GitRepos/MAM-basics/dot-claude/skills/hebrew-prose" "$HOME/.claude/skills/hebrew-prose"
```

```powershell
git diff --no-index -- "$HOME/GitRepos/MAM-basics/dot-claude/skills/hebrew-prose" "$HOME/.agents/skills/hebrew-prose"
```

Run both comparisons whenever a shared skill changes. A clean comparison is the required
evidence that Claude and Codex will receive the same instructions.
