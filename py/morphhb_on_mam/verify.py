"""Check that a directory holds morphhb's wlc/ files at db6c5c9b, blob for blob.

Written by Claude (Opus 5.5) on 2026-11-16, when the morphhb-on-MAM study was put on ice
(morphhb-on-mam/README.md), in place of the study's verify_morphhb.py, which read GitHub API
responses and the 2026-11-13 study's copies from fixed places.

morphhb-on-mam/in/fetched/morphhb-wlctree-1.json is the GitHub API's listing of the wlc/ tree
of openscriptures/morphhb at db6c5c9b, as the study fetched it on 2026-11-15
(morphhb-on-mam/in/fetch_log.jsonl). Each of its 40 entries, the 39 books and VerseMap.xml,
gives a file's Git blob SHA-1. problems() first checks that those 40 entries make the
listing's own tree, 0ee59fa2, then computes the blob SHA-1 of each file in the given directory
and compares it with the listing's; a listed file that the directory lacks, or a file that
the listing lacks, is a problem too. It reads nothing else and touches no network.
"""

import hashlib
import json
from pathlib import Path

from morphhb_on_mam import record_paths

# The mode of a regular file in a Git tree, the only kind of entry the listing has.
FILE_MODE = "100644"


def blob_sha(data: bytes) -> str:
    """Git's SHA-1 of a blob holding ``data``."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def tree_sha(entries: dict[str, str]) -> str:
    """Git's SHA-1 of a tree of regular files, from {file name: blob SHA-1}."""
    body = b"".join(
        FILE_MODE.encode("ascii")
        + b" "
        + name.encode("utf-8")
        + b"\0"
        + bytes.fromhex(sha)
        for name, sha in sorted(entries.items(), key=lambda kv: kv[0].encode("utf-8"))
    )
    return hashlib.sha1(b"tree %d\0" % len(body) + body).hexdigest()


def _listed_blobs() -> tuple[str, dict[str, str]]:
    """The listing's tree SHA-1 and {file name: blob SHA-1}; raises on anything unexpected."""
    path = record_paths.tree_listing_path()
    listing = json.loads(path.read_text(encoding="utf-8"))
    if listing["truncated"]:
        raise ValueError(f"{record_paths.shown(path)} is a truncated listing")
    blobs = {}
    for entry in listing["tree"]:
        if entry["type"] != "blob" or entry["mode"] != FILE_MODE:
            raise ValueError(f"{record_paths.shown(path)}: unexpected entry {entry!r}")
        if entry["path"] in blobs or "/" in entry["path"]:
            raise ValueError(
                f"{record_paths.shown(path)}: unexpected path {entry['path']!r}"
            )
        blobs[entry["path"]] = entry["sha"]
    if tree_sha(blobs) != listing["sha"]:
        raise ValueError(
            f"{record_paths.shown(path)}: its entries do not make its tree"
        )
    return listing["sha"], blobs


def problems(wlc_dir) -> tuple[int, list[str]]:
    """How many files match the listing, and a line for every problem found.

    The listing's own entries must make its tree, 0ee59fa2 (``_listed_blobs``), so 40
    matching files are that tree, the wlc/ of db6c5c9b and of d4265dfa.
    """
    wlc_dir = Path(wlc_dir)
    _tree, blobs = _listed_blobs()
    if not wlc_dir.is_dir():
        return 0, [f"{wlc_dir.as_posix()} is not a directory"]
    found = []
    present = {path.name for path in wlc_dir.iterdir()}
    for name in sorted(present - set(blobs)):
        found.append(f"{name}: in the directory but not in the listing")
    local = {}
    for name, sha in sorted(blobs.items()):
        path = wlc_dir / name
        if not path.is_file():
            found.append(f"{name}: missing")
            continue
        local[name] = blob_sha(path.read_bytes())
        if local[name] != sha:
            found.append(f"{name}: blob {local[name]}, but the listing has {sha}")
    n_ok = sum(1 for name, sha in local.items() if sha == blobs[name])
    return n_ok, found
