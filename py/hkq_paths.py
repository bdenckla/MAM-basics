"""Resolve the Holman corpus now co-located under MAM-basics.

The former ``holman-ketiv-qere`` repository is only a redirect host.  Its
tracked data, rendered site, assets, and raw-mailbox locations now live beneath
``MAM-basics/holman``.  Keeping every corpus path in this module makes the
location explicit and prevents a surviving caller from silently reaching the
redirect host.
"""

from __future__ import annotations

from pathlib import Path

from mb_cmn import paths


def hkq_data_root() -> Path:
    """Path to the Holman corpus stored in MAM-basics."""
    return paths.repo_root() / "holman"


def gh_pages_dir() -> Path:
    """Published Holman pages at MAM-basics' ``gh-pages/holman`` subtree."""
    return paths.gh_pages_dir() / "holman"


def email_img_dir() -> Path:
    """PNGs attached to Holman's suggested UXLC-corrections emails."""
    return gh_pages_dir() / "uxlc_img"


def out_dir() -> Path:
    """Generated reports whose tracked source data lives under ``holman/out``."""
    return hkq_data_root() / "out"


def docs_not_served_dir() -> Path:
    """Tracked Holman source data which MAM-basics Pages does not serve directly."""
    return hkq_data_root() / "docs-not-served"


def emails_dir() -> Path:
    """Address-free derivative of Holman's UXLC-corrections emails."""
    return hkq_data_root() / "emails"


def data_dir() -> Path:
    """Tracked atom-location data derived from the UXLC source clone."""
    return hkq_data_root() / "data"


def io_dir() -> Path:
    """Hand-curated input that a script also refreshes."""
    return hkq_data_root() / "io"


def assets_dir() -> Path:
    """Authored CSS and JavaScript copied by render commands into published pages."""
    return hkq_data_root() / "assets"


def novc_dir() -> Path:
    """Gitignored Holman scratch tree under the MAM-basics repository."""
    return paths.novc_dir()


def eml_dir() -> Path:
    """Untracked mailbox for Holman's suggested UXLC corrections."""
    return novc_dir() / "eml"


def table_data_json_path() -> Path:
    """The tracked 77-row ketiv/qere review table."""
    return docs_not_served_dir() / "table_data.json"


def mam_eml_dir() -> Path:
    """Untracked mailbox for Holman's suggested corrections to MAM."""
    return novc_dir() / "eml-mam"


def mam_suggestion_img_dir() -> Path:
    """Page crops belonging to Holman's suggested MAM corrections."""
    return gh_pages_dir() / "mam_img"


def mam_suggestions_json_path() -> Path:
    """The tracked address- and body-free MAM-suggestion derivative."""
    return docs_not_served_dir() / "mam_suggestions.json"


def findings_html_path() -> Path:
    """The filterable report built from the review table."""
    return gh_pages_dir() / "table_data_findings.html"


def row_github_issues_path() -> Path:
    """Checked-in issue state and labels per review row."""
    return io_dir() / "table_row_github_issues.json"


def uxlc_corrections_json_path() -> Path:
    """Tracked address-free derivative of Holman's UXLC corrections."""
    return docs_not_served_dir() / "uxlc_corrections.json"


def uxlc_corrections_html_path() -> Path:
    """The rendered suggested-UXLC-corrections report."""
    return gh_pages_dir() / "uxlc_corrections.html"


def mam_qere_words_path() -> Path:
    """MAM-basics' qere word list used by the holam-he search sanity check."""
    return paths.out_dir() / "mam-qere-words.json"
