"""Taamey D's release tool: py/main_taamey_d.py release-check and release-publish.

This module was restructured on 2026-10-29 from hbofonts' py/main_release.py, at hbofonts
3b59254a, in Phase 4 of MAM-private's doc/PLAN-evacuate-hbofonts-into-MAM-basics.md.  It
builds and checks Taamey D's public downloads tree, gh-pages/taamey-d/downloads/: the
index, one immutable directory under snapshots/ for each release, and latest/, a
byte-identical copy of the newest.  A snapshot is named
<version>-MAM-basics-<first 12 hex digits of its source commit>.  It holds a binary
archive, a corresponding-source archive, their checksums and a provenance manifest, whose
format continues hbofonts' schema 2.

hbofonts' rules came over unchanged.  A committed snapshot never changes or disappears,
which is checked both in the working tree against HEAD and through Git's history.
latest/ is replaced only once the new snapshot is verified, with a backup to roll back
to.  release-publish builds the snapshot twice, in two scratch roots, and compares the
two builds and checks both before installing either.  Its source commit is HEAD, given
in full, and every release input in the working tree equals its committed bytes.  The
release notes' first line is "Taamey D <version>".  Each archive holds exactly its
allowlisted members, and the index's links resolve.

What existed only for hbofonts' history was dropped: its schema-1 manifests (the
original Taamey_D release and two three-font snapshots), with their archive names,
paths, pinned commits and hashes, the transitional latest/, the build scripts of
hbofonts' PowerShell era, and its releases/ directory.  hbofonts' downloads stay
published from hbofonts, frozen, and the index here links them by absolute URL from
the constant tables _HBOFONTS_SNAPSHOTS and _HBOFONTS_BUNDLES below.  This tool reads
neither hbofonts' checkout nor its site.

Before the first release, when neither gh-pages/taamey-d/downloads/ nor any path under
it in Git's history exists, release-check says that no snapshot is published, and
release-publish creates the tree.  A payload's source commit missing from this
repository raises ReleaseError, or, in a shallow clone, its subclass
SourceCommitOutsideShallowHistory, so that the mega can tell a cloud session's shallow
checkout apart.
"""

from __future__ import annotations

import datetime
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import uuid
import zipfile
import zlib
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import NamedTuple
from urllib.parse import urlsplit

from mb_cmn import new_york_time
from mb_cmn import paths
from mb_cmn.git_process import git_command

_REPO_ROOT = paths.repo_root()
# The downloads tree, as Git names it from the repository root, and on disk.
_DOWNLOADS_PATH = "gh-pages/taamey-d/downloads"
_SNAPSHOTS_PATH = f"{_DOWNLOADS_PATH}/snapshots"
_DOWNLOADS_ROOT = _REPO_ROOT / _DOWNLOADS_PATH
# A snapshot's directory, gh-pages/taamey-d/downloads/snapshots/<name>, has five path
# parts, and every file of it at least six.  hbofonts' gh-pages/downloads/snapshots/<name>
# had four.
_SNAPSHOT_LEAF_DEPTH = len(PurePosixPath(_SNAPSHOTS_PATH).parts) + 1

_SOURCE_REPOSITORY = "https://github.com/bdenckla/MAM-basics"
# The repository named in each snapshot's name, as hbofonts' were named for hbofonts.
_SNAPSHOT_HOST = "MAM-basics"
_BINARY_ARCHIVE_NAME = "Taamey_D.zip"
_SOURCE_ARCHIVE_NAME = "Taamey_D-sources.zip"
_CHECKSUM_NAME = "SHA256SUMS.txt"
_PROVENANCE_NAME = "provenance.json"
_PAYLOAD_NAMES = (
    _BINARY_ARCHIVE_NAME,
    _SOURCE_ARCHIVE_NAME,
    _CHECKSUM_NAME,
    _PROVENANCE_NAME,
)
_MANIFEST_KEYS = frozenset(
    {
        "schema_version",
        "kind",
        "projection",
        "identifier",
        "published_date",
        "source",
        "files",
    }
)
_FONT_DIR = "Taamey-D/font-m-TaD"
_FONT_STEM = "Taamey_D"
_VERSION_PATH = "py/taamey_d_build/font_version.py"
_VERSION_LINE = re.compile(rb'VERSION = "([0-9]+(?:\.[0-9]+)+)"')
# Authored notes for the release, archived in the binary archive only.
_RELEASE_NOTES_NAME = "release-notes.txt"
_RELEASE_NOTES_PATH = f"{_FONT_DIR}/{_RELEASE_NOTES_NAME}"
# The build's entry point and package, which ship in the source archive under
# GPL-2.0-or-later.  release-publish refuses a commit whose tracked files under the
# package differ from this list's, so that a module added to the build later cannot
# silently fall out of the source archive.  Every published snapshot is checked against
# this list too, so changing it would refuse the snapshots published before the change:
# the list must then be chosen by each snapshot's source commit, as hbofonts' release
# tool chose between its build scripts by commit.
_BUILD_PACKAGE_PATH = "py/taamey_d_build"
_BUILD_SOURCE_PATHS = (
    "py/main_taamey_d_build.py",
    f"{_BUILD_PACKAGE_PATH}/fill_in_template.py",
    f"{_BUILD_PACKAGE_PATH}/font_version.py",
    f"{_BUILD_PACKAGE_PATH}/my_open.py",
)
_ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


class _FrozenDownload(NamedTuple):
    """One of hbofonts' frozen downloads, as the index here lists it."""

    heading: str
    label: str
    # The download's directory, relative to _HBOFONTS_DOWNLOADS_URL.
    directory: str
    binary_name: str
    source_name: str
    # Further (URL, link text) pairs listed with the download.
    extra_links: tuple[tuple[str, str], ...] = ()


# hbofonts' downloads, published from hbofonts before Taamey D moved here.  They stay on
# hbofonts' Pages site, frozen: its downloads/latest/ stays at Taamey D 1.1.  Their URLs
# are public.  The index links every one by absolute URL, and its check requires every
# link these tables make, so that an edit cannot silently drop one.
_HBOFONTS_DOWNLOADS_URL = "https://bdenckla.github.io/hbofonts/downloads/"
# hbofonts' Taamey D snapshots, newest first.
_HBOFONTS_SNAPSHOTS = (
    _FrozenDownload(
        "Taamey D 1.1",
        "1.1",
        "snapshots/1.1-hbofonts-5d9d8d461f79",
        _BINARY_ARCHIVE_NAME,
        _SOURCE_ARCHIVE_NAME,
    ),
    _FrozenDownload(
        "Taamey D 1.0",
        "1.0",
        "snapshots/1.0-hbofonts-68cd62902202",
        _BINARY_ARCHIVE_NAME,
        _SOURCE_ARCHIVE_NAME,
    ),
    _FrozenDownload(
        "Taamey D 0.931",
        "0.931",
        "snapshots/0.931-hbofonts-42ca46e82f78",
        _BINARY_ARCHIVE_NAME,
        _SOURCE_ARCHIVE_NAME,
    ),
)
# The historical three-font bundles of Shofar D, Taamey B and Taamey D, newest first,
# and the original Taamey_D release tag.
_HBOFONTS_BUNDLES = (
    _FrozenDownload(
        "hbofonts 0.930",
        "0.930",
        "snapshots/0.930-hbofonts-89319d10d7d8",
        "Taamey_D_and_friends.zip",
        "Taamey_D_and_friends-sources.zip",
    ),
    _FrozenDownload(
        "hbofonts 0.921",
        "0.921",
        "snapshots/0.921-hbofonts-a02eaa6a75d8",
        "Taamey_D_and_friends.zip",
        "Taamey_D_and_friends-sources.zip",
    ),
    _FrozenDownload(
        "Original Taamey_D v0.921-2 release",
        "v0.921-2",
        "releases/v0.921-2",
        "Taamey_D_and_friends.zip",
        "Taamey_D_and_friends-sources.zip",
        (
            (
                "https://github.com/bdenckla/Taamey_D/releases/tag/v0.921-2",
                "Original v0.921-2 GitHub release",
            ),
        ),
    ),
)


class ReleaseError(RuntimeError):
    """A public-release invariant failed."""


class SourceCommitOutsideShallowHistory(ReleaseError):
    """A shallow clone lacks the source commit of one or more published payloads.

    Raised only when ``git rev-parse --is-shallow-repository`` says the clone is shallow,
    and before any archive is checked against Git.  ``missing`` maps each payload's
    directory, relative to gh-pages/taamey-d/downloads/, such as ``latest``, to its
    source commit.  A full clone lacking a source commit raises ReleaseError itself.
    """

    def __init__(self, missing: dict[str, str]) -> None:
        self.missing = dict(missing)
        super().__init__(
            "this shallow clone's history lacks the source commit of "
            + _payload_commits(self.missing)
        )


def _payload_commits(missing: dict[str, str]) -> str:
    return ", ".join(f"{name} ({commit})" for name, commit in sorted(missing.items()))


def _binary_inputs() -> dict[str, Path]:
    filenames = [
        "license.txt",
        f"{_FONT_STEM}.ttf",
        f"{_FONT_STEM}.woff",
        f"{_FONT_STEM}.woff2",
        _RELEASE_NOTES_NAME,
    ]
    return {
        f"{_FONT_STEM}/{filename}": _REPO_ROOT / _FONT_DIR / filename
        for filename in filenames
    }


def _source_inputs() -> dict[str, Path]:
    # Each member sits at its path in this repository.
    inputs = {path: _REPO_ROOT / path for path in _BUILD_SOURCE_PATHS}
    for filename in (
        "license.sym.txt",
        "license.txt",
        "ffscript_generate_sfd_n_ttf.py",
        f"{_FONT_STEM}-nofea.sym.sfd",
        f"{_FONT_STEM}.sym.fea",
    ):
        path = f"{_FONT_DIR}/{filename}"
        inputs[path] = _REPO_ROOT / path
    return inputs


_BINARY_PATHS = frozenset(_binary_inputs())
_SOURCE_PATHS = frozenset(_source_inputs())


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git_run(*arguments: str) -> subprocess.CompletedProcess[bytes]:
    # git_command trusts exactly this repository, through a per-command safe.directory.
    return subprocess.run(
        git_command(_REPO_ROOT, *arguments), capture_output=True, check=False
    )


def _git_bytes(*arguments: str) -> bytes:
    result = _git_run(*arguments)
    if result.returncode:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise ReleaseError(f"git {' '.join(arguments)} failed: {stderr}")
    return result.stdout


def _git_text(*arguments: str) -> str:
    return _git_bytes(*arguments).decode("utf-8").strip()


def _git_succeeds(*arguments: str) -> bool:
    return _git_run(*arguments).returncode == 0


def _git_names(*arguments: str) -> list[str]:
    # The file names that a command run with -z prints, each ended by a NUL.
    return [name for name in _git_bytes(*arguments).decode("utf-8").split("\0") if name]


def _version_at_commit(source_commit: str) -> str:
    version_source = _git_bytes("show", f"{source_commit}:{_VERSION_PATH}")
    # The file has a license header and a docstring, so read its one VERSION line, with
    # an LF or a CRLF ending, rather than matching the whole file.  A second line
    # beginning VERSION would be a second assignment, so it is refused too.
    lines = [line.removesuffix(b"\r") for line in version_source.split(b"\n")]
    assignments = [line for line in lines if line.startswith(b"VERSION")]
    match = _VERSION_LINE.fullmatch(assignments[0]) if len(assignments) == 1 else None
    if match is None:
        raise ReleaseError(
            f"{source_commit}:{_VERSION_PATH} does not contain exactly one line"
            ' VERSION = "<digits and dots>"'
        )
    return match.group(1).decode("ascii")


def _snapshot_identifier(source_commit: str) -> str:
    version = _version_at_commit(source_commit)
    return f"{version}-{_SNAPSHOT_HOST}-{source_commit[:12]}"


def _version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def _path_at_commit(source_commit: str, path: str) -> bool:
    return bool(_git_names("ls-tree", "-z", "--name-only", source_commit, "--", path))


def _release_notes_at_commit(source_commit: str) -> str:
    """Return the commit's release notes, which every snapshot's commit has."""
    if not _path_at_commit(source_commit, _RELEASE_NOTES_PATH):
        raise ReleaseError(f"{_RELEASE_NOTES_PATH} does not exist at {source_commit}")
    notes = _git_bytes("show", f"{source_commit}:{_RELEASE_NOTES_PATH}")
    try:
        return notes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ReleaseError(
            f"{source_commit}:{_RELEASE_NOTES_PATH} is not UTF-8"
        ) from error


def _require_release_notes(source_commit: str) -> None:
    notes = _release_notes_at_commit(source_commit)
    expected = f"Taamey D {_version_at_commit(source_commit)}"
    first_line = notes.split("\n", 1)[0]
    if first_line != expected:
        raise ReleaseError(
            f"the first line of {source_commit}:{_RELEASE_NOTES_PATH} is "
            f"{first_line!r}, not {expected!r}"
        )


def _verify_inputs_at_commit(source_commit: str) -> None:
    head = _git_text("rev-parse", "HEAD")
    if head != source_commit:
        raise ReleaseError(
            f"snapshot commit {source_commit} is not current HEAD {head}"
        )
    inputs = set(_binary_inputs().values()) | set(_source_inputs().values())
    mismatches = []
    for path in sorted(inputs):
        relative_path = path.relative_to(_REPO_ROOT).as_posix()
        committed = _git_bytes("show", f"{source_commit}:{relative_path}")
        if not path.is_file() or path.read_bytes() != committed:
            mismatches.append(relative_path)
    if mismatches:
        raise ReleaseError(
            "current release inputs differ from the snapshot commit: "
            + ", ".join(mismatches)
        )


def _require_build_package_allowlisted(source_commit: str) -> None:
    prefix = f"{_BUILD_PACKAGE_PATH}/"
    tracked = frozenset(
        name
        for name in _git_names(
            "ls-tree", "-r", "-z", "--name-only", source_commit, "--", prefix
        )
        if name.startswith(prefix)
    )
    allowlisted = frozenset(path for path in _SOURCE_PATHS if path.startswith(prefix))
    if tracked != allowlisted:
        raise ReleaseError(
            f"the tracked files of {prefix} at {source_commit} differ from the source"
            f" archive's allowlist; not allowlisted={sorted(tracked - allowlisted)!r},"
            f" not tracked={sorted(allowlisted - tracked)!r}"
        )


def _require_files(inputs: dict[str, Path]) -> None:
    missing = [str(path) for path in inputs.values() if not path.is_file()]
    if missing:
        raise ReleaseError("missing release input(s): " + ", ".join(missing))


def _write_zip(path: Path, inputs: dict[str, Path]) -> None:
    _require_files(inputs)
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for archive_path, source_path in sorted(inputs.items()):
            info = zipfile.ZipInfo(archive_path, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source_path.read_bytes(), compresslevel=9)


def _safe_member_name(name: str) -> str:
    if "\\" in name:
        raise ReleaseError(f"ZIP member uses a backslash: {name!r}")
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ReleaseError(f"unsafe ZIP member path: {name!r}")
    return path.as_posix()


def _member_hashes(path: Path) -> dict[str, dict[str, int | str]]:
    if not path.is_file():
        raise ReleaseError(f"archive does not exist: {path}")
    members: dict[str, dict[str, int | str]] = {}
    # A damaged archive raises ReleaseError too, rather than zipfile's or zlib's own
    # errors, as every failed check does.
    try:
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                name = _safe_member_name(info.filename)
                if info.is_dir():
                    continue
                if name in members:
                    raise ReleaseError(f"duplicate ZIP member in {path}: {name}")
                data = archive.read(info)
                members[name] = {"size": len(data), "sha256": _sha256_bytes(data)}
    except (zipfile.BadZipFile, zlib.error, EOFError) as error:
        raise ReleaseError(f"unreadable ZIP archive {path}: {error}") from error
    if not members:
        raise ReleaseError(f"archive has no files: {path}")
    return members


def _validate_source_member_names(names: frozenset[str], label: str) -> None:
    for name in names:
        lowered_parts = [part.lower() for part in PurePosixPath(name).parts]
        if any("keter" in part for part in lowered_parts):
            raise ReleaseError(f"{label} exposes Keter material: {name}")
        if name.endswith(".sfd") and not name.endswith("-nofea.sym.sfd"):
            raise ReleaseError(f"{label} exposes a plain SFD: {name}")
        if name.endswith(".fea") and not name.endswith(".sym.fea"):
            raise ReleaseError(f"{label} exposes a plain feature file: {name}")


def _validate_archive(
    path: Path, expected_paths: frozenset[str], label: str
) -> dict[str, dict[str, int | str]]:
    members = _member_hashes(path)
    allowed_directories = {
        parent.as_posix()
        for name in expected_paths
        for parent in PurePosixPath(name).parents
        if parent != PurePosixPath(".")
    }
    directory_names = set()
    casefolded_names = set()
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            name = _safe_member_name(info.filename)
            folded = name.casefold()
            if folded in casefolded_names:
                raise ReleaseError(
                    f"case-folding ZIP member collision in {path}: {name}"
                )
            casefolded_names.add(folded)
            if info.is_dir():
                directory_names.add(name)
    unexpected_directories = sorted(directory_names - allowed_directories)
    if unexpected_directories:
        raise ReleaseError(
            f"{label} has unexpected directories: {unexpected_directories!r}"
        )
    actual_paths = frozenset(members)
    missing = sorted(expected_paths - actual_paths)
    extra = sorted(actual_paths - expected_paths)
    if missing or extra:
        raise ReleaseError(
            f"{label} member allowlist mismatch; missing={missing!r}, extra={extra!r}"
        )
    if "source" in label:
        _validate_source_member_names(actual_paths, label)
    return members


def _validate_archive_against_git(
    path: Path, inputs: dict[str, Path], source_commit: str, label: str
) -> None:
    members = _member_hashes(path)
    for archive_path, repository_path in sorted(inputs.items()):
        relative_path = repository_path.relative_to(_REPO_ROOT).as_posix()
        committed = _git_bytes("show", f"{source_commit}:{relative_path}")
        expected = {"size": len(committed), "sha256": _sha256_bytes(committed)}
        if members.get(archive_path) != expected:
            raise ReleaseError(
                f"{label} member {archive_path} does not match "
                f"{source_commit}:{relative_path}"
            )


def _archive_record(
    path: Path, expected_paths: frozenset[str], label: str
) -> dict[str, object]:
    members = _validate_archive(path, expected_paths, label)
    return {
        "size": path.stat().st_size,
        "sha256": _sha256_file(path),
        "member_count": len(members),
        "members": [{"path": name, **members[name]} for name in sorted(members)],
    }


def _write_checksums(directory: Path, records: dict[str, dict[str, object]]) -> None:
    lines = [f"{records[name]['sha256']}  {name}\n" for name in sorted(records)]
    (directory / _CHECKSUM_NAME).write_text(
        "".join(lines), encoding="utf-8", newline="\n"
    )


def _write_provenance(directory: Path, manifest: dict[str, object]) -> None:
    text = json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    (directory / _PROVENANCE_NAME).write_text(text, encoding="utf-8", newline="\n")


def _build_snapshot(directory: Path, source_commit: str, published_date: str) -> None:
    directory.mkdir(parents=True)
    binary_archive = directory / _BINARY_ARCHIVE_NAME
    source_archive = directory / _SOURCE_ARCHIVE_NAME
    _write_zip(binary_archive, _binary_inputs())
    _write_zip(source_archive, _source_inputs())
    records = {
        _BINARY_ARCHIVE_NAME: _archive_record(
            binary_archive, _BINARY_PATHS, "built binary archive"
        ),
        _SOURCE_ARCHIVE_NAME: _archive_record(
            source_archive, _SOURCE_PATHS, "built source archive"
        ),
    }
    identifier = _snapshot_identifier(source_commit)
    manifest = {
        "schema_version": 2,
        "kind": "current-snapshot",
        "projection": "taamey-d-only",
        "identifier": identifier,
        "published_date": published_date,
        "source": {
            "repository": _SOURCE_REPOSITORY,
            "commit": source_commit,
        },
        "files": records,
    }
    _write_checksums(directory, records)
    _write_provenance(directory, manifest)


def _tree_hashes(directory: Path) -> dict[str, str]:
    return {
        path.relative_to(directory).as_posix(): _sha256_file(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def _validate_payload_names(directory: Path, payload_names: tuple[str, ...]) -> None:
    if not directory.is_dir():
        raise ReleaseError(f"payload directory does not exist: {directory}")
    actual = frozenset(path.name for path in directory.iterdir() if path.is_file())
    expected = frozenset(payload_names)
    if actual != expected:
        raise ReleaseError(
            f"payload file mismatch in {directory}; "
            f"missing={sorted(expected - actual)!r}, extra={sorted(actual - expected)!r}"
        )
    subdirectories = [path for path in directory.iterdir() if path.is_dir()]
    if subdirectories:
        raise ReleaseError(f"unexpected payload subdirectories in {directory}")


def _read_manifest(directory: Path) -> dict[str, object]:
    try:
        manifest = json.loads(
            (directory / _PROVENANCE_NAME).read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as error:
        raise ReleaseError(
            f"invalid provenance manifest in {directory}: {error}"
        ) from error
    if not isinstance(manifest, dict):
        raise ReleaseError(f"provenance manifest is not an object in {directory}")
    return manifest


def _check_checksums(directory: Path, records: dict[str, dict[str, object]]) -> None:
    expected = "".join(
        f"{records[name]['sha256']}  {name}\n" for name in sorted(records)
    )
    actual = (directory / _CHECKSUM_NAME).read_text(encoding="utf-8")
    if actual != expected:
        raise ReleaseError(f"checksum file does not match archives in {directory}")


def _is_iso_date(value: object) -> bool:
    if not isinstance(value, str) or not _ISO_DATE.fullmatch(value):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _check_payload(directory: Path) -> dict[str, object]:
    manifest = _read_manifest(directory)
    if manifest.get("schema_version") != 2:
        raise ReleaseError(f"unknown provenance schema in {directory}")
    if manifest.get("kind") != "current-snapshot":
        raise ReleaseError(f"unexpected manifest kind in {directory}")
    if manifest.get("projection") != "taamey-d-only":
        raise ReleaseError(f"manifest projection changed in {directory}")
    source = manifest.get("source")
    if not isinstance(source, dict) or set(source) != {"repository", "commit"}:
        raise ReleaseError(f"manifest source shape changed in {directory}")
    if source.get("repository") != _SOURCE_REPOSITORY:
        raise ReleaseError(f"manifest repository changed in {directory}")
    commit = str(source.get("commit"))
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ReleaseError(f"manifest commit is invalid in {directory}")
    if manifest.get("identifier") != _snapshot_identifier(commit):
        raise ReleaseError(f"manifest identifier changed in {directory}")
    if set(manifest) != _MANIFEST_KEYS:
        raise ReleaseError(f"provenance manifest key mismatch in {directory}")
    if not _is_iso_date(manifest.get("published_date")):
        raise ReleaseError(f"invalid publication date in {directory}")
    _validate_payload_names(directory, _PAYLOAD_NAMES)
    binary_path = directory / _BINARY_ARCHIVE_NAME
    source_path = directory / _SOURCE_ARCHIVE_NAME
    records = {
        _BINARY_ARCHIVE_NAME: _archive_record(
            binary_path, _BINARY_PATHS, f"{directory.name} binary archive"
        ),
        _SOURCE_ARCHIVE_NAME: _archive_record(
            source_path, _SOURCE_PATHS, f"{directory.name} source archive"
        ),
    }
    if manifest.get("files") != records:
        raise ReleaseError(
            f"provenance file records do not match archives in {directory}"
        )
    _check_checksums(directory, records)
    _validate_archive_against_git(
        binary_path, _binary_inputs(), commit, f"{directory.name} binary archive"
    )
    _validate_archive_against_git(
        source_path, _source_inputs(), commit, f"{directory.name} source archive"
    )
    return manifest


def _copy_immutable(source: Path, destination: Path) -> None:
    if destination.exists():
        if not destination.is_dir() or _tree_hashes(source) != _tree_hashes(
            destination
        ):
            raise ReleaseError(
                f"refusing to overwrite immutable destination: {destination}"
            )
        print(f"Verified existing immutable destination: {destination}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    incoming = destination.parent / f"{destination.name}.tmp.{uuid.uuid4().hex}"
    shutil.copytree(source, incoming)
    try:
        if _tree_hashes(source) != _tree_hashes(incoming):
            raise ReleaseError(
                f"immutable staging copy failed verification: {incoming}"
            )
        try:
            incoming.rename(destination)
        except FileExistsError:
            if not destination.is_dir() or _tree_hashes(source) != _tree_hashes(
                destination
            ):
                raise ReleaseError(
                    "immutable destination appeared with different content: "
                    f"{destination}"
                )
            print(f"Verified concurrent immutable destination: {destination}")
    finally:
        if incoming.exists():
            shutil.rmtree(incoming)


def _safe_remove_scratch(path: Path) -> None:
    resolved = path.resolve()
    if resolved.parent != _REPO_ROOT.resolve() or ".tmp." not in resolved.name:
        raise ReleaseError(f"refusing to remove non-scratch path: {resolved}")
    shutil.rmtree(resolved)


def _replace_latest(source: Path) -> None:
    _DOWNLOADS_ROOT.mkdir(parents=True, exist_ok=True)
    nonce = uuid.uuid4().hex
    incoming = _DOWNLOADS_ROOT / f"latest.tmp.{nonce}"
    backup = _DOWNLOADS_ROOT / f"latest-backup.tmp.{nonce}"
    latest = _DOWNLOADS_ROOT / "latest"
    shutil.copytree(source, incoming)
    backup_created = False
    new_latest_installed = False
    try:
        if latest.exists():
            latest.rename(backup)
            backup_created = True
        incoming.rename(latest)
        new_latest_installed = True
        _check_payload(latest)
    except Exception:
        if new_latest_installed and latest.exists():
            shutil.rmtree(latest)
        if backup_created and backup.exists():
            backup.rename(latest)
        if incoming.exists():
            shutil.rmtree(incoming)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def _manifest_commit(manifest: dict[str, object], directory: Path) -> str:
    source = manifest.get("source")
    commit = str(source.get("commit")) if isinstance(source, dict) else ""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ReleaseError(f"snapshot manifest has no full source commit: {directory}")
    return commit


def _require_source_commits(directories: list[Path]) -> None:
    # Looks up every payload's source commit before any payload is checked against Git,
    # so that whether a commit is missing, and so whether the outcome is the shallow
    # clone's dedicated error, does not depend on the order of the checks.
    missing = {}
    for directory in directories:
        commit = _manifest_commit(_read_manifest(directory), directory)
        if not _git_succeeds("cat-file", "-e", f"{commit}^{{commit}}"):
            missing[directory.relative_to(_DOWNLOADS_ROOT).as_posix()] = commit
    if not missing:
        return
    if _git_text("rev-parse", "--is-shallow-repository") == "true":
        raise SourceCommitOutsideShallowHistory(missing)
    raise ReleaseError(
        "this repository lacks the source commit of " + _payload_commits(missing)
    )


def _earlier_snapshots(current_identifier: str) -> list[tuple[str, str]]:
    """Return (version, identifier) for every other snapshot, newest first."""
    snapshots = []
    for directory in (_DOWNLOADS_ROOT / "snapshots").iterdir():
        if not directory.is_dir() or directory.name == current_identifier:
            continue
        manifest = _read_manifest(directory)
        version = _version_at_commit(_manifest_commit(manifest, directory))
        sort_key = (
            _version_tuple(version),
            str(manifest.get("published_date")),
            directory.name,
        )
        snapshots.append((sort_key, version, directory.name))
    snapshots.sort(reverse=True)
    return [(version, identifier) for _, version, identifier in snapshots]


def _archive_item(
    directory: str,
    label: str,
    binary_name: str = _BINARY_ARCHIVE_NAME,
    source_name: str = _SOURCE_ARCHIVE_NAME,
) -> str:
    """Return a list item for a binary archive, with its companions nested."""
    return (
        "      <li>\n"
        f'        <a href="{directory}/{binary_name}">{label} binary archive</a>\n'
        "        <ul>\n"
        f'          <li><a href="{directory}/{source_name}">'
        f"{label} corresponding-source archive</a></li>\n"
        f'          <li><a href="{directory}/{_CHECKSUM_NAME}">'
        f"{label} checksums</a></li>\n"
        f'          <li><a href="{directory}/{_PROVENANCE_NAME}">'
        f"{label} provenance</a></li>\n"
        "        </ul>\n"
        "      </li>\n"
    )


def _link_list(*items: str) -> str:
    return "    <ul>\n" + "".join(items) + "    </ul>\n"


def _frozen_download_section(download: _FrozenDownload) -> str:
    directory = f"{_HBOFONTS_DOWNLOADS_URL}{download.directory}"
    items = [
        _archive_item(
            directory, download.label, download.binary_name, download.source_name
        )
    ]
    items.extend(
        f'      <li><a href="{url}">{text}</a></li>\n'
        for url, text in download.extra_links
    )
    return f"    <h3>{download.heading}</h3>\n" + _link_list(*items)


def _frozen_hbofonts_hrefs() -> frozenset[str]:
    """Every link that the index makes from the tables of hbofonts' downloads."""
    hrefs = set()
    for download in (*_HBOFONTS_SNAPSHOTS, *_HBOFONTS_BUNDLES):
        directory = f"{_HBOFONTS_DOWNLOADS_URL}{download.directory}"
        for name in (
            download.binary_name,
            download.source_name,
            _CHECKSUM_NAME,
            _PROVENANCE_NAME,
        ):
            hrefs.add(f"{directory}/{name}")
        hrefs.update(url for url, _ in download.extra_links)
    return frozenset(hrefs)


def _write_download_index(snapshot_identifier: str) -> None:
    snapshot_directory = _DOWNLOADS_ROOT / "snapshots" / snapshot_identifier
    notes = _release_notes_at_commit(
        _manifest_commit(_read_manifest(snapshot_directory), snapshot_directory)
    )
    sections = [
        "    <h1>Taamey D downloads</h1>\n"
        "    <p>\n"
        "      The current binary archive contains Taamey D in TTF, WOFF, and WOFF2\n"
        "      formats with its license and release notes.\n"
        "    </p>\n",
        "    <h2>Current Taamey D snapshot</h2>\n"
        "    <p>\n"
        f"      Snapshot <code>{snapshot_identifier}</code> is immutable. The stable\n"
        "      <code>latest</code> paths below are byte-identical copies and may advance\n"
        "      with a later Taamey D release.\n"
        "    </p>\n"
        + _link_list(
            _archive_item(f"snapshots/{snapshot_identifier}", "Snapshot"),
            _archive_item("latest", "Latest"),
        ),
        "    <h2>Release notes</h2>\n"
        f"    <pre>\n{html.escape(notes, quote=False)}</pre>\n",
    ]
    earlier = _earlier_snapshots(snapshot_identifier)
    if earlier:
        sections.append(
            "    <h2>Earlier Taamey D snapshots</h2>\n"
            + "".join(
                f"    <h3>Taamey D {version}</h3>\n"
                + _link_list(_archive_item(f"snapshots/{identifier}", version))
                for version, identifier in earlier
            )
        )
    sections.append(
        "    <h2>Taamey D snapshots published from hbofonts</h2>\n"
        "    <p>\n"
        "      These immutable snapshots, and the historical bundles below them, were\n"
        "      published from the hbofonts repository before Taamey D moved to\n"
        "      MAM-basics. They stay on hbofonts' site, where\n"
        "      <code>downloads/latest/</code> stays frozen at Taamey D 1.1.\n"
        "    </p>\n"
        + "".join(
            _frozen_download_section(download) for download in _HBOFONTS_SNAPSHOTS
        )
    )
    sections.append(
        "    <h2>Historical three-font bundles</h2>\n"
        "    <p>\n"
        "      These immutable bundles preserve the former Shofar D, Taamey B, and\n"
        "      Taamey D release set. They remain available as historical artifacts and\n"
        "      are not rebuilt by the current release process.\n"
        "    </p>\n"
        + "".join(_frozen_download_section(download) for download in _HBOFONTS_BUNDLES)
    )
    sections.append(
        '    <p><a href="../Taamey_D.html">'
        "Return to the Taamey D documentation</a>.</p>\n"
    )
    body = "\n".join(sections)
    text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Taamey D downloads</title>
  <style>
    body {{
      max-width: 52rem;
      margin: 0 auto;
      padding: 2rem 1.25rem;
      font-family: system-ui, sans-serif;
      line-height: 1.55;
    }}
    code {{ overflow-wrap: anywhere; }}
    li + li {{ margin-top: 0.35rem; }}
    pre {{ white-space: pre-wrap; }}
  </style>
</head>
<body>
  <main>
{body}  </main>
</body>
</html>
"""
    (_DOWNLOADS_ROOT / "index.html").write_text(text, encoding="utf-8", newline="\n")


class _DownloadIndexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for name, value in attrs:
            if name == "href" and value is not None:
                self.hrefs.add(value)


def _check_download_index(
    latest_manifest: dict[str, object], snapshots: list[str]
) -> None:
    index_path = _DOWNLOADS_ROOT / "index.html"
    parser = _DownloadIndexParser()
    parser.feed(index_path.read_text(encoding="utf-8"))
    pages_root = (_REPO_ROOT / "gh-pages").resolve()
    for href in sorted(parser.hrefs):
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (_DOWNLOADS_ROOT / parsed.path).resolve()
        try:
            target.relative_to(pages_root)
        except ValueError as error:
            raise ReleaseError(
                f"download index link escapes gh-pages: {href}"
            ) from error
        if not target.exists():
            raise ReleaseError(f"download index has a broken local link: {href}")

    identifier = str(latest_manifest.get("identifier"))
    required = {
        f"latest/{_BINARY_ARCHIVE_NAME}",
        f"latest/{_SOURCE_ARCHIVE_NAME}",
        f"snapshots/{identifier}/{_BINARY_ARCHIVE_NAME}",
        f"snapshots/{identifier}/{_SOURCE_ARCHIVE_NAME}",
    }
    # Every snapshot stays linked, not only the current one, and so does every one of
    # hbofonts' frozen downloads.
    for snapshot in snapshots:
        required.add(f"snapshots/{snapshot}/{_BINARY_ARCHIVE_NAME}")
        required.add(f"snapshots/{snapshot}/{_SOURCE_ARCHIVE_NAME}")
    required |= _frozen_hbofonts_hrefs()
    missing = sorted(required - parser.hrefs)
    if missing:
        raise ReleaseError(f"download index is missing required links: {missing!r}")


def _new_york_date_today() -> str:
    # A release date, which takes no zone label, but New York's date rather than this
    # machine's, as py/mb_cmn/new_york_time.py says of dates generated from a clock.
    moment = datetime.datetime.now(datetime.UTC)
    return new_york_time.new_york_date(moment).isoformat()


def _check_append_only(base: str) -> None:
    prefix = f"{_SNAPSHOTS_PATH}/"
    base_paths = [
        path
        for path in _git_names(
            "ls-tree", "-r", "-z", "--name-only", base, "--", _SNAPSHOTS_PATH
        )
        if path.startswith(prefix)
    ]
    leaves: dict[str, set[str]] = {}
    for path in base_paths:
        parts = PurePosixPath(path).parts
        if len(parts) <= _SNAPSHOT_LEAF_DEPTH:
            raise ReleaseError(f"invalid immutable path at {base}: {path}")
        leaf = "/".join(parts[:_SNAPSHOT_LEAF_DEPTH])
        leaves.setdefault(leaf, set()).add(path)
        current_path = _REPO_ROOT / path
        if not current_path.is_file():
            raise ReleaseError(f"immutable file from {base} was removed: {path}")
        if current_path.read_bytes() != _git_bytes("show", f"{base}:{path}"):
            raise ReleaseError(f"immutable file from {base} changed: {path}")
    for leaf, expected_paths in leaves.items():
        leaf_path = _REPO_ROOT / leaf
        current_paths = {
            path.relative_to(_REPO_ROOT).as_posix()
            for path in leaf_path.rglob("*")
            if path.is_file()
        }
        if current_paths != expected_paths:
            raise ReleaseError(f"immutable directory from {base} changed: {leaf}")


def _check_append_only_history() -> None:
    prefix = f"{_SNAPSHOTS_PATH}/"
    leaves = set()
    for path in _git_names(
        "log", "--format=", "--name-only", "-z", "HEAD", "--", _SNAPSHOTS_PATH
    ):
        if not path.startswith(prefix):
            continue
        parts = PurePosixPath(path).parts
        if len(parts) <= _SNAPSHOT_LEAF_DEPTH:
            raise ReleaseError(f"invalid immutable path in Git history: {path}")
        leaves.add("/".join(parts[:_SNAPSHOT_LEAF_DEPTH]))
    for leaf in sorted(leaves):
        commits = _git_text("rev-list", "--reverse", "HEAD", "--", leaf).splitlines()
        if not commits:
            raise ReleaseError(f"could not find introduction commit for {leaf}")
        introduction_tree = None
        for commit in commits:
            try:
                tree = _git_text("rev-parse", f"{commit}:{leaf}")
            except ReleaseError as error:
                raise ReleaseError(
                    f"immutable directory was deleted at {commit}: {leaf}"
                ) from error
            if introduction_tree is None:
                introduction_tree = tree
            elif tree != introduction_tree:
                raise ReleaseError(
                    f"immutable directory changed after introduction at {commit}: {leaf}"
                )


def _downloads_history_paths() -> list[str]:
    # Every path under the downloads tree that Git's history from HEAD holds.
    return _git_names(
        "log", "--format=", "--name-only", "-z", "HEAD", "--", _DOWNLOADS_PATH
    )


def _check_download_tree(base: str) -> bool:
    """Check the whole downloads tree, with the append-only checks against ``base``.

    Return False in the state before the first release, when neither the tree nor any
    path under it in Git's history exists, and True once a snapshot exists.
    """
    if not _DOWNLOADS_ROOT.exists() and not _DOWNLOADS_ROOT.is_symlink():
        history = _downloads_history_paths()
        if history:
            raise ReleaseError(
                f"{_DOWNLOADS_PATH}/ does not exist, but Git's history from HEAD holds"
                f" {len(history)} path(s) under it, such as {history[0]}"
            )
        print(
            f"No Taamey D snapshot is published: {_DOWNLOADS_PATH}/ does not exist,"
            " and Git's history from HEAD holds no path under it."
        )
        return False
    if _DOWNLOADS_ROOT.is_symlink() or not _DOWNLOADS_ROOT.is_dir():
        raise ReleaseError(f"download root is not a directory: {_DOWNLOADS_ROOT}")
    if not (_DOWNLOADS_ROOT / "index.html").is_file():
        raise ReleaseError("download index is missing")
    allowed_root_entries = frozenset({"index.html", "snapshots", "latest"})
    actual_root_entries = frozenset(path.name for path in _DOWNLOADS_ROOT.iterdir())
    if actual_root_entries != allowed_root_entries:
        raise ReleaseError(
            "download root allowlist mismatch; "
            f"missing={sorted(allowed_root_entries - actual_root_entries)!r}, "
            f"extra={sorted(actual_root_entries - allowed_root_entries)!r}"
        )
    for path in _DOWNLOADS_ROOT.rglob("*"):
        if path.is_symlink():
            raise ReleaseError(f"published download tree contains a symlink: {path}")
        if path.is_file() and path.suffix.lower() not in {
            ".html",
            ".json",
            ".txt",
            ".zip",
        }:
            raise ReleaseError(
                f"published download file has a forbidden extension: {path}"
            )

    snapshots_root = _DOWNLOADS_ROOT / "snapshots"
    latest = _DOWNLOADS_ROOT / "latest"
    for directory in (snapshots_root, latest):
        if not directory.is_dir():
            raise ReleaseError(f"download tree entry is not a directory: {directory}")
    snapshot_directories = sorted(snapshots_root.iterdir())
    if any(not path.is_dir() for path in snapshot_directories):
        raise ReleaseError("snapshot root contains a non-directory entry")
    if not snapshot_directories:
        raise ReleaseError("snapshot directory set is empty")
    _require_source_commits([*snapshot_directories, latest])
    snapshot_hashes = {}
    for directory in snapshot_directories:
        manifest = _check_payload(directory)
        if manifest.get("identifier") != directory.name:
            raise ReleaseError(f"snapshot manifest identifier mismatch: {directory}")
        snapshot_hashes[directory.name] = _tree_hashes(directory)

    latest_manifest = _check_payload(latest)
    latest_identifier = latest_manifest.get("identifier")
    if latest_identifier not in snapshot_hashes:
        raise ReleaseError("latest does not name a published immutable snapshot")
    if _tree_hashes(latest) != snapshot_hashes[str(latest_identifier)]:
        raise ReleaseError("latest is not byte-identical to its immutable snapshot")
    _check_download_index(latest_manifest, sorted(snapshot_hashes))
    _check_append_only(base)
    _check_append_only_history()

    files = sorted(
        path.relative_to(_DOWNLOADS_ROOT).as_posix()
        for path in _DOWNLOADS_ROOT.rglob("*")
        if path.is_file()
    )
    print(json.dumps({"published_files": files, "file_count": len(files)}, indent=2))
    return True


def release_check() -> None:
    """Check the whole downloads tree, gh-pages/taamey-d/downloads/, or its absence.

    It takes no options: it always checks every snapshot and latest/ against the source
    commit its manifest names, the index's links, and that no committed snapshot
    changed or disappeared, in the working tree against HEAD and through Git's history.
    Before the first release it says that no snapshot is published.  It raises
    ReleaseError on any failure.
    """
    _check_download_tree(_git_text("rev-parse", "HEAD"))


def release_publish(snapshot_commit: str, published_date: str | None = None) -> None:
    """Build, verify and install the immutable snapshot of ``snapshot_commit``.

    ``snapshot_commit`` is HEAD, as 40 lowercase hex digits, and every release input in
    the working tree must equal its bytes at that commit.  ``published_date`` is
    YYYY-MM-DD, by default today's date in New York.  The existing tree is checked
    first; the snapshot is then built twice, in two scratch roots, and the builds are
    compared and checked before either is installed under snapshots/; latest/ is then
    replaced with a copy, and the index is rewritten.  It raises ReleaseError on any
    failure.  Publishing a release is an outward-facing act.
    """
    if not re.fullmatch(r"[0-9a-f]{40}", snapshot_commit):
        raise ReleaseError("snapshot commit must be 40 lowercase hex characters")
    if published_date is None:
        published_date = _new_york_date_today()
    elif not _is_iso_date(published_date):
        raise ReleaseError(f"published date is not YYYY-MM-DD: {published_date!r}")
    _require_release_notes(snapshot_commit)
    _verify_inputs_at_commit(snapshot_commit)
    _require_build_package_allowlisted(snapshot_commit)
    snapshot_identifier = _snapshot_identifier(snapshot_commit)
    _check_download_tree(snapshot_commit)
    scratch_roots = [
        _REPO_ROOT / f"release.tmp.{uuid.uuid4().hex}",
        _REPO_ROOT / f"release.tmp.{uuid.uuid4().hex}",
    ]
    snapshot_stages = [root / "snapshot" for root in scratch_roots]
    succeeded = False
    try:
        for stage in snapshot_stages:
            _build_snapshot(stage, snapshot_commit, published_date)
        first_member_maps = {
            name: _member_hashes(snapshot_stages[0] / name)
            for name in (_BINARY_ARCHIVE_NAME, _SOURCE_ARCHIVE_NAME)
        }
        second_member_maps = {
            name: _member_hashes(snapshot_stages[1] / name)
            for name in (_BINARY_ARCHIVE_NAME, _SOURCE_ARCHIVE_NAME)
        }
        if first_member_maps != second_member_maps:
            raise ReleaseError(
                "the two clean snapshot builds differ by member path or hash"
            )
        for stage in snapshot_stages:
            _check_payload(stage)

        snapshot_destination = _DOWNLOADS_ROOT / "snapshots" / snapshot_identifier
        _copy_immutable(snapshot_stages[0], snapshot_destination)
        _replace_latest(snapshot_stages[0])
        _write_download_index(snapshot_identifier)
        _check_payload(snapshot_destination)
        latest_manifest = _check_payload(_DOWNLOADS_ROOT / "latest")
        if latest_manifest.get("identifier") != snapshot_identifier:
            raise ReleaseError("latest manifest does not name the published snapshot")
        if _tree_hashes(_DOWNLOADS_ROOT / "latest") != _tree_hashes(
            snapshot_destination
        ):
            raise ReleaseError("latest payload is not byte-identical to its snapshot")
        _check_download_tree(snapshot_commit)
        succeeded = True
        print(
            json.dumps(
                {
                    "snapshot": snapshot_identifier,
                    "projection": "taamey-d-only",
                    "binary_members": len(_BINARY_PATHS),
                    "source_members": len(_SOURCE_PATHS),
                    "clean_builds_compared": 2,
                },
                indent=2,
            )
        )
    finally:
        if succeeded:
            for scratch_root in scratch_roots:
                _safe_remove_scratch(scratch_root)
        else:
            print(
                "Release build failed; retained scratch directories: "
                + ", ".join(str(path) for path in scratch_roots),
                file=sys.stderr,
            )
