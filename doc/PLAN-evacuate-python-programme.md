# Evacuating Python from the remaining public repos — the programme

Written 2026-08-02, immediately after `doc/PLAN-evacuate-python-from-wlc-utils.md` finished. That
plan is the model and the precedent; this file is the umbrella over the public repos that still
hold Python — **eight hold it, six are in scope** — and it owns the three things no single repo's
plan can own: the scope, the order, and the work that must happen **before** any repo moves.

## Status

| Repo | Plan | State |
|---|---|---|
| Programme Phase 0 — reconcile the three drifted `check_*`/`fix_*` forks | this file | **DONE 2026-08-19 — all three steps.** 0a classified all sixteen files and hit the plan's own gate with category (iii) differences in two of the six scripts; **Ben's decision the same day was to reconcile the six that are one tool with drift and leave `check_all.py` and `check_word_finding.py` per-repo permanently**, the first being each repo's register of which checks it runs and the second a per-manuscript verifier. 0b: `33b3ee2` in book-of-job (5 files), `98021de` in codex-index-aleppo (9) and `f56831c` in codex-index-cam1753 (4). 0c holds — **fourteen of the sixteen are one committed blob**. **Four of the sixteen were never forked**: the `py_cam1753_word_image/` files were already one blob, and the table's "all four differ" was `cmp` reading book-of-job's stale CRLF working tree, so **compare committed blobs, not working trees**. **book-of-job's copies were canonical because its two apparent eccentricities were both load-bearing** — `_RANGE_RE` carries `mb_cmn/hebrew_points.py:33` and U+2003 carries `pyauthor/job1_full_list_details.py:41` — so **the cluttered fork was the correct one**; 0a had called `_RANGE_RE` dead on a grep that silently matched nothing, and seeing it was live is what let 0b delete `_SKIP_PREFIXES` outright instead of parameterizing it. The one edit to the canonical text is a `repo_root()` walking up to `.git`, replacing a `Path(__file__).resolve().parent` that meant the repo root in two repos and `py/` in the third: codex-index-aleppo's mark-order check went from 33 files to **128**, reading the 84 tracked `.json` it had never seen, with **zero** new violations, and that repo now passes both checks for the first time. Three findings for steps 4 and 5: **no repo's `check_all.py` runs in its own venv** (Pillow missing in all three, pyspellchecker in book-of-job), all pre-existing; **book-of-job has none of the six data directories its two word-image packages need**, so it holds 10 files of dead code; and the two word-image packages are partly forked from **each other** inside book-of-job |
| UXLC-utils | [PLAN-evacuate-python-from-UXLC-utils.md](PLAN-evacuate-python-from-UXLC-utils.md) | **DONE 2026-08-18 — all seven phases.** Phase 1 2026-08-02: `fe73d07` there, `d5a5052` here; Phase 3 2026-08-02: `662db55` and `f202d21` here, nothing there; Phase 4 2026-08-03: `ad52001` there, `2b5c87c` here; Phase 5 2026-08-03: `d5195e3` in codex-index-leningrad, `748ee2f` there, nothing in this repo's `py/`; Phase 6 2026-08-18: `30cdfd2` here, `9be1431` there; Phase 7 items 2–5 2026-08-18, no commit owed. **UXLC-utils holds zero Python** and its 214 artifacts still regenerate byte-identically from here — 213 of them untouched by Phase 6, the one that moved being `gh-pages/fois/index.html`'s breadcrumb, which now names MAM-basics. **Phase 5 dropped codex-index-leningrad's sparse `py/` half rather than repointing it** — the shared decision with the codex-index trio, written into that plan too. Phase 6 prefixed **50 of 57** bare `#NN` citations with `UXLC-utils#` and left 7 bare, so `CLAUDE.md`'s section is now "Three issue trackers"; Phase 7 item 4 deleted a 33 MB orphaned venv holding **832 `.py`**, the shape wlc-utils' Phase 7 warned of at 789. **Item 6 was done earlier, 2026-08-17, github-misc `549224e`.** This row said "Only Phase 6 remains" until the 2026-08-03 review ([#219](https://github.com/bdenckla/MAM-basics/issues/219), major 4) caught the overstatement; corrected 2026-08-04 |
| holman-ketiv-qere | [PLAN-evacuate-python-from-holman-ketiv-qere.md](PLAN-evacuate-python-from-holman-ketiv-qere.md) | **DONE 2026-08-19 — every phase.** Phases 1, 3, 4 and 6 plus Phase 7 item 1 all landed 2026-08-18; Phase 7 items 2–5 on 2026-08-19. Phase 2 does not recur here and Phase 5 has no analogue, so the plan is complete at five phases. **holman-ketiv-qere holds zero Python** and its 335 artifacts still regenerate from here, 175 rewritten and 160 untouched, `row_count` 77. Phase 7: items 2 and 3 confirmed, item 3's two strings coming back verbatim as UXLC-utils' had; item 4 deleted a **22 MB** venv — black and no pytest, smaller than wlc-utils' 789-`.py` and UXLC-utils' 832-`.py`/33 MB shapes — after `--clean-worktrees` ran first and found nothing, and after a junction check that reported a plain `Directory`. **Three findings, and unlike UXLC-utils' Phase 7 this one needed a commit** — a one-line commit in holman-ketiv-qere, `6b0bb63` there. **Finding 1: item 4's safety check failed on one tracked site.** `doc/holman-manuscript-citations.md`'s closing line named holman-ketiv-qere's **own** venv by absolute path, an instruction pointing at the directory the phase was about to delete; Phase 4 had rewritten all three `py/…` module paths in that very file, so it was missed rather than spared, and the reason is that **a `.venv` path carries no `py/` prefix and so is invisible to the `py/[A-Za-z_./]*` grep Phases 4 and 6 both swept with** — the same blind spot Phase 6 recorded for `hkq_cmn/uxlc_standard_atoms`. **Grep for the interpreter as well as for the code paths** at book-of-job and the trio. Two descriptive `.venv` sentences in holman-ketiv-qere's `CLAUDE.md` were left, UXLC-utils' `CLAUDE.md` carrying the identical one and its Phase 7 having left that. **Finding 2, left for Ben: a stale cross-reference in a third repo, which no repo's tooling can see.** MAM-private's `mgketer/documentation/mpu-parsing.md` (lines 9–10) and its generated `mgketer/out-reports/mpu-parsing.html` (lines 21–22) cite `holman-ketiv-qere/py/python_modules/mam_plus_verse_data.py` and `…/qere_projection.py` under an explicit "check for matching logic to propagate" heading — **stale twice over**, holman-ketiv-qere holding no Python and `python_modules/` having been renamed `hkq_cmn/`; the live targets are `MAM-basics/py/hkq_cmn/`. Not fixed, on the item-6 precedent that a commit to a third repo stops and asks. **This is cross-cutting finding 2 in a new shape** — a documentation cross-reference rather than a vendored copy — so **run item 5's grep against MAM-private** at the remaining repos, which the earlier plans had no reason to. **Finding 3 corrects a figure these plans have been carrying**: the `59 subtests` recorded by holman-ketiv-qere's Phases 3, 4 and 6 does **not** reproduce — `pytest-subtests` is not installed in `.venv`, so pytest cannot report it and the word appears nowhere in the output. The passed and skipped counts match exactly, so **drop the third figure** and record the suite as **947 passed / 5 skipped**; re-measure rather than copying a figure whose instrument is not in the venv. Phase 6: `4e9d809` here (the generator), `ce6dd7d` there (three artifacts), plus a `CLAUDE.md` commit. The five stale `py/…` paths flipped in **two shapes, which the artifacts themselves settled** — a bare `MAM-basics/py/…` in the two generated `note` fields, matching the one pre-existing `MAM-basics'` in the very file being edited, and `../MAM-basics/py/…` in the hand-authored `table_data_fields.md`, matching the README and `CLAUDE.md` Phase 4 had rewritten that way the same day; **ask which neighbourhood a breadcrumb sits in rather than picking one shape per repo.** **Not one bare `#NN` needed prefixing** — every `#NN` holman-ketiv-qere's Python ever carried is a CSS hex colour, a UXLC change anchor, a Yeivin *ITM* section number, or an issue of **MAM-basics'** own, so 60 files moved and none cited the tracker whose name would have been the prefix: **the citation count is not a function of the file count, so measure it before budgeting for it.** `CLAUDE.md` is now **"Four issue trackers"** — 81 issues, numbered 1–81, 60 open, the **whole** range colliding, and six numbers it already cited are now four-way. holman-ketiv-qere is also the one repo of the four needing **no `doc/` exception**, its two `doc/` files carrying no bare `#NN` at all. The `22` bare citations named in that phase's task prompt have **no source in either plan** and match no measurement. Phase 4: `0890cb8` there (111 files, +121/−16,838) and `b72f785` here — **holman-ketiv-qere holds zero Python**, and its 335 artifacts still regenerate byte-identically from here, 175 rewritten and 160 untouched on both the before and after runs, row count still 77. **The tracked deletion was 107 files, not 104**: five `_provenance.md` rather than four, the fifth being `py/_provenance.md` for the loose `py/uxlc_paths.py` and invisible to the inventory for the same reason that file is; plus `py/.gitignore`, plus `.vscode/settings.json`, which Ben agreed as an extra. **`git ls-files py \| grep -v '\.py$'` before quoting a deletion size** in book-of-job and the trio. **Phase 7 item 1 landed inside Phase 4**, the scan-root guard failing twice in the phase's own verification run — UXLC-utils' Phase 4 predicted exactly that for every remaining plan, and it now has two instances. The suite moves 950 → **947**, three tests not two: `test_vendoring_policy_paths.py` derives every parametrize list from the policy, so a dropped entry costs a dest-repo case besides its scan-root cases, the same 3 UXLC-utils lost — **predict three per repo**. The README's commands were **nine, not six**, the extra three being `main_test.py`, an entry point that disappears rather than moving, so its Tests section could not be repointed by prefix. **Ben chose to rewrite every `py/…` path** in that README and in holman's `doc/`, against the state-one-substitution answer he gave for UXLC-utils' `doc/` — not a reversal, since here the package was renamed to `hkq_cmn/` and two more trees were pure deletions, so no single stated rule covers the cases; **ask per repo**. One baseline had moved again and it was Phase 3's own effect: 16,637 lines rather than 16,640, `9e290ce` having netted −3 after the figure was taken. Phases 1 and 3, for the record: Phase 1: `6b10259` there, preceded by `50b2eaa` there (a nine-day-stale artifact, committed first and alone); nothing owed in this repo's `py/`, `mb_cmn/paths.py` already being vendored there and identical, so Phase 2 genuinely does not recur. Phase 3: `1be01b5` here, 60 new files under `py/` plus a modified `py/tests/test_h_dot_below_nfc.py`, with `9e290ce` and `15824d4` in holman-ketiv-qere either side of it — the ruff and UTF-8 preconditions before, the one artifact the `python_modules`→`hkq_cmn` rename reaches after, both deliberate exceptions to "nothing is committed there". **61 files move and only 60 land**, the NFC guard being a third `_Scope` rather than a copy; that scope also needed `.docx` added to `_BINARY_EXTENSIONS`, which holman's copy listed and this repo's did not, so **diff the binary-extension sets as well as the exclusions at every remaining repo carrying that guard**. Suite 905/5 → **950/5**, up by the 45 the seven copied modules collect; 175 of the 335 artifacts rewritten and 160 untouched, matching Phase 1 exactly; row count still 77. **The source-lint crop was 3, not UXLC-utils' 68** — holman's prose is about ketiv/qere rather than accentuation, so budget that cost by subject matter and expect book-of-job and the trio to behave like UXLC-utils instead. **Three of the seven moving entry points had no `sys.stdout.reconfigure` at all**, so UXLC-utils' "the hazard did not materialize" was a fact about that repo's `CLAUDE.md` rather than about the recipe. **Every baseline had moved** — 99 tracked `.py` not 68, 16,416 lines not 11,159, 300 `gh-pages` not 161, 9 entry points not 6, and the oracle is **335 artifacts, not 163**, of which only 175 are rewritten by a full regeneration. A whole second body of work had arrived: Holman's suggested UXLC corrections, extracted from his emails. **The hand-off from UXLC-utils' Phase 7 item 5 was wider than reported** — `py/uxlc_paths.py` is byte-identical and inventory-invisible as described, but so are the packages `py/uxlc_lci/` (4 files) and `py/uxlc_misc/` (5), all five trees named in that repo's `_VENDORED_PACKAGES`/`_VENDORED_FILES`: the pure deletions are **37, not 26**. Four corrections to the plan's own premises, all in its Phase 1 record: the fault was root **conflation** (six `parents[1]` walks) rather than cwd-relative literals, which is the shape to expect in the remaining repos; holman **has** a tracked `CLAUDE.md`, so Phase 4 edits rather than writes one; `py/tests/test_h_dot_below_nfc.py` collides here and differs, wanting a third `_Scope` rather than a copy; and holman brings **13 ruff findings**, a Phase 3 precondition this plan has no Phase 0 for. Phase 3's GitHub question is answered — `gh --repo` is named outright — and exercising that path found a live decomposed-ḥet label defect, left for Ben |
| book-of-job | [PLAN-evacuate-python-from-book-of-job.md](PLAN-evacuate-python-from-book-of-job.md) | **DONE 2026-08-22 — every phase, and this plan is COMPLETE.** Phases 0, 1 and 3 landed 2026-08-19, Phase 4 on 2026-08-21, Phases 6 and 7 on 2026-08-22; Phase 2 does not recur here and Phase 5 has no analogue, so the plan is complete at six phases plus Decision D. **Phase 7 landed as one commit here and nothing in book-of-job**, the second of the four Phase 7 runs to owe its data repo no commit. **Item 2's string survives and the plan's own attribution of it was what was stale**: `main_map_changes_to_book_of_job.py` has been this repo's since 2026-08-03, not UXLC-utils', and its `html_base` is a label `write_mapping()` writes into the output dict rather than a path anything opens — the real route to that sibling being `uxlc_paths.require_book_of_job_dir()`, and the label reaching a tracked artifact in UXLC-utils. **Item 3's strings came back verbatim for the third repo running.** **Item 4's zero-`.py` case had been decided in advance by a fix made for exactly this shape**: `run_black.py` asks `_has_tracked_py_files` *before* looking for black, an ordering changed 2026-08-02 because wlc-utils' leftover venv had just been reformatted — and book-of-job was that same shape at more than double the size, **1,722 untracked `.py` inside its venv** against wlc-utils' 789 and UXLC-utils' 832, every one skipped. **Item 5 deleted the 153 MB venv** after `--clean-worktrees` reported nothing to clean across all 20 repos, after the three safety greps came back as Phase 6 measured them, and after a junction check reporting a plain `Directory` with its own `pyvenv.cfg`. **book-of-job's `CLAUDE.md` needed no edit for the opposite reason from the other two repos'** — theirs describe a venv now gone, while line 19's "there is no `.venv` here to run it with" was *false about the disk* and the deletion makes it true. **Item 6 is the finding for the trio: five stale citations, and the grep shape the two earlier plans prescribe would have found one.** book-of-job's Python sat at the **repo root**, so `book-of-job/py` matches almost nothing that moved, and three of the five name a bare module filename leaving the repo to the surrounding prose, which no path-shaped grep sees anywhere. **Grep for the repo's NAME across all 26 clones and classify by hand.** Three sit in MAM-private and are reported, not fixed, on the standing precedent that a commit to a third repo stops and asks: `mgketer/documentation/periodic-maintenance.md` lines 137–152, a "Checks ported from book-of-job (TBD)" section naming a `check_all.py` harness and five `check_*.py` that are all this repo's now — **finding 2 recurring in the same shape in the same `mgketer/documentation/` tree it was first found in**; `masorah-books/doc/migration-checklist.md:152`'s `../book-of-job/pyauthor_qr/qr_1413.py`, whose "do not rename this, it carries a published link" point survives and only whose path is wrong; and mgketer's diverged third copy of `alef_bet_to_ascii.py`. **The fourth is ONE BLOB across two public repos** — `py/py_ac_word_image_helper/alef_bet_to_ascii.py:5` here and codex-index-aleppo's byte-identical copy, both citing "book-of-job `author.py`" — so it is **handed to the trio plan** rather than forked by an edit to one side, the family being the one programme Phase 0 reconciled; this repo's copy misattributes to a sibling a file this repo holds. The fifth is `UXLC-utils/doc/clc-design.md:824`'s "many check scripts". **github-misc and the skills are nil, unlike UXLC-utils' item 6**: book-of-job's one mention in each copy of the skill tree is `hebrew-prose/SKILL.md`'s repo list, still correct, and no module of book-of-job's was ever cited there. **The `59 subtests` figure reproduced a fourth time**, closing the argument three phases across two plans had run back and forth: it comes from `unittest`'s native `self.subTest` in six `py/tests/` modules, not from the absent `pytest-subtests`, so **the standing baseline is `945 passed, 5 skipped, 59 subtests`** and the sentence further down this row setting it at `947 passed, 5 skipped` with no third figure is Phase 1's superseded reading. Oracle silent with no `fline mismatch`, all 701 artifacts **700 byte-identical / 1 line-ending-only / 0 different** both before the deletion and after it, `check_all.py` 7 of 7. **The `parents[2]` question is STILL open and Phase 7 did not pick it either** — five phases have now put it to Ben. **Phase 6 landed as `8293ce8` here and NOTHING in book-of-job** — the first of the programme's three Phase 6 runs to owe its data repo nothing, UXLC-utils' having moved one artifact and holman-ketiv-qere's three. Both halves of its prescription were nil, as Phase 4 predicted: **both breadcrumb greps return 0**, no code in that repo ever having passed `generator_file` to `mb_cmn.file_io`, so no artifact carries an `mb_cmn.provenance` breadcrumb — which is also why `provenance.py`'s wrong `parents[2]` was latent there. **Not one of the 29 `#NN` sites in the 268 pre-move `.py` needed a prefix**: 24 lines of CSS hex colours (46 tokens) in the two crop-editor generators, 4 Yeivin *ITM* section numbers in the `mb_cmn/hebrew_accents.py` copy Phase 4 deleted, and one already written out as `bdenckla/wlc-utils#43`. **So holman-ketiv-qere's rule has its second confirming case at four times the size** — 241 modules moved and owed one clause, where 60 did: **how many citations a move owes is a function of what its code talks about, never of how many files it is**; budget it by subject matter, and expect the trio to behave the same way. book-of-job owes even less than holman-ketiv-qere did, in two places Phase 1 had already decided: its `mb_cmn/` held **no `paths.py`**, and its `test_h_dot_below_nfc.py` cites nothing. What the phase DID owe is a section neither plan wrote down: **`CLAUDE.md` is now "Five issue trackers"** — book-of-job keeps **61 issues, 1–61 with no gaps, 19 open**, measured 2026-08-22, and **four of the six four-way collisions become five-way** (#19, #29, #48, #52), #69 and #75 staying four-way since that numbering stops at 61. Eight `CLAUDE.md` edits, three of them corrections rather than extensions: holman-ketiv-qere's "Unlike the other three moves, this one had nothing to prefix" was a uniqueness claim book-of-job falsifies, its "the one place it differs from the other three" was another, and the wlc-utils paragraph's "the one standing exception" was already contradicted by the UXLC-utils paragraph below it. **book-of-job needs no `doc/` exception and goes further than holman-ketiv-qere**: `#NN` appears nowhere in any of its **784** tracked files, artifacts included, so **the four evacuated repos now split two and two** — wlc-utils' and UXLC-utils' `doc/` trees are the two standing exceptions, holman-ketiv-qere and book-of-job need none. **Two findings for the trio, both from sweeps the prescription does not ask for.** First, **a zero from the breadcrumb grep is not the answer** — holman-ketiv-qere's Phase 6 proved that, so both of its wider sweeps were run here: `git grep -nIoE '(^\|[^-a-zA-Z0-9/])py/[A-Za-z_./]*'` returns **17 hits in 2 files and every one is correct**, because Phase 4 declared the working directory once at the top of `CLAUDE.md` and left the paths bare under it — **a third breadcrumb shape**, alongside the bare `MAM-basics/py/…` and `../MAM-basics/py/…` holman's phase recorded. Second, **the interpreter sweep the programme's Phase 7 finding 1 added comes back clean**: 4 `.venv` hits and not one names book-of-job's own venv, so **Phase 7 item 5 can delete that 153 MB venv — the largest of the four, against UXLC-utils' 33 MB and holman-ketiv-qere's 22 MB — with no documentation edit owed**, unlike holman-ketiv-qere, whose `doc/` named its own venv by absolute path. Verification is confirmation rather than verification, the phase having touched no code, and was run anyway: oracle silent with no `fline mismatch`, all 701 artifacts **700 byte-identical / 1 line-ending-only / 0 different** before and after, suite **945 passed / 5 skipped / 59 subtests**, `check_all.py` 7 of 7. **The `parents[2]` question is still open and this phase did not pick it either** — moot for book-of-job since Phase 4, live only for MAM-basics' copy and the other repos that hold it. **Phase 4 landed as `a846585` there (320 files: 317 deletions, 3 modified) and `cff95f7` here (14 files) — book-of-job holds ZERO Python**, 1103 tracked files → 786, and its 701 artifacts still regenerate byte-identically from here with the oracle silent, run before the deletion, after it, and after the prose edits. **Ben was asked first and answered one question: delete the 40 orphaned UXLC data files** rather than keep them, so that repo no longer holds the UXLC snapshot its published review was built on, the bytes surviving in UXLC-utils and here. Seven things to carry. **Phase 7 item 1 fired inside Phase 4 for the THIRD repo running, and costs two tests rather than holman's predicted three**: `test_vendoring_policy_paths.py` collected 25 → 23, because book-of-job had **one** `pkg_scan_root` where holman had two — **the rule is one case per scan root plus one dest-repo case, so count scan roots rather than repeating the number three**; inventory 20 rows/129 files → 18/112, with the three `out/vendoring_*` artifacts 55 lines of pure deletion and no additions. **Two forecasts came out one short each and both for the same cause, a forecast made before a decision**: mark order scans **298** files rather than the predicted 299 (`check_mark_order._corpus_json_files()` yields every `.json` under the data root, so Ben's delete decision took `py_uxlc_loc/UXLC-misc/lci_recs.json` as well as the spelling dictionary), and the NFC scope holds **35** rather than 42 (the seven procedure docs that moved here, the prediction having counted `doc/` at nine). Neither is a defect and each was visible only because the **count** was read rather than the verdict. **The `59 subtests` figure DOES reproduce, and Phase 1's reason for saying otherwise was wrong twice over**: `pytest-subtests` is indeed absent, but the figure never came from it — six modules under `py/tests/` use `unittest`'s native `self.subTest`, which pytest counts on its own. **The standing baseline is `947 passed / 5 skipped / 59 subtests`**, and 945/5/59 after this phase. Three phases across two plans argued that figure back and forth without naming its mechanism; the rule that would have ended it is **when a figure will not reproduce, find what produces it before concluding it is spurious** — `grep -rl subTest py/tests` was the whole investigation. **The nine procedure docs split 7–2 on a criterion this plan did not supply**: the plan's "published site rather than how it is made" does not decide `viewing-image-metadata.md` or `reading-mam-simple.md`, and what was used instead is **a doc moves if following it means touching the code or the pipeline the code drives, and stays if following it means looking at something the emptied repo holds**. The seven arrive as `doc/boj-*.md`, matching the `author_boj_*` marker; `CLAUDE.md` here gains a section for them, nothing in the code pointing at them. **Repointing a doc is not just paths, and checking that every path resolves is what proves it** — 17 of 17 do here, and the check caught a double `py/py/` prefix. Four things a path rewrite alone would have missed: two of the seven told a reader to verify with **`git status --porcelain`**, the instrument this plan warns against and one that is also unrunnable across repos; the `.novc/` apply-script template's `ROOT` walk broke and now takes its destination from `boj_paths.aleppo_img_dir()`; `cam1753-word-crops.md` calls the manuscript **μC** where the site and the code both say **μY**, so **a doc unread for two years disagrees with the artifacts about more than paths**; and that same file spells its commands with **backslashes**, so a forward-slash pass missed all eleven. **There was no `.vscode/`, but there is a `book-of-job.code-workspace` and a `requirements.txt` at the repo root**, both orphaned by the deletion, neither a `.py`, neither in the plan's prescription — **at the trio, sweep the repo root for files whose subject is the interpreter rather than the code** the way holman's phase says to sweep for non-`.py` under `py/`. **Ben chose to delete both**, `aa20c61` there and the commit carrying this record here, taking book-of-job to **784** tracked files and a root of four; the NFC scope went 35 → **33**, exactly as predicted. **The workspace file is the one to look at rather than assume** — mostly launch configurations and `python.analysis` settings, but it also declared the three-folder view opening book-of-job beside the two codex-index repos, which is not about Python and is why it was a question rather than a step. And **`mb_cmn/provenance.py`'s `parents[2]` is moot for book-of-job now**, the tree holding the wrong copy having been deleted; what remains is only whether this repo's copy should walk to `.git` for the *other* repos, which is not Phase 4's to decide. **Phase 3 landed as `ef8e384` here — 243 files under the four names Ben settled that day (`author_boj_qr/` 160, `author_boj_util/` 33, `author_boj/` 10, `boj_render/` 7, plus `pydiff_mm/`, the two word-image packages and seventeen top-level modules), with 363 import rewrites across 105 files; nothing owed in book-of-job, whose HEAD is `45f8853` before and after.** **The oracle passed on the FIRST run from here and on every run since**: silent, all **701 artifacts byte-identical**, from this repo's root, from `GitRepos`, and from book-of-job's own copy — so both residencies produce the same bytes. Suite unchanged at 947 passed / 5 skipped; `check_all.py` 7 of 7 from both repos. Seven things to carry, and the first three are corrections to what this row promised. **The `path_to_uxlc` parameter is NOT needed and was not added**: all 39 UXLC XML are one blob across book-of-job, this repo and UXLC-utils, and `lci_recs.json` differs from UXLC-utils' copy in exactly one header line whose `body` is identical — so `prep()` now takes no arguments, `uxlc_misc`/`uxlc_lci` were not touched, and putting the parameter back would have re-imported the only content difference Phase 0's reconciliation dropped. The cost is that regenerating book-of-job's site now needs UXLC-utils checked out, and that book-of-job's 40 UXLC data files are read by nobody — **a Phase 4 question, not a defect**. **`py_cam1753_word_image/page.py` was left alone and so was `flat_index.py`, so both blobs stay shared**, and the move settles them in OPPOSITE directions: `flat_index.py`'s `parent.parent.parent` becomes RIGHT here, landing on the repo root exactly as in codex-index-aleppo, while `page.py`'s `parent.parent` becomes wrong. Both are inert — the three directories `page.py` names are absent from book-of-job and from here — so the plan's own "both repos at once or not at all" was taken as "not at all". **The venv needed `numpy` as well as `pyspellchecker`**, without which neither crop editor imports; `matplotlib`, which book-of-job's `requirements.txt` also names, is imported by **nothing** in that repo, so **read what the code imports, not only what `requirements.txt` declares**. **The one fork the move forced is four source lints.** `check_function_ordering`, `check_mark_order`, `check_escape_sequences` and both `fix_*` scanned a repo root that held nothing but book-of-job's code and now holds all of MAM-basics; measured, function ordering reports **1172** violations across `py/` against 0 across these packages, and the other two report violations in `py/ws/` and `py/wlc_cmn/`. They take their scope from `boj_paths.code_paths()` now, which **forks four files that were one blob with codex-index-cam1753's** — unavoidably, since **a `.git` walk finds a repo root and cannot find a subtree**, which is the wall the trio will meet. **`fix_mark_order.py` is the one that mattered**: no `main()`, no dry-run, it rewrites every file under the root it finds at import, so left alone it would have reformatted this repo on sight. **A lint that loses its inputs goes on printing OK**: scoping mark order to the code alone took it from 326 files to 241 and it still said OK, the missing 58 being book-of-job's `.json`, which stayed in the corpus — it reads both roots now and scans 300. **When a check changes scope, read what it counted, not whether it passed.** **Two of this repo's own lints fired on the arriving code and both were right**: `test_transliterations.py` on a `$tipeha` substitution key spelling ḥet with `h` where its fifteen neighbours use `x` (renamed `$tipexa`; safe to the byte, the table row being its only occurrence in 241 files), and `check_function_ordering` on a function this phase had just written. **The NFC test's fourth `_Scope`** needed no `_BINARY_EXTENSIONS` addition, book-of-job's sixteen being a strict subset — the negative result of the check holman's phase asked for. And **`doc/vendoring-inventory.md` was stale, made so by Phase 0's own re-vendoring**; regenerated as `a585cb6`, separately from the move. Phase 0 had spent a subsection on wrongly calling that file stale, so the other half of the lesson is: **re-read an artifact after changing what it measures, not only before.** **Phase 1 landed as `45f8853` there (18 files, +305/−100), adding `boj_paths.py`; nothing was owed here.** The oracle now runs from `C:\Users\BenDe\GitRepos\MAM-basics` as the working directory with all **701 artifacts byte-identical** and this repo's tree untouched, `check_all.py` 7 of 7, the NFC suite 6 tests OK. Tracked `.py` **267 → 268**, lines **16,859 → 17,064**, so **Phases 3 and 4 face 268 files**. Six things to carry. **A third answer to the `mb_cmn/paths.py` question**: holman inherited it, UXLC-utils vendored it, and **book-of-job must do neither** — `paths.repo_root()` is `parents[2]`, right for a `py/mb_cmn/` and wrong at book-of-job's **root-level** `mb_cmn/`, where it lands on `GitRepos`, so `boj_paths.code_root()` walks to `.git` instead. **Check the depth of `mb_cmn/`, not only its presence.** **The prescribed grep undercounted by six**, the one that mattered being `job_ov_and_de.py`'s `"py_uxlc_loc/UXLC"` pair — a prefix no search for `gh-pages/` or `out/` looks for, and what a foreign-cwd run actually dies on — plus a `_Path("gh-pages")` with no slash inside the quotes, an argparse `default="gh-pages"`, and two cwd-relative scans of source; **and two of its seven hits are false positives**, `test_h_dot_below_nfc.py`'s `"out/"` and `"gh-pages/"` being repo-relative exclusion prefixes rather than constructed paths. **The fault here is cwd-relativity and root conflation in equal measure**, against holman's finding that it is conflation alone: `check_spelling_in_html.main()` is the miniature, one `Path(__file__).parent` standing for both the `gh-pages` tree it reads and the custom dictionary beside its own module. **The foreign-cwd verification convention would have clobbered a tracked file here** — run before the fix, book-of-job's oracle writes `gh-pages/index.html` cwd-relatively and this repo has one of its own, so it would have overwritten it and reported success; **check what a repo's entry points write to a bare relative path before running one from here**, since two of the trio write a `gh-pages/` tree. **Being one blob across two repos does not make a depth-counting walk right in both**: `py_ac_word_image_helper/flat_index.py` is `af610508` in book-of-job and codex-index-aleppo alike and resolves to `GitRepos` in the first and the repo root in the second, because Phase 0 reviewed only the sixteen files that had **diverged** and this one was already identical — so **step 5 should sweep the reconciled packages for `parents[`/`.parent.parent` outright**. Phase 1 left it and `py_cam1753_word_image/page.py` alone rather than re-fork the family; `page.py` is correct in both repos today and becomes a **Phase 3** item. And **one question is open and is Ben's**: `mb_cmn/provenance.py`'s `parents[2]`, wrong in book-of-job alone of the four copies that exist, latent (nothing there passes `generator_file`, and `git grep "generated by book-of-job"` returns 0, so Phase 6's blast radius there is nil) and erased by Phase 4's deletion of that tree — leave it, or make MAM-basics' copy walk to `.git` and re-vendor. **Phase 0** owned the two fork families this programme's Phase 0 did not cover, and they split. **`mb_cmn/` reconciles**: all six differing files are droppable drift, MAM-basics' copy being the later text in five of them, and book-of-job's two extra `hebrew_punctuation.py` functions being dead since they arrived in 2026-02. It drags a **seventeenth** file though — MAM-basics' `file_io.py` imports `mb_cmn.provenance`, which book-of-job lacks, and whose `parents[2]` is wrong at book-of-job's root-level `mb_cmn/`. **`py_uxlc_loc/` hits the gate, and nothing was changed in either repo.** Six of its nine counterparts differ in **nothing but** an import prefix and a docstring style; the other three differ in one thing, that book-of-job's fork takes its data root as a parameter where MAM-basics' hardcodes `paths.in_dir()`. The reason that is not droppable is the **data**: book-of-job reads a **UXLC 2.1** snapshot and MAM-basics' `in/UXLC-39/` is **UXLC 2.5**, two years apart, with **30 edit runs** in the text of Job and its word count moving 8283 → 8288 — a maqaf gone from `לֹֽא־`, three deḥi-for-tipeḥa exchanges, a revia for a geresh — and word count is exactly what the location estimator runs on. book-of-job's `lci_recs.json` is meanwhile **richer** than MAM-basics' for Job, carrying column and line coordinates for Leningrad pages 397A and 406A where MAM-basics has `null`. Measured rather than argued: with book-of-job's own data the oracle is silent and all 701 artifacts are byte-identical; with MAM-basics' data it **crashes** until MAM-basics' `_stripped_text` guard is applied, and then the 701 are still byte-identical but **two new `fline mismatch` warnings** appear, at exactly the two rows sitting on those two pages. **Three corrections to that plan's own premises**, each cheap to check and each carried for seventeen days: only **one** module lacks a counterpart, not two; the other supposed orphan, `my_tanakh_book_names.py`, is an older copy of `mb_cmn/bib_locales.py`, so **book-of-job holds two copies of that module** and both are live; and **MAM-basics holds two forks of the UXLC location code**, `py/py_uxlc/` from wlc-utils and `py/uxlc_misc/`+`py/uxlc_lci/` from UXLC-utils, differing from each other by up to 78 lines, so "reconcile onto MAM-basics' copy" names two different files per module. **Three findings every remaining plan needs.** The **oracle** is `main_gen_misc_authored_english_documents.py` alone, which rewrites **183** of the 701 — so **518 tracked artifacts are written by no program**, most of Phase 4's naming job already done. The **venv held one of the five packages its own tracked `requirements.txt` names**, and the missing `pyspellchecker` stops the oracle and not merely `check_all.py`, which widens this file's Phase 0 finding: **install each repo's `requirements.txt` before concluding anything about what its entry points do**, and note MAM-basics' venv lacks `pyspellchecker` too. And **`git status --porcelain` is the wrong instrument here** — a no-op regeneration leaves it reporting 183 modified files whose blobs are unchanged, because git's cached stat sizes are the pre-run CRLF ones (777 against the real 757) and `update-index --refresh` will not clear them; use a byte comparison against `git cat-file blob HEAD:<path>`, which gives 700 identical, 1 line-ending-only, 0 content differences. That is the **fourth** table this instrument would have corrupted. One thing that needed no fixing: **`doc/vendoring-inventory.md` was right all along** — it has recorded 6 `DIFFERS`, 9 `eol-only` and 1 `identical` since `compare.py` grew its three-verdict column on 2026-08-04, so the plan's "still records all 16 as DIFFERS" was the stale claim. Phase 0 also recorded a correction to the holman-ketiv-qere row above, saying its **Finding 3 was wrong to drop the `59 subtests` figure** because the figure had reproduced; **Phase 1 re-measured and it does not**. Twice at `7bf4e00`, the suite reports **947 passed, 5 skipped** with no subtests line: `self.subTest` is used in 25 test files, `pytest-subtests` is absent, and pytest 9.1.0 does **not** count `unittest` subtests without it — the subtests run, but nothing counts them in the summary. **So Finding 3 was right on the substance and Phase 0's correction of it was wrong. The standing baseline is `947 passed, 5 skipped`**, and no remaining phase should go looking for a third figure. **Ben answered the gate the same day and both families were then reconciled**: move to UXLC 2.5, put the finer 397A/406A records upstream and into **both** copies of `lci_recs.json`, and target `uxlc_misc`/`uxlc_lci`. Landed as `4d1ad89` in UXLC-utils, `2979507` here, and `6fb8c06` plus `7ca99f7` in book-of-job. **All 701 artifacts stayed byte-identical at every step, and the final run is silent** — the two `fline mismatch` warnings the coarse records produced are gone, so the corpus moved two years and the review's 160 recorded Leningrad locations still check out. `check_all.py` passes all 7 checks there for the first time. Three things worth carrying: **check the predicate a caller uses, not a function's whole range** (`section` and `get_secid` disagree on 25 of 39 books, purely in the ḥ-against-x transliteration of the section-id strings, while the one predicate book-of-job asks agrees on all 39); **`main_write_page_break_info.main()` needs two runs to propagate**, reading `data/lci_recs.json` before copying `in/UXLC-misc/lci_recs.json` over it; and enriching those two pages moved `all_changes_loc_checks.json` by 9 entries of 1399, 5 better and 4 worse, total absolute `fline_diff` **33.03 → 12.38**, the win being 397A column 3 line 21 going from 23.69 lines out to 1.47 |
| codex-index-aleppo, -leningrad, -cam1753 | [PLAN-evacuate-python-from-codex-index-trio.md](PLAN-evacuate-python-from-codex-index-trio.md) | **not started** — all three, cam1753 included |
| MAM-simple | Appendix A below — **out of scope, nothing to evacuate** | closed, no work |
| diffable-pointed-hebrew | Appendix B below — **out of scope, left alone** | one loose end, see B |

**Every number below was measured on 2026-08-02** with the command given beside it; re-measure
before relying on any of them, and treat a mismatch as a finding rather than as noise. UXLC-utils'
Phase 1 has since moved that repo's own figures — 102 tracked `.py`, 17,932 lines, 22 vendored
`mb_cmn/` — and its plan records why.

**That instruction has now paid twice, and the second time it moved every figure for a repo.**
holman-ketiv-qere re-measured on 2026-08-18, at its `637237b`: **99** tracked `.py` against 68,
**16,416** lines against 11,159, **300** tracked `gh-pages` against 161, **9** entry points against
6, and **37** vendored files against 26 — the extra ten being `uxlc_lci/` (4), `uxlc_misc/` (5) and
`uxlc_paths.py`, all byte-identical and all invisible to `doc/vendoring-inventory.md`. A second body
of work had arrived in the sixteen days between: Holman's suggested UXLC corrections, extracted from
his emails. Its plan's re-measured baselines table carries the detail. **Treat the two repos not yet
measured as stale by a comparable margin**, and note that where holman's copies were merely
miscounted, book-of-job's and the trio's have **diverged**, so a copy the inventory cannot see is
lost work there rather than an accounting error.

---

## Why these six, and why public-only

**The destination is a public repo.** MAM-basics is `PUBLIC` (`gh repo list bdenckla --json
name,visibility`). That single fact settles the scope: Python that lives in a private repo cannot
be moved into MAM-basics without publishing it, so the private Python-heavy repos are out of
scope no matter how taxing they are to maintain. That is not a deferral — it is a different
problem with a different answer, and none of these plans should be read as a step toward it.

Out of scope, with the count that would otherwise have qualified each:

| Repo | Tracked `.py` | Why out |
|---|---|---|
| al-hatorah | 268 | private |
| mgketer | 130 | private |
| MAM-for-CCAR | 69 | private, and frozen (`in/repo_maintenance_policy.json`) |
| MAM-for-JPS | 58 | private, and frozen |
| hbofonts | 38 | private |
| MAM-for-Acc | 29 | private, and frozen |
| masorah-books | 19 | private |
| TMC | 17 | private, and frozen |
| CCAR-Psalms | 6 | private, and frozen |

**al-hatorah is the sharpest exclusion and worth stating plainly**: at 268 tracked `.py` it is
larger than book-of-job and larger than wlc-utils was, it is actively developed, and it vendors
28 `mb_cmn` files by copy script. It is excluded solely because it is private. If the tax of
maintaining Python across repos is what motivates this programme, al-hatorah is the biggest
single instance of that tax and this programme does not touch it. Say so when reporting progress,
so "all the Python is consolidated" is never claimed.

**The different answer now exists — `bdenckla/MAM-private`, created 2026-08-07.** Ben's decision
of that date: a new private repo is the destination for the full contents — not Python-only — of
masorah-books, al-hatorah, wlc-utils-private and mgketer, one top-level directory per source
repo. Its plan is `MAM-private/doc/PLAN-evacuate-private-repos.md`, kept there rather than beside
this file because MAM-basics is public and that plan discusses private repos' internals. Nothing
about this programme changes: private Python still does not move into MAM-basics, and the
al-hatorah paragraph above stands — al-hatorah's evacuation is whole-tree, into MAM-private,
under that plan.

## Scale — measured 2026-08-02

`git ls-files "*.py" | wc -l` and `git ls-files "*.py" -z | xargs -0 wc -l` in each repo:

| Repo | Tracked `.py` | Lines | Vendored `mb_*` | Vendored state | Tracked artifacts (the oracle) | Last commit | Pages workflow |
|---|---|---|---|---|---|---|---|
| book-of-job | 267 → 268 → **0** | 17,060 → 16,859 → 17,064 → **0** | 16 → 17 `mb_cmn/` → **0**, deleted with the rest | **DIFFERS** → identical, all 17 → **entry deleted from the policy** | `gh-pages` 694, `out` 7 | 2026-08-02 → 2026-08-19 → **2026-08-21** | `static.yml` |
| UXLC-utils | 100 | 17,651 | 21 `mb_cmn/` + 3 `mb_diff_mpu/` | identical | `gh-pages` 184, `out` 27, `in` 556 | 2026-08-02 | `pages.yml` |
| holman-ketiv-qere | 68 | 11,159 | 17 `mb_cmn/` + 9 `mb_diff_mpu/` | identical | `gh-pages` 161, `out` 2 | 2026-08-02 | `pages.yml` |
| codex-index-aleppo | 44 | 8,223 | 4 `py/mb_cmn/` + 4 in `aleppo-wiki/py/` | **DIFFERS** | `line-breaks` 35, `column-coordinates` 35, `aleppo-wiki` 26, `ds-flat-stream` 8, `gh-pages` 4 | 2026-08-02 | `pages.yml` |
| codex-index-leningrad | 38 | 4,358 | 4 in `lenin-wiki/py/` | **DIFFERS** | `lenin-wiki` 21 | 2026-07-27 | none |
| codex-index-cam1753 | 22 | 5,386 | 3 `mb_cmn/` | 2 identical, `str_defs.py` **DIFFERS** | `cam1753-col-quads` 28, `cam1753-line-breaks` 27 | 2026-04-27 | none |
| **total in scope** | **539** | **63,837** | | | | | |
| diffable-pointed-hebrew — **out of scope**, Appendix B | 9 | 561 | 8 `mb_cmn/` | **DIFFERS** | none tracked | 2026-04-27 | none |

For comparison, wlc-utils was **267 files / 59,870 lines** in one repo. This programme is the same
volume of code again, spread over six repos with six different shapes — which is why it is four
plans and not one. MAM-basics currently tracks **693** `.py`; it would end near **1,180**.

The vendored-state column is read from `doc/vendoring-inventory.md`, regenerated by
`py\main_vendoring.py --all`. **Every repo whose mechanism the inventory records as `unknown` has
a `DIFFERS` copy, and every repo with a copy script is `identical`** — book-of-job, all three
codex-index repos and diffable-pointed-hebrew on one side; UXLC-utils and holman-ketiv-qere on the
other. That correlation is the single best predictor of how hard each repo will be.

## Decisions carried over from the wlc-utils plan

These four hold here unchanged. Do not relitigate them per repo.

1. **Plain copy, no git history graft.** History stays readable in the source repo, which is not
   going away.
2. **`gh-pages/` stays put indefinitely** in every repo that has one, and so does its Pages
   workflow. Moving it would break links in the wild with no forwarding mechanism. The moved code
   writes back into its old repo as a sibling — already MAM-basics' dominant pattern.

   **Broken once since, deliberately — wlc-utils, 2026-08-17, by
   `doc/PLAN-evacuate-the-rest-of-wlc-utils.md`.** That plan moved wlc-utils' whole `gh-pages/`
   into MAM-basics (nested as `gh-pages/wlc/`, a pure prefix rewrite of every URL) after first
   building the forwarding mechanism this decision says did not exist: each of the 154 published
   pages was replaced in place by a redirect stub naming its successor, plus a `404.html`
   catch-all, generated by `py/main_wlc_redirect_stubs.py`, with every externally cited URL
   re-fetched and verified after the flip. The decision's reasoning stands — do not move a
   `gh-pages/` without a forwarding mechanism — but "indefinitely" is no longer literal, and a
   repo in this programme whose `gh-pages/` is ever to move has that plan's Phases 8–10 as the
   worked, verified shape of the exception.
3. **Regenerating the tracked artifacts byte-identically is the test.** No new example-based unit
   tests. Each plan names its own oracle and the one command that re-establishes it.
4. **Issues unify going forward only.** Existing issues keep their numbers and stay in their own
   trackers; a moved file's bare `#NN` gets a `<repo>#` prefix.

## Two decisions that do NOT carry over

The wlc-utils plan settled these; both are **false for this programme**, and assuming otherwise is
the fastest way to lose code silently.

- **"Flat namespacing, minimal renames — none collide."** That was true of wlc-utils and is
  emphatically not true here. Landing these six repos flat into `py/` would collide on at least
  eleven names, several of them between two source repos rather than against MAM-basics. The
  collisions are enumerated under "Cross-cutting findings" below, and Programme Phase 0 exists to
  resolve the worst family before anything moves.
- **"The vendored copies are pure deletions."** True for UXLC-utils and holman-ketiv-qere, whose
  copies are byte-identical. False for the other five: their `mb_cmn` copies have **diverged**, so
  deleting one destroys whatever local edit it carries. Each affected plan diffs its copies against
  MAM-basics' originals and resolves the differences as a **findings step of its own**, before any
  deletion.

---

## Programme Phase 0 — reconcile the drifted `check_*`/`fix_*` family — BLOCKING — **DONE 2026-08-19, all three steps**

**All three steps are done.** 0a reached the gate the prescription below sets — category (iii)
differences exist, in two of the six scripts — and **Ben's decision, 2026-08-19, was to reconcile
the six files that are one tool with drift and leave `check_all.py` and `check_word_finding.py`
per-repo permanently as what they are.** 0b landed that as `33b3ee2` in book-of-job, `98021de` in
codex-index-aleppo and `f56831c` in codex-index-cam1753, each pushed fast-forward from the head 0a
recorded — `60db958`, `3fd07be` and `e5b2ae4`, all last committed 2026-08-07. 0c holds: **fourteen
of the sixteen files are one committed blob**, and the two left per-repo differ in every pair, by
design. **The family can now land in MAM-basics once instead of three times**, which is what steps
4 and 5 of the Order section were blocked on.

The record below runs 0a first, then 0b and 0c, then the prescription as written 2026-08-02.

Absolute paths, since a fresh session executes this: `C:\Users\BenDe\GitRepos\book-of-job` (the
forked files at the repo root), `C:\Users\BenDe\GitRepos\codex-index-aleppo` (under `py/`),
`C:\Users\BenDe\GitRepos\codex-index-cam1753` (repo root). Each has a `.venv` with black 26.5.1
and **no pytest**, measured 2026-08-19, so there is no suite to run in any of the three.

### The gate, and what it decides

The prescription says to stop and ask Ben if 0a finds a category (iii) difference — a genuine
behavioural difference the repos need — because that makes the family three tools with a shared
ancestor rather than one tool with drift. Two of the six scripts are category (iii):

- **`check_all.py` is each repo's register of which checks that repo runs, and the three registers
  name three different sets of checkers.** book-of-job runs seven — spell check, function
  ordering, qr filename/record consistency, cross-record relation validity, mark order, escape
  sequences, HTML output lint — and takes `--w3c` and `--w3c-strict`, forwarded to
  `check_html_syntax_and_sanity`. codex-index-aleppo and codex-index-cam1753 run four — word
  finding, escape sequences, mark order, line-break JSON consistency — and take no arguments at
  all. Five of book-of-job's seven checkers exist in neither codex-index repo
  (`check_function_ordering.py`, `check_html_syntax_and_sanity.py`, `check_qr_consistency.py`,
  `check_qr_relations.py`, `check_spelling_in_html.py`), and `check_word_finding.py` and
  `check_line_breaks.py` exist in neither book-of-job nor at the same location as each other:
  codex-index-aleppo has `py/py_ac_loc/check_line_breaks.py` and imports it as
  `from py_ac_loc import check_line_breaks`, codex-index-cam1753 has `check_line_breaks.py` at its
  repo root and imports it as `import check_line_breaks`. Re-establish with
  `git -C <repo> ls-files | grep -E '(^|/)(check|fix)_[a-z_]*\.py$'`.
- **`check_word_finding.py` is two programs against two manuscripts.** It is absent from
  book-of-job. codex-index-aleppo's copy imports `py_ac_word_image_helper`, reads the `qr-ac-loc`
  field of the quirkrec, and calls `load_index("Job")` before `find_pages_for_verse(pages, ch, v)`;
  codex-index-cam1753's copy imports `py_cam1753_word_image`, reads `qr-cam1753-loc`, and calls
  `find_pages_for_verse("Job", ch, v)` with no index at all — so the two word-image packages do not
  share a signature either. The substantive difference is the tolerance each check allows a **maqaf
  compound**, one chanted word written as two atoms joined by a maqaf. codex-index-aleppo accepts an
  alternative **word** index, `word2`, for a compound occupying more than one token position on a
  line. codex-index-cam1753 accepts an alternative **line**, `line2`, and additionally accepts the
  found line number itself matching `line2` — its line-break data has maqaf compounds split across a
  line break, and the Aleppo Codex data as indexed here does not. Two manuscripts, two layouts, two
  JSON schemas.

**The answer is therefore a three-way design call rather than the two-way one the prescription
anticipated, because the split runs per file and not per repo.** Of the eight files that genuinely
diverge, four are one tool with drift and reconcile cleanly, two reconcile with one added parameter
or by running a command the repo already has, and two do not reconcile at all. Awaiting Ben's
decision; nothing in the three repos was changed.

### The counts were measured with the wrong instrument, and four of the sixteen are not forked

**`cmp` on the working tree measures line endings, not content.** Measured 2026-08-19 with
`git -C <repo> ls-files --eol -- '*.py' | awk '{print $2}' | sort | uniq -c`: book-of-job holds
**258 of its 267** tracked `.py` as CRLF in the working tree, codex-index-aleppo **42 of 44**, and
codex-index-cam1753 **all 22 as LF**. Every one of the three has an LF index and a `.gitattributes`
declaring `* text=auto eol=lf`, so the CRLF is a stale checkout in the working tree and never
reaches a commit. The consequence for the prescription's table: **every `cmp` against
codex-index-cam1753 was guaranteed to report `differ` whatever the content was.**

Re-run against the committed blob instead — `git -C <repo> rev-parse HEAD:<path>` — and **all four
`py_cam1753_word_image/` files are the same blob in book-of-job and codex-index-cam1753**:
`crop.py` `48c3a3e6`, `hebrew_metrics.py` `81a9f188`, `linebreak_search.py` `6a41edaa`, `page.py`
`73b3d80d`. They are not forked. The prescription's "**All four differ**" is an artifact of
book-of-job's working-tree line endings and nothing else.

**So of the sixteen files the prescription reviews, eight diverge and eight are byte-identical in
committed content**, not the twelve its table implies. The eight that diverge are the six scripts
plus `py_ac_word_image_helper/alef_bet_to_ascii.py` and `py_ac_word_image_helper/codex_page.py`.
The four `py_ac_word_image_helper/` files the table already called identical (`crop.py`,
`flat_index.py`, `hebrew_metrics.py`, `linebreak_search.py`) still are.

**Compare committed blobs, not working trees, at book-of-job and at the codex-index trio.** That is
the instrument correction to carry into steps 4 and 5 of the Order section; it is cheap, and here it
changed a quarter of the table's verdicts.

### The classification, file by file

| File | Divergence | Category |
|---|---|---|
| `check_all.py` | three different check registers; `--w3c` flags in book-of-job only | **(iii)** |
| `check_word_finding.py` | two manuscripts, two packages, two JSON schemas, two maqaf tolerances | **(iii)** |
| `check_escape_sequences.py` | `_KEEP_AS_ESCAPE` entries dropped; `mb_cmn` skip; a dead range exemption | **(ii)** + **(i)** |
| `check_mark_order.py` | function order, docstring wording, ruler padding, quotation marks | **(ii)**, cosmetic |
| `fix_mark_order.py` | `newline=""` missing in codex-index-cam1753 | **(ii)**, live defect |
| `fix_escape_sequences.py` | `newline=""` missing in codex-index-cam1753; function order | **(ii)**, live defect |
| `py_ac_word_image_helper/alef_bet_to_ascii.py` | escapes not yet converted to literals in codex-index-aleppo | **(ii)** |
| `py_ac_word_image_helper/codex_page.py` | `ROOT` depth; function order | **(i)** + pure move |

**`check_escape_sequences.py` — one part of it is load-bearing and must survive any
reconciliation.** book-of-job keeps U+2002 EN SPACE and U+2003 EM SPACE in `_KEEP_AS_ESCAPE`; both
codex-index copies dropped those two lines. book-of-job needs them:
`pyauthor/job1_full_list_details.py:41` has `" \u2003 "`, and under the codex-index copies' set that
line becomes a violation demanding an invisible em space be written literally into source — the
thing `_KEEP_AS_ESCAPE` exists to prevent, and what the user-level `CLAUDE.md` Unicode section
forbids. Neither codex-index repo has any U+2002 or U+2003 site, so the reconciliation is the
**union**, keeping book-of-job's two entries; re-establish with
`grep -rn --include='*.py' -E '\\u200[23]' <repo> --exclude-dir=.venv`. The second difference is
`_SKIP_PREFIXES = {"mb_cmn"}` in both codex-index copies and absent in book-of-job. The third is
`_RANGE_RE` and `_range_endpoint_positions` in book-of-job alone, exempting `\uXXXX-\uYYYY`
character-class ranges.

**0a called the range exemption dead and it is not — the two differences are one difference, and
0b turned on seeing that.** This paragraph said `_RANGE_RE` was "dead either way" on the evidence of
a grep returning nothing. **The grep was wrong**: written `-E '\\u[0-9A-Fa-f]{4}-...'` it matches
nothing in GNU grep's ERE, and the working spelling is `-E '[\]u[0-9A-Fa-f]{4}-[\]u[0-9A-Fa-f]{4}'`,
which finds twelve sites in book-of-job. The one that matters is
`mb_cmn/hebrew_points.py:33`, `RECC_HEBR = "֑-״"` — a plain string rather than a raw one,
so the raw-string exemption does not reach it, and U+05F4 HEBREW PUNCTUATION GERSHAYIM is
punctuation rather than a combining mark, so `_KEEP_AS_ESCAPE` does not hold it either. **So the
codex-index copies added the `mb_cmn` skip to suppress a violation their own dropping of the
exemption had created**, and `mb_cmn` is a byte-identical vendored copy in all three repos and in
MAM-basics, so the violation was the same file in each. Restoring the exemption removes the reason
for the skip, which is what let 0b delete `_SKIP_PREFIXES` outright rather than parameterize it —
**the per-repo constant dissolved instead of needing a parameter.** The skip was root-relative
besides (`str(rel).startswith("mb_cmn")`), so it would have stopped matching the moment the root
moved. Check an exemption against the tree before calling it dead, and re-run a grep that returns
zero before believing it.

**`check_mark_order.py` — no behavioural difference in the three copies' text.** book-of-job against
codex-index-aleppo is a pure function move, `main()` before the private helpers rather than after,
plus docstring wording and ruler-comment padding; codex-index-aleppo against codex-index-cam1753 is
ruler-comment padding plus curly-against-straight quotation marks. Verified pure with
`diff <(sort A) <(sort B)`, which shows those lines and nothing else.

**`fix_mark_order.py` and `fix_escape_sequences.py` — one line each, and it is a live defect in
codex-index-cam1753.** book-of-job and codex-index-aleppo have
`p.write_text(new_text, encoding="utf-8", newline="")`; codex-index-cam1753 omits `newline=""`. The
argument entered the other two repos on 2026-07-06 in the commit "Adopt LF + NFC het-dot-below
standards" — `3c4d590` in book-of-job, `c1caebb` in codex-index-aleppo — and never reached
codex-index-cam1753; re-establish with `git -C <repo> log -S 'newline=""' -- <path>`. Measured on
this machine 2026-08-19: with the text built by `"\n".join(...)`, as both scripts build it,
`write_text(text, encoding="utf-8")` emits CRLF and `write_text(text, encoding="utf-8", newline="")`
emits LF. **So codex-index-cam1753's two `fix_*` scripts write CRLF into every file they rewrite**,
against that repo's `.gitattributes`, which `e5b2ae4` (2026-08-07) added declaring
`* text=auto eol=lf` while normalizing `cam1753-page-index.json` from CRLF to LF. The next run of
`fix_mark_order.py` there puts the CRLF back.

**One tempting explanation was checked and refused.** The CRLF that `e5b2ae4` normalized was **not**
written by `261434f` (2026-08-04, "Run fix_mark_order.py over the two pre-existing Ps 18 entries").
`cam1753-page-index.json` was already CRLF at `261434f^`, 66 CRLF lines of 66, so that run preserved
CRLF rather than introducing it. The defect is forward-looking, not historical, and the neat story
that the 2026-08-04 run caused the 2026-08-07 cleanup is false.

**`py_ac_word_image_helper/alef_bet_to_ascii.py` — codex-index-aleppo's checker reports this one
itself.** book-of-job has the Hebrew letters as literals with ASCII comments; codex-index-aleppo has
them as `\uXXXX` escapes with Hebrew comments. Running codex-index-aleppo's `py/check_escape_sequences.py`
exits 1 with **32 violations, of which 28 are in `py_ac_word_image_helper/alef_bet_to_ascii.py`**,
3 in `py_ac_loc/plot_col_coords.py` and 1 in `py_ac_loc/gen_col_quad_editor.py`. book-of-job's copy
passes at zero. The remedy is `fix_escape_sequences.py --apply`, which codex-index-aleppo has and
has not run. (**0a first wrote "every one of them" in `alef_bet_to_ascii.py`**, having read the
offenders off the tail of the output rather than grouping them; the four in `py_ac_loc/` are outside
the sixteen files this phase reviews, which is why the miscount mattered — it hid the fact that
clearing the sixteen would not by itself make the repo's check pass. Group the output, never read a
tail: `… | grep '→' | sed 's/:.*//' | sort | uniq -c`.)

**`py_ac_word_image_helper/codex_page.py` — one constant, and no behavioural difference.** The only
content change is `ROOT = Path(__file__).resolve().parent.parent` in book-of-job against
`.parent.parent.parent` in codex-index-aleppo, which is the `py/` level.
`diff <(grep -v '^ROOT = ' A | sort) <(grep -v '^ROOT = ' B | sort)` is empty, so every other line is
a move of the six private helpers.

### The divergence that matters most is in no diff at all

`check_mark_order.py` and `check_escape_sequences.py` compute `root = Path(__file__).resolve().parent`
— **byte-identical in all three copies** — and that line means "the repo root" in book-of-job and in
codex-index-cam1753, where the script sits at the repo root, and "`py/`" in codex-index-aleppo, where
it does not. `check_mark_order.py` scans `.py` **and `.json`**. Measured 2026-08-19 with
`git -C codex-index-aleppo ls-files '*.json'` against `ls-files 'py/*.json'`: codex-index-aleppo has
**84 tracked `.json` and not one of them under `py/`**, so its Hebrew mark-order check, whose subject
is the Hebrew in the index data, reads **none** of that repo's index data. It also misses the 11
tracked `.py` outside `py/`. book-of-job scans 325 files and codex-index-cam1753 94, both passing;
codex-index-aleppo scans 29 `.py` and 0 `.json`.

This is holman-ketiv-qere's Phase 1 finding — root conflation through a `Path(__file__)` walk —
arriving in a family whose three copies agree textually and disagree in effect, which is a shape
neither that plan nor this one predicted. **book-of-job and codex-index-aleppo have already fixed
exactly this in `codex_page.py`** and in neither checker, so the correction exists in the family and
was applied to one file of the three that need it.

### codex-index-aleppo has no zero-diff oracle to reconcile against

Two of codex-index-aleppo's four checks fail today, at `3fd07be`, before anything in this phase is
touched: `py/check_escape_sequences.py` exits 1 with 32 violations, and `py/check_mark_order.py`
exits 1 with **12 words of non-standard mark order, all twelve in `py/gen_index_flat_annotated.py`**.
book-of-job and codex-index-cam1753 pass both of their corresponding checks, at 0 violations each.
**0b's "regenerate and require a zero diff" therefore has no baseline in codex-index-aleppo** until
those two failures are dealt with — a precondition the prescription does not mention, and one that
has to be settled before 0b can pick that repo as the place the reconciled copy lands.

### A fifth copy axis the table does not cover

Within book-of-job alone, `py_ac_word_image_helper/crop.py` and `py_cam1753_word_image/crop.py` are
the same blob (`48c3a3e6`), as are the two `hebrew_metrics.py` (`81a9f188`); the two
`linebreak_search.py` differ. The two word-image packages are therefore partly forked from **each
other inside a single repo**, which puts two more copies of those files in play than the table
counts. Out of scope as the prescription is written — say so before 0b chooses a target, rather than
discovering it during the move.

### Activity re-measured — no repo is dormant, so "most active" does not pick a winner

The prescription says codex-index-cam1753 "last moved 2026-04-27". Measured 2026-08-19 with
`git -C <repo> log --format='%cs %h %s' --since=2026-02-01`, **all three last committed 2026-08-07**
— book-of-job `60db958`, codex-index-aleppo `3fd07be`, codex-index-cam1753 `e5b2ae4` — and
codex-index-cam1753 had eleven commits on 2026-08-04 alone, indexing Lamentations. Lifetime commit
counts are close as well: book-of-job 861, codex-index-aleppo 824, codex-index-cam1753 829.
**0b's stated tie-break does not decide anything**, and needs replacing with a reason that does.

### 0b and 0c — DONE 2026-08-19, on Ben's decision the same day

**Ben's decision, 2026-08-19, on the gate above: "reconcile the six, leave those two per-repo
permanently as what they are."** So `check_all.py` stays each repo's register of which checks that
repo runs, `check_word_finding.py` stays a per-manuscript verifier, and neither was touched. **0c's
"identical across all sixteen" is therefore replaced for those two and met for the other fourteen.**

**Landed as `33b3ee2` in book-of-job (5 files, +63/−9), `98021de` in codex-index-aleppo (9 files,
+273/−203) and `f56831c` in codex-index-cam1753 (4 files, +161/−105).** All three pushed
fast-forward from the heads 0a recorded. MAM-basics' own commit is this record.

**0c, on committed blobs, is the measurement that counts** — `git -C <repo> rev-parse HEAD:<path>`,
never `cmp` on a working tree, for the reason 0a records. Fourteen of the sixteen are one blob:
`check_mark_order.py` `b23e3764`, `check_escape_sequences.py` `23798624`, `fix_escape_sequences.py`
`d0d96439` and `fix_mark_order.py` `2add3471` across all three repos; the six
`py_ac_word_image_helper/` files across book-of-job and codex-index-aleppo, `alef_bet_to_ascii.py`
now `0c20729e` and `codex_page.py` now `38b42533`; and the four `py_cam1753_word_image/` files,
which were already one blob and still are. `check_all.py` and `check_word_finding.py` differ in
every pair, by design. **The working-tree `cmp` now agrees with the blobs on all sixteen**, because
0c also refreshed book-of-job's four stale CRLF `py_cam1753_word_image/` checkouts — `rm` plus
`git checkout --`, which git then reported as no change at all, the blobs having been LF the whole
time.

**book-of-job's copies are the canonical text, and the reason is that both of its apparent
eccentricities were load-bearing.** It alone kept `_RANGE_RE`, which the correction above shows
carries `mb_cmn/hebrew_points.py:33`; it alone kept U+2002 and U+2003 in `_KEEP_AS_ESCAPE`, which
carry `pyauthor/job1_full_list_details.py:41`; and it alone satisfies its `check_function_ordering.py`,
so its ordering is the only one that could be adopted everywhere without breaking a check that
exists in one of the three repos. **The copy that looks most cluttered was the only correct one** —
worth remembering at book-of-job and the trio, where the temptation will again be to take the
tidier fork.

**One change was made to that canonical text: the root.** `check_mark_order.py`,
`check_escape_sequences.py`, `fix_mark_order.py` and `py_ac_word_image_helper/codex_page.py` all
anchored on `Path(__file__).resolve().parent`, which the section above shows is the repo root in
book-of-job and codex-index-cam1753 and `py/` in codex-index-aleppo. They now call a `repo_root()`
that walks up to the nearest ancestor holding `.git`, identical in every copy:

```python
def repo_root():
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"{here} is not inside a git repository")
```

`(candidate / ".git").exists()` rather than `.is_dir()`, so a worktree's `.git` **file** resolves
too. It is spelled **public**, not `_repo_root`, because book-of-job's `check_function_ordering.py`
requires every public function to precede every private one and three of the four files needed the
root before their first private helper; `fix_escape_sequences.py` imports it from
`check_escape_sequences` rather than holding a fifth copy. **This is also what makes the family
portable into MAM-basics**, where these files will sit at a fourth depth — so the fix is a
precondition of the eventual move, not a side errand.

**What the wider root actually bought, measured before and after.** In book-of-job and
codex-index-cam1753 it changed nothing at all, which is the point: book-of-job still scans 325 files
for mark order and 267 `.py` for escapes, codex-index-cam1753 still 94 files for mark order. In
codex-index-aleppo `check_mark_order.py` went from **33 files to 128** and `check_escape_sequences.py`
from **29 `.py` to 44** — the 84 tracked `.json` that repo's mark-order check had never read, plus
the 11 tracked `.py` under `aleppo-wiki/`. Not one of the 84 held a violation, so the widening cost
nothing and closed a gap that had been open for as long as the fork.

**codex-index-aleppo passes both checks now, for the first time, and getting there took its own
tools on three files outside the sixteen.** `fix_escape_sequences.py --apply` replaced 4 escapes
with literals — the escape `\u00d7` with a literal `×` in `py_ac_loc/gen_col_quad_editor.py` and
`py_ac_loc/plot_col_coords.py`, and the escape `\u00b0` with a literal `°` in
`py_ac_loc/plot_col_coords.py`. `fix_mark_order.py` reordered marks on 8 comment lines of
`py/gen_index_flat_annotated.py`, where a shin dot, sin dot or dagesh sat after its vowel —
Unicode-normal order where these repos use MAM-normal order, the NFC-paste signature MAM-basics'
`CLAUDE.md` describes. **That was verified as a reordering and nothing else**: every changed line
has the same codepoint multiset before and after, and so does the whole file, which is the only
check worth running on a diff whose two sides render identically. Both fixes are the repo's own
tools doing their own job, the same move codex-index-cam1753 made at `261434f`.

**Dropping `_SKIP_PREFIXES` widened codex-index-cam1753's escape check too**, from 19 `.py` to 22 —
its three `mb_cmn/` files, still at zero violations, because the restored `_RANGE_RE` covers the one
line that had needed suppressing.

### Three findings from 0b for steps 4 and 5 — one to know before verifying, two to decide during

**None of the three blocks either step, and this heading said "all of them preconditions" until it
was corrected the same day.** A precondition is something that must be true before you start;
these are things that must be read before you conclude. Finding 1 changes how a verification run
is read, and findings 2 and 3 are decisions each step makes as it goes. **Nothing here is owed in
advance** — Phase 0 was the only gate in front of steps 4 and 5, and it is down.

- **No repo's `check_all.py` can run in its own venv, and that was true before this phase.** All
  three fail at import: book-of-job on `pyspellchecker`, codex-index-aleppo and codex-index-cam1753
  on `Pillow`, which `check_word_finding.py` reaches through `codex_page.py` and
  `py_cam1753_word_image/page.py`. **Pillow is in none of the three venvs.** Verified pre-existing
  by stashing this phase's files and getting the identical `ModuleNotFoundError` — do that before
  attributing any import failure to a change. So the oracle 0b actually ran was the individual
  checks, not the aggregate entry point, and **`check_all.py` has no working baseline in any of the
  three repos** for step 4 or step 5 to regenerate against.
- **book-of-job has none of the six data directories its two word-image packages need.**
  `line-breaks/`, `column-coordinates/` and `aleppo-pages/` exist only in codex-index-aleppo;
  `cam1753-line-breaks/`, `cam1753-col-quads/` and `cam1753-pages/` only in codex-index-cam1753.
  book-of-job's `main_gen_aleppo_crop_editor.py`, `main_gen_cam1753_crop_editor.py` and
  `main_apply_cam1753_crops.py` import those packages and read `LB_DIR`, `CC_DIR` and `IMG_DIR`
  straight off them, so in book-of-job they resolve to directories that do not exist and
  `load_index` returns an empty list rather than raising. **book-of-job holds 10 files of dead
  word-image code**, and reconciling 2 of them was still right — a `repo_root()` anchor reproduces
  today's behaviour in both repos — but **step 4 should decide whether book-of-job keeps those
  packages at all** rather than carrying them into MAM-basics.
- **A fifth copy axis, unchanged and still open.** Within book-of-job, `py_ac_word_image_helper/crop.py`
  and `py_cam1753_word_image/crop.py` are one blob (`48c3a3e6`), as are the two `hebrew_metrics.py`
  (`81a9f188`); the two `linebreak_search.py` differ (`856cd8ef` against `6a41edaa`). The two
  word-image packages are partly forked from each other inside one repo. 0b did not touch this, the
  prescription not covering it; name it in step 4 or step 5 before either plan moves a package.

---

### The prescription, as written 2026-08-02 and left unchanged

**Three repos carry three forks of the same six scripts, and only one of the six pairs is still
identical.** Measured with `cmp` on 2026-08-02:

| Script | book-of-job | codex-index-aleppo | codex-index-cam1753 | bj vs aleppo | aleppo vs cam1753 |
|---|---|---|---|---|---|
| `check_all.py` | root | `py/` | root | differ | differ |
| `check_mark_order.py` | root | `py/` | root | differ | differ |
| `check_escape_sequences.py` | root | `py/` | root | differ | differ |
| `fix_escape_sequences.py` | root | `py/` | root | differ | differ |
| `fix_mark_order.py` | root | `py/` | root | **identical** | differ |
| `check_word_finding.py` | — | `py/` | root | — | differ |

Two package directories are forked the same way:

- **`py_ac_word_image_helper/`** — 6 files in book-of-job, the same 6 in codex-index-aleppo's
  `py/`. Four are byte-identical (`crop.py`, `flat_index.py`, `hebrew_metrics.py`,
  `linebreak_search.py`); `alef_bet_to_ascii.py` and `codex_page.py` differ.
- **`py_cam1753_word_image/`** — 4 files in book-of-job, the same 4 in codex-index-cam1753. **All
  four differ.**

**Do not move three forks into one repo and sort them out afterwards.** Once they are all under
`py/`, two of the three must be renamed to land at all, the rename hides that they were ever the
same tool, and the divergence becomes permanent. Reconcile first, in the repos where the code
still runs against its own data and a regression is visible.

Phase 0 is therefore its own piece of work, ahead of book-of-job and the codex-index trio:

- **0a — Characterize each divergence.** For all 16 forked files, diff the copies and classify
  each difference as (i) a per-repo constant that belongs in a parameter, (ii) a fix applied to
  one copy and not the others, or (iii) a genuine behavioural difference the repos need. Write the
  classification into this file. **The counts above are the gate**: a re-measure that finds a
  different number of differing files means the tree moved, and the classification is stale.
- **0b — Land one reconciled copy per script, in whichever repo is most active** (book-of-job and
  codex-index-aleppo both had commits on 2026-08-02; codex-index-cam1753 last moved 2026-04-27).
  Each repo's own artifacts are the oracle: regenerate and require a zero diff.
- **0c — Re-run `cmp` and require `identical` across all 16.** Only then is the family one file,
  and only then can it land in MAM-basics once instead of three times.

**Stop and ask Ben if 0a finds category (iii) differences** — genuinely divergent behaviour means
these are not one tool with drift but three tools with a shared ancestor, and the answer is three
differently-named modules rather than one reconciliation. That is a design call, not a step.

## Order

1. **UXLC-utils** — the cleanest, and therefore the one that proves the recipe transfers off
   wlc-utils. Its vendored copies are identical, all its Python is under one `py/`, it has its own
   `CLAUDE.md` stating the conventions, and it already has a `main_0_mega.py` as the oracle
   command. It also has a **downstream consumer** (see finding 2), so doing it first is what
   teaches the trio's plan what a downstream repoint costs.
2. **holman-ketiv-qere** — the same shape, smaller, vendored copies identical. Confirms the recipe
   on a second repo before the expensive one. **DONE 2026-08-19 — every phase**, Phases 1, 3, 4
   and 6 on 2026-08-18 and Phase 7 on 2026-08-19; the Status table above carries the record.
   "Smaller" held at planning time and holds less well now: the repo had grown from 68
   tracked `.py` to 99 and from one body of work to two. It still confirmed the recipe, and the
   correction it contributed is the one most worth carrying to steps 4 and 5 — that the thing to
   grep for is a `Path(__file__).resolve().parents[N]` walk conflating the two roots, not a
   cwd-relative string literal.
3. **Programme Phase 0** — must precede both remaining plans. **DONE 2026-08-19, all three
   steps**: `33b3ee2` in book-of-job, `98021de` in codex-index-aleppo, `f56831c` in
   codex-index-cam1753. Fourteen of the sixteen files are one committed blob; `check_all.py` and
   `check_word_finding.py` stay per-repo permanently, on Ben's decision that day. **Steps 4 and 5
   are unblocked, and nothing is owed in advance** — Phase 0 was the only gate in front of them.
   Read the Phase 0 section's three 0b findings anyway: **one changes how a verification run is
   read** (no repo's `check_all.py` runs in its own venv, so a failure there is the baseline rather
   than the move), and **two are decisions each step has to make** (book-of-job has none of the
   data its two word-image packages need, and those two packages are partly forked from each other
   inside book-of-job).
4. **book-of-job** — the largest, and the one whose Python is not under a `py/` at all. **DONE
   2026-08-22, every phase; this step is complete and the codex-index trio is the only step of
   the programme left.** **Phases 0,
   1 and 3 are DONE, 2026-08-19**, gate and all: Ben answered Phase 0's three questions the same
   day, both fork families are reconciled, Phase 1 landed as `45f8853` there, and **Phase 3 landed
   as `ef8e384` here — 243 files, all 701 artifacts byte-identical, the oracle silent on the first
   run from this repo and on every run since.** **Phase 4 is DONE too, 2026-08-21** — `a846585`
   there and `cff95f7` here, **book-of-job holding zero Python**, 1103 tracked files → 786, the 701
   artifacts still byte-identical and the oracle still silent. Ben was asked first and chose to
   **delete** the 40 orphaned UXLC data files. **Phase 6 is DONE as well, 2026-08-22** — one commit
   here and none in book-of-job, both halves of its prescription nil (both breadcrumb greps 0, and
   none of the 29 `#NN` sites in the 268 pre-move `.py` a citation of any tracker), so what it
   actually delivered is `CLAUDE.md`'s section becoming **"Five issue trackers"**, book-of-job
   keeping 61 issues numbered 1–61. **Phase 7 is DONE as well, 2026-08-22** — items 2–6, item 1
   having fired inside Phase 4, one commit here and none in book-of-job. Item 5's target was a
   **153 MB** venv that no tracked file names, and it needed no documentation edit first, as
   Phase 6 predicted; what it did hold was **1,722 untracked `.py`**, against wlc-utils' 789 and
   UXLC-utils' 832, and the black sweep skipped every one because `run_black.py` asks whether a
   repo tracks any `.py` before it looks for a black to run. **Item 6 is what this step hands
   the trio**: five stale citations of book-of-job's Python, of which the prescribed
   `<repo>/py` grep would have found one, because that repo's Python sat at its ROOT and because
   three of the five name a bare module filename with the repo left to the surrounding prose.
   **Grep for the repo's NAME across all 26 clones, MAM-private included, and classify by hand.**
   Three of the five are in MAM-private and were reported rather than fixed; the fourth is one
   blob across this repo and codex-index-aleppo, so **the trio plan is where it gets fixed, both
   copies at once**; the fifth is in UXLC-utils' own `doc/`. All five
   items Phase 1 handed Phase 3 are settled, and
   items Phase 1 handed Phase 3 are settled, and
   two of them differently from how this item predicted. **The `path_to_uxlc` parameter was NOT
   added**: all 39 UXLC XML are one blob across the three repos and `lci_recs.json` differs from
   UXLC-utils' copy in one header line whose `body` is identical, so `prep()` takes no arguments and
   `uxlc_misc`/`uxlc_lci` were not touched — putting the parameter back would have re-imported the
   only content difference Phase 0's reconciliation dropped. **`py_cam1753_word_image/page.py` was
   left alone**, on this plan's own "both repos at once or not at all", because the three
   directories its `ROOT` names are absent from book-of-job and from here, so the walk was inert
   before the move and is inert after it; `py_ac_word_image_helper/flat_index.py` was left alone
   too and the move **repairs** it, `parent.parent.parent` landing on the repo root exactly as in
   codex-index-aleppo. `test_h_dot_below_nfc.py` folded in as a fourth `_Scope`, needing no
   `_BINARY_EXTENSIONS` addition. The venv got `pyspellchecker` **and `numpy`**, the second
   unpredicted and needed by both crop editors; `matplotlib`, which book-of-job's
   `requirements.txt` also names, is imported by nothing in that repo. And `WriteCtx.path` took the
   vendored `mb_cmn.file_io` without change, as predicted. **Everything Phase 4 was told it owed is
   discharged**: Ben chose to delete the 40 UXLC data files, `quirks-BHQ.txt` and the spelling
   dictionary went with the `.py` so no one-file directory survived, book-of-job's `CLAUDE.md` says
   the checks run from MAM-basics, and the NFC floor of 30 holds against a measured 35 rather than
   the assumed 42. **The `parents[2]` question is now moot for book-of-job** — the tree holding the
   wrong copy of `mb_cmn/provenance.py` is deleted, so what stands open is only whether this repo's
   copy should walk to `.git` for the *other* repos that hold it. Phases 1, 3 and 4 all declined to
   pick; do not let a later phase pick it silently. **Two root-level files were orphaned by the
   deletion and neither is a `.py`** — `book-of-job.code-workspace`, whose five launch
   configurations name deleted scripts, and `requirements.txt`, whose five packages hydrate a
   `.venv` Phase 7 item 5 deletes. **Ben chose to delete both, 2026-08-21**, `aa20c61` there and
   the commit carrying this record here. **At the trio, sweep the repo root for files whose subject is the interpreter
   rather than the code.** Five things these two phases established are worth having before the trio
   runs, not only here: the oracle rewrites **183** of the 701 artifacts so **518 have no generator
   at all**; each repo's tracked `requirements.txt` has to be installed before its entry points can
   be characterized, and installing book-of-job's made `check_all.py` run there for the first time;
   **`git status --porcelain` cannot be the verification here**, the byte comparison against
   `git cat-file blob HEAD:<path>` being what replaces it; **check the depth of a vendored
   `mb_cmn/`, not only its presence**, since `paths.repo_root()`'s `parents[2]` is right two levels
   down and wrong at a repo root; and **a file being one blob across two repos does not make a
   depth-counting walk in it right in both** — sweep the reconciled `py_ac_word_image_helper/` and
   `py_cam1753_word_image/` packages for `parents[`/`.parent.parent` outright, not only the files
   that had diverged.
5. **codex-index trio** — last, and as one plan, because the three share a shape, share the
   reconciled family, and share a vendoring problem.

**One repo at a time, and one phase at a time within it.** Each plan's verification asserts that
MAM-basics' `git status --porcelain` is empty, which a concurrent plan would pollute — the same
reason the wlc-utils plan forbade running its Phases 0 and 1 together.

---

## Cross-cutting findings

**1. Entry-point names collide at MAM-basics' `py/` top level.** MAM-basics already tracks 34
`main_*.py` there. Colliding names among the repos in scope:

| Name | Held by |
|---|---|
| `main_0_mega.py` | MAM-basics **and** UXLC-utils |
| `main_test.py` | MAM-basics, UXLC-utils **and** holman-ketiv-qere |
| `main_update_vendored_files.py` | UXLC-utils, holman-ketiv-qere **and** codex-index-leningrad |
| `main_make_wikisource_page.py` | codex-index-aleppo **and** codex-index-leningrad |
| `main_find_word_in_*_images.py` | codex-index-aleppo, codex-index-cam1753 (differing stems, same job) |

`main_test.py` and `main_update_vendored_files.py` resolve by disappearing: one merged test runner
serves the whole tree, and a repo with no vendored `mb_*` left needs no refresh script.
`main_0_mega.py` and `main_make_wikisource_page.py` need real names, decided in their own plans.

**2. codex-index-leningrad vendors seventeen of UXLC-utils' own `.py`.** Its
`UXLC-utils-sparse/py/` holds `main_uxlc_estimate_atom_loc.py`, five `uxlc_lci/` modules and
eleven `uxlc_misc/` modules, refreshed by codex-index-leningrad's own
`main_update_vendored_files.py` from the sibling `../UXLC-utils`. **The vendoring inventory does
not record this**: it lists only `mb_cmn` rows for that repo, because the scan looks for
MAM-basics packages. Evacuating UXLC-utils' Python breaks that script's source. Handled in
UXLC-utils' plan; flagged here because the inventory alone will not reveal it, and because it is
evidence that a second such relation may exist somewhere the scan cannot see.

**That last clause came true twice, and the blind spot is bigger than "a loose file at the top of
`py/`."** UXLC-utils' Phase 7 item 5 found holman-ketiv-qere's `py/uxlc_paths.py` byte-identical to
this repo's and absent from the inventory, and reported it as the loose-file case: a scan looking for
`mb_*` packages cannot see a single file. holman's Phase 1 then found, 2026-08-18, that **two whole
packages are invisible on the same tracker for the same reason** — `py/uxlc_lci/` (4 files) and
`py/uxlc_misc/` (5), both named in that repo's `_VENDORED_PACKAGES` and both synced from
`../MAM-basics`. So the mechanism is not "loose files escape" but **`in/vendoring_policy.json`'s
`pkg_scan_roots` is a hand-maintained list with no cross-check against what the destination repo's
own sync script names**, exactly the failure mode a hand-maintained test registry has. **The check
worth running per repo before its Phase 4 is to read that repo's `main_update_vendored_files.py` and
compare its `_VENDORED_PACKAGES` and `_VENDORED_FILES` against the inventory's rows** — not to trust
the inventory, and not to grep for `mb_*`. For holman it cost only an undercount, 26 against 37, all
37 identical; in book-of-job and the trio the copies have **diverged**, so there the same blind spot
would destroy a local edit.

**Resolved 2026-08-03 in UXLC-utils' Phase 5: the `py/` half was dropped, not repointed**
(`d5195e3` in codex-index-leningrad, `748ee2f` in UXLC-utils). What settled it is worth carrying:
**nothing in the consumer imported the seventeen**, and their one entry point could not run there
anyway — the sparse copy never carried `mb_cmn`, so it raised `ModuleNotFoundError` long before
Phase 4. Three findings that will recur at the next downstream consumer:

- **A vendored copy can be dead without anyone noticing, and "it works today" is worth
  checking rather than assuming.** Both plans described this one as working, on the strength of a
  sync script that refreshed it. Run the consumer's entry point before deciding what its copy is
  worth.
- **The broken script failed loudly but partially.** `copy_by_intersection(strict=True)` raises on
  the first missing source file, and it iterates in sorted order — so `data/` and `in/` were
  copied and `provenance.md` was never written. Expect a half-sync, not a no-op.
- **The consumer's prose named the moved code in four files, none of which imported it** —
  `README.md`, `.github/copilot-instructions.md`, `.vscode/launch.json` and a test module's scope
  docstring. **Grep a consumer for the vendored directory's name**, not for the module names.

**3. Every repo in scope uses cwd-relative repo-internal paths**, which is the same problem
wlc-utils' Phase 1 solved. Representative hits: UXLC-utils `py/clc/clc_render.py:26`
`_OUT_DIR = "gh-pages/clc"` and `py/clc/clc_changes.py:27` `_CHANGES_DIR = "in/UXLC-misc"`;
book-of-job `pyauthor/job1_full_list_details.py:15` `out_dir = f"gh-pages/{D1D_DIR}"`;
holman-ketiv-qere `py/main_just_render_table.py:20` `Path("gh-pages/table_data_findings.html")`;
codex-index-aleppo `aleppo-wiki/py/mam_book_names.py:114` `f"in/mam-ws/{basename}.json"`. Each is
a path that resolves correctly only while the process runs from that repo's root, which is exactly
what stops being true. **`repo_root()` splitting into a CODE root and a DATA root is the organizing
idea of every plan here, as it was of the wlc-utils one** — read that plan's section of that name
before starting any of these.

Three things UXLC-utils' Phase 1 learned about this, all likely to recur:

- **A grep for leading `"in/` and friends undercounts badly.** Six known offenders there turned
  out to be 26 modules, because the same path also arrives as an f-string, as a module constant
  another module imports, as a `Path("...")` binding, and as a
  `Path(__file__).resolve().parent.parent` walk that is cwd-independent already but still
  conflates the two roots. Grep for the directory *names* anywhere in the line, not for a leading
  quote.
- **`PurePosixPath(...).name` breaks the moment a path goes absolute on Windows** — it sees no
  separator in a backslashed path and returns the whole string. Three modules used it to derive a
  link's `href` from an output path, so the failure is a wrong artifact rather than a crash.
  `git grep -n PurePosixPath` in each repo before starting.
- **`mb_cmn/paths.py` may not be in the destination repo's vendored subset**, in which case the
  accessor Phase 2 is said to have already provided is not reachable from the code that needs it.
  Finding 3 above assumes it is; check.

Five more from UXLC-utils' **Phase 3**, all of which will recur:

- **A file inside a vendored `mb_*/` directory need not be a vendored copy.** UXLC-utils'
  `py/mb_cmn/mb_cmn_bib_locales.py` is MAM-basics' `bib_locales.py` plus six local aliases,
  absent from the inventory's row for that repo and excluded from its own sync script by name.
  Copied in as-is it would have put a 636-line near-duplicate of a native module inside
  `py/mb_cmn/` — the two-module-objects failure the global `CLAUDE.md` describes, reached without
  any `sys.path` line. **`cmp` every file in a vendored directory against MAM-basics' own and
  treat "no counterpart here" as a finding, not as a new file to copy.**
- **Grep for cross-references to a renamed entry point by MODULE NAME, not by path.**
  UXLC-utils' `main_uxlc_download_changes.py` ended with `import main_0_mega; main_0_mega.main()`,
  a name that exists in both repos — so after the move it silently ran MAM-basics' tree-wide
  pipeline instead of the UXLC one. It succeeds; nothing fails. Any repo whose mega gets renamed
  has this.
- **A repo's copy of `nfc_h_dot_below_test.py` must merge, not move.** It finds its repo root by
  `git rev-parse` from its own file's location, so under MAM-basics' `py/tests/` it scans
  MAM-basics — a second, weaker pass over this tree, and a failing one. Add a `_Scope` to
  `py/tests/test_h_dot_below_nfc.py` instead; it now carries three.
- **Budget for this repo's lints scanning the arrived code.** UXLC-utils' 77 files produced 68
  genuine findings — 15 prose-convention and 53 transliteration — of which roughly half were our
  own wording to fix and half external vocabulary needing a `# translit-ok` pragma. Plus two
  ruff findings, in a repo that runs no linter. This was the largest single piece of Phase 3's
  work, larger than the copy itself. **And the traffic runs both ways**: UXLC-utils' arriving
  `source_hygiene` checker found eight orphan combining marks in *MAM-basics'* own tree.
- **Count what a run actually rewrites, not what it leaves clean.** An empty `git status` across
  an artifact tree proves nothing about files no program writes. Snapshot mtimes before the run:
  of UXLC-utils' 214 tracked artifacts only **127** were rewritten, the other 87 being static
  assets and one hand-authored report filed under `out/`. Phase 1's write-up had claimed all of
  them regenerated.

**3a. Live downloads are untestable and that is deferred, not owed.** tanach.us' `robots.txt`
disallows both paths UXLC-utils' two downloaders need, so Phase 3 there could not run either;
`polite_download` is configured `obey_robots_txt=True` and that was not worked around. **Ben's
decision, 2026-08-02: testing anything that requires a live download is deferred, and does not
block completion of this programme.** The loop closes at MAM-basics **#214**, which waits on a
separate task drafting an email to Chris Kimball, tanach.us' maintainer. The account is in
UXLC-utils' plan, Phase 3.

Whether the same exposure recurs was checked on 2026-08-03, by grepping the other four repos in
scope for `polite_download`, `robots`, `requests`, `urlopen` and `urllib`. **It does not — the
robots block is specific to `polite_download` against tanach.us, and `polite_download` is used
only in MAM-basics and UXLC-utils.** What the other repos do have, so nobody re-checks:

| Repo | Downloader | Shape |
|---|---|---|
| book-of-job | **none for source data** | its one network path is `check_html_syntax_and_sanity.py --w3c`, which POSTs generated HTML to `validator.w3.org/nu` behind an opt-in flag. `mb_cmn/uxlc_change_url.py` composes a tanach.us href for a link and downloads nothing. |
| codex-index-aleppo | `py/download_aleppo_pages.py` | page images from archive.org by raw `urlopen`; run by hand, and three modules only print "Run download_aleppo_pages.py" when the images are absent |
| codex-index-cam1753 | `download_cam1753_spreads.py` | the same shape against archive.org, and **nothing in that repo calls it** |
| codex-index-leningrad | **none** | `lenin-wiki/py/image_urls.py` composes sefaria and archive.org hrefs for links |
| holman-ketiv-qere | **none** | |

So the two archive.org downloaders cannot raise `RobotsDisallowedError` — they consult no
`robots.txt` at all. **They are nevertheless as unexercised as the tanach.us pair**, and the
finding that matters transfers unchanged: a downloader writing into the wrong repo's `in/` is the
failure the two-roots work exists to prevent, and composing the right path is not the same as
writing to it. Each affected plan should say plainly which of its downloaders it has and has not
run, rather than letting an empty `git status` stand in for the claim.

Four more from UXLC-utils' **Phase 4**, all of which will recur:

- **The `in/vendoring_policy.json` edit belongs to the DELETING phase, not to bookkeeping.** Every
  plan here files it under its own Phase 7, on the wlc-utils precedent — but wlc-utils' Phase 7
  also added `py/tests/test_vendoring_policy_paths.py`, whose whole job is to fire the moment a
  configured `pkg_scan_roots` directory vanishes. It duly failed inside UXLC-utils' Phase 4
  verification run, the first red suite of the programme, and the entry had to come out before the
  phase could pass. **Move the item into each remaining plan's deleting phase**, and regenerate
  `doc/vendoring-inventory.md` and the three `out/vendoring_*` artifacts in the same commit.
  Expect the suite's pass count to drop by exactly the number of parametrize cases that repo's
  entry contributed — three for UXLC-utils, so 916 → 913.
- **The tracked deletion is bigger than the `.py` count, and the surplus is repo-specific.**
  UXLC-utils' 102 `.py` came to 110 tracked files: plus `requirements.txt`, the two
  `_provenance.md` vendoring breadcrumbs sitting *inside* the vendored packages, `.vscode/`
  (debugpy launches and a venv auto-approve), and `.github/copilot-instructions.md`, the Copilot
  twin of `CLAUDE.md` and ~95% Python conventions. **Inventory each repo's non-`.py` Python
  scaffolding before quoting a deletion count to Ben.** And `git rm` leaves the untracked half
  behind — 217 `__pycache__`/`.pytest_cache` files here — so delete the source root outright
  afterwards, or the repo still looks like it has Python.
- **A repo's own `doc/` links at its own `py/`, and those links go dangling.** `doc/clc-design.md`
  stays in UXLC-utils by design, and 35 of its markdown links name 19 `py/…` paths this phase
  deleted. Ben's call was one sentence in `CLAUDE.md` — every `py/…` path in `doc/` now means
  `../MAM-basics/py/…` — rather than 35 edits riding along on a deletion commit, with the one file
  that did *not* move called out by name. **Grep each repo's `doc/` for `](py/` before the
  deleting phase**, decide which way, and say so in the plan rather than discovering it mid-commit.
- **Do not move a convention into MAM-basics' `CLAUDE.md` that MAM-basics already practices.**
  Each plan says the evacuated repo's conventions "move to MAM-basics' `CLAUDE.md` with the code
  they govern". For UXLC-utils that was true of none of them: the MAM-reading rule is already how
  thirteen modules here read MAM, the vendoring rules have no meaning in the vendoring *source*,
  and the entry-point and `sys.path` rules are already in this repo's `CLAUDE.md`. **Check what is
  already there and already practised before copying prose across**; a wholesale restoration is
  the failure mode Ben's standing note on this file's minimality warns about.

**4. book-of-job has no `py/`, so its modules land at MAM-basics' `py/` top level.** Sixteen
scripts sit at its repo root and seven more in a `py/` that is a package of page-rendering helpers
rather than a source root. Two of those seven are `hebrew_letter_words.py` and
`uni_heb_char_classes.py`; MAM-basics already has `mb_misc/hebrew_letter_words.py`. Landing
book-of-job's copy as a **top-level** `hebrew_letter_words` alongside `mb_misc.hebrew_letter_words`
produces two module objects for one name — the failure mode the global `CLAUDE.md` describes under
the `sys.path` ban, reached here without any `sys.path` line at all.

**5. Four of the six in scope were committed to on 2026-08-02, and one has not moved since
2026-04-27.** book-of-job, UXLC-utils, holman-ketiv-qere and codex-index-aleppo are live;
codex-index-leningrad last moved 2026-07-27 and codex-index-cam1753 is dormant. **Dormancy is not
a reason to treat a repo differently** — see the codex-index trio's plan, where cam1753 is in on
exactly the same terms as the other two. **Files change under you mid-session** — Ben edits in
parallel, and wlc-utils moved under the wlc-utils plan's own final session. Re-check `git status`
and `git log` before staging, and commit by hunk.

---

## Appendix A — MAM-simple: nothing to evacuate

MAM-simple tracks 47 `.py`, which would put it fifth in the scale table. **43 of them are already
generated by MAM-basics** — `py-examples/mb_cmn` (18), `py-examples/mb_misc` (14),
`py-examples/mb_sefaria` (7) and `py-examples/osis` (4), all recorded `identical` /
`copy_script` / `generated` in `doc/vendoring-inventory.md`. They are the published artifact of
that repo, not code maintained there, and evacuating them would delete the product.

The other four are `py/tests/test_h_dot_below_nfc.py` and the three
`py-examples/main_*_example.py`, which the inventory's "Intentionally non-vendored" table already
declares are maintained in MAM-simple on purpose. **This repo is closed for this programme.** Its
`.py` count should not be read as Python awaiting evacuation, and a future audit that reads it that
way should be pointed here.

## Appendix B — diffable-pointed-hebrew: left alone, with one loose end

Nine tracked `.py`, of which **eight are a vendored `mb_cmn`** and one is the repo's entire reason
to exist, `diffable-pointed-hebrew.py` at the root. Nineteen tracked files in total, no `out/`, no
`gh-pages/`, no Pages workflow, dormant since 2026-04-27.

**Out of scope, on the same principle as MAM-simple. Ben, 2026-08-02:** a thin script — or a
handful of them — that exists only in a non-MAM-basics repo, combined with vendored files, is a
repo to leave alone, *"as long as its vendoring is all nicely set up like vendoring in other
repos"*. That is the criterion, and it is a better one than the draft's "is this worth the
trouble", because it names the property that makes a small Python repo cheap rather than guessing
at effort.

**This repo does not currently meet that criterion, and that is the loose end.** Its eight
`mb_cmn` files are recorded **`DIFFERS`** in `doc/vendoring-inventory.md`, with mechanism
`unknown` — meaning no copy script has ever refreshed them and nobody has looked at how far they
have drifted. Compare holman-ketiv-qere, whose copies are `identical` and `copy_script`: that is
what "nicely set up" looks like.

So the work here is not an evacuation but a **vendoring repair**, and it is small:

1. Diff the eight against MAM-basics' current `py/mb_cmn/` and classify each difference — a fix
   that belongs upstream, a local adaptation, or drift to drop.
2. Give the repo a `main_update_vendored_files.py` copying by intersection, matching the four
   repos that already have one.
3. Update `in/vendoring_policy.json` to declare the mechanism, and regenerate the inventory. The
   row should then read `identical` / `copy_script`.

Worth doing on its own account whichever way the scope question had gone: a divergence nobody has
looked at is a bug of unknown size. It is not blocked by anything in this programme and does not
block anything in it.

---

## How to run this programme

Same discipline as the wlc-utils plan, and for the same reason: **no live session stays open, and
no session needs to remember anything from the one before it.**

Each session reads the relevant plan, does exactly **one** phase, verifies it, and writes the
result back into that plan's Status table — state, date, commit shas — and marks the phase heading
`— DONE <date>`, recording the numbers actually measured and anything the plan did not predict.
Then it updates this file's Status table, and spawns a task chip for the next phase quoting the
plan's absolute path. A phase whose result is not written back cannot be judged by the next
session.

**Run the test suite and every generator from each repo's own main checkout, never from a
worktree.** The wlc-utils plan's Phase 7 cost a full pass to this: from
`.claude/worktrees/<name>`, MAM-basics' suite gives 12 failures that are not real, and generators
are worse than broken — they succeed and write the worktree's directory name into the provenance
breadcrumbs.
