# Codex Design A review of the 2026-09-07 public-repository window

State: completed 2026-09-08. This is the Codex half of the second dual-agent review
under `doc/dual-agent-review.md`. It checks selected claims in
`doc/review-findings-2026-09-07.md`; it does not replace Claude's report or determine
the later dispositions.

## Scope and method

The review uses Design A. Its MAM-basics range is `b4706759..8bf586a3`, the range frozen
in the Claude report. I re-derived selected claims from immutable objects at `8bf586a3`,
using `git show`, `git grep`, and the read-only scratch script
`.novc/codex_review_2026_09_07.ps1`. The script reports 257 commits, 220 non-merge
commits, and zero newly added `sys.path` mutations. `py/main_test.py --collect-only -q`
in the clean current checkout collected 981 tests.

I kept the public-only scope. I did not inspect MAM-private, hbofonts, the contents of
the Recycle Bin, private-source records, or the absent public source clones. I did not
run a generator that writes tracked artifacts in place. The primary checkout was clean
on `main` at `05932601` when the review started. That checkout contains the six
post-anchor commits the Claude report excludes; their diff has exactly the thirteen
paths the report names, so no excluded path entered the re-derivation accidentally.

## Claude findings re-derived directly

No claim in this selected set was false.

1. **Finding 1:** `get_verse_words()` reads a scribal-difference target's `text`
   attribute or a nested `slh-word`, but does not read a nested `<text>` sibling.
   Deuteronomy 32:6 has the exact shape the report identifies: a suspended-letter
   element followed by the omitted text element.
2. **Finding 4:** `main_letter_small_job.py` passes `mam_simple_dir() / "Job.xml"` to
   the reader, while `mam_simple_dir()` resolves to MAM-simple's `json-vtrad-bhs/`
   directory. That directory contains JSON, so the required XML path cannot exist.
3. **Finding 5:** `git grep` at the anchor finds 716 old MAM-with-doc URLs. Removing
   the report's stated record and byte-verbatim data locations leaves exactly 669 hits
   in generated artifacts.
4. **Finding 7:** the redirect program defines `_DEFAULT_REPO` as
   `REDIRECT_REPOS[0]`; at the anchor, the first row is MAM-simple. The default is
   therefore table-order dependent and conflicts with the wlc-utils wording the report
   names.
5. **Findings 8.1 and 8.2:** the central NFC test excludes both `MAM-simple/` and
   `gh-pages/`, while the MAM-simple mark-order test obtains files with `git ls-files
   -- MAM-simple`. The generated MAM-simple page and its generator's Hebrew are outside
   both checks.
6. **Finding 13.1:** the type-3 page definition says final, but the structural
   classifier tests closure and tsere without testing finality. The code's invariant
   may exclude a non-final record today; the definition and classifier still differ.
7. **Findings 14.1 and 14.2:** `DATA-LICENSES.md` names neither `gh-pages/img/` nor the
   deploy-root post-stress-meteg pages, so the two documented coverage gaps are real.
8. **Finding 15:** `misc/linux-sh/repos-minus-MAM-basics.txt` is a second roster and
   `linux-clone.sh` consumes that file. The roster still names MAM-OSIS and the landed
   MAM-simple product.
9. **Finding 18:** `doc/dual-agent-review.md` says the Codex instruction file has 998
   lines and says a reviewer has no reason to write, even though Design A requires
   Codex to write the reconciliation. The tracked instruction copy had 1,077 lines on
   2026-09-08, so the count remains stale as well as internally inconsistent.

## Static checks that found no additional defect

The review found no new defect in its selected static pass. The review-window commit
census matches the Claude report, no `sys.path` mutation was added in the MAM-basics
Python diff, and the six commits after the anchor change only the thirteen declared
paths. These checks do not certify the claims outside the nine re-derived items above.

## Limits of the Codex review

The Codex review did not independently check Claude findings 2, 3, 6, 8.3–8.4, 9–12,
13.2–13.3, 14.3–14.6, 16–17, 19–24, or the unselected subclaims of findings 1, 4, 5,
7, 8, 13, 14, 15, and 18. The selected review did not uncover an omitted commit or a
new defect. That is a result of the selected checks, not a claim that the window has no
other defect.
