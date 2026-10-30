"""Extraction of explicit-xataf words from נוסח template arguments."""

import re
import unicodedata

from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import kq_special_templates as kqst
from mb_cmn import template_names as tmpln
from mb_cmn import ws_tmpl2 as wtp

XATAF_VOWELS = (hpo.XSEGOL, hpo.XPATAX, hpo.XQAMATS)
XATAF_XIRIQ = hpo.SHEVA + hpo.XIRIQ  # sheva+xiriq sequence (no single Unicode char)

_HEB_WORD_CHARS = (
    rf"[{hpo.RECC_HEBR}\u05be \u05f4]"  # Hebrew + maqaf + space + gershayim
)

# Pattern 1: sigla=word (annotation) — with optional angle brackets and space after =
# ? and ! bind tightly to individual sigla (e.g. ל,ק3?=word means ק3 is uncertain)
_SIGLA_WORD_RE = re.compile(
    r"([^\s=]+)"  # capture 1: sigil(s), may include ? or ! suffixes
    r"="  # equals sign separating sigla from word
    r"\s*"  # optional space after =
    r"<?"  # optional opening angle bracket
    r"(" + _HEB_WORD_CHARS + r"+)"  # capture 2: the word
    r">?"  # optional closing angle bracket
    r"\s*[(<]"  # space then '(' or '<' for annotation/question
)

# Pattern 2: bare word (annotation) — no sigla= prefix, word at start of string
_BARE_WORD_RE = re.compile(
    r"^"
    r"<?"  # optional opening angle bracket
    r"(" + _HEB_WORD_CHARS + r"+)"  # capture group for the word
    r">?"  # optional closing angle bracket
    r"\s*[(<]"  # space then '(' or '<' for annotation/question
)

# Pattern 3: sigla=plus form (packed form) — plus notation writes one letter twice,
# joined by '+', each copy with some of that letter's marks; the packed form after it,
# in parentheses, writes the letter once with all of them, and is the word returned.
_HEB_ATOM_CHARS = rf"[{hpo.RECC_HEBR}]"  # Hebrew, maqaf, CGJ and varika; no space
_SIGLA_PLUS_FORM_RE = re.compile(
    r"([^\s=]+)"  # capture 1: sigil(s), as in pattern 1
    r"="  # equals sign separating sigla from the plus form
    r"(" + _HEB_ATOM_CHARS + r"+\+" + _HEB_ATOM_CHARS + r"+)"  # capture 2: plus form
    r" \("  # space then '(' before the packed form
    r"(" + _HEB_ATOM_CHARS + r"+)"  # capture 3: the packed form
    r"\)"  # and its closing parenthesis
)


def flatten_arg1_strings(arg1):
    """Extract all plain strings from arg[1], which may be a list of
    strings and template dicts (e.g. {"tmpl_name": "ש"} separators).
    Adjacent strings are joined to handle angle brackets split across elements.

    A template is left out of the strings, but it must be one join_arg1_strings
    classifies, so an unknown one raises here; until 2026-10-21 any template,
    known or not, was passed over.
    """
    if isinstance(arg1, str):
        return [arg1]
    if not isinstance(arg1, list):
        raise TypeError(f"unclassified MAM note-body node: {type(arg1).__name__}")
    out = []
    for item in arg1:
        if isinstance(item, str):
            out.append(item)
        else:
            join_arg1_strings(item)
    return out


def join_arg1_strings(arg1):
    """Join the visible note text, collapsing across explicit line separators."""
    if isinstance(arg1, str):
        return arg1
    if isinstance(arg1, list):
        return "".join(join_arg1_strings(item) for item in arg1)
    if not isinstance(arg1, dict) or not wtp.is_template(arg1):
        raise TypeError(f"unclassified MAM note-body node: {type(arg1).__name__}")

    tmpln.validate_current_plus_template(arg1)
    tmpl_name = wtp.template_name(arg1)
    if tmpl_name == "ש":
        return ""
    if tmpl_name in {
        "מודגש",
        "מ:אות-ג",
        "מ:אות-ק",
        "מ:אות תלויה",
        tmpln.SLH_WORD,
    }:
        return join_arg1_strings(wtp.template_param_val(arg1, "1"))
    if tmpl_name in {"מ:קישור בהערה", "מ:קישור פנימי בהערה"}:
        return join_arg1_strings(wtp.template_param_val(arg1, "2"))
    if tmpl_name in {"מ:לגרמיה-2", "מ:פסק"}:
        return hpu.PASOLEG
    raise ValueError(f"unclassified MAM note-body template: {tmpl_name!r}")


def _has_xataf(word):
    """Return whether the word contains any ḥataf vowel (including ḥataf ḥiriq)."""
    return any(hv in word for hv in XATAF_VOWELS) or XATAF_XIRIQ in word


_MATCH_KINDS = {
    _SIGLA_WORD_RE: "sigla=word",
    _BARE_WORD_RE: "bare-word",
    _SIGLA_PLUS_FORM_RE: "sigla=plus-form",
}

# The patterns in the order tried, each with the group holding its word.
_PATTERN_WORD_GROUPS = (
    (_SIGLA_WORD_RE, 2),
    (_BARE_WORD_RE, 1),
    (_SIGLA_PLUS_FORM_RE, 3),
)


def _sigla_detail(match):
    """Build sigla_detail dict from a _SIGLA_WORD_RE or _SIGLA_PLUS_FORM_RE match."""
    sigil = match.group(1)
    return {"sigla": sigil}


def _letters(form):
    return "".join(ch for ch in form if unicodedata.category(ch) != "Mn")


def _check_plus_form(match):
    """Raise unless the plus form folds into the packed form: the letters on the two
    sides of '+' are one letter, which the packed form writes once among the same
    letters."""
    plus_form, packed = match.group(2), match.group(3)
    before, after = (_letters(part) for part in plus_form.split("+"))
    if before[-1:] != after[:1] or before + after[1:] != _letters(packed):
        raise ValueError(
            f"plus form {plus_form!r} does not fold into its packed form {packed!r}"
        )


def _xataf_match(s, kind_suffix=""):
    """The first pattern match in s whose word has a ḥataf, as extract_xataf_word
    returns it, or None."""
    for regex, word_group in _PATTERN_WORD_GROUPS:
        for match in regex.finditer(s):
            if regex is _SIGLA_PLUS_FORM_RE:
                _check_plus_form(match)
            word = match.group(word_group).strip()
            if _has_xataf(word):
                detail = _sigla_detail(match) if regex is not _BARE_WORD_RE else None
                return word, _MATCH_KINDS[regex] + kind_suffix, detail
    return None


def extract_xataf_word(arg1):
    """Extract the explicit-xataf word from arg[1] of a נוסח template.

    Returns (word, match_kind, sigla_detail) if found,
    or (None, None, None) if extraction fails.
    sigla_detail is a dict with "sigil" and "operator" for sigla matches, else None.
    """
    # Try each individual string first
    for s in flatten_arg1_strings(arg1):
        if found := _xataf_match(s):
            return found
    # Try the joined string (handles angle brackets split across elements)
    if found := _xataf_match(join_arg1_strings(arg1), "+joined"):
        return found
    return None, None, None


def classify_failure(arg1):
    """Return a short reason why extraction failed."""
    joined = join_arg1_strings(arg1)
    if "חטף" not in joined:
        return "no ḥataf in alternative reading"
    return "non-standard format (inline reference or other)"


_STRESS_VARIANT_TMPL_NAMES = ("מ:דחי", "מ:צינור")
_SLH_TMPL_NAMES = (tmpln.SLH_WORD, "מ:אות-ג", "מ:אות-ק", "מ:אות תלויה")
# Templates where arg 1 is the target/primary text (return it, ignore annotation args)
_RETURN_ARG1_TMPL_NAMES = _SLH_TMPL_NAMES + (
    tmpln.SILLUQ_BEFORE_METEG,
    tmpln.SCRDFF_TAR,
    "מ:נו״ן הפוכה",
    "מ:קו״כ-אם-2",
)
# Templates where arg 2 is the primary word
_RETURN_ARG2_TMPL_NAMES = ("קרי ולא כתיב", "כתיב ולא קרי")
# Templates that contribute no Hebrew text (structural marks).  MAM has whitespace after
# every legarmeh, and the three chapter tags never stand between two atoms.
_ZERO_CONTENT_TMPL_NAMES = (
    "מ:לגרמיה-2",
    tmpln.NO_PAR_AT_STA_OF_CHAP21,
    tmpln.NO_PAR_AT_STA_OF_CHAP03,
    tmpln.NO_PAR_AT_STA_OF_WEEKLY,
)
# Templates that stand between two atoms with no whitespace on either side, so each
# contributes a space, as the whitespace templates do: nothing would run the two atoms
# together, as it did until 2026-10-21 (Psalms 106:1's הַ֥לְﬞלוּ and יָ֨הּ came out as one
# atom).  MAM's gray maqaf is read here as a space, as near-Aleppo reads it; the
# narrow-sense paseq's glyph is left out, as before, but not the boundary it marks.
_SEPARATOR_TMPL_NAMES = ("מ:מקף אפור", "מ:פסק", "ר4")


def flatten_text(wtel):
    """Flatten a wikitext element to a plain string, for arg[0] extraction.

    For כו״ק (kethiv-qere) templates, returns only the qere (last arg),
    since the kethiv is unpointed and irrelevant to the varika word.

    For מ:דחי and מ:צינור (stress-variant) templates, returns only the
    first arg, since the second arg is the same word with different stress.

    A whitespace template or one of _SEPARATOR_TMPL_NAMES returns a space.
    """
    if isinstance(wtel, str):
        return wtel
    if isinstance(wtel, list):
        return "".join(flatten_text(x) for x in wtel)
    if isinstance(wtel, dict) and wtp.is_template(wtel):
        tmpln.validate_current_plus_template(wtel)
        tmpl_name = wtp.template_name(wtel)
        if kqst.is_special_kq_template_name(tmpl_name):
            assert kqst.is_unified_special_kq_template_name(tmpl_name), tmpl_name
            _validate_special_kq_if_needed(wtel)
            return flatten_text(wtp.template_element(wtel, 2))
        if wtp.is_template_with_name_in(wtel, tmpln.STD_KQ_TMPL_NAMES):
            return flatten_text(wtp.template_element(wtel, 2))
        if wtp.is_template_with_name_in(wtel, _STRESS_VARIANT_TMPL_NAMES):
            return flatten_text(wtp.template_element(wtel, 1))
        if wtp.is_template_with_name_in(wtel, _RETURN_ARG1_TMPL_NAMES):
            return flatten_text(wtp.template_element(wtel, 1))
        if wtp.is_template_with_name_in(wtel, _RETURN_ARG2_TMPL_NAMES):
            return flatten_text(wtp.template_element(wtel, 2))
        if wtp.is_template_with_name(wtel, "מ:קמץ"):
            return flatten_text(wtp.template_param_val(wtel, "ד"))
        if wtp.is_template_with_name_in(wtel, tmpln.WHITESPACE_TMPL_NAMES):
            return " "
        if wtp.is_template_with_name_in(wtel, _SEPARATOR_TMPL_NAMES):
            return " "
        if wtp.is_template_with_name_in(wtel, _ZERO_CONTENT_TMPL_NAMES):
            return ""
        raise ValueError(f"Unexpected template in flatten_text: {wtel}")
    raise TypeError(f"Unexpected node in flatten_text: {type(wtel).__name__}")


def _validate_special_kq_if_needed(tmpl):
    tmpl_name = wtp.template_name(tmpl)
    if not kqst.is_special_kq_template_name(tmpl_name):
        return
    sug_text = None
    if "סוג" in wtp.template_param_keys(tmpl):
        sug_val = wtp.template_param_val(tmpl, "סוג")
        assert len(sug_val) == 1 and isinstance(sug_val[0], str), sug_val
        sug_text = sug_val[0]
    kqst.canonical_special_kq_type_from_name_and_sug(tmpl_name, sug_text)


def has_varika(wtel):
    """Return whether the wikitext element contains varika."""
    return hpo.VARIKA in flatten_text(wtel)


def find_docnote_tmpls(wt_seq):
    """Find every topmost נוסח call in all recognized dataset branches.

    Documentation-note discovery is a whole-dataset inventory, so every
    parameter of every recognized non-note template is deliberately searched.
    Every encountered template is validated before discovery or recursion.
    A new template raises until its fields have been classified.
    """
    results = []
    for wtel in wt_seq:
        if isinstance(wtel, dict):
            params = tmpln.validate_current_plus_template(wtel)
            if wtp.is_doc_template(wtel):
                results.append(wtel)
            else:
                for _param_name, arg in params.items():
                    results.extend(find_docnote_tmpls([arg]))
        elif isinstance(wtel, list):
            results.extend(find_docnote_tmpls(wtel))
        elif not isinstance(wtel, str):
            raise TypeError(
                f"Unexpected node in plus documentation-note inventory: {type(wtel).__name__}"
            )
    return results
