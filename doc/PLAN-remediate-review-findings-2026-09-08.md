# Plan: remediate the reconciled 2026-09-08 public-repository review

State: live 2026-09-09; planning complete, awaiting Ben's step-5 approval; no remediation started.

This is step 4 of [PLAN-close-out-review-2026-09-08.md](PLAN-close-out-review-2026-09-08.md).
Ben's decisions D1-D11 were recorded on 2026-09-09. Step 5 approves the waves and the concrete
editorial proposals below; step 6 executes one wave per fresh Codex task. Approval of a wave
does not silently approve an editorial item labelled E or N. D7 applies to all remediation,
with the MAS pages as an example. Record each editorial item's approval, rejection, or amended
wording before applying it. D2, D5, D6, and D8 are already decided and
do not need another decision.

The plan retains the review's historical findings and adds dated corrections. In particular,
the plan does not reinstate the MAS prose Ben reverted on 2026-09-08. A finding called
confirmed by a reviewer establishes an observation, not approval of a remedy.

Ben's presentation preference, 2026-09-09: present proposals first as high-risk changes to
public-facing documents, then high-risk changes to public-facing data, then a summary by
type of the remaining, lower-risk changes. README and other reader-facing Markdown belong
with the documents; ordinary `doc/` records do not. The E/N labels and implementation waves
below remain references and execution structure, not risk categories. The standing rule is
recorded in [dual-agent-review.md](dual-agent-review.md), under "Present remediation by
public-facing risk". This preference records no additional approval of the proposed work.

## Checkout, sources, and measured starting state

Run from **C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08**, on
**codex-review-2026-09-08**. Every repository-relative path below belongs to that worktree.
The primary clone is **C:/Users/BenDe/GitRepos/MAM-basics**. Its interpreter is shared by
absolute path; no `.venv` is created, copied, linked, or junctioned into the worktree.

Before reading or editing, verify the checkout, branch, HEAD, status, and ancestry of the
required commit supplied by the preceding task. Run each command separately:

```powershell
git -C C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08 rev-parse --show-toplevel
```

```powershell
git -C C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08 branch --show-current
```

```powershell
git -C C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08 rev-parse HEAD
```

```powershell
git -C C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08 status --porcelain
```

```powershell
git -C C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08 merge-base --is-ancestor <required-commit> HEAD
```

Inspect a mismatch before proceeding. With a clean tree, merge `main` into the branch before
reading further or editing; resolve conflicts here and verify the merged tree here.

```powershell
git -C C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08 merge --no-edit main
```

An ownership check in the Windows sandbox may require the command-local option
`-c safe.directory=C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`. Do not change
global Git configuration. Writing Git's common metadata or running the primary interpreter
may require the harness's escalation mechanism; neither changes the development location.

Read these instructions before the first edit:

1. `C:/Users/BenDe/.codex/AGENTS.md` and the worktree's `CLAUDE.md`; there is no repository
   `AGENTS.md` at the measured starting commit.
2. `C:/Users/BenDe/.agents/skills/hebrew-prose/SKILL.md` and all four files under its
   `references/`: `terminology.md`, `rendered-prose.md`, `sources-and-corpora.md`, and
   `verifying.md`. Preserve the nine MAS pages' plain-"word" exception.
3. The close-out plan in full, including its task handoff and single final integration rules;
   `doc/dual-agent-review.md`; and this plan in full.
4. Before changing the shared skill, the worktree's `dot-claude/README.md`, section
   "Shared-skill deployment to Claude and Codex". The live Claude copy, tracked worktree copy,
   and live Codex copy must all agree after D2 is implemented.

Sources in order of authority are the reconciliation table in
`doc/review-findings-2026-09-08.md` at `5636d38a`, amended by the rebuttal at `da4e40a5`, the
counter-rebuttal at `ad5d9f43`, turn 5 at `2b365153` with its addendum at `7c4416cd`, the
step-1 acknowledgment at `8c49cdd2`, and Ben's subsequent decisions in the close-out plan.
The original Claude argument is at `e56ae06a`; the Codex counter-argument is
`doc/codex-review-findings-2026-09-08.md` at `5636d38a`. Read the accepting turns as well as
the original finding. The review exchange is closed. Claude's skill-reading time remains
unknown by Ben's decision; it has no remaining effect on a finding's disposition.

Planning began clean at required commit `83b470da1846fc1c739fcca48762d01627fa354e`.
The required back-merge produced `dd86c96fd29c4b345ae37ba7252ffe72944cbef3`, bringing in
`222883dd`'s cloud Graphviz handling. Measurements below are at `dd86c96f`, before adding
this plan. Re-measure at each wave's merged starting HEAD; a difference requires an
explanation and an updated scope, not an attempt to restore these numbers.

| Measurement | Result at `dd86c96f` | Re-establishment |
|---|---|---|
| Canonical suite | 987 passed, 5 skipped, 65 subtests passed in 126.54 seconds; tracked tree clean after the run | Suite command below, with `REPOS_ROOT` set |
| Earlier required baseline | 983 passed, 5 skipped, 65 subtests at `becc6f00`; the increase is the prose-mark-order test and three Graphviz pin tests added later | `git diff becc6f00 dd86c96f -- py/tests`; inspect both suite records |
| Deploy-root HTML / MAS HTML | 11 / 9 | V1 below |
| Direct `doc/PLAN-*.md` files | 15; only the merge plan lacks `State:` at line 3 | V1; this new plan makes 16, before any later work |
| Whitespace findings | 189 blank final lines and 21 trailing-space lines, in 193 distinct files | V2; the full offending set, not a clean-tree diff check |
| Holman Hebrew cells without RTL | Suppressed page: 49, comprising 32 comparison-name and 17 comparison-symbol-value cells; active page: 1 | V3 |
| `MAM-with-doc/` retained files | `.gitattributes`, `.gitignore`, `LICENSE.md`, `README.md`; no test | `git ls-files MAM-with-doc` |
| Manuscript crops in `gh-pages/img/` | Six; the named source and rights-holder gaps persist | `git ls-files gh-pages/img`; finding 9.2 and proposal P2 |
| Committed vendoring report | 25 `eol-only` rows; `paths.py` says last synchronized 2026-09-07 though its copy last changed at `9cf48863` on 2026-09-08 | V4 |
| September 7 remediation checklists | Wave 1 has 7 unchecked boxes; Wave 2 has 12, despite completed execution records | `rg -n -F -- '- [ ]' doc/PLAN-remediate-review-findings-2026-09-07.md` |
| Wave 5 Python path count | 26: 25 under `py/`, plus the vendored `MAM-simple/py-examples/mb_cmn/paths.py` | `git diff-tree --no-commit-id --name-only -r 9cf48863 -- '*.py'` |

The planning task ran no product, survey, or page generator. Complete artifact synchronization
is therefore **not** asserted as a planning baseline. The first approved task for each generator
records a before-edit regeneration and its diff. Known baseline changes, especially the
vendoring audit, must be named separately from remediation changes.

The public Phonetic MAM pages, if needed to repeat finding 8.1, are under
`C:/Users/BenDe/GitRepos/phonetic-hbo`, historically at `7322b665`; record that clone's actual
HEAD before use. This plan needs no private scholarly sources, private history, or private
survey regeneration. Render MAS pages from the tracked JSON with `--trust-surveys`.
Do not run a mega, refresh Wikisource, or write MAM-OSIS as a side effect of these waves.

Another task may be live in the primary clone. That does not block this worktree. Keep one
writer in this exact worktree; compare HEAD and status immediately before staging. The final
integration requires both checkout trees clean and uses only a fast-forward in the primary
clone. Intermediate task archival does not integrate or push.

## Decisions already taken and proposals awaiting step 5

Ben's decisions, 2026-09-09:

1. **D2:** replace the skill opening's restrictive sentence with exactly: `Plain ‘word’
   survives for an ordinary English word, inside quoted or translated source material, and
   wherever the context already settles which sense is meant (references/terminology.md).`
   Deploy and compare all three homes.
2. **D3:** append a dated correction addendum to the September 8 argument, citing the accepting
   turns. Preserve the original findings and the reconciliation table.
3. **D4:** record that Wave 4's command was not recorded and the cause of its missing subtest
   line is unknown. Wave 6 reported 65 subtests with the same 981 passing-test count. Add a
   dated correction to the separate claim that the suite "no longer prints a subtest line".
4. **D5:** retain the MAS multiplicity guards, page wording, and existing JSON fields. Do not
   add a MAS-multiplicity count; finding 13.2 is a design note, not a broken check.
5. **D6:** in the `aleppo/aleppo-wiki/` content description, change `hand corrections` to
   `Ben Denckla's hand corrections`. Do not sweep the other hand-transcription wording.
6. **D7:** in every remediation proposal, distinguish reproducible defects from editorial
   choices and obtain approval of concrete terminology, organization, interpretation, and
   attribution changes. The MAS pages are the worked example, not the scope boundary.
7. **D8:** update the site-index test's dated comment from 34 to the measured 35 anchors;
   retain the floor of 25 and the test's behavior.

D1, D7's procedure record, D9, D10, and D11 were implemented in `2cddb893` and recorded in
`83b470da`. Finding 10 and Codex C5 are settled; do not run step 3 again. D10's historical
description in `check_repo_standards.py` may receive a dated pointer to the procedure's new
standard, without changing the completed review documents or introducing a new review test.

Approval of the waves also decides these bounded proposals:

| Proposal | Recommended disposition and limit |
|---|---|
| P1 — vendoring audit, finding 12 | Keep comparison of working-tree bytes. Regenerate the report in this LF worktree after source/copy commits, so synchronization dates describe committed copies. Record that EOL-only differences can recur in another checkout. Do not change the comparator to read blobs or rewrite the primary checkout's files. |
| P2 — crop provenance, finding 9.2 | Record the source and rights-holder fields as unrecorded where the public record supplies no answer. List each crop individually in a short provenance note linked from `DATA-LICENSES.md`; retain the existing no-grant statement. This closes the missing inventory, while source identification remains explicitly deferred. Do not invent source URLs, folios, rights holders, or license conclusions. |
| P3 — plan names and latent limits, findings 7 and 13 | Keep both historical plan filenames. Add the merge plan's executed State and dated corrections; retain the live silluq plan's current State and add only the still-needed historical baseline/decision notes. Retain functioning overlap, multiplicity, fusion, and conjunctive-stress checks. Record the unverified Aramaic/edition assertions and valid empty XML targets as limits, without new example tests or a new scholarly investigation. |

If Ben rejects P1, P2, or P3, record the rejection and revised scope before the affected wave.
An approved deferral remains labelled deferred in the final disposition; it is never called
fixed. No issue comment, issue state change, external scholarly inquiry, or cleanup is
authorized merely by approval of this plan.

## Exact MAS editorial proposals

Each E item requires an explicit step-5 disposition. These are the complete proposals, not
permission for a grammar pass. Apply the approved wording in the authored source and regenerate;
do not edit generated MAS HTML directly. Plain `word`, BHS attribution, UXLC/WLC edition names,
local ITM/CoS glosses, the phi-1 callout, and Ben's restored first-person wording remain intact.
All E items belong to Wave 3.

| ID / finding | File and searchable anchor; before | Proposed after |
|---|---|---|
| E1 / 8.2 | `doc/post-stress-meteg-method.md`, `Type 3`: `Type 3 is a closed, final, tsere-vowelled syllable after a retracted stress.` | `The Fit-for-MAS implementation requires a closed, final, tsere-voweled syllable for type 3; its common criteria require penultimate stress with a conjunctive accent.` This describes the implementation and makes no new claim about a source's retraction analysis. |
| E2 / 15.1 | The 15 visible unwrapped mark-name occurrences in `gh-pages/post-stress-meteg.html`, `post-stress-meteg-methods.html`, and `post-stress-meteg-2chr-8-11.html`, generated by `py/author_site/post_stress_meteg.py`: `meteg mark`, `meteg marks`, and `meteg/merkha marks` | Use the existing `romanized` spans for `meteg` and `merkha`, keeping every visible character and space unchanged. For example, `meteg marks` becomes `<span class="romanized">meteg</span> marks`; coalesce the slash-joined names into `<span class="romanized">meteg/merkha</span> marks`, so the slash is italicized too. Do not put markup in titles or attributes. |
| E3 / 15.2 | Main page's Fit-for-MAS criteria: a three-item `<ul>`; the not-fit page calls the criteria 1, 2, and 3 | Change that list to `<ol>`, with its entries and order unchanged. Change no other list. |
| E4 / 13.5 | `py/accgram/post_stress_meteg.py`, `THE TWO SIDES ARE CHECKED`: `A chanted word where they disagree is recorded as a MISMATCH and left out of every count, rather than being classified against a syllable division the two sides do not share.` | `A chanted word where they disagree is recorded as a MISMATCH and left out of the provisional counts. At the end, _problems returns the collected problems and build_survey raises if any remain, so no survey with a mismatch is emitted.` No exception behavior changes. |
| E5 / 15.4 | Same module, anchor `A last entry`: `A last entry need not be the one with sof pasuq -- one strand's chanted verse can end at the numbered verse's boundary and the other can run on past it.` Same module, anchor `THE PAGE SHOWS`: `two annotations MAM does not write` | First sentence: `A last entry need not have sof pasuq: the numbered-verse boundary need not end both chanted verses.` Second fragment: `two annotations absent from MAM`. Preserve the following descriptions of the annotations. |
| E6 / 14.1 | `CLAUDE.md`, `before any other sentence uses either`; `py/author_site/post_stress_meteg.py`, same phrase; dated note beside the merge plan's same claim | State: `The main page defines both "word" and "atom" in its second expository paragraph; the opening sentence already uses "word".` Join that sentence to each surrounding paragraph without changing the exception. The lint docstring's existing paragraph description is accurate and stays. Do not rewrite the immutable commit or issue #265. |
| E7 / 15.5 | `doc/post-stress-meteg-method.md`, later `Another meteg in the first chanted word does not exclude the candidate from the Fit-for-MAS table.` | Delete this duplicate sentence; retain the earlier `Another meteg in the first chanted word does not disqualify the candidate.` The JSON category spelling stays unchanged; E1 changes the documentation spelling only. |
| E8 / 9.3 | Methods page: the Aleppo 1 Kings 7:37 crop has the claim in its alt text but no visible explanatory sentence | Add below that crop: `The Aleppo Codex has a meteg after the silluq in 1 Kgs. 7:37.` Use the existing romanized helpers for the mark names. This repeats the existing alt-text observation; it does not adjudicate a new reading or modify the MAM paragraph. |

Ben's step-5 decision, 2026-09-09: amend E2 to coalesce the spans around slash-joined mark
names, including the slash in the italic span. Ben's reason: "I think it looks better to
coalesce such spans, since that makes the slash be in italics as well." This settles the
slash formatting in E2; the remaining proposal and wave approvals are still pending.

## Exact editorial proposals outside the MAS text

These items apply D7's general scope. Each N item requires an explicit disposition just as
each E item does. The dated factual corrections in the crosswalk, including corrected counts
and implementation attribution, are authorized by approval of their wave; they must still
say exactly which earlier assertion they correct and what evidence establishes the correction.
No additional stylistic rewrite is implied by that authorization.

| ID / finding / wave | File and before | Proposed after |
|---|---|---|
| N1 / 5.3 / W1 | `cam1753/doc/reading-mam-simple.md`: `and this repo's was deleted` | `and codex-index-cam1753's copy was deleted` |
| N2 / 5.4a / W1 | `py/tests/test_sibling_reach.py`: `says "Old git revision (in ../MAM-parsed repo)"` | `formerly said "Old git revision (in ../MAM-parsed repo)"` |
| N3 / 5.4b / W4 | `py/vendoring/gen_inventory.py` and generated inventory: `These Python files live outside MAM-basics and are intentionally maintained in their destination repos.` | `These Python files are intentionally maintained at the listed paths rather than copied from the vendoring source.` |
| N4 / 5.5 / W1 | `doc/dual-agent-review.md`: `that guard's own` | `that guard's` |
| N5 / 5.5 / W1 | `CLAUDE.md` root-page label: `the introduction's own root page` | `the introduction's root page` |
| N6 / 5.5 / W1 | `DATA-LICENSES.md`, `in/scan-pages/` row: `MAM-basics' own work, so GPL-3.0.` | `MAM-basics' work, so GPL-3.0.` No grant changes. |
| N7 / 15.4 / W1 | `py/author_site/site_data.py`: `THE MISC TITLES ARE THE PAGES' OWN.` | `THE MISC TITLES MATCH THE PAGES' TITLES.` |
| N8 / 16 / W1 | Merge plan's `Seven commits past c73a2ad3` run-on and `converted one to the other` | Keep the original record. Add the dated numbered list below. Add beside the quote sentence: `The recorded problem was a change between straight and curly quotation marks; the record does not establish the direction.` |
| N9 / 6.8 / W1 | Site-index test comment's `after the 2026-09-07 index additions` | `after the 2026-09-08 index additions`. D8 has already approved the separate 34-to-35 change; this date clarification requires no test behavior change. |

N8's proposed dated list says `The seven non-merge commits from c73a2ad3 to a3e3f6eb were:`

1. `97a1b46f`: type-2 Fit-for-MAS criteria.
2. `39133db0`: next-conjunctive page.
3. `fe4e602f`: grammar and spelling.
4. `c5b170ad`: Methods structural subtype.
5. `d7049855`: derived references and Ben's follow-ups.
6. `0afbae68`: Fit-for-MAS predictor paragraph.
7. `a3e3f6eb`: plain-word lint.

## Finding-by-finding work and unchanged scope

The line column below records the original location **at `38a606e2`**, not a promise about
current line numbers. Anchors are the strings or identifiers to search at the executing HEAD.
For a row labelled `R`, re-establish the text with `rg -n -F` using that row's anchor and file,
then read the surrounding paragraph or function. For example:

```powershell
rg -n -F 'retained source-hygiene test' DATA-LICENSES.md
```

To check the original line and its historical context, use the same path at the pinned commit:

```powershell
git show 38a606e2:DATA-LICENSES.md
```

`H` means read the named accepting turn or commit with `git show <commit> -- <path>`; the
later acceptance determines the disposition. `V1`-`V5` are the concrete verification recipes
below. Do not rely on an ignored script from a previous task being present. A historical
record's later correction is a dated note beside that record, never a rewritten finding.

| Finding | File, original line, and searchable anchor | Re-establish | Wave and action; what stays unchanged |
|---|---|---|---|
| 1 | Methods HTML 72-77, `We ignore`; survey 2242, `post-silluq`; older MAS plan 1145, `MAM HAS NO POST-SILLUQ METEG` | R; H `3b0225e0`, `becc6f00` | W1 dated disposition: settled by Ben. Qualify the older plan's overclaim as the research's chosen interpretation. No classifier, census, or approved page change. The separate silluq-template work is not executed. |
| 2 | September 7 review 908, `Sol-1`; remediation plan 448-451, `git diff --check`; `py/mb_misc/write_utils.py`, `_write_verse_un` | R; V2; `git diff --name-only 4afe3ebc^ 4afe3ebc` | W1 correct the old fixed claim; W2 repair and regenerate all 210 findings. Preserve internal spaces, verse separators, CSV structure, corpus text, and HTML content. The MAM-for-Sefaria index and CSS are static files, so their whitespace is edited directly. |
| 3 | September 7 review 896/904, rows 13/21; remediation plan 355-358, `shared ITM/CoS`; post-silluq page 75, `BHS-derived` | R; H `1095f029`, `a9edd4f9`, `38a606e2`, `3b0225e0` | W1 dated notes distinguish retained model fixes from Ben's subsequent reversals and accepted glosses. BHS and edition questions settled; no reinstated prose. |
| 4 | `doc/PLAN-repo-maintenance-across-GitRepos.md` 21-24, `Apply every clause`; policy 70, `gitrepos_setup_rule` | R; read `all-repos.code-workspace` and policy together | W1 dated superseding instruction: clone exactly the workspace roster under the current policy. No enumerate/subtract proxy and no added gist clones. Do not run maintenance or alter the roster. |
| 5.1a | Three-repos evacuation plan 1853, `no longer prints`; September 4 review 743, `Six merged local MAM-basics branches`; 567, `does not exist` | R; H `4195440e`; D4 | W1 dated updates, explicitly distinguishing a formerly true filesystem observation from later state. Name and number the six branches from the historical record; do not invent a current branch census or delete anything. |
| 5.1b | Holman suppressed and active table pages; comparison-name and comparison-symval cells | V3; R `py/py_render/rt_comparison_table.py`, `comparison_table_html` | W2 add RTL declarations at the producing cells, including the separately traced active-page cell. Hebrew text, rows, counts, and issue metadata stay unchanged. |
| 5.2 | Public evacuation programme 832, `neither exists today`; rows 43/42, `3c8c9750` / `remains pending`; five-products plan 555, MAM-with-doc host list | R; H `19df42f3`, `9cf48863`; read landed READMEs | W1 dated notes: sparse instructions exist; workspace removal belongs to `19df42f3`; clone retirement was recorded by `9cf48863`; include `.gitattributes` and `.gitignore` in the historical host list. Do not redo evacuation or claim a fresh filesystem safety audit. |
| 5.3 | `cam1753/doc/reading-mam-simple.md` 30, `and this repo's was deleted` | R | W1 N1 if approved. Keep the historical equivalence measurements and comparison rule. |
| 5.4a | `py/tests/test_sibling_reach.py` 34-35, `says "Old git revision`; current `py/subcommands/diff_mpp.py`, `Stored release` | R | W1 N2 if approved. Test behavior unchanged. |
| 5.4b | `py/vendoring/gen_inventory.py` 350 and inventory 33, `These Python files live outside` | R; V4 | W4 N3 if approved. Regenerate inventory; policy and file ownership stay unchanged. |
| 5.5 | Public programme 915, `its own docstring`; procedure 210, `guard's own`; `CLAUDE.md` 80, `introduction's own`; `DATA-LICENSES.md` 56, `MAM-basics' own work` | R | W1 retain the dated programme sentence without cosmetic correction; N4-N6 propose the current fragments. No broad style sweep or license change. The six-branch enumeration is covered by 5.1a. |
| 5.6 | Skill `references/sources-and-corpora.md`, named three homes | H `becc6f00`; D2 comparisons | Settled; W1's later D2 edit requires a fresh whole-skill comparison. Do not inspect the retired private instruction repository. |
| 6.1-6.5 | `README.md` 67, `ten deploy-root`; `DATA-LICENSES.md` 72, `eight generated`; `py/main_authored.py` 9-12, `ten published`; `py/main_0_mega.py` 404-406, `ten deploy-root`; `py/check_html_syntax_and_sanity.py` 28, `ten HTML files` | R; V1 | W1 update current 10/8 descriptions to measured 11/9. No page added or removed, no checker scope changed. |
| 6.6-6.7 | `doc/PLAN-post-stress-meteg-page-and-holman-m23.md` 13/100, `ten deploy-root` / `including eight` | R; V1; H `825cef66` | W1 dated notes: the ninth MAS page arrived on main with the merge. Preserve the earlier execution counts as dated history. |
| 6.8 | `py/tests/test_site_index_links.py` 84, `this page carries 34` | R; run that test's walker; D8 | W1 D8 changes only 34 to 35; N9 separately proposes the accompanying date change. Retain floor 25. The old 34 was true at its date, not a false historical measurement. |
| 7.1 | Merge plan 3, missing State; 100-102, protected census; 87, `grep -c` | R; V1; H `ad44dba7`, `825cef66`; V5 | W1 insert `State: executed 2026-09-08; merge 825cef66; retained as a review record.` The later census correction already exists; do not repeat it as a new repair. Add a dated occurrence-versus-lines correction. Keep the filename and historical instructions. |
| 7.2 | Silluq plan 3, State; 25-26, English names; 279, `976 passed`; `Decisions and public contracts` | R; H `7f0e4bdd`, `2de7a969`, `527011b7`; V1 | W1 record that State and later dated decisions already arrived. Retain filename; append a note attributing the original proposal to the September 8 plan, not inventing Ben's approval of every contract. Correct the baseline-date/current-baseline claim by a dated note. Do not execute or revise that plan's product contracts. |
| 7 standard | `py/repo_util/check_repo_standards.py` 269-272, `all ten tracked` | R; V1 | W1 replace the false current census with a dated correction identifying the historical omission, then retain the existing State format rule. Add a pointer to the procedure for D10's current review naming/State rules. No new standards gate or plan deletion. |
| 8.1 | September 7 plan 334-336, `current source has 370`; September 7 review 886, row 3 | R; H reconciliation row 8 and rebuttal; public phonetic pages at `7322b665` | W1 dated correction: ordinary scope 368/370, with two dual-cantillation rows giving 370/372. Source movement did not cause the difference. Survey and its counts unchanged. |
| 8.2 | `doc/post-stress-meteg-method.md` 14-15, `retracted stress`; survey 1399-1411, type-3 conditions | R | W3 E1 only if approved; no classifier or scholarly-source change. |
| 9.1 | `DATA-LICENSES.md` 83, `retained source-hygiene test` | R; `git ls-files MAM-with-doc` | W1 remove `, and retained source-hygiene test`, joining the remaining list grammatically. Preserve the license terms. |
| 9.2 | `DATA-LICENSES.md` 73, `gh-pages/img/`; post-silluq page 66, F159A caption | R; `git ls-files gh-pages/img`; P2 | W1 individual provenance inventory with unknown fields explicitly recorded. Actual source/rights identification deferred. No image, license grant, or five unsupported folio captions changed. |
| 9.3 | Methods page 78, Aleppo crop/alt | R | W3 E8 only if approved; no new manuscript reading. |
| 10 / C5 | Procedure 24, review census; 165-174 naming; 249 path; former `will never load` | H `2cddb893`, `83b470da` | Settled in step 3. W1 records the disposition; no repeated procedure redesign. |
| 11.1 | September 7 plan 523, `had no subtest line`; three-repos plan 1853 | R; D4; suite record | W1 retain the observed Wave 4 output and add command-unrecorded/cause-unknown note. No reconstructed historical run. |
| 11.2 | September 7 plan 210-225 / 282-315, unchecked Wave 1/2 lists | R | W1 append a dated checklist-status note naming the completed implementation commits `c76239a5` and `e91d7358`; the original boxes remain an execution-record inconsistency, superseded by the note. Do not retroactively tick failed or reversed editorial items. |
| 11.3 | September 7 plan Wave 6, `all 25 Python files` / `all seven` | R; `git diff-tree --no-commit-id --name-only -r 9cf48863 -- '*.py'`; read `py/check_all.py` | W1 note 25 formatted source files plus one copied file, and the spell check's two tracked frequency outputs. Preserve the recorded successful run; do not describe the command as read-only. |
| 11.4 | September 7 Sol review 59-60 and reconciliation 858-859, `87` / `111` / `12` paths | R; V2 | W1 dated notes: those are finding counts; distinct files are 80/111/2. Keep total 210 in 193 files. |
| 11.5 / 17h | `9e6e9e17` message, `415 files`; review's 416 assertion | H `9e6e9e17`; accepting turns' limits | W1 record only: reviewer reports a commit-message file added after the 415 count; Codex did not independently establish 416. Do not use today's scratch count to falsify the earlier count, inspect unrelated task folders, or amend the commit. |
| 12 | `out/vendoring_compare_out.txt`, `eol-only` / `paths.py`; comparator `_identity` | V4; P1 | W4 regenerate after committing copies; preserve comparator purpose. Final report must distinguish observed LF identity from any guarantee about another checkout. |
| 13.1 | Survey 1518, `assert len(fit_types) <= 1` | R; accepting turns | W1 record latent unsupported overlap, keep the guard. No observed candidate or fit count changes. |
| 13.2 | Survey 1630-1644, `_census_chanted_word_summary` | R; C1, rebuttal, turn 5; D5 | Settled design note. Keep multiplicity guards, page statement, JSON schema, and counts. |
| 13.3 | Author module 1296-1298, `_hebrew_cell`; survey 2319-2324, `never to build a displayed form` | R; V3 display check | W3 technical repair: preserve all marks in an already-selected display form, translating only the existing gray-maqaf representation to maqaf. Keep comparison normalization for joining records. Current rendered text must remain identical across the full corpus. |
| 13.4 | `py/accgram/poetic_scanner.py`, `_fuse_cross_chanted_word_yored`; author `pin_claims`, `in_mam` | R; finding 1 acceptance | W1 record validation limits; keep the fusion invariant and chosen post-silluq interpretation. No extra behavioral test or assertion removal. |
| 13.5 | Survey 37-40, `MISMATCH`; `_problems` and `build_survey` | R; rebuttal correction | `_problems` returns; the build raises. W3 E4 addresses the remaining docstring omission; no code behavior change. |
| 13.6 | XML reader, `scrdfftar`; `spi-pe2` targets in `MAM-simple/xml-vtrad-mam/` | `rg -n -e scrdfftar -e spi-pe2 MAM-simple/xml-vtrad-mam py` followed by XML parsing of all targets | W1 record valid empty outputs and the review's 3+2 census as a bounded observation. Do not make valid empty targets fail. Recheck the whole target set if the input changed. |
| 13.7 | Main-page phi-6, `All 154 occur in Aramaic`; 2 Chronicles page, Leningrad forms; survey `stress_accent_classification` | R; C1 and accepting rebuttal | Conjunctive stress is checked and settled. W1 record that independent language/edition evidence is outside this remediation; retain the claims without calling them newly verified. No invented oracle or transcription. |
| 14.1 | Author 33-34; CLAUDE section; merge plan 46-47; lint 10-13 | R; rebuttal; E6 | W3 correct only the false before-any-use claim. Second expository paragraph is accurate. Immutable commit and issue unchanged. |
| 14.2 | `py/tests/test_post_stress_meteg_plain_word.py` 61-62, `_PAGE_FNAMES` | R; V1 | W2 make the existing lint detect an unlisted generated or declared MAS page while keeping missing-page failure. This is a mechanical coverage check, not an approval of a new page's terminology. No general exception registry. |
| 14.3 | Merge-hunk record / #265, 32 versus 36 | H reconciliation; V5 | W1 record only, as 17a. No history rewrite or issue action. |
| 14.4 | Skill opening, `Plain`; author and CLAUDE exception attribution; references/verifying already names the nine pages | R; D2; turn 5 | W1 D2 aligns the skill opening and checks all copies. Keep explicit repository exceptions and accepted local ITM/CoS glosses. No general registry or retrospective claim that the permission was nowhere in the skill. |
| 15.1 | Main HTML 107-109; Methods 85/88/91/93/95; 2 Chronicles 65, `meteg mark` | R; E2 | W3 approved markup only; 4/9/2 occurrences, visible text unchanged. |
| 15.2 | Main HTML 280, criteria `<ul>`; not-fit HTML 65, `three` | R; E3 | W3 approved list numbering only. |
| 15.3 | Methods 175, `We have not analyzed` / `I think`, cant-alef/cant-bet | H `a9edd4f9` | Settled author wording. Retain mixed voice and unexpanded labels; no automatic cleanup. |
| 15.4 | Survey 941 / 2459, strand sentence / annotations; author 38, `survey's own`; `py/author_site/site_data.py` 46, `THE MISC TITLES` | R; E5 | W3 E5 if approved. Retain the survey-versus-pages contrast in `survey's own`. W1 N7 proposes the site-data heading. Actual titles unchanged. |
| 15.5 | Method doc, `Another meteg`; survey category `tsere-vowelled` | R; E1/E7 | W3 remove only the approved duplicate and use the approved documentation spelling. Do not rename a JSON category for a prose cleanup. |
| 15.6 | Misc HTML 128, `gaʿya-before-paseq` | R; source-name exception | W1 record retained source phenomenon name; no meteg terminology sweep. |
| 16 | Merge plan 174, `Seven commits`; 74, `converted one`; DATA-LICENSES 88, `hand corrections`; eight withdrawn sites | R; H rebuttal; D6; V5 | W1 D6; N8 proposes a dated numbered list and explicit quote-conversion note in the merge plan. Retain all eight sites withdrawn by the rebuttal and reject the blanket cleanup premise. |
| 17a | `825cef66`, `36 hunks` | H reconciliation; V5 | W1 dated record: 32 author-module hunks, 13 conflicted files. No amended merge commit. |
| 17b-17e | Messages `fe4e602f`, `bdcdc5e2`, `24f1e4a3`, `95c457c2` | `git show <commit> --` and accepting turns | Settled: accurate descriptions of the commits that made them. D3 also corrects the later phi-5 description to three sentences and two tables; no message rewrite. |
| 17f-17g | `e91d7358`, `15ec6f4d`, `975a16c5`; prior fixed rows | H; findings 2/3/5/8.1 | W1 dated completion qualifications tied to actual remaining work, not to Ben's deliberate reversals alone. |
| 18.1-18.3 | Review's trailer, housekeeping, and merge-cadence census | H original review and reconciliation limits | Record only; housekeeping remains Ben's separate track. Do not remove branches, worktrees, folders, or caches, or rewrite trailers. This review worktree retires only under close-out step 7. |

## Wave 1 — dated records, current instructions, and settled dispositions

Preconditions: Ben has approved Wave 1 and P2/P3 and disposed of N1-N2/N4-N9; the merged starting tree is clean. Read the
original and accepting paragraphs for each W1 row before editing. Record the approvals in this
plan first. The count and historical checks above must reproduce or have a documented explanation.

1. Implement D2 exactly, following the shared-skill deployment procedure. The tracked destination
   is **C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/dot-claude/skills/hebrew-prose**,
   not the primary clone. Deploy whole directories without nesting an old copy inside a new copy.
   Verify the resolved paths before any recursive removal required by that procedure.
2. Correct the current non-MAS instructions and docstrings specified by the W1 rows. For finding
   4, add a dated paragraph immediately after the old scope paragraph: `Correction <date>:
   GitRepos setup follows the folders listed in all-repos.code-workspace, as specified by
   gitrepos_setup_rule in in/repo_maintenance_policy.json. Do not enumerate GitHub repositories
   and subtract exclusion lists, and do not add gist clones. The earlier scope paragraph's
   subtraction and gist instructions are superseded.` Link the policy and workspace. Do not
   write a competing roster into global instructions.
3. Add dated corrections beside each named September 4/7 review and execution record. The
   previous fixes' implementation commits remain historical facts; the later reversals and
   omissions must be named explicitly. D4's correction says the command was unrecorded and the
   missing-line cause is unknown. Finding 8.1's correction states both scopes and both counts.
4. In `doc/review-findings-2026-09-08.md`, append `## Corrections accepted in the review exchange`
   with a date and citations to the accepting turns. Cover C1/13.2, 13.5, 13.7's conjunctive
   stress, 14.1's paragraph qualification, the eight withdrawn finding-16 sites, 17b-17e and
   its three-sentence correction, 11.1's unknown cause, 6.8's historical truth, 14.4's actual
   location, the omitted C5 premise, and the omitted broad editorial instructions at
   `47edbee6`. Add the planning correction that the MAM-for-Sefaria index/CSS are static, not
   generator outputs. Attribute each conclusion; do not silently rewrite the original text.
5. Start `## Dispositions after remediation` in that review. Add dated rows for W1 work and for
   decisions already settled. Leave W2-W4 technical findings explicitly pending. Record P2's
   provenance-source identification as deferred, not fixed.
6. Create `doc/post-stress-meteg-image-provenance.md`, linked from the `gh-pages/img/` license
   row, listing the six exact filenames from the baseline. For each filename name only the
   codex and verse already supplied by the filename/caption. Use `Not recorded in the inspected
   public record` for photograph source and rights holder unless a specific public citation is
   actually established. Record F159A/column 3/line 8 only for the already-captioned Leningrad
   1 Samuel 17:5 crop. Preserve the no-grant license text. Add no unseen crop interpretation.

The eight finding-16 items the rebuttal withdrew are its five file/directory `carry`
examples, its two already-attributed hand-transcription phrases, and its characterization of
`b4706759` as a general vocabulary rule. List those eight items exactly as the rebuttal does.
The rebuttal's remaining-items paragraph does not retain `hand-authored whitespace` as a
remediation item; leave that phrase unchanged too. Apply the merge-plan editorial notes only
under N8, without guessing a direction of quote conversion.

Expected tracked changes: the named review/plan records; `README.md`, `DATA-LICENSES.md`,
`CLAUDE.md`; `cam1753/doc/reading-mam-simple.md`; the exact current docstring/comment files
listed in the W1 rows; the tracked skill opening; the new crop-provenance note; this plan and
the close-out execution entry. No generated page, corpus file, JSON, image, generator behavior,
test behavior, license grant, or sibling checkout changes. Finding 5.4b's generator wording
waits for W4. E items wait for W3 even when the surrounding file is touched in W1.

Format touched Python files, run the suite, and inspect `git diff --check` for the changed
text. Verify both whole-skill comparisons; both must be empty:

```powershell
git diff --no-index -- C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/dot-claude/skills/hebrew-prose C:/Users/BenDe/.claude/skills/hebrew-prose
```

```powershell
git diff --no-index -- C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/dot-claude/skills/hebrew-prose C:/Users/BenDe/.agents/skills/hebrew-prose
```

Execution record: **Not started.** Record date, approval, starting and merged HEADs, changed
paths, measurements, suite output, both skill comparisons, dispositions, implementation
commit, and final record commit. No integration or push.

## Wave 2 — whitespace outputs, Holman RTL, and page-lint coverage

Preconditions: Wave 1 complete; Ben has approved Wave 2; clean merged starting tree. Write a
unique ignored verification script and save the V2/V3 baseline reports before editing. Missing
inputs fail. Run the existing product and Holman commands once before source edits and distinguish
pre-existing output differences from the intended repairs.

1. Change the Unicode-name writer so blank separators occur between verses, not as a blank
   final line. Trace all 189 affected outputs through `py/mb_misc/write_utils.py` and the
   vendored example copy. Preserve exactly one terminating newline and all between-verse
   spacing. Do not strip every output indiscriminately.
2. Trace the nine AJF CSV trailing spaces through `py/mb_sefaria/write_utils_sef_or_ajf.py` and
   fix the emitting boundary. Parse CSV before comparing fields; remove only the measured
   line-ending spaces. Preserve meaningful internal whitespace, quoting, field counts, and
   verse text. Remove the measured trailing whitespace directly from the static
   `gh-pages/MAM-for-Sefaria/index.html` and `style-color-scheme-light.css`.
3. Fix the Holman cell constructors that emit the 49+1 missing RTL declarations. Trace the
   active-page cell separately; the suppressed table's constructor alone is not assumed to
   explain that cell. Use the existing Hebrew detection helper. Compare every row/cell's text
   before and after; only direction attributes may change.
4. Extend the existing `test_every_page_is_present` check to compare the expected tuple with
   both the rendered `post-stress-meteg*.html` set and the MAS filename constants declared in
   `author_site.site_data`. An unlisted declared or rendered page must fail, and a missing
   expected page must still fail. Preserve the existing forbidden-word scan and do not create
   an exception registry. This is a source/tree lint, not an example-based behavioral test.
5. Run the support-file copier after source changes, then regenerate MAM-simple's core outputs,
   both MAM-for-Sefaria variants, and the vendored MAM-simple example. Review the entire output diff, and run V2/V3
   again over current bytes. Zero findings must be established directly, not inferred from
   `git diff --check`. No hand-written expected verse is added as a test.

Commands from the worktree root, after formatting the touched source:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_mam_simple.py copy-support-files
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_mam_simple.py core-only
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_mam4sef.py --both-sef-and-ajf
```

Run the following command with **C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/MAM-simple**
as its working directory; the example's relative output paths require that directory:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/MAM-simple/py-examples/main_mam4sef_example.py
```

Return the tool's working directory to the verified worktree root for subsequent commands:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_just_render_table.py
```

Do not pass `--update-issue-metadata`. If a generator changes an unrelated artifact, explain
the change before staging; do not silently include it or discard another task's work.

Expected tracked changes: the producing Python files and their declared MAM-simple support
copies; the 193 whitespace files, subject to a freshly measured scope; the two Holman table
pages; the existing page-lint file; records. Holman CSS/JS must regenerate identically unless
the fix demonstrably requires a direction rule there. No MAS HTML, survey JSON, XML, parsed
corpus, downloaded input, issue metadata, or sibling output changes.

Validation: format touched Python; verify copied files equal their sources; full V2/V3
differential comparisons; canonical suite. Run the generators a second time only to establish
that the changed generators reproduce the repaired outputs, then require no additional diff.
Commit the source, copies, and regenerated products before W4 computes synchronization dates.

Execution record: **Not started.** Record approval, HEADs, exact changed paths, baseline and
final offending sets, CSV/text comparisons, RTL counts, generator commands, repeat-generation
result, suite output, implementation commit, and final record commit. No integration or push.

## Wave 3 — preserve displayed marks and apply approved MAS editorial items

Preconditions: Wave 2 complete; Ben has approved the technical repair and separately disposed
of E1-E8. Record every E disposition before editing. Save the tracked JSON's hash and baseline
HTML/text for all nine pages. Render once with the command below; any baseline diff must be
explained before the technical repair or editorial changes begin.

1. Repair `_hebrew_cell`'s use of comparison normalization. Display already-selected MAM forms
   without deleting U+05AF, U+05C4, U+05C5, or U+FB1E. Preserve the existing gray-maqaf-to-maqaf
   display conversion using the named constants. Do not change `_as_mam_would_write_it` for
   matching, add a new corpus rule, or alter the JSON. Check every display call's argument
   provenance; if a call supplies comparison text rather than the promised MAM form, resolve
   that call before claiming the general repair.
2. Before applying any E item, regenerate and compare the complete nine-page output with the
   baseline. Current HTML should be byte-identical; the observed forms contain none of the
   removable marks. Compare the helper's recovered text with its input, allowing only the
   declared maqaf conversion, across the complete current form set. Also use an exhaustive
   Hebrew-mark preservation probe against that simple independent rule; do not pin a single
   hand-picked verse. A future mark must survive even though current pages do not exercise it.
3. Apply only approved E items. E2 changes markup without text; E3 changes a list tag; E8 adds
   its approved sentence. E1/E4/E5/E6/E7 are limited to the exact source/documentation changes
   specified above. A rejected item gets a dated rejected disposition and no edit.
4. Regenerate from the same tracked JSON and inspect each page diff, including text, title,
   alt, href, IDs, images, list order, table content, and Hebrew mark order. All numerical
   claims, candidate records, Hebrew forms, and JSON bytes must remain unchanged. No MAS
   multiplicity count, new source attribution, or new terminology policy is added.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_authored.py gen-site --trust-surveys
```

Expected tracked changes: `py/author_site/post_stress_meteg.py`; approved documentation edits
in `py/accgram/post_stress_meteg.py`, `doc/post-stress-meteg-method.md`, and `CLAUDE.md`; dated
merge-plan note; only the MAS pages affected by approved E items; records. The index and
Unicode-proposals page are generated by the command but should remain identical. The survey
JSON, classifier behavior, manuscript images, BHS row, numerical tables, and all sibling trees
remain unchanged.

Validation: black on touched Python; the full display-text comparison; V1/V3; MAS page lint;
canonical suite; read the generated HTML diff. The mark-order check must cover Hebrew added
to any record as well as generated pages. Do not open a browser or start a server.

Execution record: **Not started.** Record technical and E approvals separately, retained/rejected
items, baseline synchronization, display comparison, exact visible-text and markup changes,
unchanged JSON hash, suite output, implementation commit, and final record commit. No integration
or push.

## Wave 4 — vendoring records, final dispositions, and one integration

Preconditions: Waves 1-3 have complete local execution records and clean commits; Ben has
approved Wave 4 and P1 and disposed of N3. All source/copy changes are committed before auditing. Merge current
`main` into the worktree branch and inspect any new input or instruction changes. Re-run a
relevant generator only if the merge changes its source or input; report new work rather than
assuming earlier validation covered the merged version.

1. Implement N3's exact inventory introduction if approved and format that Python file.
2. Run the full vendoring audit. Compare all declared public source/copy pairs as working-tree
   bytes and read the policy; do not traverse ignored private repository entries. The known
   25 EOL-only rows should disappear in the LF worktree if the inputs remain LF. Record the
   actual result, including any remaining differences, and the now-current synchronization
   dates. No source or copied Python file changes merely to silence the report.
3. Complete the dated disposition table with a row for every finding and qualification in the
   crosswalk. Distinguish fixed, settled by prior decision, rejected, deferred, and record-only.
   Identify which E items were approved and which were not. No source-identification deferral
   or unverified scholarly assertion becomes a claim of completed investigation.
4. Re-run V1-V4 and the canonical suite. Read all generated diffs against the implementation
   commits. Run the public repository-standards check below, using its reported current
   workspace roster; inspect every failure instead of treating an unchanged historical result
   as success. Do not run a maintenance sweep, spell check, or mega merely for a familiar
   completion checklist.
5. Commit the audit and the records locally, then perform the close-out plan's Integration
   section exactly once. The suite must pass on the final merged tree before the primary
   clone is fast-forwarded. If `main` moves meanwhile, merge it into the worktree again,
   resolve and verify there, then retry the fast-forward. Push only `main`; do not push the
   worktree branch. Record the worktree head and pushed main head in the final response.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_vendoring.py --all
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --check-repo-standards --workspace-file all-repos.code-workspace --visibility public
```

Expected tracked changes before the final merge: `py/vendoring/gen_inventory.py`,
`out/vendoring_compare_out.txt`, `out/vendoring_provenance_out.txt` if its measured data changes,
`doc/vendoring-inventory.md`, and execution/disposition records. No copied source, corpus,
image, page text, policy, or sibling source change. The final merge's additional changes are
identified separately and verified before integration.

After all source/copy commits, a second audit must produce no additional artifact difference;
this is the check that the dates were not generated before the commits they describe. Do not
make a source/copy commit after that audit without refreshing the affected audit records.

Final integration commands, after both checkout trees are clean and the merged worktree has
passed the suite:

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-basics merge --ff-only codex-review-2026-09-08
```

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-basics push origin main
```

Execution record: **Not started.** Record all local commits, final checks, complete dispositions,
worktree head, primary fast-forward, push result, and remote head verification. Worktree removal
and branch deletion are Ben's close-out step 7 after the final task ends; do not attempt them
from the live worktree.

## Verification recipes and commit discipline

Use uniquely named real scripts under `.novc/review-remediation-2026-09-08/` when a check needs
more than one plain command. Read files and subprocess output with explicit UTF-8, reconfigure
stdout/stderr, print a labelled ASCII summary, and save detailed reports as UTF-8 files. Do
not pipe shell data into `python -c`, use heredocs, or rely on old scratch-script contents.

**V1 — page and plan census.** Enumerate tracked paths with `git ls-files`. Count HTML directly
under `gh-pages/`, separately matching `post-stress-meteg*.html`; list every filename. Enumerate
direct `doc/PLAN-*.md` files and print each file's third line, failing a missing `State:`.
For the MAS lint, compare the declared filename constants, the explicit expected set, and
the generated filenames; retain failure on a missing file. The plan census is a report, not
a new test or permission to change other live plans.

```powershell
git ls-files 'gh-pages/*.html' 'doc/PLAN-*.md'
```

Git pathspecs can include descendants; the script must check each path's parent rather than
mistaking this command's total for a deploy-root count.

**V2 — all whitespace findings and output preservation.** Save the actual offending path/line
set before edits. Read bytes from every tracked file under
`MAM-simple/misc/unicode-names*`, `MAM-simple/py-examples-out/sefaria/`, and
`MAM-for-Sefaria/misc/unicode-names*`; for detection only, normalize CRLF to LF and test
`endswith(b"\n\n")`. Read the complete lines of the four trailing-space files named in
finding 2 and detect lines ending in ASCII space or tab. Report both finding counts and
distinct path counts, including their overlap. Missing expected inputs fail. At the planning
HEAD, the trailing line numbers are Deuteronomy CSV 171/176/178/179/180, Exodus CSV
525/532/533/534, static HTML 88/297/780/849/1211/1307/1308/1336/1392/1405/1476, and CSS 3.
These numbers are locators only; scan whole files again after edits. Also scan every newly
changed generated file for the same problems.

Compare each output with its pre-edit bytes after applying only the intended whitespace
removal to the baseline. Compare parsed CSV rows/fields to distinguish a field change from
a quoting or line-ending change. Require exactly the intended final-line/trailing-space
differences and no Hebrew-text or internal-spacing difference. The historical offending set
can also be recovered with:

```powershell
git diff --check b4706759 8bf586a3
```

That historical range establishes the old list, not current remediation success. A no-argument
`git diff --check` is still useful for newly edited lines but cannot replace this direct scan.

**V3 — RTL, displayed forms, and editorial diffs.** Parse both Holman HTML files using
`html.parser.HTMLParser`; accumulate cell text and inherited `dir` through the enclosing
element stack. Count Hebrew-containing `td`/`th` elements without effective RTL, recording
the page, class, row identifier, and cell text. Handle HTML void elements without pushing
them onto the stack. Compare cell text and table row order against the baseline after
regeneration. For MAS pages, compare all Hebrew text and markup before/after, with the
display-helper preservation rule described in W3. Count the unwrapped mark-name occurrences
in visible text nodes only; exclude titles and attributes. Verify E2's 4/9/2 distribution
before editing and zero of those unwrapped occurrences afterwards if E2 is approved.

**V4 — vendoring.** Read the current policy's source/copy declarations and compare every public
pair's bytes, separately reporting EOL-only differences; no missing path is silently skipped.
Inspect the index/working-tree EOL report and the last commit touching each changed copy:

```powershell
git ls-files --eol -- py/mb_cmn py/mb_misc py/mb_sefaria py/osis MAM-simple/py-examples
```

```powershell
git log -1 --format='%h %cs' -- MAM-simple/py-examples/mb_cmn/paths.py
```

```powershell
rg -n 'eol-only|^paths.py' out/vendoring_compare_out.txt
```

The authoritative refreshed artifacts come from `py/main_vendoring.py --all`, not from
hand-editing its output or substituting a blob comparator. Record the exact source/copy
commits used by the audit. The final current-byte comparison is independent of the report's
own identity labels.

**V5 — bounded historical counts.** To repair the merge-plan command explanation, read all
eight MAS HTML blobs at `15ec6f4d`, sum case-sensitive `text.count("chanted")`, and separately
sum the number of lines containing that string. The review reports 440 occurrences on 381
lines; re-measure instead of repeating the command's mistaken line-count interpretation.
For the seven-commit list, enumerate the historical branch endpoint, not current HEAD:

```powershell
git log --reverse --no-merges --format='%h %s' c73a2ad3..a3e3f6eb
```

For 17a, the reconciliation independently established 13 conflicted files and 32 author-module
hunks. If repeating the merge calculation, use the exact parents of `825cef66` in an isolated
Git object store or a read-only `git merge-tree` invocation; inspect the method's output and
count conflict markers within the author module only. Never merge these historical parents
into a checkout or rewrite the historical commit. An inability to reconstruct the old scratch
folder census leaves 11.5/17h unverified; it is not repaired by guessing.

Set the sibling root before each canonical suite run:

```powershell
$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider
```

Record the exact command, HEAD, elapsed time, passing/skipped/subtest counts, and full output
path. The planning run used the same suite with its normal cache provider; omitting that
provider avoids unrelated cache churn and does not change the tests. An unexpected count or
skip needs an explanation; a different run cannot explain an earlier missing output line.

Run black at defaults on all and only touched Python files in one invocation. Use the same
absolute interpreter with `-m black <files>`. New or edited Hebrew prose must pass
`mb_cmn.uni_denorm.has_std_mark_order`; the existing `test_prose_mark_order.py` lint covers
tracked Markdown and its other named prose paths, so stage newly added documents before relying on that lint. Check Python prose through the repository's source mark-order check or a direct call to the same authority. Do not
alter a copied Hebrew form by eye. No source or test adds `sys.path` configuration.

At each wave's end, inspect HEAD and `git status --porcelain` before staging only the named
work. Write a unique commit-message file and pass it via `git commit -F`; include
`Co-Authored-By: Codex <noreply@openai.com>`. Commit completed work locally. Record the
implementation hash in a following record commit when necessary; never amend just to insert
a commit's own hash. Update the close-out plan's step-6 execution record as well as the wave
record here. The final report gives every written path, every commit ID, clean status,
branch head, and any deferred or rejected item. Before handing writing responsibility to a
fresh task, the worktree and records must already be committed and clean.

## Work expressly left outside these waves

The silluq-template implementation, MAM-OSIS evacuation, Holman/Wikisource refresh, issue #265's
general exception registry, manuscript/edition adjudication, photograph-source investigation,
private-source research, broad prose cleanup, and repository/task-folder maintenance remain
separate work. The plan does not authorize posting comments or changing issues. The final
review worktree integration and retirement follow the close-out plan's final-wave/step-7
schedule, not the archival of an intermediate task.

## Step-4 planning execution record

2026-09-09: verified the required worktree, branch, clean tree, and source commit `83b470da`;
merged `main` to `dd86c96f`; read the public review exchange, instructions, and later decisions;
re-measured the live findings and ran the canonical suite (987 passed, 5 skipped, 65 subtests).
The new plan's links, referenced paths, table structure, and whitespace checks passed; the
existing prose mark-order lint passed after both documents were staged (1 passed, 991
deselected). No tracked Python file changed, so no Python formatting was required.
No remediation, generator run, primary fast-forward, or push occurred. Planning changes are
limited to this file and the close-out plan's dated step-4 execution entry. Step 5 remains Ben's
approval of the waves, P1-P3, and the individual E1-E8 and N1-N9 proposals.
