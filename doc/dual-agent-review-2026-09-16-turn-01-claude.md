# Findings of the 2026-09-16 review of the public repos since 2026-09-14

State: not yet acted on
Updates and later status: [dual-agent-review-2026-09-16-turn-01-claude-update.md](dual-agent-review-2026-09-16-turn-01-claude-update.md).

Written on 2026-09-16 from about 11:53 local and finished on 2026-09-17, as turn 01 of the standard
alternating dual-agent review under `doc/dual-agent-review.md` (Ben's decision D9 of 2026-09-09),
with Claude as Agent 1 by Ben's choice at the round's setup on the morning of 2026-09-16: this file
was frozen at `71f96ca3` before any Codex reviewer read it, and the Claude session neither read nor
sought a Codex half (no file named `doc/dual-agent-review-2026-09-16-turn-02*` exists, and nothing
under `~/.codex/` or `Documents/Codex/` was read beyond the live instruction, hook, configuration
and skill files that the deployment check and the Codex startup hook read, and the registration and
`git status` of the Codex worktrees under `~/.codex/worktrees/`, whose files were not read).
Nothing was fixed. A usage limit stopped the session at about 13:15 on 2026-09-16, after the five
streams had reported and while the pre-commit check was finishing; Ben resumed it on 2026-09-17,
when the check's corrections were applied and this file was committed. Every figure here was
measured on 2026-09-16 unless it carries another date. The round's shared worktree is the one D11
names, `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-16` on
branch `dual-agent-review-2026-09-16`, created and locked by a setup-only session from `main` at
`71f96ca3`; every later turn of both agents and the close-out use it directly, no intermediate task
fast-forwards `main` or pushes, and the worktree and branch are retired after the final task ends.
A second, detached scratch worktree, `.claude/worktrees/review-2026-09-16-mega-scratch` at the same
commit, held the mega run and the hand-run generator runs of the tree-health section, so that the
shared worktree stayed byte-stable while the streams read it; stream D left that scratch worktree
clean at `71f96ca3` and holding no branch, and when the session resumed on 2026-09-17 it was gone
from the worktree registry and from disk, removed by something other than this session while the
session was stopped. The reconciliation goes at the end of this file under `## Reconciliation with
the Codex review` once Agent 2's turn 02 is stable, per `doc/dual-agent-review.md`; later State and
every disposition go in `doc/dual-agent-review-2026-09-16-turn-01-claude-update.md`, which does not
yet exist.

Ben named no area of particular concern for this window: asked at the round's setup which area
Agent 1 should read first, he chose "No area of particular concern". The window was therefore read
by five agent streams plus the main session, as the 2026-09-14 review's was: (A) the 2026-09-14
round's records, its remediation plan and dispositions, and the D12 and `State:`-line conformance
of every `doc/` change; (B) the window's code under `py/`, the hook and the requirements; (C) the
instruction files, the skills, the two procedure documents and the user-level deployment; (D) the
product trees, the generated outputs and the hand-run generators; (E) the prose, the mark order,
the links and the new documents as documents. Every script and output is untracked under
`.novc/review-2026-09-16/` in the shared worktree, prefixed `A_` to `E_` per stream and unprefixed
for the main session, each stream's report beside them as `<stream>_report.md`, and the brief every
stream read first as `stream_common.md`.

Before this file was committed, every finding was given to one of five sub-agents that reported
without editing, and a sixth checked the opening, census and tree-health sections against re-runs
of the main session's scripts, as `doc/periodic-review.md` requires; their reports are
`V1_report.md` to `V6_report.md` beside the streams'. The check changed the file. It confirmed as
drafted findings 1, 2.2, 6.4 to 6.6, 8.1, 9.3 to 9.5, 10.2, 11.3, 13.1, 13.3, 16.2, 16.4, 16.5,
16.7, 16.8, 17.1, 18.1, 18.3, 19.2 to 19.4 and 20, and corrected the others in a figure, a line
number, an attribution or a referent. Four of its corrections are of substance: finding 3.1's one
stale blob assertion is four, finding 4's five calls the lint cannot see are six it would not flag,
finding 15's nine dates on four pages are thirteen on seven, and 16.9 is no defect, the rule it
named not yet having existed on the day in question. It also caught the statements that `main`'s
move at 12:39 on 2026-09-16 had overtaken. Where a correction came from the check rather than from
a stream, the finding says so.

## Scope, anchors and census

Eighth review under the public-repos-only scope, counting as the 2026-09-14 review counted itself
the seventh. It covers committed work from the 2026-09-14 review's end anchor, `bca64824`
(2026-09-13 14:48 local, "Close out the 2026-09-10 public review"), through the shared worktree's
base commit, **`71f96ca3`** (2026-09-16 10:48 local, "Repair live retirement plans"), which was
`main` and `origin/main` when the setup session created the worktree. The tree moved under the
review and the end anchor did not. When this session first read the refs, at about 11:50 local on
2026-09-16, `main` and `origin/main` stood one commit past the anchor at `6402de62` ("Close the
September 14 review record", committed 11:15); `5cf01537` ("Correct the September 14 review state
record", committed 11:46) was pushed a minute later, its Pages run being created at 11:51; and
`7014cfbb` ("Unify worktree retirement across owner selection scopes", 12:39) followed while the
streams read. The first two were fast-forwarded into `main` from the 2026-09-14 round's worktree,
since retired, and change only `doc/review-findings-2026-09-14-update.md`; the third changes three
files of the canonical user configuration, `dot-claude/skills/mam-repository-topology/SKILL.md`,
that skill's `references/repository-maintenance.md` and
`dot-Codex/skills/codex-worktree-tasks/references/task-lifecycle.md`. All three are outside this
window and were not reviewed. At 11:46 local on 2026-09-17, minutes before this file was committed,
`main` and `origin/main` both stood 35 commits past the anchor at `b6aa79a8` ("Merge branch 'main'
into codex-worktree-receipt-update-fix"), with the anchor still their ancestor.

Anchors (start → end) and counts, re-measurable with `git -C C:/Users/BenDe/GitRepos/<repo> log
<start>..<end> --oneline`:

| Repo | Range | Commits | Non-merge |
|---|---|---|---|
| MAM-basics | `bca64824..71f96ca3` | 97 | 86 |
| phonetic-hbo | `10de7970..8b134b6b` | 1 | 1 |

That is **98 commits in two public repos**. Fourteen public repos were quiet: the clone Taamey_D
(clean, `main` at `origin/main`, `38134991`, the commit the 2026-09-14 review recorded as
`3813499`), and on GitHub MAM-simple, MAM-parsed, MAM-with-doc, MAM-for-Sefaria, MAM-OSIS,
codex-index-aleppo, codex-index-cam1753, codex-index-leningrad, diffable-pointed-hebrew,
book-of-job, holman-ketiv-qere, UXLC-utils and wlc-utils, each answering 0 to `gh api
"repos/bdenckla/<repo>/commits?since=2026-09-13T18:48:49Z"` and each with a `pushed_at` before the
window (`other_repos.py`, `gh_only_repos.py`). phonetic-hbo's one commit answers 0 to that same
query too, because `since` filters by commit date: `8b134b6b` ("Regenerate Phonetic MAM after the
Wikisource refresh") was committed on 2026-09-10 at 21:48 local and reached GitHub on 2026-09-15 at
17:25Z (`pushed_at`), after the 2026-09-14 review had recorded the clone at `10de7970`; the commit
range, not the date, is what finds it (finding 20). Two clones are private and fall to the private
series: MAM-private and hbofonts, neither read. github-misc has no clone here, and the series' one
standing exception, its instruction-file byte-compare, is spent as `doc/periodic-review.md`
records. `gh_only_repos.py` also asked GitHub for the visibility and push time of three further
names, mgketer, al-hatorah and masorah-books, which answered private; nothing of theirs was read
beyond that answer and a zero commit count. The workspace roster `all-repos.code-workspace` lists
five folders — MAM-basics itself, the two private clones and the two public ones — so the thirteen
GitHub-only repos are the ones the 2026-09-14 review read: nine are named in the
`mam-repository-topology` skill's `evacuated-repositories.md` reference, and four (MAM-parsed,
MAM-with-doc, MAM-for-Sefaria and book-of-job) are not named there.

The window changed **194 paths** between its endpoints — 37 added, 11 deleted, 144 modified, 2 that
`git diff -M` pairs as renames (`py/wlc_issue_edit.py` to `py/github_issue_edit.py` at 80 per cent
similarity, `py/tests/test_issue_edit.py` to `py/tests/test_github_issue_edit.py` at 76) — 12,841
insertions and 7,819 deletions, no binary file, taking the tree from 4,692 to **4,718** tracked
files, `.py` 1,051 to 1,051 (1,044 to 1,043 under `py/`, plus the new
`dot-Codex/hooks/check_project_doc_budget.py`), `gh-pages/` 1,859 to 1,859 files (579 HTML both
times), `doc/*.md` 112 to **123** (direct children of `doc/`), `doc/PLAN-*.md` 33 to **35**,
`doc/*-update.md` 22 to **25**, `dot-claude/` 10 to **20** and `dot-Codex/` 4 to **10** tracked
files, and `out/` 341 to 338. By top-level directory: `py/` 62, `doc/` 54, `gh-pages/` 23, `out/`
15, `dot-claude/` 14, `dot-Codex/` 9, `MAM-simple/` 3, `in/` 3, `uxlc/` 2, and one each in
`.claude/`, `MAM-OSIS/`, `MAM-for-Sefaria/`, `MAM-parsed/` and `holman/` and for `AGENTS.md`,
`CLAUDE.md`, `README.md` and `requirements.txt` at the root (`census.py`, `changed_paths.txt`).

The window's substance is six things:

1. The 2026-09-14 review round, from its argument to the start of its remediation: the review file
   with its 19 walk-through and self-check commits (16 of them among the 22 the procedure counts,
   whose other 6 changed the procedure document), Codex's turn 02, turns 03 and 04, the close-out
   decision record `2e77d2fd`, the remediation plan `d141e8cb` (1,020 lines), and the seven
   remediation commits `e805bce0` through `71f96ca3` of the morning of 2026-09-16 — about 45
   commits, most of them made on that round's branch.
2. New York time on pages: the helper `py/mb_cmn/new_york_time.py` and the tzdata requirement,
   labelled dates on the Holman, printed-Decalogue and change-log pages, the change log's
   `MAM-parsed/plus` tree-id label in place of a date, and the lint
   `py/tests/test_explicit_time_zones.py`.
3. The instruction compaction: `AGENTS.md` as the repository instruction body with `CLAUDE.md`
   importing it (#274), the `github-issues` and `mam-repository-topology` skills and the
   `hebrew-prose` references split out of the two `CLAUDE.md` files, the Codex user-level file cut
   from 1,298 to 273 lines with skill routing, the Codex document-budget hook, and the
   `codex-worktree-tasks` skill.
4. The vendoring audit removed from the mega with its five modules, its entry point, its lint, its
   inventory and its three outputs.
5. The mega-speedup plan, its Phase 2 (`859c4b43`), the Graphviz pre-check, Helvetica call-graph
   nodes, temporary-file SVG rendering, and four timing records.
6. Smaller code and data work: the augmented LCI field rename (`14722a34`, 3,928 lines of
   `uxlc/data/lci_augrecs.json`), Codex worktree retirement (`4530b32a`), the `github_issue_edit`
   rename, `doc/mam-normal-mark-order.md`, `in/mam-ws-intro/README.md` and `holman/WORKFLOW.md`.

## Tree health at `71f96ca3`: the suite at 989, the mega clean at 54 steps, ruff clean

- Suite: **989 passed, 5 skipped, 65 subtests passed** (162.94 s, slowed by the lints and the
  census scripts running beside it; the 2026-09-14 review's run at `bca64824` took 103.44 s), run
  in the shared worktree with `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe
  py/main_test.py -q -rs` and no `REPOS_ROOT` set, the tree clean before and after; the five skips
  are the edition transcriptions' semantic channel, as at `bca64824` (`suite.txt`). The count fell
  from 997 by exactly the window's test changes: `--collect-only` lists 1,002 ids at `bca64824` and
  994 at `71f96ca3`; the 16 only at the start are the 10 of the deleted
  `py/tests/test_vendoring_policy_paths.py` and the 6 of `py/tests/test_issue_edit.py`, renamed;
  the 8 only at the end are those 6 under `py/tests/test_github_issue_edit.py` and one test each in
  the new `py/tests/test_explicit_time_zones.py` and `py/tests/test_receipt_update_links.py`
  (`test_counts.py`, `collected_start.txt`, `collected_end.txt`).
- Mega: **all 54 steps pass and leave no diff** — `git status --porcelain` and `git diff --stat`
  both empty afterwards — run once on the detached scratch worktree at `71f96ca3` with the same
  interpreter and no `REPOS_ROOT`, in 345.3 s of wall time, 329.6 s of it in the 54 steps, with the
  standards check, the two HTML lints and the user-configuration check running beside its first
  minute and the stream launches beside its last, so its step times are not comparable with the
  window's timing records (`mega.txt`). The step table has 54 entries against 55 at `bca64824`,
  `25bcabf6` having removed `vendoring-audit` (`git grep -c -E "^\s+StepRecord\(" <commit> --
  py/main_0_mega.py`). The Graphviz pre-check `ac24cbd3` added reports the pinned 16.0.0 and that
  Helvetica and the default font load. The five slowest steps under that load:
  `accgram-survey-post-stress-meteg` 53.4 s, `diff-wsgo` 33.1 s, `wlc-json-and-unicode` 26.0 s,
  `parse-ws` 24.6 s, `accgram-survey-chanted-word-accents` 24.0 s.
- The two generators the mega does not run: `py/main_mam4sef.py` in its three modes (default,
  `--both-sef-and-ajf`, `--just-ajf`) and `py/main_mam_osis.py`, run by stream D on the same
  scratch worktree, each exit 0 and rewrite their products with the bytes they already hold — 160
  tracked files under `MAM-for-Sefaria/`, 25 under `MAM-OSIS/` and 2 under `gh-pages/MAM-OSIS/`, by
  mtime — leaving `git status --porcelain` and `git diff --stat` empty; the 2026-09-14 review's
  finding 2.1, which found both failing with `FileNotFoundError`, is fixed by `155bb778` "Resolve
  incremental MAM-simple inputs explicitly" (`D_02_generators.txt`, `D_03_generator_mtimes.txt`).
  `uxlc/data/lci_augrecs.json`, the window's largest changed file, is written by the mega's
  `uxlc-write-page-break-info` step and so is covered by the mega's clean run.
- Product trees: `MAM-parsed/plus` and `MAM-parsed/plain` have at `71f96ca3` the tree hashes they
  had at `bca64824` (`2072b5f9…` and `98c82e34…`), and `MAM-with-doc/` is unchanged; `MAM-simple/`,
  `MAM-for-Sefaria/`, `MAM-OSIS/` and `MAM-parsed/` differ in exactly 6 files, the four READMEs,
  `MAM-simple/doc/reading-mam-simple.md` and the example-support copy
  `MAM-simple/py-examples/mb_cmn/file_io.py`, and in no data file (`git diff --stat bca64824
  71f96ca3 -- MAM-simple MAM-for-Sefaria MAM-OSIS MAM-parsed`; `census.py`).
- `black --check py`: **1,043 files would be left unchanged** (black 26.5.1). `ruff check py` (ruff
  0.16.5): **All checks passed**, against the 2 F401 errors at `bca64824` that were the 2026-09-14
  review's finding 6, removed by `82ad4b57`. `py/main_repo_util.py --check-repo-standards --repos
  MAM-basics`, run from the worktree: `SYS_PATH_MUTATIONS=0`, `SYS_PATH_IN_TESTS=0`,
  `ORPHAN_MARKS=0`, `HEX_ESCAPES=80`, `NFC_H_DOT=30`, `NFC_LATIN=39`, `ROOT_CONFTEST=False`,
  `SHIM_CONFIG=None`, `GITATTRIBUTES_LF=True`, seven linked worktrees (the scratch one included)
  and two agent branches (`standards.txt`). `git ls-files --eol`: 0 `i/crlf`, 0 `i/mixed` over
  4,718 entries (`lints.py`).
- Whitespace: `git diff --check bca64824 71f96ca3` prints nothing.
- Mark order over the added lines of the 181 text files the window added or modified: **12,810
  added lines, 193 holding Hebrew, 524 Hebrew runs, 0 runs not in MAM-normal order**, 499 of the
  runs outside the trees `doc/mam-normal-mark-order.md` exempts and 25 inside them, all in the
  hand-authored `in/mam-ws-intro/README.md`; the two renamed Python files add 3 runs, in order;
  `py/tests/test_prose_mark_order.py` passes; and every census figure of the new
  `doc/mam-normal-mark-order.md` reproduces at `71f96ca3` (699,940 clusters in all, 7,247 in 152
  files outside the captures and intermediates) (`E_01_mark_order.py`,
  `E_04_mark_order_census.py`).
- Markdown links: of 477 links in the 264 tracked `.md`, 154 are external, 5 other schemes, and 314
  relative, 7 of them inside inline code; of the 307 relative links outside code, 27 resolve to a
  directory, 241 to a file, 24 to a heading, and 15 were flagged, of which 6 are the pointer
  template and a quoted command inside backtick spans that cross a line break, 7 are fragment links
  in `MAM-simple/doc/versification-differences.md` whose GitHub anchors differ from the headings',
  dead at both anchors and untouched by the window, and 2 are the two the 2026-09-14 review named,
  `misc/what-is-mam/img/provenance-misc.md:6`, dead at both anchors, and `doc/metsudah-vs-ctr.md`'s
  `ms-snips/README.md` link, which the opening-paragraph join moved from line 4 to line 3 and left
  dead by the receipt rule, its destination now recorded in `doc/metsudah-vs-ctr-update.md:27–31`.
  So **9 dead links at both anchors, and the window created none** (`E_03_md_links.py`).
- `py/check_html_syntax_and_sanity.py`: "No HTML output issues found" in both its default mode and
  `gh-pages --deploy-root` (`html_default.txt`, `html_deploy_root.txt`).
- Pages: all **23** MAM-basics deploy runs created for commits inside the window succeeded, from
  `afbdd878` (2026-09-14 13:35Z) to `71f96ca3` (2026-09-16 14:56Z), none cancelled; the three runs
  created after the anchor and before 13:00 local that day, for `6402de62`, `5cf01537` and
  `7014cfbb`, succeeded too (`pages_runs.py`).
- The user-level homes: `--sync-user-config --check` from the primary clone at 11:59 on 2026-09-16
  reported 17 clean destinations sourced from `refs/remotes/origin/main@5cf01537` and
  `USER_CONFIG_PROBLEM_COUNT=0`; `git diff --stat 71f96ca3 5cf01537 -- dot-claude dot-Codex
  .generated AGENTS.md CLAUDE.md` is empty, so the check compared the live homes against files
  byte-identical to the anchor's, and stream C's independent hashing of every live destination
  against the anchor's blobs found 17 of 17 equal, the Codex fingerprint being the SHA-256 of
  `71f96ca3:dot-Codex/user-wide-AGENTS.md` (`sync_user_config_check.txt`,
  `C_03_hook_and_home.txt`). That held until 12:39 that day, when the homes were redeployed from
  `7014cfbb` and the two live copies of the `mam-repository-topology` skill came to differ from the
  anchor in `SKILL.md`'s line 22 and in `references/repository-maintenance.md`
  (`V3_03_live_drift.py`); by 2026-09-17 the homes had been redeployed again from later commits of
  `main`, the Claude user-level file having become a one-line import of the Codex one.
- Issues: 23 comments were posted on MAM-basics issues in the window, and every agent-written one
  says so with a date. Thirteen are agent-written: nine at 08:29 local on 2026-09-16 by a Codex
  session, on #60, #66, #68, #69, #91, #215, #216, #219 and #260, seven repointing a citation of a
  deleted `doc/` file to the last commit that held it and two, on #68 and #69, repointing a moved
  file to its current location; the comments of 2026-09-14 on #272 and #273 by a Claude session
  with Ben's approval, pointing at `doc/PLAN-mega-speedup.md`; the comment of 2026-09-15 on #274 by
  a Codex session; and the comment of 10:49 local on 2026-09-16 on #278 by a Codex session
  recording the removal of the `leningrad/page-snips/` example from that open issue's body, which
  the 2026-09-14 review's finding 9 asked for and Ben decided. All 17 `blob/<sha>/<path>` and
  `commit/<sha>` links in those comments resolve in this repository, as do the `blob/main/` targets
  of four of them. The other ten comments, by the GitHub accounts `bdenckla` and `skadish1`, are on
  #282 and #283, two questions about what doc notes say of the Aleppo Codex, both closed from the
  `bdenckla` account on 2026-09-15 after edits on Hebrew Wikisource; their Wikisource and image
  links were not followed. Three open issues, #214, #222 and #230, had their bodies edited at 08:28
  local on 2026-09-16 with a dated Codex note and links that resolve; #284 was filed on 2026-09-15
  by a Claude session and says so (`issues.py`, `issue_comments.py`, `issue_links_check.py`).
- phonetic-hbo: the 26 Hebrew cells that `8b134b6b` changed, 13 chapter pages in each of the
  `gh-pages/tnkh/` and `gh-pages/tnkh-ashkenaz/` trees, each show at `8b134b6b` a form that is
  present in its verse in `MAM-parsed/plus` at `71f96ca3` while the form shown at `10de7970` is
  absent from that verse, for 24 of the 26; the other two are Psalms 4:3 in both trees, where the
  verse's `מ:דחי` template holds both forms as its two parameters, the second being the form that
  has the deḥi's stress helper, and the page moved from the first to the second. That template, and
  the new Psalms 71:9 form, entered `MAM-parsed/plus` with the 2026-09-10 Wikisource refresh
  `209b4c05`, the form with the deḥi alone having been the verse's plain text before it, since
  `63cf6c98`; so the whole commit follows from that refresh, as its message says
  (`phonetic_hbo_check.py`, `ps4v3_template.py`, `ps_forms_history.py`). The Ashkenazic and
  Sefardic transliterations beside the four Psalms cells, 4:3 and 71:9 in each tree, moved their
  stressed syllable with the stress helper. The generator was not read: phonetic-hbo's README says
  the pages are generated by code in MAM-private's `al-hatorah/` tree, which this series does not
  read, and the repository's only Python file is `py/tests/test_h_dot_below_nfc.py`.

## What verifies sound, stream by stream

**The census, the other public repos and the issue activity (main session).** The window's commit
and path counts, the tracked-file census at both anchors and the product-tree hashes are the
tree-health section's (`census.py`). The other public repositories: phonetic-hbo's one commit
follows from the 2026-09-10 Wikisource refresh, and the thirteen GitHub-only repositories and
Taamey_D had no commit and no push in the window (the "phonetic-hbo" and "Issues" bullets of the
tree-health section, `other_repos.py`, `gh_only_repos.py`, `phonetic_hbo_check.py`,
`ps_forms_history.py`). The 13 agent-written issue comments of the window and the three edited
open-issue bodies say who wrote them and when, and every MAM-basics blob and commit link in them
resolves (`issue_links_check.py`); GitHub attributes the other ten comments to the accounts
`bdenckla` and `skadish1`. The mega step table's change from 55 to 54 is one removal,
`vendoring-audit`, and the suite's change from 997 to 989 is accounted for test by test
(`test_counts.py`).

**The 2026-09-14 round's records and its remediation (stream A).** The 18 commits of the round's
record chain, from `d14d2723` "Record the 2026-09-14 review's findings, the Claude argument of the
fifth dual-agent window" to `71f96ca3`, each contain the previous one except where the merge
`dab5d091` joins the close-out record `2e77d2fd` to `0d82b4e6` "Clarify receipt retention and
issue-link retirement", made on `main`; turn 03 declares the stopping rule reached and turn 04
acknowledges it with no objection; the six record files' `State:` lines follow D10 and the
standards docstring. Every hex token in the update file and the plan resolves, all 7 commits
ancestors of the anchor and all 5 blobs present, and 54 of the plan's 63 path-like tokens are
tracked, the other 9 prose fragments, a directory the plan says to create, and untracked `.novc/`
files by design. The plan's baselines re-measure at its checkpoint `dab5d091`: 54 `StepRecord`
entries, 42 declared entry points, `MAM-simple/` at 109 files and 37,647,937 blob bytes, 25
`doc/*-update.md` and no numbered sibling, 15 files matching the broad review glob of which 12 are
the dated series, all 25 bases lacking the pointer, ruff at two F401 errors, the primary clone's
ignored `cam1753/cam1753-pages/` at 28 files and 50,316,747 bytes; one figure re-measures
differently (finding 6.2). The update file's eleven recorded decisions and the plan's disposition
map agree in substance. Each of the seven remediation commits changed what its message and the plan
say: `e805bce0` "Add live-update pointers to receipt bases" the 25 bases and the new lint;
`b6f29b8d` "Adopt one live update per receipt" the plan's §4.1 wording in all eight named surfaces,
the close-out list kept in `doc/periodic-review.md:324–329` with `doc/dual-agent-review.md:145–148`
pointing to it, the date-shaped census pathspec, the retired "Dispositions after remediation"
section, and the docstring's "An update file is live while its base remains tracked"; `e776318e`
"Restore research receipts and correct live prose" the two reports restored to their pre-move bytes
plus the pointer (`b8fc419f…` and `b7944176…` with line 4 removed), the six meteg-after-silluq
update files and `doc/metsudah-vs-ctr-update.md` given their entries, and every §5.3 wording landed
— "UXLC 3.9 has a meteg on … This records the transcription; it does not establish what the
Leningrad Codex manuscript has" at `doc/lam-2-3-akhla-snips/README.md:70–72` and `:171–173`,
"Mikra'ot Gedolot ha-Keter" at `:67`, `:105` and `:148`, "sheva" and "nor does", "verse-final atom"
at the five crop descriptions of `doc/meteg-after-silluq-snips/README.md` and "verse-final word"
nowhere, "the WLC 4.22 prose verses" in `doc/mega-timing-2026-09-11-update.md:26–28`, "have the
מ:כפול" at `py/versification_and_cantillation/strands.py:5`, and `README.md:87`'s colon; the one
§5.2 item is finding 1; `155bb778` "Resolve incremental MAM-simple inputs explicitly" the resolver,
the tier-3 wording in `py/product_scopes.py:25–27` and `:46–48`, the lint boundary in
`py/tests/test_product_scopes.py:15–17`, and 37.6 MB in both MAM-simple documents with "39.0 MB" in
neither; `82ad4b57` "Harden atom lookup and Git filename lint" the two F401 imports gone,
`py/main_repo_util.py` reconfiguring both streams, `py/subcommands/diff_mpplus.py:61` naming
`--full-history`, `py/main_verse_links.py:162` testing `"letters"`, and
`py/main_uxlc_estimate_atom_loc.py Genesis 1:2 על` exiting 1 with "Ambiguous: 2 letters-only
matches", the 14 atoms numbered and the `py/main_verse_links.py Genesis 1:2 --atom N` command,
whose syntax `--help` confirms; `61e01681` "Correct canonical user configuration" the `.codex`
spelling at nine sites, "## Delegate bounded work when it helps" in the Claude user-level file, "##
Final messages begin with one H1 report heading" in the Codex one, the hook's inventory with no
count, and the deployment paragraph that replaces the retired write-back in
`doc/dual-agent-review.md:532–535`; `71f96ca3` "Repair live retirement plans" both plans
agent-neutral with their decisions attributed to Ben and dated, C1's primary-checkout paragraph and
C2's 36-title inventory, whose pinned facts re-measure (both `out/diff_mamws_mamgo*.json` are `[]`;
each of the eight CSV rows has `תתת` in its second field and a `/צורות נוספות` target;
`ch2.mediawiki`'s Decalogue table runs from line 362 to 386). The 14 change sites of
`doc/review-findings-2026-09-10-update.md` are each true at the anchor, the finding-20.9 rewrite at
`:880–882` of the Leningrad subsections only (finding 1): the restoration statements, the
"substantive bytes match historical blob …" rewrites (the search report minus line 4 hashes to
`5c4aaf4c…`, the screen report to `a46dbf0f…`, `doc/PLAN-mega-coverage.md` to `dee11fb2…`), the two
historical censuses at `d34afb44` and `974395f9` figure for figure, the vendoring deletions dated
to `25bcabf6`, and the finding-10 entry's new "Recorded by" line. The D12 census over the 41
modified `doc/` paths: 23 finished documents, every one changed by exactly the authorized edit — 15
by the pointer alone (the anchor blob minus line 4 equals the start blob), 5 by the
opening-paragraph join plus the pointer with the text unchanged
(`doc/PLAN-worktree-file-consolidation.md`, `doc/assessment-two-stranded-artifacts-2026-09-09.md`,
`doc/mega-coverage-2026-09-10.md`, `doc/mega-timing-2026-09-11.md`, `doc/metsudah-vs-ctr.md`; a
sixth receipt joined the same way, `doc/mega-timing-cloud-2026-09-14.md`, is outside this census
because the window added it), 2 restored to their pre-move blobs plus the pointer under Ben's
decision 3 (`doc/meteg-after-silluq-job-4-12.md`, `doc/meteg-after-silluq-psalms-72-15.md`), and
the live `doc/user-level-config-in-cloud-sessions.md` — and 18 live documents changed as live
documents may be; the 12 update files the window created or changed all read `State: open, first
entry <date>` or `first entries`, and each entry names the passage it corrects by its words. The
`State:` census over the 127 `doc/**/*.md` files at the anchor: 27 plans of which 24 have a line-3
`State:` and 21 a declared word, the six exceptions being the six the 2026-09-14 review's finding
7.1 named and Ben decided to leave; 12 reviews, 9 blind counterparts, 4 numbered turns and 25
update files all with a line-3 `State:`, every non-declared form older than the window and
preserved by D10 rule 4; 77 `State:` lines in all, 76 at line 3 and one inside quoted text at
`doc/review-findings-2026-09-08.md:43`, which predates the window. The receipt lint
`py/tests/test_receipt_update_links.py` passes, checks physical line 4 against the exact pointer,
fails on an empty `doc/`, and does fail for an update file whose base is gone; what it cannot see
is an edit to a finished document other than the pointer, an update file's own claim about its
base's blob (finding 3.1), and a live document with an update sibling (finding 2.2). The 2026-09-14
review's finding 9, the `leningrad/page-snips/` example in #278's body, was done on GitHub 90
seconds after the anchor, as the tree-health "Issues" bullet records (`A_01` to `A_12`).

**The window's code (stream B).** `py/mb_cmn/new_york_time.py` converts correctly across both 2026
DST boundaries in 19 cases and refuses a naive timestamp; `tzdata` is needed on this machine
(`zoneinfo.TZPATH` is empty) and `zoneinfo` loads it itself; the docstring's claim that the seven
`MAM-parsed/historical/manifest.json` dates are New York dates re-measures through `gh api` against
GitHub's committer times, 0 mismatches. The change log's tree sentence is true (`git log
--full-history --find-object=2072b5f9… -- MAM-parsed/plus` lists `73c6b113`, `2239cbad` and
`209b4c05`), every change-log date is labelled and the unlabelled end-of-range strings are release
names, the Holman and printed-Decalogue dates are converted from offset-bearing timestamps and
labelled (140, 34 and 1 labels), and the four sites `25e7d35d` changed reach no page and each
states its zone. `_commit_date`'s docstring in `py/subcommands/diff_mpplus.py:56–70`, which the
2026-09-14 review's finding 10.3 called stale, is true now, the `--full-history` walk having been
replaced by a tree id; no staleness key decides regeneration, the outputs read no clock. The lint
`py/tests/test_explicit_time_zones.py` flags the clock reads and date placeholders it says it does
and passes; what it cannot see — a bare-imported clock function, a format string assembled by
concatenation, Python outside `py/`, a date read from data and shown unconverted, an authored
literal date — was verified by reading its extractor. The vendoring removal is complete: of 475
lines at the anchor containing "vendoring", 260 are in dated receipts and plans and the 5 under
`py/` are past-tense prose; `_STEPS` went from 55 to 54 and `_GENERATOR_ENTRY_POINTS` from 43 to
42; `py/repo_util/maintenance_policy.py` still reads the three keys the trimmed
`in/vendoring_policy.json` keeps; the two `file_io.py` files are one blob, `d6fee875`, and the
mega's `mam-simple` step now enforces that identity. `py/main_github_issue_edit.py` handles its
arguments as the skill describes, reconfigures both streams, reads its edits file as UTF-8, and
every former `wlc_issue_edit` mention is repointed apart from a frozen 2026-09-10 baseline JSON
that no code reads. `py/mb_cmn/mam_simple_book_group.py` is the one resolver, closed on `fmt` and
`vtrad`, raising `FileNotFoundError` naming every path tried, called by the two product generators
and by `py/accgram/mam_simple_verse.py`, and no `py/*.py` builds a book-file path on a tradition
directory itself. All 28 real filename-returning git commands in tracked `py/` carry `-z` (finding
4 is about how many the lint can see). `py/product_scopes.py` declares 42 entry points, 18 wrapper
delegates and the 5 product directories `AGENTS.md` lists, and neither `AGENTS.md` nor `README.md`
states a step or entry-point count. The changed tests are the sanctioned shapes. The Graphviz
environment check returns the pinned 16.0.0 with Helvetica loading; with `dot` absent the mega
raises before any step outside a cloud session; the temporary-file SVG move is `os.replace` and the
temporary file is unlinked on failure. The LCI field rename reached its writer
(`py/uxlc_lci/uxlc_lci_augrec.py` and its duplicate `py/py_uxlc/my_uxlc_lci_augrec.py`), its output
(982 records, 0 old-name and 1,964 new-name lines), `py/uxlc_paths.py:39–46` and
`uxlc/doc/clc-design.md:277–281`, and no reader of the old names remains; the generator is
`py/main_write_page_break_info.py`, step 36 of 54. The cloud hook parses under `bash -n`, is
registered on `startup|resume|compact`, exits 0 before reading any file unless
`CLAUDE_CODE_REMOTE=true`, installs whichever of its three resources are absent, the `hebrew-prose`
skill being the only skill among them, reports against the filesystem, and never exits non-zero, as
`AGENTS.md`'s paragraph says. The Codex worktree retirement preflight refuses a target that is not
an exact worktree root, another common directory, the primary worktree, a path outside
`~/.codex/worktrees`, a locked worktree, the running checkout, any tracked or untracked change, an
in-progress merge or rebase, a HEAD not integrated into the default branch, any reflog commit no
ref contains, a `.novc` with tracked files, and ignored content outside `.novc` that is neither a
listed cache nor byte-identical in the primary, and two of those refusals were measured on real
Codex worktrees; execution re-verifies both fingerprints, moves `.novc` rather than deleting it,
and removes by unforced `git worktree remove` and `git branch -d`; nothing defaults to a
destructive action. `--sync-user-config --check` writes no live file;
`.generated/expected-user-wide-AGENTS.sha256` is generated into the temporary source tree on every
run, so it is never absent or stale; all eight new `py/main_repo_util.py` flags are in `--help`;
the group's modules break none of the code rules; `53f27e9f` replaced four local-zone clock reads
with New York time in stored records. The eleven targeted test modules: 54 passed (`B_01` to
`B_16`, `B_sub4_01` to `B_sub4_03`).

**The instruction files, the skills and the user-level deployment (stream C).** Each of the 26
sections of `CLAUDE.md` at `bca64824` (1,077 lines) has a home at the anchor — `AGENTS.md` (223
lines), one of the four skills or their references, `doc/mam-normal-mark-order.md`,
`holman/WORKFLOW.md` or `in/mam-ws-intro/README.md` — and of its 168 paragraphs the 75 that do not
survive verbatim were each read and classified; what was dropped is case history, dated counts and
enumerations that re-derive, and the two dated decisions of finding 11. The Codex user-level file's
rewrite from 1,298 to 273 lines routes every section to a compact counterpart or a skill, and its
"Load task-specific skills" section is the one Codex-only section owed no Claude counterpart. Every
`AGENTS.md` claim tested resolves: the four MAM-normal marks and the two `uni_denorm.py` functions,
`heb_alef_bet_to_ascii`, the thirteen `.mediawiki` files, the seven `doc/boj-*.md`, the two
`book-of-job/doc/` procedures, the two issue-rendering modules, the five product directories, the
required-sibling helpers of `py/mb_cmn/paths.py`, the cloud-only skip on
`py/tests/test_final_stress_vs_phonetic_mam.py:88`, and the hook's wiring. Of 2,851 backtick tokens
in 38 instruction, skill and procedure files, 447 tracked paths resolve exactly and 84 by unique
basename; every `--flag` beside a named program is defined in it; every quoted section title that
names a file exists there; the 29 `doc/` paths the two procedure documents cite exist. Figures: 20
tracked files in `dot-claude/` and 10 in `dot-Codex/`; 54 steps and 42 entry points; 17 deployment
destinations, the count the check printed; four shared skills in `dot-claude/shared-skills.txt` and
in `dot-claude/README.md`; five August 2026 timestamps in `in/mam-ws-intro/manifest.json`; 63 and
713 lines in the two Aleppo wiki files; 12, 15, 25, 4 and 9 files for the five review-file
patterns; `doc/periodic-review.md:180–182`'s 22 walk-through commits as 16 to the review file plus
6 to the procedure. The 2026-09-14 review's findings 8.1, 8.2, 8.3, 8.4, 8.7, 8.8, 8.9, 8.10 and
8.11 are fixed by `61e01681`, `b6f29b8d` or `71f96ca3`, 8.5 and 8.6 are resolved by the Codex
rewrite `b8214d3c` (the sections no longer exist), and 8.12 is partly fixed (finding 2). Every
in-window commit to either user-level file has its counterpart in the other or is owed none, with
the one exception of finding 10.2. The Codex startup hook
`dot-Codex/hooks/check_project_doc_budget.py` was run read-only five ways: against the real
`~/.codex`, `AGENTS.md` at 13,437 bytes fits the 32,768-byte budget with the fingerprint matching
and no problem; in hook mode it prints nothing; with a missing fingerprint, a wrong fingerprint,
and a 1,024-byte budget it reports each failure as `dot-Codex/README.md` says. The cloud hook was
exercised under Git Bash against fake homes: no output and no file with `CLAUDE_CODE_REMOTE` unset;
nine files installed and the three-resource banner on an empty home, every file `diff`-equal to its
source; the "already in place" banner on the second run. The live homes: `71f96ca3` is an ancestor
of `5cf01537` and no canonical configuration file differs between them, and an independent hashing
of every live destination against the anchor's blobs, made before the 12:39 redeployment the
tree-health section records, found 17 of 17 equal, the fingerprint being the SHA-256 of
`71f96ca3:dot-Codex/user-wide-AGENTS.md` (`C_01` to `C_05`, `C_hook_run0_local.txt`,
`C_hook_run1_install.txt`, `C_hook_run2_present.txt`).

**The product trees and the generated outputs (stream D).** Which generator writes each changed
file is settled from the step table and `NOT_IN_MEGA`: the 12 call-graph SVGs and 12 `.dot` files
by `tmpl-survey`, the 8 change-log files by `diff-mpplus`, the two Holman pages by
`verify-and-render-table` and `render-uxlc-corrections`, the printed-Decalogue page by
`accgram-generate-html`, `uxlc/data/lci_augrecs.json` by `uxlc-write-page-break-info`, the
MAM-simple `file_io.py` copy by the `mam-simple` step, `MAM-for-Sefaria/` and `MAM-OSIS/` by the
two hand-run generators, and the rest hand-authored. Two clean mega runs on the scratch worktree
(the main session's and stream D's, which recorded that the mega rewrote 1,152 of the 4,718 tracked
files, 566 of the 579 pages among them) leave every mega-written file in scope as its generator
writes it. The four hand-run generator commands — `py/main_mam4sef.py` in its three modes and
`py/main_mam_osis.py` — exit 0 and reproduce their products byte for byte, rewriting 160 tracked
files under `MAM-for-Sefaria/` and 27 under `MAM-OSIS/` and `gh-pages/MAM-OSIS/` with `git status
--porcelain` and `git diff --stat` empty afterwards; the 2026-09-14 review's finding 2.1 is fixed
by `155bb778`. The change log's `new_tree` equals `71f96ca3:MAM-parsed/plus`, its five named
releases and index carry labelled dates that equal the New York dates of GitHub's committer times
for all seven manifest commits, and the JSON has the shape `py/mb_diff_mpu/mpplus_json.py` writes.
All 14 Holman message dates and the 3 MAM-suggestion dates re-derive with `zoneinfo`, including the
two that move back a day, and the Decalogue page's one date is the New York date of its stored
timestamp. Over the 579 pages, 1,062 date-shaped strings: 201 labelled on 10 pages, 800 names, 52
UXLC change ids in `title=` attributes, and 9 unlabelled shown dates (finding 15). The five product
documents' links and fragments resolve, their folder contents match (24 files in each `-vtrad-mam`
folder, six book groups in `-vtrad-bhs`, five in `-vtrad-sef`), and the MAM-simple size figures
reproduce exactly: 63,269,926 bytes at `3b1adf45^`, 37,645,076 at `3b1adf45`, the deleted files
24,287,554, the `yeivinID` removal 1,340,200, 37,648,182 at the anchor; the two hand-run products
were last committed at `209b4c05` and are byte-identical to a fresh regeneration, so "can lag" is
true as a possibility with the lag nil today. `MAM-parsed/historical/README.md`'s six snapshots,
five flags and variable name exist. `in/mam-ws-intro/README.md`'s 13 files, manifest sizes, five
August timestamps, `fr-ws-intro` subcommand and the 63-line, 713-line and 97.1 per cent Aleppo-wiki
figures re-measure, and its body is byte-identical to the section `9002323b` moved apart from the
H1 and intro line. Both policy JSON files parse, every path they name exists, and their one reader
returns 6 frozen repos, 5 visibility entries, 7 package names and 6 override paths. In the four
product trees that differ between the anchors exactly 6 files changed, all README, doc or
example-support files. `holman/WORKFLOW.md`'s claims hold except finding 14: no tracked `.eml`, 0
e-mail-address-shaped strings in 57 files, the sender filter, four assets with their two JavaScript
copies blob-identical and the two CSS copies differing only at the generator's placeholders. The 12
call-graph `.dot` files differ across the window by exactly their node `fontname` line and the SVGs
by the dropped `SBL Hebrew` family, labels, titles and tooltips identical (`D_01` to `D_13`).

**Prose, mark order, links and the new documents (stream E, with three sub-streams).** The
`hebrew-prose` skill and its references were loaded before reading. The mark-order and link
censuses are the tree-health section's. The banned-term scan over the 12,445 added lines of the 152
touched `.md`, `.html`, `.py` and `.json` files, each hit read with `git blame` and compared
against the files at `bca64824`: every hit for "witness", "cantillation accent", "proclitic",
"word-division", bare "Simanim", "the Keter edition", "the latter", "prose books" or "poetic
books", "patax", "dexi", "ga'ya", "hataf", bare "L" or "A", "Leningrad has" and a loose "word" in
accent context is a quotation of the rule or of a passage corrected, an identifier, a filename, the
skill's own table, or the text of a restored receipt; "carry" with an accent as object, "hyphen"
and the transliteration holdouts score 0. Of the 249 added heading lines each names its subject,
apart from the numbering left over across the split github-issues references (finding 9.3) and the
heading `## Result` at `doc/codex-review-findings-2026-09-14.md:16` (finding 17.2); the 165 added
lines announcing a count were checked against their lists where they fall in the assigned documents
("Three things", "five of the thirteen pages", "all thirteen files", "four authored … assets",
"five differences", "three parts", "all nine pages"), and match. Every changed statement of the
reader-facing documents is true at the anchor: the MAM-simple size sentence (63,269,926 bytes at
`3b1adf45^`, 37,645,076 at `3b1adf45`, 24,287,554 deleted, 1,340,200 of `yeivinID`, 37,648,182 at
the anchor, which is 37.6 MB), the two products' reading rule, the historical manifest's New York
dates, the root README's colon, `uxlc/doc/clc-design.md`'s six LCI keys, and the two snips READMEs.
The 2026-09-14 review's findings 2.3, 11.1, 11.3, 11.4, 11.5 and 11.6 are fixed inside the window
by `155bb778` and `e776318e` — "UXLC 3.9 has a meteg on … This records the transcription; it does
not establish what the Leningrad Codex manuscript has", "Each section records the crop's available
provenance", "have the מ:כפול", "Mikra'ot Gedolot ha-Keter", "sheva", "nor does", "the verse-final
atom" — and 11.2's correction is recorded in `doc/mega-timing-2026-09-11-update.md` rather than
made in the receipt. The window's accentuation docstrings and rendered hunks conform: the
`retrieved` and `revision_timestamp` docstrings match the JSON they describe; the one rendered
change of `gh-pages/wlc/accgram/printed-decalogue.html` sits in a paragraph whose first strong
character is Latin; the two Holman pages changed only in date labels and no Hebrew cell or
mixed-direction line was added. The two restored receipts equal their pre-move text plus the
pointer (`git diff a8e4790e^ 71f96ca3 -- <the two reports>` shows one insertion each). Sub-stream 1
re-derived every table, sum, ratio, median and "N of M" of the four timing documents from their own
numbers: the cloud record's tables foot (54 executed rows plus one skipped, per-step medians
summing to 249.0, the 235.0/207.6 = 1.132 ratio, 47 ratios with median 1.226), the laptop record's
55 rows foot to within the rounding of 0.1 s addends and its 262.9 s median re-derives, every
quotation the cloud update makes of the record is verbatim, and every restatement in
`doc/mega-timing-2026-09-11-update.md` and `doc/PLAN-mega-speedup.md` matches its source; what does
not hold is finding 16. Sub-stream 3 read the three 2026-09-14 turn records and the fourteen new
skill files as documents: none of the three records was edited after its first commit, each carries
`State: completed <date>; review only`, every announced count re-counts (the fifteen quiet
repositories, the eleven findings, C1's and C2's four additions each, the eight corrected
reconciliation rows, 4 + 24 + 8 = 36), every quotation and line citation in turns 2 and 3 re-reads
at the commit it names, stream credit matches the base review's attribution, and the three
`SKILL.md` frontmatters are well formed with 44 of the 45 paths they name tracked; what does not
hold is parts of findings 9, 11 and 19, and finding 17. Sub-stream 2 checked the two new plans
against every bullet of the user-level fresh-session checklist: all 34 commit hashes and 3 blob ids
resolve, every figure the mega-speedup plan quotes from the timing documents matches its source,
every tree claim holds at the anchor (55 steps at `bca64824` and 60 at `132f2f3e`, the four `_scan`
calls and three assertions of `py/accgram/post_stress_meteg.py`), its `git log --no-merges` command
lists exactly 14 commits, its claims about #272, #273 and #278 match GitHub, the remediation plan's
baseline table reproduces at `dab5d091` for every row needing no generator, and both plans date and
attribute their decisions, give absolute paths and the interpreter, name the skills to load, say to
re-measure, and warn of a live session; what does not hold is findings 6.4 to 6.6 and 18 (`E_00` to
`E_06b`, `E_sub1_*`, `E_sub2_*`, `E_sub3_*`).

## Findings

Findings 1 to 6 are the 2026-09-14 round's remediation and its records as they stand at the anchor;
7 to 11 the instruction compaction; 12 and 13 the window's code; 14 and 15 the products, the pages
and the Holman workflow document; 16 to 19 the prose of the window's new documents; and 20 the
method of this review series. Each lead says its disposition at `71f96ca3`. Nothing touches a
distributed product: the two `MAM-parsed/` trees and `MAM-with-doc/` are unchanged across the
window, the mega and the hand-run generators reproduce every generated file, and the pages differ
from `bca64824` only as the window's generators intend.

### 1. The plan's replacement for the crop-naming rule landed in the wrong sentence of both snips READMEs

**Partly unfixed at `71f96ca3`: the 2026-09-14 review's finding 3.4 is still the tree's shape.**
Stream A. That finding (`doc/review-findings-2026-09-14.md:636–646`) located the defect in each
README's general naming sentence, quoting "where the column and line have been established"
(`doc/meteg-after-silluq-snips/README.md`) and "where they have been read off the image"
(`doc/lam-2-3-akhla-snips/README.md`), and said that, read literally, those sentences do not allow
the two Leningrad crop names whose column is the estimator's. The plan
(`doc/PLAN-remediate-review-findings-2026-09-14.md:384–395`, §5.2) says "Replace the general
coordinate sentence in both READMEs with: A Leningrad crop may include both column and line when
Ben has read the line from the image; the section must say when the column comes only from the
estimator. For another source, include only coordinates established from its image or retained
index." At the anchor the general sentences stand as `a8e4790e` "Keep page crops by project, not by
manuscript; remove leningrad/" wrote them on 2026-09-13
(`doc/meteg-after-silluq-snips/README.md:10–12`, `doc/lam-2-3-akhla-snips/README.md:9–10`), and
`e776318e` "Restore research receipts and correct live prose" put the plan's text into each
README's Leningrad subsection instead (`doc/meteg-after-silluq-snips/README.md:41–44`,
`doc/lam-2-3-akhla-snips/README.md:43–46`), replacing the sentence "Ben does not report lines and
columns (2026-09-10), so a Leningrad crop's name has a column and line only where he gave the line
unprompted". So each README states the rule twice, the general sentence stricter than the rule Ben
kept on 2026-09-13 as his decision on the 2026-09-10 review's finding 20.9. One live record now
overstates the repair: `doc/review-findings-2026-09-10-update.md:880–882`, "The rule formerly
stated in `leningrad/page-snips/README.md` is preserved in the two live snips READMEs", is true of
the Leningrad subsections only. Re-establish: `git grep -n -e "have been" -e "read off the image"
71f96ca3 -- doc/meteg-after-silluq-snips/README.md doc/lam-2-3-akhla-snips/README.md`; `git show
e776318e -- doc/meteg-after-silluq-snips/README.md doc/lam-2-3-akhla-snips/README.md`;
`A_09_more_checks.py`, `A_11_last_checks.py`.

### 2. `doc/user-level-config-in-cloud-sessions.md` still describes a hook that installs two resources, and the plan says the document needs no edit

**Unfixed at `71f96ca3`; the 2026-09-14 review's finding 8.12 is partly fixed.** Stream C, with
stream A for 2.2. Two parts.

2.1. Three passages describe the hook as it was before `8065daec` "Preposition the cloud
user-instruction import target (#274)" (2026-09-14, in the window):

1. line 9, the hook "copies two of them into `~/.claude/` when that directory lacks them";
2. lines 145–146, "Two failures get their own banner — the files being absent from the checkout,
   and only one of the two landing";
3. line 149, "The hook installs two of the tracked trees and not the rest."

Since `8065daec` the hook installs three resources, one of them `~/.codex/AGENTS.md`, which stream
C measured under Git Bash against a fake `HOME` (nine files installed and a banner naming three)
and stream B traced statically after `bash -n`. `8065daec` changed the update file and not the
base; the base's two window commits, `05bdb5ed`, an ancestor of `8065daec`, and `e805bce0`, the
only one to come after the hook change, left the three passages; the update file's second entry
says three, so the two documents disagree; and
`doc/PLAN-remediate-review-findings-2026-09-14.md:653` says the document "is already corrected and
needs no further edit". Ben decided on 2026-09-15 that the document is live and kept true in place.
Re-establish: `git grep -n -E "copies two of them|only one of the two landing|installs two of the
tracked trees" 71f96ca3 -- doc/user-level-config-in-cloud-sessions.md`; `git grep -n "already
corrected" 71f96ca3 -- doc/PLAN-remediate-review-findings-2026-09-14.md`;
`C_hook_run1_install.txt`.

2.2. **Raised: a gap in the rule rather than in the document.** The same document, live by Ben's
decision, has had an update sibling since `1842e784` took it for finished on 2026-09-13, and
`e805bce0` joined its opening paragraph and inserted "Updates and later status: …" at line 4
because `py/tests/test_receipt_update_links.py` demands the pointer for every base of an update
file. Neither `AGENTS.md`'s rule nor the lint says what a live document with an update sibling is;
the sibling's lines 9–10 now say the source is live. Re-establish: `git show e805bce0 --
doc/user-level-config-in-cloud-sessions.md`; `A_03_d12_census.py`.

### 3. Sites in `doc/review-findings-2026-09-10-update.md` that the plan's audits required and left: four stale plan-blob assertions and one `.Codex` spelling

Stream A found one of the four assertions and the spelling; the pre-commit check found the other
three. Two parts, both in a live update file.

3.1. **Unfixed at `71f96ca3`.** Four entries for the 2026-09-10 review's finding 7.1 each say "The
finished plan remains unchanged at Git blob `<hash>`", giving the blob the plan had at `bca64824`,
and `e805bce0` changed all four plans by inserting the pointer:

1. lines 1116–1117, `bbd8c142…` for `doc/PLAN-remediate-review-findings-2026-09-08.md`, which is
   `0c84712d…` at the anchor;
2. lines 1172–1173, `bc60b785…` for `doc/PLAN-wikisource-derived-mam-products.md`, now `1efcd386…`;
3. lines 1229–1230, `85fd19f1…` for `doc/PLAN-efficient-wikisource-downloads.md`, now `adf39039…`;
4. lines 1276–1277, `5b8da2dd…` for `doc/PLAN-worktree-file-consolidation.md`, now `5d4c4572…`,
   `e805bce0` having also joined that plan's six-line opening paragraph.

The plan's §5.1 required auditing "every one of the 25 live update files for a present-tense
assertion that its base `remains unchanged` at a Git blob", and the window rewrote nineteen of the
27 such assertions that stood at `bca64824`, eighteen by `e776318e` and one by `b6f29b8d`,
seventeen of them into "substantive bytes match historical blob …; its only additional line is the
authorized update pointer". Eight stand at the anchor: these four, which the window made false and
its audit left; three about the plans' update siblings, which are true; and one, lines 1323–1324,
`abc06691…` for `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md`, which was
already false at `bca64824` and which the window did not touch, so it is noticed rather than found.
In seven of the eight the phrase wraps between "remains" and "unchanged at", which is why a
single-line grep for it, stream A's and at first this session's, prints one line and the class
looked like one site. Re-establish: `git grep -n -e "unchanged at Git blob" -e "^at Git blob"
71f96ca3 -- "doc/*-update.md"`; `git rev-parse` of each plan at both anchors;
`V1_03_assertion_counts.py`, `V1_04_remaining_assertions.py`, `V2_04_blob_assertions.py`.

3.2. **Unfixed at `71f96ca3`, low.** Line 52, in the entry "Inherited item 3: live user-level
synchronization is implemented", says in the present tense that `C:/Users/BenDe/.Codex/AGENTS.md`
and `dot-Codex/user-wide-AGENTS.md` have a given SHA-256, the measurement being anchored to
`a872790e`. It is the one `.Codex/` live-home spelling left on the surfaces the plan's §8.2 told
the executor to grep case-sensitively, and it was neither changed to `.codex` nor classified as
historical, which §8.2 required for any remaining spelling and which §4.5's "including the
occurrences near the anchors" already covered; `b6f29b8d` changed the three sites §4.5 named in
this file (lines 105, 684–687 and 1044 at the anchor) and not this fourth one, and `61e01681`,
which changed the spelling in nine other files, did not touch this file. Stream C read line 52 the
other way, as a historical path the plan told the executor to keep; the entry anchors its
measurement to a commit and marks no path as historical, so both readings are available, and this
finding takes stream A's. Re-establish: `git grep -n -E "\.Codex/" 71f96ca3 -- CLAUDE.md AGENTS.md
dot-claude dot-Codex doc/dual-agent-review.md doc/periodic-review.md py .claude/hooks
doc/PLAN-deferred-template-projection-decisions.md doc/review-findings-2026-09-10-update.md` (one
hit).

### 4. The broadened filename lint still would not flag six of the 28 filename-returning git calls, one of them the call the plan said it must cover

**Unfixed at `71f96ca3`, left by `82ad4b57` "Harden atom lookup and Git filename lint".** Stream B,
with the sixth call from the pre-commit check. `py/tests/test_tracked_filenames.py:103–119`:
`_wrapped_command` returns `None` when any argument after a wrapper's fixed parameters is not a
string constant, and `_git_wrappers` (lines 66–100) recognizes only a function whose own body holds
a list beginning with `"git"` and splats its variable arguments. So the lint extracts nothing from
`py/mb_diff_mpu/mpplus_revisions.py:164–177`, the `filenames` method whose `ls-tree` call passes
`self.commit` and `self.prefix + "/"`, which
`doc/PLAN-remediate-review-findings-2026-09-14.md:567–569` (§7.2) says the broadened pass "must
cover", nor from the four calls through `codex_worktree_retirement._git_ok` (lines 102, 159, 166
and 571), a wrapper that only forwards to `_git`. A sixth call it extracts and then drops:
`py/repo_util/codex_worktree_retirement.py:326`, `git grep -l -z -I -e .novc --`, because
`_returns_filenames` (lines 52–63) accepts only `ls-files`, `ls-tree --name-only`, `status
--porcelain`, `diff --numstat` and `worktree list`, and `git grep -l` prints filenames too. Of the
28 real filename-returning sites in tracked `py/` the lint extracts 23 and checks 22; every one of
the 28 carries `-z`, so no rule is broken today, and `AGENTS.md`'s
"`py/tests/test_tracked_filenames.py` enforces both rules" still overstates, as the 2026-09-14
review's finding 10.2 said of the older lint. Neither `doc/review-findings-2026-09-14-update.md`
nor the plan records 7.2 as done, so this is a gap in the fix rather than a false claim of one.
Re-establish: `B_15_lint_sees_which_calls.py`, `B_06_git_filename_cmds.py`,
`V2_01_git_filename_census.py`.

### 5. The one-live-update rule's homes disagree on what a receipt may receive, and the remediation held blob assertions to a standard it left other sentences below

Stream B's sub-agent and stream A. Two parts.

5.1. **Unfixed at `71f96ca3`, low.** `py/repo_util/check_repo_standards.py:221–222`, "A finished
dated document is immutable while tracked, apart from its one authorized line-4 update pointer",
and `doc/periodic-review.md:328`, "apart from its line-4 pointer", allow a receipt one
post-completion edit; `AGENTS.md:114–117`, `dot-claude/user-wide-CLAUDE.md:849–851` and
`dot-Codex/user-wide-AGENTS.md:154–156` allow two, the pointer "plus a mechanically necessary
joining of a prose paragraph that begins on line 3 without changing its text". All five were
written or rewritten by `b6f29b8d` "Adopt one live update per receipt", and `AGENTS.md` names the
docstring as where the retirement rules live; the join is what `e805bce0` did to six receipts and
one live document. Re-establish, with phrases that do not wrap: `git grep -n -e "authorized line-4
update pointer" -e "apart from its line-4 pointer" -e "post-completion edit" 71f96ca3 --
py/repo_util/check_repo_standards.py doc/periodic-review.md AGENTS.md
dot-claude/user-wide-CLAUDE.md dot-Codex/user-wide-AGENTS.md` (five sites).

5.2. **Raised, low; whether to reword is Ben's.** The plan's §5.1 had nineteen blob assertions
rewritten because the pointer "makes such an assertion literally false" (finding 3.1 has the four
it left), and left three sentences of the same shape that name no blob:

1. `doc/PLAN-close-out-review-2026-09-08-update.md:30–31`, "The finished close-out plan remains
   unchanged.";
2. `doc/mega-coverage-2026-09-10-update.md:9–10`, "The source analysis is a finished dated report
   and remains unchanged.";
3. `doc/review-findings-2026-09-10-update.md:284`, "Both finished source reports remain unchanged."

It also left the "is left exactly as written" sentence of 22 of the 25 update files, on lines 3–4
in 21 of them and on lines 5–6 of `doc/meteg-after-silluq-search-in-mam-documentation-update.md`,
among them `doc/review-findings-2026-09-14-update.md:3–4`, written in the window by `2e77d2fd` at
08:20 before `e805bce0` added the pointer at 10:02. Low because the policy text defines the pointer
and the join as the only post-completion edit, so a reader with the policy reads "left as written"
as "apart from the pointer"; the remediation nonetheless held the blob assertions to the literal
standard. Re-establish: `A_11_last_checks.py` sections 1 and 2.

### 6. The round's own records: two status claims overtaken inside the window, a baseline that counts a sub-heading as an entry, rewritten entries under their old attribution, and three smaller defects of the plan

Streams A, C and E each reached 6.1; stream A found 6.2 and 6.3; stream E's sub-stream 2 found 6.4
to 6.6. Six parts.

6.1. **Unfixed at `71f96ca3` as a statement in two live documents; corrected after the anchor in
one of them.** `doc/review-findings-2026-09-14-update.md:51–52`, written by `2e77d2fd` "Record
close-out decisions and neutralize review roles" at 08:20 on 2026-09-16: "A fresh-task remediation
plan with concrete editorial wording remains the next close-out phase, and no remediation named
above has begun." `doc/PLAN-remediate-review-findings-2026-09-14.md:3–4`, written by `d141e8cb`
"Plan remediation for September 14 review" at 09:07: "State: live; … Nothing in this plan has been
remediated yet." From `e805bce0` at 10:02 to `71f96ca3` at 10:48, seven commits executed the plan's
waves 1, 3, 5 and 6 and its waves 2 and 4 in part (findings 1 and 4 are what the two left), and
none touched either sentence, though the standards docstring says a `State:` line is written "in
the SAME commit as the phase work" and an update file is kept true. Wave 7, the #278 body edit, ran
on GitHub 90 seconds after the anchor. Outside the window: `6402de62` "Close the September 14
review record" (11:15) appended a completion entry to the update file and set its line 3 to a form
outside the `open` vocabulary, and `5cf01537` "Correct the September 14 review state record"
(11:46) restored `State: open` and put the sentence into the past tense; the plan's lines 3–4 read
the same at `5cf01537` as at the anchor. Re-establish: `git log --format="%h %cI %s"
2e77d2fd..71f96ca3 --first-parent`; `git show
71f96ca3:doc/PLAN-remediate-review-findings-2026-09-14.md`, lines 3–4.

6.2. **Raised, low.** `doc/PLAN-remediate-review-findings-2026-09-14.md:109` gives the Sept-10
update file's baseline as "39 headed entries; 38 `Recorded by` lines"; at the plan's checkpoint
`dab5d091` the file has 38 `## ` entries and 38 "Recorded by" lines, and at the anchor 38 and 39.
The plan's 39 is every heading below the H1, the 38 entries plus the one `### ` sub-heading, and
under that reading its row is arithmetically consistent: the sub-heading and the finding-10 entry
have no "Recorded by" line and the finding-11.5 entry has two. So the figure is a loose name rather
than a miscount. The row's remedy, a "Recorded by" line for the finding-10 entry, landed in
`b6f29b8d`. Re-establish: `A_06_plan_counts.py`; `git show
dab5d091:doc/review-findings-2026-09-10-update.md`, counting lines that begin `## ` and `Recorded
by`.

6.3. **Raised; no rule requires otherwise, and the authorship vocabulary is the reason to raise
it.** The entries of `doc/review-findings-2026-09-10-update.md` that `b6f29b8d` and `e776318e`
rewrote — the finding-20.1 and 20.11 censuses recast as historical, the finding-7.2 blob and the
finding-11.5 restoration statement among them — still open "Recorded by Codex on 2026-09-12" or "…
2026-09-13" above sentences the remediation's executor wrote on 2026-09-16, with no mark of the
rewrite; D12 authorizes correcting a stale present-tense claim in place and prescribes no marking.
No tracked record names that executor's agent: `b6f29b8d` and `e776318e` carry subject-only
messages with no trailer, the plan's templates say `<Claude|Codex>`, and the one record of the same
execution that names an agent, the comment on #278, says "Written by a Codex session". The new
2026-09-16 entries of the Job 4:12, Psalms 72:15 and Metsudah update files and of
`doc/mega-timing-2026-09-11-update.md`, and the two 2026-09-14 entries of
`doc/mega-timing-cloud-2026-09-14-update.md`, carry a date in their heading and no author line.
Re-establish: `git blame -L 640,647 -s 71f96ca3 -- doc/review-findings-2026-09-10-update.md`
(attributed to `b6f29b8d`) against the "Recorded by" line above those lines.

6.4. **Unfixed at `71f96ca3`, low.** Three anchors the plan gives are not verbatim strings of their
files at its checkpoint `dab5d091` or at the anchor:

1. line 187's `Retiring a finished document` occurs nowhere in
   `dot-claude/skills/github-issues/references/reading-and-writing.md`, whose section is "## 5.
   Correcting references before a tracked document is retired";
2. line 498's `That reads MAM-simple` was "That reads `MAM-simple/`, so regenerate";
3. line 362's `the live rule in leningrad/page-snips/README.md remains unchanged` was "The live
   rule in `leningrad/page-snips/README.md` therefore remains unchanged."

The executing commits found all three passages, so the effect was nil; what the three fail is the
fresh-session checklist's searchable-anchor bullet. (Sub-stream 2.)

6.5. **Unfixed at `71f96ca3`, low.** Lines 28–30 tell the plan's executor to load the
`codex-worktree-tasks` skill first, "for the shared-worktree checks, integration boundary, and the
prohibition on using Codex retirement tooling on a `.claude/worktrees/...` checkout"; that skill is
tracked under `dot-Codex/skills/` and deployed to `~/.agents/skills/` only, so no Claude session
loads it as a skill, the plan names no path, and its own §9.1 (line 681) says to load it only when
the assigned checkout is Codex-managed. The prohibition is in `references/task-lifecycle.md:69–70`.
(Sub-stream 2.)

6.6. **Unfixed at `71f96ca3`, low.** The plan names its own executor four ways — "the executing
task", "the root agent", "the remediation task", "this remediation" — while "the executor" names
the executors of the two retirement plans; and its heading "### 7.3 Remaining four actionable
source gaps" (line 572) reuses the approved package's phrase "the four actionable source gaps",
which the 2026-09-14 review's reconciliation row for finding 10 uses for 10.1, 10.2, 10.3 and 10.7,
for a different four: 10.3, 10.7 and the two unused imports, 10.1 being in §4.4 and 10.2 in §7.2.
(Sub-stream 2.)

### 7. The deployed `mam-repository-topology` skill tells its reader to apply exclusions and gists that the rule it cites says do not exist

**Unfixed at `71f96ca3`, new in `9002323b` "Compact repository instructions into skills and
references", and deployed to both live homes.** Stream C.
`dot-claude/skills/mam-repository-topology/SKILL.md:24`: "Apply every clause of
`gitrepos_setup_rule`, including its exclusions and its listed gists." Clause 4 of that rule
(`in/repo_maintenance_policy.json:63`) says "CLONE NOTHING ELSE. There is no exclusion list to
consult and no GitHub enumeration to filter", and the rule's `gists` comment (line 68) says
"Neither is in any workspace file, so under clause 1 neither is cloned on a fresh machine";
`doc/PLAN-repo-maintenance-across-GitRepos.md:30–34`, the correction of 2026-09-09, says "do not
add gist clones". A reader who applies the skill's sentence clones the two gists Ben's decision of
2026-08-31 keeps off every machine. The sentence resembles the superseded paragraph that still
stands above its correction at `doc/PLAN-repo-maintenance-across-GitRepos.md:21–28`, "Apply every
clause, including the frozen-repository and keep-absent subtractions and the two added gist
clones", which predates the window. Both live copies of the skill, under `~/.claude/skills/` and
`~/.agents/skills/`, carry the sentence at line 24: they equalled the anchor when stream C hashed
them, and from 12:39 on 2026-09-16 they equalled `7014cfbb` "Unify worktree retirement across owner
selection scopes", a commit outside the window that changes the skill's line 22 and not its
line 24. Re-establish: `git grep -n "including its exclusions" 71f96ca3 -- dot-claude`; `git show
71f96ca3:in/repo_maintenance_policy.json`, lines 57–71.

### 8. Three claims the compaction moved out of `CLAUDE.md` were true there and are false in the documents they moved to, and a bare `#1` it moved breaks the rule the same commit wrote

**Unfixed at `71f96ca3`; all four moved verbatim by `9002323b`, which moved sections of `CLAUDE.md`
into standalone documents without re-reading them in their new place.** Streams C, D and E. Four
parts.

8.1. `in/mam-ws-intro/README.md:30–31`: "This tree is exempt from the mark-order rule at the top of
this file." The README has no such rule; the sentence was `CLAUDE.md:173` at `bca64824`, where the
first section was the mark-order rule, which now lives in `AGENTS.md` ("Hebrew marks go in
MAM-normal order, not Unicode-normal order") and in `doc/mam-normal-mark-order.md`. Re-establish:
`git grep -n "at the top of this file" 71f96ca3 -- in/mam-ws-intro/README.md`; `git grep -n "at the
top of this file" bca64824 -- CLAUDE.md`.

8.2. `in/mam-ws-intro/README.md:46–47` and
`dot-claude/skills/mam-repository-topology/references/evacuated-repositories.md:200–201`: "Phase 3
of `doc/PLAN-mega-coverage.md` names every file removed". Phase 3's record,
`doc/PLAN-mega-coverage.md:83–94`, says "64 files deleted and 20 edited, `CLAUDE.md`,
`py/ac_paths.py` and `py/repo_scopes.py` among them" and lists no deleted file; the list is `git
show --stat 985262e2` ("Remove the Wikisource index generators, the column plots and fr-sefaria").
Both sentences were `CLAUDE.md:190` and `:786` at `bca64824`, written by `985262e2` on 2026-09-10.
The same sentence stands at three more sites that commit wrote and the window did not touch,
`py/ac_paths.py:21`, `py/repo_scopes.py:29` and `py/subcommands/download_wikisource_intro.py:33`,
which are noticed rather than found. Re-establish: `git grep -n "names every file removed"
71f96ca3` (five lines, the two of this part and those three); `git grep -n -e wikisource_page -e
lenin_wiki -e ac_wiki -e download_sefaria 71f96ca3 -- doc/PLAN-mega-coverage.md` (nothing).

8.3. `doc/mam-normal-mark-order.md:67–69`, in a document that calls itself "This current reference"
and is kept true in place: "`codex-index-aleppo` and `codex-index-cam1753` carry near-verbatim
copies of the deleted wording, both pointing back at `uni_denorm.py` in this repo". Read on
2026-09-16 with `gh api repos/bdenckla/<repo>/contents/CLAUDE.md`, codex-index-aleppo's `CLAUDE.md`
is a short redirect-host note and codex-index-cam1753's a short breadcrumb, and no line of either
mentions mark order, NFC, normalizing or `uni_denorm`; the repository's own topology reference
calls the first "a redirect host" and dates the second's move to 2026-09-04. The sentence was
`CLAUDE.md:65–67` at `bca64824`; a dated past tense is the shape of the fix. The surrounding "This
section is back, not new" (line 66) is written from `CLAUDE.md`'s point of view and says nothing
false. Re-establish: `E_05_sizes_keys_remote.py`, whose copies are
`E_05_codex-index-aleppo_CLAUDE.md` and `E_05_codex-index-cam1753_CLAUDE.md`.

8.4. **Low.** `in/mam-ws-intro/README.md:28` writes `source #1` of `doc/sigil-decoding.md`, a bare
`#1` for a number that is not an issue, against rule 2 of `AGENTS.md`'s "Issue citations in
MAM-basics" (`AGENTS.md:89`), a rule `9002323b` wrote in the same commit that moved this sentence;
the referent is item 1 of the numbered list under `doc/sigil-decoding.md:99–103`. The form stood at
`CLAUDE.md:171` at `bca64824`, so this part is a moved form rather than a claim that was once true.
Re-establish: `git grep -n "source #1" 71f96ca3 -- in/mam-ws-intro/README.md`; `git blame -L 89,89
71f96ca3 -- AGENTS.md`.

### 9. Cross-references the compaction left pointing at headings, quotations and paths that no longer exist, and a section numbering the split broke

**Unfixed at `71f96ca3`, minor; the moved sites are raised rather than found.** Streams C and B and
stream E's sub-stream 3. Six parts.

9.1. Five references name sections the window renamed, moved or deleted:

1. `dot-claude/skills/github-issues/references/citations.md:10` "MAM-basics' `CLAUDE.md`, "Five
   issue trackers", lists the collisions", a heading that at the anchor exists only at
   `references/mam-basics-trackers.md:5` of the same skill, where `9002323b` put the section in the
   very commit that wrote this sentence, `CLAUDE.md` being one line and `AGENTS.md` having no such
   section;
2. `references/state-changes.md:46–47` "item 1 of "Two axes of risk" in `~/.claude/CLAUDE.md` and
   `~/.codex/AGENTS.md`", where `b8214d3c` "Trim Codex user instructions with skill routing"
   renamed the Codex section "Risk has two independent axes";
3. `state-changes.md:49–50`, which says the section stood in both files under the heading "Never
   change an issue's state without a comment saying why", "which stays there as a pointer to this
   skill", true of the Claude file and not of the Codex file, where `b8214d3c` folded the pointer
   into "Load task-specific skills";
4. `references/reading-and-writing.md:79–80` ""Running scripts — no inline one-liners", in
   `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`", the Codex section now being "Shell, scripts,
   and file operations";
5. `doc/dual-agent-review.md:558–559` "the prerequisite section above records the September 9
   measurement", a paragraph `61e01681` replaced, the 1,106-line measurement being gone from the
   file.

Two sites outside the skills cite the same moved headings: `py/github_issue_edit.py:31–32`, written
by `c097ecfe` on 2026-09-14 when `CLAUDE.md:323` had the heading, sends the reader to
"`CLAUDE.md`'s "Five issue trackers""; `py/product_scopes.py:70–72` cites "Two axes of risk" for
both user-level files. `AGENTS.md`'s compatibility note says a citation of "`CLAUDE.md`'s section
X" means the matching section or the reference it now points to, and speaks of historical prose;
all seven sites are live text. Five of the seven were written inside the window, the four skill
sites and `py/github_issue_edit.py:31–32`; the other two, `doc/dual-agent-review.md:558–559`
(2026-09-09) and `py/product_scopes.py:70–72` (2026-09-12), predate the window and were made stale
by it, the first by `61e01681`'s replacement of the paragraph it points at and the second by
`b8214d3c`'s renaming of the Codex section. Re-establish: `git grep -n -E "Five issue trackers|Two
axes of risk|Never change an issue's state|Running scripts — no inline|September 9 measurement"
71f96ca3 -- dot-claude/skills doc/dual-agent-review.md py/product_scopes.py
py/github_issue_edit.py`, which also prints two lines that are not part of this finding,
`doc/dual-agent-review.md:473`, a sentence of 2026-09-03 about why that `CLAUDE.md` section kept
its name, and the historical clause at `mam-basics-trackers.md:127`; `git grep -n "^## " 71f96ca3
-- dot-Codex/user-wide-AGENTS.md AGENTS.md`.

9.2. **Raised.** Four stale paths at seven sites, all older than the window, which `9002323b` moved
verbatim into the new references: `mam-basics-trackers.md:162` and `evacuated-repositories.md:226`
cite `doc/PLAN-evacuate-the-rest-of-wlc-utils.md`, which `80c9ad85` "Close second-stage evacuation
bookkeeping" deleted on 2026-09-03, both in historical sentences ("Phase 10 of …");
`mam-basics-trackers.md:153` cites `doc/PLAN-evacuate-python-from-holman-ketiv-qere.md`, deleted by
`f6173fe3` on 2026-08-29; `mam-basics-trackers.md:139` says "`doc/clc-design.md` numbers its §9
open questions" in the present tense, the file having been `uxlc/doc/clc-design.md` since
2026-09-03, which lines 172–173 of the same file record; and `mam-basics-trackers.md:39`, `:69` and
`:148` write `io/table_row_github_issues.json` for `holman/io/table_row_github_issues.json`.
Re-establish: `C_05_paragraph_coverage.py` §4; `git log --full-history --diff-filter=D --format="%h
%cI %s" -- doc/PLAN-evacuate-the-rest-of-wlc-utils.md`.

9.3. The github-issues skill's three references keep one section numbering across three files, with
5 used twice, and their references by number broke with the split. `05bdb5ed` "Add the
github-issues skill, shared with Codex, and point the old rules at it" wrote the skill as one
`SKILL.md` of six numbered sections; `9002323b` put sections 1 to 4 in
`references/reading-and-writing.md`, section 5 in `references/state-changes.md` ("## 5. Closing,
reopening, relabelling and reassigning") and section 6 in `references/citations.md` ("## 6. Citing
issues"), keeping the numbers and the cross-references; then `0d82b4e6` added "## 5. Correcting
references before a tracked document is retired" at `reading-and-writing.md:123`. At the anchor
`reading-and-writing.md:55` "(section 5)" and `:76` "Item 5 of section 5 says why" mean
`state-changes.md`'s section, whose item 5 is the agent-written rule, while in their own file
section 5 is the retirement section, which has no item 5; `state-changes.md:15` "(section 3)" means
`reading-and-writing.md`'s section 3 without naming the file. Re-establish: `git grep -n -E "^##
[0-9]\.|section [0-9]" 71f96ca3 -- dot-claude/skills/github-issues`.

9.4. `reading-and-writing.md:70–71` says "of the cross-link quoted at the top", and the split
removed the quotation, which was line 8 of `05bdb5ed:dot-claude/skills/github-issues/SKILL.md` and
is in no file of the skill at the anchor. Re-establish: `git grep -n "why edit an existing comment"
71f96ca3 -- dot-claude` (nothing; at `05bdb5ed`, one line).

9.5. **Raised.** Two bare `#NN` forms in `mam-basics-trackers.md` name another tracker's issues,
against `references/citations.md:15–16` in the same skill: line 10, `#89–#93 were filed 2026-07-31`
(wlc-utils issues), and line 141, `issues #2 and #6` (UXLC-utils issues); both were `CLAUDE.md:328`
and `:459` at `bca64824`. Re-establish: `git grep -n -E "#89|issues #2 and #6" 71f96ca3 --
dot-claude/skills/github-issues/references/mam-basics-trackers.md`.

9.6. **Raised.** `evacuated-repositories.md:125–127`, a paragraph about `../wlc-utils` paths, sits
as the last paragraph of "## Cambridge 1753 data is local under `cam1753/`", as it sat under the
same heading at `CLAUDE.md:706–708`; the wlc-utils section (lines 26–73) is where it reads
correctly.

### 10. Two asymmetries between the Codex-side files and their Claude-side counterparts

Stream C. Two parts.

10.1. **Unfixed at `71f96ca3`.** `dot-Codex/README.md:49–51` names "The cross-agent
`github-issues`, `hebrew-prose` and `verse-links` skills" as the ones
`dot-claude/shared-skills.txt` declares; the declaration names four, `9002323b` having added
`mam-repository-topology` to it and to `dot-claude/README.md:107–108` without touching this
sentence, which `05bdb5ed` wrote on 2026-09-14; `61e01681` later edited this README for the
`.codex` spelling and left it too. The deployment itself is complete: the skill is installed under
`~/.agents/skills/mam-repository-topology`, and equalled the anchor when stream C hashed it.
Re-establish: `git show 71f96ca3:dot-claude/shared-skills.txt`; `git grep -n "cross-agent" 71f96ca3
-- dot-Codex/README.md`.

10.2. **Unfixed at `71f96ca3`; whether the Codex user-level file owes it is Ben's.**
`dot-Codex/user-wide-AGENTS.md:46–48` reads "A secondary worktree uses its existing local branch.
If a new Codex-managed worktree is detached, follow `codex-worktree-tasks` … Commit there without
pushing the worktree branch", with no exception; the exception Ben decided on 2026-09-15, that a
long-lived worktree branch whose merge is not scheduled for the session's archival is pushed to
`origin` after every commit as a backup, is in `dot-claude/user-wide-CLAUDE.md:121–130` and in
`dot-Codex/skills/codex-worktree-tasks/SKILL.md:22–32`, whose description scopes it to
Codex-managed worktrees. `aebb212c` "Allow backup pushes for long-lived worktree branches" wrote it
into those two files 77 minutes after the Codex rewrite `b8214d3c`. A Codex session working in a
Claude-made long-lived worktree, which is how every dual-agent round runs, reads only the flat
rule. Re-establish: `git grep -n -i "long-lived" 71f96ca3 -- dot-Codex/user-wide-AGENTS.md
dot-claude/user-wide-CLAUDE.md dot-Codex/skills/codex-worktree-tasks/SKILL.md`.

### 11. The compaction dropped two dated decisions from the instruction body, one enumerated detail and one date, and moved four undated attributions

**Raised, low; what the compaction kept is verified sound above.** Stream C and stream E's
sub-stream 3. Three parts.

11.1. Two dated decisions left the instruction body, which now carries neither: Ben's decision of
2026-09-12 that the two renamed Holman pages get no compatibility stubs and their old URLs may
break (`CLAUDE.md:76–79` at `bca64824`), and the fact, since 2026-09-11, that the mega writes
nothing outside the repository (`CLAUDE.md:922–927` at `bca64824`). Each still has a dated home in
the tree: the mega fact in `py/main_0_mega.py:12–16` and `doc/PLAN-mega-speedup.md:131–132`, and
the Holman decision in the comment at `in/holman_ketiv_qere_redirect_pages.json:2`.

11.2. The `hebrew-prose` skill's compaction kept "the first strong character of a line must be
Latin" (`SKILL.md:38–39`) and dropped the old `SKILL.md`'s enumeration of what is not strong, "A
RUNWAY HAS TO BE A STRONG LATIN CHARACTER, AND A SECTION SIGN, A DIGIT AND A BACKTICK ARE NONE OF
THEM" (lines 214–215 at `bca64824`); no reference names the three. Re-establish: `git grep -i
"section sign" 71f96ca3 -- dot-claude/skills/hebrew-prose` (nothing).

11.3. `dot-claude/skills/hebrew-prose/references/mam-basics.md:31–32` compacted "Ben chose this
sentence over editing the eight, 2026-08-10, as he chose the same answer for UXLC"
(`CLAUDE.md:268–273` at `bca64824`) into "Ben chose to document those stale citations rather than
churn them solely for the move", dropping the date and the count; and four attributions to Ben
moved without a date, `references/core-rules.md:71–72`, `:78–79` and `:97–98` (from the old
`SKILL.md`) and `evacuated-repositories.md:126` (from `CLAUDE.md:707–708`).

### 12. The Codex worktree retirement module does not refuse a directory junction, and its citation gate fires on every MAM-basics worktree

**Unfixed at `71f96ca3`, both introduced by `4530b32a` "Record safe Codex worktree retirement
policy".** Stream B's sub-agent, re-read by stream B. Two parts. Context: a Codex session was
co-present with uncommitted modifications to thirteen paths, this module among them, in
`C:/Users/BenDe/.codex/worktrees/bd89/MAM-basics` while the streams read; that work was committed
after the anchor as `7014cfbb` "Unify worktree retirement across owner selection scopes" (12:39 on
2026-09-16), which by its `--stat` reduces this module by about 1,135 lines and adds
`py/repo_util/worktree_retirement.py`. It is outside the window and was not reviewed, so whether
either part survives on `main` is not established here.

12.1. `py/repo_util/codex_worktree_retirement.py`: `_find_novc_directories` (lines 211–231) skips a
child only when `is_symlink()` is true; `_is_reparse_point` (261–266) is called only by
`_inventory` (lines 272, 282, 291) and `_measure_residue` (743, 751), and `_safety_snapshot`
(494–611) reaches it only through `_inventory` at line 591, on the `.novc` directories it has
already found, reading no reparse attribute of anything else; `_ignored_classification` (238–258)
marks an ignored file disposable when `_content_exists_elsewhere` (188–208) finds a byte-identical
file at the primary clone's same path, which a junctioned `.venv` always does; and line 1033
removes the worktree by `git worktree remove` without `--force`. Stream B's sub-agent probed a
junction `worktree/.venv` pointing at `primary/.venv` under a temporary directory:
`Path.is_symlink()` is False, `_is_reparse_point` is True, `git status --porcelain=v1 --ignored -z
--untracked-files=all` lists the junctioned files one by one, and `_ignored_classification` returns
them as disposable with no blocker. So a worktree sharing the primary clone's `.venv` by junction —
the case both instruction trees forbid, which the window's own
`dot-Codex/skills/codex-worktree-tasks/references/worktree-runtime.md:42–43` says worktree removal
"can follow", and which the 2026-08-03 masorah-books record in the user-level file says a plain
`git worktree remove` did follow, emptying the real venv — is classified as disposable and then
removed by exactly that command. Exposure was none when measured on 2026-09-16: none of the four
registered Codex worktrees, nor any other registered worktree of MAM-basics or phonetic-hbo, had a
top-level reparse point. A junction whose content is absent from the primary is a blocker, and a
junction named `.novc` is refused by `_inventory`. Re-establish: `B_sub4_02_junction_probe.py`,
which creates its junctions under a temporary directory in the session scratchpad and removes them;
`V4_02_reparse_census.py`.

12.2. `_tracked_novc_citations` (lines 325–357) runs `git grep -l -z -I -e .novc --` over the
retiring worktree's tracked files and collects every line containing `.novc`, which the preflight
prints (689–692); `ready_for_execution` (line 663) is false while any citation stands and
`--citations-reviewed` has not been passed, and execution refuses an unready preflight (924–927).
For a MAM-basics worktree whose tracked tree is `71f96ca3`'s that is 162 files and 2,470 lines,
beginning with the five `.gitignore` files, `README.md` and `aleppo/doc/aleppo-line-breaks.md`,
ignore patterns and docstrings that name the directory rather than citations into a retiring
worktree's `.novc`, where `doc/PLAN-repo-maintenance-across-GitRepos.md:583–585` promises
"references into every old `.novc` path". A gate that fires thousands of lines on every MAM-basics
worktree, 2,470 at the anchor, is one the operator always waives, and the recorded note cannot be
checked against the list. Re-establish: `B_16_novc_citation_count.py`.

### 13. Four small defects in the window's code

**Unfixed at `71f96ca3`, minor.** Stream B and its sub-agent, with 13.4 measured by the pre-commit
check. Four parts.

13.1. `--session-ended`'s refusal message (`py/main_repo_util.py:519`, "names no linked worktree of
the selected repos") and two docstrings (`py/main_repo_util.py:25–26`,
`py/repo_util/clean_worktrees.py:52`) still say "no linked worktree" after `4530b32a` narrowed the
test to Claude-owned worktrees (`git_worktree_cleanup.is_claude_owned_worktree`: a `claude/` branch
or a path under the main checkout's `.claude/worktrees/`), so a linked Codex worktree is refused as
if it were not linked. Wording only; the narrowing is the documented design. The same change left
`is_linked_worktree` (`py/repo_util/git_worktree_cleanup.py:858`) with no caller in tracked `py/`.

13.2. `py/tests/test_explicit_time_zones.py:83`'s per-site message, "uses git date placeholders
{dropped}, which drop the offset", is false for six of the twelve placeholders it rejects: `%ci`,
`%cd` and `%cD`, and their author-side counterparts `%ai`, `%ad` and `%aD`, carry the offset, while
`%cs`, `%ch`, `%cr` and `%as`, `%ah`, `%ar` drop it (`git show -s --format="ci=%ci | cd=%cd |
cs=%cs" 71f96ca3` prints `2026-09-16 10:48:07 -0400`, `Wed Sep 16 10:48:07 2026 -0400` and
`2026-09-16`). The rule itself is a whitelist and is fine. Introduced by `7fe0fb11` "Lint py/ for
clock reads and git date placeholders with no zone".

13.3. `py/accgram/mam_simple_verse.py:185–194` passes `vtrad="bhs"` as a placeholder when
`--mam-simple-dir` names a directory other than the three tradition folders, so the resolver's
`FileNotFoundError` names a tradition the caller never asked for; the paths it lists are right.
Introduced by `155bb778`.

13.4. `dot-Codex/hooks/check_project_doc_budget.py:120` reads the SessionStart JSON with
`json.load(sys.stdin)` and reconfigures only stdout and stderr (lines 283–284), so with stdin a
pipe a non-ASCII working-directory path in that JSON is decoded with the locale code page, cp1252
on this machine, with `surrogateescape`: measured under both interpreters, a UTF-8 `ü` reads as two
characters and a Hebrew letter as one character plus a lone surrogate, and the hook would then
report "SessionStart cwd is not a directory"; a JSON that escapes non-ASCII as `\uXXXX` is
unaffected. Stdin is read only when `--cwd` is absent (line 287), and the maintenance runner
(`py/main_repo_maintenance.py:172–178`) passes `--cwd`. Introduced by `52b91ac0` "Add Codex
instruction startup checks (#274)". Re-establish: `V4_04_stdin_encoding.py`.

### 14. `holman/WORKFLOW.md`, moved by the window, states a CSS rule the authored CSS has never met, and names two modules by paths that do not resolve

**Raised and not fixed; both older than the window in content and moved verbatim by `9002323b`.**
Streams D and E. Two parts.

14.1. Lines 29–30 say every authored Holman CSS theme "keeps each color in a `light-dark(<light>,
<dark>)` custom-property pair", and the two authored CSS files hold 10 colour literals outside any
such pair: `holman/assets/table_data_findings.css:49` (`.finding-badge { color: #fff; … }`) and
`:111–118` (eight `.cat-kind-*` and `.cat-issue-tag-*` badge backgrounds, `#1d6f6f` to `#6f7682`),
and `holman/assets/uxlc_corrections.css:60` (`.finding-badge { color: #fff; … }`). The literals
have been in the CSS since `3c5dc796` "Land Holman files in MAM-basics" (2026-09-03 09:01) and the
rule was written 33 minutes later by `ae663ff2` into `CLAUDE.md`, so the rule has been contradicted
since the day it was written; every `:root` custom property does use `light-dark(...)`. Which side
is wrong, the badge colours or the rule's "each color", is Ben's call. Re-establish: `git grep -n
-e "#fff" -e "#1d6f6f" -e "#6f7682" 71f96ca3 -- holman/assets`, which prints the four lines meant
and the two `--card-bg: light-dark(#ffffff, …)` lines, which are inside pairs;
`D_09_holman_workflow.py`.

14.2. **Low.** Lines 20 and 23 name `hkq_cmn/mam_suggestion_extract.py` and
`hkq_cmn/mam_suggestion_dispositions.py` without the `py/` prefix, where every other path in the
file (`.novc/eml/`, `.novc/eml-mam/`, `holman/emails/`, `holman/assets/`, `gh-pages/holman/`) is
relative to the repository root, so neither resolves from there; and line 21's "correspondence
among Ben Denckla and Avi Kadish" names two people. Re-establish: `git grep -n "hkq_cmn/" 71f96ca3
-- holman/WORKFLOW.md`.

### 15. Thirteen date-shaped strings show on seven pages without the New York label; five are hand-written citation dates on a page repository code writes

**Raised, not a defect of any generator; Ben's call whether the rule exempts them.** Streams D and
B, their two date shapes combined by the pre-commit check. The rule at `AGENTS.md:156–162`, "Every
date shown by repository code on a page or report is converted through `py/mb_cmn/new_york_time.py`
and followed by ', New York time'", a rule the window wrote (`d7d16486` "Record the New York time
rule in CLAUDE.md and Codex's instructions", moved into `AGENTS.md` by `f3c7b05e` and `9002323b`),
was checked against the 579 tracked pages rather than the code. With stream D's date shapes, of
1,062 date-shaped strings, 201 are labelled on 10 pages, 800 are names (filenames, hrefs, the
change log's release names as link text, UXLC change ids such as `2021.02.22-3`), 52 are UXLC
change ids in `title=` attributes, and 9 show without the label, on four pages:

1. `gh-pages/holman/table_data_findings_suppressed.html`, written by the `verify-and-render-table`
   step: `2026-08-28` four times and `2026-09-03` once, inside disposition prose from
   `py/hkq_cmn/mam_suggestion_dispositions.py` ("Ben Denckla accepted all thirty of Holman's meteg
   suggestions on 2026-09-03"; "Seth (Avi) Kadish, 2026-08-28: the geresh appears to have been
   erased"), the name-and-date citations `holman/WORKFLOW.md:24` prescribes for a disposition,
   written by hand and not derived from a timestamp. This is the one class the rule's wording
   covers and the tree does not follow.
2. `gh-pages/MAM-with-doc/sigil-decoding.html`: `2026-08-27` twice, "The corpus was repointed on
   2026-08-27"; a hand-authored page no step rewrites.
3. `gh-pages/MAM-for-Sefaria/index.html:14`: "Revision: 2025-06-26 / 30th of Sivan, 5785"; a
   hand-authored page no program under `py/` names.
4. `gh-pages/holman/uxlc_corrections.html`: "August 7, 2026" once, inside the quoted forwarded
   header of a message body, rendered as data.

Stream B's day-first abbreviated-month shape adds four strings on three more pages:
`gh-pages/MAM-with-doc/misc/notes_on_aliyot.html:12`, "Revision: 4 Oct 2021", an authored literal
at `py/author_misc/notes_on_aliyot.py:69–72`;
`gh-pages/MAM-with-doc/misc/urwotm_4_atnax_hafukh.html:188`, "In its 19 Oct 2021 release (version
1.3)", an authored literal at `py/author_misc/urwotm_4_atnax_hafukh.py:295`; and
`gh-pages/uxlc/clc/Genesis.html:462`, "28 Sep 2024" and "29 Sep 2024" inside a quoted UXLC change
note, rendered as data. A lint over Python can see none of the thirteen. Of the seven pages the
window changed only the two Holman ones; the finding is about the window's rule against the tree.
Re-establish: `D_06_date_scan.py`, `B_14_month_name_dates.py`, `V4_03_date_reclassify.py`.

### 16. The four timing documents: eight defects of the two receipts and the two update files, and one thing raised that is not a defect

Stream E's sub-stream 1, spot-checked by stream E and, for 16.1 and 16.3, by this session; each
part's disposition is at `71f96ca3`. `doc/mega-timing-cloud-2026-09-14.md` (`859c4b43` "Record
three cloud mega runs, and execute PLAN-mega-speedup's Phase 2") and
`doc/mega-timing-laptop-2026-09-14.md` (`fc06b4be` "Record four mega timing runs on a Surface
Laptop 4") are receipts, so a correction to either goes in its update file, of which only the first
exists; `doc/mega-timing-cloud-2026-09-14-update.md` (`742e988a` "Correct the cloud timing record:
the runs were on the wrong Python") and `doc/mega-timing-2026-09-11-update.md` are live. Every
table, sum, ratio and median of the four foots except as stated here. Nine parts.

16.1. **Unfixed.** `doc/mega-timing-cloud-2026-09-14-update.md:67–68`: "The record's advice to
prefer a virtual environment stands", and no version of the record contains such advice (`git grep
-n -i -e virtual -e venv 71f96ca3 -- doc/mega-timing-cloud-2026-09-14.md` finds nothing, and the
same at `859c4b43`); the advice is `doc/PLAN-mega-speedup.md:359–378`, written by `f579eeaf` "Amend
Phase 2's steps so they cannot repeat the wrong-Python run", a commit to the plan alone made 18
minutes after the update's `742e988a`.

16.2. **Unfixed.** The same update's headline "229.8 s against 248.9 s, comparing medians of the
warm runs of each" (lines 85–91) does not re-derive from the two 3.13 step-loop totals it prints,
230.0 and 229.4, whose median is 229.7, and `doc/PLAN-mega-speedup.md:305–306` restates it; the
3.11 side, 248.4 and 249.4, does give 248.9, and the 7.7 per cent holds either way. Either the
figure is a sum of unrounded per-step medians and the sentence names the wrong derivation, or it is
off by 0.1 s; the update prints no 3.13 per-step table to tell which.

16.3. **Unfixed, a receipt.** `doc/mega-timing-cloud-2026-09-14.md:18` says 249.0 s is "the median
of three runs"; the three runs' step-loop totals are 271.3, 248.4 and 249.4 (lines 111–113), whose
median is 249.4, and the record's own lines 121–122 take the 249.0 s as the base of each per-step
median's share, the Median column of its §3 table summing to 249.0.

16.4. **Unfixed, a receipt.** `doc/mega-timing-laptop-2026-09-14.md:44` and its "Started" column
(lines 164–167) give clock times with no zone or offset; they are local, `fc06b4be` being committed
at 15:52:01 -04:00, six minutes after run 4's computed end. A correction would go in a
`doc/mega-timing-laptop-2026-09-14-update.md` that does not exist.

16.5. **Unfixed, a receipt.** `doc/mega-timing-cloud-2026-09-14.md:124–126` says a blank "Cloud /
Ben" ratio means `diff-mpplus` and `gen-site` raised in the dated record, and seven executed rows
are blank: those two (lines 139, 142) and `find-uxlc-accent-changes`, `tmpl-survey-toy`,
`letter-small-job`, `map-changes-to-book-of-job` and `ac-gen-index-flat-annotated` (lines 173–181),
whose Ben figure is 0.0.

16.6. **Unfixed, receipts.** Three prose defects:

1. the cloud record's lines 313–323 list four modified files and continue "Both are the
   shallow-clone effects … and neither is a defect", the pair meant being named as a pair only at
   line 40;
2. its lines 86–95 announce "three separate facts" and give them as three bold-led sentences in one
   paragraph;
3. two finding-shaped leads carry no disposition, its line 74 "The packages had to be installed,
   and the plan's command for it does not work as written" (the plan's step was since amended, and
   the update's lines 73–75 say so, but the lead does not) and the laptop record's lines 86–91,
   whose "12 tracked files were still CRLF on disk" is left without saying what became of them.

16.7. **Unfixed.** `doc/mega-timing-cloud-2026-09-14-update.md:100` uses "the dated record", the
record's coinage for `doc/mega-timing-2026-09-11.md`, without defining it, beside the update's own
"the record" for `doc/mega-timing-cloud-2026-09-14.md`.

16.8. **Unfixed.** `doc/mega-timing-2026-09-11-update.md:26–28`, the entry `e776318e` added for the
2026-09-14 review's finding 11.2, names the passage it corrects by step name only and quotes
neither "prose books" nor the section (`doc/mega-timing-2026-09-11.md:245–246`, §4 item 7), and its
replacement sentence ends after "verses", so a reader cannot tell whether the rest of the original
sentence survives; the substance is right.

16.9. **Raised, not a defect.** Neither `doc/mega-timing-cloud-2026-09-14-update.md` (`742e988a`)
nor `doc/mega-timing-2026-09-11-update.md` (`afbdd878`) added a line-4 pointer to its base when it
was created on 2026-09-14, and none was owed: D12 then said of the base that "the document it
corrects is not touched", Ben decided the pointer on 2026-09-15, and `e805bce0` added it to all 25
bases on 2026-09-16 with the lint that now checks it. Stream E's sub-stream 1 reported this as a
rule broken and then repaired; the pre-commit check found that the rule did not yet exist.

Also raised and not a defect: `doc/mega-timing-cloud-2026-09-14.md:374–376` gives `git log -1 --
MAM-parsed/plus` as a re-establishing command without `--full-history`; in this full clone the two
spellings answer differently (`209b4c05` against `73c6b113` at `89f10bb4`), in the record's shallow
container both gave the boundary commit, so every stated figure is right.

### 17. The 2026-09-14 round's turn records: a remedy credited to C3 that C3 does not name, and two questions of form

Stream E's sub-stream 3, with 17.1 re-read by this session. The three records are finished, so a
correction goes in `doc/review-findings-2026-09-14-update.md`. Three parts.

17.1. **Unfixed at `71f96ca3`.** `doc/dual-agent-review-2026-09-14-turn-03-claude.md:147–148`: "Of
the two remedies C3 names, dropping the numbers … is the one that cannot go stale again." C3's two
remedies (`doc/codex-review-findings-2026-09-14.md:90`) are "refreshed or given an explicit
checkpoint", as the reconciliation's row 7 says too; "dropping" occurs only in turn 3. Dropping the
numbers agrees with Ben's decision on finding 7.4 but is a third remedy, and
`doc/dual-agent-review-2026-09-14-turn-04-codex.md:71–72` adopts it as "the recorded remedy".
Re-establish: `git grep -n -e "dropping the numbers" -e "refreshed or given" 71f96ca3 --
doc/codex-review-findings-2026-09-14.md doc/dual-agent-review-2026-09-14-turn-03-claude.md
doc/dual-agent-review-2026-09-14-turn-04-codex.md`.

17.2. **Raised, low; a wording question D9 does not settle.** No C-finding lead in the three
records states a fixed-or-unfixed disposition; each file states it once, file-wide (turn 2 lines
11–12, turn 3 line 20, turn 4 line 15), and turn 3's and turn 4's leads open with "Accepted.", the
reviewer's stance, where `doc/periodic-review.md:125–127` asks that each finding's lead say what
happened to it; and turn 2's heading `## Result` (`doc/codex-review-findings-2026-09-14.md:16`)
names no subject. Two announced counts in turn 4 are listed in prose rather than numbered, and
match their lists: lines 76–78, "turn 3's five results", and lines 90–97, "The eight
reconciliation-row corrections".

17.3. **Raised, low.** Three figures in turns 2 and 4 carry no re-establishing command:

1. `doc/codex-review-findings-2026-09-14.md:122–123`, Black 26.8.0 over 1,044 files and ruff's two
   F401 errors;
2. `:132` of the same file, the fifteen repositories' histories;
3. turn 4's lines 118–119, "Black and Ruff were rerun directly".

Turn 3's lines 177–186 later supplied the commands and found the Black version figure wrong. Two
more defects of reference: turn 3's lines 10–13 name five files and then "every passage quoted from
the last three"; and `doc/codex-review-findings-2026-09-14.md:13` calls C1 to C3 "the
counter-findings" where line 24 calls C1 and C2 "new findings" and line 11 calls the file "the
counter-argument".

### 18. `doc/PLAN-mega-speedup.md`: a second rounding of one tree, a sentence that counts a commit its own command does not list, no baseline suite count, and two loosely introduced names

**Unfixed at `71f96ca3`, low; a live plan.** Stream E's sub-stream 2. Written by `afbdd878` "Plan
the mega speedup work, and point the 2026-09-11 timing record at it" and ten later commits. Four
parts.

18.1. Lines 87–88 give MAM-simple's tree as "37.7 MB", from a `du -sb` at no named commit, where
the plan's own re-establishing method (lines 95–97, summing the sizes of `git ls-files -z --
MAM-simple`) gives 37.6 MB: 37,647,285 bytes at `bca64824` and 37,648,182 at the anchor;
`MAM-simple/README.md:37` and the 2026-09-14 review's finding 2.3 say 37.6 MB. Two live documents
state two roundings of one tree. Re-establish: `git grep -n "37.7 MB" 71f96ca3 --
doc/PLAN-mega-speedup.md`; `E_05_sizes_keys_remote.py`.

18.2. Lines 100–102 say "The other 12 include the MAM-simple commits above", and one of those five,
`b653e9b9` "Retire MAM-simple/misc/Torah-letters-only/", is not among the 14 commits the plan's own
command lists, having touched none of the eleven paths the command names; two of the twelve,
`8b2386b0` and `cde921bf`, that sentence does not name, the plan naming `8b2386b0` at its line 74
for the `diff-mpp` rename and `cde921bf` nowhere. The pre-commit check ran the plan's command over
`132f2f3e..bca64824`, the range the plan pins its figure to, and got the 14.

18.3. Neither this plan's "Preconditions" (lines 46–66) nor section 2 of
`doc/PLAN-remediate-review-findings-2026-09-14.md` states the baseline suite count, though
`doc/review-findings-2026-09-14.md:199` records 997 passed and 5 skipped at `bca64824`; and this
plan's "Implementing items 3 to 9 and 13 to 15" (lines 410–420) carries the mega and its diff,
black and one commit per item, and neither `git diff --check` nor a suite run, though every item
changes executable source.

18.4. In Phase 2, "the record" and "the update" name the cloud timing record and its update file
(lines 305, 316, 333) with no "call it" clause, line 300's "its record is
`doc/mega-timing-cloud-2026-09-14.md`, corrected the same day by
`doc/mega-timing-cloud-2026-09-14-update.md`" being their only introduction, beside "the dated
record" coined at line 21 for the 2026-09-11 record, which the heading at line 19 names a third
way. Also raised and not a defect: lines 51–52, 274, 405 and 418 cite "this repository's
`CLAUDE.md`" and two of its sections, which `f3c7b05e` "Use AGENTS.md as shared repo instructions
(#274)" moved to `AGENTS.md` inside the window; `AGENTS.md` carries both sections, and its
compatibility note covers the citation though it speaks of historical prose and this plan is live.

### 19. Smaller prose defects of the window's new and joined text

**Unfixed at `71f96ca3`, low; 19.5 is raised, being moved text.** Stream E. Five parts.

19.1. `doc/metsudah-vs-ctr.md:3` says "U+05AD HEBREW ACCENT DEHI on prose-book tipḥas", the "prose
books" form the `hebrew-prose` skill bans, in a line `e805bce0`'s paragraph join restated; the text
is the receipt's own (lines 5–6 at `bca64824`), so a correction, if wanted, goes in
`doc/metsudah-vs-ctr-update.md`, as the 2026-09-14 review's finding 11.2 was handled for
`doc/mega-timing-2026-09-11.md`.

19.2. `dot-claude/skills/hebrew-prose/SKILL.md:50` says the post-stress-meteg pages "use plain
"word" because their own introduction fixes the meaning", an "own" carrying no contrast, in the
file whose `references/core-rules.md:81–91` ("Cut own") bans it; written by `9002323b`, and the
live copy has the same line.

19.3. Formatting residue of `9002323b`'s split: 14 headings with no blank line before them
(`reading-and-writing.md` 23, 67, 90; `core-rules.md` 95, 115; `evacuated-repositories.md` 26, 74,
103, 113, 128, 144, 165, 185, 208) and eight unwrapped prose lines over 100 characters
(`mam-basics-trackers.md` 3, 10, 70; `evacuated-repositories.md` 3, 33, 49, 137; `core-rules.md`
11); CommonMark renders the headings, so no page changes.

19.4. `dot-Codex/skills/codex-worktree-tasks/references/task-lifecycle.md:120–121` writes two
backslash paths, "`C:\Users\BenDe\...` maps to `drive-C/Users/BenDe/...`" and "`\\server\share\...`
maps to `unc/server/share/...`" (`4530b32a`); the user-level rule allows a backslash where syntax
requires it, arguably the UNC prefix, and not for the drive-letter example, which maps the same way
spelled `C:/Users/BenDe/...`.

19.5. **Raised.** Two prose slips that `9002323b` moved from the old `hebrew-prose` `SKILL.md` into
`dot-claude/skills/hebrew-prose/references/core-rules.md`: lines 65–67 announce "Three exemptions"
and list them with dashes rather than numbers, and line 130 names three works and then writes
"either of the first two".

### 20. The census method for the other public repositories cannot see a commit pushed after it was made

**Raised, not a defect of any tree: a correction to this series' method.** This session. The
2026-09-14 review established the other public repos' silence with `gh api
"repos/bdenckla/<repo>/commits?since=<UTC time of the start anchor>"` for the GitHub-only ones and
`git log` for the two clones, and this turn's prompt prescribed the same. `since` filters by commit
date, and so does `git log --since`. phonetic-hbo's `8b134b6b` "Regenerate Phonetic MAM after the
Wikisource refresh" was committed on 2026-09-10 at 21:48 local and reached GitHub on 2026-09-15 at
17:25Z (`pushed_at`), after the 2026-09-14 review had recorded the clone at `10de7970`; both
queries return 0 for it, and only the commit range from the previous review's recorded head,
`10de7970..8b134b6b`, finds it. The commit itself verifies sound (the tree-health section's
"phonetic-hbo" bullet). What finds such a commit for a clone is the range from the previous anchor;
what shows that a GitHub-only repo had no push at all is `pushed_at` compared with the window,
which this review added and which the thirteen GitHub-only repos all pass. Re-establish:
`other_repos.py`, `gh_only_repos.py`; `git -C C:/Users/BenDe/GitRepos/phonetic-hbo log --format="%h
%cI %s" 10de7970..8b134b6b`.

### Noticed outside the diff, not findings

Things the streams saw while understanding the diff, each older than the window and not restated by
it: `py/subcommands/diff_mpplus.py:104` still says "`diff-mpplus`, step 6 of the mega's 60", where
the step table has 54 entries (it is still sixth); the change log's `unpinned-latest.html` says "71
changes found" while its JSON says `diff_count: 69`, by design, one being the expanded count and
the other the pre-expansion count; `py/py_uxlc/my_uxlc_lci_augrec.py` and
`py/uxlc_lci/uxlc_lci_augrec.py` are two live copies of one module, each with importers, which
`14722a34` edited identically; five receipts under `in/` (`in/mam_products_phase6*.json`,
`in/mam_osis_repoint_verification.json`) name the removed vendoring paths and
`py/wlc_issue_edit.py`, and nothing reads them; `py/tests/test_github_issue_edit.py` holds
example-based unit tests, renamed and otherwise untouched; `py/accgram/ctr_decalogue_fetch.py:14`
prescribes `PYTHONUTF8=1` in a tracked docstring; `py/author_misc/mp_cmn_groups_misc.py:177` has
"poetic-book formatting"; `doc/PLAN-repo-maintenance-across-GitRepos.md:20–34` keeps the superseded
roster paragraph beside its 2026-09-09 correction; `doc/dual-agent-review.md:473`, a sentence of
2026-09-03, still says "`CLAUDE.md`'s "Five issue trackers" section kept its name";
`dot-claude/skills/hebrew-prose/references/terminology.md:142` and
`dot-claude/user-wide-CLAUDE.md:1292` write
`MAM-with-doc/gh-pages/misc/he_ws_intro_to_mam_pasleg.html` for
`gh-pages/MAM-with-doc/misc/he_ws_intro_to_mam_pasleg.html`, in lines the window neither moved nor
changed; `doc/review-findings-2026-09-08.md:43` holds a second `State:` line inside quoted text;
`MAM-simple/doc/versification-differences.md` has seven fragment links whose GitHub anchors differ
from their headings'; the historical manifest's `migration.source_date` is read by nothing since
`b5dd2ffb` and is still right; and four unregistered Codex worktree directories
(`C:/Users/BenDe/.codex/worktrees/{22e6,b615,e530,fdaf}/MAM-basics`) hold only `.pytest_cache`
residue. Also noticed:
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14` and its branch
were retired while the streams ran, so the remediation plan's `.novc/` evidence (518 files,
59,766,437 bytes at plan writing) can no longer be read from disk, and the plan's §12 commands name
a path and a branch that are gone.

## Open ends the window itself declares (not findings)

`doc/PLAN-remediate-review-findings-2026-09-14.md` is `State: live` and was in execution at the
anchor: its waves 1 to 6 landed in the seven remediation commits, wave 7 (the #278 body edit)
landed on GitHub 90 seconds after the anchor, and the completion was recorded in
`doc/review-findings-2026-09-14-update.md` after the anchor by `6402de62` and `5cf01537`, outside
this window; its waves 2, 4 and 5 leave findings 1, 3 and 4 of this review behind, and its §8.3 is
the plan sentence finding 2.1 names. The 2026-09-14 review's finding 2.1 is fixed and its two
products regenerate, so the "not kept current" declarations in `MAM-for-Sefaria/README.md` and
`MAM-OSIS/README.md` now describe a lag that is nil today. `doc/PLAN-mega-speedup.md` is live with
its Phase 2 executed (`859c4b43`) and its remaining items open, tracked on #272 and #273, whose
bodies point at the plan; `doc/PLAN-retire-google-sheet.md` (#279) and
`doc/PLAN-retire-codex-index-image-work.md` (#281), made agent-neutral by `71f96ca3`, are live and
unexecuted; `doc/PLAN-dispose-mega-pipeline-review-findings.md` (#280) is live;
`doc/PLAN-deferred-template-projection-decisions.md` is `paused 2026-09-12` (#277);
`doc/PLAN-silluq-before-gaya-template.md` is live (phonetic-hbo#78). #274 is open: at the anchor
`dot-claude/user-wide-CLAUDE.md` is still the full user-level text rather than an `@`-importing
wrapper, which the cloud hook's comment and `doc/user-level-config-in-cloud-sessions-update.md`
describe as the still-open conversion. #278 is open. #284, filed on 2026-09-15 by a Claude session
and saying so, asks to remove `py/main_repo_maintenance.py`'s skip of the mega after a failing
suite, and the window did not change that behaviour (`py/main_repo_maintenance.py:80` at the anchor
still reads "The rebuild step is skipped if the test step failed, unless"). The Codex worktree
retirement's execution path has never run: `C:/Users/BenDe/.codex/worktree-retirements` did not
exist on 2026-09-16. `main` and `origin/main` stood at `b6aa79a8`, 35 commits past the anchor, at
11:46 local on 2026-09-17, minutes before this file was committed.

## What this review did not check

1. Anything in MAM-private or hbofonts, and so phonetic-hbo's generator, which lives in
   MAM-private's `al-hatorah/` tree: why Phonetic MAM now selects the second parameter of Psalms
   4:3's `מ:דחי` template was not examined, only that both parameters entered `MAM-parsed/plus`
   with the refresh.
2. The cloud container itself: the hook was exercised under Git Bash on Windows against fake homes,
   which tests every path through the script and the copy semantics, not the container's `bash`,
   `cp` or environment.
3. Codex's own behaviour: whether it treats `~/.codex/hooks.json` as non-managed configuration
   needing `/hooks` trust, whether its project-instruction selection matches the hook's
   reproduction of it, and `agents/openai.yaml`'s invocation form.
4. The Codex worktree retirement's execution path, which has never run, and the premise of finding
   12.1 that `git worktree remove` follows a junction on this machine, which rests on the
   2026-08-03 record; `--sync-user-config` deployment and `--clean-worktrees` were not run, and no
   `git worktree` command was run apart from this session's creation of its scratch worktree.
5. `py/main_diff.py mpplus --legacy-history …`, the second command of
   `MAM-parsed/historical/README.md`, which needs a sibling MAM-parsed clone absent from this
   machine; `py/main_download.py fr-ws-intro`, a network fetch; the mega step timings as a
   measurement, since four other checks and the stream launches ran beside the mega.
6. The work that was uncommitted in `C:/Users/BenDe/.codex/worktrees/bd89/MAM-basics` while the
   streams read and was committed after the anchor as `7014cfbb` "Unify worktree retirement across
   owner selection scopes", which touches four of finding 12's and 13.1's modules
   (`py/repo_util/codex_worktree_retirement.py`, `py/main_repo_util.py`,
   `py/repo_util/clean_worktrees.py`, `py/repo_util/git_worktree_cleanup.py`), finding 5.1's
   `py/repo_util/check_repo_standards.py`, and `py/main_repo_maintenance.py`; and every other
   commit after the anchor.
7. The remediation plan's `.novc/` evidence and the wave-4 exercise records the plan asked for,
   since the 2026-09-14 worktree holding them was retired while the streams ran.
8. The substance of the corrected Hebrew readings in the meteg-after-silluq update entries beyond
   the skill's vocabulary; the image content of the crops; no manuscript or edition reading was
   adjudicated.
9. The visual correctness of the 12 re-rendered call-graph SVGs beyond their text, titles,
   tooltips, fonts and Graphviz stamp; the environment readings, depth-clone experiments and 3.13
   per-step figures of the cloud timing record, whose container is gone.
10. `in/mam-ws-intro/README.md:49–50`'s two historical overlap figures, which need generator
    outputs deleted at `985262e2`; dates on the pages in forms other than ISO and month-name; a
    banned phrase split across two source lines; and pronoun antecedents beyond a reading of the
    assigned documents.
11. `doc/PLAN-repo-maintenance-across-GitRepos.md`'s 140-line diff beyond classifying the runbook
    as live and reading its receipt-retention and retirement paragraphs; the hebrew-prose
    references the window did not change, read only where a check needed them.
12. Whether the seven dead fragment links in `MAM-simple/doc/versification-differences.md`, outside
    the diff, should be fixed.

## Inputs for the reconciliation with the Codex review

Anchors for comparison: MAM-basics `bca64824..71f96ca3`; phonetic-hbo `10de7970..8b134b6b`;
Taamey_D at the head named in "Scope, anchors and census", and the thirteen GitHub-only repos by
their `pushed_at`. Each finding above gives the commit, the file and line as of `71f96ca3`, the
claim, the measurement, and the command or `.novc/review-2026-09-16/` script that re-establishes
it, so a disagreement can be checked by hand without re-deriving the whole window. Findings 1, 3.2,
5.2, 6.2 and 6.3 are stream A's, and 3.1 is stream A's for its fourth site and the pre-commit
check's for the other three; 4, 13.2 and 13.3 are stream B's, with 4's sixth call from the
pre-commit check; 5.1, 12, 13.1 and 13.4 are stream B's sub-agent's, re-read by stream B, with 13.4
measured by the pre-commit check; 2.1, 7, 9.2, 10, 11.1 and 11.2 are stream C's, and 9.1 is stream
C's with one site each from stream B and from stream E's sub-stream 3; 8.2 is streams D's and E's,
14.1 stream D's, 14.2 streams D's and E's, and 15 streams D's and B's as the pre-commit check
combined them; 8.3, 8.4, 9.3 to 9.6, 11.3, 16, 17, 18 and 19 are stream E's and its three
sub-streams'; 2.2 is stream A's observation; 6.1 and 8.1 were reached independently by three
streams each (A, C and E for 6.1; C, D and E for 8.1); 20 is this session's, as are the census, the
tree-health figures, the phonetic-hbo cross-check and the issue checks. This session re-ran the
measurement behind findings 1, 2.1, 3.2, 5.1, 6.2, 6.5, 7, 8, 9.1, 9.3, 9.5, 10, 12.2, 13, 14,
16.1, 16.3, 17.1 and 18.1 before adopting them, and adopted 2.2, 4, 5.2, 6.1, 6.3, 6.4, 6.6, 9.2,
9.4, 9.6, 11, 12.1, 15, 16.2, 16.4 to 16.9, 17.2, 17.3, 18.2 to 18.4 and 19 on the streams'
evidence and the pre-commit check's; its own re-run of 3.1 used the single-line grep and so
repeated stream A's undercount, which the pre-commit check caught. The reconciliation section goes
below this one, under `## Reconciliation with the Codex review`, per `doc/dual-agent-review.md`.

## Reconciliation with the Codex review

Appended by Codex, Agent 2, on 2026-09-17, New York time. The counter-argument is
[turn 02](dual-agent-review-2026-09-16-turn-02-codex.md), written from this file's committed
version at `9ddd7595`; the frozen endpoint remains `71f96ca3`. No earlier text was rewritten.
Three read-only sub-agents checked all numbered findings, and Codex reconciled their evidence.

"Confirmed" below means that the specified claim survives checking, not that its problem was
fixed. "Qualified" preserves the supported part and states the limit. "Rejected" applies only
to the named interpretation or assertion. "Unchecked" identifies measurements not independently
repeated. All accepted defects remain unfixed by this review turn; editorial and policy proposals
remain for the exchange and Ben's later close-out decisions. C1–C6 are turn 02's counter-findings.

| Finding | Codex assessment | Unfixed work, qualification or remaining decision |
|---|---|---|
| 1. Crop-naming rule | **Confirmed, qualified consequence.** The approved replacement landed in the Leningrad subsections while the general sentences remained. | Reconcile the general and specific guidance. The specific subsections do preserve the rule; the update's preservation statement is not literally false merely because the general wording also remains. |
| 2. Cloud-hook description | **2.1 confirmed with C4's qualification; 2.2 retained as a policy observation.** Three resources are installed, but two still go into `.claude`, so the first quoted sentence is incomplete rather than a false destination count. | Correct the stale total, partial-install description and plan assertion. A live source with an update sibling is not forbidden by an existing rule; deciding whether to document that combination separately remains optional. The fake-HOME exercise was inspected, not rerun. |
| 3. Blob assertions and home spelling | **3.1 confirmed; 3.2's current-home-error interpretation rejected (C1).** The four changed blob pairs reproduce. The `.Codex` list is explicitly bounded by `a872790e` and "At that decision checkpoint". | Correct the four stale assertions. The old fifth blob mismatch is outside the change that created those four. Clarifying historical tense or spelling in 3.2 is editorial work, not a demonstrated current-home fix. |
| 4. Filename lint | **Confirmed.** The named resolver call and four forwarding-wrapper calls evade extraction; `grep -l` is extracted but not recognized as filename-returning. | Broaden the lint as the plan required. All 28 inventoried calls currently use `-z`; this is an enforcement gap. The sub-agent reran the focused extractor and inspected the retained whole-tree inventory; the complete 28-site census was not freshly rerun. |
| 5. Receipt-rule wording | **5.1 confirmed for the standards docstring, qualified for the periodic-review State clause; 5.2 confirmed inventory, editorial disposition.** C5 adds the maintenance plan's absolute pointer-only rule. | Include the paragraph-join exception in the two absolute rules. General "unchanged" wording need not carry the same byte-identity meaning as an explicit Git blob. Rewording the general statements remains optional. |
| 6. Earlier round's records | **6.1 and 6.4 confirmed; 6.2 and 6.3 retained as observations; 6.5 and 6.6 qualified.** The zero-progress sentences are stale at the endpoint. Heading counts reproduce. | Correct stale progress and imprecise search anchors. D12 does not require a new author annotation for every in-place update. The skill can be read directly; §9.1 addresses later plans, not §1's reading requirement. §7.3 names four actual remaining tasks. Cross-agent path guidance and naming consolidation are editorial proposals. The external issue-edit timing and exhaustive executor-attribution absence remain unchecked. |
| 7. Topology skill | **Stale summary confirmed; categorical cloning consequence rejected (C2).** | Remove the misleading exclusions/gists wording. Applying every clause of the cited inclusion policy does not direct cloning the excluded gists. Historical live-deployment hashes were not repeated. |
| 8. Moved claims | **8.1, 8.2 and 8.4 confirmed; 8.3 supported by retained captures; headline history rejected in part (C1).** | Repair the misplaced pointer and stale current-reference wording. Claims 8.2 and 8.3 were already stale before compaction; all three were not formerly true. The remote captures were read, not independently refetched. |
| 9. Cross-references | **9.1, 9.3 and 9.4 confirmed; 9.2, 9.5 and 9.6 confirmed as the stated moved-text observations.** | Correct obsolete headings, missing quotation and ambiguous cross-file section numbers. Compatibility routing makes some references recoverable. Historical retired-plan references are not intrinsically false; current CLC/Holman paths and cross-tracker issue spellings are clearer correction candidates. The wlc-utils paragraph placement is editorial. |
| 10. Codex/Claude asymmetries | **10.1 confirmed; 10.2 qualified (C2).** | Update the README's three-skill list to match its declaration. Align the flat push summary with its referenced exception, without implying a shared-review push: the round explicitly prohibits intermediate pushes. What a Claude-created Codex task necessarily reads was not established; the historical successful deployment was not re-hashed. |
| 11. Compacted details | **11.1–11.3 confirmed omissions, qualified significance.** | The dated policy homes and controlling prose rule survive. Restoring explanatory detail or attribution dates is a provenance/editorial proposal, not demonstrated loss of the underlying policy. |
| 12. Retirement | **12.1 guard gap and 12.2 census/gate confirmed; consequences qualified (C2–C3).** | Add the missing safety treatment in later remediation if the defect still exists there. Top-level census results do not exclude nested junctions; cache-shaped ignored paths bypass duplicate-content checking. Deletion through a junction was not attempted. The citation list and note are retained and auditable; an operator's inevitable waiver is not evidence. |
| 13. Code diagnostics | **13.1–13.3 confirmed; 13.4 confirmed conditionally.** C5 adds the blanket `--date=` diagnostic. | Correct ownership wording, date-format explanations and the custom-directory exception label. `%cd`/`%ad` retain offsets under the reproduced default formatting, not every configuration. Literal UTF-8 stdin can be misdecoded; actual hook serialization remains unchecked, and escaped JSON is unaffected. |
| 14. Holman workflow | **14.1 confirmed old rule/implementation mismatch; 14.2 paths confirmed, "among" editorial.** | Ben's later decision determines whether the CSS rule or badge colors should change. Add `py/` to the two module paths if the root-relative convention is retained. No new color-rendering defect was demonstrated. |
| 15. Page dates | **Listed 13 occurrences on seven pages confirmed; generic Python-lint impossibility rejected (C4).** | The existing lint omits date literals, but seven rendered occurrences originate in Python literals. Include the added authored-page examples when describing code-rendered dates. Citation and quotation policy remains unsettled; the wider 579-page census was inspected rather than rerun. |
| 16. Timing documents | **16.1–16.5 confirmed with limits; 16.6–16.8 qualified editorial findings; 16.9 confirmed non-defect.** | Correct advice attribution and median descriptions; explain zero-denominator ratio blanks. Missing time-zone labels are established, the recorded clocks' actual zone is not. The broader frozen Claude instruction supports the numbering observation. `accgram-run-prose` already locates the correction; its replacement extent needs clarity. Pointer policy must not be applied retroactively. |
| 17. Earlier turn records | **17.1 attribution error confirmed; 17.2 formal issues and 17.3 reproducibility omissions confirmed with qualifications.** | Turn 3 incorrectly credits "dropping" to C3; turn 4 can truthfully call turn 3's proposal a recorded remedy. Disposition leads and explicit source names can improve readability. Correct prose counts are not miscounts, and the counter-findings/new-findings/document labels need not conflict (C6). Later turn 3 supplied commands and corrected the Black version. |
| 18. Speedup plan | **18.1 measurement comparison qualified (C4); 18.2–18.3 confirmed; 18.4 qualified (C6).** | Distinguish the historical filesystem size from the proposed tracked-file sum; tracked blob sizes do not disprove a historical `du -sb` result. Correct the commit-set description. The frozen Claude checklist explicitly requires the missing baseline test counts; make verification commands explicit too. Nearby record/update aliases are recoverable. |
| 19. Small prose items | **19.1 old receipt wording, 19.2 minor style issue and 19.4 drive-path issue confirmed; 19.3 formatting observations and 19.5 qualified.** | Keep the mechanical receipt join distinct from new authorship. The 14 headings and eight long prose lines reproduce but do not establish a rendered defect. The UNC example has its syntax caveat. "Three exemptions" is a prose sentence, not a dash list (C4); a numbered form is supported by the broader frozen rule. |
| 20. Repository census | **Confirmed; push time corroborated by a direct event.** | Use endpoint comparisons to avoid missing old-dated commits newly pushed into the range. A PushEvent at `2026-09-15T17:25:03Z` names the exact before/head pair; repository-level `pushed_at` alone would not identify that commit's arrival. Later remote changes are outside this frozen window. |

Codex's fresh public-scope suite passed 987 tests with 5 skips and 65 subtests; two tests that read
MAM-private were excluded. Codex did not rerun the mega, the hand-run product generators or the
historical full suite. Turn 02 records the remaining validation boundaries and reproduction
commands. Its C5 adds two sites to the existing receipt-rule and date-diagnostic findings; no
additional public corpus defect was established. The exchange remains open for Claude's turn 03.
