"""Helpers for structural template-change descriptions in MAM-parsed-plus diff cards."""

from collections import Counter

from mb_cmn import retired_kq_special_templates as rkqst
from mb_diff_mpu.mpplus_flatten import (
    flatten_element,
    is_ketiv_velo_qere_template,
    is_parashah_template,
    is_qere_velo_ketiv_template,
    is_std_kq_template,
    is_trivial_kq_template,
)
from mb_diff_mpu.mpplus_param_access import MISSING, get_param


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


def _validate_special_kq_if_needed(tmpl):
    name = tmpl["tmpl_name"]
    if not rkqst.is_special_kq_template_name(name):
        return
    sug_raw = get_param(tmpl, "סוג")
    sug_text = None if sug_raw is MISSING else _single_string_param(sug_raw, "סוג")
    rkqst.canonical_special_kq_type_from_name_and_sug(name, sug_text)


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


def _arg2_param_key(template_name):
    """Return the param key to use as arg2_text for a trivial-kq template."""
    if template_name == 'מ:קו"כ-אם-2':
        return "3"
    return "2"


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
    if is_parashah_template(name):
        parts.append(" ")
        return
    if name == template_name:
        start = sum(len(part) for part in parts)
        p1 = get_param(tmpl, "1")
        if p1 is not MISSING:
            _collect_named_template_tracking(p1, template_name, parts, instances)
        end = sum(len(part) for part in parts)
        p2 = get_param(tmpl, _arg2_param_key(name))
        p1_text = "<missing>" if p1 is MISSING else flatten_element(p1)
        p2_text = "<missing>" if p2 is MISSING else flatten_element(p2)
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
        p1 = get_param(tmpl, "1")
        if p1 is not MISSING:
            _collect_named_template_tracking(p1, template_name, parts, instances)
        return
    if is_std_kq_template(name) or is_qere_velo_ketiv_template(name):
        _validate_special_kq_if_needed(tmpl)
        param = get_param(tmpl, "2")
        if param is not MISSING:
            _collect_named_template_tracking(param, template_name, parts, instances)
        return
    if is_trivial_kq_template(name):
        param = get_param(tmpl, "1")
        if param is not MISSING:
            _collect_named_template_tracking(param, template_name, parts, instances)
        return
    if is_ketiv_velo_qere_template(name):
        return
    if name == "מ:קמץ":
        pd = get_param(tmpl, "ד")
        if pd is not MISSING:
            _collect_named_template_tracking(pd, template_name, parts, instances)
        return
    if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
        parts.append("׀")
        return
    if name == "מ:פסק":
        parts.append("׀")
        return
    if name == "מ:כפול":
        pk = get_param(tmpl, "כפול")
        if pk is not MISSING:
            _collect_named_template_tracking(pk, template_name, parts, instances)
        return
    p1 = get_param(tmpl, "1")
    if p1 is not MISSING:
        _collect_named_template_tracking(p1, template_name, parts, instances)


_KQ_TRIVIAL_NAMES = ('קו"כ-אם', 'מ:קו"כ-אם-2')


def kq_if_template_addition_parts_list(diff):
    """Return added trivial-kq instances in new-EP order with text spans."""
    old_instances = [
        inst
        for name in _KQ_TRIVIAL_NAMES
        for inst in _collect_named_template_instances(diff["old_ep"], name)
    ]
    new_instances = sorted(
        (
            inst
            for name in _KQ_TRIVIAL_NAMES
            for inst in _collect_named_template_instances(diff["new_ep"], name)
        ),
        key=lambda x: x["start"],
    )
    # Match by arg1_text only: a קו"כ-אם and a מ:קו"כ-אם-2 with the same
    # pointed ketiv represent the same template instance (bot-edit rename).
    remaining_old = Counter(instance["arg1_text"] for instance in old_instances)
    added_instances = []
    for instance in new_instances:
        key = instance["arg1_text"]
        if remaining_old[key]:
            remaining_old[key] -= 1
            continue
        assert instance["arg1_text"] in diff["old_text"], (
            "Expected old flattened text to already contain the raw text of "
            'the new trivial-kq param "1"'
        )
        added_instances.append(instance)
    return added_instances


def kq_if_template_addition_parts(diff):
    """Return extracted parts for a pure trivial-kq addition.

    Returns a dict with template_name, arg1_text, and arg2_text.
    Assertions enforce the invariants expected for this change type.
    """
    additions = kq_if_template_addition_parts_list(diff)
    assert len(additions) == 1, (
        "Expected exactly one added trivial-kq in new_ep, " f"found {len(additions)}"
    )

    return {
        "template_name": additions[0]["template_name"],
        "arg1_text": additions[0]["arg1_text"],
        "arg2_text": additions[0]["arg2_text"],
    }
