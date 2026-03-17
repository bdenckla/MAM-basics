"""
Serialize classified MPP diffs to JSON (pre-expansion form).

Exports:
    write_json  — write the JSON diff file
"""

import difflib
import json
import os

from pydiff_mpp.mpp_extract import _collect_template_names


def _narrow_to_changed_words(old_text, new_text):
    """Return list of {"old": ..., "new": ...} dicts for changed word spans."""
    old_words = old_text.split(" ")
    new_words = new_text.split(" ")
    sm = difflib.SequenceMatcher(None, old_words, new_words, autojunk=False)
    pairs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        if op == "replace" and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                ow = old_words[i1 + k]
                nw = new_words[j1 + k]
                if ow != nw:
                    pairs.append({"old": ow, "new": nw})
        else:
            pairs.append(
                {
                    "old": " ".join(old_words[i1:i2]),
                    "new": " ".join(new_words[j1:j2]),
                }
            )
    if not pairs:
        pairs.append({"old": old_text, "new": new_text})
    return pairs


def _serialize_diff(d):
    """Build the JSON-serializable dict for one diff."""
    out = {
        "book": d["book"],
        "chapter": d["chapter"],
        "verse": d["verse"],
        "category": d["category"],
    }
    if d["text_changed"]:
        out["changes"] = _narrow_to_changed_words(d["old_text"], d["new_text"])
    else:
        old_names = sorted(set(_collect_template_names(d["old_ep"])))
        new_names = sorted(set(_collect_template_names(d["new_ep"])))
        added = sorted(set(new_names) - set(old_names))
        removed = sorted(set(old_names) - set(new_names))
        if added:
            out["templates_added"] = added
        if removed:
            out["templates_removed"] = removed
    if d["nusach_notes"]:
        out["nusach_notes"] = d["nusach_notes"]
    return out


def write_json(diffs, old_rev, new_rev, out_path):
    """Write the abstract diff data to a JSON file.

    For text-changed diffs, includes narrowed word-level change pairs
    rather than full verse text.  For structural diffs, includes the
    template names added/removed.  Excludes the bulky old_ep / new_ep
    raw MPP structures.
    """
    serialized = [_serialize_diff(d) for d in diffs]
    data = {
        "old_rev": old_rev,
        "new_rev": new_rev,
        "diff_count": len(serialized),
        "diffs": serialized,
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
