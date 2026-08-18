"""What the UXLC calls each of Holman's atoms, where it calls it something else.

Holman and the UXLC number a verse's atoms differently, so the number at the
head of a card is not always the number in his email. **The UXLC counts every
child element of the verse**: a ketiv and its qere are two atoms, a ketiv with
two qere atoms is three, and a mid-verse samekh or pe is one. Holman counts a
ketiv/qere pair once and does not count a samekh. The two agree everywhere else,
which is most of the corpus -- of Holman's 124 cases, 119 get the same number
either way.

The UXLC's numbering is the one to show, because it is the one that finds the
word at tanach.us: it is what the change list's ``<citation><position>`` means
and what a note page's address ``<book>.<c>.<v>.<position>-<code>.html`` means.
Established 2026-08-12 against the sibling UXLC-utils clone, in two passes whose
strength is very different and worth keeping apart:

  * **The ketiv/qere half is settled.** Of the 1367 records in the seventeen
    change files under ``in/UXLC-misc``, 174 cite an atom with a ``<k>`` or a
    ``<q>`` before it; counting every element, the record's quoted word is the
    atom cited in 170 of the 174, counting the pair once in 50. The 476 note
    pages under ``in/UXLC-notes`` say the same independently: 97 of them address
    an atom with a ``<k>`` or ``<q>`` before it, and beyond that every one of
    the 36 pages coded ``y`` (a yatir note, which is about a ketiv) addresses a
    ``<k>`` element and 34 of the 35 coded ``q`` address a ``<q>``, which no
    numbering that counts the pair once could do.
  * **The samekh half rests on two records**, both of them hits and no evidence
    anywhere pointing the other way: ``2022.08.14-3`` cites 2Sam 21:1.23 for
    עַֽל־, the 22nd ``<w>`` of a verse split by a samekh, and ``2023.08.09-4``
    cites 1 Chr 27:25.16 for עֻזִיָּֽהוּ׃, the 15th, its note saying outright
    that "This verse is split by a samekh closed spacing marker between the 6-th
    and 7-th words". No note page tests it at all. Two of the five cases this
    module renumbers turn on those two records, so treat a counterexample as a
    reason to revisit rather than as noise.

The probes are ``UXLC-utils/.novc/atom_scheme_final.py`` and
``note_page_positions.py``, gitignored scratch rather than anything either repo
runs.

Two steps and this module in the middle, the same division
``uxlc_atom_locations`` already draws: the derivation wants ~11 MB of UXLC core
XML from the sibling clone, so ``py/main_estimate_uxlc_locations.py`` works the
numbers out and writes the tracked ``data/uxlc_standard_atoms.json``, and the
render step reads that file and needs nothing but this checkout.
"""

from __future__ import annotations

import json
from pathlib import Path

STANDARD_ATOMS_FILE_NAME = "uxlc_standard_atoms.json"


def read_standard_atoms(data_dir: Path) -> dict[str, int]:
    """The UXLC's atom number per case, keyed as ``CaseRef.key`` spells one."""
    path = data_dir / STANDARD_ATOMS_FILE_NAME
    if not path.is_file():
        raise FileNotFoundError(
            f"{path} is missing; run py/main_estimate_uxlc_locations.py, which "
            "needs the sibling UXLC-utils clone"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    return dict(payload["standard_atoms"])


def write_standard_atoms(
    data_dir: Path, standard_atoms: dict[str, int], *, note: str
) -> Path:
    payload = {"note": note, "standard_atoms": standard_atoms}
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / STANDARD_ATOMS_FILE_NAME
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )
    return path


def require_full_coverage(standard_atoms: dict[str, int], ref_keys: list[str]) -> None:
    """Raise unless the numbers and the cases name exactly the same atoms."""
    missing = sorted(set(ref_keys) - set(standard_atoms))
    if missing:
        raise ValueError(
            f"no UXLC atom number for {missing}; rerun "
            "py/main_estimate_uxlc_locations.py, which needs the sibling "
            "UXLC-utils clone"
        )
    unmatched = sorted(set(standard_atoms) - set(ref_keys))
    if unmatched:
        raise ValueError(
            f"{STANDARD_ATOMS_FILE_NAME} names cases that no email contains: "
            f"{unmatched}; rerun py/main_estimate_uxlc_locations.py"
        )
