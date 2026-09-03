"""Resolve UXLC data now held inside MAM-basics.

The former UXLC-utils tree landed under the pure ``uxlc/`` prefix in Phase 5 of
``doc/PLAN-evacuate-the-rest-of-three-repos.md``. Its paths therefore compose
from this repository's root rather than from a sibling repository. Three
existing MAM-basics inputs stay canonical: ``in/UXLC-39/``,
``in/UXLC-misc/all_changes.json`` and ``in/lci_recs.json``. The dedicated
accessors below name those exceptions, so a generator cannot recreate a second
UXLC-utils-sourced copy by accident.
"""

from __future__ import annotations

from pathlib import Path

from mb_cmn import paths


def uxlc_data_root() -> Path:
    """Path to the non-duplicate UXLC tree under MAM-basics' ``uxlc/`` prefix."""
    return paths.repo_root() / "uxlc"


def in_dir() -> Path:
    """Committed UXLC inputs that did not already have a MAM-basics canonical copy."""
    return uxlc_data_root() / "in"


def out_dir() -> Path:
    """Generated-output tree under ``uxlc/out/``."""
    return uxlc_data_root() / "out"


def gh_pages_dir() -> Path:
    """Published UXLC tree under ``gh-pages/uxlc/``."""
    return paths.gh_pages_dir() / "uxlc"


def data_dir() -> Path:
    """Generated UXLC data other repos consume, currently ``lci_augrecs.json``."""
    return uxlc_data_root() / "data"


def novc_dir() -> Path:
    """MAM-basics' gitignored scratch tree for UXLC downloads and temporary files."""
    return paths.novc_dir()


def uxlc_39_dir() -> Path:
    """The canonical UXLC core XML, retained at MAM-basics' ``in/UXLC-39/``."""
    return paths.in_dir() / "UXLC-39"


def uxlc_rest_dir() -> Path:
    """The non-book39 Tanach.xml members under ``uxlc/in/UXLC-rest/``."""
    return in_dir() / "UXLC-rest"


def uxlc_misc_dir() -> Path:
    """UXLC change logs and hand-curated files under ``uxlc/in/UXLC-misc/``."""
    return in_dir() / "UXLC-misc"


def uxlc_misc_fixed_dir() -> Path:
    """Hand-corrected overrides under ``uxlc/in/UXLC-misc-fixed/``."""
    return in_dir() / "UXLC-misc-fixed"


def uxlc_notes_dir() -> Path:
    """The downloaded tanach.us note pages under ``uxlc/in/UXLC-notes/``."""
    return in_dir() / "UXLC-notes"


def out_uxlc_misc_dir() -> Path:
    """Change-log derivatives under ``uxlc/out/UXLC-misc/``.

    ``all_changes.json`` is deliberately absent: the canonical copy remains at
    ``in/UXLC-misc/all_changes.json`` and has its own accessor below.
    """
    return out_dir() / "UXLC-misc"


def canonical_all_changes_path() -> Path:
    """The one canonical UXLC change-list copy: ``in/UXLC-misc/all_changes.json``."""
    return paths.in_dir() / "UXLC-misc" / "all_changes.json"


def lci_recs_path() -> Path:
    """The one canonical Leningrad-index copy: ``in/lci_recs.json``."""
    return paths.in_dir() / "lci_recs.json"


def clc_pages_dir() -> Path:
    """The CLC edition's published pages under ``gh-pages/uxlc/clc/``."""
    return gh_pages_dir() / "clc"


def fois_pages_dir() -> Path:
    """The features-of-interest catalog under ``gh-pages/uxlc/fois/``."""
    return gh_pages_dir() / "fois"


def amb_early_mtg_pages_dir() -> Path:
    """The ambiguous-early-meteg survey under ``gh-pages/uxlc/amb-early-mtg/``."""
    return gh_pages_dir() / "amb-early-mtg"


def tanach_us_http_cache_dir() -> Path:
    """Where the polite downloader caches tanach.us responses."""
    return novc_dir() / "http-cache" / "tanach-us"
