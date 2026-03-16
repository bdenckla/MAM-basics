"""Render נוסח param 2 (manuscript annotations) as HTML.

Ported from mgketer's mpp_nusach module, adapted for the MAM-basics
diff pipeline.  Handles template markup inside note bodies and wraps
pointed Hebrew (vocalized/cantillated text) in spans for CSS sizing.

Exports:
    nusach_body_to_html  — convert a param-2 value to displayable HTML
"""

import re

from pydiff_mpp.mpp_extract import _get_params

# ── Pointed-Hebrew detection ──────────────────────────────────────

_DIAC = "\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7"
_HEB_CLUSTER_RE = re.compile(rf"[\u05D0-\u05EA{_DIAC}\u05BE\-]+")
_HAS_DIAC_RE = re.compile(rf"[{_DIAC}]")
_TAG_SPLIT_RE = re.compile(r"(<[^>]+>)")

_SLH_CSS_CLASS = {
    "מ:אות-ג": "letter-large",
    "מ:אות-ק": "letter-small",
    "מ:אות תלויה": "letter-hung",
}


# ── Public API ────────────────────────────────────────────────────


def nusach_body_to_html(body):
    """Convert a נוסח note body (param 2) to displayable HTML.

    The *body* value can be a plain string, a list of strings and
    template dicts, or a nested combination.  Template handling:

      ``{ש}``       → ``<br>``
      ``{מודגש}``   → ``<strong>…</strong>``
      others        → param text rendered inline

    Pointed Hebrew spans are wrapped in ``<span class="pointed-heb">``
    so CSS can size them for legibility.
    """
    raw = _to_raw_html(body)
    return _wrap_pointed_hebrew(raw)


# ── Internal helpers ──────────────────────────────────────────────


def _esc(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _to_raw_html(obj):
    if obj is None:
        return ""
    if isinstance(obj, str):
        return _esc(obj)
    if isinstance(obj, dict):
        return _render_template(obj)
    if isinstance(obj, list):
        return "".join(_to_raw_html(item) for item in obj)
    return _esc(str(obj))


def _render_template(tmpl):
    name = tmpl.get("tmpl_name", "")
    params = _get_params(tmpl)
    if name == "ש":
        return "<br>"
    if name == "מודגש":
        inner = _to_raw_html(params.get("1", ""))
        return f"<strong>{inner}</strong>"
    if name == "מ:קישור פנימי בהערה":
        if "1" in params:
            return _to_raw_html(params["1"])
        return ""
    if name == "מ:אות-מיוחדת-במילה":
        if "1" in params:
            return _to_raw_html(params["1"])
        return ""
    if name in _SLH_CSS_CLASS:
        inner = _to_raw_html(params.get("1", ""))
        return f'<span class="{_SLH_CSS_CLASS[name]}">{inner}</span>'
    # Unknown template: render param "1" or all params
    if "1" in params:
        return _to_raw_html(params["1"])
    return ""


# ── Pointed-Hebrew wrapping ──────────────────────────────────────


def _wrap_pointed_hebrew(html_str):
    """Post-process HTML to wrap pointed-Hebrew spans with a class."""
    segments = _TAG_SPLIT_RE.split(html_str)
    return "".join(
        seg if seg.startswith("<") else _wrap_pointed_in_text(seg) for seg in segments
    )


def _wrap_pointed_in_text(text):
    """Wrap contiguous pointed-Hebrew runs in plain text."""
    clusters = list(_HEB_CLUSTER_RE.finditer(text))
    if not clusters:
        return text
    pointed = [bool(_HAS_DIAC_RE.search(m.group())) for m in clusters]
    # Group consecutive pointed clusters separated only by whitespace
    groups = []
    i = 0
    while i < len(clusters):
        if not pointed[i]:
            i += 1
            continue
        grp_start = clusters[i].start()
        grp_end = clusters[i].end()
        j = i + 1
        while j < len(clusters) and pointed[j]:
            between = text[grp_end : clusters[j].start()]
            if between.strip() == "":
                grp_end = clusters[j].end()
                j += 1
            else:
                break
        groups.append((grp_start, grp_end))
        i = j
    if not groups:
        return text
    parts = []
    prev = 0
    for start, end in groups:
        parts.append(text[prev:start])
        parts.append(f'<span class="pointed-heb">{text[start:end]}</span>')
        prev = end
    parts.append(text[prev:])
    return "".join(parts)
