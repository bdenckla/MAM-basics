# Findings of the 2026-08-26 review of the public repos since 2026-08-22

Filed as [#261](https://github.com/bdenckla/MAM-basics/issues/261), which is a thin pointer to
this doc. This is the first review under the public-repos-only scope (Ben's decision, 2026-08-26,
recorded at the end of `doc/review-findings-2026-08-22.md`): it covered **every public clone
directly under `~/GitRepos`** — committed work from the 2026-08-22 review's anchors (MAM-basics
`b37bdb4`, UXLC-utils `c8db329`, holman-ketiv-qere `6b0bb63`, book-of-job `aa20c61`,
codex-index-aleppo `a50f40e`, codex-index-cam1753 `7e5ca23`, codex-index-leningrad `2abd7f6`;
elsewhere the previous review's start time, 2026-08-22T15:45 local) through 2026-08-26 ~19:05
local, when this review started. That is **125 commits across 12 public repos with activity**:
MAM-basics 99 (`b37bdb4..363fe41`), codex-index-aleppo 5, holman-ketiv-qere 4, MAM-parsed 3,
MAM-simple 3, book-of-job 2, codex-index-cam1753 2, UXLC-utils 2, MAM-with-doc 2, MAM-OSIS 1,
MAM-for-Sefaria 1, document-index 1 — re-measurable per repo with `git log <anchor>..<head>
--oneline`, or `git log --since=2026-08-22T15:45 --oneline` where no anchor was recorded. Four
public clones were quiet (ArtScroll — a public gist, checked via `gh api gists/… --jq .public` —
codex-index-leningrad, diffable-pointed-hebrew, phonetic-hbo). Two clones under `~/GitRepos` are
**private** and fall to the private series: MAM-private (110 in-window commits, reviewed by that
series' own 2026-08-26 doc earlier today) and github-misc (4 in-window commits; hbofonts, also
private, was quiet). One exception was deliberate: this review did verify github-misc's
instruction-file plumbing — the tracked `dot-claude/CLAUDE.md` and `dot-claude/skills/hebrew-prose/`
are **byte-identical** to the live `~/.claude/` copies, no drift, all five skill files compared —
because the live instruction files govern work in the public repos.

Every candidate tracker's visibility was checked (`gh repo view bdenckla/<name> --json
visibility`): 16 are public, 9 private (al-hatorah, masorah-books, mgketer, trope, github-misc,
hbofonts, MAM-private, wlc-utils-private, breuer-cos — note mgketer and trope, which the
2026-08-22 review swept, are private and now out of this series). Of the 16 public trackers,
**only MAM-basics had in-window activity — 32 issues** (`gh issue list --state all --search
"updated:>=2026-08-22"`): #3 and #4 closed 2026-08-26 with closing comments whose claims verify
against the private tree's tracked files; #232 closed 2026-08-22 by the chip; #233 filed
2026-08-22, every checkable claim in it re-derived (the 17-entry `_PASSAGES` list, the four
caller line numbers, the Nehemiah 8:7 data in MAM-parsed — one `מ:לגרמיה-2` and one `מ:פסק` in
`plus/FA-Ezra-Nexemiah.json` at that verse); and **#234–#260, 27 issues Ben transferred into
MAM-basics this evening, 18:50–19:01 local** — finding 2 below.

The review ran in four agent streams plus the main session: the codex-index trio's Phases 6 and
7 with the four commits the previous review left unverdicted; the wlc-utils clone removal, the
redirect-stub freeze and the three-repos plan's Phase 0; the near-aleppo public side with the
sigil-decoding docs and the Sheet-refresh chain; and the tracker sweep with the 2026-08-22
chip's record. The main session measured MAM-basics' tree health and the message hygiene of the
125 commits.

Anchors: HEADs at review start were MAM-basics `363fe41`, codex-index-aleppo `1c12a8e`,
codex-index-cam1753 `7309882`, codex-index-leningrad `2abd7f6`, holman-ketiv-qere `94cab4a`,
book-of-job `3f096b9`, UXLC-utils `b7b4eb9`. Every tree was clean with HEAD = origin/main, and
no session was live in any repo — the first review of the series with no co-present session, so
the in-place suite and lint runs were uncontaminated. The series' standing limitation applies
again — no regeneration-and-diff of tracked outputs was run in place — with blob-level
comparisons standing in (and holman-ketiv-qere's two regenerated artifacts checked for
re-staling against UXLC-utils' one later commit, which touched only docs and CLC HTML). Unlike
every previous review, this one landed commits of its own during its run: `bf8886a` and
`629d73b` under finding 1, on Ben's mid-review decision, plus the commit that lands this doc.

## The verdicts the previous review owed: the trio's Phases 6 and 7, and all four commits, sound

**Phases 6 and 7 (`87ef5c0` and the per-repo commits) verify item by item.** The vendoring
policy went 205 → 90 lines with `repos` down to MAM-simple, diffable-pointed-hebrew and
MAM-private and overrides 10 → 2; `doc/vendoring-inventory.md` went 18 rows/112 files → 12
rows/97; zero `codex-index` strings survive in any of the four generated audit artifacts, at
`87ef5c0` and at HEAD; the programme plan's trio row reads DONE 2026-08-22 — every phase.
**The 2026-08-22 review's finding 2 hazard is gone**: the untracked `__pycache__` directories
that alone kept the vendoring test green are deleted, the policy no longer names the scan roots
that needed them, and `test_vendoring_policy_paths` collects 18 and passes with no dependence on
untracked state. `py/check_all.py` re-runs live at 7 of 7 over **509** files and **297** `.py`,
exactly the Phase 7 record. Phase 6's five repointings all landed and spot-check true, and the
sixth site `48485f3` found (the `main_uxlc_estimate_atom_loc.py` docstring) now cites both
`linebreak_search.py` copies as this repo's.

**The four previously unverdicted commits.** `fe6cef2` (cam1753 Phase 3) checks at blob level:
19 files added, the 23 cam1753 `.py` splitting 11 arrivals / 12 dissolutions exactly, and every
cam1753 blob at `a9c3abd^` either byte-identical to a MAM-basics blob at `fe6cef2` or differing
by exactly the recorded edits (two one-line import repoints, the `main()`-and-guard additions,
the `repo_scopes` rework of the four lints, `page.py`'s `parent.parent` repair). `09d68c5`'s
headline holds: all six evacuated repos track 0 `.py` at current HEADs (`git -C <repo> ls-files
"*.py"` empty for book-of-job, holman-ketiv-qere, UXLC-utils and the trio). codex-index-aleppo
`2bdcfde` deleted the recorded three-folder workspace file; codex-index-cam1753 `a9c3abd` is
25 D + 5 M, 177 tracked → 152, nothing lost at blob level, with the five rewrites carrying the
recorded content. The rest of the two repos' windows also verify: `3003a06` (the settings.json
deletion b625665 records — but see finding 4), `94b824a` (the one-line provenance repoint, its
target `py/main_ac_download_pages.py` tracked here), `1da6b23` (the corrected 35-pages sentence
is true against the artifact: 35 fail rows, all 35 carrying the "No col 1; No col 2" pair, 29
holding exactly it), `1c12a8e` (verified from all three sides — MAM-basics `e138191` deleted the
generator, MAM-private deleted the sibling artifacts the same afternoon, aleppo's CLAUDE.md
paragraph is past tense), and `7309882` (no `.venv` on disk there). codex-index-leningrad's
quietness is exactly consistent with the records: Phase 6 found nothing to repoint there and
Phase 7's only tracked edit was cam1753's.

## What else the review verified and found sound

**The 2026-08-22 chip's self-reported record verified in every particular, zero discrepancies.**
The previous review's closing sections were written by the chip itself and no review had checked
them. Now every claim has been: `de8a28b`'s ruff clear decomposes exactly as recorded (6 F541,
1 F401, the 16 E402 as import moves in the three Copilot-era entry points, 1 F841, 1 E731, all
output-neutral) and `ruff check py` prints `All checks passed!` today; `cb3e7b2` carries every
correction it claims (ten commits, five files, 58 μY, 7 holam-he rows, 19 rules, 152 → 45, `#19`
once, 17,051/+54, three dotfiles, both dead `py_uxlc_loc/` exclusions gone, the docstring naming
both callers); `d8bec00`'s two dated notes are in place (its "both workspace files still list
`../wlc-utils`" was true at 19:25 and superseded at 22:51 by `aa89f84` — a record of its moment,
not an error); holman `36718d6`'s diff is **exactly the four JSON lines and two `<dd>` lines the
previous review predicted** (Job 32:6.6 line 19.6 → 22.0, Job 32:12.1 line 1.2 → 3.1); book-of-job
`3f096b9`, holman `5f419ef`/`b1e1a2d` and codex-index-aleppo `1da6b23` all match their records;
and the chip's start anchors reproduce from the commit graph. The halve.md pair agree: `ab54b5c`
records Ben's drop-never-copy decision (2026-08-23) and holman `94cab4a` deletes the file on a
further dated decision (2026-08-24), "stays in holman-ketiv-qere's history" remaining true.

**The wlc-utils clone removal and the stub freeze are exactly as documented.**
`in/wlc_redirect_pages.json` holds exactly 154 unique paths, equal in both directions to the
remote's stub set (`gh api repos/bdenckla/wlc-utils/git/trees/main?recursive=1`, 155 `gh-pages/*.html`
minus `404.html`); `py/tests/test_wlc_redirect_manifest.py` checks what CLAUDE.md says, resolving
no sibling and failing rather than skipping on a missing manifest; `wlc_utils_pages_dir` raises
with the documented clone command and is reached by exactly `build --publish` and no-`--dir`
`check`; the clone is absent, `all-repos.code-workspace` lists 19 folders all on disk, and
`load_workspace_repo_dirs` raises on a missing listed folder as CLAUDE.md claims. The remote is
alive (PUBLIC, not archived) and three spot-fetched stubs each answer "Moved to MAM-basics" with
a working target. The repoint sweep's negative claim re-verifies: a fresh sweep over all 19
clones for `bdenckla.github.io/wlc-utils` and `github.com/bdenckla/wlc-utils` classifies every
hit as redirect mechanism, deliberately-kept tanach.us snapshot, plan or execution record, or
prose describing the redirect — **zero unrepointed live citations**. The three-repos plan
(`doc/PLAN-evacuate-the-rest-of-three-repos.md`) re-derives figure for figure at its pinned
commits — the Scale table's six first columns exact, the collision census (5/6/45 path, 1/0/41
blob), Decision D's blob claims (all 24 `MAM-XML/*.xml` one blob with codex-index-aleppo), the
layer-4 sweep, and `9c348b5`'s corrections spot-verified six of eight — with one misrounded
total cell, finding 7. The plan is PAUSED after Phase 0 (`315ab55`, Ben's quote and the
cancelled chip), and the seven Phase 0 commits each touched the plan file alone.

**The near-aleppo public side is in the state its commits claim.** The stub
`doc/PLAN-near-aleppo.md` points at a plan, a privacy-criteria file and a whole-repo annex that
all exist in MAM-private, and contains none of the five strings `fc06d5d` asserts it lacks. The
privacy scrub left **zero residue**: every `mgketer` mention in tracked MAM-basics (141
occurrences, 30 files) is a mgketer.org URL builder or a plain tree path in vendoring and
evacuation bookkeeping, and the comparison-mechanism names the scrub commits removed have zero
hits. Spot-checked step figures re-derive from MAM data exactly: the 10 CGJ-before-U+05BD sites
in exactly the six claimed verses, 7 on a chanted word carrying its own sof pasuq (so silluq,
under the verse-final rule) and 3 maqaf-joined (so meteg), Genesis 35:22 among the silluqs
(`d03bdfe`, `59a1715`); 260 letters carrying both geresh muqdam and revia, in 260 verses
(`e158def`); 423 ole (Psalms 353, Proverbs 29, Job 41) and 13 letters with both ole and yored
(`38ccb8e`); exactly one single-consonant atom with no maqaf neighbour in all of MAM's base
text — Deuteronomy 32:6's הַ (`7ed324d`); 116 zero-parameter gray-maqaf templates (`10d7052`).
The vendored `template_names.py` in MAM-simple is byte-identical to this repo's (`2f6db2e`,
MAM-simple `06a5288`), and the historical claim re-derives (7 `קו"כ` hits at `2993dbd~1` in
MAM-parsed's Genesis, 0 after). The sigil-decoding history claims all check against git: the
doc existed at 376 lines before `20ec7f2` replaced it while saying "Add", and `5be1054`'s
restore diff is +25/−3 with the three removed lines exactly the rows it says it amended.
Seventeen of the qualifier table's pairing counts re-derive exactly (`e9b8b60`, `5aa036d`), and
`c3e8077`'s Cairo-13 gloss is on the rendered page with zero "T-S" remaining.

**The Sheet-refresh chain is coherent end to end.** `out/diff_mamws_mamgo-auto-edits.json` is
`[]` at HEAD, having stood untouched from its 2026-04 creation until `77383ac`; the 82
auto-edits sum (41+20+10+5+4+2) is right; `d0328d5`'s diff is exactly the six section CSVs plus
the template-documentation tab, with wsgo collapsing back to empty; the 2 Chronicles 34:12
repair is visible in `in/mam-ws/FD-2Chronicles.json` and the note body renders in MAM-parsed's
regenerated Chronicles (`da167e7`). Downstream, MAM-parsed `be359a0` moves exactly 14 books in
plain and plus with Exodus 26:7 carrying its promised parashah note, `0128e69`'s two SVG diffs
are exactly the three count labels tracking `ffb4fdc`'s DOT diffs (242 → 244, 141 → 143, 7 → 8),
and MAM-simple, MAM-OSIS, MAM-for-Sefaria and MAM-with-doc all touch the expected book families
with clean Hebrew. MAM-with-doc `5b3bcf3`'s change-log claims verify: the four qere-change
entries are present with matching categories and diff_count is 139 and 33. The five
MAM-with-doc verse-URL builders in this repo all pass the page name through
`urllib.parse.quote` (`c1105e2`), and no sixth unquoted builder exists under `py/`.

**MAM-basics' tree is healthy and the suite chain closes — after finding 1's repair.** At
`629d73b` (post-repair): **941 passed, 5 skipped, 59 subtests** (`.venv/Scripts/python.exe
py/main_test.py -q`, 101s), the five skips the edition-transcription semantic channel;
collect-only 946 = 941 + 5; `ruff check py` clean; `black --check py` clean at 1,133 files;
`git ls-files` = 2,279 at `363fe41`; **zero `sys.path` mutations in tracked source** (the grep
returns only docstrings describing the rule). The chain from the previous review's 940: **941**
at `e761cef` (2026-08-22 22:48, the new redirect-manifest test, its message recording exactly
that figure) → **red** from `d0328d5` (2026-08-26 17:54) through `363fe41` — finding 1 —
→ **941 green** at `629d73b`.

**Message hygiene: zero banned constructions, but a trailer regression — finding 9.** Across
the 125 public in-window commits (all authored `bdenckla@alum.mit.edu`): zero genuine "the
latter"/"the former" (every match is a quotation of the phrase being corrected, in `cb3e7b2` and
book-of-job `3f096b9`); every "the other" names its counterpart or a side already named in the
sentence; no bare "witness" outside quoted issue text.

## Findings

In rough order of consequence. Finding 1 reached the tree and was repaired during the review on
Ben's decision; findings 3, 4, 6, 7 and the first item of 8 are record errors fixed in the
commit that lands this doc; findings 2 and 5 are Ben's.

1. **The suite was red at review start — the first red the series has found — and was returned
   to green during the review, by Ben's decision.** `d0328d5` (2026-08-26 17:54, the Sheet
   download) brought five lines of decomposed h-with-dot-below (h + U+0323) into
   `in/mam-go/template-documentation-tab.csv` (lines 98, 122, 123, 124, 127 — petuxah, yerax,
   etnax and mitaxat in the Sheet's own template prose), and both NFC tests failed on them:
   **2 failed, 939 passed, 5 skipped, 59 subtests**. The file had been clean since the
   2026-07-01 NFC migration (at `d0328d5^`: 0 decomposed, 13 precomposed U+1E25; at `d0328d5`:
   6 decomposed, 7 precomposed — the download undid part of #187's migration for that file), and
   none of the commits between `d0328d5` and `363fe41` records knowing. Ben, mid-review: *"I
   have no idea why the Sheet would have started using decomposed 'h with dot below' but I don't
   really care that it does, so just add it as an expected exception to the rule."* So `bf8886a`
   adds the tab to `_EXCLUDE_MAM_GO_FILES` — the whole of `in/mam-go/` is a download of the
   Sheet now — and `629d73b` rewrites the new comment onto the house `x` shorthand after the
   transliteration denylist flagged its ASCII "yerah" (the two lints together leave exactly one
   way to name these words in a comment). Suite green at `629d73b`: 941/5/59. Durable note: the
   decomposed text lives in the Sheet's cells, so it will arrive again with every download, and
   the exclusion is what makes that harmless.

2. **Ben transferred 27 open issues into MAM-basics during the review window's last minutes, and
   the consolidation is documented nowhere.** Between 18:50 and 19:01 local this evening,
   **#234–#260** arrived by transfer (GraphQL `TransferredEvent.fromRepository`):
   codex-index-cam1753 2, MAM-simple 2, codex-index-aleppo 6, MAM-parsed 8, MAM-with-doc 9 —
   exactly each source's whole open set, all five sources public, so nothing private became
   public, and all five source trackers now hold closed issues only. CLAUDE.md's "Five issue
   trackers" section does not yet know that five more public trackers were emptied of open
   issues into this one, and the transfer's first casualty is same-evening:
   `e624139` (18:27) had carefully qualified `doc/sigil-decoding.md`'s umbrella-tracker
   citations as `MAM-with-doc#6`, and at 19:01 that issue became MAM-basics **#257** ("Decode
   sigils", open). The citations still resolve — GitHub answers the old URL with a transfer
   redirect, which Ben observed during the review — and under this repo's convention the
   citation's home form is now a bare #257. Left as written, per that observation; how the
   Five-trackers section should absorb the consolidation is Ben's to shape (the private side
   already has its half: new issues go to MAM-private or MAM-basics and nowhere else).

3. **"One tool with 43 lines of drift" survived the correction pass that was supposed to land
   it.** The true figure is **32** (28 insertions + 4 deletions), measured by the 2026-08-22
   review's finding 7 and re-measured now (`git diff --no-index --numstat` of
   `7e5ca23:py_mam_xml/mam_xml_verses.py` against `b37bdb4~1:py/py_ac_loc/mam_xml_verses.py`).
   `cb3e7b2` landed finding 7's other corrections but omitted this item, so "43" still stood in
   three editable places — the trio plan's Status row, its Phase 3 record, and
   `py/cam1753_paths.py:30` — which also means the previous review doc's chip record ("Every
   figure re-derived first and each correction dated in place") overstated what `cb3e7b2` did.
   All three sites fixed in the commit landing this doc; the figure also rides in the immutable
   `b37bdb4` and `fe6cef2` messages.

4. **The settings.json orphan record miscounts its own globs, in two mutually contradictory
   forms.** The deleted file (`git -C ..\codex-index-aleppo show
   "3003a06^:.claude/settings.json"`) held ten globs: `Bash(git *)`, `Bash(cd **/* && git *)`,
   three naming that repo's own `.venv`, one `Bash(**/.venv/…)`, three `gh issue`, one `Read()`.
   `3003a06`'s message (echoed by `b625665`) says "six were still live … only the four naming
   this repo's own .venv were dead" — three name that repo's own `.venv`, so the live count is
   seven; and the trio plan's orphan-candidates table had the split backwards ("six of its ten
   permission globs name a `.venv` python", "two `gh issue` globs"). The plan's table and its
   Status-row sentence are corrected with dated notes in the commit landing this doc; the two
   commit messages are immutable.

5. **The qualifier table's evidence for the siglum ד is understated, and the count is
   inconsistent with its own citation.** `doc/sigil-decoding.md` cites the compound `ומסורת-ל,ד`
   at Daniel 3:25 as what attaches מסורת to ד, and the מסורת row says ד (1) —
   but the same compound also occurs at Daniel 4:7 and 7:15 (three occurrences, re-derivable by
   loading `plus/F1-Daniel.json` and searching decoded strings). The row's ל count of 135 counts
   all three sites as ל attestations without distributing the comma pair, under which convention
   the cited compound attests nothing on ד and the citation contradicts the count; under the
   distributing reading the doc itself uses elsewhere, the ד count should be 3 or 4. `5aa036d`'s
   own commit message quotes the full inventory — ד at 5 occurrences — so the evidence was in
   hand and the doc recorded a third of it. Left to Ben: the fix needs a convention choice about
   distributing comma-joined sigil pairs, not just a figure.

6. **Three smaller record errors in the trio family, fixed with dated notes in the commit
   landing this doc.** The Phase 7 record said `--all` "rewrote the three tracked artifacts"
   where its own next sentence counts four generated files, and gave `vendoring_compare_out.txt`
   as "105 rows → 97" where the tracked file went 112 data rows → 97 (105 was the uncommitted
   stale-state regeneration at `ea1f035` described one section later). The Phase 3 record's
   "nineteen files added and three modified" is 19 A + **4** M, the fourth being the plan file
   itself carrying the record. And `b625665`'s message mixes two tree states — "check_all.py
   7 of 7 over 510 files" beside an NFC scope count that requires `3003a06`'s deletion, which
   had already taken the corpus to 509 four minutes before `b625665` landed; the message is
   immutable and the plan's Phase 7 record already establishes 509, so this one is recorded
   here only.

7. **The three-repos plan's Scale-table total cell said 55.4 MB outside `gh-pages/`; the true
   value is 55.5.** A sum of the three already-rounded cells (8.1 + 22.6 + 24.7) rather than the
   rounded sum — the exact total is 58,183,004 bytes = 55.49 MB, which is also what the
   section's own prescription `MB − gh-pages MB` gives (174.6 − 119.1). Every per-repo cell was
   right, and nothing downstream consumes the total. Fixed with a dated note in the commit
   landing this doc.

8. **Prose, the window's full count of that class.** (a) One bullet in `doc/sigil-decoding.md`'s
   prose-aliases list opened on Hebrew (`כתי"ל` as the first character of the line), laying the
   rendered bullet out right-to-left — given an English runway ("the alias …") in the commit
   landing this doc. (b) The qualifier table's "Attested on" cells begin on a Hebrew sigil and
   mix Latin digits, so the sigil-count pairs render in scrambled order; the fix is a runway or
   separate cells, and it is a design choice over a table Ben is actively authoring, so it is
   recorded rather than made. (c) `b308319`'s message overstates its bug: "four real ones had
   silently left the published change log" — the four qere changes never left the committed
   change-log JSONs; what the quote-mismatch bug did was make any post-`2993dbd` regeneration
   drop them, and no such regeneration was ever committed. MAM-with-doc `5b3bcf3`'s phrasing is
   the accurate account. The message is immutable; the code fix and artifacts are right.
   (d) Borderline, recorded only: the sigil-decoding operator table glosses `=` with "reads"
   four times where the house verb is "has", and "five witnesses who saw the codex whole"
   applies "witness" to people rather than to a text — outside the ban's object, inside its
   spirit.

9. **Eleven in-window commits lack the `Co-Authored-By` trailer, and unlike previous windows,
   all of them are session-written.** Ten of the 125 public commits (plus github-misc's
   `78c18e2`), every one with a full body: seven from the trio session's Phase 6–7 sweep across
   six repos (2026-08-22 16:26–16:58 — `94b824a`, `7309882`, `87ef5c0`, `b1e1a2d`, `81e036b`,
   `292e7a7`, `48485f3`) and three from 2026-08-24 sessions (`94cab4a`, `e138191`, `1c12a8e`).
   The previous window had 3 of 90, of which one was Ben-typed and two were another client's;
   this window's rate is worse and its commits are unambiguously session-written. No action a
   review can take — recorded so the pattern is visible.

## How the review was acted on (2026-08-26, during the review)

Finding 1 was repaired mid-review on Ben's decision: `bf8886a` (the exclusion) and `629d73b`
(the x-shorthand comment), suite green at 941/5/59, both pushed before this doc was written.
Findings 3, 4, 6, 7 and 8(a) are fixed in the commit that lands this doc — dated corrections in
`doc/PLAN-evacuate-python-from-codex-index-trio.md` and
`doc/PLAN-evacuate-the-rest-of-three-repos.md`, the figure in `py/cam1753_paths.py`, and the
English runway in `doc/sigil-decoding.md`. Findings 2 and 5 are Ben's: the first needs him to
shape how CLAUDE.md's Five-trackers section absorbs the consolidation (and whether
sigil-decoding's still-resolving `MAM-with-doc#6` citations become bare #257), the second a
convention choice about comma-joined sigil pairs. Findings 8(b)–(d) and 9 are recorded only.

**Findings 2, 5 and 8(b) were acted on 2026-08-27, in a follow-up session, each on Ben's
answer to one question.** Finding 2: `97b559b` — the Five-trackers section absorbs the
consolidation keeping its "Five" name (Ben deferred the framing to the session's judgment),
and `doc/sigil-decoding.md`'s six `MAM-with-doc#6` sites became bare `#257` ("sure, repoint
them to MAM-basics #257"). Finding 5: `5da49fd` — Ben's convention: a comma-joined sigil
list after the qualifier מסורת/מסורות is plural shorthand, the qualifier distributing over
the list, deliberately not generalized to other qualifiers; both rows were re-derived under
it against MAM-parsed `0128e69` by a script that first reproduced the old direct-only cells
exactly, and the question is filed for Avi Kadish's feedback as #262. That re-derivation
also found the ד evidence understated beyond this finding's statement — `מסורת-ש1,ד` at
Zechariah 9:15, missed by `5aa036d`'s five-occurrence inventory, plus plural, equals-sign
and bare-authority variants at Daniel 3:25 and 3:5 — all now in the doc's ד bullet. Finding
8(b): the runway, Ben's choice ("go with the runway"); every "Attested on" cell opens `On:`
as of the commit landing this note.

**Avi Kadish answered #262 later that same day, and finding 5's convention is now partly his
and partly still pending.** His comment confirms the distribution for the מסורת and מסורות
qualifiers and settles their morphology on the construct singular of מסורה — the two spellings
differ over how many sources have the note, not over singular against plural — so
`doc/sigil-decoding.md`'s item 6 states his answer where it stated Ben's reading, and both rows'
Meaning cells are rewritten in his terms. Two further things came as asides, to a question that
had asked neither:

1. **The siglum ד is the Venice Miqra'ot Gedolot**, used as Breuer used it and later replaced in
   MAM by מ"ג. It now has a row in the doc's edition table, its eleven corpus sites enumerated,
   and the "Two sigla the qualifier table cites that nothing here decodes" bullet is rewritten
   as resolved. No appendix could have decoded it: it is a layer of MAM's notation that did not
   survive into the finished edition, which is why the source hierarchy gains a sixth entry for
   Avi's testimony as MAM's editor.
2. **Isaiah 56:10's `מסורת-לד` is `מסורת-ל,ד` with the comma missing**, so there is no siglum
   `לד` and the speculation that it might be `ל34` is retired. The site becomes a further ד
   site, taking the מסורת row's ל from 139 to 140 and its ד from 5 to 6. The missing comma is an
   error in MAM itself — present in MAM-parsed `0128e69` and in the Wikisource-side input at
   `in/mam-ws/C1-Isaiah.json` alike — and it is Ben's to dispose of: recorded with its evidence
   in the doc, with no live wiki touched.

Avi also answered yes to #262's third question, which would generalize the distribution to the
other nine qualifiers and grow the כתיב and קרי rows considerably. Ben's instruction that day
was to put worked examples to him before concluding it, since that question named two sites
without spelling out what either reading would mean at them. Those examples are the second
comment on #262; the restriction to the two qualifiers stands meanwhile, marked pending rather
than settled.

## Open ends the window itself declares (not findings)

The tracker consolidation's documentation (finding 2) — CLAUDE.md's Five-trackers section, and
whatever prose should record that five public trackers now hold closed issues only. The
transferred #234–#260 themselves: their bodies predate the window and were not claim-checked;
several carry old figures a future pass could verify against the current tree. skadish1's
2026-08-19 question on #185, still unanswered in-thread, still Ben's to post. The three-repos
total evacuation, PAUSED after Phase 0 by Ben's decision (`315ab55`) — resumption is his call.
The scan-pages undertaking, parked at Phase 0 since 2026-08-07, now four quiet windows. The
hcanat.us /Notes/ template question, unanswered for as long. MAM-basics #225, #226, #227, #229
and #230, open and untouched in-window. The near-aleppo undertaking continues in MAM-private
under the private series, its public tail here being the census step `363fe41` added to the
mega pipeline. And the Sheet's decomposed h-with-dot-below will arrive again with every
download — expected and harmless after `bf8886a`, which is why that is not an open end so much
as a property the exclusion now documents.
