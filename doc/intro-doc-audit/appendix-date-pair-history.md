# The appendix’s completion date — history and Ben’s decision

State: live; Ben decided 2026-10-17; proposal submitted in #311, not applied.

The appendix sentence that dates the last round of corrections in the project's
second stage pairs 7 Tevet 5774 with “(10.12.14)”. 7 Tevet 5774 was 10 December 2013;
10 December 2014 was 18 Kislev 5775. The
[readable case](review.html#appendix-date-pair) shows the sentence, its history
and the proposed edit, and
[appendix-date-pair-history.json](appendix-date-pair-history.json) holds the
revisions, literal excerpts, method and limits.

The current sentence, appendices line 476 (revision 3088449, unchanged in
revision 3089143):

<div lang="he" dir="rtl">עוד שלב אחרון של עדכונים ותיקונים (בעיקר בהערות הנוסח) הסתיים בז' טבת תשע"ד (10.12.14).</div>

## The round of corrections

The sentence ends the first paragraph under the appendix heading below, the
account of the project's second stage: the Five Megillot and the other passages
missing from the Aleppo Codex. The appendix defines the round only as that
stage's last round of updates and corrections, mainly to the doc-notes. The
Torah paragraph before it puts that part's own final round in 5774, and its
footnote says that the doc-note work of that round was also done in the
Haftarot and the Five Megillot.

<div lang="he" dir="rtl">חלק שני: חמש מגילות ושאר המקומות החסרים בכתר ארם צובה</div>

## History

- Chapter 1's revision 517248, saved 2013-12-10 at 14:22 UTC, added the
  sentence with “(10.12.14)” already in it. Its parent, revision 516953
  of 2013-12-08, lacks it. A bisection of the page's 524 revisions found this
  edit ([diff](https://he.wikisource.org/w/index.php?diff=517248&oldid=516953)).
- On 2019-05-22 chapter 1's revision 900792 removed the paragraph, and two
  minutes later the appendices' revision 900793 added it
  ([removal](https://he.wikisource.org/w/index.php?diff=900792&oldid=889002), [addition](https://he.wikisource.org/w/index.php?diff=900793&oldid=888238)).
  The paragraph's line is identical in the two pages.
- A search of all namespaces' current wikitext for the sentence's opening words
  finds only the appendices page.

A sentence written on 10 December 2013 cannot report work ending on
10 December 2014. The history dates when the sentence was written, not when
the work ended, and the bisection does not exclude an earlier copy on another
page.

## Ben's decision

Ben, 2026-10-17 at 15:27 UTC, in Claude Code session `2f820cf6-3d3f-4301-bdb1-d71685173e13`:
“I'm satisfied to treat the hebrew date (ז' טבת תשע"ד) as definitive, since it is not the one in parens. And, the "wrongness" of the one in parens can be explained by an off-by-one typo in the year.”

He asked for the issue “even without evidence one way or another”. The
proposal changes only “(10.12.14)” to “(10.12.13)”.
[adjudications.json](adjudications.json) records it as `APPENDIX-DATE-BEN-20261017`, and
[#311](https://github.com/bdenckla/MAM-basics/issues/311) proposes it to Avi. Nothing here edits the Introduction.

## Scope

This research followed the original history pass, whose 94 dispositions
excluded this case as a contradiction within the appendix.
[revision-history-inventory.json](revision-history-inventory.json) keeps that
pass's classification.
