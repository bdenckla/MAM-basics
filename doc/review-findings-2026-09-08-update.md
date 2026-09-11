# Updates to the September 8 review findings

State: open, first entry 2026-09-11. Every entry here corrects a passage of
`doc/review-findings-2026-09-08.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written, like a pushed commit. A correction to one goes in
a sibling file named `<stem>-update.md`, which is what this file is for the September 8 review.
Nothing here edits the document it corrects.

## Finding 13.3's display fallback was retired on 2026-09-10

Recorded by a Claude session on 2026-09-11, for finding 3 of `doc/review-findings-2026-09-10.md`.
Two passages of `doc/review-findings-2026-09-08.md` are corrected.

**The Wave 3 technical disposition paragraph**, the one ending "Current-MAM and BHS-labelled
sources remain distinct", says both fallback sites select unannotated source text. That describes
`f1166057`'s design, which no longer exists. `3a1ab7f0` (2026-09-10 12:21, the same day as
`f1166057` at 08:42) removed both `mam_form or chanted_word` sites from
`py/author_site/post_stress_meteg.py`. That module's `_mam_form` now raises `SurveyProblem` for a
displayed survey entry with no `mam_form`, instead of looking a substitute spelling up in
MAM-private's Phonetic MAM, so no render path reaches the snapshot. The snapshot lookup is now
`_snapshot_unannotated_form`, private to `py/accgram/post_stress_meteg.py` and called only from
inside it. `CLAUDE.md`'s section "A code path reads MAM-private every time it runs, or never"
names this fallback as the case that produced that rule. The other three parts of the 13.3 remedy
hold: first-`rep`/first-unannotated-`fva` matching, preservation of the selected display marks,
and annotation validation. Re-establish: `git show 3a1ab7f0 --stat`, and Grep
`mam_form or chanted_word` over `py/` (no match).

**The final disposition table's 13.3 row**, which reads "Fixed in the Wave 3 technical phase at
`f11660576e440523e944598331e8ecc339dcdb26`", sends a reader to code that no longer exists. That
"Fixed" still holds for unannotated selection, matching and annotation validation. The display
fallback that `f1166057` made select unannotated source text was removed by `3a1ab7f0`: a
displayed survey entry with no `mam_form` now stops the render with `SurveyProblem`.
