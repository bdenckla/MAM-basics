"""Reviewed literal clause projections; no selection policy or manuscript inference.

Recipes are explicitly supplied by the edition's pinned review ledger and are
never inferred by the renderer.
"""

import hashlib
import json


def signature(target, mam_target, parts):
    """Identify the complete presentation inputs, including unburied source parts."""
    text = json.dumps([target, mam_target, parts], ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def project(parts, target, index):
    """Return a near-subject clause and the untouched remaining source clauses.

    Reinsert the quoted target to reconstruct the original clause byte for byte.
    This is a loss check against the preserved input, not a semantic review.
    """
    if len(target) != 1 or not isinstance(target[0], str):
        raise AssertionError("Recast requires one complete plain target")
    if not 0 <= index < len(parts):
        raise AssertionError("Recast clause index is outside the note")
    part = parts[index]
    if len(part) != 1 or not isinstance(part[0], str):
        raise AssertionError("Recast requires one plain source clause")
    head, equals, rest = part[0].partition("=")
    form = target[0]
    if not equals or not head or " " in head or "=" in rest:
        raise AssertionError("Recast requires a single leading source relation")
    if rest != form and not rest.startswith(form + " "):
        raise AssertionError("Recast does not quote the complete target")
    suffix = rest[len(form) :]
    promoted = ["=" + head + suffix]
    restored = [[head + "=" + form + suffix]]
    remaining = parts[:index] + parts[index + 1 :]
    if remaining[:index] + restored + remaining[index:] != parts:
        raise AssertionError("Recast lost or duplicated source content")
    return promoted, remaining
