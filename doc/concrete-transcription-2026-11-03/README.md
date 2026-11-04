# Concrete transcription trial, UXLC change 2023.03.25-112

Claude (Opus 5.5), 2026-11-03, in the session that the commander session
"Commander for Claude's forests" (`local_a80ded65-f78e-4280-8493-9dab3b8c5686`) started for it.
Ben's instruction, quoted in the commander's brief
(`C:/Users/BenDe/GitRepos/MAM-basics/.novc/commander-session/concrete-transcription-brief-2026-11-03.md`):
see whether the paused ink-region work can, with his considerable manual help, transcribe
concretely the image of that change, including a stroke that starts within the resh, passes
through the nun and belongs to no letter or diacritic. `doc/PLAN-ink-regions.md` stays paused.

## Tracked since 2026-11-04

Ben asked on 2026-11-04: "How can we wrap up this work for the time being, getting this session
ready to archive by saving whatever needs to be saved in a git-tracked fashion?" Until then the
trial's files were untracked, in `.novc/concrete-transcription-2026-11-03/` of the clone
`C:/Users/BenDe/GitRepos2/MAM-basics`. Now:

1. **Tracked in this directory:** this README; `download-image/112-Detail.jpg`, the trial's one
   input, with its fetch record, under the terms that `DATA-LICENSES.md` gives it; and
   `edits/ben-edits-1.json`, Ben's edits of draft 1. Later the same day the production images
   joined them, in `production/`: the last section.
2. **Tracked as code:** the scripts, each `ct_….py` that this README names, are the package
   `py/concrete_transcription/`, with the two page templates beside them, and one program,
   `py/main_concrete_transcription.py`, runs them: each script is the subcommand of its name
   without `ct_`, and `ct_edges_chart.py` is `edges-chart`. They changed only in how they are
   run, their imports no longer changing `sys.path` and their arguments parsed by the program;
   in their docstrings' first lines and usage; in Black's formatting; and in how they find
   files, the repository's root by `mb_cmn.paths` and Ben's edits in this directory. The two
   templates changed only in their caveat, after the check that the move changed no output.
3. **Untracked:** the work directory, `work/` below, and the pages,
   `concrete-transcription-1.html` to `-3.html` and `concrete-transcription-3-preview.html`, which
   the commands below rebuild; the close looks, `look/`, which the helpers made for Claude; and
   the change page the image came from, `download-page/changes-page.html`, which nothing reads.
   All stay in that `.novc` folder. Any untracked directory serves as the work directory.

The program is run by hand, not by the mega, as `py/main_pen_stroke.py` is, which Ben's decision
of 2026-10-30 keeps out of the mega as "a very early-stage experiment": it works on this one
image, and nothing it writes is read by a product; of what it writes, only the production images
of the last section are tracked. `py/tests/test_mega_coverage.py` declares it so.

The move changed no output. The trial was rebuilt twice from the image and Ben's edits alone,
into fresh directories, once by the untracked scripts and once by the tracked program: every
command below, then the helpers `area`, `measure` with and without `--samples`, `look`, `look2`
and `look3`. The two rebuilds wrote the same 29 files, byte for byte, and printed the same output
but for the paths they were given. The scripts' rebuild also matched the trial's own files byte
for byte, the 20 other work files and draft 3's two pages. The four that differ are those this
README says are older: pages 1 and 2, written with earlier templates, and
`work/draft3-edge-profile.json` and its chart, made with the soft edge of 1 px. Then the two
templates' caveat "nothing on it is tracked" became "the page itself is not tracked", and draft
3's two pages were written again; the caveat is their only change.

Rebuild the whole trial, from the clone's root, in this order. Pages 1 and 2 come out in the
present template, not the ones they were first written with, and the profile of the edges with
the present soft edge.

```powershell
./.venv/Scripts/python.exe py/main_concrete_transcription.py level1 doc/concrete-transcription-2026-11-03/download-image/112-Detail.jpg .novc/concrete-transcription-2026-11-03/work
./.venv/Scripts/python.exe py/main_concrete_transcription.py draft .novc/concrete-transcription-2026-11-03/work 1
./.venv/Scripts/python.exe py/main_concrete_transcription.py shapes .novc/concrete-transcription-2026-11-03/work 1
./.venv/Scripts/python.exe py/main_concrete_transcription.py page .novc/concrete-transcription-2026-11-03/work .novc/concrete-transcription-2026-11-03/concrete-transcription-1.html 1
./.venv/Scripts/python.exe py/main_concrete_transcription.py fold .novc/concrete-transcription-2026-11-03/work doc/concrete-transcription-2026-11-03/edits/ben-edits-1.json .novc/concrete-transcription-2026-11-03/work/folded-ben-1.json
./.venv/Scripts/python.exe py/main_concrete_transcription.py draft .novc/concrete-transcription-2026-11-03/work 2
./.venv/Scripts/python.exe py/main_concrete_transcription.py shapes .novc/concrete-transcription-2026-11-03/work 2
./.venv/Scripts/python.exe py/main_concrete_transcription.py page .novc/concrete-transcription-2026-11-03/work .novc/concrete-transcription-2026-11-03/concrete-transcription-2.html 2
./.venv/Scripts/python.exe py/main_concrete_transcription.py draft .novc/concrete-transcription-2026-11-03/work 3
./.venv/Scripts/python.exe py/main_concrete_transcription.py shapes .novc/concrete-transcription-2026-11-03/work 3
./.venv/Scripts/python.exe py/main_concrete_transcription.py page .novc/concrete-transcription-2026-11-03/work .novc/concrete-transcription-2026-11-03/concrete-transcription-3.html 3
./.venv/Scripts/python.exe py/main_concrete_transcription.py preview .novc/concrete-transcription-2026-11-03/work .novc/concrete-transcription-2026-11-03/concrete-transcription-3-preview.html 3
./.venv/Scripts/python.exe py/main_concrete_transcription.py edges .novc/concrete-transcription-2026-11-03/work 3 .novc/concrete-transcription-2026-11-03/work/draft3-edge-profile.json
./.venv/Scripts/python.exe py/main_concrete_transcription.py edges-chart .novc/concrete-transcription-2026-11-03/work/draft3-edge-profile.json .novc/concrete-transcription-2026-11-03/look/draft3-edge-profile.png
```

The tracked production images, which `production` writes after draft 3's commands, have their
command in the last section.

## The image

`download-page/changes-page.html` and `download-image/112-Detail.jpg`, fetched 2026-11-03 at
23:38 UTC by `ct_fetch.py` (`mb_cmn.polite_download`, robots.txt obeyed as Claude-User,
as `uxlc_misc.my_uxlc.robots_user_agent` gives for tanach.us); each `.fetch.json` beside it records
URL, bytes and SHA-256. The change record (`in/UXLC-misc/all_changes.json`): Psalms 119:175, atom 5,
page F392B, column 2, line 10 in the record's count; type NoAction; Holman's note: "The resh and
the nun are connected by a near-horizontal line which is clearly not a maqaf." The detail image is
530 x 250 pixels, credited to Sefaria, and is an enlargement, about 2.7 times Sefaria's page
image each way, judged from the letters' sizes against the snips' crops of pages F043A and F102A.

## The method

1. `ct_level1.py`: level 1 by the tracked `py/pen_stroke/level1.py`, unchanged: Otsu
   threshold 135, speck size 50 (the snips' 8, scaled), halo band 24. Writes `work/112-Detail.png`
   (the decoded JPEG, lossless) and `work/level1.json`. 23 fills, 3 residual pieces, judged in
   `ct_signs.py` (`JUDGMENTS`).
2. `ct_draft.py`: profile 2's watershed by the tracked `region_derive.settle`, from
   Claude's seeds and two cuts in `ct_signs.py` (`GROUPS`, `CUTS`). Without the cuts the
   watershed gave the stray stroke almost none of its ink: the band between the resh and the nun is
   no paler than the letters. Writes `work/draft-regions.json` and `.png`.
3. `ct_shapes.py`: one outline per draft region, its control points the traced outline's
   joints and curve middles, then thinned while a closed uniform Catmull-Rom curve through them
   keeps within 0.4 px of the traced outline (`ct_geometry.py`); and the stray stroke as a
   stroke, `STROKE` in `ct_signs.py`: a centerline of 4 points from inside the resh's roof to the
   ink left of the nun, width 14, the start flat, the end round. Writes `work/draft-shapes.json`
   and `.png`, and prints the share-out: of 28,130 px of ink, 351 px lie in no shape, 45 px
   farther than 1.3 px from every shape (chiefly the fillets where the stroke meets the nun); the
   stroke shares 387 px of ink with the resh and 418 px with the nun, and reaches 11 px beyond the
   ink. These counts are by distance, as the page counts blur (`ct_share.py`); the first
   report of this draft gave 29 px, by an eight-neighbour dilation that reaches farther along the
   diagonals.
4. `ct_page.py` with `ct_page_template.html`: writes
   `concrete-transcription-1.html`, the editor. Its script draws the shapes with the same
   construction as `ct_geometry.py`; keep the two alike.

Regenerate, from the clone's root, in order:

```powershell
./.venv/Scripts/python.exe py/main_concrete_transcription.py level1 doc/concrete-transcription-2026-11-03/download-image/112-Detail.jpg .novc/concrete-transcription-2026-11-03/work
./.venv/Scripts/python.exe py/main_concrete_transcription.py draft .novc/concrete-transcription-2026-11-03/work
./.venv/Scripts/python.exe py/main_concrete_transcription.py shapes .novc/concrete-transcription-2026-11-03/work
./.venv/Scripts/python.exe py/main_concrete_transcription.py page .novc/concrete-transcription-2026-11-03/work .novc/concrete-transcription-2026-11-03/concrete-transcription-1.html
```

A new draft for Ben gets a new page filename and a new `DRAFT_VERSION` in its data module
(`ct_drafts.py` names each draft's), since the page keeps his edits in his browser under
a key that names the draft.

## What the page does

The image with every shape's outline; Ben drags control points, adds and removes them, toggles
corners, drags the stroke's centerline and its width; undo and redo. A clean page below shows the
result live, by meaning: letters black, marks dark blue, the stray stroke violet over them, the
masora circle and other atoms' and lines' ink faint; it can hide the stray stroke, which shows the
letters as their outlines run under it. Ink that no outline holds, farther than 1.3 px from every
outline, is red. Ben's edits stay in his browser (localStorage), and Copy puts the changes in JSON
on the clipboard: `changed` and `added` shapes in full, each with its path data `d` as the page drew
it, `deleted` ids, and his general `note`.

## Folding in Ben's edits

Take each changed or added shape's `d` as given: it is exactly what he saw. Rasterize every
shape at 3 samples a pixel (as `ct_shapes.py` does), share out the ink, and show him the result
beside the image, by the README rule in `doc/pen-stroke-snips/README.md`, "Showing images to Ben".
The result stays untracked until Ben says where it goes; a tracked crop needs its row in
`DATA-LICENSES.md`.

`ct_fold.py` does this for one export, the draft it edits named by its `draft` field
(`ct_drafts.py` maps each draft's name to its data module and its work files' prefix):

```powershell
./.venv/Scripts/python.exe py/main_concrete_transcription.py fold .novc/concrete-transcription-2026-11-03/work doc/concrete-transcription-2026-11-03/edits/ben-edits-1.json .novc/concrete-transcription-2026-11-03/work/folded-ben-1.json
```

## Ben's edits of draft 1

`edits/ben-edits-1.json` is the export that Ben pasted into the trial session's chat on
2026-11-03, saved verbatim. Each edited shape's path data equals what `ct_geometry.py` draws
from its points, to the last of its three decimals, so the page and the Python agree. He edited
two shapes and wrote no note:

1. The resh: 11 of its 48 points, those of the left end of its roof, moved right and down, so
   that the roof ends where his stroke begins.
2. The stray stroke: its start moved from inside the resh's roof to the roof's lower left corner,
   its other three points with it, and its width from 14 to 18.51.

Shared out with his edits: 23 px of ink farther than 1.3 px from every shape (draft 1: 45 px):
13 px in the fillet under the resh's roof beside the stroke's start, the rest a hairline along
the stroke's lower edge, two specks where the stroke meets the nun, and the 4 px crumb at the
ḥataf pataḥ bar's left tip; the stroke shares 2 px of ink with the resh and 575 px with the nun,
and reaches beyond the ink nowhere.

Ben then wrote, while Claude was folding the edits in: "BTW there's nothing sacred about my
edits... if you want to use them as guidelines re-seeding your own analysis/shapes, that's
fine!" Hence draft 2.

## Draft 2: Claude's reading re-seeded from Ben's edits

`ct_signs2.py`, which says how in its docstring and comments:

1. **The stroke** is Ben's centerline and caps, his width made wider by half a pixel, the least,
   in tenths, that leaves none of the ink about the stroke farther than 1.3 px from a shape (at his
   width a hairline of the ink's lower edge lay just beyond); at 19.01 it reaches beyond the ink
   by a third of a pixel in all.
2. **The cuts.** The stroke's outline made wider by 1.3 px on each side, its start where Ben put
   it, is a cut, so the letters take all the ink outside the stroke and its blur, and the
   resh's left end lies along the stroke's start. (A cut along the stroke's own outline gave the
   resh a hairline of the stroke's blur along its whole lower edge.) Inside it two cuts give the
   nun its ink under the stroke: its edges there run straight from where they show just above the
   stroke to where they show just below it.
3. **The seeds** are draft 1's, but for the stroke's ink that shows, seeded between the resh and
   the nun and left of the nun, and one more for the nun, under the stroke.

The share-out, by the page's measure: 4 px of ink farther than 1.3 px from every shape, all of it
the crumb at the ḥataf pataḥ bar's left tip that touches no region in either draft; the stroke
shares 3 px of ink with the resh and 593 px with the nun; no shape reaches beyond the ink by more
than a pixel. `concrete-transcription-2.html` is its page, with one question, A, marked at the
nun's two edges under the stroke. Ben's edits of draft 1 stay in his browser under draft 1's key.

Regenerate draft 2, from the clone's root, after level 1 (the first command above):

```powershell
./.venv/Scripts/python.exe py/main_concrete_transcription.py draft .novc/concrete-transcription-2026-11-03/work 2
./.venv/Scripts/python.exe py/main_concrete_transcription.py shapes .novc/concrete-transcription-2026-11-03/work 2
./.venv/Scripts/python.exe py/main_concrete_transcription.py page .novc/concrete-transcription-2026-11-03/work .novc/concrete-transcription-2026-11-03/concrete-transcription-2.html 2
```

Generalizing the scripts to two drafts left draft 1's work files and page byte for byte as they
were (SHA-256 compared before and after); `draft-shapes.png` alone changed later, when
`ct_shapes.py` took up the page's measure for its red.

Helpers for Claude, not for Ben: `ct_measure.py` prints a text map of a draft's regions
about the crossing; `ct_look3.py` draws two sets of shapes over a close-up of the image,
into `look/`.

## Ben's requests of 2026-11-04, and what is done

Ben's messages of 2026-11-04 asked for a third draft and for changes to the clean page; the
handoff `concrete-transcription-handoff-2026-11-04.md`, in the commander's shared notes folder
(`C:/Users/BenDe/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/side-session-notes/local_a80ded65-f78e-4280-8493-9dab3b8c5686/`),
quotes them and plans draft 3. Done so far:

1. **The page's template** (`ct_page_template.html`), for every page made from now on:
   on the clean page, checkboxes for each letter with its marks in two colours by turns (black
   and `#c05800`; the clusters are `CLUSTERS` in `ct_signs.py`, as Ben gave them), for the
   image's own ink and vellum colours (their medians, which `ct_page.py` measures: ink `#403931`,
   vellum `#d5cbae`), for soft edges (a Gaussian blur of `SOFT_EDGE`, 1 px, a first guess) and for
   the difference from the image below the clean page: the shapes, whole, as the clean page shows
   them, less the image's ink, each pixel's (vellum - lum) / (vellum - ink); white where they
   agree, red where the shapes have more ink, blue where they have less. The stray mark's shapes
   are drawn as one group. The stray stroke's checkbox was there already; Ben withdrew his request
   for it. `concrete-transcription-2.html` was rewritten with this template, its data and storage
   key unchanged; page 1 keeps the old template. In the built-in browser: no script errors; with
   soft edges the difference's total falls by about a sixth, its red by more than a quarter.
2. **The weight of the outlines** (`ct_area.py`). Ben's theory: the level-1 boundary lies
   out in each edge's fade, so the shapes, dots most of all, are heavier than the ink. Measured
   on draft 2's regions: each region's deposited ink, the sum over the pixels within 4 px of it
   (nearer it than any other) of (V - lum) / (V - K), V its vellum's median, K the median of the
   ink's cores, 58, not clamped so that ringing cancels; against its area at the threshold, 135.
   The two agree within a few hundredths for every region, the dots included (in all, 28,324 px
   against 27,859; the 12 dots and small marks 1,990 against 2,000); the threshold that would equal
   them is 130 to 133, by reaches of 3 to 6 px; a boundary at the fade's start, 90 to 100, would
   hold 0.76 to 0.83 of the ink. In linear light the equal-area threshold is 145 to 160, outward.
   So by R19 the outlines are not too heavy; the clean page's black on white with hard edges is
   the likelier cause, which the new checkboxes let Ben judge.
3. **Draft 3**, made from Ben's comments on draft 2: the next section.

## Draft 3: Ben's comments of 2026-11-04 on draft 2

Made on 2026-11-04 by the session that the commander started from the handoff, which took the
trial over. `ct_signs3.py` says how in its docstring and comments; its coordinates are
the image's pixels at the level-1 threshold, 135, and its cuts and strip are the handoff's.

1. **The zayin and the resh no longer touch.** A strip of vellum (`VELLUM`), 1.5 px wide along
   the handoff's line, takes out the light ridge, luminance 107 to 130, that joined the zayin's
   head to the resh's roof at x 240 to 244, y 83 to 89: 12.0 px of ink. The two letters' shapes
   are now at least 1.67 px apart; draft 2's overlapped by 0.33 px. A 2.5 px strip, tried, parts
   them by 2.67 px; the handoff's width, the smaller change, is kept. The strip's samples leave
   the ink wherever the trial counts it: `ct_share.ink_mask` takes the draft's data module, and
   the page's ink is level 1's fills but for the one fill the strip crosses, f10, traced again
   from its samples less the strip's (`ct_page.fills_d`).
2. **The stray stroke runs into the resh.** Draft 2's stroke, Ben's centerline and his width
   fitted to the ink, 19.01, with its start made round, so that its tail reaches about half its
   width into the resh, over 161.9 px of the resh's ink: Ben's first choice. Under it a cut gives
   the resh a rounded lower left corner, the handoff's Bezier curve from (170.5, 85) to
   (180.5, 101), as 16 straight segments.
3. **The nun's hidden edges are curves**, two cuts each tangent to the nun's visible edge above
   the stroke and below it, as the handoff gives them. Draft 2's cut along the stroke's outline
   is gone, so the nun's ink under the stroke joins its head and stem, and draft 1's seeds hold
   it. The nun's outline has no corner about the crossing, so `SMOOTH` stays empty. Below y 92 the
   ink's left edge drifts left of the curve, 2 px by y 97: that is the fillet where the stroke's
   round end meets the nun's head, and it goes to the stray stroke.
4. **The stray stroke's ink beside the stroke** is its region less the stroke. Of its 9 pieces,
   the 3 that reach farther than 1.3 px from the stroke are kept: 13.9 px at the junction above
   the stroke between the nun's head and the resh, 5.8 px where the stroke meets the nun's head's
   left edge, and 7.6 px under the stroke's left end where it meets the nun's stem. Each is grown
   0.7 px into the stroke, so that the two meet without a seam. `ct_draft.py` traces them as the
   regions file's `rest`, and `ct_shapes.py` makes them one outline, `rg20`, "where it meets the
   letters", in the stroke's group, which the page draws, and hides, with the stroke
   (`STROKE_REST`). The 6 pieces dropped lie within 1.3 px of the stroke, its blur.
5. **The page's questions:** A at the resh's hidden corner and the stroke's tail, B at the nun's
   two hidden edges.

The share-out, by the page's measure: of 28,117.9 px of ink, 4.0 px lie farther than 1.3 px from
every shape, all of it the crumb at the ḥataf pataḥ bar's left tip, level 1's piece r3, as in
drafts 1 and 2; the stroke shares 161.9 px of ink with the resh and 615.6 px with the nun; no
shape reaches beyond the ink by more than a pixel. `concrete-transcription-3.html` is its page,
which says it was made on 2026-11-04: the template's date is now a placeholder, `MADE` in the
draft's data module, which drafts 1 and 2 leave at 2026-11-03.

Checked on 2026-11-04:

1. Drafts 1 and 2, regenerated into a scratch work directory with the changed scripts, gave
   every one of their work files and page 2 byte for byte (SHA-256 compared).
2. In the built-in browser, on a copy of the page: no script errors; every checkbox works; with
   the stray stroke hidden, the clean page has vellum where the bridge was and in the stroke's
   band, round end and junction, and black where the nun and the resh's corner lie under it.
3. The page's ink agrees with `ct_share.ink_mask` but for about 29 px each way of boundary
   samples along the re-traced fill, and with the page's ink, too, only the crumb is unexplained.
4. Close looks, draft 2's outlines grey under draft 3's: `look/draft3-crossing.png` and
   `look/draft3-zayin-resh.png`.

Regenerate draft 3, from the clone's root, after level 1:

```powershell
./.venv/Scripts/python.exe py/main_concrete_transcription.py draft .novc/concrete-transcription-2026-11-03/work 3
./.venv/Scripts/python.exe py/main_concrete_transcription.py shapes .novc/concrete-transcription-2026-11-03/work 3
./.venv/Scripts/python.exe py/main_concrete_transcription.py page .novc/concrete-transcription-2026-11-03/work .novc/concrete-transcription-2026-11-03/concrete-transcription-3.html 3
```

The helpers gained two options: `ct_measure.py --samples` prints a map at the samples'
resolution, the draft's cuts in lower case, and `ct_look3.py --draft=<draft>` counts the ink
less that draft's strips.

## Ben's replies on draft 3, 2026-11-04

1. **The name.** To "The name “concrete transcriber”. I have renamed nothing." Ben wrote:
   "let's go with that name." The page now calls the project "the concrete transcriber, the paused
   ink-region work". Nothing tracked is renamed; the commander was told, since recording the
   name in the tracked plan is a tracked change. Asked in another session whether anything
   should take the name, Ben answered "Rename nothing yet"; the plan records the name as item 12
   of its "Ben's decisions".
2. **The page** (`ct_page_template.html`), as he asked: the clean page's colourings are
   three choices, the image's ink and vellum the default, the others by meaning on white and
   each letter with its marks in two colours by turns on white; its edges soft by default, sharp
   the other choice; the difference from the image shown always, its checkbox gone; the side
   panel's four parts, the questions, the editing help, the selected shape and the new shape,
   each collapsed at first; the list of shapes collapsed at first under "Shapes", below "Your
   edits". The questions no longer show their letter twice. `concrete-transcription-3.html` was
   written again with this template, its data and storage key unchanged; page 2 keeps the
   template it was written with, so `ct_page.py` would now write page 2 differently. Checked in
   the built-in browser on a copy: no script errors; every part collapsed at first; each
   colouring and each edge setting draws, with its own legend.
3. **"The ink inside each outline" and "each outline whole".** Ben saw no difference between
   them, rightly: the outlines follow the ink's edge within about half a pixel, so the two
   pictures part only where an outline leaves the ink, as after an edit that drags a point into
   the vellum. Claude asked whether to drop the choice and fill each outline whole.
4. **The red inline.** Ben: "I am seeing a red outline (well, really an "inline") of every shape
   in the difference image. To me that says that the conc.-trans. has too much ink (or ink that
   is too heavy) near the edges, which agrees with my "every shape looks slightly too big"
   perception, doesn't it?" `ct_edges.py` measured it: for every pixel within 4 px of an
   outline, its signed distance from the outline; in bins of that distance, the image's ink and
   the shapes' coverage; and a least-squares fit of the image's ink by the shapes moved out by
   delta px and blurred by sigma px. Averaged over every edge, the image's ink passes half-way
   at the outline; the shapes with the page's soft edge, 1 px, are darker than the image inside
   it (the red inline) and lighter outside it (the blue fringe), the blue the larger by the
   page's measure (red 1,619.4 px, blue 2,159.4 px, net -540.0 px within 4 px of an outline).
   The fit leaves the outlines where they are (delta +0.1 px, sigma 2.4 px; with the vellum
   about the letters let be a little darker than the median, delta -0.2 px, sigma 1.8 px). So
   the outlines are the right size, to within a fifth of a pixel, and their edges too sharp:
   the image's fade is about twice the page's soft edge. The shapes' dark cores are larger than
   the image's, which reaches full darkness only 3 to 4 px inside an outline: that is the
   "slightly too big". Claude asked whether to set the soft edge to fit the image.
   `ct_edges_chart.py` draws the profile: `look/draft3-edge-profile.png`, from
   `work/draft3-edge-profile.json`.

```powershell
./.venv/Scripts/python.exe py/main_concrete_transcription.py edges .novc/concrete-transcription-2026-11-03/work 3 .novc/concrete-transcription-2026-11-03/work/draft3-edge-profile.json
./.venv/Scripts/python.exe py/main_concrete_transcription.py edges-chart .novc/concrete-transcription-2026-11-03/work/draft3-edge-profile.json .novc/concrete-transcription-2026-11-03/look/draft3-edge-profile.png
```

   The chart and `work/draft3-edge-profile.json` record the page's soft edge as it was then,
   1 px; `ct_edges.py` run again now reads the page's present soft edge.
5. **The soft edge widened.** Asked whether to widen the page's soft edge to match the image's
   own fade, Ben answered "Yes, widen it". `ct_page.SOFT_EDGE` is now 2.4 px, the fit with the
   outlines left where they are. Within 4 px of an outline the red falls from 1,619.4 px to
   640.7 and the blue from 2,159.4 to 1,215.3; the sum of squared differences from 697.9 to
   201.9, against 195.7 for the best fit. The difference image's blur now carries the image's
   edge pixels outward first, as `ct_edges.py`'s does, so that the letters the image's edge
   cuts show no false blue band; the clean page's own blur, an SVG filter, still fades them at
   the image's edge. `concrete-transcription-3.html` was written again. Checked in the built-in
   browser on a copy: the clean page's blur is 2.4 px; the difference image's red is about half
   what sharp edges give, with no band along the image's edge; no script errors.
6. **Each outline whole.** Asked whether to drop the choice and fill each outline whole, Ben
   answered "Yes, drop it". The clean page now draws each shape whole, the transcription itself,
   as the difference image already compared; the choice of "the ink inside each outline" is
   gone, and with it the introduction's claim that shared ink shows on the clean page. Checked
   in the built-in browser on a copy: one drawing a shape, no choice left, the stray stroke's
   checkbox still hiding both its shapes, no script errors.
7. **The tracked record of the name.** A session the commander started recorded it in
   `doc/PLAN-ink-regions.md` (`54dd4cd1`), and other sessions have moved this clone's `main` to
   `210affe3`; none of their commits touches code the trial imports.

## The production preview and the development page's new defaults, 2026-11-04

Ben, in the draft-3 session, about 11:00 New York time:

> Make 1.5x the default for both magnificiation settings (currently I think they are 2.5x and
> 2.0x respectively)
>
> Prepare a "production preview" page that shows a single image in the following way: no
> controls; clicking it just cycles between 3 views: original image, concrete transcription with
> stray stroke present, and concrete transcription with stray stroke removed.
>
> Here "concrete transcription" means the following two are not shown:
>
> the masora circle, and other atoms' and lines' ink
> ink no outline holds, red
>
> Colours are the image's ink and vellum
> Edges are soft
>
> most of those are already the default on the page we've been working on (which we might call
> the development page as opposed to the production page), but I'd like all of those I specify
> above to become the defaults on the development page, too

He then asked for a fresh session, which the commander started from the handoff
`concrete-transcription-preview-handoff-2026-11-04.md` in its shared notes folder. That session
made the following.

1. **The development page's defaults** (`ct_page_template.html`): both sizes 1.5×, the
   editor's and the clean page's; on the clean page, "the masora circle, and other atoms' and
   lines' ink" and "ink no outline holds, red" unchecked. The image's ink and vellum and soft
   edges were the defaults already. The editor's own "ink no outline holds, red", on the
   photograph, stays checked: Ben's list is the clean page's, and the editor's red is an aid to
   editing.
2. **The difference image** now always includes the masora circle and other atoms' and lines'
   ink, so that their ink reads white; at the new default it would otherwise show all of it
   blue. Its legend says so. The stray stroke still follows its checkbox, and the edges the
   clean page's.
3. **The clean page's legend** shows an entry only while the clean page shows what it names:
   the red, the masora circle and other ink, and the stray stroke each follow their checkbox.
4. **`concrete-transcription-3.html`** was written again. Its diff from the page before is
   exactly the template's changes; its data and storage key are unchanged, so edits kept in a
   browser carry over.
5. **The production preview**, `concrete-transcription-3-preview.html`, is written by
   `ct_preview.py` from `ct_preview_template.html`: the image at 1.5×, with no
   controls and no visible text. A click on it, or Enter or Space while it has the focus, shows
   the next of three views: the image; the concrete transcription with the stray stroke; the
   concrete transcription without it. Each view's name is the image's tooltip. The
   transcription is draft 3's shapes as Claude drew them, not edits kept in a browser: the
   atom's own shapes (owner "this-word") less the masora circle, path data by
   `ct_geometry.shape_d`, outlines filled by the even-odd rule and strokes by the nonzero rule,
   ink `#403931` on vellum `#d5cbae` (`ct_page.image_tones`), under one SVG Gaussian blur of
   `ct_page.SOFT_EDGE`, 2.4 px, and no red. Since the page has no visible text, its AI caveat is
   the comment that opens its source. Chrome rings a focused SVG element even after a click, so
   a CSS rule keeps the ring for the keyboard's focus only.

Checked on 2026-11-04 in the built-in browser, on copies in `look/page-checks/`, since deleted:

1. The development page: both sizes 1.5×, the editor, the clean page and the difference each
   795 px wide; the two checkboxes unchecked; the clean page drawing 21 shapes, the atom's 19
   letters and marks and the stray stroke's 2, and hiding 6, the masora circle and the other
   ink; toggling the masora circle's checkbox changes no pixel of the difference image, which at
   the default shows no deep blue at the masora circle; each legend entry follows its checkbox;
   no script errors.
2. The preview: the three views in turn, one at a time, by clicks and by Enter and Space, the
   tooltip naming each; no ring after a click; no script errors. With the stray stroke and
   without it, its shapes' path data and fill rules hash the same as the development page's
   clean page at its defaults (21 shapes and 19), and its blur, ink and vellum are the clean
   page's.
3. Every other file of the trial is unchanged, SHA-256 compared before and after, the work
   files of drafts 1 to 3 and pages 1 and 2 among them.

Meanwhile the Miqra Mevoar session moved this clone's `main` to `48d811f1` and had uncommitted
edits in it; none of them touches code the trial imports, and none of the modules they change
loads with the trial's scripts.

Regenerate both pages, from the clone's root, after draft 3's commands:

```powershell
./.venv/Scripts/python.exe py/main_concrete_transcription.py page .novc/concrete-transcription-2026-11-03/work .novc/concrete-transcription-2026-11-03/concrete-transcription-3.html 3
./.venv/Scripts/python.exe py/main_concrete_transcription.py preview .novc/concrete-transcription-2026-11-03/work .novc/concrete-transcription-2026-11-03/concrete-transcription-3-preview.html 3
```

## The production images, 2026-11-04

At 17:32 New York time on 2026-11-04 Ben asked the commander session for the production version
in a form that Codex can incorporate in a page it maintains outside this repository: "if you get
the image(s) committed to MAM-basics somewhere appropriate". The session that the commander
started for it committed them here, in `production/`:

1. `concrete-transcription-3-with-stray-stroke.svg` and
   `concrete-transcription-3-without-stray-stroke.svg`, 21,606 and 19,210 bytes: the production
   preview's second and third views, the concrete transcription with the stray stroke and
   without it. Each is a standalone SVG file of the image's size, 530 by 250, in its pixels; the
   preview shows them at 1.5×, 795 by 375. Each draws what its view draws: the vellum,
   `#d5cbae`, and over it draft 3's shapes as Claude drew them, in the ink, `#403931`, under one
   Gaussian blur of 2.4 px. Neither embeds the image, and each file's filter has an id of its
   own, its filename's stem with `-soft` added, so that both can be inlined in one page.
2. The first view, the image, is `download-image/112-Detail.jpg` itself, of the same size; the
   preview shows the lossless decoding of it that level 1 writes, `work/112-Detail.png`.

`ct_preview.py` writes the preview and the production images alike, from the same construction
of each view, and the program's `production` subcommand runs it. Regenerate them, from the
clone's root, after level 1 and draft 3's `draft` and `shapes` commands above:

```powershell
./.venv/Scripts/python.exe py/main_concrete_transcription.py production .novc/concrete-transcription-2026-11-03/work doc/concrete-transcription-2026-11-03/production 3
```

They are no product, and nothing checks that they are current: a change to the trial's code, to
the code of `py/pen_stroke/` that it imports, or to its image obliges the rerun, by `AGENTS.md`'s
rule for hand-run generators, and the regenerated files' diff is the check. `DATA-LICENSES.md`
gives their terms, those of the image they are traced from.

Checked on 2026-11-04:

1. Level 1 and draft 3, rebuilt from the image alone into a fresh work directory, gave
   `level1.json`, `112-Detail.png` and `draft3-shapes.json` byte for byte as the trial's own.
2. The preview page, written again from that directory by the changed `ct_preview.py`, is byte
   for byte the page it wrote before.
3. Parsed, each image's paths, in order and with their fill rules, and its vellum, ink, filter
   region, blur and viewBox, equal those of its view in the preview page as it was before the
   change: 21 paths with the stray stroke, 19 without it.
4. In the built-in browser, the JPEG and the two images, each embedded as a `data:` URL in a page
   whose Content-Security-Policy admits images only as `data:` URLs, loaded at 530 by 250 and
   drew as the preview's views do, with no console message.
