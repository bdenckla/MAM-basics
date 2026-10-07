"""Individually adjudicated pointings, independent of the frozen inference set.

Each record stores the parameters of the ketiv/qere template it points, which
frozen_ketiv.checked_target compares with the template where the pointing is
written.
"""

import copy
import json
from near_aleppo import build_paths

from near_aleppo import frozen_ketiv
from near_aleppo import phase2_templates as phase2

MANIFEST = build_paths.input_dir() / "editorial-pointed-ketiv.json"


def ga(value):
    """Serialize existing orphan carriers with guillemets, never as consonants."""
    frozen_ketiv.validate_value(value)
    return "".join(
        part if isinstance(part, str) else "«" + part["tmpl_params"]["1"] + "»"
        for part in (value if isinstance(value, list) else [value])
    )


def load():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if (
        set(data) != {"format", "records"}
        or data["format"] != "near-aleppo-editorial-pointing-v2"
    ):
        raise ValueError("Unexpected editorial pointing manifest schema")
    # EditorialPointing keys the records by verse, so two in one verse are refused.
    identities, verses = set(), set()
    for row in data["records"]:
        if set(row) != {"id", "verse", "path", "tmpl_params", "ga", "value"}:
            raise ValueError("Unexpected editorial record schema")
        if row["id"] in identities or tuple(row["verse"]) in verses:
            raise ValueError("Duplicate editorial pointing record or verse")
        identities.add(row["id"])
        verses.add(tuple(row["verse"]))
        frozen_ketiv.validate_target_params(row)
        if ga(row["value"]) != row["ga"]:
            raise ValueError("Editorial GA differs from its runtime representation")
    return data


class EditorialPointing:
    def __init__(self):
        self.by_verse = {tuple(r["verse"]): r for r in load()["records"]}
        self.seen = set()

    def apply(self, cell, verse):
        if verse not in self.by_verse:
            return cell
        row = self.by_verse[verse]
        if verse in self.seen:
            raise ValueError(f"{row['id']}: editorial pointing applied twice")
        target = frozen_ketiv.checked_target(cell, row)
        target["tmpl_params"][phase2.POINTED_KETIV_PARAMETER] = copy.deepcopy(
            row["value"]
        )
        phase2.selected_keys(target, verse)
        self.seen.add(verse)
        return cell

    def finish(self):
        if self.seen != set(self.by_verse):
            raise ValueError("Editorial import did not consume its exact set")
