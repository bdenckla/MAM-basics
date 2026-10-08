"""Phase 2 of near-aleppo: resolve MAM-parsed-plus's templates in the E column.

The public build guide is ``doc/near-aleppo-build.md``. Dispatch is closed: every template name the walk can reach has an explicit entry below, and a
name without one, or a recognized name with an unexpected parameter set, raises.

Every alternative-bearing template has one parameter the edition projection
selects (``py/near_aleppo/census/edition_projection.py``), called the selected
parameter below: ``ד`` of
``מ:קמץ``, ``1`` of ``מ:דחי`` and ``מ:צינור``, ``כפול`` of ``מ:כפול``, ``1`` of
``נוסח`` and ``מ:הערה-2``, the pointed qere of the ordinary ketiv/qere families,
and the pointed ketiv, parameter ``1``, of ``מ:קו״כ-אם-2``. Where phase 5 adds the
pointed ketiv MAM's notes give to one of the ordinary families, in
POINTED_KETIV_PARAMETER, that parameter is the family's selected parameter instead.
The projection reads MAM's text, which never has it, so the dataset's selection
differs from the projection's there. Every walk after phase 2 asks selected_keys
which parameters are selected rather than reading the rule table.

What happens to the other, unselected parameters depends on the template:

- a template phase 2 dissolves loses them with it;
- a note template keeps them verbatim, its note body above all (rule 2);
- a ketiv/qere template has its templates resolved in EVERY parameter, selected
  or not, so that ``מ:קמץ`` is absent from the dataset's own text.
  ``TEMPLATES_ABSENT_FROM_DATASET`` declares that invariant: ``assert_templates_absent``
  checks it over each whole book, every copy of MAM's target that phase 6 adds to
  a changed note excepted (``phase6_mam_targets.py``), those copies being MAM's
  text.

Phase 4, which would synthesize the pointed ketiv, is deferred,
so the ketiv/qere templates are kept, with their consonantal ketiv as MAM has it
apart from the templates resolved inside it. Phase 3's ketiv/qere apparatus
(``phase3_policies.py``) then removes 20 of them, 16 where MAM's note says the codex
has no qere note and 4 where it gives the codex's masorah note, which is not a qere
note, and phase 2 still meets and counts every one. Where MAM's notes
give the codex's pointed ketiv, ``phase5_readings.py`` adds it to the template in
POINTED_KETIV_PARAMETER, MAM's parameters staying as they are.

Rule 8's templates for marks written where no letter is, MARKS_WITHOUT_LETTER and
MARKS_WITHOUT_LETTER_OR_SPACE, are specific to the near-Aleppo dataset. MAM's text
never has them, so phase 2 raises if it meets them; later steps write them inside
pointed ketivs, and the subsequent walks keep them whole.

Legarmeh, paseq and gray maqaf are first written as private-use placeholders, so
that the spacing each replacement assumes can be checked on the verse's flattened
text, across template boundaries, before the real characters go in. The verse is
flattened twice: once along the selected parameters, and once taking the other
side of each ketiv/qere template, so that a placeholder in an unselected qere is
checked in its own context too.
"""

from collections import Counter
from typing import NamedTuple

from py_misc import orphan_marks

PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"

_LEGARMEH_MARK = ""
_PASEQ_MARK = ""
_GRAY_MAQAF_MARK = ""
_MARK_NAMES = {
    _LEGARMEH_MARK: "מ:לגרמיה-2",
    _PASEQ_MARK: "מ:פסק",
    _GRAY_MAQAF_MARK: "מ:מקף אפור",
}
_FINAL_TEXT = {_LEGARMEH_MARK: PASEQ, _PASEQ_MARK: PASEQ + " ", _GRAY_MAQAF_MARK: " "}

# What phase 2 does with a template, one action per entry of _RULES.
_DISSOLVE = "dissolve"  # replaced by its selected parameter, resolved
_KEEP_NOTE = "keep-note"  # kept; selected parameter resolved, unselected verbatim
_KEEP_KQ = "keep-kq"  # kept; templates resolved in every parameter
_VERBATIM = "verbatim"  # kept whole: a layout or separator template
_MARK = "mark"  # replaced by a placeholder, then by its final text
_COLLAPSE_WORD = "collapse-word"  # a special-letter word, flattened or kept whole
_CARRIERS = "carriers"  # the near-Aleppo dataset's rule-8 marks on carrier alefs

_SPECIAL_LETTER_WORD = "מ:אות-מיוחדת-במילה"
_SUSPENDED_KIND = "ת"
_LARGE_KIND = "ג"
_SMALL_KIND = "ק"
# Every value of the special-letter-word template's parameter 4 this walk meets,
# measured from MAM-parsed-plus by a scratch script rather than enumerated by hand:
# the three single-letter kinds above, and the two orders in which one atom carries
# both a large and a small letter. Dispatch is closed as everywhere else in phase 2,
# so a kind outside this set raises instead of falling through to the flatten
# branch, where an unrecognized kind would silently lose its letter's marking.
_SPECIAL_LETTER_KINDS = frozenset(
    (
        _LARGE_KIND,
        _SMALL_KIND,
        _SUSPENDED_KIND,
        _LARGE_KIND + _SMALL_KIND,
        _SMALL_KIND + _LARGE_KIND,
    )
)
# MAM says in all four places it treats Deuteronomy 32:6 that the codex has the
# large he, so this is the one large or small letter kept.
_KEPT_LARGE_LETTER_VERSE = ("A5-Deuter", "32", "6")

_UNSELECTED = " (unselected parameter)"

# The pointed ketiv that MAM's notes give, which phase5_readings.py adds after MAM's
# parameters to a template of POINTED_KETIV_FAMILIES, and which is then that template's
# selected parameter. The added parameter is named explicitly in Hebrew below.
POINTED_KETIV_PARAMETER = "כתיב מנוקד"
# The ordinary ketiv/qere families, whose parameter 1 is the consonantal ketiv and
# whose parameter 2, the pointed qere, is selected where they lack the pointed ketiv.
POINTED_KETIV_FAMILIES = ("כו״ק", "קו״כ", "מ:כו״ק מיוחד")
# The two evidence flags, which phase6_flags.py adds as the last parameter of a note or
# of a ketiv/qere template. They are named here, beside the rule table, so that
# selected_keys can tell a flag from a parameter nothing adds; phase6_flags.py takes
# the names from here.
APPLIED_AND_FLAGGED = "applied-and-flagged"
FLAGGED_NOT_APPLIED = "flagged-not-applied"
_FLAGS = frozenset({APPLIED_AND_FLAGGED, FLAGGED_NOT_APPLIED})

# The marks-without-letter template represents marks that MAM's notes attribute to
# a nonzero-width space in the codex. Its original schema has one parameter: alefs,
# each followed by the marks at that position, with alef as an arbitrary carrier.
# An alef carrier cannot carry dagesh. The GV extension has an explicit carrier
# discriminator and exactly artificial VAV + HOLAM; the original alef schema remains.
# The edition renders the marks in double guillemets; the dataset and the in-place
# test read them in square brackets, as MAM's notes write them.
MARKS_WITHOUT_LETTER = "ניקוד בלי אות"
MARKS_WITHOUT_LETTER_OR_SPACE = orphan_marks.MARKS_WITHOUT_LETTER_OR_SPACE


class _Rule(NamedTuple):
    action: str
    # The selected parameter keys, or for _MARK the placeholder.
    keys: tuple | str
    keysets: frozenset
    # For _KEEP_KQ, the other side of the ketiv/qere, flattened for the second
    # spacing check; () where the template has no other side to flatten.
    other_side: tuple = ()


def _keysets(*keysets):
    return frozenset(frozenset(keys) for keys in keysets)


_RULES = {
    "מ:קמץ": _Rule(_DISSOLVE, ("ד",), _keysets(("ד", "ס"))),
    "מ:דחי": _Rule(_DISSOLVE, ("1",), _keysets(("1", "2"))),
    "מ:צינור": _Rule(_DISSOLVE, ("1",), _keysets(("1", "2"))),
    "מ:כפול": _Rule(_DISSOLVE, ("כפול",), _keysets(("א", "ב", "כפול"))),
    "נוסח": _Rule(_KEEP_NOTE, ("1",), _keysets(("1", "2"))),
    "מ:הערה-2": _Rule(_KEEP_NOTE, ("1",), _keysets(("1", "2", "3"))),
    "כו״ק": _Rule(_KEEP_KQ, ("2",), _keysets(("1", "2")), ("1",)),
    "קו״כ": _Rule(_KEEP_KQ, ("2",), _keysets(("1", "2")), ("1",)),
    "מ:כו״ק מיוחד": _Rule(_KEEP_KQ, ("2",), _keysets(("1", "2", "סוג")), ("1",)),
    "מ:קו״כ-אם-2": _Rule(
        _KEEP_KQ,
        ("1",),
        _keysets(
            ("1", "2", "3", "מקורות", "סוג"),
            ("1", "2", "3", "מקורות"),
            ("1", "2", "3", "סוג"),
            ("1", "2", "3"),
        ),
        ("3",),
    ),
    "קרי ולא כתיב": _Rule(_KEEP_KQ, ("2",), _keysets(("1", "2"))),
    "כתיב ולא קרי": _Rule(_KEEP_KQ, ("1",), _keysets(("1", "2"), ("1", "2", "3"))),
    "מ:לגרמיה-2": _Rule(_MARK, _LEGARMEH_MARK, _keysets(())),
    "מ:פסק": _Rule(_MARK, _PASEQ_MARK, _keysets(())),
    "מ:מקף אפור": _Rule(_MARK, _GRAY_MAQAF_MARK, _keysets(())),
    _SPECIAL_LETTER_WORD: _Rule(
        _COLLAPSE_WORD, ("2",), _keysets(("1", "2", "3", "4", "5"))
    ),
    "ר0": _Rule(_VERBATIM, (), _keysets(())),
    "ר1": _Rule(_VERBATIM, (), _keysets(())),
    "ר2": _Rule(_VERBATIM, (), _keysets(())),
    "ר3": _Rule(_VERBATIM, (), _keysets(())),
    "ר4": _Rule(_VERBATIM, (), _keysets(())),
    "ש": _Rule(_VERBATIM, (), _keysets(())),
    "מ:ששש": _Rule(_VERBATIM, (), _keysets(())),
    "סס": _Rule(_VERBATIM, (), _keysets((), ("1",))),
    "ססס": _Rule(_VERBATIM, (), _keysets((), ("1",))),
    "פפ": _Rule(_VERBATIM, (), _keysets((), ("1",))),
    "פפפ": _Rule(_VERBATIM, (), _keysets(("1",))),
    "מ:נו״ן הפוכה": _Rule(_VERBATIM, (), _keysets(("1",))),
    "מ:קישור בהערה": _Rule(_VERBATIM, (), _keysets(("1", "2"))),
    MARKS_WITHOUT_LETTER: _Rule(
        _CARRIERS, (), _keysets(("1",), ("1", orphan_marks.GV_PARAMETER))
    ),
    MARKS_WITHOUT_LETTER_OR_SPACE: _Rule(_CARRIERS, (), _keysets(("1",))),
}

# Templates that phase 2 removes wherever they occur, so that none remains
# anywhere in the dataset's own text: not in any column, parameter or note body.
# The copies of MAM's target that phase 6 adds to changed notes are MAM's text, and
# hold them.
TEMPLATES_ABSENT_FROM_DATASET = ("מ:קמץ", "מ:דחי", "מ:צינור", "מ:כפול", "מ:מקף אפור")


class Resolver:
    """Resolves E cells verse by verse and tallies what it did."""

    def __init__(self):
        self.counts = Counter()

    def resolve_e_cell(self, cell, verse):
        """Return the resolved E cell of one verse, ``verse`` naming it as main_build.py does."""
        _assert_no_marks(cell, verse)
        resolved = self._sequence(_as_list(cell), verse, True)
        _assert_marks_flattenable(resolved, verse)
        _check_mark_spacing(_flatten(resolved, other_side=False), verse)
        _check_mark_spacing(_flatten(resolved, other_side=True), verse)
        return _replace_marks(resolved)

    def _count(self, label, selected):
        self.counts[label if selected else label + _UNSELECTED] += 1

    def _sequence(self, elements, verse, selected):
        out = []
        for element in elements:
            if isinstance(element, str):
                out.append(element)
            else:
                out.extend(self._template(element, verse, selected))
        return _merge_strings(out)

    def _template(self, tmpl, verse, selected):
        name = tmpl["tmpl_name"]
        params = tmpl.get("tmpl_params", {})
        rule = _RULES.get(name)
        if rule is None:
            raise AssertionError(f"{verse}: no phase 2 rule for template {name!r}")
        if rule.action == _CARRIERS:
            raise AssertionError(
                f"{verse}: {name!r}, a template specific to the near-Aleppo dataset, "
                "in MAM's text"
            )
        if frozenset(params) not in rule.keysets:
            raise AssertionError(
                f"{verse}: template {name!r} has unexpected parameters {sorted(params)}"
            )
        self._count(name, selected)
        if rule.action == _DISSOLVE:
            return self._sequence(_as_list(params[rule.keys[0]]), verse, selected)
        if rule.action in (_KEEP_NOTE, _KEEP_KQ):
            return [self._kept(tmpl, rule, verse, selected)]
        if rule.action == _MARK:
            return [rule.keys]
        if rule.action == _VERBATIM:
            return [tmpl]
        if rule.action == _COLLAPSE_WORD:
            return self._special_letter_word(tmpl, verse, selected)
        raise AssertionError(f"{verse}: no phase 2 action {rule.action!r}")

    def _kept(self, tmpl, rule, verse, selected):
        new_params = {}
        for key, value in tmpl["tmpl_params"].items():
            key_selected = key in rule.keys
            if key_selected or rule.action == _KEEP_KQ:
                resolved = self._sequence(
                    _as_list(value), verse, selected and key_selected
                )
                new_params[key] = _simplify(resolved)
            else:
                new_params[key] = value
        return {"tmpl_name": tmpl["tmpl_name"], "tmpl_params": new_params}

    def _special_letter_word(self, tmpl, verse, selected):
        params = tmpl["tmpl_params"]
        kind = params["4"]
        flattened = params["2"]
        if not isinstance(kind, str) or not isinstance(flattened, str):
            raise AssertionError(
                f"{verse}: {_SPECIAL_LETTER_WORD} parameters 2 and 4 must be plain text"
            )
        if kind not in _SPECIAL_LETTER_KINDS:
            raise AssertionError(
                f"{verse}: {_SPECIAL_LETTER_WORD} parameter 4 is {kind!r}, which is "
                f"not one of the measured kinds {sorted(_SPECIAL_LETTER_KINDS)}"
            )
        if kind == _SUSPENDED_KIND:
            self._count("special letter word kept, suspended", selected)
            return [tmpl]
        if verse == _KEPT_LARGE_LETTER_VERSE:
            if kind != _LARGE_KIND:
                raise AssertionError(
                    f"{verse}: expected the large he, found kind {kind!r}"
                )
            self._count("special letter word kept, large", selected)
            return [tmpl]
        self._count("special letter word flattened", selected)
        return [flattened]


def assert_templates_absent(value, label, skipped_note_parameter):
    """Raise if any of TEMPLATES_ABSENT_FROM_DATASET occurs in ``value``'s own text.

    ``skipped_note_parameter`` names the parameter of a note template that holds a
    copy of MAM's target, which is MAM's text, and that parameter is not searched.
    Everything else is, note bodies included.
    """
    if isinstance(value, list):
        for item in value:
            assert_templates_absent(item, label, skipped_note_parameter)
    elif isinstance(value, dict):
        name = value.get("tmpl_name")
        if name in TEMPLATES_ABSENT_FROM_DATASET:
            raise AssertionError(f"{label}: {name!r} survived phase 2")
        rule = _RULES.get(name)
        is_note = rule is not None and rule.action == _KEEP_NOTE
        for key, item in value.items():
            if key == "tmpl_params" and is_note:
                item = {
                    pkey: pitem
                    for pkey, pitem in item.items()
                    if pkey != skipped_note_parameter
                }
            assert_templates_absent(item, label, skipped_note_parameter)


def selected_keys(tmpl, verse):
    """The keys of the selected parameters of ``tmpl``, a note or ketiv/qere template
    this phase keeps; ``verse`` names the verse, as main_build.py does.

    For the families of POINTED_KETIV_FAMILIES it is POINTED_KETIV_PARAMETER where the
    template has it, and parameter 2, the pointed qere, where it does not; for every
    other template it is the rule table's. A ketiv/qere template raises unless its
    parameters are one of MAM's measured sets for its family, or such a set with the
    parameters later phases add to it: POINTED_KETIV_PARAMETER, in the ordinary
    families alone, and one of the two flags. A note template's selected parameter is
    its target whatever phase 6 adds to the note, MAM's target and a flag, which the
    steps that add them check. Any other template raises, having no selected
    parameter that a walk reads.
    """
    name = tmpl["tmpl_name"]
    rule = _RULES.get(name)
    if rule is None or rule.action not in (_KEEP_NOTE, _KEEP_KQ):
        raise AssertionError(
            f"{verse}: {name!r} is not a template phase 2 keeps with a selected "
            "parameter"
        )
    if rule.action == _KEEP_NOTE:
        return rule.keys
    keys = frozenset(tmpl["tmpl_params"])
    flags = keys & _FLAGS
    pointed = keys & {POINTED_KETIV_PARAMETER}
    if (
        len(flags) > 1
        or (pointed and name not in POINTED_KETIV_FAMILIES)
        or keys - flags - pointed not in rule.keysets
    ):
        raise AssertionError(
            f"{verse}: template {name!r} has unexpected parameters {sorted(keys)}"
        )
    return (POINTED_KETIV_PARAMETER,) if pointed else rule.keys


def carriers_text(tmpl, verse):
    """Validated GA or explicit GV carriers in the build's bracket notation."""
    return "[" + orphan_marks.carriers(tmpl, verse) + "]"


def marks_without_letter(carriers, verse, *, without_space=False):
    """The near-Aleppo dataset's rule-8 template holding ``carriers``, which carriers_text checks."""
    name = MARKS_WITHOUT_LETTER_OR_SPACE if without_space else MARKS_WITHOUT_LETTER
    tmpl = {"tmpl_name": name, "tmpl_params": {"1": carriers}}
    carriers_text(tmpl, verse)
    return tmpl


def _as_list(value):
    return value if isinstance(value, list) else [value]


def _simplify(elements):
    """Store a parameter the way MAM-parsed-plus does: one element bare, else a list."""
    if not elements:
        return ""
    return elements[0] if len(elements) == 1 else elements


def _merge_strings(elements):
    out = []
    for element in elements:
        if isinstance(element, str) and out and isinstance(out[-1], str):
            out[-1] += element
        else:
            out.append(element)
    return out


def _flatten(elements, other_side):
    """The verse's text, separators as spaces.

    Along the selected parameters, or with ``other_side`` taking the other side of
    each ketiv/qere template that has one.
    """
    parts = []
    for element in elements:
        if isinstance(element, str):
            parts.append(element)
            continue
        rule = _RULES[element["tmpl_name"]]
        if rule.action in (_KEEP_NOTE, _KEEP_KQ):
            keys = rule.other_side if other_side and rule.other_side else rule.keys
            for key in keys:
                parts.append(
                    _flatten(_as_list(element["tmpl_params"][key]), other_side)
                )
        elif rule.action == _COLLAPSE_WORD:
            parts.append(element["tmpl_params"]["2"])
        elif rule.action == _VERBATIM:
            parts.append(" ")
        else:
            raise AssertionError(
                f"template {element['tmpl_name']!r} survived phase 2 resolution"
            )
    return "".join(parts)


def _assert_marks_flattenable(value, verse):
    """Raise if a placeholder sits where neither flattening reaches it.

    The rule table is consulted only along parameters a flattening reads; a
    parameter kept verbatim, such as a note body, can hold templates phase 2 has
    no rule for, and is only scanned for placeholders.
    """
    if isinstance(value, list):
        for item in value:
            _assert_marks_flattenable(item, verse)
    elif isinstance(value, dict):
        rule = _RULES[value["tmpl_name"]]
        reached = set(rule.other_side)
        if rule.action != _MARK:
            reached |= set(rule.keys)
        for key, item in value.get("tmpl_params", {}).items():
            if key in reached:
                _assert_marks_flattenable(item, verse)
            elif _contains_mark(item):
                raise AssertionError(
                    f"{verse}: a placeholder in {value['tmpl_name']!r} parameter "
                    f"{key!r}, which no spacing check reads"
                )


def _contains_mark(value):
    if isinstance(value, str):
        return any(mark in value for mark in _MARK_NAMES)
    if isinstance(value, list):
        return any(_contains_mark(item) for item in value)
    return any(_contains_mark(item) for item in value.get("tmpl_params", {}).values())


def _check_mark_spacing(text, verse):
    for index, char in enumerate(text):
        if char not in _MARK_NAMES:
            continue
        before = text[index - 1] if index > 0 else ""
        after = text[index + 1] if index + 1 < len(text) else ""
        if not before or before.isspace():
            raise AssertionError(
                f"{verse}: space or verse start before {_MARK_NAMES[char]}"
            )
        if char == _LEGARMEH_MARK:
            ok = after == " "
        else:
            ok = bool(after) and not after.isspace()
        if not ok:
            raise AssertionError(
                f"{verse}: unexpected text {after!r} after {_MARK_NAMES[char]}"
            )


def _replace_marks(value):
    if isinstance(value, str):
        for mark, final in _FINAL_TEXT.items():
            value = value.replace(mark, final)
        return value
    if isinstance(value, list):
        return [_replace_marks(item) for item in value]
    if "tmpl_params" in value:
        return {
            "tmpl_name": value["tmpl_name"],
            "tmpl_params": {
                key: _replace_marks(item) for key, item in value["tmpl_params"].items()
            },
        }
    return value


def _assert_no_marks(value, verse):
    if isinstance(value, str):
        if any(mark in value for mark in _MARK_NAMES):
            raise AssertionError(f"{verse}: input already holds a phase 2 placeholder")
    elif isinstance(value, list):
        for item in value:
            _assert_no_marks(item, verse)
    else:
        for item in value.get("tmpl_params", {}).values():
            _assert_no_marks(item, verse)
