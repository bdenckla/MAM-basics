# The pen-stroke representation of a manuscript crop

State: live; the profile of the stroke-SVGs in `doc/pen-stroke-snips/`, as implemented on 2026-10-30

A crop of a manuscript page can be shown as pixels and read as a Unicode transcription. The
pen-stroke representation sits between them. It describes the crop's ink as filled outlines,
then as strokes of a pen, then as groups of strokes that a reader would call a letter, a vowel
or an accent. It is kept as a **stroke-SVG**, `<crop>.strokes.svg`, beside each crop in
`doc/pen-stroke-snips/`. That directory's `README.md` gives each crop's provenance, and
[pen-stroke-exemplars-2026-10-30.md](pen-stroke-exemplars-2026-10-30.md) reports what the first
four crops showed.

## Ben's decisions

All are of 2026-10-30. The first nine were made in the planning session "Investigate a
pen-stroke manuscript representation", whose plan was not committed, so this list is their
record here. Decisions 11 and 12 were made while Ben reviewed the first exemplars.

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

    The profile does not yet record a stroke's direction, its place in the writing or its pass,
    and `py/main_pen_stroke.py render` draws no black-on-white view.
12. **The nib model is calligraphic: a stroke's width may vary along its course.** Ben:
    "Absolutely a "calligraphic" nib model is needed, by which I mean one in which stroke-width
    is modulated (or can be modulated) throughout the course of a stroke. It doesn't matter what
    the physical analogy is, or how close that analogy is to the historical quill or reed or
    whatever. Width-modulation could even be done with a fine brush, for all we care (although
    line endings would probably be different with a brush)." The stiff nib this profile
    implements, below, is the special case in which nothing varies along a stroke. The bound on
    the modulation is not yet set. In the planning session, behind decision 6, Ben asked for
    pen strokes "where the frequency (and/or other characteristics) of the width modulation is
    limited to what seems physically possible". Without a bound, a stroke could follow every
    irregularity of its ink, and the excursions that decision 3 treats as information would
    vanish.

## The ladder

Each level holds one kind of interpretation and is authored or derived separately. The work
does not climb the levels in order. It proceeds inward from the two ends, the crop's pixels and
a Unicode transcription, and a reading at any level may send it back to revise another
(decision 11).

| Level | What it holds | Authored or derived |
| --- | --- | --- |
| 0 crop | the pixels, with their provenance | authored |
| 1 fills | the ink as filled Bézier outlines, and the image residual | outlines derived; residual judgments authored |
| 2 strokes | a median per stroke swept by a nib, and the pen residual | medians and nibs authored; ink and residual derived |
| 3 shape classes | dot, bar, corner or curve, from a stroke's median | derived |
| 4 frame | the baseline and the letter-body height | authored |
| 5 groups | strokes forming one sign, with a kind congruent to a code point | authored |
| 6 links | a group's place in a named, versioned transcription | parked (decision 4) |

## The file

The coordinates are the crop's pixels, x to the right and y down. Pixel (i, j) covers
[i, i + 1) × [j, j + 1), and a pixel is inside a shape when its centre is. The root's `viewBox`
is `0 0 <width> <height>`, the crop's pixel size.

**The root** carries `data-profile="pen-stroke 1"`; the provenance, as `data-manuscript`,
`data-page`, `data-column`, `data-line`, `data-line-read-by`, `data-mam-verse`,
`data-uxlc-verse`, `data-taxton-chanted-word`, `data-elyon-chanted-word`, `data-crop-note`,
`data-source-url`, `data-source-size`, `data-source-sha256`, `data-crop-box` and
`data-strokes-by`; the threshold and tracer parameters; and the two nibs.

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

**The nib** is a rectangle `width` long and `edge` thick. Its long side lies at `angle`
degrees counterclockwise from the crop's x axis, as seen on the page. Moved at an angle φ, it
leaves a band of ink width · |sin(φ − angle)| + edge · |cos(φ − angle)| thick. Nothing but
direction modulates it: the nib is stiff. A nib of width w at angle a with edge e leaves the
same widths as one of width e at a + 90° with edge w. A fitted nib is therefore read the way
whose width is the larger. The root's `data-nib-letters-width`, `-angle` and `-edge` give the
letters nib, and `data-nib-marks-*` give the marks nib.

**Level 2.** `<g class="strokes">` holds one `<g class="stroke" id="sN">` per stroke. Its
authored parts are:

- a `median`, one subpath of straight segments (a curve in it is flattened);
- `data-nib`, `letters` or `marks`;
- optionally, a whole nib of its own, as `data-nib-width`, `data-nib-angle` and `data-nib-edge`;
- `data-confidence`, `data-note`.

Its `ink` is derived: one convex polygon per segment of the median, the nib swept along it,
whose union is the stroke. `<g class="pen-residual">` holds `unexplained`, the ink of the fills
judged ink that no stroke sweeps, and `overshoot`, what the strokes sweep beyond that ink.

**Level 3.** `data-shape` on each stroke is derived. A median no longer than half the nib's
width, or 2 pixels, is a `dot`. One that keeps within a tenth of its length, or 1 pixel, of
its chord is a `bar`. One with exactly one turn of 60° or more is a `corner`. Any other is a
`curve`.

**Level 4.** `<g class="frame" data-letter-height="…">` holds one `<line class="baseline">`.

**Level 5.** `<g class="groups">` holds one `<g class="group" id="gN" data-kind="…">` per sign
instance, holding a `<use href="#sN"/>` for each of its strokes. A stroke can therefore belong
to two groups, as the shared bar of a QUPO letter does. The kinds are a closed list, in
`py/pen_stroke/level5.py`. Each kind names the Unicode character it is congruent to, or none,
as the undetermined kinds "bar under the letter" and "dot over the letter" do. Every stroke is
in a group, and a group's kind fixes the nib of its strokes. Ink of a neighbouring word or line
is traced and grouped too, with a `data-note` that says whose it is. Where the crop cuts it too
short to name, it takes "unidentified letter" or "unidentified mark".

## Where the profile departs from the plan's

The planning session's profile was a draft for this file. Implementing it changed seven things.

1. **The nib has an edge.** The plan gave each nib a width and an angle. With an edge of zero
   thickness, a stroke moving along the nib's long side leaves no ink at all. The edge is a
   third value of each nib, fitted like the others.
2. **The pen residual belongs to the crop, not to each stroke.** The plan made level 1's
   fills the observed ink. The residual is therefore computed once, from the fills and every
   sweep. No stroke stores an excursion of its own.
3. **A fill judged not to be ink** carries its judgment on the fill itself. There is no
   residual element for it.
4. **The image residual has three parts:** the judged pieces, and the smoothing and halo,
   which nobody judges.
5. **The marks nib is fitted to all the crops' marks together.** Each crop has few marks,
   mostly dots and short bars, and no crop's marks determined a nib.
6. **The kinds include undetermined ones and the two "unidentified" ones,** for bars the
   level cannot assign and for ink of other lines.
7. **Residual geometry follows pixel edges exactly,** so the lint can compare masks pixel for
   pixel. Fills and sweeps are curves and polygons.

## Running the tool

From the repository root, with the clone's own environment, as
`./.venv/Scripts/python.exe py/main_pen_stroke.py <subcommand>`.

1. `init <crop.png> --set key=value …` writes the stroke-SVG with its provenance, the crop's
   Otsu threshold, nibs fitted to its ink, and the derived level-1 parts.
2. Trace: add each stroke's median and nib, the groups, the frame and the judgments, in a
   vector editor or by hand. The reader ignores what Inkscape adds.
3. `derive` recomputes every derived part. A judgment carries over to the piece or fill with
   exactly the same pixels.
4. `nibfit <crop.png or stroke-SVG>` prints the stiff nib that best fits the ink's width
   against its direction. It reads the letters and marks by component size in a crop, or by
   the traced strokes in a stroke-SVG.
5. `check` reports every way a stroke-SVG departs from this profile and its crop.
   `py/tests/test_pen_stroke_svgs.py` runs the same check in the suite.
6. `render` writes `doc/pen-stroke-snips/overlays.html`: each stroke-SVG over its crop, with
   every layer switchable, and each crop's and stroke's figures.

The mega does not run the tool, by Ben's decision of 2026-10-30: "this is not an appropriate part
of mega, this is a very early-stage experiment." `py/tests/test_mega_coverage.py` declares its
subcommands with that reason. The suite's lint derives every stroke-SVG again, but nothing
checks that `overlays.html` is current, so `render` is rerun by hand after any change.
