"""Resolve the codex-index-leningrad DATA root, and the place its CODE now sits.

THIS MODULE IS DELIBERATELY TWO-ROOTED, and that is the whole point of its
existence.  The code is here in MAM-basics since Phase 3 of
``doc/PLAN-evacuate-python-from-codex-index-trio.md``; the data it reads and
writes stayed in the sibling codex-index-leningrad and goes on being hosted
there indefinitely, per Ben's decision of 2026-08-22 recorded in that plan's
section "This plan moves the Python and nothing else":

  * the CODE root is ``mb_cmn.paths.repo_root()`` -- what ``py/`` is under, what
    ``git`` acts on, what the source lints scan;
  * the DATA root is ``lenin_data_root()`` below -- codex-index-leningrad's
    ``lenin-wiki/`` (the three artifacts the wikisource pipeline writes) and
    ``UXLC-utils-sparse/`` (the vendored UXLC-utils subset it reads).

WHAT THIS REPLACED.  Phase 1 of the same plan (2026-08-22, ``eb7c83c`` there)
turned four cwd-relative literals -- one ``"UXLC-utils-sparse/data/..."`` and
three ``"lenin-wiki/..."`` -- into ``_REPO_ROOT`` and ``_WIKI_DIR`` inside the
one entry point that held them, so that this move had one root to repoint rather
than four strings to find.  Those two names do NOT survive the move: Phase 3
item 2 of the plan says not to carry ``_DATA_ROOT`` into MAM-basics as a fourth
spelling of the same idea, and the accessors below are the third spelling
retired to.

THE OTHER HALF OF THAT REPO'S PYTHON, and why it is here under a different name.
``main_update_vendored_files.py`` and its ``vendoring_sync.py`` refreshed
``UXLC-utils-sparse/`` from the sibling UXLC-utils.  The refresh is still wanted
-- Ben's decision of 2026-08-03 dropped the ``py/`` half of that sparse copy and
kept the data half -- so the script landed as
``py/main_lenin_vendor_uxlc.py``, named for ``py/main_wlc_vendor_uxlc.py``,
which does the same job for this repo's own vendored UXLC subset.  Its
``vendoring_sync.py`` was a two-line fork of ``mb_cmn/vendoring_sync.py`` and is
gone: the two lines were the breadcrumb's filename, which
``write_provenance`` now takes as a parameter.

NO ``code_paths()`` CONSUMER YET, and that is a stated gap rather than an
oversight.  The four source lints in this repo -- ``check_function_ordering``,
``check_mark_order``, ``check_escape_sequences`` and the two ``fix_*`` -- still
scope to ``boj_paths.code_paths()`` alone, so the eight modules named in
``LENIN_CODE`` below are NOT linted today.  codex-index-aleppo and
codex-index-cam1753 are the repos that bring lint copies of their own, and their
Phase 3 is where the union over the per-repo lists gets built; ``code_paths()``
is here so that step is one entry rather than a new list.  Nothing here has a
combining mark or a ``\\uXXXX`` escape, checked 2026-08-22, so the gap costs
nothing today and would cost something the moment a module here grew one.
"""

from pathlib import Path

from mb_cmn import paths

DATA_REPO_NAME = "codex-index-leningrad"
"""The sibling repo that kept the data when the Python left it."""

LENIN_PACKAGE = "lenin_wiki"
"""The package codex-index-leningrad's ``lenin-wiki/py/`` landed in.

Six modules, not the eighteen that directory held: eleven of the eighteen were
copies of this repo's own modules under four kinds of disguise -- renamed
(``my_locales``, ``my_open``, ``mam_book_names``,
``mam_book_names_and_std_book_names``), out of package (``vtrad_data``,
``vtrad_helpers``, ``get_cvm_rec_from_bcvt``, which are ``py_misc`` here) or
straightforwardly the same name (``hebrew_letters``, ``hebrew_punctuation``,
``hebrew_verse_numerals``, ``my_utils``) -- and every one of the eleven is a
plain deletion now that the six import this repo's modules directly.
"""

LENIN_TOP_LEVEL_MODULES = (
    "lenin_paths.py",
    "main_lenin_wikisource_page.py",
    "main_lenin_vendor_uxlc.py",
)
"""The three modules of codex-index-leningrad's that sit at the top of ``py/``.

``main_lenin_wikisource_page.py`` was ``lenin-wiki/main_make_wikisource_page.py``
and is renamed because codex-index-aleppo holds a file of that name too, and the
two are different tools against different input formats -- the trio plan's
Family 2 classification, settled in its Phase 0.
"""


def lenin_data_root() -> Path:
    """Path to the codex-index-leningrad corpus this code reads and writes.

    The one function the move changed: it was ``Path(__file__)``-rooted inside
    that repo until Phase 3.  Checked rather than merely composed, for the reason
    ``paths.require_sibling`` gives: an absent sibling is a misconfiguration whose
    fix the message can carry, and no CI here would catch a silent skip.
    """
    return paths.require_sibling(DATA_REPO_NAME, paths.sibling_repo(DATA_REPO_NAME))


def wiki_dir() -> Path:
    """``lenin-wiki/`` -- J David Stark's index of the Leningrad Codex and the
    three artifacts ``main_lenin_wikisource_page`` derives from it."""
    return lenin_data_root() / "lenin-wiki"


def uxlc_sparse_dir() -> Path:
    """``UXLC-utils-sparse/`` -- the vendored UXLC-utils subset.

    DATA ONLY since 2026-08-03: Ben's decision in UXLC-utils' Phase 5 dropped the
    seventeen ``.py`` this tree also held rather than repointing them at
    MAM-basics, on the ground that nothing in codex-index-leningrad imported them
    and their one entry point could not run there anyway.  Refreshed by
    ``main_lenin_vendor_uxlc``.
    """
    return uxlc_sparse_dir_of(lenin_data_root())


def uxlc_sparse_dir_of(data_root: Path) -> Path:
    """``UXLC-utils-sparse/`` under an explicitly given data root.

    ``main_lenin_vendor_uxlc`` composes its own paths off one root it names once,
    and this lets it do that without a second literal.
    """
    return data_root / "UXLC-utils-sparse"


def lci_augrecs_path() -> Path:
    """``UXLC-utils-sparse/data/lci_augrecs.json`` -- the one input of the
    wikisource pipeline, and the only file it reads from outside ``lenin-wiki/``."""
    return uxlc_sparse_dir() / "data" / "lci_augrecs.json"


def index_s0_annotated_path() -> Path:
    """``lenin-wiki/index-s0-annotated.json``, the pipeline's first artifact:
    the input rows reshaped, with a header added."""
    return wiki_dir() / "index-s0-annotated.json"


def index_s2_grouped_path() -> Path:
    """``lenin-wiki/index-s2-grouped-by-book.json``, the pipeline's second
    artifact: the collapsed rows grouped by book."""
    return wiki_dir() / "index-s2-grouped-by-book.json"


def index_wikitext_path() -> Path:
    """``lenin-wiki/index.wiki``, the pipeline's third artifact and its point --
    the wikitext of the Wikisource page."""
    return wiki_dir() / "index.wiki"


def code_paths() -> tuple[Path, ...]:
    """This repo's paths holding codex-index-leningrad's code, package first.

    Checked for existence, so a renamed or deleted entry fails loudly; only an
    unlisted ADDITION is silent, and this code is being evacuated rather than
    developed.  See the module docstring for who does not call this yet.
    """
    code_dir = paths.repo_root() / "py"
    entries = tuple(
        [code_dir / LENIN_PACKAGE]
        + [code_dir / name for name in LENIN_TOP_LEVEL_MODULES]
    )
    for entry in entries:
        if not entry.exists():
            raise FileNotFoundError(f"codex-index-leningrad code path is gone: {entry}")
    return entries
