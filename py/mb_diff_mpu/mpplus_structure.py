"""Template-structure helpers for MAM-parsed-plus diffing.

This is a deliberate whole-structure inventory, not a selected Scripture-text
projection.  Every classified structural parameter is included so a change inside a
ketiv/qere, qamats, dual-cantillation, or stress-helper alternative remains visible.
The ``נוסח`` wrapper and its documentation parameter 2 are excluded while its
Scripture target in parameter 1 is included.  ``מ:הערה-2`` and its historical
predecessor likewise contribute only their target in parameter 1: parameter 2 is
note prose and parameter 3 is mark-position metadata.  New template names fail
until their parameter roles are classified.

Exports:
    collect_template_names      — gather relevant template names from an EP tree
    template_name_counter       — count template-name multiplicities
    template_name_multiset_delta — compute added/removed template-name multiplicities
    structural_signature        — build a position-aware structural signature

Private helpers:
    _semantic_param_items        — normalize historical parameter encodings
"""

from collections import Counter

from mb_cmn import retired_kq_special_templates as rkqst
from mb_cmn import template_names
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
