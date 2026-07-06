"""Generate MAM-simple/doc/versification-and-cantillation.md.

Companion generator to versification_differences/generate_doc.py; both write into
the MAM-simple sibling repo and are driven from main_mam_simple.py's doc step.
"""

from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import bib_locales as tbn
from versification_and_cantillation import doc

_OUTPUT_PATH = (
    paths.sibling_repo("MAM-simple") / "doc" / "versification-and-cantillation.md"
)

# Only the dual-cantillation book (Exodus) and Numbers are quoted by the doc.
_SOURCE_BK39IDS = (tbn.BK_EXODUS, tbn.BK_NUMBERS)


def render_full_markdown():
    books_mpu = plus.read_parsed_plus_bk39s(_SOURCE_BK39IDS)
    return doc.render_full_markdown(books_mpu)


def output_path():
    return _OUTPUT_PATH


def check_output_matches() -> bool:
    expected = _OUTPUT_PATH.read_text(encoding="utf-8")
    actual = render_full_markdown()
    return actual == expected


def write_output_if_changed() -> bool:
    actual = render_full_markdown()
    current = _OUTPUT_PATH.read_text(encoding="utf-8") if _OUTPUT_PATH.exists() else None
    if current == actual:
        return False
    # MAM-simple's line-ending policy is LF (.gitattributes eol=lf); write LF
    # directly so the Windows working tree matches and doesn't churn.
    _OUTPUT_PATH.write_text(actual, encoding="utf-8", newline="")
    return True
