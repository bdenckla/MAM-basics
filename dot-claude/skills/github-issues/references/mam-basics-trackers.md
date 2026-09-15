# MAM-basics issue-tracker history and citation traps

Read this reference when auditing, migrating, or interpreting issue citations in MAM-basics. The concise current rule remains in MAM-basics' `AGENTS.md`.

## Five issue trackers: a bare `#NN` here means MAM-basics

wlc-utils' issues were **not** transferred when its Python moved here on 2026-08-01. They keep
their numbers and stay in `bdenckla/wlc-utils`, which is still where they are read, commented on
and closed — 93 of them as of 2026-08-17 (this paragraph long said 88, a count that was already
five short when it was written: #89–#93 were filed 2026-07-31). The trackers unify *going forward* only: **every new issue, including new work on the
moved code, is filed in MAM-basics.**

So in this repo a bare `#NN` names a MAM-basics issue, and a citation of a wlc-utils issue is
written **`wlc-utils#NN`**. The prefix is not decoration: both trackers have issues in the 1-88
range, and several numbers name quite unrelated things in each — wlc-utils#52 is the printed
Decalogue where MAM-basics #52 asks about a meteg in Ezekiel, wlc-utils#69 the hand transcriptions
where MAM-basics #69 is a CSS URL, wlc-utils#75 making maqaf a token of its own where MAM-basics
#75 is the `mb_cmn/paths.py` convention. The moved code's 326 bare citations were prefixed on
2026-08-02.

**UXLC-utils is the third tracker and works the same way.** Its issues were not transferred when
its Python moved here on 2026-08-03 either — 56 of them as of 2026-08-18, numbered 1–56, still
read, commented on and closed in `bdenckla/UXLC-utils`. So a citation of a UXLC-utils issue is
written **`UXLC-utils#NN`**, and here the whole numbered range collides: UXLC-utils#19 removes the
CLC note fallbacks where MAM-basics #19 asks for a no-args mode in `main_diff_mpp`, UXLC-utils#29
encodes the pasoleg-tokenization verses where MAM-basics #29 wants mgketer links, UXLC-utils#48
lets the editor simplify a reiterated note-target word where MAM-basics #48 is a space before sof
pasuq in Isaiah 44:24. The moved code's 50 bare citations were prefixed on 2026-08-18, across
eight `py/clc/` modules and `py/main_clc_download_notes.py`.

**holman-ketiv-qere is the fourth tracker.** Its Python moved here on 2026-08-18 and its issues
were not transferred either — **81 of them, numbered 1–81, 60 open**, measured 2026-08-18, still
read, commented on and closed in `bdenckla/holman-ketiv-qere`. So a citation of one is written
**`holman-ketiv-qere#NN`**, and the whole numbered range collides, all 81:
holman-ketiv-qere#4 is row 13's 2 Samuel 11:24 ויראו where MAM-basics #4 produces MIDI of a trope
realization, holman-ketiv-qere#48 is row 41's Jeremiah 17:11 ימו where MAM-basics #48 is a space
before sof pasuq in Isaiah 44:24, holman-ketiv-qere#75 is row 65's Ezekiel 40:34 ואלמו where
MAM-basics #75 is the `mb_cmn/paths.py` convention. Most of holman-ketiv-qere's issues are one per
review row, titled "row NN Book C:V FORM MAM qere", and `io/table_row_github_issues.json` holds
that mapping. **Six numbers became four-way collisions when holman-ketiv-qere's tracker was
added** — #19, #29, #48, #52, #69 and #75, each already cited above as a wlc-utils or a
UXLC-utils collision.

**Unlike the two moves that had citations to prefix — wlc-utils' 326 and UXLC-utils' 50 —
holman-ketiv-qere's move had nothing to prefix**, which is worth stating because the arithmetic
that predicts otherwise is so easy to do. Phase 6 read every `#`-plus-digit site in
the 60 files that moved and found no citation of any tracker among them: 19 CSS hex colours in
`py/py_render/rt_assets.py`, and the `#2026.08.05-6` UXLC **change** anchor in
`py/hkq_cmn/uxlc_change_records.py`. The rest of holman-ketiv-qere's pre-move `py/` carried eight
more sites, and every one is disposed of rather than moved. Six sat in `py/mb_cmn/`, which was a
pure deletion: four lines of `hebrew_accents.py` citing Yeivin *ITM* as `#194`, `#358` and `#361`,
and two of `paths.py`, a `#75` naming MAM-basics' paths convention and an already-prefixed
`wlc-utils#48`. The other two are both `#187`, naming MAM-basics' NFC convention — one in
`main_test.py`, which disappeared, one in `test_h_dot_below_nfc.py`, which collided with this
repo's copy. **A repo can move its whole
Python and still owe this section nothing but a clause** — count the citations, never the files.

**book-of-job is the fifth tracker.** Its Python moved here on 2026-08-19 and its issues were not
transferred either — **61 of them, numbered 1–61 with no gaps, 19 open**, measured 2026-08-22,
still read, commented on and closed in `bdenckla/book-of-job`. So a citation of one is written
**`book-of-job#NN`**, and the numbered range collides from #1 upward: book-of-job#1 studies UXLC
changes in Job where MAM-basics #1 syllabifies pointed Hebrew, book-of-job#7 shows only the first
five of each group where MAM-basics #7 adds `main_diff_mpp.py`. **Its issues take the shape
holman-ketiv-qere's do rather than wlc-utils'**: 37 of the 61 name a Job verse or a quirk-record
SID in the title, 11 of those leading with the verse, as "30:18: add prefix; expand Lenin crop"
does — one issue per quirk record, per manuscript image, or per crop-editor failure. **The bullet
below about modules that render issue references as data does not apply here**: book-of-job's
issue numbers live in its tracker and in prose, and no module of its code turns them into links or
tags, so it has no counterpart to `io/table_row_github_issues.json`. The book-of-job data and
programs now live under `book-of-job/` and `py/` in MAM-basics; no `DATA_REPO_NAME` constant remains.

**Four of the six numbers named above are now FIVE-way collisions** — #19, #29, #48 and #52, whose
book-of-job titles are "Add Aleppo Codex image for 34:5", "supplement μA images with manuscript
locations", "details is getting too big" and "30:18: add prefix; expand Lenin crop". **#69 and #75
stay four-way**, book-of-job's numbering stopping at 61.

**book-of-job had nothing to prefix either, which makes it twice running.** Its move was the
programme's largest, 241 modules against holman-ketiv-qere's 60, and it owed this section exactly
as little. All **29** `#`-plus-digit sites in the 268 `.py` that repo tracked before the move are
disposed of without a prefix: **24 are lines of CSS hex colours**, 32 colour tokens on those 24
lines (the two files hold 46 tokens over 36 such lines, the other 12 lines opening with a letter
and so not matching `#`-plus-digit; this sentence said "46 colour tokens between them" until the
2026-08-22 review), in `py/main_gen_aleppo_crop_editor.py` and
`py/main_gen_cam1753_crop_editor.py`; **four are Yeivin
*ITM* section numbers** — `#194`, `#358` and `#361` — in the `mb_cmn/hebrew_accents.py` copy Phase
4 deleted, the same four lines holman-ketiv-qere's copy carried; and the twenty-ninth,
`py/author_boj_util/qr_relations.py:75`, was already written out in full as
`bdenckla/wlc-utils#43`. book-of-job's copy of `mb_cmn/` held no `paths.py` and its
`test_h_dot_below_nfc.py` cited nothing, so even the two `#187` sites and the `#75` that
holman-ketiv-qere's move disposed of have no counterpart here. **Two moves of very different
sizes have now confirmed the same thing: how many citations a move owes is a function of what its
code talks about, never of how many files it is.**

**Five more public trackers were emptied into this one on 2026-08-26, by transfer, and this
section keeps its "Five" name anyway.** Between 18:50 and 19:01 local that evening, Ben
transferred all 27 open issues of five public trackers into MAM-basics, where they are
**#234–#260**: codex-index-cam1753 2 (#234–#235), MAM-simple 2 (#236–#237), codex-index-aleppo 6
(#238–#243), MAM-parsed 8 (#244–#251), MAM-with-doc 9 (#252–#260) — re-derived 2026-08-27 from
the GitHub GraphQL timeline (`TransferredEvent.fromRepository`), all 27 open here that day. A
transferred issue is a MAM-basics issue: its home citation is a bare `#NN`, and the old qualified
form still resolves through GitHub's transfer redirect (Ben observed this during the 2026-08-26
review), so an old-form citation is stale-but-working rather than broken. The first repointing is
done: `doc/sigil-decoding.md` carried `MAM-with-doc#6` at six sites — five citations of its
umbrella issue plus the paragraph justifying their qualifier, all six qualified by `e624139` at
18:27 that same evening, 34 minutes before the transfer — and since 2026-08-27 it cites the issue
as **#257**, its number here (Ben's decision), the justifying paragraph now carrying the
citation's three forms instead. `e624139`'s message, "MAM-with-doc becomes the sixth tracker
cited from this repo", is immutable and stays as the record of those 34 minutes.

**The five source trackers hold closed issues only now** — MAM-with-doc 1, MAM-parsed 12,
MAM-simple 2, codex-index-aleppo 21, codex-index-cam1753 10, 0 open each, measured 2026-08-27 —
and no new issue is filed in any of them: a new public-side issue goes to MAM-basics, and the
private half of that doctrine is recorded at MAM-private `9dfe424` (2026-08-26), new issues to
MAM-private or MAM-basics and nowhere else. A citation of one of those closed issues takes the
repo prefix like every cross-tracker citation in this section — `MAM-parsed#NN`,
`codex-index-aleppo#NN` — and every number in all five closed sets collides with a MAM-basics
number, so the prefix is as non-decorative there as anywhere. **The count in the section's name
stays at five** because the five it counts are unchanged — MAM-basics itself, then wlc-utils,
UXLC-utils, holman-ketiv-qere and book-of-job, whose issues stay put and are still read,
commented on and closed where they are. The newly emptied five are a consolidation record inside
the section, not a sixth through tenth count; settled 2026-08-27, Ben having deferred the
framing, and recorded here so a rename is not re-proposed. Finding 2 of
`doc/review-findings-2026-08-26.md` is the fuller record of the transfer evening.

**This section has had four names.** It was "Two issue trackers" until 2026-08-18, "Three issue
trackers" for part of that same day, "Four issue trackers" from later that day until 2026-08-22,
and "Five issue trackers" since. Dated execution records in the surviving programme and in
deleted plans preserved in Git history use the earlier names because each record describes the
section as it stood when that phase ran.

Three things a blind sweep gets wrong, so read the surrounding sentence before adding a prefix:

- **Not every `#NN` is an issue.** Yeivin's *ITM* is cited by section number in exactly the same
  shape (`#194`, `#221`, `#246`, and the `#325`–`#391` poetic run), CSS carries hex colours —
  `py/main_gen_cam1753_crop_editor.py` holds 23, as its Aleppo counterpart did until phase 6a of
  `doc/PLAN-mega-coverage.md` deleted it on 2026-09-10 — and `poetic_ply_grammar.py` numbers the
  accents of Ps 17:14 as `#7`–`#10`. None of those
  take a prefix. **The CLC code has seven such sites, and each has a real UXLC-utils issue of that
  number waiting to be mistaken for it**: `doc/clc-design.md` numbers its §9 open questions in
  the identical shape, so `clc_collect.py`'s "design doc §9 #2" and `clc_render.py`'s "design doc
  §9 #6" name that list rather than issues #2 and #6; three sites name a UXLC **change** number,
  the 2026.10.19 release's tenth change, written "change #10" and "pending change #10"; and
  `main_uxlc_grammar_test.py`'s #218 and #219 are MAM-basics' own, so they are already right
  bare. `clc_render.py`'s site read "issue #6" until 2026-08-18 and now says "design doc §9 #6,
  not an issue", which is what the `clc_collect.py` site had said all along.
- **Two modules render issue references as DATA about the Holman review, not as citations of a
  tracker, and prefixing them corrupts the rendered table.** `py/py_render/rt_issue_tags.py` and
  `py/hkq_cmn/table_row_github_issues.py` turn `io/table_row_github_issues.json` into the per-row
  issue links, state and tags on holman-ketiv-qere's report pages. Those numbers are
  holman-ketiv-qere issue numbers already, resolved through the `REPO_OWNER` and `REPO_NAME`
  constants that name `bdenckla/holman-ketiv-qere` and are passed to `gh issue list --repo`;
  leave the constants and the rendering alone. Phase 6 of
  `doc/PLAN-evacuate-python-from-holman-ketiv-qere.md` names this as the trap to check for first.
- **`github_issue_edit.py` is what keeps the split safe, and its own `#69` is deliberate.** `gh`
  resolves which tracker `issue <number>` names from the checkout it runs in, so `repo` is a
  required argument there rather than an inherited cwd; the bare `#69` in its docstring is the
  worked example of the ambiguity and must stay bare. The module was `wlc_issue_edit.py` until
  2026-09-14, and dated records keep that name.

wlc-utils' own `doc/`, `in/` and `CLAUDE.md` were left alone — a bare `#NN` read there still meant
a wlc-utils issue, and qualifying those would imply they were ambiguous. Phase 10 of
`doc/PLAN-evacuate-the-rest-of-wlc-utils.md` then deleted that repo's `doc/` and `in/` outright
(2026-08-17), and their byte-identical copies live in **this** repo's `doc/` and `in/` — the six
`doc/` files that arrived 2026-08-12 (`agent-planning-principles.md`,
`edition-transcription-workflow.md`, `review-findings-2026-07-29.md`, `simanim-tanakh-signs.md`,
`PLAN-overall-port-to-python.md`, `PLAN-two-accents-on-one-chanted-word.md`) and the wlc trees
under `in/` (`in/accgram/edition_transcriptions/` above all) — still carrying bare `#NN` issue
citations that mean wlc-utils issues. Those files are one of the two standing exceptions to "a
bare `#NN` here means MAM-basics". wlc-utils' own rewritten `CLAUDE.md` keeps its
bare-`#NN`-means-wlc-utils note for the redirect host itself.

**UXLC-utils' two `doc/` files are the same exception, in this repository now.** The 2026-09-03
evacuation moved `doc/clc-design.md` and `doc/clc-skeleton-plan.md` to `uxlc/doc/`. A bare `#NN`
inside either file still means a UXLC-utils issue, and the citations remain unqualified because a
prefix would imply that the citation was ambiguous.

**holman-ketiv-qere needs no such exception, the first of the four evacuated repos to need none.**
Its `doc/` has two files and neither carries a bare `#NN`. Measured 2026-08-18, the only
`#NN` in any of its tracked prose was the `#19` its `CLAUDE.md` quoted once. The pages now share
the stem `gh-pages/holman/JC3 The Biblical Text in the JC Edition #19-Z` in this repository
(this said "quotes twice from the filenames" until the 2026-08-22 review's follow-up;
`git grep -c '#19' -- CLAUDE.md` there was 1), and that is a JC Edition article number
rather than an issue — one more instance of the bullet above, met in the repo whose tracker had
just been added.

**book-of-job needs no such exception either, and it goes further than holman-ketiv-qere does.**
Measured 2026-08-22, `git grep -nIE '#[0-9]+'` over its **whole tracked tree** returns nothing at
all — not in its `CLAUDE.md`, its `README.md`, its two `doc/` files or the three `.md` under
`py_ac_loc/`, and not in any of the 701 artifacts under `gh-pages/` and `out/` either. All **784**
files that repo tracks are free of `#NN` in every shape, issue numbers and hex colours alike, so
there is nothing there for a reader to have to disambiguate. **So the four evacuated repos split
two and two**: wlc-utils' `doc/` and `in/` copies and UXLC-utils' `uxlc/doc/` copies are the two
standing exceptions in this repository, and holman-ketiv-qere and book-of-job need none.
