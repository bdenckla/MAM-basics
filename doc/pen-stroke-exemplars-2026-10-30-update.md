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

Effective State of the base, 2026-11-01: executed 2026-10-30; Ben has checked the readings of
the two crops on page F043A and of the vowels under the nun of F102A's על־פני, and the rest of
the two crops on page F102A awaits his review. Of the two crops of whole lines that round 3
added, Ben answered round 3's nine questions on 2026-10-31; the rest of their readings has had
no human review. Ben judged round 5's refit of their letters under profile 5 an incremental
improvement on a fundamentally flawed approach on 2026-11-01, and how to work up from level 1
instead is under discussion.
