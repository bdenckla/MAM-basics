# Plan: regions of ink in place of pen strokes, in the manuscript crops

State: live; proposed 2026-11-01, and Ben answered its three decisions the same day; phases 1
to 3 executed 2026-11-01; phase 4 paused after its first round, 2026-11-01, for the re-draft
that phases 5 to 7 plan, which Ben approved the same day; phases 5 and 6 executed 2026-11-01;
phase 7 collected Ben's answers to phase 6's sheet; phases 8 to 11, regions from a fitted word,
proposed 2026-11-02 and approved by Ben the same day, which ended phase 7; phase 8 executed
2026-11-02; phases 9 and 10 executed 2026-11-02, in a fresh session; phase 11, Ben's review,
began the same day in another, and his answers led to phases 12 to 16, the font of the
manuscript's shapes, proposed 2026-11-02 for his approval, which will end phase 11.

## Context

Claude-written (Opus 5.5) on 2026-11-01, in the session that took over from round 5 of the
pen-stroke exemplars to discuss its results. Ben's instruction behind it, asked "Shall I write a
plan for regions of ink in place of strokes, for your review?", was his button answer "Yes, write
the plan". His words below are quoted from `.novc/pen-stroke-exemplars/review/` in the
MAM-basics clone `C:/Users/BenDe/GitRepos/MAM-basics`: `ben-statements-2026-11-01.md`, sections
49 to 58, and the earlier files `ben-statements-2026-10-30.md` and `-31.md`. His answers to the
plan's three decisions are sections 56 to 58, under "Ben's decisions" below. Everything else is
Claude's reconstruction and design, which Ben has not reviewed.

The pen-stroke work, in `doc/pen-stroke-representation.md` (the schema note) and
`doc/pen-stroke-exemplars-2026-10-30-update.md` (the findings update), describes six crops of the
Leningrad Codex in `doc/pen-stroke-snips/`, each with a stroke-SVG: level 1, the ink as filled
outlines that potrace traces from the crop's thresholded pixels, with the residual pieces judged;
level 2, strokes of a pen fitted to that ink; and level 5, groups of strokes with a kind and whose
ink they are. Round 5 swept every letter's stroke with one stiff nib per crop. Ben, section 49:
"my basic message is that round 5 seems like incremental improvements on a fundamentally-flawed
system", and "I think a more promising direction is to try to work up from a lower level ink-fill
model (didn't we used to have that as level 1?)". The findings update's entry "Ben's review of
round 5, 2026-11-01" gives his review and a diagnosis of the tav he cited.

Then, section 50: "I really just wonder whether we need a stroke model at all. "Regions of ink"
may be good enough for our purposes." His motivation, in the same message: "to be able to do
things like give different colors to different ink-regions that in some way were semantically
distinct, whether they represented a whole letter, part of a letter, a diacritic, part of a
diacritic, etc." To test that, the session drew both line crops from level 1's ink alone, labelled
by the existing groups, with no stroke drawn: `.novc/pen-stroke-exemplars/review/regions-demo-two-lines.png`,
"Evidence" below. This plan replaces the strokes with regions of ink.

Claude (Opus 5.5) added the fitted word, phases 8 to 11, on 2026-11-02, in the session that the
commander session started on 2026-11-01 to try Ben's section 74 of the same statements file. That
session's trial is untracked; "The fitted word" below gives the design, Evidence items 7 to 11
the trial's figures, and "Ben's decisions", item 6, his instruction. He has not reviewed the
design.

Claude (Opus 5.5) added the font of the manuscript's shapes, phases 12 to 16, on 2026-11-02, in
the session that the commander session started that day for phase 11. Ben asked for it in
sections 80 to 84 of the same statements file, and "Ben's decisions", items 8 to 10, give his
words. He has not reviewed the design.

## Requirements

Each is Ben's, from the statements file named above, and each is active as this plan is written.

- **R1, colour by meaning** (section 50): colour ink that is semantically distinct, at whatever
  granularity an application needs: "a whole letter, part of a letter, a diacritic, part of a
  diacritic, etc."
- **R2, set aside what is not pertinent** (section 50): colour lightly, or remove, marks "not
  pertinent to the discussion of the manuscript, for example marks from another line or even
  invasive/distracting marks like a masorah circle from the line in question". Colouring them
  lightly is "perhaps more "honest" than removing them".
- **R3, a clean page** (section 50): remove "background noise, e.g. all marks we consider
  non-ink", on "a perfect white background (which also makes it abundantly clear that this is a
  synthetic image BTW)".
- **R4, proposed overlaps** (sections 52 and 53): use "color and transparency to illustrate
  proposed overlappings, i.e. proposed explanations of otherwise-perplexing shapes of ink". The
  boundary "can be from human input e.g. a boundary described in words or drawn with a line on
  the image".
- **R5, deflaking** (section 54): "conceptual re-inking flaked regions", where "probably some
  color should be used to show restored sections".
- **R6, granularity by application** (section 51): what a region is does not matter in general,
  but "for any given application, it certainly does matter!"
- **R7, feedback in words, by drawing, or both** (section 57): of boundaries and restorations
  described in words or drawn on a page, "I'd like to be able to give feedback in one or both of
  those forms, for any given crop".

- **R8, the transcription informs the regions** (section 64): "we need to let the Unicode
  transcription "inform" the ink-transcription, in that again, a qamats and its dot should be
  separate regions outside of some really extraordinary circumstance"; and "high-level
  semantics require that there be a cut between the mark above the tav and the tav itself".
- **R9, touching parts are not overlaps** (sections 62, 63 and 69): a qamats's bar and its dot
  touch "only in that the bar touches the dot below it as a tangent to a circle touches a circle.
  I.e., I don't even think this should be coded as an overlap"; and of two letters that level 1
  joins, "I see a thin strip of vellum". Of a geresh and its tav, section 69 asks for "a
  touching-but-not-overlapping pair of regions", since "the marks are perfectly formed by
  themselves", unlike "the dramatic case of the entirely lamed head clearly disappearing into the
  bottom of the mem".
- **R10, overlaps as intersections** (section 63): "I would have expected those shapes to simply
  be the intersection of reasonable shapes for the two (so far I've only seen a two-way
  intersection!) marks in question."
- **R11, supplied vellum** (section 62): for a strip of vellum that level 1's fill covers, "a
  very thin "supplied vellum" (as opposed to "supplied ink") shape".
- **R12, comments that improve the rule** (sections 65 and 66): Ben asked whether his comments
  "inform changes to the generalized algorithm, or are they just the kind of comments that each
  of these transcriptions is expected to need", and chose a re-draft by rule.
- **R13, the shapes of the letters known** (sections 69 and 70): "ultimately we still need some
  sort of stroke model although we were trying to get away from that. We need it for overlaps";
  and, of the boundary between the pe of page F043A's פני and the qamats's bar beside it, "you
  have no model of what a Pe looks like".
- **R14, a typeset word fitted to the ink** (section 74): "drop the typeset version (in some font
  we will hopefully evolve to be a Leningrad-like font) of the word down and distort it based on
  what you find in ink-fills".
- **R15, images label groups** (section 68): "I can't answer your question about g18 because I
  see that labelled on no image. I only see rgN-type images."
- **R16, the manuscript's shapes, not a print's** (sections 80 and 82): "what is our overall
  strategy of developing a font (or font-like information) that corresponds to the Leningrad
  manuscript's shapes for letters and diacritics, rather than Taamey D's?" The marks of the
  merkha, meteg and tipeḥa family "are straight bars, not curved"; atnaḥ is an inverted V; revia
  "is best thought of as a circular dot rather than as a diamond"; geresh will be modelled "as a
  simple bar rather than a curved shape"; and munaḥ is "formed from a single stroke and therefore
  be curved as it makes the transition".
- **R17, the ink-fill refined, not replaced** (section 82): "The idea here was to improve on
  that ink-fill approach, perhaps incorporating it but refining it through the use of
  letter-shapes and diacritic-shapes."
- **R18, only good examples generalize** (section 82): "Only well-preserved, well written
  examples should "generalize"!"
- **R19, area preserved** (section 82): "in cases where we think most or all ink is still
  present, our "shape transcription" should approximately preserve area", a dot transcribed "as
  some kind of ellipse with area equal to the deposited ink and center(s) some how reflecting the
  "centroid" of that ink".
- **R20, guidelines, broken per word** (section 84): "I sort of prefer to call them guidelines
  since I have a feeling we'll often want to break them, at least on a per-word basis"; the system
  is "a fully-automated way to come up with results that will, in most cases, need to be
  human-tweaked".
- **R21, rafe transcribed** (section 82): "we are going to need to transcribe rafeh but of course
  our Unicode sources rarely do so".

## What carries over, and what is parked

The schema note's decisions are numbered 1 to 22. New decisions continue that numbering from 23,
in the new note that phase 1 writes, so that one number names one decision across the work.

1. **Carried over:** 1 (one crop is the unit), 4 (no links to a transcription's coordinates), 6's
   first half (filled outlines with residuals come first), 9 (SVG with a lint), 10 (the crops in
   `doc/pen-stroke-snips/`, Claude doing the tracing), 11 (the levels transcribe the image with
   the text in hand; only level 1 is automated), 13 (the combined transcription is primary), 15
   (supplied marks, never drawn as others are), 17 (whose ink each group is, other lines' ink in a
   colour of its own), 21 (masora circles told apart from the marks that matter) and 22 (likely
   stray ink transcribed and marked so).
2. **Parked with the pen, by Ben's decision 1 below:** 2, 3, 5, 7, 12, 14, 16, 18, 19 and 20,
   which concern the nib, a stroke's widths and ends, heads, bases, the alef's upright and the
   ductus; and the history of the writing that Ben's section 4 framed ("maybe even animations
   showing some sort of abstract representation of the nib drawing it out").
3. **Historical:** 8 (the first crops were the QUPO words).

## Ben's decisions

Ben answered the plan's three decisions on 2026-11-01, after it was pushed in `5be71f6f`.

1. **Regions of ink in place of strokes.** Each crop gets a region-SVG, designed below, and the
   six stroke-SVGs and `doc/pen-stroke-snips/overlays.html` are frozen as a record of the
   pen-stroke work: no further edits, though the suite still checks them. What is given up is the
   pen and the history of the writing, item 2 of the section above. Asked "Adopt regions of ink
   in place of strokes, freezing the stroke files as a record?", Ben answered "Yes, regions"
   (section 56).
2. **Feedback in words, by drawing, or both, for any crop.** Asked "How will you give boundaries
   and restorations?", with the choices of words in the chat and a drawing page, Ben answered:
   "I'd like to be able to give feedback in one or both of those forms, for any given crop"
   (section 57, R7). So at any time and for any crop he may describe a boundary or a restoration
   in words, such as a sentence saying that a qamats's bar runs through a lamed's head and ends at
   its left edge, which the executor turns into a cut or an outline and shows him in context; and
   phase 3 builds the drawing page for all six crops. Claude had recommended words first, with the
   drawing page built only if words proved slow.
3. **Restored ink in a style of its own.** Asked "Draw restored ink in the same hatched orange as
   supplied marks?", Ben answered "A style of its own" (section 58); Claude had recommended one
   style for all added ink. So a supplied mark keeps decision 15's style, hatched in the orange
   `#ff6d00` and outlined with dashes, and restored ink (R5) gets a second reserved style, which
   "The design" proposes for his review.
4. **A re-draft by rule before more hand corrections.** After his first answers to phase 3's
   sheet, asked "Should I write a plan to re-draft all six crops by rule before any more hand
   corrections?", Ben answered "Yes, plan the re-draft" (section 66). Phases 5 to 7 are that
   plan. His comment on Claude's design choices, colour alone for supplied ink, is decision 26
   of `doc/ink-region-representation.md`, made in phase 4.
5. **The re-draft approved.** The revision that added phases 5 to 7 was pushed in `362f2d76`,
   with five design choices put to Ben: regions from seeds by a watershed, with several seeds a
   region and the 2-pixel move to the darkest ink; overlaps as authored outlines; supplied
   vellum as authored lines, with strips proposed by script; the parts rule; and wider
   restoration candidates. Asked "Approve the re-draft plan as written?", Ben answered "Approve
   the plan" (section 67). It is decision 27 of `doc/ink-region-representation.md`.
6. **A plan for regions from a fitted word.** Ben's section 74 proposed a typeset word fitted to
   the ink (R14), and section 75 asked for a try: "Okay go ahead and try this new plan". The
   commander session started a session for it on 2026-11-01, whose untracked trial gave Evidence
   items 7 to 11. Its report recommended glyphs taken from the scribe's own clean letters, with
   Taamey D's only where the library has none. Asked "Should I write the plan for building
   regions from fitted glyphs?", Ben answered on 2026-11-02, by the button labelled with his
   answer, "Yes, write the plan" (section 76). Phases 8 to 11 are that plan.
7. **Phases 8 to 11 approved.** The revision that added them was pushed in `dc3ed1cc`, with
   six design choices put to Ben: profile 3, with the watershed as the draft; the library of
   glyphs, the scribe's clean letters with Taamey D's for the marks; an overlap only where ink
   lies deep inside two glyphs, at a depth that phase 8 sets from his readings; the fit
   proposing and the check never fitting; his lines binding the fit, with Claude's corrections
   of the watershed in page F043A's מתחת dropped; and phase 7 ending on his approval. Asked
   "Approve phases 8 to 11 as written?", Ben answered on 2026-11-02, by the button labelled with
   his answer, "Approve the plan" (section 77). It is decision 29 of
   `doc/ink-region-representation.md`, and his decision 6 is its decision 28.
8. **Drawn marks.** In phase 11 Ben asked for a strategy for a font of the manuscript's shapes
   (R16). Claude recommended a library in which no glyph comes from a print: first the marks,
   drawn to the manuscript's shapes in place of Taamey D's; then every letter the scribe's own,
   from many instances; and later the marks from the scribe's ink too, with Ezra SIL's marks as
   the alternative to the first step. Asked "Should the font's next plan draw the marks to the
   manuscript's shapes?", Ben answered, by the button labelled with his answer, "Yes, drawn
   marks" (section 81). It is decision 30 of the note.
9. **Five guidelines for the font's plan.** After his comments on the fitted crops (sections 82
   and 83), Claude proposed five rules: glyphs only from well-preserved, well-written instances;
   area preserved where the ink is intact; a letter's limbs following its ink; drawn marks, with
   munaḥ one curved stroke and geresh a simple bar; and rafe a mark of its own. Asked "Shall I
   write the font's plan with these five rules?", Ben answered "Yes, write the plan with those
   five rules", and asked that they be called guidelines (R20) (section 84). Phases 12 to 16 are
   that plan. It is decision 31 of the note.
10. **Phase 11's readings.** The dark stroke above the left tav of page F102A's מתחת "is a
    rafeh" (section 84), decision 32 of the note. The light grey's name is Claude's to choose
    (section 84), and Claude keeps "overfill", decision 33. Line 23's lamed's head in page
    F043A's מתחת is placed as the fit with Claude's cut c4 placed it (section 82), decision 34.

## The design (Claude's, for Ben's review)

### Regions, cuts and groups

A **region** is a part of a crop's ink: of level 1's fills judged ink, bounded by their outlines
and by cuts. A **cut** is an authored path of straight segments, drawn across the ink where two
things that a reader tells apart touch, or along the edge of a proposed overlap; it is open, or
closed where one part lies wholly inside another. Most regions need no cut: by the count under
"Evidence", 184 of the six crops' 213 fills judged ink hold the ink of one group only. A
**group** is as now (level 5): a kind from the closed list in `py/pen_stroke/level5.py`,
`data-ink-of`, and a note; it now holds regions instead of strokes. A region in two groups is
shared ink, and that is how an overlap is proposed (R4): the cuts bound the part that two shapes
are proposed to share, and that region belongs to both groups. Granularity (R1, R6) comes from
cutting further only where an application needs it, a letter's head say, and from grouping.

**Supplied ink** extends decision 15 to restorations (R5): an authored closed outline in a group,
with `data-supplied` `no-ink`, `traces` or a new value, `flaked`, for ink restored where the image
shows it has flaked, and `data-supplied-why`. Its added ink is derived: the outline less the ink
the image shows, so supplied ink never claims ink that is there. Candidates for restoration are
level 1's residual pieces judged `damage`, which the snips README defines as "a pale spot where
the ink round it has visibly flaked".

Supplied ink of `no-ink` or `traces` is drawn in decision 15's style. Restored ink, `flaked`,
has a style of its own (Ben's decision 3), which Claude proposes for his review: stippled in the
teal `#00897b` and outlined with dots, never filled solid, never in a group's colour or black,
and in a colour that no other layer of the page uses.

### The region-SVG

`doc/pen-stroke-snips/<crop>.regions.svg`, beside the crop and its frozen stroke-SVG, with these
parts:

1. **The root:** `data-profile="ink-region 1"`, and the stroke-SVG's provenance, threshold,
   tracer, speck size and halo band, copied by script so that no Hebrew is typed. No nib and no
   ductus.
2. **Level 1:** derived exactly as the stroke-SVG's is, by `py/pen_stroke/level1.py`, with the
   judgments carried over by identical pixels, as `py/pen_stroke/derive.py` carries them.
3. **`<g class="cuts">`:** one `<path class="cut" id="cN" d="M … L …" data-note="…"/>` per cut,
   authored, of straight segments.
4. **`<g class="regions">`:** one `<g class="region" id="rN" data-seed="x y">` per region, whose
   id and seed point are authored and whose `<path>`, its outline, is derived.
5. **`<g class="supplied">`:** one `<g class="supplied-ink" id="supN" data-supplied="…"
   data-supplied-why="…">` for each outline of supplied ink, holding the authored `<path
   class="outline">` and its derived `<path class="added">`.
6. **`<g class="groups">`:** as in the stroke-SVG, each member a `<use href="#rN"/>` or
   `<use href="#supN"/>`.

How the regions are derived, every step deterministic:

1. Rasterize the fills judged ink at 3 samples a pixel, so that the ink keeps level 1's smooth
   outlines, as the demo did.
2. Remove every sample that a cut's segments cross, each cut drawn as an 8-connected line of
   samples, so that no 4-connected path crosses it.
3. Take the 4-connected components that remain. Each must hold exactly one region's seed, and
   every seed must lie in one.
4. Give each removed sample back to the adjacent region with the lowest id.
5. Trace each region's samples with level 1's tracer settings and scale the outline to crop
   pixels, to 3 decimal places.

### The check

`check` for region-SVGs reports every departure from the profile:

- level 1 differs from what the crop gives;
- a cut is not a path of straight segments, or crosses no ink;
- a seed lies outside the ink, two seeds share a component, or a component has no seed;
- a derived outline differs from what derivation gives;
- a region or supplied ink belongs to no group;
- a kind or `data-ink-of` value is not on its list;
- supplied ink lacks `data-supplied` or `data-supplied-why`, or adds no ink.

A new lint-shaped test, `py/tests/test_ink_region_svgs.py`, runs that check on every region-SVG,
as `py/tests/test_pen_stroke_svgs.py` does on the stroke-SVGs, and fails if the directory holds
none.

### The page

`doc/pen-stroke-snips/regions.html`, written by `render` for region-SVGs: per crop, its
provenance and transcriptions, and one image with checkboxes beside it that act on that image
alone (Ben, section 16), a size menu, and the photograph drawn smoothly, never as squares (Ben,
section 49). The layers:

1. the photograph, off by default;
2. the ink, black on pure white: R3, and with supplied ink, the page as it would look "if it
   hadn't aged at all and was written on a perfectly clean, white surface" (Ben, section 2);
3. the ink by meaning: the subject's letters black, its marks dark blue, masora circles and stray
   ink a faint violet, other words' and lines' ink a faint tint of decision 17's slate grey (R1,
   R2); on by default;
4. the ink by group, each group in the next of the five colours the overlay page uses,
   translucent, so that a region in two groups shows both (R4);
5. the ink by region, each region a colour of its own, from a palette without decision 15's
   orange, the restored ink's teal or decision 17's slate (R1, R6);
6. supplied ink: a supplied mark in decision 15's style, and restored ink in its own (R5); on by
   default;
7. a checkbox that hides other words' and lines' ink, and one that hides masora circles and stray
   ink: faint by default, hidden by choice (R2);
8. for checking: level 1's fills judged not ink and its residual pieces, and the cuts and seeds.

The colours of layer 3 are Claude's choice, seen in the demo; Ben may change them.

## The re-draft (Claude's design, approved by Ben on 2026-11-01)

Planned on 2026-11-01 by Claude (Opus 5.5), in the session that took over the discussion of
phases 1 to 3 and phase 4, after Ben's statements 62 to 66. Ben approved it as written the same
day, decision 5 under "Ben's decisions". Phase 2 drafted the regions by a
one-off conversion of the frozen strokes, which no new crop will have, so a correction of one of
those drafts improves that file alone. The re-draft makes the regions from what every crop has:
level 1, the photograph's luminance and the Unicode transcription, with seeds that Claude places
by eye with the text in hand (decision 11). What no rule can know, a reading of one image, stays
authored: overlaps, vellum, cuts and groups.

### Profile 2: regions from seeds by a watershed

The root carries `data-profile="ink-region 2"`. What changes from profile 1:

1. **Seeds in every written part.** A sign's written parts are the shapes this manuscript writes
   apart: a qamats is a bar and a dot under it, a segol three dots, a geresh one stroke (R8).
   Each part's ink is a region of its own, and the regions of one sign are joined in the sign's
   group, as now. A region has one seed or more, `data-seed="x1 y1 x2 y2 …"`, each in its part's
   ink. Place one in the part's darkest ink near each place where it touches another part: the
   flood follows the darkest connection, not the letter (Evidence, item 4).
2. **The watershed.** Within each piece of ink, every sample goes to the seed whose flood reaches
   it first. The floods start from all the seeds at once, each from the darkest sample of ink
   within 2 pixels of its seed, and then take the piece's samples in order of the photograph's
   luminance, darkest first, a tie going to the sample reached first. So the boundary between two
   seeds' regions runs along the palest, narrowest line between them, as at the strip of vellum
   between page F043A's pe and nun, or the neck between a qamats's bar and its dot (R9). The
   luminance at a sample is interpolated bilinearly between the centres of the crop's pixels, by
   NumPy, so that it is the same on every machine.
3. **Cuts as corrections.** A cut is optional, authored only where the watershed's line is
   wrong: the flood cannot cross it, and its samples go back afterwards to the adjacent region of
   lowest number, as in profile 1.
4. **Overlaps as authored outlines** (R4, R10). `<g class="overlaps">` holds one
   `<g class="overlap" id="ovN" data-note="…">` per proposed overlap, with an authored closed
   `<path class="outline">`, the intersection of two plausible shapes, and a derived
   `<path class="ink">`, the ink inside it. That ink is taken out of the regions the watershed
   gave and is one region of its own, which two groups or more hold. No region is shared
   otherwise: two parts that touch share nothing unless an overlap is proposed (R9).
5. **Supplied vellum** (R11). `<g class="vellum">` holds one
   `<path class="vellum" id="vN" data-width="…" data-why="…" d="M … L …"/>` per strip: an
   authored line of straight segments and a width in crop pixels, 1 unless stated. The samples
   whose centres lie within half the width of the line leave the ink before anything else, so
   that the strip divides it and shows as vellum in black on white.
6. **The parts rule** (R8). A closed table, keyed by the kinds of `py/pen_stroke/level5.py`,
   gives each kind's number of written parts in this manuscript and raises on a kind it does not
   know. A group whose kind has more than one part holds at least that many regions, overlaps and
   supplied inks, unless its `data-parts-note` says why, for what Ben called "some really
   extraordinary circumstance". Letters, unidentified kinds and set-aside kinds have no count.

The derivation, every step deterministic, at 3 samples a pixel:

1. the ink as level 1 judges it, by profile 1's rule, less every vellum strip;
2. less every cut's samples;
3. the 4-connected pieces of what remains: each holds a seed, every seed lies in one, and a
   crumb, a piece with no seed and no more samples than the speck size, is set aside;
4. each seed moves to the darkest sample of its piece within 2 pixels, the first in row order
   on a tie;
5. the flood, piece by piece, as item 2 above gives it;
6. the cuts' samples and the crumbs go back to the adjacent region of lowest number, round after
   round, as in profile 1;
7. each overlap takes the ink of step 1 inside its outline out of the regions, as one region;
8. each region and each overlap is traced as in profile 1, and supplied ink is derived as there.

The check adds to profile 1's: a seed outside the ink, on a cut or in a vellum strip; an overlap
whose outline is not closed, that takes no ink, or that fewer than two groups hold; a vellum line
not of straight segments, or that takes out no ink; and the parts rule. A piece may hold several
seeds. On the region page an overlap shows in each of its groups' colours, translucent, as a
shared region does now; vellum is drawn in the layer of supplied ink, in colour alone (decision
26), in a light colour no other layer uses, which Claude picks and the representation note
names, for Ben's review.

### What the re-draft keeps, drops and adds

- **Kept:** each crop's level 1 and judgments, its groups with their ids, kinds, owners and
  notes, and its supplied ink.
- **Dropped:** every cut and every region of profile 1, except as the next item says. A region in
  one group lends its seed to the re-draft; a region in two groups, one of phase 2's "pebbles",
  is dropped with its seed.
- **Ben's readings, carried over.** In the crop of page F043A's פני, his cut c11 becomes a vellum
  strip along the same line (section 62), and c12, between the qamats's bar and its dot, stays a
  cut (section 63). In the crop of page F043A's מתחת (section 64): the qamats's dot gets a seed
  of its own; the geresh keeps its region; and the group that the region-SVG calls the top of a
  letter of the verse's last atom, which Ben reads as the "barbed spear tip" of a lamed, becomes
  a lamed letter of the line below, with an overlap where it crosses the base of the mem, whose
  outline Claude draws by eye for Ben's review. The sliver of it that phase 2 gave the atnaḥ,
  sheet question 3, goes to it, since the atnaḥ stands about 12 pixels clear of it.
- **Added by Claude, for Ben's review:** a seed for every written part that the parts rule
  finds without one, and every seed the flood needs near a junction (Evidence, item 4), placed
  by eye; vellum strips proposed by script where the boundary between two signs' regions is
  pale, a strip along it 1 pixel wide wherever the median, over the pairs of 4-adjacent samples
  it separates, of the paler sample's luminance is at least a third of the way from the crop's
  median luminance of ink to its median luminance elsewhere; and restoration candidates, the
  four residual pieces judged damage and every hole in the ink of 30 pixels or fewer, a
  4-connected piece of what is not ink that touches no edge of the crop, whose neighbouring ink
  is all one sign's, other than a set-aside kind's.

## The fitted word (Claude's design, for Ben's review)

Planned on 2026-11-02 by Claude (Opus 5.5), after the trial of Evidence items 7 to 11. Ben asked
for the plan, decision 6, and has not reviewed the design.

Profile 2's watershed knows the ink and its luminance but not the letters, so at a junction its
boundary runs where the ink is palest, not where a letter ends: the downward blob between the pe
and the qamats's bar of page F043A's פני (section 70), the bump on the tav's roof under the geresh
of page F043A's מתחת, and a lamed's head drawn without knowing its shape (section 69). A glyph
knows the shape (R13), without the model of the pen that Ben's decision 1 set aside. So each
written part of a sign gets a glyph, an outline of the part's whole shape, placed at its ink and
fitted to it (R14). A region is the ink inside one sign's glyph, an overlap the ink deep inside
two glyphs, and ink inside none is no sign's. In the trial, glyphs fitted so gave Ben's readings
at the six places he had named in page F043A's two crops, once the letters' glyphs were the
scribe's own.

### Profile 3: regions from fitted glyphs

The root carries `data-profile="ink-region 3"`. A profile-3 file holds everything a profile-2
file holds, and its derivation begins with profile 2's, as the draft. What it adds:

1. **Glyphs.** `<g class="glyphs">` holds one `<g class="glyph" id="glN">` for each written part
   of each fitted group, with `data-group`, its group; `data-part`, empty for a sign of one part
   and otherwise the part's name in the library's closed table; `data-glyph`, its glyph in the
   library; `data-fit`, the fit's parameters; and a derived `<path class="outline">`, the
   library's glyph placed by those parameters, to 3 decimals. The parameters are a move, two
   scales, a turn and a shear, and for a letter a warp of 18 numbers, each to 4 decimals. Only
   the fit writes them: a correction changes what the fit starts from, and the fit runs again.
2. **Which groups are fitted:** every group of the crop's subject, `this-word` or `this-line`,
   whose kind the library's closed table gives glyphs for; and a group of another word or line
   that has `data-fit="yes"`, as line 23's lamed in page F043A's מתחת needs (section 64). The
   table gives none for an unidentified letter or mark, a masora circle or stray ink.
3. **The derivation,** at 3 samples a pixel, after profile 2's steps 1 to 7:
   1. each glyph's outline is rasterized by the nonzero rule;
   2. a 4-connected piece of the ink inside two glyphs or more is an overlap if some sample of it
      lies deeper than D inside each of two of them, a depth that phase 8 sets; otherwise the
      glyphs only touch there (R9), and each of its samples goes to the glyph it lies deepest
      inside, the lower group number and then the earlier part on a tie;
   3. the rest of the ink inside one glyph is that glyph's: a fitted group has one region for
      each written part, and an overlap is one region, which the groups of its glyphs hold, as
      in profile 2;
   4. an unfitted group keeps its draft regions, less the ink inside any glyph;
   5. ink that the draft gave a fitted group but that lies inside no glyph is **overfill** where
      it lies within 1.3 pixels of a glyph: level 1's fill reaching past the sign, such as the
      blur that Ben would not give the qamats's dot of page F043A's פני (section 71). The name
      comes from his "overfilled" (section 62); he left it to Claude, who kept it ("Ben's
      decisions", item 10). Farther from every glyph,
      such ink is unexplained, and the check lists it without failing;
   6. each region, overlap and piece of overfill is traced as in profile 1.
4. **Authored lines.** Ben's lines stay as they are and bind the fit as well: in page F043A's פני,
   the strip v1, from his c11 (section 62), is vellum before the fit begins, and the cut c12
   (section 63) stays. The check reports a glyph that crosses either by more than a pixel. The
   cuts, strips and overlaps that Claude authored to correct the watershed are dropped where the
   glyphs make them unneeded, each named in the execution record. In page F043A's מתחת they are
   the overlap ov1, whose shape Ben called "ridiculous" (section 69), the cut c4 below it, and
   the strip v1 between the geresh and the tav, which he had not asked for (section 69).
5. **The page** adds a layer of the glyphs' outlines, thin; draws overfill in light grey and
   unexplained ink in black, in the layer for checking; and gives every image a legend naming
   each group by its id, its kind and its letter or mark (R15).

### The library of glyphs

`doc/pen-stroke-snips/glyphs.svg`, a new file beside the crops, is the font that this work
evolves (R14). It holds one `<g class="glyph-source" id="…" data-kind="…" data-part="…"
data-from="…">` per glyph, with a `<path class="outline">`, laid out so that the file shows the
font when opened. Its glyphs are of two sorts:

1. **The scribe's letters.** A glyph with `data-from="<crop> <group>"` is the ink of that group's
   regions in that crop, traced as profile 1 traces a region, in that crop's pixels; its outline
   is derived. Only a clean letter serves: its ink touches no other group's ink and no edge of
   its crop, and Claude has looked at it beside the crop's photograph. The trial's four begin
   the library: page F102A's yod, nun and pe, groups g7, g6 and g4 of
   `leningrad-102A-col3-Deut5v6-3L0PNY`; and the lamed of page F043A's line 4, group g32 of
   `leningrad-043A-col2-line4-Ex19v23`, chosen before any fit as that line's lamed with the
   cleanest head. Phase 9 adds one for every other letter kind of the six crops that has a clean
   instance.
2. **Taamey D's,** for every mark, and for a letter that has no glyph of the scribe's: the glyph
   to which `Taamey-D/font-m-TaD/Taamey_D.ttf` maps the kind's character in `KINDS`, read with
   fontTools and flattened, in font units, its `data-from` naming Taamey D and the character's
   Unicode name. These outlines are copied into the library, with the font file's SHA-256, only
   when `regions-derive` is asked to copy them, so a new build of Taamey D changes nothing here
   until then; nothing under `Taamey-D/` changes. A mark of several written parts takes one
   glyph a part, as this manuscript writes it: a bar is Taamey D's pataḥ and a dot its ḥiriq, so
   a qamats is a pataḥ over a ḥiriq, as in the trial, and a segol three ḥiriq dots.

A closed table in `glyph_library.py`, keyed by every kind of `level5.py` and raising on a kind it
does not know, gives each kind's written parts, each part's name and Taamey D's character for it,
or says that the kind is not fitted; the module raises if its counts and `PARTS` disagree.
`regions-fit` gives a new glyph the first of the scribe's glyphs for its kind, in the library's
order, or Taamey D's where the library has none. Claude may name another in its `data-glyph`; the
fit never chooses by itself. A changed glyph of the library calls for fitting again every crop
that uses it, and `regions-check` names those crops.

### The fit

`regions-fit`, a new subcommand, proposes every glyph's `data-fit`, as Claude proposes seeds. The
check never runs it, since a fit takes minutes; the check derives the outlines from the stored
parameters. It ports the trial's `tt_fit.py`, version 3, with its constants:

1. **The ink:** level 1's, less Ben's strips, at 3 samples a pixel; and beyond the crop's edges,
   to 60 pixels, the page image's pixels darker than the crop's threshold, which only another
   line's letter counts, as its own. The page image is given on the command line and must have
   the root's `data-source-sha256`; the root's `data-crop-box` places the crop in it. The page
   images are untracked, under `.novc/pen-stroke-exemplars/sources/`, so only this clone can fit;
   deriving and checking need no page image.
2. **The start.** A letter of the scribe's starts at its own size, and one of Taamey D's at the
   size of the subject's letters, the median over them of their draft ink's height over their
   glyph's; each with its glyph's top and right edge on its draft ink's box's. A mark starts with
   its draft ink's centroid and second moments; a written part of a mark with its draft region,
   the group's regions matched to the table's parts from top to bottom. Another line's letter
   starts with its part inside the crop over its draft ink.
3. **Stage A.** CMA-ES, a seeded evolution strategy written in NumPy, moves, scales, turns and
   shears each glyph to score most: +1 for each sample of its group's draft ink, −0.5 for other
   ink in the crop, −1 for vellum. A letter's scales, turn and shear keep within 0.15 of where
   they start, as logarithms and radians, and a mark's within 0.35; a glyph moves at most 0.3 of
   its size, and at least 3 pixels, and another line's letter 40 pixels.
4. **Stage B.** Each sample of ink goes to the stage-A glyph nearest it, within 10 pixels, and
   each glyph is fitted again on its own: +1 for its own ink, −0.25 for ink that other glyphs or
   unfitted groups hold, −1 for vellum. A letter is also warped, by a thin-plate spline through 9
   control points on a 3-by-3 grid over its glyph's box, each moving at most 12% of the glyph's
   size, at a cost of 0.5 square pixels for each square pixel of movement. A mark is not warped.
5. **Rasterizing,** by the nonzero rule, in a window round each glyph rather than over the whole
   crop, so that a line crop's hundred glyphs fit in minutes. It must give what `rasterize` in
   `py/pen_stroke/geometry.py` gives; the trial's rasterizer differed from it in no sample.

Each stage is seeded, so a fit run twice on one machine gives the same parameters. On another
machine the last digits may differ; the check cannot see that, since it never fits.

## The font of the manuscript's shapes (Claude's design, for Ben's review)

Planned on 2026-11-02 by Claude (Opus 5.5), in phase 11, after Ben's comments on the six fitted
crops. He chose drawn marks and five guidelines ("Ben's decisions", items 8 and 9); he has not
reviewed this design.

Phase 11 found three things that the fit's glyphs got wrong (the execution record, "Phase 11,
2026-11-02"):

1. **Flaked letters generalized.** The library's yod, nun and pe were groups g7, g6 and g4 of
   page F102A's על־פני, whose ink has flaked. They were judged clean but never judged for
   preservation. Page F043A's פני, well preserved, was fitted with them, so its letters took
   their notches and bumps, and the ink they left uncovered, black in the images, is ink that Ben
   reads as legitimate.
2. **A glyph cannot follow a limb shorter than its own.** The warp moves each of 9 control points
   at most 12% of a glyph's size: about 6 pixels for the ḥet of page F043A's מתחת, whose glyph's
   right leg runs 11.9 pixels past the leg's ink and onto the tav's foot. The flag of line 23's
   lamed likewise runs about 3 pixels past its ink.
3. **Taamey D's marks have a print's shapes** (R16).

The system gives a first pass, which a person will usually tweak (R20). So the five guidelines
below are defaults, and any of them may be broken for one word. The derivation of profile 3, its
check, Ben's lines and the drafts stay as they are. The overlap depth D stays 1.5 until phase 14
measures it again, since the three false overlaps of phase 9 involve glyphs that change.

### Breaking a guideline

A group or a glyph may carry `data-break`. It names a guideline by its short name below (`preserved`,
`area`, `limbs`, `drawn` or `rafe`) and says why, whose word it is and when, such as
`data-break="area: the ink has flaked (Claude, 2026-11-03)"`; several are separated by `; `. The
fit and the derivation honour each break. The check lists every break as a note, without
failing, and reports a break that names no guideline or gives no reason. A break is how a tweak
to one word is written, alongside the corrections that already exist: seeds, `data-glyph`,
`data-fit="yes"` and Ben's lines. A tweak is Ben's, in words or by drawing, or Claude's on his
reading.

### Profiles

The region-SVGs move to `data-profile="ink-region 4"`: a letter's `data-fit` holds guideline 3's
warp of 32 numbers and guideline 2's offset, and a group or glyph may carry `data-break`. The
library moves to `data-profile="glyph-library 2"`, with a third sort of glyph, the drawn, and
glyph crops. The reader accepts profiles 3 and 4, so that crops can move one at a time.

### 1. `preserved`: glyphs from well-preserved, well-written instances (R18)

1. Each glyph of the scribe's carries `data-judged`: who judged it, when, and that its instance
   is well preserved and well written, judged beside the photograph. The check requires it.
   Claude judges, and brings to Ben any instance in doubt.
2. The yod, nun and pe of page F102A's על־פני leave the library, and the letters of that crop,
   flaked, are fitted with well-preserved glyphs.
3. **Glyph crops.** A new glyph of the scribe's may come from a small crop of one letter, cut from
   a page image without resampling, as the crops are, and tracked as
   `doc/pen-stroke-snips/glyph-crops/<page>-<kind>-<n>.png`. Its glyph-source records its box in
   the page image and the page image's SHA-256; a lasso, a polygon that Claude draws round the
   letter's ink, leaving out every other sign's; and a threshold, that of its page's line crop.
   Its outline is the ink inside the lasso darker than the threshold, traced as a region is. It is
   derived, so the check derives it again. The README's table of sources gains each glyph crop.
4. A well-preserved letter of a crop may remain its kind's glyph and be fitted with itself, as
   line 4's letters are. A flaked or faded letter is never a glyph.
5. A break, `preserved`, lets a glyph not judged well preserved serve one group, for a kind that
   has no well-preserved instance.

### 2. `area`: area preserved where the ink is intact (R19)

1. A mark's glyph starts as now, from its ink's centroid and second moments. After stage B it is
   scaled about its centroid, keeping its shape, until its area equals the area of its written
   part's draft ink. For a dot, that gives R19's ellipse.
2. A letter's glyph, after stage B, has each point of its outline moved along the outline's normal
   there by one distance, at most 1.5 pixels either way, chosen so that the glyph's area equals
   that of its group's draft ink. The distance is written in `data-fit`.
3. A break, `area`, leaves a group's glyphs as stage B placed them, where its ink has flaked or
   faded, such as most of page F102A's two crops.

### 3. `limbs`: a letter's limbs follow its ink (R17)

1. Stage B's warp moves 16 control points, on a 4-by-4 grid over the glyph's box, each at most 25%
   of the glyph's size, at the same cost for each square pixel of movement. So a limb may shorten
   or lengthen by up to a quarter of the letter's size.
2. A break, `limbs`, keeps phase 8's warp for one glyph: 9 control points, each moving at most
   12%.

### 4. `drawn`: marks drawn to the manuscript's shapes (R16)

1. A third sort of glyph, with `data-from="drawn <shape>"`: an outline that `glyph_library.py`
   makes from a closed table of shapes, each in a unit box, after Ben's descriptions. The fit's
   move, scales, turn and shear give each instance its place, size, proportions and slant:
   1. **a dot,** a circle: each dot of a vowel, the dagesh, the shuruq dot, the ḥolam dot, the
      shin and sin dots, the dots of sof pasuq and zaqef, the dot of tevir, and revia;
   2. **a bar,** a rectangle with rounded ends, lying flat: pataḥ, the bars of qamats and the
      ḥataf vowels, maqaf, rafe, and the bars under or over a letter;
   3. **a stroke,** the same rounded rectangle, standing: meteg and silluq, merkha and tipeḥa,
      which the fit's turn slants, the stroke of tevir, and geresh, two of them for gershayim;
   4. **munaḥ's stroke,** one stroke curving through its corner;
   5. **atnaḥ's inverted V,** two strokes meeting in a rounded top.
2. The closed table names a shape for each written part in place of Taamey D's character. Tevir
   becomes a fitted kind, a stroke and a dot.
3. Darga, pashta, qadma, mahapakh and paseq, which Ben has not described and the six crops do not
   have, keep Taamey D's glyphs until a crop needs one; that shape is then drawn to his
   description. So are the kinds that `level5.py` lacks, when a crop first has one: zarqa a
   shepherd's crook, atnaḥ hafukh a V, and pazer in its manuscript form (section 80).
4. Taamey D's glyphs stay in the library, and a break, `drawn`, may name one for a group.

### 5. `rafe`: rafe a mark of its own (R21)

1. `level5.py` gains the kind `rafe mark`, HEBREW POINT RAFE, of one written part, a drawn bar.
2. Page F102A's מתחת: the dark stroke above its left tav, at x 10 to 38 and y 23 to 30, becomes a
   group of that kind (decision 32 of the note).
3. Ben's expectations, for a later proposal of rafe where the Unicode source has none (section
   82): a letter with a dagesh is not expected to have one, except in very rare cases; on he,
   and rarely alef, without mapiq, rafe "may be somewhat common"; and on ayin and ḥet, never.
   The note records them; this plan builds no model of them.
4. A break, `rafe`, records for one word that a bar where a rafe would be expected is something
   else, or the reverse.

## Evidence, dated 2026-11-01

Measured at MAM-basics commit `c93c6273`. These are dated observations; re-measure them with the
commands given rather than relying on them. Paths under `review/` and `scripts/` are under
`.novc/pen-stroke-exemplars/`.

1. **How many fills hold more than one group's ink**, by
   `./.venv/Scripts/python.exe .novc/pen-stroke-exemplars/scripts/r6_region_census.py <stroke-SVG> ...`,
   which gives each ink sample to the groups of the strokes covering it, or of the strokes within
   3 pixels, and counts a group in a fill from 4 pixels:

   | Crop | Fills judged ink | One group | More than one | None within 3 pixels |
   | --- | --- | --- | --- | --- |
   | `leningrad-043A-col2-Ex20v2-PNY` | 7 | 6 | 1 | 0 |
   | `leningrad-043A-col2-Ex20v3-MFXF` | 15 | 12 | 2 | 1 |
   | `leningrad-102A-col3-Deut5v6-3L0PNY` | 26 | 18 | 5 | 3 |
   | `leningrad-102A-col3-Deut5v7-MFXF` | 22 | 20 | 2 | 0 |
   | `leningrad-043A-col2-line4-Ex19v23` | 73 | 62 | 11 | 0 |
   | `leningrad-102A-col2-line2-Deut4v42` | 70 | 66 | 4 | 0 |

   The 25 fills of more than one group are where cuts are needed: letters of the line above
   touching the subject's letters, a maqaf touching the letters beside it, a vowel touching its
   letter, and two letters touching, as the ayin and the final mem of page F043A's atom העם do.
   The four fills that no group reaches within 3 pixels need a group.
2. **The demo.** `./.venv/Scripts/python.exe .novc/pen-stroke-exemplars/scripts/r6_regions_demo.py <out.png> <stroke-SVG> ...`
   drew `review/regions-demo-two-lines.png`. In both line crops every ink sample lay within 12
   pixels of a stroke, so every one was given a group. It labels by nearest stroke and draws no
   cuts; its boundaries inside the shared fills are the strokes', a draft no one has checked.
3. **The tav of page F102A's atom אחת,** which Ben cited in section 49, is exact in the demo
   because it is level 1's ink. `review/tav-F102A-line2-round5.png` shows its photograph, level
   1's outline and round 5's strokes.

Items 4 to 6 were measured at `acf56d0b`, for the re-draft.

4. **A seeded watershed on Ben's two readings.** Claude's scratch prototypes, not kept, flooded
   the ink of the crop of page F043A's פני, at `acf56d0b`, from the seeds of the regions in one
   group only, with luminance interpolated bilinearly and c11 and c12 ignored. Wherever the
   seeds were, the boundaries lay on Ben's two lines: within 0.44 pixels of c11, median 0.10, and
   within 1.16 pixels of c12, median 0.50. Which side took which ink depended on the seeds. With
   one seed a part, as phase 2 placed them, the qamats's bar took the base of the pe, 999.9
   pixels of ink in all, since the pe's own stroke has a paler stretch than its junction with the
   bar. With each seed moved to the darkest ink within 2 pixels and a second seed for the pe in
   its base, near the bar, the bar held 94.9 pixels and the pe kept its base. Hence profile 2's
   several seeds a region and its 2 pixels. Phase 6 measures it again with the real derivation.
5. **The strip of vellum.** Across c11, the luminance falls to 35 to 50 in the strokes on either
   side and rises to 114, 125, 138 and 164 between them, against the crop's threshold of 142
   (the findings record's update, entry "Ben's first answers on the regions"). In the six crops
   the ink as level 1 judges it has a median luminance of 57 to 66, and the rest 175 to 225; in
   that crop a third of the way from 60 to 219 is 113, below all four values.
6. **The flood is quick.** In pure Python over a heap, the prototype's flood took 0.07 to 0.55
   seconds a crop, over the 29,692 to 212,094 samples of ink a crop holds; SciPy is not needed.

Items 7 to 11 were measured at `b41e71c2`, by the fitted word's untracked trial in
`.novc/pen-stroke-exemplars/typeset-trial/`, whose `README.md` gives the method, every figure,
the images and the commands that rerun it. Phases 8 and 9 measure them again with the tracked
code. Areas are in square crop pixels.

7. **The trial's scripts:** `tt_fit.py`, the fit, which "The fit" above ports; `tt_draw.py`, the
   three panels of each image, the photograph, the fitted glyphs' outlines over it, and what they
   give; and `tt_pny_checks.py`, `tt_contacts.py` and `tt_lamed_stats.py`, the measures below.
   Each fit took two to four minutes; every random draw in it is seeded, so it is deterministic.
8. **Page F043A's פני,** `leningrad-043A-col2-Ex20v2-PNY`, with Taamey D's marks in both runs:

   | Measure | Taamey D's letters | Page F102A's letters |
   | --- | --- | --- |
   | Ink inside the nun's glyph beyond Ben's strip (section 62) | 65.8 | 0.0 |
   | The nun's and the pe's glyphs (section 62) | touch at a corner | apart |
   | The pe's and the qamats's bar's glyphs (section 70) | overlap by 9.6 | touch, no overlap |
   | The qamats's bar's turn | 17.2° | 7.0° |
   | The gap between the qamats's bar and its dot (section 63) | 0.67 px | 0.67 px |
   | Ink inside no glyph and over 1.3 pixels from one | 126.1 | 82.1 |

   In both runs the piece at the crop's foot (section 72) lay inside no glyph. Of the 82.1, 27.6
   lay along Ben's strip and 44.6 at the pe's top.
9. **Page F043A's מתחת,** `leningrad-043A-col2-Ex20v3-MFXF`, in both runs, with Taamey D's glyphs
   throughout and with line 4's g32 as line 23's lamed: the geresh's and the tav's glyphs touch
   and overlap by 2.8 of ink, and the tav's roof is straight under the geresh (section 69). The
   ḥet's and the tav's glyphs overlap by 13.0, and the qamats's bar and dot under the tav by
   10.2; Ben has not been asked about either.
10. **Line 23's lamed in page F043A's מתחת** (sections 64 and 69), as each lamed of page F043A's
    line 4 and as Taamey D's:

    | Glyph | Its top (y) | The ascender's ink outside it | Vellum inside it, crop + beyond | Overlap with the mem |
    | --- | --- | --- | --- | --- |
    | Taamey D's | 78.6 | 138.3 | 22.6 + 135.8 | 0.6 |
    | Line 4's g32 | 75.8 | 22.4 | 18.8 + 40.0 | 4.2 |
    | Line 4's g23 | 76.6 | 45.7 | 4.3 + 43.7 | 5.3 |
    | Line 4's g28 | 74.6 | 20.4 | 7.2 + 41.9 | 7.2 |
    | Line 4's g34 | 74.9 | 30.2 | 11.8 + 54.0 | 4.8 |
    | Line 4's g37 | 72.3 | 32.7 | 9.3 + 65.3 | 16.9 |

    The foot of the mem's base is at about y 81.5, so each lamed letter of line 4 puts its head's
    top 5 to 9 pixels above it, hidden in the mem's ink. A lamed g32 with its ascender lengthened
    along its axis fitted no better than g32 itself. Whether this is the "BIG intersection" of
    section 64 awaits Ben's word.
11. **Where Taamey D departs from the scribe's letters:** its lamed has a thinner ascender and a
    long tail; its nun a much shorter base, which the warp stretched, and a square corner where
    the scribe's is cut away; its pe a thinner right stroke, no downward end to its hook and no
    wedge at its top; its qamats is one T-shaped glyph, which the trial replaced by its pataḥ over
    its ḥiriq; and its geresh has a flag at its top, which the scribe's straight stroke lacks.
    Hence a library that begins with the scribe's letters, and takes the marks from Taamey D.

## Checkout, Git and verification

- **Checkout:** `C:/Users/BenDe/GitRepos/MAM-basics`, a full clone on `main`, for every phase,
  as source, development and integration checkout. Not a worktree: the work reads untracked
  inputs that only this clone holds, the page images under `.novc/pen-stroke-exemplars/sources/`
  (`sefaria-F043A/BIB_LENCDX_F043A.jpg` and `sefaria-F102A/BIB_LENCDX_F102A.jpg`) for sheets with
  page round each crop, and the scripts and statements under `.novc/pen-stroke-exemplars/`.
- **Who may write:** the commander session "Commander for Claude's forests"
  (`local_a80ded65-f78e-4280-8493-9dab3b8c5686`) gives the clone to one writer at a time. Ask it
  by SendMessage before the first Git-impacting change, and release the clone to it once work is
  pushed, the clone is clean and only Ben's answers are awaited. Untracked writes under
  `.novc/pen-stroke-exemplars/` are not Git-impacting.
- **Before editing:** run the user-level "Linked worktrees" checks (`git rev-parse
  --show-toplevel`, `git rev-parse HEAD`, the branch, `git status --porcelain`) and record the
  path and exact `HEAD`. The commit that added this plan must be `HEAD` or its ancestor.
- **Git:** give every Git call `-c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics`, and fetch
  and push with `$env:GIT_SSH_COMMAND = 'ssh -o BatchMode=yes'` and
  `$env:GIT_TERMINAL_PROMPT = '0'`. Commit to `main` by explicit path, fetch, merge a moved
  `origin/main`, and push. The last commit of each push says which checks were skipped and why.
  The executor owns final integration.
- **Interpreter:** `./.venv/Scripts/python.exe`, from the clone's root, for every command.
- **Skills:** load `hebrew-prose` before prose that names a page or a mark, and
  `iterative-document-editing` before editing the findings update or this plan.
- **Verification** (the trial's focused checks, `doc/review-trial.md`; the mega does not run the
  tool, by Ben's decision of 2026-10-30, and no full mega or suite is owed): `git diff --check`;
  Black on every changed Python file; `py/main_pen_stroke.py derive`, `check` and `render`, which
  must leave the six stroke-SVGs and `overlays.html` byte-identical, since any change to them is a
  finding; the new region subcommands; and the ten focused tests with the new one:

  ```powershell
  ./.venv/Scripts/python.exe py/main_test.py py/tests/test_pen_stroke_svgs.py py/tests/test_ink_region_svgs.py py/tests/test_mega_coverage.py py/tests/test_graphviz_version_pin.py py/tests/test_receipt_update_links.py py/tests/test_prose_mark_order.py py/tests/test_h_dot_below_nfc.py py/tests/test_prose_conventions.py py/tests/test_no_machine_paths_in_artifacts.py py/tests/test_tracked_filenames.py py/tests/test_explicit_time_zones.py
  ```

  Stage new files before running the last two, which read tracked files. At `c93c6273` the ten
  without the new test passed 33. At `acf56d0b`, after phase 4's first round, the eleven passed 40.
- **Expected unchanged:** the six stroke-SVGs, `overlays.html`, and every product; nothing outside
  `doc/pen-stroke-snips/`, the tool and its documents reads what changes.
- **Expected changed paths:** a new module or two in `py/pen_stroke/`; `py/main_pen_stroke.py`;
  `py/tests/test_ink_region_svgs.py` (new) and `py/tests/test_mega_coverage.py`;
  `doc/ink-region-representation.md` (new); the schema note's State line and introduction; the
  findings update's dated entries; `doc/pen-stroke-snips/README.md`; the six
  `doc/pen-stroke-snips/*.regions.svg` and `regions.html` (new); and this plan's State line.
- **Phases 8 to 11** run in a fresh session that the commander session starts after Ben approves
  them, and the commit that added them must be `HEAD` or its ancestor. Their focused tests are
  the eleven above with a new one, `py/tests/test_glyph_raster.py`:

  ```powershell
  ./.venv/Scripts/python.exe py/main_test.py py/tests/test_pen_stroke_svgs.py py/tests/test_ink_region_svgs.py py/tests/test_glyph_raster.py py/tests/test_mega_coverage.py py/tests/test_graphviz_version_pin.py py/tests/test_receipt_update_links.py py/tests/test_prose_mark_order.py py/tests/test_h_dot_below_nfc.py py/tests/test_prose_conventions.py py/tests/test_no_machine_paths_in_artifacts.py py/tests/test_tracked_filenames.py py/tests/test_explicit_time_zones.py
  ```

  A fit runs for minutes, so the executor runs `regions-fit` in the background, and stops and
  reports a crop whose fit takes more than 30 minutes. Expected changed:
  `py/pen_stroke/glyph_library.py` and `glyph_fit.py` (new), the three region modules,
  `py/main_pen_stroke.py`, `py/tests/test_ink_region_svgs.py`, `py/tests/test_glyph_raster.py`
  (new) and `py/tests/test_mega_coverage.py`; `doc/pen-stroke-snips/glyphs.svg` (new), the six
  region-SVGs, `regions.html` and the snips README; the representation note; the findings
  record's update; and this plan. Expected unchanged: the six stroke-SVGs, `overlays.html`, every
  product and everything under `Taamey-D/`.
- **Phases 12 to 16** run in a fresh session that the commander session starts after Ben
  approves them, and the commit that added them must be `HEAD` or its ancestor. Their focused
  tests are the twelve above with `py/tests/test_ink_region_glyph_references.py`:

  ```powershell
  ./.venv/Scripts/python.exe py/main_test.py py/tests/test_pen_stroke_svgs.py py/tests/test_ink_region_svgs.py py/tests/test_glyph_raster.py py/tests/test_ink_region_glyph_references.py py/tests/test_mega_coverage.py py/tests/test_graphviz_version_pin.py py/tests/test_receipt_update_links.py py/tests/test_prose_mark_order.py py/tests/test_h_dot_below_nfc.py py/tests/test_prose_conventions.py py/tests/test_no_machine_paths_in_artifacts.py py/tests/test_tracked_filenames.py py/tests/test_explicit_time_zones.py
  ```

  Run each `regions-fit` in the background; a word crop took 0.3 to 0.4 minutes in phase 9 and a
  line crop 1.2, and the finer warp may take longer. Stop and report a crop whose fit takes more
  than 30 minutes. Expected changed: `py/pen_stroke/level5.py`, `glyph_library.py`,
  `glyph_fit.py`, the three region modules and `py/main_pen_stroke.py`; the region tests where
  the new parts need them; `doc/pen-stroke-snips/glyphs.svg`, `glyph-crops/` (new), the six
  region-SVGs, `regions.html` and the snips README; the representation note; the findings
  record's update; and this plan. Expected unchanged: the six stroke-SVGs, `overlays.html`, every
  product and everything under `Taamey-D/`. A new test is differential or lint-shaped only.

## Phases

Each phase ends with its commit pushed and a report to Ben, its commits first.

### Phase 1: the region-SVG and its tool

1. In `py/pen_stroke/`, a module for the region-SVG, reading and writing it as
   `stroke_svg.py` does the stroke-SVG, reusing `level1.py`, `geometry.py`, `raster.py` and
   `level5.py`; the derivation and the check above; and `render` for region-SVGs, reusing
   `render.py`'s checkboxes and script.
2. Subcommands of `py/main_pen_stroke.py`: `regions-derive`, `regions-check` and
   `regions-render`. Declare each in `py/tests/test_mega_coverage.py`'s `NOT_IN_MEGA` with a
   reason in the manner of `_PEN_STROKE_BY_HAND`.
3. The test `py/tests/test_ink_region_svgs.py`.
4. A new note, `doc/ink-region-representation.md`, with `State: live`: the region-SVG as
   "The design" above has it once Ben has reviewed it, the decisions carried over by number, and
   decision 23 on, each quoting Ben, from "Ben's decisions" above. The schema note's
   State line and introduction say that the stroke-SVGs are frozen and where the regions are.
5. Verify and commit. The new test fails while the directory holds no region-SVG, so phase 1's
   commit is pushed together with phase 2's.

### Phase 2: the six crops' region-SVGs, as drafts

An untracked script, `.novc/pen-stroke-exemplars/scripts/r6_migrate.py`, writes each crop's
region-SVG from its stroke-SVG:

1. the root and level 1 copied, and level 1 derived again, which must give the stroke-SVG's
   level 1 exactly;
2. the groups copied, with their ids, kinds, `data-ink-of` and notes;
3. every ink sample labelled by the groups of the strokes whose ink covers it, a sample that two
   groups' strokes cover taking both, or else by the groups of the nearest strokes within 12
   pixels, as `r6_regions_demo.py` reaches them; a fill whose samples all carry one label becomes
   one region, its seed the sample deepest inside it;
4. in a fill whose samples carry more than one label, a draft cut traced along each boundary
   between two labels, from the fill's outline to its outline, or closed where one part lies
   wholly inside another; each simplified to within half a pixel, and an open cut extended a
   pixel beyond the outline at each end; each part given its seed, and a part with two labels a
   region in both groups;
5. the supplied strokes of page F102A's על־פני, s30 and s31, the qamats under its nun, become
   supplied ink with their `data-supplied` and `data-supplied-why`, each outline the outline of
   the stroke's derived ink;
6. no restoration is added; the residual pieces judged `damage` are listed, with their crops and
   places, as candidates for phase 3's sheet.

Then run `regions-derive`, `regions-check` and `regions-render`, and verify, commit and push. The
findings update gets a dated entry with the figures that `regions-check` and the census print,
and the snips README says what the region-SVGs are and how they were made.

### Phase 3: show Ben

1. Give `doc/pen-stroke-snips/regions.html` as a `file:///` link, and open nothing.
2. An untracked sheet, `.novc/pen-stroke-exemplars/review/regions-sheet-1.html`, shows each fill
   that phase 2 cut, 25 by the census's rule: the photograph round it with some page, smooth;
   its draft regions translucent in their groups' colours, with the cuts; the groups named in
   words, each with its letter or mark and its line; and its question beside its image (Ben,
   section 13), asking whether the boundary is right and, if not, where it runs.
3. The same sheet shows each restoration candidate, asking whether to restore it.
4. An untracked drawing page, `.novc/pen-stroke-exemplars/review/draw-regions.html`, for all six
   crops (Ben's decision 2). It shows each crop enlarged and smooth, with its regions and cuts
   drawn over it. Clicks add the points of a cut, or, closed, of an outline of restored ink, and
   each drawn path takes a note. A text box gives every path, with its crop, its points in crop
   pixels and its note, for Ben to paste into the chat. It needs no server and saves nothing by
   itself.
5. Ben answers in words, on the drawing page, or both, for any crop.

### Phase 4: Ben's answers

Record each answer verbatim in the statements file, continuing its numbering, whether it came in
words or from the drawing page; move each cut, add each restoration, regenerate, and show him
each changed place in context. Record findings in
the findings update and decisions in the new note. Verify, commit and push, and release the
clone.

Phase 4 paused after its first round, by Ben's decision 4. The 25 questions of phase 3's sheet
about cuts are superseded by the re-draft; its 4 questions about restoring the pieces judged
damage carry over to phase 6's sheet.

### Phase 5: profile 2 and its tool

Phases 5 and 6 run only after Ben has reviewed "The re-draft" and approved the plan, and the
commit that added phases 5 to 7 must be `HEAD` or its ancestor. Read Ben's statements 49 to 66
first, in `.novc/pen-stroke-exemplars/review/ben-statements-2026-11-01.md`.

1. In `py/pen_stroke/region_svg.py`, `region_derive.py` and `region_render.py`: profile 2 as
   "The re-draft" gives it, the reader accepting `ink-region 2` only; seeds in lists, the
   watershed, overlaps, vellum and the parts rule; the check's additions; and the page's drawing
   of overlaps, vellum and every seed. The watershed is a priority flood over a heap in Python.
2. The parts table, in `level5.py` or a module of its own, with an entry for every kind, each of
   more than one part with a comment naming its parts, and raising on an unknown kind.
3. `doc/ink-region-representation.md` describes profile 2, keeps profile 1 as a paragraph of
   history, and gains the decisions Ben makes in reviewing this plan, from 27.
4. Profile 1's files fail the new reader, so phase 5's commit is pushed with phase 6's, as
   phase 1's was with phase 2's.

### Phase 6: the six crops re-drafted

1. An untracked script, `.novc/pen-stroke-exemplars/scripts/r7_redraft.py`, writes each crop's
   profile-2 region-SVG from its profile-1 file, as "What the re-draft keeps, drops and adds"
   gives it, reading the seeds that Claude adds from an input file beside it and recording what
   it did in `.novc/pen-stroke-exemplars/regions/redraft-<crop>.json`. Never run phase 2's
   `scripts/r6_migrate.py --write` again: it would overwrite Ben's readings.
2. Claude looks at every crop beside its transcription and adds, in that input file, the seeds
   the parts rule asks for and those the flood needs near junctions, then reruns the script and
   checks each crop's regions against the image, until each written part has its own ink.
3. With c11's strip and c12 left out, the watershed's boundaries must lie within 1.5 pixels of
   them, in the crop of page F043A's פני, as Evidence item 4 found; report the distances, and
   stop and report if they do not.
4. `regions-derive`, `regions-check` and `regions-render`; verify as "Checkout, Git and
   verification" gives it, with the eleven focused tests; commit and push with phase 5's work.
   The findings record's update gets a dated entry with the figures, pieces, seeds, regions,
   overlaps, vellum strips and candidates, and with every seed Claude added and why. Expected
   changed: the three region modules, `level5.py` or the parts table's module,
   `py/main_pen_stroke.py` if its help changes, the six `doc/pen-stroke-snips/*.regions.svg`,
   `regions.html`, the representation note, the findings record's update, the snips README and
   this plan's State line and execution record. Expected unchanged: the six stroke-SVGs,
   `overlays.html` and every product.
5. An updated `review/make_regions_sheet.py` writes `review/regions-sheet-2.html`: for each crop,
   the page round it, drawn smoothly, with its regions in their groups' colours, their
   boundaries thin, and each overlap, vellum strip and restoration candidate numbered for a
   question. Its drawing page can also place a seed with its group, and draw an overlap's outline
   or a vellum line.

### Phase 7: Ben's review

As phase 4: each answer recorded verbatim in the statements file, applied, regenerated and shown
in context, findings in the update and decisions in the note. Where an answer is a rule rather
than a reading of one image, Claude says so and proposes how the drafting changes, so that the
next crop needs less of Ben's time (R12).

Phase 7 recorded Ben's sections 68 to 73 on phase 6's sheet, with what each asks for, in an
untracked ledger, `.novc/pen-stroke-exemplars/regions/phase7-ledger-2026-11-01.md`, and applied
none, by his section 73, "Keep collecting". Sections 74 and 75 turned to the fitted word. Phase 7
ends when Ben approves phases 8 to 11, whose first step takes over the ledger's entries; a later
note of his on phase 6's sheet is recorded as before and becomes an input of phase 11.

### Phase 8: profile 3, the library and the fit

Phases 8 to 11 run only after Ben has reviewed "The fitted word" and approved them. Read first
Ben's sections 62 to 76, in `.novc/pen-stroke-exemplars/review/ben-statements-2026-11-01.md`;
phase 7's ledger; `doc/ink-region-representation.md`; and the trial's `README.md` and scripts in
`.novc/pen-stroke-exemplars/typeset-trial/`, the reference for the port.

1. **Phase 7's ledger taken over.** The execution record says, for each of the ledger's entries,
   where this plan meets it: section 68 by R15, in phases 8 to 10; 69 by R9, R13 and profile 3;
   the name of "supplied vellum", sections 69 and 71, by the word phase 10 asks Ben for; 70 and
   71 by profile 3; 72 in phase 9; and 74 by this plan. The ledger is phase 7's record and is
   not edited.
2. **The modules.** In `py/pen_stroke/`: `glyph_library.py`, for the library, its closed table and
   the copying of Taamey D's outlines; `glyph_fit.py`, for the rasterizer, the glyphs' placement
   and warp, CMA-ES and the two stages; and profile 3 in `region_svg.py`, `region_derive.py` and
   `region_render.py`, whose reader accepts `ink-region 2` and `ink-region 3`, so that crops can
   move to profile 3 one at a time. No tracked module reads anything under `.novc/`.
3. **The subcommands.** `regions-fit <crop> --page-image <path>` writes a crop's glyphs and their
   `data-fit`, and moves its file to profile 3. `regions-derive` derives the library's glyphs of
   the scribe's before any crop, and copies Taamey D's glyphs into the library only with
   `--copy-taamey-d`; `regions-check` checks the library and never reads the font. Declare
   `regions-fit` in `py/tests/test_mega_coverage.py`'s `NOT_IN_MEGA`, with
   `_INK_REGION_BY_HAND`.
4. **The library,** with the trial's four glyphs of the scribe's and Taamey D's glyphs for every
   kind the closed table fits, as "The library of glyphs" gives it.
5. **The port checked against the trial.** From the trial's final parameters, in
   `fit-PNY-scribe-v3.json` and `fit-MFXF-scribe-lamed-v3.json` there, the tracked code must give
   the trial's outline of every glyph, to 0.01 pixels, and the score that the trial's `tt_fit.py`
   gives the same parameters; stop and report any difference. Then fit page F043A's two crops
   afresh, to untracked copies, and report every figure of Evidence items 8 to 10 beside the
   trial's.
6. **The depth D.** On those fits, measure each piece of ink inside two glyphs: how deep its
   deepest sample lies inside each glyph. Choose D so that, in page F043A's מתחת, the geresh and
   the tav only touch (section 69) and line 23's lamed overlaps the mem (section 64), and report
   every pair's depths and what D makes of it. If no D does both, stop and report.
7. **The check and the tests.** The check adds: a glyph of an unfitted group, and a fitted group's
   written part without one; a glyph that holds no ink; a `data-glyph` not in the library, or of
   the wrong kind; an outline of a glyph or of the library's scribe's glyphs that differs from its
   derivation; a glyph that crosses one of Ben's lines by more than a pixel; and the closed
   table's counts disagreeing with `PARTS`. It lists unexplained ink, without failing.
   `py/tests/test_ink_region_svgs.py` runs the check on the library too. The new differential
   test, `py/tests/test_glyph_raster.py`, compares the fit's rasterizer with `geometry.rasterize`
   on every glyph of the library and of every region-SVG, and fails if it finds none.
8. **The note.** `doc/ink-region-representation.md` describes profile 3, the library and the
   fit, and gains decision 28, Ben's decision 6 here, with the decisions he makes in reviewing
   this revision.
9. Verify as "Checkout, Git and verification" gives it, commit and push. No crop is at profile 3
   yet: `regions-derive` must leave the six profile-2 region-SVGs byte-identical, and in
   `doc/pen-stroke-snips/` only the new library and `regions.html`, whose images gain their
   legends (R15), change.

### Phase 9: the six crops fitted

1. **Each crop fitted.** For each of the six crops: `regions-fit`, in the background, then
   `regions-derive` and `regions-check`. Claude draws the crop's three panels, as the trial's
   `tt_draw.py` does, by an untracked script that reads the tracked files, and looks at every
   glyph beside the crop's transcription and photograph. Where a glyph is wrong, Claude changes
   what the fit starts from, such as another of the library's glyphs, a new glyph of the
   scribe's, `data-fit="yes"` on another line's letter, or a seed of the draft, and fits again,
   recording each change and why.
2. **The library grows:** a glyph of the scribe's for every letter kind of the six crops that has
   a clean instance, each named in the execution record with its crop, its group and why.
3. **The ledger's places:** in page F043A's פני, the tip at the crop's foot (section 72) gets a
   group of the line below, an unidentified letter with a seed of its own, and the root gets line
   21's text, copied by script; the ledger's entry gives the place.
4. **Ben's readings as checks.** Each figure goes in the execution record, and any that fails
   stops the phase for a report. In page F043A's פני: no ink inside the nun's glyph beyond the
   strip v1 (section 62); the pe's and the nun's glyphs apart (section 62); the qamats's bar and
   dot not overlapping, and within a pixel of each other (section 63); the pe's and the bar's
   glyphs not overlapping (section 70); and the tip at the foot in no glyph of the subject's
   (section 72). In page F043A's מתחת: the geresh and the tav only touching (section 69), and
   line 23's lamed overlapping the mem (section 64).
5. **The figures** in the findings record's update, per crop: its glyphs and which are the
   scribe's, its regions, overlaps, overfill and unexplained ink, and how long its fit took.
6. `regions-render`; verify; commit and push.

### Phase 10: show Ben

A few images, not a sheet, each naming its groups (R15):

1. for each of Ben's places in page F043A's two crops, the three panels, as in the trial;
2. for each of the other four crops, the three panels of the whole crop;
3. `doc/pen-stroke-snips/regions.html`, as a `file:///` link; open nothing.

Ask only what the images answer, each question beside its image: whether the regions are right,
and where not, in words; whether the lamed's head of Evidence item 10 is the "BIG intersection"
of section 64; and what to call overfill.

### Phase 11: Ben's review

As phase 7: each answer recorded verbatim in the statements file, applied, regenerated and shown
in context, findings in the update and decisions in the note. A reading of one image becomes a
change to where the fit starts, or a line of Ben's; a rule becomes a change to the fit or the
library, proposed to Ben first (R12). What the font becomes next, such as glyphs of the scribe's
for marks, several glyphs a kind, or glyphs from other pages, is Ben's to choose after this
phase. He chose during it: drawn marks and five guidelines, which phases 12 to 16 plan, and
whose approval ends this phase.

### Phase 12: the guidelines in the code

Phases 12 to 16 run only after Ben has reviewed "The font of the manuscript's shapes" and
approved them. Read first Ben's sections 80 to 84 of the statements file; the execution record's
"Phase 11, 2026-11-02"; and phase 11's untracked scripts and images in
`.novc/pen-stroke-exemplars/fitted-word/`: `p11_lamed_seeds.py`, `p11_grid.py`, `p11_info.py`,
`fw_draw.py`, `phase10b/` and `phase11/`.

1. **The modules.** Profile 4 and the library's profile 2, as "Profiles" gives them, in
   `region_svg.py`, `region_derive.py`, `region_render.py`, `glyph_library.py` and
   `glyph_fit.py`: `data-break`; `data-judged`; glyph crops; the drawn shapes and the table's
   shape for each written part; guideline 2's stage after stage B; guideline 3's warp; and the
   kind `rafe mark` in `level5.py`, the table and the region page's names of signs.
2. **The check** adds: a glyph of the scribe's without `data-judged`; a glyph crop whose outline
   differs from its derivation, or whose PNG is missing; and a `data-break` that names no
   guideline or gives no reason. It lists every break as a note.
3. **The region page** names each group's breaks in its table and its tooltips.
4. **The note.** `doc/ink-region-representation.md` describes the guidelines, breaks, profile 4
   and the library's three sorts, and holds decisions 30 to 34.
5. Verify as "Checkout, Git and verification" gives it, commit and push. No library glyph that a
   crop uses changes yet: `regions-derive` must leave the six region-SVGs byte-identical, and in
   `doc/pen-stroke-snips/` only `glyphs.svg`, which gains the drawn glyphs, and `regions.html`
   change.

### Phase 13: the library

1. **The drawn glyphs,** made from the table.
2. **The flaked letters out.** The yod, nun and pe of page F102A's על־פני leave the library.
3. **The rest judged.** Each other glyph of the scribe's is looked at again beside its crop's
   photograph and given `data-judged`. Any that Claude doubts goes to Ben, in a report that
   stops the phase.
4. **Glyph crops** for each letter kind of the six crops with no well-preserved, clean glyph: at
   least the pe and the nun, from page F043A; the yod, unless line 4's yod g25 is judged
   well preserved and clean; and the kaf, the shin and the final nun, where page F043A or F102A
   has a clean, well-preserved instance. Claude chooses each by eye beside the page image, as
   phase 9 chose, records each choice and why in the execution record, and adds each to the
   README.
5. **No commit yet.** A changed glyph keeps the check failing for each crop that uses it until
   phase 14 fits that crop again, so phases 13 and 14 are committed together.

### Phase 14: the six crops fitted again

1. **Phase 11's readings.** In page F043A's מתחת, the mem's region rg8 gains five seeds in its
   base, (157.5, 76.5), (162, 78.5), (167, 78.5), (172, 78.5) and (174, 78), as
   `p11_lamed_seeds.py` gives them (decision 34). In page F102A's מתחת, the stroke above the left
   tav becomes a rafe group with a region and a seed of its own (decision 32).
2. **Breaks where the ink has flaked or faded:** `area` on each group whose ink has, chiefly in
   page F102A's two crops, each judged beside the photograph and recorded.
3. **Each crop fitted,** in the background, then derived and checked. Claude draws each crop's
   three panels with `fw_draw.py` and looks at every glyph beside the crop's transcription and
   photograph. A wrong glyph gets a change to where its fit starts, or a break, each recorded
   with its reason.
4. **Ben's readings as checks.** Each figure goes in the execution record, and any that fails
   stops the phase for a report. Phase 9's item 4, for page F043A's two crops. In page F043A's
   מתחת: the ḥet's glyph sharing no ink with the tav's foot, and ending within 1.5 pixels of its
   right leg's ink (section 82); and line 23's lamed overlapping the mem, its figures beside
   those of phase 11's fit with the mem's new seeds, 37.8 pixels of ink, 2.03 deep. In page
   F102A's מתחת: the rafe fitted, and no ink above the left tav unexplained.
5. **The unexplained ink,** each crop's, beside phase 9's, and each piece of a pixel or more in
   page F043A's פני, which Ben reads as legitimate ink (section 82).
6. **The depth D,** measured again as phase 8 measured it. If no D makes the three pairs of phase
   9's item 9 touch while line 23's lamed overlaps the mem, stop and report rather than choose.
7. **The figures** in the findings record's update, as phase 9 gave them; `regions-render`;
   verify; commit phases 13 and 14 together, and push.

### Phase 15: show Ben

As phase 10, a few images, each naming every group (R15): the images of `phase10b/` drawn again
from the new fits; and a sheet of the drawn marks, each beside the scribe's instances of its
kinds in the six crops. Ask only what the images answer.

### Phase 16: Ben's review

As phase 11. What the font becomes next, such as glyphs made from many instances, several glyphs
a kind, or the marks taken from the scribe's ink, is Ben's to choose after this phase.

## Constraints

- Downloads and new dependencies need Ben's word first. NumPy, Pillow, potracer and fontTools are
  there; SciPy is not.
- Tracked code never modifies `sys.path`; the untracked scripts in `.novc/` may.
- Nothing under `Taamey-D/` changes; the library copies outlines from its font.
- The page images stay untracked; only `regions-fit` reads one, from the path that its command
  line gives, after checking its SHA-256.
- Put pointed Hebrew into tracked files only by script from data, never by typing it.
- A new test is differential or lint-shaped only.
- The Yardeni material on MAM-private's branch `research-yardeni-stroke-transcription-20261031`
  stays private (Ben, section 31); this plan needs none of it.
- Ben's "Not now" of section 42, asked whether to draw masora circles faintly, is overtaken for
  the region page by R2, in which section 50 asks for them coloured lightly or removed; the
  frozen stroke views stay as they are.
- Do not create or update Claude auto memory.

## Execution record

Dated entries by the executor, Claude (Opus 5.5), in the session that the commander session
started on 2026-11-01 to execute phases 1 to 3. `doc/ink-region-representation.md` describes
what was built; this records where it departs from the plan above, each a choice of Claude's
that Ben has not reviewed.

### Phase 1, 2026-11-01

1. **A region's id is `rgN`, not `rN`:** level 1's residual pieces already have the ids `rN`.
2. **The ink is level 1's as judged, not the fills judged ink alone:** the fills, less every
   residual piece judged `paper` or `damage`, then with every piece judged ink; a piece judged
   anything else, such as `noise`, leaves the fills as they are. (Phase 1 first took away every
   piece not judged ink, which turned two one-pixel holes judged `noise` into white dots inside
   letters; phase 3's checking found it.) The four
   pieces judged `damage`, phase 2's restoration candidates, are holes that the tracer filled,
   inside the fills, as is the hole judged `paper` inside a masora circle of page F043A's line 4.
   From the fills alone, restored ink could add nothing at the candidates, and the circle would
   be a disc. The 22 specks and faint pieces judged ink, all outside the fills, become regions.
3. **Crumbs:** a piece of ink the cuts leave that holds no seed and no more samples than the
   speck size, which the tracer would drop, goes back to a region as the cuts' samples do,
   rather than needing a seed of its own.
4. **The root's `data-regions-by`** replaces `data-strokes-by`.
5. **A region's groups may disagree on whose ink it is,** as a stroke's may not: ink that two
   lines share is how their collision is proposed.
6. **Shared code made public.** `py/pen_stroke/stroke_svg.py`'s readers and writers of level 1
   and the groups, `derive.py`'s derivation and check of level 1, `render.py`'s stylesheet,
   checkbox script and provenance rows, and a labeller in `raster.py`, are shared with the new
   modules `region_svg.py`, `region_derive.py` and `region_render.py`. Afterwards `derive`,
   `check` and `render` left the six stroke-SVGs and `overlays.html` byte-identical.

### Phase 2, 2026-11-01

1. **`scripts/r6_migrate.py`** wrote the six drafts; `--write` also writes
   `.novc/pen-stroke-exemplars/regions/migrate-<crop>.json`, which records each piece of ink it
   cut, its labels before and after the merging below, its cuts, and the restoration candidates,
   for phase 3's sheet. It is deterministic: run again, it rewrites the same files.
2. **Small parts merged:** in a piece of ink of several labels, each part of one label smaller
   than 4 pixels, the census's figure, first joins the neighbouring part it shares most edge
   with. Without it, every place where two groups' strokes barely touch would be a region.
3. **Cuts end where three parts meet,** as well as at the outline, and all the cuts that meet
   there end at the same point, so that together they divide the ink.
4. **New groups:** ink that no stroke reaches within 12 pixels got groups of its own, and the
   crop of page F043A's מתחת gained the text of the line below; the findings record's update
   gives the places.
5. **The figures** are in the findings record's update, entry "Regions of ink: the six crops'
   drafts". The census gives the table under "Evidence" unchanged, and the drafts cut 25 pieces
   of ink, as many in each crop as the census counts, though not always the same ones.

### Phase 3, 2026-11-01

1. **A fix first.** Drawing a draft's regions beside its crop showed white dots inside two
   letters: one-pixel holes judged `noise`, which phase 1's rule took out of the ink. The rule
   is now the one in phase 1's item 2. The migration, run again, changed only those two regions'
   outlines and seeds, in the region-SVGs of page F102A's two crops of one chanted word, and the
   figures stayed as they were.
2. **The sheet,** `.novc/pen-stroke-exemplars/review/regions-sheet-1.html`, made by
   `review/make_regions_sheet.py` beside it, asks 29 questions, each beside its image: one for
   each of the 25 pieces of ink the drafts cut, whether its boundaries are right and, if not,
   where they run; and one for each of the 4 restoration candidates, whether to restore it.
3. **The drawing page,** `review/draw-regions.html`, made by the same script, covers the six
   crops. Its clicks were checked in the in-app browser: points come out in crop pixels, an
   outline of restored ink closes, and the box gives every path as one JSON line with its crop,
   kind, points and note. The browser there showed it as a snapshot, without the crops' images,
   which load when the file is opened directly.
4. **Ben's answers** are phase 4's input: record each in the statements file, then move the
   cuts, add the restorations, regenerate and show him each change in context.

### Phase 4, 2026-11-01

Entries by Claude (Opus 5.5), in the session that the commander session started on 2026-11-01
for the discussion of phases 1 to 3 and for phase 4.

1. **How answers are applied.** Each is recorded verbatim in
   `.novc/pen-stroke-exemplars/review/ben-statements-2026-11-01.md`, from section 62. Each
   changed place is shown before and after on an untracked page,
   `review/regions-changes-<n>.html`, which `review/make_regions_changes.py` writes from its list
   of changes, with the region-SVGs at a given commit and as they now are.
2. **The first round** applied Ben's answers to question 1, in the crop of page F043A's פני: his
   cut between the pe and the nun, and a cut of Claude's, from his words, between the qamats's
   dot and its bar. The findings record's update, entry "Ben's first answers on the regions",
   gives them.
3. **Statement 61, colour alone,** was made in the same round, as Ben asked, and also in the
   region-SVGs' own style, which this plan did not name, so that a region-SVG opened by itself
   draws supplied ink as the page does.
4. **Cuts without a white band.** The region page drew each cut as a pink line over a white
   band, which Ben read as white space between the regions; it now draws one thin pink line.
   Phase 3's untracked sheet is left as it was, the record of what Ben was asked.
5. **Paused after the first round.** Ben's comments on the crop of page F043A's מתחת, section
   64, are recorded and not applied: the re-draft that phases 5 to 7 plan carries them over.

### Phase 5, 2026-11-01

Entries by Claude (Opus 5.5), in the session that the commander session started on 2026-11-01
to execute phases 5 to 7, from `C:/Users/BenDe/GitRepos/MAM-basics` at `362f2d76`.

1. **The parts table** is `PARTS` in `py/pen_stroke/level5.py`, with `parts_of`, which raises on
   an unknown kind; the module raises if the table and the kinds disagree. The bar and dot under
   or over a letter count one part each, as the shapes they name; an unidentified mark has no
   count. The counts are Claude's, from the signs' usual forms.
2. **`data-parts-note` on a group** is read by `stroke_svg.py`'s shared group reader only when
   the region reader asks for it, and written only when it says something, so a stroke-SVG cannot
   have it. Afterwards `derive`, `check` and `render` left the six stroke-SVGs and
   `overlays.html` byte-identical.
3. **The luminance in whole numbers:** the bilinear value at a sample's centre, multiplied by 9,
   from the crop's pixels by integer arithmetic. A sample takes its pixel's value beyond the
   centres of the edge pixels.
4. **What else the check reports:** a region in two groups, since ink that signs share is an
   overlap; seeds of two regions that move to the same sample; an overlap that shares ink with
   another; and a region whose ink overlaps take entirely.
5. **Vellum on the page** is the ink that a strip takes out, traced when the page is written; the
   profile has no derived part for it, and the file's own style draws the strip's line.
6. **The page** draws every seed, each overlap's outline and each vellum line in the layer of
   cuts, and gives each crop a table of its overlaps, strips and cuts with their notes.

### Phase 6, 2026-11-01

1. **The script,** `scripts/r7_redraft.py`, reads each crop's profile-1 file from Git at
   `362f2d76`, so that it starts from the same files however often it is run, and Claude's
   additions from `scripts/r7_redraft_input.json` beside it; `--write` also writes
   `regions/redraft-<crop>.json`. `scripts/r7_view.py` draws a crop's regions over its
   photograph, which is how Claude checked each crop, and `scripts/r7_distance_check.py` is item
   3's check, whose output is `regions/redraft-distance-check-2026-11-01.txt`.
2. **Seeds joined:** the seeds lent to a letter's group, or to a group whose kind has one written
   part, are joined as one region, of the lowest id among them; those of a group of several
   parts, an unidentified mark or ink set aside stay apart. Without the joining, the watershed
   would draw boundaries inside letters that a reader does not see.
3. **The lamed of page F043A's מתחת** is a new group, g18, not g17, which is the top of the
   alef's diagonal: the findings record's update, entry "Regions of ink re-drafted by rule",
   item 4, gives Claude's reading of the page image. The sliver of g17's ink that the draft gave
   the atnaḥ went back to g17, as "What the re-draft keeps, drops and adds" says, and a cut of
   Claude's, c4, divides the mem's base from the lamed's ascender below the overlap ov1.
4. **One proposed strip set aside,** in page F102A's מתחת, where it would have left a mark's ink
   without a seed; the input file's `no-vellum` names it, with why.
5. **Item 3's check passed:** at most 0.44 and 1.16 pixels from Ben's two lines, the prototype's
   figures.
6. **Item 5, the sheet,** comes after this commit: `review/regions-sheet-2.html` and the drawing
   page are untracked.

### Phase 8, 2026-11-02

Entries by Claude (Opus 5.5), in the session that the commander session started on 2026-11-02
to execute phases 8 to 11, from `C:/Users/BenDe/GitRepos/MAM-basics` at `24a393d4`, of which
`dc3ed1cc` is an ancestor. Its untracked scripts and outputs are in
`.novc/pen-stroke-exemplars/fitted-word/`.

1. **Phase 7's ledger taken over** (item 1), unedited: section 68, that images label groups,
   is met by R15, in the region page's legend and layer of group ids and in the images of phases
   9 and 10; section 69's touching marks, the bump on the tav's roof and the lamed's head, by R9,
   R13 and profile 3; the name of "supplied vellum", sections 69 and 71, by the word phase 10
   asks Ben for; sections 70 and 71, the pe, the qamats's bar and its dot of page F043A's פני, by
   profile 3; section 72, the tip at that crop's foot, in phase 9, item 3; and section 74 by
   this plan.
2. **The port checked against the trial** (item 5), by `fw_port_check.py`. From the trial's
   final parameters in `fit-PNY-scribe-v3.json` and `fit-MFXF-scribe-lamed-v3.json`, the
   tracked placement gives each of the 24 glyphs' outlines within 0.0054 pixels of the trial's,
   each start exactly, and, with the trial's weights of stage A, exactly the score that the
   trial's objective gives. Given the trial's ink, starts and glyphs, the tracked fit gives the
   trial's parameters, to 4 decimals, for all 24, in 0.2 and 0.3 minutes against the trial's 2
   to 4; its output is `port-rerun-PNY.txt` and `port-rerun-MFXF.txt`.
3. **The fresh fits** (item 5), to untracked copies in `phase8/`, each in 0.2 minutes, with
   Claude's ov1, c4 and v1 dropped from the copy of page F043A's מתחת and line 23's lamed, g18,
   given `data-fit="yes"`, as profile 3's item 4 says. By the trial's definitions
   (`fw_figures.py`, output `phase8/figures-*.txt`), the trial's figure in brackets:
   - page F043A's פני: ink inside the nun's glyph beyond Ben's strip 0.0 (0.0); the nun's and
     the pe's glyphs apart (apart); the pe's and the qamats's bar's glyphs touch with no overlap
     (the same); the bar turned 7.0° (7.0°); the bar and its dot 0.67 pixels apart (0.67); ink
     inside no glyph and over 1.3 pixels from one 84.8 (82.1), of which 44.6 at the pe's top
     (44.6) and 31.7 along Ben's strip (27.6); the tip at the crop's foot in no glyph (no
     glyph). The fit departs from the trial's only in the nun's stage B: Ben's strip is now
     vellum.
   - page F043A's מתחת: the geresh's and the tav's glyphs overlap on ink by 2.9 (2.8), the ḥet's
     and the tav's by 13.9 (13.0), and the qamats's bar's and dot's by 10.2 (10.2).
   - line 23's lamed: its top at y 65.5 (75.8); its ascender's ink outside it 57.4 (22.4); the
     vellum inside it 22.3 in the crop and 74.4 beyond (18.8 and 40.0); its overlap with the mem
     on ink 129.9 (4.2).
4. **Without c4, line 23's lamed rises into the mem,** a finding (`fw_lamed_draft.py`). Without
   Claude's cut c4 the watershed gives the lamed's draft region 652.2 pixels, reaching up to y
   65 into the dark ink where it meets the mem's base, against 353.1 from y 81.7 with c4, so
   the fit starts the lamed there and its head ends 10 pixels higher than the trial's, deep in
   that dark ink, which may be the "BIG intersection" of section 64. But its hook covers vellum,
   and the dark ink below it, 33.6 pixels at x 160.7 to 166.3 and y 84.3 to 91.3, is
   unexplained (`phase8/MFXF-lamed-head-fresh.png`). Profile 3's item 4 counts c4 among the
   corrections that the glyphs make unneeded; here they do not, and phase 9 decides with the
   images whether c4 stays.
5. **D is 1.5 pixels** (item 6), `OVERLAP_DEPTH` in `py/pen_stroke/region_derive.py`. Each
   piece of ink inside two glyphs of the fresh fits, by the depth of its sample deepest inside
   both, inside the shallower of the two: in page F043A's מתחת, the geresh and the tav 0.64;
   the ḥet and the tav 0.90, 0.20 and 0.05; the qamats's bar and its dot 1.04; line 23's lamed
   and the mem 4.80. In page F043A's פני, the pataḥ and the bar of the qamats under the nun,
   three pieces of 0.10 to 0.17. So D makes the lamed and the mem an overlap and every other
   pair touch, as Ben's readings ask of the geresh and the tav (section 69) and of a qamats
   (sections 63 and 64). On the trial's fit, with c4, the lamed's head only grazes the mem,
   0.35, less than the geresh's 0.68: there no D gives both readings, so D rests on item 4's
   fit.
6. **Two of the trial's letters are not clean,** a finding. Page F102A's pe, g4, touches its own
   dagesh, g5, for 20 samples, and line 4's lamed g32 touches the shin of the line above, g13,
   for 22 samples, where their drafts' watersheds divide them. Since this plan names both, each
   has a `data-clean-note` of Claude's that says so, which the check accepts; the yod and the
   nun are clean.
7. **Choices of Claude's that the plan does not make:**
   - a glyph of the scribe's is the ink that its crop's draft gives its group, so that fitting
     that crop again does not change the library;
   - a profile-3 region's derived outline is its draft ink less every glyph's, so that a fitted
     group's regions hold what its glyphs leave, overfill and unexplained ink, which the check
     and the page tell apart by their distance from the glyphs; overfill is not stored apart;
   - "within 1.3 pixels" is the trial's 4 samples in 8-connected steps; a sample's depth is its
     distance from the glyph's outline, and a piece is an overlap when one sample lies deeper
     than D inside each of two glyphs;
   - every strip and cut that a profile-3 file keeps binds the fit, and a glyph crosses one by
     more than a pixel when some point of its line lies more than a pixel inside the glyph;
   - the subject's letters' size is the median of their draft ink's heights over the heights of
     Taamey D's glyphs for their kinds, whichever glyph each is fitted with, which for letters
     all of Taamey D's is the trial's;
   - another word's or line's letter starts with the part of its glyph that meets the crop's
     edge over its ink: its top for the line below, as in the trial, its bottom for the line
     above, its side for another word;
   - the table matches the parts of a tsere, a segol and a gershayim from right to left, a ḥataf
     pataḥ's bar first, at the right, and then its dots from top to bottom, and every other
     kind's from top to bottom; a sheva's, a sof pasuq's and a zaqef's dots are ḥiriq dots; a
     tevir is not fitted, since Taamey D has no character for its stroke alone;
   - a group with no region of draft ink for each written part, such as the supplied qamats
     under the nun of page F102A's על־פני, is not fitted, and the check says so without failing;
   - `regions-derive` leaves unwritten a profile-3 file whose glyphs' outlines would change, so
     that a changed glyph of the library keeps the check failing until the crop is fitted again;
   - the fit counts a glyph's samples in a window round it, which gives the whole grid's sums
     exactly;
   - the region page draws the groups' ids on each image, a layer on at first, beside the
     legend.
8. **Paths beyond the plan's list:** `py/pen_stroke/stroke_svg.py`, whose shared reader and
   writer of groups carry a group's `data-fit`, and `py/tests/test_graphviz_version_pin.py`,
   which declares the library a hand-made SVG. Afterwards `derive`, `check` and `render` left
   the six stroke-SVGs and `overlays.html` byte-identical, and `regions-derive` left the six
   profile-2 region-SVGs so.
9. **Phases 9 to 11 run in a fresh session,** since this session's context passed half; it wrote
   the prompt for the commander session.

### Phase 9, 2026-11-02

Entries by Claude (Opus 5.5), in the session that the commander session started on 2026-11-02
to execute phases 9 to 11, from `C:/Users/BenDe/GitRepos/MAM-basics` at `a411c507`, of which
`f9630ff0` is an ancestor. Its untracked scripts, logs and images are in
`.novc/pen-stroke-exemplars/fitted-word/`, the scripts named `p9_*.py` and the rest in `phase9/`.

1. **The drafts changed before the library grew** (`p9_drafts.py`), so that each crop was fitted
   with the glyphs it keeps:
   - in page F043A's פני, the tip at the crop's foot (item 3) left the silluq's region rg12 for a
     region rg16 and a group g10 of its own, an unidentified letter of the line below, and the
     root gained line 21's text, the UXLC's atom 6 of Exodus 20:4, copied by script from round
     3's extract; in the page image the tip is the top of that atom's first letter;
   - in page F043A's מתחת, Claude's ov1, c4 and v1 were dropped, as profile 3's item 4 says, and
     line 23's lamed, g18, has `data-fit="yes"`;
   - in page F102A's על־פני, the script's strips v3, between the maqaf and the pe, and v4,
     between the nun and the yod, were dropped. Claude reads "dropped where the glyphs make them
     unneeded" as dropped where both signs a strip divides are fitted, since their glyphs then
     divide the ink there. The other strips of the script's, line 4's v1 to v3, line 2's v1 and
     page F102A's v1 and v2, each divide ink of which one side at least is not fitted, and are
     kept. Ben's v1 and c12 in page F043A's פני are kept.
2. **The library grew by nine glyphs of the scribe's** (item 2, `p9_library.py`), one for each
   letter kind of the six crops with a clean instance and no glyph yet. Claude chose each by eye,
   beside the photograph, as complete and typical, and between equals took page F043A's line 4,
   the page of the two crops Ben has read:
   - from line 4, `leningrad-043A-col2-line4-Ex19v23`: the alef g36, since g24's diagonal is pale
     at its top; the he g29, the vav g26, the ayin g33, the resh g39 and the tav g35, each over
     line 2's equal; the tav also over g1 of page F043A's מתחת, a crop of Ben's readings;
   - from line 2, `leningrad-102A-col2-line2-Deut4v42`: the ḥet g32, since g19's left leg thins;
     and the mem g21 and the final mem g27, the only clean ones;
   - page F102A's מתחת has a clean tav and ḥet, g1 and g2, both badly flaked, and page F043A's
     מתחת a clean vav, g16, only a sliver of another word's vav at the crop's edge: none serves.
   The kaf, the shin and the final nun have no clean instance, so they keep Taamey D's glyphs.
   Dropping v3 and v4 left three of the trial's letters touching another sign where the
   watershed divides them: the nun and the yod each other, for 14 samples at x 69.3 to 74, y 75
   to 76, and the pe the maqaf, for 19 samples, besides its dagesh. Their `data-clean-note`s say
   so, and the ink of the yod, the nun and the pe grew by 2.8, 2.1 and 3.4 pixels.
3. **The fits** (item 1), all run before any was looked at, six at once and later three at once,
   so their times are longer than one fit alone takes: page F043A's פני 0.3 minutes and מתחת
   0.4, page F102A's על־פני 0.4 and מתחת 0.3, line 4 1.2 and line 2 1.1. No fit came near 30
   minutes.
4. **Corrections of the drafts that the fits showed** (`p9_drafts2.py`), each crop then fitted
   again:
   - line 4's atom העם: the ayin g30 had a seed in its left arm only, so the watershed gave its
     right arm and base to the final mem g31, whose glyph the fit then put on the ayin, and the
     ayin's on the final mem, leaving 679.4 pixels of the final mem's draft unexplained. Its
     region rg72 gained seeds in the right arm, where it meets the base, along the base, and
     near where the base touches the final mem; afterwards each glyph lies on its letter, and
     4.6 pixels of the ayin's ink are unexplained;
   - line 2's qamats g50 held a third region, rg84, the top of a letter of line 3 that the crop's
     foot cuts, so the qamats was not fitted; rg84 is now a group of the line below, g65, and
     the qamats is fitted;
   - page F102A's על־פני: the pe's qamats g8 had one seed in the faint left end of its bar and
     the other in the rest of the bar, which also took the dot, so the fit put the bar's glyph
     on the faint end and stretched the dot's over the bar, and left the dot unexplained. The
     bar's region rg30 now has both seeds in the bar and rg31 one in the dot; afterwards 8.6
     pixels at the bar's faint left end are unexplained.
5. **A glyph named in place of the library's first:** page F102A's מתחת's ḥet g2 is fitted with
   Taamey D's ḥet. That ḥet is flaked and about 33 pixels wide, against 46 for line 2's g32,
   and the fit's limit of 0.15 on a scale lets the scribe's ḥet shrink only to about 40, so its
   glyph took the left tav's right leg as an overlap of glyphs, and 91.3 pixels of the ḥet's
   ink were unexplained. With Taamey D's, 68.9 are, but its right leg reaches the right tav's
   foot, item 9.
6. **A ḥataf pataḥ's bar is matched at the left of its dots.** Phase 8's table matched the
   rightmost region of a ḥataf pataḥ to its bar, but the only one in the six crops, under line
   4's ayin of the atom לעלת, writes its two dots at the right of the bar; so the fit put a
   dot's glyph on the bar and the bar's on a dot. `glyph_library.py` and `region_derive.py` now
   take the leftmost region as the bar, and line 4 was fitted again; afterwards each glyph lies
   on its own part, and none of the sign's ink is unexplained.
7. **Ben's readings as checks** (item 4) all hold, by `p9_figures.py`, whose output is
   `phase9/figures-final.txt`. Page F043A's פני: no ink inside the nun's glyph beyond the strip
   v1, 0.0 pixels; the pe's and the nun's glyphs apart; the qamats's bar and dot apart, 0.67
   pixels from each other; the pe's and the bar's glyphs touching with no overlap; and the tip at
   the foot in no glyph. Page F043A's מתחת: the geresh's and the tav's glyphs share 1.7 pixels of
   ink, whose sample deepest inside both lies 0.50 pixels inside the shallower, so they only
   touch; and line 23's lamed overlaps the mem, 214.2 pixels of ink, 6.59 pixels deep.
8. **Without c4 and with it,** for phase 10 to show. An untracked copy of page F043A's
   מתחת with c4 kept, `phase9/c4/`, fitted the same way: the lamed's head overlaps the mem by
   41.0 pixels of ink, 2.16 deep, its glyph crosses c4 by 4.68 pixels, which the check reports,
   and no ink below the head is unexplained. Without c4, as the tracked file has it, the head
   lies far deeper in the mem's base, and 30.4 pixels of dark ink below it, at x 160.7 to
   166.7, y 85.7 to 91.3, are unexplained. Both are overlaps at D = 1.5.
9. **Overlaps of glyphs where the signs only touch,** a finding. At D = 1.5 three pairs of signs
   that only touch, by Ben's sections 63, 64 and 69, are overlaps: line 4's lamed g37 and
   maqaf g64 in the chanted word אל־הר, the maqaf wholly inside the library's lamed's hook,
   30.2 pixels of ink, 2.39 deep; page F102A's מתחת's ḥet g2 and tav g3, 37.2 pixels, 2.71
   deep; and that crop's qamats g13, its bar and dot, 26.1 pixels, 1.82 deep. A D above 2.71
   would make all three touch and keep the overlap of the fit without c4, 6.59, but would make
   the fit with c4 a touch, 2.16. So D rests on the fit without c4: no D both makes the three
   touch and keeps the fit with c4 an overlap. A second glyph of a kind, such as a lamed with a
   smaller hook, is for Ben to choose after phase 11.
10. **Unexplained ink of note,** each listed by the check: line 4's kaf, Taamey D's, 124.1
   pixels along the top of its roof; page F043A's פני's pe, 45.7 pixels at its top, as in phase
   8; page F102A's מתחת's left tav g1, 134.2 pixels at x 10 to 38, y 23 to 30, a dark stroke
   above the roof that no glyph explains, which is the roof or a mark of its own by Ben's reading,
   not Claude's; and line 2's alef g29, 51.2 pixels in four pieces, and lamed g30, 31.9.
11. **Groups not fitted:** page F102A's על־פני's g10, the supplied qamats under
    the nun, which holds no region with ink, and line 2's tevir g46, which the table does not
    fit; and, by the table, every masora circle, stray mark and unidentified letter or mark.
12. **The figures** (item 5) are in the findings record's update, entry "Regions from a fitted
    word: the six crops fitted". Afterwards `derive`, `check` and `render` left the six
    stroke-SVGs and `overlays.html` byte-identical, and `regions-check` found no problem in the
    library or the six crops.

### Phase 11, 2026-11-02

Entries by Claude (Opus 5.5), in the session that the commander session started on 2026-11-02
for phase 11, from `C:/Users/BenDe/GitRepos/MAM-basics` at `15f87bfb`, of which `f954b526` is an
ancestor. Its untracked scripts and images are in `.novc/pen-stroke-exemplars/fitted-word/`: the
scripts named `p11_*.py`, `fw_draw.py` as changed, and the images in `phase10b/` and `phase11/`.
Ben's words are sections 80 to 84 of the statements file.

1. **Phase 10's images named only the fitted groups.** Before showing them again, the session
   found that they left unnamed every group not fitted: masora circles, line 2's tevir g46, stray
   marks and other lines' ink. It also found that a legend line of page F102A's מתחת ran past its
   image's edge. `fw_draw.py` now names every group and widens an image to its legend and title,
   and `phase10b/` holds the eight images drawn again, their fits unchanged (R15).
2. **Ben commented on the images rather than answering phase 10's questions** (section 80), and
   asked first for a strategy for a font of the manuscript's shapes. He chose drawn marks
   (section 81).
3. **The library's yod, nun and pe were flaked,** a finding (section 82). They are groups g7, g6
   and g4 of page F102A's על־פני, the trial's, chosen as clean but never judged for preservation.
   Page F043A's פני was fitted with them, so its letters took their notches and bumps, and the ink
   that they left uncovered, black in the images, is ink that Ben reads as legitimate. Page
   F102A's letters were fitted with themselves, and follow its flaking.
4. **Line 23's lamed, as Ben preferred** (section 82): the fit with Claude's cut c4, whose head
   overlaps the mem far less than the fit without it. An untracked copy of page F043A's מתחת
   without c4, its mem's region rg8 given five seeds in the dark ink of its base
   (`p11_lamed_seeds.py`, `phase11/lamed-seeds/`), gave the lamed a draft from y 79.3, 376.3
   pixels, against c4's from y 81.7, 353.1. Fitted in 0.3 minutes, its head overlaps the mem by
   37.8 pixels of ink, 2.03 deep, against 41.0 and 2.16 with c4. The check finds no problem, and
   the crop's unexplained ink is 4.4 pixels, against 35.6 in the tracked file. Its image is
   `phase11/p11-1-F043A-MFXF-lamed-seeds.png`. Phase 14 applies the seeds.
5. **The ḥet's right leg in page F043A's מתחת** (section 82). The draft already has the vellum
   that Ben sees: rows y 61 to 64, at x 91 to 97, between the leg's ink, which ends at y 60, and
   the tav's foot (`p11_grid.py`). The glyph, line 2's ḥet g32, has legs of equal length. The
   warp can shorten the right leg by about 6 pixels, against the 11.9 needed, so the leg runs
   onto the tav's foot, the two glyphs sharing 7.9 pixels of its ink, 1.17 deep. No line of Ben's
   is needed; guideline 3 of "The font of the manuscript's shapes" is the remedy.
6. **Ben's approvals** (sections 82 and 83): in page F043A's מתחת, the geresh kept apart from the
   tav, and the qamats's large dot with its bar; the ayin of page F102A's על־פני; line 2's lamed
   g30 leaving unexplained a piece of ink that he calls a "booger"; and line 2's alef g18.
7. **Ben's answers** (section 84): the dark stroke above the left tav of page F102A's מתחת, which
   phase 9's item 10 left unexplained, is a rafe; the name of overfill is Claude's to choose, and
   it stays "overfill", which no other file of the repository uses; and the font's plan, with
   five guidelines. Phases 12 to 16 were written on 2026-11-02 for his approval.
8. **Not answered:** phase 10's questions on whether each crop's regions are right, beyond his
   comments; and D, which waits for phase 14.
