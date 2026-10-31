# The first pen-stroke exemplars, 2026-10-30

State: executed 2026-10-30; four crops traced, judged and checked; Claude's readings of the marks await Ben's review
Updates and later status: [pen-stroke-exemplars-2026-10-30-update.md](pen-stroke-exemplars-2026-10-30-update.md).

Claude (Opus 5.5) wrote this record. It covers the execution of option 2 of the planning
session "Investigate a pen-stroke manuscript representation": four crops, a level-1 tracer, a
nib-fit statistic, strokes traced by eye, a sweep-and-residual tool, a lint and an overlay page.
It then judges whether the level pays. The representation and Ben's decisions about it are in
[pen-stroke-representation.md](pen-stroke-representation.md), whose numbering of the decisions
this record uses. The crops are described in
[pen-stroke-snips/README.md](pen-stroke-snips/README.md). Every reading of a mark below is
Claude's, from the crop image, and Ben has not yet checked it.

## Verdict

**The level pays in part.**

1. **What pays now.** Level 1 costs almost nothing: it is automatic and deterministic, and the
   lint checks it. The nib-fit statistic is cheap and agrees across both pages. Level 5's
   groups record something no transcription does: whether the two strands' vowels on a QUPO
   letter are one stroke or two.
2. **What does not pay yet.** Tracing whole words as strokes of one stiff nib, with medians
   placed by eye, leaves a pen residual of about a fifth of the ink even on well-preserved
   text. Decision 3 reads such frequent excursion on well-preserved text as a problem of the
   model, the image or the tracing, and here it cannot yet be said which.

Two things should come before more tracing: Ben's review of the four crops' readings, and a nib
model that can turn or press.

## What the crops show

These are Claude's readings of the crop images. They describe where each mark stands and
argue nothing from it, under the guard in
[meteg-after-silluq-job-4-12.md](meteg-after-silluq-job-4-12.md).

1. **F043A, the second atom of the chanted word עַל־פָּנָֽי׃, Exodus 20:2 (MAM's numbering).**
   Under the nun there are one long bar, a dot under the bar's right end, and a vertical stroke
   under its left half; over the nun there is a short stroke. So the bar serves both strands.
   Alone it is the pataḥ of the עליון strand, and with the dot it is the qamats of the תחתון
   strand. In the stroke-SVG, stroke s7 is in two groups, as decision 5 foresaw.
2. **F043A, the atom מִתָּ֑חַת of Exodus 20:3.** Under the tav there are two separate marks: a
   plain bar under its left half, and a bar with a tick under its right half. The atnaḥ's
   inverted V stands below, between them, and a stroke stands over the tav. No stroke here
   serves both strands.
3. **F102A, the chanted word עַל־פָּנָֽי׃ of Deuteronomy 5:6.** Under the nun there are one
   short bar and one vertical stroke beginning at the bar's right end, and no dot. Where F043A
   has three strokes, this copy has two. The stroke-SVG puts the vertical stroke in a qamats
   group and in a silluq group, each with a note naming the other reading.
4. **F102A, the atom מִתָּ֑חַת of Deuteronomy 5:7.** The ink has flaked. Under the ḥet and the
   tav there are three separate bars, an inverted V whose apex stands under the ḥet's right
   half, a dot, and a bar with a tick under the tav. Level 5 cannot say which bar belongs to
   which letter or strand, so the three bars are grouped as "bar under the letter".

**What the transcriptions record.** MAM keeps the strands apart. The UXLC, in this repository's
copy, has both vowels on the letter in three of the four atoms: the qamats and the תחתון
strand's accent, then a CGJ, then the pataḥ and the עליון strand's accent; the תחתון accent is
an atnaḥ, or at פני the U+05BD of the silluq. In the fourth, its Deuteronomy 5:8 מִתָּ֑֜חַת, it
has the qamats, the atnaḥ and the geresh, and no pataḥ. That is a statement about the UXLC.
Whether the manuscript's three bars there include the tav's pataḥ is one of the readings Ben is
asked to check. Neither transcription says whether the manuscript has one bar or two. The
pixels show it, and the stroke groups state it checkably, beside the strokes they are made of.

## The nib

**Fitted before any tracing.** Ink components of 300 pixels or more were taken for letters.
The letters' widths against direction fit a stiff flat nib at these values:

| Crop | Width (px) | Angle | Edge (px) | Misfit (px) |
| --- | --- | --- | --- | --- |
| F043A פני | 11.97 | 86.5° | 6.09 | 1.38 |
| F043A מתחת | 12.53 | 79.5° | 4.13 | 1.06 |
| F102A על־פני | 14.40 | 80.0° | 4.34 | 2.01 |
| F102A מתחת | 14.78 | 88.5° | 5.22 | 1.32 |

The nib's long side is nearly upright, which is why square script's horizontals are heavy and
its verticals thin. At the 120 pixels a centimetre measured on F043A's photograph, the nib is
about 1.0 to 1.2 mm wide.

**Fitted again once, to the ink under the traced strokes.** The letters gave widths of 12.30 to
14.58 pixels and angles of 78.5° to 99.5°. The fit cannot tell a nib of width w at angle a from
one of width e at a + 90° with edge w. Two of the four first came out in the second form, so
the tool now reports the reading with the larger width. No one crop's marks determined a nib,
so the marks were fitted together. They gave a near-round pen, 5.56 pixels wide with a
4.55-pixel edge, with a misfit of 0.73 pixels over 878 samples. The marks' widths barely vary
with direction, as Ben expected when he said the modulation is "less frequently in diacritic
mark" (decision 2). The stroke-SVGs use these refitted values.

## The pen residual

| Crop | Strokes | Of other words | Ink no stroke explains | Sweep beyond the ink | Residual pieces |
| --- | --- | --- | --- | --- | --- |
| F043A פני | 12 | 0 | 8.7% | 22.2% | 1 |
| F043A מתחת | 26 | 5 | 19.2% | 21.9% | 0 |
| F102A על־פני | 29 | 12 | 25.3% | 22.0% | 11 |
| F102A מתחת | 26 | 2 | 23.1% | 31.4% | 12 |

The first percentage is of the ink in fills judged ink, and the second of the area the strokes
sweep.

1. **Damage shows.** The flaking crop has the most sweep beyond the ink, and its residual
   pieces include four judged damage.
2. **Well-preserved text shows excursion too.** On F043A, the pe's right side and the nun's
   stem are 9 to 11 pixels thick, where the stiff nib lays down about 7 on a vertical. The
   pe's tongue and every dot are round, where a rectangular nib is square. These are
   excursions of the model, not of the scribe.
3. **The tracing adds its own error.** Medians placed by eye are uncertain by a pixel or two,
   and each crop had one correction pass, for medians visibly off the middle of their ink.

Until a nib that can turn or press is tried, and Ben has traced one crop himself, the residual
cannot separate these three sources.

## The cost

Telling what each mark is cost the most time, not drawing it: zooms, the line counts, and
whose ink was in the box. Nineteen of the 93 strokes belong to other words, twelve of them in
F102A's על־פני alone, where the next line's lamed ascenders reach into the box. Option 3's
tracing aid would speed up the drawing, which was not the bottleneck. Tracing only the marks
of a word, with its letters left as fills, would cut most of the cost for questions like
those above.

## Corrections to the plan

1. **The plan's example מִתַּ֨חַת**, with a qadma, was written from memory. MAM's עליון form has
   a geresh: מִתַּ֜חַת. MAM numbers that verse Exodus 20:3, and the UXLC numbers it 20:4.
2. **The pixel size the plan left unknown has been measured.** Sefaria's images are 3989 × 4258
   and 3943 × 4272 pixels. The Internet Archive's raw images are the same photographs
   uncropped and more compressed.
3. **The plan's figures that this record reuses were read again at their sources on
   2026-10-30.** These are Collidoscope's five colours and the Aleppo scale-2 stroke width of
   two or three pixels. No figure from the plan's sub-agents is reused.

## What Ben may want next

Each of these needs Ben's word.

1. **Check the four readings above** against the crops, in
   [pen-stroke-snips/overlays.html](pen-stroke-snips/overlays.html).
2. **Trace one crop himself**, to separate tracing error from model error.
3. **Try a nib that turns within a stroke, or a flexible one,** and compare the residuals.
4. **Trace only the marks** of more QUPO-like letters, if the question is how the two strands
   are written.
