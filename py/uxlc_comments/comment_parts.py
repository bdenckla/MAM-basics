"""The two markers a comment paragraph may hold besides plain text.

A comment paragraph written as a list mixes plain strings, which the renderer
escapes, with ``Raw`` parts, which it emits as HTML. ``link`` is the only
producer of a ``Raw`` part that hand-authored commentary should normally need.
"""

from __future__ import annotations

from dataclasses import dataclass

from py_render.rt_html_utils import external_link_html


@dataclass(frozen=True)
class Raw:
    """HTML to emit as-is inside a comment paragraph."""

    html: str


def raw(html: str) -> Raw:
    return Raw(html)


def link(label: str, href: str) -> Raw:
    return Raw(external_link_html(href=href, label=label))
