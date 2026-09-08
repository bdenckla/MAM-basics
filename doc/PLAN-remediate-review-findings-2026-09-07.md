# PLAN — remediate the 2026-09-07 dual-agent review

State: executed 2026-09-08

The planning phase and all remediation work were completed on 2026-09-08. Ben's decision on
2026-09-08 places finding 23.2's worktree housekeeping outside remediation; Ben will track that
housekeeping separately.

Ben requested this planning phase on 2026-09-08, after the Claude review, the Codex Terra review,
and the Codex Sol re-review were complete. This file turned those three frozen reports into a working
checklist. The remediation task executed the checklist, recorded a disposition for every item, and
changed `doc/review-findings-2026-09-07.md` from `not yet acted on` to `acted on 2026-09-08` after
the work earned that state.

The review contains 24 numbered Claude findings and one additional Codex Sol finding. The Codex Sol
review also corrects two statements in the Claude report:

1. The post-stress-meteg duplication consists of **368 qamats-variant rows containing 370 duplicated
   chanted words**, not 368 duplicated chanted words.
2. The 99 commits with a co-author trailer have **five exact trailer spellings**, not four. The
   narrower census of three Codex trailer spellings remains correct.

The original Claude, Terra, and Sol findings remain frozen. Do not rewrite their findings. Record
what the remediation establishes in the later disposition section.

## Governing instructions and inputs

Before the first implementation edit, read these files completely:

1. `C:/Users/BenDe/.Codex/AGENTS.md`;
2. `C:/Users/BenDe/.agents/skills/hebrew-prose/SKILL.md`;
3. `C:/Users/BenDe/GitRepos/MAM-basics/CLAUDE.md`;
4. `C:/Users/BenDe/GitRepos/MAM-basics/doc/agent-planning-principles.md`;
5. this plan;
6. `C:/Users/BenDe/GitRepos/MAM-basics/doc/dual-agent-review.md`;
7. `C:/Users/BenDe/GitRepos/MAM-basics/doc/review-findings-2026-09-07.md`;
8. `C:/Users/BenDe/GitRepos/MAM-basics/doc/codex-review-findings-2026-09-07.md`; and
9. `C:/Users/BenDe/GitRepos/MAM-basics/doc/codex-review-findings-2026-09-07-sol.md`.

The `hebrew-prose` skill governs every implementation, generated page, docstring, comment, commit
message, and disposition that discusses Hebrew accentuation. The review's finding 21 identifies
known violations; the skill remains the authority when the review paraphrases it.

The planned implementation root is the primary checkout:

`C:/Users/BenDe/GitRepos/MAM-basics`

The interpreter is:

`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`

Three sibling checkouts matter to execution:

1. `C:/Users/BenDe/GitRepos/phonetic-hbo` supplies the public Phonetic MAM rendering used as an
   independent oracle for the post-stress census.
2. `C:/Users/BenDe/GitRepos/MAM-private` supplies the Phonetic MAM standard set to the real
   `survey-post-stress-meteg` command, and the mega pipeline writes its near-Aleppo census outputs.
   The remediation remains public-only: read only the input needed by the existing generator and do
   not copy private paths, data, or findings into a public report.
3. `C:/Users/BenDe/GitRepos/MAM-OSIS` remains the mega pipeline's remaining public sibling write
   target.

Before a full mega run, verify that MAM-private and MAM-OSIS are clean, record their exact heads, and
establish that no other task is writing either checkout. Snapshot both trees before and after the
run. Any sibling diff is an unexpected result to explain, not permission to stage or commit that
repository under this plan. If either sibling cannot safely be used, run the focused MAM-basics
generators and defer the full mega verification rather than touching an active checkout.

Do not create a feature branch for ordinary primary-checkout work. If another task is writing the
primary checkout when implementation starts, use a separately verified MAM-basics worktree and its
required non-`main` branch. In that case, run every script from the verified worktree while borrowing
the primary checkout's interpreter by the absolute path above. Never put a `.venv` junction, symlink,
or copy in the worktree.

## Planning baseline to re-establish

The following state was measured on 2026-09-08 before this plan was committed and is retained as
the historical planning baseline:

| Item | Measured state |
|---|---|
| Primary checkout | `C:/Users/BenDe/GitRepos/MAM-basics` |
| Primary branch | `main` |
| Primary `HEAD` and `origin/main` | `5dfbd7bde4c8d6bb387935e853ff80d29a562aa2` |
| Primary working tree | clean |
| Review anchor | `8bf586a3` |
| Last full suite | 976 passed, 5 skipped, 65 subtests passed at `5dfbd7bd` |
| Concurrent worktree | `C:/Users/BenDe/.codex/worktrees/MAM-basics-post-stress-meteg` |
| Concurrent branch and head | `post-stress-meteg` at `b7484530`; one commit exists only on `main`, six only on the worktree branch |
| Review scratch evidence | present under `C:/Users/BenDe/GitRepos/MAM-basics/.novc/review-2026-09-07/` |

The concurrent worktree is not a generic precondition failure. It belongs to the task titled
`Add Leningrad Aleppo evidence page`, task id `01a08138-c643-7082-a7ee-b60c4c6a4a06`. Ben reported
on 2026-09-08 that work on that task may continue, so equality of the two branch tips is not evidence
that the task has permanently relinquished its paths. Do not merge, move, or edit that worktree on
this plan's authority.

### Reassessment after the latest post-stress integration, 2026-09-08

The latest integrated snapshot materially narrows the coordination precondition:

| Item | Measured state | Command that re-establishes it |
|---|---|---|
| `main`, `origin/main`, and local `post-stress-meteg` | all at `c73a2ad344faa6d0c49f9b3dc1f99e6c679315b5` | `git rev-parse HEAD`; `git rev-parse origin/main`; `git rev-parse post-stress-meteg` |
| Primary and post-stress working trees | both clean | `git status --short`; `git -C C:/Users/BenDe/.codex/worktrees/MAM-basics-post-stress-meteg status --short` |
| Local branch divergence | `0  0` for `main...post-stress-meteg` | `git rev-list --left-right --count main...post-stress-meteg` |
| Remote post-stress branch | `9239ac3a`; no remote-only commits and 124 commits behind `main` | `git rev-parse origin/post-stress-meteg`; `git rev-list --left-right --count origin/post-stress-meteg...main` |
| Commits after the plan commit | 13 commits in `f5df191e..c73a2ad3` | `git rev-list --count f5df191e..main` |
| Latest full suite reported by the post-stress task | 976 passed and 5 skipped at `c73a2ad3` | rerun `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q` rather than trusting the report at a later head |

The 13 commits changed the post-stress generator, survey focus-verse data, generated JSON and pages,
and two new 1 Kings 7:37 manuscript crops. Re-establish that scope with
`git diff --name-status f5df191e..main`. The commits did not complete a review-remediation item:

1. Finding 3's qamats-variant flattening remains in `_chanted_words` and `_chanted_word_events`.
2. Finding 12's named stale plans, method record, docstrings, site-page counts, and fragment records
   were not changed by `f5df191e..c73a2ad3`.
3. Finding 13's type-3 definition disagreement, residual type-2 identifiers, and BHS claim remain at
   their searchable anchors.
4. The changed and added post-stress prose must be included in finding 21's fresh prose scan.
5. `gh-pages/img/` now contains six tracked crops, including two added after `f5df191e`; finding 14's
   licence work must cover the live six-file directory rather than the one-file review snapshot or
   the four-file planning snapshot. Re-establish the current list with `git ls-files gh-pages/img`.

Accordingly, Wave 2 no longer waits for accumulated branch-only work to be integrated. Immediately
before Wave 2, inspect the named task, both working-tree statuses, all three local and remote heads,
branch divergence, and the paths changed since the common head. If the task is idle and both local
tips remain equal and clean, the earlier integration creates no blocker. If the task has resumed,
agree which task owns the overlapping post-stress paths; postpone only those paths, not unrelated
waves. A later edit to a path is not proof that the finding was fixed.

Re-establish the checkout, branch, head, remote head, status, worktree list, and branch divergence
before editing. The hashes above are evidence, not expected implementation heads. Inspect every
intervening commit touching a finding's paths.

The seven post-stress pages regenerated byte-identically at the review anchor. After this plan was
first committed, the post-stress task ran the survey for its focus-verse data change, regenerated the
pages after later page-source edits, and ran the full suite at `c73a2ad3`. Those runs verify the
post-stress task's integrated changes; they do not satisfy Wave 2's acceptance conditions. Wave 2
changes the census model and must still run the real survey and render twice after its own edits.
The full mega pipeline remains unverified for this remediation.

## Decision gates before implementation

Four finding groups need Ben's decision or authorization. The implementation task may re-establish
the evidence and give a recommendation, but it must not silently choose.

1. **Finding 7 — redirect command default.** Decide whether a bare redirect command targets
   wlc-utils, targets MAM-simple, or is rejected unless `--repo` is explicit. The planning
   recommendation is to require `--repo`: table order should not choose an absent redirect host, and
   an explicit argument makes the examples and diagnostics truthful.
2. **Finding 9.1 — MAM-for-Sefaria clone.** Re-run the complete clone-safety check, including the
   unreachable `34c94a8` object and its patch equivalence, then ask whether to move
   `C:/Users/BenDe/GitRepos/MAM-for-Sefaria` to the Windows Recycle Bin. Do not permanently delete it.
3. **Finding 15 — `misc/linux-sh/`.** Establish whether Ben still uses the three shell scripts. The
   planning recommendation is to retire them if they are unused; if they remain, make them derive
   their repository set from the canonical declaration instead of preserving either text roster.
4. **Finding 20 — eleven orphaned pages.** Preserve the earlier decision about the seven previously
   known pages unless Ben changes it. Ask separately whether each of the four newly landed pages
   should gain a link from its product or subtree index, remain deliberately unlinked with a recorded
   reason, or be removed.

Finding 23.2's obsolete branch and empty directory were noticed during remediation but are not
remediation work. Ben's decision, 2026-09-08: track that worktree housekeeping separately and do not
make it a condition of remediation completion.

Finding 23.3's completed dated task folder and finding 23.4's ignored `.pytest_cache` belong to the
next repository-maintenance judgment pass, not this code-remediation task. Refer them there; do not
delete them while acting on this plan.

## Complete finding crosswalk

This table is the working ledger. Every row must receive exactly one final disposition in
`doc/review-findings-2026-09-07.md`, even when the disposition is `already fixed`, `rejected`,
`record only`, `referred to maintenance`, or `needs Ben's decision`.

| Finding | Planning classification | Planned wave and acceptance condition |
|---:|---|---|
| 1 | Fix | Wave 1. Repair the shared MAM-simple XML reader, restore the omitted Deuteronomy 32:6 content in the Aleppo line data, and make an independent full-corpus comparison expose any similar target shape. |
| 2 | Fix | Wave 1. Move the Deuteronomy 33:29 chanted word from the end of 005v to the beginning of 006r and make both line-break checks agree with the manuscript crops. |
| 3 | Fix after remeasurement; confirmed present at `c73a2ad3` | Wave 2. Collapse qamats-variant entries to MAM chanted words for census denominators and counts; use the Sol correction of 368 rows and 370 duplicated chanted words; investigate the nine deḥi-versus-meteg differences and the two unexplained prose entries before accepting new figures. The integrated focus-verse change did not alter the flattening mechanism. |
| 4 | Fix before any mega run | Wave 1. Correct the Job XML path and prevent the output from being truncated before input parsing and successful generation. |
| 5 | Regenerate after blockers | Wave 3. Regenerate every owned product that emits the MAM-with-doc URL and reduce the old-host grep to the deliberate records and byte-verbatim/downloaded inputs. |
| 6 | Partly fixed after the anchor | Wave 3. Confirm the five copies now match, make MAM-simple support-file copying LF-stable like the MAM-parsed twin, and correct the Phase 1 count from 43 to 44 with the added path named. |
| 7 | Ben's decision, then fix | Wave 5. Implement the chosen redirect default and make all examples, module prose, and `CLAUDE.md` describe the chosen behavior. |
| 8 | Fix with lint-shaped checks | Wave 4. Consolidate the landed source/prose coverage into canonical tests, restore MAM-simple page mark-order coverage, lint deploy-root pages without treating multi-site CSS classes as errors, and cover program-written product paths for machine paths. Do not scan million-line generated data merely because it shares a top-level directory. |
| 9 | Mixed decision and record repair | Wave 5. Apply decision gate 2; correct items 9.2–9.7 against current files and remote breadcrumbs. Update the MAM-simple redirect host through the established temporary-host workflow without restoring a permanent clone. |
| 10 | Fix records | Wave 5. Correct the third-stage plans, maintenance runbook, manifest spelling, clone descriptions, corpus counts, and landed-product wording from current evidence. Preserve dated history while adding explicit corrections where rewriting history would blur the execution record. |
| 11 | Mixed record and prose repair | Waves 2 and 5. Correct items 11.1–11.6 and the live-present-tense part of 11.7. Leave dated historical citations as dated history when Ben's precedent says to leave them; correct claims that still present a deleted file as current. |
| 12 | Re-measure, then fix; confirmed present at `c73a2ad3` | Wave 2. Reconcile every post-stress record and plan with the current JSON and current page set. The integrated post-stress work changed the focus-verse JSON and generated pages but not the named stale records, so no 231/232, 3,181/496, page-count, or fragment statement may be copied without regeneration. |
| 13 | Fix; confirmed present at `c73a2ad3` | Wave 2. Make the type-3 definition and classifier agree, finish the type-2 name change, and replace the unsupported BHS claim with claims supported by the actual UXLC/WLC inputs and manuscript crop. The integrated evidence-page work did not remove any of these three anchors. |
| 14 | Fix licence coverage against the live tree | Wave 5. Add precise rows for manuscript crops and post-stress outputs, correct landed/source directory descriptions and MAM statement locations, cover every Taamey D font copy, and replace vague authorship vocabulary. `gh-pages/img/` contains six tracked crops at `c73a2ad3`, two added after the plan commit; re-census the directory and read every live image's provenance before naming a rights holder or photograph source. |
| 15 | Ben's decision | Wave 5. Apply decision gate 3 and leave one canonical repository declaration. |
| 16 | Fix data and add lint coverage | Wave 4. Put the two inherited Aleppo pages in MAM mark order and extend a mechanical mark-order check to the owned Aleppo pages so later imports cannot restore Unicode-normal order silently. |
| 17 | Mixed code hardening after remeasurement | Waves 1, 2, and 4. Narrow the line comparison to the differences intentionally ignored; align post-stress mismatch and punctuation handling with the survey contract; remove or replace checks that prove nothing and dead fields that reach no output; prevent legacy-history output from choosing a tracked release path; re-evaluate finding 17.4's type-1/type-2 sample links against the current consolidated page set. |
| 18 | Fix current docstrings and comments | Wave 5. Re-scan every named path after the post-anchor repoint commits, then correct only statements still stale. Do not reintroduce obsolete sibling-repository concepts. |
| 19 | Fix README and licence prose | Wave 5. Remove nonexistent CLI options and deleted entry points, repair the `misc/linux-sh/` path if the directory remains, classify packages truthfully, number announced lists, and make the GPL/MIT and `doc/woff2/` exceptions consistent. |
| 20 | Ben's decision | Wave 5. Apply decision gate 4 and rerun the complete HTML link graph; every remaining orphan must be deliberate and recorded by exact path. |
| 21 | Fix prose against the integrated pages | Waves 2 and 5. Apply the `hebrew-prose` skill and global prose rules to the live post-stress pages, source prose, comments, plans, review disposition, and announced counts. Re-scan current files because `f5df191e..c73a2ad3` revised existing post-stress prose and added new 1 Kings 7:37 prose. |
| 22 | Record only | Wave 6. Reconfirm instruction-file identity if any instruction file changed during remediation; otherwise record that no remediation was required. Do not publish private github-misc content. |
| 23 | Record and maintenance referrals | Waves 5 and 6. Do not rewrite historical trailers; leave item 23.2 to Ben's separate worktree-housekeeping track; refer items 23.3 and 23.4 to maintenance; treat the next `fr-wikisource` refresh as a known future diff; record item 23.6 as a cadence census rather than a code defect. |
| 24 | Record only | Wave 6. Reject rewriting immutable commit messages. Preserve the corrected facts in the review and disposition record. |
| Sol-1 | Fix artifact hygiene after regeneration | Wave 3. Re-run both the frozen-range and current-tree whitespace checks, classify generated versus hand-authored whitespace, repair the canonical sources or generator where possible, and require regenerated artifacts to pass `git diff --check` without a mass unrelated reformat. |

## Wave 1 — Aleppo line data, XML reading, and fail-before-write behavior

Goal: make the line-data oracle truthful and remove the generator that can destroy a tracked output
before failing. Findings 1, 2, 4, and 17.1 share that integrity boundary.

- [ ] Run the finding 1 and 2 probes from `.novc/review-2026-09-07/` against the current checkout and
      save new labelled output under a purpose-named `.novc` directory.
- [ ] Change the `<scrdfftar>` reader only after enumerating every live element shape in all 24
      MAM-simple XML files. Concatenate the suspended-letter child and the text child in document
      order; reject an unrecognised shape instead of dropping content.
- [ ] Correct 004r, 005v, and 006r from the tracked manuscript crops and full line sequence, not by
      making the data agree with the repaired reader alone.
- [ ] Narrow `no_marks_comparison_key` to the exact marks the comparison intentionally tolerates.
      Preserve detection of a vowel, dagesh, shin/sin dot, accent, letter, or grouping error.
- [ ] Correct `main_letter_small_job.py` to use `MAM-simple/xml-vtrad-mam/Job.xml`. Parse and compute
      successfully before replacing `py-examples-out/letter-small-job.txt`; a failure must preserve
      the previous tracked file byte-for-byte.
- [ ] Run the complete Aleppo and Cambridge line-break checks. The known Aleppo issue count may change
      only for an explained correction; the Cambridge 4-of-4, 160-of-160 result must not regress.
- [ ] Run the letter-small-job entry point twice. The second run must be byte-identical, and an
      ignored adverse probe with a bad input must leave the tracked output unchanged.

Use the real line-break entry points:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_ac_check_line_breaks.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_cam1753_check_line_breaks.py
```

Use the real letter-small-Job entry point:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_letter_small_job.py
```

Expected not to change in Wave 1: Cambridge source data and crops, unrelated MAM-simple products,
post-stress survey data, and any repository outside MAM-basics.

### Wave 1 result — completed 2026-09-08

- Changed `py/py_ac_loc/mam_xml_verses.py` to handle every live `sdt-target` shape and to
  concatenate the suspended-letter and text children in document order. The current-tree rerun of
  the frozen `A_08_readonly_oracles.py` probe found 32 targets in five shapes across all 24 XML
  files; Deuteronomy 32:6 is the sole `slh-word` plus `text` shape, and the repaired reader retains
  both atoms.
- Corrected `aleppo/line-breaks/004r.json`, `005v.json`, and `006r.json` from the three reviewed
  crops. The real Aleppo line-break command changed the report from 92 to 91 issues solely by
  removing the chanted word after 005v's last line marker; the total chanted-word count increased
  by one because Deuteronomy 32:6 is complete. The real Cambridge command remained at zero issues,
  and its tracked report remained byte-identical.
- Changed `no_marks_comparison_key` to ignore only meteg and rafe. Vowels, dagesh, shin and sin
  dots, accents, format characters, letters, and punctuation now remain visible to both complete
  line-break checks.
- Corrected `py/main_letter_small_job.py` to read
  `MAM-simple/xml-vtrad-mam/Job.xml`. `py/mb_misc/letter_small_job.py` now parses and computes the
  report before using `mb_cmn.file_io.with_tmp_openw` to replace the tracked output. Two real
  entry-point runs produced SHA-256
  `a0ac8005c65dfe395d01b8d165e0410562b5e8f98a43669acc1287e3138dc071`; an adverse missing-input
  probe raised `FileNotFoundError` and preserved the output byte-for-byte.
- Verification: black and ruff passed on the four changed Python files; `git diff --check` passed;
  the canonical suite reported 976 passed, 5 skipped, and 65 subtests passed. The ignored evidence
  is under `.novc/remediation-review-2026-09-07-wave1/`.
- Commit and push: `c76239a5` (`Repair review Wave 1 line-data integrity`) is on `main` and was
  pushed to `origin/main`. No file outside MAM-basics changed. The 91 remaining Aleppo structural
  issues predate this wave and remain outside its scope.
- Next wave: inspect task `01a08138-c643-7082-a7ee-b60c4c6a4a06`, both MAM-basics checkouts, and
  the post-stress branch heads immediately before beginning Wave 2.

## Wave 2 — post-stress-meteg model, claims, records, and prose

Goal: make one current model support the survey JSON, every generated page, and every live factual
record. This wave covers findings 3, 11's post-stress prose, 12, 13, 17.2, 17.4, and the post-stress
part of finding 21.

- [ ] Recheck task `01a08138-c643-7082-a7ee-b60c4c6a4a06`, both checkout statuses, `main`,
      `origin/main`, `post-stress-meteg`, and their divergence immediately before editing. At the
      2026-09-08 reassessment, the task was idle and all three heads were clean and equal at
      `c73a2ad3`, so no accumulated branch-only work remained. If the task has resumed, coordinate
      ownership of the overlapping post-stress paths. Merge no branch merely to satisfy this
      checkbox, and do not block unrelated waves on post-stress path ownership.
- [ ] Re-run the public Phonetic MAM comparison. Establish the current qamats-variant row count,
      duplicated-chanted-word count, prose and poetic denominators, MBS counts, MAS counts, silluq
      counts, and all unexplained differences from current source data.
- [ ] Represent a qamats-variant chanted word once for MAM census purposes while retaining any
      genuinely distinct phonetic readings needed by the survey. Add a fatal invariant connecting
      entry counts, row counts, and distinct MAM chanted words.
- [ ] Resolve the nine deḥi-versus-meteg differences and two unexplained prose entries before changing
      a published figure. If public data cannot adjudicate one, record the bounded uncertainty rather
      than choosing a corpus silently.
- [ ] Decide the type-3 rule from the sources and current corpus, then make prose, classifier, and
      `pin_claims` assert the same rule.
- [ ] Complete the type-2 identifier rename without an alias unless compatibility evidence requires
      one.
- [ ] Label UXLC and WLC as the sources actually read. Do not claim that BHS has a form on the
      authority of BHS-derived transcriptions.
- [ ] Make next-chanted-word parse mismatches follow the survey's documented mismatch policy. Make
      punctuation handling explicit for paseq/legarmeh, setuma, petuxa, and qamats-note material.
- [ ] Remove or replace the vacuous multiple-type assertion, the doubled `word` gloss, unused source
      gradings, and the whole-corpus load for a one-verse lookup when each remains present.
- [ ] Re-evaluate finding 17.4 against the current consolidated lacks-MAS pages. State totals and
      sampling whenever a link opens a sample; do not restore deleted page shapes merely to match the
      review's old line numbers.
- [ ] Update every live plan, census note, docstring, site-page count, and fragment link from the newly
      regenerated artifacts. Preserve historical statements as dated history and add a dated
      correction when needed.
- [ ] Apply every prose correction in current source, including `own`, loose `word`, possession verbs,
      undefined reader-facing abbreviations, section-range punctuation, and tsere spelling. Rebuild
      shared ITM/CoS links by reuse rather than preserving duplicate local helpers.

Run the real survey before rendering the pages:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_accgram.py survey-post-stress-meteg
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_authored.py gen-site
```

Run each command twice. The second survey and second render must introduce no further content change.
Read the regenerated JSON and every generated post-stress page. Treat every unexplained generated
diff as a failure. Expected not to change in Wave 2: unrelated accgram pages, MAM-simple source
products, Aleppo line data, and the private Phonetic MAM source tree.

### Wave 2 result — completed 2026-09-08

- Re-ran the public Phonetic MAM comparison against the current source. The review-era Sol
  correction of 368 qamats-variant rows and 370 duplicate entries had become historical: the
  current source has 370 rows and 372 duplicate entries. The two grouping differences remain
  Psalms 35:10 and Proverbs 19:7, where the qamats-dal reading forms one MAM chanted word and the
  qamats-sam reading forms two. No unexplained prose residual remains.
- Changed `py/accgram/post_stress_meteg.py` so a qamats-variant row contributes one MAM chanted-word
  sequence to the census while both phonetic readings remain available for validation. Fatal
  per-system and aggregate invariants now connect source entries, MAM chanted words, qamats rows,
  duplicate entries, and the two measured grouping differences. The corrected denominators are
  233,277 prose and 29,542 poetic chanted words; MBS_O is 12,828 and 1,786; MAS is 178 and 54; and
  silluq is 18,738 and 4,465. The separate positional census has 12,962 and 1,805 pre-stress marks.
- Re-established the genuine currency differences at `jb29:16`, `pr13:25`, `ps44:27`, `ps57:9`,
  `ps69:29`, `ps86:7`, `ps108:3`, `ps138:3`, and `ps139:7`. Each current MAM-simple verse has one
  more U+05BD than the Phonetic MAM snapshot. The complete comparison has 23,184 numbered verses,
  with 38,161 snapshot U+05BD against 38,170 in MAM-simple.
- Made finality part of both structural type 3 and Fit-for-MAS type 3, completed the type-2
  next-chanted-word identifier rename, made parse-mismatch and intervening-material handling follow
  the survey contract, removed the vacuous multiple-type output and unused source gradings, and
  limited the WLC lookup to `out/wlc422/1verses_03_jsju1s.json`.
- Changed `py/author_site/post_stress_meteg.py`, `py/author_site/site_data.py`,
  `py/main_authored.py`, and `py/tests/test_site_index_links.py`; regenerated
  `out/accgram/post-stress-meteg.json` and every `gh-pages/post-stress-meteg*.html` page. The rendered
  prose now identifies UXLC 3.9 and WLC 4.22 as the transcriptions actually read, defines the dual
  cantillation labels, uses one shared ITM/CoS link implementation, states the current page and
  sample totals, and applies the Hebrew-prose terminology rules.
- Corrected `doc/post-stress-meteg-method.md`, `doc/post-stress-meteg-census-2026-09-03.md`,
  `doc/holman-meteg-m23-isaiah-23-12.md`, `doc/PLAN-holman-meteg-rollout-programme.md`, and
  `doc/PLAN-post-stress-meteg-page-and-holman-m23.md`. Dated execution facts remain in place with
  explicit 2026-09-08 corrections; live page counts and the retired M23 fragment now match the
  generated files.
- Ran the real survey and `gen-site` twice. The second pass was byte-identical for the JSON, all
  eight post-stress pages, `unicode-proposals.html`, and `index.html`. Black and ruff passed on every
  changed Python file, `git diff --check` passed, and the canonical suite reported 976 passed,
  5 skipped, and 65 subtests passed. The ignored probes and hash evidence are under
  `.novc/remediation-review-2026-09-07-wave2/`.
- Commit and push: `e91d7358` (`Repair review Wave 2 post-stress model`) is on `main` and was pushed
  to `origin/main`. The private Phonetic MAM source tree remained clean. Task
  `01a08138-c643-7082-a7ee-b60c4c6a4a06` remained idle, and its clean `post-stress-meteg` worktree
  remained at `c73a2ad3`; Wave 2 did not touch that worktree.
- Next wave: regenerate every owned product family, make MAM-simple support-file copies LF-stable,
  reconcile the old-host URL census, and repair generator-owned whitespace without changing
  byte-verbatim or downloaded inputs.

## Wave 3 — product regeneration, vendoring, URL migration, and whitespace

Goal: bring generated products back into agreement with their generators after Waves 1 and 2 remove
the known blockers. This wave covers findings 5 and 6 and Codex Sol finding Sol-1.

- [x] Recount old MAM-with-doc URLs by owned output family. Preserve occurrences only in dated records,
      byte-verbatim Wikisource input, and downloaded Sefaria input.
- [x] Run `copy-support-files`, confirm all 44 mapped MAM-simple examples are blob-identical to their
      sources, and make the copy operation LF-stable on a CRLF checkout.
- [x] Regenerate the MAM-for-Sefaria, Book of Job, Holman, UXLC, WLC, and MAM-parsed output families
      from their real entry points. Do not perform a textual bulk replacement in generated files.
- [x] Run the complete mega pipeline only after finding 4 is fixed and the focused product runs are
      understood. Inventory every changed file before accepting it.
- [x] Run `git diff --check b4706759..8bf586a3` to preserve the Sol measurement, then run
      `git diff --check` on the remediation changes. Fix whitespace in the canonical source or
      generator where one exists. Keep imported byte-verbatim data unchanged unless its policy
      explicitly assigns formatting ownership to MAM-basics.
- [x] Run every generator a second time without restoring the first run. The second run must add no
      content change.
- [x] Recount the old-host URLs. The expected result is zero in owned generated outputs; every
      surviving occurrence must be listed by exact deliberate category.

Use these established entry points:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_mam_simple.py copy-support-files
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_vendoring.py --all
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
```

Expected not to change in Wave 3: byte-verbatim/downloaded input trees, private repositories, and
generated families whose source and URL constants were untouched. The first mega run may expose the
known future `fr-wikisource` diff; separate that data refresh from URL and whitespace remediation in
the disposition record.

### Wave 3 execution result — 2026-09-08

- Regenerated the six named product families from their real entry points. The accepted MAM-basics
  content diff before this execution record comprised 390 files: 383 generated URL-family files and
  seven other files. A byte-level check, after replacing the old host with the new host and ignoring
  whitespace, found zero additional differences in the 383 URL-family files. The seven other files
  were the two Python fixes, the copied MAM-simple support module, one generated path record, two
  documentation records, and one vendoring report. No `fr-wikisource` file changed.
- Changed `py/py_misc/mam_simple_copy_py_files.py` to copy UTF-8 text with explicit newline handling.
  Two copy passes and the final verification each reported 44 mapped files, zero clean-blob
  mismatches, and zero CRLF destinations. `doc/PLAN-evacuate-five-MAM-products.md` now records the
  correct Phase 1 count of 44 and names `MAM-simple/py-examples/mb_cmn/paths.py` as the omitted path.
  Vendoring regeneration reported 44 comparison rows and 8 inventory rows covering 44 files.
- The first complete mega attempt exposed a stale sibling-path assumption in the MAM-private
  near-Aleppo subprocess: the old `C:/Users/BenDe/GitRepos/MAM-parsed` clone no longer exists.
  `py/main_0_mega.py` now supplies the consolidated `MAM-parsed` directory through
  `REPO_MAM_PARSED_DIR`. The resumed run then completed all 102 scripts and exposed four current
  near-Aleppo census expectations.
- **Authorized scope exception, Ben's decision, 2026-09-08:** update exactly the four generated
  MAM-private expectations exposed by the corrected near-Aleppo run. MAM-private commit `267a3e25`
  (`Refresh near-Aleppo census goldens`) contains only `gershayim_contexts.txt`,
  `legarmeh_narpas_diffs.txt`, `manual_suppression_outcome.txt`, and
  `nusach_suppression_outcome.txt`; it is pushed to `origin/main`. The update records the consolidated
  MAM product locations and the current suppression data. Two subsequent complete mega runs left
  MAM-private clean at `267a3e25`.
- Ran the complete mega pipeline twice from the beginning after the scope exception. Each run
  reported 102 scripts, 102 goldens written, and zero crashes. SHA-256 snapshots of all 5,517 tracked
  MAM-basics files changed in zero files from the pre-run tree through the first run and in zero files
  from the first run through the second run. The focused family generators had already passed the
  same two-run comparison.
- Reproduced the frozen Sol whitespace measurement: `git diff --check b4706759..8bf586a3` exits 2
  with 210 findings, comprising 21 trailing-whitespace findings and 189 new-blank-line-at-EOF
  findings. The current `git diff --check` exits 0. Byte-verbatim Wikisource input and downloaded
  Sefaria input did not change.
- The final old-host census has zero occurrences in owned generated output. The surviving deliberate
  occurrences are one documentation file with 3 hits, 39 downloaded Sefaria input files with 39
  hits, and 5 byte-verbatim Wikisource introduction files with 5 hits.
- Black left both changed Python files unchanged, ruff passed both files, and the canonical suite
  reported 976 passed, 5 skipped, and 65 subtests passed. The ignored inventories, censuses, and
  SHA-256 evidence are under `.novc/remediation-review-2026-09-07-wave3/`.
- Commit and push: `4afe3ebc` (`Repair review Wave 3 generated products`) is on `main` and was pushed
  to `origin/main`. The commit contains the 390-file implementation and generated-product diff.
- Next wave: consolidate the canonical lint scopes, repair the two inherited Aleppo mark-order pages,
  harden legacy-history output paths, and add the adverse and mechanical checks specified by Wave 4.

## Wave 4 — lint coverage and latent safeguards

Goal: make the current repository layout mechanically check the source and generated surfaces it
claims to check. This wave covers finding 8, finding 16, and finding 17.3 plus any remaining
lint-shaped part of finding 17.

- [x] Re-derive the intended NFC scope from authored source and prose. Do not run duplicate landed
      test files that accidentally scan the whole MAM-basics tree; move enduring lint coverage into
      the canonical suite and delete or demote misleading duplicate tests.
- [x] Make the mark-order lint cover the generator text and generated MAM-simple page named by its
      docstring.
- [x] Give the HTML checker an explicit deploy-root mode for the ten root pages (the review's count
      of nine was stale) while keeping
      subtree stylesheet resolution local to each site. Do not make undefined classes fatal until
      the ownership model can distinguish shared/external CSS from a defect.
- [x] Extend the machine-path lint to program-written Aleppo, Cambridge 1753, MAM-simple, MAM-parsed,
      and MAM-for-Sefaria paths, excluding documented machine-neutral commands rather than whole
      product trees.
- [x] Convert the 50 inherited wrong-order runs in the two Aleppo pages to MAM mark order and add the
      owned Aleppo page family to a mechanical check.
- [x] Compute legacy-history output paths only after the revisions have been resolved to their
      prefixed legacy identities. An adverse probe must prove that a legacy comparison cannot
      overwrite a tracked named-release report.

These are mechanical lint or adverse differential checks, the two test shapes allowed by
`doc/agent-planning-principles.md`. Do not add example-based tests for one Hebrew form or one path.

Expected not to change in Wave 4: the semantic content of generated Hebrew, release-report content,
the source-repository manifests, and any private path.

### Wave 4 execution result — 2026-09-08

- The canonical NFC lint now has ten non-overlapping authored-source and prose scopes. The final
  inventory measured 1,491 MAM-basics files, 3 UXLC files, 44 holman-ketiv-qere files, 3
  book-of-job files, 21 Aleppo files, 13 Cambridge 1753 files, 12 MAM-simple files, 4 MAM-with-doc
  files, 4 MAM-for-Sefaria files, and 7 MAM-parsed files. Four misleading landed-product copies of
  the NFC test were deleted. MAM-simple's now-empty test runner and package marker were deleted with
  its test copy; the canonical suite is the sole entry point for the retained coverage.
- The MAM-simple mark-order scope now comprises 241 tracked text files. Its required-file assertion
  covers both `py/versification_and_cantillation/doc.py` and
  `gh-pages/MAM-simple/versification-and-cantillation.html`.
- The HTML checker now has an explicit `--deploy-root` mode. The review's figure of nine root pages
  was stale: the current deploy root has 10 HTML files. Deploy-root mode checks those 10 files and
  root-local CSS without treating any sub-site as part of the root document tree. The mode passed;
  906 undefined CSS class references were reported informationally rather than made fatal.
- The machine-path lint now scans 1,435 tracked text files. The added program-written groups measure
  83 Aleppo files, 71 Cambridge 1753 files, 122 MAM-simple files, 6 MAM-parsed files, and 82
  MAM-for-Sefaria files. The large verse-text JSON, XML, and CSV families remain outside the scan.
  The copied `MAM-simple/py-examples/mb_cmn/paths.py` retains two exact historical path examples;
  those two excerpts are excluded rather than excluding that file or a product tree.
- The Aleppo page scope comprises all 3 owned HTML files and all 481 Hebrew runs. MAM mark order was
  applied to 48 runs in `missing_sections_nakh.html` and 2 runs in `missing_sections_torah.html`.
  Each current page is byte-for-byte equal to `give_std_mark_order` applied to the page at the
  parent commit; there is zero other content change.
- `diff_mpp.run_from_args` now prefixes legacy revision identities before it computes the default
  output path. The adverse test exercises all 5 named releases and proves that no prefixed legacy
  range selects the corresponding tracked named-release path. The tracked change-log directory did
  not change.
- Black left all 8 changed Python files formatted, Ruff passed all 8 files, `git diff --check`
  passed, all 7 repository checks passed, and the canonical suite reported 981 passed and 5 skipped
  in 131.51 seconds. The current suite output had no subtest line, so this record does not infer one.
  The exact inventories and order-only verifier are under
  `.novc/remediation-review-2026-09-07-wave4/`.
- Expected unchanged surfaces remained unchanged: no release report, source-repository manifest, or
  private path changed. MAM-private remained clean at the authorized Wave 3 golden commit.
- Commit and push: `a42216ee` (`Repair review Wave 4 lint safeguards`) is on `main` and was pushed to
  `origin/main`.
- Next wave: resolve Wave 5's five decision gates before applying the public-record, licence,
  reachability, and remaining prose changes governed by those decisions.

## Wave 5 — decisions, public records, licences, reachability, and remaining prose

Goal: make current public instructions and records describe the landed repository, with each
decision visible. This wave covers findings 7, 9–11, 14–15, 18–21, and the decision-bearing parts of
finding 23.

- [x] Resolve decision gates 1–4 before making their corresponding edit or deletion.
- [x] Correct the fourth-stage and third-stage execution records from current Git objects, manifests,
      source-host READMEs, and generated files. Every numeric correction must name the command or
      scratch script that re-established it.
- [x] Update `doc/PLAN-repo-maintenance-across-GitRepos.md` from the current global maintenance rules,
      including forest manifests, future handoffs, absent-manifest handling, standalone-clone object
      checks, and the distinction between dated task folders and external Claude cache paths.
- [x] Correct live docstrings and comments after re-running their scanners. Preserve an honest dated
      execution record; use a dated correction rather than rewriting the historical action.
- [x] Repair `README.md`, `DATA-LICENSES.md`, and every affected landed README. Re-census
      `gh-pages/img/`: it contains six tracked manuscript crops at `c73a2ad3`, including the new
      Aleppo and Leningrad crops for 1 Kings 7:37. Number every announced count and keep GPL, MIT,
      corpus-text, font, image, and source/product directory scopes distinct.
- [x] Update the MAM-simple redirect-host README through the established host workflow if the dated
      breadcrumb remains missing. Do not leave a permanent source clone in `GitRepos`.
- [x] Apply the reachability decisions and rerun the complete 576-page baseline method against the
      current page count. Record zero dead internal targets and every deliberate orphan by exact path;
      re-measure the page count rather than trusting 576.
- [x] Apply the global prose rules to current files, including the `own` scan, announced-list
      numbering, headings that name their subject, exact referents, and stable names.

Expected not to change in Wave 5: immutable commit messages and trailers, frozen original review
findings, private instruction content, and an orphan decision Ben has not changed.

### Wave 5 execution result — 2026-09-08

- Ben accepted the four actionable recommendations. Redirect-stub `build` and `check` now require
  an explicit `--repo`; both bare commands fail on the missing argument, while an explicit
  wlc-utils scratch build produced 154 stubs plus `404.html` and passed the checker.
- The complete MAM-for-Sefaria safety check found a clean clone whose `HEAD`, `main`, and
  `origin/main` were all `cf23b478`; the only unreachable commit, `34c94a8`, has the same patch ID
  as reachable commit `746d6d2`. The exact clone path was moved to the Windows Recycle Bin and is
  recoverable. The source repository remains represented by its redirect host and the landed
  `MAM-for-Sefaria/` product.
- Retired the five roster-driven files under `misc/linux-sh/`: the three multi-repository shell
  scripts and the two text rosters. Preserved `misc/linux-sh/linux-clone-MAM-basics.sh`, which is a
  standalone bootstrap for MAM-basics and does not declare the multi-repository roster.
- Added the MAM-for-Sefaria product to the deploy-root index and linked MAM-simple's
  `versification-and-cantillation.html` from the MAM-simple index. The complete link graph now
  measures 577 HTML pages, nine pages with no inbound link, and zero dead internal targets. The
  nine deliberate orphan pages are:
  1. `gh-pages/MAM-with-doc/misc/index.html`, retained under the flat MAM-with-doc landing policy;
  2. `gh-pages/MAM-with-doc/tsinnorit_oleh/tsinnorit_and_oleh_on_ivs.html`, a legacy redirect path
     whose target is linked elsewhere;
  3. `gh-pages/book-of-job/index.html`;
  4. `gh-pages/holman/JC3 The Biblical Text in the JC Edition #19-ז - English.html`;
  5. `gh-pages/holman/JC3 The Biblical Text in the JC Edition #19-ז.html`;
  6. `gh-pages/uxlc/clc/2Samuel.html`;
  7. `gh-pages/uxlc/clc/Genesis.html`;
  8. `gh-pages/uxlc/clc/Proverbs.html`; and
  9. `gh-pages/wlc/index.html`.
- Updated the MAM-simple redirect-host README through a temporary shallow clone. Commit `376912a`
  (`Date the MAM-simple evacuation breadcrumb`) is pushed on the redirect host's `main`; the clean
  temporary clone was then moved to the Windows Recycle Bin.
- Corrected the public execution plans, maintenance runbook, landed READMEs, root README, live
  docstrings, and `DATA-LICENSES.md`. The licence table now distinguishes code, analysis, corpus
  text, fonts, manuscript crops, and landed source/product trees and covers all twelve tracked
  Taamey D font copies.
- Ben's decision for the MAS census is recorded in `py/accgram/post_stress_meteg.py` and
  `doc/post-stress-meteg-method.md`: a `מ:קמץ` row contributes exactly one parameter, never both;
  the current selection is `ד`. The `ס` parameter remains available for grouping-difference
  evidence, and no separate effect analysis is required.
- Finding 23.2's worktree housekeeping was left untouched. Ben's decision on 2026-09-08 tracks that
  housekeeping separately, outside remediation completion.

## Wave 6 — final verification and disposition write-back

Goal: prove the combined tree, record every outcome, and leave no finding silently dropped.

- [x] Run black once on all and only the Python files changed by remediation. Use the primary clone's
      interpreter and black's default configuration.
- [x] Run ruff on the changed Python scope and the complete canonical suite.
- [x] Run the repository-standards public sweep with `all-repos.code-workspace` and read the labelled
      report. A changed repository count must be explained by the current workspace, not copied from
      the review.
- [x] Run the relevant product generators and the mega pipeline one final time. The final run must be
      content-idempotent and leave no unexplained generated diff.
- [x] Run the HTML link graph, HTML syntax checks, mark-order checks, NFC checks, machine-path checks,
      vendoring audit, old-host URL census, and `git diff --check`.
- [x] Reconfirm instruction-file identity only if an instruction file changed; finding 22 otherwise
      receives `record only — no remediation required`.
- [x] Append `## Dispositions after remediation, <date>` to
      `doc/review-findings-2026-09-07.md`. Give findings 1–24 and Sol-1 one row each. Each row says
      `fixed`, `already fixed`, `rejected` with the reason, `record only`, `referred to maintenance`,
      or `needs Ben's decision`, and names commits or verified machine state.
- [x] Record the Sol correction for finding 3 and the five exact trailer spellings in the disposition
      prose without rewriting the frozen Claude section.
- [x] Change the review's `State:` line to `acted on 2026-09-08` after every remediation row was
      fixed, rejected with a reason, recorded, referred to maintenance, or placed outside
      remediation by Ben.
- [x] Write the phase result back into this plan after every wave: changed files, commands, generated
      diffs, commits, pushes, unresolved risks, and the exact next wave.
- [x] Commit finished work and push `main`. If execution used a secondary worktree, follow the global
      four-step integration rule immediately before that task is archived: merge `main` into the
      worktree branch, verify in the worktree, fast-forward the primary clone with `--ff-only`, and
      push `main`.

### Wave 6 verification result — 2026-09-08

- Black left all 25 Python files changed in Wave 5 unchanged, and Ruff passed the same 25-file
  scope. The final canonical suite reported 981 passed, 5 skipped, and 65 subtests passed in 120.45
  seconds.
- The public repository-standards sweep passed across the current public workspace repositories:
  MAM-basics, MAM-OSIS, phonetic-hbo, and Taamey_D. MAM-basics reported one linked
  worktree, zero agent branches, zero `sys.path` mutations, zero orphan combining marks, 80 allowed
  hexadecimal escapes, 30 NFC h-with-dot-below findings, and 49 general NFC Latin findings.
- Two consecutive complete mega-pipeline runs each reported 102 scripts, 102 goldens written, and
  zero crashes. No new working-tree path appeared after either pass. The vendoring audit reported
  44 comparison rows and 8 inventory rows covering 44 files.
- `py/check_all.py` passed all seven repository checks:
  1. HTML spell checking;
  2. function ordering;
  3. QR filename/record consistency;
  4. cross-record relations;
  5. Hebrew mark order over 459 files;
  6. unnecessary Unicode escapes over 296 Python files; and
  7. HTML output lint.
- The full HTML graph measured 577 pages, nine deliberate orphan pages, and zero dead internal
  targets. The old MAM-with-doc host census found only three deliberate categories:
  1. one documentation file with 3 hits;
  2. 39 downloaded Sefaria input files with 39 hits; and
  3. 5 byte-verbatim Wikisource-introduction files with 5 hits.
  `git diff --check` passed.
- No instruction file changed, so finding 22 remains record only. The dispositions give findings
  1–24 and Sol-1 exactly one row each and record the five exact co-author trailer lines.
- Wave 5 implementation commit `9cf48863` and Wave 6 disposition commit `975a16c5` are pushed to
  `origin/main` after Ben explicitly approved the 55-file MAM-basics scope.
- Finding 23.2's branch and empty-path cleanup is unrelated worktree housekeeping. Ben's decision on
  2026-09-08 tracks it separately, so it does not delay this remediation's completion.

Run the full suite with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q
```

Run the public standards sweep with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --check-repo-standards --workspace-file all-repos.code-workspace --visibility public
```

The last successful suite before this plan was 976 passed, 5 skipped, and 65 subtests passed. Re-run
the suite and record the new result. A different count is a finding to explain, not an automatic
failure and not a number to overwrite silently.

## Deliberate exclusions from this remediation

1. Do not review the six post-anchor commits or later commits merely because the 2026-09-07 review
   excluded them. They belong to a later periodic-review window; remediation may inspect them only
   where they touch a current finding.
2. Do not extend the public review into MAM-private, github-misc content, hbofonts, source books, or
   private census work.
3. Do not start the unexecuted MAM-OSIS evacuation phases. The fourth-stage open end remains a
   separate programme.
4. Do not rewrite commit history, trailers, or subjects. Findings 23.1, 23.6, and 24 are records, not
   authorization for history rewriting.
5. Do not turn maintenance findings into ad hoc deletion. Task folders, caches, clones, worktrees,
   and branches keep their separate safety and authorization rules.
6. Do not create example-based tests. Use full generated-output comparisons, independent oracles,
   adverse probes, and mechanical lints.

Planning and remediation were completed, committed, and pushed on 2026-09-08. Finding 23.2's
worktree housekeeping remains separate from this completed process.
