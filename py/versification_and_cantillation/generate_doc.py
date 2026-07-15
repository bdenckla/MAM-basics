"""Generate MAM-simple/doc/versification-and-cantillation.html.

Companion generator to versification_differences/generate_doc.py; both write into
the MAM-simple sibling repo and are driven from main_mam_simple.py's doc step.
This one emits a standalone HTML page (served via GitHub Pages), whereas the
companion still emits Markdown (rendered on github.com).
"""

from pathlib import Path

from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import bib_locales as tbn
from versification_and_cantillation import doc

# Published as a standalone page under MAM-simple's gh-pages/ dir, which GitHub
# Pages serves at the repo root (see MAM-simple/.github/workflows/static.yml:
# path: gh-pages). So the live URL is
# https://bdenckla.github.io/MAM-simple/versification-and-cantillation.html.
_OUTPUT_PATH = (
    paths.sibling_repo("MAM-simple")
    / "gh-pages"
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
# file. The verbatim file-copy mirrors mpplus_assets._copy_woff2 (which copy2's the
# woff2 font), not the string-emitting make_css_file_* helpers.
_CSS_SOURCE_PATH = Path(doc.__file__).with_name(doc.CSS_FILENAME)
_CSS_OUTPUT_PATH = _OUTPUT_PATH.with_name(doc.CSS_FILENAME)

# The doc quotes Exodus and Numbers in the body, and Deuteronomy in the appendix (both
# dual-cantillation Decalogue books; Numbers 25/26 is the non-Decalogue case).
_SOURCE_BK39IDS = (tbn.BK_EXODUS, tbn.BK_NUMBERS, tbn.BK_DEUTER)


def render_full_html():
    books_mpu = plus.read_parsed_plus_bk39s(_SOURCE_BK39IDS)
    return doc.render_full_html(books_mpu)


def _css_source_text() -> str:
    return _CSS_SOURCE_PATH.read_text(encoding="utf-8")


def output_path():
    return _OUTPUT_PATH


def check_output_matches() -> bool:
    html_matches = _matches(_OUTPUT_PATH, render_full_html())
    css_matches = _matches(_CSS_OUTPUT_PATH, _css_source_text())
    return html_matches and css_matches


def write_output_if_changed() -> bool:
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
