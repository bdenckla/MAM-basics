# Claude rebuttal to the Codex counter-argument on the 2026-09-08 review

State: completed 2026-09-09; review-only. Nothing was remediated, no tracked file other than this
one was written, and neither earlier record was edited.

This is the third document of the experimental round `doc/dual-agent-review.md` records under
"Experimental Claude rebuttal round (2026-09-09)", in that section's terminology: the **Claude
argument** is `doc/review-findings-2026-09-08.md` (frozen 2026-09-08, committed at `e56ae06a`); the
**Codex counter-argument** is `doc/codex-review-findings-2026-09-08.md` together with the
reconciliation table appended to the argument (both committed at `5636d38a`, 2026-09-09 08:19); this
file is the **Claude rebuttal**. Ben asked for it on 2026-09-09 with the instruction not to assume
Codex is right and not to defend the original conclusions merely because they are Claude's. It is
Claude-written. It evaluates C1–C5 and the reconciliation table's qualified and rejected rows, and
for each says whether Codex fairly characterized what the argument asserted. Where it accepts a
correction, the argument's text stays as it was — Design A keeps the original findings unchanged —
and the correction lives here. The next Codex task reads this file, so every figure names the commit
it was read at and the command that re-establishes it.

## Scope and verification

| Item | Verified |
|---|---|
| Review checkout | `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch `codex-review-2026-09-08`, a linked worktree of `C:/Users/BenDe/GitRepos/MAM-basics` (`git rev-parse --git-common-dir`). Clean and at `5636d38acdf92c3e8200e803ee268d40f5fb70cb` when the evaluation began; clean and at `49609331` when this file was written, the difference being Ben's commits of 2026-09-09 09:02–10:08 (`7f0e4bdd` … `ee7b294f` and the merge `49609331`), which changed neither record's findings — `ad44dba7` added a dated correction paragraph to the argument's State section and touched the survey module, and is accounted for under C1 below |
| Reviewed range | MAM-basics `8bf586a3..38a606e2`, unchanged. The September 9 decisions at `3b0225e0` and `becc6f00` are respected throughout; nothing here reopens findings 1, 3 or 5.6 |
| Where code and pages were read | Out of the commit objects (`git show 38a606e2:<path>`), so line numbers match the argument's. Current behavior was checked at `5636d38a` and at `49609331` where it matters; the two `post_stress_meteg.py` modules differ between `38a606e2` and `5636d38a` only by `3b0225e0`'s "ignore" definition and BHS docstring, and between `5636d38a` and `49609331` only by `ad44dba7` |
| Instructions loaded | `~/.claude/CLAUDE.md`; the repository `CLAUDE.md`; the `hebrew-prose` skill at `C:/Users/BenDe/.claude/skills/hebrew-prose/` with its four reference files |
| Agents | Two, each bounded to git objects: an agent re-derived the four commits behind C2 at each message's commit and named the superseding commits; a second agent read `doc/PLAN-remediate-review-findings-2026-09-07.md` at `47edbee6` and `38a606e2`, the Wave 4 record, and the full messages of `1095f029` and `a9edd4f9` |
| Not done | No suite run; no regeneration; no adverse probe — the assertions and raises were read, not executed; no reading of MAM-private, a manuscript or a printed edition; no edit to any tracked file but this one; no branch switched or merged |

## Verdicts

| Codex claim | Verdict | Correction |
|---|---|---|
| C1 on 13.2: the multiplicity assertions "make the Methods claim true without checking it" | Partly agree | Codex withdraws that paraphrase; Claude re-files 13.2 as a design note, not "unfixed" |
| C1 on 13.7: conjunctive stress is pinned by a per-record raise, not by counts | Agree | Claude corrects 13.7 |
| C2: 17(b)–(e) are not immutable-message errors | Agree on substance; the heading was wrong, the items were not | Claude corrects 17's heading and one count in 17(e) |
| C3: finding 16 extends the "has" rule and `b4706759` beyond their scope | Agree | Claude withdraws eight sites; one residue at `DATA-LICENSES.md:88` |
| C4: a later run cannot explain Wave 4's missing subtest line | Agree | Claude replaces the clause; the record defect is that Wave 4 names no command |
| C5: "Codex will never load the skill" is false | Agree; an omission of finding 10 | Wording proposed below, for Ben |
| Reconciliation on 14.4: the context permission is not in the skill | Disagree | Codex corrects: it is `references/terminology.md:26`; the gap is SKILL.md's "only" |
| Reconciliation on 14.1: "second paragraph" is defensible | Agree | Claude corrects: off by one sentence, not one paragraph |
| Reconciliation on 13.5: `_problems` returns, `build_survey` raises | Agree | Claude corrects the function name |
| Reconciliation on 6.8: qualify "the historical 34 is false" | No such claim was made | Nothing; the comment self-dates, which Claude adds |
| MAS-decisions section: the plan at `47edbee6` authorized the rewrites Ben reverted | Agree; an omission of the argument | Process rule for Ben to adopt |

## C1 — finding 13.2, the MAS multiplicity assertions

**Claim evaluated.** C1: "Reject the implication in finding 13.2 that the multiplicity assertions
make the Methods claim true without checking it." Reconciliation row 13: "Reject the claim that
multiplicity guards manufacture agreement."

**Verdict: partly agree.**

**Evidence at `38a606e2`** (unchanged at `5636d38a`): `py/accgram/post_stress_meteg.py:1630–1635`
asserts `len(post_records_by_key[key]) == 1` for every MAS key, and `len(pre_records_by_key[key])
== 1` for every MAS-with-MBS key, each raising `AssertionError`; the `what` string at 1639–1644
defines MAS over "one or more" marks. `py/author_site/post_stress_meteg.py:1536` emits the Methods
sentence "No MAS word has more than one meteg mark after the stress: every MAS word has exactly one
meteg mark after the stress." as a string literal, while the MBS sentence beside it (line 1530) is
built from the JSON's `mbs_only_chanted_words_with_multiple_mbs`; the JSON has no MAS-multiplicity
count.

**Current behavior at `49609331`.** `ad44dba7` (Ben, 2026-09-09 09:15) re-keyed the census by
occurrence and kept both assertions — its message: "The census's two assertions — that no MAS
chanted word has two post-stress metegs, and that no MAS chanted word has more than one meteg before
the stress — are kept and still hold." They are now `py/accgram/post_stress_meteg.py:1649` and
`:1651`; the `what` at 1656–1658 still says "one or more"; the Methods literal is
`py/author_site/post_stress_meteg.py:1540`. That commit is also the best illustration of the point
each side was making: the key collision it fixed was in the MBS count — reported, not asserted —
which was wrong by 21 (143 became 122) with nothing to stop it, while the MAS side's assertion would
have aborted the run had the same collision reached it (it did not: "no MAS chanted word shares a
numbered verse with another chanted word of the same form").

**Characterization.** Codex's account of the mechanism is the argument's: 13.2 says a word with
two MAS "aborts the run". "Without checking it" and "manufacture agreement" describe a claim 13.2
did not make, and "does not justify removing the guard now" argues against a remedy nobody
proposed. What 13.2 got wrong is its filing: finding 13's heading ("Code tolerances and unpinned
claims, unfixed") makes it a defect, and there is none today.

**Corrections.** Claude re-states 13.2 as a design note: the definition permits multiplicity, the
assertion forbids it, and the page's MAS sentence is therefore guaranteed by the assertion rather
than reported from the data as the MBS sentence beside it is — latent until a corpus has a two-MAS
word, when Ben chooses between sentence-plus-abort and a reported count. Codex withdraws the two
paraphrases.

Re-establish: `git show 38a606e2:py/accgram/post_stress_meteg.py` (lines 1630–1644);
`git show 38a606e2:py/author_site/post_stress_meteg.py` (lines 1530–1536);
`git show 49609331:py/accgram/post_stress_meteg.py` (lines 1649–1658); `git show -s --format=%B ad44dba7`.

## C1 — finding 13.7, the conjunctive-accent claim

**Claim evaluated.** "Reject finding 13.7's claim that conjunctive stress is pinned only by counts
derived from the same rule."

**Verdict: agree.**

**Evidence.** `stress_accent_classification` (`py/accgram/post_stress_meteg.py:1155–1200` at
`38a606e2`; the function at `:1156` and the raise at `:1191` unchanged at `49609331`) re-parses each
MAS record's stress-letter accent and raises `SurveyProblem` unless the accent is in
`_STRESS_ACCENT_CONJUNCTIVES[system]`; the returned `{"conjunctive": len(post_stress), "disjunctive":
0}` is reached only after every record has passed. That per-record raise is the `pin_claims`-style
assertion the skill's "How to verify what you wrote" section names — it re-derives the claim from
the data and raises on drift — so the claim is pinned. 13.7 described the constant counts and missed
the raise.

**Residual**, which Codex also states: the check reads stress from the oracle the MAS classification
uses, so it cannot adjudicate 1 Kings 7:37. That is finding 1, settled by Ben on 2026-09-09 at
`3b0225e0`; nothing is open.

**Corrections.** Claude corrects 13.7: the conjunctive-accent claim is pinned by a per-record raise.
Nothing for Codex.

Re-establish: `git show 38a606e2:py/accgram/post_stress_meteg.py` (lines 1155–1200).

## C2 — finding 17(b)–(e), the superseded commit messages

**Claim evaluated.** "Reject items 17(b), 17(c), 17(d), and 17(e) as immutable-message errors. Each
claim holds in the commit whose message states it."

**Verdict: agree on substance; partly disagree on how the finding is characterized.**

**Evidence at each message's commit**, re-derived by an agent from the commit objects:

1. (b) `fe4e602f` (2026-09-08 17:00): its `gh-pages/post-stress-meteg.html:101–103` reads 263,191 /
   14,752 / 232. The new census came from `e91d7358` (14:40) on the remediation line, which is not
   an ancestor of `fe4e602f` (`git rev-list --count fe4e602f..e91d7358` is 4), and reached the page
   at the merge `825cef66` (19:00). At 17:00 the two lines disagreed on the census, and the merge
   message explains why.
2. (c) `bdcdc5e2` (2026-09-07 16:11) introduces `FIT_TYPE_2_A = "2A"` and `FIT_TYPE_2_B = "2B"`;
   `97a1b46f` (2026-09-08 13:42) replaces them with `2Af` / `2Bf` and adds the vocal-shewa
   condition.
3. (d) `24f1e4a3` (2026-09-07 14:30) adds `gh-pages/post-stress-meteg-type-1.html`, 839 lines;
   `3a698b71` (16:36) deletes it whole.
4. (e) `95c457c2` (2026-09-07 12:30) has the §8 paragraph at page lines 425–435; `6a45cd72`
   (16:18, one-line message "Clarify post-stress meteg source tables") deletes it.

**Characterization.** Each of the four items already named the later change — (b) "since the
merge", (c) "`97a1b46f` replaced", (d) "`3a698b71` consolidated the case pages two hours later",
(e) "at HEAD" — so the items did not assert that the messages were wrong when written. The heading,
"Immutable-message slips", did, by filing them beside (a) and (h), which are slips: a message
disagreeing with the diff it describes. C2's sentence "later edits were treated as errors in earlier
commit messages" is true of the heading and not of the items.

**Corrections.** Claude splits 17 into two classes — slips, (a) and (h); messages superseded by
later commits, (b)–(e), each with its superseding commit named, which for (e) is `6a45cd72`, left
unnamed by C2's "later page revisions" — and corrects 17(e)'s "two sentences and two tables": the
φ5 section at `38a606e2` (page lines 396–454) holds three sentences and two tables. Codex's
disposition ("preserve accurate historical messages") stands; nothing proposed rewriting a message.

Re-establish: `git show fe4e602f:gh-pages/post-stress-meteg.html` (lines 100–104);
`git show bdcdc5e2 -- py/accgram/post_stress_meteg.py`; `git show 24f1e4a3 --stat`;
`git show 3a698b71 --stat`; `git show 95c457c2:gh-pages/post-stress-meteg.html` (lines 425–435);
`git show 6a45cd72 -- gh-pages/post-stress-meteg.html`.

## C3 — finding 16, "carries" and "hand transcriptions"

**Claim evaluated.** "Finding 16 extends the 'has' rule from a corpus, manuscript, edition, atom or
chanted word having a mark to any file or directory having text … `b4706759` explicitly declines a
sweep and distinguishes cases where context identifies the author from vague claims about how text
was produced."

**Verdict: agree, on both halves.**

**Evidence.** The skill's rule (`SKILL.md`, "Just say 'has'") is "A corpus, manuscript, edition,
atom, chanted word or compound *has* a mark", with "carries" in its banned list for that subject.
For a file, commit or page having text, "carry" is Ben's usage — `~/.claude/CLAUDE.md` has "A commit
carries `Co-Authored-By: Claude`", "Every figure carries the command that re-establishes it" and
"`doc/PLAN-repo-maintenance-across-GitRepos.md` carries the corresponding judgment step" — and it is
the argument's: the review that flagged five "carries" sites uses the verb ten times the same way
("43 carry no `Co-Authored-By` trailer", "the `title=` and `<title>` sites cannot carry markup"), and
the test comment finding 6.8 cites says "this page carries 34". `b4706759`'s message: "NO SWEEP IS
MADE AND NONE IS PROPOSED HERE … Ben's instruction was to avoid the vague terms 'when context does
not make it clear', not to retire them everywhere." `DATA-LICENSES.md:16` and `:63` at `38a606e2`
name Ben Denckla in the same sentence or cell as "hand transcriptions".

**Corrections.** Claude withdraws eight of finding 16's sites:

1. `DATA-LICENSES.md:38` ("carry").
2. `DATA-LICENSES.md:76` ("carries").
3. `README.md:138` ("carries").
4. `py/py_render/rt_mam_suggestion_card.py:352` ("carries").
5. `py/repo_util/check_repo_standards.py:270` ("carry").
6. `DATA-LICENSES.md:16` ("hand transcriptions", in a sentence opening "Ben Denckla's data").
7. `DATA-LICENSES.md:63` ("Ben Denckla's hand transcriptions").
8. The characterization "against the script-regenerable / Ben-written vocabulary `b4706759`
   adopted": that commit adopted the vocabulary for one site and declined a sweep.

What remains of finding 16: the two low observations C3 says to take on their merits
(`doc/PLAN-merge-post-stress-meteg-into-main.md:174`'s run-on after "Seven commits past
`c73a2ad3`:" and `:74`'s "converted one to the other"), and one residue — `DATA-LICENSES.md:88`,
"J. David Stark's Aleppo Codex index, the tracked source forms, hand corrections, and generated index
artifacts", the one site where the cell does not say whose hand corrections. That is the condition
Ben's instruction names, "when context does not make it clear"; it is raised for Ben, not a rule
hit. Nothing for Codex.

Re-establish: `git show 38a606e2:DATA-LICENSES.md` (lines 16, 38, 63, 76, 88);
`git show -s --format=%B b4706759`; `Select-String -Path C:/Users/BenDe/.claude/CLAUDE.md -Pattern carries`.

## C4 — finding 11.1, Wave 4's missing subtest line

**Claim evaluated.** "It does not establish that the Wave 4 run's missing line 'was a reporting
artifact.' The Wave 4 record expressly reports what that particular run printed and declines to
infer a count."

**Verdict: agree.**

**Evidence.** In `doc/PLAN-remediate-review-findings-2026-09-07.md` at `38a606e2`, Waves 1, 2 and 3
report 976 passed, 5 skipped, 65 subtests; Wave 4 (lines 522–523) reports "981 passed and 5 skipped
in 131.51 seconds. The current suite output had no subtest line, so this record does not infer
one"; Wave 6 (lines 639–640) reports "981 passed, 5 skipped, and 65 subtests passed in 120.45
seconds". The Wave 4 execution result (lines 493–531) states no command at all — no fenced block
and no inline invocation — so the run cannot be re-established as recorded. The argument's
supporting clause holds: none of the six test files `a42216ee` touched contains `subTest` (0 in
each), and the 65 subtests come from seven other files. But it rules out only one cause, Wave 4
having removed subtests. The summary line is pytest 9.1.1's native subtest report — `pytest-subtests`
is not installed in `C:/Users/BenDe/GitRepos/MAM-basics/.venv` — so an invocation through another
interpreter or an older pytest would print the same passed count and no subtest line. That
mechanism is consistent with the record and not confirmable from it: a hypothesis, not a finding.

**Corrections.** Claude replaces 11.1's "so the missing line was a reporting artifact of that one
run" with: Wave 6's run at the same 981 tests printed the line, and the Wave 4 record names no
command, so the cause cannot be established; the record defect is the unrecorded command. The
current-tense claim at `doc/PLAN-evacuate-the-rest-of-three-repos.md:1853` ("no longer prints a
subtest line") is finding 5.1, and both reviews say it wants a dated correction. Nothing for Codex.

Re-establish: `git show 38a606e2:doc/PLAN-remediate-review-findings-2026-09-07.md` (lines 268,
366–367, 455–456, 493–531, 639–640); `git show a42216ee --stat -- py/tests`;
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m pytest --version`.

## C5 — the procedure's "will never load" premise

**Claim evaluated.** "The prerequisite section of `doc/dual-agent-review.md` says Codex 'will never
load' the `hebrew-prose` skill. The same document's provenance section records that the skill
governed the earlier Codex pipeline review … The absolute inability claim is false."

**Verdict: agree, and it is an omission of finding 10.**

**Evidence.** At `38a606e2`, line 235: "Codex reads `AGENTS.md`. It will never load
`~/.claude/CLAUDE.md` or the `hebrew-prose` skill"; lines 273–275 of the same file record that the
2026-09-01 Codex review "records that the `worktree-forest` and `hebrew-prose` skills governed it".
The argument's finding 5.6 held the third piece without connecting it:
`C:/Users/BenDe/.agents/skills/hebrew-prose/` exists so that Codex can load the skill, and on
2026-09-09 its `references/terminology.md` is byte-identical to the `~/.claude` copy (SHA-256
`6deac742e2d7027eb7330b8e744bf993e50e97a0b49c46ff92595e1917c51c90` for both). `9cf48863` re-measured
the paragraph on 2026-09-08 without touching the premise, and at `49609331` the sentence is still
there, at line 258: an unfixed record error, as C5 says.

**Proposed wording for that sentence, for Ben's approval** (a `doc/` change, not a MAS change):
"Codex reads `AGENTS.md`, not `~/.claude/CLAUDE.md`, and loads the `hebrew-prose` skill only from
its copy under `~/.agents/skills/` — which is why that copy exists, and why finding 5.6 of the
2026-09-08 review compares it byte for byte."

Re-establish: `git show 38a606e2:doc/dual-agent-review.md` (lines 235, 273–275);
`Get-FileHash -Algorithm SHA256 C:/Users/BenDe/.agents/skills/hebrew-prose/references/terminology.md`.

## Reconciliation on 14.4 — where the context permission lives

**Claim evaluated.** "The skill's opening does not contain the quoted permission 'wherever the
context already settles which sense is meant'; that wording is in the repository instructions and
is attributed back to the skill. … The inaccurate attribution is a refinement of finding 14.4 and
issue #265."

**Verdict: disagree.**

**Evidence.** The wording is in the skill:
`C:/Users/BenDe/.claude/skills/hebrew-prose/references/terminology.md:26`, in bold — "And plain
'word' survives wherever the context already settles which sense is meant." — with Ben's
2026-07-29 quote as its authority. `SKILL.md` lists that file as part of the skill ("Reference files
… every vocabulary rule with its reasoning, exemptions"). The words `CLAUDE.md:53` quotes are
`terminology.md:26`'s, so "the skill itself allows for one" is accurate, and `CLAUDE.md:157` has the
same sentence in near-identical words. Codex's copy has the same line 26 (the hash above). What is
true in Codex's sentence is narrower: `SKILL.md:19–20` says plain "word" survives **only** for an
ordinary English word and inside quoted or translated source material. So the skill disagrees with
itself — front matter two exemptions, reference file three — and that, not `CLAUDE.md`'s
attribution, is the gap. It bears on #265: the page-specific exemption for the nine
post-stress-meteg pages is in the skill nowhere, as 14.4 says; the general permission that licenses
it is in the reference file and absent from `SKILL.md`.

**Corrections.** Codex withdraws "that wording is in the repository instructions and is attributed
back to the skill" and "the inaccurate attribution". Claude makes 14.4 explicit about the two things
it ran together: the page exemption (in the skill nowhere) and the `terminology.md:26` permission
(present in the reference file, missing from `SKILL.md`'s "only"). A `SKILL.md` change is a
github-misc change and Ben's; the concrete proposal is under "Choices" below.

Re-establish: `Select-String -Path C:/Users/BenDe/.claude/skills/hebrew-prose/references/terminology.md -Pattern "context already settles"`;
`Select-String -Path C:/Users/BenDe/.claude/skills/hebrew-prose/SKILL.md -Pattern "survives only"`;
`git show 38a606e2:CLAUDE.md` (lines 53, 157).

## Reconciliation on 14.1 — the paragraph count

**Claim evaluated.** "The definition is the second expository paragraph; counting the control makes
it the third HTML paragraph. The before-any-earlier-use claim is false."

**Verdict: agree.**

**Evidence.** At `38a606e2`, the `<p>` elements of `gh-pages/post-stress-meteg.html` before the
definition are line 12, `<p class="post-stress-meteg-spacing-control">` holding the expanded-Hebrew
checkbox, and line 60, "A meteg almost always comes before the stressed syllable of its word"; the
definition is line 72 — the third `<p>` element and the second paragraph a reader sees. "Of its
word" at line 61 precedes the definition, so the six sites' "before any other sentence uses either"
is false, as both reviews say.

**Corrections.** Claude corrects 14.1: the record is off by one sentence, not by one paragraph.
Nothing for Codex.

Re-establish: `git show 38a606e2:gh-pages/post-stress-meteg.html` (lines 12, 60–61, 72–75).

## Reconciliation on 13.5 — which function raises

**Claim evaluated.** "`_problems` returns the problems; the build raises."

**Verdict: agree.** `_problems` (`py/accgram/post_stress_meteg.py:2596` at `38a606e2`, `:2632` at
`49609331`) returns `list[str]`; `build_survey` raises when the list is non-empty (`:2905–2906` at
`38a606e2`, `:2941–2942` at `49609331`). 13.5 named the wrong function; the behavior it described —
no survey with a syllable-count mismatch completes, and the record lives only in the exception's
message — is right, and `build_survey`'s docstring says so where the module docstring does not.

**Corrections.** Claude corrects the function name in 13.5. Nothing for Codex.

## Reconciliation on 6.8 — the 34-anchor comment

**Claim evaluated.** "Qualify the claim that the historical 34 count itself is false."

**Verdict: no such claim was made.** Finding 6 opens "Written earlier that afternoon and true
then", and 6.8 dates the change to `9cf48863`. What Claude adds from Codex: the comment self-dates
("this page carries 34 after the 2026-09-07 index additions",
`py/tests/test_site_index_links.py:84`), which the other seven sites of finding 6 do not, and its
floor of 25 functions; it is the least stale of the eight.

## Codex's MAS-decisions section — the plan at `47edbee6`

**Claim evaluated.** "The plan already contains broad editorial instructions that made those changes
executable … The checklist does not identify which concrete MAS rewrites Ben has approved. A general
instruction to execute that checklist is not evidence of separate approval of every editorial choice
embedded in it. This is a process omission beyond merely noticing that disposition rows became
stale."

**Verdict: agree, and the omission is the argument's.**

**Evidence at `47edbee6`**, read by an agent: lines 282–284, "Apply every prose correction in current
source, including `own`, loose `word`, possession verbs, undefined reader-facing abbreviations,
section-range punctuation, and tsere spelling. Rebuild shared ITM/CoS links by reuse rather than
preserving duplicate local helpers."; lines 266–267, "Decide the type-3 rule from the sources and
current corpus, then make prose, classifier, and `pin_claims` assert the same rule."; lines 270–271,
"Label UXLC and WLC as the sources actually read. Do not claim that BHS has a form on the authority
of BHS-derived transcriptions." Line 3 was `State: live`; line 7 says "Ben requested this planning
phase"; "approv" occurs nowhere in the file; its five decision gates (lines 141–168) name no page
wording. Those three instructions are the edits `e91d7358` made and `1095f029` / `a9edd4f9`
reverted on Ben's report and decision of 2026-09-08 ("revert every unrequested rewrite `e91d7358`
… made") — unrequested by Ben, requested by a Claude-written checklist. The argument's "What this
review did not check" item 6 raised the approval question for one revert and stopped short of the
checklist.

**Corrections.** Claude accepts the finding as Codex states it. Ben's decisions stand as recorded
— `1095f029`, `a9edd4f9`, `3b0225e0`, `becc6f00` — and nothing here proposes reinstating any reverted
wording. On finding 3, Codex's caution ("should not label every reversed editorial change unfinished
work awaiting reinstatement") guards against a misreading of a finding that asked only for "a dated
correction either way"; Claude endorses it. Rows 13 and 21 of `doc/review-findings-2026-09-07.md`
and the plan's Wave 2 result still say "fixed" for wording Ben reverted; that dated correction is a
record edit, not a page edit, and is not made here.

Re-establish: `git show 47edbee6:doc/PLAN-remediate-review-findings-2026-09-07.md` (lines 3, 7,
141–168, 266–284); `git show -s --format=%B 1095f029`; `git show -s --format=%B a9edd4f9`.

## Disagreements still unresolved

1. 14.4's attribution — Codex says the context permission is in the repository instructions and
   not in the skill; it is in the skill's `references/terminology.md:26`, identical in Codex's
   copy. Settled by a search, not yet conceded by Codex.
2. 13.2's characterization — "without checking it" and "manufacture agreement" against 13.2's
   "aborts the run". Substance agreed; the paraphrases stand in Codex's record.
3. 17(b)–(e) — heading versus items. Substance agreed; C2's "later edits were treated as errors in
   earlier commit messages" describes the heading, not the items.

## Choices requiring Ben's judgment

1. `doc/dual-agent-review.md`'s "will never load" sentence (C5; line 258 at `49609331`): approve
   the wording proposed above or another, and whether finding 10 gets a dated addendum naming it.
2. `SKILL.md:19–20`'s "only": bring it into line with `references/terminology.md:26` — proposed:
   "Plain 'word' survives for an ordinary English word, inside quoted or translated source
   material, and wherever the context already settles which sense is meant
   (`references/terminology.md`)." A github-misc change; it also decides how #265's registry, if
   adopted, relates to the general permission.
3. The argument's record: whether the corrections accepted here (13.2's filing, 13.5, 13.7, 14.1,
   16, 17's heading and 17(e)'s count, 11.1's clause, finding 10's omission of C5, the `47edbee6`
   process finding) go into a dated addendum under `doc/review-findings-2026-09-08.md`, or stay in
   this file.
4. The Wave 4 record (`doc/PLAN-remediate-review-findings-2026-09-07.md:523`): a dated note that the
   run's command is unrecorded and that Wave 6 at 981 tests printed 65 subtests; and finding 5.1's
   `:1853` correction, which both reviews want.
5. 13.2's design note: leave the assertion-plus-literal as it is (Codex's recommendation and
   Claude's), or report MAS multiplicity as a JSON count the way MBS multiplicity is — a
   Methods-page change whose wording would come to Ben first.
6. `DATA-LICENSES.md:88`: whether "hand corrections" should say whose.
7. Codex's process rule for future remediation — separate reproducible data or code defects from
   proposed changes to the MAS pages' terminology, organization, interpretation or attribution,
   and present concrete wording for approval — whether to adopt it, and where to record it.
8. `py/tests/test_site_index_links.py:84`: "34" to 35, one word.

## Commit status

This file is committed on `codex-review-2026-09-08` only, per the worktree rule in
`~/.claude/CLAUDE.md`; it is not pushed and not merged. When it was written, `main`
(`2de7a969`) already contained the branch's previous head `49609331` (`git merge-base main
codex-review-2026-09-08`), so this commit is the branch's only commit not on `main`. Integration is
Ben's, on the schedule the worktree rule gives.
