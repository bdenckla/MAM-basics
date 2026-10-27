"""Run one actual FOI generation and compare its entire committed output family."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


def snapshot(root):
    return {
        path.relative_to(root).as_posix(): {
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "mtime_ns": path.stat().st_mtime_ns,
            "size": path.stat().st_size,
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def main():
    root = Path.cwd()
    kind = sys.argv[1]
    arguments = {"selected": ["--foi", "args-foi-dexi-stress-meteg"], "full": []}[kind]
    directory = root / "gh-pages/MAM-with-doc/foi"
    before = snapshot(directory)
    command = [
        sys.executable,
        "py/main_foi_features_of_interest.py",
        "--single-threaded",
        *arguments,
    ]
    result = subprocess.run(command)
    after = snapshot(directory)
    changed_bytes = sorted(
        name
        for name in before.keys() | after.keys()
        if before.get(name, {}).get("sha256") != after.get(name, {}).get("sha256")
    )
    rewritten = sorted(
        name
        for name in before.keys() & after.keys()
        if before[name]["mtime_ns"] != after[name]["mtime_ns"]
    )
    allowed = {
        "foi-dexi-stress-meteg.html",
        "foi-dexi-stress-meteg.json",
        "provenance.md",
    }
    unexpected_rewrites = sorted(set(rewritten) - allowed) if kind == "selected" else []
    record = {
        "kind": kind,
        "command": command,
        "generator_exit_code": result.returncode,
        "files_before": len(before),
        "files_after": len(after),
        "all_file_bytes_identical": not changed_bytes,
        "byte_differences": changed_bytes,
        "rewritten_by_mtime": rewritten,
        "unexpected_selected_rewrites": unexpected_rewrites,
        "before": before,
        "after": after,
    }
    (root / f".novc/hourly/foi-{kind}-comparison.json").write_text(
        json.dumps(record, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in record.items()
                if key not in {"before", "after"}
            },
            indent=2,
        )
    )
    assert result.returncode == 0
    assert not changed_bytes, changed_bytes
    assert not unexpected_rewrites, unexpected_rewrites


if __name__ == "__main__":
    main()
