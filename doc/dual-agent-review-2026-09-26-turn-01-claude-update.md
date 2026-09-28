# Updates to turn 01 of the 2026-09-26 dual-agent review

State: open, first entry 2026-09-27. Every entry here corrects or supplements
`doc/dual-agent-review-2026-09-26-turn-01-claude.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit. A
correction, later decision or later disposition goes in a sibling file named `<stem>-update.md`,
which is what this file is for turn 01 of the September 26 review.

## Ben's first close-out decisions and a finding he added, 2026-09-27

Recorded by a Claude session on 2026-09-27, New York time: the session that wrote turn 05 of the
round. The alternating exchange was then waiting for Codex's turn 06, which records an
acknowledgment of turn 05 or an objection to it, and close-out step 1 had not begun. Ben answered
every question that turn 05's section "Close-out step 1's list after this turn" put to him, and he
added a finding of his own. He also asked where his answers were kept: "I don't like that my
decision is recorded here. How will Codex know to record it?" This entry is the record. It records
decisions and executes no remediation.

1. **Finding 30.3, the Cairo captions: standardize on "digital page".** Turn 05 said that only Ben
   could say whether the CSIC viewer's "digital image" and "digital page" name the same field. Ben,
   2026-09-27:

   > Yes, both descriptions are acceptable (though of course it is preferable to standardize on
   > one of the two; I am indifferent between them). In other words, this is not one of those sets
   > of manuscript images where the image is of a page-spread instead of a page. That is the main
   > way I'm aware of in which images do not correspond to pages.

   The session suggested "digital page", which the 1 Kings 7:37 Cairo caption and both EVR
   captions already use, and Ben replied:

   > I agree to the term "digital page."

   At `f4d81285` the change reaches two captions: "Cairo, digital image 204"
   (`gh-pages/post-stress-meteg-post-silluq-1k14v14.html:23`, from
   `py/author_site/post_stress_meteg_post_silluq_page.py:282`) and "Cairo, manuscript page 110,
   digital image 103" (`gh-pages/post-stress-meteg-post-silluq-1s17v5.html:25`, from line 229 of
   the same module). The decision concerns the published captions, which are finding 30.3's
   subject. Whether the provenance records and the image file names, which also say "digital
   image" or "image", follow is for the remediation plan to propose.
2. **Finding 4.2: restore the `@media` prohibition.** Ben chose, on 2026-09-27, to restore the
   sentence that `4e30b0f4` deleted, answering "I concur." to the session's option "Restore the
   sentence (recommended).", which proposed this wording for the CSS rule in `holman/WORKFLOW.md`:

   > Every authored CSS theme declares `color-scheme: light dark` on `:root`, and every theme
   > custom property that stores a color uses a `light-dark(<light>, <dark>)` pair. Fixed badge
   > foregrounds and backgrounds remain literal colors. Do not add an
   > `@media (prefers-color-scheme: dark)` block.

   The comma after `` `:root` `` repairs finding 4.2's textual defect. The session's reasons for
   recommending the restoration: the two authored Holman stylesheets handle dark mode only through
   `color-scheme: light dark` and `light-dark()` pairs, and neither has a dark-mode `@media` block;
   `py/py_render/rt_assets.py:8–10` keeps the same prohibition for generated report assets; and
   the one dark-mode `@media` block on the site, `gh-pages/wlc/style.css:413–418`, sets a
   `filter` on opted-in scans, which `light-dark()` cannot express because it chooses only colors.
3. **Finding 36, added by Ben: `holman/assets/table_data_findings.css` has too generic a name.**
   Ben, 2026-09-27:

   > That has become a terrible (too generic) file name BTW. Since a CSS file isn't really going
   > to be used in a URL, I think we are free to change it to something better, no? Let's record,
   > as part of this review, that "bad name" as a human-generated finding.

   The file lies outside the window's diff: no commit in `71f96ca3..f4d81285` changed it or its
   published copy. The facts a rename needs, at `f4d81285`:
   1. In the tree, the published copy `gh-pages/holman/table_data_findings.css` is requested only
      by the stylesheet links of the two pages that use it,
      `gh-pages/holman/table_data_findings.html:17` and
      `gh-pages/holman/table_data_findings_suppressed.html:17`.
   2. Its JavaScript twin, `holman/assets/table_data_findings.js`, has the same name; both
      template paths are set at `py/py_render/rt_assets.py:43–44`.
   3. The published CSS and JavaScript names are derived from the page's name, by
      `output_html_path.with_suffix(".css")` and `.with_suffix(".js")`
      (`py/py_render/rt_html.py:120–121`), and the page's name is fixed on purpose. A comment
      beside Ben's decision of 2026-09-03 on the page's title says "The FILENAME is unchanged,
      deliberately: table_data_findings.html is the URL index.html links and the one Ben has
      already sent to correspondents" (`py/py_render/rt_html.py:58–60`). A new name for the
      published copies therefore has to be decoupled from
      the page's name; renaming only the authored templates in `holman/assets/` needs no such
      change. `py/main_0_mega.py:572` describes the step's outputs as "the
      gh-pages/holman/table_data_findings* pages with their CSS and JS".
   4. Finished records that cite the old path, among them
      `doc/dual-agent-review-2026-09-16-turn-01-claude.md:1085`, stay as written under D12.

   The new name, and whether the JavaScript twin and the published copies take it too, are Ben's
   choice in remediation, as an editorial change under D7.
4. **Finding 30.3, the Leningrad captions: a side-lettered designation names a page, and the
   "folio 159A" form is avoided.** The session asked whether the 1 Samuel 17:5 caption should say
   "folio 159A", like the five other Leningrad captions, or keep "F159A". The earlier
   session recorded Ben's 2026-09-27 response as follows. This is the session's
   transcription; its contradictory second sentence has not been verified against the
   source conversation:

   > Call it ither page F159A or just call it F159A. Do not call F159A. By our
   > newly-decided-upon terminology, F159 is the folio, it has an A and a B page (a recto and a
   > verso) that belong to it.

   Later the same day he added how the avoided form is to be read where others use it:

   > One more note regarding phrases like "folio 57a". I think we should avoid them, but they are
   > common in existing references in published books and web sites. They should be taken to
   > imply a parenthesized meaning of "(folio 57)a" meaning, somewhat visually
   > counterintuitively, that the "folio operator" binds more tightly than the a/b operator.

   The first recorded quotation says both "page F159A or just call it F159A" and "Do not
   call F159A." Its missing or mistaken wording is unknown; it must not be repeated as a
   verified exact quotation. The surrounding explanation and Ben's later clarification
   record the decision: "F159A" and "page F159A" are allowed, and the repository avoids
   "folio 159A". The session's suggestion of "folio 159A" is withdrawn. The tree defines a page as
   one side of a folio (`doc/meteg-after-silluq-snips/README.md:52`, `evr-ii-b-55/README.md:163`).
   Read as "(folio 57)a", the "folio 57a" form states nothing false, but it is the form this
   repository's own prose avoids. The captions that use it, or its "leaf" variant, are the five
   other Leningrad captions, "folio 195B", "folio 398A", "folio 377B", "folio 379B" and "folio
   380A"; the EVR caption's "folio 57a" (`gh-pages/post-stress-meteg-post-silluq-1s17v5.html:33`);
   and the five Aleppo captions that write "leaf", as in "leaf 83r"
   (`gh-pages/post-stress-meteg-post-silluq-1k14v14.html:17`). Cambridge's "page 0073B" already
   follows the terminology. The remediation plan proposes the wording for each caption, and for
   the tree's own records that use the form, such as "folio 159A" and "folio 195B" at
   `doc/meteg-after-silluq-in-uxlc-and-wlc.md:84–85`, for Ben's approval under D7. A quotation or
   citation of a published source keeps that source's wording. The terminology has no standing
   home in the repository's instructions or skills yet; whether to give it one is for the
   remediation plan to ask.

With this entry, every question that turns 03 to 05 put on close-out step 1's list has Ben's
answer. Every other finding reaches close-out step 1 as the reconciliation table and turns 03 to
05 leave it, and finding 36 joins that list.

## Review closed; complete disposition package proposed, 2026-09-27

Prepared by Codex on 2026-09-27, New York time. Ben's instruction was: "Continue the review
process. I think in the narrow sense, the review is done, but next comes remediation, or whatever
is needed to prepare for remediation". The proposals below are Codex's reconstruction, not
decisions attributed to Ben when proposed. Ben approved the complete package on
2026-09-28; the approval entry below distinguishes that scope from the later plan's
concrete wording approval.

**The review is closed; remediation remains unstarted.** Turn 06 acknowledges turn 05 without
an objection. Its acknowledgment satisfies the stopping rule in `doc/dual-agent-review.md`.
The earlier entry preserves Ben's approved choices for finding 4.2, the Cairo captions, and
side-lettered page designations, plus his added finding 36. Those choices are not being asked
again. This entry supplies close-out step 1's previously missing list covering every finding.

The controlling passages are `doc/periodic-review.md`, "The check runs autonomously, and Ben
sees the findings once", "Close-out: from findings to dispositions", and "Separate defects
from editorial proposals". The next step after Ben decides this package is a fresh-task
remediation plan with concrete editorial wording. Approval of this package decides what that
plan includes, defers, or records as resolved; it does not approve unspecified editorial text.
Every proposed fix defaults to later, in the remediation phase.

### Source inventory and current checkout

The review evidence is turn 01's reconciliation table together with the corrections in turns 03
and 04, turn 05's acceptance, turn 06's acknowledgment, and the earlier entry in this update.
The reviewed endpoints remain `71f96ca3..f4d81285`; current-main measurements below do not
enlarge that window or rewrite its findings.

The source checkout for preparation was `C:/Users/BenDe/GitRepos/MAM-basics`, clean on
`dar-2026-09-26` at `db62361e9fb3c8688c5130267c3fd98f2a38ae7e`. The historical shared checkout
named in the review turns was not registered locally. Codex created and attached the local
managed checkout `C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics`, reused the
existing branch `dar-2026-09-26`, and locked it with "active dual-agent review 2026-09-26".
The clean primary clone was returned to `main`.

As D11 requires before close-out edits, primary `main` at
`85cb7acd8df98089614de8e3e30bb67bc5a2c36a` was merged into the review branch, producing
`d13270a056ba14424600c1da84ab728f4728f4b2` without conflicts. That merge is the development
baseline for this package. Both the required review head and current `main` are ancestors.
Only Codex writes, stages, or commits in the development checkout; the two sub-agents checked
bounded groups of findings read-only. No private repository or session record was read.

The task that executes the eventual approved plan owns final integration. It uses the primary
interpreter `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` while running tools
and generators in the development checkout. The worktree and branch remain available through
close-out; neither is retired by this preparation task.

### Complete proposed disposition list

"Plan a fix" means a defect survives and its remedy belongs in the later remediation plan.
"Defer" means the item remains unfixed for the stated decision or evidence gap, rather than
silently choosing policy. "Already resolved" applies only to the named subitem and current-main
baseline. No numbered finding is dropped because another subitem is resolved.

1. **Plan a fix: September 16 close-out credits and completion claims.** Correct attribution,
   the false claim that current `main` had already resolved part 19.4, and the remaining wording
   and wrapping defects in the live update homes, adding a single update sibling for the
   executed remediation plan where needed.
2. **Plan a fix: stale pending and closing-push language.** Correct live present-state claims
   and record the missing provenance of concrete wording approval without inventing an approval
   or treating a reconstruction as Ben's words.
3. **Plan a fix: live references to deleted plans and reports.** Repoint current guidance and
   describe retained historical evidence accurately; the retired `ac_paths.py` reference is
   already resolved by current-main retirement and is not restored.
4. **Plan a fix: prescribed wording that was missed or changed.** Repair the surviving mechanical
   defects and apply Ben's already-approved Holman CSS paragraph; propose adding 4.7's census-method
   attribution from the existing decision record, with the wording approved in the later plan.
5. **Plan a fix: the September 10 live update's stale descriptions.** Correct its descriptions
   of retired files, deleted update files, and completed closing actions in that update.
6. **Plan a fix: misleading retirement guidance and a dead link; propose a policy decision for
   remaining inbound references.** Repair demonstrated live-text defects, and ask the plan to
   distinguish current guidance from historical evidence when a referenced document is retired.
7. **Plan a fix: the retirement's receipt-link corrections and incomplete issue-family link;
   defer classification of the five Holman evidence notes.** Correct the live receipt accounts
   and the missing update-family link in MAM-basics issue 269; retain the supported commit-graph
   facts without claiming that a GitHub remote-ref read occurred, and propose no retrospective
   repinning for 7.3 because the existing immutable links show the same receipt-family bytes.
8. **Propose a policy decision: reclassifying a receipt as a maintained document.** Record a
   narrow route requiring Ben's explicit decision and a preserved account of the transition;
   the Psalms 72:15 reclassification itself remains raised, not a defect to undo.
9. **Plan a fix: terminal update states and missing completed-plan states.** Give live update
   files their required `open` state and put later execution status in the permitted live homes.
10. **Plan a fix: update entries with numbered or wrong passage locators.** Name each corrected
    passage by searchable words from that passage and correct the mislocated quotation.
11. **Propose a policy decision: rules lost or displaced in the Claude-wrapper conversion.**
    Restore shared worktree safeguards, transcription-evidence limits, searchable update
    locators, and the long-lived backup exception to homes both agents load; defer the twelve
    separately enumerated legacy clauses in 11.1 until Ben chooses which remain policy.
12. **Plan a fix: obsolete instruction citations and future-tense wrapper descriptions.**
    Correct current guidance and the wrong risk-item reference; retain intentionally historical
    citations and skip paths already removed by current-main retirement.
13. **Plan a fix: the symmetric-instructions completion account, missing budget-reversal
    provenance, and missing section-level reconciliation; defer retirement of the overtaken plan.**
    Record the established reversal to 32,768 project-instruction bytes in the live update homes
    without inventing a new budget choice or forcing one name on different baseline descriptions.
14. **Plan a fix: inconsistent documentation exemptions.** Define exemption by documentation
    and instruction content, so executable code under an instruction directory receives its
    applicable checks, and bring `product_scopes.py`'s account into agreement.
15. **Plan a fix: Wikisource-refresh worktree and final-check guidance.** State the normal
    linked-worktree behavior, retain `REPOS_ROOT` only as a supported unusual-layout override,
    and make the suite's optional status at final integration accurate.
16. **Plan a fix: the retirement citation gate's broad matches and missed exact path forms.**
    Narrow the gate to actual relocated-path references and independently check its coverage;
    remeasure current references rather than carry endpoint counts forward as current facts.
17. **Plan a fix: retirement lints, data contracts, and stale descriptions; defer a new token
    detection policy.** Cover force-flag forms, make the unused error field truthful, and correct
    docstrings without claiming that every exception is swallowed or that a constant measured
    the operator's token; leave 17.2 unresolved until its measurement choice is made, and defer
    17.8's link/junction simulation, broader Git filename-call coverage, and Hebrew presentation-form
    exclusion from Latin NFC scans.
18. **Already resolved in part; plan fixes for the remaining image-tool retirement descriptions.**
    Current-main retirement removed the dead product example, `cam1753_paths.py`, and obsolete
    module inventory; correct surviving line-ending, entry-point, instruction-body, omitted-editor,
    and historical execution-credit claims in their permitted homes, and propose describing the
    completed-row table as retained-file labels while disclosing the four inconsistent boundaries
    rather than silently adjudicating manuscript ranges.
19. **Plan a fix: the historical line-break comparison projection.** Name that the retired
    comparison ignored all U+05BD, including silluq, as well as rafe; do not restore or change
    retired comparison code merely to remedy its retained description.
20. **Plan a fix: four example-shaped tests and incomplete generated-artifact freshness coverage.**
    Replace the added checks with an independent differential or mechanical lint and include
    `style.css` and `filter.js`; do not invent a claim that those assets are stale today.
21. **Plan a fix: mark-order descriptions, terminology, and the latent vowel-point classification.**
    Describe U+05C9's implemented priority, repair the terminology, and exclude U+05C9 from
    `_VOWEL_POINTS` without changing Hebrew or claiming an unverified conflict with the SBL manual.
22. **Plan a fix: the manuscript-indexing reader's lost child content and misleading guides.**
    Preserve the recognized child form at Psalms 10:5 through the current
    `py/mb_cmn/mam_xml_verses.py`, and distinguish individual strands from a combined
    representation; defer whether implicit-maqaf pairs should be joined and propose no
    corpus-text change or new strand-selection policy.
23. **Plan a fix: the surviving smaller code and documentation defects.** Remove unused code,
    correct stale pointers and descriptions, extend geometry coverage, repair the latent diagnostic,
    and enforce the supported finite child projection; recheck current-main deletions before
    proposing a code change and choose no new ketiv/qere policy.
24. **Plan a fix: public-data consumer notices and their coverage.** Correct the parsed-plain
    rule, the guide's universal three-encoding claim and the audit's adoption of that claim,
    fourth-index coverage, and first-use gloss for Narpas;
    the Google JSON inventory gap in 24.4 is already resolved by `a41fbcdd` and no Google
    pipeline or documentation is restored.
25. **Plan a fix: demonstrated pinned change-log omissions, empty dates, stale heading, and
    split Hebrew clusters; defer 25.4's release naming/date convention.** Keep the hidden qere and
    stress-helper differences distinct from pointing migrations and old-format note or wrapper
    differences, and approve the pinned-release remedy explicitly before touching that record.
26. **Defer the rendered-date policy conflict.** Ben must choose how the existing clock-label
    rule applies to converted source revision and Holman message dates before policy or output
    is changed.
27. **Defer the Job 4:12 interpretation discrepancy.** The census and published account disagree,
    but neither reviewer adjudicated the sources; preserve the current text and survey until
    Ben chooses an account or authorizes the necessary evidence work.
28. **Plan a fix: the AI translation's title, labels, shortened quotation, and misleading
    cleanup instructions.** Give English prose its English runway and correct the source
    heading and caveat without implying human review of the translation.
29. **Plan a fix: landing-page and reader-document factual defects; defer optional terminology
    and product-scope choices.** Correct established statements and the incomplete license row;
    leave 29.5's proposal/suggestion naming and 29.6-29.7's questions for Ben.
30. **Plan a fix: post-silluq presentation defects and Ben's chosen locator vocabulary.** Repair
    the demonstrated promises, links, layout, and smaller defects; use `digital page` for the
    Cairo captions, propose explicit page wording for side-lettered locators, and defer 30.4's
    shelfmark spelling decision.
31. **Plan a fix: stale post-silluq research records and imprecise citations.** Reconcile established
    contradictions and counts in the proper live or update homes; defer 31.8's coverage of existing
    manuscript observations in maintained reports and the ledger's report links.
32. **Plan a fix: twenty noncanonical transliterated image filenames.** Use the current converter
    `consensus_to_ascii` in `py/author_boj_util/author.py`, update active references, and retain
    finished receipt paths as historical evidence; the two English `final-word` names are outside
    the finding.
33. **Plan a fix: established figure, attribution, and checkout-scope errors.** Correct the
    supported errors and narrow unverified Python, locale-URL, and Wikisource claims without
    upgrading an internal disagreement into a proved external fact.
34. **Plan a fix: unclear names and referents.** Name the subjects consistently and describe the
    session contributions accurately, respecting turn 03's narrower correction to the
    "two sessions" claim rather than adopting the table's original overstatement.
35. **Record no-action, deferred, and already-resolved dispositions for all nine judgment questions.**
    Keep privacy, process, attribution, browsing, representation, and dependency choices separate
    from defects; propose no historical-act repair for 35.4, and the retired Google comparator
    in 35.7 no longer needs a new exemption.
36. **Propose an authored-asset rename for Ben's added finding.** Rename the CSS template to
    `holman/assets/mam-suggestions-report.css` and its JavaScript twin to
    `holman/assets/mam-suggestions-report.js`, while retaining the existing published asset
    names and stable HTML URLs.

### Reader-facing documents and data: the next plan's approval surface

The risk ordering in `doc/periodic-review.md`, "Present remediation by public-facing risk",
governs the detailed plan. Its first group presents exact current and proposed reader-facing
wording for findings 3, 18-19, 21-22, 24-25, and 28-34 where their changes reach a README or HTML;
the list does not approve those future replacements merely because they correct defects.
Formatting and links are identified separately from wording.

The second group presents the consumer-notice changes embedded in distributed JSON and XML,
and any index-output effect of fixing the manuscript reader, with their affected fields or
structures. No corpus-text, strand-selection, or Job 4:12 data change is proposed by this
package. An expected unchanged generated product must be distinguished from a changed one.

The third group summarizes the remaining changes as live Markdown and receipt updates, source
comments and docstrings, canonical instructions and skills, and code and lints. The eventual
plan identifies concrete wording for editorial changes and the approved scope of each policy
repair. It includes targeted checks, Black for changed Python, the full suite after the last
test-risky change, affected hand-run generators, and the mandatory final merged-main mega.
Existing generated diffs from `main` are baseline changes, not remediation diffs to recommit.

### Choices proposed for Ben, and items deliberately deferred

The following recommendations make the judgment parts of the list explicit. Ben approved
them on 2026-09-28 as dispositions for the next plan. The plan still presents the
concrete editorial wording for approval before implementation.

| Finding | Proposed decision for the next plan |
|---|---|
| 6 | Explain how current-guidance references reach a maintained successor and historical references reach the full SHA of the last commit whose tree contains the complete receipt family, retaining the current rule for future links; never bulk-edit finished bases. |
| 7 | Repair the known receipt accounts and issue-family link; defer classification and editing of the five Holman evidence notes; make no retrospective repinning for 7.3 because its immutable links show identical family bytes. |
| 8 | Specify a narrow, Ben-authorized reclassification route that records the transition and the disposition of its update sibling, rather than treat the Psalms 72:15 decision as an unauthorized act to reverse. |
| 11 | Restore the shared safeguards and evidence limits in 11.2-11.5; keep all twelve clauses in 11.1 deferred for a separate explicit selection. |
| 13 | Record the established budget reversal and proved record discrepancies, and supply the missing section-level reconciliation table; defer retirement of the overtaken plan until its surviving work is mapped. |
| 14 | Make exemption depend on documentation/instruction content; executable hooks and helpers receive checks even below `dot-claude/` or `dot-Codex/`. |
| 17 | Repair the contracts and descriptions; retain the existing ordinary-token precondition, leave 17.2 unresolved pending a measurement method, and defer the three preventive proposals in 17.8. |
| 18.8 | Describe retained-file labels and their four inconsistent boundaries in the table; defer any manuscript-range adjudication without a consistent independent source. |
| 25 | Correct the demonstrated change-log defects only through an explicitly approved pinned-release remedy; defer changing the release naming/date convention in 25.4. |
| 26-27 | Defer the source-date labeling policy and Job 4:12 adjudication; neither is resolved by reviewer agreement. |
| 22, 29-31 | Defer implicit-maqaf joining, the proposal/suggestion label, questions 29.6-29.7, shelfmark spelling in 30.4, and coverage of existing manuscript observations in maintained reports and ledger links in 31.8. |
| 30.3 | Keep Ben's existing decisions; propose `page 83r` for Aleppo's `leaf 83r`, `page F195B` for Leningrad's `folio 195B`, and `page 57a` for EVR's `folio 57a`, applying the same form to the corresponding captions and maintained records while preserving quotations. |
| 36 | Rename the authored CSS and JavaScript pair only, to `mam-suggestions-report.css` and `.js`; keep published asset paths and the stable report HTML URLs. |

Finding 35's nine questions retain these individual dispositions so that "defer finding 35"
does not hide its scope:

| Subitem | Proposed disposition and reason |
|---|---|
| 35.1 | Defer judgment on private-tree paths and filenames in the public long-path guide; no private content is read to decide it here. |
| 35.2 | Defer judgment on private-review counts and file-kind metadata in the public procedure. |
| 35.3 | Retain the dated quotations as recorded, with no invented source; propose correcting the present location of the September 16 review record in the detailed plan. |
| 35.4 | No historical-act repair is proposed: the noticed review edits, integration acts, cleanup ownership, and data changes are not newly declared defects; defer any new process policy, while the plan may propose clearer undated-rule attribution. |
| 35.5 | Defer the pages' voice, inspection attribution, and source-line presentation choices. |
| 35.6 | Defer a new browsing or robots.txt rule; obey existing source-specific restrictions if evidence work is separately authorized. |
| 35.7 | Already resolved as a live-output question by Google Sheet retirement `a41fbcdd`: the comparator and `out/diff_mamws_mamgo.json` were removed; do not restore either to extend an exemption list. |
| 35.8 | Defer the `slhw-desc-0` representation choice for legarmeh; do not infer its semantics from similarity to the element's children. |
| 35.9 | Defer whether to document or remove PyYAML's untracked-validator use; no dependency removal is authorized by noticing the gap. |

The twelve missing clauses in finding 11.1 remain individually identifiable by the argument's
own anchors: "as unverified", "quite ready", the default-branch override, the optional second
suite, "thorny merge", `total_tokens`, "genuinely ends", "prescribe exactly what", "own words",
"Bold lead-ins", "deleting the count", and the three `py/foi/*_explanations.py` modules.
Deferral does not record any of those clauses as intentionally dropped by Ben.

### Preparation changes, verification, and remote backup

**Fixed in this live update: the claim that the inconsistent first page-designation quotation
was verified exact.** The original recorded wording is retained as a source transcription with
its contradiction disclosed; missing words are not invented. The decision is carried by the
surrounding explanation and Ben's later clarification, as turn 06 says.

This preparation changes only this live update. The review's numbered turns and frozen endpoint
remain intact. It proposes no product changes and runs no generator, full suite, deployment,
or final integration. Its checks are the diff, directly relevant document lints, and review of
the complete package against the agreed findings. Remediation checks remain for the approved
execution plan. Verification on 2026-09-27: the receipt-link, prose-convention, and prose-mark-order
checks passed (four tests); `git diff --check` passed. The restricted repository-standards
inspection exited zero and reported informational source totals; it did not expand remediation
scope. The independent package checks were reconciled before committing this entry.

**Backed up on 2026-09-28 after Ben's explicit approval.** Automatic approval review had
rejected the normal review-branch push twice on 2026-09-27, including after the D11 exception
was shown, because it considered authorization insufficient. Ben then explicitly authorized
the backup, and the normal push advanced `origin/dar-2026-09-26` from `db62361e` to
`572fa2aba1696c3afc7a6bfc56628fa2c559e168`. No workaround or force push was used; primary
`main` remains at `85cb7acd8df98089614de8e3e30bb67bc5a2c36a`.

## Ben approved the complete dispositions and branch backup, 2026-09-28

Recorded by Codex on 2026-09-28, New York time. Ben selected the question,
"Do you approve the proposed fixes, deferrals, and no-action dispositions?", and replied
"I approve". That approval applies to the complete 36-finding package committed at
`572fa2aba1696c3afc7a6bfc56628fa2c559e168`, including its policy recommendations, finite
asset-name proposal, already-resolved subitems, explicit no-action dispositions, and
deferrals. All fixes remain for later remediation. The approval does not supply approval
of unspecified editorial wording or authorize deferred semantic choices.

Ben separately selected the question,
"May I push the preparation commits to origin/dar-2026-09-26 as a backup?", and replied
"yes you may push". The authorized backup succeeded after a fresh fetch and exact
checkout/status verification; the remote branch now contains both the required `main`
merge and the preparation commit.

The next phase is the standalone detailed remediation plan, with concrete reader-facing
wording, distributed-notice effects, internal policy text, executable steps, verification,
and final integration. Implementation awaits that plan's approval. Step 1 is complete;
steps 2 through 4 remain pending. This update remains `State: open` while its base survives.

## Detailed remediation plan prepared; execution approval pending, 2026-09-28

Recorded by Codex on 2026-09-28, New York time. The standalone
[remediation plan](PLAN-remediate-review-findings-2026-09-26.md) uses the recovered
managed DAR checkout and requires the approval record at
`8ab079afbac0a6648385f725e51057c2f0fd293f`. It covers all approved active findings,
retains every approved deferral/no-action disposition, and presents exact public
wording before data effects and the lower-risk internal work. The proposed pinned
change-log correction explicitly includes useful alternative-change HTML/JSON,
five pointing migrations, and distinct unchanged-qere note/wrapper exclusions.
The plan names finite image mappings, receipt routing, independent checks,
commit/backup discipline, hand-run generators, final integration and deployment.

Two read-only agents checked the finding groups and the full draft. Codex reconciled
their material corrections and independently checked the current converter outputs,
all twenty image hashes, the sixteen Cambridge first/last stored labels and the two
substantive alternative values in the real change-log endpoints. The plan proposes
no new semantic decision for a deferred item. Preparing this plan changes no source,
product, image, issue, deployed instruction or frozen review turn.

**Clarified the push rule in response to Ben's question.** The live
`codex-worktree-tasks` skill's rule 4 restricts ordinary short-lived worktree backups
and contains a long-lived exception. The repository's `doc/dual-agent-review.md`,
"The shared worktree" (D11), explicitly requires DAR branch backups after every
commit and reserves `main` integration/push for final remediation. There is no DAR
backup prohibition. The earlier automatic-review authorization block was resolved
by Ben's explicit September 28 permission; that permission covers this preparation
backup too.

Step 1 remains complete. Step 2 now has a concrete standalone plan awaiting wording
and execution approval under `doc/periodic-review.md`, "Close-out: from findings to
dispositions" and D7. Steps 3 and 4 remain pending; no remediation implementation or
intermediate main integration has occurred. This update remains `State: open` while
its base survives.
