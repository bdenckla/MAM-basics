# The review of the Israel Bible: its inputs and records

State: live

This folder holds the inputs of Ben's review "The Israel Bible: this ain't no Koren edition".
[`py/author_misc/israel_bible_review_index.py`](../../py/author_misc/israel_bible_review_index.py)
renders them as `gh-pages/israel-bible-review/index.html`, in the review's own folder of the
site, which the site index lists under "Reviews". The review is edited here, in MAM-basics.

## The inputs

- [`review.md`](review.md) is the review's text in Markdown: its prose, its footnotes, and two
  data tables. The table headed `| Verse | Page | Israel Bible | MAM | Note |` holds the rows
  of the tour ("A sampling of quirks") whose notes are Markdown; the module draws them among
  the tour's tables, which stand where the marker `<!-- weird-pointing -->` stands. The table
  headed `| Verse | Page | Israel Bible | MAM's עליון | Note |` holds the Decalogues' rows and
  is drawn where it stands. The module raises on a table with any other headers.
- [`forms.json`](forms.json) holds the forms of the tour's other rows, whose notes are in the
  module, in `TOP`, `TRANSLIT` and `NEXT`. Each row has its verse (`reference`, as
  "Book chapter:verse"), its `page` in the Israel Bible, the Israel Bible's form
  (`israel_bible`) and MAM's form (`mam`). A row whose entry in `TOP` names a `label` has that
  label too: only 2 Kings 18:27's row has one, `Separate`, and its two forms are of the
  verse's qere. Each form is as the page shows it: stripped as the module's `stripped` strips
  it, with MAM's rafeh on the alef kept at the rows of the module's `RAFEH_REFS`, and in
  MAM-normal mark order. The rows are in the Israel Bible's order, by page, then chapter and
  verse. The module checks all of this, and that its entries draw every row once.
- The page's styles are
  [`py/author_misc/israel_bible_review_index.css`](../../py/author_misc/israel_bible_review_index.css),
  which the module publishes beside the page as `style.css`.
- The page's one image, a crop of Deuteronomy 3:22's atom from page 457 of the Israel Bible's
  PDF, is
  `gh-pages/israel-bible-review/img/Deut 3v22 FYRAV6 -- Israel Bible PDF page 457.png`.
  `review.md` names it `img/deut-3-22-word.png`, and the module's `IMAGES` maps that name to
  the file.

## Which file to edit for what

- The prose, the footnotes, the Decalogues' table and the tour's Markdown-noted rows:
  `review.md`.
- The notes of the other rows of the tour, their groups, the tour's divisions (`DIVISIONS`)
  and the hovers (`ABBREVIATIONS`): the module.
- `forms.json`: only when a row whose note is in the module is added or removed.
- The styles: the module's stylesheet.
- Never the generated page or its published stylesheet: both are rewritten by every build.

Hebrew is copied by a script, never retyped, and kept in MAM-normal order. Replaced text is
asserted verbatim and exactly once. Ben's premises are checked against the data first, and a
contradicted premise goes to him.

## How to build and check

From the MAM-basics root:

```powershell
./.venv/Scripts/python.exe py/main_authored.py gen-israel-bible-review
```

Read the page's diff; any other changed file is a finding. Run Black on the module whenever
it changes. Whenever a MAM form changes, in `forms.json` or in `review.md`'s tables, run the
lint that checks every MAM form the page shows against MAM-simple:

```powershell
./.venv/Scripts/python.exe py/main_test.py py/tests/test_israel_bible_review_mam_forms.py
```

Other checks follow `doc/review-trial.md`. Those that reach this review's files are
`py/tests/test_prose_mark_order.py` (`review.md` and this file), `test_prose_conventions.py`
and `test_transliterations.py` (the page's prose and the module's), `test_shared_html_styles.py`
(the page's stylesheets and font), and
`py/check_html_syntax_and_sanity.py gh-pages/israel-bible-review`.
A push of `main` makes the source public at once; the page reaches the site at Ben's next
dispatch of the Pages workflow.

## Privacy

What the page shows is public. Nothing else of the Israel Bible's text, and nothing of BHL,
enters MAM-basics: not in the source, these records, comments or commit messages. A new row's
Israel Bible form and page are taken by a throwaway script from research data kept outside
this repository, and the script writes only those fields.

## Decisions

Ben's decisions about the review, numbered from 1, each with his words, its date and what
changed.

1. **Jeremiah 3:17's note, "two final vav letters".** At the port, the lint
   `test_no_plural_inflections_of_hebrew_names` in `py/tests/test_prose_conventions.py`
   flagged the note's "the two final vavs", an English plural of a letter's name, and
   suggested "vav letters". Asked whether to use that fix, Ben said on 2026-11-10: "Yes that
   fix is good." The note now says "IB has a dot in the first of the two final vav letters."
2. **The review's own folder.** Ben, 2026-11-11, asking for a session "to move the
   israel-bible review to its own folder in gh-pages, a pear of book-of-job, clc, etc." The
   page left `gh-pages/MAM-with-doc/misc/review_of_israel_bible.html` for
   `gh-pages/israel-bible-review/index.html`, with its stylesheet as `style.css` and its crop
   in `img/`, the names that most of its peers use. Its module, `review_of_israel_bible.py`
   until then, became `israel_bible_review_index.py`, since the generator of an `index.html`
   takes a name ending in "index". `py/main_authored.py gen-israel-bible-review` and the mega's
   `israel-bible-review` step run it, where `gen-misc` did. No stub stands at the old address,
   where the page was never published: Ben's last dispatch of the Pages workflow before the
   move, at 12:03 New York time on 2026-11-09, deployed `4b5cf93d`, from before the port. In
   the same message Ben asked for a note that the misc folder was an outdated precedent;
   `py/main_authored.py`'s docstring, "WHERE A NEW PAGE GOES", quotes it, with what this
   repository's history shows and what it cannot settle.

## Open decisions

Questions put to Ben, numbered from 1. Each gets an "Answered" line, with his words and the
date, when he answers it, and each session that edits the review first puts every question
without such a line to him.

1. **The page's terms in `DATA-LICENSES.md`.** Put to Ben on 2026-11-11, at the move. Until
   then the page and its stylesheet fell, by their place alone, under the row for
   `gh-pages/MAM-with-doc/`, MAM's CC-BY-SA 4.0, and the crop under the row for its
   `misc/img/`, each rights holder's. The move gave `gh-pages/israel-bible-review/` rows of
   its own, which follow those of the other review in a folder of its own,
   `gh-pages/book-of-job/`: the page Ben's, with no grant made or implied, and the crop its
   rights holder's. Should the page stay so, or take GPL-3.0, as the pages that this
   repository's code writes from Ben's prose do, the post-stress-meteg pages among them, or
   CC-BY-SA 4.0? The module's notes are GPL-3.0 already, as part of `py/`, and this folder,
   `in/israel-bible-review/`, has had no row since the port.
