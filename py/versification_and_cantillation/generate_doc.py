"""Generate gh-pages/MAM-simple/versification-and-cantillation.html.

Companion generator to versification_differences/generate_doc.py; both write
standalone HTML into gh-pages/MAM-simple/ and are driven from main_mam_simple.py's
doc step.
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
# The family extension is static CSS, copied verbatim. The page also links the
# hand-authored shared gh-pages/document.css without rewriting that base.
_CSS_SOURCE_PATH = Path(doc.__file__).with_name(doc.CSS_FILENAME)
_CSS_OUTPUT_PATH = _OUTPUT_PATH.with_name(doc.CSS_FILENAME)
# The CSS's @font-face names a self-hosted Hebrew font (issue #203, C1). The page's payload is
# boundary words stripped to letters + accents, so it needs a font that renders those accents,
# rather than a system-font stack most visitors would not resolve. Its url,
# "../woff2/Taamey_D.woff2", reaches the site's one copy of Taamey D,
# gh-pages/woff2/Taamey_D.woff2, which no generator writes; so this module deploys no font.

# The doc quotes Exodus and Numbers in the body, and Deuteronomy in the appendix (both
# dual-cantillation Decalogue books; Numbers 25/26 is the non-Decalogue case).
_SOURCE_BK39IDS = (tbn.BK_EXODUS, tbn.BK_NUMBERS, tbn.BK_DEUTER)


def render_full_html():
    books_mpu = plus.read_parsed_plus_bk39s(_SOURCE_BK39IDS, paths.mam_parsed_path())
    return doc.render_full_html(books_mpu)


def _css_source_text() -> str:
    return _CSS_SOURCE_PATH.read_text(encoding="utf-8")


def output_path():
    return _OUTPUT_PATH


def check_output_matches() -> bool:
    # Assign each, then combine — `return a and b` would short-circuit past the later
    # check, silently exempting the CSS from the up-to-date test.
    html_matches = _matches(_OUTPUT_PATH, render_full_html())
    css_matches = _matches(_CSS_OUTPUT_PATH, _css_source_text())
    return html_matches and css_matches


def write_output_if_changed() -> bool:
    # Likewise: assign each write, then combine, so `or` cannot skip a later one.
    html_changed = _write_if_changed(_OUTPUT_PATH, render_full_html())
    css_changed = _write_if_changed(_CSS_OUTPUT_PATH, _css_source_text())
    return html_changed or css_changed


def _matches(path, expected: str) -> bool:
    return path.exists() and path.read_text(encoding="utf-8") == expected


def _write_if_changed(path, text: str) -> bool:
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == text:
        return False
    # MAM-simple's line-ending policy is LF (.gitattributes eol=lf); write LF
    # directly so the Windows working tree matches and doesn't churn.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")
    return True
