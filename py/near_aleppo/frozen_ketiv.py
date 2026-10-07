"""Import an approved MAM-derived pointing payload after Readings.

Each record stores, beside its pointed ketiv, the parameters of the ketiv/qere
template it points, its ketiv and whole qere, as the build has them where the
pointing is written, after the representation policies and readings. There,
checked_target requires the template's parameters to be the record's still, so
that a changed ketiv, or a changed letter or mark of the qere, stops the build at
the record it concerns, while a renamed template does not. Runtime reads only the payload and current MAM input books.
Archival ownership evidence and approval diagnostics are not runtime dependencies.
"""

from collections import defaultdict
import copy
from hashlib import sha256
import json
from near_aleppo import build_paths
import re

from near_aleppo import phase2_templates as phase2

MANIFEST = build_paths.input_dir() / "frozen-pointed-ketiv.json"
_FORBIDDEN = re.compile(r"baseline-\d+|mgketer|https?://", re.IGNORECASE)
# The parameters a record's ketiv/qere template may have: MAM's ketiv and pointed
# qere, and the סוג of a מ:כו״ק מיוחד.
_TARGET_KEYS = frozenset({"1", "2", "סוג"})


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
    """Runtime values are text or existing orphan templates, with no provenance metadata."""
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


def validate_target_params(row):
    """Require a record's tmpl_params to hold "1" and "2", and at most also סוג,
    each a string."""
    params = row["tmpl_params"]
    if (
        not isinstance(params, dict)
        or not {"1", "2"} <= set(params) <= _TARGET_KEYS
        or not all(isinstance(value, str) for value in params.values())
    ):
        raise ValueError(f"{row['id']}: unexpected recorded target parameters")


def checked_target(cell, row):
    """The ketiv/qere template at ``row``'s path in ``cell``, checked against ``row``.

    The path must resolve to a template of phase2.POINTED_KETIV_FAMILIES that has no
    pointed ketiv yet, and the template's parameters must equal the record's. The
    template's name is not compared, so a rename such as כו״ק to קו״כ passes; a
    change to the ketiv, to any letter or mark of the qere, or to סוג raises.
    """
    try:
        target = at_path(cell, row["path"])
    except (IndexError, KeyError, TypeError) as error:
        raise ValueError(f"{row['id']}: the record's path does not resolve") from error
    if (
        not isinstance(target, dict)
        or target.get("tmpl_name") not in phase2.POINTED_KETIV_FAMILIES
    ):
        raise ValueError(
            f"{row['id']}: the record's path does not reach a template of "
            f"{phase2.POINTED_KETIV_FAMILIES}"
        )
    params = target["tmpl_params"]
    if phase2.POINTED_KETIV_PARAMETER in params:
        raise ValueError(
            f"{row['id']}: the target already has a pointed ketiv, which takes priority"
        )
    if params != row["tmpl_params"]:
        raise ValueError(
            f"{row['id']}: target parameters differ from the record: recorded "
            f"{_sorted_json(row['tmpl_params'])}, current {_sorted_json(params)}"
        )
    return target


def _sorted_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def validate_manifest(data):
    required = {"format", "algorithm_commit", "mam_input_commit", "records"}
    if set(data) != required or data["format"] != "near-aleppo-frozen-pointing-v2":
        raise ValueError("Unexpected frozen pointing manifest schema")
    if _FORBIDDEN.search(json.dumps(data, ensure_ascii=False)):
        raise ValueError("Attribution, baseline identity or URL in runtime manifest")
    ids, addresses = set(), set()
    fields = {"id", "verse", "path", "tmpl_params", "value"}
    for row in data["records"]:
        if set(row) != fields:
            raise ValueError("Unexpected metadata in frozen pointing record")
        validate_target_params(row)
        address = (tuple(row["verse"]), tuple(row["path"]))
        if row["id"] in ids or address in addresses:
            raise ValueError("Duplicate frozen pointing target")
        ids.add(row["id"])
        addresses.add(address)
        validate_value(row["value"])
    return data


def load():
    return validate_manifest(json.loads(MANIFEST.read_text(encoding="utf-8")))


class FrozenPointing:
    def __init__(self):
        self.data = load()
        self.by_verse = defaultdict(list)
        for row in self.data["records"]:
            self.by_verse[tuple(row["verse"])].append(row)
        self.seen = set()

    def apply(self, cell, verse):
        # Check every target in this verse before writing to any of them.
        targets = []
        for row in self.by_verse[verse]:
            if row["id"] in self.seen:
                raise ValueError(f"{row['id']}: frozen pointing applied twice")
            targets.append((row, checked_target(cell, row)))
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
