# The first pen-stroke exemplars, 2026-10-30: update

State: open; first entries 2026-10-31

## Ben's review of the two crops on page F043A, 2026-10-31

Ben checked the readings of the marks in the two crops on page F043A. The two on page F102A
awaited his review until his second review, below. His answers are quoted from the review
session's chat.

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

On 2026-10-31 the stroke-SVGs moved to profile 2 of
[pen-stroke-representation.md](pen-stroke-representation.md), which profile 3, below, extends.
Each stroke's median is one or a
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

## Ben's second review, of page F102A's על־פני, 2026-10-31

Ben's words below are from his message of 2026-10-31 to the commander session "Commander for
Claude's forests", which quoted them into the brief of the session that applied them.

1. **Under the nun of F102A's על־פני, the bar is the pataḥ, written late, and the qamats is
   all but lost.** The base's item 3 reads: "Under the nun there are one short bar and one
   vertical stroke beginning at the bar's right end, and no dot." Ben: "there is only the
   faintest remnants of where I think a qamats was. Mainly this qamats is (very implicitly)
   indicated by the space under the nun that "pushes off" the patax to be "late"." So the short
   bar, s12, is the עליון strand's pataḥ alone, left of the space where the תחתון strand's
   qamats stood. The stroke-SVG now supplies that qamats as s30 and s31, a bar and a tick, over
   faint traces right of the pataḥ, under decision 15 of the schema note. The base's "The
   stroke-SVG puts the vertical stroke in a qamats group and in a silluq group" no longer holds:
   the vertical stroke, s13, is in the silluq group alone. Whether it is instead the top of a
   stroke of the next line's lamed is a question put to Ben.
2. **Ben judged the strokes of that crop's letters poor, except the lamed's and the yod's.**
   Ben: "Overall, for Page F102A, column 3, line 23: Deuteronomy 5:7, the strokes model did a
   pretty poor job for all letters except lamed and yod." So the ayin's, the pe's and the nun's
   strokes do not yet model their ink. He asked whether an alternative or additional approach
   would do better: "to have a model of what strokes are involved in creating an idealized
   version of this letter, and then stretch and tweak the parameters of that model to try to
   fit to the ink that is there and the ink that is implied (that's the trickiest part, I
   imagine) but flaked off areas!" No approach has been chosen.
3. **Profile 3 adds supplied strokes, for that qamats.** A supplied stroke is one the crop
   shows little or no ink of, and every view draws it in one style reserved for it. In F102A's
   על־פני the ink no stroke explains fell from 11.8% to 11.6%, the supplied bar covering the
   faint traces, and the sweep beyond the ink stayed at 12.3%, since a supplied stroke's sweep
   is not counted there. The other three crops' figures did not change.

## Round 3: two well-kept lines, 2026-10-31

Ben settled the round's questions on 2026-10-31; the schema note's decisions 15 to 17 quote his
answers about the strokes. Asked "Which easy case should the fresh session start with?", he
answered "Manuscript lines"; asked "Shall the fresh session trace F043A column 2 line 4 and
F102A column 2 line 2?", he answered "Yes, those two".

1. **Profile 4.** No end of a letter's stroke is round, and every head is a short stroke of its
   own (decision 16); every group says whose ink it is, and other words' and lines' ink is drawn
   in slate grey (decision 17); and a file may propose its ductus, the order and direction of
   its strokes. The schema note describes the profile and how the four QUPO crops were moved to
   it. Their heads are not yet strokes of their own.
2. **Two crops of whole lines**, page F043A's column 2, line 4, of Exodus 19:23, and page
   F102A's column 2, line 2, of Deuteronomy 4:42, have 123 and 105 strokes. Claude placed every
   stroke by eye, in the order and direction it proposes them written: all the letters, right
   to left, then all the marks. Each head is its own stroke, nineteen in the first line, and
   each begins at the pointed tip where the pen's corner first touched. A script of Claude's
   fitted the curves and widths and cut each end of a letter's stroke along an edge of the
   stiff nib that `nibfit` measures in the crop's letters: 12.7 pixels wide with its long edge at
   71° in F043A's line, 14.2 pixels at 80° in F102A's. The lines above and below are slate:
   the feet and vowels of line 3 and the accents over line 5 in the first crop, the feet and
   vowels of line 1 in the second. Line 3's letters reach into the second only as specks.
3. **Ink that no transcription records.** On page F043A a small ring stands over the atom
   לעלת, and on page F102A another over the atom האל. Claude takes both for circelli, the small
   circles that point to notes in the margin, and gave them the kind "masora circle mark". On
   page F043A a blot over the atom הר may be a third. On page F102A a small dot stands between
   the foot of the diagonal of the alef of the atom אחת and its pataḥ. These are questions for
   Ben.
4. **The pen residual of all six crops under profile 4:**

   | Crop | Strokes | Ink no stroke explains | Sweep beyond the ink |
   | --- | --- | --- | --- |
   | F043A פני | 13 | 6.7% | 13.4% |
   | F043A מתחת | 26 | 9.4% | 9.1% |
   | F043A, line 4 | 123 | 17.9% | 16.0% |
   | F102A, line 2 | 105 | 17.9% | 14.2% |
   | F102A על־פני | 31 | 14.2% | 13.6% |
   | F102A מתחת | 26 | 14.9% | 15.9% |

   In each of the four QUPO crops the ink no stroke explains rose under profile 4; under
   profile 3 it was 5.8% to 13.1%. A cut along the pen's edge follows a stroke's end less
   closely than a fitted round end did. In the two lines most of it is thin slivers along strokes' edges, where
   a stroke stands about a pixel off its ink, and the corners where strokes meet. A head's
   width is the stiff nib's, since the ink across a head cannot be measured apart from the
   stroke it joins.

Effective State of the base, 2026-10-31: executed 2026-10-30; Ben has checked the readings of
the two crops on page F043A and of the vowels under the nun of F102A's על־פני, and the rest of
the two crops on page F102A awaits his review, as do the two crops of whole lines that round 3
added.
