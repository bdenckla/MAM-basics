"""Recompute, from the comparison TSVs, the row counts that the receipt quotes and that no
other output states, and write them to ``out/figures.txt``.

A row's kind is ``reading difference`` when it has any label outside the policy and set-aside
ones; otherwise it is the set of those labels' kinds, such as ``policy`` or ``order-only``.
The tiers of the research queue are counted in the queue's own headings.
"""

from collections import Counter

from hbce_psalms import hbce_paths
from hbce_psalms.candidates import is_candidate, load

_READING_DIFFERENCE = "reading difference"


def _kind(row) -> str:
    if is_candidate(row):
        return _READING_DIFFERENCE
    labels = [x.strip() for x in row["labels"].split(";") if x.strip()]
    return " + ".join(sorted({lab.split(":")[0] for lab in labels}))


def _by_count(counter: Counter) -> list[str]:
    ranked = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    return [f"  {n:5d}  {key}" for key, n in ranked]


def _comparison_lines(name: str, title: str) -> list[str]:
    rows = load(hbce_paths.out_dir() / name)
    kinds = Counter(_kind(r) for r in rows)
    policy = Counter(
        lab.strip()
        for r in rows
        for lab in r["labels"].split(";")
        if lab.strip().startswith("policy")
    )
    notes = Counter(r["docnote"] for r in rows if is_candidate(r))
    return [
        "",
        f"== {name}: {title} ==",
        f"differing rows: {len(rows)}",
        "rows by kind:",
        *_by_count(kinds),
        "reading differences by doc-note status:",
        *_by_count(notes),
        "policy labels (a row can have several):",
        *_by_count(policy),
    ]


def figures_lines() -> list[str]:
    """The figures, one line per element of the list."""
    out = hbce_paths.out_dir()
    lines = [
        "Row counts quoted by doc/hbce-psalms-vs-mam-2026-09-26.md, recomputed from the TSVs",
        "beside this file by py/main_hbce_psalms.py compare.",
    ]
    lines += _comparison_lines("compare_MA.tsv", "HBCE's Aleppo transcription vs MAM")
    lines += _comparison_lines(
        "compare_ML_range.tsv",
        "HBCE's Leningrad transcription vs MAM, Psalms 15:1-25:1",
    )
    lines += _comparison_lines(
        "compare_ML.tsv", "HBCE's Leningrad transcription vs MAM"
    )
    ux_rows = load(out / "candidates_with_ML_UXLC.tsv")
    verdicts = Counter(
        r["HBCE-Aleppo-vs-UXLC"] for r in ux_rows if r["docnote"] != "word-note"
    )
    lines += [
        "",
        "== candidates_with_ML_UXLC.tsv: Aleppo reading differences with no doc-note on"
        " the chanted word ==",
        *_by_count(verdicts),
    ]
    ml_rows = load(out / "candidates_with_ML.tsv")
    agrees = Counter(r["ML-agrees-with"] for r in ml_rows)
    lines += [
        "",
        "== candidates_with_ML.tsv: which side HBCE's Leningrad form agrees with, for every"
        " Aleppo reading difference ==",
        *_by_count(agrees),
    ]
    return lines


def write_figures() -> None:
    """Write ``out/figures.txt``."""
    text = "\n".join(figures_lines()) + "\n"
    path = hbce_paths.out_dir() / "figures.txt"
    path.write_text(text, encoding="utf-8", newline="\n")
