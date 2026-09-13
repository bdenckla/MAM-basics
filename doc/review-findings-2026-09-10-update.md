# Updates to the 2026-09-10 public-repository review

State: open, first entry 2026-09-12. Every entry here corrects or supplements
`doc/review-findings-2026-09-10.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written. A correction or later disposition goes in a
sibling file named `<stem>-update.md`, which is what this file is for that review.

## Finding 9: the live plan no longer requires superseded FOI bytes

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 9 is
unfixed and not acted on.

Commit `70d1f581` on branch `dual-agent-review-2026-09-10` fixes criterion 9 in the live
`doc/PLAN-silluq-before-gaya-template.md`. The criterion now compares the regenerated
`gh-pages/MAM-with-doc/foi/foi-mtgmtg.json` with the Git blob measured immediately before
implementation instead of requiring the superseded 718-record bytes.

The 2026-09-12 baseline at `f0795231` is blob
`b6c323992bb1d05e5995b1047449931c8e026464`: 717 records, with group counts 354, 228, 19, 102 and
14. The 1 Kings 7:37 record remains in `1/sopa-y/maq-n` and has two U+05BD marks. A later
starting-blob mismatch remains a finding to remeasure, not a reason to restore old bytes.

Product axis: the repair changes a live plan and this update record; it changes no generator or
product. Act axis: both writes are ordinary repository commits on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Inherited item 2: update-file State declaration pointers

Recorded by Codex on 2026-09-12. Inherited item 2 under “Three items this round's integration
inherits” is complete.

Implementation commit `d18cbb4b` on branch `dual-agent-review-2026-09-10` adds the owed pointers
from `CLAUDE.md`'s section “A finished dated document is corrected in `<stem>-update.md`, never
edited” and D12 of `doc/dual-agent-review.md` to the declaration in
`py/repo_util/check_repo_standards.py`'s module docstring.

## Inherited item 3: live user-level synchronization has its source-ref decision

Recorded by Codex on 2026-09-13. Inherited item 3 under “Three items this round's integration
inherits” is re-established. Ben has made the first of its four decisions; the cloud-hook,
deployment-scope and check-scheduling decisions remain pending. No live user-level file, tracked
user-level copy, hook or skill has been changed by this disposition.

Re-measured at review-branch commit `a872790e70d0f02bfa40cc965760c066e0e06918`, local and
remote-tracking MAM-basics `main` are both `1d2ddc3dc8d029af06bf5cb6ac7a9696f2f78caa`, and
both are ancestors of the review branch. The current copies have no drift:

1. `C:/Users/BenDe/.claude/CLAUDE.md` and `dot-claude/user-wide-CLAUDE.md` have SHA-256
   `6EAE1FBA5EB989F71310EBC0A8BB08527E8623F100E17709D45AC3AFB12C2ADF`.
2. `C:/Users/BenDe/.Codex/AGENTS.md` and `dot-Codex/user-wide-AGENTS.md` have SHA-256
   `87C3EDDB6A9F001DAD5481D2162E0CE32D52FE7DB719C4AC651F030B5D4C393F`.
3. Recursive `git diff --no-index` comparisons from the tracked
   `dot-claude/skills/hebrew-prose/` tree to
   `C:/Users/BenDe/.claude/skills/hebrew-prose/` and
   `C:/Users/BenDe/.agents/skills/hebrew-prose/` both exit 0 with no content difference.
4. The two tracked instruction files differ from both `main` and `origin/main` by the
   verification-cadence section added on the review branch. The tracked `verse-links` skill also
   differs by its completed unique-letters lookup documentation, and comments in
   `.claude/hooks/install-user-config.sh` differ by their completed numbering correction. The
   live instruction files therefore currently contain committed review-branch text that neither
   form of `main` contains. This is the concrete condition the selected source-ref policy will
   prevent after implementation; no deployment was run as part of this disposition.

The current deployment procedures are manual and live-first. `dot-claude/README.md` and
`dot-Codex/README.md` tell an editor to change a live copy, copy the result into the primary
`C:/Users/BenDe/GitRepos/MAM-basics` checkout, compare the copies and commit. The commands do not
verify any Git ref before copying. The current shared-skill procedure separately requires the
canonical tracked tree, the live Claude tree and the live Codex tree to agree. No tracked command
has a user-level synchronization `--check` mode, and no suite, maintenance command or local
session-start path checks these copies automatically.

Ben's first decision and the three remaining decisions, with the live alternatives and
consequences, are:

1. **A main-sourced deployment uses a freshly fetched `refs/remotes/origin/main`.** Ben's
   decision, 2026-09-13: concur with Codex's recommendation to fetch `origin` in the primary
   `C:/Users/BenDe/GitRepos/MAM-basics` clone and deploy exclusively from
   `refs/remotes/origin/main`. If the fetch fails, the operation stops before changing any live
   file. An integrated local commit therefore cannot reach live configuration until it has been
   pushed and the remote-tracking ref has advanced. The rejected local `refs/heads/main`
   alternative would have worked without a network refresh, but would have allowed live
   configuration to contain integrated text absent from the remote. The deployment changes no
   MAM generator or product. Applying the deployment writes outside the repository, but the
   deployment itself performs no outward-facing Git write.

2. **Whether the cloud-session hook is an exception to the selected `main` rule.** The current
   `.claude/settings.json` runs `.claude/hooks/install-user-config.sh` at startup, resume and
   compaction. When `CLAUDE_CODE_REMOTE=true`, the hook copies an absent `CLAUDE.md` or
   `hebrew-prose` skill from `$CLAUDE_PROJECT_DIR`, so a cloud session started from a branch gets
   that branch's tracked copies. The hook does not inspect `main` or `origin/main`, and the hook
   does not overwrite a file already present.

   1. **Declare the cloud hook an exception.** A branch checkout may supply configuration to that
      branch's isolated cloud session. This keeps the current network-free bootstrap and lets the
      session receive instructions that accompany the branch, but branch-only instruction text
      can govern the same session before integration. The copy writes outside the repository into
      the cloud container's live home. The cloud-only path cannot be exercised on this machine,
      so a change to the hook must remain reported as locally unverified even if fake-home tests
      pass. The hook reaches no MAM generator or product.
   2. **Make the cloud hook obey the selected `main` source.** A branch session would extract the
      tracked configuration from the selected MAM-basics `main` ref rather than from the checkout
      tree. This prevents branch-only instruction text from governing the session, but the hook
      must define what happens when the selected ref is missing or stale. Skipping the copy in
      that case leaves the cloud session without the user-level configuration; obtaining a fresh
      ref adds a Git dependency to a hook that currently makes no network or Git call. The copy
      still writes outside the repository, and the changed cloud-only path still cannot be
      exercised on this machine. The hook reaches no MAM generator or product.

3. **Whether a main-sourced operation deploys skills as well as the two instruction files.** The
   current procedures treat these as separate operations. The instruction-file operation covers
   `~/.claude/CLAUDE.md` and `~/.Codex/AGENTS.md`. The shared-skill operation maintains a
   three-home invariant: tracked `dot-claude/skills/<name>/`, live
   `~/.claude/skills/<name>/` and live `~/.agents/skills/<name>/`.

   1. **Deploy instruction files and skills together.** The tracked `main` tree would supply both
      instruction files, both live homes of every shared skill, including
      `~/.agents/skills/`, and the live homes of tracked agent-specific skills. This makes the
      known Codex third-home drift detectable and repairable in the same operation. It also gives
      the operation the broadest external write scope. Replacing a live skill directory with the
      current remove-then-copy method is both a write outside the repository and a destructive
      local act; an interrupted replacement can leave a partial live skill. No MAM generator or
      product changes.
   2. **Deploy only the two instruction files.** Skills retain the separate three-home procedure
      in `dot-claude/README.md`. The narrower operation writes two files outside the repository
      and need not delete or replace a live directory, but running the instruction-file operation
      says nothing about whether `~/.agents/skills/` matches the canonical skill. No MAM
      generator or product changes.

4. **Whether a read-only `--check` is manual or attached to a command that runs.** Current
   comparison commands live only in the two READMEs. The SessionStart hook checks for missing
   cloud files, not drift, and exits locally before reading a live file.

   1. **Keep `--check` manual.** The check can compare every selected source and destination and
      return nonzero on drift without writing anywhere. The check touches neither risk axis, but
      drift persists until somebody remembers to run the command.
   2. **Attach `--check` to periodic MAM-basics repository maintenance.** The maintenance pass
      already runs on Ben's machines and can report drift without repairing it. The check remains
      read-only, reaches no MAM generator or product and performs no hard-to-undo act. A
      machine without a live destination needs an explicit “not installed” result rather than a
      false clean result. Attaching the check to the cloud SessionStart hook instead would modify
      the unexercisable cloud path and would cover Claude starts but not Codex starts, so that is a
      materially different wiring choice rather than evidence for the maintenance choice.

Until Ben makes all four decisions, the current live-first procedures, the cloud hook and the
manual comparisons remain unchanged. This decision record changes only the live review update and
reaches no generator or product, so it does not owe a mega run.

Product axis: this disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch. Read-only
checks inspected live user-level files, but no outward-facing act, destructive local act, external
configuration write, unexercisable cloud-hook change or receipt rewrite occurred.

## Finding 11.1: MAM's `סימנים` identifies the Simanim Tanakh

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 11.1
is unfixed and not acted on.

Implementation commit `f13b1a988ebd9871db11f28ea4aec831c48fc0c1` on branch
`dual-agent-review-2026-09-10` adds
`doc/meteg-after-silluq-search-in-mam-documentation-update.md`. The search document is a
finished report, so D12 leaves its two historical references to “the Simanim Tiqqun” intact and
the sibling update says that both references should read “the Simanim Tanakh.”

The correction rests on MAM's mirrored public introduction at
`in/mam-ws-intro/appendices.mediawiki`, which defines `סימנים` in the list of editions based on
the Aleppo Codex as `תנ"ך סימנים (פלדהיים תשס"ח)`. No inference about the Simanim Tiqqun's
haftarot is needed. Finding 11's remaining prose sites were unchanged by this disposition; the
later finding 11.5 entry records Ben's contextual `ḥataf` / `xataf` rule.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 20.2: the three historical referents are named directly

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 20.2
is unfixed and not acted on.

Implementation commit `a65bb60ed66df1cbff72d105abc68c029006a38b` on branch
`dual-agent-review-2026-09-10` completes finding 20.2. The September 8 remediation plan is a
finished document, so D12 leaves both historical phrases unchanged; the plan's existing sibling
update records source commit `0ee34bea8` for the first State and Ben's approval as the event that
made the second State historical. The live September 9 instruction-file remediation plan names
`references/sources-and-corpora.md` directly in place of “the latter.” All three sites were
applicable prose defects rather than protected quotations. No other part of finding 20 changed.

`git diff --check` and the tracked-prose mark-order lint passed. The full suite passed 997 tests,
with 5 skipped and 65 subtests passed. This documentation-only unit does not owe a mega run.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the finished
September 8 plan remains unchanged, and no outward-facing act, destructive local act, external
configuration write or receipt rewrite occurred.

## Finding 20.3: the three paired referents are named directly

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 20.3
is unfixed and not acted on.

Implementation commit `ded05cd1d24baf32fc415e3d4da881b4527b2d99` on branch
`dual-agent-review-2026-09-10` completes finding 20.3. The mega-coverage plan is finished, so D12
leaves its historical “one flag-selected mode of a program and not another” sentence intact and
`doc/PLAN-mega-coverage-update.md` names the mode that the mega runs and the mode that the mega does
not run. The live `py/tests/test_mega_coverage.py` module docstring makes the same two referents
explicit. The live `py/mb_cmn/graphviz_pin.py` module docstring names `check_installed` as the check
that prevents a wrong Graphviz stamp and `stamp_in_svg_text` as the check of existing SVG stamps.
All three sites were applicable prose defects rather than protected quotations. No other part of
finding 20 changed.

Product axis: the correction changes documentation and Python docstrings only; it changes no
generator behavior or product and does not owe a mega run. Act axis: both commits are ordinary
repository commits on the unpushed review branch; the finished mega-coverage plan remains
unchanged, and no outward-facing act, destructive local act, external configuration write or
receipt rewrite occurred.

## Finding 20.4: the five announced sets are numbered

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 20.4
is unfixed and not acted on.

Implementation commit `5d771295d95f87265cbc7ec169402f5f795c28b0` on branch
`dual-agent-review-2026-09-10` completes finding 20.4. The live instruction-file remediation plan
now numbers its two stale conditions. The live hook comment reconciles “Four further trees” with
the three entries it presents, calls them three entries, and numbers them 1 through 3.

The completed five-products evacuation plan and the completed two-artifact assessment remain
unchanged; their existing sibling update files give the two public findings and the three reasons
as numbered lists. The completed meteg-after-silluq screen report also remains unchanged; the new
`doc/meteg-after-silluq-screen-against-uxlc-and-wlc-update.md` gives its two opening definitions as
a numbered list. All five sites were applicable prose rather than protected quotations. No other
part of finding 20 changed.

Product axis: the correction changes documentation and a code comment only; it changes no
generator behavior or product and does not owe a mega run. Act axis: both commits are ordinary
repository commits on the unpushed review branch; all three finished dated documents remain
unchanged, and no outward-facing act, destructive local act, external configuration write or
receipt rewrite occurred.

## Finding 20.5: the seven finding leads put their dispositions first

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 20.5
is unfixed and not acted on.

Implementation commit `a0ff3b45891e21aa0698b9c7690676f998f68ae6` on branch
`dual-agent-review-2026-09-10` completes finding 20.5. The new
`doc/meteg-after-silluq-psalms-72-15-update.md` gives disposition-first versions of summary items
4, 7 and 8. The existing `doc/meteg-after-silluq-screen-against-uxlc-and-wlc-update.md` now gives
disposition-first versions of findings 1, 5, 6 and 7.

All seven sites were individually confirmed as the reports' analytic prose rather than protected
quotations. Each disposition comes from the same report: an established screen or source result,
Phonetic MAM's exclusion as evidence, or a result not found in Yeivin and Breuer. No substantive
finding changes. Both finished source reports remain unchanged.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; both
finished dated reports remain unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.4: the nine possession verbs have live “has” corrections

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 11.4
is unfixed and not acted on.

Implementation commit `0e40b5a1d545d13e815e863c759d6b013b40a5ae` on branch
`dual-agent-review-2026-09-10` completes finding 11.4. The new
`doc/meteg-after-silluq-koren-lookup-candidates-update.md` gives the two corrected Koren-candidates
passages, the new `doc/meteg-after-silluq-job-4-12-update.md` gives the five corrected Job 4:12
passages, and the existing `doc/meteg-after-silluq-psalms-72-15-update.md` now gives the two
corrected Psalms 72:15 passages.

All nine sites were individually confirmed as the reports' analytic prose rather than protected
quotations. Each correction replaces only the cited possession verb with “has” and preserves the
passage's claim. The three finished source reports remain unchanged. The later finding 11.5 entry
records Ben's contextual `ḥataf` / `xataf` rule.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; all three
finished dated reports remain unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.3: analytic `ga'ya` terms have live `meteg` corrections

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 11.3
is unfixed and not acted on.

Implementation commit `2c9b00ca60f077316271af6b5f8ae900cda93566` on branch
`dual-agent-review-2026-09-10` extends
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` with corrected readings for the
analytic category labels in finding 2, the MAM roster statement in finding 4, and the scope note
under “What could not be verified.” Each corrected reading uses “meteg,” as the report's opening
vocabulary note requires.

The finished source report remains unchanged at Git blob
`5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`. The passages reporting MAM's introduction,
Yeivin's `gaʿya`, or Breuer's `ga'aya` remain unchanged, as do all twelve source-reporting sites
in `doc/foi-mtgmtg-empty-cell.md`. The later finding 11.5 entry records Ben's contextual
`ḥataf` / `xataf` rule.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the
finished source report remains unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.2: finding 1's Classification cells name the codices

Recorded by Codex on 2026-09-12. This entry records partial action on finding 11.2: the
Classification-column subunit in finding 1's 31-row table is complete, while finding 11.2's
category label and later prose remain unacted on.

Implementation commit `50f1bf56dc0f311f91641005d4c0f84437059985` on branch
`dual-agent-review-2026-09-10` extends
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` with corrected readings for all
22 applicable Classification cells. The 23 individually checked abbreviations comprise 19 uses
of `L`, corrected to “the LC,” and 4 uses of `A`, corrected to “the Aleppo Codex.” The
Reference, Template, Target and Note columns remain unchanged.

The finished source report remains unchanged at Git blob
`5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`. The category label corresponding to the original
review's line 60 and the later prose corresponding to its lines 108–146 remain for later tasks;
this entry does not claim that all of finding 11.2 is complete.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the
finished source report remains unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.2: finding 2's 23-call category label names the LC

Recorded by Codex on 2026-09-12. This entry records further partial action on finding 11.2. The
finding 2 category label beginning “23: L has a ga'ya to the right of its vowel” is complete;
finding 11.2's later prose remains unacted on.

Implementation commit `b7237bd84f107a8ed7b397871d079ea179087d23` on branch
`dual-agent-review-2026-09-10` extends
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` with the cumulative corrected
reading “23: the LC has a meteg to the right of its vowel (glyph placement).” The category label
was individually checked in finding 2's category list. The correction carries forward finding
11.3's `ga'ya`-to-`meteg` correction and adds only finding 11.2's `L`-to-“the LC” correction.

The finished source report remains unchanged at Git blob
`5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`. The later prose corresponding to the original
review's lines 108–146 remains for later tasks; this entry does not claim that all of finding
11.2 is complete.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the
finished source report remains unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.2: finding 2's parse-failure Judgment cells name the codices

Recorded by Codex on 2026-09-12. This entry records further partial action on finding 11.2. The
Judgment-column subunit in finding 2's 26-row parse-failure table is complete; finding 11.2's
prose after that table remains unacted on.

Implementation commit `9b552fad86ba1cf985d23aff59057b1466d8904a` on branch
`dual-agent-review-2026-09-10` extends
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` with corrected readings for all
seven applicable Judgment cells. The seven individually checked abbreviations comprise six uses
of `L`, corrected to “the LC,” and one use of `A`, corrected to “the Aleppo Codex.” The Reference,
String and Why the parse failed columns remain unchanged.

The finished source report remains unchanged at Git blob
`5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`. The prose beginning “The 52 NON-verse-final
template calls” and continuing through finding 3's item beginning “Psalms 19:7, where L's one
stroke sits on the first syllable” remains for later tasks; this entry does not claim that all of
finding 11.2 is complete.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the
finished source report remains unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.2: the 36 enumerated codex abbreviations are corrected

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 11.2
is unfixed, not acted on or only partly acted on. Finding 11.2 is complete as bounded by the 36
sites that the finding enumerates.

Implementation commit `fa88d68f00e74cc97a714fbead97580da718530f` on branch
`dual-agent-review-2026-09-10` extends
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` with corrected readings for the
five remaining narrative abbreviations. The four individually checked passages begin “The 52
NON-verse-final template calls,” “Psalms 18:46, where L has,” “MAM's editorial rule that where L
has two or more ga'yot,” and “Psalms 19:7, where L's one stroke.” Every `L` in those passages
means the LC.

The earlier entries in the same update file correct 23 abbreviations in finding 1's
Classification cells, one abbreviation in finding 2's category label and seven abbreviations in
finding 2's parse-failure Judgment cells. Those 31 corrections plus the final five narrative
corrections account for all 36 sites named by finding 11.2. The finished source report remains
unchanged at Git blob `5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the
finished source report remains unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.6: the historical filename requires no remediation

Recorded by Codex on 2026-09-12. Finding 11.6 is recorded with no remediation authorized or
required.

The live `doc/PLAN-silluq-before-gaya-template.md` remains `State: live`. Its passage beginning
“The element name deliberately uses `meteg`, not `gaya`” still assigns `meteg` to MAM-simple's
public English vocabulary. Git history shows that commit `772545d5` introduced the plan at its
current path.

The seven in-scope references remain seven path references across four files: one in
`doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md`, three in `doc/foi-mtgmtg-empty-cell.md`, one in
`doc/meteg-after-silluq-job-4-12.md`, and two in
`doc/meteg-after-silluq-search-in-mam-documentation.md`. Each reference identifies the existing
plan or uses its path in a command; none states a filename policy. The plan is not renamed, and
this disposition makes no choice among `gaya`, `ga'ya` and `meteg` for filenames.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository commit on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 18: corrected historical counts require no implementation remediation

Recorded by Codex on 2026-09-12. Finding 18 is disposed of as an evidence-only finding; no
implementation remediation is authorized or required.

A fresh reading of NUL-delimited `git ls-tree -r --name-only -z` output, split only on NUL,
reproduces the corrected historical counts accepted in C6 and turns 3 and 4:

1. Commits `38a606e2`, `c2f238f2`, `f1166057`, `931d6762`, `c36f5baa` and `9d1de074` each have
   1,074 tracked HTML files overall, 1,829 tracked files under `gh-pages/` and 578 tracked HTML
   files under `gh-pages/`.
2. Commit `0354b6cc` has 598 tracked HTML files overall, 1,859 tracked files under `gh-pages/`
   and 579 tracked HTML files under `gh-pages/`.

The NUL-delimited filenames also confirm the two tracked Holman HTML paths named in C6. Ordinary
line splitting treated Git's quoted forms of those paths as filenames whose final character was
a quotation mark, so the original suffix test returned 1,072 rather than 1,074. The same quoted
forms explain the historical `gh-pages/` undercounts. Finding 18.2's inference that two untracked
HTML files accounted for 1,074 is therefore withdrawn in the completed review exchange.

Finding 18.1 remains unverified. The live public tree does not establish the archived run's exact
inputs, and identical bytes in two archived log files do not establish that either log file was
copied. This disposition makes no attribution for how the archived log files arose.

Finding 18 concerns the interpretation of historical evidence, not generator behavior or a
product defect. The numerical correction is already recorded in the completed review exchange,
and finding 18.1 supplies no evidence that selects an implementation change. No historical
finished report is edited.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository commit on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 8: applicable State defects have declarations

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 8 is
unfixed or not acted on. It excludes the historical review State lines that D10 of
`doc/dual-agent-review.md` protects and does not add the mechanical check that finding 8 presents
as a separate proposal.

A fresh NUL-delimited `git ls-files -z` census at starting commit `eb79e618` found 25 direct
`doc/PLAN-*.md` files after excluding sibling update files. Nine plans needed effective State
declarations:

1. `doc/PLAN-close-out-review-2026-09-08.md`: `State: executed 2026-09-10` in its new sibling
   update.
2. `doc/PLAN-efficient-wikisource-downloads.md`: `State: executed 2026-09-10` in its existing
   sibling update.
3. `doc/PLAN-evacuate-five-MAM-products.md`: `State: executed 2026-09-10` in its existing sibling
   update.
4. `doc/PLAN-evacuate-public-repos-programme.md`: `State: executed 2026-09-10` in its existing
   sibling update.
5. `doc/PLAN-wikisource-derived-mam-products.md`: `State: executed 2026-09-10` in its existing
   sibling update.
6. `doc/PLAN-worktree-file-consolidation.md`: `State: executed 2026-09-10` in its new sibling
   update.
7. `doc/PLAN-deferred-template-projection-decisions.md`: `State: paused 2026-09-12` at line 3.
8. `doc/PLAN-retire-codex-index-image-work.md`: `State: live` at line 3.
9. `doc/PLAN-retire-google-sheet.md`: `State: live` at line 3.

The first six plans are finished execution records, so D12 leaves all six plans unchanged and
their sibling update files supply the effective declarations. The last three plans describe work
that is paused or live, so the three State lines are kept true in the plans themselves. The
fourth plan added after the review anchor, `doc/PLAN-dispose-mega-pipeline-review-findings.md`,
already begins with `State: live` and needs no correction.

The same census found 21 review files in D10's families. Sixteen historical State lines remain
unchanged under D10's preservation rule. The four files in the 2026-09-10 round use the applicable
initial-argument or later-turn State phrase. The remaining line is
`doc/review-findings-2026-09-08.md`'s `State: remediated 2026-09-10`, last written by `9d1de074`
on 2026-09-10 after `2cddb893` recorded D10 on 2026-09-09. The review's existing sibling update
now supplies the corrected reading `State: acted on 2026-09-10` with the original qualifications.

Implementation commit `d3ab7cf16949c44d5c1d5fe01c53f311d38afadf` makes only those bounded
corrections. `git diff --cached --check` and the tracked-prose mark-order lint passed. The full
suite passed 997 tests, with 5 skipped, in 117.26 seconds. This documentation-only unit does not
owe a mega run.

Product axis: the corrections change documentation only and reach no generator or product. Act
axis: both commits are ordinary repository commits on the unpushed review branch; every finished
plan and review remains unchanged, and no outward-facing act, destructive local act, external
configuration write or receipt rewrite occurred.

## Finding 20.6: backslash paths require no receipt rewrite

Recorded by Codex on 2026-09-12. Finding 20.6 is disposed of as an evidence-only census; no
remediation is authorized or required.

A fresh census read NUL-delimited `git ls-files -z` output, split filenames only on NUL, decoded
each filename as UTF-8 and parsed every tracked direct `in/*.json` file from an explicit UTF-8
read. The census reproduces the finding's exact population: 45 JSON string values, each on a
distinct source line, contain a Windows absolute backslash path such as `C:\...`. A captured log
value containing more than one such path counts once, matching the review's string-line census.
The ten files and their counts are:

1. `in/mam_osis_empty_verification.json`: 2.
2. `in/mam_osis_remove_verification.json`: 9.
3. `in/mam_osis_repoint_verification.json`: 8.
4. `in/mam_osis_stubs_verification.json`: 4.
5. `in/mam_products_phase6a_verification.json`: 2.
6. `in/mam_products_phase6b_verification.json`: 5.
7. `in/mam_products_phase6c_verification.json`: 3.
8. `in/mam_products_phase6d_verification.json`: 2.
9. `in/mam_products_phase6e_verification.json`: 9.
10. `in/mam_products_phase6f_verification.json`: 1.

All 45 values are immutable evidence-receipt data: 39 are structured path or command values and
six are captured `log_text` values. None is reader-facing prose. The same NUL-safe tracked-file
scan found no Python reference to any of the ten receipt filenames, and the tracked Python tree
has no shared consumer for the two filename families. References outside the ten receipts are
finished plan and review records, evidence inventories, and a validation record; no live code
consumes the recorded path values. Converting their separators would rewrite the receipts rather
than correct live input.

`git diff --check` and the tracked-prose mark-order lint passed. The full suite passed 997 tests,
with 5 skipped and 65 subtests passed. This documentation-only disposition does not owe a mega
run.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository commit on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 20.8: immutable commit messages require no history rewrite

Recorded by Codex on 2026-09-12. Finding 20.8 is disposed of as an immutable-history census; no
remediation is authorized or required.

A fresh check of the cited commits and their Git trees reproduces the four observations:

1. Commit `5e7f0d6b` says that `CLAUDE.md` “holds Hebrew on 126 lines.” The committed
   `5e7f0d6b:CLAUDE.md` blob has 16 lines containing a Hebrew-block codepoint.
2. Commit `74d883d2` says that its twelve configuration files have “13 Hebrew clusters, 0 in
   Unicode-normal order.” The twelve committed files have 13 Hebrew letter clusters with at
   least one combining mark and zero clusters with two or more combining marks. None of the 13
   clusters can distinguish Unicode-normal order from MAM-normal order. Section 3 of the
   finished `doc/assessment-two-stranded-artifacts-2026-09-09.md` correctly says that the files
   are in the prose lint’s scope and are not offenders, but its clean result supplies no
   discriminating mark-order evidence for those files.
3. Commit `5a07e5af` reports 983 passed tests, while commit `7af937fa` reports 984 and calls 983
   “one low.” The commits are on different lines after merge base `63ac5b84`: `5a07e5af` is one
   commit from the merge base, and `7af937fa` is eight commits from the merge base. The parent of
   `7af937fa`, `c65e103d`, contains the newly added
   `test_hand_authored_prose_is_in_mam_mark_order` test. The finished assessment already states
   the historical relationship accurately: 983 passed at `a50da28b`, and 984 were expected on
   the merged tree because the prose lint added one test.
4. Commit `209b4c05` changes 24 rows of `out/vendoring_compare_out.txt` from `eol-only` to
   `identical` and merges the corresponding eight rows of `doc/vendoring-inventory.md` into four,
   while its message names only the Wikisource refresh and pipeline regeneration. Its immediate
   history contains the completed efficiency programme at `b2052ab9`; that programme’s finished
   plan explicitly says that the same generated report changes were preserved in scratch and
   restored rather than included in the programme commits. The live vendoring inventory now
   reports its current three-file population accurately as two `identical` rows.

The four inaccurate or incomplete statements are commit-message history. The assessment and the
efficiency plan are finished dated reports and remain unchanged under D12. The live `CLAUDE.md`,
the prose mark-order lint and the generated vendoring reports require no correction. Rewriting the
commit messages would require a history rewrite, which is neither authorized nor warranted.

`git diff --check` and the tracked-prose mark-order lint passed. The full suite passed 997 tests,
with 5 skipped and 65 subtests passed, in 111.21 seconds. This documentation-only disposition
does not owe a mega run.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository commit on the unpushed review branch; no history
rewrite, outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 20.1: term-of-art uses remain and the Ben attribution is explicit

Recorded by Codex on 2026-09-12. Finding 20.1 is complete.

Ben's 2026-09-04 commit `b4706759` says that `script-regenerable` supersedes an authorship claim
when a script reproduces an artifact, while `Ben-written` and `Claude-written` remain useful for
artifacts that no script reproduces. The same message expressly says that this refinement is not a
rename: “hand-authored” remains an unambiguous lint-scope term meaning “not emitted by a script,”
and no repository-wide sweep is proposed. The review's phrase “against the 2026-09-04 vocabulary”
therefore does not supply a mechanical replacement rule.

A fresh live-tree census gives these dispositions:

1. Commit `3134f32b` already corrected the three source descriptions cited in the finding.
   `py/main_pipeline_graph.py` now calls `MAM-process.dot` Ben-written, and
   `py/main_0_mega.py` describes the structured specification without an authorship claim and
   calls `MAM-process.dot` Ben-written. The three cited spellings are absent from both modules.
2. The finding's two `CLAUDE.md` anchors now occur at lines 24 and 49. Both use “hand-authored” as
   the mark-order lint's term of art. The live instruction file has two additional occurrences of
   the same term at lines 69 and 166; both make the same generated-or-captured distinction. All
   four remain. The historical “hand-maintained” test-registry description at line 992 states the
   maintenance method rather than an unknown authorship and also remains.
3. `py/tests/test_prose_mark_order.py` still has exactly five occurrences of “hand-authored,” at
   lines 1, 6, 41, 45 and 176. Line 1 names the lint's scope; line 6 quotes the instruction that
   motivated the lint; line 41 distinguishes captured note HTML from prose; line 45 distinguishes
   external input from prose; and line 176 states the lint failure. All five retain the term of
   art. The adjacent line 56 called the edition-transcription headers “hand-written” and
   immediately identified their contents as Ben's notes. Commit `c8ba9f00` changes that live
   docstring to “Ben-written.”
4. The finished `doc/PLAN-wikisource-derived-mam-products.md` and frozen
   `doc/mam-products-phase6-command-map.md` each have one “hand-authored” occurrence, both
   distinguishing source from generated output. The finished
   `doc/assessment-two-stranded-artifacts-2026-09-09.md` has ten literal “hand-authored”
   occurrences and one “hand-written” occurrence, rather than a literal population of nine. The
   occurrences at lines 66, 68 and 175 quote earlier instruction text. Lines 89, 93, 117, 176,
   233, 234 and 553 use the generated-or-captured classification. The “hand-written” occurrence
   at line 116 describes Ben's notes in a header that is never regenerated, so
   `doc/assessment-two-stranded-artifacts-2026-09-09-update.md` records that the phrase should be
   read as “Ben-written header.” D12 leaves all three finished documents unchanged.

Black left the edited Python file unchanged. `git diff --check` and the tracked-prose mark-order
lint passed; the lint passed 1 test. The full suite passed 997 tests, with 5 skipped, in 114.05
seconds. The source change is a docstring correction and reaches no generator or generated
product, so this unit does not owe a mega run.

Product axis: the correction changes a code docstring and documentation only; it reaches no
generator or product. Act axis: the commits are ordinary repository commits on the unpushed
review branch; all finished dated documents remain unchanged, and no outward-facing act,
destructive local act, external configuration write or receipt rewrite occurred.

## Finding 20.11: inline-code link examples require no remediation

Recorded by Codex on 2026-09-12. Finding 20.11 is complete as an evidence-only disposition.

A fresh live-tree inspection gives these dispositions:

1. The tracked canonical `dot-claude/user-wide-CLAUDE.md` has the cited text at line 1416, and
   the live `C:/Users/BenDe/.claude/CLAUDE.md` has the same text at line 1416. The two files are
   byte-identical at SHA-256
   `F32191A794596500297D4B566DAE98BEDCB126D00821B2BDCD880FFB438D0D18`.
2. The tracked canonical `dot-Codex/user-wide-AGENTS.md` has the cited text at line 1197, and
   the live `C:/Users/BenDe/.Codex/AGENTS.md` has the same text at line 1197. The two files are
   byte-identical at SHA-256
   `577320F67CB32E2910D1DA269899814B5E44771D2D78E4E46D43321BAA3AECFC`.

Both occurrences of `[page](gh-pages/accgram/page.html)` are enclosed by backticks, so CommonMark
parses each occurrence as an inline-code example rather than as a link. The surrounding sentence
explicitly calls the repo-relative spelling “the wrong thing here.” The nonexistent target is
therefore part of the negative example. Replacing the target with an existing page would make the
example contradict the instruction it illustrates.

The positive `file:///C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/wlc/accgram/maqaf-nonfinal-accents.html`
example occurs in a fenced code block in each instruction file, and the named file exists in both
the primary clone and the review worktree. No tracked Markdown-link checker exists in the live
tree; the review-only `md_links_check.py` named by the finding treated inline code as links. No
checker weakening, exclusion or mechanical gate is warranted.

The same review census separately identifies
`misc/what-is-mam/img/provenance-misc.md:6` as a dead link. That occurrence is an ordinary
reader-facing Markdown link, its target
`.github/prompts/capture-what-is-mam-slides.prompt.md` is absent, and commit `84a801f4` deleted the
target. The dead provenance link is pre-existing and is not one of finding 20.11's two instruction
examples, so this narrow unit leaves the dead provenance link unchanged.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 113.28 seconds. No Python file
changed, and this documentation-only disposition does not owe a mega run.

Product axis: this disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; the tracked
canonical instruction files, the live user-level copies, every finished dated document and the
dead provenance link remain unchanged. No outward-facing act, destructive local act, external
configuration write or receipt rewrite occurred.

## Finding 11.5: `ḥataf` in prose and `xataf` in ASCII-oriented contexts

Recorded by Codex on 2026-09-12; Ben's decision recorded on 2026-09-13. Finding 11.5 is complete.

At checkpoint `974395f9f2fabf69eee147c1764886a7c8e28ec0`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, a fresh census used
NUL-delimited `git ls-files -z` for the tracked-Markdown population. Each table entry gives
literal sites followed by lines containing a site:

| Finished report | `xataf` | `hataf` | `ḥataf` |
|---|---:|---:|---:|
| `doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md` | 7 / 4 | 0 / 0 | 0 / 0 |
| `doc/meteg-after-silluq-search-in-mam-documentation.md` | 6 / 5 | 3 / 3 | 0 / 0 |
| `doc/meteg-after-silluq-koren-lookup-candidates.md` | 1 / 1 | 10 / 5 | 0 / 0 |
| `doc/meteg-after-silluq-in-uxlc-and-wlc.md` | 0 / 0 | 2 / 2 | 0 / 0 |
| `doc/meteg-after-silluq-job-4-12.md` | 0 / 0 | 3 / 3 | 0 / 0 |
| `doc/meteg-after-silluq-psalms-72-15.md` | 0 / 0 | 6 / 2 | 0 / 0 |

The six reports therefore have 24 plain-`hataf` sites on 15 lines. They also have 14 `xataf`
sites on 10 lines: 13 sites on 9 lines are prose in the screen and search reports, while the
remaining site is the identifier path `py/explicit_xataf/extract.py` in the Koren-candidates
report. None of the six reports has `ḥataf`.

Outside the six reports and the remediation records that merely discuss finding 11.5, the
`ḥataf` population remains seven sites on six lines:

1. `doc/mega-pipeline-review-findings-public-2026-09-01.md:126, :128, :130` has three
   `explicit-ḥataf` sites.
2. `doc/mega-pipeline-review-phase-13-2026-09-01.md:148` has one `explicit-ḥataf` site.
3. `doc/metsudah-vs-ctr.md:237` has one `ḥataf qamats` site.
4. `misc/mam-is-a-dataset/script.md:19` has `ḥataf` and `ḥataf pataḥ` on the same line.

At checkpoint `974395f9f2fabf69eee147c1764886a7c8e28ec0`, five further `ḥataf` sites merely discussed
the then-unresolved choice:
`doc/review-findings-2026-09-10.md:626`,
`doc/meteg-after-silluq-search-in-mam-documentation-update.md:93`, and
`doc/review-findings-2026-09-10-update.md:55, :163, :185`. The pre-entry tracked-Markdown total at
the checkpoint was consequently 12 literal sites on 11 lines; only the seven sites on six lines
listed above use `ḥataf` as the prose term rather than as the subject of this review.

The authority check does not select between the two prose alternatives:

1. Commit `9e3aed3424b2cbe00cb2334360125f4ae0243666` of 2026-03-25 is the only matching commit
   message that explicitly maps `hataf` to `ḥataf` in prose and `xataf` in identifiers. The
   commit has a Claude coauthor trailer and does not attribute that editorial choice to Ben.
   Later report commits introduced the plain spelling without declaring a reversal. The
   historical commit is evidence for `ḥataf`, not an explicit Ben decision.
2. The current `py/tests/test_transliterations.py` docstring describes het-as-plain-`h` forms as
   retired, but the live denylist has no `hataf` pattern and scans Python rather than Markdown.
   The current user-level Claude and Codex instructions, `CLAUDE.md`,
   `doc/dual-agent-review.md`, and the live `hebrew-prose` skill have no `hataf`, `ḥataf` or
   `xataf` occurrence that selects the prose spelling.
3. `py/accgram/printed_decalogue_strands.py` single-sources its rendered names and has
   `ROM_PATAX = "pataḥ"`, but it has no `ROM_HATAF`. Its `SCOPE` paragraph makes the `ROM_*`
   convention specific to the printed-Decalogue pages. Extending either the dotted consonant or
   the single-sourcing table to `hataf` would be a new editorial choice.

Ben's decision, 2026-09-13, makes the choice contextual:

1. The plain-`h` spelling `hataf` is never used.
2. `ḥataf` is the spelling in narrative Unicode prose. This includes narrative text in Markdown
   documents under `doc/` and reader-facing prose under `gh-pages/`, whether the rendered prose
   is authored directly or generated by Python. The six files inventoried above are Markdown
   documents under `doc/`, not HTML documents under `gh-pages/`. They already contain Hebrew and
   the Unicode romanizations `pataḥ` and `deḥi`, so their narrative text has no ASCII advantage
   that would justify `xataf`.
3. `xataf` remains the spelling in ASCII-oriented contexts, including file and directory names,
   paths and code identifiers. A quoted filename, path or identifier keeps `xataf` when it appears
   inside narrative prose. The path `py/explicit_xataf/extract.py` therefore remains as written.

D12 leaves all six finished Markdown documents unchanged. The next remediation task can give the
document-by-document corrected readings in sibling update files; this task records the decision
only.

### Document-by-document correction follow-through

Recorded by Codex on 2026-09-13. The document-by-document correction follow-through is complete.
Five existing sibling update files now give precise corrected readings, and
`doc/meteg-after-silluq-in-uxlc-and-wlc-update.md` supplies the previously missing sixth sibling.
The six finished reports remain byte-identical to the Git blobs recorded in those sibling update
entries.

The fresh source-report census confirmed 24 plain-`hataf` sites on 15 lines, 14 `xataf` sites on
10 lines and no `ḥataf`. The sibling updates correct all 24 plain-`hataf` sites and the 13
narrative `xataf` sites to `ḥataf`. The identifier path `py/explicit_xataf/extract.py` remains
`xataf`. The same entries complete finding 11.5's already-settled romanizations by correcting
every narrative `patax` or `patah` site to `pataḥ` and every narrative `dexi` site to `deḥi`.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: the sibling update files preserve all six finished reports rather than rewriting any
receipt; no outward-facing act, destructive local act or external configuration write occurred.

`git diff --check` and the tracked-prose mark-order lint passed. The full suite passed 997 tests,
with 5 skipped and 65 subtests passed. This documentation-only disposition reaches no generator
or product and does not owe a mega run.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; all six
finished reports remain unchanged, and no outward-facing act, destructive local act, external
configuration write or receipt rewrite occurred.

## Finding 20.9: crop-coordinate filename policy still needs Ben's decision

Recorded by Codex on 2026-09-12. Finding 20.9 is re-established and remains decision-pending; no
image has been adjudicated, no coordinate has been newly confirmed, no crop has been renamed and
the live naming rule has not been tightened.

At checkpoint `bea962688e6153bac935995d4fd0e490916bd640`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, the live evidence is:

1. `leningrad/page-snips/README.md` still permits the
   `<folio><side>-col<N>-line<N>-<ref>-<slug>.png` form “when the line has been read off the image”
   and uses the coordinate-free form when the line has not been read. The rule conditions the
   coordinate-bearing name on the line; the rule does not say that every encoded coordinate must
   have been independently confirmed.
2. The tracked Psalms crop remains
   `leningrad/page-snips/380A-col2-line3-Ps72v15-yevarkhenhu.png`. Its README entry says that Ben
   read line 3 from the image and that column 2 is the estimator's, not an independently confirmed
   column. Commit `b97a2100af5d63671203dcf0d110eb741b2f0375`, which introduced the crop, states
   both facts and calls the same arrangement the Lamentations 2:3 precedent.
3. The tracked Lamentations crop remains
   `leningrad/page-snips/430B-col2-line10-Lam2v3-akhla.png`. Its README entry says that Ben read
   line 10 from the image and that column 2 is still the estimator's. A rule requiring independent
   confirmation of every coordinate would therefore affect the Lamentations crop as well as the
   Psalms crop.
4. Commit `9eff3d0044ad097d2c050bd1a4d9f9e75bc46ae0` is still the latest commit that changed
   `leningrad/page-snips/README.md`. Its subject says “a name has a line only if read,” and it
   removed the coordinates from the Job 4:12 crop because neither the column nor the line had been
   read from the image. It did not remove either crop whose line had been read.
5. A search of the post-`9eff3d00` repository history and the current repository, Codex and Claude
   instruction files found no later explicit Ben decision requiring independent confirmation of
   every coordinate. The later matching entries are the dual-agent review records themselves:
   C4 and turn 3 both call the stronger rule Ben's choice, and the reconciliation table calls the
   stronger rule undecided.

Ben still needs to choose between two policies:

1. **Keep the live rule.** Reading the line authorizes the coordinate-bearing filename. An
   estimator-supplied column may remain in the filename when the README discloses that the column
   is unconfirmed. Both current coordinate-bearing filenames comply and require no remediation.
2. **Require independent confirmation of every encoded coordinate.** An estimator-supplied column
   may not remain in a filename merely because the line was read. The Psalms and Lamentations
   crops would then need a later, explicit disposition: independently confirm each column or adopt
   and apply a filename form that does not assert the unconfirmed column.

Until Ben selects a policy, the live README, the three crop filenames and all finished dated
documents remain unchanged. This documentation-only disposition reaches no generator or product
and does not owe a mega run.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 20.9 decision: keep the live crop-coordinate filename rule

Recorded by Codex on 2026-09-13. Ben's decision, 2026-09-13: “Keep the current rule.”

The live rule in `leningrad/page-snips/README.md` therefore remains unchanged. Reading a line from
an image authorizes the coordinate-bearing filename, and an estimator-supplied column may remain
in that filename when the README discloses that the column is not independently confirmed. The
existing Psalms 72:15 and Lamentations 2:3 filenames comply with the selected rule, so neither crop
is renamed. No image has been adjudicated and no coordinate has been newly confirmed.

Finding 20.9 is complete. This documentation-only disposition reaches no generator or product and
does not owe a mega run.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 12 and C1: unique letters-only UXLC matching is implemented

Recorded by Codex on 2026-09-13; Ben's decision recorded and implemented on 2026-09-13. Finding
12/C1 is complete. This entry supersedes finding 12's 2026-09-12 disposition, which says “Has
been fixed by `80f88f7c`,” without changing that historical disposition or any other finished
review record under D12.

At pre-change checkpoint `09072b5029ba0f402d991ef317966e4d41ee576d`, after current `main` at
`1d2ddc3dc8d029af06bf5cb6ac7a9696f2f78caa` was confirmed already merged, the evidence was:

1. The canonical verse-links skill's “Running the command” items 2 and 3 said that a bare
   consonantal form fails for a verse-final or maqaf-final atom, and that a query matching none or
   more than one of the verse's atoms lists the atoms and exits 1. The same incomplete account was
   in `py/main_verse_links.py` and `py/uxlc_misc/my_uxlc_find_atom.py`; the last file also said
   that ambiguity raises rather than silently selecting one position.
2. The implementation in `my_uxlc_find_atom.py` removed only Unicode categories Mn and Cf.
   Punctuation therefore remained in each stripped candidate. The ambiguity check counted only
   candidates equal after that punctuation-sensitive stripping; an occurrence excluded because
   it ended in a sof pasuq or maqaf was absent from the candidate count.
3. A fresh public-input run used `my_uxlc.read_all_books()` and `find_atom` from that tree.
   For every UXLC atom ending in U+05BE or U+05C3, it retained only U+05D0 through U+05EA for the
   query and compared the returned atom number with the enumerated reference atom. The command was
   `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe
   .novc/finding12_c1_live_verify.py`; the complete anchor-era reproducer remains in
   `doc/codex-review-findings-2026-09-10.md` under “C1's complete reproducer follows.” The
   65,713-occurrence result was:

   | Result | Occurrences |
   |---|---:|
   | `AtomNotFound` | 61,711 |
   | ambiguity `ValueError` | 412 |
   | returned a different atom | 3,590 |
   | returned the reference atom | 0 |

4. Genesis 1:3 was the complete successful-different-position example. The UXLC's atom 4 is
   `א֑וֹר`, and atom 6 is `אֽוֹר׃`. Querying the exact atom-6 form returns
   `(6, "exact", "אֽוֹר׃")`; querying the bare consonants from atom 6 returns
   `(4, "stripped", "א֑וֹר")`. `main_verse_links.py` says that the match used letters alone and
   prints the UXLC form, but exits 0 and does not say that another occurrence with the same letters
   exists.

The documentation correction and the semantic matching policy were separate. The four policies
below were presented before the implementation changed or the documentation promised one of them.

The four viable policies had distinct user-visible consequences:

1. **Option 1 — require an exact UXLC atom form or `--atom`.** Remove the stripped fallback from
   the UXLC lookup. Bare mid-verse lookup convenience ends, and a MAM form differing from the UXLC
   in marks may not resolve. For the measured 65,713 punctuated reference atoms, the bare query is
   never the reference atom's exact form, so the user must supply the UXLC form or atom number.
2. **Option 2 — normalize punctuation for the fallback and reject repeated occurrences.** Match a
   pointed or punctuated form exactly first. For a bare consonantal form, compare the Hebrew
   letters of every atom in the verse, return only a unique candidate and list all candidates
   otherwise. On the measured population, 52,881 occurrences have a unique letters-only candidate
   and would return the reference atom; 12,832 have repeated letters and would require `--atom`.
   Genesis 1:3 would list atoms 4 and 6 instead of selecting atom 4.
3. **Option 3 — retain punctuation-sensitive matching and add a letters-only safety check.** Keep
   the current not-found behavior, but before returning a stripped match, raise ambiguity when a
   punctuation-normalized comparison finds another occurrence. On the measured population, the
   3,590 different-atom returns become errors: 61,711 remain not found and 4,002 are ambiguous.
   This option prevents the successful-different-position result but does not make a unique bare
   verse-final or maqaf-final atom resolvable.
4. **Option 4 — retain matching and correct only the documentation.** This option preserves every
   current success and failure, including the 3,590 measured successful returns at a different
   atom. The command continues to print the returned UXLC form without stating that the verse has
   another occurrence with the same letters.

Ben concurred with Codex's recommendation on 2026-09-13: implement option 2 for the UXLC matcher
only. A bare consonantal query means “find this atom if these letters occur exactly once in the
UXLC verse”; repeated occurrences raise and require `--atom`. The Aleppo Codex and Cambridge Add.
1753 linebreak locators are unchanged, and the UXLC matcher's docstring no longer claims that the
three policies are kept in sync.

The implementation keeps the exact pass for pointed or punctuated input. One exact candidate
returns; two or more byte-identical candidates raise. A bare consonantal query always proceeds to
the letters-only pass even when it is byte-identical to one unpointed UXLC atom, so another pointed
or unpointed atom with the same letters makes the query ambiguous. The letters-only pass retains
only U+05D0 through U+05EA and returns only one candidate. `py/main_verse_links.py`,
`py/main_uxlc_estimate_atom_loc.py` and the verse-links skill now state that contract.

The post-change public-input differential check establishes both kinds of ambiguity:

1. For the same 65,713 punctuated reference-atom occurrences, 52,881 bare queries return the
   reference atom and 12,832 raise ambiguity. None returns a different atom and none raises
   `AtomNotFound`.
2. Across every verse in the UXLC, 268,532 distinct letters-only query groups are unique and
   17,179 are ambiguous; every unique group returns its only atom and every ambiguous group
   raises.
3. The UXLC has 5,337 within-verse groups, comprising 11,505 occurrences, in which the exact
   pointed atom form occurs more than once. Every exact query for those forms raises rather than
   selecting the first occurrence.
4. At Genesis 1:3, exact `אֽוֹר׃` still returns atom 6. Bare `אור` now raises with atoms 4 and 6;
   `py/main_verse_links.py` lists both and exits 1.

The shared skill was changed live-first. Its complete live Claude directory was copied to the
canonical `dot-claude/skills/verse-links/` directory and the live Codex directory, and both
recursive `git diff --no-index --exit-code` comparisons passed. Black left all three changed
Python files clean. The approved-policy differential check passed. The full suite passed 997
tests with 5 skipped in 110.65 seconds. After this live-update edit, `git diff --check` and the
tracked-prose mark-order lint passed.

Product axis: these executable-source and help-text changes affect the two interactive UXLC
location commands but reach no generator or tracked product, so no intermediate mega run was
owed. Act axis: replacing the two live shared-skill directories was an explicitly authorized
external configuration write, mirrored immediately into the tracked canonical directory; all
finished records remain unchanged, and no outward-facing act, destructive unrelated act or
receipt rewrite occurred.

## Finding 21: the eight process-and-hygiene items are disposed or decision-pending

Recorded by Codex on 2026-09-13. This entry re-establishes finding 21 against the live tree after
current `main` at `7b64043ba6c3bf4ffafdc0c3ed8169a2989bd530` was merged into the review branch,
producing checkpoint `52e0c2db9b71e5bcd175c5f059acc695800ccc33`. Historical censuses remain tied to
their original range; current filesystem and remote checks are dated below.

1. **Item 21.1 is completed housekeeping.** The re-leased
   `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c` no longer
   exists and is absent from `git worktree list`. None of the three historical branch names
   `claude/eloquent-ritchie-0e4c6c`, `claude/interesting-taussig-6aa52b` and
   `claude/mam-basics-review-stage-1-72e903` exists locally. No current work remains for this
   item, and no worktree or branch was removed by this remediation.

2. **Item 21.2 is completed housekeeping with a now-recorded execution gap.** Commit
   `e7a1736bcd9e02f3e2ed3f478a6bd33032731f4d` records that its maintenance sweep removed the
   September 8 Codex review worktree named through `--session-ended`. The path remains absent
   from disk and `git worktree list`, and local branch `codex-review-2026-09-08` remains absent.
   The surviving evidence does not prove which command removed the branch. D12 leaves the
   finished `doc/PLAN-close-out-review-2026-09-08.md` unchanged; its live sibling
   `doc/PLAN-close-out-review-2026-09-08-update.md` now records that Step 7 is complete and
   preserves the evidentiary limit.

3. **Item 21.3 is a confirmed historical census, not a process defect.** Git history still
   gives 31 merge commits in `38a606e2..0354b6cc`, including 13 merges of `main` into
   `codex-review-2026-09-08`; seven merge commits have paths in their combined diff. The
   user-level instruction gives the ordinary integration schedule. The review-specific plan and
   the live D11 procedure explicitly require each close-out task to merge current `main` into the
   review branch before editing. The specific review procedure explains the measured cadence, so
   no generic instruction change or merge-history rewrite follows.

4. **Item 21.4 remains a Git census and creates no issue-attribution exception; one historical
   trailer count is corrected here.** Through anchor `0354b6cc`, Git has 12 commits whose author
   is `Claude <noreply@anthropic.com>`. Eleven have a `Claude-Session:` trailer. Merge commit
   `1af10e4cb275d59ec2effa85ab005af33ef3d9d5` is the twelfth and has no such trailer. A live
   `git ls-remote` check still finds remote branch `claude/charming-mayer-xknwcw` at
   `036deb92fa42f7b6b707dbbcd04f9560fb709b84`. C5 remains controlling: Git author and trailer
   metadata describe commits and cannot identify the actor behind a GitHub issue event. An
   agent-written explanatory comment remains required for an issue state change. The remote
   branch is a census fact, not an instruction to delete it.

5. **Item 21.5 has no residual drift.** The live `C:/Users/BenDe/.Codex/AGENTS.md` and tracked
   `dot-Codex/user-wide-AGENTS.md` have the same SHA-256 hash,
   `577320F67CB32E2910D1DA269899814B5E44771D2D78E4E46D43321BAA3AECFC`. The tracked text now
   explicitly says to edit the live file first, copy it back and commit. The two historical
   tracked-first edits caused no current mismatch; no live user-level file was written here.
   Inherited item 3's four broader sync-discipline choices remain separate and decision-pending.

6. **Item 21.6 is complete under Ben's decision for issues #266 and #267.** Ben decided on
   2026-09-13 to close both issues when the requested Wikisource corrections had reached the MAM
   source and MAM-parsed products, without making downstream phonetic-hbo regeneration a
   completion criterion. Ben described the choice between the two recorded alternatives as a
   tough judgment call, so this disposition establishes no repository-wide issue-completion rule.

   A pre-action read-only GitHub check found both issues open, each still with only skadish1's
   2026-09-09 “Fixed” comment and Wikisource diff link. Commit `209b4c05` remained the last commit
   to each of `in/mam-ws/D1-Psalms.json`, `MAM-parsed/plus/D1-Psalms.json` and
   `MAM-parsed/plain/D1-Psalms.json`; all three have both corrections. The live phonetic-hbo
   `main` remained at `10de797098dab454b5b92e1d4f479fba68f6674b`, and the relevant generated
   Psalms pages had not received the corrections. That separate downstream state did not block
   the completion criterion Ben selected for these two issues.

   Codex then posted an agent-written comment stating the reason and the selected completion
   criterion on [#266](https://github.com/bdenckla/MAM-basics/issues/266#issuecomment-5654334247)
   and [#267](https://github.com/bdenckla/MAM-basics/issues/267#issuecomment-5654335637), immediately
   before closing each issue. A final read-only check found #266 closed at 15:53:01Z and #267
   closed at 15:53:16Z on 2026-09-13. No label or assignment changed.

7. **Item 21.7 is fixed in the live instruction-file remediation plan.** Commit `516a4a1a`
   remains in the live tree, and repository `CLAUDE.md` states that a normal linked worktree needs
   no `REPOS_ROOT`; the variable is only an override for a nonstandard sibling layout. The two
   stale mandatory-export directions in
   `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md` now name the primary
   clone's venv and state that normal worktree runs need no `REPOS_ROOT`. The plan's suite check
   remains: the plan changes only instruction files, and repository `CLAUDE.md` exempts an
   instruction-only branch from the mega. The live D11 procedure in `doc/dual-agent-review.md`
   now states the current final-integration command: run `py/main_0_mega.py` from the merged
   review branch, read its Git diff, and commit every explained generated change before the
   fast-forward, with no `REPOS_ROOT`.

8. **Item 21.8 contains completed housekeeping, one continuing maintenance referral, historical
   counts and one corrected worktree interpretation.** A live remote check confirms that
   `origin/post-stress-meteg` is absent; the post-stress-meteg worktree and empty `d4d1` directory
   remain absent. The primary clone's `.pytest_cache` still exists and remains referred to
   repository maintenance; this review did not remove it. The historical five-entry count under
   `C:/Users/BenDe/.codex/plans` remains a dated census; the directory has seven top-level entries
   on 2026-09-13, whose contents were not read. `C:/Users/BenDe/GitRepos` still contains exactly
   the five directories named by `all-repos.code-workspace`, with no extra directory.

   The historical concern about `C:/Users/BenDe/.codex/worktrees/0e63` is withdrawn. A
   MAM-basics-specific `git worktree list` cannot name worktrees belonging to sibling
   repositories. MAM-private's worktree list names `0e63/MAM-private` on branch
   `codex-worktree-0e63`, and phonetic-hbo's worktree list names `0e63/phonetic-hbo` on the branch
   of the same name. The two registered worktrees are not unexplained residue. The current
   top-level `.codex/worktrees` census belongs to later task state and is not substituted for the
   September 10 census. No directory was deleted or otherwise changed.

These documentation corrections reach no generator or product and do not owe a mega run.

Product axis: the changes affect current review and process documentation only. Act axis: the
repository writes are ordinary changes on the unpushed review branch. The explanatory comments
and state changes on issues #266 and #267 are outward-facing acts explicitly authorized by Ben's
2026-09-13 decision. No destructive local act, external configuration write or finished-record
rewrite occurred.

## Finding 7.1, September 8 remediation plan: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-13. This entry classifies only the 33 live lines containing `.novc`
in `doc/PLAN-remediate-review-findings-2026-09-08.md`. It does not establish a rule for the rest
of finding 7's census.

At checkpoint `0a86cddefe2d1ed5151b91476ffadf08f3233fd1`, current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was already merged. The finished plan remains
unchanged at Git blob `bbd8c142bee6c1f1424cc33d08fa81bf37c7e1c3`, the same blob as final remediation
commit `9d1de07404bd9257c3e4cafc0acc1c46b87264c9`. Its existing sibling update remains unchanged
at Git blob `37f48fbc1feadcf374cddf6ee6e9d72617fbc543`; the update records the later retirement of
the Wave 3 display fallback and supplies no scratch artifact.

The plan's named worktree, `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, no
longer exists. Neither the review worktree nor the primary clone has the dated
`.novc/review-remediation-2026-09-08/` directory. The tracked `.gitignore` ignores `.novc/`.
The completed remediation deliberately preserved that directory outside the retired worktree:
`C:/Users/BenDe/.codex/visualizations/2026/09/10/01a08b71-0f3a-7ca2-b088-8dc432526ba8/review-remediation-2026-09-08-evidence.zip`
is 91,973,867 bytes, and its SHA-256 is
`33495ad7b7d0b040719ded27ff5544a75efb2f19c0c971c4d333a790dbb523ce`. The adjacent verified
manifest has that same size and hash, inventories 6,208 source files, and identifies final commit
and verified remote `main` as `9d1de07404bd9257c3e4cafc0acc1c46b87264c9`.

The 33 lines have these classifications:

| Searchable anchor in the finished plan | Lines in the live tree | Classification |
|---|---:|---|
| “V6 was implemented” and the later V6 script commands | 667, 699, 953, 1898 and 2047 | Historical execution-time dependency, command record and reproducible method. The original V6 gate was mandatory while the remediation was active. The verified archive preserves the exact script, its fixed Git baseline and its deliberate failure proofs. The plan also specifies reconstruction from the nine fixed `c2f238f2` HTML blobs and survey JSON. The completed remediation has no current operation that reads the gate. |
| V6 run directories and remediation scratch-root references | 681, 761, 853, 961, 1071, 1182, 1289, 1498 and 2051 | Historical output inventory. The verified archive has 1,375 files under `v6-runs/`, including the labelled failure probes and the passing wave checkpoints. The plan records each result and the fixed baseline hashes; no current generator or check reads a dated run directory. |
| “were backed up under” for the D2 skill deployment | 704 | Disposable backup and historical deployment evidence. The verified archive has 18 files under `d2-wave1-01a0891a/`, including the before/after inventories and all three skill-home copies. The current tracked skill and live deployment procedure, rather than the backup, govern a new change. |
| Wave 1A suite log and verifier | 723 | Historical command and output record. The archive preserves `wave1a-01a0891a-suite.log` and `verify_wave1a_01a0891a.py`; the plan records the command and result. The current tracked `py/main_test.py` is the entry point for a new suite run. |
| Wave 1B, Wave 1C1 and Wave 1C2 measurement commands | 770, 865, 877 and 969 | Historical measurement commands, reproducible methods and outputs. The archive preserves all four exact scripts and their reports. The plan states the populations, commits, inputs and results, while Git history preserves the cited branches, records and product trees. No current operation imports any of the measurement scripts. |
| Wave 2 verifier, baseline and Holman-label approval receipt | 1502, 1505, 1636 and 1647 | Historical differential harness, immutable before-edit output and decision receipt. The archive preserves the verifier, all 930 baseline files and the exact approval JSON. The tracked Wave 2 implementation, generated products and execution record preserve the accepted result; a new product check uses the current tracked generators and tests. |
| Wave 3 preparation and technical evidence directories | 1785 and 1971 | Historical source-trace, fault-injection, differential and output inventory. The archive preserves 27 preparation files and 2,189 technical-evidence files. The finished plan records the covered domains and results, current source and annotation validation remain tracked, and the sibling update identifies the display fallback that was retired later. |
| Editorial contract, expected pages and editorial-gate command | 2203, 2222 and 2256 | Historical execution-time dependency, approved output contract and reproducible method. The editorial gate was mandatory through Wave 4. The archive preserves the exact gate, contract, nine expected pages, twelve proposed-diff files and complete run evidence. Git history preserves the original baseline, approved source change and resulting pages. No current operation reads the completed-remediation contract. |
| Wave 4 editorial-gate runs and Wave 4 evidence | 2435 and 2441 | Historical output inventory and final-verification record. The archive preserves 303 editorial-gate run files and all 33 Wave 4 files, including the final integration receipt. The manifest verifies the archived files and the plan records the successful audit, suite, fast-forward, push and remote-head check. |
| “Use uniquely named real scripts” | 2568 | Reproducible current method and disposable output destination. The sentence prescribes how a future bounded check is written; it does not require an old script. |
| V6 baseline recipe | 2670 | Reproducible historical gate specification and disposable destination. The exact `mas-html-baseline/` is preserved in the verified archive, and every baseline byte is independently recoverable from the fixed Git commit the recipe names. The retired worktree path is not an input to a current check. |

The V6 gate and editorial gate were indispensable dependencies of the active remediation, and the
verified archive preserves both. No `.novc` artifact named or described by the 33 lines is an
indispensable missing dependency of a tracked result or current method. No further Ben decision
arises from this document-by-document unit. D12 leaves the finished plan and its existing sibling
update unchanged. Finding 7.2's first-match predicates remain decision-pending and are outside this
unit.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 79.21 seconds.

Product axis: this classification changes only the review's live sibling update and reaches no
generated MAM product. Act axis: the write is an ordinary repository change on the unpushed review
branch; no outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 7.1, Wikisource-derived MAM products plan: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-13. This entry classifies only the 43 live lines containing `.novc`
in `doc/PLAN-wikisource-derived-mam-products.md`. It does not establish a rule for the rest of
finding 7's census.

At checkpoint `cbe8b5a2a618c38a7b4fbe650013c0e6930cbd34`, current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was already merged. The finished plan remains
unchanged at Git blob `bc60b785903b1099a9bcbd9a6b9eb55bcd3103e6`. Its existing sibling update remains
unchanged at Git blob `cb6b5f7e899338380b4b404704bfbf030f2952df`; that update records the later production
refresh and supplies no scratch artifact. The plan's named worktree,
`C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics`, no longer exists. Neither the review worktree
nor the primary clone has any of the 30 named scratch paths checked for this classification. The
tracked `.gitignore` ignores `.novc/`.

The 43 lines have these classifications:

| Searchable anchor in the finished plan | Lines in the live tree | Classification |
|---|---:|---|
| “The reproducible scratch scripts remain” and the experiment command | 163–166 and 171 | Historical command record, reproducible method and disposable outputs. The plan states the conversion, comparison and codepoint-inspection method and explicitly requires reconstructing a missing checker. The tracked review-differences receipt preserves the original nine changed fields, while the Phase 2 implementation and receipt preserve the accepted general representation rules and corrected direct-cluster method. The absent scripts are not inputs to a current operation. |
| Phase 2 candidate command under “Implementation phases” | 239 | Reproducible current command and disposable output destination. The tracked `py/main_parse.py ws-products --output-dir` entry point remains live, and `py/subcommands/parse_ws_products.py` rejects a production-tree destination. A new run creates a new candidate; the named `.novc` directory is not an input. |
| Phase 5: “create a disposable standalone clone” | 328 | Historical optional verification method and disposable working copy. The plan permitted omitting the private census, and Phase 5 did omit it. Commit `d32a17b82c8dbf779be101be896c7c491c5b4e4e` later removed the `near-aleppo-census` mega step, so the current MAM-basics mega has no private writer for this procedure to support. |
| Baseline wrapper, eight-command driver, driver command and receipt directory | 360, 367, 380 and 390 | Historical wrapper and command record, reproducible method, and historical output inventory. The plan prints all eight tracked entry points in order and records every return code and generated-diff result. The later phase commits preserve the code as it stood, and current generation has the tracked `py/main_0_mega.py` entry point. The missing logs limit direct reinspection of the 2026-09-10 processes but are not inputs to a current method. |
| Phase checkout receipts | 442, 531, 714, 826 and 916 | Historical environment and starting-state records. Each phase section records the task ID, checkout, branch and starting commit in tracked prose, and Git history preserves each named commit. No current operation reads a checkout receipt. |
| Phase 1 capture and replacement-check commands and reports | 461, 464, 470 and 474 | Historical differential commands, outputs and reproducible method. The pre-edit planner survives at commit `491cb6b84639a8235941e7ad63dd1d8127b82c67`, the replacement at `ee7ee2a05502e944162e34711da8210b50e2604f`, and the tracked corpus check remains in `py/tests/test_wikisource_plan_corpus.py`. The plan records the compared populations, case counts, ordering rules and results. The exact scratch harness is unavailable, but no tracked result or current planner operation requires byte-for-byte replay of that completed harness. |
| Phase 1 downloader wrapper, log and command receipt | 502 and 507–508 | Historical command and output record. The plan records the two tracked test modules, the 15-test result and the meaning of the checks. Both test modules remain tracked; a fresh run does not read either missing output file or the missing wrapper. |
| Phase 2 whole-corpus verifier and detailed scratch receipt | 608 and 614 | Historical verification command and output. The tracked Phase 2 validation receipt preserves the 39-book, 929-chapter and 23,202-verse population, every changed path and codepoint sequence, serialization and mark-order results, plus validation and the accepted representation rules. The tracked converter remains in `py/ws/ws_plain.py`. |
| Phase 2 rendering wrapper and detailed scratch receipt | 617 and 626 | Historical verification command, reproducible method and output. The tracked Phase 2 receipt preserves the complete rendering differences and all nine inverted-nun results; the tracked MAM-with-doc, MAM-simple, Sefaria, AJF and OSIS handlers remain available for a new whole-corpus comparison. |
| Phase 2 independence wrapper and detailed scratch receipt | 632 and 642 | Historical fault-injection command, reproducible method and output. The plan states every blocked input and import, the write boundary and input census. The tracked Phase 2 receipt preserves the counts and successful boundary results, and the current candidate entry point supplies the subject for a new fault-injection harness. |
| Phase 2 receipt writer | 645 | Historical provenance. The command wrote the tracked Phase 2 validation receipt that survives; the writer is not required to read, use or re-establish that receipt. |
| Phase 2 Google, format-2 and suite wrappers, with the shared receipt directory | 653, 657, 670 and 677 | Historical wrapper commands and output inventory. The direct tracked entry points remain, while Git history at Phase 2 preserves their then-current behavior. The plan and tracked Phase 2 receipt preserve the return codes, documentation result, suite result and unchanged-production conclusion; none of the missing logs is a current input. |
| Phase 3 Google and comparator wrapper commands | 735 and 758 | Historical wrapper commands around current tracked entry points. The tracked Phase 3 receipt preserves their zero-difference results, and commits `05cfc018ee63da5bcb25dd2d3152157f75029584` and `426fa229c69aad6168cf2ec5217b105088d6293f` preserve the intermediate and cutover implementations. A current comparison runs the direct entry points rather than reading a wrapper or its logs. |
| Phase 3 source-boundary verifier and scratch receipt | 766 and 782 | Historical fault-injection command, reproducible method and output. The plan states the blocked production input and Google-only mutation checks. The tracked Phase 3 receipt preserves the reader boundary, search and replacement checks, normalization-call count and results; the Google reader and comparator remain tracked. |
| Phase 4 detailed receipts and logs | 896 | Historical output inventory. The tracked Phase 4 validation receipt preserves the source boundary, product comparison, protected-capture counts, commands and test results. Commit `426fa229c69aad6168cf2ec5217b105088d6293f` preserves the complete cutover diff. |
| Phase 5 mega logs | 923 | Historical output inventory. The tracked Phase 5 validation receipt lists every one of the 38 local steps in order with its return code and timing, records the omitted private step and preserves the stability result. The current mega is a tracked direct command and has since removed that private step. |
| Phase 5 artifact-audit receipt | 959 | Historical detailed output. The tracked Phase 5 receipt names all 30 changed artifacts, partitions them by the two accepted representation changes, records the change-log arithmetic, support copy, protected-tree hashes and empty unexplained-change set. Git diff from baseline `67cb3ecc17931732d2cd1f9bbafee1976a322a2e` through Phase 5 commit `321b2eeb43295f4de0e9e008e9c13bcbeb371df6` preserves the artifact changes themselves. |
| Phase 5 primary-checkout postcheck | 991 | Historical environment output. The tracked Phase 5 receipt preserves both observed primary-checkout heads, the three concurrent paths and the conclusion that Phase 5 wrote no primary-checkout file. Git history retains both named heads and the concurrent commit. |
| Phase 5 detailed logs and command receipts | 997 | Historical output-location record. The tracked Phase 5 receipt and the finished plan preserve the commands, results, artifact accounting, limitations and protected-tree hashes. The missing detailed logs are not inputs to the completed products or a current verification method. |

No line in this plan is a statement that no `.novc` dependency remains; the table supplies that
classification now. No `.novc` artifact named or described by the plan is an indispensable
missing dependency of a tracked result or current method. The missing harness sources and logs
limit byte-for-byte replay and direct reinspection of the historical executions, but the finished
plan, tracked validation receipts, phase commits, current entry points and Git history preserve
every accepted method and result needed now. No new Ben decision arises from this classification,
and D12 leaves both the finished plan and its existing sibling update unchanged.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped, in 75.81 seconds.

Product axis: this classification changes only the review's live sibling update and reaches no
generated MAM product. Act axis: the write is an ordinary repository change on the unpushed review
branch; no outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 7.1, revision-aware Wikisource downloads plan: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-13. This entry classifies only the 24 live lines containing `.novc`
in `doc/PLAN-efficient-wikisource-downloads.md`. It does not establish a rule for the rest of
finding 7's census.

At checkpoint `520f2df2648582651c0c58af0d00f29d45d301ff`, current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was already merged. The finished plan remains
unchanged at Git blob `85fd19f1e6a25de7f145d1e9d7678271cd9d5b94`. Its existing sibling update remains at Git blob
`d12529f6372cd5ee0db5d43bcd5bb8bb184cae99`; that update records the later production refresh
and supplies no scratch artifact. The plan's named worktree,
`C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics`, no longer exists. Neither the review worktree
nor the primary clone has the plan's named `ws_efficiency_*` scripts or `ws-efficiency-*`
output directories. The tracked `.gitignore` ignores `.novc/`.

The 24 lines have these classifications:

| Searchable anchor in the finished plan | Lines in the live tree | Classification |
|---|---:|---|
| Phase 1: “The generated versions were saved” | 301 | Historical output-location record. The tracked Phase 1 receipt preserves the generated and baseline SHA-256 values for both vendoring reports and names their disposition; the current tracked reports remain the inputs to a new comparison. The saved copies were evidence for the completed run, not inputs to a live operation. |
| Phase 1: the nine commands under “Reproducing Phase 1” | 319, 323, 329, 335, 339, 343, 347, 351 and 355 | Historical command record and reproducible method. The tracked Phase 1 receipt preserves the exact successful commands, checkout, commit, timings, logs, results and hashes of six scratch sources. The receipt-writer command at line 355 is historical provenance for the receipt that survives. The paragraph beginning “If scratch tools are absent” specifies how to reconstruct the bounded measurement against a new commit; current planner, downloader, revision-client and suite entry points remain tracked. |
| Phase 1: “Raw responses, request headers/parameters, full logs” | 359–361 | Historical evidence-location and filename inventory. The tracked receipt preserves the request counts, body-byte counts, response-manifest hashes, per-book hashes, exact upstream changes, command results and protected-tree hashes. No current program reads the missing directories. |
| Phase 2: “Reproduce the matrix from the development checkout” | 524 and 528 | Reproducible verification specification and historical command record. The plan states the complete required matrix and its 51 main checks plus 9 additional checks. The tracked Phase 2 receipt names all 60 passed checks, the exact commands and the scratch-source hashes. The production implementation and its adapted tracked downloader fixture remain in the tree, so a fresh fault-injection harness can be written against the current interfaces without recovering either dated script. |
| Phase 2: “Final command logs live under”, the extras driver and preserved reports | 535, 546 and 558 | Historical log/output inventory and reproducible method. The Phase 2 receipt records each direct command, result and log name, and records the same two generated/baseline report hashes as Phase 1. The extras driver only sequenced tracked entry points; the saved reports and logs were outputs, not inputs. |
| Phase 3: “Captures and scripts are under” | 612 | Historical evidence-location and filename inventory. The named worktree is gone. The tracked Phase 3 receipt preserves the measurement method, every run's command and result, request and response-manifest hashes, API failures, exact upstream edits, per-book hashes, product comparisons and hashes of all 13 scratch scripts. The missing response bodies cannot be used to resume the completed 2026-09-10 run, but no current operation calls for resuming that run; a new measurement must fetch and record new responses. |
| Phase 3: the live, product and comparison drivers | 722, 726 and 727 | Reproducible method and historical command record. The plan fixes the run order, independent-decoder boundary, resume rule, product scope, write guard and comparison requirements; the Phase 3 receipt records their results and source hashes. The tracked downloader, revision modules, product generators and receipt data remain the concrete inputs for a new implementation of the method. |
| Regeneration: `ws-products --output-dir` | 760 | Reproducible current command and disposable output destination. The tracked `py/main_parse.py ws-products` entry point creates the candidate; `.novc/ws-efficiency-candidate` is an output directory, never an input. |
| Regeneration: the Phase 5 mega driver | 767 | Reproducible method and historical command record. The following paragraph explicitly says to reconstruct the narrow driver from tracked `main_0_mega._STEPS` when the script is missing. The private `near-aleppo-census` step that the dated driver omitted has since been removed, and current `CLAUDE.md` names the direct tracked `py/main_0_mega.py` command for a worktree run. |

None of the 24 lines is a statement that no dependency remains; the table supplies that
classification now. No `.novc` artifact named or described by the plan is an indispensable
missing dependency of a tracked result or current method. The absent captures and logs limit
reinspection of the historical HTTP bodies, but the completed plan treats the tracked receipts as
the durable records and requires a new retrieval for a new measurement. No new Ben decision
arises from this classification, and D12 leaves both the finished plan and its existing sibling
update unchanged.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 75.63 seconds.

Product axis: this classification changes only the review's live sibling update and reaches no
generated MAM product. Act axis: the write is an ordinary repository change on the unpushed review
branch; no outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 7.1, worktree-file-consolidation plan: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-13. This entry classifies only the 24 live lines containing `.novc`
in `doc/PLAN-worktree-file-consolidation.md`. It does not establish a rule for the rest of finding
7's census.

At checkpoint `4816afe2cad093ebfc001b827805bdd593c54021`, current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was already merged. The finished plan remains
unchanged at Git blob `5b8da2ddc883016e4afa939b0a657a191f0cf5d7`. Its existing sibling update remains unchanged at
Git blob `d1a68033a6591bd3a717b990f8262fbbe08e4bf0`; that update supplies the plan's State declaration
and no scratch artifact. The six phase worktrees named by the plan no longer exist. The tracked
`.gitignore` ignores `.novc/`.

The 24 lines have these classifications:

| Searchable anchor in the finished plan | Lines in the live tree | Classification |
|---|---:|---|
| Scope: “`parse_ws` writes optional format 1 output under” | 114 | Reproducible current output policy and disposable output. The tracked `py/main_parse.py ws --write-fmt-1` entry point and `py/subcommands/parse_ws.py` write `.novc/mam-ws-parsed-fmt-1/`; the directory is generated debugging output, not an input. |
| Phase 1: “The scratch driver used for the original measurement” and “Logs and all-file before/after snapshots remain in” | 155 and 161 | Historical evidence-location record and statement that no dependency remains. The next sentence says that the scratch files are conveniences and that the committed evidence and reproduction method suffice. The Phase 1 worktree is gone, while the tracked compressed evidence retains the baseline inventory, UXLC-note entries, historical manifest and members, Job source blobs and typed values, generator runs, environment and Wikisource counts. |
| Phase 1: the original `verify_worktree_file_consolidation_phase1_plan.py` command | 200 | Historical verification command. The receipt records what the absent checker established, including the complete directory map and hashes of all 208 affected output paths. The tracked compressed evidence, the printed inventory script and Git history preserve the inputs and method needed for a new check. |
| Inventory reproduction: the printed recheck-script path, output path and command | 323, 380 and 386 | Reproducible method and disposable output destination. The complete Python source is printed in the plan, reads an explicitly supplied commit with `git ls-tree -r -l -z`, and writes a new UTF-8 JSON report under `.novc/`; neither scratch pathname is an input. |
| Phase 2: “the explicitly identified scratch replay archive” | 442 | Historical disposable test-fixture pointer. The plan distinguishes this replay from the unavailable historical `Notes.zip` comparison, and its Phase 2 acceptance criteria explicitly permit creating a scratch verification archive. The consolidated per-book JSON, `NoteStorageOperation` and the production ZIP verifier remain tracked. |
| Phase 2: the migration, verification, replay, output-comparison and inventory commands | 461–463, 465 and 470 | Historical command record and reproducible method. Git history retains the 477 source HTML blobs, the consolidation commit retains the 36 JSON results and storage implementation, and the immutable baseline records every source size and hash. The plan states the downloader probes, malformed-storage cases, generated-output comparison and inventory arithmetic; the scratch scripts and replay archive were not inputs to a live operation. |
| Phase 3: the archive builder, archive verifier and MPP comparison commands | 603–605 | Historical command record and reproducible method. The plan specifies sorted names, `ZIP_STORED`, fixed timestamps, Unix creator metadata, permissions, empty comments and extra fields, member checks and negative probes. The six archives, manifest, `mpplus_revisions.py`, historical README, Phase 1 evidence and phase commits remain tracked. |
| Phase 4: the `verify_job_records_phase4.py` command | 737 | Historical verification command and reproducible differential specification. The plan records every comparison and result; the Phase 1 evidence retains the original source blobs, ordered typed values and hashes, Git history retains the per-record modules, and the live tree retains the chapter modules and consistency and relation checks. |
| Phase 5: the static verifier, notes replay and post-verifier commands | 914, 916 and 927 | Historical verification command record and disposable replay output. The receipt says that Phase 5 used only committed inputs plus fresh task-local probes, read no earlier phase scratch and extracted no historical archive. It records every checked path set, hash, failure probe, generator result and the three corrected verifier assumptions; the production entry points and immutable baseline remain tracked. |
| Phase 6 receipt: the benchmark parent and driver | 984 and 986 | Historical execution-location and filename record. The old worktree and raw task-local record are gone, but the plan preserves the exact operation timed, six commands, revisions, fresh child paths, durations, output endpoints, Git configuration, cleanup checks, result-file hash and limitations. The driver was not an input to a live operation. |
| Phase 6 instructions: “A suitable task-owned parent is” | 1097 | Reproducible benchmark method and disposable working directory. The surrounding instructions specify alternating revisions, fresh detached worktrees, timing boundary, recorded environment and results, verified cleanup and interpretation. A new benchmark creates a new task-local directory and new measurements. |
| Commit discipline: “Write a unique commit-message file under `.novc/`” | 1132 | Historical procedure and disposable message-file destination. The sentence prescribes a fresh task-specific file and `git commit -F`; it points to no retained input or result. |

No `.novc` artifact named or described by these lines is an indispensable missing dependency of a
tracked result or current method. The unavailable raw benchmark record and phase logs limit
reinspection of those historical execution details, but the finished plan is the durable receipt
and preserves the reported measurements, methods, limitations and hashes. No new Ben decision
arises from this classification, and D12 leaves both the finished plan and its existing sibling
update unchanged.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 76.25 seconds.

Product axis: this classification changes only the review's live sibling update and reaches no
generated MAM product. Act axis: the write is an ordinary repository change on the unpushed review
branch; no outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 7.1, instruction-file remediation plan: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-12. This entry classifies only the 16 live lines containing `.novc`
in `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md`. It does not establish a
rule for the rest of finding 7's census.

At checkpoint `86fa91719c40cebd444bde6bb88a3c78fb77f752`, current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was already merged. The finished plan remains
unchanged at Git blob `abc066916cba72157693e6a89e419677abb248ad`, and no sibling update file
exists. The review worktree has no `.novc/review-2026-09-09/` directory. The primary clone still
has the complete machine-local bundle: 13 Python scripts and 10 output files. The tracked
`.gitignore` ignores that directory.

The 16 lines have these classifications:

| Searchable anchor in the finished plan | Lines in the live tree | Classification |
|---|---:|---|
| “Baseline: no drift anywhere” | 102 | Historical precondition and reproducible method. The primary clone still has `drift_check.py`, but §6 already identifies its stale checkout and filename constants. The tracked `dot-claude/README.md` supplies the current file-hash and recursive-comparison commands, including both comparisons required for the shared skill. |
| M1: `show_policy.py` | 126 | Reproducible method. The script and `policy_excerpt.txt` survive in the primary copy. The authoritative inputs remain tracked in `in/repo_maintenance_policy.json`, `all-repos.code-workspace` and `py/repo_util/repo_selection.py`; the plan states the fields and assertions the script displays. |
| M2: `resolve_paths.py` and `paths_report.txt` | 140 | Reproducible method and historical output filename. The script and report survive in the primary copy. M2 names all five paths, their tracked replacements and the governing repository section, so no unrecorded classification is needed to repeat the check. |
| M3: `substitution_proof.py` and `substitution_diff.txt` | 163 | Historical provenance and reproducible method. The script and exact report survive in the primary copy. Section 6 states that the comparison applies the same section comparison at github-misc commit `f8898a9`; §0 identifies the private remote and the commands for reaching that history. A fresh clone is an explicit input to a new run, not a missing `.novc` dependency. |
| M4: `final_checks.py` | 184 | Historical verification record and reproducible method. The script survives in the primary copy, while M4 names the checked section and the tracked file that supplies it. The verification result is evidence for the dated plan, not an input to a live repository operation. |
| M5 and D3: `section_compare.py` and `section_compare.txt` | 224 and 356 | Reproducible method and historical report. The script and report survive in the primary copy. Section 6 states the operation—compare corresponding `##` sections after the `claude` to `Codex` substitution—and warns that the checkout constant must be repointed before a new run. M5 and D3 state which differences matter; no hidden predicate is required. |
| M8: `remeasure.py`, with the alternate per-page search | 262 | Reproducible method. The same sentence gives the direct search alternative, and the three tracked pages and their Git history remain the inputs. The primary copy also retains the script. |
| M12: `resolve_issues.py` and `issues_report.txt` | 306 | Historical external-state evidence and filename inventory. The primary copy retains both files. M12 enumerates every cited site and required tracker prefix, so future edits do not depend on reconstructing the dated issue-state report. |
| D5: `remeasure2.py` | 379 | Reproducible method. D5 identifies the tracked `liberality_metric.py` constant and its `--html-dir` override, which are the facts the check inspects. The primary copy retains the script. |
| D9: `remeasure.py` and `numeral_dupes.py` | 409 | Historical measurement and reproducible method. Both scripts and `numerals_report.txt` survive in the primary copy. The plan names the measured figures and points to the corresponding sections of the tracked MAM-private `masorah-books/README.md`, which remains the authority rather than either scratch script. |
| D16: “were copied to `MAM-basics/.novc/review-2026-09-09/`” | 458 | Historical evidence-location record. The primary copy still exists. The tracked §7 preserves Ben's one-off-review decision and the remaining proposal independently of the scratch directory. |
| §4 item 1: `resolve_shas.py` and `shas_report.txt` | 467 | Historical verification result and reproducible method. The script and report survive in the primary copy. The plan pins the 23 SHAs to their repositories and dates; local or remote Git history, rather than the scratch report, remains the source for a new verification. |
| §6: the copied directory, commands that resolve there, and ignored status | 521–523 | Evidence-location record, filename inventory and explicit recovery method. The primary copy has exactly the 13 scripts and 10 outputs §6 describes. Section 6 records each script's inputs and outputs, identifies the stale constants, and instructs a fresh session to rewrite a missing script from those descriptions. The special historical input for `substitution_proof.py` is separately named in §0. |

No `.novc` artifact named or described by these lines is an indispensable missing dependency of a
tracked result or method. No new Ben decision arises from this classification; the plan's existing
substantive decisions and §7 proposal remain exactly as the finished plan records them. D12 leaves
the finished plan unchanged.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 76.16 seconds.

Product axis: this classification changes only the review's live sibling update and reaches no
generated MAM product. Act axis: the write is an ordinary repository change on the unpushed review
branch; no outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 7.1, Phase 6 map, September 8 review and close-out plan: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-12. This entry classifies only the live `.novc` references in
`doc/mam-products-phase6-command-map.md`, `doc/review-findings-2026-09-08.md` and
`doc/PLAN-close-out-review-2026-09-08.md`. It does not establish a rule for the rest of finding
7's census.

At checkpoint `a94ee16e703c768838b4b58c4d239c68623c1632`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, each assigned document
has 4 lines containing `.novc`. Their Git blobs are
`741485b0672a6985712ec9a7025d6528547b5cd0`,
`3df541234f0952f17efce6c5b897af7ff7451f11` and
`baccee1bdf429519314ea7a5252ea495e0bf98f9`, respectively. The command map has no sibling update.
The existing `doc/review-findings-2026-09-08-update.md` and
`doc/PLAN-close-out-review-2026-09-08-update.md`, at Git blobs
`d38316952314a11182beaab2ce8b2004740aea77` and
`69b989ec30fe319b13a27cc13eb04ada439b7b23`, correct unrelated State and display-fallback
passages and supply no scratch artifact.

The 12 lines have these classifications:

| Finished document and searchable anchor | Lines in the live tree | Classification |
|---|---:|---|
| `mam-products-phase6-command-map.md`: “The directories are” | 130–132 | Reproducible commands and disposable outputs. The tracked `in/mam_products_phase6_baseline.json` preserves the full `build` and `check` argument arrays, exact redirect-manifest inputs and every `scratch_stub_paths` member for all five directories. The live `py/main_redirect_stubs.py` and `py/redirect_stubs/stubs.py` implement those commands. Each `.novc` directory is regenerated output, not an input. |
| `mam-products-phase6-command-map.md`: “Use a uniquely named `.novc/` Python file” | 177 | Reproducible method and temporary implementation choice. The plan gives the exact NUL-delimited `git ls-tree` command above this line and the byte-count, SHA-256 and Git-object checks below it; the tracked baseline preserves the sets and file records being checked. No particular scratch filename or unrecorded predicate is required. |
| `review-findings-2026-09-08.md`: “and `give_std_mark_order` put them back” | 71 | Historical provenance and reproducible method. The finished review already contains the corrected bytes. The tracked `give_std_mark_order` and `has_std_mark_order` implementation remains in `py/mb_cmn/uni_denorm.py`, and `py/tests/test_prose_mark_order.py` now checks the finished review. The primary clone still has `fix_findings_marks.py`, but that writer is not an input to the document or the lint. |
| `review-findings-2026-09-08.md`: “Every script and output is untracked under” | 145 | Historical evidence-location and naming record. The line identifies the completed review's four stream prefixes and main-session bundle. The review's tracked scope, findings, reconciliation and dispositions preserve the conclusions; no current Python path invokes this directory. The primary clone still has the evidence bundle, but no tracked result or current method takes the bundle as input. |
| `review-findings-2026-09-08.md`: “`9e6e9e17`'s ‘415 files’” | 558 | Historical evidence-inventory result. The primary clone's `review-2026-09-07` directory still has exactly 416 files, including `commit_msg_review_findings_2026_09_07.txt`; commit `9e6e9e173d179aa3ddea2b2217f5798e6f1a3e94` preserves the earlier 415-file statement. The corrected count describes that completed bundle and is not an input to a live operation. |
| `review-findings-2026-09-08.md`: “or `.novc/review-2026-09-08/` script that re-establishes it” | 756 | Reproducible-method index and historical evidence pointer. The review states the fixed Git ranges, each finding's population and measurement, and the plain Git commands where a command suffices. The named throwaway scans implement those stated checks; every specifically named re-establish artifact checked for this classification remains in the primary copy. The tracked reconciliation and dated dispositions preserve the accepted conclusions, and no unrecorded semantic partition comparable to finding 7.2's first-match predicates was found. |
| `PLAN-close-out-review-2026-09-08.md`: “Turn-5 scripts” | 108 | Historical evidence pointer. The old worktree is gone, but all three named scripts and both reports remain in the primary clone's copied review directory. The tracked turn-5 document gives the Git commands and findings those files checked; finding 7's earlier singleton classification records that the verdicts depend on tracked files and Git history rather than on the verification scripts. |
| `PLAN-close-out-review-2026-09-08.md`: “integration-receipt.json” and “ignored `.novc/review-remediation-2026-09-08/` evidence” | 1177 and 1208 | Historical receipt pointer and preservation instruction. The source directory disappeared with the retired worktree, as planned, but its 6,208 files survive in the verified external evidence archive and manifest named at lines 1211–1213. The archive's current SHA-256 is `33495ad7b7d0b040719ded27ff5544a75efb2f19c0c971c4d333a790dbb523ce`, equal to the manifest, and the manifest inventories `wave4-01a08b71/integration-receipt.json`. The receipt is preserved evidence, not a missing dependency. |
| `PLAN-close-out-review-2026-09-08.md`: “the ignored `.novc/review-2026-09-08/` does not count” | 1232 | Historical retirement instruction and evidence-location note. The statement explains Git's worktree-removal behavior and points back to the primary copy of the turn-5 files, which still exists. The worktree and branch named by the completed instruction are gone; no current operation depends on the old ignored directory. |

No `.novc` artifact named or described by these lines is an indispensable missing dependency of a
tracked result or method. The close-out evidence remains deliberately external and verified; it
must remain unchanged as a receipt. No further Ben decision arises from this unit, and D12 leaves
all three finished documents and both existing sibling updates unchanged.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 81.12 seconds.

Product axis: this classification changes only the review's live sibling update and reaches no
generated MAM product. Act axis: the write is an ordinary repository change on the unpushed review
branch; no outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 7.2: the two finished reports have one missing exact-replay dependency

Recorded by Codex on 2026-09-12. This entry classifies only the `.novc` references in
`doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md` and
`doc/meteg-after-silluq-search-in-mam-documentation.md`. It does not establish a rule for the
rest of finding 7's census.

At checkpoint `c141f54105e12042150b16b81cf521685071d7be`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, each finished report
has 23 lines containing `.novc`. The current worktree has none of the named `mas_a_*` or
`mas_b_*` files. The screen report's named worktree,
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/zen-babbage-2d6583`, no longer exists. The
screen report remains unchanged at Git blob `09ac3f23175aacb1ffb10c39894b3c2d2fe78912`.
The documentation-search report remains unchanged at Git blob
`5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`.

The 23 screen-report lines have these classifications:

| Searchable anchors in the finished screen report | Lines in the live tree | Classification |
|---|---:|---|
| “Written by `.novc/mas_b_write_doc.py`” | 3 | Historical provenance. The sentence identifies the writer that lifted the Hebrew forms and made the finished report; D12 gives no current process a reason to regenerate that report. |
| `mas_b_syllables.py`, `mas_b_screen.py`, `mas_b_mgketer.py`, `mas_b_nuclei.py`, `mas_b_write_doc.py`, `mas_b_verify_members.py` and `mas_b_peek_no_sopa.py` in the analytic sections | 22, 31–32, 59, 65, 85, 96, 101, 251, 268 and 313 | Reproducible methods. Sections 1, 3 and 11 state the inputs, loader rules, verse-final-chanted-word rule, alignment, position comparison, classes, calibration and syllable criterion. The missing filenames identify the implementations used in 2026; the methods do not require those implementations. |
| “listed in `.novc/mas_b_mgketer_report.txt`” | 276 | Filename inventory. The missing intermediate report held the 17-item skip list; the screen report states the count and the reason for the skips, and the list can be re-derived by section 11's method. |
| “All are gitignored under `.novc/`” and the nine `.novc/mas_b_*.py` command lines | 318, 329, 333, 337, 341, 345, 349, 353, 357 and 361 | Historical command record. The commands name the order and environment of the completed run. The old worktree is gone, so the commands are not runnable instructions in the live tree. Lines 364–381 preserve what each command did and which intermediate files it made. |

The screen method has a concrete tracked replacement for the unavailable scripts. Commit
`6ca009a583805283c4dd695adf465fff8056f774` changed the live
`doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md` to call the screen report's section 11 “the
method of record for loading and aligning all three.” The MAM-simple, UXLC 3.9, WLC 4.22 and WLC
4.20 inputs and the named `accgram` helpers all exist at the report's pinned MAM-basics commit
`30fb7681`. Phonetic MAM exists at the pinned MAM-private commit
`3f53991ca85d0b53b0e9291d670299f4f4b5c6db`. Git history identifies
`3025e8221d05a624071dccba0eecd10bbd4c3d1c` as the last MAM-private commit affecting
`mgketer/out/` before the report was committed. No `.novc` file is indispensable to repeating
the screen as a new measurement from those tracked inputs.

The 23 documentation-search-report lines have these classifications:

| Searchable anchors in the finished documentation-search report | Lines in the live tree | Classification |
|---|---:|---|
| `mas_a_compare_a06_ws_report.txt`, `(c')` in `mas_a_ws_docnotes_report.txt` and `mas_a_intro_grep_report.txt` | 16, 135 and 139 | Filename inventory. These are missing intermediate views of the completed run. The report states the compared sets, the 52-call disposition, the eight introduction-search terms and the four filtered views. |
| `mas_a_stress_after_census.py` and `mas_a_stress_classify.py` in the analytic sections | 72 and 87 | Reproducible methods. The report states Ben's syllable definition, the census population and classifications, and the candidate rule; the classification uses the tracked `py/accgram/post_stress_meteg.py` parser. The historical Phonetic MAM input remains available at `3f53991ca85d0b53b0e9291d670299f4f4b5c6db`. |
| “the test for each is in `.novc/mas_a_write_doc.py`” | 56 | Indispensable missing dependency for exact replay of the ten first-match category counts. The report lists category names and totals, but no tracked file preserves the predicates or the precedence behavior when one call matches several predicates. Reimplementation without those decisions could produce a different partition while preserving the same 166-call population. |
| “All scripts are gitignored under `.novc/`” and the eight `.novc/mas_a_*.py` command lines | 241, 250, 256, 262, 268, 274, 280, 286 and 292 | Historical command record. The commands identify the completed run's environment and order; no live operation invokes them. |
| The eight numbered `.novc/mas_a_*.py` descriptions | 247, 253, 259, 265, 271, 277, 283 and 289 | Method and filename inventory. The entries say what was scanned, cross-checked, classified or looked up and name the intermediate files. The tracked inputs exist at MAM-basics commit `30fb7681` and MAM-private commit `3f53991ca85d0b53b0e9291d670299f4f4b5c6db`; the live tree also has the tracked Wikitext parser and the post-stress-meteg parser. The writer reference is historical provenance except for the missing first-match predicates identified above. |

Neither finished report has a statement that no `.novc` dependency remains. Finding 7's example
of that category is `doc/meteg-after-silluq-in-uxlc-and-wlc.md`, outside this classification.
The later sibling update files correct terminology and presentation but preserve no `mas_a_*` or
`mas_b_*` implementation, so they do not close the exact-replay gap.

Ben's decision, 2026-09-13: preserve and explain. Keep the category totals as historical results;
do not reconstruct predicates merely to replay the completed report. The existing
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` now corrects the finished report's
“Re-measure rather than trust” instruction. Finding 2's ten ordered predicate categories and its
`other` fallback cannot now be remeasured as the same exact partition because neither the
predicates nor their precedence was preserved. The displayed totals remain historical results of
the 2026-09-09 run; the correction does not declare the totals false. The remeasurement
instruction continues to apply to figures whose methods remain preserved.

No predicate has been reconstructed, no script has been added, and neither finished report has
been changed. This documentation-only decision record reaches no generator or product and does
not owe a mega run.

At the decision-pending classification checkpoint, `git diff --check` and the tracked-prose
mark-order lint passed; the lint passed 1 test. The full suite passed 997 tests, with 5 skipped,
in 76.12 seconds.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; both finished
reports remain unchanged, and no outward-facing act, destructive local act, external
configuration write or receipt rewrite occurred.

## Finding 7.1, mega-coverage pair: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-12. This entry classifies only the `.novc` references in
`doc/PLAN-mega-coverage.md` and `doc/mega-coverage-2026-09-10.md`. It does not establish a rule
for the rest of finding 7's census.

At checkpoint `8e2db58f6fd3b7fd30bd3c71951167871637f294`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, the finished plan has
2 lines containing `.novc` and the finished report has 3. The plan's named worktree,
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/mega-coverage`, no longer exists. The plan
remains unchanged at Git blob `dee11fb218d56f77ab780a7e1a7528322daa464b`; the report remains
unchanged at Git blob `9b0a26f459fc340c4e046403cd41340dd9220fd4`. The existing
`doc/PLAN-mega-coverage-update.md` changes only Phase 7's run-mode sentence and supplies no
missing scratch artifact.

The five lines have these classifications:

| Searchable anchor in the finished plan or report | Lines in the live tree | Classification |
|---|---:|---|
| Plan: “Throwaway scripts and message files go under” | 51 | Historical method. The sentence records where each completed phase put temporary working files; it points to no particular file and preserves no input or result. |
| Plan: “The scratch evidence is in the worktree's `.novc/mega-coverage-phase5b/ctr/`” | 226 | Historical evidence pointer. The directory and its worktree are gone, but no indispensable dependency is missing. The plan's Phase 5c item 2 records the accepted narrow-sense paseq-template mapping, the 84-entry result and the five changed records; Phase 5c's completion record names commit `9fa80e1162c8dc9a0c3f9a93dd1507ca755d92f3`. That commit preserves the handler, mega step and exact `out/diff_ctr_mam.json` diff, and the handler and step remain in the live tree. |
| Report: “a measurement written only to `.novc/`” | 137 | Reproducible method and output policy. The tracked `survey-breuer-zaqef-units` entry point regenerates `.novc/breuer-zaqef-units.json`; `.novc` is the destination, not an input. The separately stated Phonetic MAM dependency remains explicit and is not a missing `.novc` dependency. |
| Report: “read Holman's untracked mailboxes under `.novc/`; the reports regenerate from the tracked derivatives” | 154 | Statement that no report-regeneration dependency remains. The mailboxes are intentionally per-machine inputs needed only to ingest a new message. Existing reports regenerate from `holman/emails/` and `holman/docs-not-served/mam_suggestions.json`, as `CLAUDE.md`, the two tracked path accessors and the cited evacuation plan state. |
| Report: “debugging output to `.novc/`; the tracked half of the run is `parse-ws`'s” | 181 | Reproducible method and disposable output. The tracked `py/main_parse.py ws --write-fmt-1` path writes `.novc/mam-ws-parsed-fmt-1/`; the normal parse path writes the tracked format-2 and production outputs. The format-1 directory is re-created output, not an input or evidence dependency. |

No line in this pair is a filename inventory, and no `.novc` artifact is indispensable to a
tracked result or method asserted by this pair. Holman's mailboxes remain indispensable only for
future ingestion of the messages they contain; that intentional per-machine input boundary is
already tracked and requires no new decision. No correction to either finished document and no
addition to its sibling update is warranted.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped, in 77.58 seconds.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; both finished
documents and the plan's sibling update remain unchanged, and no outward-facing act, destructive
local act, external configuration write or receipt rewrite occurred.

## Finding 7.1, five singleton documents: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-12. This entry classifies only the single live `.novc` line in each
of `doc/assessment-two-stranded-artifacts-2026-09-09.md`,
`doc/codex-review-findings-2026-09-08-claude-turn-5.md`, `doc/foi-mtgmtg-empty-cell.md`,
`doc/user-level-config-in-cloud-sessions.md` and
`doc/meteg-after-silluq-in-uxlc-and-wlc.md`. It does not establish a rule for the rest of finding
7's census.

At checkpoint `e13ebba2e71e3f81fa54e04d209f9f1804ed37c1`, current `main` was already merged. The five
documents have Git blobs `f6fdd5591aeabd0a18894968eb1e493e754045ae`,
`211802245bf15d6a21b1670c450f410c9f0ad98b`, `591e14fcaa1cf734c0776887020573fdadcc48f2`,
`d7bde24203e46f12a748f365f398d4308f0f9a54` and
`fad8f1836286e3fbb76ce0da39918f23cdb9e4b9`, respectively. None has a sibling update file.

| Finished document and searchable anchor | Live line | Classification |
|---|---:|---|
| `assessment-two-stranded-artifacts-2026-09-09.md`: “the three measurements that needed a script” | 568 | Reproducible method and historical execution record. Section 9 names the interpreter, import, predicates, revisions, pathspecs and outputs, then explicitly tells a fresh session to rewrite the throwaway scripts because the preceding sections contain the whole method. Commit `847862f9ef0f6276e827b86a59ef5b6bc7d7cebb` records the same four evidence groups and their results. |
| `codex-review-findings-2026-09-08-claude-turn-5.md`: “The scripts are untracked at” | 52 | Historical evidence pointer. The unavailable filenames say where the completed review read its figures; the following sentence states that every citation also gives the plain Git command that re-establishes the figure. The verdicts depend on the cited tracked files and Git history, not on either verification script. |
| `foi-mtgmtg-empty-cell.md`: “The census scripts are gitignored” | 107 | Filename inventory and reproducible quantitative method. The section names each script's population, the tracked `wt_qere` handlers and the report role. Its numbered clauses state the counts, partitions, formulas, reduced-vowel control, consonantal-skeleton and stem comparisons, and verse-position comparison. The tracked `py/foi/foiz_wt_mtgmtg.py` handler and `gh-pages/MAM-with-doc/foi/foi-mtgmtg.json` preserve the survey population and partition; the document's regeneration command re-derives them. Commit `d99f2cf4134ac7691c3e10a58053ceb2d575180e` also records that the three evidence strands are re-derivable from the file. `verify_doc_claims.py` was a completed-run check, not an unrecorded semantic policy. |
| `user-level-config-in-cloud-sessions.md`: “The harness was a throwaway under `.novc/`” | 209 | Reproducible method and historical test record. Lines 206–210 enumerate all six fake-home cases, and the tracked `.claude/hooks/install-user-config.sh` remains the subject under test. The separately recorded real-cloud and live-home exercises are historical environment measurements, not outputs whose only evidence is the scratch harness. |
| `meteg-after-silluq-in-uxlc-and-wlc.md`: “checked that nothing in the file points into a `.novc` directory” | 118 | Statement that no dependency remains. The occurrence denies a `.novc` pointer and describes a completed writer check. Sections 9 and 10 preserve the data sources, method, calibration and tracked verse-link command. |

No `.novc` file named or described by these five lines is indispensable to a tracked result or
method. No further Ben decision arises from this five-document unit, and D12 leaves all five
finished documents unchanged.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 77.21 seconds.

Product axis: this classification changes only the review's live sibling update and reaches no
generated MAM product. Act axis: the write is an ordinary repository change on the unpushed review
branch; no outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 10: the moved crop directories have dedicated license coverage

Finding 10 is resolved. The notice-coverage mismatch recorded on 2026-09-12 no longer exists,
and Ben's 2026-09-13 decision is to keep the way `DATA-LICENSES.md` now covers the crops.

Commit `a8e4790e5f7db2efe9e5d94aecd6261e455b9a63` moved the eight crops out of the former
manuscript-based directories and into two directories for the work the crops serve:

1. `doc/meteg-after-silluq-snips/` contains five crops from images of the Aleppo Codex, the
   Leningrad Codex and the Second Rabbinic Bible.
2. `doc/lam-2-3-akhla-snips/` contains three crops from images of the Leningrad Codex, Cambridge
   Add. 1753 and Codex Sassoon 1053.

The same commit updated `DATA-LICENSES.md` in two places. The opening GPL-3.0 scope excepts both
crop directories from the repository's code-and-prose license, and one dedicated table row covers
both directories. The row says that each rights holder's terms apply, makes no grant, and states
that the crops are reproduced as evidence for the facts documented beside them. Each directory's
README separately records Ben's 2026-09-10 judgment that tiny crops like these are kept as fair
use.

On 2026-09-13 Ben said: “I thought that DATA-LICENSE.md was updated to reflect the move of
doc/*-snips. If so, keep whatever way it chooses to cover the topic of those snips.” The file is
`DATA-LICENSES.md`, and the live text does reflect the move. Therefore the dedicated shared row
and the root notice's present omission of the READMEs' fair-use statement both remain unchanged.
This remediation changes no license wording, image or crop; it updates only this live review
record.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.
