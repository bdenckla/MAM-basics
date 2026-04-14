"""Flatten MPP EP structures to body text and track נוסח overlaps.

Exports:
    flatten_ep           — flatten EP body text
    _flatten_element     — flatten a nested EP element
    _flatten_ep_with_nusach — flatten while tracking נוסח note spans
    _find_relevant_nusach — filter note spans to those relevant to a diff
    _is_parashah_template — identify parashah-marker templates
"""

import difflib

from pydiff_mpp.mpp_param_access import _MISSING, _get_param

_PARASHAH_NAMES = {"סס", "ססס", "פפ", "פפפ"}


def _is_parashah_template(name):
    """Check if template is a parashah marker (רN, סס, ססס, פפ, פפפ)."""
    if name in _PARASHAH_NAMES:
        return True
    return len(name) >= 2 and name[0] == "ר" and name[1:].isdigit()


def _is_std_kq_template(name):
    """Check if template is a standard ketiv/qere body-text variant."""
    if name in ('קו"כ', 'כו"ק'):
        return True
    return name.startswith('מ:קו"כ') or name.startswith('מ:כו"ק')


def _is_trivial_kq_template(name):
    """Check if template is a trivial ketiv/qere whose body text is param 1."""
    return name == 'קו"כ-אם'


def _is_qere_velo_ketiv_template(name):
    return name == "קרי ולא כתיב"


def _is_ketiv_velo_qere_template(name):
    return name == "כתיב ולא קרי"


def flatten_ep(ep):
    """Flatten an EP column array to a body text string.

    Includes plain text and the body-text contribution of templates
    (e.g. נוסח param 1, קו"כ params, מ:קמץ dalet variant).
    Excludes נוסח param 2 (manuscript annotations).
    """
    return "".join(_flatten_element(el) for el in ep)


def _flatten_element(el):
    if isinstance(el, str):
        return el
    if isinstance(el, dict):
        return _flatten_template(el)
    if isinstance(el, list):
        return "".join(_flatten_element(x) for x in el)
    return ""


def _flatten_template(tmpl):
    name = tmpl["tmpl_name"]
    if _is_parashah_template(name):
        return " "
    if name == "נוסח":
        p1 = _get_param(tmpl, "1")
        return _flatten_element(p1) if p1 is not _MISSING else ""
    if _is_std_kq_template(name) or _is_qere_velo_ketiv_template(name):
        p2 = _get_param(tmpl, "2")
        return _flatten_element(p2) if p2 is not _MISSING else ""
    if _is_trivial_kq_template(name):
        p1 = _get_param(tmpl, "1")
        return _flatten_element(p1) if p1 is not _MISSING else ""
    if _is_ketiv_velo_qere_template(name):
        return ""
    if name == "מ:קמץ":
        pd = _get_param(tmpl, "ד")
        return _flatten_element(pd) if pd is not _MISSING else ""
    if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
        return "׀"
    if name == "מ:פסק":
        return "׀"
    if name == "מ:כפול":
        pk = _get_param(tmpl, "כפול")
        return _flatten_element(pk) if pk is not _MISSING else ""
    p1 = _get_param(tmpl, "1")
    if p1 is not _MISSING:
        return _flatten_element(p1)
    return ""


def _flatten_ep_with_nusach(ep):
    """Flatten EP column and track נוסח templates that have param 2."""
    parts = []
    notes = []
    for el in ep:
        _flatten_tracking(el, parts, notes)
    return "".join(parts), notes


def _flatten_tracking(obj, parts, notes):
    if isinstance(obj, str):
        parts.append(obj)
    elif isinstance(obj, dict):
        _flatten_template_tracking(obj, parts, notes)
    elif isinstance(obj, list):
        for item in obj:
            _flatten_tracking(item, parts, notes)


def _flatten_template_tracking(tmpl, parts, notes):
    name = tmpl["tmpl_name"]
    if _is_parashah_template(name):
        parts.append(" ")
        return
    if name == "נוסח":
        start = sum(len(p) for p in parts)
        p1 = _get_param(tmpl, "1")
        if p1 is not _MISSING:
            _flatten_tracking(p1, parts, notes)
        end = sum(len(p) for p in parts)
        p2 = _get_param(tmpl, "2")
        if p2 is not _MISSING:
            notes.append({"start": start, "end": end, "param2": p2})
        return
    if _is_std_kq_template(name) or _is_qere_velo_ketiv_template(name):
        p2 = _get_param(tmpl, "2")
        if p2 is not _MISSING:
            _flatten_tracking(p2, parts, notes)
        return
    if _is_trivial_kq_template(name):
        p1 = _get_param(tmpl, "1")
        if p1 is not _MISSING:
            _flatten_tracking(p1, parts, notes)
        return
    if _is_ketiv_velo_qere_template(name):
        return
    if name == "מ:קמץ":
        pd = _get_param(tmpl, "ד")
        if pd is not _MISSING:
            _flatten_tracking(pd, parts, notes)
        return
    if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
        parts.append("׀")
        return
    if name == "מ:פסק":
        parts.append("׀")
        return
    if name == "מ:כפול":
        pk = _get_param(tmpl, "כפול")
        if pk is not _MISSING:
            _flatten_tracking(pk, parts, notes)
        return
    p1 = _get_param(tmpl, "1")
    if p1 is not _MISSING:
        _flatten_tracking(p1, parts, notes)


def _changed_new_positions(old_text, new_text):
    """Return set of character positions in new_text that are changed/added."""
    sm = difflib.SequenceMatcher(None, old_text, new_text, autojunk=False)
    changed = set()
    for op, _i1, _i2, j1, j2 in sm.get_opcodes():
        if op in ("replace", "insert"):
            changed.update(range(j1, j2))
    return changed


def _find_relevant_nusach(old_text, new_text, notes, text_changed):
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
