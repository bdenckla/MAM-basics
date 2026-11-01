# The ink-region representation of a manuscript crop

State: live; the profile of the region-SVGs in `doc/pen-stroke-snips/`: profile 1 implemented on 2026-11-01, to Claude's design, which Ben has not yet reviewed

A crop of a manuscript page can be shown as pixels and read as a Unicode transcription. The
ink-region representation sits between them. It describes the crop's ink as **regions**, cut
where things a reader tells apart touch, and **groups** of regions that a reader would call a
letter, a vowel, an accent, or ink to set aside. It is kept as a **region-SVG**,
`<crop>.regions.svg`, beside each crop in `doc/pen-stroke-snips/`, and `regions.html` there draws
every region-SVG in layers. That directory's `README.md` gives each crop's provenance.

It replaces the strokes of the pen-stroke representation,
[pen-stroke-representation.md](pen-stroke-representation.md), whose six stroke-SVGs and
`overlays.html` are kept as a frozen record (decision 23). Its level 1, the ink as filled
outlines with the image residual, is that representation's, unchanged. The plan that built it is
[PLAN-ink-regions.md](PLAN-ink-regions.md), and the findings record's update,
[pen-stroke-exemplars-2026-10-30-update.md](pen-stroke-exemplars-2026-10-30-update.md), reports
what the first drafts showed.

## What the regions are for

Ben, on 2026-11-01, after judging the pen-stroke work's fifth round "incremental improvements on
a fundamentally-flawed system": "I really just wonder whether we need a stroke model at all.
"Regions of ink" may be good enough for our purposes." His uses for them, each in his words of
that day:

1. **Colour by meaning:** "to be able to do things like give different colors to different
   ink-regions that in some way were semantically distinct, whether they represented a whole
   letter, part of a letter, a diacritic, part of a diacritic, etc."
2. **Set aside what is not pertinent:** "to color lightly or remove marks not pertinent to the
   discussion of the manuscript, for example marks from another line or even
   invasive/distracting marks like a masorah circle from the line in question". Colouring them
   lightly "is perhaps more "honest" than removing them".
3. **A clean page:** "getting rid of background noise, e.g. all marks we consider non-ink. And
   giving a perfect white background (which also makes it abundantly clear that this is a
   synthetic image BTW)."
4. **Granularity by application:** what a region is does not matter in general, but "for any
   given application, it certainly does matter!"
5. **Proposed overlaps:** "using color and transparency to illustrate proposed overlappings,
   i.e. proposed explanations of otherwise-perplexing shapes of ink". The boundary "can be from
   human input e.g. a boundary described in words or drawn with a line on the image".
6. **Deflaking:** "conceptual re-inking flaked regions. Of course there's honesty issues there,
   so probably some color should be used to show restored sections".

## Ben's decisions

The pen-stroke note numbers its decisions 1 to 22. This note continues from 23, so that one
number names one decision across the work.

1. **Carried over** from the pen-stroke note: 1 (one crop is the unit), 4 (no links to a
   transcription's coordinates), the first half of 6 (filled outlines with residuals come
   first), 9 (SVG with a lint), 10 (the crops in `doc/pen-stroke-snips/`, Claude doing the
   tracing), 11 (the levels transcribe the image with the text in hand; only level 1 is
   automated), 13 (the combined transcription is primary), 15 (supplied marks, never drawn as
   others are), 17 (whose ink each group is, other lines' ink in a colour of its own), 21 (masora
   circles told apart from the marks that matter) and 22 (likely stray ink transcribed and
   marked so).
2. **Parked with the pen** by decision 23: 2, 3, 5, 7, 12, 14, 16, 18, 19 and 20, which concern
   the nib, a stroke's widths and ends, heads, bases, the alef's upright and the ductus; and the
   history of the writing, which the pen-stroke note's decision 11 frames.
3. **Historical:** 8 (the first crops were the QUPO words).

The three below are Ben's answers of 2026-11-01 to the plan's three decisions.

23. **Regions of ink in place of strokes.** Asked "Adopt regions of ink in place of strokes,
    freezing the stroke files as a record?", Ben answered "Yes, regions". So each crop has a
    region-SVG, and the six stroke-SVGs and `overlays.html` are frozen as a record of the
    pen-stroke work: no further edits, though the suite still checks them. The pen and the
    history of the writing are given up.
24. **Feedback in words, by drawing, or both, for any crop.** Asked "How will you give
    boundaries and restorations?", Ben answered: "I'd like to be able to give feedback in one or
    both of those forms, for any given crop". So he may describe a cut or a restoration in words,
    which Claude turns into a cut or an outline and shows him in context, or draw it on a drawing
    page that covers all six crops. Claude had recommended words first.
25. **Restored ink in a style of its own.** Asked "Draw restored ink in the same hatched orange
    as supplied marks?", Ben answered "A style of its own". So a supplied mark keeps decision
    15's style, and restored ink has a second style, reserved for it, which "The page" below
    gives. Claude had recommended one style for all added ink.

## The file

The coordinates are the crop's pixels, as in a stroke-SVG: x to the right and y down, pixel
(i, j) covering [i, i + 1) × [j, j + 1), and a point inside a shape when it lies within its
outline. The root's `viewBox` is `0 0 <width> <height>`.

**The root** carries `data-profile="ink-region 1"`; the stroke-SVG's provenance, copied by a
script so that no Hebrew was typed, with `data-regions-by`, who drew the cuts and seeds and made
the groups, in place of `data-strokes-by`; and the threshold, tracer, speck size and halo band.
It has no nib and no ductus.

**Level 1** is derived exactly as a stroke-SVG's is, by the same code, with each judgment carried
over to the fill or piece with exactly the same pixels: `<g class="fills">` and
`<g class="image-residual">`, as the pen-stroke note's "The file" describes them.

**The cuts.** `<g class="cuts">` holds one `<path class="cut" id="cN" data-note="…" d="…">` per
cut, authored: one path of straight segments, drawn across the ink where two things a reader
tells apart touch, or along the edge of a proposed overlap. It is open, or closed where one part
lies wholly inside another.

**The regions.** `<g class="regions">` holds one `<g class="region" id="rgN" data-seed="x y">`
per region, whose id and seed point are authored, holding one derived `<path>`, its outline. A
region's id is `rg` and a number, since level 1's residual pieces already have the ids `rN`.

**Supplied ink.** `<g class="supplied">` holds one
`<g class="supplied-ink" id="supN" data-supplied="…" data-supplied-why="…">` for each outline of
ink the crop does not show, holding its authored `<path class="outline">`, which is closed, and
its derived `<path class="added">`. `data-supplied` is `no-ink` or `traces`, as for a supplied
stroke (decision 15), or `flaked`, for ink restored where the image shows the ink has flaked.
`data-supplied-why` says what implies it and who supplied it. Candidates for restoration are
level 1's residual pieces judged `damage`.

**The groups.** `<g class="groups">` holds one `<g class="group" id="gN" data-kind="…"
data-ink-of="…" data-note="…">` per sign or piece of ink a reader names, as in a stroke-SVG
(level 5 there), holding a `<use href="#rgN"/>` or `<use href="#supN"/>` for each of its regions
and supplied ink. The kinds are the closed list in `py/pen_stroke/level5.py`, and `data-ink-of`
says whose ink it is (decision 17). Every region and supplied ink is in a group. A region in two
groups is shared ink, and that is how an overlap is proposed: the cuts bound the part that two
shapes are proposed to share. Unlike a stroke's, a region's groups may disagree on whose ink it
is, since ink that two lines share is how a collision between them is proposed.

**How the regions are derived.** The ink is level 1's as judged: the fills judged ink, less every
residual piece judged `paper` or `damage`, and then with every piece judged `ink`. A hole the
tracer filled is a residual piece inside a fill, so a hole judged `paper`, such as the inside of
a ring, or `damage` is left out of the regions; a speck the tracer dropped, or faint ink, that is
judged `ink` is in them; and a piece judged anything else, such as `noise`, leaves the fills as
they are. Then, at 3 samples a pixel each way, every step deterministic:

1. the ink is rasterized, a sample being inside when its centre is, so that the regions keep
   level 1's smooth outlines;
2. every sample that a cut's segments cross is removed, each segment drawn from the sample
   holding its start to the sample holding its end as an 8-connected line of samples, so that
   no 4-connected path crosses it;
3. of the 4-connected pieces of ink that remain, each must hold exactly one region's seed, the
   seed lying in the sample whose square holds it, and every seed must lie in one; but a crumb,
   a piece that holds no seed and no more samples than the speck size, which the tracer would
   drop, is removed as the cuts' samples are;
4. each removed sample of ink goes back to the 4-adjacent region of lowest number, round after
   round, until none is left that touches a region;
5. each region's samples are traced with level 1's tracer and its speck size as the tracer's
   speck limit, and the outline is scaled to crop pixels, to 3 decimal places.

A supplied outline's added ink is its samples less the ink's, traced the same way, so that
supplied ink never claims ink the image shows.

## The check

`regions-check` reports every way a region-SVG departs from the profile and its crop:

- the profile's structure, and a kind, `data-ink-of` or `data-supplied` value not on its list;
- an id used twice, a group that holds nothing or names what is not in the file, and a region or
  supplied ink in no group;
- a group whose owner does not suit the crop's subject, or ink of the line above or below with no
  text of that line on the root;
- a residual piece not yet judged;
- level 1 that differs from what the crop gives;
- a cut that is not one path of straight segments, or crosses no ink;
- a seed outside the ink or on a cut, two seeds in one piece of ink, a piece of ink, other than a
  crumb, that holds no seed, and ink under a cut that goes back to no region;
- a region's outline that differs from what its seed and the cuts give, or too small to trace;
- supplied ink whose outline is not closed, whose added ink differs from what derivation gives,
  or that adds no ink.

`py/tests/test_ink_region_svgs.py` runs the same check in the suite, and fails if the directory
holds no region-SVG.

## The page

`regions.html` gives, for each crop, its provenance and transcriptions, and one image with
checkboxes beside it that act on that image alone, a size menu, and the photograph drawn
smoothly, never as squares of pixels. The layers, the first drawn lowest:

1. the photograph, off at first;
2. the ink, black on pure white, other words' and lines' ink in decision 17's slate;
3. the ink by meaning, on at first: the subject's letters black, its marks dark blue, masora
   circles and stray ink a faint violet, and other words' and lines' ink a faint tint of slate;
   a region in groups of several meanings takes the first of those four;
4. the ink by group, each of the subject's groups in the next of the five colours the overlay
   page uses, translucent, so that a region in two groups shows both;
5. the ink by region, each of the subject's regions in a colour of its own, from a palette
   without decision 15's orange, the restored ink's teal or decision 17's slate;
6. supplied ink, on at first: a supplied mark hatched in the orange `#ff6d00` and outlined with
   dashes (decision 15), and restored ink stippled in the teal `#00897b` and outlined with dots
   (decision 25), neither ever filled solid or drawn in black or in a group's or a region's
   colour, and each in a colour no other layer uses;
7. two checkboxes, on at first, which hide in every layer other words' and lines' ink, and
   masora circles and stray ink: faint until hidden;
8. for checking: level 1's residual pieces, by judgment; the cuts and each region's seed; and
   the regions' ids.

Ink of another word or line is slate in every layer, as decision 17 requires. The colours of the
meanings, the palette of the regions, the stippled teal and the name and profile of the file are
Claude's choices, which Ben has not yet reviewed.

## Running the tool

From the repository root, with the clone's own environment, as
`./.venv/Scripts/python.exe py/main_pen_stroke.py <subcommand>`.

1. Author a region-SVG's cuts, seeds, supplied outlines, groups and judgments in a vector
   editor or by hand. The six drafts were written by a script of Claude's, which the snips
   README describes.
2. `regions-derive` recomputes every derived part and reports what the cuts and seeds leave
   unsettled.
3. `regions-check` reports every way a region-SVG departs from this profile and its crop.
4. `regions-render` writes `doc/pen-stroke-snips/regions.html`.

The mega does not run the tool, by Ben's decision of 2026-10-30, which the pen-stroke note's
"Running the tool" quotes. `py/tests/test_mega_coverage.py` declares these subcommands with that
reason. The suite's lint derives every region-SVG again, but nothing checks that `regions.html`
is current, so `regions-render` is rerun by hand after any change.
