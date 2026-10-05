"""Import an approved, immutable MAM-derived pointing payload after Readings.

Runtime reads only the sealed payload and current MAM input books. Archival
ownership evidence and approval diagnostics are not runtime dependencies.
"""

from collections import defaultdict
import copy
from hashlib import sha256
import json
from near_aleppo import build_paths
import re

from near_aleppo import phase2_templates as phase2

MANIFEST = build_paths.input_dir() / "frozen-pointed-ketiv.json"
# Target fingerprints refreshed for MAM-basics d8435412's notice-only correction.
# Every approved record and source identity is unchanged; full-file guards remain.
MANIFEST_SHA256 = "77d38e6a9626dd71f51abf55af3e367d7f888ec9f21d4e24dd0c526425528b89"
SITES = 723
ATOMS = 733
_HEX = re.compile(r"[0-9a-f]{64}\Z")
_FORBIDDEN = re.compile(r"baseline-\d+|mgketer|https?://", re.IGNORECASE)


def digest(value):
    return sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


def sites(value, verse, path=()):
    """Closed Scripture-only walk; paths address full original target templates."""
    if isinstance(value, str):
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            yield from sites(child, verse, path + (index,))
        return
    name = value["tmpl_name"]
    rule = phase2._RULES.get(name)
    if rule is None:
        raise ValueError(f"{verse}: unsupported source template {name}")
    if name in phase2.POINTED_KETIV_FAMILIES or name == "כתיב ולא קרי":
        yield path, value
    elif rule.action == phase2._KEEP_NOTE:
        for key in phase2.selected_keys(value, verse):
            yield from sites(
                value["tmpl_params"][key], verse, path + ("tmpl_params", key)
            )
    elif name in ("מ:קו״כ-אם-2", "קרי ולא כתיב") or rule.action in (
        phase2._VERBATIM,
        phase2._COLLAPSE_WORD,
        phase2._CARRIERS,
    ):
        return
    else:
        raise ValueError(f"{verse}: unsupported source action for {name}")


def at_path(value, path):
    for part in path:
        value = value[part]
    return value


def validate_value(value):
    """Runtime values are text or existing orphan templates, with no metadata."""
    parts = value if isinstance(value, list) else [value]
    if not parts:
        raise ValueError("Empty pointing payload")
    for part in parts:
        if isinstance(part, str):
            if _FORBIDDEN.search(part):
                raise ValueError("Attribution or URL in pointing payload")
        elif isinstance(part, dict) and set(part) == {"tmpl_name", "tmpl_params"}:
            phase2.carriers_text(part, "frozen pointing")
        else:
            raise ValueError("Non-source metadata in pointing payload")


def validate_manifest(data):
    required = {
        "format",
        "algorithm_commit",
        "mam_input_commit",
        "target_mam_commit",
        "input_sha256",
        "records",
    }
    if set(data) != required or data["format"] != "near-aleppo-frozen-pointing-v1":
        raise ValueError("Unexpected frozen pointing manifest schema")
    if _FORBIDDEN.search(json.dumps(data, ensure_ascii=False)):
        raise ValueError("Attribution, baseline identity or URL in runtime manifest")
    ids, addresses = set(), set()
    fields = {
        "id",
        "verse",
        "path",
        "before_sha256",
        "after_sha256",
        "canonical_sha256",
        "value",
        "atoms",
    }
    for row in data["records"]:
        if set(row) != fields:
            raise ValueError("Unexpected metadata in frozen pointing record")
        if any(
            not _HEX.fullmatch(row[key])
            for key in ("before_sha256", "after_sha256", "canonical_sha256")
        ):
            raise ValueError("Invalid frozen pointing digest")
        address = (tuple(row["verse"]), tuple(row["path"]))
        if row["id"] in ids or address in addresses:
            raise ValueError("Duplicate frozen pointing target")
        ids.add(row["id"])
        addresses.add(address)
        validate_value(row["value"])
    if len(ids) != SITES or sum(row["atoms"] for row in data["records"]) != ATOMS:
        raise ValueError("Approved frozen pointing population changed")
    return data


def load():
    raw = MANIFEST.read_bytes()
    if sha256(raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError("Frozen pointing manifest differs from the sealed hash")
    return validate_manifest(json.loads(raw))


class FrozenPointing:
    def __init__(self, input_dir):
        self.data = load()
        actual = {
            p.name: sha256(p.read_bytes()).hexdigest()
            for p in sorted(input_dir.glob("*.json"))
        }
        if actual != self.data["input_sha256"]:
            raise ValueError("MAM inputs differ from the sealed pointing target")
        self.by_verse = defaultdict(list)
        for row in self.data["records"]:
            self.by_verse[tuple(row["verse"])].append(row)
        self.seen = set()

    def check_source(self, cell, verse):
        for row in self.by_verse[verse]:
            target = at_path(cell, row["path"])
            if digest(target) != row["before_sha256"]:
                raise ValueError(f"{row['id']}: phase-3 source target changed")

    def apply(self, cell, verse):
        # Validate every target in this verse before mutating any of them.
        targets = []
        for row in self.by_verse[verse]:
            target = at_path(cell, row["path"])
            if target["tmpl_name"] not in phase2.POINTED_KETIV_FAMILIES:
                raise ValueError(f"{row['id']}: unsupported target family")
            if phase2.POINTED_KETIV_PARAMETER in target["tmpl_params"]:
                raise ValueError(
                    f"{row['id']}: existing note pointing takes priority; import conflict"
                )
            if digest(target) != row["after_sha256"] or row["id"] in self.seen:
                raise ValueError(
                    f"{row['id']}: changed or repeated post-Readings target"
                )
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
            raise ValueError(
                "Frozen pointing import did not consume the exact approved set"
            )
