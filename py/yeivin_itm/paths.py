"""Repository-local destinations for the selected Yeivin adaptation."""

from mb_cmn import paths

LANDING_FILENAME = "yeivin_itm.html"


def pages_dir():
    """Return the canonical page directory in this checkout."""
    return paths.gh_pages_dir() / "yeivin-itm"


def product_dir():
    """Return the adaptation's documentation and approved-claim directory."""
    return paths.repo_root() / "Yeivin-ITM"
