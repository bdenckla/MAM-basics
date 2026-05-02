"""
Meta-orchestrator that runs all (or a selected subset of) processing jobs in
sequence. Useful for a full rebuild from scratch.
"""

import argparse
from dataclasses import dataclass

import main_explicit_xataf

# main_download_mam_fr_google.py
# main_download_mam_fr_sefaria.py
# main_download_mam_fr_wikisource.py
import main_gen_misc_authored_english_documents
import main_decnreub
import main_foi_features_of_interest
import main_multimark
import main_tmpl_survey
import main_wordlist
import main_mam_with_doc
import main_mam_simple
import main_mam4sef
import main_mam_osis
from subcommands import diff_mpp
from subcommands import diff_wsgo
from subcommands import parse_go
from subcommands import parse_ws
from subcommands import ws_bot_proto


@dataclass(frozen=True)
class StepRecord:
    step_id: str
    runner: object
    note: str | None


_STEPS = [
    StepRecord(
        "parse-go",
        parse_go.almost_main,
        "mam_parsed must come before mam_simple, mam_tmpl_survey, & many others",
    ),
    StepRecord(
        "foi-features-of-interest", main_foi_features_of_interest.almost_main, None
    ),
    # We run "features of interest" early since it
    # provides information about any malformed Unicode.
    # On later "main" functions, such malformed Unicode will cause
    # asserts that provide little information.
    StepRecord("mam-with-doc", main_mam_with_doc.almost_main, None),
    StepRecord(
        "diff-mpp",
        diff_mpp.almost_main,
        "writes unnamed unreleased diff report if there are changes",
    ),
    StepRecord(
        "tmpl-survey", main_tmpl_survey.almost_main, "must come after mam_parsed"
    ),
    StepRecord("mam-simple", main_mam_simple.almost_main, "must come after mam_parsed"),
    # mam_simple must come before mam4sef-and-ajf and mam_osis
    StepRecord(
        "mam4sef-and-ajf",
        main_mam4sef.run_both_sef_and_ajf,
        "must come after mam_simple",
    ),
    StepRecord("mam-osis", main_mam_osis.almost_main, "must come after mam_simple"),
    StepRecord("decnreub", main_decnreub.almost_main, None),
    StepRecord("multimark", main_multimark.almost_main, None),
    StepRecord("wordlist", main_wordlist.almost_main, None),
    StepRecord("explicit-xataf", main_explicit_xataf.almost_main, None),
    StepRecord("diff-wsgo", diff_wsgo.almost_main, "relies on download of ws"),
    StepRecord("parse-ws", parse_ws.almost_main, "relies on download of ws"),
    StepRecord("ws-bot-proto", ws_bot_proto.almost_main, "relies on download of ws"),
    StepRecord(
        "gen-misc-authored-english-documents",
        main_gen_misc_authored_english_documents.almost_main,
        None,
    ),
]

_STEP_NAMES = [step.step_id for step in _STEPS]


def main():
    """Run various mains"""
    parser = argparse.ArgumentParser(description="Run the mega pipeline")
    parser.add_argument(
        "--resume-from",
        choices=_STEP_NAMES,
        metavar="STEP",
        help="Skip steps before STEP and resume from there. Choices: "
        + ", ".join(_STEP_NAMES),
    )
    args = parser.parse_args()
    resuming = args.resume_from is not None
    for step in _STEPS:
        if resuming:
            if step.step_id == args.resume_from:
                resuming = False
            else:
                print(f"Skipping {step.step_id}")
                continue
        step.runner()
    #
    # Download of ws (Wikisource) can be accomplished by running:
    #    py/main_download.py fr-wikisource
    # It must be run in a venv like this:
    #    .venv/Scripts/python.exe py/main_download.py fr-wikisource


if __name__ == "__main__":
    main()
