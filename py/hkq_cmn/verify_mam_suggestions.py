"""Check each MAM suggestion against MAM-parsed/plus, and record what was found.

THE GENERATED ARTIFACT IS THE TEST, which is this repo's standing rule, and this
module is what makes that true of the suggestions extract: every case carries the
result of looking it up in the corpus, so regenerating the extract and reading
the diff catches both a parse that drifted and a corpus that moved underneath it.

THE ATOM INDEX IS DERIVED HERE, NOT TAKEN FROM HOLMAN, and there is no ambiguity
in doing so.  Each case gives two spellings of one stretch of text, MAM's and the
comparison edition's.  Measured 2026-09-02 across all 34 cases: the MAM spelling
occurs EXACTLY ONCE in its verse, and EXACTLY ONE atom inside it differs between
the two spellings.  Between them those two facts name one atom and no other, so
the index Holman writes after the verse reference is redundant confirmation rather
than the thing that locates the case.  Re-establish this by running
``py/main_ingest_mam_suggestions.py``: it raises on any case where either fact
stops holding, so a silent guess is not among the outcomes.

Deriving it is what makes the indices CONSISTENT, which taking them as sent did
not.  Atoms are counted with maqaf-joined atoms separate -- the rule
``find_hebrew_tokens`` already implements by leaving MAQAF out of its character
class -- and all 34 of Holman's agree with the derivation.  The extract records
the derived index as ``atom`` and keeps his under ``atom_as_sent`` wherever the
two differ, so nothing about his message is lost; no case carries that field now.

NO CORRECTION OF HOLMAN STANDS.  The last one, 2Sa 15:37 (8 as sent, 9 derived),
WAS FIXED ON 2026-09-02, and it was not his error either.  Until then
``mam_plus_verse_data`` collected into the verse text the parameters of the
navigation template מ:פסוק, which carries the book name, chapter, verse and
seder, so the verse rendered with שמואל as its first
atom and its Hebrew numerals fused onto וַיָּבֹא.  Holman's 8 was right and the
corpus rendering was wrong, exactly as it was for the two below.

WHAT WAS FIXED IS A PROXY, NOT ONE TEMPLATE'S RULE.  ``_collect_text_fragments``
decided what a template contributed by asking whether it carried parameters,
reading "carries parameters" as "carries verse text".  It dispatches on the
template NAME throughout now, and raises on a name with no rule.  Seven leaks
closed together, changing the atom count of 507 verses, מ:פסוק among them
at 895 payloads.  Genesis 1:1 rendered 9 atoms for a seven-word verse, its
first atom running the book title, the whole navigation reference and two
copies of בְּרֵאשִׁית together, and renders 7.  That function's docstring holds
the evidence, the other six leaks and the re-measurement path; do not restate
them here.

ONLY 2Sa 15:37 OF THE 34 CASES WAS AFFECTED, AND THAT WAS A RULE RATHER THAN LUCK.
The navigation template precedes every verse, but in column D, which is not parsed
into these payloads at all; it reaches a payload only where it also carries a
division marker.  Measured 2026-09-02: 895 verse payloads hold one, and 889 of
those carry a seder (סדר), an aliyah (עלייה) or both, leaving 6 that carry a bare
reference for a reason not established here.  2Sa 15:37 begins seder 29, which is
why it was the one case of the 34 that has one.

THE MAQAF COMPOUNDS ARE NOT AMONG THEM, though a cruder check reports them as
disagreements.  Holman quotes a whole compound while numbering one of its atoms,
and the atom he numbers is the one bearing the difference every time.
So עַל־יְרוּשָׁלַ͏ִם against עַל־יְרוּשָׁלַ͏ִם resolves to its second atom
and agrees with his 11.  ``_differing_offset`` is what picks the right half, and
it needs neither his index nor his prose description of where the mark sits.

TWO CORRECTIONS DISSOLVED ON 2026-09-02, when a template with no parameters was
taught to contribute a separator: 1Ki 7:24 (17 as sent) and Judg 1:7 (21 as sent)
both now land where Holman put them.  The paseq template מ:פסק was fusing the
atoms on either side of it, so Judg 1:7 counted 22 atoms rather than 23.  Earlier
the same day the shirah spaces of the Song of Deborah were fusing Judg 5:6.7 and
Judg 5:11.13 the same way, and both of those were right too.

SO INVESTIGATE AN INDEX DISAGREEMENT BEFORE REPORTING IT AS HOLMAN'S.  Five have
looked like his numbering so far -- the four above and 2Sa 15:37 -- every one of
the five has turned out to be this corpus rendering instead, and all five are
resolved as of 2026-09-02.  A sixth would be worth the same suspicion.

``comparison_form_already_present`` IS A SEPARATE QUESTION, AND IT DATES THE
CORPUS RATHER THAN JUDGING HOLMAN.  A case whose verse already
has the comparison form is one MAM has adopted since the message was sent, so
the count of those is a statement about how stale the local ``MAM-parsed`` is,
not about Holman.  Measured 2026-09-02 against MAM-parsed ``54ba7e0``, that count
was zero even for the two cases corrected on Wikisource on 2026-08-28, because
the local corpus predates those edits.

It asks that question of the form as EXTRACTED rather than as corrected, because
``main_ingest_mam_suggestions`` calls ``check_case`` before it applies
``mam_suggestion_corrections``.  So Joshua 10:12's flag still asks whether MAM has
the U+05A8 qadma spelling Holman typed, rather than the doubled pashta his card
shows; that module's docstring records the limitation and why the atom index is
unaffected by it.
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
    dropped, since MAM has one inside יְרוּשָׁלַ͏ִם and a hand-typed form of the
    same word may not.
    """
    return give_std_mark_order(form).replace(CGJ, "")


def _atom_run(form: str) -> list[str]:
    """One quoted form reduced to the run of atoms it spells.

    A run rather than a single atom BECAUSE HOLMAN QUOTES WHOLE MAQAF COMPOUNDS
    WHILE NUMBERING ONE OF THEIR ATOMS.  ``find_hebrew_tokens`` leaves MAQAF out
    of its character class, so בְנֵֽי־יִשְׂרָאֵ֛ל reduces to two atoms here exactly as
    it does in the verse text; comparing the two runs is then the same operation
    whether the form is one atom or several.  It also drops sof pasuq, which he
    keeps on a verse-final form and which is not part of the atom.
    """
    return [_comparable(one) for one in find_hebrew_tokens(form)]


def _run_starts(atoms: list[str], run: list[str]) -> list[int]:
    """Every 1-based index at which ``run`` occurs in ``atoms``.

    Every occurrence and not the first, so that a form occurring twice can be
    told from one occurring once.  Taking the first would silently pick a side
    where the right answer is that the form does not identify an atom.
    """
    if not run:
        return []
    return [
        start + 1
        for start in range(len(atoms) - len(run) + 1)
        if atoms[start : start + len(run)] == run
    ]


def _differing_offset(mam_run: list[str], comparison_run: list[str]) -> int | None:
    """Which atom of the quoted run differs between the two forms, 0-based.

    THIS IS WHAT IDENTIFIES THE ATOM A CASE IS ABOUT, and it needs no index from
    Holman at all.  He supplies two spellings of the same stretch of text, MAM's
    and the comparison edition's, and the atom his case is about is the one that
    differs between them.  For a single-atom quotation that is the atom itself;
    for a maqaf compound it picks out the half he means.
    Thus עַל־יְרוּשָׁלַ͏ִם against עַל־יְרוּשָׁלַ͏ִם resolves to the second atom
    without anything having to read his prose description of where the meteg sits.

    None when the two runs are different lengths, or differ in no atom or in more
    than one -- in which case the caller raises rather than guessing.
    """
    if len(mam_run) != len(comparison_run):
        return None
    offsets = [i for i in range(len(mam_run)) if mam_run[i] != comparison_run[i]]
    return offsets[0] if len(offsets) == 1 else None


@dataclass
class CaseCheck:
    ref: str
    atom_count: int
    quoted_atom_count: int
    quoted_form_starts_at: int
    derived_atom: int
    stated_atom: int
    comparison_form_already_present: bool

    @property
    def stated_atom_agrees(self) -> bool:
        return self.stated_atom == self.derived_atom

    def payload(self) -> dict[str, object]:
        return {
            "atom_count": self.atom_count,
            "quoted_atom_count": self.quoted_atom_count,
            "quoted_form_starts_at_atom": self.quoted_form_starts_at,
            "derived_atom": self.derived_atom,
            "stated_atom": self.stated_atom,
            "stated_atom_agrees": self.stated_atom_agrees,
            "comparison_form_already_present": self.comparison_form_already_present,
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

    starts = _run_starts(comparable_atoms, wanted)
    if len(starts) != 1:
        raise ValueError(
            f"{ref}: the quoted MAM form occurs {len(starts)} times in the verse, "
            "so it does not identify one atom; resolve this case by hand rather "
            "than letting a derivation guess"
        )
    offset = _differing_offset(wanted, proposed)
    if offset is None:
        raise ValueError(
            f"{ref}: the MAM form and the comparison form do not differ in exactly "
            "one atom, so the atom this case is about is not derivable; resolve it "
            "by hand"
        )

    return CaseCheck(
        ref=ref,
        atom_count=len(atoms),
        quoted_atom_count=len(wanted),
        quoted_form_starts_at=starts[0],
        derived_atom=starts[0] + offset,
        stated_atom=atom,
        comparison_form_already_present=bool(_run_starts(comparable_atoms, proposed)),
    )


def summarize(checks: list[CaseCheck]) -> dict[str, object]:
    """How many of Holman's stated atom indices the derivation agreed with.

    Every case has a derived index -- ``check_case`` raises rather than return one
    it could not determine -- so the only interesting count is agreement.
    ``comparison_form_already_present`` is a separate question asked of every case,
    and a non-zero count there says the local corpus has moved on rather than
    saying anything about Holman.
    """
    return {
        "case_count": len(checks),
        "stated_atom_agrees": sum(1 for one in checks if one.stated_atom_agrees),
        "stated_atom_corrected": sum(1 for one in checks if not one.stated_atom_agrees),
        "comparison_form_already_present": sum(
            1 for one in checks if one.comparison_form_already_present
        ),
    }
