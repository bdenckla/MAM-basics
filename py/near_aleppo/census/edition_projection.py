"""Template-child choices for an edition-style census of MAM's EP column.

This projection is for surveys of one continuous Scripture stream.  It is not
for template inventories, apparatus surveys, or other specialized surveys of
the dataset, which may need to visit more than one parameter deliberately.

There is intentionally no all-parameters fallback.  Every template reachable
in the EP column must be classified here before an edition-style census can
cross it.  That makes a new documentation or alternative-bearing template a
loud failure instead of silently treating every parameter as Scripture.

A recognized template is held to its measured parameter key sets as well as to
its name, so that a template which gains a parameter is a loud failure too,
rather than having its new child treated as not-Scripture by omission.
"""

from mb_cmn import ws_tmpl2 as wtp

EDITION_SEPARATOR_TEMPLATE_NAMES = {
    "ר0",
    "ר1",
    "ר2",
    "ר3",
    "ר4",
    "ש",
    "ששש",
    "מ:ששש",
    "סס",
    "ססס",
    "פפ",
    "פפפ",
    "מ:מקף אפור",
    "מ:פסק",
    "מ:לגרמיה",
    "מ:לגרמיה-2",
    'מ:נו"ן הפוכה',
    "מ:נו״ן הפוכה",
}


# Each value names the one child, if any, that belongs to the projected
# Scripture stream. The selected branches are:
# qamats ד, dexi/tsinnor parameter 1, and the combined כפול presentation.  A
# pointed qere is the temporary pointing proxy for the ordinary ketiv/qere
# families; phase 4 will synthesize the edition's pointed ketiv from it.
_EDITION_KEYS = {
    "נוסח": ("1",),
    "מ:הערה": (),
    "מ:הערה-2": ("1",),
    "מ:קישור בהערה": (),
    "מ:קישור פנימי בהערה": (),
    "מ:דחי": ("1",),
    "מ:צינור": ("1",),
    "מ:קמץ": ("ד",),
    "מ:כפול": ("כפול",),
    "כו״ק": ("2",),
    "קו״כ": ("2",),
    "מ:כו״ק מיוחד": ("2",),
    "מ:קו״כ-אם": ("1",),
    "מ:קו״כ-אם-2": ("1",),
    "קרי ולא כתיב": ("2",),
    "כתיב ולא קרי": ("1",),
    "קרי רגיל": ("1",),
    "מ:אות-מיוחדת-במילה": ("2",),
    "מ:אות-ג": ("1",),
    "מ:אות-ק": ("1",),
    "מ:אות תלויה": ("1",),
    "מודגש": ("1",),
    "ר0": (),
    "ר1": (),
    "ר2": (),
    "ר3": (),
    "ר4": (),
    "ש": (),
    "ששש": (),
    "מ:ששש": (),
    "סס": (),
    "ססס": (),
    "פפ": (),
    "פפפ": (),
    "מ:מקף אפור": (),
    "מ:פסק": (),
    "מ:לגרמיה": (),
    "מ:לגרמיה-2": (),
    'מ:נו"ן הפוכה': (),
    "מ:נו״ן הפוכה": (),
}


def _keysets(*keysets):
    return frozenset(frozenset(keys) for keys in keysets)


# The parameter key sets each template above actually occurs with in the EP column,
# measured over MAM's 23,202 verses by a scratch script rather than enumerated by
# hand.  The walk descended through every parameter of every template, so no census
# can meet a key set this table lacks.  The check in
# ``edition_parameter_keys_for`` is the one ``near_aleppo.phase2_templates``
# applies to the E column: a recognized template whose key set is not among its own
# raises, so a template that gains a parameter fails loudly instead of having its
# new child treated as not-Scripture by omission.
#
# ``_keysets(())`` is a template whose key set is empty, and ``_keysets()`` is one
# that does not occur in the EP column at all, so that no key set of it has been
# measured.  The second raises on sight, which is the request to measure it before
# an edition-style census crosses it.
_EDITION_KEYSETS = {
    "נוסח": _keysets(("1", "2")),
    "מ:הערה": _keysets(),  # never met in the EP column
    "מ:הערה-2": _keysets(("1", "2", "3")),
    "מ:קישור בהערה": _keysets(("1", "2")),
    "מ:קישור פנימי בהערה": _keysets(("1", "2")),
    "מ:דחי": _keysets(("1", "2")),
    "מ:צינור": _keysets(("1", "2")),
    "מ:קמץ": _keysets(("ד", "ס")),
    "מ:כפול": _keysets(("א", "ב", "כפול")),
    "כו״ק": _keysets(("1", "2")),
    "קו״כ": _keysets(("1", "2")),
    "מ:כו״ק מיוחד": _keysets(("1", "2", "סוג")),
    "מ:קו״כ-אם": _keysets(),  # never met in the EP column
    "מ:קו״כ-אם-2": _keysets(
        ("1", "2", "3"),
        ("1", "2", "3", "מקורות"),
        ("1", "2", "3", "מקורות", "סוג"),
        ("1", "2", "3", "סוג"),
    ),
    "קרי ולא כתיב": _keysets(("1", "2")),
    "כתיב ולא קרי": _keysets(("1", "2"), ("1", "2", "3")),
    "קרי רגיל": _keysets(),  # never met in the EP column
    "מ:אות-מיוחדת-במילה": _keysets(("1", "2", "3", "4", "5")),
    "מ:אות-ג": _keysets(("1",)),
    "מ:אות-ק": _keysets(("1",)),
    "מ:אות תלויה": _keysets(("1",)),
    "מודגש": _keysets(("1",)),
    "ר0": _keysets(()),
    "ר1": _keysets(()),
    "ר2": _keysets(()),
    "ר3": _keysets(()),
    "ר4": _keysets(),  # never met in the EP column
    "ש": _keysets(()),
    "ששש": _keysets(),  # never met in the EP column
    "מ:ששש": _keysets(()),
    "סס": _keysets((), ("1",)),
    "ססס": _keysets((), ("1",)),
    "פפ": _keysets((), ("1",)),
    "פפפ": _keysets(("1",)),
    "מ:מקף אפור": _keysets(()),
    "מ:פסק": _keysets(()),
    "מ:לגרמיה": _keysets(),  # never met in the EP column
    "מ:לגרמיה-2": _keysets(()),
    'מ:נו"ן הפוכה': _keysets(),  # never met in the EP column
    "מ:נו״ן הפוכה": _keysets(("1",)),
}


def edition_parameter_keys(tmpl, *, overrides=None):
    """Return the selected parameter keys for one edition-style survey.

    ``overrides`` is reserved for a survey whose subject is one alternative
    family, such as comparing the two qamats parameters.  Every other template
    still goes through the common, fail-fast projection.
    """
    return edition_parameter_keys_for(
        wtp.template_name(tmpl),
        wtp.template_param_keys(tmpl),
        overrides=overrides,
    )


def edition_parameter_keys_for(name, available, *, overrides=None):
    """Apply the edition projection when a caller already has name and keys."""
    choices = _EDITION_KEYS if overrides is None else _EDITION_KEYS | overrides
    keys = choices.get(name)
    if keys is None:
        raise AssertionError(f"No edition-projection rule for template {name!r}")
    available = set(available)
    keysets = _EDITION_KEYSETS.get(name)
    if keysets is None:
        raise AssertionError(
            f"No measured parameter key sets for template {name!r}: record them in "
            "_EDITION_KEYSETS beside its edition-projection rule"
        )
    if not keysets:
        raise AssertionError(
            f"Template {name!r} does not occur in the EP column as measured, so its "
            "parameter key sets are unknown. Measure them into _EDITION_KEYSETS "
            "before an edition-style census crosses it."
        )
    if frozenset(available) not in keysets:
        raise AssertionError(
            f"Template {name!r} has parameters {sorted(available)}, which is not one "
            f"of its measured key sets {sorted(sorted(one) for one in keysets)}"
        )
    missing = [key for key in keys if key not in available]
    if missing:
        raise AssertionError(
            f"Template {name!r} lacks edition parameter(s) {missing!r}"
        )
    return keys
