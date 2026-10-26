# Updates to the plan to rewrite the MAM-for-Sefaria encoding page

State: open; first entries 2026-10-26.

These entries update
[PLAN-rewrite-MAM-for-Sefaria-encoding-page.md](PLAN-rewrite-MAM-for-Sefaria-encoding-page.md),
an executed plan whose text stays as it was executed.

## 2026-10-26: three pages, and the changes Ben asked for on review

Written by Claude (Opus 5.5) on 2026-10-26, in the session that executed the plan. Ben reviewed
the generated page before any Pages dispatch and gave these instructions, quoted verbatim:

1. "Relegate AJF documentation to its own page; don't even link to it from MAM-for-Sefaria
   documentation"
2. "Relegate documentation of "Unicode names" to its own file, but unlike the AJF documentation,
   do provide links to it from teh MAM-for-Sefaria documenation."
3. "Use an unordered list instead of an "in-sentence" ("inline") list after "Song spacing,
   MAM-simple's shirah-space, is in these chapters, with these numbers of spaces:""
4. "Use short references e.g. "Gen" not "Genesis""
5. "Instead of filling out all cells of the "Order" column, call it the "q first?" column and just
   put "q first" where that is true"
6. "Yank all of this:", followed by the rows of YERAH BEN YOMO, ATNAH HAFUKH, GERESH and GERESH
   MUQDAM of the table under "Code points that stand for more than one mark" and the paragraph
   after it, which begins "ATNAH HAFUKH and GERESH MUQDAM are only in poetic verses".
7. "Yank all of this:", followed by the rows of RAFE, UPPER DOT and LOWER DOT of the table under
   "Marks with code points of their own", then "replacing it with a row for ATNAH HAFUKH, saying
   something like "as opposed to YERAH BEN YOMO""

Ben also asked whether the class `mam-kq`, described as "a ketiv and its qere", should be "a ketiv
and/or a qere", and withdrew the question on seeing that "A ketiv velo qere, a ketiv that is
written but not read, is a span of class mam-kq-k with no pair around it". The description stays.

### What changed

- **Three pages.** `gh-pages/MAM-for-Sefaria/index.html` describes `csv/` and links to
  `unicode-names/index.html`, "The Unicode-name listings of MAM for Sefaria", which describes
  `misc/unicode-names/` and has the table of the 92 code points of `csv/`.
  `ajf/index.html`, "The AJF variant of MAM for Sefaria", describes `csv-ajf/` and
  `misc/unicode-names-ajf/` and links to the other two; neither of them names it or its folders.
  `py/author_misc/mam4sef_index.py`, `mam4sef_unicode_names_index.py` and `mam4sef_ajf_index.py`
  write them, sharing `mam4sef_common.py`; `py/main_authored.py gen-mam-for-sefaria-doc` and the
  mega step `mam-for-sefaria-doc` write all three. They share `styles.css` and its font copy, so
  the count of tracked Taamey D copies in `DATA-LICENSES.md` is unchanged.
- **The Ledger's R4,** "The page covers all four folders, `csv-ajf/` and the listings included",
  is superseded by instructions 1 and 2, and so is the outline's "**The files.** All four folders
  of 39 files each".
- **The outline's item 4,** "The code points whose mark depends on context, as MAM-for-Sefaria
  uses them: ZARQA, ZINOR, PASEQ, YERAH BEN YOMO, ATNAH HAFUKH, GERESH, and GERESH MUQDAM", now
  keeps only ZARQA, ZINOR and PASEQ (instruction 6), and its "QAMATS QATAN, HOLAM HASER FOR VAV,
  RAFE, UPPER DOT and LOWER DOT" is now QAMATS QATAN, HOLAM HASER FOR VAV and ATNAH HAFUKH, the
  last "as opposed to YERAH BEN YOMO" (instruction 7). `mam4sef_survey.py` no longer checks where
  a GERESH MUQDAM stands, which no page states now.
- **Short references** use the OSIS abbreviations of `py/mb_misc/osis_book_abbrevs.py`, with no
  period and a space after a leading numeral: Gen 2:5, 2 Sam 5:2. A reference quoted as a file
  writes it, such as a row's `Genesis 1:1`, keeps the file's form. A range within one chapter
  names the chapter once: Exod 20:2–6, 8–10 and 13–15.
- **Found while moving the AJF material:** the Sefaria page's "What the files leave out" counted
  "the 24 verses with two cantillations", a count of `csv-ajf/`'s rows, in BHS numbering; the item
  now gives no count. Nine listings of `misc/unicode-names-ajf/` end a `cant-bet` strand with a
  SPACE line that the CSV row lacks, because the strand ends with a samekh break and the CSV writer
  strips spaces from the end of a row's last field; the AJF page says so, and the survey now checks
  that each such listing is one of these.
- The survey's mark class is written with named escapes, matching exactly the code points it had.

### Verification

`py/main_authored.py gen-mam-for-sefaria-doc` twice, with identical output; Black and Ruff on the
changed Python; `git diff --cached --check`; the eleven test files of the plan's "Verification"
item 3, 47 passed; and `py/tests/source_hygiene_test.py`, `py/tests/test_accent_marks_source.py`
and `py/tests/test_prose_mark_order.py`, 12 passed. The three pages were read in full. The mega
and the suite are left to the nightly run, per `doc/review-trial.md`. The Pages workflow was not
started; publication waits for Ben's go-ahead.

## 2026-10-26, later: the normalized column, and unpointed Hebrew

Written by Claude (Opus 5.5) on 2026-10-26, in the same session. Ben's next two requests, quoted
verbatim:

1. "I don't think we need the "Normalized without the CGJ" column in any of the three tables in
   which it appears."
2. "Again and again and again you but unpointed Hebrew words in pointed-Hebrew styling. Please do
   not, in "638 are in atoms spelled ירושלם (634) or ירושלמה " and elsewere in this document (I'm
   not sure if there are other cases elsewhere in this document: I think there's an inverted nun
   case, which similarly should just be left in the surrounding (default) font)"

### What changed

- **The column** is gone from the three tables that had it, all on the Sefaria page: the
  Jerusalem table and the two tables under "Two strands on one letter". So is the clause of the
  "Robust Unicode" paragraph that described it, "and the order that normalization would give
  them without the CGJ". The AJF page's strand tables never had the column. The survey still
  checks that normalization would reorder the marks of each letter that has a CGJ, which the
  paragraph still states.
- **Unpointed Hebrew in prose** is in the surrounding font, isolated for its direction in a
  `<bdi>`: the two Jerusalem spellings and the NUN HAFUKHA on the Sefaria page, the letters of
  the attention-color convention on the Sefaria and AJF pages, and the four strand names on the
  AJF page.
- **Unpointed Hebrew in an example** was too, in `658ffef3`, until the next entry put each
  example back in one font. A lifted ketiv, samekh or pe break, or inverted nun stayed in the
  surrounding font, and the pointed rest of its cell went in `lang="hbo"` spans: the
  classification of `py/accgram/almost_errors_html_shared.py`'s `wrap_hebrew_runs`, which the
  `hebrew-prose` skill's rendered-prose reference names for unpointed Hebrew. For that commit,
  `styles.css` moved the line height of `td[lang="hbo"]` to every `td[dir="rtl"]`; its header
  comment now names the three pages.
- **A guard:** `py/author_misc/mam4sef_common.py`'s `write_page` refuses a page that has an
  unpointed Hebrew token under `lang="hbo"`, now only in prose (the next entry). A token of
  punctuation alone is allowed.

### Verification of these changes

`py/main_authored.py gen-mam-for-sefaria-doc` twice, with identical output; Black and Ruff;
`git diff --cached --check`; the fourteen test files above, 59 passed. A scratch check of every
Hebrew token on the three pages, joined across inline elements, found no pointed token outside
`lang="hbo"` and no unpointed word inside it. The mega and the suite are left to the nightly
run. The Pages workflow was not started.

## 2026-10-26, later still: each lifted example in one font

Written by Claude (Opus 5.5) on 2026-10-26, in the same session. Told that the change above set a
lifted ketiv in another font than its qere, and that one font for a lifted example would be a
small change, Ben replied, verbatim: "keep those in one font (namely the font for pointed
hebreW)".

So each table cell that holds a form lifted from the files is again `lang="hbo"` throughout, its
ketiv, breaks and inverted nun included, and `styles.css` has its line height on
`td[lang="hbo"]` again. Unpointed Hebrew in prose stays in the surrounding font, and the guard in
`write_page` now exempts the cells of lifted forms.

Verification: `py/main_authored.py gen-mam-for-sefaria-doc` twice, with identical output; Black
and Ruff; `git diff --cached --check`; the fourteen test files, 59 passed. The scratch token check
found unpointed Hebrew under `lang="hbo"` only in lifted forms, and none in prose. The mega and
the suite are left to the nightly run. The Pages workflow was not started.

## 2026-10-26: Ben's review is finished

Written by Claude (Opus 5.5) on 2026-10-26, in the same session. Ben finished reviewing the three
pages as of `fab8bd0a` and asked for no further change, writing, verbatim: "I'm satisfied with all
three pages, mainly because I don't care that much about the AJF page or the abbreviations." Of
the Pages dispatch he wrote, verbatim: "Will handle that separately, perhaps leaving to nightly".

As of this entry no dispatch has been made, so the site does not yet have the three pages:
`.github/workflows/pages.yml` runs only when dispatched, and the nightly checks of
`doc/review-trial.md` dispatch no workflow.

State of the plan: executed 2026-10-26, as revised here.
