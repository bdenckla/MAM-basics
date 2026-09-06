"""Generate MAM-simple/doc/versification-and-cantillation.html.

Companion generator to versification_differences/generate_doc.py; both write into
MAM-simple/ and are driven from main_mam_simple.py's doc step.
This one emits a standalone HTML page (served via GitHub Pages), whereas the
companion still emits Markdown (rendered on github.com).
"""

from pathlib import Path

from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import bib_locales as tbn
from versification_and_cantillation import doc

# Published as a standalone page under gh-pages/MAM-simple/. So the live URL is
# https://bdenckla.github.io/MAM-basics/MAM-simple/versification-and-cantillation.html.
_OUTPUT_PATH = (
    paths.repo_root()
    / "gh-pages"
    / "MAM-simple"
    / "versification-and-cantillation.html"
)
# The stylesheet is linked (not inlined), so it is a second deployed file sitting
# next to the HTML in gh-pages/. Its source of truth is a hand-authored .css beside
# doc.py, which we copy verbatim so the two stay identical.
#
# Deliberately unlike the repo's other CSS: styles_authored.py / styles_mam_*.py /
# mpplus_assets.py all keep their CSS as a Python *string* and write it out (with a
# "DO NOT EDIT - edit the .py" banner). Here the CSS is static (no interpolation) and
# we prefer a real .css source for editor/linter support, so the source *is* a .css
# file. So deploying it is a verbatim file-copy, not a string-emit like the
# make_css_file_* helpers — as is the woff2 copy just below.
_CSS_SOURCE_PATH = Path(doc.__file__).with_name(doc.CSS_FILENAME)
_CSS_OUTPUT_PATH = _OUTPUT_PATH.with_name(doc.CSS_FILENAME)
# A third deployed file: the Hebrew font the CSS's @font-face names (issue #203, C1). The page's
# payload is boundary words stripped to letters + accents, so it needs a font that renders those
# accents — hence a self-hosted woff2, as our other Pages-served pages do, rather than a
# system-font stack most visitors would not resolve. Deployed at the product path the CSS's
# url("woff2/Taamey_D.woff2") resolves to; the former MAM-simple Pages tree had no binary asset before this.
#
# Copied verbatim from the in-repo font, deployed by the same read-compare-write shape the .css
# above uses (just bytes-wise). mpplus_assets._copy_woff2 is the nearest precedent but a poor
# model: its source path is destination-relative and would look in a nonexistent MAM-simple/misc/,
# it compares only st_size, and it skips silently when the source is missing.
_WOFF2_SOURCE_PATH = paths.repo_root() / "doc" / "woff2" / "Taamey_D.woff2"
_WOFF2_OUTPUT_PATH = _OUTPUT_PATH.parent / "woff2" / _WOFF2_SOURCE_PATH.name

# The doc quotes Exodus and Numbers in the body, and Deuteronomy in the appendix (both
# dual-cantillation Decalogue books; Numbers 25/26 is the non-Decalogue case).
_SOURCE_BK39IDS = (tbn.BK_EXODUS, tbn.BK_NUMBERS, tbn.BK_DEUTER)


def render_full_html():
    books_mpu = plus.read_parsed_plus_bk39s(_SOURCE_BK39IDS, paths.mam_parsed_path())
    return doc.render_full_html(books_mpu)


def _css_source_text() -> str:
    return _CSS_SOURCE_PATH.read_text(encoding="utf-8")


def _woff2_source_bytes() -> bytes:
    # Unlike mpplus_assets._copy_woff2, which returns quietly when the font is absent: here a
    # missing source must fail loudly. Swallowing it would let check_output_matches() report
    # "up to date" for a deployed page whose @font-face points at a file we never wrote.
    return _WOFF2_SOURCE_PATH.read_bytes()


def output_path():
    return _OUTPUT_PATH


def check_output_matches() -> bool:
    # Assign each, then combine — `return a and b and c` would short-circuit past the later
    # checks, silently exempting the CSS and the font from the up-to-date test.
    html_matches = _matches(_OUTPUT_PATH, render_full_html())
    css_matches = _matches(_CSS_OUTPUT_PATH, _css_source_text())
    woff2_matches = _matches_bytes(_WOFF2_OUTPUT_PATH, _woff2_source_bytes())
    return html_matches and css_matches and woff2_matches


def write_output_if_changed() -> bool:
    # Likewise: assign each write, then combine, so `or` cannot skip a later one.
    html_changed = _write_if_changed(_OUTPUT_PATH, render_full_html())
    css_changed = _write_if_changed(_CSS_OUTPUT_PATH, _css_source_text())
    woff2_changed = _write_bytes_if_changed(_WOFF2_OUTPUT_PATH, _woff2_source_bytes())
    return html_changed or css_changed or woff2_changed


def _matches(path, expected: str) -> bool:
    return path.exists() and path.read_text(encoding="utf-8") == expected


def _matches_bytes(path, expected: bytes) -> bool:
    # Compares bytes, not st_size as mpplus_assets._copy_woff2 does: a same-size but different
    # font would read as up to date.
    return path.exists() and path.read_bytes() == expected


def _write_if_changed(path, text: str) -> bool:
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == text:
        return False
    # MAM-simple's line-ending policy is LF (.gitattributes eol=lf); write LF
    # directly so the Windows working tree matches and doesn't churn.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")
    return True


def _write_bytes_if_changed(path, data: bytes) -> bool:
    # No newline= counterpart to _write_if_changed's: that is the text files' LF policy, and a
    # byte copy is exempt from it (MAM-simple's .gitattributes marks *.woff2 binary).
    if path.exists() and path.read_bytes() == data:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return True
