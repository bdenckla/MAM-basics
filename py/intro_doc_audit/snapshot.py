"""Read the audit's recorded Git snapshot without changing the working sources."""

import json
import subprocess
from functools import cache
from pathlib import PurePosixPath

from intro_doc_audit import audit


@cache
def text(path):
    """Keep quoted codepoints and source line numbers at the recorded revision."""
    relative = PurePosixPath(path)
    if (
        relative.is_absolute()
        or ".." in relative.parts
        or "\\" in path
        or not path.startswith(("in/mam-ws/", "in/mam-ws-intro/", "MAM-parsed/plus/"))
    ):
        raise ValueError("Audit snapshot reads must identify a recorded source file")
    return subprocess.check_output(
        [
            "git",
            "-c",
            f"safe.directory={audit.ROOT.as_posix()}",
            "-C",
            str(audit.ROOT),
            "show",
            f"{audit.pinned_commit()}:{path}",
        ]
    ).decode("utf-8")


@cache
def data(path):
    return json.loads(text(path))
