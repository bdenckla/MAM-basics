# Checkout kinds and portable knowledge: feedback and plan

State: live. Planning only: no phase has started, seven decisions are open, and nothing here
executes until Ben explicitly says so.

Written 2026-09-28 by Claude Opus 5.5 in a Plan Mode session started in
`C:/Users/BenDe/GitRepos/MAM-basics` at `a367f962`. File and line citations refer to that commit.
The same day, Ben asked to "save this plan to a file in the "doc" folder", and the session copied
its plan file here. Ben's instructions, verbatim:

1. "managing worktrees is proving taxing. I would like to revive my old idea of multiple full
   clones, e.g. GitRepos2 and GitRepos3, which are non-task specific and I just manage as a kind of
   "working set" for whatever tasks I choose. please give feedback on this"
2. "(to be clear, GitRepos2 and 3 would not be clones, they'd be "forests of clones")"
3. His reply to the first draft of this plan:
   > I guess I'd like to have my cake and eat it too, i.e. be allowed to use long-lived, non-project
   > specific, non-primary forests (GitRepos2, GitRepos3), as well as: 1. short-lived worktrees
   > 2. long-lived worktrees 3. cloud sessions (shallow clones of MAM-basics meant to "survive"
   > without siblings, e.g. we have already added some the skipping, automatically, of some mega
   > steps and some tests that use MAM-private) 4. Another machine's GitRepos (neither GitRepo
   > forest is "globally primary", i.e. they are peers, i.e. there is only a per-machine notion of a
   > "primary GitRepo") also, regarding memories, these always seem like a liability for cloud
   > sessions and also for switching machines (I already have two "GitRepos", one on my desktop and
   > one on my laptop) in other words I sort of want to move away from using memories for anything
   > non-machine-specific, which is most things. I was never comfortable with the per-repo notion
   > of memories anyway
4. His replies to the second draft:
   - On environments: "Why wouldn't each clone, whether in GitRepos, GitRepos2, or 3, have its own
     virtual environment?"
   - On memory: "Even that seems a little weird; it seems that should be at least at user level, and
     in a multi-user machine, at machine level (though I have no multi-user machines, I am the only
     user and I do not have multiple user accounts)"
   - On untracked inputs: "But it is fine to just say that no task that needs .novc or similar (I
     assume that's what you mean by "untracked inputs") is appropriate for "portability" out of its
     forest, e.g. forest-spanning work"
   - On the three resulting changes: "add those changes"

**Ben's decisions of 2026-09-28, applied in this revision:**
1. Every full clone has its own Python environments.
2. Memory is kept at user level, not per repository or per machine.
3. A task that needs untracked inputs stays in the checkout that holds them.

Everything else here is Claude's analysis and proposal. **State: planning only.** Nothing here
executes until Ben explicitly says so. Approving this plan in Plan Mode does not count as that
instruction.

**Terms (Decision 1 settles them).**
- A **forest** is a directory holding one full, independent clone of every repository in
  `all-repos.code-workspace` (MAM-basics, MAM-private, phonetic-hbo, hbofonts). Each clone has its
  canonical name.
- Each machine's **primary forest** is `$HOME/GitRepos`, the forest a machine's setup creates
  first. That is its only special role. Any **secondary forests** are `$HOME/GitRepos<N>`, N ≥ 2.
- **User-level memory** is Claude auto memory kept once per user account on each machine, rather
  than once per repository. It holds only facts that are true of that account on that machine.
- The tracked **user-wide instructions**, `dot-Codex/user-wide-AGENTS.md`, are also user level.
  Unlike user-level memory, they travel to every machine and to cloud sessions.

## Context

Worktrees are taxing to manage. Ben wants long-lived secondary forests in addition to four other
kinds of checkout, not in place of them:
- short-lived worktrees;
- long-lived worktrees;
- cloud sessions;
- the other machine's GitRepos.

No checkout is globally primary.

Separately, per-repository Claude memories fail in cloud sessions and when Ben changes machines.

The intended outcome has four parts:
1. All five kinds of checkout are first-class.
2. `origin` is the only state they share.
3. Every full clone is self-contained, down to its Python environments.
4. Everything a session needs to know travels in tracked text, except facts about Ben's account on
   one machine.

## Feedback

**Verdict: both directions are sound, and the code is already mostly there.** Resolution of sibling
repositories, cloud skips, user-configuration deployment and environment setup all work
per checkout today. Two things still don't:
- The instruction and policy text assumes one global primary clone.
- The memory is tied to one repository on one machine.

### Why the code already supports every checkout kind

1. **Siblings resolve beside each checkout's home clone.** `repos_root()` in
   `py/mb_cmn/paths.py` returns the parent of the clone a checkout was made from; for an ordinary
   clone, that is the clone itself. So a worktree made from `GitRepos2/MAM-basics` finds
   `GitRepos2/MAM-private`.
2. **Cloud skips depend on the environment, not on a missing sibling.**
   `graphviz_pin.in_cloud_session()` (`py/mb_cmn/graphviz_pin.py`) reads only
   `CLAUDE_CODE_REMOTE`. `main_0_mega.py` records the steps it skips in `_CLOUD_SKIPPED_STEPS` and
   reports such a run as "CLOUD-COMPLETE". `test_final_stress_vs_phonetic_mam.py` and
   `test_redirect_manifest.py` use the same test. So a forest missing MAM-private still fails
   loudly, as the rule that a code path "reads MAM-private every time it runs, or never" requires.
3. **Deployment works from any full clone on any machine.** `_primary_clone`
   (`py/repo_util/user_config_sync.py:134`) accepts any full clone named MAM-basics, and the
   deployment uses only a freshly fetched `origin/main`. The two machines are therefore peers.
4. **Each full clone can hydrate its own environments.** The code runs `sys.executable` with
   `cwd=_REPO` (for example in `py/main_repo_maintenance.py`), so nothing reaches into another
   clone's environment. `misc/requirements-venv-setup-windows.ps1` builds `.venv` from whatever
   repository root it runs in.
5. **Branches on `origin` already coordinate the reviews.** Today's `a367f962` says "the local
   branch name and checkout path are not shared state".
6. **Forests are small now.** The roster has 4 folders. It had 18 when Codex steered the idea
   toward worktree forests on 2026-09-01. On 2026-09-02 Ben wrote "nothing beats a single worktree";
   see line 360 of `git show 2a051ba5^:doc/PLAN-evacuate-public-repos-programme.md`.

### Why per-repository memory is the thing to leave

These counts were taken on 2026-09-28 and have no maintained reproduction path.

1. This machine holds 147 memory files in 8 directories, keyed by repository path: 92 for
   MAM-basics, 33 for MAM-private and 22 elsewhere.
2. The evacuations have already stranded 21 of them. They sit in 5 directories keyed to
   repositories no longer on this machine: mgketer 10, codex-index-aleppo 4, yeivin-itm 4,
   codex-index-cam1753 2 and wlc-utils 1.
3. None of these memories reach cloud sessions, the laptop, or secondary forests. The
   documentation says the directory "is derived from the git repository", and "Files are not shared
   across machines or cloud environments."
4. Judging by MAM-basics' index lines, only about six of its 92 entries are true only of Ben's
   account on this machine:
   - the OneDrive "no wild find" note;
   - the desktop window stuck on top;
   - the untracked Koren lookup generators;
   - the noise in mega timings;
   - stale CRLF clones;
   - where the Wikisource bot's credentials live.

   The rest are portable preferences or repository facts. Some are already duplicated in tracked
   text; for example, `AGENTS.md` covers the HBCE Psalms entry.
5. Codex's memories in `~/.codex/memories/` are already user level. But `config.toml` sets
   `generate_memories = true` and `use_memories = true`, so they fill up with portable content too.

### Checkout kinds

| Kind | Where | Siblings | Python environment | Integrates through | Ends |
|---|---|---|---|---|---|
| Primary forest | `$HOME/GitRepos` | same forest | its own, one per tracked `requirements.txt` | `main`, pushed to `origin` | never |
| Secondary forest | `$HOME/GitRepos<N>` | same forest | its own | `main` (or a long-lived branch), pushed to `origin` | if Ben drops it |
| Short-lived worktree | `<home clone>/.claude/worktrees/` or `~/.codex/worktrees/` | home clone's forest | its home clone's | fast-forward of its home clone, then push | retirement procedure |
| Long-lived worktree | same as short-lived | same | its home clone's, or its own when the task needs different dependencies | branch pushed after every commit; integrated on Ben's word | retirement procedure |
| Cloud session | container with a shallow MAM-basics clone | none; skips under `CLAUDE_CODE_REMOTE=true` | the container's | branch pushed to `origin` | with its container |

Three rules apply to every kind:

1. **One writer.** Only one session writes to a given checkout at a time.
2. **A task moves only through `origin` (Ben, 2026-09-28).** A task moves between checkouts only
   through what it has pushed. A task stays in its checkout if either of these is true:
   - it needs untracked files inside that checkout, such as `.novc/` or anything else gitignored;
   - it holds unpushed commits.

   Such a task never spans forests.
3. **Inputs outside every repository are user level.** Every forest on the machine can reach them.
   Examples are the scan archive, found through `BOOK_SCANS_ROOT` (`WLC_SCANS_DIR` until
   2026-09-28), and pywikibot's configuration in `$env:USERPROFILE/.pywikibot`.

### What secondary forests cost

1. **Three silent failures to fix before first use (Workstream A):**
   - **Stale forests.** Nothing clones or refreshes the roster. `_how_to_obtain`
     (`py/repo_util/repo_selection.py:49`) only builds text for an error message.
   - **Instructions that send sessions back into GitRepos.** The worst case is lines 54–62 of
     `dot-claude/skills/hebrew-prose/references/verifying.md`, which set
     `$env:REPOS_ROOT = "C:/Users/BenDe/GitRepos"`.
   - **Policy that calls a forest residue.** Three passages do this:
     - `evacuated-repositories.md` says "A clone's presence is residue";
     - clause 5 of `gitrepos_setup_rule`;
     - the "Completed Codex task folders" screening in `repository-maintenance.md`.
2. **A memory fork.** Until Workstream B moves MAM-basics' and MAM-private's portable memories
   into tracked text, a session in a secondary forest lacks them. After that, nothing is left to
   fork.
3. **Accepted costs:**
   - **Only `origin` is shared.** When two forests push `main`, the second must merge and push
     again. If either side reaches a mega generator, the mega is rerun on the merged state.
   - **Per-path settings, once for each new clone, which Ben makes:**
     - Claude and Codex trust;
     - the desktop permission mode;
     - Codex's Local mode;
     - a `Read` rule in `~/.claude/settings.json`.
   - **Tasks that need untracked inputs stay where those inputs are.** Today most of them are in
     the primary forest: `.novc` holds about 1.3 GiB in MAM-basics and about 490 MiB in MAM-private.
   - **Disk.** A secondary forest takes about 3.1 GiB:
     - about 2.5 GiB of clones;
     - about 0.6 GiB for its six Python environments, which also need a one-time install.

## Workstream A: make every checkout kind first-class

**Where it runs.** Any checkout may be used for development. The deployment steps must run from a
full clone, because `--sync-user-config` refuses to run in a linked worktree. The recommended
checkout is `C:/Users/BenDe/GitRepos/MAM-basics` on `main`. Every full clone runs its own
`.venv/Scripts/python.exe` from its repository root. Below, `<py>` means that interpreter, run
from `C:/Users/BenDe/GitRepos/MAM-basics`. This machine's `$HOME` is `C:/Users/BenDe`.

**Load first:**
- `mam-repository-topology`, with its two references;
- `iterative-document-editing`;
- `hebrew-prose`, before editing its `verifying.md`.

Also read `AGENTS.md` and both `dot-*/README.md` files. Read a repository's `AGENTS.md` before
writing in that repository.

**Preconditions:**
- Ben has answered Decisions 1–3.
- `HEAD` is `a367f962` or a descendant of it.
- Status holds only paths this task owns. Another session committed here today, so check `HEAD`
  again before each commit.

1. **Policy.** Record the per-machine layout in `in/repo_maintenance_policy.json` as a rule, not a
   list:
   - `$HOME/GitRepos` is the primary forest, distinguished only by being created first.
   - Secondary forests are optional, at `$HOME/GitRepos<N>`.
   - Every forest holds the full roster under its canonical names, with the same origins.
   - Neither machine's primary forest is globally primary.

   Then:
   - Point clauses 5 and 6 of `gitrepos_setup_rule` at the new rule.
   - Revise these sections so that no forest clone is screened as residue:
     - "Current operating rules" in `mam-repository-topology/SKILL.md`;
     - "Repo locations are decisions" in `evacuated-repositories.md`;
     - "Completed Codex task folders" in `repository-maintenance.md`.
2. **Terminology and rules.** Today "the primary clone" means both a worktree's home clone and a
   single global canonical clone. The second meaning goes away.
   - Where the text means the clone a worktree was made from, write "the worktree's home clone".
     That clone is the worktree's integration target, owns the shared `.git`, and supplies the
     worktree's interpreter.
   - Where the text assumes a single global clone, write "any full clone". Deployment and
     maintenance sweeps run from any full clone, and a sweep covers that clone's forest.

   Rewrite each use in:
   - `dot-Codex/user-wide-AGENTS.md`: "Canonical user configuration", "Git and commits",
     "Linked-worktree safeguards…", "Plans and finished dated records" and "Format changed Python
     with Black";
   - `AGENTS.md`: "Integrating a worktree branch here" and "Running tests";
   - `codex-worktree-tasks` and its two references;
   - `worktree-forest`, unless Decision 1 retires it;
   - "the designated primary clone" in `doc/dual-agent-review.md`;
   - `MAM-private/AGENTS.md`, section "Working directories, virtual environments, and entry
     points";
   - `hbofonts/AGENTS.md`.

   Add to the user-wide body:
   - **The integration loop for secondary forests:** fetch; merge `origin/main` if it moved; run
     the mega when owed; push; if the push is refused, repeat.
   - **The portability rule and the user-level-input rule,** both from "Checkout kinds" above.
   - **The Black section:** "A missing `.venv` means the clone is not hydrated" keeps its wording
     and applies to every full clone. A linked worktree has no `.venv` and uses its home clone's.
3. **Paths.**
   - Delete the `REPOS_ROOT` paragraph at `verifying.md` lines 54–62.
   - Rewrite the sibling-paths bullet at `verifying.md` line 241. Its heading, "Sibling paths break
     in agent worktrees, and `REPOS_ROOT` is the fix", and its last fallback, `repo_root().parent`,
     have been wrong since `516a4a1a` (2026-09-10), when `mb_cmn/paths.py` began finding siblings
     beside a worktree's home clone with no variable. Ben agreed on 2026-09-28 that this rewrite
     waits for this step.
   - Make the script paths checkout-relative in:
     - `verse-links/SKILL.md`;
     - `github-issues/references/reading-and-writing.md` (line 110);
     - `mam-wikisource-refresh/references/dependent-refresh.md`, which should then say "the same
       forest's checkouts";
     - `repository-maintenance.md`.
   - Commands run `.venv/Scripts/python.exe` from the repository root of a full clone. This covers
     the commands in `AGENTS.md` and the interpreter table in `MAM-private/AGENTS.md`, where each
     tree uses its own `.venv`.
   - A worktree names its home clone's interpreter by absolute path.
   - Commands written for Ben use `$HOME/...`.
4. **Refresh command** in `py/main_repo_util.py`.
   - **`--sync-forest ROOT`** does three things:
     - **Clones** missing roster repositories. It takes each URL from the origin of this
       checkout's sibling of the same name. It runs non-interactively, so a credential problem
       fails loudly instead of opening a dialog.
     - **Fast-forwards** each clone that meets all of these conditions:
       - it is a full clone with a matching origin;
       - it is clean;
       - it has no Git operation in progress;
       - it is on `main`.

       For each such clone it fetches and runs `git merge --ff-only origin/main`.
     - **Hydrates** environments. For each tracked `requirements.txt`, it creates a missing
       `.venv` beside it and installs against that environment's constraints (step 5). Today there
       are six:
       - MAM-basics;
       - MAM-private's root, `mgketer/`, `al-hatorah/` and `masorah-books/`;
       - hbofonts.

     It reports every other state and leaves it untouched.
   - **`--check`** fetches and reports only, including missing environments and any installed
     version that differs from the constraints.
   - **`--forest-status`** finds `$HOME/GitRepos` and every `$HOME/GitRepos<N>` by the naming rule
     and runs the check on each. It also says whether a Claude or Codex session occupies each
     forest.
   - **Limits.** The command never resets, stashes, switches branches, forces or deletes. It
     reports a failing repository and continues with the rest.
   - **Setup.** `--sync-forest $HOME/GitRepos` is also the "sync GitRepos" operation that
     `gitrepos_setup_rule` describes but no code performs today.
   - **Reuse:**
     - `load_workspace_repo_dirs` (`repo_selection.py:110`);
     - `_run_git` and `_fetch_origin` (`user_config_sync.py:206` and `:148`);
     - `_status_entries` and `_operation_markers` (`worktree_retirement_inspection.py:48` and
       `:408`);
     - `_is_ancestor` (`worktree_retirement_git.py:106`);
     - `runtime_facts` (`worktree_owners.py:68`).
   - **Tests.** Add no new test, per Ben's test-shape rule. The step 8 runs are the verification.
5. **Pinning (form per Decision 3).** Beside each of the six `requirements.txt` files, add a
   tracked `constraints.txt`, generated with `pip freeze` from the desktop's current environment.
   - Setup installs with `pip install -r requirements.txt -c constraints.txt`. That covers
     `misc/requirements-venv-setup-windows.ps1`, `misc/requirements-venv-setup-linux.txt` and
     whatever setup MAM-private and hbofonts document.
   - A constraints file changes only through a deliberate, committed regeneration.
   - On the laptop, Ben reinstalls each environment against the constraints once. This fixes the
     drift between the two machines as well as between forests.
6. **`.gitignore`.** Add `.claude/worktrees/` to the tracked `.gitignore` in MAM-basics and in
   MAM-private. Today the entry lives only in `.git/info/exclude`.
7. **Integrate and deploy.**
   1. Push.
   2. From `C:/Users/BenDe/GitRepos/MAM-basics`, run `<py> py/main_repo_util.py --sync-user-config`.
   3. Confirm that `--check` then reports clean.
   4. Ben runs the same deployment on the laptop, from any full clone there.
8. **Build the forests.** This writes outside every repository, so Ben approves it first.
   - Run `<py> py/main_repo_util.py --sync-forest $HOME/GitRepos2`, then the same command for
     `GitRepos3`. Each forest downloads about 0.9 GiB of Git data plus its packages.
   - Ben then makes the per-path settings. While doing so, he can prune the eight GitRepos entries
     at lines 60–66 and 68 of `additionalDirectories` in `~/.claude/settings.json`. Most of those
     entries name repositories that are gone.
9. **Verify each secondary forest.**
   - `--forest-status` reports every repository clean, on `main` and 0/0 with `origin`, and all
     six environments present and matching their constraints.
   - From `$HOME/GitRepos2/MAM-basics`, `.venv/Scripts/python.exe py/main_test.py` passes. The
     run includes `test_final_stress_vs_phonetic_mam.py`, which proves the forest's own MAM-private
     is the one being read.
   - After `.venv/Scripts/python.exe py/main_0_mega.py`, `git diff --stat` shows no tracked
     content change. A line-ending warning or a content change is a finding to explain.
   - `--sync-user-config --check` reports clean.

## Workstream B: portable knowledge in tracked text; user-level memory only for account facts

**Where it runs.** The tracked edits run as in Workstream A. This machine's triage runs here. The
laptop's memory directories get the same triage in a session on the laptop.

**Load first:**
- `iterative-document-editing`;
- the skill that owns each destination;
- `MAM-private/doc/near-aleppo-privacy.md`, before touching any MAM-private memory.

1. **The rule.** Replace the memory guidance in `dot-Codex/user-wide-AGENTS.md` with the following.
   - Claude auto memory and Codex memories are user level: one store per user account on each
     machine.
   - They hold only facts that are true of that account on that machine:
     - software installed or configured for the account;
     - untracked files and directories under its home directory;
     - app or operating-system behavior observed only there.
   - User-level memory never holds repository content.
   - Every other lesson becomes a tracked edit, as Decision 6 settles. The user-wide instructions
     are the user-level home for portable rules.
   - On a multi-user machine, facts about the machine itself would belong at machine level. Claude
     Code's policy settings, which can also set `autoMemoryDirectory`, could provide that level.
     Ben's machines each have a single user, so nothing here does it.
   - The rule overrides the harness's default memory guidance.
2. **Destinations and budget.**
   - Always-loaded bodies (the user-wide body, a repository's `AGENTS.md`) receive only rules that
     most tasks need, each in a sentence or two. Codex's `check_project_doc_budget.py` warns above
     32 KiB of project instructions. As of 2026-09-28, MAM-basics' `AGENTS.md` is 15,879 bytes,
     MAM-private's is 15,618 and the user-wide body is 24,774.
   - Everything else goes to the skill or document the relevant task already loads:
     - the `hebrew-prose` references;
     - `github-issues`;
     - the `mam-repository-topology` references;
     - `doc/periodic-review.md` and `doc/dual-agent-review.md`;
     - a `doc/` file routed from `AGENTS.md`.
   - Prefer an existing destination. Propose any new skill to Ben for approval.
3. **Triage MAM-basics' 92 memories.**
   - Read each file itself, not only its index line.
   - Classify each memory as one of:
     - **user-level:** move it to user-level memory;
     - **covered:** quote the tracked passage that already covers it, then delete the memory;
     - **portable:** name its tracked destination and section, then delete the memory;
     - **stale:** delete it.
   - Present the table to Ben and apply only what he approves.
   - Copy every memory directory to a dated backup under `$HOME` before any deletion.
4. **Triage MAM-private's 33 the same way.**
   - Portable private content goes only into MAM-private's tracked documents.
   - A private finding never goes into user-level memory, into MAM-basics, or into the user-wide
     body.
5. **Triage the 22 in other directories:** the 21 stranded ones and the one under
   `C--Users-BenDe-GitRepos`. Most are probably stale.
6. **User-level memory.**
   - Ben sets `"autoMemoryDirectory": "~/.claude/user-level-memory"` in his untracked
     `~/.claude/settings.json`. Every repository, forest and worktree his account opens on this
     machine then shares that one directory.
   - Move in only the memories classified user-level.
   - Re-point `_find_memory_dir` (`py/repo_util/check_memory_health.py:208`) at that directory.
7. **Cloud.** Once Workstream A step 3 has removed the Windows paths, extend
   `.claude/hooks/install-user-config.sh` to install every skill in `dot-claude/shared-skills.txt`,
   not just `hebrew-prose`, so that content moved into skills reaches cloud sessions (Decision 7).
8. **Codex memories** follow Decision 5.
9. **Deploy** with `--sync-user-config`, on this machine and on the laptop.

## Order

1. Workstream B step 1, the rule, so that no new portable memories accumulate.
2. Workstream A steps 1–7.
3. Workstream B steps 2–4.
4. Workstream A steps 8–9. After these, the secondary forests are ready for tasks.
5. The rest of Workstream B.

If Ben wants the forests sooner, a temporary bridge is available. An untracked
`.claude/settings.local.json` in each secondary forest's MAM-basics and MAM-private can point
`autoMemoryDirectory` at GitRepos' directory for that repository until the triage is done.

## Checks, unchanged outputs, risk

**Checks:**
- Every commit: `git diff --check`, and Black on each changed `.py` file.
- The full suite, after:
  - the code changes (A4 and B6);
  - the setup and constraints changes (A5);
  - the hook change (B7).

  According to `py/product_scopes.py`, `py/repo_util` is not a mega generator.
- Commits that only change instructions owe neither the suite nor the mega.

**Unchanged outputs:** every product under `gh-pages/`, `MAM-parsed/`, `MAM-simple/`,
`MAM-for-Sefaria/`, `MAM-with-doc/`, `MAM-OSIS/` and `out/`. Any diff there is a finding.

**Risk.** Nothing reaches a product. These acts are hard to undo or reach outside:
- pushing `main`, which Pages deploys at 4:17 AM, New York time;
- about 6 GiB of forests and environments written outside every repository;
- deploying to `~/.claude`, `~/.codex` and `~/.agents`;
- deleting memory files outside Git, which is why a backup and Ben's approval come first;
- Ben's own edits to `~/.claude/settings.json` and `~/.codex/config.toml`.

## Decisions for Ben

1. **Names:** should the terms be "forest", "primary forest" and "secondary forest", with the
   `worktree-forest` skill retired so that "forest" means one thing? Recommended: yes.
2. **How secondary forests integrate:** should they commit on `main` and push after a fetch, a
   merge, and the mega when owed? Recommended, because this is today's rule for a primary checkout.
   The alternative is a named branch on `origin` for each task.
3. **Pinning form:** should each `requirements.txt` get a tracked `constraints.txt` generated by
   `pip freeze` and applied with `-c`? Recommended, because `requirements.txt` stays the list of
   direct dependencies. The alternative is pinning versions in `requirements.txt` itself.
4. **Claude's user-level memory:** should there be one directory per user account on each machine,
   set by `autoMemoryDirectory` in `~/.claude/settings.json`? Recommended. The alternative is to
   turn auto memory off.
5. **Codex memories:** should their portable content in `~/.codex/memories/MEMORY.md` move into
   tracked text, with generation and use then turned off? Recommended. The alternative is to keep
   them.
6. **New lessons:** should a session propose the tracked edit in its final message and commit only
   when Ben says yes? Recommended. The alternative is to commit without asking.
7. **Cloud skills:** should the cloud hook install every shared skill once none contains Windows
   paths? Recommended. This revisits Ben's decision of 2026-09-14 not to install `github-issues` in
   the cloud.
