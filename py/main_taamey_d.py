"""Taamey D's documentation pages, checks, corpus and releases, in py/taamey_d/.

Subcommands:
    doc
        Write Taamey_D.html and Xolam_xaser_for_alef.html under gh-pages/taamey-d/,
        refusing if a comparison cell no longer matches its frozen image's record.
    qa
        Run the anchor-family lint and the four shaping checks of py/taamey_d/qa/ on
        the tracked Taamey-D/font-m-TaD/Taamey_D.ttf and the corpus in
        Taamey-D/qa-in/, printing every result and rewriting the tracked reports in
        Taamey-D/qa-out/Taamey_D/.  --one-check {mrun,plac,regr,coll} runs one shaping
        check alone.  A SKIP, an unknown status or an anchor-family FAIL raises; a
        shaping check's FAIL does not, since its report is a tracked file.
    corpus
        Refresh the Taamey-D/qa-in/bible_words_*.testcases.json test cases from this
        repository's word lists, out/mam-qere-words.json and uxlc/out/uxlc-words.json,
        printing how many test cases each file drops, adds and relabels.  It refuses
        while either list has uncommitted changes, and prints the commit it read.
        --check computes the same refresh but writes nothing, and reads the lists in
        the working tree, committed or not; when a refresh is pending, its last line
        says REFRESH PENDING and almost_main returns True, for the mega's closing
        summary, and otherwise False.  In either mode, an error that would stop a
        refresh raises.
    accept-baseline
        Accept the actual outputs in the regression reports under
        Taamey-D/qa-out/Taamey_D/ as Taamey D's expected outputs in the test cases of
        Taamey-D/qa-in/.  It is an explicit baseline operation that needs Ben's
        approval, not a test.
    release-check
        Check the published downloads tree, gh-pages/taamey-d/downloads/: every
        snapshot and latest/ against the source commit that its provenance names,
        the index's links, and that no committed snapshot changed or disappeared, in
        the working tree against HEAD and in Git's history.  It takes no options.
        Before the first release, when neither the tree nor any path under it in
        Git's history exists, it says that no snapshot is published.  A missing
        source commit raises, as SourceCommitOutsideShallowHistory in a shallow
        clone.
    release-publish
        Build the snapshot of --snapshot-commit, HEAD as 40 lowercase hex digits,
        whose release inputs must all be committed, twice in two scratch roots;
        compare and check both builds; then install the snapshot under
        gh-pages/taamey-d/downloads/snapshots/, replace latest/ with a copy of it,
        and rewrite the index.  --published-date YYYY-MM-DD defaults to today's date
        in New York.  Publishing a release is an outward-facing act.
"""

import argparse
import sys


def build_parser():
    """Describe the closed command set without running an operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doc", help="Write Taamey D's documentation pages")
    qa = commands.add_parser(
        "qa", help="Run Taamey D's shaping checks and rewrite their reports"
    )
    qa.add_argument(
        "--one-check",
        choices=("mrun", "plac", "regr", "coll"),
        help="run only the shaping check with this short name",
    )
    corpus = commands.add_parser(
        "corpus",
        help="Refresh the Bible-words test cases from this repository's word lists",
    )
    corpus.add_argument(
        "--check",
        action="store_true",
        help="report what a refresh would change, writing nothing",
    )
    commands.add_parser(
        "accept-baseline",
        help="Accept the regression reports' actual outputs as Taamey D's expected"
        " outputs: an explicit baseline operation that needs Ben's approval, not a test",
    )
    commands.add_parser(
        "release-check",
        help="Check Taamey D's published downloads tree, gh-pages/taamey-d/downloads/",
    )
    release_publish = commands.add_parser(
        "release-publish",
        help="Build, verify and install one immutable Taamey D snapshot, with latest/"
        " and the downloads index: an outward-facing act",
    )
    release_publish.add_argument(
        "--snapshot-commit",
        required=True,
        help="the snapshot's source commit, HEAD, as 40 lowercase hex digits",
    )
    release_publish.add_argument(
        "--published-date",
        help="the publication date, YYYY-MM-DD; by default today's date in New York",
    )
    return parser


def almost_main(argv=None):
    """Dispatch one explicit operation, importing only what that operation needs."""
    args = build_parser().parse_args(argv)
    if args.command == "doc":
        from taamey_d.doc.gen_doc import write_pages

        return write_pages()
    if args.command == "qa":
        from taamey_d.qa.run_checks import run_checks

        return run_checks(args.one_check)
    if args.command == "corpus":
        from taamey_d.qa.corpus_refresh import refresh_corpus

        return refresh_corpus(args.check)
    if args.command == "accept-baseline":
        from taamey_d.qa.accept_baseline import accept_baseline

        return accept_baseline()
    if args.command == "release-check":
        from taamey_d.release import release_check

        return release_check()
    if args.command == "release-publish":
        from taamey_d.release import release_publish

        return release_publish(args.snapshot_commit, args.published_date)
    raise ValueError("unknown Taamey D operation")


def main():
    """Use UTF-8 for both Windows and POSIX pipes."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    return almost_main()


if __name__ == "__main__":
    main()
