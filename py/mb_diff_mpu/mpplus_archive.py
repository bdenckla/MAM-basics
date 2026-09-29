"""Store a pinned MAM-basics boundary of the change log as a release archive.

Exports:
    archive_bytes     — the deterministic ZIP holding a set of plus/ members
    git_blob_id       — the Git object id of a blob's bytes
    head_commit       — the full hash of MAM-basics HEAD
    uncommitted_plus_paths — Git's status records for MAM-parsed/plus/
    plus_blob_ids     — the MAM-parsed/plus/*.json blob ids at a MAM-basics commit
    plus_blobs        — those blobs with their bytes
    archive_boundary  — archive the MAM-basics commit a releases.json boundary names

A stored release is an uncompressed ZIP of plus JSON in MAM-parsed/historical/, listed in that
directory's manifest.json. ``mpplus_revisions.resolve`` reads one with no Git history at all. The
six boundaries of the pre-migration releases, which are MAM-parsed commits, were stored that way
on 2026-09-10 by a program that was never tracked. A boundary pinned since is a MAM-basics
commit, and ``resolve`` reads an unstored one from Git, which a shallow clone loses: on
2026-09-28 a depth-50 clone of main at 8c2fa6c3 held 117 commits and not cb95915, the boundary
pinned on 2026-09-17, so the mega's diff-mpplus step stopped there. Ben's decisions of
2026-09-28: archive each MAM-basics boundary when it is pinned, labelled like the six older ones
by its full hash and New York date, and make that stick with a guard and a one-step pin command,
both in ``py/subcommands/diff_mpplus.py``.

The archive written here is the untracked program's, byte for byte: given the members of each of
its six archives, ``archive_bytes`` reproduces that archive, which
py/tests/test_mpplus_historical_archives.py checks. Members are named plus/<name>, relative to
the MAM-parsed product root as the older members are, so ``resolve`` reads both alike.
"""

from datetime import datetime
import hashlib
import io
import json
import subprocess
import zipfile

from mb_cmn import paths
from mb_cmn.git_process import git_command
from mb_cmn.new_york_time import new_york_date
from mb_diff_mpu import mpplus_revisions

MAM_BASICS_REPOSITORY = "https://github.com/bdenckla/MAM-basics"
_PLUS_DIRECTORY = "MAM-parsed/plus/"
# ZIP 2.0, the version Python writes by default; set explicitly so a change of default
# cannot change an archive.
_ZIP_VERSION = 20


def archive_bytes(members):
    """Return the deterministic ZIP of ``members``, a mapping of member name to bytes.

    Members are stored uncompressed in sorted order. Every ZipInfo field that
    ``mpplus_revisions`` validates is set explicitly rather than left to Python's
    defaults, which differ by platform: ``create_system`` defaults to 0 on Windows. A
    name outside ASCII is written in UTF-8 with the flag that says so, as zipfile does
    by itself; one member of b5e8f94's archive, plus/FA-Ezra-Neḥemiah.json, has one.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, date_time=mpplus_revisions.ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = mpplus_revisions.ZIP_CREATE_SYSTEM
            info.create_version = _ZIP_VERSION
            info.extract_version = _ZIP_VERSION
            info.external_attr = mpplus_revisions.ZIP_EXTERNAL_ATTR
            info.internal_attr = 0
            info.extra = b""
            info.comment = b""
            archive.writestr(info, members[name])
    return buffer.getvalue()


def git_blob_id(data):
    """Return the Git object id of a blob holding ``data``."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _git_bytes(repo, *args):
    result = subprocess.run(git_command(repo, *args), capture_output=True)
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Git failed in {repo}: {message}")
    return result.stdout


def _git_text(repo, *args):
    return _git_bytes(repo, *args).decode("utf-8").strip()


def head_commit():
    """The full hash of MAM-basics HEAD."""
    return _git_text(paths.repo_root(), "rev-parse", "--verify", "HEAD^{commit}")


def uncommitted_plus_paths():
    """Git's status records for MAM-parsed/plus/, which are empty when HEAD holds it all."""
    status = _git_bytes(
        paths.repo_root(), "status", "--porcelain", "-z", "--", _PLUS_DIRECTORY
    )
    return [record.decode("utf-8") for record in status.split(b"\0") if record]


def plus_blob_ids(commit):
    """Return {member name: blob id} for each MAM-parsed/plus/*.json at ``commit``.

    ``commit`` is a MAM-basics commit. Member names are plus/<name>. Only names ending in
    .json are kept, as the Git reader in ``mpplus_revisions`` keeps them, so a file such
    as plus/provenance.md, which cb95915 has, is left out.
    """
    listing = _git_bytes(
        paths.repo_root(), "ls-tree", "-r", "-z", commit, "--", _PLUS_DIRECTORY
    )
    blob_ids = {}
    for record in listing.split(b"\0"):
        if not record:
            continue
        meta, path_bytes = record.split(b"\t", 1)
        _mode, kind, blob_id = meta.decode("ascii").split(" ")
        path = path_bytes.decode("utf-8")
        if not path.endswith(".json"):
            continue
        if kind != "blob":
            raise RuntimeError(f"{path} at {commit} is a {kind}, not a file")
        blob_ids["plus/" + path.removeprefix(_PLUS_DIRECTORY)] = blob_id
    if not blob_ids:
        raise RuntimeError(f"No MAM-parsed/plus JSON files at {commit}")
    return blob_ids


def plus_blobs(commit):
    """Return ``(member name, blob id, bytes)`` for each of ``plus_blob_ids(commit)``.

    The rows are in sorted order. Each blob's bytes are read verbatim and checked
    against the id Git lists for it.
    """
    repo = paths.repo_root()
    blobs = []
    for name, blob_id in sorted(plus_blob_ids(commit).items()):
        data = _git_bytes(repo, "cat-file", "blob", blob_id)
        if git_blob_id(data) != blob_id:
            raise RuntimeError(f"Git returned the wrong bytes for {name} at {commit}")
        blobs.append((name, blob_id, data))
    return blobs


def _commit_date(commit):
    """The New York date of ``commit``'s committer time, as the older entries give it."""
    committed = datetime.fromisoformat(
        _git_text(paths.repo_root(), "show", "-s", "--format=%cI", commit)
    )
    return new_york_date(committed).isoformat()


def _write_manifest(manifest):
    """Write the manifest as it has always been written, so an append is the only diff."""
    with open(mpplus_revisions.manifest_path(), "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(manifest, indent=2) + "\n")


def archive_boundary(boundary, commit=None):
    """Archive the MAM-basics commit that ``boundary`` names; return its full hash.

    ``boundary`` is spelled as in releases.json, a 7-character short hash for every
    boundary pinned so far. ``commit``, when given, is its full hash, which spares Git
    resolving a short hash it might find ambiguous among its own commits; the pin command
    passes HEAD's. This writes MAM-parsed/historical/<full hash>.zip and appends
    that commit's entry to the manifest, after the others. The entry has the
    ``repository`` the commit is in, since the manifest-wide ``source_repository`` names
    MAM-parsed; the commit's ``date``; and ``files``, a row of ``path``, ``sha`` and
    ``size`` for each member, in sorted path order as in every other entry.

    Nothing is written when ``boundary`` already names a stored release, whether its own
    or another whose hash it begins; when this clone lacks the commit; or when
    ``boundary`` is not a hexadecimal prefix of its commit, since ``resolve`` finds a
    stored release only by one.
    """
    manifest = mpplus_revisions.load_manifest()
    stored = mpplus_revisions.stored_commit(boundary, manifest)
    if stored is not None:
        raise ValueError(f"{boundary!r} already names the stored release {stored}")
    repo = paths.repo_root()
    try:
        commit = _git_text(
            repo, "rev-parse", "--verify", f"{commit or boundary}^{{commit}}"
        )
    except RuntimeError as exc:
        raise ValueError(
            f"MAM-basics commit {boundary!r} is not in this clone. A shallow clone can"
            " lack it: fetch it once by its full hash with"
            " git fetch --depth=1 origin <full hash>, or archive it in a clone that has it."
        ) from exc
    if len(boundary) < 7 or not commit.startswith(boundary.lower()):
        raise ValueError(
            f"{boundary!r} is not a hexadecimal prefix of its commit {commit}, so it could"
            " never name a stored release"
        )
    blobs = plus_blobs(commit)
    entry = {
        "repository": MAM_BASICS_REPOSITORY,
        "date": _commit_date(commit),
        "files": [
            {"path": name, "sha": blob_id, "size": len(data)}
            for name, blob_id, data in blobs
        ],
    }
    archive = mpplus_revisions.archive_path(commit)
    archive.write_bytes(archive_bytes({name: data for name, _, data in blobs}))
    manifest["revisions"][commit] = entry
    _write_manifest(manifest)
    return commit
