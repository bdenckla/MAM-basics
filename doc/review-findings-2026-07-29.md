# Findings of the 2026-07-29 review of the week's committed work

State: acted on 2026-07-30

Filed as [#87](https://github.com/bdenckla/wlc-utils/issues/87), which is a thin pointer to this
doc. The review covered the range 80ca0df..0ab2c6a — the 91 commits of 2026-07-22 through
2026-07-29 — in four streams: the two new surveys (maqaf-nonfinal-accents and
chanted-word-accents), the printed-Decalogue pages, infrastructure/tooling, and tests. **All
file:line references are as of 0ab2c6a**; concurrent work has been moving the tree since, so
treat them as anchors, not gospel.

What the review verified and found sound is *not* recorded here (the pins all raise; every
rendered number re-derived from the committed JSON matched; the simtiq/simtan renames are pure;
the skip policy landed completely; the encoding and formatting hygiene of the new tooling is
clean). This doc holds only the actionable items. The pattern across the majors: each is a
quantifier or scope claim in rendered prose that the vendored data at the same HEAD contradicts,
and each is a sentence no pin defends. Everything pinned was right; everything wrong was
unpinned.

One check the review could not run: a full regeneration-and-diff of the tracked outputs
(concurrent work made in-place regeneration unsafe). Freshness was verified structurally instead
— every page module's HTML was committed at or after the module's last change, plus targeted
greps. Run the real regen-and-diff at the next quiet moment; item 19 below is one reason to.

## Major

**1. "Every strand has a meteg" on the joined לא — false against the vendored strands.**
`py/accgram/maqaf_nonfinal_accents_page.py:1020-1021` (the intro sentence 0ab2c6a itself added)
says the Simanim Tiqqun has a munaḥ on the joined לא of two compounds "where every strand has a
meteg." Two reviewers checked `in/accgram/printed_decalogue_teamim.json` independently and both
refute it: all four עליון strands have לא as a free chanted word with a munaḥ, and the two
Deuteronomy תחתון strands' joined לא of לא־יהיה has neither meteg nor accent. The same overclaim
is at `py/accgram/printed_decalogue_simanim_page.py:970` ("where all eight strands have a meteg
and no accent," about the לא of לא־תעשה), echoed in the `ROM_MUNAX` comment at
`py/accgram/printed_decalogue_strands.py:212-214` and the docstring at
`py/accgram/edition_transcription.py:55-57`. The existing `simtiq_lo_compounds` pin asserts the
meteg only for ws/ex/taxton/printed — the one strand where the claim holds. Fix: scope each
sentence to what that pin checks, or restate the per-strand facts; if any quantifier survives,
pin it. Note the corrected facts also *reopen* an observation the current wording forecloses:
the Simanim Tiqqun's munaḥ on the joined לא is exactly the mark the עליון strands have on their
free לא, the same possible carry-over shape the intro already names for Koren.

**2. The maqaf-nonfinal page's pair-table wording claims a corpus scope the survey cannot see.**
The survey counts a compound only when an accent sits on a *non-final* atom, so a pair whose two
accents both sit on a compound's final atom is invisible to it. The rewritten hover ("On a
compound chanted word") and the appendix wording ("These are the pairs that occur on a
compound"; "These pairs occur … on a simple chanted word only") state corpus-level facts — and
`out/accgram/chanted-word-accents.json` at the same HEAD contradicts them: final-atom compounds
exist for six of the ten "simple only" pairs (azla-geresh 27, merkha-tevir 8, qadma-merkha 3,
qadma-mahapakh 2, qadma-darga 1, munaḥ-revia 1), and roughly 414 munaḥ-zaqef final-atom
compounds stand against the compound count of 1 the hover shows for that pair. The colon-clause
— "no compound has one of them with its first accent on a non-final atom" — is the true
statement. Fix: retreat the headline wording to the non-final-atom criterion everywhere the
scope is stated, in `py/accgram/maqaf_nonfinal_accents_page.py` (rendered at
`gh-pages/accgram/maqaf-nonfinal-accents.html:27-29,47-48`).

**3. The newer survey's findings were not propagated back into the older survey's labels and
pointers.** Two instances, both recorded in `doc/PLAN-two-accents-on-one-chanted-word.md` §7-§8
and acted on nowhere else:
- `py/accgram/maqaf_nonfinal_accents.py:152` still labels the four merkha-before-silluq hits
  "secondary merkha in the silluq's chanted word (ITM §233)" in the tracked
  `out/accgram/maqaf-nonfinal-accents.json`, although the plan records that §233 is tipeḥa-only
  and the chanted-word survey's `mam_residue` counts merkha-silluq among the sequences no Yeivin
  section names. The comment arithmetic at `maqaf_nonfinal_accents_page.py:1149-1154` ("every
  one but merkha before pashta") leans on the wrong citation; the rendered "Most" happens to
  survive (six of eight pairs genuinely covered), so the fix is the JSON label and the comment.
- Plan §8 concludes issue #82 is the wrong issue for the citation question (its real subject is
  Yeivin's Deut 33 maqaf readings), yet `py/accgram/chanted_word_accents.py:1012` still emits
  "Issue #82 holds the citation question" into the tracked JSON, and
  `py/accgram/maqaf_nonfinal_accents.py:141` still cites "(issue #82)" for the §253/§241
  corrections. Fix: open the correct issue, repoint both, regenerate.

**4. The Koren page's cross-page promise went stale when the maqaf survey was narrowed to
MAM.** `py/accgram/printed_decalogue_koren_page.py:670-679` still promises that the linked
survey page "answers both" questions — how rare the kept accent is across Tanakh, and whether
any text has the same shape in the same surroundings — including a manuscript's precedent. After
the narrowing (4bc2d7f, f9d966d) that page mentions no manuscript and no WLC, and its MAM-only
answer ("there is not") now sits beside the Koren page's "Koren is not doing something unheard
of" as an apparent contradiction, unless the reader supplies the MAM-vs-manuscript corpus
distinction the survey page no longer draws. The precedent fact itself is still true of the
survey JSON — wlc422 has munaḥ on both atoms at 1 Chr 27:14 and 2 Chr 1:11 — but is now stated
nowhere rendered and pinned by nothing. Fix: reword the sentence to what the survey page now
answers, and either state-and-pin the manuscript precedent somewhere or drop the claim.

**5. The worktree cleanup silently destroys gitignored files while claiming it cannot destroy
work.** `_is_dirty` (`py/cmn/git_worktree_cleanup.py:233-238`) uses `git status --porcelain`,
which does not list ignored files, and `git worktree remove` without `--force` checks the same
way — so a clean, merged, idle worktree with gitignored content (a `.novc/` report, say) is
removed with that content, silently. That makes the docstring's stakes claim at lines 65-67 ("a
clean, fully-merged worktree holds nothing that does not also exist in the repo") and
`py/main_repo_maintenance.py:29-31` ("Unlike step 1 this one cannot destroy work") both false
for exactly this class of file — and the module's own header cites a destroyed `.novc` survey as
its cautionary tale. Everything else about the tool verified as genuinely conservative (six
independent spare conditions, `branch -d` never `-D`, `claude/`-prefix-only deletion behind its
own ancestor check, no `--force` anywhere). Fix, either level: correct the two docstrings
(minimal), or check `git status --porcelain --ignored` and spare-with-reason (or at least
report) a worktree with ignored content.

## Minor — rendered prose and page modules

**6. Two agentive verbs survive by line-splitting.** "There too Koren shows the p-trad"
(`py/accgram/printed_decalogue_koren_page.py:723-724` — subject and verb on different source
lines, invisible to the lint's subject-anchored patterns) and "the seven chanted words before
those marks carry four revia…" (`py/accgram/printed_decalogue_page.py:1453` — plural subject
escapes the singular pattern). Fix the two sentences; item 20 covers the lint side.

**7. Hover titles show raw mb_cmn book names** — "Levit 21:4", "Deuter 8:16", "Tsefaniah 2:15",
"2Chronicles 8:11" (`gh-pages/accgram/maqaf-nonfinal-accents.html:32-36,55-74`). The
name-fixing went out with `_case_table`, whose removal comment
(`py/accgram/maqaf_nonfinal_accents_page.py:621-624`) wrongly says the case tables were "the
only thing that ever needed a book name out of a bcv" — `_hebrew_at`'s titles need one too.
Restore a shared name-fixing path and correct that comment.

**8. "KorTan/SimTiq" shorthand in rendered prose** on the uvinkha page's group intro
(`gh-pages/accgram/printed-decalogue-uvinkha.html`). The conventions reserve the short forms
for code; rendered prose wants "the Simanim Tiqqun." Mild — the shorthand is glossed inline at
first use — but out of step with every other page.

**9. The `printed_decalogue.py` docstring restates a derived tally, imprecisely.** "Eleven of
the twelve transcribed Decalogues match their Wikisource strand at every chanted verse" (~line
33): three of the eleven have token divergences; what eleven share is their strand's *verdicts*.
Replace with a pointer to the hub page's derived tally rather than a second statement of it.

**10. A stale comment lead survived the fb3e5cc rename.** The U+0598 comment in
`py/accgram/maqaf_nonfinal_accents.py` (~line 170) still leads with "a tsinnorit beside a
tsinnor" for a prose context, though it goes on to gloss correctly. Align it with the
zarqa's-stress-helper wording the sweep gave the other modules.

## Minor — survey data and JSON

**11. U+05A2 is missing from `_ACCENT_SHORTHAND`** (`py/accgram/maqaf_nonfinal_accents.py:199-230`),
so `shape_of`'s fallback leaks a bare combining mark (ATNAH HAFUKH) into tracked JSON keys — the
uxlc and mam_simple poetic `simple_by_pair` have keys of the form "mark-ole" and "mark-ole-mer"
whose first element is the raw orphan codepoint, against both the module's ASCII-shorthand
design and the repo's no-orphan-combining-marks rule. (The page would KeyError if it ever
rendered them — at least a loud failure.) Add the shorthand.

**12. `_pair_rows` truncates a three-accent key silently.** `pair.split("-")[0],
pair.split("-")[1]` (`py/accgram/maqaf_nonfinal_accents_page.py:366-368`) would render a
three-part key truncated rather than raise, and three-part keys demonstrably occur in the
poetic data (germ-mer-rev, tsit-mah-rev). The page's "but never more than two" is likewise
pinned for compounds only. Make the split raise on len != 2, and pin the never-more-than-two
claim for simple chanted words too.

**13. Unpinned numbers in a docstring.** `py/accgram/maqaf_nonfinal_accents.py:49-53` states
"21 free ואחרי" and "all six free שלף" with no regeneration path — the exact shape the
verification rules forbid. Replace with pointers into the JSON, or pin them.

**14. `simtiq_lo_compounds` dedups its two sites away.** The matches are collected into a set,
and ws/ex/taxton/printed has *two* byte-identical לא־תעשה compounds (Ex 20:4 and the Sabbath
20:10), which dedup to one, so `assert len(found) == 1`
(`py/accgram/maqaf_nonfinal_accents_page.py:750-757`) passes without distinguishing the sites.
Collect a list (or count occurrences) so the assert says what it appears to say.

**15. `_ONE_ACCENT_WRITTEN_TWICE` is genre-blind.** The {U+0598, U+05AE} exclusion and its "one
accent written twice" label are correct for prose verses only; in a poetic verse the same two
codepoints are the genuine tsinnorit and tsinnor. It happens never to fire on poetic data at
HEAD, so no output is mislabeled — add a genre guard or an assert so that stays true by
construction rather than by luck.

**16. `atom_accents` counts any U+05BD in a verse-final chanted word's last atom as silluq**, so
a hypothetical verse-final atom with only an early meteg would miscount. The chanted-word token
survey's rule (silluq only immediately before sof pasuq) is the correct one of the two; align
the maqaf survey with it. Theoretical today.

**17. Empty-qere placeholders (`**qq`) count as chanted words** in `scan_corpus` totals — a tiny
denominator inflation, JSON-only. Exclude them.

**18. `ctr_decalogue.compare` is blind to strand-only words.** On a difflib "insert" opcode,
only CTR-side words become diffs (`py/accgram/ctr_decalogue.py:319-322`), so a strand word CTR
lacks would go unrecorded. Currently moot — the pinned counts match 142/142 and 164/164 — but
the function under-reports in exactly the direction a future re-vendor would care about.

## Minor — the prose lint

**19. The lint never scans committed artifacts.** `_scan_targets`
(`py/tests/test_prose_conventions.py:143-152`) walks only `py/**/*.py`; gh-pages HTML, out/
JSON, and doc/*.md are never linted, so a swept module leaves its committed rendering stale
silently. Demonstrated in-range: the #80 sweep (2026-07-27) left `out/accgram/dual-cant/
_dual_cant.json` stale until f0dbbc0 (2026-07-29) noticed by hand. Either extend the scan to
the committed artifacts, or add a freshness check tying each page module to its rendering — or
accept that the regen-and-diff is the only guard and say so in the lint's docstring.

**20. `_SUBJECTS` hardcodes edition names**, so a future rename (as simanim→simtiq/simtan
happened in-range) silently *narrows* the lint instead of breaking it
(`py/tests/test_prose_conventions.py:79-93`). Also the two line-split escapes of item 6: worth a
note in the lint's docstring even if the patterns stay as they are, so the gap is a recorded
choice rather than an unknown.

## Minor — tooling

**21. `issue_edit`'s `gh` calls resolve the repo from the process cwd** — no `-R` flag, no
`cwd=repo_paths.repo_root()` (`py/issue_edit.py:66-74,103-108`) — while everything else in the
module is repo-root-anchored. Run from another repo's directory, it edits that repo's issue of
the same number. Anchor the subprocess calls.

**22. `repo_paths`' failure message names the wrong "beside".** "Clone {name} beside
{repo_root()}" (`py/repo_paths.py:107`) names the *worktree* root in precisely the worktree case
the module exists for; the two env overrides in the same message are the real fix, so the advice
is recoverable but wrong. Name the siblings root it actually searches.

**23. Duplication is creeping back into the transcription tooling.** `transcription_check.py`
keeps a private `_pages_of` (lines 67-69) and re-inlines the stem-label extraction (line 82)
beside the public `pages_of`/`page_label` that `transcription_build.py:67-74` exports — the
drift class ebc3ac5 was killing. `scan_page.py:50-64` and `transcription_editor.py:62-112`
share verbatim `SCANS`/`OUT` constant blocks and a copied `_take`, and both hand-roll argv
parsing while `transcription_build` uses argparse. Consolidate.

**RESOLVED, in two unrelated passes.** The `_pages_of` and stem-label half went in `2aa40c8`,
before and independently of the entry-point work. The argv-vs-argparse half went with the move
to a single entry point (`33b850d` and the phases around it): all five modules now expose
`add_args`/`run` and are subcommands of `py/main_edition_transcription.py`, so there is one
argparse and no hand-rolled `sys.argv` scanning left. `SCANS`/`OUT` are now `scan_page`'s alone
and `transcription_editor` imports them; the copied `_take` is gone.

**24. `scan_page --name` with multiple page arguments silently overwrites.** Every page is
written to the same `<STEM>.png`, last one wins (`py/accgram/scan_page.py:91-92`) —
contradicting the flag's stated purpose of preventing overwrites. Error out on the combination.

**25. `scan_page`'s docstring still advises opening the output** "in Claude's Browser pane, or
PowerShell `Start-Process`" (`py/accgram/scan_page.py:16-20`), against the 2026-07-28
hand-a-`file:///`-link-and-open-nothing rule; the range edited this docstring without touching
that advice. Update it.

**26. Two small `transcription_editor` items.** With exactly one transcribable row the JS
`PITCH` is 0 and the entry field lands on the line it is transcribing (lines 590-591, 614) —
the failure the placement comment says it avoids; bites only the single-line crop that
`detect_margin` explicitly supports. And the bottom-clearance gate's comment (lines 326-327)
overstates: a stub the min-height filter dropped never reaches `crop_warnings`' band list, so
the smallest-stub case stays silent (vs. lines 347-351).

**27. The worktree cleanup resets the clock it reads.** `_is_dirty`'s `git status` refreshes
the index mtime `_seconds_since_activity` stats, so on a second maintenance run inside the grace
hour, dirty or unmerged worktrees are reported "git activity N min ago; may be in use" —
conservative direction, misleading reason. Also `_sweep_empty_dirs` keys off the *running*
checkout's `.claude/worktrees`, so husks in the main repo are not swept when the tool runs from
a linked worktree. Both cosmetic.

**28. `transcription_check.py:58` reconfigures stdout at module import time** — a side effect
`test_edition_transcriptions` now inherits by importing it. Pre-existing, not introduced this
week; move it into `main()` per the repo's own convention.

**RESOLVED.** The equivalent import-time `stdout.reconfigure` in `zoom_line` went in
`aa09ede`, and all five transcription modules now leave stream setup to
`py/main_edition_transcription.py`'s `force_utf8_io()`, called from its `if __name__` block.
Importing any of them has no stream side effect.

**29. Cross-module use of private members.** `transcription_parse.py:107,141` reaches
`et._ALIASES` and `et._split_on_joiners`; `transcription_check.py:143-144` reaches
`et._normalize`. Promote them to public names or move them where both callers can own them.

## Minor — tests

**30. Byte-exact rendered-sentence pins already paid the predicted cost.**
`test_the_verdict_column_says_one_of_three_things_and_the_right_one`
(`py/tests/test_edition_transcriptions.py:1249-1270`) pins three rendered English sentences
byte-exactly; ac432df had to rewrite nine "Wikisource strand" lines in this file during a
wording sweep *within the same week the test was written*. Derive the expected strings from the
generator's own constants, or pin the decision (which of three verdicts) rather than the prose.

**31. The example-based bands — decide bless-or-prune.** Per the testing rule these are the
forbidden third shape, reviewer-overridable: `py/tests/test_repo_paths.py` (its `require_*`
failure-message tests are the best-justified, protecting the fail-loud mechanism),
`py/tests/test_issue_edit.py` (line 46 pins a literal filename), the shorthand-adapter band in
`test_edition_transcriptions.py` (lines 528-612, 749-813), the synthetic-image tests in
`test_transcription_editor.py`, and one straggler in `test_ctr_decalogue.py` (line 205,
hand-built HTML string). Several encode real once-broken cases. Nothing to fix mechanically —
this item exists so the exception is a recorded decision, one way or the other.
