"""Run exactly one focused FOI command and compare its whole output family."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


def snapshot(root):
    return {
        p.relative_to(root).as_posix(): sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def main():
    root = Path.cwd()
    kind = sys.argv[1]
    arguments = {
        "selected": ["--foi", "args-foi-dexi-stress-meteg"],
        "full": [],
        "other": ["--foi", "args-foi-doc-note-notation"],
    }[kind]
    directory = root / "gh-pages/MAM-with-doc/foi"
    before = snapshot(directory)
    command = [
        sys.executable,
        "py/main_foi_features_of_interest.py",
        "--single-threaded",
        *arguments,
    ]
    subprocess.run(command, check=True)
    after = snapshot(directory)
    result = {
        "kind": kind,
        "command": command,
        "files_before": len(before),
        "files_after": len(after),
        "all_file_bytes_identical": before == after,
        "differences": sorted(
            k for k in before.keys() | after.keys() if before.get(k) != after.get(k)
        ),
        "sha256_before": before,
        "sha256_after": after,
    }
    (root / f".novc/hourly/foi-{kind}-comparison.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    assert before == after, result["differences"]
    print(
        json.dumps(
            {k: v for k, v in result.items() if not k.startswith("sha256_")}, indent=2
        )
    )


if __name__ == "__main__":
    main()
