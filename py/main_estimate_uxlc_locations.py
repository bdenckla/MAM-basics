"""What the sibling UXLC-utils clone says about each of Holman's atoms.

Run from repo root:
    .venv\\Scripts\\python.exe py/main_estimate_uxlc_locations.py

Two facts, both wanting ~11 MB of UXLC core XML this repo does not track, both
written out for the render step to read: where the atom sits in the Leningrad
Codex (data/uxlc_atom_locations.json) and what the UXLC numbers it
(data/uxlc_standard_atoms.json). The render step needs only what is tracked, so
a fresh clone can render the page but not redo either -- the same division the
.eml ingest step already draws.

The estimator itself is MAM-basics' uxlc_misc.my_uxlc_location, vendored into
py/uxlc_misc/ and py/uxlc_lci/ by py/main_update_vendored_files.py. It takes a
(book, chapter, verse, atom) quad, so no word matching is involved and none of
the CLI's ambiguity cases arise.

What it does NOT take is the atom number CaseRef holds, and until 2026-08-12 it
was handed exactly that. Three numberings are in play here and no two of them
agree everywhere; ``hkq_cmn.uxlc_standard_atoms`` sets out the evidence
for what each is:

  * **Holman's**, which CaseRef holds, counts a ketiv/qere pair as one atom and
    does not count a mid-verse samekh.
  * **the UXLC's**, which this module works out and which the page shows, counts
    every child element of the verse.
  * **the estimator's**, which is whatever my_uxlc.read_all_books builds, that
    reader dropping the <k> and keeping every <q>. bibdist.calc walks its lists
    and takes the atom number as an index into one, so this is the numbering the
    estimator's input has to be in.

So _atom_numbers below resolves Holman's index to the verse element it names,
and reports that element's place in each of the other two counts. Of the 124
cases the estimator's number differs from Holman's on one, Ezekiel 8:6, whose
ketiv מהם has two qere atoms; before the fix the estimate for that case was
worked out for אֲשֶׁ֥ר, the atom before the בֵּֽית־ the case is about.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import hkq_paths
from mb_cmn import bib_locales as tbn
from hkq_cmn.uxlc_atom_locations import AtomLocation, write_locations
from hkq_cmn.uxlc_email_extract import CaseRef, CorrectionCase, read_emails
from hkq_cmn.uxlc_standard_atoms import write_standard_atoms
from uxlc_misc import my_uxlc, my_uxlc_location

DEFAULT_EMAILS_DIR = hkq_paths.emails_dir()
DEFAULT_IMAGE_DIR = hkq_paths.email_img_dir()
DEFAULT_DATA_DIR = hkq_paths.data_dir()

NOTE = (
    "Estimated column and line for each atom Holman's emails raise, from"
    " MAM-basics' uxlc_misc.my_uxlc_location over the UXLC core XML and LC"
    " page index in the sibling UXLC-utils. Written by"
    " py/main_estimate_uxlc_locations.py and read by the render step; folio is"
    " the LC leaf in the DDDA form the manuscript image URLs use, line counts"
    " down from the top of the named column, and flat_line counts down the"
    " whole page across all three columns."
)

STANDARD_ATOMS_NOTE = (
    "The UXLC's atom number for each atom Holman's emails raise, worked out"
    " from the UXLC core XML in the sibling UXLC-utils. The UXLC counts every"
    " child element of the verse, so a ketiv and its qere are two atoms and a"
    " mid-verse samekh is one; Holman counts a ketiv/qere pair once and does"
    " not count a samekh, so the key here, which is his, disagrees with the"
    " value on the few cases where the verse has either before the atom."
    " Written by py/main_estimate_uxlc_locations.py and read by the render"
    " step; hkq_cmn/uxlc_standard_atoms sets out the evidence."
)

# Every tag the UXLC core XML puts directly under <v>. Passed to my_uxlc.read so
# that its lists hold one entry per element, which is what the UXLC's own
# numbering counts; the reader's default handlers drop <k> and the markers.
_COUNTED_VERSE_CHILD_TAGS = ("w", "k", "q", "x", "pe", "samekh", "reversednun")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emails-dir", type=Path, default=DEFAULT_EMAILS_DIR)
    parser.add_argument("--image-dir", type=Path, default=DEFAULT_IMAGE_DIR)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    args = parser.parse_args()

    _emails, cases = read_emails(args.emails_dir, args.image_dir)

    uxlc, pbi = my_uxlc_location.prep()
    verse_tags = my_uxlc.read_all_books(
        {tag: _handle_counted for tag in _COUNTED_VERSE_CHILD_TAGS}
    )
    numbers = {case.ref.key: _atom_numbers(verse_tags, case.ref) for case in cases}
    locations = {
        case.ref.key: _estimate(uxlc, pbi, case, numbers[case.ref.key][1])
        for case in cases
    }
    path = write_locations(args.data_dir, locations, note=NOTE)
    standard_path = write_standard_atoms(
        args.data_dir,
        {ref_key: standard for ref_key, (standard, _est) in numbers.items()},
        note=STANDARD_ATOMS_NOTE,
    )

    print(
        json.dumps(
            {
                "case_count": len(cases),
                "renumbered_case_count": sum(
                    1 for case in cases if numbers[case.ref.key][0] != case.ref.atom
                ),
                "output_path": path.as_posix(),
                "standard_atoms_path": standard_path.as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def _columns_on_page(book: str) -> int:
    """How many columns a leaf of this book has, as the estimator counts them.

    The Sifrei Emet -- Psalms, Proverbs and Job -- are written two columns to a
    page and the rest of the manuscript three. This is the same rule
    ``my_uxlc_location._page_column_count`` applies when it works out how many
    flat lines a page holds, restated here because this module needs it to read
    the answer back.
    """
    return 2 if tbn.get_secid(book) == tbn.SEC_SIF_EM else 3


def _require_column_on_page(case: CorrectionCase, guess: dict) -> None:
    """Raise if the estimated column is not a column this book's leaves have.

    ``page_and_guesses`` cuts the flat line into 27-line columns, naming the
    third for anything past 55. Both directions of that arithmetic use the same
    27 lines per column, so the cut is right for a two-column Sifrei Emet leaf
    too, as long as the flat line stays on the leaf. What it cannot do is notice
    when the flat line runs off the bottom: on a Psalms page it would report a
    third column, which is not a column that page has.

    This replaces a guard that refused every Sifrei Emet case outright, on the
    ground that the three-column cut reported a column that was not there and
    reported it silently. Measured 2026-08-12 over the 63 Sifrei Emet cases in
    Holman's Psalms, Proverbs and Job messages, the largest flat line is 54.8
    (Job 34:20.4), so none of them reaches a third column; and the estimated
    column agrees with Holman's own stated column in 117 of the 124 cases, the
    seven that differ being split between prose books and the Sifrei Emet. So
    the failure that guard named is worth checking for rather than assuming,
    which is what this does.

    To re-establish those figures, compare the ``column`` written to
    ``data/uxlc_atom_locations.json`` against the ``Col. N`` in each case's
    manuscript citation in ``emails/``.
    """
    columns = _columns_on_page(case.ref.book)
    column = guess["column-guess"]
    if column > columns:
        raise ValueError(
            f"{case.ref.key} is estimated at column {column} of Leningrad Codex "
            f"folio {guess['page']}, from flat line {guess['fline-guess']}, but "
            f"a leaf of {case.ref.book} has {columns} columns. The estimate has "
            "run off the bottom of the leaf; work out what it should be before "
            "letting this case reach the page."
        )


def _estimate(uxlc, pbi, case: CorrectionCase, estimator_atom: int) -> AtomLocation:
    ref = case.ref
    guess = my_uxlc_location.page_and_guesses(
        uxlc, pbi, (ref.book, ref.chapter, ref.verse, estimator_atom)
    )
    _require_column_on_page(case, guess)
    return AtomLocation(
        folio=guess["page"],
        column=guess["column-guess"],
        line=float(guess["line-guess"]),
        flat_line=float(guess["fline-guess"]),
    )


def _handle_counted(accum: list, verse_child) -> None:
    """Keep one entry per verse child, whatever its tag.

    my_uxlc.read takes its verse-child handlers as an argument for exactly this:
    the default set appends a word for <w> and each <q>, ignores <k> and the
    markers, and so builds the estimator's numbering rather than the UXLC's.
    The tag is all this needs -- the atom text is never compared here, the atom
    being identified by Holman's index rather than matched by its letters.
    """
    accum.append(verse_child.tag)


def _atom_numbers(verse_tags: dict, ref: CaseRef) -> tuple[int, int]:
    """Holman's index resolved into the UXLC's number and the estimator's.

    Walks his count -- <w> is an atom, a run of <k> and <q> is one atom, a
    marker is nothing -- to the element his index names, then reports that
    element's place in the UXLC's count of every child and in the estimator's
    count of <w> and <q>.
    """
    tags = verse_tags[ref.book][ref.chapter - 1][ref.verse - 1]
    covered = _holman_atoms(tags)
    if not 1 <= ref.atom <= len(covered):
        raise ValueError(
            f"{ref.key} names atom {ref.atom}, but counting a ketiv/qere pair "
            f"once the verse has {len(covered)}"
        )
    elements = covered[ref.atom - 1]
    if len(elements) > 1:
        raise ValueError(
            f"{ref.key} names a run of {len(elements)} ketiv and qere elements, "
            "so which of them the UXLC would number is not settled here. Decide "
            "what the card should say before letting this case reach the page."
        )
    standard = elements[0]
    if tags[standard - 1] == "k":
        raise ValueError(
            f"{ref.key} names a ketiv, which my_uxlc.read_all_books drops, so "
            "the estimator has no atom to be handed. Decide what to estimate "
            "from before letting this case reach the page."
        )
    estimator = sum(1 for tag in tags[:standard] if tag in ("w", "q"))
    return standard, estimator


def _holman_atoms(tags: list[str]) -> list[list[int]]:
    """For each atom Holman would count, the places its elements hold.

    1-based, and a list per atom rather than a number because a ketiv/qere run
    is one atom of his covering two elements or more.
    """
    atoms: list[list[int]] = []
    run: list[int] = []
    for index, tag in enumerate(tags, start=1):
        if tag in ("k", "q"):
            run.append(index)
            continue
        if run:
            atoms.append(run)
            run = []
        if tag == "w":
            atoms.append([index])
    if run:
        atoms.append(run)
    return atoms


if __name__ == "__main__":
    main()
