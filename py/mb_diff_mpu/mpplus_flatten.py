"""Flatten MAM-parsed-plus EP structures to body text and track נוסח overlaps.

Exports:
    flatten_ep                      — flatten EP body text
    flatten_ep_for_diff             — flatten EP body text for diff tokenization
    flatten_ep_words_only_for_diff  — same but omits positional-punctuation templates
    flatten_element                 — flatten a nested EP element
    flatten_ep_with_nusach_for_diff — diff flatten while tracking נוסח note spans
    find_relevant_nusach            — filter note spans to those relevant to a diff
    is_parashah_template            — identify parashah-marker templates
    is_std_kq_template              — identify standard ketiv/qere templates
    is_trivial_kq_template          — identify trivial ketiv/qere templates
    is_qere_velo_ketiv_template     — identify קרי ולא כתיב templates
    is_ketiv_velo_qere_template     — identify כתיב ולא קרי templates
    strip_square_brackets           — helper for legacy qere-only bodies
"""

import difflib

from mb_cmn.hebrew_punctuation import NU_GMAQ
from mb_cmn.str_defs import DOUB_VERT_LINE
from mb_cmn.template_names import STD_KQ_TMPL_NAMES
from mb_diff_mpu.mpplus_param_access import MISSING, get_param

_PARASHAH_NAMES = {"סס", "ססס", "פפ", "פפפ"}
_STD_KQ_TEMPLATE_NAMES = frozenset(STD_KQ_TMPL_NAMES)


def is_parashah_template(name):
    """Check if template is a parashah marker (רN, סס, ססס, פפ, פפפ)."""
    if name in _PARASHAH_NAMES:
        return True
    return len(name) >= 2 and name[0] == "ר" and name[1:].isdigit()


def is_std_kq_template(name):
    """Check if template is a standard ketiv/qere body-text variant."""
    return name in _STD_KQ_TEMPLATE_NAMES


def is_trivial_kq_template(name):
    """Check if template is a trivial ketiv/qere whose body text is param 1."""
    return name in ('קו"כ-אם', 'מ:קו"כ-אם-2')


def is_qere_velo_ketiv_template(name):
    return name == "קרי ולא כתיב"


def is_ketiv_velo_qere_template(name):
    return name == "כתיב ולא קרי"


def flatten_ep(ep):
    """Flatten an EP column array to a body text string.

    Includes plain text and the body-text contribution of templates
    (e.g. נוסח param 1, קו"כ params, מ:קמץ dalet variant).
    Excludes נוסח param 2 (manuscript annotations).
    """
    return "".join(flatten_element(el) for el in ep)


def flatten_ep_for_diff(ep):
    """Flatten an EP column to diff-friendly body text.

    Unlike flatten_ep(), this keeps qere-only body text in its own token slot
    and normalizes old single-arg קרי ולא כתיב templates by synthesizing the
    visible qere from arg 1 with square brackets stripped.
    """
    buf = _new_diff_buffer()
    for el in ep:
        _flatten_diff_element(el, buf)
    return "".join(buf["parts"])


def flatten_element(el):
    if isinstance(el, str):
        return el
    if isinstance(el, dict):
        return _flatten_template(el)
    if isinstance(el, list):
        return "".join(flatten_element(x) for x in el)
    return ""


def flatten_ep_words_only_for_diff(ep):
    """Flatten EP to diff-friendly body text, omitting positional-punctuation templates.

    Identical to flatten_ep_for_diff() except that templates whose sole
    contribution is a punctuation character at a specific position in the verse
    (מ:לגרמיה, מ:לגרמיה-2, מ:פסק, מ:מקף אפור) contribute nothing to the
    output.  This lets two EPs that share the same words but differ only in
    the placement of those punctuation markers compare as equal, enabling
    same-count reorder detection in mpplus_extract._diff_ep.
    """
    buf = _new_diff_buffer()
    for el in ep:
        _flatten_diff_element_words_only(el, buf)
    return "".join(buf["parts"])


def _new_diff_buffer():
    return {"parts": [], "length": 0, "pending_break": False}


def _append_diff_text(buf, text):
    if not text:
        return
    if buf["pending_break"] and not text.startswith(" "):
        buf["parts"].append(" ")
        buf["length"] += 1
    while buf["parts"] and buf["parts"][-1].endswith(" ") and text.startswith(" "):
        text = text[1:]
        if not text:
            buf["pending_break"] = False
            return
    buf["parts"].append(text)
    buf["length"] += len(text)
    buf["pending_break"] = False


def _append_diff_word(buf, word):
    if not word:
        return
    if buf["parts"] and not buf["parts"][-1].endswith(" "):
        buf["parts"].append(" ")
        buf["length"] += 1
    buf["parts"].append(word)
    buf["length"] += len(word)
    buf["pending_break"] = True


def strip_square_brackets(text):
    return text.replace("[", "").replace("]", "")


def _qere_velo_ketiv_body_for_diff(tmpl):
    p2 = get_param(tmpl, "2")
    if p2 is not MISSING:
        return flatten_element(p2)
    p1 = get_param(tmpl, "1")
    if p1 is MISSING:
        return ""
    return strip_square_brackets(flatten_element(p1))


def _flatten_diff_element(el, buf):
    if isinstance(el, str):
        _append_diff_text(buf, el)
        return
    if isinstance(el, dict):
        _flatten_diff_template(el, buf)
        return
    if isinstance(el, list):
        for item in el:
            _flatten_diff_element(item, buf)


def _append_diff_special_punctuation(name, buf):
    if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
        _append_diff_text(buf, "׀")
        return True
    if name == "מ:פסק":
        _append_diff_text(buf, DOUB_VERT_LINE)
        return True
    if name == "מ:מקף אפור":
        _append_diff_text(buf, NU_GMAQ)
        return True
    return False


def _flatten_diff_template(tmpl, buf):
    name = tmpl["tmpl_name"]
    if is_parashah_template(name):
        _append_diff_text(buf, " ")
        return
    if name == "נוסח":
        p1 = get_param(tmpl, "1")
        if p1 is not MISSING:
            _flatten_diff_element(p1, buf)
        return
    if is_std_kq_template(name):
        p2 = get_param(tmpl, "2")
        if p2 is not MISSING:
            _flatten_diff_element(p2, buf)
        return
    if is_qere_velo_ketiv_template(name):
        _append_diff_word(buf, _qere_velo_ketiv_body_for_diff(tmpl))
        return
    if is_trivial_kq_template(name):
        p1 = get_param(tmpl, "1")
        if p1 is not MISSING:
            _flatten_diff_element(p1, buf)
        return
    if is_ketiv_velo_qere_template(name):
        return
    if name == "מ:קמץ":
        pd = get_param(tmpl, "ד")
        if pd is not MISSING:
            _flatten_diff_element(pd, buf)
        return
    if _append_diff_special_punctuation(name, buf):
        return
    if name == "מ:כפול":
        pk = get_param(tmpl, "כפול")
        if pk is not MISSING:
            _flatten_diff_element(pk, buf)
        return
    p1 = get_param(tmpl, "1")
    if p1 is not MISSING:
        _flatten_diff_element(p1, buf)


def _flatten_diff_element_words_only(el, buf):
    if isinstance(el, str):
        _append_diff_text(buf, el)
        return
    if isinstance(el, dict):
        _flatten_diff_template_words_only(el, buf)
        return
    if isinstance(el, list):
        for item in el:
            _flatten_diff_element_words_only(item, buf)


def _flatten_diff_template_words_only(tmpl, buf):
    """Like _flatten_diff_template but positional-punctuation templates are no-ops."""
    name = tmpl["tmpl_name"]
    if is_parashah_template(name):
        _append_diff_text(buf, " ")
        return
    if name == "נוסח":
        p1 = get_param(tmpl, "1")
        if p1 is not MISSING:
            _flatten_diff_element_words_only(p1, buf)
        return
    if is_std_kq_template(name):
        p2 = get_param(tmpl, "2")
        if p2 is not MISSING:
            _flatten_diff_element_words_only(p2, buf)
        return
    if is_qere_velo_ketiv_template(name):
        _append_diff_word(buf, _qere_velo_ketiv_body_for_diff(tmpl))
        return
    if is_trivial_kq_template(name):
        p1 = get_param(tmpl, "1")
        if p1 is not MISSING:
            _flatten_diff_element_words_only(p1, buf)
        return
    if is_ketiv_velo_qere_template(name):
        return
    if name == "מ:קמץ":
        pd = get_param(tmpl, "ד")
        if pd is not MISSING:
            _flatten_diff_element_words_only(pd, buf)
        return
    # Positional-punctuation templates: deliberately omitted (no contribution)
    if name in ("מ:לגרמיה-2", "מ:לגרמיה", "מ:פסק", "מ:מקף אפור"):
        return
    if name == "מ:כפול":
        pk = get_param(tmpl, "כפול")
        if pk is not MISSING:
            _flatten_diff_element_words_only(pk, buf)
        return
    p1 = get_param(tmpl, "1")
    if p1 is not MISSING:
        _flatten_diff_element_words_only(p1, buf)


def _flatten_template(tmpl):
    name = tmpl["tmpl_name"]
    if is_parashah_template(name):
        return " "
    if name == "נוסח":
        p1 = get_param(tmpl, "1")
        return flatten_element(p1) if p1 is not MISSING else ""
    if is_std_kq_template(name) or is_qere_velo_ketiv_template(name):
        p2 = get_param(tmpl, "2")
        return flatten_element(p2) if p2 is not MISSING else ""
    if is_trivial_kq_template(name):
        p1 = get_param(tmpl, "1")
        return flatten_element(p1) if p1 is not MISSING else ""
    if is_ketiv_velo_qere_template(name):
        return ""
    if name == "מ:קמץ":
        pd = get_param(tmpl, "ד")
        return flatten_element(pd) if pd is not MISSING else ""
    if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
        return "׀"
    if name == "מ:פסק":
        return DOUB_VERT_LINE
    if name == "מ:מקף אפור":
        return NU_GMAQ
    if name == "מ:כפול":
        pk = get_param(tmpl, "כפול")
        return flatten_element(pk) if pk is not MISSING else ""
    p1 = get_param(tmpl, "1")
    if p1 is not MISSING:
        return flatten_element(p1)
    return ""


def _flatten_ep_with_nusach(ep):
    """Flatten EP column and track נוסח templates that have param 2."""
    parts = []
    notes = []
    for el in ep:
        _flatten_tracking(el, parts, notes)
    return "".join(parts), notes


def flatten_ep_with_nusach_for_diff(ep):
    """Flatten EP column for diffing and track נוסח templates that have param 2."""
    buf = _new_diff_buffer()
    notes = []
    for el in ep:
        _flatten_tracking_for_diff(el, buf, notes)
    return "".join(buf["parts"]), notes


def _flatten_tracking(obj, parts, notes):
    if isinstance(obj, str):
        parts.append(obj)
    elif isinstance(obj, dict):
        _flatten_template_tracking(obj, parts, notes)
    elif isinstance(obj, list):
        for item in obj:
            _flatten_tracking(item, parts, notes)


def _flatten_tracking_for_diff(obj, buf, notes):
    if isinstance(obj, str):
        _append_diff_text(buf, obj)
    elif isinstance(obj, dict):
        _flatten_template_tracking_for_diff(obj, buf, notes)
    elif isinstance(obj, list):
        for item in obj:
            _flatten_tracking_for_diff(item, buf, notes)


def _flatten_template_tracking(tmpl, parts, notes):
    name = tmpl["tmpl_name"]
    if is_parashah_template(name):
        parts.append(" ")
        return
    if name == "נוסח":
        start = sum(len(p) for p in parts)
        p1 = get_param(tmpl, "1")
        if p1 is not MISSING:
            _flatten_tracking(p1, parts, notes)
        end = sum(len(p) for p in parts)
        p2 = get_param(tmpl, "2")
        if p2 is not MISSING:
            notes.append({"start": start, "end": end, "param2": p2})
        return
    if is_std_kq_template(name) or is_qere_velo_ketiv_template(name):
        p2 = get_param(tmpl, "2")
        if p2 is not MISSING:
            _flatten_tracking(p2, parts, notes)
        return
    if is_trivial_kq_template(name):
        p1 = get_param(tmpl, "1")
        if p1 is not MISSING:
            _flatten_tracking(p1, parts, notes)
        return
    if is_ketiv_velo_qere_template(name):
        return
    if name == "מ:קמץ":
        pd = get_param(tmpl, "ד")
        if pd is not MISSING:
            _flatten_tracking(pd, parts, notes)
        return
    if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
        parts.append("׀")
        return
    if name == "מ:פסק":
        parts.append("׀")
        return
    if name == "מ:כפול":
        pk = get_param(tmpl, "כפול")
        if pk is not MISSING:
            _flatten_tracking(pk, parts, notes)
        return
    p1 = get_param(tmpl, "1")
    if p1 is not MISSING:
        _flatten_tracking(p1, parts, notes)


def _flatten_template_tracking_for_diff(tmpl, buf, notes):
    name = tmpl["tmpl_name"]
    if is_parashah_template(name):
        _append_diff_text(buf, " ")
        return
    if name == "נוסח":
        start = buf["length"]
        p1 = get_param(tmpl, "1")
        if p1 is not MISSING:
            _flatten_tracking_for_diff(p1, buf, notes)
        end = buf["length"]
        p2 = get_param(tmpl, "2")
        if p2 is not MISSING:
            notes.append({"start": start, "end": end, "param2": p2})
        return
    if is_std_kq_template(name):
        p2 = get_param(tmpl, "2")
        if p2 is not MISSING:
            _flatten_tracking_for_diff(p2, buf, notes)
        return
    if is_qere_velo_ketiv_template(name):
        _append_diff_word(buf, _qere_velo_ketiv_body_for_diff(tmpl))
        return
    if is_trivial_kq_template(name):
        p1 = get_param(tmpl, "1")
        if p1 is not MISSING:
            _flatten_tracking_for_diff(p1, buf, notes)
        return
    if is_ketiv_velo_qere_template(name):
        return
    if name == "מ:קמץ":
        pd = get_param(tmpl, "ד")
        if pd is not MISSING:
            _flatten_tracking_for_diff(pd, buf, notes)
        return
    if _append_diff_special_punctuation(name, buf):
        return
    if name == "מ:כפול":
        pk = get_param(tmpl, "כפול")
        if pk is not MISSING:
            _flatten_tracking_for_diff(pk, buf, notes)
        return
    p1 = get_param(tmpl, "1")
    if p1 is not MISSING:
        _flatten_tracking_for_diff(p1, buf, notes)


def _changed_new_positions(old_text, new_text):
    """Return set of character positions in new_text that are changed/added."""
    sm = difflib.SequenceMatcher(None, old_text, new_text, autojunk=False)
    changed = set()
    for op, _i1, _i2, j1, j2 in sm.get_opcodes():
        if op in ("replace", "insert"):
            changed.update(range(j1, j2))
    return changed


def find_relevant_nusach(old_text, new_text, notes, text_changed):
    """Filter nusach notes to those relevant to the change."""
    if not notes:
        return []
    if not text_changed:
        return list(notes)
    changed = _changed_new_positions(old_text, new_text)
    result = []
    for note in notes:
        note_positions = range(note["start"], note["end"])
        if any(pos in note_positions for pos in changed):
            result.append(note)
    return result
