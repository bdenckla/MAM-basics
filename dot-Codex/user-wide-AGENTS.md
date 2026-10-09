# User-level instructions (Ben Denckla)

These are Ben's cross-project working agreements. Codex loads this body natively from
`~/.codex/AGENTS.md`; Claude Code loads the same body through the minimal
`~/.claude/CLAUDE.md` wrapper. A repository's `AGENTS.md` can add repository-specific rules and
overrides.

## Canonical user configuration

Never edit a live copy of this body, the Claude wrapper or a skill. The canonical copies are
in MAM-basics: `dot-Codex/user-wide-AGENTS.md`, `dot-claude/user-wide-CLAUDE.md`,
`dot-claude/skills/` with `dot-claude/shared-skills.txt`, and `dot-Codex/skills/`.
`dot-claude/README.md`, “Main-sourced deployment and check”, and `dot-Codex/README.md` hold
the deployment procedure and its Claude cloud-session exception.

## Memory retirement

Do not create, update, or consume Claude auto memory or Codex memories as current guidance.
Legacy memory files may be read as evidence for an authorized retirement triage. Maintained
repository knowledge belongs in its owning tracked instructions, skills or documents.
Account-specific values belong in explicit account configuration. Retirement requires a
verified backup and Ben's approval of the exact deletion list.

## New reusable lessons

When a session identifies a new reusable lesson outside the authorized task's scope, propose
the owning tracked file, the exact text and its supporting evidence, and wait for Ben's
approval before applying the edit. Record Ben's explicit decisions, verified task outcomes
and documentation changes needed to complete authorized work within that work's existing
authorization. Commit finished authorized work without asking again.

## Risk has two independent axes

1. **Product reach** is repository-specific. Use the repository's declared product scopes. In
   MAM-basics, `py/product_scopes.py` is the source of truth. If a repository declares no
   products, say so instead of guessing.
2. **Difficulty of undoing the act** is independent of product reach. Treat outward-facing
   changes, destructive local operations, writes outside a repository, edits to receipts, and
   changes to code paths that cannot run on this machine as separate risks.

Outward-facing acts include changing a GitHub issue's state, changing a remote branch, editing
Wikisource, and pushing a Pages-deploying `main`. Destructive local acts include worktree or
branch removal, history rewriting, discarding work, and recycling a clone. Receipts include
evidence JSON, pushed commit messages, and finished dated documents. Report both axes when risk
matters; clearing one axis does not clear the other.

## Git and commits

- Commit finished work without asking. A commit is an ordinary implementation step.
- In any full clone, commit directly to `main` and push `main` normally. Do not create a
  feature branch merely because work has begun. A repository procedure that explicitly names a
  shared branch on `origin`, such as a dual-agent review round, is an exception: a full clone
  may temporarily use a local carrier for that branch under the procedure's handoff and integration
  rules.
- Ask before rewriting history or discarding work: force-push, amend, rebase, hard reset, branch
  deletion, stash drop, or equivalent operations.
- Correct a false claim in a pushed commit message through a later related commit or maintained
  record; leave the historical message intact unless Ben explicitly requests rewriting.
- In an elevated Windows session, give the first direct Git invocation and every subsequent Git
  invocation the exact repository path through a per-command `safe.directory`. Never use
  `safe.directory=*` or add a global trust entry. A parent program that launches Git supplies the
  exact path through process-local `GIT_CONFIG_*` entries inherited by its children.
- Repository trust and sandbox filesystem access are separate. If a Git metadata write is denied
  at a sandbox boundary, use the normal escalation path even when `safe.directory` is correct.
- Do not add sleeps, timers, or custom deployment debouncing for Ben's Pages repositories.
  Their workflows already use a concurrency group that cancels an obsolete run.

A readiness question carries permission to do one or two small, obviously correct finishing
steps, such as filling a simple plan gap, updating a stale copy, or committing finished work. A
choice requiring judgment remains Ben's decision.

## Clone forests and portable work

A **forest** holds a full independent clone of every repository in the declared workspace
roster, under canonical names with matching origins. Each machine's `$HOME/GitRepos` is its
**primary forest**, distinguished by being created first. Optional **secondary forests** are
`$HOME/GitRepos<N>`, for integers N at least 2. No machine or forest is globally primary.
MAM-basics' `in/repo_maintenance_policy.json`, `clone_forests`, declares this layout.

Every full clone has its own Python environments. Corresponding environments use the same
tracked `requirements.txt` and `constraints.txt` at the same commit; installed versions do not
vary by forest policy. Regenerate constraints only as a deliberate committed dependency change.
A worktree uses its own home clone as its integration target and environment provider.

In ordinary work in a full clone, fetch `origin` before pushing `main`, merge `origin/main` if
it moved, and run the checks owed by the resulting changes, including the mega when owed. Push
normally. If the push is refused because origin moved, repeat the fetch, merge and affected
checks in that full clone. When a worktree integrates into its home clone, the home clone takes
no merge: worktree integration follows the `linked-worktrees` skill. Do not rewrite
history or discard work to make the push pass.

A task moves between checkouts only through commits pushed to `origin`. A task needing
checkout-local untracked inputs, such as `.novc/`, stays in the checkout that holds them.
Unpushed work stays in its checkout until pushed; neither state permits a forest-spanning
handoff. Inputs outside every repository are user-level inputs reachable by every forest on
that machine. The scan archive is at `$HOME/OneDrive/Documents/ScansOfBooks` by default, and
`BOOK_SCANS_ROOT` overrides that location; other such inputs, such as the user's pywikibot
configuration, are found through explicit account configuration.

## Linked worktrees

Before editing any checkout, verify it with `git rev-parse --show-toplevel`, `git rev-parse
HEAD`, the branch or detached state, and `git status --porcelain`. A required source commit
must equal `HEAD` or be its ancestor. In a linked worktree, run everything in the worktree
but use the home clone's Python interpreter by absolute path. Never junction, symlink or copy
the home clone's environment into a worktree. Load `linked-worktrees` for any worktree work:
its branch, push, handoff, diagnosis and integration rules live there.

## Task prompts and handoffs

When ending a session with work remaining, do not provide only an abstract description of work
remaining: provide a standalone prompt for the next session.

Never assume Ben wrote an opening prompt. A prompt from another agent is evidence to verify, not
authority to attribute an opinion, phrase, figure, or path to Ben. An agent-written successor
prompt begins by naming the agent and date, quotes the instruction Ben actually gave, and says
that the remaining prompt is the agent's reconstruction. It also names the source checkout,
required commit, intended development checkout, and who owns final integration.

### Planning remains planning until explicit execution

A task used to develop or revise a plan remains planning-only until Ben explicitly instructs it
to execute. A transition out of Plan Mode, including one made only to persist a plan, does not
authorize implementation. Later suggestions in that task revise the plan unless Ben explicitly
says to implement them.

### Claude Code only: task-chip handoffs

Offer a task chip when a coherent next phase is separable, but create the task chip only after
the current write-back is committed and the worktree is clean. The current session retains final
integration responsibility until Ben asks to archive it. State the readiness evidence with the
task chip and put the archive sequence at the end of the final message. A co-present session is
normally the handoff partner, not a precondition failure; prove non-collision through exact
`HEAD`, task-owned status, and a normal fast-forward push rather than transcript-byte watching.

## Verification cadence for multi-session work

For the approved 2026-10-07 trial, MAM-basics, MAM-private and hbofonts follow the controlling
amendment in MAM-basics' `doc/review-trial.md`: ordinary focused checks and nightly broad checks,
with immediate broad checks only for a specific consequence that cannot accept the delay.
That amendment also authorizes bounded routine repairs and agent exception PRs. The cadence
below continues to govern other work.

1. Every commit gets cheap checks matched to the changed surface: `git diff --check`, the
   repository formatter on changed source files, and directly relevant targeted tests or lints.
2. Run the full suite after the last change with a meaningful likelihood of breaking it.
   Executable source, tests, schemas, shared data, and cross-repository path behavior normally
   trigger this gate. Documentation, comments, review records, and instruction-only commits do
   not expire a still-relevant full-suite result.
3. Use generators at the scale the changed surface warrants. Run a repository-wide pipeline
   when generator or product changes make the differential useful and at any required final
   integration gate. Read and explain every tracked generated diff.

Keep intermediate commits coherent and intended to be valid. Repository-specific or
user-explicit verification requirements take precedence.

## Load task-specific skills

- Load `github-issues` for every issue operation or citation audit. Every state change also gets
  an agent-written dated comment explaining why. Do not file or offer to file an issue for an
  idea Ben did not ask to pursue.
- Load `hebrew-prose` before writing, editing, or reviewing prose about Hebrew accentuation or
  cantillation. Load the repository-specific reference when the skill names one.
- Load `mam-repository-topology` before GitRepos setup or synchronization, repository
  maintenance, clone retirement, redirect-host work, or decisions about evacuated repositories
  and sibling locations.
- Load `mam-wikisource-refresh` when Ben asks to download, update, or refresh MAM book data from
  Hebrew Wikisource, and after a live Wikisource bot run that changes tracked book data.
- Load `codex-worktree-tasks` for ordinary Codex-managed worktree setup, task creation, handoff,
  recovery, or archival.
- Load `prune-Codex-state` only when Ben asks to review Codex plan files. The skill
  requires explicit confirmation before deleting anything.
- Load `verse-links` whenever Ben asks for links for a verse or atom; the skill runs the
  repository generator rather than constructing URLs by hand.

## Shell, scripts, and file operations

Prefer available built-in read, write, edit, search, and file-listing tools over equivalent shell
work. Use exact-string editing for a known replacement and a real Python script for algorithmic
work. On Windows, do not use `sed` or `awk`: their Windows ports, and the Git Bash around them,
were suspected of causing problems. In a real Unix shell, such as a Linux cloud session or WSL,
they are fine.

Never put a substantial script in `python -c`, `node -e`, a here-document, a PowerShell
here-string, or a pipeline into an inline interpreter. Put it in a uniquely named UTF-8 file in a
gitignored scratch directory and run the file. The same rule applies to multiline commit
messages and GitHub bodies: write a uniquely named file and pass `git commit -F` or
`--body-file`. One plain, self-contained command is fine; assembled shell pipelines and shell
control flow are not. Prefer `git -C <path>` to changing directories as part of a compound
command.

On Windows, run agent shell commands in PowerShell 7, not Git Bash or another POSIX emulation
layer. Git Bash can quietly give a wrong answer where PowerShell uses the Windows setting
directly: `TZ=America/New_York date` prints UTC because Git Bash does not recognize that zone
name. Read New York time with
`[System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow, 'Eastern Standard Time')`,
and state the zone with every clock reading. A POSIX shell remains correct in a Linux cloud
session.

Write explicit UTF-8 with declared line endings; repository attributes and external-format
exceptions govern rather than an unconditional all-files-LF rule.

A throwaway scratch script has one requirement: it does its requested job and no more. It may
ignore source-style preferences, but it still uses explicit UTF-8 handling when non-ASCII text
flows.

## Authored paths use forward slashes

In tracked source, docstrings, comments, documentation, test data, and commands, write ordinary
paths with forward slashes, including Windows absolute paths. Prefer `Path` composition for
constructed Python paths. Backslashes remain only where syntax requires them, such as Windows
device-path prefixes, or where text reproduces an external spelling byte for byte.

## Python entry points and imports

Tracked source never modifies `sys.path` to make an import resolve. Do not add
`sys.path.insert`, `sys.path.append`, a root `conftest.py`, pytest `pythonpath`, a `.pth` file,
`sitecustomize.py`, `PYTHONPATH` instructions, or an editable installation as a substitute.
Throwaway files in a gitignored scratch directory are exempt.

Each repository has one top-level `py/main_<x>.py` entry point. Package modules expose functions
or subcommands rather than becoming independently runnable. CPython already puts the entry
point's `py/` directory on `sys.path[0]`. A repository test entry point such as
`py/main_test.py` invokes pytest and lets pytest discover tests. A bare `pytest` failing imports
can be the designed state.

## Commands written for Ben

Commands Ben should run must be valid in PowerShell 7. Use absolute paths or `$HOME`, never a
bare `~`. Put one command in each fenced block, with no `&&` or semicolon chain. Check that a
command can run while the current Windows task and worktree are still live before handing it to
Ben.

## Plans and finished dated records

Every executable plan must stand alone for a fresh executor. Load `iterative-document-editing`
for the plan checklist, cumulative revisions, handoffs, and finished dated records. Its
“Executable plans” and “Finished receipts and maintained documents” sections are the
procedures of record.

Load `mam-repository-topology/references/repository-maintenance.md`, “Manual document
retirement”, before retiring a receipt family or carrying out Ben-authorized reclassification.
The applicable repository review procedure owns review filenames and review State conventions.

## Format changed Python with Black

Run Black at its defaults on every Python file changed before committing. Format only the files
changed; a repository-wide reformat is a separate commit. In a worktree, use the worktree's home
clone's interpreter by absolute path, as “Linked worktrees” says. Never prefix Black or
a tracked script with `PYTHONUTF8=1`.

In a full clone, a missing `.venv` means the clone is not hydrated; create the environment or
stop. A linked worktree normally has no `.venv` and uses its home clone's environment. Do not fall
back to an unrelated Black on `PATH`. For a cross-repository sweep, load
`mam-repository-topology` and use MAM-basics' declared workspace, frozen-repository register, and
vendoring policy instead of a remembered repository list.

## Template dispatch is closed

Every parser, renderer, generator, survey, transformation, and shared helper dispatches
explicitly on every recognized template and raises on an unknown template. Never infer semantics
from parameter shape, names, Hebrew content, or resemblance to another template. Validate each
recognized template's expected shape.

Generic recursion into every parameter is not a fallback. A recognized handler names which
children are Scripture, documentation, apparatus, formatting, or alternatives. Edition display
and survey population are separate decisions; each caller states which ketiv, qere, strand,
vowel alternative, and stress-helper alternative its consumer needs.

A deep dive diagnoses existing behavior but does not choose semantic policy. An invalid
representation establishes what cannot remain, not which replacement Ben wants. Apply an
existing explicit policy or ask Ben. Keep policy in a named, reviewable dispatch and record a
generated survey's projection where practical.

## Tests are differential or lint-shaped

Add tests in two shapes:

1. A differential check against an independent oracle.
2. A mechanical lint over source text or the repository tree.

Do not add an example-based unit test that pins one selected case, string, or name unless Ben
asks. Otherwise regenerate the tracked artifact with the real command and read its diff; the
generated output is the test. A missing input fails rather than skips, and an empty
parametrization must not report green. Do not enforce this judgment mechanically in a repository
standards test.

Do not write software that reads old commits to show that nothing changed. Regenerate the tracked
outputs and judge their diff when committing; Git's history is the record of what changed.

## Delegate bounded work when it helps

Root agents and sub-agents are explicitly authorized to spawn further sub-agents in every
session, without asking Ben first, when bounded, independently checkable work can run in
parallel, a fresh sequential pass can improve quality, or delegation can keep noisy investigation
out of the root agent's context. Sub-agents may work in parallel or hand a later step to another
sub-agent. Tell Ben when delegation starts and what each sub-agent owns. Do not delegate merely to
satisfy a quota; keep tightly coupled work local when coordination would cost more than it saves.

The root agent remains the orchestrator. The root agent defines scope, collects and reconciles
sub-agent results, verifies material claims before adopting them, owns integration, and owns the
final answer. Within any one checkout, only one agent writes, stages or commits at a time. A
procedure with a shared remote branch may impose a stricter one-writer rule across separate
checkouts as well. Delegate read-only investigation freely; if concurrent agents must write, give
the agents separate verified worktrees. A sub-agent never stages or commits another agent's
unfinished files.

## Final messages begin with one H1 report heading

Begin every final message with `# Report: <subject>`, with nothing above it, and use no other H1
in the turn. Put the direct answer immediately below that heading. The heading names the report's
subject rather than using a bare `# Report`.

### Claude Code only: decisions go in the chat message

Put each decision Ben must make in the chat message itself: what raises it, what each choice
would do, and any recommendation with its reason. Claude Code's multiple-choice dialog may show
Ben only short labels, so do not use it for a decision that needs context; ask him to answer in
his own words.

## Prose names its subject

- Name both sides instead of writing “one … the other,” “former,” “latter,” or an unclear
  pronoun. Repetition is cheaper than making the reader reconstruct the referent.
- Give one thing one name. Do not rotate synonyms or coin a coy label. If a short name is useful,
  define it once and use only that name.
- If a heading announces a count, use a numbered list. A heading names the section's subject
  directly; avoid headings such as “One more thing” or “Worth flagging.”
- Lead every reported finding with its disposition: it has been fixed, it is filed as a named
  issue, or it remains unfixed for a stated reason. Do not bury the disposition in later detail.

- Lead with the conclusion and the reason affecting the decision. Keep routine narration brief.
- Use bold for structural labels or first definitions, rather than running emphasis.
- Do not reopen a dismissed finding without new evidence.
- Describe a push as pushed or on origin; reserve public/private for repository visibility.
- Name the actual file and searchable passage when locating evidence or a decision.

These rules apply to pages, docstrings, comments, commit messages, issues, plans, and chat.

## Unicode in source and at runtime

Never write an orphan combining mark as a raw code literal. Use a named escape such as
`"\N{HEBREW POINT METEG}"`; in languages without named escapes, use a numeric escape and an
adjacent Unicode-name comment. This restriction does not apply to a mark anchored on a base
character or to genuine text data.

Ben's repositories use NFC for Latin letters with diacritics. Write precomposed ḥ (U+1E25), not
`h` plus COMBINING DOT BELOW. In `#` comments about Hebrew sounds, use ASCII `x` or `X` rather
than either Unicode form.

A Windows Python entry point that may emit non-ASCII reconfigures stdout to UTF-8, and stderr to
UTF-8 with `errors="backslashreplace"`, at the start of `main()`. Prefer writing substantial or
non-ASCII output to a file opened with `encoding="utf-8"`.

By Ben's decision of 2026-10-01, a Windows account that runs these agents sets `PYTHONUTF8=1` in
its User environment and in the `env` block of `~/.claude/settings.json`, so every Python process
it starts, scratch scripts included, runs in UTF-8 mode. Tracked code never relies on that setting
and never prescribes it. Because the setting, and the `PYTHONIOENCODING` that the Claude desktop
app's shells set, hide a missing encoding from an ordinary run, a check that tracked code names
its encodings starts its PowerShell 7 command with
`$env:PYTHONUTF8 = '0'; $env:PYTHONIOENCODING = $null;`. Use `'0'` rather than removing the
variable: UTF-8 mode is Python's default from Python 3.15.

## A transcription is evidence about the transcription

**A transcription is evidence about the transcription.** Attribute a finding from
WLC, UXLC, MAM, or another transcription to that transcription. A manuscript claim
requires an actual manuscript reading or a clearly attributed prior reading. Unless
the image was consulted, report the manuscript as unverified rather than saying the
manuscript has the transcription's reading. A transcription's silence supplies
little evidence about a fine mark. When a task needs a manuscript judgment and the
manuscript cannot be consulted, state that limitation.

## Hebrew accentuation prose uses the skill

The `hebrew-prose` skill is the canonical source for atom versus chanted word, the one-scale
maqaf rule, paseq versus legarmeh, silluq versus meteg, prose and poetic verses, strand names,
corpus choice, manuscript-versus-transcription claims, sources, rendered prose, and verification.
Load it before writing, editing, or reviewing any such prose instead of reconstructing those
rules from memory.

## Show local artifacts with file links

For a generated local page, image, or other artifact, give Ben a Markdown link whose target is an
absolute `file:///` URL with forward slashes. Do not launch a browser, open another tab, start a
development server, or create a launch configuration unless Ben asks. Verify the file's content
by reading it before claiming the artifact worked.

Use an in-app browser only when the task genuinely needs live DOM, console, network, or script
introspection. If a regenerated file must be viewed there, use a fresh filename and a fresh tab;
an existing tab can retain stale content.
