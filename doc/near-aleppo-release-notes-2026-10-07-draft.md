# Near-Aleppo (NA) release notes — 2026-10-07 (draft)

State: live; release-notes dry run, not an announced release

This draft describes a hypothetical release from MAM-basics commit
`2f3013113b3c2abfa23a7cea30bb10b4eb5c441d`. The main change since the first
announcement is a new JSON contract for notes whose targets differ from MAM's:
the dataset now includes the NA-adjusted clauses. Pointed ketivs now
retain final punctuation at additional sites, and the example edition has ketiv
as its primary text with pointed qere above it.

## Dataset changes

### NA-adjusted note content is included in the JSON

All 1,548 notes whose targets differ from MAM's now store the NA-adjusted
note content and the original MAM context separately. Previously the
dataset kept the original note body in parameter 2, and the example edition's
renderer supplied the NA-adjusted presentation. Consumers can now render the
stored roles directly, without consulting a review ledger or repeating the
editorial transformations.

The two changed-note template names have changed:

| Earlier name | Current name |
| --- | --- |
| Note `נוסח למקרא על פי המסורה` | Note `נוסח עם הקשר מקרא על פי המסורה` |
| Note `הערה-2 למקרא על פי המסורה` | Note `הערה-2 עם הקשר מקרא על פי המסורה` |

Their parameters have these roles:

| Parameter | Role |
| --- | --- |
| Parameter `1` | Near-Aleppo's Scripture target. |
| Parameter `2` | The NA-adjusted clause, or an empty array. |
| Parameter `מקרא על פי המסורה` | MAM's original structured target. |
| Parameter `הערת מקרא על פי המסורה` | The remaining original MAM clauses, in their original order, or the complete original note. |

There is an NA-adjusted clause in 1,047 notes. In the remaining 501,
parameter 2 is empty and the complete original note remains in MAM context.
Scroll-note parameter 3 and evidence flags keep their existing roles.

**Consumer action:** Update the closed template dispatch for the new names and
parameter sets. Interpret an agreement in parameter 2 as agreement with
near-Aleppo; interpret an agreement in the MAM-note parameter as agreement with
MAM. Keep the preserved MAM target and note clauses out of the Scripture
projection. The consumer notices in all 24 book files explain the new contract.

### Final punctuation in pointed ketivs

The stored pointed ketiv now includes a final maqaf at 36 additional sites and
a final U+05C0 sign at five additional sites. U+05C0 is the glyph near-Aleppo
uses for both narrow-sense paseq and legarmeh. These additions preserve the
pointing's existing letters and vowel and accent marks. The qeres are unchanged.

**Consumer action:** Preserve the final punctuation when selecting the pointed
ketiv. A final maqaf joins the ketiv to the following atom; do not insert a
second maqaf as a separator between the ketiv and qere alternatives.

An offline review extract records the selected sites with their notes and
neighboring verses, including punctuation that was already present. Its
[plain-text companion](https://github.com/bdenckla/MAM-basics/blob/2f3013113b3c2abfa23a7cea30bb10b4eb5c441d/out/near-aleppo/review/ketiv-final-punctuation.txt)
provides the full site list. The extract's two sections cover 42 maqaf cases
and 12 U+05C0 cases; the larger totals include already-present punctuation.

### Other ketiv/qere representation corrections

The pointed ketiv at 2 Samuel 15:8 is now encoded as `יָשֹׁ֨יב`, with holam
before qadma on the shin. The letters and marks are unchanged; their stored
order has been corrected.

Four paired ketiv/qere templates now have the name `קו״כ` instead of `כו״ק`,
following the corresponding MAM source correction:

- 2 Samuel 20:23
- Jeremiah 48:21
- Ezekiel 39:25
- 2 Chronicles 13:19

The ketiv, qere, and adopted pointed ketiv at these sites are unchanged. The
template name specifies MAM's qere-first order; parameter 1 remains the ketiv
and parameter 2 remains the pointed qere. The example edition's current
ketiv/qere display is described below.

Beyond the note-content migration and consumer-notice updates, these are the
only changes to the book payloads: 41 final-punctuation additions, the mark-order
correction, and four template renames. MAM's original target copies, evidence
flags, and all other Scripture forms and alternatives are unchanged.

## Accompanying documentation and example edition

The documentation now explains the stored note roles and distinguishes
implemented templates from planned work. In particular, the template reserved
for marks without letters or space at 2 Samuel 18:20 remains unimplemented;
it is no longer listed as part of the current consumer contract.

The editorial-policy page has a shorter retained-feature list and removes the
claim that the holam-haser-for-vav code point establishes the manuscript's dot
placement. The coverage page credits J. David Stark's Aleppo Codex Index. The
site's license inventory now identifies the near-Aleppo assets explicitly.

The documentation uses shared English styling, keeps unpointed Hebrew in its
default font, and uses relative links to the MAM-parsed-plus documentation.
The example edition uses the shared MAM-with-doc stylesheet plus its own
ketiv/qere styling. Ketiv is now the primary text, using the stored pointed
ketiv where available; pointed qere appears above it in an HTML ruby annotation
at the same size, with a small vertical gap. Trivial ketiv/qere templates also
have both readings in ruby, with their qere source metadata available on hover.
An absent reading has an editorial label in its own position. Existing notes
remain beside the text, and the ruby display adds no synthesized qere notes.
The note-content migration preserves the NA-adjusted clauses' presentation.

## Release contents and remaining work

The intended dataset ZIP would contain `README.md`, `LICENSE.md`, and the
24 book JSON files in `plus/`, all from `out/near-aleppo/`. The `review/` extract,
including its embedded font, remains outside this dataset-only ZIP. These release
notes would be a separate GitHub release attachment. The
[NA documentation](https://bdenckla.github.io/MAM-basics/near-aleppo/) and
[near-Aleppo example edition (NAEE)](https://bdenckla.github.io/MAM-basics/near-aleppo/edition/)
remain live pages that can change independently of a dataset release. The
dataset's license remains CC BY-SA 4.0; its attribution is in `LICENSE.md`.

**Release remains deferred.** Ben wants to resolve more ketiv/qere issues
before announcing another release. One-sided ketiv/qere handling, the planned
2 Samuel 18:20 representation, and the other cases listed under
[What is still pending](https://bdenckla.github.io/MAM-basics/near-aleppo/coverage-and-status.html#pending)
remain outstanding. This dry run introduces no new reading decisions.

## Dry-run comparison and verification

Ben reported the first announcements on Tuesday, 2026-10-06, at 9:06 a.m. and
4:35 p.m., New York time. No release tags were recorded at those times. This
draft uses reconstructed comparison anchors:

| Announcement | Comparison anchor | Evidence |
| --- | --- | --- |
| Dataset and documentation, 9:06 a.m., New York time | `a287e556b2626533ed8710108e546da7a60b3fcf` | This clone records a push at 8:30:06 a.m., New York time. |
| NAEE, 4:35 p.m., New York time | `429e452e8d4b72bf702c0cf996f641bdeaa89f87` | This clone records a push at 4:16:41 p.m., New York time. |

The note-content migration was already included in the afternoon anchor. The
next observed main commit, `cbafab6dbe867d8901794cde6af25688201154b1`, was
committed at 4:33:59 p.m. but first recorded by this clone at 4:39:56 p.m.,
New York time. Its dataset is identical to the afternoon anchor; its shared
documentation styling may already have been on origin at the second email.
These records establish comparison boundaries, not the exact GitHub Pages
deployment served to email recipients.

Inspection covered the endpoint diffs of the dataset, runtime inputs,
generators, documentation, and example edition. An independent structured
comparison of all 24 book files confirmed the note counts and the 46
remaining payload changes described above. The focused command
`./.venv/Scripts/python.exe py/main_near_aleppo.py --check` passed: all five
census files, the note reviews, the dataset and population file, and the
generated pages were current. The separate
`./.venv/Scripts/python.exe py/main_near_aleppo.py --punctuation-review --check`
also passed for the offline extract. Manuscript images were not consulted for this
dry run; the notes describe repository changes and existing attributed evidence.

The full mega and suite were not run for this Markdown-only draft, following
the focused-check cadence in `doc/review-trial.md`. No tag, ZIP, or GitHub
release was created. Before a real release, select its final commit and tag,
remeasure the changes, and replace this draft's hypothetical date and scope.
