"""Expand structural MPP diffs into note-scoped sub-diffs when needed."""

from pydiff_mpp.mpp_structure import _template_name_multiset_delta
from pydiff_mpp.mpp_template_change_desc import kq_if_template_addition_parts_list

_TEMPLATE_REMOVAL_CATS = {
    "מ:דחי": "dehi-removal",
    "מ:צינור": "tsinnor-removal",
}


def _split_kq_if_additions(diff):
    """Split pure קו"כ-אם additions into one sub-diff per added instance."""
    added, removed = _template_name_multiset_delta(diff["old_ep"], diff["new_ep"])
    if removed or not added or any(name != 'קו"כ-אם' for name in added):
        return None

    additions = kq_if_template_addition_parts_list(diff)
    if not additions:
        return None

    notes = diff.get("nusach_notes", [])
    subs = []
    for addition in additions:
        sub = dict(diff)
        sub["templates_added"] = ['קו"כ-אם']
        sub["templates_removed"] = []
        sub["kq_if_template_addition"] = {
            "template_name": addition["template_name"],
            "arg1_text": addition["arg1_text"],
            "arg2_text": addition["arg2_text"],
        }
        sub["nusach_notes"] = [
            note
            for note in notes
            if note["end"] > addition["start"] and note["start"] < addition["end"]
        ]
        subs.append(sub)
    return subs


def split_structural_diff(diff):
    """Split structural diffs that should render as separate cards."""
    kq_if_split = _split_kq_if_additions(diff)
    if kq_if_split is not None:
        return kq_if_split

    added, removed = _template_name_multiset_delta(diff["old_ep"], diff["new_ep"])
    splittable = set(removed) & _TEMPLATE_REMOVAL_CATS.keys()
    if added or len(splittable) < 2:
        return None

    notes = diff.get("nusach_notes", [])
    subs = []
    for i, tname in enumerate(sorted(splittable)):
        sub = dict(diff)
        sub["category"] = _TEMPLATE_REMOVAL_CATS[tname]
        sub["templates_added"] = []
        sub["templates_removed"] = [tname]
        sub["nusach_notes"] = notes if i == 0 else []
        subs.append(sub)
    return subs
