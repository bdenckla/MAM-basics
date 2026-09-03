# Findings of the 2026-08-03 review of the work since 2026-07-30

State: acted on 2026-08-04, all fifteen items

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

## How the review was acted on (2026-08-04)

**The majors and minor 6**, in four passes, Ben's ask of 2026-08-03.
Majors 1 and 2: wlc-utils 51113cf and a275830. Major 3: a concurrent masorah-books session
had already drafted the full fix in its working tree — verified correct against the trackers,
one improvement included (#16 closed the same night, so it gets no open-table row) — and the
draft was left for that session to land. Major 4: MAM-basics faa8b3f, whose verification also
caught this doc's hash error (corrected in the entry below). Major 5: MAM-basics 80c8a42
(`accgram-test-fixes` joins the mega directly after `accgram-run-prose`; no evidence the
exclusion was ever deliberate, runtime 2.8 s) and wlc-utils 505d88e (artifact regenerated:
je49:19's and mi2:7's ERROR node moves tipexa_phrase → zaqef_phrase, verdict counts
unchanged). Minor 6 was independently fixed by the concurrent session's ef3334b, which notes
the §223/§224 disagreement on the page rather than asserting either side.

**Minors 7 through 15**, later the same day, in four passes batched by kind, Ben's ask of
2026-08-04. All nine are closed out; only minor 9 is closed as a dismissal.

- **7**, the ne8:7 caveat: MAM-basics 9d78b20 and cdaeac4, wlc-utils e0abcc5 and 4fad32d. The
  marker and the note are derived rather than pinned to the verse — `mam_reads_no_legarmeh` asks
  whether WLC's sequence has a legarmeh where its MAM counterpart has none — so both leave the
  page on their own the day #215 is fixed, and `pin_claims` asserts the shape of that argument
  rather than a count the fix would falsify. The mechanism was checked against MAM-parsed-plus
  first: at Nehemiah 8:7 MAM's stroke is a `מ:לגרמיה-2` template, which MAM-simple renders as a
  vel of its own, where WLC 4.22 has the U+05C0 attached to the word.
- **8**: recorded on wlc-utils#86 as a follow-up comment. §357's ANFA-reason is the **third**, not
  the fourth — the module had two routes before d72534b.
- **9**: dismissed, as anticipated. Amending a commit message needs Ben's explicit ask and is not
  worth it; the bare hash is in no tracked file of any repo (checked 2026-08-04), so there is
  nothing to prefix. The lesson stays in this repo's CLAUDE.md.
- **10**: MAM-basics ff22f96, naming both of pytest's default `python_files` patterns and
  `mc_marks.py` as the one file under `py/tests/` matching neither. **This doc's "eight copied-in
  files are suffix-named" was wrong and is corrected to seven below** — the doc's own parenthesis
  listed six `clc_*` plus `source_hygiene_test.py` and so disagreed with its prose. Measured at
  HEAD: 69 + 7 + 1 = 77 tracked files under `py/tests/`.
- **11**: masorah-books 94a162a. `QUOTED_IN_ISSUE_7` re-counted at HEAD by an AST walk rather
  than by eye: 29, so CLAUDE.md was the only file wrong — README and the decision queue already
  said 29, and the three sibling counts in the same bullet (24, 36, 28) re-derive unchanged. A
  session was live in that repo and edited CLAUDE.md itself mid-pass, so only the one hunk was
  staged, by patch, leaving that session's prose in the working tree.
- **12**: codex-index-cam1753 ca29f9e, repointed at the user-level CLAUDE.md, the repo's own
  never having carried the rule. That was the repo's last `copilot` reference of any kind.
- **13**: UXLC-utils 47c3e97. The deleted co-citation is dropped rather than repointed, since
  `shared-with-codex-index-leningrad.md` states the canonicity alone; and the not-checked-out
  premise turned out to be load-bearing in **three** places, not the one the finding named, so
  all three were corrected together. The genuine `[TBD]` — whether lenin-wiki's index beats the
  vendored tanach.us LCIndex — survives, minus its blocked-on-a-clone framing. A broken relative
  link in the same sentence was fixed in passing.
- **14**: MAM-basics effb057. `compare.py` now hashes raw bytes and, when those differ,
  newline-normalized bytes, emitting `eol-only` as a third verdict — one whitespace-free token,
  because `gen_inventory` parses that column on runs of two or more spaces. A trailing-newline
  difference deliberately stays `DIFFERS`. **The finding understated the condition five times
  over**: 15 rows move `DIFFERS` → `eol-only`, not 3 — ten in book-of-job, four in
  codex-index-aleppo (one of them `aleppo-wiki/py/hebrew_letters.py`, outside the row the finding
  named), one in diffable-pointed-hebrew. A sixteenth row, codex-index-leningrad's
  `lenin-wiki/py/hebrew_letters.py`, moves `DIFFERS` → `identical` for an unrelated reason: that
  repo's 6ccd856 made it match on 2026-08-03 and the inventory had not been regenerated since.
  Verdicts now stand at 116 identical, 15 eol-only, 23 DIFFERS of 154. Beyond the ask, the four
  writers under `py/vendoring/` were themselves writing CRLF into this repo's `out/` and `doc/`
  against `.gitattributes`, and now pass `newline="\n"`.
- **15**: github-misc 722a1dc and fc21d72, both copies of the skill. The rule had never been in
  the skill **at all** — its only traces were a sibling mention in `references/rendered-prose.md`
  and one example in `SKILL.md` — so this was a missing rule rather than a stale one. Ben,
  2026-08-04, asked for the rule without a sweep, and asked that it not read as absolute: *"I'm
  sure there are exceptions where 'the strand' or 'the strands' is clear from context … some
  degree of implicitness (e.g. mention earlier in a sentence!) is always acceptable."*
  wlc-utils#77's open items 1 and 2, the sweep itself, stay open.

**Major 5's channel, closed the rest of the way**, later on 2026-08-04. Major 5 fixed the one
artifact it caught; the channel it named — a tracked artifact with nothing routinely regenerating
it — stayed open for every other by-hand generator that writes one. MAM-basics f162d7f makes
steps of all eight: the accgram subcommands `run-dual-cant`, `xcheck-poetic`, `servi-xcheck`,
`grammaticality`, `run-printed-decalogue` and `survey-chanted-word-accents`, plus
`main_find_uxlc_accent_changes.py` and `main_uxlc_grammar_test.py`, the two wlc-utils' CLAUDE.md
itself flagged as "not in the mega". **Two of the eight were already stale**, so the channel had
taken more than the artifact major 5 found: `out/accgram/_grammaticality.txt` since 2026-06-29
(93 → 96 ungrammatical, the METHIGAZAQEF change of #218) and `out/accgram/uxlc_grammar_test.txt`
since 2026-08-01 (ne 9:20 crosses WLC-ungram → UXLC-gram, #218 item 1's third verse). wlc-utils
505cbfc regenerates both. The second **falsified a claim the report had pinned in prose while
splicing its counts live** — "No fix leaks into OUT and no degradation leaks into IN", printed
three lines under a count of one fix that had crossed — so that paragraph is derived now and
cannot outlive its numbers again; the leak is #218 item 1 unwritten rather than a defect, and ne
9:20 rejoins the IN set when its research note names its `uxlc_change`. Cost: 12.4 s for seven of
the eight. The eighth, `survey-chanted-word-accents`, measures 68.6 s, and Ben's decision that day
was neither to pay it nor to skip the step but to run the survey once and give `generate-html` a
`--trust-survey` flag — the residue page having already been spending 60.1 s rebuilding the same
survey inside the mega, which the flag turns into 1.1 s against a byte-identical page. What is
left outside the mega on purpose: the two network vendoring subcommands, and the
`generate-html-<name>` singles the batch covers.

**The three decision items**, later on 2026-08-04, once Ben had answered all three. Each is closed
out, and two of this doc's own descriptions of them turned out to be wrong.

- **str_defs.py's drift — re-vendored**, rather than recorded as deliberate local variants:
  codex-index-aleppo e03f7ff, codex-index-cam1753 1486fb3 and book-of-job 8bc2602, each a
  byte-verbatim copy of MAM-basics' `py/mb_cmn/str_defs.py`, plus MAM-basics 377021d regenerating
  the inventory. **This doc's "aleppo also has an extra CGJ_RE" understates it**: all three copies
  had the `#` line and `CGJ_RE`, and all three were byte-identical to each other — the same blob
  transition `9d4cad6..4c76029` in all three repos is the evidence. What made the re-vendor safe is
  that it is behavior-neutral: no file in any of the three repos names `LDQM`, `RDQM` or `CGJ_RE`
  outside `str_defs.py` itself, before or after. Copying bytes rather than text cleared the latent
  CRLF in aleppo's and book-of-job's working-tree copies (295 bytes on disk against 284 in HEAD) in
  the same stroke. Verdicts move to 119 identical, 15 eol-only, 20 DIFFERS of 154, from 116/15/23.
  The row count does *not* move — 22 both sides, because book-of-job's six-file DIFFERS row
  splitting off a new identical row and cam1753's single-file row merging into its existing
  identical row cancel exactly, so the row count is no proxy for the verdicts. book-of-job's other
  five drifted copies stay untouched, being the ones that are not behavior-neutral.
- **al-hatorah's stale remote branch — deleted**, and nothing else:
  `origin/feat/override-diff-viewer`, tip 9873fe53. The deletion left main untouched at f4ef41e1
  and merged nothing, and `git branch -r` now lists `origin/HEAD` and `origin/main` alone. (A
  concurrent session in that repo has since advanced main to fb1af0d0 on unrelated ITM work, so
  f4ef41e1 is where main stood at the moment of the deletion rather than where it stands now.)
  **This doc's "fully
  merged" was true of the branch's content and false of its ancestry**: `git branch -r --merged
  main` listed only `origin/main`, because the branch's two commits were replayed rather than
  merged and sit on main as same-message, same-date twins (ccf44337→d3defafc, 9873fe53→df9544a9,
  both 2026-04-24). Every file the branch added is on main except
  `py/a2dmain_make_override_diff_viewer.py`, which main renamed to
  `py/main_3d_make_override_diff_viewer.py`.
- **wlc-utils#90 — the twelve transcription headers are provenance and stay untouched**; the old
  paths are mapped once instead, in wlc-utils 54ea941, which extends the covering note at the top
  of `doc/edition-transcription-workflow.md` and leaves everything under `in/` alone. wlc-utils#90
  is closed with the decision recorded. The mapping rests on two facts: every module the headers
  name that was ever a tracked file — five of them — still exists under `MAM-basics/py/`, so each
  header's `py/`-relative path is still correct and only the repo moved; and
  `col_profile.py`/`row_profile.py`, named in `simtiq_ex_elyon.txt`, were untracked `.novc`
  scratch, tracked in neither repo, so that mention was unfollowable on the day it was written —
  itself evidence that the headers were never pointers.

The standing open ends are untouched. Minor 14's measurement had enlarged the first decision item
before it was acted on, as recorded there.

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
§Phase 7 record item 1 as done inside MAM-basics 2b5c87c — the two claims cannot both be read
as written. (This doc first cited item 1's commit as UXLC-utils 2b44958, an unrelated sys.path
commit; corrected 2026-08-04, when the acting pass followed the plan file's record.)
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
runs" — seven copied-in files are suffix-named (`clc_attribution_test.py` and its five siblings,
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
there and in cam1753 and book-of-job. (Both halves of that last clause were measured when the
fix ran: the condition reaches 15 copies in four repos, not 3 in one, and book-of-job has six
genuinely drifted copies rather than only `str_defs.py`. See the acting entry above.)

**15. The hebrew-prose skill and wlc-utils#77's amended plural rule are unreconciled.** The
2026-08-03 comment narrows the plural carve-out (a plural needs a quantifier, not just
grammatical number); the rule lives in the comment only, the skill's text predates it, and no
sweep of existing prose has run against it. Deliberately parked (ea26ad27's message), but the
skill is what sessions load.

## Decision items, not defects

**All three were answered by Ben on 2026-08-04 and acted on the same day.** The findings are kept
here as written, because they are the record of what the review put to him; the commits, the
numbers and the two corrections to the wording below are in "How the review was acted on".

- str_defs.py's content drift in codex-index-aleppo, codex-index-cam1753 and book-of-job
  (missing the LDQM/RDQM additions; aleppo also has an extra CGJ_RE): re-vendor, or record as
  local variants. **Enlarged 2026-08-04 by minor 14's fix**, which separated the CRLF noise from
  the drift and so measured the drift for the first time: 23 copies genuinely differ, and
  book-of-job alone has six (`bib_locales.py`, `file_io.py`, `hebrew_accents.py`,
  `hebrew_punctuation.py`, `str_defs.py`, `uni_heb.py`). The decision is the same one, over a
  larger set than it was framed for. **Decided: re-vendor**, the three str_defs.py copies only.
  The parenthesis above is one of the two corrections — all three copies have the extra CGJ_RE.
- al-hatorah has a stale fully-merged remote branch, `origin/feat/override-diff-viewer`
  (2026-04-24). Deleting it is a branch deletion, so it waits for an explicit ask. **Decided:
  delete the remote ref, and nothing else** — the ask came. "Fully merged" is the other
  correction: the branch was replayed onto main rather than merged into it.
- wlc-utils#90: whether the twelve transcription headers naming old script paths are
  provenance to keep or pointers to fix — genuinely undecided, no comments yet. **Decided:
  provenance**, with the old paths mapped once in wlc-utils' workflow doc; wlc-utils#90 closed.

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
