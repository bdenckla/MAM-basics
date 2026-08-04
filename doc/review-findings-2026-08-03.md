# Findings of the 2026-08-03 review of the work since 2026-07-30

Filed as [#219](https://github.com/bdenckla/MAM-basics/issues/219), which is a thin pointer to
this doc. The review covered **every clone directly under `~/GitRepos`** — commits from
2026-07-30T00:00 through 2026-08-03 ~23:00 (about 155 commits across 20 repos with activity)
plus the in-window issue activity in the five trackers that had any (wlc-utils, MAM-basics,
masorah-books, breuer-cos, UXLC-utils) — in five streams: wlc-utils; MAM-basics; masorah-books
with breuer-cos; the twelve smaller repos; and github-misc with al-hatorah and phonetic-hbo.

The previous review is wlc-utils#87 (2026-07-29), whose doc is wlc-utils
`doc/review-findings-2026-07-29.md`; its findings were acted on in wlc-utils 2aa40c8, the first
commit of this window. **The series lives in this repo from 2026-08-03 on**: the latest
`doc/review-findings-*.md` filename here is the authority on when the last review was.

File references are as of the HEADs at review time — wlc-utils bd0737c, MAM-basics 7727edf,
masorah-books 628cc14, UXLC-utils 748ee2f — and two sessions were live *during* the review
(the MAM-basics/wlc-utils chanted-word-accents wording pair, and masorah-books' #16 diacritics
repair, both uncommitted at 23:00), so treat references as anchors, not gospel. Two checks the
review did not run: a full regeneration-and-diff of tracked outputs (the live sessions made
in-place regeneration unsafe — the same limitation the 2026-07-29 review recorded), and any
judgment of the uncommitted in-flight work, which was observed only. Ten clones were quiet
(no commits, no issue activity): ArtScroll (a gist, no tracker), CCAR-Psalms,
diffable-pointed-hebrew, document-index, MAM-for-Acc, MAM-for-CCAR, MAM-for-JPS, TMC,
mamgo-auto-edits, wlc-utils-private.

What the review verified and found sound is *not* itemized here. The arithmetic of both Python
evacuations re-derives (wlc-utils and UXLC-utils each track 0 `.py`; MAM-basics' 767 reconcile
as 691 + 74 + 2; the test-count chain 311→320→333/824→832→830→913 closes); every rendered
number re-derived from the committed JSON matched (the residue page's 28-in-19 and 12, the
maqaf page's 462/233/116/130 and both pair-table totals, the fill-in's 529 = 515 + 14 and
154 = 147 + 7, the letters-only census); the three cross-repo sweeps are complete (the Pages
bump reached all ten repos with a workflow, `copilot-instructions.md` is gone from every repo
that had it with its facts salvaged, the vendored copies are byte-identical everywhere the
inventory calls them current); the live `~/.claude` policy files are byte-identical with
github-misc's tracked copies; and masorah-books' decision queue, measured-before-built probes,
and terminology all held up. The window's page work is the opposite of the previous review's
failure mode: three commits (9415017, 1e989ee, 007e708) exist specifically to put oracles
under prose counts, and everything pinned was right. What lagged instead was **write-back into
plans and docs** — every major below is a plan or doc contradicting the tree it describes.

## Major

**1. wlc-utils' two-accents plan contradicts itself about ca8:6 and Phase 5.**
`wlc-utils/doc/PLAN-two-accents-on-one-chanted-word.md` §0 — the section 192f97d's commit
message designates as what a phase reads first — says at line 62 that ca8:6 is held on a search
of Yeivin's ITM and Breuer's CoS "which nobody has yet run"; §10 at line 1115 says "THE SEARCH
BELOW WAS RUN, 2026-08-03, and both books are silent. Phase 4 may write ca8:6's entry"
(521e8dc updated §10 only). And the plan has "WLC's residue of 34" in four places (lines 53,
470, 544, 972) with Phase 5 framed as not yet started ("before a line of it is written") —
but the page landed the same morning (wlc-utils 43890f8 / MAM-basics 5fb9a69) and the residue
is 28 since ITM §256 took the qadma-darga six out (re-derived from
`out/accgram/chanted-word-accents.json` at HEAD: 28 rows in 19 distinct pairs). f1ce314
corrected Phase 4's figures under the same settlement and left Phase 5's alone; no commit
records Phase 5 as done. A fresh session resuming from §0 — the exact reader the
plans-for-a-fresh-session rule (github-misc ffce2ed, 2026-08-03) names — believes ca8:6 is
blocked and Phase 5 unbuilt. Fix: one write-back pass over §0, §5's Phase 5 entry, §9.

**2. wlc-utils' transcription workflow doc runs code that left the repo, with no move note.**
Every command block in `wlc-utils/doc/edition-transcription-workflow.md` (lines 30, 36, 193,
223, 232, 258, 288) reads `.venv/Scripts/python.exe py/main_edition_transcription.py …`; that
file left with the 2026-08-01 evacuation (6180f8d), wlc-utils tracks no `.py`, and its
CLAUDE.md says the leftover `.venv` has nothing to run. The two-accents plan got a
the-code-moved note (61ede49) and CLAUDE.md was rewritten; this doc — self-described as
written down so a session can pick the work up from here — got nothing. Fix: repoint the
commands at `MAM-basics/py/main_edition_transcription.py` run from MAM-basics, or add the one
covering note.

**3. masorah-books' README is stale about the merged tracker's state, where CLAUDE.md was
fixed.** `masorah-books/README.md` line 138 has the Chapter-10 defect "known, and open as
`breuer-cos` #4 — … those pages need re-OCR": the re-OCR landed 2026-08-03 (f097a0f) and
breuer-cos#4 is closed — f097a0f updated the census sentences a few lines away and left this
one. Line 439 says "`breuer-cos` #1–#4 stay open in that repo": #1 closed 2026-08-02 and #4
closed 2026-08-03 (810a432 fixed CLAUDE.md's twin sentence to "#2 and #3 stay open in place"
and missed README's). And the "Open issues at a glance" table omits #14, #15, #16, #17 — all
booked after the table was composed (ce05e36). Fix: the two sentences and four table rows.

**4. The evacuation programme doc overstates UXLC-utils' progress.**
`MAM-basics/doc/PLAN-evacuate-python-programme.md` line 13's status row says of UXLC-utils
"Only Phase 6 remains" — but `doc/PLAN-evacuate-python-from-UXLC-utils.md` §Phase 7 has items
2–6 outstanding, item 6 being the edit to the hebrew-prose skill's citations of UXLC-utils
Python (flagged stop-and-ask-Ben, committing to a third repo, both unsynced copies). Smaller,
same file: the UXLC plan's status table says Phase 7 "not started" while its Phase 4 row and
§Phase 7 record item 1 as done inside 2b44958 — the two claims cannot both be read as written.
Fix: correct the programme row to name Phases 6 and 7's remainder; reconcile the Phase 7 row.

**5. wlc-utils' fix-tester artifact went stale again, through the channel 97c695e named.**
a8b8a88 (the METHIGAZAQEF fuse stopping at a space) moved je49:19's and mi2:7's ERROR node
from tipexa_phrase to zaqef_phrase; `out/accgram/fix-tester/_fix_tester.json` still has both
verses' rows from the old parse, `test-fixes` not having run since 2026-07-30 — the second
staleness in one window, exactly as 97c695e's message predicted ("test-fixes is not one of
main_0_mega.py's steps"). MAM-basics#218 records the affected research notes but not this
artifact. Fix: either add test-fixes to the mega's wlc-utils steps or give the artifact a
staleness check; regenerate once #218's notes exist.

## Minor

**6. The maqaf page still cites §224 for metigah-zaqef after the same-day correction.** #86's
2026-08-03 comment ruled §223 defines metigah-zaqef and §224 is the retraction; d3d656e
corrected the survey (`py/accgram/maqaf_nonfinal_accents.py` line 230) but
`py/accgram/maqaf_nonfinal_accents_page.py` line 2144 still renders "§§210, 216, 221, 224,
233 and 241" (and its lines 2065–2066 still gloss §224 as metigah-zaqef), so the page
disagrees with its sibling survey's citation.

**7. The WLC residue page has ne8:7's MAM figure with no caveat.** Its MAM column has
"merkha, munaḥ" against WLC's "merkha, legarmeh" for the same chanted word — but MAM has the
bar, space-delimited, invisible to the scanner (MAM-basics#215; the same defect leaves MAM
with 0 legarmeh tokens against WLC's 1,167). Mitigation: the page is deliberately unlinked,
and Ben sequenced the #215 fix before Phase 4; a one-line caveat at that row would close it.

**8. wlc-utils#86's "Left open" item 1 was implemented hours later with no follow-up
comment.** The §357 ANFA-reason ("Left to Ben") landed the same afternoon as MAM-basics
d72534b / wlc-utils 5783062; the thread as it stands reads the item as pending.

**9. MAM-basics 7727edf's message cites a bare foreign hash.** "was itself rejected in
1377ded" — a wlc-utils commit that does not resolve in MAM-basics, in the repo whose CLAUDE.md
has a section on prefixing cross-repo references. (c5638f4 is the same correction's MAM-basics
twin.)

**10. MAM-basics CLAUDE.md's test-discovery sentence is incomplete since the UXLC-utils
copy-in.** "pytest discovers `py/tests/test_*.py` itself. Drop a new test file in and it
runs" — eight copied-in files are suffix-named (`clc_attribution_test.py` and siblings,
`source_hygiene_test.py`) and collect only because pytest's default also matches `*_test.py`;
a file matching neither pattern still reports nothing at all. One sentence naming both
patterns fixes it.

**11. masorah-books CLAUDE.md line 140 says the dry run pins "26 numbers"; the table has
29.** `QUOTED_IN_ISSUE_7` in `py/itm/fillin_dry_run.py` has 29 entries (24 at c3ac950, 26 at
a15dc48, 29 at 86f9afa; CLAUDE.md tracked the first two growths and missed the third). README
and the decision queue both say 29.

**12. codex-index-cam1753 cites the deleted Copilot file.** `doc/cam1753-line-break-task.md`
line 96: "always create a script in `.novc/` per the general copilot instructions" — deleted
by 77ff9fe. One line.

**13. UXLC-utils `doc/clc-design.md` has two stale claims its covering note does not
repair.** Around line 285 it cites `.github/copilot-instructions.md` as co-authority
(deleted), and a few lines later states codex-index-leningrad "is not currently checked out
as a sibling" (the clone exists). ad52001's substitution rule covers only `py/` paths.

**14. The vendoring inventory's codex-index-aleppo row conflates CRLF noise with drift.**
Three of the four `py/mb_cmn` files it marks DIFFERS are blob-identical to MAM-basics
(`hebrew_points.py`, `uni_denorm.py`, `url_percent.py` — the difference is CRLF-on-disk, the
known latent-CRLF condition extended to a third repo); only `str_defs.py` genuinely differs,
there and in cam1753 and book-of-job.

**15. The hebrew-prose skill and wlc-utils#77's amended plural rule are unreconciled.** The
2026-08-03 comment narrows the plural carve-out (a plural needs a quantifier, not just
grammatical number); the rule lives in the comment only, the skill's text predates it, and no
sweep of existing prose has run against it. Deliberately parked (ea26ad27's message), but the
skill is what sessions load.

## Decision items, not defects

- str_defs.py's content drift in codex-index-aleppo, codex-index-cam1753 and book-of-job
  (missing the LDQM/RDQM additions; aleppo also has an extra CGJ_RE): re-vendor, or record as
  local variants.
- al-hatorah has a stale fully-merged remote branch, `origin/feat/override-diff-viewer`
  (2026-04-24). Deleting it is a branch deletion, so it waits for an explicit ask.
- wlc-utils#90: whether the twelve transcription headers naming old script paths are
  provenance to keep or pointers to fix — genuinely undecided, no comments yet.

## Standing open ends (tracked elsewhere; listed for the at-a-glance)

MAM-basics#218 (generate-html is build-blocking-broken until three research notes exist;
goerwitz.html knowingly stale meanwhile) · MAM-basics#215 (spaced U+05C0; fix sequenced before
two-accents Phase 4) · MAM-basics#216/#217/#213/#214/#207 · two-accents Phases 4–5 write-back
(major 1) and the qadma-azla melody clause held unanswered by request · the
rest-of-wlc-utils evacuation plan (b2d3aca): all 11 phases unstarted · the programme's
blocking Phase 0 (check_*/fix_* fork reconciliation) unstarted, holman-ketiv-qere,
book-of-job and the codex-index trio unstarted · UXLC-utils evacuation Phases 6–7 (major 4) ·
masorah-books: #16 in flight tonight, #13 (p. 293's dropped line), #17 (Yeivin 2003), the 38
maqaf disagreements booked and unowned, proposal phases 3–6 · wlc-utils#86's remaining
MAM-vs-Breuer research questions, #89 (Pillow, 2027 deadline), #92 (2 Chr 25:17, to settle in
al-hatorah), #93 · tanach.us robots.txt blocks both UXLC downloaders (external).
