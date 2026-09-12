"""Exports Latin-alphabet symbols for some template names

QUOTE MARKS: a name here with a quote mark uses Hebrew gershayim (U+05F4),
which is the canonical form of the name rather than one format's variant of it.
The raw wikitext writes an ASCII double quote as a shorthand for the gershayim,
and ``ws_tmpl1.template_name()`` resolves that shorthand — it normalizes the quote
to gershayim for both the ``stmpl`` and the ``tmpl`` shape, via
``py_misc.true_gershayim``, whose ``in_str`` is named for treating the gershayim as
the true character and the ASCII quote as the stand-in. So the parsed name is
always the canonical one, and these constants are what it equals.

The shorthand is still visible in stored data, which is the one thing to watch:
MAM-parsed-PLAIN keeps the raw wikitext spelling in its ``stmpl`` strings and
``tmpl`` lists — ``קו"כ``, ``מ:קו"כ-אם-2``, ``מ:כו"ק מיוחד``,
``מ:אין פרשה בתחילת פרק בספרי אמ"ת`` — so a raw plain name compared without going
through ``template_name()`` will not equal any constant here. MAM-parsed-PLUS
stores the canonical spelling directly in ``tmpl_name`` and can be compared raw,
and has since MAM-parsed 2993dbd of 2026-05-09, "Use g2 not q2 in tmpl names".
Before 2993dbd, though, plus data has the ASCII shorthand in ``tmpl_name`` just as
plain data does. So code reading plus data from arbitrary git revisions, rather than
from the working tree, must normalize the quote before comparing;
``py/mb_diff_mpu/mpplus_extract.py``'s ``_canonicalize_template_names`` is the
worked example.
Names with no quote mark are spelled identically everywhere and raise none of this.
"""

# Named because more than one comparison site needs them, in this repo's siblings
# as well as here; see the quote-mark note above for how each name is spelled.
INVERTED_NUN = "מ:נו״ן הפוכה"
TRIVIAL_QERE = "מ:קו״כ-אם-2"
QAMATS_VARIANT = "מ:קמץ"
DUAL_CANTILLATION = "מ:כפול"
STRESS_HELPER_TMPL_NAMES = frozenset(("מ:דחי", "מ:צינור"))

TWO_ACCENTS_OF_QUPO = "שני טעמים באות אחת קמץ-תחתון-פתח-עליון"
NO_PAR_AT_STA_OF_CHAP21 = "מ:אין פרשה בתחילת פרק"
NO_PAR_AT_STA_OF_CHAP03 = "מ:אין פרשה בתחילת פרק בספרי אמ״ת"
NO_PAR_AT_STA_OF_WEEKLY = "מ:אין רווח של פרשה בתחילת פרשת השבוע"
SLH_WORD = "מ:אות-מיוחדת-במילה"
SCRDFF_TAR = "מ:הערה-2"
SCRDFF_NO_TAR = "מ:הערה"

LATIN_SHORTS = {
    "כו״ק": "k1q1-kq",  # 1
    "קו״כ": "k1q1-qk",  # 2
    TRIVIAL_QERE: "kq-trivial",
    "קרי ולא כתיב": "kq-q-velo-k",
    "כתיב ולא קרי": "kq-k-velo-q",
}
#  1: a normal ketiv/qere.
#  2: a ketiv/qere where template arguments are in kq order but they should be rendered in reverse order (qk order).
# Retired special-kq subtypes (k1q1-mcom through k3q3) are intentionally
# excluded from this modern-only module.


def map_all_std_kq_to_a_constant(the_constant):
    return {n: the_constant for n in STD_KQ_TMPL_NAMES}


def map_all_whitespace_to_a_constant(the_constant):
    return {n: the_constant for n in WHITESPACE_TMPL_NAMES}


STD_KQ_TMPL_NAMES = (
    "כו״ק",
    "קו״כ",
    "מ:כו״ק מיוחד",
)
WHITESPACE_TMPL_NAMES = {
    "מ:ששש",
    "סס",
    "פפ",
    "ססס",
    "פפפ",
    "ר0",
    "ר1",
    "ר2",
    "ר3",
}

# TEMPLATES THAT CONTRIBUTE NO ATOM.  None of them is an atom and none joins the
# atoms around it, so a text collector renders each as a separator.  THERE IS NO
# FALLBACK BEHIND THIS SET: a name absent from it, and from every rule of its
# own, raises -- Ben Denckla's decision of 2026-09-02, "Don't have any fallbacks.
# If you don't recognize a template, fail fast."  So a template that reaches a
# verse payload has to be listed here or handled by name somewhere.
#
# TWO KINDS SIT HERE, FOR THE ONE THING THEY SHARE.  Most have no mark at all:
# WHITESPACE_TMPL_NAMES' shirah spaces and setuma/petucha and poetic-space
# markers, ר4 alongside them, the three no-parashah chapter tags, and the
# navigation and titling furniture, whose parameters are a verse reference, an
# aliyah identifier, a book title, a prophet name and a Psalms division name.
# The paseq, legarmeh and gray-maqaf templates DO have a mark, and are here
# because that mark is not an atom; whether one of them renders U+05C0 or a
# maqaf is a separate question, which Ben Denckla settled as separate on
# 2026-09-02.  That is also why the set is not called "no verse text", which
# would be false of those three.
#
# NAMED AS A SET BECAUSE WHAT A TEMPLATE MEANS DECIDES WHAT IT CONTRIBUTES,
# and whether it has parameters does not.  The corpus evidence, and the
# defect that reading a parameter as a proxy for meaning produced, are recorded
# at hkq_cmn/mam_plus_verse_data._collect_text_fragments.
NO_ATOM_TMPL_NAMES = WHITESPACE_TMPL_NAMES | {
    "ר4",
    "מ:פסק",
    "מ:לגרמיה-2",
    "מ:מקף אפור",
    NO_PAR_AT_STA_OF_CHAP21,
    NO_PAR_AT_STA_OF_CHAP03,
    NO_PAR_AT_STA_OF_WEEKLY,
    "מ:פסוק",
    "מ:עלייה",
    "מ:ספר חדש",
    "מ:רווח בתרי עשר בפסוק הראשון",
    "מ:רווח לספר בתהלים בפסוק הראשון",
}

# TEMPLATES WHOSE PARAM 1 IS THE WORD, OR THE PART OF IT, THAT THEY MARK: the
# large, small and hung letters, and the whole word a special letter sits in.
# Shared so that hkq_cmn/mam_plus_verse_data and hkq_cmn/qere_projection cannot
# drift apart on it, their header comments each requiring that they mirror.
IN_WORD_TMPL_NAMES = {
    "מ:אות-ג",
    "מ:אות-ק",
    "מ:אות תלויה",
    SLH_WORD,
}

# Every template name present in the current MAM-parsed-plus corpus.  This is
# the closed roster for whole-dataset inventories and structure-preserving
# transformations.  A caller that walks every parameter still has to opt into
# that scope explicitly; membership here does not decide which parameters a
# Scripture projection should select.
CURRENT_PLUS_TMPL_NAMES = frozenset(
    {
        "כו״ק",
        "כתיב ולא קרי",
        "מ:אות תלויה",
        "מ:אות-ג",
        SLH_WORD,
        "מ:אות-ק",
        NO_PAR_AT_STA_OF_CHAP21,
        NO_PAR_AT_STA_OF_CHAP03,
        NO_PAR_AT_STA_OF_WEEKLY,
        *STRESS_HELPER_TMPL_NAMES,
        SCRDFF_TAR,
        "מ:כו״ק מיוחד",
        DUAL_CANTILLATION,
        "מ:לגרמיה-2",
        "מ:מקף אפור",
        INVERTED_NUN,
        "מ:סיום בטוב",
        "מ:ספר חדש",
        "מ:עלייה",
        "מ:פסוק",
        "מ:פסק",
        TRIVIAL_QERE,
        "מ:קישור בהערה",
        "מ:קישור פנימי בהערה",
        QAMATS_VARIANT,
        "מ:רווח בתרי עשר בפסוק הראשון",
        "מ:רווח לספר בתהלים בפסוק הראשון",
        "מ:ששש",
        "מודגש",
        "נוסח",
        "סס",
        "ססס",
        "פפ",
        "פפפ",
        "קו״כ",
        "קרי ולא כתיב",
        "ר0",
        "ר1",
        "ר2",
        "ר3",
        "ר4",
        "ש",
    }
)


# Closed parameter schemas for the CURRENT MAM-parsed-plus corpus.  Each entry is
# ``(required keys, allowed keys)``.  Whole-structure inventories may visit every
# allowed key only after this validation; Scripture projections still choose among
# the named keys according to their own question.
_NO_PARAM_PLUS_TEMPLATES = frozenset(
    {
        NO_PAR_AT_STA_OF_CHAP21,
        NO_PAR_AT_STA_OF_CHAP03,
        NO_PAR_AT_STA_OF_WEEKLY,
        "מ:לגרמיה-2",
        "מ:מקף אפור",
        "מ:פסק",
        "מ:ששש",
        "ר0",
        "ר1",
        "ר2",
        "ר3",
        "ר4",
        "ש",
    }
)
_OPTIONAL_PARAM1_PLUS_TEMPLATES = frozenset({"סס", "ססס", "פפ", "פפפ"})
CURRENT_PLUS_PARAM_POLICY = {
    **{name: (frozenset(), frozenset()) for name in _NO_PARAM_PLUS_TEMPLATES},
    **{
        name: (frozenset(), frozenset({"1"}))
        for name in _OPTIONAL_PARAM1_PLUS_TEMPLATES
    },
    "כו״ק": (frozenset({"1", "2"}), frozenset({"1", "2"})),
    "קו״כ": (frozenset({"1", "2"}), frozenset({"1", "2"})),
    "מ:כו״ק מיוחד": (
        frozenset({"1", "2", "סוג"}),
        frozenset({"1", "2", "סוג"}),
    ),
    TRIVIAL_QERE: (
        frozenset({"1", "2", "3"}),
        frozenset({"1", "2", "3", "מקורות", "סוג"}),
    ),
    "כתיב ולא קרי": (
        frozenset({"1", "2"}),
        frozenset({"1", "2", "3"}),
    ),
    "קרי ולא כתיב": (frozenset({"1", "2"}), frozenset({"1", "2"})),
    **{name: (frozenset({"1"}), frozenset({"1"})) for name in IN_WORD_TMPL_NAMES},
    SLH_WORD: (
        frozenset({"1", "2", "3", "4", "5"}),
        frozenset({"1", "2", "3", "4", "5"}),
    ),
    **{
        name: (frozenset({"1", "2"}), frozenset({"1", "2"}))
        for name in STRESS_HELPER_TMPL_NAMES
    },
    SCRDFF_TAR: (
        frozenset({"1", "2", "3"}),
        frozenset({"1", "2", "3"}),
    ),
    DUAL_CANTILLATION: (
        frozenset({"כפול", "א", "ב"}),
        frozenset({"כפול", "א", "ב"}),
    ),
    INVERTED_NUN: (frozenset({"1"}), frozenset({"1"})),
    "מ:סיום בטוב": (frozenset({"1"}), frozenset({"1"})),
    "מ:ספר חדש": (frozenset({"1"}), frozenset({"1"})),
    "מ:רווח בתרי עשר בפסוק הראשון": (
        frozenset({"1"}),
        frozenset({"1"}),
    ),
    "מ:רווח לספר בתהלים בפסוק הראשון": (
        frozenset({"1"}),
        frozenset({"1"}),
    ),
    "מ:עלייה": (
        frozenset({"א", "ב0"}),
        frozenset({"א", "ב0", "ב1", "ב2", "ב3", "ג0", "ג1", "ג2", "ג3"}),
    ),
    "מ:פסוק": (
        frozenset({"1", "2", "3"}),
        frozenset({"1", "2", "3", "סדר", "עלייה"}),
    ),
    "מ:קישור בהערה": (
        frozenset({"1", "2"}),
        frozenset({"1", "2"}),
    ),
    "מ:קישור פנימי בהערה": (
        frozenset({"1", "2"}),
        frozenset({"1", "2"}),
    ),
    QAMATS_VARIANT: (
        frozenset({"ד", "ס"}),
        frozenset({"ד", "ס"}),
    ),
    "מודגש": (frozenset({"1"}), frozenset({"1"})),
    "נוסח": (frozenset({"1", "2"}), frozenset({"1", "2"})),
}
assert frozenset(CURRENT_PLUS_PARAM_POLICY) == CURRENT_PLUS_TMPL_NAMES


def validate_current_plus_template(tmpl):
    """Return a current plus template's params after closed name/shape validation."""
    if not isinstance(tmpl, dict) or not isinstance(tmpl.get("tmpl_name"), str):
        raise TypeError(f"not a current MAM-parsed-plus template: {tmpl!r}")
    raw_name = tmpl["tmpl_name"]
    name = raw_name.replace('"', "\N{HEBREW PUNCTUATION GERSHAYIM}")
    policy = CURRENT_PLUS_PARAM_POLICY.get(name)
    if policy is None:
        raise ValueError(f"unclassified current MAM-parsed-plus template: {raw_name!r}")
    extra_object_keys = set(tmpl) - {"tmpl_name", "tmpl_params"}
    if extra_object_keys:
        raise ValueError(
            f"unexpected object keys for current plus template {name!r}: "
            f"{sorted(extra_object_keys)!r}"
        )
    params = tmpl.get("tmpl_params", {})
    if not isinstance(params, dict):
        raise TypeError(
            f"non-mapping params for current plus template {name!r}: {params!r}"
        )
    required, allowed = policy
    actual = frozenset(params)
    if not required <= actual or not actual <= allowed:
        raise ValueError(
            f"unexpected parameters for current plus template {name!r}: "
            f"required {sorted(required)!r}, allowed {sorted(allowed)!r}, "
            f"got {sorted(actual)!r}"
        )
    return params
