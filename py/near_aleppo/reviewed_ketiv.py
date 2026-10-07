"""Import reviewed pointings after all prior near-Aleppo pointings.

Runtime uses current MAM books and portable pointings only. Eligibility and
adoption authority are recorded separately; the importer makes no new choice.
Each record stores the parameters of the ketiv/qere template it points, which
frozen_ketiv.checked_target compares with the template where the pointing is
written.
"""

from collections import defaultdict
import copy
import json
from near_aleppo import build_paths

from near_aleppo import frozen_ketiv
from near_aleppo import phase2_templates as phase2

MANIFEST = build_paths.input_dir() / "reviewed-pointed-ketiv.json"


def validate_manifest(data):
    """Require the closed portable schema, with no duplicate record or target."""
    if (
        set(data) != {"format", "records"}
        or data["format"] != "near-aleppo-reviewed-pointing-v2"
    ):
        raise ValueError("Unexpected reviewed pointing manifest schema")
    if frozen_ketiv._FORBIDDEN.search(json.dumps(data, ensure_ascii=False)):
        raise ValueError("Private attribution or URL in reviewed runtime manifest")
    identities, addresses = set(), set()
    fields = {"id", "verse", "path", "tmpl_params", "value"}
    for row in data["records"]:
        if set(row) != fields:
            raise ValueError("Unexpected reviewed pointing record schema")
        if len(row["verse"]) != 3 or not all(isinstance(p, str) for p in row["verse"]):
            raise ValueError("Invalid reviewed verse address")
        if not all(type(p) in (str, int) for p in row["path"]):
            raise ValueError("Invalid reviewed target address")
        frozen_ketiv.validate_target_params(row)
        address = (tuple(row["verse"]), tuple(row["path"]))
        if row["id"] in identities or address in addresses:
            raise ValueError("Duplicate reviewed pointing target")
        identities.add(row["id"])
        addresses.add(address)
        frozen_ketiv.validate_value(row["value"])
    return data


def load():
    return validate_manifest(json.loads(MANIFEST.read_text(encoding="utf-8")))


class ReviewedPointing:
    def __init__(self):
        self.data = load()
        self.by_verse = defaultdict(list)
        for row in self.data["records"]:
            self.by_verse[tuple(row["verse"])].append(row)
        self.seen = set()

    def apply(self, cell, verse):
        targets = []
        for row in self.by_verse[verse]:
            if row["id"] in self.seen:
                raise ValueError(f"{row['id']}: reviewed pointing applied twice")
            targets.append((row, frozen_ketiv.checked_target(cell, row)))
        for row, target in targets:
            target["tmpl_params"][phase2.POINTED_KETIV_PARAMETER] = copy.deepcopy(
                row["value"]
            )
            phase2.selected_keys(target, verse)
            self.seen.add(row["id"])
        return cell

    def finish(self):
        if self.seen != {r["id"] for r in self.data["records"]}:
            raise ValueError("Reviewed import did not consume its exact approved set")
