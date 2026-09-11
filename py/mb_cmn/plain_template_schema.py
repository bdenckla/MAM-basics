"""Closed shape roster for the current MAM-parsed-plain corpus.

The roster was audited against every plain book on 2026-09-11.  Whole-structure
walkers validate a template or custom tag here before visiting its children.  A
new name or arity therefore requires an explicit source change.
"""

from mb_cmn import ws_tmpl1

CURRENT_PLAIN_TEMPLATE_ARG_COUNTS = {
    "#בלי קטע:": frozenset({1}),
    "#בלי קטע:דברי הימים א טז/טעמים": frozenset({1}),
    "#בלי קטע:דברים לב/טעמים": frozenset({1}),
    "#בלי קטע:יהושע יב/טעמים": frozenset({1}),
    "#בלי קטע:מלכי כנען/צורת השיר": frozenset({1}),
    "#בלי קטע:עשרת בני המן/צורת השיר": frozenset({1}),
    "#בלי קטע:שופטים ה/טעמים": frozenset({1}),
    "#בלי קטע:שירת אסף/צורת השיר": frozenset({1}),
    "#בלי קטע:שירת דבורה/צורת השיר": frozenset({1}),
    "#בלי קטע:שירת דוד/צורת השיר": frozenset({1}),
    "#בלי קטע:שירת האזינו/צורת השיר": frozenset({1}),
    "#בלי קטע:שירת הים/צורת השיר": frozenset({1}),
    "#בלי קטע:שירת העתים/צורת השיר": frozenset({1}),
    "#בלי קטע:שמואל ב כב/טעמים": frozenset({1}),
    "#בלי קטע:שמות טו/טעמים": frozenset({1}),
    "#קטע:אסתר ט/טעמים": frozenset({1}),
    "#קטע:דברי הימים א טז/טעמים": frozenset({1}),
    "#קטע:דברים לב/טעמים": frozenset({1}),
    "#קטע:יהושע יב/טעמים": frozenset({1}),
    "#קטע:מלכי כנען/צורות נוספות": frozenset({1}),
    "#קטע:מלכי כנען/צורת השיר": frozenset({1}),
    "#קטע:עשרת בני המן/צורות נוספות": frozenset({1}),
    "#קטע:עשרת בני המן/צורת השיר": frozenset({1}),
    "#קטע:עשרת הדברות בסיס/טעמים": frozenset({1}),
    "#קטע:עשרת הדברות/טעמים": frozenset({1}),
    "#קטע:קהלת ג/טעמים": frozenset({1}),
    "#קטע:שירת אסף/צורות נוספות": frozenset({1}),
    "#קטע:שירת אסף/צורת השיר": frozenset({1}),
    "#קטע:שירת דבורה/צורות נוספות": frozenset({1}),
    "#קטע:שירת דבורה/צורת השיר": frozenset({1}),
    "#קטע:שירת דוד/צורות נוספות": frozenset({1}),
    "#קטע:שירת דוד/צורת השיר": frozenset({1}),
    "#קטע:שירת האזינו/צורות נוספות": frozenset({1}),
    "#קטע:שירת האזינו/צורת השיר": frozenset({1}),
    "#קטע:שירת הים/צורות נוספות": frozenset({1}),
    "#קטע:שירת הים/צורת השיר": frozenset({1}),
    "#קטע:שירת העתים/צורות נוספות": frozenset({1}),
    "#קטע:שירת העתים/צורת השיר": frozenset({1}),
    "#קטע:שמות טו/טעמים": frozenset({1}),
    "בסיס-משתמש": frozenset({1}),
    "גלגל-2": frozenset({1}),
    "טעמי המקרא באינטרנט": frozenset({0}),
    "ירח בן יומו-2": frozenset({1}),
    "כו״ק": frozenset({2}),
    "כתיב ולא קרי": frozenset({2, 3}),
    "מ:אות מנוקדת": frozenset({1}),
    "מ:אות תלויה": frozenset({1}),
    "מ:אות-ג": frozenset({1}),
    "מ:אות-ק": frozenset({1}),
    "מ:אין פרשה בתחילת פרק": frozenset({0}),
    "מ:אין פרשה בתחילת פרק בספרי אמ״ת": frozenset({0}),
    "מ:אין רווח של פרשה בתחילת פרשת השבוע": frozenset({0}),
    "מ:גרש ותלישא גדולה": frozenset({0}),
    "מ:גרשיים ותלישא גדולה": frozenset({0}),
    "מ:דחי": frozenset({2}),
    "מ:הערה": frozenset({2}),
    "מ:טעם": frozenset({1}),
    "מ:טעם ומתג באות אחת": frozenset({0}),
    "מ:טעמי המקרא": frozenset({0, 1}),
    "מ:טעמי המקרא-סוף": frozenset({0}),
    "מ:יישור-בשני-הצדדים": frozenset({0}),
    "מ:יישור-בשני-הצדדים-סוף": frozenset({0}),
    "מ:ירושלם": frozenset({1, 2}),
    "מ:ירושלמה": frozenset({2}),
    "מ:כו״ק מיוחד": frozenset({3}),
    "מ:כל קמץ קטן מרכא": frozenset({0}),
    "מ:כפול": frozenset({3}),
    "מ:לגרמיה-2": frozenset({0}),
    "מ:מקף אפור": frozenset({0}),
    "מ:נו״ן הפוכה": frozenset({1}),
    "מ:סיום בטוב": frozenset({1}),
    "מ:ספר חדש": frozenset({1}),
    "מ:עלייה": frozenset({3, 4, 5, 6, 7}),
    "מ:פסוק": frozenset({3, 4, 5}),
    "מ:פסק": frozenset({0}),
    "מ:צינור": frozenset({2}),
    "מ:קו״כ-אם-2": frozenset({3, 4, 5}),
    "מ:קישור בהערה": frozenset({2}),
    "מ:קישור פנימי בהערה": frozenset({2}),
    "מ:קמץ": frozenset({2}),
    "מ:רווח בתרי עשר": frozenset({1}),
    "מ:רווח בתרי עשר בפסוק הראשון": frozenset({1}),
    "מ:רווח לספר בתהלים": frozenset({1}),
    "מ:רווח לספר בתהלים בפסוק הראשון": frozenset({1}),
    "מ:שוליים": frozenset({1}),
    "מ:שוליים-סוף": frozenset({0}),
    "מ:ששש": frozenset({0}),
    "מודגש": frozenset({1}),
    "נוסח": frozenset({2}),
    "ניווט טעמים": frozenset({2}),
    "סס": frozenset({0, 1}),
    "ססס": frozenset({0, 1}),
    "עוגן בשורה": frozenset({1}),
    "פפ": frozenset({0, 1}),
    "פפפ": frozenset({0, 1}),
    "פרשה-מרכז": frozenset({1}),
    "צורות כתיבה בספרי אמ״ת": frozenset({0}),
    "קו״כ": frozenset({2}),
    "קק": frozenset({2}),
    "קרי ולא כתיב": frozenset({2}),
    "ר0": frozenset({0}),
    "ר1": frozenset({0}),
    "ר2": frozenset({0}),
    "ר3": frozenset({0}),
    "ר4": frozenset({0}),
    "רווח בסוף שורה": frozenset({0}),
    "ש": frozenset({0}),
    "שם הדף המלא": frozenset({0}),
    "שני טעמים באות אחת קמץ-תחתון-פתח-עליון": frozenset({1}),
}

CURRENT_PLAIN_CUSTOM_TAG_NAMES = frozenset(
    {
        "/noinclude",
        "noinclude",
        "references/",
        "קטע התחלה=הפסוק בלי הערה/",
        "קטע התחלה=סיום בטוב/",
        "קטע התחלה=פסוק ו לפני צורת השיר/",
        "קטע התחלה=פסוק ט אחרי צורת השיר/",
        "קטע התחלה=פסוק י אחרי צורת השיר/",
        "קטע התחלה=שורה 1 לפני השיר/",
        "קטע התחלה=שורה 2 לפני השיר/",
        "קטע התחלה=שורה 3 לפני השיר/",
        "קטע התחלה=שורה 4 לפני השיר/",
        "קטע התחלה=שורה 5 לפני השיר/",
        "קטע התחלה=שורה 6 לפני השיר/",
        "קטע סוף=הפסוק בלי הערה/",
        "קטע סוף=סיום בטוב/",
        "קטע סוף=פסוק ו לפני צורת השיר/",
        "קטע סוף=פסוק ט אחרי צורת השיר/",
        "קטע סוף=פסוק י אחרי צורת השיר/",
        "קטע סוף=שורה 1 לפני השיר/",
        "קטע סוף=שורה 2 לפני השיר/",
        "קטע סוף=שורה 3 לפני השיר/",
        "קטע סוף=שורה 4 לפני השיר/",
        "קטע סוף=שורה 5 לפני השיר/",
        "קטע סוף=שורה 6 לפני השיר/",
    }
)


def validate_current_plain_template(tmpl):
    """Return a plain template's name after closed name/arity validation."""
    if not isinstance(tmpl, dict) or not ws_tmpl1.dic_is_template(tmpl):
        raise TypeError(f"not a current MAM-parsed-plain template: {tmpl!r}")
    name = ws_tmpl1.template_name(tmpl)
    allowed_arg_counts = CURRENT_PLAIN_TEMPLATE_ARG_COUNTS.get(name)
    if allowed_arg_counts is None:
        raise ValueError(f"unclassified current MAM-parsed-plain template: {name!r}")
    arg_count = len(ws_tmpl1.template_arguments(tmpl))
    if arg_count not in allowed_arg_counts:
        raise ValueError(
            f"unexpected argument count for current plain template {name!r}: "
            f"allowed {sorted(allowed_arg_counts)!r}, got {arg_count}"
        )
    return name


def validate_current_plain_custom_tag(node):
    """Return a plain custom-tag value after closed shape/name validation."""
    if not isinstance(node, dict) or set(node) != {"custom_tag"}:
        raise TypeError(f"not a current MAM-parsed-plain custom tag: {node!r}")
    value = node["custom_tag"]
    if value not in CURRENT_PLAIN_CUSTOM_TAG_NAMES:
        raise ValueError(f"unclassified current MAM-parsed-plain custom tag: {value!r}")
    return value
