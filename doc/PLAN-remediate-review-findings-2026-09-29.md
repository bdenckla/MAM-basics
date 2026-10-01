# Remediate the September 29, 2026 dual-agent review of MAM-basics

State: live; approved for execution 2026-09-30; remediation not started.

Prepared by Claude on 2026-09-30, New York time, as close-out step 2 of the round, in two sessions.
The first drafted this plan from a handoff prompt that the close-out step-1 session prepared that
day and Ben pasted in. That prompt records one decision of Ben's: after answering the close-out
package's six questions, he answered "Do you approve the proposed fixes, deferrals, and no-action
dispositions?" by selecting "I approve". The rest of it is that session's reconstruction of the
handoff. When Ben asked the first session to wrap up, it wrote a second handoff prompt, which Ben
pasted into the second session; that prompt quotes his instruction "Wrap up and perhaps provide a
new prompt for a new session." and is otherwise the first session's reconstruction. The second
session corrected, re-verified and committed the plan. Neither session attributed a
reconstruction's facts to Ben; each checked them. The review's live update,
[`dual-agent-review-2026-09-29-turn-01-claude-update.md`](dual-agent-review-2026-09-29-turn-01-claude-update.md),
records the package, Ben's answers and this plan's preparation, under "Review closed; complete
disposition package proposed, 2026-09-30", "Ben's decisions and approval of the package,
2026-09-30" and "Detailed remediation plan prepared; approval pending, 2026-09-30", the entry
committed with this plan.

The dispositions are approved. On 2026-09-30 Ben also approved this plan's concrete editorial
wording and its execution, as [the periodic-review procedure](periodic-review.md) requires in
"Close-out: from findings to dispositions" and "Separate defects from editorial proposals" (D7),
with the choices item 5 of "Decisions this plan follows" lists. Preparing, committing or approving
this plan implemented none of its changes. The approval authorizes the stated repairs, including
the consumer notice of the 24 MAM-parsed plus files and the five product licence files, and selects
no deferred semantic or policy choice.

Line numbers are those of the planning tree, `bcbbb1dc`, where every cited passage was re-measured
on 2026-09-30; a passage's own quoted words, not its number, identify it. Two archive commits recur,
and links to them are written here in shorthand:

- `F/` stands for `https://github.com/bdenckla/MAM-basics/blob/f72297084ab94aea6fd1274dc1bc3d7ce6acddd5/doc/`,
  the last commit holding the complete families that `2a051ba5` retired;
- `E/` stands for `https://github.com/bdenckla/MAM-basics/blob/eea4c583f12ee90f75003dd4c75be5d6d52f7c85/doc/`,
  the last commit holding the complete families that `e4934b6e` retired.

Write each such link out in full, and check its path first with `git cat-file -e <commit>:<path>`.

Two merges of `origin/main` into the review branch after the planning tree, `23f96667` and
`02a20154` on 2026-09-30, moved passages this plan cites in five files without changing their
words: `doc/dual-agent-review.md` (E1's paragraph now begins at `:151`, finding 34.1's sentence is
at `:178–179` and finding 35's paragraph at `:345–347`), `doc/periodic-review.md`,
`dot-claude/README.md` (`:61` and `:90–91`), `py/main_repo_util.py` (`:50–51` and `:592–597`) and
`py/repo_util/user_config_sync.py` (`:209` and `:212–213`).

## Standalone executor contract

**Checkouts.** The development checkout is the full clone `C:/Users/BenDe/GitRepos2/MAM-basics`, on
its local carrier `dar-2026-09-29` for the shared branch `origin/dar-2026-09-29`. Phase 1, finding
30 alone, runs in the full clone `C:/Users/BenDe/GitRepos/MAM-basics`, which holds the untracked
proposal that phase reads. The integration checkout is the development checkout switched to `main`.
Under D11 (`doc/dual-agent-review.md`, "The shared origin branch"), another verified full clone may
serve as the development and integration checkout; then substitute its path throughout, while phase
1 still runs in `C:/Users/BenDe/GitRepos/MAM-basics`. Create no linked worktree for this work:
phase 1 must run in the clone that holds its checkout-local input, final integration and the
`--sync-user-config` deployment must run in a full clone, and one full clone for every other phase
keeps the work to one checkout and one chain of pushes. The root executor owns final integration.
Only one agent writes at a time, across both checkouts; read-only sub-agents may investigate and
check.

**Baselines.** Before any edit, require these commits to be ancestors of `HEAD`, checking each with
`git -C <checkout> merge-base --is-ancestor <commit> HEAD`:
`1dec120315990707cb1ff66d06d55dc0cfab43ce` (the package), `bcbbb1dc8199317b6bf9c9a6bfb430019b1f5374`
(Ben's decisions on it), and the commit that adds the live update's entry recording Ben's approval
of this plan (find it with
`git -C C:/Users/BenDe/GitRepos2/MAM-basics log --format="%H %s" -- doc/dual-agent-review-2026-09-29-turn-01-claude-update.md`).
Record the development checkout's path and the exact `HEAD` at which editing begins in the
implementation entry that "Records" below describes. The reviewed window, `f4d81285..7549ebf7`, is
a historical anchor, not a baseline.

**Interpreter.** In each full clone, that clone's own `./.venv/Scripts/python.exe`, run from the
clone's root. Never copy or link an environment.

**Instructions and skills to load first.**

1. `AGENTS.md`.
2. `doc/periodic-review.md`: "Close-out: from findings to dispositions", "Verification cadence
   during remediation", "Separate defects from editorial proposals" (D7) and "Present remediation
   by public-facing risk".
3. `doc/dual-agent-review.md`: "The shared origin branch" (D11) and "Review filenames and State
   lines".
4. `iterative-document-editing`: "Executable plans", "Finished receipts and maintained documents"
   and "MAM-basics and MAM-private State conventions".
5. `hebrew-prose`, with its references `core-rules.md`, `terminology.md`, `rendered-prose.md`,
   `mam-basics.md`, `sources-and-corpora.md` and `verifying.md`.
6. `mam-repository-topology`, with `references/repository-maintenance.md` (findings 7 and 34.1)
   and `references/evacuated-repositories.md` (finding 28.3).
7. `hbce-psalms/README.md`, which `AGENTS.md` requires before touching `hbce-psalms/`,
   `py/hbce_psalms/` or `py/main_hbce_psalms.py` (findings 20, 21 and 28.6 and item 36.10).

Load `github-issues` only if an edit comes to cite an issue; this plan performs no issue operation.
Edit only the canonical copies under `dot-claude/` and `dot-Codex/`, never a live deployed copy.

**Before every edit phase**, verify with separate commands, each naming the exact checkout with
`-C`: `git rev-parse --show-toplevel`, `git rev-parse HEAD`, `git branch --show-current`,
`git status --porcelain=v1 -z` and the ancestry checks above. Stop on unexpected `HEAD` movement,
another writer's files, missing source material, a refused push or an unexplained generated diff.

**Not authorized:** amending, rebasing, force-pushing, resetting, dropping a stash, discarding work,
deleting a branch or worktree, retiring or reclassifying a document, any GitHub issue or Wikisource
edit, running `py/main_mam4sef.py`, `py/main_mam_osis.py` or `py/main_hbce_psalms.py compare`,
running the forest synchronizer's write form, reading MAM-private beyond what the suite and the
mega's documented steps read (`py/tests/test_final_stress_vs_phonetic_mam.py` reads its Phonetic
MAM), and editing a live deployed instruction or skill.

**At the start of every task that executes part of this plan**, as D11 requires, in the
development checkout: fetch `origin` (`git -C <checkout> fetch origin`); switch to the carrier
(`git -C <checkout> switch dar-2026-09-29`, or
`git -C <checkout> switch -c dar-2026-09-29 origin/dar-2026-09-29` if the clone has none) and
fast-forward it with `git -C <checkout> merge --ff-only origin/dar-2026-09-29`; merge current
`origin/main` into it with `git -C <checkout> merge origin/main`, resolving any conflict there; and
push any commit the merge made with `git -C <checkout> push origin HEAD:dar-2026-09-29`. A clean
merge of `main`'s own changes owes no suite or mega. Re-measure any passage this plan cites in a
file changed since the planning tree, `bcbbb1dc`, whether by this merge or an earlier one;
`git -C <checkout> diff --stat bcbbb1dc HEAD` lists those files. **A task that ends before final
integration** pushes its last commit
the same way and switches the full clone back to `main` (`git -C <checkout> switch main`), as D11
requires of a full clone.

## Decisions this plan follows

1. **Ben's package approval, 2026-09-30.** He selected "I approve" for the package committed at
   `1dec1203`, after selecting these options for its six questions. As the live update records, the
   option labels and descriptions are the close-out session's wording; Ben's part is his selection
   of each:
   1. Question 1, finding 11: "Keep all five", an exception for all five stub test ids.
   2. Question 2, item 36.2: "Allow the lag (Recommended)": `AGENTS.md` and `py/product_scopes.py`
      are amended so that a MAM text refresh does not oblige rerunning the MAM-for-Sefaria and
      MAM-OSIS generators; a change to their code still does.
   3. Question 3, finding 32: "Rule names the default (Recommended)", with no code or machine
      change.
   4. Question 4, finding 33: "Home clone stays ff-only (Recommended)".
   5. Question 5, finding 8.2: "In the hebrew-prose skill (Recommended)", widening its
      description, with conforming edits proposed here.
   6. Question 6, item 36.1 with finding 10.1: "Restore an explicit grant (Recommended)" in the
      five product licence files.
2. **Ben's planning answers, 2026-09-30.** While this plan was being drafted, three gaps in the
   package went to Ben in one dialog. The questions, option labels and descriptions were the
   drafting session's wording; Ben's part is his selection of each:
   1. For the conforming edits of question 5, he selected "Maintained prose (Recommended)" rather
      than "Also generated pages, data" or "Only question 5's list". So question 5's listed sites
      and the other maintained Markdown, docstrings, skill text and tool messages change, while the
      generated Holman UXLC-corrections page, the generated goerwitz page and the Evr. II B 55 page
      index's note, which the second option would have changed, stay as they are, and the new skill
      section names them as not yet swept. This plan adds, for approval, three more places left
      as they are: the note that the mega step `py/main_estimate_uxlc_locations.py` writes into
      `holman/data/uxlc_atom_locations.json` from its `NOTE` constant (`:59–68`), the introduction
      of the same generated Holman page, and the row label of the generated WLC a-notes
      full-record pages. It also adds the maintained sites that checks after that answer found
      beyond its description's list, each marked below "found after the planning answer".
   2. For sites with the same defect as an approved item but not named in the package: "Include,
      flagged (Recommended)". They are in "Sites found while planning", below, each for approval.
   3. For an in-place correction of an open update file: "Dated entry per file (Recommended)".
      Each such file gains one dated entry that identifies each corrected passage by its own words,
      former and new. Item 36.3's general policy question stays deferred.
3. **Wording already approved or prescribed, followed without asking again.**
   1. Finding 2.1: the replacement that `doc/PLAN-remediate-review-findings-2026-09-26.md` gives
      under "Historical links and retained manuscript labels" (the paragraph beginning "Finding 3.1
      replaces"), whose wording Ben approved on 2026-09-28.
   2. Finding 2.4's "folio 57a": that plan's substitution of "page 57a", in its table under
      "Formatting, source links and caption locators" (row "EVR, 1 Samuel 17:5"), which it applies
      to the snips README where the locator occurs.
   3. Finding 9.1: the recorded form `State: open, first entry <date>.` (`iterative-document-editing`,
      "MAM-basics and MAM-private State conventions").
   4. Finding 1.1: the notice order that `doc/PLAN-remediate-review-findings-2026-09-26.md`
      prescribes under "Distributed data and published change-log effects": "In both notices, move
      the existing NARPAS definition before WHITESPACE so the abbreviation is defined before use;
      leave both rule strings unchanged." The 2026-09-26 remediation (`22d18d72`) applied it, and
      the merge `ebbfa90f` reversed it.
4. **Earlier decisions this plan relies on.** Ben's page and folio terminology of 2026-09-27,
   recorded as item 4 of the first entry of `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`;
   his decision of 2026-09-26 that `hbce-psalms/out/` is a frozen record ("I accept the frozen
   record.", quoted in the `NOT_IN_MEGA` reason for `py/main_hbce_psalms.py compare` in
   `py/tests/test_mega_coverage.py`); his decision of 2026-09-12 that MAM-for-Sefaria and MAM-OSIS
   are not kept continuously current ("I know of no reason to be supplying constantly-updated
   versions of these", quoted in the same file's `_SEF_AND_OSIS_NOT_KEPT_CURRENT`); D7, D11 and
   D12; and the common body's "Tests are differential or lint-shaped".
5. **Ben's approval of this plan, 2026-09-30.** After this plan was committed at `50ef50ee`, Ben
   answered twelve questions in four dialogs. The questions, option labels and descriptions were
   the second session's wording; Ben's part is his selection of each, which the live update records
   in full under "Ben's approval of the remediation plan, 2026-09-30". His selections settle every
   choice this plan leaves open:
   1. The reader-facing wording, the public-data change and the lower-risk changes: approved as
      worded.
   2. `MAM-with-doc/LICENSE.md`: the edition sentence, the alternative under "The five product
      `LICENSE.md` files"; `DATA-LICENSES.md`'s new paragraph takes the variant shown for it.
   3. Flagged site 9: the "join" wording in `hbce-psalms/README.md` and `DATA-LICENSES.md`.
   4. Flagged site 12: the Holman page's introduction is fixed.
   5. Finding 8.1: the September 9 plan's passages and the hazard-5 re-reading are approved as they
      stand, and findings 2.5, 28.5 and 29 apply to them as worded; the reversal list does not apply.
   6. Hazard H6: the wording that names the worktree's home clone.
   7. Flagged sites: all three groups approved, so sites 1 to 10 and 13 apply; site 11, the test
      fix, applies too.
   8. `py/tests/test_mega_coverage.py:379–381`, item 23.7 under "Python comments and docstrings":
      "a lookup that prints one estimated page, column and line".
   9. Execution: approved, as close-out steps 3 and 4 in a fresh task.

## Reader-facing documents: the approval surface (high risk)

These are the changes to rendered HTML and to Markdown written for readers, first in the order of
`doc/periodic-review.md`'s "Present remediation by public-facing risk". Each item gives the current
words and the proposed words. Items marked **approved wording** follow wording Ben has already
approved; every other item is proposed for his approval. Copy any Hebrew from the current file byte
for byte, never normalized, and wrap lines so that none begins with Hebrew.

### Rendered HTML

**Finding 1.1, `gh-pages/MAM-parsed/plus/html/mpplus.html`, the consumer notice in three places,
approved wording.**

- Current: in the notice's list (`:35–39` and `:40–44`), the item beginning "A whitespace template
  can be the only separator" comes before the item beginning "Narpas (narrow-sense paseq, ׀) forms
  no compound of any kind", so the page says "This rule does not apply to narpas, whose missing
  literal whitespace prescribes no display spacing." one item before it glosses "narpas". The page's
  two example headers, Job's (`:154–155`) and Samuel's (`:186–187`), hold the same two rules in the
  same order, one line each.
- Proposed: the same two list items, and the same two lines of each example header, word for word,
  with the narpas rule first, as the 2026-09-26 remediation (`22d18d72`) ordered them before the
  merge `ebbfa90f` reversed the order.
- The page is generated. `py/main_parse.py ws` rewrites it from `py/mb_cmn/public_data_consumer_notice.py`,
  which supplies the list (through `py/author_misc/mp_body_shared.py:73`) and the two example headers
  (through `py/author_misc/mpplus_body.py:110` and `:123`), as "Public data" below describes.
  Formatting: each of the three places is an exchange of whole lines, and the two five-line list
  items keep their wrapping; nothing else on the page changes. `22d18d72` changed the page in exactly
  these three places.

**Flagged site 12, `gh-pages/holman/uxlc_corrections.html`, the introduction, for approval or
striking.**

- Current, from `py/py_render/uc_html.py:423–425`: "The folio link under the line is decoded from
  the page ordinal Holman's citation begins with, so the folio number is not his either." It has
  been false since 2026-08-12, when the link began to show the estimate's page.
- Proposed: "The folio link under the line is the estimate's too; where the folio Holman's ordinal
  decodes to differs, the card names it beside the estimate." The page's own word "folio" stays,
  since question 5 leaves generated pages unswept. Evidence and regeneration are under "Sites found
  while planning", site 12.

### Reader-facing Markdown

#### `in/mam-ws-intro/README.md`

1. **Finding 2.1, `:48–49`, approved wording.**
   - Current: "`git show --stat 985262e2` names every file removed; Phase 3 of
     `doc/PLAN-mega-coverage.md` records the totals."
   - Proposed: "`git show --stat 985262e2` names every file removed. Phase 3 of the
     [retired mega-coverage plan](https://github.com/bdenckla/MAM-basics/blob/f72297084ab94aea6fd1274dc1bc3d7ce6acddd5/doc/PLAN-mega-coverage.md)
     records the totals."
2. **Finding 13, `:36–38`.**
   - Current: "five of the thirteen pages were edited in August 2026 alone (the committed manifest's
     count; this said four until 2026-09-01, from a drafting-time fetch predating the month's last
     two edits)."
   - Proposed: "five of the thirteen pages were edited in August 2026 alone (the count in the
     manifest committed on 2026-08-31, which the refresh of 2026-09-27 replaced; this said four
     until 2026-09-01, from a drafting-time fetch predating the month's last two edits)."
   - Facts: `d061fad8` (2026-08-31) committed a manifest with five August timestamps, those of ch2,
     ch3, ch4, ch5 and the appendices, summing 1,852,837 bytes. `c450060e` (2026-09-27) refreshed
     it; it now has one August timestamp, ch4's, and sums 1,886,674 bytes.

#### `doc/meteg-after-silluq-snips/README.md`

The 2026-09-26 plan treated this README as reader-facing, and `evr-ii-b-55/README.md` links it.

1. **Finding 2.4, `:119–120`, approved wording.** Current: "so Ben identifies the page as folio
   **57a**." Proposed: "so Ben identifies the page as page **57a**."
2. **Finding 2.4, `:366–368`.** Current: "so this source image is recorded as folio **307b**."
   Proposed: "so this source image is recorded as page **307b**." This matches `:289`, "so this
   source image is recorded as page **303a**".
3. **Question 5, `:416`.** Current: "The folio is right and the column is not independently
   confirmed:". Proposed: "The page is right and the column is not independently confirmed:". The
   estimator's page is F380A (`:409`).
4. **Question 5, found after the planning answer, `:167`, `:246` and `:320`.** Current, in each:
   "whole-folio photograph at Sefaria", whose link opens the image of one page
   (`BIB_LENCDX_F195B.jpg`, `BIB_LENCDX_F377B.jpg` and `BIB_LENCDX_F379B.jpg`). Proposed, in each:
   "whole-page photograph at Sefaria".
5. **Question 5, found after the planning answer, `:464–465`.** Current: "The Internet Archive's
   photograph of the leaf has the same two strokes". Proposed: "The Internet Archive's photograph of
   the page has the same two strokes"; the photograph is `271r.jpg`, one page.

#### `doc/lam-2-3-akhla-snips/README.md` (question 5)

The sibling of the README above and of the same kind: `DATA-LICENSES.md:8` and `:101` name both
crop directories together. No reader-facing page links it, and the 2026-09-26 plan did not name it;
it is presented here beside its sibling so that both READMEs' locators are approved together. Its
crop filenames and the estimator's printed `{'page': '430B', …}` at `:84` stay as they are.

1. `:43–45`. Current: "has both links for every folio — 982 of them, checked 2026-09-10 — so it is
   the way to get from a folio number to an image. The page is a folio and side, as in `430B`."
   Proposed, reusing the approved wording of the sibling README's `:52–55`: "has both links for
   every manuscript page identifier — 982 of them, checked 2026-09-10 — so it is the way to get from
   a page identifier to an image. The manuscript page identifier combines the folio number and side,
   as in `F430B`."
2. `:49`. Current: "The page is a leaf and side in `{leaf:04d}{side}` form, as in `0105B`." Proposed,
   parallel to the approved sentence at the sibling README's `:34`: "The manuscript page identifier
   is `{leaf:04d}{side}`, as in `0105B`."
3. `:58`. Current: "on **folio 430B, column 2, line 10**." Proposed: "on **page F430B, column 2,
   line 10**."
4. `:75–76`. Current: "for Cambridge Add. 1753 leaf 0105B column 2." Proposed: "for Cambridge Add.
   1753 page 0105B column 2."
5. `:80–81`. Current: "put this word at folio 430B, column 2, line 12.9". Proposed: "put this word
   at page F430B, column 2, line 12.9".
6. `:87`. Current: "The folio is right and the column is not independently confirmed:". Proposed:
   "The page is right and the column is not independently confirmed:".
7. `:93–94`. Current: "on **leaf 0105B, column 2, third line up from the bottom**". Proposed: "on
   **page 0105B, column 2, third line up from the bottom**".
8. Found after the planning answer, `:32–33`. Current: "so the leaf hunt for that manuscript still
   runs through `../../cam1753/`". Proposed: "so finding the page for that manuscript still runs
   through `../../cam1753/`", matching the section heading "Finding a page and its image" (`:18`).

#### `evr-ii-b-55/README.md`

1. **Finding 3.1, `:523`.** Current heading: "### Segmentation of Psalms, Job and Proverbs".
   Proposed: "### Segmentation of the verses the catalog lists before 2 Chronicles 11". The
   paragraph below it concerns "the 4,827 verses that the catalog lists before 2 Chronicles 11",
   under "## Reaching images 005–495". No link targets the old heading's anchor.
2. **Finding 3.2, `:343–344`.** Current: "They agree on all 17,358 verses but Psalms 10:5, where
   `get_verse_words` drops an atom (item 6)." Proposed: "They agreed on all 17,358 verses but
   Psalms 10:5, where `get_verse_words` then dropped an atom; item 6 records the fix of
   2026-09-28."
3. **Question 5, `:182`.** Current: "image 623 is folio 303a, and images 632, 634 and 714 are folios
   307b, 308b and 348b." Proposed: "image 623 is page 303a, and images 632, 634 and 714 are pages
   307b, 308b and 348b."
4. **Question 5 (listed), `:194`.** Current: "and identifies the page as folio 57a." Proposed: "and
   identifies image 120 as page 57a."
5. **Question 5 (listed), `:485–486`.** Current: "Ben's folio 57a on image 120 puts fol. 78b at
   image 163, if the images run two per folio in between." Proposed: "Ben's page 57a on image 120
   puts fol. 78b at image 163, if the images run two per folio in between." Here, at `:186–259`,
   at `:473–474`, `:482` and `:487`, the catalog's "fol." locators cite the catalog and keep its
   form.
6. **Question 5, `:493`.** Current: "By the relation at image 120, image 116 would be folio 55a."
   Proposed: "By the relation at image 120, image 116 would be page 55a."

#### `cam1753/doc/cam1753-line-break-task.md` and `cam1753/README.md`

1. **Finding 18.1, the note's `:7–9`.**
   - Current: "Until then this file was the marking procedure;
     `git show f4d81285:cam1753/doc/cam1753-line-break-task.md` recovers that version, and
     `git show f4d81285:<path>` recovers each retired program."
   - Proposed: "Until then this file was the marking procedure;
     `git show f4d81285:cam1753/doc/cam1753-line-break-task.md` recovers that version, and
     `git show f4d81285:<path>` recovers each retired program except those that `f2a9ead4` deleted
     earlier that day. Among them is the interactive line-break editor that version describes:
     `git show 4ac4f16a:py/py_cam1753_loc/gen_line_break_editor.py` recovers it, and its wrapper,
     `py/main_cam1753_gen_line_break_editor.py`, is at the same commit."
   - Facts: `f2a9ead4` (2026-09-26, 13:22:50 New York time) deleted the editor and is an ancestor
     of `f4d81285`, which lacks both editor files; `4ac4f16a` holds both.
2. **Finding 18.2, the README's `:4–5`.** Current: "Its line-break data begins in Psalms and
   continues through Job, and its page index also covers Lamentations." Proposed: "Its line-break
   data begins at Psalms 149:7 and continues through Job into Proverbs, ending with the first three
   atoms of Proverbs 1:31, and its page index also covers Lamentations."
3. **Finding 18.2, the note's `:26`.** Current: "- Line breaks: 27 pages, `0072B` through `0085B`,
   from Ps 149:7 through the end of Job." Proposed: "- Line breaks: 27 pages, `0072B` through
   `0085B`, from Ps 149:7 through the end of Job and on into Proverbs: `0085B` ends with the first
   three atoms of Proverbs 1:31, closed by a `verse-fragment-end` label." The next line, "Page `0086A`
   is past Job and has no line-break file.", stays.
   - Facts, measured on 2026-09-30: after Job, `cam1753/cam1753-line-breaks/0085B.json` holds
     Proverbs 1:1–30 and three atoms of 1:31, 221 atoms in all.

#### Four more documents that call a page a folio or a leaf (question 5, found after the planning answer)

Each is written for readers of its data: `cam1753/README.md:27` links the first, `DATA-LICENSES.md`'s
rows for `aleppo/` describe the Aleppo records (`:91`, `:93`), and the snips README's opening links
the Psalms 72:15 report (`:6`).

1. `cam1753/things-noticed-in-cam1753.md`: `:12`, "above Lam 1:1 on leaf 0105A col 2", becomes
   "above Lam 1:1 on page 0105A col 2"; `:14`, "one instance above leaf 0105B col 2", becomes "one
   instance above page 0105B col 2"; and `:18`, "**Lamentations begins on leaf 0105A col 2", becomes
   "**Lamentations begins on page 0105A col 2".
2. `aleppo/aleppo-pages-provenance.md:27`: "Leaves 270r through 281v (24 pages), covering the Book
   of Job in the" becomes "Pages 270r through 281v, 24 in all, covering the Book of Job in the".
   Line 8's "gives leaf 270 recto" and the naming convention's leaf numbers (`:32–37`) speak of the
   leaf and stay.
3. `aleppo/doc/aleppo-line-breaks.md`: `:63`, "(see leaf table below)", becomes "(see the Job page
   table below)"; `:83`, the heading "## Job leaf table", becomes "## Job page table" (only `:63`
   refers to it, and nothing links its anchor); and `:86`, the code block's column header "Leaf",
   becomes "Page", since its rows are pages such as `270r`. Line 66's "Job leaves" and "extra leaf
   241a" speak of the leaves and stay.
4. `doc/meteg-after-silluq-psalms-72-15.md:10`: "Sefaria's image of the folio is" becomes
   "Sefaria's image of the page is", before the link to `BIB_LENCDX_F380A.jpg`.

#### `hbce-psalms/README.md`

1. **Finding 20, `:36–40`.**
   - Current: "The outputs under `out/` quote MAM, which keeps its CC-BY-SA 4.0 terms, and forms
     from HBCE's transcriptions, which keep CC BY 4.0 with the attribution above; the outputs change
     those forms only by splitting them into chanted words and, in `out/research_queue.md`, by
     putting their marks in MAM-normal order. [`../DATA-LICENSES.md`](../DATA-LICENSES.md) records
     the same terms."
   - Proposed: "The outputs under `out/` quote MAM, which keeps its CC-BY-SA 4.0 terms, and forms
     from HBCE's transcriptions, which keep CC BY 4.0 with the attribution above. The outputs change
     those forms only in these ways: they join each form that ends in a maqaf to the form after it,
     so that each form they quote is a chanted word; they replace U+05BA HEBREW POINT HOLAM HASER
     FOR VAV with U+05B9 HEBREW POINT HOLAM; they insert a space before a U+05C0 HEBREW PUNCTUATION
     PASEQ that ends one of HBCE's `<w>` elements; and, in `out/research_queue.md`, they put the
     forms' marks in MAM-normal order. [`../DATA-LICENSES.md`](../DATA-LICENSES.md) records the
     same terms."
   - The first of those four clauses is flagged site 9 under "Sites found while planning": the
     current "splitting them into chanted words" misdescribes the code, which never splits a form,
     and the package did not name that defect. If Ben strikes the flagged site, the clause reads
     "they split them into chanted words" and the other three stand.
   - Facts, measured on 2026-09-30 over the 35 TEI files: of 11,789 `<w>` elements, 1,499 end in a
     maqaf and are joined to the next, and 4 hold an inner maqaf and stay as they are; 32 hold
     U+05BA; all 370 U+05C0 marks inside `<w>` elements end their element; no `<w>` element holds
     U+05C3, U+200C, U+200D or U+034F, the other characters `hbce_finalize` strips
     (`py/hbce_psalms/compare.py:218–245`, with `_shown` at `:620–621`). The wording names the
     Unicode character, which can stand for narrow-sense paseq or for legarmeh, and chooses neither.
2. **Finding 28.6, `:62–66`.** Current: "From the repository root:" over
   `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_hbce_psalms.py compare`.
   Proposed: "From the root of a full MAM-basics clone, with its own environment (a linked worktree
   uses its home clone's interpreter by absolute path):" over
   `./.venv/Scripts/python.exe py/main_hbce_psalms.py compare`.

#### `MAM-parsed/historical/README.md` (inside the distributed `MAM-parsed/`)

1. **Finding 24.1, `:24–26`.** Current: "The six pre-migration archives were written on 2026-09-10
   by a program that was never tracked." Proposed: "The six pre-migration archives were written on
   2026-09-10, from loose JSON copies of their files stored on 2026-09-06, by a program that was
   never tracked."
2. **Finding 24.1, `:36–38`.** Current: "The snapshots had been made on 2026-09-06 for the six
   boundaries that lived in MAM-parsed, and a later boundary was read from MAM-basics history, which
   a shallow clone lacks beyond its depth." Proposed: "Snapshots of the six boundaries that lived in
   MAM-parsed had been stored since 2026-09-06, as loose JSON until 2026-09-10 and as archives
   since, and a later boundary was read from MAM-basics history, which a shallow clone lacks beyond
   its depth."
   Facts: `8176e91d` (2026-09-06) added the loose JSON, and `32fa7da6` (2026-09-10) replaced it with
   the ZIP archives.
3. **Finding 24.2, `:78–81`.** Current: "Every change-log run refuses, before comparing anything, a
   boundary of `releases.json` that has no snapshot, and names the fix. For a boundary pinned without
   `--pin`, run this in a clone that has the boundary's commit, then run `--all`:" Proposed:

   > Before comparing anything, a change-log run refuses each boundary of `releases.json` that it
   > checks and that has no snapshot, and names the fix. Which boundaries it checks depends on the
   > run. `--all`, `--check` and the mega's diff-mpplus step check every boundary. A run without
   > arguments checks only the latest release's end, the one boundary it compares. `--pin` checks
   > the latest release's end before it writes anything, and the other boundaries only when it
   > regenerates the change log, after it has written HEAD's snapshot, its manifest entry and its
   > line in `releases.json`; the fix a refusal names then completes the pin. A run with explicit
   > `--old` and `--new` checks no boundary. A snapshot counts as stored when `manifest.json` lists
   > it, so a listed snapshot whose archive file is missing passes every guard and stops the run at
   > its first read, with an error that names the missing file but not the fix. For a boundary
   > pinned without `--pin`, run this in a clone that has the boundary's commit, then run `--all`:

   Sources: `py/subcommands/diff_mpplus.py:285`, `:320–321`, `:437–438`, `:458–464`, `:502–505` and
   `:597–605`, `py/mb_diff_mpu/mpplus_revisions.py:66–82` and `:95–101`, as turns 07 to 10 read
   them, and the mega's step at `py/main_0_mega.py:268–272`.

#### `MAM-parsed/README.md` (item 36.12, inside the distributed `MAM-parsed/`)

Insert after `:8–9` ("`plus/` contains one JSON file for each of the 24 books of the Miqra. Hebrew
Wikisource supplies the source data."):

> Until 2026-09-28 this directory also held a second format, MAM-parsed plain, under `plain/`. It was
> retired that day and is no longer generated or distributed. Git history keeps it:
> [`52f1f6bf`](https://github.com/bdenckla/MAM-basics/tree/52f1f6bfce902b1493a6738979aac959841e8f0d/MAM-parsed/plain),
> the last commit `main` pointed to before the retirement, holds its 24 book files. A link to a
> `plain/` file on `main` no longer resolves; pin such a link to that commit, or read the `plus/`
> file for the same books, whose format differs.

Facts: `doc/PLAN-retire-mam-parsed-plain.md` records Ben's decisions of 2026-09-27 and execution on
2026-09-28. `87fc7141` deleted `plain/` and reached `main` through the merge `ebbfa90f`, whose other
parent, `52f1f6bf`, was `main`'s tip before the fast-forward. The eight static pages under
`gh-pages/MAM-parsed/plain/html/` say "MAM-parsed plain was retired on 2026-09-28."

#### `README.md` (the repository root)

**Finding 27, `:71–74`.** Current: `.venv/Scripts/pip.exe install -r requirements.txt`. Proposed:
`.venv/Scripts/pip.exe install -r requirements.txt -c constraints.txt`. The line above it,
`python -m venv .venv`, stays.

#### `DATA-LICENSES.md`

1. **Finding 10.2, `:82`, the `MAM-parsed/` row.** Current: "MAM-parsed's plain and plus JSON,
   historical release snapshots, documentation, license, and example program". Proposed:
   "MAM-parsed's plus JSON, historical release snapshots, documentation, license, and example
   program".
2. **Finding 20, `:99`, the end of the `hbce-psalms/out/` row.** Current: "the outputs change those
   forms only by splitting them into chanted words and, in the research queue, by putting their
   marks in MAM-normal order". Proposed: "the outputs change those forms only by joining each form
   that ends in a maqaf to the form after it, so that each form they quote is a chanted word, by
   replacing U+05BA HEBREW POINT HOLAM HASER FOR VAV with U+05B9 HEBREW POINT HOLAM, by inserting a
   space before a U+05C0 HEBREW PUNCTUATION PASEQ that ends one of HBCE's `<w>` elements, and, in
   the research queue, by putting their marks in MAM-normal order". The first clause is flagged
   site 9, as in the README; if Ben strikes it, the clause reads "by splitting them into chanted
   words".
3. **Finding 10.1 with question 6, the section "The MAM statement, repeated verbatim".**
   - Current introductory paragraph (`:129–135`): "What follows is the license and attribution
     statement from the former MAM Google spreadsheet, which became a frozen historical archive on
     September 12, 2026. The statement is copied without change. The same file stands as
     `LICENSE.md` in the landed `MAM-parsed/`, `MAM-simple/`, `MAM-with-doc/`, `MAM-for-Sefaria/`,
     and `MAM-OSIS/` product directories. The historical `MAM-OSIS/MAPM-orig/` and
     `MAM-OSIS/MAPM-orig-24/` files retain the separate CC-BY-SA 3.0 notice recorded above. Where
     the statement says "the data in this GitHub repository", read it as the MAM paths named in the
     table above, not as everything in MAM-basics."
   - Proposed introductory paragraph:

     > What follows is the license and attribution statement from the former MAM Google spreadsheet,
     > which became a frozen historical archive on September 12, 2026. The statement is copied
     > without change. Here it applies to the MAM paths named in the table above, not to everything
     > in MAM-basics; in it, ignore the references to "in this spreadsheet" (English)
     > and שבגליון הנתונים הזה (Hebrew). Each of the landed `MAM-parsed/`, `MAM-simple/`,
     > `MAM-with-doc/`, `MAM-for-Sefaria/`, and `MAM-OSIS/` product directories holds a `LICENSE.md`
     > that repeats the statement after a short preface saying that it applies equally to the data
     > in that directory. The preface in `MAM-OSIS/LICENSE.md` excepts the historical
     > `MAM-OSIS/MAPM-orig/` and `MAM-OSIS/MAPM-orig-24/` files, which retain the separate
     > CC-BY-SA 3.0 notice recorded above.

     If Ben chooses the MAM-with-doc alternative below, the sentence's "the data in that directory"
     becomes "the data in that directory, or, for `MAM-with-doc/`, the edition MAM-basics publishes
     from `gh-pages/MAM-with-doc/`".

   - Also delete the copy's old wrapper, `:138–145`: the blank line after the first `----`, the five
     lines from "We here repeat, in English & Hebrew, the licence & attribution information" through
     "or שבגליון הנתונים הזה (Hebrew).", the blank line after them and the second `----`. The copy
     then runs from the remaining `----` straight into "License:", as the statement stands in the
     product files; the statement itself, from "License:" to the end of the section, stays byte for
     byte.

#### The five product `LICENSE.md` files (question 6, distributed data)

Today `MAM-parsed/LICENSE.md`, `MAM-simple/LICENSE.md`, `MAM-with-doc/LICENSE.md`,
`MAM-for-Sefaria/LICENSE.md` and `MAM-OSIS/LICENSE.md` are one blob, `8bd7a07a`, which opens: "The
statement below is preserved verbatim from the former MAM Google spreadsheet, / which became a frozen
historical archive on September 12, 2026." The proposed sentences adapt, to each file's own
directory, the preface the files carried until `a41fbcdd` ("This information applies equally to the
data in this GitHub repository. / So, in the text below, ignore any references to "in this
spreadsheet" (English) / or שבגליון הנתונים הזה (Hebrew).").

1. **In the four files other than MAM-OSIS's**, insert directly after line 2:

   > This statement applies equally to the data in this directory. So, in the text below,
   > ignore any references to "in this spreadsheet" (English) or שבגליון הנתונים הזה (Hebrew).

   The four stay one blob, or three under the MAM-with-doc alternative below.
2. **In `MAM-OSIS/LICENSE.md`**, insert directly after line 2:

   > This statement applies equally to the data in this directory, except the historical files
   > under `MAPM-orig/` and `MAPM-orig-24/`, which keep the CC-BY-SA 3.0 Unported notice in
   > `MAPM-orig/readme.txt`. So, in the text below, ignore any references to "in this spreadsheet"
   > (English) or שבגליון הנתונים הזה (Hebrew).
3. **An alternative for `MAM-with-doc/LICENSE.md`, for Ben's choice.** `MAM-with-doc/` holds only
   its README, its licence, `.gitattributes` and `.gitignore`; MAM-basics publishes the edition
   itself from `gh-pages/MAM-with-doc/` (`DATA-LICENSES.md:85`, `MAM-with-doc/README.md:7–8`), so
   "the data in this directory" covers nothing there. The alternative inserts instead:

   > This statement applies equally to the MAM-with-doc edition, which MAM-basics publishes from
   > `gh-pages/MAM-with-doc/`. So, in the text below, ignore any references to "in this spreadsheet"
   > (English) or שבגליון הנתונים הזה (Hebrew).

   That file would then leave the blob the other three share, and `DATA-LICENSES.md`'s new
   paragraph takes the variant shown with it above.

Formatting: two inserted lines, three in the MAM-with-doc alternative and four in
`MAM-OSIS/LICENSE.md`; the blank line and everything after it stay byte for byte. The table rows of
`DATA-LICENSES.md` that say "as `<product>/LICENSE.md` states" become true of the grant again and
stay as they are.

## Public data (high risk)

**The one public-data change is finding 1.1's consumer notice, in all 24 `MAM-parsed/plus/*.json`
files.** In each file's `header.consumer_notice.critical_rules`, rules 5 and 6 exchange places, so
that the narpas rule, beginning "Narpas (narrow-sense paseq, ׀) forms no compound of any kind",
precedes the whitespace-template rule, beginning "A whitespace template can be the only separator".
Neither rule's text changes. Each file changes on two adjacent lines: 18–19 in the single-book
files, 25–26 in `BA-Samuel.json`, `BC-Kings.json`, `FA-Ezra-Nexemiah.json` and `FC-Chronicles.json`,
and 75–76 in `CA-The-12-Minor-Prophets.json`. Every `book39s` value, every other header field and
every Scripture payload stays byte for byte.

- **Source change:** in `py/mb_cmn/public_data_consumer_notice.py`, `mam_parsed_notice`, list
  `NARPAS_GROUPING_RULE` before `MAM_PARSED_WHITESPACE_TEMPLATE_RULE` (`:79–80`).
- **Regeneration:** `py/main_parse.py ws`, which writes the 24 files and ends by regenerating the
  MAM-parsed documentation, `mpplus.html` included (`py/subcommands/parse_ws_products.py:39–44`).
- **Independent check:** after regeneration, rules 5 and 6 of each file equal the lines holding
  them at `52f1f6bf`, `main`'s tip before the merge that reversed them (lines 18–19 of
  `git show 52f1f6bf:MAM-parsed/plus/A1-Genesis.json`, and correspondingly in each file). Rule 7
  differs from `52f1f6bf` by the plain retirement's change and is not part of this fix.
- **Traced effects:** `mpplus.html`, in the three places named under "Rendered HTML" above: the
  notice's list and the two example headers. No change-log file is expected to change: nothing under
  `py/mb_diff_mpu/` or in `py/subcommands/diff_mpplus.py` reads `consumer_notice`. The historical
  archive `MAM-parsed/historical/cb95915d54e6cfdd38babef710d46f48a2c4acf5.zip` keeps its old
  notice, as every stored snapshot must.

No other public data changes, apart from the five product licence files presented above. By Ben's
answer to question 2, MAM-for-Sefaria and MAM-OSIS are not regenerated, so MAM-for-Sefaria's rows
and MAM-OSIS's `MAPM-24` files and `mapm.osis.xml` keep lagging MAM-simple at Judges 19:23 and
2 Kings 22:1. By Ben's first planning answer, the note in `evr-ii-b-55/evr-ii-b-55-page-index.json`
stays as it is, as do the generated Holman and goerwitz pages. Question 5's remaining edits, to the
`hebrew-prose` and `verse-links` skills, to `py/main_verse_links.py` and to two Holman helper
modules, are lower-risk changes, under "Editorial proposals: agent instructions" and "Editorial
proposals: Python comments and docstrings". No change to MAM's own text is proposed.

## Lower-risk changes

### Summary by type

1. **Markdown under `doc/` and update entries:** the procedure record of this round and E1 in
   `doc/dual-agent-review.md`; corrections in the two runbooks, `doc/clone-forests.md` and the
   maintenance runbook, in the live September 9 plan, in five other maintained documents and in two
   more among the flagged sites; in-place corrections of eight open update files, each with a dated
   entry; a new update file for the HBCE receipt; and dated entries in two more updates, the
   finding-30 list of approved public additions among them.
2. **Python comments and docstrings:** about thirty files, among them the special-page downloader,
   the introduction downloader, `py/product_scopes.py`, the forest synchronizer and three test
   modules, four with flagged site 6.2.
3. **Agent instructions:** repository `AGENTS.md` (findings 11, 12, 34.1 and item 36.2), which
   takes effect when committed; the common body `dot-Codex/user-wide-AGENTS.md` (findings 2.5, 32,
   33 and 34.1) and the skills `hebrew-prose`, `verse-links`, `mam-wikisource-refresh`,
   `mam-repository-topology`, `github-issues`, `iterative-document-editing` and Codex's
   `codex-worktree-tasks`, which take effect when deployed; and the two configuration READMEs.
4. **Code and tests:** thirteen defects, findings 1.2, 5.6, 6.1 to 6.3, 7, 14.1, 14.2, 15, 16, 17,
   25 and 26 (the package's list of twelve counted finding 1.1, which "Public data" covers here, and
   counted finding 6 as one), with one new lint for finding 25 and an extension of the retirement
   simulation for finding 7. No mega generator's tracked output is expected to change except as
   "Public data" says, and finding 16 changes line 2 of one lock file.

### Reproducible code and test defects (D7: defects)

Each fix stays within its approved disposition and the rule that tests be differential or
lint-shaped. Scratch mutations named under "Verification" are run from a gitignored scratch
directory and never committed.

**Finding 1.2, `py/tmpl_survey/stack_path_lookup.py:74–80`.** `_dataset_file_paths` binds the local
name `paths` at `:76`, so `:75`'s `paths.mam_parsed_dir()` raises `UnboundLocalError`.
- Fix: rename the local list to `file_paths` (three lines). Do not restore the merge parents'
  `_dataset_folder`, whose assertion admitted the retired `"plain"`.
- Verification: `./.venv/Scripts/python.exe -m ruff check --no-cache py` prints "All checks passed!"
  once finding 14.2 is fixed too (today it reports F823 here and F401 at
  `py/verify_mp/verifiers_plus.py:14`); `--no-cache` keeps ruff from writing `.ruff_cache/`, which
  `.gitignore` does not list. Then run
  `./.venv/Scripts/python.exe py/main_tmpl_survey.py --find-stack-path "E/נוסח" --find-stack-path-limit 2`
  and, separately, since the two flags exclude each other,
  `./.venv/Scripts/python.exe py/main_tmpl_survey.py --find-stack-path-verbose "E/נוסח" --find-stack-path-limit 2`:
  each must print two hits, Genesis 1:1 and then 1:3. The lookup writes nothing. Then
  `py/tests/test_stack_path_lookup.py` and `py/tests/test_mega_coverage.py`, whose `:368–372`
  becomes true again.

**Finding 5.6, `py/py_html/my_html_for_img.py:98–272`.** `focus_fade_img` keeps an `overlay_class`
parameter (`:105`) that its only caller, `py/author_site/post_stress_meteg_post_silluq_images.py:482–489`,
never passes.
- Fix: delete `:105` and write its default at `:264`: `"class": "scan-annot-overlay focus-fade-overlay",`.
- Verification: `./.venv/Scripts/python.exe py/main_authored.py gen-site --trust-surveys` must leave
  `gh-pages/post-stress-meteg-post-silluq-1k14v14.html`, the only page with that class (`:31`), and
  every other page byte for byte; then `py/tests/test_scan_overlay_viewboxes.py`.

**Finding 6.1, the force-flag lint, `py/tests/test_worktree_retirement_policy.py:69–113`.** It
compares whole tokens, so `-df`, `-fd` and `-ff` pass.
- Fix: read a single-dash letter token as a cluster of short options, as Git does. Add `import re`
  after `import ast` (`:3`); without it ruff reports F821. Then add three module-level helpers:

  ```python
  _SHORT_OPTION_CLUSTER = re.compile(r"-[A-Za-z]+")


  def _short_options(token):
      """The option letters of a single-dash cluster such as -df; none for any other token."""
      if isinstance(token, str) and _SHORT_OPTION_CLUSTER.fullmatch(token):
          return frozenset(token[1:])
      return frozenset()


  def _forces(token):
      """--force, or a short-option cluster holding f or D: -f, -D, -df, -fd, -ff."""
      return token == "--force" or bool(_short_options(token) & {"f", "D"})


  def _deletes_branch(token):
      """--delete, or a short-option cluster holding d or D: -d, -D, -df, -fd."""
      return token == "--delete" or bool(_short_options(token) & {"d", "D"})
  ```

  `:72` becomes `assert not _forces(node.value), (…)`, and the comment above it (`:70–71`) becomes
  "# These finite retirement modules have no use for a literal force flag, alone or / # in a
  short-option cluster such as -df. This also catches flags in separately / # assigned argument
  sequences." (the slash marks a line break); `:80–82` becomes
  `branch_delete = "branch" in tokens and any(_deletes_branch(token) for token in tokens)`; `:90`
  becomes `assert not any(_forces(token) for token in tokens), (…)`.
- Trade-off: `visit_Constant` (`:69–76`) sees every constant of a scanned module, so a future
  standalone constant of a dash and letters holding `f` or `D`, such as PowerShell's `-NoProfile`,
  `-Confirm`, `-Depth` or `-Directory`, would fail the lint and need an explicit exception.
- Verification: the test passes on today's twelve scanned modules, whose single-dash constants are
  `-d -z -l -I -i -e -t -q - -p -m`; scratch mutations (`-ff` on the engine's worktree removal,
  `git branch -df` in an adapter, a `"-fd"` constant) now fail it.

**Finding 6.2, the cluster lint, `py/tests/test_mpplus_alternative_oracle.py:385–396`.** It checks a
mark only when a Hebrew letter precedes it, so a mark after a `gray-maqaf` span goes unchecked.
- Fix: `:391` becomes `if self.base_context is None or context != self.base_context:`, so every
  combining mark needs a Hebrew-letter base in its own highlight context. The class docstring
  (`:360`), now """Check every real Hebrew cluster across highlight/pointed-span boundaries.""",
  gains a second paragraph, "Every combining mark needs a Hebrew-letter base in its own highlight
  context.", with its closing quotes on a line of their own.
- Verification: the test passes on all seven current reports. As a scratch check, the changed lint
  run over `git show f4d81285:gh-pages/MAM-with-doc/change-log/2026-03-06.html` reports exactly one
  problem, U+05A5 at line 70, the fifth case of the 2026-09-26 round's finding 25.5, besides the
  four cases the old lint found in the other reports at that commit.

**Finding 6.3, `test_exact_relocation_citations_gate_and_survive_retirement` in
`py/repo_util/worktree_retirement_simulation_test.py`.** `22d18d72` dropped its fingerprint
assertion, and the merge `2374ea30` kept the drop.
- Fix: restore main's own post-split text (`89ae4b85`). After `:632` insert:

  ```python
          review_payload = {
              key: value
              for key, value in reviewed["citation_review"].items()
              if key != "fingerprint"
          }
  ```

  and before `retirement.execute_retirement(…)` (`:638`) insert:

  ```python
          assert reviewed["citation_review"]["fingerprint"] == preflight._fingerprint(
              review_payload
          )
  ```

  The module already imports `worktree_retirement_preflight as preflight` (`:24`).
- Verification: `./.venv/Scripts/python.exe py/main_test.py py/repo_util/worktree_retirement_simulation_test.py -q`,
  which default discovery does not collect.

**Finding 7, `py/repo_util/worktree_retirement_inspection.py`, `_citation_references` (`:276–331`).**
A target's retained `.novc/t`, where `py/main_test.py`'s `_add_windows_basetemp` (`:116–133`) puts
the suite's per-process base temporary directories on Windows, becomes a gating citation; on this
tree it would gate on ten lines in six files, among them this review's own records, and this plan's
own mentions of `.novc/t` add more once it is committed.
- Fix, gating only: beside `_DISPOSABLE_CACHE_DIRS` (`:32–34`) add

  ```python
  # py/main_test.py's _add_windows_basetemp puts pytest's per-process base temporary
  # directories below this child of a checkout's root .novc on Windows. Retirement
  # relocates it with the rest of that .novc, but it is disposable cache: no spelling
  # of it, or of anything below it, is a citation that gates retirement.
  _SUITE_BASETEMP_NOVC_CHILD = "t"


  def _is_suite_basetemp(relative: str) -> bool:
      return PurePosixPath(relative).parts[:1] == (_SUITE_BASETEMP_NOVC_CHILD,)
  ```

  and in `_citation_references`, before `:292`, compute
  `root_novc = _same_path(source, retirement_target / ".novc")`, then filter both `extend` calls at
  `:293–298` with `if not (root_novc and _is_suite_basetemp(relative))`, using `file["path"]` for
  files. Only the target's root `.novc/t` is exempt; a nested `.novc/t` and every other retained
  child keep gating. Relocation is unchanged: `.novc/t` is still inventoried, copied and verified.
  A preflight whose recorded citations include a spelling of `.novc/t`, as one prepared on this
  tree before the change would, fails closed as drifted and must be prepared again.
- Verification, differential: extend `test_exact_relocation_citations_gate_and_survive_retirement`'s
  fixture after `:540` with `(source / "t" / "p1").mkdir(parents=True)` and
  `(source / "t" / "p1" / "basetemp.txt").write_bytes(b"suite base temp\n")`; in
  `_write_citation_oracle_receipt` (`:488–530`) compute
  `suite_basetemp = (target / ".novc").resolve() / "t"` and pass
  `accepted=path != suite_basetemp and suite_basetemp not in path.parents` where the four accepted
  lines pass `accepted=True`. The `t` spellings are then written into the receipts but must not be
  detected, and `assert_retained` still proves `t` relocated byte for byte. Run the simulation, the
  policy lint and, later, the full suite. This test function is also finding 6.3's; make both
  changes in one commit.
- Documentation, editorial: gate 4 of `mam-repository-topology`'s `references/repository-maintenance.md`
  and hazard H2 of the maintenance runbook; their wording is under "Editorial proposals: agent
  instructions" and "Sites found while planning" (flagged site 7). Commit gate 4's wording, and H2's
  if Ben approves it, with this change.

**Finding 14.1, `py/tests/test_h_dot_below_nfc.py:281–287`.** Remove `"google/"` and `"plain/"`
from `_MAM_PARSED_EXCLUDE_DIR_PREFIXES`, leaving `("historical/", "plus/", "py-examples-out/")`. No
tracked file lies under either prefix. Verification: the test passes with the same eight MAM-parsed
files in scope.

**Finding 14.2.** Delete the unused import `iter_template_objects` (`py/verify_mp/verifiers_plus.py:14`);
delete `JSON_BOOK39_SKEL_COMMON` (`py/author_misc/mp_cmn_top_header_book39.py:13–15`) and its snippet
`py/author_misc/json_snippets/top_header_book39/book39_skel_common.json`. Nothing lists or globs the
snippet directory, and no test names the snippet; the historical receipt
`in/mam_products_phase6_baseline.json`, which names its path, stays as written. Verification: ruff
as under finding 1.2; the documentation that `py/main_parse.py ws` regenerates is unchanged.

**Finding 15, `py/verify_mp/parser_stage.py:203–210`.** `_validate_no_parser_stage_encoding`
recurses through `dict` and `list` only, and every plus verse row is a tuple.
- Fix: `:208` becomes `elif isinstance(node, (list, tuple)):`. Nothing else in the walker assumes a
  list.
- Verification: `py/main_parse.py ws` passes on current data (over all 23,202 rows the patched walk
  took 0.07 s on 2026-09-30); as a scratch check, `{"stmpl": "x"}` injected into Genesis 1:1's E
  cell, or into parameter 1 of its first E template, now makes `validate_plus_conversion` raise.

**Finding 16, the parser-stage grammar lock.** `py/verify_mp/expanded_stack_grammar_parser_stage.lock.json:2`
names `py/main_tmpl_survey.py`, which writes only the plus lock, and nothing regenerates this one.
Mirror the plus lock's workflow with a flag on the program whose run checks the lock:
- `py/main_parse.py`: add `--write-parser-stage-grammar-lock` to the existing mutually exclusive
  group of the `ws` subcommand (`:48–50`), with the help text "Infer the transient parser stage's
  expanded stack grammar from all 24 book groups, write its lock file, and validate the current run
  against that lock."; pass it on from `_run_ws` (`:73–74`); add the command to the module
  docstring's examples (`:10–13`).
- `py/subcommands/parse_ws.py` and `py/subcommands/parse_ws_products.py`: pass the keyword through
  `almost_main`, `generate_production` and `generate`. When it is set, `almost_main` refuses at its
  top, after `:17–19` and before it writes any fmt-1 or fmt-2 output, unless every book is
  selected; the refusal is defensive, since the mutually exclusive group already rejects the flag
  beside `--book39` or `--section6`. Then `generate` writes the lock from all 24 in-memory
  parser-stage groups before the per-group loop, which validates each group against the new lock
  as it does today.
- `py/verify_mp/parser_stage.py`: add `from mb_cmn import file_io`, which the module does not yet
  import (ruff would report F821); split `validate` (`:185–200`) so a helper returns `stack_counts`
  and `mpasuq_calls`, and, once finding 17 lands, finding 17's D-label projections beside them;
  add `write_expanded_stack_grammar_lock(sections)`, which sums the helper's counts, infers the
  grammar with `nesting_normal_form.infer_expanded_stack_grammar`, and writes
  `{"provenance": "This file was generated by MAM-basics/py/main_parse.py ws --write-parser-stage-grammar-lock.", **grammar}`
  with `file_io.json_dump_to_file_path` and no `generator_file`. Findings 16 and 17 both rework
  `validate` and `_validate_book39`; implement finding 16's split first and add finding 17's
  projections to the same helper.
- `py/tests/test_mega_coverage.py`, `NOT_IN_MEGA`: add the mode beside `"py/main_parse.py ws --write-fmt-1"`
  (`:343–347`), with the reason given under "Python comments and docstrings" below.
- Verification: run `./.venv/Scripts/python.exe py/main_parse.py ws --write-parser-stage-grammar-lock`
  once, either before finding 1.1's source change or after 1.1's regenerated products are
  committed, since the run regenerates every product; the lock's diff must then be line 2 alone (on
  2026-09-30 the inferred grammar, 173 edges and 196 order pairs, reproduced the rest of the file
  byte for byte), and no product may change. Then `py/tests/test_mega_coverage.py` and, later, the
  full suite and the mega's parse-ws step.

**Finding 17, `validate_plus_conversion` (`py/verify_mp/parser_stage.py:242–249`).** It compares
only the aliyah records, so removing or changing a `סדר` parameter, or dropping a `סדר`-only label,
passes. Under the approved recommendation, compare every D-column label parameter:
- Projection, with closed dispatch, computed for each true verse on both sides and compared as
  `(wrapped, labels)`:
  1. The `נוסח` template: its parameters must be exactly 1 and 2. Parameter 1 must be
     one `מ:פסוק`, which is projected; parameter 2 is the documentation note, named as not a
     label parameter and excluded.
  2. The `מ:פסוק` template: parameters 1 to 3, the coordinates, are skipped because the
     collectors already check them; `סדר` projects to its string, and `עלייה` projects
     through `מ:עלייה`.
  3. The `מ:עלייה` template: each of `א`, `ב0` to `ב3` and `ג0` to `ג3` projects to its string.
  4. Any other template or parameter raises `ValueError`. An empty plus D projects to
     `(False, {})`, as a bare parser-stage `מ:פסוק` does.
- Placement: in `py/verify_mp/parser_stage.py`, not in the collectors, whose plus copy also feeds
  the plus survey's output. `_validate_book39` records the parser-stage projections, `validate`
  returns them as `"d_labels"`, the plus walk collects its own, and `validate_plus_conversion`
  asserts equality after `:249`, naming the first differing verse and both projections.
- Verification: `py/main_parse.py ws` passes (both projections agreed on all 23,202 verses on
  2026-09-30, in about 0.24 s); as a scratch check, turn 01's three mutations at Genesis 8:1 and a
  changed `ב0` at Genesis 2:4 now raise.

**Finding 25, time bounds in `py/repo_util/forest_sync.py` and `py/repo_util/forest_environments.py`.**
Nine of the thirty process launches run Git with no timeout; none of the nine touches the network.
Under the approved recommendation:
- Define `GIT_TIMEOUT_SECONDS = 60` in `forest_environments.py` and add it to `forest_sync.py`'s
  existing `from repo_util.forest_environments import (…)` list (`:17–21`), or ruff reports F821;
  use it at `forest_sync.py:31` in place of the literal, and pass it as `timeout_seconds=` at
  `forest_sync.py:93`, `:139`, `:144` and `:161` and at `forest_environments.py:153` and `:180`.
- Give `worktree_retirement_git._git` two keyword-only parameters,
  `timeout_seconds: int | None = None`, the type `user_config_sync._run_git` uses (`:208`), and
  `noninteractive: bool = False`; when `noninteractive` is set, pass an `env` copy with
  `GIT_TERMINAL_PROMPT=0` and `GCM_INTERACTIVE=Never`, the pair `user_config_sync._run_git` sets
  (`:211–212`). Forward both through `_git_ok`, `_list_worktrees`, `_status_entries` and
  `_operation_markers`, and pass `timeout_seconds=GIT_TIMEOUT_SECONDS, noninteractive=True` at
  `forest_sync.py:112`, `:113` and `:120`. With the defaults every other caller runs exactly as
  today.
- `doc/clone-forests.md:66`'s sentence stays, and becomes true with this fix.
- Verification: a new lint, `py/tests/test_forest_subprocess_bounds.py`, walks the two modules'
  syntax trees and fails unless every `subprocess.run` passes `timeout=` and `env=`, every
  `_run_git` call passes `timeout_seconds=`, every call of the three helpers passes both new
  arguments, and every other launch is a call of one of the modules' own wrappers,
  `forest_sync._git` or `forest_environments._run_python` (18 of today's 30), whose bodies are the
  `_run_git` and `subprocess.run` calls checked above. Any other launcher fails it: a `subprocess`
  function other than `run`, `os.system`, `os.popen`, an `os.spawn*` or `os.exec*` function, or a
  function imported from `repo_util.user_config_sync`, `repo_util.worktree_retirement_git` or
  `repo_util.worktree_retirement_inspection` other than `_run_git`, `_command_error` and the three
  helpers. A scan that finds no calls fails. Then `py/tests/test_worktree_retirement_policy.py` and
  the full suite. No test exercises either forest module's behaviour (item 36.6, deferred).

**Finding 26, the write form of the forest synchronizer (`_sync_repo`, `py/repo_util/forest_sync.py:174–237`,
whose path for an existing clone is `:194–237`).** It fetches before judging a clone's own state.
Under the approved recommendation:
- In the write form, after the snapshot and runtime reads (`:197–198`), which follow the origin
  check (`:195–196`), and before `_fetch_main` (`:199`), compute the reasons a clone's own state
  decides (branch other than `main`, dirty, Git operation or lock in progress, and the runtime
  blockers) and, if any applies, print the `FOREST_REPO` line without ahead or behind and raise,
  with the message "…; not fetched; checkout and environments left untouched".
- Otherwise fetch, count ahead and behind, print, and add the ahead reason. That refusal's message
  becomes "unpushed or divergent commits; fetched origin/main (any missing objects, FETCH_HEAD, and
  refs/remotes/origin/main created or fast-forwarded); local branches, checkout and environments
  left untouched". "Local" is needed because the remote-tracking ref did change, and `_fetch_main`
  creates that ref when it is absent (`:144–147`, `:168–170`). The recheck at `:234–235` stays.
- The check form keeps its flow and output and still fetches every clone.
- Texts that change, worded under "Editorial proposals: procedure documents, runbooks and plans"
  and "Editorial proposals: Python comments and docstrings": `doc/clone-forests.md:36–38`, the
  module docstring (`:5–6`), `py/main_repo_util.py:44–45` and the maintenance runbook's
  `--sync-forest` rows.
- Verification: by reading, with Black and the full suite. Do not run the write form. No test
  exercises `forest_sync`'s behaviour; finding 25's lint checks only its launch bounds (item 36.6,
  deferred).

### Editorial proposals: agent instructions (D7: editorial)

#### Repository `AGENTS.md`

1. **Finding 11, "Writing tests: differential and lint-shaped only" (`:230–235`).** At `:233`, "The
   `ws_bot` tests remain the deliberate exception" becomes "The `ws_bot` tests remain a deliberate
   exception", and after the sentence ending "with no regeneratable artifact." insert:

   > By Ben's decision of 2026-09-30, the five stub test ids of
   > `py/tests/test_wikisource_special_page_download.py` are a second exception. Its four
   > fault-injection ids hold five cases: each checks that a bad API response or bad local metadata
   > makes the special-page download raise, and all but the last, a manifest overwritten with "not
   > json", also check that no mirrored file changed, a property with no regeneratable artifact. Its
   > round trip is the only offline check of the download's reuse and forced refresh, neither of
   > which a regenerated mirror's diff would show.

   The test module gains a docstring in the "BLESSED EXAMPLE-BASED BAND" form that
   `py/tests/test_mb_cmn_paths.py:6–12` uses, given under "Python comments and docstrings". No test
   changes under this item; flagged site 11 proposes a fix to the last case.
2. **Finding 12, "MAM special pages are mirrored with every Wikisource chapter download" (`:76–78`).**
   Current: "`py/ws/ws_special_page_download.py` owns the literal inventory, checks it against the
   two tables in `in/mam-ws-intro/ch2.mediawiki`, and permits only the eight declared identities to
   overlap the chapter mirror." Proposed: "`py/ws/ws_special_page_download.py` owns the literal
   inventory and permits only the eight declared identities to overlap the chapter mirror. It
   checks the inventory against chapter 2 of the mirrored introduction,
   `in/mam-ws-intro/ch2.mediawiki`: the Decalogue section's table and the paragraph after it, and
   the song-form table."
3. **Finding 34.1 (`:130–131`).** Current: "Load `mam-repository-topology`, “Manual document
   retirement”, before retiring a receipt family or carrying out Ben-authorized reclassification."
   Proposed: "Load `mam-repository-topology/references/repository-maintenance.md`, “Manual document
   retirement”, before retiring a receipt family or carrying out Ben-authorized reclassification."
   This is the form `dot-claude/skills/github-issues/references/reading-and-writing.md:149` already
   uses.
4. **Item 36.2, "What this repository's products are, and which check a change owes" (`:163–165`).**
   Current: "A change to a hand-run generator, or to any input it reads, requires rerunning every
   affected hand-run generator and inspecting its tracked outputs. Product reach and whether an act
   is hard to undo are separate risk axes, as the user-level instructions explain." Proposed:

   > A change to a hand-run generator, or to any input it reads, requires rerunning every affected
   > hand-run generator and inspecting its tracked outputs, with two exceptions that Ben decided. A
   > refresh of MAM's text does not oblige rerunning `py/main_mam4sef.py` or `py/main_mam_osis.py`
   > (his decision of 2026-09-30), so MAM-for-Sefaria and MAM-OSIS may lag MAM-simple, as their
   > READMEs say; any other change to either generator or its inputs still does. A change to MAM's
   > data does not oblige rerunning `py/main_hbce_psalms.py compare` (his decision of 2026-09-26,
   > in the HBCE section above). Product reach and whether an act is hard to undo are separate risk
   > axes, as the user-level instructions explain.

#### The common body, `dot-Codex/user-wide-AGENTS.md`

Deployed to `~/.codex/AGENTS.md`, and to Claude through the wrapper, by `--sync-user-config`. It is
26,077 bytes, loaded outside Codex's project-instruction budget (`dot-Codex/README.md:81–83`).

1. **Findings 2.5 and 33, "Git and commits", the bullet at `:83–86`.** Current: "- Integrate a
   worktree branch immediately before the task is archived, or earlier only when Ben asks or a
   concrete dependency requires it. Load `codex-worktree-tasks` and follow the repository's
   integration check. The worktree's home clone receives only a verified fast-forward, then `main`
   is pushed." Proposed:

   > - Integrate a worktree branch immediately before the task is archived, or earlier only when Ben
   >   asks or a concrete dependency requires it. Follow the repository's integration check and the
   >   linked-worktree safeguards below; ChatGPT-Codex also loads `codex-worktree-tasks`. The
   >   worktree's home clone receives only fast-forwards, to a freshly fetched `origin/main` and to
   >   the verified worktree branch, and then `main` is pushed.

2. **Finding 33, "Clone forests and portable work", `:125–128`.** Current: "Before pushing a full
   clone's `main`, fetch `origin`, merge `origin/main` if it moved, and run the checks owed by the
   resulting changes, including the mega when owed. Push normally. If the push is refused because
   origin moved, repeat the fetch, merge and affected checks in that full clone. Do not rewrite
   history or discard work to make the push pass." Proposed:

   > In ordinary work in a full clone, fetch `origin` before pushing `main`, merge `origin/main` if
   > it moved, and run the checks owed by the resulting changes, including the mega when owed. Push
   > normally. If the push is refused because origin moved, repeat the fetch, merge and affected
   > checks in that full clone. When a worktree integrates into its home clone, the home clone takes
   > no merge: worktree integration follows the linked-worktree safeguards below. Do not rewrite
   > history or discard work to make the push pass.

3. **Finding 32, the same section, `:133–135`.** Current: "Inputs outside every repository are
   user-level inputs reachable by every forest on that machine, discovered through explicit account
   configuration such as `BOOK_SCANS_ROOT` or the user's pywikibot configuration." Proposed:

   > Inputs outside every repository are user-level inputs reachable by every forest on that
   > machine. The scan archive is at `$HOME/OneDrive/Documents/ScansOfBooks` by default, and
   > `BOOK_SCANS_ROOT` overrides that location; other such inputs, such as the user's pywikibot
   > configuration, are found through explicit account configuration.

   This matches `py/mb_cmn/paths.py`'s `book_scans_root` (`:119–136`); no code or machine changes.
4. **Finding 33, "Linked-worktree safeguards shared by Claude and Codex", `:166–168`.** Current: "If
   the worktree's home clone refuses the final fast-forward, return to the development worktree,
   merge the new main there, and repeat the applicable checks. Do not replace the failed
   fast-forward with a merge in the worktree's home clone." Proposed:

   > Before integrating a worktree, fetch `origin` in its home clone and fast-forward the home
   > clone's `main` if `origin/main` moved. Immediately before the final fast-forward, fetch again;
   > if `origin/main` is not then an ancestor of the worktree branch, merge it in the development
   > worktree and repeat the applicable checks. If the home clone refuses the final fast-forward
   > because its `main` moved, or its push of `main` is refused because `origin/main` moved, return
   > to the development worktree, fetch `origin`, merge the moved branch there, repeat the
   > applicable checks, and fast-forward again. Do not replace a failed fast-forward or push with a
   > merge in the worktree's home clone.

5. **Finding 34.1, "Plans and finished dated records", `:294–295`.** The same replacement as in
   `AGENTS.md`: "Load `mam-repository-topology/references/repository-maintenance.md`, “Manual
   document retirement”, before retiring a receipt family or carrying out Ben-authorized
   reclassification."
6. **Finding 2.5, "Format changed Python with Black", `:301–302`.** Current: "In a worktree, use the
   worktree's home clone's interpreter by absolute path as `codex-worktree-tasks` specifies."
   Proposed: "In a worktree, use the worktree's home clone's interpreter by absolute path, as the
   linked-worktree safeguards say."

The Codex-addressed routings at `:80–82`, `:170–171` and `:224–225` stay. `AGENTS.md`'s integration
section ("after merging the home clone's `main` into the worktree branch", `:188`) stays true under
item 4, since the home clone's `main` is first fast-forwarded to the fetched `origin/main`.

#### Codex's `codex-worktree-tasks` skill, `references/task-lifecycle.md` (finding 33)

Under "## Integrate immediately before archival", replace the lead-in, the numbered list and the
paragraph after it (`:47–59`), keeping the heading:

> Once the worktree and home clone are clean:
>
> 1. In the worktree's home clone, fetch `origin`. If `origin/main` moved, fast-forward `main` with
>    `git -C <home-clone> merge --ff-only origin/main`.
> 2. In the worktree, merge `main` into the worktree branch. Resolve conflicts and make any fixes on
>    that branch.
> 3. Run the repository's required broad check on the merged branch. Commit every explained
>    generated change there; an unexplained change is a failure.
> 4. In the worktree's home clone, fetch `origin` again. If `origin/main` is not an ancestor of the
>    worktree branch, merge `origin/main` into the worktree branch in the worktree and return to
>    step 3. Otherwise fast-forward `main` with `git -C <home-clone> merge --ff-only <worktree-branch>`.
>    If `main` moved, return to step 2 instead of creating a merge in the worktree's home clone.
> 5. Push `main` normally. If the push is refused because `origin/main` moved, return to step 4.
>
> The worktree's home clone receives only fast-forwards: to a freshly fetched `origin/main` and to
> the verified worktree branch. Removing the worktree and deleting its branch wait until the task
> has ended on Windows; never force removal around a live process.

After a refused push, step 4's merge in the worktree makes the new worktree branch a descendant of
the home clone's `main`, so the home clone fast-forwards again without a merge of its own.

#### The `hebrew-prose` skill

1. **Finding 8.2 (question 5), the description in `SKILL.md:3`.** Current, final sentence: "Also use
   for manuscript-versus-transcription prose beyond accentuation." Proposed: "Also use for
   manuscript-versus-transcription prose beyond accentuation, and for any prose that names a
   manuscript page or folio, such as "page F159A"."
2. **Question 5, `SKILL.md`, "Load only the references the task needs".** Add, after the entry for
   `references/terminology.md`:

   > - **A manuscript page or folio locator, such as "page F159A":** read `references/terminology.md`,
   >   “A manuscript page is named as a page, never as "folio 57a"”.

3. **Question 5, `references/terminology.md`, a new section after `"The LC," not bare "L"`
   (`:424–429`):**

   > ## A manuscript page is named as a page, never as "folio 57a"
   >
   > Ben's terminology, 2026-09-27: a **folio** is one leaf of a manuscript, and it has two
   > **pages**, its A and B sides, a recto and a verso. A page identifier, which carries the side,
   > names a page. So write "page F159A", or just "F159A", for the Leningrad Codex, never "folio
   > 159A", and "page 83r" for the Aleppo Codex, never "leaf 83r". Each manuscript keeps its own form
   > of page identifier: "F159A" in the Leningrad Codex, "83r" in the Aleppo Codex, "0073B" in
   > Cambridge Add. 1753 and "57a" in Evr. II B 55. "Folio" and "leaf" stay the words for the leaf
   > itself: a folio number, a count of folios or leaves, the two pages of one folio.
   >
   > Published books and web sites often write "folio 57a". Ben, the same day: *"One more note
   > regarding phrases like "folio 57a". I think we should avoid them, but they are common in
   > existing references in published books and web sites. They should be taken to imply a
   > parenthesized meaning of "(folio 57)a""*, the A page of folio 57. A quotation or citation of
   > such a source keeps its wording, as a catalog's "fol. 78b" does where the catalog is cited;
   > this repository's own prose avoids the form.
   >
   > The decision's record is item 4 of the first entry of MAM-basics'
   > `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`, which also says why Ben's first
   > statement there is not quoted as exact.
   >
   > Swept on adoption: the maintained prose, skills and tool messages that called a page a folio
   > or a leaf. **Not** swept, and worth offering when touched: the generated Holman
   > UXLC-corrections page's "folio 035A" links, its "Holman cites folio …" notes and its
   > introduction's "folio link" (`py/py_render/uc_case_card.py` and `py/py_render/uc_html.py`);
   > the "folio col line" row label of the generated WLC a-notes full-record pages
   > (`py/py_wlc_a_notes/my_wlc_a_notes_full.py`); the generated goerwitz page's "folio 009B"
   > (`py/accgram/prose_ob_notes_gn.py`); the note of `holman/data/uxlc_atom_locations.json` that
   > `py/main_estimate_uxlc_locations.py` writes; and the note in
   > `evr-ii-b-55/evr-ii-b-55-page-index.json`. Receipts, among them the dated Holman research
   > records under `holman/doc/`, and external captures keep their words, and so does wording that
   > follows a source's own term or citation form: the "LC folio index" that `in/lci_recs.json`
   > compiles, the "folio references" of MAM's daf-and-amud citations such as `(8ב)`, and a
   > catalog's "fol." locators.

   Under that last clause these stay: `DATA-LICENSES.md:67`, "a table of Leningrad Codex folio
   locations", after the title of `LCIndex.xml`, "LC folio index for sefaria.org images";
   `doc/sigil-decoding.md:213–214` and the hand-maintained `gh-pages/MAM-with-doc/sigil-decoding.html:142`
   and `:148`, "folio references such as `(8ב)`"; and `evr-ii-b-55/README.md:474`, "identify those
   folios", after the catalog's "fol. 1a" and "fol. 79a". The dated Holman research records,
   `holman/doc/holman-manuscript-citations.md` and `holman/doc/uxlc-email-count-disagreements.md`
   ("Measured 2026-08-12", with no `State:` line), are read as receipts and keep their words.

4. **Question 5, `references/sources-and-corpora.md:46`.** Current: "pending a look at folio 009B
   rather than `lc`." Proposed: "pending a look at page F009B rather than `lc`."
5. **Finding 4.5, `references/mam-basics.md:34–36`.** Current: "His 2026-08-11 al-hatorah decision
   covered seven historical accgram citations and one test site; only three of those eight sites
   literally used `../al-hatorah/...`." Proposed: "His 2026-08-11 al-hatorah decision named seven
   sites, six historical accgram citations and one test site; a re-measurement on 2026-09-12 found
   an eighth, `post_stress_meteg.py:15`, written after the decision, and only three of the eight
   literally used `../al-hatorah/...`." Sources: `73f8ea3c:CLAUDE.md:122–128` names the seven, and
   `bca64824:CLAUDE.md`, "Eight sites", the re-measured eight.
6. **Finding 28.3, `references/verifying.md:118–125`.** Current path: "run with the cwd at that
   tree's own root — `C:/Users/BenDe/GitRepos/MAM-private/masorah-books` since the tree moved into
   `MAM-private` on 2026-08-10, never MAM-private's root —". Proposed: "run with the cwd at that
   tree's own root — `<forest>/MAM-private/masorah-books` since the tree moved into `MAM-private` on
   2026-08-10, never MAM-private's root —", so that the dating clause stays attached to the path;
   and, after the code block that follows (`:123–125`), a new paragraph: "`<forest>` is the
   directory holding the invoking checkout's home clone, `$HOME/GitRepos` or `$HOME/GitRepos<N>`."
7. **Finding 34.3, `references/verifying.md:96–98`.** Current: "so while this paragraph read "Never"
   the skill contradicted the repo's own instruction file." Proposed: "so while this reference
   carried the worktree ban withdrawn on 2026-09-09, which read “Never from a git worktree, only from
   that repo root”, the skill contradicted the repo's own instruction file." The paragraph at
   `:90–98` never held the ban itself; the quoted ban is the text `0e254fdc` removed from an earlier
   paragraph (`0e254fdc^:dot-claude/skills/hebrew-prose/references/verifying.md:54–56`).

#### The `verse-links` skill (question 5)

1. `SKILL.md:3`, the description. Current: "Sefaria's image of the Leningrad Codex folio with the
   atom's estimated column and line". Proposed: "Sefaria's image of the Leningrad Codex page with the
   atom's estimated column and line".
2. `SKILL.md:70`, the table row. Current: "| `LC <folio>` | Sefaria's image of that Leningrad Codex
   folio, with the estimator's column and line for the atom; a verse crossing a page break gets two
   such lines |". Proposed: "| `LC F<page>` | Sefaria's image of that Leningrad Codex page, with the
   estimator's column and line for the atom; a verse crossing a page break gets two such lines |".
3. `SKILL.md:87–88`. Current: "holds for a manuscript folio as well." Proposed: "holds for a
   manuscript page as well."
4. `SKILL.md:94–95`. Current: "The folio comes from the UXLC's page index". Proposed: "The page
   comes from the UXLC's page index".
5. `dot-claude/README.md:60`, the skill's row. Current: "Sefaria's image of the Leningrad Codex folio
   with the estimator's column and line". Proposed: "Sefaria's image of the Leningrad Codex page with
   the estimator's column and line".
6. Found after the planning answer, `SKILL.md:75–76`. Current: "when a session offered to download a
   leaf of each codex:". Proposed: "when a session offered to download a page image from each
   codex:". Ben's quotation after it stays.
7. The generator, `py/main_verse_links.py`, whose wording is under "Python comments and docstrings".

#### The `mam-wikisource-refresh` skill (finding 23)

In "## After a Wikisource bot run", `SKILL.md:82–85`. Current: "unless `--no-post-download` is given,
it force-downloads exactly the chapters it saved into `in/mam-ws/` and `in/mam-ws-revisions.json`,
then reparses those books. That download takes the place of the one above." Proposed: "unless
`--no-post-download` is given, it calls `download_wikisource.run`, the function every
`fr-wikisource` download runs, with a forced download. That download refetches all 36 declared
special pages into `in/mam-ws-special/`, then force-downloads exactly the chapters the bot saved
into `in/mam-ws/` and `in/mam-ws-revisions.json`, and reparses those books. It takes the place of
the one above." Sources: `py/subcommands/ws_bot_real.py:270` and
`py/subcommands/download_wikisource.py:18–61`.

Open for Ben, not worded here: the skill's post-bot section says the dependent refresh's first
commit is "the bot run's own record, the saved chapters' regenerated outputs with a new entry in
`py/ws/ws_bot_edit_history.md`", and nothing says which commit takes a special page that this
download changes. This plan proposes no rule for it.

#### The `mam-repository-topology` skill

1. **Finding 34.1, `SKILL.md:21–22`.** Current: "5. Read `references/repository-maintenance.md` for a
   maintenance sweep, Black coverage, or retirement of selected linked worktrees, completed Codex
   task folders and disposable cache data." Proposed: "5. Read `references/repository-maintenance.md`
   for a maintenance sweep, Black coverage, manual document retirement, or retirement of selected
   linked worktrees, completed Codex task folders and disposable cache data." Finding 34.1 offered
   two remedies, naming the reference in the four citations or routing document retirement to it
   from the skill; this plan does both.
2. **Finding 7, `references/repository-maintenance.md:104–108`, gate 4.** Current last sentence:
   "Generic `.novc` policy prose does not gate." Proposed: "Generic `.novc` policy prose does not
   gate, and neither does a spelling of the target's root `.novc/t` or of anything below it, where
   `py/main_test.py` puts the suite's per-process base temporary directories on Windows: that subtree
   is disposable cache, relocated with the rest of `.novc` but never a citation. Every other retained
   child keeps gating."
3. **Finding 28.3, `references/evacuated-repositories.md`, the five clone commands at `:61`, `:106`,
   `:136`, `:201` and `:221`.** Each has the form
   `git clone --depth 1 https://github.com/bdenckla/<repo>.git C:/Users/BenDe/GitRepos/<repo>`.
   Proposed: replace `C:/Users/BenDe/GitRepos/<repo>` with `<forest>/<repo>` in all five, and after
   the first of them, the code block at `:60–62` below "It raises with the command that fixes it:",
   add the definition: "In this command and the four below, `<forest>` is the directory holding the
   invoking checkout's home clone, `$HOME/GitRepos` or `$HOME/GitRepos<N>`, which is where
   `py/redirect_stubs/stubs.py`'s `source_pages_dir` looks, through `paths.sibling_repo`; the
   program's own message prints the exact path." Sources: `py/redirect_stubs/stubs.py:479–497`.

#### The `github-issues` skill (finding 34.2)

`references/reading-and-writing.md:63–66`. Current: "2. **A `doc/review-findings-*.md` file gets no
issue.** Its `State:` line carries open or closed. The thin tracking issues the reviews used to file
were retired on 2026-09-01, and `doc/dual-agent-review.md`, “Review filenames and State lines”, owns
the review State rule; `check_repo_standards.py` retains the dated rationale." Proposed: "2. **A
review file gets no issue**, whether it is a single-agent or blind review file or a numbered
dual-agent turn. Its line-3 `State:` follows `doc/dual-agent-review.md`, “Review filenames and State
lines”, and later remediation State and every disposition belong in the first review file's single
live update file. The thin tracking issues the reviews used to file were retired on 2026-09-01;
`check_repo_standards.py` retains the dated rationale." The rest of the item, from "A review that
finds work somebody must do", stays, and so does the dated rationale in
`py/repo_util/check_repo_standards.py:280–284`, which describes the convention as it stood.

#### The `iterative-document-editing` skill (finding 34.1)

`SKILL.md:70–71`. Current: "Load `mam-repository-topology`, “Manual document retirement”, for
retirement references and Ben-authorized reclassification." Proposed: "Load
`mam-repository-topology/references/repository-maintenance.md`, “Manual document retirement”, for
retirement references and Ben-authorized reclassification."

#### The configuration READMEs (finding 29; not deployed)

1. `dot-Codex/README.md:123–124`. Current: "The read-only form reports `clean`, `drift`, or `not
   installed` for every Claude and Codex destination:". Proposed: "The check form, which fetches
   `origin` but changes no live configuration, reports `clean`, `drift`, or `not installed` for
   every Claude and Codex destination:".
2. `dot-claude/README.md:88–89`. Current: "The read-only form uses the same fresh source and reports
   `clean`, `drift`, or `not installed` for every destination:". Proposed: "The check form, which
   fetches `origin` but changes no live configuration, uses the same fresh source and reports
   `clean`, `drift`, or `not installed` for every destination:".

Both follow the common body's "Its `--check` mode fetches and compares without changing live
configuration." (`dot-Codex/user-wide-AGENTS.md:22–23`).

### Editorial proposals: procedure documents, runbooks and plans (D7: editorial)

#### `doc/dual-agent-review.md`

1. **E1, the D9 paragraph at `:147–149`.** Current: "**Every turn is review only and, in this
   repository's series, uses public evidence only.** It performs no remediation and does not rewrite
   an earlier turn. A correction belongs in the turn that accepts the correction." Proposed:

   > **Every turn is review only and, in this repository's series, uses public evidence only.**
   > "Public evidence only" means that the turn reads nothing in MAM-private: the series'
   > public-only property, as `doc/periodic-review.md`, "Two standing properties of the series",
   > states it. A claim that only an agent transcript can check stays out of a tracked turn under
   > D11, "The shared origin branch" below. A turn performs no remediation and does not rewrite an
   > earlier turn. A correction belongs in the turn that accepts the correction.

   This is the reading turns 07 and 08 agreed. Only `:147–149` change; the paragraph's next three
   lines, from "Turn 2's initial reconciliation", stay.
2. **Finding 34.1, `:174–175`.** Current: "Load `mam-repository-topology`, “Manual document
   retirement”, for receipt-family retirement and Ben-authorized reclassification." Proposed: "Load
   `mam-repository-topology/references/repository-maintenance.md`, “Manual document retirement”, for
   receipt-family retirement and Ben-authorized reclassification."
3. **Finding 35, the September 16 paragraph, `:286–288`.** Current: "The package makes the shared
   review branch subject to the backup exception recorded above and reserves all other remediation
   for a fresh-task plan with concrete editorial wording." Proposed: "The package made the shared
   review branch subject to the user-level backup exception that D11 then named; D11 now puts the
   review branch under the user-level shared-remote-branch exception instead. The package reserved
   all other remediation for a fresh-task plan with concrete editorial wording." D11 moved the
   review branch from one exception to another rather than renaming an exception.
4. **This round's procedure record**, which the paragraph beginning "After the exchange closes"
   (`:154–160`) requires after Ben's decisions: a new subsection after "### The September 16 round"
   and before "### Remediation approvals: D7 and the risk ordering":

   > ### The September 29 round
   >
   > The September 29 round reviewed MAM-basics `f4d81285..7549ebf7`. Claude was Agent 1 and wrote
   > the odd turns; Codex was Agent 2 and wrote the even turns. Every turn ran in the full clone
   > `C:/Users/BenDe/GitRepos2/MAM-basics`, on a carrier for `origin/dar-2026-09-29`, under Ben's
   > decision of 2026-09-29 that by default a review runs in whatever checkout its session is already
   > in. Turn 01's session had first made a linked worktree for the round and run only the suite
   > there; at Ben's instruction that session removed the worktree before any of turn 01's review
   > streams started. Turns 04 to 10 also settled the times that turns 03 and 05 gave for their own
   > work: turn 03's two New York times, for its writing and for its listing of an untracked file,
   > fell after its own commit; turn 05's "at about 16:15" was shown neither wrong nor right; and
   > the public record, meaning Git's commit times and GitHub's activity record for the branch,
   > supports only an interval for each turn. Turns 09 to 11 ran at each agent's top effort level, as
   > Ben decided on 2026-09-30. Turn 10 accepted every point of turn 09 and listed no unresolved
   > disagreement, and turn 11 acknowledged turn 10 without an objection. Ben answered the close-out
   > package's six questions and, in its seventh, approved the package on 2026-09-30; his decisions
   > are recorded in `doc/dual-agent-review-2026-09-29-turn-01-claude-update.md`. The package
   > reserved every fix for the fresh-task remediation plan,
   > `doc/PLAN-remediate-review-findings-2026-09-29.md`.

#### `doc/clone-forests.md` (finding 26)

`:36–38`. Current: "Eligible clones are fetched and fast-forwarded. Ineligible clones and their
environments stay untouched; other roster entries continue." Proposed:

> Eligible clones are fetched and fast-forwarded. A clone that is dirty, off `main`, mid-operation,
> locked or occupied is refused before any fetch. A clone refused only because its history is ahead
> of or diverged from `origin/main` is fetched first: the fetch adds any missing objects, rewrites
> `FETCH_HEAD`, and creates or fast-forwards `refs/remotes/origin/main`. A clone whose
> `origin/main` history was rewritten is fetched and refused with that ref retained. Every refused
> clone keeps its local branches, checkout and environments; other roster entries continue.

"Locked" is `_snapshot`'s lock files and "occupied" the runtime blockers of `_runtime`; the
rewritten-history refusal is `_fetch_main`'s (`py/repo_util/forest_sync.py:92–133` and
`:160–165`). The check form's paragraph (`:20–23`) and the sentence at `:66` stay.

#### `doc/PLAN-repo-maintenance-across-GitRepos.md`, a runbook (finding 28.4)

Every command below runs from the root of a full MAM-basics clone, so relative paths replace the
pinned primary-forest ones.

1. `:335–336`: `git -C C:/Users/BenDe/GitRepos/MAM-basics worktree list` becomes
   `git worktree list`, and `git -C C:/Users/BenDe/GitRepos/MAM-basics branch --list "claude/*"`
   becomes `git branch --list "claude/*"`.
2. `:343`: `Get-ChildItem -Directory C:/Users/BenDe/GitRepos` becomes `Get-ChildItem -Directory ..`,
   the invoking clone's forest; the rest of the command stays.
3. `:360–361`. Current: "Run everything from `C:/Users/BenDe/GitRepos/MAM-basics` with
   `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`." Proposed: "Run everything from the
   root of a full MAM-basics clone, in any forest, with that clone's own `./.venv/Scripts/python.exe`;
   a repository sweep covers that clone's forest."
4. The action table (`:366–377`): the `--sync-user-config` row's note, "run only from the primary
   MAM-basics clone after the canonical changes are pushed", becomes "run from any full MAM-basics
   clone after the canonical changes are pushed". Add three rows after it, the check and write forms
   of `--sync-forest` apart, as the two `--sync-user-config` rows are:

   > | `--sync-forest ROOT --check` | fetches; no checkout write | fetches every clone of the forest at `ROOT` and reports clone, branch, local-change, Git-operation and environment state, without cloning, merging or installing; see `doc/clone-forests.md` |
   > | `--sync-forest ROOT` | **CLONES, FAST-FORWARDS AND CREATES ENVIRONMENTS** | refuses a dirty, off-`main`, mid-operation, locked or occupied clone before fetching it, and an ahead or diverged clone after fetching it; see `doc/clone-forests.md` |
   > | `--forest-status` | fetches; no checkout write | runs the check form over `$HOME/GitRepos` and each `$HOME/GitRepos<N>`; see `doc/clone-forests.md` |

   The lead-in at `:363–364` becomes "Actions are mutually exclusive, one per invocation. Repository
   sweeps use workspace selection; `--sync-user-config`, the forest actions and exact-target
   retirement actions do not:", since a forest action always takes the complete roster
   (`doc/clone-forests.md:13–14`).
5. `:408`: `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_repo_util.py --inspect-worktrees --worktree-owner both --workspace-file C:/Users/BenDe/GitRepos/MAM-basics/all-repos.code-workspace`
   becomes
   `./.venv/Scripts/python.exe py/main_repo_util.py --inspect-worktrees --worktree-owner both --workspace-file all-repos.code-workspace`.
6. `:415`: "from the primary MAM-basics root:" becomes "from the root of a full MAM-basics clone:".
7. `:418` and `:422`: `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` becomes
   `./.venv/Scripts/python.exe`.
8. `:463`: `git -C C:/Users/BenDe/GitRepos/MAM-basics grep -l "^State: executed" -- "*PLAN-*.md"`
   becomes `git grep -l "^State: executed" -- "*PLAN-*.md"`.
9. `:500`: "Run this search from `C:/Users/BenDe/GitRepos/MAM-basics`;" becomes "Run this search from
   the root of a full MAM-basics clone;".
10. `:504`: `git -C C:/Users/BenDe/GitRepos/MAM-basics grep -n -E …` becomes `git grep -n -E …`,
    with the pattern unchanged.
11. Hazard H6, `:725–727`. Current: "Run from the main clone; if a worktree is unavoidable, pass
    `--repos-root C:/Users/BenDe/GitRepos` explicitly." Proposed: "Run from a full clone; if a
    worktree is unavoidable, pass `--repos-root` explicitly, naming the worktree's home clone,
    against which the roster's `../<name>` folders resolve into its forest." The current value is
    itself wrong, which this proposal flags for Ben: `py/main_repo_util.py:531–536` defaults
    `--repos-root` to the workspace file's directory, and `py/repo_util/repo_selection.py:94–107`
    resolves a folder that does not exist beside the workspace file against it, so with
    `C:/Users/BenDe/GitRepos` the roster's `../MAM-private`, `../phonetic-hbo` and `../hbofonts`
    are looked for in `C:/Users/BenDe`, above the forest, and not found.

The settled baseline command at `:759` stays, as turn 07 set it aside.

#### `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md`, a live plan

Finding 8.1 is Ben's choice here: approval or reversal of the September 9 passages and the hazard-5
re-reading. Finding 2.2 applies under either outcome. If he approves, findings 2.5 and 28.5 and
the extra finding-29 sites apply as below; if he reverses, only finding 28.5 has sites in the
restored text (`git grep` at `93fe8704` finds neither `codex-worktree-tasks` nor "read-only" in
the plan).

**Finding 8.1, for approval or reversal.** The 2026-09-26 remediation (`22d18d72`) added the section
"## Current execution boundary, corrected 2026-09-28" (`:61–67`) and rewrote §1 items 1, 2 and 4
(`:71–84`, `:88–96`), §4 item 6 (`:487–489`) and §5 steps 2 to 4 and 8 (`:499–509`, `:517–523`),
where the approved plan said "For finding 12, update only surviving current section locators." It
also added, to `doc/public-data-consumer-hazards-2026-09-16-update.md`, in its entry "## 2026-09-28:
structural-boundary audience and conditional break encodings" (`:109`), a re-reading of hazard 5
that the plan did not list: the four sentences from "The audit's hazard 5 passage" through "the
representation can also mislead an external MAM-simple consumer." (`:114–119`). The approved changes
`22d18d72` made to the same two files stay under either choice: in the September 9 plan, D4's link
and §5 step 7's locator; in the hazards update, the rest of that entry.

- **Approve as they stand (recommended).** Keep both as written. The rewritten September 9
  procedures state the deployment rules the common body states now: edit canonical sources, deploy
  from fresh `origin/main`, never edit a live copy. Their "the primary clone" and "read-only
  `--check`" have disagreed with the common body since `7cf780e1` (2026-09-29), which findings 28.5
  and 29 correct below. The hazard-5 re-reading agrees with the `hebrew-prose` checklist's paseq and
  legarmeh rule.
- **Reverse.** Remove the September 9 section and restore the eight rewritten passages' text at
  `93fe8704`, the 2026-09-26 plan's approval commit; remove the four hazard-5 sentences, recording
  the removal in a dated entry of the hazards update. The restored §1 item 2 ("**Live-first order,
  for every file that has a live copy.** Edit `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md` and
  `~/.claude/skills/hebrew-prose/`, then copy back…") and §5 steps 2 to 4 would then contradict the
  common body's "never edit either live file directly" (`dot-Codex/user-wide-AGENTS.md:12–13`).

**Findings 2.5, 28.5 and the extra finding-29 sites, applied to the wording as it stands.**

1. §1 item 1 (`:71–78`). Current: "1. **Which checkout.** Use the verified MAM-basics development
   checkout named by the execution task, with one writer. A linked worktree uses the primary clone's
   interpreter `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`, while scripts, checks,
   staging and commits run in that development checkout. Integrate and push `main` before
   deployment. The complete user-configuration deployment runs only from the primary clone,
   `C:/Users/BenDe/GitRepos/MAM-basics`, and installs from fresh `origin/main`; do not substitute a
   worktree path into that deployment. Load `codex-worktree-tasks` for a linked worktree's
   verification and integration procedure." Proposed:

   > 1. **Which checkout.** Use the verified MAM-basics development checkout named by the execution
   >    task, with one writer. A full clone uses its own interpreter, `./.venv/Scripts/python.exe`
   >    from its root; a linked worktree uses its home clone's interpreter by absolute path, while
   >    scripts, checks, staging and commits run in that development checkout. Integrate and push
   >    `main` before deployment. The complete user-configuration deployment runs from any full
   >    MAM-basics clone, never from a worktree, and installs from fresh `origin/main`. A linked
   >    worktree's verification and integration follow the common body's linked-worktree
   >    safeguards and the repository's integration check; ChatGPT-Codex also loads
   >    `codex-worktree-tasks`.

2. §1 item 2 (`:79–84`). Current: "…then run the complete `py/main_repo_util.py --sync-user-config`
   deployment from the primary clone and its read-only `--check`." Proposed: "…then run the complete
   `py/main_repo_util.py --sync-user-config` deployment from a full clone, and its `--check`, which
   fetches and compares without changing live configuration."
3. §5 step 8 (`:517–523`). Current: "The primary checkout receives only a verified `--ff-only`
   integration, followed by a normal `main` push. Run the complete `py/main_repo_util.py
   --sync-user-config` deployment and its read-only `--check` from the primary clone after the
   normal `main` push." Proposed: "The worktree's home clone receives only verified `--ff-only`
   integration, followed by a normal `main` push. Run the complete `py/main_repo_util.py
   --sync-user-config` deployment and its `--check` from a full clone after the normal `main` push."

**Finding 28.5 in the restored text, if Ben chooses reversal.** These replacements, and nothing
else in the restored passages:

1. `93fe8704:63–65`: "Prefer the primary clone, `C:/Users/BenDe/GitRepos/MAM-basics` on `main`: the
   deploy commands and drift checks in `dot-claude/README.md` §"Shared-skill deployment to Claude
   and Codex" name that path," becomes "Prefer a full MAM-basics clone on `main`: the deploy
   commands and drift checks in `dot-claude/README.md` §"Shared-skill deployment to Claude and
   Codex" run there,".
2. `93fe8704:66`: "substitute the worktree path in those commands" becomes "run those commands from
   its home clone".
3. `93fe8704:69–70`: "the primary clone's tracked copies" becomes "the tracked copies". The quoted
   "when a concrete need requires the primary checkout to contain the work" (`:68–69`) stays.
4. `93fe8704:84–85`: "from `C:/Users/BenDe/GitRepos/MAM-basics`, never from `py/`" becomes "from
   the full clone's root, never from `py/`".
5. `93fe8704:87`: "name the primary clone's venv by absolute path" becomes "name the worktree's
   home clone's interpreter by absolute path".
6. `93fe8704:513–516`: "in the primary clone, run" becomes "in a full clone, run"; "the primary
   clone's venv" becomes "the worktree's home clone's interpreter"; and "`--ff-only` in the primary
   clone" becomes "`--ff-only` in the worktree's home clone".

**Finding 2.2, outside 8.1's passages.**

1. §4 item 2 (`:471–475`). Current: "2. **Sections.** All 13 `§"…"` citations resolve, as do
   `clc-design.md` §2 and §7.16, … `review-findings-2026-07-29.md` item 14, … and finding 5.6 and
   row 22 of `review-findings-2026-09-08.md` (`final_checks.py`)." Proposed: "2. **Sections.** On
   2026-09-09 all 13 `§"…"` citations resolved, as did `clc-design.md` §2 and §7.16, …
   [`review-findings-2026-07-29.md`](F/review-findings-2026-07-29.md) item 14, … and finding 5.6 and
   row 22 of [`review-findings-2026-09-08.md`](F/review-findings-2026-09-08.md) (`final_checks.py`);
   `2a051ba5` later retired both reviews, and [the 2026-09-08 review's update](F/review-findings-2026-09-08-update.md)
   with them." The elided citations stay as they are.
2. §7 item 2 (`:596–598`). Current: "`doc/review-findings-2026-09-08.md` is headed "review of the
   public repos"". Proposed: "[`doc/review-findings-2026-09-08.md`](F/review-findings-2026-09-08.md),
   retired by `2a051ba5`, is headed "review of the public repos"".

#### Other maintained documents

1. **Finding 19, `doc/boj-image-crop-reproducibility.md:5`.** Current: "No program in this repository
   makes crops now: the crop tools were retired on 2026-09-26 by
   [`PLAN-retire-codex-index-image-work.md`](PLAN-retire-codex-index-image-work.md). The principles
   below explain the records the retained crops carry, and they still govern any crop made in
   future." Proposed: "No program in this repository makes manuscript crops now: the codex crop tools
   were retired on 2026-09-26 by [`PLAN-retire-codex-index-image-work.md`](PLAN-retire-codex-index-image-work.md).
   Three accgram modules still crop scans of printed editions for reading, `py/accgram/scan_page.py`,
   `py/accgram/zoom_line.py` and `py/accgram/transcription_editor.py`, and all three write
   disposable renderings under `.novc/scans/`. The principles below explain the records the
   retained crops carry, and they still govern any crop made in future." Sources:
   `py/accgram/scan_page.py:8`, `py/accgram/zoom_line.py:11`, and
   `py/accgram/transcription_editor.py:7` and `:788–790`.
2. **Finding 5.2, `doc/mam-normal-mark-order.md:14–16`.** Current: "The code calls it "(our) standard
   mark order" and its combining-class table "SBL2", after the appendix to the SBL Hebrew Font manual,
   so grep for **std mark order** and **SBL2** as well as for this section's heading." Proposed: "The
   code calls it "(our) standard mark order", and `py/check_mark_order.py` calls it "SBL2", after the
   SBL Hebrew Font recommendation to which the combining-class table's comment attributes the order,
   so grep for **std mark order** and **SBL2** as well as for this section's heading."
3. **Finding 4.4, `doc/user-wide-instruction-conversion-reconciliation.md`, a maintained document.**
   1. `:26`: "shared-review backup exception preserved (11.5)" becomes "long-lived-branch backup
      exception restored (11.5)".
   2. `:37`: "Retained." becomes "Retained; exact-command harness override remains deferred (11.1)."
   3. `:38`: "Retained; exact-command harness override remains deferred (11.1)." becomes
      "Retained."
   4. `:49`: "Retained; do-not-delete-the-count clause remains deferred (11.1)." becomes "Retained;
      do-not-delete-the-count and bold-lead-ins clauses remain deferred (11.1)."
   5. `:50`: "Retained; bold-lead-ins clause remains deferred (11.1)." becomes "Retained."

   Sources: at `71f96ca3:dot-claude/user-wide-CLAUDE.md`, the harness clause is at `:595` under "##
   Running scripts — no inline one-liners", the bold-lead-ins clause at `:1109` under "## Prose: if
   you announce a count, NUMBER the items", and the Git section's exception is the general
   long-lived-branch one (`:121–130`).
4. **Finding 23, `py/ws/pywikibot-setup.md:55–57`.** Current: "By default, after `main_ws_bot.py
   real` completes its live edits, it automatically downloads the modified chapters into `in/mam-ws`
   and reparses affected books." Proposed: "By default, after `main_ws_bot.py real` completes its
   live edits, it runs the same download function as `py/main_download.py fr-wikisource`, with a
   forced download: it refetches all 36 declared special pages into `in/mam-ws-special/`, downloads
   the modified chapters into `in/mam-ws` and reparses affected books."
5. **Question 5, found after the planning answer, `uxlc/doc/clc-design.md`,** the living CLC design
   document: `:224`, "guesses the LC folio/column/line", becomes "guesses the LC page/column/line";
   `:280`, "the existing cumulative per-folio estimator counts", becomes "the existing cumulative
   per-page estimator counts" (each `lci_augrecs.json` record is one page); and `:389`, "an LC
   folio-102A (col 3, line 22) detail image", becomes "an LC F102A (col 3, line 22) detail image".

### Editorial proposals: receipts' live updates and new records (D7: editorial)

A finished base stays as written. Each open update corrected in place below also gains, by Ben's
third planning answer, one dated entry headed "## Corrections made in the 2026-09-29 review's
remediation, <date>", or "## <date>: corrections made in the 2026-09-29 review's remediation" in a
file whose entries put the date first. The entry opens "Recorded by <agent> on <date>, New York
time, under the approved remediation plan for the 2026-09-29 dual-agent review." and names each
corrected passage by its former words and its new words, with the finding number. Where an update
gains a dated entry for another reason, that entry names the in-place corrections instead.

1. **Finding 1.3, `doc/blind-dive-into-template-params-update.md`**, restoring `87fc7141`'s own
   wording, which the merge `ebbfa90f` dropped:
   1. `:42–43`: "`py/mb_cmn/plain_template_schema.py:validate_current_plain_template` checks every
      argument's identity as well as the argument count: against
      `_CURRENT_PLAIN_NAMED_ARGUMENT_IDENTITIES` where" becomes
      "`py/mb_cmn/parser_stage_template_schema.py:validate_parser_stage_template` checks every
      argument's identity as well as the argument count: against
      `_PARSER_STAGE_NAMED_ARGUMENT_IDENTITIES` where". Both names exist
      (`py/mb_cmn/parser_stage_template_schema.py:197` and `:125`).
   2. `:63–64`: "The survey and documentation-verification paths named beside them remain current."
      becomes "The survey and documentation-verification paths named beside them remained current at
      that checkpoint." Line 63 keeps `e4934b6e`'s archive link.
2. **Item 2's dated entry, with findings 4.4 and 35, `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`.**
   Written in phase 5's closing-records commit, with its two in-place corrections, since the
   completions it dates land in phases 2 to 4 and row 11's deploys in phase 5. Append after
   "## Archived receipt references, 2026-09-29":

   > ## Execution rows that overstated what landed or later became false, <date>
   >
   > Recorded by <agent> on <date>, New York time, under the approved remediation plan for the
   > 2026-09-29 dual-agent review, whose findings 1, 2, 4.4 and 35 are the source of this entry.
   >
   > The execution table under "Approved remediation implemented; final gates pending, 2026-09-28"
   > called six findings fixed whose approved changes had not landed in full:
   >
   > 1. Row 3: the pinned link to the retired mega-coverage plan reached only the topology reference;
   >    `in/mam-ws-intro/README.md`, `py/repo_scopes.py` and
   >    `py/subcommands/download_wikisource_intro.py` kept the retired plan's path.
   > 2. Row 5: the September 10 review's update gained base-and-update link pairs that made three of
   >    its passages false, and it kept presenting retired or executed things as current.
   > 3. Row 6: three of the named sites survived, in `py/ac_paths.py` and in two passages of the live
   >    September 9 plan.
   > 4. Row 11: the common body's two routings of every reader to the Codex-only
   >    `codex-worktree-tasks` skill, and a third written into the live September 9 plan, were not
   >    made agent-specific.
   > 5. Row 29: `py/author_site/post_stress_meteg.py`'s docstring kept the old account of
   >    `gh-pages/style.css`.
   > 6. Row 30: `doc/meteg-after-silluq-snips/README.md` kept "folio **57a**", which the approved
   >    plan changed to "page 57a", and "folio **307b**", which the plan's list of side-lettered
   >    identifiers omitted.
   >
   > Row 24 was true when written; the merge `ebbfa90f`, later on 2026-09-28, restored the old
   > order of the MAM-parsed plus consumer notice and so made its "narpas first-use glosses" false
   > of that notice, in the 24 `MAM-parsed/plus/` files and
   > `gh-pages/MAM-parsed/plus/html/mpplus.html`. The 2026-09-29 review's remediation completed
   > each of these on <date>, in <commit or commits>.
   >
   > Also corrected in place in this file: row 13's "from the old common body" now reads "from the
   > old Claude body", the file the reconciliation maps (finding 4.4); and in the paragraph
   > "Clarified the push rule in response to Ben's question", in the entry "Detailed remediation
   > plan prepared; execution approval pending, 2026-09-28", "The shared worktree" (D11) now reads
   > "The shared origin branch", the section's present title (finding 35).

   The two in-place corrections the entry names: `:549`, row 13, "from the old common body" becomes
   "from the old Claude body"; `:439`, "The shared worktree" becomes "The shared origin branch".
3. **Finding 4.1, `doc/review-findings-2026-09-14-update.md:100–104`, item 10.** Current: "The
   overall retirement remains incomplete until Ben applies and reports the manual frozen-Sheet and
   Hebrew Wikisource documentation edits and the required live results are verified. The September
   14 remediation-plan update records that distinction." Proposed: "The retirement was completed on
   2026-09-27: the [Google Sheet retirement plan](E/PLAN-retire-google-sheet.md) records the frozen
   Sheet, the five Hebrew Wikisource documentation edits and both live verifications as complete
   (`c450060e`). The update of the [September 14 remediation plan](E/PLAN-remediate-review-findings-2026-09-14.md),
   [PLAN-remediate-review-findings-2026-09-14-update.md](E/PLAN-remediate-review-findings-2026-09-14-update.md),
   recorded the distinction while the retirement was incomplete; `e4934b6e` retired both." The
   base is linked with its update, as `mam-repository-topology`'s
   `references/repository-maintenance.md`, "Manual document retirement", asks of a historical
   reference to a retired family.
4. **Findings 4.2 and 4.3, `doc/review-findings-2026-09-10-update.md`.**
   1. 4.2(a), `:668–670`. Current: "4. The finished [PLAN-wikisource-derived-mam-products.md](F/PLAN-wikisource-derived-mam-products.md)
      and [PLAN-wikisource-derived-mam-products-update.md](F/PLAN-wikisource-derived-mam-products-update.md)
      and frozen `doc/mam-products-phase6-command-map.md` each had one “hand-authored” occurrence,
      both distinguishing source from generated output." Proposed: "4. The finished
      [PLAN-wikisource-derived-mam-products.md](F/PLAN-wikisource-derived-mam-products.md) and the
      frozen [`doc/mam-products-phase6-command-map.md`](F/mam-products-phase6-command-map.md) each had
      one “hand-authored” occurrence, both distinguishing source from generated output; the plan's
      [update](F/PLAN-wikisource-derived-mam-products-update.md) had none." The entry's "D12 left
      all three finished documents unchanged." (`:677`) is then true as written.
   2. 4.2(b), `:1035–1038`. Current: "D12 left the finished [PLAN-close-out-review-2026-09-08.md](F/PLAN-close-out-review-2026-09-08.md)
      and [PLAN-close-out-review-2026-09-08-update.md](F/PLAN-close-out-review-2026-09-08-update.md)
      unchanged; its live sibling [PLAN-close-out-review-2026-09-08-update.md](F/PLAN-close-out-review-2026-09-08-update.md)
      now records that Step 7 is complete and preserves the evidentiary limit." Proposed: "D12 left
      the finished [PLAN-close-out-review-2026-09-08.md](F/PLAN-close-out-review-2026-09-08.md)
      unchanged; its live sibling [PLAN-close-out-review-2026-09-08-update.md](F/PLAN-close-out-review-2026-09-08-update.md)
      recorded that Step 7 was complete and preserved the evidentiary limit, until `2a051ba5` retired
      both."
   3. 4.2(c), `:1395–1397`. Current: "This entry classifies only the live `.novc` references in
      `doc/mam-products-phase6-command-map.md`, [review-findings-2026-09-08.md](F/review-findings-2026-09-08.md)
      and [review-findings-2026-09-08-update.md](F/review-findings-2026-09-08-update.md) and
      [PLAN-close-out-review-2026-09-08.md](F/PLAN-close-out-review-2026-09-08.md) and
      [PLAN-close-out-review-2026-09-08-update.md](F/PLAN-close-out-review-2026-09-08-update.md)."
      Proposed: "This entry classifies only the live `.novc` references in
      [`doc/mam-products-phase6-command-map.md`](F/mam-products-phase6-command-map.md),
      [`doc/review-findings-2026-09-08.md`](F/review-findings-2026-09-08.md) and
      [`doc/PLAN-close-out-review-2026-09-08.md`](F/PLAN-close-out-review-2026-09-08.md); the two
      sibling updates, the [review's](F/review-findings-2026-09-08-update.md) and the
      [plan's](F/PLAN-close-out-review-2026-09-08-update.md), held none." The three-blob count at
      `:1400–1405` and "The 12 lines" at `:1412` are then true as written.
   4. 4.3, `:1206`: "The tracked review-differences receipt preserves" becomes "The archived
      review-differences receipt preserves"; add the receipt to the archive list at `:1722–1729` as
      a ninth bullet,
      "- [wikisource-derived-mam-products-review-differences.json](F/wikisource-derived-mam-products-review-differences.json)",
      and change the list's lead-in at `:1719`, "The validation receipts and compressed evidence",
      to "The validation and review-differences receipts and compressed evidence".
   5. 4.3, `:1217`: "The direct tracked entry points remain, while Git history at Phase 2 preserves
      their then-current behavior. The plan and tracked Phase 2 receipt preserve" becomes "The direct
      entry points remain tracked, though `a41fbcdd` removed the `go` subcommand of
      `py/main_parse.py` on 2026-09-27; Git history at Phase 2 preserves their then-current
      behavior. The plan and the archived Phase 2 receipt preserve".
   6. 4.3, `:1218`: "Historical wrapper commands around current tracked entry points." becomes
      "Historical wrapper commands around the `py/main_parse.py go` and `py/main_diff.py wsgo`
      commands, which `a41fbcdd` removed on 2026-09-27.", and "A current comparison runs the direct
      entry points rather than reading a wrapper or its logs." becomes "Until that removal, a
      comparison could run those commands directly rather than read a wrapper or its logs."
      `a41fbcdd` removed subcommands, not entry points: no `py/main_*.py` file went.
   7. 4.3, `:1219`: "the Google reader and comparator remain tracked." becomes "`a41fbcdd` deleted
      the Google reader and comparator on 2026-09-27, and Git history keeps them."
   8. 4.3, `:532–533`: "The last three plans describe work that is paused or live, so the three
      State lines are kept true in the plans themselves." becomes "The last three plans described
      work that was paused or live when this entry was first written, so their State lines were kept
      true in the plans themselves; the codex-index plan has since recorded `State: executed
      2026-09-26`, and the Google Sheet plan `State: executed 2026-09-27` before `e4934b6e` retired
      it."
   9. 4.3, close-out row 3 (`:1650`): "The retired display fallback is recorded in the two sibling
      update files named in the 2026-09-11 disposition." becomes "The retired display fallback was
      recorded in the two sibling update files named in the 2026-09-11 disposition,
      [review-findings-2026-09-08-update.md](F/review-findings-2026-09-08-update.md) and
      [PLAN-remediate-review-findings-2026-09-08-update.md](F/PLAN-remediate-review-findings-2026-09-08-update.md),
      updates of [review-findings-2026-09-08.md](F/review-findings-2026-09-08.md) and
      [PLAN-remediate-review-findings-2026-09-08.md](F/PLAN-remediate-review-findings-2026-09-08.md);
      `2a051ba5` later retired all four."
   10. 4.3, close-out row 6 (`:1653`): "The Wikisource refresh and the records it overtook are
       recorded in three sibling update files; the finished plans and validation receipt remain
       unchanged." becomes "The Wikisource refresh and the records it overtook were recorded in three
       sibling update files; the finished plans and validation receipt stayed unchanged until
       `2a051ba5` retired their families, which remain at `f7229708`."

   The table rows at `:1416–1417`, which name `mam-products-phase6-command-map.md` while
   classifying "the measured tree" that the entry at `:1700–1705` dates, stay as they are; 4.2(a)
   and 4.2(c) above give the command map its archive link at `:669` and `:1396`.
5. **Finding 4.7, `doc/dual-agent-review-2026-09-16-turn-01-claude-update.md:91–92`.** Current: "The
   plan was subsequently written and executed on 2026-09-18." Proposed: "The plan was subsequently
   written on 2026-09-17 and executed on 2026-09-18." Sources: `49c7b1c9` (2026-09-17 17:30:41) wrote
   the plan, and `f3bd280a` (2026-09-18 09:59:26) set its State to "executed 2026-09-18".
6. **Finding 4.8, `doc/meteg-after-silluq-job-4-12-update.md:84–86`.** Current: "The NLI presents B
   55 together with its direct continuation, Evr. II B 247; they are separate shelfmarks, not former
   and current names." Proposed: "The cached introduction's appendix calls B 55 formerly B 247
   (`in/mam-ws-intro/appendices.mediawiki:78`) and describes B 247 as its direct continuation
   (`:93`); the NLI presents both shelfmarks together." "The cached introduction" is the file's own
   name for the mirror (`:83`, `:86`). This matches the row of `doc/sigil-decoding.md` that
   `22d18d72` corrected (`:222`).
7. **Findings 4.9, 9.1 and 9.2, `evr-ii-b-55/evr-ii-b-55-images-provenance-update.md`.**
   1. 9.1, line 3: "State: open; the finished base remains tracked." becomes "State: open, first
      entry 2026-09-28."
   2. 4.9, `:9–10`: "Their current paths and filename changes are recorded in [the post-stress-meteg
      provenance update](../doc/post-stress-meteg-image-provenance-update.md)." becomes "Five of them
      were renamed on 2026-09-28, and [the post-stress-meteg provenance update](../doc/post-stress-meteg-image-provenance-update.md)
      records their current paths; the sixth, `st-petersburg-evr-ii-b-55-Ps60v10-HFRV33Y.png`, kept its
      name, which the finished base [`doc/post-stress-meteg-image-provenance.md`](../doc/post-stress-meteg-image-provenance.md)
      records."
   3. 9.2, under the recommended choice, a new dated entry, which also names the two corrections
      above:

      > ## Passages of the base changed in place on 2026-09-28, <date>
      >
      > Recorded by <agent> on <date>, New York time, under the approved remediation plan for the
      > 2026-09-29 dual-agent review (its finding 9.2). Commit `db152332` (2026-09-28) changed four
      > passages of the finished base in place, where the rule the 2026-09-26 remediation plan
      > applied to this base puts later facts in an update rather than the finished base. The base
      > stays as it stands, and this entry records the four changes:
      >
      > 1. "Who prepared the pCloud folder is not known." became "Ben reports on 2026-09-28 that the
      >    link belongs to Avi's pCloud directory. A different zip in that directory has the images
      >    absent from this zip, but Ben does not intend to locate it now. Avi used two zip files to
      >    separate Prophets from Writings; this manuscript spans both divisions and fits that
      >    organization awkwardly. The other zip's filename and exact location have not been
      >    recorded."
      > 2. "so the Prophets, presumably images 005–495, are not in the download." became "so the
      >    Prophets, presumably images 005–495, are not in this zip. Ben reports that Avi's other zip
      >    has those images."
      > 3. "They presumably come from whoever prepared the pCloud folder." became "They presumably
      >    come from whoever prepared this zip."
      > 4. "The download lacks them, so they have no row here." became "This zip lacks them, so they
      >    have no row here; Ben reports that Avi's other zip has the images."
      >
      > Also corrected in place in this file: line 3, "State: open; the finished base remains
      > tracked.", now reads "State: open, first entry 2026-09-28." (finding 9.1); and "Their
      > current paths and filename changes are recorded in the post-stress-meteg provenance
      > update." now reads "Five of them were renamed on 2026-09-28, and the post-stress-meteg
      > provenance update records their current paths; the sixth,
      > `st-petersburg-evr-ii-b-55-Ps60v10-HFRV33Y.png`, kept its name, which the finished base
      > `doc/post-stress-meteg-image-provenance.md` records." (finding 4.9).

   The quoted sentences keep their links in the file; the entry quotes their words.
8. **Finding 9.1, `doc/post-stress-meteg-image-provenance-update.md`, line 3.** "State: open; the
   finished base remains tracked." becomes "State: open, first entry 2026-09-28." By Ben's third
   planning answer the file also gains a dated entry:

   > ## Corrections made in the 2026-09-29 review's remediation, <date>
   >
   > Recorded by <agent> on <date>, New York time, under the approved remediation plan for the
   > 2026-09-29 dual-agent review. Line 3, "State: open; the finished base remains tracked.", now
   > reads "State: open, first entry 2026-09-28.", the recorded form of an update's State (finding
   > 9.1).
9. **Finding 21, a new `doc/hbce-psalms-vs-mam-2026-09-26-update.md`**, with the base's permitted
   pointer, "Updates and later status: [hbce-psalms-vs-mam-2026-09-26-update.md](hbce-psalms-vs-mam-2026-09-26-update.md).",
   inserted as its line 4, directly below its status line, "Claude-written on 2026-09-26 for Ben
   Denckla, who has not reviewed it." The receipt has no `State:` line of its own; its text and
   `hbce-psalms/out/` stay as they are, and so does `py/hbce_psalms/compare.py`. The new file:

   > # Updates to the HBCE Psalms comparison receipt of 2026-09-26
   >
   > State: open, first entry <date>.
   >
   > Every entry here corrects or supplements `doc/hbce-psalms-vs-mam-2026-09-26.md`, which is left
   > exactly as written. Ben's decision of 2026-09-11 (D12): a finished dated document is left as
   > written, and a correction or later fact goes in its single update.
   >
   > ## Two defects found by the 2026-09-29 review, <date>
   >
   > Recorded by <agent> on <date>, New York time, under the approved remediation plan for the
   > 2026-09-29 dual-agent review (its finding 21).
   >
   > 1. **Two summary sections share one heading.** `hbce-psalms/out/compare_summary.txt` heads both of
   >    its Leningrad comparisons "=== ML vs MAM (Leningrad) ===". The first covers the 170 verses of
   >    Psalms 15:1–25:1 and writes `compare_ML_range.tsv`; the second covers all 801 verses of HBCE's
   >    Leningrad transcription, Psalms 1:1–51:21, and writes `compare_ML.tsv`.
   >    `py/hbce_psalms/compare.py` writes the heading without the range. `compare_summary.txt` and
   >    `compare.py` stay unchanged until the HBCE work resumes and reruns the comparison, since a
   >    change to that hand-run program would owe the rerun that Ben's frozen-record decision of
   >    2026-09-26 does not waive.
   > 2. **The receipt cites more than its opening says.** "Everything it cites is in `hbce-psalms/`,
   >    `py/hbce_psalms/` and `py/main_hbce_psalms.py`" is too broad: the receipt also cites
   >    `DATA-LICENSES.md`, `MAM-simple/xml-vtrad-mam/Ps.xml`, `MAM-parsed/plus/D1-Psalms.json`,
   >    `explicit_xataf.extract.find_docnote_tmpls`, `in/mam-ws-intro/`, `in/UXLC-39/Psalms.xml`,
   >    `in/meteg_after_silluq_cases.json`, `aleppo/line-breaks/`, `py/tests/test_transliterations.py`,
   >    `py/tests/test_prose_conventions.py`, `py/tests/test_prose_mark_order.py` and
   >    `py/main_verse_links.py`.

   Facts: `hbce-psalms/out/compare_summary.txt:51` and `:76` hold the two headings, `:52` and `:77`
   their counts; `py/hbce_psalms/compare.py:713` writes the heading, and `:704–705` add the
   `_range` suffix only to the file name. `py/tests/test_receipt_update_links.py` requires the base's
   line 4 to be exactly the pointer and checks nothing inside the update.

10. **Finding 30, a tracked list of the approved public additions** (phase 1, in
    `C:/Users/BenDe/GitRepos/MAM-basics`). The source is the untracked
    `C:/Users/BenDe/GitRepos/MAM-basics/.novc/PROPOSAL-memory-retirement-and-instruction-consolidation-2026-09-28.md`
    (95,251 bytes, last written 2026-09-28 19:18:06 New York time, as observed on 2026-09-30). The
    base, `doc/memory-retirement-and-instruction-consolidation-2026-09-28.md:27–28`, says the labels
    "were reconciled against their named tracked destinations", and the checkout-kinds plan points to
    the proposal (`doc/PLAN-checkout-kinds-and-portable-knowledge.md:46–47` and `:369–370`).

    **Phase 1a: draft, check and present; nothing is written into a repository.** Read the
    proposal. Draft the 36 rows and the two entries below in a UTF-8 file in the session's scratch
    directory, outside every repository; apply the privacy check to that draft; and present the
    draft and the check's result to Ben. The rows are editorial wording under D7, and a push
    publishes them. **Phase 1b, after Ben's answer:** write into the two tracked updates only the
    wording he approves, with his changes; nothing drawn from the proposal enters a tracked file, a
    commit or `origin` before then.

    Append to `doc/memory-retirement-and-instruction-consolidation-2026-09-28-update.md`, whose
    entries put the date first:

    > ## <date>: the approved public additions, listed
    >
    > Recorded by <agent> on <date>, New York time, under the approved remediation plan for the
    > 2026-09-29 dual-agent review (its finding 30). The base says the approved public additions
    > P01–P26, N01–N08 and A01–A02 "were reconciled against their named tracked destinations", and
    > until this entry the only list any tracked record pointed to was in an untracked file of one
    > clone, which a default maintenance run can delete. They are:
    >
    > | Label | Tracked destination (file and section) | Addition, in brief | Reconciliation |
    > |---|---|---|---|

    with one row for each of the 36 labels, as Ben approves them. Append to
    `doc/PLAN-checkout-kinds-and-portable-knowledge-update.md`:

    > ## <date>: the approved public additions, now listed in a tracked record
    >
    > Recorded by <agent> on <date>, New York time, under the approved remediation plan for the
    > 2026-09-29 dual-agent review (its finding 30). The labels P01–P26, N01–N08 and A01–A02 of the
    > approved public additions, which Workstream B's step "Migrate and consolidate" applies from the
    > proposal this plan names, are now defined in
    > [the memory-retirement record's update](memory-retirement-and-instruction-consolidation-2026-09-28-update.md),
    > under "the approved public additions, listed". The full public triage and the private
    > dispositions stay in their untracked proposal files.

    **The privacy check, applied to the draft:** every one of the 36 labels gets a row, and no PR
    label appears. Each row restates only what its named tracked destination already says at
    `HEAD`, confirmed with `git grep` in this clone; nothing in a row comes from the proposal's
    triage prose, an auto-memory file or the private appendix. A row names no memory file, memory
    store, memory topic, incident or account observation; no MAM-private path, file, commit or
    content; no private disposition (PR01–PR06 and the private appendix stay private); and no
    credential or its location. A row that cannot meet all of this reads "withheld: private", and
    the entry says how many rows do. A row whose named destination at `HEAD` does not hold its
    addition says so in its Reconciliation cell, and the presentation to Ben lists each such row.
    Stop and report to Ben if the labels do not number exactly 26, 8 and 2, or if the file is
    missing or is no longer 95,251 bytes, last written 2026-09-28 19:18:06 New York time.

    Do not run `py/main_repo_maintenance.py` in that clone before phase 1b is committed and pushed:
    its first step deletes `.novc/` unless `--skip-novc` is given.

### Editorial proposals: Python comments and docstrings (D7: editorial)

Put a long pinned URL on a line of its own, as `py/author_site/post_stress_meteg_post_silluq_data.py:554`
does; E501 is not enforced (`ruff.toml`). None of these changes alters a tracked generated file;
`py/main_verse_links.py` and the two Holman helpers change only what they print on demand or in an
error.

1. **Finding 2.1, approved wording in docstrings.** `py/repo_scopes.py:29–30` and
   `py/subcommands/download_wikisource_intro.py:33–34` each end a sentence with "`git show --stat
   985262e2` names every file removed; Phase 3 of `doc/PLAN-mega-coverage.md` records the totals."
   Proposed in both: "`git show --stat 985262e2` names every file removed. Phase 3 of the retired
   mega-coverage plan,
   https://github.com/bdenckla/MAM-basics/blob/f72297084ab94aea6fd1274dc1bc3d7ce6acddd5/doc/PLAN-mega-coverage.md,
   records the totals." (the approved README sentence, with the link written as a URL). The
   approved wording links the retired plan alone, while finding 2.2's docstring, below, links the
   plan and its update, as the retirement rule asks of a new historical reference.
2. **Finding 2.2, `py/ac_paths.py:25`.** Current: "which phase 3 of ``doc/PLAN-mega-coverage.md``
   records," Proposed: "which phase 3 of
   https://github.com/bdenckla/MAM-basics/blob/f72297084ab94aea6fd1274dc1bc3d7ce6acddd5/doc/PLAN-mega-coverage.md
   (update https://github.com/bdenckla/MAM-basics/blob/f72297084ab94aea6fd1274dc1bc3d7ce6acddd5/doc/PLAN-mega-coverage-update.md)
   records,", putting the pinned URL in the path's place, as `py/tests/test_mega_coverage.py:74–75`
   does; "the same plan" and "phase 6b" after it (`:26–27`) then refer to that plan.
3. **Finding 2.3, `py/author_site/post_stress_meteg.py:16–17`.** Current: "``gh-pages/style.css`` is
   the deploy-root stylesheet, whose whole job is the light/dark switching;" Proposed:
   "``gh-pages/style.css`` is the deploy-root stylesheet, which supplies light/dark switching, the
   bounded text measure and book-title italics;" as `22d18d72` worded `py/author_site/site_data.py:78–86`.
4. **Finding 5.1, `py/mb_diff_mpu/mpplus_structure.py:3–5`.** Current: "Every classified structural
   parameter is included so a change inside a ketiv/qere, qamats, dual-cantillation, or
   stress-helper alternative remains visible." Proposed: "Every classified structural parameter is
   included, so a template added, removed, reordered or moved to another parameter inside a
   ketiv/qere, qamats, dual-cantillation, or stress-helper alternative remains visible. The
   inventory records template names and positions,
   not strings: a changed string inside an alternative that the selected Scripture projection does not
   take is visible only where the separate alternative population below compares it."
5. **Finding 5.3, `py/author_site/site_data.py:98`.** Current: "# py/tests/test_site_index_links.py
   resolves each one against gh-pages/." Proposed, in three comment lines: "#
   py/tests/test_site_index_links.py resolves each relative href, and each absolute one / # under
   https://bdenckla.github.io/MAM-basics/, against the files tracked under / # gh-pages/, and checks
   no other URL; it fetches nothing." (each slash marks a line break). The test compares hrefs with
   `git ls-files -z -- gh-pages/` and fetches nothing (`py/tests/test_site_index_links.py:8`,
   `:63–72`, `:80–88`).
6. **Finding 5.4, `py/boj_paths.py`.**
   1. `:108–109`: "because every one of them is an entry point:" becomes "because every one of them
      but this library is an entry point:".
   2. `:187–188`: "and now has LF line endings like the other 700 retained files." becomes "and now
      has LF line endings like the other 183 text files among the 701 retained under
      ``gh-pages/book-of-job`` and ``book-of-job/out``; the remaining 517 are binary, 515 PNG images
      and two WOFF2 fonts (measured 2026-09-30 with ``git ls-files --eol``)." The measure is
      `git ls-files --eol -- gh-pages/book-of-job book-of-job/out`: 701 files, 184 `i/lf` and 517
      `i/-text`.
7. **Finding 5.5, `py/tests/test_mam_xml_verses.py`, the module docstring.** Line 1's "a lint over the
   tree and a differential." becomes "a lint over the tree and two differentials."; `:6–7`'s "Ben chose
   on 2026-09-26 to add both checks:" becomes "Ben chose on 2026-09-26 to add the first two checks,
   and the remediation plan he approved on 2026-09-28 added the third:"; item 2's label, "THE
   DIFFERENTIAL:" (`:14`), becomes "THE RANGE DIFFERENTIAL:", since there are now two; and after
   item 2 add:

   > 3. THE CONTENT DIFFERENTIAL: over the whole corpus, the atoms the reader gives, marks as well as
   >    letters, match an independent walk of the source nodes the reader selects
   >    (``_selected_parts``), which shares none of the reader's word joining. It came with the fix
   >    of 2026-09-28 that reads the child form of ``<kq-trivial>``, keeping Psalms 10:5's second
   >    atom and its legarmeh.

   The fix is the one `evr-ii-b-55/README.md:379–381` records ("preserving the second atom and its
   legarmeh"); the child form at `MAM-simple/xml-vtrad-mam/Ps.xml:302–305` holds one atom.

8. **Finding 11, `py/tests/test_wikisource_special_page_download.py`, a new module docstring** above
   `import json`:

   > """Tests of the special-page download, ``py/ws/ws_special_page_download.py``.
   >
   > The first test is lint-shaped: it checks the declared inventory against the mirrored
   > chapter-2 introduction, ``in/mam-ws-intro/ch2.mediawiki``.
   >
   > BLESSED EXAMPLE-BASED BAND.  The other five test ids run the download over a stub API
   > that this module builds, and are kept under the exception Ben decided on 2026-09-30,
   > which ``AGENTS.md``, "Writing tests: differential and lint-shaped only", records.  The
   > four fault-injection ids hold five cases.  Every case checks that a bad API response or
   > bad local metadata makes the download raise, and every case but the last, a manifest
   > overwritten with "not json", also checks that no mirrored file changed: a property with
   > no regeneratable artifact.  The round trip is the only offline check of the download's
   > reuse and forced refresh, neither of which a regenerated mirror's diff would show.
   > """

9. **Finding 12, `py/ws/ws_special_page_download.py`.**
   1. The module docstring's last sentence (`:5–7`). Current: "The literal inventory is checked
      against the two source tables in the local chapter-2 introduction mirror before any network
      result can replace a file." Proposed: "The literal inventory is checked against chapter 2 of
      the local introduction mirror before any network result can replace a file: the table in its
      Decalogue section gives three of the titles, the paragraph after that table gives the fourth,
      and its song-form table gives the other thirty-two."
   2. `:138`: "Extract the inventory independently from chapter 2's two named tables." becomes
      "Extract the inventory independently from chapter 2's Decalogue section and song-form table."
   The code, which slices `ch2.mediawiki:359–389` from the Decalogue heading to the next heading,
   is right and stays. The test name at `py/tests/test_wikisource_special_page_download.py:131`,
   "…matches_the_independent_intro_tables", stays, since renaming it would change a test id.
10. **Finding 13, `py/subcommands/download_wikisource_intro.py`.**
    1. `:21`: "1,852,837 bytes of wikitext, the committed manifest's sum" becomes "1,852,837 bytes
       of wikitext, the sum in the manifest committed that day".
    2. `:52–53`: "Five of the thirteen pages were edited in August 2026 alone (the manifest's count;"
       becomes "Five of the thirteen pages were edited in August 2026 alone (the count in the manifest
       committed on 2026-08-31, which the refresh of 2026-09-27 replaced;".
11. **Finding 14.3, the five-site inventory, under the recommended choice.**
    1. `py/author_misc/mp_cmn_top_header_book39.py:2`: "Shared sources for top-level/header/book39
       sections in mpplain/mpplus docs." becomes "Shared sources for top-level/header/book39 sections
       in MAM-parsed-plus docs.", as `87fc7141` worded its sibling module's line 2.
    2. `py/author_misc/mp_cmn_examples_and_file_naming.py:12`: "# JSON snippets shared by plain and
       plus common-templates sections" becomes "# JSON snippets for the plus common-templates
       sections".
    3. `py/ws/ws_plain.py:1`: "Convert faithful Wikisource format 2 into the plain-product schema."
       becomes "Convert faithful Wikisource format 2 into the transient parser stage's plain-shaped
       schema."
    4. `py/ws/ws_plain.py:59`: "# The category identifies the source page; it is not a plain-product
       row." becomes "# The category identifies the source page; it is not a parser-stage row."
    5. `py/py_misc/mam_parsed_plus.py:33–34`: "Current plain headers already match plus shape for
       these fields." becomes "Current parser-stage headers already match plus shape for these
       fields."

    No identifier is renamed. `py/ws/ws_plain.py:3` and `:24` and the two "plain-file concern"
    passages, `py/hkq_cmn/mam_plus_verse_data.py:55` and `py/hkq_cmn/qere_projection.py:414`, keep
    the shape name the plain retirement plan itself uses.
12. **Finding 14.4, three bare-path citations of deleted files.**
    Each slash below marks a line break; each URL stands on a line of its own.
    1. `py/hkq_cmn/qere_ending_search.py:29`: "# it held, as read_books_from_mam_parsed_plain.py's
       (0314c6e)." becomes "# it held, as the retired py/py_misc/read_books_from_mam_parsed_plain.py's
       (0314c6e, / #
       https://github.com/bdenckla/MAM-basics/blob/0314c6effbb088c46d4fe3737c4e18b73e6e7332/py/py_misc/read_books_from_mam_parsed_plain.py)."
    2. `py/main_search_final_hiriq_verse_text.py:25–26`: "# hkq_cmn/qere_ending_search.py's sentinels
       and read_books_from_mam_parsed_plain.py's / # (0314c6e)." becomes "#
       hkq_cmn/qere_ending_search.py's sentinels and the retired / #
       py/py_misc/read_books_from_mam_parsed_plain.py's (0314c6e, / #
       https://github.com/bdenckla/MAM-basics/blob/0314c6effbb088c46d4fe3737c4e18b73e6e7332/py/py_misc/read_books_from_mam_parsed_plain.py)."
    3. `py/ws/ws_bot_edit_sigil_b2_to_t451.py:38`: "doc/PLAN-replace-sigil-b2-with-t451.md is the
       fuller historical statement," becomes "The retired doc/PLAN-replace-sigil-b2-with-t451.md,
       whose last version is at /
       https://github.com/bdenckla/MAM-basics/blob/4f3fed2dcb1e21835ad73a31ea8e5e472f4960d7/doc/PLAN-replace-sigil-b2-with-t451.md,
       / is the fuller historical statement,", with `:39–41` unchanged.

    `a41fbcdd` deleted the reader module, whose version at `0314c6ef` both comments cite; `f6173fe3`
    deleted the plan, which never had an update, and `4f3fed2d`, its only parent, made the plan's
    last change. The receipt `py/ws/ws_bot_edit_history.md` keeps its citation as written.
13. **Finding 16, `py/tests/test_mega_coverage.py`, the new `NOT_IN_MEGA` reason** for
    `"py/main_parse.py ws --write-parser-stage-grammar-lock"`: "Ben's decision, <plan-approval date>,
    approving a Claude-written proposal: every parse-ws run checks the transient parser stage against
    py/verify_mp/expanded_stack_grammar_parser_stage.lock.json, so rewriting the lock on every run
    would make that check pass by construction.  Run it by hand when a legitimate new raw nesting
    stops parse-ws.  Recorded in doc/PLAN-remediate-review-findings-2026-09-29.md, finding 16."
14. **Finding 24.2, `py/subcommands/diff_mpplus.py:49–51`.** Current: "--pin stores each boundary as
    it pins it, and --all, --check, a run with no arguments and the mega refuse a boundary that is
    not stored before comparing anything (_refuse_unstored_boundaries)." Proposed: "--pin stores
    each boundary as it pins it; --all, --check and the mega refuse, before comparing anything, every
    boundary that is not stored, and a run with no arguments refuses the latest release's end, the
    one boundary it compares, if it is not stored (_refuse_unstored_boundaries).  A run with explicit
    --old and --new checks no boundary, and "stored" means listed in
    MAM-parsed/historical/manifest.json."
15. **Finding 26, two docstrings.**
    1. `py/repo_util/forest_sync.py:5–6`: "Dirty, diverged, active or otherwise ineligible clones stay
       untouched." becomes "A write refuses a dirty, off-main, mid-operation, locked or occupied
       clone before fetching it, and an ahead or diverged clone after a fetch that adds any missing
       objects, rewrites FETCH_HEAD, and creates or fast-forwards refs/remotes/origin/main; either
       way the clone's local branches, checkout and environments stay untouched." Both docstrings
       describe the behaviour after finding 26's fix and land in its commit.
    2. `py/main_repo_util.py:44–45`: "Ineligible repositories are reported unchanged;" becomes
       "Ineligible repositories are reported with their local branches, checkouts and environments
       unchanged, though a write run has fetched an ahead or diverged clone before refusing it;".
16. **Finding 31, two citations of retired auto-memory notes.**
    1. `py/repo_util/run_black.py:30–32`: "Ben's decision of 2026-08-31, whose reasoning is recorded in
       this project's auto-memory as venv-roster-2026-08-31.md --" becomes "Ben's decision of
       2026-08-31, whose reasoning no tracked record holds --". `88ba0392`'s commit message records
       the decision's date and effect, six repositories without a `.venv`, but not its reasoning.
    2. `py/accgram/lexical_validation.py:32`: "(output-neutral today, but future-proof; cf. memory
       parse-rate-not-a-goal)." becomes "(output-neutral today, but future-proof; a checker's
       acceptance rate is diagnostic, not the objective: doc/agent-planning-principles.md, "Keep
       Verification Close To The Workflow")."
17. **C1, `py/ws/ws_special_page_download.py:441`,** the docstring of `download`. Current: """Validate,
    retrieve, and atomically replace the special-page mirror.""" Proposed:

    > """Validate, retrieve, and replace the special-page mirror, one file at a time.
    >
    > Every response is validated before anything is written.  Then each fetched page whose
    > bytes changed is replaced atomically through ``file_io.with_tmp_path``, and
    > ``manifest.json`` is replaced last; the mirror as a whole is not replaced atomically.
    > If writing a page's temporary file fails, ``with_tmp_path`` removes it and leaves the
    > page as it was, and a later run refetches any page whose bytes disagree with the
    > manifest.  If the final replacement fails, ``<slug>.tmp.mediawiki`` is left behind,
    > which Git ignores and ``_validate_existing_files`` rejects, so every later run, a
    > saving bot run's post-run download included, stops before any request until a person
    > deletes it.
    > """

    Sources: `py/mb_cmn/file_io.py:22–37` and `:90–94`; `py/ws/ws_special_page_download.py:291–296`,
    `:412–429`, `:441–453` and `:499–508`; `.gitignore:7`.

18. **Item 36.10, `py/tests/test_mega_coverage.py:471–475`,** the reason for
    `"py/main_hbce_psalms.py lint-receipt"`. Current: "Claude-written proposal, not yet reviewed by
    Ben: it checks the Hebrew forms of one dated receipt against hbce-psalms/, and writes nothing.
    Recorded in py/main_hbce_psalms.py's docstring and hbce-psalms/README.md." Proposed: "Ben's
    decision, <plan-approval date>, approving a Claude-written proposal: it checks the Hebrew forms
    of one dated receipt against hbce-psalms/, and writes nothing.  Recorded in
    py/main_hbce_psalms.py's docstring, hbce-psalms/README.md and
    doc/PLAN-remediate-review-findings-2026-09-29.md." Its facts hold; running it in the suite stays
    deferred.
19. **Item 36.2, `py/product_scopes.py`.**
    1. `:36–37`, after "owes every affected hand-run generator and inspection of its outputs.", add:
       "A refresh of MAM's text is the exception for ``py/main_mam4sef.py`` and
       ``py/main_mam_osis.py``, by Ben's decision of 2026-09-30, and a change to MAM's data is the
       exception for ``py/main_hbce_psalms.py compare``, by his decision of 2026-09-26; AGENTS.md's
       products section states both." (true once `AGENTS.md` item 4 above lands).
    2. `:51–53`, after "a mega run does not do that for it.", add: "The one input change exempted for
       these two programs is a refresh of MAM's text: by Ben's decision of 2026-09-30 their products
       may lag it, as their READMEs say."
20. **Question 5, `py/main_verse_links.py`.**
    1. The docstring's output list (`:27–29`): "LC <folio>" becomes "LC F<page>", and "Sefaria's image
       of that Leningrad Codex folio, with the atom's estimated" becomes "Sefaria's image of that
       Leningrad Codex page, with the atom's estimated".
    2. `:43–47`: "so the folio is looked up" becomes "so the page is looked up"; "two columns to a
       leaf" becomes "two columns to a page"; "runs past a leaf's last column" becomes "runs past a
       page's last column".
    3. `_estimate`'s docstring (`:195–197`): "if it runs off the leaf." becomes "if it runs off the
       page."; "Two columns to a leaf" becomes "Two columns to a page".
    4. `_folio_line` (`:209–213`): the output "- [LC {folio}](…): Sefaria's image of Leningrad Codex
       folio {folio}, where {where}" becomes "- [LC F{folio}](…): Sefaria's image of Leningrad Codex
       page F{folio}, where {where}". The function keeps its name.
    5. `_off_the_leaf` (`:216–220`): "runs past the last column of a leaf of {book}, so no folio line
       is given;" becomes "runs past the last column of a page of {book}, so no LC page link is
       given;". The function keeps its name.
21. **Question 5, `py/hkq_cmn/uxlc_manuscript_page.py`.** `:1`, "to Leningrad Codex folios." becomes
    "to Leningrad Codex pages."; `:5`, "counting folio 001A as 1," becomes "counting page F001A as
    1,"; `:13–14`, "looking the folios up" becomes "looking the pages up"; `:22`, "``<DDDA>`` is the
    folio label:" becomes "``<DDDA>`` is the page label:"; `:71`, "The folio in the DDDA form the image
    URLs use, e.g. 035A." becomes "The page in the DDDA form the image URLs use, e.g. 035A." Found
    after the planning answer: `:33`, "the decoded folio is compared" becomes "the decoded page is
    compared"; `:43`, "links ``uxlc_atom_locations``' folio" becomes "links the page
    ``uxlc_atom_locations`` estimates"; `:80`, "The Sefaria scan of one leaf" becomes "The Sefaria
    scan of one page"; `:83`, "estimated folio" becomes "estimated page". The formula at `:7`, "the
    folio and side" at `:9`, "three digits for the folio" at `:22` and the formula at `:111` speak of
    the leaf and stay; identifiers such as `folio_label` and the JSON field `folio` stay.
22. **Question 5, `py/main_estimate_uxlc_locations.py`.** The error message at `:172–176`: "of
    Leningrad Codex folio {guess['page']}" becomes "of Leningrad Codex page F{guess['page']}"; "a leaf
    of {case.ref.book} has {columns} columns" becomes "a page of {case.ref.book} has {columns}
    columns"; "run off the bottom of the leaf" becomes "run off the bottom of the page"; and "reach
    the page." becomes "reach the generated corrections page.", which names the other page the
    message now mentions; the same phrase at `:226` and `:233` becomes "reach the generated
    corrections page" too. Found after the planning answer, in docstrings: `:133`, "How many columns
    a leaf of this book has" becomes "How many columns a page of this book has", matching `:135–136`;
    `:145`, "a column this book's leaves have" becomes "a column this book's pages have"; and
    `:149–150`, "a two-column Sifrei Emet leaf too, as long as the flat line stays on the leaf"
    becomes "a two-column Sifrei Emet page too, as long as the flat line stays on the page". The
    `NOTE` constant (`:59–68`), which this mega step (`py/main_0_mega.py:513–520`) writes into
    `holman/data/uxlc_atom_locations.json`, stays, as the skill's not-swept list says.
23. **Question 5, found after the planning answer: other maintained Python.** Each names a
    Leningrad Codex page:
    1. `py/py_render/uc_case_card.py`, docstrings and comments: `:219`, "the folio link's
       neighbours" becomes "the page link's neighbours"; `:221`, "the folio link that" becomes "the
       page link that"; `:289`, "The estimated folio, column and line" becomes "The estimated page,
       column and line"; `:293`, "the folio his ordinal decodes to" becomes "the page his ordinal
       decodes to"; `:299`, "The folio was the card's own answer" becomes "The page was the card's own
       answer"; `:315`, "The Sefaria image of the estimated leaf." becomes "The Sefaria image of the
       estimated page.". Its output strings at `:310` and `:322` generate the page the skill leaves
       unswept, and stay.
    2. `py/clc/clc_render.py:742`: "(paired with the LC folio-102A detail image this spec carries)"
       becomes "(paired with the LC F102A detail image this spec carries)".
    3. `py/tests/clc_collect_test.py:151`: "an LC folio-102A detail image" becomes "an LC F102A
       detail image".
    4. `py/uxlc_paths.py:43`: "cumulative per-folio estimator counts;" becomes "cumulative per-page
       estimator counts;".
    5. `py/accgram/poetic_ob_notes.py:23`: "``LC-<folio>-col-<n>-line-<n>-<ref>.png``" becomes
       "``LC-<page>-col-<n>-line-<n>-<ref>.png``", as in `LC-159A-col-3-line-8-1S-17v5.png`.
    6. `py/hkq_cmn/uxlc_email_extract.py:149`: "reach the folio and column readers" becomes "reach
       the page and column readers"; the reader it means decodes a page such as 035A.
    7. For Ben's choice: `py/tests/test_mega_coverage.py:379–381`, the reason for
       `py/main_uxlc_estimate_atom_loc.py`, "a lookup that prints one estimated folio, column and
       line", which the program's `{'page': '430B', …}` shows to be a page. The reason is marked
       "Claude-written, accepted by Ben on 2026-09-10", so the plan proposes "a lookup that prints one
       estimated page, column and line" only if Ben approves changing an accepted reason.

## Sites found while planning (flagged; each for approval)

The planning sub-agents found these sites, where the package names no disposition. Sites 1 to 10
and 13 have the same defect as an approved item; by Ben's second planning answer each is proposed
here for his approval or striking, apart from the others. Sites 11 and 12 are defects of a kind the
package does not name, found by this plan's checks; each is presented for his approval or striking
in the same way.

1. **Finding 1's kind, `doc/blind-dive-into-template-params-update.md`,** present-tense accounts of
   the removed plain walker.
   1. `:68–70`: "the topmost-documentation-note finder and the plain/plus stack-path lookup now
      validate recognized templates before recording a result or recursing." becomes "the
      topmost-documentation-note finder and the plain/plus stack-path lookup were made to validate
      recognized templates before recording a result or recursing."
   2. `:87–88`: "Both walkers now validate names and shapes before matching or recursing. The plain
      walker also validates the recognized custom-tag leaves." becomes "Both walkers then validated
      names and shapes before matching or recursing, and the plain walker also validated the
      recognized custom-tag leaves; the merge `ebbfa90f`, which integrated the plain retirement on
      2026-09-28, removed that walker, and `_walk_wtel_plus` keeps the validation." (`87fc7141`, the
      retirement itself, and `52f1f6bf` both still had `_walk_wtel_plain`.)
   3. `:91`: "Normal and verbose CLI results for `E/נוסח` match before and after in each dataset"
      becomes "Normal and verbose CLI results for `E/נוסח` matched before and after in each
      dataset".

   The file's dated entry for finding 1.3 names these corrections too.
2. **Finding 23's kind, the bot's help and the downloader's docstrings.**
   1. `py/main_ws_bot.py:59–61`, the help of `--no-post-download`: "Skip the automatic post-run
      download of modified chapters to in/mam-ws" becomes "Skip the automatic post-run download,
      which refreshes the 36 declared special pages and downloads the modified chapters to
      in/mam-ws".
   2. `py/subcommands/download_wikisource.py:1`, the module summary: "Download revision-checked
      MAM chapters and rebuild affected production books." becomes "Download MAM's declared special
      pages and revision-checked chapters, and rebuild affected production books."
   3. The same file, `:4`: "--force-download retrieves every selected chapter." becomes
      "--force-download retrieves every selected chapter and all 36 declared special pages."
   4. The same file, `:19`: "Download selected chapters, then always run the affected-book product
      hook." becomes "Refresh the 36 declared special pages and download the selected chapters, then
      always run the affected-book product hook."
3. **Finding 28's kind, more live texts pinned to the primary forest.**
   1. The maintenance runbook's `:346`: "4. **Run from the MAIN MAM-basics clone, never from a
      worktree.**" becomes "4. **Run from a full MAM-basics clone, never from a worktree.**"
   2. `doc/edition-transcription-workflow.md`: at `:8–10`, "names a file under
      `C:/Users/BenDe/GitRepos/MAM-basics/py/`, which is why every command below runs from
      `C:/Users/BenDe/GitRepos/MAM-basics`, with that repo's interpreter." becomes "names a file
      under MAM-basics' `py/`, which is why every command below runs from the root of a full
      MAM-basics clone, with that clone's own interpreter."; and in all seven commands, at `:49`,
      `:55`, `:216`, `:244`, `:253`, `:279` and `:309`, the prefix
      `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/`
      becomes `./.venv/Scripts/python.exe py/`, the rest of each command unchanged. The lead-in at
      `:45–46` then stays.
   3. `py/main_verse_links.py:3–6`: "Run with MAM-basics' interpreter, from any directory -- every
      path here is resolved from this file, never from the cwd:" over
      `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_verse_links.py …` becomes
      "Run with a full MAM-basics clone's own interpreter; every path here is resolved from this
      file, never from the cwd. From the clone's root:" over
      `./.venv/Scripts/python.exe py/main_verse_links.py <book> <c:v> [<word> | --atom N]`.
   4. `hebrew-prose`'s `references/rendered-prose.md:236–237`: "A markdown link whose href is an
      absolute `file:///` URL, forward slashes:" becomes "A markdown link whose href is an absolute
      `file:///` URL to the page in the checkout that generated it, forward slashes; from a clone in
      `$HOME/GitRepos` it reads:". The example link stays.
   5. `py/mb_cmn/paths.py:170–171`, `sibling_repo`'s docstring: "Precedence: per-repo
      ``REPO_<NAME>_DIR`` -> ``REPOS_ROOT/name`` -> ``repo_root().parent/name``." becomes
      "Precedence: per-repo ``REPO_<NAME>_DIR`` -> ``repos_root() / name``, where ``repos_root`` is
      ``REPOS_ROOT`` or else the parent of this checkout's home clone."
4. **Finding 29's kind, the September 9 plan's "its read-only `--check`"** (`:82–83` and `:522`).
   The wording above, under "Findings 2.5, 28.5 and the extra finding-29 sites", includes both; if
   Ben strikes this site, items 2 and 3 there keep "its read-only `--check`" and take only their
   other changes.
5. **Finding 32's kind, four more statements of the rule and one receipt.**
   1. `doc/clone-forests.md:91–92`: "external inputs use explicit user-level account configuration."
      becomes "external inputs are user level: the scan archive at its default location, which
      `BOOK_SCANS_ROOT` overrides, and explicit account configuration such as pywikibot's."
   2. `in/repo_maintenance_policy.json:92`, in `clone_forests.portability`: "External inputs use
      explicit user-level configuration." becomes "External inputs are user level: the scan archive
      at its default location, which BOOK_SCANS_ROOT overrides, and explicit account configuration."
      No code reads `clone_forests`.
   3. `py/mb_cmn/paths.py:123–124`: "a worktree reads the same scans the primary clone does."
      becomes "every checkout on the machine, in any forest, reads the same scans."
   4. `py/scan_pages/editions.py:5–6`, the module docstring: "A worktree therefore reads the same
      scans the primary clone does." becomes "Every checkout on the machine, in any forest,
      therefore reads the same scans."
   5. `doc/PLAN-checkout-kinds-and-portable-knowledge-update.md`, whose entries put the date first,
      a dated entry on two passages of the executed plan, which stays as written:

      > ## <date>: corrections made in the 2026-09-29 review's remediation
      >
      > Recorded by <agent> on <date>, New York time, under the approved remediation plan for the
      > 2026-09-29 dual-agent review. The finished plan is left as written.
      >
      > 1. The third rule for every checkout kind, "Examples are the scan archive, found through
      >    `BOOK_SCANS_ROOT`" (`:170–172`): `py/mb_cmn/paths.py`'s `book_scans_root` finds the
      >    archive at `$HOME/OneDrive/Documents/ScansOfBooks` unless `BOOK_SCANS_ROOT` overrides it,
      >    and by Ben's decision of 2026-09-30 the common body's rule now names that default (the
      >    review's finding 32).
      > 2. "For each such clone it fetches and runs `git merge --ff-only origin/main`." and "It reports
      >    every other state and leaves it untouched." (`:302` and `:310`): the synchronizer's write
      >    form fetched every existing independent full clone with a matching origin before judging
      >    its eligibility. Since the remediation it refuses a clone that its own state disqualifies
      >    before any fetch, and an ahead or diverged clone after a fetch that changes only its
      >    objects, `FETCH_HEAD` and `refs/remotes/origin/main` (the review's finding 26).

      The plan's rules are introduced at `:161` as "Three rules apply to every kind:".

6. **Finding 14.4's kind, two more bare-path citations of the deleted sigil plan.**
   1. `doc/sigil-decoding.md:540`: "`doc/PLAN-replace-sigil-b2-with-t451.md` is the record of that
      work" becomes "the retired
      [`doc/PLAN-replace-sigil-b2-with-t451.md`](https://github.com/bdenckla/MAM-basics/blob/4f3fed2dcb1e21835ad73a31ea8e5e472f4960d7/doc/PLAN-replace-sigil-b2-with-t451.md)
      is the record of that work".
   2. `py/tests/test_ws_bot_sigil_b2_to_t451.py:18–20`: "and Phase 3 of
      doc/PLAN-replace-sigil-b2-with-t451.md re-downloads the six edited chapters into that same
      file." becomes "and Phase 3 of the retired doc/PLAN-replace-sigil-b2-with-t451.md, whose last
      version is at /
      https://github.com/bdenckla/MAM-basics/blob/4f3fed2dcb1e21835ad73a31ea8e5e472f4960d7/doc/PLAN-replace-sigil-b2-with-t451.md,
      / re-downloaded the six edited chapters into that same file." (each slash marks a line break).
7. **Finding 7's second documentation site, the maintenance runbook's hazard H2 (`:688–694`).**
   "Every tracked reference to one of those exact relative or absolute paths requires review; generic
   `.novc` policy prose does not." becomes "Every tracked reference to one of those exact relative or
   absolute paths requires review; generic `.novc` policy prose does not, and neither does a spelling
   of a target's root `.novc/t` or of anything below it, the suite's disposable base-temporary tree on
   Windows."
8. **Finding 2.5's kind, three every-reader routings to the Codex-only skill in the shared
   `hebrew-prose` skill.**
   1. `references/verifying.md:60–61`: "From a MAM-basics worktree, follow `AGENTS.md`, “Running
      tests”, and the worktree runtime reference." becomes "From a MAM-basics worktree, follow
      `AGENTS.md`, “Running tests”, and, for ChatGPT-Codex, the worktree runtime reference of
      `codex-worktree-tasks`."
   2. `references/verifying.md:107–109`: "following `AGENTS.md`, “Running tests”, and the worktree
      runtime reference:" becomes "following `AGENTS.md`, “Running tests”, and, for ChatGPT-Codex,
      the worktree runtime reference of `codex-worktree-tasks`:".
   3. `references/verifying.md:229–231`: "MAM-basics' `AGENTS.md`, “Running tests”, and
      `codex-worktree-tasks/references/worktree-runtime.md` own the current procedure;" becomes
      "MAM-basics' `AGENTS.md`, “Running tests”, owns the current procedure, with
      `codex-worktree-tasks/references/worktree-runtime.md` for ChatGPT-Codex;".
9. **Finding 20's kind, the HBCE outputs' "splitting them into chanted words".** In
   `hbce-psalms/README.md:38` and `DATA-LICENSES.md:99`, the outputs are said to change HBCE's forms
   by "splitting them into chanted words", but `hbce_finalize` (`py/hbce_psalms/compare.py:218–245`)
   never splits a form: it joins each form that ends in a maqaf to the next. On 2026-09-30, 1,499 of
   the 35 files' 11,789 `<w>` elements ended in a maqaf, and the 4 that hold an inner maqaf stay
   whole. The proposed clause, "they join each form that ends in a maqaf to the form after it, so
   that each form they quote is a chanted word" in the README and "by joining each form that ends
   in a maqaf to the form after it, so that each form they quote is a chanted word" in
   `DATA-LICENSES.md`, is folded into finding 20's wording above.
10. **Item 36.10's kind, `py/tests/test_mega_coverage.py:456–457`,** the reason for
    `"py/main_verse_links.py"`, which begins "Claude-written proposal, not yet reviewed by Ben: an
    on-demand lookup that prints the links for a verse, and an atom of it, named on its command
    line, and writes nothing." Proposed: "Ben's decision, <plan-approval date>, approving a
    Claude-written proposal: an on-demand lookup that prints the links for a verse, and an atom of
    it, named on its command line, and writes nothing." The rest of the reason stays.
11. **A defect beside finding 11, in `py/tests/test_wikisource_special_page_download.py`.** The last
    case, a manifest overwritten with "not json" (`:252–259`), runs after the swapped chapter
    records of the case before it (`:232–242`), which it never restores, so its `ValueError` comes
    from the chapter-owner check whether or not the manifest check works: a copy of `_load_manifest`
    that accepts "not json" still leaves the test passing. Proposed: before `:252`, rewrite the
    chapter manifest with `_write_chapter_manifest(chapter_manifest_path, endpoint,
    downloader.identities)`, and give the last case's `pytest.raises` `match="special-page
    manifest"`, the words of the loader's error (`py/ws/ws_special_page_download.py:287`). This is a
    test change under the exception finding 11 records, and the docstring's account of the last
    case stays true.
12. **A false sentence on a published page, beside question 5.** The generated Holman
    UXLC-corrections page, `gh-pages/holman/uxlc_corrections.html`, says in its introduction, from
    `py/py_render/uc_html.py:423–425`: "The folio link under the line is decoded from the page
    ordinal Holman's citation begins with, so the folio number is not his either." Since 2026-08-12
    the link has shown the estimate's page instead (`py/py_render/uc_case_card.py:299–302` and
    `:314–323`), and the card names the page Holman's ordinal decodes to only where it differs
    (`:308–310`). Proposed, keeping the page's own word "folio", which question 5 leaves unswept on
    generated pages: "The folio link under the line is the estimate's too; where the folio Holman's
    ordinal decodes to differs, the card names it beside the estimate." This changes a reader-facing
    page when the mega's `render-uxlc-corrections` step (`py/main_0_mega.py:521–528`) regenerates
    it; phase 4 regenerates it with `./.venv/Scripts/python.exe py/main_render_uxlc_corrections.py`.
13. **Finding 9.1's kind, `doc/memory-retirement-and-instruction-consolidation-2026-09-28-update.md:3`.**
    "State: open; first entry 2026-09-29." becomes "State: open, first entry 2026-09-29.", the
    recorded form. Finding 30's phase-1b entry, which this file gains anyway, names the
    correction.

**Noticed and left out**, each for the reason given:

1. `gh-pages/style.css:3–5` and `py/author_site/unicode_proposals.py:17–18`, on which pages the
   root stylesheet serves, and `py/main_repo_maintenance.py:38`: turn 01 listed them under "Noticed
   outside the diff, not findings", which the package leaves as it is.
2. The bare citations of `doc/PLAN-mega-coverage.md` at `py/boj_paths.py:103`,
   `py/main_0_mega.py:213`, `:244`, `:273` and `:499`, `py/main_diffable_pointed_hebrew.py:29`,
   `py/repo_hygiene/source_hygiene.py:43` and `py/tests/test_h_dot_below_nfc.py:221` and `:377`:
   each dates a change to a phase of that plan, and the 2026-09-26 review's finding 6 counted such
   lines among its 94 historical attributions, not among its defects
   (`doc/dual-agent-review-2026-09-26-turn-01-claude.md:756–760`). The receipt
   `py/ws/ws_bot_edit_history.md:193` keeps its words.
3. The floor comment at `py/tests/test_h_dot_below_nfc.py:450–451`, whose file count is stale: a
   different defect from finding 14.1's dead prefixes, which the package does not name.
4. The test id at `py/tests/test_wikisource_special_page_download.py:131`: renaming it would change
   a test id, as finding 12's item says.
5. The runbook table's missing Codex compatibility actions and `--check`'s help, which omits
   `--forest-status`: gaps of a different kind from finding 28's pinned paths and finding 29's
   label.
6. `_plus_header`'s branch for legacy plain headers in `py/py_misc/mam_parsed_plus.py`: whether that
   branch is still reachable is a code question that finding 14.3's rewording does not settle.
7. The September 9 plan's D13 (`:435`) and §4 item 7 (`:492`), which cite `worktree-forest/SKILL.md`,
   removed by `7cf780e1` on 2026-09-29: whether D13 is moot belongs to Ben's decision whether that
   plan is spent, which its section "Current execution boundary, corrected 2026-09-28" leaves open.
8. `holman/doc/uxlc-email-count-disagreements.md:101`, whose "leaf 621" and "leaf 623" are page
   ordinals rather than leaves: the dated research record is a receipt with no update, and the
   package does not name it.

## Finite execution ledger

"Active" means an approved disposition whose execution is pending; it claims nothing is fixed.

| Finding | Status and exact scope |
|---|---|
| 1 | Active. 1.1: the notice order and its regeneration (public data). 1.2: the shadowed `paths` (defect). 1.3: `87fc7141`'s two corrections (editorial, its own wording). |
| 2 | Active. 2.1 (approved wording) in the README and two docstrings; 2.2 and 2.3 (editorial); 2.4's "folio 57a" (approved wording) and "folio 307b" (editorial); 2.5 (editorial) at the common body's `:84` and `:302` and in the September 9 plan; the dated entry in the 2026-09-26 close-out record (editorial). 2.6 is finding 4. |
| 3 | Active: 3.1's heading and 3.2's sentence (editorial; reader-facing). |
| 4 | Active: 4.1's second site, 4.2 to 4.5 and 4.7 to 4.9 (editorial). Already resolved: 4.1's first site and 4.6, by `e4934b6e`. |
| 5 | Active: 5.1 to 5.5 (editorial); 5.6 (defect). |
| 6 | Active: 6.1 to 6.3 (defects in tests). |
| 7 | Active: `.novc/t` stops gating retirement (defect; recommended choice), with gate 4's wording (editorial). |
| 8 | Active: 8.1 for Ben's approval or reversal (recommended: approval); 8.2 by question 5, the skill section and the conforming edits (editorial). |
| 9 | Active: 9.1's State form (recorded form); 9.2's record in the update (editorial; recommended choice). |
| 10 | Active: 10.1 with question 6, `DATA-LICENSES.md` and the five product licence files; 10.2 (editorial; reader-facing). |
| 11 | Active: the exception for all five stub test ids, in `AGENTS.md` and the test module's docstring (editorial; question 1). No test changes. |
| 12 | Active (editorial). |
| 13 | Active (editorial; the README is reader-facing). |
| 14 | Active: 14.1 and 14.2 (defects); 14.3's two false references and three rewordings (editorial; recommended choice); 14.4 (editorial). |
| 15 | Active (defect). |
| 16 | Active (defect), with its `NOT_IN_MEGA` reason (editorial). |
| 17 | Active (defect; recommended choice). |
| 18 | Active: 18.1 and 18.2 (editorial; reader-facing). |
| 19 | Active (editorial). |
| 20 | Active (editorial; reader-facing). |
| 21 | Active: the new update file for the HBCE receipt (editorial). Deferred: the heading fix in `py/hbce_psalms/compare.py`; `hbce-psalms/out/` stays unchanged. |
| 22 | Deferred: no MAM-basics change; the next dependent refresh checks that the variant reaches phonetic-hbo's page and the survey. |
| 23 | Active (editorial; the skill is deployed). |
| 24 | Active: 24.1 and 24.2 with the module docstring (editorial; reader-facing). |
| 25 | Active (defect; recommended choice), with a new lint. |
| 26 | Active (defect; recommended choice), with its texts (editorial). |
| 27 | Active (editorial; reader-facing). |
| 28 | Active: 28.3 to 28.6, turn 07's ten runbook lines and the three action-table rows (editorial). Already resolved: 28.1 and 28.2, by `4d3ebf66`. |
| 29 | Active (editorial). |
| 30 | Active: the tracked list, drafted and checked in phase 1a and written in `C:/Users/BenDe/GitRepos/MAM-basics` in phase 1b with the wording Ben approves (editorial). |
| 31 | Active (editorial). |
| 32 | Active: the common body's rule names the default location, with `BOOK_SCANS_ROOT` as its override (editorial; question 3). |
| 33 | Active: the home clone stays fast-forward-only; the common body and the Codex lifecycle gain a fetch step and a refused-push branch (editorial; question 4). |
| 34 | Active: 34.1 to 34.3 (editorial; the skills are deployed). |
| 35 | Active (editorial). |
| 36 | Individually, below. |
| C1 | Active (editorial). |
| E1 | Active (editorial). |
| Round record | Active: the September 29 round's subsection in `doc/dual-agent-review.md`, which that document requires after Ben's decisions (editorial). |
| Sites found while planning | Active for each site Ben approves: sites 1 to 10 and 13 (editorial), 11 (a test defect) and 12 (a reader-facing page). A struck site is recorded as `superseded`. |

### The items of finding 36, and the other deferrals

| Item | Disposition |
|---|---|
| 36.1 | Active with finding 10.1 (question 6). |
| 36.2 | Active: `AGENTS.md` and `py/product_scopes.py` amended (question 2); MAM-for-Sefaria and MAM-OSIS are not rerun. |
| 36.3 | Deferred: whether an in-place correction of a claim false when written needs a dated note is a receipt-policy question. No note is added for `22d18d72`'s unmarked in-place rewrites in the eight update files that lack one. Three of them, those of findings 4.1, 4.7 and 4.8, are corrected here, and their new entries name only this plan's corrections. This plan's own corrections carry dated entries by Ben's third planning answer, which decides nothing more. |
| 36.4 | Deferred: only Ben can supply the words of his 2026-09-28 decisions; no attribution is reworded. |
| 36.5 | Deferred: the published memory topics and MAM-private metadata. |
| 36.6 | Deferred: differential tests of the forest modules and of the freshness guard's failure path. |
| 36.7 | Deferred: whether a loanword like "taamim" is a Hebrew filename component; no action on the four pre-rule slugs. |
| 36.8 | No action in remediation: the Sheet link on the English Decalogue page is an outward-facing Wikisource edit, Ben's to make. |
| 36.9 | No action: `e4934b6e` retired the executed Google Sheet plan. |
| 36.10 | Active: the `NOT_IN_MEGA` reason; running `lint-receipt` in the suite stays deferred. |
| 36.11 | Deferred: whether a validator must itself dispatch over every recognized template. |
| 36.12 | Active: the account of the plain retirement in `MAM-parsed/README.md`; no action on `cam1753/cam1753-page-index.json:3`, whose retained JSON may not change. |
| 11's older tests | No action on the fourteen pre-window example-based methods of `py/tests/test_main_download_fr_wikisource.py`. |

## Outputs expected to stay unchanged

Any other diff is a finding and blocks integration until explained.

1. **Allowed generated diffs:** the two exchanged notice lines in each of the 24
   `MAM-parsed/plus/*.json` files; the same two rules exchanged in the three places of
   `gh-pages/MAM-parsed/plus/html/mpplus.html` that "Rendered HTML" names; line 2 of
   `py/verify_mp/expanded_stack_grammar_parser_stage.lock.json`; and, if Ben approves flagged site
   12, the one sentence of the introduction of `gh-pages/holman/uxlc_corrections.html`.
2. **Unchanged:** every Scripture payload and every `book39s` value; `MAM-simple/`,
   `MAM-for-Sefaria/`, `MAM-OSIS/` and `MAM-with-doc/` apart from the licence files;
   `MAM-parsed/py-examples/` and `MAM-parsed/py-examples-out/`; every other page under
   `gh-pages/`, including `gh-pages/post-stress-meteg-post-silluq-1k14v14.html` (finding 5.6), the
   rest of `gh-pages/MAM-parsed/` and `doc/mp-claims.md` (finding 14.2), and every change-log file
   under `gh-pages/MAM-with-doc/change-log/`; `out/tmpl-survey-plus/plus.json` and the plus grammar
   lock (finding 17 leaves the collectors unchanged); `out/accgram/post-stress-meteg.json`;
   `hbce-psalms/out/`; `in/mam-ws/`, `in/mam-ws-special/`, and the pages and manifest of
   `in/mam-ws-intro/`, whose README alone changes; every archive under
   `MAM-parsed/historical/`; `holman/data/`; `evr-ii-b-55/evr-ii-b-55-page-index.json`; the
   Cambridge 1753 and Aleppo data; and every finished base named here, apart from the one permitted
   pointer line of the HBCE receipt.
3. **Not touched:** MAM-private, which only the suite and the mega's documented steps read; live
   deployed instructions, until the deployment step.

## Execution, verification and integration

### Phases

These dependency phases order the work; they do not permit implementing only part of it. The root
executor may choose smaller coherent commits and read-only sub-agents, keeping one writer.

1. **Phase 0, the development checkout.** The checks and the D11 start under "Standalone executor
   contract". The first commit moves this plan's line 3 to "State: live; approved for execution
   <date>; remediation in progress." if the approval record has not already set it.
2. **Phase 1a, `C:/Users/BenDe/GitRepos/MAM-basics`, read-only: finding 30's draft.** It comes
   first because until phase 1b lands, a default `py/main_repo_maintenance.py` run in that clone can
   delete its only source. Read the proposal, draft the rows and entries in the session's scratch
   directory, apply the privacy check and present the draft to Ben, as finding 30's item describes.
   Nothing is written into either checkout. Phases 2 to 4 need not wait for his answer.
3. **Phase 1b, `C:/Users/BenDe/GitRepos/MAM-basics`, after Ben's answer and before phase 5.** First
   push the development checkout's last commit; that checkout writes nothing until phase 1b is
   pushed. Name that clone in every command with `git -C C:/Users/BenDe/GitRepos/MAM-basics`.
   Verify it clean and on `main`; fetch `origin`; verify that `origin/dar-2026-09-29` is the
   development checkout's last pushed commit. That clone had no local `dar-2026-09-29` on
   2026-09-30, so create the carrier with
   `git -C C:/Users/BenDe/GitRepos/MAM-basics switch -c dar-2026-09-29 origin/dar-2026-09-29`, or,
   if it exists, switch to it and fast-forward it with `merge --ff-only origin/dar-2026-09-29`.
   Write the wording Ben approved; run that clone's own
   `./.venv/Scripts/python.exe py/main_test.py py/tests/test_receipt_update_links.py py/tests/test_prose_conventions.py py/tests/test_prose_mark_order.py`
   from its root, and `git -C C:/Users/BenDe/GitRepos/MAM-basics diff --check`; commit; push with
   `git -C C:/Users/BenDe/GitRepos/MAM-basics push origin HEAD:dar-2026-09-29`; and switch that
   clone back to `main`. The development checkout then fetches and fast-forwards its carrier before
   its next edit.
4. **Phase 2, the development checkout: records, instructions and procedures.** The lower-risk
   Markdown, update entries, agent instructions, skills, runbooks, the September 9 plan under Ben's
   8.1 choice, the round record and the Markdown and instruction flagged sites Ben approves.
   Passages that describe a phase-4 behaviour change wait for that change, below.
5. **Phase 3: the reader-facing documents and the five product licence files.**
6. **Phase 4: code, tests and docstrings,** including finding 1.1's source change and its
   regeneration, and the Python flagged sites Ben approves. Commit each passage that describes a
   behaviour change with that change: gate 4 of `references/repository-maintenance.md` and hazard
   H2 with finding 7; the `verse-links` skill's table row (`SKILL.md:70`) with
   `py/main_verse_links.py`; `doc/clone-forests.md`, the runbook's `--sync-forest` rows and the two
   forest docstrings with finding 26.
7. **Phase 5: the full suite, final integration, deployment and the closing records.**

### Checks for every commit

1. Verify `HEAD` and task-owned status before staging, and stage only this plan's paths.
2. `git diff --check`.
3. Black at its defaults on every changed Python file, with `./.venv/Scripts/python.exe -m black <files>`.
4. For Markdown, update and instruction commits:
   `./.venv/Scripts/python.exe py/main_test.py py/tests/test_receipt_update_links.py py/tests/test_prose_conventions.py py/tests/test_prose_mark_order.py`.
   The prose-convention lint also scans every changed `py/**/*.py`.
5. The item's own verification, from the lists above and the table below.
6. Write each multi-line commit message to a uniquely named UTF-8 scratch file and commit with
   `git commit -F`. Push every commit with `git push origin HEAD:dar-2026-09-29`; never force, and
   stop on a refused push. Do not push `main` before phase 5.

### Targeted verification

| Finding | Command or check, from the development checkout's root |
|---|---|
| 1.1 | `./.venv/Scripts/python.exe py/main_parse.py ws`; then `py/main_test.py py/tests/test_public_data_consumer_notices.py`; the diff is the two exchanged lines in each of the 24 JSON files and the three exchanges in `mpplus.html`, nothing else; rules 5 and 6 equal `52f1f6bf`'s; in each file the first "narpas", case-insensitively, is the gloss. |
| 1.2, 14.2 | `./.venv/Scripts/python.exe -m ruff check --no-cache py`; the `--find-stack-path` and `--find-stack-path-verbose` commands written out under finding 1.2; `py/main_test.py py/tests/test_stack_path_lookup.py py/tests/test_mega_coverage.py`. |
| 5.6 | `./.venv/Scripts/python.exe py/main_authored.py gen-site --trust-surveys`, with no tracked diff; `py/main_test.py py/tests/test_scan_overlay_viewboxes.py`. |
| 6.1 | `py/main_test.py py/tests/test_worktree_retirement_policy.py`, and the scratch mutations. |
| 6.2 | `py/main_test.py py/tests/test_mpplus_alternative_oracle.py`, and the scratch run over `f4d81285`'s report. |
| 6.3, 7 | `py/main_test.py py/repo_util/worktree_retirement_simulation_test.py -q` and the policy lint. |
| 14.1 | `py/main_test.py py/tests/test_h_dot_below_nfc.py`. |
| 15, 17 | `py/main_parse.py ws` passes; the scratch injections and mutations now raise. |
| 16 | `./.venv/Scripts/python.exe py/main_parse.py ws --write-parser-stage-grammar-lock`, run before finding 1.1's source change or after its regenerated products are committed, then a diff of line 2 of the lock alone; `py/main_test.py py/tests/test_mega_coverage.py`. |
| 25 | `py/main_test.py py/tests/test_forest_subprocess_bounds.py py/tests/test_worktree_retirement_policy.py`. |
| 26 | Reading, Black and the full suite; do not run the write form. |
| 21 | `./.venv/Scripts/python.exe py/main_hbce_psalms.py lint-receipt` reports "0 problems"; the receipt lint. |
| 36.2 | `py/main_test.py py/tests/test_product_scopes.py`. |
| Flagged site 5.2 | `py/main_test.py py/tests/test_repo_visibility_declared.py py/tests/test_sibling_reach.py py/tests/test_no_machine_paths_in_artifacts.py`, the tests that read `in/repo_maintenance_policy.json`. |
| Flagged site 11 | `py/main_test.py py/tests/test_wikisource_special_page_download.py`, and, as a scratch check, a copy of `_load_manifest` that accepts "not json" now makes the last case fail. |
| Flagged site 12 | `./.venv/Scripts/python.exe py/main_render_uxlc_corrections.py` changes only the introduction's sentence in `gh-pages/holman/uxlc_corrections.html`; `holman/docs-not-served/uxlc_corrections.json` stays byte for byte. |
| Question 5 | `./.venv/Scripts/python.exe py/main_verse_links.py 1Samuel 17:5 --atom 14` prints an `LC F159A` line reading "Sefaria's image of Leningrad Codex page F159A". Then `git grep -n -I -i -E "folio [0-9]"` finds only the not-swept outputs and their sources (the generated Holman page with `py/py_render/uc_case_card.py:310` and `:322`, the goerwitz page, the EVR page index's note), receipts and the dated entries of open update files, the dated Holman research records, external captures, the LCIndex notes copied into `in/lci_recs.json`, `uxlc/data/lci_augrecs.json` and `uxlc/out/UXLC-misc/lci_recs.xml`, the new `terminology.md` section and routing line, and this plan; and `git grep -n -I -i -E -e "leaf [0-9]" --and --not -e "leaf 270 recto" --and --not -e "extra leaf 241a"` finds only receipts, dated update entries, `holman/doc/uxlc-email-count-disagreements.md:101`, the new section's "leaf 83r" and this plan. Neither search proves the sweep complete: forms such as "folio **57a**", "per-folio" and "the folio link" escape both, so the site lists under question 5 are the check for those. |
| Docstrings and comments | Black, and the prose-convention lint. |

`py/main_test.py` above means `./.venv/Scripts/python.exe py/main_test.py`.

### The full suite

Run `./.venv/Scripts/python.exe py/main_test.py` once, after the last executable, test, schema or
shared-data change; a later documentation, comment or instruction commit does not expire it. Record
its passed, skipped and subtest counts, with the commit.

### Final integration

1. In the development checkout, fetch `origin` and merge current `origin/main` into the carrier.
   Resolve any conflict there, and repeat the checks whose inputs the merge changed.
2. Run the mega from the development checkout's root with no `REPOS_ROOT`:
   `./.venv/Scripts/python.exe py/main_0_mega.py`. A failing step or an unexplained tracked diff is a
   failure. Read the diff, explain it, and commit every explained generated change; push it to
   `origin/dar-2026-09-29`.
3. Fetch with `git -C C:/Users/BenDe/GitRepos2/MAM-basics fetch origin` and verify that
   `origin/dar-2026-09-29` is exactly the mega-verified commit. Switch the clean checkout with
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics switch main`, fast-forward it with
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics merge --ff-only origin/dar-2026-09-29`, and push with
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics push origin main`. If the fast-forward or the push is
   refused because `origin/main` moved, switch back to the carrier, merge the new `origin/main`,
   verify again, push the review branch, and retry. Never merge in `main` or force a push. This push
   reaches the published Pages tree and the distributed products; it is an outward-facing act.
4. Deploy the common body and the changed skills from this full clone, then check:
   `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config`, then
   `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check`, which must report
   every destination `clean`.
5. Commit the closing records ("Records" below) on the carrier, push them with
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics push origin HEAD:dar-2026-09-29`, fast-forward
   `main` to them and push `main` again as in step 3, and repeat the `--check` of step 4. The
   2026-09-26 round closed the same way
   (`doc/dual-agent-review-2026-09-26-turn-01-claude-update.md:739–746`); these records change no
   source, product or canonical configuration, so the suite, mega and deployment evidence stands.
6. Leave the clone on `main`. Keep both carriers and `origin/dar-2026-09-29`; retiring a local
   carrier is later cleanup that needs Ben's approval, and deleting the remote branch is separate
   outward-facing cleanup that needs its own authorization.

### Records

1. Put every disposition and all verification evidence in the review's live update,
   `doc/dual-agent-review-2026-09-29-turn-01-claude-update.md`, in dated entries modelled on the
   2026-09-26 round's: "Approved remediation implemented; final gates pending, <date>", with a
   disposition row for each of findings 1 to 36, C1, E1 and each flagged site; then "Final
   integration and configuration deployment completed, <date>", with the suite counts, the mega
   result, the commits and the deployment check. The first of them records the development
   checkout's path and the `HEAD` at which editing began, and maps every ledger row onto
   `implemented`, `superseded`, `deferred` or `unresolved`. The base's line 3 stays as written.
2. In the commit of the closing record, set this plan's line 3 to "State: executed <date>."; the plan
   is then a receipt, corrected later only through its single update.
3. The dated entries in the corrected update files, which "Editorial proposals: receipts' live
   updates and new records" describes, belong to the commits of their phases, not to these closing
   records. The one exception is item 2's entry in the 2026-09-26 close-out record, with its two
   in-place corrections, which goes in the closing-records commit because it dates completions
   that land in phases 2 to 5.
