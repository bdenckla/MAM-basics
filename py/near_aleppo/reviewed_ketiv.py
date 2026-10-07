"""Import sealed, reviewed pointings after all prior near-Aleppo pointings.

Runtime uses current MAM books and portable pointings only. Eligibility and
adoption authority are recorded separately; the importer makes no new choice.
"""

from collections import defaultdict
import copy
from hashlib import sha256
import json
from near_aleppo import build_paths

from near_aleppo import frozen_ketiv
from near_aleppo import phase2_templates as phase2

MANIFEST = build_paths.input_dir() / "reviewed-pointed-ketiv.json"
MANIFEST_SHA256 = "34bfdcbb5d4c571ccc3daf93708e9364bffbcad87196bc2515eb181ba187f883"
SITES = 236
ATOMS = 237


def validate_manifest(data):
    """Require the closed portable schema and exact reviewed population."""
    if (
        set(data) != {"format", "input_sha256", "records"}
        or data["format"] != "near-aleppo-reviewed-pointing-v1"
    ):
        raise ValueError("Unexpected reviewed pointing manifest schema")
    if frozen_ketiv._FORBIDDEN.search(json.dumps(data, ensure_ascii=False)):
        raise ValueError("Private attribution or URL in reviewed runtime manifest")
    identities, addresses = set(), set()
    fields = {"id", "verse", "path", "expected_sha256", "value", "atoms"}
    for row in data["records"]:
        if set(row) != fields or not frozen_ketiv._HEX.fullmatch(
            row["expected_sha256"]
        ):
            raise ValueError("Unexpected reviewed pointing record schema")
        if len(row["verse"]) != 3 or not all(isinstance(p, str) for p in row["verse"]):
            raise ValueError("Invalid reviewed verse address")
        if not all(type(p) in (str, int) for p in row["path"]) or row["atoms"] not in (
            1,
            2,
        ):
            raise ValueError("Invalid reviewed target address or atom count")
        address = (tuple(row["verse"]), tuple(row["path"]))
        if row["id"] in identities or address in addresses:
            raise ValueError("Duplicate reviewed pointing target")
        identities.add(row["id"])
        addresses.add(address)
        frozen_ketiv.validate_value(row["value"])
    if len(identities) != SITES or sum(r["atoms"] for r in data["records"]) != ATOMS:
        raise ValueError("Reviewed pointing population changed")
    return data


def load():
    raw = MANIFEST.read_bytes()
    if sha256(raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError("Reviewed pointing manifest differs from the sealed hash")
    return validate_manifest(json.loads(raw))


class ReviewedPointing:
    def __init__(self, input_dir):
        self.data = load()
        actual = {
            p.name: sha256(p.read_bytes()).hexdigest()
            for p in sorted(input_dir.glob("*.json"))
        }
        if actual != self.data["input_sha256"]:
            raise ValueError("MAM inputs differ from the reviewed pointing target")
        self.by_verse = defaultdict(list)
        for row in self.data["records"]:
            self.by_verse[tuple(row["verse"])].append(row)
        self.seen = set()

    def apply(self, cell, verse):
        targets = []
        for row in self.by_verse[verse]:
            target = frozen_ketiv.at_path(cell, row["path"])
            if target["tmpl_name"] not in phase2.POINTED_KETIV_FAMILIES:
                raise ValueError(f"{row['id']}: unsupported reviewed target family")
            if phase2.POINTED_KETIV_PARAMETER in target["tmpl_params"]:
                raise ValueError(f"{row['id']}: prior pointing takes priority")
            if (
                frozen_ketiv.digest(target) != row["expected_sha256"]
                or row["id"] in self.seen
            ):
                raise ValueError(f"{row['id']}: changed or repeated reviewed target")
            targets.append((row, target))
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
