"""Helpers for structural template-change descriptions in MPP diff cards."""

from pydiff_mpp.mpp_extract import _MISSING, _flatten_element, _get_param


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


def kq_if_template_addition_parts(diff):
    """Return extracted parts for a pure קו"כ-אם addition.

    Returns a dict with template_name, arg1_text, and arg2_text.
    Assertions enforce the invariants expected for this change type.
    """
    old_instances = list(_iter_named_templates(diff["old_ep"], 'קו"כ-אם'))
    new_instances = list(_iter_named_templates(diff["new_ep"], 'קו"כ-אם'))
    assert not old_instances, 'Expected no existing קו"כ-אם in old_ep'
    assert len(new_instances) == 1, (
        'Expected exactly one added קו"כ-אם in new_ep, ' f"found {len(new_instances)}"
    )

    tmpl = new_instances[0]
    p1 = _get_param(tmpl, "1")
    p2 = _get_param(tmpl, "2")
    assert p1 is not _MISSING, 'Expected קו"כ-אם to have param "1"'

    p1_text = _flatten_element(p1)
    p2_text = "<missing>" if p2 is _MISSING else _flatten_element(p2)
    assert p1_text in diff["old_text"], (
        "Expected old flattened text to already contain the raw text of "
        'the new קו"כ-אם param "1"'
    )

    return {
        "template_name": 'קו"כ-אם',
        "arg1_text": p1_text,
        "arg2_text": p2_text,
    }
