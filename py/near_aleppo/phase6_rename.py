"""Phase 6 of near-aleppo: a note carrying MAM's target takes a name of the dataset's own.

MAM template names retain their MAM meaning. The public build guide is
``doc/near-aleppo-build.md``. Where a note has MAM_TARGET_PARAMETER, which ``phase6_mam_targets.py`` adds
to each note whose target the build changes, the note's clauses are about that
parameter, MAM's own target, and not about parameter 1, the dataset's text, so a
consumer knowing only MAM's templates would misread such a note without an error.
RENAMED_NOTES gives both notes distinct names so consumers can recognize that
the note body describes the preserved MAM target.

Both names are specific to the near-aleppo dataset, as rule 8's two templates are:
MAM's text never has them, and like rule 8's they have no מ: prefix.

This step is the last of phase 6, after the flags and before serialization. It
renames each נוסח and מ:הערה-2 in the dataset's own text that has
MAM_TARGET_PARAMETER, keeping every parameter as it stands, so every step before it
sees MAM's names, and so does ``phase2_templates.assert_templates_absent``, which
``main_build.py`` runs before this step. The walk is phase 6's, by phase 2's rule
table: it enters a note's target and every parameter of a ketiv/qere template but a
flag, and no other parameter. So it never enters a MAM_TARGET_PARAMETER value, whose
templates are MAM's text and keep MAM's names, nor a note body or a
flag value, which quote MAM's notes. A template other than a note that has
MAM_TARGET_PARAMETER raises, and the renames are asserted equal to phase 6's counts
of the notes given MAM's target.
"""

from collections import Counter

from near_aleppo import phase2_templates as phase2
from near_aleppo import phase6_mam_targets as phase6
from near_aleppo.phase6_mam_targets import MAM_TARGET_PARAMETER

# MAM's note templates, each with the name, specific to the near-aleppo dataset,
# that it takes where it has MAM_TARGET_PARAMETER.
RENAMED_NOTES = {
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

    def __init__(self):
        self.counts = Counter()

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
                value["tmpl_name"] = RENAMED_NOTES[name]
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
