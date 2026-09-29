# Checkout kinds and portable knowledge: feedback and plan

State: live. Workstream B's focused memory retirement and instruction consolidation is complete
through the exact deletion-approval boundary on 2026-09-28. Memory deletion remains unapproved.
Workstream A and Decisions 1–3, 6 and 7 remain planning only.

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

The three decisions above preserve Claude's earlier revision. Ben's later instruction of
2026-09-28 supersedes the user-level memory exception with complete memory retirement:
“Execute the approved proposal” and its private appendix, followed by “Do not delete memories
yet.” The approved proposal is
`C:/Users/BenDe/GitRepos/MAM-basics/.novc/PROPOSAL-memory-retirement-and-instruction-consolidation-2026-09-28.md`;
its private appendix is
`C:/Users/BenDe/GitRepos/MAM-private/.novc/PROPOSAL-memory-retirement-private-2026-09-28.md`.
Codex's revision below executes that focused scope. Every unrelated proposal remains planning
only; a Plan Mode transition grants no implementation authority.

**Terms (Decision 1 settles them).**
- A **forest** is a directory holding one full, independent clone of every repository in
  `all-repos.code-workspace` (MAM-basics, MAM-private, phonetic-hbo, hbofonts). Each clone has its
  canonical name.
- Each machine's **primary forest** is `$HOME/GitRepos`, the forest a machine's setup creates
  first. That is its only special role. Any **secondary forests** are `$HOME/GitRepos<N>`, N ≥ 2.
- **User-level memory** names the superseded earlier proposal. The approved Workstream B retains
  no account-local memory exception and creates no replacement memory directory.
- The tracked **user-wide instructions**, `dot-Codex/user-wide-AGENTS.md`, travel to every machine
  and to cloud sessions. Account-specific values belong in explicit account configuration.

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
4. Maintained repository knowledge travels in tracked text. Account-specific values use explicit
   account configuration and discovery through the owning setup documentation.

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

The following figures are Claude's earlier 2026-09-28 observations, with no maintained
reproduction path. They are preserved as dated evidence, not the execution inventory. The later
approved census contains 247 files in eight exact stores; the private inventory and refreshed
verified backups govern this retirement. The earlier counts and Codex-state assertion below
must not be used to select files or infer current memory contents.

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
2. **Memory retirement is independent.** Workstream B migrates approved content and disables
   memory use. Secondary-forest setup is not a prerequisite for that work.
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
   - Recheck `verifying.md`, “Commands”, rather than applying the old line-number deletion.
     The approved memory consolidation already routes ordinary sibling discovery to MAM-basics'
     instructions and retains `REPOS_ROOT` only as an unusual-layout override. Workstream A's
     broader forest and path policy remains unresolved.
   - Rewrite the sibling-paths bullet at `verifying.md` line 241. Its heading, "Sibling paths break
     in agent worktrees, and `REPOS_ROOT` is the fix", and its last fallback, `repo_root().parent`,
     have been wrong since `516a4a1a` (2026-09-10), when `mb_cmn/paths.py` began finding siblings
     beside a worktree's home clone with no variable. Ben agreed on 2026-09-28 that this rewrite
     was then proposed for this step; the narrower stale sibling recipe was subsequently
     corrected under the approved Workstream B, without settling forest policy.
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

## Workstream B: approved memory retirement and instruction consolidation

Ben authorized execution on 2026-09-28, including both approved proposal files named above.
The root Codex executor owns both migrations and final integration, and is the sole writer.
Deletion requires Ben's later approval of the refreshed exact manifest. The full public triage
and private dispositions remain in their approved proposal files; private-derived material
stays in MAM-private.

**Verified checkouts and baselines, recorded before editing:**

| repository | source and primary integration checkout | managed development checkout | verified baseline and branch |
|---|---|---|---|
| Public | `C:/Users/BenDe/GitRepos/MAM-basics` | `C:/Users/BenDe/.Codex/worktrees/memory-retirement/MAM-basics` | `52f1f6bfce902b1493a6738979aac959841e8f0d`, `codex-worktree-memory-retirement` |
| Private | `C:/Users/BenDe/GitRepos/MAM-private` | `C:/Users/BenDe/.Codex/worktrees/3372/MAM-private` | `e781b1accbdf8fb5f94c3a8469b78fd26ab2e86f`, `codex-worktree-3372` |

Both origins were fetched before reading source. Public `origin/main` contains required
`f368a30598e7cb2a6377463d2616b71884a98dda`; private `origin/main` contains required
`e781b1accbdf8fb5f94c3a8469b78fd26ab2e86f`. A successor refreshes HEAD, branch, ancestry and
NUL-delimited status before editing or staging, and stops on unowned changes. Public commands
run from the public development root with
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`. Private instruction checks run
from the private development root; no private generator is invoked.

**Load before editing:** common instructions, each repository's AGENTS, both public configuration
READMEs, `iterative-document-editing`, `codex-worktree-tasks` and its runtime/lifecycle references,
`mam-repository-topology` and its maintenance reference, `hebrew-prose` with its MAM-basics and
destination references, `github-issues` with its destination references, both canonical pruning
skills, and `openai-docs` for account settings. Read private AGENTS and
`C:/Users/BenDe/GitRepos/MAM-private/doc/near-aleppo-privacy.md` before private evidence, then the
private appendix and its destination-specific skill. These routes add no issue-operation scope.

1. **Freeze and back up.** Preserve Ben's exact authorization and actual checkout verification.
   Refresh all eight exact stores, read changed/new files, and copy complete originals into the
   retained private archive under
   `C:/Users/BenDe/GitRepos/MAM-private/memory-retirement-backups/20260928-memory-retirement-a78e/`.
   Verify every size and SHA-256, preserve provenance and configuration originals, and use
   SQLite's consistent backup API for the evidence database. Never archive raw memories publicly.
2. **Migrate and consolidate.** Apply the approved public additions and private PR01–PR06 at
   their named homes. Route duplicate rules to the proposal's sole authorities, preserve
   repository exceptions and dated rationale, remove `--check-memory-health` and its module,
   and rewrite both existing pruning skills in place for plans only. Do not change the shared
   deployment implementation or executable hook behavior. Do not create a replacement memory
   store or choose Decision 6's general future-lessons policy.
3. **Check and commit in development.** Run `git diff --check` with the exact safe.directory.
   From the public development root, run these commands with the public interpreter named above:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black py/main_repo_util.py py/repo_util/check_repo_standards.py py/tests/test_mega_coverage.py
   ```

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m ruff check --no-cache py/main_repo_util.py py/tests/test_mega_coverage.py
   ```

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --help
   ```

   Check that the real entrypoint rejects the removed flag with an unrecognized-argument error
   before an action runs. Stage the authorized module deletion before the coverage lint, which
   reads Git's tracked-file index. Then run:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_mega_coverage.py
   ```

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
   ```

   Private PR06 additionally requires `git check-ignore -q -- memory-retirement-backups/verification-probe.txt`
   to return 0 and `git check-ignore -q -- AGENTS.md` to return 1, in the verified private checkout
   with its exact safe.directory. Recheck HEAD and owned status, stage exact paths and commit
   locally on each existing branch. Do not push ordinary worktree branches. A passing suite
   remains applicable after prose-only corrections; a new executable change or unresolved failure
   requires relevant checks again.
4. **Integrate and push.** Fetch and verify clean primary `main` in each repository. Merge current
   primary `main` into each development branch. The executable public branch owes this final gate,
   run from the public development root:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
   ```

   Only the planned authored `MAM-parsed/README.md` prose may change among products; all remaining
   generated/product content and every private output are expected unchanged. Treat an unexpected
   diff as a finding; explain and commit any required generated change before integration.
   Fast-forward each primary to its verified development branch and push `main` normally. A failed
   fast-forward or push sends the merge and checks back to development; no primary merge substitute,
   history rewrite or discarded work is authorized.
5. **Deploy from public primary.** Run from `C:/Users/BenDe/GitRepos/MAM-basics`:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config
   ```

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check
   ```

   Read the result and verify that both deployed pruning skills contain plan pruning only.
   Never hand-edit live instruction copies. The private skill remains canonical in MAM-private.
6. **Disable and verify account memory.** Back up configuration originals; preserve unrelated
   settings. Set Claude `autoMemoryEnabled=false`, Codex `features.memories=false`, and Codex
   `memories.generate_memories=false` / `memories.use_memories=false`. Check higher-precedence
   settings and launch overrides for those keys only. Verify fresh sessions; cached injected
   context is not erased. These account edits are separate from canonical deployment.
7. **Quiesce, refresh and request exact deletion approval.** Preserve task state before closing
   affected writers. Re-inventory all eight stores, read every changed/new file, verify a final
   consistent backup, and publish the exact private path/size/SHA-256 deletion manifest. It names
   candidate files and separately names only their now-empty memory directories. Databases,
   sidecars, session logs, credentials, configuration and backup archives are excluded.
   Return the manifest to Ben and stop before deletion. Changed files invalidate their approval
   entries. Deletion and backup disposal require separate explicit approval.

Record completed checks, deployed versions, configuration evidence and exact private backup
locations in the execution receipt; keep its public summary sanitized. Laptop retirement is an
independent later task after its own source and memory checks. This desktop execution neither
assumes nor changes laptop settings. Cloud skill installation remains Decision 7, rather than
an execution step of this approved scope.

## Order

Execute the approved Workstream B independently of Workstream A. Finish migration, consolidation,
checks, integration, deployment, account disablement and verified backup before asking for exact
deletion approval. Workstream A remains gated by Decisions 1–3; cloud expansion remains gated by
Decision 7. No temporary memory-directory bridge is part of the approved implementation.

## Checks, unchanged outputs, risk

Workstream B's exact gates and expected unchanged outputs are above. Workstream A keeps its own
prospective gates: relevant checks after executable/setup changes, its full suite, secondary-forest
mega and deployment checks once that work is authorized. Instruction-only revisions do not expire
a relevant full-suite result. The Workstream B utility removal has no mega-generator reach but
still owes the repository's final integration mega.

MAM-basics declares product reach in `py/product_scopes.py`; MAM-private declares no corresponding
product map or root test runner. The approved authored `MAM-parsed/README.md` change is explicit;
remaining products and generated outputs are expected unchanged. Outward or difficult-to-undo
acts are separate: normal public/private `main` pushes, account deployment, account-setting writes,
and later memory deletion. Deletion remains protected by the verified private archive and exact
approval. Public main retains its existing Pages schedule. Forest creation and environment
pinning remain outside this execution scope.


## Decisions for Ben

1. **Names:** should the terms be "forest", "primary forest" and "secondary forest", with the
   `worktree-forest` skill retired so that "forest" means one thing? Recommended: yes.
2. **How secondary forests integrate:** should they commit on `main` and push after a fetch, a
   merge, and the mega when owed? Recommended, because this is today's rule for a primary checkout.
   The alternative is a named branch on `origin` for each task.
3. **Pinning form:** should each `requirements.txt` get a tracked `constraints.txt` generated by
   `pip freeze` and applied with `-c`? Recommended, because `requirements.txt` stays the list of
   direct dependencies. The alternative is pinning versions in `requirements.txt` itself.
4. **Resolved — Claude memory:** Ben's approved focused proposal of 2026-09-28 retires all legacy
   stores and disables auto memory. No replacement `autoMemoryDirectory` is created. The exact
   deletion manifest still requires later approval.
5. **Resolved — Codex memories:** the same approval migrates useful content into tracked text and
   turns generation and use off. Its active metadata database is retained; the refreshed exact
   legacy-file manifest governs any later deletion.
6. **New lessons:** should a session propose the tracked edit in its final message and commit only
   when Ben says yes? Recommended. The alternative is to commit without asking.
7. **Cloud skills:** should the cloud hook install every shared skill once none contains Windows
   paths? Recommended. This revisits Ben's decision of 2026-09-14 not to install `github-issues` in
   the cloud.

## Revision ledger

Codex, 2026-09-28: replaced the superseded Workstream B account-local exception with Ben's
approved complete retirement and instruction consolidation. Recorded actual managed paths,
verified source baselines, sole-writer and integration ownership, exact gates, private archive
protection, fresh-session disablement and the later deletion-approval boundary. Decisions 4–5
are resolved; Decisions 1–3, 6 and 7 remain open. Workstream A, laptop execution and cloud-skill
expansion are not authorized by this revision.

Codex, 2026-09-28: Workstream B is implemented through the exact deletion-approval boundary.
Both migrations are on origin/main, canonical deployment checks clean, account memory is off,
fresh runtime settings are verified and the final eight-store backup matches every source hash.
No memory was deleted. [memory-retirement-and-instruction-consolidation-2026-09-28.md](memory-retirement-and-instruction-consolidation-2026-09-28.md), “Disablement, retained backup and approval boundary”,
records the sanitized evidence and private receipt route. Decisions 1–3, 6 and 7 remain open.
