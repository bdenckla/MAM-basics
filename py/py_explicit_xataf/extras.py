"""Handling of "extras" — non-varika nusach notes that mention hataf."""

import json

from pycmn import file_io


def _read_extras_annotations():
    """Read manual annotations (category + translation) for extras."""
    path = "in/explicit-xataf-extras-annotations.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _annotate_extras(extras):
    """Merge extras with manual annotations for category and translation."""
    annotations = _read_extras_annotations()
    ann_by_key = {(a["ref"], a["target_word"]): a for a in annotations}
    # Also build ref-only index for entries with complex target_words
    ann_by_ref = {}
    for a in annotations:
        ann_by_ref.setdefault(a["ref"], []).append(a)
    for extra in extras:
        key = (extra["ref"], extra["target_word"])
        ann = ann_by_key.get(key)
        if ann is None:
            # Fall back to ref-only match (for complex flattened target_words)
            candidates = ann_by_ref.get(extra["ref"], [])
            if len(candidates) == 1:
                ann = candidates[0]
        extra["category"] = ann["category"] if ann else "uncategorized"
        extra["translation"] = ann["translation"] if ann else ""


def write_extras(all_extras):
    """Annotate and write extras to out/explicit-xataf-extras.json."""
    _annotate_extras(all_extras)
    result = {
        "header": {
            "description": (
                "Non-varika nusach notes that mention hataf. "
                "These are nusach notes whose target word does NOT contain "
                "varika (U+FB1E) but whose commentary text mentions "
                "hataf in some way."
            ),
            "categories": {
                "lc-differs": (
                    "LC (Leningrad Codex) differs from MAM regarding hataf: "
                    "either LC is missing hataf dots that MAM has, or LC "
                    "surprisingly has hataf where MAM does not."
                ),
                "ac-differs": (
                    "AC (Aleppo Codex) differs from MAM regarding hataf: "
                    "either AC has hataf where MAM has plain shewa or a "
                    "different vowel, or AC is missing hataf that MAM has."
                ),
                "hataf-qamats-for-qamats-qatan": (
                    "A manuscript uses hataf qamats to explicitly mark a "
                    "qamats qatan vowel, making the short pronunciation "
                    "visible in the pointing."
                ),
                "uncertain-hataf": (
                    "The note raises uncertainty about whether a mark in a "
                    "manuscript is actually hataf or something else (a stain, "
                    "smudge, or ambiguous mark)."
                ),
                "hataf-hiriq": (
                    "The note mentions hataf hiriq, a non-standard vowel "
                    "combination with no dedicated Unicode character, "
                    "represented as shewa+hiriq."
                ),
                "vowel-discussion": (
                    "General discussion of hataf in a grammatical, masoretic, "
                    "or comparative context, without a simple "
                    "manuscript-vs-MAM variant."
                ),
                "misc": "Cases that do not fit neatly into the other categories.",
            },
            "entry_fields": {
                "ref": "Verse reference",
                "target_word": (
                    "The target word (arg[0] of the nusach template), "
                    "flattened to plain text"
                ),
                "nusach_comment": (
                    "The full commentary text (arg[1] of the nusach template)"
                ),
                "category": "One of the categories defined above",
                "translation": (
                    "Tentative English translation/summary of the note's "
                    "hataf-related content"
                ),
            },
        },
        "entries": all_extras,
    }
    out_path = "out/explicit-xataf-extras.json"
    file_io.json_dump_to_file_path(result, out_path)
    n = len(all_extras)
    n_uncat = sum(1 for e in all_extras if e["category"] == "uncategorized")
    print(f"Wrote {n} extras to {out_path}", end="")
    if n_uncat:
        print(f" ({n_uncat} uncategorized)")
    else:
        print()
