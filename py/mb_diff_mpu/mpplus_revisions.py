"""Read stored release inputs and committed MAM-parsed data.

Named historical releases use the tracked snapshots in MAM-parsed/historical/.
HEAD and other current repository refs use MAM-parsed/plus/ in MAM-basics.
Only an explicit legacy: revision reads the sibling MAM-parsed Git repository.
That optional mode performs read-only Git operations and never fetches or clones.
"""

from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
import json
from pathlib import Path
import re
import subprocess
import zipfile

from mb_cmn import paths
from mb_cmn.git_process import git_command
from mb_cmn.new_york_time import new_york_date

_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
_ZIP_CREATE_SYSTEM = 3
_ZIP_EXTERNAL_ATTR = 0o100644 << 16


def _git(repo, *args):
    result = subprocess.run(
        git_command(repo, *args),
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
    """A resolved plus tree, the commit it is read from, and what a report records of it.

    ``commit`` is always the full 40-character hash of the commit the tree is read from,
    never the revision as given. A stored release or a legacy:<ref> is recorded by that
    commit and by ``date``. A MAM-basics ref is recorded by ``tree``, the git tree id of
    MAM-parsed/plus at ``commit``, and its ``date`` is empty; ``resolve`` says why.
    """

    commit: str
    date: str
    directory: Path
    prefix: str
    stored_files: tuple[str, ...] | None = None
    archive: Path | None = None
    tree: str | None = None

    @property
    def label(self):
        """The kind and id a report records: ("tree", tree id) or ("rev", commit hash)."""
        if self.tree is not None:
            return "tree", self.tree
        return "rev", self.commit

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

    A stored release and a legacy:<ref> are recorded by their MAM-parsed commit and its
    date. A MAM-basics ref is recorded by the git tree id of MAM-parsed/plus at the ref,
    and has no date.

    Every date is the commit's date in New York time, by Ben's decision of 2026-09-14,
    recorded in mb_cmn/new_york_time.py. A legacy:<ref>'s date is converted from git's
    committer time. A stored release's date is the manifest's, which a check that day
    against GitHub's UTC committer times found is already the New York date.

    WHY A TREE ID, AND NO DATE. Until 2026-09-14 a MAM-basics ref resolved to its content
    commit, the last commit at or before the ref that changed MAM-parsed/plus, found with
    ``git log --full-history -1`` and dated by that commit. Ben's decision of 2026-09-11
    was that the change log record "a true hash" rather than the literal HEAD, which
    names nothing once the report is committed. But that walk can be wrong in a shallow
    clone, such as a Claude cloud container's. Git treats each commit listed in
    .git/shallow as having no parents, so every path in it looks added, and the
    newest-first walk returns such a boundary commit whenever one is newer than the last
    real change. The report then published a wrong hash and date over correct diffs, as
    section 7 of doc/mega-timing-cloud-2026-09-14.md and its update record. On 2026-09-14
    Ben chose the tree id instead. ``git rev-parse <commit>:MAM-parsed/plus`` needs only
    the commit and its trees, which every shallow clone has, and prints the same id in
    every clone. A tree that a later commit restores gets its old id back, which is
    right, since the inputs are then identical: 73c6b113 restored 209b4c05's tree, and
    both carry 2072b5f9. So HEAD keeps one id until MAM-parsed/plus changes, and a report
    regenerated over unchanged inputs is byte-identical. In a clone with full history,
    ``git log --full-history --find-object=<tree id> -- MAM-parsed/plus`` lists the
    commits that introduced or removed a tree.

    TWO QUESTIONS, ONE ID. Ben observed on 2026-09-14, having chosen the tree id, that
    two distinct questions had been fused into one. The first is what a reader of the
    HTML report should see to identify what unpinned-latest describes: ideally something
    human-meaningful, such as a date, and human-useful, such as a commit hash a reader
    can look up on GitHub. The second is what, for internal use, should be the "stat"
    that says whether the report is stale, that is, whether the diff needs running at
    all. The tree id suits the second, since it is the same in every clone and changes
    exactly when MAM-parsed/plus does. The option offered for the first, and not taken,
    was to fetch the git history a shallow clone lacks, without file contents, before a
    cloud mega run. Unshallowing a depth-50 clone of 89f10bb4 that way grew its packs by
    2.6 MiB on 2026-09-14, after which the walk described above returned 73c6b113 again,
    a true commit hash and date. It was untried in a cloud container, whose clone is an
    ordinary shallow clone rather than a partial one, and a --filter fetch needs a
    promisor remote; a guard would also have had to raise whenever git log still
    returned a commit listed in .git/shallow.

    A revision naming the manifest's migration.source_commit, the last MAM-parsed commit
    before MAM-parsed's data moved into MAM-basics, reads migration.landing_commit, where
    that data landed, and is recorded like any other MAM-basics ref.
    """
    if rev.startswith("legacy:"):
        legacy_ref = rev.removeprefix("legacy:")
        repo = paths.sibling_repo("MAM-parsed")
        paths.require_sibling("MAM-parsed", repo)
        if not (repo / ".git").exists():
            raise FileNotFoundError(f"Legacy comparisons require a Git clone at {repo}")
        commit = _git(repo, "rev-parse", "--verify", f"{legacy_ref}^{{commit}}")
        committed = datetime.fromisoformat(
            _git(repo, "show", "-s", "--format=%cI", commit)
        )
        date = new_york_date(committed).isoformat()
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
    tree = _git(repo, "rev-parse", "--verify", f"{commit}:MAM-parsed/plus")
    return Revision(commit, "", repo, "MAM-parsed/plus", tree=tree)


# ``count_newer_commits`` stood here until 2026-09-11, counting the commits between a revision
# and HEAD by walking from the manifest's ``migration.landing_commit``. Its two callers were
# both in ``py/subcommands/diff_mpplus.py``, and both are gone: ``_latest_release_entry`` now walks
# ``releases.json``'s chain, and ``run_unpinned_latest``'s zero-count branch was doing the same
# work as the branch beside it. Deleted rather than kept, because the walk it needed is exactly
# what a shallow clone cannot do -- in a cloud container the landing commit is outside the
# window and the count died, taking the mega's ``diff-mpplus`` step with it. Ben's decision,
# 2026-09-11. Nothing now reads ``manifest["revisions"][<sha>]["commits_to_migration"]``; the
# key is left in the tracked manifest rather than migrated out of it. Nothing has read
# ``manifest["migration"]["source_date"]`` either since b5dd2ffb, which stopped dating a
# MAM-basics revision on 2026-09-14, and that key is left in the manifest as well.
