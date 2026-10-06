"""Deploy the shared MAM-with-doc / OSIS / FOI / near-Aleppo stylesheet.

The CSS is static (no interpolation), so its source of truth is a real .css file
beside this module (styles_mam_with_doc.css), not a Python string.
make_css_file_for_mwd copies it verbatim to gh-pages/MAM-with-doc; the other
families link that shared deployment. The pinned MAM-mode differential also
compares its bytes. The versification-and-cantillation doc uses this same
real-.css approach.
"""

from pathlib import Path

_CSS_SOURCE_PATH = Path(__file__).with_name("styles_mam_with_doc.css")


def css_for_mwd():
    # The MAM-mode differential includes the canonical stylesheet's text.
    return _CSS_SOURCE_PATH.read_text(encoding="utf-8")


def make_css_file_for_mwd(out_path):
    css = css_for_mwd()
    # Force LF: the deployed copies are LF, and a plain text-mode write would emit
    # CRLF on Windows and churn them.
    with open(out_path, "w", encoding="utf-8", newline="") as out_fp:
        out_fp.write(css)
