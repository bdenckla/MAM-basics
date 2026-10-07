"""Publish reviewed clauses with explicit near-Aleppo and MAM roles.

Reviews are validated against a pre-bake source replay before this phase starts.
The phase matches complete evidence, uses each review once, and changes only note
content. All editorial decisions remain in the review ledger.
"""

import copy

from near_aleppo import phase2_templates as phase2
from near_aleppo.phase6_rename import RENAMED_NOTES, LEGACY_NOTES
from py_misc import near_aleppo_params as nap


def body_from_parts(parts):
    """Store ordered clauses using MAM's explicit shin clause separator."""
    result = []
    for index, part in enumerate(parts):
        if index:
            result.append({"tmpl_name": "ש"})
        result.extend(copy.deepcopy(part))
    return result[0] if len(result) == 1 else result


def evidence_target(value, ref):
    """The pre-bake target spelling that the review ledger's evidence records."""
    value = copy.deepcopy(value)

    def walk(node):
        if isinstance(node, str):
            return
        if isinstance(node, list):
            for child in node:
                walk(child)
            return
        name = node["tmpl_name"]
        source = {new: old for old, new in RENAMED_NOTES.items()}.get(name, name)
        rule = phase2._RULES.get(source)
        if rule is None:
            raise AssertionError(f"{ref}: unknown evidence-target template {name}")
        params = node.get("tmpl_params", {})
        if rule.action == phase2._KEEP_NOTE:
            if name != source:
                node["tmpl_name"] = LEGACY_NOTES[source]
            walk(params["1"])
        elif rule.action == phase2._KEEP_KQ:
            phase2.selected_keys(node, ref)
            for key, child in params.items():
                if key not in phase2._FLAGS:
                    walk(child)
        elif rule.action not in (
            phase2._VERBATIM,
            phase2._COLLAPSE_WORD,
            phase2._CARRIERS,
        ):
            raise AssertionError(f"{ref}: unresolved evidence-target template {name}")

    walk(value)
    return value


class NoteContent:
    """Bake exactly one reviewed decision into each changed source note."""

    def __init__(self, ledger):
        self.rows = {
            (tuple(row["ref"]), row["note_ordinal"]): row for row in ledger["notes"]
        }
        if len(self.rows) != len(ledger["notes"]):
            raise AssertionError("Duplicate reviewed note identity")
        self.seen = set()

    def apply(self, cell, ref):
        ordinal = 0

        def walk(value):
            nonlocal ordinal
            if isinstance(value, str):
                return
            if isinstance(value, list):
                for child in value:
                    walk(child)
                return
            name = value["tmpl_name"]
            source_name = {new: old for old, new in RENAMED_NOTES.items()}.get(
                name, name
            )
            rule = phase2._RULES.get(source_name)
            if rule is None:
                raise AssertionError(f"{ref}: unknown note-content template {name}")
            params = value.get("tmpl_params", {})
            if rule.action == phase2._KEEP_NOTE:
                ordinal += 1
                identity = ref, ordinal
                if name in RENAMED_NOTES.values():
                    row = self.rows.get(identity)
                    if row is None or identity in self.seen:
                        raise AssertionError(
                            f"{identity}: missing or duplicated review"
                        )
                    if (
                        row["source_template"] != source_name
                        or row["near_target"] != evidence_target(params["1"], ref)
                        or row["original_target"] != params[nap.MAM_TARGET]
                        or row["original_body"] != params["2"]
                    ):
                        raise AssertionError(
                            f"{identity}: review evidence differs from build"
                        )
                    parts = row["review"]["proposed_parts"]
                    params["2"] = (
                        body_from_parts([parts["near_clause"]])
                        if parts["near_clause"] is not None
                        else []
                    )
                    params[nap.MAM_NOTE] = (
                        body_from_parts(parts["mam_clauses"])
                        if parts["near_clause"] is not None
                        else copy.deepcopy(row["original_body"])
                    )
                    nap.validate_baked_note(value)
                    self.seen.add(identity)
                elif identity in self.rows:
                    raise AssertionError(f"{identity}: reviewed target was not renamed")
                walk(params["1"])
            elif rule.action == phase2._KEEP_KQ:
                phase2.selected_keys(value, ref)
                for key, child in params.items():
                    if key not in phase2._FLAGS:
                        walk(child)
            elif rule.action not in (
                phase2._VERBATIM,
                phase2._COLLAPSE_WORD,
                phase2._CARRIERS,
            ):
                raise AssertionError(f"{ref}: unresolved note-content template {name}")

        walk(cell)

    def finish(self):
        if self.seen != set(self.rows):
            raise AssertionError(
                f"Unused changed-note reviews: {sorted(set(self.rows) - self.seen)}"
            )
