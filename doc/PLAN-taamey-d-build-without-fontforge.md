# Plan: build Taamey D from a UFO with fontTools and ufo2ft, retiring FontForge and the SFD

State: live; proposed 2026-10-29, awaiting Ben's answers to "Decisions for Ben" below; nothing
executed. Tracked by #340, the thin pointer issue.

## Context

Claude-written on 2026-10-29. Ben asked that day: "Since I have no plans to ever use FontForge
interactively again, would it make sense to move to some different tool to build Taamey D (and
different file format to store Taamey D's sources)?" The session's assessment was yes, and this
plan is that answer worked out; everything below the quotation is the session's reconstruction.
The assessment found that FontForge is now only a compiler in Taamey D's pipeline, that
fontTools' feature compiler accepts Taamey D's feature file unchanged, and that the font's
shaping corpus can prove a new build equivalent.

The pipeline today, all paths from the MAM-basics root:

- `py/main_taamey_d_build.py` fills three `$`-symbol templates with standard-library Python,
  writing `Taamey-D/font-m-TaD/Taamey_D.fea`, `Taamey_D-nofea.sfd` and `license.txt`.
- It then runs FontForge on `Taamey-D/font-m-TaD/ffscript_generate_sfd_n_ttf.py`, seven lines:
  open `Taamey_D-nofea.sfd`, `mergeFeature` the `.fea`, save `Taamey_D.sfd`, generate
  `Taamey_D.ttf`, `.woff` and `.woff2`.
- FontForge is installed separately, found on PATH or at `FontForgeBuilds/fontforge.bat`, and is
  the only non-pip tool among the repository's generators. The build is hand-run and outside the
  mega by Ben's decision of 2026-10-28, "Yes, keep FontForge run out of MAM-basics mega", which
  `py/main_0_mega.py`'s step comments and `py/tests/test_mega_coverage.py`'s `NOT_IN_MEGA`
  entry record.

What the SFD holds, measured on `Taamey-D/font-m-TaD/Taamey_D-nofea.sym.sfd` at commit
`95dc8ddd`: 304 glyphs, 204 with outlines (cubic; no `Order2` header), 94 built only from
references (`Refer` lines, 272 in all, 8 with a scale, flip or 30-degree rotation), no glyph
mixing outlines and references, PostScript stem hints on most glyphs, no TrueType instructions,
no lookups and no anchors (every OpenType layout rule lives in `Taamey_D.sym.fea`), and three
`$`-symbols (`$copyright_and_license`, `$version`, and the unique-ID name). The TTF has one more
glyph, `nonmarkingreturn`, which FontForge adds.

What the SFD's edit history shows (hbofonts, 21 commits touching the SFD against 37 touching
the feature file, 2021-10 to 2026-10): composite glyphs added from existing parts, reference
offsets tweaked, glyph renames, version and name records, and one 2021 autohint pass. No
outline was drawn in that history.

## Evidence, dated 2026-10-29

Measured at MAM-basics commit `95dc8ddd`; the quoted passages were re-checked at `5c113154`.

1. **feaLib compiles the filled feature file unchanged.** `fontTools.feaLib.builder.
   addOpenTypeFeatures` (fontTools 4.64.0, the venv's pin) compiled
   `Taamey-D/font-m-TaD/Taamey_D.fea` onto a copy of `Taamey_D.ttf` stripped of GSUB, GPOS and
   GDEF, in memory, with no error. Lookup counts differ (FontForge: 46 GSUB, 72 GPOS; feaLib:
   32 GSUB, 40 GPOS), as the two compilers split lookups differently; equivalence is proved by
   shaping, in Phase 1.
2. **GDEF glyph classes must be carried explicitly.** FontForge's GDEF classifies every glyph
   (202 base, 24 ligature, 79 mark). feaLib's build from the feature file alone classifies 156
   (83 base, 73 mark). Six marks are missing: `dieresisnosp`, `dotnosp`, `lowerdot.no_xazaq`,
   `ringnosp`, `shevana.rectangle`, `xolam.invis`. The 24 FontForge ligatures are the
   `*dagesh.xazaq` compositions, `aleflamed` and `trueshingereshtg`. All 20 `lookupflag`
   statements in the feature file are `UseMarkFilteringSet`, so a glyph's mark class decides
   whether a lookup skips it: the classes are part of the font's behaviour.
3. **FontForge's quadratic conversion drifts between FontForge versions.** hbofonts'
   `doc/PLAN-move-MAM-basics-off-Taamey_D-0.921.md`, "Invisible or non-shaping changes": "36
   glyphs' TrueType outlines differ by at most 5.3 units of the 2,048-unit em ... a newer
   FontForge converted the same curves." MAM-basics' `doc/review-findings-2026-10-02.md`, "The
   font's exact rebuild": "21 of 278 glyphs differ in quadratic-conversion points".
   `Taamey-D/README.md`, "Building the font", pins the claim to one FontForge: it "reproduces
   the tracked outputs byte for byte", and "A different FontForge can change the built bytes".
4. **The oracle exists.** `Taamey-D/qa-in/` holds 120,437 test cases, each with Taamey D's
   expected shaping output by glyph name and position, and `py/main_taamey_d.py qa` rewrites the
   reports in `Taamey-D/qa-out/Taamey_D/` from `Taamey-D/font-m-TaD/Taamey_D.ttf`. A new build
   that leaves every report unchanged shapes the whole corpus identically.
5. **The environment.** `./.venv/Scripts/python.exe` is Python 3.13.15 with fonttools 4.64.0,
   uharfbuzz 0.57.0, vharfbuzz 0.3.1, collidoscope 0.6.5, ufoLib2 0.18.1 and skia-pathops.
   Not installed: brotli (so this fontTools cannot write WOFF2), ufo2ft, fontmake, sfdLib,
   defcon. ufo2ft 3.9.1 on PyPI is MIT, needs Python >= 3.10 and `fonttools[ufo] >= 4.61.1`,
   `booleanoperations`, `cffsubr`, `fontmath`.
6. **The release tool anticipates a changed source list.** `py/taamey_d/release.py`, comment
   above `_BUILD_SOURCE_PATHS`: "Every published snapshot is checked against this list too, so
   changing it would refuse the snapshots published before the change: the list must then be
   chosen by each snapshot's source commit".
7. **The import lint records a decision.** `py/tests/test_taamey_d_build_imports.py`: "By
   Ben's decision of 2026-10-28, the scripts that are to ship in Taamey D's source archives ...
   import only the standard library". Its reason is GPL-3.0 avoidance and the archive's
   self-sufficiency; fontTools (MIT), ufo2ft (MIT) and ufoLib2 (MIT) are compatible with
   GPL-2.0-or-later, and the archive already needs an external compiler, FontForge, installed.

## Decisions for Ben

Record each answer here, dated, before execution.

1. **Go ahead at all.** Recommended: yes.
2. **Where the UFO's outlines come from.** Recommended: from the committed Taamey D 1.2 TTF,
   with fontTools, so the UFO holds the shipped TrueType outlines (quadratic) and composites
   exactly, and the new build's `glyf` can be compared point for point with 1.2. Alternative:
   from the SFD with sfdLib (BSD-3; parses outlines, references with full transforms,
   `GlyphClass`, widths, Unicode values; drops stem hints; its last release date is unverified),
   which keeps cubic curves but reintroduces a cubic-to-quadratic conversion whose result can
   only be compared within a tolerance.
3. **The compiler.** Recommended: ufo2ft, called from Python, with explicit options
   (`featureWriters=[]`, `useProductionNames=False`, `removeOverlaps=False`). Alternative:
   fontTools' `FontBuilder` with hand-written table setup, fewer dependencies but more code to get
   right.
4. **The build joins the mega.** Recommended: yes, as a step before `taamey-d-qa`, once it is
   pure Python. The 2026-10-28 decision excluded a FontForge run; a pip-installed build has no
   such reason, and the mega would then check the font's bytes like every other product. If no,
   it stays hand-run and `NOT_IN_MEGA` keeps it.
5. **The unique-ID name.** Name ID 3 is "FontForge 2.0 : Taamey D : 1.2", fixed by hbofonts
   `53ce684` (2026-10-23). Keep the string for continuity, or change it to one that no longer
   names FontForge, such as "Taamey D 1.3 : MAM-basics".
6. **Retire the SFD files from the tree.** Recommended: delete `Taamey_D-nofea.sym.sfd`,
   `Taamey_D-nofea.sfd`, `Taamey_D.sfd` and `ffscript_generate_sfd_n_ttf.py`; Git history and
   hbofonts keep them. Alternative: keep `Taamey_D-nofea.sym.sfd` as a frozen reference that
   nothing builds from.
7. **Release timing.** Make Taamey D 1.3 right after the migration (a tooling-only release whose
   notes say the shaping is unchanged), or wait for the next content change. The site's pages
   keep loading the 1.2 pin either way.
8. **Widen the import lint.** Allow `fontTools`, `ufo2ft` and `ufoLib2` in
   `py/tests/test_taamey_d_build_imports.py`, amending the 2026-10-28 decision, with the
   docstring giving the licences.

## Checkouts, interpreter, baseline

- Development and integration checkout: `C:/Users/BenDe/GitRepos/MAM-basics`, a full clone in
  Claude's primary forest; every command below runs from its root with
  `./.venv/Scripts/python.exe`. A linked worktree is possible under the `linked-worktrees`
  skill but not preferred (Ben, 2026-10-20: a full clone is the default checkout).
- Read-only reference: `C:/Users/BenDe/GitRepos/hbofonts` (HEAD `3b59254`, 2026-10-29,
  "Announce Taamey D's development freeze here"). Nothing is written there.
- Baseline: this plan was written at MAM-basics HEAD `5c113154` (2026-10-29, "Check Taamey D's
  downloads before every Pages deploy, and correct the fresh read's points"), with a clean tree
  and `main` equal to `origin/main`. Precondition for Phase 2 onwards: `git status --porcelain`
  is empty, `5c113154` is an ancestor of HEAD, and the executor records HEAD here before the
  first edit.
- Executor and integration owner: the Claude session that executes, committing to `main` and
  pushing after the checks of "Verification" below. One writer in the clone at a time.
- Read first: `Taamey-D/README.md` (AGENTS.md requires it before touching `Taamey-D/`),
  `AGENTS.md` "What this repository's products are", `doc/clone-forests.md` "Environments".
  Load `iterative-document-editing` for the ledger, and `hebrew-prose` before writing release
  notes or page prose that describes marks.

## Phase 1: feasibility spike, no tracked change

Everything here writes only under `.novc/` (gitignored) and the session scratchpad.

1. Make a scratch environment `.novc/tad-spike-venv/` with Python 3.13 and install
   `fonttools==4.64.0`, `ufoLib2==0.18.1`, `ufo2ft` (3.9.1 at planning time) and `brotli`.
   The repository's `.venv` is not touched in this phase.
2. Scratch script `.novc/tad_ufo_from_ttf.py`: read `Taamey-D/font-m-TaD/Taamey_D.ttf` with
   fontTools and write `.novc/tad-spike/Taamey_D.ufo` with ufoLib2:
   - every glyph in the TTF's order, drawn from `glyf` through the UFO glyph's pen (simple
     glyphs become `qcurve` contours; the 94 composites become `<component>` elements with
     their full transform; `nonmarkingreturn` included), advance width from `hmtx`, Unicode
     values from `cmap`;
   - `public.glyphOrder` = the TTF's order; `public.postscriptNames` absent, so names are kept;
   - `fontinfo.plist` from `head`, `hhea`, `OS/2`, `post`, `gasp` and `name`: unitsPerEm 2048,
     ascender 1638, descender -410, the hhea, typo and win metrics as the TTF has them (win
     descent 900, hhea descent -900), `openTypeHeadCreated` from `head.created`,
     `openTypeHeadFlags` [0, 1, 3], gasp records, vendor `YGNT`, panose, fsType 0, the OS/2
     Unicode and code-page ranges, italic angle 0, underline position -170 and thickness 70,
     family and style names and `postscriptFontName` "Taamey_D" as name IDs 1, 2 and 6 give
     them. Version, copyright, unique ID and the version string are set by the build, not stored.
3. Add to a scratch copy of the feature file template `Taamey-D/font-m-TaD/Taamey_D.sym.fea` a
   `table GDEF { GlyphClassDef @gdef_bases, @gdef_ligatures, @gdef_marks, ; } GDEF;` block
   whose three classes list exactly the glyphs of 1.2's GDEF (202, 24 and 79 names, read from
   the TTF, not from the SFD's partial `GlyphClass` lines). The block makes the classes
   authored text in the file where every glyph is already declared for layout, and feaLib
   raises if a `markClass` glyph is listed as a base, which is the consistency check.
4. Scratch script `.novc/tad_compile.py`: fill the templates with
   `taamey_d_build.fill_in_template.fill_in` (the module imports nothing else), set
   `versionMajor`/`versionMinor`, `copyright`, `openTypeNameVersion` ("Version 1.2") and
   `openTypeNameUniqueID` on the UFO in memory from `py/taamey_d_build/font_version.py` and the
   template values, set `ufo.features.text` to the filled feature file, and call
   `ufo2ft.compileTTF(ufo, featureWriters=[], useProductionNames=False, removeOverlaps=False)`.
   Then set `head.fontRevision` to the version as a float, set `head.modified` to a fixed value
   with `recalcTimestamp` off, save the TTF, and save WOFF and WOFF2 copies by setting
   `flavor`. No `FFTM` table is written; that table is FontForge's own.
5. Scratch script `.novc/tad_compare.py`: dump both TTFs with `ttx` to the scratchpad and
   compare table by table. Expected equal: `glyf` outlines and components (point for point,
   component flags excepted and listed), `hmtx`, `cmap`, `post` glyph names, `maxp.numGlyphs`,
   GDEF class map, `gasp`, `OS/2` metrics. Expected different, each to be listed: GSUB and GPOS
   structure, `name` records, `head.modified`, absence of `FFTM`, `OS/2.version` if ufo2ft
   writes a newer one. Any other difference is a finding.
6. Shaping equivalence: copy the scratch TTF over `Taamey-D/font-m-TaD/Taamey_D.ttf` in the
   working tree, run

       ./.venv/Scripts/python.exe py/main_taamey_d.py qa

   read every printed result and `git status --porcelain Taamey-D/qa-out`, then restore the
   tracked files with `git restore Taamey-D/font-m-TaD/Taamey_D.ttf Taamey-D/qa-out`. Expected:
   no `FAIL`, no `SKIP`, and no changed report. The anchor-family lint runs inside `qa`. A
   changed report is a finding that stops the plan until explained.
7. Record the spike's results, dated, in "Ledger" below, with the scratch scripts' paths.

## Phase 2: the dependency change, one commit

1. Add `ufo2ft` and `brotli` to `requirements.txt` under a comment naming the build and the
   WOFF2 writer; `fonttools` is already there. Install them into `./.venv`.
2. Regenerate `constraints.txt` as `doc/clone-forests.md`, "Environments", says: capture
   `-m pip freeze` in a uniquely named scratch script and write the file explicitly as UTF-8
   with LF line endings; run `pip check`; read the diff (new pins: ufo2ft, brotli,
   booleanoperations, cffsubr, fontmath, and any of their dependencies).
3. Commit the two files, naming them in the message.

## Phase 3: the migration, committed as sources and outputs together

1. Add `Taamey-D/font-m-TaD/Taamey_D.ufo/` by rerunning the Phase 1 converter against the
   committed 1.2 TTF. The converter stays a scratch script; the commit message records the
   command, the TTF's commit, and the Phase 1 comparison results. (Tracked filenames: glif names
   are ASCII, so `py/tests/test_tracked_filenames.py` is satisfied.)
2. Add the GDEF block of Phase 1 step 3 to `Taamey_D.sym.fea`.
3. Remove `Taamey_D-nofea.sym.sfd`, `Taamey_D-nofea.sfd`, `Taamey_D.sfd` and
   `ffscript_generate_sfd_n_ttf.py` (decision 6).
4. Rewrite `py/main_taamey_d_build.py`: fill `Taamey_D.sym.fea` and `license.sym.txt` as now
   (the `attrib` read-only dance kept), then compile through a new
   `py/taamey_d_build/compile_font.py` holding Phase 1 step 4's logic. Fixed timestamps: keep
   `head.created` in `fontinfo.plist`; store the `head.modified` value as an ISO 8601 string with
   offset beside `VERSION` in `py/taamey_d_build/font_version.py`, changed with each release.
   Drop `--fontforge` and `find_fontforge`.
5. `py/tests/test_taamey_d_build_imports.py`: allow `fontTools`, `ufo2ft`, `ufoLib2` (decision
   8); rewrite the docstring's reason; drop the sentence about the FontForge script.
6. `py/taamey_d/release.py`: choose the source list by snapshot source commit. Snapshots whose
   source commit is an ancestor of the migration commit keep today's list (the FontForge script,
   `Taamey_D-nofea.sym.sfd`); later snapshots use the new list: every file under
   `Taamey_D.ufo/`, `Taamey_D.sym.fea`, `license.sym.txt`, `license.txt`, and the build's entry
   point and package. `_validate_archive_against_git` and the archive-member refusal (today:
   plain `.sfd` and `.fea`) follow the same choice; after the migration the tool refuses any
   `.sfd`, any plain `.fea`, and any built font in a source archive. `release-check` must still
   pass for the 1.2 snapshot.
7. `.gitattributes`, the FontForge lines (`Taamey-D/**/*.sfd` and `*.fea`): retire the `.sfd`
   line-ending rules that no longer apply; `*.glif` and `*.plist` are ordinary LF text.
8. Docs that name FontForge, each rewritten to the new build: `Taamey-D/README.md` ("What is
   where", "Authored sources and generated outputs", "Building the font", "Publishing a
   release"), `AGENTS.md` ("The font's FontForge build"), `README.md` ("hand-run FontForge
   build"), `DATA-LICENSES.md` (the `font-m-TaD/`, build and downloads rows),
   `Taamey-D/LICENSE.md` (the FontForge-script sentences), the comments in `py/main_0_mega.py`
   at the `taamey-d-doc` and `taamey-d-qa` steps. If decision 4 is yes: a `taamey-d-build` step
   before `taamey-d-qa`, and the `NOT_IN_MEGA` entry removed from
   `py/tests/test_mega_coverage.py`.
9. Never touched: `in/font-support/taamey-d-1.2/` (hash-pinned by
   `py/py_html/taamey_d_assets.py`; the immutable record of 1.2's FontForge build),
   `gh-pages/taamey-d/downloads/` (append-only snapshots), `gh-pages/woff2/Taamey_D.woff2`
   (changes only through a new pin), `Taamey-D/qa-in/` (no baseline change is expected or
   allowed here).
10. Run the build, then `qa` and `doc`; read every result. Run Black on the changed Python.
    Commit the sources, the build, the lint, the release tool, the docs and the three
    regenerated font files together, with the Phase 1 comparison summarized in the message.

## Phase 4: release 1.3, outward-facing, only on Ben's go-ahead (decision 7)

Follow `Taamey-D/README.md`, "Publishing a release": set `VERSION` and the modified timestamp,
rewrite `Taamey-D/font-m-TaD/release-notes.txt` (first line `Taamey D 1.3`; the notes say the
build moved to fontTools and ufo2ft and the shaping is unchanged), build, `doc`, `qa`, commit,
`release-publish --snapshot-commit <full HEAD>`, `release-check`, commit the snapshot, `latest/`
and the index. A new pin into `in/font-support/taamey-d-1.3/` follows `git log --
in/font-support/`, and a Pages dispatch needs Ben's go-ahead.

## Phase 5: follow-ons, each a separate decision, not part of this plan

- Derive `fill_in_template.py`'s `_WIDTH` and `_BELOW_INK` tables from the UFO at build time
  (advance widths and ink extents), removing two hand-maintained copies of glyph data.
- Drop the `-nofea` vocabulary from names and prose.
- Give `py/main_taamey_d.py qa` a `--font` option so a scratch build can be checked without
  overwriting the tracked TTF.

## Verification

- Phase 1 is the equivalence proof: the table comparison and a `qa` run with no changed
  report. Expected unchanged after Phase 3: `Taamey-D/font-m-TaD/Taamey_D.fea` apart from the
  added GDEF block, `license.txt`, every file of `Taamey-D/qa-out/`, both pages that `doc`
  writes, `gh-pages/woff2/Taamey_D.woff2`, `in/font-support/taamey-d-1.2/`,
  `gh-pages/taamey-d/downloads/`. Expected changed: `Taamey_D.ttf`, `.woff` and `.woff2`
  (listed table by table), and the files Phase 3 names.
- Before the push that carries Phase 3: the full suite and the mega, as `AGENTS.md` requires of
  a push to `main`:

      ./.venv/Scripts/python.exe py/main_test.py

      ./.venv/Scripts/python.exe py/main_0_mega.py

  A failing step or an unexplained tracked diff is a failure. `taamey-d-release-check` must pass
  for the 1.2 snapshot with the per-commit source list.
- Determinism: run the build twice into scratch directories and compare the three font files
  byte for byte, which is also what `release-publish` does before installing a snapshot.
- Risk, on both axes: product reach is `Taamey-D/` (distributed data) and the generators; the
  site changes only through Phase 4's pin and dispatch. Everything in Phases 1 to 3 is local and
  reversible until pushed; Phase 4 is outward-facing.

## Ledger

| Id | Requirement | Status |
|----|-------------|--------|
| R1 | Replace FontForge as the compiler with a pip-installed one | active, awaiting decisions 1 and 3 |
| R2 | Replace the SFD as the glyph source with a UFO | active, awaiting decisions 2 and 6 |
| R3 | Prove shaping equivalence on the whole corpus before any tracked change | active (Phase 1) |
| R4 | Keep the 1.2 snapshot, pin and downloads immutable | active |
| R5 | Release 1.3 from the new build | deferred to decision 7 |
| R6 | Put the build in the mega | awaiting decision 4 |
