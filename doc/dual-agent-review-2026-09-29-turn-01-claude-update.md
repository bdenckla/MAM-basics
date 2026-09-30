# Updates to turn 01 of the 2026-09-29 dual-agent review

State: open, first entry 2026-09-30.

Every entry here corrects or supplements `doc/dual-agent-review-2026-09-29-turn-01-claude.md`, which
is left exactly as written. Ben's decision of 2026-09-11 (D12): a finished dated document is left as
written, like a pushed commit, and a correction, later decision or later disposition goes in a
sibling named `<stem>-update.md`, which is what this file is for turn 01 of the September 29 review.

## Review closed; complete disposition package proposed, 2026-09-30

Prepared by Claude on 2026-09-30, New York time, as close-out step 1 of the round, in response to a
handoff prompt that a Claude session prepared that day and Ben pasted into this session. The prompt
quotes Ben's instruction to that session: "You just say "Close-out step 1 comes next" but you give
no concrete instructions like a prompt to paste into a new session." The rest of the prompt is that
session's reconstruction of the handoff, and this entry checked its facts rather than attributing
them to Ben. The dispositions below are Claude's proposals, not Ben's decisions; a later entry
records his answers. This entry executes no remediation.

**The review is closed and remediation has not started.** Turn 10 accepted every point of turn 09
and listed no unresolved disagreement, and turn 11 acknowledged turn 10 without an objection, which
satisfies the stopping rule in `doc/dual-agent-review.md`; no objection remains for Ben to resolve
before close-out. The controlling passages are `doc/periodic-review.md`, "The check runs
autonomously, and Ben sees the findings once", "Close-out: from findings to dispositions",
"Separate defects from editorial proposals" (D7) and "Present remediation by public-facing risk".
Every proposed fix defaults to later, in the remediation phase. Approval of this package decides
what the step-2 remediation plan includes, defers or records as resolved. It approves no
unspecified editorial wording, and agreement between the reviewers approves nothing.

### Sources, checkout and merge

The evidence is turn 01's findings 1 to 36 and the reconciliation table appended to it, read with
turns 02 to 11: the corrections listed under "Close-out inputs" in turns 03, 07 and 09, which turn
11 left unchanged, and the objections that turns 04, 06, 07, 08 and 09 raised and later turns
settled, the last of them in turn 10. C1 is turn 02's omission, which turn 03 added to the findings
as an unfixed docstring overclaim. The reviewed window remains `f4d81285..7549ebf7`; the
measurements on the merged branch below neither enlarge it nor rewrite its findings.

The checkout is the full clone `C:/Users/BenDe/GitRepos2/MAM-basics`, on its local carrier
`dar-2026-09-29` for `origin/dar-2026-09-29`. After a fetch, `HEAD` and the remote branch were both
the required commit `a62ca604a92be552bc2de9eb169345f1062981a5`, turn 11, and the tree was clean. As
D11 requires of every close-out task, current `origin/main`,
`303bf2399c1e1fc1300a75f4fb1ed335d62984d0`, was merged into the review branch before editing, as
`c344c5dfdd47d1c603904732e0c4375a24cf6fb4` at 14:10:19 New York time, and pushed. `git merge-tree`
found no conflict, and the merged tree is `origin/main`'s tree plus the eleven turn files, so the
merge owed neither the suite nor the mega. The handoff prompt named `21ade9da` as `origin/main`; by
this session's fetch `main` had also gained `303bf239`, which changes only
`doc/PLAN-automate-the-dual-agent-review-relay.md`, an unapproved plan that changes nothing in this
close-out.

This session is the only writer in the checkout. Four read-only sub-agents checked a draft of this
entry against turns 01 to 11 and the merged tree, and edited nothing: S1 took findings 1 to 9 and
question 5; S2 findings 10 to 21, C1 and questions 1 and 6; S3 findings 22 to 35, E1, questions 3
and 4 and the section below on what is already resolved; and S4 finding 36, question 2, the framing
sections and a completeness audit. This session re-read the source of every correction it adopted.
This session and the four sub-agents ran at `max`, the level `doc/periodic-review.md`, "The effort
a review runs at", sets for a Claude review turn: the app's session record shows it, and so does
every assistant record of this session's transcript and of the four sub-agents' transcripts, which
this session read for that field alone after Ben asked about the level. Nothing below depends on
it. No MAM-private content was read. The task that executes the approved step-2 plan, close-out
steps 3 and 4, owns final integration; this task integrates nothing into `main`.

### What is already resolved on the merged branch

`main` changed 36 paths between `7549ebf7` and `303bf239`. Every cited file among them was re-read
on the merged tree; the other cited files are unchanged since `7549ebf7`. Four subitems, in two
groups, no longer hold there:

1. **4.1's first site and 4.6.** `e4934b6e` retired
   `doc/PLAN-remediate-review-findings-2026-09-14-update.md` and
   `doc/PLAN-symmetric-CLAUDE-and-AGENTS-instructions-update.md` with their receipt families, which
   remain at `eea4c583`, so no live update makes either claim.
2. **28.1 and 28.2.** `4d3ebf66` rewrote the refresh skill's interpreter passages and the
   `hebrew-prose` skill's test command in `references/verifying.md` to name the selected full
   clone's own interpreter, or a linked worktree's home-clone interpreter by absolute path.

`e4934b6e` also retired the executed Google Sheet plan that item 36.9 concerns. Every other cited
defect remains on the merged tree. `main` appended entries to four open updates that the findings
cite, and in two further open updates it replaced the retired Sheet plan's path with a link to its
archive, at the very passages findings 1.3 and 4.3 cite; none of those edits removes a defect.
Some cited lines moved:

1. `dot-Codex/user-wide-AGENTS.md`: turn 01's lines 36 to 242 rise by two and those after 242 by
   ten, so the rule finding 11 cites, `:325–326`, is now `:335–336`.
2. `doc/dual-agent-review.md`: `:143`, `:170–171`, `:173`, `:223–224`, `:274–276` and `:486–490`
   are now `:147`, `:174–175`, `:177`, `:234–235`, `:286–288` and `:498–502`.
3. `doc/PLAN-remediate-review-findings-2026-09-26.md`: every line from 4 on rises by one, below its
   new line-4 pointer.
4. `dot-claude/skills/mam-wikisource-refresh/SKILL.md`: `:60–62` and `:66–67` are now `:82–84` and
   `:88–89`.
5. `dot-claude/skills/hebrew-prose/references/verifying.md`: `:57`, `:93` and `:112–115` are now
   `:62`, `:98` and `:118–121`.
6. `dot-claude/skills/github-issues/references/reading-and-writing.md`: `:61–64` is now `:63–66`.

### Complete proposed disposition list

**Plan a fix** means a defect survives and its remedy belongs in the step-2 plan, to be carried
out later, in the remediation phase. **Plan a proposal** means the review found no defect but the
step-2 plan presents a change for Ben's approval. **Defer** leaves the item unfixed for the named
decision or evidence gap. **No action** changes nothing, for the stated reason. **Already
resolved** applies only to the named subitem, measured on the merged branch. **Ben's decision** is
one of the questions below. The bracket after each item separates, under D7, a **defect** (a
reproducible code or data defect), **approved wording** (wording Ben has already approved, or a
form a recorded rule prescribes, which the plan follows without asking again), **editorial**
wording (which the step-2 plan presents for Ben's approval before it is applied) and a **choice**
(decided in this close-out). It also marks, in `doc/periodic-review.md`'s high-risk categories,
**public data** (distributed corpus data) and **reader-facing** changes (rendered HTML, or Markdown
written for readers, such as a README or a licence page); plans, review records and working notes
under `doc/` are lower risk, like every item marked neither.

1. **Plan a fix:** restore the approved order, `NARPAS_GROUPING_RULE` before
   `MAM_PARSED_WHITESPACE_TEMPLATE_RULE` in `py/mb_cmn/public_data_consumer_notice.py`, so that the
   consumer notice in all 24 `MAM-parsed/plus/` files and in
   `gh-pages/MAM-parsed/plus/html/mpplus.html` glosses narpas before using it (1.1); repair
   `py/tmpl_survey/stack_path_lookup.py:75`, whose `paths` the local `paths` of line 76 shadows, so
   that `--find-stack-path` and `--find-stack-path-verbose` stop raising `UnboundLocalError` (1.2);
   and restore the two corrections of `87fc7141` that the merge `ebbfa90f` dropped from
   `doc/blind-dive-into-template-params-update.md` (1.3) [1.1 defect, its fix restoring approved
   wording, public data and reader-facing; 1.2 defect; 1.3 editorial, proposing `87fc7141`'s own
   wording].
2. **Plan a fix:** complete at every named site the approved 2026-09-26 changes that did not land
   in full (2.1 to 2.5; 2.6 is findings 4.2 and 4.3), 2.5 by applying the 2026-09-26 plan's "Make
   skill routing agent-specific" to the three every-reader routings turn 01 names, the common
   body's `:84` and `:302` and the live September 9 plan's `:77–78`, which is turn 01's reading of
   that plan; and add a dated entry to `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`
   recording that rows 3, 5, 6, 11, 29 and 30 of its execution table overstated what landed, that
   the merge `ebbfa90f` of finding 1 made row 24 false, and when each change was completed
   [approved wording for 2.1 and for 2.4's "folio 57a", which the 2026-09-26 plan worded;
   editorial for 2.2, 2.3, 2.4's "folio 307b" and 2.5, which it only directed, and for the dated
   entry; 2.1's `in/mam-ws-intro/README.md` is reader-facing, and so is 2.4's
   `doc/meteg-after-silluq-snips/README.md`, which the 2026-09-26 plan's approval surface treated
   as reader-facing and `evr-ii-b-55/README.md` links; 2.5's common-body change is deployed with
   `--sync-user-config`].
3. **Plan a fix:** replace the Evr. II B 55 README's heading "Segmentation of Psalms, Job and
   Proverbs", which the approved 2026-09-26 plan supplied and which names the wrong books (3.1),
   and its sentence that `get_verse_words` drops an atom at Psalms 10:5, which the 2026-09-26
   remediation made false (3.2) [editorial; reader-facing].
4. **Plan a fix** for 4.1's second site, `doc/review-findings-2026-09-14-update.md:100–104`,
   together with its pointer at `:104` to the September 14 plan's update, which `e4934b6e` retired,
   for 4.2 to 4.5 and for 4.7 to 4.9, correcting each open update or maintained document in place,
   while 4.1's first site and 4.6 are already resolved by that retirement [editorial; 4.5's file is
   in the shared `hebrew-prose` skill, so its fix is deployed with `--sync-user-config`].
5. **Plan a fix:** bring 5.1's module docstring, 5.2's search hint, 5.3's comment, 5.4's two
   docstring claims and 5.5's module docstring into agreement with the code, the data and each
   other, and drop the `overlay_class` parameter of `focus_fade_img`, which no caller has passed
   since `22d18d72`, keeping its default value in the body (5.6) [5.1 to 5.5 editorial; 5.6
   defect].
6. **Plan a fix:** make the force-flag lint catch aggregated short options such as `-df` and `-ff`
   (6.1), make the cluster lint check a mark that follows a `gray-maqaf` span (6.2), and restore
   the fingerprint assertion that `22d18d72` dropped from
   `test_exact_relocation_citations_gate_and_survive_retirement` (6.3), each within the rule that
   tests be differential or lint-shaped [defects in tests].
7. **Plan a fix** under the recommended choice below: `.novc/t`, the directory under which the
   suite puts its per-process base temporary directories on Windows, stops gating worktree
   retirement, while every other retained `.novc` child keeps gating as the 2026-09-26 plan
   specified [choice; defect against the stated rule "Generic `.novc` policy prose does not
   gate."].
8. **Plan a fix** for 8.1: the step-2 plan presents the hazard-5 re-reading, and the September 9
   plan's section "Current execution boundary, corrected 2026-09-28" with its rewritten
   procedures, which the 2026-09-26 remediation (`22d18d72`) applied without the approval D7
   requires, for Ben's approval or reversal; 8.2 is question 5 [8.1 editorial and choice; 8.2
   choice].
9. **Plan a fix:** give `doc/post-stress-meteg-image-provenance-update.md` and
   `evr-ii-b-55/evr-ii-b-55-images-provenance-update.md` the recorded form `State: open, first
   entry 2026-09-28.` (9.1), and, under the recommended choice below, leave the Evr. II B 55
   provenance base as it stands while recording its four passages changed in place on 2026-09-28,
   by their words and their commit `db152332`, in its update (9.2) [9.1 approved wording, the
   recorded form; 9.2 editorial and choice].
10. **Plan a fix:** make `DATA-LICENSES.md` describe the five product licence files as they now
    stand, replacing its claim that "The same file stands as `LICENSE.md`" in the five product
    directories, its copy of the old wrapper and the gloss at `:134–135` on a phrase only that copy
    contains (10.1, with question 6 deciding whether the product files change too), and drop
    "plain" from its `MAM-parsed/` row (10.2) [editorial; reader-facing].
11. **Ben's decision** (question 1): whether he asks for any of the five stub test ids in
    `py/tests/test_wikisource_special_page_download.py`, which both reviewers class as
    example-based, while the sixth id, the inventory check, is lint-shaped and stays, and no action
    is proposed for the fourteen pre-window example-based methods of
    `py/tests/test_main_download_fr_wikisource.py`, one of which `a41fbcdd` extended with a mock of
    the special-page download and two assertions about its call, since turn 01 cites them as the
    older pattern rather than as part of the finding [choice].
12. **Plan a fix:** say in `AGENTS.md` and in `py/ws/ws_special_page_download.py`'s docstrings
    that the special-page inventory is checked against chapter 2's Decalogue section, its table and
    the paragraph after it, and against its song-form table, rather than against "the two tables":
    the two tables give 35 titles, and the paragraph gives the 36th [editorial].
13. **Plan a fix:** date or re-source the claim in `in/mam-ws-intro/README.md` and in
    `py/subcommands/download_wikisource_intro.py` that five of the thirteen pages were edited in
    August 2026, which the committed manifest stopped supporting at `c450060e` [editorial; the
    README is reader-facing].
14. **Plan a fix:** remove the dead `"google/"` and `"plain/"` lint exclusions (14.1) and the
    unused import and the dead constant with its JSON snippet (14.2); in 14.3's five-site
    inventory, correct the two false documentation references,
    `py/author_misc/mp_cmn_top_header_book39.py:2` and
    `py/author_misc/mp_cmn_examples_and_file_naming.py:12`, and, under the recommended choice
    below, reword the three passages that name the transient parser stage with the retired
    product's name; and replace the bare-path citations of deleted files at
    `py/hkq_cmn/qere_ending_search.py:28–29`, `py/main_search_final_hiriq_verse_text.py:24–26` and
    `py/ws/ws_bot_edit_sigil_b2_to_t451.py:38–40`, keeping the receipt `py/ws/ws_bot_edit_history.md`
    as written (14.4) [14.1 and 14.2 defects; 14.3 editorial and choice; 14.4 editorial].
15. **Plan a fix:** make the check that plus holds no parser-stage encoding descend into the tuple
    verse rows it is given, so that an injected `{"stmpl": ...}` node fails
    `validate_plus_conversion` [defect, in the validation of distributed data].
16. **Plan a fix:** give the parser-stage grammar lock a tracked regeneration command and a
    provenance line that names it [defect].
17. **Plan a fix** under the recommended choice below: compare every D-column label parameter,
    `סדר` among them, between the parser stage and plus in `validate_plus_conversion` [choice;
    defect in validation coverage].
18. **Plan a fix:** restore a working recovery pointer for the Cambridge 1753 line-break editor,
    which `f4d81285` does not hold and `4ac4f16a` does (18.1), and state that the retained
    line-break data continues after Job through Proverbs 1:30 and the first three of Proverbs
    1:31's five atoms (18.2) [editorial; reader-facing].
19. **Plan a fix:** qualify "No program in this repository makes crops now" in
    `doc/boj-image-crop-reproducibility.md`, since `py/accgram/scan_page.py` and
    `py/accgram/transcription_editor.py` crop printed-edition scans [editorial].
20. **Plan a fix:** in `hbce-psalms/README.md` and in `DATA-LICENSES.md`'s `hbce-psalms/out/` row,
    which describe the changes CC BY 4.0 asks a reuser to indicate, add the substitution of U+05B9
    HEBREW POINT HOLAM for U+05BA HEBREW POINT HOLAM HASER FOR VAV to the two changes they name,
    and say how the outputs treat the U+05C0 (Unicode PASEQ) that HBCE holds inside a `<w>`
    element and 112 comparison cells print after an inserted space [editorial; reader-facing, the
    licence file included].
21. **Plan a fix** under the recommended choice below: record 21.1's two identical "ML vs MAM
    (Leningrad)" headings and 21.2's overbroad "Everything it cites" sentence in a new update file
    for `doc/hbce-psalms-vs-mam-2026-09-26.md`, and leave `py/hbce_psalms/compare.py` and
    `hbce-psalms/out/` unchanged until the HBCE work resumes, because a change to that hand-run
    generator would owe a rerun that Ben's frozen-record decision of 2026-09-26, which covers a
    change to MAM's data, does not waive [21.1 defect, its code fix deferred; 21.2 editorial;
    choice].
22. **Defer:** the public evidence shows only that the post-stress-meteg survey's tracked output
    and phonetic-hbo's 2 Kings 22 page lack 2 Kings 22:1's new qamats variant, while the survey's
    Phonetic MAM input, in MAM-private, is unchecked, the cause is not established, and
    `py/accgram/post_stress_meteg.py` permits the snapshot to lag; the next dependent refresh is
    where to check that the variant reaches phonetic-hbo's page and changes the survey's prose
    `variant_rows`, now 309 [deferred for that evidence gap; no MAM-basics change proposed].
23. **Plan a fix:** state in the refresh skill's post-bot section and in
    `py/ws/pywikibot-setup.md` that a bot run's post-run download, which calls
    `download_wikisource.run`, the function every `fr-wikisource` download runs, also
    force-refreshes all 36 special pages [editorial; the skill fix is deployed with
    `--sync-user-config`].
24. **Plan a fix:** in `MAM-parsed/historical/README.md`, tell apart the loose JSON of 2026-09-06
    and the ZIP archives of 2026-09-10 (24.1), and state each change-log run form's guard, none for
    explicit `--old`/`--new`, the latest release's end for a run without arguments, and every
    boundary for `--all`, `--check` and the mega's step, with turn 09's two details on `--pin` and
    on "stored" meaning listed in the manifest, aligning the module docstring of
    `py/subcommands/diff_mpplus.py`, whose list of refusing runs turn 03 found silent on the
    no-argument run's single boundary (24.2) [editorial; reader-facing, inside the distributed
    `MAM-parsed/`].
25. **Plan a fix** under the recommended choice below: give a timeout to the nine of the 30
    process-launching call sites in `py/repo_util/forest_sync.py` and
    `py/repo_util/forest_environments.py` that run Git unbounded, and noninteractive settings to
    the three of them that go through `worktree_retirement_git._git`, so that
    `doc/clone-forests.md:66` holds [defect; choice].
26. **Plan a fix** under the recommended choice below: in the forest synchronizer's write form,
    judge the conditions a clone's own state decides (dirty, off `main`, mid-operation, occupied)
    before any fetch, and state exactly what the fetch touches in a clone that form then refuses,
    leaving the check form's fetch of every clone as `doc/clone-forests.md:20–23` describes it
    [choice; defect against the stated rule].
27. **Plan a fix:** add `-c constraints.txt` to the root README's install command [editorial;
    reader-facing].
28. **Plan a fix** for 28.3 to 28.6, making their live commands and working directories
    checkout-neutral, with the ten further runbook lines that turn 07 added to 28.4 and rows for
    `--sync-forest` and `--forest-status` in the runbook's action table, while 28.1 and 28.2 are
    already resolved by `4d3ebf66` [editorial; 28.6's `hbce-psalms/README.md` is reader-facing; the
    skill fixes are deployed with `--sync-user-config`].
29. **Plan a fix:** replace both configuration READMEs' "The read-only form" with a label that
    agrees with the common body's "fetches and compares without changing live configuration"
    [editorial].
30. **Plan a fix:** preserve in a tracked record the approved public additions that P01–P26,
    N01–N08 and A01–A02 label, read from the untracked proposal in
    `C:/Users/BenDe/GitRepos/MAM-basics/.novc/` after a check that nothing private or taken from
    memory text is published, in a step that runs in that clone because the proposal is
    checkout-local; the proposal still existed, 95,251 bytes, at 14:50 New York time on 2026-09-30,
    and until the fix lands a default `py/main_repo_maintenance.py` run there can delete the only
    list any tracked record points to [editorial].
31. **Plan a fix:** repoint the two live citations of retired auto-memory notes,
    `py/repo_util/run_black.py:30–32` and `py/accgram/lexical_validation.py:32`, to tracked
    evidence, or state the decision without a memory pointer where no tracked record holds its
    reasoning; as turn 07 narrowed it, the approved retirement removed the 247 approved desktop
    files and leaves laptop execution open, so the finding rests on the common body's rule against
    consuming auto memory as current guidance [editorial].
32. **Ben's decision** (question 3): whether the common body's rule names the scan archive's
    default location or the code requires `BOOK_SCANS_ROOT` [choice; a common-body change is
    deployed with `--sync-user-config`].
33. **Ben's decision** (question 4): where the merge belongs when `origin/main` moves during a
    worktree's integration, which also settles the Codex lifecycle reference's missing fetch step
    and refused-push branch [choice; a common-body change is deployed with `--sync-user-config`].
34. **Plan a fix:** name `references/repository-maintenance.md` in the four citations of "Manual
    document retirement", or route document retirement there from the skill (34.1); correct the
    `github-issues` reference's open-or-closed review-State shorthand (34.2); and make
    `verifying.md`'s "while this paragraph read "Never"" readable without the removed quotation
    (34.3) [editorial; the skill fixes are deployed with `--sync-user-config`].
35. **Plan a fix:** make `doc/dual-agent-review.md`'s September 16 paragraph name the current
    shared-remote-branch exception instead of "the backup exception recorded above", and correct
    the open 2026-09-26 update's "The shared worktree" to "The shared origin branch" in place
    [editorial].
36. **Record the twelve items' individual dispositions** in the table under "The items of finding
    36": two are Ben's decisions, questions 2 and 6; one is no action because its plan was retired;
    two are proposals for the step-2 plan; one is no action in remediation; and six are deferred
    [choices; 36.10 and 36.12 editorial; 36.12 reader-facing].
37. **C1, plan a fix:** replace the promise of `py/ws/ws_special_page_download.py:441` to
    "atomically replace the special-page mirror" with the per-file replacement and manifest-last
    sequence the module implements, and say that a failed page replacement leaves
    `<slug>.tmp.mediawiki`, which stops every later run, a saving bot run's post-run download
    included, until a person deletes it [editorial].
38. **E1, from the exchange, plan a proposal:** turns 07 and 08 agreed that D9's "uses public
    evidence only" (`doc/dual-agent-review.md:147`) means not reading MAM-private, with D11
    excluding a claim that only a transcript can check; the step-2 plan proposes wording that says
    so [editorial].

### Questions for Ben

Each question gives the facts needed to answer it and is asked in a dialog. Where a question has a
recommendation, the recommendation is its first option.

1. **Finding 11: which of the five stub test ids do you ask for?** The rule: "Do not add an
   example-based unit test that pins one selected case, string, or name unless Ben asks"
   (`dot-Codex/user-wide-AGENTS.md:325–326` at `7549ebf7`, now `:335–336`). Both reviewers class
   five of the six test ids that `a41fbcdd` added in
   `py/tests/test_wikisource_special_page_download.py` as example-based. Four fault-injection ids,
   holding five cases, check that a bad API response or bad local metadata stops the download;
   four of those cases also check that no existing special-page file changed, and the remaining
   case, a manifest overwritten with "not json", checks only that the download raises. Turn 01's reason
   for an exception is that this refuse-to-replace property has no regenerable artifact. The fifth
   id, the round trip, pins one scenario's counts, call kinds and write order, and compares 36
   pages its stub composes with the downloader's copies. The property its comparison checks, byte
   preservation, has a regenerable artifact, the mirror under `in/mam-ws-special/`, whose
   regeneration needs Wikisource; its stub pages hold none of the 44,598 Hebrew combining marks of
   the tracked mirror. Its possible reason is its offline coverage of reuse and forced refresh, and
   neither behaviour shows in a regenerated mirror's diff: a reuse that fetched every page anyway,
   or a forced refresh that fetched none, would leave the same bytes in the mirror and in
   `manifest.json`, which records no retrieval time. The options, with no recommendation because
   the facts cut both ways: keep all five under an exception; keep the four fault-injection ids
   under an exception and remove the round trip; or keep none.
2. **Item 36.2: which rule governs the hand-run products after a Wikisource refresh?** The refresh
   `97c4aff5` changed MAM-simple at Judges 19:23 and 2 Kings 22:1, and MAM-for-Sefaria's rows for
   both verses and MAM-OSIS's `MAPM-24` files and `mapm.osis.xml` still hold the old words there.
   `AGENTS.md:163–164` says a change to a hand-run generator, "or to any input it reads, requires
   rerunning every affected hand-run generator and inspecting its tracked outputs", and
   `py/product_scopes.py:51–53` that it "owes rerunning every affected generator and inspecting
   every tracked output it writes". Both products' READMEs say "This product is not kept
   continuously current, and has not been since 2026-09-12.", the date of Ben's decision that
   `py/product_scopes.py` records and quotes: "I know of no reason to be supplying
   constantly-updated versions of these." After the previous refresh, `61aa48ee` (2026-09-18)
   reran both generators; since then the MAM-simple data they read has changed only at those two
   verses. The options: allow the lag, amending `AGENTS.md` and `py/product_scopes.py` so that a
   MAM text refresh does not oblige rerunning `py/main_mam4sef.py` and `py/main_mam_osis.py`, as
   `AGENTS.md` already says of the HBCE comparison, while a change to either generator's code still
   does; rerun both in remediation and keep the rule, a public-data change at the two verses; or
   rerun both once in remediation and amend the rule for later refreshes.
3. **Finding 32: which side changes, the rule or the code?** The common body says inputs outside
   every repository are "discovered through explicit account configuration such as
   `BOOK_SCANS_ROOT`" (`dot-Codex/user-wide-AGENTS.md:133–135`), but `py/mb_cmn/paths.py:133–136`
   falls back to `~/OneDrive/Documents/ScansOfBooks` when the variable is unset, and `f368a305`
   records that neither the desktop nor Ben's laptop set the old variable. The options: reword the
   rule to name the default location, with `BOOK_SCANS_ROOT` as its override, changing no code or
   machine; or make `book_scans_root()` fail when the variable is unset and set it on each machine.
4. **Finding 33: where does the merge go when `origin/main` moves during a worktree's
   integration?** The common body's rule for pushing a full clone's `main`
   (`dot-Codex/user-wide-AGENTS.md:125–128`) fetches and merges first and, after a push refused
   because `origin` moved, says to "repeat the fetch, merge and affected checks in that full
   clone". A worktree's home clone is a full clone, but `:85–86` say it "receives only a verified
   fast-forward", and `:166–168` send a refused fast-forward back to the worktree. No text sends a
   push refused after the home clone's fast-forward back to the worktree; read literally,
   `:125–128` put that merge in the home clone, which `:85–86` forbid. The Codex lifecycle
   reference (`dot-Codex/skills/codex-worktree-tasks/references/task-lifecycle.md:53–58`) has no
   fetch step and no refused-push branch. The options: keep the home clone fast-forward-only,
   scoping the fetch-and-merge rule to ordinary full-clone work as `doc/clone-forests.md:88–90`
   already does and giving worktree integration, in the common body and the lifecycle reference,
   a fetch before the fast-forward and a refused-push branch that returns to the worktree; or
   allow a merge in the home clone after a refused push and relax "receives only a verified
   fast-forward".
5. **Finding 8.2: should the page and folio terminology get a standing home?** Ben's terminology
   of 2026-09-27: a folio has an A and a B page, "F159A" or "page F159A" names a page, and forms
   like "folio 57a" are avoided in the repository's own prose and read as "(folio 57)a" in
   others'. His statement is recorded only in
   `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`, whose first entry left whether to
   give it a standing home "for the remediation plan to ask"; the plan did not ask, and no
   instruction or skill carries the terminology. Some prose already follows it
   (`doc/meteg-after-silluq-snips/README.md:54–55`, `evr-ii-b-55/README.md:168`), and some does
   not: finding 2.4's two locators; "folio 57a" at `evr-ii-b-55/README.md:194` and `:485`, in a
   reader-facing README, from before the window; the `hebrew-prose` skill's own "folio 009B"
   (`references/sources-and-corpora.md:46`); and the `verse-links` skill and its generator, which
   call a Leningrad Codex page a folio (`dot-claude/skills/verse-links/SKILL.md:70` and `:95`,
   `py/main_verse_links.py:209–212`). The options: add it to the shared `hebrew-prose` skill,
   widening the skill's description, which covers accentuation prose and
   manuscript-versus-transcription prose, to take in manuscript locators, with the wording and
   the conforming edits proposed in the step-2 plan; put it in a MAM-basics document, such as
   `doc/meteg-after-silluq-snips/README.md`, which already defines a page; or give it no standing
   home and fix only finding 2.4's two locators.
6. **Item 36.1 with finding 10.1: how should the five product licence files read?** Since
   `a41fbcdd`, `LICENSE.md` in `MAM-parsed/`, `MAM-simple/`, `MAM-with-doc/`, `MAM-for-Sefaria/`
   and `MAM-OSIS/`, one blob, opens "The statement below is preserved verbatim from the former MAM
   Google spreadsheet", while the statement still speaks of the material "as found in this
   spreadsheet". The wrapper dropped the sentence "This information applies equally to the data in
   this GitHub repository.", which `DATA-LICENSES.md:134–135` reads as the MAM paths named in its
   table. `DATA-LICENSES.md` still copies the old wrapper, says "The same file stands as
   `LICENSE.md`" in the five product directories, and gives each product's terms "as
   `<product>/LICENSE.md` states". Of the five product READMEs, only `MAM-simple/README.md:89`
   names a licence: "MAM-simple is available under CC BY-SA 4.0." The options: add to the five
   wrappers a sentence saying that the statement covers the data in that directory, a change to a
   licence file in each distributed product, with `DATA-LICENSES.md` then describing the files as
   they stand; keep the five files as they are and correct only `DATA-LICENSES.md`; or correct
   `DATA-LICENSES.md`'s stale claims in remediation and defer the question of whether each grant is
   clear.
7. **The package: "Do you approve the proposed fixes, deferrals, and no-action dispositions?"**
   This last question covers every disposition in the list above, the table of recommendations and
   the table of finding 36's items below, and Ben's answers to questions 1 to 6. It approves no
   unspecified editorial wording.

### Recommendations the package approval covers

| Finding | Recommended decision |
|---|---|
| 7 | Treat `.novc/t`, under which the suite puts its per-process base temporary directories on Windows, as disposable cache that does not gate retirement; every other retained `.novc` child keeps gating, as the 2026-09-26 plan specified. |
| 8.1 | Present the hazard-5 re-reading and the September 9 plan's section "Current execution boundary, corrected 2026-09-28" with its rewritten procedures, as they stand, for approval or reversal, with findings 2.5 and 28.5 applied to whichever wording survives. |
| 9.2 | Leave the finished base as it stands and record the four passages, with `db152332`, in its update, following the 2026-09-26 plan's rule that later facts go in updates while the bases keep their original State and header (`doc/PLAN-remediate-review-findings-2026-09-26.md:308–309` and `:319–320`). |
| 14.3 | Correct the two false documentation references; reword `py/ws/ws_plain.py:1` and `:59` and `py/py_misc/mam_parsed_plus.py:33–34` to name the parser stage, under the whole sentence of `doc/PLAN-retire-mam-parsed-plain.md:349–351`, renaming no identifier. |
| 17 | Extend the comparison to every D-column label parameter, reading "labels" in `doc/PLAN-retire-mam-parsed-plain.md:366–368` apart from its "coordinates" and "aliyah records". |
| 21 | Record both defects in a new update file for `doc/hbce-psalms-vs-mam-2026-09-26.md`, and defer the heading fix in `py/hbce_psalms/compare.py` until the HBCE work resumes and reruns the comparison: Ben's 2026-09-26 decision exempts only a change to MAM's data from the rerun that `AGENTS.md` requires after a change to a hand-run generator. |
| 25 | Bound the nine unbounded Git call sites, give the three helper calls noninteractive settings, and keep `doc/clone-forests.md`'s sentence. |
| 26 | In the write form, check the conditions a clone's own state decides before fetching, and describe the remaining fetch exactly. |

### The items of finding 36

| Item | Proposed disposition and reason |
|---|---|
| 36.1 | Ben's decision, question 6, with finding 10.1. |
| 36.2 | Ben's decision, question 2. |
| 36.3 | Defer: whether an in-place correction of a claim that was false when written needs a dated note is a receipt-policy question; no retroactive marking of the eight update files that lack one is proposed. |
| 36.4 | Defer: only Ben can supply the words of his 2026-09-28 decision that D11's heading names, and of the remediation's execution-location amendment and branch-deletion authorization; no attribution is reworded without them. |
| 36.5 | Defer judgment on the published memory topics and MAM-private metadata, as the 2026-09-26 package deferred its items 35.1 and 35.2; editing the tip would not unpublish what is pushed. |
| 36.6 | Defer: differential tests of the forest modules and of the freshness guard's failure path would be within the rule, and whether to add them is a policy choice that this package does not make. |
| 36.7 | Defer whether a loanword like "taamim" or "haazinu" is a Hebrew filename component; no action on the four pre-rule slugs, which the approved 2026-09-26 plan chose to keep. |
| 36.8 | No action in remediation: removing the Sheet link from the English Decalogue page is an outward-facing Wikisource edit, Ben's to make; the mirror records any change at its next download. |
| 36.9 | No action: `e4934b6e` retired the executed Google Sheet plan to its archive at `eea4c583`, and with the Sheet frozen the 17 unreconciled differences are moot. |
| 36.10 | Plan a proposal: the step-2 plan presents the `NOT_IN_MEGA` reason for `py/main_hbce_psalms.py lint-receipt` for Ben's review, so that "not yet reviewed by Ben" can go; running it in the suite is deferred. |
| 36.11 | Defer: whether a validator must itself dispatch over every recognized template is a question of the closed-dispatch rule's scope; no change is proposed. |
| 36.12 | Plan a proposal for a short account of the plain retirement in `MAM-parsed/README.md`, reader-facing in a distributed product, with its wording in the step-2 plan; no action on `cam1753/cam1753-page-index.json:3`, which the codex-index plan left because no retained JSON may change. |

### Defects and editorial proposals, separated under D7

1. **Reproducible code and data defects, fixed to the prescribed or recommended behaviour:** 1.1,
   whose fix restores approved wording in distributed data; 1.2; 5.6; 6; 7; 14.1; 14.2; 15; 16;
   17; 25; and 26.
2. **Approved wording and recorded forms, followed without asking again:** 2.1 and 2.4's "folio
   57a", which the 2026-09-26 plan worded, and 9.1's State form.
3. **Editorial proposals, whose wording the step-2 plan presents for approval:** 1.3; 2.2; 2.3;
   2.4's "folio 307b"; 2.5; item 2's dated entry; 3; 4; 5.1 to 5.5; 8.1; 9.2; 10; 12; 13; 14.3;
   14.4; 18 to 20; the record of 21.1 and 21.2 in the receipt's new update file; 23; 24; 27 to 31;
   34; 35; C1; E1; 36.10; 36.12; and whatever questions 1 to 6 add.
4. **Choices for Ben:** questions 1 to 6, and the table of recommendations.
5. **Deferred, no action, or already resolved:** 21.1's code fix in `py/hbce_psalms/compare.py`;
   22; 36.3 to 36.6, 36.8, 36.9 and 36.11; 36.7's loanword question and its four slugs; the suite
   run 36.10 leaves deferred; 36.12's page-index JSON; the fourteen pre-window test methods named
   in item 11; and the resolved subitems 4.1's first site, 4.6, 28.1 and 28.2.

### Reader-facing documents and public data: the step-2 plan's approval surface

1. **Reader-facing documents, high risk.** 1.1's `gh-pages/MAM-parsed/plus/html/mpplus.html`;
   `in/mam-ws-intro/README.md` (2.1 and 13); `doc/meteg-after-silluq-snips/README.md` (2.4);
   `evr-ii-b-55/README.md` (3); `DATA-LICENSES.md` (10 and 20); `cam1753/README.md` and
   `cam1753/doc/cam1753-line-break-task.md` (18); `hbce-psalms/README.md` (20 and 28.6);
   `MAM-parsed/historical/README.md` (24); the root `README.md` (27); and, if Ben chooses them, the
   five product `LICENSE.md` files (question 6), the conforming edits of question 5's first
   option, and `MAM-parsed/README.md` (36.12). The plan shows current and proposed wording for
   each.
2. **Public data, high risk.** The one proposed change is 1.1's consumer notice, the
   `header.consumer_notice` of all 24 `MAM-parsed/plus/` files; every Scripture payload stays
   unchanged, and no change to MAM's own text is proposed. Question 2's rerun options would carry
   the refresh's two existing changes, at Judges 19:23 and 2 Kings 22:1, into MAM-for-Sefaria and
   MAM-OSIS.
3. **Lower-risk changes.** Live Markdown under `doc/` and update entries; Python docstrings and
   comments; agent instructions, both `AGENTS.md`, which takes effect when committed, and the
   common body and skills, which take effect when deployed with `--sync-user-config`; and code and
   tests.

### What this package leaves as it is

The sections of turn 01 headed "Noticed outside the diff, not findings" and "Open ends the window
itself declares (not findings)" hold no findings and receive no disposition; nothing in them is
proposed for remediation. The timing of turns 03 and 05 stands as turns 07 to 10 left it: turn 03
was written between 15:13:27 and 16:03:24 and turn 05 between 16:10:24 and 16:13:11, New York
time, the public record does not establish the exact times, and turn 05's "at about 16:15" is
shown neither wrong nor right. Those corrections live in the turns that made them and need no
remediation.

### Verification of this entry

This entry changes only this file and inserts, as line 4 of
`doc/dual-agent-review-2026-09-29-turn-01-claude.md`, the pointer to it, the base's one permitted
post-completion edit. No turn, finding, source file, product or generator changes, and no suite,
mega or generator run is owed for these review records. Before this entry was committed on
2026-09-30, `git diff --check` passed, and `./.venv/Scripts/python.exe py/main_test.py
py/tests/test_receipt_update_links.py py/tests/test_prose_conventions.py
py/tests/test_prose_mark_order.py` passed its four tests. The step-2 plan's executor re-measures
every line reference it relies on.

## Ben's decisions and approval of the package, 2026-09-30

Recorded by Claude on 2026-09-30, New York time, in the session that prepared the package above,
committed and pushed at `1dec120315990707cb1ff66d06d55dc0cfab43ce`. Ben answered the package's
seven questions in two dialogs by selecting one option of each. The option labels and descriptions
quoted below are the session's wording; Ben's part is his selection of each.

1. **Question 1, finding 11:** Ben selected "Keep all five", described as "Record an exception for
   all five: the four for refuse-to-replace, the round trip for its offline reuse and
   forced-refresh coverage." Under the rule's "unless Ben asks", Ben asks for all five stub test
   ids of `py/tests/test_wikisource_special_page_download.py`. The step-2 plan records that
   exception with its two reasons, for example beside the `ws_bot` exception that `AGENTS.md`'s
   section on writing tests declares, and presents the wording for approval; no test is removed.
2. **Question 2, item 36.2:** Ben selected "Allow the lag (Recommended)", described as "Amend
   AGENTS.md and py/product_scopes.py so a MAM text refresh does not oblige rerunning mam4sef and
   mam_osis, as AGENTS.md already says of the HBCE comparison; a change to their code still does.
   The products keep lagging." MAM-for-Sefaria and MAM-OSIS are therefore not rerun, and no public
   data changes under this item; the step-2 plan words the amendment.
3. **Question 3, finding 32:** Ben selected "Rule names the default (Recommended)", described as
   "Reword the common-body rule to name the default location, with BOOK_SCANS_ROOT as its
   override; no code or machine change." The common-body change is deployed with
   `--sync-user-config`.
4. **Question 4, finding 33:** Ben selected "Home clone stays ff-only (Recommended)", described as
   "Scope the fetch-and-merge rule to ordinary full-clone work, as doc/clone-forests.md already
   does, and give worktree integration (common body and Codex lifecycle) a fetch before the
   fast-forward and a refused-push branch back to the worktree."
5. **Question 5, finding 8.2:** Ben selected "In the hebrew-prose skill (Recommended)", described
   as "Add it to the shared skill, widening its description to cover manuscript locators; the
   step-2 plan proposes the wording and the conforming edits." The conforming edits it proposes
   cover the prose that question 5 listed as not following the terminology, each for approval.
6. **Question 6, item 36.1 with finding 10.1:** Ben selected "Restore an explicit grant
   (Recommended)", described as "Add to the five wrappers a sentence saying the statement covers
   the data in that directory (a licence file in each distributed product; wording in the step-2
   plan); DATA-LICENSES.md then describes them as they stand." The five product `LICENSE.md` files
   thereby join the step-2 plan's reader-facing approval surface.
7. **Question 7, the package:** to "Do you approve the proposed fixes, deferrals, and no-action
   dispositions?", Ben selected "I approve", described as "Approve the complete package committed
   at 1dec1203, with your answers to the six questions. It approves no unspecified editorial
   wording; the step-2 plan presents concrete wording."

The approval applies to the complete package committed at
`1dec120315990707cb1ff66d06d55dc0cfab43ce`, meaning its disposition list, the table of
recommendations, the table of finding 36's items, the already-resolved subitems, the deferrals and
the no-action dispositions, as the six answers above settle its questions. It supplies no approval
of unspecified editorial wording and no semantic choice beyond those answers. Every fix remains for
later remediation. The list also raised with Ben the risk that a default `py/main_repo_maintenance.py`
run deletes finding 30's untracked source in `C:/Users/BenDe/GitRepos/MAM-basics/.novc/`; he gave
no instruction about it, and this task took no action on it.

**Close-out step 1 is complete; steps 2 to 4 remain.** Step 2 is a fresh-task remediation plan
with concrete editorial wording, presented in `doc/periodic-review.md`'s risk order.
`doc/dual-agent-review.md`'s record of this round, which its close-out paragraph requires "after
Ben's decisions", is left to a later close-out step, the step-2 plan or its executor; this task
does not write it. This entry changes only this file; before it was committed, `git diff --check`
passed, and the same four lint tests passed. This update remains `State: open` while its base
survives.
