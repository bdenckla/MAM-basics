"""What repo-maintenance sweeps must leave alone, and which repos are private.

Three separate questions, deliberately answered by two separate files:

- Frozen repos come from in/repo_maintenance_policy.json. A frozen repo is a
  paused project whose last-changed date is itself worth preserving, so even a
  reformat that changes no output is unwelcome. The list lives here rather than
  as a marker inside each frozen repo because writing such a marker would change
  the repo and destroy the date the freeze exists to protect.
- Vendored directories are derived from in/vendoring_policy.json's declared
  source package names, and individually vendored files from its overrides and
  foreign_vendored sections; foreign_vendored can name copies whose source is a
  repo other than MAM-basics. A vendored copy is maintained in its source repo;
  if it arrives non-black-compliant, that is the source's business, and
  reformatting the copy only makes the next vendoring sync noisier. The same
  file's record_dirs section names whole folders of records in a swept repo,
  such as an archive whose manifest pins each file's SHA-256, or dated
  provenance. A record's bytes are the record, so the sweep skips each such
  folder's whole subtree.

- Repo visibility comes from in/repo_maintenance_policy.json too, as a second
  section beside the frozen list. It answers a question the freeze does not:
  whether a repo's findings may be written into a file this public repo tracks.
  Frozen and private are unrelated -- MAM-private is private and very much not
  frozen, and mamgo-auto-edits is frozen and public -- so neither list may be
  derived from the other, exactly as with the two lists above.
"""

from __future__ import annotations

from pathlib import Path
import re

from mb_cmn import paths
from repo_util.common import read_json

REPO_ROOT = paths.repo_root()
DEFAULT_MAINTENANCE_POLICY = REPO_ROOT / "in" / "repo_maintenance_policy.json"
DEFAULT_VENDORING_POLICY = REPO_ROOT / "in" / "vendoring_policy.json"


def frozen_repos(policy_path: Path | None = None) -> dict[str, dict]:
    """Map of repo name to its freeze record."""
    payload = read_json(policy_path or DEFAULT_MAINTENANCE_POLICY)
    return payload["frozen_repos"]


def repo_visibility(policy_path: Path | None = None) -> dict[str, str]:
    """Map of repo name to "public" or "private".

    The "comment" key of the JSON section is prose, not a repo, so it is dropped
    here rather than left for every caller to remember to skip.
    """
    payload = read_json(policy_path or DEFAULT_MAINTENANCE_POLICY)
    section = payload["repo_visibility"]
    return {
        name: record["visibility"]
        for name, record in section.items()
        if isinstance(record, dict)
    }


def private_repos(policy_path: Path | None = None) -> list[str]:
    """Names of the repos whose findings must not reach a public repo's tree."""
    visibility = repo_visibility(policy_path)
    return sorted(name for name, kind in visibility.items() if kind == "private")


def public_repos(policy_path: Path | None = None) -> list[str]:
    visibility = repo_visibility(policy_path)
    return sorted(name for name, kind in visibility.items() if kind == "public")


def vendored_package_names(policy_path: Path | None = None) -> list[str]:
    """Names of the packages MAM-basics vendors out to sibling repos."""
    payload = read_json(policy_path or DEFAULT_VENDORING_POLICY)
    return sorted(payload["global"]["source_pkg_dirs"])


def _record_dirs(payload: dict) -> dict[str, list[str]]:
    """Map of repo name to the folders the policy's record_dirs section names in it.

    Each folder is a path relative to the repo root that ends in "/", the mark by
    which vendored_exclude_regex tells a folder from a file. Raises ValueError on
    a malformed section or entry, and on a folder without that trailing slash.
    """
    section = payload["record_dirs"]
    if not isinstance(section, list):
        raise ValueError(f"record_dirs must be a list, not {section!r}")
    by_repo: dict[str, list[str]] = {}
    for entry in section:
        if not isinstance(entry, dict) or set(entry) != {"dest_repo", "dest_dirs"}:
            raise ValueError(
                f"A record_dirs entry needs exactly dest_repo and dest_dirs: {entry!r}"
            )
        repo = entry["dest_repo"]
        dirs = entry["dest_dirs"]
        if not isinstance(repo, str) or not isinstance(dirs, list) or not dirs:
            raise ValueError(
                "A record_dirs entry needs a repo name and a nonempty list of"
                f" folders: {entry!r}"
            )
        for rel_dir in dirs:
            if not isinstance(rel_dir, str) or not rel_dir.endswith("/"):
                raise ValueError(
                    f"record_dirs folder {rel_dir!r} in {repo} does not end in '/'"
                )
        by_repo.setdefault(repo, []).extend(dirs)
    return by_repo


def vendored_overrides(policy_path: Path | None = None) -> dict[str, list[str]]:
    """Map of repo name to the files and folders within it that the sweep leaves alone.

    Whole vendored packages are found by directory name, but the policy can also
    record single files copied to paths of their own. Those files are just as
    vendored and just as much not this repo's to reformat.

    Merges the policy's two per-file sections, overrides (sourced from
    MAM-basics) and foreign_vendored (sourced outside MAM-basics), with the
    folders of its record_dirs section, each of which keeps its trailing slash.
    For the black sweep the three differ only in that a folder's path ends in
    "/": none of them is the sweep's to reformat.
    """
    payload = read_json(policy_path or DEFAULT_VENDORING_POLICY)
    by_repo: dict[str, list[str]] = {}
    for override in payload["overrides"]:
        by_repo.setdefault(override["dest_repo"], []).append(override["dest_path"])
    for entry in payload["foreign_vendored"]:
        by_repo.setdefault(entry["dest_repo"], []).extend(entry["dest_paths"])
    for repo, dirs in _record_dirs(payload).items():
        by_repo.setdefault(repo, []).extend(dirs)
    return by_repo


def vendored_exclude_regex(
    package_names: list[str], override_paths: list[str] | None = None
) -> str:
    """A black --extend-exclude regex covering vendored packages, files and folders.

    black re.searches this against the path relative to the project root, in
    forward slashes with a leading one, and gives a directory's path a trailing
    slash as well. Bracketing the package alternation in slashes matches a whole
    path component at any depth (py/mb_cmn/, py-examples/mb_misc/). An entry of
    override_paths is a folder when it ends in "/" and a file otherwise.
    Anchoring a file's path with a leading slash and a trailing end-of-string
    matches that one file and nothing else. A folder's path takes the leading
    slash and keeps its own trailing one, with no end-of-string, so it matches
    the folder itself and black skips the folder's whole subtree.
    """
    packages = "|".join(re.escape(name) for name in package_names)
    branches = [f"/({packages})/"]
    for rel_path in sorted(override_paths or []):
        if rel_path.endswith("/"):
            branches.append(f"/{re.escape(rel_path)}")
        else:
            branches.append(f"/{re.escape(rel_path)}$")
    return "|".join(branches)
