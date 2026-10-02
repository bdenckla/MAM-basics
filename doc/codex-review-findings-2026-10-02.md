# Codex findings of the 2026-10-02 review of MAM-basics since 2026-09-29

State: completed 2026-10-02; review only

Written by the independent Codex reviewer at xhigh (extra high) effort in
`C:/Users/BenDe/GitRepos3/MAM-basics`, a full clone on `main`. The reviewed endpoint is
`db59ef5e22bbfb60dce7d398c63b837d98a74339`; the kickoff procedure was read at
`699c7b173d423187a1198e36aa94413763c47de0` and again after synchronization at
`c23d852245a4f8829db713081df60cae53e306bf`. The kickoff commit is an ancestor of the
report checkout. Three bounded delegated reviews covered Phonetic MAM, parser and
survey changes, and Yeivin ITM and documentation. The root reviewer reconciled their
results and checked the supporting scripts and artifacts.

Ben paused the review while the machine was busy, then explicitly resumed it on
2026-10-02. The interrupted suite run is not counted as a passing result. Neither
this session nor its delegates opened the current Claude report or an account of
that review. No remediation was performed. The kickoff owner in
`C:/Users/BenDe/GitRepos2/MAM-basics` owns verification of findings, dispositions and
remediation.

## Scope, anchors and census

The window is MAM-basics
`7549ebf706ca6a098478fe0ea5e6a8cfd90866c0..db59ef5e22bbfb60dce7d398c63b837d98a74339`,
reviewed as an endpoint diff, not as a collection of intermediate commits. The diff
changes 1,533 paths, with 1,334,327 insertions and 6,012 deletions. A no-renames path
census includes 1,025 paths under `gh-pages/`, 285 under `py/`, 80 under `doc/`,
42 under `Phonetic-MAM/`, and three under `Yeivin-ITM/`.

The exact evidence-only boundary is kickoff item 4 in
[dual-agent-review.md](dual-agent-review.md), “The MAM-basics trial review, kicked
off 2026-10-02”: the specified 22 earlier-round records, the named relay software
and relay-only hunks, and the automated-relay procedure passages. Earlier rounds'
remediation of other code, data and documents remains subject. Other records changed in the
window were not silently excluded. Sibling repositories supplied inputs to checks;
their changes are not additional review windows.

Window files were read at the end commit. At `699c7b17`, the checkout differed from
that endpoint only in the trial procedure. After synchronization, two book-of-Job
source files and associated products also postdated the endpoint; current-tree
checks below do not establish the frozen versions of those files.

## Tree health at c23d852245a4f8829db713081df60cae53e306bf

Python checks used this full clone's `./.venv/Scripts/python.exe` from its root.

| Check | Commit and inputs | Result |
| --- | --- | --- |
| Endpoint `git diff --check` | Frozen start/end pair; no siblings | Passed. |
| `py/main_phonetic_mam.py check` | `699c7b173d423187a1198e36aa94413763c47de0`; public inputs only | Passed. |
| Exhaustive public analysis-reader check | Same commit; public inputs only | All 263,320 Sephardic readings exposed by the analysis reader, including its alternative branches, decoded and supplied syllables, stress positions and scanner forms without failures; reconstructed syllable counts matched the displayed transcriptions. |
| `py/main_yeivin_itm.py check` | Same commit; public inputs only | Passed. |
| `py/main_test.py py/tests/test_meteg_before_stress.py -q` | Same commit; public inputs only | Three passed; pytest cache access warning. |
| `py/main_parse.py ws-products --output-dir .novc/review-surveys-parser-20261002` | Same commit; public inputs only | All 24 candidate book-group JSON files byte-identical to tracked `MAM-parsed/plus/`. |
| `py/main_accgram.py survey-breuer-zaqef-units --json-out .novc/review-surveys-breuer-20261002.json` | Same commit; public inputs only | Completed; joins and declared exceptions inspected. |
| `py/check_html_syntax_and_sanity.py` for `gh-pages/phonetic-mam` and `gh-pages/yeivin-itm` | Same commit; no siblings | Both passed. |
| Changed Markdown link audit | Frozen endpoint; no siblings | All 17 new or changed relative file targets resolve, from 93 subject Markdown files scanned. No heading-fragment links occurred in that set. |
| `py/main_test.py -q` | `c23d852245a4f8829db713081df60cae53e306bf`; synchronized siblings below | 1,056 passed, five skipped, 60 subtests passed in 862.81 seconds. |
| `py/main_0_mega.py` | `c23d852245a4f8829db713081df60cae53e306bf`; synchronized siblings below | Passed: 57 steps in 611.2 seconds; no tracked diff. |

Before sibling-reading checks, `py/main_repo_util.py --sync-forest $HOME/GitRepos3
--check` identified clean clones behind origin; the same command without `--check`
fast-forwarded eligible clones and reported zero problems. The earlier suite attempt
at `699c7b17` read MAM-private `1313c9ba76b2c2a9a3d693f622ec646e8afe5e92` and
hbofonts `6eb3ee0e9b89addefdb4752abbc7cd2e86b0f065`; that attempt was interrupted.
The resumed suite read MAM-private
`b69906915dc724f743a291b30149fdb3052b5938` and hbofonts
`6eb3ee0e9b89addefdb4752abbc7cd2e86b0f065`. A fresh forest check before the mega
reported zero problems; the mega read those same sibling commits.

The five skips are the declared edition-transcription controls for pages that
diverge from their Wikisource strand; the separate grammaticality checks cover
those pages. The mega was launched with `PYTHONUTF8=0` and `PYTHONIOENCODING`
unset so account settings could not mask an implicit output encoding.

The suite and mega changed no tracked files in this clone, and the siblings
remained clean. The parser and Breuer candidate outputs were written only under
ignored `.novc/`. No check-generated tracked change required restoration. The
report is the only file committed by this session.

## What verifies sound, stream by stream

- **Phonetic MAM migration.** Reviewed the closed release and token validators,
  independent frozen-HTML projection, read-only computation interface, exporter,
  unified renderer, public analysis reader and preparation boundary. The public
  corpus checks and exhaustive decoding found no introduced defect. Pronunciation
  selection, fallback behavior, query/fragment preservation and separate example
  pages were examined in source; browser acceptance recorded by the window was not
  repeated by this review.
- **Parser and public analyses.** Inspected recognized-template dispatch and the
  conversion of public consumers to the tracked display release. Regenerated parser
  products matched their committed bytes. The post-stress survey's endpoint changes
  preserve its numeric census and classification while replacing annotated forms
  with publicly displayed forms. The Breuer survey's MAM join gap at Deuteronomy
  32:6 is an already-declared grouping mismatch; the survey keeps MAM and WLC 4.22
  joins separate, and WLC 4.22 join differences were not promoted into MAM defects.
  Combined vowel and stress alternatives remain
  explicitly selected.
- **Yeivin ITM.** Reviewed claim projection, substitution validation, selected
  content, assets and rendering. The revised pre-stress claim is supported by the
  public analysis and mechanical claim check. The selected adaptation remains
  distinct from the full source; no claim of independent full-source verification
  is made here.
- **Redirects, fonts and product boundaries.** Checked the closed redirect target
  variants, frozen 1,959-path Phonetic manifest, target paths and anchors, legacy
  pronunciation queries, support assets and source identities. The font's same-host
  support mapping accompanies the copied font. Product scopes and mega registration
  agree with the new public products and the exporter-only private dependency.
- **Maintenance and portable execution.** Reviewed forest synchronization's clean
  fast-forward eligibility, subprocess bounds, worktree-retirement timeout changes,
  public/private path helpers and Windows UTF-8 entry-point changes. No substantive
  introduced defect was established. Actual clone retirement, configuration
  deployment and relay operation were not performed.
- **Instructions and other documentation.** Read subject changes independently of
  the evidence-only records, checked scope and command contracts, and audited new
  relative links. The trial's precedence clause resolves the retained older review
  procedures.

Minor wording note, not a finding: `doc/phonetic-mam-preparation.md`'s “remain separate steps” is ambiguous about cutover status, but does not contradict “accepted Pages redirects” in `dot-claude/skills/mam-repository-topology/references/evacuated-repositories.md` or establish unfinished deployment.

## Findings

No actionable introduced defect was established. The publication-status wording
candidate was not retained for the reason above; no remediation is proposed by
this report.

## Open ends the window itself declares (not findings)

- `doc/phonetic-mam-preparation.md`, “Font support”, explicitly says an exact font
  rebuild has not been established. The frozen font and support package are present;
  their presence does not establish reproducibility of the font build.
- The private source adapter remains a migration dependency for calculation and
  example generation. Moving public consumers to the release does not complete
  private retirement.
- `doc/PLAN-deferred-template-projection-decisions.md` leaves identified survey
  population decisions paused. This review did not choose replacement semantics.
- `MAM-for-Sefaria/` and `MAM-OSIS/` may lag MAM-simple after text refreshes under
  the exceptions their READMEs declare.

## What this review did not check

The review did not inspect the current Claude review, review sibling changes as
subject, re-review the excluded relay, perform remediation, or operate live
Wikisource or redirect hosts. It did not independently verify live deployment,
repeat browser interaction and printing checks, establish an exact font rebuild,
compare every historical frozen legacy page visually, or inspect manuscript images
and full private OCR. Corpus evidence here concerns MAM, its public display release
and the explicitly named comparison text; it is not a new manuscript reading.
Post-window book-of-Job edits are outside the frozen window even when current-tree
checks exercise them. The operational worktree-retirement simulation is outside
the default suite and was not run.
