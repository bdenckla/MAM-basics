"""Compare HBCE's transcriptions of the Aleppo and Leningrad Codices, Psalms 1-51, with MAM.

HBCE, the Critical Edition of the Hebrew Psalter, publishes its transcriptions through a
Virtual Manuscript Room. hbce-psalms/README.md describes the snapshot under hbce-psalms/in/,
how it was obtained, and why no more may be fetched the same way; the report of record is
doc/hbce-psalms-vs-mam-2026-09-26.md. This program reads only files in this repository and
never touches the network.

Subcommands:
    compare
        Regenerate every file under hbce-psalms/out/ from the snapshot and from this
        repository's MAM-simple, MAM-parsed/plus/, mirrored introduction and UXLC data.
        Then read `git diff -- hbce-psalms/out`: the outputs are the test.
    lint-receipt
        Check that every Hebrew form in the receipt is in MAM-normal mark order and
        occurs in the outputs or the transcriptions. Writes nothing.
"""

import argparse
import sys

from hbce_psalms import candidates
from hbce_psalms import compare
from hbce_psalms import cross_check_ml
from hbce_psalms import figures
from hbce_psalms import mam_docnotes
from hbce_psalms import receipt_lint
from hbce_psalms import research_queue
from hbce_psalms import tei_survey
from hbce_psalms import uxlc_check


def _run_compare(_args):
    tei_survey.write_survey()
    print("wrote tei_survey.txt")
    print(f"wrote mam_psalms_docnotes.tsv: {mam_docnotes.write_docnotes()} doc-notes")
    for line in compare.write_comparisons():
        print(line)
    candidates.write_candidates_ma_full()
    print("wrote candidates_MA_full.txt")
    cross_check_ml.write_candidates_with_ml()
    print("wrote candidates_with_ML.tsv")
    verdicts = uxlc_check.write_candidates_with_ml_uxlc()
    print(f"wrote candidates_with_ML_UXLC.tsv: {dict(verdicts)}")
    print(f"wrote research_queue.md: {research_queue.write_research_queue()}")
    figures.write_figures()
    print("wrote figures.txt")


def _run_lint_receipt(_args):
    n_forms, found = receipt_lint.problems()
    print(f"{n_forms} distinct Hebrew forms in the receipt; {len(found)} problems")
    for line in found:
        print("  " + line)
    if found:
        sys.exit(1)


def build_parser():
    """Return the argument parser, buildable without running the program."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    subparsers.add_parser(
        "compare", help="regenerate every file under hbce-psalms/out/"
    )
    subparsers.add_parser("lint-receipt", help="check the receipt's Hebrew forms")
    return parser


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = build_parser().parse_args()
    {"compare": _run_compare, "lint-receipt": _run_lint_receipt}[args.subcommand](args)


if __name__ == "__main__":
    main()
