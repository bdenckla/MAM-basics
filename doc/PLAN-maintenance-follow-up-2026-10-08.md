# PLAN — follow-up to the 2026-10-07 repository maintenance

State: live; written 2026-10-08. Workstream A executed 2026-10-08 and 2026-10-09; Ben decided on
2026-10-09 to keep `collect` and `text_of`. Workstream B executed 2026-10-08; Ben reported on
2026-10-09 that its live deployment on his Windows machines is done. Workstream C executed
2026-10-09: the public half after Ben approved the list in “C1. Public audit result,
2026-10-08”, and the private half the same day.

Written by Claude (Opus 5.5) on 2026-10-08, New York time, in the session that ran the
2026-10-07 maintenance from `C:/Users/BenDe/GitRepos2/MAM-basics`. Ben had to switch that
machine off and asked whether a cloud session could do the remaining work: "Maybe for now our
goal will just be to record these decisions in a lightweight plan." Everything below is that
session's reconstruction of his replies to its maintenance report; each decision quotes him.
The private half, which names MAM-private paths, is `doc/PLAN-maintenance-follow-up-2026-10-08.md`
in MAM-private.

## Checkouts, integration and reading

- **Source:** MAM-basics `main` at the commit that added this file, or later. Check with
  `git log -1 --format=%H -- doc/PLAN-maintenance-follow-up-2026-10-08.md` and
  `git merge-base --is-ancestor <that commit> HEAD`.
- **Development:** a Claude cloud session's MAM-basics checkout, using `.venv/bin/python` after
  hydrating from the tracked `requirements.txt` and `constraints.txt`, or any full clone or
  worktree on Ben's machines. Record the checkout path and `HEAD` before editing.
- **Integration:** the executing session. Where it can push `main`, fetch, merge a moved
  `origin/main`, repeat the item's checks and push. Otherwise push the session branch and open
  a pull request for Ben. Checks follow `doc/review-trial.md`: focused checks per item, with
  the broad checks left to the nightly run.
- **Read first:** `AGENTS.md`, the `iterative-document-editing` skill, and the skills each
  workstream names. Another session edits near-Aleppo code most days, so fetch before
  workstream A and stop if its files changed since this plan.

## Ben's decisions of 2026-10-08

| Decision | Ben's words | Disposition |
|---|---|---|
| The near-Aleppo census reads note prose with phase 3's reader | "sure, let's do that" | Workstream A |
| The three instruction trims the report listed | "pursue all of those trims" | Workstream B |
| Reference audit of the five retirement-ready `doc/` families | "sure, please run the full reference audit" | Workstream C; deletion waits for his approval of the exact list |
| The Black sweep's exclusion stays narrow | "I concur, keep the exclusion narrow" | No action: `in/vendoring_policy.json` keeps its one `foreign_vendored` entry |
| Retire the evacuated phonetic-hbo clone in `GitRepos2` | "delete it please" | Done 2026-10-08: moved to the Recycle Bin after a recheck found no unique work |
| Add `project_doc_max_bytes = 32768` to that machine's `~/.codex/config.toml` | "go ahead and add the key please" | Done 2026-10-08; the file parses. Other machines still need the key, per `dot-Codex/README.md`, “Machine-local project-instruction budget” |
| Delete merged branches, sparing `codex/near-aleppo-ketiv-final-maqaf-20261007` | "I concur, please delete those branches" | Done 2026-10-08: 8 MAM-basics, 10 MAM-private and 1 hbofonts remote branches, each leased at its audited tip, and the local `dar-2026-09-29` with `git branch -d` |
| Permanently delete the two large Claude scratchpads | "Permanently/immediately delete, i.e. non-recycle-bin delete them, please" | Ben's own act: agent safety policy forbids an agent's permanent deletion |

Ben asked what retiring the 2026-09-29 review's records requires; answered 2026-10-09 from a
read-only audit. The review and its remediation are finished, but the turn-01 update's
disposition table is the only tracked home of ten deferrals: finding 21's heading fix in
`py/hbce_psalms/compare.py`, finding 22's next-refresh check, items 36.3 to 36.8, item 36.10's
suite run of `lint-receipt`, and item 36.11. Retirement first needs Ben's ruling on each, a
maintained home or a dismissal. One deleting commit would then link the 14 records at its
parent: in place for current guidance (`AGENTS.md`'s test-exception passage, D11 in
`doc/dual-agent-review.md`, two reasons in `py/tests/test_mega_coverage.py` and this plan) and
through single updates for the historical citers. No tracker cites a member. The skipped
`.novc/` wipe in `GitRepos2/MAM-basics` does not wait on retirement: no code reads that scratch,
and `doc/periodic-review.md`'s item 4 says it is not evidence. `py/main_repo_maintenance.py`
deletes `.novc/` permanently, so the wipe is Ben's own act unless an agent recycles it instead.

## A. Read the census's note prose with phase 3's closed reader

Load `hebrew-prose` before writing about these templates. The 2026-10-07 audit entry in
`doc/blind-dive-into-template-params-update.md`, “The 2026-10-07 maintenance audit found no
undeclared projection in new or changed walkers”, latent items 1 and 2, gives the evidence.

1. In `py/near_aleppo/census/nusach_aleppo_readings.py`, make `clauses` read a note body with
   `py/near_aleppo/phase3_policies.py`'s `_clauses(body, verse)`. That reader keeps link display
   text, writes Unicode PASEQ for the legarmeh template and the narrow-sense paseq template, and
   raises on a template it does not name. Its `verse` argument appears only in its error
   message; pass the census's own verse reference. The caller is
   `py/near_aleppo/census/stress_helper_census.py`, `main`, at `nar.clauses(...)`.
2. Delete what that leaves uncalled in the same module: `flatten`, `text_of`, `collect` and
   `keys_for`, after `git grep` confirms no caller.
3. Expected outputs: the five baselines under `in/near-aleppo/census/` stay byte for byte. On
   2026-10-07 at `72c698939af4b89dd2025a761cb4a85f21e5af56`, none of the 18 clauses that
   `stress_helper_census.txt` reports contained a template. Any diff is a finding to explain
   before committing.
4. Checks: `py/main_near_aleppo.py --check`;
   `py/main_test.py py/tests/test_near_aleppo.py py/tests/test_near_aleppo_note_content.py`;
   Black on the changed files; `python -m ruff check py`.
5. Record: append a dated entry to `doc/blind-dive-into-template-params-update.md`, and correct
   in place that entry's present-tense sentence "Three latent items remain unfixed."

## B. Make the three instruction trims Ben approved

Edit canonical copies only: `dot-Codex/user-wide-AGENTS.md` and the repository's `AGENTS.md`.
Never edit `~/.codex/AGENTS.md` or `~/.claude/CLAUDE.md`. Sizes measured 2026-10-07: the common
body 28,733 bytes, `AGENTS.md` 16,998 bytes against Codex's 32,768-byte project budget.

1. **Common body, worktree material, about 3.4 KB.** Move “Linked-worktree safeguards shared by
   Claude and Codex” and three worktree items of “Git and commits” (the bullets beginning "A
   secondary worktree uses its existing local branch." and "Integrate a worktree branch
   immediately before the task is archived", and the paragraph beginning "An ordinary secondary
   worktree commits locally without pushing its branch.") into a skill both agents load for
   worktree work. Build it from `dot-Codex/skills/codex-worktree-tasks`, whose agent-neutral
   rules already repeat much of this, and declare it in `dot-claude/shared-skills.txt`. Keep
   about 600 bytes in the body: verify the exact checkout, use the home clone's interpreter by
   absolute path, never junction or copy an environment, and load the skill. Ben's decision
   reopens finding 11.2 of `doc/user-wide-instruction-conversion-reconciliation.md`; record that
   there under the receipt rules.
2. **Common body, configuration sections, about 1.5 KB.** Reduce “Canonical user
   configuration” and “Claude Code only: cloud SessionStart installation” to about 350 bytes:
   never edit a live copy, the canonical paths, and a pointer to `dot-claude/README.md`,
   “Main-sourced deployment and check”, and `dot-Codex/README.md`, which hold the procedure.
3. **`AGENTS.md`, hebrew-prose routing, about 1.5 KB.** Reduce “Invoke the `hebrew-prose` skill
   before accentuation prose” and its subsection “Claude Code cloud SessionStart installation”
   to a short pointer. The skill's “MAM-basics prose” bullet and “Canonical copy” section already
   carry the repository exception and the deployment.

Checks: report each file's UTF-8 size before and after; confirm every moved rule has exactly one
home and that each trimmed passage's pointer resolves; run `py/main_test.py`. After the push,
someone on each of Ben's Windows machines runs, from a full MAM-basics clone:

```powershell
./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config
```

Ask Ben before taking up any other opportunity from the 2026-10-07 audit. Those were not put to
him. MAM-basics sections whose owning documents hold the detail (about 1.9 KB). The
2026-09-30 test-exception paragraph (about 0.8 KB). “Repository topology is task-specific”
(about 0.8 KB). Small duplicates (about 0.9 KB). Two forest paragraphs of the common body (about
0.65 KB). The common body's second hebrew-prose pointer (about 0.44 KB). hbofonts' “Generation
and verification” (about 0.45 KB). MAM-private's file (private half). Trial-dependent text, at
the trial's seven-night assessment.

## C. Audit the five retirement-ready families; delete nothing yet

Follow `mam-repository-topology/references/repository-maintenance.md`, “Manual document
retirement”, and the `github-issues` skill. In a cloud session, use that skill's REST read and
record any tracker the session cannot reach. The three public families:

1. `doc/PLAN-shared-html-styles.md`: no tracked reference was found on 2026-10-07, and its
   successor `doc/html-styles.md` is a runbook.
2. `doc/PLAN-retire-mam-parsed-plain.md`: only finished review records cite it.
3. `doc/PLAN-remediate-review-findings-2026-09-26.md` with its `-update.md`: its deferrals also
   live in the 2026-09-26 review's turn-01 update. Citations from MAM-private, and the other
   two families, are in the private half.

For each family, find the last commit whose tree holds every member, as a full SHA on
`origin/main`. Classify every tracked and issue reference as current guidance or historical
evidence, and prepare the permalink corrections through each citing receipt's single update
file. Bring Ben the exact deletion list with those corrections; delete only after he approves
it.

### C1. Public audit result, 2026-10-08

Recorded by Claude in the cloud session that executed workstreams A and B, from a read-only
sub-agent audit whose reference census the session re-ran on the merge of `origin/main` at
`7c82b5df6deeee66568830bf63b7ba0a2cee1350`. MAM-private and every tracker but MAM-basics' were
unreachable, so their citations remain for the private half. Nothing blocks retirement.

1. **Last changes.** `doc/PLAN-shared-html-styles.md` last changed in
   `43740def00c9bd8ed5858bb78a48076fe924d224`; `doc/PLAN-retire-mam-parsed-plain.md` in
   `1e14a8a17accb81cd6f3ef6f3f7427c230546a61`; the 2026-09-26 family's update in
   `1ad77de0d1a416e771ef12ed1a5b54550136f758` and its base in `e4934b6e`. Neither of the first
   two ever had an update. This clone is shallow at `9b654fd4`, so these came from GitHub's REST
   commit history; every member is byte-identical from its last change through `7c82b5df`.
2. **Permalink commit.** Following `e4934b6e`'s retirement, the corrections link the parent of
   the deleting commit, which holds every member. Record that parent's full SHA when the
   deletion is made; `7c82b5df` qualifies today.
3. **Current guidance.** Only this plan cites any member; correct it in place in the deleting
   commit. The plan's claim that only finished review records cite the plain retirement plan is
   slightly narrow: the executed `doc/PLAN-remediate-review-findings-2026-09-29.md` and
   `doc/blind-dive-into-template-params-update.md` also cite it.
4. **Historical citers and where each correction goes.**
   - `doc/dual-agent-review-2026-09-29-turn-01-claude-update.md`: one appended “Archived receipt
     references” entry covers that round's turns 01, 03, 07, 08, 09, 10 and 11 and the update
     itself, per `doc/dual-agent-review.md`'s single-update rule. It notes that turns 01 and 09
     count the 2026-09-26 base's lines before its line-4 pointer, as at `8c2fa6c3`.
   - `doc/PLAN-remediate-review-findings-2026-09-29.md`: a new
     `doc/PLAN-remediate-review-findings-2026-09-29-update.md`, with the one pointer line below
     the base's line 3.
   - `doc/blind-dive-into-template-params-update.md`, `doc/PLAN-remediate-review-findings-2026-10-02-update.md`,
     `doc/review-findings-2026-10-02-update.md` and `doc/review-findings-2026-10-04-update.md`:
     one appended entry each.
   - `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`: its two relative links to the
     2026-09-26 plan, in the passages beginning “uses the recovered” and “The live [remediation
     plan]”, become permalinks in place, with an appended entry; its link at `1a92af88` stays.
5. **Issues.** A repository-scoped REST download of 301 issues and pull requests and 313
   comments found no reference to any member. Issue 288's comment naming “the 2026-09-26
   review-remediation session” names a session, not a file.
6. **Deferrals.** Every item of the 2026-09-26 plan's “Explicit deferral and no-action ledger”
   appears in `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`. Two details appear only
   in the plan: 31.8's “Do not silently add an EVR reading to the Psalms 72 report” and 35.4's
   “The optional three undated-rule label clarifications are left unimplemented because this plan
   proposes no finite replacement for them.” Whether that update's entry repeats them is Ben's
   choice.
7. **Proposed deletion list.** `doc/PLAN-shared-html-styles.md`,
   `doc/PLAN-retire-mam-parsed-plain.md`, `doc/PLAN-remediate-review-findings-2026-09-26.md` and
   `doc/PLAN-remediate-review-findings-2026-09-26-update.md`. The successor `doc/html-styles.md`
   stays.

### C2. Public retirement executed, 2026-10-09

Ben approved the C1 list and its corrections on 2026-10-09, including the repetition of the two
deferral details of item 6. The retiring commit deleted the four files of item 7 and made the
corrections item 4 lists, linking the families at
`38a8db9ae851b83d43b5c5ad42c007943b54d724`, the last commit on `origin/main` whose tree holds
every member, with the member blobs the audit recorded. The private half's audit, on
2026-10-09, searched every tracker this audit could not reach, MAM-private's included, and
found no reference to any member. It repointed MAM-private's one citation of the 2026-09-26
family to this archive, and on Ben's approval retired MAM-private's own two families that day.

Ben approved three public follow-ups of the private half's report the same day. MAM-basics
`545e0c96378be0ac5d0a30700246ba6509d52110` gave his naming preference a home in
`Yeivin-ITM/README.md`, “Permission and authorship”. phonetic-hbo
`fefc401ffadb3dab3843ef465bb2c75814558d9f` restored its README's link to the former
masorah-books repository, which the 2026-10-02 redirect conversion had dropped against his
decision of 2026-09-30; the deployed `gh-pages/` tree is unchanged. Two leftover phonetic-hbo
clones on the machine that ran the 2026-10-07 maintenance, and the temporary clone used for that
README commit, went to the Recycle Bin after recovery checks.
