# The ink-region representation of a manuscript crop

State: live; the profile of the region-SVGs in `doc/pen-stroke-snips/`: profile 2 implemented on 2026-11-01, to Claude's design, which Ben approved as a plan the same day (decision 27); of its details he has so far reviewed how supplied ink is drawn (decision 26)

A crop of a manuscript page can be shown as pixels and read as a Unicode transcription. The
ink-region representation sits between them. It describes the crop's ink as **regions**, one or
more for each written part of a sign, which a watershed on the photograph's luminance draws from
seeds, and **groups** of regions that a reader would call a letter, a vowel, an accent, or ink to
set aside. It is kept as a **region-SVG**, `<crop>.regions.svg`, beside each crop in
`doc/pen-stroke-snips/`, and `regions.html` there draws every region-SVG in layers. That
directory's `README.md` gives each crop's provenance.

It replaces the strokes of the pen-stroke representation,
[pen-stroke-representation.md](pen-stroke-representation.md), whose six stroke-SVGs and
`overlays.html` are kept as a frozen record (decision 23). Its level 1, the ink as filled
outlines with the image residual, is that representation's, unchanged. The plan that built it is
[PLAN-ink-regions.md](PLAN-ink-regions.md), and the findings record's update,
[pen-stroke-exemplars-2026-10-30-update.md](pen-stroke-exemplars-2026-10-30-update.md), reports
what the drafts showed.

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

Decisions 23 to 25 are Ben's answers of 2026-11-01 to the plan's three decisions, and 26 on are
his later word.

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
26. **Supplied ink in colour alone, for now.** Asked to comment on the design choices that were
    Claude's, Ben wrote on 2026-11-01: "I don't think we want to use stipple, bars, dotted
    outlines, or anything else other than color, for now at least. Those all introduce too much
    high-spatial-frequency distracting information." So on the region page a supplied mark is
    filled with decision 15's orange and restored ink with decision 25's teal, with no hatching,
    stipple or dashed or dotted outline, and a region-SVG's own style draws them the same way;
    the frozen overlay page keeps decision 15's hatching. He asked for the change to wait for the
    next round of substantive changes, and it was made with his first answers to phase 3's sheet.
27. **The re-draft by rule.** After his first answers on the regions, Ben asked whether his
    comments "inform changes to the generalized algorithm, or are they just the kind of comments
    that each of these transcriptions is expected to need"; asked "Should I write a plan to
    re-draft all six crops by rule before any more hand corrections?", he answered "Yes, plan the
    re-draft". The plan's revision put five design choices to him: regions from seeds by a
    watershed, with several seeds a region and each seed's move of 2 pixels to the darkest ink;
    overlaps as authored outlines; supplied vellum as authored lines, with strips proposed by
    script; the parts rule; and wider candidates for restoration. Asked "Approve the re-draft
    plan as written?", Ben answered "Approve the plan". So the region-SVGs follow profile 2,
    which "The file" below gives, and all six crops were re-drafted under it on 2026-11-01.

## The file

The coordinates are the crop's pixels, as in a stroke-SVG: x to the right and y down, pixel
(i, j) covering [i, i + 1) × [j, j + 1), and a point inside a shape when it lies within its
outline. The root's `viewBox` is `0 0 <width> <height>`.

**The root** carries `data-profile="ink-region 2"`; the stroke-SVG's provenance, copied by a
script so that no Hebrew was typed, with `data-regions-by`, who placed the seeds, cuts, overlaps
and strips of vellum and made the groups, in place of `data-strokes-by`; and the threshold,
tracer, speck size and halo band. It has no nib and no ductus.

**Level 1** is derived exactly as a stroke-SVG's is, by the same code, with each judgment carried
over to the fill or piece with exactly the same pixels: `<g class="fills">` and
`<g class="image-residual">`, as the pen-stroke note's "The file" describes them.

**Supplied vellum.** `<g class="vellum">` holds one
`<path class="vellum" id="vN" data-why="…" d="…">` per strip, authored: its line, one open path
of straight segments, and `data-width`, its width in crop pixels, written only where it is not 1.
The ink whose samples lie within half the width of the line leaves the ink before anything else,
so that the strip divides it and shows as vellum, white in black on white. It is for a strip of
the page that level 1's fill covers, where the photograph's blur joins two signs: in Ben's words
of 2026-11-01, "a very thin "supplied vellum" (as opposed to "supplied ink") shape".
`data-why` says who drew or proposed the strip, and why.

**The cuts.** `<g class="cuts">` holds one `<path class="cut" id="cN" data-note="…" d="…">` per
cut, authored: one path of straight segments, open or closed. A cut is a correction, drawn only
where the watershed's boundary is wrong: no flood crosses it, and its ink goes back to a region
afterwards.

**The regions.** `<g class="regions">` holds one
`<g class="region" id="rgN" data-seed="x1 y1 x2 y2 …">` per region, whose id and seeds are
authored, holding one derived `<path>`, its outline. A region is a written part of a sign, one
of the shapes this manuscript writes apart: a qamats is a bar and a dot under it, a segol three
dots, a geresh one stroke. It has one seed or more, each in its part's ink, and one belongs in
the part's darkest ink near each place where it touches another part, since a flood follows the
darkest connection, not the letter. A region's id is `rg` and a number, since level 1's residual
pieces already have the ids `rN`.

**Overlaps.** `<g class="overlaps">` holds one `<g class="overlap" id="ovN" data-note="…">` per
proposed overlap: an authored `<path class="outline">`, closed, the intersection of plausible
shapes of two signs, and a derived `<path class="ink">`, the ink inside it. That ink is a region
of its own, which two groups or more hold. No other ink is shared: two parts that touch share
nothing unless an overlap is proposed.

**Supplied ink.** `<g class="supplied">` holds one
`<g class="supplied-ink" id="supN" data-supplied="…" data-supplied-why="…">` for each outline of
ink the crop does not show, holding its authored `<path class="outline">`, which is closed, and
its derived `<path class="added">`. `data-supplied` is `no-ink` or `traces`, as for a supplied
stroke (decision 15), or `flaked`, for ink restored where the image shows the ink has flaked.
`data-supplied-why` says what implies it and who supplied it. Candidates for restoration are
level 1's residual pieces judged `damage`.

**The groups.** `<g class="groups">` holds one `<g class="group" id="gN" data-kind="…"
data-ink-of="…" data-note="…">` per sign or piece of ink a reader names, as in a stroke-SVG
(level 5 there), holding a `<use href="#rgN"/>`, `<use href="#ovN"/>` or `<use href="#supN"/>`
for each of its regions, overlaps and supplied ink. The kinds are the closed list in
`py/pen_stroke/level5.py`, and `data-ink-of` says whose ink it is (decision 17). Every region is
in one group, every overlap in two or more, and every supplied ink in a group. Unlike a
stroke's, an overlap's groups may disagree on whose ink it is, since ink that two lines share is
how a collision between them is proposed. A group may carry `data-parts-note`, which the next
paragraph explains.

**The parts rule.** A closed table in `py/pen_stroke/level5.py`, `PARTS`, gives each kind's
number of written parts in this manuscript, and raises on a kind it does not know: two for a
sheva, a tsere, a qamats, a sof pasuq, a gershayim, a tevir and a zaqef; three for a segol, a
qubuts and a ḥataf pataḥ; one for every other mark; and no count for a letter, a kind that
leaves the sign undetermined, or ink set aside. A group whose kind has more than one part holds
at least that many regions, overlaps and supplied inks, unless its `data-parts-note` says why,
for what Ben called "some really extraordinary circumstance". The counts are Claude's, from the
signs' usual forms in this manuscript, and Ben has not reviewed them.

**How the regions are derived.** The ink is level 1's as judged: the fills judged ink, less every
residual piece judged `paper` or `damage`, and then with every piece judged `ink`. A hole the
tracer filled is a residual piece inside a fill, so a hole judged `paper`, such as the inside of
a ring, or `damage` is left out of the regions; a speck the tracer dropped, or faint ink, that is
judged `ink` is in them; and a piece judged anything else, such as `noise`, leaves the fills as
they are. Then, at 3 samples a pixel each way, every step deterministic:

1. the ink is rasterized, a sample being inside when its centre is, so that the regions keep
   level 1's smooth outlines, and every sample whose centre lies within half a strip of
   vellum's width of its line leaves the ink;
2. every sample that a cut's segments cross is set aside, each segment drawn from the sample
   holding its start to the sample holding its end as an 8-connected line of samples, so that
   no 4-connected path crosses it;
3. every 4-connected piece of the ink that remains must hold a seed, and every seed must lie in
   one, the seed lying in the sample whose square holds it; but a crumb, a piece that holds no
   seed and no more samples than the speck size, which the tracer would drop, is set aside as
   the cuts' samples are;
4. each seed moves to the darkest sample of its piece within 2 pixels, the first in row order on
   a tie;
5. the watershed: from all the seeds at once, the floods take each piece's samples in order of
   the photograph's luminance, darkest first, a tie going to the sample reached first, and each
   sample goes to the seed whose flood reaches it first, so that the boundary between two
   regions runs along the palest, narrowest line between their seeds; the luminance at a sample
   is interpolated bilinearly between the centres of the crop's pixels, in whole numbers, so
   that it is the same on every machine;
6. each sample set aside goes back to the 4-adjacent region of lowest number, round after round,
   until none is left that touches a region;
7. each overlap takes the ink of step 1 inside its outline out of the regions, as a region of
   its own;
8. each region's and each overlap's samples are traced with level 1's tracer and its speck size
   as the tracer's speck limit, and the outline is scaled to crop pixels, to 3 decimal places.

A supplied outline's added ink is its samples less the ink's, traced the same way, so that
supplied ink never claims ink the image shows.

**Profile 1,** of 2026-11-01, had the same level 1, supplied ink and groups, but no vellum,
overlaps or parts rule. Each region had one seed; cuts divided every piece of ink that held more
than one region; and a region that two groups held was how an overlap was proposed. A script
drafted its six region-SVGs from the frozen strokes, which no new crop would have, and after
Ben's first answers on them all six were re-drafted under profile 2 (decision 27).

## The check

`regions-check` reports every way a region-SVG departs from the profile and its crop:

- the profile's structure, and a kind, `data-ink-of` or `data-supplied` value not on its list;
- an id used twice; a group that holds nothing or names what is not in the file; a region,
  overlap or supplied ink in no group; a region in more than one group; and an overlap that
  fewer than two groups hold;
- a group that holds fewer members than its kind has written parts, with no `data-parts-note`;
- a group whose owner does not suit the crop's subject, or ink of the line above or below with no
  text of that line on the root;
- a residual piece not yet judged;
- level 1 that differs from what the crop gives;
- a strip of vellum whose line is not one open path of straight segments, or that takes out no
  ink; a cut that is not one path of straight segments, or crosses no ink;
- a seed outside the ink, in a strip of vellum or on a cut; seeds of two regions that move to the
  same sample; a piece of ink, other than a crumb, that holds no seed; and ink under a cut or in
  a crumb that goes back to no region;
- an overlap whose outline is not closed, that takes no ink, or that shares ink with another
  overlap, and a region whose ink overlaps take entirely;
- a region's outline or an overlap's ink that differs from what derivation gives, or that is too
  small to trace;
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
   page uses, translucent, so that an overlap shows the colour of each group that holds it;
5. the ink by region, each of the subject's regions and overlaps in a colour of its own, from a
   palette without decision 15's orange, the restored ink's teal or decision 17's slate;
6. supplied ink and supplied vellum, on at first: a supplied mark filled with the orange
   `#ff6d00` (decision 15), restored ink with the teal `#00897b` (decision 25), and the ink a
   strip of vellum takes out with the tan `#e6cf9c`, each in its colour alone, with no hatching,
   stipple or outline (decision 26), none ever drawn in black or in a group's or a region's
   colour, and each in a colour no other layer uses;
7. two checkboxes, on at first, which hide in every layer other words' and lines' ink, and
   masora circles and stray ink: faint until hidden;
8. for checking: level 1's residual pieces, by judgment; the cuts, overlaps' outlines and the
   lines of the strips of vellum, each one thin pink line, and every seed; and the regions' and
   overlaps' ids.

Ink of another word or line is slate in every layer, as decision 17 requires. The colours of the
meanings, the palette of the regions, the teal, the tan and the name and profile of the file are
Claude's choices, which Ben has not yet reviewed.

## Running the tool

From the repository root, with the clone's own environment, as
`./.venv/Scripts/python.exe py/main_pen_stroke.py <subcommand>`.

1. Author a region-SVG's seeds, cuts, strips of vellum, overlaps' outlines, supplied outlines,
   groups and judgments in a vector editor or by hand. A script of Claude's, which the snips
   README describes, re-drafted the six under profile 2.
2. `regions-derive` recomputes every derived part and reports what the authored parts leave
   unsettled.
3. `regions-check` reports every way a region-SVG departs from this profile and its crop.
4. `regions-render` writes `doc/pen-stroke-snips/regions.html`.

The mega does not run the tool, by Ben's decision of 2026-10-30, which the pen-stroke note's
"Running the tool" quotes. `py/tests/test_mega_coverage.py` declares these subcommands with that
reason. The suite's lint derives every region-SVG again, but nothing checks that `regions.html`
is current, so `regions-render` is rerun by hand after any change.
