"""Lint the annotation inventory against every distributed MAM-simple verse.

The inventory includes all retained Scripture alternatives and notes. This check
ensures its explicit shape dispatch accepts the generated corpus without silently
skipping an unknown structure. Missing tracked inputs and an empty scan fail.
"""

import subprocess

from mb_cmn import mam_simple_json, paths
from mb_cmn.git_process import git_command
from mb_misc.letter_small_job import _small_letters


def test_all_distributed_verses_pass_the_annotation_inventory():
    root = paths.repo_root()
    tracked = subprocess.run(
        git_command(root, "ls-files", "-z", "--", "MAM-simple/json-vtrad-*/*.json"),
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    files = [root / name for name in tracked.stdout.split("\0") if name]
    assert files, "No tracked MAM-simple JSON payloads"
    count = 0
    for path in files:
        for verse in mam_simple_json.verses(mam_simple_json.read_book_group(path)):
            list(_small_letters(verse))
            count += 1
    assert count, "No distributed MAM-simple verses were checked"
