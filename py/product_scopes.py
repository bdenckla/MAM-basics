"""What this repository publishes and distributes, and which code generates it.

WHY THIS EXISTS

Ben asked on 2026-09-12, of a list of review findings, which of them concerned
"risky" things, "where 'risky' includes things like code changes that could (or
will!) change MAM-parsed, MAM-with-doc, MAM-simple, gh-pages, or other things you
deem 'public facing'".  Answering it took about fifteen separate measurements --
whether a module is named in ``py/main_0_mega.py``, whether a generated tree holds a
word, whether a tracked image is published -- because the repository had no written
answer to "what are this repository's products".  Ben then asked that the notion be
defined for future use.  This module is that definition, and
``py/tests/test_product_scopes.py`` is what keeps it from going stale.

THE THREE TIERS

1. PUBLISHED.  ``gh-pages/``, which a push to ``main`` deploys.  Anyone with the URL
   reads it, and a push is the act that makes that true, so a change reaching this
   tier is outward-facing in the ordinary sense.
2. DISTRIBUTED DATA.  ``MAM-parsed/``, ``MAM-simple/``, ``MAM-for-Sefaria/``,
   ``MAM-with-doc/`` and ``MAM-OSIS/``.  These are consumed by git URL whether or not
   Pages serves them, so "not published" is not the same as "not distributed": a
   consumer pinning a path in one of these trees sees a change here without any
   deploy at all.
3. GENERATORS.  The entry points listed in ``_GENERATOR_ENTRY_POINTS`` below.  This
   is the tier that matters, because it is the only route into tiers 1 and 2 other
   than editing those trees by hand.

WHAT A CHANGE OWES

A change that can reach tier 3 owes a mega run and a reading of the ``git diff`` it
leaves; a change that cannot owes the suite.  CLAUDE.md's section "Integrating a
worktree branch here: run the mega and read its ``git diff``, not the suite" states
that rule and the four conditions on reading the diff; this module does not restate
it.

TIER 3 IS THE MEGA'S STEP TABLE, AND THAT IS NOT EVERY ROUTE INTO A PRODUCT

``_GENERATOR_ENTRY_POINTS`` is exactly what the runners of ``_STEPS`` in
``py/main_0_mega.py`` run, wrappers resolved.  It is therefore the ROUTINE route into
tiers 1 and 2, and not the only one.  The hand-run interactive programs -- the Aleppo
and Cambridge 1753 word-image and crop work above all -- write tracked images that
are published under ``gh-pages/``, and ``py/tests/test_mega_coverage.py`` declares
each of them, with its reason, in ``NOT_IN_MEGA``.  So "this program is not a mega
step" answers a different question from "this change reaches no product", and reading
the first as the second is the mistake this paragraph exists to stop.  A change to a
hand-run generator owes regenerating what it generates, which a mega run will not do
for it.

THE WORKED EXAMPLE, WHICH CROSSES TIERS BY NAME RATHER THAN BY PATH

Three unrelated functions in this repository are called ``strip_heb``.  Measured
2026-09-12: ``py/py_ac_word_image_helper/hebrew_metrics.py`` and
``py/py_cam1753_word_image/hebrew_metrics.py`` reach the manuscript crop generators
through each package's ``linebreak_search.py``, and those generators write the
published crops under ``gh-pages/book-of-job/jobn/img/Aleppo``, ``.../Lenin`` and
``.../cam1753``.  ``py/uxlc_misc/my_uxlc_find_atom.py`` is read by
``py/main_verse_links.py`` and ``py/main_uxlc_estimate_atom_loc.py``, two interactive
lookups that write nothing tracked.  All three sit in programs the mega does not run,
and two of the three reach a published product anyway.  A sweep that edits
``strip_heb`` by name therefore crosses from "reaches nothing" to "changes published
images" without crossing a directory that says so.

"NOT TIER 3" IS NOT "SAFE"

Whether a change reaches a product is one axis of risk.  The other has nothing to do
with products: outward-facing acts, destructive local acts, writes outside the
repository, records that are receipts, and code paths that cannot be exercised on
this machine.  That axis is stated in Ben's user-level instruction files,
``~/.claude/CLAUDE.md`` and ``~/.codex/AGENTS.md``, tracked here as
``dot-claude/user-wide-CLAUDE.md`` and ``dot-Codex/user-wide-AGENTS.md``, under the
heading "Two axes of risk".

WHAT THIS MODULE IS NOT

It is not a second ``py/tests/test_mega_coverage.py``.  That lint asks whether every
PROGRAM is either run by the mega or declared with a reason, by an AST pass over the
tree.  This module asks a narrower question -- which entry points the mega's step
table names, written down where a reader can consult it -- and its lint defends that
written answer against drift.  The two fail on different things: a new program with
no justification fails the coverage lint, while a new mega step whose entry point
nobody has recorded here fails this one.
"""

from pathlib import Path

from mb_cmn import paths

_PRODUCT_DIR_NAMES = (
    "MAM-parsed",
    "MAM-simple",
    "MAM-for-Sefaria",
    "MAM-with-doc",
    "MAM-OSIS",
)

# Every entry point the runners of _STEPS in py/main_0_mega.py run, by repo-relative
# path, with the _run_* wrappers defined in that file resolved to what they drive.
# Four of them live inside a product tree rather than under py/: the vendored example
# scripts the mega runs to prove that a consumer of MAM-parsed and MAM-simple can run
# them from a clone of that product alone.
_GENERATOR_ENTRY_POINTS = (
    "MAM-parsed/py-examples/main_tmpl_survey_toy_example.py",
    "MAM-simple/py-examples/main_letter_small_job_example.py",
    "MAM-simple/py-examples/main_mam4sef_example.py",
    "MAM-simple/py-examples/main_mam_osis_example.py",
    "py/main_ac_gen_index_flat_annotated.py",
    "py/main_accgram.py",
    "py/main_amb_early_mtg.py",
    "py/main_authored.py",
    "py/main_clc.py",
    "py/main_decnreub.py",
    "py/main_diff.py",
    "py/main_diffable_pointed_hebrew.py",
    "py/main_estimate_uxlc_locations.py",
    "py/main_explicit_xataf.py",
    "py/main_find_uxlc_accent_changes.py",
    "py/main_foi_features_of_interest.py",
    "py/main_fois.py",
    "py/main_gen_misc_authored_english_documents.py",
    "py/main_letter_small_job.py",
    "py/main_mam4sef.py",
    "py/main_mam_osis.py",
    "py/main_mam_simple.py",
    "py/main_mam_with_doc.py",
    "py/main_map_changes_to_book_of_job.py",
    "py/main_multimark.py",
    "py/main_pipeline_graph.py",
    "py/main_render_uxlc_corrections.py",
    "py/main_search_final_hiriq_verse_text.py",
    "py/main_search_holam_he_qere.py",
    "py/main_sigil_inventory.py",
    "py/main_tmpl_survey.py",
    "py/main_tmpl_survey_toy.py",
    "py/main_uxlc_check_changes.py",
    "py/main_uxlc_grammar_test.py",
    "py/main_uxlc_word_list.py",
    "py/main_vendoring.py",
    "py/main_verify_and_render_table.py",
    "py/main_wlc_a_notes.py",
    "py/main_wlc_diffs_420422.py",
    "py/main_wlc_json_and_unicode.py",
    "py/main_wordlist.py",
    "py/main_write_page_break_info.py",
    "py/subcommands/diff_mpplus.py",
    "py/subcommands/diff_wsgo.py",
    "py/subcommands/parse_go.py",
    "py/subcommands/parse_ws.py",
    "py/subcommands/ws_bot_proto.py",
)

# Each _run_* wrapper defined in py/main_0_mega.py itself, and the entry point it
# drives.  A wrapper is how a step reaches a program that takes a subcommand or a
# flag, or a script run in another directory, so its runner's module is main_0_mega
# rather than the program's.  The lint resolves a step through this table rather than
# skipping it, so a wrapper added without an entry here fails rather than passing
# unclassified.
_MEGA_WRAPPER_DELEGATES = {
    "_run_ac_gen_index_flat_annotated": "py/main_ac_gen_index_flat_annotated.py",
    "_run_accgram_dual_cant": "py/main_accgram.py",
    "_run_accgram_generate_html": "py/main_accgram.py",
    "_run_accgram_grammaticality": "py/main_accgram.py",
    "_run_accgram_poetic": "py/main_accgram.py",
    "_run_accgram_printed_decalogue": "py/main_accgram.py",
    "_run_accgram_prose": "py/main_accgram.py",
    "_run_accgram_servi_xcheck": "py/main_accgram.py",
    "_run_accgram_survey_chanted_word_accents": "py/main_accgram.py",
    "_run_accgram_survey_post_stress_meteg": "py/main_accgram.py",
    "_run_accgram_test_fixes": "py/main_accgram.py",
    "_run_accgram_xcheck_poetic": "py/main_accgram.py",
    "_run_clc": "py/main_clc.py",
    "_run_diff_ctr_vs_mam": "py/main_diff.py",
    "_run_find_uxlc_accent_changes": "py/main_find_uxlc_accent_changes.py",
    "_run_gen_site": "py/main_authored.py",
    "_run_vendored_letter_small_job": (
        "MAM-simple/py-examples/main_letter_small_job_example.py"
    ),
    "_run_vendored_mam4sef": "MAM-simple/py-examples/main_mam4sef_example.py",
    "_run_vendored_mam_osis": "MAM-simple/py-examples/main_mam_osis_example.py",
    "_run_vendored_tmpl_survey_toy": (
        "MAM-parsed/py-examples/main_tmpl_survey_toy_example.py"
    ),
}


def published_tree() -> Path:
    """Tier 1: the tree a push to ``main`` deploys to GitHub Pages."""
    return paths.repo_root() / "gh-pages"


def product_dirs() -> list[Path]:
    """Tier 2: the five data products, each consumed by git URL as well as by Pages."""
    root = paths.repo_root()
    return [root / name for name in _PRODUCT_DIR_NAMES]


def generator_entry_points() -> list[Path]:
    """Tier 3: every entry point the mega's step table runs, wrappers resolved."""
    root = paths.repo_root()
    return [root / rel for rel in _GENERATOR_ENTRY_POINTS]


def generator_entry_point_rels() -> list[str]:
    """Tier 3 as repo-relative paths, the spelling the lint compares and reports."""
    return list(_GENERATOR_ENTRY_POINTS)


def mega_wrapper_delegates() -> dict[str, str]:
    """For each ``_run_*`` wrapper in ``py/main_0_mega.py``, the entry point it drives."""
    return dict(_MEGA_WRAPPER_DELEGATES)
