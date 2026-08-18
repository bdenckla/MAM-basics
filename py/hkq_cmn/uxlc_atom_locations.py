"""Where in the Leningrad Codex each of Holman's atoms sits, estimated.

Holman cites the scan he worked from by its file name and a rough position on
it -- ``366_2Sa_23.29b-24.16a (Col. 3 top)`` -- and the page shows an estimate
of the column and line instead. The estimate comes from MAM-basics'
``uxlc_misc.my_uxlc_location``, which interpolates by word count between the
page breaks the UXLC's LC index records, so it wants ~11 MB of UXLC XML from
the sibling UXLC-utils clone that a fresh clone of this repo does not have.

Hence two steps and this module in the middle. ``py/main_estimate_uxlc_locations.py``
runs the estimator and writes ``data/uxlc_atom_locations.json``, which is
tracked; the render step reads that file through ``read_locations`` below and
needs nothing but the clone. It is the same division the emails already use:
one step needs more than the checkout, everything downstream reads its tracked
derivative.

``require_full_coverage`` is why a new email cannot render with a missing
estimate: it raises both on a case with no entry and on an entry naming no
case, in the manner of ``uxlc_change_records.require_known_refs``.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

LOCATIONS_FILE_NAME = "uxlc_atom_locations.json"

# What the estimator reports, and what it does not. The line is a float because
# it is an interpolation, and the column comes from cutting the page into equal
# 27-line thirds -- which is what confines this to the prose books, the Sifrei
# Emet pages being set in two columns rather than three.
_ENTRY_KEYS = ("folio", "column", "line", "flat_line")


@dataclass(frozen=True)
class AtomLocation:
    """One atom's estimated place on its Leningrad Codex page."""

    folio: str
    column: int
    line: float
    flat_line: float

    @property
    def rounded_line(self) -> int:
        """The line to report, as a whole number of lines from the column top.

        Rounded because a tenth of a line is a precision the estimate does not
        have, and held inside the 27 lines the column arithmetic assumes: an
        interpolation landing at line 27.6 means the foot of the column, and
        reporting a line 28 the reader cannot find there would be worse than
        reporting the last one. Only 2Samuel 5:21.1 reaches that today.
        """
        return min(27, max(1, round(self.line)))


def read_locations(data_dir: Path) -> dict[str, AtomLocation]:
    """The tracked estimates, keyed as ``CaseRef.key`` spells a reference."""
    path = data_dir / LOCATIONS_FILE_NAME
    if not path.is_file():
        raise FileNotFoundError(
            f"{path} is missing; run py/main_estimate_uxlc_locations.py, which "
            "needs the sibling UXLC-utils clone"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        ref_key: AtomLocation(
            folio=entry["folio"],
            column=entry["column"],
            line=entry["line"],
            flat_line=entry["flat_line"],
        )
        for ref_key, entry in payload["locations"].items()
    }


def write_locations(
    data_dir: Path, locations: dict[str, AtomLocation], *, note: str
) -> Path:
    path = data_dir / LOCATIONS_FILE_NAME
    payload = {
        "note": note,
        "locations": {
            ref_key: {
                "folio": location.folio,
                "column": location.column,
                "line": location.line,
                "flat_line": location.flat_line,
            }
            for ref_key, location in locations.items()
        },
    }
    data_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )
    return path


def require_full_coverage(
    locations: dict[str, AtomLocation], ref_keys: list[str]
) -> None:
    """Raise unless the estimates and the cases name exactly the same atoms."""
    missing = sorted(set(ref_keys) - set(locations))
    if missing:
        raise ValueError(
            f"no manuscript-location estimate for {missing}; rerun "
            "py/main_estimate_uxlc_locations.py, which needs the sibling "
            "UXLC-utils clone"
        )
    unmatched = sorted(set(locations) - set(ref_keys))
    if unmatched:
        raise ValueError(
            f"{LOCATIONS_FILE_NAME} names cases that no email contains: "
            f"{unmatched}; rerun py/main_estimate_uxlc_locations.py"
        )
