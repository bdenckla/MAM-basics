"""
Meta-orchestrator that runs all (or a selected subset of) processing jobs in
sequence. Useful for a full rebuild from scratch.

Covers both halves of the pipeline: this repo's own steps, which write into
MAM-parsed, MAM-with-doc, MAM-simple, MAM-OSIS and MAM-for-Sefaria, and the
wlc-utils steps at the end, which write into wlc-utils' out/ and gh-pages/.
wlc-utils had its own mega until 2026-08-01; the two are one list now so that
accgram cannot read a MAM-simple that mam-simple has not yet regenerated.
"""

import argparse
from dataclasses import dataclass
import subprocess
import sys
from typing import Callable

from mb_cmn import paths

import main_explicit_xataf

# main_download_mam_fr_google.py
# main_download_mam_fr_sefaria.py
# main_download_mam_fr_wikisource.py
import main_authored
import main_decnreub
import main_foi_features_of_interest
import main_multimark
import main_tmpl_survey
import main_vendoring
import main_wordlist
import main_mam_with_doc
import main_mam_simple
import main_mam4sef
import main_mam_osis
import main_letter_small_job
import main_tmpl_survey_toy

# The wlc-utils half of the pipeline.  Its code lives here; the corpus it reads and
# writes stayed in wlc-utils (see wlc_paths, and
# doc/PLAN-evacuate-python-from-wlc-utils.md).
import main_accgram
import main_wlc_a_notes
import main_wlc_diffs_420422
import main_wlc_json_and_unicode
import main_wlc_vendor_uxlc
from subcommands import diff_mpp
from subcommands import diff_wsgo
from subcommands import parse_go
from subcommands import parse_ws
from subcommands import ws_bot_proto
from wlc_cmn.utf8_io import force_utf8_io

_REPOS = paths.repos_root()


@dataclass(frozen=True)
class StepRecord:
    step_id: str
    runner: Callable[[], object]
    note: str | None


def _run_vendored_tmpl_survey_toy():
    subprocess.run(
        [sys.executable, "py-examples/main_tmpl_survey_toy_example.py"],
        cwd=_REPOS / "MAM-parsed",
        check=True,
    )


def _run_vendored_letter_small_job():
    subprocess.run(
        [sys.executable, "py-examples/main_letter_small_job_example.py"],
        cwd=_REPOS / "MAM-simple",
        check=True,
    )


def _run_vendored_mam4sef():
    subprocess.run(
        [sys.executable, "py-examples/main_mam4sef_example.py"],
        cwd=_REPOS / "MAM-simple",
        check=True,
    )


def _run_vendored_mam_osis():
    subprocess.run(
        [sys.executable, "py-examples/main_mam_osis_example.py"],
        cwd=_REPOS / "MAM-simple",
        check=True,
    )


def _run_accgram_prose():
    main_accgram.almost_main(["run-prose"])


def _run_accgram_poetic():
    main_accgram.almost_main(["run-poetic"])


def _run_accgram_generate_html():
    main_accgram.almost_main(["generate-html"])


_STEPS = [
    StepRecord(
        "parse-go",
        parse_go.almost_main,
        "mam_parsed must come before mam_simple, mam_tmpl_survey, & many others",
    ),
    StepRecord(
        "foi-features-of-interest",
        main_foi_features_of_interest.almost_main,
        None,
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
        "tmpl-survey",
        main_tmpl_survey.almost_main,
        "must come after mam_parsed",
    ),
    StepRecord(
        "tmpl-survey-toy",
        main_tmpl_survey_toy.almost_main,
        "must come after parse-go",
    ),
    StepRecord(
        "vendored-tmpl-survey-toy",
        _run_vendored_tmpl_survey_toy,
        "runs MAM-parsed/py-examples/main_tmpl_survey_toy_example.py as subprocess; must come after parse-go",
    ),
    StepRecord(
        "mam-simple",
        main_mam_simple.almost_main,
        "must come after mam_parsed",
    ),
    # mam_simple must come before mam4sef-and-ajf and mam_osis
    StepRecord(
        "mam4sef-and-ajf",
        main_mam4sef.run_both_sef_and_ajf,
        "must come after mam_simple",
    ),
    StepRecord(
        "mam-osis",
        main_mam_osis.almost_main,
        "must come after mam_simple",
    ),
    StepRecord(
        "letter-small-job",
        main_letter_small_job.almost_main,
        "must come after mam_simple",
    ),
    StepRecord(
        "vendored-letter-small-job",
        _run_vendored_letter_small_job,
        "runs MAM-simple/py-examples/main_letter_small_job_example.py as subprocess; must come after mam_simple",
    ),
    StepRecord(
        "vendored-mam4sef",
        _run_vendored_mam4sef,
        "runs MAM-simple/py-examples/main_mam4sef_example.py as subprocess; must come after mam_simple",
    ),
    StepRecord(
        "vendored-mam-osis",
        _run_vendored_mam_osis,
        "runs MAM-simple/py-examples/main_mam_osis_example.py as subprocess; must come after mam_simple",
    ),
    StepRecord("decnreub", main_decnreub.almost_main, None),
    StepRecord("multimark", main_multimark.almost_main, None),
    StepRecord("wordlist", main_wordlist.almost_main, None),
    StepRecord(
        "explicit-xataf",
        main_explicit_xataf.almost_main,
        None,
    ),
    StepRecord(
        "diff-wsgo",
        diff_wsgo.almost_main,
        "relies on download of ws",
    ),
    StepRecord(
        "parse-ws",
        parse_ws.almost_main,
        "relies on download of ws",
    ),
    StepRecord(
        "ws-bot-proto",
        ws_bot_proto.almost_main,
        "relies on download of ws",
    ),
    StepRecord(
        "gen-misc-authored-english-documents",
        main_authored.almost_main,
        None,
    ),
    # The wlc-utils steps, in the order wlc-utils' own mega ran them until it was
    # absorbed here on 2026-08-01.  They are LAST rather than free-standing because
    # accgram reads MAM-simple's json-vtrad-bhs, which mam-simple above regenerates:
    # while the two megas were separate, nothing ordered them, and an accgram run could
    # silently consume a stale MAM-simple.
    StepRecord(
        "wlc-vendor-uxlc",
        main_wlc_vendor_uxlc.almost_main,
        "refreshes wlc-utils' in/UXLC-39 and in/UXLC-misc from UXLC-utils",
    ),
    StepRecord(
        "wlc-json-and-unicode",
        main_wlc_json_and_unicode.almost_main,
        "must come before accgram, which reads out/wlc422-kq-u",
    ),
    StepRecord(
        "accgram-run-prose",
        _run_accgram_prose,
        "must come after mam-simple and wlc-json-and-unicode",
    ),
    StepRecord(
        "accgram-run-poetic",
        _run_accgram_poetic,
        "must come after mam-simple and wlc-json-and-unicode",
    ),
    StepRecord(
        "accgram-generate-html",
        _run_accgram_generate_html,
        "must come after accgram-run-prose and accgram-run-poetic",
    ),
    StepRecord("wlc-diffs-420422", main_wlc_diffs_420422.almost_main, None),
    StepRecord("wlc-a-notes", main_wlc_a_notes.almost_main, None),
    # Last, and not because anything above it feeds it: this one AUDITS rather than
    # builds, reading the vendored .py copies as they sit in the sibling repos, and a
    # report reads most naturally as the closing act.  It is here at all because until
    # 2026-08-02 nothing routine ran py/main_vendoring.py, which let it stay outright
    # broken for a day (a deleted wlc-utils scan root) and let its inventory drift
    # since April.  Its three artifacts are git-tracked, so drift now surfaces the way
    # everything else here does -- as an unexplained diff after a rebuild.  ~15s.
    StepRecord(
        "vendoring-audit",
        main_vendoring.almost_main,
        "scans every sibling repo on disk; writes doc/vendoring-inventory.md and out/vendoring_*_out.*",
    ),
]

_STEP_NAMES = [step.step_id for step in _STEPS]


def main():
    """Run various mains"""
    # The wlc steps emit Hebrew.  Their own `if __name__ == "__main__"` blocks called
    # this and no longer run now that they are in-process steps, and on Windows a
    # redirected stdout encodes with cp1252, so without this the first Hebrew print
    # raises UnicodeEncodeError whenever the mega is run into a file or a pipe.
    force_utf8_io()
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
    old_argv = sys.argv
    try:
        # Isolate mega CLI flags from child parsers in step scripts.
        sys.argv = [old_argv[0]]
        for step in _STEPS:
            if resuming:
                if step.step_id == args.resume_from:
                    resuming = False
                else:
                    print(f"Skipping {step.step_id}")
                    continue
            step.runner()
    finally:
        sys.argv = old_argv
    #
    # Download of ws (Wikisource) can be accomplished by running:
    #    py/main_download.py fr-wikisource
    # It must be run in a venv like this:
    #    .venv/Scripts/python.exe py/main_download.py fr-wikisource


if __name__ == "__main__":
    main()
