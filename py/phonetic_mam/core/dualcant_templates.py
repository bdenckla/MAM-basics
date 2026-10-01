"""Closed MAM-parsed-plus shapes accepted by untangler preparation.

Validation visits explicitly declared parameters, including documentation, but
never treats those parameters as Scripture. Current dual templates are direct EP
elements. A nested dual template requires a separately reviewed traversal policy.
"""

from mb_cmn import ws_tmpl2

# Exact parameter identities, in the input order used by the existing pipeline.
# These are the current EP shapes in the three books that contain dual templates.
_SHAPES = {
    "כו״ק": (("1", "2"),),
    "מ:אות-ג": (("1",),),
    "מ:אות-מיוחדת-במילה": (("1", "2", "3", "4", "5"),),
    "מ:אות-ק": (("1",),),
    "מ:הערה-2": (("1", "2", "3"),),
    "מ:כו״ק מיוחד": (("1", "2", "סוג"),),
    "מ:כפול": (("כפול", "א", "ב"),),
    "מ:לגרמיה-2": ((),),
    "מ:פסק": ((),),
    "מ:קו״כ-אם-2": (("1", "2", "3", "מקורות", "סוג"),),
    "מ:קישור בהערה": (("1", "2"),),
    "מ:קמץ": (("ד", "ס"),),
    "מ:ששש": ((),),
    "מודגש": (("1",),),
    "נוסח": (("1", "2"),),
    "סס": ((), ("1",)),
    "ססס": (("1",),),
    "פפ": ((), ("1",)),
    "קו״כ": (("1", "2"),),
    "ר3": ((),),
    "ש": ((),),
}


def sequence(value):
    """Restore a plus parameter's singleton representation without flattening."""
    if isinstance(value, (str, dict)):
        return [value]
    if not isinstance(value, (list, tuple)):
        raise ValueError("unexpected template parameter representation")
    return value


def validate_sequence(value, *, allow_dual=False):
    """Validate one EP sequence; only its immediate elements may be dual."""
    if not isinstance(value, (list, tuple)):
        raise ValueError("expected an EP sequence")
    for element in value:
        if isinstance(element, str):
            continue
        validate_template(element, allow_dual=allow_dual)


def validate_template(value, *, allow_dual=False):
    """Reject unknown fields, names, parameter identities, and nested duals."""
    if not isinstance(value, dict) or not ws_tmpl2.is_template(value):
        raise ValueError("unexpected EP element")
    name = ws_tmpl2.template_name(value)
    if name not in _SHAPES:
        raise ValueError("unclassified untangler template")
    params = value.get("tmpl_params", {})
    if not isinstance(params, dict) or tuple(params) not in _SHAPES[name]:
        raise ValueError("unexpected untangler template parameters")
    if name == "מ:כפול" and not allow_dual:
        raise ValueError("nested dual template has no preparation policy")
    for key in tuple(params):
        validate_sequence(sequence(params[key]))
    return name
