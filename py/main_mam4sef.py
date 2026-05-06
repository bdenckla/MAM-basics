"""Create Sefaria and/or AJF MAM variants from the XML MAM."""

import argparse
import sys

from mb_cmn import bib_locales as tbn
from mb_sefaria import mam4sef_letter_small_report
from mb_sefaria import mam4sef_runners


def run_sef():
    """Create the Sefaria MAM from the XML MAM."""
    mam4sef_runners.run_sef()


def run_ajf():
    """Create the AJF MAM from the XML MAM."""
    mam4sef_runners.run_ajf()


def run_both_sef_and_ajf():
    """Create both Sefaria and AJF MAM variants from the XML MAM."""
    mam4sef_runners.run_both_sef_and_ajf()


def run_both_sef_and_misc():
    """Create both main exports plus misc outputs.

    "misc" currently means generating out/letter-small.txt by scanning
    MAM-simple xml-vtrad-mam data for <letter-small> occurrences.
    """
    run_both_sef_and_ajf()
    mam4sef_letter_small_report.write_letter_small_report(tbn.ALL_BK39_IDS)


def almost_main():
    """Create the Sefaria MAM from the XML MAM."""
    run_sef()


def _build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    mutex = parser.add_mutually_exclusive_group()
    mutex.add_argument(
        "--both-sef-and-ajf",
        action="store_true",
        help="Generate both Sefaria and AJF outputs.",
    )
    mutex.add_argument(
        "--just-ajf",
        action="store_true",
        help="Generate only AJF outputs.",
    )
    parser.add_argument(
        "--write-letter-small-report",
        action="store_true",
        help="Also write out/letter-small.txt from MAM-simple xml-vtrad-mam data.",
    )
    return parser


def _runner_from_args(args):
    if args.just_ajf:
        return run_ajf
    if args.both_sef_and_ajf:
        return run_both_sef_and_ajf
    return run_sef


def _run_with_passthrough_argv(runner, passthrough_argv):
    old_argv = sys.argv
    try:
        sys.argv = [old_argv[0], *passthrough_argv]
        runner()
    finally:
        sys.argv = old_argv


def _bkids_from_passthrough_argv(passthrough_argv):
    parser = argparse.ArgumentParser(add_help=False)
    mutex = parser.add_mutually_exclusive_group()
    mutex.add_argument("--book39")
    mutex.add_argument("--section6")
    args, _unknown = parser.parse_known_args(passthrough_argv)
    if args.book39:
        return (args.book39,)
    if args.section6:
        return tbn.bk39s_of_sec(args.section6)
    return tbn.ALL_BK39_IDS


def main(argv=None):
    """Create Sefaria output by default, with explicit selectors for AJF modes."""
    if argv is None:
        argv = sys.argv[1:]
    args, passthrough_argv = _build_parser().parse_known_args(argv)
    runner = _runner_from_args(args)
    _run_with_passthrough_argv(runner, passthrough_argv)
    if args.write_letter_small_report:
        bkids = _bkids_from_passthrough_argv(passthrough_argv)
        mam4sef_letter_small_report.write_letter_small_report(bkids)


if __name__ == "__main__":
    main()
