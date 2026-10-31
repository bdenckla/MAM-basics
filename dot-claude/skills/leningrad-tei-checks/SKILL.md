---
name: leningrad-tei-checks
description: How to check Charles Loder's leningrad-codex-tei, the TEI encoding of the Leningrad Codex, against MAM-basics' Leningrad index, the UXLC change records and Sefaria's page images, and how to report what the check finds, to Ben, in MAM-basics' data and to Charles. Use when Charles's edition gains pages or Ben asks for it to be checked, before showing Ben evidence about a Leningrad page boundary or line, and before filing an issue in charlesLoder/leningrad-codex-tei.
---

# Leningrad TEI checks

Charles Loder's `charlesLoder/leningrad-codex-tei` encodes the Leningrad Codex as TEI, one file
per page under `edition/`, with every atom on its column and line. Its text is UXLC 2.5. Its page
boundaries are seeded from MAM-basics' `in/lci_recs.json`, at the MAM-basics commit its
`config.yaml` pins; an AI aligner, Gemini or a Claude agent, then places each page's atoms on the
lines of Sefaria's photograph and corrects the seed where a page's first or last atoms do not match
the image. A finding from the TEI is evidence about the TEI; a claim about the manuscript needs the
image.

## What each source is evidence for

- **The TEI's page boundaries** mostly repeat the index, so their agreement shows little. Where
  they differ, the aligner moved the seed. Charles's contributors, who could not open issues on
  MAM-basics, report such seed errors on
  https://github.com/charlesLoder/leningrad-codex-tei/issues/1076. Read it first: on 2026-10-31 it
  held six that MAM-basics had never received.
- **The TEI's lines** are the aligner's reading of the image. A column whose line count is unusual
  may have a blank line missing or added; check it against the image before using its numbers.
- **The UXLC change records' locators**, the page, column and line in
  `in/UXLC-misc/all_changes.json`, are human readings and make a sparse index that is usually
  right. They count only lines that hold writing, so below a blank line a locator's line number is
  smaller than a count of ruled lines; a few records also count a line of erased writing. Give
  such a line both ways, IB/NIB, as `hebrew-prose`'s terminology reference says. A line
  such as "1-2" is a range, and
  `py/uxlc_changes/uxlc_changes_loc.py` forces column 1 on F182A and F182B. Find a record's atom by
  its `reftext` as well as its position: the UXLC's positions count `<w>`, `<k>` and `<q>`, and an
  old record may predate a change to its verse.
- **The image** settles a disagreement: Sefaria's colour photograph,
  `https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F<page>.jpg`, roughly 3,800 pixels
  wide. Count every ruled line from the top of the column, and compare a doubtful line's height
  with the next column's lines.

## Atom numbers

The TEI's `xml:id` `f<page>-w-<n>` names atom `n` of a word stream built from UXLC 2.5 in
canonical book order, counting `<w>` and `<k>` but not `<q>`
(`src/leningrad_codex_tei/stages/word_stream.py` in Charles's repository). MAM-basics held UXLC 2.5
until `869234b2`, so `869234b2^:in/UXLC-39` rebuilds that stream. Within a verse, its numbering,
the index's and the UXLC's agree unless the verse has a ketiv, a qere or a samekh or pe inside it;
say which, when reporting a boundary. The TEI leaves out verses the UXLC marks as absent from the
codex, such as Josh 21:36–37.

## Viewing the images

Make crops as CSS windows onto Sefaria's images in a static HTML page under `.novc/`; nothing is
downloaded. The in-app browser renders a local file as a static snapshot in a new tab: give each
view a fresh file name, close the previous tab, and use neither a query string nor
`loading="lazy"`, which keeps the snapshot's images from loading. A grid of lines every 50 or
100 source pixels makes line heights comparable across columns.

## Reporting to Ben

- Show every text that needs his approval in the transcript itself, in full, and link every local
  file with a `file:///` link. Ben, 2026-10-31: *"I'm unlikely to look at things you don't give me
  links to or, even better, show right here in the transcript."*
- For a page boundary, give beside the crops the transcription's last line of the earlier page and
  first line of the later page, with the index's current break marked, for example by a red ✕.
  Leave out tables of the atoms around the break. Ben, 2026-10-31: *"these tables are almost
  useless"*.
- Caption each crop with its page, column and lines, and take Hebrew forms from the UXLC, the TEI or
  the change record, never retyped. Name a page "page F124B" or "F124B", never "folio 124B", as
  `hebrew-prose` says.

## Where each finding goes

- **A wrong boundary or an unnoted long column in the index:** a corrected `in/lci_recs.json`
  record, made after Ben approves, in a MAM-basics clone that the session's commander assigns. A
  layout note takes the shape "column 3 has 28 lines", counting blank lines. Regenerate with the
  mega steps that read the index, read every diff, and say in the commit what each regenerated file
  changes, as `cb878aef` and `05f51588` did. Then comment on issue 1076 with the commit's link.
- **A wrong UXLC locator:** an override copy under `uxlc/in/UXLC-misc-fixed/`, a byte-for-byte copy
  of the change list with only the corrected value changed, as `a961e13a` made, and an entry in
  that folder's `corrections.json`: the list, the record, the field, the UXLC's value, the corrected
  value, the line counted IB, whether the value is a reading or an estimate, and the evidence. The
  corrected line counts only lines holding text, NIB, as the UXLC's locators do.
  `py/tests/test_uxlc_misc_fixed.py` checks each copy against its original and the manifest, and
  `doc/uxlc-potential-corrections.md`, section 9, points to the folder.
- **An error in the TEI:** a new issue in `charlesLoder/leningrad-codex-tei`, the one tracker
  outside MAM-basics and MAM-private that takes new issues (`github-issues`,
  `references/reading-and-writing.md`, section 2, item 2). Keep it short and in that tracker's
  style, with a title such as "309B: pe marker on column 3 line 10", the authorship line, the page,
  column and lines, and the image's link. Ben approves each text before it is posted.

## Canonical copy

This skill is canonical at `MAM-basics/dot-claude/skills/leningrad-tei-checks/` and is shared with
Codex through `dot-claude/shared-skills.txt`. Change the canonical copy first, then use the
deployment procedure in `dot-claude/README.md`. A Claude cloud session can follow everything but the
image checks, which need network access to Sefaria and a way to view images.
