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

The procedure-record update follows this entry. A fresh-task remediation plan with concrete
editorial wording remains the next close-out phase, and no remediation named above has begun.

Product axis: this decision record and the procedure-record update reach no repository product.
Act axis: they are ordinary local commits on the unpushed review branch; they perform no external
write, destructive operation, receipt rewrite or primary-checkout change.
