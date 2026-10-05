"""Individually adjudicated pointings, independent of the frozen inference set."""

import copy
from hashlib import sha256
import json
from near_aleppo import build_paths

from near_aleppo import frozen_ketiv
from near_aleppo import phase2_templates as phase2

MANIFEST = build_paths.input_dir() / "editorial-pointed-ketiv.json"
MANIFEST_SHA256 = "4bb888b3d1107b928dbecc3d6da3c8cf351c3ea8a10a233dbf08898c75678eb2"


def ga(value):
    """Serialize existing orphan carriers with guillemets, never as consonants."""
    frozen_ketiv.validate_value(value)
    return "".join(
        part if isinstance(part, str) else "«" + part["tmpl_params"]["1"] + "»"
        for part in (value if isinstance(value, list) else [value])
    )


def load():
    raw = MANIFEST.read_bytes()
    if sha256(raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError("Editorial pointing manifest differs from the reviewed hash")
    data = json.loads(raw)
    if (
        set(data) != {"format", "records"}
        or data["format"] != "near-aleppo-editorial-pointing-v1"
    ):
        raise ValueError("Unexpected editorial pointing manifest schema")
    if len(data["records"]) != 5:
        raise ValueError("Editorial pointing population changed")
    for row in data["records"]:
        if set(row) != {"id", "verse", "path", "expected_sha256", "ga", "value"}:
            raise ValueError("Unexpected editorial record schema")
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
        target = frozen_ketiv.at_path(cell, row["path"])
        if target["tmpl_name"] not in phase2.POINTED_KETIV_FAMILIES:
            raise ValueError("Unsupported editorial target family")
        if phase2.POINTED_KETIV_PARAMETER in target["tmpl_params"]:
            raise ValueError("Existing pointing conflicts with editorial import")
        if frozen_ketiv.digest(target) != row["expected_sha256"] or verse in self.seen:
            raise ValueError("Changed or repeated editorial target")
        target["tmpl_params"][phase2.POINTED_KETIV_PARAMETER] = copy.deepcopy(
            row["value"]
        )
        phase2.selected_keys(target, verse)
        self.seen.add(verse)
        return cell

    def finish(self):
        if self.seen != set(self.by_verse):
            raise ValueError("Editorial import did not consume its exact set")
