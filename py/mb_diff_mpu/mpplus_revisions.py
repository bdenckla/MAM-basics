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
import zipfile

from mb_cmn import paths

_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
_ZIP_CREATE_SYSTEM = 3
_ZIP_EXTERNAL_ATTR = 0o100644 << 16


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


def _listed_archive_members(prefix, stored_files):
    members = tuple(f"{prefix}/{name}" for name in stored_files)
    duplicates = sorted({name for name in members if members.count(name) > 1})
    if duplicates:
        raise ValueError(
            "Historical manifest has duplicate release inputs: " + ", ".join(duplicates)
        )
    return members


def _archive_members(archive_path, expected):
    try:
        stat = archive_path.stat()
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Stored MAM-parsed release archive is absent: {archive_path}"
        ) from exc
    return _validated_archive_members(
        str(archive_path), expected, stat.st_size, stat.st_mtime_ns
    )


@lru_cache(maxsize=32)
def _validated_archive_members(archive_name, expected, _size, _mtime_ns):
    archive_path = Path(archive_name)
    try:
        with zipfile.ZipFile(archive_path) as archive:
            infos = archive.infolist()
            names = tuple(info.filename for info in infos)
            duplicates = sorted({name for name in names if names.count(name) > 1})
            if duplicates:
                raise RuntimeError(
                    f"Stored MAM-parsed release archive {archive_path} has duplicate"
                    f" members: {', '.join(duplicates)}"
                )
            missing = sorted(set(expected) - set(names))
            unlisted = sorted(set(names) - set(expected))
            if missing or unlisted:
                details = []
                if missing:
                    details.append("missing " + ", ".join(missing))
                if unlisted:
                    details.append("unlisted " + ", ".join(unlisted))
                raise RuntimeError(
                    f"Stored MAM-parsed release archive {archive_path} differs from"
                    f" its manifest: {'; '.join(details)}"
                )
            if names != tuple(sorted(names)):
                raise RuntimeError(
                    f"Stored MAM-parsed release archive has unsorted members:"
                    f" {archive_path}"
                )
            if archive.comment:
                raise RuntimeError(
                    f"Stored MAM-parsed release archive has a comment: {archive_path}"
                )
            for info in infos:
                if (
                    info.is_dir()
                    or info.compress_type != zipfile.ZIP_STORED
                    or info.date_time != _ZIP_TIMESTAMP
                    or info.create_system != _ZIP_CREATE_SYSTEM
                    or info.external_attr != _ZIP_EXTERNAL_ATTR
                    or info.internal_attr != 0
                    or info.extra
                    or info.comment
                ):
                    raise RuntimeError(
                        f"Stored MAM-parsed release archive member has unexpected"
                        f" metadata: {archive_path}!{info.filename}"
                    )
            bad_member = archive.testzip()
            if bad_member is not None:
                raise RuntimeError(
                    f"Stored MAM-parsed release archive has a corrupt member:"
                    f" {archive_path}!{bad_member}"
                )
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        raise RuntimeError(
            f"Stored MAM-parsed release archive is corrupt: {archive_path}"
        ) from exc
    return names


@dataclass(frozen=True)
class Revision:
    """A resolved plus tree, its source commit, and its content date.

    ``commit`` is always the full 40-character hash of the commit the tree is read from,
    never the revision as given, so a report can record it as the source of its inputs.
    For a MAM-basics ref it is the ref's content commit, which ``resolve`` defines.
    """

    commit: str
    date: str
    directory: Path
    prefix: str
    stored_files: tuple[str, ...] | None = None
    archive: Path | None = None

    def _validate_archive(self):
        if self.archive is None:
            raise RuntimeError(
                f"Stored MAM-parsed release has no archive path: {self.commit}"
            )
        expected = _listed_archive_members(self.prefix, self.stored_files or ())
        _archive_members(self.archive, expected)

    def filenames(self):
        if self.stored_files is not None:
            names = list(self.stored_files)
            self._validate_archive()
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
            self._validate_archive()
            member = f"{self.prefix}/{filename}"
            try:
                with zipfile.ZipFile(self.archive) as archive:
                    return archive.read(member).decode("utf-8")
            except (OSError, UnicodeDecodeError, zipfile.BadZipFile) as exc:
                raise RuntimeError(
                    f"Stored MAM-parsed release input is corrupt:"
                    f" {self.archive}!{member}"
                ) from exc
        return _git(self.directory, "show", f"{self.commit}:{self.prefix}/{filename}")


@lru_cache(maxsize=64)
def resolve(rev):
    """Resolve a stored release, a MAM-basics ref, or explicit legacy:<ref>.

    A MAM-basics ref resolves to its content commit: the last commit at or before the
    ref that changed MAM-parsed/plus. MAM-parsed/plus is the same at both commits, so
    the inputs read are the same, and the content commit is the hash a report records.
    HEAD therefore resolves to one hash until a commit changes MAM-parsed/plus, and a
    report regenerated over unchanged inputs is byte-identical. Ben's decision,
    2026-09-11, was that the change log records "a true hash" rather than the literal
    HEAD, which names nothing once the report is committed.
    """
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
            archive = paths.repo_root() / "MAM-parsed" / "historical" / f"{commit}.zip"
            return Revision(
                commit,
                entry["date"],
                archive.parent,
                "plus",
                tuple(row["path"].removeprefix("plus/") for row in entry["files"]),
                archive,
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
    content_commit = (
        _git(repo, "log", "-1", "--format=%H", commit, "--", "MAM-parsed/plus")
        or commit
    )
    date = (
        migration["source_date"]
        if content_commit == migration["landing_commit"]
        else _git(repo, "show", "-s", "--format=%cs", content_commit)
    )
    return Revision(content_commit, date, repo, "MAM-parsed/plus")


# ``count_newer_commits`` stood here until 2026-09-11, counting the commits between a revision
# and HEAD by walking from the manifest's ``migration.landing_commit``. Its two callers were
# both in ``py/subcommands/diff_mpp.py``, and both are gone: ``_latest_release_entry`` now walks
# ``releases.json``'s chain, and ``run_unpinned_latest``'s zero-count branch was doing the same
# work as the branch beside it. Deleted rather than kept, because the walk it needed is exactly
# what a shallow clone cannot do -- in a cloud container the landing commit is outside the
# window and the count died, taking the mega's ``diff-mpp`` step with it. Ben's decision,
# 2026-09-11. Nothing now reads ``manifest["revisions"][<sha>]["commits_to_migration"]``; the
# key is left in the tracked manifest rather than migrated out of it.
