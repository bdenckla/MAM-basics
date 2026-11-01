# Plan: regions of ink in place of pen strokes, in the manuscript crops

State: live; proposed 2026-11-01, and Ben answered its three decisions the same day; phases 1
to 3 executed 2026-11-01; phase 4 awaits Ben's answers to phase 3's sheet.

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
  without the new test passed 33.
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
