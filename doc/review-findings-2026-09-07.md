# Findings of the 2026-09-07 review of the public repos since 2026-09-04

State: acted on 2026-09-08. Finding 23.2's worktree housekeeping is outside remediation and Ben will
track it separately. Written 2026-09-07 as the Claude half of the second dual-agent review under
`doc/dual-agent-review.md`, Design A: this file was frozen before any Codex reviewer read it, and the
Claude session neither read nor sought a Codex half (no file named `codex-review-findings-2026-09-07*`
exists, and nothing under `~/.codex/` or `Documents/Codex/` was read beyond the directory listings
recorded under finding 23). Nothing was fixed. Before this file was committed, a check with
`has_std_mark_order` over its 20 Hebrew runs found two in Unicode-normal order — lifted from the data,
which is in MAM-normal order, and reordered by the file-writing tool on the way in, which is the
mechanism CLAUDE.md's first section names — and `give_std_mark_order` put them back
(`.novc/review-2026-09-07/fix_findings_marks.py`). The reconciliation goes at the end of this file under
`## Reconciliation with the Codex review` once the Codex review is stable, and the dispositions under
a later `## Dispositions after remediation` section, per that document.

## Scope, anchors and census

Fourth review under the public-repos-only scope. It covers committed work from the 2026-09-04 review's
anchors through the moment this review started, 2026-09-07 about 10:35 local, when MAM-basics' HEAD
was **`8bf586a3`** (2026-09-07 10:23, "Make Design A the default dual review"), the tree was clean and
`origin/main` stood at the same commit. **The tree moved under the review, as it did under the last
one.** A session live in the Codex worktree `C:/Users/BenDe/.codex/worktrees/MAM-basics-post-stress-meteg`
committed five times between 11:26 and 11:53 (`6b5e4a40`, `7b11fd6b`, `e3d1344f`, `b0533f7b`,
`11fb9c24`, all with the Claude Fable 5.1 trailer) and `main` took them by the merge `d5a2238f` at
11:56, pushed. **None of those six commits was reviewed.** Two of them overtake findings below and are
named there (finding 6). Every figure in this file was measured at `8bf586a3`, on the clean tree, by
`git show`, or on GitHub for the repos that have no clone; line numbers are as of `8bf586a3`, and the
six later commits touch only `py/tests/test_sibling_reach.py`, `py/tests/test_vendoring_policy_paths.py`,
`py/vendoring/discover.py`, `py/repo_util/repo_selection.py`, `py/mb_cmn/provenance.py`, six files
under `MAM-simple/py-examples/`, `doc/vendoring-inventory.md` and `out/vendoring_compare_out.txt`.

Anchors (start → end) and counts, re-measurable with
`git -C C:/Users/BenDe/GitRepos/<repo> log <start>..<end> --oneline`, or with
`gh api repos/bdenckla/<repo>/commits?since=2026-09-04T16:40:00Z` for the repos read on GitHub:

| Repo | Range | Commits | Non-merge |
|---|---|---|---|
| MAM-basics | `b4706759..8bf586a3` | 257 | 220 |
| MAM-for-Sefaria (clone) | `ce1e04c..cf23b478` | 1 | 1 |
| phonetic-hbo (clone) | since 2026-09-04T12:40 → `7322b665` | 1 | 1 |
| MAM-simple (GitHub) | `7a4f21d..9a350be5` | 1 | 1 |
| MAM-parsed (GitHub) | `5108203..c9e04c49` | 2 | 2 |
| MAM-with-doc (GitHub) | `0fe406c..904c9fa1` | 1 | 1 |
| codex-index-aleppo (GitHub) | `8f1fcfd..82aa50b7` | 2 | 2 |
| codex-index-cam1753 (GitHub, archived) | `3667b6c..aab417b1` | 1 | 1 |
| diffable-pointed-hebrew (GitHub, archived) | `dd1fdb9e..a30ff8aa` | 2 | 2 |

That is **268 commits across nine public repos**. Seven public repos were quiet: MAM-OSIS, Taamey_D,
codex-index-leningrad, book-of-job, holman-ketiv-qere, UXLC-utils and wlc-utils. Three clones are
private and fall to the private series: MAM-private (2 in-window commits), github-misc (8) and hbofonts
(0); the series' one deliberate exception was applied again, github-misc's instruction-file plumbing
being byte-compared (finding 22).

All 220 non-merge MAM-basics commits are authored Ben Denckla. **121 of them carry no `Co-Authored-By`
trailer and 96 are subject-only**; the 99 that carry one spell it four ways (`Co-Authored-By: Codex
<noreply@openai.com>` 92, `Co-Authored-By: Codex <codex@openai.com>` 3, `Co-authored-by: Codex
<noreply@openai.com>` 2, one Claude Opus 5, one Claude Fable 5.1). 72 non-merge commits sit on
`main`'s first-parent line and 148 arrived through the 37 merges, 31 of them titled `Merge branch
'post-stress-meteg'`; 21 of those merges fell between 22:19 and 23:52 on 2026-09-05, one per branch
commit. The window added 1,346 tracked files and modified 205, deleting and renaming none: 4,161 →
**5,507** tracked files, 1,162 → 1,219 `.py`, `gh-pages/` 1,501 → 1,822 files (429 → 576 HTML). The
new top-level trees are the fourth stage's four landed products (`MAM-simple/` 386, `MAM-parsed/` 205,
`MAM-for-Sefaria/` 165, `MAM-with-doc/` 5, plus `gh-pages/MAM-with-doc/` 204, `gh-pages/MAM-parsed/`
36, `gh-pages/MAM-simple/` 4, `gh-pages/MAM-for-Sefaria/` 3) and the third stage's last three lanes
(`aleppo/` 142 plus `gh-pages/aleppo/` 4, `cam1753/` 99, `diffable-pointed-hebrew/` 8).

`GitRepos` holds 8 clones for a 7-folder roster (the extra is MAM-for-Sefaria, finding 9). The review
ran as five agent streams plus the main session: (A) the third-stage closeout of the 2026-09-04
afternoon, the two maintenance-runbook additions and the three line-break commits; (B1) the fourth
stage's landings, licences, stubs, emptyings and records; (B2) the fourth stage's repoint code,
configuration and product prose; (C) the post-stress-meteg survey and its seven pages; (D) the
remediation of the 2026-09-04 review, disposition by disposition. Every script and output is untracked
under `.novc/review-2026-09-07/` on the machine that ran the review (copied there from the session
scratchpad before this file was committed; prefixed `A_`, `B1_`, `B2_`, `C_`, `D_` per stream,
unprefixed for the main session).

## Tree health at `8bf586a3`: green, with the suite at 976

- Suite: **976 passed, 5 skipped, 65 subtests** (`.venv/Scripts/python.exe py/main_test.py -q`,
  126.22 s, clean tree before and after); collect-only 981 = 976 + 5, every item under `py/tests/`
  (finding 8 says what that leaves out). CLAUDE.md's "976 passed, 5 skipped" of 2026-09-07 holds.
- `ruff check py` clean; `black --check py` clean at **1,164** files (1,162 at the last review); black
  and ruff also clean over the 54 `.py` under `MAM-simple/py-examples/`, `MAM-simple/py/`,
  `MAM-parsed/py-examples/` and `MAM-for-Sefaria/py/`.
- Zero `sys.path` mutations in tracked `.py`, under `py/` and under the landed trees alike (every
  match is a docstring or comment).
- `--check-repo-standards --workspace-file all-repos.code-workspace --visibility public` sweeps **4**
  repos (11 at the last review) and reports no new problem: MAM-basics LINKED_WORKTREES=1 (the Codex
  worktree, finding 23), HEX_ESCAPES 80 (79), NFC_H_DOT 30, NFC_LATIN 49 (38; the landed data), the NFC
  lint itself green; Taamey_D GITATTRIBUTES_LF=False as before.
- Markdown links: 240 relative links in 163 tracked `.md` files, one dead and pre-existing
  (`misc/what-is-mam/img/provenance-misc.md:6` → `.github/prompts/capture-what-is-mam-slides.prompt.md`,
  file last changed 2026-05-04). The 53 dead links of the last review's finding 6 are gone.
- Mark order over every window-changed `.py`, `.md`, `.json`, `.html`, `.css`, `.js` and `.txt` file
  outside the landed data trees, `out/`, `misc/`, `holman/`, `uxlc/` and `in/mam-ws*` (216 files): the
  only runs new in the window are the 48 + 2 in the two landed Aleppo pages (finding 16); the other 108
  runs sit on pre-existing lines of 20 files (the four Holman notes, four plans,
  `doc/review-findings-2026-09-01.md`, `doc/metsudah-vs-ctr.md`, `doc/scan-pages.md`,
  `doc/ms-snips/README.md` and nine `py/` files), outside the window and not examined for whether they
  are deliberate illustrations of Unicode-normal order, as the last review also left them. The Holman
  pages and the seven post-stress-meteg pages are clean (`mark_order_window_scan.py`).
- Pages: every deploy in the window succeeded — MAM-basics run 34132735851 at `8bf586a3`, MAM-simple
  34038057050 at `9a350be5`, MAM-parsed 34055284061 at `c9e04c49`, MAM-with-doc 34062108606 at
  `904c9fa1`, MAM-for-Sefaria 34049004202 at `cf23b478`, codex-index-aleppo 33905367876 at `82aa50b7`
  (the stub commit's run cancelled by the concurrency group, as designed), phonetic-hbo 34010529936
  at `7322b665`.
- Issues: nothing was opened, closed, commented on or relabelled in the window; #264 (filed 13:04 on
  2026-09-04, after the last anchor) is the newest, with 0 comments, and was read by this review; 95
  open.

## What verifies sound, stream by stream

**The third-stage closeout, the runbook additions and the line-break commits (stream A).** Blob
identity holds for all three landed products: Aleppo's 175 source blobs at `8f1fcfd5` map to 146
paths here (142 `aleppo/`, 4 `gh-pages/aleppo/`) plus the 24 `MAM-XML/` blobs `df61173a` carried
(170 blobs, 39,905,269 bytes, the source's 39,924,885 less the five host files), 139 identical at
HEAD and the 6 that differ each changed by a named later commit; Cambridge 1753's 152 → 100 (14
spreads, 25,262,600 bytes; the 28 page JPEGs and the 24 XML deliberately not landed); diffable-pointed-hebrew's
19 → 7 (the eight `mb_cmn/` copies, the old command and its `.vscode/` dropped). The Aleppo manifest
equals the source's three pages; each legacy URL answers 200 with all four carriers and each target is
byte-identical to the tracked page; `test_redirect_manifest.py` covers the row (9 of 9). Archive
states match every claim in CLAUDE.md and the trio plan (aleppo not archived, cam1753 archived,
leningrad archived, diffable-pointed-hebrew archived; open issues 0, 0, 0, 0). The readers resolve
only tracked paths; `py/check_cam1753_all.py` passes 4 of 4 (160 of 160 words) and `py/check_ac_all.py`
fails in exactly the two pre-existing ways the records name (word finding 160 of 160 on the
`found=1of2 expected=1` comparison; line breaks with 92 issues), both reports regenerating
byte-identically to the tracked ones when written to scratch. The fourth-stage Phase 1 record's
"seven files, ten diacritic-only differences" for `cam1753/cam1753-line-breaks/` re-derives exactly
(seven meteg removals or additions, two rafe additions, one meteg addition). The landed command
`py/main_diffable_pointed_hebrew.py` reproduces `tiny-sample-output.json`, `sample-output.json` and
both `misc/zarqa-table-diff/*.dph.txt` byte for byte; `tiny-sample-output-normalized.json` differs at
two lines, as the trio plan's lines 356–361 say (the source's `--normalize` was `unicodedata.normalize("NFC")`,
fetched from `dd1fdb9e`, and was deliberately not moved). Every figure in the 27 listed commit messages
re-derives.

**The fourth stage's landings (stream B1).** The plan's Phase 0 table re-derives exactly for all six
repositories. Blob identity holds at every Land commit — MAM-parsed 95 of 95 (29,936,589 bytes),
MAM-with-doc 272 of 272, MAM-for-Sefaria 166 plus two same-commit adaptations — and every difference
at HEAD is a named later commit's. All 144 `MAM-parsed/historical/` JSON blobs match their six source
commits (84,572,003 bytes), every `releases.json` boundary is stored, and `manifest.json` records the
source and landing commits. The four manifests equal the sources' html sets (2, 1, 22, 113); every one
of the 138 legacy URLs answers 200 with all four carriers and every target answers 200; each host's
catch-all forwards; `test_redirect_manifest.py` passes 9 of 9. The four redirect hosts hold exactly
README, workflow, the two dotfiles, the stubs and `404.html`, none archived, `main` at the recorded
commit. All nine Pages runs the records name succeeded at the commits they are paired with. Sparse-checkout
instructions exist (`MAM-simple/README.md:28–40`, `MAM-parsed/README.md:82–98`). Phase 5 (MAM-OSIS)
is unstarted and described consistently: `py/main_mam_osis.py:10–19` still writes the sibling, which
is in both workspace files and the visibility map.

**The fourth stage's repoint (stream B2).** `test_sibling_reach._scan()` at HEAD equals the
declaration, with no site resolving a retired sibling in normal operation: MAM-OSIS through
`main_mam_osis.py`, MAM-parsed only in `--legacy-history` mode and in the portable reader's unused
default, MAM-private through the census step and `paths.al_hatorah_phonetic_dir`, and a temporary
redirect-host clone through `stubs.py:288`. Every repointed writer is `repo_root()`-relative. Normal
change-log mode never touches a sibling (all six boundaries are stored snapshots) and legacy mode
fails loudly with `REPO_MAM_PARSED_DIR` / `REPOS_ROOT` advice. `paths.py`'s functions behave as their
docstrings say; every `require_*` raises rather than skips; no new skip guard entered any of the ten
changed tests. `doc/process-documentation/pipeline.dot` is byte-identical to
`pipeline_graph.render_dot_text()`. The four vendored example trees pass black and ruff; the four
example entry programs resolve their inputs from the cwds the mega sets.

**The post-stress-meteg survey (stream C).** All seven pages regenerate byte-identically from the
tracked JSON (`gen_html_files` to scratch with `trust_survey=True`; `pin_claims` passed). Every figure
on the seven pages re-derives from the JSON and the JSON's arithmetic holds (census 233,586 / 13,091 /
178 / 1.3% and 29,605 / 1,814 / 54 / 2.9%; the type table 123 + 60 + 42 + 7 = 232; the type-1 rows
103 + 12 + 7 + 1 = 123, which is `78e711f6`'s fix of the earlier 113; Fit for MAS 496 records,
203 with MAS, 293 lacking, 40.9%). From the landed MAM-simple tree: the 18 dual-cantillation numbered
verses, the 23,184 / 38,170 currency figures, the 154 / 136 / 18 overlap, all 232 MAS word pairs and
the 215 / 17 next-word split reproduce exactly. **The stress oracle is publicly re-derivable**:
phonetic-hbo's published pages mark the stressed syllable of every chanted word, and a walk over all
23,202 verses (`C_phon_oracle.py`, 0 parse problems) reproduces all 232 MAS records with matching
stressed syllables, Isaiah 23:12 ק֣וּמִֽי (M23) included. Footnotes φ1–φ7 are sequential, each referenced
once and resolving; every Hebrew table cell is `dir="rtl"` and no rtl cell lacks Hebrew; romanizations
are in `span.romanized`; no English sentence opens on a Hebrew word; mark order is MAM-normal in the two
modules, the JSON and the pages (0 of 1,205 page runs off); the "next" vocabulary of `d325a21b` holds
in the JSON keys, the pages and the docs. `02f90095`'s scanner change (a positioned `Token` and one
`ATN_H → GALGAL` rule) alters no tracked artifact but the survey JSON, U+05A2 occurring 0 times in
`out/wlc422-kq-u`; `18667671` changed no `gh-pages/wlc` page. `_syllable_of`'s `default=0` misclassifies
nothing (594 pre-nucleus metegs probed; the one stressed-first-syllable case, Job 31:7, is a silluq and
is read as one).

**The remediation of the 2026-09-04 review (stream D).** Eleven of the nineteen disposition rows hold
in full (1, 2, 3, 7, 8, 10, 12, 13, 14 as scoped, 15, 19); row 6 holds for what it claims; row 5's
repointing holds; five hold in part (4, 9, 11, 16, 18; finding 11 below) and row 17 is not checkable
on the public side. Re-derived exactly: the mark-order check `OK … 459 files`, the nine named runs and
every Hebrew run of the Holman JSON and both Holman pages MAM-normal; the change log's 56 records and
58 cards dated 2026-09-04 with the 31 / 8 / 6 / 5 / 4 / 3 / 1 split; the `uxlc/doc/` dead links
48 → 47 → 0 at `b4706759` / `9eedccbd` / `887f7fb8`; `gh-pages/index.html` linking the three sub-site
indexes; the Holman Archived page's 34 M cards agreeing with the JSON card by card, 0 comparison-value
cells lacking `dir="rtl"`; the roster and the visibility map both exactly seven; the HTML checker's
UTF-8 reconfigure and same-file-fragment fix (0 issues on `gh-pages/book-of-job`); the Codex-only
redirect-manifest wording fixed by `726daafd`.

**Main session.** The trailer and merge census, the branch and worktree census, the roster and
visibility map, the doc/ `State:` lines (all ten `doc/PLAN-*.md` carry one from the standard's five
words; every `doc/review-findings-*.md` has `acted on`), the instruction-file plumbing, the
GitHub-side state of sixteen repos, the diffable-pointed-hebrew regeneration, the `misc/` diff, the
mark-order scan, the markdown-link check, the standards sweep, the suite, black and ruff.

## Findings

In rough order of consequence. Nothing was fixed; where a commit after the anchor fixed something, the
finding says so in its lead. Line numbers are as measured at `8bf586a3`.

1. **Data defect, unfixed: the shared MAM-simple XML reader drops one word of Deuteronomy 32:6, and
   `5fad1d7c` edited `aleppo/line-breaks/004r.json` to match the hole.** `py/py_ac_loc/mam_xml_verses.py:101–114`
   handles `<scrdfftar>` by taking `<sdt-target>`'s `text` attribute and, when that is absent, only its
   `<slh-word>` child's `slhw-desc-0`; a `<text>` sibling is ignored. Exactly one `<sdt-target>` in the
   24 files of `MAM-simple/xml-vtrad-mam/` has that shape, `Deut.xml:1672–1677` (Deut 32:6), whose
   children are `<slh-word slhw-desc-0="הַ">` and `<text text=" לְיְהֹוָה֙">`, so `get_verse_words`
   returns the atom הַ and drops לְיְהֹוָה֙ (stream A's census, `A_08_readonly_oracles.py`). `5fad1d7c`
   (2026-09-06 12:08, "Fix Aleppo line-break sequence runs") then inserted `"הַ"` at index 140 of
   `004r.json`, before `תִּגְמְלוּ־`, and nothing for the following word, which the tracked scan
   `aleppo/aleppo-pages/004r.jpg` shows on that line (column 1 line 15, crop
   `A_13_004r_lines13-16.png`, read by the main session as well: the line opens with the large he
   and then the word ליהוה before תגמלו־זאת). The word-sequence check passes only because the oracle
   and the data now have the same hole; Cambridge 1753 is unaffected (its reader is the same module,
   but its books are Ketuvim). Re-establish: `A_08_readonly_oracles.py` (the reader probe and the
   `sdt-target` shape census), `A_09_linebreak_data.py`, `A_13_crop_004r.py`; or
   `git -C C:/Users/BenDe/GitRepos/MAM-basics show 5fad1d7c -- aleppo/line-breaks/004r.json`.

2. **Data defect, unfixed: `5fad1d7c` removed יִשְׂרָאֵ֜ל (Deut 33:29) from `aleppo/line-breaks/006r.json`,
   the page whose first line has it, and kept the copy in `005v.json` after that page's last
   line-end.** The word was duplicated across the 005v/006r boundary. The commit deleted it at index 3
   of `006r.json`, the first word after `line-start 1of3/1`, and left index 594 of `005v.json`, after
   `line-end 3of3/28` — the copy the checker itself flags as "1 word(s) after last line-end", an issue
   the tracked `aleppo/check_line_breaks.html` still lists after the commit. The scans say the
   opposite: 005v column 3 line 28 ends with the atom אשריך and nothing follows it
   (`A_11_005v_col3_bottom.png`), and 006r column 1 line 1 begins ישראל מי כמוך
   (`A_11_006r_col1_top.png`); both crops were read by the main session too. So both pages' line data
   now misplace the word, and the commit's subject calls a data edit a fix. Re-establish:
   `A_09_linebreak_data.py`, `A_11_crops.py`.

3. **Published-page defect, unfixed: the post-stress-meteg census double counts MAM's 368 `מ:קמץ`
   words, so the page's "words", MBS and silluq figures are Phonetic MAM entry counts, not MAM word
   counts.** Phonetic MAM holds two entries for each word MAM writes with a `מ:קמץ` template (the
   qamats-gadol and qamats-qatan readings), and `py/accgram/post_stress_meteg.py:677–706`
   (`_chanted_words`, `_chanted_word_events`) flatten every `cb` structure — the docstring names "a
   qamats note" among them — so `_one_verse` classifies both readings. Re-deriving the whole census
   from phonetic-hbo's public pages, which render each such word once (`C_phon_oracle.py`,
   `C_variant_rows.py`): prose entries 233,586 on the page against 233,277 words (+309), poetic 29,605
   against 29,542 (+63); prose MBS 13,091 against 12,962 (+129), poetic 1,814 against 1,805 (+9);
   prose silluq 18,771 against 18,738 (+33), poetic 4,486 against 4,465 (+21); MAS 178 and 54 with no
   excess, no variant word having a MAS. The second readings supply exactly 162 = 129 + 33 prose and
   30 = 9 + 21 poetic extra U+05BD and 307 + 63 = 370 extra entries (two prose entries of the 309 are
   not variant words and were not chased). Counted once, the prose "% MAS" cell reads 1.4%
   (178 / (12,962 + 178)), not the page's 1.3%; the poetic 2.9% and overall 1.5% stand at one decimal.
   The page says "MAM has …" throughout. The same duplication is what the JSON's `currency` section
   reports as staleness: of its 186 "differing" numbered verses, 177 differ by exactly one U+05BD and
   each holds one variant word, and only 9, all poetic, are genuine text differences (a doubled deḥi in
   the snapshot against deḥi plus U+05BD in MAM-simple: jb29:16, pr13:25, ps44:27, ps57:9, ps69:29,
   ps86:7, ps108:3, ps138:3, ps139:7; `C_currency_probe.py`). The pre-refresh "221 of 23,184" the plans
   quote was this artifact plus about 29 verses of genuine pre-rollout staleness.

4. **Code defect, unfixed: `py/main_letter_small_job.py:7` names `MAM-simple/json-vtrad-bhs/Job.xml`,
   which does not exist, and the mega step truncates a tracked file before it dies.** `cf7c7a35`
   replaced `paths.sibling_repo("MAM-simple") / "xml-vtrad-mam" / "Job.xml"` with
   `paths.mam_simple_dir() / "Job.xml"`, and `mam_simple_dir()` (`py/mb_cmn/paths.py:234–236`) is the
   `json-vtrad-bhs` tree, which holds `Job.json`; the XML wanted is `MAM-simple/xml-vtrad-mam/Job.xml`.
   The mega step `letter-small-job` (`py/main_0_mega.py:219–223`) therefore raises `FileNotFoundError`
   from `ET.parse` — after `py/mb_misc/letter_small_job.py:9–11` has opened its cwd-relative output
   `py-examples-out/letter-small-job.txt` for writing, so a run from the repo root empties the tracked
   root-level file (last written `b24dc771`, 2026-05-07) and then stops. No test reaches this entry
   point; the vendored `MAM-simple/py-examples/main_letter_small_job_example.py:14` reads
   `xml-vtrad-mam/Job.xml` relative to its cwd and is unaffected. Verified by the main session.

5. **Stale generated artifacts, unfixed: `3c8c9750` repointed the generators that emit the MAM-with-doc
   URL, but only the MAM-with-doc lane's outputs were regenerated, so 385 tracked artifacts still carry
   the retired host.** `git grep -I -n -E 'bdenckla\.github\.io/MAM-with-doc/'` returns 716 lines in
   430 files; outside `doc/` (records), `in/mam-ws-intro/` (byte-verbatim) and `in/mam-from-sefaria/`
   (downloaded), 669 lines in 385 files, each written by a module whose URL constant the commit changed
   (`B1_oldurls.py`, `B2_old_mwd_urls.py`):
   1. `MAM-for-Sefaria/csv/*.csv` (39) and `MAM-simple/py-examples-out/sefaria/csv/*.csv` (39), line 5
      "Version Notes" — `py/mb_sefaria/sef_header.py:48` now says `…/MAM-basics/MAM-with-doc/`, the
      CSVs were last written at `4195440e` (13:29), before the change (17:41); the vendored copy of
      `sef_header.py` was re-vendored after the anchor (finding 6) but its outputs were not rerun.
   2. `gh-pages/book-of-job/jobn-details/*.html` (161, 168 hits) and `book-of-job/out/enriched-quirkrecs.json`
      (4 hits) — `py/author_boj_util/job_ov_and_de.py:295` and the `py/author_boj_qr/qr_*.py` files.
   3. `gh-pages/holman/uxlc_corrections.html` (125 hits) — `py/py_render/rt_external_links.py:73`.
   4. `gh-pages/uxlc/amb-early-mtg/**` (77 files) — `py/uxlc_amb_early_mtg/amb_early_mtg_url_generator.py:50`.
   5. `gh-pages/wlc/**` (62 files, 196 hits: the `420422/` records from `py/py_wlc/my_url_generator.py:50`,
      and `accgram/goerwitz.html` 97, `poetic.html` 15, `almost-errors.html` 11,
      `maqaf-nonfinal-accents.html` 10, `telg-doc-notes.html` 6, `ps17v14-mam-doc-notes.html` 1,
      `printed-decalogue.html` 1 from the seven `py/accgram/*.py` modules the commit changed).
   6. `gh-pages/MAM-parsed/{plain,plus}/html/mpplain.html`, `mpplain_kq_special.html`, `mpplus.html`,
      `mpplus_kq_special.html` (20 hits) — `py/author_misc/mp_body_shared.py:162`, `mp_cmn_kq_special.py:9`.
   The old URLs still resolve through the redirect host, so no reader meets a 404; the cost is that the
   generated artifact is no longer the test of its generator, and the next `py/main_0_mega.py` run
   rewrites about 385 tracked files as an unexplained diff. `3c8c9750`'s "repoint all writers and
   readers, regenerate the product" and the plan's oracle sentence "Links controlled by Ben are
   repointed" (`doc/PLAN-evacuate-five-MAM-products.md:114`) describe the MAM-with-doc product only.

6. **Vendored copies drifted from their sources while the inventory called them identical — fixed
   after the anchor by `7b11fd6b` and `11fb9c24` (11:50–11:53), not reviewed here.** At `8bf586a3`, 5 of
   the 44 `MAM-simple/py-examples/` copies differed from `py/` at blob level (`mb_cmn/paths.py`,
   `mb_misc/write_utils.py`, `mb_sefaria/sef_header.py`, `mb_cmn/template_names.py`,
   `osis/osis_runner.py` — the last lacking `726daafd`'s schema guard), while `doc/vendoring-inventory.md:20–23`
   and `out/vendoring_compare_out.txt` said `identical` and `last_synced` `no-commits` for all 44,
   having been generated inside `cf7c7a35` before the copies were tracked (`B1_vendored_drift.py`,
   `B2_vendored_blobs.py`). Phases 2, 3 and 4 each changed a vendored source without rerunning
   `copy-support-files`. What the two later commits do not touch: `py/py_misc/mam_simple_copy_py_files.py:36`
   still copies with `shutil.copy`, where `2a50fd15` gave the MAM-parsed twin an LF-forcing write
   because a CRLF checkout can leave a blob-identical copy persistently modified (26 of the 44 sources
   are `w/crlf` in this checkout); and the Phase 1 record's "43 vendored source files" is 44 at HEAD,
   `cf7c7a35` having added `MAM-simple/py-examples/mb_cmn/paths.py`, which the record does not name.

7. **Record and code-doc error, unfixed: the redirect program's default row moved from wlc-utils to
   MAM-simple without a record, and three docstrings and CLAUDE.md still describe the wlc-utils
   default.** `py/redirect_stubs/stubs.py:203` is `_DEFAULT_REPO = REDIRECT_REPOS[0]`; `REDIRECT_REPOS[0]`
   was wlc-utils at `b4706759`, MAM-simple from `cf7c7a35`, MAM-parsed at `2a50fd15`, and MAM-simple
   again from `affddc03`, whose subject "Preserve the redirect command's previous default" preserved
   Phase 1's unrecorded change. `build.py:27` and `check.py:35` take that row as the `--repo` default,
   so a bare `check` now resolves a MAM-simple clone, which no machine has (recycled 2026-09-06), and
   names `https://github.com/bdenckla/MAM-simple.git` when it is absent. Stale against that:
   `stubs.py:43` ("`redirected_pages` reads `in/wlc_redirect_pages.json`"), `:113–117` ("The table
   starts with wlc-utils"), `:202` and `:270–272`; `py/main_redirect_stubs.py:40–42`'s bare examples;
   and `CLAUDE.md:500–509`, which says `build --publish` and `check` with no `--dir` reach the
   wlc-utils clone and gives the wlc-utils clone command as the fix. Which row should be the default
   is Ben's decision; the prose is wrong under either answer.

8. **Lint coverage lost, unfixed, in four places:**
   1. `py/tests/test_h_dot_below_nfc.py:195` excludes `MAM-simple/` whole (comment `:180`: "generated
      product data"), which also drops `MAM-simple/README.md`, its four `doc/*.md` and its Python — the
      Ben-written prose the old MAM-simple repository's copy of this lint scanned. That copy is now
      `MAM-simple/py/tests/test_h_dot_below_nfc.py`, discovered only by `MAM-simple/py/main_test.py`
      and by nothing the canonical suite runs (981 items, all under `py/tests/`), and its `REPO_ROOT`
      is `git rev-parse --show-toplevel`, so its scope is 3,565 files, 3,179 of them outside
      `MAM-simple/`; `MAM-with-doc/py/tests/test_h_dot_below_nfc.py` is rooted the same way (3,560
      outside). The MAM-for-Sefaria and MAM-parsed copies are scoped to their products (5 and 7 files)
      and run by nothing either, though `DATA-LICENSES.md:74` calls the MAM-for-Sefaria one a
      "source-hygiene test". `MAM-for-Sefaria/` is meanwhile scanned whole, 160 generated files and
      about 1.2 million lines per run. This is the unregistered-file failure CLAUDE.md's test section
      names (`B2_product_nfc_scopes.py`).
   2. `py/tests/test_mam_simple_mark_order.py` no longer reads the page it was written for: its
      docstring (`:16–18`) names `gh-pages/versification-and-cantillation.html`, one of the two places
      found in the wrong mark order on 2026-08-09, and its scope is now `git ls-files -- MAM-simple`,
      which excludes `gh-pages/MAM-simple/versification-and-cantillation.html`; `test_h_dot_below_nfc.py`
      excludes `gh-pages/` too, so the Hebrew in `py/versification_and_cantillation/doc.py` is checked
      for MAM mark order by nothing.
   3. `py/check_html_syntax_and_sanity.py` now refuses the multi-site `gh-pages/` root (`:73–79`, exit
      2), and the nine deploy-root pages (the seven post-stress-meteg pages, `index.html`,
      `unicode-proposals.html`) belong to no sub-site, so nothing lints them; a scratch mirror of the
      root reports 0 issues for the seven (`C_run_checker.py`). Its "unknown CSS class" category is
      noise rather than a scoping false positive: the uxlc 3,602 and MAM-with-doc 14,116 hits are
      classes (`clc-text` 3,250, `mam-doc-part-0` 4,004, `mam-spi-samekh` 1,988 …) defined in none of
      the 16 stylesheets under `gh-pages/` (`C_checker_classes.py`).
   4. `py/tests/test_no_machine_paths_in_artifacts.py` does not scan the program-written parts of
      `aleppo/`, `cam1753/`, `MAM-simple/`, `MAM-parsed/` or `MAM-for-Sefaria/`; a grep found no machine
      path in them apart from the two product READMEs of finding 14.6 and the stale vendored docstring
      finding 6 covers.

9. **The fourth stage's records, unfixed, with one decision for Ben:**
   1. **Ben's decision: the MAM-for-Sefaria clone.** Phase 2's execution record
      (`doc/PLAN-evacuate-five-MAM-products.md:151–181`, headed DONE) records no Remove step, though
      the common lane's line 89 says "a lane does not silently skip a common step"; the only record is
      the programme row (`doc/PLAN-evacuate-public-repos-programme.md:42`, "its clone remains pending
      its separate safety report"), and `4f68b18d`'s message claims the retention decision is "in the
      fourth-stage plan and programme". The clone at `C:/Users/BenDe/GitRepos/MAM-for-Sefaria` would
      pass the plan's step-6 criteria today: clean, `HEAD` = `origin/main` = `cf23b478`, one worktree,
      no stash, only `main`, its three tags on the remote, and one unreachable commit (`34c94a8`, the
      pre-rebase copy of `746d6d2` from 2026-03-09, two README lines) (`B1_report.md` (b)3). It is in no
      workspace file, so `gitrepos_setup_rule`'s clause 5 already calls it residue.
   2. `doc/PLAN-evacuate-public-repos-programme.md:632–634` says "The remaining four product lanes
      have not started" under the heading "Phases 1–4 done 2026-09-06" (`:622`) and beside rows 42–44;
      lines 712–714 ("the defect in `py/mb_misc/write_utils.py` stands"), 831–833 (no sparse checkout
      "exists today"), 914–916 (`in/vendoring_policy.json` "loses MAM-simple, leaving
      diffable-pointed-hebrew and MAM-private"; at HEAD `repos` is MAM-basics and MAM-private) and
      926–927 (the pipeline label "raised here, not fixed"; fixed) are overtaken the same way.
   3. `doc/PLAN-evacuate-five-MAM-products.md:529` and the programme's row 43 attribute the removal of
      MAM-with-doc from the workspace files and the visibility map to `3c8c9750`, which touches neither;
      the removal is `19df42f3`.
   4. The plan's scope table (`:17–18`) still names the recycled MAM-parsed and MAM-with-doc clones
      without the annotation line 15 gives MAM-simple; line 63's "totaling 23,497,110 bytes" and
      "total 23,498,632 bytes" are the outputs' totals labelled as including the example programs
      (measured 23,675,571 for the 47 + 105 MAM-simple files and 23,500,226 for the four programs plus
      106 outputs); line 132's "all 389 selected source blobs landed … with no difference" leaves the
      seven post-staging differences and the added `mb_cmn/paths.py` unnamed, where Phases 2–4 name
      theirs; line 533 lists the MAM-with-doc host's retained files without its two dotfiles.
   5. The Phase 4 record (`:527–531`, programme row 43) does not say that 13 landed published pages
      differ from source, nor why: ten by the URL repoint, and `change-log/unpinned-latest.json` from
      24 to 56 records because the source's report had not been regenerated since `b3837db0`
      (2026-09-02) — the last review's finding 2 — so oracle layer 2 ("preserves the committed product
      artifact") was not met there and the record does not say so.
   6. MAM-simple's redirect-host README on GitHub has no date, where the Empty step (`:95`)
      requires "a dated breadcrumb README" and the other three hosts' READMEs say "On 2026-09-06".
   7. `MAM-simple/README.md:3, 67` and `MAM-for-Sefaria/README.md:13` link MAM-parsed to
      `https://github.com/bdenckla/MAM-parsed`, the redirect host, where the plan's line 104 asks for a
      relative link to the landed product, as `MAM-parsed/README.md:50–51` does; `MAM-parsed/README.md:68–95`
      and `MAM-parsed/historical/README.md:20, 33, 37` put `C:/Users/BenDe/…` paths into reader-facing
      commands of a public product README, where `MAM-simple/README.md:34–37` gives the same recipe
      machine-neutrally.

10. **The third-stage records and the maintenance runbook, unfixed:**
    1. `doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md:365–366` says "43 rows
       across seven destination repositories"; `doc/vendoring-inventory.md` at `95525845` ends "7 rows,
       43 files", all seven rows targeting MAM-simple; the Phase 5 record (`:444`) has it right.
    2. `doc/PLAN-evacuate-public-repos-programme.md:336` still heads the third stage "Phases 0–2 DONE
       2026-09-04" and `:345` says "a later task runs Phase 2 only", against the Status row's "all five
       phases".
    3. The trio plan's Phase 1 Status row (`:56`) still says the Leningrad primary clone "remains only
       as shared Git metadata"; row 60 and the Phase 5 record say it went to the Recycle Bin (also the
       last review's finding 4, whose "Fixed" is therefore partial).
    4. Two prescriptions spell the Aleppo manifest `in/codex-index-aleppo_redirect_pages.json` (trio
       plan `:213`, programme `:508`); the tracked file, `stubs.py:197` and the Phase 2 record spell it
       `in/codex_index_aleppo_redirect_pages.json`.
    5. `doc/PLAN-repo-maintenance-across-GitRepos.md:33–34` says the workspace lists 19 folders and
       `GitRepos` holds 19 clones; `:131–139` present book-of-job, UXLC-utils, holman-ketiv-qere and the
       three codex-index repos as clones whose data is resolved "as `DATA_REPO_NAME` in `py/ac_paths.py`,
       `py/boj_paths.py`, `py/cam1753_paths.py`, `py/hkq_paths.py` and `py/lenin_paths.py`", and
       `:140–144` say archiving the three codex-index trackers "would freeze corpora still in use": none
       of the six has a clone, `DATA_REPO_NAME` occurs in no file under `py/` (`CLAUDE.md:292` makes the
       same claim), and two of the three are archived. The two 2026-09-04 additions (`2a9c3cbd`,
       `18b4eb7a`) did not touch that scope text, and their step 7 lists the Claude-cache paragraph as
       the fourth "case" of a dated task folder, which it is not (it concerns directories outside
       `Documents/Codex`); against the global instruction the runbook also omits "preserve a forest
       naming a future handoff", the absent-manifest rule and `git count-objects -vH`.
    6. `aleppo/doc/aleppo-line-breaks.md:10–14, 18, 24, 31, 38–41, 136, 198–199` still call
       codex-index-aleppo "this repo" ("none of them can be run from this repo any more", "this repo
       tracks no Python at all") after `5fad1d7c` and `4ab308eb` edited the file;
       `cam1753/doc/reading-mam-simple.md:25–31` has the same shape after two repoints.
    7. Smaller: `py/ac_paths.py:106` "(37 tracked JPEG), leaves 270-281 recto and verso" — 24 of the
       37 are those leaves, the other 13 are 001r–006r and 148r/148v; `py/repo_scopes.py:30–37` and
       `py/check_mark_order.py:85–88` cite "24 line-break files" under `book-of-job/`, which holds 7
       JSON, none a line-break file (the corpus count today is 162: aleppo 83, cam1753 72, book-of-job
       7); `doc/PLAN-evacuate-public-repos-programme.md:539–540` requires "the same 150 JSON" and no
       execution record states the count.

11. **Record errors introduced or left by the 2026-09-04 review's remediation, unfixed (stream D):**
    1. `doc/PLAN-evacuate-the-rest-of-three-repos.md:1853`, the "Correction, 2026-09-07" paragraph
       `9eedccbd` added, says "The current suite no longer prints a subtest line". It does: this
       review's run printed `976 passed, 5 skipped, 65 subtests passed`, and the disposition table's
       row 9 says 65 subtests. The paragraph's other claim, that the figure comes from pytest natively
       and not from `pytest-subtests`, is right.
    2. `CLAUDE.md:446–448` now says the `doc/boj-*.md` paths were "repointed on arrival" to
       `book-of-job/out/…`, `gh-pages/book-of-job/…` and `.novc/book-of-job/…`; the 2026-08-21 arrival
       used `../book-of-job/…`, as the last review's finding 5 and the pre-`9eedccbd` sentence record,
       and those spellings date from 2026-09-07.
    3. `py/repo_util/check_repo_standards.py:269` still says "all thirteen of this repo's
       doc/PLAN-*.md" (`git ls-files doc/PLAN-*.md` lists 10; the last review's finding 11.4 named it,
       and row 11 does not cover it); `:278–281` call the three-repos plan "paused" and "cited by
       nothing outside doc/" (it is `executed 2026-09-03` and cited from `py/uxlc_paths.py`) and say the
       codex-index-trio plan "is cited from 31 modules" (27 files under `py/`, and the plan was deleted
       2026-08-29).
    4. Disposition row 18 rejects "changing the deliberate primary-clone constant"; `_PRIMARY_CLONE`
       was removed by `4195440e` on 2026-09-06, so finding 18.5 is moot, not rejected. The row's "Six
       merged local MAM-basics branches" cannot be re-derived: the finding named four, and the HEAD
       reflog shows two further merged names (`codex/plan-five-mam-products`,
       `codex/correct-fitformas-analysis`) the row does not list.
    5. Row 16 is partial: `doc/holman-meteg-m13-qamats-template.md:34` still has "the same meteg is
       carried again", and the 24 comment and docstring "own" lines the finding counted are unchanged
       (`py/hkq_cmn/mam_suggestion_extract.py:33, 88, 128, 417, 438, 440, 552`;
       `mam_suggestion_dispositions.py:20, 43, 47, 87`; `py/py_render/rt_mam_suggestion_card.py:14, 352`;
       `verify_mam_suggestions.py:111`; `py/main_ingest_mam_suggestions.py:24`;
       `py/accgram/post_stress_meteg.py:19, 497, 2075, 2106`; `py/author_site/post_stress_meteg.py:4, 15`;
       `:499` "a vowel of its own" is a real contrast). Outside the finding's named cells, 49
       Hebrew-holding `comparison-name-col` and `comparison-symval-col` cells on the Archived Holman page
       and 1 on the Active page have no `dir="rtl"`.
    6. Row 17's detail "`~/.Codex/plans/`, a directory that does not exist" is stale: it exists now,
       with one entry, not read. `~/.agents/skills/prune-claude-state/SKILL.md` still differs from the
       `~/.claude/skills/` copy in exactly the five rewritten lines and is tracked in github-misc's
       `dot-Codex/skills/prune-claude-state/` byte-identically (finding 22).
    7. `py/redirect_stubs/stubs.py:13` reads "See ``doc/PLAN-evacuate-the-rest-of-wlc-utils.md``,
       Phases 8 and 9." as if the file existed; the other eight docstring citations of the deleted plan
       read as dated history, and Ben's leave-as-written precedent covers all nine. `CLAUDE.md:351`
       counts "four [sentences] in `doc/PLAN-evacuate-the-rest-of-wlc-utils.md`" that left with the file.

12. **Post-stress-meteg docs stale against the JSON, unfixed (stream C):**
    1. Three docs say the Phonetic MAM oracle was never refreshed and the count is 231:
       `doc/post-stress-meteg-census-2026-09-03.md:21–34` ("231 post-stress metegs, 13,131 prose
       pre-stress … lists no difference at all … 221 of its 23,184 … 38,379 metegs against 38,170 …
       the question is closed"), `doc/PLAN-holman-meteg-rollout-programme.md:25–32, 183–184, 194–196, 213`
       and `doc/PLAN-post-stress-meteg-page-and-holman-m23.md:1091, 1148, 1158–1161, 1173–1176` ("The
       figures stay at 231. This is a closed question … the regeneration is not to be re-proposed").
       The oracle was refreshed on 2026-09-06 (phonetic-hbo `7322b665` at 00:02, MAM-basics `fee6367e`
       at 09:55): the JSON went 231 → 232 post-stress metegs, prose MBS 13,118 → 13,091, `currency`
       221 → 186 differing verses, and `legacy_baseline.differences` from three entries to four
       (`C_commit_figures.py`). `9eedccbd` edited the census doc's line 27 and the programme's lines
       183–184 a day after the figures moved, without updating them; the main page says 232.
    2. `doc/post-stress-meteg-method.md` describes a superseded Fit-for-MAS: lines 8–14 admit "one or
       more of the three source-derived types" where `_fit_type` (`py/accgram/post_stress_meteg.py:1308–1327`,
       `763b5578`) admits types 1A, 1B, 2 and 3 only and 1,564 candidates with 4 MAS fall out on that
       ground; lines 39–40 cite "the 3,181 Fit-for-MAS records" (496 at HEAD); lines 85–86 say the first
       chanted word's accent condition comes from the accent grammar, where `c7f384a8` replaced it with
       a raw stress-letter codepoint test (`:1004–1007`); line 81 says tokenization excludes no
       candidate, where since `c0f713c2` the next word's tokens are a filter (`:1299–1305`). The doc was
       last edited by `4845da43` at 08:05, before `763b5578` at 08:51.
    3. `py/accgram/post_stress_meteg.py:50–63` says `numbered_verses_whose_last_entry_lacks_sof_pasuq`
       "records all twelve" Decalogue verses; the JSON's list is `[]`, empty by construction since
       `78813a64` projects each dual verse onto one strand before `_one_verse` runs.
    4. Stale counts: `py/tests/test_site_index_links.py:84` "this page carries 31" (34 anchors);
       `py/author_site/site_data.py:93` "all seven pages at the deploy root" (nine) and `:102–103` "the
       four deploy-root pages that show pointed Hebrew" (all seven post-stress pages link
       `wlc/style.css`); `py/main_authored.py:9–12` names three `gen-site` pages (it writes nine).
    5. `8de50290` removed the page's M23 section and its `m23-isaiah-23-12` id, and
       `py/py_render/rt_suggestion_context.py` now links the page with no fragment, while
       `doc/PLAN-post-stress-meteg-page-and-holman-m23.md:70, 466, 1281–1300` and
       `doc/holman-meteg-m23-isaiah-23-12.md:259` still describe the fragment as live.

13. **Definitions and claims on the post-stress-meteg page that the code or the sources do not
    support, unfixed:**
    1. The page says type 3 is "a closed, final, tsere-vowelled syllable" (generator line 1201, the
       `abbr` titles at 181–184 and 1395); `_structural_type` (`py/accgram/post_stress_meteg.py:656–657`)
       and `_fit_for_mas_candidate` (`:1255–1256`) test closure and tsere with no finality test, and only
       the near-miss subtype `misc-almost-type-3` requires finality (`:658–659`). No nonfinal case
       exists today and `pin_claims` asserts finality for the type-3 records, so drift would fail the
       build; the definitions still disagree.
    2. `d325a21b`'s body says the rename covered every module-level name; `TYPE_2_FOLLOWING_FILTER_GROUPS`
       and `_TYPE_2_FOLLOWING_FILTER_GROUP_BY_INITIAL` survive at `py/accgram/post_stress_meteg.py:155–156,
       468, 472, 486`.
    3. Footnote φ1's "BHS" row is UXLC 3.9's form: `_post_silluq_comparison`
       (`py/author_site/post_stress_meteg.py:1921–1947`) reads 1 Samuel 17:5's verse-final נחשת from
       `in/UXLC-39` and `out/wlc422`, asserts the two agree, and labels the row "BHS"; no BHS text is
       read anywhere in the repo. The page then says "This surprising meteg is correctly recorded in
       BHS and in BHS-derived editions such as UXLC and WLC" (`:2012–2016`) — a claim about BHS on a
       transcription's authority, and two transcriptions called editions, which the global rule "A
       transcription is evidence about the transcription" and the plan's section 5 both forbid;
       `9727e35b`'s wording had the sanctioned form ("Their forms are evidence about UXLC and WLC") and
       `8de50290` replaced it. The manuscript sentence itself rests on the crop the page shows, which is
       the sanctioned form.

14. **Licence gaps and errors in `DATA-LICENSES.md`, unfixed:**
    1. No row covers `gh-pages/img/`, whose one file `LC-159A-col-3-line-8-1S-17v5.png` (`7de2f136`,
       70,782 bytes) is a Leningrad Codex crop; every other directory of manuscript crops has a "no
       grant is made or implied" row, and the page's caption names the folio and "crop attached to
       phonetic-hbo #78" but no rights holder or photograph source.
    2. No row covers the seven `gh-pages/post-stress-meteg*.html` pages, which display MAM's text in
       1,205 Hebrew runs; the deploy-root rows (lines 66–67) cover `index.html` and
       `unicode-proposals.html`, both "holds no corpus text". The `out/accgram/` row (line 65) says the
       Hebrew each file quotes "comes from the WLC and the UXLC"; `out/accgram/post-stress-meteg.json`
       quotes Phonetic MAM and MAM-simple (3,958 Hebrew strings).
    3. Line 79 describes `MAM-with-doc/` as "MAM's HTML edition, its documentation-note source
       materials, product README, and license"; the directory holds five files, 14,272 bytes
       (`.gitattributes`, `.gitignore`, `LICENSE.md`, `README.md`, `py/tests/test_h_dot_below_nfc.py`);
       the edition is `gh-pages/MAM-with-doc/`, row 80.
    4. Lines 122–123 say the MAM statement "stands as `LICENSE.md` in the MAM-parsed, MAM-simple,
       MAM-with-doc, MAM-OSIS and MAM-for-Sefaria repositories"; the four evacuated repositories' HEAD
       trees track no `LICENSE.md` (MAM-OSIS still does), and the file stands here as the four landed
       `MAM-*/LICENSE.md`, one blob `51094acf`.
    5. Rows 80 and 82 except only `woff2/Taamey_D.woff2` and `foi/woff2/Taamey_D.woff2` from the
       CC-BY-SA row, but `gh-pages/MAM-with-doc/change-log/woff2/Taamey_D.woff2` and
       `gh-pages/MAM-with-doc/misc/woff2/Taamey_D.woff2` are tracked too (`3c8c9750`), so two copies of
       a third-party font read as inherited CC-BY-SA; `gh-pages/book-of-job/jobn/woff2/Taamey_D.woff2`
       is named by neither row 92 nor 94, pre-existing.
    6. Vocabulary: line 83 "three hand-authored pages" (`a0a2a379`, 1h49m after `b4706759` adopted
       script-regenerable / Ben-written / Claude-written) and lines 86, 88, 90 "hand-annotated",
       "hand-made"; `aleppo/README.md:16` the same. Ben's instruction was to avoid the vague terms
       where context does not make them clear, so low.

15. **A second roster survives under `misc/linux-sh/`, and one lane of four maintained it.**
    `misc/linux-sh/repos.txt` and `repos-minus-MAM-basics.txt` list twelve names — AHT-issues,
    CCAR-Psalms, codex-index, github-misc, hbofonts, MAM-for-Acc, MAM-for-JPS, MAM-OSIS, MAM-parsed,
    MAM-with-doc, MAM-simple, MAM-basics — and `linux-clone.sh`, `linux-pull.sh` and `linux-status.sh`
    iterate them, so the two files are a clone roster for Linux naming three frozen repos, three
    products retired this window and two names in no roster. Untouched since `c55e7620` (2026-04-28)
    until `4f68b18d` removed MAM-for-Sefaria; `cf7c7a35`, `9a61e7b5` and `19df42f3` left MAM-simple,
    MAM-parsed and MAM-with-doc in place. `gitrepos_setup_rule`'s clause 1 says the roster is
    `all-repos.code-workspace` "and nothing else" and clause 4 forbids a second list; `README.md:131`
    names the directory as root-level `linux-sh/`. Ben's decision whether the scripts stay.

16. **Data inherited in the wrong mark order, unfixed and covered by no lint:**
    `gh-pages/aleppo/missing_sections_nakh.html` has 48 of its 427 Hebrew runs, and
    `missing_sections_torah.html` 2 of 54, in Unicode-normal rather than MAM-normal order
    (`has_std_mark_order` false; `A_07_mark_order_pages.py`, `mark_order_window_scan.py`). Both pages
    are byte-identical to codex-index-aleppo's, so the order is inherited, not introduced; the pages
    are Ben-written per `DATA-LICENSES.md:83`, which is CLAUDE.md's mechanism for Unicode-normal order. No
    lint covers `gh-pages/aleppo/`: `check_mark_order` reads `.py` and `.json` only, and no file under
    `py/tests` or `py/check_*` names the directory.

17. **Code tolerances and fragilities, unfixed, all latent today:**
    1. `no_marks_comparison_key` (`py/py_cam1753_word_image/hebrew_metrics.py:7–26`, used by
       `py/py_ac_loc/check_line_breaks.py:159–191` and `py/py_cam1753_loc/check_line_breaks.py:422–461`
       since `4ab308eb` and `22491536`) strips every `Mn` and `Cf` character — vowels, dagesh, shin and
       sin dots, accents, meteg, rafe — where the ten Cambridge differences and the Aleppo mismatches
       it was written for were meteg and rafe only; a vowel or accent error in a line-break JSON word
       is now caught by no check. No `unicodedata.normalize` is involved.
    2. In `py/accgram/post_stress_meteg.py`: `_type_1_subtype` calls `_parse` on the next chanted word
       (`:582`), so a syllable mismatch there raises `SurveyProblem` out of `_one_verse` and aborts the
       run, where the same mismatch in the current word is recorded in `found["mismatches"]`
       (`:1792–1798`) as the module docstring promises; `_intervening_punctuation` (`:755–770`) raises
       on any material other than Phonetic MAM's paseq token, so a MAS record whose next chanted word
       follows a setuma, petuxa or qamats marker would abort the build, while the Fit-for-MAS path
       tolerates those markers (`:774–792`); `candidates_meeting_multiple_types` (`:1612–1614`) can only
       be 0 because `_fit_type` asserts at most one type first, so `pin_claims`' assertion of 0 checks
       nothing; `_case_type_cell(..., unqualified_word=True)` replaces "chanted word" with "word" in a
       gloss that already says "word"; `_TYPE_SOURCES`' third element (the obligatory/optional gradings,
       `:161–169`) reaches no page; `_wlc_words` (`:1904–1918`) loads every `out/wlc422/1verses_*.json`
       to find one verse.
    3. `py/subcommands/diff_mpp.py:225–227` computes `default_output_path` from the un-prefixed
       revisions, so a `--legacy-history` comparison whose hash range matches a `releases.json` entry
       overwrites that release's tracked report (stream B2; observation, not a defect today).
    4. The φ7 "Lacks MAS" cells for types 1A (112) and 1B (31) both link
       `post-stress-meteg-type-1-lacks-mas.html`, which shows a seeded sample of 100 prose and 10
       poetic pairs drawn from 1A and 1B together (143 pairs) without stating the total or the sample's
       relation to it, where the type-2 link opens all 150.

18. **Stale docstrings and comments after the repoint, unfixed:** `py/mb_cmn/paths.py:9–11` names
    MAM-with-doc among the cross-repo dependencies (landed by `3c8c9750`) and omits MAM-for-Sefaria
    among the landed products; `:175`'s `display_path` example spells a form the function no longer
    yields. `py/main_0_mega.py:3–9` says "Several other generators still write to sibling repositories"
    (two remain: MAM-OSIS and the MAM-private census) and `:412` says the vendoring audit "scans every
    sibling repo on disk" (it scans none). `py/tests/test_sibling_reach.py:36–38` quotes a help string
    `8e5735fb` removed, `:77–79` says the mega builds subprocess cwds "for MAM-parsed and MAM-private"
    (MAM-private only), `:98–100` quotes a `paths.mam_parsed_path` docstring that survives only in the
    stale vendored copy, `:208–211` says `paths.py` calls `sibling_repo("MAM-parsed")` (it calls it once,
    with MAM-private), `:25–27` cites 22 docstrings reading `../MAM-parsed/gh-pages/…` that `8e5735fb`
    rewrote, and `SIBLINGS_REACHED["MAM-parsed"]` does not name `stubs.py:288, 290`, which the scan
    attributes to it (line numbers before `6b5e4a40`'s edit). `py/py_misc/mam_simple_copy_py_files.py:94–111`
    and its output `MAM-simple/py-examples/provenance.md:4–16` say "in the MAM-basics sibling repo" and
    "maintained directly in this repo (MAM-simple)", as do `py/vendoring/gen_inventory.py:22–37`'s three
    MAM-simple rows and so `doc/vendoring-inventory.md:33–35`; `py/main_mam_simple.py:200` "Copy support
    files to the MAM-simple repo."; `py/main_scan_pages.py:9–10` "from a worktree, set REPOS_ROOT";
    `py/tests/test_vendoring_policy_paths.py:12–13` "nine sibling repos"; `py/main_vendoring.py:24`
    "~174 vendored copies" (44). `MAM-simple/py/main_test.py:29–34` says "this repo's venv holds black
    and nothing else, and there is no requirements.txt" beside `MAM-simple/requirements.txt`.
    CLAUDE.md: `:675` lists MAM-with-doc among the sibling-repo paths built from `sibling_repo`;
    `:679–680` omits MAM-with-doc from the products that need no `REPOS_ROOT`; `:683–687`'s
    vendored-files exception says the copies go "into sibling repos" and keep "cwd-relative or
    self-contained `__file__`-relative logic … without also requiring `mb_cmn/paths.py`", where the
    copies now go to `MAM-simple/py-examples/`, `write_utils.py:12` and `mam4sef_or_ajf.py:10` import
    `mb_cmn.paths` since `cf7c7a35`, and `paths.py` is itself vendored (`mam_simple_copy_py_files.py:53`);
    `:292` cites `DATA_REPO_NAME`, which no `py/` file holds. `doc/dual-agent-review.md:247, 273` say
    `~/.codex/AGENTS.md` "is 998 lines" (1,047 lines, 83,044 bytes; line 250 dates the first mention),
    and its §"2. Keep the Codex reviewer read-only" ("A review agent has no reason to write") is
    contradicted by its Design A procedure and by the record: the Codex session wrote
    `.novc/codex_review_scan.py`, promoted its report and appended the reconciliation (`820232ef`,
    `2988abf2`).

19. **README.md, pre-existing and window-introduced, unfixed:** lines 109–114 ("Optional: list or run
    selected test groups", `--list`, `--ws-urls-encoding`) are false — `py/main_test.py --list` exits 4
    with `unrecognized arguments`, and neither string has ever been in the file (`fd2241a5`,
    2026-05-03); line 131's `linux-sh/` is `misc/linux-sh/` (moved `c55e7620`); lines 31 and 68 name
    `main_osis_split_mapm.py` and `main_rename_jpeg_scans.py`, both deleted 2026-03-10; lines 134–138
    call `mb_diff_mpu` and `mb_author` vendored packages, which the vendoring policy audits nowhere;
    line 142 "Two declarations" and `DATA-LICENSES.md:23` "Three things" are followed by unnumbered
    prose; lines 144–146 omit the `doc/woff2/` exception `DATA-LICENSES.md:5–9` makes, and
    `DATA-LICENSES.md:91` lists `py/main_diffable_pointed_hebrew.py` in an MIT row while lines 5–6 say
    everything under `py/` is GPL-3.0.

20. **Reachability, Ben's decision: eleven tracked pages are linked from no page.** The link graph
    over all 576 tracked HTML pages (`D_orphans.py`; 0 dead internal targets) finds seven of the last
    review's eight still orphaned by the recorded decision — `book-of-job/index.html`,
    `uxlc/clc/2Samuel.html`, `uxlc/clc/Genesis.html`, `uxlc/clc/Proverbs.html`, the two
    `holman/JC3 … #19-ז` pages, `wlc/index.html` (`uxlc/index.html` is now linked) — and four new
    ones from the products landed after the anchor: `MAM-for-Sefaria/index.html`,
    `MAM-simple/versification-and-cantillation.html`, `MAM-with-doc/misc/index.html`,
    `MAM-with-doc/tsinnorit_oleh/tsinnorit_and_oleh_on_ivs.html`. The ten `wlc/accgram/img/*-unused*`
    images are unchanged.

21. **Prose rules, unfixed, in this window's files (against the hebrew-prose skill and the global
    rules), listed by rule:**
    1. Grammar and banned verbs on the post-stress-meteg pages: "Exactly what words are included and
       excluded in these three types vary between ITM, CoS, and our document here" (generator
       `:1237–1238`, "vary" for "varies"); "the meteg-bearing word" (misc page, `:1770`) and
       "stress-bearing accent" (`py/accgram/post_stress_meteg.py:2212`); footnote heading "A meteg after
       silluq in Leningrad" (`:1972`) where the body says "the Leningrad Codex"; the φ1 callout sits on
       "In every MAS case, the stress syllable has a conjunctive accent" (`:1110–1114`) with no sentence
       saying why a post-silluq meteg in the Leningrad Codex bears on that; "cant-alef" and "cant-bet"
       on the methods page undefined for a reader (the method doc defines them at line 47); section
       ranges with an ASCII hyphen ("§§46-47", `_TYPE_SOURCES` `:162–168`) where the plan uses an en
       dash; "ṣere" in `_VOWEL_NAMES` (`:240`) and `pin_claims` (`:761, 780`) against "tsere" on the
       pages and in the type constant; `itm()` / `cos()` rebuilt locally
       (`py/author_site/post_stress_meteg.py:892–921`) where `almost_errors_html_shared.itm()` /
       `cos()` exist (`36f34547`, deliberate); "the gaʿya-before-paseq pattern described in ITM §325"
       (`:1771–1777`), borderline as a source's phenomenon name.
    2. The "own" tic: the 24 lines of finding 11.5; six in the survey module after `9eedccbd`'s sweep
       of the same file (`py/accgram/post_stress_meteg.py:18, 19, 497, 499, 2075, 2106`); three new in
       this window's docs (`doc/PLAN-evacuate-public-repos-programme.md:916`,
       `doc/dual-agent-review.md:272`, `book-of-job/doc/reading-mam-simple.md:24`).
    3. Announced counts left unnumbered: disposition row 18's "Six merged local MAM-basics branches"
       (finding 11.4); `README.md:142`, `DATA-LICENSES.md:23` (finding 19).
    4. The two rendered-page wordings of the last review's finding 16.7 are gone; no "witness", no
       bare "Simanim", no "the former/latter", no "one … the other" was added anywhere in the window's
       `doc/`, `CLAUDE.md` or the seven pages (`D_prose_scan.py`, `C_prose_grep.py`).

22. **Instruction-file plumbing: identical everywhere it is tracked.** `~/.claude/CLAUDE.md` is
    byte-identical to github-misc's `dot-claude/CLAUDE.md` (95,777 bytes) and the two tracked skills
    (six files) to `dot-claude/skills/`; `~/.codex/AGENTS.md` (83,044 bytes, 1,047 lines) to
    `dot-Codex/AGENTS.md`; `~/.agents/skills/hebrew-prose/` (five files) to `~/.claude/skills/hebrew-prose/`;
    `~/.agents/skills/prune-claude-state/` and `worktree-forest/` to `dot-Codex/skills/`, where
    github-misc `d961120` now tracks the variant the last review's finding 17 found untracked. github-misc
    is private; only the copies' identity was compared (`plumbing_compare.py`).

23. **Process and hygiene, recorded for Ben's decisions:**
    1. Trailers: 121 of the 220 non-merge commits carry none and 96 are subject-only, both
       concentrated in the `post-stress-meteg` branch's 148 merged-in commits (94 with no trailer),
       while the 72 on `main`'s first-parent line carry one in 45 cases; the Codex trailer is spelled
       three ways (finding 19 of the last review rejected rewriting, so this is census only).
    2. The Codex worktree `C:/Users/BenDe/.codex/worktrees/MAM-basics-post-stress-meteg` is live and
       clean (at `11fb9c24` by 11:59), its branch fully merged; `C:/Users/BenDe/.codex/worktrees/d4d1/MAM-basics-post-stress-meteg`
       is an empty directory, not a repository (created 2026-09-05 23:35); `origin/post-stress-meteg`
       stands at `9239ac3a`, merged and 48 commits behind the local branch, a pushed worktree branch
       the global Git section says not to push as a backup. Deletion of the remote branch, and of the
       empty directory, is Ben's call.
    3. `C:/Users/BenDe/Documents/Codex/2026-09-04/referenced-chatgpt-conversation-this-is-an/work/`
       holds 20 disk-audit `.py` scripts and three JSON reports last written 2026-09-04 13:45 with an
       empty `outputs/`; `Documents/Codex/ReviewForests/` and `C:/Users/BenDe/Forests/` are empty. The
       runbook's step 7 says such a folder is classified and, if verifiably complete, moved to the
       Recycle Bin by a maintenance run, not by a review; no tracked doc names it.
    4. `MAM-basics/.pytest_cache` exists again (created 10:14:29, `nodeids` rewritten 11:24:52 today),
       self-ignored; the last review's disposition moved its predecessor to the Recycle Bin.
    5. phonetic-hbo `7322b665` (public) changed 36 chapters under `gh-pages/tnkh/` and the same 36 under
       `gh-pages/tnkh-ashkenaz/`, 42 distinct verses: 32 of the rollout's 33 (2 Samuel 18:20's rows
       were notes only) plus ten verses outside the roster — Numbers 11:24 (meteg removed), 16:18
       (meteg moved), Joshua 4:10, 19:9, 20:5, 24:29 and Judges 7:12 (meteg added), 2 Samuel 17:1
       (meteg moved), Psalms 14:1 and 2 Chronicles 34:12 (U+FB1E) — MAM edits beyond the programme,
       which the next `fr-wikisource` refresh will bring into `in/mam-ws` (`C_phon_verses.py`).
    6. The `post-stress-meteg` worktree was merged into `main` 37 times in the window, 21 of them one
       commit each on the evening of 2026-09-05, and main was merged back into the branch, so the
       branch tip's ancestry holds 217 of the 220 non-merge commits; the global Git section's "merge just
       before the session is archived" describes a different cadence. Census only.

24. **Immutable-message slips, the window's census, recorded only.** (a) `5fad1d7c` "Fix Aleppo
    line-break sequence runs" covers two data edits that were not fixes (findings 1 and 2). (b)
    `3c8c9750` "Move the product and its published Pages tree into MAM-basics" — the move is
    `5a28bc0e`; and "regenerate the product" is true of MAM-with-doc alone (finding 5). (c) `affddc03`
    "Preserve the redirect command's previous default" — Phase 1's, not the pre-window one (finding 7).
    (d) `4f68b18d` "record … source-clone retention decision in the fourth-stage plan and programme" —
    the programme only (finding 9.1). (e) `8e5735fb` "Product and example blobs match their source
    oracles apart from required documentation changes" — two MAM-simple copies were already stale
    (finding 6). (f) `4195440e` "Update the … source-hygiene test for the landed tree" — run by nothing
    (finding 8.1). (g) `bf8969e1` "Add current README files for landed product directories" — five
    added, `diffable-pointed-hebrew/README.md` modified. (h) `d325a21b` credits `23d8ba3b` with survey-module
    changes it did not make (all eight non-rename string differences come from `9eedccbd`). (i)
    `6b536ee1` "Name the verses of Job's prose frame and main poetic section" names no verse. (j)
    `4f3d26fb` "written blind to a concurrent Codex review of the same range (doc/dual-agent-review.md,
    Design B)" — the Codex review was later (`820232ef`, 16:23) and Design A; and "The reconciliation …
    is a later task for a session that wrote neither file" — the Codex session wrote it 73 minutes
    later (`2988abf2`). (k) `95525845` and `e22a5180`, subject-only, changed a tracked artifact
    (`misc/zarqa-table-diff/zarqa-table-from-open-siddur-project.dph.txt`, three entries) without a word;
    the trio plan's lines 356–361 record it. (l) Five post-stress-meteg subjects true when written and
    superseded since: `522083fa` (punctuation column, folded by `b721fe34`), `64444d4b` (Jeremiah 46:14
    as misc, reclassified by `d6d3bf44`), `9727e35b` (crop position, moved by `8de50290`), `387c4f9e`
    (3,181 records, 496 now), `3b4c7df2` (the lamed/guttural/resh sentence, removed by `13ae0848`).

## Open ends the window itself declares (not findings)

The fourth stage's Phase 5 (MAM-OSIS) and Phase 6 are unstarted; MAM-OSIS is the last sibling the
mega writes, with the MAM-private census. Six commits landed on `main` after the anchor (11:26–11:56)
and are unreviewed. The MAM-for-Sefaria clone awaits its Remove step (finding 9.1). The eleven deferred
Holman meteg edits of the last review's open ends, and the ten extra phonetic-hbo verses of finding
23.5, will reach `in/mam-ws` at the next `fr-wikisource` refresh, a known-cause future diff that wants a
mega — which will also rewrite the 385 files of finding 5 and empty the file of finding 4 unless that
is fixed first. #264 is open with 0 comments, and the empty `d4d1` directory of finding 23.2 is not the
case it describes (it is in no workspace file). The post-stress-meteg page's census numbers (finding 3)
are published at `bdenckla.github.io/MAM-basics/post-stress-meteg.html`. The Codex half of this
dual-agent window has not been run.

## What this review did not check

1. Anything in MAM-private, github-misc beyond the plumbing identity, or hbofonts: the Phonetic MAM
   standard set itself (its public rendering on phonetic-hbo's pages was used instead), Yeivin's ITM
   and Breuer's CoS (every attribution and grading on the post-stress-meteg pages was checked for form
   only), the mgketer phase of the Holman work, and the MAM-private repoint `6b92090a` records.
2. Regeneration of any generator that writes tracked files in place (the mega, the MAM product
   generators, the Aleppo and Leningrad index generators, the spread splitter); regenerated to
   scratch instead: the seven post-stress-meteg pages, the two `check_line_breaks` reports, the five
   diffable-pointed-hebrew outputs, `pipeline.dot`. So the mtime and byte-identity claims of the
   fourth-stage records for the product generators are taken from the record.
3. The recorded test counts of the phases (973, 974, 975; "47 tests", "7 tests and 27 subtests") —
   recorded runs; only the 976 at HEAD was re-run.
4. The MAM-parsed and MAM-with-doc clone safety reports (the clones are in the Recycle Bin), the
   Pages runs beyond their metadata and today's live pages, and the contents of the Recycle Bin.
5. The six commits after the anchor, `6b5e4a40` … `d5a2238f`.
6. The nine deḥi-versus-meteg differences of finding 3 (whether MAM changed after the refresh or
   Phonetic MAM transforms them is not decidable from public data), and the two prose entries of the
   +309 that are not variant words.
7. Whether the 108 pre-existing non-MAM-normal runs of the tree-health section are deliberate
   illustrations of Unicode-normal order.

## Inputs for the reconciliation with the Codex review

Anchors for comparison: MAM-basics `b4706759..8bf586a3`; the sibling ranges in the table above; the
six repos read on GitHub at the commits the table names. Each finding above gives the commit, the
file and line as of `8bf586a3`, the claim, the measurement, and the command or `.novc/review-2026-09-07/`
script that re-establishes it, so a disagreement can be checked by hand without re-deriving the whole
window. Findings 1, 2, 3, 4, 5 and 7 were re-derived by the main session as well as by their streams
(the two scan crops were read, the reader and the XML element read, the `Job.xml` path resolved, the
old-URL grep and the redirect default read). The reconciliation section goes below this one, under
`## Reconciliation with the Codex review`, per `doc/dual-agent-review.md`.

## Reconciliation with the Codex review

This window used Design A. Codex read this Claude review deliberately, checked selected claims
against the same anchors, and looked for an unaccounted commit or defect. The Codex result is
`doc/codex-review-findings-2026-09-07.md`. Under the Design A procedure in
`doc/dual-agent-review.md`, the Codex reviewer writes this comparison because Design A is anchored
by construction; a fresh third reviewer is required only for Design B.

### Claude claims confirmed by Codex

Codex independently confirmed nine selected claims:

1. Finding 1's Deuteronomy 32:6 reader and XML mechanism.
2. Finding 4's nonexistent MAM-simple Job XML path.
3. Finding 5's 669 stale generated MAM-with-doc URLs outside the stated records and data.
4. Finding 7's MAM-simple redirect default and the stale wlc-utils documentation.
5. Findings 8.1 and 8.2's NFC and MAM-mark-order coverage gaps.
6. Finding 13.1's disagreement between the type-3 page definition and its classifier.
7. Findings 14.1 and 14.2's licence-coverage gaps.
8. Finding 15's second Linux clone roster.
9. Finding 18's stale instruction-file count and incompatible read-only instruction.

### Claude claims rejected by Codex

None among the selected claims Codex checked. Design A did not independently check every claim in
this file, so this result does not endorse the claims outside the selected set.

### Claude omission found by Codex

None in the selected commit and static checks. Codex re-derived the 257 / 220 commit census, found
no new `sys.path` mutation in the reviewed Python diff, and verified that the six commits after the
anchor change only the thirteen paths this report declares. Those checks do not establish that no
unselected omission exists.

### Claude claims not independently checked by Codex

The unselected claims are listed in `doc/codex-review-findings-2026-09-07.md` under
`## Limits of the Codex review`. The Codex review also did not recreate or inspect the absent public
source clones, and it preserved the Claude report's public-only boundary.

## Reconciliation with the Codex Sol re-review

The additional Design A run is recorded in
`doc/codex-review-findings-2026-09-07-sol.md`. The Sol report preserves both the Terra report and
the Terra reconciliation above. The Sol report checked a largely separate selection of claims.
The Sol reviewer accidentally saw the Terra reconciliation summary before switching to the frozen
Claude blob, but did not read the Terra report until after freezing the Sol findings; the Sol report
therefore records an explicit independence caveat.

### Claude claims confirmed by Codex Sol

Codex Sol independently confirmed ten selected claim groups:

1. Finding 2's Deuteronomy 33:29 placement.
2. Finding 6's census of five stale vendored copies.
3. Finding 10's checked stale and incorrect review records.
4. Finding 12's checked stale post-stress-meteg records.
5. Findings 13.2 and 13.3's residual classifier names and unsupported BHS prose.
6. Findings 14.3, 14.4, and 14.5's placement, licence, and font-exception gaps.
7. Finding 16's MAM-mark-order counts.
8. Findings 17.1 and 17.3's overbroad comparison key and premature output-path calculation.
9. Finding 19's checked README and licence errors.
10. Finding 20's 576-page link graph, eleven orphans, and zero dead internal targets.

### Claude claims rejected in part by Codex Sol

1. Finding 3 has the correct core diagnosis and the correct later corpus counts, but its opening
   phrase gives the wrong unit. The public pages have 368 qamats-variant rows containing 370
   duplicated chanted words. Psalms 35:10 and Proverbs 19:7 each place two duplicated chanted words
   in one row.
2. The scope census correctly gives 99 commits with a co-author trailer, but says the trailers are
   spelled four ways. The parenthetical list and the independent census have five exact trailer
   lines. Finding 23.1's narrower statement that the Codex trailer has three spellings remains
   correct.

### Claude omission found by Codex Sol

`git diff --check b4706759..8bf586a3` reports 210 whitespace errors in landed product artifacts: 21
trailing-space lines and 189 blank final lines. The errors arrived in `cf7c7a35` and `4195440e`
from the source products. The result is an artifact-hygiene finding rather than a behavioral
defect, but the Claude review did not record the failing `git diff --check` result.

### Relation between the Terra and Sol Codex reviews

The Terra report's no-rejection and no-omission conclusion remains accurate for the claims and
checks selected by Terra. The Sol report adds the two partial corrections and the omitted
artifact-hygiene finding above; the Sol report does not replace or revise the Terra report.

### Claude claims not independently checked by Codex Sol

The Sol limits are listed in `doc/codex-review-findings-2026-09-07-sol.md` under
`## Limits of the Sol re-review`. Codex Sol did not rerun the full suite, the mega pipeline,
artifact generators, GitHub Pages deployments, issue state, mutable worktree state, private-side
facts, source-clone safety reports, source-book claims, or every code fragility under finding 17.

## Dispositions after remediation, 2026-09-08

Every remediation finding is fixed, rejected with a reason, recorded, or referred to repository
maintenance. Ben's decision on 2026-09-08 decouples finding 23.2's worktree housekeeping from
remediation completion and tracks it separately.

| Finding | Disposition | Evidence |
|---:|---|---|
| 1 | fixed | `c76239a5` repairs every live `sdt-target` shape and the full-corpus reader probe. |
| 2 | fixed | `c76239a5` restores the Deuteronomy 33:29 chanted word to the beginning of Aleppo leaf 006r. |
| 3 | fixed | `e91d7358` counts each `מ:קמץ` row once in the MAM census. The Sol correction of 368 rows and 370 duplicate entries was right for the review anchor; the 2026-09-08 source has 370 rows and 372 duplicate entries. Psalms 35:10 and Proverbs 19:7 remain the two measured grouping differences. Ben's 2026-09-08 decision accepts selecting exactly one parameter without a separate effect analysis; the implementation selects `ד`, never both `ד` and `ס`. |
| 4 | fixed | `c76239a5` corrects the Job XML path and makes a failed input parse preserve the prior output. |
| 5 | fixed | `4afe3ebc` regenerates every affected product; the final census has no old-host URL in owned generated output. |
| 6 | fixed | `4afe3ebc` makes all 44 MAM-simple support copies LF-stable and source-identical and corrects the inventory count. |
| 7 | fixed | `9cf48863` requires an explicit `--repo` for both redirect commands. Bare-command adverse probes fail, and an explicit wlc-utils build/check passes with 154 stubs plus `404.html`. |
| 8 | fixed | `a42216ee` consolidates the NFC scope, restores MAM-simple mark-order coverage, adds deploy-root HTML coverage, and extends the machine-path lint. |
| 9 | fixed | `9cf48863` corrects the fourth-stage records. The clean MAM-for-Sefaria clone at `cf23b478` was moved to the Windows Recycle Bin after the unreachable `34c94a8` patch was matched to reachable `746d6d2`. MAM-simple redirect-host commit `376912a` dates its breadcrumb and is pushed on that host's `main`. |
| 10 | fixed | `9cf48863` corrects the third-stage records and expands the maintenance runbook from the current rules. |
| 11 | fixed | `e91d7358` repairs the post-stress records; `9cf48863` repairs the remaining current records and prose while preserving dated history. |
| 12 | fixed | `e91d7358` remeasures and reconciles the survey JSON, eight pages, plans, census note, and fragment links. |
| 13 | fixed | `e91d7358` aligns type 3 with the classifier, completes the type-2 rename, and identifies UXLC 3.9 and WLC 4.22 as the inputs actually read. |
| 14 | fixed | `9cf48863` covers the post-stress analysis, six deploy-root manuscript crops, twelve Taamey D font copies, and the current landed product/source paths without extending a rights grant. |
| 15 | fixed | `9cf48863` retires the three multi-repository Linux scripts and two text rosters while preserving the standalone MAM-basics bootstrap script. |
| 16 | fixed | `a42216ee` puts all 50 inherited Aleppo-page Hebrew runs in MAM mark order and adds a mechanical lint over the three owned Aleppo pages. |
| 17 | fixed | `c76239a5` narrows the line comparison; `e91d7358` hardens the post-stress contracts and sample descriptions; `a42216ee` prevents legacy-history output from selecting a tracked named-release path. |
| 18 | fixed | `9cf48863` updates the live repoint, corpus-count, product-location, and review-procedure docstrings and comments. |
| 19 | fixed | `9cf48863` removes nonexistent options and entry points, corrects package classifications, numbers the announced lists, and separates GPL, MIT, data, and font scopes. |
| 20 | fixed | `9cf48863` adds the two accepted navigation links. The complete graph has 577 HTML pages, nine deliberate orphan pages recorded in the remediation plan, and zero dead internal targets. |
| 21 | fixed | `e91d7358` applies the Hebrew-prose rules to the post-stress analysis; `9cf48863` applies the global prose rules to the remaining current files and disposition. |
| 22 | record only | No instruction file changed during remediation, so the review's verified identity result requires no remediation or private-content publication. |
| 23 | referred to maintenance | Item 23.2's unrelated worktree housekeeping is tracked separately by Ben and is not a remediation completion condition. Items 23.3 and 23.4 are referred to repository maintenance. Item 23.5 is a known future `fr-wikisource` diff, and item 23.6 is a cadence census rather than a code defect. Historical trailers remain unchanged. |
| 24 | record only | Immutable commit subjects and bodies remain unchanged; the corrected facts are preserved in this disposition and the remediation plan. |
| Sol-1 | fixed | `4afe3ebc` regenerates the affected artifacts and makes the current `git diff --check` pass while preserving byte-verbatim and downloaded inputs. |

Finding 23.1's narrower count of three Codex spellings is correct. The complete set among the 99
review-window commits with a co-author trailer has five exact lines:

1. `Co-Authored-By: Codex <noreply@openai.com>` — 92 commits;
2. `Co-Authored-By: Codex <codex@openai.com>` — 3 commits;
3. `Co-authored-by: Codex <noreply@openai.com>` — 2 commits;
4. `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>` — 1 commit; and
5. `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` — 1 commit.

**Rows 13 and 21, revisited 2026-09-09.** Ben's reverts of 2026-09-08 (`1095f029`, `a9edd4f9`)
restored the post-silluq page's one "BHS" row and its sentence, removed the "cant-alef" /
"cant-bet" gloss again, brought back the local ITM and CoS glosses and "on a page of their
own", so row 13's "identifies UXLC 3.9 and WLC 4.22 as the inputs actually read" and that part
of row 21 describe the tree at `975a16c5`, not at `38a606e2`. On 2026-09-09 Ben read the printed
BHS at 1 Samuel 17:5 and confirms the two marks, meteg after silluq, so the page's claim about
BHS rests on that reading; by Ben's decision it is recorded in `_post_silluq_comparison`'s
docstring and in `doc/review-findings-2026-09-08.md`, whose finding 3 has the details, and not
on the page.
