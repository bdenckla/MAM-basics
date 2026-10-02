# Findings of the 2026-10-02 review of MAM-basics since 2026-09-29

State: not yet acted on

Written on 2026-10-02, from about 14:57 to about 16:15 New York time, by a fresh Claude session
(Claude Opus 5.5 at `max` in the Claude desktop app) as the Claude reviewer of the MAM-basics trial
review that Ben started that day under `doc/dual-agent-review.md`, "Next review: independent reviews
and one disposition list" (his decision of 2026-10-02). The kickoff session in
`C:/Users/BenDe/GitRepos2/MAM-basics` owns the trial and writes neither report; a Codex session in
`C:/Users/BenDe/GitRepos3/MAM-basics` reviews the same window independently. This session did not
open `doc/codex-review-findings-2026-10-02.md` or any other account of the Codex review. Nothing was
fixed. Every time here is New York time and every figure was measured on 2026-10-02. The file follows
`doc/periodic-review.md`, "What a review file contains", and adds one short last section of notes on
the trial procedure, because Ben's instruction at kickoff asked this review to flesh that procedure
out; minor wording and plan inconsistencies are collected as one-line items in finding 15.

**The checkout.** The session opened in the owner's clone, `C:/Users/BenDe/GitRepos2/MAM-basics`.
The kickoff prompt assigns the Claude reviewer to `C:/Users/BenDe/GitRepos/MAM-basics` and says to
stop if the session is anywhere else, and the kickoff section of `doc/dual-agent-review.md` adds that
no reviewer uses the owner's checkout. Before anything else the session ran `git status` in both
clones, read that kickoff section in the owner's clone to confirm the assignment, and asked Ben; he
chose "Move, then I say go (Recommended)", and the app's change-directory tool moved the session. In
the reviewer's clone `main` was clean at `f3760d1c`. A fetch this session did not issue (its reflog
form, `fetch ... --porcelain --verbose --no-write-fetch-head`, is not this session's) moved
`origin/main` to `699c7b17` at 14:56:40; this session's own `git fetch origin` then moved only
`origin/dar-2026-10-01`, and `main` was fast-forwarded to `699c7b17` at 14:57:36. `699c7b17` is the
kickoff's last commit and contains the window's end, `db59ef5e`; the only path whose text differs
between them is `doc/dual-agent-review.md`, two documentation commits that record the kickoff, so
every check below that ran at `699c7b17` speaks for `db59ef5e`'s code and data. The window's version
of that one file was read with `git show db59ef5e:doc/dual-agent-review.md`.

**Which records inside the window are subject and which are evidence.** Ben decided this at kickoff
("Evidence only; skip relay (Recommended)"); the trial's step 1 gives him the decision that
`doc/periodic-review.md`, "A prior round's own records inside a successor window", would otherwise
leave to this review's opening. Evidence, not subject: the September 29 round's
turn files 01 to 11, its turn-01 update file and `doc/PLAN-remediate-review-findings-2026-09-29.md`;
the October 1 round's round file, turns 01 to 05, turn-01 update file,
`doc/PLAN-close-out-review-2026-10-01.md` and `doc/dual-agent-review-comparison-2026-10-01.md`; the
relay software (`py/repo_util/dual_agent_review_dispatch.py`, `dual_agent_review_round.py`, their two
test modules, `doc/dual-agent-review-automation.md`, `doc/PLAN-automate-the-dual-agent-review-relay.md`,
`in/dual_agent_review_automation.json`, the two `misc/` relay scripts and
`dot-claude/agents/dual-agent-review-turn.md`); the hunks the relay commits `1a50d4b6` and `2e120b85`
contributed to `py/main_repo_util.py`, `py/repo_util/user_config_sync.py` and `dot-claude/README.md`;
and the passages of the two procedure documents that describe the automated relay. Everything else
is subject, including the September 29 round's remediation of code, data and documents.

**How it was read.** Twelve read-only sub-agent streams read the window, each writing only its own
files under the untracked `.novc/review-2026-10-02/` (the brief every stream read first is
`stream_common.md`; each report is `<letter>_report.md`): P1, the Phonetic MAM computation, export and
release; P2, the Phonetic MAM renderer and its published site; Y, Yeivin ITM; F, fonts and licences; R,
the redirect stubs, the phonetic-hbo retirement and repository topology; M, the meteg surveys; V, the
parser stage, MAM-parsed, the Wikisource tooling and the pipeline graph; T, the forest, retirement,
user-configuration and hook tooling; U, the UTF-8 sweep and the small code and page changes; D1, the
instruction files and skills; D2, the maintained documents, reader-facing READMEs and retired
receipts; and W, whole-diff censuses (mark order, links, HTML, Pages, issues, mechanical rules). V and
W delegated parts of their work to sub-agents of their own and rechecked what they adopted. This
session ran the census, the suite, the mega and the lints itself, and before adopting a stream's
claim re-read the lines it cites or re-ran the measurement. Two figures here come from this
session's re-runs rather than a stream's report: finding 2's count of changed fractions (stream M
reported 9; the re-run gives 11) and finding 5.1's count of extraordinary points, on which streams M
and P1 differed (53 against 52; P1 counted verse text only). No blanket per-finding sub-agent check
was run before committing: the trial's owner verifies the findings instead
(`doc/dual-agent-review.md`, "Running a trial review", step 2).

**Departures from the rules, all read-only.** This session's stream brief at first called the
private hbofonts clone a public sibling; it was corrected at 15:31, after stream F had run `rev-parse`,
`ls-tree` and one `git show` of a licence file there and listed package names in its `.venv`, and
stream R had run `git ls-files` and `rev-parse` there. Neither stream F nor stream R uses anything it
read there, and nothing here relies on it. Stream F's directory search for `.venv` folders printed
four directory names under MAM-private and opened nothing. Stream V made one `gh repo view` metadata
query of `bdenckla/trope`, which proved private, and read no content. A sub-agent of stream W saw the
first line of a Codex-written comment posted on #250 after the window; nothing from it is used, and
this session read none of it. Some streams ran commands outside the shell rules: P2's first two calls used Bash with
`cd ... &&` and pipelines, D2 ran about ten display commands in Git Bash with `&&`, `sed` or `awk`, M one
PowerShell `foreach`, D1 two `;`-joined calls, T `bash -n` and two sandboxed hook runs in Git Bash,
and F ran FontForge's own `ffpython.exe` inside `.novc` to rebuild the font. Stream R used the app's
browser pane for two public page visits. Every stream reported `git status --porcelain` empty at its
start and end, and no tracked file was written.

## Scope, anchors and census

This review follows the September 29 round, which counted itself the tenth review under the
public-repos-only scope. It covers MAM-basics from **`7549ebf7`** (2026-09-29 11:21, "Require
approval for reusable lessons outside authorized task scope"), the end commit the September 29 round
recorded, through **`db59ef5e`** (2026-10-02 13:36, "Record the simplified process for the next public
and private reviews"), which was `origin/main` at kickoff. `7549ebf7` is an ancestor of `db59ef5e`
(`git merge-base --is-ancestor`). The October 1 automated round reviewed only the relay's own window,
`303bf239..1bfceff4`, and left the series' anchor where the September 29 round put it.

**148 commits, 118 non-merge and 30 merges.** The diff changes **1,533 paths**, the same with or
without rename detection: 226 modified, 1,297 added, 10 deleted and no renames, with **1,334,327
insertions and 6,012 deletions**; 14 of the paths are binary (`census2.py`). The tree went from 4,679
to **5,966** tracked files: `.py` 1,027 to 1,210 (1,019 to 1,202 under `py/`), `py/tests/` 115 to 124,
`gh-pages/` 1,894 to 2,908 files (588 HTML to 1,579), `doc/**/*.md` 117 to 137, `doc/PLAN-*.md` 22 to
19, `doc/*-update.md` 27 to 28, `in/` 320 to 337 and `out/` 329 to 330, plus two new product trees,
`Phonetic-MAM/` (42 files) and `Yeivin-ITM/` (3). Every product tree changed (`git rev-parse
<commit>:<dir>`): `MAM-simple/`, `MAM-for-Sefaria/` and `MAM-with-doc/` only in `LICENSE.md`, `MAM-OSIS/`
in its `LICENSE.md` and command example, and `MAM-parsed/` in its licence, two READMEs and the
notice line of all 24 plus files; MAM's text did not change in the window. The size is the
evacuation: `gh-pages/phonetic-mam/` alone is 985 added files and 1,189,732 inserted lines, and
`out/accgram/meteg-before-stress.json` another 75,888. The ten deletions are the nine receipts
`e4934b6e` retired and a JSON snippet the plain retirement left.

The window's substance is seven things:

1. The evacuation of the public Phonetic MAM and Yeivin ITM products from phonetic-hbo into
   MAM-basics (`a0016209`, `4b12bc41`, the merge `9a67d51b`, which itself adds most of the content,
   `f170616d`, `23750060`, `85f29edb`, `b04bef78`): the source-independent phonetic core and its
   read-only computation interface under `py/phonetic_mam/`, a closed public display release in
   `Phonetic-MAM/`, a unified Phonetic MAM site under `gh-pages/phonetic-mam/`, the editable Yeivin
   adaptation under `py/yeivin_itm/` with `Yeivin-ITM/meteg-claims.json` and 17 pages under
   `gh-pages/yeivin-itm/`, Taamey D's source package, a new meteg-before-stress survey, the
   post-stress-meteg survey's move from MAM-private's Phonetic MAM to the public release, and five
   new mega steps.
2. phonetic-hbo's retirement from routine ownership (`d0c660c9`) and its redirect conversion,
   prepared here (`5fae4331`) and executed in phonetic-hbo `2ca51088` on 2026-10-01 (stream R).
3. The September 29 round's remediation of code, data and documents (`d67bee39` to `37002a28` on
   2026-09-30, then `3451942e`, `71214987`, `9588700f`, `174357eb` and others).
4. The automated dual-agent review relay, its rollout and the October 1 automated round
   (`1a50d4b6` to `184ecd15`), all evidence here, and the record of the simplified process this trial
   runs (`db59ef5e`).
5. Instruction and skill changes: the six shared skills installed in Claude cloud sessions
   (`4d3ebf66`), the session's own checkout as every review's default (`89c001ba`), top effort for
   review turns (`38a360d2`), PowerShell 7 over Git Bash (`90d1169e`), the UTF-8 mode setup
   (`6cfcf8ee`), the private follow-up register (`c3eb743c`), a standalone prompt when ending with work
   remaining (`4f4cbb66`), and the retirement of nine spent receipts (`e4934b6e`).
6. Two sweeps: "name no forest" (`d54e12df`, `cb5bcda1`, `c71beed1`, `e2c1eae7`, `66582f1d`,
   `325a1c66`) and UTF-8 standard streams (`33470e2d`, `855e9eeb`, `0b7c77b1`).
7. Smaller items: the capture and translation of a Wikisource discussion about dagesh ḥazaq
   (`7577b56d`), and the bot's post-run writes in the refresh skill and the pipeline graph
   (`7c9bde53`, `24b39715`, `dd4f85df`).

## Tree health at `699c7b17`: the suite at 1,056 passed, the mega clean at 57 steps, 17 ruff errors

Before the first check that reads a sibling, `py/main_repo_util.py --sync-forest $HOME/GitRepos
--check` reported hbofonts 1 and MAM-private 53 commits behind `origin`; the synchronize form
fast-forwarded both, to hbofonts `6eb3ee0e` and MAM-private `1313c9ba`, and the check form then
reported all three clones level. The synchronize form exited 1, because it refused this session's own
clone (finding 9.3). The suite and the mega read those siblings through tracked code; this session
read neither itself.

- **Suite: 1,056 passed, 5 skipped, 60 subtests passed** in 1,529.51 s, from 15:02 to 15:27, run as
  `./.venv/Scripts/python.exe py/main_test.py -v -p no:cacheprovider` with twelve read-only streams
  running beside it (the September 29 round's run took 145 s); `git status --porcelain` empty
  afterwards. The collected ids go from 1,016 at `7549ebf7` (collected from an extracted start tree) to
  1,061: one only at the start (`test_graphviz_version_pin.py`'s renamed SVG test) and 46 only at the
  end (15 in the two relay test modules, 9 in `test_yeivin_itm.py`, 4 each in
  `test_entry_point_subcommands.py`, `test_phonetic_compute_boundary.py` and
  `test_phonetic_display_release.py`, 3 each in `test_phonetic_untangler_preparation.py` and
  `test_meteg_before_stress.py`, and 1 each in `test_forest_subprocess_bounds.py`,
  `test_phonetic_redirect_contract.py`, `test_redirect_manifest.py` and `test_graphviz_version_pin.py`)
  (`test_ids_diff.py`). The five skips are `test_edition_transcriptions.py`'s semantic channel, as at
  the start.
- **Mega: all 57 steps pass and leave no diff**, run once at `699c7b17` from 15:28:18 to 15:48:30,
  1,191.7 s of it in the steps; `git status --porcelain` and `git diff --stat` empty afterwards. The
  Graphviz pre-check reports the pinned 16.0.0 with Helvetica and the default font; the claims check
  passed 50 of 50 with none pending. So every generated product reproduces byte for byte at the end
  commit, the evacuated ones included: `phonetic-mam-export` (229.2 s) re-exported all 40 release files
  from the current MAM-parsed through MAM-private's adapter at `1313c9ba`, and `phonetic-mam-render`
  (103.5 s) rewrote the 985 site files, both without a byte of difference. Afterwards MAM-private was
  still at `1313c9ba` with no status entry, tracked or untracked (`private_state_counts.py`, which
  prints counts, not paths), so the export left that checkout unchanged.
- **The products' own validators.** `py/main_phonetic_mam.py check` and `py/main_yeivin_itm.py check`
  exit 0 and write nothing.
- **Hand-run generators.** `py/main_mam4sef.py` and `py/main_mam_osis.py` were not run: they build
  from MAM-simple's XML, which the window did not change (MAM-simple changed only in its
  `LICENSE.md`), the window did not touch their packages, and their products changed only in
  authored files.
- **Lints.** `black --check py` (26.5.1): 1,202 files unchanged. `ruff check py` (0.16.5): **17 errors**
  (finding 9.2). `py/main_repo_util.py --check-repo-standards --repos MAM-basics`:
  `SYS_PATH_MUTATIONS=0`, `SYS_PATH_IN_TESTS=0`, `HEX_ESCAPES=76`, `ORPHAN_MARKS=0`, `NFC_H_DOT=25` and
  `NFC_LATIN=72`, up from 32: all 40 new findings are the 39 `Phonetic-MAM/data/` files and
  `examples/display.json`, which `py/tests/test_h_dot_below_nfc.py:191–195` now exempts (finding 14).
  `git diff --check 7549ebf7 db59ef5e` prints nothing; `git ls-files --eol` shows no `i/crlf` or
  `i/mixed` entry among 5,966.
- **Mark order** (stream W). Of 1,950,193 pointed clusters in the diff's added lines, 5 are out of
  MAM-normal order, all in the faithful capture `doc/wikisource-dagesh-discussion-2026-10-01.mediawiki`
  (finding 15.13). `MAM-parsed/plus`, `MAM-simple`, `MAM-for-Sefaria`, `Phonetic-MAM`, `Yeivin-ITM` and
  the two new sub-sites are in MAM-normal order; `MAM-OSIS`'s 20 out-of-order clusters, in its
  historical `MAPM-orig` files, are unchanged.
- **Links** (streams W and D2). Of 403 non-absolute Markdown targets in 284 `.md` files, no dead link
  was introduced or broken in a subject file; all 26 fragment links and all 69 pinned blob and tree
  links the window added resolve.
- **HTML** (stream W). `py/check_html_syntax_and_sanity.py` reports no issue in its default mode and as
  `gh-pages --deploy-root`, with the same 1,140 informational CSS references as at the start; the two
  new sub-sites report none.
- **Pages** (stream W). Four `pages.yml` runs had a window commit as head, all successful: `90d1169e`,
  `1bfceff4`, `38c0116f` (manual dispatch) and `184ecd15`. The site deployed from `184ecd15` at 04:35 on
  2026-10-02 has `db59ef5e`'s `gh-pages` tree, `1cf6b558`.
- **Issues** (stream W). Activity in the window was three dated Codex-written comments at 11:31 on
  2026-09-29; no issue changed state, and no window commit cites an issue.
- **The user-level homes** (stream D1, rechecked here). Nine live destinations lag their canonical
  sources (finding 3).

## What verifies sound, stream by stream

**The census, the suite and the mega (this session).** The census section's figures; the suite's 46
added ids and one removed id accounted for by file; every mega product reproducing byte for byte; the
two product validators; MAM-private unchanged by the export; the 14 tracked `Taamey_D.woff2` copies one blob
(21,148 bytes); and `in/font-support/taamey-d-0.921/` byte-identical with
`gh-pages/font-sources/taamey-d-0.921/` (`woff2_identity.py`).

**The Phonetic MAM release (stream P1).** The committed release equals the legacy projection of
phonetic-hbo `8da90513`'s pages for 39 of 39 books, byte for byte. All 1,858 oracle hashes recompute
from public blobs, and `verify_site` passes. The public core regenerates the Sephardic and
Ashkenazic transcriptions of all 263,320 displayed readings and their displayed stress, and all 122
dual-cantillation rows. The schema validates, verse coverage is 23,202 verses, equal to MAM-parsed
plus, and the Hebrew is in MAM-normal order. Only `py/phonetic_mam/exporter.py` reaches MAM-private,
through `paths.require_sibling`, in a subprocess run with `-B` and `PYTHONDONTWRITEBYTECODE`.

**The Phonetic MAM site (stream P2).** The renderer is pure and its four dispatchers raise on an
unknown kind. All 991 publisher outputs re-render byte for byte from the committed release. All
1,858 chapter-and-pronunciation pairs match the legacy pages, the five example pages differ only by
the favicon line, and the five Jacobson images and the font are byte-identical: nothing a reader could
see was lost. All 7,687 internal `href` and `src` values and 110 fragment links resolve; all 272,837
Hebrew text nodes are in MAM-normal order, with no orphan combining mark and none of the forbidden
marks. 933 pages load Taamey D, and the index links the font's notice and source.

**Yeivin ITM (stream Y).** All 17 pages reproduce phonetic-hbo `8da90513`'s pages byte for byte apart
from the recorded changes: one favicon line on each, Ben's approved claim corrections on three pages,
and the landing page's font link. The stylesheet and font are byte-identical. `meteg-claims.json`
regenerates byte for byte from the committed survey; an independent recount agrees on all 20
fractions, and all 13 cited examples belong to their populations. The renderer is pure, and the HTML
checker and a link resolver find nothing.

**Fonts and licences (stream F).** Every size and hash the Taamey D source package records matches
the committed files and the public upstream `bdenckla/Taamey_D` at `40115a36`, and a rebuild from the
eight archived inputs reproduces the frozen font's layout tables (GDEF, GPOS, GSUB, OS/2, hmtx and
others) byte for byte. The five product `LICENSE.md` files repeat the MAM statement identically, and
the MAM-OSIS exception matches its historical readme. The Yeivin rights statements agree with each
other apart from finding 4.6.

**Redirects and topology (stream R).** phonetic-hbo `2ca51088`, deployed at 17:10:52 on 2026-10-01,
serves 1,959 stubs and a `404.html` byte-identical to what `py/redirect_stubs/stubs.py` renders at
`db59ef5e`; the frozen manifest lists exactly the 1,959 HTML pages phonetic-hbo published at
`8da90513`; all 991 targets exist; all 44,946 legacy anchors survive; and live requests redirect.
`stubs.py` dispatches closed and rejected all 21 malformed manifests fed it, and the 567 older stubs
and 11 catch-alls are unchanged. No caller of a removed `paths` helper remains, and no routine code
path or instruction in the tracked tree needs a phonetic-hbo clone.

**The meteg surveys (stream M).** The 793 changed lines of `out/accgram/post-stress-meteg.json` are
790 Hebrew values that differ only by the U+05C8 to U+05B0 and U+05C9 to U+05BC fold the public release
makes unnecessary, and three prose strings naming the new input; no count, record, MAM form or
classification changed, and the three post-stress-meteg pages changed only in five link targets,
which resolve. Both survey files regenerate byte for byte. Thirty hand-checked meteg-before-stress
cases agree with the classifier's stated algorithm, and an independent count of the target meteg
agrees on 6,119 of 6,119 cases; finding 2's accent class is the exception. The join handles the
annotations, the extraordinary points and perpetual qere correctly.

**The parser stage and the Wikisource tooling (stream V).** The tightened parser-stage checks raise
on every fault the September 29 round's findings 15 and 17 named; the new lock writer reproduces the
committed lock byte for byte; the narpas-first notice agrees across the 24 plus files, the guide and
the code; the unpinned-latest pages reproduce; the stack-path lookup works; and nothing live refers to
the retired plain or Google Sheet products.

**Repository tooling (stream T).** The fixes for the September 29 round's findings 7, 25, 26, 29 and
30 are correct as far as they go: every launch in the two forest modules is bounded and
noninteractive, the write form refuses a dirty, off-`main`, mid-operation, locked or occupied clone
before fetching, only the root `.novc/t` is exempt from the retirement gate, both configuration
READMEs say the check form fetches, and the 36 approved labels are listed. The cloud hook passes
`bash -n` and installs idempotently; the Codex hook decodes every encoding it was given.

**The UTF-8 sweep and small changes (stream U).** `33470e2d` reconfigures both streams first in all
eleven programs, and a census of 73 entry points finds none that prints non-ASCII to an unreconfigured
stdout; `855e9eeb`'s pool initializer is right under Windows spawn. Each generated page in scope
regenerates byte for byte: the Holman corrections page's introduction and 125 cards, `Deuter-5-long-notes.html`,
two MAM-with-doc misc pages and `gh-pages/index.html`. Every command line the "name no forest"
commits changed runs as written, and all 991 favicon links resolve.

**Instructions and skills (stream D1).** The window's instruction edits resolve the September 29
round's findings 2.5, 11, 12, 28.1 to 28.3, 29, 32, 33 and 34.1 to 34.3 and its item 36.2 consistently
across `AGENTS.md`, the common body, the Codex lifecycle, the skills and both configuration READMEs;
every path, function, heading and count in the changed hunks resolves at `db59ef5e`, apart from the
pointers in findings 10.3 and 10.4.

**Documents, READMEs and retired receipts (stream D2).** The nine retired documents survive at
`eea4c583` byte-identical to the last commits that held them, and every reference to them by filename
outside evidence files is covered by a dated update entry or an archive link; closed issues #274 and
#279 each got a dated correction comment. Across 59 documents, 395 links resolve. Every update file in
scope has a dated entry and the recorded State form, and every base with an update carries the
line-4 pointer. The dagesh discussion's capture is byte-identical to that section of Wikisource
revision 3086254, and the translation renders all ten comments, their speakers, times and reply
relations faithfully.

## Findings

Finding 1 is the most consequential: it will stop the next text refresh. Finding 2 is the one that
reaches published figures today. Findings 3 to 8 concern licences, instructions and published or
distributed text; 9 to 13 tooling, stale descriptions and checks; 14 is a question for Ben; 15
collects one-line items. Each lead says the finding's disposition at `db59ef5e`; nothing here was
fixed. Under `doc/periodic-review.md`, "Present remediation by public-facing risk": the public-facing
documents (rendered HTML and reader-facing Markdown) are in findings 2 (three Yeivin pages), 4
(`DATA-LICENSES.md`, `MAM-with-doc/LICENSE.md`, the root README), 5.1 (`Phonetic-MAM/README.md`), 6.1
(a Yeivin page), 11 (the pipeline diagram the root README offers) and 13.2 (the Phonetic MAM pages);
the public-facing data are in findings 2 (`Yeivin-ITM/meteg-claims.json` and
`out/accgram/meteg-before-stress.json`) and 5.2 (`Phonetic-MAM/data/` at two verses); everything else
is lower risk. No finding concerns MAM's own text.

### 1. A Wikisource refresh that changes MAM's text can no longer pass the gates the window built around the evacuated products, and no procedure says how to re-approve them

Unfixed at `db59ef5e`; both gates pass today only because MAM's text has not changed since
phonetic-hbo last rendered its pages. A refresh that changes a chapter's text changes `MAM-parsed/plus/`,
which the mega's `phonetic-mam-export` turns into a changed `Phonetic-MAM/` release
(`py/phonetic_mam/exporter.py:55–56` hands the private adapter MAM-basics' own MAM-parsed). Two pins
then fail by construction, and nothing regenerates either. Reach: the mega, the suite and the MAM
refresh workflow, and through them every product a refresh regenerates.

1. **The mega stops at `yeivin-itm-survey-meteg-claims`.** `py/yeivin_itm/claims.py:32–42` hashes the
   whole of `out/accgram/meteg-before-stress.json`, and `claim_schema.pin_claims`
   (`py/yeivin_itm/claim_schema.py:93–102`) raises "The independent meteg analysis has changed; review
   Ben's claims" unless that hash equals the hand-set `APPROVED_INPUT_SHA256`. The survey file embeds
   the SHA-256 of each of the 39 release files (`py/accgram/meteg_before_stress.py:345–356`), so any
   release change trips the pin even when none of the 20 approved fractions moves: stream Y zeroed one
   release hash in memory and got "all 20 fractions unchanged: True" and then the `ValueError`. The
   mega re-raises a step's exception (`py/main_0_mega.py:780–782`), so the run stops before
   `yeivin-itm-render`, `accgram-survey-post-stress-meteg`, `gen-site` and the three steps after it;
   stream Y found that resuming past the step would publish stale claims while two test modules fail.
   `Yeivin-ITM/README.md:75–78` states the gate's intent, "a changed corpus or population requires a
   fresh review", so the gate is deliberate; the defects are its trigger, the whole survey file rather
   than the twenty fractions it protects, and finding 1.3.
2. **The suite fails `test_complete_release_and_unified_projection`.** It compares every rendered
   chapter, in both pronunciations, with `in/phonetic_mam_legacy_projection_sha256.json`
   (`py/tests/test_phonetic_display_release.py:12–20`, `py/phonetic_mam/projection_check.py:115–142`):
   929 hashes per pronunciation that, in the module's own words, "come from the old public pages" of
   phonetic-hbo `8da90513`. Any change to a chapter's displayed text changes its hash; streams R and P2
   each changed one point or token in memory (Genesis 1, Ruth 1) and the hashes stopped matching. The
   file is read by this test alone and written by no code, and `d0c660c9` records that the legacy page
   families it was frozen from can no longer be produced.
3. **No procedure covers either.** The refresh procedure describes these steps as producing diffs to
   audit — the mega "exports `Phonetic-MAM/` ... then renders and analyzes the tracked public
   release", and "the Yeivin claims/rendering consume public data. Audit every diff and commit
   explained dependent changes" (`dot-claude/skills/mam-wikisource-refresh/references/dependent-refresh.md:33–34`,
   `:62–64`) — and requires the full suite before any push (`:86`). Neither it nor either product
   README says which constants a refresh must change, how the legacy hashes are to be replaced, or who
   approves. The data-level comparison the documents also require
   (`doc/phonetic-mam-preparation.md:20–22`, `Phonetic-MAM/README.md:12–14`) has no tracked runner:
   `py/phonetic_mam/legacy_projection.py` has no importer, and it can run only against a legacy
   phonetic-hbo tree (streams P1 and P2 ran it by hand: 39 of 39 books equal today).

The pins and the projection module arrived with `4b12bc41` and the merge `9a67d51b`; the refresh
procedure's sentences with `d0c660c9`.

### 2. The meteg-before-stress survey reads a one-chanted-word oleh-weyored as conjunctive, so 13 cases in poetic verses and 11 of the 20 approved Yeivin fractions are wrong, among them figures printed on three published pages

Unfixed at `db59ef5e`. `classify` sets `accent_class` by whether the accent on the stressed syllable
is in the conjunctive list (`py/accgram/meteg_before_stress.py:94`). In a poetic verse whose chanted
word carries both the oleh (U+05AB) and the yored of oleh-weyored, the accent on the stressed syllable
is the yored's U+05A5, and the poetic conjunctive list includes U+05A5 as merkha — with the list's own
comment, "MER, # but as yored (always in oleh-we-yored) is disjunctive"
(`py/mb_cmn/hebrew_accents.py:138–140`). accgram's poetic scanner reads the same chanted words as
`OLEH_WEYORED`, a disjunctive (stream M). `out/accgram/meteg-before-stress.json` records Psalms 120:1's
oleh-weyored chanted word, the second of the verse, as pattern FR3 with `"accent_class": "conj"`.

Stream M's differential against accgram's accent grammar found 13 such fully regular cases, all in
Psalms: 4:5, 37:40, 39:13, 50:3, 120:1, 121:1, 123:1, 125:1, 126:1, 128:1, 129:1, 132:1 and 134:1 (12
FR3, 1 FR1); none involves an oleh-weyored split over two chanted words. This session re-ran stream M's
recomputation (`M_ole_claims.py`), which re-reads those 13 as disjunctive and recomputes the claims;
it changes **11** of the 20 pinned fractions (stream M had reported 9): fully regular conjunctives with
the target meteg 221 to 210 of 3,583; disjunctives without it 132 to 134; exceptions 353 (9.9%) to
344 (9.6%); the five sub-fractions over 132 move to denominators of 134 (other meteg 31/132 to 33/134);
FR1 conjunctives with the target meteg 81/284 (28.5%, printed "about 29%") to 80/283 (28.3%); FR3
41/622 to 31/610; and the disjunctive exception rate 132/2184 to 134/2197.
`py/yeivin_itm/claim_schema.py:16–40` pins the current fractions, which are printed in
`gh-pages/yeivin-itm/yeivin_itm-318_344.html:539–553`, `yeivin_itm-huge-ftnt-320.html` and
`yeivin_itm-huge-ftnt-322.html`. The classifier entered with `9a67d51b`; the legacy page reported 222
such conjunctives, close to the new 221, so the private predecessor probably had the same rule, which
this public review cannot confirm. A fix changes the approved input hash and the pins (finding 1.1),
so the corrected prose is Ben's to approve. Reach: published pages and public data.

### 3. The live user-level configuration was not redeployed after the window's last two instruction commits, so every session on this machine loads a refresh skill that preflights, writes and pushes the retired phonetic-hbo clone

Unfixed when checked at 15:24 (stream D1) and again at about 15:50 (this session); a state of this
machine, not of a tracked file. The common body says to deploy after a canonical change is pushed,
and `d0c660c9`'s message says "Canonical deployment follows this normal main push." Nine live
destinations differ from their canonical sources at `db59ef5e`, exactly by the content of two pushed
commits, `4f4cbb66` (2026-10-01 15:38) and `d0c660c9` (2026-10-02 12:50):

1. `~/.codex/AGENTS.md`, which `~/.claude/CLAUDE.md` imports, is the body as it stood before
   `4f4cbb66`, without `dot-Codex/user-wide-AGENTS.md:184–185`, "When ending a session with work
   remaining, ... provide a standalone prompt for the next session." The fingerprint the Codex
   SessionStart hook compares against, `~/.codex/hooks/expected-user-wide-AGENTS.sha256`, names the same
   stale body, so that check stays silent.
2. In both `~/.claude/skills/` and `~/.agents/skills/`: `mam-wikisource-refresh/SKILL.md` and
   `references/dependent-refresh.md`, `mam-repository-topology/references/evacuated-repositories.md`, and
   `github-issues/references/mam-basics-trackers.md`.

The deployed `dependent-refresh.md` requires "the same forest's full MAM-private and phonetic-hbo
checkouts" (`:17`), has the agent audit phonetic-hbo's Pages output and commit it (`:62–65`), and pushes
"MAM-private, phonetic-hbo, MAM-basics" (`:130–132`); the canonical text says the refresh "never reads,
preflights, writes or restores" that clone, and that "A phonetic-hbo clone belongs on no machine". This
forest still holds a residue clone at `C:/Users/BenDe/GitRepos/phonetic-hbo`, at the pre-cutover
`8da90513`, and the deployed topology reference lacks the section that classifies it. An agent
refreshing MAM here today would preflight that clone and could commit to and push the live redirect
host. The documented remedy is the `--sync-user-config` deployment; this review deployed nothing.
Reach: agent instructions on this machine, and through them an outward-facing repository.

### 4. The licence statements do not match what the window published

All unfixed at `db59ef5e`. Facts and inconsistencies only; no legal conclusion is drawn. Reach:
licence documentation of the published site and the distributed products.

1. **`DATA-LICENSES.md:88` cites the font's "upstream license" at a path inside the private hbofonts
   repository.** The link is `https://github.com/bdenckla/hbofonts/blob/main/font-m-TaD/license.txt`;
   `in/repo_maintenance_policy.json:9–12` declares hbofonts private, and the same file's
   `repo_visibility` comment records Ben's decision of 2026-08-27 that a private repository's name may
   appear in public files but not "paths inside them, file names of theirs". An anonymous request for
   the link returned 404 (the row's pinned `bdenckla/Taamey_D` link returned 200). The
   licence is public twice already: `in/font-support/taamey-d-0.921/FONT-NOTICE.txt`, and
   `sources/font-m-TaD/license.txt` in the public `bdenckla/Taamey_D` at `38134991`, which stream F found
   equal to `FONT-NOTICE.txt` after blank-line normalization. Introduced by `066eb650`. It is the only
   link into the hbofonts repository's files; the links to `bdenckla.github.io/hbofonts/Taamey_D.html`
   go to its Pages site and resolve.
2. **The window states the font's GPL v2 duties for all fourteen copies but supplies the notice,
   licence text and source link beside two of the thirteen published ones.** `066eb650` rewrote
   `DATA-LICENSES.md:88` to cover `doc/woff2/Taamey_D.woff2` "and every `gh-pages/**/woff2/Taamey_D.woff2`
   (fourteen tracked, byte-identical copies ...)" and to say "Redistribution must preserve the copyright
   and license notices, provide the GPL v2 text, and satisfy its corresponding-source requirements."
   Only `gh-pages/phonetic-mam/woff2/` and `gh-pages/yeivin-itm/woff2/` hold `FONT-NOTICE.txt`,
   `GPL-2.0.txt` and `SOURCE.txt`, and only those two products' landing pages link the notice. The
   eleven other published directories — `MAM-parsed`, `MAM-simple`, `MAM-with-doc` with its `change-log`,
   `foi` and `misc`, `book-of-job` with its `jobn`, `holman`, `uxlc` and `wlc` — hold the font alone, and no
   page that loads them links the same-host package under `gh-pages/font-sources/taamey-d-0.921/`. The
   copies are older than the window; the window's own implementation, `py/py_html/taamey_d_assets.py:29–30`,
   refuses every product but the two new ones. The font binary carries its notice and grant in
   OpenType name ID 0 (stream F).
3. **The two new distributed products have no `LICENSE.md`, and `DATA-LICENSES.md` assigns no terms to
   some of their files.** Each of the five older products holds a `LICENSE.md` repeating the MAM
   statement, and `DATA-LICENSES.md:144–150` describes those five. `Phonetic-MAM/` and `Yeivin-ITM/` have
   README prose only, and `Phonetic-MAM/README.md`, "Attribution and terms", gives the English
   attribution but not the statement's Hebrew-language rule. The path table has no row for either
   README or `schema/` directory, nor for the six notice files in the two product `woff2/` directories,
   which rows 51 and 56 exclude and row 88, covering only `.woff2` files, does not reach. Adding a
   `LICENSE.md` to `Phonetic-MAM/` also needs `py/phonetic_mam/release.py:validate_complete_release`
   (`:57–69`) and `py/tests/test_phonetic_display_release.py:58–66` changed, whose closed file sets would
   reject it. Arrived with `9a67d51b`.
4. **`MAM-with-doc/LICENSE.md`'s new preface extends the CC-BY-SA statement over a tree that also holds
   third-party crops and GPL font copies.** `aef596c7` wrote "This statement applies equally to the
   MAM-with-doc edition, which MAM-basics publishes from `gh-pages/MAM-with-doc/`" (`:3–4`). That tree
   also holds the crops of `gh-pages/MAM-with-doc/misc/img/`, which `DATA-LICENSES.md:97` keeps as "each
   rights holder's; no grant is made or implied here", and four Taamey D copies, which `:96` excepts;
   `MAM-OSIS/LICENSE.md`'s preface, by contrast, states its exception. Ben approved the edition sentence
   on 2026-09-30 (`doc/PLAN-remediate-review-findings-2026-09-29.md:540–550`, evidence); that text did not
   consider these two exceptions.
5. **The GPL exclusion of `py/yeivin_itm/content/` also covers helper code the GPL renderer imports.**
   `DATA-LICENSES.md:6–7` and `:58` and the root README exclude that subtree as the adaptation and its
   remarks, and `Yeivin-ITM/README.md:5–6` says "the renderer and its helpers are under `py/yeivin_itm/`".
   But six modules there hold rendering code and no Yeivin or Revell prose (637 lines, among them
   `my_yeivin_amisc_traverse.py` and `my_yeivin_amisc_tocsec_metadata.py`), and the GPL-3.0
   `py/yeivin_itm/renderer.py:8–9` and `helpers.py` import five of them, so part of what the renderer needs
   carries no stated code licence (streams F and Y). Which modules count as adaptation is Ben's call.
   Arrived with `a0016209`.
6. **`DATA-LICENSES.md:58` puts a passage from Yeivin's separate 1968 study under the permission
   granted for the 1980 book.** The row places all of `py/yeivin_itm/content/`, "including the separately
   identified small comment passage", under the publication permission, whose stated object is the
   1980 *Introduction to the Tiberian Masorah*; `Yeivin-ITM/README.md:37–40` says that passage,
   `py/yeivin_itm/content/my_yeivin_sec_320.py:90–147`, comes from "Yeivin's separate 1968 Hebrew study",
   "is not an edition of ITM", and that "Ben accepted" it. The repository records no permission or rights
   holder for the 1968 work. Introduced by `a0016209`.
7. **The README and `DATA-LICENSES.md` claim GPL-3.0 over a CC BY-SA 4.0 capture and its translation.**
   `README.md:114–117` and `DATA-LICENSES.md:5–11` place everything under `doc/` under GPL-3.0 except the
   font and the snips crops. `7577b56d` added `doc/wikisource-dagesh-discussion-2026-10-01.mediawiki`, a
   verbatim section of a Hebrew Wikisource talk page by four Wikisource users, and its translation, which
   declares itself CC BY-SA 4.0 (`doc/wikisource-dagesh-discussion-translation.md:27–29`); neither has a
   row in the path table (stream D2).
8. **The root README's product list omits Phonetic-MAM and Yeivin-ITM.** "Product and corpus
   directories" (`README.md:21–36`) lists the five older products; the two new ones and their entry
   points `py/main_phonetic_mam.py` and `py/main_yeivin_itm.py` appear in none of its lists, though the
   window edited the same README's licence section for Yeivin. `gh-pages/index.html` links both.

### 5. The Phonetic MAM release is not MAM's written text, and its README does not say how

Unfixed at `db59ef5e`. Reach: a distributed product and its published pages.

1. **The README calls the content "generic MAM Hebrew"** (`Phonetic-MAM/README.md:3–5`) and says nothing
   about how it departs from MAM's spelling, which a consumer joining it to MAM must know. The display
   has only the qere at 7,706 MAM chanted words — Genesis 2:4, for instance, displays the perpetual
   qere where MAM-simple has the Tetragrammaton — and the old input's written-form field has no
   counterpart (stream M). It has no extraordinary point: `MAM-simple/json-vtrad-mam/` holds 53 U+05C4
   and 4 U+05C5 and the release none (`puncta_counts.py`), as
   `py/py_html/forbidden_phonetic_marks.py:1–6` and `display_schema` intend. It uses the second parameter
   of the stress-helper templates where MAM-simple uses the first, keeps varika, and writes Latin vowel
   marks decomposed (finding 14). The explanation of the join rules lived in the docstring of
   `paths.al_hatorah_phonetic_dir`, which `9a67d51b` deleted; of its three facts only the annotation
   fold survives, in `py/author_site/post_stress_meteg_annotations.py`'s docstring, and the handling of
   extraordinary points is explained nowhere. The joins themselves handle all of it correctly (stream
   M).
2. **New evidence on the September 29 round's deferred finding 22, and a second, undisclosed text
   difference.** Ben deferred finding 22, the missing 2 Kings 22:1 qamats variant, "for that evidence
   gap", and its record was retargeted on 2026-10-02: "The next dependent refresh checks
   `Phonetic-MAM/data/BD-2Kings.json`, the corresponding public page ... and the post-stress-meteg
   survey" (`doc/dual-agent-review-2026-09-29-turn-01-claude-update.md:1769–1780`, evidence). Stream P1
   compared every verse of the release with MAM-simple: 23,200 of 23,202 agree; the release shows
   qamats alternatives at 356 of the 357 verses where MAM has a qamats template, nested ones included,
   and the one without is 2 Kings 22:1, where it has only the U+05B8 reading that `97c4aff5` (2026-09-27)
   turned into an alternative. This session's mega re-exported the release from the current MAM-parsed
   and left it byte-identical, so the current exporter reproduces the omission, and the next refresh
   will not bring the variant in; why the private adapter drops this one nested template is not visible
   in public code. The other difference is 2 Chronicles 25:17, where the displayed atom is the ketiv's
   final kaf with the qere's points (U+05DC U+05B0 U+05DA U+05B8 U+0596) against MAM's ketiv (U+05DC
   U+05DA) and qere (U+05DC U+05B0 U+05DB U+05B8 U+0596 U+05D4). That one is known — the docstring of
   `py/tests/test_final_stress_vs_phonetic_mam.py:21–24` records it — but neither the README nor the
   schema does. Both differences are in phonetic-hbo `8da90513`'s pages, which the release equals, and the
   frozen oracle of finding 1.2 encodes them too.

### 6. A published Yeivin page cites a verse that does not exist, and the tests leave no way to correct it

Unfixed at `db59ef5e`.

1. **"2K 52:1".** `gh-pages/yeivin-itm/yeivin_itm-207_285.html:39` and `:82` cite it for an example form,
   as the tooltip and in the page's list of biblical references; 2 Kings has 25 chapters. The source is
   `py/yeivin_itm/content/my_yeivin_sec_239.py:8`. MAM has the form at Isaiah 52:1, among 25 places, and
   the paragraph's other examples are from Isaiah, so Isaiah 52:1 is the likely intent; Yeivin's printed
   text, in private OCR, was not read. Of the 807 distinct references on the 17 pages it is the only one
   that names no existing verse (stream Y, against MAM-for-Sefaria). It is older than the window:
   phonetic-hbo `8da90513`'s page has it twice, and the evacuation carried it forward.
   `py/yeivin_itm/content/my_yeivin_amisc_helpers_for_locales.py:27–40` parses a reference without
   range-checking it. Reach: a published page.
2. **The "editable adaptation" has no editing procedure, and its tests forbid this correction.**
   `Yeivin-ITM/README.md:3` and `DATA-LICENSES.md:58` call `py/yeivin_itm/content/` an editable
   adaptation, but nothing documents how to edit it, and `py/tests/test_yeivin_itm.py` freezes it against
   the legacy pages: 112 of its 114 modules are hash-pinned to hand-maintained values in
   `in/yeivin_itm_legacy_differential.json`, every changed rendered line must be recorded there by hand,
   the set of changed pages is hard-coded, and every Hebrew example's attributes and text must equal the
   legacy page's (`:77–83`), with no way to record an approved difference. Stream Y applied the
   correction to Isaiah 52:1 in memory and recorded it as the differential expects; the example
   comparison still failed. Introduced by `a0016209` and `9a67d51b`. Reach: tests and agent
   instructions.

### 7. The bot's setup guide gives `--no-save`'s behaviour to `--identity-run`, so a dry run done by the guide tests no edit before a live Wikisource save

Unfixed at `db59ef5e`; older than the window. `py/ws/pywikibot-setup.md:72–77`: "For
process/idempotence checks, use `--identity-run` ... It processes chapters and fails at the end if any
chapter text would change." In the code `--identity-run` is a null bot: it loads no edits
(`py/subcommands/ws_bot_real.py:52–59`, `wbe.no_edits()`, "null bot: no processing and no saves") and
gives each page back its own text (`:102–103`), so it cannot fail on a change. The mode that applies
the edits without saving and fails if any chapter would change is `--no-save` (`:106–115`, `:85`), which
the guide never names. The refresh skill sends "Preparing, dry-running, and saving Wikisource bot
edits" to this guide (`dot-claude/skills/mam-wikisource-refresh/SKILL.md:128–129`). The sentence dates
from `d4994a42`, when `--identity-run` still processed edits; `5ea68e33` split the modes the same day
without updating it, and the window rewrote the neighbouring section (`8fd5b6e6`, `d0c660c9`) and left
this one (stream V). Reach: instructions for an outward-facing act on Hebrew Wikisource.

### 8. The dependent refresh's step 4 regenerates the change logs step 5 exists to produce, so step 5's stop rule, read as written, halts a correct refresh

Unfixed at `db59ef5e`; older than the window, carried forward by `d0c660c9`'s rewrite. Step 4 of
`dot-claude/skills/mam-wikisource-refresh/references/dependent-refresh.md` (`:55–65`) runs the mega
and says "Audit every diff and commit explained dependent changes"; step 5 (`:67–82`) runs
`py/main_diff.py mpplus --all` and says "If book data changed but no change-log diff results, stop and
resolve the discrepancy." The mega's `diff-mpplus` step (`py/main_0_mega.py:283–287`) rewrites
`unpinned-latest.html`, `unpinned-latest.json` and `index.html` from committed `HEAD`
(`py/subcommands/diff_mpplus.py:281–331`), so after step 1's commit, step 4's mega writes the change-log
diff; committed there, as step 4 says, it leaves step 5 nothing to change, and the stop rule fires.
`SKILL.md:10–13` says change logs are committed only after the loop returns, but neither file tells
step 4 to hold those paths back. The window shows the mechanism in small: `f62428c4`'s header-only
plus commit left the unpinned-latest pages stale until `94535122` regenerated them. Written by
`e91e5e12` (stream V). Reach: the shared skill every Wikisource refresh and saving bot run follows.

### 9. Repository tooling

All unfixed at `db59ef5e`. Reach: internal tooling.

1. **Routine maintenance stops at its first step on Windows after any suite run.**
   `py/main_repo_maintenance.py:135–145` wipes `.novc` with a plain `shutil.rmtree` (`:140`), and `main()`
   calls it first and unguarded (`:218–219`). On Windows the suite's pytest base directory lives under
   `.novc/t`, and the relay's two test modules, added to the default suite by `1a50d4b6`, make Git
   repositories there whose object files Git writes read-only, which `shutil.rmtree` cannot delete on
   Windows. After this session's suite run the clone held 6,478 files under `.novc/t`, 1,199 of them
   read-only, every one under a relay test (`readonly_census.py`). Stream T ran the production
   `_clean_one_novc` on a copy of one such directory: `PermissionError [WinError 5]`, with 163 of 179
   files left. The run then never reaches worktree inspection, the user-configuration check, Black, ruff,
   the suite or the mega, against the docstring's "Seven independent steps". The relay tests are
   evidence here, but the failing step is subject; the wipe is older than the window (`7e8ee0f2`), and
   the window made the condition routine.
2. **Ruff reports 17 errors, so maintenance's lint step reports FAILED.** `py/main_repo_maintenance.py:186–190`
   runs `ruff check py`. The errors: eleven E402 in `py/phonetic_mam/compute.py:14–24`, where
   `sys.dont_write_bytecode = True` deliberately precedes the imports but carries no `noqa`; F401 at
   `py/phonetic_mam/core/resolve_generic.py:3`, `py/tests/test_phonetic_compute_boundary.py:4`,
   `py/yeivin_itm/content/my_yeivin_sec_318.py:2` and `my_yeivin_sec_388.py:3`; F541 at
   `py/yeivin_itm/content/my_yeivin_amisc_helpers_private.py:212`; and F841 at
   `py/tests/test_dual_agent_review_dispatch.py:805`, an evidence file. The sixteen in subject files
   arrived with `a0016209` and `9a67d51b`; the start commit's two errors are gone (`8742d96a`).
3. **The synchronize form of `--sync-forest` run by an agent on its own forest always refuses that
   agent's clone and exits 1, and nothing documents the case.** `runtime_facts`
   (`py/repo_util/worktree_owners.py:74–82`) counts the calling session's own record as occupancy, the
   write form raises on it before fetching (`py/repo_util/forest_sync.py:250–261`), and every refusal
   counts as a problem (`:322–332`). This session's run printed "running Claude session ...; not fetched;
   checkout and environments left untouched" and `FOREST_PROBLEM_COUNT: 1`. `doc/clone-forests.md`'s
   examples sync another forest, while `doc/PLAN-checkout-kinds-and-portable-knowledge.md:318–319` calls
   `--sync-forest $HOME/GitRepos` the "sync GitRepos" operation, which an agent naturally runs from that
   forest's MAM-basics; from an agent session it can never exit 0 (stream T). Older than the window;
   `3a1b9a7c` moved the refusal before the fetch and kept the counting.
4. **The new forest launch lint checks that a bound keyword is present, not that it bounds, and misses
   forms its docstring claims.** `py/tests/test_forest_subprocess_bounds.py:91–92` tests keyword presence
   only, so `timeout=None` passes, and `_imported_names` (`:56–58`) ignores a relative import's level, so
   `from .user_config_sync import _run_git` escapes, against the docstring's claim (`:19–22`) that a
   launcher is recognized "whether it is called by a name that `from ... import` binds"; stream T also
   found launches through unlisted modules, `asyncio`, `os.posix_spawn`, `os.startfile` and
   `functools.partial` unflagged in synthetic sources. Today's modules are bounded. From `3a1b9a7c` and
   `9588700f`.
5. **Cross-volume `.novc` relocation removes its source with the same plain `shutil.rmtree`.**
   `py/repo_util/worktree_retirement_relocation.py:121–132` copies, verifies and then removes; on a
   Windows worktree whose `.novc/t` holds the read-only objects of 9.1, which `b158db02` no longer lets
   gate the retirement, removal stops partway, leaving a verified copy, a partly deleted source and a
   retirement stuck for manual repair. The default same-volume path renames and is unaffected. Older
   than the window and more readily reached since `b158db02`; the mechanism is confirmed by stream T's
   execution, the end-to-end run is not.

### 10. Descriptions the window made false

All unfixed at `db59ef5e`.

1. **Help text and comments say the post-stress-meteg survey needs MAM-private and is skipped in the
   cloud.** Since the evacuation the survey reads the tracked `Phonetic-MAM/` release and runs in a cloud
   session: `AGENTS.md:191–193`, `hebrew-prose/references/verifying.md:49–52` and the mega's step note
   (`py/main_0_mega.py:636–642`) say so. But `py/main_accgram.py:49–52` and its `--help` (`:421`) say "Needs
   the MAM-private clone" and that the mega runs it "except in a cloud session";
   `py/main_authored.py:15–18`, `:135–142` and its `--help` (`:243–245`), `py/author_site/post_stress_meteg.py:204–206`
   and `py/mb_cmn/graphviz_pin.py:57–60` say the same; `py/main_0_mega.py:603–610`, written for this
   survey, says "a cloud run skips the survey altogether, which its runner does" and now sits above
   `phonetic-mam-export`; and `py/tests/test_redirect_manifest.py:38–39` cites the final-stress module as
   the one that skips its MAM-private tests in a container, which it no longer does. Older sentences
   that `9a67d51b` made false (streams D1, P1 and V). Reach: `--help` and comments an agent reads before
   running a command.
2. **`doc/phonetic-mam-preparation.md` says the site's deployment and the legacy redirect cutover are
   still to come.** Line 8: "Site deployment and live URL verification remain separate publication
   steps"; line 79: "target deployment and the coordinated legacy redirect cutover remain separate
   steps". Both were written by `85f29edb` at 14:40 on 2026-10-01; the Pages run for `38c0116f`, which
   holds the evacuation, finished at 15:39:45 that day, and phonetic-hbo `2ca51088` converted the old
   host at 17:09:51 and deployed at 17:10:52 (stream R). `d0c660c9` updated the other close-out documents
   but not this one.
3. **`hebrew-prose` still sends readers to a private Yeivin copy the repository records as removed.**
   `dot-claude/skills/hebrew-prose/references/sources-and-corpora.md:68–73` says "the old
   `MAM-private/al-hatorah/py/itm/` copy remains until the later retirement gates pass", while
   `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md:387–392`, written by `d0c660c9`,
   records that private integration `5c526cac` "removed the duplicate adaptation after the consumer gates
   passed". `references/mam-basics.md:30–37`'s eighth site went stale when `9a67d51b` rewrote
   `py/accgram/post_stress_meteg.py`'s docstring.
4. **`py/product_scopes.py`, which `AGENTS.md` names the declaration of record, lists five distributed
   products in its docstring (`:17–26`) and seven in `_PRODUCT_DIR_NAMES`**; `py/tests/test_product_scopes.py`'s
   docstring says "the five product directories". From `9a67d51b`.

### 11. The pipeline graph misstates which programs the mega runs, draws none of the five new steps, and nothing checks it

Unfixed at `db59ef5e`; older than the window, which widened it. `doc/process-documentation/pipeline.svg`,
which the root README offers as a diagram of the pipeline, draws 12 of the mega's 57 steps and none
of the five the window added, and under "Pipeline steps" draws four programs the mega does not run:
`py/main_mam4sef.py` and `py/main_mam_osis.py` (out of the mega since 2026-09-12), `ws_bot real` (in
`NOT_IN_MEGA`) and `osis_split_mapm`, whose program `85c6c354` deleted on 2026-03-10. It draws the bot's
post-run reparse into `MAM-parsed/plus/` and `out/` (`dd4f85df`, in the window) but not the same reparse
that every `fr-wikisource` download runs (`py/subcommands/download_wikisource.py:62`), so a reader
concludes that a download leaves `plus/` alone, against the skill. No test compares
`py/pipeline_graph/pipeline_graph_spec.py` with the step table, and `py/tests/test_mega_coverage.py:246–251`
cites the graph as its record for `fr-wikisource`. `doc/mega-coverage-2026-09-10.md:288–292` raised the
drift, and the September 29 round noticed the deleted program (stream V). Reach: reader-facing
documentation and a lint's record.

### 12. Checks that check less than they claim

All unfixed at `db59ef5e`. Reach: tests and internal validation.

1. **The remediated pre-write check that plus "holds no parser-stage encoding" still recognizes only
   the `stmpl` form.** `41d73299` fixed the September 29 round's finding 15 by making the check walk
   tuples (`py/verify_mp/parser_stage.py:332–339`), but its test is still `"stmpl" not in node`; the
   parser stage also writes `{"tmpl": [...]}` and keeps custom tags (`py/mb_cmn/ws_tmpl1.py:54–56`,
   `:108–119`). Stream V injected a `tmpl` node into a cell, the same node inside a template parameter,
   and a custom tag into an in-memory copy of Genesis plus: all three passed `validate_plus_conversion`.
   The claims verification catches a top-level one after the write, and only the later `tmpl-survey`
   step a nested one. The test is older (`146f6145`); the remediation plan's acceptance check injected
   only `stmpl` (`doc/PLAN-remediate-review-findings-2026-09-29.md:773–779`).
2. **`test_meteg_before_stress` has no independent oracle.** The module docstring says the classifier
   "preserves the existing algorithm's syllable grouping, vowel-length convention, structural table,
   accent buckets, and case selection" (`py/accgram/meteg_before_stress.py:3–6`), but no tracked record
   holds that one-time comparison, and the tests check only regeneration against the committed output,
   field shape, and the claims' reproduction — which is why finding 2 went unseen. Stream M's two
   independent checks, an accent-class differential against accgram's grammar and a nucleus count for
   the target meteg (6,119 of 6,119), were cheap. Against the legacy pages, AFR4 disjunctives moved from
   63/105 to 72/129, and all 109 AFR4 "J" cases depend on reading a varika-marked shewa as hataf
   (`:274`); whether the predecessor did so cannot be settled from public evidence. From `9a67d51b`.
3. **Two new untangler tests are not of the shapes the repository allows.**
   `test_preparation_rejects_unclassified_template_shapes`
   (`py/tests/test_phonetic_untangler_preparation.py:64–79`) is an example-based fault-injection test that
   `AGENTS.md`, "Writing tests", does not declare among its exceptions;
   `test_preparation_operation_matches_direct_core_without_file_access` (`:43–61`) compares
   `compute.execute` with `dualcant_prepare.prepare`, which is exactly what `compute._prepare_untanglers`
   returns (`py/phonetic_mam/compute.py:152–154`), so its equality half cannot fail (stream P1). From
   `9a67d51b`.
4. **`_written_stress_helpers` is not a closed template dispatch.** `py/accgram/post_stress_meteg_sources.py:116–143`
   silently skips every element that is not one of the two stress-helper templates, unknown templates
   included, against the rule that template dispatch is closed, and never indexes the 68 nested stress
   helpers. So `snapshot_before_qere` now exists only for top-level stress-helper chanted words, where the
   old input's written form covered every perpetual-qere site. All 378 current records are unchanged;
   the effect is latent (stream M). From `9a67d51b`.

### 13. Smaller code defects

Both unfixed at `db59ef5e`.

1. **The compute interface ends its stream on an undecodable byte and drops replies already owed.**
   `f170616d` made `py/main_phonetic_mam.py:58` reconfigure stdin to strict UTF-8, and `compute.serve`
   reads in its `while` condition, outside its `try` (`py/phonetic_mam/compute.py:299–320`), so an invalid
   byte raises out of the loop and the process exits 1, and a valid request decoded in the same buffered
   chunk gets no reply. `doc/phonetic-mam-compute.md` promises "Each input line receives one output line"
   and "A rejected ordinary line does not end the stream", naming only an oversized request and a broken
   pipe as ending it. Stream P1 confirmed it with UTF-8 mode off; the failure is loud. Reach: the private
   consumers of the interface.
2. **The Ashkenazic display depends on the CSS `:has()` selector alone.** `py/phonetic_mam/assets/style.css:37–41`,
   published as `gh-pages/phonetic-mam/style.css`, switches the transcriptions only through
   `body:has(#pronunciation-ashkenazic:checked)`, and `pronunciation.js` sets the radio, the URL and the
   links but no class. In a browser without `:has()` (Firefox before 121, Safari before 15.4), choosing
   Ashkenazic, or arriving at `?pronunciation=ashkenazic`, as redirected legacy Ashkenazic URLs now do,
   shows the Sephardic transcriptions under an Ashkenazic label; the recorded acceptance was in Edge
   (`doc/phonetic-mam-preparation.md:48`). From `4b12bc41`. Reach: the 929 published chapter pages; low.

### 14. A question for Ben: the new product ships decomposed Latin vowel marks under an exemption the window wrote

Unfixed at `db59ef5e`; not called a defect here, because the choice is Ben's. The common body says his
repositories "use NFC for Latin letters with diacritics". `py/phonetic_mam/display_projection.py:19–31`
writes the transcriptions' acute and breve vowels as a base letter plus U+0301 or U+0306 while writing
ḥ precomposed: 385,991 and 73,384 such marks (stream P1) in all 39 `Phonetic-MAM/data/` files,
`examples/display.json` and the published pages. `9a67d51b` exempted the data from
`py/tests/test_h_dot_below_nfc.py:191–195`, citing "the existing public transcription exactly"; stream W
found no recorded decision of Ben's for it, and `py/phonetic_mam/analysis_reader.py` now depends on the
decomposed form. The forms are older, in phonetic-hbo's pages; the window made them a distributed
product. The question is whether the release keeps the legacy bytes, as the exemption says, or is
composed to NFC, which would change the published pages, the frozen oracle of finding 1.2 and the
reader.

### 15. One-line items

All unfixed at `db59ef5e` unless stated.

1. `doc/periodic-review.md:32–33` and `:286–299` still make the per-finding sub-agent check mandatory before a review is committed, while its own `:15–17` and `doc/dual-agent-review.md`'s trial text say the owner's verification replaces it; the post-window `742aaf41` settled only `doc/dual-agent-review.md` (stream D2).
2. `doc/user-wide-instruction-conversion-reconciliation.md:90` cites "The symmetric-instructions plan's update", which `e4934b6e` retired, without an archive link; the retirement's audit searched by filename (stream D2).
3. `py/main_diff.py` reconfigures neither standard stream and `py/main_sigil_inventory.py:9` only stdout; neither can crash, and both are older than the window (stream U).
4. `reconfigure(encoding="utf-8")` resets stderr's error handler from `backslashreplace` to `strict` in the eleven programs of `33470e2d` (stream U).
5. `py/main_github_issue_edit.py:3–4`, rewritten by `d54e12df`, still says every path is resolved from the file, but `--edits` is relative to the working directory (stream U).
6. `py/tests/test_final_stress_vs_phonetic_mam.py:15–24` says Phonetic MAM keeps two chanted words at 113 gray-maqaf places; the release has 113 tilde-joined readings, and the prose non-joins are 12, not 11, 2 Kings 22:1 being new (stream M; older, carried forward by `9a67d51b`).
7. `Phonetic-MAM/README.md:21` says `render` "reads only this public product"; it also reads `in/phonetic-mam-images/`, `in/font-support/`, `doc/woff2/` and its assets, and writes `gh-pages/font-sources/` (stream P2).
8. The Phonetic MAM index's English attribution links the he.wikisource page, not the en.wikisource page the MAM statement prescribes; inherited from phonetic-hbo (streams P2 and F).
9. `DATA-LICENSES.md:57` still calls the font-support README's mapping "the required future same-host publication mapping", which `9a67d51b` published (stream F).
10. `DATA-LICENSES.md:51` says the Yeivin permission notice "remains on the pages"; it is on 11 of the 17 (streams F and Y).
11. `py/py_html/taamey_d_assets.py:34–40` hash-checks only the font and the archive, the other support files only for being non-empty (stream F).
12. `.gitattributes` does not mark the two new source zips binary; Git's content detection treats them as binary today (stream F).
13. `doc/mam-normal-mark-order.md` does not list `doc/wikisource-dagesh-discussion-2026-10-01.mediawiki` among the faithful captures, though its 5 clusters are the window's only ones out of MAM-normal order (stream W).
14. `Yeivin-ITM/schema/meteg-claims-v1.schema.json:3`'s `$id` names a URL that Pages does not serve, `Yeivin-ITM/` being outside `gh-pages/` (streams Y and W).
15. The Yeivin claim data names strands in romanized letters ("alef strand", "bet cantillation strand"), where `hebrew-prose` keeps strand names in Hebrew letters in reader-facing prose (stream W).
16. `Yeivin-ITM/README.md:88–89`, "not a claim that Pages has been deployed", is stale, and `in/yeivin_itm_legacy_differential.json:5`'s description omits the favicon line's removal (stream Y).
17. `py/main_0_mega.py:634` says `yeivin-itm-render` "writes all 17 public Yeivin pages"; it also writes `style.css`, four `woff2/` files and the shared `font-sources/` package (stream Y).
18. `py/main_phonetic_mam.py:18`, `py/main_yeivin_itm.py:16` and `py/phonetic_mam/compute.py:12` set `sys.dont_write_bytecode` at import, so a mega or pytest process that imports them stops caching bytecode for every later import (streams V and P1).
19. `py/phonetic_mam/exporter.py:85–120` discards the adapter's stderr and waits without a timeout, so a failure reports only "source adapter failed" (stream P1).
20. `py/phonetic_mam/test_page_display.py` is a production module whose name matches pytest's `test_*.py` pattern (stream P2).
21. `py/tests/test_sibling_reach.py:212`'s comment says `paths.py` calls `sibling_repo("MAM-private")`; the reach is now `py/phonetic_mam/exporter.py:34–35` (stream R).
22. `py/mb_cmn/paths.py:215`'s `display_path` example gives `Phonetic-MAM/data`; the function returns `MAM-basics/Phonetic-MAM/data` (stream R).
23. `AGENTS.md:249–250` says `doc/agent-planning-principles.md`, "Generated Outputs Are the Tests", carries the dated evidence for the test exceptions; it records neither exception (stream D1).
24. `evacuated-repositories.md`'s `<forest>/...` clone commands, in `powershell` fences, do not parse as written, and the new phonetic-hbo block spells the location `../phonetic-hbo` (streams D1 and R).
25. `mam-basics-trackers.md`'s "Five issue trackers" framing now sits beside a section routing two more trackers (stream R).
26. `doc/clone-forests.md:20–22` omits "behind `origin/main`" from the check form's failure conditions (stream T).
27. `py/repo_util/run_black.py:31–33` keeps an orphan comment line after `37002a28`'s rewording (stream T).
28. The retirement force-flag lint passes abbreviated long options such as `--forc` and `--del`, which Git accepts; not a regression (stream T).
29. `cb5bcda1` edited two dated Holman research records in place, which the terminology reference classifies as receipts, and `d0c660c9`'s 2026-10-02 update entry has no "Recorded by" line (stream D2).
30. The dagesh translation's introduction credits the correction to Dovi alone, though Mo Yu Hu made it first (stream D2).
31. Comments in the Yeivin adaptation link issues of the private `bdenckla/trope` tracker, which public readers cannot open (stream W).

## Noticed outside the diff, not findings

1. `forest_sync._git`'s 60-second bound also covers `git merge --ff-only`, which an expired timeout
   kills mid-checkout, leaving `index.lock`; a fast-forward across this whole window writes 1,523 files,
   far inside the bound (stream T; plausible).
2. `gh-pages/MAM-OSIS/two_col_style.css:22` points at a `woff2/Taamey_D.woff2` that does not exist, and
   `gh-pages/MAM-parsed/woff2/Taamey_D.woff2` is published but referenced by no stylesheet (stream F).
3. `py/tests/test_stack_path_lookup.py:41` still patches `_dataset_file_paths`, so the crash `8742d96a`
   fixed would pass the suite again (stream V).
4. `py/ws/pywikibot-setup.md:13` and `:23` use `cp`, a bare `~` and a POSIX environment form, and the
   "Wikisource bot" launch configuration it cites passes no `--edits` (stream V).
5. `doc/scan-pages.md` is a plan with no State line (stream D2).
6. The evacuated pages carry legacy HTML faults byte for byte: a `blockquote` and a `ul` inside a `p`,
   139 obsolete `align` attributes on two Yeivin pages, and five stray `</img>` tags and five images
   without `alt` on one Phonetic example page (streams Y and P2).

## Open ends the window itself declares (not findings)

1. **1 Kings 7:37's silluq before a later meteg.** `doc/PLAN-silluq-before-gaya-template.md` (live,
   under phonetic-hbo#78) records that MAM's verse-final atom there has two U+05BD, the first the silluq
   and the second a meteg. The evacuated core still takes the last U+05BD before sof pasuq as the silluq
   (`py/phonetic_mam/core/separate_accents.py:42–80`), and its comment says the only exception it knows
   is one MAM does not follow, so the published chapter page and the release stress that atom's later
   syllable until the plan lands (stream W).
2. **The font's exact rebuild.** `in/font-support/taamey-d-0.921/BUILD.txt` and
   `doc/phonetic-mam-preparation.md:62–63` say an exact rebuild has not been established; stream F's rebuild
   reproduced every layout table but not the `glyf` bytes (21 of 278 glyphs differ in quadratic-conversion
   points) or the build metadata.
3. **The private adapter remains a migration dependency** for the example pages' calculation
   (`doc/phonetic-mam-preparation.md:26–31`).
4. **The September 29 round's finding 22 stays deferred**, with the new evidence of finding 5.2.
5. **`doc/PLAN-mega-speedup.md`'s items 13 to 15 are superseded**, and a later optimization must measure
   the new reader first.
6. **The residue phonetic-hbo clone** in this forest is at the pre-cutover `8da90513`, where
   `evacuated-repositories.md` says a phonetic-hbo clone belongs on no machine; run here,
   `py/main_redirect_stubs.py check --repo phonetic-hbo` without `--dir` lints the legacy pages and reports
   9,796 problems (stream R). Retiring it is Ben's decision.
7. **The relay software**, evidence here, which Ben hopes to discard.

## What this review did not check

1. Anything in MAM-private or hbofonts: the private source adapter that `phonetic-mam-export` runs,
   whether the predecessor of the meteg-before-stress classifier shared finding 2's rule or the varika
   rule of finding 12.2, and Yeivin's printed text (private OCR) for the intent of finding 6.1.
2. The relay software and the earlier rounds' records, as subject; the Codex review.
3. Real-browser rendering, apart from stream R's two page visits: in particular finding 13.2 in a
   browser without `:has()`, and full HTML5 conformance (no validator; `--w3c` posts pages to an
   external service and was not used).
4. A Linux or cloud run of the suite, the mega or the hooks.
5. The hand-run generators, which the window gave nothing to rerun for (tree health), and the live
   deployment beyond stream W's six sampled files.

## Notes on the trial procedure from the reviewer's side

Offered because Ben's kickoff instruction asked this review to flesh the process out; none is a
finding about the window.

1. **The reviewer's session started in the owner's clone.** The kickoff prompt's guard caught it, and
   Ben moved the session with the desktop app's change-directory tool before any work. A kickoff prompt
   could tell Ben which folder to start each reviewer's session in, and say that a session started
   elsewhere may offer to move itself.
2. **The prompt's sibling synchronization cannot exit 0 for a reviewer in its own forest** (finding 9.3).
   The check form is the useful one; the synchronize form's refusal of the reviewer's own clone is
   expected.
3. **Run the suite and the mega before fanning out.** With twelve streams beside it the suite took 25½
   minutes against the September 29 round's 145 s, and the mega rewrote products while streams read
   them, which the brief handled by sending them to committed blobs.
4. **Give the stream brief the private-repository list.** This session's brief misclassified hbofonts;
   `in/repo_maintenance_policy.json`'s `repo_visibility` is the source to copy.
5. **The owner's verification earns its place.** A stream's count did not survive this session's
   re-run (finding 2), two streams disagreed on another (finding 5.1), and several findings arrived from
   two or three streams independently, which this file reports once.
6. **`doc/periodic-review.md` still contradicts the trial about the pre-commit check** (finding 15.1);
   this review followed the trial.
