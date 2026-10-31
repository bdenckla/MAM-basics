"""Reviewed literal clause projections; no selection policy or manuscript inference.

Recipes are explicitly supplied by the edition's pinned review ledger and are
never inferred by the renderer.
"""

import hashlib
import json
import re

from mb_cmn import hebrew_points as hpo
from mb_cmn import uni_denorm

_CLUSTER = "[א-ת]" + hpo.RE_APCV_STAR


def signature(target, mam_target, parts):
    """Identify the complete presentation inputs, including unburied source parts."""
    text = json.dumps([target, mam_target, parts], ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def quoting(rest, form):
    """Split a clause's text after its source head's "=" for a recast, or return None.

    Return the recast clause's text after its source head, and the original text
    rebuilt from the same pieces. Two shapes quote the complete ``form``. In the
    first, ``rest`` is ``form``, alone or followed by a space, and the recast drops
    ``form``, which the lemma shows. In the second, ``rest`` is a plus form of
    ``form`` followed by ``form`` in parentheses, alone or followed by a space; the
    recast drops ``form`` and keeps the plus form in parentheses, since it explains
    what the source has, as the clause's prose does (Ben, 2026-10-30).
    """
    if rest == form or rest.startswith(form + " "):
        suffix = rest[len(form) :]
        return suffix, form + suffix
    plus, space, after = rest.partition(" ")
    quoted = "(" + form + ")"
    if not space or (after != quoted and not after.startswith(quoted + " ")):
        return None
    if fold_plus(plus) != form:
        return None
    suffix = after[len(quoted) :]
    return " (" + plus + ")" + suffix, plus + " " + quoted + suffix


def fold_plus(plus_form):
    """The packed form that ``plus_form`` writes in plus notation, or None.

    Plus notation writes one letter twice, joined by a plus sign, with some of the
    letter's marks on each copy. The packed form writes that letter once with the
    marks of both copies, a mark on both copies once, in MAM's standard mark order.
    """
    if plus_form.count("+") != 1:
        return None
    before, after = plus_form.split("+")
    last = re.search(_CLUSTER + "$", before)
    first = re.match(_CLUSTER, after)
    if not last or not first or last.group()[0] != first.group()[0]:
        return None
    marks = last.group()[1:]
    marks += "".join(mark for mark in first.group()[1:] if mark not in marks)
    packed = before[: last.start()] + last.group()[0] + marks + after[first.end() :]
    return uni_denorm.give_std_mark_order(packed)


def project(parts, target, index):
    """Return a near-subject clause and the untouched remaining source clauses.

    Rebuild the original clause from the recast's pieces to reconstruct it byte for
    byte. This is a loss check against the preserved input, not a semantic review.
    """
    if len(target) != 1 or not isinstance(target[0], str):
        raise AssertionError("Recast requires one complete plain target")
    if not 0 <= index < len(parts):
        raise AssertionError("Recast clause index is outside the note")
    part = parts[index]
    if len(part) != 1 or not isinstance(part[0], str):
        raise AssertionError("Recast requires one plain source clause")
    head, equals, rest = part[0].partition("=")
    if not equals or not head or " " in head or "=" in rest:
        raise AssertionError("Recast requires a single leading source relation")
    split = quoting(rest, target[0])
    if split is None:
        raise AssertionError("Recast does not quote the complete target")
    near, original = split
    promoted = ["=" + head + near]
    restored = [[head + "=" + original]]
    remaining = parts[:index] + parts[index + 1 :]
    if remaining[:index] + restored + remaining[index:] != parts:
        raise AssertionError("Recast lost or duplicated source content")
    return promoted, remaining
