# The pen-stroke representation of a manuscript crop

State: live; the profile of the stroke-SVGs in `doc/pen-stroke-snips/`: profile 1 implemented on 2026-10-30, profiles 2 to 4 on 2026-10-31

A crop of a manuscript page can be shown as pixels and read as a Unicode transcription. The
pen-stroke representation sits between them. It describes the crop's ink as filled outlines,
then as strokes of a pen, then as groups of strokes that a reader would call a letter, a vowel
or an accent. It is kept as a **stroke-SVG**, `<crop>.strokes.svg`, beside each crop in
`doc/pen-stroke-snips/`. That directory's `README.md` gives each crop's provenance, and
[pen-stroke-exemplars-2026-10-30.md](pen-stroke-exemplars-2026-10-30.md) reports what the first
four crops showed. [pen-stroke-sources.md](pen-stroke-sources.md) lists the books, articles and
PDFs that the work's research has cited.

## Ben's decisions

The first twelve are of 2026-10-30, and decisions 13 to 21 of 2026-10-31. The first nine
were made in the planning session "Investigate a pen-stroke manuscript representation", whose
plan was not committed, so this list is their record here. Decisions 11 to 15 were made while
Ben reviewed the first exemplars, decisions 16 and 17 as he settled the third round of
tracing, on two well-kept lines, and decisions 18 to 21 in the fourth round.

1. **The unit is one crop, not a page.** Ben: "This is not about whole manuscripts or even whole
   pages. At least not yet." No page, column or line geometry is in scope, and no
   image-processing pipeline is to be built unless hand-made exemplars show that the level pays.
2. **Strokes are calligraphic.** A stroke's ink is the sweep of a broad nib, so its thickness
   varies with its direction. Ben asked whether the design included "the fact that the stroke
   (in letters; less frequently in diacritic mark) is width-modulated by nib angle".
3. **A nib-model, and excursions from it, which are information.** Ben: "if they occur
   frequently when modelling well preserved sections of the text (as opposed to horrific
   re-inkings), then perhaps we have some problem with our model, or with the base image data".
4. **Linking to a transcription is premature; stroke groups come first.** Groups have a kind
   congruent to a code point, such as "alef letter" or "zarqa accent", and no link to any
   transcription's coordinates.
5. **A bar is a bar at the lowest level.** Frames of reference, which make a bar horizontal or
   vertical, belong to a higher level.
6. **Filled Bézier outlines with residuals come first, then pen strokes.** The image residual
   and the pen residual are different things.
7. **Two nibs per crop:** one for the letters and one for the marks.
8. **The first crops are the Decalogue's QUPO words**, cut afresh in color. QUPO is Ben's
   shorthand for a dual-cantillation atom with a qamats and an accent under a letter in one
   strand, and a pataḥ and an accent over the same letter in the other.
9. **The medium is SVG with a lint,** and the ladder of levels below stands as written.
10. **Execution** (Ben accepted all four recommendations together): Claude downloaded two page
    images from Sefaria and one from the Internet Archive to compare them; potracer became a
    dependency; the files live in `doc/pen-stroke-snips/` with this note in `doc/`; and Claude,
    not Ben, traced the strokes.
11. **The levels transcribe the image with the text in hand; they automate nothing.** Ben:
    "What we're doing here is in no way related to automated transcription to various
    intermediate levels of abstraction (intermediate between pixels and Unicode)." And: "What
    we're doing here is we have pixels, plus a Unicode transcription plus often some remarks
    about the image, and we want to transcribe the image to intermediate levels of
    abstraction." The work does not climb the levels: "we're not working up a ladder of
    abstraction, we're working "inward" (or jumping around inside, with arbitrary feedback from
    different levels of abstraction, downward and upward) from two extremes of abstraction
    (Unicode and pixels)." Only level 1 might be made without the text: "Only perhaps the first
    level of filled beziers, that tries to describe ink, could be automated without reference to
    Unicode or the remarks." Ink that no letter or mark of the transcription accounts for is
    transcribed too. His example of such a remark is "there's an unexplained, seemingly-stray
    mark above the letter ב that I think is ink so we better transcribe it even though it is
    part of no letter or mark in the Unicode transcription". He framed the task three more ways
    the same day:
    1. **The unaged page.** The strokes say "here's what I think the image would look like, if
       it hadn't aged at all and was written on a perfectly clean, white surface". Colour stays
       the other view: "But also color to show different strokes is an important view still,
       just to be clear."
    2. **A history of the writing.** "I.e. part of this is proposing a history of how the text
       was written, and maybe even animations showing some sort of abstract representation of
       the nib drawing it out."
    3. **A plausible history, not the real one.** The temporal aspects "just need to be a
       plausible of sequence of events"; Ben confirmed that the words before that, "need to
       correspond to reality", meant "don't need to". "Particularly with respect to overlaps, it
       doesn't really matter who is "on top" of who. But it would be sort of perverse not to
       show (1) letters before diacritics (because we strongly suspect that *is* the historical
       order of things and (2) show each pass (letter-pass, diacritic-pass) in right-to-left
       order."

    The profile records each stroke's pass, letters or marks, as `data-pass`, and the overlay
    page has a layer of the strokes in black, which with the crop switched off shows the page
    unaged. Since profile 4 a file may also propose the direction in which each stroke was
    written and its place in the writing, its ductus, which "The ductus" below describes.
12. **The nib model is calligraphic: a stroke's width may vary along its course.** Ben:
    "Absolutely a "calligraphic" nib model is needed, by which I mean one in which stroke-width
    is modulated (or can be modulated) throughout the course of a stroke. It doesn't matter what
    the physical analogy is, or how close that analogy is to the historical quill or reed or
    whatever. Width-modulation could even be done with a fine brush, for all we care (although
    line endings would probably be different with a brush)." Profile 1's stiff nib was the
    special case in which nothing varies along a stroke. In the planning session, behind
    decision 6, Ben asked for pen strokes "where the frequency (and/or other characteristics) of
    the width modulation is limited to what seems physically possible". Without a bound, a
    stroke could follow every irregularity of its ink, and the excursions that decision 3 treats
    as information would vanish. Decision 14 says what kind of bound; Ben has set no tighter
    one.
13. **The combined transcription is the primary one, and it says what to expect.** Ben: "The
    combined is the primary transcription of concern here (it should come from UXLC or, where
    I disagree with UXLC, it should come from how I tell you UXLC should be changed)." His
    reason: "sometimes the manuscript doesn't superimpose taxton and elyon the way one would
    expect." MAM's two strands stay beside it as secondary transcriptions. The combined
    transcription sets what a reader of the crop expects. Its qamats and pataḥ on F043A's nun
    made two bars there what Claude "should have taken as a given, or a near-given". It is not
    the last word: "if you only look for what you're trying to find, that will lead, in general
    to both false positives and false negatives. So the transcription is a starting place for
    what you expect to find, not the "final statement" on what you should find." Decision 4
    stands: no group is linked to a place in the transcription.
14. **A stroke is one or a few smooth curves, and its width varies smoothly along them.** Ben:
    "I don't like the way strokes are modeled as multiple connected line segments. I think they
    should be one or a few smooth curves (bezier or others, whatever) whose width is smoothly
    modulated along them (via the "time" parameter over which the curve is presumably
    parameterized)". This makes decision 12 concrete, and smoothness along one or a few curves
    is a bound of the kind decision 12 leaves open. Profile 2, below, implements it in a form
    Claude chose and Ben has not yet reviewed: each segment is a cubic Bézier curve with a width
    at each of its four points, the width at the segment's parameter t is the cubic Bernstein
    polynomial of those four, and a stroke ends round or flat; profile 4 made the ends round or
    cut (decision 16).
15. **A mark the crop shows little or no ink of can be supplied, and a supplied mark is never
    drawn as the others are.** Under the nun of page F102A's על־פני, Ben sees "only the faintest
    remnants of where I think a qamats was. Mainly this qamats is (very implicitly) indicated by
    the space under the nun that "pushes off" the patax to be "late"." He went on: "So we need a
    way to supply (clearly indicated by annotations in metadata attached to our
    stroke-transcription) marks "ex nihilo" or nearly "ex nihilo". And this would be an
    important use of color; these marks should probably *never* be displayed in a way that
    colors them the same as other marks, to avoid any suggestion that they are based on strong
    evidence. And this color use is important because if that metadata saying "this mark
    provided ex nihilo" is in a caption or something, we can't rely on the reader to pay
    attention to that." Profile 3 implements it in a form Claude chose, which Ben kept on
    2026-10-31: asked "Keep the supplied strokes hatched orange, dashed, and left out of the
    overshoot?", he answered "Keep it". A supplied stroke carries `data-supplied`, `no-ink` or
    `traces`, and `data-supplied-why`, and every view of it is hatched in an orange reserved
    for it, outlined with dashes.
16. **No end of a letter's stroke is round, and every head is a short stroke of its own.** Of
    a letter's stroke drawn ending in a disc, Ben wrote: "The diacritic-nib model should allow
    a circle, i.e. the depositing of a drop (or micro-drop) of ink, but not, I think, the
    letter-nib model." When research on how the letters are stroked had come in, he answered:
    "Adopt no round heads on letters. Adopt each head a short pen stroke." Asked "Model every
    head as its own stroke, with the pen lifted before its arm?", he answered "Yes, own
    strokes". His aim, the same day: "we just need a model that works, not necessarily a model
    that corresponds to reality." So every end of a stroke of the letters is cut, never round;
    a head is a short stroke of its own, written before the arm or stem it joins; and a mark
    may still end round. How an end is cut is Claude's design: profile 4 cuts it straight, at
    an angle the file records for each end, and round 3's fitting cut each end along an edge of
    the stiff nib that `nibfit` measures in the crop's letters, which Ben chose to keep for now
    (decision 20).
17. **Each group says whose ink it is, and other words' and lines' ink has a colour of its
    own.** Ben: "it is often important to have a Unicode transcription of the text above and
    below, in order to do a good job of determining what marks belong to what line. One of the
    values of our stroke transcription is that we can eliminate marks from the above and below
    lines. Or rather, we can show what we consider signal and what we consider noise, where
    above- and below- marks are considered noise. Or we can choose to show them, but give them
    a different color, to be "fully transparent" (in the truthfulness sense of transparent, not
    the visual!) about our decisions". Asked "Adopt the design for other lines' ink: groups say
    whose it is, own colour, hide checkbox?", he answered "Adopt it". Profile 4 implements it:
    every group's `data-ink-of`, the lines above and below on the root, and slate grey for ink
    that is not the crop's subject's, in every view, with a checkbox that hides it.
18. **A base is a stroke of its own, written from left to right, and a mem's left stroke is
    written upward.** Round 3 drew the base of a kaf, a mem or a final mem, and the foot of a
    tav, leftward, as the end of a stroke that turns the letter's corners, and the mem's left
    stroke downward. Figure 247 of Ada Yardeni's *The Book of Hebrew Script* is an exercise in
    drawing the parts of the letters in the 10th-century Eastern book-hand. Asked "Re-trace the
    bases and the mem's left stroke as figure 247 draws them?", Ben answered "Yes, as figure
    247". So where a file proposes its ductus, a base or a tav's foot is a stroke of its own,
    written after the strokes it meets, from left to right, and a mem's left stroke runs upward
    to the right. The figure teaches how to write that type of hand. It is no record of how the
    Leningrad Codex's scribe wrote, and the ductus stays a plausible proposal (decision 11).
19. **An alef's upper-left upright is a short stroke of its own.** Ben asked how round 3's
    heads lined up with where Yardeni's book expects heads. They lined up, except at the alef's
    upper left, where round 3 drew a short upright as the top of the left leg or of the
    diagonal. Asked "Make each alef's upper-left upright a short stroke of its own?", Ben
    answered "Yes, own stroke", and then: "I authorized that yes to that specific question about
    alef (though I didn't engage with the details, I admit) just in the spirit of "do what you
    need to do to develop a model of Leningrad's script, which may differ in some (probably
    small) ways from the script Yardeni describes". So each alef's upright is a stroke of its
    own, written downward after the diagonal and before the left leg. Where a diagonal's start,
    cut along the pen's edge, reaches up beside the upright, as in both alefs of page F102A's
    line 2, the two strokes overlap.
20. **For now, every end of a letter's stroke keeps to the crop's one pen.** Decision 16 left
    how an end is cut to Claude's design. Asked "Should every end keep to one pen per crop, or
    should each end's angle be free to follow the ink?", Ben answered: "I guess my (non-)answer
    is we'll have to gain some experience of what the error-penalty is for being strict about
    sticking to the nib model at stroke ends vs what would be gained allowing the "angle [to] be
    free to follow the ink". Let's start by being strict, just to choose arbitrarily". So each
    end of a letter's stroke is cut along an edge of the one stiff nib that `nibfit` measures in
    the crop's letters, as round 3's fitting cut it, and what freeing each end's angle would gain
    is still to be measured.
21. **A masora circle is transcribed and told apart from the marks that matter, and its line is
    a weak guess.** Asked whether a ring over the atom לעלת and a blot over the atom הר of page
    F043A's line 4 are circelli and that line's, Ben answered: "yeh I'd say they are masorah
    circles and the do belong to this line." He went on: "I think that luckily we're not terribly
    concerned with masorah circle ownership; though it is important to transcribe them (often to
    remove them, to get them out of the way (or color them a very light color) the main thing is
    distinguishing them from marks we consider important." And: "So, we should assign ownership
    (or have a way to leave them unassigned), but it should be understood that these assignments
    in 99 to 100% of cases won't be accompanied by much confidence because they won't be
    accompanied by much research (and as I said, sometimes even with a lot of research, the
    confidence is still low!)" Of two circles at the foot of that crop, he added: "though I have
    seen the occasional masorah circle at or near the baseline, (a) those are rare and (b) I'e
    never seen ones this low (at below-vowel level). In other words, the vast majority of MC's
    are above-marks". So a masora circle's group says whose ink it is, as every group does, and
    a circle between two lines is taken for the lower line's, above its letters. That is a weak
    guess unless the group's note gives the research behind it. Drawing the circles faintly,
    and leaving a circle's line unassigned, are not yet implemented.

## The ladder

Each level holds one kind of interpretation and is authored or derived separately. The work
does not climb the levels in order. It proceeds inward from the two ends, the crop's pixels and
a Unicode transcription, and a reading at any level may send it back to revise another
(decision 11).

| Level | What it holds | Authored or derived |
| --- | --- | --- |
| 0 crop | the pixels, with their provenance | authored |
| 1 fills | the ink as filled Bézier outlines, and the image residual | outlines derived; residual judgments authored |
| 2 strokes | a smooth median per stroke with a width varying along it and its ends' cuts, whether it is supplied, the strokes' order, and the pen residual | medians, widths, ends, order and supplied strokes authored; ink and residual derived |
| 3 shape classes | dot, bar, corner or curve, from a stroke's median and widths | derived |
| 4 frame | the baseline and the letter-body height | authored |
| 5 groups | strokes forming one sign, with a kind congruent to a code point, and whose ink it is | authored |
| 6 links | a group's place in a named, versioned transcription | parked (decision 4) |

## The file

The coordinates are the crop's pixels, x to the right and y down. Pixel (i, j) covers
[i, i + 1) × [j, j + 1), and a pixel is inside a shape when its centre is. The root's `viewBox`
is `0 0 <width> <height>`, the crop's pixel size.

**The root** carries `data-profile="pen-stroke 4"`; the provenance, as `data-manuscript`,
`data-page`, `data-column`, `data-line`, `data-line-read-by`, `data-mam-verse`,
`data-uxlc-verse`, `data-combined-chanted-word` or `data-combined-line`,
`data-combined-source`, `data-taxton-chanted-word`, `data-elyon-chanted-word`,
`data-line-above`, `data-line-below`, `data-adjacent-source`, `data-crop-note`,
`data-source-url`, `data-source-size`, `data-source-sha256`, `data-crop-box` and
`data-strokes-by`; the threshold and tracer parameters; and `data-ductus`.
`data-combined-chanted-word` is the primary transcription (decision 13) of a crop of one
chanted word, which is then the crop's subject: the chanted word with both strands' marks, as
the UXLC has it unless Ben has changed it, and `data-combined-source` says which. The two
strands' chanted words are MAM's. `data-combined-line` is the primary transcription of a crop
of a whole line, which is then the subject. `data-line-above` and `data-line-below` hold the
lines above and below as far as the crop reaches, and `data-adjacent-source` says where they
come from (decision 17).

**Level 1.** `data-channel="luminance"` is Pillow's ITU-R 601-2 luma. The ink is every pixel
whose luminance is below `data-threshold`. Potrace's pure-Python port traces the ink, with the
parameters `data-tracer` names, and drops every path of no more than `data-speck-size` pixels.
`<g class="fills">` holds one path per outline with its holes. A fill that is not ink takes a
`data-judged` attribute. `<g class="image-residual">` holds:

- one `piece` per thing a human must judge: a `speck` of ink the tracer dropped, a `hole` it
  filled, or a `faint` region, which is light but not paper-light, holds more than the speck
  size, and does not touch the ink;
- `smoothing`, the slivers where the outlines depart from the ink's pixels;
- `halo`, the pixels within `data-halo-band` of the threshold on either side.

The judgments are `ink`, `speck`, `stain`, `bleed-through`, `damage`, `noise`, `paper` and,
until someone judges, `unjudged`. The residual's paths trace pixel edges exactly.

**A stroke's width** varies along its median (decision 14). The median is one or a few cubic
Bézier segments, end to end. Each point of its path data, the start and each segment's two
control points and end, has a width, so each segment has four widths as it has four points.
At the segment's parameter t, the width is the cubic Bernstein polynomial of its four widths,
as the point is of its four points. The width is therefore smooth along each segment,
continuous where two segments meet, and never outside the range of the widths given; a
segment's two middle widths, like its control points, need not be reached. The ink is a band of
that width centred on the median. A stroke whose ends are `round` is cut square at its ends and
adds a disc of the end's width at each end and at each corner, as a round brush would. One
whose ends are `cut` ends along a straight cut at each end, as a broad pen's edge ends a
stroke, and fills the outer side of each corner to a mitre. A cut passes through the median's
end, and where the band's two edges meet it are its corners, one beyond the band's square end
and one short of it. Its angle is in degrees, counterclockwise on the page from the crop's x
axis, from 0 up to but not including 180, so that 90 is upright, and it makes at least 15° with
the median where it ends. Where two segments meet with a turn of less than 1°, there is no
corner.

**Level 2.** `<g class="strokes">` holds one `<g class="stroke" id="sN">` per stroke. Its
authored parts are:

- a `median`, one open subpath of one or more `C` segments, with no straight segment;
- `data-widths`, one positive width for each point of the median's path data: 1 + 3 × the
  number of segments;
- `data-ends`, `round` or `cut`; a stroke of the letters is cut (decision 16);
- `data-cuts`, for a cut stroke only: the angles of its cuts at the median's start and end;
- `data-pass`, `letters` or `marks`;
- `data-confidence`, `data-note`;
- for a supplied stroke only (decision 15), `data-supplied` and `data-supplied-why`, which
  go together.

**A supplied stroke** is one whose ink the crop does not show: `data-supplied="no-ink"` where
no ink of it is seen, and `traces` where only faint traces are. Every other stroke models ink
the crop shows, however flaked. `data-supplied-why` says what implies the stroke, such as the
transcription, the layout or a reader's judgment, and who supplied it. A supplied stroke's
median, widths and ends are authored like any other's, by analogy rather than by fitting.

Its `ink` is derived: convex polygons, each running clockwise, whose union is the band with
its discs or mitres. `<g class="pen-residual">` holds `unexplained`, the ink of the fills
judged ink that no stroke sweeps, and `overshoot`, what the strokes that are not supplied sweep
beyond that ink. A supplied stroke can explain ink, as faint traces of it, but its sweep beyond
the ink is no overshoot, since nothing fitted it to ink.

**How a supplied stroke is drawn.** Everything that draws a stroke-SVG draws a supplied stroke
in one style only: hatched in the orange `#ff6d00`, outlined with dashes, never filled solid,
and never in a stroke's colour, a group's colour or black, as the strokes in black that show
the page unaged are. No other layer uses that orange. `py/pen_stroke/render.py` holds the style,
and the stroke-SVG's own style element outlines a supplied stroke the same way when the file is
viewed alone.

**Level 3.** `data-shape` on each stroke is derived. A median no longer than half its greatest
width, or 2 pixels, is a `dot`. One that keeps within a tenth of its length, or 1 pixel, of
its chord is a `bar`. One whose segments meet at exactly one turn of 60° or more is a
`corner`. Any other is a `curve`.

**Level 4.** `<g class="frame" data-letter-height="…">` holds one `<line class="baseline">`.

**Level 5.** `<g class="groups">` holds one `<g class="group" id="gN" data-kind="…">` per sign
instance, holding a `<use href="#sN"/>` for each of its strokes. A stroke can therefore belong
to two groups, as a bar that served both strands' vowels would. The kinds are a closed list, in
`py/pen_stroke/level5.py`. Each kind names the Unicode character it is congruent to, or none,
as the undetermined kinds "bar under the letter" and "dot over the letter" do. Every stroke is
in a group, and a group's kind fixes the pass of its strokes. Ink of a neighbouring word or line
is traced and grouped too. Where the crop cuts it too short to name, it takes "unidentified
letter" or "unidentified mark".

**Whose ink.** Every group says whose ink it is, as `data-ink-of` (decision 17): `this-word`,
the chanted word a word's crop is of; `other-word`, another word of that word's line;
`this-line`, the line a line's crop is of; or `line-above` or `line-below`. A word's crop uses
`this-word` for its subject and a line's crop `this-line`, and a stroke's groups agree. Ink of
the line above or below needs that line's text on the root. Everything that draws a stroke-SVG
draws the strokes that are not the subject's in slate grey, `#607d8b`, which no other layer
uses, and the stroke-SVG's own style element does the same when the file is viewed alone.

**The ductus.** `data-ductus` says whether a file proposes how its subject was written, its
ductus: a term of palaeography for a letter's strokes, how many, in which direction and in
which order. Where it is `plausible`, the strokes are listed in the order written, every
stroke of the letters before every stroke of the marks (decision 11), and each median runs the
way the pen moved; a head comes before the stroke it joins (decision 16), a base after the
strokes it meets, written from left to right (decision 18), and an alef's upright before its
left leg (decision 19). Other lines' strokes
keep that order of the passes, but their directions propose nothing. Where it is `unrecorded`,
as in the four QUPO crops, the strokes' order and their medians' directions mean nothing.

## Where the profile departs from the plan's

The planning session's profile was a draft for profile 1 of this file. Implementing it changed
seven things, and profile 2 then replaced its stiff nib.

1. **Profile 1's nib had an edge.** The plan gave each nib a width and an angle. With an edge
   of zero thickness, a stroke moving along the nib's long side leaves no ink at all. The edge
   was a third value of each nib, fitted like the others. Profile 2 has no nib.
2. **The pen residual belongs to the crop, not to each stroke.** The plan made level 1's
   fills the observed ink. The residual is therefore computed once, from the fills and every
   sweep. No stroke stores an excursion of its own.
3. **A fill judged not to be ink** carries its judgment on the fill itself. There is no
   residual element for it.
4. **The image residual has three parts:** the judged pieces, and the smoothing and halo,
   which nobody judges.
5. **Profile 1's marks nib was fitted to all the crops' marks together.** Each crop has few
   marks, mostly dots and short bars, and no crop's marks determined a nib. Profile 2 fits each
   stroke's widths to its own ink.
6. **The kinds include undetermined ones and the two "unidentified" ones,** for bars the
   level cannot assign and for ink of other lines.
7. **Residual geometry follows pixel edges exactly,** so the lint can compare masks pixel for
   pixel. Fills and sweeps are curves and polygons.

## Profiles 1 to 4

Profile 1, of 2026-10-30, swept each crop's two stiff nibs, one for the letters and one for
the marks, along medians of straight segments that Claude placed by eye. Profile 2, of
2026-10-31, implements decision 14. A script of Claude's converted the four stroke-SVGs; it is
not tracked, and its steps were these:

1. split each median placed by eye at its turns of 55° or more, which became corners;
2. moved each run between corners onto the middle of its ink, where both edges of the ink can
   be found across it;
3. fitted each run with one or a few cubic segments, joined smoothly;
4. fitted the widths to the ink's width measured across the curve, leaving out every place
   where the measurement ran into another stroke's ink;
5. moved each free end to where its ink ends, and kept round or flat ends, whichever left
   less of the stroke's ink unexplained and less sweep beyond the ink.

The nibs are gone from the file. `nibfit` still measures them, as a statistic of the ink. The
pen residual under each profile is in the findings record's update.

Profile 3, also of 2026-10-31, adds supplied strokes (decision 15) and changes nothing else.
Moving the four stroke-SVGs to it changed only their profile and their style element, and
then page F102A's על־פני gained the qamats under its nun, supplied from faint traces as s30
and s31.

Profile 4, also of 2026-10-31, implements decisions 16 and 17 and the ductus. Ends are `round`
or `cut`, and `flat` is gone. A script of Claude's, not tracked, moved the four QUPO crops to
it:

1. each flat end became a cut square to the median, which left its ink as it was;
2. each round end of a stroke of the letters became a cut along an edge of the crop's stiff
   nib, as `nibfit` measures it, with the end slid along the median to fit the ink;
3. each group got its `data-ink-of` from its note, and each root the text of the lines above
   and below as far as the crop reaches, and `data-ductus="unrecorded"`.

Their heads are not yet strokes of their own. The two crops traced next, of whole lines, are
the first under profile 4 throughout; the findings record's update describes them.

## Running the tool

From the repository root, with the clone's own environment, as
`./.venv/Scripts/python.exe py/main_pen_stroke.py <subcommand>`.

1. `init <crop.png> --set key=value …` writes the stroke-SVG with its provenance, the crop's
   Otsu threshold and the derived level-1 parts.
2. Trace: add each stroke's median, widths, ends and pass, the groups, the frame and the
   judgments, in a vector editor or by hand. The reader ignores what Inkscape adds.
3. `derive` recomputes every derived part. A judgment carries over to the piece or fill with
   exactly the same pixels.
4. `nibfit <crop.png or stroke-SVG>` prints the stiff nib that best fits the ink's width
   against its direction, a statistic of the ink. It reads the letters and marks by component
   size in a crop, or by each pass's strokes in a stroke-SVG.
5. `check` reports every way a stroke-SVG departs from this profile and its crop.
   `py/tests/test_pen_stroke_svgs.py` runs the same check in the suite.
6. `render` writes `doc/pen-stroke-snips/overlays.html`: each stroke-SVG over its crop, drawn
   smoothly rather than as squares of pixels, with checkboxes beside each image that switch its
   layers, among them the strokes in black, the supplied strokes and other words' and lines'
   ink, and each crop's and stroke's figures. Where a file proposes its ductus, each median
   ends in an arrowhead, and a button beside the image plays the writing: the subject's
   strokes appear in their order, each along its median.

The mega does not run the tool, by Ben's decision of 2026-10-30: "this is not an appropriate part
of mega, this is a very early-stage experiment." `py/tests/test_mega_coverage.py` declares its
subcommands with that reason. The suite's lint derives every stroke-SVG again, but nothing
checks that `overlays.html` is current, so `render` is rerun by hand after any change.
