"""Helpers for structural template-change descriptions in MPP diff cards."""

from collections import Counter

from pydiff_mpp.mpp_flatten import (
    _flatten_element,
    _is_ketiv_velo_qere_template,
    _is_parashah_template,
    _is_qere_velo_ketiv_template,
    _is_std_kq_template,
    _is_trivial_kq_template,
)
from pydiff_mpp.mpp_param_access import _MISSING, _get_param


def _iter_named_templates(obj, template_name):
    """Yield every template dict with a matching tmpl_name."""
    if isinstance(obj, dict):
        if obj.get("tmpl_name") == template_name:
            yield obj
        for value in obj.values():
            yield from _iter_named_templates(value, template_name)
    elif isinstance(obj, list):
        for item in obj:
            yield from _iter_named_templates(item, template_name)


def _collect_named_template_instances(ep, template_name):
    """Collect named template instances with flattened text spans."""
    parts = []
    instances = []
    for el in ep:
        _collect_named_template_tracking(el, template_name, parts, instances)
    return instances


def _collect_named_template_tracking(obj, template_name, parts, instances):
    if isinstance(obj, str):
        parts.append(obj)
        return
    if isinstance(obj, list):
        for item in obj:
            _collect_named_template_tracking(item, template_name, parts, instances)
        return
    if isinstance(obj, dict):
        _collect_named_template_from_template(obj, template_name, parts, instances)


def _collect_named_template_from_template(tmpl, template_name, parts, instances):
    name = tmpl["tmpl_name"]
    if _is_parashah_template(name):
        parts.append(" ")
        return
    if name == template_name:
        start = sum(len(part) for part in parts)
        p1 = _get_param(tmpl, "1")
        if p1 is not _MISSING:
            _collect_named_template_tracking(p1, template_name, parts, instances)
        end = sum(len(part) for part in parts)
        p2 = _get_param(tmpl, "2")
        p1_text = "<missing>" if p1 is _MISSING else _flatten_element(p1)
        p2_text = "<missing>" if p2 is _MISSING else _flatten_element(p2)
        instances.append(
            {
                "template_name": template_name,
                "arg1_text": p1_text,
                "arg2_text": p2_text,
                "start": start,
                "end": end,
            }
        )
        return
    if name == "נוסח":
        p1 = _get_param(tmpl, "1")
        if p1 is not _MISSING:
            _collect_named_template_tracking(p1, template_name, parts, instances)
        return
    if _is_std_kq_template(name) or _is_qere_velo_ketiv_template(name):
        param = _get_param(tmpl, "2")
        if param is not _MISSING:
            _collect_named_template_tracking(param, template_name, parts, instances)
        return
    if _is_trivial_kq_template(name):
        param = _get_param(tmpl, "1")
        if param is not _MISSING:
            _collect_named_template_tracking(param, template_name, parts, instances)
        return
    if _is_ketiv_velo_qere_template(name):
        return
    if name == "מ:קמץ":
        pd = _get_param(tmpl, "ד")
        if pd is not _MISSING:
            _collect_named_template_tracking(pd, template_name, parts, instances)
        return
    if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
        parts.append("׀")
        return
    if name == "מ:פסק":
        parts.append("׀")
        return
    if name == "מ:כפול":
        pk = _get_param(tmpl, "כפול")
        if pk is not _MISSING:
            _collect_named_template_tracking(pk, template_name, parts, instances)
        return
    p1 = _get_param(tmpl, "1")
    if p1 is not _MISSING:
        _collect_named_template_tracking(p1, template_name, parts, instances)


def kq_if_template_addition_parts_list(diff):
    """Return added קו"כ-אם instances in new-EP order with text spans."""
    old_instances = _collect_named_template_instances(diff["old_ep"], 'קו"כ-אם')
    new_instances = _collect_named_template_instances(diff["new_ep"], 'קו"כ-אם')

    remaining_old = Counter(
        (instance["arg1_text"], instance["arg2_text"]) for instance in old_instances
    )
    added_instances = []
    for instance in new_instances:
        key = (instance["arg1_text"], instance["arg2_text"])
        if remaining_old[key]:
            remaining_old[key] -= 1
            continue
        assert instance["arg1_text"] in diff["old_text"], (
            "Expected old flattened text to already contain the raw text of "
            'the new קו"כ-אם param "1"'
        )
        added_instances.append(instance)
    return added_instances


def kq_if_template_addition_parts(diff):
    """Return extracted parts for a pure קו"כ-אם addition.

    Returns a dict with template_name, arg1_text, and arg2_text.
    Assertions enforce the invariants expected for this change type.
    """
    additions = kq_if_template_addition_parts_list(diff)
    assert len(additions) == 1, (
        'Expected exactly one added קו"כ-אם in new_ep, ' f"found {len(additions)}"
    )

    return {
        "template_name": additions[0]["template_name"],
        "arg1_text": additions[0]["arg1_text"],
        "arg2_text": additions[0]["arg2_text"],
    }
