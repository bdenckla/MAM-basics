"""Guard: every program is run by py/main_0_mega.py, or declared here with its reason.

WHY THIS EXISTS

Ben's instructions of 2026-09-10: "Everything that is not part of mega should have a
recorded justification as to why it is not in mega", and "It should be part of repo
maintenance (if it is not already) to check that the only programs not part of mega are
those that have documented justifications for why they are not part of mega."  The
design is section 7 of ``doc/mega-coverage-2026-09-10.md``, which Ben agreed to that
day; this file is phase 7 of ``doc/PLAN-mega-coverage.md``.  It is part of maintenance
with no wiring of its own: ``py/main_repo_maintenance.py`` runs the suite at its step 5,
before its step 6 runs the mega.

This is a mechanical lint over the tree, the second of the two test shapes CLAUDE.md
sanctions, and it follows ``py/tests/test_sibling_reach.py``: an AST pass rather than a
grep, a declaration that says why rather than a count, a hard failure for any site the
scan cannot resolve, and a dead-entry check on every declaration table.

WHAT COUNTS AS A PROGRAM

Every tracked ``.py`` outside ``py/tests/`` with a module-level
``if __name__ == "__main__":`` block, found by AST rather than by file name, since
``check_*.py`` and ``fix_*.py`` are programs too.  That includes the example scripts
under ``MAM-simple/py-examples/`` and ``MAM-parsed/py-examples/``.  A program with
argparse subcommands counts as one program per subcommand, keyed
``"<path> <subcommand>"``, and not as a program of its own.  A subcommand name built
from a table, as ``py/main_accgram.py`` builds ``generate-html-<name>`` from
``_HTML_GENERATORS``, is read from that table; a name the scan cannot read fails.

WHAT COUNTS AS RUN BY THE MEGA

What the runners of ``_STEPS`` in ``py/main_0_mega.py`` call, read from its source:

* any function of an imported entry module that has no subcommands: that program;
* ``almost_main([...])`` of an entry module that has subcommands, the list naming the
  subcommand: that subcommand;
* a script path in the argument list of a subprocess: the program at that path;
* a call listed in ``_RUNNER_CALLS``, which names the program or programs it runs,
  for the calls whose program the scan cannot name from the call alone.

A call into an entry module with subcommands that neither names its subcommand nor is
listed fails.  A call into any other module is library code and is ignored: if one runs
a program after all, that program is reported as neither run nor declared.

MODES, WHICH THE SCAN CANNOT SEE

A mode chosen by flags or arguments is invisible to a scan of calls.  So where the mega
runs one mode of a program and not another, the other mode is declared by hand, keyed
``"<program> <mode>"``: ``"py/main_find_uxlc_accent_changes.py --audit"``, or
``"py/main_accgram.py generate-html without --trust-survey"`` for the form lacking a
flag the mega passes.  A mode's program must exist, and each ``--flag`` its key names
must still be defined by an ``add_argument`` call in the program's file or in a module
that file imports, or the entry is dead.  The modes declared are those sections 3 and 4
of the analysis name.  A flag that only narrows a job the mega runs whole (``--book39``,
``--section6``, ``--book``, ``--target``), points it at other paths (``--emails-dir``,
``INPUT OUTPUT``), or changes only what it prints (``--verbose``) is not declared as a
mode.  Whether the mega has begun to run a declared mode is checked only where a step
spells out the program's arguments.

WHAT FAILS

1. A program the mega does not run and ``NOT_IN_MEGA`` does not declare.
2. A declaration whose program, subcommand or flag is gone, and an entry of
   ``_RUNNER_CALLS`` or ``_EXTERNAL_SCRIPTS`` that nothing uses any more.
3. A declaration whose program the mega now runs.

WHERE THE REASONS COME FROM

Each reason says why the mega leaves the program out, and where that is recorded.  A
reason beginning "Claude-written proposal, not yet reviewed by Ben" has no record but
the proposal: most were proposed in section 4 of the analysis.  When Ben accepts or
changes one, delete that marker and cite his decision.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_mega_coverage.py
"""

from __future__ import annotations

import ast
import functools
import subprocess
from dataclasses import dataclass

from mb_cmn import paths

# ---------------------------------------------------------------------------
# Reasons shared by several programs.  The first group is section 3 of
# doc/mega-coverage-2026-09-10.md: a reason already written down elsewhere.
# ---------------------------------------------------------------------------
_ACCGRAM_SINGLE = (
    "One report of the batch that the accgram-generate-html step runs whole."
    ' Recorded in doc/review-findings-2026-08-03.md ("the generate-html-<name> singles'
    ' the batch covers") and doc/mega-coverage-2026-09-10.md §3.'
)
_EDITION_HAND_WORK = (
    "Interactive work on printed-edition scans, most of it reading a personal scan"
    " archive outside every repository.  Recorded in py/main_edition_transcription.py's"
    ' docstring ("The interactive, machine-local half of the printed-Decalogue work")'
    " and doc/mega-coverage-2026-09-10.md §3."
)
_ALEPPO_HAND_WORK = (
    "Interactive hand work on the Aleppo Codex page images.  Recorded in py/ac_paths.py,"
    " aleppo/README.md, aleppo/doc/aleppo-line-breaks.md and"
    " doc/mega-coverage-2026-09-10.md §3."
)
_CAM1753_HAND_WORK = (
    "Interactive hand work on the Cambridge 1753 images.  Recorded in"
    " cam1753/doc/cam1753-line-break-task.md, py/cam1753_paths.py,"
    " doc/boj-cam1753-word-crops.md, doc/book-of-job-artifacts.md and"
    " doc/mega-coverage-2026-09-10.md §3."
)
_PER_MANUSCRIPT_CHECK = (
    "A per-manuscript check, run by hand.  Recorded in cam1753/CLAUDE.md, which calls"
    " check_cam1753_all.py the artifact oracle, in"
    " doc/PLAN-evacuate-public-repos-programme.md, and in"
    " doc/mega-coverage-2026-09-10.md §3."
)
_HOLMAN_MAILBOX = (
    "Reads Holman's untracked mailboxes under .novc/; the reports regenerate from the"
    " tracked derivatives, which the mega's Holman steps read.  Recorded in"
    ' doc/PLAN-evacuate-the-rest-of-three-repos.md ("neither is needed to'
    " regenerate\"), CLAUDE.md's section on Holman's mailboxes, and"
    " doc/mega-coverage-2026-09-10.md §3."
)
_NETWORK_VENDORING = (
    "A network tool that refreshes a vendored snapshot, from Hebrew Wikisource or from"
    " chabad.org.  Recorded in py/main_accgram.py's docstring (\"NETWORK AUTHOR TOOL,"
    ' run by hand") and doc/mega-coverage-2026-09-10.md §3.'
)
_REDIRECT_STUBS = (
    "Frozen redirect stubs, with or without --publish; publishing needs a temporary"
    ' clone of a redirect host.  Recorded in CLAUDE.md ("Nothing schedules the'
    ' program") and doc/mega-coverage-2026-09-10.md §3.'
)

# ---------------------------------------------------------------------------
# Reasons shared by several programs, second group: section 4 of the analysis,
# proposals with no other record.
# ---------------------------------------------------------------------------
_CHECK_WRITES_NOTHING = (
    "Claude-written proposal, not yet reviewed by Ben: a check that writes nothing;"
    " py/check_all.py runs it by hand, and the suite runs the deploy-root mode of"
    " py/check_html_syntax_and_sanity.py.  Proposed in doc/mega-coverage-2026-09-10.md"
    " §4."
)
_VENDORING_PART = (
    "Claude-written proposal, not yet reviewed by Ben: one part of the --all audit"
    " that the vendoring-audit step runs.  Proposed in doc/mega-coverage-2026-09-10.md"
    " §4."
)

# ---------------------------------------------------------------------------
# A reason shared by two programs, from a decision of Ben's.
# ---------------------------------------------------------------------------
_LINE_BREAK_REPORT = (
    "Ben's decision, 2026-09-10: the line-break reports stay out of the mega, since the"
    ' fine-grained indexing they check "served its purpose for the book-of-job'
    ' project".  Recorded in doc/mega-coverage-2026-09-10.md §1, decision 4(c), and'
    " phase 7 of doc/PLAN-mega-coverage.md."
)

# ---------------------------------------------------------------------------
# THE DECLARATION.  Every program the mega does not run, keyed as the module
# docstring says, with why the mega leaves it out and where that is recorded.
#
# ADDING A STEP FOR ONE OF THESE?  Delete its entry here: the check fails
# naming it otherwise, so a stale reason cannot outlive the step that ended it.
# ---------------------------------------------------------------------------
NOT_IN_MEGA: dict[str, str] = {
    # --- Section 3 of doc/mega-coverage-2026-09-10.md: reasons already recorded.
    "py/main_accgram.py survey-breuer-zaqef-units": (
        "A measurement written only to .novc/, which also reads MAM-private's Phonetic"
        " MAM.  Recorded in py/accgram/breuer_word_length.py's docstring (\"WRITES TO"
        ' ``.novc/``, not to ``out/``") and doc/mega-coverage-2026-09-10.md §3.'
    ),
    "py/main_accgram.py vendor-printed-decalogue": _NETWORK_VENDORING,
    "py/main_accgram.py vendor-ctr-decalogue": _NETWORK_VENDORING,
    "py/main_accgram.py generate-html without --trust-survey": (
        "The batch the accgram-generate-html step runs, except that its residue page"
        " rebuilds the survey the accgram-survey-chanted-word-accents step has just"
        " written.  Recorded in py/main_0_mega.py, the comment in"
        " _run_accgram_generate_html, and doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_accgram.py generate-html-poetic": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-goerwitz": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-almost-errors": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-supplied-marks": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-printed-decalogue": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-printed-decalogue-simanim": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-maqaf-nonfinal-accents": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-printed-decalogue-koren": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-printed-decalogue-uvinkha": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-dual-under-bars-in-leningrad-decalogues": (
        _ACCGRAM_SINGLE
    ),
    "py/main_accgram.py generate-html-telg-doc-notes": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-ps17v14-mam-doc-notes": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-ps17v14-double-tsinnor": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-wlc-chanted-word-residue": _ACCGRAM_SINGLE,
    "py/main_accgram.py generate-html-wlc-chanted-word-residue without --trust-survey": (
        "The same page with its survey rebuilt.  Recorded in"
        " py/accgram/wlc_chanted_word_residue_page.py's docstring (\"READING THAT JSON"
        ' INSTEAD IS WHAT ``--trust-survey`` IS FOR") and'
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_authored.py gen-site without --trust-surveys": (
        "It rebuilds the post-stress-meteg survey that the"
        " accgram-survey-post-stress-meteg step has just written, so the mega passes"
        " --trust-surveys and gen-site renders from that step's JSON.  Recorded in"
        " py/main_0_mega.py, the comment in _run_gen_site, and py/main_authored.py, the"
        " comment above _SURVEY_READING_PAGES.  doc/mega-coverage-2026-09-10.md §3 gives"
        " the reason as it stood before phase 2 of doc/PLAN-mega-coverage.md put the"
        " survey in the mega."
    ),
    "py/main_edition_transcription.py scan-page": _EDITION_HAND_WORK,
    "py/main_edition_transcription.py editor": _EDITION_HAND_WORK,
    "py/main_edition_transcription.py zoom-line": _EDITION_HAND_WORK,
    "py/main_edition_transcription.py highlight-picker": _EDITION_HAND_WORK,
    "py/main_edition_transcription.py build": (
        "Its plain form wraps the line editor's downloaded exports, named with --export,"
        " into the committed JSON: the last step of interactive transcription.  Recorded"
        " in py/main_edition_transcription.py's docstring and"
        ' doc/mega-coverage-2026-09-10.md §3, as "build with --export".'
    ),
    "py/main_edition_transcription.py build --check": (
        "Writes nothing.  Recorded in py/main_edition_transcription.py's docstring, in"
        " py/accgram/transcription_build.py's, which names"
        " py/tests/test_edition_transcriptions.py as the check over every stem, and in"
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_edition_transcription.py build --derive-only": (
        "Re-derives each stem's tracked .txt from its tracked JSON, and the suite already"
        " fails on any drift between the two.  Recorded in"
        " py/accgram/transcription_build.py's docstring and"
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_edition_transcription.py check": (
        "Checks a hand transcription before it is committed, and writes nothing."
        "  Recorded in py/main_edition_transcription.py's docstring and"
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_diff.py mpp --legacy-history": (
        "Reads a sibling MAM-parsed clone that belongs on no machine.  Recorded in"
        " py/subcommands/diff_mpp.py's docstring, CLAUDE.md, and"
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_download.py fr-google": (
        "A network download from Google Sheets, with or without --download-only, run"
        " when the upstream moves.  Recorded in doc/process-documentation/pipeline.dot"
        ' ("External prerequisites (not part of _STEPS)") and'
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_download.py fr-wikisource": (
        "A network download from Hebrew Wikisource, run when the upstream moves."
        '  Recorded in doc/process-documentation/pipeline.dot ("External prerequisites'
        " (not part of _STEPS)\"), the closing comment of py/main_0_mega.py's main(),"
        " and doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_download.py fr-ws-intro": (
        "A network download of Hebrew Wikisource's introduction to MAM, which nothing"
        " downstream reparses.  Recorded in CLAUDE.md's section on in/mam-ws-intro/ and"
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_ws_bot.py real --no-save": (
        "Reads live Wikisource pages through the bot's login.  Recorded in"
        " doc/PLAN-holman-meteg-rollout-programme.md and"
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_ws_bot.py proto --edits <file>": (
        "A rehearsal of one edit file before a real save; the ws-bot-proto step runs"
        " proto without --edits.  Recorded in doc/PLAN-holman-meteg-rollout-programme.md"
        " and doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_slide_generator.py render-slides": (
        "Needs Playwright with headless Chromium, which"
        " py/slide_generator/json_snippet_browser.py launches, and the Windows font"
        " directory, which py/slide_generator/slide_render.py reads.  Recorded in"
        " doc/mega-coverage-2026-09-10.md §3, which cites"
        " misc/what-is-mam/img/provenance-misc.md for the what-is-mam deck."
    ),
    "py/main_uxlc_download_changes.py": (
        "A network download of UXLC from tanach.us.  Recorded in"
        " py/main_clc_download_notes.py's docstring, which names it as the network half"
        " of the UXLC build, and doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_clc.py <BookId> [chapter]": (
        "One book or one chapter, for focused work; the clc step runs the all form, every"
        " pilot page.  Recorded in py/main_clc.py's docstring,"
        " doc/mega-coverage-2026-09-10.md §3, and phase 7 of doc/PLAN-mega-coverage.md."
    ),
    "py/main_clc_download_notes.py": (
        'A network download of UXLC\'s note pages, "NOT part of the default build".'
        "  Recorded in its docstring and doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_ingest_uxlc_emails.py": _HOLMAN_MAILBOX,
    "py/main_ingest_mam_suggestions.py": _HOLMAN_MAILBOX,
    "py/main_verify_notes_zip.py": (
        "A verification aid against a downloaded zip outside every repository."
        "  Recorded in its docstring and doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_ac_find_word_in_images.py": _ALEPPO_HAND_WORK,
    "py/main_ac_gen_col_quad_editor.py": _ALEPPO_HAND_WORK,
    "py/main_ac_gen_lb_flat_stream.py": _ALEPPO_HAND_WORK,
    "py/main_ac_gen_line_break_editor.py": _ALEPPO_HAND_WORK,
    "py/main_ac_download_pages.py": (
        "A network download of Aleppo Codex page images from archive.org.  Recorded in"
        " its docstring and doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_cam1753_download_spreads.py": (
        "A network download of Cambridge 1753 spreads from archive.org.  Recorded in"
        " py/py_cam1753_loc/download_spreads.py's docstring and"
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_cam1753_find_word_in_images.py": _CAM1753_HAND_WORK,
    "py/main_cam1753_gen_col_quad_editor.py": _CAM1753_HAND_WORK,
    "py/main_cam1753_gen_flat_stream.py": _CAM1753_HAND_WORK,
    "py/main_cam1753_gen_line_break_editor.py": _CAM1753_HAND_WORK,
    "py/main_gen_cam1753_crop_editor.py": _CAM1753_HAND_WORK,
    "py/main_apply_cam1753_crops.py": _CAM1753_HAND_WORK,
    "py/main_cam1753_gutter_profile.py": (
        "Its chart is not reproducible across matplotlib versions.  Recorded in"
        " cam1753/CLAUDE.md and doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_cam1753_split_spreads.py": (
        "Regenerates the untracked page JPEGs when an editor or crop task needs them; its"
        " tracked split records do not move.  Recorded as Ben's decision of 2026-09-04"
        " in doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md, in"
        " cam1753/CLAUDE.md, and in doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_list_missing_aleppo_imgs.py": (
        'A console report only.  Recorded in doc/book-of-job-artifacts.md ("Console'
        ' output only") and doc/mega-coverage-2026-09-10.md §3.'
    ),
    "py/check_ac_all.py": _PER_MANUSCRIPT_CHECK,
    "py/check_cam1753_all.py": _PER_MANUSCRIPT_CHECK,
    "py/check_cam1753_word_finding.py": _PER_MANUSCRIPT_CHECK,
    "py/main_test.py": (
        "The suite, which MAM-basics' maintenance runs at its step 5, just before its"
        " step 6 runs the mega.  Recorded in py/main_repo_maintenance.py's docstring and"
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_repo_util.py": (
        "Cross-repository maintenance, all six actions; --commit-across-repos is barred"
        " from the sweep.  Recorded in doc/PLAN-repo-maintenance-across-GitRepos.md and"
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_repo_maintenance.py": (
        "MAM-basics' maintenance, whose step 6 runs the mega.  Recorded in its docstring"
        " and doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/main_redirect_stubs.py build": _REDIRECT_STUBS,
    "py/main_redirect_stubs.py check": _REDIRECT_STUBS,
    "py/check_mark_order.py": (
        "A source check over file types the suite's lint does not cover, run by hand."
        "  Recorded in CLAUDE.md's section on mark order and"
        " doc/mega-coverage-2026-09-10.md §3."
    ),
    "py/fix_escape_sequences.py": (
        "The fixer py/check_escape_sequences.py points to, run by hand, as a dry run or"
        ' with --apply.  Recorded in py/check_escape_sequences.py ("Run'
        ' fix_escape_sequences.py to replace these") and doc/mega-coverage-2026-09-10.md'
        " §3."
    ),
    # --- Section 4 of the analysis: Claude-written proposals, not yet reviewed by Ben.
    "py/main_find_uxlc_accent_changes.py --audit": (
        "Claude-written proposal, not yet reviewed by Ben: it prints coverage counts and"
        " writes nothing, where the find-uxlc-accent-changes step runs the form that"
        " writes in/accgram/uxlc_accent_changes.json.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4; phase 7 of doc/PLAN-mega-coverage.md"
        " names this mode."
    ),
    "py/main_scan_pages.py survey": (
        "Claude-written proposal, not yet reviewed by Ben: it reads the personal scan"
        " archive, which is on no other machine, so it is rerun by hand when a scan"
        " folder changes.  Proposed in doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_scan_pages.py check": (
        "Claude-written proposal, not yet reviewed by Ben: it writes nothing, and"
        " py/tests/test_scan_pages_index.py runs the same check.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_parse.py ws --write-fmt-1": (
        "Claude-written proposal, not yet reviewed by Ben: debugging output to .novc/;"
        " the tracked half of the run is the parse-ws step's.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_diff.py mpp --old A --new B": (
        "Claude-written proposal, not yet reviewed by Ben: a one-off comparison of two"
        " revisions someone picks, where the diff-mpp step rebuilds every named release."
        "  Proposed in doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_download.py fr-google --skip-download": (
        "Claude-written proposal, not yet reviewed by Ben: it runs the parse the parse-go"
        " step runs, then the check the check-mpplus step has run since phase 5b of"
        " doc/PLAN-mega-coverage.md; the comment on _run_check_mpplus in"
        " py/main_0_mega.py records that overlap.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4, before that step existed."
    ),
    "py/main_ws_bot.py real": (
        "Claude-written proposal, not yet reviewed by Ben: it saves edits to live Hebrew"
        " Wikisource under Ben's bot account, so every run is a deliberate act."
        "  Proposed in doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_ws_bot.py real --identity-run": (
        "Claude-written proposal, not yet reviewed by Ben: it exercises the live-wiki"
        " plumbing, and needs the network and the bot login.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_tmpl_survey.py --write-expanded-stack-grammar-lock": (
        "Claude-written proposal, not yet reviewed by Ben: every survey run is checked"
        " against the locks, so rewriting them on every run would make that check pass"
        " by construction.  Proposed in doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_tmpl_survey.py --find-stack-path": (
        "Claude-written proposal, not yet reviewed by Ben: a lookup that prints and"
        " writes nothing; --find-stack-path-verbose is the same lookup with more"
        " context.  Proposed in doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_foi_features_of_interest.py --foi <name>": (
        "Claude-written proposal, not yet reviewed by Ben: a subset of the"
        " foi-features-of-interest step's full run.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_foi_features_of_interest.py --single-threaded": (
        "Claude-written proposal, not yet reviewed by Ben: a debugging variant of the"
        " foi-features-of-interest step's full run.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_vendoring.py --compare": _VENDORING_PART,
    "py/main_vendoring.py --provenance": _VENDORING_PART,
    "py/main_vendoring.py --gen-inventory": _VENDORING_PART,
    "py/main_slide_generator.py make-pptx": (
        "Claude-written proposal, not yet reviewed by Ben: it builds an untracked"
        " presentation file for giving a talk.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_uxlc_estimate_atom_loc.py": (
        "Claude-written proposal, not yet reviewed by Ben: a lookup that prints one"
        " estimated folio, column and line.  Proposed in doc/mega-coverage-2026-09-10.md"
        " §4."
    ),
    "py/main_just_render_table.py --update-issue-metadata": (
        "Claude-written proposal, not yet reviewed by Ben: it refreshes a snapshot of"
        " the live GitHub tracker through gh.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/check_qr_relations.py": _CHECK_WRITES_NOTHING,
    "py/check_qr_consistency.py": _CHECK_WRITES_NOTHING,
    "py/check_html_syntax_and_sanity.py": _CHECK_WRITES_NOTHING,
    "py/check_escape_sequences.py": _CHECK_WRITES_NOTHING,
    "py/check_function_ordering.py": _CHECK_WRITES_NOTHING,
    "py/main_ac_gen_flat_stream.py": (
        "Claude-written proposal, not yet reviewed by Ben: it seeds one page from a"
        " hand-chosen verse range, and refuses to overwrite.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4."
    ),
    "py/main_ac_merge_line_markers.py": (
        "Claude-written proposal, not yet reviewed by Ben: it merges line markers from a"
        " hand edit, so it has no input until a person edits a page.  Proposed in"
        " doc/mega-coverage-2026-09-10.md §4."
    ),
    # --- Ben's decisions of 2026-09-10.
    "py/main_ac_check_line_breaks.py": _LINE_BREAK_REPORT,
    "py/main_cam1753_check_line_breaks.py": _LINE_BREAK_REPORT,
    "py/main_slide_generator.py make-thumbs": (
        "Ben's decision, 2026-09-10: \"don't include these thumbnail-generator-programs"
        ' in mega".  It thumbnails the slides that render-slides draws, which the mega'
        " does not run either.  Recorded in doc/mega-coverage-2026-09-10.md §1,"
        " decision 4(d), and phase 7 of doc/PLAN-mega-coverage.md."
    ),
    # --- Programs the analysis's sections 3 and 4 do not name.
    "py/main_0_mega.py": (
        "The mega itself, which py/main_repo_maintenance.py runs at its step 6."
        "  Recorded in the docstrings of both."
    ),
    "py/main_authored.py gen-mp-claims-index": (
        "Claude-written proposal, not yet reviewed by Ben: it rewrites doc/mp-claims.md"
        " alone, and the parse-go step already rewrites that file, since the step runs"
        " gen-mam-parsed-docs, which writes the claims index too.  The overlap is"
        " recorded in py/main_authored.py's docstring and in the Method paragraph of"
        " doc/mega-coverage-2026-09-10.md."
    ),
    "py/main_authored.py verify-mp": (
        "Claude-written proposal, not yet reviewed by Ben: it runs the MAM-parsed claim"
        " verification alone, and the parse-go step already runs it, since the step runs"
        " gen-mam-parsed-docs, which verifies the claims too.  The overlap is recorded in"
        " py/main_authored.py's docstring and in the Method paragraph of"
        " doc/mega-coverage-2026-09-10.md."
    ),
    "py/main_mam_simple.py all": (
        "The mega runs its two halves as two steps, mam-simple for the export and"
        " mam-simple-docs for the docs.  Recorded in item 1 of phase 5b of"
        " doc/PLAN-mega-coverage.md, and in the comment above the mam-simple-docs step"
        " in py/main_0_mega.py."
    ),
    "py/main_just_render_table.py": (
        "Its default form renders the pages that the verify-and-render-table step"
        " renders once it has verified Holman's table; its --update-issue-metadata form"
        " is declared on its own.  Recorded in doc/mega-coverage-2026-09-10.md §5, in"
        ' the row for py/main_verify_and_render_table.py ("its render-only subset"),'
        " whose recommendation Ben agreed to on 2026-09-10 and phase 5a of"
        " doc/PLAN-mega-coverage.md carried out."
    ),
    "py/check_all.py": (
        "Claude-written proposal, not yet reviewed by Ben: it is book-of-job's register"
        " of seven checks, run by hand, and each of the seven is accounted for on its"
        " own: its spell check runs at the end of the book-of-job-site step, and the"
        " other six are declared here.  That it is book-of-job's register is recorded in"
        " py/ac_paths.py and doc/PLAN-evacuate-public-repos-programme.md"
        ' ("`check_all.py` stays each repo\'s register"), and'
        " doc/book-of-job-artifacts.md runs it by hand."
    ),
}

# ---------------------------------------------------------------------------
# Calls whose program the scan cannot name from the call alone.  Each key is a
# call as a runner in py/main_0_mega.py writes it, ``<imported name>.<function>``,
# and each value is the program key or keys that call runs.  Words after a program
# key are the arguments that run passes, which is what the mode check reads.
# ---------------------------------------------------------------------------
_RUNNER_CALLS: dict[str, tuple[str, ...]] = {
    # The function `py/main_parse.py go` calls.  It ends by calling
    # main_authored.cmd_gen_mam_parsed_docs(None), which is exactly what
    # `py/main_authored.py gen-mam-parsed-docs` runs.
    "parse_go.almost_main": (
        "py/main_parse.py go",
        "py/main_authored.py gen-mam-parsed-docs",
    ),
    # The function `py/main_parse.py ws` calls, here with no book named.
    "parse_ws.almost_main": ("py/main_parse.py ws",),
    # What `py/main_diff.py mpp --all` runs.
    "diff_mpp.run_all": ("py/main_diff.py mpp --all",),
    # py/subcommands/diff_wsgo.py binds almost_main to run, the function `wsgo` calls.
    "diff_wsgo.almost_main": ("py/main_diff.py wsgo",),
    # The function `py/main_ws_bot.py proto` calls, here with no edit file.
    "ws_bot_proto.almost_main": ("py/main_ws_bot.py proto",),
    # gen-misc, the default, runs cmd_gen_misc, which calls almost_main.
    "main_authored.almost_main": ("py/main_authored.py gen-misc",),
    # What cmd_gen_site runs for `gen-site --trust-surveys`.
    "main_authored.gen_site": ("py/main_authored.py gen-site --trust-surveys",),
    # The export core-only runs, which ends by calling the function copy-support-files
    # calls, mam_simple_copy_py_files.copy_support_files().
    "main_mam_simple.almost_main": (
        "py/main_mam_simple.py core-only",
        "py/main_mam_simple.py copy-support-files",
    ),
    # The function doc-only calls.
    "main_mam_simple.write_generated_docs": ("py/main_mam_simple.py doc-only",),
    # book-of-job's site generator, which ends by calling check_spelling_in_html.main().
    "main_gen_misc_authored_english_documents.main": (
        "py/main_gen_misc_authored_english_documents.py",
        "py/check_spelling_in_html.py",
    ),
}

# Scripts a step runs by subprocess that are not programs of this repository.  Naming
# them here is what keeps a script path the scan cannot match a failure everywhere else.
_EXTERNAL_SCRIPTS: dict[str, str] = {
    "near-aleppo/census/run_all.py": (
        "MAM-private's census runner, which the near-aleppo-census step runs in that"
        " clone: a program of MAM-private, not of this repository."
    ),
}

_MEGA = "py/main_0_mega.py"
_SUBPROCESS_FUNCTIONS = frozenset(
    {"run", "call", "check_call", "check_output", "Popen"}
)


# ---------------------------------------------------------------------------
# Reading the tree.
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=1)
def _tracked_py() -> frozenset[str]:
    """Every tracked .py, by repo-relative path."""
    result = subprocess.run(
        ["git", "-C", str(paths.repo_root()), "ls-files", "*.py"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    rels = frozenset(line for line in result.stdout.splitlines() if line)
    assert rels, "git ls-files listed no tracked .py -- the scan has no input"
    return rels


@functools.lru_cache(maxsize=None)
def _source(rel: str) -> str:
    return (paths.repo_root() / rel).read_text(encoding="utf-8")


@functools.lru_cache(maxsize=None)
def _tree(rel: str) -> ast.Module:
    return ast.parse(_source(rel), filename=rel)


def _callee_name(call: ast.Call) -> str | None:
    """The name a call is made through: ``f`` for both ``f()`` and ``x.f()``."""
    return getattr(call.func, "attr", None) or getattr(call.func, "id", None)


def _module_level_value(tree: ast.Module, ident: str) -> ast.expr | None:
    """What ``ident`` is assigned at module level, if anything."""
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == ident:
                    return node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            if isinstance(node.target, ast.Name) and node.target.id == ident:
                return node.value
    return None


def _module_rel(dotted: str) -> str | None:
    """The tracked file an import of ``dotted`` reads, from py/, where programs run."""
    rel = "py/" + dotted.replace(".", "/") + ".py"
    return rel if rel in _tracked_py() else None


def _is_main_guard(node: ast.stmt) -> bool:
    """Is this statement ``if __name__ == "__main__":``, either way round?"""
    if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
        return False
    test = node.test
    if len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return False
    sides = (test.left, test.comparators[0])
    has_name = any(isinstance(s, ast.Name) and s.id == "__name__" for s in sides)
    has_main = any(isinstance(s, ast.Constant) and s.value == "__main__" for s in sides)
    return has_name and has_main


# ---------------------------------------------------------------------------
# The programs.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class _EntryPoint:
    """A program file, with its subcommands, or none when the file is one program."""

    rel: str
    subcommands: tuple[str, ...]


@functools.lru_cache(maxsize=1)
def _entry_points() -> tuple[dict[str, _EntryPoint], tuple[str, ...]]:
    """Every program file by path, and the add_parser sites the scan could not read."""
    found: dict[str, _EntryPoint] = {}
    problems: list[str] = []
    for rel in sorted(_tracked_py()):
        # A file with the guard has the string in it, so only those files are parsed.
        if rel.startswith("py/tests/") or "__main__" not in _source(rel):
            continue
        tree = _tree(rel)
        if any(_is_main_guard(node) for node in tree.body):
            found[rel] = _EntryPoint(rel, _subcommand_names(rel, tree, problems))
    assert found, "no tracked .py has a __main__ block -- discovery is broken"
    return found, tuple(problems)


def _programs() -> set[str]:
    """Every program key: a path, or a path and one of its subcommands."""
    entry_points, _ = _entry_points()
    out: set[str] = set()
    for rel, entry in entry_points.items():
        if entry.subcommands:
            out.update(f"{rel} {name}" for name in entry.subcommands)
        else:
            out.add(rel)
    return out


def _subcommand_names(
    rel: str, tree: ast.Module, problems: list[str]
) -> tuple[str, ...]:
    """The name of every add_parser call in one file, table-built names included."""
    names: list[str] = []
    loops = _enclosing_loops(tree)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and _callee_name(node) == "add_parser"):
            continue
        name_node = node.args[0] if node.args else None
        if isinstance(name_node, ast.Constant) and isinstance(name_node.value, str):
            names.append(name_node.value)
            continue
        from_table = _names_from_table(tree, name_node, loops.get(id(node), ()))
        if from_table is None:
            shown = "no name" if name_node is None else ast.unparse(name_node)
            problems.append(
                f"{rel}:{node.lineno}: add_parser({shown}) names a subcommand this scan"
                " cannot read.  Build the names from a module-level tuple, as"
                " py/main_accgram.py builds its generate-html-<name> subcommands from"
                " _HTML_GENERATORS, or teach _names_from_table the new shape."
            )
            continue
        names.extend(from_table)
    return tuple(names)


def _enclosing_loops(tree: ast.Module) -> dict[int, tuple[ast.For, ...]]:
    """For each node, by id, the for loops it sits inside, outermost first."""
    out: dict[int, tuple[ast.For, ...]] = {}

    def visit(node: ast.AST, loops: tuple[ast.For, ...]) -> None:
        inner = loops + (node,) if isinstance(node, ast.For) else loops
        for child in ast.iter_child_nodes(node):
            out[id(child)] = inner
            visit(child, inner)

    visit(tree, ())
    return out


def _names_from_table(
    tree: ast.Module, name_node: ast.expr | None, loops: tuple[ast.For, ...]
) -> list[str] | None:
    """The names an f-string builds inside a loop over a module-level table.

    ``f"generate-html-{name}"`` inside ``for name, module in _HTML_GENERATORS:`` reads
    the first element of each row.  Any other shape gives None, which the caller
    reports as a site it cannot read.
    """
    if not isinstance(name_node, ast.JoinedStr):
        return None
    holes = [part for part in name_node.values if isinstance(part, ast.FormattedValue)]
    if len(holes) != 1 or not isinstance(holes[0].value, ast.Name):
        return None
    if holes[0].conversion != -1 or holes[0].format_spec is not None:
        return None
    ident = holes[0].value.id
    for loop in reversed(loops):
        position = _bound_position(loop.target, ident)
        if position is None:
            continue
        if not isinstance(loop.iter, ast.Name):
            return None
        table = _module_level_value(tree, loop.iter.id)
        if not isinstance(table, (ast.Tuple, ast.List)):
            return None
        values: list[str] = []
        for row in table.elts:
            cell = row
            if position >= 0:
                if not isinstance(row, (ast.Tuple, ast.List)):
                    return None
                if len(row.elts) <= position:
                    return None
                cell = row.elts[position]
            if not (isinstance(cell, ast.Constant) and isinstance(cell.value, str)):
                return None
            values.append(cell.value)
        return [
            "".join(
                part.value if isinstance(part, ast.Constant) else value
                for part in name_node.values
            )
            for value in values
        ]
    return None


def _bound_position(target: ast.expr, ident: str) -> int | None:
    """-1 if a loop's target is ``ident``, its index in a tuple target, else None."""
    if isinstance(target, ast.Name):
        return -1 if target.id == ident else None
    if isinstance(target, (ast.Tuple, ast.List)):
        for index, element in enumerate(target.elts):
            if isinstance(element, ast.Name) and element.id == ident:
                return index
    return None


# ---------------------------------------------------------------------------
# What the mega runs.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class _Run:
    """One program a step runs, with the arguments it passes where they can be read."""

    step_id: str
    program: str
    args: tuple[str, ...] | None


@dataclass(frozen=True)
class _MegaScan:
    runs: tuple[_Run, ...]
    problems: tuple[str, ...]
    used_runner_calls: frozenset[str]
    used_external_scripts: frozenset[str]


# A call a runner makes: what is called, with its positional and keyword arguments.
_Call = tuple[ast.expr, list[ast.expr], list[ast.keyword]]


@functools.lru_cache(maxsize=1)
def _scan_mega() -> _MegaScan:
    """Read every runner of the mega's _STEPS, and record what each one runs."""
    tree = _tree(_MEGA)
    entry_points, _ = _entry_points()
    aliases = _import_aliases(tree)
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    runs: list[_Run] = []
    problems: list[str] = []
    used_calls: set[str] = set()
    used_scripts: set[str] = set()
    for step_id, runner, lineno in _steps(tree, problems):
        calls = _calls_of(runner, functions)
        if calls is None:
            problems.append(
                f"{_MEGA}:{lineno}: the runner of step {step_id}, {ast.unparse(runner)},"
                " is neither a function that module defines, nor a lambda, nor a"
                " function of a module it imports, so this scan cannot read it."
            )
            continue
        for func, args, keywords in calls:
            if not (
                isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)
            ):
                continue
            alias, attr = func.value.id, func.attr
            if alias == "subprocess" and attr in _SUBPROCESS_FUNCTIONS:
                _record_script(step_id, args, runs, problems, used_scripts)
                continue
            rel = aliases.get(alias)
            if rel is None:
                continue  # not a module of this repository
            call = f"{alias}.{attr}"
            if call in _RUNNER_CALLS:
                used_calls.add(call)
                for key in _RUNNER_CALLS[call]:
                    parsed = _split_key(key, entry_points)
                    if isinstance(parsed, tuple):  # else the dead-entry test reports it
                        runs.append(_Run(step_id, parsed[0], tuple(parsed[1].split())))
                continue
            entry = entry_points.get(rel)
            if entry is None:
                continue  # library code
            passed = _passed_args(attr, args, keywords)
            if not entry.subcommands:
                runs.append(_Run(step_id, rel, passed))
            elif attr == "almost_main" and passed and passed[0] in entry.subcommands:
                runs.append(_Run(step_id, f"{rel} {passed[0]}", passed[1:]))
            else:
                problems.append(
                    f"step {step_id} calls {call}, a function of {rel}, which has"
                    " subcommands, and this scan cannot tell which subcommand that"
                    " runs.  Call almost_main([...]) with the subcommand first, or add"
                    " the call to _RUNNER_CALLS with the program key it runs."
                )
    return _MegaScan(
        tuple(runs), tuple(problems), frozenset(used_calls), frozenset(used_scripts)
    )


def _steps(tree: ast.Module, problems: list[str]) -> list[tuple[str, ast.expr, int]]:
    """(step id, runner, line) for each StepRecord in the mega's _STEPS."""
    steps = _module_level_value(tree, "_STEPS")
    assert isinstance(steps, ast.List), f"{_MEGA} assigns _STEPS no list literal"
    out: list[tuple[str, ast.expr, int]] = []
    for element in steps.elts:
        fields: dict[str, ast.expr] = {}
        if isinstance(element, ast.Call) and _callee_name(element) == "StepRecord":
            fields = dict(zip(("step_id", "runner", "note"), element.args))
            fields.update({kw.arg: kw.value for kw in element.keywords if kw.arg})
        step_id, runner = fields.get("step_id"), fields.get("runner")
        if runner is None or not (
            isinstance(step_id, ast.Constant) and isinstance(step_id.value, str)
        ):
            problems.append(
                f"{_MEGA}:{element.lineno}: an element of _STEPS this scan cannot read"
                " as StepRecord(step_id, runner, note)."
            )
            continue
        out.append((step_id.value, runner, element.lineno))
    assert out, f"{_MEGA}'s _STEPS lists no step -- the scan has no input"
    return out


def _calls_of(
    runner: ast.expr, functions: dict[str, ast.FunctionDef]
) -> list[_Call] | None:
    """Every call a runner makes, following the mega's own functions that it calls."""
    if isinstance(runner, ast.Attribute):
        return [(runner, [], [])]  # main() calls every runner bare
    if isinstance(runner, ast.Name) and runner.id in functions:
        return _calls_in(functions[runner.id], functions, {runner.id})
    if isinstance(runner, ast.Lambda):
        return _calls_in(runner, functions, set())
    return None


def _calls_in(
    node: ast.AST, functions: dict[str, ast.FunctionDef], seen: set[str]
) -> list[_Call]:
    out: list[_Call] = []
    for sub in ast.walk(node):
        if not isinstance(sub, ast.Call):
            continue
        out.append((sub.func, sub.args, sub.keywords))
        callee = sub.func
        if isinstance(callee, ast.Name) and callee.id in functions:
            if callee.id not in seen:
                seen.add(callee.id)
                out.extend(_calls_in(functions[callee.id], functions, seen))
    return out


def _import_aliases(tree: ast.Module) -> dict[str, str]:
    """Each name a module-level import binds to a tracked module, with its path."""
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                rel = _module_rel(alias.name)
                # ``import a.b`` binds ``a``, not the module ``a.b``.
                if rel is not None and (alias.asname or "." not in alias.name):
                    out[alias.asname or alias.name] = rel
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            for alias in node.names:
                rel = _module_rel(f"{node.module}.{alias.name}")
                if rel is not None:
                    out[alias.asname or alias.name] = rel
    return out


def _passed_args(
    attr: str, args: list[ast.expr], keywords: list[ast.keyword]
) -> tuple[str, ...] | None:
    """The command-line arguments a call hands its program, where the call shows them.

    ``almost_main([...])`` spells them out.  A bare ``almost_main()`` or ``main()``
    passes none, since py/main_0_mega.py blanks sys.argv while its steps run.  What
    any other call passes is unknown, and None says so.
    """
    if attr in ("almost_main", "main") and not args and not keywords:
        return ()
    if attr == "almost_main" and len(args) == 1 and not keywords:
        return _string_list(args[0])
    return None


def _string_list(node: ast.expr) -> tuple[str, ...] | None:
    """A list or tuple literal of strings, or None for anything else."""
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    items = node.elts
    if all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in items):
        return tuple(e.value for e in items)
    return None


def _record_script(
    step_id: str,
    args: list[ast.expr],
    runs: list[_Run],
    problems: list[str],
    used_scripts: set[str],
) -> None:
    """Record the program a subprocess runs: the first .py path in its argument list."""
    if not args or not isinstance(args[0], (ast.List, ast.Tuple)):
        return
    elements = args[0].elts
    for index, element in enumerate(elements):
        if isinstance(element, ast.Constant) and isinstance(element.value, str):
            if element.value.endswith(".py"):
                break
    else:
        return  # runs no Python script
    script = element.value
    if script in _EXTERNAL_SCRIPTS:
        used_scripts.add(script)
        return
    entry_points, _ = _entry_points()
    matches = [
        rel for rel in entry_points if rel == script or rel.endswith("/" + script)
    ]
    if len(matches) != 1:
        problems.append(
            f"step {step_id} runs {script} by subprocess, which matches"
            f" {len(matches)} tracked programs rather than one.  If it is a program of"
            " another repository, add it to _EXTERNAL_SCRIPTS saying whose."
        )
        return
    entry = entry_points[matches[0]]
    passed = _string_list(ast.List(elts=list(elements[index + 1 :]), ctx=ast.Load()))
    if not entry.subcommands:
        runs.append(_Run(step_id, entry.rel, passed))
    elif passed and passed[0] in entry.subcommands:
        runs.append(_Run(step_id, f"{entry.rel} {passed[0]}", passed[1:]))
    else:
        problems.append(
            f"step {step_id} runs {entry.rel} by subprocess without naming one of its"
            " subcommands first, so this scan cannot tell which one it runs."
        )


# ---------------------------------------------------------------------------
# Reading a declared key.
# ---------------------------------------------------------------------------
def _split_key(key: str, entry_points: dict[str, _EntryPoint]) -> tuple[str, str] | str:
    """(program key, mode) for a declared key, or why the key names no program."""
    rel, _, rest = key.partition(" ")
    entry = entry_points.get(rel)
    if entry is None:
        return f"no tracked program is {rel}"
    if not entry.subcommands:
        return rel, rest
    name, _, mode = rest.partition(" ")
    if name not in entry.subcommands:
        if not name:
            return f"{rel} has subcommands, and the key names none of them"
        return f"{rel} has no subcommand {name!r}"
    return f"{rel} {name}", mode


def _mode_flags(mode: str) -> tuple[frozenset[str], bool]:
    """The flags a mode names, and whether it is the program run without them."""
    words = mode.split()
    flags = frozenset(word for word in words if word.startswith("--"))
    return flags, bool(words) and words[0] == "without"


@functools.lru_cache(maxsize=None)
def _defined_flags(rel: str) -> frozenset[str]:
    """Option strings that add_argument defines in a file or a tracked module it imports."""
    sources = {rel}
    for node in ast.walk(_tree(rel)):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names = [node.module] + [f"{node.module}.{a.name}" for a in node.names]
        else:
            continue
        sources.update(found for found in map(_module_rel, names) if found)
    flags: set[str] = set()
    for source in sources:
        for node in ast.walk(_tree(source)):
            if isinstance(node, ast.Call) and _callee_name(node) == "add_argument":
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        flags.add(arg.value)
    return frozenset(flags)


def _declared_programs(entry_points: dict[str, _EntryPoint]) -> set[str]:
    """The programs NOT_IN_MEGA declares whole, its modes left out."""
    out: set[str] = set()
    for key in NOT_IN_MEGA:
        parsed = _split_key(key, entry_points)
        if isinstance(parsed, tuple) and not parsed[1]:
            out.add(parsed[0])
    return out


# ---------------------------------------------------------------------------
# The three failures.
# ---------------------------------------------------------------------------
def test_every_program_is_run_by_the_mega_or_declared() -> None:
    entry_points, unread_names = _entry_points()
    scan = _scan_mega()
    problems = [*unread_names, *scan.problems]
    assert not problems, (
        "This scan met a site it cannot read, so the set of programs, or what the"
        " mega runs, is unknown rather than merely different.  Resolving the site is"
        " the fix; weakening the scan is not.\n  " + "\n  ".join(problems)
    )
    ran = {run.program for run in scan.runs}
    missing = sorted(_programs() - ran - _declared_programs(entry_points))
    assert not missing, "\n  ".join(
        ["Programs that the mega does not run and NOT_IN_MEGA does not declare:"]
        + [
            f"NEITHER RUN NOR DECLARED: {key}.  Add a step to _STEPS in"
            " py/main_0_mega.py that runs it, or declare it in NOT_IN_MEGA with a"
            " reason that says why the mega leaves it out and cites where that reason"
            " is recorded: a section of doc/mega-coverage-2026-09-10.md, a plan phase,"
            " CLAUDE.md, a docstring, or a quoted decision of Ben's with its date.  If"
            " a step already runs it through a call this scan cannot name, add that"
            " call to _RUNNER_CALLS instead."
            for key in missing
        ]
    )


def test_every_declaration_names_something_that_exists() -> None:
    entry_points, _ = _entry_points()
    scan = _scan_mega()
    dead: list[str] = []
    for key in sorted(NOT_IN_MEGA):
        parsed = _split_key(key, entry_points)
        if isinstance(parsed, str):
            dead.append(
                f"DECLARED BUT GONE: {key}: {parsed}.  Delete its NOT_IN_MEGA entry,"
                " or correct the key."
            )
            continue
        flags, _ = _mode_flags(parsed[1])
        rel = parsed[0].partition(" ")[0]
        for flag in sorted(flags - _defined_flags(rel)):
            dead.append(
                f"DECLARED BUT GONE: {key}: neither {rel} nor a module it imports"
                f" defines {flag} any more.  Delete its NOT_IN_MEGA entry, or correct"
                " the key."
            )
    for call in sorted(_RUNNER_CALLS):
        if call not in scan.used_runner_calls:
            dead.append(
                f"_RUNNER_CALLS[{call!r}]: no runner in py/main_0_mega.py makes this"
                " call any more.  Delete the entry."
            )
        for key in _RUNNER_CALLS[call]:
            parsed = _split_key(key, entry_points)
            if isinstance(parsed, str):
                dead.append(
                    f"_RUNNER_CALLS[{call!r}] names {key!r}, but {parsed}.  Correct the"
                    " entry, or delete it."
                )
    for script in sorted(_EXTERNAL_SCRIPTS):
        if script not in scan.used_external_scripts:
            dead.append(
                f"_EXTERNAL_SCRIPTS[{script!r}]: no step runs this script by"
                " subprocess any more.  Delete the entry."
            )
    assert not dead, (
        "A declaration here names something the tree no longer has.  Nothing consults"
        " it, so the check would go on passing while the table went on describing code"
        " that is gone.\n  " + "\n  ".join(dead)
    )


def test_no_declared_program_is_run_by_the_mega() -> None:
    entry_points, _ = _entry_points()
    scan = _scan_mega()
    ran: list[str] = []
    for key in sorted(NOT_IN_MEGA):
        parsed = _split_key(key, entry_points)
        if isinstance(parsed, str):
            continue  # the dead-entry test reports it
        program, mode = parsed
        flags, without = _mode_flags(mode)
        for run in scan.runs:
            if run.program != program:
                continue
            if not mode:
                hit = True
            elif not flags or run.args is None:
                hit = False  # a mode this scan cannot see
            elif without:
                hit = set(run.args).isdisjoint(flags)
            else:
                hit = flags <= set(run.args)
            if hit:
                passing = f", passing {list(run.args)}" if mode else ""
                ran.append(
                    f"DECLARED BUT RUN: {key}, which the mega's {run.step_id} step"
                    f" runs{passing}.  Delete its NOT_IN_MEGA entry: the mega runs it"
                    " now."
                )
                break
    assert not ran, (
        "A program that NOT_IN_MEGA declares as left out of the mega is one the mega"
        " runs.\n  " + "\n  ".join(ran)
    )
