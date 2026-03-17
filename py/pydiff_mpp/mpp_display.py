"""
Paseq and ketiv/qere display transformations for MPP diff reports.

Converts raw MPP text into display-ready text with sentinel markers,
then post-processes HTML to replace sentinels with ruby annotations.

Exports:
    display_text               — apply paseq + gray maqaf + K/Q sentinels to raw text
    normalize_paseq_spacing    — fix spacing around paseq sentinels
    postprocess_gray_maqaf_html — replace gray maqaf sentinels with styled HTML
    postprocess_paseq_html     — replace paseq sentinels with ruby HTML
    postprocess_kq_html        — replace K/Q sentinels with ruby HTML
"""

import re

from pydiff_mpp.mpp_extract import (
    _MISSING,
    _get_param,
    _is_parashah_template,
)

# ── Paseq display (ruby annotations for legarmeih / narpas) ──

_LEG_SENTINEL = "\ufdd0"
_NAR_SENTINEL = "\ufdd1"
_LEG_RUBY = '<ruby class="paseq-ruby">\u05c0<rt>\u05dc</rt></ruby>'
_NAR_RUBY = '<ruby class="paseq-ruby">\u05c0<rt>\u05e4</rt></ruby>'

# ── Gray maqaf display ──

_GRAY_MAQ_SENTINEL = "\ufdd2"
_GRAY_MAQ_HTML = '<span class="gray-maqaf">\u05be</span>'

# ── K/Q display (ruby annotations for ketiv/qere) ──

_KQ_K_START = "\ue010"
_KQ_K_END = "\ue011"
_KQ_Q_START = "\ue012"
_KQ_Q_END = "\ue013"


def _collect_paseq_types(obj, types):
    """Recursively collect paseq template types, mirroring flatten_ep."""
    if isinstance(obj, str):
        return
    if isinstance(obj, dict):
        name = obj["tmpl_name"]
        if _is_parashah_template(name):
            return
        if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
            types.append("legarmeih")
            return
        if name == "מ:פסק":
            types.append("narpas")
            return
        if name == "נוסח":
            p1 = _get_param(obj, "1")
            if p1 is not _MISSING:
                _collect_paseq_types(p1, types)
            return
        if name in ('קו"כ', 'כו"ק'):
            p1 = _get_param(obj, "1")
            if p1 is not _MISSING:
                _collect_paseq_types(p1, types)
            p2 = _get_param(obj, "2")
            if p2 is not _MISSING:
                _collect_paseq_types(p2, types)
            return
        if name == "מ:קמץ":
            pd = _get_param(obj, "ד")
            if pd is not _MISSING:
                _collect_paseq_types(pd, types)
            return
        if name == "מ:כפול":
            pk = _get_param(obj, "כפול")
            if pk is not _MISSING:
                _collect_paseq_types(pk, types)
            return
        p1 = _get_param(obj, "1")
        if p1 is not _MISSING:
            _collect_paseq_types(p1, types)
        return
    if isinstance(obj, list):
        for item in obj:
            _collect_paseq_types(item, types)


def _collect_gray_maqaf_positions(ep):
    """Walk EP structure and return positions where gray maqaf should be inserted."""
    positions = set()
    pos = [0]
    for el in ep:
        _gray_maqaf_walk(el, pos, positions)
    return positions


def _gray_maqaf_walk(obj, pos, positions):
    if isinstance(obj, str):
        pos[0] += len(obj)
    elif isinstance(obj, dict):
        _gray_maqaf_walk_template(obj, pos, positions)
    elif isinstance(obj, list):
        for item in obj:
            _gray_maqaf_walk(item, pos, positions)


def _gray_maqaf_walk_template(tmpl, pos, positions):
    name = tmpl["tmpl_name"]
    if name == "מ:מקף אפור":
        positions.add(pos[0])
        return
    if _is_parashah_template(name):
        pos[0] += 1
        return
    if name == "נוסח":
        p1 = _get_param(tmpl, "1")
        if p1 is not _MISSING:
            _gray_maqaf_walk(p1, pos, positions)
        return
    if name in ('קו"כ', 'כו"ק'):
        p1 = _get_param(tmpl, "1")
        if p1 is not _MISSING:
            _gray_maqaf_walk(p1, pos, positions)
        p2 = _get_param(tmpl, "2")
        if p2 is not _MISSING:
            _gray_maqaf_walk(p2, pos, positions)
        return
    if name == "מ:קמץ":
        pd = _get_param(tmpl, "ד")
        if pd is not _MISSING:
            _gray_maqaf_walk(pd, pos, positions)
        return
    if name in ("מ:לגרמיה-2", "מ:לגרמיה", "מ:פסק"):
        pos[0] += 1
        return
    if name == "מ:כפול":
        pk = _get_param(tmpl, "כפול")
        if pk is not _MISSING:
            _gray_maqaf_walk(pk, pos, positions)
        return
    p1 = _get_param(tmpl, "1")
    if p1 is not _MISSING:
        _gray_maqaf_walk(p1, pos, positions)


def _collect_kq_positions(ep):
    """Walk EP structure and return k/q boundary positions in flattened text."""
    positions = []
    pos = [0]
    for el in ep:
        _kq_position_walk(el, pos, positions)
    return positions


def _kq_position_walk(obj, pos, positions):
    if isinstance(obj, str):
        pos[0] += len(obj)
    elif isinstance(obj, dict):
        _kq_position_walk_template(obj, pos, positions)
    elif isinstance(obj, list):
        for item in obj:
            _kq_position_walk(item, pos, positions)


def _kq_position_walk_template(tmpl, pos, positions):
    name = tmpl["tmpl_name"]
    if _is_parashah_template(name):
        pos[0] += 1
        return
    if name == "נוסח":
        p1 = _get_param(tmpl, "1")
        if p1 is not _MISSING:
            _kq_position_walk(p1, pos, positions)
        return
    if name in ('קו"כ', 'כו"ק'):
        p1 = _get_param(tmpl, "1")
        p1_start = pos[0]
        if p1 is not _MISSING:
            _kq_position_walk(p1, pos, positions)
        p1_end = pos[0]
        p2 = _get_param(tmpl, "2")
        p2_start = pos[0]
        if p2 is not _MISSING:
            _kq_position_walk(p2, pos, positions)
        p2_end = pos[0]
        if name == 'כו"ק':
            k_start, k_end = p1_start, p1_end
            q_start, q_end = p2_start, p2_end
        else:
            q_start, q_end = p1_start, p1_end
            k_start, k_end = p2_start, p2_end
        positions.append(
            {
                "k_start": k_start,
                "k_end": k_end,
                "q_start": q_start,
                "q_end": q_end,
            }
        )
        return
    if name == "מ:קמץ":
        pd = _get_param(tmpl, "ד")
        if pd is not _MISSING:
            _kq_position_walk(pd, pos, positions)
        return
    if name in ("מ:לגרמיה-2", "מ:לגרמיה", "מ:פסק"):
        pos[0] += 1
        return
    if name == "מ:כפול":
        pk = _get_param(tmpl, "כפול")
        if pk is not _MISSING:
            _kq_position_walk(pk, pos, positions)
        return
    p1 = _get_param(tmpl, "1")
    if p1 is not _MISSING:
        _kq_position_walk(p1, pos, positions)


def display_text(text, ep):
    """Replace U+05C0 with paseq sentinels, insert gray maqaf sentinels,
    and wrap k/q parts with sentinels."""
    paseq_types = []
    for el in ep:
        _collect_paseq_types(el, paseq_types)
    kq_positions = _collect_kq_positions(ep)
    gray_maqaf_positions = _collect_gray_maqaf_positions(ep)
    # Build insertion maps: position -> sentinels to insert
    kq_before = {}  # insert before char at this position
    kq_after = {}  # insert after last char before this position
    for kq in kq_positions:
        kq_before.setdefault(kq["k_start"], []).append(_KQ_K_START)
        kq_after.setdefault(kq["k_end"], []).append(_KQ_K_END)
        kq_before.setdefault(kq["q_start"], []).append(_KQ_Q_START)
        kq_after.setdefault(kq["q_end"], []).append(_KQ_Q_END)
    result = []
    paseq_idx = 0
    for i, ch in enumerate(text):
        if i in kq_after:
            result.extend(kq_after[i])
        if i in kq_before:
            result.extend(kq_before[i])
        if i in gray_maqaf_positions:
            result.append(_GRAY_MAQ_SENTINEL)
        if ch == "\u05c0":
            result.append(
                _LEG_SENTINEL
                if paseq_types[paseq_idx] == "legarmeih"
                else _NAR_SENTINEL
            )
            paseq_idx += 1
        else:
            result.append(ch)
    end = len(text)
    if end in kq_after:
        result.extend(kq_after[end])
    return "".join(result)


def normalize_paseq_spacing(text):
    """Normalize spacing around paseq sentinels for display.

    Legarmeih: tight against preceding word, regular space after.
    Narpas:    non-breaking space before, regular space after.
    """
    text = re.sub(r" ?" + _LEG_SENTINEL + r" ?", _LEG_SENTINEL + " ", text)
    text = re.sub(r" ?" + _NAR_SENTINEL + r" ?", "\u00a0" + _NAR_SENTINEL + " ", text)
    return text


def postprocess_gray_maqaf_html(html_str):
    """Replace gray maqaf sentinels with styled HTML."""
    return html_str.replace(_GRAY_MAQ_SENTINEL, _GRAY_MAQ_HTML)


def postprocess_paseq_html(html_str):
    """Replace paseq sentinels with ruby HTML."""
    return html_str.replace(_LEG_SENTINEL, _LEG_RUBY).replace(_NAR_SENTINEL, _NAR_RUBY)


def _kq_ruby_html(k_content, q_content):
    """Build ruby HTML with qere as base text and ketiv as annotation."""
    return (
        '<ruby class="kq-pair">'
        f'<span class="kq-q">{q_content}</span>'
        "<rp>(</rp>"
        f'<rt><span class="kq-k">{k_content}</span></rt>'
        "<rp>)</rp>"
        "</ruby>"
    )


def postprocess_kq_html(html_str):
    """Replace k/q sentinel pairs with ruby HTML."""
    # Ketiv-first pattern (כו"ק)
    html_str = re.sub(
        re.escape(_KQ_K_START)
        + r"(.*?)"
        + re.escape(_KQ_K_END)
        + re.escape(_KQ_Q_START)
        + r"(.*?)"
        + re.escape(_KQ_Q_END),
        lambda m: _kq_ruby_html(m.group(1), m.group(2)),
        html_str,
    )
    # Qere-first pattern (קו"כ)
    html_str = re.sub(
        re.escape(_KQ_Q_START)
        + r"(.*?)"
        + re.escape(_KQ_Q_END)
        + re.escape(_KQ_K_START)
        + r"(.*?)"
        + re.escape(_KQ_K_END),
        lambda m: _kq_ruby_html(m.group(2), m.group(1)),
        html_str,
    )
    # Strip any remaining stray sentinels
    for s in (_KQ_K_START, _KQ_K_END, _KQ_Q_START, _KQ_Q_END):
        html_str = html_str.replace(s, "")
    return html_str
