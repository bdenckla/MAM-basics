"""Where the morphhb-on-MAM study's record, inputs and outputs are.

The study is a frozen record, put on ice by Ben's instruction of 2026-11-16;
``morphhb-on-mam/README.md`` describes it. Every tracked path is composed from
``mb_cmn.paths``, so the program runs from any working directory and in a linked worktree.
morphhb's ``wlc/`` directory comes from the command line, and the large intermediates go to a
work directory, by default under the gitignored ``.novc/``.
"""

from pathlib import Path

from mb_cmn import paths

RECORD_NAME = "morphhb-on-mam"


def record_dir() -> Path:
    """The ``morphhb-on-mam/`` directory: the README, inputs, outputs and research."""
    return paths.repo_root() / RECORD_NAME


def in_dir() -> Path:
    """The study's inputs: the page's specification and fragment, morphhb's tree listing."""
    return record_dir() / "in"


def out_dir() -> Path:
    """The study's small outputs and its page."""
    return record_dir() / "out"


def research_dir() -> Path:
    """The research sub-agents' reports, the root session's checks and their evidence."""
    return record_dir() / "research"


def readme_path() -> Path:
    """The record's README, which also states the facts that the page quotes from it."""
    return record_dir() / "README.md"


def tree_listing_path() -> Path:
    """The GitHub API's listing of morphhb's ``wlc/`` tree at db6c5c9b, as served."""
    return in_dir() / "fetched" / "morphhb-wlctree-1.json"


def fragment_path() -> Path:
    """The fragment of the page that the study's root session wrote."""
    return in_dir() / "page-fragment.html"


def page_path() -> Path:
    """The study's page."""
    return out_dir() / "morphhb-on-mam.html"


def page_text_path() -> Path:
    """The page's visible text."""
    return out_dir() / "40-page-text.txt"


def default_work_dir() -> Path:
    """Where the large intermediates go unless the command line names another directory."""
    return paths.novc_dir() / RECORD_NAME / "work"


def in_repo(path) -> str:
    """``path`` relative to the repository root, with forward slashes.

    The page names its work directory this way, so a work directory outside the repository
    raises rather than putting a machine's path into a tracked output.
    """
    resolved = Path(path).resolve()
    root = paths.repo_root().resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError:
        raise ValueError(
            f"{resolved.as_posix()} is outside the repository; the page names its work"
            " directory, so give one inside the repository"
        ) from None


def shown(path) -> str:
    """``path`` for a progress message: relative to the repository root when inside it."""
    try:
        return in_repo(path)
    except ValueError:
        return Path(path).resolve().as_posix()
