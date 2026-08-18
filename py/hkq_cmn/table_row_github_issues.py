from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

import hkq_paths
from hkq_cmn.json_io import load_json

# The tracker these row numbers name, stated outright rather than inferred from a
# working directory: refresh_table_row_github_issues passes it to `gh --repo`.  It
# stays bdenckla/holman-ketiv-qere after the Python moves to MAM-basics, the issues
# being about the review this repo holds.
REPO_OWNER: Final = "bdenckla"
REPO_NAME: Final = "holman-ketiv-qere"
ROW_GITHUB_ISSUES_JSON_PATH: Final = hkq_paths.row_github_issues_path()

ISSUE_LABEL_TO_TAG: Final[dict[str, str]] = {
    "QyV": "qyv",
    "ḥolam he": "holam-he",
    "בו״א sans א": "boa-sans-aleph",
    "rafeh": "rafeh",
}

ISSUE_TAG_DISPLAY_TEXT: Final[dict[str, str]] = {
    "holam-he": "ḥolam he",
    "qyv": "QyV",
    "boa-sans-aleph": "בו״א sans א",
    "rafeh": "rafeh",
    "no-issue-tag": "no issue tag",
}


@dataclass(frozen=True)
class RowGitHubIssueMetadata:
    issue_number: int
    is_closed: bool
    tags: tuple[str, ...] = ()


def load_row_github_issues(
    path: Path = ROW_GITHUB_ISSUES_JSON_PATH,
) -> dict[str, RowGitHubIssueMetadata]:
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise ValueError("row GitHub issues JSON root must be an object")

    row_metadata: dict[str, RowGitHubIssueMetadata] = {}
    for row_number, metadata_obj in sorted(
        payload.items(), key=lambda item: int(str(item[0]))
    ):
        if not isinstance(metadata_obj, dict):
            raise ValueError(
                f"row GitHub issue metadata for row {row_number} must be an object"
            )
        issue_number = metadata_obj.get("issue_number")
        is_closed = metadata_obj.get("is_closed")
        tags = metadata_obj.get("tags")
        if not isinstance(issue_number, int):
            raise ValueError(f"row {row_number} issue_number must be an integer")
        if not isinstance(is_closed, bool):
            raise ValueError(f"row {row_number} is_closed must be a boolean")
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise ValueError(f"row {row_number} tags must be a list of strings")
        row_metadata[str(row_number)] = RowGitHubIssueMetadata(
            issue_number=issue_number,
            is_closed=is_closed,
            tags=tuple(tags),
        )
    return row_metadata


def reload_row_github_issues(
    path: Path = ROW_GITHUB_ISSUES_JSON_PATH,
) -> dict[str, RowGitHubIssueMetadata]:
    global ROW_GITHUB_ISSUES
    ROW_GITHUB_ISSUES = load_row_github_issues(path)
    return ROW_GITHUB_ISSUES


ROW_GITHUB_ISSUES: dict[str, RowGitHubIssueMetadata] = reload_row_github_issues()


def issue_url_from_number(issue_number: int) -> str:
    return f"https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"


def row_github_issue_metadata(row_number: str) -> RowGitHubIssueMetadata | None:
    return ROW_GITHUB_ISSUES.get(str(row_number))


def require_row_github_issue_metadata(row_number: str) -> RowGitHubIssueMetadata:
    metadata = row_github_issue_metadata(row_number)
    if metadata is None:
        raise KeyError(f"missing GitHub issue metadata for table row {row_number}")
    return metadata


def row_github_issue_number(row_number: str) -> int | None:
    metadata = row_github_issue_metadata(row_number)
    if metadata is None:
        return None
    return metadata.issue_number


def row_github_issue_url(row_number: str) -> str | None:
    issue_number = row_github_issue_number(row_number)
    if issue_number is None:
        return None
    return issue_url_from_number(issue_number)


def row_github_issue_is_closed(row_number: str) -> bool | None:
    metadata = row_github_issue_metadata(row_number)
    if metadata is None:
        return None
    return metadata.is_closed


def row_github_issue_tags(row_number: str) -> tuple[str, ...]:
    metadata = row_github_issue_metadata(row_number)
    if metadata is None:
        return ()
    return metadata.tags
