"""Highlight Hebrew text clusters based on quirkrec settings."""

import re
from author_boj_util.author import span_color

__all__ = ["highlight", "color"]


def highlight(quirkrec, key):
    """Highlight Hebrew text clusters based on quirkrec settings.

    Args:
        quirkrec: enriched quirkrec dict.
        key: field name to highlight (e.g. "qr-lc-proposed" or
            "qr-consensus").
    """
    zbhls = _zb_highlights(quirkrec, key)  # zero-based highlights
    rk = quirkrec[key]
    clusters = re.findall(r"[א-ת־ ׀][^א-ת־ ׀]*", rk)
    jc = "".join(clusters)
    assert jc == rk
    out = [cl if i not in zbhls else color(cl, key) for i, cl in enumerate(clusters)]
    return out


def color(text, key):
    return span_color(text, _RK_COLOR[key])


_RK_COLOR = {
    "qr-lc-proposed": "red",
    "qr-ac-proposed": "red",
    "qr-consensus": "green",
}
_RK_HL_SPECIFIC = {
    "qr-lc-proposed": "qr-highlight-lc-proposed",
    "qr-ac-proposed": "qr-highlight-ac-proposed",
    "qr-consensus": "qr-highlight-consensus",
}


def _zb_highlights(quirkrec, key):
    hl_both = quirkrec.get("qr-highlight")
    hl_spec = quirkrec.get(_RK_HL_SPECIFIC[key])
    assert (hl_both is None) or (hl_spec is None)
    hl = hl_both or hl_spec
    if hl is None:
        return []
    if isinstance(hl, int):
        return [hl - 1]
    assert isinstance(hl, list)
    return [obi - 1 for obi in hl]
