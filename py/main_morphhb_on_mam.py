"""Apply morphhb's morphology to MAM's text: a feasibility study, put on ice on 2026-11-16.

morphhb, the morphology of the Open Scriptures Hebrew Bible, gives each word of its text of
the Westminster Leningrad Codex a lemma, a morph code and an id. This program aligns morphhb's
words at db6c5c9b with MAM's atoms in MAM-simple's JSON, classifies every atom, breaks the
classes down and builds the study's page. morphhb-on-mam/README.md describes the study, which
Ben put on ice on 2026-11-16: the files under morphhb-on-mam/out/ record one run, and the
program is rerun only if the work resumes. It reads morphhb's wlc/ directory, named on the
command line, and files of this repository, MAM-simple's JSON among them, and it never touches
the network.

The large intermediates, 10-atoms*.jsonl and 11-unmatched-morphhb*.jsonl (about 445 MB), go to
the work directory, --work-dir, by default .novc/morphhb-on-mam/work/, which is not tracked.

Subcommands:
    verify-morphhb
        Check that a wlc/ directory holds exactly the 40 files that
        morphhb-on-mam/in/fetched/morphhb-wlctree-1.json lists for morphhb's db6c5c9b, each
        with its Git blob SHA-1. Writes nothing; exits non-zero on any problem.
    census
        Write the censuses of MAM's atoms, 01-, 03- and 31-, under morphhb-on-mam/out/.
    align
        Align one strand of MAM (--strand, cant-combined by default) with morphhb: the
        records go to the work directory, the summary, 12-align-summary*.txt, under
        morphhb-on-mam/out/.
    analyze
        From the work directory's records of all three strands, write the breakdowns, lists
        and figures, 20- to 30-, under morphhb-on-mam/out/, and the views 28- and 29- that
        the page links; 29- reads the wlc/ directory again.
    page
        Build morphhb-on-mam/out/morphhb-on-mam.html and its visible text, 40-page-text.txt,
        then check them against the outputs; exits non-zero on any problem.
    selftest-page
        Show that the page's checks catch planted faults and that its placeholders work.
        Writes nothing.
    all
        verify-morphhb, census, align for each strand, analyze and page, stopping at the
        first failure. Then read `git diff -- morphhb-on-mam/out`: the outputs are the test.
"""

import argparse
import sys
from pathlib import Path

from morphhb_on_mam import align
from morphhb_on_mam import analyze
from morphhb_on_mam import analyze2
from morphhb_on_mam import analyze3
from morphhb_on_mam import build_page
from morphhb_on_mam import census
from morphhb_on_mam import figures
from morphhb_on_mam import mam_reader
from morphhb_on_mam import page_check
from morphhb_on_mam import page_selftest
from morphhb_on_mam import record_paths
from morphhb_on_mam import strands
from morphhb_on_mam import verify
from morphhb_on_mam import views

_WLC_HELP = (
    "morphhb's wlc/ directory at db6c5c9b: a flat directory of <Book>.xml files, as in a"
    " morphhb checkout"
)


def _verified(wlc_dir) -> bool:
    n_ok, found = verify.problems(wlc_dir)
    print(f"{n_ok} files match the tracked listing; {len(found)} problems")
    for line in found:
        print("  " + line)
    return not found


def _run_verify(args):
    if not _verified(args.wlc_dir):
        sys.exit(1)


def _out_dir():
    out = record_paths.out_dir()
    out.mkdir(parents=True, exist_ok=True)
    return out


def _run_census(_args):
    census.run(_out_dir())


def _run_align(args):
    args.work_dir.mkdir(parents=True, exist_ok=True)
    align.run(args.wlc_dir, args.work_dir, _out_dir(), args.strand)


def _run_analyze(args):
    work, out = args.work_dir, _out_dir()
    analyze.run(work, out)
    analyze2.run(work, out)
    analyze3.run(work, out)
    strands.run(work, out)
    figures.run(work, out)
    views.write_list_views(out)
    views.write_pairs(args.wlc_dir, out)


def _run_page(args):
    build_page.write_page(args.work_dir)
    if page_check.check(args.work_dir):
        sys.exit(1)


def _run_selftest_page(_args):
    page_selftest.run()


def _run_all(args):
    if not _verified(args.wlc_dir):
        sys.exit(1)
    _run_census(args)
    args.work_dir.mkdir(parents=True, exist_ok=True)
    for strand in mam_reader.STRANDS:
        align.run(args.wlc_dir, args.work_dir, _out_dir(), strand)
    _run_analyze(args)
    _run_page(args)


def _add_wlc_dir(parser):
    parser.add_argument("wlc_dir", type=Path, help=_WLC_HELP)


def _add_work_dir(parser):
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=record_paths.default_work_dir(),
        help="where the large intermediates are (default: .novc/morphhb-on-mam/work/)",
    )


def build_parser():
    """Return the argument parser, buildable without running the program."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    sub = subparsers.add_parser(
        "verify-morphhb", help="check a wlc/ directory against the tracked listing"
    )
    _add_wlc_dir(sub)
    subparsers.add_parser("census", help="write the censuses of MAM's atoms")
    sub = subparsers.add_parser("align", help="align one strand of MAM with morphhb")
    _add_wlc_dir(sub)
    sub.add_argument(
        "--strand", choices=mam_reader.STRANDS, default=mam_reader.STRANDS[0]
    )
    _add_work_dir(sub)
    sub = subparsers.add_parser(
        "analyze", help="write the breakdowns, lists, figures and views"
    )
    _add_wlc_dir(sub)
    _add_work_dir(sub)
    sub = subparsers.add_parser("page", help="build the study's page, then check it")
    _add_work_dir(sub)
    subparsers.add_parser(
        "selftest-page", help="show that the page's checks catch planted faults"
    )
    sub = subparsers.add_parser("all", help="run every step but selftest-page")
    _add_wlc_dir(sub)
    _add_work_dir(sub)
    return parser


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = build_parser().parse_args()
    {
        "verify-morphhb": _run_verify,
        "census": _run_census,
        "align": _run_align,
        "analyze": _run_analyze,
        "page": _run_page,
        "selftest-page": _run_selftest_page,
        "all": _run_all,
    }[args.subcommand](args)


if __name__ == "__main__":
    main()
