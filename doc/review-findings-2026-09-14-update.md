# Updates to the 2026-09-14 public-repository review

State: open, first entry 2026-09-16. Every entry here corrects or supplements
`doc/review-findings-2026-09-14.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit. A
correction, later decision or later disposition goes in a sibling file named `<stem>-update.md`,
which is what this file is for the September 14 review.

## Ben approved the complete close-out decision package on 2026-09-16

Recorded by Codex on 2026-09-16 after the alternating review exchange closed without a remaining
disagreement. Ben approved the recommended package presented as one list covering every finding.
Approval records the decisions below; it does not execute remediation or approve wording that the
remediation plan must present separately.

1. **Finding 1:** remove the volatile tier-3 count rather than updating it, document the lint's
   boundary, correct the contradictory description, and add a general rule that changing an input
   used by a hand-run generator requires rerunning every affected generator.
2. **Finding 2:** repair the two hand-run generators and their regeneration and size documentation;
   treat the already-fixed defects as closed and leave the broader delete-and-rerun guard work with
   MAM-basics issue #278.
3. **Finding 3:** classify the two dated research reports as finished receipts, restore their
   pre-move text, and put the moved-path information in their live sibling update files; perform the
   other path and crop-rule corrections the finding names.
4. **Finding 4:** remove the volatile al-hatorah count rather than updating it, make the ambiguous
   atom-estimator error point to `py/main_verse_links.py --atom N` rather than adding a second
   `--atom` interface, and restore the missing letters-only-match note; the intentionally changed
   lookup policy needs no fix.
5. **Finding 5:** the transient generated-product rewrite was already reversed and requires no
   work.
6. **Finding 6:** remove the two unused imports so Ruff passes.
7. **Finding 7:** apply the recorded receipt and update-file decisions, add the missing pointers and
   outcome record, repair stale hashes and live line claims, and do not fabricate the historical
   remediation plan that was never written.
8. **Finding 8 and counter-findings C1 and C2:** apply the settled instruction and procedure
   corrections, including neutral Agent 1 and Agent 2 roles; perform the ignored Cambridge-tree
   move from the primary checkout after integration rather than granting a secondary-worktree
   exception; pin the explicit 4 + 24 + 8 Wikisource title list from the introduction chapter at a
   named commit; independently mirror all 36 pages while allowing the eight known cross-mirror
   overlaps and rejecting unexpected or within-mirror convergence; and add a general delegation
   counterpart to the Claude user-level instructions.
9. **Finding 9:** remove the obsolete hand-authored-directory example from MAM-basics issue #278
   rather than replacing it.
10. **Finding 10:** fix the four actionable source gaps; protect a shared review worktree with
    `git worktree lock` for the duration of the review rather than creating another session
    registry.
11. **Finding 11:** fix the remaining prose and usage defects; current `main` already supplied
    `doc/mega-timing-2026-09-11-update.md`, so that part requires no further work.

The procedure-record update was written immediately after this decision entry. At the time, a
fresh-task remediation plan with concrete editorial wording was the next close-out phase, and no
remediation named above had begun.

Product axis: this decision record and the procedure-record update reach no repository product.
Act axis: they are ordinary local commits on the unpushed review branch; they perform no external
write, destructive operation, receipt rewrite or primary-checkout change.

## Remediation completed and integrated on 2026-09-16

Later State: completed. The approved remediation was committed on the shared review branch,
fast-forwarded into `main`, pushed to `origin/main`, and deployed where the canonical user
configuration required deployment. `main`, `origin/main`, and the review branch all resolved to
`71f96ca3801863f6fa64c1fd0e75ccfde773439b` after integration.

The seven remediation commits were:

1. `e805bce0`, `Add live-update pointers to receipt bases`;
2. `b6f29b8d`, `Adopt one live update per receipt`;
3. `e776318e`, `Restore research receipts and correct live prose`;
4. `155bb778`, `Resolve incremental MAM-simple inputs explicitly`;
5. `82ad4b57`, `Harden atom lookup and Git filename lint`;
6. `61e01681`, `Correct canonical user configuration`; and
7. `71f96ca3`, `Repair live retirement plans`.

Every approved disposition has the following outcome:

1. **Finding 1:** the volatile counts remain removed; the product-scope description, lint
   boundary and rule for inputs of hand-run generators were corrected.
2. **Finding 2:** the Sefaria and OSIS hand-run generators and their regeneration documentation
   were repaired. Their products regenerated byte-identically. The broader whole-directory guard
   work remains with open MAM-basics issue #278, as approved.
3. **Finding 3:** the two finished research reports were restored, their moved paths were recorded
   in their live update files, and the approved link, path and crop-rule corrections were made.
4. **Finding 4:** the volatile al-hatorah count remains removed, estimator ambiguity now points to
   `py/main_verse_links.py --atom N`, and the letters-only-match note was restored. The intentional
   lookup policy remains unchanged.
5. **Finding 5:** no remediation was required because the transient generated-product rewrite had
   already been reversed.
6. **Finding 6:** the two unused imports were removed and Ruff passed.
7. **Finding 7 and counter-finding C3:** the one-live-update policy, base pointers and exception
   were implemented; stale facts, hashes, attribution and line claims were repaired; the missing
   outcome was recorded; and no historical remediation plan was fabricated.
8. **Finding 8:** the approved live instructions, cloud hook, procedures and user-configuration
   corrections were made. Neutral Agent 1 and Agent 2 roles remain in force, and the Claude
   user-level instructions now have the general delegation counterpart.
9. **Counter-finding C1:** the image-retirement plan now requires the primary checkout to move the
   ignored Cambridge tree after tracked integration. The move itself remains a later execution
   step of that retirement plan, not part of this review remediation.
10. **Counter-finding C2:** the Google-Sheet retirement plan now pins the exact 4 + 24 + 8 title
    inventory and the approved identity rules. Building the independent mirror remains a later
    execution step of that retirement plan.
11. **Finding 9:** MAM-basics issue #278's obsolete hand-authored-directory example was removed
    without replacement. The issue remained open with its state, labels and assignment preserved,
    and received the required dated Codex note and agent-written comment.
12. **Finding 10:** shared-review worktree locking, the Git filename-command lint, the
    `--full-history` description and UTF-8 stream configuration were implemented. The approved
    observations remain observations.
13. **Finding 11:** the remaining prose and usage corrections were made, using the existing
    `doc/mega-timing-2026-09-11-update.md` rather than creating another sibling.

The full suite and Ruff passed. The final mega completed successfully and left no tracked diff.
The Sefaria and OSIS hand-run products remained byte-identical. The receipt and filename lints
passed, with one live update per receipt and no numbered update sibling. The cloud-hook checks
passed locally; no real cloud container was exercised. Canonical user configuration was deployed
from the pushed `origin/main`, and its read-only follow-up check reported no drift.

Product axis: the generator repairs can reach the distributed Sefaria and OSIS products, but both
product sets remained byte-identical and the final mega generated no tracked change. Act axis:
issue #278 was edited and commented on, `main` was pushed, and canonical configuration was deployed
outside Git. No Cambridge files, worktrees, branches or review evidence were deleted.

The remaining `.novc/` evidence classification, shared-worktree unlock and removal, and deletion
of the merged review branch belong to the separate cleanup-only task. That cleanup does not leave
the review or its remediation open.
