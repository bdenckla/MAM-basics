"""Render נוסח param 2 (manuscript annotations) as HTML.

Ported from a predecessor module in MAM-private (private annex section 4),
adapted for the MAM-basics
diff pipeline.  Handles template markup inside note bodies and wraps
pointed Hebrew (vocalized/cantillated text) in spans for CSS sizing.

Exports:
    docnote_body_to_html  — convert a param-2 value to displayable HTML
"""

import re

from mb_cmn import hebrew_punctuation as hpu
from mb_diff_mpu.mpplus_param_access import MISSING, get_param, param_items

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


def docnote_body_to_html(body):
    """Convert a נוסח note body (param 2) to displayable HTML.

    The *body* value can be a plain string, a list of strings and
    template dicts, or a nested combination.  Template handling:

      ``{ש}``       → ``<br>``
      ``{מודגש}``   → ``<strong>…</strong>``
      external note links → escaped links whose visible label is param 2
      internal note links → historical param-1 text pending a target decision
      marked letters and punctuation → their explicitly named content

    Every reachable note-body template is classified.  An unfamiliar template or
    parameter shape raises instead of guessing that parameter 1 is visible prose.

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
    raise TypeError(f"unclassified MAM note-body node: {type(obj).__name__}")


def _require_param_keys(tmpl, expected):
    name = tmpl.get("tmpl_name")
    actual = tuple(key for key, _value in param_items(tmpl))
    if set(actual) != set(expected) or len(actual) != len(expected):
        raise ValueError(
            f"unexpected parameters for MAM note-body template {name!r}: "
            f"expected {sorted(expected)!r}, got {list(actual)!r}"
        )


def _required_param(tmpl, key):
    value = get_param(tmpl, key)
    if value is MISSING:
        raise ValueError(
            f"missing parameter {key!r} in MAM note-body template "
            f"{tmpl.get('tmpl_name')!r}"
        )
    return value


def _plain_link_target(value, template_name):
    if isinstance(value, str):
        return value
    if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
        return value[0]
    raise ValueError(
        f"non-text link target in MAM note-body template {template_name!r}: {value!r}"
    )


def _render_template(tmpl):
    name = tmpl.get("tmpl_name")
    if not isinstance(name, str):
        raise ValueError(f"MAM note-body mapping lacks tmpl_name: {tmpl!r}")
    if name == "ש":
        _require_param_keys(tmpl, ())
        return "<br>"
    if name == "מודגש":
        _require_param_keys(tmpl, ("1",))
        inner = _to_raw_html(_required_param(tmpl, "1"))
        return f"<strong>{inner}</strong>"
    if name == "מ:קישור בהערה":
        _require_param_keys(tmpl, ("1", "2"))
        target = _plain_link_target(_required_param(tmpl, "1"), name)
        label = _to_raw_html(_required_param(tmpl, "2"))
        return f'<a href="{_esc(target)}">{label}</a>'
    if name == "מ:קישור פנימי בהערה":
        _require_param_keys(tmpl, ("1", "2"))
        # The internal-target contract is deferred in
        # doc/PLAN-deferred-template-projection-decisions.md.  Preserve the
        # behavior on main until then: display parameter 1 without emitting a
        # page-relative link whose target is known to be wrong.
        return _to_raw_html(_required_param(tmpl, "1"))
    if name == "מ:אות-מיוחדת-במילה":
        _require_param_keys(tmpl, ("1",))
        return _to_raw_html(_required_param(tmpl, "1"))
    if name in _SLH_CSS_CLASS:
        _require_param_keys(tmpl, ("1",))
        inner = _to_raw_html(_required_param(tmpl, "1"))
        return f'<span class="{_SLH_CSS_CLASS[name]}">{inner}</span>'
    if name in {"מ:לגרמיה-2", "מ:פסק"}:
        _require_param_keys(tmpl, ())
        return hpu.PASOLEG
    raise ValueError(f"unclassified MAM note-body template: {name!r}")


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
