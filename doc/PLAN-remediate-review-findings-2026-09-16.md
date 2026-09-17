# Plan: remediate the closed 2026-09-16 dual-agent review

State: live. Written 2026-09-17 after Ben approved the dispositions. Ben has not yet approved the
concrete editorial wording in this plan, and no remediation in this plan has been executed.

This is a fresh-task plan for the existing shared checkout
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16` on branch
`dual-agent-review-2026-09-16`. The complete decision package is recorded at required source
commit `fbaae3d0b0bf66792d5ab1d0095eb4358cffaaa6` in
`doc/dual-agent-review-2026-09-16-turn-01-claude-update.md`. Current `main` at
`d3edadc6e3d8d85964bf503c0e207ee357cb6561` was merged by `6911d1d4` before this plan was
written. The plan remeasured the merged tree rather than copying the review's frozen counts.

## 1. Authority, skills, checkout and baseline

Before editing, read `AGENTS.md`, the decision entry named above, all six numbered review turns,
`doc/dual-agent-review.md`, and `doc/periodic-review.md`. Load these skills and references:

1. `codex-worktree-tasks`, including `references/task-lifecycle.md` and
   `references/worktree-runtime.md`, for the worktree, backup, integration and cleanup rules. A
   Claude executor reads `dot-Codex/skills/codex-worktree-tasks/SKILL.md` and those two tracked
   references directly when the Codex-only skill is not installed;
2. `hebrew-prose`, including `references/core-rules.md`, `references/terminology.md`,
   `references/mam-basics.md` and `references/verifying.md`, before touching accentuation prose;
3. `github-issues`, including `references/citations.md`, `references/reading-and-writing.md`,
   `references/state-changes.md` and `references/mam-basics-trackers.md`, before changing issue
   citations; and
4. `mam-repository-topology`, including `references/evacuated-repositories.md` and
   `references/repository-maintenance.md`, before changing topology, retirement or deployment
   instructions.

The remediation task's root agent is the only writer, stager and committer in this shared
checkout. Read-only sub-agents may remeasure bounded surfaces; the root agent verifies every
adopted result. Before each wave, verify the exact checkout, required source, branch and clean
tracked state:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 rev-parse --show-toplevel
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 rev-parse HEAD
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 branch --show-current
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 merge-base --is-ancestor fbaae3d0b0bf66792d5ab1d0095eb4358cffaaa6 HEAD
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 status --short --branch
```

The worktree is already locked for the active review. Immediately before remediation, merge the
then-current local `main` into this branch. If `main` moved beyond `d3edadc6`, remeasure every
drift-prone inventory below and treat a conflicting later fix as a disposition, not as work to
repeat.

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 merge main
```

Use the primary clone's interpreter from the worktree root for every Python command:

`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.

The review branch is a long-lived backup branch under the user-level exception. After every
commit, push `dual-agent-review-2026-09-16` to `origin`; do not push `main` until final integration.
Substantial throwaway measurements belong in uniquely named UTF-8 files under this worktree's
gitignored `.novc/`.

The following current-tree facts are dated measurements, not invariants:

- the filename-command census finds 27 filename-returning Git sites; all 27 use `-z`, while the
  lint sees 14 and misses 13;
- finding 12.2's current broad grep finds 137 files and 2,027 `.novc` lines in this branch and 132
  files and 2,000 lines in current `main`;
- the four skill/reference files in finding 19 contain 13 headings without a preceding blank line
  and eight overlong prose lines after excluding tables and the clone command; and
- the fourteen non-merge commits named by `doc/PLAN-mega-speedup.md`'s exact pathspec and range
  `132f2f3e..bca64824` are `20f18020`, `6dbd27e7`, `3b1adf45`, `dcd2c1f6`, `d6a6764d`,
  `1b7b97ef`, `5cb06e25`, `2239cbad`, `cde921bf`, `7fd381db`, `af1c404a`, `15c09692`,
  `8b2386b0` and `fa517040`.

## 2. Approval presentation by public-facing risk

### 2.1 Public-facing documents: high reader-facing risk, no product reach

No generated HTML changes. Three reader-facing README edits remain.

In both `doc/meteg-after-silluq-snips/README.md` and
`doc/lam-2-3-akhla-snips/README.md`, retain each existing filename prefix and replace the
conflicting general coordinate rule with:

> A Leningrad crop may include both column and line when Ben has read the line from the image; the
> relevant section must say when the column comes only from the estimator. For another source,
> include only coordinates established from its image or retained index.

Remove the now-duplicate two-sentence rule from each Leningrad subsection, leaving the preceding
page-description sentence. Do not change `doc/review-findings-2026-09-10-update.md`'s preservation
statement: the Leningrad-specific rule really was preserved.

In `in/mam-ws-intro/README.md`, replace the source-number wording with:

> `doc/sigil-decoding.md`'s Source Hierarchy item 1 records what a summarizing fetch did to the
> sigil roster on 2026-08-06, and the mirrored wikitext is where you can see what it flattened.

Replace the mark-order pointer with:

> This tree is exempt from the MAM-normal mark-order rule documented in
> `doc/mam-normal-mark-order.md`.

Replace the Phase 3 assertion with:

> `git show --stat 985262e2` names every file removed; Phase 3 of
> `doc/PLAN-mega-coverage.md` records the totals.

These edits change guidance, not crop bytes, mirrored introduction bytes or generated pages.

### 2.2 Public-facing data: high risk

None. The plan changes no corpus JSON, XML, image or other distributed data.

### 2.3 Other work by product reach and act risk

The remaining work consists of review and timing receipts, live plans, internal documentation,
agent instructions and skills, Python diagnostics and tests, and maintenance tooling. Product
reach and act risk remain separate:

- finding 13.3 lies on an accgram mega path and therefore reaches the generator tier; the final
  mega must prove that the diagnostic-only repair produces no tracked product diff;
- finding 12 has no repository-product reach, but its subject is destructive retirement tooling;
  its wave runs only simulations and must not retire a real worktree;
- adding the permitted pointer to a finished receipt base is a narrowly authorized historical
  record edit; and
- the final push of `main` is outward-facing and triggers the Pages workflow, while the later
  user-configuration deployment writes outside the repository.

## 3. Current merged-tree disposition map

| Finding | Disposition at `fbaae3d0` |
| --- | --- |
| 1 | Open: reconcile the two README rules with the approved wording in section 2.1. |
| 2 | Open: correct the three-resource cloud-session account and record the old plan's false no-edit assertion in that finished plan's new update sibling. |
| 3 | Open but changed by later retirement: classify `.Codex` historically and replace four present-tense blob assertions with checkpoint, pointer and retirement history. |
| 4 | Open and wider: implement a general lint repair for 13 missed current sites, not a six-site patch and not a pinned count. |
| 5 | Open: add the paragraph-join exception to the three absolute pointer-only rules. |
| 6 | Open: create the September 14 remediation plan's update sibling and record every correction there; do not rewrite the finished base beyond its pointer and mechanically necessary paragraph join. |
| 7 | Open: correct the topology skill's summary and deploy it only after integrated `main` is pushed. |
| 8 | Open: repair the pointer, Phase 3 and current-repository claims, plus the non-issue source-number form. |
| 9 | Partly resolved by current `main`; repair only the remaining current references, paths and issue spellings. Preserve truthful historical retired-plan paths. |
| 10 | Closed by current `main` plus `fbaae3d0`: the README list, common-body wrapper and D11 backup exception are current. |
| 11 | Open: restore dated or explicitly undated provenance without implying that any underlying policy disappeared. |
| 12 | Part 12.1 closed by the current reparse-point guards. Part 12.2 remains open in the broad `.novc` citation gate. |
| 13 | Part 13.1 now needs only an owner-scope diagnostic and removal of the unused `is_claude_owned_worktree`; parts 13.2 and 13.3 remain open; part 13.4 remains conditional on a real serialization capture. |
| 14 | Open: repair two module paths and narrow the CSS prose; leave the CSS and the word “among” unchanged. |
| 15 | Open: narrow the rule to generated clock dates and timestamps; leave all thirteen inventoried historical or name-like dates unchanged. |
| 16 | Open except 16.9, which remains a nondefect. Correct the timing records through live updates and create the laptop update sibling. |
| 17 | Open: append corrections to the September 14 review update; never edit the finished turn records. |
| 18 | Open in the live speedup plan: keep only the provenance gap for 37.7 MB and repair the commit, suite, verification and alias prose. |
| 19 | Part 19.4 is already closed by current `main`; the receipt correction, redundant “own”, formatting, numbered exemptions and direct work names remain open. |
| 20 | Open: replace date-filtered repository census guidance with endpoint comparisons and direct push evidence. |

## 4. Proposed editorial wording for internal records and plans

### 4.1 Finding 2: the cloud-session record and prior remediation plan

In `doc/user-level-config-in-cloud-sessions.md`, replace only the clause beginning “and
`.claude/hooks/install-user-config.sh`,” preserving the opening paragraph's explanation of the two
tracked configuration directories, with:

> `.claude/hooks/install-user-config.sh`, wired in by `.claude/settings.json` as a `SessionStart`
> hook, installs three resources when their destinations are absent:
> `dot-Codex/user-wide-AGENTS.md` as `~/.codex/AGENTS.md`, and
> `dot-claude/user-wide-CLAUDE.md` plus `dot-claude/skills/hebrew-prose/` under `~/.claude/`.

Replace the failure sentence with:

> Two failures get their own banner—a needed tracked source being absent from the checkout, and any
> of the three destinations still missing after copying—and each tells the session to say so to
> Ben before starting work rather than to proceed as though the rules had been read.

Replace the inventory lead with:

> **The hook installs the three tracked resources the symmetric Claude setup needs and not the
> rest.**

Change “all of `dot-Codex/`” in that inventory to “the rest of `dot-Codex/`.”

Create `doc/PLAN-remediate-review-findings-2026-09-14-update.md` with this exact opening:

```text
# Updates to the plan to remediate the closed 2026-09-14 dual-agent review

State: open, first entry 2026-09-17. Every entry here corrects or supplements
`doc/PLAN-remediate-review-findings-2026-09-14.md`, whose substantive wording is left exactly as
written apart from the mechanically required paragraph join and update pointer.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit,
and a correction or later measurement goes in a sibling file named `<stem>-update.md`. This file
is that sibling. The paragraph join and update pointer are the only edits to the document this
file supplements; its substantive wording remains unchanged.
```

Use the dated entry heading `## 2026-09-17: corrections after the September 16 review`.
Mechanically join the base's State paragraph, without changing its text, then insert this exact
line as physical line 4:

```text
Updates and later status: [PLAN-remediate-review-findings-2026-09-14-update.md](PLAN-remediate-review-findings-2026-09-14-update.md).
```

The update records this correction:

> The plan's statement that `doc/user-level-config-in-cloud-sessions.md` was already corrected and
> needed no further edit was false. The document still needed the three-resource opening and the
> two stale two-resource passages corrected by the 2026-09-16 review remediation.

### 4.2 Finding 3: historical path and retired plan assertions

In `doc/review-findings-2026-09-10-update.md`, replace the `.Codex` item with:

> The historical capture at `a872790e` used `C:/Users/BenDe/.Codex/AGENTS.md`; that file and
> `dot-Codex/user-wide-AGENTS.md` had SHA-256
> `87C3EDDB6A9F001DAD5481D2162E0CE32D52FE7DB719C4AC651F030B5D4C393F`. The `.Codex` spelling
> is retained as historical evidence rather than as the current live Codex home.

For each of the four retired plan families, replace “live lines” with “lines at checkpoint
`<checkpoint>`” and replace the present-tense blob paragraph with this form:

> At checkpoint `<checkpoint>`, current `main` at
> `f079523148ae4892bec3b313dd43b3b627c1a2a9` was already merged. Before retirement, the finished
> plan's substantive bytes matched historical blob `<historical>`; its only later base edit was the
> authorized update pointer, producing blob `<pre-retirement>`. Its update sibling's final blob was
> `<update>`. Commit `2a051ba509901228fbd4d62d91b73765b94a39e4` retired the base and update
> together on 2026-09-17.

Use these values:

| Family | Checkpoint | Historical | Pre-retirement | Update |
| --- | --- | --- | --- | --- |
| September 8 remediation | `0a86cddefe2d1ed5151b91476ffadf08f3233fd1` | `bbd8c142bee6c1f1424cc33d08fa81bf37c7e1c3` | `0c84712d539bce20e6f0c01555ac73ebebad350d` | `37f48fbc1feadcf374cddf6ee6e9d72617fbc543` |
| Wikisource products | `cbe8b5a2a618c38a7b4fbe650013c0e6930cbd34` | `bc60b785903b1099a9bcbd9a6b9eb55bcd3103e6` | `1efcd386afb2dfa67c89112f8bac32305f3e928a` | `cb6b5f7e899338380b4b404704bfbf030f2952df` |
| Efficient downloads | `520f2df2648582651c0c58af0d00f29d45d301ff` | `85fd19f1e6a25de7f145d1e9d7678271cd9d5b94` | `adf3903960d593740c3e4210602fd943dcf209f7` | `d12529f6372cd5ee0db5d43bcd5bb8bb184cae99` |
| Worktree consolidation | `4816afe2cad093ebfc001b827805bdd593c54021` | `5b8da2ddc883016e4afa939b0a657a191f0cf5d7` | `5d4c4572a863f2be9d4370b9f35945546dd1fed4` | `d1a68033a6591bd3a717b990f8262fbbe08e4bf0` |

Before editing, verify every object ID from Git history. For worktree consolidation, say
“substantive wording” and “its later base edits were the authorized update pointer and the
mechanically necessary joining of its opening paragraph.”

Retain each entry's true remaining classification facts after the corrected historical paragraph:
the September 8 entry's relation to final remediation commit `9d1de074`, and the four update
siblings' descriptions of the display-fallback retirement, production refreshes, State
declaration and absence of scratch artifacts.

### 4.3 Finding 6: corrections to the finished September 14 remediation plan

Under the dated heading from section 4.1, after its finding-2 paragraph, use this exact numbered
text rather than asking the executor to reconstruct prose from facts:

> 1. The plan's repository remediation reached `71f96ca3` on 2026-09-16. The later GitHub issue
>    edit completed the plan's execution after that repository endpoint.
> 2. In section 1, the remediation task should read
>    `C:/Users/BenDe/.agents/skills/codex-worktree-tasks/SKILL.md`, including
>    `references/task-lifecycle.md` and `references/worktree-runtime.md`.
> 3. “39 headed entries” meant 38 level-2 entries plus one level-3 subheading, with 38
>    `Recorded by` lines. The finding-10 entry and the subheading had none, while finding 11.5 had
>    two.
> 4. The corrected anchors are `Correcting references before a tracked document is retired`,
>    `The live rule in \`leningrad/page-snips/README.md\` therefore remains unchanged`, and
>    `That reads \`MAM-simple/\`, so regenerate`.
> 5. The phrase “four actionable source gaps” was reused for a different set of four. The later
>    heading should read `### 7.3 Remaining source corrections`.
> 6. Throughout the plan, “remediation task” names the task, “remediation task's root agent” names
>    its root agent, and “the remediation task's final report” replaces the ambiguous
>    self-reference.
> 7. No new author annotation is owed for the entries in
>    `doc/review-findings-2026-09-10-update.md` that were rewritten beneath older `Recorded by`
>    lines.

### 4.4 Finding 16: timing records

In `doc/mega-timing-cloud-2026-09-14-update.md`, use:

> The virtual-environment advice in `doc/PLAN-mega-speedup.md` stands; the record itself gives no
> such advice. That advice was added to the plan after this update's first entry was written. The
> setup script was already making a virtual environment.

Replace the Python-version comparison with:

> **Python 3.13 runs the mega 7.7% faster than 3.11 on identical hardware**: the median of its two
> printed warm-run step-loop totals is 229.7 s, against 248.9 s on 3.11.

Make the corresponding figure in `doc/PLAN-mega-speedup.md` read “**229.7 s**, the median of the
two printed 3.13 step-loop totals, against 248.9 s on 3.11.” Name the comparison row “Ben
unpinned, run 1 of `doc/mega-timing-2026-09-11.md`.”

Append this numbered correction entry to the cloud update:

> ## 2026-09-17: corrections to the cloud record
>
> 1. The summary's 249.0 s is the sum of the 54 per-step medians in section 3, not the median of
>    the three run totals; the run-total median is 249.4 s from 271.3, 248.4 and 249.4 s.
> 2. A blank `Cloud / Ben` ratio has one of two causes: `diff-mpplus` and `gen-site` raised in the
>    comparison run, while `find-uxlc-accent-changes`, `tmpl-survey-toy`, `letter-small-job`,
>    `map-changes-to-book-of-job` and `ac-gen-index-flat-annotated` have a recorded Ben value of
>    0.0, so their ratios have a zero denominator.
> 3. In section 7, “Both” means the two output groups: the `vendoring-audit` outputs,
>    `doc/vendoring-inventory.md` and `out/vendoring_compare_out.txt`, and the `diff-mpplus`
>    outputs, `unpinned-latest.html` and `unpinned-latest.json`; all four listed files changed.
> 4. The dry-run explanation's three facts are: `ws-bot-proto` uses local file I/O; the live path
>    is `ws_bot_real`, which the mega does not name; and only `py/subcommands/ws_bot_real.py`
>    imports pywikibot.
> 5. The package-install defect is fixed by the amended Phase 2 step 3, as this update's first
>    entry records. The Surface Laptop record separately reports that `git add` refreshed cache
>    entries for four files in the first status and two in the second and staged no content, while
>    twelve files remained CRLF on disk. The record gives no disposition for that worktree-only
>    condition.

Create `doc/mega-timing-laptop-2026-09-14-update.md`, mechanically join the base's opening
paragraph if necessary, and insert this exact single physical line as the base's line 4:

```text
Updates and later status: [mega-timing-laptop-2026-09-14-update.md](mega-timing-laptop-2026-09-14-update.md).
```

Give the update this exact opening before the substantive entry:

```text
# Updates to the 2026-09-14 Surface Laptop mega timing record

State: open, first entry 2026-09-17. Every entry here supplements
`doc/mega-timing-laptop-2026-09-14.md`, whose substantive wording is left exactly as written apart
from the mechanically required paragraph join and update pointer.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit,
and a correction or later measurement goes in a sibling file named `<stem>-update.md`. This file
is that sibling. The paragraph join and update pointer are the only edits to the document this
file supplements; its substantive wording remains unchanged.
```

The substantive entry is:

> ## 2026-09-17: the unlabelled clock reads imply an offset of `-04:00`
>
> The clock read in the sentence beginning “The runs ran from 15:20 to 15:46” and the run table's
> `Started` column are unlabelled. The record's checkout associations and commit chronology imply
> an offset of `-04:00`: run 1 ended at 15:25:25.9 on the record's clock before `823be50b` was
> committed at 2026-09-14T15:26:31-04:00, and run 2 began at 15:29:35 after `8834ce4b` was
> committed at 2026-09-14T15:27:44-04:00. Those constraints bracket the clock's offset between
> approximately -04:01:05 and -03:58:09, making `-04:00` the only ordinary civil offset in the
> interval. The offset is inferred; the record names no zone.

Replace the final entry in `doc/mega-timing-2026-09-11-update.md` with:

> ## 2026-09-16: `accgram-run-prose` scans prose verses, not prose books
>
> In section 4 item 7, replace only `prose books` with `prose verses`; the remainder of the
> entry—“19,531 verse bodies, with the prose scanner and the PLY grammar, and writes
> `out/accgram/prose/`”—continues unchanged.

Finding 16.9 remains a nondefect and gets no remediation text.

### 4.5 Finding 17: correction of the earlier alternating records

Append this entry to `doc/review-findings-2026-09-14-update.md`:

> ## 2026-09-17: corrections to the alternating turn records
>
> Turn 3's statement that dropping the numbers was one of C3's two remedies is incorrect. C3
> offered refreshing the numbers or giving them an explicit checkpoint; dropping them was Turn
> 3's third proposal. Turn 4's phrase “the recorded remedy” can truthfully refer to Turn 3's
> proposal.
>
> The finished turn records also have these form and reproducibility limitations: finding leads
> state acceptance rather than fixed-or-unfixed disposition; `## Result` names no subject; Turn 3
> names five files and then says “the last three”; Turn 2 omitted re-establishing commands for its
> Black, Ruff and fifteen-repository-history figures; and Turn 4 says Black and Ruff were rerun
> directly without giving the commands. Turn 3 later supplied Black and Ruff commands and
> corrected the Black version to 26.5.1. The accurate prose counts need no numerical correction,
> and `counter-findings`, `new findings` and `counter-argument` describe different scopes rather
> than contradictory names.

### 4.6 Finding 18: the live mega-speedup plan

Replace the `37.7 MB` bullet's claim with:

> **MAM-simple's tree was recorded as shrinking from 107.7 MB to 37.7 MB on 2026-09-12, but the
> post-shrink figure is not reproducible from the preserved evidence.** The session attributed the
> figures to `du -sb` but preserved neither its raw output nor the exact working-tree state. At
> `bca64824`, the tracked files total 37,647,285 bytes, or 37.6 MB. Treat 37.7 MB as an unverified
> historical filesystem measurement unless preserved evidence re-establishes it.

Replace the fourteen-commit description with:

> Two are the dated record's speedups, `af1c404a` and `15c09692`. The other twelve are four
> MAM-simple commits (`d6a6764d`, `dcd2c1f6`, `3b1adf45`, `20f18020`), `6dbd27e7`, the three
> template-projection commits (`2239cbad`, `5cb06e25`, `1b7b97ef`), and four mpplus commits
> (`fa517040`, `8b2386b0`, `cde921bf`, `7fd381db`).

Add under `## Preconditions`:

> - **Baseline suite at `bca64824`:** the repository suite passed 997 tests with 5 skipped.
>   Re-run the suite at the execution baseline and record the new counts before relying on that
>   baseline.

Add to the executable-items section:

> Run `git diff --check` and the full suite before committing each completed executable item. Run
> the repository's final mega integration gate after the last executable change and explain every
> tracked generated diff.

After Phase 2's two filenames, insert:

> This phase calls `doc/mega-timing-cloud-2026-09-14.md` the cloud record and
> `doc/mega-timing-cloud-2026-09-14-update.md` the cloud update. The 2026-09-11 dated record is
> `doc/mega-timing-2026-09-11.md`.

Use “cloud record” and “cloud update” throughout that phase where bare “record” or “update” could
name the 2026-09-11 files. The compatibility-covered `CLAUDE.md` citations need no change.

### 4.7 Finding 19: the Metsudah receipt and small skill prose

Append to `doc/metsudah-vs-ctr-update.md`:

> ## 2026-09-17: the prose system is a property of verses, not books
>
> The base's phrase `prose-book tipḥas` should read `tipḥas in prose verses`; the prose and poetic
> systems classify verses, not books.

In `dot-claude/skills/hebrew-prose/SKILL.md`, replace “because their own introduction fixes the
meaning” with “because their introduction fixes the meaning.”

In `dot-claude/skills/hebrew-prose/references/core-rules.md`, replace the inline exemption sentence
with:

> Three exemptions:
>
> 1. A source's rule quoted in the source's terms, such as Breuer's “cancelling”.
> 2. Stress retraction (nesiga).
> 3. Anything explicitly declared a thought experiment.

Replace “which names either of the first two” in its vocabulary table with “which can name
Mikra'ot Gedolot ha-Keter or the Jerusalem Crown.” Add the missing blank lines before three
headings in `dot-claude/skills/github-issues/references/reading-and-writing.md`, two in
`dot-claude/skills/hebrew-prose/references/core-rules.md`, and eight in
`dot-claude/skills/mam-repository-topology/references/evacuated-repositories.md`. Wrap the eight
remeasured overlong prose lines across those three files and
`dot-claude/skills/github-issues/references/mam-basics-trackers.md` without changing their words.
Leave long table rows and the clone command alone. The backslash drive-path example no longer
exists on current `main`; preserve the intentional UNC syntax and do no 19.4 edit.

## 5. Proposed editorial wording for instructions and procedures

### 5.1 Finding 5: receipt-rule exception

In each of the three absolute pointer-only rules below, add “and a mechanically necessary joining
of a prose paragraph that begins on line 3 without changing its text” after “authorized line-4
update pointer,” adjusting singular or plural grammar only:

- `py/repo_util/check_repo_standards.py`, module-docstring anchor `The doc/ directory standard`, at
  the sentence beginning “A finished dated document is immutable while tracked”;
- `doc/PLAN-repo-maintenance-across-GitRepos.md`, anchor `Receipt immutability and retention are
  independent`; and
- `dot-claude/skills/mam-repository-topology/references/repository-maintenance.md`, anchor
  `Manual document retirement`.

Do not change ordinary “unchanged” or “as written” sentences: those do not claim byte identity.

### 5.2 Finding 7: topology setup summary

In `dot-claude/skills/mam-repository-topology/SKILL.md`, replace the stale exclusions-and-gists
sentence with:

> Apply every clause of `gitrepos_setup_rule`: clone only the folders in
> `all-repos.code-workspace`; do not consult exclusion lists, enumerate GitHub repositories, or
> clone the listed gists.

This wording summarizes `in/repo_maintenance_policy.json`; it does not predict that following the
complete policy would clone excluded gists.

### 5.3 Finding 8: moved and stale claims

Use the Phase 3 sentence from section 2.1 in all five current sites:

- `in/mam-ws-intro/README.md`;
- `dot-claude/skills/mam-repository-topology/references/evacuated-repositories.md`;
- `py/ac_paths.py`;
- `py/repo_scopes.py`; and
- `py/subcommands/download_wikisource_intro.py`.

In `doc/mam-normal-mark-order.md`, replace the present-tense repository claim with:

> When this section was restored on 2026-08-04, `codex-index-aleppo` and
> `codex-index-cam1753` carried near-verbatim copies of the deleted wording that pointed back at
> `uni_denorm.py` here; both repositories replaced those copies with evacuation breadcrumbs on
> 2026-09-04.

Do not say that all three assertions became false only when text moved. The source-hierarchy claim
remained true and only its `#1` form violated the non-issue-number rule; the Phase 3 and
current-repository claims need their separate corrections above.

### 5.4 Finding 9: current cross-references

Apply these literal current-reference repairs:

- In `doc/dual-agent-review.md`, replace “the prerequisite section above records the September 9
  measurement” with “`~/.codex/AGENTS.md` was 1,106 lines when remeasured on 2026-09-09,” and
  replace its remaining reference to `CLAUDE.md`'s “Five issue trackers” with
  `dot-claude/skills/github-issues/references/mam-basics-trackers.md`.
- In `py/github_issue_edit.py`, replace “the five trackers `CLAUDE.md`'s ‘Five issue trackers’
  registers” with “the five trackers recorded in
  `dot-claude/skills/github-issues/references/mam-basics-trackers.md`.”
- In `references/state-changes.md`, qualify the bare section reference as
  “`references/reading-and-writing.md`, section 3.”
- In `references/reading-and-writing.md`, qualify both section-5 references with
  `references/state-changes.md` and its `Closing, reopening, relabelling and reassigning` section
  or item 5, as the sentence requires. Replace the ambiguous attribution with “Ben, 2026-09-14,
  of the ‘Related: the mega speedup plan’ cross-link in MAM-basics #278:”.
- In `references/mam-basics-trackers.md`, use `wlc-utils#89` through `wlc-utils#93`,
  `uxlc/doc/clc-design.md`, `UXLC-utils#2` and `UXLC-utils#6`, and
  `holman/io/table_row_github_issues.json` at all three current sites.
- Move the paragraph beginning “The ../wlc-utils paths” verbatim from the Cambridge section to the
  wlc-utils section. This is editorial relocation, not new policy.

Preserve the historical references to retired plans. Do not modify cross-repository issue state.

### 5.5 Finding 11: restored provenance

Add to `AGENTS.md`'s product section:

> Ben decided on 2026-09-11 that `py/main_0_mega.py` writes nothing outside this repository;
> MAM-private runs its own near-Aleppo census.

Add to `holman/WORKFLOW.md`:

> Ben decided on 2026-09-12 that the two renamed JC3 zayin pages receive no compatibility stubs,
> so their old URLs may break; `in/holman_ketiv_qere_redirect_pages.json` records that decision.

In the Hebrew-prose skill's bidirectional runway rule, add:

> A section sign, a digit and a backtick are neutral rather than strong; none satisfies this
> rule.

Do not add list markers or quotation marks to the historical three-item enumeration without a new
decision.

In `dot-claude/skills/hebrew-prose/references/mam-basics.md`, use:

> Ben chose on 2026-08-10 to document the eight stale `../masorah-books/...` citations rather than
> edit them, and chose the same disposition on 2026-08-11 for the eight stale
> `../al-hatorah/...` citations.

In `dot-claude/skills/mam-repository-topology/references/evacuated-repositories.md`, replace the
loose cross-reference with:

> the dispositions Ben chose on 2026-08-10 for masorah-books and on 2026-08-11 for al-hatorah.

The three Ben attributions in `dot-claude/skills/hebrew-prose/references/core-rules.md`—“Just say
‘has,’” “Never ‘witness,’” and the preference for “consensus” over “eclectic”—had no decision date
in the pre-compaction source. Do not invent one. Introduce each as “Ben's undated rule, already
present when MAM-basics became the canonical configuration home on 2026-09-09.”

### 5.6 Finding 14: Holman workflow

In `holman/WORKFLOW.md`, change the two root-relative module paths to
`py/hkq_cmn/mam_suggestion_extract.py` and `py/hkq_cmn/mam_suggestion_dispositions.py`. Replace the
CSS rule with:

> Every authored CSS theme declares `color-scheme: light dark` on `:root`, and every theme custom
> property that stores a color uses a `light-dark(<light>, <dark>)` pair. Fixed badge foregrounds
> and backgrounds remain literal colors.

Leave “correspondence among Ben Denckla and Avi Kadish” unchanged. Leave both CSS files unchanged.

### 5.7 Finding 15: generated clock dates

Replace the `AGENTS.md` heading and paragraph with:

> ## Generated clock dates and timestamps shown on pages use New York time and say so
>
> A date or timestamp that repository code generates from a clock for display on a page or report
> is converted through `py/mb_cmn/new_york_time.py` and followed by “, New York time”. Historical
> decision dates, citations, quotations, release or revision dates, and date-like names—including
> release names, change ids and dated filenames—take no label. Stored timestamps retain full ISO
> 8601 offsets. Git dates retain their offset with `%cI` or `%ct`, never `%cs`; clock reads name
> their zone. `py/tests/test_explicit_time_zones.py` enforces the mechanical rule.

Replace the opening policy paragraph in `py/mb_cmn/new_york_time.py` with:

> Ben's decision, 2026-09-14: a date or timestamp that repository code generates from a clock for
> display on a page or report is the date or time in New York (`America/New_York`) and is followed
> by the label “, New York time”. Historical decision dates, citations, quotations, release or
> revision dates, and date-like names—including release names, change ids and dated filenames—take
> no label. A timestamp stored in data keeps its full ISO 8601 form with its offset.

Retitle that module docstring “Generated clock dates and timestamps shown on pages use New York
time and say so.” Preserve its evidence paragraph and implementation details.

Replace the opening decision paragraph in `py/tests/test_explicit_time_zones.py` with:

> Ben's decision of 2026-09-14, recorded in `py/mb_cmn/new_york_time.py`: a date or timestamp that
> repository code generates from a clock for display on a page or report uses New York time and
> says so. Historical decision dates, citations, quotations, release or revision dates, and
> date-like names are outside this generated-clock rule. Stored timestamps retain their ISO 8601
> offsets. An unzoned clock read or a Git date form outside the `%cI`, `%aI`, `%ct` and `%at`
> whitelist can write a date with no canonical zone evidence, so this lint rejects both in tracked
> Python under `py/`.

Change the test's final diagnostic clause to “generate displayed clock dates through
`py/mb_cmn/new_york_time.py`.” Do not change the thirteen inventoried visible dates.

### 5.8 Finding 20: repository census method

After the one-diff paragraph in `doc/periodic-review.md`, add:

> Establish each repository's review window from endpoint commits, not commit dates. For a cloned
> repository, carry forward the previous review's recorded end commit and compare
> `<previous-end>..<current-end>`. For a GitHub-only repository, record the previous and current
> default-branch commit IDs and compare those endpoints through the API. Repository-level
> `pushed_at` can establish that some push occurred; when the arrival of a particular commit
> matters, corroborate it with a direct ref update or PushEvent that names the before and after
> commits. Do not use `git log --since` or `commits?since=` as a completeness check: both filter by
> commit date and can miss an older commit pushed during the current review window.

## 6. Technical implementation

### 6.1 Finding 4: make the Git filename lint structural

Change `py/tests/test_tracked_filenames.py` rather than enumerating the 13 current misses:

1. resolve recognized imported and local Git-command constructors transitively, including a
   forwarding wrapper such as `_git_ok` calling `_git`;
2. retain literal subcommands and flags when repository, revision or path arguments are dynamic;
3. recognize `git grep -l`, `-L`, `--files-with-matches` and `--files-without-match` as
   filename-returning; and
4. continue requiring `-z` for every recognized filename-returning command.

Create `.novc/remeasure_filename_git_calls_2026_09_16.py` as an independent AST census and have it
record the examined HEAD, every filename-returning call, whether the lint sees it, and whether it
uses `-z`. At baseline `fbaae3d0` it must reproduce 27 current sites, 14 seen, 13 missed and 27
using `-z`; after implementation it must show that the lint sees all current sites. Run it with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/remeasure_filename_git_calls_2026_09_16.py
```

The count is review evidence, not a test constant.

### 6.2 Finding 12.2: gate only references to relocated `.novc` artifacts

In `py/repo_util/worktree_retirement.py`, derive the exact normalized source paths of the
particular `.novc` directories that the preflight will relocate. The search universe is the exact
retirement target, the primary checkout and every other registered linked worktree. Search each
checkout for tracked references to those exact relative or absolute paths; a generic `.novc`
policy, docstring or ignore pattern is not a citation. Deduplicate identical hits. Preserve the
existing explicit reviewed flag and nonempty overall note, and retain the full structured hit
list, note and fingerprint in the preflight and every sidecar.

Use this CLI help text in `py/main_repo_util.py`:

> affirm that every printed tracked reference to a `.novc` path being relocated has a durable
> disposition

In `doc/PLAN-repo-maintenance-across-GitRepos.md`, use “Read the JSON and settle every tracked
reference to a `.novc` path that this retirement will relocate” and the heading “Tracked
references to relocated `.novc` paths require review.” Apply equivalent current wording in the
topology skill's maintenance reference.

Extend `py/repo_util/worktree_retirement_simulation_test.py` with a differential fixture: generic
`.novc` policy lines do not gate, while a tracked reference to the exact target artifact gates and
survives in the preflight and sidecar with the review note. Do not weaken the current reparse-point
guards; finding 12.1 needs no code change.

### 6.3 Finding 13.1: owner-scope diagnostic

In `py/main_repo_util.py`, replace the refusal text with:

> `--session-ended` names no linked worktree in the selected owner scope of the selected repos:

Remove the now-unused `is_claude_owned_worktree` from
`py/repo_util/git_worktree_cleanup.py`. Keep the used, owner-neutral `is_linked_worktree`.

### 6.4 Finding 13.2: Git date diagnostics describe the whitelist

In `py/tests/test_explicit_time_zones.py`, replace the blanket `--date=` diagnostic with:

> `<value>` selects a noncanonical Git date display mode; use `%cI`, `%aI`, `%ct` or `%at` without
> `--date=`.

Replace the rejected-placeholder explanation with:

> `<value>` uses Git date placeholders outside the allowed `%cI`, `%aI`, `%ct` and `%at` set.

Do not claim that every rejected mode or placeholder drops the offset.

### 6.5 Finding 13.3: custom MAM-simple directory diagnostic

Keep template and versification dispatch closed. Extend
`py/mb_cmn/mam_simple_book_group.resolve_book_group_path` with an explicit custom-directory
branch. A standard directory continues to require and name its recognized `vtrad`; a supplied
`requested_dir` does not receive a dummy tradition and raises:

> No MAM-simple `<fmt>` book group in requested directory `<path>`; tried `<paths>`

Change `py/accgram/mam_simple_verse.py` to use that branch without passing the false `bhs` label.
Add a differential test whose independent test-local oracle constructs candidate paths directly
from the format suffix, requested directory, standard tradition directories, ordered stems and
file presence. Compare the resolver with that oracle across every recognized format and
versification, standard fallback and no-fallback modes, multiple stem orders, and present or
absent candidates. The custom-directory error must name the custom directory and never say
`for bhs`.

### 6.6 Finding 13.4: conditional hook stdin hardening

The official hook contract establishes one JSON object on stdin but does not establish whether
non-ASCII text is escaped. Establish the runtime behavior without changing live configuration:

1. Create the isolated scratch Git repository
   `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16/.novc/hook-serialization-é`.
   Its project-local `.codex/hooks.json` contains only a synchronous `SessionStart` command hook
   with matcher `startup`; `commandWindows` invokes the shared Python interpreter and scratch
   `capture_hook_stdin.py` by absolute path. The reviewed script reads `sys.stdin.buffer` and
   writes the bytes unchanged to `session-start-stdin.bin` beside itself.

   ```powershell
   git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16/.novc/hook-serialization-é init C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16/.novc/hook-serialization-é
   ```

   Use this hook structure after substituting no paths:

   ```json
   {
     "hooks": {
       "SessionStart": [{
         "matcher": "startup",
         "hooks": [{
           "type": "command",
           "commandWindows": "C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16/.novc/hook-serialization-é/capture_hook_stdin.py"
         }]
       }]
     }
   }
   ```

2. Inspect those two scratch files. Also read and record a hash of
   `C:/Users/BenDe/.codex/hooks.json` and
   `C:/Users/BenDe/.codex/hooks/check_project_doc_budget.py`; require the user hook to name only
   that expected `SessionStart` command. `--ignore-user-config` omits
   `C:/Users/BenDe/.codex/config.toml`, but hook sources are cumulative and the user-level
   `hooks.json` still runs. That is intentional: the live hook is the target, while the inspected
   project hook captures the same event's raw stdin.

   Write and review a scratch `run_codex_hook_probe.py` that invokes `codex exec` with a fixed
   argument array and captures stdout and stderr as bytes in separate files. Its first,
   no-bypass invocation uses `--ephemeral`, `--ignore-user-config`, `--skip-git-repo-check`, the
   scratch repository as `-C`, a separate `codex-inventory-last-message.txt`, and the prompt
   `Reply only INVENTORY and do not call tools.` The project capture hook is still untrusted, so
   that first invocation must skip it rather than change persisted trust. Inspect the captured
   startup inventory of every configured user, project, plugin and managed hook source. The only
   permitted sources are the already-inspected user hook and the exact project capture hook
   above; no plugin or managed hook is permitted. If the captured diagnostics do not provide a
   complete source inventory, or report any additional source or any hook failure, retain the
   output, record the experiment as inconclusive and do not run the bypass invocation.

   Record the paths and SHA-256 hashes of both permitted hook definitions and both command scripts,
   then recheck all four hashes immediately before the experiment. Only after that complete
   inventory and unchanged-hash check, run the same reviewed wrapper in its fixed capture mode,
   adding `--dangerously-bypass-hook-trust` to the argument array and using the output path and
   prompt below. The flag deliberately applies to both fully inspected non-managed hooks; it
   creates no persisted hook-trust decision. If startup nevertheless reports a source not in the
   recorded inventory or a hook failure, retain both byte streams, treat the experiment as invalid
   and stop without interpreting the capture:

   ```powershell
   codex exec --ephemeral --ignore-user-config --dangerously-bypass-hook-trust --skip-git-repo-check -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16/.novc/hook-serialization-é --output-last-message C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16/.novc/hook-serialization-é/codex-last-message.txt "Reply only OK and do not call tools."
   ```

3. Run scratch `classify_hook_serialization.py`, which requires the captured JSON's `cwd` to name
   the non-ASCII directory and reports whether the raw bytes contain literal UTF-8 for `é` or an
   ASCII `\u00e9` escape. Retain the config, scripts, raw capture, Codex output and classification
   together under that `.novc` directory through task cleanup. The ephemeral session leaves no
   saved task, and no live configuration file is created or changed.

If the capture contains literal UTF-8, configure `sys.stdin` with UTF-8 at the start of `main()` in
`dot-Codex/hooks/check_project_doc_budget.py`, before `_read_hook_input()` calls
`json.load(sys.stdin)`. If the capture is ASCII-escaped, record that the conditional defect does
not reproduce and make no hook change. In either case, run a scratch subprocess harness that
passes the captured bytes to the tracked hook and verifies its exit status and parsed result.

## 7. Execution waves and commit boundaries

### 7.1 Wave 1: reader-facing README and Holman workflow wording

Implement finding 1 and the reader-facing part of finding 8 from section 2.1, plus finding 14's
Holman workflow corrections. Verify the two crop-rule occurrences, the CSS custom-property and
fixed-badge inventory, and the absence of tracked output changes. Commit this documentation wave
alone.

### 7.2 Wave 2: receipt and live-plan corrections

Implement findings 2, 3, 6, 16, 17, 18 and the finding-19 receipt correction from section 4. Add
only the two authorized base pointers and their mechanically necessary paragraph joins: the
September 14 remediation plan's pointer and the laptop timing record's pointer.
Verify every historical Git object before writing finding 3's final full hashes. Commit the
receipt and live-plan wave after the receipt-link test and `git diff --check`.

### 7.3 Wave 3: instructions, skills and review procedure

Implement findings 5, 7 to 9, 11, 15 and 20 from section 5. Apply finding 19's skill formatting in
this wave. Run the repository-standards and prose-convention checks. Commit canonical skill and
instruction changes together; deployment waits for pushed `main`.

### 7.4 Wave 4: filename lint

Implement finding 4 and the independent census. Run the targeted lint and the full suite because
this wave changes test infrastructure. Commit only when the structural lint covers every current
site without a pinned count.

### 7.5 Wave 5: worktree-retirement citation gate

Implement finding 12.2 and its differential operational simulation. Do not run a real retirement.
Commit the engine, CLI, simulation and matched documentation together.

### 7.6 Wave 6: remaining diagnostics

Implement findings 13.1 to 13.3, and implement 13.4 only if the serialization capture reproduces
the defect. Run the matched tests, the full suite after the final executable change, and the final
mega after merging current `main` as section 8 requires. No tracked generated diff is expected.

Finding 10, finding 12.1, finding 16.9 and finding 19.4 get no implementation commit. Record their
already-resolved or nondefect dispositions in the final review update rather than touching code.

## 8. Verification and commit discipline

Before every commit, recheck `HEAD` and task-owned status, inspect the complete staged diff, run
formatting matched to changed Python files, and run:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 diff --cached --check
```

Run Black at defaults on every changed Python file through the shared interpreter. The targeted
checks are:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_tracked_filenames.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_receipt_update_links.py py/tests/test_explicit_time_zones.py py/tests/test_prose_conventions.py py/tests/test_post_stress_meteg_plain_word.py py/tests/test_worktree_retirement_policy.py py/tests/test_mam_simple_dualcant_loader.py py/tests/test_mega_coverage.py
```

Run the operational retirement simulation through the supported test entry point:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/repo_util/worktree_retirement_simulation_test.py -q -p no:cacheprovider
```

Run repository standards after documentation, receipt and instruction changes:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --check-repo-standards --repos C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16
```

After the last source or test change, run the full suite from the worktree root:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
```

Documentation-only commits after that result do not expire it. Immediately before the final
integration gate, merge then-current `main` into the review branch again, resolve conflicts here,
and rerun affected checks. Then run the mandatory mega:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
```

Read every tracked generated diff. The expected result is no generated diff. Any generated change
is a finding that must be explained and committed on the branch before integration; it is not
permission to accept an unrelated product change.

After each coherent commit, push the review branch as a backup:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 push origin dual-agent-review-2026-09-16
```

## 9. Final disposition record

After all substantive remediation is verified, assemble the facts for one completion entry in
`doc/dual-agent-review-2026-09-16-turn-01-claude-update.md`, but keep this plan `State: live` and
do not write the entry yet. The entry will lead each numbered finding with its final disposition,
name the implementing commit or the current-main commit that had already fixed it, and record the
targeted, suite and mega results. Do not modify the finished turn-01 base or any numbered turn.
Section 10 writes the entry only after the substantive head has been integrated, pushed and
deployed, so every claim in the closing record is already true when committed.

## 10. Final integration, deployment and cleanup

The remediation task retains integration responsibility. After the final merged-main mega is
clean, require a clean primary clone at `C:/Users/BenDe/GitRepos/MAM-basics`, verify that primary
`main` is an ancestor of the substantive review head, and fast-forward primary `main` with
`--ff-only`. If primary `main` moved, return to this worktree, merge it, rerun affected checks and
the mega, then retry. Push `main` only after local names resolve to the same verified commit.

Run these commands separately from the primary clone:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics status --short --branch
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics merge-base --is-ancestor main dual-agent-review-2026-09-16
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics merge --ff-only dual-agent-review-2026-09-16
```

Require the two printed object IDs to match before pushing:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics rev-parse main dual-agent-review-2026-09-16
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics push origin main
```

Only after canonical configuration is on pushed `origin/main`, deploy from the primary clone:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config
```

Then verify the deployed copies read-only:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check
```

Deployment changes live user configuration outside Git and must be reported separately from
repository product reach.

Only after the substantive head is integrated, pushed and deployed, return to the shared worktree
and write the completion entry prepared in section 9. In that same closing documentation commit,
replace this plan's opening State with:

```text
State: executed <completion-date>. The substantive remediation, required repository verification, integration of the substantive branch head, and user-configuration deployment are complete. This closing record commit requires only its documentation fast-forward and push.
```

Use the actual New York completion date, not the placeholder. Stage only this plan and
`doc/dual-agent-review-2026-09-16-turn-01-claude-update.md`, run `git diff --cached --check`, commit
and back up the review branch. This documentation-only commit does not expire the suite or mega
and does not require another configuration deployment because it changes no canonical
configuration file.

Fast-forward the primary clone to that closing record commit, verify equality again, and push
`main` a second time:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 add doc/PLAN-remediate-review-findings-2026-09-16.md doc/dual-agent-review-2026-09-16-turn-01-claude-update.md
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 diff --cached --check
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 commit -m "Close September 16 review remediation"
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16 push origin dual-agent-review-2026-09-16
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics merge --ff-only dual-agent-review-2026-09-16
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics rev-parse main dual-agent-review-2026-09-16
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics push origin main
```

Run the read-only user-configuration check once more after the closing push. A push of `main`
triggers the published Pages workflow even though this plan expects no generated-page diff. Record
the final pushed `main` SHA, list the workflow runs, select the row whose `headSha` exactly equals
that SHA, and require `gh run watch` to exit zero with conclusion `success`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics rev-parse main
```

```powershell
gh run list --repo bdenckla/MAM-basics --workflow pages.yml --branch main --limit 20 --json databaseId,headSha,status,conclusion
```

```powershell
gh run watch <database-id-for-the-final-pushed-main-sha> --repo bdenckla/MAM-basics --exit-status
```

Do not unlock or delete this Claude-managed worktree during remediation or integration. After
integration and deployment are verified, a separate cleanup-only Claude task inventories the
shared worktree's `.novc/`, preserves or promotes evidence with lasting value, explicitly disposes
of the rest, unlocks the worktree, and removes it under the Claude worktree procedure. Do not use
Codex worktree-retirement tooling on this `.claude/worktrees/...` checkout.

## 11. Completion report

The final report names:

- each remediation commit, the integrated and pushed `main` commit, and the backup branch head;
- every already-resolved and nondefect disposition;
- targeted-test, full-suite, repository-standards and mega results;
- whether the conditional hook defect reproduced and what evidence established the result;
- whether the mega produced any tracked diff and the disposition of every diff;
- user-configuration deployment and check results;
- the Pages workflow result; and
- the separate cleanup task that remains for `.novc/`, the locked shared worktree and the merged
  branch.
