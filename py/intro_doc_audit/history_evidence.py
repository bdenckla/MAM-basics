"""Literal excerpt helpers for the separate, read-only revision-history cache."""

import json
import re
from pathlib import Path

from mb_cmn import hebrew_verse_numerals as hvn, uni_denorm
from intro_doc_audit.revision_history import revision_url


class CachedHistory:
    """Read retained API responses without fetching or touching the source corpus."""

    def __init__(self, path=".novc/proverbs-history-api"):
        self.path = Path(path)

    def metadata(self, key):
        # The first Proverbs investigation used distinct metadata/content keys.
        metadata_key = "proverbs" if key == "chapter" else key
        paths = sorted(self.path.glob(metadata_key + "-metadata-*.json"))
        if not paths:
            raise ValueError(f"No retained metadata for {key}")
        pages = [json.loads(p.read_bytes()) for p in paths]
        if "continue" in pages[-1]:
            raise ValueError(f"Incomplete metadata for {key}")
        return [r for p in pages for r in p["query"]["pages"][0]["revisions"]]

    def contents(self, key):
        records = self.selected(key)
        wanted = {r["revid"] for r in self.metadata(key)}
        if set(records) != wanted:
            raise ValueError(f"Chapter content coverage differs from metadata: {key}")
        return records

    def selected(self, key):
        """Read a named batch of selected revision responses without claiming completeness."""
        records = {
            r["revid"]: r
            for path in sorted(self.path.glob(key + "-content-*.json"))
            for page in json.loads(path.read_bytes())["query"]["pages"]
            for r in page.get("revisions", [])
        }
        if not records:
            raise ValueError(f"No retained selected contents for {key}")
        return records

    def revision(self, revision_id):
        value = json.loads((self.path / f"revision-{revision_id}.json").read_bytes())
        return value["query"]["pages"][0]["revisions"][0]


def letters(text):
    """Route a pointed expression; never use the key as source prose."""
    return "".join(c for c in text if "\u05d0" <= c <= "\u05ea")


def verse_excerpt(text, verse, include_heading=False):
    number = hvn.INT_TO_STR_DIC[verse]
    pattern = (
        r"<\u05e7\u05d8\u05e2 \u05d4\u05ea\u05d7\u05dc\u05d4="
        + number
        + r"/>(.*?)<\u05e7\u05d8\u05e2 \u05e1\u05d5\u05e3="
        + number
        + r"/>"
    )
    match = re.search(pattern, text, re.S)
    if not match:
        raise ValueError(f"Historical verse {verse} lacks its declared delimiters")
    start = match.start(1)
    if include_heading:
        marker = "<\u05e7\u05d8\u05e2 \u05d4\u05ea\u05d7\u05dc\u05d4=\u05e1\u05d9\u05de\u05df/>"
        start = text.rfind(marker, 0, match.start())
        if start < 0:
            raise ValueError(f"Historical verse {verse} lacks its heading delimiter")
    return {"line": text[:start].count("\n") + 1, "text": text[start : match.end(1)]}


def capture(revision, kind, verse=None, needles=(), include_heading=False):
    """Retain exact source strings; only selection uses comparison mark order."""
    text = revision["slots"]["main"]["content"]
    if verse is not None:
        excerpts = [verse_excerpt(text, verse, include_heading)]
    else:
        keys = [uni_denorm.give_std_mark_order(n) for n in needles]
        excerpts = [
            {"line": i, "text": line}
            for i, line in enumerate(text.splitlines(), 1)
            if any(key in uni_denorm.give_std_mark_order(line) for key in keys)
        ]
    return {
        "kind": kind,
        **{k: revision[k] for k in ("revid", "parentid", "timestamp", "comment")},
        "url": revision_url(revision["revid"]),
        "excerpts": excerpts,
    }
