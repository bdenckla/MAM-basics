"""
Meta-orchestrator that runs all (or a selected subset of) processing jobs in
sequence. Useful for a full rebuild from scratch.

Covers both halves of the pipeline: this repo's own steps, which write into
MAM-parsed, MAM-with-doc, MAM-simple, MAM-OSIS and MAM-for-Sefaria, and the wlc
steps at the end, which write into this repo's own out/ and gh-pages/wlc/.
wlc-utils had its own mega until 2026-08-01; the two are one list now so that
accgram cannot read a MAM-simple that mam-simple has not yet regenerated.  The wlc
steps wrote into the wlc-utils clone until 2026-08-12, when the corpus came home
(doc/PLAN-evacuate-the-rest-of-wlc-utils.md, Phases 3 and 5) -- so this mega no
longer writes outside the checkout it runs in, which is what makes a worktree run
of it isolated.
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
import main_sigil_inventory
import main_tmpl_survey
import main_vendoring
import main_wordlist
import main_mam_with_doc
import main_mam_simple
import main_mam4sef
import main_mam_osis
import main_letter_small_job
import main_tmpl_survey_toy

# The wlc half of the pipeline.  Its code moved here on 2026-08-01
# (doc/PLAN-evacuate-python-from-wlc-utils.md) and the corpus it reads and writes
# followed on 2026-08-12 (doc/PLAN-evacuate-the-rest-of-wlc-utils.md).
import main_accgram
import main_find_uxlc_accent_changes
import main_uxlc_grammar_test
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


def _run_near_aleppo_census():
    subprocess.run(
        [sys.executable, "near-aleppo/census/run_all.py", "--write"],
        cwd=_REPOS / "MAM-private",
        check=True,
    )


def _run_accgram_prose():
    main_accgram.almost_main(["run-prose"])


def _run_accgram_test_fixes():
    main_accgram.almost_main(["test-fixes"])


def _run_accgram_dual_cant():
    main_accgram.almost_main(["run-dual-cant"])


def _run_accgram_printed_decalogue():
    main_accgram.almost_main(["run-printed-decalogue"])


def _run_accgram_poetic():
    main_accgram.almost_main(["run-poetic"])


def _run_accgram_xcheck_poetic():
    main_accgram.almost_main(["xcheck-poetic"])


def _run_accgram_servi_xcheck():
    main_accgram.almost_main(["servi-xcheck"])


def _run_accgram_grammaticality():
    main_accgram.almost_main(["grammaticality"])


def _run_accgram_survey_chanted_word_accents():
    main_accgram.almost_main(["survey-chanted-word-accents"])


def _run_accgram_generate_html():
    # --trust-survey because accgram-survey-chanted-word-accents ran directly above and wrote
    # out/accgram/chanted-word-accents.json.  Without it the residue page rebuilds that survey,
    # and the mega walks all three corpora twice for a minute it has already spent (#219; Ben's
    # decision, 2026-08-04, over paying the minute twice or leaving the survey out).
    main_accgram.almost_main(["generate-html", "--trust-survey"])


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
    # run_all, not almost_main, since 2026-08-25.  almost_main is only
    # run_unpinned_latest, so for four months the mega refreshed unpinned-latest on
    # every run while the five NAMED release reports and index.html were rewritten by
    # nobody -- they had gone untouched since 2026-04-21 and were stale by two changes
    # that had landed here meanwhile (the provenance key of 4f3cc11, the
    # nusach_notes -> docnote_notes rename of d205dbb).  The tracked generated artifact
    # is the test in this repo (CLAUDE.md), and that check was simply not running on
    # these eleven files: the giveaway was a committed index.html advertising "11 body
    # text changes" for an unpinned-latest.json that said 0.  ~40s.
    StepRecord(
        "diff-mpp",
        diff_mpp.run_all,
        "every named release from releases.json, plus unpinned-latest and index.html",
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
    # The wlc steps, in the order wlc-utils' own mega ran them until it was
    # absorbed here on 2026-08-01.  They are LAST rather than free-standing because
    # accgram reads MAM-simple's json-vtrad-bhs, which mam-simple above regenerates:
    # while the two megas were separate, nothing ordered them, and an accgram run could
    # silently consume a stale MAM-simple.
    StepRecord(
        "wlc-vendor-uxlc",
        main_wlc_vendor_uxlc.almost_main,
        "refreshes this repo's in/UXLC-39 and in/UXLC-misc from UXLC-utils",
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
    # Not a step wlc-utils' own mega ever had.  Added 2026-08-04 (#219 major 5) after its
    # artifact, wlc-utils' tracked out/accgram/fix-tester/, went stale twice in one window
    # through exactly this gap -- wlc-utils 97c695e's message named the channel and
    # predicted the recurrence.  ~3s.
    StepRecord(
        "accgram-test-fixes",
        _run_accgram_test_fixes,
        "must come after accgram-run-prose; also reads out/wlc422-kq-u, in/UXLC-39 and MAM-simple",
    ),
    # The six steps below, and the two entry points after generate-html, joined the mega on
    # 2026-08-04 for the reason accgram-test-fixes did the same morning (#219): each writes a
    # git-tracked artifact, and until now nothing routine rewrote any of them.  Two were already
    # stale when the wiring was done -- out/accgram/_grammaticality.txt since 2026-06-29 and
    # out/accgram/uxlc_grammar_test.txt since the METHIGAZAQEF change of #218 -- which is the
    # channel doing exactly what it did to fix-tester.  ~12 s for all eight together.
    StepRecord(
        "accgram-run-dual-cant",
        _run_accgram_dual_cant,
        "reads out/wlc422-kq-u and MAM-simple; run after accgram-run-prose (wlc-utils#36)",
    ),
    StepRecord(
        "accgram-run-poetic",
        _run_accgram_poetic,
        "must come after mam-simple and wlc-json-and-unicode",
    ),
    StepRecord(
        "accgram-xcheck-poetic",
        _run_accgram_xcheck_poetic,
        "cross-checks the poetic scanner against MAM-simple; reads out/wlc422-kq-u, not the poetic run",
    ),
    StepRecord(
        "accgram-servi-xcheck",
        _run_accgram_servi_xcheck,
        "same inputs as accgram-xcheck-poetic, per-disjunctive servant instead of segmentation",
    ),
    StepRecord(
        "accgram-grammaticality",
        _run_accgram_grammaticality,
        "must come after BOTH accgram-run-prose and accgram-run-poetic: it estimates its PCFG"
        " over the *_ag.json those two write",
    ),
    StepRecord(
        "accgram-run-printed-decalogue",
        _run_accgram_printed_decalogue,
        "reads only committed inputs (the vendored in/accgram/printed_decalogue_teamim.json"
        " and in/accgram/edition_transcriptions), so nothing above it feeds it",
    ),
    StepRecord(
        "accgram-survey-chanted-word-accents",
        _run_accgram_survey_chanted_word_accents,
        "must come after mam-simple, wlc-vendor-uxlc and wlc-json-and-unicode -- and BEFORE"
        " accgram-generate-html, which is passed --trust-survey on the strength of it",
    ),
    StepRecord(
        "accgram-generate-html",
        _run_accgram_generate_html,
        "must come after accgram-run-prose, accgram-run-poetic and"
        " accgram-survey-chanted-word-accents",
    ),
    StepRecord(
        "find-uxlc-accent-changes",
        main_find_uxlc_accent_changes.main,
        "must come after wlc-vendor-uxlc, whose in/UXLC-misc/all_changes.json it filters;"
        " writes the tracked in/accgram/uxlc_accent_changes.json",
    ),
    StepRecord(
        "uxlc-grammar-test",
        main_uxlc_grammar_test.main,
        "must come after find-uxlc-accent-changes, whose JSON it reads, and after"
        " wlc-json-and-unicode",
    ),
    StepRecord("wlc-diffs-420422", main_wlc_diffs_420422.almost_main, None),
    StepRecord("wlc-a-notes", main_wlc_a_notes.almost_main, None),
    # The sigil inventory reads MAM-parsed's plus/ tree too, so it takes the same placement
    # argument the near-aleppo comment just below makes: after parse-go and after everything
    # else that writes MAM-parsed.  Added 2026-08-27, for the reason accgram-test-fixes was
    # added on 2026-08-04 and near-aleppo-census on 2026-08-26 -- py/main_sigil_inventory.py
    # was imported by nothing, so nothing routine rewrote its tracked artifact.  This one had
    # already gone stale, and provably so twice over: out/sigil-inventory.json had exactly one
    # commit in its history, c14122a of 2026-04-07, and d205dbb changed this generator's own
    # header description string on 2026-05-21 while the committed JSON kept the old spelling.
    # So the file was three months stale on a string alone, before any corpus change was
    # counted.  The rebuild moved every header count -- notes_scanned 3847 -> 3863,
    # distinct_expressions 1711 -> 1721, distinct_expression_tokens 2363 -> 2371,
    # distinct_prose_tokens 667 -> 678 -- and 5,536 lines of the 73,847-line file.  ~1.5s.
    StepRecord(
        "sigil-inventory",
        main_sigil_inventory.almost_main,
        "reads MAM-parsed's plus/ tree; writes the tracked out/sigil-inventory.json",
    ),
    # The near-aleppo censuses read MAM-parsed's plus/ tree, so this belongs after
    # parse-go and after everything else that writes it.  --write regenerates their
    # tracked goldens under near-aleppo/census/expected/, which is a build and not an
    # audit: run_all.py's own default mode diffs instead, and that mode is for a human
    # asking "what moved?", not for a rebuild.  Without a step here the goldens go
    # stale silently, and the next session to run run_all.py meets a wall of red it
    # has to explain from history.  Added 2026-08-26, the day exactly that happened:
    # a Google Sheet download moved plus/ and 24 of the 82 censuses went red at once.
    # TEMPORARY, by Ben's decision the same day -- at some point the censuses stop
    # running here and this step becomes the real generator of the near-aleppo
    # edition.  MAM-private is a private clone, so a checkout without it beside this
    # one fails here rather than skipping, which is the choice mb_cmn/paths.py's
    # require_sibling already makes for the other private trees.
    StepRecord(
        "near-aleppo-census",
        _run_near_aleppo_census,
        "regenerates near-aleppo/census/expected/ in MAM-private; needs that private sibling",
    ),
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
