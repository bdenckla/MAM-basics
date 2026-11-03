"""Check the Word files of Miqra Mevoar against the tracked JSON and against MAM-simple.

For every .docx in a directory, the check extracts the book again and requires:

1. the record to equal the tracked JSON, and the directory's books to be the tracked
   books;
2. the book's chapters, and each chapter's verse numbers, to equal MAM-simple's;
3. each row's Bible column, letters only, to match MAM-simple's verse of the same
   number better than either neighbouring verse, with a ratio of at least _FLOOR.

The ratio is difflib's, without autojunk. A verse with a ketiv and a qere scores lower,
since MAM-simple's projection keeps both: Joshua 15:53 scored 0.78 and Hosea 10:10 0.88
on 2026-11-02, while their closer neighbouring verses scored 0.34. The margin of a row
is its ratio less its best neighbour's. The report, under .novc/miqra-mevoar/checks/,
lists each book's five smallest margins and lowest ratios. Nothing tracked is written.
"""

import datetime
import difflib
import re

from mb_cmn import paths
from mb_cmn.new_york_time import NEW_YORK
from miqra_mevoar import books
from miqra_mevoar import extract
from miqra_mevoar import mam_simple
from miqra_mevoar import tracked


def run(directory):
    """Check every .docx in directory; return 1 if any check fails, else 0."""
    report, failures = [f"Miqra Mevoar check of {directory}"], []
    docx_paths = extract.docx_paths(directory)
    docx_stems = [path.stem for path in docx_paths]
    tracked_stems = [book.stem for book in tracked.tracked_books()]
    if docx_stems != tracked_stems:
        failures.append(f"Word files {docx_stems}, tracked JSON {tracked_stems}")
    for docx_path in docx_paths:
        book = books.book_of_stem(docx_path.stem)
        record, bible = extract.extract_book(docx_path, book)
        _check_book(book, record, bible, report, failures)
    report.append("")
    report.append(f"failures: {len(failures)}")
    report.extend(f"  FAIL {failure}" for failure in failures)
    stamp = datetime.datetime.now(NEW_YORK).strftime("%Y%m%d-%H%M%S-%f%z")
    out_path = paths.novc_dir() / "miqra-mevoar" / "checks" / f"{stamp}.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(report) + "\n", encoding="utf-8", newline="")
    print("\n".join(report))
    print(f"report: {out_path}")
    return 1 if failures else 0


def _check_book(book, record, bible, report, failures):
    verses = [verse for chapter in record["chapters"] for verse in chapter["verses"]]
    report.append("")
    report.append(
        f"## {book.stem}: {len(record['chapters'])} chapters, {len(verses)} verses,"
        f" {sum(verse['heading'] is not None for verse in verses)} headings"
    )
    json_names = {path.name for path in tracked.json_dir().glob("*.json")}
    if f"{book.stem}.json" not in json_names:
        failures.append(f"{book.stem}: no tracked JSON")
    elif record != tracked.read_record(book):
        failures.append(f"{book.stem}: the extraction differs from the tracked JSON")
    keys = [
        (chapter["chapter"], verse["verse"])
        for chapter in record["chapters"]
        for verse in chapter["verses"]
    ]
    mam_keys = mam_simple.verse_keys(book)
    if keys != mam_keys:
        failures.append(
            f"{book.stem}: versification differs from MAM-simple's:"
            f" {_first_difference(keys, mam_keys)}"
        )
    letters = mam_simple.verse_letters(book)
    scores = []
    for (chapter, verse), text in bible.items():
        ours = _NON_LETTER.sub("", text)
        same = _ratio(ours, letters.get((chapter, verse), ""))
        neighbours = [
            _ratio(ours, letters[key])
            for key in ((chapter, verse - 1), (chapter, verse + 1))
            if key in letters
        ]
        best_other = max(neighbours, default=0.0)
        scores.append((same - best_other, same, best_other, chapter, verse))
        if same < _FLOOR or best_other >= same:
            failures.append(
                f"{book.stem} {chapter}:{verse}: ratio {same:.3f},"
                f" best neighbour {best_other:.3f}"
            )
    report.append("  smallest margins (margin, ratio, best neighbour):")
    report.extend(_score_line(score) for score in sorted(scores)[:5])
    report.append("  lowest ratios (margin, ratio, best neighbour):")
    report.extend(
        _score_line(score) for score in sorted(scores, key=lambda s: s[1])[:5]
    )


def _score_line(score):
    margin, same, best_other, chapter, verse = score
    return f"    {chapter}:{verse}  {margin:.3f}  {same:.3f}  {best_other:.3f}"


def _first_difference(ours, theirs):
    for index, (a, b) in enumerate(zip(ours, theirs)):
        if a != b:
            return f"item {index}: Word file {a}, MAM-simple {b}"
    return f"Word file {len(ours)} verses, MAM-simple {len(theirs)}"


def _ratio(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


_FLOOR = 0.6
_NON_LETTER = re.compile("[^\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}]")
