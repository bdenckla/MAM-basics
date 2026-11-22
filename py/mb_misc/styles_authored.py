"""Deploy the "authored" docs stylesheet, and the script of their side-by-side pages.

The CSS is static (no interpolation), so its source of truth is a real .css file
beside this module (styles_authored.css), not a Python string. make_css_file_for_authored
copies it verbatim to the destination. (Unlike the repo's other styles_*.py, which still
keep their CSS as Python strings; the versification-and-cantillation doc uses this same
real-.css approach.)

The side-by-side pages of the Introduction to MAM, which author.he_en_gen_html_file
writes, also load a script, the view control's, whose source of truth is the real .js
file beside this module, HE_EN_VIEW_JS. make_js_file_for_he_en_view copies it verbatim,
under that name, into the folder of the pages and of their style.css.
"""

from pathlib import Path

_CSS_SOURCE_PATH = Path(__file__).with_name("styles_authored.css")
HE_EN_VIEW_JS = "he_en_view.js"
_JS_SOURCE_PATH = Path(__file__).with_name(HE_EN_VIEW_JS)


def make_css_file_for_authored(out_path):
    _copy_verbatim(_CSS_SOURCE_PATH, out_path)


def make_js_file_for_he_en_view(out_path):
    _copy_verbatim(_JS_SOURCE_PATH, out_path)


def _copy_verbatim(source_path, out_path):
    text = source_path.read_text(encoding="utf-8")
    # Force LF: the deployed copies are LF, and a plain text-mode write would emit
    # CRLF on Windows and churn them.
    with open(out_path, "w", encoding="utf-8", newline="") as out_fp:
        out_fp.write(text)
