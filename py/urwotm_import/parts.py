"""Static facts about the four source documents.

The doc ids are the published-to-web ("/pub") ids from
document-index/README.md, category "Undoing and redoing the work of the
Masoretes".
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

# Provisional titles, taken from document-index/README.md. The emitted
# modules take their titles from the documents themselves; these are only
# for report headings and for spotting a fetch that returned the wrong doc.
PROVISIONAL_TITLES = {
    1: "The tale of the qadma",
    2: "Saying the quiet part out loud",
    3: "Extra verses",
    4: "Atnaḥ hafukh",
}

# Raw source tag counts, confirmed against lxml. Phase 5's structural
# tripwire compares generated output against these.
#
# These are the counts of every tag in the document, including the ones
# nested inside Part 2's two tables -- the six table-cell <p> elements and
# the two <img> they hold. The plan's own table had the <li> column one
# high in all four parts; the numbers here are the observed ones.
EXPECTED_COUNTS = {
    # part: (p, li, table, img)
    1: (114, 26, 0, 8),
    2: (131, 27, 2, 20),
    3: (107, 14, 0, 14),
    4: (75, 27, 0, 10),
}


def pub_url(part: int) -> str:
    return f"{_GDOC_BASE}/{DOC_IDS[part]}/pub"


def cache_dir():
    return paths.repo_root() / ".novc" / "urwotm_cache"


def http_cache_dir():
    return cache_dir() / "http"


def snapshot_dir():
    """The pinned per-part HTML snapshots the whole importer reads from."""
    return cache_dir() / "snapshot"


def img_cache_dir():
    return cache_dir() / "img"


def report_dir():
    return cache_dir() / "reports"


def src_dir():
    """Tracked, hand-vendored normalized source text (the Phase 8 oracle)."""
    return paths.repo_root() / "py" / "urwotm_import" / "src"
