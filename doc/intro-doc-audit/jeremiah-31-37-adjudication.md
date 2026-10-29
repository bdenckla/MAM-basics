# Jeremiah 31:37 — Ben’s adjudication of the doc-note quotation

State: live; Ben adjudicated 2026-10-14; proposal submitted in #313; correction applied on Wikisource in revision 3092656, without the optional circle; #313 closed 2026-10-29.

This note records Ben’s direct adjudication and contextual observations from
`Sentinel_a32e0898f09c8191bc489d5b907129fd`. Codex prepared the research record on
2026-10-14 in the isolated branch, starting at `555311ca884106f72b97fe0852f0a99784447108`.
The machine-readable companion is [adjudications.json](adjudications.json).
The readable comparison is [the Jeremiah case](review.html#jeremiah-accent).

## Current quotation and Ben’s proposed correction

The current cached doc-note’s Aleppo quotation is retained verbatim:

<div lang="he" dir="rtl">הִנֵּ֛ה יָמִ֥ים [] נְאֻם־יְהֹוָֽה</div>

Ben’s proposed corrected quotation is:

<div lang="he" dir="rtl">הִנֵּ֛ה יָמִ֥ים [֯] נְאֻם־יְהוָ֑ה</div>

The chapter 5 quotation, also retained verbatim, is:

<div lang="he" dir="rtl">יָמִ֥ים [֯] נְאֻם־יְהוָ֑ה</div>

Ben judges the doc-note’s U+05BD to be an error and asks for U+0591 etnaḥta
(his “atnax”), agreeing with chapter 5. He also asks to remove the ḥolam dot,
which he reports is absent from the manuscript. Adding the orphan masorah circle
between the brackets is optional: Ben explicitly says that excluding it is valid
and is not a correctness issue, whether or not the circle is discussed.

The three recorded edits are limited to U+05BD → U+0591 on the divine name,
omission of U+05B9 HEBREW POINT HOLAM there, and optional inclusion of U+05AF
HEBREW MARK MASORA CIRCLE in the gap. The leading phrase and all other source
characters are retained. The main report validates this proposal against those
declared edits; it does not treat the proposal as an already changed source.

## Sources independently checked

The audit source remains `89cb865729b0876f1fd32a8a3579eaec80b4fc0c`. The faithful chapter cache
and parsed note both contain the current U+05BD and ḥolam dot. The Introduction
contains U+0591, no ḥolam dot, and the orphan masorah circle. Parsed MAM mark order
and faithful raw-source mark order are preserved separately.

- [Introduction chapter 5, line 458](https://github.com/bdenckla/MAM-basics/blob/89cb865729b0876f1fd32a8a3579eaec80b4fc0c/in/mam-ws-intro/ch5.mediawiki#L458), cache revision **3087740**.
- [Parsed doc-note](https://github.com/bdenckla/MAM-basics/blob/89cb865729b0876f1fd32a8a3579eaec80b4fc0c/MAM-parsed/plus/C2-Jeremiah.json#L9544), pointer `/book39s/0/chapters/31/37/2/1`, chapter revision **3088451**.
- Faithful raw chapter: `in/mam-ws/C2-Jeremiah.json`, chapter key `לא`, verse marker `<קטע התחלה=לז/>`.

Ben’s adjudication selects the doc-note correction for this case. The broader audit’s
other manuscript and attribution questions remain separate.

## Three contextual facts Ben asked to retain

1. **The broken etnaḥta.** Ben reports that the accent is broken and judges its
   non-contiguous shape to have been laid down originally, rather than caused by
   aging or later damage. His supplied local crop is
   `C:/Users/BenDe/OneDrive/Pictures/Screenshots/Screenshot 2026-10-14 114737.png`.
   Codex inspected that exact file locally: 72533 bytes,
   SHA-256 `363034f1ad10d2cc0c5f4e25079f0c0f6e805bd7eb465a4c6e3fd32b17baba81`. The crop visibly has separated lower
   accent strokes at the disputed location and no visible ḥolam dot over the divine
   name. This visual inspection supports those visible features; the original
   formation of the broken shape remains Ben’s interpretation.
2. **The torn leaf.** Ben identifies this as the famous torn leaf of Aleppo and
   places the passage in its extant section. That provenance is recorded as Ben’s;
   the cropped word alone does not independently identify the leaf.
3. **The recent restoration.** Ben attributes to Avi the recent addition of the
   needed phrase <bdi lang="he" dir="rtl">נְאֻם־</bdi>. The cached history independently
   confirms the restoration. It does not independently identify the Wikisource
   editor as Avi; that attribution remains Ben’s.

The supplied screenshot stays at its original local path. It was not copied into
the repository, embedded in the report, uploaded or published. Only its identifying
metadata and the attributed observations are recorded here.

## Recent restoration: bounded cached history

The earlier cache at `3c58d0871210fc01298979f286e19bac9d11d58d` has this Aleppo clause:

<div lang="he" dir="rtl">הִנֵּ֛ה יָמִ֥ים [] יְהֹוָֽה (חסר ניקוד ברווח המיועד ל"קרי ולא כתיב")</div>

The refreshed cache at `647f5e225f69782194137e74627cfaced4a7d2a2` has:

<div lang="he" dir="rtl">הִנֵּ֛ה יָמִ֥ים [] נְאֻם־יְהֹוָֽה (חסר ניקוד ברווח המיועד ל"קרי ולא כתיב")</div>

The Aleppo clause changed only by restoring the missing phrase. The U+05BD and ḥolam
dot were already present in the earlier cache, and the gap still lacked the circle.
The refreshed cache commit is dated 2026-10-13; the preceding inspected snapshot is
dated 2026-10-06. These Git dates bound the cached observations, not the original
creation of the error.

The audit’s retained [MAM-basics #304](https://github.com/bdenckla/MAM-basics/issues/304)
snapshot records the requested restoration and the closed issue. Its
[completion comment](https://github.com/bdenckla/MAM-basics/issues/304#issuecomment-6138147770) is by `skadish1`,
dated `2026-10-13T04:19:55Z`, and links a Wikisource comparison from revision
**2988015** to **3088451**. This agrees with the cache’s current chapter revision.
No live issue or Wikisource fetch was needed for this check.

## Copying theory: hypothesis, not established history

Ben suggests that the post-gap phrase might have been pasted separately from the
preceding verse, omitting sof pasuq, instead of pasting one whole quotation starting
with <bdi lang="he" dir="rtl">הִנֵּ֛ה יָמִ֥ים</bdi>.
The cached text of Jeremiah 31:36 does end with:

<div lang="he" dir="rtl">נְאֻם־יְהֹוָֽה׃</div>

Its final U+05BD functions as silluq; the disputed quotation in 31:37 belongs at the
midverse etnaḥta position. The preceding verse’s ending without sof pasuq matches
the current post-gap quotation exactly. That establishes a textual match, not a
copying event. The wrong mark predates the recent restoration, so that restoration
does not establish the origin of the mark.

No Wikisource edit, issue/comment, dataset or edition change, main integration,
deployment, or screenshot publication is part of this research update.

## Submitted to Avi

On 2026-10-17 at 20:20 UTC Ben asked for an issue for each correction he had approved in this review: “Sure, go ahead and file those 12 issues”. #313 proposed this correction to Avi.

## Applied on Wikisource

On 2026-10-19 skadish1 reported the correction done in #313, linking
[revision 3092656](https://he.wikisource.org/w/index.php?diff=3092656&oldid=3088451),
whose parent is the audited chapter revision **3088451**. MAM-basics' chapter
mirror holds that revision from `fd0d1b1d`, of 2026-10-28, where the quotation reads:

<div lang="he" dir="rtl">הִנֵּ֛ה יָמִ֥ים [] נְאֻם־יְהוָ֑ה</div>

The divine name has atnaḥ and no ḥolam dot, as Ben asked, and the gap still has no
masorah circle, which he left optional. A Claude session checked this against the
mirror and closed #313 on 2026-10-29 at Ben's request;
[adjudications.json](adjudications.json) records the application.
