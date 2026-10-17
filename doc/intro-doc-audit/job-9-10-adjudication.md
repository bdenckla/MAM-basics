# Job 9:10 — Ben’s decision on the reversed reference

State: live; Ben decided 2026-10-17; proposal submitted in #312, not applied.

A footnote in chapter 1 of the Introduction, under the heading below, gives as
an example of a typing difference a word it places at Job 10:9. The word is in
Job 9:10. The [readable case](review.html#job-chapter-verse) shows the passage
and the proposed edit, and [adjudications.json](adjudications.json) records the
decision as `JOB-9-10-BEN-20261017`.

<div lang="he" dir="rtl">הבסיס להקלדה ולתיעוד</div>

The current reference, chapter 1 line 258 (revision 3087907, still the live
revision on 2026-10-17):

<div lang="he" dir="rtl">לדוגמה: באיוב י,ט התיבה</div>

## Evidence

- MAM's Job 9:10 has the word, by its letters; Job 10:9 does not.
- The example's Westminster link asks for `Tanach.xml?Job9:10-9:10`, and its
  Mechon Mamre link, `c2709.htm`, is Job chapter 9.
- Its mgketer link, `mikra/30/9/1`, uses book 30. In the repository's mgketer
  numbering (`py/mb_cmn/verse_external_links.py`) Job is book 29 and book 30 is
  the Song of Songs. That link was not opened, and #312 does not mention it.

## Ben's decision

Ben, 2026-10-17 at 18:47 UTC, in Claude Code session `2f820cf6-3d3f-4301-bdb1-d71685173e13`:
“Regarding "Job 9:10 — chapter and verse reversed in an example", yeah this is pretty obviously a typo of the form you identify. Please create a github issue for it.”

The proposal changes only the reference's two numerals, from Job 10:9 to
Job 9:10, and [#312](https://github.com/bdenckla/MAM-basics/issues/312) proposes it to Avi. Nothing here edits the
Introduction.
