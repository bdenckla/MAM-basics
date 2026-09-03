"""Resolve the Leningrad-index paths now held inside MAM-basics.

Phase 1 of
``doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md``
landed the former codex-index-leningrad tree under the pure ``leningrad/``
prefix. The index generator's input is MAM-basics' canonical
``uxlc/data/lci_augrecs.json``; the temporary ``UXLC-utils-sparse/`` copy and
its vendor command have been retired.

``lenin-wiki/`` holds the three artifacts that
``main_lenin_wikisource_page.py`` derives. ``page-snips/`` holds the
hand-maintained Leningrad Codex image crop and its evidence note. The former
repository's Python remains in ``py/lenin_wiki/`` plus this paths module and
the generator, so ``code_paths()`` keeps the eight modules in the source-lint
scope.
"""

from pathlib import Path

from mb_cmn import paths

import uxlc_paths

LENIN_PACKAGE = "lenin_wiki"
"""The package that the former ``lenin-wiki/py/`` directory contributed."""

LENIN_TOP_LEVEL_MODULES = (
    "lenin_paths.py",
    "main_lenin_wikisource_page.py",
)
"""The former codex-index-leningrad modules at the top of ``py/``."""


def lenin_data_root() -> Path:
    """Path to the former codex-index-leningrad tree under ``leningrad/``."""
    return paths.repo_root() / "leningrad"


def wiki_dir() -> Path:
    """The three generated artifacts under ``leningrad/lenin-wiki/``."""
    return lenin_data_root() / "lenin-wiki"


def lci_augrecs_path() -> Path:
    """The canonical ``uxlc/data/lci_augrecs.json`` generator input."""
    return uxlc_paths.data_dir() / "lci_augrecs.json"


def index_s0_annotated_path() -> Path:
    """The pipeline's reshaped-input JSON artifact."""
    return wiki_dir() / "index-s0-annotated.json"


def index_s2_grouped_path() -> Path:
    """The pipeline's page-grouped JSON artifact."""
    return wiki_dir() / "index-s2-grouped-by-book.json"


def index_wikitext_path() -> Path:
    """The pipeline's Wikisource starting-point artifact."""
    return wiki_dir() / "index.wiki"


def code_dir() -> Path:
    """The ``py/`` directory holding the former repository's Python."""
    return Path(__file__).resolve().parent


def code_paths() -> list[Path]:
    """Every Leningrad-index Python location that the source lints scan."""
    named = [code_dir() / LENIN_PACKAGE]
    named += [code_dir() / name for name in LENIN_TOP_LEVEL_MODULES]
    missing = [path for path in named if not path.exists()]
    if missing:
        raise SystemExit(
            "lenin_paths.code_paths: no longer present: "
            + ", ".join(str(path) for path in missing)
        )
    return named
