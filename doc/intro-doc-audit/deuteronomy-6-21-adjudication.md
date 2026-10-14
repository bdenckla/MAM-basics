# Deuteronomy 6:21 — Ben’s adjudication of the opening source list

State: live; Ben adjudicated 2026-10-14; proposed source correction not applied.

Ben requests removing only bare ל from the opening defective-vav list in
`Sentinel_4e66eddc6bf48191ba19bb417ae3ae7f`. His manuscript assessment is attributed
below. The [readable case](review.html#deuteronomy-leningrad-spelling) retains the
complete original note and full English translation, then shows the precise
opening-clause correction. [adjudications.json](adjudications.json) retains both
the original and proposed complete notes.

## Exact proposed edit

Current opening clause:

<div lang="he" dir="rtl">=ל,ל1,ש,ש1,ק3[אחרי תיקון],ו,ל3,ל9,פטרבורג-EVR-II-B-8[טקסט בין השורות] ומסורת-ל וטברניות ורמ"ה (כתיב חסר וי"ו)</div>

Proposed opening clause:

<div lang="he" dir="rtl">=ל1,ש,ש1,ק3[אחרי תיקון],ו,ל3,ל9,פטרבורג-EVR-II-B-8[טקסט בין השורות] ומסורת-ל וטברניות ורמ"ה (כתיב חסר וי"ו)</div>

The edit removes U+05DC HEBREW LETTER LAMED and the following U+002C COMMA
immediately after the initial equals sign. It retains that equals sign, the
distinct sigil ל1 for Firkovich B17, the Masorah reference מסורת-ל, and all other
source characters, clauses and punctuation. It does not remove every lamed or
every reference to Leningrad. No source correction has been applied.

## Why this direction

Ben distinguishes this decision from choosing an arbitrary direction merely to
make the note internally consistent. The note gives the plene-vav direction more
clearly and redundantly: its explicit Leningrad alternative and its concluding
manuscript statement both favor it.

<div lang="he" dir="rtl">ל!=וַיּוֹצִיאֵ֧נוּ (כתיב מלא וי"ו)</div>

<div lang="he" dir="rtl">כתי"ש=חסר וי"ו, כתי"ל=מלא וי"ו.</div>

Ben also independently examined the manuscript. He judges the spelling to be
“pretty clearly” plene-vav despite the poor condition at this location. This
external manuscript assessment is Ben’s, rather than an inference made by the
report generator or a reading independently adjudicated by Codex.

## Image and condition

Ben supplied the local crop
`C:/Users/BenDe/OneDrive/Pictures/Screenshots/Screenshot 2026-10-14 143534.png`.
Codex opened that exact file locally: 131388 bytes,
SHA-256 `745f14bd5cca6608dca902bb3d95ead6054ab1d2069db4792beb443fbc127ae6`. The crop has a visibly
irregular/obscured area across the word. The cause remains uncertain: Ben mentions
aging damage, erasure, or both. The local inspection does not resolve that cause
or provide an independent adjudication of the spelling.

The supplied image stays at its original path. It is not copied into the
repository, uploaded, embedded or committed; this record contains identifying
metadata and attributed observations only.

## Source and scope

The source remains `89cb865729b0876f1fd32a8a3579eaec80b4fc0c`. The doc-note is
`Deuter 6:21/2/0`, [parsed line 3794](https://github.com/bdenckla/MAM-basics/blob/89cb865729b0876f1fd32a8a3579eaec80b4fc0c/MAM-parsed/plus/A5-Deuter.json#L3794),
pointer `/book39s/0/chapters/6/21/2/1`, chapter revision **2987745**. The complete
four-clause note and translation remain unchanged as historical evidence.
Only the proposed note has the initial list entry removed. Research-only updates
do not edit a cache, dataset, Wikisource page, issue/comment or main.
