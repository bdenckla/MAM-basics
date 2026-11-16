# Upkeep and product shape: MAM-morphhb and MAM's text (2026-11-15)

Written by a read-only research sub-agent of Claude (Opus 5.5) on 2026-11-15 for questions 4
and 5 of the morphhb-on-MAM feasibility study. The harness refused the sub-agent's own write of
this file, so it returned the text and the root session saved it here, condensed. Its scripts
are in `scripts/` and their outputs in `out/` beside this file. Not reviewed by a human. Nothing
tracked changed; Git was read only through `git log`. The checkout's HEAD was then `f689951f`,
whose commits after `374d9436` touch only `DATA-LICENSES.md`, `doc/commander-prompt.md` and
`dot-claude/skills/hebrew-prose/SKILL.md` (checked by the root session with `git diff
--name-only 374d9436 HEAD`).

**Tracked copy, 2026-11-16.** This file was tracked in
`morphhb-on-mam/research/upkeep-shape/` when the study was put on ice, with the five files
of `out/` that it and `../CHECKED.md` name. The scripts and the rest of `out/` stayed
untracked in the study folder, `.novc/morphhb-on-mam-2026-11-15/research/upkeep-shape/`
(`morphhb-on-mam/README.md`, "What is not tracked").

## A. How MAM-morphhb is made today

`py/main_mam_morphhb.py` writes `MAM-morphhb/MAPM.xml` from MAM-simple's JSON in the BHS
numbering (`py/mam_morphhb/morphhb_runner.py` line 86, `resolve_book_group_path(...,
vtrad="bhs")`) and validates it against OSIS 2.1.1. `MAM-parsed/plus/` supplies only titles,
the Torah's parashot and poetic line breaks (`morphhb_plus.py`). Rendering is a closed dispatch
on MAM-simple's (type, class) pairs: `morphhb_inline.render` raises on an unknown pair, and
`HANDLERS` with the four structural types that `morphhb_runner._Writer` handles covers exactly
the 37 pairs present (`out/dual_cant_and_census.txt`); plus/ templates pass
`validate_current_plus_template` and an unprojected name raises.

- Ketiv/qere: each of the 1,047 pairs becomes an `x-ketiv` seg and an `x-qere` seg in MAM-simple's
  order. The 149 trivial pairs (`kq-trivial`) pass through unmarked as one pointed form, which at
  all 128 comparable verses is the template's first parameter (`out/kq_trivial_check.txt`). The 8
  ketiv words without qere and 9 qere words without ketiv become `x-ketiv-velo-qere` and
  `x-qere-velo-ketiv` segs.
- Maqaf: an ordinary maqaf is text; a gray maqaf (`implicit-maqaf`, 116) becomes an
  `x-implicit-maqaf` seg.
- Legarmeh (1,787) and narrow-sense paseq (508, in `x-paseq` segs) are written with U+05C0.
- Dual cantillation: only `cant-combined` is written, in 24 verses (Genesis 35:22; Exodus 20:2-6,
  8-10, 13-15; Deuteronomy 5:6-10, 12-15, 17-19).
- Special letters become `x-small`, `x-big` and `x-suspended` segs; 94 notes.
- OSIS vocabulary: 22 element types, verse milestones (23,211 verses; Joshua 21:36-37 skipped),
  `l`/`lg` for poetic lines, 12 seg types; no `<w>` element (`out/mapm_vocab.json`). The line
  layout serves OpenScriptorium's line-by-line importer (`MAM-morphhb/README.md`).

Open: whether `<w>` elements could be added without breaking that importer was not examined.

## B. Declared product status

MAM-morphhb is tier-2 distributed data (`py/product_scopes.py`, `_PRODUCT_DIR_NAMES`), and its
generator is hand-run, outside the mega (`py/tests/test_mega_coverage.py`,
`NOT_IN_MEGA["py/main_mam_morphhb.py"]`). By Ben's decision of 2026-11-03 (AGENTS.md, the
products section; commit `825032c0`), a refresh of MAM's text does not oblige rerunning it, so it
may lag MAM-simple; any other change to the generator or its inputs still does. A morphology
layer would be such an input, and one meant to follow MAM's text would need a mega step, the
hand-run rule, or a new exemption: Ben's choice.

## C. Upkeep

**The rule.** AGENTS.md, the paragraph beginning "A product derived from MAM's text takes each
Wikisource refresh": such a product gets no hashes, fingerprints or pinned populations; its
deterministic checks are closed dispatch, or a check that a hand-made statement still holds,
covering exactly what the statement depends on. The `mam-wikisource-refresh` skill
(`dot-claude/skills/mam-wikisource-refresh/SKILL.md`, "Judge every diff") predicts each refresh's
changes verse by verse with `py/main_diff.py mpplus`, checks that the predicted changes and only
they appear in each product, and repairs a failing statement in one reviewable edit; its
`references/dependent-refresh.md` lists the checks a text change can trip.

**How much MAM's text changes.** The change logs in `gh-pages/MAM-with-doc/change-log/` record
releases, not refreshes, so the sub-agent measured the 52 Wikisource downloads committed to
`in/mam-ws/` from 2026-03-12 to 2026-11-10 (`scripts/refresh_census.py`,
`scripts/classify_pairs.py`, `out/refresh_table.md`), classifying each changed verse through a
closed dispatch over the 48 template names present:

- per download: median 3.5 changed verses (mean 13.0, maximum 133 in a template migration), of
  which a median of 1 changed text, ketiv/qere or an alternative form; none in 22 downloads;
- over the year, 677 verse changes: letters 3 (Lamentations 4:3, Joshua 10:24, Zephaniah 2:9);
  atoms split or joined 0; ketiv/qere structure 192 (133 in the 2026-04-20 trivial-pair migration,
  37 in the 2026-05-03 migration); ketiv or qere forms inside trivial templates 10; pointing 10
  (rafeh or varika marks; the one change to a vowel point proper is a qamats that became a qamats
  qatan at 2 Kings 22:1); accents 6; meteg marks 134 verses; narrow-sense paseq and legarmeh 4;
  other characters 2; alternatives only 4; layout 1; markup 8; documentation notes only 301;
- since the 2026-09-16 change-log boundary: 19 downloads changed 105 verses, only 12 in text or
  ketiv/qere (6 atoms), exactly the 12 entries of `unpinned-latest.json`
  (`out/crosscheck_unpinned.txt`).

Open: the projection is the study's own and was validated only after 2026-09-16; counts are verse
changes, not verses; history before 2026-03-09 is not in MAM-basics.

## D. Precedents for per-word annotation

None of MAM-basics' products has stable word ids; each keys a word by verse and position, or by
its form, with the form as a guard.

- **Phonetic MAM** (mega step `phonetic-mam-export`) attaches transcriptions to each chanted word,
  keyed by verse and row order (`Phonetic-MAM/schema/phonetic-mam-public-v1.schema.json`).
  MAM-private's adapter aligns its source to current MAM, and the export stops on a verse it
  cannot reconcile. The closest precedent: an outside source aligned word by word to current MAM.
- **Near-Aleppo**'s `in/near-aleppo/*-pointed-ketiv.json` records key a target by book, chapter,
  verse, an index and a path, and store the ketiv/qere forms as a guard: a changed letter or mark
  of the qere stops the build (`py/near_aleppo/frozen_ketiv.py`), and every record must be used.
- **Yeivin-ITM**'s quoted forms (`py/yeivin_itm/quoted_forms.py`) and **Taamey D**'s corpus key by
  the form; **Holman**'s table keys by verse plus segment number, verified by form.
- MAM-parsed, MAM-simple, MAM-with-doc, MAM-for-Sefaria, MAM-OSIS and MAM-morphhb attach nothing
  per word.

Open: Phonetic MAM's adapter, in MAM-private, was not read.
