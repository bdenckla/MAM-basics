"""Reduce a comparison TSV to its reading differences, the candidate findings, grouped by
doc-note status; ``out/candidates_MA_full.txt`` is this report on ``out/compare_MA.tsv``.

``load`` and ``is_candidate`` also serve ``cross_check_ml``, ``uxlc_check``, ``research_queue``
and ``figures``.
"""

from collections import Counter, defaultdict
from pathlib import Path

from hbce_psalms import hbce_paths
from hbce_psalms.compare import NOISE_PREFIXES


def load(path: Path) -> list[dict]:
    """The rows of a TSV under ``out/``, each a dict keyed by the header."""
    rows = []
    with path.open(encoding="utf-8") as f:
        header = next(f).rstrip("\n").split("\t")
        for line in f:
            parts = line.rstrip("\n").split("\t")
            rows.append(dict(zip(header, parts)))
    return rows


def real_labels(row) -> list[str]:
    """A row's labels other than the policy and set-aside ones."""
    labels = [x.strip() for x in row["labels"].split(";")]
    return [lab for lab in labels if lab and not lab.startswith(NOISE_PREFIXES)]


def is_candidate(row) -> bool:
    """Whether a row is a reading difference: a candidate finding."""
    return bool(real_labels(row))


def report_lines(name: str, show_noted: bool) -> list[str]:
    """The report on one comparison TSV, one line per element of the list."""
    lines = []
    rows = load(hbce_paths.out_dir() / name)
    cands = [r for r in rows if is_candidate(r)]
    other_col = [k for k in rows[0] if k in ("Aleppo", "Leningrad")][0]
    lines.append(
        f"\n##### {name}: {len(rows)} differing rows, {len(cands)} candidate rows"
    )
    by_label = defaultdict(Counter)
    for r in cands:
        for lab in real_labels(r):
            by_label[lab][r["docnote"]] += 1
    lines.append("label -> docnote status counts:")
    for lab, cnt in sorted(by_label.items(), key=lambda kv: -sum(kv[1].values())):
        lines.append(f"  {sum(cnt.values()):4d}  {lab:45s} {dict(cnt)}")
    for status in ("none", "verse-note") + (("word-note",) if show_noted else ()):
        sel = [r for r in cands if r["docnote"] == status]
        lines.append(f"\n--- candidates with docnote={status}: {len(sel)} ---")
        for r in sel:
            intro = r["intro"] or "-"
            lines.append(
                f"{r['ref']:10s} MAM={r['MAM']:28s} HBCE={r[other_col]:28s}"
                f" | {r['labels']} | flags={r['orig|flags']} | intro={intro}"
            )
            if r["details"]:
                lines.append(f"{'':10s}   {r['details']}")
            if status != "none" and r["note_text"]:
                lines.append(f"{'':10s}   note: {r['note_text'][:300]}")
    return lines


def write_candidates_ma_full() -> None:
    """Write ``out/candidates_MA_full.txt``: the Aleppo report, noted rows included."""
    text = "\n".join(report_lines("compare_MA.tsv", show_noted=True)) + "\n"
    path = hbce_paths.out_dir() / "candidates_MA_full.txt"
    path.write_text(text, encoding="utf-8", newline="\n")
