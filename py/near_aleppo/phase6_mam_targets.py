"""Phase 6 of near-aleppo: MAM's own target, in an added parameter of each changed note.

The public build guide is ``doc/near-aleppo-build.md``. Note bodies remain
verbatim: a clause opening with "=" has MAM's text as its implicit subject. A
changed target could otherwise make that clause appear to assert agreement with
the dataset's text. Every changed נוסח or מ:הערה-2 therefore gains an added
parameter holding MAM's original target. MAM_TARGET_PARAMETER names that parameter
in Hebrew, using MAM's own name to identify whose text it holds.

A note's target has changed wherever the dataset's parameter 1 differs from
MAM-parsed-plus's parameter 1 of the same note, the two compared as JSON values, with
no judgment about whether the change touches the note's point. Such a note gains
MAM_TARGET_PARAMETER, after its other parameters, holding MAM-parsed-plus's parameter
1 verbatim, templates included. A note whose parameter 1 is MAM's gains nothing. At
Exodus 34:7, Leviticus 6:2, Numbers 10:10 and Deuteronomy 32:6 a changed מ:הערה-2
sits in the target of a changed נוסח: the מ:הערה-2 gains its own parameter, and the
נוסח's parameter holds MAM's target with MAM's מ:הערה-2 inside it, without an added
parameter, that being MAM's text.

The copies hold templates that phase 2 removes from the dataset's own text, so
main_build.py passes MAM_TARGET_PARAMETER to phase 2's assert_templates_absent as the
parameter to skip. The name is defined here rather than in phase2_templates.py
because this module imports phase2_templates.py for its rule table, and
phase2_templates.py must not import this module.

The step compares the build's output with its input, so it covers every change a
later phase makes to a target, provided it stays the last step that changes cell
text. ``phase6_flags.py`` runs after it, adding parameters only and none inside a
note's target, and ``phase6_rename.py`` last, giving each note that has the
parameter a name specific to the near-aleppo dataset. MAM-parsed-plus cannot already have the parameter: phase 2 raises on
a note template whose parameters are other than those its rule table lists.
"""

import copy
from collections import Counter

from near_aleppo import phase2_templates as phase2

# The parameter a note gains where the build changes its target. It holds
# MAM-parsed-plus's parameter 1 of that note, MAM's own target. The name is MAM's own
# Hebrew name, so the parameter says whose text it holds.
MAM_TARGET_PARAMETER = "מקרא על פי המסורה"

# A note template's target, its selected parameter in phase 2's rule table.
_TARGET = "1"

_REACHED = ": notes reached"
_ADDED = ": notes given MAM's target"

# The notes reached are the notes phase 2 counts: both phases use the same walk,
# so the reached-note expectations follow phase 2.
#
# A MAM-only census cannot count notes given MAM's target, because those counts
# depend on the difference between the finished dataset and MAM's input text.
# This pass derives that difference directly for every paired note. Any phase
# that changes a target can increase the added-target count, but a note changed
# by several phases is counted once. Nested changed notes each receive their own
# copy; MAM's source structures inside those copies remain unchanged.
#
# The counts live in in/near-aleppo/build-populations.json. An input refresh may
# advance reached-note expectations with phase 2. The two added-target counts
# remain fixed, and both target copying and final renaming must reproduce them;
# a changed count fails for review.


class MamTargets:
    """Adds MAM's own target to the changed notes verse by verse and tallies them."""

    def __init__(self):
        self.counts = Counter()

    def add_to_e_cell(self, mam_cell, cell, verse):
        """Add MAM_TARGET_PARAMETER, in place, to each note of ``cell`` whose target changed.

        ``mam_cell`` is MAM-parsed-plus's E cell of the verse, copied before phase 2;
        ``cell`` is the E cell phase 5 returns; ``verse`` names the verse as
        main_build.py does. The notes of the two cells are paired in document order,
        and the build raises unless each pair has the same template name and the same
        parameters other than the target, note bodies included, which rule 2 keeps
        verbatim. Every pair is decided before any parameter is added, so that a
        parameter added to a מ:הערה-2 can never make the target of the נוסח holding
        it look changed. Each added parameter is a deep copy, so no object is shared
        between a copy of MAM's target and the dataset's text.
        """
        mam_notes = _notes(mam_cell, verse)
        notes = _notes(cell, verse)
        if len(mam_notes) != len(notes):
            raise AssertionError(
                f"{verse}: MAM's E cell has {len(mam_notes)} note templates and the "
                f"dataset's has {len(notes)}"
            )
        changed = []
        for number, (mam_note, note) in enumerate(zip(mam_notes, notes), 1):
            name = mam_note["tmpl_name"]
            mam_params, params = mam_note["tmpl_params"], note["tmpl_params"]
            if (
                note["tmpl_name"] != name
                or list(params) != list(mam_params)
                or any(
                    params[key] != value
                    for key, value in mam_params.items()
                    if key != _TARGET
                )
            ):
                raise AssertionError(
                    f"{verse}: note template {number} is {name!r} in MAM's E cell and "
                    f"{note['tmpl_name']!r} in the dataset's, or the two differ in a "
                    "parameter other than the target"
                )
            self.counts[name + _REACHED] += 1
            if params[_TARGET] != mam_params[_TARGET]:
                changed.append((name, mam_params[_TARGET], params))
        for name, mam_target, params in changed:
            params[MAM_TARGET_PARAMETER] = copy.deepcopy(mam_target)
            self.counts[name + _ADDED] += 1

    def assert_expected_counts(self, expected_counts):
        drift = [
            f"{label}: expected {expected}, build {self.counts[label]}"
            for label, expected in expected_counts.items()
            if self.counts[label] != expected
        ]
        if drift:
            raise AssertionError("Phase 6 populations drifted: " + "; ".join(drift))


def _notes(value, verse):
    """The note templates of ``value``, in document order, along phase 2's walk.

    The walk enters a template phase 2 dissolves in its selected parameter, a note
    template in its target, a ketiv/qere template in every parameter, and no other
    template. A note template comes before the notes in its target.
    """
    notes = []
    _walk(value, verse, notes)
    return notes


def _walk(value, verse, notes):
    if isinstance(value, str):
        return
    if isinstance(value, list):
        for item in value:
            _walk(item, verse, notes)
        return
    name = value["tmpl_name"]
    rule = phase2._RULES.get(name)
    if rule is None:
        raise AssertionError(
            f"{verse}: phase 6 met {name!r}, which phase 2 has no rule for"
        )
    params = value.get("tmpl_params", {})
    if rule.action == phase2._DISSOLVE:
        _walk(params[rule.keys[0]], verse, notes)
    elif rule.action == phase2._KEEP_NOTE:
        notes.append(value)
        _walk(params[_TARGET], verse, notes)
    elif rule.action == phase2._KEEP_KQ:
        for item in params.values():
            _walk(item, verse, notes)
