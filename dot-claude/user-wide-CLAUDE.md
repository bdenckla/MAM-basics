# User-level instructions (Ben Denckla)

Personal, cross-project preferences — these apply in **every** repo. A project's own
`CLAUDE.md` or auto-memory may add repo-specific detail on top.

**Canonical location: my `MAM-basics` repo, at `dot-claude/user-wide-CLAUDE.md`** (cloned to
`~/GitRepos/MAM-basics`). The file you are reading, `~/.claude/CLAUDE.md`, is the live working
copy that Claude Code actually loads; nothing syncs the two automatically. **After editing this
file, copy it back to the repo and commit**, or the tracked copy silently goes stale:
```powershell
Copy-Item "$HOME/.claude/CLAUDE.md" "$HOME/GitRepos/MAM-basics/dot-claude/user-wide-CLAUDE.md" -Force
```
See `dot-claude/README.md` there for the drift check and for what is deliberately *not*
tracked (`settings*.json`, `projects/`).

**It lived in `github-misc` at `dot-claude/CLAUDE.md` until 2026-09-09**, beside the `dot-emacs`
and `dot-gitconfig` copies, and it moved for a reason worth stating rather than a tidying
impulse. A cloud session reaches only the repositories attached to it, and `github-misc` is not
one of them, so nothing tracked there could be fetched into a container — measured that day, a
clone of it from a MAM-basics cloud session returns `Invalid username or token`. Privacy was
never why `github-misc` held this file: the commit that put it there, `f1078d5` of 2026-07-25,
gives the reason as the `dot-emacs` / `dot-gitconfig` precedent and the fact that this was the
one authored config file under no version control at all. MAM-basics travels with the clone, so
storing it there is what makes a cloud session able to read it.

**The history stayed behind, so a `github-misc <sha>` citation below is right as written.** The
files were copied rather than filtered out with their commits, so every commit that touched this
file before 2026-09-09 is still a `github-misc` commit and is still cited as one — `1925699`,
`7780489`, `14a53df`, `56737b6`. Commits from 2026-09-09 onward are MAM-basics commits. Do not
"correct" an old citation to name MAM-basics: it would then resolve to nothing.

**The tracked name is `user-wide-CLAUDE.md`, not `CLAUDE.md`, and that is deliberate.** Claude
Code auto-loads a nested `CLAUDE.md` from a directory being worked in, so a second file of that
name inside MAM-basics would start loading itself beside the repo's own `CLAUDE.md` the moment
anyone edited a file beside it. The live copy keeps the name `~/.claude/CLAUDE.md`, which is
what the loader requires there; only the tracked copy is renamed.

**A shared SKILL has THREE homes, not two, and the third is the one that goes stale.**
`MAM-basics`'s `dot-claude/skills/<name>/` is canonical, `~/.claude/skills/<name>/` is what
Claude Code loads, and `~/.agents/skills/<name>/` is what Codex loads. The procedure, and the
two `git diff --no-index` comparisons that prove a change reached both live homes, are in
`dot-claude/README.md` §"Shared-skill deployment to Claude and Codex" — read them there rather
than here, and **run both comparisons whenever a shared skill changes.** Checking the canonical
copy against `~/.claude/` alone passes while Codex is reading something else.

**Why this needs saying in the file that loads every session:** the rule has been in
`dot-claude/README.md` all along and `~/.agents` fell behind anyway, because nothing loads that
README. `~/.agents/skills/hebrew-prose/references/sources-and-corpora.md` silently lacked
github-misc `1925699` of 2026-09-07 — finding 5.6 of
`MAM-basics/doc/review-findings-2026-09-08.md` — until `25a8955` put it back in step on
2026-09-09. It then fell behind again **that same day**, when `560239c` reached the canonical and
Claude homes and not the Codex one. Nothing warns, and the Codex home is tracked nowhere of its
own, so those two comparisons are the only detector there is.

## Git & commits — commit at will; integrate worktrees at archival
Rewritten 2026-09-07 from Ben's Codex instructions — `~/.codex/AGENTS.md`'s section of the same
name, github-misc commits `7780489` and `14a53df` of 2026-09-06 and `56737b6` of 2026-09-07 — so
that Claude and Codex run one worktree protocol. Until then this section was headed "commit and
push at will", told a worktree session to merge into `main` *during* the session, and called
unpushed work "anomalous — a symptom rather than a pending chore". Those three positions are
retired; the reasoning bullets that survive below are unchanged.
- **Commit finished work without asking.** A commit is an ordinary step of doing the work, not
  an outward-facing action needing its own yes. This reverses the old rule that left finished
  work uncommitted in a worktree while waiting for permission. Ben's reason, 2026-08-02, still
  stands: he no longer vetoes a change before it lands, and can read a diff after it lands and
  ask for a follow-on commit fixing whatever he does not like.
- **In a primary checkout, push `main` normally. In a secondary worktree, commit only to its
  local non-`main` branch.** Do not push that worktree branch merely as a backup: nobody needs
  to inspect it on the remote. Do not merge it into `main` merely because it has a commit.
- **Merge a worktree branch into `main` and push `main` just before the session is archived.**
  Integrate earlier only when Ben asks or when a concrete need requires the primary checkout to
  contain the work. A local worktree commit is the intended state between implementation and
  integration, not unfinished work that needs a remedial push.
- **A worktree Codex made, under `C:/Users/BenDe/.codex/worktrees/<repo>-<branch>`, is an
  ordinary linked worktree of the primary clone, and a Claude session works in it under these
  same rules.** Ben's question, 2026-09-07, answered by `git rev-parse --git-common-dir` there
  naming the primary clone's `.git`. The same holds the other way round for a worktree Claude
  made under `<repo>/.claude/worktrees/`.
- **More generally, "is this ready?" carries an implicit "and if two easy, obviously-right
  things would make it ready, do them."** Me, 2026-08-03, on a session that had done exactly
  that: *"this is an example of something good I've seen you do."* The answer I want is **"it
  wasn't quite ready when you asked, but now it is,"** with the things done listed — not a
  readiness report handing the work back. This applies past pushing: an unfilled gap in a plan,
  a stale copy of a file, an uncommitted edit. The limit is *obviously right* — if the fix needs
  a decision, or is more than a couple of small steps, tell me what it is and let me choose.
- **The prior this is correcting.** "Work isn't done until it's pushed, and a push needs
  permission" is entirely reasonable for someone whose push lands on colleagues. It is not my
  situation — I work solo on every one of these repos, so a push is a backup and a deploy
  trigger, never a publication to a team waiting on me.
- **The gh-pages worry that motivated the old rule is already handled, and needs no timer.**
  Every repo of mine with a Pages workflow — twelve of them, checked 2026-08-02 — already
  declares `concurrency: {group: github-pages, cancel-in-progress: true}`. A rapid-fire series
  of pushes therefore produces **one** deploy, the last one: each new run cancels the one still
  in flight. The hard part I imagined, firing a trailing deploy for the 17th of 17 pushes, is
  what that setting already does. Do not add a `sleep`, a cron, or a "have I deployed in the
  last 10 minutes" check to a workflow on my behalf; if I ever want the deploy *delayed* as
  well as debounced, that is a separate ask.
- **Still ask before rewriting history or discarding work**: force-push, `--amend`, rebase,
  `reset --hard`, branch deletion, `stash drop`. Commit-at-will is about adding commits, and
  says nothing about removing or rewriting them.
- Commit **directly to `main`** — do **not** create a feature
  branch first. I work solo on all my repos and don't use pull requests or
  branch-based collaboration. (This overrides the harness default "if on the default
  branch, branch first," which once created an unwanted side branch I had to merge back.)
- **A worktree is the exception, because there the branch is the mechanism, not a
  workflow.** Git will not check the same branch out in two worktrees, so a worktree
  session has to commit somewhere other than `main`. That branch is one I asked for by
  asking for the worktree, not one invented on my behalf, and merging back at the end is
  the price of the isolation rather than a chore taken on for nothing. The bullet above
  bans branching as the **default for ordinary work**; it does not ban a branch a
  worktree requires. (Added 2026-07-31 — the original bullet predates my knowing what a
  worktree was.)
- **The scheduled final integration is verified in the worktree and reaches the primary clone
  only as a fast-forward.** Ben's decision, 2026-09-07, reversing the order this bullet gave
  until that day — merge in the primary clone first, run the suite there second: *"if there
  were any issue with the merge, wouldn't you want to catch it and fix it on the worktree,
  before it ever hit the primary clone's main?"* Four steps, once both checkout trees are
  clean:
  1. In the worktree, `git merge --no-edit main` (or `-F <message file>` for a merge that
     deserves a body). Merging *from* a branch that is checked out elsewhere is allowed; git
     forbids only checking it out twice. Resolve any conflict here, on the branch.
  2. Run the repo's suite in the worktree on the merged tree, with `REPOS_ROOT` set where the
     repo's `CLAUDE.md` says a worktree needs it. A failure is fixed by a further commit on the
     branch, never on `main`.
  3. In the primary clone, `git -C <main clone> merge --ff-only <worktree branch>`. The
     `--ff-only` is the check that `main` did not move between steps 1 and 3; if it refuses,
     go back to step 1 rather than let a second merge happen in the primary clone.
  4. Push `main`. A second suite run in the primary clone before the push is optional
     insurance at about 100 seconds; it is the same tree.
  What this buys: `main` never holds a commit the suite has not passed; a bad merge or a bad
  conflict resolution is one more local commit on an unpushed branch rather than a fix-forward
  on `main` or an ask-first rewrite of it; and the primary clone, where another session may be
  live, is touched by nothing but a fast-forward, which cannot conflict and needs no message.
  The cost is a back-merge commit, "Merge branch 'main' into <branch>", sitting at the tip of
  `main` afterwards — the shape a `git pull` on a feature branch leaves, and for a long-lived
  named worktree the right state anyway, since later work there starts from a tree that
  already contains `main`. The case that produced the rule: the MAM-basics integration
  `d5a2238f` of 2026-09-07 was merged in the primary clone first and tested second, and for
  the two minutes between, `main` held a commit nothing had verified; a failure would have
  meant a fix-forward or a `reset --hard` of an unpushed `main`. The worktree need not end
  before any of this; only its removal and its branch deletion wait for shutdown on Windows.
  The timing is a scheduling rule, not a resource constraint. (Ben, 2026-08-02, on exceptions
  to rules of this kind: *"as with most rules, I can imagine exceptions — and even if I can't
  imagine particular exceptions, it seems wise to imagine that there might be exceptions."*
  Worth reading as a note on how to write the rest of this file. The exception that bullet
  once named — push the worktree branch while a thorny merge is being worked out — is still a
  fair one, and the branch push is then deleted once the merge lands.)
- **What the isolation is worth:** when a second session is live in the same repo, two
  sessions staging in one index can commit each other's half-written work, which fails
  *cleanly* and therefore silently. That is worth the worktree; it does not make immediate
  integration necessary.

## all-repos.code-workspace is the roster: clone only what it lists
**"Set up GitRepos" on a new machine and "sync GitRepos" on this one are the same question,
and `MAM-basics/all-repos.code-workspace` is the whole answer.** Ben's decision, 2026-08-31:
only the repos its `folders` array lists are to be cloned. `MAM-basics/in/repo_maintenance_policy.json`'s
**`gitrepos_setup_rule`** key states it as ordered clauses — bootstrap MAM-basics first, since
the roster lives inside it, then clone each remaining folder by name.
`py/repo_util/repo_selection.py`'s `_how_to_obtain()` already maps a folder name to its clone
command, gists included, and is the implementation of record.

**NEVER enumerate GitHub to decide what to clone.** Not `gh repo list`, not "what is on GitHub
but missing here", not filtered by the archived flag. An inclusion list is the point: whatever
is not in the roster is not cloned, archived or not, fork or not, gist or not. There is no
exclusion list to consult — `repos_to_keep_absent` and `frozen_repos` are documentation, and
**omission alone does the work**. A repo Ben wants nowhere simply goes in no list at all.

- **Why an inclusion list rather than enumerate-and-subtract**, which is what this section said
  for a few hours on 2026-08-31 before Ben rejected it as too broad: under a set difference a
  deliberately removed repo and a newly added one are indistinguishable, since both read as
  "on GitHub, absent locally". That is not a gap to patch with a longer exclusion list; it is
  the proxy being wrong. Omission is self-enforcing and needs no register to defend it.
- **The case that produced this section: `trope`.** Discontinued 2026-03-19 in favour of
  MAM-basics; Ben parked its clone that same day as
  `GitRepos.old/trope.old.use-mam-basics-instead`. The 2026-08-31 sync cloned it straight back,
  because the March decision lived only in that repo's README and in the parked directory's
  name — and a sync reads neither. About 1.0 GB across the two copies, removed 2026-08-31.
- **Absence from GitHub's archived flag is not evidence a repo is wanted.** `trope` is not
  archived, so it looks live to anything enumerating GitHub. Its own README promises archival
  only "once all open issues have been closed or copied to other repositories", and 111 remain
  open — so it will keep looking live for as long as that is true. **Do not infer from an
  unarchived remote that a missing clone should be restored.**
- **Ben's instruction is usually narrower than a set difference, so do not widen it.** That
  sync was asked to add repos "that have been added over the summer, i.e. since the last time I
  used this machine". It implemented "on GitHub but not in GitRepos" instead, which is a
  different set — `trope` is in the second and not the first. When an instruction names a
  *recency* criterion, apply that criterion; a set difference is a proxy, and it is the proxy
  that dragged a discontinued repo back onto the disk.
- **`repos_to_keep_absent` and `frozen_repos` are both documentation now, and neither may be
  derived from the other.** A frozen repo keeps its clone and is merely left untouched, so its
  last-changed date goes on testifying to the pause; `repos_to_keep_absent` records why one
  particular absence was chosen, in the single case where the reason was worth keeping.
  **Most absent repos rightly appear in neither**, and adding them would build a second roster
  to keep in sync with the first — which is the failure the inclusion list just removed.
- **A gist's clone URL is not derivable from its name**, and `gh repo list` cannot see a gist
  at all, so a gist reaches a new machine only if its URL was written down. `Gist-ArtScroll` is
  in the roster and its URL is in `repo_selection.py`'s `_NON_REPO_WORKSPACE_FOLDERS`;
  `Gist-Hebrew-World` is in no workspace file, so it is not cloned, and its URL is recorded in
  `gitrepos_setup_rule`'s `gists` key because until 2026-08-31 it existed nowhere on the
  machine except inside its own clone's git remote.

## Periodic repository maintenance also retires completed Codex task folders
Ported verbatim from `~/.codex/AGENTS.md` on 2026-09-07 (Ben's text, github-misc commits
`32c8d5c` and `cb79c5a` of 2026-09-04); Claude sessions run the same maintenance runbook, so the
rule belongs on both sides. `py/main_repo_util.py` deliberately operates only on Git repositories,
but periodic maintenance also includes the judgment-based cleanup of completed task artifacts under
`C:/Users/BenDe/Documents/Codex`. **Do not create a second maintenance script for this work.** An
automated sweep cannot know whether a task is still active, whether a clone has recoverable local
work, or whether a forest is a deliberate handoff environment.

- **Screen dated task folders after the mechanical repository sweeps and the `doc/` sweep.** Keep
  `C:/Users/BenDe/Documents/Codex/ReviewForests` even when it is empty, and keep any active task
  folder. Do not remove `C:/Users/BenDe/Documents/Codex` itself while either remains.
- **A directory of repository-looking copies is not a worktree forest merely because it contains
  repository names.** A reusable forest has a `review-manifest.json` at its forest root and Git
  worktrees at the manifest's declared paths. A linked worktree's `.git` is a pointer file; a
  `.git` directory identifies a standalone clone, not a linked worktree. A `proposed/` directory
  whose copies have no `.git` marker is a proposal snapshot, not a forest.
- **Read a declared forest's manifest before running a repository command inside it.** Preserve a
  forest that still names a future phase or handoff. If a manifest is absent, do not call the
  directory reusable; inspect every Git directory before deciding whether the task folder can
  retire.
- **For each standalone clone, establish that the working tree is clean, its checked-out commit
  is already preserved in the primary clone or remote, and no local branch or object is the only
  copy of unmerged work.** A clone with `.git/objects/info/alternates` can expose dangling objects
  from its primary clone; `git count-objects -vH` tells whether the task clone itself has unique
  objects. Do not mistake those primary-clone objects for task-local recoverable work.
- **Also screen Claude cache and temporary-data directories outside `Documents/Codex`.** Do not
  hard-code a cache path: Claude's cache layout can change. Report each Claude cache or temporary
  directory with its exact path and measured size, treating a directory of 1 GiB or more as a
  maintenance finding. Do not call a directory cache merely because it is large: Claude project
  directories, session transcripts, and `memory/` directories can be durable work. Verify that a
  directory is disposable cache data before retiring it, and leave an uncertain directory in place.
- **Retire verified folders through the Windows Recycle Bin, not permanent deletion.** State the
  exact paths and why each path is safe; if any task folder's status is ambiguous, leave that task
  folder in place and report the question. Recycle Bin contents remain recoverable but still use
  disk space until emptied.

The MAM-basics runbook `doc/PLAN-repo-maintenance-across-GitRepos.md` carries the corresponding
judgment step (its step 7), so a repository-maintenance session learns that this work belongs in
maintenance without trying to automate the decision.

## Never change an issue's state without a comment saying why
Closing, reopening, reassigning or relabelling a GitHub issue writes one line into its timeline:
the event, the account, the timestamp. **It records no reason, and it will not record one later.**
So the reason goes in a comment, posted with the state change — `gh issue close --comment`, or a
`gh issue comment` immediately before. This applies to me as much as to you; I ask for it because
I have been on the wrong end of it.

- **The account is not the actor, so the timeline cannot tell us apart.** A session's `gh issue
  close` authenticates with my personal token, so its event reads `actor: bdenckla`,
  `actor_type: User`, `performed_via_github_app: null` — byte for byte what my own click in the
  web UI produces. Do not infer from a timeline entry that a human did something, or that a
  session did; the only honest reading is "this account did it."
- **The worked case, 2026-08-27: MAM-basics #260.** It was closed at 11:19 local with no comment.
  An hour later the work it tracked completed. Nothing on the issue said whether it had been
  closed because the *question* was answered — `skadish1` had answered it at 00:05 — or because
  the *work* was done, and those are different definitions of done for that issue: its title says
  "Investigate and document sigil ב2" and its "Done when" is entirely about evidence and
  confidence, while the replacement of ב2 by ת451 was the consequence rather than the scope.
  Establishing merely that no session had closed it took a scan of **483 transcripts** across
  every project directory. A one-sentence closing comment would have cost nothing and answered it.
- **Say when a comment is agent-written.** A commit carries `Co-Authored-By: Claude`, so commits
  are already attributed; issue comments and state changes have no such convention and are
  indistinguishable from mine. Put it in the text.
- **This is the cheap half of a bigger question I decided against.** A separate GitHub machine
  account for agent use would make every action self-identifying, and I already run exactly that
  pattern on Wikisource as `BDencklaBot`. On GitHub it is not worth it for attribution alone:
  ~20 repos to add a collaborator to, a second persona in front of `skadish1`, `gh auth` juggling
  whose failure mode is worse than the problem, and a possible paid seat for MAM-private. If I
  ever want it, the reason will be **permission scoping** — an agent token that cannot force-push
  or delete — not attribution, which this section fixes for free. A fine-grained PAT or a GitHub
  App would be the form, since an App's actions set `performed_via_github_app` and so are
  distinguishable without adding a second voice.

## Handing off to a task chip: be archivable BEFORE you spawn it
The handoff we use over and over runs: a session spawns a task chip, I launch the chip, I ask
the original session whether I can archive it, that session does a little work to become
archivable, I archive it. **So two sessions are live in the same repo by design, and the window
is exactly the readiness question.** Added 2026-08-10, when Ben pointed out that the overlap is
structural rather than anomalous.

- **OFFER a chip unprompted once a coherent piece of work is committed and pushed and the
  next task is separable** — don't wait for me to notice the session has got long. Ben's
  instruction, 2026-09-02, after asking whether a session could tell it had become
  context-clogged. **The honest answer is that it mostly cannot**, and that is why the
  trigger is phase count rather than a measurement: the `<total_tokens>` figure in each turn
  is the SESSION BUDGET, not how full the context window is, and it barely moves while the
  context fills, so treating it as an occupancy gauge is self-deception. Say plainly that it
  is not a gauge if I ask.
- **The symptoms that mean you left it too late**: re-reading a file you already read,
  re-deriving a figure you established earlier, losing a thread I had settled, or the harness
  summarizing the conversation out from under you. In the 2026-09-02 session that produced
  this bullet, a count of four was reported off a sample list already in view that showed two.
  Those are confirmations, not triggers — by the time one shows, the detail is already gone.
- **Spawn the chip LAST, after the worktree is clean and its write-back is committed locally.**
  Do not merge the worktree branch or push it merely to create the chip. A successor starts from
  the named local commit, while the original session retains responsibility for integrating that
  commit just before its own archive. In a primary checkout, where there is no integration to
  schedule, the older form of this bullet still holds — clean tree, nothing unpushed, the
  write-back committed and pushed, so that "can I archive it?" is answerable with a bare yes.
  (Reworded 2026-09-07 from `~/.codex/AGENTS.md`; until then it read "when there is nothing
  left you could be asked to do … nothing unpushed", with no worktree case.)
- **When Ben asks to archive the original session, do the scheduled integration before
  answering.** Integrate by the Git section's four steps — `main` merged into the branch and the
  suite run in the worktree, then `main` fast-forwarded in the primary clone and pushed — and
  give the clean worktree, the branch head, and the pushed `main` head as evidence. Do not say
  that a worktree session can be archived immediately after its chip is launched: that would
  incorrectly promise integration before its scheduled time.
- **And SAY so, in the message that carries the chip — reaching the state silently is half the
  protocol, not all of it.** Me, 2026-08-10, to a session that had run the readiness sweep,
  spawned the chip, and then written a summary that never mentioned readiness: *"I thought the
  new protocol was you'd get this session (and sessions like it) ready to archive (and state
  that they are ready to archive) before putting up a task chip."* The whole point of reaching
  the state early is that my "can I archive it?" becomes a bare yes — and a session that reaches
  it without telling me has not delivered that, because I am still the one who has to ask, which
  is the round trip the bullet above exists to remove. **Give the evidence with the claim**:
  clean tree, the write-back committed — and pushed, in a primary checkout — the heads of
  whatever other repos the work touched, and, in a worktree, the branch and commit that the
  archive request will merge into `main`. "Ready" on its own is something I would have to go
  and check.
  **Put it LAST — the final sentence of the final message, after the chip is announced — phrased
  with the sequencing in it.** In a primary checkout: "This session can be archived after you
  launch its chip." In a worktree, where the archive request triggers the scheduled merge: "After
  you launch its chip, ask this session to archive; it will then merge `main` into `<branch>`,
  verify in the worktree, fast-forward `main` to it and push `main`." (The worktree form was
  added 2026-09-07 with the Git section's rewrite, and reworded later that day when the
  integration's order was reversed — see that section.) This
  read "at the top or the bottom of the message" until 2026-08-10, and the top half is struck,
  for two reasons I gave the day the protocol was new. **There is no identifiable "top" of a
  response in an agentic session**: by the time the closing message arrives, a long stream of
  narration between tool calls has already gone by, so a line at the head of that closing block
  is buried in the stream rather than at the head of anything — *"the first thing that looks like
  a wrap-up comment I might be interested in is the heading."* Only the end is a well-defined
  place. And **the statement belongs beside the chip**, which the bullet above requires be
  spawned last; separating them puts the state at one end of the report and the action it governs
  at the other. **"Ready to archive" is the wrong phrasing** besides — it states a property,
  where the sentence above states what to do and in what order, and the order matters, since
  archiving before launching risks taking the chip with it. The evidence goes with that sentence
  or just above it, never instead of it. A yes/no answer to a question I actually asked still
  goes first and/or last per the prose section below; it is this *unprompted* declaration that is
  last only.
- **This defuses the "is this ready?" bullet above rather than fighting it.** That bullet is
  right, and it is also what creates the work in the readiness step: asked whether it is ready,
  a session correctly goes and does two easy obviously-right things — which is a *second* write
  to a repo the new session is already working in. Reaching the archivable state before the
  chip removes the occasion instead of forbidding the response. In a worktree the archive
  request does generate one piece of work by design — the scheduled merge into `main` — and
  that is the protocol working, not the readiness step failing.
- **Never treat a co-present session as a precondition failure.** It usually *is* the handoff
  partner. A transcript under `~/.claude/projects/<repo-slug>/` names in its first line the
  phase or task it was launched for, so identify it rather than counting its bytes: measured
  2026-08-10 in MAM-private, two successive phases each logged "a second session was live,
  against the plan's preconditions," and both times it was the previous phase's session writing
  a single burst 20–36 seconds after the new session started — Ben answering the archive
  question.
- **Watching transcript byte counts is the wrong instrument, so stop reaching for it.** It
  answers "was another session open?", which does not matter. What matters is "did another
  session's work interleave with mine?", and that is provable directly and cheaply: `HEAD` at
  the start equals `HEAD` immediately before committing; `git status --porcelain` empty at the
  start and holding only your own paths before staging; and the push landing fast-forward with
  no `--force`. Those three prove non-collision, and they cover the whole real surface — the
  shared index (the one silent failure), a file both sessions edit (loud, since `Edit` matches
  exact text read earlier), and the push (loud, and already the case to stop on).
- **The exception, and it is the one worth serializing for: a session that genuinely ends
  unfinished** — a rejected push, a decision pending, a half-applied change. There the
  departing session really does still have work, which is precisely when overlap could bite.
  Say so plainly instead of spawning a chip, and let me close it out before launching anything.

## A successor session verifies its exact checkout and commit before editing
Ben authorized these safeguards on 2026-09-06 after a Codex post-mortem: page edits had landed
in `C:/Users/BenDe/.codex/worktrees/7a5d/MAM-basics-post-stress-meteg` while Ben was viewing
`C:/Users/BenDe/.codex/worktrees/MAM-basics-post-stress-meteg` — both worktrees — and a later
handoff involved the primary clone. A warning to avoid the primary clone does not identify which
worktree should contain the work. The Codex-specific mechanics (`create_thread`, `list_projects`,
Handoff, provisional thread ids) are in `~/.codex/AGENTS.md` under "Task creation and recovery";
what follows is the part that holds for a Claude session too, ported 2026-09-07.
- **A fresh task continuing a named worktree should use that worktree directly**, not a fresh
  managed worktree — Ben's explicit preference. Additional isolation is appropriate when he asks
  for it or simultaneous editing requires it; state that reason. A Claude task chip gets a fresh
  worktree of its own, so a chip is the wrong vehicle when the work must continue in a named
  checkout; name the checkout the successor is to use, in absolute form, and the commit it must
  contain.
- **Identify the source before creating the successor**: the calling session's actual checkout,
  the intended checkout's absolute path, and the source commit holding the work to continue.
  These can differ. Put all three in the successor's prompt, with who integrates and when.
  Resolve a stale source before creating a dependent task.
- **Verify before editing.** `git rev-parse --show-toplevel`, `git rev-parse HEAD`, the branch or
  detached-HEAD state, and `git status --porcelain`, each checked against the intended checkout.
  The required commit must be present, or an ancestor of a deliberately newer start. Inspect a
  mismatch before editing or moving anything, and recheck when analysis becomes implementation.
- **Check commits before diagnosing lost edits.** Refresh HEAD, status, recent commits, the
  reflog and the relevant file diffs before searching stashes or unreachable objects. A checkout
  that was dirty earlier can be clean now because another session committed the work. An
  unreachable snapshot is not evidence of loss without its provenance and a comparison with
  committed work; never restore one merely because its paths match an earlier status report.
- **Verify the exact page path Ben is reviewing.** Generating and committing a page in a
  different worktree does not update that path. State the checkout and commit containing the
  result, and establish where the result will be reviewed before editing. A commit in one
  checkout does not establish that `main` or the remote contains it; verify each claimed
  integration or push.

## A worktree runs the primary clone's venv, by absolute path
A `.venv` is gitignored, so a fresh worktree has none and not one command in a repo's
`CLAUDE.md` will run there. **Share the clone's, spelled absolutely**, and put nothing named
`.venv` inside the worktree at all:
```powershell
C:/Users/BenDe/GitRepos/<repo>/.venv/Scripts/python.exe py/main_<x>.py <subcommand>
```
- **It is isolation-safe, and that is not obvious enough to leave unstated.** The interpreter's
  location decides nothing: CPython puts the *script's* directory on `sys.path[0]`, so
  `py/main_<x>.py` under the worktree imports the worktree's `py/`; and a `repo_root()` anchored
  to `Path(__file__)` — the shape all my repos use — resolves to the worktree too. Verified
  2026-08-03 in `masorah-books`, where a gate run this way wrote into the worktree's `books/itm/`
  and left the clone's untouched.
- **The primary checkout is not the development workspace.** The primary checkout is the clone
  under `C:/Users/BenDe/GitRepos/<repo>`; a secondary worktree is a linked checkout where a task
  runs. In a secondary-worktree task, the primary clone's `.venv` may appear only as the absolute
  interpreter path above. Every script path, current directory, source edit, generator,
  formatter, test, staging operation, and commit must use the task's verified secondary
  worktree. Being in some secondary worktree is insufficient: verify the exact checkout, as the
  section above on a successor session says. Do not run a generator, formatter, `git add`, or
  `git commit` in the primary checkout, and do not write its source or generated files while
  developing. The sole exception is integration immediately before archival (or earlier when Ben
  asks), by the Git section's four steps: `main` merged into the branch and the suite run in the
  worktree, then `main` fast-forwarded in the primary checkout and pushed — so even the exception
  touches the primary checkout with nothing but a fast-forward. (Ben's rule, 2026-09-06, ported
  from `~/.codex/AGENTS.md` on 2026-09-07; the fast-forward form is Ben's decision of that same
  day, recorded in the Git section.)
- **Sharing is also the better answer, not merely the cheap one.** One black version across every
  branch, so no reformat drift; no `pip install` per worktree; no second copy of a 40 MB tree that
  git is deliberately not tracking.
- **NEVER junction or symlink the venv into the worktree, however tempting.** It works
  perfectly — every relative command in the repo's docs runs verbatim — right up until
  teardown, and then **`git worktree remove`, plain, with no `--force`, follows the junction and
  deletes the real venv's contents.** It does not refuse and does not warn; on 2026-08-03 it
  emptied `masorah-books/.venv/Scripts/` and then died with "Permission denied" on the locked
  `python.exe`, leaving the clone with no Python. Recreating cost about a minute, and the point
  is that a routine cleanup command silently destroyed a resource three other sessions shared.
- **Copying the venv is a worse answer than it looks**, though it is not destructive: `robocopy`
  takes about 3 seconds for 41 MB, and the copy's `python.exe` re-roots itself correctly, so
  `python.exe -m black` and `-m pip` are genuinely the copy's. But `Scripts/black.exe`,
  `pip.exe` and every other console script embed an **absolute** `#!` path to the *source*
  venv's interpreter. That is harmless while both exist with identical packages, and it is
  exactly wrong in the one case worth copying for: a worktree pinning different library
  versions, where `pip.exe install X` then installs into the original venv and `black.exe` runs
  the original's black, with no error either time. `python -m venv` has no "clone from another
  venv" flag; if a worktree genuinely needs its own, build it and let pip serve from its wheel
  cache, which makes a recreate near-offline anyway.
- **The exception, and it is narrow:** a worktree whose *purpose* is a different set of Python
  libraries gets a real venv of its own. Then there is nothing shared to protect and this
  section simply does not apply — but say so out loud, because an unexplained second venv reads
  as a session that did not know the rule.
- **A repo path that reaches a sibling clone can break in a worktree, and the failure is loud.**
  Anything computing `repo_root().parent / "<sibling>"` lands in `.claude/worktrees/<sibling>`,
  or in `.codex/worktrees/<sibling>` for a worktree Codex made, and neither exists. In `masorah-books` exactly one pass is affected and it takes an override
  flag. Check for the pattern before running a suite in a worktree rather than after.

## Running scripts — no inline one-liners
- Never pass a script as a big inline command line: no `python -c "..."`, no shell
  here-docs, no piping data into `python -c` / `node -e`. Write a real temp file and run it.
- Same rule for multi-line CLI *arguments* (git commit messages, `gh`/PR bodies): no shell
  here-docs and no PowerShell here-strings (`@'...'@`) — write a temp file and pass it via
  `git commit -F <file>` / `gh ... --body-file <file>`.
- **Expect the harness to prescribe exactly what these bullets ban, and override it.** Claude
  Code's own tool descriptions push the other way: the Bash tool says *"for multi-line strings
  use a heredoc"*; the PowerShell tool, under *"Passing multiline strings (commit messages,
  file content)"*, says to use a single-quoted here-string; and Auto mode lists heredocs among
  the ways to "make file changes … rather than using the dedicated Read, Edit, or Write tools."
  The PowerShell one names **commit messages** as the use case, which is the very case the
  bullet above forbids. **This section wins** — it is the more specific, user-given rule.
  Added 2026-08-31, after a session broke `~/.gitconfig` *globally* with a `cat <<'EOF'` whose
  `\\` collapsed to `/`, leaving the invalid git escape `/U` — every later `git` command in
  that session died with `fatal: bad config line 2` — and then wrote its commit message with a
  second here-doc, the named case, which passed unnoticed because it happened to work. The
  harness teaches the construct without teaching its escaping, so the pull recurs every
  session; naming the collision here is what lets the rule survive it.
- **Name each such temp file uniquely, for its one task** — never a generic
  `issue_body.md` reused across unrelated jobs. A stale file from an earlier task gets
  posted in place of what you meant to post, and posted silently; `.novc/issue77_comment.md`
  and `.novc/pr_body_fix_dehi.md` are the shape to use. (From `mgketer/CLAUDE.md`, whose
  copy of this section Ben had deleted on 2026-08-24 as generic — this clause was the one
  part of it stated nowhere else. That file is `MAM-private/mgketer/CLAUDE.md` now, having
  moved there with mgketer's content on 2026-08-09.)
- **Why it actually breaks (not just style):** piping into `python -c` makes Python
  decode stdin with surrogateescape; with multibyte/Hebrew text a lone surrogate then
  throws on re-encode — this once silently pushed an empty body to a GitHub issue. A
  `.py` file that reads the data directly with `encoding="utf-8"` avoids it entirely.
- Temp-file location, in order of preference: a repo's gitignored scratch dir (e.g.
  `.novc/`), the session scratchpad, or `/tmp`. Read external data (e.g. `gh ... --json`)
  from inside the script with explicit `encoding="utf-8"`, never via a stdin pipe.

## Prefer the built-in tools to shell, and a Python script to assembled shell
Promoted from `mgketer/CLAUDE.md` on 2026-08-24, when the argument it used to rest on —
that every un-allowed Bash pattern costs an approval prompt — died with glob-based
permissions. Ben's Auto mode ended the prompts; his reasons below replaced the old one the
same day, and they are better. That file is `MAM-private/mgketer/CLAUDE.md` now, having moved
there with mgketer's content on 2026-08-09.

- **Default to Claude Code's built-in tools** (Read, Write, Edit, Grep, Glob) rather than
  doing the same job through Bash. Fall back to Bash only when a built-in genuinely cannot
  do it. The built-ins handle paths correctly, report their own failures, and produce output
  that is easier for me to review.
  - **Read files** — the Read tool, not `cat`/`head`/`tail`.
  - **Write/create files** — the Write tool, not `echo >` / `cat <<EOF >` / redirection.
  - **Edit files** — the Edit tool for an exact known string, a **Python script** for
    anything algorithmic. Not `sed` or `awk`.
  - **Search file contents** — the Grep tool, not `grep` or `rg`.
  - **Find files by pattern** — the Glob tool, not `find` or `ls`.
- **The Edit tool is not the whole alternative to `sed`/`awk`.** Ben, 2026-08-24: *"I'm not
  sure why you should restrict yourself to the Edit tool, since I'm not sure what algorithmic
  capabilities it possesses (regex search and replace perhaps)? Whatever algorithmic
  capabilities it has, I doubt that it can cover everything as well as a Python script can, so
  I see no reason to limit yourself to the Edit tool."* He is right about its reach: it is
  exact-string replacement with an optional replace-all, and **no regex at all**. Past one
  known string, write a script.
- **`sed` and `awk` stay banned, on measured grounds.** Ben, the same day: *"Your attempts to
  use sed and awk seem often to fail … it seems more reliable to just use Python scripts for
  everything."* The failure that prompted it: a `sed -i` meant to write `/uXXXX` escapes into
  a file had its backslashes eaten by sed's own replacement handling, so the file got a
  character class of bare digits — silently, and the script then ran and produced wrong counts.
- **The ban covers shell assembled for INSPECTION, not only for editing, and that is the
  expensive half.** Ben, 2026-08-24: *"please stop attempting to use all this UNIX/bash
  trickery. Perhaps I only see the cases that don't work, but even those are frequent. You just
  don't seem to be able to get it right, and don't seem to immediately notice your mistakes,
  and of course a not-immediately-noticed mistake can be costly … I consider the uttering of
  falsehoods as costly, especially since I think I followed up on that falsehood, i.e. I
  engaged with it, unlike with a lot of most of your output, which I pay little or no attention
  to."* And: *"instead of UNIX/bash trickery, i'm going to make my same old observation: just
  use python. the way people used to use perl to replace sed, awk, and other UNIX/bash
  trickery."*
- **Why it costs more than a retry:** a silently wrong pipeline does not fail, it **answers**,
  and the answer reaches Ben as a statement of fact. The case that settled it:
  `ls "$d/.claude" 2>/dev/null | tr '\n' ' ' || printf "(none)"`, where `||` tests the exit
  status of the **last** element of the pipeline, `tr`, which succeeds on empty input. So the
  fallback could never fire, two directories that did not exist printed as blank lines, and
  both were reported to Ben as existing but empty, with an offer to delete them.
- **So, past a single self-contained command, write a Python script that prints a labelled
  report, and read the report.** One plain command whose output is the answer is fine —
  `git status`, `git rm`, `git commit -F`, running a venv's python. What is banned is
  *assembled* shell: pipelines built to survey a tree, `||`/`&&` as control flow around one,
  `2>/dev/null` swallowing the very failure that matters, and any construct whose exit status
  comes from a different command than the one being tested.
- **Prefer `git -C <path>` to `cd <path> && git`**, for the same reason: the compound leaves
  the shell's directory changed behind it and hides which half failed.

## Throwaway scripts: the lowest bar of software
Ben, 2026-08-05: *"In general throwaway scripts can disobey any stylistic rules I have. They
truly have the lowest bar of software, which is just that they do what they are supposed to
(and no more!), regardless of how they accomplish that!"* A gitignored scratch script (a
repo's `.novc/`, the session scratchpad) is judged on whether it did its one job — not on
black, naming, dict-access style, fail-fast conventions, prose rules in its comments, or the
`sys.path` ban (whose section below records its own copy of this exemption). Two limits are
in the quote itself rather than exceptions to it: **"and no more"** — the script does its one
job, not a generalized version of it — and it has to actually *work*, so the mechanics that
keep a script from crashing on this machine (a real file rather than `python -c`,
`encoding="utf-8"` where non-ASCII flows) are self-interest, not style.

## No `sys.path` surgery — one entry point per repo, subcommands under it
I don't like `sys.path.insert` (or `sys.path.append`, or `sys.path[0:0] = ...`) in my source.
**Never add one to make an import resolve** — the count per repo is **zero, not one**. Where a
module can import from is decided by how the program is *entered*, and each of my repos already
declares that exactly once:
- **`python py/main_<x>.py`** — CPython puts the script's own directory at `sys.path[0]`, so
  `py/` is already there. A module under `py/accgram/` imports as `accgram.foo`, and top-level
  `py/` modules (`repo_paths`, `cmn.utf8_io`) import by their own names, with nothing added.

**Throwaway scripts are exempt — the zero count is about tracked source** (one instance of
the "lowest bar" section above, and the statement that prompted it). In a gitignored
scratch script (a repo's `.novc/`, the session scratchpad) do whatever resolves the import.
Ben, 2026-08-05, after a session rewrote a scratch script to avoid one: *"frankly, you can do
whatever crazy sys.path.insert stuff you want in throwaway (.novc folder) scripts!"* A tidier
option when the script leans on a repo's modules: name it `py/<name>.novc.py` inside the repo's
entry-point directory, under a `*.novc.*` gitignore glob (`masorah-books` has one as of that
day), and `sys.path[0]` is the same directory the real entry point gets.

**That covers the tests too, so there is no root `conftest.py` either.** A test runner is just
another `py/main_<x>.py`: MAM-basics runs ~900 tests (as of 2026-08-10; the count has grown
steadily since wlc-utils' Python moved in on 2026-08-01) and holman-ketiv-qere 51, both
through `python py/main_test.py` from the repo root, both with *no* path configuration of any
kind.
Since a repo needs none, none is the standard. **A bare `pytest` failing to collect with
`ModuleNotFoundError` is therefore the designed state, not a defect** — don't "fix" it with a
`conftest.py`, a `pytest.ini` `pythonpath`, a `.pth`, or `PYTHONPATH`. This **reverses** an
earlier version of this section that called one line in a root `conftest.py` "the whole
sanctioned use"; settled 2026-07-30, after MAM-basics demonstrated the zero-config path works
for a full suite.

**This is the rule you are most likely to break, so re-read it before adding any file.** A blame
crawl on 2026-07-30 found 18 `sys.path` mutations across wlc-utils, UXLC-utils and al-hatorah:
**14 sit in commits carrying a `Co-Authored-By: Claude`/Copilot trailer, and the other 4 are the
same one-line idiom with no evidence of a human author. I have never written one.** They are an
LLM reflex, not a convention of mine, and one of them entered as bullet five of a commit about
installing PLY (wlc-utils `51e2748`) — never a decision anyone made. Two were pure no-ops that
inserted the very directory CPython had already supplied.

**So a library module is not independently runnable.** If a module under a package wants a
command line, it does *not* grow a `sys.path` prelude plus its own `main()` and
`if __name__ == "__main__"`. It exposes `add_args(parser, repo_root=...)` and `run(args)`, and
a `py/main_<x>.py` at the top of `py/` adds it as a **subcommand**. `wlc-utils`'
`py/main_accgram.py` is the worked example — a dozen generators behind one entry point,
`generate-html-<name>` derived from a table rather than a file each.

**Why it actually costs something, beyond taste:**
- It is a *lie about where the module lives.* With `py/` and `py/accgram/` both on the path,
  `py/accgram/foo.py` is importable as **both** `accgram.foo` and `foo` — two module objects,
  two copies of every module-level constant and cache, and a class from one failing
  `isinstance` against the other. This is a real bug class, not a hypothetical.
- It forces `# noqa: E402` on **every** real import below it, because the imports must now run
  after a statement. That silences the linter for the whole block, so a genuinely misplaced
  import later can't be seen.
- Inserting a directory the launcher already put there is **dead code that still looks
  load-bearing** — nobody dares delete it, and it gets copied into the next file.
- It multiplies entry points. Five runnable modules mean five spellings in the docs, five
  hand-rolled `main()`s that drift apart (one on `argparse`, one on raw `sys.argv`), and
  cross-calls done by **subprocess** — one of my modules shelled out to another *by path* —
  where a function call was available all along.

**Don't reach for the other global fixes either:** no `conftest.py`, no `pytest.ini`
`pythonpath`, no `sitecustomize.py` (it never fires for `python py/main_*.py` — see the UTF-8
section below), no `.pth` file, no `PYTHONPATH=` in a doc telling me what to export before
running something. And there is no `pyproject.toml` anywhere in my repos, so "just
`pip install -e .`" is not the answer here; the entry point is.

**A `main_test.py` registry drops test files silently — check it after adding one.** The
pattern's one weakness is that its `TEST_MODULE_SPECS` tuple is hand-maintained with no
auto-discovery, so a test file nobody listed simply never runs. On 2026-07-30 *both* repos
then using the pattern had the bug: MAM-basics 2 of 34 unregistered (one of them edited four
times over seven weeks while never once executing), holman-ketiv-qere 2 of 8. This is worse
than the silent-green skip warned about below — an unregistered file reports nothing at all.
Where a registry exists, compare `py/main_test.py --list` against
`git ls-files "py/tests/test_*.py"` after touching a test file. Of those two repos only
holman-ketiv-qere still has one: MAM-basics dropped its registry on 2026-08-01, for exactly
this failure mode — its `main_test.py` is now a `pytest.main()` wrapper, and pytest discovers
`py/tests/` itself.

## Authored paths use forward slashes

In tracked source, docstrings, comments, documentation, test data and commands, write every
ordinary authored path with forward slashes. This includes Windows absolute paths
(`C:/Users/BenDe/GitRepos/MAM-basics`) and repo-relative paths (`py/tests/test_example.py`),
including paths inside normal Python strings. Do not write backslashes merely because the path
will be used on Windows: Python's file APIs, `pathlib` and ordinary Windows file APIs accept
forward slashes, while a backslash in a string can become an escape such as `\t` or `/U`.

For constructed Python paths, prefer `Path` composition (`repo_root / "py" / "tests"`) over a
separator-bearing string. Backslashes remain only where the syntax itself requires them — for
example the `\\?\` and `\\.\` Windows device-path prefixes — or where text deliberately
reproduces an external spelling byte for byte, such as quoted command output or an exact test
fixture. This is Ben's cross-repository standard as of 2026-09-02.

## Commands you hand *me* to run: PowerShell, one per block
My terminal is **PowerShell 7**, not bash. What you run in your own Bash tool is your
business; the moment a command is written for *me* to paste or click Run on, it has to be
PowerShell-valid:
- **Absolute paths** (`C:/Users/BenDe/GitRepos/...`) or `$HOME`. **Never a bare `~`** —
  PowerShell does not expand it for native executables like `git`, so it reaches the exe
  as a literal.
- **One command per fenced block.** No `&&` chaining, no `;`. The app's Run button takes
  the block as a unit, and a chain also dies outright in `cmd.exe` or PowerShell 5.1.
- **Why the habit survives:** tested 2026-07-27, bare `~` and `&&` happen to work in
  pwsh 7.6.3. That makes them worse than an outright error — they pass review, then fail
  in some other shell or context. Don't rely on the accident.

**A failing command is not always a syntax problem, and misreading it as one wastes a
turn.** The standing example: `git worktree remove` on the session's *own* agent worktree
cannot work while the session is live, because the shell is `cd`'d inside it and Windows
will not delete a directory a running process holds open. `branch -D` then fails too,
since the branch is still checked out there. Say "run this after the session ends" — no
spelling of it will work before then. Check whether the command is even runnable *now*
before handing it over.

## Plans are written for a FRESH session to execute
Assume the plan will be picked up by a session that has none of the context you have — a task
chip, a new window, or me a week later. That is the normal case, not the exception: I routinely
approve a plan and then have it run somewhere else, so a plan that leans on the conversation
around it is a plan that has to be re-derived. Written 2026-08-03, after a first draft said "Ben,
this session" and "since reverted" with no date, and gave no repo paths.
- **No deixis.** Never "this session", "as we discussed", "the change I made above", "since
  reverted". Date every decision and attribute it — "Ben's decision, 2026-08-03: …". A rejected
  alternative is worth a line only where it stops the executor re-proposing it.
- **Absolute repo paths, and which one to run from.** `C:/Users/BenDe/GitRepos/<repo>`, plus
  where the `.venv` is, since only some repos have one. Sibling repos the work reads get named
  too.
- **Name the skills and instruction files to load** before the first edit — the `hebrew-prose`
  skill above all, for anything touching accentuation prose.
- **Every figure carries the command that re-establishes it**, and the plan says to re-measure
  rather than trust it, treating a mismatch as a finding. Say what the numbers were measured
  against — the commit of each repo involved — because the tree will have moved on.
- **Say what is NOT expected to change**, not only what is. That is what turns an unexpected diff
  into a finding instead of noise.
- **Line numbers drift, so cite a searchable anchor too** (the identifier, the sentence). A plan
  written today and run tomorrow will not find `~line 1186` where it left it.
- **State the preconditions**: the baseline test count, whether the generated artifacts are
  currently in sync, and whether another session may be live in the same repos (they collide in
  any repo without its own worktree).
- **Carry forward the verification and the commit discipline** — the real regeneration commands,
  black on the files touched, and commit-and-push per the Git section above — so the fresh
  session does not have to infer them from these global rules alone.

## Format Python with black
- **black is my formatter of choice.** After writing or editing any Python file, run black
  on it before committing — mandatory, not optional.
  ```bash
  .venv/Scripts/python.exe -m black <file_or_directory>
  ```
  **Never prefix `PYTHONUTF8=1` — not on black, not on any tracked script.** Until 2026-08-09
  this line said to prefix one when running black in mgketer. That was wrong, and mgketer's own
  `CLAUDE.md` wins — that file is `MAM-private/mgketer/CLAUDE.md`, having moved there with
  mgketer's content on 2026-08-09, and the rule deferred to is its §"UTF-8 Everywhere" rule 6:
  the variable is for `.novc/` throwaway scripts only, where changing the code is not an option. black is a tracked tool run over tracked files and never qualifies. **A
  tracked script that dies on a codec error gets fixed, not prefixed** — see the
  Unicode-at-runtime section below. The retired line also named a single repo, which the very
  next bullet forbids.
- **Never write a list of repos here.** Which repos exist, which are exempt, and which files
  are skipped are all declared elsewhere (see the sweep bullet below); a copy of any of them
  in this file is stale from the day it is written. This entry has already been wrong twice
  that way. Cite the source, don't restate it.
- **A missing `.venv` is not a documentation bug.** Venvs aren't tracked and `CLAUDE.md` is,
  so a repo with Python and no `.venv` is simply un-hydrated — true of every fresh clone, and
  no reason to soften prose that names the venv path. Create it, or say it's missing and
  stop; there is no black on PATH on this machine, so there is nothing to fall back to.
- **Format only the files you changed** — don't reformat a whole repo unless asked. Pass
  multiple files in a single invocation rather than one call each.
- **No config: black runs at its defaults.** There is no `pyproject.toml` anywhere in my
  repos, and `MAM-basics/py/repo_util/run_black.py` passes no `--line-length`, so the limit
  is black's default of **88**. Don't infer a laxer limit from the long lines you'll see:
  those live inside triple-quoted string literals or comments, which black never reformats.
  A prose line at 128 chars inside a template string is not evidence that code may run long.
- **Repo-wide reformatting is its own commit.** If black wants to touch files you didn't
  edit, that's pre-existing drift (usually a black version bump) — don't let it ride along
  and make a small change look like a formatting commit. In MAM-basics there's a wrapper for
  exactly this, run from that repo's root:
  ```bash
  .venv/Scripts/python.exe py/main_repo_util.py --run-black --workspace-file all-repos.code-workspace --repos <repo>
  ```
  `--workspace-file` is not optional in practice: the default `MAM-basics.code-workspace`
  lists only the handful of repos MAM-basics generates into, so anything outside it dies with
  "Requested repo was not found in workspace folders". Drop `--repos` to sweep everything —
  which **reformats**, so don't run it just to look; check for `.venv/Scripts/black.exe` per
  repo instead.
- **Three declarations in MAM-basics settle what the sweep runs on.** To describe black's
  coverage, read these rather than recalling it:
  - `all-repos.code-workspace` — every repo a sweep can reach, and since 2026-08-07 the whole
    of that answer. **A frozen repo is not in it.**
  - `in/repo_maintenance_policy.json` — `frozen_repos`, the register of *what* is frozen and
    *why*: paused client projects whose last-changed dates are the point, so even an
    output-neutral reformat is unwelcome. It no longer **skips** anything at run time, and
    that changed on 2026-08-07, when the frozen clones left the workspace file. **The freeze
    is structural now** — a sweep iterates the repos a workspace file lists and resolves them
    under `--repos-root`, so a repo no workspace file lists cannot be reached at all, and a
    `--run-black` run prints no "Skipped: frozen" line. There is no override flag:
    `--include-frozen` was removed the same day, having become a way to ask for repos the
    sweep could no longer see. To thaw a repo, un-archive it on GitHub — all six frozen
    remotes are archived, so a push returns 403 — then clone it into `GitRepos`, re-add it to
    the workspace file, and delete its entry from the register.
    **That same 2026-08-07 move parked the six clones in a sibling `C:/Users/BenDe/FrozenRepos`,
    and THAT directory is retired: it is not expected on any machine** (Ben's decision,
    2026-08-31). Parking rather than deleting felt safer at the time, but each archived remote
    is itself read-only and durable, which makes the remote the copy of record and a clone only
    ever a second copy of it. A machine with no such directory is conforming, not broken — this
    one has none, and a full session's work noticed nothing missing. What settled it: a sync on
    2026-08-31 restored every non-archived repo and not one archived repo, so no sync can
    produce the directory, and keeping it would mean a manual per-machine act that nothing
    checks and nothing reminds anyone about. A repo's location on disk was never what enforced
    the freeze; absence from the workspace file is. The fullest statement, with the evidence, is
    that file's own `location_comment`.
  - `in/vendoring_policy.json` — which files *within* a repo are left alone, passed as an
    `--extend-exclude` (`0f7dfe3`). A vendored copy is maintained in its source repo.

  Whether a repo has Python at all is stored nowhere: `run_black.py` derives it per run from
  `git ls-files "*.py"`, and treats "tracked `.py` but no black" as a failure.
- **So the sweep, not a guess, is the authority on its own coverage.** It fails on a repo it
  cannot format rather than skipping it silently (`b5d093e`) — that old silence is how
  al-hatorah went unswept long enough to accumulate a 61-file reformat (`cab47317`, black
  26.5.1). Run it and read `BLACK_PROBLEM_COUNT`.
- **This entry is the statement of record — don't go looking for a fuller one.**
  `MAM-private/mgketer` retains its repository Black section. `codex-index-aleppo` stopped
  carrying an instruction copy when the third-stage evacuation made the repository a redirect host
  on 2026-09-04. **mgketer's
  is not at `bdenckla/mgketer` any more**: it moved with mgketer's content into
  `MAM-private/mgketer/` on 2026-08-09, and that repo's whole root is now one `README.md` —
  `gh api repos/bdenckla/mgketer/contents/CLAUDE.md` returns HTTP 404, and
  `gh api repos/bdenckla/mgketer --jq .archived` returns true, the repo having been archived on
  2026-08-27 (both checked 2026-08-31). This bullet named `bdenckla/mgketer` as the location until
  2026-08-31. **MAM-basics has no black section at all, and that is deliberate**: its
  `CLAUDE.md` is deliberately small, and the black material that once sat in its
  `CLAUDE-disabled.md` and `.github/copilot-instructions-disabled.md` said nothing this entry
  does not, so when those two files were deleted on 2026-08-03 (Copilot having stopped being
  used) nothing was moved into `CLAUDE.md` to replace them. Written 2026-07-15, when those
  stranded copies were the reason a global entry was wanted; kept because the reason has
  outlived them.

## Tests: differential and lint-shaped only
An audit of git history, code comments, and issues across all twenty repos (2026-07-25) found
exactly **four** occasions where a test demonstrably found something, and **zero** recorded
cases of a pre-existing example-based unit test failing later and thereby catching a
regression. All four winners share one of two shapes. Write those; skip the rest.
- **Shape 1 — differential check against an independent oracle.** Regenerate the whole corpus
  and compare against a frozen reference, or against a second derivation of the same fact.
  The three that paid: a MAM-private project's self-test reconstructing each verse's visible
  text from that project's emitted JSON and comparing it against the project's own input
  (`efa95ccf` — caught paseq silently dropped in 8 verses across 5 chapters; private annex §5);
  wlc-utils' PLY parity comparator against the frozen C checker (Phases
  A–F, `51e2748`..`cda21f9` — drove the port to 18,666/18,666 byte-identical, and *was* the
  completion criterion); the Decalogue transcription checks against vendored strands
  (`ee21ebb`, `80ca0df` — each found a real divergence in a printed edition).
- **Shape 2 — mechanical lint over the tree.** A decidable property of the *source text*, not
  of behavior: `wlc-utils/py/tests/test_transliterations.py` (issue #26) still fires (`9c95cf9`
  fixed a `tarkha`→`tarxa` it exposed).
- **Otherwise the generated output is the test.** Regenerate the tracked JSON/HTML with the
  real CLI command and read the diff. Unexplained diffs are failures.
- **Do not write** example-based unit tests that pin one hand-picked case, a string, or a
  name. Nothing in the record shows one catching anything, and they pin identifiers that get
  renamed: wlc-utils' suite has been dragged through `simanim_*`→`simtiq_*`, the `ws/` prefix,
  "oddball"→ungrammatical, and the meteg standardization — 253 of 807 commits touch `py/tests`.
- **Remember that no CI runs pytest anywhere.** Every repo's only workflow is a `pages.yml`
  Pages deploy. A suite that runs only when someone chooses to run it earns its keep by finding
  things *when written*, not by standing guard.
- **Beware silent green.** wlc-utils once had 21 test sites that skipped when an input was
  absent, reporting green having verified nothing (`25a7800` removed them); an empty
  `@parametrize` also reports as a skip. A missing input should FAIL.
- **Don't enforce this rule mechanically** (e.g. in `check_repo_standards.py`). "Is this test
  example-based?" isn't decidable, and #27→#49 is the cautionary tale: a guard test faithfully
  enforced decomposed ḥ across 21 files until the policy reversed to NFC, making the reversal
  more expensive. This one is advice a reviewer can override, not a gate.
- **Where this is documented:** `MAM-basics/doc/agent-planning-principles.md` §"Generated
  Outputs Are the Tests" (the fullest version, with the evidence; it was wlc-utils' `doc/` file
  until the 2026-08 evacuation); a short pointer in `MAM-basics/CLAUDE.md`.

## Prose: name the referent, don't leave me to reconstruct it
Applies to **every** kind of prose you write for me — rendered pages, docstrings, code comments,
commit messages, issue bodies, chat replies — which is why it lives here and not in the
`hebrew-prose` skill, where the first draft of it was nearly filed.
- **Never "one X … the other."** Never "the latter" / "the former". Never a pronoun or a
  demonstrative whose antecedent is a paragraph, or a section, back. Name both sides outright.
- The sentence that produced this rule (wlc-utils, 2026-07-27): *"which leaves the munax to one
  strand and the maqaf to the other"* — on a page that names the two strands explicitly
  everywhere else. Me: *"Just say what you mean: 'which leaves the munax to the תחתון and the
  maqaf to the עליון'!"*
- **Repetition is the cheaper cost.** This is the same trade already settled by "just say *has*,
  repeating it is fine" in the accentuation sections below — say the noun again rather than make
  a reader hold it in their head.
- **One thing, one name. Do not coin an alias, and never a coy one.** Me, 2026-08-07, on a repo
  maintenance report that called a single problem "drift", "the vendoring drift", and
  "`df3d6e7`'s cull left five sibling repos stale" within one message, never saying that the
  three named the same problem, then closed by offering to file an issue about "the vendoring
  drift": *"Please, please don't coin terminology referring to stuff obliquely/coyly. If you must
  coin, tell what the coinage means! I don't know why I have to keep asking this."* Reuse the
  name the thing already has, verbatim. If a short name really does earn its keep, **define it
  once where it is introduced — "call this X" — then use X and nothing but X.**
- **Synonym rotation is the specific habit to suppress**, and it is not a matter of taste. Me,
  same day: it reads like *"terrible advice given to 4th grade children by their well-meaning
  English teacher."* **Write boringly, as if in a computer program: things have as few additional
  names (aliases) (synonyms) as possible**, and *"don't be afraid to repeat a word as opposed to
  using a possibly-unclear pronoun ('it')"*. Varying the wording buys nothing — prose written for
  me is not graded on vocabulary range — and it costs the reader a guess about whether two names
  mean two things.
- **The end of a report is where this breaks most often**, because a closing sentence is tempted
  to compress a finding into a short coined phrase. The finding was already stated in full
  further up; repeat that statement, or refer to it in its own words.
- **Why it actually costs something:** the reader has to stop, go back, and work out which item
  got which property, then carry that mapping forward. Four saved words are not worth that, and
  the reconstruction is often ambiguous where the original was not.
- **Treat it as a habit of yours, not a slip.** My complaint was *"why do you so frequently write
  like this, leaving the reader to do so much work filling in details?"* — so re-read a draft
  looking for it, the way you would for a banned verb.

## Prose: if you announce a count, NUMBER the items — `1.`, `2.`, `3.`
Same scope as the section above: every kind of prose you write for me. Added 2026-08-25, after a
wrap-up headed "Three things you should know" was followed by **four** paragraphs.

**This is not a preference, and it sits in a file of preferences only because I keep breaking it.**
Ben, 2026-08-25: *"Why is this numbering preference of mine even a rule that needs stating? Because
it is not some weird whim of mine, i.e. not really a preference, it is just common sense."* He is
right, and the distinction changes how to read the section. Numbering an enumerated set is ordinary
practice in every register of writing, so **nothing here is idiosyncratic to Ben and nothing here is
owed to Ben in particular** — write this way for everyone, and never treat "he hasn't asked for
numbering in this context" as a reason to skip it. **The rule earns its place by naming a defect of
mine, not a taste of his.** That is also why it went unstated for so long: a convention this
ordinary is exactly the kind nobody thinks to write down, so a habit that violates it can run for a
long time without ever meeting a rule that says otherwise. Where a section of this file records
something genuinely particular to Ben — the paseq/legarmeh vocabulary, the `file:///` link, the
venv layout — it says so. This one does the opposite.
- **A heading that names a count is a promise the list has to keep.** "Three things you should
  know", "two findings", "the four files" — the moment you write the number, the items become a
  numbered list. Write `1.`, `2.`, `3.`. Me, 2026-08-25: *"SIMPLY NUMBER THEM, like any reasonable
  person (or AI) would do!"*
- **Bold lead-ins are not a substitute, and that is the specific habit to drop.** The failing
  wrap-up leaned on a bold first sentence per paragraph to mark the boundaries. It is weak even
  when it is applied consistently, and it was not: one item began ``main_diff.py mpp`` in code
  formatting rather than bold, so that item did not look like an item at all. Bold marks emphasis
  *within* a passage; numerals mark enumeration. They are not interchangeable.
- **Numbering is also what catches the miscount.** Three-versus-four is the whole reason this
  section exists, and it is a mistake that cannot survive typing `4.` under a heading that says
  three. Prose that only *implies* its structure lets the count drift; a numbered list makes the
  drift visible while you are still writing it.
- **Do not fix this by deleting the count from the heading.** "Some things you should know" keeps
  the mushy structure and merely stops advertising it. The count is useful — it tells me how much
  is coming. Keep the count and number the items.
- **Expect this to need re-reading rather than to have sunk in.** Me, the same day: *"I have tried
  to get you to stop writing like this but a few remarks in CLAUDE.md is no match for your original
  training."* He is describing a habit that reasserts itself, so treat this the way the section
  above says to treat its own rule: re-read a draft looking for it, the way you would for a banned
  verb.

## Prose: a heading NAMES ITS SUBJECT — no cute or coy titles
Same scope again: every kind of prose written for me. Added 2026-08-27, after a maintenance
report closed with a section headed **"One thing left for you"**, which announces that one thing
exists and withholds what it is. Me, that day: *"avoid such cute/coy titles. A small cost in
length yields something far more informative, e.g. 'One thing left for you: issue transfers'."*
And: *"I believe I've said this many different ways before, and asked that this be recorded."* He
had — the two sections above are the adjacent statements — but **this rule was recorded nowhere
until now**, which is why the many different ways kept not taking.

- **The test is whether the heading alone tells me what the section is about.** "One thing left
  for you" fails it; "One thing left for you: issue transfers" passes at a cost of two words.
  "What ran" passes. "Recommendation Ben should decide on" fails — decide on *what*?
- **The subject goes IN the heading, not merely in the paragraph under it.** I read headings to
  decide what to read; a heading that only promises content makes me descend into the prose to
  find out whether I wanted it, which is the work the heading existed to save.
- **Length is the wrong thing to optimize here, and that is the whole trade.** A heading is
  competing against the paragraph it heads, not against another heading. Two more words in the
  heading routinely save a paragraph of reading.
- **This is NOT the numbering rule and NOT the coinage rule, though it lives beside both.** The
  numbering section above is about a heading that names a count and then fails to number its
  items — that heading has a subject. The coinage bullet is about naming one thing two ways in
  the body. This one is about a heading with **no subject at all**. Fixing one does not fix the
  others; check for all three.
- **The tempting failures are the wrap-up ones.** A closing section is where the pull toward
  "One more thing", "What's next", "A note of caution", "Worth flagging" is strongest, because
  the writer already knows the subject and the heading feels like a transition. It is not a
  transition to the reader, who is scanning.
- **Expect this to need re-reading rather than to have sunk in**, exactly as the numbering
  section says of its own rule. Re-read a draft's headings on their own, as a list, and ask of
  each: does this name what is under it?

## Prose: a reported finding says what HAPPENED to it — "has been fixed", up front
Same scope as the three sections above: every kind of prose you write for me. Added 2026-09-02,
after a step-through report headed **"A stale figure in step 36's row, found by re-measuring for
this one"** described the defect at length, fixed it, and never said so except obliquely, in a
later sentence beginning "The correction also …".

- **Every finding you report gets an explicit disposition IN ITS LEAD** — the heading or the
  first sentence. The three that cover nearly everything: **"has been fixed"**, **"is filed as
  `<repo>#NN`"**, and **"is raised and not fixed, because …"**. Me, 2026-09-02: *"You go into
  excruciating detail describing this stale figure but don't mention (or it is buried) whether
  you fixed the stale figure. You do mention 'the correction' in 'The correction also makes a
  nuance statable …' but that seems rather implicit. Why are you not clearer and say 'A stale
  figure HAS BEEN FIXED in step 36's row …'"*
- **The detail was not the problem, so do not fix this by cutting the detail.** It goes
  underneath the disposition, where it costs me nothing. What I could not get from that report
  was the one thing I needed from it: whether anything was left for me to do.
- **Use the plain phrase, not a paraphrase.** "Has been fixed" is four words and unambiguous.
  "The correction", "this is now consistent", "addressed above" all make me reconstruct who did
  what and whether it landed — which is the same work the referent section above forbids making
  me do.
- **This is the heading rule's twin and neither one covers the other.** The heading section is
  about a heading with no subject; this is about a heading that names a subject and withholds
  its **status**. "A stale figure in step 36's row" passes the heading test and fails this one.
  Check for both.
- **A findings list is where this bites hardest**, because there the disposition varies from
  item to item and I am scanning for the ones that are still mine. A list whose items each open
  with their disposition can be read in one pass; one that buries them cannot be read at all
  without reading every word.
- **It applies to commit messages, issue bodies and plan rows too**, not only to chat. A plan
  row saying a figure was wrong should say in the same breath that it now is not.

## Unicode in source code — no orphan combining marks
- Never write a combining mark (a diacritic/accent/point with no base character) as a
  raw literal in code — e.g. `replace("<U+0323>", "")`, `_CGJ = "<U+034F>"`,
  `ch == "<U+05BD>"`. Standing alone in a string literal, a bare combining mark renders
  as an invisible or floating diacritic on the opening quote: unreadable, un-diffable,
  easy to introduce by accident. (Note I deliberately don't paste the raw marks even
  here — that's the point.)
- Instead use the named escape `"\N{UNICODE NAME}"` (e.g. `"\N{COMBINING DOT BELOW}"`,
  `"\N{COMBINING GRAPHEME JOINER}"`, `"\N{HEBREW POINT METEG}"`). Byte-identical at
  runtime, self-documenting, plain ASCII in the file. In languages without `\N{}`, use
  a numeric escape (`̣`) with the Unicode name in an adjacent comment.
- This is only about **orphan** marks in *code*. A mark anchored on a base letter is fine,
  and real Hebrew/multibyte *text data* in a string is fine. The antipattern is specifically
  a literal that begins with a bare combining mark.
- **My repos are now standardized to NFC (precomposed) for Latin-diacritic letters** (issue
  #187; the cross-repo LF + NFC migration of ~2026-07-01; enforced by tests such as MAM-basics
  `py/tests/test_h_dot_below_nfc.py`). So h-with-dot-below is the single precomposed codepoint
  U+1E25, **never** the decomposed `h` + `\N{COMBINING DOT BELOW}` (U+0323) pair. This
  **reverses** my earlier "decomposed is normal" guidance; two consequences:
  - **Editing is now simple:** a precomposed h-with-dot-below (U+1E25) that I type **matches**
    the file, so use the Edit tool normally — the old regex-wildcard / temp-script workaround
    for decomposed spans is obsolete. Author any new one precomposed (NFC).
  - **In `#` comments use plain ASCII** for the sound — `x`/`X` for the letter ח (as in the
    `taxton` identifier), never either Unicode form; the same NFC test enforces ASCII-only
    comments.

## Terminology: paseq vs. legarmeh (Hebrew accentuation)
Across MAM-basics and my other Hebrew-text repos (MAM-simple, al-hatorah, TMC, ...), "paseq" is
ambiguous and has a broad sense with two narrow
sub-meanings. Get this right without me re-explaining it:
- **The glyph.** Both meanings below render as the identical vertical line, Unicode
  `\N{HEBREW PUNCTUATION PASEQ}` (U+05C0, `׀`) after a word. There is **no separate
  codepoint** for the second meaning — same bytes either way, distinguished only
  grammatically/by tradition, never graphically. Code that names this constant broadly
  sometimes calls it `PASOLEG` (a paseq+legarmeh portmanteau) for exactly this reason.
- **Narrow-sense paseq** — an ordinary separating stroke, *not* an accent, not part of
  the musical cantillation system at all; just a reader's cue to pause slightly between
  two words despite a conjunctive accent joining them.
- **Legarmeh** — the *same glyph* after a conjunctive accent (usually *munax*, hence
  "*munax legarmeh*" in the 21 prose books; the poetic books — Psalms/Job/Proverbs —
  have their own forms, *azla legarmeh* / *mahapakh legarmeh*) instead **transforms
  that accent into a disjunctive**: it *is* part of the musical system, with its own
  melody and its own conjunctive accents (typically *merkha*). A word that just happens
  to carry a genuine conjunctive *munax* followed by an independent paseq is
  **graphically identical** to *munax legarmeh* — the difference is grammatical, not
  visible, and historically was adjudicated by Masoretic tradition/lists, not derivable
  from the bare text.
- When precision matters, use "paseq" only for the narrow sense and always write
  "legarmeh" (or "paseq/legarmeh" / "legarmeh-vs-paseq") when the broad glyph or the
  ambiguity itself is meant — don't let unqualified "paseq" stand in for both.
- **Where this is documented:**
  - The fullest treatment is a bilingual (Hebrew/English) essay in **MAM-basics**:
    `py/author_misc/he_ws_intro_to_mam_pasleg.py` +
    `he_ws_intro_to_mam_pasleg_footnotes.py` (adapted from Avi Kadish's introduction to
    *Miqra al pi ha-Masora*, ch. 2, "פסק ולגרמיה"), rendered at
    `MAM-with-doc/gh-pages/misc/he_ws_intro_to_mam_pasleg.html`. This is the canonical
    source — start here for the rules (e.g. legarmeh almost always precedes *revia*;
    the sole Biblical exception is Isa. 42:5) and the manuscripts'/editions' own
    marginal `לג׳`/`פס׳` annotations.
  - **MAM-basics** `uxlc/doc/clc-design.md` §7.16 ("Legarmeh vs. paseq distinction") is the
    design-doc-level summary of the same distinction as it applies to the CLC edition;
    it also notes there's a *separate*, unrelated ambiguous-vertical-bar problem (§2,
    the "under-bar") — don't conflate the two.
  - `wlc-utils/py/accgram` (the accent-grammar parser) already models *munax legarmeh*
    as its own grammatical category distinct from plain paseq.
  - `mb_cmn/hebrew_punctuation.py` (formerly vendored into UXLC-utils and wlc-utils) defines the
    shared `PASOLEG` constant referenced above.

## Terminology: silluq vs. meteg (Hebrew accentuation)
Same shape as the paseq/legarmeh entry above: one glyph, two grammatical readings,
distinguished only by **verse-position**, never by appearance. Get this right without me
re-explaining it — "the elyon/taxton/whatever strand calls for a silluq on `<word>`" is
flatly wrong whenever `<word>` isn't the verse's own last word, and I've caught this
exact mistake in the wild (UXLC-utils, 2026-07-02: a generated CLC note claimed Deut
5:7's maqaf-joined יִהְיֶה־ — mid-verse, not verse-final — "calls for a silluq", when it
can only ever want an ordinary meteg there).
- **The glyph.** Both meanings render as the identical mark, Unicode
  `\N{HEBREW POINT METEG}` (U+05BD). There is **no separate codepoint** for silluq — same
  bytes either way. Code that names this constant broadly sometimes spells it `MTGOSLQ`
  (a meteg+silluq portmanteau) for exactly this reason.
- **Meteg** (also *gaʿya*) — a purely **metrical** mark (secondary stress), **not an
  accent**, not part of the cantillation/trope system at all. It can sit on any word,
  anywhere in a verse, including mid-verse maqaf-joined words.
- **Silluq** — the *same glyph*, but **only** when it lands on the stressed syllable of
  the verse's own **last word**, immediately paired with *sof pasuq*. In that position it
  **is** part of the cantillation system: the strongest disjunctive accent, marking verse
  end (the same rank/role atnach plays mid-verse). Silluq is *defined* by that
  verse-final position — there is no such thing as "silluq" on a non-verse-final word,
  no matter how the word is otherwise accented.
- **Distinguishing rule — context, not codepoint identity.** Never name a bare U+05BD
  occurrence "silluq" without checking verse-finality first (does *this* word carry, or
  stand immediately before, that verse's own sof pasuq?). A word joined by *maqaf* to a
  following word is by definition **not** verse-final, so a U+05BD there is *always* an
  ordinary meteg — this is the single most common way the mistake happens, because a
  maqaf-joined word can otherwise look "accented enough" to seem verse-worthy.
- **Where this is documented:**
  - **MAM-basics** `uxlc/doc/clc-design.md` §2 states the rule directly ("the easiest of these
    to distinguish, by context — it falls on the last word of the verse, before *sof
    pasuq*"); `py/clc/clc_dual_cant.py`'s `_accent_name` is the code-level mechanism that
    must actually *apply* that rule (verse-finality is read off whether the strand's own
    atom text carries *sof pasuq* — see that function's docstring) rather than just
    hardcoding "silluq" for every U+05BD, which is precisely the 2026-07-02 bug.
  - **wlc-utils** `py/accgram/meteg_silluq_context.py` implements the same disambiguation
    independently (`u05bd_is_silluq()` — true only when the word is the verse's last
    Hebrew token, or failing that, when *sof pasuq*/paseq-legarmeh is present).
  - **MAM-basics** `py/foi/mtgmtg_explanations.py` and `unicode_explanations.py` document
    a related FOI (double-meteg words: "a meteg in the narrow sense (געיה) after the mark
    that serves as silluq"); `qamats_var_explanations.py` abbreviates the ambiguity itself
    as `mos` = "meteg or silluq" in its accent-name table.

## Maqaf sits on the accents' own scale, at the bottom of it
Same shape as the two entries above: a claim about Hebrew accentuation, not about one repo,
and it decides how a difference between two accentuations gets counted.
- **One scale of separating force** — disjunctives, then conjunctives, then **maqaf**. A maqaf
  separates the word it sits on from the next even less than a conjunctive does, so it has the
  weakest *separating* force on the scale. **Never write a bare "weakest":** a maqaf *binds*
  tightest, and unqualified it reads as backwards to anyone who knows Wickes or Yeivin.
- **No second ledger.** A maqaf is not an accent narrowly, but it is far too intertwined with
  them to be counted apart from them: an edition that moves a maqaf has not followed its
  exemplar "in every accent". This rejects the tempting convention that word division is counted
  separately from accents. The real problem that convention solved was double counting — and the
  honest fix is that a split compound was never two facts.
- **Counted once**, at the word whose marking changed, never as a regrouping plus an accent.
- **Stated as an exchange, both marks named** — "a maqaf where the other text has a *merkha*", or
  the other way about. Naming only the absent maqaf is the second ledger surviving in the phrasing.
- **Do not define a maqaf as "the atom left blank of an accent."** Fair as a gloss for the normal
  case (a maqaf-joined proclitic usually takes at most a meteg), but false as a definition: a
  compound can keep an accent on its joined atom. Koren's Deuteronomy עליון has *munax* on both
  atoms of לא־תעשה, and the Simanim Tiqqun has one on the joined לא of לא־יהיה and of לא־תעשה.
- **But prose is stingy with a second accent on a compound, and poetry is not** — that asymmetry
  is a major difference between the two systems, not a detail. In the **prose** system an accent
  on a non-final atom of a maqaf compound is rare, and largely nothing but a consequence of the
  compound being a single chanted word: the accents that turn up there are the ones that can be
  the **first of two on an atomic word**. That is also Yeivin's list of prose *secondary accents*
  (ITM §§221, 224, 233, 241): *munax*-zaqef, *metigah*-zaqef (*metigah* being in effect a special
  name for *qadma* used this way), and rare *merkha*/*mehuppakh* on the word of a *tevir*. A
  separate case, not a grammatical category at all, is a **maqaf written after a word that keeps
  its own conjunctive** — a manuscript habit, commonest with penultimate stress, that Yeivin §293
  uses to tell manuscripts apart and names **L** for ("a tradition somewhat different from the
  standard"). Yeivin §292 is also where the "atom left blank" *gloss* comes from, and he states it
  as a near-rule for the best manuscripts — a good gloss, still not a definition. The **poetic** system puts two accents on one chanted word readily and
  systematically: Breuer's Ch. 9 devotes §§20–21 to a mafsik plus a servant, and to two servants,
  in one word, and §§22–26 to the secondary *mahapakh*/*merkha*, with the governing rule that two
  marks "appear in one word — in the same manner in which they are used to appear in two separate
  words". (Breuer's English translation says **"hyphen"**, never "maqqef" — grep for that.) He
  also notes the maqaf after a secondary *merkha* is usually omitted, so the compound is written
  as two words though chanted as one, with "but a few cases" keeping it (Job 6:10, Prov. 25:20).
- **Yeivin is in two places and they are not the same.**
  `~/GitRepos/MAM-private/al-hatorah/py/itm/` is my
  *adaptation* — partial, sections still untranscribed.
  `~/GitRepos/MAM-private/masorah-books/books/itm/md-export-of-docx/`
  is the **full** OCR of the book, one file per section-run. Search the full OCR before concluding
  Yeivin says nothing about something; searching only the adaptation once produced exactly that
  wrong conclusion about the maqaf material above. That repo was `yeivin-itm` until 2026-07-31,
  when it was renamed and Breuer's CoS was merged in from `breuer-cos`, so Breuer's chapters
  are the sibling `~/GitRepos/MAM-private/masorah-books/books/cos/md-export-of-docx/` — one tree,
  both books. That tree moved out of its own clone into `MAM-private` on 2026-08-10, which is the
  extra directory in both paths above; `bdenckla/masorah-books` keeps a breadcrumb `README.md`, the
  history and its 19 issues, so a `masorah-books#NN` citation still resolves there. **al-hatorah
  went the same way**: its tree moved into `MAM-private` on 2026-08-10 and its clone came off the
  disk on 2026-08-11, so `~/GitRepos/al-hatorah` names nothing now, and `bdenckla/al-hatorah` keeps
  a breadcrumb `README.md`, the history and its 124 issues.
- **Where this is documented:** wlc-utils `py/accgram/printed_decalogue_strands.py` — the
  `MAQAF_IS_THE_LAST_RUNG` constant is the verbatim reader-facing statement, and its guardrail
  comment records the convention it replaced and why that one was wrong; the module docstring's
  "ONE scale" bullet is the rule for authors. `edition_transcription`'s "WHAT A DIFFERENCE MEANS"
  and `ctr_decalogue`'s "ONE SCALE HERE TOO" say the same at the two comparison harnesses. Short
  pointer in MAM-basics' own `CLAUDE.md`. Issue #76.

## A transcription is evidence about the transcription, never about the manuscript
Ben, 2026-09-01, on a session that had settled a question about the Leningrad Codex by reading
UXLC's XML: *"why would we trust UXLC. It is not MAM's policy to write notes about Leningrad
that in fact are about UXLC."* Same shape as the terminology sections above — a distinction that
is easy to collapse and expensive to have collapsed.
- **Never write, cite, or reason from "Leningrad has X" on UXLC's or WLC's authority.** Write
  "UXLC records X", and treat the manuscript as unconsulted. The same holds of every
  transcription in these repos: UXLC and WLC for Leningrad, the Aleppo data now in
  MAM-basics' `aleppo/` tree and the mgketer comparison for the Aleppo Codex, MAM-parsed for
  MAM. It holds of a printed edition standing in
  for a manuscript too.
- **The failure is silent and therefore cheap to commit.** A transcription agreeing with its
  manuscript is the normal case, so laundering one into the other usually yields a *true*
  statement, and the practice is never caught by being wrong. It was not caught on 2026-09-01
  either: Ben looked the word up in Leningrad and it did lack the mark, exactly as UXLC recorded.
  Agreeing was never what made the claim admissible.
- **A transcription's silence is weakest exactly where these projects most want to hear it.** A
  stress helper, a rafe, a fine ga'ya, a maqaf after an unaccented atom — those are the marks a
  transcription most readily normalises away, and they are the marks the accentuation work turns
  on. Treat "the transcription does not record it" as near-zero evidence for a mark of that class.
- **Where a manuscript claim is wanted and no manuscript has been read, say so and stop.** An
  unconsulted manuscript is a limitation to document, not a gap to fill with the nearest
  transcription. Reading one folio to settle one word is often cheap and is the right move; what
  is not right is quietly promoting a transcription to stand in for the reading nobody did.
- **This is not a claim that transcriptions are unreliable**, and don't turn it into one. UXLC is
  excellent and is the right instrument for a great many questions — including any question about
  UXLC itself, and any survey where a transcription's systematic behaviour is what is being
  measured. The rule is about what a finding may be *called*, not about which file to open.
- **Where this is documented:** `MAM-private/doc/PLAN-near-aleppo.md` §3 rule 7 is the fullest
  version, with the case that produced it (2 Chronicles 28:23's zarqa stress helper) and the two
  manuscript crops that settle that site, in `MAM-private/near-aleppo/img/`.

## Unicode at runtime — UTF-8 stdio on Windows; prefer files for non-ASCII output
- On Windows, when stdout/stderr is redirected to a file or pipe (a background task,
  `> out.txt`, CI, a tool capturing output), Python encodes those streams with the
  locale code page (**cp1252**), not UTF-8. The first `print()` of Hebrew/non-ASCII
  then dies with `UnicodeEncodeError`. Any Python entry point of mine that may emit
  non-ASCII must reconfigure the streams as the first lines of `main()`:
  `sys.stdout.reconfigure(encoding="utf-8")` and the same for `sys.stderr`. This is
  the established convention across my repos — match it; don't invent a "magic" import
  with global side effects or a `sitecustomize.py` (the latter never fires for
  `python py/main_*.py`: CPython adds the script dir to `sys.path` only *after* `site`
  imports `sitecustomize`).
- **Prefer files over stdout for non-ASCII.** I use stdout only for short ASCII
  progress (e.g. echoing each book name while iterating). Real/non-ASCII output —
  Hebrew, data dumps, reports — goes to a file opened with `encoding="utf-8"`, read
  back if you need to inspect it. Keeping Hebrew off stdout is itself a crash
  mitigation: if it never reaches stdout, the cp1252 error can't happen.
- **`PYTHONUTF8=1` is a workaround, and this bullet called it the "root-cause cure" until
  2026-08-09.** Setting it in the environment does make all Python use UTF-8 stdio and the
  UTF-8 default file encoding, so it works — but reaching for it is declining to write the
  script correctly, and the per-`main()` reconfigure above is the right answer rather than a
  "portable backstop" for machines missing the variable. Ben, 2026-08-09, settling this against
  the black section's old advice to prefix it: *"`PYTHONUTF8=1` should only be used if you can't
  be bothered to write scripts correctly, which I don't know why you can't do even for throwaway
  scripts, but if it is easier for you to workaround (what I consider to be) Unicode bugs in your
  throwaway scripts with environment variable hacks, go ahead."* So: **never on tracked code**,
  which gets the reconfigure and explicit `encoding="utf-8"` instead; permitted on a `.novc/`
  throwaway script, grudgingly, on the same "lowest bar of software" grounds as the rest of that
  section — and writing even those correctly is the preference, not merely the tidier option.

## Showing me a local file: hand me a `file:///` link, don't open anything
**Give me the URL and stop there.** To put a generated page or image in front of me, write a
markdown link whose href is an absolute `file:///` URL — forward slashes, three slashes after
`file:`:
```
[maqaf-nonfinal-accents.html](file:///C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/wlc/accgram/maqaf-nonfinal-accents.html)
```
**A repo-relative link is the wrong thing here.** `[page](gh-pages/accgram/page.html)` opens the
*source* in the editor — useless when the point is to look at the rendered page. The harness's
default "link files relative to the working directory" still governs source files you're
pointing me at (a module, a test, a line number); it is the **rendered artifact** that wants
`file:///`.

**Do not launch it** (me, 2026-07-28): *"in sessions like this, I usually already have the
document open, so particularly after the first turn, this results in multiple copies up in my
browser."* No `Start-Process`, no browser tool — a link costs me one click when the page isn't
already open, and costs me a duplicate tab when it is. Launch only if I ask. This **reverses**
the older advice here ("default to `Start-Process`", later softened to "but only the first
time"): even the first time is usually one copy too many.

**Never stand up a dev server or write a `.claude/launch.json`** — a local file needs no
server, and I bring up pages myself. That part was always right.

A link hands you no screenshot back, so **verify the content with the `Read` tool on the
file** — better evidence than eyeballing a screenshot anyway, and it is now the *only* evidence
you have, since you are no longer opening anything.

**Why not the Browser pane** (me, 2026-07-26): it is *"too unreliable, and has yet to show
any advantage over an external browser, for my needs."* Don't burn a turn diagnosing it and
don't reach for it as a fallback. This entry used to say local `file://` URLs *do* work and
that sessions kept wrongly concluding otherwise. Correction: they *can* work — the mechanics
below are accurate when they do — but they work unreliably enough that the right default is
the external browser. A 2026-07-27 session lost five minutes to `preview_start` timing out
after 300s, precisely because this section told it to insist. The same correction is in the
`hebrew-prose` skill (`references/rendered-prose.md`) and in
`MAM-basics/doc/edition-transcription-workflow.md` §2.

### If a task genuinely needs the pane's introspection
Only when you need something an external browser can't give (console messages, network
requests, evaluating JS against the live DOM). Absolute path, forward slashes, three
slashes after `file:`:
```
preview_start({url: "file:///C:/Users/BenDe/GitRepos/<repo>/.novc/scans/<x>.png"})
tabs_context()                                        # which tab ACTUALLY holds it
computer({action: "screenshot", tabId: "<that one>"}) # tabId is MANDATORY
```
Four things then mislead, each of which looks like "the file didn't load" — so distinguish
them from the pane simply being flaky, and give up quickly either way:
- **`computer` without `tabId` is an input-validation error, not a page error.** It reads as
  a load failure on the very first screenshot. Always pass `tabId`.
- **`navigate` reports success into the wrong tab.** A `tabs_create` id can come back with an
  empty `origin` while the content lands in a tab that appeared on its own — screenshots then
  answer "No site is open in this tab." After navigating, call `tabs_context` and use the tab
  whose `origin` is actually the file.
- **The pane fits an image to the viewport and will not scroll** (`scrollHeight ===
  innerHeight`), so a tall page is unreadable there. For a full-page look use the **Read**
  tool on the PNG — which is the reason the pane rarely earns its keep for *looking* at
  something in the first place.
- **"renders as static snapshots" does not mean inert.** It only means no dev server and no
  live-reload: scripts run, `<input>`s accept typing, `localStorage` persists across sessions.
  Verified on wlc-utils' `transcription_editor` page, whose earlier sessions' typed Hebrew was
  still in its `linetx:` keys.

**Regenerating a file in place will not refresh a tab** — tool result and tab title both claim
success while the old image is still shown. Write a **fresh filename**, open a **fresh tab**.
And **verify before saying it worked**, whichever browser you used.
