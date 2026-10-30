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
record here.

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

## The ladder

Each level adds one kind of interpretation and is authored or derived separately, so a
disagreement at a higher level never rewrites a lower one.

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

The mega does not run the tool. `py/tests/test_mega_coverage.py` declares its subcommands, as a
Claude-written proposal awaiting Ben's review: they are run by hand, and the suite's lint
already derives every file again.
