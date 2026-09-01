# Findings of the 2026-08-22 review of the work since 2026-08-18

State: acted on 2026-08-22

Filed as [#232](https://github.com/bdenckla/MAM-basics/issues/232), which is a thin pointer to
this doc. The review covered **every clone directly under `~/GitRepos`** — committed work from
the 2026-08-18 review's anchors (MAM-basics `6a6e600`, MAM-private `a1b489e`, UXLC-utils
`9be1431`, holman-ketiv-qere `637237b`; elsewhere the previous review's filing time,
2026-08-18T12:56 local) through 2026-08-22 ~15:45 local, when this review started. That is
**90 commits across 8 repos with activity**: MAM-basics 59 (`6a6e600..b37bdb4`), holman-ketiv-qere
7, book-of-job 6, codex-index-aleppo 6, MAM-private 5, codex-index-leningrad 3, UXLC-utils 2,
codex-index-cam1753 2 — re-measurable per repo with `git log <anchor>..<head> --oneline`, or
`git log --since=2026-08-18T12:56 --oneline` where no anchor was recorded. Twelve clones were
quiet (ArtScroll, MAM-OSIS, MAM-for-Sefaria, MAM-parsed, MAM-simple, MAM-with-doc,
diffable-pointed-hebrew, document-index, github-misc, hbofonts, phonetic-hbo, wlc-utils). Every
tracker was checked for in-window activity (`gh issue list --state all --search
"updated:>=2026-08-18"`), and six had some — **33 issues touched**: MAM-basics 6 (#231, #228,
#215, #185, #4, #3), wlc-utils 9, al-hatorah 9, masorah-books 4, codex-index-cam1753 4,
holman-ketiv-qere 1. UXLC-utils, book-of-job, MAM-private, breuer-cos, mgketer, trope,
codex-index-aleppo, codex-index-leningrad, wlc-utils-private, phonetic-hbo and github-misc were
silent.

The review ran in four agent streams plus the main session: the holman-ketiv-qere evacuation
(the verdict the previous review owed); the book-of-job evacuation; the codex-index trio
evacuation; and the tracker activity with MAM-private. The main session measured MAM-basics' tree
health and the message hygiene of all 90 commits.

Anchors: HEADs at review start were MAM-basics `b37bdb4`, MAM-private `8f30d37`, UXLC-utils
`c8db329`, holman-ketiv-qere `6b0bb63`, book-of-job `aa20c61`, codex-index-aleppo `a50f40e`,
codex-index-cam1753 `7e5ca23`, codex-index-leningrad `2abd7f6`. **One session was live in
MAM-basics and the codex-index repos throughout — the trio evacuation session — and a second in
MAM-private**, and between them they landed **six commits during the review**: MAM-basics `fe6cef2`
(cam1753 Phase 3) and `09d68c5` (cam1753 Phase 4), codex-index-aleppo `2bdcfde`,
codex-index-cam1753 `a9c3abd`, MAM-private `a225faa` and `555ed14`. Those six get no verdict.
So this is a review of **committed work only**, and the one standing limitation of the series
applies again: no regeneration-and-diff of tracked outputs was run in place (a live session makes
in-place regeneration unsafe) — though the holman stream ran the full oracle against a scratch copy
of that repo, which is the first time the series has had a regeneration oracle at all.
Consequently **the codex-index trio evacuation gets a verdict on its Phases 0–4 as committed at
`b37bdb4` and none on its Phases 6 and 7**, which the next review owes it.

## The verdict the previous review owed: the holman-ketiv-qere evacuation is sound

Every substantive figure in `doc/PLAN-evacuate-python-from-holman-ketiv-qere.md` re-derives, the
moved code is intact, the deleted code was byte-identical to this repo's originals, and the
artifacts regenerate from MAM-basics. The exact re-derivations, each against the named oracle:

- Baselines at `637237b`: 454 tracked, 99 `.py`, 16,416 `.py` lines — `git ls-tree -r 637237b
  --name-only | wc -l`, grep counts, `git show <c>:<f> | wc -l` summed. Lines 16,640 at `6b10259`
  and 16,637 at `9e290ce` and `15824d4`, exact, including Phase 4's correction of Phase 3's figure.
- The six surviving trees = 335 (gh-pages 300, emails 26, docs-not-served 4, out 2, data 2, io 1;
  `ls-tree -z` is needed, since two gh-pages names carry spaces), 348 tracked and 0 `.py` at
  `0890cb8`, `ce6dd7d` and `6b0bb63`.
- **Nothing lost, at blob level.** Of the 60 files `1be01b5` added here, 23 blobs are identical
  to holman's at `15824d4` under the `python_modules/` → `hkq_cmn/` mapping, and the 37 that
  differ reduce, after removing the rename's own lines, to exactly the three edits the plan names
  (a `# prose-ok` pragma, `mahpakh` → `mahapakh`, and `hkq_paths.py`'s body). The 37 pure
  deletions are byte-identical to MAM-basics at `b72f785~1`, 37 of 37; 100 = 37 + 2 + 61, exact.
- ruff: 13 findings at `6b10259`, in the files `9e290ce`'s message names; **0 at `9e290ce`** —
  `git archive` of each tree into the scratchpad, `ruff check --config ruff.toml`.
- Test arithmetic: the seven copied modules collect 45 at HEAD; holman's own 51 = 45 + the 6
  `def test_` of its shorter NFC copy; `test_vendoring_policy_paths.py` yields 3 tests per
  two-root entry, consistent with 28 → 25 and 950 → 947.
- `b72f785`: the policy diff is only the holman entry, the inventory diff only the two holman rows,
  `23 rows, 155 files` → `21 rows, 128 files`; no `holman` in either file at HEAD.
- Tracker: 81 issues, 1–81, no gaps, 60 open; 77 of 81 titled `row NN …`;
  `io/table_row_github_issues.json` has 77 rows; `REPO_OWNER`/`REPO_NAME` in
  `py/hkq_cmn/table_row_github_issues.py` still name `bdenckla/holman-ketiv-qere`.
- The breadcrumb flip: both `data/*.json` `note` fields equal the constants in
  `py/main_estimate_uxlc_locations.py`; `git grep` for a `py/` path over holman's `data`,
  `docs-not-served` and `io` returns nothing. Of 26 distinct `MAM-basics/…` paths holman's prose
  cites, 24 exist by `git ls-files`; the two that do not are `.venv/Scripts/python.exe` (untracked
  by design) and the README's explicit `py/hkq_cmn/foo.py` example.
- **The full oracle, with no repo written to**: holman's tree (minus `.git`, plus its `.novc/eml/`)
  was copied to the scratchpad, `REPO_HOLMAN_KETIV_QERE_DIR` pointed at the copy, and all six
  generators run from MAM-basics on MAM-basics' interpreter. All exit 0, `row_count` 77, MAM-basics'
  tree untouched, and `diff -rq` against holman's committed tree differs in **2 files of 175** —
  finding 3 below, which is drift from a later UXLC-utils commit and not an evacuation defect.
- MAM-private `e8fd4ae`'s two targets exist here (`py/hkq_cmn/mam_plus_verse_data.py`,
  `py/hkq_cmn/qere_projection.py`). `5f229ad` is not holman fallout: it repoints masorah-books'
  `doc/issues/7-fill-in-plan.md` after MAM-private's own R.2 move, and all six paths it names exist.

## What else the review verified and found sound

**The book-of-job evacuation (Phases 0–7, 2026-08-19 to 2026-08-22) verifies from both sides.**
`git diff-tree -r --diff-filter=D a846585` (book-of-job) against `--diff-filter=A ef8e384` (here),
matched through the four package renames: 317 deleted = 268 `.py` + 40 UXLC data + 7 docs +
2 loose; 243 added = 241 `.py` + 2. Of the 243 pairs, **133 blob-identical, 110 differing,
0 missing, 0 added without a source**; 99 of the 110 differ only by the import-prefix rewrite,
and the other 11 are exactly the edits Phase 3 records. The 17 `mb_cmn/` deletions are
blob-identical to `py/mb_cmn/` here; all 39 `py_uxlc_loc/UXLC/*.xml` are one blob with
`in/UXLC-39/` here and in UXLC-utils. Tracked files 1,103 → 786 (`a846585`) → 784 (`aa20c61`,
= HEAD), 0 `.py`. The 701 published artifacts decompose as CLAUDE.md states (694 `gh-pages` +
7 `out`; 515 png = 160 × 3 + 30 + 5 loose; 518 = 515 + 2 + 1). The lci merge (`4d1ad89` /
`2979507`) lands 979 → 982 records in all three homes with bodies equal. `a585cb6` and `cff95f7`
take the inventory 21 rows / 128 files → 20 / 129 → 18 / 112 with zero `book-of-job` left in policy
or inventory. All seven `doc/boj-*.md` are tracked and every `py/…` and `../book-of-job/…` path
they cite resolves. The tracker claims hold: 61 issues, 1–61, no gaps, 19 open; the four quoted
titles exact; `git grep -nIE '#[0-9]+'` over book-of-job's whole tracked tree returns nothing;
the 29 `#`-plus-digit sites at `45f8853` decompose as 24 + 4 + 1. `90487af`'s message is right
that `check_keys.py` had been tracked since `13ee3d9`. The Pages workflow uploads `gh-pages/` only
and needs no Python.

**The codex-index trio's Phases 0–4, as committed at `b37bdb4`, verify.** Phase 0's three claims
re-establish: the dead generator's four `"aleppo/..."` literals date from `9025037` (2026-03-28)
and no commit but a black run and the LF+NFC migration touched the tree since; `py\check_ac_word_finding.py`
reports `PASS: 0 / FAIL: 160 / TOTAL: 160` with every mismatch a `col` clause, the column-ID
migration being `eb4bcaf` (2026-03-14); cam1753's `check_line_breaks.py:654` wrote with
`write_text(html, encoding="utf-8")` where aleppo's copy had `newline=""`. The Phase 1 headline
`2ddf667` corrected to — 19 root walks and 13 literals — re-derives from the three commits' `-U0`
removed lines (12 + 4, 7 + 5, 0 + 4), and the post-phase baselines (228/73/177 tracked, 50/21/23
`.py`, 8,584/2,572/5,579 lines) reproduce exactly. Phase 3 for leningrad: 9 `.py` added, and of
the eleven dissolved copies only `hebrew_letters.py` was byte-identical, exactly as the record's
table says. Phase 3 for aleppo: 30 `.py` added = 29 moved + the new `repo_scopes.py`, and the lint
union (`repo_scopes.code_paths()`) re-runs at **419 / 278** from a scratch extraction. Phase 4:
codex-index-aleppo and -leningrad track **0 `.py`** at HEAD; 20 of the 50 aleppo deletions are
byte-identical to a file here and the other 30 differ only by CRLF normalization, usage-docstring
repoints, renamed imports or the recorded edits. The NFC scopes re-count through the test's own
`_tracked_files_in_scope`: leningrad 8 (`2abd7f6` was right), aleppo 28 (`fde301d` was right),
book-of-job 33, holman 45, UXLC 11, MAM-basics 1,328. After `e2903be`'s reversal, no sentence
still carries the images-stay decision unmarked — the only residue is the paragraph framed as "the
rejected version". `7ddd6da` touched `MAM-basics.code-workspace` only (8 → 6 folders), so
`all-repos.code-workspace` still lists 20 and the black sweep is unaffected. `b37bdb4`'s whole diff
is six lines in `py/py_ac_loc/mam_xml_verses.py`; `MAM-XML/Ps.xml` carries 7 `spi-invnun` and
`Num.xml` 2. `a50f40e`'s report parses as 35 pages, 93 issues, 18,377 bytes against 4,771 for
one page before. cam1753 at `7e5ca23`: `git ls-files --eol` is 108 `i/lf` and 44 `i/-text`,
nothing else.

**The 2026-08-19 closure burst was one Ben-approved batch, and every closure's justification
checks out.** The oracle is `MAM-private/.novc/issue-sweep-2026-08-18/{HANDOFF.md,AGENT_BRIEF.md,
approved.json,apply_verdicts.py}` and that session's transcript: three read-only triage agents
(wlc-utils 25 issues, al-hatorah 37, masorah-books 12) wrote verdicts under a closed vocabulary
("when torn, KEEP"); the main session then put 11 questions to Ben, who took the recommended option
on every one; `apply_verdicts.py --go` ran at 15:47:46Z. `approved.json` names exactly the 18
issues in the burst — 11 closes, 7 comments — and masorah-books#18, which Ben chose to skip, got
nothing. Every one of the 11 closes cites a commit, path or issue that exists and covers it
(wlc-utils#89's `7033f94` and the `get_flattened_data()` call; wlc-utils#86's
`crossing_a_chanted_word_boundary` at 0 in all three corpora; wlc-utils#76's single `# prose-ok`
"word division"; al-hatorah#120's `עֲ֭טִנָיו` in `in/latest/Iyyov/21.txt` v24 and no Jb21:24 row
in `a08`; the four al-hatorah supersessions' targets #109, #112, #113, #118 all closed in
February 2025 and naming the places). The seven progress comments' figures re-derive too
(wlc-utils#81's 150 / 16 / 81 and 164 / 67; masorah-books#6's `itm.json` 13,868 / 515 / 14,383).
The earlier 2026-08-18 cluster — #231, #228, codex-index-cam1753 #11/#4/#2/#1, holman-ketiv-qere#3
— likewise cites commits and paths that exist. #215's 15:10Z comment is the write-up of the fix
that closed it at 14:31Z, and every figure in it matches the tracked JSON.

**MAM-private's window is clean.** Modes all 100644, no venv or cache paths, HEAD = `origin/main`
with fast-forward throughout. The unpushed state the main session observed at the start (`9db65d8`
alone, ahead by 1) was the live session's ordinary cadence: `8f30d37` landed three minutes later
and both were pushed within ten. **`9db65d8`'s vendoring of tropetransmission's `xml/` is verbatim
modulo line endings, and `8f30d37` is right to record both hashes**: a pinned re-fetch of the
three files from `github.com/jes5199/tropetransmission` at `a8b20c0` gives exactly the upstream
sha256s and byte counts `PROVENANCE.md` records (1,037,925 / 350,130 / 6,374), `git show HEAD:<path>
| sha256sum` gives exactly the stored ones, and `tr -d '\r'` of the upstream bytes hashes to the
stored values. The re-measured figures (28,727 lines, 45 `TROPEDEF`, 30 names, 10,740 `NOTE`,
TYPE split Torah 22 / Haftarah 15 / HiHoliday 4 / TorahBlessing 2 / HaftarahBlessing 1 /
Tehillim 1) all match. `license: null` upstream is confirmed via `gh api`, and the provenance
note's "must not move to a public repo" rule follows from it.

**MAM-basics' tree is healthy and the suite chain closes.** Re-measured for this review at
`b37bdb4`: **945 passed, 5 skipped, 59 subtests** (`.venv/Scripts/python.exe py/main_test.py`,
145s), all five skips the edition-transcription semantic channel; collect-only 950 = 945 + 5;
`black --check py` clean at 1,133 files (1,114 tracked plus the live session's then-untracked
cam1753 modules); `git ls-files` = 2,259. The chain from the previous review's 905: **950** at
holman Phase 3 (the seven copied test modules collect 45) → **947** at holman Phase 4 (3 tests per
two-root vendoring entry, dropped with the entry) → 947 through book-of-job Phases 0–3 → **945**
after book-of-job Phase 4 (the plan's line "947 → 945") → 945 through every trio phase → 945 today.
**Zero `sys.path` mutations in tracked source** (`git grep -nE 'sys\.path\.(insert|append)|sys\.path\['
-- '*.py'` returns only docstrings that describe the rule).

**Message hygiene is the best in the series.** Of the 90 in-window commits, **3 lack the
`Co-Authored-By: Claude` trailer** (`7ddd6da` here, MAM-private `9db65d8` and `8f30d37`), against
8 of 95 last window and 10 of 44 the window before; `7ddd6da` is Ben-typed (no body), and the
MAM-private pair read as session-written, with the author email set to `ben.denckla@gmail.com`
where the trailered commits carry `bdenckla@alum.mit.edu` — a different client. Banned
constructions in the 90 messages: **one** "the latter" (codex-index-aleppo `98021de`: "° with the
degree sign in the latter"); zero "the former"; the one "the other" (holman `15824d4`) names both
sides. Every sweeping negative in the window names its oracle, as the 2026-08-18 review found had
become practice, and the self-correcting habit runs hot: nine of MAM-basics' 59 commits exist only
to correct a figure an earlier commit of the same morning stated (`eca7f14`, `4682adf`, `6621db4`,
`1e36d56`, `c3a6287`, `b594c72`, `2ddf667`, `c6bf42d`, `fe2f9ce`), and finding 6 below is about
one of those corrections being wrong in its turn.

## Findings

In rough order of consequence. Unlike the previous two reviews, one finding reaches the code —
a lint regression, not a wrong behaviour, wrong datum or broken artifact, none of which the review
found.

1. **`ruff check py` went from 0 findings to 25 in the window, and the two plans that brought them
   never ran ruff.** Re-established by `git archive <commit> py ruff.toml | tar -x -C <scratch>`
   and `.venv/Scripts/python.exe -m ruff check py` in each extraction: **0** at `6a6e600` (the
   previous review's anchor) and still 0 at `2ce3efb` (holman Phase 7 — holman's `9e290ce`
   cleared that repo's 13 findings *before* its Phase 3 copied the code here, and the holman plan
   recorded "`ruff check py` exit 0" at every phase after); **11** at `ef8e384` (book-of-job Phase 3); **21** at `11f7ced` (aleppo Phase 3); **25**
   at `fe6cef2` (cam1753 Phase 3, landed during the review). By code: 16 E402 (imports placed
   after a module-level assignment or a function — Copilot-era layout in
   `py/main_gen_aleppo_crop_editor.py`, `py/main_gen_cam1753_crop_editor.py` and
   `py/main_ac_find_word_in_images.py`, **not** a `sys.path` prelude), 6 F541, 1 F401, 1 F841,
   1 E731 — seven of them auto-fixable. `py/main_repo_maintenance.py`'s step 4 runs exactly this
   command, so its lint step has reported FAILED since 2026-08-19.
   `doc/PLAN-evacuate-python-from-book-of-job.md` mentions ruff zero times, and
   `doc/PLAN-evacuate-python-from-codex-index-trio.md` only to note `28a3208`'s `target-version`
   bump — whose message knows of "the pre-existing 11" without saying where they came from. Not
   fixed during the review: the files are the live trio session's, and that plan's Phase 7 is the
   natural home. The oracle for "done" is `ruff check py` printing `All checks passed!`.

2. **The vendoring audit is green by accident, in two repos.** `in/vendoring_policy.json` still
   gives `codex-index-aleppo` a `pkg_scan_roots.mb_cmn` of `py/mb_cmn` and `codex-index-cam1753`
   one of `mb_cmn`, and Phase 4 emptied both (`078b74d`, `a9c3abd`): each repo tracks 0 `.py`, and
   each directory survives on disk only as an untracked `__pycache__/`
   (`ls ../codex-index-aleppo/py/mb_cmn ../codex-index-cam1753/mb_cmn` → `__pycache__` and nothing
   else). `test_every_pkg_scan_root_exists` therefore passes, and `py/main_vendoring.py --all` runs,
   on this machine only; a fresh clone, or the trio plan's Phase 7 item 5 (delete `__pycache__`)
   run before its item 1, turns the test red and `discover.py:98` into the `ValueError` the test's
   own message describes from 2026-08-01. The tracked `doc/vendoring-inventory.md` (last regenerated
   by `cff95f7`, 2026-08-21) also still carries 7 trio rows for deleted files. The trio plan assigns
   all of this to Phase 7 but does not record that the test currently depends on untracked state.

3. **Drift, not an evacuation defect: holman-ketiv-qere's `data/uxlc_atom_locations.json` and
   `gh-pages/uxlc_corrections.html` are one UXLC-utils commit stale.** UXLC-utils `4d1ad89`
   (2026-08-19 14:27, the finer LC index records for pages 397A and 406A) landed five hours after
   holman Phase 7's oracle run (`2ce3efb`, 09:44). Regenerating now moves `Job 32:6.6` on 406A
   from col 1 line 19.6 to line 22.0 and `Job 32:12.1` from col 2 line 1.2 to line 3.1, and the two
   matching `<dd>Column …, line …` lines of the HTML — the 2 of 175 files the scratch-copy oracle
   found differing. Fix: `main_estimate_uxlc_locations` then `main_render_uxlc_corrections` from
   MAM-basics, and a commit in holman-ketiv-qere.

4. **Two tracker items only Ben can settle.** (a) The comments posted to #3 and #4 on 2026-08-22
   at 19:31–19:32Z say the melody-compiler sketch is "prose only (every `TROPEDEF` tradition is
   `TYPE="Torah"`)"; MAM-private `9db65d8`, thirteen minutes later, measured 22 of 45 blocks as
   `TYPE="Torah"`, and `a225faa` then established that the conclusion still holds because the one
   `Tehillim` block is a relabelled copy of a haftarah block. The two comments carry the false
   premise as fact, nothing in them links to the vendoring, and the tracked record of the truth is
   `al-hatorah/in/tropetransmission/PROVENANCE.md` only. (b) skadish1's 2026-08-19 comment on #185
   asks, in his words, whether it is possible "to 'program this in' as a known anomaly to the
   cantillation syntax", and adds four readings (printed editions' meteg under ש, Venice 1525's
   merkha under ר, LC's לג׳ note, LC Ne 12:24). The answer already exists — `BREUER_ENTRIES`'
   closed list of one and the `accounted_for_by_breuer_ch3_s2` group, described in the 2026-08-18
   comment above his — but nobody has said so in the thread, and his readings have no oracle on
   this machine.

5. **The programme plan is stale on the trio, against its own per-phase convention.** At
   `b37bdb4` — and still at `09d68c5`, after cam1753's Phase 4 — `doc/PLAN-evacuate-python-programme.md`'s
   trio row (line 16) and its Order item read "Phases 0 and 1 DONE 2026-08-22; Phases 3, 4, 6 and 7
   not started — all three repos", though `10ae4d5`, `11f7ced`, `98053b7`, `492057d`, `fe6cef2` and
   `09d68c5` have landed Phases 3 and 4 for all three. None of those commits touched the programme
   file (`git show --stat`). Every other plan's row was updated per phase. Left for the live
   session, which owns both files. Two smaller record gaps in the same family: `7ddd6da` removed
   `../wlc-utils` from `MAM-basics.code-workspace`, which
   `doc/PLAN-evacuate-the-rest-of-wlc-utils.md`'s Phase 11 item 7 says "both workspace files keep"
   — Ben's own commit, so a decision, but unrecorded in any plan; and holman Phase 7's Finding 2
   ("left for Ben") was fixed by MAM-private `e8fd4ae` fifteen minutes after `2ce3efb`, while the
   holman plan still reads "Not fixed" and only the book-of-job plan cites `e8fd4ae`.

6. **Three record errors fixed during the review** (the commit that lands this doc):
   - **The holman plan's Phase 7 "Finding 3" is false.** It says the `59 subtests` figure "does not
     reproduce — `pytest-subtests` is not installed in `.venv`, so pytest has no way to report the
     figure", and the programme's holman row repeats it. pytest 9.1.0 reports `unittest` subtests
     natively: this review's full run printed `945 passed, 5 skipped, 59 subtests passed`, and
     `py/main_test.py -q` over the six `subTest` modules alone prints `90 passed, 59 subtests
     passed`. The book-of-job plan already says so (its Phase 4 record: "that is wrong … measured
     twice"), but the holman plan and the programme row were never re-pointed. Why the 2026-08-19
     measurement saw no subtests line is not explained by anything in the record and this review
     did not reproduce it.
   - **The programme's "The order" subsection gave three wrong dates.** "Their Python having moved
     on 2026-08-18, 2026-08-19 and 2026-08-22 respectively" for book-of-job, holman-ketiv-qere and
     UXLC-utils, where the Phase 3 dates in those plans' Status tables are 2026-08-19, 2026-08-18
     and 2026-08-02; nothing moved on 2026-08-22. The conclusion it supports still holds.
   - **CLAUDE.md's "24 are lines of CSS hex colours, 46 colour tokens between them" mixes two
     counts.** The 24 lines that match `#`-plus-digit carry **32** tokens; 46 is the count over all
     36 lines of the two crop-editor files that carry a hex colour, the other 12 opening with a
     letter (`git grep -hoIE '#[0-9a-fA-F]{3,8}\b' 45f8853 -- main_gen_*_crop_editor.py | wc -l`
     in book-of-job). The separate bullet saying the two generators "hold 46 between them" is right.

7. **A Phase 0 figure was corrected wrongly, and the correction then falsified by later commits.**
   `4682adf` rewrote the trio plan's Phase 0 headline to "One commit in codex-index-aleppo and five
   here"; `git rev-list --count ef5525d^..72a4629^` is **10**, five more (`6621db4`, `c3a6287`,
   `b594c72`, `f6e7ad2`, `60aabf5`) having followed. Phase 1's Preconditions then say "the four
   commits between are" and list seven hashes. The same family, smaller: the Phase 4 aleppo record
   says "26 sites in four files" where its own breakdown and `078b74d`'s 5 M entries say five;
   `a50f40e`'s message says the `No col 1…; No col 2…` pair is on "29 of the 35 pages" where
   35 × 2 = 70 puts it on all 35 and 29 is the count of pages with nothing else (copied verbatim
   into codex-index-aleppo's CLAUDE.md by `2bdcfde`); holman's `6b10259` and the holman plan say
   the label refresh dropped `holam-he` from "8 of the 77 rows" where `io/table_row_github_issues.json`
   has 7 such rows (the eighth label sits on #81, which maps to no row); `0890cb8`, the holman plan
   and holman's `CLAUDE.md:14` say the deleted `.vscode/settings.json` held "fifteen" rules naming
   "nothing but that repo's interpreter and its `py/` scripts" where it held 19, nine of them
   `git`/`where.exe`/`settings.json` rules (`git -C holman-ketiv-qere show 15824d4:.vscode/settings.json`);
   the NFC-scope counts "154 → 47" in `b72f785`'s test comment, `0890cb8`'s message and the plan
   are 152 → 45 through the test's own `is_file()` filter, which drops the two octal-quoted JC3
   names the arithmetic kept; `ebc9669`'s "17,060 before the programme's Phase 0 having added 45"
   is 17,051 at `33b3ee2^` and +54 net; the holman plan and CLAUDE.md say holman's `CLAUDE.md`
   "quotes `#19` twice" where it is one backtick span naming two pages; `b37bdb4`'s "43 lines of
   drift" against cam1753's reader is 28+/4− = 32; "57 occurrences of μY" re-measures at 58.

8. **Stale comments in `py/tests/test_h_dot_below_nfc.py`'s book-of-job scope.** The floor
   comment itemizes 34 files ("four dotfiles") where the dotfiles are three and the measured 33 is
   right; and `_BOJ_EXCLUDE_DIR_PREFIXES` still lists `py_uxlc_loc/UXLC/` and `py_uxlc_loc/UXLC-misc/`
   with a present-tense "py_uxlc_loc/ holds 40 data files beside its 9 .py", all deleted by
   book-of-job `a846585`. Dead exclusions, harmless.

9. **No test exercises `b37bdb4`.** The inverted-nun clause in `py/py_ac_loc/mam_xml_verses.py` has
   one importer, `py_ac_loc/gen_flat_stream.py`, and the artifact that consumed it is
   codex-index-aleppo's `check_line_breaks.html` (`a50f40e`) — so the generated output is the
   test, per this repo's rule, and it was regenerated. Its docstring says the reader's callers
   "read Ps, Job and Prov" where `gen_flat_stream.py`'s `BOOK_XML` also lists Deut (harmless;
   Deut has no inverted nun).

10. **Prose, the window's full count of that class.** Three banned "the latter": codex-index-aleppo
    `98021de`'s message; the holman plan's line 240 (`0f11f5e`: "the latter checked and merely
    dead"); book-of-job `CLAUDE.md:30` (`a846585`: "the latter is the wrong instrument").
    wlc-utils#18's closing comment says "the two-witness gate" — "witness" is on the skill's banned
    list, though it quotes the issue body's own name for it. masorah-books#6's comment says "70
    parked" where the JSON key is `pending` (the fill-in plan's own word, three hits, so not a
    coinage). The holman `6b10259` message's "Eleven files, twelve accessors" matches no obvious
    count (12 files changed; `hkq_paths.py` defines 18 functions). Stale-by-later-work, accurate
    when written: holman `CLAUDE.md:104` still runs `codex-index-aleppo/py/main_find_word_in_aleppo_images.py`,
    deleted by `078b74d`; holman `README.md:328` calls the NFC scope "one of three" where the test
    now has seven; holman `CLAUDE.md:17` and `:91–92` describe a venv Phase 7 deleted (recorded as
    deliberately left, and a question for Ben). book-of-job's `.gitignore` still lists `__pycache__/`
    and `.venv/`.

## How the review was acted on (2026-08-22, during the review)

Finding 6's three record errors were the actionables a session could take without a decision from
Ben and without touching a file the live trio session owns, and they are fixed in the commit that
lands this doc: a dated correction appended to the holman plan's Phase 7 "Finding 3" and to the
programme's holman row; the three dates in the programme's "The order" subsection; and CLAUDE.md's
hex-colour sentence. Findings 1, 2 and 5 are left to the trio session, which owns the files and
whose Phase 7 is where the first two belong. Finding 3 is a two-command regeneration in a repo
with no live session, left because the series reviews rather than regenerates — the commands are
in the finding. Finding 4 is Ben's: both halves are outward-facing comments.

**Later the same day, 2026-08-22, after this doc was filed (`ea1f035`):**

- **Finding 4a is done.** On Ben's instruction, corrections were posted to #3 and #4
  ([#3 comment](https://github.com/bdenckla/MAM-basics/issues/3#issuecomment-5382436360),
  [#4 comment](https://github.com/bdenckla/MAM-basics/issues/4#issuecomment-5382436416)), each
  quoting its comment's false parenthesis, giving the measured `TYPE` split with the command that
  re-establishes it, and explaining why "prose only" still holds.
- **Findings 2 and 5 were cleared by the trio session's Phases 6 and 7** (`87ef5c0`, 16:46):
  `in/vendoring_policy.json` holds no `codex-index` entry and `doc/vendoring-inventory.md` no
  trio row, and the programme's trio row reads "DONE 2026-08-22 — every phase". The two smaller
  record gaps under finding 5 (`7ddd6da`'s reversal of the wlc-utils plan's Phase 11 item 7,
  and the holman plan's "Not fixed" at its line 783) remain. Of finding 10's stale-by-later-work
  items, holman `CLAUDE.md`'s `main_find_word_in_aleppo_images.py` line was rewritten by holman
  `b1e1a2d` (16:50); holman `README.md:328`'s "one of three" remains.
- **Finding 1 stands at 25** (`ruff check py`, re-run at `48485f3`), and finding 3's two holman
  artifacts are still unregenerated — holman `b1e1a2d` is a doc repoint, not a regeneration.
- **Finding 4b led somewhere else.** Reading #185's thread and the checker to answer Ben's
  question about it established that the checker never found the Ne 8:7 merkha odd — the
  June ERROR was the `has_legarmeh` book-name bug, fixed by wlc-utils `306e15f` on 2026-06-12 —
  but that the checker reads the verse's **second** bar as a legarmeh where MAM, the LC's
  margin and another edition's paseq list read a paseq, because `has_legarmeh` decides per verse.
  Filed as [#233](https://github.com/bdenckla/MAM-basics/issues/233). A reply to skadish1 on
  #185 is still Ben's to post.
- The remaining actionables — findings 1, 3, the residue of 5, and the record corrections of
  7, 8, 9 and 10 — were handed to a task chip on 2026-08-22, once the trio session was archived.

**The task chip ran later on 2026-08-22, starting from MAM-basics `fb3b7f3`, holman-ketiv-qere
`b1e1a2d`, book-of-job `81e036b` and codex-index-aleppo `94b824a`, all clean, and every item it
was handed landed:**

- **Finding 1 — MAM-basics `de8a28b`.** `ruff check py` prints `All checks passed!`, from 25.
  Seven by `ruff --fix` (6 F541, 1 F401), the 16 E402 by moving the imports above
  `OUT_DIR = …novc_dir()` and `serve_and_open` in the three Copilot-era entry points, the F841
  and E731 by hand. `py\check_ac_word_finding.py` and `py\check_cam1753_word_finding.py`
  produce byte-identical output before and after, black reports all seven files unchanged, and
  the three rearranged entry points import cleanly.
- **Finding 3 — holman-ketiv-qere `36718d6`.** `main_estimate_uxlc_locations` then
  `main_render_uxlc_corrections` from MAM-basics, UXLC-utils at `292e7a7`; the diff is exactly the
  four JSON lines and two `<dd>` lines the finding predicted, nothing else in `git status`.
  (The chip's brief named `py/main_uxlc_estimate_atom_loc.py` as the estimator; that is the
  word-finding CLI whose docstring `48485f3` repointed, and `py/main_estimate_uxlc_locations.py`
  is the generator, as the holman plan's line 68 says.)
- **Finding 5's residue — MAM-basics `d8bec00`.** Dated notes on `7ddd6da` at the wlc-utils plan's
  Phase 11 item 7 and on `e8fd4ae` at the holman plan's Phase 7 finding 2.
- **Findings 7, 8 and 9 — MAM-basics `cb3e7b2`**, plus **codex-index-aleppo `1da6b23`** for the
  `CLAUDE.md` there and **holman-ketiv-qere `5f419ef`** for its `CLAUDE.md:14`. Every figure
  re-derived first and each correction dated in place with its command: 10 commits (twice) and
  five files and 58 μY in the trio plan; 7 `holam-he` rows, 19 rules with 9 naming neither
  interpreter nor script, 152 → 45, `#19` once, and line 240's file named in the holman plan;
  17,051 and +54 in the book-of-job plan's Baselines row; the 35-page pair in codex-index-aleppo;
  the `#19` sentence in this repo's `CLAUDE.md`. Finding 8: three dotfiles, and the two dead
  `py_uxlc_loc/` exclusions gone, book-of-job's scope 33 before and after through
  `_tracked_files_in_scope`. Finding 9: the docstring names both callers and their book lists.
- **Finding 10 — holman-ketiv-qere `5f419ef`** (README's "one of three" → seven, with the dates
  it went 3 → 4 → 7) and **book-of-job `3f096b9`** (`CLAUDE.md:30` names
  `git status --porcelain`; `.gitignore` loses `__pycache__/` and `.venv/`, neither of which
  exists on disk there). Holman `CLAUDE.md:17` and `:91–92` left alone as the holman plan
  records. The three "the latter" are now one, codex-index-aleppo `98021de`'s message, which is
  immutable.
- **One figure in the chip's brief was stale and is recorded here rather than acted on:** the
  suite baseline. The brief said 945 at `fb3b7f3`, from this doc's measurement at `b37bdb4`;
  re-measured before any edit it is **940 passed, 5 skipped, 59 subtests**, because `87ef5c0`
  (trio Phases 6 and 7) dropped `test_vendoring_policy_paths.py` from 23 cases to 18 with the
  trio's policy entries and says so in its message. 940 / 5 / 59 after every commit above.

## Open ends the window itself declares (not findings)

The codex-index trio evacuation's Phases 6 and 7 — in flight during this review, Phase 4 for all
three repos landed by `09d68c5` — owed a verdict by the next review, together with findings 1, 2
and 5 above, which that phase is expected to clear. The plan for the total evacuation of
book-of-job, holman-ketiv-qere and UXLC-utils (their `gh-pages/` trees to MAM-basics, stubs left
behind), which the programme says is written after the trio finishes — not started. MAM-private's
melody-compiler work, which `555ed14` (landed during the review) plans and specifies for a fresh
session — not started, and #3/#4 are its tracker home. MAM-basics #225, #226, #227, #229 and #230,
all open and untouched in-window; #185 open deliberately, now with skadish1's unanswered question
(finding 4b). The scan-pages undertaking parked at Phase 0 done since 2026-08-07 (`doc/scan-pages.md`),
untouched for a third window. The hcanat.us /Notes/ template question `e4d7997` flags, unanswered.
The cam1753 line-ending watch item from the 2026-08-10 review's finding 8 was finally exercised —
`f56831c` and `7e5ca23` fixed eight CRLF-writing sites and `git ls-files --eol` shows no CRLF
tracked — and is closed.

## Scope change, 2026-08-26: this series covers public repos only from now on

Ben's decision, 2026-08-26. Findings about private repos are no longer recorded in this series or
filed in this repo's tracker: private-repo reviews have their own series, recorded in
`bdenckla/MAM-private` at `doc/review-findings-YYYY-MM-DD.md` there, with thin-pointer issues
there, under the same conventions. The first private review ran 2026-08-26 and took the
private-side open ends above with it — MAM-private's melody-compiler work among them, on which it
delivered the verdicts this doc left owed on `a225faa` and `555ed14`. The next review in this
series covers the public repos only: the scope statement's "every clone directly under
`~/GitRepos`" narrows to every public clone there, and the public open ends above — the
codex-index trio Phases 6 and 7 verdict among them, plus the four public commits this doc left
unverdicted (`fe6cef2`, `09d68c5`, codex-index-aleppo `2bdcfde`, codex-index-cam1753 `a9c3abd`) —
stay with it.
