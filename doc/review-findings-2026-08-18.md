# Findings of the 2026-08-18 review of the work since 2026-08-10

Filed as [#231](https://github.com/bdenckla/MAM-basics/issues/231), which is a thin pointer to
this doc. The review covered **every clone directly under `~/GitRepos`** — committed work from
the 2026-08-10 review's anchors (MAM-basics `0a3eb1a`, MAM-private `b0aa6b1`, wlc-utils
`79404fa`; elsewhere the previous review's filing time, 2026-08-10T20:47 local) through
2026-08-18. That is **95 commits across 10 repos with activity**: MAM-basics 51 (three of them
the previous review's own filing and same-evening closures), holman-ketiv-qere 13, MAM-private
10, UXLC-utils 9, wlc-utils 4, github-misc 3, MAM-with-doc 2, MAM-parsed 1, MAM-simple 1,
phonetic-hbo 1 — re-measurable per repo with `git log <anchor>..HEAD --oneline`. Every tracker
was checked for in-window activity (`gh issue list --state all --search "updated:>=2026-08-10"`)
and only MAM-basics' had any: #215 closed by its fix, #229 and #230 filed, #185 commented, #228
and this review's #231 filed. wlc-utils, UXLC-utils, MAM-private, al-hatorah, masorah-books,
breuer-cos, holman-ketiv-qere and trope were all silent (trope#129's last comment is
2026-08-10T08:50 local, before the previous review filed).

The review ran in four streams: MAM-basics reviewed directly; three agent streams for
MAM-private (with the breadcrumb repos), for wlc-utils with UXLC-utils, and for
holman-ketiv-qere with github-misc and the four small repos.

Anchors: HEADs at review time were MAM-basics `6a6e600` (with `30cdfd2` and `6a6e600` committed
on main just before and during the review by the live UXLC-evacuation session), MAM-private
`a1b489e`, wlc-utils `8250b69`, UXLC-utils `9be1431`, holman-ketiv-qere `637237b`, github-misc
`549224e`. One session was live in MAM-basics throughout — the UXLC-utils evacuation session,
which during the review wrote back that plan's Phases 6 and 7 and declared holman-ketiv-qere
next — so this is a review of **committed work only**, and the one standing limitation of the
series applies again: no regeneration-and-diff of tracked outputs was run (a live session makes
in-place regeneration unsafe). Consequently **the holman-ketiv-qere evacuation gets no verdict**
— it had not started as an evacuation, though holman's 13 in-window commits are reviewed below —
and the next review owes it one.

## The verdict the previous review owed: al-hatorah R.3/R.4 are sound

The 2026-08-10 review left the al-hatorah evacuation mid-flight (R.0–R.2 committed and clean,
R.3/R.4 not started). Both phases are now committed, and **every figure the review could
re-derive matched exactly**; nothing contradicted. The record is MAM-private's
`doc/PLAN-evacuate-private-repos.md` (R.3 recorded by `9abae34`, R.4 by `6274009`), and the
programme closed itself on 2026-08-11 (`b31215a`). The exact re-derivations, each against the
named oracle:

- R.1's move commit `c67c210`: 1,559 files, 4,422,566 insertions — `git show --shortstat`, exact.
- R.3's emptying of the al-hatorah clone to a breadcrumb (`5d3afe61`): 53 additions, 4,422,566
  deletions — GitHub's commit API, exact, the deletion count equal to R.1's insertion count.
- All four breadcrumb repos (al-hatorah, masorah-books, mgketer, wlc-utils-private) track exactly
  `README.md`; al-hatorah keeps 124 issues (highest #127, the gap being PRs) and its full history
  — 2,875 content commits plus the breadcrumb commit, paginated out of the API rather than
  trusted; masorah-books keeps its 19 issues at head `e0b168d`.
- The nested tree's tracked working bytes reconcile **to the byte**: 148,942,042 on disk at
  MAM-private HEAD minus the two 2026-08-11 commits' net blob delta of +3,253 equals the
  148,938,789 the record states.
- `in/latest/` 929, `in/` 959, 26 overrides, 4 loose — `git ls-files` counts, exact (upholding
  R.3's finding 4, which corrected R.2's wrong 1,163).
- R.4's sibling commits all exist and match their described shapes: MAM-basics `136c6b9` (exactly
  `CLAUDE.md` + `all-repos.code-workspace`; the workspace keeps 20 folders, every one resolving
  on disk today), github-misc `81fdcec`, phonetic-hbo `59354973`.

MAM-private's window is 10 commits, local main == origin/main, tree clean, no accidental
commits: modes all 100644 (plus one deliberate deletion), no venv or cache files, the largest
new blobs being successive revisions of the plan doc itself (~394 KB).

## What else the review verified and found sound

**The wlc-utils evacuation (Phases 0–11, complete 2026-08-17) verifies from both sides.**
wlc-utils ends at `8250b69` tracking exactly the 161 files the record states (155 stub pages
plus six root files), CLAUDE.md and README rewritten to redirect-host facts. `cd668e3`'s
"Nothing is lost" was re-derived independently rather than trusted: all 335 deleted-and-copied
paths compared by blob SHA-1 against MAM-basics at `aa7f269`, with the recorded
`data/lci_recs.json` → `in/lci_recs.json` rename applied — 329 identical, 6 differing, 0
missing, and the 6 are exactly the files the message characterizes (the two survey JSONs Phase 5
was reworking, and the four files of the UXLC change-log refresh `3edbc5b`). The live site was
fetched, not assumed: three old wlc-utils URLs serve their committed stubs byte-identically
(sha256), their three MAM-basics targets return 200, an unstubbed path returns 404 carrying the
committed forwarding page, and all four fragment anchors UXLC-utils' pages cite exist on the
target page. `f10f405`'s staged-diff figures (1 A, 130 D, 154 M; the 130 decomposing as 122 png,
3 js, 2 jpg, 1 xml, 1 woff2, 1 css) re-derive verbatim, as do `cd668e3`'s (336 D + 2 M). Both
cited deploy runs are green under `gh run view`.

**On the MAM-basics side, the suite chain closes and the tree is healthy.** The previous
review's 904 moved to 903 in `0a3eb1a` — that commit's own message accounts for the one test, a
vendoring parametrize case dropped when al-hatorah's policy key folded into MAM-private's — and
903 held from Phase 0 through Phase 7, moving to 905 at `6a7347d` because
`test_entry_point_subcommands.py` parametrizes twice over every `py/main_*.py` that registers
subcommands and that commit added `main_wlc_redirect_stubs.py`. Re-measured for this review at
`6a6e600`: **905 passed, 5 skipped, 57 subtests** (`.venv/Scripts/python.exe py/main_test.py`,
91s), all five skips the edition-transcription semantic channel; `black --check py` clean at 774
files; `git ls-files` = 1,910, exactly the figure `a70ee8d` states. The vendoring audit's 22
DIFFERS rows decompose as the previous review's 20 pre-existing plus the two
`mb_cmn/uxlc_change_url.py` rows (mgketer, book-of-job) that `6fd9a9c` recorded rather than
fixed, its source having changed at `e4d7997`.

**Fix #215 (`2716e90`) verifies at the artifact level.** Its internal arithmetic closes (both
count drops equal the 1,610 lone bars; the munaḥ → legarmeh exchange is the same 1,172 on both
sides), and the tracked artifacts have the stated end state:
`out/accgram/chanted-word-accents.json` has `chanted_words` 233,232 / 233,115 / 233,066 (WLC /
UXLC / MAM) with MAM's `atomic_chanted_words` at 196,280, and
`gh-pages/wlc/accgram/wlc-chanted-word-residue.html` has its 28 rows with the Ne 8:7 dagger
caveat gone. A point the review had to establish for its own brief: **no MAM-simple data change
was expected**, because MAM-simple's data has the bar as a typed element (1,794 `lp-legarmeih`
plus 512 `lp-paseq` elements corpus-wide, no U+05C0 in verse text) and the fold is load-time, in
`mam_frags` alone.

**The two-accents plan is complete** — every phase executed or withdrawn (`8eef618`, `a70ee8d`).
The residue arithmetic verifies in the tracked JSON: `mam_residue.total` stays 12, the new
`accounted_for_by_breuer_ch3_s2` group holds 1, and `left_over_after_all_three` holds ca8:6
alone. MAM-private `a1b489e` pins the Breuer quote: the four pinned phrases were found verbatim
in `books/cos/md-export-of-docx/C03-S001.md`, and ITM's §279.4 citation of Ne 8:7 (one of two
legarmeh-before-pazer places) was verified in `books/itm/md-export-of-docx/N0241.md`. `a70ee8d`
records that **#185 stays open deliberately**, Breuer being one voice in a question weighing
manuscripts against printed editions.

**The UXLC-utils evacuation completed during the review** (Phases 1–7 all DONE, 6 and 7 written
back in `6a6e600`). Its committed work verifies: UXLC-utils keeps doc/ 2, in/ 556, out/ 27,
gh-pages/ 184, data/ 2 — the five counts MAM-basics' CLAUDE.md states, all re-derived at
`9be1431` — and the change-log saga's figures re-derive exactly (1367 → 1368 records at
`dd364d2`, → 1399 at `3435fc8`, the +31 being 1 in changeset 2026.07.24 plus Daniel Holman's 30
in 2026.08.05, which `aa5322c` here accepts a second address for). `30cdfd2`'s citation-prefix
figures re-derive from its own message's accounting: 57 sites read, 50 prefixed, 7 deliberately
bare, with `clc_render.py`'s "issue #6" corrected to "design doc §9 #6, not an issue".

**holman-ketiv-qere's 13 commits are sound.** Suite green at 51/51 (run for this review);
`TEST_MODULE_SPECS` complete at 8 registered = 8 tracked test files; `1206bcf`'s 20 → 124
correction-cases re-derived from `docs-not-served/uxlc_corrections.json` with every per-book
count exact; `636213d`'s five differing atom numbers re-derived (they are Lev 16:21, Josh 5:1,
2 Sam 24:10, Ezek 8:6, 1 Chr 27:21); `a0a722a`'s 1,367 records re-derived by ElementTree against
UXLC-utils at `3435fc8~1` — a method note worth keeping: a raw grep counts 1,379 because 12
`<change>` occurrences sit inside XML comments, so the parser is the right oracle.

**github-misc's tracked mirrors are honest**: the live `~/.claude/CLAUDE.md` and all six tracked
skill files are byte-identical to their `dot-claude/` copies (`cmp`), and no live skill file
lacks a tracked counterpart. The four small repos' single commits match their messages
(MAM-parsed `95f64d7`'s 12 Graphviz SVGs with balanced diffs and unchanged title sets;
MAM-with-doc's two dated drifts of `unpinned-latest.html` with "0 changes found" untouched;
phonetic-hbo's README repoint touching nothing under gh-pages/).

**The record-keeping ask of the previous review is now practice.** That review's finding 3 said
a sweeping negative is a claim too and wants the command that establishes it named. In this
window's ~95 messages, every sweeping negative names its oracle, and every one the review could
re-derive was true — "zero files touched, by mtime and not merely by git status" (`89b9b1d`),
the blob-SHA re-derivation above, sha256-compared URL fetches (`56ac9f4`, Phase 9), and
`d100480`'s differential run of old and new scanner spellings over 13,857 files in all 20
workspace repos. Corrections land in place with dates and their re-establishment commands
(`9194265` re-measuring the worktree suite count it had left unsettled, `69931be` correcting
Phase 10's expected count before that phase could trip on it, `e6c3141`'s "layer 1's number was
never 626", the 88 → 93 issue-count correction in `aa7f269`/`2658c02`).

## Findings

In rough order of consequence. As last time, nothing reaches "major": the review found **no
wrong code, no wrong data and no broken artifact** in the window.

1. **#228 is open with nothing left in it** — the same shape as the previous review's finding
   about #219. All three of its actionables are verified done: #219 closed 2026-08-11T03:05Z;
   the test-count refresh landed as github-misc `5e6234d`/`47dcfdb` with the live
   `~/.claude/CLAUDE.md` byte-identical to the tracked copy today; the Pillow `getdata` swap
   landed as `7033f94`. Its finding-8 watch item went unexercised — codex-index-cam1753 had no
   in-window commits — and transfers to this doc's open ends. Ben asked on 2026-08-18 whether
   #228 can be closed; the answer is yes.

2. **One factual error in a tracked doc, fixed during the review**: the UXLC evacuation plan's
   Baselines bullet said "the 19 `in/UXLC-misc/*.xml` change logs" where the count was always
   17 — provable from the paragraph's own arithmetic (39 + 7 + 17 + 477 downloaded plus 15
   hand-curated = its stated 555; 19 sums to 557). Nothing downstream leaned on it (the oracle
   figure is the artifact count 214, which never involved it). Fixed in `52cb1c6`.

3. **Eight of the window's 95 commits lack the `Co-Authored-By: Claude` trailer**: MAM-basics
   `20bb89e`, `2250c1c`, `5ed6bb4`, `3edbc5b`, `6fd9a9c`, `89b9b1d` (all 2026-08-12, one
   session); MAM-private `7f25357`; holman-ketiv-qere `637237b`. Convention slip only, the same
   class as the previous window's 10 of 44.

4. **Two loose phrasings in immutable messages, the window's full count of that class.**
   MAM-private `a1b489e` says "21 claims now, all confirmed" where the CLAIMS table's verdict
   vocabulary includes `needs qualifying` (three entries), `refuted for a single servant` and
   `confirmed as a negative` — so "all confirmed" can only mean "the checker passes on all 21",
   which is not what it says; the same message switches between "legarmeh" and "legarmeih"
   unmarked (defensible — each spelling tracks its book's transliteration — but unstated).
   wlc-utils `f10f405` calls the stubs "four-line" where a stub is 17 physical lines, four of
   which carry the redirect machinery. Zero banned constructions ("the latter", "the former", an
   unnamed "one … the other") anywhere in the window's messages, against two last window.

5. **Two cosmetic record gaps.** The 2026-08-10 review doc itself names the scan-pages plan as
   `doc/PLAN-scan-pages.md` where the file is `doc/scan-pages.md` (code `py/main_scan_pages.py`).
   And holman-ketiv-qere's `uxlc_standard_atoms.py` docstring figures (1,367 records, 174/170,
   50) were outrun 27 minutes after their 2026-08-12 re-measurement by UXLC-utils `3435fc8`
   (corpus now 1,399) — they are dated in the docstring, so a future re-measure moves them
   knowingly rather than silently.

## How the review was acted on (2026-08-18, during the review)

Finding 2 was the only actionable a session could take without a decision from Ben, and it was
fixed before this doc was filed (`52cb1c6`). Finding 1 closed the same day: Ben instructed
"close #228" within the hour of this doc's filing, and it was closed with a comment citing this
doc. Findings 3–5 recommend no work (immutable messages, practices going forward, dated figures
behaving as designed).

## Open ends the window itself declares (not findings)

The holman-ketiv-qere evacuation, which the live session declared next in `6a6e600` — owed a
verdict by the next review. MAM-basics #225, #226, #227 (from the previous window), #229 and
#230 (filed in-window), all open; #185 open deliberately, `a70ee8d` recording why. The
scan-pages undertaking parked at Phase 0 done since 2026-08-07 (`doc/scan-pages.md`), untouched
in-window. The cam1753 line-ending watch item from the previous review's finding 8, unexercised.
And the hcanat.us /Notes/ template question `e4d7997` flags: hcanat.us builds note pages from a
newer template than the 477 committed under UXLC-utils' `in/UXLC-notes/`, so a bulk
`main_clc_download_notes.py` run would mix two templates for `clc_note_pages` to parse — nobody
has decided to accept that, and the drafted reply to Chris Kimball asks whether hcanat.us is a
second front door or a staging copy.
