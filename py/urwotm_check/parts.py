"""Static facts about the four source documents.

The doc ids are the published-to-web ("/pub") ids from the category "Undoing
and redoing the work of the Masoretes" in Ben's index of his own documents.
That index was ``document-index/README.md`` when these ids were recorded; it
is ``gh-pages/index.html`` here since 2026-08-31, written from
``py/author_site/site_data.py`` (doc/PLAN-unify-the-document-index.md). The
category kept its name through the move. Nothing fetches these ids any more
-- ``src/`` holds the frozen text -- but they are the only record of where
that text came from, so a later reader can reach the document a page was
ported from.
"""

from mb_cmn import paths

_GDOC_BASE = "https://docs.google.com/document/d/e"

PART_NUMS = (1, 2, 3, 4)

DOC_IDS = {
    1: (
        "2PACX-1vRb9FFplpKS8RcQ120gPt9-lz2zhpn5ttW3w6WBvhhGkVgahzwA"
        "_oSe2eHTr8ix9J9bVg04rh7-d-g6"
    ),
    2: (
        "2PACX-1vTJY9m46s2kIOgT9ccFeSgubRUj1aP-rxnF0IlOLeCy2pTJJmB5"
        "DpM7_D5z4ZiN1P5ev4z8tFHDVTyq"
    ),
    3: (
        "2PACX-1vR5AlviW3BrLRPXAcunRBgC7q4Qd7APZ_44voIg-EMrigP6zBP9"
        "gIG4Ae8wj_8l1UTQYjlzed7HchyY"
    ),
    4: (
        "2PACX-1vQpkwDpUZW1H_MeIpY4XPEWu8Zrdj0mdRVFGzZkSlePBGcnd3rq"
        "cTdqwYEQGxX-T7WI5KvxeInhUtQg"
    ),
}


def pub_url(part: int) -> str:
    return f"{_GDOC_BASE}/{DOC_IDS[part]}/pub"


def src_dir():
    """Tracked, hand-vendored normalized source text: the oracle."""
    return paths.repo_root() / "py" / "urwotm_check" / "src"


def src_path(part: int):
    """One part's frozen source words, one word per line."""
    return src_dir() / f"urwotm_{part}.gdoc.txt"
