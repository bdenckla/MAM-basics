# Evacuate all Python from codex-index-aleppo, -leningrad and -cam1753 into MAM-basics

Written 2026-08-02. Governed by [PLAN-evacuate-python-programme.md](PLAN-evacuate-python-programme.md).
**Last in the order.** One plan for three repos, because they share a shape, share two fork
families, and share a vendoring problem — doing them separately would answer the same question
three times and risk answering it three different ways.

## Status

| Phase | State |
|---|---|
| 0 — reconcile the fork families (programme Phase 0, plus the wiki family below) | **DONE 2026-08-22.** Programme Phase 0 confirmed rather than re-derived — fourteen of its sixteen files still one committed blob, `check_all.py` and `check_word_finding.py` per-repo permanently on Ben's decision of 2026-08-19. **Family 2 needed no design call**: on committed blobs **two** of the eight shared wiki module names differ, not four, and `mam_book_names.py` — the 230-line "real work" — is **one blob** and was one on 2026-08-02, the "230 lines" being 115 + 115 of whole-file diff caused by codex-index-aleppo's CRLF checkout. The two that do differ, `main_make_wikisource_page.py` and `write_wikitext_file.py`, are **two tools against two input formats**; Phase 3 names them. `hebrew_letters.py` and `my_utils.py` genuinely differed and `6ccd856` (leningrad, 2026-08-03) reconciled both with a black run. **The baselines are stale in eight places** and the inventory was right where this plan was wrong, for the second time in the programme. **Item 2's sweep finds two depth walks and the verdicts are opposite** — `flat_index.py` right in both repos but naming a file absent here, `page.py` right in codex-index-cam1753 and wrong here. **Item 3's wall is already up**: the four shared `check_*`/`fix_*` are two blobs, MAM-basics against the trio, and five top-level names are taken. **Item 4 landed** — `a171dd4` in codex-index-aleppo and `ef5525d` here, both copies byte-identical at md5 `f330012f28fdad782776c08ffbdb7b4b`; mgketer's third copy reported, MAM-private not written to. Two findings the phase turned up and did not fix: **`aleppo-wiki/main_make_wikisource_page.py` has been dead since 2026-03-28**, naming a directory `aleppo/` a rename removed, and **codex-index-aleppo's `check_word_finding.py` fails 160 of 160** comparing a `"1of2"` column identifier against the integer 1, since 2026-03-14. A third: **`codex-index-cam1753/check_line_breaks.py` writes CRLF** where codex-index-aleppo's copy writes LF, one missing `newline=""` — the programme Phase 0 defect in a seventh script, which dirties that repo's tree on any verification run. **Corrected 2026-08-22, after the first draft of this record**: the `parents[2]` question does **not** become live here. Only **three** copies of `mb_cmn/provenance.py` exist anywhere — MAM-basics, MAM-simple, MAM-private's `al-hatorah/` — all byte-identical and all with `parents[2]` resolving correctly; **none of the trio and not diffable-pointed-hebrew holds the file at all**, so there is nothing to re-vendor. And the fact that decides the question turned up with it: **walking to `.git` would regress al-hatorah**, a subtree of MAM-private rather than a repo, renaming three tracked breadcrumbs to the wrong tree — this step's own "a `.git` walk cannot find a subtree" lesson arriving at the file the question is about |
| 1 — two roots, no cwd (per repo) | **DONE 2026-08-22.** One commit per repo and one here: **`ee09e67`** in codex-index-aleppo, **`eb7c83c`** in codex-index-leningrad, **`7e5ca23`** in codex-index-cam1753, and **`72a4629`** here carrying this record and nothing else. **Nineteen root walks and thirteen cwd-relative literals become two paths modules** — `codex-index-aleppo/py/ac_paths.py` and `codex-index-cam1753/cam1753_paths.py` — **plus two named `_DATA_ROOT`s** in the two wiki entry points, which is four sites for Phase 3 to repoint rather than thirty-two. **The gating item landed and turned up a twin**: codex-index-aleppo's wiki generator runs again and its three artifacts are byte-identical, and so does `py/gen_index_flat_annotated.py`, **a SECOND generator dead since the same 2026-03-28 rename** and invisible to the prescribed grep because its dead path went through the vanished sibling repo `codex-index` rather than through a cwd-relative string. **The one-argument `newline=""` defect is in SEVEN sites in six scripts, all in codex-index-cam1753 and none in the other two**, three of them writing tracked files; the plan named one. **56 of the trio's 351 tracked artifacts have a generator and 295 do not**, so path-equality — import each module, assert every constant resolves where it did — is the second instrument, and all 36 repointed constants pass it; of the 56, **51 were regenerated and every one is byte-identical**, the other five being one crash Phase 0 already owns and four matplotlib renders. **A repo can have TWO `sys.path` roots**, which no earlier step met and which is why codex-index-aleppo needs both a paths module and a `_DATA_ROOT`. **`git status --porcelain` was wrong in the OTHER direction here**, four false positives where Phase 0 saw a false negative. **And the latent-CRLF claim is off by a repo**: measured whole-repo against HEAD blobs, codex-index-leningrad has **0** of 73 and codex-index-aleppo **152** of 222 |
| 3 — copy the Python in (per repo, dual residency) | **ALL THREE DONE 2026-08-22.** **codex-index-cam1753, 23 tracked `.py`, is twelve deletions and eleven arrivals**, and the twelfth deletion is the one the prescription got wrong: it lists `py_mam_xml/` as an arrival to "check against MAM-basics' `mb_xml`", a package that shares no function with it, where the real counterpart is `py_ac_loc/mam_xml_verses.py` — **one tool with 43 lines of drift**, which had moved here the day before. **A tag census over the three books both read finds exactly ONE tag treated differently**: `spi-invnun`, 7 occurrences, all in Ps.xml, the inverted nuns of Psalm 107 that `mb_sefaria/mam4ajf_handlers.py` has always counted at seven. codex-index-aleppo's copy **raises** on it and codex-index-cam1753's **silently skips** it, and since `check_cam1753_all` reaches the reader through `check_line_breaks` → `gen_flat_stream`, importing the unfixed shared copy would have taken that repo's 4 of 4 to a crash. **Ben's decision on a measurement rather than an argument: add the one missing skip clause and share one reader** (`b37bdb4`), proved by loading both readers side by side — **4512 verses, 30322 words, 0 mismatches**. Un-masking `check_ac_all`'s crash rewrote a **fossil** report covering 1 page of 35 (`a50f40e` there, 2 issues → 93, 4,771 → 18,377 bytes), of which **70 of the 93 are one known cause**, the N-of-M column migration that also fails `check_ac_word_finding` 160 of 160; the new signal is six pages, including a five-word MAM-XML alignment mismatch on 004r. **The eight runnable modules land as `py_cam1753_loc/` with the `cam1753` infix dropped**, which is what makes `main_cam1753_` plus the stem a rule rather than a list, and **four of the eight now share a module name with their `py_ac_loc` counterpart exactly** — the payoff codex-index-aleppo's phase predicted when it prefixed all fifteen of its own. **Three module-level scripts where Phase 1 named two**, the third being `download_cam1753_spreads.py`, which did `os.makedirs` and fourteen network reads at import — codex-index-aleppo's `download_aleppo_pages.py` exactly, one repo later. `page.py`'s `parent.parent` is repaired, closing Phase 0's pair of opposite verdicts and fixing book-of-job's `main_gen_cam1753_crop_editor.py` as `codex_page.py`'s repair fixed its aleppo twin. Lints widen to **510 files / 297 `.py`** and all still pass, 7 of 7. **The NFC test gains a SEVENTH scope, and it is the one EXPANSION among the seven** — that repo never had a copy of this test, so nothing obliged the entry; it is there because after Phase 4 nothing would otherwise read its hand-authored Hebrew, and because it passed on the first run. **Two contrasts with codex-index-aleppo, both absences**: not one of the 23 copied files was CRLF, and no module rebinds `sys.stdout`. Oracle **44 of 44 byte-identical** in both residencies (the 45th, `cam1753-gutter-profiles.png`, tracks the matplotlib version and is not one), path-equality **11 of 11**, import smoke **23 of 23**. **codex-index-aleppo, 50 tracked `.py`, is twenty-one deletions and twenty-nine arrivals** — the largest single thing that phase settled being that **the four source lints are deletions**, this repo already holding them, where Phase 0's Item 3 had invited a rename. Names are mechanical: `main_ac_` or `check_ac_` plus the module stem, applied to all fifteen top-level modules and not only the five that collided, because codex-index-cam1753 holds a counterpart of six of them. **All four artifacts byte-identical on the first run** from MAM-basics and from a foreign cwd, one of them proving a private-to-public symbol rewrite in `mam_bknas` that no static check could. **`py/repo_scopes.py` is new** and is what that phase actually owed: the four lints now union the per-repo `code_paths()` lists, taking mark order from 298 files to **419** and the escape check from 241 `.py` to **278**, with book-of-job's `check_all.py` still 7 of 7 — a restoration that imported no violations. `check_function_ordering` was deliberately left un-widened. **`codex_page.py` and `flat_index.py` are repaired at last**, and repairing the first fixes `main_gen_aleppo_crop_editor.py`, book-of-job's tool, broken in this repo since 2026-08-19. **Three module-level side effects**, one of them destructive: `main_ac_find_word_in_images.py` replaced `sys.stdout` at import and so swallowed output any importer had already printed. matplotlib was missing from this repo's venv, exactly as book-of-job's Phase 3 warned; kraken is missing too and deliberately stays so, codex-index-aleppo's own venv never having had it. The NFC test gains a **sixth** scope and a second extension from a dropped copy, `.xlsx`; ten copied files were CRLF and were normalized on arrival. Both pre-existing failures reproduce exactly — `check_word_finding` 0 of 160, `check_line_breaks` still raising on `<spi-invnun>` |
| 3 — the codex-index-leningrad half, kept for its own findings | The smallest of the three went first: **six own modules land as `py/lenin_wiki/`, eleven vendored copies dissolve**, and the two entry points become `py/main_lenin_wikisource_page.py` and `py/main_lenin_vendor_uxlc.py` beside a new `py/lenin_paths.py`. **The oracle passed on the first run from MAM-basics and from a foreign cwd** — all three tracked artifacts byte-identical, in both residencies. **Phase 0's table has the `vtrad_helpers.py` fork backwards**: codex-index-leningrad holds the `CvveType` Enum and MAM-basics the `CVVE_TYPE_*` integers, not the other way about, and this repo's shape was taken. **The collision table's "disappears" cost a live tool nearly being binned**: `main_update_vendored_files.py` still refreshes `UXLC-utils-sparse/`, whose `lci_augrecs.json` is the pipeline's only input, so it was renamed rather than dropped — and its `vendoring_sync.py` fork, two lines naming `provenance.md` against `_provenance.md`, dissolved into a `basename` parameter of `mb_cmn/vendoring_sync.py`. **That sparse copy is 19 days stale** and was deliberately left so, refreshing it being a regeneration of the three artifacts rather than a data update; the two runs that proved it stale were the check on the port and were reverted. **The four source lints still scope to book-of-job alone**, a gap stated rather than closed, because the union over per-repo lists wants building where the lint copies arrive. The NFC test gains a **fifth** scope, 30 files now and 9 after Phase 4 |
| 4 — empty each repo | **ALL THREE DONE 2026-08-22** — `824910e` in codex-index-leningrad, `078b74d` in codex-index-aleppo, `a9c3abd` in codex-index-cam1753, **so all three of the trio hold zero `.py`** and with book-of-job, holman-ketiv-qere and UXLC-utils before them, so do all six repos this programme set out to evacuate. **codex-index-cam1753 is 25 deletions and 5 rewrites**, 177 tracked files → 152, and **Ben settled both of the two beyond the Python**: `requirements.txt` (his codex-index-aleppo answer taken as settling it, that repo having no Pages workflow to distinguish it) and `codex-index-cam1753.code-workspace`, **asked as ONE question covering both repos' workspace files** since each declared a three-folder view of the same cluster from its own vantage point and book-of-job's had already gone — delete both, so nothing opens those three repos together now. **The prose sweep had to go by module BASENAME**, this repo's Python having sat at its root: 26 sites in five files, and the one worth carrying is a code citation inside a tracked **data** file, `cam1753-page-index.json`'s comment naming `download_cam1753_spreads.py` where no path-shaped grep would ever look — **sweep tracked data for module names, not only tracked prose**. `doc/cam1753-line-break-task.md` spells its four commands with **backslashes**, book-of-job's Phase 4 finding recurring in the sibling repo about the same manuscript. **The artifact classification reproduces Phase 1 to the file** — 10 paperwork, 142 artifacts, 45 generated, 97 not — but only 44 of the 45 regenerably, the forty-fifth tracking the matplotlib version. **The NFC scope came out at 14 against a prediction of 16**, the gap being Ben's own two deletions. Oracle **44 of 44 byte-identical after the deletion**, `check_cam1753_all.py` 4 of 4 with word finding 160 of 160, `py/check_all.py` 7 of 7 over 510 files and 297 `.py`. **A second session was live in MAM-basics throughout and did not collide**: `doc/PLAN-evacuate-python-programme.md` was left strictly alone, **including the trio's Status row there, which Phase 6 or 7 still owes**. **codex-index-aleppo is 50 deletions and 5 rewrites**, 228 tracked files → 178 and then → **175** as Ben settled its three orphan candidates one at a time, all three deleted (`b2b347e`, `2bdcfde`, `3003a06`); every one of the 50 is Python — no twenty-second file rode along as codex-index-leningrad's `.vscode/launch.json` did, that repo having none. **The third orphan is the one worth reading**: `.claude/settings.json` was NOT orphaned — six of its ten globs were still live — and Ben deleted it because it "dates from before 'auto' permissions", a reason the evacuation knows nothing about, which is the worked example of why these sub-decisions are put to him rather than inferred from what the move touched. **The doc repointing is 26 sites in four files where the plan named one**, and **three of the 26 were wrong before this programme began**: line 110's direct invocation, dead since that module gained an intra-repo import, plus a folder-layout block and an OCR doc that between them put `line-breaks/`, `codex-index/`, `MAM-simple/` and `column-coordinates/` under a `py/py_ac_loc/` **none of them has ever been in** — kept as ✗ rows rather than deleted, so a reader who remembers the old shape stops looking. **The artifact classification came out at exactly the predicted 154 of 162**, but only by counting the 16 pieces of repo furniture and subtracting: the plan's own list of trees adds to 136, and `ds-flat-stream/` is the entry that looks regenerable and is not, its generator's per-page verse ranges being recorded nowhere. **A second repo's figure was wrong and this phase's own measurement found it** — codex-index-leningrad's `CLAUDE.md` said "Nine files are in scope" where its Phase 4 had measured 8 and corrected MAM-basics' copy but not its own prose (`2abd7f6` there); **what found it was printing all six NFC scope counts rather than the one this phase needed**. **A sigil disagreement book-of-job's Phase 4 had already settled once**: `README.md` called the Cambridge manuscript μC where the code and site say μY, 57 to 0, and codex-index-cam1753's own README said the same until its Phase 4 corrected it the same day, so **all three repos that name this manuscript now agree with the code**. `pages.yml` was read rather than assumed and **runs no Python at all**, so the one thing distinguishing this repo from book-of-job does not bear on `requirements.txt`. **Ben lifted this phase's gate the same day**: run Phase 4 for a repo as soon as its Phase 3 is green, rather than asking first. 22 files deleted in codex-index-leningrad, all 21 tracked `.py` plus `.vscode/launch.json`, whose two debugpy configurations named one program the move took and one this repo never had. `README.md` and `CLAUDE.md` rewritten for a repo that is staying. The three `lenin-wiki/` artifacts are byte-identical after a pipeline run made AFTER the deletion, which is the order that proves the deletion took nothing the move needed. NFC scope **8**, not the 9 Phase 3 predicted — the ninth was the deleted `launch.json` |
| 6 — breadcrumbs and issue citations | **DONE 2026-08-22.** **One commit in one repo, `94b824a` in codex-index-aleppo**; the other two had nothing to repoint. The prescribed `git grep -lI "generated by codex-index"` returns **zero in all three**, as all three Phase 4 records predicted, and settles nothing — **the one site it found is invisible to every path-shaped grep**: `aleppo-pages-provenance.md:11` named the downloader as a bare `download_aleppo_pages.py`, now `../MAM-basics/py/main_ac_download_pages.py`. **That is the second phase running to find its one citation inside a file documenting DATA**, codex-index-cam1753's Phase 4 having found `cam1753-page-index.json`'s comment naming `download_cam1753_spreads.py` — two repos, two manuscripts, two download scripts, both cited where a sweep of "tracked prose" does not look. Three sweeps ran: the `py/…` grep (30 hits, 1, 3, all already correct), a **module-basename sweep over every tracked file** built from the **70 distinct basenames** of the 94 modules the three repos held before Phase 4, and a resolution of all **82** distinct `.py`-shaped tokens against the disk. **Issue citations: zero in all three** — every `#NN` is a hex colour, a Hebrew wikitext line prefix, or a UXLC change number in vendored data — so **three moves running, at 60, 241 and 94 modules, have owed a prefix nothing**. The `.venv` sweep: 16 lines mention one, 14 already naming MAM-basics' interpreter absolutely. An instrument note: **`sed -i` on a CRLF worktree file in codex-index-aleppo strips every CR in the file**, and `git diff` still reports the one real line because the index is LF |
| 7 — cross-repo bookkeeping | **DONE 2026-08-22 — and with it this plan, and the programme.** Items 1–5 discharged; **item 6 found five stale citations and every one is in a third repo, so all five stop and ask Ben** rather than being fixed. `in/vendoring_policy.json` goes **205 lines → 90**, losing three `repos` entries and eight `overrides` rows, and **the two halves are one edit**: `repo_policy.py:208` rejects an override naming a repo the manifest no longer knows, which is a second failure mode beside the missing-scan-root one the plan named. The prescription's account of the eight rows is wrong — they are **four `aleppo-wiki/py/` and four `lenin-wiki/py/`, and no override ever named `py/mb_cmn/` or codex-index-cam1753's `mb_cmn/`**, which were scan roots; that is why cam1753's inventory row vanished with its files while the other two survived as `MISSING-DEST`. Inventory **18 rows/112 files → 12/97**. **Running the audit BEFORE editing showed the tracked artifacts were already stale** — 14 rows/105 files at `ea1f035`, so the three Phase 4 commits left it unregenerated — and surfaced something that is not the trio's bookkeeping at all: **`10ae4d5`, this plan's own Phase 3, put MAM-private's two `mb_cmn/vendoring_sync.py` copies out of date**, dissolving a fork here having drifted a private repo's copies. Item 2 **wanted rewording and had no home left to reword**, item 1 having deleted the entry its comment sat on, so the fact went to the policy's top-level `comment` — and **a second home for it exists that the plan never named**, `UXLC-utils/shared-with-codex-index-leningrad.md`. The lint drops **23 → 18** cases, exactly 7 + 3 + 8, and the suite **945 → 940**. **The policy edit must precede item 5's deletions** and nothing in the prescription says so. Item 5: **328 MB**, all three real directories rather than junctions, plus fifteen `__pycache__` and nine emptied trees, leaving **no `py`-shaped directory in any of the three**. **Item 6's name sweep found four of the five**, a `codex-index-*/py` grep reaching only the two mgketer sites — book-of-job's Phase 7 lesson at nearly the same ratio. Verified after the venv deletions: oracles **4 of 4, 3 of 3, 44 of 44** byte-identical, `check_cam1753_all` 4 of 4, suite 940 passed/5 skipped/59 subtests, `py/check_all.py` 7 of 7 over **509** files and 297 `.py` — **509 and not the 510 the task carried, because `3003a06` deleted `codex-index-aleppo/.claude/settings.json`**, a `.json` inside `check_mark_order`'s corpus scope that nobody had noticed was in it, so **Ben's third orphan decision moved a lint's file count**. codex-index-aleppo's whole tree: **121 of 175 EOL-only and zero real drift** |

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

## This plan moves the Python and nothing else — **DECIDED 2026-08-22**

**Ben, 2026-08-22: the trio's data stays in place.** The manuscript scans and the derived JSON are
not evacuated, now or later, and no phase of this plan should propose moving them. When Phase 4
empties each repo, "empty" means **empty of Python** — every one of these three repos stays alive
as a data host afterwards, holding the trees its moved code now reads from
`C:\Users\BenDe\GitRepos\MAM-basics`.

**The decision is not a deferral, and the question should not be re-put.** It was settled against a
measurement taken the same day, which is that the trio has almost no served content and a great deal
of data:

| Repo | Tracked `gh-pages/` | Pages workflow | Tracked total | Where the bulk is |
|---|---|---|---|---|
| codex-index-aleppo | **4 files, 638 bytes** | `pages.yml` | 38.3 MB | `aleppo-pages/` 28.3 MB, `MAM-XML/` 7.2 MB |
| codex-index-leningrad | **none** | **none** | 12.8 MB | `UXLC-utils-sparse/` 42 files, `lenin-wiki/` 21 |
| codex-index-cam1753 | **none** | **none** | 80.6 MB | `cam1753-pages` 48 MB, `cam1753-spreads` 24 MB, `MAM-XML/` 7.2 MB |

Re-establish with `git -C <repo> ls-files gh-pages | wc -l`, `ls <repo>/.github/workflows`, and
`git -C <repo> ls-tree -r -l HEAD | awk '{s+=$4} END {print s/1048576}'`. codex-index-aleppo's four
are `index.html`, `missing_sections_nakh.html`, `missing_sections_torah.html` and a `README.md`.

**The wider programme this sits under does not follow the trio here.** Ben decided the same day that
**book-of-job, holman-ketiv-qere and UXLC-utils are to be totally evacuated** — served pages replaced
by forwarding stubs, README pointers rewritten to MAM-basics — under a new plan of their own, written
after this one finishes. The record is
[`PLAN-evacuate-python-programme.md`](PLAN-evacuate-python-programme.md)'s section "Decision — total
evacuation for three repos, Python-only for the codex-index trio". **Do not read that decision as
reaching these three repos**, and do not add a gh-pages phase to this plan on the strength of it.

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

**SETTLED LATER THE SAME DAY: Ben took that recommendation. `_repo_root()` stays `parents[2]`, and
the question is closed rather than narrowed.** The record is
[`PLAN-evacuate-python-programme.md`](PLAN-evacuate-python-programme.md)'s section "Decision —
`mb_cmn/provenance.py`'s `_repo_root()` stays `parents[2]`", which is the one home for it. **No
phase of this plan should re-put it**, and the sentence above calling it "Ben's to settle" is this
phase's own record of the state before he settled it.

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

## Phase 1 — two roots, no cwd — the execution record — **DONE 2026-08-22**

**One commit per repo, and in MAM-basics only this record.** `ee09e67` in codex-index-aleppo
(21 files: 15 modified, 6 added), `eb7c83c` in codex-index-leningrad (4 modified), `7e5ca23`
in codex-index-cam1753 (9 modified, 1 added), and **`72a4629`** here, which is the two plan
files and nothing else. The prescription this record answers is the section below it, left as
written 2026-08-02.

**The phase in one sentence: the trio's Python addressed its data through nineteen separate
root walks and thirteen cwd-relative literals, and it now addresses it through two new paths
modules and two named `_DATA_ROOT`s, with 51 of the 56 artifacts that have a generator
regenerated and every one of the 51 byte-identical.**  Counted off the four commits'
own diffs: twelve root walks removed in codex-index-aleppo and seven in codex-index-cam1753,
none in codex-index-leningrad, which had none to remove; four literals in each wiki entry
point and five in codex-index-cam1753's two module-level scripts. What it turned up beyond that is of three
kinds: a **second** dead generator in codex-index-aleppo from the same 2026-03-28 rename, **six** more
instances of the programme's missing-`newline=""` defect in codex-index-cam1753, and a standing
claim about which repo carries the latent-CRLF condition that is off by a repo and by two orders
of magnitude.

### Preconditions — every one matched, and MAM-basics is four prose commits further on

MAM-basics at **`60aabf5`**, not the `90487af` Phase 0's record names. The four commits between
are that phase's own provenance corrections — `1e36d56`, `4682adf`, `6621db4`, `c3a6287`,
`b594c72`, `f6e7ad2`, `60aabf5` — all prose in `doc/`, none touching anything this phase reads.
Suite **945 passed, 5 skipped, 59 subtests** in 122s; `py\check_all.py` **7 of 7**, mark order
over **298** files, escapes over **241** `.py`. codex-index-aleppo `a171dd4`,
codex-index-leningrad `0904b16`, codex-index-cam1753 `f56831c`, all clean and pushed.
codex-index-cam1753's `check_all.py` 4 of 4; codex-index-aleppo's exit 1 on the two pre-existing
failures Phase 0 characterized, `check_word_finding.py` 160 of 160 on `col: found=1of2
expected=1` and `check_line_breaks` on `ValueError: Unhandled tag <spi-invnun> in verse
Ps.107.23`.

**The `59 subtests` figure reproduced for the sixth measurement running.** book-of-job's Phase 1
recommended dropping it, on a run that reported `947 passed, 5 skipped` with no subtests line;
that recommendation should be dropped rather than the figure. It has reproduced at every
measurement since.

Baselines after the phase, for Phase 3 to check against:

| | codex-index-aleppo | codex-index-leningrad | codex-index-cam1753 |
|---|---|---|---|
| HEAD | **`ee09e67`** | **`eb7c83c`** | **`7e5ca23`** |
| tracked `.py` | **50** *(was 44)* | 21 *(unchanged)* | **23** *(was 22)* |
| lines of `.py` | **8,584** *(was 8,284)* | **2,572** *(was 2,524)* | **5,579** *(was 5,443)* |
| tracked total | **228** *(was 222)* | 73 *(unchanged)* | **177** *(was 176)* |

codex-index-aleppo's six new files are `py/ac_paths.py` and five `py/main_*.py`;
codex-index-cam1753's one is `cam1753_paths.py`.

### The gating item: codex-index-aleppo's wiki generator, and a SECOND dead generator beside it

The four `"aleppo/..."` literals in `aleppo-wiki/main_make_wikisource_page.py` are repointed and
**all three of its artifacts came back BYTE-IDENTICAL** against `git cat-file blob HEAD:`.
Five months dead, and no output drift at all: the code that could not run was still the code
that made the committed files.

**Then the same fossil turned up a second time, in a different shape, and the plan did not know
about it.** `py/gen_index_flat_annotated.py:43` read
`DEFAULT_INPUT = ROOT.parent / "codex-index" / "aleppo" / "index-flat-corrected.json"` — the same
2026-03-28 rename, `9025037`, reached through the **vanished sibling repo** `codex-index` rather
than through a cwd-relative string. So it was invisible to the prescribed grep twice over: no
leading quote, and the directory name it carries is `codex-index`, which is in nobody's list of
this repo's artifact directories. It is repointed to `aleppo-wiki/index-flat-corrected.json`, it
runs, and **`index-flat-annotated.json` came back BYTE-IDENTICAL too**.

**Two dead generators, one rename, and only one of them was findable by reading a plan.** The
transferable part is that a rename fossil survives in as many spellings as the code has ways to
name a directory: a cwd-relative literal, a `Path(__file__)` walk out of the repo and back in,
and a docstring. `gen_index_flat_annotated.py` had all three at once — and its **`DEFAULT_OUTPUT`
was already right**, so its Usage block was simultaneously wrong about a live path and right
about a dead one. **Grep for the OLD directory name, not only for the current ones.**

### The grep undercounted, and this time by one in each direction

Re-run per repo at the pre-phase heads, the prescribed grep widened with each repo's own artifact
directory names returns 18 hits in codex-index-aleppo, 5 in codex-index-leningrad and 20 in
codex-index-cam1753. Against the 30 sites actually changed:

- **It misses `gen_index_flat_annotated.py:43`** outright, for the two reasons above.
- **It misses nothing else**, once widened with the per-repo directory names as the task
  prescribed. The narrow form in the plan as written — six directory names, none of them
  `cam1753-*`, `aleppo*`, `ds-flat-stream/`, `index-*` or `plot_col_coords-out` — finds **two**
  hits in codex-index-cam1753 against the twenty the widened form finds.
- **Nine of its hits are false positives**, and they fall into four kinds rather than
  book-of-job's one:
  - `py/tests/test_h_dot_below_nfc.py`'s seven `_EXCLUDE_DIR_PREFIXES` in codex-index-aleppo and
    one in codex-index-leningrad, plus `_EXCLUDE_FILES`' `index-flat-annotated.json` — matched
    with `str.startswith` against a path `_iter_files` has already produced. book-of-job's Phase 1
    met exactly this and left it; so did this one, and a comment now says so in both copies.
  - `gen_col_quad_editor.py:234` (codex-index-aleppo) and `:140` (codex-index-cam1753) — a
    `source_note` **displayed in the editor's HTML**, telling the user which file the defaults came
    from. A near-miss for the `src`-attribute case the prescription already names, and a
    different one: not a URL, just prose that looks like a path.
  - `gutter_profile.py:40` and `split_cam1753_spreads.py:58` — `fname.replace("cam1753-page-",
    "")`, filename string surgery.
  - `download_cam1753_spreads.py:23` — `os.path.join(OUT_DIR, f"cam1753-page-{page:04d}.jpg")`,
    a leaf name joined to an already-absolute root.

**So book-of-job's "read what a hit does before counting it an offender" holds, and the reason to
read has broadened.** There, two of seven hits were exclusion prefixes. Here nine of 43 are false
positives and only four of the nine are that same kind.

### What each repo's Phase 1 actually was, and the three shapes are quite different

**codex-index-aleppo — conflation only, no cwd-relativity under `py/` at all.** Every one of that
tree's twelve data-addressing modules was already `Path(__file__)`-rooted; what they lacked was
any statement of which root they meant. `py/ac_paths.py` now holds twelve accessors, and thirteen
constants across nine modules read from it. The only cwd-relative literals this repo had were the
four in `aleppo-wiki/` and the uncalled `mam_book_path`.

**codex-index-leningrad — four literals and nothing else.** No paths module: there is one entry
point with four paths in it, and `main_update_vendored_files.py` was already `_REPO`-rooted with
its one `Path("in/UXLC")` a relative subpath inside `_SPARSE_ROOT` rather than a cwd-relative
path. The four are now spelled off `_REPO_ROOT` and `_WIKI_DIR`.

**codex-index-cam1753 — the conflation at its strongest, plus five bare literals.** The Python
sits AT the repo root beside the data, so `Path(__file__).resolve().parent` was code root and data
root in the same expression in nine modules — the shape `boj_paths.py`'s docstring calls "one
expression standing for two roots", here not in one function but repo-wide.
`gutter_profile.py` and `split_cam1753_spreads.py` went further and were cwd-relative outright,
five bare strings between them, both module-level scripts with no `main()` so the paths resolved
at import.

### The two paths modules, and why neither vendors `mb_cmn/paths.py`

book-of-job's Phase 1 asked which of three answers a repo takes — inherit `paths.py`, vendor it,
or do neither — and said to check the depth of the vendored `mb_cmn/` per repo. Measured here:
**neither codex-index-aleppo's `py/mb_cmn/` (4 files) nor codex-index-cam1753's `mb_cmn/` (3)
holds `paths.py`, and codex-index-leningrad has no `mb_cmn/` at all.** Vendoring it in would
also import the wrong root into codex-index-cam1753, whose `mb_cmn/` sits at the repo root where
`parents[2]` lands on `GitRepos` — book-of-job's situation exactly. So both new modules compute
their own root from `__file__`, as `boj_paths.py` did before its move, and **both become a
`paths.sibling_repo(...)` call at Phase 3**, which is the one line each that changes.

`ac_paths.CODE_DIR` and `cam1753_paths.CODE_DIR` are spelled off `__file__` rather than off the
data root, for the reason `boj_paths.code_dir()` gives: they must stay right when the code moves
out from under the data.

**No `code_paths()` list in either, and that is deliberate.** book-of-job needed one because its
four source lints had to be told what to lint once the code shared a root with all of MAM-basics.
Here the lints still walk to `.git` and still find only this code, so the list would be
premature; Phase 3 is where it becomes necessary, and Phase 0's record already says so.

### A repo can have TWO sys.path roots, which no earlier step in this programme met

codex-index-aleppo is entered two ways — `python py/main_*.py`, which puts `py/` on
`sys.path[0]`, and `python aleppo-wiki/main_make_wikisource_page.py`, which puts `aleppo-wiki/`
there. **A module in one is not importable from the other**, and closing that with a `sys.path`
line is banned. So `ac_paths` serves `py/` and the wiki entry point names its own `_DATA_ROOT`.
codex-index-leningrad has the same split for the same reason.

That is not a defect and it does not survive the move: at Phase 3 both trees land under
MAM-basics' `py/` and share one root, at which point the wiki pipelines can take an accessor
like everything else. It is recorded because the obvious tidy — one paths module per repo — is
**not available** in two of these three repos, and a session that assumes it is will reach for
`sys.path`.

### Five entry-point wrappers, because `ac_paths` is only importable from `py/`

Three of codex-index-aleppo's nine `py_ac_loc/` modules already had a `py/main_*.py` wrapper, and
the reason was not documented anywhere: those three import a sibling as `py_ac_loc.<name>`, so
`python py/py_ac_loc/gen_lb_flat_stream.py` had already been dead for however long — verified by
running all three, each `ModuleNotFoundError: No module named 'py_ac_loc'`. **`doc/aleppo-line-breaks.md:110`
documents one of those three as a direct invocation and has been wrong ever since.**

Giving the other five modules `ac_paths` would have taken away a command line each, so they get
the same wrapper the first three have: `main_gen_col_quad_editor.py`,
`main_gen_line_break_editor.py`, `main_kraken_seg_baselines.py`, `main_merge_line_markers.py`,
`main_plot_col_coords.py`. **This is applying a standing rule rather than inventing one** —
`~/.claude/CLAUDE.md`'s "a library module is not independently runnable ... a `py/main_<x>.py` at
the top of `py/` adds it as a subcommand" — and the naming is mechanical, `main_` plus the module
stem, matching the three that existed. Phase 3 may rename any of them freely; a wrapper is three
lines.

codex-index-cam1753 needed none of this: its Python is at the repo root, so `cam1753_paths` is
importable from every module without a wrapper.

### The missing `newline=""` is in SIX more sites, all in codex-index-cam1753, and three write tracked files

The plan handed this phase one instance, `check_line_breaks.py:654`. Grepping every text write in
all three repos for a missing `newline=` found **seven sites in six scripts, every one in
codex-index-cam1753 and not one in codex-index-aleppo or codex-index-leningrad**. All seven are
fixed.

| Site | Writes | Fired? |
|---|---|---|
| `check_line_breaks.py:653` | `check_line_breaks.html`, tracked | yes — Phase 0 caught it |
| `split_cam1753_spreads.py:131` | `cam1753-spread-splits-doc/*.json`, 14 tracked | **yes — caught here by running it** |
| `split_cam1753_spreads.py:142` | `cam1753-spread-splits-doc/_all-splits.json`, tracked | **yes** |
| `gen_cam1753_flat_stream.py:352` | `cam1753-line-breaks/*.json`, 27 tracked | **latent** |
| `gen_cam1753_line_break_editor.py:176` | `.novc/`, gitignored | harmless |
| `gen_col_quad_editor.py:674` | `.novc/`, gitignored | harmless |
| `main_find_word_in_cam1753_images.py:212` | `.novc/`, gitignored | harmless |

**codex-index-aleppo's counterpart of every one of those seven already had the argument** —
including the two that write only into `.novc/`. So this is a per-repo split rather than a
scattering, and closing it whole is what stops the next reader finding three of seven still open.

**The `gen_cam1753_flat_stream.py` one is latent for a reason worth stating, because it is how a
defect hides in plain sight.** Its 27 output files are LF on disk today, so nothing looks wrong;
they are LF because the line-break workflow is human-in-the-loop and each file arrives as a
**browser download** that the editor produces and a human moves into place, not from this writer.
The writer runs only when a page is generated fresh. So the check that would have caught it —
"is the tracked output CRLF?" — answers no, and answers no about a file this code did not write.

**And the two that fired were found by running the code from a foreign working directory,
which is the whole method.** Verifying `split_cam1753_spreads.py`'s repoint meant running it, and
running it is what produced 15 line-ending-only verdicts that no amount of reading would have
produced.

### The oracles, per repo, and what has none

**codex-index-aleppo — 4 artifacts, all BYTE-IDENTICAL**: `aleppo-wiki/index-flat.json`,
`index-grouped-by-book.json`, `index.wiki` from the revived wiki generator, and
`index-flat-annotated.json` from the revived annotator.

**codex-index-leningrad — 3 artifacts, all BYTE-IDENTICAL**: `lenin-wiki/index-s0-annotated.json`,
`index-s2-grouped-by-book.json`, `index.wiki`, mtimes bumped and checked.

**codex-index-cam1753 — 45 artifacts, 44 BYTE-IDENTICAL and one excluded with cause.** A full run
of `split_cam1753_spreads.py` rewrote all 28 `cam1753-pages/*.jpg` and all 15
`cam1753-spread-splits-doc/*.json`; the 15 were **line-ending-only before the `newline=""` fix and
byte-identical after it**, so one run proved the repoint and the fix together. A run of
`check_all.py` — 4 of 4 — now leaves `check_line_breaks.html` byte-identical where before it left
the tree dirty, which closes Phase 0's finding by demonstration.

**`cam1753-gutter-profiles.png` is not an oracle and was restored rather than committed.**
`gutter_profile.py` re-renders it **run-to-run byte-identical** under matplotlib 3.11.1 and
**1,541 bytes larger** than the tracked copy (650,806 against 649,265). So its bytes track the
matplotlib version, not the code, and the path-equality proof below covers what the phase actually
changed. Committing a 650 KB re-render inside a paths commit would be the ride-along the black
section of `~/.claude/CLAUDE.md` forbids for the same reason. **Ben's call whether to re-render
it deliberately, in its own commit.**

**What has no oracle at all, in any of the three, and why.** `ds-flat-stream/` (8),
`line-breaks/` (35 aleppo, 27 cam1753) and `column-coordinates/` / `cam1753-col-quads/` (35, 28):
the flat-stream generators take **explicit per-page verse ranges** as arguments and those
arguments are recorded nowhere, and the line-break and quad files are the human-in-the-loop
editors' output. `aleppo-pages/` (37) and `cam1753-spreads/` (14) are downloaded scans.
`MAM-XML/` (24 in each of two repos) is a vendored snapshot. `gh-pages/` (4) is hand-authored.
**Counted rather than estimated**, by listing each artifact tree and loose data file per repo
and asking of each whether a program in that repo writes it: **351 tracked artifacts across the
three, of which 56 have a generator and 295 have none** — 162 artifacts in codex-index-aleppo
with 8 generated, 47 in codex-index-leningrad with 3, and 142 in codex-index-cam1753 with 45.
That is the same split book-of-job's Phase 0 found, 518 against 183, and it is the reason an
empty `git status` proves nothing here.

**Of the 56, this phase regenerated 51 and proved every one byte-identical.** The five it did
not are named rather than glossed: codex-index-aleppo's `check_line_breaks.html`, whose
generator crashes on `<spi-invnun>` before it writes, which is Phase 0's pre-existing failure
and not this phase's; and four matplotlib renders — codex-index-aleppo's three
`plot_col_coords-out/` PNGs, not run, and codex-index-cam1753's `cam1753-gutter-profiles.png`,
run and restored for the reason the `cam1753-gutter-profiles.png` paragraph above gives.

### Path-equality is the proof that covers what regeneration cannot

For the artifacts with no generator there is a second instrument, and it is stronger than a diff
because it does not depend on anything being rewritten: **import each module and assert that every
repointed constant is the same absolute path it was before.** Thirty-six constants were checked
this way, 19 in codex-index-aleppo and 17 in codex-index-cam1753, against the pre-change
expressions read off the HEAD blobs. **All 36 resolve identically**, and the one path that moved
moved on purpose: `gen_index_flat_annotated.DEFAULT_INPUT`, from a directory that does not exist
to one that does.

The cam1753 half of that check was run **from `C:\Users\BenDe\AppData\Local\Temp`**, which is what
makes it a test of the cwd-relative sites rather than a restatement of them: before this phase
`gutter_profile.IMG_DIR` was the string `"cam1753-spreads"` and `split_cam1753_spreads.OUT_DIR`
the string `"cam1753-pages"`, and from that directory the first would have raised and the second
would have written 28 JPEGs into the system temp directory.

**Recommend this to Phase 3.** A move changes exactly these expressions, and a phase whose only
evidence is regenerated output can say nothing about the 190 artifacts nothing regenerates.

### `git status --porcelain` is wrong here in the OTHER direction, which is a fourth demonstration

Phase 0 recorded it reporting a **false negative** — a tree that looked clean while
`check_line_breaks.html` sat CRLF. Here it produced **false positives**: after the wiki generator
ran, `git status --porcelain` listed `index-flat.json`, `index-grouped-by-book.json`, `index.wiki`
and `index-flat-annotated.json` as modified while `git diff` was empty and
`git hash-object` on each equalled `git rev-parse HEAD:<path>` exactly. The cause is the
stat cache: the working copies had been **CRLF on disk against an LF blob**, the regeneration
wrote LF, the size changed, and git flagged the size change before re-hashing settled it. A
`git add` of the four paths — which staged nothing, `git diff --cached --stat` empty — cleared it.

**So the instrument rule needs stating as a positive, not only as a prohibition.** The three
verdicts come from comparing bytes against `git cat-file blob HEAD:<path>`; `git status` is a
report about the index's opinion of the filesystem and can be wrong about content in both
directions.

### The latent-CRLF condition is codex-index-aleppo's, and codex-index-leningrad has none

Every tracked file in all three repos was compared against its HEAD blob, which is a
measurement no phase of this programme had taken for a whole repo before:

| Repo | tracked | byte-identical | line-ending-only | genuinely different |
|---|---|---|---|---|
| codex-index-aleppo | 222 | 55 | **152** | 15 (all files this phase edited) |
| codex-index-leningrad | 73 | 69 | **0** | 4 (all files this phase edited) |
| codex-index-cam1753 | 176 | 166 | **1** | 9 (all files this phase edited) |

**Not one tracked artifact is genuinely different in any of the three**, which is the phase's
verification in one line.

And the standing claim is wrong in the direction that matters. This phase's own task prompt says
"codex-index-leningrad is one of the three repos known to carry the latent-CRLF condition", and
Phase 0's verification section repeats it. **codex-index-leningrad carries it in zero files of
73.** codex-index-aleppo carries it in **152 of 222** — two thirds of the repo, including all 24
`MAM-XML/`, all 35 `line-breaks/`, all 35 `column-coordinates/`, `CLAUDE.md`, `README.md` and
every `.py` of `aleppo-wiki/`. `doc/review-findings-2026-08-03.md`'s item 14 had codex-index-aleppo
right and the trio plan's Phase 0 had leningrad's `lenin-wiki/*.py` measured as LF; what nobody
did was put the two together. **This is the "a list of repos is a measurement" lesson from Phase 0's
own record, recurring at the very next phase and about the very same trio** — a sentence naming
which repos have a property gets quoted rather than re-run.

The condition is harmless while `* text=auto eol=lf` holds, which it does in all three; it matters
only as the thing that makes `cmp` and `git status` lie, and the byte-against-blob comparison is
immune to it.

### Two dead functions left in place, and the reason is that there is nowhere to point them

The plan's first named offender, `aleppo-wiki/py/mam_book_names.py:114`'s
`f"in/mam-ws/{basename}.json"`, is **uncalled** — `git grep mam_book_path` in both repos finds the
definition and the docstring and no call site — and **`in/mam-ws/` is in neither codex-index repo**;
it is MAM-basics'. codex-index-leningrad has a second of the same shape,
`mam_book_names_and_std_book_names.wikisource_book_path_fr_bk39id:30`.

Repointing either would mean inventing a data root for a directory that is not there. Both are
left with a docstring note saying they are dead and why, on book-of-job's Phase 1 precedent, and
Phase 3 deletes both modules outright when the code imports MAM-basics' `mb_cmn/mam_bknas.py`
directly. **`mam_book_names.py` is ONE COMMITTED BLOB across the two repos and the identical note
went into both**, so it is still one blob — checked by md5 after the edit.

The MAM-basics counterpart is the interesting half: `mb_cmn/mam_bknas_and_std_bknas.py:30` takes
the directory as a **parameter** and composes `f"{path}/{osdf}.json"`. So the fork is that the
wiki copies hardcoded what MAM-basics parameterized, and the hardcoded version then went unused.

### Three shared blobs untouched, exactly as Phase 0 ruled

`py_ac_word_image_helper/codex_page.py` and `flat_index.py` in codex-index-aleppo and
`py_cam1753_word_image/page.py` in codex-index-cam1753 compose data paths off roots of their own
and were left alone. **All ten files of the two packages re-verified as one committed blob with
MAM-basics' copies** before the phase started. Both new paths modules' docstrings name these three
and say why they are excluded, so the exclusion is discoverable from the code rather than only
from this plan.

### Findings reported and not fixed

- **`py/gen_permission_glob.py:8` in codex-index-aleppo cites `../masorah-books/.claude/test_globs.py`.**
  That tree moved into MAM-private on 2026-08-10 and the path wants `../MAM-private/masorah-books/`.
  Ben's decision of 2026-08-10, recorded in MAM-basics' `CLAUDE.md`, was to leave the eight such
  spellings in `py/accgram/` and cover them with a sentence rather than edit them; this is a ninth
  of the same kind, in a different repo, and is left on the same terms. **Phase 6's**, if anyone's.
- **`doc/aleppo-line-breaks.md` in codex-index-aleppo is stale in two ways.** Line 110 gives
  `python py/py_ac_loc/gen_lb_flat_stream.py 270v`, which has not worked since that module gained
  an intra-repo import; lines 30 and 113 say the line-break data lives in
  `py/py_ac_loc/line-breaks/`, where it has never lived — it is at the repo root.
  `doc/ocr-with-kraken.md:137,140` give a direct invocation of `kraken_seg_baselines.py` under a
  WSL kraken interpreter, which the new wrapper supersedes. Left because a doc edit riding along
  on a paths commit is the ride-along this programme keeps warning about, and because the WSL
  command cannot be tested here — **kraken is still absent from that repo's venv**, so
  `main_kraken_seg_baselines` is the one entry point of the eleven that does not import.
- **`py/main_find_word_in_aleppo_images.py:34` rebinds `sys.stdout` at module scope**, with
  `io.TextIOWrapper(sys.stdout.buffer, ...)`, where `~/.claude/CLAUDE.md` calls for
  `sys.stdout.reconfigure(encoding="utf-8")` as the first lines of `main()`. It discards whatever
  was buffered on the original stream, which is how it silently ate a line of an import check run
  here. Not a path defect; not this phase's.
- **`py/download_aleppo_pages.py` and codex-index-cam1753's `gutter_profile.py` and
  `split_cam1753_spreads.py` do their whole job at IMPORT**, having no `main()` and no
  `if __name__` guard. `download_aleppo_pages` also calls `os.makedirs` at module scope. Importing
  any of the three runs it. Worth knowing before Phase 3 imports anything to inspect it.
- **`cam1753-page-index.json` (tracked, at codex-index-cam1753's root) is read by no program** —
  only cited in `page-snips/README.md` and `things-noticed-in-cam1753.md`. Named in
  `cam1753_paths.py`'s docstring so Phase 4's inventory of artifacts with no generator does not
  have to re-derive it.
- **`main_update_vendored_files.py` in codex-index-leningrad was not run.** It refreshes
  `UXLC-utils-sparse/` from the sibling UXLC-utils and is unaffected by anything here; running it
  would have written tracked files for reasons that are not this phase's.

### Verification

- **MAM-basics is untouched by the code half of this phase and was measured anyway**, before and
  after: suite **945 passed, 5 skipped, 59 subtests** (122s, then 94s), `py\check_all.py` **7 of
  7**, mark order over **298** files, escapes over **241** `.py`. Identical both times, this
  phase's only edits here being the two plan files.
- **codex-index-aleppo `check_all.py` exits 1 on the two pre-existing failures and on nothing
  else** — `check_word_finding.py` 160 of 160 on `col: found=1of2 expected=1`, and
  `check_line_breaks` on `ValueError: Unhandled tag <spi-invnun> in verse Ps.107.23`, both
  characterized by Phase 0. Its other two checks report **escapes over 50 `.py`** and **mark order
  over 134 files**, against Phase 0's 44 and 128 — **exactly six more each, and the six are
  `ac_paths.py` plus the five wrappers**. Reading the counts rather than the verdicts is what makes
  that an accounting rather than a coincidence.
- **codex-index-cam1753 `check_all.py` passes 4 of 4**, with **escapes over 23 `.py`** and **mark
  order over 95 files** against 22 and 94 — one more each, that one being `cam1753_paths.py`. And
  the run now leaves `check_line_breaks.html` byte-identical rather than dirtying the tree.
- **codex-index-leningrad has no `check_all.py` and no pytest in its venv**, so its check is that
  every module compiles and that the wiki generator runs silent at exit 0 — both done.
- **Eleven of codex-index-aleppo's twelve `py/` entry points import cleanly**;
  `main_kraken_seg_baselines` does not, because **kraken is still absent from that repo's venv**,
  which is the state Phase 0 left and not something this phase changed.
- **black clean on all 35 Python files changed or added**, run from MAM-basics' venv so that one
  black version reaches all three repos.
- **`git status --porcelain` clean in all four repos at the end**, `HEAD` and `git log` re-read
  before staging in each, every file staged by explicit path, and all four pushes fast-forward with
  no `--force`. It was **not** clean in between, in codex-index-aleppo, and the byte comparison is
  what showed those four entries to be a stat-cache artifact rather than a change.

### What Phase 3 now owes, beyond what Phase 0 already told it

1. **Two paths modules, two `_DATA_ROOT`s, one line each.** `ac_paths.ac_data_root()`,
   `cam1753_paths.cam1753_data_root()`, `aleppo-wiki/main_make_wikisource_page.py`'s `_DATA_ROOT`
   and `lenin-wiki/main_make_wikisource_page.py`'s `_REPO_ROOT`/`_WIKI_DIR` are the whole surface
   the move has to repoint. Everything else composes off one of the four.
2. **The two-sys.path-root split dissolves at the move, and the two wiki pipelines should take an
   accessor then.** Do not carry `_DATA_ROOT` into MAM-basics as a fourth spelling of the same
   idea.
3. **Five new `py/main_*.py` in codex-index-aleppo, eight in total for `py_ac_loc/`.** They are
   free to rename and they collide with nothing: cam1753's counterparts carry no `main_` prefix.
4. **`ac_paths.py` and `cam1753_paths.py` collide with nothing at MAM-basics' `py/` top level**
   — checked against its 74 top-level modules. The five collisions Phase 0 named are unchanged.
5. **`code_paths()` becomes necessary at the move and does not exist yet**, in either module, for
   the reason Phase 0 gives: the four source lints walk to `.git` today and that stops being the
   right scope the moment the code shares a root with MAM-basics.
6. **Import-and-compare-absolute-paths is the verification for the 190 artifacts nothing
   regenerates.** The throwaway shape used here is: import each module, read each constant, assert
   it equals the pre-move expression.

---

## Phase 1 — two roots, no cwd — the prescription, left as written 2026-08-02

**The execution record above answers this.** Its two named offenders both turned out to be things
to leave rather than fix, and the grep it prescribes misses the one genuinely dead path in the
trio.

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

## Phase 3, codex-index-leningrad — the execution record — **DONE 2026-08-22**

**The first of the three, and the smallest.** Landed in MAM-basics as one commit: four files
added (`py/lenin_paths.py`, `py/lenin_wiki/` with six modules,
`py/main_lenin_wikisource_page.py`, `py/main_lenin_vendor_uxlc.py`) and two modified
(`py/mb_cmn/vendoring_sync.py`, `py/tests/test_h_dot_below_nfc.py`). **Nothing was owed in
codex-index-leningrad**, whose HEAD is `eb7c83c` before and after and whose tree is clean at
both ends — dual residency, so the twenty-one `.py` there are Phase 4's to delete.

**Every baseline was re-measured first and every one matched**: codex-index-leningrad clean at
`eb7c83c` with 21 tracked `.py`; MAM-basics clean at `e2903be` with **945 passed, 5 skipped, 59
subtests**; the wikisource pipeline run from codex-index-leningrad's own root and its three
tracked artifacts byte-identical to their HEAD blobs.

### The oracle passed on the first run from MAM-basics, and from a foreign cwd

All three tracked artifacts byte-identical to their HEAD blobs, measured with
`git cat-file blob HEAD:<path>` and `cmp`, and `git status --porcelain` empty in
codex-index-leningrad after each run:

| Run | `index-s0-annotated.json` | `index-s2-grouped-by-book.json` | `index.wiki` |
|---|---|---|---|
| baseline, codex-index-leningrad's copy from its own root | identical | identical | identical |
| MAM-basics' copy, cwd = MAM-basics | identical | identical | identical |
| MAM-basics' copy, cwd = `C:\Users\BenDe\GitRepos` | identical | identical | identical |

**Both residencies produce the same bytes**, which is what "dual residency" has to mean and was
cheap to check. Re-establish with:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_lenin_wikisource_page.py
```

`git status --porcelain` **is** the right instrument in codex-index-leningrad, unlike book-of-job
and unlike this trio's Phase 1, where it was wrong in both directions. That repo's checkout is
all LF — Phase 1 measured 0 latent CRLF of 73 files — and the pipeline rewrites exactly the three
files it generates, so an empty porcelain there means what it says. The byte comparison was run
anyway, and agreed.

### Eleven of eighteen wiki modules were copies of this repo's own, and all eleven dissolved

Phase 0's finding that `lenin-wiki/` is a far bigger vendoring fork than
`doc/vendoring-inventory.md` can see is what this phase spent its effort on, and the count held:
of the eighteen `.py` under `lenin-wiki/`, **six are codex-index-leningrad's own**, eleven are
copies of MAM-basics modules under three kinds of disguise, and the eighteenth is the entry
point. The six landed as `py/lenin_wiki/`; the eleven are Phase 4 deletions and are imported
from this repo directly instead:

| `lenin-wiki/py/` | imported from | disguise |
|---|---|---|
| `hebrew_letters.py` | `mb_cmn/hebrew_letters.py` | none — and byte-identical already |
| `hebrew_punctuation.py` | `mb_cmn/hebrew_punctuation.py` | none |
| `hebrew_verse_numerals.py` | `mb_cmn/hebrew_verse_numerals.py` | none |
| `my_utils.py` | `mb_cmn/my_utils.py` | none |
| `my_locales.py` | `mb_cmn/bib_locales.py` | renamed |
| `my_open.py` | `mb_cmn/file_io.py` | renamed |
| `mam_book_names.py` | `mb_cmn/mam_bknas.py` | renamed |
| `mam_book_names_and_std_book_names.py` | `mb_cmn/mam_bknas_and_std_bknas.py` | renamed |
| `vtrad_data.py` | `py_misc/vtrad_data.py` | out of package |
| `vtrad_helpers.py` | `py_misc/vtrad_helpers.py` | out of package |
| `get_cvm_rec_from_bcvt.py` | `py_misc/get_cvm_rec_from_bcvt.py` | out of package |

**Every symbol the six use was checked against this repo's module before the swap, and the
oracle then checked the swap**: `file_io.with_tmp_openw` and `file_io.json_dump_to_file_path`,
`my_utils.sum_of_map` / `sl_map` / `my_groupby`, `hebrew_verse_numerals.INT_TO_STR_DIC`,
`bib_locales.mk_bcvtbhs`, `mam_bknas_and_std_bknas.he_bk39_name`,
`get_cvm_rec_from_bcvt.get_cvm_rec_from_bcvt` and `cvm_rec_get_parts`, and `vtrad_helpers`'
three verse-correspondence constants. `mam_bknas.py`, `hebrew_letters.py`,
`hebrew_punctuation.py` and `vtrad_data.py` are reached only through the others and needed no
call-site check of their own.

**One adaptation was needed and exactly one**, and the diffs are otherwise import lines and
comment wording: `file_io.json_dump_to_file_path` has three optional parameters
codex-index-leningrad's `my_open` did not, all with the defaults that copy's fixed behaviour
supplied (`newline=""`, `indent=2`, no provenance breadcrumb), so the two positional calls carry
across as written.

### The fork's direction in `vtrad_helpers.py` is the OPPOSITE of what this plan said

Phase 0's table of the eighteen says `get_cvm_rec_from_bcvt.py` "differs in an enum MAM-basics
has since made (`CVVE_TYPE_SAME_CONTENTS` → `CvveType.SAME_CONTENTS`)". **It is the other way
round.** codex-index-leningrad's `vtrad_helpers.py` holds a `CvveType(Enum)` with three members;
MAM-basics' `py_misc/vtrad_helpers.py` holds three module-level integer constants named
`CVVE_TYPE_SAME_CONTENTS`, `CVVE_TYPE_NO_CONTENTS` and `CVVE_TYPE_PARTIAL_CONTENTS`. So the
wiki copy is the newer shape and this repo's is the older one.

**Taken as this repo's, not as the wiki copy's**, so the one site that named the enum —
`write_wikitext_file.py`'s `_PARTIAL_AND_SAME` — now names the two integer constants. The
alternative was to upgrade `py_misc/vtrad_helpers.py` to the enum, which would have meant
editing its six other call sites in `mb_json/json_root_from_bksams.py` and
`mb_xml/xml_root_from_bksams.py`, and an evacuation's job is to move code rather than to
modernize the modules it lands beside. **Recorded rather than done, because the upgrade is
genuinely the better shape and someone should get to choose it deliberately.**

**The transferable part is Phase 0's own lesson, met again.** That phase wrote "treat 'the repos
that have X' as a figure: give it its command, and re-run the command rather than the sentence."
A sentence naming which of two copies is newer is the same kind of figure, and this one was
quoted forward without the two-second `diff` that settles it. Re-establish with:

```powershell
diff C:\Users\BenDe\GitRepos\codex-index-leningrad\lenin-wiki\py\vtrad_helpers.py C:\Users\BenDe\GitRepos\MAM-basics\py\py_misc\vtrad_helpers.py
```

### The other half of that repo's Python is a live tool, and it kept its job under a new name

`main_update_vendored_files.py` and the root `vendoring_sync.py` refresh
`UXLC-utils-sparse/` from the sibling UXLC-utils. Phase 3's collision table above says the first
"disappears" and the second "resolve with the rest of that repo's `mb_cmn`", and read as a
disposition rather than as a name collision that would have been wrong: **the refresh is still
wanted**, since Ben's decision of 2026-08-03 dropped the `py/` half of that sparse copy and kept
the data half, and one of the two files it keeps is the wikisource pipeline's only input.

- The script landed as **`py/main_lenin_vendor_uxlc.py`**, named for `py/main_wlc_vendor_uxlc.py`
  beside it, which does the same job for this repo's own vendored UXLC subset. The old name was
  held by three repos at once and says nothing about which vendored files are meant.
- **`vendoring_sync.py`'s two-line fork is gone, dissolved into a parameter.** The two lines were
  a docstring and `dest_dir / "provenance.md"`, against this repo's `dest_dir / "_provenance.md"`;
  `mb_cmn/vendoring_sync.write_provenance` now takes `basename="_provenance.md"` and the one
  caller that wants the other spelling passes it. codex-index-leningrad's breadcrumb has no
  leading underscore because it is a tracked file of that repo's, named that way since before
  `mb_cmn/vendoring_sync.py` existed.
- **The two bodies were not merged**, and that is deliberate: `main_wlc_vendor_uxlc` copies two
  flat directories filtered to one suffix each, and this one copies a whole subtree recursively
  and suffix-blind. Either walk applied to the other's destination sees no files at all and so
  reports "unchanged" forever, which is the failure `_content_digest`'s own comment already
  warns about.

### `UXLC-utils-sparse` is stale, and finding that out is not the same as fixing it

Running the refresh — codex-index-leningrad's copy first, then this repo's — **wrote three
tracked files** of that repo's: `UXLC-utils-sparse/data/lci_augrecs.json` (+77 lines),
`data/lci_recs.json` (+61) and `provenance.md`, which stamps UXLC-utils' HEAD moving from
`748ee2f` to `c8db329`, and the date from 2026-08-03 to 2026-08-22.

**Reverted both times with `git checkout -- UXLC-utils-sparse/`, discarding nothing**: every byte
of that tree is re-derivable from UXLC-utils by re-running the refresh, which is the whole point
of a vendored copy, and UXLC-utils' Phase 5 record already names this exact command doing this
exact thing.

**It is left stale on purpose, and the reason is that refreshing it is not a data update but a
regeneration.** `lci_augrecs.json` is the wikisource pipeline's only input, so a refresh moves
the three artifacts under `lenin-wiki/` as well — and the oracle this phase depends on is
precisely that those three come back byte-identical. Doing both at once would have made a stale
input and a moved pipeline indistinguishable in the same diff. Phase 1 declined to run the
script for the same kind of reason and said so. **What this phase adds is that the script's two
runs were the check on the port**: this repo's copy produced the identical three-file diff that
codex-index-leningrad's copy did, including `provenance.md` written without the leading
underscore, which is what proves the `basename` parameter carries the fork.

**Someone should decide about the refresh**, and it is not a phase of this plan: it would land
five changed files across one repo, three of them artifacts, for reasons that have nothing to do
with moving Python.

### The four source lints still scope to book-of-job alone — a stated gap, not an oversight

`check_function_ordering`, `check_mark_order`, `check_escape_sequences` and the two `fix_*` take
their scope from `boj_paths.code_paths()`, so **the eight modules that landed here are not
linted**. Evidence that this is so rather than silently otherwise: `py/check_all.py` reports 7 of
7 after the move, over **298 files and 241 `.py`** — the same two figures Phase 0 recorded before
it.

**Not closed here, because codex-index-leningrad is the wrong repo to close it in.** The union
over per-repo lists is what the four lints need, and it wants building where the lint copies
actually arrive — codex-index-aleppo and codex-index-cam1753 each hold four, one committed blob
between them, which Phase 0's Item 3 table records. Closing it now would mean designing the
union against one repo and redoing it against three. **`lenin_paths.code_paths()` exists and
returns the four paths**, so that step is one entry rather than a new list.

**The gap costs nothing today and was measured rather than assumed**: nothing in the eight
modules carries a combining mark or a `\uXXXX` escape, checked 2026-08-22. It would start costing
something the moment one did, which is why it is written down here and in `lenin_paths.py`'s
module docstring rather than left to be noticed.

### The NFC test gains a fifth scope, and it is the smallest by an order of magnitude

`py/tests/test_h_dot_below_nfc.py` had four `_Scope`s and has five. codex-index-leningrad's own
304-line copy is Phase 4's to delete; copied across unchanged it would have found its root by
`git rev-parse` from its own directory and so scanned MAM-basics, which is the third time this
programme has met that exact trap. Its `_BINARY_EXTENSIONS` were compared against this file's
first, as holman-ketiv-qere's and book-of-job's were, and were a strict subset — this file has
seven more, `.man`, `.wts`, `.md5sum`, `.docx` and three others — so nothing was owed.

**30 files in scope now, 9 after Phase 4**, measured 2026-08-22 rather than predicted: 21 of the
30 are the `.py` this phase has copied here. What survives is `.gitattributes`, `.gitignore`,
`.vscode/launch.json`, `CLAUDE.md`, `README.md`, `page-snips/README.md` and the three artifacts
under `lenin-wiki/`. **So the floor is 5, not the 20 that repo's own copy asserted**, which would
not have survived its own Phase 4. `UXLC-utils-sparse/` is excluded, carried over verbatim from
that copy; `lenin-wiki/` deliberately is not, generated though its three artifacts are, because
excluding it would leave the scope with no Hebrew in it at all.

Re-establish the count with the scratch shape this phase used: import the module, call
`_tracked_files_in_scope` on each `_Scope`, print the lengths. It gave 1289, 11, 45, 33, 30.

### The four names

| codex-index-leningrad | MAM-basics | Files |
|---|---|---|
| `lenin-wiki/py/` (the six own modules) | `py/lenin_wiki/` | 6 |
| `lenin-wiki/main_make_wikisource_page.py` | `py/main_lenin_wikisource_page.py` | 1 |
| `main_update_vendored_files.py` | `py/main_lenin_vendor_uxlc.py` | 1 |
| — (new at this phase) | `py/lenin_paths.py` | 1 |

**The entry point had to be renamed and the package did not.** codex-index-aleppo holds a
`main_make_wikisource_page.py` too, and Phase 0 classified the two as different tools against
different input formats rather than one tool with drift, so both cannot keep the name; `lenin_`
is the prefix because `lenin-wiki/` is what that repo already calls the tree. `lenin_wiki` as a
package name collides with nothing, and its six module basenames are reached as
`lenin_wiki.<name>`, so none of them is a second module object for a name this repo already has.

**`lenin_paths.py` does not vendor `mb_cmn/paths.py`, and now delegates to it.** Phase 1's
reasoning for the pre-move module — compute the root from `__file__`, vendor nothing — was
correct while the code sat in a repo whose `mb_cmn/` was absent entirely. Here the depth is the
one `paths.py` is written for, and `boj_paths.py`, `hkq_paths.py` and `uxlc_paths.py` are three
worked precedents: `lenin_data_root()` is
`paths.require_sibling("codex-index-leningrad", paths.sibling_repo("codex-index-leningrad"))`,
checked rather than merely composed, for the reason `require_sibling` gives.

**Phase 1's `_REPO_ROOT` and `_WIKI_DIR` did not survive**, as Phase 3 item 2 said they should
not: the wiki pipeline takes accessors like everything else, and there is no fourth spelling of
the data root in this repo.

### Verification

- Wikisource pipeline, three runs, three artifacts each: **all byte-identical**, table above.
- Vendoring refresh, this repo's copy against codex-index-leningrad's: **identical three-file
  diff**, reverted both times, tree clean.
- MAM-basics suite: **945 passed, 5 skipped, 59 subtests** — the baseline exactly.
- `py/check_all.py`: **7 of 7**, 298 files and 241 `.py`, both unchanged.
- black clean on all six files this phase added or edited.
- `git status --porcelain` empty in codex-index-leningrad at HEAD `eb7c83c`, unchanged
  throughout.

### What Phase 4 now owes for this repo, beyond what it already knew

1. **Twenty-one `.py` to delete, in three places**: `lenin-wiki/main_make_wikisource_page.py`
   and its `py/` (18), the root `main_update_vendored_files.py` and `vendoring_sync.py`, and
   `py/tests/test_h_dot_below_nfc.py`. That empties `lenin-wiki/py/` and `py/tests/` outright.
2. **`.vscode/launch.json` names the moved scripts** and is one of the nine files that survive
   in the NFC scope. Grep the repo for the two entry-point filenames, not only for `py/`.
3. **`README.md` and `CLAUDE.md` are written for a repo that is staying**, per the decision
   recorded under "This plan moves the Python and nothing else": the code moved to
   `../MAM-basics/py/` and the data did not.
4. **Name the artifacts no program generates**, which here is `page-snips/` (2 files) and the
   whole of `UXLC-utils-sparse/`, that last being vendored rather than generated and refreshed
   by `../MAM-basics/py/main_lenin_vendor_uxlc.py`.
5. **The NFC scope's floor of 5 is checked against 9**, so Phase 4 should re-run the scope count
   after its deletion and confirm 9 rather than assume it.

### What the other two repos' Phase 3 now owes, beyond what Phase 0 already told them

1. **The lint union is theirs to build**, per the stated gap above, and
   `lenin_paths.code_paths()` is already written to be one entry in it.
2. **Check the direction of every fork before taking a side**, not only its existence. This
   phase found one recorded backwards, and Phase 0 found the same class of error in its Family 2
   table and in both `requirements.txt`.
3. **A collision table entry saying a name "disappears" is about the NAME.** Read it as a
   disposition and a live tool goes in the bin: `main_update_vendored_files.py` still had a job,
   and so may `main_make_wikisource_page.py` in codex-index-aleppo, whose Phase 1 revived it.
4. **`git status --porcelain` is usable in codex-index-leningrad** and is not in the other two:
   codex-index-aleppo has 152 latent CRLF of 222 files by Phase 1's measurement, and
   codex-index-cam1753 is where the seven missing `newline=""` sites were. Compare bytes against
   HEAD blobs there.

---

## Phase 3, codex-index-aleppo — the execution record — **DONE 2026-08-22**

**The second of the three, and the largest.** Landed in MAM-basics as one commit. **Nothing was
owed in codex-index-aleppo**, whose HEAD is `ee09e67` before and after and whose tree is clean at
both ends — dual residency, so the fifty `.py` there are Phase 4's to delete.

**Every baseline was re-measured first and every one matched**: codex-index-aleppo clean at
`ee09e67` with 50 tracked `.py`; MAM-basics clean at `10ae4d5` with **945 passed, 5 skipped, 59
subtests**; both generators run from codex-index-aleppo's own root with all four tracked
artifacts byte-identical; `check_word_finding` 0 of 160; `check_mark_order` OK over 134 files and
`check_escape_sequences` OK over 50 `.py`, both in that repo.

### What moved, what was deleted, and the two counts are close to equal

Fifty tracked `.py`, of which **twenty-one are Phase 4 deletions rather than arrivals** and
twenty-nine moved:

| Deletion | Count | Why it is not an arrival |
|---|---|---|
| `py/py_ac_word_image_helper/` | 6 | one committed blob with this repo's copy, which arrived with book-of-job 2026-08-19 |
| `py/mb_cmn/` | 4 | vendored from this repo, byte-identical |
| `aleppo-wiki/py/` vendored six | 6 | `hebrew_letters`, `hebrew_punctuation`, `hebrew_verse_numerals`, `my_utils` under their own names; `mam_book_names` (this repo's `mam_bknas`) and `my_open` (`file_io`) renamed |
| `py/check_mark_order.py`, `check_escape_sequences.py`, `fix_mark_order.py`, `fix_escape_sequences.py` | 4 | this repo already holds all four, forked at book-of-job's Phase 3 to take a scope list; what they needed was codex-index-aleppo's code IN that scope, not a second copy |
| `py/tests/test_h_dot_below_nfc.py` | 1 | folds into this repo's file as a sixth `_Scope` |

**The four lints being deletions is the single largest thing this phase settled**, and the
prescription does not say it: Phase 0's Item 3 established that the trio's four and MAM-basics'
four are two committed blobs and concluded "Phase 3 cannot land the trio's four under their own
names", which invites a rename. The right answer is that they should not land at all.

### The names, and the rule is mechanical

| codex-index-aleppo | MAM-basics | Files |
|---|---|---|
| `py/py_ac_loc/` | `py/py_ac_loc/` | 9 |
| `aleppo-wiki/py/` (the four own modules) | `py/ac_wiki/` | 4 |
| `py/ac_paths.py` | `py/ac_paths.py` | 1 |
| `py/check_all.py` | `py/check_ac_all.py` | 1 |
| `py/check_word_finding.py` | `py/check_ac_word_finding.py` | 1 |
| `py/main_<stem>.py` × 8 | `py/main_ac_<stem>.py` × 8 | 8 |
| `py/main_find_word_in_aleppo_images.py` | `py/main_ac_find_word_in_images.py` | 1 |
| `aleppo-wiki/main_make_wikisource_page.py` | `py/main_ac_wikisource_page.py` | 1 |
| `py/gen_index_flat_annotated.py` | `py/main_ac_gen_index_flat_annotated.py` | 1 |
| `py/download_aleppo_pages.py` | `py/main_ac_download_pages.py` | 1 |
| `py/gen_permission_glob.py` | `py/main_gen_permission_glob.py` | 1 |

**`main_ac_` plus the module stem, and `check_ac_` plus the stem, with no exceptions among the
fifteen top-level modules.** Only five of the fifteen names were actually taken — the four lints
and `check_all.py` — and the other ten were prefixed anyway, which is the decision worth
recording. The reason is codex-index-cam1753: it holds a counterpart of six of these, against the
same problem on a different manuscript, and its Phase 3 lands them as `main_cam1753_` plus the
same stems. Prefixing only the collisions would have produced a `py/` where
`main_gen_flat_stream.py` is one manuscript's and `main_cam1753_gen_flat_stream.py` is the
other's, with nothing saying which. The rule as applied can be stated in one line, which the
alternative could not.

**`main_gen_permission_glob.py` is the one file that moved with this code without belonging to
it.** It turns a shell command into a Claude Code permission glob and mentions no manuscript, no
codex and no Hebrew; it is a utility of this repo's that happened to be sitting in
codex-index-aleppo's `py/`. So it landed unprefixed, and `ac_paths.AC_TOP_LEVEL_MODULES`
deliberately does not list it — listing it would put a general tool inside a per-repo lint scope.

**`py_ac_loc` kept its name and `aleppo-wiki/py/` could not keep one it never had**: a directory
called `py` inside a data directory, importable as `py.<module>` only because that repo was
entered two ways. `ac_wiki` is what it became, matching `lenin_wiki` from the phase before it.

### The oracle passed on the first run from MAM-basics, and from a foreign cwd

All four tracked artifacts byte-identical to their HEAD blobs, measured with
`git cat-file blob HEAD:<path>` and `cmp`:

| Run | `index-flat.json` | `index-grouped-by-book.json` | `index.wiki` | `index-flat-annotated.json` |
|---|---|---|---|---|
| baseline, codex-index-aleppo's copy from its own root | identical | identical | identical | identical |
| MAM-basics' copy, cwd = MAM-basics | identical | identical | identical | identical |
| MAM-basics' copy, cwd = `C:\Users\BenDe\GitRepos` | identical | identical | identical | identical |

**That is a stronger result than it looks, because one of the four proves a symbol rewrite the
static check could not.** `ac_wiki/book_names.py` read
`mbn.BOOK24_AND_SUB_TO_BOOK39[mbn.BS_FST_SAM]` and six more like it, and that dictionary is
`_BOOK24_AND_SUB_TO_BOOK39` — **private** — in this repo's `mb_cmn/mam_bknas.py`. The six were
rewritten to the public `mbn.he_bk39_name(*mbn.BS_FST_SAM)`, which is the same lookup except for
a special case on `ספר תרי עשר` and `ספר עזרא` that none of the six can reach. `index.wiki`
carries every one of those Hebrew book names, so a byte-identical `index.wiki` is the proof that
the rewrite is behaviour-preserving.

Re-establish with:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_ac_wikisource_page.py
```

### Path-equality: thirteen accessors, thirteen equal

The 190-artifact problem Phase 3 item 6 names is answered the way that item prescribes — import
each module, read each constant, assert it equals the pre-move expression — and here it can be
done as a **differential** rather than as a list of assertions, because codex-index-aleppo's
`ac_paths.py` is still live during dual residency. Loading both copies under different module
names and calling every zero-argument accessor on each gives **13 of 13 equal**, every one
resolving under `C:\Users\BenDe\GitRepos\codex-index-aleppo`, with `CODE_DIR` correctly moving
from that repo's `py/` to this repo's. Five accessors are additions: `code_paths` and the four
`wiki_index_*` that replace the entry point's `_DATA_ROOT` literals.

**Do that comparison rather than re-deriving the expected values**, and do it before Phase 4
deletes the other copy. It is the cheapest instrument this programme has found for a move of this
shape, and it needs no oracle.

### The lint union, which is what codex-index-aleppo's Phase 3 actually owed

`py/repo_scopes.py` is new, and it is what Phase 0's Item 3 predicted would be needed: the four
source lints take their scope from a union of the per-repo `code_paths()` lists rather than from
`boj_paths.code_paths()` alone. Only two files change to use it, `check_mark_order.py` and
`check_escape_sequences.py`, because `fix_mark_order.py` and `fix_escape_sequences.py` each
derive their scope from their own checker.

**Per-repo lists unioned in one place, rather than one list that knows which repo each path
belongs to.** Phase 0 said per-repo is the default unless Phase 3 finds a reason against it, and
none turned up: each list belongs beside that repo's data-root accessor, where the reader who
adds a module is already looking.

| Check | Before | After |
|---|---|---|
| `check_mark_order` | 298 files | **419** |
| `check_escape_sequences` | 241 `.py` | **278** |

**Both still pass, and so does book-of-job's `check_all.py`, 7 of 7.** So the widening restored
codex-index-aleppo's coverage without importing a single violation — which was not a foregone
conclusion and is the reason the widening could be done in this phase rather than deferred.

**Three of the six evacuated repos are in the union, and the other three are deliberately out.**
book-of-job, codex-index-aleppo and codex-index-cam1753 ran these lints over their own trees, so
keeping their code linted is a restoration; codex-index-leningrad never ran them and IS included,
because it is eight small modules that pass both as they stand, which closes the gap that phase's
record had to state. UXLC-utils and holman-ketiv-qere never ran them either and are **out**:
adding their code would surface violations that are nobody's current business, and that is an
expansion rather than a restoration.

**`check_function_ordering` was deliberately NOT widened**, and the reason is the same one in
reverse. Only book-of-job ever ran it — it is one of the seven checks in `check_all.py`, and
codex-index-aleppo's register lists four that do not include it. Widening it would turn a passing
check into a failing one over code that has never been held to it, which is a decision for Ben
rather than a restoration for this phase. It still reads `boj_paths.code_paths()` directly, and
`repo_scopes`' module docstring says so.

**The corpus half is shorter than the code half, and that is not an oversight.**
`check_mark_order` reads `.json` as well as `.py`, and the hand-made JSON stayed behind in each
data repo — 24 line-break files in book-of-job and 78 line-break, column-coordinate and
flat-stream files in codex-index-aleppo. `corpus_roots()` is those two and not
codex-index-leningrad's, whose JSON is two artifacts of its own pipeline and two files vendored
from UXLC-utils, whose contents are that repo's business.

### Two root walks repaired at last, and one of them was breaking a book-of-job tool

Phase 0's Item 2 found exactly two depth-counting walks in the reconciled word-image packages and
recorded their verdicts as opposite. Both are settled here, and the plan is right that Phase 3 is
where "at once" becomes possible:

- **`py_ac_word_image_helper/codex_page.py`** walked to the nearest ancestor holding `.git` and
  composed `line-breaks`, `column-coordinates` and `aleppo-pages` off it. Right in
  codex-index-aleppo; in MAM-basics it found a correct root with all three directories missing.
  Now `ac_paths.line_breaks_dir()`, `col_coords_dir()` and `pages_dir()`.
- **`py_ac_word_image_helper/flat_index.py`** was `parent.parent.parent`, which the move to
  MAM-basics did repair as book-of-job's Phase 3 said — but "the right root and a reachable file
  are two claims, and the move bought only the first": `index-flat-annotated.json` is
  codex-index-aleppo's and is absent here. Now `ac_paths.flat_index_annotated_path()`.

**`py/main_gen_aleppo_crop_editor.py` has been broken in this repo since 2026-08-19 and is not
any more.** It is book-of-job's tool and it imports `LB_DIR` and `CC_DIR` from `codex_page`, so
it inherited that module's missing directories the day book-of-job's Phase 3 landed the package
here. Naming the data root is what repairs it. **A move can leave a consumer broken in a way no
test sees**, and what found this one was reading the two modules' roots rather than running
anything.

**The one-blob relationship with codex-index-aleppo's copies ends with these two edits, and that
is deliberate rather than an oversight.** Those copies are Phase 4 deletions, so what looks like a
fork is the last few days of dual residency. Both files say so in a comment, and both name
`py_cam1753_word_image/page.py` as the counterpart codex-index-cam1753's Phase 3 has to settle
the same way.

### Three module-level side effects, and one of them was destroying output

codex-index-aleppo's Python was entered only by being run, so module scope and `main()` were
interchangeable there. In MAM-basics, importing a top-level module to inspect it is ordinary, and
three files could not survive that:

1. **`main_ac_find_word_in_images.py` replaced `sys.stdout` at import** —
   `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")`,
   with a comment explaining the Windows cp1252 problem it solves. Rewrapping the buffer
   **abandons whatever the old wrapper had buffered**, so importing this module silently swallowed
   output another program had already printed. **Found by watching an import smoke test lose its
   first eighteen lines**, and confirmed by the lines coming back once the line was replaced with
   `force_utf8_io()` under the `if __name__` guard — this repo's convention, which reconfigures
   the existing streams instead of replacing them.
2. **`main_ac_download_pages.py` downloaded at import.** The whole of it ran at module scope: the
   `os.makedirs`, the loop over twenty-four page IDs, the network reads. Phase 1 noted the hazard
   and left it, that phase being about paths. It has an `almost_main()` and a guard now.
3. **`py/gen_index_flat_annotated.py`** was already well-formed and needed nothing.

**The transferable part: an entry point that only ever ran is not the same as a module, and the
move is what makes the difference matter.** codex-index-cam1753's `gutter_profile.py` and
`split_cam1753_spreads.py` are named by Phase 1 as module-level scripts with no `main()`, so its
Phase 3 has two more of these and already knows where they are.

### matplotlib was missing, and book-of-job's Phase 3 said to look

That phase's handover ends "**at the codex-index trio, read what the code imports, not only what
`requirements.txt` declares**", and this is the payoff: `py_ac_loc/plot_col_coords.py` imports
matplotlib, MAM-basics' venv did not have it, and an import smoke test over all 38 moved and
edited modules was 36 of 38 until it was installed. It is now in the venv and in this repo's
`requirements.txt`.

**`kraken` is a second missing package and is deliberately NOT installed.**
`py_ac_loc/kraken_seg_baselines.py` imports `from kraken import blla`, and **codex-index-aleppo's
own venv does not have it either** — its `requirements.txt` names black, matplotlib and
pyspellchecker, and Phase 0 already found that file wrong in both directions. So that module was
un-runnable before the move and is un-runnable after it, which is a pre-existing state rather than
something the move broke. Installing an OCR stack to preserve the property would be a decision
about this repo's venv, not a step of an evacuation.

Re-establish the import check by importing every module named in `ac_paths.AC_PACKAGES` and
`AC_TOP_LEVEL_MODULES`, plus the two `py_ac_word_image_helper` modules this phase edited and the
two book-of-job entry points that consume them. **38 of 38** as of 2026-08-22.

### Ten of the copied files were CRLF, and `cp` does not notice

codex-index-aleppo's checkout is where Phase 1 measured **152 latent CRLF of 222 files**, and ten
of the files this phase copied came across with CRLF line endings: the four of `ac_wiki/`,
`check_ac_all.py`, `main_ac_check_line_breaks.py`, `main_ac_gen_flat_stream.py`,
`main_ac_gen_lb_flat_stream.py`, `main_gen_permission_glob.py` and
`py_ac_loc/mam_xml_verses.py`. All ten were normalized to LF on arrival. This repo's
`.gitattributes` declares `* text=auto eol=lf`, so git would have normalized them at check-in and
the working tree would then have disagreed with the index from the first commit — a small mess,
and invisible unless someone looks. **Check the line endings of what a `cp` brought over**, which
codex-index-cam1753's Phase 3 will need too.

### Two pre-existing failures reproduce exactly, which is the point of reproducing them

- **`check_ac_word_finding` fails 160 of 160** from MAM-basics, as `check_word_finding` fails 160
  of 160 in codex-index-aleppo. Phase 0 owns this: a `col: found=1of2 expected=1` comparison of a
  string against an integer, since `eb4bcaf` (2026-03-14) migrated that repo's column identifiers
  to N-of-M form. Every failure is a column clause and none is a line or word clause, so the
  located positions are right in all 160.
- **`py_ac_loc/check_line_breaks` raises `ValueError: Unhandled tag <spi-invnun> in verse
  Ps.107.23`** before it writes, from MAM-basics as from codex-index-aleppo. Also Phase 0's, and
  it is why `check_line_breaks.html` is one of the five artifacts Phase 1 could not regenerate.

**Neither was fixed here and neither should be read as this phase's.** An unchanged failure is
evidence: a move that changed behaviour would have changed one of these two, and the identical
tallies are what say it did not.

### The NFC test gains a sixth scope, and a second extension from a dropped copy

codex-index-aleppo's own 319-line `py/tests/test_h_dot_below_nfc.py` located its root by
`git rev-parse` from its own directory, so copying it across unchanged would have aimed it at
MAM-basics — the **fifth** repo in a row whose copy would have done that.

**Diffing its `_BINARY_EXTENSIONS` against this file's found `.xlsx`**, which that copy had and
this file did not: `aleppo-wiki/precursors/E-J David Stark Aleppo Codex Index.xlsx`, the
spreadsheet form of the index, beside the `.docx` form that holman-ketiv-qere's copy contributed
the extension for. Without it the merged scope reads a zip container as text and raises
`UnicodeDecodeError`. **That is two extensions in three repos found by the same two-minute diff**,
which is why the step is worth writing down rather than assuming a subset.

**79 files in scope now, 29 after Phase 4**, measured rather than predicted: 50 of the 79 are the
`.py` this phase has copied here. The floor is **20**, where that repo's own copy asserted 40 over
a scope its comment called "~72".

### Verification

- Wikisource pipeline and flat-index annotator, three runs each, four artifacts: **all
  byte-identical**, table above.
- Path-equality, both `ac_paths` copies loaded side by side: **13 of 13 accessors equal**.
- Import smoke over all 38 moved and edited modules: **38 of 38**.
- MAM-basics suite: **945 passed, 5 skipped, 59 subtests** — the baseline exactly.
- `py/check_all.py` (book-of-job's register): **7 of 7**, over the widened 419 files and 278 `.py`.
- `py/check_ac_word_finding.py`: **0 of 160**, the baseline exactly.
- black clean on all 37 files this phase added or edited.
- `git status --porcelain` empty in codex-index-aleppo at HEAD `ee09e67`, unchanged throughout.

### What Phase 4 now owes for this repo, beyond what it already knew

1. **Fifty `.py` to delete**, emptying `py/`, `py/tests/`, `py/py_ac_loc/`,
   `py/py_ac_word_image_helper/`, `py/mb_cmn/` and `aleppo-wiki/py/` outright.
2. **`doc/aleppo-line-breaks.md:110` documents a direct invocation that has been wrong since
   before this programme** — Phase 1 found it, naming `py/py_ac_loc/gen_lb_flat_stream.py`, which
   has raised `ModuleNotFoundError` for however long. It wants
   `py/main_ac_gen_lb_flat_stream.py` in MAM-basics now, so the correction and the repoint are
   one edit.
3. **`.claude/settings.json`, `codex-index-aleppo.code-workspace` and `requirements.txt`** are
   all in the NFC scope and all name the moved code or the venv it needed. The workspace file and
   `requirements.txt` are the two files book-of-job's Phase 4 decided to delete as orphaned;
   **that decision was Ben's there and is Ben's here**, and this repo differs in keeping a Pages
   workflow.
4. **`README.md` and `CLAUDE.md` are written for a repo that is staying**, and this one keeps
   three published pages and its `pages.yml` as well as its data.
5. **Name the artifacts no program generates**, which here is 154 of the 162: the 37 downloaded
   scans, the 24 vendored MAM-XML, the 35 hand-made line-break and 35 column-coordinate JSON, the
   4 gh-pages files and the loose `test-data-from-book-of-job.json`.
6. **The NFC scope's floor of 20 is checked against 29**, so re-run the scope count after the
   deletion and confirm 29 rather than assume it.

### What codex-index-cam1753's Phase 3 now owes, beyond what Phase 0 already told it

1. **Its four lints are deletions too**, and its `check_all.py` and `check_word_finding.py` land
   as `check_cam1753_all.py` and `check_cam1753_word_finding.py`.
2. **Add one line to `repo_scopes.py`** — `cam1753_paths.code_paths()` — and one to
   `corpus_roots()`, that repo's 27 line-break and 28 column-quad JSON being exactly the kind of
   hand-made file the mark-order check exists for.
3. **`py_cam1753_word_image/page.py` is the third root walk** and this phase's two are the worked
   example: it wants `cam1753_paths`, and its blob relationship with codex-index-cam1753's copy
   ends the same way and for the same reason.
4. **Its fourteen root-level modules land as a package**, which the prescription already says;
   the entry points take `main_cam1753_` plus the module stem, matching this phase's rule.
5. **Two module-level scripts with no `main()`** — `gutter_profile.py` and
   `split_cam1753_spreads.py`, named by Phase 1 — need the treatment
   `main_ac_download_pages.py` got here.
6. **Check the line endings of everything copied**, and check its own `.venv` against what its
   code imports rather than against its `requirements.txt`.

---

## Phase 3, codex-index-cam1753 — the execution record — **DONE 2026-08-22**

**The last of the three, and the one that had to reconcile a fork nobody had classified.**
Landed in MAM-basics as one commit: nineteen files added and three modified. **Nothing was owed
in codex-index-cam1753**, whose HEAD is `7e5ca23` before and after and whose tree is clean at
both ends — dual residency, so the twenty-three `.py` there are Phase 4's to delete.

**Every baseline was re-measured first and every one matched**: codex-index-cam1753 clean at
`7e5ca23` with 23 tracked `.py` and 177 tracked files; MAM-basics' suite at the standing
baseline; its `check_all.py` 7 of 7 over 419 files and 278 `.py`; codex-index-cam1753's own
`check_all.py` 4 of 4.

### Twenty-three files, twelve of them deletions — one more than the plan predicted

| Deletion | Count | Why it is not an arrival |
|---|---|---|
| `mb_cmn/` | 3 | vendored from this repo, all three byte-identical blobs |
| `py_cam1753_word_image/` | 4 | one committed blob with this repo's copy, which arrived with book-of-job 2026-08-19 |
| `check_mark_order.py`, `check_escape_sequences.py`, `fix_mark_order.py`, `fix_escape_sequences.py` | 4 | this repo already holds all four; what they needed was this repo's code and corpus IN their scope, not a second copy |
| `py_mam_xml/mam_xml_verses.py` | 1 | **the twelfth, and the plan did not predict it** — see below |

**The plan's task said "about 11 files to move" and the answer is 11 exactly**, but the
arithmetic reaching it differs: the four lints, `py_cam1753_word_image/` and `mb_cmn/` are the
eleven deletions the plan names, and `py_mam_xml/mam_xml_verses.py` is a twelfth that the
prescription had listed as an **arrival** to "check against MAM-basics' `mb_xml` before
landing". That comparand is wrong — the module has nothing to do with `mb_xml` — and the right
one turns it into a deletion.

### The twelfth deletion: one tag, seven occurrences, and a fork nobody had classified

`codex-index-cam1753/py_mam_xml/mam_xml_verses.py` and this repo's
`py/py_ac_loc/mam_xml_verses.py` are **one tool with drift, not two tools** — 43 diff lines, 177
against 201, most of it docstring. Both read the same three books, and **the MAM-XML snapshots
in the two codex-index repos are byte-identical for all three**, checked on blobs.

**A tag census over Ps, Job and Prov settles it: exactly ONE tag is treated differently.**

| Tag | Ps | Job | Prov | `py_ac_loc` | `py_mam_xml` |
|---|---|---|---|---|---|
| `text` | 1238 | 304 | 251 | handled | handled |
| `lp-legarmeih` | 467 | 93 | 52 | handled | handled |
| `implicit-maqaf` | 82 | 19 | 15 | handled | handled |
| `kq` | 60 | 32 | 61 | handled | handled |
| `lp-paseq` | 51 | 4 | 5 | handled | handled |
| `kq-trivial` | 8 | 11 | 5 | handled | handled |
| `slh-word` | 3 | 5 | 3 | handled | handled |
| **`spi-invnun`** | **7** | 0 | 0 | **RAISED** | **silently skipped** |

Those seven are the inverted nuns (nun hafukha) of Psalm 107, first at `Ps.107.23`.
`mb_sefaria/mam4ajf_handlers.py` in this repo has always known them — its comment reads "the 7
Psalm 107 invnuns", beside the two of Numbers 10:35–36 that this module's callers never reach —
so the count is confirmed by a module written years earlier and for another purpose.
`py_ac_loc`'s copy grew a fail-fast `else: raise` for unknown tags and **was never given a
clause for that one**; `py_mam_xml`'s has no `else` at all and skips everything it does not
recognize.

**That is what has made `check_ac_all.py` exit on `check_line_breaks` since before this
programme began** — Phase 0 characterized it as `ValueError: Unhandled tag <spi-invnun> in verse
Ps.107.23` and deliberately did not fix it.

**And it is why "just import the other copy" was not available.**
`check_cam1753_all` → `check_line_breaks` → `gen_flat_stream` → the reader, so pointing
codex-index-cam1753's generator at the unfixed shared reader would have taken its `check_all.py`
from 4 of 4 to crashing — it would have inherited codex-index-aleppo's exact failure.

**Ben's decision, 2026-08-22, taken on a measurement rather than an argument**: add the one
`elif tag == "spi-invnun": pass` clause, alongside the `implicit-maqaf` and `shirah-space` skips
already there, and share one reader. Landed as **`b37bdb4`** here, separately from the move, and
proved by differential rather than asserted:

> Both readers loaded side by side, `get_verses_in_range` over whole-book ranges of all three
> books: **4512 verses, 30322 words, 0 mismatches.** Before the clause the MAM-basics reader
> could not complete Ps at all.

**What un-masking that check cost is smaller than it looked, and was measured before Ben was
asked rather than after.** `check_ac_all.py` now writes `check_line_breaks.html` in
codex-index-aleppo, which had been a fossil of a run that only ever saw one page: **1 page → 35,
2 issues → 93, 4,771 bytes → 18,377.** But **70 of the 93 are "No col 1 line markers; No col 2
line markers" across 29 of the 35 pages**, which is one cause and a known one — the N-of-M column
migration of `eb4bcaf` (2026-03-14) that also makes `check_ac_word_finding` fail 160 of 160. The
genuinely new signal is on six pages: columns short of 28 lines with gaps in the numbering, an
unhandled `unknown-dict(['blank-line'])` item type, one word after the last line-end, and on page
004r a **five-word alignment mismatch against MAM-XML**, every one offset by a single word.
Committed as **`a50f40e`** in codex-index-aleppo, in its own commit rather than alongside the
code change, so neither reads as the other's side effect.

**The transferable part is that the prescription named the wrong comparand and that is what hid
the fork for three weeks.** "Check `py_mam_xml/` against MAM-basics' `mb_xml`" sends a reader to
a package that shares no function with it; the real counterpart was a module of the *sibling
repo's* code, which had already moved here the day before. **Compare a module against what does
its job, not against what its name resembles.**

### The names, and the rule is the one codex-index-aleppo settled

| codex-index-cam1753 | MAM-basics | Files |
|---|---|---|
| the 8 runnable root modules | `py/py_cam1753_loc/` | 8 |
| — (new at this phase) | `py/main_cam1753_<stem>.py` | 8 |
| `cam1753_paths.py` | `py/cam1753_paths.py` | 1 |
| `check_all.py` | `py/check_cam1753_all.py` | 1 |
| `check_word_finding.py` | `py/check_cam1753_word_finding.py` | 1 |

**There was no package to keep, so `py_cam1753_loc` is named for `py_ac_loc`.** All fifteen of
that repo's modules sat loose at its root beside the data, and the prescription's "land it as a
package" is what this answers. **The eight drop a now-redundant `cam1753` infix that the package
name carries** — `gen_cam1753_flat_stream.py` is `py_cam1753_loc.gen_flat_stream` — and that is
what makes `main_cam1753_` plus the module stem a **rule** rather than a list: without the drop
the entry point would read `main_cam1753_gen_cam1753_flat_stream.py`.

**Four of the eight now share a name with their `py_ac_loc` counterpart exactly** —
`check_line_breaks`, `gen_flat_stream`, `gen_line_break_editor` and `gen_col_quad_editor` — which
is the payoff codex-index-aleppo's Phase 3 predicted when it prefixed all fifteen of its own
rather than only the five whose names were taken. The two manuscripts' answers to the same
problem now sit under the same module names in two packages, and the entry points differ only in
`main_ac_` against `main_cam1753_`.

**Every runnable module gets a wrapper, where codex-index-aleppo's root modules carried their
code into a top-level `main_ac_*.py`.** The difference is not a departure: that repo's
`py_ac_loc/` modules got thin wrappers and its *root* modules did not, and here every module
lands in the package, so every one takes a wrapper. Uniformity was worth more than the eight
seven-line files it costs, because six of the eight have a `main_ac_` counterpart addressing the
same problem.

### Three module-level scripts, where Phase 1 named two

`gutter_profile.py` and `split_cam1753_spreads.py` are the two Phase 1 recorded as having no
`main()` and no `if __name__` guard. **`download_cam1753_spreads.py` is a third**, and it is the
worst of them: `os.makedirs` and fourteen network reads at import. All three have a `main()` and
a guard now, and each says in its docstring why it grew one.

**That is codex-index-aleppo's finding recurring exactly.** Its `download_aleppo_pages.py` had
the identical shape and became `main_ac_download_pages.py` the day before — so the pair of
download scripts was the same defect in two repos, and the second copy was found by grepping for
`^def main(` across the whole tree rather than by trusting the plan's list of two.
`gen_col_quad_editor.py` needed a fourth, smaller version of the same treatment: its argument
parsing sat directly under `if __name__ == "__main__"` with no function to import, exactly as
`py_ac_loc.gen_col_quad_editor`'s had before Phase 1 gave it a `main()`.

### The third root walk is repaired, and Phase 0 was right that Phase 3 is where it becomes possible

`py_cam1753_word_image/page.py` composed `cam1753-line-breaks`, `cam1753-col-quads` and
`cam1753-pages` off a `Path(__file__).resolve().parent.parent` of its own. It now calls
`cam1753_paths.line_breaks_dir()`, `col_quads_dir()` and `pages_dir()`.

**Phase 0's Item 2 found two depth walks and recorded their verdicts as opposite, and both
readings held.** `py_ac_word_image_helper/flat_index.py` and `codex_page.py` were wrong here and
right there, and codex-index-aleppo's Phase 3 repaired them; this one was right there and inert
here, and this phase repairs it. Its one-blob relationship with codex-index-cam1753's copy ends
with the edit, deliberately: that copy is a Phase 4 deletion, so what looks like a fork is the
last few days of dual residency. A comment in the file says so.

**And it repairs a consumer, as codex-index-aleppo's did.**
`py/main_gen_cam1753_crop_editor.py` is book-of-job's tool and imports from this module, so it
inherited the missing directories the day book-of-job's Phase 3 landed the package here. The
import smoke test covers it, and it is the counterpart of `main_gen_aleppo_crop_editor.py`,
repaired the day before for the same reason.

### The lint union gains its fourth entry, and the corpus half gains its third

`repo_scopes.code_paths()` gains `cam1753_paths.code_paths()` and `corpus_roots()` gains
`cam1753_paths.cam1753_data_root()` — the two lines codex-index-aleppo's Phase 3 said this one
owed.

| Check | After codex-index-aleppo | After this phase |
|---|---|---|
| `check_mark_order` | 419 files | **510** |
| `check_escape_sequences` | 278 `.py` | **297** |

**The arithmetic is exact rather than approximate, which is what makes it an accounting.** The 19
new `.py` are the 8 package modules plus the 11 at `py/`'s top level; the 91 new files the
mark-order check reads are those 19 plus **72 JSON** — 27 line-break, 28 column-quadrilateral, 15
spread-split records, `cam1753-page-index.json` and `test-data-from-book-of-job.json`.

**Both still pass, and so does book-of-job's `check_all.py`, 7 of 7.** So the widening restored
codex-index-cam1753's coverage without importing a single violation, for the second repo running.

### The NFC test gains a SEVENTH scope, and this one is an expansion rather than a restoration

**codex-index-cam1753 is the one evacuated repo of the six that never had a copy of this test**,
so unlike the five before it there was nothing to fold in and nothing obliged the entry. The
plan asked for a deliberate decision; the decision is **to add it**, and the reasons are:

1. **After Phase 4 nothing anywhere would read that repo's hand-authored Hebrew** —
   `things-noticed-in-cam1753.md`, `page-snips/README.md`, `cam1753-page-index.json`, its two
   prose files and its three `doc/`.
2. **It passed on the first run**, so the expansion surfaced no violation that is nobody's
   current business.
3. The five other evacuated repos are all in scope, so leaving this one out would make it the
   exception a later session has to rediscover the reason for.

**That is the opposite call from the one `repo_scopes.py` records for the SOURCE lints**, where
UXLC-utils and holman-ketiv-qere are deliberately out. The two differ in what an expansion costs:
widening a source lint over code never held to it surfaces violations nobody has budgeted for,
where this check is a decidable property of hand-authored text that passed as soon as it was
asked. Both the `_Scope` comment and the module docstring say which case this is.

**Its exclusion list was CHOSEN rather than inherited**, on the principle the other six embody —
exclude what is downloaded, vendored or program-written, keep what a human wrote. Six trees are
out: `MAM-XML/` (vendored), `cam1753-spreads/` (downloaded), `cam1753-pages/` and
`cam1753-spread-splits-doc/` (written by `split_spreads`), and `cam1753-line-breaks/` and
`cam1753-col-quads/`, excluded because codex-index-aleppo's own copy excluded its counterparts of
exactly those two. `page-snips/` is deliberately kept, as codex-index-leningrad's is.

**39 files in scope, 16 after Phase 4** — measured, not predicted, and the prediction was 41
because it forgot that two of the tracked files are PNGs the binary-extension filter drops.
Floor 10.

### The oracle: 44 artifacts, 44 byte-identical, in both residencies

| Run | 28 `cam1753-pages/*.jpg` | 15 `cam1753-spread-splits-doc/*.json` | `check_line_breaks.html` |
|---|---|---|---|
| `main_cam1753_split_spreads.py` + `check_cam1753_all.py`, cwd = MAM-basics | identical | identical | identical |
| the same two, cwd = `C:\Users\BenDe\AppData\Local\Temp` | identical | identical | identical |

**44, not the 45 the plan's task names**, and the difference is the one Phase 1 already
recorded: `cam1753-gutter-profiles.png` is the forty-fifth and is **not an oracle**, re-rendering
byte-identical run-to-run under one matplotlib version but 1,541 bytes larger than the tracked
copy. It was not run, and the tracked copy is untouched.

`check_cam1753_all.py` reports **4 of 4** from MAM-basics, and `git status --porcelain` in
codex-index-cam1753 is empty after every run — which is the right instrument in that repo, Phase
1 having measured 1 latent CRLF of 176 files there and having closed the seven missing
`newline=""` sites that made it lie.

### Path-equality: eleven accessors, eleven equal

Both `cam1753_paths` copies loaded side by side under different module names, every zero-argument
accessor called on each: **11 of 11 equal**, every one resolving under
`C:\Users\BenDe\GitRepos\codex-index-cam1753`. `code_paths` is the one addition, and `CODE_DIR`
moves on purpose, from that repo's root to this repo's `py/`.

That is the instrument codex-index-aleppo's Phase 3 recommended, applied for the second time and
for the same reason: **it needs no oracle**, so it covers the artifacts nothing regenerates. Do
it before Phase 4 deletes the other copy.

### Two contrasts with codex-index-aleppo's Phase 3, both of them absences

- **Not one of the 23 copied files was CRLF.** codex-index-aleppo's checkout is where Phase 1
  measured 152 latent CRLF of 222, and ten of its copied files had to be normalized on arrival.
  codex-index-cam1753's `.py` are all LF in the working tree, checked with `git ls-files --eol`
  before the copy and `file` after it. **The check was still worth running** — its cost is one
  command and its absence would have been invisible.
- **No module rebinds `sys.stdout`.** codex-index-aleppo's `main_find_word_in_aleppo_images.py`
  replaced it at import and so discarded whatever the previous stream had buffered, which is how
  it silently ate eighteen lines of that phase's import smoke test. `git grep sys.stdout` over
  this repo's arriving code returns nothing, so the one destructive side effect of the three that
  phase found has no counterpart here.

### Verification

- **Oracle: 44 of 44 byte-identical**, from MAM-basics' root and from a foreign working
  directory, compared with `git cat-file blob HEAD:<path>` and `cmp`.
- **`check_cam1753_all.py` 4 of 4** from both working directories.
- **Import smoke over all 23 moved and edited modules: 23 of 23**, including
  `main_gen_cam1753_crop_editor.py`, book-of-job's consumer of the repaired `page.py`.
- **Path-equality: 11 of 11 accessors equal.**
- **Reader differential: 4512 verses, 30322 words, 0 mismatches.**
- **`py/check_all.py` 7 of 7**, over the widened **510** files and **297** `.py`.
- **black clean on all 22 files this phase added or edited.**
- **`git status --porcelain` empty in codex-index-cam1753 at `7e5ca23`**, unchanged throughout.

### What Phase 4 now owes for this repo

1. **Twenty-three `.py` to delete**, emptying `mb_cmn/`, `py_cam1753_word_image/` and
   `py_mam_xml/` outright and taking the fifteen loose modules off the repo root.
2. **`README.md:4` calls the manuscript μC where the code and the generated site say μY**, 57 to
   0 — the same correction book-of-job's Phase 4 made in its own doc on 2026-08-21 and
   codex-index-aleppo's made in its README the same day as this phase.
3. **`codex-index-cam1753.code-workspace` and `requirements.txt` are its two orphan candidates**,
   and it has **no `.claude/`**, so its unforced set is two files rather than
   codex-index-aleppo's three. Read the workspace file rather than assuming it.
4. **Sweep its prose with the wide `py/…` grep and with the module basenames.** Its Python sat at
   the **repo root**, so a `py/` prefix matches almost nothing that moved — book-of-job's shape
   rather than codex-index-aleppo's, and book-of-job's Phase 6 recorded that the path-shaped grep
   found one of five citations there.
5. **The NFC scope's 16 is checked against 39**, so re-run the scope count after the deletion and
   confirm 16 rather than assume it.
6. **Classify all its tracked files rather than adding up the trees a prediction names**, which
   is what made codex-index-aleppo's 154 come out exact.

---

## Phase 3 — copy the Python in (dual residency) — the prescription, left as written 2026-08-02

**The two records above answer this for two of the three repos.** Four of its rows read
differently after execution: `main_update_vendored_files.py` does not "disappear", it is renamed
and keeps its job; `vendoring_sync.py` resolves into a parameter of `mb_cmn/vendoring_sync.py`
rather than into that repo's `mb_cmn`, which it never had; the six `check_*`/`fix_*` land as
**two** files rather than one reconciled copy, the other four being deletions because this repo
already holds them; and `py_ac_word_image_helper/` is a deletion for the same reason rather than
a copy to reconcile.

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

## The Phase 4 gate is lifted — **DECIDED 2026-08-22**

The prescription below says "Stop and ask Ben before each." **Ben, 2026-08-22, asked whether to
keep that gate or run Phase 4 for a repo as soon as its Phase 3 is green: run it as soon as
Phase 3 is green.** So Phase 4 for a repo is part of the same unit of work as its Phase 3 and
needs no separate yes. The gate sentence below is left as written, being what the plan said
before he settled it.

**This does not license the sub-decisions inside Phase 4.** What to do with a file the move
orphans but does not delete — a workspace file, a `requirements.txt`, a `.vscode/` config — was
Ben's call at book-of-job's Phase 4 and stays his wherever the answer is not forced. A file whose
every line names something the move took is forced and needs no asking; one that would still be
useful to a repo that is staying is not.

---

## Phase 4, codex-index-leningrad — the execution record — **DONE 2026-08-22**

**Landed as `824910e` in codex-index-leningrad — 22 files deleted, 2 modified, and that repo now
tracks no Python at all.** Nothing was owed in MAM-basics beyond a figure correction, recorded
under Verification below.

### The deletion is 22 files, and 21 of them are the Python

All twenty-one tracked `.py`: `lenin-wiki/main_make_wikisource_page.py` and the eighteen under
`lenin-wiki/py/`, the root `main_update_vendored_files.py` and `vendoring_sync.py`, and
`py/tests/test_h_dot_below_nfc.py`. `lenin-wiki/py/` and `py/tests/` are gone as directories, and
so is `py/`, which held nothing else.

**The twenty-second is `.vscode/launch.json`, deleted as orphaned**, and it is the one file in
this phase that needed a judgment rather than a rule. Both of its debugpy configurations named a
program the move had taken. **One of the two had been wrong for five months on top of that**: it
named `aleppo/main_make_wikisource_page.py`, a path this repo has never had — `aleppo/` was
codex-index-aleppo's directory name until `9025037` renamed it to `aleppo-wiki/` on 2026-03-28,
the same rename that killed that generator's four path literals. So the file was a launcher for
one program that no longer lives here and one that never did.

**That is the forced case, not a precedent for the unforced one.** Every line of the file named
something gone; nothing in it would serve a repo that is staying. codex-index-aleppo's
`requirements.txt`, `.claude/settings.json` and workspace file are the unforced case and are
Ben's, per the section above.

### The two prose files, written for a repo that is staying

`README.md` and `CLAUDE.md` both now say the Python left and the data did not, and neither reads
as a wind-down — per Ben's decision of 2026-08-22 recorded in "This plan moves the Python and
nothing else".

`CLAUDE.md` gained four things a reader of that repo alone could not otherwise find:

1. **Which MAM-basics entry point writes what**, with the absolute-path PowerShell command for
   each: `main_lenin_wikisource_page.py` for the three files under `lenin-wiki/`,
   `main_lenin_vendor_uxlc.py` for `UXLC-utils-sparse/`.
2. **Why each was renamed** — the first because codex-index-aleppo holds a file of that name and
   the two are different tools; the second because `main_update_vendored_files.py` was held by
   three repos at once and names no vendored files.
3. **That `UXLC-utils-sparse/` is behind**, taken at UXLC-utils `748ee2f` on 2026-08-03, and that
   refreshing it moves the three `lenin-wiki/` artifacts as well, `lci_augrecs.json` being the
   pipeline's input. So the refresh is a regeneration rather than a data update.
4. **That MAM-basics still scans this tree for NFC**, through a scope of its own, so deleting
   `py/tests/test_h_dot_below_nfc.py` did not end the check it ran.

**What no program writes is named**, as this phase requires: `page-snips/` (one PNG crop and the
README recording what it settles), the two prose files and the two dotfiles.
`UXLC-utils-sparse/` is called vendored rather than generated, the distinction being that the
refresh copies it and UXLC-utils' own generators write the originals.

### Verification

- **The three artifacts under `lenin-wiki/` are byte-identical to their HEAD blobs after a run of
  MAM-basics' pipeline made AFTER the deletion.** That is the check worth doing in this order:
  running it before the deletion proves the move, running it after proves the deletion took
  nothing the move needed.
- `git status --porcelain` clean in codex-index-leningrad at `824910e`; `git ls-files '*.py'`
  returns **0**.
- The NFC scope re-counted: **8 files, not the 9 this plan's Phase 3 record predicted.** The
  ninth was `.vscode/launch.json`, which this phase deleted. `py/tests/test_h_dot_below_nfc.py`'s
  comment and module docstring in MAM-basics are corrected to 8, with the reason.
- Floor 5 against 8, so the floor still means "an exclusion filter swallowed everything" rather
  than asserting a tree size.

### What Phase 6 and Phase 7 now owe for this repo

1. **Phase 7 item 2 wants rewording rather than deleting, and now has its wording.**
   `in/vendoring_policy.json`'s comment for codex-index-leningrad says the
   `main_update_vendored_files.py` the provenance scan finds there is not a MAM-basics one. That
   script is gone from that repo, so the sentence describes something that no longer exists — but
   the sync it describes still happens, from MAM-basics' `main_lenin_vendor_uxlc.py`. Say that.
2. **The four `overrides` rows naming codex-index-leningrad paths** are part of Phase 7 item 1's
   eight, and they name `lenin-wiki/py/` files that no longer exist.
3. **Phase 7 item 5 — that repo's `.venv`** holds black and no pytest, and now has no Python to
   run against.
4. **Phase 6's grep for "generated by codex-index"** has one fewer place to find anything: the
   provenance breadcrumb `UXLC-utils-sparse/provenance.md` is written by MAM-basics now and names
   UXLC-utils as its source, not this repo.

---

## Phase 4, codex-index-aleppo — the execution record — **DONE 2026-08-22**

**Landed as `078b74d` in codex-index-aleppo — 50 files deleted, 5 modified, and that repo now
tracks no Python at all.** Tracked total 228 → **178**. Nothing was owed in MAM-basics beyond
one figure correction, recorded under Verification below, and a **second repo's** figure
correction that this phase's own measurement turned up — `2abd7f6` in codex-index-leningrad.

**Every baseline was re-measured first and every one matched exactly**: codex-index-aleppo
clean at `ee09e67` with 50 tracked `.py`; codex-index-cam1753 clean at `7e5ca23` with 23;
codex-index-leningrad clean at `824910e` with 0; MAM-basics clean at `98053b7` with **945
passed, 5 skipped, 59 subtests** and `py/check_all.py` **7 of 7** over 419 files and 278 `.py`.
No mismatch, so there is no finding to report against the task's stated state.

### The deletion is 50 files and every one of them is Python

`py/`, `py/tests/`, `py/py_ac_loc/`, `py/py_ac_word_image_helper/`, `py/mb_cmn/` and
`aleppo-wiki/py/` are gone as directories. **Unlike codex-index-leningrad's Phase 4, no
twenty-second file rode along**: that repo's `.vscode/launch.json` was forced — every line of
it named a program the move had taken — and codex-index-aleppo has no `.vscode/` at all. Its
three orphan candidates are the unforced case and are Ben's, per "The Phase 4 gate is lifted";
they are recorded in their own subsection below.

**The order that proves the deletion is the order this phase ran in.** Both generators were run
from MAM-basics **before** the deletion and again **after** it, and all four tracked artifacts
came back byte-identical against `git cat-file blob HEAD:<path>` both times. Running before
proves the move; running after proves the deletion took nothing the move needed. That is
codex-index-leningrad's Phase 4 recipe applied unchanged, and it is worth keeping because the
pre-deletion run is the one a session is tempted to skip.

| Run | `index-flat.json` | `index-grouped-by-book.json` | `index.wiki` | `index-flat-annotated.json` |
|---|---|---|---|---|
| MAM-basics' copy, before the deletion | identical | identical | identical | identical |
| MAM-basics' copy, after the deletion | identical | identical | identical | identical |

Re-establish with:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_ac_wikisource_page.py
```

### The doc repointing is twenty-six sites in four files, and three of them were wrong before this programme began

The plan's item 2 hands this phase **one** site, `doc/aleppo-line-breaks.md:110`. Swept with
`git grep -nIoE '(^|[^-a-zA-Z0-9/_.])py/[A-Za-z_0-9./]*'` over the surviving prose, the real
count is **26 sites across `doc/aleppo-line-breaks.md` (8), `doc/ocr-with-kraken.md` (5),
`doc/reading-mam-simple.md` (1), `README.md` (5) and `CLAUDE.md` (7)**. That is book-of-job's
Phase 4 lesson — repointing a doc is not just the site the plan names — met at a repo whose
plan named exactly one.

**Three of the twenty-six were not made stale by this programme, and two of the three name a
directory neither repo has ever had.** They are worth separating from the twenty-three the move
broke, because a session that "repoints" them mechanically writes `../MAM-basics/` in front of
a path that never existed:

- **`doc/aleppo-line-breaks.md:110`** gave `python py/py_ac_loc/gen_lb_flat_stream.py 270v`.
  Phase 1 found that this has raised `ModuleNotFoundError` ever since that module gained an
  intra-repo import, because `py_ac_loc/` modules import a sibling as `py_ac_loc.<name>`. It is
  now the MAM-basics wrapper `main_ac_gen_lb_flat_stream.py`, spelled with the absolute
  interpreter path, **so the correction and the repoint are one edit** exactly as the plan
  predicted.
- **`doc/aleppo-line-breaks.md`'s folder-layout block and its lines 30, 113 and 163** put
  `line-breaks/`, `codex-index/` and `MAM-simple/` under `py/py_ac_loc/`. None of the three has
  ever been there: the data is at the repo root, and `codex-index` was a **sibling repo** the
  2026-03-28 rename `9025037` removed. The file contradicted itself about this the whole time —
  its own Export step says "move the downloaded file into `line-breaks/`", which is right.
- **`doc/ocr-with-kraken.md:116`** does the same for `column-coordinates/`.

**The rewritten folder-layout block keeps the wrong paths as ✗ rows rather than deleting them**,
with one line each saying what was wrong. A reader who remembers the old shape would otherwise
go looking for a directory three separate sentences had promised them.

**`doc/ocr-with-kraken.md`'s two commands are repointed and explicitly marked untested.**
They run a WSL kraken interpreter that is no part of either repo, and **kraken is in no venv on
this machine** — not codex-index-aleppo's and not MAM-basics', which Phase 3 recorded as a
deliberate non-installation. So `main_ac_kraken_seg_baselines.py` is still the one entry point
of the eleven that does not import. Phase 1 left these two sites for exactly this reason; the
answer taken here is to repoint them and say in the file that they are the shape to restore
rather than something known to work, which is cheaper than leaving a reader to find out.

### A sigil disagreement that book-of-job's Phase 4 had already settled once

**`README.md` called the Cambridge 1753 manuscript μC, and the code and the generated site call
it μY.** Measured across MAM-basics 2026-08-22: **57 occurrences of μY against 3 of μC**, and
all three of the μC are these plan files quoting the finding. `py/author_boj/job6_cam1753_mentions.py`
is the proof rather than the count — the module that lists Job detail pages mentioning the
Cambridge manuscript tests `"μY" in _extract_text(value)`.

book-of-job's Phase 4 found the same disagreement in `cam1753-word-crops.md` on 2026-08-21 and
corrected that file to μY; `doc/boj-cam1753-word-crops.md` here reads μY today. So this is not a
new call, and codex-index-aleppo's README was corrected on that precedent rather than on this
phase's own judgment.

**codex-index-cam1753's own `README.md:4` said μC too, and its Phase 4 settled it the same day.**
That one is the repo describing its own manuscript rather than an aside about a sibling, which is
a slightly bigger claim to change, but the measurement is the same one. **All three repos that
name this manuscript now agree with the code.**

### The three orphan candidates, and why none of them is forced

Named by the plan's item 3 and put to Ben one at a time, per "This does not license the
sub-decisions inside Phase 4". All three are in the NFC scope and all three name the moved code
or the venv it needed:

| File | What the move leaves of it | Why it is not forced |
|---|---|---|
| `requirements.txt` | nothing — black, matplotlib, pyspellchecker, and no Python here imports any of them | book-of-job's counterpart was deleted as orphaned on Ben's decision, but that repo has no Pages workflow to reason about — **Ben's answer 2026-08-22: delete it**, landed as `b2b347e` there |
| `codex-index-aleppo.code-workspace` | the `.venv\Scripts\python.exe` auto-approve entry | it also declares a **three-folder view** opening this repo beside book-of-job and codex-index-cam1753, which is not about Python — the same thing that made book-of-job's a question rather than a step |
| `.claude/settings.json` | six of its ten permission globs name a `.venv` python that no longer runs here | the other four are still live: `Bash(git *)`, two `gh issue` globs, and a `Read()` glob over the Yeivin scans folder |

**`pages.yml` was checked rather than assumed, and it decides nothing.** It is
`actions/checkout` → `configure-pages` → `upload-pages-artifact` with `path: gh-pages` →
`deploy-pages`, and **runs no Python at all**. So the Pages workflow this repo keeps, which is
the one thing distinguishing it from book-of-job, does not need `requirements.txt` and is not a
reason to keep it. Whether the file is worth keeping for a human who might want the venv back is
the actual question, and that is Ben's.

**All three were answered, one at a time, on 2026-08-22, and Ben deleted all three.** The scope
figure moves once per answer — **29 → 28 → 27 → 26** — and the tracked total **178 → 175**:

| File | Landed | Ben's reason |
|---|---|---|
| `requirements.txt` | **`b2b347e`** | orphaned by the move; the Pages workflow turned out not to be the difference it looked like, so book-of-job's decision holds here after all |
| `codex-index-aleppo.code-workspace` | **`2bdcfde`** | orphaned; **asked as ONE question covering codex-index-cam1753's too**, the two being near-identical, and answered "delete both" |
| `.claude/settings.json` | **`3003a06`** | **not orphaned at all** — see below |

**The third one is the interesting answer, and it is not an evacuation decision.** Six of that
file's ten permission globs were still live — `Bash(git *)`, three `gh issue` globs, a `Read()`
over the Yeivin *Introduction to the Tiberian Masorah* scans, and
`Bash(**/.venv/Scripts/python.exe **/*)`, which still matched when a session sitting in
codex-index-aleppo reached sideways for MAM-basics' interpreter, now the only way to run anything
against that repo's data. Only the four naming that repo's own `.venv` were dead. **Ben's reason,
in his own words: the file "dates from before 'auto' permissions caused me to struggle mightily,
and with little success, to get permissions set up."** It is a fossil of an approach he has moved
off, and the move merely brought it to his attention.

**The transferable part: an orphan sweep can surface a file worth deleting for a reason the
sweep knows nothing about.** Two of these three were forced-ish and one was not, and the one that
was not is the only one where reading the file's contents would have argued for keeping it.
**Put the file to Ben rather than deciding it from what the move touched**, which is what "This
does not license the sub-decisions inside Phase 4" already says and what this is the worked
example of.

codex-index-aleppo was the only one of the three repos with a `.claude/` at all, so that
directory is gone with the file.

### What no program writes: 154 of 162, and the classification is arithmetic rather than judgment

The plan's item 5 predicts 154 and names six trees adding to 136. The gap is not an error in
either figure — the prediction's list is incomplete rather than wrong. **Measured by classifying
all 178 tracked files**: 16 are the repo's own furniture (the four `doc/`, `pages.yml`,
`.claude/settings.json`, `requirements.txt`, the workspace file, three provenance files,
`README.md`, `CLAUDE.md`, `.gitignore`, `.gitattributes`, and `aleppo-wiki/LICENSE.txt`), which
leaves **162 artifacts**, of which **8 are generated** and **154 are not**. That reproduces
Phase 1's "162 artifacts in codex-index-aleppo with 8 generated" exactly.

**Deleting the three takes the furniture to 13 and the tracked total to 175, and moves
neither artifact figure** — which is the point of counting the two groups separately rather than
subtracting from the tracked total.

The eight generated are the three under `aleppo-wiki/`, `index-flat-annotated.json`,
`check_line_breaks.html` and the three PNGs under `plot_col_coords-out/`. The 154 are 37
downloaded scans, 35 line-break and 35 column-coordinate JSON, 24 vendored `MAM-XML/`, 10 of
`aleppo-wiki/` (the CSV index, its five precursors, `index-flat-corrected.json` and three
Wikisource notes), 8 of `ds-flat-stream/`, the 4 `gh-pages/` files and
`test-data-from-book-of-job.json`.

**`ds-flat-stream/` is the entry worth writing down, because it looks regenerable and is not.**
Its generator exists and runs, but it takes explicit per-page verse ranges as arguments and
**those arguments are recorded nowhere**, so the eight files cannot be reproduced from anything
tracked. `CLAUDE.md` says so in the table rather than leaving the reader to infer it from
"generated".

### A second repo's figure was wrong, and this phase's own measurement is what found it

**codex-index-leningrad's `CLAUDE.md:101` said "Nine files are in scope after the move" where
its own Phase 4 record, two days' reading above, says **8** and had already corrected
MAM-basics' copy of the test.** That phase measured 8, wrote the correction into
`py/tests/test_h_dot_below_nfc.py` here, and left its own prediction of 9 standing in the prose
it wrote the same day. Fixed as **`2abd7f6`** in that repo.

**What found it was running the scope count for all six scopes rather than for the one this
phase needed.** The script imports `py/tests/test_h_dot_below_nfc.py` and calls
`_tracked_files_in_scope` on each `_Scope`; reading the whole output cost nothing and the
neighbouring row was visibly wrong. **A phase that measures one figure should print the ones
beside it** — this is the cheapest instance of that in the programme so far, and it is the same
shape as Phase 1's "read what it counted, not whether it passed".

Re-establish with the six-line scratch script this phase used: 1328, 11, 45, 33, 8, 29 — and
1328, 11, 45, 33, 8, **26** after Ben's three decisions below.

### Verification

- **Both generators run AFTER the deletion, four artifacts byte-identical** to their HEAD blobs,
  compared with `git cat-file blob HEAD:<path>` and `cmp`. Table above.
- **`git status --porcelain` in codex-index-aleppo showed exactly 50 deletions and 5
  modifications** before staging, and nothing else — so neither regeneration run left a single
  artifact dirty, in a repo where Phase 1 measured 152 latent CRLF of 222 files.
- **MAM-basics suite: 945 passed, 5 skipped, 59 subtests** — the baseline exactly. The
  `59 subtests` figure reproduces for the **eighth** measurement running.
- **`py/check_all.py` 7 of 7**, over **419** files and **278** `.py` — both unchanged by the
  deletion, which is the expected result and was checked rather than assumed: `code_paths()`
  names MAM-basics' own paths, so emptying the data repo cannot move either count.
- **Both pre-existing failures reproduce at their exact tallies**: `py/check_ac_word_finding.py`
  **0 of 160**, every failure a `col:` clause; `py/check_ac_all.py` raising
  `ValueError: Unhandled tag <spi-invnun> in verse Ps.107.23` out of `py_ac_loc/mam_xml_verses.py:116`.
  An unchanged failure is evidence — a deletion that took something the move needed would have
  changed one of these two.
- **The NFC scope re-counted at 29**, the figure Phase 3 predicted, so unlike
  codex-index-leningrad's Phase 4 there is no correction owed. **It is 26 after Ben's
  three orphan decisions below**, and the comment in `py/tests/test_h_dot_below_nfc.py`
  carries both numbers with the reason the count moved. Floor 20 against 29, so the floor
  still means "an exclusion filter swallowed everything" rather than asserting a tree size. The
  comment in `py/tests/test_h_dot_below_nfc.py` is reworded from a prediction to a measurement.
- **`git ls-files '*.py'` returns 0** in codex-index-aleppo, and the tree is clean at `078b74d`.
- `HEAD` and `git log` re-read before staging in all four repos, every file staged by explicit
  path, and both pushes fast-forward with no `--force`.

### What Phase 6 and Phase 7 now owe for this repo

1. **`py/gen_permission_glob.py:8` cited `../masorah-books/.claude/test_globs.py`** and moved
   here as `py/main_gen_permission_glob.py` carrying that citation. Phase 1 named it as Phase
   6's; it is now a MAM-basics file rather than a codex-index-aleppo one, so it falls under this
   repo's own standing sentence about the eight stale `../masorah-books/…` spellings in
   `py/accgram/` rather than under a codex-index breadcrumb sweep.
2. **`__pycache__` directories survive the deletion, and so do the empty `py/` and
   `aleppo-wiki/py/` directories that hold them.** They are gitignored, so git never saw them
   and `git status` is clean; codex-index-leningrad's Phase 4 left the same thing. **Phase 7 item
   5 owns them**, along with that repo's `.venv`.
3. **Phase 7 item 1's override rows**: four of the eight name codex-index-leningrad paths and are
   already dead; the codex-index-aleppo rows name `py/mb_cmn/` and `aleppo-wiki/py/` files that
   no longer exist either.
4. **Phase 6's `git grep -lI "generated by codex-index"` has nothing to find here**, checked
   during this phase: no code in this repo ever passed `generator_file` to `mb_cmn.file_io`, and
   the four regenerated artifacts carry no provenance breadcrumb. Run it anyway, per
   book-of-job's Phase 6 lesson that a zero from the breadcrumb grep is not the answer — the
   wider `py/…` sweep is what found the twenty-six sites above.

### What codex-index-cam1753's Phase 4 now owes, beyond what it already knew

**All four were discharged the same day; that phase's own record, below, says how each came
out.** Item 1 in particular paid off beyond what it asked for, the basename sweep finding a code
citation inside a tracked data file that no path-shaped grep would have reached.

1. **Sweep its prose for `py/…` with the wide grep, not for the sites its plan names.** Its
   Python sits at the **repo root**, so a `py/` prefix matches almost nothing that moved — this
   is book-of-job's shape rather than codex-index-aleppo's, and book-of-job's Phase 6 recorded
   that the path-shaped grep found one of five citations there. **Grep for the module basenames
   as well.**
2. **`README.md:4` calls the manuscript μC where the code and the site say μY**, 57 to 0. The
   correction is book-of-job's Phase 4 precedent of 2026-08-21, applied here for
   codex-index-aleppo's aside about the same manuscript.
3. **`codex-index-cam1753.code-workspace` and `requirements.txt` are its two orphan
   candidates**, and it has no `.claude/` — so its unforced set is two files rather than three.
   Read the workspace file rather than assuming it, per book-of-job's Phase 4.
4. **Classify all its tracked files rather than adding up the trees a prediction names.** The
   154 above came out right only because the furniture was counted and subtracted; the plan's own
   list of trees adds to 136.

## Phase 4, codex-index-cam1753 — the execution record — **DONE 2026-08-22**

**The last repo of the trio, and of the whole evacuation programme, to be emptied.** Landed as
**`a9c3abd`** in codex-index-cam1753 — 25 files deleted, 5 modified — and that repo now tracks
no Python at all. Tracked total 177 → **152**. **All three of the trio hold zero `.py`**, and
with book-of-job, holman-ketiv-qere and UXLC-utils before them, so do all six repos this
programme set out to evacuate.

### The deletion is 25 files, and Ben settled both of the two beyond the Python

Twenty-three tracked `.py`, emptying `mb_cmn/`, `py_cam1753_word_image/` and `py_mam_xml/`
outright and taking the fifteen loose modules off the repo root. **The other two were the
unforced case**, asked one at a time per "The Phase 4 gate is lifted", and both answered the
same day:

- **`requirements.txt`** — deleted. Ben's answer for codex-index-aleppo's was taken as settling
  this one too, and said so before acting: the two files name the same three packages, black,
  matplotlib and pyspellchecker, and this repo has **no Pages workflow**, which was the only
  thing that made codex-index-aleppo's worth a question of its own.
- **`codex-index-cam1753.code-workspace`** — deleted, and **this one was asked as a single
  question covering both repos' workspace files**, the two being near-identical. Each declared a
  three-folder view of the same cluster from its own vantage point: this repo's opened itself
  beside book-of-job and codex-index-aleppo, and codex-index-aleppo's opened itself beside
  book-of-job and this repo. **book-of-job's declared the same cluster and had already gone** on
  2026-08-21, so the question put to Ben was whether to keep one as the cluster's entry point;
  his answer was to delete both. Nothing opens those three repos together now, and
  MAM-basics' `all-repos.code-workspace` is where a sweep still reaches all three.

**codex-index-cam1753 has no `.claude/` at all**, so its unforced set was two files where
codex-index-aleppo's was three.

### The prose sweep found more than a `py/` grep could, and the plan said it would

**This repo's Python sat at its ROOT**, so `py/` matches almost nothing that moved — book-of-job's
shape rather than codex-index-aleppo's, and its Phase 6 recorded that a path-shaped grep found
one of five citations there. Swept instead by **module basename**, over every tracked `.md` and
`.json`:

| File | Sites | What they were |
|---|---|---|
| `README.md` | 8 | the whole pipeline list, plus `LINES_PER_COL`'s home |
| `CLAUDE.md` | 5 | the editor/server table and the mark-order pointer |
| `doc/cam1753-line-break-task.md` | 9 | four runnable commands, a checklist and a module table |
| `doc/reading-mam-simple.md` | 3 | the reader and its caller |
| **`cam1753-page-index.json`** | **1** | **a code citation inside a tracked DATA file** |

**The last row is the one worth carrying.** `cam1753-page-index.json`'s `comment` field explains
that its `de_archive_spread` number "equals the jp2 file number `download_cam1753_spreads.py`
uses" — a bare module filename, in a data artifact, which **no path-shaped grep anywhere would
have found** and which a sweep of `doc/` and the two prose files would have missed as well. It
now names `../MAM-basics/py/main_cam1753_download_spreads.py`. Nothing reads that file, so the
edit is safe; the point is that the citation existed at all. **Sweep tracked DATA for module
names, not only tracked prose.**

**`doc/cam1753-line-break-task.md` spells its four commands with BACKSLASHES**, so a
forward-slash pass finds none of them — book-of-job's Phase 4 recorded exactly this about
`cam1753-word-crops.md`, and it recurs here in the sibling repo about the same manuscript. `sed`
could not take them either; a throwaway Python script did. That file also carried a standing
instruction to "always use `.venv\Scripts\python.exe`", which now names an interpreter with none
of this project's Python left to run, so it says to use MAM-basics' by absolute path instead.

### The sigil is corrected, on the precedent set two days earlier

**`README.md` called the manuscript μC where the code and the generated site say μY**, 57
occurrences against 0 measured across MAM-basics. book-of-job's Phase 4 made the same correction
in `boj-cam1753-word-crops.md` on 2026-08-21 and codex-index-aleppo's README was corrected the
same day as this phase, so **all three of the repos that name this manuscript now agree with the
code**. `py/author_boj/job6_cam1753_mentions.py` is the proof rather than the count: the module
that lists Job detail pages mentioning the Cambridge manuscript tests `"μY" in _extract_text(value)`.

### What no program writes: 97 of 142, and the classification reproduces Phase 1 exactly

Measured by classifying all 152 tracked files rather than by adding up the trees a prediction
names, which is what made codex-index-aleppo's figure come out exact:

- **10 are the repo's own paperwork** — three `doc/`, `README.md`, `CLAUDE.md`, two provenance
  files, `things-noticed-in-cam1753.md` and two dotfiles — leaving **142 artifacts**.
- **45 of the 142 are generated**, and **97 are not**.

That reproduces Phase 1's "142 in codex-index-cam1753 with 45 generated" to the file, three
weeks and two phases later.

**Only 44 of the 45 are regenerable, and the distinction is worth keeping in the prose rather
than in a plan.** `cam1753-gutter-profiles.png` re-renders byte-identically run-to-run under one
matplotlib version and 1,541 bytes larger under a newer one, so its bytes track the library
rather than the code. `CLAUDE.md` says so beside the oracle commands, so that a reader who runs
everything and finds one file dirty knows which one and why.

### Verification

- **The oracle passed AFTER the deletion**: `main_cam1753_split_spreads.py` and
  `check_cam1753_all.py` run from MAM-basics, and **all 44 artifacts byte-identical** to their
  HEAD blobs — 28 `cam1753-pages/*.jpg`, 15 `cam1753-spread-splits-doc/*.json` and
  `check_line_breaks.html`, compared with `git cat-file blob HEAD:<path>` and `cmp`. Running
  before the deletion proves the move; running after proves the deletion took nothing the move
  needed, and this phase did both.
- **`check_cam1753_all.py` 4 of 4**, with word finding still **160 of 160**.
- **`py/check_all.py` 7 of 7** over 510 files and 297 `.py`, unchanged by the deletion — checked
  rather than assumed, `code_paths()` naming MAM-basics' own paths.
- **The NFC scope re-counted at 14, against a prediction of 16**, and the two-file gap is
  Ben's two deletions above rather than an error: 39 − 23 `.py` = 16, − `requirements.txt` −
  the workspace file = 14. The comment in `py/tests/test_h_dot_below_nfc.py` carries the
  prediction, the measurement and the reason they differ. Floor 10 against 14.
- **`git ls-files '*.py'` returns 0** in codex-index-cam1753, and the tree is clean.
- `HEAD` and `git log` re-read before staging, every file staged by explicit path, pushes
  fast-forward with no `--force`.

### A second session was live in MAM-basics throughout, and did not collide

`doc/PLAN-evacuate-python-programme.md` acquired an uncommitted 81-line addition partway through
this session — a "the site's landing page becomes generated" decision — and then landed as
`2d36dbe` on top of this session's `fde301d`. **That file was left strictly alone**, including
the trio's row in its Status table, which would otherwise have been this phase's to update.

Non-collision was proved rather than assumed, by the three checks `~/.claude/CLAUDE.md`
prescribes: `HEAD` re-read immediately before each commit, every path staged explicitly and no
`git add -A`, and every push fast-forward. **Watching transcript byte counts was not the
instrument and was not reached for.** Whoever picks up Phase 6 or 7 should update that Status
row, which is one sentence and is all the programme file owes the trio.

### What Phase 6 and Phase 7 now owe for this repo

1. **Phase 7 item 1's `in/vendoring_policy.json` entry for codex-index-cam1753** names
   `mb_cmn/` paths that no longer exist. Its three trio entries and eight `overrides` rows are
   now all dead, this being the last of the three to empty.
2. **Phase 7 item 5 — this repo's `.venv`**, which has black and no pytest, and now has no
   Python to run against. Its `__pycache__` directories survive the deletion, as
   codex-index-leningrad's and codex-index-aleppo's do.
3. **Phase 6's `git grep -lI "generated by codex-index"` has nothing to find here**, checked
   during this phase. Run it anyway, per book-of-job's Phase 6 lesson that a zero from the
   breadcrumb grep is not the answer — the module-basename sweep above is what found five files
   and a data artifact that no breadcrumb grep would have.
4. **`doc/PLAN-evacuate-python-programme.md`'s trio Status row is unwritten**, deliberately, for
   the reason the section above gives.

---

## Phase 4 — empty each repo — the prescription, left as written 2026-08-02

**None of the three has a `CLAUDE.md`** — codex-index-aleppo does, the other two do not.
Whichever the repo, write or update one in this phase saying that there is no Python left, that
the code is `../MAM-basics/py/`, and which entry point writes what. **Name the tracked artifacts
no program generates**, which for these repos includes the downloaded scans.

**Phase 0 corrected the first sentence above: all three got a `CLAUDE.md` on 2026-08-03**, one day
after this plan was written, so this phase updates three files and writes none from nothing.

**Write each repo's `README.md` and `CLAUDE.md` for a repo that is staying, not one being wound
down.** Per Ben's decision of 2026-08-22, recorded in the section "This plan moves the Python and
nothing else" above, each of these three repos keeps its data — the manuscript scans, the derived
line-break and column-coordinate JSON, the `MAM-XML/` trees — and goes on hosting it indefinitely.
So the prose says the code moved to `../MAM-basics/py/` and the data did not, rather than implying
the repo is finished with. **codex-index-aleppo also keeps its three published pages and its
`pages.yml`**, which no phase of this plan touches.

**Stop and ask Ben before each.**

## Phase 6 — breadcrumbs and issue citations — the execution record — **DONE 2026-08-22**

**One commit, in one repo: `94b824a` in codex-index-aleppo.** codex-index-leningrad and
codex-index-cam1753 had nothing to repoint and got no Phase 6 commit at all.

### The prescribed grep returns nothing in all three, and that is not the answer

`git grep -lI "generated by codex-index" -- .` returns zero files in codex-index-aleppo,
codex-index-leningrad and codex-index-cam1753, which is what Phase 4 predicted for each of the
three. book-of-job's Phase 6 had already established that a zero there settles nothing, and it
settled nothing here either: **the one site this phase found is invisible to that grep, to the
wider `py/…` grep, and to any path-shaped grep whatever.**

The three sweeps that were actually run:

1. **`git grep -nIoE '(^|[^-a-zA-Z0-9/_.])py/[A-Za-z_0-9./]*'`** — the programme's path-shaped
   sweep. 30 hits in codex-index-aleppo, 1 in codex-index-leningrad, 3 in codex-index-cam1753,
   every one of them already repointed by Phase 4 or deliberately historical.
2. **A sweep by module BASENAME over every tracked file, data included.** The 94 modules the
   three repos held before Phase 4 — 50, 21 and 23 — carry **70 distinct basenames**, taken from
   `git ls-tree -r --name-only <phase-4-commit>^`, and every one was swept as a fixed string
   against every tracked file of all three repos. This is the sweep codex-index-cam1753's Phase 4
   found its `cam1753-page-index.json` citation with, and it is the one that paid here too.
3. **Every `.py`-shaped token in every tracked file, resolved against the disk.** 82 distinct
   tokens across the three repos — 42 in codex-index-aleppo, 28 in codex-index-cam1753, 12 in
   codex-index-leningrad — each classified as `../MAM-basics/`-relative, `py/`-rooted,
   repo-relative or bare basename, and each looked up. This is the sweep that turns "a citation
   exists" into "a citation resolves", and it is what isolated the single failure.

### The one site is in a file that documents DATA, which is the second time in two phases

`codex-index-aleppo/aleppo-pages-provenance.md:11` read

```
- **Download script:** `download_aleppo_pages.py`
```

a bare basename, no path, in the file recording where the 24 Aleppo page images came from. That
module left the repo with Phase 4's `078b74d` and is MAM-basics' `py/main_ac_download_pages.py`
now — its own docstring says so, having been rewritten in Phase 3 to give a module-scope script a
`main()`. The line now names that path and records the old one.

**The shape is exactly codex-index-cam1753's `cam1753-page-index.json`**, whose `comment` named
`download_cam1753_spreads.py` and which that repo's Phase 4 repointed to
`../MAM-basics/py/main_cam1753_download_spreads.py`. Two repos, two manuscripts, two download
scripts, and in both the surviving citation sat in a file about the DATA rather than in a file
about the code — which is where a sweep of "tracked prose" does not look, because neither file is
prose about the pipeline. **Sweep every tracked file, not the ones that look like documentation.**

### Everything else resolves, and the historical statements are meant to be there

Of the 82 `.py`-shaped tokens, the ones that do not name a file on disk are all deliberate:
codex-index-aleppo's `CLAUDE.md:75` ("That was `aleppo-wiki/main_make_wikisource_page.py` here
until the move") and `:150`, `:33`; codex-index-leningrad's `CLAUDE.md:33`, `:53` and `:54`;
codex-index-cam1753's `CLAUDE.md:22`, `:26` and `:45` and its `doc/reading-mam-simple.md:27`.
Each states where a file used to be, which is the point of writing it. Phase 4's twenty-six
repointed sites in codex-index-aleppo and twenty-six in codex-index-cam1753 all still resolve.

One token names neither repo's file and is not ours: `mb_cmn_bib_locales.py`, cited in
`codex-index-leningrad/UXLC-utils-sparse/data/lci_recs.json:17`. That tree is vendored from
UXLC-utils and refreshed by MAM-basics' `py/main_lenin_vendor_uxlc.py`, so its contents are
UXLC-utils' business; editing it here would be overwritten by the next sync.

### Issue citations: zero in all three, which makes it three moves running

Every `#`-plus-digit site in the three repos was read. **None is an issue citation.** They are
hex colours in `codex-index-aleppo/aleppo-wiki/precursors/B-J David Stark.htm` and in
`codex-index-cam1753/check_line_breaks.html`; Hebrew wikitext line prefixes in
`aleppo-wiki/Wikisource-manual-final.txt`; and three UXLC **change** numbers inside the vendored
`codex-index-leningrad/UXLC-utils-sparse/in/UXLC-39/*.xml`, which are that data's own numbering.

So the trio's 94 modules owed nothing, after holman-ketiv-qere's 60 owed nothing and
book-of-job's 241 owed nothing. **Three moves running, at 60, 241 and 94 modules, have owed this
repo's "Five issue trackers" section not one prefix** — which is the third confirmation of that
section's own claim that what a move owes is a function of what its code talks about and never of
how many files it is. The trio adds a reason of its own: none of these three repos has a tracker
that MAM-basics' citations could collide with, because none of the code that moved ever cited one.

### The interpreter sweep, per the programme's Phase 7 finding 1

`git grep -nI '\.venv'` in each repo, since holman-ketiv-qere's `doc/` had named its own venv by
absolute path and a `py/`-shaped grep had missed it. **Sixteen lines mention `.venv` across the
three repos** — 6 in codex-index-aleppo, 3 in codex-index-leningrad, 7 in codex-index-cam1753,
`.gitignore` aside — **and fourteen of them already name
`C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe` by absolute path.** The other two
are codex-index-aleppo's `CLAUDE.md:46`, which is historical, and codex-index-cam1753's
`doc/cam1753-line-break-task.md:95`, which warned a reader off that repo's own venv and which
Phase 7 item 5 then made obsolete by deleting it (`7309882` there).

### One figure in `94b824a`'s own message is wrong, and this is the correction

That commit message says "All 43 other `.py` tokens in its tracked files either resolve under
`../MAM-basics/py/` or are deliberate statements about where a file used to be." **The number is
41, not 43**: codex-index-aleppo carries 42 distinct `.py` tokens and this phase repointed one of
them. The 43 was the three-repo figure this record's own first draft also carried, and it was
wrong there too. The message is left as pushed rather than amended; the count that holds is the
one here.

### An instrument note about editing a CRLF worktree file

codex-index-aleppo holds `aleppo-pages-provenance.md` as CRLF on disk against an LF blob, under
`* text=auto eol=lf`. **`sed -i` on such a file strips every CR in it, not just on the line
edited** — the file went from 33 CRLF to 33 LF — and `git diff` still reported one insertion and
one deletion, because the index is LF either way and git normalized on the way in. The commit is
therefore the one-line change it looks like. Worth knowing before reading a whole-file diff in
that repo as evidence of anything.

---

## Phase 6 — breadcrumbs and issue citations — the prescription, left as written 2026-08-02

```powershell
git grep -lI "generated by codex-index" -- .
```

Per repo, in a dedicated commit near the end, and not mid-move.

## Phase 7 — cross-repo bookkeeping — the execution record — **DONE 2026-08-22**

**Items 1–5 are discharged; item 6 found five stale citations and every one is in a third repo,
so all five stop and ask Ben.** One commit here carrying items 1–4 and this record, and
`7309882` in codex-index-cam1753 carrying the half of item 5 that was a tracked file.

### Item 1 — the policy loses three entries and eight rows, and they cannot go separately

`in/vendoring_policy.json` goes from **205 lines to 90**. The `repos` object loses
`codex-index-aleppo`, `codex-index-cam1753` and `codex-index-leningrad` and keeps `MAM-simple`,
`diffable-pointed-hebrew` and `MAM-private`; the `overrides` list goes from ten rows to two.

**The prescription describes the eight override rows wrongly, and the correction matters for
reading the diff.** It says they name "`codex-index-aleppo` and `codex-index-leningrad` paths",
and the Phase 4 records elaborated that the rest name codex-index-aleppo's `py/mb_cmn/` and
codex-index-cam1753's `mb_cmn/`. Measured: the eight are **four naming
`codex-index-aleppo/aleppo-wiki/py/` and four naming `codex-index-leningrad/lenin-wiki/py/`**,
one per file for `hebrew_letters.py`, `hebrew_punctuation.py`, `hebrew_verse_numerals.py` and
`my_utils.py` in each. **No override ever named `py/mb_cmn/` or codex-index-cam1753's `mb_cmn/`**
— those two were `pkg_scan_roots`, discovered by scan rather than declared. That is exactly why
codex-index-cam1753's inventory row vanished the moment its files did, while codex-index-aleppo's
and codex-index-leningrad's `*-wiki/py` rows survived as `MISSING-DEST`: a scanned row exists
only while the files do, and a declared row outlives them.

**The two halves are one edit, not two, and the loader enforces it.**
`vendoring/repo_policy.py:208` rejects an override whose `dest_repo` is not a known repo, so
deleting the three entries while leaving the eight rows raises `dest_repo must name a known repo`
at load — before `--all` gets anywhere near a scan root. The prescription's warning that
`main_vendoring.py --all` raises on a missing scan root is true and is the *second* way a
half-done edit fails; this is the first.

`py/main_vendoring.py --all` then rewrote the three tracked artifacts: **`doc/vendoring-inventory.md`
18 rows/112 files → 12 rows/97 files**, and `out/vendoring_compare_out.txt` 105 rows → 97. No
`codex-index` string survives in any of the four generated files.

### The tracked artifacts were ALREADY stale, and running the audit before editing is what showed it

Run at `ea1f035` with the policy untouched, `--all` produced **14 rows/105 files** against the
18/112 the tree held. So the trio's three Phase 4 commits — `824910e`, `078b74d` and `a9c3abd` —
deleted the files those rows describe and left the audit unregenerated, and nothing ran it in the
interval. **That the drift shows up at all is the design working**: `main_vendoring.py`'s own
docstring says the audit was made a step of `py/main_0_mega.py` precisely so a stale inventory
surfaces as an ordinary unexplained diff. **What it also shows is that the mega had not been run
since**, which is the sort of thing only a regeneration-before-editing tells you. Running the
generator before touching its input, and reading the numbers rather than the exit code, is what
separated "Phase 4 left this stale" from "Phase 7 changed this".

### The stale regeneration surfaced something that is NOT the trio's bookkeeping

Two rows moved for a reason nothing in this plan predicted: **MAM-private's two vendored copies of
`mb_cmn/vendoring_sync.py` now read `DIFFERS` where they read `identical`** —
`mgketer/py/mb_cmn/vendoring_sync.py` and `al-hatorah/py/mb_cmn/vendoring_sync.py`. The cause is
this plan's own Phase 3: **`10ae4d5`** is the last commit to touch MAM-basics'
`py/mb_cmn/vendoring_sync.py`, and it is "Phase 3 for codex-index-leningrad: land the wiki
pipeline, dissolve eleven copies", which dissolved that repo's two-line fork into a `basename`
parameter. Dissolving a fork in this repo put a *private* repo's two copies out of date, and
nobody would have known until an audit ran.

**Not fixed here.** MAM-private is not written to without Ben's say-so, and the fix is a
re-vendor rather than a bookkeeping edit — `mgketer/py/main_update_vendored_files.py` and
`al-hatorah/py/main_update_vendored_files.py` are the scripts that would do it. Reported.

### The test loses five cases, and the rule predicts exactly which five

`py/tests/test_vendoring_policy_paths.py` derives all three of its parametrize lists from the
policy: one case per `source_pkg_dirs` entry, one per non-ignored dest repo, one per scan root.
Before: 7 + 6 + 10 = **23**. After: 7 + 3 + 8 = **18**. The three lost dest-repo cases are the
three deleted entries; the two lost scan-root cases are `codex-index-aleppo` `py/mb_cmn` and
`codex-index-cam1753` `mb_cmn`, codex-index-leningrad having declared `pkg_scan_roots: {}` and so
having contributed none all along. **Counting scan roots rather than repos is what makes the
prediction come out**, which is why this plan said to count them.

### The policy edit has to come BEFORE item 5, and both orders end in the same place

Once item 5 deletes `codex-index-aleppo/py/` and `codex-index-cam1753/mb_cmn/` from disk, a
policy still naming them raises `Configured scan root does not exist` on every `--all` run and
fails two cases of the lint. Doing item 1 first means the audit works throughout; doing item 5
first means it is broken for as long as the two are out of step. **Nothing in the prescription
puts the six items in an order**, and five of the six are order-free; this is the one pair that
is not.

### Item 2 — reworded, and its home was not where either instruction expected

The prescription said **delete** the codex-index-leningrad comment with the script it describes.
codex-index-leningrad's Phase 4 record overrode that: **reword**, because the sync it describes
still happens. Both assumed the comment would still have a repo entry to sit on — and item 1
deletes that entry, so there is no comment left to reword. **The two instructions were written
against different assumptions about item 1 than item 1 turned out to have.**

The surviving home is the policy's **top-level `comment`**, which already named
codex-index-leningrad in its account of why mechanism is declared and never detected — "would
have asserted it wrongly for codex-index-leningrad, whose script copies from UXLC-utils rather
than from here". That clause now says: the script is `main_update_vendored_files.py`, it is gone,
Phase 4 emptied that repo of Python on 2026-08-22, no provenance scan finds a copy script there
any more, **the sync it did still happens from MAM-basics' `py/main_lenin_vendor_uxlc.py`**, it
is still not a MAM-basics-to-there vendoring and so is still nothing this manifest describes, and
all three codex-index repos left the `repos` object and the `overrides` list the same day.

**A second home for the same fact exists and the plan never named it**:
`UXLC-utils/shared-with-codex-index-leningrad.md` tells its reader that the sparse copy "should
be refreshed by running that repo's `main_update_vendored_files.py` script". Third repo — item 6
below carries it to Ben.

### Item 3 — all three still listed, confirmed rather than assumed

`all-repos.code-workspace` lines 10, 13 and 16 name `../codex-index-aleppo`,
`../codex-index-cam1753` and `../codex-index-leningrad`. Left exactly as they are: each repo
keeps its tracked non-Python files, and with all three per-repo `.code-workspace` files now
deleted on Ben's decision of 2026-08-22 — as book-of-job's was — **this file is the only thing
that opens the three together.**

### Item 4 — both sweeps skip all three, and the black gate is confirmed by measuring it twice

`run_black.py` reports, for each of the three,
`BLACK_ATTEMPTED=False; BLACK_OK=False; Skipped: no tracked .py files in this repo`.
**Measured twice on purpose: once with the three venvs still present and once after item 5 had
deleted them, with byte-identical output.** That is `_has_tracked_py_files` being asked before
black is looked for, which is what book-of-job's 1,722 untracked `.py` settled, demonstrated here
from the other side — a repo with no venv at all skips by the same route as one with a full venv.

`check_repo_standards.py` reports `MAINTENANCE_SCRIPT=n/a; WORKTREE_STEP=n/a; PATH_UTILITY=n/a;
ROOT_CONFTEST=False; SHIM_CONFIG=None; SYS_PATH_MUTATIONS=0; SYS_PATH_IN_TESTS=0` for all three,
with `py_file_count_scanned: 0` — every Python-shaped check correctly inapplicable rather than
vacuously passing.

**One nonzero in that line is worth reading rather than passing over.** codex-index-leningrad
reports `NFC_H_DOT=1; NFC_LATIN=1` where the other two report 0, over 50 text files scanned. The
finding is a single site, `UXLC-utils-sparse/in/UXLC-39/Psalms.xml:758` — vendored UXLC-utils
data, pre-existing, and outside the 8-file scope `py/tests/test_h_dot_below_nfc.py` gives that
repo, which is why the suite passes while this scan does not report zero. The cross-repo scan is
deliberately the wider of the two instruments, as its own docstring says; the per-repo test is
the authoritative one. Nothing to fix here, and nothing that this phase changed.

### Item 5 — 328 MB, fifteen `__pycache__` directories, and nine emptied trees

`--clean-worktrees` first, per the memory note that hand-running `git status` in a worktree makes
that sweep skip it: **"worktrees: nothing to clean" in all three**, consistent with
`check_repo_standards`' `LINKED_WORKTREES=0; AGENT_BRANCHES=0` for each.

**All three `.venv` are real directories — no junction, no symlink**, checked with a POSIX
`-L` test and with `dir /AL`, which reported "File Not Found" for reparse points in each. So the
2026-08-03 `masorah-books` hazard, where `git worktree remove` followed a junction and emptied a
shared venv, does not arise. Sizes: codex-index-aleppo **153 MB**, codex-index-cam1753 **153 MB**
(both with matplotlib, Pillow and fontTools), codex-index-leningrad **22 MB** (black and pip
only). All three had black and none had pytest.

Also deleted, all gitignored and invisible to `git status`: **fifteen `__pycache__` directories**
— 7 under codex-index-aleppo, 4 under codex-index-leningrad, 4 under codex-index-cam1753 — and
the nine now-empty trees holding them: `py/`, `py/mb_cmn/`, `py/py_ac_loc/`,
`py/py_ac_word_image_helper/` and `aleppo-wiki/py/` in codex-index-aleppo; `py/` and
`lenin-wiki/py/` in codex-index-leningrad; `mb_cmn/`, `py_cam1753_word_image/` and `py_mam_xml/`
in codex-index-cam1753. **Each was checked to hold nothing but `__pycache__` before deletion** —
`aleppo-wiki/` and `lenin-wiki/` themselves hold 15 and 3 tracked data files and stay. After it,
**not a `py`-shaped directory remains in any of the three**, and all three trees are clean.

The prescribed grep for anything naming a venv about to be deleted found **exactly two sites**:
codex-index-cam1753's `doc/cam1753-line-break-task.md:95`, fixed in that repo as `7309882`, and
`MAM-private/mgketer/CLAUDE.md:297`, which is item 6's business.

### Item 6 — swept all 26 clones, by path AND by repo name, and by name is what found four of five

Twenty in `~/GitRepos` and six in `~/FrozenRepos`. **Eighteen of the twenty-two other clones
mention `codex-index` nowhere at all**, including every one of the six frozen. Four public clones
and MAM-private do, at 3, 2, 2, 1 and 11 files.

**Five citations are genuinely stale, and all five are in a third repo**, so each stops and asks
Ben rather than being fixed here:

| Repo | Site | What it says now | What is true |
|---|---|---|---|
| holman-ketiv-qere | `CLAUDE.md:91-104` | `cd C:\Users\BenDe\GitRepos\codex-index-aleppo` then `.venv/Scripts/python.exe py/main_find_word_in_aleppo_images.py`, under "run each with its own repo's interpreter" | `MAM-basics\.venv\Scripts\python.exe … py\main_ac_find_word_in_images.py`, from anywhere. The Leningrad half of the same section, `:107-112`, was already corrected when UXLC-utils' Python moved |
| book-of-job | `doc/reading-mam-simple.md:28` | "The repos that do read this XML are codex-index-aleppo and codex-index-cam1753, each with a separate `mam_xml_verses.py`" | Neither repo holds code, and the two `mam_xml_verses.py` are one file — `py/py_ac_loc/mam_xml_verses.py` here — since this plan's Phase 3 for codex-index-cam1753 |
| UXLC-utils | `shared-with-codex-index-leningrad.md:5-6` | the sparse copy "should be refreshed by running that repo's `main_update_vendored_files.py` script" | `MAM-basics/py/main_lenin_vendor_uxlc.py`. This is Phase 7 item 2's fact, in a place item 2 never looked |
| MAM-private | `mgketer/CLAUDE.md:294-297` | `PYTHONUTF8=1 ../codex-index-aleppo/.venv/Scripts/python.exe ../codex-index-aleppo/py/main_find_word_in_aleppo_images.py` | Both the venv and the script are gone; `MAM-basics/py/main_ac_find_word_in_images.py` |
| MAM-private | `mgketer/CLAUDE.md:347-371` | `cd ../codex-index-leningrad/UXLC-utils-sparse && … main_uxlc_estimate_atom_loc.py` | `MAM-basics/py/main_uxlc_estimate_atom_loc.py`. **Stale since 2026-08-03**, when UXLC-utils' Phase 5 dropped `UXLC-utils-sparse/py` — this programme did not break it and had not caught it either |

**A sixth site belongs to the fourth row rather than to a row of its own**:
`mgketer/py/main_crop_from_export.py:11`'s docstring also cites
`codex-index-aleppo/py/main_find_word_in_aleppo_images.py`. So the mgketer repointing, if Ben
wants it, is two files — `mgketer/CLAUDE.md` and that module — and it is the only one of the five
that would touch code rather than prose.

**The name sweep is what found four of the five.** `holman-ketiv-qere/CLAUDE.md:100` is a bare
`cd` to the repo with the script on a separate line; `book-of-job/doc/reading-mam-simple.md:28`
names the two repos with no path in the sentence at all; `UXLC-utils`' site names a script with
no path. A `codex-index-*/py` grep reaches only the two mgketer sites. **book-of-job's Phase 7
found three of five stale citations only by name, and this phase found four of five that way** —
the same lesson twice, at nearly the same ratio.

**Checked and deliberately left alone**, because each is about DATA, which these three repos
still host: `mgketer/py/py_ac_word_image_helper/codex_page.py:14` and `flat_index.py:16`, both
resolving `MGKETER_ROOT.parent.parent / "codex-index-aleppo"` for page images and
`index-flat-annotated.json`; `mgketer/documentation/codex-index-aleppo-provenance.md`, which
records a data copy and its source commit; `MAM-private/py/tests/test_h_dot_below_nfc.py`'s
`"codex-index/"` exclusion, naming mgketer's in-tree snapshot; the fifteen lines in
`UXLC-utils/doc/clc-design.md`, every one about codex-index-leningrad as a data sibling; and
`github-misc`'s two, which are the tracked copy of `~/.claude/CLAUDE.md` and the `hebrew-prose`
skill's repo list. `MAM-private/doc/PLAN-evacuate-private-repos.md`'s twenty-seven lines are
that plan's execution record and are left as written, on the same principle as this plan's own
retired-section-name citations.

**One stale citation found that this programme did not cause and does not own**:
`book-of-job/py_ac_loc/codex-index/codex-index-provenance.md` names the source repo
`bdenckla/codex-index` and a local path `..\..\GitRepos\codex-index\aleppo\index-flat.json`. That
repo went in the 2026-03-28 rename this plan's Phase 1 met twice as the cause of two dead
generators. Reported with the five above.

### Verification

- **Suite `.venv\Scripts\python.exe py\main_test.py -q`: 940 passed, 5 skipped, 59 subtests**, in
  103s. The 945 of the baseline less the five vendoring-lint cases item 1 removed, and no other
  test moved. The `59 subtests` figure reproduces for the sixth measurement running.
- **`py/check_all.py`: all 7 checks passed, mark order over 509 files, escapes over 297 `.py`.**
- **The oracles, all run AFTER item 5 deleted the three venvs**, which is the order that proves
  the deletions took nothing the code needed: codex-index-aleppo **4 of 4** byte-identical
  (`main_ac_wikisource_page.py`'s three under `aleppo-wiki/` plus
  `main_ac_gen_index_flat_annotated.py`'s `index-flat-annotated.json`); codex-index-leningrad
  **3 of 3**; codex-index-cam1753 **44 of 44**, with `check_cam1753_all.py` passing **4 of 4** and
  its mark-order check reading 509 files too.
- **Whole-repo comparison against HEAD blobs, EOL-normalized, in all three.** codex-index-aleppo:
  54 byte-identical, **121 EOL-only, 0 real drift** — the latent-CRLF condition, now 121 of 175
  where Phase 1 measured 152 of 222. codex-index-leningrad: **51 of 51 byte-identical**, 0
  EOL-only, confirming Phase 1's finding that this repo has none. codex-index-cam1753: 151
  byte-identical and **one real difference, `doc/cam1753-line-break-task.md`, which is this
  phase's own commit**.
- All four repos clean and pushed at the end; every push fast-forward, none forced.

### `check_all.py` reads 509 files, not 510, and Ben's third orphan decision is why

The task that ran this phase carried **510 files and 297 `.py`** as the baseline, measured at the
close of codex-index-cam1753's Phase 4. The figure now is **509 and 297**, and the missing file is
`codex-index-aleppo/.claude/settings.json`, deleted by **`3003a06`** — the third of the three
orphan decisions Ben settled that day.

**A `.claude/settings.json` was inside a lint's scope, which nobody had noticed.**
`check_mark_order`'s `_corpus_json_files()` walks each entry of `repo_scopes.corpus_roots()` for
`*.json`, skipping only `.venv`, `__pycache__`, `.novc`, `.git` and `node_modules` — so every
`.json` anywhere under codex-index-aleppo counted, repo furniture included. The deletion was
decided on grounds the evacuation knew nothing about, that the file predated "auto" permissions,
and it moved a lint's file count as a side effect. **The effect cannot recur in scope**: of the
three corpus roots, book-of-job and codex-index-cam1753 have no `.claude/` at all, and
codex-index-aleppo no longer has one.

This is the third time in this programme that re-measuring a quoted figure rather than trusting it
produced a finding, and the first where the cause was a decision taken outside the plan entirely.

### A second session was live in MAM-basics, and did not collide

It had landed `2d36dbe` and `ea1f035` before this phase started, so the uncommitted
`CLAUDE.md`, `doc/PLAN-evacuate-python-from-holman-ketiv-qere.md` and
`doc/PLAN-evacuate-python-programme.md` edits the task warned of were already committed and the
tree was clean. The three checks that prove non-collision, per the memory note that transcript
byte counts are the wrong instrument: **`HEAD` was `ea1f035` at the start and `ea1f035`
immediately before this phase's commit**; `git status --porcelain` was empty at the start and
held only this phase's own five paths before staging; and the push landed fast-forward with no
`--force`. Every file was staged by explicit path.

**`doc/PLAN-evacuate-python-programme.md` is written in this commit**, its trio Status row having
been left unwritten by both Phase 4 records for exactly this reason. That file is no longer held
by another session, so the row that describes Phases 0, 1, 3, 4, 6 and 7 is landed here — the
last thing the programme owed the trio.

---

## Phase 7 — cross-repo bookkeeping — the prescription, left as written 2026-08-02

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
