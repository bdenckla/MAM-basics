"""Template-structure helpers for MPP diffing.

Exports:
    collect_template_names      — gather relevant template names from an EP tree
    template_name_counter       — count template-name multiplicities
    template_name_multiset_delta — compute added/removed template-name multiplicities
    structural_signature        — build a position-aware structural signature

Private helpers:
    _semantic_param_items        — normalize historical parameter encodings
"""

from collections import Counter

from pydiff_mpp.mpp_param_access import MISSING, get_param


def collect_template_names(obj):
    """Recursively collect template names relevant to body text."""
    names = []
    if isinstance(obj, dict):
        if "tmpl_name" in obj:
            if obj["tmpl_name"] == "נוסח":
                p1 = get_param(obj, "1")
                if p1 is not MISSING:
                    names.extend(collect_template_names(p1))
                return names
            names.append(obj["tmpl_name"])
        for value in obj.values():
            names.extend(collect_template_names(value))
    elif isinstance(obj, list):
        for item in obj:
            names.extend(collect_template_names(item))
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
        return []
    if "tmpl_name" not in obj:
        occurrences = []
        for key in sorted(obj):
            occurrences.extend(
                _structure_occurrences(obj[key], path + (("dict", key),))
            )
        return occurrences

    name = obj["tmpl_name"]
    if name == "נוסח":
        p1 = get_param(obj, "1")
        return [] if p1 is MISSING else _structure_occurrences(p1, path)

    occurrences = [(path, name)]
    child_path = path + (("tmpl", name),)
    for key, value in _semantic_param_items(obj):
        occurrences.extend(
            _structure_occurrences(value, child_path + (("param", key),))
        )
    return occurrences


def structural_signature(ep):
    """Return a normalized, position-aware structural signature for EP."""
    return tuple(_structure_occurrences(ep))
