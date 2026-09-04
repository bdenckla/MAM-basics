# Codex Design A review of the 2026-09-04 public-repository window

State: not acted on. Written untracked at
`.novc/codex-review-findings-2026-09-04.md` on Ben Denckla's 2026-09-04
instruction not to write a tracked file while another task was active, then promoted
to this tracked path after Ben reported that task paused and asked for the review to
be committed. This is the Codex half of the first dual-agent review under
`doc/dual-agent-review.md`. It is not the reconciliation and does not alter the
Claude findings.

## Scope and method

This is Design A from `doc/dual-agent-review.md`: I read
`doc/review-findings-2026-09-04.md`, re-derived selected claims from immutable Git
objects, and inspected the same local public-clone ranges. The primary range was
MAM-basics `4cc0c33..b4706759`. The other existing local public clones inspected
were MAM-parsed `46209cd..5108203`, MAM-simple `cd2bef8..7a4f21d`, MAM-with-doc
`999a437..0fe406c`, MAM-for-Sefaria `cf193470..ce1e04c`, MAM-OSIS
`2f783d1..697dc98`, codex-index-leningrad `2abd7f6..86f88c0`, and Taamey_D
`4a3c836..3813499`.

No worktree, review forest, clone, checkout, or test run was created. The absent public
source clones book-of-job, holman-ketiv-qere, UXLC-utils, codex-index-aleppo, and
codex-index-cam1753 were not recreated or inspected remotely. The review therefore
does not independently re-derive claims that require those source clones. I did not
read MAM-private, github-misc, or hbofonts.

## Finding 1: the redirect-manifest test is not automatically run

`py/tests/test_redirect_manifest.py:8` says that its check was moved into "a suite
that runs all the time." That is false: MAM-basics' only workflow,
`.github/workflows/pages.yml`, deploys the existing `gh-pages/` directory and runs no
Python test command. The test runs only when a person invokes `py/main_test.py`.

The wording entered in `b6bb8fae`, inside the reviewed range. The false claim does
not make the test incorrect, but it misstates the test's protection: a stale redirect
manifest can persist until someone elects to run the suite. Replace "runs all the
time" with wording that says the check runs whenever the repository test suite runs.

## Claude findings re-derived directly

No directly checked claim in the Claude report was false. Four code-level findings
are confirmed at MAM-basics `b4706759`:

1. `mam_suggestion_extract._parse_prose_list()` silently skips a heading whose book
   abbreviation is not in `STD_BOOK_NAME_BY_HOLMAN_ABBREV`, despite the table's stated
   fail-closed purpose.
2. `main_0_mega._refuse_if_sibling_writes_are_misdirected()` tests only
   `cwd_relative.is_dir()`. An existing non-clone directory satisfies the guard,
   contradicting the docstring's statement that a non-clone destination is refused.
3. `osis_runner._xsd_parser()` accepts any non-None `xml_xsd_path` without first
   checking that the path names a file.
4. `test_versification_and_cantillation_doc.py` builds `_CURRENT_DOC_PATH` through
   `paths.sibling_repo("MAM-simple")` at module scope, without `require_sibling`.
   A missing MAM-simple clone therefore fails at collection rather than giving the
   standard missing-sibling advice.

## Static checks that found no additional defect

The 147 changed MAM-basics Python files add no `sys.path` mutation. Every added
`open`, `Path.read_text`, or `Path.write_text` call specifies an encoding. `git diff
--check` was clean for changed Python source in MAM-basics, MAM-parsed, MAM-simple,
and Taamey_D.

## Repository state during the review

MAM-parsed, MAM-simple, MAM-with-doc, MAM-for-Sefaria, MAM-OSIS,
codex-index-leningrad, and Taamey_D were clean on `main` when checked. MAM-basics had
a pre-existing `DATA-LICENSES.md` modification at the start. MAM-basics then advanced
concurrently through the diffable-pointed-hebrew evacuation and was clean immediately
before this report was promoted. The review's disposable scan remains ignored at
`.novc/codex_review_scan.py`.
