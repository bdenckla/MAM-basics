# Evacuate all Python from codex-index-aleppo, -leningrad and -cam1753 into MAM-basics

Written 2026-08-02. Governed by [PLAN-evacuate-python-programme.md](PLAN-evacuate-python-programme.md).
**Last in the order.** One plan for three repos, because they share a shape, share two fork
families, and share a vendoring problem — doing them separately would answer the same question
three times and risk answering it three different ways.

## Status

| Phase | State |
|---|---|
| 0 — reconcile the fork families (programme Phase 0, plus the wiki family below) | **DONE 2026-08-22.** Programme Phase 0 confirmed rather than re-derived — fourteen of its sixteen files still one committed blob, `check_all.py` and `check_word_finding.py` per-repo permanently on Ben's decision of 2026-08-19. **Family 2 needed no design call**: on committed blobs **two** of the eight shared wiki module names differ, not four, and `mam_book_names.py` — the 230-line "real work" — is **one blob** and was one on 2026-08-02, the "230 lines" being 115 + 115 of whole-file diff caused by codex-index-aleppo's CRLF checkout. The two that do differ, `main_make_wikisource_page.py` and `write_wikitext_file.py`, are **two tools against two input formats**; Phase 3 names them. `hebrew_letters.py` and `my_utils.py` genuinely differed and `6ccd856` (leningrad, 2026-08-03) reconciled both with a black run. **The baselines are stale in eight places** and the inventory was right where this plan was wrong, for the second time in the programme. **Item 2's sweep finds two depth walks and the verdicts are opposite** — `flat_index.py` right in both repos but naming a file absent here, `page.py` right in codex-index-cam1753 and wrong here. **Item 3's wall is already up**: the four shared `check_*`/`fix_*` are two blobs, MAM-basics against the trio, and five top-level names are taken. **Item 4 landed** — `a171dd4` in codex-index-aleppo and `ef5525d` here, both copies byte-identical at md5 `f330012f28fdad782776c08ffbdb7b4b`; mgketer's third copy reported, MAM-private not written to. Two findings the phase turned up and did not fix: **`aleppo-wiki/main_make_wikisource_page.py` has been dead since 2026-03-28**, naming a directory `aleppo/` a rename removed, and **codex-index-aleppo's `check_word_finding.py` fails 160 of 160** comparing a `"1of2"` column identifier against the integer 1, since 2026-03-14. A third: **`codex-index-cam1753/check_line_breaks.py` writes CRLF** where codex-index-aleppo's copy writes LF, one missing `newline=""` — the programme Phase 0 defect in a seventh script, which dirties that repo's tree on any verification run. **Corrected 2026-08-22, after the first draft of this record**: the `parents[2]` question does **not** become live here. Only **three** copies of `mb_cmn/provenance.py` exist anywhere — MAM-basics, MAM-simple, MAM-private's `al-hatorah/` — all byte-identical and all with `parents[2]` resolving correctly; **none of the trio and not diffable-pointed-hebrew holds the file at all**, so there is nothing to re-vendor. And the fact that decides the question turned up with it: **walking to `.git` would regress al-hatorah**, a subtree of MAM-private rather than a repo, renaming three tracked breadcrumbs to the wrong tree — this step's own "a `.git` walk cannot find a subtree" lesson arriving at the file the question is about |
| 1 — two roots, no cwd (per repo) | **not started.** Phase 0 hands it a working oracle for codex-index-leningrad's wiki half and none for codex-index-aleppo's; repoint that repo's four `aleppo/` literals first, so the rest of the phase has something to prove itself against. It also owns the one-argument `newline=""` fix in `codex-index-cam1753/check_line_breaks.py:654` |
| 3 — copy the Python in (per repo, dual residency) | **not started** |
| 4 — empty each repo | **not started** |
| 6 — breadcrumbs and issue citations | **not started** |
| 7 — cross-repo bookkeeping | **not started** |

## Baselines — measured 2026-08-02 — **STALE in eight places; re-measured in the Phase 0 record below**

**Do not quote a figure from this table.** Phase 0 re-measured every cell on 2026-08-22 and the
superseding table is under "The baselines are stale in eight places". The `mb_cmn` row's three
`DIFFERS` verdicts are the worst of them: all four of codex-index-aleppo's `py/mb_cmn/` files and
all three of codex-index-cam1753's are byte-identical to MAM-basics', and `doc/vendoring-inventory.md`
said so the whole time.

| | codex-index-aleppo | codex-index-leningrad | codex-index-cam1753 |
|---|---|---|---|
| tracked `.py` | 44 | 38 | 22 |
| lines | 8,223 | 4,358 | 5,386 |
| tracked total | 223 | 88 | 172 |
| last commit | **2026-08-02** | 2026-07-27 | **2026-04-27** |
| Pages workflow | `pages.yml` | none | none |
| vendored `mb_cmn` | 4 in `py/mb_cmn/` + 4 in `aleppo-wiki/py/`, **DIFFERS** | 4 in `lenin-wiki/py/`, **DIFFERS** | 3 in `mb_cmn/`, 2 identical + `str_defs.py` **DIFFERS** |
| oracle | `line-breaks` 35, `column-coordinates` 35, `aleppo-wiki` 26, `MAM-XML` 24, `ds-flat-stream` 8, `gh-pages` 4 | `lenin-wiki` 21 | `cam1753-col-quads` 28, `cam1753-line-breaks` 27, `cam1753-spread-splits-doc` 15, `MAM-XML` 24 |

`aleppo-pages` (37), `cam1753-pages` (28) and `cam1753-spreads` (14) are downloaded scans, not
generated artifacts — they are inputs to the oracle, not part of it. Confirm that reading against
each repo's `download_*.py` before relying on it.

---

## All three move, and dormancy is not a reason to treat one differently

codex-index-cam1753 has not been committed to since **2026-04-27** and has no Pages workflow;
codex-index-leningrad last moved 2026-07-27 and also has no Pages workflow; only codex-index-aleppo
is unambiguously live. **This plan's first draft proposed asking whether cam1753 was worth doing at
all. Ben, 2026-08-02: it is low cost and symmetric with the other two, so it is in.**

That is the right reading, and the draft's was not. cam1753 is 22 `.py` of which 3 are vendored,
so the move proper is 19 files — the smallest in the programme. The expensive part for that repo
is reconciling the fork families, and **that has to happen whether or not a line ever moves**:
three drifted copies of one script are three chances to fix a bug once and leave it broken twice,
and the dormant copy is precisely the one that stays broken. Having paid that, stopping short of
the move would leave the repo tracking Python for no gain, and would make it the one exception a
future session has to rediscover the reason for.

---

## Phase 0 — the execution record — **DONE 2026-08-22**

**Family 2 is classified and there is no design call in it.** The prescription below expects
`mam_book_names.py`, at 230 differing lines, to be the phase's real work and possibly a fork into
one parameterized module plus two data tables. Measured on committed blobs 2026-08-22, that file is
**one blob** across `codex-index-aleppo/aleppo-wiki/py/` and `codex-index-leningrad/lenin-wiki/py/`
— `e7d29128`, 115 lines each side — and it was already one blob on 2026-08-02, the day the
prescription was written. **Two of the eight shared module names differ, not four**, and both are
plainly two tools rather than one tool with drift, which the prescription itself sanctions landing
under two names. The gate this phase could have tripped was not tripped, and nothing was chosen on
Ben's behalf.

**One commit in codex-index-aleppo and five here.** `a171dd4` there and `ef5525d` here are the two
halves of the one edit item 4 of the programme's Order hands this step, and are the only code
change this phase made. The other four here are all prose: `eca7f14` backfilled `ef5525d`'s own
hash, `0ea8d3e` recorded the CRLF defect a verification run turned up in codex-index-cam1753,
`1e36d56` corrected the provenance claim below, and `4682adf` repaired the sentence you are reading,
which said "one commit in each of two repos" and was true for about an hour.

### Preconditions — one mismatch, benign

MAM-basics is at **`90487af`**, not the `a606e43` the task named. `a606e43` is an ancestor and two
commits have landed since — `28a3208` (ruff `target-version` py311 → py313) and `90487af` (delete
`check_keys.py`) — neither touching anything this phase reads. Tree clean, nothing unpushed, in all
four repos before and after.

Everything else matched exactly: suite **945 passed, 5 skipped, 59 subtests** in 109s via
`.venv\Scripts\python.exe py\main_test.py -q`; `py\check_all.py` **7 of 7**, mark order over **298**
files, escapes over **241** `.py`. The `59 subtests` figure reproduced for the fifth measurement
running, so Phase 1 of the book-of-job plan was right to correct holman-ketiv-qere's Finding 3 back.

### The baselines are stale in eight places, and the instrument is why in three of them

Re-measured 2026-08-22. The prescription's table is left as written below; this one supersedes it.

| | codex-index-aleppo | codex-index-leningrad | codex-index-cam1753 |
|---|---|---|---|
| tracked `.py` | 44 *(unchanged)* | **21** *(was 38)* | 22 *(unchanged)* |
| lines | **8,284** *(was 8,223)* | **2,524** *(was 4,358)* | **5,443** *(was 5,386)* |
| tracked total | **222** *(was 223)* | **73** *(was 88)* | **176** *(was 172)* |
| last commit | **2026-08-19 `98021de`** *(was 2026-08-02)* | **2026-08-04 `0904b16`** *(was 2026-07-27)* | **2026-08-19 `f56831c`** *(was 2026-04-27)* |
| Pages workflow | `pages.yml` *(unchanged)* | none | none |
| `CLAUDE.md` | yes, `77cc57b` | **yes, `69ef5c6`** | **yes, `77b5e60`** |
| vendored `mb_cmn` | 4 in `py/mb_cmn/` **all identical**; 4 in `aleppo-wiki/py/`, **1 identical + 3 DIFFER** | 4 in `lenin-wiki/py/`, **1 identical + 3 DIFFER**, plus `vendoring_sync.py` at the root, **DIFFERS and unrecorded** | 3 in `mb_cmn/`, **all identical** |

Every oracle-tree count in the prescription's table reproduced unchanged — aleppo `line-breaks` 35,
`column-coordinates` 35, `aleppo-wiki` 26, `MAM-XML` 24, `ds-flat-stream` 8, `gh-pages` 4;
leningrad `lenin-wiki` 21; cam1753 `cam1753-col-quads` 28, `cam1753-line-breaks` 27,
`cam1753-spread-splits-doc` 15, `MAM-XML` 24 — as did the three downloaded-scan trees,
`aleppo-pages` 37, `cam1753-pages` 28, `cam1753-spreads` 14. **New since 2026-08-02**: leningrad and
cam1753 each have a `page-snips/` of 2 files.

**Where each stale figure came from:**

- **leningrad's `.py` count, line count and tracked total** moved because `d5195e3` (2026-08-03)
  dropped `UXLC-utils-sparse/py`, which is UXLC-utils' Phase 5 doing exactly what the section below
  records. 38 − 17 = 21.
- **All three "last commit" dates** are pre-Phase-0 and pre-`CLAUDE.md`. The prescription's
  "codex-index-cam1753 has not been committed to since 2026-04-27" was already wrong when the
  programme's Phase 0 re-measured it on 2026-08-19, and is wronger now.
- **Phase 4's "None of the three has a `CLAUDE.md` — codex-index-aleppo does, the other two do
  not"** is both self-contradictory as written and now false in the direction it did not intend.
  **All three got one on 2026-08-03**, one day after this plan was written. Phase 4 updates three
  files, not one, and writes none from nothing.
- **The three `mb_cmn` verdicts** are the instrument. aleppo's `py/mb_cmn/` reads `DIFFERS` here
  and all four files are the same blob as MAM-basics'; cam1753's `str_defs.py` reads `DIFFERS` and
  is identical. **`doc/vendoring-inventory.md` had all seven trio rows right the whole time** —
  `eol-only` where this plan says `DIFFERS`, `identical` where it says `DIFFERS` — so this is the
  second time a plan in this programme has been the stale record and the inventory the accurate one, book-of-job's Phase 0 being the first.
  Read the inventory before quoting a vendoring verdict from a plan.

### Family 2 — the classification, on committed blobs

`git -C <repo> rev-parse HEAD:<path>`, never `cmp` or `diff` on a checked-out file.

| Module | Prescription said | Blob verdict 2026-08-22 | What it is |
|---|---|---|---|
| `main_make_wikisource_page.py` | differs, 50 lines | **DIFFERS** (21 vs 29 lines) | two tools |
| `py/write_wikitext_file.py` | differs, 139 lines | **DIFFERS** (79 vs 134 lines) | two tools |
| `py/mam_book_names.py` | differs, 230 lines | **IDENTICAL** `e7d29128` | never forked |
| `py/my_utils.py` | differs, 2 lines | **IDENTICAL** `a4007d77` | forked, reconciled 2026-08-03 |
| `py/hebrew_letters.py` | differs, 2 lines | **IDENTICAL** `8e0f696f` | forked, reconciled 2026-08-03 |
| `py/my_open.py` | identical | **IDENTICAL** `ffdf54f2` | never forked |
| `py/hebrew_punctuation.py` | identical | **IDENTICAL** `bfa3379b` | never forked |
| `py/hebrew_verse_numerals.py` | identical | **IDENTICAL** `0d0c1c7f` | never forked |

**Three of the four "differs" verdicts are the CRLF instrument, and the fourth is a real diff.**
`git ls-files --eol` says codex-index-aleppo holds all 11 of its `aleppo-wiki/*.py` as **CRLF** in
the working tree and codex-index-leningrad all 18 of its `lenin-wiki/*.py` as **LF**, both with an
LF index and `* text=auto eol=lf`. So a `cmp` or `diff` across the two on 2026-08-02 reported
`differ` for every pair whatever the content was — **the same fault that cost the programme's Phase
0 four of its sixteen verdicts, arriving in this plan's table on the same day.** The numbers say
so too: "50 lines" is 21 + 29 and "230 lines" is 115 + 115, both of them a whole-file mismatch
counted twice, where "139 lines" is a real diff of a genuinely differing pair.

**The two 2-line divergences closed themselves, and dating them settles that they were real.** At
the 2026-08-02 heads — aleppo `3f46a3b8`, leningrad `9a2a2e39` — `hebrew_letters.py` and
`my_utils.py` did differ, and `mam_book_names.py`, `my_open.py`, `hebrew_punctuation.py` and
`hebrew_verse_numerals.py` did not. **`6ccd856` in codex-index-leningrad, 2026-08-03, "Reformat the
two files black 26.5.1 had not reached", changed exactly those two files by exactly one line each**,
and both pairs have been one blob since. The drift was a black version difference and a routine
reformat ended it. So the prescription's figures for those two rows were right, and its diagnosis —
"diverged `mb_cmn` copies" needing a decision about which 2-line delta to keep — described something
that had a day left to live.

**`hebrew_letters.py` went further and is now byte-identical to MAM-basics' `py/mb_cmn/`.** Of the
four vendored `mb_cmn` copies in each wiki tree, that one is `8e0f696f` in all three repos. The
other three differ from MAM-basics, and the three divergences are of three different kinds:

- **`hebrew_verse_numerals.py`: one line, and it is the packaging.** `from mb_cmn import
  hebrew_letters as hl` in MAM-basics against `import py.hebrew_letters as hl` in both wiki trees.
  Not drift at all — an adaptation to the wiki trees' layout, where every intra-tree import is
  spelled `py.<name>` because the entry point sits one level above a `py/` package. It dissolves
  the moment the code lives in MAM-basics.
- **`hebrew_punctuation.py`: MAM-basics moved on.** MAM-basics has `MAQ_RE` and `NU_GMAQ`, four
  lines the wiki copies never got; the wiki copies keep a trailing `# ׆` comment on `NUN_HAF`.
  Droppable in both directions.
- **`my_utils.py`: a widened signature with no caller.** The wiki copies' `dv_dispatch(fn_table,
  dic, *extra_args)` calls `fn_table[key](*extra_args, val)`, against MAM-basics'
  `dv_dispatch(fn_table, dic)`. **`git grep dv_dispatch` finds no call site in either wiki tree**,
  and MAM-basics has sixteen call sites in eight modules, every one passing two arguments. The wiki copies also import
  `itertools.groupby` and use it only inside a comment saying it is no longer used. Both are
  droppable drift, and the widening is dead code rather than a fix worth taking upstream.

### Family 2 — what the two genuinely differing modules are

**Two tools against two input formats, and this is not a close call.**

`aleppo-wiki/main_make_wikisource_page.py` reads a hand-made CSV, J David Stark's Aleppo Codex
index, writes a flat JSON, groups it by book and emits the wikitext.
`lenin-wiki/main_make_wikisource_page.py` reads `UXLC-utils-sparse/data/lci_augrecs.json`, dumps an
annotated stage-0 JSON, collapses rows, groups by book, dumps a stage-2 JSON and emits the wikitext.
Three of the four steps have no counterpart in the other pipeline and the two share no data file.
`write_wikitext_file.py` differs the same way and by more — leningrad's is 134 lines to aleppo's 79,
and it pulls in `image_urls`, `masorah_finalis_lines`, `get_cvm_rec_from_bcvt`, `vtrad_helpers` and
`my_locales`, none of which aleppo has.

So the prescription's "if the answer is that they are two tools, say so and land them under two
names" is the answer, **and choosing the two names is Phase 3's, not this phase's**. The name
collision that forces it is real: `main_make_wikisource_page.py` is one of the five entry-point
collisions the programme's Cross-cutting finding 1 lists.

**The nine leningrad-only modules and the aleppo/leningrad pairs are the same finding.** Aleppo's
`read_csv_file.py` / `group_by_book.py` / `book_names.py` against leningrad's `read_json_file.py` /
`s1_collapse_rows.py` / `s2_group_by_book.py` are two readers of two formats and two groupers under
two names already. They need no reconciliation, only two homes.

### The wiki trees are a far bigger vendoring fork than the inventory can see

**The prescription calls the four small ones "diverged `mb_cmn` copies", and that undercounts by
better than two to one.** Measured 2026-08-22 by comparing each wiki module against MAM-basics'
tree:

| Wiki module | MAM-basics counterpart | In the inventory? |
|---|---|---|
| `hebrew_letters.py` | `mb_cmn/hebrew_letters.py` | yes |
| `hebrew_punctuation.py` | `mb_cmn/hebrew_punctuation.py` | yes |
| `hebrew_verse_numerals.py` | `mb_cmn/hebrew_verse_numerals.py` | yes |
| `my_utils.py` | `mb_cmn/my_utils.py` | yes |
| `mam_book_names.py` | `mb_cmn/mam_bknas.py` | **no — renamed** |
| `my_open.py` | `mb_cmn/file_io.py` | **no — renamed** |
| `my_locales.py` *(leningrad)* | `mb_cmn/bib_locales.py` | **no — renamed** |
| `mam_book_names_and_std_book_names.py` *(leningrad)* | `mb_cmn/mam_bknas_and_std_bknas.py` | **no — renamed** |
| `vtrad_data.py` *(leningrad)* | `py_misc/vtrad_data.py` | **no — wrong package** |
| `vtrad_helpers.py` *(leningrad)* | `py_misc/vtrad_helpers.py` | **no — wrong package** |
| `get_cvm_rec_from_bcvt.py` *(leningrad)* | `py_misc/get_cvm_rec_from_bcvt.py` | **no — wrong package** |
| `vendoring_sync.py` *(leningrad root)* | `mb_cmn/vendoring_sync.py` | **no — loose file** |

**Six of aleppo-wiki's 11 modules and eleven of lenin-wiki's 18 are copies of MAM-basics modules,
plus leningrad's root `vendoring_sync.py`. The inventory records eight of those eighteen.** Common
ancestry is not in doubt for any of them: `my_locales.py` is `bib_locales.py` with `book39` renamed
`book39tbn` through the same comment block and one function added, `my_open.py` is `file_io.py` with
the same eight functions, `mam_book_names.py` is `mam_bknas.py` plus a `mam_book_path` and one
constant made public, and `get_cvm_rec_from_bcvt.py` differs in an enum MAM-basics has since made
(`CVVE_TYPE_SAME_CONTENTS` → `CvveType.SAME_CONTENTS`) and one dictionary rename
(`BCV_DIC_FROM_MAM_TO_XXX` → `_TO_YYY`).

**This widens the programme's Cross-cutting finding 2 rather than repeating it.** That finding says
`pkg_scan_roots` is hand-maintained and cannot see a loose file or an unlisted package, and
prescribes reading each repo's `main_update_vendored_files.py` and comparing its
`_VENDORED_PACKAGES` against the inventory. **That prescription finds nothing here**:
codex-index-leningrad's `main_update_vendored_files.py` names no MAM-basics package at all — it
syncs `UXLC-utils-sparse` from `../UXLC-utils`, exactly as `in/vendoring_policy.json`'s comment for
that repo says — and codex-index-aleppo and codex-index-cam1753 have no such script. **A copy under
a different name, or out of the package it came from, is invisible to both the scan and the
cross-check.** codex-index-leningrad's `pkg_scan_roots` is `{}`; its four recorded rows come from
the `overrides` list, which is why Phase 7 item 1 has eight override rows to delete.

**`vendoring_sync.py` at leningrad's root differs from MAM-basics' by two lines** and they are the
same line twice: `_provenance.md` against `provenance.md`, in a docstring and in the path
`dest_dir / "provenance.md"`. A genuine local adaptation — that repo's breadcrumb is
`UXLC-utils-sparse/provenance.md`, without the leading underscore — and it disappears with the
script it serves.

### Item 2 — the depth sweep, and the two verdicts are opposite

`git grep -nE 'parents\[|\.parent\.parent|repo_root|Path\(__file__\)'` over both reconciled
packages, in all four repos that hold one, on the whole package and not only the files that had
diverged. **All ten files are still one blob with their codex-index counterpart**, verified on blobs
— the six of `py_ac_word_image_helper/` between MAM-basics and codex-index-aleppo, `alef_bet_to_ascii.py`
at `0c20729e` before this phase's edit and `codex_page.py` at `38b42533`, and the four of
`py_cam1753_word_image/` between MAM-basics and codex-index-cam1753.

**The sweep finds exactly two depth-counting walks, and `codex_page.py`'s `repo_root()` is the
third site, already fixed by the programme's Phase 0.** book-of-job's Phase 3 left both, and
re-checking rather than inheriting was worth doing, because one of its two readings needs a
correction:

- **`py_ac_word_image_helper/flat_index.py:7`** — `Path(__file__).resolve().parent.parent.parent`.
  The package sits under a `py/` in both repos, so the walk lands on the repo root in both, and
  book-of-job's Phase 3 is right that the move repaired it. **But the file it then names does not
  exist here.** `ROOT / "index-flat-annotated.json"` is a tracked file of codex-index-aleppo's and
  is absent from MAM-basics, so this repo's copy resolves a correct root to a missing target and
  raises on first read. Nothing imports it in either repo, which is why nothing has noticed. **The
  right root and a reachable file are two claims, and the move bought only the first.**
- **`py_cam1753_word_image/page.py:10`** — `Path(__file__).resolve().parent.parent`. Correct in
  codex-index-cam1753, where the package sits at the repo root; **wrong in MAM-basics**, where it
  names `py/` and the three directories it composes — `cam1753-line-breaks`, `cam1753-col-quads`,
  `cam1753-pages` — are absent. All three exist in codex-index-cam1753 and hold 27, 28 and 28
  tracked files. So book-of-job's Phase 3 reading holds exactly: inert here, live and correct
  there, and settle it in both repos at once or not at all.

**Phase 3 is where "at once" becomes possible, and it is also what forces the issue**: the moment
codex-index-cam1753's Python moves, `page.py`'s two-level walk is wrong in the only repo left
holding it, and its three directories stay behind as data. It wants `paths.sibling_repo` the way
`boj_paths.boj_data_root()` does, not a deeper walk.

### Item 3 — the `.git`-walk wall is already up, and it is taller here than at book-of-job

**A `.git` walk finds a repo root and cannot find a subtree.** book-of-job's Phase 3 met this and
forked four source lints to be told what they lint, through `py/boj_paths.py`'s `code_paths()`.
Re-measured here, that fork is already visible from the trio's side:

| Script | MAM-basics | codex-index-aleppo | codex-index-cam1753 |
|---|---|---|---|
| `check_mark_order.py` | `b8454750` | `b23e3764` | `b23e3764` |
| `check_escape_sequences.py` | `c8603671` | `23798624` | `23798624` |
| `fix_mark_order.py` | `1ada8b12` | `2add3471` | `2add3471` |
| `fix_escape_sequences.py` | `ba13cd41` | `d0d96439` | `d0d96439` |
| `check_all.py` | `29d2b7da` | `da7096ec` | `21989384` |

**The four are two blobs, not one: MAM-basics on one side and the two codex-index repos on the
other.** The programme's Phase 0 made all three repos one blob on 2026-08-19 and book-of-job's
Phase 3 re-forked MAM-basics' copies the same day, deliberately and with the reason recorded.
`check_all.py` is three-way distinct by Ben's decision of 2026-08-19 and always will be.

**So Phase 3 cannot land the trio's four under their own names at MAM-basics' `py/` top level:
those five names are taken.** Measured 2026-08-22, MAM-basics has 74 top-level `py/*.py`, and
codex-index-aleppo and codex-index-cam1753 each collide on all five —
`check_all.py`, `check_escape_sequences.py`, `check_mark_order.py`, `fix_escape_sequences.py`,
`fix_mark_order.py`. **codex-index-leningrad collides on none.** Against MAM-basics' module
basenames at any depth the collisions are wider: 20 for codex-index-aleppo, 12 for
codex-index-cam1753, 9 for codex-index-leningrad — the two word-image packages, the vendored
`mb_cmn` files, and each repo's `test_h_dot_below_nfc.py`.

**And `fix_mark_order.py` is the one that must not arrive unscoped.** It has no `main()`, no
dry-run and no `--apply`: it rewrites every file under the root it finds, at import. book-of-job's
Phase 3 records that it would have reformatted MAM-basics on sight. That is now a settled hazard
rather than a live one — MAM-basics' copy is already scoped to `boj_paths.code_paths()` — but the
trio's copies are not, and a session that copies one in before scoping it gets the same result.

**What this costs Phase 3, stated plainly: `boj_paths.py` has a counterpart per repo, or the trio
shares one.** The four lints already take a hand-maintained scope list; adding three more repos'
code to MAM-basics means either three more lists or one list that knows which repo each path belongs
to. The `page.py` and `flat_index.py` sites above want a data root each as well. `py/hkq_paths.py`,
`py/uxlc_paths.py` and `py/boj_paths.py` are three worked precedents and all three are per-repo, so
per-repo is the default unless Phase 3 finds a reason against it.

### Item 4 — the citation, fixed in both public copies at once

`py/py_ac_word_image_helper/alef_bet_to_ascii.py` said "Same scheme as mgketer
``hebrew_word_id.py`` and book-of-job ``author.py``". book-of-job has held zero Python since
2026-08-21; that file is **MAM-basics' `py/author_boj_util/author.py`**, having been book-of-job's
`pyauthor_util/author.py` until 2026-08-19. MAM-basics' copy therefore attributed to a sibling a
file MAM-basics itself holds, which is the sharper edge book-of-job's Phase 7 named.

The two public copies were byte-identical at md5 `5a25fbe8734f08553d0bc1c31521904c`, exactly as
that phase recorded, so both got the same edit and are byte-identical after it at
**`f330012f28fdad782776c08ffbdb7b4b`**. mgketer's counterpart gains its path for the same reason
the stale one lacked it: **a bare module filename is not greppable**, which is how this citation
stayed stale through four evacuations. A note in the docstring now says the two copies are one blob
and must be edited together, so the next reader does not have to find that out from a plan.

Landed as **`a171dd4`** in codex-index-aleppo and **`ef5525d`** here.
Verified after the edit: black clean on both, `check_mark_order.py` OK over 128 files and
`check_escape_sequences.py` OK over 44 `.py` in codex-index-aleppo, and 298 / 241 unchanged here.

**`MAM-private/mgketer/py/py_ac_word_image_helper/alef_bet_to_ascii.py:6` is reported and not
fixed.** It has the same stale sentence, and it is a third copy already diverged at md5
`c7d2c780664875449d98a55c2c567fbc` — an "Initially generated by GitHub Copilot" line, `\uXXXX`
escapes where the reconciled pair has literal Hebrew, and two double-spaces after a period. It is
no part of the blob and needs its own edit whichever way. **MAM-private was not written to**, per
the precedent UXLC-utils' Phase 7 item 6 set and holman-ketiv-qere's and book-of-job's followed.

### codex-index-aleppo has no working oracle on either half, and one of the two has been dead five months

The programme's Phase 0 recorded that codex-index-aleppo had no zero-diff oracle because two of its
four checks failed. Installing what its code actually imports moves that finding rather than
closing it, and turns up a second, worse one.

**`aleppo-wiki/main_make_wikisource_page.py` cannot run from any working directory.** Its four path
literals name a directory `aleppo/` that this repo does not have:

```
FileNotFoundError: [Errno 2] No such file or directory: 'aleppo/J David Stark Aleppo Codex Index.csv'
```

The tracked files are under `aleppo-wiki/`, and `9025037` (2026-03-28) "add aleppo-wiki/ (moved
from codex-index/aleppo)" is the rename that left the literals behind. **Nothing but black
(`c68c04e`) and the LF+NFC standards commit (`c1caebb`) has touched that tree since**, so the
generator has been dead for **five months** and its four tracked artifacts —
`index-flat.json`, `index-flat-corrected.json`, `index-grouped-by-book.json`, `index.wiki` — cannot
be regenerated. This is the plan's Phase 1 known offender
`aleppo-wiki/py/mam_book_names.py:114` in a worse form than the plan describes: the same
cwd-relative habit, but naming a directory that stopped existing rather than one that only resolves
from the right root.

**`lenin-wiki/main_make_wikisource_page.py` runs and is a real oracle.** From
`C:\Users\BenDe\GitRepos\codex-index-leningrad`, silent, exit 0. Its three tracked artifacts were
rewritten — mtimes bumped, checked — and all three came back **byte-identical** against
`git cat-file blob HEAD:<path>`. So Phase 1 has a zero-diff oracle for the leningrad half of Family
2 and none for the aleppo half.

**`check_word_finding.py` in codex-index-aleppo fails 160 of 160, on one cause, and it is a data
format the check was never updated for.** Installing Pillow and numpy got it past the import error
the programme's Phase 0 recorded, and it then reports `PASS: 0 FAIL: 160 TOTAL: 160`. Every one of
the 160 failures is a `col:` clause and **not one is a `line:` or a `word:` clause**, so the located
positions are right in all 160 cases. The column comparison is a string against an integer:
`col: found=1of2 expected=1`. codex-index-aleppo's line-break JSON has `"col": "1of3"`, a column
identifier of the form N-of-M, and book-of-job's `qr-ac-loc` `"column"` field has an integer.
**`eb4bcaf` (2026-03-14) "Add Deut support and migrate column IDs to NofM format" is where the data
changed, and `check_word_finding.py` has not been touched since `8be6cf9` (2026-03-15), a pure
move into `py/`.** So the check has compared incomparable values for five months and nobody has
seen it, because Pillow was missing from that repo's venv and the check could not import.

**codex-index-cam1753 passes 4 of 4**, and the contrast is the proof rather than a coincidence:
its line-break JSON keeps `"col": 1`, so its structurally identical check passes 160 of 160. This
is the second thing the programme's Phase 0 gate found these two files disagreeing about — the
first being the tolerance each allows a maqaf compound, one chanted word written as two atoms
joined by a maqaf, where codex-index-aleppo accepts an alternative word index and
codex-index-cam1753 an alternative line. **Two manuscripts, two layouts, two JSON schemas** was
right, and the column encoding is a third axis of it. Ben's decision of 2026-08-19 to leave
`check_word_finding.py` per-repo permanently is confirmed rather than reopened by this.

**Nothing here was fixed.** `check_word_finding.py` is one of the two files Ben settled as per-repo,
the fix is a change to a live check against live data, and this phase's job was to characterize.

### A third script in codex-index-cam1753 writes CRLF, and running the check is what showed it

**`codex-index-cam1753/check_line_breaks.py:654` is `out_path.write_text(html, encoding="utf-8")`,
and codex-index-aleppo's copy at `py/py_ac_loc/check_line_breaks.py:629` is the same line with
`newline=""`.** So the cam1753 copy writes CRLF into `check_line_breaks.html`, against that repo's
`.gitattributes` declaring `* text=auto eol=lf`, and the aleppo copy writes LF. The two copies are
not one blob and never were, `95ed146b` against `d27a2b93`.

**This is the programme's Phase 0 finding recurring in a seventh script**, that phase having found
exactly this one missing argument in codex-index-cam1753's `fix_mark_order.py` and
`fix_escape_sequences.py` and fixed both. `check_line_breaks.py` was outside the six scripts it
reviewed, so it kept the defect while its two neighbours lost it.

**It fires on a plain verification run, which is how it turned up here.** Running
`check_all.py` in codex-index-cam1753 left `git status --porcelain` reporting one modified file;
compared against `git show HEAD:check_line_breaks.html`, the verdict is **line-ending-only** — 11,014
bytes against 11,126, the difference being 112 carriage returns and nothing else. Restored with
`git checkout --`, so nothing was lost and the repo is clean. **The next run puts it back.**

**Not fixed, and the reason is ownership rather than doubt.** The fix is one argument, matching the
sibling repo's copy verbatim, in a repo whose `.gitattributes` already settles which line ending is
wanted. But it is a code change in a repo whose Python has not moved, and **Phase 1 is this plan's
IO-and-paths phase** — the same phase that has to repoint codex-index-aleppo's four dead literals.
Both belong there, and doing them together keeps the record of why in one place. Put to Ben
2026-08-22 as a thing he can have sooner if he would rather not wait for Phase 1.

### The two venvs, and `requirements.txt` wrong in both directions

`codex-index-aleppo` and `codex-index-cam1753` each track a `requirements.txt` naming **black,
matplotlib, pyspellchecker**, and each venv held **black and nothing else**. `codex-index-leningrad`
tracks none and needs none — its Python is stdlib only.

**Installing the tracked file would not have been enough, and installing it alone would have been
wrong.** What the code imports, measured with `git grep` for the import statements rather than read
off the declaration:

| Package | Declared | Imported by | Verdict |
|---|---|---|---|
| Pillow | **no** | 4 modules in codex-index-aleppo, 4 in codex-index-cam1753 | **missing from the declaration** |
| numpy | **no** | `py_ac_word_image_helper/crop.py`, `py_cam1753_word_image/crop.py`, `gutter_profile.py`, `split_cam1753_spreads.py`, `plot_col_coords.py` | **missing from the declaration** |
| matplotlib | yes | `py_ac_loc/plot_col_coords.py`, `gutter_profile.py` | correct |
| pyspellchecker | yes | **nothing, in either repo** | **declared and unused** |
| kraken | **no** | `py_ac_loc/kraken_seg_baselines.py` (codex-index-aleppo only) | **missing from the declaration** |

So both files omit the two packages without which nothing runs and name one that neither repo has
ever imported — there is no `check_spelling_in_html.py` in either. This is book-of-job's Phase 3
finding — read what the code imports, not only what `requirements.txt` declares — recurring with
the error in both directions instead of one. Both venvs now have `requirements.txt` plus Pillow and
numpy, which is a change to a gitignored venv and nothing else; `kraken` was not installed and
`kraken_seg_baselines.py` was not run.

**With that done, the programme's "no repo's `check_all.py` runs in its own venv" is half
retired.** codex-index-cam1753's now runs and passes 4 of 4 — word finding 160/160, escapes over 22
`.py`, mark order over 94 files, line-break JSON consistency OK. codex-index-aleppo's still exits 1,
now for two reasons neither of which is an import: `check_word_finding.py` above, and
`check_line_breaks` crashing with `ValueError: Unhandled tag <spi-invnun> in verse Ps.107.23` out of
`py_ac_loc/mam_xml_verses.py:116`. Its other two checks pass at the counts the programme's Phase 0
established after widening the root — **escapes over 44 `.py`, mark order over 128 files** — which
independently confirms `98021de` still holds.

### What Phases 1, 3 and 4 now owe, beyond what they already knew

1. **Phase 1 has an oracle for one of the two Family 2 halves and must say so rather than let an
   empty `git status` stand in for it.** codex-index-leningrad's wiki generator regenerates three
   artifacts byte-identical; codex-index-aleppo's regenerates nothing because it cannot start.
   Repointing its four literals from `aleppo/` to `aleppo-wiki/` is what gives that half an oracle,
   and it should be done **first in Phase 1**, before any other path work in that repo, so that the
   rest of the phase has something to prove itself against.
2. **Phase 3 names two tools, not one.** `main_make_wikisource_page.py` and
   `write_wikitext_file.py` each land twice under two names.
3. **Phase 3 cannot reuse five top-level names**, and `fix_mark_order.py` rewrites its root at
   import. Scope before copying, never after.
4. **Phase 3 folds two more `_Scope`s into `py/tests/test_h_dot_below_nfc.py`**, which has four
   today. codex-index-aleppo's copy is 319 lines and codex-index-leningrad's 304, and **the two
   differ**, so they merge into scopes rather than one scope serving both; codex-index-cam1753 has
   no copy. Diff their `_BINARY_EXTENSIONS` against this file's, as holman's phase did.
5. **Phase 3 has eighteen vendored copies to dispose of, not eight**, under four names that the
   inventory's `mb_cmn` scan cannot match: renamed (`mam_book_names`, `my_open`, `my_locales`,
   `mam_book_names_and_std_book_names`), out of package (the three `py_misc` modules), and loose
   (`vendoring_sync.py`). Every one is a plain deletion once the code imports MAM-basics' modules
   directly, and every one is a silent survival if it is missed.
6. **Phase 4 updates three `CLAUDE.md` files**, one per repo, all three of which exist.
7. **Phase 7 item 1's eight override rows are confirmed** — twelve `codex-index` mentions in
   `in/vendoring_policy.json`, being three repo entries, the leningrad comment and eight
   `dest_repo` override rows.

### The `parents[2]` question does NOT become live here, and the fact that decides it is a cost on the `.git` side

**This subsection said the opposite when it was first written, 2026-08-22, and both halves of what
it said were false.** It read "**this step is where it becomes live**: the repos that still hold a
copy are the two codex-index repos and diffable-pointed-hebrew", and went on to reason about
whether `parents[2]` is right at codex-index-aleppo's depth. **None of those four repos holds
`mb_cmn/provenance.py` at all.** The error came in through this phase's task prompt, which took it
from book-of-job's Phase 6 record, which appears to have derived it from the programme plan's
correct sentence about which repos have a `DIFFERS` **vendored copy** — a different subject
entirely. book-of-job's own Phase 1 record had the true facts the whole time. Caught 2026-08-22 by
the book-of-job Phase 7 session, which measured it across all 26 clones and MAM-private's subtrees
and sent the correction rather than editing under this plan; **verified here independently before
this rewrite**, with `git ls-files '*provenance.py'` in each of the six repos and `md5sum` on what
it found.

**There are three copies, not four and not five, and all three are byte-identical** at md5
`e53232a9782827e9af80669a31452f16`:

| Copy | `parents[2]` resolves to | Right? |
|---|---|---|
| `MAM-basics/py/mb_cmn/provenance.py` | MAM-basics' root | yes |
| `MAM-simple/py-examples/mb_cmn/provenance.py` | MAM-simple's root | yes |
| `MAM-private/al-hatorah/py/mb_cmn/provenance.py` | `MAM-private/al-hatorah/` | yes |

**codex-index-aleppo, codex-index-cam1753, codex-index-leningrad and diffable-pointed-hebrew hold
none.** diffable-pointed-hebrew's eight `mb_cmn/` files predate the feature outright: its
`file_io.py` never mentions provenance, where MAM-basics' imports it at line 8 and calls
`with_json_provenance` at line 31. **So there is nothing to re-vendor, this step is not where the
question becomes live, and book-of-job's Phase 4 deletion left the walk right in every copy that
survives it.**

**And the fact no phase had found: the proposed fix would regress the one live consumer.**
al-hatorah emits breadcrumbs today — `MAM-private/al-hatorah/out/a2d-override-diff-viewer/data.json`
and its two neighbours carry `"provenance": "This file was generated by
al-hatorah/py/main_3d_make_override_diff_viewer.py."` **al-hatorah is a subtree of MAM-private, not
a repo**: it has no `.git`, and `git -C MAM-private rev-parse --show-toplevel` is MAM-private's
root. So `parents[2]` lands on `al-hatorah` and names the tree correctly, while a `_repo_root()`
walking to `.git` would land on `MAM-private` and rewrite those tracked artifacts to name the wrong
tree.

**That is this step's own lesson arriving at the file the question is about.** The Item 3 subsection
above states it for the source lints — a `.git` walk finds a repo root and **cannot find a
subtree** — and it is exactly why `boj_paths.code_paths()` is a hand-maintained list rather than a
walk. The same wall stands in front of `provenance.py`, and it was invisible for as long as the
question was asked about repos that do not hold the file.

**So the question is narrowed rather than restated.** Five phases of the book-of-job plan and this
one put "leave it, or walk to `.git` and re-vendor?" to Ben as an open choice with no cost recorded
on either side. There is a cost, it is on the `.git` side, and it is measurable: three tracked
artifacts renamed to the wrong tree, in a repo neither this plan nor book-of-job's is allowed to
commit to. **Leaving it costs nothing that anyone has been able to find in six attempts.** Ben's to
settle, and this phase still did not pick — but a future phase should stop re-asking it as if the
two options were symmetric. book-of-job's Phase 7 session, correcting its own plan the same day,
went further and **recommends closing it as a no**, with the al-hatorah cost as the reason.

**A list of repos is a measurement, and this one was never taken.** That is the transferable part,
and it is not "the list was hard to check". book-of-job's Phase 1 record had the right three repos
and book-of-job's Phase 6 record had the wrong four, **in the same file, four screens apart, for
three days** — and three successive sessions, that plan's Phase 7, this phase's task prompt and
this phase's own first draft, copied the wrong one forward without either checking it against the
right one or running the two-second `git ls-files '*provenance.py'` that settles it. Every other
figure in these records carries a re-establishing command and an instruction to re-measure; a
sentence naming which repos hold a file reads like context rather than data, and so gets quoted
instead of checked. **Treat "the repos that have X" as a figure**: give it its command, and re-run
the command rather than the sentence. The same applies to "the files that differ", which is how
this phase's Family 2 table came to be wrong, and to "the packages a repo needs", which is how both
`requirements.txt` came to be wrong in two directions at once.

### Verification

- **Suite 945 passed, 5 skipped, 59 subtests**, before this phase's edits; the edits touch one
  docstring in a module no test imports.
- **`py\check_all.py` 7 of 7**, mark order over **298** files, escapes over **241** `.py`, before
  and after the docstring edit — unchanged in both counts and both verdicts.
- **codex-index-aleppo `py/check_mark_order.py` OK over 128 files** and
  **`py/check_escape_sequences.py` OK over 44 `.py`**, after the edit.
- **black clean** on the one Python file changed, in both repos, and the two are byte-identical
  after it.
- **codex-index-leningrad's three wiki artifacts byte-identical** against their HEAD blobs after a
  full regeneration, compared with `git show HEAD:<path>` rather than with `git status --porcelain`,
  per this programme's instrument rule. That repo is one of the three named as carrying the
  latent-CRLF condition and the comparison found no line-ending-only verdict in it.
- **`git status --porcelain` clean** in all four repos at the end; `git log` and `HEAD` re-read
  before staging in each, and both pushes fast-forward with no `--force`. **It was not clean in
  codex-index-cam1753 in between**: running `check_all.py` there rewrote `check_line_breaks.html`
  with CRLF, which the byte comparison called **line-ending-only** and `git checkout --` restored.
  The subsection above says why that happens and who fixes it.

---

**The original prescription follows.** The Baselines table above it and the two fork-family
sections below are left as written 2026-08-02.

## The fork families

**This is the prescription Phase 0's record above answers, left as written 2026-08-02. Both
families are settled; Family 2's table below is superseded by the blob table in that record.**

Two families span these three repos and book-of-job. **Programme Phase 0 owns the first and is
blocking; this plan owns the second.**

### Family 1 — the `check_*`/`fix_*` scripts (programme Phase 0)

Six scripts held by book-of-job, codex-index-aleppo and codex-index-cam1753, of which exactly one
pair is still identical. The table is in the programme file; do not re-derive it here.
`py_ac_word_image_helper/` (6 files, book-of-job and codex-index-aleppo, 2 differing) and
`py_cam1753_word_image/` (4 files, book-of-job and codex-index-cam1753, **all 4 differing**) are
part of the same phase.

### Family 2 — the wikisource page generators

`codex-index-aleppo/aleppo-wiki/` and `codex-index-leningrad/lenin-wiki/` are two builds of the
same thing — a Wikisource page for a manuscript index — and share eight module names. Measured
2026-08-02 with `cmp` and `diff`:

| Module | Result |
|---|---|
| `main_make_wikisource_page.py` | differs, 50 lines |
| `py/mam_book_names.py` | differs, 230 lines |
| `py/write_wikitext_file.py` | differs, 139 lines |
| `py/my_open.py` | **identical** |
| `py/hebrew_letters.py` | differs, 2 lines |
| `py/my_utils.py` | differs, 2 lines |
| `py/hebrew_punctuation.py` | **identical** |
| `py/hebrew_verse_numerals.py` | **identical** |

The last four are the diverged `mb_cmn` copies the vendoring inventory already flags — and the
shape of their divergence is informative: **they are nearly identical to each other and both
drifted from MAM-basics**, which reads as one ancestor copied twice while MAM-basics moved on.
That makes them the cheapest reconciliation in the whole programme: diff each against MAM-basics'
current `py/mb_cmn/`, decide whether the 2-line deltas are fixes worth keeping, and then they are
a plain deletion in both repos.

The first three are the real work. `mam_book_names.py` at 230 differing lines is not drift —
Aleppo and Leningrad have genuinely different book divisions and page conventions, and the honest
outcome may be **one parameterized module plus two data tables** rather than one merged file.
Classify before merging, and if the answer is that they are two tools, say so and land them under
two names.

**leningrad's `lenin-wiki/py/` has nine modules aleppo has no counterpart for** —
`vtrad_data.py`, `vtrad_helpers.py`, `masorah_finalis_lines.py`, `image_urls.py`,
`get_cvm_rec_from_bcvt.py`, `my_locales.py`, `read_json_file.py`, `s1_collapse_rows.py`,
`s2_group_by_book.py` — and aleppo has `group_by_book.py`, `book_names.py` and `read_csv_file.py`
against leningrad's `s2_group_by_book.py` and `read_json_file.py`. Those pairs are the same job
against different input formats. They are part of the same classification.

---

## The third UXLC fork — DECIDED 2026-08-03, in UXLC-utils' Phase 5

`codex-index-leningrad/UXLC-utils-sparse/py/` held **17 of UXLC-utils' own `.py`** —
`main_uxlc_estimate_atom_loc.py`, five `uxlc_lci/` modules and eleven `uxlc_misc/` modules —
refreshed from `../UXLC-utils` by codex-index-leningrad's root `main_update_vendored_files.py`.
The data half of that sparse copy (`in/UXLC-39/*.xml` 39, `data/lci_*.json` 2) is unaffected,
since `in/` and `data/` stayed in UXLC-utils.

**Ben's decision: the `py/` half was dropped, not repointed at `../MAM-basics`.** Landed as
`d5195e3` in codex-index-leningrad and `748ee2f` in UXLC-utils; the full account is
[PLAN-evacuate-python-from-UXLC-utils.md](PLAN-evacuate-python-from-UXLC-utils.md) Phase 5. **The
data half stays**, and `main_update_vendored_files.py` now runs to completion over those 41 files
rather than dying on the first `.py`. Do not vendor the seventeen back, and do not add a
`_SOURCE_REPO` pointing at MAM-basics.

**So one repo of this trio is already partly settled, and its remaining Python is `lenin-wiki/`
plus the root `main_update_vendored_files.py` / `vendoring_sync.py` pair.** Phase 7 item 2 below
still holds: that script now refreshes a data-only subtree, so the inventory's comment about it
wants rewording rather than deleting when the script itself goes.

**Three things from that phase bear directly on this plan:**

- **What decided it was that nothing in codex-index-leningrad imported the seventeen**, and that
  their one entry point could not run there anyway — the sparse copy never carried `mb_cmn`, so it
  raised `ModuleNotFoundError`. **Check the same before assuming this answer transfers.**
  book-of-job's `py_uxlc_loc/` is the third instance of the question and is **not** decided by
  this: it has its own importers to check, and the reasoning here turns entirely on there being
  none.
- **A downstream consumer's prose names the moved code in more places than the sync script.**
  Here it was `README.md`, two sections of `.github/copilot-instructions.md`, a
  `.vscode/launch.json` debugpy config, and a test module's scope docstring — five edits across
  four files. Grep a consumer for the **vendored directory's name**, not for the module names: the
  module names appeared in none of them.
- **codex-index-leningrad has a `.venv` with `black` but no `pytest`**, despite a
  `copilot-instructions.md` section headed "No Venv in This Repo" (now removed). Its one test
  module could not be run. **Check each of the three repos' venvs before quoting a verification
  command in this plan**, rather than inheriting MAM-basics' `.venv\Scripts\python.exe
  py\main_test.py` shape.

---

## Phase 1 — two roots, no cwd

Per repo, and each proved by regenerating that repo's own artifacts to a zero diff before anything
moves.

Known offenders:

- codex-index-aleppo `aleppo-wiki/py/mam_book_names.py:114` — `f"in/mam-ws/{basename}.json"`
- codex-index-aleppo `py/tests/test_h_dot_below_nfc.py:77` — `"gh-pages/"`

**Re-run `git grep -nI '"gh-pages/\|"out/\|"in/\|"MAM-XML/\|"line-breaks/\|"column-coordinates/'`
per repo** — these repos put their artifacts in top-level directories named after the artifact
rather than in an `out/`, so the usual grep misses most of them. That is the single most likely
way to leave a path bug behind in this plan.

**Ignore the `"../aleppo-pages/{page_id}.jpg"` hits** in `py/py_ac_loc/gen_line_break_editor.py:37`
and `py/py_ac_word_image_helper/codex_page.py:34`: those are `src` attributes in generated HTML,
not filesystem paths, and rewriting one breaks the published editor silently.

## Phase 3 — copy the Python in (dual residency)

Per repo, one at a time, each within a single session. Name collisions to settle first:

| Name | Held by | Resolution |
|---|---|---|
| `main_make_wikisource_page.py` | aleppo **and** leningrad | falls out of Family 2's classification |
| `main_update_vendored_files.py` | leningrad (and UXLC-utils, holman-ketiv-qere) | disappears |
| `vendoring_sync.py` | leningrad root — a **vendored `mb_cmn` module** sitting outside `mb_cmn/` | resolve with the rest of that repo's `mb_cmn` |
| `check_*`/`fix_*` × 6 | aleppo and cam1753 | one reconciled copy, from Phase 0 |
| `py_cam1753_word_image/`, `py_ac_word_image_helper/` | shared with book-of-job | one reconciled copy each, from Phase 0 |
| `py_mam_xml/` (cam1753) | — | check against MAM-basics' `mb_xml` before landing |

cam1753's Python is **14 files at the repo root**, so it lands at MAM-basics' `py/` top level and
carries the same two-module-objects hazard book-of-job's `py/` does. Land it as a package.

Retarget each repo's data root to `sibling_repo("codex-index-<x>")`; watch `force_utf8_io()` where
an entry point becomes a library module; finish with the oracle run from MAM-basics and
`git status --porcelain` empty in both repos.

**Stop and ask Ben before the first Phase 3 of the three.**

## Phase 4 — empty each repo

**None of the three has a `CLAUDE.md`** — codex-index-aleppo does, the other two do not.
Whichever the repo, write or update one in this phase saying that there is no Python left, that
the code is `../MAM-basics/py/`, and which entry point writes what. **Name the tracked artifacts
no program generates**, which for these repos includes the downloaded scans.

**Stop and ask Ben before each.**

## Phase 6 — breadcrumbs and issue citations

```powershell
git grep -lI "generated by codex-index" -- .
```

Per repo, in a dedicated commit near the end, and not mid-move.

## Phase 7 — cross-repo bookkeeping

1. `in/vendoring_policy.json` — delete all three entries **and the eight `overrides` rows** naming
   `codex-index-aleppo` and `codex-index-leningrad` paths. Then regenerate
   `doc/vendoring-inventory.md`. `py/main_vendoring.py --all` **raises** on a missing scan root
   rather than degrading, so a half-done edit breaks the audit rather than producing a stale one.
2. The inventory's own comment on `codex-index-leningrad` — that the copy script the provenance
   scan finds there refreshes `UXLC-utils-sparse` from UXLC-utils and never touches `lenin-wiki/py/`
   — becomes obsolete when that script goes. **Delete the comment with the script**, or it will be
   read later as describing something that still exists.
3. `all-repos.code-workspace` — leave all three listed; each keeps its tracked non-Python files.
4. Confirm `run_black.py` and `check_repo_standards.py` skip each once it tracks no `.py`.
5. **Delete each repo's `.venv` and any orphaned agent worktrees.**
6. Grep the other repos for `codex-index-*/py` paths. book-of-job is the known consumer of the two
   word-image helpers; run the grep anyway.
