"""Read stored release inputs and committed MAM-parsed data.

Named historical releases use the tracked snapshots in MAM-parsed/historical/.
HEAD and other current repository refs use MAM-parsed/plus/ in MAM-basics.
Only an explicit legacy: revision reads the sibling MAM-parsed Git repository.
That optional mode performs read-only Git operations and never fetches or clones.
"""

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
import re
import subprocess

from mb_cmn import paths


def _git(repo, *args):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode:
        raise RuntimeError(
            f"Git could not read the requested revision in {repo}:"
            f" {result.stderr.strip()}"
        )
    return result.stdout.strip()


def _manifest():
    path = paths.repo_root() / "MAM-parsed" / "historical" / "manifest.json"
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


@dataclass(frozen=True)
class Revision:
    """A resolved plus tree, its source commit, and its content date."""

    commit: str
    date: str
    directory: Path
    prefix: str
    stored_files: tuple[str, ...] | None = None

    def filenames(self):
        if self.stored_files is not None:
            names = list(self.stored_files)
            for name in names:
                if not (self.directory / self.prefix / name).is_file():
                    raise FileNotFoundError(
                        f"Stored MAM-parsed release input is absent:"
                        f" {self.directory / self.prefix / name}"
                    )
        else:
            names = _git(
                self.directory,
                "ls-tree",
                "-r",
                "--name-only",
                "-z",
                self.commit,
                self.prefix + "/",
            ).split("\0")
            names = [
                name.removeprefix(self.prefix + "/")
                for name in names
                if name.endswith(".json")
            ]
        if not names:
            raise RuntimeError(
                f"No plus JSON files at {self.commit} in {self.directory}."
                " The legacy source's redirect-host HEAD has no product data;"
                " select a pre-evacuation revision for a legacy comparison."
            )
        return names

    def read(self, filename):
        if self.stored_files is not None:
            if filename not in self.stored_files:
                raise ValueError(f"Unlisted release input: {filename}")
            return (self.directory / self.prefix / filename).read_text(encoding="utf-8")
        return _git(self.directory, "show", f"{self.commit}:{self.prefix}/{filename}")


@lru_cache(maxsize=64)
def resolve(rev):
    """Resolve a stored release, a MAM-basics ref, or explicit legacy:<ref>."""
    if rev.startswith("legacy:"):
        legacy_ref = rev.removeprefix("legacy:")
        repo = paths.sibling_repo("MAM-parsed")
        paths.require_sibling("MAM-parsed", repo)
        if not (repo / ".git").exists():
            raise FileNotFoundError(f"Legacy comparisons require a Git clone at {repo}")
        commit = _git(repo, "rev-parse", "--verify", f"{legacy_ref}^{{commit}}")
        date = _git(repo, "show", "-s", "--format=%cs", commit)
        return Revision(commit, date, repo, "plus")

    manifest = _manifest()
    if re.fullmatch(r"[0-9a-fA-F]{7,40}", rev):
        matches = [sha for sha in manifest["revisions"] if sha.startswith(rev.lower())]
        if len(matches) > 1:
            raise ValueError(f"Ambiguous stored MAM-parsed revision: {rev}")
        if matches:
            commit = matches[0]
            entry = manifest["revisions"][commit]
            return Revision(
                commit,
                entry["date"],
                paths.repo_root() / "MAM-parsed" / "historical" / commit,
                "plus",
                tuple(row["path"].removeprefix("plus/") for row in entry["files"]),
            )

    migration = manifest["migration"]
    repo = paths.repo_root()
    actual_ref = (
        migration["landing_commit"]
        if migration["source_commit"].startswith(rev) and len(rev) >= 7
        else rev
    )
    try:
        commit = _git(repo, "rev-parse", "--verify", f"{actual_ref}^{{commit}}")
    except RuntimeError as exc:
        raise ValueError(
            f"{rev!r} is neither a stored release nor a MAM-basics revision."
            " Arbitrary old MAM-parsed revisions require --legacy-history"
            " (or legacy:<ref>) and read access to a sibling MAM-parsed clone."
        ) from exc
    content_commit = _git(
        repo, "log", "-1", "--format=%H", commit, "--", "MAM-parsed/plus"
    )
    date = (
        migration["source_date"]
        if content_commit == migration["landing_commit"]
        else _git(repo, "show", "-s", "--format=%cs", content_commit or commit)
    )
    return Revision(commit, date, repo, "MAM-parsed/plus")


def count_newer_commits(rev):
    """Count source commits to migration, then commits changing landed plus data."""
    resolved = resolve(rev)
    if rev.startswith("legacy:"):
        return int(
            _git(resolved.directory, "rev-list", "--count", f"{resolved.commit}..HEAD")
        )
    manifest = _manifest()
    if resolved.stored_files is not None:
        distance = manifest["revisions"][resolved.commit]["commits_to_migration"]
        boundary = manifest["migration"]["landing_commit"]
    else:
        distance = 0
        boundary = resolved.commit
    return distance + int(
        _git(
            paths.repo_root(),
            "rev-list",
            "--count",
            f"{boundary}..HEAD",
            "--",
            "MAM-parsed/plus",
        )
    )
