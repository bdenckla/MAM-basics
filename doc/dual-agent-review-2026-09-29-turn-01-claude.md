# Findings of the 2026-09-29 review of MAM-basics since 2026-09-26

State: not yet acted on

Written on 2026-09-29 from about 11:20 New York time, as turn 01 of the standard alternating
dual-agent review under `doc/dual-agent-review.md` (Ben's decision D9 of 2026-09-09), with Claude as
Agent 1 by Ben's choice at the round's setup that day. Asked at setup which area Agent 1 should read
first, Ben chose "No particular concern". This file was frozen at `7549ebf7` before any Codex reviewer
read it, and the Claude session neither read nor sought a Codex half: no file named
`doc/dual-agent-review-2026-09-29-turn-02*` exists. Nothing was fixed. Every figure here was measured
on 2026-09-29 unless it carries another date, and every time is New York time. The reconciliation goes
at the end of this file under `## Reconciliation with the Codex review` once Agent 2's turn 02 is
stable; later State and every disposition go in
`doc/dual-agent-review-2026-09-29-turn-01-claude-update.md`, which does not yet exist.

**The checkout.** This turn ran in the full clone `C:/Users/BenDe/GitRepos2/MAM-basics`, on the local
carrier `dar-2026-09-29` for `origin/dar-2026-09-29`, under the default Ben set that morning: a review
runs in whatever checkout its session is already in. This session fetched at 11:22:09, found
`origin/main` at `7549ebf7`, fast-forwarded the clone's `main` to it at 11:22:15, and created the branch
at 11:22:33 in a new linked worktree, `.claude/worktrees/dar-2026-09-29`, pushing it as
`origin/dar-2026-09-29` at 11:22:42. Only the suite ran there. Ben then wrote "Let's not use a
worktree" and asked that both review procedures name the session's own checkout as the default; that
change is `89c001ba` on `main` (11:33:38), merged with `origin/main` as `3bf60cec` and pushed at
11:34:03, after this window's end anchor and not reviewed here. At his further instruction ("Remove the
worktree quickly/summarily") the worktree was removed with a plain `git worktree remove` between
11:34:03 and 11:35:00, the branch kept, and the full clone switched to the carrier at 11:35:00. Twice
before any stream started, from 11:38:18 to 11:38:31 and from 11:38:58 to 11:41:11, this session checked
out `f4d81285` detached in the same clone to collect and run the suite at the start anchor, and
returned to the carrier each time with `git status --porcelain` empty. Twice, at 11:32:02 and 12:03:21,
a fetch this session did not issue (its reflog form, `--porcelain --verbose --no-write-fetch-head`, is
not this session's) moved the clone's `origin/main`; no tracked file changed.

**The streams.** The window was read by eleven agent streams and this session: (A) the Google
Sheet retirement and the special-page mirror; (B) the MAM-parsed plain retirement and the parser-stage
validation; (C) the Wikisource refresh, the note-link bot run and MAM-with-doc's pages; (D) the change
logs and the stored release archives; (E) the module splits, small code changes and the whole-tree
lints; (F) the 2026-09-26 round's close-out, remediation plan and remediation; (G) the instruction
files, memory retirement, clone forests and deployment; (K) the codex-index image-work retirement, HBCE
Psalms, `BOOK_SCANS_ROOT` and Evr. II B 55; (R) the records of `doc/` and the review procedure; (S) the
skill files the window changed, started when stream G's skills sub-agent had not reported and then set
to check that sub-agent's report once it arrived; and (W) censuses across the whole diff, reader-facing
Markdown, issues and Pages. Each stream was one read-only sub-agent working in this checkout; stream F
used two read-only sub-agents of its own, and streams G and W one each. Every script and output is
untracked under `.novc/review-2026-09-29/`, prefixed with the stream's letter and unprefixed for this
session; each stream's report is `<letter>_report.md`, and the briefs every stream read first are
`stream_common.md` and `brief_<letter>.md`. The streams' process notes record their departures from the
shell rules: stray `python -c "print(1)"` runs by streams K and W, a few compound or pipeline commands,
and reads by streams A and B and G's sub-agent of the harness's saved copies of their own command
output under `~/.claude/projects/`; stream C read the public sibling clone
`C:/Users/BenDe/GitRepos2/phonetic-hbo` and made one read-only Wikisource API query, stream G read the
refs and blobs of the primary forest's MAM-basics clone and listed one untracked file in its `.novc/`,
and stream W and its sub-agent made read-only `gh` queries. None wrote a tracked file, and `git status
--porcelain` was empty at the start and end of every stream. Stream F's sub-agent F_sub1 wrote two
ignored bytecode files under `py/tests/__pycache__/`, and the imports of stream G's sub-agent and of a
verifier wrote bytecode inside the review directory. This session's own shell commands often chained
commands with `;` and piped output through `Select-Object`, `Out-File` or `ForEach-Object` to trim or
save it, against the shell rules of the common instruction body, `dot-Codex/user-wide-AGENTS.md`; none
changed a tracked file.

**The pre-commit check.** Before this file was committed, read-only verifier sub-agents re-measured
every finding and every other passage against `7549ebf7`, each writing only its own `V<N>_*` files and a
`V<N>_report.md` beside the streams' reports (their common brief is `verify_common.md`). V1 took findings
4.1, 10.1, 11 to 13, 14.1, 14.4 and 23 and the Google half of 4.3 (9 passages: 2 confirmed as drafted, 4
with corrections of substance, 3 with corrections of wording); V2 findings 1.2, 1.3, 10.2, 14.2, 14.3, 15
to 17 and 24 (8: 2, 1 and 5); V3 findings 9.2 and 18 to 22 (6: 1 confirmed, and 6 corrections of
substance and 8 of wording within the other 5); V4 findings 25 to 32 and 35, apart from 28.2 and 28.3 (9
passages: 2 confirmed, 3 corrections of substance, 12 of wording); V5 findings 1 to 3 (18 entries: 9, 4
and 5); V6 findings 4 to 9 (30 passages: 17, 7 and 6); and V7 findings 33, 34, 28.2 and 28.3 (16 entries:
7, 3 and 6). Most corrections of substance were attributions, to the commit that wrote a line or the
stream that found an item, and line ranges, baselines of claims older than the window, and absolutes
their own sources defeat. Three of the attribution errors came from reading `git blame` as authorship, so
V9 then checked every attribution in findings 1 to 35 by pickaxe (95 attributions: 90 confirmed, 2
corrections of substance and 3 of wording), and V8 checked the rest of the file and how its parts fit (79
entries: 46 confirmed, 11 corrections of substance and 22 of wording, among them counts in the
tree-health and verifies-sound sections, dates in "Open ends", and one name for the 2026-09-26 close-out
record). This session applied every correction, some in its own words, and adopted item 4.9 from stream
K's report on V6's evidence. Two Hebrew forms that stream C's report quoted in Unicode's canonical order
were caught by V3; this file takes them byte for byte from `MAM-parsed/plus/BC-Kings.json`, and the
assembly script, `assemble.py`, checks every Hebrew run in the file for MAM-normal order, every line for
a right-to-left opening, and the text for backslashes and orphan combining marks. The verifiers' process
notes record departures like the streams': compound `cd … &&` commands and reads of the harness's saved
copies of their own command output; none wrote a tracked file.

**Which review records inside the window are read as subject and which as evidence.** The window's
diff contains review records, so `doc/periodic-review.md`'s section "A prior round's own records inside
a successor window" (Ben's decision of 2026-09-21) requires this turn to say which it reads as subject
and which it treats as evidence:

1. **Evidence, with their form as receipts checked:** the six turn files of the 2026-09-26 round,
   `doc/dual-agent-review-2026-09-26-turn-01-claude.md` through `-turn-06-codex.md`, all added in this
   window. That exchange checked each turn in the next and reached its stopping rule, and Ben decided
   its close-out on 2026-09-27 and 2026-09-28; reviewing its findings again would reopen an exchange only
   Ben can reopen, about a window (`71f96ca3..f4d81285`) this review does not cover. Their conformance
   as tracked receipts (`State:` lines, the turn-01 pointer, no edit after a turn's commit other than the
   specified reconciliation append) is subject, and verifies sound.
2. **Subject:** everything written after that exchange closed: the close-out record,
   `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`, with Ben's close-out decisions and every
   disposition; the remediation plan, `doc/PLAN-remediate-review-findings-2026-09-26.md`; and the
   remediation's code, data, pages and documents, which no review has read.
3. **Subject:** every edit the window made to an earlier round's records, among them
   `doc/dual-agent-review-2026-09-16-turn-01-claude-update.md` and
   `doc/review-findings-2026-09-10-update.md`.

Every other file in the diff is ordinary subject matter. The setup recommended neither disposition, and
no case needed Ben's decision.

## Scope, anchors and census

The tenth review under the public-repos-only scope, counting as the 2026-09-26 review counted itself
the ninth. It covers MAM-basics from the 2026-09-26 review's recorded end anchor, **`f4d81285`**
(2026-09-26 13:30, "aleppo/README.md: name the one annotation editor left"), through **`7549ebf7`**
(2026-09-29 11:21, "Require approval for reusable lessons outside authorized task scope"), which was
`origin/main` when this session fetched at 11:22:09. `f4d81285` is an ancestor of `7549ebf7`
(`git merge-base --is-ancestor`). After the anchor, `origin/main` moved on. At 14:04 on 2026-09-29, immediately before this file was
staged and after a fetch, it stood at `73bb4a7b`, eight commits past `7549ebf7`: the approved six-skill
cloud installation and its records (`8c165838`, `4d3ebf66`, `73bb4a7b`, with the merge `50374e65`), the
retirement of spent maintenance receipts (`e4934b6e`, with the merge `8ab01f49`), and this session's
`89c001ba` with its merge `3bf60cec`. They change 35 paths, among them files that findings 1 to 4, 8 to
12, 14, 23, 28, 29 and 32 to 36 cite (`postanchor.py`): `e4934b6e` retired documents several findings
cite, among them `doc/PLAN-retire-google-sheet.md`, `doc/PLAN-remediate-review-findings-2026-09-14-update.md`
and both symmetric-instructions plan files, and `4d3ebf66` rewrote instruction and skill files that
findings 23, 28 and 34 cite. So some findings may already be fixed, moved or retired on `main`. This turn
did not review those commits; every finding and figure here is of `7549ebf7`.

**91 commits, 77 of them non-merge and 14 merges** (`git rev-list --count f4d81285..7549ebf7`, with
`--no-merges` and `--merges`). The diff changes **804 paths** with rename detection (415 modified, 148
added, 214 deleted, 27 renamed) and **831** without it (415 modified, 175 added, 241 deleted), with
**46,672 insertions and 1,099,256 deletions** with rename detection (49,386 and 1,101,970 without).
The 27 renames are 20 images under `gh-pages/img/`, two Holman assets, and five Python and data files:
`py/py_ac_loc/mam_xml_verses.py` to `py/mb_cmn/`, `py/mb_cmn/plain_template_schema.py` to
`parser_stage_template_schema.py`, `py/py_misc/mam_parsed_plain.py` to `mam_parser_stage.py`,
`py/tmpl_survey/expanded_stack_grammar_plain.lock.json` to
`py/verify_mp/expanded_stack_grammar_parser_stage.lock.json`, and `py/verify_mp/verifiers_both.py` to
`verifiers_templates.py`. 92 paths are binary without rename detection: the new release archive
`MAM-parsed/historical/cb95915d54e6cfdd38babef710d46f48a2c4acf5.zip`, 37 deleted Aleppo page scans, 14
deleted cam1753 spreads, and both names of each of the 20 renamed images. By top-level entry, without
rename detection: `py/` 261, `gh-pages/` 137, `MAM-parsed/` 80, `in/` 69, `doc/` 66, `hbce-psalms/` 55,
`aleppo/` 42, `out/` 35, `cam1753/` 20, `dot-claude/` 20, `MAM-simple/` 9, `dot-Codex/` 8,
`evr-ii-b-55/` 5, `holman/` 5, `misc/` 4, one each under `.claude/`, `.vscode/`, `MAM-OSIS/`,
`MAM-for-Sefaria/`, `MAM-with-doc/`, `book-of-job/`, `py-examples-out/` and `uxlc/`, and seven files at
the root (`.gitattributes`, `.gitignore`, `AGENTS.md`, `DATA-LICENSES.md`, `README.md`,
`constraints.txt`, `requirements.txt`). The deletions are dominated by `MAM-parsed/` (1,031,455 lines,
the retired plain and Google products) and `in/` (25,944, most of them the retired Google Sheet exports
under `in/mam-go/`).

The tree went from 4,745 to **4,679** tracked files: `.py` 1,068 to 1,027 (1,060 to 1,019 under `py/`),
`py/tests/` 112 to 115, `gh-pages/` 1,900 to 1,894 files (588 HTML at both), `doc/**/*.md` 100 to 117
(96 to 113 direct children), `doc/PLAN-*.md` 16 to 22, `doc/*-update.md` 20 to 27, `MAM-parsed/` 91 to
43, `in/` 289 to 320, `out/` 338 to 329, `aleppo/` 134 to 97, `cam1753/` 97 to 82, `hbce-psalms/` 0 to
55, and `dot-claude/` 23 and `dot-Codex/` 10 at both. Of the product trees, `MAM-parsed/plus`,
`MAM-simple` and `gh-pages` changed, `MAM-parsed/plain` and `MAM-parsed/google` are gone, and
`MAM-for-Sefaria`, `MAM-OSIS` and `MAM-with-doc` changed only their `LICENSE.md` files (`git rev-parse
<anchor>:<dir>`). Re-establish: `census.py` → `census.txt`, `commits_files.py` → `commits_files.txt`.

The window's substance is eight things:

1. The 2026-09-26 round from its argument to its remediation: the six turn files (`47599802` through
   `db62361e`), Ben's close-out decisions (`f8b77adb`, `73f1dfe1`, `572fa2ab`, `8ab079af`), the
   remediation plan (`5f2affeb`, `1a92af88`, `93fe8704`) and its execution (`22d18d72`, with the merge
   `2374ea30` and the records `583a0c2e` and `8c2fa6c3`).
2. The retirement of the Google Sheet pipeline (`a41fbcdd`, `81825cf0`, `c450060e`), with a new mirror
   of the 36 declared Wikisource special pages and a refreshed mirror of the MAM introduction.
3. The retirement of MAM-parsed plain (`4d4385c3`, `87fc7141`, `1e14a8a1`), keeping the parser stage
   as a validated transient stage (`24b7f23a`, `146f6145`).
4. The retirement of the codex-index image work's programs, page scans and procedures (`65f5a1c6`), and
   the HBCE Psalms comparison kept in MAM-basics as a frozen record (`fc819f6b`, `a3ca231e`).
5. A Wikisource refresh of four chapters (`97c4aff5`) and a note-link bot run that edited four more
   (`298958d3`), with MAM-with-doc page fixes (`fef1a416` through `103b2308`) and regenerated change logs.
6. The first release archive written by a tracked builder, with a pin command and a guard (`428f5462`,
   `04133265`, `0ba7498b`, `bfcc34a9`).
7. Four module splits (worktree retirement, the chanted-word-accents survey, the CLC oracle, the
   post-silluq image pages) and small tooling changes (`py/main_test.py`, `BOOK_SCANS_ROOT`).
8. Memory retirement and instruction consolidation (`0e254fdc`, `c6962aa9`, `cb9ae042`), independent
   clone forests with pinned environments (`7cf780e1`, `9fabe026`, `eea4c583`), branch-based review
   handoffs (`a367f962`) and the rule on new reusable lessons (`7549ebf7`).

## Tree health at `7549ebf7`: the suite at 1,011, the mega clean at 52 steps, two ruff errors

- **Suite: 1,011 passed, 5 skipped, 60 subtests passed** (145.29 s), run in this checkout with
  `C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider`
  and no `REPOS_ROOT`, `git status --porcelain` empty afterwards; this session's earlier run in the
  removed worktree at the same commit gave the same counts (169.72 s). At `f4d81285`, run the same way
  in this checkout with `-v`: **1,006 passed, 5 skipped, 115 subtests passed** (128.90 s); at `7549ebf7`
  with `-v`, the same counts as above (164.37 s). The five skips are the same five ids at both anchors,
  `test_edition_transcriptions.py`'s semantic channel. The suite's Phonetic MAM test reads MAM-private,
  as earlier reviews' runs did; this review read nothing there itself. The collected ids go from 1,011
  to 1,016: 19 only at the start (6 in `test_explicit_claims.py`, 4 each in
  `test_diff_mpplus_unpinned_latest.py` and `test_tmpl_survey_plus_invariants.py`, 2 each in
  `test_stack_path_lookup.py` and `test_tmpl_survey_nesting_normal_form.py`, 1 in
  `test_mam_xml_verses.py`) and 24 only at the end (6 in `test_wikisource_special_page_download.py`, 4
  in `test_diff_mpplus_unpinned_latest.py`, 2 each in `test_entry_point_subcommands.py`,
  `test_mam_xml_verses.py`, `test_mpplus_alternative_oracle.py`,
  `test_mpplus_historical_archives.py` and `test_tmpl_survey_nesting_normal_form.py`, 1 each in
  `test_product_scopes.py`, `test_public_data_consumer_notices.py`, `test_scan_overlay_viewboxes.py`
  and `test_stack_path_lookup.py`) (`test_counts.py` → `test_counts.txt`). The subtests fell by 55:
  `test_diff_mpplus_unpinned_latest.py` gave 50 at `f4d81285` (three sites over 15 artifact names plus
  5 selectors, measured by stream D in an extracted start tree) and none at `7549ebf7`, and
  `test_explicit_claims.py` lost its five-id loop over `mp.plain` claims with plain (13 to 8; stream B).
- **Mega: all 52 steps pass and leave no diff**, `git status --porcelain` and `git diff --stat` both
  empty afterwards, run once in this checkout at `7549ebf7` with the same interpreter and no
  `REPOS_ROOT`, from 11:44:27 to 11:49:15, 281.7 s of it in the 52 steps, with nothing else running
  (`mega.txt`, `status_after_mega.txt`). The step table has 54 entries at `f4d81285` and 52 at
  `7549ebf7`; the two gone are `parse-go` and `diff-wsgo`, the Google Sheet steps, and every declared
  step ran (`mega_steps.py`). The Graphviz pre-check reports the pinned 16.0.0 and that Helvetica and
  the default font load. The claims check passed 50 of 50 with none pending. The mega's
  post-stress-meteg survey step read this forest's MAM-private Phonetic MAM, as the suite's Phonetic MAM
  test did; this review read nothing there itself.
- **The generators the mega does not run.** `py/main_mam4sef.py` and `py/main_mam_osis.py` were not
  run: by Ben's decision of 2026-09-12 they are not kept continuously current, as both products'
  READMEs say. This session checked instead whether their products carry the window's two text changes,
  at Judges 19:23 and 2 Kings 22:1, which the refresh `97c4aff5` changed in MAM-simple: MAM-for-Sefaria's
  rows for both verses (both CSV sets) still hold the old words, as do MAM-OSIS's `MAPM-24` files and
  `mapm.osis.xml`, while its `MAPM-orig*` sets hold neither form of the 2 Kings 22:1 word
  (`root_handrun_lag.py` → `root_handrun_lag.txt`; item 36.2). `py/main_hbce_psalms.py compare` was not rerun, by Ben's decision of 2026-09-26 that
  `hbce-psalms/out/` is a frozen record; its `lint-receipt` reports "0 problems" (stream K).
- **Lints** (stream E, black 26.5.1, ruff 0.16.5, CPython 3.13.15). `black --check py`: 1,019 files
  would be left unchanged (1,060 at `f4d81285`, reproduced). `ruff check py`: **2 errors**, F823 at
  `py/tmpl_survey/stack_path_lookup.py:75` (finding 1.2) and F401 at `py/verify_mp/verifiers_plus.py:14`
  (finding 14.2); the 2026-09-26 turn's one error, F401 at
  `py/author_site/post_stress_meteg_post_silluq_page.py:92`, reproduces at `f4d81285` and is gone from
  `22d18d72` on. `py/main_repo_util.py --check-repo-standards --repos MAM-basics`, which writes nothing
  without `--report-*`: `SYS_PATH_MUTATIONS=0`, `SYS_PATH_IN_TESTS=0`, `ORPHAN_MARKS=0`,
  `HEX_ESCAPES=76`, `NFC_H_DOT=25`, `NFC_LATIN=32`, `ROOT_CONFTEST=False`, `SHIM_CONFIG=None`,
  `GITATTRIBUTES_LF=True`; recomputed from blobs with the checker's own functions, 80, 30 and 39 at
  `f4d81285`, every decrease traced to files `65f5a1c6`, `87fc7141` and `a41fbcdd` deleted, and to one
  escaped line `87fc7141` removed from `py/author_misc/mp_cmn_rows_core.py` (`E_standards_compare.py`); `LINKED_WORKTREES=0` and `AGENT_BRANCHES=0` describe this clone. `git
  ls-files --eol`: 0 `i/crlf` and 0 `i/mixed` over 4,679 entries. `git diff --check f4d81285 7549ebf7`
  prints nothing; under the start tree's attributes it reports 2,053 trailing-whitespace lines, 1,756 in
  six `hbce-psalms/out/*.tsv` and 297 in eleven `in/mam-ws-special/*.mediawiki`, which
  `.gitattributes:19–22` (`fc819f6b`) and `:35–36` (`a41fbcdd`) exempt.
- **Mark order** (stream W, `W_01_mark_order.py`). The added lines of 164 files hold pointed clusters.
  Clusters out of MAM-normal order sit in 67 exempt files: `hbce-psalms/in/transcriptions/` 126 in 13
  files and `hbce-psalms/out/` 60 in 5 (both counts equal `doc/mam-normal-mark-order.md:44–47`, which
  exempts them), `in/mam-ws-special/` 5,369 in 25, `in/mam-ws-intro/` 59 in 2, `in/mam-ws/` 76 in 7,
  `out/mam-ws-bot/proto/` 76 in the same 7 books, and `out/mam-ws-bot/proto-fmt-2/` and
  `out/mam-ws-parsed-fmt-2/` 20 each in 4. Outside them, 12 clusters in 2 files, every one a verbatim move
  of a pre-window line (`e329557b`'s CLC oracle, 11; `f922501a`'s inventory module, 1). The 63 shipped
  files under `MAM-parsed/plus/` (24) and `MAM-for-Sefaria/csv/` (39) are in MAM-normal order.
  `py/tests/test_prose_mark_order.py` passes.
- **Markdown links** (stream W, `W_02_md_links.py`). Of the 344 non-absolute links in the 259 tracked
  `.md` files at `7549ebf7`, 331 resolve, and all 26 with a fragment resolve by GitHub's anchor rules;
  of the 13 that do not, 10 are inside the 2026-09-26 turn 01's quotations of earlier findings and 3
  are older than the window. Outside that turn file the window created no dead link and fixed one
  (`uxlc/doc/clc-design.md:287`). All 115 pinned `github.com/bdenckla/MAM-basics` blob and tree links
  resolve to an existing commit, path and heading.
- **HTML.** `py/check_html_syntax_and_sanity.py` reports "No HTML output issues found." in its default
  mode, which checks book-of-job's pages, and as `gh-pages --deploy-root`, which also gives an
  informational count of 1,140 undefined CSS class references (stream W). Run on the sub-sites the window
  changed, `gh-pages/MAM-with-doc` goes from 79 issues at `f4d81285` to 74 (the five duplicate ids
  `fef1a416` removed). `gh-pages/MAM-parsed` goes from 12 to 16: the six plain call-graph SVGs the check
  counted as unexpected files are gone, and the ten static pages the plain retirement left are unlinked,
  as the plain plan intends (`V8_05_html.py`).
- **Pages.** Three runs of `pages.yml` had a window commit as head, all scheduled and successful:
  36306464351 (`63bd060e`, 2026-09-27 04:31), 36399039371 (`85cb7acd`, 2026-09-28 04:43) and
  36543719607 (`c6962aa9`, 2026-09-29 04:35). The seven later window commits change no `gh-pages/`
  path, so the deployed site equals `7549ebf7`'s `gh-pages/` (stream W's sub-agent).
- **The user-level homes** (stream G). All 19 live content destinations match the primary forest's
  `origin/main` at `50374e65`, seven commits past `7549ebf7`; each difference from `7549ebf7` is one that
  post-window `4d3ebf66` made. The retired `worktree-forest` skill is absent from
  `~/.agents/skills/`. `--sync-user-config --check` was not run, because it fetches.
- **Issues** (stream W's sub-agent). Ten MAM-basics issues had activity from 2026-09-26 15:00 to
  2026-09-29 11:30: 8 closes (#241 as not planned, #279, #281, #288, #291, #292, #293, #294), 11 comments,
  2 retitles and 3 commit references; no issue was opened, reopened, labelled or assigned. The ten
  comments posted through `bdenckla` each open with a dated agent line; seven of the eight closes had a
  reason comment posted with them, and every commit each names was committed before the close. The
  eighth, #294's, is under "Noticed outside the diff". Earlier in the window's span, at 13:30:35 on
  2026-09-26, #234 was closed as not planned with a dated reason comment (`V8_08_issue_234.py`).

## What verifies sound, stream by stream

**The census, the tests and the mega (this session).** The window's commit and path counts, the
tracked-file census and the product-tree identities are the census section's; the suite's change from
1,006 to 1,011 passed is accounted for id by id and its subtests' fall of 55 by file; the mega's two
retired steps are the Google Sheet's.

**The 2026-09-26 round's close-out, plan and remediation (stream F, with two sub-agents).** Every one of
the 2026-09-26 turn 01's 35 findings, and Ben's 36th item, has a disposition in the close-out record
(`doc/dual-agent-review-2026-09-26-turn-01-claude-update.md:182–307`, execution table 537–572); the one
question the record raised without a disposition is the new terminology's standing home (finding 8.2).
The decision package follows turns 03 and 04, and Ben's words are quoted identically where the close-out
record and the remediation plan carry them ("I agree to the term "digital page."", "I
concur.", "I approve", "yes you may push"). The recorded gates re-measure: the change-log counts (59,
565, 28, 113, 33, 76 and 4 JSON entries; 59, 565, 28, 117, 35, 78 and 4 cards), the 18 alternative
changes, the 57 `.py` paths, the tree ids, the 52 mega steps, the 80 claims with one pending, and the 21
deployment mappings. The twenty image renames are pure renames with identical blobs, and each new name
component equals `consensus_to_ascii` of MAM-simple's verse-final chanted word; the captions, the
Cambridge label table (16 of 16 rows), the reader guides' three Job verses and
the XML guide's 3,381 between-verse breaks hold. The merges `d13270a0` and `9c516a2a` resolve nothing;
`2374ea30` keeps both the remediation and the splits (stream E). Of the remediation plan's 36 items,
stream F tabulates which landed as specified and which did not (`F_report.md`, Appendix A); the lost,
partial or faulty changes are findings 1.1, 2 to 6 and 8, finding 7 reports behaviour the plan
specified, and finding 9 is stream R's.

**The Google Sheet retirement (stream A).** The mega's step list, `py/pipeline_graph/pipeline_graph_spec.py`,
the rendered graphs, `NOT_IN_MEGA` (79 entries naming 39 programs, none retired) and
`py/product_scopes.py` agree. The special-page mirror's 36 slugs, 36 files, 36 manifest entries and the
declared inventory agree; every size and SHA-256 matches; the only overlap with the chapter mirror is the
eight declared chapters, at the same revisions; the downloader validates everything before its first
write, writes the manifest last, and raises on every unexpected response. The introduction mirror's 13
files match its manifest (sizes summing 1,852,837 at `f4d81285` and 1,886,674 at `7549ebf7`), and
`index-aleppo`'s 601 Bar-Hama links became 601 template calls. The plan's figures (8 differences and 5
auto-edits at `f4d81285`; 25 and 25 at `86132514`) reproduce, its `State:` line moved in the right
commits, and consumer-facing text presents neither the Sheet nor `MAM-parsed/google/` as live. No code
imports or writes a deleted module or path, and the other mentions of retired names are receipts,
past-tense text or same-named copies (`A_01_stem_search.py`, 4,679 blobs), except findings 4.3, 14.1 and
14.4.

**The MAM-parsed plain retirement (stream B).** The transient parser stage is the retired plain payload
less its notice, held in memory: all 24 groups built at `7549ebf7` equal the last committed plain files
without `header.consumer_notice`. All 24 pass the validation, the plus JSON regenerated in memory equals
every committed blob, and 19 injected parser-stage defects each raise at the expected check. Both grammar
locks equal the grammar inferred from current data (173 edges and 196 order pairs for the parser stage,
97 and 119 for plus). `out/tmpl-survey-plus/plus.json`'s growth is the embedded mpasuq (12,242 lines,
532 flirecs), equal to the plain survey's; the six plus call-graph SVGs match their DOT files. The
retirement removed 25, 6 and 7 files from `MAM-parsed/plain/`, `gh-pages/MAM-parsed/plain/` and
`out/tmpl-survey-plain/`, rewrote the other eight pages under `gh-pages/MAM-parsed/plain/` as static
pages, and left ten static pages with one consistent account. Of 80 claims, all 19 that
applied to both products survive as plus claims, and the mega passed 50 of 50.

**The refresh, the bot run and MAM-with-doc (stream C).** The refresh changed four chapter records and
the bot run's download four more, one verse each; MAM-parsed plus, the bot and parsed-format outputs,
and the sigil and qere inventories change exactly at those verses and recompute from each revision's
plus data, and MAM-simple changes only at Judges 19:23 and 2 Kings 22:1, the two whose Scripture
changed. Over all 115 MAM-with-doc pages: no duplicate id among 23,858; all 4,331 local
fragment links resolve; all 152 note links name a note with the same lemma; no block-level tag inside an
open `<p>`; no raw space in any link or image path; no line break after a `<wbr>` that loses a space.
Applying the two bot edit files to the pre-run chapters reproduces the post-run downloads, one read-only
API query confirmed the four saved revisions, and the five links render as links. The survey's two
changed counts follow from Judges 19:23.

**The change logs and the release archives (stream D).** All seven archives hash as their manifest
lists; `cb95915` is the 2026-09-17 release's end; the relabelling is consistent across `releases.json`,
the index and every release page. The guard refuses an unstored boundary on every guarded path before
comparing anything, and `--archive` and `--pin` refuse every malformed, taken, reserved or empty case
tried; the dispatch is closed. The published change log equals a fresh regeneration, and an independent
comparison of `cb95915`'s archive with `7549ebf7` finds the same four reported verses and nine
notes-only or column-0 changes.

**The codex-index retirement, HBCE Psalms, the scan archive and Evr. II B 55 (stream K).** No live
reference names a deleted program, scan or document as present, apart from the page-index header the
plan left (item 36.12); `65f5a1c6`'s counts reproduce. The move of `mam_xml_verses.py` kept behaviour
(23,202 verses and 305,439 atoms identical), the window's one behaviour change being the Psalms 10:5 fix.
No HBCE code contacts the site, every figure of the dated HBCE receipt that stream K checked reproduces
from the frozen outputs, and `BOOK_SCANS_ROOT` replaced `WLC_SCANS_DIR` everywhere; the Evr. II B 55 index's 25 atom
fields match the reader and the README's eight letter counts recount exactly.

**The module splits and the test entry point (stream E).** Every split moved its definitions verbatim
(identical syntax trees for 56, 63, 43 and 75 items, the docstring-only commits aside), the layering holds,
512 references into the new modules resolve, and no living text cites a moved definition under its old
module. `py/main_test.py` behaves as `AGENTS.md`, "Running tests", says in 15 argument patterns and
creates `.novc` only at the checkout root. The corrected count in `uxlc/doc/clc-design.md`'s §7.16
status row (`:1083`, `71d17913`) re-counts from MAM's wikitext as 15 (11 legarmeh and 4 paseq).

**The instructions, forests, memory retirement and deployment (stream G, with a sub-agent, and stream
S).** Every path, function, heading, count and command `AGENTS.md`, the common body, both configuration
READMEs and `doc/clone-forests.md` name exists; the common body's new rule on reusable lessons is word
for word the proposal Ben approved. The forest code runs no destructive Git operation and fails loudly
on a missing source clone or origin; `constraints.txt` pins all 19 direct requirements, and this
checkout's environment matches it exactly. The memory records publish no MAM-private content and no
memory text, and show the retirement followed its rule: a verified backup, and Ben's approval of the
exact 247-file deletion list. The cloud hook parses (`bash -n`) and changed only in comments. In the
skills, no changed file presents a retired thing as current, every command `7cf780e1` converted runs from
the selected checkout, and the `hebrew-prose` edits agree with the rest of the skill on terminology and
the maqaf rule.

**The records and the review procedure (stream R).** At `7549ebf7`, 65 files require a line-3 `State:`
and all 65 have one, 63 in a declared form (the exceptions are finding 9.1); every base with an update
carries the line-4 pointer (28 of 28); the eight pointer insertions were the only edits their bases took;
every document the window finished stays byte-identical to its finishing commit, apart from the Google
Sheet plan (item 36.9); and the six 2026-09-26 turn files hold as receipts. Every section, pinned link and
figure the two procedure documents cite resolves, and they agree with `AGENTS.md`, the common body and the
skills on the shared branch, carriers, handoff, one writer, cadence and integration.

**The censuses and reader-facing surfaces (stream W).** The mark-order, link, HTML, Pages and issue
figures are the tree-health section's. Of 117 terminology hits outside the 2026-09-26 turn files, 79 are
in text moved verbatim and the 38 in new text, each read in context, break no rule of the `hebrew-prose`
skill. Every clock-derived date the window added to a page carries ", New York time"; no added line has
an orphan combining mark or a decomposed Latin letter, and none outside the 2026-09-26 turn-01 file,
whose two quote an external spelling, has a backslash path; no tracked filename has a Hebrew letter. The Holman assets'
renames reached every live reference, `gh-pages/index.html`'s one change gives its Hebrew an English
runway, and the licence set agrees that every MAM product is CC BY-SA 4.0 with attribution to Hebrew
Wikisource.

## Findings

Findings 1 to 9 concern the 2026-09-26 round's close-out and remediation and the merge that undid part
of it; 10 to 24 the window's retirements and data work (10 to 14 what the Google Sheet and plain
retirements left, 15 to 17 the plain retirement's validation, 18 and 19 the codex-index retirement, 20
and 21 the HBCE comparison, 22 and 23 the refresh and the bot run, 24 the release archives); 25 to 35
the instructions, skills, forests and procedure; and 36 collects items for Ben's judgment that this
review does not call defects. Each lead says its disposition at `7549ebf7`, and nothing here was fixed.
Under `doc/periodic-review.md`'s "Present remediation by public-facing risk", the public-facing documents
(rendered HTML and reader-facing Markdown) are in findings 1.1 (`gh-pages/MAM-parsed/plus/html/mpplus.html`),
2.1, 3, 10 (among them the five product licences), 13, 18, 20, 24, 27 and 28.6; the one public-facing data
change is 1.1's notice in all 24 MAM-parsed plus files; the rest are lower-risk, and finding 22 also
concerns phonetic-hbo's published page, outside this repository. No finding concerns MAM's own text:
every product the mega writes reproduces, and MAM's text in each changed only at verses the refresh and
the bot run changed.

### 1. The merge of `main` into the plain-retirement branch, `ebbfa90f`, undid the remediation's narpas-order fix in the distributed data and the published guide, dropped two corrections of a live update, and broke the stack-path lookup

**Unfixed at `7549ebf7`.** Streams F, B, E and R. `ebbfa90f` "Merge main before MAM-parsed plain
retirement integration" (2026-09-28 22:29:53) merged `main` at `52f1f6bf`, which contains the
remediation (`git merge-base --is-ancestor 22d18d72 52f1f6bf` exits 0), into the plain-retirement branch
at `87fc7141`, which had branched before it (`… 22d18d72 87fc7141` exits 1); `main` was then
fast-forwarded to the result. The plain retirement's close-out describes the merge's conflict resolution
and its stack-path repair with passing tests (`doc/PLAN-retire-mam-parsed-plain.md:42–53`) and mentions
neither the notice order nor the blind-dive update's lost corrections; of that update it says only that
the resolution "combined the two independently added finished-document dispositions" (`:45–46`).

1.1. **The consumer notice again uses "narpas" before defining it, in all 24 MAM-parsed plus files and
the published format guide.** The remediation (2026-09-26 finding 24.5, `22d18d72`) put `NARPAS_GROUPING_RULE`
before `MAM_PARSED_WHITESPACE_TEMPLATE_RULE`; at `7549ebf7`
`py/mb_cmn/public_data_consumer_notice.py:79–80` lists the whitespace rule first again, so
`MAM-parsed/plus/A1-Genesis.json:18` ends "This rule does not apply to narpas, whose missing literal
whitespace prescribes no display spacing." and only `:19` opens "Narpas (narrow-sense paseq, ׀) forms
no compound of any kind", and `gh-pages/MAM-parsed/plus/html/mpplus.html:39–40` the same. `git diff
52f1f6bf ebbfa90f -- py/mb_cmn/public_data_consumer_notice.py` shows the line moving; `git show --cc
ebbfa90f` prints no hunk for the module, the JSON or the page, because the resolution took the first
parent's lines (`F_sub1_notice_order.py` traces the order across ten commits; `V5_03_merge_sim.py` shows a
plain three-way merge conflicting in exactly that region). At `f4d81285` the order was the same, 2026-09-26
finding 24.5's original defect; the window's content here is the lost fix and the close-out record's row 24 ("narpas
first-use glosses", `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md:560`), true when
`22d18d72` wrote it and false at `7549ebf7`. Tier: distributed data (`MAM-parsed/`) and the published
site.

1.2. **`py/main_tmpl_survey.py --find-stack-path` crashes on every lookup.** The merge wrote
`py/tmpl_survey/stack_path_lookup.py:75`, `folder = str(paths.mam_parsed_dir() / "plus")`, into
`_dataset_file_paths`, whose line 76, `paths = []`, already bound a local `paths` in both parents, where
it was harmless; now the local name shadows the module at line 75. Ruff reports F823 at `:75`, and both
`--find-stack-path` and `--find-stack-path-verbose` raise `UnboundLocalError: cannot access local
variable 'paths' where it is not associated with a value`. This session reproduced it with
`py/main_tmpl_survey.py --find-stack-path "E/נוסח" --find-stack-path-limit 2`, stream E with
`E_f823_repro.py`, and verifier V2 with both flags. `git show --cc -p ebbfa90f` marks line 75 "++", in
neither parent; both parents and `f4d81285` call `_dataset_folder` there and are ruff-clean. The suite
misses it because `py/tests/test_stack_path_lookup.py:41` patches `_dataset_file_paths`, and the mega
does not run the lookup. Still described as working: `doc/blind-dive-into-template-params-update.md:85–92`,
`py/tests/test_mega_coverage.py:368–372` and `doc/PLAN-retire-mam-parsed-plain.md:49–53`. Tier: internal
(a hand-run lookup that writes nothing). A reproducible code defect.

1.3. **The blind-dive update lost two of `87fc7141`'s corrections.**
`doc/blind-dive-into-template-params-update.md:63–64` says "The survey and documentation-verification
paths named beside them remain current." of the plain survey paths that the same file's last section
(lines 138–149) calls retired; `87fc7141` had changed it to "remained current at that checkpoint.".
Lines 42–43 still name `py/mb_cmn/plain_template_schema.py:validate_current_plain_template` and
`_CURRENT_PLAIN_NAMED_ARGUMENT_IDENTITIES`, which `87fc7141` had corrected and neither of which exists at
`7549ebf7`. `main`'s side changed neither passage (`git diff 85cb7acd 52f1f6bf --
doc/blind-dive-into-template-params-update.md` only appends after line 64, `85cb7acd` being the merge
base), yet the resolution kept `52f1f6bf`'s text at both places, which `git show --cc -p` cannot show
because the result equals that parent there (`R_09`). Tier: internal.

### 2. The close-out record calls fixed six items whose approved changes did not land, or landed at only some of their sites

**Unfixed at `7549ebf7`.** Stream F, with its sub-agent F_sub2 for 2.1, 2.2 and 2.5. The close-out
record is `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`, and the remediation plan
`doc/PLAN-remediate-review-findings-2026-09-26.md`; the record's execution table (lines 537–572) marks
each of these findings fixed.

2.1. **2026-09-26 finding 3.1 (row 3, "Fixed: surviving reader/procedure links reach verified archive
families"):** the remediation plan (lines 215–220) prescribes a pinned link for
`in/mam-ws-intro/README.md` and "Use that same complete-family historical commit at the surviving
topology reference, `py/repo_scopes.py` and `py/subcommands/download_wikisource_intro.py`." Only the
topology reference changed: `in/mam-ws-intro/README.md:48–49`, `py/repo_scopes.py:29–30` and
`py/subcommands/download_wikisource_intro.py:33–34` still say "Phase 3 of `doc/PLAN-mega-coverage.md`
records the totals", and that file is absent at `7549ebf7` (`git cat-file -e
7549ebf7:doc/PLAN-mega-coverage.md` fails; the sites: `git grep -n -F "Phase 3 of" 7549ebf7 --
in/mam-ws-intro/README.md py/repo_scopes.py py/subcommands/download_wikisource_intro.py`). The README is
reader-facing.

2.2. **2026-09-26 finding 6 (row 6, "Fixed"):** three of that turn 01's named sites survive:
`py/ac_paths.py:23–25` ("which phase 3 of ``doc/PLAN-mega-coverage.md`` records"), and the live
September 9 plan, `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md`, at lines
471–475 (citations of `review-findings-2026-07-29.md` and `review-findings-2026-09-08.md` that "resolve")
and 596–597 ("`doc/review-findings-2026-09-08.md` is headed "review / of the public repos""). `2a051ba5`
deleted all three documents; the remediation plan (line 759) said "For findings 5, 6 and 10, use the
finite passages enumerated in turn 01".

2.3. **2026-09-26 finding 29.3 (row 29, "Fixed: … root styles"):** that turn 01 named two docstrings; `22d18d72`
corrected `py/author_site/site_data.py` and left `py/author_site/post_stress_meteg.py:16–17`,
"``gh-pages/style.css`` is the / deploy-root stylesheet, whose whole job is the light/dark switching;",
while adding a `.book-title` rule to that stylesheet (`gh-pages/style.css:1`).

2.4. **2026-09-26 finding 30 (row 30, "approved page locators"):** `doc/meteg-after-silluq-snips/README.md:119–120`
still reads "identifies the page as folio **57a**" and `:366–368` "recorded as folio / **307b**",
beside `:289` "page **303a**", `:452` "page **308b**" and `:554` "page **348b**". The remediation plan
substitutes "folio 57a" with "page 57a" (line 194) and applies its substitutions in this README (lines
168–171), but its list of "three additional side-lettered EVR identifiers" (lines 182–186) omits 307b. Ben's words
(close-out record lines 99–100): "One more note regarding phrases like "folio 57a". I think we should avoid
them".

2.5. **2026-09-26 finding 11.2 (row 11, "Fixed"):** that turn 01 named two lines of the common body that
address every reader, `dot-Codex/user-wide-AGENTS.md:82` ("Load `codex-worktree-tasks` and follow the") and `:292`
("as `codex-worktree-tasks` specifies"); the skill deploys only to `~/.agents/skills/`. Of the body's
routings to the skill, `22d18d72` changed only the sentence already addressed to Codex (now `:168`,
"ChatGPT-Codex loads `codex-worktree-tasks`"), while restoring the shared safeguards above it, and wrote a
third every-reader routing into the live September 9 plan
(`doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md:77–78`, "Load `codex-worktree-tasks`
for a linked / worktree's verification and integration procedure."). The remediation plan (lines
651–652): "Make skill routing agent-specific". Whether its sentence reached the two lines is a reading of
the remediation plan.

2.6. **2026-09-26 finding 5 (row 5, "Fixed"):** see this file's finding 4, items 4.2 and 4.3.

Tier: reader-facing Markdown (2.1's README) and internal.

### 3. The Evr. II B 55 README gained a heading that names the wrong books and kept a sentence the remediation made false

**Unfixed at `7549ebf7`.** Streams F and K independently for 3.1; stream K for 3.2.

3.1. `evr-ii-b-55/README.md:523`, "### Segmentation of Psalms, Job and Proverbs", heads a paragraph on
"the 4,827 verses that the catalog lists before 2 Chronicles 11" whose example is "a ketiv that is not
read, with its maqaf, in 2 Kings 5:18" (`:525–528`), under "## Reaching images 005–495" (`:384`), whose
images "presumably hold the Prophets and whatever of Chronicles comes before 2 Chronicles 11"
(`:386–387`). The wording is the plan's row (`doc/PLAN-remediate-review-findings-2026-09-26.md:297`,
"| 34.2, same README, Psalms/Job/Proverbs heading | "Segmentation of these books" | "Segmentation of
Psalms, Job and Proverbs". |"), which departs from the 2026-09-26 turn 01's 34.2 (its lines 2144–2145);
the baseline heading, "### Segmentation of these books", was vague but not false.

3.2. `evr-ii-b-55/README.md:343–344`: "They agree on all 17,358 verses but Psalms 10:5, where
`get_verse_words` drops an atom (item 6)."; item 6 (`:379–381`) now says "`get_verse_words` now reads
the child form of `<kq-trivial>` at Psalms 10:5, preserving the second atom and its legarmeh."
`22d18d72` changed the reader and item 6 and left item 3 (`K_02_mam_xml_verses_diff.txt`: 11 atoms at
`7549ebf7`, 10 before).

Introduced by `22d18d72`. Tier: reader-facing Markdown.

### 4. Records the remediation rewrote now misstate their sources, dates or their own contents

**Unfixed at `7549ebf7`.** Streams F (with F_sub2), A, R and K, as each item says.

4.1. **Two live update files still say the Google Sheet retirement "remains incomplete"; the
remediation rewrote that clause into `doc/review-findings-2026-09-14-update.md` a day after the Sheet
plan recorded the retirement complete** (streams A, R and F, independently). `doc/PLAN-retire-google-sheet.md:3–5` (`c450060e`, 2026-09-27 15:39): "State: executed
2026-09-27. Repository implementation, the frozen Google Sheet, the five Hebrew Wikisource
documentation edits, both live verifications, and the tracked introduction-mirror refresh are
complete." Against it, `doc/PLAN-remediate-review-findings-2026-09-14-update.md:50–52`, the 2026-09-27
entry `a41fbcdd` wrote at 09:40, true then: "The overall retirement / remains incomplete until Ben
applies and reports the manual frozen-Sheet and Hebrew / Wikisource documentation edits and both live
results are verified as that plan requires." (`22d18d72` edited this file's 2026-09-18 entry in place
and left this one); and `doc/review-findings-2026-09-14-update.md:100–104`, item 10, rewritten by
`22d18d72` (2026-09-28 10:34), of which `c450060e` is an ancestor: "The overall retirement remains
incomplete until Ben applies and reports / the manual frozen-Sheet and Hebrew Wikisource documentation
edits and the required live / results are verified." Both are `State: open` updates, whose stale
present-tense claims are corrected in place (`dot-claude/skills/iterative-document-editing/SKILL.md:58–59`),
and, for `doc/review-findings-2026-09-14-update.md`, row 2 of the remediation plan asked to "replace
stale pending/closing clauses in existing September 14/16 review updates" (`doc/PLAN-remediate-review-findings-2026-09-26.md:484`).

4.2. **`doc/review-findings-2026-09-10-update.md`'s inserted "[base] and [update]" pairs made three
passages false or self-contradictory.** (a) Lines 668–670 say the finished base, its update "and frozen
/ `doc/mam-products-phase6-command-map.md` each had one “hand-authored” occurrence"; at the named
checkpoint `d34afb44` the update has none, and line 677's "D12 left all three finished documents
unchanged." now follows four. (b) Lines 1035–1037: "D12 left the / finished
[PLAN-close-out-review-2026-09-08.md](…) and [PLAN-close-out-review-2026-09-08-update.md](…) unchanged;
its live sibling / [PLAN-close-out-review-2026-09-08-update.md](…) now records that Step 7 is complete".
(c) Lines 1395–1397 now name five documents, while `:1400–1405` still says "each assigned document has 4
lines containing `.novc`" over three blobs "respectively", and `:1412` "The 12 lines". At `93fe8704`
the three passages named bases only.

4.3. **The same update still presents retired or executed things as current.** Line 1206, "The tracked
review-differences receipt preserves the original nine changed fields"; close-out rows 1650 ("The
retired display fallback is recorded in the two sibling update files named in the 2026-09-11
disposition.") and 1653 ("the finished plans and validation receipt remain unchanged."); the command
map, named at `:669`, `:1396`, `:1416` and `:1417` without a link; and, from stream A, lines 1217–1219
("The direct tracked entry points remain", "the Google reader and comparator remain tracked") and 532–533
("The last three plans describe work / that is paused or live", two of them, the codex-index plan at
line 526 and the Google Sheet plan at line 527, executed on 2026-09-26 and 2026-09-27). `2a051ba5`
retired the receipt and the map before the window, and `a41fbcdd` deleted the Google reader and the
comparator and removed the `py/main_parse.py go` and `py/main_diff.py wsgo` commands. The remediation
rewrote lines 1218–1219 in place, changing only "tracked" to "archived", and rewrote lines 529–532,
putting the first six plans into the past tense, replacing "D12 leaves all six plans unchanged" with
"D12 preserved their bases" and adding "The six complete families were later retired by `2a051ba5` …";
it kept the stale claims in both places, and it added an archive list (`:1722–1729`) that omits the
receipt, while
the command map has no archive link anywhere in the file although line 1707 names its family as retired
(`V6_10_rewritten_lines.py`).

4.4. **`doc/user-wide-instruction-conversion-reconciliation.md` files two deferred clauses under the
wrong old sections.** Line 37 gives "Running scripts — no inline one-liners" as "Retained." and line 38
puts "exact-command harness override remains deferred (11.1)" on "Prefer the built-in tools"; the clause
("**Expect the harness to prescribe exactly what these bullets ban, and override it.**",
`71f96ca3:dot-claude/user-wide-CLAUDE.md:595`) sits under "## Running scripts — no inline one-liners".
Line 50 puts "bold-lead-ins clause remains deferred (11.1)" on "Prose: a heading NAMES ITS SUBJECT";
the clause (old line 1109) sits under "## Prose: if you announce a count, NUMBER the items — `1.`, `2.`,
`3.`". Line 26
says "shared-review backup exception preserved (11.5)", where the fix for 2026-09-26 finding 11.5
restored the general long-lived-branch paragraph (`dot-Codex/user-wide-AGENTS.md:102`). The close-out
record (row 13) says the file maps headings "from the old common body"; the mapped file is the old
Claude body.

4.5. **`dot-claude/skills/hebrew-prose/references/mam-basics.md:34–36` credits Ben's 2026-08-11
al-hatorah decision with eight sites:** "His 2026-08-11 al-hatorah decision / covered seven historical
accgram citations and one test site"; the decision's record (`73f8ea3c:CLAUDE.md:120–127`) names
"**Seven / sites**", six accgram sites and the test.

4.6. **`doc/PLAN-symmetric-CLAUDE-and-AGENTS-instructions-update.md:256` misquotes the passage it
locates:** "The base's Phase 1 step beginning “Set project_doc_max_bytes to 131072”"; the base reads
"Set `project_doc_max_bytes = 131072` in `C:/Users/BenDe/.codex/config.toml` …"
(`doc/PLAN-symmetric-CLAUDE-and-AGENTS-instructions.md:100`), under "### 4. Convert MAM-basics repository
instructions" (`:88`), and has no "Phase 1". This is the locator rule that the fix for 2026-09-26 finding
11.4 restored.

4.7. **`doc/dual-agent-review-2026-09-16-turn-01-claude-update.md:91–92` dates the plan's writing to
2026-09-18:** "The plan was subsequently written and executed on / 2026-09-18."; `49c7b1c9` added it on
2026-09-17 at 17:30.

4.8. **The remediation withdrew a claim from `doc/sigil-decoding.md:222` and left it in
`doc/meteg-after-silluq-job-4-12-update.md:84–86`** (stream R), "The NLI presents B 55 together with its direct
continuation, Evr. II B 247; they are separate shelfmarks, not former and current names.", which cites
`doc/sigil-decoding.md` at line 83 and whose next line `22d18d72` edited; the introduction
says "ולשעבר B 247", "formerly B 247" (`in/mam-ws-intro/appendices.mediawiki:78`), and the corrected row now
reads "The mirrored appendix calls B 55 formerly B 247 at line 78 …". The two documents agreed at
`f4d81285`.

4.9. **`evr-ii-b-55/evr-ii-b-55-images-provenance-update.md:7–10` says the six Evr. II B 55 crops'
"current paths and filename changes are recorded in" `doc/post-stress-meteg-image-provenance-update.md`,
whose table (lines 22–43) lists five** (stream K). The sixth, `st-petersburg-evr-ii-b-55-Ps60v10-HFRV33Y.png`,
kept its name and appears only in the finished base (`doc/post-stress-meteg-image-provenance.md:40`).

Introduced by `22d18d72`, except 4.1's first site (`a41fbcdd`, made false by `c450060e`) and 4.3:
`2a051ba5` made the receipt, map and close-out-row claims stale before the window, and `a41fbcdd`,
`02879b9c` and `c450060e` made lines 1217–1219 and 532–533 stale inside it; `22d18d72` left those claims,
rewrote lines 1218–1219 and 529–532 around them, and added the archive list. Tier: internal.

### 5. Documentation, docstrings, comments and one signature the remediation wrote or kept disagree with the code, the data or each other

**Unfixed at `7549ebf7`.** Streams F (with F_sub1 and F_sub2) and K.

5.1. `py/mb_diff_mpu/mpplus_structure.py:3–5`: "Every classified structural parameter is included so a
change inside a / ketiv/qere, qamats, dual-cantillation, or stress-helper alternative remains visible.";
`:12–14`, added by `22d18d72`, says the module "compares only the approved trivial-template qere and
deḥi / stress-helper role". Changing the unselected `א` of the first `מ:כפול` (Genesis 35:22) or `ס` of
the first `מ:קמץ` (Genesis 9:21) gives no diff from `mpplus_extract._diff_ep`
(`F_09_alt_visibility_recheck.py`, `V6_03_alt_visibility.py`). The sentence quoted from lines 3–5
predates the window; `22d18d72` edited the docstring and kept it.

5.2. `doc/mam-normal-mark-order.md:14–16`: "The code calls it "(our) standard mark order" and its
combining-class table "SBL2", / … so grep for **std mark order** and **SBL2**"; `22d18d72` rewrote the
last lines of the table's comment (`py/mb_cmn/uni_denorm.py:60–61`) and removed the table's only "SBL2"
label, while editing this document for 2026-09-26 finding 21 (`py/check_mark_order.py:4` still calls the order
"SBL2").

5.3. `py/author_site/site_data.py:96–98`, whose lines 96–97 `22d18d72` rewrote: "# Hrefs below include relative
paths within the deploy root and absolute URLs to / # published pages, including MAM-with-doc and other
repositories. / # py/tests/test_site_index_links.py resolves each one against gh-pages/." The lint
returns `None` for any other `://` URL (`py/tests/test_site_index_links.py:80–88`; its line 8, "External
destinations are not fetched").

5.4. `py/boj_paths.py:99–100`, "Twelve retained modules from book-of-job: eleven runnable entry points
and one / library.", against `:108–109`, "every one of them is / an entry point"; and `:187–188`, "now
has LF line endings like the other 700 / retained files", where 517 of the 701 files under
`gh-pages/book-of-job/` and `book-of-job/out/` are binary (`git ls-files --eol`: 184 `i/lf`, 517
`i/-text`).

5.5. `py/tests/test_mam_xml_verses.py:1` describes "a lint over the tree and a differential", and lines
6–18 list those two; the third test,
`test_reader_atom_content_matches_selected_source_nodes_over_the_full_corpus` (lines 144–165, with its
helper `_selected_parts` at 94–141), which `22d18d72` added, is described nowhere in it.

5.6. `focus_fade_img` keeps an `overlay_class` parameter (`py/py_html/my_html_for_img.py:105`) that its
only caller, `py/author_site/post_stress_meteg_post_silluq_images.py:482`, has not passed since
`22d18d72` dropped the caller's argument; the 2026-09-26 turn 01's 23.3 reported the same condition for
`annotated_img`, whose parameter `22d18d72` removed.

Introduced by `22d18d72`, except 5.1's quoted sentence, which it kept. Tier: internal.

### 6. Three of the remediation's test changes check less than they claim

**Unfixed at `7549ebf7`.** Streams F (with F_sub1) and E.

6.1. The broadened force-flag lint compares whole tokens (`py/tests/test_worktree_retirement_policy.py:72`,
`assert node.value not in ("--force", "-f", "-D"), (`; `:80–82` and `:90` likewise), so aggregated short
options pass it: `branch -df` and `-fd` pass and `worktree remove -ff` counts as not forced
(`F_sub1_policy_lint_probe.py`). The plan (lines 844–845) asked for detection "at every destructive Git
worktree/branch argument position". No module uses such spellings today.

6.2. The cluster lint added for 2026-09-26 finding 25.5 (`py/tests/test_mpplus_alternative_oracle.py:389–396`)
checks a mark only when a Hebrew letter precedes it, so it cannot see that finding's fifth case, a merkha after a
`gray-maqaf` span (`F_sub1_cluster_lint_probe.py` finds the other cases in three reports at `93fe8704`
and none in 2026-03-06). The current output is correct.

6.3. `22d18d72` rewrote `test_exact_relocation_citations_gate_and_survive_retirement` in
`py/repo_util/worktree_retirement_simulation_test.py` without its assertion that the reviewed plan's
`citation_review` fingerprint equals `_fingerprint` of the review payload
(`db152332:py/repo_util/worktree_retirement_simulation_test.py:568–570`, the same blob as at `f4d81285`);
the merge `2374ea30` kept the rewrite, and "fingerprint" appears nowhere in the simulation at `7549ebf7`.

Introduced by `22d18d72`. Tier: internal.

### 7. The narrowed retirement citation gate still stops every Windows worktree that has run the suite without `--basetemp`

**Unfixed at `7549ebf7`.** Stream F, with F_sub1.
`py/repo_util/worktree_retirement_inspection.py:313–316` treats a bare relative `.novc` root as generic
policy but keeps "actual child paths": a retained child `t` yields the reference `.novc/t`, and
`py/main_test.py:125–126` creates `.novc/t` on every Windows run without `--basetemp`. That reference
matches three lines of generic prose, `py/main_test.py:86`, `doc/windows-long-paths.md:107` and
`doc/dual-agent-review-2026-09-26-turn-01-claude.md:1242`, against the rule "Generic `.novc` policy prose
does not gate." (`dot-claude/skills/mam-repository-topology/references/repository-maintenance.md:108`).
`F_sub1_novc_t_gate2.py` runs the production `_citation_references` and `_reference_matches` for a
target whose `.novc` holds `t`: 3 matching lines among 128 candidate files. The code does what the plan
specified ("Include retained child directories/files", line 827); the baseline gated on 1,715 lines.
Introduced by `22d18d72`, which the merge `2374ea30` carried into the module `89ae4b85` had split out.
Whether a shared relative child path should gate is a policy choice. Tier: internal.

### 8. The close-out and remediation departed from their approved scope twice: editorial wording applied without the approval D7 requires, and a question the record assigned to the plan that nobody asked

**Unfixed at `7549ebf7`.** Stream F, with F_sub2.

8.1. `doc/public-data-consumer-hazards-2026-09-16-update.md:114–119` re-reads hazard 5 ("Read it as:
“A standalone XML element representing either / narrow-sense paseq or legarmeh had been treated as a
space-delimited chanted word.” …"); the plan's 34.4 (lines 801–807) lists four other edits and no
hazard-5 re-reading. The live September 9 plan gained "## Current execution boundary, corrected
2026-09-28" and rewritten procedures (§1 items 1, 2 and 4; §4 item 6, line 489; §5 steps 2–4 and 8),
where the remediation plan (line 781) says "For finding 12, update only surviving current section
locators." The close-out record says "The approval does not supply approval of unspecified editorial
wording" (lines 402–403). The hazard-5 wording agrees with the hebrew-prose checklist. The
September 9 plan's wording agreed with the deployment procedure when written, but since `7cf780e1` its
deployment location (`:75–76`, `:81–83`, `:521–523`) disagrees with the common body (finding 28.5), and
its routing line is finding 2.5.

8.2. The close-out record (lines 119–121, written by `73f1dfe1`): "The terminology has no standing home
in the repository's instructions or skills yet; whether to give it one is for the remediation plan to
ask." Neither the decision package (`572fa2ab`) nor the remediation plan (`5f2affeb`) asks it, and no
instruction or skill carries the page and folio terminology; Ben's statement survives only in the
close-out record (lines 93–102). Finding 2.4 is one consequence.

Introduced by `22d18d72` (8.1), and by `572fa2ab` and `5f2affeb` not asking what `73f1dfe1` assigned
(8.2). Tier: internal (process).

### 9. Two provenance records break the receipt rules: the remediation's two new update files lack a first-entry date, and the Evr. II B 55 base still carries in-place changes

**Unfixed at `7549ebf7`.** Streams R, F and K.

9.1. `doc/post-stress-meteg-image-provenance-update.md:3` and
`evr-ii-b-55/evr-ii-b-55-images-provenance-update.md:3` read `State: open; the finished base remains
tracked.`; the skill says "An update file uses `State: open` with its first-entry date"
(`dot-claude/skills/iterative-document-editing/SKILL.md:84–85`), and the other three update files
`22d18d72` created read "State: open, first entry 2026-09-28." (`R_13_state_forms.py`). Introduced by
`22d18d72`.

9.2. Four passages of `evr-ii-b-55/evr-ii-b-55-images-provenance.md` (`:9–13`, `:29`, `:37–38`,
`:142–143`) changed in place on 2026-09-28, for example "Ben reports on 2026-09-28 that the link belongs
to Avi's pCloud directory". The approved remediation plan says "For the dated image-provenance records,
put later facts in updates, not the finished base." and "Keep both provenance bases' original
State/header and add only their permitted update pointers." (`doc/PLAN-remediate-review-findings-2026-09-26.md:307–308`,
`:318–319`); `db152332` (08:50) is an ancestor of the plan's approval `93fe8704` and of `22d18d72`,
whose new update (`evr-ii-b-55/evr-ii-b-55-images-provenance-update.md:5–11`) corrects only "No image is
tracked in this repository" and neither holds nor records the four changes. `22d18d72` did not reconcile
them; they are `db152332`'s, written before the plan's rule reached its tree (neither `db152332` nor
`5f2affeb`, which wrote the rule, is an ancestor of the other). The record's own line 3 had already
recorded an in-place addition of 2026-09-26, before the window; the finished classification is the
plan's.

Tier: internal (9.2's record is linked from `evr-ii-b-55/README.md:38`).

### 10. `DATA-LICENSES.md` no longer describes the products it covers: its licence copy and its MAM-parsed row

**Unfixed at `7549ebf7`.** Streams A, W, B and D.

10.1. **The Google Sheet retirement rewrote the five product licence wrappers but not the copy in
`DATA-LICENSES.md`, which still calls them the same file** (streams A and W, independently).
`DATA-LICENSES.md:130–132`: "The statement is copied without change. The same file stands as
`LICENSE.md` in the landed `MAM-parsed/`, `MAM-simple/`, `MAM-with-doc/`, `MAM-for-Sefaria/`, and
`MAM-OSIS/` product directories." Its copy still opens (`:139–143`) "We here repeat, in English &
Hebrew, the licence & attribution information / from the MAM Google spreadsheet. / This information
applies equally to the data in this GitHub repository. / …". Each of the five product files, one blob,
now opens (`MAM-parsed/LICENSE.md:1–2`) "The statement below is preserved verbatim from the former MAM
Google spreadsheet, / which became a frozen historical archive on September 12, 2026." At `f4d81285`
all five equalled the copy byte for byte; at `7549ebf7` none does (the copy's five wrapper lines against
the files' two; the last 31 lines shared), and `DATA-LICENSES.md:134–135`, which glosses "the data in
this GitHub repository", now explains a phrase only its own copy contains (`A_02_license_compare.py`,
`W_04_license_copies.py`). The product files also dropped "This information applies equally to the data
in this GitHub repository." and the instruction to ignore "in this spreadsheet", while the statement they
preserve still says "as found in this spreadsheet"; whether each product's grant is still clear is item
36.1. Introduced by `a41fbcdd`, which rewrote the five wrappers and `DATA-LICENSES.md:129–131`,
re-wrapping line 131's "The same file stands as `LICENSE.md` …" without changing its claim; the plan
asked to change "its wrapper in `DATA-LICENSES.md` and the product licenses"
(`doc/PLAN-retire-google-sheet.md:201–202`).

10.2. **`DATA-LICENSES.md` still says `MAM-parsed/` holds plain JSON** (streams B and W, independently,
and streams A and D in passing). `DATA-LICENSES.md:82`: "| `MAM-parsed/` | MAM-parsed's plain and plus
JSON, historical release snapshots, documentation, license, and example program | …". `87fc7141` deleted
`MAM-parsed/plain/` and edited line 54 of the same table (its `out/tmpl-survey-plain/` entry) but not
line 82; Phase 4 of the plan names `DATA-LICENSES.md` (`doc/PLAN-retire-mam-parsed-plain.md:488–491`).
`README.md:25` and `MAM-parsed/README.md:3–5` name only plus.

Tier: distributed data (10.1's five product licences) and reader-facing Markdown. Reproducible text
defects.

### 11. The six new special-page tests are mostly scenarios over a stub, neither differential nor lint-shaped

**Unfixed at `7549ebf7`.** Stream A. Of the six ids `a41fbcdd` added in
`py/tests/test_wikisource_special_page_download.py`, one (`:131–132`) is lint-shaped: the literal
inventory against the tracked `ch2.mediawiki`. The other five run over a stub API the test builds
(`:11–97`): a synthetic round trip with reuse and force (`:135–190`), and hand-chosen fault injections
(`:193–259`: a page omitted from metadata, a convergence onto another page, a wrong size, two chapter
records swapped, "not json" written to the manifest); the round trip's test is named
`test_special_mirror_matches_complete_api_oracle_reuse_and_force`, but its oracle is the stub the test
builds. The common body's rule ("Tests are differential or lint-shaped",
`dot-Codex/user-wide-AGENTS.md:318`) allows an example-based test only when Ben asks (`:325–326`), and
`AGENTS.md`'s one declared exception (`AGENTS.md:233–234`) covers the `ws_bot` tests; no tracked record
shows Ben asked for these. The pattern predates the window: `py/tests/test_main_download_fr_wikisource.py`
had 14 example-based methods at `f4d81285`, and `a41fbcdd` extended one. The refuse-to-replace property
these tests guard has no regenerable artifact, which may favour declaring an exception; that is Ben's
choice. Tier: internal. Rule conformance, not a code defect: all six pass.

### 12. `AGENTS.md` and the downloader say the special-page inventory is checked against "the two tables"; the 36th title comes from the paragraph after the Decalogue table

**Unfixed at `7549ebf7`.** Stream A. `AGENTS.md:76–77`: "owns the literal inventory, / checks it
against the two tables in `in/mam-ws-intro/ch2.mediawiki`"; `py/ws/ws_special_page_download.py:5–7`,
"checked against the two source tables", and `:138`, "from chapter 2's two named tables". The code
(`:139–140`) slices `ch2.mediawiki:359–389`, from the section's heading to the next, not the marked
table at `:362–386`. The two tables yield 35 titles; the 36th, `עשרת הדברות/ניקוד`, is linked only at
`ch2.mediawiki:388`, after the table's end marker (`A_03_mirror_check.txt`, `V1_03_g6_tables.py`). A
reimplementation that read only the tables would drop a declared page. Introduced by `a41fbcdd`; the
wording follows the plan's own "parses the two named tables" (`doc/PLAN-retire-google-sheet.md:149–150`),
while its range, "around lines 361–388", takes in line 388. Tier: internal (the repository instructions
and the downloader's docstrings). Editorial: the description is inaccurate, the code right.

### 13. The introduction mirror's README and downloader cite "the committed manifest" for figures the manifest stopped supporting at `c450060e`

**Unfixed at `7549ebf7`.** Stream A. `in/mam-ws-intro/README.md:36–38`: "five of the thirteen pages
were / edited in August 2026 alone (the committed manifest's count; …)"; likewise
`py/subcommands/download_wikisource_intro.py:52–53` ("the manifest's count"). At `f4d81285` the manifest
had five 2026-08 timestamps and summed 1,852,837 bytes; since `c450060e`'s refresh it has one (`ch4`)
and sums 1,886,674 (`A_03`, `V1_04_g7_manifest.py`). The docstring's other figure (`:21`, "1,852,837 bytes
of wikitext, the committed manifest's sum") is introduced as the state "on 2026-08-31", so it is dated.
The text predates the window; the window changed the evidence it cites. Tier: reader-facing Markdown and
an internal docstring. Editorial: a stale evidence pointer.

### 14. The Google Sheet and plain retirements left a lint exclusion, an unused import, a dead constant, and comments that still name what they removed

**Unfixed at `7549ebf7`.** Streams A, B and E.

14.1. **A lint still excludes the retired `google/` and `plain/` trees.**
`py/tests/test_h_dot_below_nfc.py:281–287`, `_MAM_PARSED_EXCLUDE_DIR_PREFIXES = ("google/",
"historical/", "plain/", "plus/", "py-examples-out/")`, identical at `f4d81285`. `a41fbcdd` deleted
`MAM-parsed/google/` and edited this file (it dropped `_EXCLUDE_MAM_GO_FILES`) but kept `"google/"`;
`87fc7141` deleted `MAM-parsed/plain/` and left the file untouched. Neither tree has a tracked file,
and the lint enumerates `git ls-files`, so both entries now exclude nothing: dead configuration. The
Sheet plan asked that lints no longer expect Google outputs (`doc/PLAN-retire-google-sheet.md:119–120`).

14.2. **An unused import and a dead constant.** `py/verify_mp/verifiers_plus.py:14` still imports
`iter_template_objects`, whose one use in this module, inside `verify_mp_plus_diff_from_plain`,
`87fc7141` deleted; ruff reports F401 (clean at `87fc7141^` and at `f4d81285`). `JSON_BOOK39_SKEL_COMMON`
(`py/author_misc/mp_cmn_top_header_book39.py:13`) and its snippet
`py/author_misc/json_snippets/top_header_book39/book39_skel_common.json` are now unused; their one reader
was `py/author_misc/mpplain_body.py:216` at `f4d81285`, which `87fc7141` deleted.

14.3. **Comments and docstrings that describe plain as a current product:** `py/ws/ws_plain.py:1` ("into
the plain-product schema"), `:3`, `:24` ("the plain boundary rows"), `:59` ("not a plain-product row");
`py/py_misc/mam_parsed_plus.py:33–34` ("Current plain headers already match plus shape");
`py/hkq_cmn/mam_plus_verse_data.py:55` and `py/hkq_cmn/qere_projection.py:414` ("a plain-file concern");
`py/author_misc/mp_cmn_top_header_book39.py:2` ("mpplain/mpplus docs"); and
`py/author_misc/mp_cmn_examples_and_file_naming.py:12` ("JSON snippets shared by plain and plus
common-templates sections"). All nine predate the window; `87fc7141` made them false. In the last file it
dropped `JSON_KQ` and `JSON_DOCNOTE` below that file's line 12 and reworded the header at line 22, but
left line 12.
Phase 4 of the plain plan lists "current comments".

14.4. **Comments and docstrings that cite deleted files.** `py/hkq_cmn/qere_ending_search.py:28–29` and
`py/main_search_final_hiriq_verse_text.py:24–26` cite `read_books_from_mam_parsed_plain.py`'s sentinel by
module path; `a41fbcdd` deleted that module, whose only importer was the Google reader it also deleted.
The commit they also cite, `0314c6ef`, still shows the module, so the harm is a bare-path citation rather
than a lost reference. `py/ws/ws_bot_edit_sigil_b2_to_t451.py:38–40`, which `a41fbcdd` rewrote:
"doc/PLAN-replace-sigil-b2-with-t451.md is the fuller historical statement, / including the four classes
of non-sigil ב2 and the former chain through the / Google Sheet." That plan was deleted on 2026-08-29
(`f6173fe3`); the reference already dangled at `f4d81285`, and the rewrite kept it.
`py/tests/test_mega_coverage.py`, for one, cites retired documents by pinned URL; the same deleted plan is
also cited by bare path, from before the window, at `doc/sigil-decoding.md:540`,
`py/tests/test_ws_bot_sigil_b2_to_t451.py:19` and the receipt `py/ws/ws_bot_edit_history.md:155`.

Tier: internal. Dead configuration and code hygiene (14.1, 14.2); editorial (14.3, 14.4).

### 15. The raw-to-plus check that plus holds no parser-stage encoding inspects nothing

**Unfixed at `7549ebf7`.** Stream B. `py/verify_mp/parser_stage.py:203–210` recurses only through
`dict` and `list`, and line 236 passes it a plus verse row, which is always a tuple
(`py/py_misc/mam_parsed_plus.py:169`, `return new_cp, new_dp, new_ep`). Over Genesis's 1,533 rows it is
entered 1,533 times and descends into no column, and a row with an injected `{"stmpl": "x"}` passes
`validate_plus_conversion` (`B_05`; `B_04` P2). Introduced by `146f6145`. At `f4d81285` the property was
checked on the loaded plus JSON by `_assert_no_stmpl_in_plus_node` inside
`verify_mp_plus_diff_from_plain`, which `87fc7141` retired. After the write, parse-ws's own claim checks
reject such a node at the top of a C or E column (`py/verify_mp/verifiers_plus.py:107`, `:208`), and the
plus survey (`py/tmpl_survey/survey_plus.py:27–29`) rejects a nested one in the mega's tmpl-survey step
(`V2_04_post_write_guards.py`), so the no-encoding clause of the raw-to-plus validation, which the plain
retirement's close-out says runs before the write (`doc/PLAN-retire-mam-parsed-plain.md:86–89`), is
vacuous rather than the property unguarded. Tier: internal (validation of distributed data). A reproducible code defect.

### 16. The parser-stage grammar lock names a generator that no longer writes it, and no tracked command regenerates it

**Unfixed at `7549ebf7`.** Stream B. `py/verify_mp/expanded_stack_grammar_parser_stage.lock.json:2`:
`"This file was generated by MAM-basics/py/main_tmpl_survey.py."`; `py/main_tmpl_survey.py:80–85` writes
only the plus lock, its help (`:153–158`) names only that lock, and nothing else writes this one
(`py/verify_mp/parser_stage.py:17–19` names it and `:175–182` only reads it). A legitimate new raw
nesting from Wikisource would stop `parse-ws` with no command to regenerate the lock. Introduced by
`4d4385c3`, which renamed the lock with its bytes unchanged and removed the survey's writer and check for
it (`87fc7141` later removed the plain survey itself); at `f4d81285` the same line was true of
`py/tmpl_survey/expanded_stack_grammar_plain.lock.json`.
The lock equals the grammar inferred from current data (173 edges and 196 order pairs; `B_04`,
`V2_03_parser_stage.py`). Tier: internal.

### 17. The raw-to-plus check compares aliyah records and verse keys, not the D-column labels Phase 2 named

**Unfixed at `7549ebf7`.** Stream B. Removing a `סדר` parameter, changing its value, or dropping a
label that has only a `סדר` parameter from plus all pass `validate_plus_conversion` (`B_04` P5–P7, at
Genesis 8:1; `V2_03_parser_stage.py`), because the only D-column comparison in `validate_plus_conversion`
(`py/verify_mp/parser_stage.py:242–249`) is the mpasuq equality at line 249, and both collectors record
the aliyah parameter `עלייה` alone (`py/tmpl_survey/column_d_0_store_the_mpasuq_call.py:60`, `if "עלייה"
not in named_params:`; `py/tmpl_survey/column_d_0_store_the_mpasuq_call_plus.py:49–51`). Phase 2 required "the
D-column labels, coordinates, aliyah records, and their raw-to-plus correspondence checked directly"
(`doc/PLAN-retire-mam-parsed-plain.md:366–368`), and the plan's ledger (line 120) marks the retained
validation implemented. No verifier in `py/verify_mp/` compared plain's and plus's D labels at `f4d81285`
either, so this is not a regression. After the write, the removed parameter would fail `mp.plus.verse.d-col.semantics`
(`py/verify_mp/verifiers_plus.py:174–178`); the changed value and the dropped label fail no automated
check, though either would show as a tracked diff of the plus JSON. Introduced by `146f6145`. Tier:
internal. Whether "labels" meant more than coordinates is a reading of the plan.

### 18. The Cambridge 1753 README and line-break note misdescribe the retained data, and the note's recovery command fails for the editor it describes

**Unfixed at `7549ebf7`.** Stream K.

18.1. `cam1753/doc/cam1753-line-break-task.md:7–9`: "`git show f4d81285:<path>` recovers each retired
program." The note says the markers "were then added by hand in an interactive editor" (lines 84–85) and
gives no other pointer; the editor, `py/py_cam1753_loc/gen_line_break_editor.py` with
`py/main_cam1753_gen_line_break_editor.py`, is absent at `f4d81285` (`f2a9ead4` deleted both before the
window) and present at `4ac4f16a`. `65f5a1c6` dropped both pointers `f4d81285` had, the note's "`git show
4ac4f16a:py/py_cam1753_loc/gen_line_break_editor.py` recovers the editor"
(`f4d81285:cam1753/doc/cam1753-line-break-task.md:68`) and the README's (`f4d81285:cam1753/README.md:17`);
the Aleppo note (`aleppo/doc/aleppo-line-breaks.md:12–14`, corrected at line 121) keeps its pointer. The
note still links the codex-index plan, which names `f2a9ead4` as the deleting commit, so the editor stays
reachable: the defect is a false instruction, not a lost program.

18.2. `cam1753/README.md:4–5`, "Its line-break data begins in Psalms and continues through Job", and
`cam1753/doc/cam1753-line-break-task.md:26`, "from Ps 149:7 through the end of Job": the retained
`cam1753/cam1753-line-breaks/0085B.json` holds, after Job, Proverbs 1:1–30 and the first three of 1:31's
five atoms: 221 atoms with 81 line markers, ending with a `verse-fragment-end` label for Proverbs 1:31
(`K_14_cam1753_0085B_tail.txt`, `V3_01_kA.py`). Both sentences are `65f5a1c6`'s. The README's is new (at
`f4d81285` it said "The current work concerns Job"); the note's restates
`f4d81285:cam1753/doc/cam1753-line-break-task.md:35`, "Ps 149:7 through end of Job (page 0085B)", and
`22d18d72` removed the one text that had the coverage right, `f4d81285:cam1753/doc/reading-mam-simple.md:42`:
"Psalms, Job or Proverbs, the books the Cambridge 1753 streams cover".

Tier: reader-facing Markdown.

### 19. "No program in this repository makes crops now" is false

**Unfixed at `7549ebf7`.** Stream K. `doc/boj-image-crop-reproducibility.md:5`, added by `65f5a1c6`,
which also says the doc's principles "still govern any crop made in future".
`py/accgram/scan_page.py:76–86` (`render_page(..., crop=...)` writes `<stem>-crop.png`) and
`py/accgram/transcription_editor.py:108–112` (`crop_and_resize`) crop printed-edition scans; both exist
at both anchors. The sentence means the codex crop tools that `f2a9ead4`, before the window, and
`65f5a1c6` retired. Tier: internal.

### 20. The HBCE licence statements understate how the outputs change HBCE's forms

**Unfixed at `7549ebf7`.** Stream K. `hbce-psalms/README.md:37–39`: "the outputs change those forms
only by splitting them into chanted words and, in `out/research_queue.md`, by putting their marks in
MAM-normal order"; `DATA-LICENSES.md:99` says the same with "in the research queue".
`hbce-psalms/out/compare_ML.tsv:44` quotes HBCE's Leningrad form of Psalms 5:9 with U+05B9 ḥolam where
`hbce-psalms/in/transcriptions/ML_25010.xml` has U+05BA HOLAM HASER FOR VAV (`hbce_finalize`,
`py/hbce_psalms/compare.py:224–226`; the row's flags say `holam-haser-vav`). `K_15_hbce_changed_forms.py`
lists the 32 TEI `<w>` elements holding U+05BA and the one output row that quotes a converted form. The
outputs also print a paseq that HBCE's `<w>` holds after an inserted space, in 112 cells of the five
comparison TSVs (`V3_12_paseq_cells.txt`), which the receipt records; whether "splitting them into chanted
words" covers that is a reading. The receipt's comparison rules state the substitution
(`doc/hbce-psalms-vs-mam-2026-09-26.md:94–95`); the two licence statements, which describe the changes
CC BY 4.0 asks a reuser to indicate, do not. Introduced by `fc819f6b`. Tier: reader-facing Markdown (a
README and the licence file).

### 21. Two smaller defects in the HBCE comparison's outputs and receipt

**Unfixed at `7549ebf7`.** Stream K. Item 1 is in `hbce-psalms/out/`, which Ben's decision of 2026-09-26
froze ("I accept the frozen record.", recorded by `a3ca231e`), and item 2 in a dated receipt that Ben has
not reviewed (its line 3), so a correction would take an update entry rather than a rerun.

21.1. `hbce-psalms/out/compare_summary.txt:51` and `:76` both read "=== ML vs MAM (Leningrad) ===", for
the 170-verse range comparison and the 801-verse full one; `py/hbce_psalms/compare.py:713` writes the
heading without the range.

21.2. `doc/hbce-psalms-vs-mam-2026-09-26.md:6–7` says "Everything it cites is in `hbce-psalms/`,
`py/hbce_psalms/` and `py/main_hbce_psalms.py`"; the same receipt cites `MAM-simple/xml-vtrad-mam/Ps.xml`,
`MAM-parsed/plus/D1-Psalms.json`, `in/mam-ws-intro/`, `in/UXLC-39/Psalms.xml` (lines 87–90),
`in/meteg_after_silluq_cases.json` (101), `DATA-LICENSES.md` (80) and four `py/` files (287–293).

Introduced by `fc819f6b`. Tier: internal.

### 22. The post-stress-meteg survey does not wholly follow the refresh: its Phonetic MAM input lacks 2 Kings 22:1's new qamats variant

**Unfixed at `7549ebf7`.** Stream C. `97c4aff5` gave 2 Kings 22:1 a new note, `נוסח`, whose lemma
is a new call of the qamats template `מ:קמץ` (in `MAM-parsed/plus/BC-Kings.json:17030–17031`,
the pair `"ד": "מִבׇּֽצְקַֽת"` and `"ס": "מִבָּֽצְקַֽת"`); the plus survey counts 376 such calls in column E, 375 at
`f4d81285`
(`out/tmpl-survey-plus/plus.json:12421–12424`). The survey reads Phonetic MAM from MAM-private, which this
review does not read; its public product, phonetic-hbo's page `gh-pages/tnkh/BD-2Kings/22.html:68–69` at
that repository's `8da90513`, still has the one old reading, where the same shape at 1 Samuel 13:21 has
both (`gh-pages/tnkh/BA-1Samuel/13.html:1270–1273`). Of the 357 verses of `MAM-parsed/plus/` with a
qamats call, 2 Kings 22:1 is the only one whose page has no variant row (`C_11_phonetic_qamats.py`). The
survey's `"variant_rows": 309` for prose verses (`out/accgram/post-stress-meteg.json:322–324`) is the same
at both anchors, where the new call should make it 310; the mega at `7549ebf7` reproduced the committed
survey, so this forest's snapshot lacks the row. The survey's own currency check compares only U+05BD counts per
verse, and both forms hold two, so it cannot see this. Recorded in MAM-basics by `5caab189` "Refresh
post-stress meteg survey"; the cause lies in the dependent refresh outside this repository and is not
verifiable from public evidence. Tier: internal (the qamats-variant census appears on no published page;
the page figures are unaffected), and phonetic-hbo's published 2 Kings 22 page outside MAM-basics.

### 23. The refresh skill and the bot's setup guide say a bot run's post-run download fetches only chapters; since the Sheet retirement it also refetches all 36 special pages

**Unfixed at `7549ebf7`.** Stream C, with stream A.
`dot-claude/skills/mam-wikisource-refresh/SKILL.md:60–62`: "it force-downloads exactly the chapters it
saved into `in/mam-ws/` and `in/mam-ws-revisions.json`, then reparses those books"; `:66–67` makes the
first commit "the saved chapters' regenerated outputs with a new entry in `py/ws/ws_bot_edit_history.md`";
`py/ws/pywikibot-setup.md:55–57`: "it automatically downloads the modified chapters into `in/mam-ws`
and reparses affected books." `py/subcommands/ws_bot_real.py:270` calls
`download_wikisource.run(modified_book_plans, force_download=True)`, whose first act
(`py/subcommands/download_wikisource.py:27–34`) is the special-page download with that
`force_download`, which refetches every page (`py/ws/ws_special_page_download.py:460–470`). `86132514`
wrote the skill's section, and added `py/ws/pywikibot-setup.md:59–63` under that guide's 2026-05-02
sentence (`986a041d`), when the download fetched chapters only; `a41fbcdd`, on another branch, added the
special pages; the merge `85cb7acd` joined them, resolving by hand only the skill's description line.
Tier: internal. Editorial.

### 24. `MAM-parsed/historical/README.md` gives the six pre-migration snapshots two creation dates and overstates the guard's reach

**Unfixed at `7549ebf7`.** Stream D. The two date sentences (lines 24–26 and 36–37) and the guard
sentence (lines 78–79) are new in the window; the definition at lines 7–8 was already there in substance
at `f4d81285`.

24.1. Lines 7–8 define the term, "Each snapshot is an uncompressed ZIP archive named by the full hash of
its commit."; lines 24–26 say "The six pre-migration archives were written on 2026-09-10 by a program that
was never tracked."; lines 36–37 say "The snapshots had been made on 2026-09-06 for the six boundaries
that lived in MAM-parsed". Each date is true of a different object, the loose JSON of `8176e91d`
(2026-09-06) and the ZIPs of `32fa7da6` (2026-09-10), and the text never tells them apart. Introduced by
`04133265`.

24.2. Lines 78–79: "Every change-log run refuses, before comparing anything, a boundary of
`releases.json` that has no snapshot". An explicit `--old`/`--new` run is not guarded
(`py/subcommands/diff_mpplus.py:597–605`), as `0ba7498b`'s message says ("Explicit --old/--new
MAM-basics refs and legacy:<ref> are unchanged"), and it can write a named release's page
(`default_output_path`, `:184–191`); `D_07_guard_checks.txt` line 14 shows one reach `generate_report`
without refusal. `diff_mpplus.py:49–51` states the exact scope. Introduced by `0ba7498b`.

Tier: reader-facing Markdown inside the distributed `MAM-parsed/`.

### 25. `doc/clone-forests.md` says every Git and Python subprocess is time-bounded; nine call sites in the two forest modules launch Git with no timeout

**Unfixed at `7549ebf7`.** Stream G. `doc/clone-forests.md:66`: "Git and Python subprocesses have
bounded execution time and noninteractive settings." Six direct calls go through
`user_config_sync._run_git`, whose `timeout_seconds` defaults to `None`
(`py/repo_util/user_config_sync.py:208`, `:220`): `py/repo_util/forest_sync.py:93`, `:139`, `:144`,
`:161` and `py/repo_util/forest_environments.py:153`, `:180`. Three inspection helpers,
`_status_entries`, `_operation_markers` and `_list_worktrees`, launch Git through
`worktree_retirement_git._git` (`py/repo_util/worktree_retirement_git.py:31–42`), with no timeout and no
`GIT_TERMINAL_PROMPT`. Only `forest_sync._git` (60 s), `clone` (600 s) and `_run_python` (300 s) are
bounded (`V4_03_forest_bounds.py`: 30 process-launching calls in `forest_sync.py` and
`forest_environments.py`, nine of them unbounded; `G_forest_timeouts.py`'s 33 lines also include the
helpers' and wrappers' own lines). Introduced by `7cf780e1` (the sentence and both modules). The unbounded commands are local, so the practical risk is low; the absolute is false. Tier:
internal.

### 26. The forest write form fetches into every existing full clone with a matching origin before judging the rest of its eligibility, so dirty, off-`main`, mid-operation, ahead or occupied clones are not "untouched"

**Unfixed at `7549ebf7`.** Stream G. `doc/clone-forests.md:37`, "Ineligible clones and their
environments stay untouched", after "Eligible clones are fetched and fast-forwarded." (`:36–37`); `py/repo_util/forest_sync.py:5–6`, "Dirty, diverged, active or otherwise
ineligible clones stay untouched."; `py/main_repo_util.py:44`, "Ineligible repositories are reported
unchanged". The code refuses a target that is not an independent full clone, or whose origin differs,
before any fetch (`forest_sync.py:194–196`), but for every other target (`:197–199`) it runs `_snapshot`,
`_runtime` and then `_fetch_main`, which fetches `origin refs/heads/main` (objects and `FETCH_HEAD`, `:149–158`) and
updates `refs/remotes/origin/main` (`:168–170`); eligibility is computed afterwards (`:214–224`), and the
refusal message says only "checkout and environments left untouched" (`:232`). So a clone another
session is using, or one mid-rebase, still takes a fetch and a guarded tracking-ref update. Introduced
by `7cf780e1`. Tier: internal.

### 27. The root README installs without `constraints.txt`, which the forest work made the rule

**Unfixed at `7549ebf7`.** Streams G and W, independently. `README.md:71–74`: `python -m venv .venv` and
`.venv/Scripts/pip.exe install -r requirements.txt`. `7cf780e1` added `constraints.txt` and changed both
setup scripts (`misc/requirements-venv-setup-windows.ps1:58`, `misc/requirements-venv-setup-linux.txt:4`)
to install with `-c constraints.txt`, and `doc/clone-forests.md:63` says environments are "installed with
`-r requirements.txt -c constraints.txt`"; the forest check rejects any installed version that differs
from its pin (`py/repo_util/forest_environments.py:141–143`), so an environment built from the README
can fail it. The README's setup section is unchanged since before `f4d81285`, when it agreed with both
scripts; the plan's list of setup sites to change did not name it
(`doc/PLAN-checkout-kinds-and-portable-knowledge.md:330–332`). Tier: reader-facing Markdown.

### 28. Live texts still pin commands to the primary forest or restrict them to "the primary clone", against the forest rules the window adopted

**Unfixed at `7549ebf7`.** Streams C, F, G, R, S and W. `7cf780e1` made every full clone self-contained and
no forest globally primary (`dot-Codex/user-wide-AGENTS.md:115`, "No machine or forest is globally
primary."; `:118`, "Every full clone has its own Python environments."; `:15`, deploy "from any full
MAM-basics clone") and rewrote several homes accordingly. These did not follow:

28.1. `dot-claude/skills/mam-wikisource-refresh/SKILL.md:15–17`, "Use
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` as the interpreter, even when the
development checkout is a linked worktree.", with `:32` and `:46`, against the skill's own
`references/dependent-refresh.md:14–16`, which `7cf780e1` rewrote to "Use the interpreter belonging to
each full clone, or a worktree's home clone." (stream C).

28.2. `dot-claude/skills/hebrew-prose/references/verifying.md:102–106`: "Tests run from the verified
repository root with the home clone's interpreter, following `AGENTS.md`, “Running tests”, and the
worktree runtime reference:" over the command
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py`. `0e254fdc` replaced the
relative `.venv/Scripts/python.exe py/main_test.py` with that absolute path, which then matched
`AGENTS.md`'s command; `7cf780e1` rewrote `AGENTS.md`'s command to `./.venv/Scripts/python.exe
py/main_test.py` for a full clone (`AGENTS.md:207–211`) and edited the same file's lines 18–19, and left
this block, which the file's own lines 223–225 say `AGENTS.md`, “Running tests”, and
`codex-worktree-tasks/references/worktree-runtime.md` own; that reference gives only a
`C:/absolute/home-clone/` placeholder (`:39`) and calls `AGENTS.md`'s section "the authority" (`:52–53`)
(streams G and S, and G's sub-agent).

28.3. Five clone commands and one working directory in changed skill files, unchanged since before the
window, name the primary forest:
`dot-claude/skills/mam-repository-topology/references/evacuated-repositories.md:61`, `:106`, `:136`,
`:201` and `:221` (`git clone --depth 1 https://github.com/bdenckla/<repo>.git
C:/Users/BenDe/GitRepos/<repo>`, the form line 58 presents for wlc-utils as the command
`py/main_redirect_stubs.py` "raises with"), and `dot-claude/skills/hebrew-prose/references/verifying.md:112–115`
(the masorah-books working directory under `C:/Users/BenDe/GitRepos/`). For the five, `source_pages_dir`
raises with `paths.sibling_repo(...)` (`py/redirect_stubs/stubs.py:487`, `:496`), the path beside the
invoking checkout's home clone, so a session in `GitRepos2` that follows the skill clones where the
program does not look; a session following the sixth would work in another forest's MAM-private clone.
`7cf780e1` declared `clone_forests` and edited both files (`evacuated-repositories.md:23–25`,
`verifying.md:18–19`) without converting these lines (stream S, confirming G's sub-agent).

28.4. `doc/PLAN-repo-maintenance-across-GitRepos.md`, a runbook: `:360–361`, "Run everything from
`C:/Users/BenDe/GitRepos/MAM-basics` with `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.";
`:375`, `--sync-user-config` "run only from the primary MAM-basics clone"; `:415` (from `0e254fdc`),
"from the primary MAM-basics root"; and its action table (`:366–377`) has no row for `--sync-forest` or
`--forest-status`, which `7cf780e1` added to the same parser group. `7cf780e1` edited the runbook and
left these (stream G).

28.5. `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md:75`, live plan text `22d18d72`
wrote: deployment "runs only from the primary clone"; the same passage's lines 72–73 give a linked
worktree "the primary clone's interpreter `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`",
and lines 82–83 speak of "deployment from the primary clone and its read-only `--check`" (streams R and
F).

28.6. `hbce-psalms/README.md:62–65` runs `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`
"From the repository root" (`fc819f6b`; stream W).

Tier: internal (skills, a runbook, a plan) and reader-facing Markdown (28.6).

### 29. Both configuration READMEs call `--sync-user-config --check` "the read-only form"; it fetches

**Unfixed at `7549ebf7`.** Stream G. `dot-Codex/README.md:123`, "The read-only form reports `clean`,
`drift`, or `not installed` for every Claude and Codex"; `dot-claude/README.md:88`, "The read-only form
uses the same fresh source and reports …". `py/repo_util/user_config_sync.py:98` fetches `origin`
(`:151–158`) before the `if check:` branch (`:103`). The sentences and the fetch predate the window: at
`f4d81285` they were `dot-Codex/README.md:114` and `dot-claude/README.md:77`, `user_config_sync.py:97`
fetched before `if check:` at `:102`, and the common body agreed with the READMEs. `7cf780e1` replaced
the common body's "Its `--check` mode is read-only." with "Its `--check` mode fetches and compares
without changing live configuration." (`dot-Codex/user-wide-AGENTS.md:22–23`) and edited the command
block under each README sentence without aligning it; the runbook's row already says "fetches `origin`".
Each README says elsewhere that the check uses a fresh fetch, so the defect is the label. Tier: internal
(the configuration READMEs). Editorial.

### 30. The tracked records name an untracked `.novc/` file as the only list of the approved additions, and routine maintenance deletes `.novc/`

**Unfixed at `7549ebf7`.** Stream G. `doc/PLAN-checkout-kinds-and-portable-knowledge.md:46–47`: "The
approved proposal is
`C:/Users/BenDe/GitRepos/MAM-basics/.novc/PROPOSAL-memory-retirement-and-instruction-consolidation-2026-09-28.md`;",
and `:369–370`, "The full public triage and private dispositions remain in their approved proposal
files;"; `doc/memory-retirement-and-instruction-consolidation-2026-09-28.md:27–28`, "The approved public
additions P01–P26, N01–N08 and A01–A02 were reconciled against their named tracked destinations." The
plan's Workstream B records the approved scope, but its step 2 (`:401–402`) says to "Apply the approved
public additions ... at their named homes" without listing them, and no tracked file defines those labels
(`git grep -n -e "P01" -e "N01" 7549ebf7 -- doc dot-claude dot-Codex AGENTS.md` finds only the record's
own line 27 besides unrelated `MP01-*` ids and `N0131.md`). The file exists only in the primary forest's
checkout, untracked, and `py/main_repo_maintenance.py`'s step 1 wipes `.novc/` by default (`:135–145`,
`:218–219`); the step "cannot tell the difference" between a cache and a durable result, and its
docstring leaves it to whoever runs it to check first "that nothing in ``.novc/`` is the sole home of a
decision or a pending item" (`:23–32`). The reconciliation claim cannot be checked from tracked evidence,
and a default maintenance run in that clone deletes its only source unless that manual check catches it.
Introduced by `0e254fdc` and `c6962aa9`. Tier: internal.

### 31. A code comment and a docstring still cite retired auto-memory notes as their record

**Unfixed at `7549ebf7`.** Stream G. `py/repo_util/run_black.py:30–32`: "Ben's decision of 2026-08-31,
whose reasoning is recorded in this project's auto-memory as venv-roster-2026-08-31.md";
`py/accgram/lexical_validation.py:32`, in its module docstring: "(output-neutral today, but future-proof;
cf. memory parse-rate-not-a-goal)." Both lines predate the window; the approved retirement recorded at
`cb9ae042` deleted every legacy memory store
(`doc/memory-retirement-and-instruction-consolidation-2026-09-28-update.md:19–22`), and `0e254fdc`'s
migration gave a checker's acceptance rate a tracked home (`doc/agent-planning-principles.md:130–131`)
that the docstring does not cite; nothing tracked records the reasoning of `venv-roster-2026-08-31.md`.
Whether those two notes were among the 247 deleted files was not checked (the memory directories are out
of bounds). Tier: internal.

### 32. The rules say the scan archive is found through explicit account configuration; the code falls back to a tracked default that no machine is recorded as overriding

**Unfixed at `7549ebf7`.** Stream K. `dot-Codex/user-wide-AGENTS.md:131–133` (`7cf780e1`): "Inputs
outside every repository are user-level inputs reachable by every forest on that machine, discovered
through explicit account configuration such as `BOOK_SCANS_ROOT` or the user's pywikibot
configuration."; `doc/PLAN-checkout-kinds-and-portable-knowledge.md:170–172` likewise.
`py/mb_cmn/paths.py:133–136` returns `Path.home() / "OneDrive" / "Documents" / "ScansOfBooks"` when the
variable is unset. `f368a305`, which coined the name, stopped reading the old `WLC_SCANS_DIR` because
"neither the desktop nor Ben's laptop sets it", so both machines used the default before the rename;
`BOOK_SCANS_ROOT` is unset in this session and in this machine's User and Machine environment, and nothing
tracked records either machine setting it. No setup text (the README's Setup section,
`doc/clone-forests.md`, the two `misc/` scripts) names the variable; two procedure notes name it as an
override (`doc/edition-transcription-workflow.md:45`, `doc/scan-pages.md:183`). The code is `f368a305`'s
(it consolidated a default present at `f4d81285` in two places); the rule text is `7cf780e1`'s and
`6219f593`'s (the plan's variable name updated by `f368a305`). Which side should change is Ben's choice.
Tier: internal.

### 33. The common body's new fetch-and-merge rule for pushing `main` contradicts its own worktree-integration rule and the Codex worktree lifecycle

**Unfixed at `7549ebf7`.** Stream S, confirming stream G's sub-agent. The common body,
`dot-Codex/user-wide-AGENTS.md:123–126`: "Before pushing a full clone's `main`, fetch `origin`, merge
`origin/main` if it moved … If the push is refused because origin moved, repeat the fetch, merge and
affected checks in that full clone." Applied to a worktree's home clone, which is a full clone, that rule
puts a merge there, which the same body forbids at `:83–84` ("The worktree's home clone receives only a
verified fast-forward, then `main` is pushed.") and `:165–166`. The Codex worktree lifecycle,
`dot-Codex/skills/codex-worktree-tasks/references/task-lifecycle.md:53–58`, keeps the older rule: "3. In
the worktree's home clone, fast-forward `main` … If `main` moved, return to step 1 instead of creating a
second merge in the worktree's home clone. 4. Push `main` normally. The worktree's home clone receives
only the verified fast-forward." It has no fetch step and no branch for a refused push.
`doc/clone-forests.md:88–90` ("Ordinary work in any full clone …") and `in/repo_maintenance_policy.json:91`
("Ordinary full-clone work …") scope the rule to ordinary full-clone work; the common body's sentence does
not. The common body's rule is new in `7cf780e1`. The lifecycle's steps predate the window (`b8214d3c`),
and `7cf780e1` only renamed their "primary clone" to "the worktree's home clone". At `f4d81285` the common
body had no fetch-and-merge rule, and its line 63, "The primary clone receives only a verified
fast-forward", agreed with the lifecycle. Whether the common body's rule takes the ordinary-work scope, or
the lifecycle and the common body's `:83–84` and `:165–166` take a fetch step and a refused-push branch,
is Ben's choice. Tier: internal (the common body, which both agents load, and a Codex-only skill
reference).

### 34. Pointers that `0e254fdc` wrote or orphaned miss their target or contradict the text beside them

**Unfixed at `7549ebf7`.** Stream S, with stream G's sub-agent and stream R.

34.1. **"Manual document retirement".** Four citations name it as a section of `mam-repository-topology`
without naming the reference that holds it: `AGENTS.md:130`, `dot-Codex/user-wide-AGENTS.md:284`,
`dot-claude/skills/iterative-document-editing/SKILL.md:70` and `doc/dual-agent-review.md:170–171`.
`22d18d72` had added the first, second and fourth as "follow `mam-repository-topology`'s
`references/repository-maintenance.md`, "Manual document retirement""; `0e254fdc` rewrote those three
without the reference's name and added the third. The heading exists only at
`dot-claude/skills/mam-repository-topology/references/repository-maintenance.md:30`, and the skill's
routing (`SKILL.md:21–22`, "5. Read `references/repository-maintenance.md` for a maintenance sweep, Black
coverage, or retirement of selected linked worktrees, completed Codex task folders and disposable cache
data.") never names document retirement, though "a maintenance sweep" can be read to include it.

34.2. **`dot-claude/skills/github-issues/references/reading-and-writing.md:61–64`:** "Its `State:` line
carries open or closed. … `doc/dual-agent-review.md`, “Review filenames and State lines”, owns the review
State rule". The named owner (`doc/dual-agent-review.md:486–490`) says line 3 "records … what was true
when that review finished", that later turns use `State: completed <date>; review only`, and that later
remediation State belongs in the single live update file. At `f4d81285` the item cited the docstring
passage "THE `State:` LINE ON doc/review-findings-*.md" of `py/repo_util/check_repo_standards.py`, which
agreed with it; `0e254fdc` removed that passage and named `doc/dual-agent-review.md` the owner. The item
also says the checker "retains the dated rationale", whose surviving paragraph
(`py/repo_util/check_repo_standards.py:280–284`) still describes "the State line carrying the
open/closed state".

34.3. **`dot-claude/skills/hebrew-prose/references/verifying.md:93`:** "while this paragraph read "Never"
the skill contradicted the repo's own instruction file"; `0e254fdc` removed the quoted ban ("It read
"Never from a git worktree, only from that repo root"") from lines 55–58, so the file no longer shows
what read "Never"; line 57, which `0e254fdc` also wrote, names "The worktree ban withdrawn on
2026-09-09", so only the ban's wording is gone. Line 93 itself predates the window.

Introduced by `0e254fdc`. Tier: internal.

### 35. `a367f962`'s rewrite of D11 left the September 16 paragraph pointing at a "backup exception recorded above" that no longer exists

**Unfixed at `7549ebf7`.** Stream R. `doc/dual-agent-review.md:274–276` (from `fbaae3d0`): "The package
makes the shared review branch subject to the backup exception recorded above". At `f4d81285` D11 read
"The shared review branch is a long-lived branch under the user-level backup exception: push it to
`origin` after every commit"; at `7549ebf7` (lines 223–224) it reads "under the user-level
shared-remote-branch exception", and line 275 is the file's only "backup exception". The 2026-09-26
close-out record (`doc/dual-agent-review-2026-09-26-turn-01-claude-update.md:438–440`, written by
`5f2affeb` before `a367f962`) also cites the section by its old title, "The shared worktree"; it is now
"The shared origin branch" (line 173). Introduced by `a367f962`. Tier: internal (procedure).

### 36. Items raised for Ben's judgment that this review does not call defects

Each is a question only Ben can settle; none is a defect of the tree as its rules stand.

36.1. **The product licences' grant** (streams A and W). Since `a41fbcdd`, the five product `LICENSE.md`
files present the statement as a verbatim exhibit of the former Sheet and no longer say it "applies
equally to the data in this GitHub repository", while the statement still speaks of the material "as
found in this spreadsheet". `MAM-simple/README.md:89` states that MAM-simple is CC BY-SA 4.0; the READMEs
of MAM-parsed, MAM-for-Sefaria, MAM-OSIS and MAM-with-doc name no licence. Is each directory's grant still
clear? (With finding 10.1.)

36.2. **The hand-run products lag MAM-simple at two verses** (this session and stream C). The refresh
changed Judges 19:23 and 2 Kings 22:1 in MAM-simple; MAM-for-Sefaria and MAM-OSIS were not regenerated,
as their READMEs say they are "not kept continuously current" since Ben's decision of 2026-09-12:
MAM-for-Sefaria's rows for both verses and MAM-OSIS's `MAPM-24` files still carry the old words.
`AGENTS.md`, "What this repository's products are", still says such a change "requires rerunning every
affected hand-run generator" (`AGENTS.md:163–164`), and `py/product_scopes.py:51–53` that it "owes
rerunning every affected generator" (likewise `:36–37`). After the previous refresh, `61aa48ee`
(2026-09-18) did rerun them. Which rule stands?

36.3. **In-place rewrites of dated update entries** (stream R, with stream F). `22d18d72` edited twelve
pre-existing update files in place; four carry a dated entry saying what was corrected, and eight do not
(among them `doc/mega-timing-2026-09-11-update.md:26–31`, whose "## 2026-09-16" entry now carries the
2026-09-26 review's figures). The skill permits correcting "stale present-tense claims in place"; these
rewrites also correct claims that were false when written, which D12's reason, that "a reader cannot tell
how the writer could have known", seems to want marked.

36.4. **Decisions attributed to Ben without his words** (streams R and F). D11's heading
(`doc/dual-agent-review.md:173`) names a 2026-09-28 decision that no tracked text records or quotes, and
`a367f962`'s message is its subject line only; the remediation plan's execution-location amendment and
branch-deletion authorization (the remediation plan's lines 33–38; the close-out record's lines 508 and
515–516) are likewise attributed to Ben without his words, unlike every approval the close-out record
quotes.

36.5. **Privacy of published metadata** (stream G). `doc/PLAN-checkout-kinds-and-portable-knowledge.md:137–144`
lists the topics of six account-only memory entries, among them "where the Wikisource bot's credentials
live", and the tracked texts publish MAM-private metadata: private file paths and one heading, private
commit ids, subtree names, the size of MAM-private's `.novc`, and two `git check-ignore` probes. No
credential value or location, memory text or private file content appears (`G_privacy_scan.txt`).

36.6. **Tests of the new safety claims** (streams G and D). No tracked test covers `forest_sync.py`,
`forest_environments.py` or the retired-skill path of `user_config_sync.py`;
`doc/PLAN-checkout-kinds-and-portable-knowledge.md` chose manual probes and the two real builds (`:327`,
`:595–601`). Nothing now exercises the change-log freshness guard's failure path:
`py/tests/test_diff_mpplus_unpinned_latest.py:145–148` asserts only the clean case. Differential tests
would be within the rule; whether to add them is a policy choice.

36.7. **Filename transliterations** (streams W, F and R). The special-page mirror's stems use the
hand transliterations "taamim" (8 paths) and "haazinu" (3), 10 distinct paths in all, where
`AGENTS.md:28–29` says to convert a Hebrew filename component with `consensus_to_ascii` (which gives E3MY6
and HAZYNV); and four pre-rule romanized slugs (`…-Ps72v15-yevarkhenhu.png` twice, `…-Job4v12-menhu.png`
twice) stand beside converter slugs on the same pages, as the remediation plan chose to preserve them. Do
conventional English loanwords count as Hebrew filename components, and should the four be renamed?

36.8. **A surviving Sheet link on Wikisource** (stream A). The mirrored English Decalogue page,
`in/mam-ws-special/decalogue-en.mediawiki:3` (revision 2980688), still links the Sheet as "Technical Base
(Spreadsheet)". The Sheet plan names the pages it edited and does not mention this one; any change is an
outward-facing Wikisource edit.

36.9. **The executed Google Sheet plan's two comparison counts** (streams A and R). Its lines 26–29
report 8 differences and 5 auto-edits at `f4d81285`; its lines 189–194, from `bfab23cb`, which the merge
`85cb7acd` added to the plan after `c450060e` had executed it, report 25 and 25 at `86132514` and say that
an unexplained difference "is still a finding". The 17 later differences, from the refresh and the bot
run, were never reconciled; with the Sheet frozen, their substance is moot.

36.10. **An unreviewed `NOT_IN_MEGA` reason** (stream K). `py/tests/test_mega_coverage.py:471–475`, the
reason `py/main_hbce_psalms.py lint-receipt` stays out of the mega, still begins "Claude-written proposal,
not yet reviewed by Ben"; its facts hold. Since its inputs are frozen and it writes nothing, it could also
run in the suite.

36.11. **Validators and closed dispatch** (stream C). `check_mpplus`'s `_check_note_link_tmpl` and
`_check_doc_tmpl` check named templates and pass every other; closure comes from the parser-stage schema
that runs first. Should a validator itself dispatch over every recognized template? The rule names
parsers, renderers, generators, surveys, transformations and shared helpers.

36.12. **Two retirements' consumer-facing traces** (streams B and K). `MAM-parsed/README.md` gives
consumers who pin paths by Git URL no account of the plain retirement; only the ten static pages explain
it. `cam1753/cam1753-page-index.json:3` still names a deleted program in the present tense, which the
codex-index plan left because no retained JSON may change.

## Noticed outside the diff, not findings

Things the streams saw while understanding the diff that are older than the window, or found on GitHub.
Three of them the window carried forward, and the item says so for each. Issue #294 was closed at
15:51:49 on 2026-09-26, inside the window's span, with no comment from the closing account giving the
reason, which `dot-claude/skills/github-issues/references/state-changes.md:8–10` asks of every state
change; the actor is the `bdenckla` account, and the reason is readable only in the issue's one comment,
`skadish1`'s own, posted 41 minutes earlier (stream W's sub-agent). `py/main_repo_maintenance.py:38` still
says its step 3 fetches "in the primary MAM-basics clone", where it fetches in the invoking checkout's
home clone, and `doc/PLAN-mam-mega-pipeline-phase-13-and-remediation.md` is `State: live` though its line
12 says both forests were retired by 2026-09-04 and its required reading names the retired
`worktree-forest` skill (stream G). `py/repo_util/user_config_sync.py:274–277` writes the generated
fingerprint with Windows line endings, which the hook tolerates (stream G). `uxlc/doc/clc-design.md:611`
and `:905–906` and `py/clc/clc_dual_cant_oracle.py:161` put all 15 Decalogue tags on the §7.7 split's
subtracted sites, where §7.16's own breakdown puts four elsewhere (stream E; `e329557b` moved the oracle
comment verbatim). `py/main_diff.py:13`'s example names the primary forest's interpreter (stream D).
Three dead links are older than the window: `doc/metsudah-vs-ctr.md:3`,
`misc/what-is-mam/img/provenance-misc.md:6` and `book-of-job/doc/opening-html-files.md:8` (stream W).
The recursive HTML check of `gh-pages/MAM-with-doc` reports the same 36 orphan images, 2 unlinked pages
and 36 unexpected file types at both anchors (stream W). Skill files the window changed keep older
staleness: `dot-claude/skills/hebrew-prose/references/terminology.md:240–241`'s "Full list in
`SKILL.md`" and "Two extra notes" (`0e254fdc` rewrote line 240 and kept both) and its line 3's "quick
table in `SKILL.md`", and `dot-claude/skills/hebrew-prose/references/rendered-prose.md:61`'s cited
section, none of which `dot-claude/skills/hebrew-prose/SKILL.md` has;
`dot-claude/skills/hebrew-prose/references/verifying.md:66`'s "fourteen call sites" (there are 16);
`dot-claude/skills/mam-repository-topology/references/evacuated-repositories.md:195`'s "six-page"
manifest, which has four pages; seven citations of retired plans without pinned links; and
`dot-claude/skills/hebrew-prose/references/sources-and-corpora.md:16`'s "two bullets down" (stream G's
sub-agent and stream S). `py/mb_cmn/uni_norm_fragile.py:63–68` lists the marks of MAM-normal order
without U+05C9, and `py/author_site/unicode_proposals.py:17–18` says the root stylesheet serves two
pages, where the 16 post-stress-meteg pages use it too (stream F). `aleppo/doc/aleppo-line-breaks.md:56`
calls the Internet Archive item "CC0", while `DATA-LICENSES.md:91` makes no grant and defers to the
item's current terms (stream K; `65f5a1c6` reworded the sentence and kept the claim, which this review
did not check against the item page). The call-graph edge labels (`py/tmpl_survey/survey_dot.py:77–90`)
are cumulative, though `gh-pages/MAM-parsed/plus/html/mpplus-template-call-graphs.html:71` says each counts
the nesting's occurrences (stream B). Three he.wikisource links on MAM-with-doc `misc/` pages hold raw
Hebrew, where the other 894 hold no raw non-ASCII (893 percent-encoded, one an ASCII-only `oldid` URL;
stream C). `py/main_0_mega.py:54` comments out a long-gone program, `py/ws/ws_chapter_counts.py:3` still
mentions Google CSVs, and the pipeline graph keeps an `osis_split_mapm` node for a program deleted on
2026-03-10 (stream A). `doc/periodic-review.md` and `doc/dual-agent-review.md` cite `~/.claude/CLAUDE.md`
in three places for rules that now live in the common body (stream R).

## Open ends the window itself declares (not findings)

`doc/PLAN-checkout-kinds-and-portable-knowledge.md` is executed for its Workstreams A and B, and its
update is open: at `7549ebf7` Ben has approved Decision 6's rule, which `7549ebf7` adds to the common
body, while the update records its canonical implementation, push and deployment as "Active under that
approval" (`doc/PLAN-checkout-kinds-and-portable-knowledge-update.md:195`), and Decision 7 is deferred
pending Ben's choice. `doc/PLAN-mega-speedup.md`, `doc/PLAN-silluq-before-gaya-template.md`,
`doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md`,
`doc/PLAN-remediate-review-findings-2026-09-14.md`, `doc/PLAN-symmetric-CLAUDE-and-AGENTS-instructions.md`,
`doc/PLAN-overall-port-to-python.md`, `doc/PLAN-dispose-mega-pipeline-review-findings.md` and
`doc/PLAN-mam-mega-pipeline-phase-13-and-remediation.md` are `live`, and
`doc/PLAN-deferred-template-projection-decisions.md` is `paused`. The 2026-09-26 remediation plan is
executed, and that round's close-out record is open. From 2026-09-26 15:00 to 2026-09-29 11:30 no issue
was opened and eight were closed; earlier in the window's span, #234 was closed as not planned at
13:30:35 on 2026-09-26, with a dated reason comment. The memory retirement's two backups are retained,
untracked: the record names one, a gitignored directory in the primary forest's MAM-private checkout, and
does not say where the second is. MAM-for-Sefaria and MAM-OSIS were not regenerated after the refresh
(item 36.2). Every window commit that changed `gh-pages/` was deployed by 04:36:33 on 2026-09-29, when run
36543719607's deployment succeeded.

## What this review did not check

1. Anything in MAM-private: Phonetic MAM itself, so finding 22 rests on phonetic-hbo's public pages and
   the survey JSON; the memory retirement's private approval artifact and backups; MAM-private's own
   requirements and constraints.
2. The network: no external link was fetched. Apart from this session's fetches and pushes that the
   opening describes, the only network reads were stream C's one read-only Wikisource API query and
   read-only `gh` queries of MAM-basics issues and Pages runs; the HBCE site was not contacted.
3. The worktree-retirement simulation (34 tests), any retirement, and the forest synchronizer,
   `--forest-status` and `--sync-user-config --check`, each of which fetches or writes outside the
   review directory; the forest code was judged by reading.
4. The hand-run generators `py/main_mam4sef.py`, `py/main_mam_osis.py` and `py/main_hbce_psalms.py
   compare`, for the reasons the tree-health section gives, and `--pin`'s successful path, which writes
   tracked files.
5. The six 2026-09-26 turn files' findings, by this turn's boundary.
6. Browser rendering, among it the layout claims of `4cf101ca` and `103b2308`, and W3C conformance.
7. Manuscript and edition images: no reading was adjudicated.
8. The live Google Sheet and its frozen exports, which are untracked, and the live Wikisource
   documentation edits beyond the mirrored pages.
9. Codex's behaviour and cloud sessions; the post-anchor six-skill cloud installation (`4d3ebf66`) only as
   it explains the live hashes.
10. The legal adequacy of the licence statements (finding 20 and item 36.1).
11. Figures recorded at intermediate commits that would need another checkout, such as the suite counts at
    `2374ea30` and the plans' mega times.

## Inputs for the reconciliation with the Codex review

Anchors for comparison: MAM-basics `f4d81285..7549ebf7`. Each finding gives the file and line as of
`7549ebf7`, the words of the tree, what they contradict, the measurement and the introducing commit; most
also name the command or `.novc/review-2026-09-29/` script that re-establishes them, and the others give
the `path:line` and commit from which `git show` and `git log -S` re-establish them. Findings 1 to 8 are
stream F's, with its two sub-agents, and, for their parts, streams B, E, R, A and K as each lead says; 9
stream R's, with streams F and K; 10 to 14 streams A's, B's, W's, D's and E's; 15 to 17 stream B's; 18 to
21 and 32 stream K's; 22 and 23 stream C's, with stream A for 23; 24 stream D's; 25 to 27 and 29 to 31
stream G's, with stream W for 27; 28 streams C's, F's, G's, R's, S's and W's; 33 stream S's, confirming
stream G's sub-agent; 34 stream S's, with stream G's sub-agent and stream R; 35 stream R's; and 36
collects what streams A, B, C, D, F, G, K, R and W raised, with this session's measurement for 36.2. This
session re-ran the measurements behind the census, the tree-health section's suite, test-id, subtest and
mega figures, finding 1.2's crash and item 36.2's lag with its own commands and scripts (`census.py`,
`commits_files.py`, `test_counts.py`, `mega_steps.py`, `root_handrun_lag.py`), and adopted the others on
the streams' evidence and the pre-commit check's. The reconciliation section goes below this one, under
`## Reconciliation with the Codex review`, per `doc/dual-agent-review.md`.

## Reconciliation with the Codex review

Appended by Codex, Agent 2, on 2026-09-29, New York time. The counter-argument is
[turn 02](dual-agent-review-2026-09-29-turn-02-codex.md), written against this
file at `27999316` and the frozen window `f4d81285..7549ebf7`. No earlier text
was changed. Three read-only sub-agents checked the principal sources for
findings 1–35 and selected sources for item 36, and
Codex reconciled their reports and checked the material qualifications. C1–C6
name turn 02's counter-findings. "Confirmed" means the cited condition
survives review, not that its problem was fixed. "Qualified" states the
supported part and its limit; "unchecked" does not establish the claim.
Every accepted defect remains unfixed by this review. Later remediation and
State belong in this argument's single update file after close-out.

| Finding | Codex assessment | Unfixed work, limit or remaining decision |
|---|---|---|
| 1. Merge losses | **Confirmed.** Notice order, stack-path crash and lost update corrections reproduce. | Restore the lost changes in later remediation; this turn changes none. |
| 2. Close-out credits | **Confirmed, with scope qualification.** The cited credited changes are absent or partial; item 2.5's skill-routing scope needs the approved plan's reading. | Correct the later disposition record and complete only approved work. |
| 3. Evr. II B 55 README | **Confirmed.** The heading names the wrong books and the Psalms 10:5 exception is stale. | Correct the reader-facing record later. |
| 4. Remediation records | **Confirmed, qualified.** The inaccuracies reproduce; some cited passages or conditions existed before this window. | Correct present claims in their permitted live homes without attributing all errors to this window. |
| 5. Code and prose disagreement | **Confirmed.** Cited docstrings, comments and signature disagree with current code or data; item 5.6's parameter is unused rather than a demonstrated runtime failure. | Bring descriptions and signature into agreement. |
| 6. Test claims | **Confirmed as coverage gaps.** Current outputs pass, but three changed tests prove less than their prose says. | Strengthen claims or checks under the repository's test rule. |
| 7. Retirement citation gate | **Confirmed conditionally.** A Windows suite run's `.novc/t` child can make the gate fail; exact behavior depends on retaining that child. | Narrow the gate or define the intended cache treatment. |
| 8. Approved scope | **Confirmed.** The unapproved editorial wording and unasked plan question remain process discrepancies; the underlying hazard-5 wording is sound. | Close-out determines whether to retain the wording and where the question belongs. |
| 9. Receipt provenance | **Confirmed, qualified.** Two updates lack the required first-entry date; item 9.2's in-place base edits preceded the approved remediation plan. | Correct receipt handling without assigning those edits to the wrong commit. |
| 10. Licence and product account | **Confirmed as textual inconsistency.** `DATA-LICENSES.md` and the changed wrappers disagree with the product account. | Reader-facing wording needs later disposition; legal adequacy remains unchecked. |
| 11. Special-page tests | **Qualified (C2).** Four fault cases are selected scenarios; the all-36-page round trip has a possible differential oracle. | Decide whether that oracle satisfies the test rule before treating all five stub tests as prohibited. |
| 12. Two-table description | **Confirmed.** The Decalogue section slice includes a 36th link after its table. | Describe the actual inventory source. |
| 13. Introduction manifest | **Confirmed.** The current manifest does not support the README's five August timestamps. | Correct the reader-facing source claim. |
| 14. Retirement residue | **Qualified (C3).** Dead lint entries, import, constant and citations remain; several "plain-file concern" passages describe a true historical distinction. | Repair stale sites without rewriting accurate historical descriptions. |
| 15. Parser-stage encoding check | **Confirmed.** The dict/list-only walker misses tuple rows in this call path. | Make the check inspect the actual plus representation. |
| 16. Grammar lock provenance | **Confirmed.** The lock names a generator that writes only the plus lock. | Record or implement a real parser-stage lock regeneration path. |
| 17. D-column labels | **Qualified (C4).** The validation compares aliyah or `mpasuq` records, not every label; the plan's intended meaning of "labels" is unresolved. | Decide the required projection before expanding the check. |
| 18. Cambridge 1753 records | **Confirmed on cited contradictions.** The recovery command and retained Proverbs evidence disagree with the README and note; the 221-atom count was not rerun here. | Correct reader-facing instructions and inventory. |
| 19. Crop-program absolute | **Confirmed.** Retained `accgram` code still makes crops. | Qualify the absolute claim. |
| 20. HBCE licence description | **Confirmed as a code/text discrepancy.** The comparison also changes U+05BA to U+05B9; legal adequacy was not assessed. | Describe the transformation accurately. |
| 21. HBCE outputs and receipt | **Confirmed.** The repeated headings and receipt's overbroad claim reproduce. | A correction to the frozen output needs Ben's decision; correct the dated receipt through its update file. |
| 22. Survey lag | **Qualified (C4).** Public artifacts show a specific 2 Kings 22:1 lag after a refresh attempt; the private input and an exact expected replacement count are unchecked. | Decide whether and how to refresh the snapshot before changing the survey. |
| 23. Bot refresh guidance | **Qualified (C3).** The special-page side effect is omitted, but the cited guidance does not literally say "only chapters". | Document the effect of a post-run forced download. |
| 24. Release archive README | **Confirmed with guard-scope detail (C4).** The two dates refer to different objects; explicit and no-argument runs do not perform the same boundary census as `--all`. | State chronology and each guard path precisely. |
| 25. Forest timeouts | **Confirmed.** The universal timeout claim exceeds the Git call sites' behavior. | Bound those calls or narrow the claim. |
| 26. Forest fetch before eligibility | **Confirmed, qualified.** Ineligible clones can have remote-tracking refs updated before eligibility is decided, while checkout and environment files remain untouched. | Define and describe the intended meaning of "untouched". |
| 27. Root setup command | **Confirmed.** The README omits the newly required constraints file. | Align the command with environment policy. |
| 28. Forest-specific paths | **Confirmed overall.** Cited live commands remain pinned to the primary forest; item 28.4 is an incomplete action table, and historical examples need not be rewritten. | Make live commands checkout-neutral. |
| 29. Read-only label | **Qualified (C5).** The READMEs disclose the fetch; "read-only" is ambiguous about local Git metadata, not a hidden operation. | Sharpen wording if the intended scope includes every local write. |
| 30. Untracked proposal | **Qualified (C5).** Tracked records lack the labeled additions and maintenance can delete `.novc/`; the file's present contents and uniqueness are unverified. | Preserve a checkable approval record before relying on those labels. |
| 31. Auto-memory citations | **Qualified (C5).** A live comment and docstring still cite retired memory names, but the deleted store was not inspected. | Repoint supported claims to tracked evidence. |
| 32. Scan-root configuration | **Qualified (C5).** The tracked explicit-configuration rule conflicts with the tracked default path; account settings were not verified from public evidence. | Ben decides which behavior the rule should describe. |
| 33. Full-clone push rule | **Confirmed as a scope ambiguity (C5).** The specific worktree fast-forward rule can resolve a run, but the general full-clone wording does not state that exception. | Clarify where a merge belongs when `origin/main` moves. |
| 34. Skill pointers | **Qualified (C5).** The retirement section exists but its reference is omitted; the review-State shorthand is wrong; the removed historical quotation is a weaker navigation gap. | Repair the false shorthand and make the intended reference explicit. |
| 35. D11 backup pointer | **Confirmed.** "Backup exception recorded above" no longer names the current shared-branch exception. | Correct the live procedure; preserve historical receipt wording as historical. |
| 36. Ben's questions | **Retained as questions, not defects (C6).** Item 36.2 is a verified conflict between the hand-run-generator rule and the products' allowed lag; the other subitems were not all rechecked. | Ben settles policy, legal clarity and editorial choices at close-out; this turn approves none. |

**Additional omission C1:** the new special-page downloader promises a whole-mirror atomic
replacement, but implements per-file atomic replacements followed by the manifest. This is
an unfixed docstring overclaim, not a failure of the approved validation and write order.
