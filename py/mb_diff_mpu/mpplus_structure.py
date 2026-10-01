"""Template-structure helpers for MAM-parsed-plus diffing.

This is a deliberate whole-structure inventory, not a selected Scripture-text
projection.  Every classified structural parameter is included, so a template added,
removed, reordered or moved to another parameter inside a ketiv/qere, qamats,
dual-cantillation, or stress-helper alternative remains visible.  The inventory records
template names and positions, not strings: a changed string inside an alternative that
the selected Scripture projection does not take is visible only where the separate
alternative population below compares it.
The ``נוסח`` wrapper and its documentation parameter 2 are excluded while its
Scripture target in parameter 1 is included.  ``מ:הערה-2`` and its historical
predecessor likewise contribute only their target in parameter 1: parameter 2 is
note prose and parameter 3 is mark-position metadata.  New template names fail
until their parameter roles are classified.

The separate alternative population follows the existing selected Scripture
traversal and compares only the approved trivial-template qere and deḥi
stress-helper role. It does not derive those roles from the structural inventory.

Exports:
    collect_template_names      — gather relevant template names from an EP tree
    template_name_counter       — count template-name multiplicities
    template_name_multiset_delta — compute added/removed template-name multiplicities
    structural_signature        — build a position-aware structural signature
    alternative_changes         — compare the approved Scripture alternatives
    normalized_trivial_qere_content — prove a recognized rename's content equal

Private helpers:
    _semantic_param_items        — normalize historical parameter encodings
"""

from collections import Counter
import difflib
import re

from mb_cmn import retired_kq_special_templates as rkqst
from mb_cmn import template_names
from mb_cmn import unicode_data
from mb_cmn.hebrew_punctuation import NU_GMAQ, PASOLEG
from mb_cmn.str_defs import DOUB_VERT_LINE
from mb_cmn.uni_denorm import give_std_mark_order
from mb_diff_mpu.mpplus_param_access import MISSING, get_param


def collect_template_names(obj):
    """Collect names in all classified structural branches, excluding note prose."""
    names = []
    if isinstance(obj, dict):
        if "tmpl_name" in obj:
            if obj["tmpl_name"] == "נוסח":
                for _key, value in _classified_param_items_for_structure(obj):
                    names.extend(collect_template_names(value))
                return names
            names.append(_canonical_template_name_for_structure(obj))
            for _key, value in _classified_param_items_for_structure(obj):
                names.extend(collect_template_names(value))
            return names
        for key in sorted(obj):
            names.extend(collect_template_names(obj[key]))
    elif isinstance(obj, list):
        for item in obj:
            names.extend(collect_template_names(item))
    elif not isinstance(obj, str):
        raise TypeError(
            f"unclassified MAM-parsed-plus structure node: {type(obj).__name__}"
        )
    return names


def template_name_counter(obj):
    """Return a Counter of relevant template names in an EP structure."""
    return Counter(collect_template_names(obj))


def template_name_multiset_delta(old_ep, new_ep):
    """Return net added/removed template names, preserving multiplicity."""
    old_counts = template_name_counter(old_ep)
    new_counts = template_name_counter(new_ep)
    added = sorted((new_counts - old_counts).elements())
    removed = sorted((old_counts - new_counts).elements())
    return added, removed


def _sort_param_keys(keys):
    """Sort semantic parameter keys numerically, then lexically."""
    return sorted(keys, key=lambda key: (0, int(key)) if key.isdigit() else (1, key))


def _extract_named_arg(arg):
    """Return (key, value) for a named tmpl_args item, else None."""
    if isinstance(arg, str) and "=" in arg:
        key, value = arg.split("=", 1)
        return key, value
    if isinstance(arg, list) and arg and isinstance(arg[0], str) and "=" in arg[0]:
        key, head = arg[0].split("=", 1)
        tail = arg[1:]
        if not head and len(tail) == 1:
            value = tail[0]
        else:
            value = ([head] if head else []) + tail
        return key, value
    return None


def _semantic_param_items(tmpl):
    """Return normalized semantic parameter items for a template."""
    for dict_key in ("tmpl_params", "tmpl_args_dic"):
        d = tmpl.get(dict_key)
        if d is not None:
            return [(key, d[key]) for key in _sort_param_keys(d.keys())]
    args = tmpl.get("tmpl_args")
    if args is None:
        return []
    items = []
    positional_index = 1
    for arg in args:
        named = _extract_named_arg(arg)
        if named is not None:
            items.append(named)
            continue
        items.append((str(positional_index), arg))
        positional_index += 1
    return items


def _single_string_param(raw_value, param_name):
    if isinstance(raw_value, str):
        return raw_value
    if isinstance(raw_value, list):
        assert len(raw_value) == 1 and isinstance(raw_value[0], str), (
            param_name,
            raw_value,
        )
        return raw_value[0]
    assert False, (param_name, raw_value)


def _canonical_template_name_for_structure(tmpl):
    name = tmpl["tmpl_name"]
    if not rkqst.is_special_kq_template_name(name):
        return name
    sug_raw = get_param(tmpl, "סוג")
    sug_text = None if sug_raw is MISSING else _single_string_param(sug_raw, "סוג")
    return rkqst.canonical_special_kq_old_name_from_name_and_sug(name, sug_text)


def _normalized_param_items_for_structure(tmpl):
    items = _semantic_param_items(tmpl)
    name = tmpl["tmpl_name"]
    if rkqst.is_unified_special_kq_template_name(name):
        return [(key, value) for key, value in items if key != "סוג"]
    return items


_HISTORICAL_TEMPLATE_NAMES = frozenset(
    ("מ:לגרמיה", "קו״כ-אם", template_names.SCRDFF_NO_TAR)
)


def _classified_param_items_for_structure(tmpl):
    name = tmpl["tmpl_name"]
    if not (
        name in template_names.CURRENT_PLUS_TMPL_NAMES
        or name in _HISTORICAL_TEMPLATE_NAMES
        or rkqst.is_special_kq_template_name(name)
    ):
        raise ValueError(f"unclassified MAM-parsed-plus structure template: {name!r}")
    items = _normalized_param_items_for_structure(tmpl)
    if name in {"נוסח", template_names.SCRDFF_TAR, template_names.SCRDFF_NO_TAR}:
        return [(key, value) for key, value in items if key == "1"]
    return items


def _structure_occurrences(obj, path=()):
    """Collect template occurrences with semantic ancestry and content order."""
    if isinstance(obj, str):
        return []
    if isinstance(obj, list):
        occurrences = []
        for item in obj:
            occurrences.extend(_structure_occurrences(item, path))
        return occurrences
    if not isinstance(obj, dict):
        raise TypeError(
            f"unclassified MAM-parsed-plus structure node: {type(obj).__name__}"
        )
    if "tmpl_name" not in obj:
        occurrences = []
        for key in sorted(obj):
            occurrences.extend(
                _structure_occurrences(obj[key], path + (("dict", key),))
            )
        return occurrences

    name = _canonical_template_name_for_structure(obj)
    if obj["tmpl_name"] == "נוסח":
        occurrences = []
        for _key, value in _classified_param_items_for_structure(obj):
            occurrences.extend(_structure_occurrences(value, path))
        return occurrences
    occurrences = [(path, name)]
    child_path = path + (("tmpl", name),)
    for key, value in _classified_param_items_for_structure(obj):
        occurrences.extend(
            _structure_occurrences(value, child_path + (("param", key),))
        )
    return occurrences


def structural_signature(ep):
    """Return a normalized, position-aware structural signature for EP."""
    return tuple(_structure_occurrences(ep))


# This population is separate from the whole-structure inventory above.  Find the
# two approved alternatives only on the existing selected Scripture traversal;
# entering every parameter would invent roles in other alternatives or note prose.
_OLD_TRIVIAL_QERE = "קו״כ-אם"
_QERE_SOURCE_PREFIXES = frozenset(
    ("קרי", "א-קרי", "א,ל-קרי", "אל-קרי", "ל-קרי", "ל-קרי,ק13-קרי", "ל1,ק3-קרי")
)
_PARAM1_ROLE_TARGETS = (
    template_names.IN_WORD_TMPL_NAMES
    | template_names.STRESS_HELPER_TMPL_NAMES
    | {template_names.SCRDFF_TAR, "מודגש", "מ:סיום בטוב", "נוסח"}
)
_DROPPED_ROLE_TARGETS = frozenset(
    (
        template_names.INVERTED_NUN,
        template_names.SCRDFF_NO_TAR,
        "מ:קישור בהערה",
        "מ:קישור פנימי בהערה",
        "כתיב ולא קרי",
    )
)


def _positional_role_arg(value, number):
    """Remove a written positional key without treating source text as a key."""
    prefix = f"{number}="
    if isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    if (
        isinstance(value, list)
        and value
        and isinstance(value[0], str)
        and value[0].startswith(prefix)
    ):
        head = value[0][len(prefix) :]
        tail = value[1:]
        return (
            tail[0] if not head and len(tail) == 1 else ([head] if head else []) + tail
        )
    return value


def _alternative_role_params(tmpl):
    """Validate recognized current or historical shapes for the role traversal."""
    if not isinstance(tmpl, dict) or not isinstance(tmpl.get("tmpl_name"), str):
        raise TypeError(f"not a MAM-parsed-plus alternative template: {tmpl!r}")
    name = tmpl["tmpl_name"]
    allowed_object_keys = {"tmpl_name", "tmpl_args", "tmpl_params", "tmpl_args_dic"}
    if set(tmpl) - allowed_object_keys:
        raise ValueError(f"unexpected object keys for alternative template {name!r}")
    if "tmpl_args" in tmpl and not isinstance(tmpl["tmpl_args"], list):
        raise TypeError(f"non-list historical arguments for {name!r}")
    for key in ("tmpl_params", "tmpl_args_dic"):
        if key in tmpl and not isinstance(tmpl[key], dict):
            raise TypeError(f"non-mapping alternative parameters for {name!r}")
    if "tmpl_params" in tmpl and "tmpl_args_dic" in tmpl:
        if tmpl["tmpl_params"] != tmpl["tmpl_args_dic"]:
            raise ValueError(f"conflicting alternative parameter mappings for {name!r}")
    mapped = "tmpl_params" in tmpl or "tmpl_args_dic" in tmpl
    if not mapped and name in {_OLD_TRIVIAL_QERE, "נוסח"}:
        args = tmpl.get("tmpl_args", [])
        if len(args) != 2:
            raise ValueError(f"historical {name!r} requires two positional arguments")
        params = {
            str(number): _positional_role_arg(value, number)
            for number, value in enumerate(args, 1)
        }
    else:
        items = _semantic_param_items(tmpl)
        params = dict(items)
        if len(params) != len(items):
            raise ValueError(f"duplicate alternative parameters for {name!r}")
    if name == _OLD_TRIVIAL_QERE or rkqst.is_old_special_kq_template_name(name):
        required = allowed = frozenset({"1", "2"})
    elif name == "מ:לגרמיה":
        required = allowed = frozenset()
    elif name == template_names.SCRDFF_NO_TAR:
        required, allowed = frozenset({"1"}), frozenset({"1", "שם"})
    elif not mapped and name in template_names.STRESS_HELPER_TMPL_NAMES:
        required, allowed = frozenset({"1"}), frozenset({"1", "2"})
    elif not mapped and name == "כתיב ולא קרי":
        required, allowed = frozenset({"1"}), frozenset({"1", "2", "3"})
    elif not mapped and name == "קרי ולא כתיב":
        required, allowed = frozenset({"1"}), frozenset({"1", "2"})
    else:
        policy = template_names.CURRENT_PLUS_PARAM_POLICY.get(name)
        if policy is None:
            raise ValueError(
                f"unclassified MAM-parsed-plus alternative template: {name!r}"
            )
        required, allowed = policy
    actual = frozenset(params)
    if not required <= actual or not actual <= allowed:
        raise ValueError(
            f"unexpected alternative parameters for {name!r}: required "
            f"{sorted(required)!r}, allowed {sorted(allowed)!r}, got {sorted(actual)!r}"
        )
    if name == template_names.TRIVIAL_QERE:
        for key in ("2", "מקורות", "סוג"):
            if key in params:
                value = params[key]
                if not (
                    isinstance(value, str)
                    or (
                        isinstance(value, list)
                        and len(value) == 1
                        and isinstance(value[0], str)
                    )
                ):
                    raise ValueError(f"non-text trivial-template metadata {key!r}")
    if rkqst.is_special_kq_template_name(name):
        sug = params.get("סוג")
        sug = None if sug is None else _single_string_param(sug, "סוג")
        rkqst.canonical_special_kq_type_from_name_and_sug(name, sug)
    return params


def _selected_role_target(name, params):
    """Name the existing selected Scripture child or literal for each template."""
    if name in _PARAM1_ROLE_TARGETS or name in {
        _OLD_TRIVIAL_QERE,
        template_names.TRIVIAL_QERE,
    }:
        return "child", params["1"]
    if (
        name in template_names.STD_KQ_TMPL_NAMES
        or rkqst.is_old_special_kq_template_name(name)
    ):
        return "child", params["2"]
    if name == "קרי ולא כתיב":
        return "qere-only", params.get("2", params["1"])
    if name == template_names.QAMATS_VARIANT:
        return "child", params["ד"]
    if name == template_names.DUAL_CANTILLATION:
        return "child", params["כפול"]
    if name in {"מ:לגרמיה", "מ:לגרמיה-2"}:
        return "literal", PASOLEG
    if name == "מ:פסק":
        return "literal", DOUB_VERT_LINE
    if name == "מ:מקף אפור":
        return "literal", NU_GMAQ
    if name in template_names.NO_ATOM_TMPL_NAMES or name == "ש":
        return "literal", " "
    if name in _DROPPED_ROLE_TARGETS:
        return "literal", ""
    raise ValueError(f"unclassified MAM-parsed-plus alternative target: {name!r}")


def _alternative_text(node):
    """Read an alternative's Scripture text with closed template/shape dispatch."""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "".join(_alternative_text(item) for item in node)
    if not isinstance(node, dict):
        raise TypeError(f"unclassified alternative node: {type(node).__name__}")
    params = _alternative_role_params(node)
    role, value = _selected_role_target(node["tmpl_name"], params)
    if role == "literal":
        return value
    text = _alternative_text(value)
    return text.replace("[", "").replace("]", "") if role == "qere-only" else text


def _historical_qere_value(raw):
    """Decode the old qere role, excluding its source and parenthetical metadata."""
    if isinstance(raw, str):
        head, tail = raw, []
    elif isinstance(raw, list) and raw and isinstance(raw[0], str):
        head, tail = raw[0], raw[1:]
    else:
        raise ValueError(f"unrecognized historical qere value: {raw!r}")
    if head.startswith("ל=יתיר י' (קרי="):
        match = re.fullmatch(r"ל=יתיר י' \(קרי=([^()]*)\)", head)
        if match is None or tail:
            raise ValueError(f"malformed historical qere metadata: {raw!r}")
        head = match[1]
    else:
        if "=" in head:
            source, head = head.split("=", 1)
            if source not in _QERE_SOURCE_PREFIXES:
                raise ValueError(f"unrecognized historical qere source: {source!r}")
        if "(" in head or ")" in head:
            match = re.fullmatch(r"([^()]*) \([^()]*\)", head)
            if match is None or tail:
                raise ValueError(f"malformed historical qere metadata: {raw!r}")
            head = match[1]
    return [head, *tail]


def _normalized_alternative_text(node):
    # A historical written paseq and its parsed template may differ only by the
    # separating space.  MAM mark order, rather than Unicode normalization, keeps
    # the two retained Scripture values comparable.
    return give_std_mark_order(_alternative_text(node)).replace(" " + PASOLEG, PASOLEG)


def _alternative_instances(ep):
    instances = []
    counts = Counter()

    def visit(node):
        if isinstance(node, str):
            return
        if isinstance(node, list):
            for item in node:
                visit(item)
            return
        if not isinstance(node, dict):
            raise TypeError(f"unclassified alternative node: {type(node).__name__}")
        name = node["tmpl_name"]
        params = _alternative_role_params(node)
        family = None
        if name in {_OLD_TRIVIAL_QERE, template_names.TRIVIAL_QERE}:
            family, role = template_names.TRIVIAL_QERE, "qere"
            raw = (
                _historical_qere_value(params["2"])
                if name == _OLD_TRIVIAL_QERE
                else params["3"]
            )
        elif name == "מ:דחי":
            family, role = name, "stress-helper-alternative"
            # The oldest recognized format permits no second argument or an
            # empty second argument; both mean that no alternative was supplied.
            raw = params.get("2", [])
        if family is not None:
            counts[family] += 1
            value = _normalized_alternative_text(raw)
            if role == "qere" and not value:
                raise ValueError("empty required qere alternative")
            instances.append(
                {
                    "template": family,
                    "occurrence": counts[family],
                    "role": role,
                    "selected": _normalized_alternative_text(params["1"]),
                    "value": value,
                }
            )
        child_role, child = _selected_role_target(name, params)
        if child_role != "literal":
            visit(child)

    visit(ep)
    return instances


def normalized_trivial_qere_content(ep):
    """Return selected/qere content used to prove a trivial-template rename equal."""
    return tuple(
        (item["selected"], item["value"])
        for item in _alternative_instances(ep)
        if item["role"] == "qere"
    )


def alternative_changes(old_ep, new_ep):
    """Compare the approved qere and stress-helper roles independently of body text.

    Existing instances pair in reading order.  When a family population changes,
    equal selected targets anchor the surviving instances; unmatched additions or
    removals keep their existing structural classification and presentation.
    """
    old_instances = _alternative_instances(old_ep)
    new_instances = _alternative_instances(new_ep)
    changes = []
    for family in (template_names.TRIVIAL_QERE, "מ:דחי"):
        old = [item for item in old_instances if item["template"] == family]
        new = [item for item in new_instances if item["template"] == family]
        if len(old) == len(new):
            pairs = list(zip(old, new))
        else:
            matcher = difflib.SequenceMatcher(
                None,
                [item["selected"] for item in old],
                [item["selected"] for item in new],
                autojunk=False,
            )
            pairs = []
            for op, i1, i2, j1, j2 in matcher.get_opcodes():
                if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
                    pairs.extend(zip(old[i1:i2], new[j1:j2]))
        for before, after in pairs:
            if before["value"] == after["value"]:
                continue
            old_value, new_value = before["value"], after["value"]
            unpointed_old = "".join(c for c in old_value if not unicode_data.is_mark(c))
            unpointed_new = "".join(c for c in new_value if not unicode_data.is_mark(c))
            migration = (
                after["role"] == "qere"
                and old_value == unpointed_old
                and old_value != new_value
                and unpointed_old == unpointed_new
            )
            changes.append(
                {
                    "template": family,
                    "occurrence": after["occurrence"],
                    "role": after["role"],
                    "kind": "pointing-migration" if migration else "content",
                    "old": old_value,
                    "new": new_value,
                }
            )
    return changes
