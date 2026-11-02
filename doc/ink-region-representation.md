# The ink-region representation of a manuscript crop

State: live; the profile of the region-SVGs in `doc/pen-stroke-snips/`: profile 2 implemented on 2026-11-01, to Claude's design, which Ben approved as a plan the same day (decision 27); profile 3, regions from fitted glyphs, implemented on 2026-11-02, to Claude's design, which Ben approved as a plan the same day (decision 29), with all six crops moved to it the same day; of their details he has so far reviewed how supplied ink is drawn (decision 26); his review of the fitted crops on 2026-11-02 gave decisions 30 to 34 and a plan for the font of the manuscript's shapes, phases 12 to 16 of the plan, which he approved the same day (decision 35); profile 4 and the library's profile 2, which follow that font's guidelines, implemented on 2026-11-02, and the library and all six crops moved to them the same day; the work paused on 2026-11-02, at Ben's word, with phase 14 of the plan unfinished

A crop of a manuscript page can be shown as pixels and read as a Unicode transcription. The
ink-region representation sits between them. It describes the crop's ink as **regions**, one or
more for each written part of a sign, which a watershed on the photograph's luminance draws from
seeds, and **groups** of regions that a reader would call a letter, a vowel, an accent, or ink to
set aside. It is kept as a **region-SVG**, `<crop>.regions.svg`, beside each crop in
`doc/pen-stroke-snips/`, and `regions.html` there draws every region-SVG in layers. That
directory's `README.md` gives each crop's provenance. Under profile 3 the watershed's regions
are only a draft: each written part of a sign gets a **glyph** from a library of glyphs,
`glyphs.svg` there, placed at its ink and fitted to it, and a region is the ink inside one
sign's glyph. Under profile 4 the fit follows the five guidelines of the font of the
manuscript's shapes, which a group or a glyph may break.

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
28. **A plan for regions from a fitted word.** Ben proposed on 2026-11-01 to "drop the typeset
    version (in some font we will hopefully evolve to be a Leningrad-like font) of the word
    down and distort it based on what you find in ink-fills", and then asked for a try: "Okay
    go ahead and try this new plan". An untracked trial fitted glyphs to page F043A's two
    crops of one chanted word, and its report recommended glyphs taken from the scribe's own
    clean letters, with Taamey D's only where the library has none. Asked "Should I write the
    plan for building regions from fitted glyphs?", Ben answered on 2026-11-02 "Yes, write the
    plan". It is decision 6 of [PLAN-ink-regions.md](PLAN-ink-regions.md).
29. **Profile 3 approved.** The plan's revision put six design choices to Ben: profile 3, with
    the watershed as the draft; the library of glyphs, the scribe's clean letters with Taamey
    D's for the marks; an overlap only where ink lies deep inside two glyphs, at a depth set
    from his readings; the fit proposing and the check never fitting; his lines binding the
    fit, with Claude's corrections of the watershed in page F043A's מתחת dropped; and phase 7
    ending on his approval. Asked "Approve phases 8 to 11 as written?", Ben answered on
    2026-11-02 "Approve the plan". So profile 3, which "Profile 3: regions from fitted glyphs"
    below gives, was implemented the same day.
30. **Drawn marks.** Reviewing the fitted crops on 2026-11-02, Ben asked for "our overall
    strategy of developing a font (or font-like information) that corresponds to the Leningrad
    manuscript's shapes for letters and diacritics, rather than Taamey D's", whose printed shapes
    he saw causing small problems. Claude recommended a library in which no glyph comes from a
    print: first the marks, drawn to the manuscript's shapes; then every letter the scribe's own,
    from many instances; and later the marks from the scribe's ink too. Ezra SIL's marks were the
    alternative to the first step. Asked "Should the font's next plan draw the marks to the
    manuscript's shapes?", Ben answered "Yes, drawn marks".
31. **Five guidelines, broken per word.** After his comments on the fitted crops, Claude proposed
    five rules for the font's plan: glyphs only from well-preserved, well-written instances; area
    preserved where the ink is intact; a letter's limbs following its ink; drawn marks, with
    munaḥ one curved stroke and geresh a simple bar; and rafe a mark of its own. Ben answered
    "Yes, write the plan with those five rules. I sort of prefer to call them guidelines since I
    have a feeling we'll often want to break them, at least on a per-word basis", and of the
    system: "At the moment I'm conceiving of this system as a fully-automated way to come up
    with results that will, in most cases, need to be human-tweaked." They are phases 12 to 16
    of [PLAN-ink-regions.md](PLAN-ink-regions.md), which he approved (decision 35).
32. **Rafe.** Ben: "we are going to need to transcribe rafeh but of course our Unicode sources
    rarely do so". His expectations, for a later proposal of rafe where the Unicode source has
    none: "except in very rare cases, a letter with a dagesh is not expected to have a rafeh";
    "On gutturals that can get mapiq (mainly he but, rarely, alef), rafeh may be somewhat
    common, to express (no mapiq). But I would expect rafeh never on either ayin or xet." Asked
    whether the dark stroke above the left tav of page F102A's מתחת is a rafe, he answered "yes
    it is a rafeh".
33. **The name "overfill".** Asked what to call the ink that a sign's draft holds outside its
    glyph but within 1.3 pixels of one, Ben answered "just choose a name; as long as it is fairly
    unique, we can bulk-change it later if I don't like it". Claude kept "overfill", from his
    "overfilled", which no other file of the repository uses.
34. **Line 23's lamed's head.** Shown two fits of line 23's lamed at the mem's base in page
    F043A's מתחת, Ben preferred the one with Claude's cut c4, "at least as far as the more
    limited extent of the overlap it proposes, compared to the huge overlap of "without c4"". The
    plan reaches that placement with seeds in the mem's base rather than the cut, which the
    lamed's glyph crossed.
35. **Phases 12 to 16 approved.** The plan's revision put its design choices to Ben: breaks
    written as `data-break`; glyphs judged well preserved, with glyph crops for new ones; area
    matched by scaling a mark and moving a letter's outline; a finer warp; five drawn shapes;
    and rafe a kind of its own. Asked "Approve phases 12 to 16 as written?", Ben answered on
    2026-11-02 "Approve the plan". So profile 4 and the library's profile 2, which "Profile 4:
    the guidelines of the font" and "The library of glyphs" below give, were implemented the
    same day.

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

## Profile 3: regions from fitted glyphs

The watershed knows the ink and its luminance but not the letters, so at a junction its boundary
runs where the ink is palest, not where a letter ends. A glyph knows the shape, without the
model of the pen that decision 23 set aside. A profile-3 file, `data-profile="ink-region 3"`,
holds everything a profile-2 file holds, whose derivation is its **draft**, and adds:

- **Glyphs.** `<g class="glyphs">` holds one `<g class="glyph" id="glN">` for each written part
  of each fitted group: `data-group`, its group; `data-part`, the part's name in the library's
  table, written only for a sign of several parts; `data-glyph`, its glyph in the library;
  `data-fit`, the fit's parameters, a move, two scales as logarithms, a turn in radians and a
  shear, and for a letter a warp of 18 numbers, each to 4 decimals; a derived
  `<path class="outline">`, the library's glyph placed by those parameters, to 3 decimals; and
  a derived `<path class="ink">`, the ink that is that glyph's alone. Only the fit writes the
  parameters: a correction changes what the fit starts from, and the fit runs again.
- **Overlaps of glyphs.** `<g class="glyph-overlaps">` holds one derived
  `<path class="glyph-overlap" id="goN" data-glyphs="glA glB" d="…">` for each piece of ink
  that lies deep inside two glyphs, numbered in the order of each piece's first sample.
- **Which groups are fitted:** each group of the crop's subject, and each group of another word
  or line that has `data-fit="yes"`, whose kind the library's table fits and which holds a
  region with draft ink for each written part of a sign of several. The table fits no
  unidentified letter or mark, masora circle, stray ink or tevir. A group with no region, such
  as the supplied qamats of page F102A's על־פני, is not fitted, and the check says so without
  failing.

The derivation, after the draft's eight steps, at the same samples:

9. each glyph's outline, as written, is rasterized by the nonzero rule;
10. a 4-connected piece of the ink inside two glyphs or more is an overlap if some sample of it
    lies deeper than 1.5 pixels inside each of two of them, its depth inside a glyph being its
    distance from the glyph's outline; otherwise the glyphs only touch there, and each of its
    samples goes to the glyph it lies deepest inside, the lower group number and then the
    earlier part on a tie;
11. the rest of the ink inside one glyph is that glyph's;
12. each region keeps the ink the draft gave it that lies inside no glyph, as its derived
    outline: an unfitted group's region its ink, and a fitted group's region what its glyphs
    leave of its draft, **overfill** within 4 samples, about 1.3 pixels, of a glyph in
    8-connected steps, and **unexplained ink** farther away;
13. each glyph's ink, each overlap of glyphs and each region is traced as in profile 2.

The depth of 1.5 pixels was set on 2026-11-02 from Ben's readings of page F043A's מתחת: the
geresh and the tav only touch, the deepest sample inside both lying 0.64 pixels inside the
shallower of the two, and line 23's lamed overlaps the mem, 4.80; a qamats's bar and its dot
there, 1.04, also only touch. The fits of all six crops later that day found three pairs of
signs that only touch lying 1.82 to 2.71 pixels deep, so that D makes them overlaps, a finding
for Ben's review that the plan's execution record, "Phase 9, 2026-11-02", gives. Every strip of
vellum and every cut that a profile-3 file keeps
binds the fit: the strips are vellum before it begins, and the check reports a glyph inside
which some point of a strip's or a cut's line lies more than a pixel deep. An authored overlap
or a region of an unfitted group that glyphs take entirely is a problem: it is to be dropped.

## Profile 4: the guidelines of the font

Profile 4, `data-profile="ink-region 4"`, is profile 3 under the five guidelines of the font of
the manuscript's shapes (decision 31). The system gives a first pass, which a person will
usually tweak, so each guideline is a default that any group or glyph may break. A profile-4
file holds everything a profile-3 file holds, its derivation is profile 3's, and the library
must be of its profile 2. By their short names:

1. **`preserved`:** glyphs only from well-preserved, well-written instances. Each glyph of the
   scribe's in the library carries `data-judged`, below.
2. **`area`:** area preserved where the ink is intact. After stage B a mark's glyph is scaled
   about its centroid, keeping its shape, until its area is that of its written part's draft
   ink, which for a dot gives an ellipse of the ink's area centred on its ink; and every point of
   a letter's outline is moved along the outline's normal there by one distance, at most 1.5
   pixels either way, until the glyph's area is that of its group's draft ink. The normal at a
   point is square to the chord between the outline's points two either side of it. A glyph
   whose draft ink meets the crop's edge, so that the crop may not hold all its ink, is left as
   stage B placed it.
3. **`limbs`:** a letter's limbs follow its ink. Stage B warps a letter through 16 control
   points on a 4-by-4 grid over its glyph's box, each moving at most 25% of its size, at the
   cost of profile 3's warp, so that a limb may shorten or lengthen by up to a quarter of the
   letter's size.
4. **`drawn`:** a mark's glyph is drawn, from the library's drawn shapes below, wherever its
   written part has a shape.
5. **`rafe`:** rafe is a mark of its own, the kind `rafe mark`, HEBREW POINT RAFE, of one written
   part, a drawn bar. Ben's expectations of where a rafe is found, decision 32, are recorded
   there; no rule proposes a rafe that the transcription lacks.

A letter's `data-fit` therefore holds 39 numbers: the move, two scales, turn and shear; the warp
of 32; and the distance along its normal. A mark's holds 6, as in profile 3.

**Breaking a guideline.** A group, `<g class="group">`, or a glyph, `<g class="glyph">`, may
carry `data-break`, which names a guideline by its short name and says why, whose word it is
and when, ending with the two in parentheses, as in `area: the ink has flaked (Claude,
2026-11-03)`; several are separated by `; `. A group's breaks hold for each of its glyphs. A
break is how a tweak to one word is written, alongside the seeds, a glyph's `data-glyph`, a
group's `data-fit="yes"` and Ben's lines. The fit honours each break: `limbs` keeps profile 3's
warp of 9 control points, each moving at most 12%, for which a letter's `data-fit` holds 25
numbers; `area` leaves the glyph as stage B placed it, a letter's distance 0; `drawn` lets a
mark's glyph be Taamey D's; and `preserved` lets a glyph name a glyph of the scribe's that is
not judged well preserved. A break of `rafe` records for one word that a bar where a rafe
would be expected is something else, or the reverse, and changes nothing in the fit.

**Which groups are fitted,** and with which glyphs: as under profile 3, but a kind is fitted
when each of its written parts has a drawn shape or Taamey D's character, so that a tevir, a
stroke and at its left a dot, and a rafe are fitted too. A new glyph takes the first glyph of
the scribe's for its kind and part, in the library's order, that is judged well preserved; or
else the drawn glyph for its part; or else Taamey D's. `regions-fit` moves a file to profile 4.

## The library of glyphs

`glyphs.svg` is the font that this work evolves. It holds one
`<g class="glyph-source" id="…" data-kind="…" data-part="…" data-from="…">` per glyph, with a
`<path class="outline">`, laid out by a derived transform so that the file shows the font when
opened, with each id beneath its glyph. Under `data-profile="glyph-library 1"` its glyphs are of
two sorts, the scribe's from crops' groups and Taamey D's; under `data-profile="glyph-library 2"`,
which the region-SVGs' profile 4 needs, of three, the drawn too, and the scribe's may come from
glyph crops:

1. **The scribe's,** `data-from="<crop> <group>"`: the ink that the crop's draft gives the
   group's regions, traced as a region is, in that crop's pixels; its outline is derived. Only a
   clean letter serves: its ink meets no edge of its crop and touches no other group's ink,
   unless its `data-clean-note` says why it serves even so, and Claude has looked at it beside
   the crop's photograph. Under profile 2 a glyph of the scribe's may instead come from a
   **glyph crop**, `data-from="glyph crop <stem>"`: a small crop of one letter, cut from a page
   image without resampling, as the crops are, and kept as `glyph-crops/<stem>.png` beside the
   library, its stem `<page>-<letter>-<n>`. Its glyph-source records its box in the page image,
   `data-box`; the page image's SHA-256, `data-source-sha256`; a lasso, `data-lasso`, a polygon
   in the glyph crop's pixels that Claude draws round the letter's ink, leaving out every other
   sign's; and the threshold and speck size of its page's line crop, `data-threshold` and
   `data-speck-size`. Its outline is derived: its pixels darker than the threshold, traced by
   level 1's tracer, then the ink of those fills inside the lasso at 3 samples a pixel, traced
   as a region is. The letter's ink may not meet the glyph crop's edge. Under profile 2 every
   glyph of the scribe's carries `data-judged`: that its instance is well preserved and well
   written, judged beside the photograph, ending with who judged it and when in parentheses.
   A glyph that is not so judged carries instead `data-break="preserved: …"`, with why it is
   kept; no new glyph takes it, and a region-SVG's glyph may name it only where that glyph or
   its group breaks `preserved` too.
2. **Taamey D's,** `data-from="Taamey D <Unicode name>"`: the glyph to which
   `Taamey-D/font-m-TaD/Taamey_D.ttf` maps the character, each curve cut into 8 straight
   segments, in font units, y up, which 7 decimals write exactly. They are copied, with the
   font file's SHA-256 on the root, only when `regions-derive` is given `--copy-taamey-d`, so a
   new build of Taamey D changes nothing here until then. A bar is Taamey D's pataḥ and a dot
   its ḥiriq: a qamats is a pataḥ over a ḥiriq, a segol three ḥiriq dots. They stay in the
   library under profile 2, for the kinds whose parts have no drawn shape and for a break of
   `drawn`.
3. **The drawn,** under profile 2, `data-from="drawn <shape>"`: one glyph for each written part
   of each fitted kind whose part has a shape, its outline that shape's in a unit box, y down,
   made by `glyph_library.py` and derived, so that `regions-derive` makes them all afresh, after
   the scribe's and before Taamey D's. The shapes follow Ben's descriptions (decisions 30 and
   31): a **dot**, a circle, for each dot of a vowel, the dagesh, the shuruq, ḥolam, shin and
   sin dots, the dots of sof pasuq and zaqef, the dot of tevir, revia, and a dot under or over
   a letter; a **bar**, a rectangle with rounded ends, lying flat, for pataḥ, the bars of qamats
   and ḥataf pataḥ, maqaf, rafe and a bar under or over a letter; a **stroke**, the same,
   standing, for meteg and silluq, merkha and tipeḥa, which the fit's turn slants, the stroke
   of tevir, and geresh, two of them for gershayim; munaḥ's **bent stroke**, one stroke down
   its right side, round a curved corner and along its foot to the left; and atnaḥ's **inverted
   V**, two strokes meeting in a rounded top. Darga, pashta, qadma, mahapakh and paseq, which Ben
   has not described, keep Taamey D's glyphs until a crop needs one.

A closed table in `py/pen_stroke/glyph_library.py`, keyed by every kind of `level5.py`, gives each
kind's written parts, each part's name, Taamey D's character for it and its drawn shape, and how
a group's regions are matched to its parts: from top to bottom, from right to left, or the bar
first, at the left, and then from top to bottom, as page F043A's line 4 writes its ḥataf pataḥ;
or it says that the kind is not fitted, and why. It has two views: under the region-SVGs'
profile 3 a kind is fitted when each of its parts has Taamey D's character, and under profile 4
when each has a drawn shape or Taamey D's character. A rafe's bar has no character of Taamey
D's in the table. The module raises if its counts and `PARTS` disagree. A new glyph takes the
first of the scribe's glyphs for its kind and part, in the library's order, or else, under
profile 4, its drawn glyph, or else Taamey D's; Claude may name another in its `data-glyph`, and
the fit never chooses by itself.

## The fit

`regions-fit` proposes every glyph's `data-fit`, as Claude proposes seeds; the check never runs
it. `py/pen_stroke/glyph_fit.py` ports the untracked trial of 2026-11-01, `tt_fit.py`, version
3, and gives the trial's parameters exactly from the trial's start and ink. The ink is the
draft's step 1, at 3 samples a pixel, and beyond the crop's edges, to 60 pixels, the page
image's pixels darker than the crop's threshold, which only another word's or line's letter
counts, as its own. The page image is given on the command line and must have the root's
`data-source-sha256`; the root's `data-crop-box` places the crop in it. A letter of the scribe's
starts at its own size, and one of Taamey D's at the size of the subject's letters, the median
over them of their draft ink's height over the height of Taamey D's glyph for their kind; a
letter with its glyph's top and right edge on its draft ink's box's, a mark with its draft ink's
centroid and second moments, and another word's or line's letter with the part of its glyph
that meets the crop's edge over its draft ink. Stage A then moves, scales, turns and shears
each glyph by CMA-ES, seeded, toward its group's draft ink; stage B fits each glyph again
toward the ink nearest it, a letter also warped by a thin-plate spline. The plan's "The fit"
gives the weights and limits, which the module names. Under profile 4 stage B's warp is
guideline 3's, and guideline 2's stage follows it, as "Profile 4: the guidelines of the font"
gives them; the derivation places a letter's glyph by its fit and then moves its outline along
its normal by the distance its `data-fit` ends with.

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
  or that adds no ink;
- under profile 3: a glyph of a group that is not fitted, and a fitted group's written part with
  no glyph or two; a `data-glyph` not in the library, or of another kind or part; a `data-fit`
  of the wrong length for a letter or a mark; a glyph that holds no ink, or inside which a
  strip's or a cut's line lies more than a pixel deep; a glyph's outline that differs from what
  its glyph and its fit give, which after a change to the library's glyph calls for fitting the
  crop again; and a glyph's ink, an overlap of glyphs or a region's ink inside no glyph that
  differs from what the glyphs give. It lists, without failing, each fitted group's
  unexplained ink, by pieces of at least a pixel, and each group that its owner and kind would
  have fitted but that is not;
- under profile 4 also: a library that is not of profile 2; a `data-fit` whose length does not
  suit a letter's breaks; a break that names no guideline, or gives no reason ending with whose
  word it is and when; and, where neither a glyph nor its group breaks the guideline, a mark's
  glyph that is not drawn though its part has a shape, a glyph naming a glyph of the scribe's
  that is not judged well preserved, and a letter's outline moved along its normal by more than
  1.5 pixels, or at all where it breaks `area`. It lists every break, without failing.

`regions-check` also checks the library: its table against the parts rule; that every glyph is
of a fitted kind and one of its written parts; that Taamey D's glyphs cover every such part,
under the font's SHA-256; and that each glyph of the scribe's is the outline its crop's draft
gives, of a clean letter or one whose `data-clean-note` says why it serves. Under profile 2 it
also checks that each glyph crop's PNG is there, of its box's size, and that its outline is
what its lasso, threshold and speck size give; that each drawn glyph's outline is its shape's,
and the drawn glyphs those the table gives, in its order; and that each glyph of the scribe's
carries `data-judged`, ending with who judged it and when, or else a break of `preserved`, and
not both. It never reads the font. `py/tests/test_ink_region_svgs.py` runs the same check in the suite, and fails if the
directory holds no region-SVG or no library. `py/tests/test_glyph_raster.py` checks that the
fit's rasterizer gives exactly what `geometry.rasterize` gives, for every glyph of the library
and of every profile-3 region-SVG.

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
   overlaps' ids;
9. under profile 3, the glyphs' outlines, each a thin grey line, on at first; and, for checking,
   what the glyphs leave of a fitted group's draft, overfill in light grey and unexplained ink
   in black;
10. the groups' ids, in red, each at the middle of its ink, on at first.

Beside each image a legend names each group by its id, its kind and its letter or mark, a mark
on a dotted circle, with its colour in the ink by group: Ben, on 2026-11-01, "I can't answer
your question about g18 because I see that labelled on no image". Under profiles 3 and 4 a
fitted group's ink, in every layer, is its glyphs' ink and the overlaps of its glyphs, an
overlap of glyphs showing the colour of each group that holds it. Under profile 4 the table of
groups gains a column, "Guidelines broken", wherever a group or a glyph of the crop breaks one,
naming each break of a group and of its glyphs with its reason, and the tooltips of the
group's ink and of its glyphs' outlines name them too.

Ink of another word or line is slate in every layer, as decision 17 requires. The colours of the
meanings, the palette of the regions, the teal, the tan and the name and profile of the file are
Claude's choices, which Ben has not yet reviewed.

## Running the tool

From the repository root, with the clone's own environment, as
`./.venv/Scripts/python.exe py/main_pen_stroke.py <subcommand>`.

1. Author a region-SVG's seeds, cuts, strips of vellum, overlaps' outlines, supplied outlines,
   groups and judgments in a vector editor or by hand. A script of Claude's, which the snips
   README describes, re-drafted the six under profile 2.
2. `regions-derive` derives the library's glyphs of the scribe's, from crops and glyph crops,
   and makes its drawn glyphs afresh, and then recomputes every derived part of the region-SVGs
   and reports what the authored parts leave unsettled. With `--copy-taamey-d` it copies Taamey
   D's glyphs into the library afresh. It leaves as it is a fitted file whose glyphs' outlines
   would change, to be fitted again.
3. `regions-fit <region-SVG> --page-image <page image>` fits a crop's glyphs, writes them,
   moves the file to profile 4 and derives it; it needs the library's profile 2. It takes
   minutes, and only the clone that holds the untracked page images can run it. A glyph crop
   is cut from a page image by hand, or by an untracked script of Claude's, without
   resampling; its glyph-source records its box and the page image's SHA-256.
4. `regions-check` reports every way the library and a region-SVG depart from this profile and
   their crops.
5. `regions-render` writes `doc/pen-stroke-snips/regions.html`.

The mega does not run the tool, by Ben's decision of 2026-10-30, which the pen-stroke note's
"Running the tool" quotes. `py/tests/test_mega_coverage.py` declares these subcommands with that
reason. The suite's lint derives every region-SVG again, but nothing checks that `regions.html`
is current, so `regions-render` is rerun by hand after any change.
