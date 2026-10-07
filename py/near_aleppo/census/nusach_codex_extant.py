"""Classify coverage of the Aleppo Codex for MAM's cited reading clauses.

The public aleppo/ index has inclusive range endpoints and leaves spanning book
boundaries. A book absent from the index has no surviving leaf. Bang-qualified
source entries remain source statements; the marker does not change coverage.
"""

import json
import sys

from near_aleppo.census import census_paths

sys.stdout.reconfigure(encoding="utf-8")

IDX = census_paths.aleppo_dir() / "index-flat-annotated.json"

# The index spells the books its own way.
IDX_NAME = {
    "Deuter": "Deut",
    "Joshua": "Josh",
    "Judges": "Judg",
    "1Samuel": "1 Sam",
    "2Samuel": "2 Sam",
    "1Kings": "1 Kgs",
    "2Kings": "2 Kgs",
    "Isaiah": "Isa",
    "Jeremiah": "Jer",
    "Ezekiel": "Ezek",
    "Hosea": "Hos",
    "Joel": "Joel",
    "Amos": "Amos",
    "Micah": "Mic",
    "Nahum": "Nah",
    "Habakkuk": "Hab",
    "Tsefaniah": "Zeph",
    "Zechariah": "Zech",
    "Malachi": "Mal",
    "Psalms": "Ps",
    "Proverbs": "Prov",
    "Job": "Job",
    "Song of Songs": "Song",
    "Ruth": "Ruth",
    "1Chronicles": "1 Chron",
    "2Chronicles": "2 Chron",
}

with open(IDX, encoding="utf-8") as handle:
    spans = [
        tuple(map(tuple, r["de_text_range"]))
        for r in json.load(handle)["body"]
        if r.get("de_text_range")
    ]


def extant(bk39, ch, vr):
    """Whether the codex has a leaf covering this verse."""
    name = IDX_NAME.get(bk39)
    if name is None:
        return False
    cv = (ch, vr)
    for (b0, c0, v0), (b1, c1, v1) in spans:
        if b0 == name and b1 == name:
            if (c0, v0) <= cv <= (c1, v1):
                return True
        elif b0 == name and cv >= (c0, v0):
            return True
        elif b1 == name and cv <= (c1, v1):
            return True
    return False
