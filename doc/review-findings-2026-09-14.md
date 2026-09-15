# Findings of the 2026-09-14 review of the public repos since 2026-09-10

State: not yet acted on

Written 2026-09-14, from about 07:45 to 08:44 local, as the Claude argument, turn 1 of
the standard alternating dual-agent review under `doc/dual-agent-review.md` (Ben's decision D9 of
2026-09-09): this file was frozen before any Codex reviewer read it, and the Claude session neither
read nor sought a Codex half (no file named `codex-review-findings-2026-09-14*` exists, and nothing
under `~/.codex/` or `Documents/Codex/` was read beyond directory listings). Nothing was fixed. The
round's shared worktree is the one D11 names,
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14` on branch
`dual-agent-review-2026-09-14`, created by this session at the round's start from `main` at
`bca64824`; every later turn of both agents and the close-out use it directly, no task
fast-forwards `main` or pushes before the final remediation wave, and the worktree and branch are
retired after the final task ends. A second, detached scratch worktree,
`.claude/worktrees/review-2026-09-14-mega-scratch` at the same commit, held the mega run and the
two generator runs of the tree-health section, so that the shared worktree stayed byte-stable
while five agent streams read it; this session removed that scratch worktree, clean and holding
no branch, before this file was committed. The reconciliation goes at the end of this file under
`## Reconciliation with the Codex review` once the Codex counter-argument is stable, and the
dispositions under a later `## Dispositions after remediation` section, per that document.

**Ben's instruction for this window differs from the earlier windows' in one respect, and this
file is shaped by it.** Ben, 2026-09-14: "I have some areas of particular concern because I became
aware that some sessions doing work in this review window were set at merely 'high' effort level,
which may be fine for the work they were given, but is not my standard ('max' is) so it makes me
nervous." His message carried a list of four areas to read first: the fix batch pushed to `main`
on 2026-09-12 (`80f88f7c`, `6dfabceb`, `53696b30`, `3134f32b`, the third of which changes the
cloud-session hook); the mega-speedup session that trimmed MAM-simple and the mega; the README
session that edited `README.md` and `DATA-LICENSES.md`, removed `diffable-pointed-hebrew/` and
moved the page crops; and `py/product_scopes.py`. The four areas were read in full by this session
itself, and their answers come first, under "Ben's four areas of concern". The rest of the window
was read by five agent streams, as the 2026-09-10 review's was. The stream prompts were written by
this session and carried four wrong figures, which the streams corrected rather than repeated: a
commit written `eb8adf13` that is `eb9adf13`, an update-file line count of 1,641 that is 1,640,
"twelve" update files added in the window that are 22 with six rather than five about the
meteg-after-silluq work, and a "five largest new documents" list of which only one document is
among the five largest.

## Scope, anchors and census

Seventh review under the public-repos-only scope. It covers committed work from the 2026-09-10
review's anchor, `0354b6cc`, through the moment this review started, 2026-09-14 about 07:45 local,
when MAM-basics' HEAD was **`bca64824`** (2026-09-13 14:48, "Close out the 2026-09-10 public
review"), the primary clone's tree was clean and `origin/main` stood at the same commit. The tree
did not move under the review: `main` and `origin/main` were still at `bca64824` when this file
was committed.

Anchors (start → end) and counts, re-measurable with
`git -C C:/Users/BenDe/GitRepos/<repo> log <start>..<end> --oneline`, or with
`gh api "repos/bdenckla/<repo>/commits?since=2026-09-11T02:20:00Z"` for the repos read on GitHub:

| Repo | Range | Commits | Non-merge |
|---|---|---|---|
| MAM-basics | `0354b6cc..bca64824` | 203 | 176 |

That is **203 commits in one public repo**. Fifteen public repos were quiet: the two clones
phonetic-hbo (clean, `main` at `origin/main`, `10de7970`) and Taamey_D (clean, `3813499`), and on
GitHub MAM-simple, MAM-parsed, MAM-with-doc, MAM-for-Sefaria, MAM-OSIS, codex-index-aleppo,
codex-index-cam1753, codex-index-leningrad, diffable-pointed-hebrew, book-of-job,
holman-ketiv-qere, UXLC-utils and wlc-utils, each answering 0 to the `gh api` query above. Two
clones are private and fall to the private series: MAM-private and hbofonts, neither read.
github-misc has no clone here, and the series' one standing exception, its instruction-file
byte-compare, is spent as `doc/periodic-review.md` records.

The window changed **673 paths** between its endpoints — 43 added, 286 deleted, 265 modified, 79
that `git diff -M` pairs as renames — taking the tree from 4,935 to **4,692** tracked files, 1,088
to **1,051** `.py`, `gh-pages/` 1,859 to 1,859 files (579 HTML both times), `doc/*.md` 79 to
**112** (direct children of `doc/`), `doc/PLAN-*.md` 21 to **33**, and `doc/*-update.md` 0 to
**22**. Of the 79 rename pairs, 69 are the Hebrew-letter filenames `4e007289` migrated to ASCII (66
under `gh-pages/`, two under `misc/`, one under `in/`), seven are page crops `a8e4790e` moved into
`doc/meteg-after-silluq-snips/` and `doc/lam-2-3-akhla-snips/` (an eighth, which `f3a11572` added
inside the window, shows as an addition), one pairs `doc/ms-snips/README.md` with
`doc/lam-2-3-akhla-snips/README.md` at 53 per cent similarity, one is
`py/subcommands/diff_mpp.py` becoming `diff_mpplus.py`, and one pairs
`diffable-pointed-hebrew/short_unicode_name_overrides.json` with
`in/diffable-pointed-hebrew-short-name-overrides.json` at 65 per cent similarity. By top-level
directory: `MAM-simple/` 328 (274 deletions — `py-examples-out/` 104, `misc/` 53, `py-examples/`
43, and 74 `json-` and `xml-vtrad-bhs` and `-sef` files — taking that product from 383 to **109**
tracked files), `py/` 129, `gh-pages/` 93, `doc/` 63, `MAM-parsed/` 15, `in/` 9, `out/` 8,
`diffable-pointed-hebrew/` 7 (all deletions), `dot-claude/` 4, the root 3, `aleppo/`, `cam1753/`,
`dot-Codex/`, `leningrad/` and `misc/` 2 each, `.claude/`, `MAM-OSIS/`, `MAM-for-Sefaria/` and
`holman/` 1 each.

The window's substance is five things. 1. The 2026-09-10 review's exchange and close-out: turns 2
to 4, Ben's walk through the findings, the fix batch and the second batch of fixes on `main`, the
dispositions and the twelve sibling `-update.md` files on the review branch, the three inherited
items, and the integration by fast-forward at `bca64824` — about 110 commits, most of them on
`dual-agent-review-2026-09-10`. 2. The mega made sound and then trimmed: every step timed
(`93550605`), `mpp` renamed `mpplus` (`8b2386b0`), the Isaiah 24:18 diff defect fixed and the change
log regenerated (`f11ecaf8`, `6b45ad0f`), the post-stress-meteg survey regenerated for the refresh's
eleven meteg edits (`aedac688`), the `near-aleppo-census` step deleted (`d32a17b8`), the cloud
skips, and then the mega-speedup session of 2026-09-12 that retired MAM-simple's two example
programs and two Unicode-names trees, stored its BHS and Sefaria corpora incrementally, dropped
`yeivinID`, and took the Sefaria and OSIS products out of the mega — about 20 commits. 3. The
instruction-file work: the `<stem>-update.md` rule in both user-level files, "Two axes of risk",
the product tiers, the verification cadence, `doc/periodic-review.md` split out of
`doc/dual-agent-review.md`, and the `origin/main`-sourced user-configuration deployment
(`1842e784`) — about 20 commits. 4. Codex's template-projection audit on `codex-worktree-36c2`:
every template dispatch closed (`5cb06e25`), a checkpoint that rewrote nine `MAM-parsed/plus/` files
and the restoration 3 hours 35 minutes later (`2239cbad`, `73c6b113`; finding 5), the blind-dive
review and the deferred-decisions plan, and the Hebrew-filename migration
(`4e007289`) — about 15 commits. 5. On `main` directly, the Google Sheet refresh of 2026-09-10 night
and its retirement plan, the codex-index image-work retirement plan, the mega-pipeline review
disposition plan, and the README session of 2026-09-13 morning.

The review ran as five agent streams plus the main session: (A) the 2026-09-10 review's close-out
records, D12 compliance and the `State:` lines; (B) the window's code commits outside Ben's four
areas; (C) the Google Sheet refresh, the template-projection thread, the new plans and the issues;
(D) the user-configuration deployment and the live homes; (E) the prose, the mark order, the links
and the formatters. Every script and output is untracked under
`.novc/review-2026-09-14/` in the shared worktree, prefixed `A_` to `E_` per stream and
unprefixed for the main session, each stream's report beside them as `<stream>_report.md`. Two
stream claims were checked by the main session and rejected, and are recorded under "What
verifies sound" rather than as findings.

## Ben's four areas of concern, answered first

Each area's lead says what the review concluded; the numbered findings under `## Findings` carry
the evidence, and "What verifies sound" carries what was checked and found right.

1. **The fix batch of 2026-09-12 (`80f88f7c`, `6dfabceb`, `53696b30`, `3134f32b`) verifies sound on
   every claim but one small count, and the hook change has now been exercised.** All four touch no
   product tree and no data, and none of them changes what a generator writes (`3134f32b` edits the
   docstring of `py/main_pipeline_graph.py`, a generator the mega runs, and a step description in
   `py/main_0_mega.py`), so the risk assessment that sent them to `main` without detailed review
   holds on the product axis; on the act axis `53696b30` changes the cloud-session hook, which the
   2026-09-10 review, the commit message and stream D all call unexercised. This review exercised
   it: run under Git Bash with `HOME` pointed at a temporary directory and
   `CLAUDE_CODE_REMOTE=true`, the hook installs the two documents byte-identically when the
   destination is absent (`hook_exercise.py` compares the bytes of `CLAUDE.md` and the names of the
   skill's five files; a byte comparison of the five, made during Ben's walk-through of this review
   on 2026-09-14, found them identical), reports "already in place" when it is complete, fills a
   half-copied skill directory (its `SKILL.md` removed, `references/` left) back to the source's
   five files without nesting a second `hebrew-prose/` inside it, reinstalls an absent skill beside
   a present `CLAUDE.md`, and does nothing at all with `CLAUDE_CODE_REMOTE` unset
   (`hook_exercise.py`, `hook_exercise.txt`). What is verified is every path through the script that
   the fix changed, and the `cp -R <dir>/. <dest>/` semantics the fix relies on; what is not
   verified is the Linux container itself, or four paths the fix did not change: the banner for a
   missing source, the banner for a partial install, the fallback used when `CLAUDE_PROJECT_DIR` is
   unset, and an absent `CLAUDE.md` beside a complete skill. `6dfabceb`'s re-measured figures
   re-derive (7, 80 and 72 tracked `.json` files; the eight `al-hatorah` path sites at the lines it
   names), and `3134f32b`'s three edits are in place; the one count the batch left stale is finding
   4.1. `80f88f7c` was superseded the next day by `a872790e`, which changed the matching it had only
   documented, and the four cases it measured behave as the new docstring says (finding 4.2).
2. **The mega-speedup session reached products, and at `bca64824` the two products it moved out of
   the mega can no longer be regenerated: `py/main_mam4sef.py` and `py/main_mam_osis.py` both fail
   on their first book group, because the incremental storage removed the files they read 22 minutes
   after the same session took them out of the mega (finding 2.1).** The two product READMEs written
   that day tell the reader to run exactly those commands; the products are current in content as of
   the last Wikisource refresh, and from the next one on they will lag it with no working command to
   update them. Everything the mega still runs reproduces: the mega at `bca64824` passes all 55
   steps and leaves no diff, so every MAM-simple file a generator writes, the corpora, the
   Unicode-names tree and `MAM-simple/doc/versification-differences.md` among them, is what the
   generators at `bca64824` write; the README and the three `MAM-simple/doc/reading-mam-simple*.md`
   guides are written by hand, and a mega run does not check them. `3b1adf45`, the commit that
   stored the corpora incrementally, introduced two other defects, and the session fixed both before
   `main` held either: it orphaned the block that writes `MAM-simple/misc/unicode-names-vtrad-mam/`
   into a new function behind an early return, so for three commits the tree was not regenerated at
   all, which no diff could show and which `20f18020` records and fixes 62 minutes later (finding
   2.2); and it left the poetic cross-check reading no verse of Psalms, Proverbs or Job, which the
   mega's diff showed and `6dbd27e7` fixed 16 minutes later (finding 2.4). The figures the session
   wrote into the product's README, its docs and the code's comments re-derive — 23,202 `yeivinID`
   pairs with the chapter and verse always matching and a one-to-one map over 39 books, 18 of 24 BHS
   and 19 of 24 Sefaria Unicode-names files identical to the MAM ones but for the tradition token,
   9.78 MB each, six BHS and five Sefaria book groups stored, the `versification-tradition` values
   18, 1 and 5 — except the size after: 63.3 MB before and the 24.3 MB the deleted files weighed are
   right, but the same commit's `yeivinID` removal took another 1.3 MB, so the product is 37.6 MB
   after, by git blob size and by disk, not 39.0 MB (finding 2.3).
3. **The README session verifies sound apart from the D12 question its crop move raises and the
   three consequences of that move.** Every path `README.md` names exists at `bca64824` except
   `.novc/`, a gitignored directory, and `doc/*-snips/`, a glob; the eight crop sections of the four
   old READMEs are byte-identical to the new READMEs' sections apart from path tokens, as
   `a8e4790e`'s message claims; `DATA-LICENSES.md` and `README.md` agree on the crops' exception
   from the GPL-3.0 scope; `diffable-pointed-hebrew/`'s nine assignments are in `in/` under CC0 with
   the mega's step and the command repointed and the mega passing. The question is that `a8e4790e`
   edited two reports in place on `main` to repoint the moved crops while the 2026-09-10 review's
   branch, not yet merged into `main`, treated the same two reports as finished: sibling files
   created on that branch the evening before correct them, and Codex's dispositions say the finished
   source reports "remain unchanged" (finding 3.1). The consequences are that those sibling files
   and the 2026-09-10 review's update file now say the reports are unchanged at blobs the reports no
   longer have (finding 3.2); that `doc/metsudah-vs-ctr.md`, one of the dated records the commit
   left as written, got no update entry and holds the window's one new dead link (finding 3.3); and
   that the commit deleted the README holding the crop-naming rule Ben had decided that morning to
   keep, a rule the new READMEs state two ways (finding 3.4).
4. **`py/product_scopes.py`'s declaration equals the live step table, and its wrapper table is
   right, but the section of `CLAUDE.md` that presents it went stale the day it was written, and
   no rule in either file covers the path finding 2.1 took.**
   The lint's five tests pass, and an independent resolution of the 55 steps' runners gives the
   same 43 entry points and the same 18 wrappers, each wrapper read against the function it names.
   `CLAUDE.md` still says 47 entry points across 59 steps. Since `bf4a6c5e` of the same day,
   `MAM-for-Sefaria/` and `MAM-OSIS/` are written only by the two hand-run programs of finding 2.1,
   and neither file covers a change to what such a program reads, which is how finding 2.1 went
   unnoticed: `3b1adf45` changed MAM-simple, got its mega run, and broke both programs (finding 1).

## Tree health at `bca64824`: the suite at 997 and the mega clean, but ruff failing

- Suite: **997 passed, 5 skipped, 65 subtests passed** (103.44 s), run in the shared worktree with
  `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -rs` and no
  `REPOS_ROOT` set, the tree clean before and after; the five skips are the edition transcriptions'
  semantic channel (`suite.txt`). Stream A's run without the one module that reads MAM-private
  gave 995 passed, 5 skipped, the two figures agreeing. The window's own messages report 990 (ten
  commits), 992 (two), 995 (three), 996 (one) and 997 (ten) at their trees.
- Mega: **all 55 steps pass in 194.4 s and leave no diff** — `git status --porcelain` and `git
  diff --stat` both empty afterwards — run once on the detached scratch worktree at `bca64824` with
  the same interpreter and no `REPOS_ROOT` (`mega.txt`, `mega-status.txt`). So every tracked
  artifact the mega writes, the MAM products and the change log included, is what the generators
  at `bca64824` produce. The five slowest steps are `accgram-survey-post-stress-meteg` 34.6 s,
  `accgram-survey-chanted-word-accents` 15.9 s, `wlc-json-and-unicode` 14.6 s, `diff-wsgo` 11.6 s
  and `parse-ws` 11.4 s.
- The two generators the mega no longer runs: `py/main_mam4sef.py` (all three modes) and
  `py/main_mam_osis.py`, run on the same scratch worktree, each rewrite two files with the bytes
  they already hold and then exit 1 with `FileNotFoundError` on `Gen`, changing no tracked file
  (finding 2.1; `run_mam4sef.txt`, `run_mam4sef_default.txt`, `run_mam4sef_ajf.txt`,
  `run_mam_osis.txt`).
- Product trees: `MAM-parsed/plus` and `MAM-parsed/plain` at `bca64824` have the tree hashes they
  had at `209b4c05`, the last Wikisource refresh (`2072b5f9…` and `98c82e34…`), so the window
  changed neither product at its endpoints; finding 5 is about what happened between.
- The product-tier declaration: `py/product_scopes.py`'s 43 entry points (36 `py/main_*.py`, five
  `py/subcommands/*.py`, two product-tree examples) equal the set an independent resolution of the
  55 `_STEPS` runners names, its 18 wrapper entries are all used and each names the program its
  wrapper calls (`scopes_check.py`, `scopes_check.txt`).
- `black --check py`: **1,044 files would be left unchanged**. `ruff check py`: **2 errors, both
  F401**, unused imports that `5cb06e25` left behind (finding 6); `py/main_repo_maintenance.py`'s
  lint step runs the same command. Zero `sys.path` mutations in tracked `.py`: the 31 matches are
  docstrings, string literals and comments. `git ls-files --eol`: 0 `i/crlf`, 0 `i/mixed`.
  `py/tests/test_tracked_filenames.py`: 2 passed (stream E).
- Mark order over the added lines of the 313 text files the window added or modified outside the
  trees `CLAUDE.md` exempts: **54,818 added lines, 27,957 holding Hebrew, 460,654 Hebrew runs, 0
  runs not in MAM-normal order**, inside the unclassified trees and outside them alike
  (`E_02_mark_order_added_lines.py`); `py/tests/test_prose_mark_order.py` passes.
- Whitespace: `git diff --check 0354b6cc bca64824` prints nothing, 0 sites, against the previous
  window's 43.
- Markdown links: of 428 link targets in the 237 tracked `.md`, 149 are external and were not
  followed, 5 sit inside fenced code blocks and 7 are GitHub `#L` line anchors on source files; of
  the other 267, 265 resolve and **2 are dead**: the pre-existing
  `misc/what-is-mam/img/provenance-misc.md:6`, and `doc/metsudah-vs-ctr.md:4`, which `a8e4790e` made
  dead (finding 3.3). The previous review's other two "dead links", in the two user-level files, sit
  inside backticks and were never links, which the 2026-09-10 review's update file already records
  (`E_03_md_links.py`).
- `py/check_html_syntax_and_sanity.py`: "No HTML output issues found" in both its default mode
  and `--deploy-root`; after `4e007289`'s 69 renames, all 6,896 relative `src=` and `href=`
  values in the 579 tracked `gh-pages/**/*.html` resolve to tracked files (`B_08_ghpages_links.py`).
- Pages: all **37** MAM-basics deploy runs created in the window were disposed of as the
  concurrency setting intends — 36 succeeded and the one for `a8e4790e` (created 15:38:21Z) was
  cancelled by the run for `1d2ddc3d` 34 seconds behind it; the latest, for `bca64824`, succeeded
  at 18:49Z.
- Issues: fourteen touched in the window — eleven opened (#271 to #281), #266 and #267 closed on
  2026-09-13 with agent-written comments saying why, #275 opened and closed the same way, and #270
  commented on by Ben; 109 open, from 101 at the last review.
- The user-level homes: `--sync-user-config --check` from the primary clone reports nine clean
  destinations sourced from `refs/remotes/origin/main@bca64824`, and an independent hashing of the
  17 live files those destinations hold agrees, every one byte-identical to its blob (stream D).

## What verifies sound, stream by stream

**The four areas Ben named (main session).** The fix batch: `80f88f7c`, `6dfabceb`, `53696b30` and
`3134f32b` touch `CLAUDE.md`, `dot-claude/`, `py/repo_scopes.py`,
`py/repo_util/git_worktree_cleanup.py`, the docstrings of `py/main_verse_links.py` and
`py/uxlc_misc/my_uxlc_find_atom.py`, `py/main_0_mega.py`'s console text,
`py/main_pipeline_graph.py`'s docstring, the hook and two `doc/` files, and nothing under a product
tree or in a generator's output; `git ls-files` at `bca64824` gives 7, 80 and 72 `.json` under
`book-of-job/`, `aleppo/` and `cam1753/`; the eight `al-hatorah` path sites are at the lines
`CLAUDE.md` names (`chanted_word_accents.py:696`, `final_stress.py:5`,
`maqaf_nonfinal_accents.py:112`, `breuer_word_length.py:37`, `:43`, `:105`,
`post_stress_meteg.py:15`, `test_final_stress_vs_phonetic_mam.py:4`); `_held_commits` is defined
once, at `git_worktree_cleanup.py:1101`, and called at `:1127`; the retired authorship words are
gone from both modules, which now say "Ben-written"; the screen document ends on its table's last
row; the cloud document names `sed` among the hook's commands, and stream D's static trace finds
that the hook invokes `cp`, `ls`, `mkdir`, `sed`, `dirname` and the builtins `cd`, `pwd`, `echo`,
`[`, `set` and `exit`, no `git`, `curl` or `gh`; the hook parses under `bash -n` and, with `HOME`
redirected, installs, no-ops, fills and reinstalls as the "Ben's four areas" section says
(`readme_and_fixbatch_check.py`, `hook_exercise.py`). The mega-speedup session: the six MAM-simple
book groups BHS places
differently and the five Sefaria does (`vtrad.bk24s_differing_from_mam`) are exactly the files
`xml-` and `json-vtrad-bhs/` and `-sef/` hold; every `xml-` and `json-vtrad-mam/` root says
`vtmam,vtbhs,vtsef` except `Num`'s `vtmam,vtsef` and the five that say `vtmam`; the 23,202
`yeivinID` pairs at `3b1adf45^` match their `osisID` in chapter and verse and map 39 books one to
one; 18 of 24 BHS and 19 of 24 Sefaria Unicode-names files at `dcd2c1f6^` equal the MAM file but
for the tradition token, at 9.78 MB a tree; the product was 63.3 MB by blob size before
`3b1adf45`; `mam_simple_verse.mam_simple_json_path` falls back from `json-vtrad-bhs` and `-sef` to
`json-vtrad-mam` and raises otherwise, and none of its four callers skips a missing book;
`main_mam4sef.py` and `main_mam_osis.py` are declared in `NOT_IN_MEGA` with Ben's quoted reason, and
each product's README says it is not kept current and gives the command that should regenerate it,
which finding 2.1 shows failing (`mam_simple_figures.py`). The README session: of the 48 path-like
tokens `README.md` names, 43 resolve at `bca64824`, three are URLs, and the two that do not resolve,
`.novc/` and `doc/*-snips/`, are a gitignored directory and a glob (`readme_and_fixbatch_check.py`);
the eight crop sections of the four retired READMEs are byte-identical to the new READMEs' sections
once backtick path tokens are masked (`snips_readme_check2.py`);
`in/diffable-pointed-hebrew-short-name-overrides.json` holds the nine assignments and
`main_diffable_pointed_hebrew.py`'s `TRACKED_EXPANSIONS` has two pairs; `MAM-process.dot` lost its
JPS node and `pipeline.dot` and `pipeline.svg` regenerate unchanged in the mega.
`py/product_scopes.py`: the five lint tests pass, the 43 declared entry points equal the resolved
step table, the 18 wrapper entries are all used and each names the program its wrapper's body
calls (`_run_gen_site` calls `main_authored.gen_site`, `_run_diff_ctr_vs_mam` calls
`main_diff.almost_main`, the eleven `_run_accgram_*` call `main_accgram.almost_main`, the two
vendored ones run the example scripts by subprocess), and the merge `2a4b010c` correctly dropped
the four retired entry points and two wrappers (`scopes_check.py`).

**The window's other code (stream B).** `e7a1736b`'s rewrite of `py/repo_util/git_worktree_cleanup.py`
writes nothing outside the repository, reads its two outside sources (`~/.claude/sessions/*.json`
and the desktop app's `git-worktrees.json`) inside `try` blocks in the sparing direction only,
parses `worktree list --porcelain -z` and `status --porcelain --ignored -z` on NUL, decodes every
git call as UTF-8, and leaves no duplicated or unreferenced definition; `--session-ended` without
`--clean-worktrees` is refused before any repository is selected. The change log regenerates to
scratch byte-identically — `unpinned-latest.json` (21,601 bytes, 69 diffs, `new_rev` `73c6b113`)
and its HTML, and all five named releases — so `f11ecaf8`'s recorded positions and `9f6ee787`'s
`--full-history` lookup produce what the tracked artifacts carry; three throwaway repositories
show the lookup naming a commit with HEAD's `MAM-parsed/plus` tree in every merge shape. `af1c404a`'s
`json.dumps` writer re-dumps 17 of 20 tracked JSON products byte-identically, the other three
differing only by a trailing newline their own writers never emit (finding 10.6), and the
rationale holds on this venv's Python 3.13.15. The cloud skips gate on `CLAUDE_CODE_REMOTE ==
"true"` alone; `aedac688`'s 12,842 closes arithmetically from the survey's own accounting (prose
12,955 = 12,842 + 104 + 9; poetic 1,805 = 1,786 + 18 + 1; 104 + 18 = 122) and `pin_claims` passes
over the tracked survey; `5cb06e25`'s `py/mb_cmn/template_names.py` has no `.get` with a default,
no `else` arm and no catch-all, and `validate_current_plus_template` raises on a name or a
parameter outside the closed sets; 201 of the 203 commits carry `209b4c05`'s `MAM-parsed/plus`
tree; all 20 filename-returning git calls in the 1,051 tracked `.py` carry `-z`;
`mam_simple_verse.mam_simple_json_path` raises rather than returning `None`, and none of its four
callers skips a book (`B_01` to `B_12`).

**The 2026-09-10 close-out records (stream A).** The exchange reached D9's stopping rule at turn 3,
which turn 4 acknowledged ("No factual or characterization disagreement remains"), each turn an
ancestor of the next. In `doc/review-findings-2026-09-10-update.md` (1,640 lines) all 96 named
commits resolve and are ancestors of `bca64824`; 24 of 27 blob claims hold; the censuses of the
2026-09-10 review's findings 7, 8, 9, 11.5, 12/C1, 20.6, 20.8 and 21 reproduce to the last figure —
the 17 documents' 208 `.novc` lines, 25 direct plans and 21 review files, the FOI's 717 records in
groups 354 / 228 / 19 / 102 / 14, the 45 backslash paths in ten receipts, the 65,713-atom lookup
differential with its 52,881 / 12,832 / 0 / 0 split, and the closures of #266 and #267 at 15:53:01Z
and 15:53:16Z on 2026-09-13, each seven seconds after an agent-written comment. The three inherited
items are done with evidence: the merge `a7d37b34` resolves the `CLAUDE.md` conflict as item 1 says,
`d18cbb4b` adds the two pointers of item 2, and `1842e784`'s deployment reached every live home. The
nine "Classify … .novc references" commits each insert one entry into the update file and nothing
else. Of the 68 `State:` lines at `bca64824`, 61 begin with the declared State phrase for their kind
of file or keep a historical form that D10 preserves. Of the other seven, five are in files finding
7.1 names, one is in `doc/assessment-two-stranded-artifacts-2026-09-09.md`, a file of no declared
kind, and one is the State quoted at line 42 of `doc/review-findings-2026-09-08.md`. The standards
check runs clean from the worktree (`SYS_PATH_MUTATIONS=0`, `ORPHAN_MARKS=0`, `HEX_ESCAPES=80`,
`NFC_H_DOT=30`, `NFC_LATIN=39`, six linked worktrees, two agent branches). One stream A claim was
checked and rejected: the update file's SHA-256 for `dot-Codex/user-wide-AGENTS.md` is the file's,
`87C3EDDB6A9F…`, not a transposed value (`verify_a_findings.py`).

**The Google Sheet refresh, the template-projection thread, the plans and the issues (stream C).**
`a7586b4b` recorded 34 Wikisource-versus-Sheet differences in 21 verses across 11 books, all in the
verse-body column, and `44479798` brought `in/mam-go/`'s five CSVs and the tier-2
`MAM-parsed/google/` tree level in exactly those 21 verses, after which `py/main_diff.py wsgo`
reports nothing and reproduces the tracked empty files byte for byte when run to scratch; no program
in this repository writes to the live Sheet, the outward-facing act being the two tracked Apps
Scripts run inside it, per `doc/process-documentation/auto-edits-process.md`. The closed-dispatch
section is byte-identical in the two user-level files; the blind-dive review's five findings each
have a disposition at `bca64824` that the code bears out (`1b7b97ef`); #275 was closed with an
agent-written comment saying why. `doc/PLAN-dispose-mega-pipeline-review-findings.md` passes the
fresh-session checklist, and every one of its figures re-measures (85 findings, 81 open, 8 / 55 / 18
by priority) except its count of 63 `Open — queued` findings naming no root cause, which stream C
did not re-derive; `doc/PLAN-retire-codex-index-image-work.md`'s file and byte counts all
re-measure; nothing was lost in the `doc/periodic-review.md` split (69 of 75 removed lines verbatim
in the new file, six rewordings); all six named instruction commits landed in both user-level files.
The 2026-09-10 review's finding 21.6 is resolved by the closures of #266 and #267.

**The user-configuration deployment (stream D).** `--sync-user-config --check`, run once from the
primary clone, fetched `origin`, sourced `refs/remotes/origin/main@bca64824` and reported nine clean
destinations and `USER_CONFIG_PROBLEM_COUNT=0`; an independent hashing of the 17 live files those
nine destinations hold agrees, every one byte-identical to its blob at `bca64824`, LF, not a
symlink, with no live-only file inside any tracked destination and no staging or backup residue.
`user_config_sync.py` (560 lines) fetches before it reads, can source nothing but that ref (a `git
archive` into a temporary directory), stops with `USER_CONFIG_DEPLOY_FAILED` before any live write
when the fetch fails or times out, stages every changed destination before the first `os.replace`,
keeps a named backup per destination and rolls back on a later failure, removes nothing outside its
nine mappings, refuses two sources aiming at one destination, sets `GIT_TERMINAL_PROMPT=0` and
`GCM_INTERACTIVE=Never`, and in `--check` mode writes no live file (every live mtime unchanged
across the run). The deployment ran once, at about 14:31 on 2026-09-13 from `origin/main` at
`a7d37b34`: both live instruction files carry that commit's committer time to the second, the
clone's `FETCH_HEAD` had not moved since, and `bca64824` differs from `a7d37b34` in no configuration
file. The hook is wired as a `SessionStart` hook on `startup|resume|compact`, unchanged in the
window; its static trace agrees with the main session's exercise. The thirteen instruction-file
commits stream D's prompt named, of the 35 non-merge commits in the window that changed `CLAUDE.md`
or a user-level file, are each paired between the two user-level files or owed no pair, and the
preamble's five claims about the deployment re-measure against the code. One stream D statement is
superseded rather than rejected: its finding that the hook rewrite "has been exercised nowhere" was
true of the record when written, and the main session's exercise above is the measurement it asked
for.

**Prose, mark order, links and formatters (stream E).** The `hebrew-prose` skill was loaded before
reading. The two new snips READMEs state every manuscript claim as Ben's reading of a named image,
with the transcription named separately where one is cited, the one inherited exception being
finding 11.1; the six `doc/meteg-after-silluq-*-update.md` files use "has", "the LC", "the Aleppo
Codex", "the Simanim Tanakh", "pataḥ", "ḥataf", "deḥi" and "meteg" as the skill requires, every bare
"L", "A", "ga'ya", "hataf", "patax" and "dexi" in them being a quotation of the passage corrected,
except the two passages of finding 7.6; the `doc/PLAN-silluq-before-gaya-template.md` hunk's blob,
record and group figures re-measure; `aedac688`'s eleven meteg edits account for every moved figure
in the seven documents and the page hunk, and `py/tests/test_post_stress_meteg_plain_word.py`
passes; the MAM-simple, MAM-OSIS, MAM-for-Sefaria, `README.md`, `DATA-LICENSES.md` and `CLAUDE.md`
hunks re-measure except for findings 2.3 and 1.1; a banned-term scan over the added lines of the 206
`.md`, `.html` and `.py` files the window touched finds no "witness", "cantillation accent",
"proclitic", "word-division", bare "the Keter edition", or "the latter" used as a referent, and
every bare "Simanim" a quotation or the publisher sense. The five named new documents, and the four
larger ones read as well, keep every announced count, define every coined name, and lead every
finding with its disposition; `doc/mega-timing-2026-09-11.md`'s tables foot. Stream E's own figure
for the tier-3 declaration, 38, is a miscount that omitted the five `py/subcommands/` entries; the
declaration has 43 (`scopes_check.txt`).

## Findings

Findings 1 to 4 are Ben's four areas: finding 1 his fourth, 2 his second, 3 his third and 4 his
first; 5 is a rewrite of product files made and undone between the window's two anchors, out of
scope as a problem, and 6 is a lint failure that repository maintenance reports; 7 to 11 are the
record, the instruction files, the issues, the code's guards and the prose. Each lead says its
disposition at `bca64824`.

### 1. `CLAUDE.md`'s tier-3 counts went stale the day they were written, and no rule covers a change to what a hand-run program reads

**Unfixed at `bca64824`.** Ben's fourth area. Four parts.

1.1. **`CLAUDE.md`'s section "What this repository's products are, and which check a change
owes" says tier 3 is "the 47 entry points that the step table of `py/main_0_mega.py` runs across
its 59 steps, measured 2026-09-12".** Both figures were true when `63aaa6f3` wrote them at 10:23
that day. On the mega-speedup branch, `d6a6764d` (12:44) removed the `vendored-mam4sef` and
`vendored-mam-osis` steps and `bf4a6c5e` (12:47) removed `mam4sef-and-ajf` and `mam-osis`, taking
the step table from 59 steps to 55 and its entry points from 47 to 43. The two lines of work first
met in the merge `2a4b010c` at 14:35, and the sentence has been false on `main` since `main`
fast-forwarded to that merge nine seconds later. At `bca64824` the step table has **55** steps and
`py/product_scopes.py` declares **43** entry points, which is what the lint checks and what an
independent resolution of the runners gives (`scopes_check.txt`). The merge `2a4b010c`, which
brought `product_scopes.py` onto the mega-speedup branch at 14:35, resolved the conflict by
removing the four retired entry points and two wrappers from the module, with a comment saying
why, and edited no other file, so this sentence stayed as `63aaa6f3` wrote it. `CLAUDE.md`
is a document that describes the present and is kept true in place, so this is a stale figure in
a live instruction, not a receipt. Streams A, B, C, D and E each found the 59 independently.
Re-establish with `scopes_check.py`, or with `git grep -c -E "^\s+StepRecord\(" bca64824 --
py/main_0_mega.py`.

1.2. **Unfixed at `bca64824`: no rule in `CLAUDE.md` or `py/product_scopes.py` covers a change to
what a hand-run program reads, and that is the path finding 2.1 took.** Since `bf4a6c5e`,
`MAM-for-Sefaria/` and `MAM-OSIS/` are written only by `py/main_mam4sef.py` and
`py/main_mam_osis.py`, which `py/tests/test_mega_coverage.py` declares in `NOT_IN_MEGA`. Tier 3 is
still the only routine route into tiers 1 and 2, and both files' paragraph on hand-run programs
covers a change to either program: "a change to a hand-run generator owes regenerating what it
generates, which a mega run will not do for it". Neither covers a change upstream of such a program.
`3b1adf45` changed `py/main_mam_simple.py` and MAM-simple's layout, a tier-3 change that got its
mega run, and broke both programs, which read MAM-simple and which the mega no longer runs. Neither
file names the two products among what hand-run programs write: `CLAUDE.md`'s examples are all image
work, and `py/product_scopes.py` says it only in the code comment where the two entries stood. This
is an instruction gap for Ben to decide how to close; the products' own READMEs say the right thing
about currency and the wrong thing about how to regenerate (finding 2.1).

1.3. **The tiers' lint cannot see either 1.1 or 1.2, by design, and that is worth saying where
the lint is described.** `py/tests/test_product_scopes.py` defends the declaration against the
step table, so a step added or removed fails it, which is what happened on 2026-09-12 and what
`2a4b010c` resolved. It does not read `CLAUDE.md`, and it cannot know that a program leaving the
step table left a product behind. The lint's docstring says what it checks; a
one-sentence statement of what it does not check would have made 1.1 a known cost rather than a
surprise.

1.4. **Unfixed at `bca64824`: `py/product_scopes.py:26` says tier 3 is "the only route into tiers 1
and 2 other than editing those trees by hand", and lines 39–41 of the same docstring say it is "the
ROUTINE route into tiers 1 and 2, and not the only one".** `63aaa6f3` wrote both, so line 26 has
been false since it was written, because of the hand-run programs lines 41–44 name. `CLAUDE.md`'s
version says "the only routine route".

### 2. The mega-speedup session broke the two product generators it moved out of the mega, introduced and fixed two other defects in the same commit, and documented a size the product never had

Ben's second area. Four parts.

2.1. **Unfixed at `bca64824`, and the window's most serious finding: `py/main_mam4sef.py` and
`py/main_mam_osis.py` both fail on their first book group, so `MAM-for-Sefaria/` and `MAM-OSIS/`
cannot be regenerated by the commands their READMEs give.** Run from the scratch worktree at
`bca64824`: `py/main_mam4sef.py --both-sef-and-ajf`, `py/main_mam4sef.py` and `py/main_mam4sef.py
--just-ajf` each exit 1 with `FileNotFoundError` on `MAM-simple/json-vtrad-sef/Gen.json` (the AJF
mode on `json-vtrad-bhs/Gen.json`), and `py/main_mam_osis.py` exits 1 with `FileNotFoundError` on
`MAM-simple/xml-vtrad-bhs/Gen.xml`; before failing, each rewrites two files with the bytes they
already hold (two `_provenance.md` sidecars under `MAM-for-Sefaria/`, or
`gh-pages/MAM-OSIS/index.html` and its stylesheet), so none changes a tracked file
(`run_mam4sef*.txt`, `run_mam_osis.txt`). The cause is `3b1adf45` (13:09), which stored the BHS and
Sefaria corpora incrementally 22 minutes after `bf4a6c5e` (12:47) had taken the two programs out of
the mega, leaving `json-vtrad-sef/` with five book groups, `json-vtrad-bhs/` and `xml-vtrad-bhs/`
with six, and the other 18 or 19 of each only in the MAM folders. `_read_book_group` in
`py/mb_sefaria/mam4sef_or_ajf.py:71–81` opens `<input_base>/json-vtrad-<sef|bhs>/<bkg>.json`
directly, and `py/main_mam_osis.py:9` names `MAM-simple/xml-vtrad-bhs` as the only MAM-simple
directory it reads. Neither has the fallback to the MAM folder that `3b1adf45` itself gave
`py/accgram/mam_simple_verse.py` after four tests failed without it, and that `6dbd27e7` made the
only resolver the accgram callers use once the mega's diff had exposed a second resolver without it
(finding 2.4); neither commit's message names these two programs.
`MAM-simple/doc/reading-mam-simple.md` says of the two that they "read this product exactly as the
retired examples did", which is true and is the defect. Nothing caught it: the two programs were out
of the mega before the storage changed, the suite runs neither, and `20f18020`'s "Mega run on this
tree: every step passed" is true of a mega that no longer ran them. What the breakage costs today is
bounded: both products last changed in the Wikisource refresh `209b4c05` of 2026-09-10; every file
of the three MAM-simple folders they read is byte-identical at `209b4c05` and at `3b1adf45^`, and at
`bca64824` MAM-simple's reading rule gives, for every book group, that same file but for the root's
`versification-tradition` value, which neither program's code names; so the products are current in
content, and from the next refresh on they will lag it with the commands that would bring them up to
date failing. The two READMEs' "How current this product is" sections, which `bf4a6c5e` wrote and
`d0ca548e` trimmed 34 minutes after `3b1adf45`, keeping "the command", say "To bring it up to date,
run" the failing commands, and `README.md`'s core pipeline step 4 describes the two programs as what
makes the two products. `py/tests/test_mega_coverage.py`'s `NOT_IN_MEGA` reason quotes Ben's
judgment that "that code is unlikely to break (or if it does, would be easy to fix)"; it broke 22
minutes later, and the fix is the reading rule `mam_simple_verse.mam_simple_json_path` already
implements for JSON, applied in both programs, or a direct read of the MAM folder for the book
groups the tradition folders lack. Re-establish from any checkout at `bca64824`:
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_mam_osis.py`.

2.2. **Fixed by `20f18020`, 62 minutes after `3b1adf45` introduced it, and raised here because it is
a defect the mega's "no diff" check cannot catch.** `3b1adf45` inserted `def
_prune_if_same_as_vtmam` between `_finish_one_book_group`'s last statement and the block that writes
`MAM-simple/misc/unicode-names-vtrad-mam/`, which orphaned that block into the new function after an
early `return` for the `vtmam` variant — the one variant that writes Unicode names. So at
`3b1adf45`, `6dbd27e7` and `d0ca548e` the tree was not regenerated at all, and no diff could show
it, because a writer that stops writing leaves the previous run's correct files in place: the full
mega run recorded in `6dbd27e7`'s message passed over it. `20f18020` (14:11) records the defect,
proves it by deleting `Ruth.txt` and re-running, and puts the block back in `_finish_one_book_group`
(`py/main_mam_simple.py:150` at `bca64824`); the mega at `bca64824` rewrites the 24 files and leaves
them unchanged, so the tree is current. Both commits reached `main` in one fast-forward (`2a4b010c`,
14:35), so no pushed `main` held the defect. What this shows: the integration check `CLAUDE.md`
prescribes, a mega run followed by a reading of its diff, is blind to a generator that ceases to
write one of its outputs, and the check `20f18020` used — delete the output and confirm the run
restores it — is one that sees that class. No rule says to do that. #278, opened at 14:26 that day,
15 minutes after `20f18020`, by a Claude session at Ben's request, names this defect as the case
that produced it and proposes that a single-writer program assert `written_this_run == intended ==
on_disk` at the end of a whole-directory run, its first failure, "A writer went dead", being this
class; it is open and assigned to no plan. So a session at the effort level Ben is concerned about
produced an instance of the class and caught it. Finding 2.1 is a different kind of defect: programs
that fail loudly when run, and that nothing runs.

2.3. **Unfixed at `bca64824`: `MAM-simple/README.md` and `MAM-simple/doc/reading-mam-simple.md` say
the incremental storage removed 24.3 MB, "taking the product from 63.3 MB to 39.0 MB", and the
product was never 39.0 MB.** `3b1adf45` wrote both figures, and its message gives them with a file
count: "43 files and 24.3 MB go; MAM-simple drops from 63.3 MB to 39.0 MB". Summing git blob sizes
over `MAM-simple/`, the product is 63,269,926 bytes at `3b1adf45^` (63.3 MB), and the 74 files
`3b1adf45` deleted, not 43, weighed 24,287,554 bytes there (24.3 MB), which leaves 38,982,372 (39.0
MB). But the same commit also removed `yeivinID` from the 48 MAM files, another 1,340,200 bytes, so
the product is 37,645,076 bytes at `3b1adf45` (37.6 MB), and 37,647,285 at `bca64824`, which is also
what its 109 tracked files measure on disk in the worktree, with no untracked file beside them. So
24.3 MB is right for the deleted files, and 39.0 MB is a size the product had at no commit. Both
files are reader-facing product documentation. Re-establish by summing `git ls-tree -r -l -z
<commit> MAM-simple` at `3b1adf45^` and `3b1adf45`, and the `3b1adf45^` sizes of the paths
`3b1adf45` deleted.

2.4. **Fixed by `6dbd27e7`, 16 minutes after `3b1adf45` introduced it: the poetic cross-check read
no verse of Psalms, Proverbs or Job.** `3b1adf45` gave the incremental fallback to
`mam_simple_verse`'s resolver and not to a second resolver, `_mam_json_path` in
`py/accgram/mam_poetic_accents.py`, which returned `None` for the three books, and its caller
skipped them. `6dbd27e7`'s message records that the first mega run after `3b1adf45` left a diff in
eight tracked files, `out/accgram/poetic/_mam_xcheck.txt` going from "total: 4407/4465 agree
(98.70%); 58 divergences" to "total: 0/0 agree (0.00%); 0 divergences". `6dbd27e7` deleted the
second resolver and made the one left raise rather than return `None`; at `bca64824` the file's
total line reads "total: 4407/4465 agree (98.70%); 58 divergences". Both commits reached `main` in
the fast-forward to `2a4b010c`, so no `main` held the defect. Raised to complete the account of
`3b1adf45`, which introduced three defects: the mega's diff caught this one, the session caught
2.2's while writing `20f18020`, and nothing caught 2.1's. Re-establish with `git show 6dbd27e7 --
py/accgram` and `git grep -n "total:" bca64824 -- out/accgram/poetic/_mam_xcheck.txt`.

### 3. The crop move edited in place, on `main`, two reports the 2026-09-10 review's unmerged branch had declared finished, deleted the README holding a crop-naming rule Ben had decided that morning to keep, and left a dead link in a dated record it did not edit

Ben's third area. Five parts: 3.1 leaves Ben a decision, on which the fix for 3.2 depends; 3.3 and
3.4 are further consequences of the move, and 3.5 is what holds.

3.1. **Unfixed at `bca64824`; Ben's decision.** `a8e4790e` ("Keep page crops by project, not by
manuscript; remove leningrad/", 2026-09-13 11:34) changed four lines of
`doc/meteg-after-silluq-job-4-12.md` and two of `doc/meteg-after-silluq-psalms-72-15.md`
(eight and four lines in the diff, counting removals), replacing `aleppo/page-snips/…`,
`leningrad/page-snips/…` and `doc/ms-snips/…` with the crops' new paths under
`doc/meteg-after-silluq-snips/`, and "that directory's README" with "that folder's README". Its
message lists the two under "Live references updated" and says "Dated records keep the old paths,
doc/metsudah-vs-ctr.md among them". But the 2026-09-10 review's branch, which `main` did not hold
until it fast-forwarded to `a7d37b34` at 14:30 that day, already treated the two reports, like four
other reports of the meteg-after-silluq work, as finished dated documents. Each of the two has a
sibling `-update.md` that Codex created on that branch on 2026-09-12
(`doc/meteg-after-silluq-job-4-12-update.md` by `0e40b5a1`,
`doc/meteg-after-silluq-psalms-72-15-update.md` by `a0ff3b45`), whose opening sentences say the
report "is left exactly as written"; and the 2026-09-10 review's update file says "The three
finished source reports remain unchanged" in Codex's finding 11.4 disposition, of the
Koren-candidates, Job 4:12 and Psalms 72:15 reports, and "Both finished source reports remain
unchanged" in Codex's finding 20.5 disposition, of the Psalms 72:15 and screen reports. Under D12
(Ben's decision of 2026-09-11, recorded in `doc/dual-agent-review.md` by `279a6ec1` and added to
`CLAUDE.md` by `1095b027` as the section "A finished dated document is corrected in
`<stem>-update.md`, never edited", both commits on the 2026-09-10 review's branch; `main` at
`a8e4790e` had the rule in the two user-level instruction files and in `doc/periodic-review.md`) an
update to a finished document goes in the sibling file, and a path that moved is an update of
exactly that kind; the same commit left `doc/metsudah-vs-ctr.md` as written, but without the sibling
entry whose absence is finding 3.3. Either the two reports are live documents, in which case the
sibling files' "remains unchanged" statements describe a status the reports no longer have, or the
two reports are finished, in which case the new crop paths on the six changed lines belong in
entries in the two sibling files, with the reports restored. Stream A's D12 census classifies the
other in-window edits of pre-existing `doc/` files: the four finished plans and three other
documents `aedac688` edited in place with dated notes at 11:11 on 2026-09-11 predate the decision by
seven hours; `3134f32b` (2026-09-12) removed one trailing blank line from the finished
`doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md` in place, a breach by the letter and
whitespace only, and edited `doc/user-level-config-in-cloud-sessions.md`, whose status is finding
8.12; every other edit it classifies is to a live document. It leaves out two earlier edits of the
Job 4:12 report itself, which bear on whether that report is live: `f3a11572` and `bfe28eee`, at
10:20 and 10:32 on 2026-09-11, before the decision, added to that report in place what Ben reported
that day about the Second Rabbinic Bible and about two of his scans. Re-establish with `git show
a8e4790e -- doc/meteg-after-silluq-job-4-12.md doc/meteg-after-silluq-psalms-72-15.md` and, per
file, `git log --full-history --no-merges --format="%h %ad %s" --date=iso-local 0354b6cc..bca64824
-- <file>`.

3.2. **Unfixed at `bca64824`: three live records say the two reports are unchanged at blobs
`a8e4790e` replaced.** `doc/meteg-after-silluq-job-4-12-update.md:43–44` gives blob `b8fc419f…`, and
the report at `bca64824` is `eb4dcee4…`; `doc/meteg-after-silluq-psalms-72-15-update.md:55–56` gives
`b7944176…`, and the report is `e1b0559a…`; `doc/review-findings-2026-09-10-update.md:795–796`
(`8ee5e54e`, 10:21 on 2026-09-13) says "The six finished reports remain byte-identical to the Git
blobs recorded in those sibling update entries", and two of the six are not. `8ee5e54e` wrote all
three statements on the 2026-09-10 review's branch, where they were true; `a8e4790e` was committed
on `main` 73 minutes later, and the three statements first became false in the merge `8c6b66c4` at
12:00 that day, the first commit to hold both `8ee5e54e` and `a8e4790e`; `main` has held both
commits since it fast-forwarded to `a7d37b34` at 14:30. An update file "is itself live, so it is
kept true". What `a8e4790e` changed in the two reports is where they say the crops are, and every
passage the siblings correct is in the reports word for word both before and after `a8e4790e`, so
the corrected readings the siblings give still apply. Re-establish: `git rev-parse
bca64824:doc/meteg-after-silluq-job-4-12.md bca64824:doc/meteg-after-silluq-psalms-72-15.md`
(`verify_a_findings.py`); `git merge-base --is-ancestor 8ee5e54e a8e4790e`, which fails.

3.3. **Unfixed at `bca64824`: `doc/metsudah-vs-ctr.md:4` is a dead link, and
`doc/metsudah-vs-ctr-update.md` does not record it.** The link
`[ms-snips/README.md](ms-snips/README.md)` resolves to `doc/ms-snips/README.md`, which `a8e4790e`
renamed to `doc/lam-2-3-akhla-snips/README.md`; in that finished document, three further mentions
give `doc/ms-snips/README.md` as a path, and three more speak of "the ms-snips thread", "the
ms-snips spotlight" and "the ms-snips correction thread". Leaving the document as written is what
D12 requires, and the commit message says so; the rule's other half, the correction in the sibling
file, was not done — the update file's one entry, of 2026-09-12, is about `download_sefaria.py`.
This is the window's one new dead link. Re-establish: `E_03_md_links.py`; `git ls-tree bca64824
doc/ms-snips/` (empty).

3.4. **Unfixed at `bca64824`: `a8e4790e` deleted `leningrad/page-snips/README.md` six minutes after
Ben's decision to keep its crop-naming rule was recorded on the 2026-09-10 review's branch, and each
new README states the rule two ways.** `f3c7f79a` (Codex, 11:28 on 2026-09-13) recorded the decision
in the 2026-09-10 review's update file as Ben's decision on that review's finding 20.9, "Keep the
current rule.", followed by "The live rule in `leningrad/page-snips/README.md` therefore remains
unchanged". That rule named a Leningrad crop `<folio><side>-col<N>-line<N>-<ref>-<slug>.png` "when
the line has been read off the image", and the entry adds that an estimator's column may stay in the
name when the README says so. `main` did not hold `f3c7f79a` when `a8e4790e` deleted the README at
11:34. Each new README's general naming sentence asks for more, putting a column and line in a name
only "where the column and line have been established"
(`doc/meteg-after-silluq-snips/README.md:9–11`) or "where they have been read off the image"
(`doc/lam-2-3-akhla-snips/README.md:9–10`), while its Leningrad subsection conditions the name on
the line alone: "a Leningrad crop's name has a column and line only where he gave the line
unprompted" (`doc/meteg-after-silluq-snips/README.md:40–42`,
`doc/lam-2-3-akhla-snips/README.md:43–45`). The sections for
`leningrad-380A-col2-line3-Ps72v15-yevarkhenhu.png` and
`leningrad-430B-col2-line10-Lam2v3-akhla.png` still say that the column in each name is the
estimator's, so the general sentences, read literally, do not allow those two names: that is the
stricter policy finding 20.9 put to Ben, and not the one he chose. Two live records say the rule was
kept unchanged: the entry's sentence above, at `doc/review-findings-2026-09-10-update.md:874`, and
the close-out table's "item 20.9 keeps the live crop-coordinate rule by Ben's decision" (line 1622),
which `bca64824` wrote after the merge `8c6b66c4` had brought the deletion into the 2026-09-10
review's branch. Re-establish: `git show a8e4790e^:leningrad/page-snips/README.md`; `git merge-base
--is-ancestor f3c7f79a a8e4790e`, which fails.

3.5. **Raised, not a defect: everything else about the move holds.** The eight crop files moved at
100 per cent similarity; the eight crop sections of the four retired READMEs are byte-identical to
the new READMEs' sections apart from path tokens; `DATA-LICENSES.md`'s new row covers both folders
where the old table had a row for `leningrad/page-snips/` only and none for `doc/ms-snips/`;
`cam1753/cam1753-page-index.json`'s note, the verse-links skill, docstrings and comments in three
Python files, and `doc/PLAN-retire-codex-index-image-work.md` are repointed; and `1d2ddc3d`, four
minutes after the move, replaced `README.md`'s `leningrad/` entry with one for `in/lci_recs.json`,
which exists. What the new READMEs promise and do not keep is finding 11.3.

### 4. The one count the fix batch left stale, the atom lookup's changed policy, a traceback on an ambiguous form, and a letters-only note that no longer prints

Ben's first area. Four parts, the first unfixed and the other three raised.

4.1. **Unfixed at `bca64824`: `CLAUDE.md`'s "Two further mentions name the repo with no path in them
— `edition_transcription.py:67` and `final_stress.py:16`" is five within `py/accgram/`.** `6dfabceb`
re-measured the path-bearing sites, correctly, from seven to eight, and left the path-free count as
it was written on 2026-08-11. At `bca64824` `py/accgram/post_stress_meteg.py` names the repository
without a path at lines 19, 24 and 2723 ("al-hatorah's schedule", "al-hatorah's business",
"al-hatorah's pipeline"), all of which read correctly as written, and all three already stood at
`0354b6cc`, so the batch left the count stale rather than making it stale. Outside `py/accgram/`, 24
more lines under `py/` name the repository, 20 of them outside `py/tests/` as well, most of them
with a path; `CLAUDE.md` counts one of the 24, `py/tests/test_final_stress_vs_phonetic_mam.py:4`,
among its eight sites. Re-establish with `git grep -n "al-hatorah" bca64824 -- py/`. A remediation
option, raised during Ben's walk-through of this review on 2026-09-14: delete the count and the two
sites it names rather than correcting it to five, since a mention with no path needs no action and
this count was already stale when `6dfabceb` re-measured the eight sites beside it; one sentence
saying that such mentions read correctly as written would keep that `CLAUDE.md` paragraph's point
with no figure to go stale.

4.2. **Raised, not a defect: `80f88f7c` documented a matching behaviour that `a872790e` changed the
next day, so three of the four cases the fix batch measured for finding 12 now come out
differently.** `80f88f7c` recorded that the letters-alone pass dropped only Unicode categories Mn
and Cf, so a bare consonantal form failed for a verse-final or maqaf-final atom; Codex's C1 then
found 3,590 punctuated atoms whose bare query succeeded at a different position; and `a872790e`
("Make bare UXLC atom lookup unambiguous"), implementing Ben's decision of 2026-09-13, which the
entry "Finding 12 and C1" of `doc/review-findings-2026-09-10-update.md` records, made the
`strip_heb` of `py/uxlc_misc/my_uxlc_find_atom.py` retain only U+05D0–U+05EA and made a bare query
use the letters-only pass always, returning only when its letters occur once in the verse. Re-run at
`bca64824` with `py/main_uxlc_estimate_atom_loc.py`: Psalms 72:15's bare last atom and Job 4:12's
bare last atom now match by letters alone, Job 4:12's bare first atom still matches atom 1, and
Genesis 1:2's bare `על` is refused as ambiguous between atoms 6 and 12, all as the new docstring and
the skill's three homes say; stream A reproduced that entry's whole 65,713-atom differential. The
2026-09-10 review's finding 12, its reconciliation row and its disposition row of 2026-09-12
describe the older behaviour, accurately for their date, and that entry says it supersedes the
disposition row.

4.3. **Raised, minor: on an ambiguous form `py/main_uxlc_estimate_atom_loc.py` exits 1 with a Python
traceback rather than a message.** Its `main` catches `AtomNotFound` only, so the
`ValueError("Ambiguous: 2 letters-only matches …")` that `find_atom` raises propagates. Its
docstring says "An ambiguous form is refused by find_atom", which is true; `py/main_verse_links.py`
catches the same error and lists the atoms numbered with exit 1, as the verse-links skill promises
for it. Re-establish with `py/main_uxlc_estimate_atom_loc.py Genesis 1:2 על`. A remediation option,
raised during Ben's walk-through of this review on 2026-09-14: catching the error and listing the
numbered atoms, as `py/main_verse_links.py` does, would not be enough by itself, since
`py/main_uxlc_estimate_atom_loc.py` takes no `--atom` to accept a number, and where the repeated
atoms are byte-identical, as Genesis 1:2's atoms 6 and 12 are in the UXLC, the UXLC's form of the
atom is refused as ambiguous too; the command needs an `--atom` option, or an error that points to
`py/main_verse_links.py --atom N`, which gives the same folio, column and line estimate. The
traceback predates the window: at `0354b6cc`, too, the program's `main` function caught only
`AtomNotFound`. `a872790e` made ambiguity the result of every bare query whose letters occur more
than once in its verse: 12,832 of the 65,713 bare queries in the differential of
`doc/review-findings-2026-09-10-update.md`'s entry "Finding 12 and C1".

4.4. **Raised, minor: since `a872790e`, `py/main_verse_links.py` no longer says when it placed an
atom by its letters alone.** `a872790e` renamed the method `find_atom` returns for a letters-only
match from `"stripped"` to `"letters"` and left `py/main_verse_links.py:162` testing `method ==
"stripped"`, so that command's note "(matched by its letters alone; the UXLC has …)" has not printed
since, while `py/main_uxlc_estimate_atom_loc.py`, which tests for any method other than `"exact"`,
still prints its note. The atom is still placed correctly, since a letters-only match returns only
when the letters occur once in the verse; what is lost is the only sign that the UXLC's form of the
atom differs from the form given, such as MAM's. The entry "Finding 12 and C1" of
`doc/review-findings-2026-09-10-update.md` records the note as the command's behaviour before the
change. Added during Ben's walk-through of this review on 2026-09-14, when a query that is Psalms
72:15's first atom as the UXLC has it, without its accent, returned `(1, "letters", …)` from
`find_atom` at `bca64824`, and of the two commands only `py/main_uxlc_estimate_atom_loc.py` printed
a note. Re-establish: `git grep -n '"stripped"' bca64824 -- py/main_verse_links.py
py/uxlc_misc/my_uxlc_find_atom.py`, which finds the test and no return.

### 5. Out of scope as a problem, and already remediated: a Codex checkpoint commit on a side branch rewrote nine `MAM-parsed/plus/` files, a distributed product, and a commit 3 hours 35 minutes later restored them

**Out of scope as a problem, and already remediated.** Across the window `MAM-parsed/plus` did not
change: its tree is the same at `0354b6cc` and at `bca64824`. What this finding describes existed
only between those two commits, on a side branch, and this review is of the window's single diff
(Ben, 2026-09-15, during his walk-through of this review: "The review is, conceptually, of a single
diff, between the start commit and the end commit"). What let it happen was remediated inside the
window, and Ben agreed during the same walk-through that nothing more is needed: `e97ba21c`
(2026-09-11 18:23, on `codex-worktree-36c2`) added the rules "A deep dive diagnoses; Ben decides
semantic policy" and "An invalid representation does not select its replacement" to both user-level
instruction files; `63aaa6f3` (committed 2026-09-12 10:36) defined this repository's product tiers
in `CLAUDE.md` and `py/product_scopes.py`; and `fb575b09` (committed the same minute) added "Two
axes of risk" to both user-level instruction files. `2239cbad` ("Checkpoint the template-projection
audit", committed 2026-09-11 12:20) changed `MAM-parsed/plus/A1-Genesis.json`, `A2-Exodus.json`,
`A3-Levit.json`, `A4-Numbers.json`, `A5-Deuter.json`, `B1-Joshua.json`, `D1-Psalms.json`,
`D2-Proverbs.json` and `D3-Job.json`, 140 insertions and 627 deletions. The special-letter wrapper
template `מ:אות-מיוחדת-במילה` has a chanted word with a small, large or hung letter in two forms,
decomposed around the special letter in parameter 1 and as a plain string in parameter 2, with a
dot-mask, a type code and a summary in parameters 3 to 5; 11 of its 95 calls at `bca64824` wrap a
maqaf compound. In documentation text `2239cbad` replaced each call with the contents of its
parameter 1 — 40 of the 72 calls in those nine books, all in note parameters, while the 32 in
Scripture stayed — so the special letter's template remained, the chanted word's other letters
stayed as text beside it, and parameters 2 to 5 were dropped: at Genesis 5:1, for one, the note
quoting the large samekh kept its letters and lost the wrapper. The same commit changed 18 files
under `gh-pages/`, a published product: five files of MAM-with-doc's `foi-slh-word`,
`foi-rare-tmpls` and `foi-unicode` pages, `foi/provenance.md` and 12 call-graph SVGs. `5cb06e25`
inherited that plus tree and regenerated 27 files of MAM-simple's Deuteronomy, Genesis and Numbers
from it, in all three versifications. `73c6b113` ("Restore special-letter wrappers in documentation
text", 15:55, 3 hours 35 minutes after the checkpoint was committed) put them back:
`MAM-parsed/plus` has the same tree hash, `2072b5f9…`, at `209b4c05`, `0354b6cc`, `73c6b113` and
`bca64824`, and `ff2f5bfb…` only at `2239cbad` and `5cb06e25`; `MAM-parsed/plain` is `98c82e34…` at
all 203 commits; and at `73c6b113` the 27 MAM-simple files and 17 of the 18 `gh-pages/` files are
byte-identical to their state at `6982dcf5`, the 18th being `foi/provenance.md`. `2239cbad`,
`5cb06e25` and `73c6b113` reached `main` together in the fast-forward to `2a75c1e2` at 10:20 on
2026-09-12, pushed at 10:21, and no Codex branch is on the remote, so no pushed branch tip had the
flattened tree, though that push took `2239cbad` and `5cb06e25` to GitHub in `main`'s history. The
mega at `bca64824` regenerates `MAM-parsed/plus` byte-identically, which confirms that the
restoration equals what the parser writes. Re-establish with `git log --full-history --format="%h
%s" 0354b6cc..bca64824 -- MAM-parsed/plus` and `git rev-parse <commit>:MAM-parsed/plus`.

### 6. `ruff check py`, which repository maintenance runs, fails on two unused imports that `5cb06e25` left behind

**Unfixed at `bca64824`.** With ruff 0.16.5, `ruff check py` passes at `0354b6cc` and reports two
F401 errors at `bca64824`. `5cb06e25` replaced `_token_text`'s body in `py/accgram/rtmsr_verse.py`
with a call to `text_from_one_token_like`, leaving `from accgram import rtmsr_sat` at line 6 unused,
and replaced `_flatten_text`'s body in `py/foi/kq_trivial_types.py` with a call to
`project_qere_atoms`, leaving `from mb_cmn import template_names as tmpln` at line 9 unused. `git
blame` dates both import lines before the window; `git log -S` names `5cb06e25` for both removed
uses. `ruff.toml` says the linter is "wired into the repo-maintenance script's lint step", and
`py/main_repo_maintenance.py:167` runs `ruff check py`, so the next maintenance run reports its lint
step as failed, goes on to its later steps, and exits with status 1. `py/main_repo_maintenance.py`
is the only tracked program that runs ruff, so a ruff failure shows up only in repository
maintenance; Ben, 2026-09-15, during his walk-through of this review: "it is fine by me that such
ruff issues only show up during repo maintenance", and "repo maintenance should only stop if it
cannot continue". Removing the two imports would change no output: neither is part of an import
cycle, each of the five modules that import `rtmsr_verse` loads `rtmsr_sat` by another route, and
`kq_trivial_types` also loads `template_names` through `ws_tmpl2`. Re-establish with
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m ruff check py` from the repository
root ("Found 2 errors"), and for `0354b6cc` by running the same command at the root of an extracted
`git archive 0354b6cc py ruff.toml` ("All checks passed!").

### 7. The 2026-09-10 review's close-out record: a stale line-3 State by design, one blob that does not exist, two departures from the written procedure, and three smaller defects

Stream A, with one item from stream E. Six parts; none touches a product. Apart from the labels 7.1
to 7.6 of its six parts, every finding number in finding 7 names a finding of the 2026-09-10 review.

7.1. **Raised, not fixed; Ben's decision on its remediation is at the end of this part:
`doc/review-findings-2026-09-10.md`'s line 3 and its dispositions table were left stale on purpose,
and no rule declares what replaces them, a current State given in a sibling update file, which eight
more finished documents also have.** Line 3, last written by `c8de6abc` on 2026-09-12, says that
review's findings 7 to 11, 18 and 21 and the rest of 13, 16, 19 and 20 are "not acted on", and the
dispositions section's closing paragraph says the same; the update file's close-out entry ("##
Close-out: every finding and inherited integration item has a disposition") says "This entry
supersedes the initial review's line-3 statement … D12 leaves that finished dated review unchanged".
Three rules of record place remediation state in the review file itself: D10 rule 3 in
`doc/dual-agent-review.md` and `py/repo_util/check_repo_standards.py`'s docstring put it on line 3,
and `doc/periodic-review.md`'s close-out step 3, written after D12, puts the dispositions in the
review's own `## Dispositions after remediation` section while "the rest of the file is left as
written". The round kept line 3 and the table current through its 2026-09-12 batch and recorded
every later disposition in the update file; a reader of line 3 now gets the wrong answer. The same
arrangement covers eight more finished documents at `bca64824`, each with a sibling entry that gives
or supersedes its State: three plans have no `State:` line at all
(`doc/PLAN-efficient-wikisource-downloads.md`, `doc/PLAN-wikisource-derived-mam-products.md`,
`doc/PLAN-worktree-file-consolidation.md`); three have a line 3 outside the declared vocabulary
(`doc/PLAN-close-out-review-2026-09-08.md`, `doc/PLAN-evacuate-five-MAM-products.md`,
`doc/PLAN-evacuate-public-repos-programme.md`); `doc/review-findings-2026-09-08.md` reads
"remediated 2026-09-10"; and `doc/blind-dive-into-template-params.md` reads "five open findings.",
which its sibling entry calls overtaken. No rule tells a reader of line 3, human or mechanical, to
look for such an entry. Ben decided on 2026-09-15, during his walk-through of this review, that the
sibling arrangement is to become the written rule in the remediation phase, a timing he left open
("Either is fine"): a finished document's line 3 stays as written, and a State it takes on later,
and a review's dispositions, go in its update file, which supersedes line 3, so that a review gets
no `## Dispositions after remediation` section; `doc/dual-agent-review.md` and
`doc/periodic-review.md` are to say so, edited in place because they describe the current procedure.
His words on the remediation: "don't change any existing plan documents, just make whatever updates
you suggest to an -update.md (or -update-N.md if -update.md is taken already, and N is sequentially
the next unused integer)"; and, asked whether the procedure should say that a finished document's
later status goes in its update file: "Yes, the policy of -update.md files should be documented in
the two files you suggest", the two files being those two documents. Re-establish: `git grep -n
"^State:" bca64824 -- "doc/*.md"`; `A_05`.

7.2. **Unfixed at `bca64824`: the update file's entry for the 2026-09-10 review's finding 7.2 cites
a blob that is not in the repository.** `doc/review-findings-2026-09-10-update.md:1414`: "The screen
report remains unchanged at Git blob `09ac3f23175aacb1ffb10c39894b3c2d2fe78912`." `git cat-file -t`
on that id fails. The screen report's blob at the entry's own checkpoint and at `bca64824` is
`a46dbf0f…`, which `doc/meteg-after-silluq-screen-against-uxlc-and-wlc-update.md` records correctly;
the screen report's only other blob in the history of any branch is `2b146272…`. The hash has stood
since `8e2db58f`. Re-establish: `git cat-file -t 09ac3f23175aacb1ffb10c39894b3c2d2fe78912`
(`verify_a_findings.py`).

7.3. **Raised: the close-out record departs from D9's written procedure at two points.** D9's
close-out list in `doc/dual-agent-review.md` has, as step 2, "Update the procedure record with the
round's outcome and the approved process changes": the process changes, D12 among them, are in that
file, but the outcome is not, since at `bca64824` the file does not contain the string `2026-09-10`
and its "What Codex joined" census is still the one measured on 2026-09-09. As step 3 it has a
remediation plan for a fresh task, with concrete editorial wording for Ben's approval: no such plan
was written, and the remediation is recorded entry by entry in
`doc/review-findings-2026-09-10-update.md`. The exchange itself followed D9: turn 3 says that under
the stopping rule "it ends the round", turn 4 says "This file is the acknowledgment required by the
stopping rule", as `8c49cdd2` acknowledged the September 8 round's turn 5, and D9 asks Ben at that
stage to settle only an objection, which turn 4 does not raise. Ben's decisions are recorded for
findings 7.2, 10, 11.5, 12/C1, 20.9 and 21.6 and inherited item 3, and his 2026-09-12 instruction on
findings 12 to 21 went to the Claude session whose batch the 2026-09-10 review's dispositions table
records. No approval is recorded for the corrected readings Codex wrote for findings 11.1 to 11.4
and 20.2 to 20.5, for 20.1's docstring change or for finding 8's State declarations, but D7 says to
"Follow already-recorded decisions without asking again", and most of those apply rules already
recorded: the `hebrew-prose` vocabulary, the prose rules and D10's State words; 11.1 corrects a
misidentified edition. Re-establish: `git grep -n "2026-09-10" bca64824 --
doc/dual-agent-review.md`; `git grep -n "stopping rule" bca64824 --
doc/dual-agent-review-2026-09-10-turn-03-claude.md
doc/dual-agent-review-2026-09-10-turn-04-codex.md`.

7.4. **Raised, low: the standards docstring and D12 describe an update file's entries in ways that
conflict, and one entry of `doc/review-findings-2026-09-10-update.md` has no "Recorded by" line.**
`py/repo_util/check_repo_standards.py:339` says "An update file's entries are each finished and
dated the moment they are written, so nothing in one is ever pending", while D12 in
`doc/dual-agent-review.md` says an update file "is itself live, so it is kept true"; 7.2, 7.5 and
7.6 of this finding follow D12, counting stale statements in a live update file as defects to
correct. At `bca64824` the update file has 39 headed sections, 38 of them with a "Recorded by" line;
the one without is the entry for finding 10, "Finding 10: the moved crop directories have dedicated
license coverage". Re-establish: `git grep -n "finished and dated" bca64824 --
py/repo_util/check_repo_standards.py`; `git grep -c "^Recorded by" bca64824 --
doc/review-findings-2026-09-10-update.md`.

7.5. **Raised, low: the line numbers in two live entries have drifted, and one entry's SHA-256
values name no checkpoint.** Both entries name the text they locate. The entry for finding 20.1
gives `CLAUDE.md`'s "hand-authored" at lines 24, 49, 69 and 166 and "hand-maintained" at 992, and at
`bca64824` lines 166 and 992 are 173 and 1005. The entry for finding 20.11 gives
`[page](gh-pages/accgram/page.html)` at line 1416 of `dot-claude/user-wide-CLAUDE.md` and line 1197
of `dot-Codex/user-wide-AGENTS.md`, which are 1461 and 1240 at `bca64824`, and it gives the two
files' SHA-256 values without the commit they were measured at; the values were right when the entry
was written, and both files have changed since. Re-establish: `git grep -n -e hand-authored -e
hand-maintained bca64824 -- CLAUDE.md`; `git grep -n -F "[page](gh-pages/accgram/page.html)"
bca64824 -- dot-claude/user-wide-CLAUDE.md dot-Codex/user-wide-AGENTS.md`.

7.6. **Unfixed at `bca64824`: two internal inconsistencies in the live
`doc/meteg-after-silluq-search-in-mam-documentation-update.md`.** Its line 117 says "Finding 11.5's
separate choice between `hataf` and `ḥataf` remains unmade", while the same file's entry for that
finding, the 2026-09-10 review's finding 11.5, at lines 25–47, recorded 2026-09-13, records the
choice and applies it; and the corrected reading for the 1 Kings 7:37 Classification cell, at line
70, keeps "silluq then ga'ya" while the entry at line 93, "Analytic `ga'ya` terminology should read
`meteg`", says the six passages it corrects use "the report's analytic voice, for which the report's
opening vocabulary note declares" meteg, and the cell is the report's classification, not a
quotation of MAM's note (stream E).

### 8. Twelve stale, unattributed or asymmetric statements in the instruction files, procedure documents and plans

Streams C and D; stream E also found 8.7's `CLAUDE.md` spellings and 8.10's census glob. None
touches a product; each is in a live document kept true in place, or in a plan a fresh session would
execute. 8.12's document is live by Ben's decision of 2026-09-15, recorded in that part.

8.1. **Unfixed at `bca64824`: `dot-claude/user-wide-CLAUDE.md:329` says the maintenance runbook's
Codex task-folder step is "its step 7"; since `2239cbad` that step is 8.** `2239cbad` inserted
step 7, "Audit recursive template and node walkers for undeclared projections", into
`doc/PLAN-repo-maintenance-across-GitRepos.md` and renumbered the task-folder step to 8. The Codex
file's parallel sentence carries no number. The live `~/.claude/CLAUDE.md` is byte-identical, so
every Claude session loads the stale number. Re-establish: `git grep -n "its step 7" bca64824 --
dot-claude/user-wide-CLAUDE.md`.

8.2. **Unfixed at `bca64824`: `dot-claude/user-wide-CLAUDE.md:855–856` says the fuller statement
of the `<stem>-update.md` rule "reaches MAM-basics' `main` with the 2026-09-10 review round, so
until then it is findable only on that round's branch".** The round integrated at `bca64824`;
`1095b027`, which put the statement in `CLAUDE.md`, is an ancestor of `origin/main`. Live in
`~/.claude/CLAUDE.md`. Re-establish: `git merge-base --is-ancestor 1095b027 origin/main`.

8.3. **Unfixed at `bca64824`: `doc/dual-agent-review.md:480–487` still describes the retired
live-first procedure**, saying the Codex file's canonical copy comes "with the same manual
write-back and the same drift check" and giving a `Get-Content … .Count` command for the live file.
`1842e784` retired the write-back and replaced the check with `--sync-user-config --check`. The file
is live: its own D12 names "this file" among the documents that describe the present and are kept
true in place. Re-establish: `D_03_report.txt` §6.

8.4. **Unfixed at `bca64824`; Ben's decision on its remediation is at the end of this part: the
hook's inventory of tracked entries omits `dot-claude/shared-skills.txt`.**
`.claude/hooks/install-user-config.sh:45–62` says "Three further entries are tracked beside them and
none is installed here"; `1842e784` added `shared-skills.txt` beside them and edited this file's
comments without extending the list. `dot-claude/` holds ten tracked files. Ben decided on
2026-09-15, during his walk-through of this review, that in the remediation phase the comment is to
name what the hook does not install without claiming to name all of it, so that a newly tracked
entry cannot make it stale again. Re-establish: `git ls-tree -r --name-only bca64824 -- dot-claude`.

8.5. **Raised, outside the window's diff: the Codex instruction file's two Hebrew-terminology
sections cite an evacuated repository where the Claude file cites this one.** "**UXLC-utils**
`doc/clc-design.md` §7.16", "`mb_cmn/hebrew_punctuation.py` (vendored into UXLC-utils and
wlc-utils)" and "**UXLC-utils** `doc/clc-design.md` §2" in `dot-Codex/user-wide-AGENTS.md`, where
`dot-claude/user-wide-CLAUDE.md` says "**MAM-basics** `uxlc/doc/clc-design.md`" and "formerly
vendored". Both wordings entered this repository with `74d883d2`, which brought both files here on
2026-09-09, six days after the 2026-09-03 evacuation, and both sections are byte-identical in both
files at `0354b6cc` and at `bca64824`. So the window's diff did not touch what this part describes;
it was noticed while the two files were compared, and since a periodic review is of the window's
single diff (`doc/periodic-review.md`, "What the periodic review is"), it stands here as something
noticed rather than as a defect of the window. Re-establish: `git grep -n "UXLC-utils" 0354b6cc
bca64824 -- dot-Codex/user-wide-AGENTS.md`.

8.6. **Raised, not a defect: the Codex file did not receive `6dfabceb`'s clarification that the
cited github-misc commits do not resolve here.** `dot-Codex/user-wide-AGENTS.md:44–47` cites
`25a8955` and `560239c` with only `1925699` labelled `github-misc`; none of the three resolves in
MAM-basics. Re-establish: `D_03_report.txt` §3.

8.7. **Raised; Ben's decision on its remediation is at the end of this part: the Codex home is
spelled `.Codex` in the code and `~/.Codex/` in 9 lines of the files the command below searches,
`~/.codex/` or `C:/Users/BenDe/.codex/` in 22 lines of them, and the directory on disk is
`.codex`.** `user_config_sync.py:252` maps to `.Codex/AGENTS.md`; NTFS makes that one file with
`.codex`, and a case-sensitive filesystem would not. The Codex-side files already spelled the home
`.Codex` at `0354b6cc`, and `1842e784` changed `~/.codex/` to `~/.Codex/` in axis item 3 of both
user-level files and in `CLAUDE.md:105`. At `bca64824` the command prints 34 lines: 9 with
`~/.Codex/`, 14 with `~/.codex/`, 8 with `C:/Users/BenDe/.codex/`, and three relative paths,
`.codex/worktrees/<sibling>` in the Claude user-level file and `.Codex/worktrees/<sibling>` and
`.Codex/launch.json` in the Codex one. Ben decided on 2026-09-15, during his walk-through of this
review, that `.codex`, the spelling on disk, is to stand everywhere, a change for the remediation
phase. Re-establish: `git grep -n -E "\.[Cc]odex/" bca64824 -- CLAUDE.md dot-claude dot-Codex
doc/dual-agent-review.md`.

8.8. **Raised, unfixed at `bca64824`; Ben's decision on its remediation is at the end of this part:
`doc/PLAN-retire-google-sheet.md` fails four items of the fresh-session checklist and carries a
stale expectation.** No decision in it is dated or attributed — the retirement and the freeze date
"the Sheet as frozen on September 12, 2026" name no decider; lines 28–29 tell the executor to read
"the `hebrew-prose`, `spreadsheets`, and `computer-use` skills", of which only `hebrew-prose` is
tracked in this repository's skill homes, without saying where the other two live; the stage-count
figure carries no re-establishing command; it does not say whether another session may be live, one
of the preconditions the checklist asks a plan to state; and lines 45–46 expect 57 mega stages after
the retirement where `bca64824`'s 55 minus `parse-go` and `diff-wsgo` is 53 (its "if the planning
snapshot's 59 stages have not otherwise changed" hedge is right, and they have). It has no
authorship line either, though no checklist item asks for one. It also does not record that the last
auto-edit application left the Sheet level with Wikisource — both `out/` files are `[]` and `wsgo`
reproduces them — which is the fact that makes freezing the Sheet harmless, and which the plan's
deletions remove the tool for re-establishing. Ben decided on 2026-09-15, during his walk-through of
this review, that in the remediation phase this plan and the plan of 8.9 are to be made
agent-neutral, their Codex-specific lines, such as the `codex-worktree-<worktree-id>` branch naming,
replaced so that either agent can execute either plan. Re-establish: `C_06_mega_step_counts.py`;
`git ls-files -- "dot-Codex/skills/*/SKILL.md" "dot-claude/skills/*/SKILL.md"`.

8.9. **Raised, unfixed at `bca64824`; Ben's decision on its remediation is at the end of this part:
`doc/PLAN-retire-codex-index-image-work.md` dates its seven decisions and attributes none of them**,
listing them in the imperative under "Decisions recorded on 2026-09-12" with only the 2026-09-13
amendments naming Ben, and its line 60 sends the executor to `C:/Users/BenDe/.codex/AGENTS.md`,
which a Claude executor does not load, without saying which agent the plan is written for. Every
file count and byte count in it re-measures; its test counts, taken at its planning snapshot
`06874577`, were not re-run. Ben decided on 2026-09-15, during his walk-through of this review, that
in the remediation phase this plan and the plan of 8.8 are to be made agent-neutral, their
Codex-specific lines, such as line 60's pointer to Codex's instruction file, replaced so that either
agent can execute either plan.

8.10. **Raised, low; Ben's decision on its remediation is at the end of this part: the
`doc/periodic-review.md` split left the close-out procedure stated in both files, and hands the
reader a census glob that now over-matches.** `doc/periodic-review.md` §"Close-out" gives four steps
and `doc/dual-agent-review.md:125–137` six, step 1 verbatim in both; and the new file's "ten files
match `doc/review-findings-*.md` … all of them window reviews" with `git ls-files --
"doc/review-findings-*.md"` as its command returns 13 files at `bca64824`, two of them the
2026-09-08 and 2026-09-10 update files. Ben decided on 2026-09-15, during his walk-through of this
review, that the duplicated close-out list is to be removed in the remediation phase by the same
edit that writes finding 7.1's update-file rule into the two documents: one of them keeps the list
and the other points to it. Re-establish: `C_04_split_check.py`; `git ls-tree --name-only bca64824
doc/`.

8.11. **Raised; Ben's decision on its remediation is at the end of this part: `2eee5f51` rewrote the
closing-message section of the Claude user-level file, a section the Codex file has never had, from
a rule bar to an H1 heading.** That section is one of seven whose headings exist only in the Claude
file, at `0354b6cc` and at `bca64824` alike, and the other six have the same text at both commits,
so the window's diff changed only this one of the seven. Five of the seven entered this repository
with `74d883d2` on 2026-09-09; "Prompt authorship: sign the chips you write" came with `628b1ac8`
that evening, and the closing-message section with `35a73b06`. Two of the seven,
"all-repos.code-workspace is the roster" and "A successor session verifies its exact checkout and
commit before editing", have Codex counterparts under other headings, and the window added one
Codex-only section, `06874577`'s, whose Claude counterpart is in `CLAUDE.md`. Ben decided on
2026-09-15, during his walk-through of this review, that the closing-message rule is not meant to be
Claude-only: Codex needs it too, and giving Codex's user-level instructions a counterpart is for the
remediation phase. Re-establish: `C_02_headings_compare.py`; for each heading, `git log
--full-history --format="%h %ad" --date=iso-local -S "<heading>" -- dot-claude/user-wide-CLAUDE.md`.

8.12. **Raised; Ben's decision is at the end of this part:
`doc/user-level-config-in-cloud-sessions.md` is classified both ways inside the window.** `3134f32b`
changed one clause in place on 2026-09-12; `1842e784` created its sibling update file on 2026-09-13
and the entry "Inherited item 3: live user-level synchronization is implemented" in
`doc/review-findings-2026-09-10-update.md` calls it one of "two affected finished dated reports";
its lines 110–112 still instruct "Edit the live copy, copy outwards, run both comparisons" and cite
a README section that no longer exists, corrected only in the sibling. Its title and its gating
section describe the present and `CLAUDE.md` sends sessions to it for "the diagnosis"; its body is a
dated record of 2026-09-09 measurements. Ben decided on 2026-09-15, during his walk-through of this
review, that it is a live document, kept true in place; correcting it in place, and correcting its
update file's statement that it is a finished dated report, is for the remediation phase.
Re-establish: `git log --format="%h %ad %s" --date=iso-local 0354b6cc..bca64824 --
doc/user-level-config-in-cloud-sessions.md`.

### 9. Two pointer issues are unsigned and one open issue names a directory the window removed

Stream C.

9.1. **Raised, unfixed: issues #279 and #281 do not say whether they are agent-written.** Each body
is one line naming its plan. Every other issue opened or commented on in the window says so in its
first or last line. Re-establish: `C_01_fetch_issues.py`.

9.2. **Raised, unfixed: #278's body names `leningrad/page-snips/`, which `a8e4790e` removed the
day after the issue was opened.** The example still holds under the two new folders. The issue is
open, and an open issue's body is corrected. Everything else in #278 re-measures.

### 10. Ten guards, invariants and pointers in the window's code, none a defect in shipped data

Streams B and D. Each is a place where a later change would go unnoticed, or a count in an
immutable message.

10.1. **Raised, unfixed at `bca64824`: the worktree sweep's session records do not cover a session
whose work is in a worktree while its recorded working directory is the primary clone, which is
this review's own shape.** `_session_in` (`py/repo_util/git_worktree_cleanup.py:825–840`) spares a
worktree when a running session's `cwd` is the worktree or inside it, or when the desktop register
leases it. Measured 2026-09-14: this session's record says `cwd = C:\Users\BenDe\GitRepos\MAM-basics`
while every command of the review ran in the review worktree, and the desktop register listed no
worktree; so both worktrees of this review printed `session record: None` and were protected only
by the activity hour and the dirty and unique-ignored-content checks. A clean, merged review
worktree idle for an hour would be removed while the session that made it still reads it. H8 of
`doc/PLAN-repo-maintenance-across-GitRepos.md` names Codex threads and the desktop pool as what
the records miss, not this shape; `git worktree lock` is the module's own remedy. Re-establish:
`B_02_worktree_records_dry.py`, `B_10_session_records_liveness.py`.

10.2. **Raised, unfixed at `bca64824`: `test_git_filename_commands_request_nul_delimiters` cannot
see a git call made through a wrapper, so it enforces less than `CLAUDE.md`'s "enforces both
rules" says.** `_literal_command` (`py/tests/test_tracked_filenames.py:42–49`) examines only a
literal list or tuple containing `"git"`; three of the 20 filename-returning calls go through a
wrapper (`git_worktree_cleanup.py:361` and `:491`, `mpplus_revisions.py:158`), all three with
`-z` today, and the lint would not notice one that dropped it. Re-establish:
`B_12_git_filename_calls_any_callee.py`.

10.3. **Raised, not a defect: `mpplus_revisions.resolve()`'s `--full-history` lookup rests on an
invariant it does not check, and one docstring beside it is stale.** The commit it names is
assumed to have HEAD's `MAM-parsed/plus` tree; three throwaway repositories show that holding in
every merge shape, and it can fail only under committer-date skew. A guard comparing the two
trees' hashes would make a report unable to record a hash whose tree is not the one diffed.
`_commit_date`'s docstring in `py/subcommands/diff_mpplus.py:56–68` still says HEAD resolves
through `git log -1 -- MAM-parsed/plus`, which since `9f6ee787` is `--full-history -1`.
Re-establish: `B_05_full_history_demo.py`.

10.4. **Raised, not a defect: the byte identity the deployment relies on rests on
`.gitattributes`' `* text=auto eol=lf`, and nothing in `user_config_sync.py` says so.** `git
archive` applies working-tree conversion, and `core.autocrlf = true` is set for every repository
on this machine; only the tracked attribute makes the archive of `dot-claude/` and `dot-Codex/`
byte-identical to the blobs (a `text eol=crlf` CSV archives 15 bytes longer than its blob). Were
the attribute relaxed, every check on Windows would report drift on every file and a deployment
would write CRLF into all nine destinations. Reading the blobs raw with `git cat-file` would need
no conversion. Re-establish: `D_03_remeasure.py` §7.

10.5. **Raised, not a defect, by design and half documented: inside a tracked destination a
deployment removes every live-only file, and a skill removed from the tracked tree is neither
retired nor reported.** `dot-claude/README.md` says it "replaces complete skill directories" and
the check names a live-only file before any deploy; the converse, that deleting
`dot-claude/skills/<name>/` leaves `~/.claude/skills/<name>/` in place and invisible to every later
check, is undocumented. Nothing outside the nine destinations is ever touched.

10.6. **Raised, not a defect: two writers still write JSON products with a bare `json.dump`,
outside `af1c404a`'s speedup and `file_io`'s temp-file-and-retry.** `py/mb_diff_mpu/mpplus_json.py:113`
(the change-log JSON) and `py/hkq_cmn/qere_ending_search.py:300` (`holman/out/holam_he_qere_report.json`),
both without a trailing newline. Re-establish: `B_04_file_io_byte_identity.py`.

10.7. **Raised, not a defect: a backup or staging directory the deployment could leave behind
would carry a `SKILL.md` directly under a skills root**, named `.<name>.user-config-stage-<hex>`
or `.<name>.user-config-backup-<hex>`; whether Claude Code and Codex skip a dot-prefixed skill
directory is not established. None exists today.

10.8. **Raised, not a defect of the window: `py/main_repo_util.py` does not reconfigure stdout to
UTF-8**, while `py/main_repo_maintenance.py:192–193` does; the deployment's failure branch prints
git's stderr, so a non-ASCII message under a redirected cp1252 stdout would raise after the
failure had already been decided.

10.9. **Raised, not a defect: `fa517040` kept one mock-based example test.**
`test_zero_diffs_writes_empty_unpinned_latest_artifacts` (`py/tests/test_diff_mpplus_unpinned_latest.py:18–46`)
stubs two functions and asserts one call, the shape `CLAUDE.md`'s "Writing tests" section says
not to add; the lint-shaped chain test beside it is the right shape.

10.10. **Raised, a count in an immutable message: `4e007289`'s "the three references in finished
dated records" are five lines in three files** (`doc/PLAN-evacuate-the-rest-of-three-repos.md:1561`,
`doc/PLAN-remediate-review-findings-2026-09-07.md:660–661`,
`doc/codex-review-findings-2026-09-10.md:159–160`), all rightly left as written.

### 11. Six prose defects against the `hebrew-prose` skill and the prose rules, one of them inherited

Stream E, with the skill loaded.

11.1. **Unfixed at `bca64824`, and inherited rather than written in the window:
`doc/lam-2-3-akhla-snips/README.md:69–72` states manuscript facts on UXLC's authority.** "Two
further facts about the same verse, from `../../in/UXLC-39/Lamentations.xml` rather than from the
image: the verse has a meteg on [two named atoms], plus the silluq on the verse-final [atom]. So
the absence on [the atom] sits among three marks present, not on a page sparing with them." The
source is disclosed, but the sentence's subject is the Leningrad Codex's verse and its conclusion
is about the manuscript page, which the rule "A transcription is evidence about the transcription,
never about the manuscript" forbids; it should say that UXLC 3.9 records the three marks and stop.
`a8e4790e` moved the paragraph byte for byte from `leningrad/page-snips/README.md`, so the window
carried it unreviewed rather than composing it. Re-establish: `git show
0354b6cc:leningrad/page-snips/README.md`.

11.2. **Unfixed at `bca64824`: `doc/mega-timing-2026-09-11.md:248` says "the WLC 4.22 prose
books".** The skill: "Prose verses and poetic verses, never prose or poetic BOOKS"; the corpus name
is "the 21 books". The document is a finished dated report, so the correction belongs in a new
`doc/mega-timing-2026-09-11-update.md`, which does not exist.

11.3. **Unfixed at `bca64824`, low: `doc/meteg-after-silluq-snips/README.md:7` promises "Each
section says whose crop it is and which image it was read from", and its two Leningrad Codex
sections do not.** The `leningrad-380A-…` section names neither the cropper nor the image; the
`leningrad-398A-…` section says "Ben's crop, 2026-09-10" and names no image; both rely on the
folder-level statement that Leningrad images come from Sefaria's and the Internet Archive's sets.
The three other sections keep the promise.

11.4. **Unfixed at `bca64824`, low: `py/versification_and_cantillation/strands.py:5`, a line
`2239cbad` rewrote, says "The Decalogue verses carry the מ:כפול (dual-cantillation) template".**
"have" is the word; the same rewrite rightly removed the "upper/lower" glosses.

11.5. **Raised, low, in finished documents: three vocabulary slips the update files would take.**
`doc/review-findings-2026-09-10.md:379` and `:388` say "the plus" for `MAM-parsed/plus/`;
`doc/meteg-after-silluq-snips/README.md` says "the verse-final word" at three lines and "the
verse-final atom" at one for the same kind of thing; `doc/lam-2-3-akhla-snips/README.md:66` and
`:104` spell the edition "Mikraot Gedolot Haketer" where the skill's table has "Mikra'ot Gedolot
ha-Keter", line 62 has "shewa" where the other README has "sheva", and lines 65–66 read "MAM has
no meteg there, as does Mikraot Gedolot Haketer", where "nor does" is meant. All three README
sentences were moved verbatim from the pre-window READMEs.

11.6. **Unfixed at `bca64824`, trivial: `README.md:87` reads "Run tests through the unified
harness (on MS-Windows:):"**, a doubled colon inside the parenthesis, from the window's rewrite of
the root README.

## Open ends the window itself declares (not findings)

`doc/PLAN-retire-google-sheet.md`, `doc/PLAN-retire-codex-index-image-work.md` and
`doc/PLAN-dispose-mega-pipeline-review-findings.md` are `State: live` and unexecuted, tracked on
#279, #281 and #280; `doc/PLAN-deferred-template-projection-decisions.md` is `State: paused
2026-09-12`, tracked on #277; `doc/PLAN-silluq-before-gaya-template.md` is `live` and unexecuted, on
phonetic-hbo#78. `MAM-for-Sefaria/` and `MAM-OSIS/` are declared not kept current since 2026-09-12
by their READMEs, whose commands for regenerating them fail (finding 2.1). The 2026-09-10 review's
update file declares that review's remediation complete, with every finding disposed of and two ends
left open: finding 18.1's archived-log provenance, unverified, and finding 21.8's `.pytest_cache` in
the primary clone, referred to repository maintenance; that review's line 3 and dispositions table
still say otherwise (this review's finding 7.1). Issues #271 to #274, #276 and #278 are open and
assigned to no plan. `main` and `origin/main` stood at `bca64824` when this file was committed.

## What this review did not check

1. Anything in MAM-private or hbofonts: the Phonetic MAM figures behind the post-stress-meteg survey
   `aedac688` regenerated, MAM-private's own census, and the two MAM-private commits named in the
   2026-09-10 review's update-file entry for its finding 7.2.
2. The cloud container itself: the hook was exercised under Git Bash on Windows with `HOME`
   redirected, which tests every path through the script that `53696b30` changed and the copy
   semantics that change relies on, but neither the four other paths that area 1 of "Ben's four
   areas" names nor the container's `bash`, `cp` or environment; and no credential miss was forced
   against the deployment's fetch.
3. The live Google Sheet and the live Hebrew Wikisource: whether the Apps Script run of
   2026-09-10 wrote "Applied 34 auto-edits." into the Sheet, and the editorial correctness of the
   34 auto-edits.
4. The image content of the eight moved crops beyond their bytes being unchanged by the move; no
   manuscript or edition reading was adjudicated.
5. The live user-level homes beyond stream D's comparison; nothing under `~/.claude/projects/` or
   `~/.codex/sessions/` was read, and the Codex-side facts behind the live `~/.codex/AGENTS.md` were
   read only as a hash.
6. The sixty-odd modules `5cb06e25` changed beyond `py/mb_cmn/template_names.py`, against the
   closed-dispatch rule; the 2026-09-10 review's template-projection findings were not redone.
7. The Codex entries' judgments of reproducibility in the update file; only their counts, line
   numbers and blobs were re-measured, and the correctness of their corrected readings was checked
   by stream E for vocabulary, not for substance.
8. `doc/PLAN-retire-codex-index-image-work.md`'s 355 lines and `doc/PLAN-retire-google-sheet.md`
   beyond its first forty, for prose beyond the fresh-session checklist and the banned-term scan;
   and the rendered `gh-pages/` prose outside the one `post-stress-meteg.html` hunk.
9. Whether the six Claude-only sections of the user-level instruction files that the window's diff
   did not change, and the two Codex-only sections that predate the window, are meant to exist in
   one file only (finding 8.11).

## Inputs for the reconciliation with the Codex review

Anchors for comparison: MAM-basics `0354b6cc..bca64824`; the fifteen quiet public repos at the
heads named in "Scope, anchors and census". Each finding above gives the commit, the file and line
as of `bca64824`, the claim, the measurement, and the command or `.novc/review-2026-09-14/` script
that re-establishes it, so a disagreement can be checked by hand without re-deriving the whole
window. Findings 1, 2, 4.2 and 4.3 were derived by the main session, which also read Ben's third
area itself; finding 4.1 is stream E's, and the main session's check found the same three
`post_stress_meteg.py` lines; findings 3.1 to 3.3 are streams A's and E's; finding 5's tree hashes,
counts and Genesis 5:1 example are stream B's (`B_07_plus_tree_hashes.py`), and no script of the
main session measured it; finding 2.1 was found by running the two generators after stream B noted
that they read the incremental folders directly; findings 6, 7.6 and 11 are stream E's, the rest of
7 stream A's, 8 and 9 streams C's and D's, with stream E also finding 8.7's `CLAUDE.md` spellings
and 8.10's census glob, 10 streams B's and D's, each spot-checked by the main
session where a figure could be re-run cheaply (the stale step count by all six readings, the
nonexistent blob, the two replaced blobs, the dead link, the ruff errors, the "its step 7" sentence,
the Codex file's UXLC-utils citations, the 13-file glob). The census, and the tree-health section's
suite, mega, generator and product-tier figures, are the main session's own. The reconciliation
section goes below this one, under `## Reconciliation with the Codex review`, per
`doc/dual-agent-review.md`.
