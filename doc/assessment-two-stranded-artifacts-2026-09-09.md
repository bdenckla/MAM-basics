# Assessment — two stranded artifacts of 2026-09-09

State: assessment only, written 2026-09-09. Nothing was merged, deleted or force-pushed, and every
disposition below is Ben's to choose. The one change this session made is the corrected
`repo_visibility.github-misc.comment` recorded in §7.

The two artifacts:

1. **The stranded branch** `origin/claude/charming-mayer-xknwcw` in `bdenckla/MAM-basics`, tip
   `036deb92fa42f7b6b707dbbcd04f9560fb709b84`, two commits ahead of `main` and on no machine.
2. **The stranded review plan**
   `C:/Users/BenDe/GitRepos/github-misc/doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md`,
   the only file under that repository's `doc/`.

Measured against `MAM-basics` at `a50da28b` (`main` and `origin/main` both, primary clone clean)
and `github-misc` at `cfd5510` (clean). A second checkout was live during this work,
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08` on branch `codex-review-2026-09-08`
at `2b365153`; it holds a different branch, so it shares no index with the primary clone.
Re-measure every figure below rather than trusting it, and treat a mismatch as a finding.

## 1. What the two stranded commits hold: a 15-file repair and a lint that would have caught it

**Disposition: read in full, and the repair is verified byte-exact.** No recommendation is made in
this section; §2 and §3 carry them.

### `73ab8383` — the repair

Fifteen tracked prose files, 72 insertions and 72 deletions, across `doc/` (13 files),
`holman/doc/uxlc-email-count-disagreements.md` and `leningrad/page-snips/README.md`. Every changed
line puts one or more Hebrew clusters back into MAM-normal mark order. Nothing else changes: no
letter, no mark, no wording.

That is verified rather than assumed. For each of the fifteen files, all three of these hold:

1. `give_std_mark_order(before) == after` — the repair is exactly what `py/mb_cmn/uni_denorm.py`
   prescribes, not an approximation of it.
2. `has_std_mark_order(after)` — the result is in MAM-normal order.
3. `Counter(before) == Counter(after)` — the multiset of codepoints is unchanged, so no character
   was added, removed or substituted.

Re-establish by reading each blob pair with
`git -C C:/Users/BenDe/GitRepos/MAM-basics show 73ab8383^:<path>` and `show 73ab8383:<path>` and
applying the three predicates above.

### `036deb92` — the lint, and two corrections to `CLAUDE.md`

Four files. The substance is `py/tests/test_prose_mark_order.py`, new, 123 lines.

**What the lint checks.** It lists every tracked `.md` plus the `.html` under `doc/` with
`git ls-files -- "*.md" "doc/*.html"`, reads each file, and fails if any line is not
`has_std_mark_order`. The failure message names every offending `<path>:<line>` and says explicitly
not to fix the result by calling `unicodedata.normalize`, which is what causes the defect.

**What the lint exempts.** Nothing by name: its `_EXCLUDED` frozenset is empty. Everything it
leaves out, it leaves out **by file type**, and the docstring argues the case. The exempt trees are
excluded structurally rather than listed — `in/mam-ws/`, `out/mam-ws-bot/proto/` and
`out/mam-ws-parsed-fmt-2/` sit upstream of the pipeline's denormalizing step and carry their
source's order by design, and none of them is a `.md`.

**The declared `in/mam-ws-intro/` exemption is honoured.** That tree is byte-verbatim mirrored
wikitext and `CLAUDE.md` exempts it by name. It holds 14 files, of extensions `.json` and
`.mediawiki` only, and no `.md` at all, so the lint's file-type scope excludes it without needing
an entry. Re-establish with `git ls-files -- "in/mam-ws-intro/*"`.

**The two `CLAUDE.md` corrections.** The first section said two things the commit shows to be
false. "There is no lint over hand-authored source here" was already contradicted by
`py/tests/test_mam_simple_mark_order.py` and `py/check_mark_order.py`. "A cluster in the other
order is always something hand-authored" is the more dangerous, because it invites a mass rewrite
of the download; the replacement names the upstream kind and says never to repair it. The commit
also marks as past `test_mam_simple_mark_order.py`'s quotation of the sentence that changed.

### Two claims in the new docstring that do not hold as written

Both are in the passage arguing against widening the lint's file types. Each conclusion survives;
each stated reason is incomplete.

1. **The `.html` count is right and its explanation is not.** The docstring says widening to all
   `.html` "would take in 67 offenders, every one either generated (`gh-pages/`) or a
   byte-verbatim capture (`misc/*/img-sources/`)". Measured at the branch tip, there are indeed
   exactly 67 — but they divide 28 in `gh-pages/`, 3 in `misc/*/img-sources/`, and **36 in
   `uxlc/in/UXLC-notes/`**, which the sentence names nowhere. Those 36 are the majority, and they
   are an input capture rather than either category offered.
2. **The `.txt` inventory names two of four categories.** The docstring says widening to `.txt`
   would take in `aleppo/aleppo-wiki/Wikisource-manual-*.txt` and `misc/zarqa-table-diff/*.txt`.
   Measured on `main`, 15 tracked `.txt` are not in MAM-normal order: those 4, plus **4 in
   `in/accgram/edition_transcriptions/`** (`koren_dt_elyon`, `koren_ex_elyon`, `simtan_dt_taxton`,
   `simtiq_ex_elyon`), 1 in `uxlc/in/UXLC-misc/` and 6 in `uxlc/out/UXLC-misc/`.

### The four edition transcriptions are ordinary hand-authored prose, and the repair is safe

**Disposition: recommended for repair, on the same footing as the branch's other 132 clusters.**
This assessment first filed them as a judgment call for Ben — whether a transcription of a printed
page counts as hand-authored prose or as a capture — and that framing was wrong, because the
offending Hebrew is not in the transcription at all. Ben's questions of 2026-09-09 prompted the
measurements below.

**They are in Unicode-normal order specifically**, not merely outside MAM-normal order, which the
predicate alone does not establish. All four satisfy `text == NFC(text)` and `text == NFD(text)`,
and all seven offending clusters carry the canonical signature — a vowel before the dagesh, which is
exactly what `CLAUDE.md`'s first section says Unicode-normal order produces. Six are a tav with
qamats or segol before a dagesh; the seventh is a shin with sheva, dagesh and shin dot, where
MAM-normal order wants shin dot, dagesh, sheva.

**Not one distinguishing cluster is MAM-normal**, so these are not MAM-normal files carrying a few
contaminating clusters. Of the 765 clusters across the four files, 758 are indifferent — the two
orders give identical bytes for them — and all 7 that can tell the orders apart are Unicode-normal.
An accent transcription rarely stacks a vowel with a dagesh, which is why so few clusters can
testify at all.

**The capture question never arises, because the transcribed body has no pointing.** The committed
JSON beside each `.txt` stores accent names in Hebrew abbreviations, `פש מונ זקף` and the like, and
holds no vowel point anywhere. All 12 JSON files in the directory are in MAM-normal order. So the
body carries nothing that could distinguish the two orders, and what a transcription of a printed
page "is" turns out not to bear on the question.

**Every offending cluster sits on a `#` comment line in the hand-written header** — Ben's notes on
what each printed edition does at a given place, quoting pointed Hebrew. That is hand-authored prose
pasted through something that normalizes, which is the way in `CLAUDE.md` names, and it is the same
defect as the other 132 rather than a different kind.

**The repair is safe against the idempotence check.** `py/accgram/transcription_build.py` states
that "THE HEADER STAYS IN THE .txt AND IS NEVER REWRITTEN. Only the body beneath it is derived", and
`py/tests/test_edition_transcriptions.py` runs `build --check` to assert that re-deriving the body
reproduces each file byte for byte. Repairing a header comment therefore survives the next
`--derive-only` and cannot fail `--check`. A repair inside the derived body would not have been
safe, and none is needed.

**These four are the first real instance of a weakness the new lint's docstring admits**, that "a
`.txt` is covered by nothing". A blanket widening to `.txt` remains wrong, since 11 of the 15
offending `.txt` are genuine captures; a scope naming `in/accgram/edition_transcriptions/*.txt`
would cover these four without taking in any capture.

### One silent-skip channel in the lint

`if not full.is_file(): continue` passes over a path that `git ls-files` reports but that is absent
from the working tree, and says nothing. It cannot fire in an ordinary checkout, and the `_FLOOR`
assertion described in §2 catches the case where the whole listing collapses. It is still a channel
through which the lint can report green having checked less than it listed, which is the shape
`CLAUDE.md` §"Writing tests" warns about. Changing `continue` to an appended offender would close
it.

## 2. Whether the commits were ever desired: yes, and the lint is the shape the rules permit

**Disposition: both commits answer a gap `CLAUDE.md` names in its own first section, and the lint
satisfies every constraint the test rules impose.** Recommended for `main`, subject to §3's
freshening.

### The gap is real, and the repository named it

`CLAUDE.md`'s first section said "There is no lint over hand-authored source here ... so the check
is yours to run". A lint over hand-authored prose is exactly the gap that sentence describes, and
the sentence had already been overtaken in part, since two mark-order lints existed. So the work
is not speculative: it closes a hole the instruction file advertises.

### The shape is permitted

`CLAUDE.md` §"Writing tests — differential and lint-shaped only" admits two shapes. This is the
second, "a mechanical lint over the tree — a decidable property of the *source text* rather than of
behavior", and it sits beside the three the section already names.

### A missing input fails rather than skips

The rule that a missing input must FAIL is satisfied. `_FLOOR = 100` guards the file listing:

    assert len(in_scope) > _FLOOR, "... the pathspec or the exclusion set may be too broad."

A pathspec that matched nothing, or a run from outside the repository, fails the assertion rather
than passing vacuously over an empty list. There is no `skip` anywhere in the file, and no
`@parametrize` that could empty out. The one residual silent channel is the `is_file()` guard in
§1.

### The declared exemption is honoured

Covered in §1: `in/mam-ws-intro/` cannot enter scope, because it holds no `.md`.

### What this costs

One second, over 189 files as of `a50da28b`. There is no cost argument for narrowing it.

## 3. Whether the commits survive the config move: yes, and they need no rebase at all

**Disposition: the branch merges into `main` cleanly and the defect it repairs is still live.
Neither a rework nor obsolescence — and not even the light rebase the question anticipated.** The
freshening it does need is three stale figures in prose, listed below, not a code change.

### The defect is still live on `main`

All **132** offending clusters in all **16** files are present at `a50da28b`, unrepaired, with
per-file counts identical to those at the branch base `20ebbac1`. Nothing that landed on `main`
between the two has fixed any of them. So the repair commit has lost none of its point.

### The merge is clean, and the merged tree is clean

`git -C C:/Users/BenDe/GitRepos/MAM-basics merge-tree --write-tree --name-only main
origin/claude/charming-mayer-xknwcw` returns tree `af5e8cd7` and no conflict, although `main` has
advanced 15 commits since the branch forked and has itself modified three of the sixteen offending
files plus `CLAUDE.md`.

Scanning that hypothetical merged tree with the lint's own logic gives **0 offending files and 0
offending clusters across all 189 files in scope**.

### The `dot-claude/` and `dot-Codex/` trees should be covered, and already are

The question was whether the new lint should cover the trees that arrived with `74d883d2`,
`6d19c34a` and `c6575fc8`, or explicitly exempt them.

**Recommendation: cover them, which needs no code change, and add no exemption.** They are
hand-authored prose containing Hebrew — the `hebrew-prose` skill's reference files carry worked
Hebrew examples — and hand-authored prose containing Hebrew is precisely what the lint is for. They
are not captures and not pipeline intermediates, so no ground for exemption applies.

The evidence that this costs nothing: the config move added 16 files to the lint's scope, raising
it from 173 to 189, of which 12 are under `dot-claude/` and `dot-Codex/`. **Not one of the 16 is an
offender.** The lint would pass over them today, unmodified, because `git ls-files -- "*.md"`
already reaches them.

This is also the one forward-looking connection between the two stranded artifacts, and §4 keeps it
distinct from the retrospective question. If the review plan of §5 is executed, its edits land in
`dot-claude/user-wide-CLAUDE.md` and the skill's five files — all now inside the lint's scope, so
the lint would guard that work.

### The three figures the branch should have freshened before merging

None is a conflict; each is prose overtaken by the config move.

1. **`test_prose_mark_order.py`'s file counts.** The docstring says "171 of them on 2026-09-09" and
   the `_FLOOR` comment says "Well under the 173 files in scope on 2026-09-09". On `a50da28b` the
   figures are 187 `.md` and 189 in scope. Re-establish with
   `git ls-files -- "*.md" "doc/*.html"`.
2. **The docstring's `.html` and `.txt` inventories**, per §1: the `.html` explanation omits
   `uxlc/in/UXLC-notes/`, and the `.txt` inventory omits `in/accgram/edition_transcriptions/`,
   `uxlc/in/UXLC-misc/` and `uxlc/out/UXLC-misc/`.
3. **One imprecision in the `CLAUDE.md` replacement text.** It says `py/check_mark_order.py`
   "covers the `.py` and Ben-authored `.json` of the four repos `py/repo_scopes.py` names".
   `repo_scopes.code_paths()` does draw on four (book-of-job, codex-index-aleppo, Cambridge 1753
   and codex-index-leningrad), but that module's own docstring says the Leningrad tree "contributes
   no mark-order scope" for JSON, so the `.json` half covers three, not four.

Everything else in the `CLAUDE.md` replacement holds. All seven helper files it cites exist on
`main`, and the merged first section reads coherently against what `74d883d2` added.

### Verification the executing session still owes

The scan above reproduces the lint's logic; it is not the lint itself running. Before merging, check
out the merged tree and run `.venv/Scripts/python.exe py/main_test.py` from the repository root. The
baseline on `a50da28b` is **983 passed, 5 skipped, 65 subtests passed** in 83.7 seconds; the merged
tree should give 984 passed, the new lint being one test.

## 4. Whether the branch connects to the instruction-file review: ruled out

**Disposition: no retrospective connection exists.** The two are independent work by two different
sessions on the same day. One prospective interaction exists and is stated in §3; it is not a link
between the commits and the review.

The plausible link the question raises is that `036deb92` edits a `CLAUDE.md` and the review is
about instruction files. That link does not hold, on five counts.

1. **They are different files.** `036deb92` edits `C:/Users/BenDe/GitRepos/MAM-basics/CLAUDE.md`,
   the project instruction file. The review covers twelve files that were then
   `github-misc/dot-claude/` and `github-misc/dot-Codex/`, among them the user-level
   `dot-claude/CLAUDE.md`. MAM-basics' project `CLAUDE.md` is not in the plan's §0 list of what was
   reviewed.
2. **The plan cites MAM-basics' `CLAUDE.md` only as an authority, never as a file to edit.** Its
   five mentions, at lines 67, 97, 252, 320 and 335, each invoke one of its sections as a governing
   rule.
3. **The plan contains no mark-order finding, and no mark-order vocabulary.** Searching it for
   `mark order`, `mark-order`, `uni_denorm`, `normaliz`, `NFC`, `NFD`, `std_mark`, `SBL2` and
   `denorm` returns a single hit, `#49 NFC` at line 254, which is a wlc-utils issue title inside
   the M12 issue-prefix sweep.
4. **They are different sessions.** Both stranded commits carry the trailer
   `Claude-Session: https://claude.ai/code/session_0132vm6tQ7Vz4mceDQgfka4Y`, a cloud session. The
   review ran in a local worktree, `github-misc/.claude/worktrees/elastic-montalcini-f28420`.
5. **The co-present session the plan noticed was a third one.** The plan's §1 item 5 records that
   the MAM-basics primary clone held an untracked `doc/user-level-config-in-cloud-sessions.md`. That
   file was committed by `6d19c34a` at 11:03, part of the config move — not the mark-order work,
   which was a cloud session with no local working tree at all.

The chronology, in local time on 2026-09-09, shows three streams running in parallel rather than one
handing off to another:

| Time | Repository | Event |
| --- | --- | --- |
| 09:40 | MAM-basics | `20ebbac1`, the base the cloud session forked from |
| 09:58 | MAM-basics | `73ab8383`, the repair (cloud session) |
| 10:34 | github-misc | `810ffd0`, the review's measurement baseline |
| 10:37 | MAM-basics | `036deb92`, the lint (cloud session) |
| 11:03 | MAM-basics | `6d19c34a`, cloud sessions get the user-level config |
| 11:31 | github-misc | `5f6f989`, the review plan committed |
| 12:02 | MAM-basics | `74d883d2`, MAM-basics becomes the canonical home |
| 12:03 | github-misc | `cfd5510`, the trees leave, breadcrumbs stay |

The two stranded commits carry UTC timestamps, containers running UTC; the table converts them.

**The cloud session is also why the branch went unnoticed.** A cloud session pushes its `claude/*`
branch to the remote and leaves no local branch and no worktree behind, so there was nothing on disk
to notice. §6 gives the full account, which has a second half.

## 5. Whether the review plan can move to MAM-basics: it can, and it needs no redaction

**Disposition: the privacy screen is clean — the file can move into the public repository with no
redaction.** The move is not free: it needs a repointing pass over wording the plan already
contains, costed below. Ben's premise for the move holds as a claim about ongoing work, though the
tree does still hold dormant Hebrew Bible material, and both halves are recorded so a later session
does not mistake one for the other.

### The privacy screen found nothing that bars publication

Screened for the two concerns Ben named and for the wider class.

1. **Scraping mgketer.org: absent.** No occurrence of `scrap`, `crawl`, `spider` or `harvest`
   appears in any relevant sense; the only hit is the phrase "blame crawl" at line 139, describing a
   `git blame` pass.
2. **Comparing mgketer.org against MAM: absent.** All 14 mgketer mentions are instruction-file
   bookkeeping — whether a passage should cite `mgketer/CLAUDE.md` or `mgketer/AGENTS.md`, that the
   file moved into `MAM-private/mgketer/` on 2026-08-09, and that the repository was archived on
   2026-08-27. None concerns mgketer's content, and none concerns any comparison.
3. **Email addresses: none.** No string matching an address appears.
4. **Credentials: none.** No hit for `ghp_`, `github_pat`, a private-key header, `password`,
   `secret`, `api key` or `bearer`. The two `token` hits are "maqaf token" (a wlc-utils issue title)
   and `<total_tokens>`.
5. **Personal correspondence: none.** The only people named are `bdenckla`, Ben's own public GitHub
   handle, and Breuer, a scholar cited throughout MAM-basics' published pages. Neither Holman nor
   Kadish nor `skadish1` appears.
6. **Private-repo content quoted at length: none.** Twelve lines mention MAM-private, and each is a
   path citation or a figure attribution rather than quoted material. The single verbatim quotation
   is one line of code in D5, a hardcoded path constant from
   `MAM-private/masorah-books/py/itm/liberality_metric.py`.

**The figures the plan draws from MAM-private are already public**, published by the very move that
stranded the plan. `MAM-basics/dot-claude/skills/hebrew-prose/` now tracks both "522 sections in 57
files" and "719 page images"; `phonetic-hbo`, the path in D5's code quote, appears in 16 MAM-basics
`doc/` files. So the plan discloses nothing the public repository does not already carry.

Against `CLAUDE.md` §"Holman's mailboxes, public derivatives, and authored CSS" as the model: that
section's boundary exists because the raw material carries mail headers and message bodies. This
plan has no counterpart to either, so the question of a redacted derivative does not arise. Nothing
would have to be omitted, and the remainder question is moot.

### Ben's premise holds on the reading that matters, and Hebrew Bible bytes remain anyway

Ben's reasoning was that github-misc "no longer holds anything of relevance to MAM-basics,
MAM-private, or related Hebrew Bible work". Read as a claim about **ongoing** work, which is what
"relevance to MAM-basics, MAM-private" makes it, the premise holds. Read as a claim that no Hebrew
Bible material is tracked there, it does not. Both halves are worth recording, because a later
session running `git -C C:/Users/BenDe/GitRepos/github-misc ls-files` will find the second half and
could mistake it for the first.

**What is tracked there**, at `cfd5510`:

1. **`Dead Sea Scrolls/`**, Ben's writing rather than a stray asset: five essays titled "Qumran,
   Isaiah, and the NJPS", "More on Qumran, Isaiah, and the NJPS", "Qumran, Isaiah, and Stern", and
   "The daleth and the resh" in two parts, plus a 2,021-byte comment on Isaiah 2:9–10 and the minus
   at that point in 1QIsa-a.
2. **Two images**, `Ps 19v15 MAM doc-note.png` and `Ps 137v9.png`, the first naming MAM outright.

**Why none of it is ongoing work.** Ben's assessment, 2026-09-09: this material is ancient and
predates the phase of his work that the `trope` repository opened and MAM-basics later replaced; he
does not expect MAM-basics or MAM-private ever to reference the image, and does not expect further
images to be added there for either repository to reference. Three measurements bear him out.

1. **The dates.** Every commit touching `Dead Sea Scrolls/` falls between 2012-08-21 ("initial
   commit of Isaiah/NJPS/Qumran work") and 2012-11-07, fourteen years ago. The two images were
   uploaded on 2022-09-20 and 2022-09-21, both as bare "Add files via upload".
2. **Nothing references them.** No file in MAM-basics or MAM-private cites the `Dead Sea Scrolls/`
   tree or either image. The topic words do appear in both — Yeivin and Breuer discuss Qumran, and
   MAM-basics' `py/author_misc/urwotm_1_tale_of_the_qadma.py` and `urwotm_3_extra_verses.py` do too
   — but each of those reaches the subject on its own, with no dependency on github-misc.
3. **Every citation of github-misc in both repositories is about something else.** The 32 files in
   MAM-basics and 5 in MAM-private that name github-misc concern the tracked agent configuration,
   repo maintenance and the review series — which is precisely the relationship the 2026-09-09 move
   ended.

So the premise is sound as a reason not to keep the plan in github-misc. What it does not support is
the stronger sentence "github-misc holds nothing of Hebrew Bible interest", which the tree
contradicts; the material is simply dormant rather than absent.

### The reason that does not rest on the premise at all

**The plan is stranded because its subject left, not because its host became irrelevant.** All
twelve files the plan reviews are now tracked in MAM-basics, at `dot-claude/` and `dot-Codex/`; what
remains in github-misc under those two names is a pair of breadcrumb READMEs. A plan whose every
work item edits a file in another repository belongs with the files, and that argument is
independent of whatever else github-misc holds.

### What the move costs: a repointing pass, and one new ambiguity

The file cannot move verbatim, because the move that stranded it also renamed two of its subjects.
**Every item below is an edit to wording the plan already contains — text to change, never text to
add.** Six kinds of site, measured on the file at `cfd5510`:

1. **`dot-claude/CLAUDE.md` → `dot-claude/user-wide-CLAUDE.md`**, 3 occurrences on 3 lines.
2. **`dot-Codex/AGENTS.md` → `dot-Codex/user-wide-AGENTS.md`**, 3 occurrences on 3 lines.
3. **Bare `AGENTS.md`**, 28 occurrences on 26 lines, each now naming a file that exists under a
   different name.
4. **`C:/Users/BenDe/GitRepos/github-misc` as the checkout to work in**, 5 occurrences, including
   §1 item 1's instruction to prefer that primary clone and §5 item 8's integration step.
5. **`github-misc` in any role**, 14 occurrences on 13 lines.
6. **Bare `CLAUDE.md`, on 20 lines.** Each of those 20 lines already stands in the plan, and each
   means the user-level file. Inside MAM-basics a bare `CLAUDE.md` names this repository's project
   instruction file instead, so each of the 20 needs `user-wide-CLAUDE.md` written in place of what
   it says now.

Item 6 is the same defect class as the plan's own M12, which exists to prefix 18 bare issue numbers
that collide across trackers. Moving the plan without changing those 20 lines would carry 20 sites
of the identical ambiguity into the file that documents the fix for it.

### Recommendation on destination

**Move it to `MAM-basics/doc/`, with the repointing pass applied in the same commit.** Public
MAM-basics rather than MAM-private, because the screen is clean and because the files the plan acts
on are public MAM-basics files now — a plan tracked privately about editing public files would put
the plan and its subject on opposite sides of the boundary for no privacy gain.

MAM-private would be the right destination only if Ben wants the plan's §7 recommendation — that
this review join the periodic series — resolved onto the private side first, since §7 observes that
github-misc's privacy is what put the review in the private series. That observation is now
obsolete for the same reason the plan is stranded: the files moved to a public repository, so a
review of them falls to the public series. **This is a decision for Ben, not a fact this assessment
can settle**, and it is the one place where the destination question is genuinely open.

Two smaller points for whoever executes the move:

1. **The plan's §0 baselines are stale but still serviceable.** It was measured against github-misc
   at `810ffd0` and MAM-basics at `d8a0fdae`, both superseded within the hour. Its §0 already
   instructs re-measurement, so this is not a defect in the plan.
2. **The plan's own Hebrew passes the new lint.** Its only Hebrew is the maqaf, spelled `מקף`,
   twice, unpointed; the file satisfies `has_std_mark_order` as it stands. So the §3 lint would
   accept it on arrival, with no repair needed.

## 6. Why the branch was stranded: an ambiguous readiness report, and a sweep that cannot see it

**Disposition: both causes are identified; neither is fixed here.** The first needs no fix, per
Ben's decision recorded below. The second is a decision about scope rather than a correction, so it
is Ben's.

The two causes are independent, and either alone would have been survivable.

### Cause 1 — "on the remote" was read as "on `main`", and the readiness sentence did not say which

Ben's diagnosis, 2026-09-09, from the archived cloud session's transcript. He asked the session to
get ready to be archived and it answered **"Ready to archive. Everything worth keeping is on the
remote."** He read "the remote" as `main` on the remote. The session meant its own branch, and said
so in a later heading, "What survives on `claude/charming-mayer-xknwcw`", which he also missed.

The statement was true and still failed, because "the remote" does not distinguish `origin/main`
from `origin/claude/charming-mayer-xknwcw`. `~/.claude/CLAUDE.md` §"Handing off to a task chip"
already requires the distinction in the readiness sentence itself: **"Give the evidence with the
claim ... and, in a worktree, the branch and commit that the archive request will merge into
`main`."** The branch name did appear in that message, but in a heading rather than in the sentence
that claimed readiness, and the same section requires the readiness statement to be "the final
sentence of the final message". So the required form was available and was not used.

**There is a structural reason a cloud session stops at its branch, and it is not carelessness.**
The Git section's integration is four steps: merge `main` into the branch in the worktree, run the
suite there, then `git -C <primary clone> merge --ff-only <branch>` and push `main`. Steps 3 and 4
name the primary clone, which a cloud container does not have. So a cloud session **cannot** perform
the integration that the archive request is supposed to trigger, and the protocol as written has no
cloud form.

**Ben's decision, 2026-09-09: do not try to make future cloud sessions push to `main`.** Be aware
instead that a cloud session will push only to the non-`main` branch it worked on. That is the
right call given the paragraph above — the behaviour follows from the container's lack of a primary
clone, so it is a fact to know rather than a habit to correct.

**What makes awareness sufficient rather than a reliance on memory is the second cause.** Ben's
decision leaves the branch correctly parked on the remote and leaves him to notice it; the sweep
below is what could do the noticing.

### Cause 2 — the `--clean-worktrees` sweep sees local branches only

`py/repo_util/git_worktree_cleanup.py`'s `_agent_branches` reads local heads only:

    _git(repo_dir, "for-each-ref", "--format=%(refname:short)",
         f"refs/heads/{_AGENT_BRANCH_PREFIX}")

`refs/heads/claude/` cannot see a branch that exists only on the remote. The module mentions
`origin` in one other place, `_default_branch`, and never to enumerate branches. So after cause 1
had let the branch past the archive, nothing else could catch it: a cloud session leaves nothing
local, and the sweep looks only at what is local.

**How widespread it is: one instance.** Across every clone under `C:/Users/BenDe/GitRepos`,
`git ls-remote --heads origin "claude/*"` finds exactly one remote-only agent branch, the stranded
one in MAM-basics. Every other clone, the six other workspace folders included, has none.

So this is a genuine blind spot rather than an accumulating mess. Three things argue for closing it
anyway: the sweep's stated purpose is that agent branches "would accrue" unswept; a remote-only
branch accrues in the one place nobody looks; and under Ben's decision in cause 1 a cloud session's
work is *expected* to sit on a remote-only branch, so this is now a routine end state rather than an
anomaly.

A **report-only** widening fits the module's existing caution — list remote `claude/*` heads and
name any with no local counterpart, without deleting anything, since deleting a remote branch is the
irreversible act the module's narrow branch-deletion policy already avoids. Report-only is also what
cause 1 asks for: the branch is where it belongs, and what was missing was a way to be told it is
there.

## 7. The policy comment has been fixed

`in/repo_maintenance_policy.json`'s `repo_visibility.github-misc.comment` read "Tracks the canonical
copies of the dotfiles, ~/.claude/CLAUDE.md and the hebrew-prose skill among them." The 2026-09-09
move made that false.

Current state, confirmed before writing the replacement: github-misc tracks `dot-emacs` and
`dot-gitconfig`, which are still canonical there, and `dot-claude/README.md` and
`dot-Codex/README.md`, which are breadcrumbs headed "dot-claude moved to MAM-basics on 2026-09-09"
and "dot-Codex moved to MAM-basics on 2026-09-09". Re-establish with
`git -C C:/Users/BenDe/GitRepos/github-misc ls-files "dot-*"`, which returns those four paths.

The replacement names what github-misc still tracks, when the rest moved, and where it went. The
JSON parses after the edit.

## 8. What is recommended, and what is left for Ben

Recommended, each with the section that argues it:

1. **Merge `origin/claude/charming-mayer-xknwcw` into `main`** after freshening the three stale
   figures in §3 and running the suite on the merged tree. The merge is clean and the defect is
   live.
2. **Move the review plan to `MAM-basics/doc/`** with the repointing pass of §5 applied in the same
   commit. No redaction is needed.
3. **Consider the report-only widening of `--clean-worktrees`** in §6 cause 2. Under Ben's decision
   in §6 cause 1 — that a cloud session will be left to push only to its own branch — a remote-only
   `claude/*` branch is the expected end state of cloud work, and this widening is what would make
   that state visible.

4. **Repair the seven Unicode-normal clusters in the four
   `in/accgram/edition_transcriptions/*.txt`** (§1). They are hand-authored prose in comment
   headers, not captures, and the header is never re-derived, so the repair cannot be undone by
   `build --derive-only` or fail `build --check`.

Left for Ben, because each is a decision rather than a correction:

1. **Whether the lint's scope gains `in/accgram/edition_transcriptions/*.txt`** (§1), so that
   recommendation 4's repair is guarded rather than merely done once. A blanket widening to `.txt`
   is not the way, since 11 of the 15 offending `.txt` are genuine captures.
2. **Whether the review joins the public periodic series** now that its subject files are public
   (§5), which is the plan's own D16 asked again under changed facts.
3. **Whether to close the lint's `is_file()` silent-skip channel** (§1).

## 9. How the figures here were measured

Commands are given in the sections that use them. The three measurements that needed a script,
rather than a single command, ran from `C:/Users/BenDe/GitRepos/MAM-basics` on that repository's
venv, `.venv/Scripts/python.exe`, importing `mb_cmn.uni_denorm`, and are untracked under `.novc/`:

1. **The byte-exactness of `73ab8383`** — for each file the commit touched, the three predicates in
   §1 over the before and after blobs.
2. **The offender scans** — the lint's own logic against a named revision or tree, reporting
   offending files and offending clusters, run against the branch base `20ebbac1`, against `main`
   at `a50da28b`, and against the hypothetical merge tree `af5e8cd7`.
3. **The scope-claim checks and the plan screen** — the `.html` and `.txt` widening inventories, the
   plan's Hebrew and mark order, and the repointing counts.
4. **The edition-transcription diagnosis** of §1 — whether each file equals its NFC and NFD forms,
   the MAM-normal against Unicode-normal cluster tally counting only clusters that can tell the two
   orders apart, the Hebrew-bearing fields of the committed JSON, and whether every offending line
   begins with `#`.

**One deliberate use of `unicodedata.normalize` needs stating**, since `CLAUDE.md`'s first section
bans it. Measurement 4 calls it to ask whether a file already equals its own NFC or NFD form. That
is a question about the text rather than a change to it: nothing is written back, and no repair
anywhere in this assessment goes through it. Repairing by normalizing remains the banned act, and
`give_std_mark_order` remains the only sanctioned repair.

Each is throwaway-grade under `~/.claude/CLAUDE.md` §"Throwaway scripts: the lowest bar of
software". A fresh session should rewrite rather than hunt for them; the predicates and pathspecs
above are the whole of what they do.
