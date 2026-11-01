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
ends to the ink. The schema note's "Profiles 1 to 5" gives its steps. The base's
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

## Round 4: bases written as strokes of their own, 2026-10-31

1. **Decision 18 of the schema note.** Asked "Re-trace the bases and the mem's left stroke as
   figure 247 draws them?", Ben answered "Yes, as figure 247": figure 247 of Ada Yardeni's *The
   Book of Hebrew Script*, an exercise in drawing the parts of the letters in the 10th-century
   Eastern book-hand. In page F043A's line 4, the bases of the kaf of the atom יוכל and of the
   final mem of the atom העם, and the foot of the tav of the atom לעלת, are now strokes of their
   own, written after the strokes they meet, from left to right; round 3 drew each leftward as
   the end of a stroke turning the letter's corners. In page F102A's line 2 the same holds for
   the base of the mem of the atom מן, the base of the final mem of the atom הערים and the foot
   of the tav of the atom אחת, and that mem's left stroke now runs upward to the right. Each line
   has three strokes more, so every later stroke's id is higher than in round 3.
2. **The pen residual of the two lines,** with round 3's figures in parentheses:

   | Crop | Strokes | Ink no stroke explains | Sweep beyond the ink |
   | --- | --- | --- | --- |
   | F043A, line 4 | 126 (123) | 17.8% (17.9%) | 15.4% (16.0%) |
   | F102A, line 2 | 108 (105) | 17.3% (17.9%) | 14.2% (14.2%) |

   Both moved little: the change is chiefly to the order and direction in which the line is
   proposed to have been written, not to how closely its strokes model the ink.
3. **The alef's upper-left upright, decision 19.** Asked "Make each alef's upper-left upright a
   short stroke of its own?", Ben answered "Yes, own stroke", in the spirit of modelling the
   Leningrad Codex's script, which may differ in small ways from the hand Yardeni describes.
   Each of the four alefs of the two lines now has its upright as a short stroke of its own,
   written downward after the diagonal and before the left leg. Round 3 drew it as the top of
   the left leg in page F043A's line and as the top of the diagonal in page F102A's. In the
   second line each diagonal's start, cut along the pen's edge, still reaches up beside the
   upright, so the two overlap; making those diagonals start lower left more ink unexplained
   and swept more beyond it.
4. **Ends stay strict for now, decision 20.** Every end of a letter's stroke is still cut along
   an edge of the crop's one pen, so this changed no file.
5. **The ring and the blot of page F043A's line 4 are masora circles of that line,** as Ben
   reads them (decision 21), and their groups' notes now say so. Round 3's item 3, above,
   asked this. Where the top of the lamed of that line's atom לא meets line 3's qamats, Ben
   judged round 3's split right: "what you did with that tricky lamed-qamats collision seems
   right."
6. **The chanted word אל־הר of page F043A's line 4 has its maqaf.** Round 3 saw none there and
   took the lamed's body to run straight into the he's roof. Ben: "there is a maqaf in both
   places", the other being in the chanted word לא־יוכל, and of this one, what runs into the he
   "is nowhere near as thick as the lamed's body (i'd say it is only about half as thick)". The
   lamed's body now starts at its ascender, and a maqaf of its own joins it to the he's roof.
7. **The curl over line 5's chanted word כי־אתה and the ring over its atom העדתה are masora
   circles,** Ben: "those are both masorah circles". Nearly every masora circle stands above
   its own line's letters, he added, so these are line 5's (decision 21). Round 3 had left both
   unidentified. Their groups now have that kind and say so.
8. **The pen residual after decision 19 and that maqaf,** with the figures after decision 18 in
   parentheses:

   | Crop | Strokes | Ink no stroke explains | Sweep beyond the ink |
   | --- | --- | --- | --- |
   | F043A, line 4 | 129 (126) | 17.6% (17.8%) | 15.3% (15.4%) |
   | F102A, line 2 | 110 (108) | 16.6% (17.3%) | 14.5% (14.2%) |
9. **The ring over the atom האל of page F102A's line 2 is a masora circle of that line.** Ben:
   "that's an MC above alef, i.e. a normal above-MC". The file already had it so, and its
   group's note now says so.
10. **The dot by that line's first alef is likely stray ink,** decision 22. Its group's kind is
    now "stray mark", and its note gives Ben's best guess and the mapiq he did not rule out.
11. **The order of the writing.** Asked whether the order each line proposes looks plausible,
    and which strokes look written the wrong way round, Ben answered: "I have no opinion as to
    plausibility, but what you did seems fine". With that, round 3's nine questions are all
    answered.

## Round 5: the letters swept by one pen, 2026-11-01

After round 4 Ben judged the two lines' letters: "Overall, as far as letters, i've got to say,
we are not doing great, for instance as measured by "ink no stroke explains" and "sweep beyond
the ink" (we might think of these as false negatives and false posities)." And: "But also as
helpful as those two diagnostics are, the writing just looks scrappy/wrong." Asked "Which should
the next round build first?", he answered "Pen first, then letters". Round 5 built the pen, to a
design of Claude's that Ben has not yet reviewed.

1. **Profile 5 of the schema note.** In the two crops of whole lines every stroke of the letters
   is now the crop's nib, a rectangle, carried along its median without turning, so that its
   thickness comes from its direction alone and its ends are the nib's own edges. Round 4's
   widths had been fitted to the ink measured across each stroke, so they followed flaking, the
   threshold's edges and the places where strokes overlap. The four QUPO crops moved to profile
   5 by their profile string alone and keep their strokes' widths.
2. **The fit.** A script of Claude's moved each median to lower the ink no stroke explains plus
   the sweep beyond the ink, weighed alike; the schema note's "Profiles 1 to 5" gives its steps.
   Two of its bounds were found by trial. With every point within 3 pixels of round 4's medians,
   the ink no stroke explains stayed near 9% and the sweep beyond the ink near 11%: the medians
   could not reach ink that round 4 had traced a few pixels off, such as the left side of the
   final mem of page F102A's atom הערים. Every point may now move 5 pixels. And with no floor
   on how far a stroke may shrink, strokes that a head or a roof overlaps shrank almost to
   nothing, among them the ascender of the second lamed of page F043A's atom לעלת and the left
   leg of the tav of page F102A's atom אחת, since ink that another stroke covers is worth nothing
   to a stroke. No segment or median now shrinks below 60% of its length.
3. **The nib.** Each crop's nib for the letters started from `nibfit`'s and was refined by a
   coordinate search round it, in steps of 1 pixel of width, 0.5 pixel of edge and 4°, then half
   those, the medians fitted again from round 4's at each trial nib. Both nibs grew half a pixel
   wider and thinner at the edge. With `nibfit`'s nib the same fit had left 5.7% of the ink
   unexplained and swept 8.4% beyond it in page F043A's line, and 6.1% and 8.2% in page F102A's.

   | Crop | `nibfit`'s nib | Chosen nib | How far it moved |
   | --- | --- | --- | --- |
   | F043A, line 4 | 12.71 × 3.15 pixels at 71° | 13.21 × 2.15 pixels at 73° | width +0.5, edge −1, angle +2° |
   | F102A, line 2 | 14.18 × 4.63 pixels at 80° | 14.68 × 3.88 pixels at 80° | width +0.5, edge −0.75, angle 0° |

4. **The marks keep their widths.** Swept by a nib for the marks that `nibfit` fitted to each
   line's marks, 4.98 by 4.25 pixels at 97.5° in page F043A's line and 5.47 by 3.25 at 90° in
   page F102A's, the lines fitted worse than with the marks' own widths: by the overlay page's
   count, 70 pixels more of the two figures together in the first and 165 more in the second.
5. **The pen residual,** with round 4's figures in parentheses:

   | Crop | Strokes | Ink no stroke explains | Sweep beyond the ink |
   | --- | --- | --- | --- |
   | F043A, line 4 | 129 | 6.8% (17.6%) | 6.6% (15.3%) |
   | F102A, line 2 | 110 | 6.5% (16.6%) | 7.3% (14.5%) |

6. **Where the one pen still misses.** In page F043A's line the six strokes that end in a tail,
   the five lameds' bodies and a yod's, leave 259 pixels of ink unexplained near them, almost as
   many as the line's nineteen heads leave (294). A tail tapers to a point thinner than the nib
   sweeps there, so its stroke stops short of the tip. Modern Torah-scroll practice draws such
   fine lines with the nib's corner, pulling wet ink out of the stroke, as Jen Taylor Friedman's
   Beit Yosef practice sheet teaches; whether the Leningrad Codex's scribe did is unknown. The
   marks, which keep their fitted widths, carry 450 of the line's 1,565 pixels swept beyond the
   ink. Page F102A's line shows the same less strongly: 77 pixels near its three tails, and 228
   of its 1,726 beyond the ink at the marks.
7. **What strictness costs, decision 20's measurement.** Ben, asked whether every end should keep
   to one pen per crop: "we'll have to gain some experience of what the error-penalty is for
   being strict about sticking to the nib model at stroke ends vs what would be gained allowing
   the "angle [to] be free to follow the ink"." Each freedom below was measured alone from the
   strict fit, every point keeping the strict fit's reach; none is adopted, and decision 20's
   strictness stands until Ben decides. Each pair is the ink no stroke explains and the sweep
   beyond the ink.

   | Crop | Strict | Each end's cut free | Each stroke's own nib angle | Each stroke's own scale of the nib's width |
   | --- | --- | --- | --- | --- |
   | F043A, line 4 | 6.8%, 6.6% | 7.0%, 5.3% | 6.6%, 5.9% | 6.0%, 5.9% |
   | F102A, line 2 | 6.5%, 7.3% | 6.5%, 5.7% | 6.2%, 6.2% | 6.0%, 6.2% |

   A free end is cut by a straight line at an angle and an offset of its own, at least 15° from
   the median; an own angle keeps within 20° of the crop's; an own scale is from 0.75 to 1.25.
   Each freedom cuts the two figures' sum by 8% to 12%, free ends mostly the sweep beyond the
   ink. The strokes' own angles centre on the crop's, most within 8° of it, and their own scales
   on 1, most between 0.76 and 1.08. A nib held at an angle of its own for a
   stroke is what the Beit Yosef sheet's tilted vav asks for; turning it during a stroke, the
   sheet's wedge, was not measured.

## Ben's review of round 5, 2026-11-01

Ben's words below are from his message of 2026-11-01 to the session that took over from round 5
to discuss its results.

1. **Round 5 is an incremental improvement on a flawed approach.** Ben: "my basic message is
   that round 5 seems like incremental improvements on a fundamentally-flawed system." He cited
   the tav of the atom אחת of page F102A's line 2, whose ink is clean: "Image-wise, it seems a
   fine signal (no flaking, good image quality, etc.). But stroke-matching is comically bad. If
   we can't get that tav right, we have no hope for this approach". He declined to choose among
   round 5's three freedoms, which would mean distinguishing "fine variations in "how
   terrible", which I decline to do based on pointlessness." So no freedom is adopted, and
   decision 20's strictness stands.
2. **What went wrong in that tav.** Ben named two places a flaw may lie: "the nib model (writing
   instrument model) is flawed", whether "too restrictive, too permissive" or otherwise, and
   "the fitting procedure is flawed", whether by "following noise, failing to follow signal" or
   otherwise. The tav shows both. Its four strokes are a head, the roof running into the right
   leg, the left leg, and the foot, written from left to right (decision 18). In round 4 the
   left leg's median, placed by eye, stood about 10 pixels left of the middle of its ink, which
   is 6 to 8 pixels wide, so that only 15% of its sweep lay on ink. Round 5's fit lets each
   point move at most 5 pixels from round 4's median, and it moves one point, or one smooth
   join, at a time, never a whole stroke; it moved the leg about 2 pixels, and 32% of its sweep
   now lies on ink. Most of the leg's ink is unexplained, and most of its stroke covers
   paper. A fit that only polishes medians placed by eye keeps a gross error in their placement.
   The rigid nib, for its part, cannot make the ink's sharp tips, the head's peak and the
   foot's point: it sweeps the foot as a broad band with blunt ends. And where the ink runs the
   leg into the foot in one curve, the strokes are two.
3. **Letter models.** Of phase B, letter models fitted to the ink, Ben wrote: "perhaps worth a
   try but i'm pessimistic." It has not begun.
4. **A direction Ben finds more promising.** Ben: "I think a more promising direction is to try
   to work up from a lower level ink-fill model (didn't we used to have that as level 1?)".
   Level 1, the ink as filled outlines that potrace traces, is still in every stroke-SVG, and in
   the tav it follows the ink closely, tips and all. How to work up from it is under discussion.
5. **The photograph is no longer drawn as squares of pixels.** Ben: "btw what is "the page's
   pixels as squares"? whatever it is, it seems useless; please get rid of it but tell me what it
   was". It was a checkbox beside each image, on round 5's sheet and, as "the crop's pixels as
   squares", on the overlay page, which drew the photograph with each pixel enlarged as a
   hard-edged square instead of smoothly. Both pages no longer have it.

## Regions of ink: the six crops' drafts, 2026-11-01

Asked "Adopt regions of ink in place of strokes, freezing the stroke files as a record?", Ben
answered "Yes, regions": decision 23 of
[ink-region-representation.md](ink-region-representation.md), the profile of the new
region-SVGs, which [PLAN-ink-regions.md](PLAN-ink-regions.md) built. The six stroke-SVGs and
`overlays.html` are now a frozen record of the pen-stroke work.

1. **Six region-SVGs, as drafts.** A script of Claude's wrote each crop's region-SVG from its
   stroke-SVG, and the snips README gives its steps. Each region-SVG's level 1 is its
   stroke-SVG's, derived again and found identical. Its regions are drawn from the strokes: a
   cut runs where the ink that one group's strokes reach meets the ink that another's reach,
   and no one has checked a cut against the image.
2. **The figures,** for files that `regions-check` passes with no problem. A piece of ink is a
   4-connected piece of the ink as level 1 judges it, at 3 samples a pixel: a fill, or a residual
   piece judged ink that lies outside the fills. Labels are the groups whose strokes reach it.

   | Crop | Pieces of ink | With several labels | Cut | Cuts | Regions | Regions in two groups or more |
   | --- | --- | --- | --- | --- | --- | --- |
   | F043A פני | 8 | 2 | 1 | 10 | 14 | 3 |
   | F043A מתחת | 15 | 3 | 2 | 3 | 18 | 0 |
   | F043A, line 4 | 76 | 12 | 11 | 38 | 101 | 11 |
   | F102A, line 2 | 75 | 6 | 4 | 17 | 84 | 4 |
   | F102A על־פני | 33 | 10 | 5 | 15 | 46 | 3 |
   | F102A מתחת | 29 | 5 | 2 | 3 | 32 | 1 |

   A piece with several labels kept only one where every other label's part was smaller than 4
   pixels and joined its neighbour, as 13 did.
3. **The census.** `r6_region_census.py`, rerun on the stroke-SVGs at `cc1e7ddd`, gives the
   plan's table unchanged: 25 fills hold more than one group's ink. The drafts cut 25 pieces,
   as many in each crop, though not always the same ones, since the census counts a group in a
   fill from 4 pixels of ink that its strokes cover or come within 3 pixels of, and the drafts
   count a label's parts.
4. **Ink that no stroke reaches within 12 pixels** got groups of its own, of the kind
   "unidentified letter", in four places. At the foot of page F043A's מתחת, the top of a letter
   of line 23, which touches the atnaḥ over it, as Claude read the page image; its crop had no
   text of the line below, and its region-SVG now gives as that text the atom under the crop,
   the last of Exodus 20:4, copied by script from round 3's extract of the UXLC. At the top edge
   of page F043A's line 4,
   the foot of a letter of line 3, and at the foot of page F102A's line 2, the tops of four
   letters of line 3: specks the tracer dropped and Claude judged ink. A speck at the top edge
   of page F102A's על־פני, 12.3 pixels from a mark of the line above, joined that mark's group.
5. **Restoration candidates.** The four residual pieces judged damage are all in page F102A's
   מתחת, each a pale spot that the tracer filled, inside a fill: r3, 7 pixels, at x 99 to 101
   and y 47 to 49 of the crop; r7, 4 pixels, at x 93 to 94 and y 66 to 67; r10, 2 pixels, at
   x 63 and y 106 to 107; and r11, 3 pixels, at x 104 to 106 and y 114. Their ink is left out of
   the regions, so that restored ink could fill them. No restoration has been added; each awaits
   Ben's word.
6. **Supplied ink.** The bar and the tick of the qamats under the nun of page F102A's על־פני,
   strokes s30 and s31, are now supplied ink, each outline the outline of its stroke's ink.

Effective State of the base, 2026-11-01: executed 2026-10-30; Ben has checked the readings of
the two crops on page F043A and of the vowels under the nun of F102A's על־פני, and the rest of
the two crops on page F102A awaits his review. Of the two crops of whole lines that round 3
added, Ben answered round 3's nine questions on 2026-10-31; the rest of their readings has had
no human review. Ben judged round 5's refit of their letters under profile 5 an incremental
improvement on a fundamentally flawed approach on 2026-11-01, and chose regions of ink in place
of strokes the same day. The stroke-SVGs are a frozen record since then, and the six crops'
region-SVGs, drafted by script from the strokes, await his review.

## Ben's first answers on the regions, 2026-11-01

Ben's words below are from his messages of 2026-11-01 to the session that took over the
discussion of the regions and phase 4 of [PLAN-ink-regions.md](PLAN-ink-regions.md). Both concern
question 1 of phase 3's sheet: the piece of ink of page F043A's פני that holds the pe, the nun and
the vowels under the nun.

1. **The pe and the nun do not touch.** Ben: "My perception is that the פ and נ of Ex20v2-PNY do
   not intersect and thus there is no need for (or should not be a need for) a cut". He sees "a
   thin strip of vellum" between them, which level 1's fill covers. He drew a cut along it, now
   the region-SVG's c11, in place of the draft's cuts c7, c8 and c9 and its region rg6, which was
   in both letters' groups. The ink on either side of c11 is now one letter's alone.
2. **The strip is paler than the strokes but darker than the threshold.** Across the strip, at
   four places along Ben's cut, the crop's luminance falls to 35 to 50 in the strokes on either
   side and rises to a ridge of 114, 125, 138 and 164 between them, against the crop's threshold
   of 142. So the threshold leaves the strip ink along most of its length, and the two letters
   one piece of ink. A strip of vellum narrower than the photograph's blur can join letters that
   do not touch, so other pieces of ink that hold two letters may be joined in the same way. Ben
   proposed "a very thin "supplied vellum" (as opposed to "supplied ink") shape" for such a
   place, which would take the strip out of the ink so that the letters stand apart even in black
   on white. Whether the profile gains it awaits his decision.
3. **The qamats under the nun: a dot and a bar that only touch.** Ben: "The nun's qamats should
   have a separate qamats dot from its patax-like bar above it. I would code them as touching only
   in that the bar touches the dot below it as a tangent to a circle touches a circle. I.e., I
   don't even think this should be coded as an overlap". The dot is now a region of its own,
   rg15, in the qamats's group, cut from the bar by c12, which runs along the bar's lower edge,
   where the ink below it narrows towards the dot.
4. **The shapes of the draft's overlaps.** Ben: "I would have expected those shapes to simply be
   the intersection of reasonable shapes for the two (so far I've only seen a two-way
   intersection!) marks in question. Instead, the two marks in question seem to end awkwardly and
   there's a "pebble" sort of wedged in between them that doesn't fill the space between them,
   i.e. there's whitespace!" The pebbles come from how the draft cut a piece of ink where three
   labels met, one group's, the other's and both: its script ended the cuts at one point inside
   the ink, so the shared part is a wedge in the middle of the junction, and the two marks still
   touch above and below it. The white space is the drawing's rather than the regions': the sheet
   drew each cut over a white band 4 screen pixels wide, as the region page did, while the
   regions leave little ink uncovered beside the cuts, 2.2 pixels in this crop and 33 in all six.
   The region page now draws each cut as one thin pink line. An overlap that is the intersection
   of two shapes fits the profile as two cuts, each running across the junction from edge to
   edge where one mark's shape ends, with the part between them in both groups.
5. **Supplied ink in colour alone,** decision 26 of
   [ink-region-representation.md](ink-region-representation.md), from Ben's comment on the design
   choices: "I don't think we want to use stipple, bars, dotted outlines, or anything else other
   than color, for now at least."

Effective State of the base, 2026-11-01: as the previous entry gives it, except that Ben has begun
to review the region-SVGs, with question 1 of phase 3's sheet.

## Regions of ink re-drafted by rule, 2026-11-01

Asked "Approve the re-draft plan as written?", Ben answered "Approve the plan": decision 27 of
[ink-region-representation.md](ink-region-representation.md), whose profile 2 the six
region-SVGs now follow. A script of Claude's re-drafted each from its profile-1 draft, as the
snips README says: it kept level 1, the groups and the supplied ink, dropped the draft's cuts and
its regions in two groups, kept the seeds of its regions in one group, and added the seeds,
overlaps, strips and cuts that the list below gives. A watershed on the photograph's luminance
draws every region from its seeds.

1. **The figures,** for files that `regions-check` passes with no problem. A piece of ink here
   is a 4-connected piece of the ink as level 1 judges it, at 3 samples a pixel, less the strips
   of vellum and the cuts.

   | Crop | Pieces of ink | Seeds | Regions | Overlaps | Strips of vellum | Cuts | Restoration candidates |
   | --- | --- | --- | --- | --- | --- | --- | --- |
   | F043A פני | 10 | 13 | 11 | 0 | 1 | 1 | 0 |
   | F043A מתחת | 17 | 27 | 19 | 1 | 1 | 1 | 0 |
   | F043A, line 4 | 79 | 112 | 91 | 0 | 3 | 0 | 0 |
   | F102A, line 2 | 76 | 84 | 80 | 0 | 1 | 0 | 0 |
   | F102A על־פני | 37 | 51 | 28 | 0 | 4 | 0 | 0 |
   | F102A מתחת | 29 | 33 | 18 | 0 | 0 | 0 | 5 |

   The seeds lent to a letter, or to a sign of one written part, joined as one region, so a crop
   of mostly letters, such as F102A's על־פני, has far fewer regions than its draft's 46.
2. **The watershed on Ben's two lines.** In the crop of page F043A's פני, with Ben's strip v1,
   the draft's cut c11, and the cut c12 left out, the watershed's boundary between the nun and
   the pe lies at most 0.44 pixels from v1's line, median 0.10, over 24 pairs of samples, and
   its boundary between the qamats's bar and its dot at most 1.16 pixels from c12, median 0.50,
   over 14 pairs: within the 1.5 pixels that phase 6 required, and the figures that the plan's
   prototype found (its Evidence, item 4).
3. **Ben's readings, carried over.** In page F043A's פני, Ben's c11 is now the strip of vellum
   v1, along the same line, and Claude's c12 stays a cut. In page F043A's מתחת, the qamats's dot
   has a region of its own; the geresh keeps its region, and the script proposes a strip of
   vellum between it and the tav; and the lamed of line 23 has a group of its own, g18, with
   an overlap, ov1, where its tip crosses the base of the mem.
4. **Which ink is the lamed's.** The plan took the group g17 for the lamed's "barbed spear tip".
   On the page image, the piece at the crop's foot that g17 holds is the top of the alef's
   diagonal, the next letter of line 23's atom, and the lamed's ascender is the stroke under the
   mem's base, which the draft gave to the mem and which runs out of the crop's foot into line
   23's lamed. So g17 is now that alef, holding also the sliver that the draft gave the atnaḥ
   (phase 3's sheet, question 3), and the new g18 is the lamed. The watershed cannot divide the
   dark ink that the mem's base and the lamed's tip share, so a cut of Claude's, c4, runs along
   the foot of ov1: above it the mem's base, below it the ascender. Claude drew ov1 by eye, and
   it awaits Ben's review.
5. **Seeds Claude added,** each placed by eye on the photograph with the transcription in hand,
   where the watershed from the draft's seeds gave a written part's ink to another sign, or
   where a written part had no seed:

   | Crop | Sign | Seeds | Why |
   | --- | --- | --- | --- |
   | F043A פני | the pe | 1, in its base | the qamats's bar took the base, past a paler stretch of the pe's stroke |
   | F043A מתחת | the qamats under the tav | 2 for the bar, in place of the draft's 1, and 1 for its dot | the dot is a written part; the draft's seed lay at the neck between them |
   | F043A מתחת | the mem | 3, in its roof and its base, in place of the draft's 1 | the draft's seed lay where the lamed crosses the base |
   | F043A מתחת | line 23's lamed | 5, along its ascender and in the barb of its tip | a new group |
   | F043A, line 4 | the he of הר | 3, in its roof's right end, its corner and its right leg | the maqaf took the leg |
   | F043A, line 4 | the maqaf after אל | its 1 seed moved to its middle | its seed lay against the he's corner |
   | F043A, line 4 | the first lamed of לעלת | 3, in its ascender and its flag | the base of line 3's shin, which its tip meets, took the ascender |
   | F043A, line 4 | the final mem of העם | 4, in its sides, its base and its corner | the ayin, which meets that corner, took all but the roof |
   | F043A, line 4 | the lamed of לא | 3, along its ascender | the ḥolam, and line 3's qamats, took the ascender |
   | F043A, line 4 | line 3's two qamatses | for each, 2 or 5 for the bar, in place of the draft's 1, and 1 for its dot | the dot is a written part, and the bar under the vav of the first divine name lost its middle to the lamed of לא |
   | F043A, line 4 | line 3's vav foot, g20, and sheva, g40 | 1 for the foot, and 1 for each of the sheva's dots | the foot's only region was in two groups; level 1 joins the sheva's dots |
   | F102A, line 2 | line 1's munaḥ | 1, in its upright | the foot it hangs from took the upright |
   | F102A, line 2 | line 1's segol, g42 | 1, for its lower dot | level 1 joins it to the upper left dot |
   | F102A, line 2 | the qamats under the vav of וחי | 2 for the bar, in place of the draft's 1, and 1 for its dot | the dot is a written part |
   | F102A על־פני | the pe | 4, in its base and its right side | the dagesh took them |
   | F102A על־פני | the nun | 3, in its vertical and its base | the yod, whose long tail meets the base, took them |
   | F102A על־פני | the yod | 1, in its tail | near where it meets the nun's base |
   | F102A מתחת | the qamats under the tav | 2 for the bar, in place of the draft's 1, and 1 for its dot | the dot is a written part |

   The input file beside the script, `r7_redraft_input.json`, gives every seed's place, and the
   records under `.novc/pen-stroke-exemplars/regions/redraft-<crop>.json` what the script did.
6. **Strips of vellum proposed by the script,** where the median luminance of the paler sample
   of each pair across the boundary between two signs' regions is at least a third of the way
   from the crop's median of ink to its median elsewhere, 101 to 113 in these crops: 9 strips.
   Between the geresh and the tav of page F043A's מתחת, median 129; in line 4, between line 3's
   alef and a lamed's tip, 128, between a foot of line 3's he and its qamats's bar, 115, and
   between a segol of line 3 and the mem above it, 125; in line 2, between line 1's alef and the
   lamed's head, 132; and in page F102A's על־פני, between the maqaf and the pe, 104, between the
   nun and the yod's tail, 105, and two between pieces of the next line's letters, 109 and 143.
   One proposal was set aside: in page F102A's מתחת, a strip between the qamats and the small
   mark g14 would have taken out most of g14's ink, leaving it without a seed.
7. **Restoration candidates,** listed for Ben and not added: all five are in page F102A's מתחת,
   the four residual pieces judged damage, each a hole whose neighbouring ink is one sign's, and
   one hole of 19.6 pixels in the left leg of the tav, at x 93 to 97 and y 71 to 78 of the crop.
   No other crop has a hole of 30 pixels or fewer whose neighbouring ink is all one sign's.

Effective State of the base, 2026-11-01: as the previous entry gives it, except that the six
region-SVGs are re-drafted under profile 2 and await Ben's review, on phase 6's sheet.
