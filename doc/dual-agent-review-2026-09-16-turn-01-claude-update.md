# Updates to turn 01 of the 2026-09-16 dual-agent review

State: open, first entry 2026-09-17. Every entry here corrects or supplements
`doc/dual-agent-review-2026-09-16-turn-01-claude.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit. A
correction, later decision or later disposition goes in a sibling file named `<stem>-update.md`,
which is what this file is for turn 01 of the September 16 review.

## Ben approved the complete close-out decision package on 2026-09-17

Recorded by Codex on 2026-09-17, New York time, after the alternating review exchange closed
without a remaining disagreement. Ben first supplied the three decisions reserved by turns 05 and
06, then approved the two recommendations presented under the final "Decisions needed" heading.
Those approvals complete the one-list decision package below. Approval records dispositions; it
does not execute the remediation or approve concrete editorial wording that the fresh-task
remediation plan must present separately.

1. **Finding 1:** reconcile both snips READMEs' general crop-naming guidance with the approved
   Leningrad-specific rule without describing the September 10 preservation statement as
   literally false.
2. **Finding 2:** correct the cloud-session document's incomplete opening and two stale
   two-resource passages and the remediation plan's false no-edit assertion; make no policy change
   for a live document with an update sibling because no rule forbids that combination.
3. **Finding 3:** correct the four stale plan-blob assertions; retain `.Codex` at line 52 of
   `doc/review-findings-2026-09-10-update.md` and classify the path explicitly as a historical
   capture at `a872790e`.
4. **Finding 4:** extend the filename lint to the six missed filename-returning Git calls while
   recording that all 28 inventoried calls already use NUL delimiters.
5. **Finding 5:** add the permitted paragraph-join exception to all three pointer-only rules; leave
   the ordinary "unchanged" and "as written" statements alone because they do not assert byte
   identity and the governing policy supplies the exception.
6. **Finding 6:** correct stale progress and State wording, the loose heading-count label, three
   imprecise anchors, the missing cross-agent skill path, inconsistent executor naming and the
   reused section 7.3 phrase; require no new author annotation for historical in-place edits.
7. **Finding 7:** replace the topology skill's stale exclusions-and-gists wording and deploy the
   canonical correction; withdraw the unsupported prediction that following the complete cited
   rule would clone the excluded gists.
8. **Finding 8:** correct the moved mark-order pointer, stale Phase 3 and current-repository claims,
   and the non-issue source-number form without claiming that all three assertions became false
   only when moved.
9. **Finding 9:** repair obsolete live headings, quotations, paths, cross-file section references
   and cross-tracker issue spellings; preserve truthful historical retired-plan references and
   treat relocation of the wlc-utils paragraph as editorial.
10. **Finding 10:** add `mam-repository-topology` to the README's shared-skill list. The original
    user-level-file asymmetry no longer survives on current `main`, where the Claude file imports
    the common Codex body. The long-lived-branch backup exception wins over D11 for a shared review
    branch: push the branch to `origin` after every commit as a backup without pushing `main`. This
    procedure change is recorded in `doc/dual-agent-review.md` in the same close-out commit.
11. **Finding 11:** carry the low-severity provenance omissions into the remediation plan, with
    concrete wording required before restoring omitted decision dates, the enumerated
    strong-character detail, counts or attribution dates; do not imply that the underlying
    policies disappeared.
12. **Finding 12:** remeasure the rewritten retirement code on current `main`; if the defects
    survive, add reparse-point protection and a precise `.novc` citation-review gate while
    preserving the established auditability of the recorded list and note.
13. **Finding 13:** correct the Claude-ownership wording and unused-helper residue, make both Git
    date diagnostics describe the whitelist accurately, report a custom MAM-simple directory
    without the false `bhs` label, and harden stdin decoding if current hook serialization confirms
    the conditional non-ASCII defect.
14. **Finding 14:** add `py/` to the two broken root-relative module paths and leave the merely
    editorial "among" wording alone. Narrow `holman/WORKFLOW.md` to say that theme custom
    properties use `light-dark(...)`; leave the fixed badge colors unchanged.
15. **Finding 15:** narrow the New York label rule to generated clock dates and timestamps. Exempt
    historical decision dates, citations, quotations, release or revision dates and date-like
    names; do not add "New York time" to the thirteen inventoried visible dates merely because
    repository code writes or carries the page.
16. **Finding 16:** correct advice attribution, median descriptions, zero-denominator ratio blanks,
    receipt prose, document naming and replacement extent. Create
    `doc/mega-timing-laptop-2026-09-14-update.md` with the required base pointer and state that the
    unlabelled clock's inferred offset is `-04:00`, bracketed by approximately -04:01:05 and
    -03:58:09; do not claim that the receipt recorded a named zone. Treat finding 16.9 as a
    nondefect.
17. **Finding 17:** record in `doc/review-findings-2026-09-14-update.md` the correction of the false
    attribution of the "dropping" remedy to C3 and the supported disposition-lead, source-naming,
    reference and reproducibility shortcomings; do not rewrite the finished turn records or treat
    correct prose counts and differing scope labels as contradictions.
18. **Finding 18:** retain only the missing provenance and reproducibility defect in the `37.7 MB`
    figure, correct the commit-set description, add the omitted baseline suite count and explicit
    verification commands, clarify the recoverable record aliases, and treat the
    compatibility-covered `CLAUDE.md` citations as nondefects.
19. **Finding 19:** record through the receipt's update the correction of the phrase that assigns
    the prose system to books, remove the redundant "own", clean up the confirmed editorial
    formatting residue, use forward slashes for the drive path while retaining necessary UNC
    syntax, number the three exemptions, and name the intended works directly.
20. **Finding 20:** revise the review method to compare endpoint commit ranges and corroborate
    pushes directly, because commit-date `since` queries can miss an older commit pushed during the
    review window; the reviewed repository trees require no correction from this finding.

The fresh-task remediation plan with concrete editorial wording is the next close-out phase. No
remediation named above is performed by this decision entry, except for the procedure-record update
that the sequential-review procedure requires after Ben's decisions.

Product axis: this decision record and the procedure-record update reach no repository product.
Act axis: they are ordinary commits on the locked shared review branch, backed up to the existing
remote review branch; they do not update `main`, open a pull request, change an issue, perform a
destructive operation or rewrite a receipt beyond its authorized update pointer.

## Remediation completed on 2026-09-18

Recorded by Codex on 2026-09-18, New York time, after the substantive remediation head
`61aa48ee730a3cff222f28886298c6a06079586e` was backed up to the existing review branch,
fast-forwarded to `main`, pushed, and used to deploy the canonical user configuration. These are
the final dispositions of the twenty findings:

1. **Finding 1 was fixed by `4e30b0f4`.** The two snips READMEs now distinguish their general crop
   naming from the approved Leningrad-specific preservation rule.
2. **Finding 2 was fixed by `18ddfbf7`.** The cloud-session account now names all three resources,
   and the finished September 14 remediation plan's update records the false no-edit assertion.
3. **Finding 3 was fixed by `18ddfbf7`.** The remaining `.Codex` spelling is classified as a
   historical capture, and the stale plan-blob assertions now state the checkpoint, pointer and
   retirement history.
4. **Finding 4 was fixed by `016fc273`.** The structural lint now recognizes every current
   filename-returning Git call without pinning a site count, while retaining the NUL-delimiter
   requirement.
5. **Finding 5 was fixed by `18aabf8d`.** All three receipt-pointer rules now permit the
   mechanically necessary paragraph join.
6. **Finding 6 was fixed by `18ddfbf7`.** The September 14 remediation plan's update sibling holds
   the stale progress, State, heading, anchor, skill-path and executor corrections.
7. **Finding 7 was fixed by `18aabf8d`.** The topology skill now describes the declared workspace,
   frozen-repository register and vendoring policy; the canonical correction was deployed from
   pushed `main` at `61aa48ee`.
8. **Finding 8 was fixed by `4e30b0f4` and `18aabf8d`.** The reader-facing introduction guidance,
   moved mark-order pointer, Phase 3 and current-repository claims, and source-number form are
   corrected without rewriting the move's history.
9. **Finding 9 was fixed by `18aabf8d`; the portions already current at baseline remain
   unchanged.** The live headings, quotations, paths, cross-file section references and
   cross-tracker issue spellings are repaired, while truthful historical retired-plan references
   remain historical.
10. **Finding 10 was already resolved by current `main` at `d3edadc6` plus `fbaae3d0`.** The shared
    skill list, common-body wrapper and long-lived review-branch backup exception were current, so
    no later implementation commit was required.
11. **Finding 11 was fixed by `18aabf8d`.** The affected instruction and skill passages now carry
    dated or explicitly undated provenance without implying that the underlying policies had
    disappeared.
12. **Finding 12 was fixed by baseline `d3edadc6` and `d759adec`.** The current reparse-point
    guards already closed 12.1. The citation gate for 12.2 now matches only the exact relocated
    paths across the target, primary checkout and registered worktrees, preserves its complete
    audit record, and rejects generic `.novc` and `.novc-old` references. Verification used the
    operational simulation; no real worktree retirement ran.
13. **Findings 13.1 through 13.3 were fixed by `5b8e4026`; conditional finding 13.4 required no
    hook change under the approved stop rule.** The owner-scope diagnostic, unused helper, Git-date
    wording and custom MAM-simple directory diagnostic are corrected. Codex
    `0.154.0-alpha.6.2` ran the no-bypass inventory in ephemeral session
    `01a0b49d-6169-7812-810b-c3f61ef0ef0e`, but its diagnostics did not provide a complete hook
    source inventory. The result was therefore inconclusive: the hook-trust bypass was not used,
    the capture and subprocess harness were not run, and no live or tracked hook changed. The
    cleanup disposition and durable hashes for the ignored experiment result are recorded below;
    the `.novc/` path is not durable evidence.
14. **Finding 14 was fixed by `4e30b0f4` and `18aabf8d`.** The two module paths now include `py/`,
    and the Holman workflow distinguishes theme custom properties that use `light-dark(...)` from
    fixed badge colors.
15. **Finding 15 was fixed by `18aabf8d`.** The New York label rule now governs generated clock
    dates and timestamps, with the approved historical, citation, quotation, release, revision and
    name exemptions.
16. **Finding 16 was fixed by `18ddfbf7`; finding 16.9 remains a nondefect.** The timing updates
    correct the attribution, medians, ratio blanks, receipt prose, names and replacement extent.
    The new laptop update records the inferred `-04:00` offset and its approximately -04:01:05 to
    -03:58:09 bracket without claiming a recorded zone name.
17. **Finding 17 was fixed by `18ddfbf7`.** The September 14 review update now records the corrected
    remedy attribution and the supported disposition, source, reference and reproducibility
    shortcomings without rewriting the finished turns.
18. **Finding 18 was fixed by `18ddfbf7`.** The live speedup plan retains only the provenance gap
    for 37.7 MB and now gives the corrected commit set, baseline suite count, verification commands
    and recoverable record aliases.
19. **Finding 19 was fixed by `18ddfbf7` and `18aabf8d`; part 19.4 was already resolved at baseline
    `d3edadc6`.** The receipt update corrects the prose-system wording, and the remaining skill and
    plan prose removes the redundant “own”, fixes formatting and the drive path, numbers the three
    exemptions and names the intended works directly.
20. **Finding 20 was fixed by `18aabf8d`.** The review procedure now establishes windows from
    endpoint commits and corroborates pushes directly rather than treating commit-date queries as
    a completeness check.

The four affected hand-run generator modes all succeeded. Their eight tracked output changes were
not resolver regressions: they refreshed stale Sefaria and OSIS derivatives of the Wikisource
input change in `b5b15c01`, and `61aa48ee` records the inspected result. The final mega completed
all 54 steps, its MAM-parsed verification reported 79 passed, 0 failed and 1 pending, and it left
no tracked diff.

Verification passed: the filename lint reported 2 passed; the receipt, time-zone, prose,
post-stress-meteg, retirement-policy, dualcant-loader and mega-coverage group reported 13 passed;
the MAM-simple resolver matrix reported 2 passed; the operational retirement simulation exited
zero; repository standards passed; and the final full suite reported 1003 passed, 5 skipped and 1
warning. Every staged commit passed `git diff --cached --check`, and changed Python files passed
Black. The deployed user configuration was then checked against pushed
`origin/main@61aa48ee730a3cff222f28886298c6a06079586e` with
`USER_CONFIG_PROBLEM_COUNT=0`.

Product axis: the remediation reaches generated Sefaria and OSIS data through the eight inspected
refresh diffs in `61aa48ee`; the final mega added no product diff. Act axis: the substantive head
was backed up to the existing remote review branch, fast-forwarded to `main`, pushed and deployed
to the live user-configuration destinations. No issue changed, no history was rewritten and no
worktree was retired. The closing documentation commit still requires its planned backup,
fast-forward and final `main` push.

## Cleanup evidence disposition recorded on 2026-09-18

Recorded by Codex on 2026-09-18, New York time, before the cleanup task's planned removal of the
review worktree. The inventory found 4,295 files totaling 8,304,766 bytes under `.novc/`. Every
item has one of these prefix-complete dispositions:

- `codex-turn02-20260917/` (5 files, 9,519 bytes), `darp-2026-09-16/` (4 files, 31,347 bytes),
  `review-2026-09-16/` (286 files, 5,149,689 bytes), and `review-2026-09-16-turn03/` (52 files,
  958,952 bytes) are redundant review scripts, captures, reports, prompt copies and test output;
- `remeasure_filename_git_calls_2026_09_16.json` and
  `remeasure_filename_git_calls_2026_09_16.py` (2 files, 25,226 bytes together),
  `verify_review_history_2026_09_18.py` (1 file, 2,202 bytes), and `t/` (3,916 files,
  2,093,002 bytes) are reproducible measurement scripts and pytest or retirement-simulation
  temporary trees; and
- `hook-serialization-é/` (29 files, 34,829 bytes) is the inconclusive hook experiment. This
  entry preserves its lasting result and hashes; its isolated Git repository, config, helper
  scripts, sample hooks and captured diagnostics are disposable scratch after this entry is
  integrated.

The hook experiment ran under Codex `0.154.0-alpha.6.2` in ephemeral session
`01a0b49d-6169-7812-810b-c3f61ef0ef0e`. The no-bypass inventory exited zero and wrote
`INVENTORY` to both its last-message and stdout files, but its 904-byte stderr did not enumerate
every hook source. The approved stop rule therefore made the result inconclusive: no bypass,
capture, classification or subprocess harness ran, and no live or tracked hook changed. The
scratch evidence still matched these SHA-256 hashes immediately before disposition:

- experiment result:
  `CF5691ED43FB71D038355F14CE37366CB45E988E681F674B10AB8BC0BA10DDBD`;
- pre-inventory permitted-hook record:
  `316AB3227ED794834AF2CAA7D5B129983F8FAF0FC342CA8B260812069F08EB2D`;
- project hook definition:
  `A4611F9413EDA8C0FB5E9AE5FAAE175B1D9D32DC697E6660B06B0D573E7B9CD4`;
- capture helper:
  `A9BD2BF5B8381008913C56F8E388E8913BEB00CFED7A23356C2BF9FAE1F6F843`;
- inventory last message:
  `44E764C4A7DB9A4F8E25B2826D2DF39BD21670A30BD9C74ED108FA889A61584D`;
- inventory stdout:
  `8B5DB0AA4B11806BDC91BDB0D6606F988A58EFCC9204C9272732DC93AB56DC9E`;
- inventory stderr:
  `17EA4571B8D377642917804F1B6DDE855855520EB3C9C9B52AC0AFDF3CD40767`;
- live user hook definition:
  `5ACBD9978BFFB22944F93F48B71272741F9509CA3ADA7D2812A9D6B48EC90D2C`; and
- live hook command:
  `33C24422DBE49A07BBFA2A92407580FEA110E3274B8B80608D194221A1B4E0D4`.

Outside `.novc/`, `.pytest_cache/`, `.ruff_cache/` and every `__pycache__/` directory reported by
Git contain only reproducible tool caches and bytecode and are disposable with the worktree. The
access-restricted `.pytest_cache/` was inspected separately and contained only its three metadata
files and one pytest node-id cache. A second access-context inspection covered the restricted
`codex-turn02-20260917/pytest-temp/`, which contained one test-output Markdown file. The complete
tree had no junction, symbolic link or other reparse point, and no process other than the
inspection command named the exact worktree path. These facts permit ordinary non-forced removal
after this documentation commit is backed up, integrated and published.

Product axis: this cleanup entry reaches no repository product. Act axis: preserving the durable
evidence requires the ordinary review-branch backup, `main` fast-forward and push; later worktree
and local-branch removal dispose only the explicitly classified scratch and merged local state.
