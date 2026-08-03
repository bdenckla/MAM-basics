"""Exports check"""

import mb_cmn.file_io as my_open


def check(changeset_date, raw_changes, path):
    """
    Sanity-check raw changes (before date_qualify_and_reformat).
    Write any problems to path and assert if any were found.
    """
    problems = []
    for change in raw_changes:
        _check_one(problems, changeset_date, change)
    my_open.json_dump_to_file_path(problems, path)
    assert not problems, f"Sanity check failed. See {path}"


def _check_one(problems, changeset_date, change):
    lc = change.get("lc")
    if lc is not None and lc.get("line") is None:
        problems.append(
            {
                "changeset": changeset_date,
                "n": change["n"],
                "check": "lc_line_is_none",
            }
        )
