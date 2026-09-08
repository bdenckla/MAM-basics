# Codex Sol Design A re-review of the 2026-09-07 public-repository window

State: completed 2026-09-08. This is an additional Codex half of the second dual-agent review under
`doc/dual-agent-review.md`, requested after the first Codex half had been run with Terra. It
preserves `doc/codex-review-findings-2026-09-07.md` and does not revise the frozen Claude findings.

## Scope and method

This is Design A from `doc/dual-agent-review.md`: I read the pre-reconciliation Claude report at
`9e6e9e17:doc/review-findings-2026-09-07.md`, re-derived selected claims from immutable Git objects,
and inspected the primary MAM-basics range `b4706759..8bf586a3`. I also used the public
phonetic-hbo pages at `7322b665` for the post-stress-meteg census and inspected the local
MAM-for-Sefaria range `ce1e04c..cf23b478`.

The review did not read MAM-private, github-misc, or hbofonts. It did not recreate the absent public
source clones or inspect their remote trees. It created only ignored scripts under
`.novc/sol-review-2026-09-07/`; no tracked source or generated artifact was changed during the
review.

## Independence caveat

The current Claude file already had the Terra reconciliation appended. My first whole-file read
reached that reconciliation before I switched to the pre-reconciliation Git blob. I therefore knew
that Terra had confirmed nine selected Claude claims, rejected none, and found no omission. I did
not read the Terra findings file before freezing this Sol report, but this Sol re-review is not
perfectly blind to the Terra result. Every Sol result below was re-derived from the frozen Claude
report, the declared anchors, and the public data.

## Claude finding 3 has 368 variant rows but 370 duplicated chanted words

The core diagnosis in Claude finding 3 is correct, but its opening count and unit are false. The
public phonetic-hbo pages have 368 qamats-variant rows: 307 in prose verses and 61 in poetic verses.
Those rows contribute 370 duplicated chanted words: 307 in prose verses and 63 in poetic verses.
The rows for Psalms 35:10 and Proverbs 19:7 each contribute two duplicated chanted words.

The public-page re-derivation otherwise supports the finding. It counts 233,277 prose chanted words
and 29,542 poetic chanted words, against the survey JSON's 233,586 and 29,605. It reproduces all 232
post-stress-meteg records, with 178 in prose verses and 54 in poetic verses, and agrees with every
record's stress position. The finding should say that the survey double counts 370 chanted words
from 368 qamats-variant rows, not “MAM's 368 `מ:קמץ` words.”

## The scope census lists five exact trailer spellings, not four

The scope section correctly reports 220 non-merge commits, 121 without a `Co-Authored-By` trailer,
96 subject-only commits, and 99 commits with a trailer. Its next clause says those 99 trailers are
spelled four ways, but the parenthetical list and an independent census contain five exact lines:

1. 92 instances of `Co-Authored-By: Codex <noreply@openai.com>`.
2. 3 instances of `Co-Authored-By: Codex <codex@openai.com>`.
3. 2 instances of `Co-authored-by: Codex <noreply@openai.com>`.
4. 1 instance of `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
5. 1 instance of `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

Finding 23.1's narrower statement that the Codex trailer has three spellings is correct.

## Omission: the landed product artifacts make `git diff --check` fail

`git diff --check b4706759..8bf586a3` exits 2 with 210 whitespace errors: 21 trailing-space lines
and 189 blank final lines. The errors are distributed across 87 `MAM-for-Sefaria/` paths, 111
`MAM-simple/` paths, and 12 `gh-pages/MAM-for-Sefaria/` paths. The 189 blank final lines are in the
generated Unicode-name listings. The 21 trailing-space lines are in nine AJF CSV rows and twelve
MAM-for-Sefaria HTML or CSS lines.

The errors arrived with the landed product artifacts in `cf7c7a35` and `4195440e`; the landing
commits preserved them from the source products. This is an artifact-hygiene finding, not evidence
of a behavioral defect, but the Claude review does not record it and the reviewed range is not clean
under the same `git diff --check` used in the first Codex periodic review.

## Ten Claude claim groups confirmed directly

1. Finding 2's Deuteronomy 33:29 placement is correct. At `8bf586a3`, `005v.json` has
   the form `יִשְׂרָאֵ֜ל` after its final line-end marker, while `006r.json` begins its first
   line with the form `מִ֣י`. The two scan crops show that 005v ends before `יִשְׂרָאֵ֜ל` and
   006r begins with the text `יִשְׂרָאֵ֜ל מִ֣י כָמ֗וֹךָ`.
2. Finding 6's vendored-copy census is correct at the anchor: 39 of the 44 source-mapped
   `MAM-simple/py-examples/` files are blob-identical to `py/`, and the five named copies differ.
3. Finding 10's checked record errors are present: the third-stage plan says “43 rows across seven
   destination repositories”; two plans use the hyphenated Aleppo manifest path; the maintenance
   runbook retains its 19-clone scope; and the two corpus-scope docstrings retain the false
   “24 line-break files” statement.
4. Finding 12's checked stale post-stress-meteg records are present. The rollout records still say
   231 after the JSON reached 232, the method file still says 3,181 Fit-for-MAS records rather than
   496, the survey docstring says the diagnostic records twelve dual-cantillation numbered verses
   while the JSON list is empty, and the removed M23 fragment remains cited.
5. Findings 13.2 and 13.3 are correct. The two `TYPE_2_FOLLOWING_FILTER` names survived the declared
   complete rename, and the BHS row is derived from UXLC and WLC data while the rendered prose makes
   an unsupported claim about BHS and calls the two transcriptions editions.
6. Findings 14.3, 14.4, and 14.5 are correct. The MAM-with-doc source-tree row describes content
   that is under `gh-pages/MAM-with-doc/`; the MAM statement describes four evacuated source repos
   as still holding `LICENSE.md`; and three tracked Taamey D copies fall outside the named font
   exceptions.
7. Finding 16's mark-order counts are exact at the anchor: 48 of 427 Hebrew runs in
   `missing_sections_nakh.html` and 2 of 54 in `missing_sections_torah.html` are outside MAM-normal
   order.
8. Findings 17.1 and 17.3 are correct. `no_marks_comparison_key` removes every `Mn` and `Cf`
   character and is the sole content comparison in both line-break checks; `diff_mpp.run()` chooses
   the output path before it prefixes revisions with `legacy:`.
9. Finding 19's checked README and licence statements are false at the anchor: the two unsupported
   test options, the two deleted entry points, the root-level `linux-sh/` path, and both unnumbered
   announced counts remain present.
10. Finding 20's link graph re-derives exactly from the anchored Git blobs: 576 tracked HTML pages,
    eleven pages with no inbound link from another tracked page, and zero dead internal targets.

## Static checks that found no further defect

The MAM-basics range contains 257 commits, 220 non-merge commits, and 72 non-merge commits on the
first-parent line. A scan of all changed Python at the anchor found no added `sys.path` mutation and
no added text-file `open`, `Path.open`, `read_text`, or `write_text` call lacking an explicit
encoding. The apparent `sys.path[0]` match is prose in `MAM-simple/py/main_test.py`, not a mutation.

I scanned every non-merge commit subject and its changed top-level paths. Every commit fits one of
the Claude report's declared streams or the remediation stream; I found no unaccounted commit.

## Limits of the Sol re-review

The Sol re-review did not independently check every Claude finding. It did not rerun the full suite,
the mega pipeline, artifact generators, GitHub Pages deployments, issue state, or mutable worktree
and task-folder state. It did not re-derive the private-side facts, the absent source-clone safety
reports, the Yeivin or Breuer source claims, or every code fragility grouped under finding 17.

## Relation to the preserved Terra review

The Terra report checked findings 1, 4, 5, 7, 8.1, 8.2, 13.1, 14.1, 14.2, 15, and 18. The Sol
report checked a largely separate set: findings 2, 3, 6, 10, 12, 13.2, 13.3, 14.3, 14.4, 14.5,
16, 17.1, 17.3, 19, and 20, plus the scope census and commit-stream coverage. The Terra report's
conclusion that its selected claims had no rejection or omission remains accurate for the Terra
selection. The Sol report adds two partial corrections and one omitted artifact-hygiene finding;
the Sol report does not replace the Terra report.
