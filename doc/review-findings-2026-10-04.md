# Findings of the 2026-10-04 review of MAM-basics since 2026-10-02

State: not yet acted on
Updates and later status: [review-findings-2026-10-04-update.md](review-findings-2026-10-04-update.md).

Written on 2026-10-04, from 15:00 New York time, by a Claude session (Claude Opus 5.5 at `max` in
the Claude desktop app; the app's session record gives `max`, the level the session was started at)
as a single-agent periodic review under `doc/periodic-review.md`. Ben's instruction, verbatim: "Do a
single agent review of MAM-basics." The session worked in the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, on `main` at the end commit `139e2d63`, which was also
`origin/main` after the session's fetch, and the file was written against that commit. Nothing was
fixed. Every time of the review's work is New York time from a named reading of this machine's clock
(PowerShell's
`[System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow, 'Eastern Standard Time')`);
Git and GitHub timestamps keep their offsets. The file follows `doc/periodic-review.md`, "What a
review file contains", and adds one short section of things noticed outside the diff, as the
2026-10-02 review did; minor wording items are one line each, in finding 9.

**Which records inside the window are subject and which are evidence.** The window holds the
2026-10-02 review's records, and `doc/periodic-review.md`, "A prior round's own records inside a
successor window", asks this opening to say which of them it reads as a subject. Evidence, not
subject:

- `doc/review-findings-2026-10-02.md` and `doc/codex-review-findings-2026-10-02.md`, the two
  reports, because the owner's disposition list checked every Claude item, and every Codex statement
  that bears on one, against public evidence, and Ben approved it as the close-out package, so
  reading the reports again as a subject would reopen settled dispositions without new evidence;
- that disposition list and Ben's recorded decisions in `doc/review-findings-2026-10-02-update.md`,
  for the same reason;
- `doc/PLAN-remediate-review-findings-2026-10-02.md` and its update file, which this review uses as
  the statement of what the remediation was meant to do, its approved wording included;
- every entry that records an act on a machine (`LAPTOP-DBLE8UKA`, `BENS-HP-MINI`), which tracked or
  public evidence cannot check.

Subject: everything else in the diff, including all the code, data, pages, instructions, skills and
procedure documents that the remediation changed and the relay's removal, since no review has read
them; the update file's claims that a finding was implemented, in its section "Dispositions of the
ledger's rows", since close-out step 3 makes such a claim checkable and no review has checked one;
and the window's new entries in the September 29 and October 1 rounds' update files, except where
they record an act on a machine. Item 2 of one entry, which records an act on a machine, is reported
all the same, in finding 3.1, because what it discloses is a property of its public text, not a
claim about a machine.

**How it was read.** The root reviewer ran the census, the suite, the mega, the lints, the
user-configuration and forest checks, and the Pages and issue queries itself before any stream
started, and later ran the two hand-run generators itself on extracted trees in scratch. Nine
read-only sub-agent streams read the window from 15:24, each writing only under this session's
scratch directory, outside the checkout, apart from the ignored files that their allowed targeted
test runs left in the checkout's `.novc/` and `__pycache__`: A, Yeivin ITM and the
meteg-before-stress survey; B, Phonetic MAM; C, licences, fonts, attribution and the reader-facing
READMEs; D, the parser stage, the consumer notices and the mpplus guide, the stress-helper index,
the bot guide and refresh procedure, and the pipeline graph; E, repository tooling and the
standard-stream sweep; F, the relay's retirement and the two review procedure documents; G,
instructions, skills and maintained documents; H, the Book of Job footnote; and I, whole-diff
mechanical censuses with the Pages and issue evidence. Each stream also checked the remediation rows
of its area against the plan. Their briefs named MAM-private, hbofonts and the `bdenckla/trope`
tracker as private and off limits. Each finding says which of its claims the root reviewer re-read
or re-ran itself, which a checker re-ran, and which rest on a stream's evidence; an item of finding
9 that names only a stream rests on that stream's evidence, which the pre-commit check re-derived,
and finding 8's lead says that a checker re-derived every one of its items. The streams' scratch
files are not evidence: every figure in the census and tree health names its commit and the method
that re-establishes it, every figure in the findings names its commit and either its method or,
through its finding's lead, who measured it, and a figure under "What verifies sound" names the
stream that measured it. Before the commit, checker sub-agents checked every finding, the other
sections and the window for omissions, as "Reviewing the review, with the same agent and with Ben"
requires; the last paragraph of this opening records that check.

**Acts outside the repository, and departures.** Before the suite,
`py/main_repo_util.py --sync-forest $HOME/GitRepos --check` reported one problem, the MAM-private
clone behind `origin`; the write form, run between the 15:00:10 and 15:03:54 readings,
fast-forwarded that clone to `2de55e29` and refused this clone, in which two Claude sessions were
recorded, this one and an idle one, so it exited 1, the refusal that `doc/clone-forests.md:53–54`
prescribes when a second session is recorded (finding 7.5 concerns the same skip). hbofonts was
level at `6eb3ee0e`. The suite reads hbofonts, and the mega MAM-private, through tracked code; this
review recorded only the forest check's result, the two siblings' commits and, after the mega, their
status-entry counts, 0 and 0, and read nothing else in them. The mega's two-file diff (finding 1)
was saved to scratch and the two files were restored with `git restore` between the mega's end,
15:22:37, and the 15:24:27 reading, so that the streams read a clean checkout; this paragraph is the
record of the restore, and finding 1.1 the record of the diff. The start tree and the end tree were
extracted with `git archive` into scratch to collect the start's test ids and to run the hand-run
generators. Read-only `gh` queries of public data were made by the root reviewer and by streams B, C
(of the public `bdenckla/Taamey_D`, as its brief allowed), G and I. Streams A and B each ran one
read-only Git Bash command (a `grep`; an `ls` and a `du`), against their briefs, and the root
reviewer one (a `git show` piped through `head` and `tail`, while applying the re-check's
corrections), against the user-level rule that agent shell commands on Windows run in PowerShell 7;
several streams set the working directory with `Set-Location` before running a scratch script;
stream E ran Git's writing commands only in throwaway repositories under its scratch directory.
Every stream reported `git status --porcelain` empty at its start and end. Against `AGENTS.md`, the
root reviewer loaded the `hebrew-prose` skill only after the re-check, before the commit; it then
checked this file's accentuation prose against the skill, which changed some verbs, units and strand
names.

**The pre-commit check.** Ten read-only checker sub-agents checked the draft before it was
committed, from 16:28:28 at the latest, the earliest checker's starting reading: K1 checked finding
1; K2 findings 2 and 3; K3 items 4.1 to 4.5 and 7.9; K4 findings 5 and 6; K5 items 7.1 to 7.8; K6
finding 8, then 17 items; K7 and K8 items 1 to 33 of finding 9 and the two sections after it; K9
every other section and the file's consistency; and K10 swept the window's diff for substantive
defects that the draft omitted. Each also checked the passages that restate its items, and each
reported `git status --porcelain` showing only the untracked draft. No finding was refuted. The root
reviewer re-read or re-ran each correction before adopting it. Among the changes: the hand-run check
now covers both halves of `py/main_mam4sef.py`, and the lag it measures is 8 and 3 files, not the 82
and 3 of a comparison that line endings distorted; finding 3.4 records the two owner-noted sites as
already left as written by the 2026-10-02 plan rather than reopening them; finding 4.1's count of
`kq` pairs at which the release has only the qere is 1,046 of 1,047, not every pair; finding 8
dropped three items, moved three to finding 9 and merged two; the `unicodedata.normalize` count
became twelve calls on eleven lines; and many citations, labels and introducing commits were
corrected. The omission sweep found no substantive defect that the window introduced and the draft
omitted; it added items 4.6, 4.7, 7.10 and 7.11, one-line items 37 to 42, the additions to items
7.2, 7.4 and 9.35, and the third noticed item. The checkers' `gh` queries were read-only queries of
public `bdenckla/MAM-basics` data. A further checker, K11, then re-checked the text written after
the check, this paragraph included; its corrections, each re-read here before it was applied, added
the governing-document question of finding 3, one-line item 43, and many narrower citations and
wordings, and the root reviewer re-read every passage they changed before the commit.

## Scope, anchors and census

This review follows the 2026-10-02 trial review, whose window was MAM-basics `7549ebf7..db59ef5e`.
It covers MAM-basics from **`db59ef5e`** (2026-10-02T13:36:01-04:00, "Record the simplified process
for the next public and private reviews"), the end commit that review recorded, through
**`139e2d63`** (2026-10-04T14:53:01-04:00, "Correct a misquoted docstring and the Codex trial
report's suite claim"), `origin/main` when this review began. `db59ef5e` is an ancestor of
`139e2d63` (`git merge-base --is-ancestor`).

**76 commits, 72 non-merge and 4 merges** (`c23d8522`, `f0c50473`, `6f53a603` and `93ffe8cf`;
`git rev-list --count`, with and without `--no-merges`). The diff changes **292 paths** with rename
detection, 263 modified, 17 added, 11 deleted and 1 renamed (`py/phonetic_mam/test_page_display.py`
to `example_display.py`, R100), and 293 without it. It has **10,217 insertions and 7,122 deletions**
(`git diff --shortstat`); 2 paths are binary, the two new PNGs. The tracked tree went from 5,966 to
5,972 files (`git ls-tree -r` at both commits). The 11 deletions are the relay's ten files and
`py/phonetic_mam/legacy_projection.py`.

The window's substance is six things:

1. The 2026-10-02 trial review's records, 15 commits: the kickoff and the fleshing-out of the trial
   procedure (`742aaf41`, `699c7b17`), the two reports (`58df29bd`, `09be20b3`), the disposition
   list and Ben's close-out decisions with his three procedure changes (`d8b6e1d7`, `644a6c9c`), the
   remediation plan and his advance authorization (`286d2e8c`, `074af13a`), and the records of the
   remediation and of the acts on two machines (`cbd405b1`, `e9c72f2b`, `aa92b8fb`, `db4fb267`,
   `bd40ace5`, `b61481ff`, `9125db0a`).
2. That review's remediation, 40 commits: 39 on 2026-10-03
   (`git rev-list --count cbd405b1..7bd5ee8c`), from the automated relay's retirement (`4573b007`,
   `75a1127b`) through `7bd5ee8c`, holding the Yeivin classifier, claim and gate changes, Phonetic
   MAM's README, oracle and robustness changes, the licence statements and the tooling changes; then
   `b246e05e`, which Ben asked for after the executor's report, giving every stderr reconfiguration
   its `backslashreplace` handler.
3. The Book of Job 38:12 footnote and its two Aleppo crops, 8 commits (`6004709e`, `14baabe3`,
   `a1bbce52`, `3e446584`, `420f5828`, `f6d8610a`, `f8a96a0e`, and the merge `c23d8522`).
4. Instruction and procedure changes, 5 commits: `AGENTS.md`'s rule for when a push of `main` runs
   the mega and the suite (`61660578`, `57e47fe8`), `iterative-document-editing`'s request-file rule
   (`d168e22e`), and the port of the dual-agent rounds' general lessons into
   `doc/periodic-review.md` (`4b795109`) with the two corrections found while making it
   (`139e2d63`): a quotation in `doc/dual-agent-review.md` and an update entry on the Codex trial
   report's suite claim.
5. The mpplus format guide and the consumer notices, 5 commits (`e4a393f8`, `a8025333`, `a7a5803a`,
   the merge `93ffe8cf`, and `25ff446f`).
6. The MAM-with-doc index's layout (`1e090019`) and two merges of `origin/main` (`f0c50473`,
   `6f53a603`), 3 commits.

Groups 1 and 4 also edit `doc/dual-agent-review.md` and `doc/periodic-review.md`, which this review
reads as subject.

## Tree health at `139e2d63`: the suite fails one test, the mega passes all 57 steps but rewrites two published files, and the lints are clean

- **Suite: 1 failed, 1,047 passed, 5 skipped, 60 subtests passed** in 404.89 s, from 15:04:08 to
  15:10:55, run alone as `./.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider`. The
  failure is
  `py/tests/test_diff_mpplus_unpinned_latest.py::test_registered_outputs_match_real_regeneration`
  (finding 1.1). The collected ids go from 1,061 at `db59ef5e` (collected from the extracted start
  tree, `gh-pages/` included) to 1,053: 20 only at the start (11 in
  `test_dual_agent_review_dispatch.py` and 4 in `test_dual_agent_review_turns.py`, both deleted with
  the relay by `4573b007`; 2 in `test_phonetic_untangler_preparation.py`; 3 in `test_yeivin_itm.py`)
  and 12 only at the end (4 in `test_yeivin_itm.py`, 2 in `test_meteg_before_stress.py`, and 1 each
  in `test_mega_coverage.py`, `test_parser_stage_node_keys.py`,
  `test_phonetic_untangler_preparation.py`, `test_product_scopes.py`, `test_review_turn_files.py`
  and `test_stderr_error_handler.py`). The five skips are `test_edition_transcriptions.py`'s
  semantic channel, as before.
- **Mega: all 57 steps exit 0, in 646.6 s of steps**, from 15:11:45 to 15:22:37, with Graphviz the
  pinned 16.0.0 (20260814.1018) and the claims check at 50 passed, 0 failed, 0 pending. It left
  **one tracked diff, in two files**: its `diff-mpplus` step rewrote
  `gh-pages/MAM-with-doc/change-log/unpinned-latest.json` and `.html` on three lines, each the
  MAM-parsed/plus tree id (finding 1.1), and nothing else; no untracked file; the two files were
  then restored (see the opening). Every other product the mega generates reproduces byte for byte
  at the end commit, the `phonetic-mam-export` step (123.4 s) included, which re-exported the
  release through MAM-private's adapter at `2de55e29` without a byte of difference. Afterwards both
  private siblings were at the commits above with no status entry.
- **Hand-run generators.** `py/main_mam4sef.py`, its Sefaria half (the default) and its AJF half
  (`--just-ajf`), and `py/main_mam_osis.py`, whose inputs `25ff446f` changed, were run on the
  extracted start and end trees in scratch. Their outputs are byte-identical between the two trees
  apart from the provenance line that names the extraction folder, one line in each of five files
  (four `_provenance.md` sidecars of `MAM-for-Sefaria/` and `gh-pages/MAM-OSIS/index.html`), so the
  window changes neither product (finding 1.4). Compared with the committed files through
  `git hash-object --path`, which applies the CSVs' `eol=crlf`, and leaving those provenance lines
  aside, both trees' outputs differ identically from `MAM-for-Sefaria/` in 8 files (the Judges and
  II Kings files of its four directories) and from `MAM-OSIS/` in 3: the lag behind MAM-simple that
  Ben accepted on 2026-09-30 and that both READMEs state.
- **Lints.** `black --check py` (26.5.1): 1,201 files unchanged. `ruff check py` (0.16.5): "All
  checks passed!". `py/main_repo_util.py --check-repo-standards --repos MAM-basics`:
  `SYS_PATH_MUTATIONS=0`, `SYS_PATH_IN_TESTS=0`, `HEX_ESCAPES=76`, `ORPHAN_MARKS=0`, `NFC_H_DOT=25`
  and `NFC_LATIN=72`, the same figures as the previous review's.
  `git diff --check db59ef5e 139e2d63` prints nothing, and `git ls-files --eol` shows no `i/crlf` or
  `i/mixed` entry among 5,972.
- **User-level configuration.** `py/main_repo_util.py --sync-user-config --check`, run against
  `refs/remotes/origin/main` at `139e2d63`: `USER_CONFIG_PROBLEM_COUNT=0`.
- **Mark order** (stream I). Of the 142 clusters in the diff's added lines that carry a combining
  mark, by `py/mb_cmn/uni_denorm.py`'s cluster pattern, none fails `has_std_mark_order`.
- **Links and HTML** (stream I). Every relative link in the 42 changed Markdown files resolves at
  `139e2d63` (`git cat-file -e`) except 16 in quoted wording inside the evidence-only plan, every
  pinned link the window added resolves locally, and all 256 relative `href`, `src` and `srcset`
  values in the 8 changed pages resolve, paths and fragments both.
  `py/check_html_syntax_and_sanity.py`, without `--w3c`, reports nothing for three of the five
  changed sub-sites (`book-of-job`, `phonetic-mam` and `yeivin-itm`) or for `--deploy-root`, and
  identical older issues at both commits for the other two, `gh-pages/MAM-with-doc` and
  `gh-pages/MAM-parsed`.
- **Pages.** Two `pages.yml` runs had a window commit as head, both scheduled and successful:
  `286d2e8c` at 2026-10-03T08:31:53Z and `bd40ace5` at 2026-10-04T10:17:43Z. The live site is
  `bd40ace5`'s, whose `gh-pages/` tree differs from `139e2d63`'s only in
  `gh-pages/MAM-with-doc/index.html`, by `1e090019`'s seven-line style block.
- **Issues** (read-only `gh`). Since the start commit, issue #296 was opened (2026-10-03T06:17:53Z)
  and one dated, agent-written comment was posted on #250 (2026-10-02T18:18:51Z); no issue changed
  state, and no pull request moved.

## What verifies sound, stream by stream

**The census, the suite, the mega and the hand-run generators (root reviewer).** The census figures;
the suite's 20 removed and 12 added ids, accounted for by file; every mega product but the two of
finding 1.1 reproducing byte for byte, the export through the private adapter included; the two
hand-run products unchanged by the window's one input change; the lints and the user-level
configuration as stated above.

**Yeivin ITM and the meteg-before-stress survey (stream A).** All 11 remediation rows hold (C1.1,
C2, C6.1, C6.2, C9.2's three content fixes, C12.2, C15.14, C15.15, C15.16, C15.17, C15.31). Rebuilt
in memory, the survey reproduces all 6,119 records, and the classifier's accent class agrees with
accgram's scanners on every record but the 18 the new test declares, each a scanner artifact
(`DEXI_DEXI`) where the survey's disjunctive deḥi is right; reverting C2 in memory makes the new
test fail on exactly the 13 oleh-weyored records. An independent recount agrees on all 20 fractions,
the claim file's values and every printed figure and rounding; 13 of the 17 pages are byte-identical
to the start commit and the other 4 changed only on C2's and C6.1's lines. Gate B passes a real
release change made on a scratch copy and fails a change to the population or to a fraction; the
README's editing procedure works on a scratch copy; `in/yeivin_itm_published_anchors.json` lists
exactly the 345 ids of the start commit's pages; no reference to 2 Kings 52 remains outside the
three review records, and no trope URL remains.

**Phonetic MAM (stream B).** All 16 remediation rows hold as the plan worded them (C1.2, C1.3, C5.1,
C5.2, C10.2, C12.3, C13.1, C13.2, C14, C15.6, C15.7, C15.18 to C15.22); findings 4.1 to 4.5 are
where the aims of C5.1 (4.1), C1.2 and C1.3 (4.2 to 4.4) and C15.19 (4.5 and 7.10) stay incomplete.
Oracle A's input fingerprints recompute 929 of 929 at `c17de175` and at `139e2d63`, and it catches a
one-point page change in either pronunciation. Interleaved undecodable and malformed compute lines,
each between good lines, get one reply each at `139e2d63`, where the start commit gave exit 1 and no
reply; items 7.9 and 7.11 are request lines that still do not. A fake adapter, with nothing reaching
MAM-private, produces each of the exporter's five planned messages with the right exit status and
stderr tail when the adapter writes UTF-8 (stream B showed four; a checker showed the fifth, "source
adapter failed", with the book projector stubbed in memory; finding 7.10 is the non-UTF-8 case). All
991 files that `render` writes reproduce byte for byte, and, judged from the stylesheet, the script
and the rendered pages, with no browser run, the display switches, with JavaScript and without
`:has()`, on every page that shows transcriptions. The README's items 1 to 6 re-derive from the
data, the 7,710 and 356 counts included, and `sys.dont_write_bytecode` is set only inside two
`main()` functions.

**Licences, fonts and attribution (stream C).** All 16 remediation rows hold (C4.1 to C4.8, C10.4,
C15.8 to C15.13, C15.30). The 14 tracked `Taamey_D.woff2` copies are one blob, which the pinned
public upstream commit holds; the seven MAM statement blocks are byte-equal; the two new
`LICENSE.md` files and the prefaces equal the plan's approved texts; both index pages that carry the
attribution are generated through `py/mb_misc/mam_attribution.py` and regenerate byte for byte; all
24 injected faults in the Taamey D support files raise.

**Parser stage, notices, bot guide and pipeline graph (stream D).** All six remediation rows hold
(C7, C8, C10.1, C11, C12.1, C12.4). Every parser-stage encoding injected into a verse cell or a
template parameter raises (24 of 24); the stress-helper index raises on every bad shape injected and
leaves `out/accgram/post-stress-meteg.json` unchanged, which also regenerates byte for byte with no
sibling repositories and the cloud flag set; `pipeline.dot`, `pipeline.svg` and `mpplus.html`
reproduce from their generators; the notices in the 24 plus files and the 70 MAM-simple files equal
the generator's; the C7 and C8 texts are the plan's. No tracked output other than finding 1.1's two
files depends on the plus tree id, and Phonetic MAM's legacy fingerprints skip the plus header.

**Repository tooling and the stderr sweep (stream E).** All rows hold (C9.1, C9.3, C9.4, C9.5,
C15.3, C15.4, C15.5, C15.26 to C15.28, and the stderr fix). Both `.novc` removals clear read-only
Git objects and read-only directories on Windows scratch trees (one-line item 36 is the POSIX case);
the abbreviated-option lint catches every abbreviation Git 2.53.0 accepts and has no false positive
in the tree; all 30 real launches that the forest launch lint covers are bounded; all 49
`sys.stderr.reconfigure` calls keep `backslashreplace`, and the only other setting of a standard
stream's encoding in tracked Python is the `PYTHONIOENCODING` that
`py/repo_util/forest_environments.py:38` gives child processes, which leaves stderr's
`backslashreplace` in place.

**The relay's retirement and the procedure documents (stream F).** R1 to R7 hold as the plan worded
them (items 28 to 30 and 32 of finding 9 are inaccuracies in that wording, and item 31 one in the
new lint's docstring): `4573b007` deleted exactly the ten files R1 names, and no code path, option,
test, skill, instruction, configuration or deployment list at `139e2d63` refers to a removed file or
command; `--sync-user-config` neither deploys nor checks the retired agent file. The turn-file lint
checks what R5 says, shown by an in-memory fault replay. Ben's three procedure changes of 2026-10-03
are in place word for word, the two documents agree on the pre-commit check, and every quotation in
the window's text of the two documents that a tracked source can check matches it.

**Instructions and skills (stream G).** All seven rows hold (C10.3, C15.2, C15.15's skill half,
C15.23, C15.24, C15.25, C15.29): the landed text is the approved text, and its facts check against
the tree apart from one-line items 23 to 25, while question 8.9 bears on the reference that C15.15's
sentence now points to. Apart from finding 5, every text that states when a push runs the mega and
the suite agrees with `AGENTS.md`, mostly by deferring to it; the request-file rule of `d168e22e` is
consistent with the rest of `iterative-document-editing`.

**The Book of Job footnote (stream H).** The page's step, `book-of-job-site`, reproduces all 183
text outputs byte for byte; the five JSON changes follow from the 38:12 record alone; both crops,
viewed enlarged, show what the text and the alt text say, and the page attributes each reading to
μA, whose image it shows; the Hebrew forms and verses match MAM-parsed and UXLC; pages 186r and 58r
match the tracked Aleppo index; mark order is MAM-normal.

**Mechanical rules (stream I).** No Hebrew letter in a tracked filename; NUL-delimited Git filename
output, orphan marks, forward slashes, `sys.path`, encodings named in text-mode calls, Latin NFC and
the parsing of every changed JSON, XML and HTML file are all clean in the changed files; the 96
files that `25ff446f` changed under `MAM-parsed/` and `MAM-simple/` (94 notices and the 2 MAM-simple
reading guides) differ from the start commit by exactly one line each.

## Findings

Findings 1, 2 and 4 reach published pages, distributed products or reader-facing documents; 3
concerns what public files disclose of private repositories; 5 to 7 are instructions, procedures and
tooling; 8 collects questions for Ben; 9 collects one-line items. Each lead says the finding's
disposition at `139e2d63`; nothing here was fixed. Under `doc/periodic-review.md`, "Present
remediation by public-facing risk": the public-facing documents are in findings 1 (a published
change-log page and two product READMEs, and, under question 1.3, the two MAM-simple reading
guides), 2 (`DATA-LICENSES.md`) and 4 (`Phonetic-MAM/README.md` and its schema's description, and,
under item 6, two chapter pages), in questions 8.1 and 8.3 to 8.6, and in one-line items 2 to 4, 8
to 10, 12, 15, 22, 34, 41 and 43; the public-facing data are in findings 1 (the change log's JSON
and, under question 1.3, the notices of 70 MAM-simple files) and 4.6 (the release's rows for two
verses); everything else is lower risk. No finding concerns MAM's text.

### 1. `25ff446f` changed every plus file's notice without regenerating the change log, so the suite fails on `main` and every mega run rewrites two published files

Unfixed at `139e2d63`; introduced by `25ff446f` (2026-10-03T18:14:30-04:00, "Name the narrow-sense
paseq template in consumer guidance"). Pressing under `doc/periodic-review.md:393–394` ("Something
pressing, such as a mega that fails on `main`, is raised with him at once"), so it was raised with
Ben in chat while the mega ran, between the suite's end at 15:10:55 and the mega's at 15:22:37.
Items 1, 2 and 4 were re-run by the root reviewer; item 3's counts are stream D's, confirmed by a
checker.

1. **The change log names a superseded MAM-parsed/plus tree.** `25ff446f` replaced one line of the
   consumer notice, its narpas rule, in all 24 plus files, which moved the `MAM-parsed/plus` tree id
   from `c36194469e83b5e8100bc9733bbf21ff8c773985` to `f5b2c69f61d2ef48af855ae39c3db560977ad73a`
   (`git rev-parse <commit>:MAM-parsed/plus` at `25ff446f^` and `25ff446f`). The unpinned-latest
   report records that id as its end (`py/subcommands/diff_mpplus.py`, `generate_report`'s
   docstring: "since then records the git tree id of MAM-parsed/plus"), and the commit regenerated
   neither `gh-pages/MAM-with-doc/change-log/unpinned-latest.json` nor `.html`, which still say
   `c3619446…` (`"new_tree"` at line 4 of the JSON; the range table and the `git log` hint of the
   HTML). So, at `139e2d63`:
   - `test_registered_outputs_match_real_regeneration` fails with "Differing artifact:
     unpinned-latest.html" and "… .json", the suite's one failure;
   - the mega's `diff-mpplus` step rewrites both files on three lines, each the tree id, so every
     mega run until a fix leaves this diff, which `AGENTS.md` calls a failure when unexplained;
   - the live site, deployed from `bd40ace5`, whose two files are the same blobs (`bbf30734`,
     `20490eaa`), tells readers that the unpinned changes end at tree `c3619446…`, which is no
     longer the distributed `MAM-parsed/plus`. The four Scripture changes it lists are still right:
     the regenerated files differ from the tracked ones only on those three lines, so every other
     key of the JSON, `"diff_count": 4` included, is unchanged.

   The same failure happened two days earlier: `94535122` (2026-10-01) regenerated these two files
   after `f62428c4` changed the plus files' headers, and its message records the cause. Remedy, as
   there: `py/main_diff.py mpplus --all`, which rewrote only these two files then. `25ff446f`'s
   message records that it skipped the mega and the suite, as `AGENTS.md`'s rule of 52 minutes
   earlier (`57e47fe8`) asks when they are skipped; finding 5.5 is the question that follows.
2. **Two product READMEs keep the old label.** `MAM-parsed/README.md:37` and
   `MAM-simple/README.md:44` still say "(narrow-sense paseq," with the U+05C0 glyph, the ambiguous
   glyph that `25ff446f` set out to replace, where the notice
   (`py/mb_cmn/public_data_consumer_notice.py:31`), the 24 plus files, the 70 MAM-simple JSON and
   XML files, both MAM-simple reading guides and `gh-pages/MAM-parsed/plus/html/mpplus.html` now
   name the template `מ:פסק`. The README text dates from `47a86b4d` (2026-09-16); `25ff446f` changed
   98 files and neither README. The census, over every tracked text file for "narrow-sense paseq"
   followed by a comma or an opening parenthesis and the glyph, finds these two maintained sites and
   five lines in four dated records, which stay as written: four with the comma form
   (`doc/PLAN-remediate-review-findings-2026-09-26.md:131`,
   `doc/PLAN-remediate-review-findings-2026-09-29.md:213` and `:561`,
   `doc/dual-agent-review-2026-09-29-turn-01-claude.md:417`) and one dated entry of an open update
   file, `doc/public-data-consumer-hazards-2026-09-16-update.md:19` (stream D's census, widened by a
   checker; re-read here).
3. **Question: MAM-simple's guidance now names a template that MAM-simple does not contain.** The
   shared rule names `מ:פסק` in every MAM-simple notice and in both MAM-simple reading guides
   (`MAM-simple/doc/reading-mam-simple.md:86`, `reading-mam-simple-xml.md:225`). MAM-simple's
   narrow-sense paseq is `lp-paseq`, and the string `מ:פסק` occurs in `MAM-simple/` only in those 70
   notices and 2 guides (stream D). For MAM-parsed the label is accurate: plus has the template on
   521 lines. Whether MAM-simple's text should name `lp-paseq` instead is Ben's call.
4. **The hand-run generators were not rerun.** `25ff446f` changed MAM-simple's JSON and XML, the
   inputs of `py/main_mam4sef.py` (the JSON) and `py/main_mam_osis.py` (the BHS XML), and its
   message records no rerun of them, which `AGENTS.md`'s hand-run rule (`:166–172`) requires for a
   change that is not a text refresh. This review ran both, `py/main_mam4sef.py` in both its halves
   (tree health): neither product changes, since the OSIS reader drops XML comments and the Sefaria
   reader ignores `consumer_notice`, so the lapse is one of procedure only, with no product effect.

### 2. `DATA-LICENSES.md` dedicates to CC0 a capture of MAM's Hebrew Wikisource Decalogue page, and credits MAM's Hebrew in accent-grammar outputs to the WLC and UXLC

Unfixed at `139e2d63`; older, introduced by `20bb89ed` (2026-08-12, "Map the wlc corpus's licences,
and scope CC0 short of the scan crops";
`git log --full-history -S "in/accgram/printed_decalogue_teamim.json" -- DATA-LICENSES.md`); the
window's `007f9f31` rewrote other rows of the same table (`DATA-LICENSES.md:52–53`, `:57`, `:60–63`,
`:93`, `:118–119`) and left these. A reader-facing licence statement. Stream C's evidence, widened
by a checker; the rows, the file's provenance block and the history re-read here.

1. Row 79 puts `in/accgram/printed_decalogue_teamim.json` under "CC0 1.0 — the dedication at the end
   of this file", as "the table that indexes" Ben Denckla's hand transcriptions. The file is a
   vendored capture of MAM's Hebrew Wikisource page עשרת הדברות בסיס/טעמים: its provenance block
   (`:2–8`) gives that page, its URL, page id 344500 and revision 3025606, and it has eight
   Decalogue versions of MAM's Hebrew and no index of transcriptions. Row 65 maps the same page, as
   one of the 36 declared special pages (`py/ws/ws_special_page_download.py:28`; the special-page
   manifest records the same page id and revision), to CC-BY-SA 4.0, and `DATA-LICENSES.md:198–200`
   says the CC0 dedication "reaches none of the vendored material". The file arrived with `f99996f3`
   (2026-08-12).
2. Rows 84 (`out/accgram/`) and 91 (`gh-pages/wlc/`) say that the biblical Hebrew their files quote
   or display "comes from the WLC and the UXLC and keeps their terms above"; row 84 says so though
   its description names "the printed-Decalogue outputs". That is not so for the files that quote
   the capture: `out/accgram/printed-decalogue/_printed_decalogue.json` and
   `gh-pages/wlc/accgram/printed-decalogue.html`, which tabulate its strands, and
   `printed-decalogue-simanim.html`, `printed-decalogue-uvinkha.html` and
   `maqaf-nonfinal-accents.html`, which quote forms lifted from it. Nor is it so for files that
   quote MAM-simple or MAM-with-doc: `out/accgram/maqaf-nonfinal-accents.json`, whose `mam_simple`
   corpus is MAM-simple's Hebrew, the same page, `telg-doc-notes.html` and
   `ps17v14-mam-doc-notes.html`. `printed-decalogue-koren.html`'s only pointed Hebrew is two WLC
   forms. This list comes from the generators' docstrings and a checker's comparison of each
   output's pointed Hebrew with the capture; it is not a census of the two rows' files.

### 3. Public files carry material from private repositories

Unfixed at `139e2d63`: item 1 was introduced in the window, items 2 and 3 are older, item 4 is the
census, 106 of whose 112 hits predate the window, two of whose sites were already left as written,
and whose other hits wait on item 5, and item 5 is a question. The rule is Ben's decision of
2026-08-27, recorded in the `repo_visibility` comment of `in/repo_maintenance_policy.json`: a
private repository's name may appear in a public file, but "what must not cross is their CONTENT,
meaning paths inside them, file names of theirs, and findings about them". For MAM-private's trees,
the same file's `MAM-private` entry (`:15`) names a document inside MAM-private as "the governing
statement of what about these trees may reach a public repo" and says to read it "before writing
public prose about any of them"; this public-only review cannot read it, so items 2, 4 and 5 are
judged against the 2026-08-27 rule alone, and the conflict between that instruction and
`doc/periodic-review.md:198–200` is a question for Ben. `doc/periodic-review.md:207–208`, added by
`4b795109` on 2026-10-04, has a review record a check whose tracked code reads a private sibling by
"only such a check's result and the sibling's commit, never a path or any content from the sibling",
and this file is a public file under the 2026-08-27 rule, so this finding names no private path
itself.

1. **Introduced by `b246e05e`.** Item 2 of the entry "Two observations of the executor's report
   addressed, 2026-10-03" in `doc/review-findings-2026-10-02-update.md` (`:815–819`) names a file
   inside hbofonts, quotes an hbofonts commit's subject, and says which other hbofonts file that
   commit edits. Its sentence "Nothing in MAM-basics names the deleted file" holds only of the rest
   of the tree: `git grep` at `139e2d63` finds the file name in that entry alone, and at `b246e05e^`
   nowhere (stream I; re-run here). The content disclosed is not sensitive, but the rule is
   categorical, and the text is on `origin/main`; whether to edit a live update entry, which history
   keeps anyway, is Ben's call.
2. **Older.** Two links point into MAM-private: `doc/dual-agent-review.md:357` links a file inside
   it (the path since `2a74dd44`, 2026-09-20; the link since `e4934b6e`, 2026-09-29), and
   `doc/PLAN-silluq-before-gaya-template.md:509`, in a live plan, links one of its issues
   (`772545d5`, 2026-09-08). C15.31's remediation treated a private-issue URL as such a path, but
   its scope was the 13 trope comment lines (stream C; both lines and their histories re-read here).
3. **Older.** `py/ws/ws_bot_edit_history.md:237–239`, with `:242–243`, gives a clone command for the
   private `bdenckla/trope` and file paths inside it: the paths since `555230d6` (2026-03-12, under
   the file's earlier name, which `198a6e33` renamed), the clone command and the restated paths
   since `cb5bcda1` (2026-10-01), after the rule. trope is outside `repo_visibility`'s map, which
   classifies only workspace folders (`in/repo_maintenance_policy.json:5`; finding 6.3), but the
   2026-10-02 plan applied the rule to trope's issue URLs under C15.31, which Ben accepted, and the
   2026-10-02 review's update file records `gh repo view` printing `PRIVATE`
   (`doc/review-findings-2026-10-02-update.md:554–555`) (stream A; history re-read here).
4. **The census, with two sites already disposed of.**
   `git grep -I -E "(MAM-private|hbofonts)/[A-Za-z0-9_.-]"` over the tree at `139e2d63` finds 112
   line hits in 52 files, against 108 in 51 at `db59ef5e` (re-run here): 28 lines in 11 files with a
   date in the name, three of them plans, 12 in 11 Python files, 14 in 7 skill files, 21 in 4
   undated plans and 37 in 19 other files, the three `in/` policy and manifest files among them, six
   of the 112 being only URLs of the hbofonts Pages site (a classification by file kind, re-run
   here, in that order of precedence). The pattern misses possessive spellings followed by a path
   (16 lines with "MAM-private's" and 2 with "hbofonts'", 18 lines in 9 files), the two historical
   sibling spellings that `dot-claude/skills/hebrew-prose/references/mam-basics.md:30–33` says
   resolve into MAM-private (34 lines in 19 files), and bare file names; this review judged against
   the rule only the sites named in this finding, so it gives no complete list of what crosses. The
   two sites that the 2026-10-02 owner noted beside C4.1, `doc/windows-long-paths.md:131–137` and
   `doc/PLAN-checkout-kinds-and-portable-knowledge.md:261`, were left as written by the 2026-10-02
   plan for its stated reasons (`doc/PLAN-remediate-review-findings-2026-10-02.md:958–963`):
   `doc/PLAN-checkout-kinds-and-portable-knowledge.md` is an executed plan (`:3`), a receipt, and
   `doc/windows-long-paths.md` falls under Ben's deferral of 2026-09-28, which stands. The same
   receipt's lines 259–260 (`doc/PLAN-checkout-kinds-and-portable-knowledge.md:259–260`) name a file
   inside MAM-private that neither the owner nor the plan named, and fall under the same receipt
   rule. This review does not reopen them.
5. **Question.** The shared `hebrew-prose` skill deliberately sends agents to "the current
   MAM-private paths" (`references/mam-basics.md:44–45`); `7bd5ee8c` restated one such path in
   `references/sources-and-corpora.md:71` and listed three historical sibling paths
   (`references/mam-basics.md:40–42`), which that reference says resolve into MAM-private. Ben's
   choices of 2026-08-10 and 2026-08-11 to keep such citations (`:33–37`) predate the rule, and the
   policy file that records the rule itself names MAM-private paths
   (`in/repo_maintenance_policy.json:15`, `:71`). Whether agent routing, code comments and dated
   records are exempt from the rule decides 54 of item 4's 112 hits, its skill, Python and
   dated-name groups; whether plans, maintained documents and the policy files are exempt decides
   the rest; both are Ben's call.

### 4. Phonetic MAM's documents omit two of the release's departures from MAM's text and omit or misstate how chapters leave the legacy comparison, and in two Decalogue verses the release has one strand's narrow-sense paseqs in both strands

Unfixed at `139e2d63`. A distributed product's README, schema description and data, two published
pages, and the refresh procedure. Items 2 to 5 rest on stream B's evidence, re-run by a checker (the
Ruth demonstration, the 20.2 s measurement and a search of the tracked tree for item 4's absence);
item 1's counts and item 6's rows were re-run here; item 6 and question 7 come from the pre-commit
check's omission sweep.

1. **Introduced by `82235e8c`, in the plan's approved wording.** `Phonetic-MAM/README.md:28–29`
   tells a consumer joining the release to MAM that it "must allow for these differences" and lists
   six, and the schema description (`Phonetic-MAM/schema/phonetic-mam-public-v1.schema.json:5`) says
   the README lists how the release differs. The list omits two:
   - the release's 39 book files have no U+05BF rafe, which `MAM-simple/json-vtrad-mam/` has 94
     times, 84 of them in running text at 84 chanted words in 81 verses, Exodus 2:3 among them (the
     release's `examples/display.json` keeps it in three example atoms, at two of those verses);
   - the release has only the qere at 1,046 of MAM-simple's 1,047 `kq` ketiv/qere pairs (the 1,047th
     is 2 Chronicles 25:17, the README's item 6) and none of its 8 unread ketivs (`kq-k-velo-q`),
     while the README's item 1 confines "only the qere" to perpetual qere. MAM-simple's guide has a
     consumer choose one branch at `kq`, so there the release makes an unstated branch choice rather
     than altering the text; the guide's plain-text procedure keeps an unread ketiv
     (`MAM-simple/doc/reading-mam-simple-xml.md:150–156`), so the lack of the 8 is a separate
     departure. Either way, the README promises the differences a join must allow for.

   Stream B's census of the chanted words of MAM-simple's `cant-alef` strand in all 23,202 verses,
   which set aside MAM-simple's narrow-sense paseq, parashah and inverted-nun markers and its unread
   ketivs before comparing, accounts for every other difference in their Hebrew by the README's
   items 1 to 6; a checker's comparison of consonants and atom boundaries finds every verse but 2
   Chronicles 25:17 (README item 6) and Deuteronomy 32:6 (README item 1) in agreement with
   MAM-simple's qere reading. Re-run here: no U+05BF in the 39 book files and 94 in the 24
   MAM-simple book-group files; 1,047 `kq`, 8 `kq-k-velo-q`; and no mention of rafe or of ketiv/qere
   pairs in the README beyond its item 6. **Question:** the release also has none of MAM-simple's 9
   inverted nuns, while it keeps parashah breaks and narrow-sense paseq as layout rows
   (`py/phonetic_mam/display_schema.py:28`); whether that is a third departure the README owes, or
   structure outside "How the Hebrew differs", is Ben's call.
2. **Introduced by `a363e5ce`, in the plan's approved wording.** The refresh procedure requires each
   chapter that `check` lists to be one "whose data a committed refresh changed"
   (`dot-claude/skills/mam-wikisource-refresh/references/dependent-refresh.md:137–138`), and
   `Phonetic-MAM/README.md:19–20` says "a chapter that a refresh changes leaves that comparison". A
   chapter's fingerprint covers the verse before it and the verse after it in the same plus file
   (`py/phonetic_mam/projection_check.py:125–166`), so a change to a chapter's first or last verse
   also makes its neighbour leave: a change to Ruth 2:1 makes Ruth 1 and Ruth 2 leave. The README's
   sentence omits the neighbours, and the procedure's requirement fails on a correct refresh.
3. **Introduced by `a363e5ce`.** `check` now also lists the chapters that have left the comparison,
   which the procedure relies on, but the README's command list (`Phonetic-MAM/README.md:76`) and
   the `check` subcommand's help string (`py/main_phonetic_mam.py:25`) still describe it as
   validation only, though the description that `--help` prints above that string, the module
   docstring (`:8–10`), names the listing.
4. **Question.** When every chapter has left, `verify_site` raises "every chapter left the
   comparison" (`py/phonetic_mam/projection_check.py:213`), and the procedure says only never to
   regenerate either record (`dependent-refresh.md:139–140`). A `git grep` of the tracked tree for
   the ways of saying that chapters have left the comparison finds only the code,
   `Phonetic-MAM/README.md:20` and the evidence-only plan, none saying what to do then. A
   representation change that touches every plus record would reach that state at once.
5. **Question; latent.** The exporter's time limit does not bound the export when a child of the
   adapter holds the adapter's stderr: after the watchdog kills the adapter, `Popen.__exit__` waits
   while closing stderr, and, on Windows, the test-page run's post-timeout `communicate()` has no
   limit, since `subprocess.run` repeats it there only (`py/phonetic_mam/exporter.py:164–209`,
   `:215–233`, against the contract at `:23–24`). With a fake adapter, a child holding stderr for 20
   seconds and a 5-second limit, the errors came at 20.2 s and 20.1 s. Public code cannot show
   whether the private adapter starts such a child.
6. **Older; present in distributed data and two published pages.** At Exodus 20:3 and Deuteronomy
   5:7 MAM-parsed's dual-cantillation template has two narrow-sense paseqs (`מ:פסק`) in
   its טעם עליון strand and none in its טעם תחתון strand
   (`MAM-parsed/plus/A2-Exodus.json:7988–7996`; `MAM-parsed/plus/A5-Deuter.json:2782–2790`). The
   release has each as an unlabelled marker row whose one cell is in the first transcription column,
   where an unlabelled cell is a transcription common to both strands, so the selection for each
   strand lists the two narrow-sense paseqs (rows 2 and 6, counted from 0, of each verse in
   `Phonetic-MAM/data/A2-Exodus.json` and `A5-Deuter.json`;
   `py/phonetic_mam/analysis_reader.py:156–172`, `:202–204`), and the two chapter pages render them
   so (`gh-pages/phonetic-mam/tnkh/A2-Exodus/20.html:176–181`, `:200–205`;
   `gh-pages/phonetic-mam/tnkh/A5-Deuter/05.html:419`, `:443`). The census of all 18
   dual-cantillation verses finds no other layout template in one strand alone. Whether the README's
   list of departures should name it is Ben's call. The misattribution is in the data and the pages,
   and the release's display contract cannot say which strand a marker belongs to: a layout element
   has only its label and projects, unlabelled, into the first transcription column
   (`py/phonetic_mam/display_projection.py:145–148`), and the validator refuses any other marker
   shape (`py/phonetic_mam/display_schema.py:144–157`). The release data came with the merge
   `9a67d51b`.
7. **Question; introduced (restated) by `a363e5ce`.** The legacy projection oracle hashes every row
   and cell of each chapter table (`py/phonetic_mam/projection_check.py:81–107`, `:118–122`), no
   code writes its records (`:11`), and the procedure calls a mismatch "a regression" and says never
   to regenerate either file (`dependent-refresh.md:138–140`). So a deliberate correction of the
   display, such as one that labels item 6's marker rows, fails
   `test_complete_release_and_unified_projection` for every chapter it changes whose input did not
   change (for item 6's rows, Exodus 20 and Deuteronomy 5), and no text gives a path past it; the
   plan's approved design accepted that failure
   (`doc/PLAN-remediate-review-findings-2026-10-02.md:1183`), and `Phonetic-MAM/README.md:3`'s "the
   existing Phonetic MAM display" may mean that the freeze is intended. The hashing came with the
   merge `9a67d51b`; `a363e5ce` added the input gating and the procedure's "Never regenerate".
   Distinct from item 4, the state in which every chapter has left.

### 5. `AGENTS.md`'s new rule for a push of `main` left texts behind

Introduced by `57e47fe8` (2026-10-03, "Decide by judgment whether a push of main runs the mega and
the suite"), which replaced the content-based exemption with "Before pushing `main` to `origin`, run
the mega and the suite", subject to a judged and recorded skip (`AGENTS.md:161–165`). Unfixed at
`139e2d63`. Stream G's census, over every tracked text file outside the generated trees; items 1 and
2 re-read here.

1. **A live plan still prescribes the removed exemption.**
   `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md` (State `live`) tells its
   executor to "Apply the current content-based verification exemption and full-suite cadence;
   Markdown-only work owes no full suite or mega" (`:93–95`) and that "A linked worktree receives
   the repository's mandatory final mega unless its branch is content-exempt" (`:533–535`). Both
   name a rule that `AGENTS.md` no longer has, against `iterative-document-editing`'s rule that
   plans still being executed "stay true in place" (`SKILL.md:88–89`). Minor: the plan is dormant,
   and its "Current execution boundary"
   (`doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md:61–67`) sends the executor to
   the current instructions first.
2. **Question.** D11's final integration (`doc/dual-agent-review.md:396–405`) runs the mega but no
   suite on the merged tree and records no skip before it pushes `main`; the new rule asks for both
   or a recorded skip. D11's final-integration paragraph is unchanged in the window (`4573b007`
   edited only D11's relay passages, `:334–353` and `:366`) and matched the old "Running the suite
   too is optional".
3. **Question.** The skip note goes "in the message of the last commit you push"
   (`AGENTS.md:162–164`); when the decision follows that commit, as when a worktree branch is
   fast-forwarded unchanged, only an extra commit or an amend, which needs Ben's say-so, can carry
   it.
4. `py/product_scopes.py:33–36` says its docstring "does not restate" the rule, and its next
   paragraph restates the hand-run part (`:48–52`); the claim came with `57e47fe8`.
5. **Question.** `25ff446f` followed the rule as written and left the suite failing and every mega
   run rewriting two published files (finding 1). Whether a change to tracked product files, as that
   one was, should be excluded from the judged skip is Ben's call.

### 6. The review procedure documents disagree with themselves and with each other, and omit a private repository

Unfixed at `139e2d63`. Stream F's evidence; every citation and quotation re-read by a checker, and
items 1, 2 and 4 re-read here. `4b795109`'s message says that Ben approved its edits as drafted, so
the wording of items 2, 4 and 5 is approved wording, and changing it is an editorial proposal under
D7.

1. **Question; consequential for the next two-agent window.** Both documents still give Ben's
   2026-10-02 trial as the procedure for "the next review in each of MAM-basics and MAM-private"
   (`doc/periodic-review.md:11–17`; `doc/dual-agent-review.md:9–10`, `:29–31`), though the
   MAM-basics trial ran on 2026-10-02 and `doc/dual-agent-review.md` records it as finished
   (`:124–167`). The trial's precedence holds "For this trial" (`doc/dual-agent-review.md:50`; "for
   that trial", `doc/periodic-review.md:14`), which points a later two-agent window of MAM-basics
   back to D9's alternating round (`doc/dual-agent-review.md:230–233`), but Ben's three changes of
   2026-10-03 refined the trial's steps after it ran, and `doc/dual-agent-review.md:62` still calls
   the process "a next-review trial". No tracked record holds a decision of his on which governs.
   The sentences date from `db59ef5e`; six window commits edited these sections without marking the
   MAM-basics instance spent. Single-agent reviews are unaffected.
2. **Introduced by `4b795109`.** `doc/periodic-review.md:19–23` says that every rule about how one
   reviewer finds, checks and records findings belongs there and that `doc/dual-agent-review.md`
   "records only what pairing adds" (`doc/dual-agent-review.md:26–27`, from the same commit,
   agrees). Yet `doc/dual-agent-review.md` still holds single-agent rules: D10's filename and line-3
   State rules (`doc/dual-agent-review.md:703–712`), to which `AGENTS.md:125–127` and
   `doc/periodic-review.md:192`, `:223–225` and `:292` send a single-agent reviewer, although
   `doc/periodic-review.md:11–12` (older, `a2af0c1b`) says to read that document only for a
   two-agent window; and D12 (`doc/dual-agent-review.md:311–325`). This review needed D10.
3. **Question.** The rule that a reviewer's brief names the private repositories takes them from
   `repo_visibility` (`doc/dual-agent-review.md:84–87`; `doc/periodic-review.md:198–202`,
   `:236–238`), which declares only MAM-private and hbofonts private; it omits the private
   `bdenckla/trope`, which the tree cites (`trope#NN (private tracker)` on 13 lines of six
   `py/yeivin_itm/content/` modules) and finding 3.3 reaches, and al-hatorah, whose remote the same
   policy file calls "live, private and complete" (`in/repo_maintenance_policy.json:69`). For a
   MAM-private window the list would also name the window's repository. The wording is Ben's
   approved change 3 of 2026-10-03.
4. **Introduced by `4b795109`.** `doc/periodic-review.md:260–262` says a claim that only a
   transcript can check "goes to Ben in chat rather than into the file, as D9 and D11 of
   `doc/dual-agent-review.md` require of a turn". D9 says such a claim "stays out of a tracked turn
   under D11" (`doc/dual-agent-review.md:294–295`), and D11 requires a turn to record enough to
   check a claim without scratch (`:374–381`); neither says it goes to Ben in chat.
5. **Introduced by `4b795109`.** D9 glosses "public evidence only" as reading nothing in MAM-private
   (`doc/dual-agent-review.md:291–294`), citing property 2 of `doc/periodic-review.md`, which
   `4b795109` widened to every repository `repo_visibility` declares private, hbofonts included
   (`doc/periodic-review.md:198–201`), so the two texts now define "public evidence only"
   differently.

### 7. Checks and tools that do less than they say

Unfixed at `139e2d63`. Each is minor. Items 1 to 4 and 7 are latent: nothing in the tree trips them
today. Items 5, 6 and 8 need no change to the tree, only a state at run time: a Claude session
working in a linked worktree under the clone, or a dirty clone that only the caller occupies (5); a
file held open during a relocation (6); a Git failure or an unreadable branch ref during
maintenance's step 2 (8). Items 9 and 11 need a client's input, and item 10 an adapter that writes
non-UTF-8 output. Every demonstration below was run again by a checker, or, for the additions to
items 2 and 4, by a checker's sub-agents and then by the further checker's, in memory, on scratch
copies or, for the file-free compute command of items 9 and 11, by subprocess; items 10 and 11, and
the additions to items 2 and 4, come from the pre-commit check's omission sweep.

1. **Introduced (restated) by `1c42c5b1`.** The pre-write parser-stage check validates verse cells
   only (`py/verify_mp/parser_stage.py:376`) and never `good_ending_plus`, the only other wikitext
   in plus (`py/py_misc/mam_parsed_plus.py:85`, `:181–186`): all 8 cases that stream D injected
   there pass, 4 encodings each in the element's parameter 1 and as the whole element. The new
   lint's docstring says that `_validate_no_parser_stage_encoding` "refuses any dict in plus with a
   key in `PARSER_STAGE_NODE_KEYS`" (`py/tests/test_parser_stage_node_keys.py:3–4`). The gap dates
   from `146f6145` (2026-09-28).
2. **Introduced by `1c42c5b1`.** That lint reads only the classifier's top-level `if` statements and
   the return constants of two helpers, so a fourth encoding admitted through `ws_tmpl1.is_template`
   or an `elif` passes it (`py/tests/test_parser_stage_node_keys.py:38–48`; stream D's mutations M1
   and M2). The lint pins only the key set, so reverting the refusal's body
   (`py/verify_mp/parser_stage.py:343–344`) to the start commit's `assert "stmpl" not in node`
   passes every test, and, since plus holds none of the three keys, `parse-ws` and the mega too:
   C12.1's fix has no regression guard. The plan's specification shares both gaps: its check is that
   lint, and "No example-based injection test is added"
   (`doc/PLAN-remediate-review-findings-2026-10-02.md:1578`).
3. **Introduced by `8ad4c1d2`.** The pipeline-graph lint checks that each listed step runs the
   node's program, not that the node lists every such step
   (`py/tests/test_mega_coverage.py:1174–1191`), while the spec promises "a solid box labelled with
   its step ids" and a check of every program node against `_STEPS`
   (`py/pipeline_graph/pipeline_graph_spec.py:9–13`); dropping `mam-simple-docs` from a node passes.
   The plan's specification of the test shares the gap
   (`doc/PLAN-remediate-review-findings-2026-10-02.md:1022–1026`).
4. **Introduced by `a363e5ce`.** `review-claims` collects its report, renders the projected pages
   and only then prints (`py/yeivin_itm/publication.py:66–103`), so when a claim printed in words
   would reach 7, the word-form raise (`py/yeivin_itm/claim_text.py:38–39`) prints none of the
   report its docstring promises, which the refresh procedure relies on: at a projected 6 it prints
   39 lines, at 7 none. Both such claims are 2 today. It prints nothing either when a claim's
   denominator empties, since its first statement, `claims.projection()`
   (`py/yeivin_itm/publication.py:74`), raises "Empty claim population"
   (`py/yeivin_itm/claims.py:157–158`); the smallest of the 20 denominators is 18.
5. **Introduced by `00974386`, in the plan's approved wording.** `doc/clone-forests.md:47–52` says
   the write form skips the clone that only the calling Claude session occupies, recognized by a
   session record "whose working directory is in the clone". A session working in a linked worktree
   under the clone (`.claude/worktrees/`) is counted twice, once as a session
   (`py/repo_util/forest_sync.py:142–143`) and once as worktree occupancy (`:144–155`), so the write
   form refuses it and exits 1. The code follows the plan's "exactly that one string"
   (`doc/PLAN-remediate-review-findings-2026-10-02.md:1763`), and the page's last sentence
   (`doc/clone-forests.md:53–54`) can be read to cover the case, so it is the page's account of the
   skip that is imprecise. **Question:** the skip (`py/repo_util/forest_sync.py:288`) returns before
   the dirty, off-`main`, mid-operation and locked reasons collected at `:277–283` are consulted
   (`:295–296`), so such a clone that only the caller occupies is skipped, while
   `doc/clone-forests.md:38–39` and the module docstring say it is refused; which the plan meant is
   Ben's call.
6. **Older.** A `.novc` relocation that fails on a file held open leaves a `relocation_failed`
   sidecar that `_reconcile_relocations` refuses on every later execution: on the cross-volume path
   even after the leftover source is removed by hand, and on the default same-volume path, where
   nothing moved, until the sidecar is deleted, which
   `dot-claude/skills/mam-repository-topology/references/repository-maintenance.md:175–176` forbids;
   no tracked procedure says how to repair it
   (`py/repo_util/worktree_retirement_relocation.py:44–80`, `:134–146`). The window fixed only the
   read-only trigger, as C9.5's plan scoped it; the code was introduced by `4530b32a` and carried
   through `7014cfbb` and `89ae4b85`.
7. **Introduced (restated) by `936d7b45`.** The forest launch lint's docstring says it recognizes a
   launcher called through any name that `from ... import` binds
   (`py/tests/test_forest_subprocess_bounds.py:29–32`), but a star import, `getattr`, `__import__`
   and `importlib` dispatch all evade it in synthetic modules; in the two real modules a star import
   would still fail the lint, though only by disqualifying every `GIT_TIMEOUT_SECONDS` bound, and
   ruff's F403 and F405 would flag it. The sentence is `9588700f`'s; `936d7b45` kept it, widened the
   list it covers and rewrote the limits (`:37–39`) without naming these.
8. **Older.** `py/main_repo_maintenance.py:17` calls its steps "Seven independent steps", but a
   `RetirementError` from step 2's `clean_worktrees()` (`:226–227`) stops steps 3 to 7.
9. **Older.** A compute request line holding a bare carriage return, which JSON allows between
   tokens, gets two replies on Windows, where standard input keeps universal newlines
   (`py/main_phonetic_mam.py:67`, `py/phonetic_mam/compute.py:302`), against
   `doc/phonetic-mam-compute.md:6`'s "Each input line receives one output line" (stream B, by
   subprocess at both commits).
10. **Introduced by `95683791`.** The exporter's test-page run now captures the adapter's stderr and
    decodes both pipes strictly (`py/phonetic_mam/exporter.py:216–227`), while the streaming run
    decodes stderr with `"replace"` (`:28–64`, `:174`). On Windows, with a timeout and two pipes, a
    decode error kills the reader thread: non-UTF-8 stderr from a failing adapter yields "its stderr
    ended with:\n(nothing)", which C15.19's plan reserves for an empty tail, and non-UTF-8 stdout
    after exit 0 yields a `TypeError` where the start commit raised an accurate
    `UnicodeDecodeError`. Shown with fake adapters and nothing reaching MAM-private; the adapter
    inherits `dict(os.environ)`, so `PYTHONUTF8=1`, or the `PYTHONIOENCODING` that the Claude
    desktop app's shells set, hides it (`dot-Codex/user-wide-AGENTS.md:413–416`); tracked code may
    rely on neither.
11. **Older.** A compute success reply that echoes a JSON-escaped lone surrogate, as a `phrase`
    reply copies its untangler keys into `untangler-use-counts`, is encoded with
    `ensure_ascii=False` and written outside the `try` to a strict UTF-8 stdout
    (`py/phonetic_mam/compute.py:312`, `:323`; `py/main_phonetic_mam.py:68`), so the process dies
    with `UnicodeEncodeError` and later lines get no reply, against `doc/phonetic-mam-compute.md:6`;
    `38cf30ea` closed only the undecodable-byte route of this class. The census of echo routes is
    not complete.

### 8. Questions for Ben

All unfixed at `139e2d63`, each awaiting a decision of Ben's, and each minor; the label says whether
the matter is older than the window. Every item was re-derived by a checker; the pre-commit check
moved three items of an earlier draft to finding 9, merged two into item 6 and dropped three that
were neither defects nor decisions Ben owes.

1. **The Job footnote's "orphaned"** (`py/author_boj_qr/qr_38.py:131`, from `3e446584`) uses the
   word for any point that belongs to no letter, as the Job "Orphan pointing" page does
   (`py/author_boj/job5_orphan_qere_points.py:79`), while `hebrew-prose`'s
   `references/terminology.md:380` reserves "orphaned" for the ḥiriq of the implicit yod, a
   reservation that reached MAM-basics (`74d883d2`, 2026-09-09) after the Job pages' usage
   (`ef8e384c`, 2026-08-19); whether it reaches the Job pages is Ben's call.
2. **No tracked record gives the image source or the crop coordinates of the two new crops**
   (`6004709e`, `a1bbce52`); their captions name the manuscript, verse and page
   (`py/author_boj_qr/qr_38.py:104`, `:150`), and `DATA-LICENSES.md:122` leaves them, like every
   crop in `jobn/img/`, "each rights holder's". `doc/boj-image-crop-reproducibility.md:5` says its
   principles "still govern any crop made in future"; older practice lacks such records too: only
   the Cambridge 1753 crops carry them, and only in part (of the 160 records in
   `book-of-job/out/cam1753-crops.json`, 107 give coordinates and 109 a source, and 107 of the 160
   PNGs embed them), and none of the 160 Aleppo, 160 Leningrad or 5 older root crops does. Whether
   those principles reach a crop supplied as a finished image is Ben's call.
3. **The site's landing page lists four MAM dataset READMEs and not Phonetic-MAM's**
   (`gh-pages/index.html:23–28`, from `py/author_site/site_data.py:145–151`), though it links
   Phonetic MAM's pages among the editions (`gh-pages/index.html:16`), against the page's
   description, "links to editions and datasets of MAM" (`gh-pages/index.html:11–12`); whether the
   release's README belongs in the dataset list is Ben's call; older.
4. **Eight English pages credit Hebrew Wikisource with a he.wikisource link**, not the en.wikisource
   page that the MAM statement prescribes for English attribution: the three translated-introduction
   pages under `gh-pages/MAM-with-doc/misc/`, two Aleppo pages and three of the four
   printed-Decalogue pages (the fourth, `printed-decalogue-uvinkha.html:17`, credits it with no
   link); C15.8 covered only the two index pages; older. Whether these credits are the attribution
   the statement governs is Ben's interpretation.
5. **The terms of the 505 pointed-Hebrew strings in `Phonetic-MAM/examples/display.json` are
   unstated** (`Phonetic-MAM/LICENSE.md:3`, `DATA-LICENSES.md:55–56`); whether they are MAM text
   carrying MAM's terms is Ben's call (older, restated by `007f9f31`).
6. **Two present-tense sentences of `Yeivin-ITM/README.md` outlived the gate that `59e41a99`
   retired.** `:52–53`, "Its source is pinned to MAM-private commit …", reads as a live pin, though
   no test pins the adaptation now and 10 of the 112 hashed modules differ from the frozen hashes;
   and `:58–59`, "All 17 existing filenames, internal links, and anchors are preserved", is true,
   but C6.2's option C kept it "since it remains enforced"
   (`doc/PLAN-remediate-review-findings-2026-10-02.md:1411–1413`), while the tests now hold the
   anchors, link resolution and, through `py/tests/test_redirect_manifest.py`, the filenames, not
   each legacy link; option A's "The migration preserved …" was the alternative.
7. **`doc/PLAN-mega-speedup.md`** (State `live`) still says that a cloud run skips the
   post-stress-meteg survey: in its executed Phase 2's steps (`:416–418`, "which reads
   MAM-private"), which its `:333` leaves as written, and in its maintained list of things carried
   forward (`:336–338`), which that clause does not cover, against `iterative-document-editing`'s
   rule that plans still being executed "stay true in place"
   (`dot-claude/skills/iterative-document-editing/SKILL.md:88–89`); its 2026-10-01 disposition says
   the survey runs in cloud sessions (`doc/PLAN-mega-speedup.md:173–176`), and the one step a cloud
   run skips is now `phonetic-mam-export`; whether `:333`'s clause should reach that list is Ben's
   call; older.
8. **The common body's Unicode section** (`dot-Codex/user-wide-AGENTS.md:406–407`) still says only
   "reconfigures stdout and stderr to UTF-8", without the handler that `hebrew-prose`'s
   `references/verifying.md:229–231` and the new lint now require; changing Ben's user-level text is
   his decision.
9. **`rendered-prose.md` calls the Hebrew-letters strand rule both trio-only (`:9`) and "Cross-repo"
   (`:24`)**, and `SKILL.md:35` now sends readers there for the rule's scope; the module that
   `rendered-prose.md:24` cites romanizes the names
   (`py/versification_and_cantillation/doc.py:173`), which fits trio-only; older.
10. **Twelve calls on eleven lines apply `unicodedata.normalize` to Hebrew**, against `AGENTS.md`'s
    "Never call `unicodedata.normalize` in any form on Hebrew", with no recorded exception: nine to
    Hebrew text (`py/accgram/decalogue_m_trad.py:154`, `py/main_uxlc_word_list.py:57`,
    `py/mb_cmn/uni_norm_fragile.py:29`, `py/py_render/rt_validate_holam_he.py:170`,
    `py/py_wlc_json_and_unicode/wlc_compare_mdc_with_uxlc.py:51` and `:52`, and
    `py/tests/test_decalogue_m_trad.py:113`, twice, and `:124`) and three NFKD calls to Hebrew
    presentation forms (`py/hkq_cmn/extract_docx_notes.py:52`,
    `py/tests/test_extract_docx_notes.py:89` and `:95`); a composability probe
    (`py/tests/test_transliterations.py:130`) also passes Hebrew pairs. None is in the window's
    added lines, and each arrived with copied or vendored code, seven of them, on six lines, with
    the wlc-utils and UXLC-utils copies (`7e8ee0f2`, `f202d219`), while the rule stood only in two
    disabled instruction files (`.github/copilot-instructions-disabled.md`, `CLAUDE-disabled.md`),
    before `2b671ae1` restored it on 2026-08-04; whether the rule admits these uses is Ben's call;
    older.

### 9. One-line items

All unfixed at `139e2d63`; "introduced" unless marked older.

1. The two new PNGs made four undated counts false: `doc/book-of-job-artifacts.md:9–10` (701 and
   518, now 703 and 520) and `:20` (5 PNG, now 7), and `py/boj_paths.py:175–176` (515 of 694, now
   517 of 696) and `:208` (485, now 487); recounted here with `git ls-tree` at both commits (stream
   H).
2. The footnote's heading calls its two comparison cases "the parallel passages"
   (`py/author_boj_qr/qr_38.py:188`), where the discussion that calls the footnote names them
   "Similar cases" (`:35`) and the footnote's body "The similar כתיב/קרי word-boundary shifts"
   (`:76`), against "Give one thing one name" (`3e446584`; stream H).
3. `DATA-LICENSES.md:122` calls the Jerusalem Crown a manuscript; it is a printed edition (older,
   `fdf8f3ec`; stream H).
4. `Phonetic-MAM/LICENSE.md` and `Yeivin-ITM/LICENSE.md` have no row in `DATA-LICENSES.md`, whose
   older product rows cover their licence files, though `Phonetic-MAM/LICENSE.md:4` says
   `DATA-LICENSES.md` records the terms of that directory's other files (`007f9f31`, the plan's C4.3
   wording; stream C).
5. `py/tests/test_product_scopes.py:13–29`'s "WHAT IT CHECKS" omits the new licence lint
   (`:133–143`) (`007f9f31`; stream C).
6. `py/mb_cmn/paths.py:9–10` still lists five landed products beside `phonetic_mam_dir`, a site
   beside the three that C10.4 named (older, from the merge `9a67d51b`, found with `git log -m`;
   stream C).
7. Five binary files carry no `binary` attribute, though every PNG, JPG, PDF, WOFF2 and ZIP does and
   `* text=auto` already leaves the five unconverted, a consistency point (older); and
   `.gitattributes`'s "Copied verbatim from wlc-utils' .gitattributes" now heads three lines that
   did not come from there, one from `32fa7da6` and two added by `6581e5a4` (stream C).
8. `README.md:116–121` reads the GPL-covered `out/` clause as one more exception (restated by
   `007f9f31`, the plan's C4.7 wording; the shape is older), and
   `gh-pages/MAM-with-doc/index.html:18` has no separator before "Source attribution:" (older;
   stream C).
9. `Yeivin-ITM/README.md:59–68` lists three commands, "All three commands", without `a363e5ce`'s
   `review-claims` (stream A).
10. The reference lint's docstring (`py/tests/test_yeivin_itm.py:108`) and
    `Yeivin-ITM/README.md:122–124` say "each" and "every" reference, but the lint reads data
    attributes and full-match source literals only; two references written with a book name occur
    only in visible text, and so do the five alternative numberings of `_ISE_RECORDS`
    (`py/yeivin_itm/content/my_yeivin_amisc_helpers_for_bibrefs.py:6–12`), such as "others have it
    as 31:18"; all name real verses (`f2774cea`; stream A).
11. `py/accgram/post_stress_meteg_model.py:42–45`, and the same module's `_intervening_punctuation`
    docstring (`:740–741`), say that Phonetic MAM does not distinguish narrow-sense paseq from
    legarmeh; the release's display separates them (older, `e91d7358`, moved here by `44f03b15`;
    stream A).
12. The mpplus guide names two audiences for the notice, "people and programs" (`mpplus.html:105`)
    and "writers of programs" (`:539`) (`a7a5803a`; stream D).
13. The bot guide's "That list should name exactly the chapters that the edit file targets"
    (`py/ws/pywikibot-setup.md:86–87`) and "a re-run fails at the first chapter whose guard it
    checks" (`:100–101`) hold only in the common case (`6c303371`, the plan's approved C7 text;
    stream D).
14. The guide (`py/ws/pywikibot-setup.md:55–59`) and `--no-post-download`'s help say the post-run
    download refetches the 36 special pages; it refetches nothing when no chapter changed (older;
    stream D).
15. "Here’s the header for Job, a book24 has no sub-books:" lacks "that"
    (`py/author_misc/mp_body_shared.py:64`) (older; stream D).
16. `doc/clone-forests.md:22` says "a Git lock file"; the check form detects five named lock files
    (`6a55f8e0`, the plan's wording; stream E).
17. The 2026-10-02 update's reason for skipping the mega at `b246e05e`, that the 35 changed lines
    are in `main()` or `__main__` "which no mega step runs"
    (`doc/review-findings-2026-10-02-update.md:810–813`), is false for 11, whose `main()` the mega
    runs in process; its conclusion stands (stream E).
18. `py/main_explicit_xataf.py:131–133` reconfigures the streams in `almost_main`, which the mega
    runs as a step, though the mega's setting comes first; C15.3 moved `main_sigil_inventory`'s like
    line out of its `almost_main` (question; the stderr line restated in place by `750844b9`, as
    C15.4's plan directed, the stdout line from `d86e5779`; stream E).
19. `forest_sync.py:359–361`'s failure line gives "behind origin/main" as a cause, which a write
    cannot have (older; stream E).
20. `py/main_0_mega.py:611`, the `phonetic-mam-render` step record, still names only the release
    among its inputs and omits the asset, image and font inputs and the shared font-sources output
    that the window's other two render descriptions now name (older; stream B).
21. `py/main_uxlc_grammar_test.py` matches pytest's `*_test.py` pattern, the class of C15.20, though
    it is not in the default collection (older, `7e8ee0f2`; stream B); `py/main_test.py` matches it
    too, but `AGENTS.md:227` and the common body name that file, so for it this is a question.
22. Eleven `powershell` blocks with unreplaced `<placeholder>`s do not parse, against "Commands
    written for Ben", the class C15.24 fixed at five of its six sites:
    `doc/user-wide-instruction-conversion-reconciliation.md:103`,
    `doc/PLAN-repo-maintenance-across-GitRepos.md:427`, `:431`,
    `dot-claude/skills/mam-repository-topology/references/repository-maintenance.md:18`,
    `MAM-parsed/historical/README.md:65`, `:96`, `:102`,
    `doc/PLAN-silluq-before-gaya-template.md:266`, `:485`,
    `doc/edition-transcription-workflow.md:244` and `:279`; and
    `doc/PLAN-repo-maintenance-across-GitRepos.md:770`, in an unlabelled fence, chains three
    statements with `;` and does not parse either, since it pipes a `foreach` statement to
    `Format-Table` (older; streams G and I). The list is complete for the 225 `powershell` fences in
    tracked Markdown; eight placeholder blocks in unlabelled or `bash` fences fail the same way (a
    checker's parse of every fence).
23. `mam-basics-trackers.md:132–133` says the routing section (`:211–219`) "records no number
    collisions for them", which reads as "has none", though it names `phonetic-hbo#78` (`:218`),
    whose number MAM-basics #78 shares (`7bd5ee8c`, the plan's wording; stream G).
24. `holman/doc/uxlc-email-count-disagreements-update.md:11–12` calls a whole sentence "its second
    half" (`b7f7e204`, the plan's wording; stream G).
25. `hebrew-prose`'s `references/mam-basics.md:37–38` says `9a67d51b` rewrote "the docstrings that
    held the other five"; one of the five, `py/accgram/breuer_word_length.py:105` at `9a67d51b^1`,
    was a comment (`7bd5ee8c`, the plan's wording; stream G).
26. `evacuated-repositories.md:58`'s "It raises with the command that fixes it" follows a clause
    whose subject is a test that prints no command (older; stream G).
27. `doc/dual-agent-review.md:151` still says the relay is software Ben "hopes to discard soon",
    beside `:433–434`'s record of its removal (`742aaf41`, left by `4573b007`; stream I).
28. `doc/dual-agent-review.md:434` and the October 1 update
    (`doc/dual-agent-review-2026-10-01-turn-01-claude-update.md:363`) call `cbd405b1` "the last
    commit whose tree holds" the removed files; `d168e22e`, merged by `f0c50473`, holds all ten
    (`4573b007`; stream F).
29. The October 1 update (`doc/dual-agent-review-2026-10-01-turn-01-claude-update.md:363–364`) says
    every path and line the round's records cite in the removed files resolves at `cbd405b1`; the
    paths do, but the line numbers point at other code there (`4573b007`; stream F).
30. `doc/dual-agent-review.md:429–430` and `:444` call the October 1 round the relay's "only round";
    the runbook records an isolated rehearsal round and two probe rounds (at `cbd405b1`,
    `doc/dual-agent-review-automation.md:229–233`, `:271–279`, `:295–316`) (`4573b007`, the plan's
    R6 wording; stream F).
31. `py/tests/test_review_turn_files.py:4–7` names one of the two checks it dropped, not
    `lint_automated_round_headers`, the `Next:`-header check (`4573b007`; stream F).
32. D10's item 4 (`doc/dual-agent-review.md:716–719`) lists `Next:` lines among filenames and State
    lines (`4573b007`, R6.9's wording; stream F).
33. The October 1 update (`doc/dual-agent-review-2026-10-01-turn-01-claude-update.md:331–332`) still
    says evidence "is retained" in a worktree that the same file records as removed on 2026-10-04:
    `184ecd15` wrote it true, and `b61481ff`, which records the removal and corrected two other
    passages of the file in place, left it (stream F).
34. The two crops' alt texts romanize פתח as "patah" (`py/author_boj_qr/qr_38.py:94`, `:139`), where
    the Job pages' romanization table has "pataḥ" (`py/author_boj_util/author.py:490`) (`14baabe3`,
    `3e446584`; stream H).
35. The new quirk-record field `qr-footnotes` (`py/author_boj_util/job_ov_and_de.py:359`) is not in
    `doc/boj-quirkrec-comments.md:9–15`'s list of where comments live, and the μY-mentions page
    reads only the two older comment fields (`py/author_boj/job6_cam1753_mentions.py:38–41`), so a
    future footnote mentioning μY would be missed; `py/author_boj_util/flatten_qrs.py:5–22`, which
    flattens three other fields for `py/author_boj_util/prep_quirkrecs.py`, also passes the new
    field over (`3e446584`; stream H and the omission sweep).
36. On POSIX, the read-only handler (`py/repo_util/common.py:23–26`) sets mode 0o200 on what it
    retries and still fails, since POSIX refuses an unlink for the parent's permissions; reasoned
    from the code, with no Linux run (`a1c4a746`; stream E).

Items 37 to 42 come from the pre-commit check's omission sweep, each re-run or re-read by it.

37. `py/accgram/meteg_before_stress.py:13–15` says a candidate whose U+05A5 follows an oleh on the
    previous chanted word "is refused"; the code refuses only after an unpaired oleh (`:140–145`, as
    its docstring at `:133–134` says), and four candidates, Psalms 28:1, 28:7, 59:13 and 125:1,
    follow a paired oleh and are classified conjunctive (`c17de175`).
38. Question: the exporter's book-limit error gives the exit status that its kill of the adapter
    produces, "(exit status 1)" on Windows, so it reads as a failure of the adapter
    (`py/phonetic_mam/exporter.py:87–89`, `:179–185`) (`95683791`, the plan's wording).
39. Question: a compute request of exactly 16 Mi characters ends the stream with no reply when a
    newline ends it but is answered when unterminated (`py/phonetic_mam/compute.py:302–304`, against
    `doc/phonetic-mam-compute.md:19–20`) (older, `9a67d51b`).
40. The untangler test's file-access guard denies only `builtins.open` and `pathlib.Path.open`
    (`py/tests/test_phonetic_untangler_preparation.py:44–48`), and the compute-boundary lint checks
    `compute.py` only for bare-name calls (`py/tests/test_phonetic_compute_boundary.py:88–90`), so
    an `io.open` or `os.open` in `compute.py` passes both (older; the window's `ac25adc9`, C12.3,
    renamed the test to `test_preparation_operation_runs_without_file_access` and left the guard as
    it was).
41. `README.md:18` says "A solid box is a step of `py/main_0_mega.py`", where the graph's legend
    says a solid box is a program that mega steps run, labelled with their ids
    (`py/pipeline_graph/pipeline_graph_spec.py:93–94`), and it says "directories" though one drawn
    store is Hebrew Wikisource (`8ad4c1d2`).
42. `test_real_check_command_is_write_neutral` (`py/tests/test_yeivin_itm.py:193–214`) cannot fail
    on the "including Python import caches" half of `py/main_yeivin_itm.py:58–61`'s claim, which
    since `38cf30ea` only `main()` makes true: where bytecode writing is on, pytest's collection
    imports write those caches before its snapshot, and where it is off, as in this review's
    session, whose process environment sets `PYTHONDONTWRITEBYTECODE=1`, the child writes none
    either way (older, `9a67d51b`, made load-bearing by `38cf30ea`).
43. `py/accgram/printed_decalogue_uvinkha_page.py:486` and `:491` give two alt texts "Minhat Shai"
    (`gh-pages/wlc/accgram/printed-decalogue-uvinkha.html:126`, `:131`), while the page's prose has
    "Minḥat Shai", against `hebrew-prose`'s accgram rule that ḥet is never h
    (`references/terminology.md:494–497`) (older, `7e8ee0f2`; found by the re-check).

## Noticed outside the diff, not findings

1. Issue #296, opened 2026-10-03T06:17:53Z, says it was written by a Codex session but gives no
   date, which `github-issues` rule 2 asks of an agent-written issue (stream I; read again by a
   checker); editing it is an outward-facing act for Ben.
2. `_reference_matches` (`py/repo_util/worktree_retirement_inspection.py:264–295`), unchanged in the
   window, does not count a `path:line` form as a citation of the file: called in memory at
   `139e2d63`, it rejects `check-b.md:3`, `:3:`, `:3-5` and `#L3`, the form that
   `doc/dual-agent-review-comparison-2026-10-01.md:488–489` uses. The September 26 plan's
   specification does not say whether such a form counts, so this is an older question (stream F's
   lead, run by a checker).
3. At Genesis 35:22 the release has one marker, "פפפ", where MAM-parsed's dual-cantillation template
   has "פפ" in both strands (`MAM-parsed/plus/A1-Genesis.json:16022–16030`). The repository
   documents פפפ as an open parashah with no blank line
   (`py/author_misc/mp_cmn_rows_other.py:81–82`; `py/mb_cmn/mam_xml_verses.py:82–84`), while MAM's
   note on the verse reports a blank line in three manuscripts
   (`MAM-parsed/plus/A1-Genesis.json:16019`). A further checker's census of break markers found,
   besides ססס rows that the release has and MAM-parsed lacks in passages laid out as songs, only
   two other differences, at Exodus 20:13 and Deuteronomy 5:17, where the release has "סס" for
   MAM-parsed's mid-verse "ססס"; the root reviewer re-read the three verses in both (the omission
   sweep and the re-check; noticed, not assessed).

## Open ends the window itself declares (not findings)

1. **`origin/dar-2026-10-01` stays**: act A6 of the 2026-10-02 plan is not done, by Ben's choice
   (`doc/PLAN-remediate-review-findings-2026-10-02.md:2892–2893`;
   `doc/PLAN-remediate-review-findings-2026-10-02-update.md:16–17`).
2. **The residue phonetic-hbo clone stays Ben's decision**
   (`doc/review-findings-2026-10-02-update.md:617`, the C3 row of its ledger, and `:105–106`).
3. **The September 29 round's finding 22 stays deferred**, with C5.2's new sentence in its entry
   (`doc/dual-agent-review-2026-09-29-turn-01-claude-update.md:1782–1798`).
4. **A browser with neither `:has()` nor JavaScript still cannot switch the Phonetic MAM display**,
   a residual the plan documented and declined under C13.2
   (`doc/PLAN-remediate-review-findings-2026-10-02.md:459–460`).

## What this review did not check

1. Anything in MAM-private or hbofonts beyond the forest check's result, their commits and their
   status-entry counts: the private adapter, whether its children inherit stderr (finding 4.5) or
   whether it ever writes output that is not UTF-8 (finding 7.10), Yeivin's printed text, which only
   private OCR holds, and the document that `in/repo_maintenance_policy.json:15` names as governing
   what about MAM-private's trees may reach a public repo (finding 3).
2. As subject: the two 2026-10-02 reports, the disposition list and Ben's recorded decisions, the
   plan and its update file, and the machine-act entries, apart from item 2 of one entry, whose
   public text finding 3.1 reports.
3. Real-browser rendering and live URLs; the font's OpenType name table (fontTools' WOFF2 reader
   needs Brotli, which is not installed).
4. A Linux or cloud run of anything: one-line item 36 is reasoned, and finding 4.5's test-page half
   and findings 7.9 and 7.10 were measured on Windows only; the worktree-retirement simulation to a
   pass, which stream E could not run inside its scratch directory because of Windows path lengths.
5. The line-by-line classification of finding 3.4's census hits, beyond a count by file kind; and
   command text outside Markdown fences (docstrings, inline code spans, non-Markdown files),
   together with the 16 parse failures without placeholders that a checker found in unlabelled,
   `bash` and `text` fences, which were not classified.
6. phonetic-hbo's redirect deployment, in another repository.
