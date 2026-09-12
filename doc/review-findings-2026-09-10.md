# Findings of the 2026-09-10 review of the public repos since 2026-09-08

State: not yet acted on, except findings 1 to 6, fixed on 2026-09-11 before the Codex counter-argument ran — findings 1 and 2 at Ben's direction, findings 3 to 6 unasked; see `## Dispositions after remediation` at the end

Written 2026-09-10, late evening, as the Claude argument, turn 1 of the standard alternating
dual-agent review under `doc/dual-agent-review.md` (Ben's decision D9 of 2026-09-09): this file was
frozen before any Codex reviewer read it, and the Claude session neither read nor sought a Codex
half (no file named `codex-review-findings-2026-09-10*` exists, and nothing under `~/.codex/` or
`Documents/Codex/` was read beyond a directory listing and, by stream A, the untracked evidence
receipt of the September 8 remediation). Nothing was fixed. The round's shared worktree is the one
D11 names, `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-10` on
branch `dual-agent-review-2026-09-10`, created by this session at the round's start from `main` at
`0354b6cc`; every later turn of both agents and the close-out use it directly, no task fast-forwards
`main` or pushes before the final remediation wave, and the worktree and branch are retired after the
final task ends. The session itself was launched by the desktop app into
`.claude/worktrees/eloquent-ritchie-0e4c6c`, a worktree the app had re-leased from two earlier
sessions; that checkout took no part in the review and holds nothing (finding 21.1). Before this
file was committed, its Hebrew runs were checked with `has_std_mark_order` and any run the
file-writing tool had put into Unicode-normal order was put back with `give_std_mark_order`, which
is the mechanism `CLAUDE.md`'s first section names. The reconciliation goes at the end of this file
under `## Reconciliation with the Codex review` once the Codex counter-argument is stable, and the
dispositions under a later `## Dispositions after remediation` section, per that document.

## Scope, anchors and census

Sixth review under the public-repos-only scope. It covers committed work from the 2026-09-08
review's anchor through the moment this review started, 2026-09-10 about 22:43 local, when
MAM-basics' HEAD was **`0354b6cc`** (2026-09-10 22:20, "meteg-after-silluq-in-uxlc-and-wlc: NO
POINTER INTO ANY .novc DIR REMAINS, at Ben's word"), the primary clone's tree was clean and
`origin/main` stood at the same commit. **The tree moved under the review, five times by 23:40,
all outside the window**: at 22:56 `e7a1736b` ("Worktree sweep: read Claude Code's session
records; override per worktree only", five files, 336 insertions) landed on `main` and
`origin/main` from the primary clone, and between 23:13 and 23:38 `a7586b4b`, `44479798`,
`9dd066ad` and `e84e2c70` followed (the Wikisource–Google Sheet differences refreshed, the Sheet
refreshed after the auto-edits, surveys declaring template projections, every template dispatch
made closed; 18 files against `e7a1736b`). They are the first commits of the next window and were
not reviewed; the shared worktree stayed at `0354b6cc` throughout, and every figure below is
measured there. The sweep `e7a1736b` describes
also retired, at about 22:56, the two Codex worktrees that were live and clean at the start —
`C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics` on `codex-worktree-3a6b` at `a0a2e3ab` and
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08` on `codex-review-2026-09-08` at
`9d1de074`, both already merged into `main` — and deleted both branches, so `git worktree list`
named five checkouts at 22:43 and three at 23:10, and stream B1, starting at 22:52, found neither
branch name in any ref.

Anchors (start → end) and counts, re-measurable with
`git -C C:/Users/BenDe/GitRepos/<repo> log <start>..<end> --oneline`, or with
`gh api "repos/bdenckla/<repo>/commits?since=2026-09-09T01:49:00Z"` for the repos read on GitHub:

| Repo | Range | Commits | Non-merge |
|---|---|---|---|
| MAM-basics | `38a606e2..0354b6cc` | 249 | 218 |
| MAM-OSIS (GitHub, redirect host since 2026-09-10) | `26a7e85f`, `8df241b3` (15:11Z, 15:33Z) | 2 | 2 |
| phonetic-hbo | `10de7970` (2026-09-09 21:56Z), clone clean at it | 1 | 1 |

That is **252 commits across three public repos**. Thirteen public repos were quiet: the Taamey_D
clone (clean, `main` at `origin/main`, `3813499`), and on GitHub MAM-simple, MAM-parsed,
MAM-with-doc, MAM-for-Sefaria, codex-index-aleppo, codex-index-cam1753, codex-index-leningrad,
diffable-pointed-hebrew, book-of-job, holman-ketiv-qere, UXLC-utils and wlc-utils
(codex-index-cam1753, codex-index-leningrad and diffable-pointed-hebrew archived). Two clones are
private and fall to the private series: MAM-private (22 in-window commits, none read; the clone is
clean at `ecab726` with `origin/main` there too) and hbofonts (0). github-misc has had no clone on
this machine since 2026-09-09, and the series' one standing exception, its instruction-file
byte-compare, is spent as `doc/dual-agent-review.md` records, so it was not applied; the twelve
files it reached are tracked here at `dot-claude/` and `dot-Codex/` and were read like any other
tracked file (stream D).

Of the 249 MAM-basics commits, 247 are authored Ben Denckla and **2 are authored
`Claude <noreply@anthropic.com>`** — `73ab8383` and `036deb92`, the prose mark-order commits, made
by a cloud session (each carries a `Claude-Session:` URL trailer beside its `Co-Authored-By`) and
pushed as `origin/claude/charming-mayer-xknwcw`, which `b490988a` merged and which still exists on
the remote (finding 21.4). The trailers are spelled four ways: `Co-Authored-By: Claude Opus 5
<noreply@anthropic.com>` 122, `Co-Authored-By: Codex <noreply@openai.com>` 84, `Co-Authored-By:
Claude Fable 5.1 <noreply@anthropic.com>` 10, and a new one, `Co-Authored-By: Codex
<codex@openai.com>` 7. 26 commits carry no trailer, and all 26 are `Merge branch 'main' into
<branch>` merges (25 of them subject-only); the other five merges — `4008737d`, `bccc6ad5`,
`8f5c1c96`, `b490988a`, `0c2b0eda` — carry one. 31 commits are merges, 218 are not, and 69 sit on
`main`'s first-parent line, because the window's work ran on thirteen branches: the twelve the
merge subjects name — `codex-review-2026-09-08` (which merged `main` thirteen times),
`codex-worktree-a3ff`, `codex-worktree-3f99`, `codex-worktree-3a6b`, `claude/mega-coverage` and
seven `claude/<adjective>-<name>-<hex>` branches of desktop-app sessions — and the cloud session's
remote branch. Seven of the 31 merges carry a conflict resolution that differs from both parents
(`git diff-tree --cc --name-only <merge>`): `8f5c1c96` in ten files (`py/main_0_mega.py`,
`py/mb_cmn/paths.py`, `README.md`, `py/tests/test_prose_mark_order.py`, `py/main_download.py` and
five more), `b490988a` in `CLAUDE.md` and three docs, `5f996d0e` in `aleppo/README.md` and
`leningrad/page-snips/README.md`, `30fb7681` in `py/repo_util/git_worktree_cleanup.py`,
`4008737d` in `py/main_uxlc_estimate_atom_loc.py`, `bccc6ad5` in `py/main_download.py`, and
`c7df66d0` in `doc/review-findings-2026-09-08.md`, where the branch's `ad44dba7` (the 143 → 122
correction to that review's State line) met `main`'s `5636d38a` (the reconciliation table); both
survive in the file at `0354b6cc`.

The window changed **1,677 paths** between its endpoints — 247 added, 824 deleted, 571 modified,
35 that `git diff -M` pairs as renames — taking the tree from 5,512 to **4,935** tracked files,
1,216 to **1,088** `.py`, `gh-pages/` 1,763 to 1,790 files (576 to 577 HTML, the deploy root eleven
to eleven), `doc/*.md` 57 to **82**, `doc/PLAN-*.md` 13 to **21**. Of the 35 rename pairs, 14 are
the Job quirk records renamed by chapter under `py/author_boj_qr/`, and 21 pair the new
`MAM-parsed/google/` files with deleted `MAM-parsed/historical/<sha>/plus/` files at 52 to 63 per
cent similarity — rename detection reporting a resemblance, not a move: the google files were
written by `05cfc018` from `in/mam-go/` and are byte-identical to `MAM-parsed/plain/` at that
commit (stream B2). By top-level directory: `uxlc/` 516 (477 deletions and 36 additions, the
per-note UXLC files consolidated by book), `py/` 362, `MAM-parsed/` 178, `MAM-simple/` 172,
`MAM-for-Sefaria/` 95, `in/` 70 (39 of them the deleted `in/mam-from-sefaria/`), `doc/` 69,
`gh-pages/` 62, `MAM-OSIS/` 59 (all additions), `out/` 45, `aleppo/` 15, `dot-claude/` 9,
`leningrad/` 7, the root 6, `dot-Codex/` 4, `holman/` 3, `.claude/` 2, `MAM-with-doc/`, `cam1753/`
and `misc/` 1 each. The 824 deletions are dominated by five trees: `uxlc/in/UXLC-notes/` 477,
`py/author_boj_qr/` 146 (with 25 additions, the Job records consolidated by chapter),
`MAM-parsed/historical/<sha>/plus/` 123 (six release trees replaced by six `.zip` files),
`in/mam-from-sefaria/` 39, and the Wikisource-index generators with their outputs (`py/ac_wiki/` 4,
`py/lenin_wiki/` 6, `aleppo/aleppo-wiki/index*` 3 and J. David Stark's CSV, `leningrad/lenin-wiki/`
3, `aleppo/plot_col_coords-out/` 3); ten single programs went with them (`py/main_uxlc_mega.py`,
`py/check_ac_word_finding.py`, `py/main_source_hygiene.py`, `py/main_verify_meteg_vs_mgketer.py`,
`py/main_gen_aleppo_crop_editor.py`, `py/main_ac_kraken_seg_baselines.py`,
`py/main_ac_plot_col_coords.py`, `py/main_ac_wikisource_page.py`, `py/main_lenin_wikisource_page.py`,
`py/lenin_paths.py`), plus `misc/zarqa-table-diff/make-dph-files.ps1` and
`aleppo/test-data-from-book-of-job.json`.

The window's substance is five things. 1. The close-out and remediation of the 2026-09-08 review —
turns 2 to 5 of the exchange, steps 1 to 6 of `doc/PLAN-close-out-review-2026-09-08.md`, and Waves
1A to 4 of `doc/PLAN-remediate-review-findings-2026-09-08.md`, about 60 commits on the Codex review
worktree, integrated by fast-forward at `9d1de074` on 2026-09-10 09:36. 2. The instruction-file
consolidation of 2026-09-09 — `dot-claude/` and `dot-Codex/` made canonical here (`74d883d2`), the
cloud-session hook (`6d19c34a`), the prose mark-order lint and the 132 clusters it found
(`73ab8383`, `036deb92`, `b490988a`), github-misc leaving the roster (`63ac5b84`), the four edition
transcriptions repaired (`10a5c307`) — about 30 commits. 3. The meteg-after-silluq investigation —
the screen and the documentation search of 2026-09-09, the Koren lookups, Job 4:12 and Psalms 72:15
with their four manuscript crops, `aleppo/page-snips/` started, `py/main_verse_links.py` and the
verse-links skill, and `doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md` executed — about 45 commits
ending at the anchor. 4. The mega-coverage plan, phases 1 to 8 of `doc/PLAN-mega-coverage.md` — the
coverage check, the dead-code deletions, the twelve generators of tracked files added to the mega
plus the five folded in from `py/main_uxlc_mega.py`, `repos_root()` made worktree-aware, the
MAM-private rule — about 45 commits on `claude/mega-coverage`. 5. On three Codex worktrees, the
cutover of the MAM products from the Google Sheet to Wikisource
(`doc/PLAN-wikisource-derived-mam-products.md`, `doc/PLAN-efficient-wikisource-downloads.md`),
Phase 6 of the five-products evacuation, MAM-OSIS's Phase 5 landing, and the worktree file
consolidation — about 40 commits.

The review ran as five agent streams plus the main session: (A) the September 8 close-out and
remediation records; (B1) the mega-coverage plan and the deletions; (B2) the Wikisource cutover,
Phase 6, MAM-OSIS and the consolidations; (C) the meteg-after-silluq documents and the Koren
lookups; (D) the instruction-file and configuration work. Every script and output is untracked under
`.novc/review-2026-09-10/` in the shared worktree, prefixed `A_`, `B1_`, `B2_`, `C_`, `D_` per
stream, unprefixed for the main session (whose scripts were copied there from the session
scratchpad before this file was committed), each stream's own report beside them as
`<stream>_report.md`.

## Tree health at `0354b6cc`: green, with the suite at 992

- Suite: **992 passed, 5 skipped, 65 subtests passed** (217.93 s), run in the shared worktree with
  `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider`
  and **no `REPOS_ROOT` set** — the first review run to rely on `516a4a1a`'s worktree-aware
  `repos_root()` — with the tree clean before and after. The chain from the last review's 983 by
  `def test_` count (stream A, `A_11_test_counts.py`): 753 at `becc6f00`, 757 at `dd86c96f` (+3
  `test_graphviz_version_pin.py`, +1 `test_prose_mark_order.py`), 758 at `f1166057` (+1
  `test_post_stress_meteg_annotations.py`, the 988 `CLAUDE.md` dates 2026-09-10), 761 at
  `0354b6cc` (+3 `test_mega_coverage.py`, +1 `test_wikisource_plan_corpus.py`, −1
  `test_mb_cmn_paths.py`), with 39 `parametrize` decorators throughout, which predicts 991; the
  run reports 992, and the one-item difference was not chased. `e7a1736b`'s message, outside the
  window, records the same 992. The window's own messages report 983, 984, 987, 988, 989, 990 and
  992 at their trees (stream D).
- `ruff check py` clean; `black --check py` clean at **1,039** files (1,167 at the last review; the
  128 fewer are the window's deletions under `py/`).
- Zero `sys.path` mutations in tracked `.py`: the grep's 30 matches are docstrings, comments and
  `check_repo_standards.py`'s rule text.
  `--check-repo-standards --workspace-file all-repos.code-workspace --visibility public` (run with
  `--repos-root C:/Users/BenDe/GitRepos/MAM-basics`, the spelling that resolves the workspace
  file's `.` entry from a worktree) sweeps 3 repos, the roster having lost github-misc and MAM-OSIS
  in the window: MAM-basics linked_worktrees **2** (this round's and the re-leased
  `eloquent-ritchie-0e4c6c`, the two Codex worktrees having gone at 22:56), agent_branches **1**
  (`claude/mam-basics-review-stage-1-72e903`, the branch the desktop app made in the re-leased
  worktree; the remote-only `origin/claude/charming-mayer-xknwcw` is an ancestor of `main` and
  reportable only by `--clean-worktrees`, which was not run), HEX_ESCAPES 80 and NFC_H_DOT 30 as at
  the last review, NFC_LATIN **39** (49 last time; the UXLC-notes consolidation folded the per-note
  sites into `uxlc/in/UXLC-notes/2Kings.json:12` and `Genesis.json:6`, and
  `MAM-parsed/google/BA-Samuel.json:26553` is a new site); Taamey_D GITATTRIBUTES_LF=False as
  before; phonetic-hbo reports one linked worktree of its own, not read (`standards-public.txt`).
- Mark order over the lines the window added to 712 files of prose, code and data outside the
  trees `CLAUDE.md` exempts (1,683,363 Hebrew runs): **20 runs not in MAM-normal order, all on
  lines of the landed MAPM originals** — `MAM-OSIS/MAPM-orig/MAPM.xml` 10,
  `MAM-OSIS/MAPM-orig-24/Deut.xml` 5, `Exod.xml` 3, `Num.xml` 1, `Song.xml` 1 — byte-verbatim
  captures of the OSIS source that the landing's blob proof requires be left as they are; and,
  in the consolidated `uxlc/in/UXLC-notes/*.json` that the main session's scan skipped, **73
  runs** on added lines that stream A found, UXLC's own text stored byte-verbatim by `09d00880`.
  Both trees are expected and neither is in `CLAUDE.md`'s exemption list (finding 4). Whole-file,
  110 pre-existing runs in 17 files, 62 of them in `gh-pages/MAM-for-Sefaria/index.html` and the
  rest in seven `py/` modules and two MAM-parsed HTML pages, the same class the last three reviews
  left unexamined (`mark_order_window_scan.py`, `A_10_mark_order_added_lines.py`). Stream D's
  tree-wide scan is finding 4.
- Whitespace on the window's added lines (`git diff --check 38a606e2 0354b6cc`, the range form
  that flags added lines only): 43 sites, 42 of them the trailing tab and blank last line of each of
  the 21 landed `MAM-OSIS/MAPM-orig-24/*.xml` that have one (byte-verbatim, expected), and one
  authored: `doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md:552`, a blank line at EOF
  (finding 20.10).
- Markdown links: 265 relative links in 210 tracked `.md` files, **3 dead**: the pre-existing
  `misc/what-is-mam/img/provenance-misc.md:6`, and two the window added by tracking Ben's user-level
  instructions, `dot-claude/user-wide-CLAUDE.md:1275` and `dot-Codex/user-wide-AGENTS.md:1061` —
  the illustrative `[page](gh-pages/accgram/page.html)` of the "Showing me a local file" section,
  which is an example of the wrong link rather than a link, and which a checker cannot tell apart
  (`md_links_check.py`; finding 20.11).
- `py/check_html_syntax_and_sanity.py` over the deploy root: "No HTML output issues found".
- Pages: all **66** MAM-basics deploy runs created in the window were disposed of as the
  concurrency setting intends — 65 succeeded and the one for `3b0225e0` was cancelled by the run for
  `becc6f00` 75 seconds behind it; MAM-OSIS's two runs (`26a7e85f`, `8df241b3`) succeeded
  (`gh_census.py`).
- Issues: five opened in the window, #266 to #270, none closed, 101 open. #266 (Psalms 4:3, a
  deḥi stress helper) and #267 (Psalms 71:9, the helper moved) were filed by a Claude session with
  Ben on 2026-09-09 and each answered by skadish1 with "Fixed" and a Wikisource diff link at 22:05Z
  and 22:09Z that evening; the 2026-09-10 refresh (`209b4c05`) brought both edits into
  `in/mam-ws/D1-Psalms.json`, and both are in `MAM-parsed/plus/D1-Psalms.json` and `plain/` at
  `0354b6cc` (`issues_266_267_check.py`); the issues themselves do not yet say so (finding 21.6).
  #268 (Claude, 2026-09-09), #269 (Claude, 2026-09-10, opening on Ben's words) and #270 (Codex,
  2026-09-10) each say in their first line that they are agent-written, as the global rule asks; #266
  and #267 say so in their last.

## What verifies sound, stream by stream

**The September 8 close-out and remediation (stream A).** Every disposition the record calls fixed
that public evidence can check holds at `0354b6cc`, with the exceptions under findings 3, 8 and 13.
Finding 2's 210 whitespace findings are gone: a byte scan of the 232 files under the named trees
finds 0 blank final lines and 0 files without a terminating newline, the four named files have 0
trailing-whitespace lines, and the historical 87 / 111 / 12 in 80 / 111 / 2 files re-derive from the
blobs at `38a606e2`. Finding 5.1b is fixed: an `HTMLParser` walk finds 0 Hebrew-holding cells
without effective `dir="rtl"` on either Holman page (578 and 724 cells, 163 and 119 with Hebrew),
`c2f238f2..f709e0b8` adding a net 49 and 1 attributes and swapping one label. All eleven
deploy-root pages render byte-identically from the tracked `out/accgram/post-stress-meteg.json`
(`9b2ebdf4…`) into scratch, `pin_claims` and the annotation validator raising nothing (1,017
`_hebrew_cell` calls on 674 inputs, `source_marks_checked` 0 on every page). V6 held: between
`c2f238f2` and `931d6762^` the only HTML that changed under `gh-pages/` is Wave 2's four declared
files, and every HTML hunk of `931d6762` is E2 (4 + 9 + 1 `romanized` spans), E3 (`<ul>` to `<ol>`)
or E8 (the Aleppo sentence), its non-HTML hunks E1 and E4 to E7 verbatim; the three pages' hashes
are the contract's. Finding 15.1 has zero unwrapped mark names in visible text; finding 6's eight
sites read eleven / nine / 35 or carry a dated note; finding 7's two plans have `State:` lines and
the standard's docstring is corrected (11 / 11 at `9cf48863`, 13 / 11 at `38a606e2`, 16 / 16 at
`9d1de074`); findings 8, 9, 10 and 11 have their dated corrections at the 24 sites the record
names; finding 12's vendoring artifacts reproduce in memory and to scratch (44 `identical`, 4
inventory rows, all 115 audited entries `i/lf w/lf`); finding 13.3's mark-preserving display,
matching-only transformation and all-page validator are in the tree; finding 14.2's lint now reads
the page set off `vars(site_data)` and the rendered glob; D2's sentence is byte-identical in all
three skill homes; D4's two notes, D6's "Ben Denckla's hand corrections" and N6's row are present;
D8's 35 was true at `9d1de074` (index `<a ` 36). `9d1de074` reached `main` by fast-forward
(`main@{32}` in the shared reflog), and the untracked receipt the record defers to records both
checkouts clean, the `--ff-only` over 244 files, the push, and a final suite at `9d1de074`. All 17
"Executed <date>: commit <id>" lines of the close-out plan name commits that exist and touch what
they say; the five 40-hex ids that resolve to nothing here are foreign by design. Mark order on the
2,045 added lines holding Hebrew in the 40 scope files: 0 failures outside `uxlc/in/UXLC-notes/`.

**The mega-coverage plan and the deletions (stream B1).** `_STEPS` has 60 `StepRecord`s by AST
and by import; the coverage check's arithmetic closes at `0354b6cc` (142 program keys = 92 files
with a `__main__` block, 81 whole programs and 61 subcommands; 62 run by 59 of the 60 steps; 100
declarations, 80 whole and 20 modes; nothing neither run nor declared, nothing both), every mode
key's flag is defined and all 47 cited paths exist, and `test_mega_coverage.py` passes (3 tests); 26
reasons begin "Claude-written, accepted by Ben on 2026-09-10", which with the two dropped
`--foi`/`--single-threaded` entries are the plan's 28. The counts in the deletion commits re-derive:
26 library modules lost their `__main__` blocks (15 + 6 + 5), five dead programs and eight files
went with `5f35dea3`, nine unused names with `15822344`, six generators joined with `a153ccb5`, and
`985262e2`'s 64 deletions and 20 edits are as its message says. A sweep of 3,603 tracked text
files for 55 deleted names finds every surviving mention in a dated record, apart from findings
19.1 and 19.3. `516a4a1a`'s `repos_root()` resolves to `C:/Users/BenDe/GitRepos` from the worktree
by reading the worktree's `.git` file and the `commondir` beside its gitdir, an empty `REPOS_ROOT`
reads as unset, a wrong one is honoured and named by `require_sibling`. `3a1ab7f0` holds: the nine
post-stress-meteg pages render byte-identically with `REPO_MAM_PRIVATE_DIR` pointed at a directory
that does not exist and zero calls to either Phonetic MAM accessor, and every remaining
MAM-private read in `py/` is unconditional on its path. The cloud skips fire on
`CLAUDE_CODE_REMOTE == "true"` alone, print at the step and again at the end, and never on a missing
sibling; the suite's only `pytest.skip` is the edition transcriptions' semantic channel (the 5
skips). `dot -V` is the pinned 16.0.0 (20260814.1018); `MAM-process.dot.svg`, `pipeline.dot`,
`pipeline.svg` and all four vendoring outputs regenerate to scratch byte-identically; 14 of 15
tracked SVGs are stamped at the pin and the fifteenth is the declared exception. `git ls-files
--eol` in the worktree has no `i/crlf`, and 0 of the primary clone's 3,395 LF-attributed paths hold
CRLF bytes on disk. `9fa80e11`'s handler maps the narrow-sense paseq template to U+05C0 plus a
space, its only consumer being `out/diff_ctr_mam.json`, whose six one-line changes are the commit's.
`5a07e5af`'s stranded-branch report fetches `+refs/heads/claude/*` with
`credential.interactive=false`, `GIT_TERMINAL_PROMPT=0` and a 30 s timeout and reports a failed
fetch as a stale basis. The Codex branch-naming rule lives in `dot-Codex/user-wide-AGENTS.md`
lines 90 to 98 and the live copy is identical. The 15 largest messages match their diffs, apart from
findings 16.1 and 20.8.

**The Wikisource cutover, Phase 6, MAM-OSIS and the consolidations (stream B2).** Every
consolidation preserves every byte: the six historical zips' 144 members equal the `38a606e2`
blobs and `manifest.json` in id, size and set, with the plan's six archive hashes and its
84,572,003 member bytes; the 477 UXLC note pages equal the 36 per-book JSON strings byte for byte
(925,517 bytes, the plan's digest); the 160 Job quirk records give identical per-record digests and
the plan's whole-sequence hash from the old and the new `py/`. `MAM-parsed/google/`'s 24 files
equal `MAM-parsed/plain/` at `05cfc018`. `has_std_mark_order` over every string of
`MAM-parsed/plus` (193,300), `plain` (240,875), `google` (240,855), `MAM-for-Sefaria/csv` (46,802
cells) and `MAM-simple/xml-vtrad-mam` (84,121): 0 violations; `check_mpplus` over the 24 plus
files: 0 errors. The product diffs are fully accounted for: 23 verses in `plus` and `plain` (21
text, 2 reorder-only), 3 of them the Phase 2 accounting in `review-differences.json` and 20 the
refresh's chapters at the plan's line numbers, 12 verses in `MAM-simple/xml-vtrad-mam` and 12
lines in `MAM-for-Sefaria/csv`. `in/mam-ws-revisions.json` has 39 books and 929 records whose
hashes, titles, page ids and revision ids all check (909 at `b2052ab9` with the Phase 3 file hash,
929 at `209b4c05`); one read-only `prop=info` query for Genesis 1 returned the recorded page id and
revision; `ws_revision_api.py` raises on every malformed or partial response and re-fetches on a
hash mismatch, and no test touches the network or skips (27 passed over the four related files).
The MAM-OSIS landing is what `in/mam_osis_land_manifest.json` says: 92 entries, 90 selected, all
source blob ids equal to the GitHub tree at `697dc98a`, 78 of 90 destinations still at the manifest
blob and the 12 others explained; the redirect host at `8df241b3` has six files; the OSIS product
(24 `MAPM-24/*.xml`, `mapm.osis.xml` at 6,800,717 bytes, `index.html`, the CSS) regenerates to
scratch byte-identically; `DATA-LICENSES.md`'s three MAM-OSIS rows say what `LICENSE.md`,
`readme.txt` and `provenance.txt` say. All the Phase 6 inventory figures re-derive (5,649 / 5,646 /
4,949 / 5,642 tracked files, 340 target published files, 144 stubs and 139 pairs), the two rosters
list five repositories, and `wsgo_go.py` reorders Hebrew by combining class and reaches
`unicodedata.normalize` only for a cluster with no Hebrew. The 15 largest messages match their
diffs, apart from findings 1, 2 and 6.

**The meteg-after-silluq documents and the Koren lookups (stream C).** The plan's run re-derives
exactly from `MAM-simple/json-vtrad-bhs`, `in/UXLC-39/*.xml`, `out/wlc422-u/` and `out/wlc420-u/`:
23,213 verses on both sides, the passes 23,066 / 23,062 / 23,062 whole, 24 / 28 / 28 final-atom,
121 / 121 / 121 aligned, class 1 hits 4 + 1, 3 + 1, 3 + 1 with Psalms 60:10 the aligned-pass member,
every letter position of sections 3 to 5, and the syllable columns under the doc's ownership rule.
The screen's seven classes at `0354b6cc` are the doc's with class (i) one lower and (vi) one higher,
exactly the 2 Chronicles 26:15 change the refresh made. The 1 Kings 14:14 change record is as cited
(`uxlc/in/UXLC-misc/2022.12.07 - Changes.xml:4524–4568`). Every link and estimate in the three
docs reproduces from `py/main_verse_links.py` (folios 159A, 195B, 377B, 379B, 380A, 398A with
their columns and lines). The Job doc's leading-meteg figures re-derive (40,709 atoms with a U+05BD,
873 with U+05BD U+034F, 727 leading metegs, the 146 others, the vowel split, the 31-row table). 143
became 122 for the reason `ad44dba7` gives: 21 (verse, form) pairs where a one-meteg non-final form
occurs twice in one prose verse, and the FOI oracle reconciles (135 two-meteg chanted words − 10
MAS-with-MBS − 3 Decalogue forms = 122); every surviving 143 / 12,828 / 14,614 is a dated record
carrying its correction. The tracked `foi-mtgmtg.json` reproduces independently (717; 354 / 228 /
19 / 102 / 14). The Koren doc's 392 rows are internally consistent and match the JSON's 11
readings and the FOI; the search doc's countable figures and the scan-pages probe's ten records
re-derive; the empty-cell doc's loader-independent figures re-derive; 35 line-number anchors hold.
Every manuscript claim sits beside a tracked crop whose README names its source, and no sentence
states a Leningrad reading on UXLC's or WLC's authority. Mark order is clean over 8,180 Hebrew runs
in 27 scope files and 1,030 on the nine pages. The verse-links skill's three homes are
byte-identical. `2e1e8516` ("still the only one found", about MAM) and `f3c1898a` ("5 class 1
hits", transcriptions recording a mark later than MAM's last) do not conflict. `.novc` pointers
are gone from the five files `6ca009a5` and `0354b6cc` name.

**The instruction-file and configuration work (stream D).** No drift at any home:
`dot-claude/user-wide-CLAUDE.md` (106,942 bytes) equals `C:/Users/BenDe/.claude/CLAUDE.md`,
`dot-Codex/user-wide-AGENTS.md` (89,044 bytes) equals `C:/Users/BenDe/.codex/AGENTS.md`, the five
`hebrew-prose` files and `verse-links/SKILL.md` are identical across the worktree, the primary
clone, `~/.claude/skills/` and `~/.agents/skills/`, and the two Codex-side skills across their three
homes; `dot-claude/README.md`'s and `dot-Codex/README.md`'s comparison commands, run verbatim, all
pass. The hook runs on `SessionStart`, exits before any read unless `CLAUDE_CODE_REMOTE` is exactly
`true`, copies only what is absent, and prints one of four banners, matching
`doc/user-level-config-in-cloud-sessions.md` on every point but finding 20.7's one word.
github-misc is out of both rosters (7 → 6 → 5 folders and keys), and all 169 surviving mentions in
36 files are historical citations, descriptions of the move, or the plan's correct `gh api` and
`git clone` instructions. The prose lint covers 224 files (210 `.md`, 2 `doc/*.html`, 12
transcription `.txt`), fails rather than skips on an absent file, and finds 0 offenders; "132
clusters in 16 prose files" reproduces exactly at `38a606e2` and the four transcriptions' 7 at their
four comment lines; the lint-scope figures in five messages reproduce. The three mam-ws trees hold
172,018 offending clusters each, file for file. 39 of the 43 paths `CLAUDE.md`'s changed sentences
name are tracked and the 4 untracked are the ones it says were deleted. The instruction-file plan's
`State: live … nothing acted on` is accurate: all 40 anchors of its 29 items are still in place. Of
the 249 commits, exactly 2 are authored Claude and all 218 non-merge commits carry a trailer.
`23d33437`'s three edits are where it says; the edition transcriptions are nowhere called captures
that may not be edited, and Ben's 2026-09-09 decision is recorded in the lint's docstring where the
exemption used to be.

## Findings

In rough order of consequence. Nothing was fixed. Line numbers are as measured at `0354b6cc`.

1. **Code defect, unfixed: `py/main_diff.py mpp` raises at `0354b6cc`, so the mega's `diff-mpp`
   step fails and the change log cannot be regenerated.**
   `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpp --old 9ce6ee5
   --new HEAD --output <scratch>` exits 1 with
   `mb_diff_mpu.mpplus_verify.VerificationError: 1 diff(s) failed roundtrip verification; no JSON
   or HTML report was written` after "193 raw changes found" (stream B2, `B2_17_misc_claims.py`;
   reproduced by the main session, exit 1, tree clean after). The failing diff is Isaiah 24:18,
   category `meteg-addition`: the refresh `209b4c05` put a meteg before the accent in the verse's
   first cluster (old U+05D5 U+05B0 U+05A0, new U+05D5 U+05B0 U+05BD U+05A0), and
   `py/mb_diff_mpu/change_ops_apply.py:91–97 _apply_mark_added` reconstructs a `MarkAdded` op by
   `marks.append(op.char)`, giving U+05D5 U+05B0 U+05A0 U+05BD, which
   `py/mb_diff_mpu/mpplus_verify.py:62–74` rejects; `py/subcommands/diff_mpp.py:119–126` then
   raises before writing anything. `_apply_mark_moved` (`:100–113`) and the fallback of
   `_apply_mark_replaced` (`:125`) append the same way, so the defect is the class: a `MarkAdded`
   op records the letter and the mark but not the mark's position among the cluster's other marks,
   and MAM order fixes that position only for the shin dot, sin dot, dagesh and rafe. `run_all`
   (`diff_mpp.py:140–154`) reaches `run_unpinned_latest` after the five named releases, so `--all`
   fails too, and `py/main_0_mega.py:343–344` registers `diff_mpp.run_all` as step `diff-mpp`.
   Re-establish with the command above, or `B2_09_unpinned_latest_stale.py`.

2. **Stale generated artifact, unfixed: the tracked change log describes the plus as it stood
   before the refresh.** `gh-pages/MAM-with-doc/change-log/unpinned-latest.json:5` says
   `"diff_count": 57` with `"new_rev": "HEAD"`, and `unpinned-latest.html` and `index.html` carry
   the same count; recomputing `9ce6ee5 → HEAD` in memory gives 69 records, the 12 missing verses
   being Joshua 19:8, 1 Samuel 1:6 and 22:22, 2 Kings 6:23, Isaiah 22:5, 24:18, 42:24 and 50:7,
   Zephaniah 3:13, Psalms 4:3, 2 Chronicles 26:15 and 28:19 — exactly the refresh's text changes
   (`B2_09_unpinned_latest_stale.py`; the main session confirms that the tracked log's only Isaiah
   entry is 23:12 and its Psalms entries are 14:1, 27:13 and 34:10, `changelog_verses.py`). Cause:
   `mpplus_revisions.resolve("HEAD")` reads `git show HEAD:MAM-parsed/plus/…`, so the mega run
   behind `209b4c05` compared the committed pre-refresh plus and left the three change-log files
   untouched (they last changed in `321b2eeb`); the commit message "regenerate the complete
   pipeline" is therefore not true of the change log, and finding 1 now blocks regenerating it.

3. **Outdated written account, unfixed: finding 13.3's "Fixed" disposition describes a display
   fallback that `3a1ab7f0` retired three hours after the fast-forward at `9d1de074`, and no
   dated note says so.**
   `doc/review-findings-2026-09-08.md:1054` ("both fallback sites select unannotated source
   text") and `doc/PLAN-remediate-review-findings-2026-09-08.md:1952–1956` ("Both `mam_form or
   chanted_word` sites now select the snapshot's unannotated form when the MAM form is absent")
   describe `f1166057`'s design, and the final table at `:1166` calls 13.3 "Fixed … Unannotated
   selection, matching and annotation validation pass the retained technical proofs." At
   `0354b6cc` the author module has no `mam_form or chanted_word` site: `_mam_form`
   (`py/author_site/post_stress_meteg.py:2079–2096`) raises `SurveyProblem` on a displayed survey
   entry with no `mam_form`, its docstring saying "RENDERING NEVER READS MAM-PRIVATE";
   `_snapshot_unannotated_form`'s docstring (`py/accgram/post_stress_meteg.py:2361–2365`) says
   nothing outside that module calls it; and `CLAUDE.md`'s section "A code path reads MAM-private
   every time it runs, or never" names this fallback as the case that produced the rule
   (`3a1ab7f0`, Ben, 2026-09-10 12:21). The other three parts of the 13.3 remedy hold. A reader of
   "Fixed" at `:1166` is sent to code that no longer exists. Re-establish: `git show 3a1ab7f0
   --stat`; `Grep 'mam_form or chanted_word' py/author_site/post_stress_meteg.py` (no match).

4. **`CLAUDE.md`'s mark-order section, unfixed: its tree-wide figure is off by a factor of three
   and its exemption list is short by three trees, and 51 `.py` files hold clusters no lint
   covers.** Lines 28–35 (`036deb92`, freshened by `5e7f0d6b`) say "A tree-wide scan finds some
   200,000 clusters in the other order and every one is expected", then name the trees. Measured
   at `0354b6cc` over all 4,935 tracked files: **699,940** offending clusters. Four items:
   1. The three named mam-ws trees account for 516,054 (172,018 each), and a fourth
      byte-count-identical copy of the download, `out/mam-ws-bot/proto-fmt-2/` (39 files, 172,018
      clusters), is named nowhere in the section.
   2. **7,247 clusters in 152 files sit outside every tree the section names**: `uxlc/` 3,890 in
      40 files (`uxlc/in/UXLC-misc/`, `uxlc/in/UXLC-notes/`, `uxlc/in/UXLC-rest/`,
      `uxlc/out/UXLC-misc/`), `in/accgram/` 1,431 in 3 (`printed_decalogue_teamim.json` 1,404),
      `out/accgram/` 702, `gh-pages/` 334 in 31, `in/UXLC-misc/` 178, `in/mam-ws-bot-edits/` 20,
      `MAM-OSIS/MAPM-orig*/` 20, `in/mam-go/` 8, `in/chabad-ctr/` 4, and `py/` (item 3). The
      "some 200,000" appears to be a scan of `in/` alone (178,181), which is what `73ab8383`'s
      message describes (`D_04_treewide_scan.py`).
   3. **51 tracked `.py` files hold non-MAM-normal clusters** — 656 clusters by stream D's count,
      292 Hebrew runs by the main session's (`py_cluster_spotcheck.py`), the same 51 files —
      headed by `py/author_misc/he_ws_intro_to_mam_pasleg.py` (134 clusters), `he_ws_intro_to_mam_gray_maqaf_1.py`
      (28), `py/ws/ws_bot_edit_old_joshua_meteg.py` (23), `he_ws_intro_to_mam_pasleg_footnotes.py`
      (13), `py/foi/sec_yyy_qualifier.py` (13), `py/accgram/breuer_word_length.py` (12),
      `py/versification_and_cantillation/strands.py` (12), `py/clc/clc_dual_cant.py` (11) and
      `py/accgram/mam_simple_verse.py` (10), with 42 more at 1 to 10 each. `CLAUDE.md:40–41` says
      `py/check_mark_order.py` covers only the `.py` of the three evacuated repos, so these are in
      no lint's scope and in no named exemption; whether each is expected (a paste from
      Wikisource, a fixture that deliberately holds Unicode-normal input) is Ben's to judge, and
      the per-file list is in `D_04_treewide_scan.txt`.
   4. The two trees the window's own additions put into the other order — the landed
      `MAM-OSIS/MAPM-orig/` and `MAPM-orig-24/` (20 runs on added lines) and the consolidated
      `uxlc/in/UXLC-notes/*.json` (73 runs on added lines, stream A) — are byte-verbatim captures
      exempt on the same ground as `in/UXLC-39/`, and neither is in the list.
   The sentence "The rest are byte-verbatim captures of external sources" is contradicted by items
   2 and 3. Re-establish: `D_04_treewide_scan.py`, `py_cluster_spotcheck.py`.

5. **Stale claim in `CLAUDE.md`, unfixed: lines 37–43 say the prose lint covers "every tracked
   `.md` plus the `.html` under `doc/`" and that "a `.txt` is covered by nothing".** Since
   `10a5c307` (2026-09-09 13:59) the lint's pathspec has a third element,
   `in/accgram/edition_transcriptions/*.txt`, and its scope at `0354b6cc` is 224 files, 12 of them
   `.txt`; Ben's decision went into the lint's docstring (lines 54–66) and `CLAUDE.md`, which
   points at that lint, was left saying the opposite, `985262e2` having later edited the same
   paragraph's `check_mark_order` sentence without touching these two (stream D). Re-establish:
   `git ls-files -- "*.md" "doc/*.html" "in/accgram/edition_transcriptions/*.txt"`.

6. **Record errors in the Wikisource cutover's plans, unfixed, and no record of the production
   refresh at all.** Four items:
   1. `doc/PLAN-efficient-wikisource-downloads.md:19–23` says "Metadata is seeded for 909
      chapters. The 20 unequal chapters retain their committed raw text and have no seeded record;
      a production refresh remains a separate decision", `:659` "A normal all-book run against the
      committed partial seed would fetch the 20 excluded chapters", `:734` "The unresolved
      production-text decision concerns the 20 excluded chapters", and
      `doc/efficient-wikisource-downloads-phase3-validation.json:2892` the same. At `0354b6cc`
      `in/mam-ws-revisions.json` has 929 records, all 20 chapters were refreshed, and 21 verses
      changed in every product (`B2_08_ws_revisions_offline.py`, `B2_13_product_diffs.py`).
   2. `doc/PLAN-wikisource-derived-mam-products.md:30–31` "Raw inputs and bot captures are
      unchanged" is false at `0354b6cc` for 11 `in/mam-ws/` books and 11 `out/mam-ws-bot/proto/`
      books.
   3. `git grep` of `doc/` for `209b4c05` or "Refresh Wikisource products" finds nothing: the
      decision the plan reserved was taken and executed with its 21 verse changes recorded only in
      a two-line commit message.
   4. The Phase 6 records and `doc/PLAN-evacuate-five-MAM-products.md` (`State: complete`) never
      mention the cutover that changed their verified outputs the same day: 97 of 6B's 415 outputs,
      16 of 6C's 99 and 57 of 6D's 295 no longer carry the recorded blobs, all changed by
      `209b4c05`, `321b2eeb`, `426fa229`, `8f5c1c96` or `516a4a1a`; the records are dated and name
      `40b8ea4b`, so they are not wrong, but a reader of "unchanged generated bytes" (`:1515`) is
      not told the state lasted hours (`B2_12_phase6_json_vs_tree.py`).

7. **`.novc` pointers in tracked prose, unfixed: the window added 208 such lines in 17 documents,
   against Ben's rule of 2026-09-10, and no tracked file states that rule, so a fresh session
   cannot learn it from the repositories.** Ben's word, quoted in
   `6ca009a5` and `0354b6cc`: "Just get this thing into an archivable state, which includes not
   pointing to things in anybody's .novc dir." Those two commits removed every pointer from the
   five files they name (stream C), and left the rest of the window's additions as they were.
   Counted by `git grep -c` over the window-added `.md` files at `0354b6cc`:
   1. `doc/PLAN-wikisource-derived-mam-products.md` 43, `doc/PLAN-remediate-review-findings-2026-09-08.md`
      33, `doc/PLAN-efficient-wikisource-downloads.md` 24, `doc/PLAN-worktree-file-consolidation.md`
      24, `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md` 16,
      `doc/PLAN-close-out-review-2026-09-08.md` 4, `doc/mam-products-phase6-command-map.md` 4,
      `doc/review-findings-2026-09-08.md` 4, `doc/mega-coverage-2026-09-10.md` 3,
      `doc/PLAN-mega-coverage.md` 2 (one of them, line 226, pointing into the scratch of a
      worktree that no longer exists), and one each in `doc/assessment-two-stranded-artifacts-2026-09-09.md`,
      `doc/codex-review-findings-2026-09-08-claude-turn-5.md`, `doc/foi-mtgmtg-empty-cell.md`
      (six script names on lines 106–111), `doc/user-level-config-in-cloud-sessions.md` and
      `doc/meteg-after-silluq-in-uxlc-and-wlc.md` (whose one mention states that none exists).
      Many of the Codex plans' pointers name scratch under six other worktrees
      (`C:/Users/BenDe/.codex/worktrees/2665`, `4378`, `3169`, `ffc9`, `3f2e`, `3f99`) that no
      fresh checkout has, and several are a figure's only evidence pointer (stream B2).
   2. **`6ca009a5`'s title overclaims**: "meteg-after-silluq docs: NO POINTER INTO ANY .novc DIR
      REMAINS" is true of the three docs, the plan and the JSON its body names, while the two
      other docs of the same investigation, untouched by it, hold 23 lines each —
      `doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md` (3, 22, 31, 32, 59, 65, 85, 96,
      101, 251, 268, 276 and its whole section 12 of `.novc/mas_b_*.py` commands) and
      `doc/meteg-after-silluq-search-in-mam-documentation.md` (16, 56, 72, 87, 135, 139 and its
      whole "Scripts and commands" section) (stream C).
   3. The rule is recorded in two commit messages and in this machine's Claude auto-memory, and
      in no tracked instruction file: `~/.claude/CLAUDE.md`'s "Running scripts" section says
      where a temp file goes and nothing about naming one in tracked prose. Six earlier files
      also carry pointers (`doc/PLAN-evacuate-the-rest-of-three-repos.md` 30,
      `doc/PLAN-evacuate-five-MAM-products.md` 19, `doc/metsudah-vs-ctr.md` 12,
      `doc/review-findings-2026-09-04.md` 10, `doc/PLAN-mam-mega-pipeline-phase-13-and-remediation.md`
      9, `doc/sigil-decoding.md` 8), census only; the eleven mentions each in
      `dot-claude/user-wide-CLAUDE.md` and `dot-Codex/user-wide-AGENTS.md` are Ben's instructions
      about where temp files go, not pointers.
   Re-establish: `git grep -c -I "\.novc" HEAD -- "*.md"`; `C_03_terminology.py`;
   `B2_14_prose_rules.py`.

8. **`State:` lines, unfixed: 6 of 21 plans and 4 of 17 review files do not conform to the two
   vocabularies — `check_repo_standards.py`'s five plan words (`executed <date>`, `paused
   <date>`, `live`, `runbook`, `pointer`) and D10's review-file phrases (`not yet acted on`,
   `acted on <date>`, and `completed <date>; review only` for a later turn) — and nothing checks
   any of it.** Stream D's census
   (`D_05_state_lines.py`), in the vocabulary of `py/repo_util/check_repo_standards.py:269–289`
   and `doc/dual-agent-review.md`'s D10 section:
   1. Three 2026-09-10 Codex-written plans have no `State:` line at all while each says in prose
      it is complete: `doc/PLAN-efficient-wikisource-downloads.md:3` is `## Authorization, status,
      and development location`, `doc/PLAN-wikisource-derived-mam-products.md:3` is
      `## Authorization and status`, `doc/PLAN-worktree-file-consolidation.md:3` is body text. All
      three arrived after `9d1de074`, at which the Wave 4 census of 16 out of 16 was true, so the
      September 8 review's finding 7 recurred the same day its remediation was verified
      (stream A).
   2. `doc/PLAN-evacuate-five-MAM-products.md` and `doc/PLAN-evacuate-public-repos-programme.md`
      say `State: complete`, a sixth word beside the five the lead names;
      `doc/PLAN-close-out-review-2026-09-08.md`
      leads with `State: remediation executed 2026-09-10`.
   3. `doc/review-findings-2026-09-08.md:3` reads `State: remediated 2026-09-10; …`, a third word
      where D10 rule 2 allows `not yet acted on` or `acted on <date>`, written by the very
      close-out that adopted D10 in the file D10 names as owning remediation state; every
      intermediate State that file quotes as history ("remediation in progress 2026-09-10")
      was outside the vocabulary too (stream A).
   4. The three Codex files of 2026-09-07 and 2026-09-08 lack "; review only";
      `doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md:3` opens with the standard's `executed
      2026-09-10` and runs on for four sentences, as five other plans do.
   5. `State:` occurs in `check_repo_standards.py` only in its docstring, whose pointer to D10
      (lines 291–292) names neither `dual-agent-review-<date>-turn-NN-<agent>.md` nor the
      `codex-review-findings-*.md` glob, and whose line 295 says it "adds no mechanical standards
      check".
   Re-establish: `D_05_state_lines.py`; `A_04_state_lines.py`.

9. **Stale figure in a live plan, unfixed: `doc/PLAN-silluq-before-gaya-template.md:445–449`
   (acceptance criterion 9) pins `gh-pages/MAM-with-doc/foi/foi-mtgmtg.json` "byte-identical …
   718 records … `1/sopa-y/maq-y` 229", and the file at `0354b6cc` has 717 and 228.** The record
   that left is 2 Chronicles 26:15's verse-final chanted word, whose meteg on the joined כִּי the
   refresh `209b4c05` removed; the file had 718 / 229 at `becc6f00` and `30fb7681` and 717 / 228
   at `5f996d0e` and `0354b6cc`. The criterion says "re-measure and treat any mismatch as a
   finding", so its first execution reports a mismatch that has nothing to do with the template,
   and its "byte-identical" is unsatisfiable as written, the file having already changed: the
   criterion needs re-pinning to the current bytes, or rewriting to compare against a named
   commit. That plan's line 3 says `State: live`, so it is kept true in place rather than
   corrected in a sibling `-update.md` file (D12 of `doc/dual-agent-review.md`). The same 229
   stands as a dated measurement in
   `doc/foi-mtgmtg-empty-cell.md:31, :151` and `doc/meteg-after-silluq-koren-lookup-candidates.md:52`;
   the 38, 354, 392, 135 and 122 are unaffected (stream C, `C_05_mtgmtg_oracle.py`,
   `C_12_followups.py`).

10. **Licence coverage gap, unfixed: `DATA-LICENSES.md` has no row for `aleppo/page-snips/`.** The
    directory arrived in `ca0b4d02` with Ben's crop of the Aleppo Codex from mgketer.org's image,
    and `7d40fa06` added a second. Its only cover is line 92's catch-all "`aleppo/`, except
    `aleppo/aleppo-pages/` and `aleppo/aleppo-wiki/`", which describes its contents as "line and
    column data annotated by Ben Denckla, derived reports, procedures, and provenance records"
    under the terms "Ben Denckla's compilation and analysis". A crop of a photograph of the Codex
    is none of those four things, and its terms are not Ben's to state. The row a remedy would
    copy is line 95's, for `leningrad/page-snips/`: "crops that Ben Denckla made from Leningrad
    Codex photographs", under the terms "each rights holder's; no grant is made or implied here"
    (added 2026-09-07, `9eedccbd`). The window's two licence commits, `c39b6dd6` and `42520d05`,
    both predate the directory, so no licence pass has run since the crops arrived (stream C).

11. **Terminology in the meteg-after-silluq documents, unfixed, listed by rule** (stream C,
    `C_03_terminology.py`, then read):
    1. `doc/meteg-after-silluq-search-in-mam-documentation.md:37, :52` render MAM's note's סימנים
       at 1 Kings 7:37 as "the Simanim Tiqqun". The Simanim Tiqqun is a Torah-and-haftarot tiqqun
       (`doc/scan-pages.md:6`) and 1 Kings 7:37 is in no haftarah (the readings from 1 Kings 7
       are 7:13–26, 7:40–50 and 7:51–8:21 — stream C's knowledge, not the repository's, since
       `in/scan-pages/simanim-tiqqun.json` has no census); the edition MAM's note compares is the
       Simanim Tanakh, which the Job and Psalms docs read by page (1172, 1053).
       `references/terminology.md:291` says an unqualified "Simanim" "reads as the Tiqqun by
       historical accident alone", which is what happened.
    2. Bare "L" and "A" for the two codices in the search doc's own voice, 36 sites (the
       classification column of finding 1's table at lines 20–47, the category label at 60, lines
       108–146), against the skill's "the LC" and the named codex.
    3. "ga'ya" in the docs' own voice against their own declarations (search doc line 12,
       empty-cell doc lines 10–13): 14 sites in the search doc (60, 61, 63, 66, 135, 141–146, 216,
       221, 236) and 12 in `doc/foi-mtgmtg-empty-cell.md` (42, a heading; 45, 52, 63, 68, 71, 72,
       120, 147, 169, 171).
    4. Agentive verbs the skill has retired, 8 sites: `doc/meteg-after-silluq-koren-lookup-candidates.md:68`
       ("MAM writes one deḥi", "MAM-simple carries no deḥi stress helper"; `18612038`),
       `doc/meteg-after-silluq-job-4-12.md:64, :79, :84, :85` ("MAM marks", "UXLC codes", "MAM
       puts", "the Aleppo Codex puts"), `doc/meteg-after-silluq-psalms-72-15.md:9, :14` and the Job
       doc's line 9 ("MAM copies", "MAM prints").
    5. Three romanizations of the same three words across the six docs: "patax / xataf / dexi" in
       the screen doc (17 sites) and the search doc (11), "pataḥ / hataf / deḥi" in the Koren doc
       (229) and `doc/post-stress-meteg-method.md`, "patah / hataf" in the in-uxlc, Job and Psalms
       docs; the user-level rule puts ASCII `x` in `#` comments only.
    6. `doc/PLAN-silluq-before-gaya-template.md` is still named with "gaya" while its line 81
       says the element name "deliberately uses meteg, not gaya" — pre-existing (`772545d5`), cited
       at seven in-scope sites, note only.

12. **Record error in the new verse-links skill, unfixed: "a bare consonantal form works" fails
    for every verse-final or maqaf-final atom.** `dot-claude/skills/verse-links/SKILL.md:27–29`
    (and `py/main_verse_links.py:9–10`, `py/uxlc_misc/my_uxlc_find_atom.py:22–24`) say the Hebrew
    "is matched against the UXLC exactly, then by its letters alone, so MAM's pointed form and a
    bare consonantal one both work". `py/main_verse_links.py Psalms 72:15 יברכנהו` and
    `Job 4:12 מנהו` exit 1 with "Word … not found … Give the atom's number with --atom", while a
    mid-verse `Job 4:12 שמץ` matches: `strip_heb` (`:50–57`) removes only categories Mn and Cf, so
    the sof pasuq (Po) and a maqaf (Pd) survive it and a bare form never matches the atoms every
    lookup in this work is about. The behaviour is inherited from `py/main_uxlc_estimate_atom_loc.py`;
    the claim is new (`5aae8465`, `225ea3f2`), in a skill that is byte-identical in three homes
    (stream C, `C_15_letters_only.report.txt`).

13. **Stale figures written in the window and overtaken in the window, unfixed, four sites:**
    1. `py/tests/test_site_index_links.py:84` says "this page carries 35", the D8 change from 34
       in `42520d05`; `d61c3472` (11:07, "Register MAM-OSIS redirects and link the published
       product", 91 minutes after the fast-forward) added the MAM-OSIS entry and the walk returns
       36. The comment self-dates and the floor of 25 still functions, so the test is not wrong;
       D8 spent a decision and a commit on an inventory number in a comment that calls itself "a
       floor … not an inventory", and the number was stale again within the day (stream A,
       `A_07_render_pages.py`).
    2. `py/repo_scopes.py:35` says "81 in aleppo"; `7fa58d73` (18:10) deleted
       `aleppo/test-data-from-book-of-job.json` after `985262e2` (14:07) wrote 81, and
       `15822344` then edited the module without touching the figure; 80 at `0354b6cc`
       (streams B1 and D).
    3. `CLAUDE.md:699` says `leningrad/` holds "the hand-maintained `page-snips/` crop with its
       evidence note", singular, written by `985262e2` when the directory held one PNG;
       `b97a2100` and `7d40fa06` added two more that evening, so three crops sit there, and
       "hand-maintained" is the authorship vocabulary Ben retired on 2026-09-04 (stream B1).
    4. `CLAUDE.md:237–244`, the "Seven sites" of stale `al-hatorah` paths (pre-existing text):
       two line numbers have drifted (`chanted_word_accents.py:638` is `:696`,
       `breuer_word_length.py:106` is `:105`), and `py/accgram/post_stress_meteg.py:15` is a site
       of the same shape the list does not name (stream D).

14. **Stale record, unfixed: `doc/assessment-two-stranded-artifacts-2026-09-09.md` says six things
    are open that were closed within three hours.** Its State (lines 3–5) says "every disposition
    below is Ben's to choose" and §8 (537–562) lists four recommendations and two items left for
    Ben; recommendation 1 was executed by `b490988a` (13:48), 2 by `361b3dab` (13:36), 3 by
    `5a07e5af` (14:16), 4 by `10a5c307` (13:59), left-for-Ben item 2 by `5300d714` (14:04) and
    item 1 by `23d33437` (13:36); the five executing commits cite the assessment and the assessment
    cites none of them. Its §9 (566–580) also announces "The three measurements that needed a
    script" and numbers four (`40c0ade4` added the fourth without changing "three") (stream D).

15. **Record error in the file loaded every session, unfixed: `dot-claude/user-wide-CLAUDE.md:29`
    (= `~/.claude/CLAUDE.md`, `74d883d2`) says "Commits from 2026-09-09 onward are MAM-basics
    commits."** The boundary is the move, `74d883d2` at 12:02 on 2026-09-09, not the date: the same
    file cites `25a8955` and `560239c` at lines 50–51 as github-misc commits of that morning, and
    neither resolves in MAM-basics (`git cat-file -t` fails for both), as neither does any of the
    seven 2026-09-09 github-misc commits the instruction-file plan's M11 lists. A reader following
    line 29 would look for `25a8955` here and find nothing (stream D, `D_10_misc_checks.py`).

16. **Code defects of low reach, unfixed, three:**
    1. `5a07e5af` defines `_held_commits` twice in `py/repo_util/git_worktree_cleanup.py`, at
       lines 918–922 and 956–960 with identical bodies, both inserted by that commit's own diff;
       the second rebinds the first silently, and the duplicate survives `e7a1736b`'s rewrite of
       the module (lines 1101 and 1142 there) (stream B1; `git grep -n "def _held_commits"`).
    2. `_run_near_aleppo_census` (`py/main_0_mega.py:190`) builds the census `cwd` as
       `_REPOS / "MAM-private"` rather than through `paths.sibling_repo`, so the
       `REPO_MAM_PRIVATE_DIR` override does not reach that step and a missing clone fails there
       with a bare `FileNotFoundError` naming no override; `test_sibling_reach.py:76` records the
       shape (stream B1).
    3. `.claude/hooks/install-user-config.sh:105` decides the skill is present by `[ -d
       "$DEST/skills/hebrew-prose" ]` while line 159 checks `SKILL.md` inside it, so a directory
       left by an interrupted `cp -R` takes the "already in place" branch; cloud-only, read not
       exercised (stream D).

17. **Missing qualifier in `CLAUDE.md`'s new MAM-private section, unfixed.** Its last sentence,
    "only the survey build in `py/accgram/post_stress_meteg.py` reads Phonetic MAM", is false of
    the repository: `py/accgram/breuer_word_length.py:444` (`survey-breuer-zaqef-units`) and
    `py/tests/test_final_stress_vs_phonetic_mam.py:131` also read it through
    `require_al_hatorah_phonetic_dir`; `doc/mega-coverage-2026-09-10.md` §1 has the precise form,
    "the only post-stress-meteg code that reads MAM-private" (stream B1).

18. **Verification evidence the public record cannot check, recorded:**
    1. The archived "final committed-tree" suite log of the September 8 remediation
       (`wave4-01a08b71/20260910T133726Z-final-committed-tree.txt` in the evidence zip) is
       byte-identical to the Wave 3 technical log (`wave3-01a08b34/20260910T123821Z-suite.txt`),
       1,205 bytes, CRC `1f68664b`, elapsed time `109.92s` included; their JSON envelopes record
       two distinct wrapper runs (heads `c36f5baa` and `9d1de074`, 110.92 s and 110.88 s), so a
       process did run each time, and whether the identical hundredth of a second is coincidence
       or a copied log the public record cannot tell. The tracked record gives no figure for the
       final tree, deferring it to the receipt (stream A, `A_13_archive_suite_log.py`).
    2. "1,074 generated/public HTML files" (`doc/PLAN-close-out-review-2026-09-08.md:69`,
       `doc/review-findings-2026-09-08.md:1063, :1075, :1105`): `git ls-tree` counts 1,072 tracked
       `.html` at every commit from `38a606e2` to `9d1de074`; the remediation plan (`:2029–2031`)
       says its inventory "included untracked HTML" and never says which two.

19. **Dead references, unfixed, three:**
    1. `doc/metsudah-vs-ctr.md:72` "(the same endpoint `py/subcommands/download_sefaria.py` uses
       for MAM)" — `985262e2` deleted the module with `fr-sefaria`; the sentence reads as current
       (stream B1).
    2. `doc/PLAN-evacuate-public-repos-programme.md:866` names a `DATA-LICENSES.md` row
       `in/mam-from-sefaria/`; the row (`DATA-LICENSES.md:51`) is `in/mam-from-Sefaria-2021-11-23/`,
       a different directory that still exists; the deleted `in/mam-from-sefaria/` had no licence
       row and has no surviving code reference (stream B2).
    3. `doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md:359`
       "`misc/zarqa-table-diff/make-dph-files.ps1` now calls the new command" — `e820ca4e`
       deleted the script and its message says the record stays as written; listed so the "now"
       is visible, not to reverse the choice (stream B1).

20. **Prose-rule hits and small record slips, all low, unfixed:**
    1. "hand-authored" at `CLAUDE.md:24, :37` (`036deb92`), `doc/PLAN-wikisource-derived-mam-products.md:594`,
       `doc/mam-products-phase6-command-map.md:156`, nine sites of the assessment and five of
       `py/tests/test_prose_mark_order.py`; "HAND-AUTHORED", "hand-maintained" and "hand-written"
       at `py/main_pipeline_graph.py:9` and `py/main_0_mega.py:742–743`, against the 2026-09-04
       vocabulary (Ben-written, Claude-written, script-regenerable); in `CLAUDE.md` and the lint it
       is the lint's term of art (streams A, B1, B2, D).
    2. "the former current State" at `doc/PLAN-remediate-review-findings-2026-09-08.md:1208` and
       "the former line-3 State" at `:2803` (adjectival; "previous" says it); "the latter" at
       `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md:405`.
    3. "one … the other" at `doc/PLAN-mega-coverage.md:411`, `py/tests/test_mega_coverage.py:47–48`
       and `py/mb_cmn/graphviz_pin.py:27`, referents recoverable in each.
    4. Announced counts left unnumbered: `doc/PLAN-evacuate-five-MAM-products.md:1964` ("two
       bounded public findings. First, … Second, …"), the assessment's §6 line 510 ("Three
       things"), the hook's comment lines 42–59 ("Four further trees", three entries), the
       instruction-file plan's §6 line 529 ("Two things"), the screen doc's line 5 ("Two terms").
    5. Findings without a disposition in their lead: `doc/meteg-after-silluq-psalms-72-15.md`
       summary items 4, 7 and 8 (lines 12, 15, 16), the screen doc's findings 1, 5, 6 and 7 (lines
       15, 25–27), the assessment's lines 72 and 158.
    6. Backslash paths: none in added prose; 45 occurrences in 10 tracked `in/*.json` evidence
       files, e.g. `in/mam_osis_stubs_verification.json:5–6, :286, :289`.
    7. `doc/user-level-config-in-cloud-sessions.md:214–216` says the hook invokes "`cp`, `echo`,
       `ls`, `mkdir`, and `cd` / `dirname` / `pwd` … and nothing else"; it also invokes `sed`
       (line 129); the substantive claim, no network call, holds.
    8. Immutable-message slips: `5e7f0d6b` "holds Hebrew on 126 lines" (16 lines hold a
       Hebrew-block codepoint); `74d883d2` "13 Hebrew clusters, 0 in Unicode-normal order" over the
       twelve config files, which hold 0 clusters with two or more marks, so no cluster there can
       tell the orders apart and the assessment's §3 repeats that vacuous evidence; `5a07e5af`
       "983 passed" and `7af937fa` "984 passed … The 983 this task was given as the baseline is one
       low" for nearly the same tree; `209b4c05` silently carried the vendoring-report
       reclassification (24 `eol-only` rows to `identical`) that the efficiency programme kept out
       of its own commits (streams B1, B2, D).
    9. `leningrad/page-snips/380A-col2-line3-Ps72v15-yevarkhenhu.png` carries a column nobody
       read, against the README's naming rule (lines 4–6) that `9eff3d00` applied to the Job crop
       and not to this one (stream C).
    10. `doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md:552`, a blank line at EOF, the one
        authored whitespace error on the window's added lines.
    11. `dot-claude/user-wide-CLAUDE.md:1275` and `dot-Codex/user-wide-AGENTS.md:1061`, the
        illustrative `[page](gh-pages/accgram/page.html)` that a link checker reads as dead.

21. **Process and hygiene, recorded for Ben's decisions:**
    1. **The desktop app re-leased `eloquent-ritchie-0e4c6c` to this session**, the third session
       in that worktree (created 2026-09-09 13:45 for `claude/eloquent-ritchie-0e4c6c`, re-used
       2026-09-10 08:58 by the Koren-lookups session on `claude/interesting-taussig-6aa52b`, and
       again at 22:42 tonight on `claude/mam-basics-review-stage-1-72e903`); Ben's 09:00 re-use was
       his choice and tonight's was the app's. `e7a1736b`, outside the window, already records the
       hazard as the maintenance runbook's H8 and says the sweep spared this worktree as leased.
       What remains is housekeeping after this session ends: the worktree and its branch, which
       holds no commit, can go with `git worktree remove` and `git branch -d`.
    2. **Step 7 of the close-out was executed after the window and nothing records it**: the
       September 8 review worktree and branch are gone (`e7a1736b`'s message says the sweep removed
       the review worktree "named with `--session-ended`"), while `doc/PLAN-close-out-review-2026-09-08.md:3`
       still says "Step 7 remains Ben's task after the final task ends" and step 7 has no execution
       line; whether the branch went with `-d` or `-D` is not recoverable from the public tree
       (stream A).
    3. Cadence: the Codex review worktree merged `main` thirteen times in the window; seven of the
       31 merges resolved conflicts; the global Git section's "merge just before the session is
       archived" describes a different cadence, as the last two reviews also noted. Census only.
    4. **Nothing tracked says that a cloud session's commits are authored `Claude`**: 12 such
       commits are on `main` (the window's two and ten of 2026-08-31 and 2026-09-01), all with a
       `Claude-Session:` trailer, so the "account is not the actor" reasoning of the user-level
       issue section has an exception nobody has written down; and the cloud session's remote
       branch `origin/claude/charming-mayer-xknwcw`, merged by `b490988a`, was never deleted on the
       remote (stream D). The Codex trailer now has a second address, `codex@openai.com`, on 7
       commits. Census only.
    5. Two Codex commits (`ac3e49e2`, `1fe3c989`) edited the tracked `dot-Codex/user-wide-AGENTS.md`
       first and synchronized the live copy second, the reverse of the live-first order
       `dot-claude/README.md` settled on 2026-09-09; the copies are identical, so no drift
       resulted (stream D).
    6. **#266 and #267 are open though fixed upstream and refreshed here**: skadish1's Wikisource
       edits of 2026-09-09 are in `in/mam-ws/`, `MAM-parsed/plus/` and `plain/` at `0354b6cc`, and
       neither issue says so. Whether the issues close when the products carry the fix, or when
       phonetic-hbo's page does, is Ben's; the answer to the question each asks is now in the
       tree.
    7. The instruction-file plan's §1 item 4 and §5 item 8 tell a worktree session to set
       `REPOS_ROOT`, true when written and overtaken by `516a4a1a` the next day; the plan is
       `live` and will be executed from its text (stream D).
    8. The last review's findings 18.2 to 18.4 are disposed of: `origin/post-stress-meteg` is
       gone from the remote, the empty `d4d1` directory and the post-stress-meteg Codex worktree are
       gone, the primary clone's `.pytest_cache` remains (referred to maintenance), and
       `~/.codex/plans` holds five entries (not read). `GitRepos` holds exactly the roster's five
       directories and no residue; `C:/Users/BenDe/.codex/worktrees/` holds one directory, `0e63`,
       that `git worktree list` does not name (not read).

## Open ends the window itself declares (not findings)

The mega cannot complete on the committed tree until finding 1 is fixed, and the change log's
regeneration (finding 2) waits on the same fix; `e7a1736b`'s "suite 992 passed" says nothing about
the mega. `doc/PLAN-silluq-before-gaya-template.md` is `live` and unexecuted, tracked on
phonetic-hbo#78 (open), and its criterion 9 now mismatches for the reason finding 9 gives. Issue
#265's registry proposal is filed and undecided; #269's twenty `sys.argv` programs and #270's
lamed-anchored template arguments are filed and open. `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md`
is `live` with nothing acted on, accurately. The September 8 review's remediation is complete and
integrated, its worktree retired after the window (finding 21.2); the Codex counter-argument of
this window has not been run. `main` and `origin/main` stood at `e84e2c70` when this file was
committed, five commits past this review's anchor, and those commits — `e7a1736b`'s 250-line
rewrite of `git_worktree_cleanup.py` and the four Google Sheet and template-dispatch commits that
followed it — fall to the next review.

## What this review did not check

1. Anything in MAM-private, hbofonts, or github-misc: the Phonetic MAM figures the
   meteg-after-silluq docs rest on (the 263,320-word syllable census, the Koren doc's sheva base
   rates and its class A / B / C assignment, the in-uxlc doc's Phonetic MAM checks), mgketer's
   transcription and the screen's section 10, Yeivin's and Breuer's OCR exports behind every ITM
   and CoS citation, the MAM-private goldens the census step rewrites, and `b865b7c8`'s Phonetic
   MAM figures.
2. Regeneration of any generator that writes tracked files in place: the mega and its 59 steps,
   `py/main_diff.py ctr-vs-mam`, `py/main_diff.py wsgo`, `parse go`, the survey, the MAM product
   generators, `py/main_vendoring.py --all`, `py/main_authored.py gen-site`. Regenerated to
   scratch or recomputed in memory instead: the eleven deploy-root pages (twice, by streams A and
   B1), the OSIS product, both pipeline graphs, the four vendoring outputs, the change log (finding
   2), the FOI, the plan's run, and `diff mpp` to scratch (finding 1).
3. The recorded suite counts of the intermediate commits; only the 992 at `0354b6cc` was run, and
   the one-item gap between it and the `def test_` arithmetic's 991.
4. The four crops' image content beyond their existence, dimensions, captions and provenance, and
   no reading of any manuscript or printed edition is adjudicated; Ben's readings of Koren, the
   Simanim Tanakh and BHS are not on disk.
5. The September 8 remediation's untracked evidence beyond the receipt, the four suite logs and
   the two envelopes: Wave 2's 930 output hashes, the V6 gate script and its probes, Wave 3's
   snapshot differentials (MAM-private), the archive manifest's hashes.
6. Every cloud-container measurement in `doc/user-level-config-in-cloud-sessions.md`, and the
   hook's local no-op, which running it would have meant writing into `~/.claude/`.
7. Phase 6E's 484 HTTP responses and every deployment's served bytes; the efficiency plan's live
   timings; the Wikisource editorial correctness of the 20 refreshed chapters; the search doc's
   parser-dependent totals (23,283 segments, 16,665 calls), which stream C's own parser did not
   settle either way.
8. Whether each of the 7,247 clusters outside `CLAUDE.md`'s named exemptions, and each of the 51
   `.py` files, is expected (finding 4): the scans decide order, not provenance.
9. Whether the 37 pre-existing non-MAM-normal runs the last review left on nine files are
   deliberate illustrations, as the last three reviews also left them; and the 110 whole-file runs
   above.
10. The Codex-side facts behind the instruction-file plan's D7 and D8 (`~/.codex/plans/` layout,
    `memories_1.sqlite`), and github-misc's history behind the plan's M11.

## Inputs for the reconciliation with the Codex review

Anchors for comparison: MAM-basics `38a606e2..0354b6cc`; MAM-OSIS `26a7e85f` and `8df241b3` on
GitHub; phonetic-hbo `10de7970`; the thirteen quiet public repos at the heads `gh_census.txt`
records. Each finding above gives the commit, the file and line as of `0354b6cc`, the claim, the
measurement, and the command or `.novc/review-2026-09-10/` script that re-establishes it, so a
disagreement can be checked by hand without re-deriving the whole window. Findings 1, 2, 4.3 and
16.1 were re-derived by the main session as well as by their streams (the `diff mpp` command run
to scratch for 1; the change log's Isaiah and Psalms entries read for 2; the 51 `.py` files
rescanned for 4.3; the two `def _held_commits` lines grepped at both commits for 16.1), and the
tree health figures, the census and finding 21 are the main session's own. The reconciliation
section goes below this one, under `## Reconciliation with the Codex review`, per
`doc/dual-agent-review.md`.

## Dispositions after remediation

Recorded by a Claude session on 2026-09-11. Findings 1 to 6 were fixed before the Codex
counter-argument had run, so this section exists ahead of the reconciliation section that
`doc/dual-agent-review.md` places above it. That section goes between "Inputs for the
reconciliation with the Codex review" and this one. The counter-argument reviews the window at
the anchor `0354b6cc`, where all six findings still stand as written above.

Ben asked for the fixes to findings 1 and 2 only. Findings 3 to 6 were fixed unasked, by a
session that read his instruction to step through the findings as an instruction to fix the
problems they describe, when he had asked to be shown each finding and to discuss its wording.
This is said here because the rows below would otherwise read as six requested fixes.

| Date | Finding | Disposition |
|---|---|---|
| 2026-09-11 | 1 | Has been fixed by `f11ecaf8` on `main`. Every op that places a mark now records the index the mark has among its cluster's marks in the new text, and `change_ops_apply` places it there, so the mpplus diff rebuilds Isaiah 24:18 and the mega's step, now named `diff-mpplus`, no longer stops. The finding's command re-establishes it with the subcommand renamed: `py/main_diff.py mpplus --old 9ce6ee5 --new HEAD`. |
| 2026-09-11 | 2 | Has been fixed by `6b45ad0f` on `main`. `gh-pages/MAM-with-doc/change-log/unpinned-latest.json` has 69 records, the 57 it had plus the twelve verses the refresh `209b4c05` changed; `unpinned-latest.html` and `index.html` were regenerated with it. |
| 2026-09-11 | 3 | Has been fixed, unasked, by `2b140909` on this branch, which supersedes `2bb94060`. Under Ben's decision of 2026-09-11 that a finished dated document is left as written, a correction to one goes in a sibling `<stem>-update.md` instead of beside the passage it corrects. `2bb94060` had put the corrections beside the passages; `2b140909` restores both documents to their earlier text and puts the same corrections in two new files: `doc/review-findings-2026-09-08-update.md`, for the Wave 3 technical paragraph and the 13.3 row of the final disposition table, and `doc/PLAN-remediate-review-findings-2026-09-08-update.md`, for items 1 and 2 of the Wave 3 technical source changes. Each says that `3a1ab7f0` retired the display fallback. |
| 2026-09-11 | 4 | Has been fixed, unasked, by `d71387a5` on this branch, by making `CLAUDE.md`'s mark-order section state only what was measured. Re-measured at `2bb94060` with the same counting as `D_04_treewide_scan.py`: 699,940 clusters; 688,072 in the four mam-ws trees, `out/mam-ws-bot/proto-fmt-2/` now named among them; 4,621 in the named captures; and 7,247 in 152 files, now stated as unclassified rather than expected. At Ben's direction, whether each unclassified cluster is deliberate was not judged, so the two trees item 4 calls captures are counted among the unclassified. Item 3's two figures are both true of different sets: 656 clusters are in the 65 files under `py/`, and 369 of them are in the 51 `.py` files. |
| 2026-09-11 | 5 | Has been fixed, unasked, by that same commit `d71387a5`. `CLAUDE.md` now names the prose lint's third pathspec element, the `.txt` under `in/accgram/edition_transcriptions/`, and says that any other `.txt` is covered by nothing. |
| 2026-09-11 | 6 | Has been fixed, unasked, by `89c1d7cf` and then `ffc82f60`, both on `main` and both made off this branch, at Ben's direction that fix-now remediation lands outside the review branch. `89c1d7cf` had put dated corrections, and a new section, inside three completed plans; under Ben's decision of 2026-09-11 that a finished dated document is left as written, `ffc82f60` restores those three plans to their earlier text and puts the same material in three sibling files: `doc/PLAN-efficient-wikisource-downloads-update.md`, holding the production refresh `209b4c05` of 2026-09-10 with its figures and the three passages it made stale, `doc/PLAN-wikisource-derived-mam-products-update.md` and `doc/PLAN-evacuate-five-MAM-products-update.md`. The first two also state, in the conventional form, the state their plans declare only in prose: both complete. The Phase 3 validation JSON stays as written, as a receipt. Re-measured from `209b4c05` alone, item 1's "21 verses changed in every product" holds for MAM-parsed plus and plain; `MAM-simple/xml-vtrad-mam/` changed in 11, the meteg changes. |

Findings 7 to 21 are not yet acted on.
