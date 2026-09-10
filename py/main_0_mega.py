"""Run all, or a selected subset, of the processing jobs in sequence.

The sequence combines this repository's processing steps with the wlc steps
that write into this repository's ``out/`` and ``gh-pages/wlc/`` trees. The
five MAM product generators write into this repository after the fourth-stage
Repoint steps completed on 2026-09-10. Two steps use the MAM-private sibling:
the near-Aleppo census still runs there, and the post-stress-meteg survey reads
its Phonetic MAM. A cloud session skips both steps (Ben's decisions,
2026-09-10). Elsewhere both find the sibling through
``mb_cmn.paths.repos_root()``, which in a worktree looks beside the worktree's
home clone, so a worktree run needs no ``REPOS_ROOT``.

Since 2026-09-10 the sequence also runs the five UXLC steps that
``py/main_uxlc_mega.py`` ran until it was folded in here, from
``uxlc-check-changes`` to ``uxlc-word-list``. They write into ``uxlc/``,
``gh-pages/uxlc/`` and ``in/UXLC-misc/``.

Six more steps joined on 2026-09-10, when Ben agreed to add the other offline
generators of tracked files, from ``clc`` to ``map-changes-to-book-of-job``.
They write into ``gh-pages/uxlc/clc/``, ``holman/``, ``gh-pages/holman/``,
``gh-pages/book-of-job/``, ``book-of-job/out/`` and ``uxlc/in/UXLC-misc/``.
Three of them fail the run on purpose, as their notes say:
``render-uxlc-corrections``, ``verify-and-render-table`` and
``book-of-job-site``, the last on any spelling finding in book-of-job's pages.

Also since 2026-09-10, the ``check-mpplus`` step checks MAM-parsed's plus JSON
once ``parse-go`` has written it and ``foi-features-of-interest`` has reported
on it, and fails the run on any error it finds.

Six more generators of tracked files joined the same day, each placed by what
it reads: ``mam-simple-docs``, the doc half of ``py/main_mam_simple.py``, after
``mam-simple``; the two Holman corpus searches after ``wordlist``; and
``diffable-pointed-hebrew``, ``ac-gen-index-flat-annotated`` and
``pipeline-graph``, whose inputs no step writes, between ``gen-site`` and
``vendoring-audit``.

The ``diff-ctr-vs-mam`` step joined the same day, after ``diff-mpp``, once
``py/diff_ctr_vs_mam/massage_mpu_verse.py`` could handle the narrow-sense paseq
template that Proverbs 8:34 has had in MAM-parsed since 2026-03-16.
"""

import argparse
from dataclasses import dataclass
import os
import subprocess
import sys
from typing import Callable

from mb_cmn import bib_locales as tbn
from mb_cmn import graphviz_pin
from mb_cmn import paths
from py_misc import check_mpplus

import main_explicit_xataf

# main_download_mam_fr_google.py
# main_download_mam_fr_wikisource.py
import main_authored
import main_decnreub
import main_diff
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
from subcommands import diff_mpp
from subcommands import diff_wsgo
from subcommands import parse_go
from subcommands import parse_ws
from subcommands import ws_bot_proto
from wlc_cmn.utf8_io import force_utf8_io

# The UXLC steps, folded in from py/main_uxlc_mega.py on 2026-09-10.
import main_amb_early_mtg
import main_fois
import main_uxlc_check_changes
import main_uxlc_word_list
import main_write_page_break_info

# The other offline generators of tracked files, added on 2026-09-10.
import main_clc
import main_estimate_uxlc_locations
import main_gen_misc_authored_english_documents
import main_map_changes_to_book_of_job
import main_render_uxlc_corrections
import main_verify_and_render_table

# The MAM-side and remaining offline generators, added the same day.
import main_ac_gen_index_flat_annotated
import main_diffable_pointed_hebrew
import main_pipeline_graph
import main_search_final_hiriq_verse_text
import main_search_holam_he_qere

_REPOS = paths.repos_root()


@dataclass(frozen=True)
class StepRecord:
    step_id: str
    runner: Callable[[], object]
    note: str | None


def _run_vendored_tmpl_survey_toy():
    subprocess.run(
        [sys.executable, "py-examples/main_tmpl_survey_toy_example.py"],
        cwd=paths.mam_parsed_dir(),
        check=True,
    )


def _run_vendored_letter_small_job():
    subprocess.run(
        [sys.executable, "py-examples/main_letter_small_job_example.py"],
        cwd=paths.repo_root() / "MAM-simple",
        check=True,
    )


def _run_vendored_mam4sef():
    subprocess.run(
        [sys.executable, "py-examples/main_mam4sef_example.py"],
        cwd=paths.repo_root() / "MAM-simple",
        check=True,
    )


def _run_vendored_mam_osis():
    subprocess.run(
        [sys.executable, "py-examples/main_mam_osis_example.py"],
        cwd=paths.repo_root() / "MAM-simple",
        check=True,
    )


def _run_check_mpplus():
    # Added 2026-09-10.  Until then check_mpplus ran only in py/main_download.py fr-google,
    # after a Google download, while parse-go runs the same parse on every mega run and
    # skipped the check that follows it on the download path.  So a change to the parser,
    # or to the check's own rules, reached the plus JSON with nothing checking it.  Ben,
    # 2026-09-10: running it in the mega "also 'checks the check', i.e. makes sure the
    # check itself is still working."  The download path keeps its own call, which exits
    # 1; this one raises, so an error fails the mega run.  The paths are the 24 that
    # parse-go writes, one per book24, so a missing file fails here too.
    plus_dir = paths.mam_parsed_plus_dir()
    plus_paths = [
        plus_dir / f"{tbn.ordered_short_dash_full_24(bk24id)}.json"
        for bk24id in tbn.ALL_BK24_IDS
    ]
    errors = check_mpplus.check_mpplus(plus_paths)
    if errors:
        for plus_path, error in errors:
            print(f"  {error[0]} in {plus_path}: {error[1]!r}")
        raise RuntimeError(
            f"check_mpplus found {len(errors)} error(s) in MAM-parsed's plus/ tree;"
            " each is printed above"
        )
    print(f"check_mpplus: no errors in the {len(plus_paths)} files of {plus_dir}")


def _run_diff_ctr_vs_mam():
    main_diff.almost_main(["ctr-vs-mam"])


# Every step this run skipped because it is running in a cloud session, in order, each with
# the reason it was skipped.  Read by _report_cloud_skips, which reports them once at the
# end of the run, beside graphviz_pin's list of unrendered SVGs.
_CLOUD_SKIPPED_STEPS: list[tuple[str, str]] = []


def _run_near_aleppo_census():
    # Skipped in a cloud session, whether or not MAM-private is attached there.  Ben's
    # decision, 2026-09-10: "the near-aleppo census should be skipped if mega detects
    # that mega is running in the cloud."  Until then a cloud run without MAM-private
    # died here, one step before the post-stress-meteg survey that was already skipped.
    if graphviz_pin.in_cloud_session():
        step_id = "near-aleppo-census"
        reason = (
            "it runs in MAM-private and rewrites that clone's tracked"
            " near-aleppo/census/expected/ goldens, which no later step reads"
        )
        _CLOUD_SKIPPED_STEPS.append((step_id, reason))
        print(
            f"STEP SKIPPED in this cloud session: {step_id}: {reason}", file=sys.stderr
        )
        return
    env = os.environ.copy()
    env["REPO_MAM_PARSED_DIR"] = str(paths.mam_parsed_dir())
    subprocess.run(
        [sys.executable, "near-aleppo/census/run_all.py", "--write"],
        cwd=_REPOS / "MAM-private",
        env=env,
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


def _run_accgram_survey_post_stress_meteg():
    # Skipped altogether in a cloud session, whether or not MAM-private is attached there:
    # Ben's decision, 2026-09-10, on the precedent of the SVG renders graphviz_pin skips in a
    # cloud container.  gen-site then renders from the tracked JSON unchanged.
    if graphviz_pin.in_cloud_session():
        step_id = "accgram-survey-post-stress-meteg"
        reason = (
            "it reads MAM-private's Phonetic MAM; gen-site renders the nine"
            " post-stress-meteg pages from the tracked out/accgram/post-stress-meteg.json,"
            " unchanged"
        )
        _CLOUD_SKIPPED_STEPS.append((step_id, reason))
        print(
            f"STEP SKIPPED in this cloud session: {step_id}: {reason}", file=sys.stderr
        )
        return
    main_accgram.almost_main(["survey-post-stress-meteg"])


def _run_gen_site():
    # --trust-surveys because accgram-survey-post-stress-meteg ran directly above and wrote
    # out/accgram/post-stress-meteg.json, so recomputing the survey here would walk the corpus
    # a second time -- the reason accgram-generate-html is passed --trust-survey.  In a cloud
    # session that step is skipped, and the flag is what keeps gen-site from rebuilding the
    # survey there itself: the nine pages render from the tracked JSON unchanged.
    main_authored.gen_site(trust_surveys=True)


def _run_accgram_generate_html():
    # --trust-survey because accgram-survey-chanted-word-accents ran directly above and wrote
    # out/accgram/chanted-word-accents.json.  Without it the residue page rebuilds that survey,
    # and the mega walks all three corpora twice for a minute it has already spent (#219; Ben's
    # decision, 2026-08-04, over paying the minute twice or leaving the survey out).
    main_accgram.almost_main(["generate-html", "--trust-survey"])


# The three runners below pass their programs' argument lists explicitly, as the
# main_accgram.py runners above do.  Until 2026-09-10 (phase 5c of
# doc/PLAN-mega-coverage.md) each of the three programs read sys.argv by hand, and the
# mega got the mode it runs only because this module's main() blanks sys.argv while the
# steps run.
def _run_clc():
    main_clc.almost_main(["all"])


def _run_find_uxlc_accent_changes():
    main_find_uxlc_accent_changes.almost_main([])


def _run_ac_gen_index_flat_annotated():
    main_ac_gen_index_flat_annotated.almost_main([])


_STEPS = [
    StepRecord(
        "parse-go",
        parse_go.almost_main,
        "mam_parsed must come before mam_simple, mam_tmpl_survey, & many others",
    ),
    # We run "features of interest" early, straight after parse-go, since it
    # provides information about any malformed Unicode.
    # On later "main" functions, such malformed Unicode will cause
    # asserts that provide little information.
    StepRecord(
        "foi-features-of-interest",
        main_foi_features_of_interest.almost_main,
        None,
    ),
    # Since 2026-09-10 (phase 5c of doc/PLAN-mega-coverage.md), check-mpplus follows
    # foi-features-of-interest rather than parse-go directly.  check-mpplus raises on
    # any string out of standard mark order, and such a string is malformed Unicode,
    # which foi-features-of-interest reports as the feature NON_STANDARD_MARK_ORDER;
    # run before foi-features-of-interest, check-mpplus would stop the run before that
    # report was written.  So a doc-note template with the wrong number of arguments
    # stops the run inside foi-features-of-interest, before check-mpplus can report
    # it, at the assert in label_args_of_doc (py/foi/foi_wikitext_helpers.py).  Since
    # phase 6a of the same plan, that assert's message names the template and its
    # argument count, so the order costs no information.
    StepRecord(
        "check-mpplus",
        _run_check_mpplus,
        "must come after parse-go, whose MAM-parsed plus/ JSON it checks, and after"
        " foi-features-of-interest, whose report on malformed Unicode it would"
        " otherwise pre-empt: checks the mark order of every string, and the"
        " arguments of every doc-note template; raises on any error, so a bad parse"
        " fails the mega; writes nothing",
    ),
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
    # Added 2026-09-10, in phase 5c of doc/PLAN-mega-coverage.md.  Until then nothing
    # routine ran py/main_diff.py ctr-vs-mam, and the only commit of
    # out/diff_ctr_mam.json was d86e5779 (2026-03-09).  From 2026-03-16 on, ctr-vs-mam
    # could not complete: Proverbs 8:34 has had the narrow-sense paseq template since
    # MAM-parsed revision 1880cbbd of that day, and
    # py/diff_ctr_vs_mam/massage_mpu_verse.py raised a KeyError on that template until
    # the commit that added this step gave the template a handler.
    StepRecord(
        "diff-ctr-vs-mam",
        _run_diff_ctr_vs_mam,
        "py/main_diff.py ctr-vs-mam: compares Psalms and Proverbs in MAM-parsed's"
        " plus/ tree with the committed CTR JSON under in/chabad-ctr/, and writes"
        " out/diff_ctr_mam.json; must come after parse-go",
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
    # Added 2026-09-10.  The mam-simple step above runs almost_main, the export and the
    # support-file copy, which never reaches the doc half of py/main_mam_simple.py, so
    # until then nothing routine rewrote these docs.  doc/mega-coverage-2026-09-10.md,
    # section 5, records that they had gone stale once.
    StepRecord(
        "mam-simple-docs",
        main_mam_simple.write_generated_docs,
        "py/main_mam_simple.py doc-only: reads MAM-parsed's plus/ tree and rewrites,"
        " each only where its content changed,"
        " MAM-simple/doc/versification-differences.md,"
        " gh-pages/MAM-simple/versification-and-cantillation.html with its CSS and"
        " font, and gh-pages/MAM-simple/index.html; must come after parse-go",
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
        "runs the landed MAM-simple py-examples/main_letter_small_job_example.py as a subprocess; must come after mam_simple",
    ),
    StepRecord(
        "vendored-mam4sef",
        _run_vendored_mam4sef,
        "runs the landed MAM-simple py-examples/main_mam4sef_example.py as a subprocess; must come after mam_simple",
    ),
    StepRecord(
        "vendored-mam-osis",
        _run_vendored_mam_osis,
        "runs the landed MAM-simple py-examples/main_mam_osis_example.py as a subprocess; must come after mam_simple",
    ),
    StepRecord("decnreub", main_decnreub.almost_main, None),
    StepRecord("multimark", main_multimark.almost_main, None),
    StepRecord("wordlist", main_wordlist.almost_main, None),
    # The two Holman corpus searches, added 2026-09-10; until then nothing routine
    # rewrote their tracked reports.  They sit after wordlist because
    # search-holam-he-qere compares its hits with the qere word list that wordlist
    # writes.
    StepRecord(
        "search-final-hiriq-verse-text",
        main_search_final_hiriq_verse_text.main,
        "reads MAM-parsed's plus/ tree; writes"
        " holman/out/final_hiriq_verse_text_report.json",
    ),
    StepRecord(
        "search-holam-he-qere",
        main_search_holam_he_qere.main,
        "must come after wordlist, whose out/mam-qere-words.json it reads with"
        " MAM-parsed's plus/ tree; writes holman/out/holam_he_qere_report.json",
    ),
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
    # Named gen-misc since 2026-09-10, after the py/main_authored.py subcommand it runs.
    # Until then it was gen-misc-authored-english-documents, the file name main_authored.py
    # had until eb18bb71 (2026-05-05).  book-of-job's site generator arrived under that
    # freed module name on 2026-08-19 (ef8e384c), and the shared name let
    # doc/PLAN-evacuate-the-rest-of-three-repos.md count that generator as a mega step when
    # no step ran it.  book-of-job-site, further down, runs it now.
    StepRecord(
        "gen-misc",
        main_authored.almost_main,
        "runs py/main_authored.py gen-misc, which writes the authored documents under"
        " gh-pages/MAM-with-doc/; not py/main_gen_misc_authored_english_documents.py,"
        " which book-of-job-site runs",
    ),
    # The wlc steps, in the order wlc-utils' own mega ran them until it was
    # absorbed here on 2026-08-01.  They are LAST rather than free-standing because
    # accgram reads MAM-simple's json-vtrad-bhs, which mam-simple above regenerates:
    # while the two megas were separate, nothing ordered them, and an accgram run could
    # silently consume a stale MAM-simple.
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
    # The six steps below, and find-uxlc-accent-changes and uxlc-grammar-test further down,
    # joined the mega on 2026-08-04 for the reason accgram-test-fixes did the same morning
    # (#219): each writes a git-tracked artifact, and until now nothing routine rewrote any
    # of them.  Two were already stale when the wiring was done --
    # out/accgram/_grammaticality.txt since 2026-06-29 and out/accgram/uxlc_grammar_test.txt
    # since the METHIGAZAQEF change of #218 -- which is the channel doing exactly what it did
    # to fix-tester.  ~12 s for all eight together.
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
        "must come after mam-simple and wlc-json-and-unicode -- and BEFORE"
        " accgram-generate-html, which is passed --trust-survey on the strength of it",
    ),
    StepRecord(
        "accgram-generate-html",
        _run_accgram_generate_html,
        "must come after accgram-run-prose, accgram-run-poetic and"
        " accgram-survey-chanted-word-accents",
    ),
    # The five UXLC steps, in the order py/main_uxlc_mega.py ran them until Ben agreed on
    # 2026-09-10 to fold that program in here.  It was UXLC-utils' own mega, renamed on
    # arrival, and its reason for standing apart -- that it rebuilt the sibling
    # UXLC-utils' trees -- stopped being true when uxlc/ landed here on 2026-09-03.  The
    # five read only committed inputs, so no step above feeds them.  They sit here because
    # uxlc-check-changes rewrites the in/UXLC-misc/all_changes.json that
    # find-uxlc-accent-changes filters, and until then nothing in the mega rebuilt it.
    StepRecord(
        "uxlc-check-changes",
        main_uxlc_check_changes.main,
        "reads the UXLC change logs under uxlc/in/, in/UXLC-39 and in/lci_recs.json;"
        " writes the canonical in/UXLC-misc/all_changes.json and its derivatives under"
        " uxlc/out/UXLC-misc/; must come before uxlc-fois and find-uxlc-accent-changes",
    ),
    StepRecord(
        "uxlc-fois",
        main_fois.main,
        "reads in/UXLC-39 and in/UXLC-misc/all_changes.json; writes the UXLC features"
        " of interest, JSON and HTML, under gh-pages/uxlc/fois/; must come after"
        " uxlc-check-changes",
    ),
    StepRecord(
        "uxlc-write-page-break-info",
        main_write_page_break_info.main,
        "reads in/UXLC-39 and in/lci_recs.json; writes uxlc/data/lci_augrecs.json, and"
        " lci_augrecs.json, page_counts.json and lci_recs.xml under uxlc/out/UXLC-misc/",
    ),
    StepRecord(
        "uxlc-amb-early-mtg",
        main_amb_early_mtg.main,
        "reads the records in py/uxlc_amb_early_mtg/amb_early_mtg.py, in/UXLC-39 and"
        " in/lci_recs.json; writes the HTML pages under gh-pages/uxlc/amb-early-mtg/",
    ),
    StepRecord(
        "uxlc-word-list",
        main_uxlc_word_list.main,
        "reads in/UXLC-39; writes uxlc/out/uxlc-words.json and"
        " uxlc/out/uxlc-words-fragile.json",
    ),
    # The six steps below joined the mega on 2026-09-10, when Ben agreed to add the other
    # offline generators of tracked files (phase 5a of doc/PLAN-mega-coverage.md); until
    # then nothing routine rewrote what they write.  They sit after the UXLC steps because
    # clc, estimate-uxlc-locations, verify-and-render-table and map-changes-to-book-of-job
    # read the committed UXLC inputs, though none of the six reads what those five steps
    # write.  Where one of the six must follow another step, its note says so.  Three of
    # them fail the mega on purpose: render-uxlc-corrections, verify-and-render-table and
    # book-of-job-site, each for the reason its note gives.
    StepRecord(
        "clc",
        _run_clc,
        "py/main_clc.py all: reads in/UXLC-39 and the note pages and change logs"
        " under uxlc/in/; writes the five pilot jobs' pages, notes JSON and"
        " long-notes pages under gh-pages/uxlc/clc/",
    ),
    StepRecord(
        "estimate-uxlc-locations",
        main_estimate_uxlc_locations.main,
        "reads the derivative of Holman's UXLC-correction emails under holman/emails/,"
        " in/UXLC-39 and in/lci_recs.json; writes holman/data/uxlc_atom_locations.json"
        " and holman/data/uxlc_standard_atoms.json; must come before"
        " render-uxlc-corrections",
    ),
    StepRecord(
        "render-uxlc-corrections",
        main_render_uxlc_corrections.main,
        "must come after estimate-uxlc-locations, whose two JSON files it reads, and"
        " raises unless they cover exactly the cases in holman/emails/; writes"
        " gh-pages/holman/uxlc_corrections.html with its CSS and JS, and"
        " holman/docs-not-served/uxlc_corrections.json",
    ),
    StepRecord(
        "verify-and-render-table",
        main_verify_and_render_table.main,
        "must come after parse-go: checks Holman's ketiv/qere review table against"
        " MAM-parsed's plus/ tree and in/UXLC-39, and raises on any verification"
        " failure; writes its summary into holman/docs-not-served/table_data.json"
        " and the gh-pages/holman/table_data_findings* pages with their CSS and JS",
    ),
    StepRecord(
        "book-of-job-site",
        main_gen_misc_authored_english_documents.main,
        "book-of-job's site generator: reads only committed inputs; deletes and"
        " rewrites the HTML and CSS under gh-pages/book-of-job/ and the generated JSON"
        " under book-of-job/out/; ends in a spell check of those pages that exits 1 on"
        " any spelling, apostrophe or period finding, so such a finding fails the"
        " mega, as doc/PLAN-mega-coverage.md intends",
    ),
    StepRecord(
        "map-changes-to-book-of-job",
        main_map_changes_to_book_of_job.main,
        "must come after book-of-job-site, whose gh-pages/book-of-job/jobn-details/"
        " pages and book-of-job/out/enriched-quirkrecs.json it reads, with"
        " uxlc/in/UXLC-misc/2026.04.01 - Changes.xml; writes"
        " uxlc/in/UXLC-misc/2026.04.01-map-to-book-of-job.json",
    ),
    StepRecord(
        "find-uxlc-accent-changes",
        _run_find_uxlc_accent_changes,
        "py/main_find_uxlc_accent_changes.py without --audit; must come after"
        " uxlc-check-changes, which rewrites the in/UXLC-misc/all_changes.json this"
        " step filters; writes the tracked in/accgram/uxlc_accent_changes.json",
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
    # edition.  MAM-private is a private clone, so outside a cloud session a checkout
    # without it beside this one fails here rather than skipping, which is the choice
    # mb_cmn/paths.py's require_sibling already makes for the other private trees.  A
    # cloud session skips the step, attached clone or not, by Ben's decision of
    # 2026-09-10 that _run_near_aleppo_census quotes.
    StepRecord(
        "near-aleppo-census",
        _run_near_aleppo_census,
        "regenerates near-aleppo/census/expected/ in MAM-private; needs that private"
        " sibling; skipped in a cloud session",
    ),
    # Added 2026-09-10, when Ben decided the survey "should join mega" on two conditions: a
    # worktree run finds MAM-private beside its home clone with no REPOS_ROOT (516a4a1a), and
    # a cloud run skips the survey altogether, which its runner does.  Until then nothing
    # routine rewrote out/accgram/post-stress-meteg.json; the survey was run by hand from
    # main_accgram.py when the corpus moved.  Placed immediately before gen-site, which
    # renders from the JSON it writes, and so after every step that writes MAM-simple, whose
    # xml-vtrad-mam it reads.
    StepRecord(
        "accgram-survey-post-stress-meteg",
        _run_accgram_survey_post_stress_meteg,
        "reads MAM-private's Phonetic MAM and MAM-simple's xml-vtrad-mam, and writes the"
        " tracked out/accgram/post-stress-meteg.json; skipped in a cloud session; must"
        " come before gen-site",
    ),
    # Must come after accgram-survey-post-stress-meteg, since 2026-09-10: it renders the nine
    # post-stress-meteg pages from the JSON that step writes.  Nothing else it reads is
    # written by a step.  That has been so since 2026-08-31, when Ben deleted the landing
    # page's manifest section, DERIVED from the set of tracked gh-pages/<subtree>/index.html,
    # and py/author_site/published_subtrees.py with it; that section was why the step sat
    # after every step writing a subtree.
    StepRecord(
        "gen-site",
        _run_gen_site,
        "writes the eleven deploy-root pages: gh-pages/index.html,"
        " gh-pages/unicode-proposals.html, and nine post-stress-meteg pages from the"
        " survey JSON; must come after accgram-survey-post-stress-meteg",
    ),
    # The three steps below joined on 2026-09-10, with the other offline generators of
    # tracked files that Ben agreed to add; until then nothing routine rewrote what they
    # write.  Each reads only committed inputs that no step writes, so nothing orders
    # them against the steps above: they sit together after gen-site and before the
    # closing audit.
    StepRecord(
        "diffable-pointed-hebrew",
        main_diffable_pointed_hebrew.write_tracked_expansions,
        "reads only committed inputs: expands the two sample inputs under"
        " diffable-pointed-hebrew/ and the two zarqa tables under"
        " misc/zarqa-table-diff/ into the four tracked outputs beside them, the pairs"
        " in py/main_diffable_pointed_hebrew.py's TRACKED_EXPANSIONS",
    ),
    StepRecord(
        "ac-gen-index-flat-annotated",
        _run_ac_gen_index_flat_annotated,
        "py/main_ac_gen_index_flat_annotated.py with no arguments, so with its"
        " default paths: reads only the committed, hand-corrected"
        " aleppo/aleppo-wiki/index-flat-corrected.json; writes"
        " aleppo/index-flat-annotated.json",
    ),
    StepRecord(
        "pipeline-graph",
        main_pipeline_graph.almost_main,
        "writes doc/process-documentation/pipeline.dot and pipeline.svg from the"
        " hand-maintained py/pipeline_graph/pipeline_graph_spec.py, and renders the"
        " hand-written MAM-process.dot to MAM-process.dot.svg; needs the pinned"
        " Graphviz, and a cloud session skips its two SVG renders as it does"
        " tmpl-survey's",
    ),
    # Last, and not because anything above it feeds it: this one AUDITS rather than
    # builds, reading the copied .py files under MAM-simple/py-examples/, and a
    # report reads most naturally as the closing act.  It is here at all because until
    # 2026-08-02 nothing routine ran py/main_vendoring.py, which let it stay outright
    # broken for a day (a deleted wlc-utils scan root) and let its inventory drift
    # since April.  Its three artifacts are git-tracked, so drift now surfaces the way
    # everything else here does -- as an unexplained diff after a rebuild.  ~15s.
    StepRecord(
        "vendoring-audit",
        main_vendoring.almost_main,
        "audits 44 MAM-simple example-support copies; writes"
        " doc/vendoring-inventory.md and out/vendoring_*_out.*",
    ),
]

_STEP_NAMES = [step.step_id for step in _STEPS]


def _report_cloud_skips():
    """Announce, once and at the end, every step and SVG render skipped for the cloud.

    Two kinds of thing are skipped in a cloud session, which
    graphviz_pin.in_cloud_session detects. A cloud container has no Graphviz, so
    the tmpl-survey step skips its renders rather than killing the run -- Ben's
    decision, 2026-09-09; graphviz_pin's docstring has the reasoning. And the two
    steps that use MAM-private are skipped altogether, each by a decision of
    Ben's on 2026-09-10. The near-aleppo-census step runs in MAM-private and
    rewrites that clone's census goldens, which no later step reads. The
    accgram-survey-post-stress-meteg step reads MAM-private's Phonetic MAM and
    is skipped on the precedent of the SVG renders, so gen-site renders the nine
    post-stress-meteg pages from the tracked out/accgram/post-stress-meteg.json,
    unchanged.

    Such a run is CLOUD-COMPLETE, meaning that no step failed, and that every step
    either ran or was skipped for the cloud, while some SVGs may have gone
    unrendered. It is deliberately not called incomplete, and the exit status
    stays 0.

    The banner exists because the skips are printed beside whichever step
    produced them, thousands of lines up by the time a full run ends. It also
    names the one hazard an SVG skip leaves behind, which is not obvious: the
    .dot beside an unrendered .svg IS rewritten, so committing a .dot change
    without its .svg would put the tracked pair out of step -- the very drift
    the Graphviz pin exists to prevent.
    """
    skipped_steps = tuple(_CLOUD_SKIPPED_STEPS)
    skipped_svgs = graphviz_pin.cloud_skipped_renders()
    if not skipped_steps and not skipped_svgs:
        return
    print()
    print("=" * 80)
    print(
        f"  MEGA RUN IS CLOUD-COMPLETE: {len(skipped_steps)} step(s) and "
        f"{len(skipped_svgs)} SVG render(s) skipped for the cloud"
    )
    print("=" * 80)
    print("No step failed. This is a cloud session, so what is listed below was")
    print("skipped rather than run.")
    if skipped_steps:
        print()
        print("STEPS SKIPPED:")
        for step_id, reason in skipped_steps:
            print(f"    {step_id}: {reason}")
    if skipped_svgs:
        print()
        print("SVG RENDERS SKIPPED. This container has no Graphviz, so the SVG files")
        print("below were not re-rendered. Their .dot sources WERE rewritten.")
        print()
        print("  DO NOT COMMIT A CHANGED .dot WITHOUT ITS .svg. The two are a matched")
        print("  pair in the tracked tree, and letting them drift apart is what the")
        print("  Graphviz pin exists to prevent. If `git status` shows no .dot change,")
        print("  nothing was lost and this notice is informational.")
        print()
        for svg_path in skipped_svgs:
            print(f"    {svg_path}")
    print("=" * 80)


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
    _report_cloud_skips()
    #
    # Download of ws (Wikisource) can be accomplished by running:
    #    py/main_download.py fr-wikisource
    # It must be run in a venv like this:
    #    .venv/Scripts/python.exe py/main_download.py fr-wikisource


if __name__ == "__main__":
    main()
