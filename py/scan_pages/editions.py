"""The five editions, where their scans live, and where the index is tracked.

The scans root is absolute and checkout-independent on purpose: the images live
outside every repo and no image ever enters one, so nothing here may be built from
repo_root().  A worktree therefore reads the same scans the primary clone does.
"""

from pathlib import Path

from mb_cmn import paths

JC1 = "jc1"
KOREN = "koren"
SIMANIM_TANAKH = "simanim-tanakh"
SIMANIM_TIQQUN = "simanim-tiqqun"
BHL = "bhl"

ALL_EDITION_IDS = (JC1, KOREN, SIMANIM_TANAKH, SIMANIM_TIQQUN, BHL)

_FOLDERS = {
    JC1: "JC1 Jerusalem Crown",
    KOREN: "Koren Classic Tanakh",
    SIMANIM_TANAKH: "Feldheim Simanim Tanakh",
    SIMANIM_TIQQUN: "Feldheim Simanim Tiqqun",
    BHL: "Biblia Hebraica Leningradensia",
}

# Ben's title for each edition, for reports and for the eventual bring-up page.
TITLES = {
    JC1: "Jerusalem Crown",
    KOREN: "Koren Classic Tanakh",
    SIMANIM_TANAKH: "Feldheim Simanim Tanakh",
    SIMANIM_TIQQUN: "Feldheim Simanim Tiqqun",
    BHL: "Biblia Hebraica Leningradensia",
}


def scans_root() -> Path:
    """Return the folder holding one subfolder per scanned book."""
    return Path.home() / "OneDrive" / "Documents" / "ScansOfBooks"


def folder_name(edition_id: str) -> str:
    """Return an edition's subfolder name under the scans root."""
    return _FOLDERS[edition_id]


def edition_dir(edition_id: str) -> Path:
    """Return the folder holding one edition's page images."""
    return scans_root() / folder_name(edition_id)


def index_dir() -> Path:
    """Return the tracked directory holding one index JSON per edition."""
    return paths.repo_root() / "in" / "scan-pages"


def index_path(edition_id: str) -> Path:
    """Return an edition's tracked index JSON."""
    return index_dir() / f"{edition_id}.json"
