# Mapping UXLC 2026.04.01 Changes to book-of-job

## Overview

The 2026.02.05 changeset in `uxlc/in/UXLC-misc/2026.04.01 - Changes.xml`
contains 162 proposed changes to UXLC, all concerning the Book of Job.
These correspond to the "quirkrecs" (quirk records) maintained in the
retained book-of-job tree (`book-of-job/out/enriched-quirkrecs.json`),
which has 160 entries.

The script `py/main_map_changes_to_book_of_job.py` establishes and verifies
this correspondence. Run it from the repository root:

```
.venv/Scripts/python.exe py/main_map_changes_to_book_of_job.py
```

**This file is hand-authored prose, not a generated artifact.** Nothing
writes it — `DATA-LICENSES.md` says so explicitly — so it goes stale
silently whenever the changeset moves under it, and it cannot be brought
back into line by regenerating. Every figure below is one that command
prints, or one obtained by differencing two numbers it prints. The figures
this file carried until 2026-09-04 were measured against an earlier state of
the changeset; see "Why the earlier figures differed".

## Results

- **160 matched** by verse reference (all 160 quirkrecs have a
  corresponding XML change entry)
- **2 XML-only** entries with no quirkrec counterpart:
  - **#65 Job 19:16.6** — a "[Part 2 of previous change]" that is
    combined with #64 in the quirkrec.
  - **#71 Job 21:15.2** — a second entry for Job 21:15 (same verse as
    #70) that is combined in the quirkrec.
- **0 HTML-only** entries

## Deep comparison

Of the 160 matched pairs, comparing LC manuscript location, Hebrew text,
and semantic topic:

- **130 fully OK** — all fields match or are semantically compatible
- **30 line-number discrepancies** — see below

Those are the program's two buckets and they are exhaustive: it prints
`OK: 130` and `Issues: 30`, and all thirty issue blocks print an `LC LINE`
line and nothing else. No entry now fails on verse reference, on LC page or
column, on Hebrew text, or on semantic topic.

### The trailing space that used to make a thirty-first issue

Entry **#63 Job 19:16.2** used to print

```
** LC COL: xml=1  qr=1
```

with two spaces where the f-string has one, because its `<column>` element
is `"1 "` and the quirkrec's column is `1`. The two values agree; the
comparison did not. `parse_xml_entries` now reads `<folio>`, `<column>` and
`<line>` through a helper that strips the text, so #63 compares equal and
the issue count is 30 rather than 31.

The stray space is rare but real: across the 1398 changes of the seventeen
changes files under `uxlc/in/UXLC-misc/`, `<column>` has a trailing space
twice — 2024.07.08 #6 and 2026.02.05 #63, both `"1 "` — while `<folio>`
and `<line>` are clean in all 1398. The helper strips all three anyway,
because all three are compared the same way.

## Why the earlier figures differed

Until 2026-09-04 this section reported **128 fully OK**, **1 genuine content
mismatch** (#123, said to discuss נָשָׂ֨א rather than נִכַּר־), and **31
line-number discrepancies**. Those figures were correct when written, and
three things have changed since.

1. **The changeset was corrected upstream.** Entry #123 pointed at Job 34:19
   position 3; it now points at position 7, where its `reftext` is נִכַּר־
   and its quirkrec `3419-NKR0.html` agrees on verse, LC location, Hebrew
   text and topic. Entry #124 sits at position 8 with שׁ֭וֹעַ, which
   corroborates the numbering: נִכַּר־שׁ֭וֹעַ is one chanted word, and #123 and
   #124 point at its two atoms. Reconstruct the earlier state by setting
   #123's `pos` to `3` and its `reftext` to the atom standing there, and the
   program prints `OK: 128` and `Issues: 32` — the 32 being one `HEBREW`
   mismatch on #123 and the same 31 `LC` issues. So the earlier three
   categories were the program's two all along, with the 32 issues split by
   hand into #123 and the rest; #123 was never a judgment the program missed.
2. **The label on the 31 was wrong even then.** One of those 31 was #63's
   column comparison, described above, not a line number.
3. **The trailing-space fix moved one more entry into the OK bucket**,
   giving today's 130 and 30.

## Line number conventions

The two sources count manuscript lines differently:

| Convention | XML (UXLC) | Quirkrec (book-of-job) |
|---|---|---|
| Direction | Always top-down (positive) | Positive (top-down) or negative (bottom-up from line 28) |
| Blank lines | Not counted | Counted, with `including-blank-lines` field recording how many |

To convert quirkrec line numbers to the XML convention:

1. If negative: add 28 (e.g. `-2` becomes `26`).
2. If positive and `including-blank-lines` is set: subtract it.

After this normalization the 30 remaining discrepancies distribute as
follows, the delta being the quirkrec's normalized line minus the XML's --
both numbers printed on each `LC LINE` line:

| Delta | Entries | Count |
|---|---|---|
| -1 | #11, #52, #64 | 3 |
| +1 | #6, #7, #12, #26, #27, #36, #40, #46, #57, #67, #70, #77, #78, #91, #92, #97, #107, #141, #142, #143 | 20 |
| +2 | #13, #96, #115, #128 | 4 |
| +3 | #155, #156, #157 | 3 |

The 20 at +1 fit the reading that those quirkrecs are missing an
`including-blank-lines: 1` annotation; only 8 of the 160 quirkrecs have that
field at all, every one of them with the value 1, and just one of those 8
(#107) is among the 30. The 7 at +2 and +3 are consistent with pages having
more than one blank line. The 3 at -1 point the other way, and that reading
does not cover them.

## Known problems in the XML

These were identified during the comparison and review. The status column
was re-established against the changeset on 2026-09-04; five of the nine had
been fixed upstream since the review.

| Entry | Verse | Problem recorded at review | Status on 2026-09-04 |
|---|---|---|---|
| #65 | Job 19:16.6 | `lc_line` is None (sanity check failure) | **Fixed upstream.** `<line>` is `9`, and `uxlc/out/UXLC-misc/sanity_problems.json` regenerates as `[]` |
| #83 | Job 23:5.6 | Discusses a different maqaf than intended; the question is an Aleppo quirk, not relevant to UXLC | **Open.** Recorded here as position 5 until 2026-09-04; the entry is at position 6 |
| #98 | Job 29:3.5 | Description said "geresh-muqdam" where it should say whether the resh has a revia | **Fixed upstream.** The description is now "Examine possible revia on the resh." |
| #109 | Job 31:15.1 | Old encoding was fine; new encoding misuses ZWJ against the Unicode Standard | **Open, and no longer a change.** `reftext` and `changetext` are identical, and both have the ZWJ |
| #115 | Job 32:6.11 | Should use CGJ, not ZWJ, to control ordering (pre-existing problem) | **Open.** `reftext` and `changetext` are identical, and both have the ZWJ |
| #123 | Job 34:19.7 | Wrong atom discussed | **Fixed upstream.** Recorded here as position 3 until 2026-09-04; the entry is at position 7, whose `reftext` matches its quirkrec |
| #135 | Job 36:19.2 | Capitalization: "THe" | **Fixed upstream.** The description is now "Examine accent on the shin: dehi or tipeha.", and no description or note in the changeset has "THe" |
| #156 | Job 40:19.1 | Typo: "Examime" should be "Examine" | **Fixed upstream.** The description is now "Examine accent below the he: dehi or tipeha.", and no description or note in the changeset has "Examime" |
| #161 | Job 42:10.10 | Image link broken | **Not checkable from this data.** No change in the changeset has an image element; `<lc>` holds `<folio>`, `<column>`, `<line>` and `<credit>` only. The link belongs to UXLC's web presentation |

The ZWJ (U+200D) rows are the only two of the 162 whose `reftext` has one.
Four `changetext` fields have one: #35, #65, #109 and #115.

## Output files

- `uxlc/in/UXLC-misc/2026.04.01-map-to-book-of-job.json` — the mapping
  from XML change number to quirkrec HTML file. It carries no LC
  coordinates, so the trailing-space fix left it byte-identical.
- `uxlc/out/UXLC-misc/sanity_problems.json` — sanity check failures, written
  by `py/main_uxlc_check_changes.py`. It is `[]`; the `lc_line_is_none`
  failure on #65 that this file recorded until 2026-09-04 has been fixed
  upstream.
