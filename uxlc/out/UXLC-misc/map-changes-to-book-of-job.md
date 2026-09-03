# Mapping UXLC 2026.04.01 Changes to book-of-job

## Overview

The 2026.02.05 changeset in `in/UXLC-misc/2026.04.01 - Changes.xml`
contains 162 proposed changes to UXLC, all concerning the Book of Job.
These correspond to the "quirkrecs" (quirk records) maintained in the
sibling `book-of-job` repo (`out/enriched-quirkrecs.json`), which has
160 entries.

The script `py/main_map_changes_to_book_of_job.py` establishes and verifies
this correspondence.

## Results

- **160 matched** by verse reference (all 160 quirkrecs have a
  corresponding XML change entry)
- **2 XML-only** entries with no quirkrec counterpart:
  - **#65 Job 19:16.6** — a "[Part 2 of previous change]" that is
    combined with #64 in the quirkrec. Also flagged in
    `out/UXLC-misc/sanity_problems.json` as `lc_line_is_none`.
  - **#71 Job 21:15.2** — a second entry for Job 21:15 (same verse as
    #70) that is combined in the quirkrec.
- **0 HTML-only** entries

## Deep comparison

Of the 160 matched pairs, comparing LC manuscript location, Hebrew text,
and semantic topic:

- **128 fully OK** — all fields match or are semantically compatible
- **1 genuine content mismatch** — #123 Job 34:19.3 discusses the wrong
  word (`נָשָׂ֨א` instead of `נִכַּר־`)
- **31 line-number discrepancies** — see below

## Line number conventions

The two sources count manuscript lines differently:

| Convention | XML (UXLC) | Quirkrec (book-of-job) |
|---|---|---|
| Direction | Always top-down (positive) | Positive (top-down) or negative (bottom-up from line 28) |
| Blank lines | Not counted | Counted, with `including-blank-lines` field recording how many |

To convert quirkrec line numbers to the XML convention:
1. If negative: add 28 (e.g. `-2` becomes `26`)
2. If positive and `including-blank-lines` is set: subtract it

After this normalization, most remaining discrepancies are off-by-one
(26 cases), suggesting that many quirkrecs are missing
`including-blank-lines: 1` annotations. A few have larger deltas
(+2 or +3), likely pages with multiple blank lines.

## Known problems in the XML

These were identified during the comparison and review:

| Entry | Verse | Problem |
|---|---|---|
| #65 | Job 19:16.6 | `lc_line` is None (sanity check failure) |
| #83 | Job 23:5.5 | Discusses a different maqaf than intended; issue is an Aleppo quirk, not relevant to UXLC |
| #98 | Job 29:3.5 | Description says "geresh-muqdam" but should mention whether there is a revia on the resh |
| #109 | Job 31:15.1 | Old encoding was fine; new encoding misuses ZWJ against Unicode Standard |
| #115 | Job 32:6.11 | Should use CGJ not ZWJ to control ordering (pre-existing problem) |
| #123 | Job 34:19.3 | Wrong word discussed (`נָשָׂ֨א` instead of `נִכַּר־`) |
| #135 | Job 36:19.2 | Capitalization issue: "THe" |
| #156 | Job 40:19.1 | Typo: "Examime" should be "Examine" |
| #161 | Job 42:10.10 | Image link broken |

## Output files

- `in/UXLC-misc/2026.04.01-map-to-book-of-job.json` — the mapping
  from XML change number to quirkrec HTML file
- `out/UXLC-misc/sanity_problems.json` — sanity check failures
  (entry #65 `lc_line_is_none`)
