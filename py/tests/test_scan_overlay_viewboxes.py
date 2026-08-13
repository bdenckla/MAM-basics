"""Every highlight overlay's viewBox equals its scan's real pixel size.

WHY THIS IS WORTH A TEST.  ``my_html_for_img.Box(x, y, w, h)`` coordinates are in the
committed PNG's own pixel space, and ``scan_figure``'s ``viewbox=(w, h)`` declares what that
space is.  Nothing checked the two against each other, and every way of getting it wrong is
SILENT: the page still builds, ``pin_claims`` still agrees, the whole suite still passes, and
the only symptom is highlight rectangles sitting off the words they mean to mark -- a defect
visible solely to someone who opens the page and looks.  A rescanned or recropped image is
the obvious way in, since it changes the pixel space without touching the module that names
it, and the two literals live in different places in the page module.

THE SHAPE.  A mechanical lint over the tree -- one of the two kinds of test that have ever
found anything here (``doc/agent-planning-principles.md`` SS"Generated Outputs Are the
Tests") -- decidable from the committed artifacts alone: does this viewBox equal
``Image.open(scan).size``?

PAIRED OFF THE RENDERED HTML, NOT THE PAGE MODULES.  The pairing is what makes this
checkable, and the HTML is where it already exists as one object: a ``<div class=
"scan-annot">`` holds the ``<img src=...>`` and the ``<svg ... viewBox="0 0 W H">`` side by
side, so the src resolves against the page's own directory and no import, no AST walk and no
naming convention is involved.  In the modules the two are separate top-level names -- an
``_*_IMG`` filename constant and an ``_*_VIEWBOX`` tuple that some call sites do not bother
to name at all -- with nothing but adjacency in the call to connect them.  Checking the HTML
also checks the artifact that actually ships, which is the thing a reader's browser lays out.

SO IT DISCOVERS ITS OWN WORK.  Every ``gh-pages/**/*.html`` is parsed; a page that grows an
overlay later is covered without anyone registering it, and a page whose overlay is removed
drops out on its own.  As of this writing ten figures on the three accgram pages qualify.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_scan_overlay_viewboxes.py
"""

from __future__ import annotations

import pathlib
from html.parser import HTMLParser
from typing import NamedTuple

import pytest
from PIL import Image

from mb_cmn import paths

# The two class names ``my_html_for_img.annotated_img`` emits.  A rename there without a
# rename here NARROWS this lint to nothing rather than breaking it, which is why the
# emptiness guard below is not optional.
_WRAPPER_CLASS = "scan-annot"
_OVERLAY_CLASS = "scan-annot-overlay"


class Figure(NamedTuple):
    """One annotated figure, as the rendered page states it."""

    page: str  # the HTML file, relative to the repo root
    src: str  # the img's src, verbatim -- relative to the page's own directory
    img: pathlib.Path | None  # that src resolved; None only on the empty-tree sentinel
    viewbox: tuple[int, int] | None  # the SVG viewBox's (width, height)


class _OverlayParser(HTMLParser):
    """Collect (img src, viewBox) for each annotated-scan wrapper in one page.

    Nesting is tracked rather than assumed: the wrapper is found by class, and its inner
    ``<div>``s (should any appear) are counted so a later sibling figure is not folded into
    it.  ``HTMLParser`` lowercases attribute names, hence ``viewbox`` below for ``viewBox``.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found: list[tuple[str | None, str | None]] = []
        self._depth = 0  # 0 = outside a wrapper
        self._src: str | None = None

    @staticmethod
    def _classes(attrs: dict[str, str | None]) -> set[str]:
        return set((attrs.get("class") or "").split())

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "div":
            if self._depth:
                self._depth += 1
            elif _WRAPPER_CLASS in self._classes(attr):
                self._depth, self._src = 1, None
            return
        if not self._depth:
            return
        if tag == "img":
            self._src = attr.get("src")
        elif tag == "svg" and _OVERLAY_CLASS in self._classes(attr):
            self.found.append((self._src, attr.get("viewbox")))

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self._depth:
            self._depth -= 1


def _viewbox_size(viewbox: str | None) -> tuple[int, int] | None:
    """The (width, height) of a ``0 0 W H`` viewBox, or None if it is not that shape."""
    if viewbox is None:
        return None
    fields = viewbox.split()
    if len(fields) != 4 or not all(f.lstrip("-").isdigit() for f in fields):
        return None
    min_x, min_y, width, height = (int(f) for f in fields)
    # A scan's pixel space starts at its own top-left corner, which is the only origin
    # scan_figure can emit; anything else is not a viewBox this lint knows how to read.
    if (min_x, min_y) != (0, 0):
        return None
    return width, height


def _annotated_figures() -> list[Figure]:
    """Every annotated figure in the published tree, in page then document order."""
    gh_pages = paths.wlc_pages_dir()
    figures = []
    for page in sorted(gh_pages.rglob("*.html")):
        parser = _OverlayParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parser.close()
        for src, viewbox in parser.found:
            figures.append(
                Figure(
                    page=str(page.relative_to(paths.repo_root())).replace("\\", "/"),
                    src=src or "(no <img> in the wrapper)",
                    img=(page.parent / src).resolve() if src else None,
                    viewbox=_viewbox_size(viewbox),
                )
            )
    return figures


# An empty parameter set reports as a SKIP, and a skip in this suite is the SEMANTIC channel
# for "this page diverges from its strand" (``25a7800`` removed twenty-one guards that
# reported green having verified nothing).  A tree with no overlays left to check is not that
# finding, so the sentinel below turns it into a failure on the first assertion instead.
_NO_FIGURES = Figure(
    page="gh-pages",
    src="no annotated figure anywhere in the published tree",
    img=None,
    viewbox=None,
)


def _figure_id(figure: Figure) -> str:
    return f"{figure.page}::{pathlib.PurePosixPath(figure.src).name}"


@pytest.mark.parametrize(
    "figure", _annotated_figures() or [_NO_FIGURES], ids=_figure_id
)
def test_an_overlays_viewbox_is_its_scans_own_pixel_size(figure: Figure) -> None:
    """The overlay's coordinate space is the PNG's, so the two sizes must be equal.

    Unequal, the highlights are scaled by the ratio between them and land somewhere else
    entirely -- ``preserveAspectRatio="none"`` on the overlay means the mismatch stretches
    the rectangles rather than letterboxing them, so nothing about the rendering hints that
    the declared space is wrong.
    """
    assert figure.img is not None, f"{figure.page}: {figure.src}"
    assert figure.img.is_file(), f"{figure.page}: no scan committed at {figure.src}"
    assert figure.viewbox is not None, (
        f"{figure.page}: {figure.src} has no usable viewBox"
        ' -- expected the "0 0 W H" that scan_figure emits'
    )
    with Image.open(figure.img) as image:
        natural = image.size
    assert figure.viewbox == natural, (
        f"{figure.page}: {figure.src} is {natural[0]}x{natural[1]} pixels but its overlay"
        f" declares viewBox 0 0 {figure.viewbox[0]} {figure.viewbox[1]}."
        " Box coordinates are in the scan's own pixel space, so every highlight on this"
        " figure is misplaced. Fix the viewbox=(w, h) passed to scan_figure and regenerate"
        " the page."
    )
