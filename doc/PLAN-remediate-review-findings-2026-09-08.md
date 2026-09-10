# Plan: remediate the reconciled 2026-09-08 public-repository review

State: live 2026-09-10; Waves 1-2 and Wave 3 technical implementation complete; separate Wave 3 editorial phase and Wave 4 pending; technical unchanged-HTML condition retained.

Status updated 2026-09-10 after Wave 3 technical verification: finding 13.3's revised
technical remedy is complete. Full-domain matching, serialized mark preservation,
annotation validation, normal generation and the final suite pass. The separate fresh
editorial task prepares its output contract under the existing E1-E8 approval after
the clean local checkpoint. Earlier status entries remain historical.

Status updated 2026-09-10 after Wave 3 preparation: the complete snapshot-form
differential and displayed-form trace are recorded below. The matching-only VARIKA
transformation is necessary for compatibility. No technical implementation or editorial
change has been made; Wave 3 remains incomplete. A fresh implementation task follows
the clean local preparation checkpoint under the existing bounded-task authorization.

Status updated 2026-09-10 after Ben's label approval: Wave 2 is complete. The dated
completion record below supersedes the partial checkpoint's pending-label status.
Wave 3 technical work is the next authorized fresh task; E1-E8 remain for the separate
editorial phase after passing technical verification.

Status updated 2026-09-10 during Wave 2: the whitespace and existing page-membership
lint repairs are ready for a local partial checkpoint. Holman RTL is implemented and
verified in the working tree, but its generator also updates an existing background-link
label outside the original direction-only contract. Ben's decision is pending; Wave 2
is incomplete and no successor is dispatched. Earlier status entries remain historical.

Status updated 2026-09-10 after Wave 1D2: all Wave 1 crosswalk rows and settled
decisions have explicit dispositions. Wave 2's whitespace, Holman RTL and page-lint
work is next. Waves 2-4 technical work and all E items remain pending; P2 source and
rights-holder identification remains deferred. The dated records below are preserved.

Status updated 2026-09-10 after Wave 1D1: the accepted-corrections append is complete;
verification and the local checkpoint are recorded below. Wave 1D2 owns the remaining
record-only dispositions and full Wave 1 reconciliation. Wave 1 remains incomplete.

Status updated 2026-09-09 after Wave 1C3: the assigned MAS-plan and standards
historical corrections are complete. Wave 1D is next; Wave 1 remains incomplete.

Status updated 2026-09-09 after Wave 1C2: the assigned September 7 historical records
now have dated corrections. Wave 1C3 is next; Wave 1 remains incomplete.

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

## Conditional approval: changed MAS HTML stops remediation

**Step-5 update, 2026-09-09:** Ben's approval of all waves and P/E/N proposals is recorded
under "Step-5 approval record and next execution phase" below. That decision supersedes
the pending-approval statements in this plan, including the earlier statements in this
section. The technical unchanged-HTML condition, fixed baseline, and mandatory stop remain
in force. Approval of E2/E3/E8 does not permit their execution during technical remediation.

Ben's decision, 2026-09-09, after the displayed-mark simulation and review of newer Phonetic
MAM work: the discussed technical changes are approved **only on the assumption that no
generated/public HTML changes**. This updates the proposed remediation itself: reassess the
use of annotated forms where an unannotated form is available, preserve legitimate displayed
marks, and revise annotation validation accordingly. Approval is conditional on the measured
output, not permission for any consequences of those code changes. The request to update this
plan authorizes documentation work now; it does not start a remediation wave or approve the
other pending proposals.

**A single changed byte in any of the nine MAS HTML files invalidates this conditional
approval and stops the entire remediation process for interactive discussion with Ben.**
Markup, whitespace, line endings, attributes, and Unicode mark order count just as visible
text does. A missing or additional MAS page also fails. Other HTML is not expected to change
from the discussed technical work; any such change is also a scope failure. Separately
approved Holman/whitespace work in W2 keeps its declared output contract.

Before any remediation edit or back-merge, establish V6's executable check against the nine
reviewed HTML blobs at `c2f238f2c253d7b00b2d22dc262fe95c81a82401`. Keep that baseline fixed
through the remediation waves and final integration. Run V6 before and after back-merges,
after rendering and validation, and before committing completed remediation or integrating.
An earlier passing simulation or suite is never a substitute for the current comparison.

On a difference, the check must exit nonzero and print prominently:

```text
STOP: MAS HTML CHANGED. BEN'S CONDITIONAL APPROVAL NO LONGER APPLIES.
REMEDIATION HALTED; INTERACTIVE DECISION REQUIRED.
```

Preserve the changed output, baseline, hashes, and readable diffs. Report the exact files,
changed locations, and relevant Unicode names to Ben. Stop all remaining remediation edits,
waves, completion commits, integration, and pushes; read-only diagnosis to prepare that
discussion is permitted. Do not normalize away the difference, update the baseline, add an
exception, filter the marks back out, mix in an editorial change, or fix forward and resume
without Ben. Do not discard existing work. Even if a later diagnosis identifies a correction
that would restore identical HTML, **Ben must explicitly renew or revise the agreement before
remediation resumes**. A failed or incomplete comparison likewise prevents proceeding; it
cannot establish the approval's prerequisite.

E2, E3, and E8 would deliberately change MAS HTML. Those proposals remain separately pending
and are excluded from this conditionally approved technical work. Ben's earlier preference
for coalesced E2 slash spans settles the proposed formatting only. Any later approval of an
HTML-changing E item must name the intended diff and explicitly revise the no-change contract
for a separate editorial phase, after the technical result has passed V6. An executor cannot
use an E item as an explanation that permits an unexpected technical diff. Other E/N items
and wave approvals retain their existing individual dispositions.

This condition takes precedence over any instruction below to explain a diff, update scope,
continue after verification, or carry out final integration. It applies to this remediation
process; it is not a permanent prohibition on future separately approved page development.

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

Inspect a mismatch before proceeding. For remediation execution, establish and run V6
before the required clean-tree merge of `main` into the branch. Run V6 immediately after the
merge, resolve conflicts in the worktree, and verify the merged tree here. An incoming MAS
HTML difference also triggers the conditional-approval stop; do not silently choose a newer
baseline. The 2026-09-09 simulation and this follow-up plan-only update retain the named
review checkout and commit without a back-merge; they do not execute these waves.

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
this plan. Re-measure at each wave's merged starting HEAD. Ordinary census changes require
an explanation and a scoped update. MAS HTML differences instead invoke the mandatory stop
above; neither re-measurement nor an agent-written scope update renews Ben's approval.

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
vendoring audit, must be named separately from remediation changes. The later simulation
below establishes synchronization for the nine MAS pages only, at its stated commit.

The public Phonetic MAM pages, if needed to repeat finding 8.1, are under
`C:/Users/BenDe/GitRepos/phonetic-hbo`, historically at `7322b665`; record that clone's actual
HEAD before use. Ben separately authorized looking beyond the review window at the newer
Phonetic MAM technical implementation and documentation named below, including that bounded
MAM-private history. Those read-only sources inform the remedy; no private scholarly-source
research, private survey regeneration, or publication of private source text is authorized.
Render MAS pages from the tracked JSON with `--trust-surveys`. Do not run a mega, refresh
Wikisource, or write MAM-OSIS as a side effect of these waves.

Another task may be live in the primary clone. That does not block this worktree. Keep one
writer in this exact worktree; compare HEAD and status immediately before staging. The final
integration requires both checkout trees clean and uses only a fast-forward in the primary
clone. Intermediate task archival does not integrate or push.

## Displayed marks: simulation and newer technical evidence

Measured 2026-09-09 in the required worktree, branch `codex-review-2026-09-08`, at
`c2f238f2c253d7b00b2d22dc262fe95c81a82401`: the real nine-page renderer reproduced every
tracked MAS HTML file byte for byte. Replacing only `_hebrew_cell` in memory to retain marks
also produced byte-identical HTML. This is a latent deletion risk, not an observed loss of
marks in the current pages.

`py/accgram/post_stress_meteg.py::_PHONETIC_MAM_ANNOTATIONS` deletes these marks in the
comparison helper `_as_mam_would_write_it`; `_hebrew_cell` currently reuses that helper:

| Code point | Unicode name | Relation to the Phonetic MAM annotations |
|---|---|---|
| U+05AF | HEBREW MARK MASORA CIRCLE | After HEBREW POINT SHEVA, annotates vocal shewa |
| U+05C4 | HEBREW MARK UPPER DOT | After HEBREW POINT DAGESH OR MAPIQ, annotates strong dagesh |
| U+05C5 | HEBREW MARK LOWER DOT | Not either of those two annotation encodings; the old deletion set is broader |
| U+FB1E | HEBREW POINT JUDEO-SPANISH VARIKA | Not either of those two annotation encodings; the old deletion set is broader |

The helper also converts ASCII `~`, the gray-maqaf placeholder `hpu.NU_GMAQ`, to U+05BE
HEBREW PUNCTUATION MAQAF. The simulated display behavior retained only that conversion;
it did not insert any mark absent from its input.

All protected files are under the worktree's `gh-pages/`. Counts below include repeated
helper calls and punctuation. Re-establish them with the targeted simulation recipe below.

| HTML filename | Helper calls at `c2f238f2` | Changed locations |
|---|---:|---:|
| `post-stress-meteg.html` | 35 | 0 |
| `post-stress-meteg-methods.html` | 32 | 0 |
| `post-stress-meteg-cases.html` | 468 | 0 |
| `post-stress-meteg-misc.html` | 20 | 0 |
| `post-stress-meteg-lacks-mas.html` | 357 | 0 |
| `post-stress-meteg-not-fit.html` | 68 | 0 |
| `post-stress-meteg-post-silluq.html` | 2 | 0 |
| `post-stress-meteg-2chr-8-11.html` | 5 | 0 |
| `post-stress-meteg-next-conjunctive.html` | 30 | 0 |

The run captured 1,017 calls and 674 distinct input strings. No input contained any of the
four deleted marks or the gray-maqaf placeholder. Both full output sets and all helper
results were identical. The input `out/accgram/post-stress-meteg.json` had SHA-256
`9b2ebdf41ab1a211a728b2f025fcbc101f8c33338007f9ea2fbe0b50c775fad2`.

The real call was `author_site.post_stress_meteg.gen_html_files(out_dir, trust_survey=True)`,
twice, with separate scratch destinations, normal claim checks and serializer, and unchanged
survey JSON. The simulated `_hebrew_cell` returned
`wrap_hebrew_runs((form or "").replace(psm.hpu.NU_GMAQ, psm.MAQAF))`. The run took 1.147
seconds and changed no tracked files. The command actually run was:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B C:/Users/BenDe/Documents/Codex/2026-09-09/referenced-chatgpt-conversation-this-is-an/work/simulate_preserve_displayed_marks.py
```

The script, report, helper-call trace, input hashes, and summary were saved under
`C:/Users/BenDe/Documents/Codex/2026-09-09/referenced-chatgpt-conversation-this-is-an/outputs/`
as `simulate_preserve_displayed_marks.py`, `preserve-marks-simulation-report.md`,
`preserve-marks-helper-calls.json`, `preserve-marks-input-hashes.json`, and
`preserve-marks-summary.json`. The script sets the worktree as its working directory and
requires the exact measured HEAD, so it will reject the later plan-update commit. Do not
weaken that historical check and present a later run as the original measurement. A fresh
executor should reproduce the two-pass method in a new, uniquely named scratch script,
record the actual HEAD, retain V6's fixed HTML baseline, and fail on missing inputs.

The provenance inspection found selected MAM forms, next MAM forms, and punctuation; no
observed record call used the `mam_form or chanted_word` fallback. A BHS-labelled comparison
form comes from vendored UXLC 3.9, with an equality assertion against WLC 4.22. The
dual-cantillation comparison path uses selected MAM forms through `_template_mam_forms` and
`_mam_forms_for_dual_cantillation_difference`; involvement of Phonetic MAM records does not
make those displayed strings annotated `fva` text. Do not describe every helper input as a
current MAM form, or every Phonetic MAM comparison as annotated text needing deletion.

Newer evidence, inspected read-only with Ben's permission on 2026-09-09:

1. MAM-basics `b865b7c8fd9cb95e6a3a850fadcb9f852299c2a4`,
   `py/mb_cmn/paths.py::al_hatorah_phonetic_dir`, documents `READ rep FOR MAM'S SPELLING OF A
   CHANTED WORD, NOT fva`. That documentation commit was absent from the measured review
   branch. Inspect it with `git show` from the worktree's shared Git history; its presence
   on newer main is not evidence that consumers were migrated.
2. At `C:/Users/BenDe/GitRepos/MAM-private`, commit
   `e21306165707f9500ea19540d04af3e1918b563d`, read
   `al-hatorah/io/a01-phonetic-std-set/README.md`, anchor `To get MAM's spelling of a chanted
   word, read rep, not fva`, and
   `doc/explore-phonetic-mam-carrier-marks-2026-09-09.md`, sections 3.3, 3.4 and 6. A record's
   first `rep` form supplies its unannotated snapshot spelling when annotations are present;
   otherwise the first `fva` form suffices: `(record.get("rep") or record["fva"]).split(" ")[0]`.
   This establishes an alternative to stripping annotations, not equivalence to current MAM.
   The snapshot preparation had already removed native extraordinary dots; `rep` cannot
   recover those dots. Keep current-MAM selection and edition distinctions where needed.
3. The same MAM-private commit adds
   `al-hatorah/py/aht_phon/carrier_guard.py::write_published_page` and
   `assert_no_carriers`. The guard fails after writing a published page if MASORA CIRCLE or
   UPPER DOT occurs; it never repairs a source literal. This is generated-output validation,
   not a Python-literal linter, and it does not cover MAM-basics MAS pages. The related
   `a9cae00964cd24785564b8632aad7717695c48e7` explicitly removed accidentally pasted UPPER DOT
   from two literals at `testrecs_jacobson_notes.py::EX_24_11_GAYA_MV`. Existing consumers
   still include `fva`-plus-removal display paths; documentation and the guard did not perform
   a general migration to `rep`.
4. MAM-basics already calls
   `_assert_no_phonetic_mam_annotations_in_lacks_mas_page` after generation. Its forbidden
   set is the entire old translation table, including LOWER DOT, VARIKA and the placeholder.
   That blanket check covers only the lacks-MAS page. It must be reassessed alongside display
   preservation: merely removing display filtering leaves a guard that rejects legitimate
   source marks. The newer private guard is useful precedent for failing visibly, but its
   blanket UPPER DOT ban cannot be copied into general MAM display validation.

The revised remedy must select unannotated text from the appropriate source, preserve that
source's marks, and fail accidental Phonetic MAM annotations using source/context evidence.
An accidentally annotated Python literal is a source defect to report and correct explicitly,
not a reason to silently sanitize all display strings. Audit the existing matching uses of
`_as_mam_would_write_it` against `rep` availability; do not assume they are all necessary or
all removable. These are substantive changes to the proposed repair and validation.

Confidence is high for the simulated display rule at the measured inputs. The simulation
did not change `rep` selection, matching, or validation, rerun the survey, regenerate the
whole site, or inspect the live deployment. The broader revised implementation therefore
needs fresh differential evidence and V6; the original zero-diff result does not preapprove
its consequences. No actual before/after Hebrew snippet changed in the simulation.

## Decisions already taken and proposals awaiting step 5

**Status correction, 2026-09-09:** step 5 is complete. The heading and earlier conditional
phrasing below predate the final approval. The dated step-5 record gives the current
dispositions; no listed wave, P, E, or N item needs its proposal approved again.

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
All E items remain associated with Wave 3 but require a separately authorized editorial
phase. They are not bundled into the conditionally approved technical changes. E2/E3/E8
cannot run under the present no-HTML-change contract; see the conditional-approval section.

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

**Later decision, 2026-09-09:** Ben approved E1-E8 in full, including the amended E2 above.
The preceding paragraph remains the record of the earlier slash-formatting decision.
E1-E8 execute in the separate Wave 3 editorial phase after the technical phase passes V6;
the phase's output-contract preparation is specified below.

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
later acceptance determines the disposition. `V1`-`V6` are the concrete verification recipes
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
| 13.3 | Author module 1296-1298, `_hebrew_cell`; survey 2319-2324, `never to build a displayed form` | R; newer technical evidence above; V3; V6 | W3: use available unannotated source forms where appropriate; reassess comparison normalization against `rep`; preserve legitimate displayed marks and revise annotation validation together. No silent display sanitization or changed survey JSON. All nine complete HTML files must remain byte-identical; any difference stops the entire remediation for Ben's renewed decision. |
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

### Smaller execution tasks, recorded 2026-09-09

Ben's instruction, 2026-09-09: size remediation tasks to avoid compaction, and certainly
multiple compactions. Codex's initial Wave 1 task compacted during preparation. The execution
units below replace the earlier one-task-per-wave expectation without changing approved scope,
wave order, V6, or the single integration after Wave 4:

1. **Wave 1A: V6 and D2.** Establish and prove V6, back-merge and recheck, deploy the exact D2
   sentence, verify, and commit. Required source `6e15a648ac292760b6bf623cca2d5e43442aabd4`;
   merged source `bd5d9e56fdafb47617c38ce98bc9c98d8337448f`. The Step-5 approval above
   authorizes D2 and the remaining Wave 1 work; no additional approval is needed.
2. **Wave 1B: current documentation and P2.** Apply the current-file corrections in W1's
   crosswalk and N proposals, create the six-file crop-provenance inventory and its license
   link, and add finding 4's dated maintenance-scope correction. Leave historical review and
   execution-record corrections for Wave 1C, including the standards docstring's dated
   census correction. Record dispositions only for work completed in Wave 1B.
3. **Wave 1C: earlier historical records.** Add the approved dated corrections to the
   September 4/7 reviews and named execution plans, including the merge plan's State line
   and N8 notes and the standards docstring's census correction. Keep original records.
4. **Wave 1D: September 8 accepted corrections and completion.** Append the complete
   accepted-corrections section, reconcile all W1 and already-settled dispositions, verify
   Wave 1's full completion, and then hand off Wave 2. W2-W4 and editorial work remain pending.

The next task reads the governing approval, V6, checkout, and handoff requirements and its
assigned crosswalk/proposal entries. Read original and accepting source paragraphs for those
entries; do not reload every complete historical turn for an unrelated item. This scoped
reading instruction supersedes the earlier requirement to reread both plans in full in every
execution task. Applicable global, repository, and skill instructions still apply. A task
needing a smaller boundary records completed and remaining items before a clean commit and
handoff; it does not mark its wave complete prematurely. Ben's existing automatic phase-handoff
authorization applies to these smaller execution tasks. No predecessor is archived automatically.

Wave 1A execution record follows the wave's original execution placeholder below.

**Step-5 handoff, 2026-09-09:** Wave 1, P2/P3, and N1-N2/N4-N9 are approved. The next
fresh task first implements and proves V6 in ignored scratch files, checks the original
checkout and fresh scratch render, and only then back-merges `main` and checks V6 again.
No remediation edit precedes that gate, including D2 or a dated correction. After those
checks pass, execute only Wave 1. The approvals are already recorded; cite the dated
step-5 decision in the wave record instead of asking Ben again.

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

### Wave 1A execution record, 2026-09-09

The preceding placeholder describes the original full-wave execution record. Wave 1 is
partially complete: Wave 1A is complete, and Wave 1B is next. Codex task
`01a0891a-4362-7891-bf6f-84b76900164c` verified the exact clean required source
`6e15a648ac292760b6bf623cca2d5e43442aabd4` in the named review worktree, on
`codex-review-2026-09-08`. Ben's Step-5 approval authorizes the implemented D2 sentence.

V6 was implemented in the ignored worktree file
`.novc/review-remediation-2026-09-08/v6_gate_wave1_01a0891a.py`, SHA-256
`286e1aa5410ed39b6851c7f94d64476bb826a460909ca27f00de5289eb6e4f9c`.
The script recovered all nine HTML blobs and the survey JSON from the fixed `c2f238f2` commit
using binary Git output, wrote an immutable baseline with hashes, and proved nonzero failure
on separately labelled changed-byte, missing-page, and extra-page probes. All three deliberate
probe runs exited 17. The probes were separate from the actual checkout and render checks.
The actual checkout and a fresh render both passed before the merge, with exact membership
and bytes, unchanged JSON, normal assertions and annotation validation, input read/hashes,
and imported worktree-module hashes recorded. No private source was read by the renderer.

The clean back-merge of `main` completed without conflicts at
`bd5d9e56fdafb47617c38ce98bc9c98d8337448f`, incorporating `4ee7ec7c`'s Graphviz work.
V6 passed immediately afterward. The reviewed HTML baseline remains `c2f238f2`, not the merge.
The evidence directories below are relative to the worktree's
`.novc/review-remediation-2026-09-08/v6-runs/`:

1. Before merge and deliberate failure proofs: `20260910T022130Z-wave1-before-merge-29831f6c/`.
2. Immediately after merge: `20260910T022214Z-wave1-after-merge-e1800160/`.
3. After the Wave 1A suite: `20260910T023336Z-wave1a-after-suite-3826fb4e/`.
4. Before the checkpoint commit: `20260910T023548Z-wave1a-before-commit-653351d3/`.

Each actual check passed for nine checkout pages and nine freshly rendered pages, with zero
changed locations. The pinned JSON SHA-256 remains
`9b2ebdf41ab1a211a728b2f025fcbc101f8c33338007f9ea2fbe0b50c775fad2`.
No real V6 stop occurred. A future missing script or baseline requires inspecting or rebuilding
the gate from the fixed Git blobs and the full V6 specification; it does not permit skipping V6.
Never clear a real `V6-STOP-REQUIRES-BEN.json` record to continue without Ben's renewed approval.

To reuse the gate after verifying the script, baseline, and absence of a real stop, run from
**C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08** with a fresh identifying label:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B .novc/review-remediation-2026-09-08/v6_gate_wave1_01a0891a.py check --label wave1b-before-merge
```

D2 changed only the approved opening sentence. All three skill directories were byte-identical
before editing and were backed up under
`.novc/review-remediation-2026-09-08/d2-wave1-01a0891a/`. Codex edited the live Claude copy,
verified the exact resolved destination paths and absence of reparse points, then copied whole
directories to the tracked worktree and live Codex homes in the prescribed order. Both required
`git diff --no-index` comparisons passed with empty output. An independent SHA-256 inventory
confirmed identical bytes for all five files in each home and proved that only the exact D2
sentence changed. The existing references and MAS exception were preserved.

The skill-creator `quick_validate.py` could not run in the primary clone's interpreter:
`yaml` is not installed. The same missing dependency prevents validation of the backed-up
pre-edit skill. No dependency or frontmatter change was made for this sentence correction;
the exact-edit and whole-directory checks above passed.

The canonical suite ran in the worktree with `REPOS_ROOT=C:/Users/BenDe/GitRepos`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B py/main_test.py -q -p no:cacheprovider
```

Result: **987 passed, 5 skipped, 65 subtests passed in 110.21 seconds**. The log is
`.novc/review-remediation-2026-09-08/wave1a-01a0891a-suite.log`; the invocation and environment
are preserved in `verify_wave1a_01a0891a.py` beside it. V6 ran immediately after the suite.
The changed-line whitespace check passed. No tracked Python file changed, so black was not
required. The existing prose mark-order lint passed after the record additions (1 passed in
0.16 seconds). No generated HTML, survey JSON, image, corpus, or generator behavior changed.

Tracked changes are confined to this plan, the close-out plan, the D2 sentence in
`dot-claude/skills/hebrew-prose/SKILL.md`, and the Wave 1A disposition in
`doc/review-findings-2026-09-08.md`. The implementation and subsequent record commit are
recorded after their hashes exist. No integration, push, or archival occurred.

Implementation commit recorded 2026-09-09: `d5616b8f` contains the Wave 1A changes and
execution record. The subsequent record-only commit supplies this hash without amending
the implementation commit. Its clean branch head is the required source for Wave 1B.
Wave 1B uses the same saved worktree directly and starts from this implementation as an
ancestor. The final handoff reply and task creation result identify that source head and
the successor task. No remaining decision blocks Wave 1B; later editorial output-contract
preparation remains assigned to the separate editorial phase.

### Wave 1B execution record, 2026-09-09

Codex task `01a0892f-1dac-7811-9662-8554324cbafc` completed the approved current-documentation
corrections and P2 inventory under Ben's Step-5 decision. The verified checkout was
**C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08**, branch
`codex-review-2026-09-08`, clean at required source
`85dcf63dc1a0aef83cca8cedbacc95365743f6f9`. The required `git merge --no-edit main` reported
`Already up to date.`; the source HEAD therefore remained unchanged.

Before the back-merge, Codex inspected the existing V6 script and immutable manifest. The
script's SHA-256 matched the Wave 1A record, and the gate verified every baseline file against
the fixed `c2f238f2` Git blobs. The earlier deliberate failure proofs remain applicable; no
baseline or gate code changed. Actual V6 checks all passed for nine checkout pages and nine
freshly rendered pages, with zero changed locations and unchanged pinned survey JSON:

1. Before merge: `v6-runs/20260910T024255Z-wave1b-before-merge-c4fc1a74/`.
2. Immediately after merge: `v6-runs/20260910T024313Z-wave1b-after-merge-ddfad623/`.
3. Immediately after the suite: `v6-runs/20260910T025056Z-wave1b-after-suite-c2cf23c6/`.

These evidence paths are under the worktree's `.novc/review-remediation-2026-09-08/`.
Each directory records the actual input reads, hashes, imported worktree modules, complete
output hashes, and comparison result. The invocation used the absolute primary interpreter
with `-B`, `v6_gate_wave1_01a0891a.py check --label <named-check>`. No real V6 stop occurred.

`measure_wave1b_01a0892f.py` wrote `wave1b-01a0892f-measurements.json` in the same scratch
directory. Re-establish from the named checkout using:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B .novc/review-remediation-2026-09-08/measure_wave1b_01a0892f.py
```

The first report is preserved; later measurements use timestamped filenames rather than
overwrite the recorded evidence. At `85dcf63d`, the tracked deploy root had eleven HTML
pages, including nine MAS pages. The site's real `_authored_anchors()` walker returned 35,
with floor 25. MAM-with-doc retained `.gitattributes`, `.gitignore`, `LICENSE.md`, and
`README.md`. The crop inventory matched all six tracked files and their recorded captions.
The workspace roster now had six entries: `63ac5b841ba7896acff8a5bd4c7a248d5609478c` removed
`github-misc` after the review's seven-folder measurement. The workspace and policy were read
together; neither changed and no maintenance operation ran.

Changed paths, all relative to the verified checkout:

| Paths | Completed scope |
|---|---|
| `README.md`; `DATA-LICENSES.md`; `py/main_authored.py`; `py/main_0_mega.py`; `py/check_html_syntax_and_sanity.py` | Findings 6.1-6.5: current eleven/nine wording. DATA-LICENSES also has finding 9.1's corrected retained-file inventory, N6's exact phrase, D6's Ben Denckla attribution, and P2's inventory link. |
| `CLAUDE.md`; `cam1753/doc/reading-mam-simple.md`; `doc/dual-agent-review.md`; `py/tests/test_sibling_reach.py`; `py/author_site/site_data.py`; `py/tests/test_site_index_links.py` | Exact N1/N2/N4/N5/N7/N9 fragments and D8's 35-anchor comment; floor 25 preserved. |
| `doc/PLAN-repo-maintenance-across-GitRepos.md` | Finding 4's exact dated correction immediately after the old scope paragraph, with links to the policy and workspace. |
| `doc/post-stress-meteg-image-provenance.md` | P2's six-file inventory; photograph sources and rights holders unrecorded, with only the already-captioned F159A/column 3/line 8 location. Source identification remains deferred. |
| `doc/review-findings-2026-09-08.md`; `doc/PLAN-remediate-review-findings-2026-09-08.md`; `doc/PLAN-close-out-review-2026-09-08.md` | Dated dispositions only for completed Wave 1B work and execution/checkpoint records. |

Black at defaults left all six touched Python files unchanged. The scratch
`verify_wave1b_01a0892f.py` compared Python ASTs against the source commit: only docstrings and
the approved `gen-site` description differ. The same check verified the allowed changed paths,
unchanged license terms, unchanged crop hashes, exact inventory membership, unknown-source
fields, the sole captioned folio, and changed-line whitespace. This is disposable verification;
no test was added or changed in behavior. D2's three deployed skill homes were preserved.

The canonical suite ran with `REPOS_ROOT=C:/Users/BenDe/GitRepos` in the verified worktree:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B py/main_test.py -q -p no:cacheprovider
```

Result: **987 passed, 5 skipped, 65 subtests passed in 108.36 seconds**; the wrapper's elapsed
time was 109.32 seconds. The complete log is `wave1b-01a0892f-suite.log`; invocation, cwd,
environment, HEAD, exit code, and elapsed time are in `wave1b-01a0892f-suite.json`. Both are
under the scratch directory above. The new provenance note was staged before the suite so the
existing tracked-prose lint included it. V6 passed immediately afterward.

No generated page, corpus, survey JSON, image, generator behavior, test behavior, license grant,
or sibling checkout was changed by Wave 1B. No private research, source refresh, survey
regeneration, mega, issue communication, cleanup, integration, push, or archival ran. E6 and
all other E items remain assigned to the separate editorial phase. Wave 1 is not complete.

**Next execution boundary:** Wave 1C begins with a smaller Wave 1C1 task for findings 5.1a
and 5.2: the evacuation records and September 4 review. Its targets are
`doc/PLAN-evacuate-the-rest-of-three-repos.md`, `doc/review-findings-2026-09-04.md`,
`doc/PLAN-evacuate-public-repos-programme.md`, and `doc/PLAN-evacuate-five-MAM-products.md`,
plus the required disposition and plan records. The three-repos plan's subtest correction
uses D4's command-unrecorded/cause-unknown limit. Remaining September 7 and MAS-plan historical
corrections, N8, and the standards docstring correction stay for a subsequent Wave 1C task,
split again if needed. Wave 1D still owns the September 8 accepted-corrections append and
complete disposition reconciliation. Ben's automatic handoff authorization applies after
the verified clean checkpoint; integration and push occur once after Wave 4.

Wave 1B implementation commit recorded 2026-09-09:
`42520d05ad004e99c0fff68bcf634a763ad22b15`. The implementation commit left the worktree clean.
Final disposable scope checks passed in `wave1b-01a0892f-final-verification.json`, and the
post-record prose mark-order lint passed (1 test in 0.16 seconds). The pre-implementation-commit
V6 evidence is `v6-runs/20260910T025358Z-wave1b-before-commit-9fd8bb6c/`; V6 also passed at
`42520d05` before the record commit, in
`v6-runs/20260910T025612Z-wave1b-before-record-commit-04f763c5/`. Both checks had zero changed
locations. Paths are relative to the scratch directory identified above. The following
record-only commit provides Wave 1C1's required clean source; its hash and actual successor
task ID are reported at handoff. The saved project was verified as
`51e16ebd-373a-41f7-833e-9def3ef72b81`, at the exact review-worktree path; use it directly
with `environment.type = local`. No new decision blocks Wave 1C1.

### Wave 1C1 execution record, 2026-09-09

Codex task `01a08940-ef16-7b02-b00b-a99f8e9048c7` applied findings 5.1a and 5.2 under
Ben's Step-5 approval in **C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08**,
branch `codex-review-2026-09-08`. The required clean source was
`d4dacdbaea8f57cd23012840fa9a0a30e378a950`, containing Wave 1B implementation
`42520d05ad004e99c0fff68bcf634a763ad22b15`. The required back-merge reported
`Already up to date.`; HEAD remained at the required source.

The existing `v6_gate_wave1_01a0891a.py` was inspected before editing or merging. Its
SHA-256 remained `286e1aa5410ed39b6851c7f94d64476bb826a460909ca27f00de5289eb6e4f9c`.
The gate verified its immutable baseline against the fixed `c2f238f2` Git blobs and passed
for nine checkout pages and nine fresh-render pages, with zero changed locations and
unchanged survey JSON. Evidence under `.novc/review-remediation-2026-09-08/`:

1. Before merge: `v6-runs/20260910T030021Z-wave1c1-before-merge-7b488862/`.
2. Immediately after merge: `v6-runs/20260910T030117Z-wave1c1-after-merge-3f06fc43/`.

The sandbox initially prevented the shared interpreter from launching; the escalated
invocation executed successfully. No gate comparison failed, and no real V6 stop occurred.
The script, baseline, and earlier labelled failure probes are preserved.

Historical evidence was re-established with bounded scratch scripts in the same directory:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B .novc/review-remediation-2026-09-08/measure_wave1c1_01a08940.py
```

The resulting `wave1c1-01a08940-20260910T030751Z-measurements.json` records the HEAD,
landed README instructions, named historical commit diffs, and the fixed public MAM-with-doc
Git tree at `904c9fa178265dce6fec5704f5c0424fc94f6719`. That host tree includes
`.gitattributes` and `.gitignore`. The earlier `20260910T030550Z` report is preserved.
Neither measurement found original branch-deletion tool-output events in the bounded
September 4–7 session files. A narrower extraction then found the quoted deletion output
in the retained checkpoint of September 7 task `01a07c08-5db6-7833-a7ce-d96a397fd77e`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B .novc/review-remediation-2026-09-08/extract_branch_outputs_wave1c1_01a08940.py
```

`wave1c1-01a08940-branch-output-extract.json` identifies the source, timestamp, and matched
deletion lines. Only the matching fields were extracted; full historical conversations were
not loaded. The September 4 review now numbers the six names and recorded tips from that
checkpoint, explicitly as historical evidence. No current branch census or cleanup ran.

| Changed path | Completed scope |
|---|---|
| `doc/PLAN-evacuate-the-rest-of-three-repos.md` | Dated correction beside the no-subtest-line claim, preserving D4's command-unrecorded/cause-unknown limit and citing the later Wave 6 output. |
| `doc/review-findings-2026-09-04.md` | Dated directory-state distinction, numbered historical branch list, and the superseding `4195440e` removal of `_PRIMARY_CLONE`. |
| `doc/PLAN-evacuate-public-repos-programme.md` | Dated sparse-instruction correction and adjacent table notes for `19df42f3`'s workspace/visibility removal and `9cf48863`'s recorded clone retirement. The dated `its own docstring` sentence remains unchanged. |
| `doc/PLAN-evacuate-five-MAM-products.md` | Dated correction naming both omitted host dotfiles. |
| `doc/review-findings-2026-09-08.md` | Disposition rows for completed 5.1a/5.2 work only. |
| This plan and `doc/PLAN-close-out-review-2026-09-08.md` | Execution evidence and the next bounded task. |

All original lines in the historical records are retained. No tracked Python changed,
so black was not needed. No generated HTML, corpus, JSON, image, behavior, license grant,
or sibling checkout changed. D2's three deployed homes and Wave 1B's work are preserved.
The canonical suite ran at `d4dacdba` plus the Wave 1C1 edits, with
`REPOS_ROOT=C:/Users/BenDe/GitRepos`, using:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B py/main_test.py -q -p no:cacheprovider
```

It reported **987 passed, 5 skipped, and 65 subtests passed in 106.01 seconds**.
`verify_wave1c1_01a08940.py suite` preserves the complete output in
`wave1c1-01a08940-20260910T031242Z-suite.txt`, with invocation and elapsed time in the
adjacent `.json`. The script propagated command failure and ran V6 immediately afterward:
`v6-runs/20260910T031429Z-wave1c1-after-suite-4e8cf93b/` passed with zero changed locations.
The same verification script's `scope` mode checks the allowed Markdown paths, exact
preservation of every original historical line, Hebrew mark order through
`has_std_mark_order`, and `git diff --check` against the required source. No test was added.
The implementation commit is recorded below after creation.

**Next execution boundary:** Wave 1C2 covers the September 7 historical review and
remediation records, including the Sol review's finding-versus-file counts: findings 2,
3, 8.1, and 11.1–11.4, with only the corresponding historical completion qualifications
from 17f–17g. Add dated notes beside original and accepting paragraphs; do not reinstate
reverted prose, repair whitespace outputs, reconstruct a historical suite run, or run the
spell checker. Preserve the original checkboxes. Split again if needed to avoid compaction.
The MAS-plan notes, N8, standards docstring census, and remaining record-only dispositions
remain for later Wave 1 work. Wave 1D owns the September 8 accepted-corrections append and
full disposition reconciliation. Wave 1 is incomplete; Wave 2 and all E items remain pending.
The successor uses the same saved project directly with `environment.type = local`, after
the implementation and write-back are committed and clean. No intermediate integration,
push, or automatic archival is due.

Executed 2026-09-09: Wave 1C1 implementation commit
`9241107ba5c3438a8b51c3032bfdce0bd7b4d070`. The worktree was clean after that commit.
The final scope report is `wave1c1-01a08940-20260910T031639Z-scope.json`: all changed
paths are the seven named Markdown files, all original historical lines are preserved,
and mark order and changed-line whitespace pass. V6 also passed at both checkpoints:

1. Before implementation commit: `v6-runs/20260910T031544Z-wave1c1-before-commit-3d3395df/`.
2. At `9241107b`, before record commit: `v6-runs/20260910T031635Z-wave1c1-before-record-commit-7af62954/`.

All Wave 1C1 actual comparisons had zero changed locations; no real stop occurred.
This following record-only commit supplies Wave 1C2's required clean source; the final
hash and actual successor ID are reported at handoff. The saved project was verified as
`51e16ebd-373a-41f7-833e-9def3ef72b81`, with the exact review-worktree path and Git enabled;
use `environment.type = local`. No new decision blocks the bounded Wave 1C2 task.

### Wave 1C2 execution record, 2026-09-09

Codex task `01a08953-8231-70f1-859c-663cb8c29a72` executed the bounded September 7
historical-record corrections under Ben's Step-5 approval, directly in
**C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08**, branch
`codex-review-2026-09-08`. The required clean source was
`8d6c4df8bac66367aa4519b633cf450a558b27c8`, containing Wave 1C1 implementation
`9241107ba5c3438a8b51c3032bfdce0bd7b4d070`. Exact path, branch, HEAD, clean status,
required ancestry, and actual task ID were verified before reading; the required
back-merge reported `Already up to date.`

The existing `.novc/review-remediation-2026-09-08/v6_gate_wave1_01a0891a.py` was
inspected and its SHA-256 matched
`286e1aa5410ed39b6851c7f94d64476bb826a460909ca27f00de5289eb6e4f9c`.
The script verified the immutable nine-page and survey baseline against `c2f238f2`.
The initial sandbox invocation could not launch Python; the escalated invocation
succeeded before any edit or merge. No actual gate comparison failed and no real stop
occurred. The unchanged gate passed for nine checkout pages and nine fresh-render
pages with zero changed locations at both initial checkpoints, under
`.novc/review-remediation-2026-09-08/`:

1. Before merge: `v6-runs/20260910T032021Z-wave1c2-before-merge-83d96703/`.
2. Immediately after merge: `v6-runs/20260910T032130Z-wave1c2-after-merge-7933f3ad/`.

Historical facts were re-established without regeneration by:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B .novc/review-remediation-2026-09-08/measure_wave1c2_01a08953.py
```

The final measurement report is `wave1c2-01a08953-20260910T032641Z-measurements.json`,
beside that script; the earlier `20260910T032547Z` report is preserved. The report
records the exact offending paths/lines and input hashes, 210 findings in 193 files,
189 blank final lines and 21 trailing-space lines with no file overlap, and no
offending path among `4afe3ebc`'s 390 changed files. The saved frozen-range output is
`wave1c2-01a08953-20260910T032641Z-frozen-whitespace.txt`.
It also records 26 Python paths in `9cf48863` (25 source files plus one identical
copy), historical spell-check code and tracked output paths, and the named commit
messages and changed paths. No spell checker ran.

Public Phonetic MAM was read at fixed commit `7322b665`; the clone's actual HEAD was
`10de797098dab454b5b92e1d4f479fba68f6674b`. Reading the fixed chapter-page Git blobs
reproduced 368 ordinary qamats rows / 370 duplicated chanted words, plus the two
dual-cantillation rows, giving 370/372. The report retains the matched rows and the
Psalms 35 / Proverbs 19 grouping differences. No private scholarly research, survey
regeneration, or sibling-checkout write occurred.

| Changed path | Completed scope |
|---|---|
| `doc/PLAN-remediate-review-findings-2026-09-07.md` | Dated completion, checklist, scope, editorial-status, whitespace, subtest-record, Python-count, and spell-check-output corrections. |
| `doc/review-findings-2026-09-07.md` | Dated Sol-1, count/scope, completion, and retained-versus-reversed status notes, preserving the existing BHS inspection note. |
| `doc/codex-review-findings-2026-09-07-sol.md` | Dated ordinary/dual scope and findings-versus-files corrections. |
| `doc/review-findings-2026-09-08.md` | Disposition rows for work actually completed in Wave 1C2 only. |
| This plan and `doc/PLAN-close-out-review-2026-09-08.md` | Execution evidence and next bounded task. |

All original historical lines and checkboxes are preserved. No tracked Python changed,
so black was unnecessary; no tests were added. No generated HTML, corpus, JSON, image,
behavior, license grant, or sibling checkout changed. D2's deployed copies and the
completed Wave 1B/1C1 edits remain intact. Verification and local commit evidence are
recorded below after the checks complete.

Verification completed 2026-09-09 at `8d6c4df8` plus the Wave 1C2 documentation edits.
The canonical suite ran with `REPOS_ROOT=C:/Users/BenDe/GitRepos`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B py/main_test.py -q -p no:cacheprovider
```

It reported **987 passed, 5 skipped, and 65 subtests passed in 107.46 seconds**.
`verify_wave1c2_01a08953.py suite` saves the full output in
`wave1c2-01a08953-20260910T033358Z-suite.txt`, with invocation, HEAD, return code,
and elapsed time in the adjacent `.json`. V6 ran immediately after the suite and passed:
`v6-runs/20260910T033547Z-wave1c2-after-suite-ab6adb65/`, zero changed locations.

The same verifier's `scope` mode requires only the six named Markdown files, exact
preservation of every original line in all six, Hebrew mark order through
`has_std_mark_order`, and `git diff --check` against the required source. It also
compares the complete frozen and current whitespace path/line/kind sets: they are
identical. The pre-suite scope report is
`wave1c2-01a08953-20260910T033346Z-scope.json`; final scope and commit evidence follow.

**Next execution boundary:** Wave 1C3 covers the remaining named MAS-plan and standards
historical corrections: findings 1, 6.6–6.7, 7.1, 7.2, the finding-7 standards docstring
census, and 16 / N8 with the corresponding 17a merge-hunk record. Target only
`doc/PLAN-post-stress-meteg-page-and-holman-m23.md`,
`doc/PLAN-merge-post-stress-meteg-into-main.md`,
`doc/PLAN-silluq-before-gaya-template.md`, and
`py/repo_util/check_repo_standards.py`, plus completed disposition rows and both plans'
write-back. Verify exact filenames against the approved crosswalk before editing.
Keep original dated records, add the approved State line/dated notes and exact N8
wording, preserve standards behavior, and do not execute those product plans.
Split further at a clean checkpoint if needed to avoid compaction.

Wave 1D owns the remaining record-only dispositions, the complete September 8
accepted-corrections append, and full Wave 1 reconciliation. Wave 1 is incomplete;
Wave 2 and all E items remain pending. The next authorized task uses saved project
`51e16ebd-373a-41f7-833e-9def3ef72b81` with `environment.type = local` after a clean
committed checkpoint. No intermediate integration, push, or automatic archival is due.

Executed 2026-09-09: Wave 1C2 implementation commit
`4cc94bef9251b4677c7ea918875c913e17ca5c31`. The worktree was clean after the commit.
The final pre-commit scope report is `wave1c2-01a08953-20260910T033638Z-scope.json`:
all six changed files are authorized Markdown, every original line is preserved,
Hebrew mark order and changed-line whitespace pass, and the complete frozen/current
offending sets are identical. V6 also passed at both final checkpoints:

1. Before implementation commit: `v6-runs/20260910T033642Z-wave1c2-before-commit-9b8f3e2e/`.
2. At `4cc94bef`, before record commit: `v6-runs/20260910T033742Z-wave1c2-before-record-commit-c552fbf0/`.

All five actual Wave 1C2 V6 runs passed with zero changed locations; no real stop occurred.
The following record-only commit supplies Wave 1C3's required clean source; its hash
and actual successor ID are reported at handoff. Saved project
`51e16ebd-373a-41f7-833e-9def3ef72b81` was rechecked against the exact worktree path
with Git enabled. The successor uses `environment.type = local`. No new decision blocks
Wave 1C3, and no intermediate integration, push, or archival is due.

### Wave 1C3 execution record, 2026-09-09

Codex task `01a08967-0bc1-7f01-b9e0-2776b5403ef2` used saved project
`51e16ebd-373a-41f7-833e-9def3ef72b81` directly at
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`. Source `1b86afa85af9566032eb839d941bac057121da99`
was clean and contained Wave 1C2 implementation `4cc94bef`. The required
back-merge of `main` reported `Already up to date.`; HEAD remained `1b86afa8`.
Ben's Step-5 decision authorized this work and N8 without another approval.

The existing gate `v6_gate_wave1_01a0891a.py` was inspected; its SHA-256 remains
`286e1aa5410ed39b6851c7f94d64476bb826a460909ca27f00de5289eb6e4f9c`.
The immutable nine-page and survey baseline remains `c2f238f2`. Every path below
is under the worktree's `.novc/review-remediation-2026-09-08/`. The command is the
primary interpreter `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B`
followed by that gate's worktree path, `check`, and the recorded `--label`:

1. `wave1c3-before-merge`: `v6-runs/20260910T034220Z-wave1c3-before-merge-87889826/`.
2. `wave1c3-after-merge`: `v6-runs/20260910T034241Z-wave1c3-after-merge-035e6ce6/`.

Both runs passed: nine checkout pages, nine fresh-render pages, zero changed
locations, unchanged pinned survey JSON. The three deliberate failure probes
remain Wave 1A's established proof. No real approval stop occurred.

The bounded script `evidence_wave1c3_01a08967.py`, run with the same interpreter
and `-B` from the worktree root, wrote
`wave1c3-01a08967-historical-evidence.json` and
`wave1c3-01a08967-source-patches.txt`. The reports re-establish:

1. The root/MAS page counts: ten/eight at `15ec6f4d`, eleven/nine at `825cef66`
   and source `1b86afa8`.
2. The historical direct-plan census: eleven plans and eleven State lines at
   `9cf48863`, thirteen/eleven at `38a606e2`, sixteen/fifteen before these edits.
3. The eight MAS blobs at `15ec6f4d`: 440 occurrences of `chanted` on 381 lines.
4. The exact seven non-merge commits from `c73a2ad3` to `a3e3f6eb` in N8.

The edits qualify finding 1's older-plan overclaim, date the ninth-page arrival
beside both older ten/eight descriptions, add the merge plan's executed State
and occurrence-versus-lines note, attribute the original silluq-plan proposals
and correct the baseline claim, replace the standards docstring's false census,
and add the exact N8 notes. The already-landed census correction, silluq State
and dated decisions, and 32-hunk/13-file counts were inspected and retained.
The 17a note identifies the immutable merge-message discrepancy without
recomputing a historical merge. All original dated records remain intact.
The live State above now names Wave 1D as next; its previous Wave 1C2-next wording
is preserved in source commit `1b86afa8`.

Only the four assigned target files, completed September 8 disposition rows,
and both plans' write-back changed. The sole Python change is documentation in
`py/repo_util/check_repo_standards.py`; black at defaults left it unchanged.
No product-plan implementation, classifier, census, generator behavior, license grant,
or sibling checkout changed. All E items remain for the separate editorial phase. Suite,
final scope, V6, and commit evidence follow after verification.

**Next execution boundary:** Wave 1D owns the remaining record-only dispositions,
the complete September 8 accepted-corrections append, and full Wave 1 disposition
reconciliation under this plan's original Wave 1 steps 4-5 and crosswalk. Read the
completed Wave 1A/1B/1C1/1C2/1C3 records and disposition rows before adding anything.
Cover the accepted corrections listed in step 4, exactly enumerate the eight
withdrawn finding-16 items as the rebuttal does, and preserve the separate
`hand-authored whitespace` wording. Reconcile the remaining record-only rows,
including 10/C5, 11.5/17h, 13.1-13.2, 13.4, 13.6-13.7, 15.3, 15.6, 17b-17e,
and 18.1-18.3, against their accepting paragraphs and Ben's decisions. Findings
already completed receive no repeated repair. W2-W4 technical and all E items
remain pending. Do not conduct maintenance or reconstruct a filesystem census.
For 13.6, recheck the complete target set if the named input changed; preserve valid
empty outputs. Attribute unverified language/edition claims without inventing an oracle.

Keep the same checkout and gate, run V6 before and after the required back-merge,
then make only the scoped review/plan record edits. Run the canonical suite and
V6, inspect diffs, update both plans, and commit locally. Mark Wave 1 complete
only after full reconciliation. Split at a clean checkpoint if needed to avoid
compaction. The next fresh task is already authorized after the committed clean
checkpoint, using saved project `51e16ebd-373a-41f7-833e-9def3ef72b81` with
`environment.type = local`. Integration and push occur only after final Wave 4;
no predecessor is automatically archived.

Verification completed 2026-09-09 at `1b86afa8` plus the Wave 1C3 documentation edits:
the canonical suite reported **987 passed, 5 skipped, and 65 subtests passed in
103.43 seconds**. The exact command was
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider`,
from the verified worktree with `REPOS_ROOT=C:/Users/BenDe/GitRepos`.
`verify_wave1c3_01a08967.py suite` saved the full UTF-8 output as
`wave1c3-01a08967-20260910T035210Z-suite.txt`, with invocation metadata in the
matching `-suite.json`, and invoked V6 immediately after the suite. V6 passed at
`v6-runs/20260910T035355Z-wave1c3-after-suite-e1ff4b93/` with zero changed locations.

The same scratch script without `suite` verifies the seven-file scope, preservation
of original historical lines (except the explicitly updated live State), unchanged
standards AST after removing the module docstring, valid Hebrew mark order, diff
whitespace, and all sixteen direct tracked plans' line-3 State entries. Both
whole-skill comparisons are empty. Its latest pre-commit scope evidence is
`wave1c3-01a08967-20260910T035352Z-scope.json`; final gate and commit evidence follows.
No new tests were added. No generated HTML, corpus, JSON, image, or sibling file
changed. The existing 210 whitespace findings remain assigned to Wave 2.

Executed 2026-09-09: Wave 1C3 implementation commit
`26cf55dd354ae2afdeaa8ef352a94278d2372eab`. The worktree was clean after the commit.
The final implementation scope report is
`wave1c3-01a08967-20260910T035453Z-scope.json`. V6 passed before that commit at
`v6-runs/20260910T035458Z-wave1c3-before-commit-01863dd5/`. The following
record-only commit supplies Wave 1D's required clean source; the handoff reports
its hash and the actual successor ID. The saved project's exact path and Git status
were rechecked. No new decision blocks Wave 1D, and no intermediate integration,
push, or automatic archival is due.

At `26cf55dd`, V6 passed before the record commit at
`v6-runs/20260910T035618Z-wave1c3-before-record-commit-8bb4c854/`.
All five actual Wave 1C3 V6 runs passed with zero changed locations and unchanged
pinned survey JSON; no real stop occurred.

### Wave 1D1 execution record, 2026-09-10

Codex task `01a08977-c847-7f41-887f-7b1891162ef1` verified the exact development
checkout `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`, clean at required source
`0ee34bea8ac36f058543d7f757c97f66e6b562cd`, containing `26cf55dd`.
The required back-merge of `main` reported `Already up to date.`; HEAD stayed at
`0ee34bea8`. All edits and verification use that worktree. The primary clone supplies
only `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.

The inspected gate `v6_gate_wave1_01a0891a.py` has SHA-256
`286e1aa5410ed39b6851c7f94d64476bb826a460909ca27f00de5289eb6e4f9c`.
Its immutable nine-page and survey baseline remains `c2f238f2`. Evidence paths below
are relative to the worktree's `.novc/review-remediation-2026-09-08/`. Invoke the
primary interpreter with `-B`, that gate's path, `check`, and the recorded `--label`:

1. `wave1d-before-merge`: `v6-runs/20260910T035943Z-wave1d-before-merge-2ada0d8b/`.
2. `wave1d-after-merge`: `v6-runs/20260910T040030Z-wave1d-after-merge-7495629f/`.

Both passed with zero changed locations, nine checkout pages, nine fresh-render pages,
and unchanged survey JSON. The first check preceded local midnight; execution/write-back
is dated September 10. Wave 1A's three deliberate probes remain the failure-propagation
proof. No real stop occurred.

Under the permitted smaller-task boundary, Wave 1D1 completes original Wave 1 step 4:
the full `Corrections accepted in the review exchange` append, with citations to the
accepting turns, exact finding-16 withdrawals, 17b-17e's historical-message distinction,
D3's three-sentence/two-table correction, and the static-index/CSS planning correction.
The review now has a current State above its preserved September 9 State. A dated D3
disposition records only this completed append. Existing disposition rows are retained.
Only the September 8 review and these two plans change; no tracked Python file changes.

`wave1d_01a08977_evidence.py`, run with the primary interpreter and `-B`, captures bounded
original/accepting Git excerpts in `wave1d-01a08977-accepted-source-evidence.json` and the
exact rebuttal list in `wave1d-01a08977-withdrawn-exact.md`. Its pinned phi-5 HTML at
`38a606e2` confirms three sentences and two tables. These are record checks, not new
language/edition validation. The static filenames are the approved Wave 2 targets
`gh-pages/MAM-for-Sefaria/index.html` and `style-color-scheme-light.css`.

The former current State at source `0ee34bea8` is preserved here:

> State: live 2026-09-09; Waves 1A-1B and 1C1-1C3 complete, Wave 1D next; all waves, P1-P3, E1-E8 and N1-N9 approved as amended; technical unchanged-HTML condition retained.

**Next execution boundary: Wave 1D2.** Complete original Wave 1 step 5: reconcile the
entire crosswalk and all settled decisions against the Wave 1A/1B/1C1/1C2/1C3/1D1
records and dated disposition rows. Add only remaining record-only dispositions,
including 10/C5, 11.5/17h, 13.1-13.2, 13.4, 13.6-13.7, 15.3, 15.6, 17b-17e,
18.1-18.3, and any qualification still required by the full crosswalk. Do not repeat
completed repairs or the accepted-corrections append. Preserve 13.1's overlap guard,
13.2's multiplicity guards, 13.4's fusion invariant and chosen post-silluq interpretation.
For 13.6, recheck all named XML targets if the input changed, keeping valid empty outputs.
Attribute language/edition assertions without inventing an oracle. The reviewer's
415/416 scratch count remains unverified by Codex; no filesystem census is authorized.

Keep W2-W4 technical findings and every E item pending, P2 source/rights-holder
identification deferred, and the rejected blanket cleanup rejected. D6 and N8 are already
complete. Mark Wave 1 complete only after full reconciliation; then define Wave 2's scope
and output contract for its fresh task. Read only governing sections, completed records,
assigned crosswalk rows, and original/accepting paragraphs needed for this reconciliation.
Preserve the historical State text while updating each document's current status.

Wave 1D2 uses the same saved project `51e16ebd-373a-41f7-833e-9def3ef72b81` directly,
with `environment.type = local`, after Wave 1D1's verified clean local commit. Verify the
source path, commit, branch, clean status, and actual task ID. Run the unchanged V6 gate
before and after the required back-merge, the canonical suite, and V6 immediately afterward.
Inspect diffs and complete both plans' write-back before committing and handing off.
No new decision is needed. No predecessor is automatically archived. Integration and
push occur once after final Wave 4, including across intermediate archival.

Verification completed 2026-09-10 at `0ee34bea8` plus Wave 1D1's record edits:
the canonical suite reported **987 passed, 5 skipped, and 65 subtests passed in
108.80 seconds**. The command was
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider`,
from the exact review worktree with `REPOS_ROOT=C:/Users/BenDe/GitRepos`.
`wave1d_01a08977_verify.py suite` saved full output to
`wave1d1-01a08977-20260910T040907Z-suite.txt` and invocation metadata to the matching
`-suite.json`, then ran V6 immediately. V6 passed at
`v6-runs/20260910T041058Z-wave1d1-after-suite-3bcbdb71/`: zero changed locations,
unchanged page membership and pinned survey JSON.

The same script's `scope` mode checks the exact three-path scope against `0ee34bea8`,
preservation of the original historical lines except the explicitly replaced current
remediation State (quoted above), exact reproduction of the eight withdrawals, Hebrew
mark order, diff whitespace, and both whole-skill comparisons. All passed; the pre-suite
report is `wave1d1-01a08977-20260910T040907Z-scope.json`. The actual review/plan diffs
were read. No new tests were added; no tracked Python changed, so black was not required.
No generated HTML, corpus, JSON, image, behavior, or sibling-checkout change occurred.
Final scope, pre-commit V6, and local commit evidence follow.

Executed 2026-09-10: Wave 1D1 implementation commit
`b829a6aaf45d3b92e594da462f0012241c5aece6`. The worktree was clean afterward.
Final implementation scope evidence is `wave1d1-01a08977-20260910T041158Z-scope.json`;
V6 passed before that commit at
`v6-runs/20260910T041201Z-wave1d1-before-commit-c2ba956f/`.
The following record-only commit supplies Wave 1D2's clean required source, containing
`b829a6aa`. The handoff reports its exact hash and the actual successor ID. Saved project
`51e16ebd-373a-41f7-833e-9def3ef72b81` names the verified worktree directly. Wave 1D2
is authorized without a new decision; writing responsibility transfers at dispatch.
Wave 1 remains incomplete. No integration, push, or automatic archival occurred.

At `b829a6aa`, final record scope passed in
`wave1d1-01a08977-20260910T041323Z-scope.json`; V6 passed before the record commit at
`v6-runs/20260910T041327Z-wave1d1-before-record-commit-01692ee6/`.
Every actual Wave 1D1 gate run passed with zero changed locations and unchanged survey
JSON. No real stop occurred.

### Wave 1D2 execution record, 2026-09-10

Codex task `01a08987-8ee2-7372-9104-7cfb7f224d5a` verified the exact development
checkout `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`, clean at required source
`f60aa4260c24cfff726c590613abd72b88fdfd4d`, containing Wave 1D1 implementation
`b829a6aaf45d3b92e594da462f0012241c5aece6`. Command-local `safe.directory` and
authorized escalation resolved sandbox access restrictions. The required back-merge
reported `Already up to date.`; HEAD stayed at `f60aa426`. Every edit and verification
uses that worktree; the primary clone supplies only its absolute venv interpreter.

The inspected gate `v6_gate_wave1_01a0891a.py` retains SHA-256
`286e1aa5410ed39b6851c7f94d64476bb826a460909ca27f00de5289eb6e4f9c` and the immutable
nine-page/survey baseline at `c2f238f2c253d7b00b2d22dc262fe95c81a82401`.
Evidence paths below are relative to the worktree's `.novc/review-remediation-2026-09-08/`.
Run the primary interpreter with `-B`, that gate path, `check`, and the named `--label`:

1. `wave1d2-before-merge`: `v6-runs/20260910T041706Z-wave1d2-before-merge-8f92da85/`.
2. `wave1d2-after-merge`: `v6-runs/20260910T041749Z-wave1d2-after-merge-9e7f3b74/`.

Both passed with zero changed locations, exact checkout and fresh-render membership,
and unchanged survey JSON. Wave 1A's labelled deliberate probes remain the successful
failure-propagation proof. No real stop occurred.

`wave1d2_01a08987_evidence.py`, run with the primary interpreter and `-B`, wrote
`wave1d2-01a08987-20260910T042203Z-evidence.json`. The report preserves bounded pinned
original/accepting excerpts, verifies completed implementation ancestry, and records
every file hash and target in the named XML input set. The reader and all 24
`MAM-simple/xml-vtrad-mam/` files are unchanged from `38a606e2`. Parsing all 32 targets
and applying the real reader reproduces valid empty outputs at these locations:

1. Empty target: `Deut.xml`, `Deut.27.19`.
2. Empty target: `Exod.xml`, `Exod.26.6`.
3. Lone `spi-pe2`: `Exod.xml`, `Exod.33.23`.
4. Lone `spi-pe2`: `Lev.xml`, `Lev.7.21`.
5. Lone `spi-pe2`: `Lev.xml`, `Lev.7.27`.

The report checks the complete named set, without a new page-range assertion or any
unrelated filesystem census. The reviewer's 415/416 scratch-folder account remains
unverified by Codex. Independent language/edition claims remain outside the remediation's
verification; no new oracle or scholarly investigation is implied.

The review's Wave 1D2 rows record only the remaining settled dispositions and limits:
10/C5, 11.5/17h, 13.1/13.2/13.4/13.6/13.7, 15.3, the retained part of 15.4, 15.6,
17b-17g, and 18.1-18.3. Its full crosswalk table assigns every original row to a completed
Wave 1 checkpoint or an explicit later-phase boundary. D1-D11 and P/N outcomes are also
reconciled. Completed repairs and the entire Wave 1D1 accepted-corrections section are
preserved. Wave 1 is complete; no Wave 2 work has started.

Only `doc/review-findings-2026-09-08.md`, this plan, and
`doc/PLAN-close-out-review-2026-09-08.md` change. Their earlier records remain intact;
the review and remediation plan have updated current States with their prior States
quoted in the dated records. The previous remediation State at `f60aa426` was:

> State: live 2026-09-10; Waves 1A-1B, 1C1-1C3 and 1D1 complete; Wave 1D2 owns the remaining reconciliation; all waves, P1-P3, E1-E8 and N1-N9 approved as amended; technical unchanged-HTML condition retained.

**Next execution boundary: Wave 2.** A fresh task uses saved project
`51e16ebd-373a-41f7-833e-9def3ef72b81` directly with `environment.type = local`, at the
exact worktree above and the verified clean source commit reported at handoff. Verify
the actual task ID, checkout, branch, HEAD, status and required ancestry before reading.
Inspect the unchanged gate and immutable baseline; run V6 before the required back-merge
and immediately afterward. No additional approval is needed under Ben's Step-5 decision.

Wave 2 covers finding 2's complete whitespace set, 5.1b's Holman RTL declarations and
14.2's existing MAS lint membership coverage. Read its full section below and V2/V3/V6,
the governing approval/checkout/handoff rules, and only the assigned original/accepting
paragraphs. Save before-edit baselines and run the real product/Holman commands before
source edits. Trace the Unicode-name separators, AJF CSV boundaries, both Holman pages
and declared/rendered MAS filename sets. The MAM-for-Sefaria index and
`gh-pages/MAM-for-Sefaria/style-color-scheme-light.css` are static direct-edit targets.
Re-measure the complete offending set; Wave 1C2 preserved the original 210 findings in
193 files. Do not infer repair from a clean-tree diff check.

Wave 2's output contract allows only the measured final-line/trailing-space removals,
Holman direction attributes, source/support-copy repairs and the existing membership
lint, plus records. Preserve corpus text, internal spacing, parsed CSV fields apart from
the specifically intended trailing-space removal, Holman cell text/order and issue
metadata. No MAS HTML, survey JSON, XML, parsed corpus, downloaded input or sibling output
change is authorized. Compare all outputs and reproduce the repaired output with the
required second generation. Format touched Python, verify support copies, run the canonical
suite and V6 immediately afterward, write both plans' records and commit locally. Split
at a precise clean boundary if necessary to avoid compaction; do not declare Wave 2
complete with outstanding items.

Waves 3-4 and every E item remain pending. All E items execute in the separate editorial
phase after Wave 3 technical verification, under its explicit output contract. P2's
source/rights-holder identification stays deferred. A real changed byte/membership
difference or failed/incomplete V6 stops the entire remediation for Ben's renewed decision.
No cleanup, source refresh, survey regeneration, mega, issue communication, integration,
push or automatic archival belongs to Wave 2. There is one integration and push after
final Wave 4, including across intermediate archival. Transfer writing responsibility
only after the committed clean checkpoint; stop editing at dispatch.

Verification completed 2026-09-10 at `f60aa426` plus the Wave 1D2 record edits.
The canonical suite reported **987 passed, 5 skipped, and 65 subtests passed in
102.78 seconds**, using
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider`
from the exact review worktree with `REPOS_ROOT=C:/Users/BenDe/GitRepos`.
`wave1d2_01a08987_verify.py suite` saves full output in
`wave1d2-01a08987-20260910T042803Z-suite.txt` and invocation metadata in the matching
`-suite.json`, then invokes V6 immediately. The passing post-suite evidence is
`v6-runs/20260910T042947Z-wave1d2-after-suite-28e2f03f/`.

The new scratch verifier's default mode uses Wave 1D2's source and exact three-file
scope. It checks every historical line except the replaced-and-quoted current States,
the byte-for-byte preservation of Wave 1D1's accepted-corrections section, exact matching
of all 52 original crosswalk row labels, Hebrew mark order, changed-line whitespace and
both whole-skill comparisons. All checks passed in
`wave1d2-01a08987-20260910T042756Z-scope.json`; final scope and pre-commit V6 evidence
follow below. The actual review/plan diff was read. No tracked Python changed, so black
was not required; no new tests or generated-artifact changes occurred. No real V6 stop
occurred. Implementation and final record commits are recorded after their hashes exist.

Executed 2026-09-10: Wave 1D2 implementation commit
`f7360667f2cd00ea5453757c81921b31b4b2d859`. The worktree was clean afterward.
Final implementation scope passed in `wave1d2-01a08987-20260910T043045Z-scope.json`;
V6 passed before that commit at
`v6-runs/20260910T043054Z-wave1d2-before-commit-ce5a4167/`.
The following record-only commit supplies Wave 2's clean required source, containing
`f7360667`. Its full hash and actual successor ID are reported at handoff. Saved project
`51e16ebd-373a-41f7-833e-9def3ef72b81` was verified as the exact review worktree with
`isGitRepository=true`; the successor uses that path directly with `environment.type = local`.
Wave 1 is complete and Wave 2 is authorized without another decision. Writing responsibility
transfers at dispatch. No integration, push or automatic archival occurred.

At `f7360667`, record scope passed in
`wave1d2-01a08987-20260910T043230Z-scope.json`; V6 passed before the record commit at
`v6-runs/20260910T043233Z-wave1d2-before-record-commit-23c37abc/`.
Every actual Wave 1D2 gate run passed with zero changed locations and unchanged survey
JSON. No real stop occurred.

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
the change before staging; do not silently include it or discard another task's work. Any
MAS HTML difference triggers the mandatory V6 stop instead of this explain-before-staging rule.

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

### Wave 2 partial execution record, 2026-09-10

Codex task `01a08999-29a0-7b60-aa25-1454c9b49084` verified the exact checkout
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`, clean at required source
`efeb9fd44c9ebd244a81a4d54377aa04de2264df`. The required merge of `main` reported
`Already up to date.` Ben's Step-5 approval authorizes the original Wave 2 work.
Every script, edit, generation, validation and commit uses this worktree, with the
primary clone's absolute interpreter. No primary fast-forward or push occurred.

The unchanged `v6_gate_wave1_01a0891a.py` has SHA-256
`286e1aa5410ed39b6851c7f94d64476bb826a460909ca27f00de5289eb6e4f9c` and verifies the
fixed nine-page and survey-JSON baseline at `c2f238f2c253d7b00b2d22dc262fe95c81a82401`.
The before/after-merge evidence is
`v6-runs/20260910T043609Z-wave2-before-merge-a7005410/` and
`v6-runs/20260910T043807Z-wave2-after-merge-1448a5ee/`, relative to
`.novc/review-remediation-2026-09-08/`. Both passed with zero changed locations.
All actual Wave 2 V6 checks have passed; no real stop occurred.

The independently written scratch verifier is
`.novc/review-remediation-2026-09-08/verify_wave2_01a08999.py`. Run it with the primary
interpreter and `-B`. Its `baseline` mode, run before edits, saved complete bytes for
930 named product/support/input files, totaling 182,324,171 bytes, under
`.novc/review-remediation-2026-09-08/wave2-01a08999/baseline/`. The adjacent
`baseline.json` records hashes, the complete offending path/line sets and Holman cells.
It independently reproduced 210 findings in 193 distinct files: 189 blank final lines
and 21 trailing-space lines, with no overlap. This is an output verification inventory,
not the unrelated 415/416 scratch-folder census, which remains unverified by Codex.

`trace_wave2_01a08999.py` and `producer-trace.json` trace every blank final line:

1. `MAM-simple/misc/unicode-names-vtrad-bhs/`: 24 files.
2. `MAM-simple/misc/unicode-names-vtrad-mam/`: 24 files.
3. `MAM-simple/misc/unicode-names-vtrad-sef/`: 24 files.
4. `MAM-simple/py-examples-out/sefaria/misc/unicode-names/`: 39 files.
5. `MAM-for-Sefaria/misc/unicode-names/`: 39 files.
6. `MAM-for-Sefaria/misc/unicode-names-ajf/`: 39 files.

The core exporter calls `write_bkg_in_un_fmt` through `_finish_one_book_group`;
the Sefaria/AJF exporter and example call it through `_do_one_book_group` in
`mb_sefaria/mam4sef_or_ajf.py`. `_write_callback` in `mb_misc/write_utils.py` now
emits the blank separator before each verse after the first. `_write_verse_un` no
longer emits a blank line after the last verse. Every affected output equals its
baseline with exactly one final LF removed; internal separators and one terminating
newline remain. No XML or JSON content changes.

`write_utils_sef_or_ajf.py` now trims ASCII space/tab only from the final CSV field
at the record boundary. The baseline has 3,509 whitespace-ending fields, of which
only nine are final fields; all other fields remain unchanged. Full byte comparisons
and parsed comparisons of every saved CSV establish only the nine measured removals,
preserving quoting, field counts, verse text, internal whitespace and mark order.
`repair_static_wave2_01a08999.py` removed the measured 11 HTML and one CSS trailing
spaces from the named static files; `static-repair.json` records those changes.

The pre-edit `generate before` run used all five commands specified in Wave 2,
including the example's exact `MAM-simple` cwd, and V6 immediately after each command.
The copier's recursive targets were first resolved and checked within the declared
worktree child directory; `before-copier-targets.json` records them. The full comparison
identified these pre-existing differences, saved separately under `pre-edit-generation/`:

1. `MAM-simple/py-examples/mb_cmn/paths.py` receives the existing documentation from
   source commit `b865b7c8fd9cb95e6a3a850fadcb9f852299c2a4`. This is an exact declared
   support copy, included with the required copier output. The source is unchanged.
2. `gh-pages/holman/table_data_findings_suppressed.html` changes one background-link
   label from `Meteg after the primary stress` to `Meteg after the stress`.
   `rt_suggestion_context._POST_STRESS_METEG` uses the existing
   `site_data.POST_STRESS_METEG_TITLE`. No source wording was edited in Wave 2.
   The exact generated label update exceeds Wave 2's original direction-only contract;
   Codex asked Ben whether to include it or defer Holman to the editorial phase.
   No response has been recorded. The label difference is not a MAS HTML difference,
   and no V6 baseline or exception changed.

The existing `test_every_page_is_present` now compares `_PAGE_FNAMES` with both actual
`post-stress-meteg*.html` files and the `POST_STRESS_METEG` filename constants in
`author_site.site_data`. Missing-page failure and the forbidden-word scan remain.
`check_lint_wave2_01a08999.py` proves missing, additional rendered and additional declared
pages fail, using only disposable scratch fixtures; `membership-probes.json` retains
the results. No new tracked test or exception registry was added.

The Holman draft uses `contains_hebrew_char` at the producing cells. The suppressed
page's 32 comparison-name and 17 comparison-symbol-value cells come from
`rt_comparison_table._comparison_row_html`; the active page's separate summary cell
comes from `rt_summary._summary_row_html`. V3 uses `HTMLParser` with an inherited
direction stack and correct void-element handling. Both pages now have zero offenders.
All 724 active-page cells and 578 suppressed-page cells retain their text and order;
the proposed output differs only by 50 direction attributes and the pending label.
Holman data, issue metadata, CSS and JavaScript are byte-identical to the baseline.

`generate repaired` regenerated the products. The Holman command failed opening the
suppressed output with Windows `OSError: [Errno 22] Invalid argument`; its log is
`20260910T044759Z-repaired-holman.txt`. V6 passed immediately after the failure at
`v6-runs/20260910T044907Z-wave2-after-holman-failure-c012023f/`. The isolated `holman`
retry succeeded (`20260910T044931Z-holman-retry.txt`), followed by a passing V6.
The failed generation was not called a passing verification or a deliberate probe.

`draft-verification.json` records zero whitespace findings, nine changed CSV fields,
and zero Holman RTL omissions. Its Holman comparison explicitly treats the exact label
update as a pending proposal; a draft pass is not approval or Wave 2 completion.
All changed tracked Python passed black at defaults; both whole-skill Git comparisons
with the worktree's canonical directory and the live Claude/Codex directories exited 0.
The canonical suite, with `REPOS_ROOT=C:/Users/BenDe/GitRepos`, passed **987 tests,
5 skips and 65 subtests in 111.22 seconds**. Full output and command/HEAD/time metadata
are `20260910T045041Z-suite.txt` and `.json`; V6 ran immediately afterward, with its
log at `20260910T045233Z-suite-v6.txt`. Repeat-generation and commit evidence follow.

Repeat generation completed: `generate repeat` reran every required product/Holman
command and V6 after each. The second `draft` comparison found all 930 saved paths
byte-identical to `draft-hashes.json`; no additional output diff occurred. The repeat
logs run from `20260910T045251Z-repeat-copy.txt` through
`20260910T045322Z-repeat-holman-v6.txt`. `draft-verification.json` preserves the full
post-repeat comparison. This proves reproducibility of the draft; it does not approve
the pending label update. Final scope and partial-commit evidence follow.

The previous current State, preserved from `efeb9fd4`, was:

> State: live 2026-09-10; Wave 1 complete through Wave 1D2 reconciliation; Wave 2 is next and has not started; all waves, P1-P3, E1-E8 and N1-N9 approved as amended; technical unchanged-HTML condition retained.

Executed 2026-09-10: partial implementation commit
`ce833525f517eab97958141f7380a2da2267656e` includes the 193 whitespace files,
three support copies, three producing-source/lint files and three records: 202 paths.
The full working-tree scope is 206 paths. Exact absolute paths and the pending/committed
split are in `wave2-01a08999/20260910T045822Z-scope.json`; the readable inventory is
`wave2-01a08999/changed-paths.md`, relative to the remediation scratch directory.
`scope_wave2_01a08999.py` verifies all 44 support copies, exact changed-path membership,
preservation of all prior record text apart from the quoted current States, Hebrew mark
order and diff whitespace. V6 passed immediately before the partial commit at
`v6-runs/20260910T050034Z-wave2-before-partial-commit-05abf168/`.

Staging initially found an empty `index.lock` last written at 00:42 local. A Windows
process query found no running Git process; the index was empty and HEAD remained
`efeb9fd4`. The stale zero-byte lock was preserved as
`wave2-01a08999/stale-empty-index-lock-20260910T0500Z`, after which staging and commit
succeeded. No source work or Git history was discarded.

The remaining uncommitted paths are exactly the active and suppressed Holman HTML
pages and `py/py_render/rt_comparison_table.py` / `py/py_render/rt_summary.py`.
The worktree is deliberately not a clean handoff checkpoint. A following record-only
commit records this implementation hash; the final response supplies its exact head.

**Next execution boundary:** resolve the exact Holman label question with Ben, then
finish Wave 2's applicable verification, records and local commits before any successor.
The whitespace and page-lint checkpoint does not complete Wave 2. All E items remain
for the separate editorial phase after Wave 3 technical verification unless Ben explicitly
amends the contract for this label. P2 source/rights-holder identification stays deferred.
No new task, archival, integration or push occurs while the decision is pending.

### Wave 2 completion record, 2026-09-10

Ben's exact decision on 2026-09-10 was: "Yes, I authorize the dropping of \"primary\"
from that label." The selected question named `Meteg after the primary stress` to
`Meteg after the stress`. This approval adds only that existing generated background-link
change in `gh-pages/holman/table_data_findings_suppressed.html` to Wave 2's output
contract. The approval does not change V6, its fixed baseline, or the E-item boundary.
The exact decision is saved as `wave2-01a08999/holman-label-approval.json` under
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/.novc/review-remediation-2026-09-08/`.

Codex resumed task `01a08999-29a0-7b60-aa25-1454c9b49084` at partial-record commit
`059511e856933a7274e8e23af35bff622cbbd14f`, with exactly the four recorded Holman
source/page paths uncommitted. The checkout remains
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`. V6 passed on resumption at
`v6-runs/20260910T113422Z-wave2-approved-label-resume-9acb3e06/` with all nine
checkout pages and fresh renders unchanged. Survey JSON remains unchanged.

The real-file command `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B
.novc/review-remediation-2026-09-08/verify_wave2_01a08999.py repaired`, run from the
review worktree, passed the approved full-byte comparison. Its `repaired-verification.json`
records zero whitespace findings, exactly nine changed CSV final fields, and zero Holman
RTL omissions. All 1,302 cell texts and their order are preserved; the only Holman byte
differences are the 50 required direction attributes and the approved label.

`final_scope_wave2_01a08999.py`, run with the same interpreter and working directory,
compares all 930 approved output hashes against the tested, twice-generated draft and
compares the entire technical diff against the saved post-verification patch. This
establishes that the prior canonical suite result, **987 tests, 5 skips and 65 subtests
in 111.22 seconds**, and the repeat-generation result apply to the approved implementation.
No technical edit was needed after approval, so the suite and generators were not rerun.
The same final check verifies all 44 support copies, the exact 206-path Wave 2 scope,
record preservation against both `efeb9fd4` and `059511e8`, Hebrew mark order and
`git diff --check`. The evidence is `wave2-01a08999/final-scope.json`; the absolute
path inventory is `wave2-01a08999/changed-paths.md`. Final commit evidence follows.

The previous current State at `059511e8`, preserved here, was:

> State: live 2026-09-10; Wave 1 complete; Wave 2 whitespace and page-lint repairs verified, Holman draft awaits Ben's decision on a pre-existing generated label difference; Wave 2 completion pending; technical unchanged-HTML condition retained.

Wave 2 is complete. The next authorized phase is Wave 3 technical work, using saved
project `51e16ebd-373a-41f7-833e-9def3ef72b81` with `environment.type = local`
at the exact review worktree. Create the fresh task only after a clean local checkpoint,
and put that checkpoint's full hash in its prompt. Transfer writing responsibility at
dispatch. E1-E8 stay in the separate editorial phase; P2 source/rights-holder identification
remains deferred, and the 415/416 scratch count remains unverified. No primary integration,
push or automatic archival occurs here; integration remains scheduled after final Wave 4.

Executed 2026-09-10: Holman completion commit
`f709e0b87d6f8b0e82250374263a00a7b1150cb3` contains the four remaining source/page
paths and the three completion records. The worktree was clean after that commit.
Together with whitespace/lint implementation `ce833525f517eab97958141f7380a2da2267656e`
and partial-record commit `059511e856933a7274e8e23af35bff622cbbd14f`, the local
history contains all completed Wave 2 work. Final scope verification passed at
`wave2-01a08999/20260910T113815Z-final-scope.json`, and V6 passed immediately before
the Holman commit at
`v6-runs/20260910T113855Z-wave2-before-approved-holman-commit-363246e9/`.
The following record-only commit supplies the clean required source for Wave 3's
prompt; the task-creation result and final response record the actual successor ID.

## Wave 3 — select unannotated forms, preserve displayed marks, and validate annotations

Preconditions: Wave 2 complete; its own approval and execution record are present. Ben's
2026-09-09 approval of the discussed technical work is conditional as stated above. Establish
V6 before any technical edit. Check both the checkout and a fresh scratch render against the
fixed reviewed HTML baseline; an initial difference stops remediation just as a later
difference does. Record the actual starting HEAD, input hashes, and every input's provenance.

1. Trace `_hebrew_cell`, `mam_form or chanted_word` fallbacks, comparison/prose inputs,
   `_attach_mam_forms`, and `_as_mam_would_write_it`'s matching callers. Where a Phonetic MAM
   snapshot form is sufficient, use the first `rep` form when present, otherwise the first
   unannotated `fva` form, rather than reconstructing that spelling by deletion. Retain
   current MAM forms and the BHS-labelled source where those are the intended editions.
   Establish which matching transformations remain necessary; do not keep or remove every
   use merely by rule. A change affecting record matching requires differential evidence
   that selected records and the complete existing survey are unchanged. If that evidence
   requires private survey regeneration or another run outside this plan's scope, stop for
   Ben's decision before changing the matching path. Do not alter JSON to accommodate it.
2. Remove comparison normalization from rendering selected display text. Preserve its Hebrew
   marks; retain only the existing `hpu.NU_GMAQ` to `MAQAF` display conversion. This changes
   the technical design without predicting a change in the current page bytes. No new marks,
   corpus rule, normalization policy, or edition substitution are introduced.
3. Revise annotation validation at the same time. Cover all nine MAS pages and the routes
   that supply their displayed forms, including authored literals and fallback paths.
   Detect unintended Phonetic MAM annotations using source/context evidence, and report the
   source and output location without deleting characters. Preserve valid source upper/lower
   dots and VARIKA; neither a blanket character ban nor disabling the existing guard is an
   adequate replacement. Retain the existing normal claim checks. Correct an accidentally
   annotated literal explicitly only after applying the conditional-approval stop whenever
   the finding implies changed current HTML; no automatic sanitizer hides the defect.
4. Render all nine pages from the same tracked JSON into scratch output and run V6 immediately.
   Compare every helper result with its selected source, permitting only the declared maqaf
   conversion. Use an exhaustive mark-preservation differential probe and a mechanical
   annotation check, with legitimate source marks distinguished from annotated inputs; no
   hand-picked verse fixture or blanket mark deletion. The original simulation measured
   only step 2's display behavior; it does not validate steps 1 or 3.
5. After the scratch result passes, run the normal authored-site command below and V6 again.
   Black on touched Python, V1/V3, the existing MAS lint, and the canonical suite must pass.
   Check V6 after validation and immediately before committing. Survey JSON, classifier
   behavior, candidate selection, numerical claims, images, and all generated/public HTML
   must remain unchanged by this technical work. An unexpected non-MAS HTML diff also stops
   technical remediation; the authored command generates the index and Unicode-proposals
   page as well. Do not open a browser or start a server.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_authored.py gen-site --trust-surveys
```

Expected tracked changes for the technical phase: bounded producing/validation Python and
necessary documentation of that behavior, mechanical/differential checks, and execution
records. No generated/public HTML, survey JSON, manuscript image, or sibling-tree changes.
Record the actual touched source paths, rather than assuming a display-only helper edit
implements the revised remedy. Any broader source proposal requires a separate disposition.

Do not apply E items during this technical phase. A later editorial phase requires Ben's
explicit item dispositions; HTML-changing items additionally require his explicit revised
output contract, concrete expected diffs, and a distinct baseline after the technical result
has passed. Until that decision, leave the pending items pending and do not render their
proposed HTML. The technical approval alone does not permit continuing into editorial work.

Execution record: **Not started.** Record the conditional approval, starting and final HEADs,
unannotated-form and matching decisions, source/validation coverage, baseline and final input
hashes, all-nine-page byte comparisons, V6 command and result, and suite output. Record any
failed check and Ben's subsequent explicit decision; a later pass must not erase a stop.
Commit completed, passing technical work locally with its record. No integration or push.
Record separately approved editorial work separately if Ben later authorizes that phase.

### Wave 3 preparation record, 2026-09-10

Codex task `01a08b1f-acc9-7e22-984d-b1f1333f3f38` verified the exact development
checkout `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`, clean at required source
`d4068b79066e9f0f741fc3c1a099980b8e969f0f`. The required merge of `main` produced
`32969e0e86c18d0ca577f86fde38a3b5479f269f`, with second parent
`f92c061c21eb76ffc00a6347e53fcb04e65c02a6`. Its only incoming path was
`doc/scan-pages.md`; it changed no MAS source, input or HTML. Primary integration and
push did not occur.

Ben's Step-5 technical approval, its unchanged-HTML condition, and the separate
editorial-phase boundary remain in force. The smaller-task rule under Wave 1 permits
this preparation checkpoint and fresh implementation task. Wave 3's original
"Execution record: Not started" above is retained as history: preparation is now
complete, but technical implementation and all E items remain pending.

The previous current State, preserved from `d4068b79`, was:

> State: live 2026-09-10; Waves 1-2 complete; Ben approved the exact Holman label change; Wave 3 technical work is next; technical unchanged-HTML condition retained.

The existing V6 script was inspected unchanged and its SHA256 matched
`286e1aa5410ed39b6851c7f94d64476bb826a460909ca27f00de5289eb6e4f9c`.
The fixed baseline remains `c2f238f2c253d7b00b2d22dc262fe95c81a82401`.
V6 passed on the initial checkout, immediately after the back-merge, after the source
trace's scratch render, and after the matching probe. Every comparison found the nine
pages unchanged in bytes and membership, with unchanged pinned survey JSON. No real
V6 stop occurred and no deliberate gate probe was repeated.

All preparation scripts and detailed evidence are under
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/.novc/review-remediation-2026-09-08/wave3-01a08b1f/`.
The interpreter for every command below is
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`; the working directory is
the exact review worktree. Run a named scratch script with `-B` and its path. The
scripts read source data and write only ignored evidence. Neither `_scan`, `_one_verse`,
the classifiers nor `build_survey` was called by the source or matching probe.

1. **Source selection: `inspect_sources.py`.** The read-only inspection covered all
   39 expected snapshot JSON files, with exact filename membership checked against
   `_bb_of_stem`. The inspected MAM-private checkout was
   `55252b834d28a6c241e75758aff5d15836621f56`; every snapshot file's bytes equal its
   Git blob at the plan's technical-source pin
   `e21306165707f9500ea19540d04af3e1918b563d`. The technical README and exploration
   were read at that pin. `snapshot-form-differential.json` records every input hash;
   `snapshot-form-provenance.json` records every form's source file and JSON pointer.
   No private source was refreshed or regenerated.
2. **Complete snapshot differential.** The source contains 263,320 records with `fva`:
   122,555 select first `rep`, and 140,765 select first unannotated `fva`. Every selected
   form lacks the snapshot's MASORA CIRCLE and UPPER DOT annotations. Both join-key
   equality and meteg-count equality hold for every raw/selected pair. The selected
   form, with only the gray-maqaf conversion, equals the old matching string for
   262,650 records. All 670 differences are VARIKA, which the selected source form
   retains and the old helper deletes. No raw full form has LOWER DOT; 113 have a
   gray-maqaf placeholder. There are zero ambiguous mappings from `(bcv, first fva)`
   to the selected form, and zero even when keyed by first `fva` alone. These are
   measurements of this snapshot, not a general source-schema guarantee.
3. **Matching necessity: `probe_matching.py`.** For every VARIKA-affected source
   record, the probe compares `_settle` against combined current MAM, cant-alef and
   cant-bet: 2,010 comparisons. It also compares `_next_mam_context` over every
   current-form/native-punctuation context in each affected numbered verse: 9,377
   comparisons. Using the selected form without the matching-only VARIKA transformation
   changes 81 settlement results and four next-context results in those domains.
   Re-attaching both ways to every complete serialized attachment record gives 786
   comparisons and five changed records. The changed serialized records are all under
   `diagnostics/sharing_a_letter_with_a_non_stress_marking_accent`: indices 76, 82,
   87, 92 and 93. Indices 82 and 87 lose a selected MAM form; indices 76, 92 and 93
   change `mam_form_matched_by`. These are counterfactual scratch results, not changed
   survey JSON or a V6 failure. `matching-differential.json` preserves the full results.
4. **Compatible matching expression.** Selecting first `rep` or first unannotated
   `fva`, then applying the existing VARIKA removal and gray-maqaf conversion for
   matching only, equals `_as_mam_would_write_it` for every full snapshot form. This
   establishes why the VARIKA transformation must remain in matching. It does not
   authorize deleting VARIKA from displayed text, changing `_join_key`, replacing
   classifier inputs, or substituting snapshot spelling for current MAM. The probe
   does not regenerate or compare a complete new survey. The implementation task must
   establish the plan's complete-survey invariance requirement for its actual data
   flow before changing matching; it must stop for Ben if that requires prohibited
   survey regeneration. Do not describe the bounded probe as that completed check.
5. **Displayed routes: `inspect_sources.py`.** The normal nine-page renderer, with
   normal checks and traced helpers, made 1,017 `_hebrew_cell` calls on 674 distinct
   input strings. Each helper result equals `wrap_hebrew_runs` of its selected input
   with only the permitted gray-maqaf conversion. The per-page counts reproduce the
   earlier nine-row simulation table exactly, and all nine fresh HTML files equal
   the fixed baseline. `display-route-trace.json` records each call, caller, source
   line, matching survey pointers and output page. Calls bypassing `_hebrew_cell`
   include `_mam_post_silluq_statement` twice, `_post_silluq_footnote` once,
   `_type_2_type_3_footnote` once, and `_para` four times. These routes must participate
   in annotation validation too.
6. **Source distinctions and fallback coverage.** The trace's forms without an exact
   survey-string pointer comprise joined dual-cantillation forms, the BHS-labelled
   form selected from UXLC with the existing WLC equality assertion, and the authored
   L-1/L-2/next-word constants for 2 Chronicles 8:11. Preserve those source distinctions
   and interpretations. Both `mam_form or chanted_word` fallback sites remain latent
   on current displayed inputs. The survey has 797 objects with a `mam_form` field,
   including two null forms in diagnostics; neither reaches the traced display helper.
   The 1,578 occurrences counted for the specifically inspected `chanted_word`,
   `next_chanted_word` and `preceding_chanted_word` fields all have snapshot mappings;
   22 differ from the old matching string because of VARIKA. This field census is not
   a census of every string or annotation occurrence in the JSON.

The traced source paths are `py/author_site/post_stress_meteg.py` and
`py/accgram/post_stress_meteg.py`, with their existing MAM-simple, UXLC and WLC readers.
No tracked Python was changed. The future implementation must handle unannotated
snapshot selection, both fallback sites, all matching callers, every displayed route,
and all nine pages' annotation validation together. In particular, replacing the
single-page guard with a blanket UPPER DOT ban would reject legitimate MAM forms.
Source and context must distinguish those forms from snapshot annotations and
accidentally annotated literals, with source/output locations in diagnostics. The
exhaustive mark-preservation probe and mechanical annotation-coverage checks remain
implementation work, as does normal `gen-site --trust-surveys` generation with the
all-public-HTML byte contract.

Preparation verification completed 2026-09-10. `run_checks.py` captured the canonical
`py/main_test.py -q -p no:cacheprovider` invocation with
`REPOS_ROOT=C:/Users/BenDe/GitRepos`: **987 passed, 5 skipped, 65 subtests passed in
121.00 seconds** at merged HEAD `32969e0e`. Full output is
`wave3-01a08b1f/20260910T115453Z-preparation-suite.txt`; command, environment, HEAD,
exit code and elapsed time are in `wave3-01a08b1f/preparation-suite.json`. V6 ran
immediately afterward and passed at
`v6-runs/20260910T115655Z-wave3-after-preparation-suite-01a08b1f-090b4639/`.

`check_preparation_scope.py` independently verifies that only the three record paths
changed, all historical lines remain in order, each replaced State is preserved as a
quotation, and the entire accepted-corrections section is byte-identical as UTF-8 text.
Hebrew mark order and `git diff --check` pass. V1 reports 11 deploy-root pages, nine
MAS pages with exact actual/declared membership, and 16 direct plans with State lines.
V3 reports zero RTL omissions in the unchanged Holman pages, with 578 and 724 cells
respectively. The full report is `wave3-01a08b1f/preparation-scope.json`. No tracked
Python changed, so black was not applicable. No normal authored-site generation was
run for this record-only checkpoint; the technical implementation task still owes that
command and its all-public-HTML comparison.

V6 also passed at the following evidence directories under the remediation scratch root:

1. Initial: `v6-runs/20260910T114251Z-wave3-initial-01a08b1f-b3e3faab/`.
2. After merge: `v6-runs/20260910T114500Z-wave3-after-backmerge-01a08b1f-c51d711a/`.
3. After source trace: `v6-runs/20260910T115021Z-wave3-after-source-trace-01a08b1f-c1fe63ba/`.
4. After matching probe: `v6-runs/20260910T115447Z-wave3-after-matching-probe-01a08b1f-16f0ca76/`.
5. After record-scope validation: `v6-runs/20260910T115932Z-wave3-after-preparation-scope-01a08b1f-4ba4ea9f/`.

The exact V6 invocation uses the unchanged script with `check --label <unique-label>`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B .novc/review-remediation-2026-09-08/v6_gate_wave1_01a0891a.py check --label wave3-before-preparation-commit-01a08b1f
```

Executed 2026-09-10: preparation commit
`cef81ec984ca3a8772c9264608a572b2f4a7ab0e` contains the three progress records.
The worktree was clean afterward. V6 passed immediately before the commit at
`v6-runs/20260910T120203Z-wave3-before-preparation-commit-01a08b1f-cbda7ddb/`.
The following record-only commit preserves this hash and supplies the fresh technical
implementation task's required clean source. The final response and task-creation result
record the exact handoff head and actual successor ID. Wave 3 remains incomplete.

Only this plan,
the close-out plan and the September 8 review receive progress records. Their historical
content, including the complete accepted-corrections section, remains intact. After a
clean committed checkpoint, start a fresh Wave 3 technical implementation task directly
in the same saved project. E1-E8 remain for a separate fresh editorial task after the
technical phase passes and is committed. P2 source/rights-holder identification remains
deferred, and the 415/416 scratch count remains unverified. There is no new approval
request in this preparation record. Integration and push remain scheduled once, after
final Wave 4.

### Wave 3 technical implementation record, 2026-09-10

The preceding current State is preserved here as a historical preparation checkpoint:

> State: live 2026-09-10; Waves 1-2 complete; Wave 3 source-and-matching preparation complete, technical implementation pending; technical unchanged-HTML condition retained.

Codex task `01a08b34-edc5-74b3-9c56-b10d169ae862` verified the exact checkout
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`, clean at required source
`67d180ae4aca456c135862c4f19b391c80851f3d`. The required back-merge produced
`c36f5baa3eed464877f0b0c9ac34b9b6dedf268a`, with second parent
`5e61a2d1b5af1803ec4390a411bcbcf1b48bff86`. Incoming changes were confined to
`doc/meteg-after-silluq-koren-lookup-candidates.md` and
`in/meteg_after_silluq_koren_readings.json`. V6 passed before and immediately after
the merge. No primary integration or push occurred.

The technical implementation, source differential, complete existing-survey
comparison, fallback checks and normal generation have passed. Final suite and local
commit evidence are recorded below after completion. Ben's original conditional
approval remains in force; E1-E8 have not been applied.

The technical source changes are:

1. `py/accgram/post_stress_meteg.py` selects the snapshot's first `rep`, otherwise its
   first unannotated `fva`, through a lazy source index. The index checks the complete
   book-file set, reports source file/JSON pointers, and refuses ambiguous raw-to-selected
   mappings or an annotated `fva` lacking `rep`. The classifier still receives raw
   `fva`; record construction, candidate selection, both matching callers, the attachment
   logic and summary construction retain their executable bodies. Matching retains
   VARIKA removal and gray-maqaf conversion; display retains only gray-maqaf conversion.
   An actual display fallback requires the
   snapshot to be available; ordinary trusted rendering, whose displayed records all
   have MAM forms, needs no private source.
2. `py/author_site/post_stress_meteg.py` preserves all selected display marks, with only
   the existing gray-maqaf conversion. Both `mam_form or chanted_word` sites now select
   the snapshot's unannotated form when the MAM form is absent. Current-MAM selection,
   the dual-cantillation routes, the BHS-labelled UXLC form with its WLC equality check,
   and the authored 2 Chronicles interpretation constants remain in place.
3. `py/author_site/post_stress_meteg_annotations.py` validates complete output pages,
   including prose, cells, literals, fallback forms, inline compositions and attributes.
   MASORA CIRCLE or UPPER DOT needs an exact independently sourced Hebrew form, rather
   than failing because of the codepoint alone. Current-MAM forms from all cantillation
   projections and the explicitly supplied comparison source provide that evidence.
   Every expected MAM book input is required. LOWER DOT and VARIKA remain intact.
   Survey pointers and Python literal lines locate rejected inputs; those inputs do not
   authorize themselves. The validator reports output path, line, column, context and
   Unicode names, and never repairs displayed text. All normal claim checks remain active.
4. `py/tests/test_post_stress_meteg_annotations.py` adds a mechanical check of every
   actual MAS HTML page through that source/context validator. The existing MAS
   terminology/membership lint remains active. No example-based verse test was added.

Evidence is under
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/.novc/review-remediation-2026-09-08/wave3-01a08b34/`.
Every command below uses the absolute interpreter
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`, with the working
directory at the exact review worktree. Run the named scratch scripts with `-B`.
The preparation evidence under `wave3-01a08b1f/` was read and preserved; its source
trace and VARIKA-necessity probe were not repeated.

1. **Before changing matching:** `prove_matching_invariance.py` produced
   `matching-invariance.json`. All 263,320 prepared source records have identical old
   and proposed matching strings. All 525,637 usable entries in the actual strand/qamats
   projections belong to that verified domain. Every one of 789,960 settlement
   comparisons, across the full snapshot and all current-MAM projections, agrees.
   Reattaching all 786 complete serialized attachment records within copies of the
   complete survey preserves every persisted field and the complete survey tree;
   there are no differences against the existing survey either.
2. **Why that establishes complete-survey invariance without regeneration:** the only
   substituted value is the matching helper's string result. `_settle` and
   `_next_mam_context` are its only callers. Their raw inputs originate in the covered
   first-`fva` domain, including template records and next-word contexts. Equality of
   that value for every possible input preserves every candidate-subset and context
   decision. Raw classifier inputs, record construction and summary logic are unchanged.
   This is a complete input-domain substitution proof plus a differential of the complete
   existing serialized survey; it is **not** a regenerated new survey. No classifier,
   `_scan`, `_one_verse` or `build_survey` was run. The first scratch comparison reached
   its final report and failed because its walker handled lists but not tuples returned
   by the existing attachment code; the corrected walker completed the comparison.
3. **Actual implementation:** `verify_implementation.py` compares against the preserved
   pre-edit module `baseline_post_stress_meteg.py`. Its AST comparison confirms that
   the only changed existing executable function body in the survey module is the
   matching helper. Actual source selection and all 789,960 settlement comparisons
   pass; all 786 serialized attachment records and the complete survey remain equal.
   All 263,320 selected source records and 124,451 distinct current-MAM forms pass the
   display differential. All 784 eligible serialized case fallbacks and all six actual
   oleh-record fallbacks equal independently selected source forms. The report is
   `implementation-verification.json`; the complete compared survey copy is
   `implemented-existing-survey.json`.
4. **Every display route:** `implementation-display-trace.json` preserves the 1,017
   helper calls, the direct `_mam_post_silluq_statement`, `_post_silluq_footnote`,
   `_type_2_type_3_footnote` and `_para` calls, their source lines and output pages.
   The helper's nine per-page counts equal preparation. Complete-page validation
   checks 41/36/468/20/359/68/2/5/30 Hebrew tokens respectively in the nine pages'
   declared order; these include attribute tokens. All fresh page bytes equal V6.
5. **Independent serialized-text differential:** `verify_serialized_marks.py` passes
   each distinct selected snapshot/current-MAM form through the real helper and HTML
   serializer, decodes the result with `HTMLParser`, and compares exact text against
   the source with only gray-maqaf conversion. All 128,823 forms agree, including 570
   distinct VARIKA forms, 17 upper-dot forms and one lower-dot form. Every one of
   67,654 distinct annotated snapshot forms is rejected through actual helper markup,
   through inline markup split at every character, and through an attribute. Each
   diagnostic includes the original source pointer. All nine deliberately incomplete
   page sets are rejected. `serialized-mark-verification.json` records the results.
6. **A defect found by that synthetic check:** the initial diagnostic lookup omitted
   the original source pointer when the gray-maqaf conversion changed a raw form.
   `serialized-mark-source-location-failure.json` preserves the failing synthetic input
   and diagnostic. Source-location indexing now recognizes both the raw and permitted
   display spelling. The full serialized-text/annotation check then passed. These were
   deliberately synthetic annotation checks, not changed public output or V6 failures.
7. **Normal generation:** `run_site_and_suite.py site` saved the complete bytes and
   actual membership of all 1,074 HTML files under non-hidden worktree directories,
   including untracked HTML, before running
   `py/main_authored.py gen-site --trust-surveys`. Both runs preserved all 1,074 files,
   totaling 18,091,494 bytes, and all membership. This includes the index and Unicode
   proposals. Hidden scratch/metadata and `__pycache__` directories are excluded from
   this inventory. Final normal-generation output is `20260910T123046Z-site.txt`;
   `all-html-before-manifest.json` and `all-html-after-comparison.json` name the saved
   bytes and report zero differences. The earlier `20260910T122506Z-site.txt` and its
   timestamped command/manifest/comparison records remain preserved.

The tracked survey's SHA256 remains
`9b2ebdf41ab1a211a728b2f025fcbc101f8c33338007f9ea2fbe0b50c775fad2`.
All 39 private snapshot hashes still equal preparation and the technical-source pin
`e21306165707f9500ea19540d04af3e1918b563d`. No private source was regenerated,
refreshed, edited or published. V6's `actual-read-inputs.json` and
`worktree-module-hashes.json` preserve each real render's input/source hashes.

The immutable V6 script remains
`.novc/review-remediation-2026-09-08/v6_gate_wave1_01a0891a.py`, SHA256
`286e1aa5410ed39b6851c7f94d64476bb826a460909ca27f00de5289eb6e4f9c`, with fixed
baseline `c2f238f2c253d7b00b2d22dc262fe95c81a82401`. Run it with the absolute
interpreter, `-B`, then the script and `check --label <unique-label>`.
Passing evidence under `.novc/review-remediation-2026-09-08/v6-runs/` includes:

1. Entry: `20260910T120554Z-wave3-entry-01a08b34-c83e5a99/`.
2. After merge: `20260910T120911Z-wave3-after-backmerge-01a08b34-2b0902d8/`.
3. Before source edits: `20260910T121317Z-wave3-after-invariance-proof-01a08b34-29706d28/`.
4. First technical render: `20260910T121852Z-wave3-first-technical-render-01a08b34-1e20137d/`.
5. Complete display trace: `20260910T122342Z-wave3-after-implementation-trace-01a08b34-4c3b8957/`.
6. First normal generation: `20260910T122517Z-wave3-after-site-01a08b34-7e66b997/`.
7. First suite: `20260910T122753Z-wave3-after-suite-01a08b34-bd4b56d1/`.
8. Final serialized-mark check: `20260910T122952Z-wave3-after-serialized-mark-check-01a08b34-7f061f6c/`.
9. Final normal generation: `20260910T123053Z-wave3-after-site-01a08b34-29f7f3bf/`.

Every actual V6 check passed; no real stop occurred and no deliberate V6 gate probe
was repeated. The first canonical suite passed **988 tests, 5 skips and 65 subtests
in 117.23 seconds**, before the diagnostic-index correction; full output is
`20260910T122555Z-suite.txt`. The one-test increase is the new mechanical annotation
lint. Final verification and commit evidence follow below.

Final technical verification, recorded 2026-09-10: after the diagnostic correction,
all four changed Python files passed Black at its defaults. The new source and lint
files were staged before the final canonical suite so tracked-source checks included
them. `run_site_and_suite.py suite` ran
`py/main_test.py -q -p no:cacheprovider` with
`REPOS_ROOT=C:/Users/BenDe/GitRepos`: **988 passed, 5 skipped, 65 subtests passed in
109.92 seconds**. Full output is `20260910T123821Z-suite.txt`, with exact invocation,
working directory, starting HEAD and timing in `20260910T123821Z-suite-command.json`.
V6 passed immediately afterward at
`v6-runs/20260910T124012Z-wave3-after-suite-01a08b34-af6d298d/`.

`check_final_scope.py` and `final-scope.json` verify the seven changed paths, all
prior dated record lines, the complete accepted-corrections section, standard Hebrew
mark order and `git diff --check`. V1 has nine matching declared/tracked/actual MAS
pages, 11 deploy-root HTML pages and 16 direct plan files with State lines. V3 preserves
both Holman pages byte for byte: 578 suppressed-table cells and 724 active-table cells,
with zero Hebrew-cell RTL omissions. The vendoring policy gives none of the changed
Python paths a source-package copy obligation. All 39 snapshot hashes and V6's script
hash still match their recorded pins. No real stop record exists.

Wave 3 technical implementation is complete. The local commit and final pre-commit
V6 evidence are recorded in the following checkpoint append.

After the technical work and records are committed cleanly, Ben's existing automatic
handoff instruction starts a separate fresh editorial task. That task resolves and
records the editorial output contract against the existing E1-E8 approval before any
HTML edit. It preserves V6's technical baseline and evidence. Wave 3 editorial work
and Wave 4 remain pending; P2 source/rights-holder identification and the unverified
415/416 scratch count remain deferred. No intermediate integration, push, issue
action or automatic archival is authorized by this technical checkpoint.

Wave 3 technical checkpoint, recorded 2026-09-10: implementation commit
`f11660576e440523e944598331e8ecc339dcdb26` contains the complete passing remedy and
execution record. V6 passed immediately before that commit at
`v6-runs/20260910T124233Z-wave3-before-technical-commit-01a08b34-47c17bdc/`.
The seven committed paths, relative to the verified review worktree, are:

1. `py/accgram/post_stress_meteg.py`.
2. `py/author_site/post_stress_meteg.py`.
3. `py/author_site/post_stress_meteg_annotations.py`.
4. `py/tests/test_post_stress_meteg_annotations.py`.
5. `doc/PLAN-remediate-review-findings-2026-09-08.md`.
6. `doc/PLAN-close-out-review-2026-09-08.md`.
7. `doc/review-findings-2026-09-08.md`.

The following record-only commit supplies the clean required source for the editorial
successor, including this implementation commit as an ancestor. The saved project is
`51e16ebd-373a-41f7-833e-9def3ef72b81`, whose actual path is the review worktree above;
use `environment.type = local`. The creation result and final response record the actual
successor ID. Writing responsibility transfers at dispatch. Integration and push remain
scheduled once after final Wave 4; the technical task does not archive any task.

### Wave 3 editorial phase: approved items and output-contract preparation

**Step-5 decision recorded 2026-09-09:** E1-E8 are approved as specified in their table,
including E2's coalesced italic `meteg/merkha` span. This supersedes Wave 3's earlier
pending-item language. Finish and commit the passing technical phase before preparing
the separate editorial execution. Preserve its fixed baseline, evidence, and any stop record.

The intended MAS HTML differences are confined to these approved items:

| Item | Intended difference | Preserved content |
|---|---|---|
| E2 | Wrap the specified visible mark names in existing `romanized` spans on the main, Methods, and 2 Chronicles pages; use one span around `meteg/merkha`, including the slash. | All visible characters and spaces; titles and attributes. Re-measure the listed occurrences before editing. |
| E3 | Change only the main page's Fit-for-MAS criteria list from `ul` to `ol`. | The criteria entries and their order; every other list. |
| E8 | Add the approved sentence below the Aleppo 1 Kings 7:37 crop on the Methods page, with romanized mark names. | The crop, alt text, MAM paragraph, and existing attribution. |

E1/E4/E5/E6/E7 have no intended generated-HTML difference. Apply only their approved source
and documentation edits, including the dated-note treatment of historical records. Survey
JSON, numerical claims, displayed Hebrew forms, images, and MAS page membership stay unchanged
through editorial work too.

Before the editorial phase begins, document the exact intended byte differences, the
technical phase's passing commit, and the proposed editorial comparison baseline and gate.
Resolve that output contract against Ben's recorded approval; do not silently replace V6's
technical baseline or treat an unexpected technical difference as an editorial change. If
an explicit revision to the output contract still requires Ben's decision, present only that
specific revision with the concrete differences. Do not ask again whether E1-E8 are approved.
Until the editorial output contract is resolved and recorded, retain V6's original contract
and do not execute the HTML edits or advance to final integration. A real V6 stop always
requires Ben's renewed explicit approval, even when a proposed repair is already known.

Keep the editorial execution record and commit separate from the technical phase. Use a
fresh task for the editorial phase, then hand off to Wave 4 only after the approved editorial
work and its output verification are complete. Wave 4's final checks must use the explicitly
resolved editorial contract while retaining the technical result and original V6 evidence.

## Wave 4 — vendoring records, final dispositions, and one integration

Preconditions: Waves 1-3 have complete local execution records and clean commits; Ben has
approved Wave 4 and P1 and disposed of N3. All source/copy changes are committed before
auditing. Run V6, merge current `main` into the worktree branch, and run V6 again; any changed
MAS HTML stops the entire process for Ben, including changes arriving from main. Inspect new
input or instruction changes. If the merge changes MAS source or input, repeat the targeted
render and V6 before proceeding. Re-run other relevant generators only when the merge changes
their source or input; earlier validation does not cover a changed implementation. A separate
editorial baseline is valid only if Ben explicitly approved that revised output contract.

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
4. Re-run V1-V4, V6, and the canonical suite; run V6 again after the suite. Read all generated
   diffs against the implementation commits. Run the public repository-standards check below, using its reported current
   workspace roster; inspect every failure instead of treating an unchanged historical result
   as success. Do not run a maintenance sweep, spell check, or mega merely for a familiar
   completion checklist.
5. Commit the audit and the records locally, then perform the close-out plan's Integration
   section exactly once. The suite must pass on the final merged tree before the primary
   clone is fast-forwarded, with V6 passing on that exact tree and no unresolved approval
   stop. If `main` moves meanwhile, run V6 before and after merging it into the worktree again,
   then resolve and verify there. A V6 failure stops integration; it does not permit an
   automatic fix-and-retry. After a passing final check, push only `main`; do not push the
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
identified separately and verified before integration; changed MAS HTML still requires
Ben's renewed interactive decision under the conditional-approval rule.

After all source/copy commits, a second audit must produce no additional artifact difference;
this is the check that the dates were not generated before the commits they describe. Do not
make a source/copy commit after that audit without refreshing the affected audit records.

Final integration commands, after both checkout trees are clean and the merged worktree has
passed the suite and V6, with no unresolved conditional-approval stop:

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
removal to the baseline. This normalization is confined to W2's declared whitespace
outputs; V6 never normalizes MAS HTML. Compare parsed CSV rows/fields to distinguish a field change from
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
before editing and zero of those unwrapped occurrences afterwards only in a separately
authorized E2 phase. V3's parsed-text checks supplement V6; they never replace the byte gate.

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

**V6 — mandatory unchanged-MAS-HTML gate.** Implement this execution check in a uniquely
named real scratch script before remediation begins. It is an approval check for this
remediation process, not a permanent snapshot test forbidding unrelated future page work.

1. Read the protected filename set from the nine-row table above and recover each baseline
   with binary `git show c2f238f2c253d7b00b2d22dc262fe95c81a82401:gh-pages/<filename>`.
   Use `subprocess.run(..., check=True, stdout=PIPE)` without text decoding for those bytes.
   Save immutable baseline files and a SHA-256 manifest in
   `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/.novc/review-remediation-2026-09-08/mas-html-baseline/`.
   Verify the manifest against the pinned Git blobs on subsequent runs; never refresh it
   from a changed checkout. Capture the pinned survey JSON as well and require identical
   JSON bytes throughout the technical work. An absent baseline/input is a failure.
2. Compare the protected set with both renderer-declared filenames and every actual
   `post-stress-meteg*.html` in the target output directory. Fail any missing or additional
   file, including an untracked file. Compare complete bytes, with no whitespace, line-ending,
   Unicode, or HTML normalization. Check both the worktree `gh-pages` files and the fresh
   scratch render. A clean Git status alone proves neither output identity nor reproducibility.
3. Reproduce the real MAS renderer with `trust_survey=True` in a fresh scratch destination,
   using the worktree's modules and primary clone's absolute interpreter with `-B`. Retain
   normal claim checks and annotation validation. Record every input actually read and its
   hash so changed inputs cannot be mistaken for the previously simulated state. On future
   technical implementation runs, render the real changed code without the simulation's
   monkeypatch. Compare the full output with step 1's fixed baseline. Before the normal
   authored-site run, also save the other generated HTML's bytes and filenames and require
   unchanged output from the technical work. Missing or newly emitted HTML fails that scope
   check; do not restrict inspection to Git's tracked changed-file list.
4. Fail with an explicit nonzero exit, not a Python `assert` that `-O` can disable. Print the
   prominent STOP message above, every changed/missing/additional path, before/after hashes,
   and evidence paths; save byte-preserving outputs and UTF-8 textual/Unicode diffs. Preserve
   a stop record so a later pass cannot be treated as renewed approval. Invoke the gate with
   `subprocess.run(..., check=True)` or equivalent command failure propagation. No wrapper
   may catch failure and proceed to the next wave, commit, merge, or push. Any incomplete
   rendering/check likewise blocks continuation and must be reported.
5. Before relying on the gate, deliberately alter a byte in a scratch output copy and prove
   the check exits nonzero; also prove a missing file and an extra matching file fail. These
   are disposable differential checks of the gate, not edits to public HTML. Label those
   deliberate gate probes separately from real remediation results. Then require the
   untouched scratch render and checkout to pass. An unexpected failure is never a probe.
6. Run the gate before and after every back-merge, immediately after each affected generation,
   after validation/suite runs, before completed-remediation commits, and on the exact final
   tree before integration and push. Record the real script path, command, HEAD, manifest,
   output hashes, and result in the wave record. Preserve any failure record and Ben's
   subsequent explicit renewed/revised approval. If Ben later authorizes a separate editorial
   phase, document its specific allowed diff and baseline before executing that phase; do
   not let an agent replace the technical baseline retroactively.

The outcome required by the current approval is **zero changed HTML files and zero changed
locations**, regardless of passing tests or unchanged visible text. Any real difference
triggers the conditional-approval section's stop of the entire remediation process.

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
private scholarly-source research, broad prose cleanup, and repository/task-folder
maintenance remain separate work. The newer Phonetic MAM technical sources explicitly named
above are the bounded read-only exception, not permission for a private corpus refresh.
The plan does not authorize posting comments or changing issues. The final review worktree
integration and retirement follow the close-out plan's final-wave/step-7
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

## Follow-up planning record: displayed marks and conditional approval

2026-09-09: at review worktree HEAD `c2f238f2c253d7b00b2d22dc262fe95c81a82401`, the targeted
two-pass simulation measured byte-identical HTML in all nine pages and no differing helper
results, as recorded above. Later read-only inspection established the `rep` alternative,
the limits of snapshot spelling, the newer output guard and explicit literal repair, and the
existing MAS guard's broader forbidden set. Those findings change the proposed remediation
and its validation, rather than merely changing the explanation of a display-only fix.

Ben then conditionally approved the discussed technical work on unchanged HTML and requested
this plan update. The plan now requires an executable byte gate and a stop of all remediation
for interactive discussion if that condition fails. E2/E3/E8 remain separate pending changes;
the slash-span preference is preserved without turning it into unconditional HTML approval.
This update changes only this plan, with no back-merge, production-code edit, generated-product
edit, remediation execution, primary integration, or push. The earlier planning execution
record above remains historical; the conditional approval here supersedes its wholly-pending
description only for the discussed technical work. Other wave/P/E/N dispositions are unchanged.

## Step-5 approval record and next execution phase

**Ben's decision, 2026-09-09:** after the plan update at
`961554d4ffb9e4ee7d849c4620083bd93f170ffb`, Ben answered the original question,
"Do you approve the waves and P1–P3 recommendations, including the exact editorial proposals
E1–E8 and N1–N9?", with "I can now say yes". Ben requested Step 5 in a fresh task. The
predecessor recorded that approval in close-out-plan commit
`e2693d9a3fbd43981f81c70e21ef6ec66ba41d4c`; the Step-5 task verified that exact clean HEAD
and branch `codex-review-2026-09-08` in
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`.

| Items | Disposition |
|---|---|
| Wave 1, Wave 2, Wave 3, Wave 4 | Approved in the stated order and scope, subject to V6 and the separate editorial phase. |
| P1, P2, P3 | Approved as recommended, including their limits and explicitly deferred investigation. |
| E1, E2, E3, E4, E5, E6, E7, E8 | Approved exactly as amended; E2 includes the italic slash. Execute separately from the technical phase, as specified above. |
| N1, N2, N3, N4, N5, N6, N7, N8, N9 | Approved exactly as proposed, in their assigned waves. |

These dispositions supersede every earlier pending-approval statement and satisfy every
"if approved" prerequisite for the listed proposals. The earlier records are preserved as
history. For example, the former line-3 State was:

> State: live 2026-09-09; MAS technical work conditionally approved only with unchanged HTML; other step-5 approvals remain pending; no remediation started.

The approval does not waive the technical unchanged-HTML condition. V6 still compares
complete bytes and exact page membership against
`c2f238f2c253d7b00b2d22dc262fe95c81a82401`, preserves its pinned JSON, and halts the entire
remediation process on a real difference. Failed or incomplete rendering/checking blocks
progress too. The simulation establishes only its stated display-preservation result; it
does not validate revised `rep` selection, matching, or annotation validation. The bounded
technical-source read permission and restrictions on private regeneration and scholarly
investigation remain unchanged.

Ben's presentation order remains public-facing wording, including HTML and reader-facing
Markdown, then published corpus data, then broad categories of lower-risk changes. Internal
`doc/` Markdown and MAS analysis JSON are generally lower risk; Phonetic MAM JSON without a
resulting HTML change is also lower risk. Classification does not expand the approved scope.

**Next authorized execution phase:** Step 6, Wave 1, in a fresh task using the same saved
worktree directly. Its first work is V6 setup and proof, before any remediation back-merge
or edit. No new decision blocks that handoff. The later editorial output contract must be
addressed before the separate Wave 3 editorial phase begins, as specified above.

Step 5 performs planning/approval write-back only. No remediation, generator run, V6
implementation, back-merge, integration, or push has been performed. No tracked Python file
changed. The Step-5 completion record in the close-out plan records verification and the local
commit. Integration remains scheduled once, at the end of Wave 4, including across intermediate
task archival. Ben's phase-handoff instruction of 2026-09-09 authorizes starting each next
fresh task once the preceding phase is committed and clean and no new decision is needed.
