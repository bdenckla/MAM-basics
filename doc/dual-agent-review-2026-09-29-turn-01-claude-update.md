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

## Detailed remediation plan prepared; approval pending, 2026-09-30

Prepared by Claude on 2026-09-30, New York time, as close-out step 2 of the round, in two sessions.
The first session worked from a handoff prompt that the step-1 session prepared that day and Ben
pasted in; that prompt records Ben's selection of "I approve" for the package and is otherwise that
session's reconstruction. When Ben told the first session "You're about to get compacted. Wrap up
and perhaps provide a new prompt for a new session.", it wrote a second handoff prompt and
checkout-local notes, and Ben pasted the prompt into the second session, which corrected,
re-verified and committed the plan. Neither
session attributed a reconstruction's facts to Ben; each checked them. This entry records the plan
and three answers Ben gave while it was drafted. It executes no remediation.

**Checkout and merge.** The full clone `C:/Users/BenDe/GitRepos2/MAM-basics`, on its carrier
`dar-2026-09-29`. The clone's reflog shows it switched to `main` and fast-forwarded to
`origin/main` at 15:05:00 New York time, a minute after the step-1 session's last commit, and
moved back to the carrier by a checkout at 15:07:34, where the first session found it. At the start
of each session a fetch found `HEAD` and `origin/dar-2026-09-29` both at
`bcbbb1dc8199317b6bf9c9a6bfb430019b1f5374`, the tree clean (for the second session, apart from the
untracked draft), and `origin/main`, `303bf2399c1e1fc1300a75f4fb1ed335d62984d0`, already merged by
`c344c5df`; so the merge that D11 requires before editing made no commit, and nothing was pushed
before this entry. Each session was the only writer in the checkout. The primary forest's clone,
`C:/Users/BenDe/GitRepos/MAM-basics`, was clean on `main` at `90d1169e` when the first session
looked at 15:22 and when the second looked at 17:58 New York time, and finding 30's untracked
source there still existed at both checks, 95,251 bytes, last written 2026-09-28 19:18:06 New York
time. Neither session opened it.

**The plan** is [`PLAN-remediate-review-findings-2026-09-29.md`](PLAN-remediate-review-findings-2026-09-29.md),
State "live; detailed plan drafted 2026-09-30; awaiting approval of concrete wording and execution."
It presents the changes in `doc/periodic-review.md`'s risk order: the reader-facing documents, with
current and proposed wording, including the five product licence files and question 5's
conforming edits; then the one public-data change, finding 1.1's consumer notice in all 24
MAM-parsed plus files, with its generated effects; then the lower-risk changes, first by type. It
keeps the thirteen reproducible code and test defects apart from the editorial proposals, gives
concrete wording for every editorial item, presents finding 8.1's rewritten passages for Ben's
approval or reversal, and lists thirteen sites found while planning, each for his approval or
striking. Finding 30's list of approved public additions is drafted from its untracked source and
shown to Ben before anything drawn from that source is committed or pushed.

**Ben's answers while the plan was drafted.** Three gaps in the package went to Ben in one dialog on
2026-09-30. The questions, option labels and descriptions quoted here were the first session's
wording; Ben's part is his selection of each.

1. To "Question 5 listed seven sites that write a manuscript page as "folio 57a". A census of the tree
   found more. Which sites should the plan's conforming edits cover?", Ben selected "Maintained prose
   (Recommended)", described as "Q5's list plus the other maintained Markdown, docstrings, skill text
   and tool output: evr-ii-b-55/README.md:182 and :493, the meteg snips README's :416, seven passages
   of the Lamentations snips README, the rest of the verse-links skill and generator, and two
   Holman/UXLC helper docstrings or messages. The new skill section names the unswept rest." The
   other options were "Also generated pages, data" and "Only question 5's list". The question's
   "seven sites" should have said eight: question 5's list names finding 2.4's two locators,
   `evr-ii-b-55/README.md:194` and `:485`, `references/sources-and-corpora.md:46`,
   `dot-claude/skills/verse-links/SKILL.md:70` and `:95`, and `py/main_verse_links.py:209–212`.
2. To "The sub-agents found further sites with the same defect as approved items but not named in the
   package. … Should the plan include them?", Ben selected "Include, flagged (Recommended)", described
   as "A separate "Sites found while planning" section gives current and proposed wording for each.
   You approve or strike them along with the rest of the plan." The other option was "Leave them".
3. To "When the executor corrects a stale claim in place in an open update file (findings 1.3, 4,
   35), should that file also get a dated entry naming each passage it corrected? Item 36.3's general
   policy question stays deferred either way.", Ben selected "Dated entry per file (Recommended)",
   described as "Each corrected update gains one dated entry naming, in their own words, the passages
   corrected, so a reader can see what changed and when." The other option was "In place only".

**Delegation and checks.** By its own account the first session had read-only sub-agents re-measure
every cited site before drafting, and five read-only verifiers check the draft in bounded groups; it
verified three verifiers' corrections against the tree, while the defects verifier's report
arrived as it wrapped up and the verifier of the receipts' updates and docstrings reported after
it. The second session re-checked each of the verified corrections against the tree before applying
it, and four fresh read-only sub-agents checked what remained: A the defects section and the
defects verifier's items; B the receipts' updates, the new HBCE update and finding 30; C the Python
comments and docstrings and `AGENTS.md`'s test exception; and D a census of "folio" and "leaf"
across the tree. The second session re-read the source of every claim it adopted. Those checks
corrected counts, line numbers and wording, and found three things the package did not name: the
last case of `py/tests/test_wikisource_special_page_download.py` would pass even if the manifest
check were broken (flagged site 11), a sentence on the generated Holman corrections page has been
false since 2026-08-12 (flagged site 12), and the census found eighteen more maintained passages
that call a page a folio or a leaf. The plan adds those to question 5's conforming edits, as it does
the sites that the first session's later checks found, each marked as found after Ben's answer. No
MAM-private content was read. Every assistant record of both sessions' transcripts
gives Claude's `max` effort level; the app's session record for the second session gave `high` when
read at 17:17 New York time, and "The app's effort record and the clone's checkouts, 2026-09-30",
below, records what followed.

**Verification of this entry.** This entry and the plan are one commit, and nothing else changes.
No source file, product or generator changes, and no suite, mega or generator run is owed for these
documentation commits. Before the commit, `git diff --check` passed, and
`./.venv/Scripts/python.exe py/main_test.py py/tests/test_receipt_update_links.py
py/tests/test_prose_conventions.py py/tests/test_prose_mark_order.py` passed.

**What remains.** Ben's approval of the plan's reader-facing wording, its public-data change and its
lower-risk changes; his choices on finding 8.1, on each group of flagged sites, on the MAM-with-doc
licence alternative, on the corrected H6 value and on the HBCE "split" and "join" wording; and his
approval of execution. Then close-out steps 3 and 4, execution and final integration, in a fresh
task. This update remains `State: open` while its base survives.

## Ben's approval of the remediation plan, 2026-09-30

Recorded by Claude on 2026-09-30, New York time, in the second step-2 session, which committed the
plan at `50ef50ee50804ddf802e058a78d557d34d5be65a`. The session presented the plan in
`doc/periodic-review.md`'s risk order: each reader-facing change with its current and proposed
words, a few long passages in summary with the plan holding their full text; then the public-data
change; then the lower-risk changes by type. Ben then answered twelve questions in four dialogs.
The questions, option labels and descriptions quoted or summarized here were the session's
wording; Ben's part is his selection of each.

1. **Reader-facing wording.** To "Do you approve the reader-facing wording shown above (the
   rendered-HTML and reader-facing Markdown items, including the licence files and question 5's
   page locators)?", Ben selected "Approve (Recommended)" rather than "Not yet".
2. **The MAM-with-doc licence file.** Ben selected "Edition sentence (Recommended)", described as
   ""This statement applies equally to the MAM-with-doc edition, which MAM-basics publishes from
   gh-pages/MAM-with-doc/." The file then leaves the blob the other three share.", rather than
   "Directory sentence".
3. **The HBCE wording, flagged site 9.** Ben selected "Join wording (Recommended)" rather than
   "Keep "split"".
4. **The Holman page's introduction, flagged site 12.** Ben selected "Fix it (Recommended)" rather
   than "Leave it".
5. **The public-data change.** To "Do you approve the one public-data change: in all 24
   MAM-parsed/plus/*.json files, rules 5 and 6 of header.consumer_notice.critical_rules exchange
   places (narpas rule first), every Scripture payload and book39s value unchanged?", Ben selected
   "Approve (Recommended)".
6. **The lower-risk changes.** To the question covering the `doc/` Markdown and update entries,
   the Python comments and docstrings, the agent instructions and skills, and the thirteen code and
   test defect fixes, Ben selected "Approve (Recommended)".
7. **Finding 8.1.** Ben selected "Approve as they stand (Recommended)" rather than "Reverse".
8. **Hazard H6.** Ben selected "Name the home clone (Recommended)" rather than "Drop the worktree
   advice".
9. **The flagged sites.** To "Which groups of flagged sites (same defect as an approved item, not
   named in the package) do you approve? Unselected groups are struck.", Ben selected all three
   groups: "Records and runbooks", "Skills" and "Python text and policy JSON".
10. **Flagged site 11, the test fix.** Ben selected "Fix it (Recommended)" rather than "Leave it".
11. **The accepted `NOT_IN_MEGA` reason of `py/main_uxlc_estimate_atom_loc.py`.** Ben selected
    "Change to "page" (Recommended)" rather than "Keep as accepted".
12. **Execution.** To "With those answers, do you approve executing the plan (close-out steps 3
    and 4: phases 0–5 in a fresh task, including finding 30's draft shown to you before anything
    from it is committed, final integration into main and the --sync-user-config deployment)?",
    Ben selected "Approve execution (Recommended)".

**What this records.** The plan's line 3 now reads "State: live; approved for execution 2026-09-30;
remediation not started.", and item 5 of its "Decisions this plan follows" lists these choices.
Ben's approval covers the plan committed at `50ef50ee`, as this commit amends it to record them and
to give the new line numbers below. It selects no deferred semantic or policy choice beyond the
plan's own.

**The branch.** After the plan's commit, `origin/main` moved twice, first with the dual-agent review
relay (`9988db8e`) and then with D13, the automated review protocol (`0f745369`). Each move was
merged into the review branch without conflict, as `23f9666742f8f9f3adb2a62145bcc6833f14156d` and
`02a20154392386a296df41011ca2d95b102e3c2f`, and pushed. Each merged tree is `origin/main`'s tree
plus the round's eleven turn files, this update and the plan, so neither merge owed the suite or
the mega. The merges moved passages the plan cites in five files without changing their words; the
plan now lists the new line numbers, and its contract has the executor re-measure every cited file
changed since its planning tree. D13 changes nothing in this close-out: it governs automated rounds,
and manual close-out and integration keep D11's rules.

**Verification of this entry.** This entry and the plan's approval edits are one commit. No source
file, product or generator changes, and no suite, mega or generator run is owed. Before the commit,
`git diff --check` passed, and the same four lint tests passed.

**Close-out step 2 is complete; steps 3 and 4 remain**, in a fresh task that executes the plan and
owns final integration. This update remains `State: open` while its base survives.

## Approved remediation implemented; final gates pending, 2026-10-01

Recorded by Claude on 2026-10-01, New York time, in the session that executes the remediation plan
as close-out steps 3 and 4. It worked from a handoff prompt that the second step-2 session prepared
and Ben pasted in; that prompt quotes Ben's selection of "Approve execution (Recommended)", which
the entry above records, and is otherwise that session's reconstruction, which this session checked
against the plan and the tree. **Implemented: every active row of the plan's "Finite execution
ledger", apart from finding 2's dated entry in the 2026-09-26 close-out record, which the plan's
"Records" assigns to the closing records.** The full suite passed at `94535122`, and it runs again
after the final merge because `9588700f`, later, changed a test. Final integration, meaning the
merge of the current `origin/main`, the mega and the push of `main`, and the `--sync-user-config`
deployment remain pending.

**Checkouts and baseline.** The development checkout is the full clone
`C:/Users/BenDe/GitRepos2/MAM-basics`, on its carrier `dar-2026-09-29`. Editing began there at
`a849e068f1db485ef0dea9062596ff12cfef9896`, the commit of "Ben's approval of the remediation plan,
2026-09-30", with the tree clean. A fetch found `origin/dar-2026-09-29` at the same commit, and
`1dec1203`, `bcbbb1dc`, `a849e068` and `origin/main`, then `0f745369`, were all ancestors of `HEAD`,
so the merge that D11 requires made no commit. Phase 1, finding 30, ran in the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, which holds the finding's untracked source: phase 1a read it
and drafted the list in this session's scratch directory, and after Ben's answer phase 1b created
that clone's carrier from `origin/dar-2026-09-29` at `94535122`, committed and pushed `b8700f12`
there, and switched that clone back to `main`. The development checkout then fast-forwarded to
`b8700f12`. From its first edit, at 22:29 New York time on 2026-09-30, to this entry, this session
was the only writer in either checkout; its sub-agents only read.

**Ben's decisions in this session.** Each question and its options were this session's wording;
Ben's part is his selection of each, made at 06:54 New York time on 2026-10-01.

1. **Finding 30.** To the question whether he approved the phase-1a draft (36 rows and two
   entries, the privacy check passed, every addition present at `HEAD` and added by `0e254fdc`,
   with rows A01 and A02 generalizing their destinations' wording to keep account observations
   out of a public row), Ben selected "Approve as drafted (Recommended)" rather than "Approve;
   quote A01/A02 exactly" or "Not yet". Phase 1b wrote the draft as approved.
2. **The step-2 session's request.** The second step-2 session asked this session, at Ben's
   suggestion, to record an in-place correction of its sentence on the app's effort record and a
   new entry on that record and the clone's checkouts. Ben selected "Record it, verified",
   described as "Before writing, I check each fact against the reflog, the app's session records,
   the settings file and the transcripts; I drop any fact I cannot verify and say what I verified.
   It goes in with the closing records.", rather than "Leave it out".

**Commits.** Twenty-six commits before this entry, each pushed to `origin/dar-2026-09-29` with
`git push origin HEAD:dar-2026-09-29` as soon as it was made, never forced:

1. Phase 2, records, instructions and procedures: `d67bee39` (the plan's State, E1, findings 34.1
   and 35, and the round record), `76fc0086` (`AGENTS.md`), `7cf1ed21` (the common body and the
   lifecycle reference of Codex's `codex-worktree-tasks` skill), `1c0cf3f8` (the shared skills and
   the configuration READMEs), `8fd5b6e6` (runbooks and procedure documents) and `37169648`
   (seven open update files and the HBCE receipt's new update); and `3451942e`, made during phase
   4, which corrects two of `37169648`'s entries.
2. Phase 3, the reader-facing documents and the licence files: `4a5f9800` and `aef596c7`.
3. Phase 4, code, tests, docstrings and their generated outputs: `8742d96a`, `572e2f08`,
   `71f5cd50`, `951f9b35`, `b158db02`, `41d73299`, `f62428c4`, `3a1b9a7c`, `23e0f587`, `392dced7`,
   `4f271a50` and `37002a28`.
4. Phase 5: `94535122`, the change-log regeneration that the first full suite showed was owed;
   and `71214987`, `9588700f` and `174357eb`, which fix what the read-only verifiers below found.
5. Phase 1b: `b8700f12`, made in `C:/Users/BenDe/GitRepos/MAM-basics`.

### Dispositions of findings 1 to 36, C1, E1 and the round record

| Finding | Execution disposition |
|---|---|
| 1 | Implemented. 1.1: `f62428c4` lists the narpas rule before the whitespace-template rule and regenerates the 24 `MAM-parsed/plus` files and `mpplus.html`, and `94535122` regenerates the change log's `unpinned-latest` for the new plus tree id. 1.2: `8742d96a`. 1.3: `37169648`, corrected by `3451942e`. |
| 2 | Implemented, apart from the dated entry in the 2026-09-26 close-out record, which goes in the closing records. 2.1: `4a5f9800` (`in/mam-ws-intro/README.md`) and `37002a28` (two docstrings). 2.2: `8fd5b6e6` (the September 9 plan) and `37002a28` (`py/ac_paths.py`). 2.3: `572e2f08`. 2.4: `4a5f9800`. 2.5: `7cf1ed21` and `8fd5b6e6`. |
| 3 | Implemented in `4a5f9800`: 3.1's heading and 3.2's sentence in `evr-ii-b-55/README.md`. |
| 4 | Implemented: 4.1's second site, 4.2, 4.3 and 4.7 to 4.9 in `37169648`; 4.4 in `8fd5b6e6`; 4.5 in `1c0cf3f8`. Already resolved before this task: 4.1's first site and 4.6, by `e4934b6e`. |
| 5 | Implemented: 5.1, 5.4 and 5.5 in `37002a28`; 5.2 in `8fd5b6e6`; 5.3 and 5.6 in `572e2f08`. |
| 6 | Implemented: 6.1 in `71f5cd50`, 6.2 in `951f9b35` and 6.3 in `b158db02`. |
| 7 | Implemented in `b158db02`, with gate 4's wording and hazard H2 (flagged site 7). |
| 8 | Implemented. 8.1: approved as it stands, so its passages stay. 8.2, by question 5: the `hebrew-prose` description and its new section in `1c0cf3f8`, and the conforming edits in `1c0cf3f8`, `8fd5b6e6`, `4a5f9800`, `392dced7`, `4f271a50` and `37002a28`. |
| 9 | Implemented in `37169648`: 9.1's State form in `evr-ii-b-55/evr-ii-b-55-images-provenance-update.md` and `doc/post-stress-meteg-image-provenance-update.md`, and 9.2's record in the first. |
| 10 | Implemented in `aef596c7`: 10.1 with item 36.1, in `DATA-LICENSES.md` and the five product licence files, and 10.2 in `DATA-LICENSES.md`. |
| 11 | Implemented: the exception for all five stub test ids in `AGENTS.md` (`76fc0086`) and in the test module's docstring (`23e0f587`). No test was removed. |
| 12 | Implemented in `76fc0086` (`AGENTS.md`) and `23e0f587` (the docstrings of `py/ws/ws_special_page_download.py`). |
| 13 | Implemented in `4a5f9800` (`in/mam-ws-intro/README.md`) and `37002a28` (`py/subcommands/download_wikisource_intro.py`). |
| 14 | Implemented in `8742d96a`: 14.1, 14.2, 14.3's two false references and three rewordings, and 14.4. |
| 15 | Implemented in `41d73299`. |
| 16 | Implemented in `41d73299`, with its `NOT_IN_MEGA` reason; `9588700f` corrects one sentence of `parse_ws.almost_main`'s docstring. |
| 17 | Implemented in `41d73299`. |
| 18 | Implemented in `4a5f9800`: 18.1 and 18.2. |
| 19 | Implemented in `8fd5b6e6`. |
| 20 | Implemented with flagged site 9's "join" wording: `hbce-psalms/README.md` in `4a5f9800` and `DATA-LICENSES.md` in `aef596c7`. |
| 21 | Implemented in `37169648`: the new `doc/hbce-psalms-vs-mam-2026-09-26-update.md` and the base's line-4 pointer. Deferred, as the plan records: the heading fix in `py/hbce_psalms/compare.py`. `hbce-psalms/out/` is unchanged. |
| 22 | Deferred: no MAM-basics change; the next dependent refresh checks that the variant reaches phonetic-hbo's page and the survey. |
| 23 | Implemented: the `mam-wikisource-refresh` skill in `1c0cf3f8` and `py/ws/pywikibot-setup.md` in `8fd5b6e6`, with flagged site 2 in `37002a28`. Unresolved when this entry was written, and decided by Ben on 2026-10-01, as "Ben's decision on the commit for a bot run's special-page changes, 2026-10-01" records: the question the plan leaves open under "The `mam-wikisource-refresh` skill (finding 23)", which commit takes a special page that the post-bot download changes. |
| 24 | Implemented: 24.1 and 24.2 in `MAM-parsed/historical/README.md` (`4a5f9800`, rewrapped by `71214987`) and the module docstring of `py/subcommands/diff_mpplus.py` (`37002a28`). |
| 25 | Implemented in `3a1b9a7c`, with the new lint `py/tests/test_forest_subprocess_bounds.py`, which `9588700f` extends to calls through imported modules. |
| 26 | Implemented in `3a1b9a7c`, with its texts; `174357eb` restores the approved wording of flagged site 5.5's entry. The write form was not run. |
| 27 | Implemented in `4a5f9800`. |
| 28 | Implemented: 28.3 in `1c0cf3f8`; 28.4, turn 07's ten runbook lines, in `8fd5b6e6`, and its three action-table rows in `3a1b9a7c`; 28.5 in `8fd5b6e6`; 28.6 in `4a5f9800`. Already resolved before this task: 28.1 and 28.2, by `4d3ebf66`. |
| 29 | Implemented: the configuration READMEs in `1c0cf3f8` and the September 9 plan in `8fd5b6e6`. |
| 30 | Implemented in `b8700f12`, with the wording Ben approved on 2026-10-01. |
| 31 | Implemented in `37002a28`. |
| 32 | Implemented in `7cf1ed21`, with flagged site 5's other statements of the rule. |
| 33 | Implemented in `7cf1ed21`: the common body and Codex's lifecycle reference. |
| 34 | Implemented: 34.1 in `d67bee39`, `76fc0086`, `7cf1ed21` and `1c0cf3f8`; 34.2 and 34.3 in `1c0cf3f8`. |
| 35 | Implemented in `d67bee39`. |
| 36 | By item, below. |
| C1 | Implemented in `23e0f587`. |
| E1 | Implemented in `d67bee39`. |
| Round record | Implemented in `d67bee39`: "The September 29 round" in `doc/dual-agent-review.md`. |

### Dispositions of the sites found while planning

Ben approved all thirteen; none was struck, so none is superseded.

| Site | Execution disposition |
|---|---|
| 1 | Implemented in `37169648`, whose new entry `3451942e` corrected. |
| 2 | Implemented in `37002a28`. |
| 3 | Implemented: 3.1 and 3.2 in `8fd5b6e6`, 3.3 in `4f271a50`, 3.4 in `1c0cf3f8` and 3.5 in `37002a28`. |
| 4 | Implemented in `8fd5b6e6`. |
| 5 | Implemented: 5.1 in `8fd5b6e6`; 5.2, 5.3 and 5.4 in `37002a28`; 5.5 in `3a1b9a7c`, with its approved wording restored by `174357eb`. |
| 6 | Implemented: 6.1 in `8fd5b6e6` and 6.2 in `8742d96a`. |
| 7 | Implemented in `b158db02`. |
| 8 | Implemented in `1c0cf3f8`. |
| 9 | Implemented in `4a5f9800` and `aef596c7`, as finding 20's wording. |
| 10 | Implemented in `37002a28`. |
| 11 | Implemented in `23e0f587`. |
| 12 | Implemented in `392dced7`. |
| 13 | Implemented in `b8700f12`. |

The plan's "Noticed and left out" items stay as the plan leaves them.

### The items of finding 36, and the other deferrals

| Item | Execution disposition |
|---|---|
| 36.1 | Implemented with finding 10.1, in `aef596c7`. |
| 36.2 | Implemented: `AGENTS.md` in `76fc0086` and `py/product_scopes.py` in `37002a28`. MAM-for-Sefaria and MAM-OSIS were not rerun. |
| 36.3 | Deferred, as the plan records. |
| 36.4 | Deferred: only Ben can supply the words of his 2026-09-28 decisions. |
| 36.5 | Deferred. |
| 36.6 | Deferred: no test exercises either forest module's behaviour. |
| 36.7 | Deferred. |
| 36.8 | Deferred to Ben, with no action in remediation: the Sheet link on the English Decalogue page is an outward-facing Wikisource edit, his to make. |
| 36.9 | Superseded: `e4934b6e` retired the executed Google Sheet plan, so no action is owed. |
| 36.10 | Implemented: the `NOT_IN_MEGA` reason, in `37002a28`. Deferred: running `lint-receipt` in the suite. |
| 36.11 | Deferred. |
| 36.12 | Implemented in `4a5f9800`; `cam1753/cam1753-page-index.json:3` is unchanged, as the plan records. |
| 11's older tests | Implemented as no action: the fourteen pre-window example-based methods of `py/tests/test_main_download_fr_wikisource.py` stay. |

### Verification and generated-diff evidence before final integration

**Checks for every commit.** `git diff --check` passes on every one of the 26 commits, each of
which has a single parent, rechecked commit by commit on 2026-10-01. Every Markdown, update and
instruction commit passed `./.venv/Scripts/python.exe py/main_test.py
py/tests/test_receipt_update_links.py py/tests/test_prose_conventions.py
py/tests/test_prose_mark_order.py`, run from the root of the checkout it was made in. Black at its
defaults found every changed Python file formatted. Each edit to a file holding pointed Hebrew was
applied byte for byte by a scratch script, so no other Hebrew in those files changed. Each commit
message records its own targeted checks; the results of those that "Targeted verification" names
were:

1. **Finding 1.1:** in each of the 24 plus files, only the two exchanged lines changed, and they
   equal `52f1f6bf`'s; the first "narpas", case-insensitively, is the gloss; `mpplus.html`
   exchanged the same two rules in the notice's list and in the Job and Samuel example headers and
   changed nowhere else; `py/tests/test_public_data_consumer_notices.py` passed.
2. **Findings 1.2 and 14.2:** both `--find-stack-path` lookups of `E/נוסח` print Genesis 1:1 and
   1:3 and write nothing; `ruff check --no-cache py` reports only the E731 named below.
3. **Finding 5.6:** `py/main_authored.py gen-site --trust-surveys` rewrote every deploy-root page
   byte for byte, including `gh-pages/post-stress-meteg-post-silluq-1k14v14.html`.
4. **Finding 6.1:** three scratch mutations, `-ff` on a worktree removal, `git branch -df` and a
   `"-fd"` constant, each fail the lint; the old lint caught none of them.
5. **Finding 6.2:** over the reports at `f4d81285`, the new lint finds the old lint's nine problem
   marks at four sites and exactly one more, U+05A5 at line 70 of `2026-03-06.html`.
6. **Findings 6.3 and 7:** `py/main_test.py py/repo_util/worktree_retirement_simulation_test.py`
   passed twice, 34 tests each, in about 300 seconds each.
7. **Findings 15 and 17:** six in-memory scratch faults on Genesis now raise, where the old checks
   let all six pass.
8. **Finding 16:** one run of `py/main_parse.py ws --write-parser-stage-grammar-lock`, 17
   seconds, changed line 2 of the lock alone and no product.
9. **Finding 21:** `py/main_hbce_psalms.py lint-receipt` reported "0 problems".
10. **Finding 25:** the lint counts 30 launches, 18 of them the modules' own wrappers. A scratch
    harness that writes mutated sources outside the checkout found that each of eleven mutations
    fails the lint as `9588700f` leaves it; the lint as `3a1b9a7c` committed it missed four of
    them, all calls through an imported module or package.
11. **Flagged site 11:** with a scratch `_load_manifest` that accepts "not json", the fixed test
    fails where the old one passed.
12. **Flagged site 12:** `py/main_render_uxlc_corrections.py` changed only the one sentence of the
    page's introduction; `holman/docs-not-served/uxlc_corrections.json` and `holman/data/` are
    unchanged.
13. **Question 5:** `py/main_verse_links.py 1Samuel 17:5 --atom 14` prints "Sefaria's image of
    Leningrad Codex page F159A"; the two searches that "Targeted verification" names found only
    the categories it lists.
14. **Finding 30:** the 36 rows' destinations were re-confirmed with `git grep` at `94535122`, 71
    searches with none missing, and the privacy check passed on the draft and again before the
    commit.

**Read-only verification of the whole plan.** Four read-only sub-agents each checked one part of
the plan against `b8700f12`, reading each file with `git show` and each change with `git diff
a849e068 b8700f12`: the reader-facing documents and public data; the code and test defects and the
Python comments and docstrings; the agent instructions, skills and procedure documents; and the
receipts' updates and the sites found while planning. Each found every item of its part present,
apart from finding 2's entry, which is pending by design, and found no change that no item accounts
for. This session re-checked against the tree each fault they reported before acting on it; the
corrections below list those faults.

**The full suite.** Its first run, at `37002a28`, the last executable change at the time, ended at
23:38 New York time on 2026-09-30 with 1 failed, 1,015 passed and 5 skipped, in 168.03 seconds.
The failure,
`py/tests/test_diff_mpplus_unpinned_latest.py::test_registered_outputs_match_real_regeneration`,
showed that the committed `unpinned-latest.html` and `unpinned-latest.json` no longer matched a
regeneration: finding 1.1's change to the plus files' headers moved the `MAM-parsed/plus` tree id
that labels the unpinned release from `0758f964` to `c3619446`. `py/main_diff.py mpplus --all`
changed only those two files, on three lines, committed as `94535122`. The second run, at
`94535122`, ended at 06:59:47 New York time on 2026-10-01 with 1,016 passed and 5 skipped, in
180.20 seconds; its summary line reports no subtest count. `9588700f` later changed a test, so the
suite runs again on the integrated tree.

**Generated diffs, each explained.** These are the only generated outputs that changed:

1. The 24 `MAM-parsed/plus/*.json` files: rules 5 and 6 of `header.consumer_notice.critical_rules`
   exchange places (finding 1.1); every Scripture payload and `book39s` value is unchanged.
2. `gh-pages/MAM-parsed/plus/html/mpplus.html`: the same exchange, in the notice's list and the two
   example headers.
3. `py/verify_mp/expanded_stack_grammar_parser_stage.lock.json`: line 2, the provenance, now names
   the writer (finding 16).
4. `gh-pages/holman/uxlc_corrections.html`: the one sentence of flagged site 12.
5. `gh-pages/MAM-with-doc/change-log/unpinned-latest.html` and `unpinned-latest.json`: the plus
   tree id, on three lines. The four Scripture changes they report, every named release and
   `index.html` are unchanged.

The mega at final integration checks every other output that "Outputs expected to stay unchanged"
names.

**Corrections to the plan and to this branch's records.**

1. The plan's "Outputs expected to stay unchanged" names "every change-log file under
   `gh-pages/MAM-with-doc/change-log/`" as unchanged. Finding 1.1 necessarily changes
   `unpinned-latest.html` and `unpinned-latest.json`, whose label is the plus tree id; the plan
   missed that consequence, and `94535122` regenerated them as explained above.
2. The plan's "Summary by type", item 2, counts "three test modules, four with flagged site 6.2"
   among the docstring changes; there are four, five with flagged site 6.2.
3. The subject of `37169648` says "Correct eight open update files"; that commit corrects seven.
   The plan's eighth, the 2026-09-26 close-out record, is corrected in the closing records. The
   pushed message stays as it is, and `3451942e`'s message says so.
4. Fixed in `174357eb`: the entry "2026-09-30: corrections made in the 2026-09-29 review's
   remediation", which `3a1b9a7c` added to `doc/PLAN-checkout-kinds-and-portable-knowledge-update.md`
   for flagged site 5.5, departed from the approved text twice. Its item 1 cited "(`:171–172`)",
   which now reads "(`:170–172`)", as approved; and it ended with "The plan's rules are introduced
   at `:161` as "Three rules apply to every kind:".", a note the plan addresses to the executor
   outside the quoted entry, now removed.
5. Fixed in `71214987`: `4a5f9800` left one 142-character line in `MAM-parsed/historical/README.md`,
   a file that wraps at about 79 characters; the paragraph is rewrapped, with no word changed.
6. Fixed in `9588700f`: the lint that `3a1b9a7c` added for finding 25 recognized a launcher only by
   a name that `from ... import` binds, so a call through an imported module object or a dotted
   path escaped it; and `parse_ws.almost_main`'s docstring said the lock is rewritten "first",
   though the per-book outputs are written before it.
7. Left as Ben approved it: finding 30's entry in
   `doc/memory-retirement-and-instruction-consolidation-2026-09-28-update.md` names its line-3
   correction by former and new words but not by its number, flagged site 13, which the plan's
   general rule for dated entries asks for; `b8700f12`'s message names the site.
8. Left unfixed, because a fix would change wording Ben approved: in the maintenance runbook,
   preconditions 2 and 3 now run cwd-relative commands, `git worktree list`,
   `git branch --list "claude/*"` and a loop over `Get-ChildItem -Directory ..`, and only
   precondition 4 and section 1 then say to run from the root of a full MAM-basics clone. Before
   the remediation the commands named the primary forest's clone.
9. Left unfixed because the approved plan does not cover it: `ruff check --no-cache py` reports
   E731, a lambda assigned to a name, at `py/tests/test_dual_agent_review_dispatch.py:42`, which
   `1a50d4b6` added after the plan was written.

**Noticed outside the plan, for Ben.** Finding 28's kind, a live text pinned to the primary
forest's clone, remains at sites the plan names nowhere: the interpreter path
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` in `py/main_diff.py:13`,
`py/main_github_issue_edit.py:6`, `py/main_pipeline_graph.py:31`,
`py/main_uxlc_estimate_atom_loc.py:65` and `py/tests/test_graphviz_version_pin.py:39`, and several
passages of `doc/scan-pages.md`. No action was taken.

**What remains.** Final integration as the plan's "Final integration" describes: merging the
current `origin/main`, which has moved to `1158938e`; the mega; the full suite on the integrated
tree; the fast-forward and push of `main`; and the `--sync-user-config` deployment and its check.
Then the closing records: the entry "Final integration and configuration deployment completed",
the plan's State, finding 2's entry in the 2026-09-26 close-out record with its two in-place
corrections, and the step-2 session's correction and entry, verified. This update remains
`State: open` while its base survives.

## The app's effort record and the clone's checkouts, 2026-09-30

Recorded by Claude on 2026-10-01, New York time, in the session executing close-out steps 3 and 4,
at the request of the second step-2 session, which drafted this entry on 2026-09-30 after the
approval entry above was committed at `a849e068`; Ben had suggested to that session that it ask
this session to do the writes. Ben then selected "Record it, verified", as "Approved remediation
implemented; final gates pending, 2026-10-01" records. Every fact below was checked before it was
written, as the last paragraph describes, which also names the draft's three corrections. All times
are New York time.

**Effort.** Every assistant record of the second step-2 session's transcript gives `max`: 768
before its context was compacted at 22:24:11, and 28 after, through 22:33:07, its last record
when this entry was written.
The first step-2 session's 377 assistant records also all give `max`. The app's session record for
the second session gave `high` when that session read it at 17:17, ten minutes after its creation
at 17:07:26. At 22:17 Ben wrote to it: "UI says "high" just now. I set it to Max. Seems like
something is slipping it downward.", and at 22:19: "By "I set it to Max" I meant "I set it back to
Max" just now." The record gave `max` when the session read it at 22:18, and again at 22:27, after
the compaction. Ben's user-level settings file, `~/.claude/settings.json`, last written at 11:43
on 2026-09-30, sets `CLAUDE_CODE_EFFORT_LEVEL` to `max` in its `env` block, which is consistent
with the responses running at `max` while the record gave `high`. At 22:20 Ben asked: "Perhaps it
dropped back to high because the session is about to be compacted?" The record already gave `high`
at 17:17, while the context was small, and it gave `max` after the compaction, so an approaching
compaction does not explain it. What set the record to `high` is not established.

**Checkouts.** The first and second step-2 sessions and the steps 3–4 session all ran in the full
clone `C:/Users/BenDe/GitRepos2/MAM-basics`. Its reflog records five checkouts on 2026-09-30. The
first, at 15:05:00 from the carrier to `main`, is recorded under "Detailed remediation plan
prepared; approval pending, 2026-09-30". The other four bear on D11:

1. At 15:07:34, from `main` to the carrier, about a second before the app's recorded creation of
   the first step-2 session at 15:07:35, whose record names `dar-2026-09-29` as its source branch.
2. At 22:14:20, from the carrier to `main`, followed in the same second by a fast-forward of `main`
   to `0f745369`: the second step-2 session's D11 switch, issued at 22:14:19, after it pushed
   `a849e068`.
3. At 22:18:24, from `main` to the carrier, in the same second as the app's recorded creation of
   the steps 3–4 session, whose record names `dar-2026-09-29` as its source branch.
4. At 22:20:08, from the carrier to the carrier: the second step-2 session's own `git switch`,
   issued at 22:20:06, which changed nothing.

No command that any Claude transcript or Codex rollout records from 15:06:30 to 15:08:30 or from
22:17:30 to 22:19:00 switches or checks out a branch. Checkouts 1 and 3 each coincide with the
app's creation of a session whose record names `dar-2026-09-29` as its source branch, which is
consistent with the app checking out a new session's source branch in that session's working
directory; the app itself was not examined. The app's record of the second step-2 session names no
source branch, and the reflog records no checkout when that session was created at 17:07:26. A full
clone that D11 has returned to `main` can therefore be on the carrier again once the app creates a
session from the carrier. The second step-2 session left the clone on the carrier, where the steps
3–4 session was working, instead of switching it back to `main` a second time.

**Two writers, briefly.** From 22:20:33 to 22:22:42 the second step-2 session had uncommitted
edits, which it had also staged, to this update file in that clone: an earlier draft of this entry.
The steps 3–4 session was working in the clone at the time. At 22:22:00 Ben wrote to the second
step-2 session: "BTW the "steps 3-4" session is running concurrently with this one". By 22:22:42
that session had saved its staged edits as a patch outside the repository and restored the file
to `a849e068`, leaving the clone clean, and it wrote nothing in either checkout after that. The
steps 3–4 session's transcript records no read of this file and no `git status` of that clone
during that interval; its first edit came at 22:29.

**Also corrected in place in this file**, in the entry "Detailed remediation plan prepared;
approval pending, 2026-09-30": "the app's session record for the second session gives `high`." now
reads "the app's session record for the second session gave `high` when read at 17:17 New York
time, and "The app's effort record and the clone's checkouts, 2026-09-30", below, records what
followed."

**How this was verified.** The checkouts and their times come from the clone's reflog, read with
`git reflog --date=iso`. The sessions' creation times, source branches and effort values come from
the app's session records, read through its session-management tool on 2026-10-01, and from the
second step-2 session's own reads of them, which its transcript records with their results. The
settings line and the file's last-write time were read from the file on 2026-10-01. Ben's words,
the commands, the edits and the record counts come from the transcripts of the three sessions;
the search for checkout commands covered every Claude transcript written since 2026-09-29 and
every Codex rollout file under `~/.codex`. Three of the draft's details are corrected here. Its
count of "25 after, counted at 22:27" could not be reproduced: 22 records after the compaction
precede 22:28, and 28 precede the transcript's last record, so the count above covers the whole
transcript. Its "four checkouts on 2026-09-30" are five, the first of which the earlier entry
records. Its end of the edit interval, 22:22:41, is given here as 22:22:42, when the restore's
result returned.

## Final integration and configuration deployment completed, 2026-10-01

Recorded by Claude on 2026-10-01, New York time. **Completed: final integration and the
configuration deployment, so close-out steps 3 and 4 are complete.** This entry supersedes the
pending items that "Approved remediation implemented; final gates pending, 2026-10-01" names in its
first paragraph and under "What remains". Every deferral, no-action disposition and unresolved
question there remains as recorded, apart from finding 23's question, which Ben decided later that
day, as "Ben's decision on the commit for a bot run's special-page changes, 2026-10-01" records.

**The final merge.** A fetch found `origin/main` at `c3eb743c`, five commits past the carrier's
last merge base, `0f745369`: the review relay's toast fix and production kickoff (`1bfceff4`), its
registered relay record (`d488f405`), the captured and translated Wikisource dagesh discussion
(`7577b56d`, merged by `1158938e`) and the private follow-up register rule (`c3eb743c`). `e05db0c0`
merged it into the carrier without conflict and was pushed; the one file both sides changed,
`doc/dual-agent-review.md`, merged automatically, and its close-out paragraph reads as both sides
wrote it.

**The mega.** `./.venv/Scripts/python.exe py/main_0_mega.py`, run from the clone's root with no
`REPOS_ROOT` at `e05db0c0`, from 07:27:06 to 07:31:33 New York time, completed all 52 steps in
260.6 seconds with exit status 0 and left the tree clean, with no tracked or untracked change, so
no generated-output commit was owed. Its pinned Graphviz check passed. Every output that "Outputs
expected to stay unchanged" names therefore reproduces the committed one, and the five generated
changes that the implementation entry explains stand as committed.

**The full suite.** `./.venv/Scripts/python.exe py/main_test.py -q`, run at `e05db0c0` after the
mega, from 07:32:00 to 07:35:03 New York time, passed 1,016 tests, with 5 skipped and 60 subtests
passed, in 181.08 seconds, and left the tree clean. It covers `9588700f`'s test change and the
executable changes the merge brought from `origin/main`.

**Integrated and pushed.** A fetch then found `origin/dar-2026-09-29` at `e05db0c0`, exactly the
commit the mega and the suite verified, and `origin/main` still at `c3eb743c`, its ancestor. `main`
in `C:/Users/BenDe/GitRepos2/MAM-basics`, clean at `0f745369`, was fast-forwarded to `e05db0c0`
and pushed normally at 07:35:27, moving `origin/main` from `c3eb743c` to `e05db0c0`. No merge in
`main`, history rewrite or forced push was used. The push carries the changes to the distributed
products; the changed pages under `gh-pages/` reach the published site at its next scheduled or
dispatched publication.

**Deployed and checked.** From that clone on `main`,
`./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config` fetched and validated its
source at `refs/remotes/origin/main@e05db0c0`, deployed 16 changed mappings and reported all 22
mappings clean. The read-only `--sync-user-config --check` that followed, from the same freshly
fetched source, reported all 22 clean and `USER_CONFIG_PROBLEM_COUNT=0`, with exit status 0. Live
instructions, hooks and skills changed only through the deployment command.

**Closing records.** This entry is committed with the plan's State, now "State: executed
2026-10-01.", so the plan is a receipt; finding 2's entry "Execution rows that overstated what
landed or later became false, 2026-10-01" in `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`,
with its two in-place corrections; and the step-2 session's entry above, with its in-place
correction. These records change no source, product or canonical configuration, so the suite, mega
and deployment evidence above stands. The commit is pushed to `origin/dar-2026-09-29`, `main` is
fast-forwarded to it and pushed, and the read-only `--sync-user-config --check` is repeated.

**Preserved for separate cleanup.** Both carriers, `dar-2026-09-29` in
`C:/Users/BenDe/GitRepos2/MAM-basics` and in `C:/Users/BenDe/GitRepos/MAM-basics`, and the remote
branch `origin/dar-2026-09-29` remain; retiring a local carrier needs Ben's approval, and deleting
the remote branch is separate outward-facing cleanup that needs its own authorization. The clone
`C:/Users/BenDe/GitRepos2/MAM-basics` is left on `main`.

This update remains `State: open` while its base survives.

## Ben's approval of D11's sentences on the app's checkouts, 2026-10-01

Recorded by Claude on 2026-10-01, New York time, in the second step-2 session, resumed after the
steps 3–4 session had finished. At 22:33 on 2026-09-30 the second step-2 session proposed three
sentences for D11, `doc/dual-agent-review.md`, "The shared origin branch", and at 07:46 on
2026-10-01 it reported that they were not applied, ending: "If you approve, I'll apply it on main
once the steps 3–4 session, which is still busy, has finished." At 07:55 Ben replied: "no sessions
are currently working. go ahead and make this fix".

D11 now adds 2026-10-01 to its heading's dates and says, after its sentence that a full clone
switches back to `main` when the task ends:

> When the Claude desktop app creates a session whose recorded source branch is the carrier, it
> checks that branch out in the session's working directory, as two checkouts in
> `$HOME/GitRepos2/MAM-basics` on 2026-09-30 indicate. A full clone that a task has returned to
> `main` can therefore be on the carrier again when a later session starts. Each task verifies the
> branch before acting, and only the task that owns the current turn switches the clone back to
> `main`.

An attribution follows, as D11 gives Ben's other decisions, pointing to this entry. The sentences
differ from the proposal in two places. "The desktop app" became "the Claude desktop app", because
D11 governs Codex's turns too and the evidence comes only from Claude's app. "As two checkouts in
`$HOME/GitRepos2/MAM-basics` showed on 2026-09-30" became "as two checkouts in
`$HOME/GitRepos2/MAM-basics` on 2026-09-30 indicate", because "The app's effort record and the
clone's checkouts, 2026-09-30", above, records the evidence and says that the app itself was not
examined.

**Also corrected in place in this file**, in "The app's effort record and the clone's checkouts,
2026-09-30": "and 28 after, through its last record at 22:33:07." now reads "and 28 after, through
22:33:07, its last record when this entry was written.", because the second step-2 session resumed
on 2026-10-01 and added records. Every one of those records also gives `max`.

**Verification of this entry.** This entry, the in-place correction and D11's change are one
commit. `git diff --check` passed, and `py/main_test.py` with
`py/tests/test_receipt_update_links.py`, `py/tests/test_prose_conventions.py` and
`py/tests/test_prose_mark_order.py` passed. No source, product, generator or canonical
configuration changes, so no suite, mega, generator run or deployment is owed.

This update remains `State: open` while its base survives.

## Ben's decision on the commit for a bot run's special-page changes, 2026-10-01

Recorded by Claude on 2026-10-01, New York time, in a session that worked from a handoff prompt
that Claude prepared that day in the session that executed close-out steps 3 and 4, and that Ben
pasted in. The prompt quotes Ben's instruction to that session, a request for a prompt for a
session that would address the first of the five "Left for you" items in that session's final
report; the rest of the prompt is that session's reconstruction, which this session checked
against the tree. **Resolved: finding 23's open question, which commit takes a special page that
the post-bot download changes.** Ben selected the rule that the bot run's own commit takes every
such change. The rule is the new last paragraph of "## After a Wikisource bot run" in
`dot-claude/skills/mam-wikisource-refresh/SKILL.md`, beginning "Ben decided on 2026-10-01 that the
bot run's own commit also takes every change", and is committed with this entry. No other file
needed a change: step 1 of the skill's `references/dependent-refresh.md` already commits "the bot
run's own commit that `SKILL.md` describes", and `py/ws/pywikibot-setup.md`, "Post-run download
behavior", sends the reader to the skill's section.

**The facts the question showed**, established from the code and Git history before it was asked:

1. **The post-run download.** `py/subcommands/ws_bot_real.py` runs it only when the bot saved at
   least one chapter and none of `--no-post-download`, `--no-save` and `--identity-run` was given.
   `download_wikisource.run` refreshes the special pages before the saved chapters: it fetches the
   36 pages' metadata, checks that the eight special pages that are chapter pages have the page IDs
   and resolved titles of their chapter records, comparing no revision IDs, and with
   `force_download` fetches all 36 pages' content. It writes a page file, and then `manifest.json`,
   only when the bytes differ. It then force-downloads the saved chapters into `in/mam-ws/` and
   `in/mam-ws-revisions.json` and reparses their books.
2. **When the mirror changes.** The bot edits only chapter pages, so of the 36 special pages it can
   change only the eight that are chapter pages, and a page among them that it saves lands in both
   mirrors at the same revision. Every other change is someone else's edit made since the last
   download, and any new revision changes its page's manifest record even when the bytes are
   unchanged. A forced refetch of unchanged pages writes nothing: the manifest holds no fetch-time
   field, its stored key order is the order the code builds, and
   `test_special_mirror_matches_complete_api_oracle_reuse_and_force` asserts the unchanged bytes.
   The bot run of 2026-09-03, `031b4306`, saved Judges 5, one of the eight. The mirror's
   `judges-5` record holds revision 3080379, timestamped seven minutes before that run's commit,
   and Judges 5's record in `in/mam-ws-revisions.json` holds the same revision.
3. **Precedent.** `a41fbcdd` is the only commit on any ref that touches `in/mam-ws-special/`. It is
   not an ancestor of the last recorded bot run, `298958d3`; the merge `85cb7acd` joined their two
   lines, and no commit that `main` gained after that merge touches `in/mam-ws/`,
   `in/mam-ws-revisions.json`, `in/mam-ws-special/` or `py/ws/ws_bot_edit_history.md`. No
   recorded bot run has yet happened with the mirror present.
4. **The bot run's own commit.** `298958d3` holds the saved chapters' books in `in/mam-ws/` and
   `in/mam-ws-revisions.json`, the outputs of the reparse and the full mega, and the new entry in
   `py/ws/ws_bot_edit_history.md`; the change logs followed in `cf8e7be7`.
5. **Products.** No product generator reads the mirror; under `py/`, only the download, its test,
   the setup guide and the pipeline graph name it.

**Ben's selection.** The question and its three options were this session's wording; Ben's part
is the selection, made at about 08:03 New York time on 2026-10-01. To "After a live bot run, which
commit should take the changes that the post-run download makes under in/mam-ws-special/?
Selecting an option approves its wording as shown in the preview.", Ben selected "Bot run's commit
(Recommended)", whose preview showed the paragraph now in the skill. The other two options were
"Separate commit first", which would have put every special-page change in a special-page refresh
committed before the bot run's commit, and "Split by cause", which would have put the pages the
bot saved in the bot run's commit and the other changed pages in a special-page refresh committed
first. Both "Separate commit first" and "Split by cause" would also have added a sentence to step 1
of `references/dependent-refresh.md`, because a commit made first moves `HEAD` before that step
checks that `HEAD` still equals the recorded starting commit.

**A second writer in the clone.** This session verified the clone shortly after 07:46 New York
time, clean on `main` at `3bd8d24c`, and made no edit until Ben's selection. At 08:00:19 the second
step-2 session committed `a36aa24a` in the same clone and pushed it, with the entry above. Every
edit of this session came after Ben's selection and was made on top of that commit; this session's
recheck of `HEAD` before staging found the new commit, and its own commit follows it.

**Also corrected in place in this file:**

1. In "Approved remediation implemented; final gates pending, 2026-10-01", finding 23's row:
   "Unresolved, for Ben: the question the plan leaves open" now reads "Unresolved when this entry
   was written, and decided by Ben on 2026-10-01, as "Ben's decision on the commit for a bot run's
   special-page changes, 2026-10-01" records: the question the plan leaves open".
2. In "Final integration and configuration deployment completed, 2026-10-01": "Every deferral,
   no-action disposition and unresolved question there remains as recorded." now reads "Every
   deferral, no-action disposition and unresolved question there remains as recorded, apart from
   finding 23's question, which Ben decided later that day, as "Ben's decision on the commit for a
   bot run's special-page changes, 2026-10-01" records."

The plan, `doc/PLAN-remediate-review-findings-2026-09-29.md`, is a receipt and stays as written.

**Verification of this entry.** This entry, its two in-place corrections and the skill's new
paragraph are one commit on `main`. It changes no source file, product or generator, so neither the
suite nor the mega is owed. Before the commit, `git diff --check` passed, and
`py/tests/test_receipt_update_links.py`, `py/tests/test_prose_conventions.py` and
`py/tests/test_prose_mark_order.py` passed through `py/main_test.py`. No test reads the skill:
under `py/tests`, `git grep` finds `dot-claude/skills` only in two strings of
`py/tests/test_mega_coverage.py` and in the module docstring of
`py/tests/test_prose_conventions.py`, and `mam-wikisource-refresh` nowhere. The live copies of the
skill change only when `--sync-user-config` deploys this commit from `origin/main`.

This update remains `State: open` while its base survives.
