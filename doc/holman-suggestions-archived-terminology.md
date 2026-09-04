# Note: rename the reader-facing word "Suppressed" to "Archived" on the Holman findings pages

Evidence for the seven-item programme
[`PLAN-holman-meteg-rollout-programme.md`](PLAN-holman-meteg-rollout-programme.md). The rename it
describes is Phase 4 of that programme's item 1, planned in
[`PLAN-post-stress-meteg-page-and-holman-m23.md`](PLAN-post-stress-meteg-page-and-holman-m23.md);
it is NOT part of item 6, which archives the thirty records themselves.

Captured 2026-09-03 in a plan-mode session of MAM-basics (`C:/Users/BenDe/GitRepos/MAM-basics`,
HEAD `3829585`), one of a set of six notes written under `C:/Users/BenDe/.claude/plans/` because
concurrent work in git-tracked areas had not concluded. All six were moved into `doc/` on
2026-09-03.

**Status, 2026-09-04: THE RENAME HAS BEEN DONE, and this paragraph said "the
rename itself is not yet done; no edit has been made" until now.** It was
applied on 2026-09-03 as Phase 4 of
[`PLAN-post-stress-meteg-page-and-holman-m23.md`](PLAN-post-stress-meteg-page-and-holman-m23.md),
whose "Phase 4 done 2026-09-03" section is the execution record and reports both
renames applied with the per-row ketiv/qere vocabulary untouched. The
reader-facing strings live in `py/py_render/rt_html.py` as `SUPPRESSED_NAV_LABEL`,
`SUPPRESSED_PAGE_TITLE` and `SUPPRESSED_PAGE_HEADING`, whose `SUPPRESSED_*`
NAMES were deliberately left alone; what changed is their values.

**Path note, 2026-09-03:** the Holman review moved out of the separate `holman-ketiv-qere`
repo into `MAM-basics/holman/` (data) and `MAM-basics/gh-pages/holman/` (rendered pages)
during this session, in a concurrent session; `holman-ketiv-qere`'s clone is gone from
`GitRepos` and the GitHub repo is now a redirect host. This note is written against the new
location throughout; it originally cited the old one.

## Ben's decision, 2026-09-03

The word shown to readers on `MAM-basics/gh-pages/holman/table_data_findings_suppressed.html`
is to change from **"Suppressed"** to **"Archived"**. "Archived" means, roughly, handled: the
suggestion was accepted, rejected, or partially accepted, and the page does not classify
beyond that coarse resolution. That is the meaning the page's subtitle already gives
("Handled: accepted, rejected, or something in between", Ben's decision of 2026-09-02, recorded
at `py/py_render/rt_html.py` lines 63–66); only the one-word label changes.

**Scope is the rendered text, at least.** The filename `table_data_findings_suppressed.html`
may stay as it is, and internal names in the code (function names, variable names, the
`is_suppressed` predicate, `suppressed_output_path`, the `SUPPRESSED_*` constants' names) may
stay as they are. Ben left both open rather than requiring them to change.

## Where the word is rendered

All the reader-facing strings live in `py/py_render/rt_html.py`, as module constants and one
literal, so the change is confined to that file:

| site | current value | line (2026-09-03) |
|---|---|---|
| `SUPPRESSED_NAV_LABEL` | `"Suppressed"` | 44 |
| `SUPPRESSED_PAGE_TITLE` | `"Holman k/q - Suppressed"` | 55 |
| `SUPPRESSED_PAGE_HEADING` | `"Suppressed"` | 57 |
| `records_heading=` literal in the suppressed-page render call | `"Suppressed Records"` | 165 |

Those four produce the six occurrences in the published pages: the `<title>`, the nav link
label on both pages, the `<h1>`, and the "Suppressed Records" section title. The redirect
script in `table_data_findings.html` (line 12) and the nav `href` name the FILE, and stay.

**Correction, 2026-09-03: the numeral "six" in the paragraph above HAS BEEN MEASURED AND IS
WRONG — the count is five**, which is what the enumeration beside it already adds up to and
what the programme document and its item 1 plan both say. Counted that day over the two
published pages: `gh-pages/holman/table_data_findings.html` has one, the nav link at line 23;
`gh-pages/holman/table_data_findings_suppressed.html` has four, the `<title>` at line 16, the
nav link at line 23, the `<h1>` at line 25 and the "Suppressed Records" section title at line
90. The four render sites in the table above are unaffected — the slip is in the total, not in
the list of what to edit.

Two comments in the same file say "the Suppressed page" (lines 58 and 250) and one in
`py_render/rt_mam_suggestion_card.py` (line 205) says the state is "suppressed" for every
ruling; those are prose about the code and can be updated to match or left, at the
implementer's discretion, since the code names are allowed to keep the old word.

## How to carry it out

1. Edit the four sites in `py/py_render/rt_html.py` (line numbers reconfirmed 2026-09-03,
   after the Holman migration into MAM-basics: 44, 55, 57, and 165 for the
   `records_heading="Suppressed Records"` literal — that same call site's sibling at line 145
   passes `records_heading="Records"` for the main page, unaffected).
2. Regenerate the pages with the real command. Two entry points exist post-migration:
   `py/main_just_render_table.py` (the original, still present) and the newer
   `py/main_verify_and_render_table.py` (adds verification against `../MAM-parsed` and
   `../UXLC-utils`); check which is current practice at execution time and use that one.
   Read the diff of `MAM-basics/gh-pages/holman/table_data_findings.html` and
   `table_data_findings_suppressed.html`: exactly the six "Suppressed" occurrences should
   change and nothing else.
3. Run black on the edited file; commit and push MAM-basics — its own `.github/workflows/pages.yml`
   now deploys `gh-pages/` on push to `main`, which is what serves the public Holman pages.
   There is no second repo to push: `holman-ketiv-qere` no longer holds the data or the
   render, only a redirect stub.
