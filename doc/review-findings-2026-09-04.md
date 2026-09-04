# Findings of the 2026-09-04 review of the public repos since 2026-09-01

State: not acted on. Written untracked at `.novc/review-findings-2026-09-04.md` on Ben's
instruction of 2026-09-04 ("Don't write anything to git-tracked locations … Even your review
findings should go to .novc", other sessions being live in MAM-basics), then committed here the
same afternoon at Ben's instruction with nothing acted on. Between the two, only this paragraph, the
scope paragraph's count of post-anchor commits, the scripts' location and the closing section
changed, plus seven Hebrew runs put into MAM-normal mark order: they had been typed rather than
lifted from the data, which is finding 1's own mechanism, and were caught by running finding 1's
check over this file before committing it. It is the Claude half of the first dual-agent review
under `doc/dual-agent-review.md`. The Codex half was neither read nor sought (the blindness rule:
no file named `codex-review-findings*`, nothing under `~/.codex/` beyond `AGENTS.md`'s line count,
nothing under `Documents/Codex/`), and the four-bucket reconciliation is a later, separate task for
a session that wrote neither file; it goes at the end of this file, under `## Reconciliation with
the Codex review`. Nothing here was fixed; every finding is "unfixed" or "Ben's decision".

## Scope, anchors and census

Third review under the public-repos-only scope. It covers committed work from the 2026-09-01
review's anchors through the moment this review started, 2026-09-04 ~12:40 local, when MAM-basics'
HEAD was **`b4706759`** (2026-09-04 12:08). **The tree moved under the review, and a session was
live in it throughout.** By the time this file was written (about 14:30) MAM-basics stood seven commits
past the anchor, from `df61173a` (13:56, "Land Aleppo data and pages", 170 files under new paths
`MAM-XML/`, `aleppo/`, `gh-pages/aleppo/`) to `18b4eb7a` (14:26), with the last of them unpushed and
two plan files dirty, and stream D had seen five `py/` files dirty mid-review; by the time it was
committed (about 15:30) the count was fifteen, through `d92c8a32` (15:16, "Record the completed
Cambridge 1753 evacuation"). That is the third stage's Aleppo and Cambridge 1753 lanes executing
beside this review. **None of those fifteen commits was reviewed.** Every figure below was measured at `b4706759` by
`git show`, or on working-tree files those commits do not touch, or by the suite run at 12:45
local while the tree was still clean at the anchor.

Anchors (start → end) and counts, re-measurable with
`git -C C:/Users/BenDe/GitRepos/<repo> log <start>..<end> --oneline`:

| Repo | Range | Commits | Non-merge |
|---|---|---|---|
| MAM-basics | `4cc0c33..b4706759` | 187 | 151 |
| MAM-parsed | `46209cd..5108203` | 3 | 3 |
| MAM-simple | `cd2bef8..7a4f21d` | 5 | 5 |
| MAM-with-doc | `999a437..0fe406c` | 5 | 5 |
| MAM-for-Sefaria | since 2026-09-01T10:30 → `ce1e04c` | 2 | 2 |
| MAM-OSIS | since 2026-09-01T10:30 → `697dc98` | 2 | 2 |
| codex-index-aleppo | `1c12a8e..8f1fcfd` | 1 | 1 |
| codex-index-cam1753 | `7309882..3667b6c` | 1 | 1 |
| codex-index-leningrad | `2abd7f6..86f88c0` | 3 | 3 |
| Taamey_D | since 2026-09-01T10:30 → `3813499` | 1 | 1 |

That is **210 commits across ten local public repos**; MAM-basics' 187 are 183 authored Ben Denckla
and 4 authored Claude (the three cloud commits `205c64a9`, `b403e6df`, `86c87d24`, entering through
the merge `81fac842`, which is the fourth). Two local public clones were quiet: diffable-pointed-hebrew
and phonetic-hbo. **Three public repos have no local clone any more and were read on GitHub**:
book-of-job (3 commits since the anchor, ending `c8a6bbf` "Empty Book-of-Job into redirect host"),
holman-ketiv-qere (20, `aacd3ee` … `ca55c4a` "Empty Holman redirect host") and UXLC-utils (3, ending
`2745c65` "Retire UXLC-utils source tree"); with those 26 the window is **236 commits**. Three
clones are private and fall to the private series: MAM-private, github-misc (10 in-window commits),
hbofonts (1). The series' one deliberate exception was applied again: github-misc's instruction-file
plumbing was byte-compared (finding 17).

`GitRepos` holds 15 clones for a 14-folder roster (the extra is codex-index-leningrad, finding 4)
plus two non-clone directories (finding 18). The review ran as five agent streams plus the main
session: (A) the 2026-09-01 post-review tail, the change-log remediation, the cloud commits and
the Job-mapping report; (B) Holman's suggested corrections to MAM and the template dispatch;
(C) the 2026-09-02 evacuation assessment, the WLC severance, and the Holman, book-of-job and
Leningrad lanes; (D) the UXLC-utils evacuation, the sibling-reach lint, the mega guards, the
fourth-stage draft and the dual-agent doc; (E) the Holman meteg rollout end to end. Every script
and output is untracked under `.novc/review-2026-09-04/` on the machine that ran the review (210
files copied there from the session scratchpad before this file was committed; prefixed `A_` … `E_`
per stream, unprefixed for the main session).

## Tree health at `b4706759`: green, with the suite at 973

- Suite: **973 passed, 5 skipped, 65 subtests** (`.venv/Scripts/python.exe py/main_test.py -q`,
  105.66 s, run on the clean anchor tree); collect-only 978 = 973 + 5.
- `ruff check py` clean; `black --check py` clean at **1,162** files (1,148 at the last review).
- `git ls-files` = **4,161** (2,305 at the last review; the +1,856 are the three evacuations'
  landings). Tracked under `gh-pages/`: 1,505 files, 429 HTML (156 HTML at the last review).
- Zero `sys.path` mutations in tracked source: a grep matches 15 files, every one a docstring or
  comment naming the construct (the twelve `py/main_ac_*` / `py/main_cam1753_*` wrapper docstrings,
  `main_test.py`, and `check_repo_standards.py`'s own rule text).
- `--check-repo-standards --workspace-file all-repos.code-workspace --visibility public` sweeps 11
  repos and reports no new problem. For the record: MAM-basics HEX_ESCAPES 79, NFC_H_DOT 30,
  NFC_LATIN 38, all in data or legacy-source files the NFC lint excludes (that lint is green);
  Taamey_D GITATTRIBUTES_LF=False as before.
- **The suite chain from the last review's 971, each step attributed** (collected 974 → 978):
  +2 `test_no_machine_paths_in_artifacts.py` (already inside the 971 measured after `81fac842`);
  `test_wlc_redirect_manifest.py` (1) replaced by `test_redirect_manifest.py` (4, parametrized over
  the four redirect hosts as each manifest froze: `46ba28a0`, `dc6442fb`, `8c42a3f4`) = +3;
  `test_site_index_links.py` +1 (`df4b5661`); `test_vendoring_policy_paths.py` −4 (`abb03ec4`, 18 → 14
  collected); `test_sibling_reach.py` +2 (`bc36750c`, `1f39b6f9`). So 971 + 3 + 1 = 975 on the
  afternoon of 2026-09-03, then 975 − 4 + 2 = 973 on 2026-09-04. See finding 9.

## What verifies sound, stream by stream

**The 2026-09-01 tail, the change-log remediation, the cloud commits and the Job-mapping report
(stream A).** The three cloud commits hold up on Windows as they did in the Linux sandbox:
`paths.display_path` behaves as its docstring says in the in-repo, sibling, bare-root and no-repo
cases and introduces no import cycle; the OSIS resolver was called with exactly
`http://www.w3.org/2001/xml.xsd` and answered it from `in/xml.xsd`, after which
`MAM-OSIS/mapm.osis.xml` validates in 0.2 s; the diff-mpp fail-loud paths raise where the message
says. The machine-paths lint's floor figures re-derive (626 → 501 → 500 at `86c87d24`), and at HEAD
the two trees hold 1,846 tracked files with **zero offenders** by the lint's regex and by broader
patterns (`/home/`, `/Users/`, `BenDe`, `GitRepos`, `AppData`, `Forests`); the 55 drive-letter hits
are Michigan-Claremont transliteration strings such as `W:/NFHFR.03`. `81fac842`'s "45 commits since
the cut" and "main touched only DATA-LICENSES.md" re-derive. **The regenerated change logs are
consistent with the code byte for byte**: an in-memory run of `9ce6ee5..54ba7e0` with `4439077e`'s
scroll-difference-note normalization on gives 24 records / 25 cards equal to the tracked
`unpinned-latest.json`, and with it off gives 175 raw / 51 / 57, `4397daa`'s three figures, so
`b3837db` removed exactly the 27 accent-removal and 5 misc cards the code now ignores. `bc24f7ad`'s
eleven `newline=""` sites across eight files count; the MAM-parsed and MAM-simple vendored copies
are blob-identical to their sources. `1761d5ca`, `4386f4a1`, `5f3d7f4f`, `297f7e55` and `3e9d5cf0`
check against their claims. The Codex phase docs' figures spot-check (Phase 11's two SHA-256s and
byte sizes, Phase 12's 43 / 8 / 46 rows, Phase 13's 45 = 17 + 13 + 13 + 2 and the 89-row ledger).
The Job-mapping report: every figure in `py/main_map_changes_to_book_of_job.py`'s docstring
re-derives from a read-only call of its functions (OK 130 / Issues 30; deltas 3 / 20 / 4 / 3 with the
same entries; 1,398 changes across 17 files; two trailing-space columns; the mapping JSON byte-equal
in memory); `823358a3`'s evidence that #123 moved is confirmed from UXLC-utils' history via `gh api`
(position 3 with `נָשָׂ֨א ׀` at `816918ca` and `2ab7f0e1`, position 7 with `נִכַּר־` from `d03f1405`
on); "hand-authored" is exactly 72 occurrences in 32 files at `b4706759`.

**Holman's suggested corrections to MAM and the template dispatch (stream B).** The privacy
boundary holds as CLAUDE.md states it: `mam_suggestion_extract.py` accepts a message only when the
From display name is Holman's, and the tracked derivative `holman/docs-not-served/mam_suggestions.json`
holds no `@`, no quoted body text and no header field beyond subject, date and sender name; 34 cases
(30 Aleppo Codex, 4 Jerusalem Crown) from three messages, 34 crops under `gh-pages/holman/mam_img/`,
every disposition dated and attributed (Seth (Avi) Kadish 2026-08-28 ×4; Ben Denckla 2026-09-03 ×30),
none naming anyone's circumstances. **All 34 atom indices re-derive** with an independent tokenizer
over MAM-parsed `5108203`, and every corpus figure in `757aa68a`, `147e9e4f`, `d8442efd` and
`_collect_text_fragments`' docstring re-measures exactly (23,202 payloads; the navigation template
in 895 payloads, 889 with a seder or aliyah and 6 bare; 532 aliyah templates; 507 verses changing
atom count between the two collectors; 626 atoms across 559 verses, 508 / 116 / 2 by template;
Genesis 1:1 at 9 then 7; 3,824 double-U+0599 atoms with exactly two qadma-before-pashta, Exodus 20:9
and Deuteronomy 5:13). The dispatch at HEAD has no fallback and raised nothing over all 23,202
payloads. The rendered Archived page agrees with the JSON card by card for all 34; every
suggestion-card Hebrew cell is `dir="rtl"`; the extra-letter-spacing class is on exactly M32 and
M34; "HUB" occurs zero times on both pages; the Aleppo lacunae `ca4752b1` cites (2 Kgs 14:21–18:13,
Zeph 3:20–Zech 9:17) are what codex-index-aleppo's missing-sections page says. The 1 Samuel 28:12
derivative is address-free and its pinned atom 11 is right by MAM's count of 16.
holman-ketiv-qere's 20 same-day commits mirror the MAM-basics ones title for title; `c811f63` and
`7a25b34` changed only that repo's README, and their substance reached MAM-basics through `ca4752b1`
and `3829585c`. All 19 non-merge commits carry the Claude trailer.

**The evacuation assessment, the WLC severance, and the Holman, book-of-job and Leningrad lanes
(stream C).** Both redirect lanes re-derive exactly. `in/holman_ketiv_qere_redirect_pages.json` (6)
and `in/book_of_job_redirect_pages.json` (175) equal the `.html` sets of the source trees at their
last pre-stub commits (`7a25b34`, `fea3acd`); all 183 stubs fetched from `723bd73` and `138db11` name
percent-encoded `bdenckla.github.io/MAM-basics/<tree>/…` targets, every one tracked here at
`b4706759`; the live old hosts answer 200 on every frozen Holman URL and on four book-of-job pages,
404 on non-stub paths; the emptied hosts hold 12 and 181 files as their records say. All 379 Holman
and 703 book-of-job carried files were blob-identical at their Land commits (`3c5dc796`,
`050c7bb8`), the later differences each deliberate. No `.eml` and no email address landed. The WLC
severance (`d152ec8d`) removed `wlc_utils_private_dir()` and the two `2025-03-21` descriptors;
`688bc05a`'s restored fixture is inert (an env-name mapping that never touches the filesystem); the
only `wlc-utils` resolution left in `py/` is `stubs.source_pages_dir`. `leningrad/`'s five files are
blob-identical to codex-index-leningrad `aa603a9` except the two cross-link repoints;
`main_lenin_wikisource_page.py` reads `uxlc/data/lci_augrecs.json`; `86f88c0` left a 382-byte README
and the repo is archived. The Phase 1 and 2 records of the three-repos plan, the 2026-09-02
assessment's ten drifts and four dated decisions, and the `DATA-LICENSES.md` rows for the four
landed trees all re-derive.

**The UXLC-utils evacuation, the sibling-reach lint, the mega guards, the fourth-stage draft and the
dual-agent doc (stream D).** `in/uxlc_utils_redirect_pages.json`'s 91 pages equal the source's
`gh-pages/*.html` at `a2768f4` both ways; all 91 stubs at `2745c65` target files tracked at HEAD (a
pure prefix rewrite, 91 of 91); the live host and three targets answer 200 with the expected bodies
(stubs Last-Modified 2026-09-03 20:02:08 GMT, `2745c65`'s deploy). Of the source's 780 blobs, 726
landed byte-identical, 2 were rewritten by later deliberate commits, 1 was deleted (`d8a63afd`), and
the 42 dropped by `df6b913e`'s recorded decision are byte-identical to MAM-basics' retained copies for
40 and differ by one header-comment line for the two `lci_recs.json`; the six not carried are repo
metadata. The `uxlc/doc/` bare-`#NN` exception paragraph in CLAUDE.md is accurate. `8da39b48`'s five
named sites go through `require_sibling` (but see finding 14). The site-index reverse check does
fail on an unindexed deploy-root page by construction, and its input is non-vacuous (two pages
checked). `SIBLINGS_REACHED` has thirteen entries at `b4706759`, the four redirect hosts declared and
not in the roster, codex-index-leningrad in neither, correctly; no import alias of the resolvers
exists. The mega guard refuses the half-steered and the unsteered worktree shapes and runs before
any step. The vendoring de-audit leaves exactly the two MAM-private run-time routes the lint
declares (`main_0_mega.py`'s census step and `paths.al_hatorah_phonetic_dir`), nothing at import
time. The fourth-stage draft names the five product repos of the workspace, numbers its six
sub-questions, dates and attributes them, and the second stage's closing rule is narrowed in place
in both files so it no longer deletes the third stage. `doc/dual-agent-review.md`'s figures
re-derive (50 lines / 23 files and 29 / 11 at `dc24164b`; 67 / 23 at HEAD; `~/.codex/AGENTS.md`
998 lines; 42 `StepRecord`s at `c3e810d0`). The forward-slash sweep left zero fixed-string backslash
residue in seven repos and one deliberate docstring quotation here.

**The Holman meteg rollout, end to end (stream E).** **The live Wikisource edit re-derives
exactly.** `in/mam-ws-bot-edits/holman-meteg-removal.json` holds 29 entries over 22 chapters and
`holman-meteg-add-isaiah-23-12.json` 1, the 23 chapters of `031b4306`'s message; every `old` string
occurs exactly once in its chapter before the bot and zero times after. Per-book U+05BD before →
after: Judges 1202 → 1194, 1 Samuel 1482 → 1480, 2 Samuel 1142 → 1138, 1 Kings 1338 → 1330, 2 Kings
1265 → 1264, 2 Chronicles 1462 → 1456, Isaiah 2034 → 2035 — 29 off, 1 on, 29 changed verse lines,
**zero non-meteg changes** in the 23 chapters. Four live chapters fetched read-only on 2026-09-04
are byte-identical to `in/mam-ws` at HEAD. `0d1ad458`'s two re-downloads changed exactly Joshua
10:12 and Zechariah 2:4, both non-meteg, as recorded. The wsgo round trip: 35 auto-edit rows at
`e43cb5fd` = 28 removal verses + Isaiah 23:12 + Joshua 10:12 + Zechariah 2:4 + two rows at 2 Kings
21:12 + two at 2 Samuel 18:20 (33 verses), and all three outputs `[]` at `17323f3f`. The carry into
the five derivative repos touches no verse outside those 33 (see finding 12 for the count).
MAM-simple's `template_names.py` is blob `0cd401c0` in both repos, 48 lines added. The thirty records
and their archive check out: 29 removals + M23's addition + four "neither" (M17, M24, M32, M34); all
34 cards on the Archived page and none on the Active page, every card's forms, outcome and summary
equal to the data, M1 holding the batch reason and the other 29 meteg cards linking to it;
"Suppressed" visible nowhere; the M23 card carries exactly one added link. Item 2's "17 fail
verbatim, 11 for mark order alone" re-derives exactly. The post-stress meteg survey is internally
consistent: 231 = 177 + 54, the type and accent tallies re-tally, the currency figures 221 / 23,184
and 38,379 − 38,170 = 209 hold, MAM-simple at HEAD reproduces all 221 "today" values, 235 of 235
Hebrew cells are `dir="rtl"`, and the rendered page has no banned vocabulary. The eleven deferred
edits verify live (nine removals, two additions at the named verses). black leaves all 18 touched
Python files unchanged.

**Main session.** The trailer census, the branch census, the roster and visibility map, the doc/
`State:` lines, the instruction-file plumbing, the HTML sanity lint on the archived anchor tree,
the standards sweep, and the independent re-derivations recorded under the findings below (the
mark-order scan of every window-changed `.py`, the meteg delta of three carry commits, the roster
file's parse history, the three maqaf-compound cases, the sanity lint's false positives).

## Findings

In rough order of consequence. Nothing was fixed. Line numbers are as measured at `b4706759`; the
files the Aleppo lane has since edited will have drifted, so search for the quoted text.

1. **Data defect, unfixed: nine Hebrew clusters in Unicode-normal mark order entered hand-authored
   Python in this window, in four files, and one of them reaches tracked data and a rendered page.**
   This is the defect class CLAUDE.md's first section exists for, and the mechanism it names — Hebrew
   that was not lifted from the data. Measured by the main session with `has_std_mark_order` over
   every Hebrew run of every `.py` added or modified in `4cc0c33..b4706759` (`.novc/review-2026-09-04/mark_order_window_scan.py`; streams B and E found the same sites independently):
   1. `py/hkq_cmn/mam_suggestion_dispositions.py:363` (`b20f7aff`): the syllable glossed "(shu)" as
      shin, qubuts, shin dot (05E9 05BB 05C1) — MAM-normal order puts the shin dot first. It
      propagates to `holman/docs-not-served/mam_suggestions.json` line 942 (M24's reason) and to
      `gh-pages/holman/table_data_findings_suppressed.html` line 3959, the one non-MAM-normal run on
      either Holman page; the Active page has zero.
   2. `py/accgram/post_stress_meteg.py:395, 399, 400` (`deb80472`): וַיֹּאמֶר and פַּדֶּנָה twice in
      `_structural_type`'s docstring, each with the dagesh after the vowel.
   3. `py/hkq_cmn/uxlc_atom_index_notes.py:39, 42, 43` (`32167f2f`): qamats before shin dot, patah
      before dagesh, hiriq before dagesh.
   4. `py/py_render/rt_mam_suggestion_card.py:47` (`a9422f94`): two clusters with holam before dagesh.
   `d8442efd`'s sweep was scoped to "two of these files" and missed these. Twelve further
   non-MAM-normal runs sit on pre-existing, untouched lines of four other files (`mam_simple_verse.py`
   ×8, `mpplus_diff_from_plain.py:134`, `uxlc_email_extract.py:197`,
   `main_estimate_uxlc_locations.py:36` ×2), outside the window and not examined for whether they are
   deliberate illustrations of the other order. Re-establish: run `.novc/review-2026-09-04/mark_order_window_scan.py`, or
   `give_std_mark_order` on each quoted run.

2. **Stale generated artifact, unfixed, found independently by streams A and E: MAM-with-doc's
   published unpinned change log does not list the Holman meteg rollout.**
   `gh-pages/change-log/unpinned-latest.{html,json}` at MAM-with-doc `0fe406c` was last regenerated by
   `b3837db` (2026-09-02): "2026-09-01", range `9ce6ee5..HEAD` ending at MAM-parsed `b9c8a77`, 24
   records / 25 cards, none of the 33 rollout verses — while MAM-parsed's HEAD is `5108203`
   (2026-09-04, 14 `plus/` files). Mechanism: `diff_mpp.run_unpinned_latest` compares committed
   MAM-parsed revisions; the 2026-09-04 mega ran while MAM-parsed HEAD was still `54ba7e0`;
   `5108203` was committed afterwards as item 5 step 7; and nothing in the programme re-runs
   `py/main_diff.py mpp --all` after the MAM-parsed commit, so the published log lags one mega run
   behind every carry of this shape. An in-memory run of `9ce6ee5..5108203` gives **180 raw / 56
   records / 58 cards, verification clean** (meteg-removal 31, template-change 8, meteg-addition 6,
   misc 5, rafeh 4, varika 3, accent-addition 1), so `db4298e8`'s fail-closed raise is not what
   stopped it. `0fe406c` committed nine book pages and three FOI files and no change-log file
   (confirmed from its stat). Design note: `new_rev: "HEAD"` in the tracked JSON is a moving label,
   so the JSON alone cannot say which MAM-parsed commit it was built from; only the HTML's end date
   does.

3. **Record error, unfixed: `DATA-LICENSES.md` line 93 says of `uxlc/out/` "Every file here is
   script-regenerable; the one exception … was deleted on 2026-09-04", and two tracked files there
   are not.** `uxlc/out/Possible false early meteg marks.code-search` is a saved VS Code search
   (header `# Query: …`, `# Flags: CaseSensitive RegExp`, `66 results - 21 files`) and
   `uxlc/out/Possible false early meteg marks.csv` is its result; no tracked Python names either,
   and `doc/PLAN-evacuate-the-rest-of-three-repos.md:698` says what they are. Both arrived with
   `db9b0d72`; the sentence was written by `d8a63afd` and sharpened by `b4706759`. Under the
   vocabulary `b4706759` itself adopts, they are Ben-written, not script-regenerable. Adjacent, same
   tree: `uxlc/doc/clc-design.md:203` links that CSV relative to `uxlc/doc/`, where it is not;
   the three-repos plan's line 698 told the move to "fix that link to `../out/…` as the doc moves",
   and it was not. Re-establish: `git ls-files uxlc/out`; `grep -n "early meteg" uxlc/doc/clc-design.md`.

4. **Stale doc with a decision attached, Ben's decision: CLAUDE.md keeps the codex-index-leningrad
   clone for a review forest that no longer exists, and the forests' retirement is recorded
   nowhere.** §"codex-index-leningrad is a review-forest exception" (`cd9d3979`, 2026-09-03 18:17)
   says the primary clone "remains solely as the shared Git directory" for a detached worktree at
   `C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/codex-index-leningrad`
   and "can leave only after that forest no longer needs its shared Git metadata". Measured four
   times on 2026-09-04 (main session, streams A, C, D): that path does not exist; `ReviewForests/`
   exists, is empty, and was last written at **12:49:54** (41 minutes after the anchor commit);
   `C:/Users/BenDe/Forests/` is empty too; `git worktree list` in the clone prints the main worktree
   only and `.git/worktrees/` is absent, so the worktree was torn down with `worktree remove` or
   `prune`, not merely deleted; the clone's reflog is one `clone:` entry at 2026-09-03 18:14:40, the
   re-clone the trio plan's Phase 1 record describes. So the section's stated reason lapsed at 12:49
   today, and by CLAUDE.md's own "Repo locations are decisions" rule the clone is now residue — in
   no workspace file, no `repo_visibility` entry, no roster. Nothing through `d92c8a32` records the
   forests' retirement: `doc/PLAN-mam-mega-pipeline-phase-13-and-remediation.md:429, 492` still say
   the two remediation forests "remain present pending … retirement decision",
   `doc/dual-agent-review.md:242` still says four forests exist, and the trio plan's Phase 1 Status
   row and the programme's third-stage Status row repeat the lapsed premise. Ben's decision: whether
   the clone leaves now, and where the forests' retirement is recorded (the mega-pipeline plan is
   the natural place). Re-establish: `ls -la C:/Users/BenDe/Documents/Codex/ReviewForests`;
   `git -C C:/Users/BenDe/GitRepos/codex-index-leningrad worktree list`.

5. **Stale doc, unfixed: five of the seven `doc/boj-*.md` procedures still address `../book-of-job/`
   at 33 sites, and CLAUDE.md gives that spelling as current, though the clone was retired by
   `5e61a549` on 2026-09-03.** `boj-cam1753-word-crops.md` 16, `boj-aleppo-word-crops.md` 12,
   `boj-leningrad-word-crops.md` 3, `boj-leningrad-image-scaling.md` 1,
   `boj-image-crop-reproducibility.md` 1 — four of them `Start-Process
   "C:/Users/BenDe/GitRepos/book-of-job/gh-pages/…"` lines, one naming the dropped `py_ac_loc/`.
   `058f6b03` repointed only `boj-quirkrec-comments.md` and the two `book-of-job/doc/` procedures, yet
   the three-repos plan's Phase 4 record says "`doc/boj-*.md` … now name their MAM-basics
   locations", and CLAUDE.md §"`doc/boj-*.md` are book-of-job's procedures" still states "Every path
   in them was repointed on arrival: … book-of-job's corpus and published site as `../book-of-job/…`".
   A session following `boj-aleppo-word-crops.md` would write crops into a directory that does not
   exist. Two more sentences went stale the same way with the 2026-09-03 evacuations:
   `doc/book-of-job-artifacts.md`'s closing sentence still says the location cross-check "reads the
   `UXLC-utils` sibling repository", and `holman/doc/uxlc-email-count-disagreements.md:179` names a
   run "from `C:/Users/BenDe/GitRepos/holman-ketiv-qere` on that repo's own venv". Re-establish:
   `grep -rn "\.\./book-of-job" doc/boj-*.md`.

6. **Stale doc, unfixed: five markdown links point at `doc/PLAN-evacuate-the-rest-of-wlc-utils.md`,
   which `80c9ad85` deleted three hours after `8be49eca` had repaired the previous dead links.**
   `80c9ad85` "Close second-stage evacuation bookkeeping" (2026-09-03 17:10) deleted that 2,844-line
   plan under `5cfc6d4e`'s rule that it "holds nothing unique", after `8be49eca` (14:19) had recorded
   "Every one of doc/'s 44 relative markdown links now resolves"; nobody re-ran the check. Dead at
   `b4706759`: `DATA-LICENSES.md:31`; `doc/PLAN-evacuate-public-repos-programme.md:1005`;
   `doc/PLAN-evacuate-the-rest-of-three-repos.md:11` ("**Read [it] before executing any phase
   here**"), `:45`, `:62`. None uses the "(deleted <date> by `<sha>`; in git history)" form
   `8be49eca` established. Ten docstring citations of the file by name carry no annotation either
   (`py/main_0_mega.py:11, 75`; `py/main_repo_maintenance.py:21, 109`; `py/mb_cmn/paths.py:36`;
   `py/redirect_stubs/stubs.py:13`; `py/accgram/rtms_report.py:459`;
   `py/tests/test_h_dot_below_nfc.py:18, 172`; `py/tests/test_prose_conventions.py:181`) — Ben's
   leave-as-written precedent may cover those. Separately, **48 links in `uxlc/doc/` were already
   dead when the files landed**: `clc-design.md`'s 42 and `clc-skeleton-plan.md`'s 6 are repo-root-relative
   (`py/main_fois.py`, `py/clc/clc_render.py`, `data/lci_augrecs.json`, …) and now sit two directories
   down, so they resolve to `uxlc/doc/py/…`; CLAUDE.md's exception paragraph covers bare `#NN` only and
   sends readers to §7.16 of that document. Whether those 48 are an execution record to be left is
   not said anywhere. Re-establish: `.novc/review-2026-09-04/D_md_links.py`, or `git ls-files` against each link.

7. **Record error, unfixed: the forward-slash sweep `61b192f9` rewrote escape notation in prose as if
   it were a path, at four sites, against its own "preserving … string-escape … backslashes".**
   `doc/PLAN-repo-maintenance-across-GitRepos.md:530` now reads "converting `/uXXXX` escapes to
   `\N{...}`" (was `\uXXXX`, in a live runbook describing a sweep); `doc/PLAN-evacuate-public-repos-programme.md:1229`
   "exempting `/uXXXX-/uYYYY`" and `:1276` "`/uXXXX` escapes with Hebrew comments";
   `doc/PLAN-evacuate-the-rest-of-three-repos.md:856` "`<mode> <sha1> 0/t<path>`" (was `0\t<path>`,
   the quoted `git ls-files -s` output format). The authored-paths rule itself keeps a backslash
   "where the syntax itself requires" it, and `\uXXXX` is such syntax. codex-index-aleppo `8f1fcfd`
   did the same to its `CLAUDE.md:195`, moot since `82aa50b` (14:20 today, after the anchor) reduced
   that file to a breadcrumb. Re-establish: `git grep -n -F "/uXXXX" -- doc`; `git grep -n -F "0/t<path>" -- doc`.

8. **Record error, unfixed: `py/hkq_cmn/verify_mam_suggestions.py:54–56` (`3829585c`) says the three
   maqaf compounds each differ "by one meteg on the compound's second atom".** True of 2Ki 21:12.11
   only: at 2Sa 18:3.9 the meteg is on the first atom of לֹֽא־יָשִׂ֧ימוּ and at Judg 6:1.2 on the first
   atom of בְנֵֽי־יִשְׂרָאֵ֛ל — the JSON's `mam_form` / `comparison_form` pairs show it, re-derived by
   the main session. The same sentence went into holman-ketiv-qere's README in `7a25b34`, since
   emptied. `3829585c`'s own message speaks of 2Ki 21:12 alone and is right. Two smaller stale
   docstrings in the same stream: `py/py_render/rt_suggestion_kinds.py:59–63` still says "a qadma
   added" for Joshua 10:12, though `757aa68a` corrected that form to a doubled U+0599, a pashta's
   stress helper, and `suggestion_kind` now sees a pashta; and `py/main_ingest_mam_suggestions.py:23–29`
   says the corpus check "never fails the run", though since `ac923a85` `check_case` raises when the
   quoted forms do not name exactly one atom, which `mam_suggestion_corrections.py:45–54` records
   happening on Joshua 10:12.

9. **Stale figure, unfixed: CLAUDE.md's "Running tests" baseline says 975 passed and the suite is 973
   at the anchor.** The sentence "A fresh primary checkout run after the Leningrad move passed **975
   passed, 5 skipped, 65 subtests** on 2026-09-03" was written by `05af8728` (18:13) and was true
   then (`56707b45`, `e1bb66ac`, `c3f8b499` and the trio plan's Phase 1 record all measured 975). It
   moved on 2026-09-04: `abb03ec4` −4 (`test_vendoring_policy_paths.py`, 18 → 14 collected),
   `bc36750c` +1, `1f39b6f9` +1, giving the 973 the main session measured on the clean anchor tree.
   The figure to carry is 973 at `b4706759`, with 975 kept as the dated 2026-09-03 record; the same
   dated 975 stands harmlessly in the trio plan (`:139, :199`), the Holman programme (`:499, :848`)
   and the item-1 plan (`:1236, :1299`). Related record error, stream C: `b6bb8fae`'s message and the
   three-repos plan's Phase 2 record say pytest reports no subtest count because `pytest-subtests`
   is absent; the package is absent and pytest 9.1.1 counts `unittest` subtests natively, which the
   Phase 1 and Phase 3 records the same day, the trio plan, CLAUDE.md and today's run all show from
   the same venv — the programme's book-of-job row had settled the identical question on 2026-08-22
   ("find what produces it before concluding it is spurious"). The record paragraph's advice that
   "no later phase should copy a subtest count" was rightly ignored by every later phase.

10. **Record errors, unfixed, in the roster's own rule and its visibility map — the defect the
    2026-09-01 review's finding 4 fixed, recurring one window later.** (1) `in/repo_maintenance_policy.json`'s
    `gitrepos_setup_rule` clauses 1 and 5 still give the roster as 18 folders, with the 2026-09-01
    note that took it from 19 to 18; the window de-listed four more — holman-ketiv-qere (`519e3f4e`),
    book-of-job (`058f6b03`), UXLC-utils (`f3187d73`), codex-index-leningrad (`05af8728`) — to **14**,
    and none of the four commits, nor the three later ones that edited this file, touched the
    clauses. (2) The same file's `repo_visibility` map dropped codex-index-leningrad's entry
    (`05af8728`, following the programme's third-stage item 9: "loses each evacuated repo's entry in
    the same commit that drops its folder") but still classifies `book-of-job`, `holman-ketiv-qere`
    and `UXLC-utils`; the map is 17 entries against 14 folders, `test_repo_visibility_declared.py`
    enforces only workspace ⊆ map, and the three-repos plan's Phase 6 record mentions the map
    nowhere. (3) `doc/PLAN-evacuate-public-repos-programme.md:917` names hbofonts as a vendoring
    `repos` entry; it is only a `foreign_vendored` source. Re-establish: `git diff 4cc0c33 b4706759 --
    all-repos.code-workspace in/repo_maintenance_policy.json`.

11. **Stale doc, unfixed: `State:` lines and Status rows that stop one phase short of what their own
    files record, two new plans with no `State:` line at all, and a deletion hazard the third stage
    already met once.** The doc/ standard (`check_repo_standards.py`'s docstring) puts a `State:`
    line at line 3 of every `doc/PLAN-*.md`, "one of five words plus an optional date".
    1. `doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md:3` says "Phase 0
       complete" while line 167 is "Execution record — Phase 1, 2026-09-03" and the programme's row
       47 says "Phases 0–1 DONE".
    2. `doc/PLAN-evacuate-the-rest-of-three-repos.md:3` says "Phase 5 complete — Steps 1–6" while its
       Status (line 31) says "Phase 6 completed" and the programme calls the second stage DONE.
    3. `doc/PLAN-evacuate-public-repos-programme.md:3–4` names only the third stage's Phase 0 and not
       the drafted fourth stage; its second-stage Status row (line 46, `80c9ad85`) still says the
       sparse vendor "remains and reads MAM-basics" and counts a "15-folder workspace", both retired
       within the hour (`079b1e63`, `05af8728`), so one row says the vendor remains and the next that
       Phase 1 retired it.
    4. `doc/PLAN-holman-meteg-rollout-programme.md` and `doc/PLAN-post-stress-meteg-page-and-holman-m23.md`,
       both new this window, have no `State:` line (line 3 is prose in each; the first carries
       "STATUS: THE WHOLE PROGRAMME IS DONE" at line 8 instead), and the docstring's "all thirteen
       of this repo's doc/PLAN-*.md" now describes nine. The Holman programme says every section is
       an execution record, which under the same standard ("a doc file that only records finished
       work is deleted") makes it a deletion candidate — Ben's call.
    5. Deletion hazard: the fourth-stage draft (`fa0c082d`) lives only in the programme file ("no
       plan file written"), but the programme's DO-NOT-DELETE paragraph (lines 6–16, `5cfc6d4e`)
       conditions deletion on "once the third stage has left it" and the trio plan's Phase 5 (lines
       268–269, `e1bb66ac`) says to delete the programme "only after confirming this plan contains
       their remaining live decisions" — a test the trio plan cannot pass for a stage that is not its
       business. This is the shape `5cfc6d4e` corrected for the third stage, one stage later.
    6. `cd9d3979` left a duplicated half-sentence at the trio plan's lines 164–165 ("in the same
       Empty commit; no `frozen_repos` entry is added." twice), confirmed by the main session.

12. **Immutable-message slip with a record consequence: the five carry commits are titled "29
    metegs off, one on", and their diffs remove 30 (31 in MAM-parsed).** MAM-parsed `5108203`,
    MAM-simple `d2e48e0` and `7a4f21d`, MAM-with-doc `0fe406c`, MAM-OSIS `697dc98`, MAM-for-Sefaria
    `ce1e04c`. The two uncounted removals are at 2 Kings 21:12 — M18's meteg on the resh of ירושלם
    and the meteg on the vav of ויהודה — which reached `in/mam-ws` by `8e3ae6ca`'s download rather
    than by the bot, and which these commits are the first to carry; the bodies name M24 and M34 as
    "the two records outside that count" and 2 Kings 21:12 nowhere. The 31/30 split is M13, whose
    `{{מ:קמץ}}` call keeps both parameters in MAM-parsed. The programme file counts the same thing
    correctly but only implicitly ("this is where M18 finally propagates"); nowhere does it state the
    derivative count. Main-session re-derivation from the diffs: net meteg change per tree 30
    (MAM-parsed `plain`, `plus`), 29 (each of MAM-simple's six vtrad trees). Related immutable slip:
    MAM-simple `d2e48e0` says "88 files in all" for a 63-file commit (88 = 63 + `7a4f21d`'s 25).

13. **Code defects and lint gaps, all latent or low, unfixed:**
    1. `py/main_0_mega.py:148–158` (`a43b3e88`): the guard's second test is `is_dir()`, not "is a
       clone", so a phantom `.claude/worktrees/MAM-simple` left by an earlier misdirected run —
       exactly the 2026-09-04 incident's residue, which the docstring's repair recipe copies across
       rather than deletes — passes it, and the docstring's "a destination that is not already a
       clone is refused" overstates the check. Latent: `.claude/worktrees/` holds nothing today. A
       `.git` presence test, the shape `paths.display_path` already uses, would close it.
    2. `py/check_html_syntax_and_sanity.py` (pre-existing, from book-of-job) has no
       `sys.stdout.reconfigure(encoding="utf-8")` and dies with `UnicodeEncodeError` on the first
       Hebrew issue line whenever stdout is redirected — the exact failure the user-level UTF-8
       rule says a tracked script gets fixed for, not prefixed. Its scope no longer fits this tree
       either: at the anchor it reports 7,580 issues over 429 pages, of which 3,881 are "broken
       fragment (same-file)" false positives (the anchors are present; `id="row04"` sits on a
       multi-line `<article>` tag) and 3,664 "unknown CSS class" against the one stylesheet it knows,
       while `uxlc/` and `holman/` carry their own.
    3. `mam_suggestion_extract._parse_prose_list` (lines 308–309) `continue`s past a heading whose
       book abbreviation is not in `STD_BOOK_NAME_BY_HOLMAN_ABBREV`, while the table's comment says an
       unseen abbreviation "is a message whose shape changed" and the module raises on every other
       drift; a crop-less case in a new book would vanish (a case with a crop is caught by
       `_assign_prose_list_images`).
    4. `_xsd_parser` with a missing `xml_xsd_path` falls through silently to the network (the
       schema still built against a nonexistent path on this online machine), so on a filtered
       network the failure would again be the misleading `xml:lang` QName error; a
       `Path(...).is_file()` check would name the cause.
    5. `py/tests/test_versification_and_cantillation_doc.py:10–25` composes
       `sibling_repo("MAM-simple") / "gh-pages" / …` at module scope and reads it bare at line 25, so
       with MAM-simple absent it raises a bare `FileNotFoundError` with no `REPO_MAM_SIMPLE_DIR`
       advice; `8da39b48`'s "all eleven test files … through the same wording" is false for this
       one file, which the commit did not touch. Message quality only.
    6. Lint gaps: `test_sibling_reach.py`'s "FIVE MECHANISMS, ALL OF WHICH THIS COVERS" omits
       `py/repo_util/repo_selection.py:74–105`, which resolves every workspace folder as
       `workspace_dir / folder["path"]` and so reaches github-misc, hbofonts, phonetic-hbo and Taamey_D,
       roster-but-undeclared; the machine-paths lint scans `out/` and `gh-pages/` only, while
       program-written trees now also sit under `uxlc/out/`, `book-of-job/out/`, `leningrad/lenin-wiki/`,
       `holman/`, `py-examples-out/` and two `doc/` files (a whole-tree scan found no offender);
       `check_repo_standards.py`'s AGENT_BRANCHES and `git_worktree_cleanup._AGENT_BRANCH_PREFIX`
       count only `claude/`, so the four merged Codex branches in MAM-basics report as 0 (finding 18).

14. **Reachability, Ben's decision: at the anchor eight tracked pages are linked from no page, where
    the last review found one, and the landing page names no entry for the three sub-sites the
    window landed.** The sanity lint over the archived anchor tree lists as orphan
    `book-of-job/index.html`, `uxlc/index.html`, `uxlc/clc/2Samuel.html`, `uxlc/clc/Genesis.html`,
    `uxlc/clc/Proverbs.html`, the two `holman/JC3 The Biblical Text in the JC Edition #19-ז…` pages,
    and `wlc/index.html` (the one the last review recorded as settled). `gh-pages/index.html` links one
    book-of-job article and nothing under `uxlc/`, `holman/` or `aleppo/`, so a reader starting at the
    site root reaches the Holman tree (6 pages) and the UXLC tree (91) only through the retired
    hosts' redirect stubs or by URL. `test_site_index_links.py` stops its reverse check at the deploy
    root by design, and its docstring records Ben "at peace with no lint reaching
    `gh-pages/holman/index.html`" — a decision about lint, not about whether the landing page should
    name the sub-site indexes. Ten orphan images under `wlc/accgram/img/`, all with `-unused` in their
    names, are pre-existing.

15. **Record inconsistencies and stale docstrings, unfixed, smaller:**
    1. `doc/review-findings-2026-09-01.md`'s "fifteen CRLF phantoms" (also `bc24f7ad`'s message) is
       MAM-basics' own subset — `doc/mp-claims.md`, twelve `out/tmpl-survey-*/` dot files and two
       `py-examples-out/` files — of the **29** paths `doc/mega-pipeline-review-phase-13-2026-09-01.md`
       (MP13-02) counts across the forest (15 + 1 MAM-parsed + 12 MAM-with-doc + 1 MAM-simple), which
       `bc24f7ad`'s writers and the two vendored-copy refreshes did cover; one clause naming the 14
       sibling files as the same class would reconcile the two. Also `bc24f7ad`'s "~25 MAM-private
       rows" against `78370e83`'s and the doc's 27, neither re-measurable now.
    2. `py/tests/test_no_machine_paths_in_artifacts.py`'s docstring says "twelve tracked files
       outside `out/` and `gh-pages/` carry one"; by the lint's own regex there were **27** at
       `86c87d24` (no sub-pattern yields 12) and 50 at the anchor.
    3. `py/repo_util/maintenance_policy.py:91–92` still cites "mgketer's two `py/python_modules/`
       files" as the policy's per-file `overrides`, which `abb03ec4` emptied to `[]`.
    4. `doc/holman-meteg-vs-mgketer.md:48` refers to "the two display artifacts noted under M13 and
       M18 below"; the section covers M13 and M22, and no M18 footnote exists in the file.
    5. `_collect_text_fragments`' docstring gives its setuma/petucha and special-letter counts
       (1519/35, 404/26, 1545/8, 3/15; 51) as MAM-parsed counts; they count nodes the collector
       reaches, and the whole tree holds 1525/41, 404/26, 1546/9, 3/15 and 95, the surplus under the
       dual-cantillation template's א and ב parameters, which the collector never enters.
    6. `leningrad/` landed with no `DATA-LICENSES.md` row, though
       `leningrad/page-snips/430B-col2-line10-Lam2v3-akhla.png` is a crop of a Leningrad Codex
       photograph and `leningrad/lenin-wiki/*` derives from J. David Stark's CC-BY-4.0 index; every
       other landed crop directory got a "no grant is made or implied" row, and the trio plan's Phase
       1 record asserts "no … licence-inventory row applied" by fiat. (The pre-existing
       `doc/ms-snips/` crops have the same gap, outside this window.)
    7. Sibling spellings that were right in a source clone and are wrong inside MAM-basics:
       `book-of-job/doc/reading-mam-simple.md:25, 27`, `holman/doc/holman-manuscript-citations.md:11,
       84, 158`, `holman/doc/uxlc-email-count-disagreements.md:6` and
       `holman/docs-not-served/table_data_fields.md:35` spell this repo's own modules as
       `../MAM-basics/py/…`; `leningrad/page-snips/README.md:39` points at `../../cam1753/page-snips/…`,
       the Phase 3 landing directory, which does not exist yet (self-healing when Phase 3 lands
       there); `doc/book-of-job-artifacts.md:15` reads as though the HTML and CSS sit under
       `book-of-job/out/` (only the 6 JSON do).
    8. `holman_email_common.py:10–18` defers de-duplicating five helpers of `uxlc_email_extract.py` on
       a condition ("no other session is in `uxlc_email_extract`") that has long lapsed;
       `uxlc_email_extract.py:484–595` still holds `_sender_display_name`, `_email_key`,
       `_plain_text_body` and `_utc`. `holman_email_common.py:3` ("holman-ketiv-qere is public and every
       `.eml` …") and `main_ingest_uxlc_emails.py:22` ("needs the sibling UXLC-utils clone") went stale
       with the evacuation.
    9. The trio plan's Phase 0 and Phase 1 "tracked bytes" (429,462,145 and 429,477,537) are
       working-tree bytes under a CRLF checkout of `*.csv`, 464,191 above the blob sums both times,
       while the records say `git ls-files -z`; a re-measurer from blobs gets a "mismatch" that is not one.

16. **Prose rules, unfixed, in this window's files.** Against the hebrew-prose skill and the
    user-level prose rules, listed by rule:
    1. "carries" / "bears" for a letter or text having a mark ("just say has"): rendered once, on
       the Archived page's M24 "Why:" line ("the two letters that would carry it",
       `mam_suggestion_dispositions.py:369`); in JSON prose at `post_stress_meteg.py:933, 994, 1040`;
       in comments at `rt_mam_suggestion_card.py:49`, `template_names.py:90`, `post_stress_meteg.py:814`;
       in docs at `doc/PLAN-holman-meteg-rollout-programme.md:75`,
       `doc/PLAN-post-stress-meteg-page-and-holman-m23.md:1148, 1182, 1193`,
       `doc/holman-meteg-m13-qamats-template.md:34, 51`, `doc/holman-accent-placement-four.md:73`,
       `py/ws/holman_meteg_edit_spec.py:331`.
    2. The "own" tic: rendered once (M24: "a syllable of its own", `mam_suggestion_dispositions.py:362`);
       three times in the survey JSON's prose; about 25 window-added comment and docstring lines in
       the Holman modules (`.novc/review-2026-09-04/B_prose_scan_report.txt` lists them) and about 30 times across 17 of the
       rollout's 44 messages.
    3. Announced counts left unnumbered: `mam_suggestion_corrections.py:69–76` ("for three reasons")
       and `uxlc_atom_index_notes.py:23–28` ("Two guards"); in messages `32167f2f`, `681df4a4`,
       `995251a6`, `95040d8f`, `b20f7aff`, each following its count with lead-ins rather than numerals.
    4. "one … the other": `mam_suggestion_extract.py:63–64`;
       `doc/PLAN-evacuate-public-repos-programme.md:538` ("Stubs for one repo of three, and an archive
       for the other two", the sides named only by reference to decision 2). The window's two "the
       former" hits (`823358a3`, `fdf8f3ec`) are the adjective, "the former repository", and are not
       violations.
    5. Comment lines whose first strong character is Hebrew: `uxlc_atom_index_notes.py:42–43`, the
       flip `bdab03a7` removed from four other lines.
    6. Numbered verse vs chanted verse, `88ab9cc3`'s distinction, right where applied and missing at
       five sites stating the same 221 / 23,184 measurement: `doc/PLAN-holman-meteg-rollout-programme.md:181–182`,
       `doc/PLAN-post-stress-meteg-page-and-holman-m23.md:1155–1157`,
       `doc/post-stress-meteg-census-2026-09-03.md:27`, the page's M23 paragraph
       (`py/author_site/post_stress_meteg.py:478`) and the JSON `scope` string.
    7. Coinage before definition: "wsgo" at `PLAN-holman-meteg-rollout-programme.md:92` and the
       item-1 plan's line 14, glossed at line 508. Two rendered-page wordings on `post-stress-meteg.html`:
       "the comparison forms on his card are what he was sent" (Holman sent them) and "so nothing
       here rests on an entry's position in a list" (implementation jargon).
    8. Pre-existing on the page stream B extended: the ketiv/qere cards' Hebrew comparison cells
       (`rt_comparison_table.py:65`; 177 on the Active page, 100 on the Archived) lack `dir="rtl"`,
       while every suggestion-card cell has it.

17. **Instruction-file plumbing, one variant tracked nowhere.** `~/.claude/CLAUDE.md` and both
    tracked skills (hebrew-prose's five files, prune-claude-state) are byte-identical to
    github-misc's `dot-claude/` copies; `~/.codex/AGENTS.md` (79,274 bytes, 998 lines) is byte-identical
    to `dot-Codex/AGENTS.md`; the Codex-visible `~/.agents/skills/hebrew-prose/` and
    `worktree-forest/` are byte-identical to their tracked canonicals. **But
    `~/.agents/skills/prune-claude-state/SKILL.md` is a hand-adapted variant** — renamed
    `prune-Codex-state`, its text rewritten to "Codex's own persisted state" and to plan files under
    `~/.Codex/plans/`, a directory that does not exist (`~/.claude/plans/` does) — tracked in neither
    `dot-claude/` nor `dot-Codex/`, while `dot-Codex/README.md` says the Codex-visible copies of the two
    shared skills are the canonical trees deployed, and the required comparison it names covers
    hebrew-prose only. Either the variant is wanted, and wants tracking and a README sentence, or it
    is drift. github-misc is private; this is the series' standing exception, and only the copies'
    identity was compared.

18. **Process and hygiene, recorded for Ben's decisions:**
    1. Trailers: 26 non-merge MAM-basics commits carry no `Co-Authored-By` at all (the whole Holman
       lane `3c5dc796` … `e3882ea1`, the whole book-of-job lane `050c7bb8` … `48b9c55b`, ten UXLC-utils
       lane commits `137eff43` … `80c9ad85`, plus `83fe66fd`, `c46dee13`, `706395bf`, `463e47c0`), so
       they read as Ben's own hand-made commits, six of them subject-only including the 379-file Land
       commit; codex-index-leningrad `aa603a9` likewise. Four default merge messages carry none
       (`c476452c`, `fdbd3466`, `9af532fd`, `18d17e84`). The Codex trailer is spelled three ways
       (`Codex <noreply@openai.com>`, `Codex <codex@openai.com>`, and absent), so `doc/dual-agent-review.md:260`'s
       attribution of `706395bf` to Codex rests on the doc, not the commit. Every Claude-authored
       commit carries its trailer.
    2. Branches: the last review's "only main, locally and on origin" (`6d0aef7b`) no longer holds.
       MAM-basics has four merged local branches (`remediation/change-log-fail-closed-2026-09-02`,
       `remediation/mp02-01-extraction-2026-09-02`, `review/holman-meteg-comments-2026-09-04`,
       `review/mega-pipeline-2026-09-01`) and the merged remote `origin/review/mega-pipeline-2026-09-01`
       (tip `1635b846`); MAM-with-doc one merged local `remediation/mp02-01-extraction-2026-09-02`. All
       are fully merged (`git branch --no-merged main` is empty in both); deletion is Ben's call under
       the ask-before-deletion rule. The standards sweep reports AGENT_BRANCHES=0 for both because it
       counts `claude/` only (finding 13.6).
    3. The roster file was unparsable JSON on `main` for 38 minutes, from `f3187d73` (16:05:28) to
       `56707b45` (16:43:50), across seven commits (`74c16b3e`, `dc24164b`, `8184104a`, `86ba7b56`,
       `6a1c0655`, `df4b5661`, `14ca4b48`); `repo_selection.load_workspace_repo_dirs` uses plain
       `json.load` and runs before every `main_repo_util.py` action, so every sweep and
       `test_repo_visibility_declared.py` were dead across those commits. Confirmed by parsing the
       blob at each commit.
    4. Residue under `GitRepos`, which clause 6 of the roster rule bars: `.pytest_cache/`
       (created 2026-09-03 15:41, one minute after `067f78fe`'s worktree suite run; its `nodeids` is
       `[]`, so some pytest took `GitRepos` as its rootdir and collected nothing) and `.codex/worktrees/`
       (empty, created today). The codex-index-leningrad clone is finding 4.
    5. `py/main_0_mega.py:103` hardcodes `_PRIMARY_CLONE = "C:/Users/BenDe/GitRepos/MAM-basics"` in
       tracked source (deliberate per its comment; noted against the machine-path convention).
    6. Process notes honestly recorded in the trio plan and moot since finding 4: the Leningrad clone
       was deleted before `git worktree list` was consulted, against the lane's own Step 6 order, and
       re-cloned at 18:14:40. `abb03ec4`'s title "so nothing here resolves that clone" overclaims — the
       census step and `paths.al_hatorah_phonetic_dir` still resolve MAM-private, as its body and the
       lint's declaration say.
    7. The eleven-chapter download route the Holman programme leaves open will also bring one
       unreviewed non-meteg edit: live 2 Chronicles 28 wraps דַרְמֶ֘שֶׂק֮ at 28:23 in a `{{נוסח|…}}`
       documentation note absent locally, while the programme reserves its "week of edits nobody
       here has reviewed" warning for the full-download route.

19. **Immutable-message slips, the window's census, recorded only.** (a) `81fac842` "of the eight
    files the branch touches": ten, eight modified plus the two it adds. (b) `2e66268a` "14 sibling
    folders": 14 folders including `.`, so 13 siblings. (c) `823358a3` "re-downloaded … eight times":
    eight commits touch the path, one the initial add and one the retirement, so six re-downloads;
    "three that post-date this XML release": three changesets, 41 records. (d) `ac923a85` "The four
    maqaf compounds": three; `757aa68a` "subsumes the WHITESPACE_TMPL_NAMES branch": `147e9e4f` found
    that false and `mam_plus_verse_data.py:213–223` records it. (e) `d2e48e0` "88 files" (finding
    12). (f) `208f65a3` calls its eighteen "ketiv/qere rows" in a paragraph about suggestion
    dispositions. (g) `988f2f76` "noise class (2)" and `78370e83` "noise kind (1)" for the review
    doc's one enumeration. (h) `56707b45`'s "1 failed, 973 passed → 975" is explained by `62a10b03`'s
    concurrent policy edit (+1) plus `df4b5661` (+1), as its message half-says.

## Open ends the window itself declares (not findings)

The Aleppo and Cambridge 1753 lanes executed beside this review (fifteen commits past the anchor
by 15:16), so the third-stage records this review read are already moving;
finding 11's `State:` items are the ones most likely to be overtaken. The Holman programme's item 1
survey corpus predates the rollout (`369d5cd2` records Ben tolerating that). The eleven deferred
Holman meteg edits are Ben's, by either route (`94d4bf5f`), and the next fr-wikisource refresh will
carry them plus Avi Kadish's edits since (2 Chronicles 28:23's note among them) — a known-cause
future diff that will want a mega. The MAM-with-doc change log is one mega behind (finding 2). The
fourth stage's six sub-questions are open and dated. MAM-basics #264 ("A workspace folder that
exists but is not a git repo drops out of every sweep, silently") was filed at 13:04 local today,
after the anchor, and was not read. skadish1's 2026-08-19 question on #185 is still unanswered
in-thread (last comment his), and #225–#230 were untouched in-window. The survey's currency TOTAL
differs from a count of every text field of MAM-simple's non-dual verses by nine metegs
(38,179 vs 38,170), six of them in `sdt-note` text; all 221 per-verse differences match, so the
gap is in how the loader counts, not in the differences — unresolved, not a defect.

## What this review did not check

1. Anything in MAM-private, github-misc beyond the plumbing identity, or hbofonts: the mgketer
   reports (so the "30 of 30 match" and the 67 → 37 / 5 → 4 totals are taken from the record), the
   Phonetic MAM standard set (so the survey's 231 and the currency snapshot side are unverified),
   Yeivin §239 and the Breuer claim behind M24, and the private ledger commits the records cite.
2. The raw mailboxes under `.novc/eml*/`, the Google Sheet and its Apps Scripts.
3. Nothing was regenerated: every page was compared to its tracked data as it stands, and the
   seven post-anchor commits were not reviewed.
4. GitHub Actions run IDs cited by the lane records (the deploys were verified by live effect);
   Phase 13's aggregate SHA-256s and two-run determinism; the five named UXLC releases' raw counts;
   whether `in/xml.xsd` is byte-identical to the W3C's file; the eight bot-touched Wikisource
   chapters not fetched; the finer 12/2/2/1/1 split of `208f65a3`'s eighteen closures.
5. Whether the twelve pre-existing non-MAM-normal runs of finding 1 are deliberate illustrations.
6. Whether the 48 repo-root-relative links in `uxlc/doc/` are meant to stay as an execution record.

## For the reconciliation with the Codex review

Anchors for bucket-sorting: MAM-basics `4cc0c33..b4706759`; the sibling ranges in the table above;
book-of-job `fea3acd..c8a6bbf`, holman-ketiv-qere `aacd3ee..ca55c4a`, UXLC-utils `a2768f4..2745c65`
on GitHub. Each finding above carries the commit, the file and line as of `b4706759`, the claim, the
measurement, and the command or `.novc/review-2026-09-04/` script that re-establishes it, so a bucket-4 conflict
can be checked by hand without re-deriving the whole window. The reconciliation section goes below, under `## Reconciliation with the Codex review`, per
`doc/dual-agent-review.md`. The untracked original at `.novc/review-findings-2026-09-04.md` is the
frozen blind draft, not the file to append to.
