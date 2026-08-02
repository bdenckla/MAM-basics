"""Map each dually-cantillated passage verse to its detangled per-strand readings,
for the goerwitz verse display (issue wlc-utils#36).

For a verse in one of the three dually-cantillated prose loci (Gen 35:22 and the two
Decalogues), the goerwitz report replaces the single combined WLC verse line with one
line per reading (e.g. taxton + elyon). The elyon reading groups several numbered
verses into one chanted verse, so a reading's span label can differ from the row's own
verse (e.g. the elyon line for dt 5:8 spans dt 5:7–10).

Each reading is a plain dict so the renderer stays dumb: ``strand`` / ``strand_label`` /
``display_label`` (labels), ``span_label``, ``words`` + ``word_bcvs`` (each word's
numbered verse), and -- for the group-by-reading dt 5:8 display -- ``status`` / ``tree``
(the reading's own parse, so the elyon's ERROR tree shows beside the taxton's) and
``word_leaf_counts`` (parse-tree leaves per word). The ``word_bcvs`` / ``word_leaf_counts``
let the renderer gray the words and tree columns that fall outside the row's own verse: an
elyon reading groups several numbered verses, so on the dt 5:8 row its 5:7 / 5:9 / 5:10
material is de-emphasized, spotlighting the 5:8 part where the ungrammatical lives.
``display_label`` carries the actual Unicode het (as opposed to the cant-strand
ASCII label, which spells it "x"), per the repo transliteration standard.

The heavy ``tree`` / ``word_leaf_counts`` fields are dropped from serialized research
artifacts via :func:`without_heavy_reading_fields` (issue wlc-utils#44): they live canonically in
``out/accgram/dual-cant/_dual_cant.json``, and the goerwitz HTML renders from the in-memory
rows, which keep them.
"""

from __future__ import annotations

import re
from pathlib import Path

from accgram import dual_cant_run

# The real het glyph, precomposed U+1E25, per the repo transliteration standard.
_XET_UNI = "ḥ"
_EN_DASH = chr(0x2013)
_BCV_RE = re.compile(r"(\d+):(\d+)$")

# The heavy parse tree + its per-word leaf counts live canonically in
# out/accgram/dual-cant/_dual_cant.json; drop them from serialized research artifacts
# (the goerwitz HTML renders from the in-memory rows, which keep these). Issue wlc-utils#44.
_HEAVY_READING_FIELDS = ("tree", "word_leaf_counts")


def without_heavy_reading_fields(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return copies of ``rows`` with each ``dual_cant_readings`` entry's heavy fields
    (``tree``, ``word_leaf_counts``) dropped. Non-mutating: callers' rows keep their trees.
    """
    out: list[dict[str, object]] = []
    for row in rows:
        readings = row.get("dual_cant_readings")
        if not isinstance(readings, list):
            out.append(row)
            continue
        new_row = dict(row)
        new_row["dual_cant_readings"] = [
            (
                {k: v for k, v in reading.items() if k not in _HEAVY_READING_FIELDS}
                if isinstance(reading, dict)
                else reading
            )
            for reading in readings
        ]
        out.append(new_row)
    return out


def load_readings_by_bcv(
    wlc422_kq_u_dir: Path, mam_simple_dir: Path
) -> dict[str, list[dict[str, object]]]:
    """Compact-bcv -> ordered per-strand readings (alef/taxton first, then bet/elyon)."""
    results = dual_cant_run.detangle_results(wlc422_kq_u_dir, mam_simple_dir)
    by_bcv: dict[str, list[dict[str, object]]] = {}
    for passage in results:
        for strand in passage.strands:
            for cv in strand.chanted_verses:
                span = list(cv.bcv_span)
                reading: dict[str, object] = {
                    "strand": cv.strand,  # "alef" / "bet" -- keys the per-strand notes
                    "strand_label": cv.strand_label,  # ASCII ("taxton" / "elyon" / ...)
                    "display_label": _display_label(strand.strand_label),
                    "span_label": _span_label(span),
                    "words": list(cv.words),
                    "word_bcvs": list(cv.word_bcvs),
                    "status": cv.status,  # clean / ungrammatical -> whether to show a parse tree
                    "tree": cv.tree,  # the parse-tree image (None when location-only)
                    "word_leaf_counts": list(
                        cv.word_leaf_counts
                    ),  # per-word leaf count, for graying
                }
                for bcv in _bcvs_in_span(span):
                    by_bcv.setdefault(bcv, []).append(reading)
    return by_bcv


def _display_label(strand_label: str) -> str:
    # The cant-strand ASCII label spells het as "x" (taxton); display uses the real glyph.
    return strand_label.replace("x", _XET_UNI)


def _parse_bcv(bcv: str) -> tuple[str, int, int]:
    match = _BCV_RE.search(bcv)
    if match is None:
        raise ValueError(f"Unparseable bcv: {bcv!r}")
    return bcv[: match.start()], int(match.group(1)), int(match.group(2))


def _span_label(span: list[str]) -> str:
    _, ch1, v1 = _parse_bcv(span[0])
    _, ch2, v2 = _parse_bcv(span[-1])
    if (ch1, v1) == (ch2, v2):
        return f"{ch1}:{v1}"
    if ch1 == ch2:
        return f"{ch1}:{v1}{_EN_DASH}{v2}"
    return f"{ch1}:{v1}{_EN_DASH}{ch2}:{v2}"


def _bcvs_in_span(span: list[str]) -> list[str]:
    bb, ch1, v1 = _parse_bcv(span[0])
    _, ch2, v2 = _parse_bcv(span[-1])
    # The dually-cantillated passages never cross a chapter boundary within a chanted
    # verse; if that ever changes, fall back to the endpoints rather than guess verse
    # counts per chapter.
    if ch1 != ch2:
        return [span[0], span[-1]]
    return [f"{bb}{ch1}:{v}" for v in range(v1, v2 + 1)]
