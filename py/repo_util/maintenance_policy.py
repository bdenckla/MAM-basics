"""What repo-maintenance sweeps must leave alone, and which repos are private.

Three separate questions, deliberately answered by two separate files:

- Frozen repos come from in/repo_maintenance_policy.json. A frozen repo is a
  paused project whose last-changed date is itself worth preserving, so even a
  reformat that changes no output is unwelcome. The list lives here rather than
  as a marker inside each frozen repo because writing such a marker would change
  the repo and destroy the date the freeze exists to protect.
- Vendored directories are derived from in/vendoring_policy.json's declared
  source package names, and individually vendored files from its overrides and
  foreign_vendored sections; foreign_vendored names copies whose source is a
  repo other than MAM-basics, such as Taamey_D's hbofonts build scripts. A
  vendored copy is maintained in its source repo; if it arrives
  non-black-compliant, that is the source's business, and reformatting the copy
  only makes the next vendoring sync noisier.

- Repo visibility comes from in/repo_maintenance_policy.json too, as a second
  section beside the frozen list. It answers a question the freeze does not:
  whether a repo's findings may be written into a file this public repo tracks.
  Frozen and private are unrelated -- MAM-private is private and very much not
  frozen, and mamgo-auto-edits is frozen and public -- so neither list may be
  derived from the other, exactly as with the two lists above.

Note that in/vendoring_policy.json also has a per-repo "ignore" flag. That means
"do not scan this repo for vendoring" and says nothing about whether the repo is
frozen. The two lists coincide today; that is not a rule and must not become one.
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


def vendored_overrides(policy_path: Path | None = None) -> dict[str, list[str]]:
    """Map of repo name to individually vendored file paths within it.

    Whole vendored packages are found by directory name, but the policy also
    records single files copied to paths of their own -- mgketer's two
    py/python_modules/ files. Those are just as vendored and just as much not
    this repo's to reformat.

    Merges the policy's two per-file sections: overrides (MAM-basics-sourced,
    measured by the vendoring audit) and foreign_vendored (sourced outside
    MAM-basics -- Taamey_D's hbofonts build scripts -- which the audit
    deliberately does not measure). For the black sweep the distinction is
    nothing: neither kind is this repo's to reformat.
    """
    payload = read_json(policy_path or DEFAULT_VENDORING_POLICY)
    by_repo: dict[str, list[str]] = {}
    for override in payload["overrides"]:
        by_repo.setdefault(override["dest_repo"], []).append(override["dest_path"])
    for entry in payload["foreign_vendored"]:
        by_repo.setdefault(entry["dest_repo"], []).extend(entry["dest_paths"])
    return by_repo


def vendored_exclude_regex(
    package_names: list[str], override_paths: list[str] | None = None
) -> str:
    """A black --extend-exclude regex covering vendored packages and files.

    black re.searches this against the path relative to the project root, in
    forward slashes with a leading one. Bracketing the package alternation in
    slashes matches a whole path component at any depth (py/mb_cmn/,
    py-examples/osis/); anchoring each override path with a leading slash and a
    trailing end-of-string matches that one file and nothing else.
    """
    packages = "|".join(re.escape(name) for name in package_names)
    branches = [f"/({packages})/"]
    for rel_path in sorted(override_paths or []):
        branches.append(f"/{re.escape(rel_path)}$")
    return "|".join(branches)
