"""Checks of the stored releases in MAM-parsed/historical/.

Differential: ``mpplus_archive.archive_bytes``, given the members of each stored archive,
reproduces that archive byte for byte. The six pre-migration archives were written on
2026-09-10 by a program that was never tracked, so they are an oracle independent of the
builder. An archive the builder has written since, of a MAM-basics boundary, is checked the
same way, which holds the builder to the archives already in history.

Lint: every boundary of releases.json names a stored release, no stored release is left
that no boundary names, and every member of every stored release hashes, as a Git blob, to
the ``sha`` its manifest row lists. That is what lets the named releases be compared with no
Git history at all, and this check reads none, so it runs in a shallow clone too. Ben's
decisions of 2026-09-28 archive each boundary when it is pinned;
``py/subcommands/diff_mpplus.py`` refuses a boundary that is not stored.

A missing archive, an empty manifest or an empty releases.json fails.
"""

import hashlib
import io
import json
from pathlib import Path
import zipfile

from mb_diff_mpu import mpplus_archive, mpplus_revisions
from subcommands import diff_mpplus


def test_archive_writer_reproduces_every_stored_archive():
    revisions = mpplus_revisions.load_manifest()["revisions"]
    assert revisions, "MAM-parsed/historical/manifest.json lists no stored release"
    for commit in revisions:
        stored = mpplus_revisions.archive_path(commit).read_bytes()
        with zipfile.ZipFile(io.BytesIO(stored)) as archive:
            members = {info.filename: archive.read(info) for info in archive.infolist()}
        assert members, f"the archive of {commit} has no members"
        rebuilt = mpplus_archive.archive_bytes(members)
        assert rebuilt == stored, f"the builder does not reproduce {commit}.zip"


def test_every_boundary_is_stored_and_every_member_hashes_as_listed():
    releases = json.loads(Path(diff_mpplus.RELEASES_JSON).read_text(encoding="utf-8"))[
        "releases"
    ]
    assert releases, "releases.json names no release"
    manifest = mpplus_revisions.load_manifest()
    boundaries = {entry[side] for entry in releases for side in ("old", "new")}
    named = set()
    for boundary in sorted(boundaries):
        commit = mpplus_revisions.stored_commit(boundary, manifest)
        assert commit is not None, (
            f"releases.json boundary {boundary} is not a stored release; archive it with"
            f" py/main_diff.py mpplus --archive {boundary}"
        )
        named.add(commit)
    unnamed = sorted(set(manifest["revisions"]) - named)
    assert not unnamed, f"stored releases that no boundary names: {unnamed}"
    for commit, entry in manifest["revisions"].items():
        rows = entry["files"]
        assert rows, f"the manifest lists no member of {commit}"
        with zipfile.ZipFile(mpplus_revisions.archive_path(commit)) as archive:
            assert sorted(archive.namelist()) == sorted(row["path"] for row in rows)
            for row in rows:
                data = archive.read(row["path"])
                blob_id = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
                assert (blob_id, len(data)) == (
                    row["sha"],
                    row["size"],
                ), f"{commit}.zip!{row['path']} is not the blob its manifest row lists"
