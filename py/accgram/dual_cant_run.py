r"""Driver for the dual-cantillation detangler (issue #36).

Runs the detangler over the three dually-cantillated prose loci (Gen 35:22 and the two
Decalogues) and writes the full detangled readings to
``out/accgram/dual-cant/_dual_cant.json``: per passage, each reading's chanted verses
with their token stream and parse tree, plus the supplied-mark inventory and the
candidate-WLC-error anomalies.

This is the complete record of the detangled trees (the analogue of prose_run's
``*_ag.json``).  Two derived surfaces consume the *same* detangling separately:

  * the oddity chanted verses are folded into the prose ungrammatical-verse report (goerwitz.html)
    by prose_run, keyed by their numbered verse; and
  * the supplied-mark inventory is rendered to gh-pages/accgram/supplied-marks.html by
    accgram.supplied_marks.

Run via ``main_accgram.py run-dual-cant`` (after run-prose).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import dual_cant_detangle as dcd
from accgram import rtms_data
from accgram.mam_simple_verse import default_mam_simple_dir, load_mam_simple_for_refs
from accgram.prose_ply_grammar import build_parser
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import file_io
from mb_cmn import provenance

import wlc_paths


def default_out_path(repo_root: Path) -> Path:
    return wlc_paths.out_dir() / "accgram" / "dual-cant" / "_dual_cant.json"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--wlc422-kq-u-dir",
        type=Path,
        default=rtms_data.default_wlc422_kq_u_dir(repo_root),
        help="Directory of WLC 4.22 ketiv/qere Unicode 1verses_*.json files.",
    )
    parser.add_argument(
        "--mam-simple-dir",
        type=Path,
        default=default_mam_simple_dir(repo_root),
        help="Directory of MAM-simple json-vtrad-bhs book files.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=default_out_path(repo_root),
        help="Output JSON path for the detangled dual-cantillation readings.",
    )


def detangle_results(
    wlc422_kq_u_dir: Path, mam_simple_dir: Path
) -> list[dcd.PassageResult]:
    wlc_index = rtms_data.load_wlc422_index(wlc422_kq_u_dir)
    mam_by_bcv = load_mam_simple_for_refs(
        mam_simple_dir, dcd.all_refs_by_book(), include_strands=True
    )
    return dcd.detangle_all(wlc_index, mam_by_bcv, build_parser())


def run(args: argparse.Namespace) -> None:
    results = detangle_results(args.wlc422_kq_u_dir, args.mam_simple_dir)
    payload = _payload(results)
    payload = provenance.with_json_provenance(payload, __file__)

    out_path: Path = args.out
    # file_io: temp-file write, PermissionError retry, and it makes the directory.
    # Provenance is already on the payload, so no generator_file= here.
    file_io.json_dump_to_file_path(payload, str(out_path))

    s = payload["summary"]
    print(
        f"dual-cant: {s['passages']} passages, {s['chanted_verses']} chanted verses "
        f"({s['ungrammatical']} ungrammatical verses), {s['supplied_marks']} supplied marks, "
        f"{s['anomalies']} anomalies, {s['punctuation_changes']} punctuation changes -> {out_path}"
    )


def _payload(results: list[dcd.PassageResult]) -> dict[str, object]:
    chanted_verses = [
        cv for pr in results for tr in pr.strands for cv in tr.chanted_verses
    ]
    return {
        "summary": {
            "passages": len(results),
            "chanted_verses": len(chanted_verses),
            "clean": sum(1 for cv in chanted_verses if cv.status == "clean"),
            "ungrammatical": sum(1 for cv in chanted_verses if cv.status != "clean"),
            "supplied_marks": sum(len(pr.supplied_marks) for pr in results),
            "anomalies": sum(len(pr.anomalies) for pr in results),
            "punctuation_changes": sum(len(pr.punctuation_changes) for pr in results),
        },
        "passages": [_passage_obj(pr) for pr in results],
    }


def _passage_obj(pr: dcd.PassageResult) -> dict[str, object]:
    return {
        "name": pr.passage.name,
        "bb": pr.passage.bb,
        "alef_label": pr.passage.alef_label,
        "bet_label": pr.passage.bet_label,
        "strands": [_strand_obj(tr) for tr in pr.strands],
        "supplied_marks": [_supply_obj(s) for s in pr.supplied_marks],
        "anomalies": [_anomaly_obj(a) for a in pr.anomalies],
        "punctuation_changes": [
            _punctuation_change_obj(d) for d in pr.punctuation_changes
        ],
    }


def _strand_obj(tr: dcd.StrandResult) -> dict[str, object]:
    return {
        "strand": tr.strand,
        "strand_label": tr.strand_label,
        "chanted_verses": [_chanted_verse_obj(cv) for cv in tr.chanted_verses],
    }


def _chanted_verse_obj(cv: dcd.ChantedVerseResult) -> dict[str, object]:
    return {
        "ref": cv.ref,
        "bcv_span": list(cv.bcv_span),
        "status": cv.status,
        "words": list(cv.words),
        "word_bcvs": list(cv.word_bcvs),
        "marks": cv.body,
        "tokens": list(cv.tokens),
        "tree": cv.tree,
        "word_leaf_counts": list(cv.word_leaf_counts),
    }


def _supply_obj(s: dcd.SuppliedMark) -> dict[str, object]:
    return {
        "bcv": s.bcv,
        "strand": s.strand,
        "strand_label": s.strand_label,
        "mam_word": s.mam_word,
        "wlc_word": s.wlc_word,
        "accent": s.accent,
        "accent_name": s.accent_name,
        "reason": s.reason,
        "source": s.source,
        "aside": s.aside,
    }


def _punctuation_change_obj(d: dcd.PunctuationChange) -> dict[str, object]:
    return {
        "bcv": d.bcv,
        "strand": d.strand,
        "strand_label": d.strand_label,
        "mark": d.mark,
        "delta": d.delta,
        "wlc_word": d.wlc_word,
        "mam_word": d.mam_word,
    }


def _anomaly_obj(a: dcd.Anomaly) -> dict[str, object]:
    return {
        "bcv": a.bcv,
        "strand": a.strand,
        "strand_label": a.strand_label,
        "mam_word": a.mam_word,
        "wlc_word": a.wlc_word,
        "expected": a.expected,
        "expected_name": a.expected_name,
        "found": a.found,
        "found_name": a.found_name,
    }


def main() -> None:
    force_utf8_io()
    repo_root = wlc_paths.wlc_data_root()
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser, repo_root=repo_root)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
