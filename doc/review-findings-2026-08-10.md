# Findings of the 2026-08-10 review of the work since 2026-08-03

State: acted on, verified 2026-08-18

Filed as [#228](https://github.com/bdenckla/MAM-basics/issues/228), which is a thin pointer to
this doc. The review covered **every clone directly under `~/GitRepos`** — commits from
2026-08-03T23:00 (the previous review's cutoff) through 2026-08-10, about 217 commits across 20
repos with activity, re-measurable per repo with `git log --since=2026-08-03T23:00 --oneline` —
plus the in-window issue activity in the trackers that had any (MAM-basics #218–#227,
MAM-private#1, masorah-books #16/#18/#19, al-hatorah #126/#127, wlc-utils #11/#15/#48/#86/#90,
trope#129). It ran in three streams: MAM-basics reviewed directly; MAM-private; the remaining
repos in two windows (2026-08-07→10, then 2026-08-04→06 — see the next paragraph for why two).

The previous review is `doc/review-findings-2026-08-03.md` (#219), acted on 2026-08-04. **This
review's first pass took 2026-08-07 as its baseline, which was wrong by three days.** Asked for
"an overall review of all work since the last such review," the session searched session
transcripts for that phrase, found nothing, and declared no record of a previous review existed —
without ever globbing `doc/review-findings-*.md`, the very filename this series declares
authoritative, and without searching the issue trackers. Ben's correction of 2026-08-10 ("Can you
look harder? Did you look in GitHub issues?") pointed at the record, and the 2026-08-04→06 span
was then reviewed as a second pass. The auto-memory directory now holds a pointer
(`project-review-series.md`) naming both lookups, so a future session finds the series before
choosing a baseline.

Anchors: HEADs at review time were MAM-basics `204aa93` (plus `2168ee1` and `0a3eb1a`, committed
on main during the review by the live al-hatorah R.2 session), MAM-private `dbd7385` (plus
`b0aa6b1`, likewise), wlc-utils `79404fa`. Three sessions were live while the review ran (the
al-hatorah R.2 evacuation phase, the breuer-cos cleanup, and the review itself), so working trees
were ignored everywhere: this is a review of **committed work only**, per Ben's ask. Two checks
the review did not run, the same limitation all three reviews in this series have recorded: a
full regeneration-and-diff of tracked outputs (live sessions make in-place regeneration unsafe),
and any judgment of in-flight work — in particular **the al-hatorah evacuation gets no verdict**:
R.0–R.2 are committed and clean, R.3/R.4 had not started, and the next review owes it one.

## What the review verified and found sound

The completed evacuations' arithmetic re-derives exactly: wlc-utils-private 87 files at
MAM-private `9263074`, 86 at HEAD with the NFC lint's promotion accounting for the difference,
and 99 + 1 breadcrumb = R.4's 100 commits; mgketer 5,225 files at `0796411` with exactly
`test_h_dot_below_nfc.py` deleted since, and the commit-count chain **closes at 557 on
`bdenckla/mgketer` today** — 555 content-history commits + the breadcrumb commit `cf40ce72` +
the later `.gitignore` removal `22bdc73b` — dissolving the 555-vs-556 discrepancy this review at
first suspected between the R.3 and R.4 records (the two figures count different things and both
are right); masorah-books 174 files exact; al-hatorah R.1's 1,559 and the 7,049-entry index
exact. No accidental commits anywhere in MAM-private: all modes 100644, no venv or cache files,
largest blob a legitimate 6 MB WLC input.

The suite: **904 passed, 5 skipped** at `2168ee1`, matching `ca24e15`'s stated count, with the
whole in-window chain (915 → 910 → 902 → 903 → 904) closing against the culls and additions that
moved it; all five skips are `test_edition_transcriptions.py`'s semantic channel, none
environmental. `black --check` clean over all 771 files. The vendoring audit in sync at
`36b9475` (22 rows over 154 files, the 20 remaining DIFFERS all pre-existing and named).

The cross-repo sweeps are complete and byte-verified: the licence bump's LICENSE.md is
blob-identical (`51094ac`) in MAM-parsed, MAM-simple, MAM-with-doc, MAM-OSIS and MAM-for-Sefaria,
with MAM-OSIS also reconciling `header.xml` with `mapm.conf`; the re-vendored
`mb_cmn/str_defs.py` is blob-identical (`4c76029`) in its four repos, and `template_names.py`
byte-identical in all three destinations of the 2026-08-09 re-vendor; the LF `.gitattributes`
sweep's base rule is identical everywhere it landed, github-misc's `-text` exception exactly
covering its three upstream `.lisp` files; the live `~/.claude/CLAUDE.md` and all four
hebrew-prose skill files are byte-identical with github-misc's tracked copies.

Every closure of the 2026-08-03 review's findings matches that doc's account of it (majors 1–5,
minors 7–15, the three decision items), and the closure commits' artifact counts re-derive:
fix-tester "92 confirmed, 1 denied, 0 changed, 0 untestable", grammaticality 18,629 clean / 96
ungrammatical, ne 9:20 crossing OUT→IN as #218 predicted. In the 2026-08-04→06 span,
codex-index-cam1753's mark-order chain re-derives exactly (94 tracked files; 15 → 3 → 0 words in
the wrong order across `a44fa8c` → `912363b` → `261434f`), and applying `give_std_mark_order` to
the parent pages reproduces phonetic-hbo `cdbb8f91`'s four regenerated Yeivin pages
codepoint-for-codepoint.

Beyond the checks, the window's record-keeping held up under adversarial reading: failed
predictions stay in the maintenance plan with dates, corrections land as new commits rather than
rewrites (`4549cf2` re-deriving what `ca5fea5` got wrong, with the re-establishment commands in
the message, is the model of the form), and nearly every figure in a commit message re-derives
from the tree it commits — which is what made this review checkable at all.

## Findings

In rough order of consequence. Nothing reaches the previous review's "major" band: the review
found **no wrong code, no wrong data and no broken artifact** in the window.

1. **#219 is open with nothing left in it.** All fifteen of its items are recorded as acted on
   (2026-08-04, in this repo's `bca9561`/`4e0f30f` and the doc's "How the review was acted on"
   section), and its predecessor wlc-utils#87 was closed at the same stage. Close it, or record
   in it what is deliberately held open.

2. **The user-level CLAUDE.md still says "MAM-basics runs 320 tests"** (the "No `sys.path`
   surgery" section, line ~251; canonical copy `github-misc/dot-claude/CLAUDE.md`). The suite
   runs ~904; `52208c0` corrected the same stale figure in `doc/metsudah-vs-ctr.md` on
   2026-08-07 but the global file kept it. A task chip was put up during the review.

3. **The window's wrong statements are all sweeping negatives — three of them.** `df3d6e7`'s
   message ends "No sibling repo changed" and the vendoring audit showed eight DIFFERS rows an
   hour later (recorded in `46621c7`, resolved in `bbf600b`); `46621c7` in turn mis-attributed
   the `provenance.py` drift to `df3d6e7` when it came from `aa5e4f6` (corrected in al-hatorah
   `c4f0e48a`); `ca5fea5`'s "nothing is broken and nothing needs undoing" was cleared by a check
   against the wrong object, and `4549cf2` established that origin/main had a NameError on the
   survey's main path for five minutes. Each self-corrected within the window, and the positive
   counts all held — the counts have oracles now, which was the previous review's ask. The
   pattern worth carrying forward: **a sweeping negative is a claim too, and wants the command
   that establishes it in the message** ("the audit was re-run and reports no DIFFERS"), or it
   wants not to be made.

4. **Two prose-rule slips in about 217 commit messages**: `0d23f0e` writes "the latter", and
   wlc-utils `e0abcc5` writes "reads a legarmeh in the one and not in the other" — both
   constructions the user-level CLAUDE.md bans. Nothing to do (no history rewrites); recorded as
   the window's full count of that class.

5. **Ten of MAM-private's 44 commits lack the `Co-Authored-By: Claude` trailer** (`e888dae`,
   `0796411`, `1d1bd76`, `f777afa`, `8ee5d0a`, `bdb9fc7`, `f3f6d3b`, `13b87ce`, `c75f4b7`,
   `fc6a133`), clustered in the mgketer-phase sessions. Convention slip only.

6. **Pillow deprecation with a date on it**: `py/accgram/transcription_editor.py:177`'s
   `column.getdata()` warns four times per suite run; Pillow 14 removes it 2027-10-15. A task
   chip was put up during the review.

7. **Five record gaps, all cosmetic, none touching content**: the mgketer stale-prose census
   missed `mgketer/CLAUDE.md:258` (a third absolute-path site of exactly the class it
   documented); the mgketer R.2 record says `git status` "listed only the eight source files
   R.2 itself edited" where the listing would have shown nine paths (the deleted tree lint is
   the ninth); MAM-simple `69f8562`'s "every Hebrew token in both files … appears verbatim in
   xml-vtrad-mam" is false for six unpointed terminology words, unavoidably, a pointed corpus
   holding no unpointed letter runs; phonetic-hbo `cdbb8f91` lists §334 among its regenerated
   sections where its source commit al-hatorah `fb1af0d0` names no `sec_334` file (the §334
   change comes through the substitutions file, which the message never says); and cam1753
   `912363b`'s "have not been revisited" comment about the Ps 18 entries was outrun minutes
   later by `261434f`'s mark-order pass over their bytes.

8. **A churn risk to watch, not a defect**: codex-index-cam1753's `e5b2ae4` normalized `cam1753-page-index.json` to LF under the new `.gitattributes`; if the tool that
   writes that file emits CRLF, the next regeneration shows line-ending churn.
   codex-index-aleppo's `*.csv eol=crlf` exception is the fix shape if it recurs.

## How the review was acted on (2026-08-10, the same evening)

All three actionables closed the day the review was filed, each verified rather than trusted:

- **Finding 1** (#219 open with nothing left): closed on Ben's instruction, with a comment
  citing this doc.
- **Finding 2** (the stale test count): Ben ran the task chip; github-misc `5e6234d` and
  `47dcfdb`. The live `~/.claude/CLAUDE.md` now says "~900 tests (as of 2026-08-10)", the
  tracked copy is byte-identical (`fc /b`), both commits pushed. The chip also scoped the
  registry-check paragraph to holman-ketiv-qere, MAM-basics no longer having a registry.
- **Finding 6** (the Pillow deprecation): Ben ran the task chip; MAM-basics `7033f94`, the
  one-line `getdata` → `get_flattened_data` change in `row_profile`. The 23
  transcription-editor tests pass with the deprecation warnings gone.

Findings 3, 4, 5 and 7 recommend no work (practices going forward, immutable messages, cosmetic
records); finding 8 stays a watch item for cam1753's next page-index regeneration.

## Open ends the window itself declares (not findings)

The al-hatorah evacuation's R.3/R.4, running or queued as this doc is written. MAM-basics #225,
#226 and #227, filed in-window and open. The scan-pages undertaking at Phase 0
(`doc/PLAN-scan-pages.md`). cam1753's unchecked 0105B column 1 link and its still-pointed Ps 18
entries (deliberate, `912363b`). The two task chips named in findings 2 and 6.
