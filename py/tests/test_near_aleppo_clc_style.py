"""Compare NAEE's borrowed k/q appearance with the authoritative CLC CSS.

NAEE owns the wrapper layout and vertical padding for two pointed readings.
CLC supplies the border, horizontal spacing, reading size and placeholder style.
"""

import re

from mb_cmn import paths


def _declarations(css, selector):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    matches = re.findall(re.escape(selector) + r"\s*\{([^}]+)\}", css)
    assert len(matches) == 1, f"Expected one rule for {selector!r}"
    declarations = {}
    for part in matches[0].split(";"):
        if part.strip():
            name, value = part.split(":", 1)
            assert name.strip() not in declarations
            declarations[name.strip()] = " ".join(value.split())
    assert declarations, f"Empty rule for {selector!r}"
    return declarations


def _horizontal_padding(value):
    """Left and right sides of a one- to four-value CSS padding shorthand."""
    sides = value.split()
    if len(sides) == 1:
        return sides[0], sides[0]
    if len(sides) in (2, 3):
        return sides[1], sides[1]
    assert len(sides) == 4, f"Unsupported padding shorthand: {value!r}"
    return sides[3], sides[1]


def test_naee_borrows_clc_box_size_and_placeholder_styles():
    root = paths.repo_root()
    clc = (root / "gh-pages/uxlc/style.css").read_text(encoding="utf-8")
    naee = (root / "py/near_aleppo/edition.css").read_text(encoding="utf-8")
    pairs = (
        ("span.clc-kq-box", "span.near-aleppo-kq-box"),
        ("ruby.clc-kq", "ruby.near-aleppo-kq"),
        ("ruby.clc-kq rt", "ruby.near-aleppo-kq > rt"),
        ("ruby.clc-kq span.clc-kq-none", "ruby.near-aleppo-kq .near-aleppo-kq-none"),
    )
    for source, target in pairs:
        expected = _declarations(clc, source)
        actual = _declarations(naee, target)
        for name, value in expected.items():
            if source == "span.clc-kq-box":
                if name == "display":
                    continue  # The wrapper layout belongs to NAEE.
                if name == "padding":
                    assert _horizontal_padding(actual[name]) == _horizontal_padding(
                        value
                    )
                    continue
            assert actual.get(name) == value, (source, target, name, expected, actual)
