# Numbers 9:7 — Ben’s confirmed doc-note wording correction

State: live; Ben confirmed 2026-10-14; proposal submitted in #314; correction applied on Wikisource in revision 3092657; #314 closed 2026-10-19.

Ben explicitly confirms that the doc-note should name yod rather than vav,
in `Sentinel_ed2fbcd60d008191a26921b22a3c08d9`. The
[readable case](review.html#numbers-yod-label) shows the exact before/after wording;
[adjudications.json](adjudications.json) retains the confirmation and declared edit.

Current cached wording, with stored punctuation:

<div lang="he" dir="rtl">(כתיב מלא וי"ו)</div>

Ben’s confirmed corrected wording:

<div lang="he" dir="rtl">(כתיב מלא יו"ד)</div>

The edit changes only the letter-name abbreviation. It preserves U+0022 QUOTATION
MARK and both parentheses. The selected MAM word contains yod and no vav; the
Introduction and the note’s Leningrad clause describe the corresponding yod
difference. Existing [spelling-prose proofs](spelling-prose-proofs.json) retain
the faithful raw-note evidence.

The source remains `89cb865729b0876f1fd32a8a3579eaec80b4fc0c`. The doc-note is
`Numbers 9:7/2/0`, [parsed line 4976](https://github.com/bdenckla/MAM-basics/blob/89cb865729b0876f1fd32a8a3579eaec80b4fc0c/MAM-parsed/plus/A4-Numbers.json#L4976),
chapter revision **2987712**; the Introduction entry is `ch3:L153`.
The historical quotation is unchanged. This report update does not apply the
correction to Wikisource, a cache, dataset or edition, and does not create an issue
or merge main.

## Submitted to Avi

On 2026-10-17 at 20:20 UTC Ben asked for an issue for each correction he had approved in this review: “Sure, go ahead and file those 12 issues”. #314 proposed this correction to Avi.

## Applied on Wikisource

On 2026-10-19 skadish1 reported the correction done in #314, linking
[revision 3092657](https://he.wikisource.org/w/index.php?diff=3092657&oldid=2987712),
whose parent is the audited chapter revision **2987712**, and closed #314.
MAM-basics' chapter mirror holds that revision from `fd0d1b1d`, of 2026-10-28,
where the note has Ben's confirmed wording. A Claude session checked this against
the mirror on 2026-10-29 at Ben's request; [adjudications.json](adjudications.json)
records the application.
