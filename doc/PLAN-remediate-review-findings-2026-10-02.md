# Remediate the October 2, 2026 trial review of MAM-basics

State: executed 2026-10-03; left to Ben: A1, refused by the relay-machine session's permission rules; A4 and A5, blocked on the relay machine; and A9
Updates and later status: [PLAN-remediate-review-findings-2026-10-02-update.md](PLAN-remediate-review-findings-2026-10-02-update.md).

Prepared by Claude on 2026-10-03, New York time, as close-out step 2 of the 2026-10-02 trial review
(`doc/periodic-review.md`, "Close-out: from findings to dispositions"). The session ran as Claude
Opus 5.5 at `max` in the Claude desktop app, on the machine `LAPTOP-DBLE8UKA`, in the full clone
`C:/Users/BenDe/GitRepos2/MAM-basics`, on clean `main` at
`644a6c9c3203e12e5fe7bdad75b165c16bb9aab5`, equal to `origin/main` after a fetch. It worked from a
prompt that the trial's owner session wrote on 2026-10-03 and Ben pasted in. That prompt quotes
Ben's instruction that started the review, "start a new review, using the very-new (just committed)
simplified dual agent process, which is not fully fleshed out so I guess that will be part of this
review, to fully flesh it out.", and names his three selections of 2026-10-03, which
[`review-findings-2026-10-02-update.md`](review-findings-2026-10-02-update.md), "Ben's close-out
decisions, 2026-10-03", records. The rest of the prompt is the owner session's reconstruction of
this step, and this plan attributes none of it to Ben.

**What is approved and what is not.** Ben approved the disposition list as the close-out package on
2026-10-03. As the update records, that approval "records dispositions only. It does not execute
remediation, and it does not approve wording that the remediation plan must present", in particular
C1's gate design and C2's corrected Yeivin prose. This plan proposed the remediation's concrete
wording and its execution, with thirteen choices that were his alone. Later on 2026-10-03, after it
was pushed, Ben accepted every recommendation in it and, for six items that it had left without
one, the recommendation that its preparing session then gave; he also authorized every act outside
the repository in advance, asking for execution "as unattended as possible". "Decisions this plan
follows", item 4, quotes him. Execution begins when Ben starts the executor's session; preparing,
committing or pushing this plan implemented none of it.

**How it was prepared.** Eight read-only sub-agents, each given one group of items, re-read the files
at `644a6c9c`, quoted the current wording, drafted the proposals and demonstrated each mechanism in
memory or on scratch copies. They wrote nothing in any repository and read nothing in MAM-private,
hbofonts or the private `bdenckla/trope`. The root session re-read the passages and code that the
proposals rest on, re-ran the measurements that decide a disposition, and changed several proposals;
where this plan departs from the update file's notes or from a sub-agent's recommendation it says so.

**Citations.** Findings are cited as the update cites them: Claude finding `n` as `C<n>`. Line
numbers are those of `644a6c9c`; a passage's own quoted words, not its number, identify it. Between
the review's end commit `db59ef5e` and `644a6c9c` only book-of-Job files and review records changed,
so the review's citations hold apart from `doc/dual-agent-review.md`. This plan never repeats a path
inside a private repository: Ben's rule of 2026-08-27, in `in/repo_maintenance_policy.json`'s
`repo_visibility` comment, allows a private repository's name in a public file but not "paths inside
them, file names of theirs".

## Standalone executor contract

**Checkouts.** The development and integration checkout is a full clone, by default
`C:/Users/BenDe/GitRepos2/MAM-basics` on `LAPTOP-DBLE8UKA`; another verified full clone may serve,
and then its path replaces this one throughout. Work happens on a local branch
`remediate-review-2026-10-02`, which every commit is pushed to as `origin/remediate-review-2026-10-02`;
`main` is fast-forwarded to it and pushed only at final integration. This plan names that branch
under the "Git and commits" exception of the common instruction body, for two reasons: a push of
`main` that carries a generator change owes the mega first, and Pages deploys `main` daily at 04:17
New York time, so the remediation's intermediate states must not reach `main`; and the work may
span sessions, which hand off only through commits pushed to `origin`. A session that ends before
final integration pushes its last commit to the branch and switches the clone back to `main`,
because `doc/clone-forests.md`'s synchronization check fails a full clone on any other branch.
Create no linked worktree. One agent writes at a time; read-only sub-agents may investigate and
check. The executor of final integration owns it and pushes `main`.

**Unattended.** Ben has answered every choice and authorized every act outside the repository in
advance ("Decisions this plan follows", item 4). Do not ask him again for a choice or an act that
this plan settles; implement each chosen option and no other. Stop only on the stop conditions
below, on a failing check, or on a fact that contradicts this plan or that it does not settle, and
then report with a standalone continuation prompt.

**Not the relay machine's GitRepos2 before A1.** The relay's scheduled task runs the GitRepos2 clone
of the machine that ran the relay every three minutes ("The relay's retirement", below). If the
executor works on that machine, act A1 must be done before the first relay-retirement edit there.
The default executor works on `LAPTOP-DBLE8UKA`, which holds no relay state; the relay machine's acts
belong to the separate session that "The relay-machine session" describes.

**Baselines.** Before any edit, require each of these to be an ancestor of `HEAD`, with
`git -C <checkout> merge-base --is-ancestor <commit> HEAD`: `644a6c9c3203e12e5fe7bdad75b165c16bb9aab5`;
`286d2e8cce69b1cc798b67302b80a91f4c6c161a`, the commit that adds this plan; and the commit "Record
Ben's choices and advance authorization for the 2026-10-02 remediation", which records them in the
update file and revises this plan to match (find it with
`git -C <checkout> log --format="%H %s" -- doc/review-findings-2026-10-02-update.md`). Record the
checkout's path and the exact `HEAD` at which editing begins in the update entry that "Records"
describes. The reviewed window, `7549ebf7..db59ef5e`, is a historical anchor, not a baseline.

**Interpreter.** The full clone's own `./.venv/Scripts/python.exe`, run from its root. In this plan
`py/main_test.py <paths>` means `./.venv/Scripts/python.exe py/main_test.py <paths>`.

**Instructions and skills to load first.**
1. `AGENTS.md`.
2. `doc/periodic-review.md`: "Close-out: from findings to dispositions", "Verification cadence during
   remediation", "Separate defects from editorial proposals" and "Present remediation by
   public-facing risk".
3. `iterative-document-editing`: "Executable plans", "Finished receipts and maintained documents"
   and "MAM-basics and MAM-private State conventions".
4. `hebrew-prose`, with `references/core-rules.md`, `terminology.md`, `rendered-prose.md`,
   `mam-basics.md` and `sources-and-corpora.md`, before any edit to C2's Yeivin prose, C5's
   README section, C12.4's docstring, C15.15 or C10.3.
5. `mam-repository-topology`, with `references/repository-maintenance.md` ("Manual document
   retirement" and "Completed linked worktrees"), for the relay's retirement.
6. `github-issues`, for the retirement's read-only reference audit; this plan performs no issue
   operation.
7. `mam-wikisource-refresh`, before editing its canonical copy (C1, C7, C8).

Edit only the canonical copies under `dot-claude/` and `dot-Codex/`, never a live deployed copy.

**Before every edit phase**, verify with separate commands, each naming the checkout with `-C`:
`git rev-parse --show-toplevel`, `git rev-parse HEAD`, `git branch --show-current`,
`git status --porcelain=v1 -z` and the ancestry checks. Stop on unexpected `HEAD` movement, another
writer's files, missing source material, a refused push or an unexplained generated diff.

**At the start of every executing session**, in the checkout: `git -C <checkout> fetch origin`; switch
to the branch (`git -C <checkout> switch remediate-review-2026-10-02`, or, the first time,
`git -C <checkout> switch -c remediate-review-2026-10-02` from the clean `main` that holds the
baselines, then `git -C <checkout> push origin HEAD:remediate-review-2026-10-02`); fast-forward it to
its remote with `git -C <checkout> merge --ff-only origin/remediate-review-2026-10-02`; merge current
`origin/main` into it with `git -C <checkout> merge origin/main`, resolving any conflict there; push
any commit that merge made. Re-measure any passage this plan cites in a file changed since
`644a6c9c` (`git -C <checkout> diff --stat 644a6c9c HEAD`).

**Not authorized:** amending, rebasing, force-pushing, resetting, dropping a stash, discarding work;
deleting a branch or worktree except as "Acts outside the repository" below permits; retiring or
reclassifying a document other than the two relay documents of R1; any GitHub issue operation
beyond the read-only audit; any Wikisource edit or refresh; running `py/main_mam4sef.py`,
`py/main_mam_osis.py` or `py/main_hbce_psalms.py compare`; the write form of `--sync-forest`; reading
MAM-private or hbofonts beyond what the suite and the mega's documented steps read; editing a live
deployed instruction, skill or agent file except through acts A2 and A3; deleting permanently
anything that Git history does not keep.

**Do not refresh MAM from Wikisource before C1 lands.** Until then a refresh that changes MAM's text
changes the Phonetic MAM release and stops the mega at `yeivin-itm-survey-meteg-claims` (the update,
entry 1). This is a caution for Ben's own refreshes as well as the executor's.

## Decisions this plan follows

1. **Ben's close-out decisions of 2026-10-03**, which `doc/review-findings-2026-10-02-update.md`,
   "Ben's close-out decisions, 2026-10-03", records with his selections verbatim:
   1. "Approve as listed (Recommended)": the disposition list is the close-out package. The 64
      accepted items are fixed here; C3 stands as fixed after the review, by a deployment; C15.1
      stands as rejected.
   2. "Keep the legacy bytes" for C14: the decomposed acute and breve vowels of `Phonetic-MAM/` and
      `gh-pages/phonetic-mam/` stay, and the exemption in `py/tests/test_h_dot_below_nfc.py` cites
      this decision.
   3. "Retire the relay now": "The relay's retirement", below.
   4. The three procedure changes, already applied to `doc/dual-agent-review.md` in `644a6c9c`.
2. **The update file is the authority** for every disposition, correction and remedy note; where it
   corrects the Claude report, this plan uses its figures and citations. Where this plan's checks found
   a note of the update's to be inexact, the item says so: C9.1's "only from the two relay test
   modules", C10.3's "eighth site", C12.2's "25", C15.25's "a framing Ben chose" and C2's "to 557".
3. **Earlier decisions relied on, and not reopened:**
   - Ben's rule of 2026-08-27 on private repositories in public files (`in/repo_maintenance_policy.json`,
     `repo_visibility`), for C4.1 and C15.31.
   - His deferral of 2026-09-28 of the private-tree paths in `doc/windows-long-paths.md` (the
     September 26 round's finding 35.1), which stands; C4.1 leaves that guide alone.
   - His approval of 2026-09-30 of `MAM-with-doc/LICENSE.md`'s edition sentence, which C4.4 keeps
     word for word in either option.
   - His decision of 2026-09-19 that the publication permission extends to the editable Yeivin
     adaptation, whose words C4.6 keeps; and his approval of 2026-10-01 of the corrected Yeivin claims,
     which C2 extends.
   - No change here touches a hand-run generator (`py/main_mam4sef.py`, `py/main_mam_osis.py`,
     `py/main_hbce_psalms.py compare`) or any input it reads, so none is run; MAM's text does not
     change.
   - The common instruction body's "Tests are differential or lint-shaped": no item adds an
     example-based test; where none is admissible, the item names a scratch demonstration instead.
   - `doc/periodic-review.md`'s D7 and risk ordering, which shape this plan.
4. **Ben's choices and advance authorization, 2026-10-03,** given in this plan's preparing session
   after the plan was pushed at `286d2e8c`. His words, verbatim: "Regarding my choices, I accept all
   your recommendations. Are there any choices for which you had no recommendation?" The session
   then named six items without a stated recommendation, recommended one course for each, and said
   that accepting them would not authorize the acts in advance, since the executor would still ask
   him for each act at its turn. His reply, in one message: "I accept all those recommendations as
   well." and "Please authorize those acts in advance. I want this all to be as unattended as
   possible." So:
   1. Every recommended option of the thirteen questions under "Choices for Ben" is chosen; the
      executor implements that option and no other.
   2. The six further items: the flagged addition under C15.13 is made; A5, A8, A9 and A10 are done;
      A6 is not done, so `origin/dar-2026-10-01` stays, as the other round branches on origin do.
   3. Every act outside the repository, A0 to A10, is authorized in advance in the form this plan
      gives it. This plan reads "those acts" as all of them, since Ben asked for everything to be
      as unattended as possible. Each outcome is still recorded.
   4. Every other proposal in this plan stands as written, R5 included.
   5. In recording this, the preparing session revised the acts only toward caution. No act deletes
      anything: A2 and A8 move the agent file and the rehearsal home into a retention folder, which
      Ben may delete whenever he wants the space. A plain deletion would be permanent, and a
      recycling that runs without confirmation dialogs can delete permanently a folder too large
      for the Recycle Bin; the rehearsal home holds a whole clone with its environment. A7's
      selection of entries is spelled out. A9 is left to Ben in the Codex app, since this plan has
      no verified command that deletes a Codex follow-up. A new section, "The relay-machine
      session", gives the relay machine's acts to a session that Ben starts there, since the
      executor works on another machine.

## Choices for Ben, answered 2026-10-03

These were the decisions this plan left to Ben. Each names the item where its options are written
out in full, with their wording. They are in the order of `doc/periodic-review.md`, "Present
remediation by public-facing risk"; the recommended option is listed first. **On 2026-10-03 Ben
accepted every recommended option** ("Decisions this plan follows", item 4), so the executor
implements: for 1, the figures-only correction, keeping "roughly"; for 2, "Is 52:1"; for 3, 4, 5, 9,
10, 11, 12 and 13, option 1 of each item; for 6, option 2; for 7, Gate B and Oracle A; and for 8,
option C. Text elsewhere in this plan that applies only under an option Ben did not choose is moot.

1. **C2's corrected Yeivin prose.** Approve the figures-only correction of nine sentences on three
   published pages and the 11 corrected fractions in `Yeivin-ITM/meteg-claims.json`; or reword. A
   detail inside it: whether φ3's "agrees, roughly, with this estimate of 200" stays now that the
   figure is 210 (proposed: it stays).
2. **C6.1's intended verse.** "Is 52:1", on MAM's evidence; or Ben checks Yeivin's printed text first,
   and if ITM itself prints "2K 52:1", the adaptation gains a footnote saying so instead.
3. **C15.15's strand names.** Keep the romanized names in the claim data and scope `hebrew-prose`'s
   rule to the printed-Decalogue pages, as its own reference already does; or change the claim data to
   Hebrew letters.
4. **C4.4, `MAM-with-doc/LICENSE.md`.** Add an exception for the 112 third-party crops and the four
   Taamey D copies, as `MAM-OSIS/LICENSE.md` has one; or leave Ben's approved sentence of 2026-09-30
   as it stands.
5. **C4.5, which modules count as adaptation.** Declare the six rendering-helper modules GPL-3.0 code
   and narrow the exclusion (documents only); or move them out of `content/`; or state that the
   exclusion covers them with no code licence.
6. **C11, what the pipeline graph depicts.** The core pipeline that the root README names, marked and
   linted; or every mega step; or retire the graph. The floor fix applies under the first two.
7. **C1's gate design.** For the Yeivin claims: pin the fractions and the claim population (Gate B);
   or keep the whole-file pin with a review on every text refresh (Gate A); or pin the fractions only
   (Gate C). For the Phonetic MAM display oracle: freeze each chapter while its input is unchanged
   (Oracle A); or a Hebrew differential against MAM-simple (Oracle B); or move the oracle out of the
   suite (Oracle C).
8. **C6.2, the Yeivin migration gate.** Retire the byte-level gate and keep the published fragment ids
   (option C); or retire it outright (option A); or keep it and record each approved edit (option B).
9. **C8, the change log in the dependent refresh.** Step 4 holds the change-log paths back for step 5;
   or step 5 accepts a log that step 4 committed, confirmed from history.
10. **C12.4, nested stress helpers.** Close the dispatch and decline nested helpers explicitly; or
    close it and index them under a named per-container policy. Neither changes today's survey.
11. **C15.25, "Five issue trackers".** Keep the name and add a paragraph about the two routed
    trackers; or rename the section "Seven issue trackers", with two conforming edits.
12. **C15.29, the two Holman research records.** They are receipts: record `cb5bcda1`'s edits in new
    update files; or they are maintained records: reclassify them and amend `hebrew-prose`.
13. **C15.31, the private trope links.** Replace each with `trope#NN (private tracker)`, which also
    asks Ben to confirm that trope is private; or delete the references; or keep the URLs, marked
    private (not recommended).

## Published pages and distributed data (high risk)

These change what readers of the published site see or what consumers of the distributed products
receive, first in the order of `doc/periodic-review.md`'s "Present remediation by public-facing risk".
Each item gives the current and the proposed wording or behaviour. Copy any Hebrew from its source
byte for byte, never normalized, and wrap lines so that none begins with Hebrew.

### C2, the one-chanted-word oleh-weyored (question 1)

**The defect.** `classify` in `py/accgram/meteg_before_stress.py` sets the accent class at `:94`,
`conjunctive = facts.primary_accent in ha.CONJUNCTIVES_BCC[facts.cantillation_system]`. In a poetic
verse whose chanted word has both the oleh (U+05AB) and the yored of oleh-weyored, the closed stress
table (`py/phonetic_mam/core/bccvecs_that_are_known.py:160`, `:172`, `:196`: the shapes (oleh, yored),
(atnax hafukh, oleh, yored) and (merkha, oleh, yored)) makes the yored's U+05A5 the primary accent,
and the poetic conjunctive list holds U+05A5 as merkha (`py/mb_cmn/hebrew_accents.py:140`, "MER,  #
but as yored (always in oleh-we-yored) is disjunctive"). An in-memory rebuild reproduces all 6,119
tracked records; the fix below changes exactly 13, all in poetic verses of Psalms (4:5, 37:40,
39:13, 50:3, 120:1, 121:1, 123:1, 125:1, 126:1, 128:1, 129:1, 132:1 and 134:1; 12 FR3 and 1 FR1),
which accgram's poetic scanner reads as `OLEH_WEYORED`, and exactly 11 of the 20 pinned fractions.
No record is misclassified the other way.

**The fix** (code, lower risk in itself):
- `ChantedWordFacts` gains `accent_vector`, `primary_index` and `previous_accent_vector`;
  `facts_from_reading(reading, bcvt, previous=None)` fills them, and `analyze_books` passes each
  reading's predecessor in its own qamats sequence through a helper `_previous_readings(verse)`, keyed
  by identity, since one verse can display the same chanted word twice.
- `:94` and `:104` give way to `"accent_class": _accent_class(facts)`:

  ```python
  _POETIC = cantsys.get_cantsys_from_is_poetcant(True)


  def _accent_class(facts: ChantedWordFacts) -> str:
      """Conjunctive or disjunctive, with the yored of oleh-weyored named explicitly.

      In a poetic verse U+05A5 is merkha, a conjunctive, unless it is the yored of
      oleh-weyored, which is disjunctive. The yored is identified when U+05A5 is the
      last and primary accent of the chanted word's accent vector and U+05AB, the oleh,
      comes before it there: the stress table's (oleh, yored), (atnax hafukh, oleh,
      yored) and (merkha, oleh, yored). A primary U+05A5 after an unpaired oleh on the
      previous chanted word is refused rather than classified.
      """
      vector = facts.accent_vector
      if facts.cantillation_system == _POETIC and facts.primary_accent == ha.MER:
          if facts.primary_index == len(vector) - 1 and ha.OLE in vector[:-1]:
              return "disj"
          previous = facts.previous_accent_vector
          if ha.OLE in previous and ha.MER not in previous[previous.index(ha.OLE) :]:
              raise ValueError(
                  "A poetic U+05A5 after an oleh on the previous chanted word needs an"
                  " oleh-weyored analysis"
              )
      if facts.primary_accent in ha.CONJUNCTIVES_BCC[facts.cantillation_system]:
          return "conj"
      return "disj"
  ```

  and `analyze_books` re-raises the refusal with the verse and chanted word.
- U+05A5 stays in the poetic conjunctive list, where an ordinary merkha belongs, and the scanner's
  tokens are not substituted wholesale.
- A yored whose oleh is on the previous chanted word is **refused, not handled**: there are 17 such
  in MAM (Psalms 4:7, 8:3, 14:4, 18:44, 28:3, 37:7, 44:4, 53:5, 53:6, 56:9, 118:27, 142:7; Proverbs
  8:34, 24:12, 30:16; Job 3:6, 32:2), none a candidate of the survey, so a handling branch would be
  code no record checks; a refusal fails loudly; and `py/accgram/post_stress_meteg_classification.py:61–63`
  and `:81–88` already refuse both oleh-weyored shapes. A scratch check, not committed: the refusal
  predicate, run over all poetic readings without the candidacy filter, matches exactly those 17.

**What regenerating changes** (outputs to be read line by line):
1. `out/accgram/meteg-before-stress.json`, an 82-line diff: the 13 `"accent_class"` lines; in
   `reshaped_counts`, FR1 `cwg` 81 to 80 and `dwg` 418 to 419, and FR3 `cwg` 41 to 31, `csg` 581 to
   579, `dwg` 1015 to 1025 and `dsg` 77 to 79; and Psalms 4:5 and 50:3 joining
   `selections.fully_regular_disjunctive_without_target_meteg`, 132 to 134. Nothing else.
2. `py/yeivin_itm/claim_schema.py`: `APPROVED_INPUT_SHA256` (`:11–13`) takes the regenerated survey's
   SHA-256, read from the file, and these 11 pins change; the other nine stay.

   | Pin | Current | Corrected |
   |---|---|---|
   | `fully-regular.disjunctive-without-target-meteg` | 132/3583 | 134/3583 |
   | `fully-regular.conjunctive-with-target-meteg` | 221/3583 | 210/3583 |
   | `fully-regular.exceptions` | 353/3583 (9.85%) | 344/3583 (9.60%) |
   | `…disjunctive-without-target-meteg.other-meteg` | 31/132 | 33/134 |
   | `…qadma-or-metigah` | 6/132 | 6/134 |
   | `…merkha` | 3/132 | 3/134 |
   | `…metigah` | 6/132 | 6/134 |
   | `…merkha-with-azla-legarmeh` | 2/132 | 2/134 |
   | `FR1.conjunctive-with-target-meteg` | 81/284 (28.52%) | 80/283 (28.27%) |
   | `FR3.conjunctive-with-target-meteg` | 41/622 (6.59%) | 31/610 (5.08%) |
   | `fully-regular.disjunctive-exception-rate` | 132/2184 (6.04%) | 134/2197 (6.10%) |
3. `Yeivin-ITM/meteg-claims.json`, distributed data: line 5 (`input.sha256`) and the numerator,
   denominator and percentage lines of those 11 measurements; definitions and exclusions unchanged.
4. Three published pages, figures only, which the corrected prose below lists.
5. `in/yeivin_itm_legacy_differential.json`'s change records, while a test still reads them (today's
   gate, or question 8's option B).

The numbers reach the pages only through the `claim_text` placeholders of the two footnote modules
(`py/yeivin_itm/content/my_yeivin_amisc_sec_320_footnotes.py`, `..._sec_322_footnotes.py`), resolved by
`claim_text.resolve` before line wrapping and rounded once from each fraction
(`py/yeivin_itm/claim_text.py:26–50`); those two modules are excluded from the module pins, so no
source module changes and no module hash breaks. Every new figure has the same width as the old, so
the wrapping is unchanged.

**The corrected prose, approved by Ben on 2026-10-03 (question 1).** The proposal changes figures
only; every qualitative sentence stays true ("agrees almost exactly with this estimate of 90%": 90.4%
follow the rule; "far more than could be called a few dozen": 134; "in two cases": unchanged).
1. `gh-pages/yeivin-itm/yeivin_itm-318_344.html:539–540`, footnote φ1 of §320. Current: "I find 3,583
   fully regular words, of which 353 (9.9%) are exceptions to the rule, breaking down as follows:"
   Corrected: "… of which 344 (9.6%) are exceptions …"
2. `:541`. Current: "132 disjunctives without the expected gaʿya." Corrected: "134 disjunctives …"
3. `:542`. Current: "221 conjunctives with the expected gaʿya of a disjunctive." Corrected: "210
   conjunctives …"
4. `:551–552`, φ3. Current: "My research agrees, roughly, with this estimate of 200. I find 221
   conjunctives with the expected gaʿya of a disjunctive." Corrected: "… I find 210 conjunctives …".
   Whether "roughly" should stay now that the figure is 210 is Ben's to say; the proposal keeps it.
5. `:552–557`. Current: "I find about 29% of FR1 conjunctives to have this gaʿya, about 20% of FR2
   conjunctives to have it, and only about 7% of FR3 conjunctives to have it." Corrected: "I find
   about 28% of FR1 conjunctives … and only about 5% of FR3 conjunctives to have it." (The FR1
   figure returns to the legacy page's "about 28%".)
6. `gh-pages/yeivin-itm/yeivin_itm-huge-ftnt-320.html:13–14`. Current: "I find 132 disjunctives without
   the expected gaʿya." Corrected: "I find 134 disjunctives …"
7. `:70–72`. Current: "I find that 31 of the 132 disjunctives without the expected gaʿya nonetheless
   have a gaʿya elsewhere." Corrected: "I find that 33 of the 134 disjunctives …"
8. `:84–86`. Current: "I find that 6 of the 132 disjunctives without the expected gaʿya nonetheless
   have a metigah where we would expect a gaʿya." Corrected: "I find that 6 of the 134 disjunctives …"
9. `gh-pages/yeivin-itm/yeivin_itm-huge-ftnt-322.html:36–39`. Current: "While I find that about 6% of
   FR disjunctives (132 out of 2184) lack the expected gaʿya, …" Corrected: "… (134 out of 2197) …"

The changed lines are 539, 541, 542, 552, 553 and 556 of the first page, 13, 70, 71 and 84 of the
second, and 36 of the third; no other page changes. (The update's "to 557" includes `:557`,
"have it.</p>", the end of the FR3 sentence, which itself does not change.) In `Yeivin-ITM/README.md`,
`:75–76` becomes "Ben approved correction of his added claims and their explanatory prose on
2026-10-01, and the 11 fractions that the oleh-weyored correction changed on <date>.", and under
question 8's option B, `:86–87`'s "The original page hashes and correction ranges remain unchanged."
becomes "The original page hashes are unchanged; the correction ranges record the corrections Ben
approved on 2026-10-01 and <date>."

**Order.** (1) The fix and C12.2's checks and docstring in one commit; C12.2's scanner differential
then fails against the old survey with exactly the 13 undeclared `OLEH_WEYORED` disagreements. (2)
Regenerate the survey with `./.venv/Scripts/python.exe py/main_accgram.py survey-meteg-before-stress`;
`py/tests/test_meteg_before_stress.py` passes, and the Yeivin steps raise at the pins. (3) With
Ben's approval (question 1), set the pins, then run `./.venv/Scripts/python.exe py/main_yeivin_itm.py survey-meteg-claims`
and `./.venv/Scripts/python.exe py/main_yeivin_itm.py render`. (4) While a test still reads
`in/yeivin_itm_legacy_differential.json` (today's gate, or question 8's option B), rewrite C2's
change records there, as an in-memory replay showed they must be: in `yeivin_itm-318_344.html`'s, the
records at `new_start` 537 and 539 take the new lines, the record at 550 shrinks to its one line
"find 210 conjunctives …", because the FR1 line now equals the legacy text, a record at 554 is added
for "only about 5% …", and 986 and 994 stay; in `yeivin_itm-huge-ftnt-320.html`'s, the record at 11
takes the new line, the one-line record at 69 becomes a two-line record at 68 that adds the "31" to
"33" line, and the record at 82 takes the new line; in `yeivin_itm-huge-ftnt-322.html`'s, the record at
34 takes "(134 out of 2197)", and 40, 45 and 65 stay. Every page must still reconstruct its
`old_sha256`. Under options A and C nothing reads the records, and nothing is rewritten. (5)
`./.venv/Scripts/python.exe py/main_yeivin_itm.py check` and
`py/main_test.py py/tests/test_meteg_before_stress.py py/tests/test_yeivin_itm.py`. The other 14
Yeivin pages, every Phonetic MAM output and `out/accgram/post-stress-meteg.json` stay byte for byte.
Today's gate does not block C2 beyond step 4's records: the pages are already in its hard-coded
set, no Hebrew example changes, and no pinned module is edited.

### Other published pages

**C6.1, `gh-pages/yeivin-itm/yeivin_itm-207_285.html`, the citation "2K 52:1" (question 2).** 2 Kings
has 25 chapters. The page cites it at `:39`, as the tooltip of an example form in §239's list Is 19:19,
2K 10:30, 2K 52:1 and Ho 2:5, and at `:82`, in "Biblical references in this section:". The source is
`py/yeivin_itm/content/my_yeivin_sec_239.py:8`, a `hlp.hboloc(...)` call whose second argument is
`"@2K 52:1"`.
Of the 17 pages' 715 distinct references (717 counting two found only in visible text), checked
against the verse lists of MAM-simple's three versifications, it is the only one that names no verse.
MAM's evidence for the intent: of MAM's 25 atoms whose letters spell ירושלם and that carry pashta,
only Isaiah 52:1's is numbered 52:1 (MAM's atom there has the pashta with its stress helper, where
the adaptation's form has the pashta alone). Yeivin's printed text, which only private OCR holds, was
not read. Ben confirms the verse:
1. **Option 1 (recommended): "Is 52:1".** In the source, the substring `"@2K 52:1"` becomes
   `"@Is 52:1"`; the Hebrew argument stays byte for byte. Regenerating changes exactly two lines of
   the page: `:39` becomes `<bdi lang="hbo" data-bk-ch-vr="@Is 52:1" title="Is 52:1">…</bdi>, and`
   and `:82` becomes `<bdi lang="hbo" data-bk-ch-vr="@Is 52:1" title="Is 52:1">…</bdi> <bdi>Is 52:1</bdi>,`,
   the Hebrew unchanged.
2. **Option 2: Ben first checks ITM.** If ITM itself prints "2K 52:1", the adaptation's precedent for
   a locale it corrects is a footnote naming ITM's locale (`my_yeivin_sec_390.py:12–20`,
   `my_yeivin_sec_392.py:17–25`): after the `hboloc` element add
   `sub.footnote(["Here $itm gives locale 2K 52:1 for ", hlp.hbo(<the same form>), ", but 2 Kings has only 25 chapters. I use Is 52:1, where MAM has this atom."])`,
   which adds the ids `sec-239-callout-1` and `sec-239-ftnt-1`.
- With either, a new lint in `py/tests/test_yeivin_itm.py`,
  `test_every_biblical_reference_names_an_existing_verse`: every `data-bk-ch-vr` and
  `data-bk-ch-vr-2` value on the 17 tracked pages, and every string literal fully matching
  `@\S+ \d+:\d+` under `py/yeivin_itm/`, mapped from Yeivin's book id to OSIS through
  `YBKID_AND_STD_BKID_PAIRS` (`my_yeivin_amisc_helpers_for_locales.py:43–83`) and `BOOK_ABBREVS`
  (`py/mb_misc/osis_book_abbrevs.py:57–97`), must name a verse `osisID` in one of
  `MAM-simple/json-vtrad-mam`, `json-vtrad-bhs` and `json-vtrad-sef`; no input files, fewer than
  23,000 verses or fewer than 700 references fail. It fails today only on "@2K 52:1". It proves that
  a verse exists, not that it holds the form. A range check inside the parser
  (`my_yeivin_amisc_helpers_for_locales.py:27–40`) is not proposed: it would put a versification
  table in a hash-pinned content module and rest on `assert`.
- Depends on question 8 (C6.2): today's tests forbid this edit.
- Verification: `./.venv/Scripts/python.exe py/main_yeivin_itm.py render`, then
  `git diff -- gh-pages/yeivin-itm` shows the two lines and nothing else;
  `./.venv/Scripts/python.exe py/main_yeivin_itm.py check`; `py/main_test.py py/tests/test_yeivin_itm.py`.

**C13.2, the Ashkenazic display depends on `:has()` alone.** `py/phonetic_mam/assets/style.css:37–41`,
published as `gh-pages/phonetic-mam/style.css`, switches the transcriptions only through
`body:has(#pronunciation-ashkenazic:checked)`, and `pronunciation.js` sets the radio buttons, the URL
and the links but no class (`:8–22`). A browser without `:has()` shows Sephardic transcriptions under
an Ashkenazic label, including at `?pronunciation=ashkenazic`, where redirected legacy Ashkenazic URLs
land.
- Fix, in `style.css`, `:37–41` become:

  ```css
  .pronunciation-ashkenazic, .column-ashkenazic-only { display: none; }
  /* pronunciation.js keeps body.ashkenazic-selected in step with the radio group, for a
     browser without :has(). Its rules stay apart from the :has() rules, because a browser
     that does not know :has() drops every rule whose selector list holds it. */
  body.ashkenazic-selected .pronunciation-sephardic,
  body.ashkenazic-selected .column-sephardic-only { display: none; }
  body.ashkenazic-selected .pronunciation-ashkenazic { display: inline; }
  body.ashkenazic-selected .column-ashkenazic-only { display: table-cell; }
  body:has(#pronunciation-ashkenazic:checked) .pronunciation-sephardic,
  body:has(#pronunciation-ashkenazic:checked) .column-sephardic-only { display: none; }
  body:has(#pronunciation-ashkenazic:checked) .pronunciation-ashkenazic { display: inline; }
  body:has(#pronunciation-ashkenazic:checked) .column-ashkenazic-only { display: table-cell; }
  ```

  and in `pronunciation.js`'s `select`, after the radio loop (`:11`) and before `if (replaceURL)`:

  ```js
          // style.css's fallback for a browser without :has().
          document.body.classList.toggle("ashkenazic-selected", pronunciation === "ashkenazic");
  ```

  The `:has()` rules stay for a browser without JavaScript; a browser with neither still cannot
  switch, which would need the noscript sentence and all 969 page bodies changed, and is not proposed.
- Generated effects: `./.venv/Scripts/python.exe py/main_phonetic_mam.py render` rewrites exactly
  `gh-pages/phonetic-mam/style.css` and `gh-pages/phonetic-mam/pronunciation.js`; no HTML page changes.
  Nothing hashes or compares these assets: C1.2's oracle projects only each chapter's `body/main`.
- Verification: after `render`, `git status --porcelain` lists exactly the two sources and their two
  published copies; `py/main_test.py py/tests/test_phonetic_display_release.py`. No admissible test
  runs a browser, so once, as a scratch check with the in-app browser's live DOM: copy
  `gh-pages/phonetic-mam/tnkh/A1-Genesis/01.html` into a scratch `site/tnkh/A1-Genesis/`, the new
  `pronunciation.js` into `site/`, and the new `style.css` into `site/` with its four `body:has(`
  rules removed; open `.../site/tnkh/A1-Genesis/01.html?pronunciation=ashkenazic`; require
  `document.body.classList.contains("ashkenazic-selected")`, a computed `display` of `inline` for a
  `.pronunciation-ashkenazic` span and `none` for its Sephardic sibling; switch twice and repeat; and
  with the old `pronunciation.js`, see the defect.

**C15.8, the English attribution link on two index pages.** The MAM statement prescribes, for
"Attribution in English and all languages other than Hebrew", a link to
`https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning`
(`MAM-simple/LICENSE.md:18–22`, the same in every product licence). The English page
`gh-pages/phonetic-mam/index.html:30–33` links "Hebrew Wikisource" to the he.wikisource page of MAM
instead, from `py/phonetic_mam/renderer.py`'s `_SOURCE_URL` (`:17–21`, used once, at `:50`); the
older `gh-pages/MAM-with-doc/index.html:11–14`, which the update notes has the same link, gets it
from `py/mwd/mwd_write_index_dot_html.py:41` (`ws_urls.HEBREW`). `ws_urls.HEBREW` also serves as
Sefaria's "Version Source" and is pinned by `py/tests/test_ws_urls_encoding.py:13`, so it stays.
- Fix: a new module `py/mb_misc/mam_attribution.py`:

  ```python
  """The attribution link that the MAM statement prescribes outside Hebrew.

  DATA-LICENSES.md, "The MAM statement, repeated verbatim", prescribes for attribution
  in English and every language other than Hebrew a direct link to this page.
  """

  ENGLISH_ATTRIBUTION_URL = (
      "https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning"
  )
  ```

  `mwd_write_index_dot_html.py:41` uses `mam_attribution.ENGLISH_ATTRIBUTION_URL` in place of
  `ws_urls.HEBREW`; in `renderer.py`, `_SOURCE_URL` goes and `:50` uses the same constant. The anchor
  text stays "Hebrew Wikisource". The constant is not added to `py/mb_misc/ws_urls.py`, because
  `py/mb_sefaria/sef_header.py` imports that module, so editing it would change the code of the
  hand-run `py/main_mam4sef.py` and oblige rerunning it.
- Generated effects: each index page changes on one line, the `<a href=...>Hebrew` line
  (`gh-pages/phonetic-mam/index.html:32` and `gh-pages/MAM-with-doc/index.html:13`), to
  `<a href="https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning">Hebrew`;
  the other 973 Phonetic MAM pages, every other MAM-with-doc page and MAM-for-Sefaria stay byte for
  byte. C1.2's oracle reads only the chapter pages (`projection_check.verify_site`, `:131–142`).
- Verification: `./.venv/Scripts/python.exe py/main_phonetic_mam.py render` and
  `./.venv/Scripts/python.exe py/main_mam_with_doc.py`, then `git diff --stat` shows the two pages
  with one line each and the three source files; `py/main_test.py py/tests/test_phonetic_display_release.py py/tests/test_ws_urls_encoding.py`.

### Distributed data

#### `Phonetic-MAM/README.md` (C5.1, C5.2, C15.7, with C1.2)

**C5.1 and C5.2, how the Hebrew differs from MAM's text.** The README says the product "contains
generic MAM Hebrew" (`:3–5`) and nothing about spelling. "Generic" is the codebase's term
(`py/phonetic_mam/core/distinguished.py:40–41`, `to_generic_points`, which replaces U+05C8 with U+05B0
and U+05C9 with U+05BC). Recounted in memory: under the generic perpetual-qere rule
(`qere_from_implicit_kq.get_qere_from_implicit_kq`), 7,711 of MAM-simple's chanted words change, and at
7,710 the release has only the qere (the four the review's join key missed are gray-maqaf compounds at
Psalms 18:1, 98:9 and 106:48 and Proverbs 30:9); the 7,711th is Deuteronomy 32:6's, which the release
folds with the preceding atom. Of the 2,305 top-level stress-helper templates the release has the
second parameter alone at 2,056, both forms at 81 (where the first is a substring of the second), and
the perpetual qere at 168. The release holds no U+05C4 or U+05C5, 671 U+FB1E (varika), 385,991 U+0301
and 73,384 U+0306. Insert after `:14`, before "## Commands":

> ## How the Hebrew differs from MAM's text
>
> The Hebrew here is generic, this repository's term for Hebrew without the phonetic
> computation's annotations. It has neither U+05C8, which marks a vocal shewa, nor
> U+05C9, which marks a dagesh ḥazaq, nor either retired annotation pair, U+05B0 U+05AF
> or U+05BC U+05C4: a shewa here is U+05B0 and a dagesh U+05BC. Generic Hebrew is still
> not MAM's text as `MAM-simple/` has it, and a consumer joining this release to MAM
> must allow for these differences:
>
> 1. **Perpetual qere.** Where MAM has a perpetual qere, such as the Tetragrammaton,
>    this release has only the qere, in the form that
>    `py/phonetic_mam/core/qere_from_implicit_kq.py` derives from MAM's spelling; that
>    module's docstring lists the kinds. At Genesis 2:4, for example, `MAM-simple/`
>    has יְהֹוָ֥ה and this release has אֲדֹנָ֥י. This release has the qere in place of
>    MAM's spelling at 7,710 of MAM's chanted words. One more is at Deuteronomy 32:6,
>    where MAM has two chanted words, הַ with a large he and לְיְהֹוָה֙, and this
>    release has one form for both, הַלְאֲדֹנָי֙.
> 2. **Extraordinary points.** This release has none of MAM's extraordinary points,
>    the upper dot U+05C4 and the lower dot U+05C5. The release validator,
>    `py/phonetic_mam/display_schema.py`, refuses both.
> 3. **Stress helpers.** MAM's two stress-helper templates, `מ:דחי` and `מ:צינור`,
>    give a chanted word in two forms, the second with the accent's stress helper.
>    `MAM-simple/` has the first form and this release the second. At Psalms 2:6,
>    for example, `MAM-simple/` has וַ֭אֲנִי and this release has וַ֭אֲנִ֭י.
> 4. **Varika.** This release keeps MAM's varika, U+FB1E, which `MAM-simple/` lacks.
> 5. **2 Kings 22:1.** MAM's qamats template, `מ:קמץ`, gives the verse's last chanted
>    word two alternatives, {{2KI-D}} for its ד parameter and {{2KI-S}} for its ס
>    parameter. This release has only the second, as {{2KI-REL}}, without the
>    labels קמץ-ד and קמץ-ס that it has at each of the other 356 verses where MAM has
>    that template. Until the Wikisource refresh of 2026-09-27, this repository's copy
>    of MAM had only the form this release has.
> 6. **2 Chronicles 25:17.** MAM has the ketiv לך and the qere לְכָ֖ה. This release
>    has לְךָ֖, with the ketiv's final kaf and the qere's points. MAM's note there
>    reports that the Aleppo Codex has לְךָ֖ with no qere note, so this release has
>    the form that MAM's note attributes to that manuscript. That is MAM's report;
>    the manuscript itself has not been checked.
>
> The transcriptions have each acute or breve vowel decomposed, as a base letter
> followed by U+0301 or U+0306, while their ḥ is the precomposed U+1E25. Elsewhere the
> repository keeps Latin letters with diacritics in NFC; these are the bytes of the
> previously published pages, which Ben's decision of 2026-10-03, recorded in
> `doc/review-findings-2026-10-02-update.md`, keeps.

The executor lifts every Hebrew form from its source rather than from this plan, and runs the
mark-order lint on the README. The forms, with their sources: `{{2KI-D}}` is parameter ד of the
qamats template `מ:קמץ` at 2 Kings 22:1 in `MAM-parsed/plus/BC-Kings.json` (U+05DE 05B4 05D1 05BC
05C7 05BD 05E6 05B0 05E7 05B7 05BD 05EA); `{{2KI-S}}` is its parameter ס (the same with U+05B8 for U+05C7);
`{{2KI-REL}}` is the verse's last Hebrew cell in `Phonetic-MAM/data/BD-2Kings.json`, `{{2KI-S}}` and
U+05C3; the Genesis 2:4 and Deuteronomy 32:6 forms come from `MAM-simple/json-vtrad-mam` and
`Phonetic-MAM/data/A1-Genesis.json` and `A5-Deuter.json`, and the Psalms 2:6 forms from parameters 1
and 2 of that verse's `מ:דחי` template. Item 2's last sentence depends on the U+05C5 guard below.

**C5.1's guard (a latent defect).** The guards refuse U+05C4, a retired annotation carrier, but not
U+05C5 (`py/phonetic_mam/display_schema.py:27`, the schema's text pattern at
`Phonetic-MAM/schema/phonetic-mam-public-v1.schema.json:90`, and
`py/py_html/forbidden_phonetic_marks.py:17–19`), so an export could carry one extraordinary point and
not the other. Fix: `display_schema.py:27` becomes, with its comment, "# The computation's annotation
points, the retired carriers U+05AF and U+05C4, and / # U+05C5: the release has neither extraordinary
point (Phonetic-MAM/README.md)." and
`_FORBIDDEN = frozenset(map(chr, (0x05AF, 0x05C4, 0x05C5, 0x05C8, 0x05C9)))`; the schema pattern
becomes `"^[^<>\\u05af\\u05c4\\u05c5\\u05c8\\u05c9]+$"`; `forbidden_phonetic_marks.py`'s set gains
`hpu.LODOT` (U+05C5, `py/mb_cmn/hebrew_punctuation.py:8`) and its docstring says "It refuses U+05C5
as well, so that neither extraordinary point passes through these generators unnoticed: a genuine
source dot requires an independently validated path."; and a lint in
`test_no_public_record_quality_layer` (`py/tests/test_phonetic_display_release.py`, after `:73–74`)
requires the schema's pattern to equal `f"^[^<>{forbidden}]+$"` built from `display_schema._FORBIDDEN`.
No U+05C5 occurs in `Phonetic-MAM/`, the 974 Phonetic MAM pages or the 17 Yeivin pages, so every
output stays byte for byte; the guard reaches mega steps, so the final mega covers it.

**C5.2, the schema's description.** `Phonetic-MAM/schema/phonetic-mam-public-v1.schema.json:5`'s
"description" gains, after its first sentence: "README.md, \"How the Hebrew differs from MAM's
text\", defines generic Hebrew and lists how it differs from MAM's text." The data stays as it is:
changing it would need the private adapter and would act on the September 29 round's finding 22,
which Ben deferred. That finding's live record,
`doc/dual-agent-review-2026-09-29-turn-01-claude-update.md`, "Deferred refresh finding 22: current
target ownership, 2026-10-02", tells the next refresh to check `Phonetic-MAM/data/BD-2Kings.json`; it
gains a dated entry, after the README text lands:

> ## Deferred refresh finding 22: evidence from the 2026-10-02 review, <YYYY-MM-DD>
>
> Recorded on <YYYY-MM-DD> by <agent, model and session>, executing item C5.2 of
> `doc/PLAN-remediate-review-findings-2026-10-02.md`. Finding 22 remains deferred; this
> entry adds a pointer and resolves nothing.
>
> The 2026-10-02 review checked the public release that the entry above names
> (`doc/review-findings-2026-10-02.md`, finding 5.2). `Phonetic-MAM/data/BD-2Kings.json`
> lacks MAM's qamats alternative at 2 Kings 22:1, and 2 Kings 22:1 is the only one of
> the 357 verses with a `מ:קמץ` template whose display has no qamats-labelled forms; the
> owner's verification re-derived both (`doc/review-findings-2026-10-02-update.md`,
> C5.2). The review also reported that its mega re-exported the release from the current
> MAM-parsed without a byte of difference, so a refresh alone would not bring the
> variant in; that report rests on the private adapter, and the owner did not re-derive
> it. `Phonetic-MAM/README.md`, "How the Hebrew differs from MAM's text", now discloses
> the difference.

If this remediation's own mega re-exports the release and leaves `BD-2Kings.json` unchanged, the
entry adds: "This remediation's mega re-exported the release at `<commit>` and left
`Phonetic-MAM/data/BD-2Kings.json` unchanged, which re-derives that report."

**C15.7, `:21`.** Current: "- `render` reads only this public product and writes `gh-pages/phonetic-mam/`".
Proposed: "- `render` reads this public product, its stylesheet and script in
`py/phonetic_mam/assets/`, the five example images in `in/phonetic-mam-images/`, and the Taamey D
font in `doc/woff2/` with its source support in `in/font-support/`; it writes `gh-pages/phonetic-mam/`
and the shared font-source package in `gh-pages/font-sources/`". `:27`, "All rendering and ordinary
public analyses run without MAM-private.", stays true.

Verification for this README: `git diff --check`;
`py/main_test.py py/tests/test_phonetic_display_release.py py/tests/test_prose_mark_order.py py/tests/test_h_dot_below_nfc.py py/tests/test_yeivin_itm.py`;
`./.venv/Scripts/python.exe py/main_phonetic_mam.py check`; `./.venv/Scripts/python.exe py/main_yeivin_itm.py check`.

#### `Yeivin-ITM/README.md` and the claim schema (C15.14, C15.16)

C2's, C4.5's, C4.6's, C6.2's and C1.1's sentences in the same README are under those items.

**C15.16, two stale Yeivin descriptions.** `Yeivin-ITM/README.md:88–89`, "This records branch output,
not a claim that Pages has been deployed.", is deleted (every option of question 8 rewrites `:81–89`
anyway); no deployment claim replaces it. `in/yeivin_itm_legacy_differential.json:5`'s description,
"Every old page is recovered byte-for-byte by reversing only the listed font-source link or
Ben-approved claim corrections. Other adaptation modules remain byte-identical.", omits that the
favicon line is removed first; it becomes "Every old page is recovered byte-for-byte by removing the
shared favicon line from its head and then reversing only the listed font-source link or Ben-approved
claim corrections. Other adaptation modules remain byte-identical.", and under question 8's options A
and C gains "Frozen record: this held for the pages and modules as of `<the parent of the commit that
retires the gate>`, and no test reads it now." Keep the key order and the two-space indent.

**C15.14, `Yeivin-ITM/schema/meteg-claims-v1.schema.json:3`.** The schema's `$id` is
`https://bdenckla.github.io/MAM-basics/Yeivin-ITM/schema/meteg-claims-v1.schema.json`, a URL that Pages
does not serve, since it publishes only `gh-pages/` (`.github/workflows/pages.yml:35`). JSON Schema
does not require an `$id` to resolve, nothing else references it, and changing it would change the
schema's identity, so the `$id` stays. In `Yeivin-ITM/README.md`, after "`meteg-claims.json` follows
the closed schema in `schema/meteg-claims-v1.schema.json`." (`:67–68`), insert: "The schema's `$id`,
`https://bdenckla.github.io/MAM-basics/Yeivin-ITM/schema/meteg-claims-v1.schema.json`, identifies the
schema; it is not where the schema is served, since Pages publishes only `gh-pages/`. Read the schema
from this directory."

#### The Yeivin claim data's strand names (C15.15, question 3)

**C15.15, romanized strand names in the Yeivin claim data (question 3).** Each of the 20 claims of
`Yeivin-ITM/meteg-claims.json` has the exclusion "The bet cantillation strand is excluded; the alef
strand is counted once.", from `py/yeivin_itm/claims.py:102`; the schema constrains it only as a string
and no page renders it. `hebrew-prose`'s `SKILL.md` item 7 says "Keep strand names in Hebrew letters in
reader-facing prose." generally, while its `references/rendered-prose.md` (`:9–14`) and the SCOPE
paragraph of `py/accgram/printed_decalogue_strands.py` (`:25–31`) make "strand names in Hebrew letters"
a rule of the printed-Decalogue pages only; the published methods page
`gh-pages/post-stress-meteg-methods.html` already writes `cant-alef` and `cant-bet` romanized, as do
MAM-simple's own element names (`<cant-alef>`, `<cant-bet>`). Ben's call:
1. **Option 1 (recommended): keep the romanized names; scope the skill's rule as its reference
   does.** In `dot-claude/skills/hebrew-prose/SKILL.md`, item 7's "Keep strand names in Hebrew letters
   in reader-facing prose." becomes "On the printed-Decalogue pages, keep the strand
   names תחתון and עליון in Hebrew letters in reader-facing prose; `references/rendered-prose.md` gives that rule's
   scope and its exempt registers. Elsewhere, keep the strand names a page or data product already
   uses, such as MAM-simple's `cant-alef` and `cant-bet` strands.", wrapped so that no line begins
   with Hebrew. No file under `Yeivin-ITM/` changes; the skill takes effect when deployed (A3).
2. **Option 2: Hebrew letters in the claim data.** `claims.py:102` becomes
   `"The ב cantillation strand is excluded; the א strand is counted once."`; regenerating with
   `./.venv/Scripts/python.exe py/main_yeivin_itm.py survey-meteg-claims` changes those 20 lines of
   `Yeivin-ITM/meteg-claims.json` and no page, pin or input hash. The skill's general rule then leaves
   the methods page and the accgram pages that romanize strand names as unswept violations.

Recommendation, option 1: the reference and the SCOPE paragraph are the rule's homes of record and
both scope it to the trio; the claim strings are machine-facing data in MAM-simple's own vocabulary,
and option 2 changes distributed data for no reader-visible gain.

#### The two new product `LICENSE.md` files (C4.3)

**C4.3, the two new products' `LICENSE.md` files.** Each of the five older products holds a
`LICENSE.md` repeating the MAM statement after a short preface; `Phonetic-MAM/` and `Yeivin-ITM/`
have none, and `DATA-LICENSES.md` gives no row to their READMEs, their `schema/` directories or the
six notice files beside their fonts. Proposed:

1. **New `Phonetic-MAM/LICENSE.md`**: these six lines, then a byte-for-byte copy of
   `MAM-simple/LICENSE.md:5–35` (the blank line and the statement from `----` to the end). The
   preface uses the words of `DATA-LICENSES.md:53`, the row for `Phonetic-MAM/data/`; copy its Hebrew
   from `MAM-simple/LICENSE.md:4`.

   ```
   The statement below is preserved verbatim from the former MAM Google spreadsheet,
   which became a frozen historical archive on September 12, 2026.
   This statement applies equally to the MAM text and its derivative display in `data/`.
   `DATA-LICENSES.md` at the repository root records the terms of this directory's other files,
   and no new grant is made here over other source material. So, in the text below, ignore any
   references to "in this spreadsheet" (English) or שבגליון הנתונים הזה (Hebrew).
   ```
2. **New `Yeivin-ITM/LICENSE.md`**, which does not repeat the MAM statement, because the product
   holds no MAM text:

   ```
   This directory holds no MAM text, so this file does not repeat the MAM statement that the
   other product directories' `LICENSE.md` files carry. `DATA-LICENSES.md` at the repository
   root maps terms path by path; for this directory it records the following.

   - `meteg-claims.json`: "Ben Denckla's analysis; no new dedication or additional grant is made
     by this migration. This aggregate data product contains no additional transcription of
     Yeivin's works".
   - `README.md` and `schema/`: MAM-basics' own work, so GPL-3.0.

   The adaptation these claims serve is not in this directory. It is under
   `py/yeivin_itm/content/` and is rendered to `gh-pages/yeivin-itm/`. It is adapted, by
   permission, from Israel Yeivin, *Introduction to the Tiberian Masorah*, translated and edited
   by E. J. Revell, copyright © 1980 by the Society of Biblical Literature. `README.md`,
   "Permission and authorship", and `DATA-LICENSES.md` give its terms.
   ```

   The repository records no licence grant for `meteg-claims.json` (only `DATA-LICENSES.md:50` and
   `Yeivin-ITM/README.md:94–95`), so the file quotes the row and grants nothing. The README and
   schema rows apply the repository's declared GPL-3.0 for "MAM-basics' work in code and prose"
   (`DATA-LICENSES.md:5–7`), as the `hbce-psalms/README.md` row does (`:111`); striking that
   sentence leaves those two paths without stated terms.
3. **The closed file sets that would reject a new file change in the same commit:**
   `py/phonetic_mam/release.py:60–69` (`expected`) and `py/tests/test_phonetic_display_release.py:60–66`
   (`allowed`) gain `root / "LICENSE.md"`, and `py/yeivin_itm/claims.py:19` becomes
   `{"LICENSE.md", "README.md", "meteg-claims.json", "schema/meteg-claims-v1.schema.json"}`. Nothing
   else reads a closed set of either directory: the exporter writes only `data/` and `examples/`,
   and `py/accgram/meteg_before_stress.py:341–356` hashes `data/*.json` only, so C1's pins do not move.
4. **A recurrence lint:** in `py/tests/test_product_scopes.py`, assert that every `product_dirs()`
   entry has a tracked `LICENSE.md`.

Verification: `./.venv/Scripts/python.exe py/main_phonetic_mam.py check`,
`./.venv/Scripts/python.exe py/main_yeivin_itm.py check`, and
`py/main_test.py py/tests/test_phonetic_display_release.py py/tests/test_yeivin_itm.py py/tests/test_meteg_before_stress.py py/tests/test_product_scopes.py py/tests/test_prose_mark_order.py`;
the two render steps produce no diff. The `DATA-LICENSES.md` rows are under that file below.

## Reader-facing documents (high risk)

Markdown written for readers: the licence pages, the root README, the pipeline diagram it offers,
and a translation. Ordinary plans and records under `doc/` are under "Lower-risk changes".

### Reader-facing Markdown

#### `MAM-with-doc/LICENSE.md` (C4.4, question 4)

Current `:3–5`: "This statement applies equally to the MAM-with-doc edition, which MAM-basics
publishes from / `gh-pages/MAM-with-doc/`. So, in the text below, ignore any references to "in
this spreadsheet" / (English) or שבגליון הנתונים הזה (Hebrew)." Ben approved that sentence on
2026-09-30 (`doc/PLAN-remediate-review-findings-2026-09-29.md:186–187`; its wording at `:540–550`),
on the premise that `MAM-with-doc/` "holds only its README, its licence, `.gitattributes` and
`.gitignore`". The tree it names also holds 112 third-party crops under `misc/img/`, which
`DATA-LICENSES.md:97` keeps as "each rights holder's; no grant is made or implied here", and four
Taamey D copies (`woff2/`, `change-log/woff2/`, `foi/woff2/`, `misc/woff2/`), which `:96` excepts.
Any change is Ben's:

1. **Option 1 (recommended): an exception, as `MAM-OSIS/LICENSE.md`'s preface has one.** Replace
   `:3–5` with the following; its last line is the existing `:5`, Hebrew unchanged:

   ```
   This statement applies equally to the MAM-with-doc edition, which MAM-basics publishes from
   `gh-pages/MAM-with-doc/`, except the crops under its `misc/img/`, which remain each rights
   holder's, and the four copies of the Taamey D font in its `woff2/`, `change-log/woff2/`,
   `foi/woff2/` and `misc/woff2/`, which keep the font's GNU GPL version 2 terms with its
   font-embedding exception; `DATA-LICENSES.md` at the repository root records both. So, in the
   text below, ignore any references to "in this spreadsheet"
   (English) or שבגליון הנתונים הזה (Hebrew).
   ```

   and add to `DATA-LICENSES.md`'s paragraph before the statement (under C4.3's rewrite of it):
   "The preface in `MAM-with-doc/LICENSE.md` excepts the crops under
   `gh-pages/MAM-with-doc/misc/img/` and the four Taamey D copies below `gh-pages/MAM-with-doc/`,
   which keep the terms the table records for them."
2. **Option 2: no change.** `DATA-LICENSES.md:96–97`, to which `README.md:120–124` sends readers,
   already excepts both, and the sentence is Ben's approved wording.

Recommendation, option 1: read on its own, the licence file now covers 112 third-party crops and
four GPL font copies; the approved main clause is kept word for word, and the approval's premise
did not consider the published tree.

#### `README.md`, the repository root (C4.7, C4.8, with C4.5 and C11)

1. **C4.8, "Product and corpus directories" (`:21–36`).** The list names the five older products
   and none of the window's two. Insert after the `MAM-OSIS/` item (`:29`):

   > - [`Phonetic-MAM/`](Phonetic-MAM/README.md) — the Phonetic MAM display as JSON: MAM's displayed Hebrew with its Sephardic and Ashkenazic transcriptions; `main_phonetic_mam.py` exports it and renders its [published pages](https://bdenckla.github.io/MAM-basics/phonetic-mam/) in the site tree
   > - [`Yeivin-ITM/`](Yeivin-ITM/README.md) — the exact fractions behind the meteg claims Ben Denckla added to his adaptation of selected excerpts from Israel Yeivin's *Introduction to the Tiberian Masorah*; `main_yeivin_itm.py` writes them and renders the [published excerpts](https://bdenckla.github.io/MAM-basics/yeivin-itm/yeivin_itm.html) in the site tree

   "Displayed Hebrew" keeps the entry from implying MAM's written text, which is C5.1's subject.
2. **C4.7, the licence summary (`:114–117`).** Current: "1. **Code: GPL-3.0**, in [`LICENSE`](LICENSE).
   This covers MAM-basics' work in code and prose — / everything under `py/`, `.github/` and `doc/`
   except the adapted excerpts under / `py/yeivin_itm/content/`, the third-party font under
   `doc/woff2/`, and the page crops in `doc/*-snips/`, / and the generated indexes and reports under
   `out/` that carry no corpus text." Proposed: the same, with "the page crops in `doc/*-snips/`,"
   becoming "the page crops in `doc/*-snips/` and the Hebrew Wikisource Village Pump discussion
   captured and translated in `doc/wikisource-dagesh-discussion-*`,". C4.5's option 1 edits the
   same sentence; apply both together.

#### `DATA-LICENSES.md` (C4.1, C4.2, C4.3, C4.4, C4.7, C15.9; C4.5, C4.6 and C15.10 below)

1. **C4.1 and C4.2, the font row (`:88`), Terms cell.** Its link "[upstream license](…)" points
   into the private hbofonts repository, against Ben's rule of 2026-08-27 in
   `in/repo_maintenance_policy.json`'s `repo_visibility` comment that a private repository's name
   may appear in public files but not "paths inside them, file names of theirs"; the same text is
   public as `in/font-support/taamey-d-0.921/FONT-NOTICE.txt`. And its sentence "Redistribution must
   preserve the copyright and license notices, provide the GPL v2 text, and satisfy its
   corresponding-source requirements." states duties for fourteen copies while the notice, the
   licence text and a source pointer stand beside only the two in `gh-pages/phonetic-mam/woff2/`
   and `gh-pages/yeivin-itm/woff2/`. Proposed Terms cell, which records only facts and changes no
   published byte:

   > GNU GPL version 2, with the font-embedding exception stated in the font's OpenType name table and transcribed in [`FONT-NOTICE.txt`](in/font-support/taamey-d-0.921/FONT-NOTICE.txt). Copyright © 2021 Ben Denckla; Hebrew glyphs © 2009–2010 Yoram Gnat; Latin glyphs © 1999 (URW)++ Design & Development. The exact version 0.921 file is present in the [pinned upstream repository](https://github.com/bdenckla/Taamey_D/blob/40115a364a4e05f610cbd4e6a0abb76fd72b7dab/docs/woff2/Taamey_D.woff2), whose [source tree](https://github.com/bdenckla/Taamey_D/tree/40115a364a4e05f610cbd4e6a0abb76fd72b7dab/sources) records its build inputs. This repository holds the notice, the [GPL v2 text](in/font-support/taamey-d-0.921/GPL-2.0.txt) and the corresponding-source package in [`in/font-support/taamey-d-0.921/`](in/font-support/taamey-d-0.921/README.md), and the site publishes the same package from [`gh-pages/font-sources/taamey-d-0.921/`](gh-pages/font-sources/taamey-d-0.921/SOURCE.txt). Of the thirteen published copies, only the two in `gh-pages/phonetic-mam/woff2/` and `gh-pages/yeivin-itm/woff2/` have `FONT-NOTICE.txt`, `GPL-2.0.txt` and a `SOURCE.txt` pointing to that package beside them, and only those two products' landing pages link that `SOURCE.txt`; the other eleven carry the notice only in their name table. The exception in that notice says that embedding the font in a document does not by itself cause the document to be covered by the GPL. MAM-basics makes no additional grant over the font |

   Not proposed: placing the notice, licence text and a source pointer beside all thirteen published
   copies. That is a product change, 33 new published files, nine of them in directories that no
   generator writes; Ben may ask for it separately. The update's remedy note, that
   `PRODUCT-WOFF2-SOURCE.txt`'s `../../font-sources/` paths are wrong three levels deep, matters only
   to that product change: the two directories that hold a copy of it today are two levels deep,
   where the paths resolve. A pinned upstream link was considered and not proposed: at the package's
   pin `40115a36` the public `bdenckla/Taamey_D` has no `sources/font-m-TaD/license.txt`; only the
   later `38134991` has one.
2. **C15.9, the `in/font-support/taamey-d-0.921/` row (`:57`).** Its last sentence, "[`README.md`](in/font-support/taamey-d-0.921/README.md)
   gives the required future same-host publication mapping and the unverified exact-build
   limitation", becomes "[`README.md`](in/font-support/taamey-d-0.921/README.md) gives the required
   same-host publication mapping, which the Phonetic MAM and Yeivin ITM publishers apply through
   `py/py_html/taamey_d_assets.py`, and the unverified exact-build limitation".
3. **C4.3, three new rows.** After `:50`: "| `Yeivin-ITM/README.md`, `Yeivin-ITM/schema/` | the product's
   README, with the adaptation's permission notice and bibliographic scope, and the closed JSON Schema
   of its claim data | MAM-basics' own work, so GPL-3.0. The adaptation the README describes keeps
   the terms of the `py/yeivin_itm/content/` row below |". After `:54`: "| `Phonetic-MAM/README.md`,
   `Phonetic-MAM/schema/` | the product's README and the closed JSON Schema of its display data |
   MAM-basics' own work, so GPL-3.0 |". After `:56`: "| `gh-pages/phonetic-mam/woff2/` and
   `gh-pages/yeivin-itm/woff2/`, except `Taamey_D.woff2` | in each directory, byte-for-byte copies of
   `FONT-NOTICE.txt` and `GPL-2.0.txt` from `in/font-support/taamey-d-0.921/`, and of its
   `PRODUCT-WOFF2-SOURCE.txt` as `SOURCE.txt`, which the two products' publishers write through
   `py/py_html/taamey_d_assets.py` | The same terms as their sources in the
   `in/font-support/taamey-d-0.921/` row below |".
4. **C4.3 with C4.4, the paragraph before the MAM statement (`:144–150`).** From "and שבגליון הנתונים הזה
   (Hebrew)." (`:144`, Hebrew unchanged) to the paragraph's end becomes: "and שבגליון הנתונים הזה
   (Hebrew). Each of the landed `MAM-parsed/`, `MAM-simple/`, `MAM-with-doc/`,
   `MAM-for-Sefaria/`, `MAM-OSIS/` and `Phonetic-MAM/` product directories holds a `LICENSE.md` that
   repeats the statement after a short preface saying that it applies equally to the data in that
   directory, or, for `MAM-with-doc/`, the edition MAM-basics publishes from `gh-pages/MAM-with-doc/`,
   or, for `Phonetic-MAM/`, the MAM text and its derivative display in `Phonetic-MAM/data/`. The
   preface in `MAM-OSIS/LICENSE.md` excepts the historical `MAM-OSIS/MAPM-orig/` and
   `MAM-OSIS/MAPM-orig-24/` files, which retain the separate CC-BY-SA 3.0 notice recorded above.
   `Yeivin-ITM/LICENSE.md` does not repeat the statement, because that product holds no MAM text; it
   restates what the table records for its files." Under question 4's option 1, C4.4's sentence
   follows "recorded above."
5. **C4.7, the opening paragraph (`:5–11`) and two new rows.** In "… the plans and notes under
   `doc/` — the font at `doc/woff2/` and the page crops in / `doc/meteg-after-silluq-snips/` and
   `doc/lam-2-3-akhla-snips/` excepted, since the table below / covers them — …", the exception
   becomes "the font at `doc/woff2/`, the page crops in `doc/meteg-after-silluq-snips/` and
   `doc/lam-2-3-akhla-snips/`, and the capture and translation of a Hebrew Wikisource Village Pump
   discussion, `doc/wikisource-dagesh-discussion-2026-10-01.mediawiki` and
   `doc/wikisource-dagesh-discussion-translation.md`, excepted, since the table below covers them".
   After `:112` add: "| `doc/wikisource-dagesh-discussion-2026-10-01.mediawiki` | the byte-verbatim
   wikitext of one section of the Hebrew Wikisource Village Pump, ויקיטקסט:מזנון, as page revision
   3086254 held it on 2026-10-01: ten signed comments by four Wikisource users | CC BY-SA 4.0, the
   terms that `doc/wikisource-dagesh-discussion-translation.md`, "Source and attribution", records for
   this source, with its four authors and a link to the page history, which supplies contribution
   attribution |" and "| `doc/wikisource-dagesh-discussion-translation.md` | the English translation
   of that section, with its source record and the translator's notes | CC BY-SA 4.0, as the file's
   "Source and attribution" section states for the source and for this English adaptation |". The
   update's wording correction, Village Pump and not talk page, needs no edit elsewhere: only the
   Claude report, a receipt, says "talk page" (`:463`).

**C4.5, the GPL exclusion over rendering code (question 5).** `DATA-LICENSES.md:6–7` and `:58`, the
root README (`:114–119`) and `Yeivin-ITM/README.md:21–24` exclude all of `py/yeivin_itm/content/` from
the GPL as the adaptation and its remarks, and `Yeivin-ITM/README.md:5–6` says "the renderer and its
helpers are under `py/yeivin_itm/`". But six modules there hold rendering code and no Yeivin or
Revell prose: `my_yeivin_amisc_helpers_for_bibrefs.py` (103 lines), `my_yeivin_amisc_helpers_for_locales.py`
(84), `my_yeivin_amisc_helpers_private.py` (212), `my_yeivin_amisc_tocsec_metadata.py` (77),
`my_yeivin_amisc_traverse.py` (132) and `my_yeivin_amisc_typed_table.py` (29), 637 lines; the GPL-3.0
`renderer.py:8–9` and `helpers.py:2–5` import the first five, and only `my_yeivin_sec_383.py:3` imports
the sixth. The two content modules that `substitutions.py:5–6` imports,
`my_yeivin_amisc_manuscripts.py` and `my_yeivin_amisc_substitutions_private.py`, hold ITM-derived
material and adaptation prose, and are not among the six. Which modules count as adaptation is Ben's
call:
1. **Option 1 (recommended): the six are GPL-3.0 code; the exclusion narrows to the adaptation and
   remark modules.** No pin or output changes.
   - `DATA-LICENSES.md:6–7`: "everything under `py/` except `py/yeivin_itm/content/`, the Pages
     workflow" becomes "everything under `py/` except the adaptation and remark modules of
     `py/yeivin_itm/content/`, the Pages workflow" (merged with C4.7's edit of the same paragraph).
   - `:58`, path cell: "`py/yeivin_itm/content/`, except the six rendering-helper modules in the next
     row"; its last sentence, "This exact subtree is excluded from the blanket `py/` GPL statement",
     becomes "These modules are excluded from the blanket `py/` GPL statement".
   - New row after `:58`: "| `py/yeivin_itm/content/my_yeivin_amisc_helpers_for_bibrefs.py`,
     `my_yeivin_amisc_helpers_for_locales.py`, `my_yeivin_amisc_helpers_private.py`,
     `my_yeivin_amisc_tocsec_metadata.py`, `my_yeivin_amisc_traverse.py` and
     `my_yeivin_amisc_typed_table.py` | Ben Denckla's rendering helpers for the adaptation: page
     traversal, biblical-reference parsing and lists, footnote and section-heading markup,
     section-to-page metadata and a table helper. They hold no Yeivin or Revell prose, and the
     renderer and its helpers import five of them | MAM-basics' own work, so GPL-3.0, like the
     renderer under `py/yeivin_itm/` that uses them |".
   - Root `README.md:114–119`: "… except the adapted excerpts under `py/yeivin_itm/content/`, …"
     becomes "… except the adapted excerpts and their remarks under `py/yeivin_itm/content/`, …",
     and after "… that carry no corpus text." add "Six rendering-helper modules beside the excerpts
     are GPL-3.0 code; [`DATA-LICENSES.md`](DATA-LICENSES.md) names them."
   - `Yeivin-ITM/README.md:5–6` ends "…; the renderer and its helpers are under `py/yeivin_itm/`,
     apart from six rendering-helper modules that sit beside the adaptation in
     `py/yeivin_itm/content/`."; `:21–24` becomes "The adaptation and remark modules of
     `py/yeivin_itm/content/` are excluded from the repository's blanket GPL statement.
     [`../DATA-LICENSES.md`](../DATA-LICENSES.md) records the path-specific terms. The renderer, and
     the six rendering-helper modules that `../DATA-LICENSES.md` names in that subtree, are repository
     code under GPL-3.0."
2. **Option 2: move the modules into `py/yeivin_itm/`**, updating the imports of `renderer.py:8–9`,
   `helpers.py:2–5` and the moved modules (and `my_yeivin_sec_383.py:3` if the sixth moves); the
   pages must stay byte for byte. It needs question 8's options A or C first, and then the "exact
   subtree" wording stays true as it stands.
3. **Option 3: state the status quo.** Append to `:58`'s terms: "The subtree also holds six of Ben
   Denckla's rendering-helper modules, which the GPL-3.0 renderer imports; the exclusion covers them
   as well, and no code licence is stated for them."

Recommendation, option 1: documents only, independent of question 8, no output change, and it states
what the review found; option 2 fits better if Ben wants the directory boundary to be the licence
boundary.

**C4.6, the 1968 passage, `DATA-LICENSES.md:58` and `Yeivin-ITM/README.md:37–40`.** The row places all
of `py/yeivin_itm/content/`, "including the separately identified small comment passage", under the
publication permission for the 1980 book, while the README says that passage
(`my_yeivin_sec_320.py:90–147`, a source comment no page renders) comes from "Yeivin's separate 1968
Hebrew study" and that "Ben accepted" it; the repository records no permission or rights holder for
the 1968 work. The remedy keeps the words of Ben's 2026-09-19 decision and adds the facts, drawing no
legal conclusion:
- `:58`, terms cell, current: "Adapted by permission. The 1980 work is copyright © 1980 by the Society
  of Biblical Literature. Ben's 2026-09-19 decision treats the existing publication permission as
  extending to this editable adaptation, including the separately identified small comment passage;
  it does not establish a GPL sublicense or grant further rights. See … This exact subtree is
  excluded from the blanket `py/` GPL statement". Proposed: after "…or grant further rights." insert
  "That permission's stated object is the 1980 book. The comment passage comes from Yeivin's separate
  1968 Hebrew study, for which the repository records no permission and no rights holder, and no
  grant is made or implied here over it."
- `Yeivin-ITM/README.md:37–40`, after "It is not an edition of ITM." insert: "The permission above
  names only the 1980 work, and the repository records no permission for the 1968 study and no rights
  holder of it." The sentence "Ben accepted this small comment-only passage with the editable
  adaptation." stays.

**C15.10, `DATA-LICENSES.md:51`.** Its terms end "The source copyright and permission notice remains
on the pages"; the notice (`_COPYRIGHT`, `py/yeivin_itm/renderer.py:236–245`) is on the 11 section
pages and not on the landing page or the five footnote pages. Proposed ending: "The source copyright
and permission notice remains on the eleven section pages, whose names end in a section range, such as
`yeivin_itm-207_285.html`; the landing page `yeivin_itm.html` and the five footnote pages
`yeivin_itm-huge-ftnt-*.html` do not carry it". Adding the notice to the six pages, which would change
published pages, is not proposed.

Left as written, with their reasons: the Claude report's repetition of the hbofonts path (`:403–404`)
and `doc/PLAN-checkout-kinds-and-portable-knowledge.md:261`, both receipts, which may not be edited
(`iterative-document-editing`, "Finished receipts and maintained documents"); and the hbofonts
file paths in `doc/windows-long-paths.md:130–137`, a maintained guide whose same question Ben
deferred on 2026-09-28 (the September 26 round's finding 35.1,
`doc/dual-agent-review-2026-09-26-turn-01-claude-update.md:356`), a deferral that stands.

Verification for the reader-facing Markdown: `git diff --check`;
`git grep -n -F "github.com/bdenckla/hbofonts/" -- DATA-LICENSES.md` prints nothing;
`git ls-files --error-unmatch` on every path the new links name;
`py/main_test.py py/tests/test_prose_mark_order.py py/tests/test_prose_conventions.py`.

#### `doc/process-documentation/pipeline.svg` and the root README's offer of it (C11, question 6)

The root README's "Core pipeline" (`README.md:7–19`) names the download, `main_parse.py ws`,
`main_mam_simple.py`, `main_mam4sef.py`, `main_mam_osis.py` and `main_mam_with_doc.py`, then says
"Two diagrams show this pipeline:" and links `pipeline.svg` and `MAM-process.dot.svg`.
`pipeline.svg` is generated by `./.venv/Scripts/python.exe py/main_pipeline_graph.py` (the mega
step `pipeline-graph`) from `py/pipeline_graph/pipeline_graph_spec.py`. At `644a6c9c` it draws 12 of
the mega's 57 steps (parse-ws, foi-features-of-interest, mam-with-doc, tmpl-survey, mam-simple, the
five "misc-1" steps decnreub, multimark, wordlist, explicit-xataf and diff-ctr-vs-mam, ws-bot-proto
as "misc-3", and gen-misc under the stale label "...english_documents", which is now the name of
book-of-job's site generator); none of the five steps the window added; and four programs the
mega does not run: `py/main_mam4sef.py` and `py/main_mam_osis.py` (both in `NOT_IN_MEGA`),
`py/main_ws_bot.py real` (in `NOT_IN_MEGA`) and `osis_split_mapm`, whose program `85c6c354` deleted
on 2026-03-10 (spec `:72`, `:119`, `:152`). The split between mega steps and external prerequisites
is only a pair of comments in `pipeline.dot` (`:23`, `:27`); the SVG marks nothing, and the
prerequisite node's attributes (spec `:55–60`) override the dashed style. Every download reparses
(`py/subcommands/download_wikisource.py:62`), but only the bot is drawn with the reparse edges.

**The floor fix, owed under options 1 and 2 (a spec defect).** In the spec delete
`DisplayNode("osis_split", "osis_split_mapm", PIPELINE_STEPS),` (`:72`),
`RawNode("main_osis_split_mapm", "osis_split_mapm", "osis_split"),` (`:119`) and
`RawEdge("main_osis_split_mapm", "out_osis", "MAM-simple pipeline"),` (`:152`); after the
download's edge to `in_mam_ws_special` (`:167–171`) add
`RawEdge("main_download__fr_wikisource", "out_local", "Wikisource pipeline", attrs=(("tooltip", "via automatic reparse"),))`
and the same edge to `"mpu_plus"`. Regenerating then drops the `osis_split` node and edge from
`pipeline.dot` and adds `download_ws -> ds_out` and `download_ws -> ds_parsed_plus` with that
tooltip. If Ben defers question 6, the floor fix lands alone.

**What the graph depicts is Ben's decision (question 6).**

1. **Option 1: every mega step.** The spec gains a table keyed by all 57 `_STEPS` ids, each with
   the stores it reads and writes, and one keyed by `NOT_IN_MEGA` for the four drawn hand-run
   programs (the download, the bot, `main_mam4sef.py` and `main_mam_osis.py`); about 30 stores are
   added and the SVG grows from 23 nodes to about 90. Mega steps are solid boxes, hand-run
   programs dashed and gray, with the legend "Solid box: a step of py/main_0_mega.py. Dashed box:
   a program the mega does not run." A new test in `py/tests/test_mega_coverage.py` requires the
   table's keys to equal the `_steps()` ids in order and every hand-run key to be in
   `NOT_IN_MEGA`; nothing can lint the hand-entered edges. README item 1 becomes:
   "[`doc/process-documentation/pipeline.svg`](doc/process-documentation/pipeline.svg) draws every
   step that `py/main_0_mega.py` runs, with the directories each step reads and writes. A dashed
   box is a program that the mega does not run, such as the download and the Wikisource bot."
2. **Option 2 (recommended): the core pipeline that the README names.** The spec's docstring
   states the rule: "The graph draws the programs that the root README's 'Core pipeline' section
   names, and `py/main_ws_bot.py real`, whose saves and post-run download feed that pipeline. It
   draws the stores those programs read and write among Hebrew Wikisource, `in/mam-ws/`,
   `in/mam-ws-special/`, `MAM-parsed/plus/`, `MAM-simple/`, `MAM-for-Sefaria/`, `MAM-OSIS/` and
   `gh-pages/MAM-with-doc/`, and nothing else. A program that `py/main_0_mega.py` runs is a solid
   box labelled with its step ids; a program it does not run is a dashed gray box." Dashed: the
   download, `main_mam4sef.py`, `main_mam_osis.py` and the bot; solid: `main_parse.py ws`
   (parse-ws), `main_mam_simple.py` (mam-simple, mam-simple-docs) and `main_mam_with_doc.py`
   (mam-with-doc). Dropped: foi, tmpl_survey, misc-1, misc-3, "...english_documents",
   `osis_split_mapm`, the `out/` store and the Google Sheet note. The floor fix's reparse edge and a
   legend are included, and the attribute override at spec `:55–60` goes. A new test in
   `py/tests/test_mega_coverage.py` checks that a node with step ids names `_STEPS` ids whose scan
   runs that node's program or one of its subcommands, that a node without step ids is a
   `NOT_IN_MEGA` key, and that the drawn programs other than the bot equal the backticked
   `main_*.py` commands of `README.md`'s "### Core pipeline", prefixed with `py/` (six today).
   README item 1 becomes: "[`doc/process-documentation/pipeline.svg`](doc/process-documentation/pipeline.svg)
   draws the programs named above and the Wikisource bot, with the directories they read and
   write. A solid box is a step of `py/main_0_mega.py`; a dashed box is a program run by hand."
3. **Option 3: retire the graph.** Delete `pipeline.dot`, `pipeline.svg` and `py/pipeline_graph/`;
   `py/main_pipeline_graph.py` keeps only the `MAM-process.dot.svg` render (its docstring's "TWO
   GRAPHS" section and the step note at `py/main_0_mega.py:690–694` are rewritten); delete the test
   at `py/tests/test_graph_provenance.py:244–255` and its import at `:9`; in
   `py/tests/test_graphviz_version_pin.py:64–67` "Eight" becomes "Seven" and `pipeline.svg` is
   dropped; `doc/process-documentation/MAM process original -- provenance.md:9–10` drops "which also
   generates this directory's other graph, `pipeline.dot` and `pipeline.svg`";
   `dot-claude/skills/mam-repository-topology/references/evacuated-repositories.md:55–56` says
   "`py/main_0_mega.py` never names it"; and `README.md:16–19` becomes "A diagram shows this
   pipeline: [`doc/process-documentation/MAM-process.dot.svg`](doc/process-documentation/MAM-process.dot.svg)."

Under every option, the record that `py/tests/test_mega_coverage.py:246–251` gives for
`py/main_download.py fr-wikisource` changes. Current: "A network download from Hebrew Wikisource,
run when the upstream moves.  Recorded in doc/process-documentation/pipeline.dot ("External
prerequisites (not part of _STEPS)"), the closing comment of py/main_0_mega.py's main(), and
doc/mega-coverage-2026-09-10.md §3." Proposed, options 1 and 2: "... Recorded in
py/pipeline_graph/pipeline_graph_spec.py, which draws it dashed as a program the mega does not run,
the closing comment of py/main_0_mega.py's main(), and doc/mega-coverage-2026-09-10.md §3."; option
3: "... Recorded in the closing comment of py/main_0_mega.py's main() and
doc/mega-coverage-2026-09-10.md §3." `doc/mega-coverage-2026-09-10.md:288–292`, which raised the
drift, is a dated record and stays as written. `MAM-process.dot` still draws the retired
`parsed-plain` (`MAM-process.dot:16`, `:39`, `:44`); that is outside C11 and this plan leaves it.

Recommendation, option 2: it draws what the README describes, a product pipeline that already
includes two hand-run programs, and its lint fails the suite on drift against either the README or
`_STEPS`. Option 1 duplicates `_STEPS` in a graph whose edges nothing checks; option 3 leaves only
`MAM-process.dot.svg`, which draws the retired `parsed-plain`.

Generated effects: `pipeline.dot` and `pipeline.svg` only (option 3 deletes them);
`MAM-process.dot.svg` stays byte for byte. Regenerating needs Graphviz at the pinned stamp
`16.0.0 (20260814.1018)` (`py/mb_cmn/graphviz_pin.py:144`); never commit a `.dot` without its SVG.
Verification: regenerate with `./.venv/Scripts/python.exe py/main_pipeline_graph.py` and read both
diffs; then `py/main_test.py py/tests/test_mega_coverage.py py/tests/test_graph_provenance.py py/tests/test_graphviz_version_pin.py py/tests/test_product_scopes.py`.
The spec is read by a mega step, so the final mega covers it.

#### `doc/wikisource-dagesh-discussion-translation.md` (C15.30)

A maintained translation ("State: live; refreshed when Ben requests an update."). Its
introduction (`:8–11`) says: "The initial proposal rests on a misunderstanding that Dovi
subsequently corrects: the request for a distinct dagesh ḥazaq character had already succeeded
alongside the vocal shewa request." The capture shows Mo Yu Hu first (capture `:19`, signed 22:13
IDT on 30 September 2026, the translation's comment 2) and Dovi after (capture `:25–27`, signed
06:39 IDT on 1 October 2026, comment 6, which begins "As Mo Yu Hu correctly wrote"). Proposed, as an
exact substring replacement that leaves the rest of the sentence's bytes alone: "that Dovi
subsequently corrects" becomes "that Mo Yu Hu corrects first, citing an earlier discussion on the
same page, and that Dovi then confirms and explains, crediting Mo Yu Hu". The sentence then reads:
"The initial proposal rests on a misunderstanding that Mo Yu Hu corrects first, citing an earlier
discussion on the same page, and that Dovi then confirms and explains, crediting Mo Yu Hu: the
request for a distinct dagesh ḥazaq character had already succeeded alongside the vocal shewa
request." C4.7 edits the licence statements about this file, not the file itself.

## Lower-risk changes

### Summary by type

1. **Code and tests (D7: defects).** C1's two gates and a dead module (question 7); C6.2's Yeivin
   migration gate (question 8); C9.1 to C9.5; C12.1 to C12.4; C13.1; C15.3; C15.4; C15.11; C15.12;
   C15.18 to C15.20; C15.28; and the relay's removal. New lints or checks come with C4.3, C5.1, C6.1,
   C6.2 (option C), C9.4, C11 (option 2), C12.1, C12.2 and the relay's turn files (R5). No
   other generated output changes beyond those listed under "Outputs expected to change".
2. **Agent instructions and skills.** `AGENTS.md` (C10.4, C15.23), which takes effect when
   committed; the skills `hebrew-prose` (C10.3, C15.15),
   `mam-wikisource-refresh` (C1.3, C8), `mam-repository-topology` (C15.24) and `github-issues`
   (C15.25), which take effect when deployed (act A3); and the bot guide (C7).
3. **Markdown under `doc/` and update entries.** C10.2, C15.2, C15.13, C15.26 and C15.29; C9.3's
   two runbook passages; C13.1's sentence in the compute document; the relay's procedure text (R6)
   and the October 1 round's update (R7); and the finding-22 pointer (C5.2).
4. **Python comments, docstrings and help text.** C10.1, C10.4, C14, C15.5, C15.6, C15.17, C15.21,
   C15.22, C15.27 and C15.31 (question 13).

### Reproducible defects in code and tests (D7: defects)

Each fix stays within its approved disposition and the rule that tests be differential or
lint-shaped. A scratch demonstration named here runs from a gitignored scratch directory and is never
committed.

#### C1, the gates a text refresh trips (question 7)

**C1.1, the Yeivin claims gate.** `py/yeivin_itm/claims.py:32–42` hashes the whole of
`out/accgram/meteg-before-stress.json`, and `claim_schema.pin_claims` (`py/yeivin_itm/claim_schema.py:93–102`)
raises "The independent meteg analysis has changed; review Ben's claims" unless that hash equals
`APPROVED_INPUT_SHA256`. The survey embeds the SHA-256 of each of the 39 release files
(`py/accgram/meteg_before_stress.py:345–356`), so any release change trips the pin: in memory, one
changed release-file hash raises while all 20 fractions stay equal. `Yeivin-ITM/README.md:75–78`
states the intent: "The prose pins in `py/yeivin_itm/claim_schema.py` fix the reviewed fractions and
input hash, so a changed corpus or population requires a fresh review." The design is Ben's:
1. **Gate A: keep the whole-file pin and add the procedure.** Every refresh that changes displayed
   text stops the mega at `yeivin-itm-survey-meteg-claims` and needs Ben's review, even when no
   fraction moves; the error never names a fraction. No code changes. README `:75–78` becomes: "Ben
   approved correction of his added claims and their explanatory prose on 2026-10-01. The prose pins
   in `py/yeivin_itm/claim_schema.py` fix the 20 reviewed fractions and the SHA-256 of the whole
   analysis file, `out/accgram/meteg-before-stress.json`. That file records the SHA-256 of every
   Phonetic MAM release file, so any change to the release requires Ben's fresh review, even when no
   fraction moves. Until he approves, `survey-meteg-claims` and `check` raise and write nothing."
2. **Gate B (recommended): pin the fractions and the claim population.** Pin the 20 fractions and a
   SHA-256 of the canonical JSON of every ordinary-population record whose pattern is FR1, FR2, FR3,
   AFR1, AFR4 or XAFR1 (3,914 of 6,049 today: 722, 1,147, 1,714, 137, 173 and 21), each with all ten
   fields; the claim file keeps `input.sha256`, the whole-file hash, as provenance, not as a pin. A
   refresh that changes no claim record and no fraction passes, changing only line 5 of
   `Yeivin-ITM/meteg-claims.json`; one that does raises "The claim population has changed; review
   Ben's claims" or "Ben's prose pin changed: <name>; review the footnotes". Code: in
   `claim_schema.py`, `CLAIM_PATTERNS` and `APPROVED_POPULATION_SHA256` replace
   `APPROVED_INPUT_SHA256`, and a `pin_population` sits beside `pin_claims`, which keeps the fraction
   pins; `claims.py` gains `population_sha256(survey)` and applies `pin_population` in
   `from_analysis`; `claim_schema.validate` splits into a shape check and the pins, because
   `renderer.page_texts` validates at `renderer.py:40`; `py/tests/test_yeivin_itm.py:115` goes,
   since `:130` already ties the claim file to the analysis; and a new read-only
   `py/main_yeivin_itm.py review-claims` prints each changed pin, approved and projected, and the
   page lines that would change, computed in memory. The docstring at `claim_schema.py:3–4`,
   "Changing the corpus or a population requires inspecting both the data and prose.", becomes
   "Changing a fraction or a record of the claim population requires inspecting both the data and
   prose." README `:75–78` becomes: "Ben approved correction of his added claims and their explanatory
   prose on 2026-10-01. The prose pins in `py/yeivin_itm/claim_schema.py` fix the 20 reviewed
   fractions and a SHA-256 of the claim population: every record of
   `out/accgram/meteg-before-stress.json` whose pattern is FR1, FR2, FR3, AFR1, AFR4 or XAFR1. A
   changed fraction, or a changed, added or removed record in that population, therefore requires
   Ben's fresh review; a change elsewhere in the Phonetic MAM release does not. Until he approves new
   pins, `survey-meteg-claims` and `check` raise and write nothing. The claim file's input SHA-256
   identifies the whole analysis file that it was projected from; it is not a pin."
3. **Gate C: pin the fractions only.** About five lines; the least review, but it misses a changed,
   added or removed record that leaves every count equal, though the footnotes name population
   members (the AFR1 footnote's "including that in …" cites Ezekiel 3:15's chanted word). README
   `:75–78` becomes: "… fix the 20 reviewed fractions, so a changed fraction requires Ben's fresh
   review; a change to the Phonetic MAM release that leaves every fraction unchanged does not, even
   when it changes which records a population holds. …" with the same last two sentences as Gate B.

Under every design `:78–79` ("Numerical text is inserted … original fractions.") stays. Recommendation,
Gate B: it keeps the README's stated intent for the population, including which chanted words a
footnote names, and drops the trigger that stops every text refresh. The gate's behaviour has no
admissible test (it would be example-based fault injection); the executor runs a scratch
demonstration: one release-file hash changed passes under B; one claim-population record's `hebrew`
changed raises the population error; C2's 13 reclassifications raise. Land C2 first, so that B's
population hash is set once, from the corrected survey.

**C1.2, the frozen legacy display oracle.** `test_complete_release_and_unified_projection`
(`py/tests/test_phonetic_display_release.py:12–20`) compares every rendered chapter, in both
pronunciations, with `in/phonetic_mam_legacy_projection_sha256.json`: 1,858 hashes, 929 chapters in
two pronunciations, of a canonical projection of each chapter page's `body/main` (verses, rows and
cells, the other pronunciation's spans dropped; `py/phonetic_mam/projection_check.py:56–142`), frozen
from phonetic-hbo `8da90513`'s pages, which can no longer be produced. Only this test reads the file
and no code writes it; it holds today (`verify_site` passes in about 20 seconds), and one changed
point in Genesis 1 breaks both of that chapter's hashes. Regenerating it from the new renderer would
make the test circular. The design is Ben's:
1. **Oracle A (recommended): a per-chapter freeze while the chapter's input is unchanged.** A new
   frozen record, `in/phonetic_mam_legacy_projection_inputs.json` (schema
   `phonetic-mam-projection-inputs-v1`, `source_commit`, and `chapters` mapping each page path to a
   SHA-256), created once at execution from `MAM-parsed/plus/` at a commit where the oracle holds:
   each fingerprint hashes the canonical JSON of the verse before the chapter, the chapter's verses
   and the verse after it (the plus reader attaches each verse's successor's cell C across chapter
   boundaries, `py/mb_cmn/read_books_from_mam_parsed_plus.py:80–84`, `:105–107`). 929 fingerprints map
   one to one onto the oracle's paths (about 86 KB). `verify_site` compares a chapter only while its
   current fingerprint equals the recorded one, and `py/main_phonetic_mam.py check` lists the chapters
   that have left the comparison; unchanged chapters must still match, so exporter and renderer
   regressions are still caught, and a display change in a chapter whose input did not change fails.
   No code writes either record after its creation. About 60 to 90 lines.
2. **Oracle B: a Hebrew differential against MAM-simple**, by declared, closed rules (qere only at
   perpetual-qere sites, no extraordinary points, the second parameter of the stress-helper
   templates, varika kept, gray maqaf as tilde), with 2 Kings 22:1 and 2 Chronicles 25:17 as
   reviewed exceptions. Independent of the exporter and valid across refreshes, but it covers only
   the Hebrew, and costs about 200 to 400 lines with upkeep.
3. **Oracle C: a frozen migration record outside the default suite.** The cheapest; the suite loses
   its only end-to-end regression check of the exporter and renderer.

Recommendation, Oracle A: it keeps the original independent oracle exactly where it is valid, needs
no approval per refresh, and fails loudly rather than silently. Under A, `Phonetic-MAM/README.md:12–14`,
"Complete-output comparison with the previously published pages and assessment of all artifacts
together are required before a release is approved. Schema validation and rendered-page parity alone
are insufficient.", becomes: "The release's complete output was compared with the pages that
phonetic-hbo published at the commit named below, and all artifacts were assessed together; schema
validation and rendered-page parity alone were not enough. Those pages cannot be produced again, so
the comparison cannot be repeated for text that MAM has changed since. The suite compares each
rendered chapter with the old pages' frozen projection hashes only while the chapter's MAM-parsed
input matches its fingerprint in `in/phonetic_mam_legacy_projection_inputs.json`; a chapter that a
refresh changes leaves that comparison, and its diff is reviewed instead." Verification:
`py/main_test.py py/tests/test_phonetic_display_release.py`; `./.venv/Scripts/python.exe py/main_phonetic_mam.py check`;
and a scratch demonstration (the fingerprint function takes a directory argument): change one chapter
in a scratch copy of `MAM-parsed/plus` and its page in memory, and that chapter leaves the comparison
while the others pass; change a page whose input is unchanged, and the check fails.

**C1.3, the missing re-approval procedure, and a dead module.** No tracked text says which constants
a refresh changes, how the legacy hashes are replaced, or who approves; `git grep` for "re-approv",
"reapprov" and `APPROVED_INPUT_SHA256` finds only the code and `test_yeivin_itm.py:115`.
`py/phonetic_mam/legacy_projection.py` has no importer, no entry point, and runs only against the two
legacy page families, which survive only in phonetic-hbo's history at `8da90513`, which no maintained
clone holds. Proposed:
1. **Delete `py/phonetic_mam/legacy_projection.py`.** In `doc/phonetic-mam-preparation.md`, `:20–22`,
   "The independent `legacy_projection` module reads only the frozen public HTML. The source-driven
   exporter must produce the same complete display corpus as this public-only projection. Matching
   rendered HTML alone is insufficient.", becomes: "Until <date>, the independent `legacy_projection`
   module projected the frozen public HTML of phonetic-hbo commit `8da90513` into the release schema,
   and the source-driven exporter had to produce the same complete display corpus; matching rendered
   HTML alone was insufficient. The 2026-10-02 review ran that module by hand and found all 39 books
   equal. The module was removed on <date> because it reads only the two old page families, which no
   generator can now produce and no maintained clone holds; Git history keeps it at
   `<last commit holding it>`. For chapters whose MAM-parsed input is unchanged, the frozen projection
   hashes in `in/phonetic_mam_legacy_projection_sha256.json` remain the comparison with those pages."
   `:22–24`, "Review also covers … boundary.", stays.
2. **The refresh procedure,** in `dot-claude/skills/mam-wikisource-refresh/references/dependent-refresh.md`:
   - step 1, after "commit only the audited refresh paths.", add: "If the mega stops at
     `yeivin-itm-survey-meteg-claims`, follow "Gates that a text change can trip", item 1, before
     committing.";
   - step 4's "Failed gates, stale inputs and unexplained output changes stop the workflow." becomes
     "Failed gates, stale inputs and unexplained output changes stop the workflow; "Gates that a text
     change can trip" says how the Yeivin claim pins and the legacy display projection are
     resolved.";
   - "Required scenario behavior" gains "6. A changed claim-population record or Yeivin fraction
     stops the refresh until Ben approves new pins.";
   - a new section before "## Required scenario behavior", written here for Gate B and Oracle A:

   ```markdown
   ## Gates that a text change can trip

   Two checks compare current output with records that no generator rewrites. A refresh that
   changes MAM's text can trip both. Approval of the refresh does not approve either record, and no
   agent approves the Yeivin pins.

   1. **The Yeivin claim pins.** `py/yeivin_itm/claim_schema.py` pins the 20 fractions that Ben
      approved and a SHA-256 of the claim population, which is every record of
      `out/accgram/meteg-before-stress.json` whose pattern is FR1, FR2, FR3, AFR1, AFR4 or XAFR1.
      When a pinned fraction or a claim-population record changes, the mega stops at
      `yeivin-itm-survey-meteg-claims`, and `py/main_yeivin_itm.py survey-meteg-claims` and
      `check` raise without writing.
      1. Leave `py/yeivin_itm/claim_schema.py`, `Yeivin-ITM/meteg-claims.json` and
         `gh-pages/yeivin-itm/` unchanged.
      2. Run `./.venv/Scripts/python.exe py/main_yeivin_itm.py review-claims`, which writes
         nothing, and give Ben its report: each changed fraction with its approved and new
         values, and each page line whose text would change, before and after. Add the
         claim-population records that `git diff -- out/accgram/meteg-before-stress.json` shows
         added, removed or changed.
      3. Stop until Ben approves the new pins in his own message. Without that approval the
         refresh ends before any push.
      4. With his approval, change only the pins he approved and run
         `./.venv/Scripts/python.exe py/main_0_mega.py --resume-from yeivin-itm-survey-meteg-claims`.
         Audit the regenerated claim file and pages. Commit step 1's refresh paths first, then the
         pins, the claim file and the changed pages in a commit of their own whose message quotes
         Ben's approval.
   2. **The legacy display projection.** `test_complete_release_and_unified_projection` compares a
      rendered Phonetic MAM chapter with its frozen hashes in
      `in/phonetic_mam_legacy_projection_sha256.json` only while the chapter's MAM-parsed input
      matches its fingerprint in `in/phonetic_mam_legacy_projection_inputs.json`.
      `./.venv/Scripts/python.exe py/main_phonetic_mam.py check` lists the chapters that have left
      the comparison. Require each listed chapter to be one whose data a committed refresh changed,
      and audit each newly listed chapter's rendered diff in both pronunciations. A mismatch in a
      chapter whose input is unchanged is a regression: stop and resolve it. Never regenerate
      either file; no source exists for the old pages' display of new text.
   ```

   Under Gate A or C, item 1's first two sentences take that design's description from C1.1 and
   step 2 drops `review-claims` unless it is built anyway; under Oracle C, item 2 becomes "The legacy
   display projection is a frozen migration record outside the suite; do not run or regenerate it
   during a refresh." Under question 8's option B, item 1.4 also records each changed page line in
   `in/yeivin_itm_legacy_differential.json`. The skill takes effect when deployed (A3), and C8 edits
   the same file.

**C12.2, `test_meteg_before_stress` has no independent oracle.** The module docstring
(`py/accgram/meteg_before_stress.py:3–6`) says "The FR/AFR classification preserves the existing
algorithm's syllable grouping, vowel-length convention, structural table, accent buckets, and case
selection." No tracked record holds that comparison, and the tests check only regeneration, field
shape and the claims' reproduction.
- Docstring, `:3–6` becomes (`:8–10` unchanged):

  ```text
  Reduced syllables are grouped with their following main syllable; the target is
  the main part of the grouped syllable two before primary stress. The syllable
  grouping, vowel-length convention, structural table, accent buckets and case
  selection were written to follow this survey's private predecessor, but no tracked
  record compares the two. py/tests/test_meteg_before_stress.py checks the accent
  class against accgram's prose and poetic scanners and the target meteg against an
  independent nucleus locator.

  In a poetic verse, U+05A5 on the stressed syllable is the conjunctive merkha unless
  it is the yored of oleh-weyored, which is disjunctive. The yored is identified when
  the chanted word's accent vector has U+05AB, the oleh, before its final U+05A5. A
  candidate whose U+05A5 follows an oleh on the previous chanted word is refused
  rather than classified.
  ```
- The test module's docstring (`py/tests/test_meteg_before_stress.py:1–5`) becomes: "Independent-oracle
  differentials, regeneration and disclosure-shape checks. / The full tracked analysis is the golden
  for regeneration. Two of its fields are also checked against oracles that share none of the
  classifier's code: the accent class against accgram's prose and poetic scanners, which read each
  chanted word's displayed Hebrew, and the target meteg against accgram's nucleus parser. The public
  display corpus is the only input; the one-time migration oracles are not test inputs."
- Two new checks:
  1. **Accent class.** For each verse's cant-alef selection and each qamats selection, feed accgram's
     scanners each chanted word's plain displayed Hebrew, `Reading.hebrew` (not `scanner_word()`,
     which writes a geminate dagesh as U+05C4 and so stops the prose scanner's legarmeh lookahead),
     through `uni_to_marks.word_to_marks`, `cwa._verse_units` and `cwa._by_chanted_word`, appending
     the display's paseq marker as `post_stress_meteg_model._accent_grammar_tokens_by_entry` does;
     run `poetic_scanner.scan_accent_tokens` or `prose_scanner.scan_accents` as
     `poetic_filter.should_keep_line` routes the verse; match the survey's records to the readings in
     order by `(bcv, hebrew, transcription, qamats_variant)`, with no call to the classifier; a
     chanted word is disjunctive if any token is in `pan.POETIC_DISJUNCTIVES` or
     `post_stress_meteg_model._PROSE_DISJUNCTIVE_TOKENS`. Assert that every record was matched and
     that the disagreements equal a declared set, keyed by `(population, bcv, tokens)` with no Hebrew
     literal in source. After C2's fix that set is 18 records, in each of which the chanted word has a
     dexi and its stress helper, and the poetic scanner reads the two dexi marks as the pair
     `DEXI_DEXI`, which is not a grammar token, while the survey's disjunctive is right: Psalms 24:7,
     37:36, 77:20, 78:31, 78:35, 78:57, 94:20, 99:5, 99:9, 105:3, 106:24, 107:25 and 136:18; Job 11:17
     (ordinary and samekh), 16:8, 22:4 and 32:13 (the last two with a `MUNAX` token too). The update's
     "25" holds only for `scanner_word()` input, where seven prose munax legarmeh sites read as
     `MUNAX`.
  2. **Target meteg.** For each record, `post_stress_meteg_model._parse(hebrew, transcription)` aligns
     the transcription's syllable nuclei with the Hebrew's; syllables holding a hataf vowel are
     reduced; the target is the main syllable two main syllables before the stressed one; assert
     that U+05BD on the target's nucleus letter equals `target_meteg`, and that the count compared
     equals the record count and is not zero. 6,119 of 6,119 agree.
- The two run in about 28 seconds. Their oracles share no classifier code: the token types, the
  disjunctive sets, the chanted-word segmentation, the verse routing and the nucleus parser are
  accgram's. Both still read the same display through `analysis_reader`, and neither tests
  `pattern`, `accent_on_target` or `other_meteg_count`.

**C6.2, the migration gate and the "editable adaptation" (question 8).** `Yeivin-ITM/README.md:3` and
`DATA-LICENSES.md:58` call `py/yeivin_itm/content/` an editable adaptation, but no text says how to
edit it, and `py/tests/test_yeivin_itm.py` forbids every edit: 112 of its 114 modules are pinned by
hash in `in/yeivin_itm_legacy_differential.json` (`:228–339`; asserted at `:99–104`); each page is
reconstructed by reversing hand-recorded changes (13 records on four pages) and hashed against the
legacy page (`:23–37`); the set of changed pages is hard-coded (`:46–51`); and every Hebrew example's
attributes and text must equal the legacy page's (`:77–83`). In memory, the C6.1 correction fails at
`:36` and `:104`, and, even recorded with its pin updated, at `:46` and `:82`. The same gate forbids
C9.2's three content-module fixes, C15.31 and C4.5's option 2, and lets C2's corrected figures pass
only once their change records are rewritten by hand (C2's "Order", step 4). Whether to keep it is
Ben's decision:
1. **Option A: retire the gate; regeneration becomes the test.** Delete `_oracle` and `_legacy_text`
   (`:18–37`) and the module-pin test (`:96–104`); keep the checks that the pages equal their
   regeneration (`:53`), that they hold no forbidden mark or claim marker (`:55–56`), that ids are
   unique (`:65`), that the favicon is present (`:67–72`) and that links and fragments resolve
   (`:84–93`); add C6.1's lint. The legacy differential stays as a frozen record that no test reads.
2. **Option B: keep the gate and record approvals.** The differential becomes
   `yeivin-itm-legacy-differential-v2`, with a top-level `approvals` map, an `approval` key on each
   change, optional per-page `approved_examples` pairs of old and new attributes, and an
   `edited_content` map to which an edited module moves from `unchanged_content_sha256`; the tests
   accept a difference only through a recorded approval. Every edit then takes a six-step procedure,
   and the existing landing-page font-link record has no recorded approval of Ben's to cite.
3. **Option C (recommended): option A, keeping the published fragment ids.** Option A, plus a new
   frozen record `in/yeivin_itm_published_anchors.json`, built once at execution from the 17 pages'
   `//@id` values in document order (345 ids: 103 `nsNNN`, 121 `sec-N-callout-N`, 121 `sec-N-ftnt-N`;
   written with `ensure_ascii=False`, `indent=2` and a trailing newline), and a test that every
   recorded id remains (ids may be added). phonetic-hbo's redirect pages forward old addresses with
   their fragments to these pages (`py/redirect_stubs/stubs.py:725–726`), and the filenames are
   already guarded (`py/tests/test_redirect_manifest.py:78–94`), so the ids are the one legacy
   property something still relies on.

Recommendation, option C: the evacuation is complete and deployed, every edit already shows as a
diff in the regenerated pages, and the repository already holds that "the one-time migration oracles
are not test inputs" (`py/tests/test_meteg_before_stress.py:3–4`); C keeps the one property the
redirects need, at the cost of one frozen file and one test. Under A or C, `Yeivin-ITM/README.md:81–89`
becomes:

> `in/yeivin_itm_legacy_differential.json` is the frozen record of the migration from phonetic-hbo
> commit `8da90513df1c759d8db34b135d007e79686715d3`. From the pages and adaptation modules as of
> `<the parent of the commit that retires the gate>`, it reconstructed each page that phonetic-hbo
> commit published, after removing the shared favicon line and reversing only Ben's approved
> numerical and explanatory corrections in three pages and the landing page's font-source link, and
> it pinned every other adaptation module to its mechanically moved public source. No test reads it
> now.
>
> ## Editing the adaptation
>
> The adaptation under `py/yeivin_itm/content/` is editable source, and Ben approves each change to
> it. After editing a module, regenerate the pages and run the product's tests from the repository
> root:
>
> ```powershell
> ./.venv/Scripts/python.exe py/main_yeivin_itm.py render
> ```
>
> ```powershell
> ./.venv/Scripts/python.exe py/main_test.py py/tests/test_yeivin_itm.py
> ```
>
> The regenerated pages are the test: read every changed line under `gh-pages/yeivin-itm/` before
> committing, and name in the commit message the approval of Ben's that the change carries out. The
> tests require the tracked pages to equal regeneration, every internal link and fragment to
> resolve, and every biblical reference to name a verse in one of the three versifications that
> MAM-simple ships. Ben's numerical claims are not edited in the pages; they come from
> `meteg-claims.json` under the pins described above.

and option C adds: "`in/yeivin_itm_published_anchors.json` lists the 345 fragment identifiers that the
17 pages had at the end of the migration, the same identifiers as the pages phonetic-hbo published.
phonetic-hbo's redirect pages forward old addresses, fragments included, to these pages, so the
tests require every listed identifier to remain. An edit may add identifiers; removing one is Ben's
decision and updates that record in the same commit." Under A, `:53–54`, "All 17 existing filenames,
internal links, and anchors are preserved.", becomes "The migration preserved all 17 existing
filenames, internal links, and anchors."; under C it stays, since it remains enforced. Under B,
`:81–89` describes the v2 record and a six-step editing procedure instead. Verification:
`py/main_test.py py/tests/test_yeivin_itm.py py/tests/test_redirect_manifest.py`, then the full suite
after the last test change.

**C13.1, the compute stream ends on an undecodable byte.** `py/main_phonetic_mam.py:58` reconfigures
standard input as strict UTF-8, and `compute.serve` reads in its `while` condition, outside its `try`
(`py/phonetic_mam/compute.py:295–321`), so one byte that is not UTF-8 ends the process with exit 1 and
drops replies already owed, against `doc/phonetic-mam-compute.md`'s "Each input line receives one
output line" and "A rejected ordinary line does not end the stream". Reproduced through the command
line with UTF-8 mode off and on. Fix: `:58` becomes
`sys.stdin.reconfigure(encoding="utf-8", errors="surrogateescape")`, and `main()`'s docstring gains
"Standard input keeps an undecodable byte as an escape, so that the compute stream rejects only the
line that holds it (``compute.serve``)."; in `serve`, the first statement inside the `try`, before
`json.loads`, is `line = line.encode("utf-8", "surrogateescape").decode("utf-8")`, so a line that is
not UTF-8 gets the error reply `{"schema": "phonetic-mam-compute-v1", "error": {"type":
"UnicodeDecodeError", "message": "computation rejected"}}` and the next line is read; `serve`'s
docstring says so. Valid lines, the line splitting and the 16 Mi character limit are unchanged, and
an oversized request still ends the stream. `doc/phonetic-mam-compute.md:18` gains, after
"Non-finite numbers are not JSON input.": "A line that is not valid UTF-8 is rejected like any other
malformed request." No test covers `serve` and none is admissible; the executor runs, once, a scratch
script in `.novc/` that pipes `valid, 0xFF, valid` and `200 rejected lines, 0xFF, valid` into
`./.venv/Scripts/python.exe -B py/main_phonetic_mam.py compute` with `PYTHONUTF8=0`: before the fix,
exit 1 with no replies, then exit 1 after 115 replies; after it, exit 0 with 3 replies ending
`result, UnicodeDecodeError, result`, then exit 0 with 202. Then
`py/main_test.py py/tests/test_phonetic_compute_boundary.py py/tests/test_phonetic_untangler_preparation.py`.

**C15.18, `sys.dont_write_bytecode` set at import.** `py/main_phonetic_mam.py:17–18`,
`py/main_yeivin_itm.py:15–16` and `py/phonetic_mam/compute.py:11–12` set it at module level, so any
importer, among them the mega (`py/main_0_mega.py:74–75`) and pytest, stops caching bytecode for every
later import. Delete the three, and at the top of `main()` in each of the two entry points add:

```python
    # No command-line run writes import caches into either repository, as
    # doc/phonetic-mam-compute.md promises of compute. Set here, before almost_main
    # imports anything, rather than at import, so that an importer such as
    # py/main_0_mega.py keeps its own bytecode caching.
    sys.dont_write_bytecode = True
```

(in `main_yeivin_itm.py` the comment's first sentence reads "The check operation is write-neutral,
including Python import caches."). This also removes C9.2's eleven E402 at `compute.py:14–24`. Check:
a scratch probe that imports each module in a fresh interpreter prints `False` afterwards;
`./.venv/Scripts/python.exe -m ruff check --no-cache py/phonetic_mam/compute.py py/main_phonetic_mam.py py/main_yeivin_itm.py`
reports nothing; `py/main_test.py py/tests/test_yeivin_itm.py py/tests/test_product_scopes.py py/tests/test_mega_coverage.py py/tests/test_phonetic_untangler_preparation.py`.
Commit it with C13.1, which edits the same `main()`.

**C15.19, the exporter's error reporting, `py/phonetic_mam/exporter.py:85–120` and `:123–137`.** Both
adapter runs discard the adapter's stderr and wait without a limit; an adapter that dies early reports
only "source adapter ended early or exceeded its book limit" (the update's correction), and a hung one
blocks the export. Fix: keep a bounded tail of stderr in memory only (`_STDERR_TAIL_BYTES = 4096`,
drained by a daemon thread from `process.stderr.buffer`), so nothing that may quote private data is
written to disk; bound both runs at `_ADAPTER_TIME_LIMIT_SECONDS = 1800` (the whole export step took
229.2 seconds), by a watchdog timer for the streaming run and `subprocess.run(..., timeout=...)` for
the test-page run; and raise `display_schema.PublicReleaseError` with these messages, the tail
following each:
- "source adapter ended early or exceeded its book limit (exit status N); its stderr ended with:"
- "source adapter failed (exit status N); its stderr ended with:"
- "source adapter exceeded its 1800-second limit and was stopped (exit status N); its stderr ended with:"
- "test-page source adapter failed (exit status N); its stderr ended with:"
- "test-page source adapter exceeded its 1800-second limit and was stopped; its stderr ended with:"

with "(nothing)" for an empty tail; the `finally` block kills rather than terminates, since `wait()`
would otherwise be unbounded once the watchdog is cancelled. A successful export is byte for byte the
same. Check: a scratch fake adapter, substituted for `exporter._adapter_command` in memory with the
limit cut to 5 seconds, writes a traceback to stderr and either exits with status 3 (the error arrives
at once with the status and the tail) or sleeps (stopped at 5 seconds); then
`py/main_test.py py/tests/test_sibling_reach.py py/tests/test_phonetic_display_release.py`.

**C15.20, `py/phonetic_mam/test_page_display.py`, a production module named like a test.** It
defines the closed display format of the five public example pages. Rename it with
`git mv py/phonetic_mam/test_page_display.py py/phonetic_mam/example_display.py` and update its
importers: `py/phonetic_mam/release.py:6`, `:88`; `py/phonetic_mam/publication.py:4`, `:20`, `:24`;
`py/phonetic_mam/exporter.py:15`, `:162`, `:164`, `:166`, `:168`, `:169`, `:198`; and
`py/tests/test_phonetic_display_release.py:8`, `:34`, `:52`. `SCHEMA_ID` stays. Public evidence cannot
show whether the private adapter names the module, so right after the rename the executor runs
`./.venv/Scripts/python.exe py/main_phonetic_mam.py export`, a documented step that reads MAM-private
through the adapter, and requires `Phonetic-MAM/` to stay byte for byte; if the adapter fails on the
name, revert the rename and record C15.20 as `unresolved`, pending a change on the private side. Then
`git grep -n test_page_display` finds only the Claude report, a receipt;
`py/main_test.py py/tests/test_phonetic_display_release.py`; and `check` and `render` with no diff.

**C12.3, two untangler tests of shapes the repository does not allow,
`py/tests/test_phonetic_untangler_preparation.py`.** Remove the example-based fault-injection test
`test_preparation_rejects_unclassified_template_shapes` (`:64–79`); the closed dispatch's refusals are
explicit `raise` statements (`py/phonetic_mam/core/dualcant_templates.py:56–70`), and the roster
differential at `:32–40` keeps `_SHAPES` equal to the corpus's shapes. Replace
`test_preparation_operation_matches_direct_core_without_file_access` (`:43–61`), whose equality half
compares `compute.execute` with the very function that `compute._prepare_untanglers` returns
(`py/phonetic_mam/compute.py:152–154`), with `test_preparation_operation_runs_without_file_access`,
which denies `builtins.open` and `pathlib.Path.open`, runs `compute.execute` with `operation`
`prepare-untanglers` for every book, and checks that each reply encodes as `serve` encodes it,
`json.dumps(result, ensure_ascii=False, allow_nan=False)`. The module docstring becomes
"Corpus-shaped checks for the closed, file-free untangler preparation boundary." and the unused
imports go. The suite loses one test. Verification: Black;
`py/main_test.py py/tests/test_phonetic_untangler_preparation.py`, two passed.

**C15.11, `py/py_html/taamey_d_assets.py:34–40`.** `product_font_assets` hash-checks the font and the
source archive but checks the other support files only for being non-empty (`:39–40`, `:46–48`); a
scratch run accepted a one-byte change to each of them.
- Fix: add `import io`, `import zipfile`, `_ARCHIVED_COMPANIONS = ("FONT-NOTICE.txt", "GPL-2.0.txt",
  "SOURCE-INVENTORY.json", "BUILD.txt")`, and, commented as the two files that neither the archive
  nor the inventory records, `_UNARCHIVED_SHA256 = {"SOURCE.txt":
  "6e4497069cb52456348480bb75964019ae4cbcb0c4bbf839e8d24b9adc699c37", "PRODUCT-WOFF2-SOURCE.txt":
  "5da2baf9ac4cc80596e21149d8b876aecd5268376b6c98301167a2bbf233278f"}`. After the archive check,
  require each companion to equal its member `f"{_ARCHIVE.removesuffix('.zip')}/{name}"` of
  `zipfile.ZipFile(io.BytesIO(shared[_ARCHIVE]))`, raising "Taamey D {name} differs from its copy in
  the archive"; then check the two unarchived files, raising "Taamey D {name} differs from its
  recorded SHA-256". The non-empty checks become redundant and go.
- The check is the code itself: `product_font_assets` is the one gate for both publishers and for
  `py/main_yeivin_itm.py check`, and it already runs in the suite and in two mega steps. Scratch
  demonstration, not committed: copy `in/font-support/taamey-d-0.921/` and `doc/woff2/Taamey_D.woff2`
  to a scratch root, point `mb_cmn.paths.repo_root` at it in memory, append one byte to each of the
  seven inputs in turn (every one must raise), and confirm that the unaltered copy returns the same
  mapping as the tracked tree.
- Verification: `./.venv/Scripts/python.exe py/main_yeivin_itm.py check`;
  `./.venv/Scripts/python.exe py/main_phonetic_mam.py render` with no tracked diff;
  `py/main_test.py py/tests/test_yeivin_itm.py`.

**C15.12, `.gitattributes`.** The two copies of the source archive,
`in/font-support/taamey-d-0.921/Taamey_D-0.921-source-40115a364a4e.zip` and
`gh-pages/font-sources/taamey-d-0.921/Taamey_D-0.921-source-40115a364a4e.zip` (one blob, `7e6fa071`,
77,676 bytes), fall under `* text=auto eol=lf` (`:2`). After `MAM-parsed/historical/*.zip binary`
(`:33`) add `in/font-support/taamey-d-0.921/*.zip binary` and
`gh-pages/font-sources/taamey-d-0.921/*.zip binary`. In a scratch repository the stored blob stays
`7e6fa071`, and `git add --renormalize` stages nothing. Verification: `git check-attr binary diff
merge text -- <both zips>`; `git hash-object -- <both zips>` prints `7e6fa071…` twice;
`git add --renormalize -- <both zips>` then `git status --porcelain` shows only `.gitattributes`. A
configuration change, so it rides on the full suite.

**C12.1, `py/verify_mp/parser_stage.py:332–339`.** `_validate_no_parser_stage_encoding` asserts only
`"stmpl" not in node`. The parser stage also writes `{"tmpl": ...}` (`py/mb_cmn/ws_tmpl1.py:108–119`,
`simplify_wtel`) and `{"custom_tag": ...}` (`ws_abtag_parser.py:54`, `ws_plain.py:53`, `:55`, `:65`,
`:67`, `:113`; recognized by `ws_tmpl1.is_abtag`, `:87–89`). `node_type_and_subtype`
(`parser_stage.py:51–67`) admits a node only through `wtp1.is_template` (keys `tmpl` or `stmpl`,
`ws_tmpl1.dic_is_template`, `:54–56`) or `wtp1.is_abtag` (key `custom_tag`), and raises `TypeError`
otherwise, so those three keys are the complete set. In memory, Genesis plus with a `tmpl` node or a
custom tag injected into a column-E cell or into a template parameter passes the current check.
- Fix: add, above the function, a module constant with its reason, and test membership against it:

  ```python
  # The keys of every transient parser-stage node.  node_type_and_subtype admits a node only
  # through ws_tmpl1.dic_is_template, whose keys are the two template encodings ("tmpl" and
  # "stmpl", which ws_tmpl1.simplify_wtel writes), or ws_tmpl1.is_abtag, whose key is the
  # custom-tag encoding ("custom_tag", which ws_abtag_parser and ws_plain write).  Plus has
  # templates as {"tmpl_name": ..., "tmpl_params": ...} and no custom tag, so a dict in plus
  # with any of these keys is a parser-stage node that the conversion left behind.
  PARSER_STAGE_NODE_KEYS = frozenset({"tmpl", "stmpl", "custom_tag"})


  def _validate_no_parser_stage_encoding(node):
      if isinstance(node, dict):
          leaked = PARSER_STAGE_NODE_KEYS & set(node)
          assert not leaked, f"plus holds a parser-stage node: {node!r}"
          for value in node.values():
              _validate_no_parser_stage_encoding(value)
      elif isinstance(node, (list, tuple)):
          for item in node:
              _validate_no_parser_stage_encoding(item)
  ```
- Check: a new lint, `py/tests/test_parser_stage_node_keys.py`, reading source with `ast`: the
  top-level `if` tests of `node_type_and_subtype` call exactly `wtp1.is_template` and
  `wtp1.is_abtag`; the string constants in the single `return` of `ws_tmpl1.dic_is_template` and
  of `ws_tmpl1.is_abtag` (docstrings excluded) unite to `{"tmpl", "stmpl", "custom_tag"}`; that
  union equals `parser_stage.PARSER_STAGE_NODE_KEYS`; a missing function or a second `return`
  fails. No example-based injection test is added. Once, as a scratch check, inject each of the
  three encodings into a column-E cell and into a template parameter of in-memory Genesis plus:
  all six must raise and the unmodified plus must pass.
- Verification: Black; `py/main_test.py py/tests/test_parser_stage_node_keys.py`;
  `./.venv/Scripts/python.exe py/main_parse.py ws` with no tracked diff (`MAM-parsed/plus/` holds
  none of the three keys today); the final mega (the check runs inside the `parse-ws` step).

**C12.4, `py/accgram/post_stress_meteg_sources.py:116–143` (question 10).** `_written_stress_helpers`
skips every element that is not `מ:דחי` or `מ:צינור` without validating it, so an unknown template
passes silently. In `MAM-parsed/plus` at `644a6c9c` there are 2,373 stress helpers, all in column
E with parameters exactly {1, 2}: 2,305 at the top level and 68 nested, all in Psalms, Proverbs and
Job: in parameter 1 of `נוסח`, 37 `מ:דחי` and 2 `מ:צינור`, and 1 `מ:דחי` inside a `כו״ק`
parameter 2 there; in parameters `ד` and `ס` of `מ:קמץ`, 7 each; in parameter 2 of `כו״ק`, 6; in
parameters 1 and 3 of `מ:קו״כ-אם-2`, 4 each. Only one nested helper has a written form that
differs from its implicit qere, at Psalms 15:1 inside `נוסח`, and no survey record falls in that
verse. Of the survey's 378
`snapshot_before_qere` fields, 4 have a value and 374 are null, and a rebuild in memory under
either option below, and under the widest nested policy, leaves `out/accgram/post-stress-meteg.json`
byte for byte. `doc/PLAN-deferred-template-projection-decisions.md` (paused 2026-09-12) settles no
policy for this consumer and requires "an explicit, consumer-specific dispatch" (`:403–405`).
`py/mb_cmn/template_names.py` already has `CURRENT_PLUS_TMPL_NAMES`, `CURRENT_PLUS_PARAM_POLICY`
and `validate_current_plus_template` (`:133–306`), which raises on an unknown name or shape.

1. **Option 1 (recommended): close the dispatch and decline nested helpers explicitly.** Validate
   every top-level column-E template with `validate_current_plus_template`, index a top-level
   stress helper as today, and descend into no template, from a policy table that gives every name
   in `CURRENT_PLUS_TMPL_NAMES` an explicit entry:

   ```python
   # What this index does with each current plus template at the top level of a verse's E
   # cell.  It indexes a stress helper there and descends into no template: see
   # _snapshot_written_form for what that leaves out.  validate_current_plus_template raises
   # on a template outside CURRENT_PLUS_TMPL_NAMES or of another shape.
   _INDEX = "index this stress helper"
   _DO_NOT_DESCEND = "do not descend"
   _TOP_LEVEL_POLICY = {
       **{name: _INDEX for name in tmpln.STRESS_HELPER_TMPL_NAMES},
       **{
           name: _DO_NOT_DESCEND
           for name in tmpln.CURRENT_PLUS_TMPL_NAMES - tmpln.STRESS_HELPER_TMPL_NAMES
       },
   }
   ```

   The loop skips plain strings, calls `params = tmpln.validate_current_plus_template(element)`,
   looks the policy up by the name as that function normalizes it (ASCII `"` to U+05F4 HEBREW
   PUNCTUATION GERSHAYIM), continues on `_DO_NOT_DESCEND`, and keeps `written = params.get("2") or
   params["1"]`, the plain-text check and the ambiguity check. The docstring of
   `_snapshot_written_form` (`:105–111`), whose "never descends into documentation" misdescribes
   parameter 1 of `נוסח`, which is annotated Scripture, becomes:

   > Recover a diagnostic's written form from MAM's displayed stress helper.
   >
   > This index reads only the stress-helper templates, מ:דחי and מ:צינור, that stand at the
   > top level of a verse's E cell, and it reads their parameter 2, the form that has the
   > helper. It descends into no template: not into parameter 1 of נוסח, the Scripture that a
   > documentation note annotates; not into either alternative of מ:קמץ; and not into a
   > ketiv/qere template. So snapshot_before_qere exists only for a chanted word whose
   > stress-helper template is at the top level. On 2026-10-03, 68 of the 2,373 stress helpers
   > in MAM-parsed/plus were nested so. One of them, at Psalms 15:1, inside נוסח, has a written
   > form that differs from its qere, and no survey record falls in that verse.
   > The ordinary MAM spelling still supplies matching through the public qere rule below; the
   > stress-helper spelling is needed only for the diagnostic.

2. **Option 2: close the dispatch and index nested helpers under a named policy.** The walk
   descends only into named parameters, each the chanted word that the Phonetic MAM display has:
   parameter 1 of `נוסח` (never 2, the note); parameter 2 of `כו״ק`, `קו״כ` and `מ:כו״ק מיוחד`, the
   qere; parameter 1 of `מ:קו״כ-אם-2`, the pointed ketiv; parameter `ד` of `מ:קמץ`, the qamats-dal
   alternative the census selects (`py/accgram/post_stress_meteg_model.py:629–631`); a helper
   inside `מ:כפול` raises until a policy names its strand; every other template is not descended.
   A helper whose parameter 2 is a `מ:אות-מיוחדת-במילה` template (three, at Psalms 80:16, Proverbs
   1:1 and 28:17, none differing from its qere) takes that template's plain-text parameter 2. The
   docstring states the policy with Ben's decision and date. Today the only new index entry is
   Psalms 15:1, which matches no record.

Recommendation, option 1: it fixes the defect, the open dispatch, and makes today's behaviour
explicit and documented without new semantics; option 2 needs six container decisions and a
refusal for one unused index entry, and stays available later as the consumer-specific decision
that the deferred-projection plan prescribes.
- Verification: Black; `./.venv/Scripts/python.exe py/main_accgram.py survey-post-stress-meteg`, then
  `git diff --exit-code -- out/accgram/post-stress-meteg.json`;
  `py/main_test.py py/tests/test_prose_conventions.py py/tests/test_post_stress_meteg_annotations.py py/tests/test_post_stress_meteg_plain_word.py`;
  the final mega (the code runs in `accgram-survey-post-stress-meteg`). The regenerated survey is
  the test; the dispatch raises at every run.

**C9.1 and C9.5, the plain `shutil.rmtree` calls: they still need a handler after the relay is
retired.** Ben's decision 3 asks this plan to settle the point. Retiring the relay stops its two test
modules from adding read-only Git objects under `.novc/t`, but it removes neither the read-only
files already there (on `LAPTOP-DBLE8UKA` on 2026-10-03: 1,199 in `GitRepos/MAM-basics`, 280 in
`GitRepos2/MAM-basics` and 1,879 in `GitRepos3/MAM-basics`, every one in a relay test's directory)
nor the other source: an agent's scratch Git repository in a `.novc`, of which
`GitRepos/MAM-basics/.novc` holds four with 230 read-only files. No other default-suite test writes
a Git object, and pytest writes no read-only file. So the next wipe in every clone would still stop.
- Fix: one shared handler in `py/repo_util/common.py` (add `import os` and `import stat`):

  ```python
  def clear_read_only_and_retry(function: Any, path: str, exc: BaseException) -> None:
      """``shutil.rmtree``'s ``onexc`` handler for read-only files.

      Git writes its object and pack files read-only, and Windows refuses to delete
      a read-only file, so a plain ``rmtree`` stops partway through any tree that
      holds a Git repository.  This clears the attribute and retries the one failed
      removal.  Any other failure, and a retry that fails again, propagates.
      """
      if not isinstance(exc, PermissionError) or function not in (os.unlink, os.rmdir):
          raise exc
      os.chmod(path, stat.S_IWRITE)
      function(path)
  ```

  `py/main_repo_maintenance.py:140` becomes `shutil.rmtree(novc, onexc=clear_read_only_and_retry)`
  and `py/repo_util/worktree_retirement_relocation.py:132` becomes
  `shutil.rmtree(source, onexc=clear_read_only_and_retry)`, each importing the handler from
  `repo_util.common`. `onexc` needs Python 3.12; the environment runs 3.13.15 and the code already
  needs 3.12 (`Path.is_junction`, `ruff.toml`'s `py313`). And `main()` (`:218–219`) guards the wipe,
  so that one failure no longer stops the other steps, as the module docstring's "Seven independent
  steps" says:

  ```python
      if not args.skip_novc:
          try:
              clean_novc()
          except OSError as exc:
              print(f"MAM-basics .novc: FAILED ({exc})")
              ok = False
  ```
- The lint that pins the call's form, `py/tests/test_worktree_retirement_policy.py:143–165`, now
  refuses any keyword (`:155`, `not node.keywords`). In the same commit, it admits exactly one keyword,
  `onexc`, whose value must resolve to `repo_util.common.clear_read_only_and_retry` (a new
  `_READ_ONLY_RETRY` constant, resolved through the module's existing `_qualified_name`), with the
  comment: "Git writes object and pack files read-only, which Windows will not delete, so the one
  admitted keyword is the shared handler that clears that attribute and retries; ignore_errors,
  onerror and any other handler stay refused."
- Check for C9.5: the on-demand differential simulation `py/repo_util/worktree_retirement_simulation_test.py`
  gains one read-only input: in `add_novc` (`:133–139`), after the nested file is written, add
  `os.chmod(source / "evidence.bin", stat.S_IREAD)` with the comment "Git writes object and pack
  files read-only; Windows refuses to delete them." (and `import stat`). Its oracles stay Git's
  registration and branch state, the retained bytes and the sidecar inventory. On scratch copies,
  before the fix its cross-volume case failed with "[WinError 5] Access is denied" and after it
  both cases passed. This is a changed input to an existing differential check, not a new test.
- Check for C9.1: the lint; and once, as a scratch demonstration that is not committed, copy a relay
  test's leftover directory into a scratch `.novc` and run `_clean_one_novc` on it before and after
  the fix. **Never verify by running the wipe in a real clone:** `GitRepos2/MAM-basics/.novc/review-2026-09-29/`
  is cited by tracked records (`doc/dual-agent-review-2026-09-29-turn-01-claude.md:45`, `:1442`,
  and turns 07, 09 and 10), and the wipe is a destructive local act.
- Verification: Black; `./.venv/Scripts/python.exe -m ruff check --no-cache py`;
  `py/main_test.py py/tests/test_worktree_retirement_policy.py`;
  `./.venv/Scripts/python.exe py/main_test.py py/repo_util/worktree_retirement_simulation_test.py`,
  the whole module, which must pass; the full suite.

**C9.2, ruff's 17 errors.** `./.venv/Scripts/python.exe -m ruff check --no-cache py` (ruff 0.16.5,
configured in `ruff.toml`, which has no per-file ignores) reports at `644a6c9c`: eleven E402 at
`py/phonetic_mam/compute.py:14–24`; F401 at `py/phonetic_mam/core/resolve_generic.py:3`,
`py/tests/test_phonetic_compute_boundary.py:4`, `py/yeivin_itm/content/my_yeivin_sec_318.py:2` and
`my_yeivin_sec_388.py:3`; F541 at `py/yeivin_itm/content/my_yeivin_amisc_helpers_private.py:212`; and
F841 at `py/tests/test_dual_agent_review_dispatch.py:805`. Dispositions:
1. F841 goes with the relay's test module (R1).
2. Delete `py/phonetic_mam/core/resolve_generic.py:3` (`import phonetic_mam.core.udl_char_classes as cc`,
   unused there) and `py/tests/test_phonetic_compute_boundary.py:4` (`from pathlib import Path`).
   `resolve_generic.py` is phonetic core code that mega steps import, so this rides on the final mega,
   which must show no diff.
3. The eleven E402 vanish with C15.18, which moves `sys.dont_write_bytecode` out of `compute.py`'s
   module level; no ignore is added.
4. The three content-module errors are fixed after question 8 (C6.2) is settled, in the form that
   question's answer prescribes for editing the adaptation: `my_yeivin_amisc_helpers_private.py:212`
   `return aht_html.anchor(f"#", attr)` becomes `return aht_html.anchor("#", attr)`, and the unused
   imports `my_yeivin_sec_318.py:2` (`import yeivin_itm.helpers as hlp`) and `my_yeivin_sec_388.py:3`
   (`import mb_cmn.str_defs as sd`) are deleted. Under options A and C nothing else changes; under
   option B each becomes an approved edit, re-pinned at the hashes the executor computes. The pages
   must stay byte for byte.
- Verification: ruff prints "All checks passed!" once the relay's module is gone and C15.18 and
  question 8's edits have landed;
  `py/main_test.py py/tests/test_phonetic_compute_boundary.py py/tests/test_yeivin_itm.py`.

**C9.3, the synchronize form refuses the calling session's own clone.** `runtime_facts`
(`py/repo_util/worktree_owners.py:74–82`) counts every `~/.claude/sessions/*.json` record whose `cwd`
is in a clone as a blocker, so the write form of `--sync-forest` (`py/repo_util/forest_sync.py:250–261`)
refuses the clone the calling Claude session is in, and every refusal is a problem (`:322–332`). The
update's correction holds: a Codex task blocks only while its writer lock exists. Claude Code gives
its tool processes `CLAUDE_CODE_SESSION_ID` and `CLAUDE_PID`, which equal the session record's
`sessionId` and `pid` (verified for this session; not verified for the CLI entry point, the cloud or
Codex).
- Fix: a function `_calling_session_blocker(repo)` returns the blocker string `runtime_facts` gives
  for the calling session's own record, `f"running Claude session {session}"`, only when both
  variables are set and one record matches both with its `cwd` in the clone, and `None` otherwise or
  on any read error; in the write form, when the clone's blockers are exactly that one string, print
  the clone's usual `FOREST_REPO:` line and `FOREST_REPO_SKIPPED: <repo>: the calling Claude session's
  own clone; not fetched; checkout and environments left untouched`, and return success without
  fetching. Any second session, lease or worktree occupancy keeps the refusal. The module docstring
  gains: "A clone that only the calling Claude session occupies is not refused: a write skips it
  unfetched and does not count it as a failure, since that session updates its own checkout."
- Documentation: `doc/clone-forests.md`, after `:44`:

  > One occupied clone is skipped rather than refused: the clone that only the calling Claude
  > session occupies. The write form recognizes that session when the `CLAUDE_CODE_SESSION_ID` and
  > `CLAUDE_PID` variables that Claude Code gives its tool processes match the `sessionId` and `pid`
  > of a session record whose working directory is in the clone. The write form reports that clone
  > as `FOREST_REPO_SKIPPED`, leaves it unfetched and untouched, and does not count it as a problem,
  > so the command exits 0 when every other clone succeeds. The session updates its own clone with
  > ordinary Git. Any other session, lease or worktree occupancy in the same clone keeps the
  > refusal.

  and in the runbook `doc/PLAN-repo-maintenance-across-GitRepos.md`, its `--sync-forest` row
  (`:383`), insert " skips, unfetched, a clone that only the calling Claude session occupies;" after
  "an ahead or diverged clone after fetching it;". `doc/PLAN-checkout-kinds-and-portable-knowledge.md:318–319`
  is an executed receipt and stays.
- Check: no admissible new test exists. Scratch demonstration, not committed: a bare origin, one
  clone and a fake home holding one session record; the current code refuses, the new code prints
  `FOREST_REPO_SKIPPED` and writes no `FETCH_HEAD`, and it refuses as today when `CLAUDE_PID`
  differs, when both variables are unset, or when a second session's record is added.
  `py/main_test.py py/tests/test_forest_subprocess_bounds.py` must pass on the new `forest_sync.py`.
  Do not run the write form against a real forest without Ben's authorization.

**C9.4, the forest launch lint, `py/tests/test_forest_subprocess_bounds.py`.** It tests that a bound
keyword is present (`:101–103`, `:117–118`, `:121–123`), so `timeout=None` passes, and
`_imported_names` (`:56–58`) skips a relative import's level, against the docstring's `:19–22`.
- Fix:
  1. **Values.** A `timeout=` or `timeout_seconds=` value must be a positive `int` or `float` literal
     (not `True`), or a name or module attribute bound at the top level of a module under `py/` only
     to such literals (so `GIT_TIMEOUT_SECONDS = 60` counts and a name later rebound to `None` does
     not); `noninteractive=` must be the literal `True`; `env=` must not be the literal `None`. Each
     launch that the scan records is then checked.
  2. **Relative imports.** Resolve `ImportFrom.level` against the scanned file's package
     (`py/repo_util/forest_sync.py` is in `repo_util`), including `from . import m`.
  3. **More launchers refused:** `os.startfile`, `os.posix_spawn*`, `os.fork*` and `asyncio`'s
     `create_subprocess_*`, beside today's `os.system`, `os.popen`, `os.spawn*` and `os.exec*`.
  4. **The docstring** states the value rules and names the limits it keeps: a call through a local
     alias or a `functools.partial` object, and a launch inside a function of a module the lint does
     not list.
- Check: the lint is the check. On the real tree, today's and the new lint both find 22 launches in
  `forest_sync.py` and 8 in `forest_environments.py`, with no problem. Scratch synthetic sources,
  not committed: `timeout=None`, `timeout_seconds=None`, `noninteractive=False`, `env=None`,
  `timeout=-1`, `timeout=True`, a constant rebound to `None`, the two relative-import forms without a
  bound, and the four new launchers must each be flagged; a literal `timeout=5`,
  `GIT_TIMEOUT_SECONDS` and `fe.GIT_TIMEOUT_SECONDS` must pass.
- Verification: Black; `py/main_test.py py/tests/test_forest_subprocess_bounds.py`.

**C15.3 and C15.4, standard streams.**
- C15.3: `py/main_diff.py`'s `main()` (`:49–50`) reconfigures neither stream, and
  `py/main_sigil_inventory.py` reconfigures stdout in `almost_main()` (`:9`) and not stderr. Each
  `main()` gets, first, `sys.stdout.reconfigure(encoding="utf-8")` and
  `sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")`, and the stdout line moves out
  of `main_sigil_inventory.almost_main`; the mega, which calls both `almost_main`s after its own
  `force_utf8_io()`, is unaffected.
- C15.4: in the eleven programs of `33470e2d`, `sys.stderr.reconfigure(encoding="utf-8")` resets
  stderr's error handler from `backslashreplace` to `strict` (demonstrated on Python 3.13.15 with and
  without UTF-8 mode). Replace that line with
  `sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")` in: `py/check_escape_sequences.py:91`,
  `py/check_mark_order.py:49`, `py/check_qr_relations.py:31`, `py/check_spelling_in_html.py:266`,
  `py/main_authored.py:275`, `py/main_explicit_xataf.py:133`, `py/main_foi_features_of_interest.py:109`,
  `py/main_gen_misc_authored_english_documents.py:30`, `py/main_mam_simple.py:353`,
  `py/main_mam_with_doc.py:67` and `py/main_tmpl_survey.py:168`.
- Several of these run inside mega steps, so they ride on the final mega, which must show no diff.
  Verification: Black; ruff; `./.venv/Scripts/python.exe py/main_diff.py --help`.

**C15.28, abbreviated long options in the retirement lint, `py/tests/test_worktree_retirement_policy.py:29–36`.**
Git reads `--f` to `--forc` as `--force` for `git worktree remove`, and `--d` to `--delet` as
`--delete` and `--forc` as `--force` for `git branch` (Git 2.53.0); the lint compares whole tokens,
so `worktree remove --f` and `branch --del` escape it. Fix:

```python
def _long_option(token, option):
    """Whether Git reads ``token`` as the long ``option``.

    Git accepts the whole name or any prefix that no other option of the command
    shares: ``git worktree remove`` reads ``--f`` to ``--forc`` as ``--force``, and
    ``git branch`` reads ``--d`` to ``--delet`` as ``--delete`` and ``--forc`` as
    ``--force``.  A prefix that Git finds ambiguous is refused here as well.
    """
    return (
        isinstance(token, str)
        and len(token) > 2
        and token.startswith("--")
        and option.startswith(token)
    )


def _forces(token):
    """--force or an abbreviation of it, or a short-option cluster holding f or D."""
    return _long_option(token, "--force") or bool(_short_options(token) & {"f", "D"})


def _deletes_branch(token):
    """--delete or an abbreviation of it, or a short-option cluster holding d or D."""
    return _long_option(token, "--delete") or bool(_short_options(token) & {"d", "D"})
```

On the real tree the lint's result is unchanged. Verification:
`py/main_test.py py/tests/test_worktree_retirement_policy.py`, in the same commit as C9.1's change to
the same file's other hunks.

### Editorial proposals: agent instructions and skills (D7: editorial)

**C15.23, `AGENTS.md:241–250`.** The pointer "`doc/agent-planning-principles.md`, “Generated Outputs
Are the Tests”, carries the dated evidence and rationale." follows both test exceptions and reads as
covering them, but that section records neither: the `ws_bot` exception rests on its own sentence
and the test docstrings, and the special-page exception on Ben's decision of 2026-09-30, which
`doc/dual-agent-review-2026-09-29-turn-01-claude-update.md` records under "Ben's decisions and
approval of the package, 2026-09-30", item 1. Proposed, the section's body:

> Follow the common instruction body's “Tests are differential or lint-shaped” rule.
> `doc/agent-planning-principles.md`, “Generated Outputs Are the Tests”, carries that rule's dated
> evidence and rationale. The `ws_bot` tests remain a deliberate exception because a live
> Wikisource edit is an outward-facing act with no regeneratable artifact. By Ben's decision of
> 2026-09-30, which `doc/dual-agent-review-2026-09-29-turn-01-claude-update.md` records under
> “Ben's decisions and approval of the package, 2026-09-30”, the five stub test ids of
> `py/tests/test_wikisource_special_page_download.py` are a second exception. Its four
> fault-injection ids hold five cases: each checks that a bad API response or bad local metadata
> makes the special-page download raise, and all but the last, a manifest overwritten with "not
> json", also check that no mirrored file changed, a property with no regeneratable artifact. Its
> round trip is the only offline check of the download's reuse and forced refresh, neither of
> which a regenerated mirror's diff would show.

`AGENTS.md` stays far under Codex's `project_doc_max_bytes` of 32,768 bytes (15,783 bytes at
`644a6c9c`). It takes effect when committed.

**C10.3, `hebrew-prose`.** `references/sources-and-corpora.md:68–75` says the 2026-10-01
"evacuation work branch moves this selected source and its renderer to MAM-basics; / the old
`MAM-private/al-hatorah/py/itm/` copy remains until the later retirement / gates pass", while
`doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md:387–392`, "D5 superseded,
2026-10-02", records that private integration `5c526cac` "removed the duplicate adaptation after the
consumer gates passed". Proposed bullet:

> - `MAM-basics/py/yeivin_itm/content/` — Ben's **partial adaptation**;
>   `my_yeivin_amisc_sec_not_yet_transcribed.py` names what is missing. The 2026-10-01
>   evacuation moved this selected source and its renderer to MAM-basics. The old
>   `MAM-private/al-hatorah/py/itm/` copy is gone: MAM-basics'
>   `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md`, “D5 superseded,
>   2026-10-02”, records that private integration `5c526cac` removed that duplicate adaptation
>   after the consumer gates passed. Neither change moved or replaced the full OCR above.
>   Historical `al-hatorah#NN` citations keep their original tracker. The adaptation's body text
>   is Yeivin's and Revell's, **not Ben's voice** (his footnotes in it are his) — exclude it when
>   treating "Ben's own writing" as a style corpus.

In `references/mam-basics.md:30–40`, the count of al-hatorah citation sites is staler than the
update says: `9a67d51b` rewrote the docstrings of five of the eight sites (`breuer_word_length.py`
three times, `post_stress_meteg.py` and `py/tests/test_final_stress_vs_phonetic_mam.py`), and three
remain, the literal ones. Replace "Those historical source citations remain as written." with:

> On 2026-10-01 `9a67d51b` rewrote the docstrings that held the other five, when the Breuer and
> post-stress-meteg analyses and the final-stress test moved to the public Phonetic MAM release.
> The three that remain are `chanted_word_accents_inventory.py`'s `../al-hatorah/py/itm/`,
> `final_stress.py`'s `../al-hatorah/py/aht_phon` and `maqaf_nonfinal_accents.py`'s
> `../al-hatorah/py/aht_phon/stress.py`; the adaptation the first names is now MAM-basics'
> `py/yeivin_itm/content/`. Those historical source citations, and the eight masorah-books ones,
> remain as written.

**C15.24, `mam-repository-topology`'s `references/evacuated-repositories.md`.** The five clone
commands in `powershell` fences that write `<forest>/...` (`:61`, `:111`, `:141`, `:206`, `:226`) do
not parse in PowerShell 7 ("The '<' operator is reserved for future use."), and the phonetic-hbo
block (`:296–300`) clones to the relative `../phonetic-hbo`. Ben approved the `<forest>` wording on
2026-09-30 (`1c0cf3f8`, the September 29 round's finding 28.3), so this replacement is for his
approval: in the five commands `<forest>/` becomes `$HOME/GitRepos/`, for example
`git clone --depth 1 https://github.com/bdenckla/wlc-utils.git $HOME/GitRepos/wlc-utils`; the
explanation at `:64–67`, "In this command and the four below, `<forest>` is the directory holding the
invoking checkout's home clone, `$HOME/GitRepos` or `$HOME/GitRepos<N>`, which is where …", becomes
"This command and the five like it below clone into the primary forest, `$HOME/GitRepos`. From a
checkout whose home clone is in a secondary forest, write that forest instead, for example
`$HOME/GitRepos2`. The forest holding the invoking checkout's home clone is where
`py/redirect_stubs/stubs.py`'s `source_pages_dir` looks, through `paths.sibling_repo`; the program's
own message prints the exact path."; and `:296–301` becomes "Only explicitly selected redirect-stub
publication uses a temporary shallow clone, a sibling of the selected MAM-basics full clone; from a
secondary forest, write that forest in place of `$HOME/GitRepos`:" with the fenced command
`git clone --depth 1 https://github.com/bdenckla/phonetic-hbo.git $HOME/GitRepos/phonetic-hbo`.
Verification: each of the six commands parses with
`[System.Management.Automation.Language.Parser]::ParseInput` with no error.

**C15.25, `github-issues`' `references/mam-basics-trackers.md` (question 11).** The section is named
"## Five issue trackers: a bare `#NN` here means MAM-basics" (`:6`) and explains at `:121–126` why the
count stays five ("settled 2026-08-27, Ben having deferred the framing"); the routing section that
`d0c660c9` added on 2026-10-02 (`:204–212`) routes two more trackers, phonetic-hbo's and
masorah-books'. The update's note says the count "is a framing Ben chose on 2026-08-27"; the
section itself and `97b559b0`'s message say Ben deferred it and that session kept "Five". Ben
decides now:

1. **Option 1 (recommended): keep "Five".** Insert before "**This section has had four names.**"
   (`:129`):

   > **Two trackers added since are routed below, not counted here.** The 2026-10-01 evacuation of
   > the public Phonetic MAM and Yeivin ITM products left phonetic-hbo's and masorah-books' existing
   > issues in their own trackers, as the four moves above left theirs. The section “Phonetic MAM
   > and Yeivin ITM tracker routing after evacuation”, added on 2026-10-02, routes them and records
   > no number collisions for them. By Ben's decision of <date>, this section's name still counts
   > the five settled on 2026-08-27.
2. **Option 2: rename to "Seven issue trackers".** `:6` becomes "## Seven issue trackers: a bare
   `#NN` here means MAM-basics"; `:98–99` ends "…by transfer, and this section's count leaves them
   out.**"; `:121–126` says the count leaves the emptied five out because it counts the trackers
   whose issues stay put, now including phonetic-hbo and masorah-books, and that the count rose to
   seven by Ben's decision of <date>; `:129–131` becomes "**This section has had five names.** …
   "Five issue trackers" until <date>, and "Seven issue trackers" since."; and two conforming edits
   follow: `py/github_issue_edit.py:32`, "the five trackers", becomes "the seven trackers", and
   `doc/dual-agent-review.md:814–817`'s precedent becomes "… kept “Five issue trackers” after five
   more trackers were consolidated into it, with an explicit note recorded so a rename was not
   re-proposed; it became “Seven issue trackers” on <date> only when two trackers that it counts
   joined."

Recommendation, option 1: one paragraph against four passages in three files, and it keeps true
both the section's "four names" history and `doc/dual-agent-review.md`'s precedent, which cites this
very section. Option 2 matches the section's own criterion, trackers "whose issues stay put", which
both new trackers meet.

The three skills take effect when deployed (act A3).

**C7, `py/ws/pywikibot-setup.md:72–77`.** Current:

> For process/idempotence checks, use `--identity-run`:
>
>        .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --identity-run
>
> `--identity-run` does **not** save live pages. It processes chapters and
> fails at the end if any chapter text would change.

In `py/subcommands/ws_bot_real.py`, `--identity-run` loads no edits (`:52–59`, "null bot: no
processing and no saves") and gives each page back its own text (`:102–103`); `--no-save` applies
the edits, records each chapter that would change (`:106–115`) and, after the last chapter, exits
1 with "no-save run found chapters that would change" (`:85`, `:130–139`). Both modes turn off the
post-run download (`:46–51`, `:86`). Of the six edit kinds (`py/ws/ws_bot_edit.py:78–100`), three
leave their own output unchanged (`kq-trivial-to-kq-trivial-2`, `kq-trivial-2-rename-extra-alef-sug`,
`kuk-special-callsite-migration`) and three are one-shot (`meteg-removal` and `explicit-replacement`
require each `old` to occur exactly once, `:206–212`; `sigil-b2-to-t451` requires a per-chapter
count, `ws_bot_edit_sigil_b2_to_t451.py:93–97`). Proposed, replacing `:72–77`:

> ## Dry runs before a save
>
> Neither `--no-save` nor `--identity-run` saves a live page, and each turns
> off the post-run download.
>
> `--no-save` is the dry run for an edit file. Give it the edit file and the
> selector that the save will use:
>
>        .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --no-save
>
> It fetches every selected chapter, applies the edits in memory, writes each
> resulting chapter to the run's `chapters/` directory, and saves nothing.
> Before a save it is expected to exit non-zero: after the last chapter it
> stops with "no-save run found chapters that would change" and lists each
> chapter that the save would change. That list should name exactly the
> chapters that the edit file targets. Any other failure, such as an
> `AssertionError` from an edit's guard or "Selector includes chapters outside
> this edit spec target set", must be resolved before saving. An exit of zero
> before a save means that no selected chapter would change, so the edit file
> or the selector is wrong.
>
> Run again after the save, with the same edit file and selector, `--no-save`
> checks idempotence only for an edit kind that is idempotent, one that leaves
> its own output unchanged: `kq-trivial-to-kq-trivial-2`,
> `kq-trivial-2-rename-extra-alef-sug` and `kuk-special-callsite-migration`.
> For those kinds an exit of zero confirms that every selected chapter already
> has the edited text. The other kinds are one-shot. `meteg-removal` and
> `explicit-replacement` require each `old` string to occur exactly once, and
> `sigil-b2-to-t451` requires a per-chapter count of the old sigil, so after
> the save a re-run fails at the first chapter whose guard it checks. That
> failure shows that the old text is gone, not that the saved text is right;
> compare the saving run's `chapters/` files with the dry run's instead.
>
> `--identity-run` is a null bot. It reads no edit file, although the parser
> still requires `--edits`; it gives each selected chapter back its own text
> and saves nothing, so it cannot fail on a change. Use it only to exercise a
> run's plumbing: the pywikibot configuration, the selector, the page reads
> and the run's artifact directory.
>
>        .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --identity-run

The refresh skill's routing line (`dot-claude/skills/mam-wikisource-refresh/SKILL.md:128–130`) stays
true and needs no edit. Verification: `git diff --check` and a reading of the section.

**C8, `dot-claude/skills/mam-wikisource-refresh/references/dependent-refresh.md` steps 4 and 5
(question 9).** Step 4 (`:55–65`) runs the mega and says "Audit every diff and commit explained
dependent changes."; step 5 (`:67–82`) runs `py/main_diff.py mpplus --all`, then
`py/main_diff.py mpplus --check`, and says "If book data changed but no change-log diff results, stop
and resolve the discrepancy." The mega's `diff-mpplus` step (`py/main_0_mega.py:283–287`) runs
`diff_mpplus.run_all`, which rewrites `unpinned-latest.html`, `unpinned-latest.json` and `index.html`
under `gh-pages/MAM-with-doc/change-log/` from committed `HEAD` (`py/subcommands/diff_mpplus.py:281–339`),
so after step 1's commit, step 4's mega writes the change-log diff, and step 4's instruction commits
it. `--check` cannot be combined with `--all` (`:554–568`), and it compares a regeneration with the
working-tree copies, so it cannot show that a log is committed. Ben chooses:

1. **Option 1 (recommended): step 4 holds the change log back.** In step 4, replace the paragraph
   from "The exporter is the routine public pipeline's only private dependency." to "stop the
   workflow." with:

   > The exporter is the routine public pipeline's only private dependency. Phonetic rendering,
   > both meteg surveys, the Breuer survey and the Yeivin claims/rendering consume public data.
   > The mega's `diff-mpplus` step rewrites the MAM change log under
   > `gh-pages/MAM-with-doc/change-log/` from committed `HEAD`, which now includes step 1's
   > commit, so this run leaves the change-log diff that step 5 audits and commits. Audit every
   > other diff and commit the explained dependent changes, leaving every path under
   > `gh-pages/MAM-with-doc/change-log/` uncommitted for step 5. Failed gates, stale inputs and
   > unexplained output changes stop the workflow.

   In step 5, replace "Audit every change-log diff; named historical-release reports must remain
   unchanged." with:

   > This rewrites the change log from committed `HEAD`, so it reproduces what step 4's mega
   > left uncommitted. Audit every change-log diff; named historical-release reports must
   > remain unchanged. In an ordinary refresh only `unpinned-latest.html` and
   > `unpinned-latest.json` change, with `index.html` when the count of unreleased changes
   > moves.

   The stop rule, the commit sentence and `SKILL.md` stay as they are. C1.3's pointer to "Gates that
   a text change can trip" joins the new paragraph's last sentence, as it would today's.
2. **Option 2: accept a log already committed at step 4.** In step 4, replace "Audit every diff
   and commit explained dependent changes." with "Audit every diff and commit explained dependent
   changes. The mega's `diff-mpplus` step rewrites the MAM change log under
   `gh-pages/MAM-with-doc/change-log/` from committed `HEAD`, which now includes step 1's commit;
   commit that change-log diff separately, as `Regenerate MAM change logs`." Retitle step 5
   "**Confirm change logs from final committed public data.**", keep its two command blocks, and
   replace its last paragraph with: "If `--all` left a change-log diff, commit the audited logs
   separately as `Regenerate MAM change logs` and repeat the freshness guard. If it left none and
   the guard passes, the change log is already committed when a commit made since the starting
   `HEAD` changed `gh-pages/MAM-with-doc/change-log/unpinned-latest.json`, which
   `git -C <DEV> log --format=%H <starting HEAD>..HEAD -- gh-pages/MAM-with-doc/change-log/unpinned-latest.json`
   shows. If book data changed and that command prints nothing, stop and resolve the discrepancy.
   Do not create an empty commit." `<starting HEAD>` is the commit that `SKILL.md`'s "Verify the
   checkout", item 2, records.

Recommendation, option 1: it changes the fewest instructions, keeps step 5 the one place where the
change log is generated, audited and committed, and keeps its stop rule a plain working-tree
observation; option 2 must replace that rule with a history query. The skill takes effect when
deployed (act A3), and C1.3 edits the same file. Verification: `git diff --check`.

### Editorial proposals: procedure documents and records (D7: editorial)

**C10.2, `doc/phonetic-mam-preparation.md`**, a maintained document with no State line. Proposed:
`:7–8`, "Site deployment and live URL verification remain separate publication steps.", becomes "The
Pages run for `38c0116f`, a descendant of that merge, deployed the generated site; it finished at
15:39:45 New York time on 2026-10-01."; `:51–52`, "These results verify the integrated local pages;
live deployment still requires its own checks.", becomes "These results verify the integrated local
pages, not the deployed site."; `:77–79`, "Both targets are on integrated `main`; target deployment
and the coordinated legacy redirect cutover remain separate steps.", becomes "Both targets are on
integrated `main`, and the Pages run for `38c0116f` deployed them on 2026-10-01. The coordinated
legacy redirect cutover followed that day: phonetic-hbo's redirects, from its commit `2ca51088`,
deployed at 17:10:52 New York time." No tracked record shows a live URL check of the deployed site,
so none is claimed.

**C15.2, a retired document cited without an archive link.** `e4934b6e` retired
`doc/PLAN-symmetric-CLAUDE-and-AGENTS-instructions.md` and its update; its parent `eea4c583` holds
both (`git cat-file -e` succeeds for each).
- `doc/user-wide-instruction-conversion-reconciliation.md:90`, a maintained document, in place:
  "The symmetric-instructions plan's update records this later result." becomes "The archived
  [symmetric-instructions plan's update](https://github.com/bdenckla/MAM-basics/blob/eea4c583f12ee90f75003dd4c75be5d6d52f7c85/doc/PLAN-symmetric-CLAUDE-and-AGENTS-instructions-update.md),
  which `e4934b6e` retired on 2026-09-29, records this later result."
- `doc/PLAN-remediate-review-findings-2026-09-26.md`, a receipt (`:621–622`, "Change the
  symmetric-plan update's own `State: executed`…", and `:728–729`, "Use existing updates for
  September 10/14/16 review families, symmetric instructions, …"): its update,
  `doc/PLAN-remediate-review-findings-2026-09-26-update.md`, whose one entry (written by `e4934b6e`)
  links the September 14 and 16 families but not this one, gains a dated entry:

  > ## <YYYY-MM-DD>: the archived symmetric-instructions family
  >
  > Recorded by <agent> on <YYYY-MM-DD>, New York time, under the approved remediation plan for the
  > 2026-10-02 review (its item C15.2). The base plan's passages beginning “Change the symmetric-plan
  > update's own `State: executed`” and “Use existing updates for September 10/14/16 review families,
  > symmetric instructions,” refer to the symmetric-instructions plan's update. `e4934b6e` retired that
  > plan and its update from the tracked tree on 2026-09-29, and the entry above, written in the same
  > commit, gave archive links for the September 14 and September 16 remediation families only. The
  > symmetric-instructions family remains at these immutable locations:
  >
  > - [symmetric-instructions plan](https://github.com/bdenckla/MAM-basics/blob/eea4c583f12ee90f75003dd4c75be5d6d52f7c85/doc/PLAN-symmetric-CLAUDE-and-AGENTS-instructions.md)
  >   and its [update](https://github.com/bdenckla/MAM-basics/blob/eea4c583f12ee90f75003dd4c75be5d6d52f7c85/doc/PLAN-symmetric-CLAUDE-and-AGENTS-instructions-update.md).

**C15.13, `doc/mam-normal-mark-order.md`.** Its list of byte-verbatim captures (`:42–48`) lacks the
dagesh discussion's capture, whose 5 clusters (one at capture line 11, four at line 22, each with
the dagesh after its vowel) are the window's only ones out of MAM-normal order. No test enumerates
the captures (`py/tests/test_prose_mark_order.py:108–111`, `:128–137`). Add after `:48`:

> `doc/wikisource-dagesh-discussion-2026-10-01.mediawiki` is another capture tracked after that
> scan: the exact UTF-8 section text that the MediaWiki revisions API returned on 2026-10-01 for a
> Hebrew Wikisource Village Pump discussion, with 5 clusters in the other order. Its translation,
> `doc/wikisource-dagesh-discussion-translation.md`, says not to reorder the capture's marks, and
> gives its own Hebrew examples in MAM-normal order.

Found while planning, and approved by Ben on 2026-10-03: the same list also lacks
`in/mam-ws-special/`, the declared special pages that every chapter download mirrors byte for byte,
added on 2026-09-27 with 5,369 clusters in the other order in 25 of its 36 `.mediawiki` files; it did
not change in the window. Add: "`in/mam-ws-special/`, the declared special pages that every
Wikisource chapter download mirrors byte for byte, was added 2026-09-27 with 5,369 clusters in the
other order in 25 of its 36 `.mediawiki` files."

**C15.29, two Holman research records edited in place, and a missing "Recorded by" (question 12).**
On 2026-10-01 `cb5bcda1` rewrote the last sentence of `holman/doc/holman-manuscript-citations.md`
(`:178–179`) and the method sentence of `holman/doc/uxlc-email-count-disagreements.md` (`:178–179`) to
name "a full MAM-basics clone" instead of a path in the primary forest, wording Ben selected that day
("All 30 files (Recommended)", `doc/dual-agent-review-2026-09-29-turn-01-claude-update.md:1540–1547`).
Both records are dated ("Measured 2026-08-12"), have no State line and no update, and were edited in
place before as well (`9eedccbd` on 2026-09-07, both; `73ab8383` on 2026-09-09, the second).
`hebrew-prose`'s `references/terminology.md:460–461` calls "the dated Holman research records under
`holman/doc/`" receipts. Whether they are receipts is Ben's decision:

1. **Option 1 (recommended): they are receipts.** In each base, join the line-3 paragraph into one
   physical line 3 without changing its text and insert the line-4 pointer ("Updates and later
   status: [holman-manuscript-citations-update.md](holman-manuscript-citations-update.md)." and
   "Updates and later status: [uxlc-email-count-disagreements-update.md](uxlc-email-count-disagreements-update.md).");
   leave the edited sentences as they now read; create the two update files, each with
   "State: open, first entry <YYYY-MM-DD>." and one dated entry, recorded under this plan and Ben's
   decision, that quotes the sentence's former and present words, names Ben's 2026-10-01 selection
   and says that the measurements of 2026-08-12 are unchanged. The receipt lint
   `py/tests/test_receipt_update_links.py` scans only `doc/*-update.md`, so read both pointers by
   eye; `evr-ii-b-55/evr-ii-b-55-images-provenance-update.md` is the precedent for an update outside
   `doc/`. The two new files:

   ```markdown
   # Updates to "Holman's manuscript-image citations, and the five that name the wrong scan"

   State: open, first entry <YYYY-MM-DD>.

   ## <YYYY-MM-DD>: an in-place edit of the finished record, recorded

   Recorded by <agent> on <YYYY-MM-DD>, New York time, under the approved remediation plan for the
   2026-10-02 review (its item C15.29), on Ben's decision of <YYYY-MM-DD> that this dated research
   record is a receipt.

   On 2026-10-01 `cb5bcda1` edited the record's last sentence in place. It had read "Run anything
   written for this from the repo root with
   `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`." and now reads "Run anything
   written for this from the root of a full MAM-basics clone, with that clone's own
   `./.venv/Scripts/python.exe`." Ben had selected that wording on 2026-10-01 among the census
   fixes that `doc/dual-agent-review-2026-09-29-turn-01-claude-update.md` records under "Live texts
   pinned to the primary forest fixed, 2026-10-01", so the sentence stays as it now reads. The
   record's measurements, made on 2026-08-12, are unchanged. An earlier in-place edit, by
   `9eedccbd` on 2026-09-07, predates the receipt reading that the 2026-09-29 review's remediation
   recorded on 2026-09-30, and is not itemized here.
   ```

   ```markdown
   # Updates to "Where Holman's messages disagree with themselves about their count"

   State: open, first entry <YYYY-MM-DD>.

   ## <YYYY-MM-DD>: an in-place edit of the finished record, recorded

   Recorded by <agent> on <YYYY-MM-DD>, New York time, under the approved remediation plan for the
   2026-10-02 review (its item C15.29), on Ben's decision of <YYYY-MM-DD> that this dated research
   record is a receipt.

   On 2026-10-01 `cb5bcda1` edited, in place, the sentence under "Re-establishing the figures"
   that introduces the method. Its second half had read "The method, run from
   `C:/Users/BenDe/GitRepos/MAM-basics` with that repository's venv:" and now reads "The method,
   run from the root of a full MAM-basics clone with that clone's own venv:". Ben had selected
   that wording on 2026-10-01 among the census fixes that
   `doc/dual-agent-review-2026-09-29-turn-01-claude-update.md` records under "Live texts pinned to
   the primary forest fixed, 2026-10-01", so the sentence stays as it now reads. The record's
   measurements, made on 2026-08-12, are unchanged. Two earlier in-place edits, by `9eedccbd` on
   2026-09-07 and `73ab8383` on 2026-09-09, predate the receipt reading that the 2026-09-29
   review's remediation recorded on 2026-09-30, and are not itemized here.
   ```

   The titles are the two records' H1 lines, and "Live texts pinned to the primary forest fixed,
   2026-10-01" is the September 29 update's section (`:1482`).
2. **Option 2: they are maintained research records.** A Ben-authorized reclassification under
   `mam-repository-topology/references/repository-maintenance.md`, "Manual document retirement":
   record his decision and date in this review's update; name `d54e12df`, the parent of `cb5bcda1`,
   as the archival commit holding both; change `terminology.md:460–461` from "Receipts, among them
   the dated Holman research records under `holman/doc/`, and external captures keep their words"
   to "Receipts and external captures keep their words", and add to that passage's list of what is
   "**Not** swept" the "folio" and "leaf" wording of the two Holman research records; deploy the
   skill.

Recommendation, option 1: it keeps both of Ben's decisions true without changing either, the
2026-09-30 receipt reading in the skill and the wording he approved on 2026-10-01, and it only
adds records.

Under either option, `doc/PLAN-checkout-kinds-and-portable-knowledge-update.md`'s entry "##
Phonetic refresh authority closeout, 2026-10-02" (`:370–376`), written by `d0c660c9`, gains a
paragraph after its heading: "Recorded by OpenAI Codex on 2026-10-02, New York time, under Ben's
paired evacuation closeout instruction, in `d0c660c9`. This line was added on <YYYY-MM-DD> under the
remediation of the 2026-10-02 review (item C15.29); the other entry that `d0c660c9` wrote, in
`doc/dual-agent-review-2026-09-29-turn-01-claude-update.md`, names that recorder." The update calls
the line a house convention, not a rule; `:362` of the same file shows it.

### Editorial proposals: comments, docstrings, help text and small document fixes (D7: editorial)

**C10.1, descriptions that still say the post-stress-meteg survey needs MAM-private or is skipped
in the cloud.** Since `9a67d51b` (2026-10-01) the survey reads the tracked `Phonetic-MAM/` release
(through `analysis_reader.read_book` and `paths.phonetic_mam_dir()`), MAM-simple and MAM-parsed
plus; the mega runs it unconditionally (`py/main_0_mega.py:206–207`), and run with `REPOS_ROOT` set
to an empty directory and `CLAUDE_CODE_REMOTE=true` it reproduces `out/accgram/post-stress-meteg.json`
byte for byte. `graphviz_pin.in_cloud_session()` keeps four callers, none for this survey.
`AGENTS.md:191–193`, `hebrew-prose`'s `references/verifying.md:49–52` and `py/main_0_mega.py:6–11`,
`:210–215`, `:636–642` and `:704–710` are already right. The stale passages and their replacements:

1. `py/main_accgram.py:45–52`, the `survey-post-stress-meteg` entry of the module help. Current, from
   "with" onward: "with / Phonetic MAM as the stress oracle, and write / out/accgram/post-stress-meteg.json.
   Needs the MAM-private / clone.  main_0_mega.py runs it as a step, except in a cloud / session, and
   py/author_site/post_stress_meteg.py renders the / page from the JSON it writes." Proposed: "with /
   the public Phonetic MAM display release as the stress oracle, / and write
   out/accgram/post-stress-meteg.json.  It needs no / MAM-private clone and runs in a cloud session
   too. / main_0_mega.py runs it as a step, and / py/author_site/post_stress_meteg.py renders the page
   from the / JSON it writes."
2. `py/main_accgram.py:419–421`, the subcommand's `--help`. Current: "Classify every U+05BD in MAM by its
   position relative to the chanted word's primary stress, with Phonetic MAM as the stress oracle, and
   write out/accgram/post-stress-meteg.json. Needs the MAM-private clone." Proposed: "Classify every
   U+05BD in MAM by its position relative to the chanted word's primary stress, with the public
   Phonetic MAM display release as the stress oracle, and write out/accgram/post-stress-meteg.json."
3. `py/main_authored.py:15–18`. Current: "--trust-surveys lets the post-stress pages that read the
   survey / load it from the tracked out/accgram/post-stress-meteg.json / instead of recomputing it,
   which needs the MAM-private clone; / only main_0_mega.py passes it." Proposed: "… instead of
   recomputing it from the tracked Phonetic-MAM / release; only main_0_mega.py passes it."
4. `py/main_authored.py:135–142`, the comment beginning "WHY ANY PAGE NEEDS IT: post-stress-meteg's
   survey reads Phonetic MAM, which lives in MAM-private." Proposed:

   ```python
   # WHY ANY PAGE NEEDS IT: py/main_0_mega.py runs post-stress-meteg's survey as a step of its
   # own just before gen-site, and the survey writes the tracked out/accgram/post-stress-meteg.json,
   # so the mega renders all nine pages from that JSON rather than walking the corpus a second
   # time.  The survey reads the tracked Phonetic-MAM release, so the mega runs it in a cloud
   # session too; until 2026-10-01 it read MAM-private's Phonetic MAM, and a cloud session
   # skipped it and rendered the pages from the tracked JSON unchanged.  Recomputing from the
   # corpus is what a standalone run does.  The JSON's absence FAILS rather than falling back, so
   # a mega that quietly published a page from nothing is not a state this can reach.
   ```
5. `py/main_authored.py:243–245`, the `--trust-surveys` help. Current: "… Passed by
   main_0_mega.py, which runs the survey as a step of its own, except in a cloud session."
   Proposed: "… Passed by main_0_mega.py, which runs the survey as a step of its own."
6. `py/author_site/post_stress_meteg.py:204–208`. Current: "``main_0_mega.py`` passes it because its
   survey step has just written that / JSON, or in a cloud session has skipped the survey and left the
   tracked JSON unchanged." Proposed: "``main_0_mega.py`` passes it because its survey step, which
   runs in a cloud / session too, has just written that JSON."
7. `py/mb_cmn/graphviz_pin.py:57–61`. Current: "Since 2026-09-10 the mega also skips a whole step in a
   cloud session, the post-stress-meteg survey, and ``py/main_0_mega.py``'s ``_report_cloud_skips``
   reports both kinds of skip. It skipped the near-Aleppo census too, until that step was deleted on
   2026-09-11." Proposed: "Since 2026-09-10 the mega also skips a whole step in a cloud session, and
   ``py/main_0_mega.py``'s ``_report_cloud_skips`` reports both kinds of skip. The skipped step was
   the post-stress-meteg survey until 2026-10-01, when ``9a67d51b`` moved the survey onto the
   tracked ``Phonetic-MAM/`` release; since then it is ``phonetic-mam-export``, the one step that
   reads private source inputs. The mega skipped the near-Aleppo census too, until that step was
   deleted on 2026-09-11."
8. `py/main_0_mega.py:603–610`, the comment beginning "Added 2026-09-10, when Ben decided the survey
   "should join mega"", which now sits above the `phonetic-mam-export` step: delete it there and
   insert directly above the `StepRecord(` for `"accgram-survey-post-stress-meteg"`:

   ```python
       # Added 2026-09-10, when Ben decided the survey "should join mega" on two conditions: a
       # worktree run finds MAM-private beside its home clone with no REPOS_ROOT (516a4a1a), and
       # a cloud run skips the survey altogether.  Until then nothing routine rewrote
       # out/accgram/post-stress-meteg.json; the survey was run by hand from main_accgram.py when
       # the corpus moved.  Since 9a67d51b (2026-10-01) the survey reads the tracked Phonetic-MAM
       # release rather than MAM-private, so neither condition concerns it any more: it runs in a
       # cloud session too, and the cloud skip belongs to phonetic-mam-export.  Placed immediately
       # before gen-site, which renders from the JSON it writes, and so after every step that
       # writes MAM-simple, whose json-vtrad-mam it reads (paths.mam_simple_vtrad_mam_dir).  This
       # comment and the description below said xml-vtrad-mam until 2026-09-11.
   ```
9. `py/tests/test_redirect_manifest.py:37–41`. Current: "This follows
   ``py/tests/test_final_stress_vs_phonetic_mam.py``, which skips in a container the tests that read
   MAM-private. Like that module, it asks ``graphviz_pin.in_cloud_session()``, the repository's one
   cloud predicate, so the read is skipped in a container whether or not hbofonts is attached
   there." Proposed: "It asks ``graphviz_pin.in_cloud_session()``, the repository's one cloud
   predicate, so the read is skipped in a container whether or not hbofonts is attached there. When
   this skip was added it followed ``py/tests/test_final_stress_vs_phonetic_mam.py``, which then
   skipped in a container the tests that read MAM-private; since ``9a67d51b`` (2026-10-01) that
   module reads the tracked ``Phonetic-MAM/`` release and runs everywhere."

Items 1, 2 and 5 are program output, so they ride on the full suite. Verification: Black; read
`py/main_accgram.py survey-post-stress-meteg --help` and `py/main_authored.py gen-site --help`;
`py/main_test.py py/tests/test_entry_point_subcommands.py py/tests/test_mega_coverage.py py/tests/test_product_scopes.py py/tests/test_redirect_manifest.py py/tests/test_prose_conventions.py`.
C15.17 edits the step note inside the block that item 8 moves; make the two edits in one commit.

**C10.4, the product count.** `py/product_scopes.py:21–26` lists five distributed products while
`_PRODUCT_DIR_NAMES` (`:85–93`) holds seven. Proposed: "2. DISTRIBUTED DATA.  ``MAM-parsed/`` (whose
current parsed payload is ``MAM-parsed/plus/``), ``MAM-simple/``, ``MAM-for-Sefaria/``,
``MAM-with-doc/``, ``MAM-OSIS/``, ``Phonetic-MAM/`` and ``Yeivin-ITM/``. These are consumed by git URL
whether or not Pages serves them, …" (the rest unchanged). `py/tests/test_product_scopes.py:19–22`,
"the published tree, the five product directories, and every tier-3 entry point", becomes "the
published tree, every product directory ``_PRODUCT_DIR_NAMES`` declares, and every tier-3 entry
point". `AGENTS.md:157–158`, "`MAM-parsed/`, `MAM-simple/`, `MAM-for-Sefaria/`, `MAM-with-doc/`, and
`MAM-OSIS/`, `Phonetic-MAM/`, and `Yeivin-ITM/`", becomes "`MAM-parsed/`, `MAM-simple/`,
`MAM-for-Sefaria/`, `MAM-with-doc/`, `MAM-OSIS/`, `Phonetic-MAM/`, and `Yeivin-ITM/`". Verification:
Black and `py/main_test.py py/tests/test_product_scopes.py`.

**C14, the citation of Ben's decision at the exemption, `py/tests/test_h_dot_below_nfc.py:191–195`.**
Current comment: "# Generated display data retains the existing public transcription exactly, /
# including its decomposed Latin vowel marks. Authored README/schema stay in / # the main scope;
this is the same generated-data boundary as out/ above." Proposed:

```python
    # Generated display data retains the existing public transcription exactly,
    # including its decomposed acute and breve vowels. Keeping those legacy bytes,
    # here and in gh-pages/phonetic-mam/, is Ben's decision of 2026-10-03, "Keep the
    # legacy bytes": doc/review-findings-2026-10-02-update.md, "Ben's close-out
    # decisions, 2026-10-03", item 2. Authored README/schema stay in the main
    # scope; this is the same generated-data boundary as out/ above.
```

**C15.6, `py/tests/test_final_stress_vs_phonetic_mam.py:15–24`.** It says "MAM has a gray maqaf in 113
places where Phonetic MAM keeps two chanted words" and counts "11 more". In fact Phonetic MAM has each
gray-maqaf compound as one entry, spelling the maqaf as a tilde where the test's loader gives U+05BE,
so none of the 113 joins; and the prose non-joins are 12, 2 Kings 22:1 being new. Replace `:15–24`
(`:25` stays) with:

```text
so says nothing about stress.  MAM, because Phonetic MAM is MAM; prose, because the page the
measurement is for is about prose verses, and because only poetic verses have MAM's gray maqaf,
which this test's join cannot match.  Phonetic MAM has each of MAM's gray-maqaf compounds as one
entry, 113 of them, and ``analysis_reader`` spells that maqaf as a tilde where ``mam_simple_verse``
gives it as U+05BE; the join key keeps both marks, so none of the 113 joins, and they are most of
what will not join anywhere in MAM's Tanakh.  The rest, 12 chanted words in prose verses, are
outside this test's reach for reasons of their own (issue wlc-utils#91): 8 dually-cantillated
chanted words in the two Decalogues, whose ``cant-combined`` projection is neither strand; the two
chanted words of Deuteronomy 32:6, where MAM's large ה stands apart from לְיְהֹוָה֙ and Phonetic
MAM has one entry for the two atoms; 2 Kings 22:1, where Phonetic MAM has only {{2KI-REL}} and
MAM-simple has the other qamats alternative, {{2KI-SIMPLE}}; and 2 Chronicles 25:17, where Phonetic
MAM has לְךָ֖ against the qere לְכָ֖ה that MAM-simple and WLC 4.22 both have.  Those last two are
differences in the text rather than in the grouping.  The
```

with `{{2KI-SIMPLE}}` lifted from `MAM-simple/json-vtrad-mam` (the verse's last chanted word,
`{{2KI-D}}` and U+05C3). Verification:
`py/main_test.py py/tests/test_final_stress_vs_phonetic_mam.py py/tests/test_prose_conventions.py`.

**C15.21, `py/tests/test_sibling_reach.py:210–213`.** Current: "… Only the / repos_root recognizer skips
it; its sibling_repo("MAM-private") call is a real reach / and is counted." `py/mb_cmn/paths.py` no
longer names a sibling: `9a67d51b` deleted `al_hatorah_phonetic_dir`, and MAM-private's one reach is
`py/phonetic_mam/exporter.py:34–35`. Proposed, from "Only the": "Only the / repos_root recognizer skips
it.  paths.py has named no sibling since 9a67d51b deleted / its al_hatorah_phonetic_dir: MAM-private's
one reach is the exporter's call at / py/phonetic_mam/exporter.py:34-35, which the scan counts like any
other."

**C15.22, `py/mb_cmn/paths.py:215`.** The `display_path` docstring's example "``Phonetic-MAM/data``"
becomes "``MAM-basics/Phonetic-MAM/data``", which is what the function returns (`:239–240`) and what
`out/accgram/post-stress-meteg.json:21848` records.

**C15.17, `py/main_0_mega.py:634`, the step note of `yeivin-itm-render`.** Current: "reads the
approved tracked claims and adaptation; writes all 17 public Yeivin pages". The step also reads
`py/yeivin_itm/assets/style.css`, `doc/woff2/` and `in/font-support/taamey-d-0.921/`, and writes
`gh-pages/yeivin-itm/style.css`, the four files of `gh-pages/yeivin-itm/woff2/` and the shared
`gh-pages/font-sources/taamey-d-0.921/`. Proposed note: "reads the approved tracked claims, the
adaptation and py/yeivin_itm/assets/style.css, and the frozen font inputs doc/woff2/ and
in/font-support/taamey-d-0.921/; writes the 17 public Yeivin pages, gh-pages/yeivin-itm/style.css,
the four files of gh-pages/yeivin-itm/woff2/ and the shared gh-pages/font-sources/taamey-d-0.921/
package, which phonetic-mam-render also writes", split across string literals within 88 columns. The
note is never printed or read. Commit it with C10.1's item 8, which moves the comment above the same
block.

**C15.31, links into the private `bdenckla/trope` tracker (question 13).** Thirteen comment lines in
six adaptation modules link nine of its issues, 374 to 382: `my_yeivin_sec_320.py:33`,
`my_yeivin_sec_321.py:28`, `my_yeivin_sec_322.py:140`, `my_yeivin_sec_326.py:35`, `:48`, `:52` and
`:57`, `my_yeivin_sec_327.py:21`, `:28`, `:35`, `:49` and `:70`, and `my_yeivin_sec_328.py:25`; for
example the comment at `my_yeivin_sec_320.py:33`, "# MAM has gaʿya on yod; see closed issue", ends
with the URL of that tracker's issue 374, which this plan does not repeat. The
tracker's privacy rests on the reviewer's metadata query (`in/repo_maintenance_policy.json` lists trope
under `repos_to_keep_absent` with no visibility). `AGENTS.md`, "Issue citations in MAM-basics", item
1, cites another tracker as `repo#NN`; Ben's rule of 2026-08-27 lets a private repository's name
appear in a public file but not "paths inside them, file names of theirs". What replaces the links is
Ben's call:
1. **Option 1 (recommended): `trope#NN (private tracker)`.** For example, `:33` becomes
   "# MAM has gaʿya on yod; see closed issue trope#374 (private tracker)." The label assumes that
   trope is private, an assumption stated when Ben accepted this option on 2026-10-03. The executor
   re-checks it first with `gh repo view bdenckla/trope --json visibility --jq .visibility`, a
   read-only query that must print `PRIVATE`, and stops if it does not. The label keeps the
   provenance in the form `AGENTS.md` prescribes, and an issue number is an identifier, not a path.
2. **Option 2: delete the reference.** Delete "; see [closed issue] <URL>" and keep each line's final
   punctuation; for example "# MAM has gaʿya on yod."
3. **Option 3: keep each URL and add "(private)".** Not recommended: it keeps paths inside the private
   repository in a public file.

Every option edits six hash-pinned modules, so it waits for question 8. The pages do not change.
Verification: `py/main_test.py py/tests/test_yeivin_itm.py py/tests/test_prose_conventions.py` and
`./.venv/Scripts/python.exe py/main_yeivin_itm.py check`.

**C15.5, `py/main_github_issue_edit.py:3–4`**, which is also its `--help` (`description=__doc__`).
Current: "Run with a full MAM-basics clone's own interpreter; every path here is resolved / from this
file, never from the cwd. From the clone's root:". `--edits` is read with `Path(args.edits)` (`:53`),
relative to the working directory. Proposed: "Run with a full MAM-basics clone's own interpreter. The
output path under this / repository's .novc/ is resolved from this file, never from the cwd; the
--edits / path is resolved from the working directory, as any command-line path is. From / the
clone's root:".

**C15.26, `doc/clone-forests.md:20–22`.** Current: "… A missing clone or environment, a dirty /
checkout, a branch other than `main`, ahead/diverged history or dependency drift returns failure."
The check form also fails on any Git operation in progress or lock file (`py/repo_util/forest_sync.py:248–249`,
`:108–133`) and on a clone behind `origin/main` (`:282`). Proposed: "… A missing clone or environment,
a dirty / checkout, a branch other than `main`, a Git operation in progress or a Git lock file, history
/ behind, ahead of or diverged from `origin/main`, or dependency drift returns failure." The lock file
goes one step past the update's addition because the code reports it under the same reason.

**C15.27, `py/repo_util/run_black.py:32–37`.** The comment line `:32`, "# into the base Python", was
left stranded by `37002a28`'s rewording of `:31`; rewrap `:32–37` into these five lines without
changing a word:

```python
    # into the base Python for them, reached through Ben's persisted USER PATH. An
    # agent shell does not inherit that PATH, so shutil.which above returns None
    # there and the sweep would report every such repo as a problem when black is
    # in fact present. sys.base_prefix is the base installation root inside a venv
    # and equals sys.prefix outside one, so no venv-detection branch is needed.
```

## The relay's retirement

Ben's decision 3 of 2026-10-03, "Retire the relay now", retires the automated dual-agent review
relay: "its code, tests, runbook, plan, configuration, agent file and deployed copy, its
registered scheduled task, and the procedure text that describes it". This section is the plan for
all of it. Everything in the repository is lower risk on product reach: no page, product or mega
generator reads the relay, so the removal owes the suite and not the mega. The acts outside the
repository are listed last; Ben authorized them in advance on 2026-10-03.

### Where the relay's state is

**The relay ran on another machine, not on the one where this plan was prepared.** This plan was
prepared on `LAPTOP-DBLE8UKA`, whose `C:/Users/BenDe/GitRepos2/MAM-basics` was cloned at 09:58 New
York time on 2026-09-29 and whose reflogs hold no relay commit; `1a50d4b6`, the relay's first
commit, was never checked out there. That machine has no scheduled task named
`Dual-agent review relay`, no `.novc/dual-agent-review/`, no `relay-*` receipt and no linked
worktree in any of its three MAM-basics clones. The tracked records give the relay's paths, which
use the same `C:/Users/BenDe/GitRepos2/MAM-basics`, but never name its machine; this plan calls it
**the relay machine**. Per those records, it holds the scheduled task, the dispatcher's registry and
evidence under its GitRepos2 clone's `.novc/`, three locked worktrees, two local branches, a
rehearsal home and a paused Codex follow-up. The deployed agent file is on `LAPTOP-DBLE8UKA` too,
byte-identical to the canonical file (SHA-256
`2CB3B50A719FF019162C9BF7B0684094106A99EE22AE0E60A9CD5ACA907E4308`), and this plan assumes the relay
machine has a copy.

### In the repository

All of the following lands in one commit, with the dated entry of R7 and the procedure text of R6,
because the D13 note and that entry cite the removal commit's parent, `<ARCHIVE-SHA>`: the last
commit whose tree holds every removed file. The executor writes its full 40-character SHA in place
of the placeholder.

**R1. Delete the ten relay files.**

| File | Bytes at `644a6c9c` |
|---|---|
| `py/repo_util/dual_agent_review_dispatch.py` | 60,378 |
| `py/repo_util/dual_agent_review_round.py` | 15,047 |
| `py/tests/test_dual_agent_review_dispatch.py` | 47,799 |
| `py/tests/test_dual_agent_review_turns.py` | 13,150 |
| `doc/dual-agent-review-automation.md` (State: runbook) | 50,075 |
| `doc/PLAN-automate-the-dual-agent-review-relay.md` (State: live) | 66,778 |
| `in/dual_agent_review_automation.json` | 1,648 |
| `misc/dual-agent-review-toast.ps1` | 1,969 |
| `misc/register-dual-agent-review-task.ps1` | 1,563 |
| `dot-claude/agents/dual-agent-review-turn.md` | 2,494 |

The runbook and the plan are maintained one-file families with no update file, so this is the
retirement that `mam-repository-topology/references/repository-maintenance.md`, "Manual document
retirement", describes, with Ben's decision as its approval. Its reference audit was done while
planning and is repeated by the executor before committing: no GitHub issue, pull request or
comment of `bdenckla/MAM-basics` names either file, the relay or `dual_agent_review` (a complete
paginated scan of 295 issues and pull requests and 312 comments on 2026-10-03); in tracked files,
the one current-guidance reference, `doc/dual-agent-review.md:884`, is rewritten under R6, and
every other reference is historical evidence that reaches the files through `<ARCHIVE-SHA>`, the
D13 note or a commit it already names. Re-run the tracked census before committing with
`git -C <checkout> grep -n -I -e dual-agent-review-automation -e PLAN-automate-the-dual-agent-review-relay`.

**R2. Remove the relay's hunks from `py/main_repo_util.py`**, which `1a50d4b6` added (`2e120b85`
added only the `deactivate` usage line and choice): the seven usage lines from
`--dual-agent-review status` through `--dual-agent-review deactivate` (`:16–22`); the
`--dual-agent-review` action and its nine options `--repo`, `--round`, `--agent`, `--agent-1`,
`--start`, `--end`, `--instruction`, `--rehearsal` and `--automation-config` (`:173–199`); the
validation ending `parser.error("review options apply only to --dual-agent-review")` (`:387–403`);
the `pythonw` fallback that opens `.novc/dual-agent-review/scheduler.log` when a standard stream is
`None` (`:511–517`); and the dispatch branch `if args.dual_agent_review:` (`:584–587`). No other
code reads those attributes. Oracle: afterwards `git diff 303bf2399c1e1fc1300a75f4fb1ed335d62984d0 -- py/main_repo_util.py`
shows exactly two hunks, the `--sync-forest` docstring paragraph and the `--visibility private`
example, which later non-relay commits made.

**R3. Remove the agent file's deployment from `py/repo_util/user_config_sync.py`:** its
`_ARCHIVE_PATHS` entry (`:39`), its `ConfigMapping` (`:300–304`) and the source-validation loop
that came with it (`:347–349`), which validates only sources that `:265–271` and `_skill_names`
already validate. Oracle: `git diff --exit-code 303bf2399c1e1fc1300a75f4fb1ed335d62984d0 -- py/repo_util/user_config_sync.py`
exits 0. The canonical agent file, its archive entry and its mapping must leave in the same commit:
otherwise `git archive` fails on the missing path and `--sync-user-config` reports
`USER_CONFIG_CHECK_FAILED`. `--sync-user-config` deploys and compares only declared mappings, and its
one removal mechanism, the `absent` kind, serves retired skill directories under `~/.agents/skills/`
only, so it will neither remove nor report the deployed copy: that is act A2.

**R4. `dot-claude/README.md`.** Delete the table row
`` | `agents/dual-agent-review-turn.md` | `~/.claude/agents/dual-agent-review-turn.md` | `` (`:16`),
and in `:82–84` replace "every Claude-specific and Codex-specific skill, both destinations of every
shared skill, / and the automated review's Claude agent file. The" with "every Claude-specific and
Codex-specific skill, and both destinations of every shared skill. The", rewrapped as at
`303bf239`. Oracle: `git diff 303bf2399c1e1fc1300a75f4fb1ed335d62984d0 -- dot-claude/README.md`
then shows only `1c0cf3f8`'s two hunks.

**R5. Keep the turn-file lint that the relay's test module carried (proposed).** Deleting
`py/tests/test_dual_agent_review_turns.py` also deletes `test_turn_census_and_sequences` (`:13–46`),
which checks every numbered turn of every round dated 2026-09-16 or later, manual rounds included:
contiguous numbering from 01, Agent 1 and Agent 2 alternating, and the line-3 `State:` shapes of
D10. It arrived with the relay in `1a50d4b6` but guards D9 and D10, which survive. Proposed: a new
lint, `py/tests/test_review_turn_files.py`, holding that test's own oracle and checks without the
relay module: it lists tracked files with `git ls-files -z`, keeps those matching
`^doc/dual-agent-review-([0-9]{4}-[0-9]{2}-[0-9]{2})-turn-([0-9]{2})-(claude|codex)[.]md$`, fails if
none match, groups rounds dated 2026-09-16 or later, and asserts the same numbering, alternation
and `State:` shapes (turn 01's line 3 starts with "State: "; every later turn's line 3 matches
`State: completed \d{4}-\d{2}-\d{2}; review only`). It drops the comparison with the relay module's
`census`, `lint_automated_round_headers` and the `Next:`-transition test. Ben's acceptance of
2026-10-03 covers R5, so the lint is kept.

**R6. Procedure text: current and proposed wording.** Most proposals restore the words that the
relay's commits replaced; `git show a92b2ebe -- doc/dual-agent-review.md doc/periodic-review.md`
and `303bf239`'s text show the originals.

1. `doc/dual-agent-review.md:61–63`. Current: "This is a next-review trial, not a commitment to two
   reviewers for every later window. It requires no new relay implementation or private automated
   rollout, and leaves the existing relay code and historical evidence in place. Do not expand
   relay features merely to prepare this trial." Proposed: "This is a next-review trial, not a
   commitment to two reviewers for every later window, and it uses no relay software: by Ben's
   decision of 2026-10-03 the automated relay is retired, as D13 below records."
2. `:236–242`, D9's delegation paragraph. Current: "… verifies the claims it adopts, and owns the
   tracked file. In a manual round the root reviewer also owns the commit; D13 assigns automated
   staging, commits and pushes to the dispatcher. Only one agent writes, …". Proposed, the text
   and wrapping at `303bf239`: "… verifies the claims it adopts, and owns the tracked file and
   commit. Only one agent writes, stages, commits or pushes the round's branch at a time; …",
   which also ends the over-long line `:240`.
3. `:251–252`. Current: "Manual rounds have no maximum number of turns; the stopping rule below
   ends the exchange. D13 additionally caps automated rounds." Proposed: "There is no maximum
   number of turns; the stopping rule below ends the exchange."
4. `:271–281`. Current: "… In a manual round, Ben supplies the next task with that file's path and
   pushed commit; … The naming section distinguishes this standard round from single-agent and
   blind-review filenames. D13 assigns automated launches and the verified handoff to the
   dispatcher." Proposed, the paragraph at `303bf239`: "… Ben supplies the next task with that
   file's path and pushed commit; … The naming section distinguishes this standard round from
   single-agent and blind-review filenames."
5. `:334–341`, D11. Current: "**By default, each turn and close-out task runs in whatever verified
   checkout its session is already in for a manual round** … A manual round may still use a linked
   worktree made for it, but its procedure requires none. D13 requires two dedicated worktrees for
   automated turns. A local branch …". Proposed: "**By default, each turn and close-out task runs
   in whatever verified checkout its session is already in** … A round may still use a linked
   worktree made for it, but no step of this procedure requires one. A local branch …"; the rest
   of the paragraph, including the sentences on the app's checkouts, stays and is rewrapped.
6. `:369`: "For a manual turn, fetch" becomes "At the start of a turn, fetch"; and `:376–377`, "For
   an automated turn, D13 assigns these Git operations to the dispatcher; the worker writes review
   prose and does not fetch, stage, commit or push. Manual close-out follows the rules below.", is
   deleted.
7. `:426–496`, the whole D13 section, from "### Automated relay and the `Next:` line — Ben's
   decisions, 2026-09-30 and 2026-10-01 (D13)" to "… pending Ben's separate choice.", becomes:

   > ### D13, the automated relay — Ben's decisions, 2026-09-30 and 2026-10-01; retired by his decision of 2026-10-03
   >
   > **The automated relay is retired.** Ben's selection on 2026-10-03, verbatim, was "Retire the
   > relay now" (`doc/review-findings-2026-10-02-update.md`, "Ben's close-out decisions,
   > 2026-10-03", item 3). D13, approved on 2026-09-30 and qualified on 2026-10-01, let Ben start a
   > round with `py/main_repo_util.py --dual-agent-review start`. A Windows scheduled task then ran
   > a dispatcher every three minutes; the dispatcher launched each turn's worker in one of two
   > dedicated worktrees, read the `Next:` line that every automated turn carried, and alone
   > staged, committed and pushed each turn to `origin/dar-<date>`. The October 1 round below was
   > its only round. No round is started that way now: a dual-agent round follows D9 and D11, and
   > Ben starts each turn's session himself.
   >
   > The relay's code, tests, configuration, scripts, agent file, runbook and plan were removed on
   > <DATE>. `<ARCHIVE-SHA>` is the last commit whose tree holds them; there are
   > [D13's full text](https://github.com/bdenckla/MAM-basics/blob/<ARCHIVE-SHA>/doc/dual-agent-review.md),
   > in the section "Automated relay and the `Next:` line",
   > [the runbook](https://github.com/bdenckla/MAM-basics/blob/<ARCHIVE-SHA>/doc/dual-agent-review-automation.md)
   > and [the plan](https://github.com/bdenckla/MAM-basics/blob/<ARCHIVE-SHA>/doc/PLAN-automate-the-dual-agent-review-relay.md).
   > The October 1 round's records stay in `doc/`, and
   > `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md` records the retirement.
8. `:498–507`, "The first automated round, 2026-10-01", whose "The actual home registration is
   retained inactive/manual", "The enabled scheduler skips that registration; PAUSE and evidence
   remain" and "private rollout remains separate" become false, becomes:

   > ### The October 1 round
   >
   > The October 1 round, the only round run under D13, reviewed the relay's own implementation
   > window, MAM-basics `303bf239..1bfceff4`, with Claude as Agent 1, and closed after five turns.
   > Ben approved C1–C6 and the surviving remediation scope, and the remediation reached `main` on
   > 2026-10-01: the final merged tree passed 1,056 tests and 60 subtests, with 5 skips, and the
   > required 57-step mega produced no tracked diff.
   > `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md` records the dispositions, the
   > outcomes and the relay's retirement. The round file `doc/dual-agent-review-2026-10-01-round.md`,
   > the five numbered turns and the finished comparison `doc/dual-agent-review-comparison-2026-10-01.md`
   > are unchanged.
9. `:771–777`, D10. Item 4's last sentence, "Preserve historical filenames and `State:` lines,
   including September 4's Codex "acted on", September 8's turns under a Codex-prefixed stem, and
   September 14's mixed old and numbered naming.", gains at its end: ", and the October 1 round's
   `doc/dual-agent-review-2026-10-01-round.md` and the `Next:` lines of its turns, which follow
   the retired D13"; item 5, "**Automated rounds additionally follow D13:** … Manual rounds keep
   their existing relay and State conventions.", is deleted.
10. `:883–885`. Current: "2. **Manual Codex launches.** D13, approved 2026-09-30, defines the
    automated relay; `doc/dual-agent-review-automation.md` records the implemented launcher,
    verified probes and remaining live prerequisites. Invocation outside automated rounds remains
    unspecified here." Proposed, the text at `303bf239`: "2. **How to run Codex on this machine.**
    No command line is given here. Codex demonstrably runs here — see the provenance section — but
    this document has not examined how it is invoked, and guessing a spelling would be worse than
    the omission."
11. `:929–931`: delete the blank line and "The provenance above describes manual rounds. D13,
    approved 2026-09-30, replaces Ben's relay with dispatcher guards only for explicitly started
    automated rounds."
12. `doc/periodic-review.md:24–26`. Current: "… reconciles the reports, verifies the claims it
    adopts, and owns the findings file. The reviewer owns the commit in a manual review; D13 in
    `doc/dual-agent-review.md` assigns automated commits to the dispatcher." Proposed, the text at
    `303bf239`: "… reconciles the reports, verifies the claims it adopts, and owns the findings
    file and commit."
13. `doc/periodic-review.md:46–48`. Current: "A review may still use a linked worktree made for it,
    but manual review procedures require none. D13 in `doc/dual-agent-review.md` requires two
    dedicated worktrees for automated dual-agent turns." Proposed, the text at `303bf239`: "A review
    may still use a linked worktree made for it, but nothing in this procedure or in
    `doc/dual-agent-review.md` requires one."

These stay as written: the kickoff record (`doc/dual-agent-review.md:127–131`, `:139–159`, including
"which Ben hopes to discard soon") and Ben's quotation at `:67–73`, which are historical; the trial
text's "No mandatory rebuttal, … shared relay branch, dedicated relay worktrees or automated relay is
required." (`:49–51`), which stays true; and D9's "Turn 01 cannot request acknowledgment; turn 02
always supplies this counter-argument and reconciliation append before an acknowledgment can be
owed." (`:262–263`), a rule for every round. Two plans use "D13" for an earlier worktree-forest
decision (`doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md:446`, `:507`, `:525`;
`doc/PLAN-remediate-review-findings-2026-09-29.md:2250–2251`); they are not about the relay and stay.

**R7. The October 1 round's records are kept as they are, and its live update records the
retirement.** The round file `doc/dual-agent-review-2026-10-01-round.md` (State "executed
2026-10-01; close-out completed"), turns 01 to 05, `doc/PLAN-close-out-review-2026-10-01.md` and
`doc/dual-agent-review-comparison-2026-10-01.md` are finished records and stay byte for byte, as
D12 and `iterative-document-editing` require; each citation they make of a removed file resolves
at `<ARCHIVE-SHA>`. The round's one live update, `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md`,
gets a dated entry after "Update-State correction by Codex, 2026-10-02", and its stale present-tense
claims are corrected in place, each listed in that entry with its former and new words:

1. `:5–6`. Current: "**Approved remediation and close-out are completed on main; deployment and
   home deactivation are verified.** / The execution entry below records the current disposition.
   Findings 1 and 11 remain withdrawn." Proposed: "**Approved remediation and close-out were
   completed on main on 2026-10-01; the relay was retired on <DATE>.** / "Relay retired, <DATE>"
   below records the current disposition. Findings 1 and 11 remain withdrawn."
2. `:297–299`. Current: "The revised canonical / `dot-claude/agents/dual-agent-review-turn.md` is
   deployed; live instruction files were not / edited directly." Proposed: "The revised canonical
   `dot-claude/agents/dual-agent-review-turn.md` was deployed; live instruction files were not
   edited directly. "Relay retired, <DATE>" below records the deployed copy's later disposition."
3. `:302–307`, from "Its actual registry retains the entry" to "remain recoverable.": the same
   facts in the past tense ("retained", "was retained", "PAUSE remained present"), ending "When this
   entry was written, both worktrees, the branch and all original control evidence remained
   recoverable; "Relay retired, <DATE>" below records what became of them."
4. `:311–314`, from "The Windows task's inspected action uses" to "It / remains Ready, enabled, with
   IgnoreNew.": the same facts in the past tense, ending "It remained Ready, enabled, with IgnoreNew
   when this entry was written."
5. `:320–321`. Current: "`State: executed 2026-10-01; close-out completed`; its parser/lint already
   admits this / terminal state and it cannot dispatch." Proposed: "`State: executed 2026-10-01;
   close-out completed`; the relay's parser and lint then admitted this terminal state, and the
   round could not dispatch."

The dated entry, filled in by the executor:

> ## Relay retired, <DATE>
>
> **Retired: the relay that this round reviewed and remediated was removed from the tree on
> <DATE>; this round's records stay unchanged.** Ben's selection on 2026-10-03, verbatim, was
> "Retire the relay now" (`doc/review-findings-2026-10-02-update.md`, "Ben's close-out decisions,
> 2026-10-03", item 3). Commit `<REMOVAL-SHA>` removed the relay's ten files, among them
> `py/repo_util/dual_agent_review_dispatch.py`, `py/repo_util/dual_agent_review_round.py`, their two
> test modules, `doc/dual-agent-review-automation.md` and
> `doc/PLAN-automate-the-dual-agent-review-relay.md`, together with the `--dual-agent-review`
> action of `py/main_repo_util.py` and the agent file's deployment in
> `py/repo_util/user_config_sync.py` and `dot-claude/README.md`. Its parent,
> [`<ARCHIVE-SHA>`](https://github.com/bdenckla/MAM-basics/tree/<ARCHIVE-SHA>), is the last commit
> whose tree holds every removed file; each path and line that this round's records cite in those
> files resolves there. D13 in `doc/dual-agent-review.md` is now a dated retirement note.
>
> The round file, the five numbered turns, `doc/PLAN-close-out-review-2026-10-01.md` and
> `doc/dual-agent-review-comparison-2026-10-01.md` are unchanged. In the round file, "This
> present-state file identifies an automated round" and "PAUSE, worktrees, branch and evidence are
> retained" describe the round as of 2026-10-01; no dispatcher reads the file now. <The five
> in-place corrections above, each with its former and new words.>
>
> Ben authorized in advance, on 2026-10-03, the acts outside the repository that the remediation
> plan lists under "Acts outside the repository"; later dated entries here record each one's
> outcome as it is done, and `origin/dar-2026-10-01` stays by his choice.
>
> **Effective base State, <DATE>:** acted on; the approved remediation completed on 2026-10-01
> stands as recorded above, and the relay it remediated was retired on <DATE>.

**Not in this plan: MAM-private's own records.** This plan reads nothing in MAM-private. The
runbook's State line says that "private readiness P7 and concrete private kickoff decisions remain
pending"; with the relay retired, that rollout lapses. A MAM-private session may check that
repository's tracked tree for `dual-agent-review-automation`, `--dual-agent-review`, `D13` and
`relay`, and record any retirement there under its own procedure.

### Effects and checks

- The suite loses exactly the relay's 15 test functions (11 in the dispatch module, 4 in the turns
  module; none parametrized) and gains R5's one, with the same 60 subtests and 5 skips: a
  differential check on the full-suite counts.
- `ruff check` loses its F841 at `py/tests/test_dual_agent_review_dispatch.py:805`, one of C9.2's 17.
- No product, page or generated file changes, and no mega step reads the removed code.
- Checks: Black on `py/main_repo_util.py`, `py/repo_util/user_config_sync.py` and the new lint; the
  three `303bf239` oracles of R2 to R4; `git diff --check`;
  `git grep -n -I -e "dual_agent_review" -e "dual-agent-review-turn" -e "--dual-agent-review" -e "dual-agent-review-toast" -e "register-dual-agent-review-task" -- py misc in dot-claude dot-Codex .claude AGENTS.md doc/periodic-review.md`,
  which must print nothing;
  `py/main_test.py py/tests/test_review_turn_files.py py/tests/test_worktree_retirement_policy.py py/tests/test_mega_coverage.py py/tests/test_entry_point_subcommands.py py/tests/test_receipt_update_links.py py/tests/test_prose_conventions.py py/tests/test_tracked_filenames.py`;
  `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check` from the carrier, which
  reads `origin/main` and must still report no problem while `origin/main` keeps the agent file.
- **After the push, every full clone on every machine still running the old code fails
  `--sync-user-config --check`**, because its `_ARCHIVE_PATHS` names a file that `origin/main` no
  longer has; that failure writes nothing. Each clone is fine once fast-forwarded, which Ben's
  ordinary synchronization does. Until then, routine maintenance's configuration step in such a
  clone reports the failure.

### Acts outside the repository

Ben authorized every act below in advance on 2026-10-03 ("Decisions this plan follows", item 4), so
no session asks him for any of them. The executor performs A3, A2 and A10 on its own machine,
`LAPTOP-DBLE8UKA`, as steps 4 and 5 of "Final integration". A session that Ben starts on the relay
machine performs A0, A1, A7, A3, A2, A4, A5 and A8 there, in the order that "The relay-machine
session" gives; A9 is Ben's own, and A6 is not done. **No act deletes anything:** each removal moves
its object into the retention folder `$HOME/relay-retirement-2026-10/` on its machine, and A4's
retirement tooling relocates its evidence there too; Ben may delete that folder whenever he wants the
space. Whoever performs an act records its outcome (done; unnecessary, because A0 did not find its
object; or blocked, with the blocker) as "Records" and "The relay-machine session" describe. A
session whose own rules refuse an act skips that act only, records it with the exact command for Ben
to run, and goes on with the rest.

1. **A0, read-only: inventory the relay machine,** the machine on which Ben starts the relay-machine
   session. In PowerShell 7:

   ```powershell
   $env:COMPUTERNAME
   ```

   ```powershell
   Get-ScheduledTaskInfo -TaskPath '\' -TaskName 'Dual-agent review relay' | Format-List LastRunTime, LastTaskResult, NextRunTime
   ```

   ```powershell
   git -C C:/Users/BenDe/GitRepos2/MAM-basics worktree list --porcelain
   ```

   ```powershell
   Get-ChildItem -Force -LiteralPath C:/Users/BenDe/GitRepos2/MAM-basics/.novc | Select-Object Name, LastWriteTime
   ```

   ```powershell
   Test-Path -LiteralPath C:/Users/BenDe/GitRepos-rehearsal
   ```

   ```powershell
   Test-Path -LiteralPath $HOME/.claude/agents/dual-agent-review-turn.md
   ```

   ```powershell
   Test-Path -LiteralPath $HOME/relay-retirement-2026-10
   ```

   This reads only. If A0 finds none of the scheduled task, `.novc/dual-agent-review/` and A4's three
   worktrees, the machine is not the relay machine, and "The relay-machine session" says what happens
   then. Nothing already in the retention folder is ever overwritten.
2. **A1: unregister the scheduled task `\Dual-agent review relay`** on the relay machine, without
   elevation, as Ben registered it on 2026-10-01:

   ```powershell
   Unregister-ScheduledTask -TaskPath '\' -TaskName 'Dual-agent review relay' -Confirm:$false
   ```

   ```powershell
   @(Get-ScheduledTask -TaskPath '\' | Where-Object TaskName -eq 'Dual-agent review relay').Count
   ```

   The second command must print `0`. **Order:** before that machine's GitRepos2 clone is
   fast-forwarded past the relay's removal, and before A7, since a tick can recreate
   `.novc/dual-agent-review/`. The task runs that clone's working tree with `pythonw`. Once the
   removal is checked out there, each tick raises at once and writes nothing, because both standard
   streams are `None` and R2 removes the fallback that opened a log for them. That is harmless: the
   push of `main` need not wait for A1, and a session that may not run A1 still goes on with the
   fast-forward. Undo: re-register with the deleted script from `<ARCHIVE-SHA>`.
3. **A2: retire the deployed agent file on each machine,** after that machine's A3, so that the
   configuration deployed there no longer names it. On `LAPTOP-DBLE8UKA` the file exists (SHA-256
   `2CB3B50A…`, equal to the canonical file); on the relay machine A0 says. Record its hash, then move
   it into the retention folder:

   ```powershell
   Get-FileHash -Algorithm SHA256 -LiteralPath "$HOME/.claude/agents/dual-agent-review-turn.md"
   ```

   ```powershell
   New-Item -ItemType Directory -Force -Path "$HOME/relay-retirement-2026-10"
   ```

   ```powershell
   Move-Item -LiteralPath "$HOME/.claude/agents/dual-agent-review-turn.md" -Destination "$HOME/relay-retirement-2026-10/dual-agent-review-turn.md"
   ```

   `Test-Path` on the old path must then print `False`. Undo: move it back. Until A2, Claude sessions
   on that machine still list a `dual-agent-review-turn` agent type.
4. **A3: deploy the changed canonical instructions and skills on each machine,** from a full clone
   whose `main` holds the integrated remediation, as the common body requires after a canonical
   change: `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config`, then
   `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check`, which must report
   `USER_CONFIG_PROBLEM_COUNT=0`. The remediation changes the skills `hebrew-prose` (C10.3, C15.15),
   `mam-wikisource-refresh` (C1, C8), `mam-repository-topology` (C15.24) and `github-issues`
   (C15.25), and stops deploying the agent file. On `LAPTOP-DBLE8UKA` it is step 4 of "Final
   integration"; on the relay machine the relay-machine session does it. Any other machine of Ben's
   that has the agent file needs A3 and A2 as well, which the relay-machine session's prompt also
   does there (its step 3).
5. **A4: retire the relay's three worktrees on the relay machine,** each below
   `C:/Users/BenDe/GitRepos2/MAM-basics`: `.claude/worktrees/dar-2026-10-01-claude` (branch
   `dar-2026-10-01`) and `.claude/worktrees/dar-2026-10-01-codex` (branch
   `dual-agent-review-2026-10-01-codex`), both locked with the reason "active automated dual-agent
   review 2026-10-01", and `.claude/worktrees/dar-comparison-2026-10-01-claude`, detached at
   `dd50e9b9` and locked by the comparison operator. Every task that used them ended on 2026-10-01.
   Follow `mam-repository-topology/references/repository-maintenance.md`, "Completed linked
   worktrees", only once that clone runs code with C9.1's handler, from the clone's root with its own
   interpreter. For each worktree, with `<W>` its absolute path and `<name>` its last path component:
   1. `git -C C:/Users/BenDe/GitRepos2/MAM-basics worktree unlock <W>`, since that procedure's gate 1
      refuses a locked worktree.
   2. `./.venv/Scripts/python.exe py/main_repo_util.py --inspect-worktrees --worktree "<W>"`.
   3. `./.venv/Scripts/python.exe py/main_repo_util.py --prepare-worktree-retirement "<W>" --task-ended --retirement-root "$HOME/relay-retirement-2026-10/worktree-retirements" --preflight-file "$HOME/relay-retirement-2026-10/preflight-<name>.json"`.
      If it reports tracked references to `.novc` paths that it will relocate, and every one of them
      is in the October 1 round's records (`doc/dual-agent-review-2026-10-01-*.md`,
      `doc/PLAN-close-out-review-2026-10-01.md` and `doc/dual-agent-review-comparison-2026-10-01.md`),
      prepare again to the new file `preflight-<name>-2.json` in the same folder, adding
      `--citations-reviewed --citation-note "Historical citations in the finished records of the October 1, 2026 relay round; each relocated path is recorded in the retirement sidecar and in the relay-machine session's dated entry in doc/dual-agent-review-2026-10-01-turn-01-claude-update.md."`,
      and record each relocated path in that entry.
   4. Read the newest preflight, then run
      `./.venv/Scripts/python.exe py/main_repo_util.py --execute-worktree-retirement "<preflight>" --task-ended`.

   Any other blocker that the procedure reports, a session record or runtime lease among them, stops
   this act for that worktree: record the blocker and lock the worktree again with
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics worktree lock --reason "relay retirement blocked: <blocker>" <W>`.
   Never bypass a gate, remove a lease or force a removal. The tooling keeps both branches, since
   neither name has an agent prefix; A5 deletes them.
6. **A5: delete the two local branches** `dar-2026-10-01` and `dual-agent-review-2026-10-01-codex` on
   the relay machine, after A4. Record each tip with
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics rev-parse <branch>`, then delete it with
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics branch -d <branch>` only. Both are contained in `main`;
   `-d` refuses a branch that is unmerged or still checked out in a worktree that A4 left in place,
   and such a refusal is recorded, never overridden. Undo: recreate the branch at its recorded tip.
7. **A6: not done.** `origin/dar-2026-10-01`, whose tip `db59ef5e` is contained in `main`, stays, as
   the other round branches on origin do.
8. **A7: keep the relay's control state and evidence outside the clone,** after A1, since routine
   maintenance's wipe of `.novc/` would delete them. Copy these top-level entries of the relay
   machine's `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/`, where present, to
   `$HOME/relay-retirement-2026-10/novc/`, keeping each relative path and overwriting nothing:
   `dual-agent-review/` (the registry, the round's `PAUSE`, the deactivation record and
   `scheduler.log`); every entry whose name contains `relay` or `dual-agent-review`; and every other
   entry that the relay's runbook or plan at `<ARCHIVE-SHA>`, or the October 1 round's records, name
   with the pattern `[.]novc/[A-Za-z0-9_.-]+`; but not `t`, the suite's disposable temporary root.
   Use a scratch Python script in the session's scratch directory. It also writes
   `$HOME/relay-retirement-2026-10/novc-manifest.json`, with the source root, the copy's time with its
   UTC offset, and each file's relative path, bytes and SHA-256, and then verifies every copy's hash
   against its source. Leave the originals for maintenance's next wipe.
9. **A8: retire the rehearsal home `C:/Users/BenDe/GitRepos-rehearsal/`,** if A0 finds it. It holds
   the relay's rehearsal fixtures: a public-source MAM-basics clone with its own environment, its
   local bare origin and their evidence. Record its top-level entries, file count and total bytes,
   and check that no worktree in A0's list lies inside it; then, with the retention folder created
   as in A2, move the home there on the same volume:

   ```powershell
   Move-Item -LiteralPath C:/Users/BenDe/GitRepos-rehearsal -Destination $HOME/relay-retirement-2026-10/GitRepos-rehearsal
   ```

   If the move fails, record why and leave the home where it is. Undo: move it back.
10. **A9, Ben's: the paused Codex follow-up `verify-first-production-dual-agent-review`.** Ben
    approved it in a Codex chat on 2026-10-01, and it was paused after the round's verification
    (`doc/dual-agent-review-automation.md` at `<ARCHIVE-SHA>`). It lives in the Codex app's own state,
    for which this plan has no verified command, so no session touches it: if the Codex app still
    lists it, Ben deletes it there. While paused it runs nothing.
11. **A10: delete `origin/remediate-review-2026-10-02` and the local branch,** at step 5 of "Final
    integration", once `origin/main` contains the branch's tip. Record the tip; check with
    `git -C <checkout> merge-base --is-ancestor origin/remediate-review-2026-10-02 origin/main`; then
    run `git -C <checkout> push origin --delete remediate-review-2026-10-02` and
    `git -C <checkout> branch -d remediate-review-2026-10-02`. Undo: push the recorded tip again.

### The relay-machine session

Ben starts this session on the relay machine after the executor's final integration, with the prompt
below, in the full clone `C:/Users/BenDe/GitRepos2/MAM-basics` itself rather than a new worktree. It
uses that clone's own `./.venv/Scripts/python.exe` from the clone's root, and in the repository it
writes only step 8's records. Ben may start the same prompt on any other machine of his that has the
agent file; step 3 covers that case.

1. Load `AGENTS.md`, `mam-repository-topology` with `references/repository-maintenance.md`, and
   this plan's "The relay's retirement", reading the plan from `origin/main` after step 2's fetch.
2. Verify with separate commands. `git rev-parse --show-toplevel` in the session's working directory
   must print `C:/Users/BenDe/GitRepos2/MAM-basics`;
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics branch --show-current` must print `main`; and
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics status --porcelain=v1 -z` must print nothing. Then
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics fetch origin`. Line 3 of this plan at `origin/main`
   (`git -C C:/Users/BenDe/GitRepos2/MAM-basics show origin/main:doc/PLAN-remediate-review-findings-2026-10-02.md`)
   must begin "State: live; remediation integrated on main"; if it does not, the executor has not
   finished, so stop and report without acting. Read `<REMOVAL-SHA>` and `<ARCHIVE-SHA>`, its parent,
   from the entry "Relay retired, <date>" of `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md`
   at `origin/main`.
3. A0. If A0 finds none of the scheduled task, `.novc/dual-agent-review/` and A4's three worktrees,
   this is not the relay machine: fast-forward as in step 5; do A3, and A2 if the agent file exists;
   record that in step 8's entries without changing this plan's State; and report, so that Ben can
   start this session on the relay machine.
4. A1, then A7.
5. Fast-forward with `git -C C:/Users/BenDe/GitRepos2/MAM-basics merge --ff-only origin/main`. The new
   `HEAD` must contain `<REMOVAL-SHA>`, which the October 1 update's entry "Relay retired, <date>"
   names: `git -C C:/Users/BenDe/GitRepos2/MAM-basics merge-base --is-ancestor <REMOVAL-SHA> HEAD`.
6. A3, then A2.
7. A4, then A5; then A8.
8. Records: a dated entry "Relay retirement acts on <machine>, <date>" in
   `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md`, naming the machine and recording each
   act's outcome, each relocated `.novc` path, the branches' recorded tips and the retention folder's
   contents; a dated entry pointing to it in `doc/review-findings-2026-10-02-update.md`; and, on the
   relay machine, this plan's line 3 set to "State: executed <date>", naming any act left blocked or
   to Ben. Run
   `./.venv/Scripts/python.exe py/main_test.py py/tests/test_receipt_update_links.py py/tests/test_prose_conventions.py py/tests/test_prose_mark_order.py`,
   `git -C C:/Users/BenDe/GitRepos2/MAM-basics diff --check`, and once more
   `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check`, which must report
   `USER_CONFIG_PROBLEM_COUNT=0`. Commit on `main` with a message file; fetch, merging `origin/main`
   if it moved; and push `main`. These records change no source or product, so nothing else is owed.
9. The final report begins with "# Report:" and gives each act's outcome, the retention folder's path
   and size, and what is left to Ben: A9 in the Codex app, if the follow-up is still listed; deleting
   the retention folder whenever he wants the space; and the exact command for any act that the
   session's rules refused.

The prompt that starts it, for Ben to paste:

> Written by Claude Opus 5.5 on 2026-10-03, New York time, in the MAM-basics session on
> `LAPTOP-DBLE8UKA` that prepared `doc/PLAN-remediate-review-findings-2026-10-02.md`. Ben's
> instructions in that session, verbatim: "Regarding my choices, I accept all your
> recommendations."; "I accept all those recommendations as well."; and "Please authorize those acts
> in advance. I want this all to be as unattended as possible." The rest of this prompt is that
> session's reconstruction, not Ben's words.
>
> Run unattended, at max effort. You are "The relay-machine session" of that plan. Your working
> directory must be the full MAM-basics clone `C:/Users/BenDe/GitRepos2/MAM-basics` on this machine
> itself, not a new worktree. Fetch `origin`, read the plan from `origin/main`, and carry out its
> section "The relay-machine session" exactly, with the acts under "Acts outside the repository"
> that it names. Ben authorized every one of them in advance: do not ask him again. You own the
> records commit on `main` and its push. Stop on a failing check or a fact that contradicts the
> plan, record what was done, and report with a standalone continuation prompt. Begin your final
> message with "# Report:".

## Finite execution ledger

"Active" means an approved disposition whose execution is pending; it claims nothing is fixed. "D"
marks a reproducible defect and "E" an editorial change, under `doc/periodic-review.md`, "Separate
defects from editorial proposals"; the risk column follows "Present remediation by public-facing
risk".

| Item | Status, kind and scope | Risk | Wave | Question |
|---|---|---|---|---|
| C1.1 | Active. D: the claims gate's trigger (Gate B); E: `Yeivin-ITM/README.md`. | lower; blocks the next refresh | 3 | 7 |
| C1.2 | Active. D: the frozen legacy projection oracle (Oracle A); E: `Phonetic-MAM/README.md`. | lower; blocks the next refresh | 3 | 7 |
| C1.3 | Active. D: `py/phonetic_mam/legacy_projection.py` removed (wave 3); E: the refresh procedure's re-approval text (wave 6). | lower | 3, 6 | 7 |
| C2 | Active. D: the classifier, the survey, the claims and pins; E: the corrected prose on three pages, figures only, keeping "roughly". | published pages, distributed data | 3 | 1 |
| C4.1 | Active. E: the font row's link. | reader-facing | 5 | — |
| C4.2 | Active. E: the font row's duties sentence; no published change. | reader-facing | 5 | — |
| C4.3 | Active. E: two `LICENSE.md` files and three rows; D: three closed file sets; a recurrence lint. | distributed data, reader-facing | 5 | — |
| C4.4 | Active. E: the exception in `MAM-with-doc/LICENSE.md` (option 1). | reader-facing | 5 | 4 |
| C4.5 | Active. E: the six modules declared GPL-3.0 code (option 1). | reader-facing | 5 | 5 |
| C4.6 | Active. E: `DATA-LICENSES.md:58`, `Yeivin-ITM/README.md:37–40`. | reader-facing | 5 | — |
| C4.7 | Active. E: the README and `DATA-LICENSES.md` exceptions and two rows. | reader-facing | 5 | — |
| C4.8 | Active. E: two README list items. | reader-facing | 5 | — |
| C5.1 | Active. E: `Phonetic-MAM/README.md`; D: the U+05C5 guard. | distributed data (README) | 4 | — |
| C5.2 | Active. E: the README's disclosure of two text differences. | distributed data (README) | 4 | — |
| C6.1 | Active. D/E: the citation, "Is 52:1" (option 1), and a reference lint. | published page | 3 | 2 |
| C6.2 | Active. D: the migration gate (option C); E: the editing procedure. | lower (README reader-facing) | 2 | 8 |
| C7 | Active. E: the bot guide. | lower | 6 | — |
| C8 | Active. E: the refresh skill's steps 4 and 5 (option 1). | lower | 6 | 9 |
| C9.1 | Active. D: the handler, the guarded wipe and the lint. | lower | 7 | — |
| C9.2 | Active. D: two imports in wave 4, three content fixes in wave 3, E402 by C15.18, F841 by R1. | lower | 1, 3, 4 | (8) |
| C9.3 | Active. D: skip the caller's own clone; E: two runbook passages. | lower | 7 | — |
| C9.4 | Active. D: the launch lint. | lower | 7 | — |
| C9.5 | Active. D: the handler; the simulation's input. | lower | 7 | — |
| C10.1 | Active. E: help text, comments and a docstring in seven files. | lower | 8 (item 8 in 3) | — |
| C10.2 | Active. E: `doc/phonetic-mam-preparation.md`. | lower | 8 | — |
| C10.3 | Active. E: two `hebrew-prose` references. | lower | 8 | — |
| C10.4 | Active. E: two docstrings and `AGENTS.md`. | lower | 8 | — |
| C11 | Active. D: the floor fix; E/D: the core pipeline, marked and linted (option 2). | reader-facing (diagram) | 6 | 6 |
| C12.1 | Active. D: the encoding check and a lint. | lower | 6 | — |
| C12.2 | Active. D: an independent oracle; E: the docstring. | lower | 3 | — |
| C12.3 | Active. D: two untangler tests. | lower | 4 | — |
| C12.4 | Active. D: a closed dispatch that declines nested helpers (option 1). | lower | 6 | 10 |
| C13.1 | Active. D: the compute stream. | lower | 4 | — |
| C13.2 | Active. D: the `:has()` fallback. | published pages | 4 | — |
| C14 | Resolved by Ben ("Keep the legacy bytes"). Active: the citation at the exemption. | lower | 4 | — |
| C15.2 | Active. E: one in-place link, one dated update entry. | lower | 8 | — |
| C15.3 | Active. D. | lower | 7 | — |
| C15.4 | Active. D: eleven programs. | lower | 7 | — |
| C15.5 | Active. E. | lower | 7 | — |
| C15.6 | Active. E: a docstring. | lower | 4 | — |
| C15.7 | Active. E: the README's `render` sentence. | distributed data (README) | 4 | — |
| C15.8 | Active. D: two index pages' attribution link. | published pages | 4 | — |
| C15.9 | Active. E. | reader-facing | 5 | — |
| C15.10 | Active. E. | reader-facing | 5 | — |
| C15.11 | Active. D. | lower | 5 | — |
| C15.12 | Active. D: two attribute lines. | lower | 5 | — |
| C15.13 | Active. E; one flagged addition. | lower | 8 | — |
| C15.14 | Active. E: a README sentence; the `$id` stays. | distributed data (README) | 3 | — |
| C15.15 | Active. E: `hebrew-prose`'s rule scoped; the claim data unchanged (option 1). | lower | 8 | 3 |
| C15.16 | Active. E. | distributed data (README) | 3 | — |
| C15.17 | Active. E: a step note. | lower | 3 | — |
| C15.18 | Active. D. | lower | 4 | — |
| C15.19 | Active. D. | lower | 4 | — |
| C15.20 | Active. D: a rename. | lower | 4 | — |
| C15.21 | Active. E. | lower | 4 | — |
| C15.22 | Active. E. | lower | 4 | — |
| C15.23 | Active. E: `AGENTS.md`. | lower | 8 | — |
| C15.24 | Active. E: six commands. | lower | 8 | — |
| C15.25 | Active. E: "Five" kept, with a paragraph on the two routed trackers (option 1). | lower | 8 | 11 |
| C15.26 | Active. E. | lower | 7 | — |
| C15.27 | Active. E: a comment. | lower | 7 | — |
| C15.28 | Active. D: the lint. | lower | 7 | — |
| C15.29 | Active. E: two update files (option 1), and a "Recorded by" line. | lower | 8 | 12 |
| C15.30 | Active. E: one credit. | reader-facing | 5 | — |
| C15.31 | Active. E: `trope#NN (private tracker)` (option 1). | lower | 3 | 13 |
| C3 | Fixed after the review, by deployment; no action. The residue phonetic-hbo clone stays Ben's decision. | — | — | — |
| C15.1 | Rejected; no action. | — | — | — |
| R1–R7 | Active: the relay's retirement in the repository. | lower | 1 | — |
| A0–A10 | Authorized in advance on 2026-10-03; A6 not done. The executor does A2, A3 and A10 on `LAPTOP-DBLE8UKA`; the relay-machine session does the rest. | outside the repository | 9, 10 | — |

The items of the update's "Not findings" paragraph (the six items noticed outside the diff, the
seven declared open ends and the oleh-weyored at Psalms 44:4) get no action here.

## Outputs expected to change, and everything that must not

Any other diff in a generated output is a finding and blocks integration until explained.

1. **Generated outputs this plan changes, each read line by line:**
   - C2: `out/accgram/meteg-before-stress.json` (the 82-line diff its entry describes),
     `Yeivin-ITM/meteg-claims.json` (line 5 and the 11 corrected measurements) and eleven lines of
     three Yeivin pages (`yeivin_itm-318_344.html:539`, `:541`, `:542`, `:552`, `:553`, `:556`;
     `yeivin_itm-huge-ftnt-320.html:13`, `:70`, `:71`, `:84`; `yeivin_itm-huge-ftnt-322.html:36`);
   - C6.1: two lines of `gh-pages/yeivin-itm/yeivin_itm-207_285.html`;
   - C13.2: `gh-pages/phonetic-mam/style.css` and `gh-pages/phonetic-mam/pronunciation.js`;
   - C15.8: one line each of `gh-pages/phonetic-mam/index.html` and `gh-pages/MAM-with-doc/index.html`;
   - C11: `doc/process-documentation/pipeline.dot` and `pipeline.svg`.
2. **Authored or frozen files this plan adds or removes:** the two product `LICENSE.md` files (C4.3);
   `in/phonetic_mam_legacy_projection_inputs.json` (C1.2, Oracle A);
   `in/yeivin_itm_published_anchors.json` (C6.2, option C); `py/mb_misc/mam_attribution.py` (C15.8);
   the new lints and tests the items name; the relay's ten files and
   `py/phonetic_mam/legacy_projection.py`, removed; and two update files under `holman/doc/` (C15.29,
   option 1).
3. **Unchanged:** every other file under `gh-pages/`, including the other 14 Yeivin pages, every other
   Phonetic MAM page, every change log under `gh-pages/MAM-with-doc/change-log/` and every other
   MAM-with-doc page; `Phonetic-MAM/data/` and `Phonetic-MAM/examples/display.json` (C14 keeps the
   legacy bytes, and C5.2 discloses rather than changes); `MAM-parsed/`, `MAM-simple/`,
   `MAM-for-Sefaria/` and `MAM-OSIS/`; `MAM-with-doc/` apart from `LICENSE.md` (C4.4);
   `out/accgram/post-stress-meteg.json` (C12.4); `Yeivin-ITM/meteg-claims.json` apart from C2's
   changes (C15.15's option 1 leaves its exclusion strings alone); `in/mam-ws/`, `in/mam-ws-special/`
   and `in/mam-ws-intro/`; `in/phonetic_mam_legacy_projection_sha256.json`, which is never
   regenerated; `in/yeivin_itm_legacy_differential.json` apart from C15.16's description and, while a
   test still reads it, C2's rewritten change records; `hbce-psalms/out/`; and every finished base
   receipt, apart from the line-4 pointers that C15.29 adds to the two Holman records.
4. **Not touched:** MAM-private and hbofonts, which only the suite's and the mega's documented steps
   read, and C15.20's export check through the same adapter; and the live deployed instructions,
   skills and agent file, until acts A2 and A3.

## Execution, verification and integration

### Waves

The waves order the work by dependency; they do not permit implementing only part of the plan. Ben
has answered every question, so no item waits on him. Within a wave the executor may choose smaller
coherent commits and read-only sub-agents, keeping one writer.

1. **Wave 0, the start.** The checks and the branch under "Standalone executor contract". The first
   commit sets this plan's line 3 to "State: live; Ben's choices and advance authorization recorded
   2026-10-03; execution started <date>".
2. **Wave 1, the relay's retirement in the repository (R1 to R7).** One commit holds R1 to R4, R6 and
   R7, because the D13 note and the October 1 update's entry cite that commit's parent as
   `<ARCHIVE-SHA>`; R5's lint goes in the same commit or the next. This wave also removes C9.2's
   F841. An executor working on the relay machine itself would do A1 first.
3. **Wave 2, the Yeivin migration gate.** C6.2's option C (question 8), since C6.1, C9.2's
   content-module fixes and C15.31 cannot pass today's Yeivin tests.
4. **Wave 3, the survey, the gates and the Yeivin product.** C2 and C12.2 first (question 1), under
   today's claims gate, as C2's "Order" gives them; then C1.1 and C1.2 (question 7: Gate B and Oracle
   A), whose new records are set from the corrected survey and the unchanged MAM-parsed input, with
   C1.3's removal of `py/phonetic_mam/legacy_projection.py` and its dated record; then C6.1 (question
   2); C15.31 (question 13); C9.2's three content-module fixes; C15.14; C15.16; and C15.17 in one
   commit with C10.1's item 8.
5. **Wave 4, Phonetic MAM.** C13.2 and C15.8 with their regenerated pages; C5.1, C5.2 and C15.7 in
   `Phonetic-MAM/README.md`, with C5.1's guard and the finding-22 pointer; C13.1 and C15.18 in one
   commit (C15.18 removes C9.2's eleven E402); C15.19; C15.20, with its export check at once; C12.3;
   C9.2's two other unused imports; C14's citation; C15.6, C15.21 and C15.22.
6. **Wave 5, licences and the reader-facing documents.** C4.1 to C4.8, C15.9 to C15.12 and C15.30,
   with C4.3's two `LICENSE.md` files and their three closed sets in one commit, and every
   `DATA-LICENSES.md` change of C4.1, C4.2, C4.3, C4.4, C4.5, C4.6, C4.7, C15.9 and C15.10 applied in
   one planned sequence.
7. **Wave 6, the Wikisource tooling and the refresh procedure.** C7; C8 (question 9); C11 (question 6);
   C12.1; C12.4 (question 10); C1.3's procedure text, after wave 3 has implemented question 7's
   designs.
8. **Wave 7, repository tooling.** C9.1 and C9.5 with their handler and lint; C9.3; C9.4; C15.3; C15.4;
   C15.5; C15.26; C15.27; C15.28.
9. **Wave 8, stale descriptions, instructions and records.** C10.1 to C10.4 (C10.1's item 8 went in
   wave 3), C15.2, C15.13 with its approved addition, C15.15 (question 3), C15.23, C15.24, C15.25
   (question 11) and C15.29 (question 12); then the first entry of "Records", item 1.
10. **Wave 9, on `LAPTOP-DBLE8UKA`: the full suite and final integration,** with A3, A2 and A10 there
    and the closing records.
11. **Wave 10, on the relay machine: "The relay-machine session",** which Ben starts after wave 9's
    push of `main`.

### Checks for every commit

1. Verify `HEAD` and task-owned status before staging, and stage only this plan's paths.
2. `git -C <checkout> diff --check`.
3. Black at its defaults on every changed Python file, with
   `./.venv/Scripts/python.exe -m black <files>`, and
   `./.venv/Scripts/python.exe -m ruff check --no-cache <files>`.
4. For a commit that changes Markdown, an update file or an instruction:
   `py/main_test.py py/tests/test_receipt_update_links.py py/tests/test_prose_conventions.py py/tests/test_prose_mark_order.py`.
5. The item's own verification, as its entry above gives it.
6. A generator's output is regenerated with the documented command and committed with its source
   change, after every line of its diff has been read and explained.
7. Write each multi-line commit message to a uniquely named UTF-8 file in a gitignored scratch
   directory and commit with `git commit -F`; push every commit with
   `git -C <checkout> push origin HEAD:remediate-review-2026-10-02`. Never force; stop on a refused
   push. Do not push `main` before final integration.

### The full suite

Run `py/main_test.py` once, after the last executable, test, schema or shared-data change; a later
documentation, comment or instruction commit does not expire it. At `644a6c9c` it passed 1,056 with
5 skipped and 60 subtests. Record the new counts with the commit, and explain the difference
exactly: minus the relay's 15 tests, plus each new test this plan adds, with the subtests and skips
unchanged unless an entry above says otherwise.

### Final integration

1. In the checkout, fetch `origin` and merge current `origin/main` into the branch. Resolve any
   conflict there, and repeat the checks whose inputs the merge changed.
2. Run the mega from the checkout's root with no `REPOS_ROOT`:
   `./.venv/Scripts/python.exe py/main_0_mega.py`. A failing step or an unexplained tracked diff is a
   failure. Since every wave committed its own regenerated outputs, the expected diff is empty; read
   and explain any line it shows, commit each explained change, and push the branch.
3. Fetch with `git -C <checkout> fetch origin` and verify that `origin/remediate-review-2026-10-02` is
   exactly the mega-verified commit. Switch with `git -C <checkout> switch main`, fast-forward with
   `git -C <checkout> merge --ff-only origin/remediate-review-2026-10-02`, and push with
   `git -C <checkout> push origin main`. This push reaches the published Pages tree at the next
   04:17 deployment and the distributed products at once; it is outward-facing, and it is the
   integration that Ben accepted with this plan on 2026-10-03. It need not wait for A1 ("Acts
   outside the repository"). If the fast-forward or the push is refused because `origin/main` moved,
   switch back to the branch, merge the new `origin/main`, repeat the owed checks and the mega if a
   generator input moved, push the branch, and retry. Never merge in `main` here and never force.
4. **A3, then A2, on this machine,** as "Acts outside the repository" gives them. A3 deploys from the
   `origin/main` just pushed, and its `--check` must report `USER_CONFIG_PROBLEM_COUNT=0`.
5. **A10,** once `origin/main` contains the branch's tip. The clone stays on `main`.
6. **The closing records** ("Records" below), committed directly on `main`: they change no source,
   product or canonical configuration, so the suite, mega and deployment evidence stands. Run the
   checks for Markdown, fetch, and if `origin/main` moved merge it into `main` under the ordinary
   full-clone rule (step 3's rule protects only the mega-verified integration); then push `main`.
7. Leave the clone on clean `main`. The final report gives the outcome of every wave and act, and ends
   with the prompt under "The relay-machine session" for Ben to start on the relay machine.

### Records

1. In `doc/review-findings-2026-10-02-update.md`, dated entries on the model of the September 29
   round's: "Remediation implemented; final gates pending, <date>", committed on the branch after
   wave 8, recording the checkout's path and the `HEAD` at which editing began, the option
   implemented under each of Ben's thirteen answers, and a disposition for every row of the ledger
   above, mapped onto `implemented`, `superseded`, `deferred` or `unresolved`; then "Final
   integration completed, <date>", committed at step 6 of "Final integration", with the suite
   counts, the mega result, the commits, the deployment check, the outcomes of A2, A3 and A10 on
   `LAPTOP-DBLE8UKA`, and the relay machine's acts still to come. The Claude report's own line 3
   stays as written. In the same commit, `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md`
   gains a dated entry "Relay retirement acts on LAPTOP-DBLE8UKA, <date>", with the outcomes of A3
   and A2 there.
2. In `doc/dual-agent-review.md`, item 5 of "The MAM-basics trial review, kicked off 2026-10-02" gains,
   in the closing records' commit, the sentence: "On 2026-10-03 Ben accepted the recommendations of
   the remediation plan, `doc/PLAN-remediate-review-findings-2026-10-02.md`, and authorized its acts
   in advance; its remediation reached `main` on <date>, and the update file records the
   dispositions."
3. In the closing records' commit, this plan's line 3 becomes "State: live; remediation integrated on
   main <date>; the relay machine's acts remain, under "The relay-machine session"". That session's
   records commit makes it "State: executed <date>", naming any act left blocked or to Ben; the plan
   is then a receipt, corrected later only through a single update file.
4. The dated entries that individual items write into other update files (R7's October 1 entry,
   C5.2's finding-22 pointer, C15.2's and C15.29's) belong to their items' commits, and the
   relay-machine session's entries to its records commit.
