"""Version 1 metadata binding raw chapter arrays to Wikisource revisions.

The top-level fields are schema_version, endpoint, and books. Each books entry
is keyed by book39 ID, then Hebrew chapter ID. A chapter record contains
requested_title, resolved_title, page_id, revision_id, and sha256. The digest
covers compact UTF-8 JSON of the line array, without a serialization newline.
No string normalization or routine check timestamp belongs in this format.
"""

import hashlib
import json
from pathlib import Path
import re

from mb_cmn import file_io

SCHEMA_VERSION = 1
IDENTITY_FIELDS = ("requested_title", "resolved_title", "page_id", "revision_id")


def positive_id(value):
    """Reject booleans as well as nonpositive or noninteger IDs."""
    return type(value) is int and value > 0


def valid_lines(lines):
    """Raw chapters are arrays of unmodified strings."""
    return isinstance(lines, list) and all(isinstance(line, str) for line in lines)


def chapter_hash(lines):
    """Hash exactly the compact UTF-8 serialization of the raw line array."""
    if not valid_lines(lines):
        raise ValueError("Chapter content must be a list of strings")
    serialized = json.dumps(lines, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def empty(endpoint):
    """Create an endpoint-bound manifest without chapter claims."""
    return {"schema_version": SCHEMA_VERSION, "endpoint": endpoint, "books": {}}


def _valid_record(record):
    return (
        isinstance(record, dict)
        and set(record) == {*IDENTITY_FIELDS, "sha256"}
        and all(
            isinstance(record.get(key), str) and record[key]
            for key in ("requested_title", "resolved_title")
        )
        and all(positive_id(record.get(key)) for key in ("page_id", "revision_id"))
        and isinstance(record.get("sha256"), str)
        and re.fullmatch(r"[0-9a-f]{64}", record["sha256"]) is not None
    )


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key!r}")
        result[key] = value
    return result


def load(path, endpoint, full_titles):
    """Keep valid records; report metadata that cannot authorize reuse.

    full_titles maps every book39/chapter pair to its requested title, including
    unselected books. Invalid chapter records do not erase valid sibling records.
    """
    result = empty(endpoint)
    try:
        data = json.loads(
            Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object
        )
        if not (
            isinstance(data, dict)
            and set(data) == {"schema_version", "endpoint", "books"}
            and type(data["schema_version"]) is int
            and data["schema_version"] == SCHEMA_VERSION
            and data["endpoint"] == endpoint
            and isinstance(data["books"], dict)
        ):
            raise ValueError("unsupported schema or mismatched endpoint")
    except (OSError, UnicodeError, ValueError) as error:
        print(
            f"Wikisource metadata unavailable ({path}): {error}; fetching selected content"
        )
        return result
    for bkid, chapters in data["books"].items():
        if bkid not in full_titles or not isinstance(chapters, dict):
            print(f"Wikisource metadata invalid book {bkid!r}; ignoring its records")
            continue
        for chapter, record in chapters.items():
            if (
                chapter not in full_titles[bkid]
                or not _valid_record(record)
                or record["requested_title"] != full_titles[bkid][chapter]
            ):
                print(
                    f"Wikisource metadata invalid chapter {bkid}/{chapter}; fetching if selected"
                )
                continue
            result["books"].setdefault(bkid, {})[chapter] = record
    return result


def matches(record, identity):
    """Compare requested title, resolved title, page ID, and revision ID."""
    return all(record[key] == identity[key] for key in IDENTITY_FIELDS)


def with_hash(identity, lines):
    """Create a record only from an identity paired with the supplied content."""
    return {**identity, "sha256": chapter_hash(lines)}


def write_if_changed(data, path):
    """Atomically replace metadata only when serialized bytes differ."""
    serialized = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    target = Path(path)
    if target.exists() and target.read_bytes() == serialized:
        return
    file_io.json_dump_to_file_path(data, path)
