"""What repo-maintenance sweeps must leave alone: frozen repos, vendored dirs.

Two separate questions, deliberately answered by two separate files:

- Frozen repos come from in/repo_maintenance_policy.json. A frozen repo is a
  paused project whose last-changed date is itself worth preserving, so even a
  reformat that changes no output is unwelcome. The list lives here rather than
  as a marker inside each frozen repo because writing such a marker would change
  the repo and destroy the date the freeze exists to protect.
- Vendored directories are derived from in/vendoring_policy.json's declared
  source package names. A vendored copy is maintained in its source repo; if it
  arrives non-black-compliant, that is the source's business, and reformatting
  the copy only makes the next vendoring sync noisier.

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


def vendored_package_names(policy_path: Path | None = None) -> list[str]:
    """Names of the packages MAM-basics vendors out to sibling repos."""
    payload = read_json(policy_path or DEFAULT_VENDORING_POLICY)
    return sorted(payload["global"]["source_pkg_dirs"])


def vendored_overrides(policy_path: Path | None = None) -> dict[str, list[str]]:
    """Map of repo name to individually vendored file paths within it.

    Whole vendored packages are found by directory name, but the policy also
    records single files copied to paths of their own -- mgketer's
    py/python_modules/my_diffs.py, the wiki repos' hebrew_letters.py. Those are
    just as vendored and just as much not this repo's to reformat.
    """
    payload = read_json(policy_path or DEFAULT_VENDORING_POLICY)
    by_repo: dict[str, list[str]] = {}
    for override in payload["overrides"]:
        by_repo.setdefault(override["dest_repo"], []).append(override["dest_path"])
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
