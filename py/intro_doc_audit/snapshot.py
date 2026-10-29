"""Read the audit's recorded Git snapshot without changing the working sources."""

import json
import re
import subprocess
from functools import cache
from pathlib import PurePosixPath

from intro_doc_audit import audit


@cache
def text(path):
    """Keep quoted codepoints and source line numbers at the recorded revision."""
    return text_at(audit.pinned_commit(), path)


@cache
def text_at(commit, path):
    """Read a recorded source file at the pinned commit or at a later recorded one,
    such as the mirror refresh that holds an applied proposal."""
    relative = PurePosixPath(path)
    if (
        relative.is_absolute()
        or ".." in relative.parts
        or "\\" in path
        or not (
            path.startswith(("in/mam-ws/", "in/mam-ws-intro/", "MAM-parsed/plus/"))
            or path == "in/mam-ws-revisions.json"
        )
    ):
        raise ValueError("Audit snapshot reads must identify a recorded source file")
    if not re.fullmatch("[0-9a-f]{40}", commit):
        raise ValueError("Audit snapshot reads must name a full commit id")
    return subprocess.check_output(
        [
            "git",
            "-c",
            f"safe.directory={audit.ROOT.as_posix()}",
            "-C",
            str(audit.ROOT),
            "show",
            f"{commit}:{path}",
        ]
    ).decode("utf-8")


@cache
def data(path):
    return json.loads(text(path))
