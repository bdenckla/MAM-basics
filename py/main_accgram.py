"""Accent grammar utilities.

Subcommands:
    run-prose
                Run the Python port over the WLC prose corpus
                (out/wlc422-kq-u, genre-filtered) and write
                out/accgram/prose/*_ag.json (mirrors `accents -p`, one JSON record
                per verse).  A verse the grammar cannot parse at all is a fatal
                error.  Use --book to restrict to specific books (e.g. --book ob).
    run-poetic
                Run the POETIC (Three Books) scanner + grammar over the
                poetic corpus (Psalms, Proverbs, poetically-cantillated Job) and
                write out/accgram/poetic/*_ag.json (one JSON record per verse).
                Unparseable verses are recorded as no_parse and tallied, not
                fatal.  Use --book to restrict (ps, pr, jb).
    run-dual-cant
                Detangle WLC's three dually-cantillated prose loci (Gen 35:22 and
                the two Decalogues) into two single-cantillation readings each,
                guided by MAM's cant-alef/cant-bet strands, and write
                out/accgram/dual-cant/_dual_cant.json (each reading's chanted-verse
                trees, the supplied-mark inventory, and candidate-WLC-error
                anomalies).  The oddity chanted verses are separately folded into
                the prose ungrammatical-verse report by run-prose; supplied-marks.html is
                rendered by generate-html.  Run after run-prose (issue wlc-utils#36).
    run-printed-decalogue
                Grammar-check the printed-tradition (דפוסים) Decalogue
                accentuations against the manuscript baseline -- both books,
                taxton and elyon -- and write
                out/accgram/printed-decalogue/_printed_decalogue.json (issue wlc-utils#52).
                Reads the vendored in/accgram/printed_decalogue_teamim.json that
                vendor-printed-decalogue refreshes, plus the committed hand
                transcriptions under in/accgram/edition_transcriptions, whose own
                verdicts against the strand each follows go in the file's
                transcriptions section.
    survey-chanted-word-accents
                Measure every chanted word carrying two or more accent TOKENS across
                WLC 4.22, UXLC and MAM-simple, prose verses only, and write
                out/accgram/chanted-word-accents.json.  Transcribes Yeivin's prose
                inventory of the phenomenon beside the measurement and raises where
                one of his closed verse lists and the data disagree.
    xcheck-poetic
                Cross-check the poetic scanner's disjunctive segmentation against
                MAM-simple and write out/accgram/poetic/_mam_xcheck.txt (a
                per-book agreement tally plus every divergence grouped by edit
                signature).  The Phase 2 validation surface.
    servi-xcheck
                Cross-check, per disjunctive, the servant (conjunctive) the WLC
                scanner and MAM-simple put immediately before it, and write
                out/accgram/poetic/_servi_xcheck.txt.  The second-witness gate
                for vetting Breuer servant-adjacency rules (it settled dexi and
                small revia).  Use --target to restrict.
    generate-html
                Generate the accgram HTML reports in one pass:

                  * gh-pages/accgram/poetic.html -- the residual poetic ungrammatical
                    (missing-silluq ERROR-leaf trees and NO_PARSE anomalies),
                    each enriched with its pointed-Hebrew text, scanned token
                    sequence, rendered tree, and WLC-vs-MAM-simple disjunctive
                    comparison (plus out/accgram/poetic/_oddballs.json).
                    Run run-poetic first.
                  * gh-pages/accgram/goerwitz.html -- the prose ungrammatical
                    set (from out/accgram/prose), enriched with its matching
                    wlc422-kq-u verse object and structured XML-ish UXLC verse
                    node (plus out/accgram/research-oddballs.json).
                  * gh-pages/accgram/almost-errors.html -- the "almost errors"
                    page documenting the editorial charities the checker applies
                    and the non-charity ek20:31 mahapakh!qadma, with live parse
                    trees regenerated from the grammar at build time.
                  * gh-pages/accgram/supplied-marks.html -- the dual-cantillation
                    "Supplied and suppressed marks" page (issue wlc-utils#36): the supplied-mark
                    inventory plus the per-strand punctuation (maqaf/sof-pasuq/legarmeh)
                    restructuring, generated live from the detangling run and linked
                    from almost-errors.html.
                  * gh-pages/accgram/telg-doc-notes.html -- a deep-dive
                    translation of MAM's documentation notes on the five
                    telisha-gedola + geresh/gershayim words (companion to the
                    telg exhibit on the almost-errors page).
                  * gh-pages/accgram/ps17v14-mam-doc-notes.html and
                    ps17v14-double-tsinnor.html -- the Psalms 17:14 deep dives,
                    generated from their committed htel bodies.
                  * gh-pages/accgram/maqaf-nonfinal-accents.html -- the Tanakh-wide
                    survey of accents on a maqaf-joined atom (issue wlc-utils#76), which
                    also writes out/accgram/maqaf-nonfinal-accents.json.  Splits the
                    hits into Yeivin's grammatical secondary accents and the scribal
                    habit of §293, and settles whether Koren's Deuteronomy mun-mun on
                    לא־תעשה has a precedent.
                  * gh-pages/accgram/printed-decalogue-uvinkha.html -- the printed
                    editions cited at ובנך in MAM-basics issue #208, each with its
                    link and, where one has been taken, a crop of its page.
                  * gh-pages/accgram/wlc-chanted-word-residue.html -- WLC's chanted
                    words whose two accents are a pair no section of Yeivin's prose
                    inventory names. Deliberately linked from nothing; it is in the
                    batch so it cannot go stale. Needs run-prose first, for its
                    verdict column.

                Each report runs with its default paths.  --trust-survey lets the
                wlc-chanted-word-residue report read out/accgram/chanted-word-accents.json
                instead of spending another minute rebuilding the survey; pass it only
                after survey-chanted-word-accents, as main_0_mega.py does.
    generate-html-<name>
                Generate a single report instead of the whole batch, where <name>
                is the output file's basename (e.g. generate-html-printed-decalogue-simanim
                writes gh-pages/accgram/printed-decalogue-simanim.html). Each accepts
                the same options as its generator (e.g. --html-out). The full set:
                generate-html-poetic, -goerwitz, -almost-errors, -supplied-marks,
                -printed-decalogue, -printed-decalogue-simanim, -printed-decalogue-koren,
                -printed-decalogue-uvinkha,
                -dual-under-bars-in-leningrad-decalogues, -telg-doc-notes,
                -ps17v14-mam-doc-notes, -ps17v14-double-tsinnor,
                -maqaf-nonfinal-accents, -wlc-chanted-word-residue.
    grammaticality
                Estimate a PCFG over the committed prose + poetic parse trees
                (one production per tree node) and score each verse's
                log-likelihood -- a continuous companion to the binary
                clean/ungrammatical verdict (issue wlc-utils#11).  Reports the learned grammar,
                the rarest-but-legal verses (per-accent log-likelihood, with the
                least-probable production drilled out), and a validation that the
                flagged ungrammatical score at the bottom; an n-gram baseline is kept
                as a sanity check.  Writes out/accgram/_grammaticality.txt.  Run
                run-prose + run-poetic first (it reads their committed JSON).
    test-fixes
                For every annotated prose ungrammatical verse, test whether adopting its
                MAM-simple value clears the ERROR: substitute the MAM value into the
                verse, re-transcode + re-scan + re-parse, and classify CONFIRMED / DENIED /
                CHANGED / UNTESTABLE.  Cross-checks each verdict against the
                prose_ob_notes claim and writes out/accgram/fix-tester/_fix_tester.{txt,json}.
                Run run-prose first.
    vendor-printed-decalogue
                NETWORK AUTHOR TOOL, run by hand.  Refresh the vendored snapshot of the
                eight Wikisource Decalogue accentuations ({Exodus, Deuteronomy} × {taxton,
                elyon} × {manuscript, printed}) from he.wikisource's
                עשרת הדברות בסיס/טעמים, and overwrite
                in/accgram/printed_decalogue_teamim.json.  Each version is stored twice:
                the folded scanner-ready chanted verses, and the faithful ones that keep
                the legarmeh/paseq, ketiv/qere and setumah/petuxah templates (issue wlc-utils#74).
                --oldid pins a revision; the committed snapshot is 3025606.
    vendor-ctr-decalogue
                NETWORK AUTHOR TOOL, run by hand.  Refresh the vendored snapshot of CTR's
                two Decalogues -- Exodus 20:2-14 and Deuteronomy 5:6-18 of the Complete
                Tanach with Rashi at chabad.org -- and overwrite
                in/accgram/ctr_decalogue.json (issue wlc-utils#73).  The verse text is kept
                accent-exact, with CTR's own encoding intact; normalizing it is
                ctr_decalogue.py's job, not the vendoring's.  --cache reads pre-fetched
                chapter HTML from a directory instead of hitting the server.

Examples:
    .venv/Scripts/python.exe py/main_accgram.py run-prose
    .venv/Scripts/python.exe py/main_accgram.py run-prose --book ob
    .venv/Scripts/python.exe py/main_accgram.py generate-html
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import almost_errors
from accgram import chanted_word_accents
from accgram import ctr_decalogue_fetch
from accgram import dual_cant_run
from accgram import dual_under_bars_page
from accgram import fix_tester
from accgram import grammaticality
from accgram import maqaf_nonfinal_accents_page
from accgram import poetic_oddballs
from accgram import ps17v14_double_tsinnor
from accgram import ps17v14_doc_notes
from accgram import research_tao
from accgram import prose_run
from accgram import poetic_run
from accgram import printed_decalogue
from accgram import printed_decalogue_fetch
from accgram import printed_decalogue_koren_page
from accgram import printed_decalogue_page
from accgram import printed_decalogue_simanim_page
from accgram import printed_decalogue_uvinkha_page
from accgram import supplied_marks
from accgram import servi_xcheck
from accgram import telg_doc_notes
from accgram import wlc_chanted_word_residue_page
from accgram import poetic_xcheck
from wlc_cmn.utf8_io import force_utf8_io

import wlc_paths


def _repo_root() -> Path:
    return wlc_paths.wlc_data_root()


def _run_run_prose(args: argparse.Namespace) -> None:
    prose_run.run(args)


def _run_run_poetic(args: argparse.Namespace) -> None:
    poetic_run.run(args)


def _run_run_dual_cant(args: argparse.Namespace) -> None:
    dual_cant_run.run(args)


def _run_run_printed_decalogue(args: argparse.Namespace) -> None:
    printed_decalogue.run(args)


def _run_survey_chanted_word_accents(args: argparse.Namespace) -> None:
    chanted_word_accents.run(args)


def _run_xcheck_poetic(args: argparse.Namespace) -> None:
    poetic_xcheck.run(args)


def _run_servi_xcheck(args: argparse.Namespace) -> None:
    servi_xcheck.run(args)


def _run_fix_tester(args: argparse.Namespace) -> None:
    fix_tester.run(args)


def _run_grammaticality(args: argparse.Namespace) -> None:
    grammaticality.run(args)


def _run_vendor_printed_decalogue(args: argparse.Namespace) -> None:
    printed_decalogue_fetch.run(args)


def _run_vendor_ctr_decalogue(args: argparse.Namespace) -> None:
    ctr_decalogue_fetch.run(args)


# HTML report generators, as (name, module) pairs.  Each name is the basename of the file the
# module generates (gh-pages/accgram/<name>.html), so the derived subcommands are named
# accordingly: `generate-html` runs the whole list, `generate-html-<name>` runs just one.
_HTML_GENERATORS = (
    ("poetic", poetic_oddballs),
    ("goerwitz", research_tao),
    ("almost-errors", almost_errors),
    ("supplied-marks", supplied_marks),
    ("printed-decalogue", printed_decalogue_page),
    ("printed-decalogue-simanim", printed_decalogue_simanim_page),
    # BEFORE printed-decalogue-koren, which reads the out/accgram JSON this one writes
    # alongside its page -- the sole read of one generator's output by another.  It sat
    # after koren until 2026-08-01, which nothing noticed because the JSON was always
    # left over from a previous run: `generate-html` could not run against a deleted
    # out/accgram, and deleting out/accgram is exactly how you prove the rebuild is not
    # silently no-opping.
    ("maqaf-nonfinal-accents", maqaf_nonfinal_accents_page),
    ("printed-decalogue-koren", printed_decalogue_koren_page),
    ("printed-decalogue-uvinkha", printed_decalogue_uvinkha_page),
    ("dual-under-bars-in-leningrad-decalogues", dual_under_bars_page),
    ("telg-doc-notes", telg_doc_notes),
    ("ps17v14-mam-doc-notes", ps17v14_doc_notes),
    ("ps17v14-double-tsinnor", ps17v14_double_tsinnor),
    # Built by the batch, linked from nothing -- see that module's docstring.  Membership here
    # is what keeps it from going stale; it is not a decision to surface it anywhere.
    ("wlc-chanted-word-residue", wlc_chanted_word_residue_page),
)


# The one report whose generator can be told to read a JSON another subcommand writes rather
# than recompute it; see `_run_generate_html`.
_SURVEY_READING_REPORT = "wlc-chanted-word-residue"


assert _SURVEY_READING_REPORT in dict(_HTML_GENERATORS), (
    f"{_SURVEY_READING_REPORT} names no report in _HTML_GENERATORS; a rename here fails"
    " silently otherwise -- the mega would simply pay the survey twice again"
)


def _generate_one_html(module, argv: tuple[str, ...] = ()) -> None:
    """Run a single HTML generator module with its default arguments, plus ``argv``.

    ``argv`` goes through the module's own parser rather than being set on the namespace by
    hand, so a flag the batch passes is spelled and validated by the module that declares it.
    """
    sub = argparse.ArgumentParser()
    module.add_args(sub, repo_root=_repo_root())
    module.run(sub.parse_args(list(argv)))


def _generate_one_html_from_args(module, args: argparse.Namespace) -> None:
    """Run a single HTML generator module with the args parsed for its subcommand."""
    module.run(args)


def _run_generate_html(args: argparse.Namespace) -> None:
    """Run every HTML generator, each with its own default arguments."""
    trust_survey = getattr(args, "trust_survey", False)
    for name, module in _HTML_GENERATORS:
        argv = (
            ("--trust-survey",)
            if trust_survey and name == _SURVEY_READING_REPORT
            else ()
        )
        _generate_one_html(module, argv)


def build_parser() -> argparse.ArgumentParser:
    """The fully-configured parser, so a test can read the subcommands off it."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="subcommand", metavar="SUBCOMMAND")
    subparsers.required = True

    run_prose_parser = subparsers.add_parser(
        "run-prose",
        help=(
            "Run the Python port over the WLC prose corpus and write "
            "out/accgram/prose/*_ag.json (mirrors `accents -p`). Use --book to "
            "restrict (e.g. --book ob)."
        ),
    )
    prose_run.add_args(run_prose_parser, repo_root=_repo_root())
    run_prose_parser.set_defaults(func=_run_run_prose)

    run_poetic_parser = subparsers.add_parser(
        "run-poetic",
        help=(
            "Run the poetic (Three Books) scanner + grammar over Psalms, "
            "Proverbs, and poetically-cantillated Job and write "
            "out/accgram/poetic/*_ag.json (one JSON record per verse). "
            "Unparseable verses become no_parse records (not fatal). Use "
            "--book to restrict (ps, pr, jb)."
        ),
    )
    poetic_run.add_args(run_poetic_parser, repo_root=_repo_root())
    run_poetic_parser.set_defaults(func=_run_run_poetic)

    run_dual_cant_parser = subparsers.add_parser(
        "run-dual-cant",
        help=(
            "Detangle the dually-cantillated prose loci (Gen 35:22 + the two "
            "Decalogues) into two single-cantillation readings each and write "
            "out/accgram/dual-cant/_dual_cant.json (chanted-verse trees + supplied "
            "marks + anomalies). Run after run-prose."
        ),
    )
    dual_cant_run.add_args(run_dual_cant_parser, repo_root=_repo_root())
    run_dual_cant_parser.set_defaults(func=_run_run_dual_cant)

    run_printed_decalogue_parser = subparsers.add_parser(
        "run-printed-decalogue",
        help=(
            "Grammar-check the printed-tradition (דפוסים) Decalogue accentuations "
            "against the manuscript baseline -- both books, taxton and elyon -- and write "
            "out/accgram/printed-decalogue/_printed_decalogue.json (issue wlc-utils#52). Reads the "
            "vendored in/accgram/printed_decalogue_teamim.json, plus the committed hand "
            "transcriptions under in/accgram/edition_transcriptions, whose own verdicts "
            "against the strand each follows go in the file's transcriptions section."
        ),
    )
    printed_decalogue.add_args(run_printed_decalogue_parser, repo_root=_repo_root())
    run_printed_decalogue_parser.set_defaults(func=_run_run_printed_decalogue)

    chanted_word_parser = subparsers.add_parser(
        "survey-chanted-word-accents",
        help=(
            "Measure every prose chanted word with two or more accent tokens across WLC "
            "4.22, UXLC and MAM-simple, with Yeivin's own prose inventory beside it, and "
            "write out/accgram/chanted-word-accents.json."
        ),
    )
    chanted_word_accents.add_args(chanted_word_parser, repo_root=_repo_root())
    chanted_word_parser.set_defaults(func=_run_survey_chanted_word_accents)

    xcheck_poetic_parser = subparsers.add_parser(
        "xcheck-poetic",
        help=(
            "Cross-check the poetic scanner's disjunctive segmentation against "
            "MAM-simple and write out/accgram/poetic/_mam_xcheck.txt."
        ),
    )
    poetic_xcheck.add_args(xcheck_poetic_parser, repo_root=_repo_root())
    xcheck_poetic_parser.set_defaults(func=_run_xcheck_poetic)

    servi_xcheck_parser = subparsers.add_parser(
        "servi-xcheck",
        help=(
            "Cross-check, per disjunctive, the servant (conjunctive) the WLC scanner "
            "and MAM-simple put immediately before it -- the second-witness gate for "
            "vetting Breuer servant-adjacency rules. Writes "
            "out/accgram/poetic/_servi_xcheck.txt. Use --target to restrict."
        ),
    )
    servi_xcheck.add_args(servi_xcheck_parser, repo_root=_repo_root())
    servi_xcheck_parser.set_defaults(func=_run_servi_xcheck)

    fix_tester_parser = subparsers.add_parser(
        "test-fixes",
        help=(
            "Test whether adopting each annotated prose ungrammatical's MAM-simple value "
            "clears its ERROR; write out/accgram/fix-tester/_fix_tester.{txt,json}. "
            "Run run-prose first."
        ),
    )
    fix_tester.add_args(fix_tester_parser, repo_root=_repo_root())
    fix_tester_parser.set_defaults(func=_run_fix_tester)

    grammaticality_parser = subparsers.add_parser(
        "grammaticality",
        help=(
            "Estimate a PCFG over the committed prose + poetic parse trees and "
            "score every verse's log-likelihood -- a continuous companion to the "
            "binary clean/ungrammatical verdict (issue wlc-utils#11). Writes "
            "out/accgram/_grammaticality.txt. Run run-prose + run-poetic first."
        ),
    )
    grammaticality.add_args(grammaticality_parser, repo_root=_repo_root())
    grammaticality_parser.set_defaults(func=_run_grammaticality)

    generate_html_parser = subparsers.add_parser(
        "generate-html",
        help=(
            "Generate the accgram HTML reports in one pass: "
            "gh-pages/accgram/poetic.html (run run-poetic first), "
            "goerwitz.html, almost-errors.html, and telg-doc-notes.html. Each "
            "runs with its default paths; live trees are regenerated from the "
            "grammar."
        ),
    )
    # Passed by main_0_mega.py, whose survey-chanted-word-accents step runs directly above
    # generate-html and has therefore just written the JSON the residue page would otherwise
    # spend another minute recomputing.  Off by hand, so a batch run on its own still derives
    # every page from the code rather than from a file (#219).
    generate_html_parser.add_argument(
        "--trust-survey",
        action="store_true",
        help=(
            "Let the wlc-chanted-word-residue report read "
            "out/accgram/chanted-word-accents.json instead of rebuilding the survey. Only "
            "for a caller that has just run survey-chanted-word-accents."
        ),
    )
    generate_html_parser.set_defaults(func=_run_generate_html)

    # One `generate-html-<name>` subcommand per report, generating that file alone.  Each exposes
    # its module's own arguments (e.g. --html-out), same as the module's standalone entry point.
    for name, module in _HTML_GENERATORS:
        one_parser = subparsers.add_parser(
            f"generate-html-{name}",
            help=f"Generate gh-pages/accgram/{name}.html only.",
        )
        module.add_args(one_parser, repo_root=_repo_root())
        one_parser.set_defaults(
            func=lambda a, m=module: _generate_one_html_from_args(m, a)
        )

    # The two network author-tools, kept last because they are the only subcommands that
    # reach off the machine and the only ones that overwrite a vendored input under in/.
    vendor_printed_decalogue_parser = subparsers.add_parser(
        "vendor-printed-decalogue",
        help=(
            "NETWORK AUTHOR TOOL, run by hand: re-fetch the eight Wikisource Decalogue "
            "accentuations (both books, taxton and elyon, manuscript and printed) and "
            "overwrite the vendored in/accgram/printed_decalogue_teamim.json. --oldid pins "
            "a revision; the committed snapshot is 3025606."
        ),
    )
    printed_decalogue_fetch.add_args(
        vendor_printed_decalogue_parser, repo_root=_repo_root()
    )
    vendor_printed_decalogue_parser.set_defaults(func=_run_vendor_printed_decalogue)

    vendor_ctr_decalogue_parser = subparsers.add_parser(
        "vendor-ctr-decalogue",
        help=(
            "NETWORK AUTHOR TOOL, run by hand: re-fetch CTR's two Decalogues (Exodus "
            "20:2-14 and Deuteronomy 5:6-18 from chabad.org) accent-exact and overwrite "
            "the vendored in/accgram/ctr_decalogue.json (issue wlc-utils#73). --cache reads "
            "pre-fetched chapter HTML instead of hitting the server."
        ),
    )
    ctr_decalogue_fetch.add_args(vendor_ctr_decalogue_parser, repo_root=_repo_root())
    vendor_ctr_decalogue_parser.set_defaults(func=_run_vendor_ctr_decalogue)

    return parser


def almost_main(argv: list[str] | None = None) -> None:
    """Run one subcommand.  ``main_0_mega.py`` calls this with an explicit ``argv``.

    ``argv`` rather than ``sys.argv`` because the mega runs several of these
    subcommands in one process, and blanks ``sys.argv`` before doing so.
    """
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    force_utf8_io()
    almost_main()
