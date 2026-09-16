# User-level instructions (Ben Denckla)

These are Ben's cross-project working agreements. A repository's `AGENTS.md` can add
repository-specific rules and overrides.

## Canonical user configuration

The canonical repository path is `dot-Codex/user-wide-AGENTS.md` in MAM-basics. The live file
`~/.Codex/AGENTS.md` is a deployed copy; never edit it directly. Edit the canonical file in the
applicable MAM-basics development checkout, commit the change, integrate and push `main`, then
deploy from the primary MAM-basics clone:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config
```

The deployment fetches `origin`, validates all canonical sources, and installs only from the
fresh `refs/remotes/origin/main` tree. Its `--check` mode is read-only.

Shared skills are canonical under `dot-claude/skills/` and declared for Codex in
`dot-claude/shared-skills.txt`. Codex-only skills are canonical under `dot-Codex/skills/`.
`~/.agents/skills/` is only a live destination. Change canonical skills, commit and integrate
them, then use the same complete deployment. `dot-Codex/README.md` and
`dot-claude/README.md` define the full mapping.

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
- In a primary checkout, commit directly to `main` and push `main` normally. Do not create a
  feature branch merely because work has begun.
- A secondary worktree uses its existing local branch. If a new Codex-managed worktree is
  detached, follow `codex-worktree-tasks` for exact checkout verification and the
  `codex-worktree-<worktree-id>` branch name. Commit there without pushing the worktree branch.
- Integrate a worktree branch immediately before the task is archived, or earlier only when Ben
  asks or a concrete dependency requires it. Load `codex-worktree-tasks` and follow the
  repository's integration check. The primary clone receives only a verified fast-forward, then
  `main` is pushed.
- Ask before rewriting history or discarding work: force-push, amend, rebase, hard reset, branch
  deletion, stash drop, or equivalent operations.
- Do not add sleeps, timers, or custom deployment debouncing for Ben's Pages repositories.
  Their workflows already use a concurrency group that cancels an obsolete run.

A readiness question carries permission to do one or two small, obviously correct finishing
steps, such as filling a simple plan gap, updating a stale copy, or committing finished work. A
choice requiring judgment remains Ben's decision.

## Verification cadence for multi-session work

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
- Load `codex-worktree-tasks` for ordinary Codex-managed worktree setup, task creation, handoff,
  recovery, or archival.
- Load `worktree-forest` for a pinned multi-repository worktree forest. Do not apply that skill
  to an ordinary single-repository worktree.
- Load `prune-Codex-state` only when Ben asks to review Codex memory or plan files. The skill
  requires explicit confirmation before deleting anything.
- Load `verse-links` whenever Ben asks for links for a verse or atom; the skill runs the
  repository generator rather than constructing URLs by hand.

## Shell, scripts, and file operations

Prefer available built-in read, write, edit, search, and file-listing tools over equivalent shell
work. Use exact-string editing for a known replacement and a real Python script for algorithmic
work. Do not use `sed` or `awk`.

Never put a substantial script in `python -c`, `node -e`, a here-document, a PowerShell
here-string, or a pipeline into an inline interpreter. Put it in a uniquely named UTF-8 file in a
gitignored scratch directory and run the file. The same rule applies to multiline commit
messages and GitHub bodies: write a uniquely named file and pass `git commit -F` or
`--body-file`. One plain, self-contained command is fine; assembled shell pipelines and shell
control flow are not. Prefer `git -C <path>` to changing directories as part of a compound
command.

A throwaway scratch script has one requirement: it does its requested job and no more. It may
ignore source-style preferences, but it still uses explicit UTF-8 handling when non-ASCII text
flows.

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

Write a plan for a fresh session with no access to the surrounding conversation:

- use absolute repository paths and name the checkout where each command runs;
- name the skills and instruction files to load before editing;
- attribute and date decisions instead of using “this session” or “as discussed”;
- attach a re-measurement command and baseline commits to figures that must remain current;
- say which outputs are expected not to change and treat an unexpected diff as a finding;
- cite a searchable anchor as well as any line number;
- state preconditions, verification commands, and commit and integration discipline.

A figure answering a passing question may remain a dated measurement with no maintained
reproduction path if the plan says that explicitly.

A finished dated review, remediation plan, completed plan, or execution record is a receipt.
Correct it in `<stem>-update.md`, then `<stem>-update-2.md`; name the passage being corrected by
its words rather than by a drifting line number. Keep present-state documents, instructions,
README files, comments, and docstrings true in place.

In MAM-basics and MAM-private, an unprefixed `doc/review-findings-<date>.md` belongs to the
single-agent Claude review series and the Claude half of blind Design B. A Codex Design B review
uses `doc/codex-review-findings-<date>.md`. A standard sequential alternating round instead uses
`doc/dual-agent-review-<date>-turn-<NN>-<claude|codex>.md`; Agent 1 owns odd turns, Agent 2 owns
even turns, and either Claude or Codex may be Agent 1. The private series stays in MAM-private.

## Format changed Python with Black

Run Black at its defaults on every Python file changed before committing. Format only the files
changed; a repository-wide reformat is a separate commit. In a worktree, use the primary clone's
interpreter by absolute path as `codex-worktree-tasks` specifies. Never prefix Black or a tracked
script with `PYTHONUTF8=1`.

A missing `.venv` means the clone is not hydrated; create the environment or stop. Do not fall
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

## Delegate bounded work when it helps

Root agents and sub-agents are explicitly authorized to spawn further sub-agents in every
session, without asking Ben first, when bounded, independently checkable work can run in
parallel, a fresh sequential pass can improve quality, or delegation can keep noisy investigation
out of the root agent's context. Sub-agents may work in parallel or hand a later step to another
sub-agent. Tell Ben when delegation starts and what each sub-agent owns. Do not delegate merely to
satisfy a quota; keep tightly coupled work local when coordination would cost more than it saves.

The root agent remains the orchestrator. The root agent defines scope, collects and reconciles
sub-agent results, verifies material claims before adopting them, owns integration, and owns the
final answer. In a shared checkout, only one agent writes, stages or commits at a time. Delegate
read-only investigation freely; if concurrent agents must write, give the agents separate verified
worktrees. A sub-agent never stages or commits another agent's unfinished files.

## Prose names its subject

- Name both sides instead of writing “one … the other,” “former,” “latter,” or an unclear
  pronoun. Repetition is cheaper than making the reader reconstruct the referent.
- Give one thing one name. Do not rotate synonyms or coin a coy label. If a short name is useful,
  define it once and use only that name.
- If a heading announces a count, use a numbered list. A heading names the section's subject
  directly; avoid headings such as “One more thing” or “Worth flagging.”

These rules apply to pages, docstrings, comments, commit messages, issues, plans, and chat.

## Unicode in source and at runtime

Never write an orphan combining mark as a raw code literal. Use a named escape such as
`"\N{HEBREW POINT METEG}"`; in languages without named escapes, use a numeric escape and an
adjacent Unicode-name comment. This restriction does not apply to a mark anchored on a base
character or to genuine text data.

Ben's repositories use NFC for Latin letters with diacritics. Write precomposed ḥ (U+1E25), not
`h` plus COMBINING DOT BELOW. In `#` comments about Hebrew sounds, use ASCII `x` or `X` rather
than either Unicode form.

A Windows Python entry point that may emit non-ASCII reconfigures stdout and stderr to UTF-8 at
the start of `main()`. Prefer writing substantial or non-ASCII output to a file opened with
`encoding="utf-8"`. `PYTHONUTF8=1` is permitted only as a scratch-script workaround, never for
tracked code.

## Hebrew accentuation prose uses the skill

The `hebrew-prose` skill is the canonical source for atom versus chanted word, the one-scale
maqaf rule, paseq versus legarmeh, silluq versus meteg, prose and poetic verses, strand names,
corpus choice, sources, rendered prose, and verification. Load it before writing, editing, or
reviewing any such prose instead of reconstructing those rules from memory.

## Show local artifacts with file links

For a generated local page, image, or other artifact, give Ben a Markdown link whose target is an
absolute `file:///` URL with forward slashes. Do not launch a browser, open another tab, start a
development server, or create a launch configuration unless Ben asks. Verify the file's content
by reading it before claiming the artifact worked.

Use an in-app browser only when the task genuinely needs live DOM, console, network, or script
introspection. If a regenerated file must be viewed there, use a fresh filename and a fresh tab;
an existing tab can retain stale content.
