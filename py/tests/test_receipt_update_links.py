"""Lint tracked receipt/update families and their base-document pointers."""

import re
import subprocess
from pathlib import PurePosixPath

from mb_cmn import paths

_ORDINARY_UPDATE_RE = re.compile(r"doc/[^/]+-update\.md")
_NUMBERED_UPDATE_RE = re.compile(r"doc/[^/]+-update-[0-9]+\.md")


def _tracked_doc_paths() -> list[str]:
    repo_root = paths.repo_root()
    result = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={repo_root.as_posix()}",
            "ls-files",
            "-z",
            "--",
            "doc",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return [path for path in result.stdout.split("\0") if path]


def test_receipt_update_families_have_one_update_and_exact_pointers() -> None:
    tracked = set(_tracked_doc_paths())
    ordinary_updates = sorted(
        path for path in tracked if _ORDINARY_UPDATE_RE.fullmatch(path)
    )
    numbered_updates = sorted(
        path for path in tracked if _NUMBERED_UPDATE_RE.fullmatch(path)
    )

    assert ordinary_updates, "No tracked doc/*-update.md inputs were found."
    assert not numbered_updates, (
        "Tracked numbered update siblings are not allowed; keep one live -update.md: "
        f"{numbered_updates}"
    )

    missing_bases = []
    bad_pointers = []
    for update_path in ordinary_updates:
        base_path = update_path.removesuffix("-update.md") + ".md"
        if base_path not in tracked:
            missing_bases.append((update_path, base_path))
            continue

        update_name = PurePosixPath(update_path).name
        expected = f"Updates and later status: [{update_name}]({update_name})."
        lines = (paths.repo_root() / base_path).read_text(encoding="utf-8").splitlines()
        actual = lines[3] if len(lines) >= 4 else None
        if actual != expected:
            bad_pointers.append((base_path, actual, expected))

    assert not missing_bases, (
        "Every tracked ordinary update needs its tracked base document: "
        f"{missing_bases}"
    )
    assert not bad_pointers, (
        "Every receipt base needs its derived update pointer on physical line 4: "
        f"{bad_pointers}"
    )
