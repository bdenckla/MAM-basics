# The first pen-stroke exemplars, 2026-10-30: update

State: open; first entries 2026-10-31

## Ben's review of the two crops on page F043A, 2026-10-31

Ben checked the readings of the marks in the two crops on page F043A. The two on page F102A
still await his review. His answers are quoted from the review session's chat.

1. **F043A's פני has two bars under the nun, not one.** The base's item 1 reads: "Under the
   nun there are one long bar, a dot under the bar's right end, and a vertical stroke under its
   left half". It concludes: "So the bar serves both strands." Ben: "s7 is certainly two bars".
   The two bars meet at x 26 to 27 of the crop, and the right one sits about a pixel higher.
   The right bar, with the dot under it, is the qamats of the תחתון strand. The left bar alone
   is the pataḥ of the עליון strand. So no stroke serves both strands, and the base's "stroke
   s7 is in two groups" no longer holds: s7 is now the right bar and s13 the left, each in one
   group. The vertical stroke stands under the left end of the right bar, not under the left
   half of one long bar. Ben confirmed the other readings: "s8 is indeed the dot of a qamats
   and s9 is indeed a silluq", and "s12 is indeed the revia".
2. **F043A's מתחת stands as read.** The base's item 2 reads: "Under the tav there are two
   separate marks: a plain bar under its left half, and a bar with a tick under its right
   half." It goes on: "No stroke here serves both strands." Ben: "2a and 2b: without having to
   type it all here, I'll just say that all your speculations about the four QUPO marks are
   correct". So the plain bar is the עליון strand's pataḥ, the bar with the tick is the
   תחתון strand's qamats, the inverted V is the atnaḥ, and the stroke over the tav is the
   עליון strand's geresh, not ink of the line above.
3. **The combined transcription is now each crop's primary one.** The base's "What the
   transcriptions record" begins: "MAM keeps the strands apart." By Ben's decision 13 in
   [pen-stroke-representation.md](pen-stroke-representation.md), the transcription that
   matters first is the combined one, from the UXLC unless Ben says it should be changed:
   "sometimes the manuscript doesn't superimpose taxton and elyon the way one would expect."
   Each stroke-SVG now gives it as `data-combined-chanted-word`, with `data-combined-source`,
   and [pen-stroke-snips/README.md](pen-stroke-snips/README.md) shows the four forms. MAM's
   strands stay beside it as secondary transcriptions.
4. **The strokes are now smooth curves.** By Ben's decision 14 in the same note, a stroke is
   "one or a few smooth curves" whose width is "smoothly modulated along them". The base's "a
   nib model that can turn or press", under "Verdict", is superseded by that. The next section
   reports the change.

## Profile 2: smooth curves with fitted widths, 2026-10-31

The stroke-SVGs now follow profile 2 of
[pen-stroke-representation.md](pen-stroke-representation.md). Each stroke's median is one or a
few cubic Bézier curves, with a width that varies smoothly along them, and its ends are round
or flat. A script of Claude's converted the medians placed by eye and fitted the widths and
ends to the ink. The schema note's "Profile 1 and profile 2" gives its steps. The base's
sections "The nib" and "The pen residual" describe profile 1.

| Crop | Strokes | Ink no stroke explains, profile 1 | Profile 2 | Sweep beyond the ink, profile 1 | Profile 2 |
| --- | --- | --- | --- | --- | --- |
| F043A פני | 13 | 8.7% | 5.8% | 22.2% | 11.5% |
| F043A מתחת | 26 | 19.2% | 7.7% | 21.9% | 10.8% |
| F102A על־פני | 29 | 25.3% | 11.8% | 22.0% | 12.3% |
| F102A מתחת | 26 | 23.1% | 13.1% | 31.4% | 16.8% |

The profile-1 figures are the base's, from before the bar under F043A's nun became two strokes.

The residual fell in every crop. The widths are fitted to the ink, so part of the fall is the
model's new freedom and says nothing new about the scribe. Two of the base's excursions, under
"Well-preserved text shows excursion too", are now within the model: the round dots, which
round ends or a width tapering at both ends can give, and the thick right side of F043A's pe,
which a width varying along the stroke gives. What remains is where a smooth width along one or a few curves cannot follow the ink:
most of all in the flaked crop, and where strokes cross, since the widths there are carried
over from the stroke's other parts rather than measured.

Effective State of the base, 2026-10-31: executed 2026-10-30; Ben has checked the readings of
the two crops on page F043A, and those of the two on page F102A await his review.
