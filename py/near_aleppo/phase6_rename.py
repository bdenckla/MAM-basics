"""Give changed notes explicit near-Aleppo names before baking their content.

The walk enters note targets and ketiv/qere fields, excluding apparatus. MAM
target copies retain their source names. The final note-content phase then assigns
reviewed clauses to the near-Aleppo and MAM roles of the renamed templates.

Source replay alone uses historical names, keeping nested targets byte-identical
to the sealed review evidence. Distributed data uses only RENAMED_NOTES.
"""

from collections import Counter

from near_aleppo import phase2_templates as phase2
from near_aleppo import phase6_mam_targets as phase6
from near_aleppo.phase6_mam_targets import MAM_TARGET_PARAMETER

# MAM's note templates, each with the name, specific to the near-aleppo dataset,
# that it takes where it has MAM_TARGET_PARAMETER.
RENAMED_NOTES = {
    "נוסח": "נוסח עם הקשר מקרא על פי המסורה",
    "מ:הערה-2": "הערה-2 עם הקשר מקרא על פי המסורה",
}
LEGACY_NOTES = {
    "נוסח": "נוסח למקרא על פי המסורה",
    "מ:הערה-2": "הערה-2 למקרא על פי המסורה",
}

# A note template's target, its selected parameter in phase 2's rule table.
_TARGET = "1"
_FLAGS = frozenset((phase2.APPLIED_AND_FLAGGED, phase2.FLAGGED_NOT_APPLIED))
# What phase 2 keeps whole: none of these holds a note.
_HOLDING_NO_NOTE = frozenset(
    (phase2._VERBATIM, phase2._COLLAPSE_WORD, phase2._CARRIERS)
)


class Renames:
    """Renames the notes that carry MAM's target, verse by verse, and tallies them."""

    def __init__(self, *, source_replay=False):
        self.counts = Counter()
        self.names = LEGACY_NOTES if source_replay else RENAMED_NOTES

    def rename_e_cell(self, cell, verse):
        """Rename, in place, each note of ``cell`` that has MAM_TARGET_PARAMETER.

        ``cell`` is a verse's E cell as the flags step leaves it, and ``verse`` names
        the verse as main_build.py does.
        """
        self._walk(cell, verse)

    def assert_expected_counts(self, phase6_counts):
        """Require one rename for each note that phase 6 gave MAM's target."""
        drift = []
        for name in RENAMED_NOTES:
            label = name + phase6._ADDED
            if self.counts[name] != phase6_counts[label]:
                drift.append(
                    f"{name}: renamed {self.counts[name]}, but {label!r} is "
                    f"{phase6_counts[label]}"
                )
        if drift:
            raise AssertionError("Phase 6's renames drifted: " + "; ".join(drift))

    def _walk(self, value, verse):
        if isinstance(value, str):
            return
        if isinstance(value, list):
            for item in value:
                self._walk(item, verse)
            return
        name = value["tmpl_name"]
        rule = phase2._RULES.get(name)
        if rule is None:
            raise AssertionError(
                f"{verse}: the rename met {name!r}, which phase 2 has no rule for"
            )
        params = value.get("tmpl_params", {})
        if rule.action == phase2._KEEP_NOTE:
            self._walk(params[_TARGET], verse)
            if MAM_TARGET_PARAMETER in params:
                value["tmpl_name"] = self.names[name]
                self.counts[name] += 1
            return
        if MAM_TARGET_PARAMETER in params:
            raise AssertionError(
                f"{verse}: {name!r} has {MAM_TARGET_PARAMETER!r}, which only a note "
                "may have"
            )
        if rule.action == phase2._KEEP_KQ:
            for key, item in params.items():
                if key not in _FLAGS:
                    self._walk(item, verse)
        elif rule.action not in _HOLDING_NO_NOTE:
            raise AssertionError(
                f"{verse}: {name!r}, which phase 2 does not keep, in the dataset's text"
            )
