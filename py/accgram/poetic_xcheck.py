r"""Cross-check the poetic scanner's disjunctive segmentation against MAM-simple.

Phase 2 of ``doc/PLAN-poetic-accent-grammar.md``: confirm the trees' division
points are *correct*, not merely parseable.  For every poetic verse we compare two
ordered disjunctive sequences:

  * WLC side -- the disjunctive tokens the scanner (``poetic_scanner``) reads
    from the Michigan-Claremont codes, in order.
  * MAM side -- the disjunctive sequence extracted from MAM-simple's pointed
    Unicode text by ``mam_poetic_accents.disjunctives_from_verse_node``.

Servus (conjunctive) signs are excluded on both sides: L and MAM routinely pick
different conjunctive *signs* for the same slot and Yeivin pins no exact servus
chains, so only the disjunctive skeleton is a meaningful equality check (see
``mam_poetic_accents`` for the rationale).

The WLC side compares the *reconciled* token stream (``poetic_reconcile``), the same
one the driver parses.  One consequence is honest to flag: legarmeh-vs-paseq is not in
WLC's M-C source, so the reconciler resolves it *from MAM* -- the legarmeh dimension of
this check is therefore agree-by-construction, not an independent witness.  Every other
disjunctive (silluq, atnax, oleh-we-yored, the revias, dexi, tsinnor, pazer) is still
derived from WLC alone, so the check remains a meaningful Phase-2 surface for them.

The run writes a git-tracked report ``out/accgram/poetic/_mam_xcheck.txt``: a
per-book agreement tally, then every divergence grouped by its edit signature
(the difflib opcodes turning the WLC sequence into the MAM one), each annotated
with whether the WLC verse currently parses.  This file is the Phase 2 verification
surface -- regenerate and diff it after any scanner change.
"""

from __future__ import annotations

import argparse
import difflib
from dataclasses import dataclass
from pathlib import Path

from accgram import poetic_filter
from accgram import rtms_data
from accgram import uni_to_marks
from accgram.mam_poetic_accents import load_poetic_disjunctives
from accgram.mam_simple_verse import default_mam_simple_dir
from accgram.poetic_accent_names import POETIC_DISJUNCTIVES
from accgram.poetic_ply_grammar import build_parser, parse_tokens
from accgram.poetic_scanner import scan_book
from accgram.poetic_reconcile import reconcile_tokens

from mb_cmn import paths


@dataclass(frozen=True)
class Divergence:
    reference: str
    wlc: tuple[str, ...]
    mam: tuple[str, ...]
    parses: bool
    signature: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...]


def _edit_signature(
    wlc: list[str], mam: list[str]
) -> tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...]:
    """The difflib opcodes (minus 'equal') turning the WLC seq into the MAM seq."""
    matcher = difflib.SequenceMatcher(a=wlc, b=mam, autojunk=False)
    return tuple(
        (tag, tuple(wlc[i1:i2]), tuple(mam[j1:j2]))
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
        if tag != "equal"
    )


def _signature_label(
    signature: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...],
) -> str:
    parts = []
    for tag, wlc_run, mam_run in signature:
        if tag == "insert":
            parts.append(f"MAM adds {' '.join(mam_run)}")
        elif tag == "delete":
            parts.append(f"WLC has extra {' '.join(wlc_run)}")
        else:  # replace
            parts.append(f"WLC {' '.join(wlc_run)} -> MAM {' '.join(mam_run)}")
    return "; ".join(parts)


def collect_divergences(
    input_path: Path, mam_simple_dir: Path
) -> tuple[list[Divergence], dict[str, tuple[int, int]]]:
    """Return (divergences, per-book (matched, total)) over the poetic corpus."""
    mam_by_ref = load_poetic_disjunctives(mam_simple_dir)
    parser = build_parser()
    book_texts = uni_to_marks.build_book_texts(
        input_path, keep_line_fn=poetic_filter.should_keep_line
    )

    divergences: list[Divergence] = []
    per_book: dict[str, tuple[int, int]] = {}
    for bb, text in book_texts.items():
        matched = 0
        total = 0
        for verse in scan_book(text, bb):
            mam = mam_by_ref.get(verse.reference)
            if mam is None:
                continue
            total += 1
            tokens = reconcile_tokens(
                verse.reference, verse.body, list(verse.tokens), mam, parser
            )
            wlc = [t for t, _ in tokens if t in POETIC_DISJUNCTIVES]
            if wlc == mam:
                matched += 1
                continue
            divergences.append(
                Divergence(
                    reference=verse.reference,
                    wlc=tuple(wlc),
                    mam=tuple(mam),
                    parses=parse_tokens(parser, tokens) is not None,
                    signature=_edit_signature(wlc, mam),
                )
            )
        per_book[bb] = (matched, total)
    return divergences, per_book


def render_report(
    divergences: list[Divergence], per_book: dict[str, tuple[int, int]]
) -> str:
    lines: list[str] = []
    lines.append("# Poetic scanner vs MAM-simple: disjunctive cross-check")
    lines.append("")
    total_matched = sum(m for m, _ in per_book.values())
    total_all = sum(t for _, t in per_book.values())
    for bb, (matched, total) in per_book.items():
        rate = 100.0 * matched / total if total else 0.0
        lines.append(f"{bb}: {matched}/{total} verses agree ({rate:.2f}%)")
    overall = 100.0 * total_matched / total_all if total_all else 0.0
    lines.append(
        f"total: {total_matched}/{total_all} agree ({overall:.2f}%); "
        f"{len(divergences)} divergences"
    )
    lines.append("")

    by_sig: dict[
        tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...], list[Divergence]
    ] = {}
    for div in divergences:
        by_sig.setdefault(div.signature, []).append(div)

    lines.append("## Divergences grouped by edit signature")
    lines.append("")
    for signature, group in sorted(by_sig.items(), key=lambda kv: -len(kv[1])):
        parses_n = sum(1 for d in group if d.parses)
        lines.append(
            f"### {_signature_label(signature)} "
            f"-- {len(group)} verse(s); {parses_n} parse, "
            f"{len(group) - parses_n} NO_PARSE"
        )
        for div in group:
            flag = "parses" if div.parses else "NO_PARSE"
            lines.append(f"  {div.reference} [{flag}]")
            lines.append(f"    WLC: {' '.join(div.wlc)}")
            lines.append(f"    MAM: {' '.join(div.mam)}")
        lines.append("")
    return "\n".join(lines) + "\n"


def default_input_path(repo_root: Path) -> Path:
    return rtms_data.default_wlc422_kq_u_dir(repo_root)


def default_report_path(repo_root: Path) -> Path:
    return paths.out_dir() / "accgram" / "poetic" / "_mam_xcheck.txt"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input_path(repo_root),
        help="Directory of the -kq-u Unicode source (wlc422-kq-u/1verses_*.json).",
    )
    parser.add_argument(
        "--mam-simple-dir",
        type=Path,
        default=default_mam_simple_dir(repo_root),
        help="Directory containing MAM-simple json-vtrad-bhs book files.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=default_report_path(repo_root),
        help="Output path for the cross-check report.",
    )


def run(args: argparse.Namespace) -> None:
    divergences, per_book = collect_divergences(args.input, args.mam_simple_dir)
    report = render_report(divergences, per_book)

    report_path: Path = args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8", newline="\n")

    total_matched = sum(m for m, _ in per_book.values())
    total_all = sum(t for _, t in per_book.values())
    overall = 100.0 * total_matched / total_all if total_all else 0.0
    print(
        f"Cross-check: {total_matched}/{total_all} verses agree ({overall:.2f}%); "
        f"{len(divergences)} divergences -> {report_path}"
    )
