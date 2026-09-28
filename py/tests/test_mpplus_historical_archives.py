"""Checks of the stored releases in MAM-parsed/historical/.

Differential: ``mpplus_archive.archive_bytes``, given the members of each stored archive,
reproduces that archive byte for byte. The six pre-migration archives were written on
2026-09-10 by a program that was never tracked, so they are an oracle independent of the
builder. An archive the builder has written since, of a MAM-basics boundary, is checked the
same way, which holds the builder to the archives already in history. A missing archive or
an empty manifest fails.
"""

import io
import zipfile

from mb_diff_mpu import mpplus_archive, mpplus_revisions


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
