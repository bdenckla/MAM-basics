# Plan: regions of ink in place of pen strokes, in the manuscript crops

State: live; proposed 2026-11-01, and Ben answered its three decisions the same day; phases 1
to 3 executed 2026-11-01; phase 4 paused after its first round, 2026-11-01, for the re-draft
that phases 5 to 7 plan, written the same day for Ben's review.

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
- **R9, touching parts are not overlaps** (sections 62 and 63): a qamats's bar and its dot touch
  "only in that the bar touches the dot below it as a tangent to a circle touches a circle.
  I.e., I don't even think this should be coded as an overlap"; and of two letters that level 1
  joins, "I see a thin strip of vellum".
- **R10, overlaps as intersections** (section 63): "I would have expected those shapes to simply
  be the intersection of reasonable shapes for the two (so far I've only seen a two-way
  intersection!) marks in question."
- **R11, supplied vellum** (section 62): for a strip of vellum that level 1's fill covers, "a
  very thin "supplied vellum" (as opposed to "supplied ink") shape".
- **R12, comments that improve the rule** (sections 65 and 66): Ben asked whether his comments
  "inform changes to the generalized algorithm, or are they just the kind of comments that each
  of these transcriptions is expected to need", and chose a re-draft by rule.

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

## The re-draft (Claude's design, for Ben's review)

Planned on 2026-11-01 by Claude (Opus 5.5), in the session that took over the discussion of
phases 1 to 3 and phase 4, after Ben's statements 62 to 66. Phase 2 drafted the regions by a
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

## Constraints

- Downloads and new dependencies need Ben's word first. NumPy, Pillow, potracer and fontTools are
  there; SciPy is not.
- Tracked code never modifies `sys.path`; the untracked scripts in `.novc/` may.
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
