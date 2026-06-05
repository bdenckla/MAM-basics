"""Expand structural MAM-parsed-plus diffs into note-scoped sub-diffs when needed."""

from mb_diff_mpu.mpplus_structure import template_name_multiset_delta
from mb_diff_mpu.mpplus_template_change_desc import kq_if_template_addition_parts_list

_TEMPLATE_REMOVAL_CATS = {
    "מ:דחי": "dexi-removal",
    "מ:צינור": "tsinnor-removal",
}

_KQ_TRIVIAL_NAMES = frozenset(["קו״כ-אם", "מ:קו״כ-אם-2"])


def _split_kq_if_additions(diff):
    """Split pure trivial-kq additions into one sub-diff per added instance."""
    added, removed = template_name_multiset_delta(diff["old_ep"], diff["new_ep"])
    if removed or not added or any(name not in _KQ_TRIVIAL_NAMES for name in added):
        return None

    additions = kq_if_template_addition_parts_list(diff)
    if not additions:
        return None

    notes = diff.get("docnote_notes", [])
    subs = []
    for addition in additions:
        sub = dict(diff)
        sub["templates_added"] = [addition["template_name"]]
        sub["templates_removed"] = []
        sub["kq_if_template_addition"] = {
            "template_name": addition["template_name"],
            "arg1_text": addition["arg1_text"],
            "arg2_text": addition["arg2_text"],
        }
        sub["docnote_notes"] = [
            note
            for note in notes
            if note["end"] > addition["start"] and note["start"] < addition["end"]
        ]
        subs.append(sub)
    return subs


def _is_kq_trivial_rename(diff):
    """Return True if diff is a pure bot-edit rename: קו״כ-אם → מ:קו״כ-אם-2."""
    added, removed = template_name_multiset_delta(diff["old_ep"], diff["new_ep"])
    if not added or not removed:
        return False
    if not all(n == "קו״כ-אם" for n in removed):
        return False
    if not all(n == "מ:קו״כ-אם-2" for n in added):
        return False
    return len(added) == len(removed)


def split_structural_diff(diff):
    """Split structural diffs that should render as separate cards."""
    if _is_kq_trivial_rename(diff):
        return []
    kq_if_split = _split_kq_if_additions(diff)
    if kq_if_split is not None:
        return kq_if_split

    added, removed = template_name_multiset_delta(diff["old_ep"], diff["new_ep"])
    splittable = set(removed) & _TEMPLATE_REMOVAL_CATS.keys()
    if added or len(splittable) < 2:
        return None

    notes = diff.get("docnote_notes", [])
    subs = []
    for i, tname in enumerate(sorted(splittable)):
        sub = dict(diff)
        sub["category"] = _TEMPLATE_REMOVAL_CATS[tname]
        sub["templates_added"] = []
        sub["templates_removed"] = [tname]
        sub["docnote_notes"] = notes if i == 0 else []
        subs.append(sub)
    return subs
