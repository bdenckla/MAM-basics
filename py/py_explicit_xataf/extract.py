"""Extraction of explicit-xataf words from נוסח template arguments."""

import re

from pycmn import hebrew_points as hpo
from pycmn import template_names as tmpln
from pycmn import ws_tmpl2 as wtp

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


def flatten_arg1_strings(arg1):
    """Extract all plain strings from arg[1], which may be a list of
    strings and template dicts (e.g. {"tmpl_name": "ש"} separators).
    Adjacent strings are joined to handle angle brackets split across elements."""
    if isinstance(arg1, str):
        return [arg1]
    out = []
    for item in arg1:
        if isinstance(item, str):
            out.append(item)
    return out


def join_arg1_strings(arg1):
    """Join adjacent strings in arg[1], collapsing across template separators.
    This handles cases where angle brackets span multiple list elements."""
    if isinstance(arg1, str):
        return arg1
    parts = []
    for item in arg1:
        if isinstance(item, str):
            parts.append(item)
        else:
            parts.append("")
    return "".join(parts)


def _has_xataf(word):
    """Return whether the word contains any ḥataf vowel (including ḥataf ḥiriq)."""
    return any(hv in word for hv in XATAF_VOWELS) or XATAF_XIRIQ in word


_MATCH_KINDS = {
    _SIGLA_WORD_RE: "sigla=word",
    _BARE_WORD_RE: "bare-word",
}


def _sigla_detail(match):
    """Build sigla_detail dict from a _SIGLA_WORD_RE match."""
    sigil = match.group(1)
    return {"sigla": sigil}


def extract_xataf_word(arg1):
    """Extract the explicit-xataf word from arg[1] of a נוסח template.

    Returns (word, match_kind, sigla_detail) if found,
    or (None, None, None) if extraction fails.
    sigla_detail is a dict with "sigil" and "operator" for sigla matches, else None.
    """
    # Try each individual string first
    strings = flatten_arg1_strings(arg1)
    for s in strings:
        for regex in (_SIGLA_WORD_RE, _BARE_WORD_RE):
            for match in regex.finditer(s):
                word_group = 2 if regex is _SIGLA_WORD_RE else 1
                word = match.group(word_group).strip()
                if _has_xataf(word):
                    detail = _sigla_detail(match) if regex is _SIGLA_WORD_RE else None
                    return word, _MATCH_KINDS[regex], detail
    # Try the joined string (handles angle brackets split across elements)
    joined = join_arg1_strings(arg1)
    for regex in (_SIGLA_WORD_RE, _BARE_WORD_RE):
        for match in regex.finditer(joined):
            word_group = 2 if regex is _SIGLA_WORD_RE else 1
            word = match.group(word_group).strip()
            if _has_xataf(word):
                detail = _sigla_detail(match) if regex is _SIGLA_WORD_RE else None
                return word, _MATCH_KINDS[regex] + "+joined", detail
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
    tmpln.SCRDFF_TAR,
    'מ:נו"ן הפוכה',
    'קו"כ-אם',
)
# Templates where arg 2 is the primary word
_RETURN_ARG2_TMPL_NAMES = ("קרי ולא כתיב", "כתיב ולא קרי")
# Templates that contribute no Hebrew text (structural/spacing marks)
_ZERO_CONTENT_TMPL_NAMES = (
    "מ:לגרמיה-2",
    "מ:פסק",
    "מ:מקף אפור",
    "ר4",
    tmpln.NO_PAR_AT_STA_OF_CHAP21,
    tmpln.NO_PAR_AT_STA_OF_CHAP03,
    tmpln.NO_PAR_AT_STA_OF_WEEKLY,
)


def flatten_text(wtel):
    """Flatten a wikitext element to a plain string, for arg[0] extraction.

    For כו"ק (kethiv-qere) templates, returns only the qere (last arg),
    since the kethiv is unpointed and irrelevant to the varika word.

    For מ:דחי and מ:צינור (stress-variant) templates, returns only the
    first arg, since the second arg is the same word with different stress.
    """
    if isinstance(wtel, str):
        return wtel
    if isinstance(wtel, list):
        return "".join(flatten_text(x) for x in wtel)
    if isinstance(wtel, dict) and wtp.is_template(wtel):
        if wtp.is_template_with_name_in(wtel, tmpln._STD_KQ_TMPL_NAMES):
            return flatten_text(wtp.template_element(wtel, 2))
        if wtp.is_template_with_name_in(wtel, _STRESS_VARIANT_TMPL_NAMES):
            return flatten_text(wtp.template_element(wtel, 1))
        if wtp.is_template_with_name_in(wtel, _RETURN_ARG1_TMPL_NAMES):
            return flatten_text(wtp.template_element(wtel, 1))
        if wtp.is_template_with_name_in(wtel, _RETURN_ARG2_TMPL_NAMES):
            return flatten_text(wtp.template_element(wtel, 2))
        if wtp.is_template_with_name(wtel, "מ:קמץ"):
            return flatten_text(wtp.template_param_val(wtel, "ד"))
        if wtp.is_template_with_name_in(wtel, tmpln._WHITESPACE_TMPL_NAMES):
            return ""
        if wtp.is_template_with_name_in(wtel, _ZERO_CONTENT_TMPL_NAMES):
            return ""
        assert False, f"Unexpected template in flatten_text: {wtel}"
    return ""


def has_varika(wtel):
    """Return whether the wikitext element contains varika."""
    return hpo.VARIKA in flatten_text(wtel)


def find_nusach_tmpls(wt_seq):
    """Recursively find all נוסח templates in a wikitext sequence."""
    results = []
    for wtel in wt_seq:
        if isinstance(wtel, dict):
            if wtp.is_doc_template(wtel):
                results.append(wtel)
            elif wtp.is_template(wtel):
                for arg in wtp.template_param_vals(wtel):
                    if isinstance(arg, list):
                        results.extend(find_nusach_tmpls(arg))
        elif isinstance(wtel, list):
            results.extend(find_nusach_tmpls(wtel))
    return results
