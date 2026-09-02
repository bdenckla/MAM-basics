"""Check each MAM suggestion against MAM-parsed/plus, and record what was found.

THE GENERATED ARTIFACT IS THE TEST, which is this repo's standing rule, and this
module is what makes that true of the suggestions extract: every case carries the
result of looking it up in the corpus, so regenerating the extract and reading
the diff catches both a parse that drifted and a corpus that moved underneath it.

WHY THIS SEARCHES RATHER THAN INDEXES.  Holman gives each case an atom index, and
those indices are good: measured 2026-09-02 against MAM-parsed ``54ba7e0``, 30 of
the 34 cases land exactly on his index once maqaf-joined atoms are counted
separately, which is the rule ``find_hebrew_tokens`` already implements by leaving
MAQAF out of its character class.  Re-establish that figure by running
``py/main_ingest_mam_suggestions.py`` and reading ``mam_plus_verify``.

The four that do not are two known divergences, and both are more useful reported
than papered over:

  * ONE case, 2Ki 21:12.11, numbers one atom of a maqaf compound and quotes the
    WHOLE compound -- and the direction is not fixed, since Judg 6:1.2 quotes
    forward from the numbered atom where 2Ki 21:12.11 quotes backward from it.
    Judg 6:1.2 lands on its stated atom only because the atom it numbers is the
    compound's first.
  * THREE cases -- 1Ki 7:24.17, 2Sa 15:37.8 and Judg 1:7.21 -- disagree with the
    corpus by one in a direction that is not consistent either (the first and
    third are one high, the second one low).  All three are the atom יְרוּשָׁלַ͏ִם,
    which is suggestive but does not settle anything, and this is a question for
    Holman rather than something to resolve by guessing.

A DEFECT IN THE CORPUS RENDERING ACCOUNTED FOR TWO MORE, and finding it is why
these figures are worth trusting.  Before ``mam_plus_verse_data`` was taught that
a whitespace template means whitespace, on 2026-09-02, Judg 5:6.7 and Judg 5:11.13
also looked one out; both were right, and the shirah spaces of the Song of Deborah
were fusing the atoms on either side of them.  So an index disagreement here is
worth investigating before it is reported as his.

The check reports several independent facts per case -- whether his MAM form is in
the verse at all, where, whether that covers the atom he numbered, and whether the
verse instead already has the form he proposes -- and lets the reader see which.
Collapsing them to one pass/fail would throw away the distinction between "his
index is off by one" and "MAM has since been corrected", which are opposite
conclusions.

THE THIRD FACT IS THE ONE THAT DATES THE CORPUS.  A case whose verse already
has the comparison form is one MAM has adopted since the message was sent, so
the count of those is a statement about how stale the local ``MAM-parsed`` is,
not about Holman.  Measured 2026-09-02 against MAM-parsed ``54ba7e0``, that count
was zero even for the two cases corrected on Wikisource on 2026-08-28, because
the local corpus predates those edits.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path

from hkq_cmn.hebrew_text_tokens import find_hebrew_tokens
from hkq_cmn.mam_plus_verse_data import verse_texts_by_location
from hkq_cmn.verify_table_words_in_mam_plus import (
    expected_plus_location_for_standard_book_name,
)
from mb_cmn import paths
from mb_cmn.uni_denorm import give_std_mark_order

CGJ = "\N{COMBINING GRAPHEME JOINER}"


def _comparable(form: str) -> str:
    """One atom reduced to what two spellings of it must share.

    Mark order first -- ``give_std_mark_order`` and never ``unicodedata.normalize``,
    per this repo's standing rule -- and then the combining grapheme joiner
    dropped, since MAM has one inside יְרוּשָׁלַ͏ִם and a hand-typed form of the
    same word may not.
    """
    return give_std_mark_order(form).replace(CGJ, "")


def _atom_run(form: str) -> list[str]:
    """One quoted form reduced to the run of atoms it spells.

    A run rather than a single atom BECAUSE HOLMAN QUOTES WHOLE MAQAF COMPOUNDS
    WHILE NUMBERING ONE OF THEIR ATOMS.  ``find_hebrew_tokens`` leaves MAQAF out
    of its character class, so בְנֵֽי־יִשְׂרָאֵ֛ל reduces to two atoms here exactly as
    it does in the verse text; comparing the two runs is then the same operation
    whether the form is one atom or several.  It also drops sof pasuq, which he
    keeps on a verse-final form and which is not part of the atom.
    """
    return [_comparable(one) for one in find_hebrew_tokens(form)]


def _run_start(atoms: list[str], run: list[str]) -> int | None:
    """The 1-based index at which ``run`` occurs in ``atoms``, or None."""
    if not run:
        return None
    for start in range(len(atoms) - len(run) + 1):
        if atoms[start : start + len(run)] == run:
            return start + 1
    return None


@dataclass
class CaseCheck:
    ref: str
    atom_count: int
    quoted_atom_count: int
    mam_form_found_at: int | None
    at_stated_atom: bool
    covers_stated_atom: bool
    comparison_form_already_present: bool
    atom_text_at_stated_index: str | None

    def payload(self) -> dict[str, object]:
        return {
            "atom_count": self.atom_count,
            "quoted_atom_count": self.quoted_atom_count,
            "mam_form_found_in_verse": self.mam_form_found_at is not None,
            "mam_form_found_at_atom": self.mam_form_found_at,
            "mam_form_starts_at_stated_atom": self.at_stated_atom,
            "mam_form_covers_stated_atom": self.covers_stated_atom,
            "comparison_form_already_present": self.comparison_form_already_present,
            "atom_text_at_stated_atom": self.atom_text_at_stated_index,
        }


@lru_cache(maxsize=32)
def _verse_texts_for_book(std_book_name: str) -> dict[tuple[int, int, int], str]:
    filename, _ = expected_plus_location_for_standard_book_name(std_book_name)
    plus_path = (
        paths.require_sibling("MAM-parsed", paths.sibling_repo("MAM-parsed"))
        / "plus"
        / filename
    )
    return verse_texts_by_location(json.loads(plus_path.read_text(encoding="utf-8")))


def check_case(
    std_book_name: str,
    chapter: int,
    verse: int,
    atom: int,
    mam_form: str,
    comparison_form: str,
) -> CaseCheck:
    filename, book39_index = expected_plus_location_for_standard_book_name(
        std_book_name
    )
    texts = _verse_texts_for_book(std_book_name)
    key = (book39_index, chapter, verse)
    text = texts.get(key)
    ref = f"{std_book_name} {chapter}:{verse}.{atom}"
    if text is None:
        raise ValueError(f"{ref}: verse not present in MAM-parsed/plus/{filename}")

    atoms = find_hebrew_tokens(text)
    comparable_atoms = [_comparable(one) for one in atoms]
    wanted = _atom_run(mam_form)
    proposed = _atom_run(comparison_form)

    found_at = _run_start(comparable_atoms, wanted)
    proposed_at = _run_start(comparable_atoms, proposed)

    covers = found_at is not None and found_at <= atom <= found_at + len(wanted) - 1

    return CaseCheck(
        ref=ref,
        atom_count=len(atoms),
        quoted_atom_count=len(wanted),
        mam_form_found_at=found_at,
        at_stated_atom=found_at == atom,
        covers_stated_atom=covers,
        comparison_form_already_present=proposed_at is not None,
        atom_text_at_stated_index=atoms[atom - 1] if 1 <= atom <= len(atoms) else None,
    )


def summarize(checks: list[CaseCheck]) -> dict[str, object]:
    """Four disjoint outcomes plus the corpus-staleness count, which overlaps them.

    The first four partition the cases: a form starts where he says, or merely
    covers the atom he numbered (the maqaf-compound quirk), or is in the verse
    somewhere else entirely (his index and the corpus disagree), or is not in the
    verse at all.  ``comparison_form_already_present`` is a separate question asked of
    every case, and a non-zero count there says the local corpus has moved on
    rather than saying anything about Holman.
    """
    return {
        "case_count": len(checks),
        "mam_form_starts_at_stated_atom": sum(
            1 for one in checks if one.at_stated_atom
        ),
        "mam_form_covers_stated_atom_only": sum(
            1 for one in checks if one.covers_stated_atom and not one.at_stated_atom
        ),
        "mam_form_elsewhere_in_verse": sum(
            1
            for one in checks
            if one.mam_form_found_at is not None and not one.covers_stated_atom
        ),
        "mam_form_not_in_verse": sum(
            1 for one in checks if one.mam_form_found_at is None
        ),
        "comparison_form_already_present": sum(
            1 for one in checks if one.comparison_form_already_present
        ),
    }
