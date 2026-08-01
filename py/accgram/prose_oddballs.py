from __future__ import annotations

import json
import re
from pathlib import Path

# Statuses (prose_run) whose verse carries an ERROR leaf -> the verse is ungrammatical.
_ERROR_STATUSES = {"error", "illegal_mark"}
_REF_TAIL_RE = re.compile(r"(\d+):(\d+)\s*$")


def _collect_ungrammatical_refs(output_path: Path) -> set[tuple[int, int]]:
    """The (chapter, verse) of every ungrammatical verse in one book's JSON output.

    Reads the ``wlc_422_ps_<bb>_ag.json`` record set (issue #20) and selects the
    verses flagged as ungrammatical by their ``status`` -- replacing the prior scan
    for an ERROR token in the bespoke indented-tree text.
    """
    ungrammatical_refs: set[tuple[int, int]] = set()
    if not output_path.is_file():
        return ungrammatical_refs

    with output_path.open("r", encoding="utf-8") as f_out:
        payload = json.load(f_out)

    for verse in payload.get("verses", []):
        if verse.get("status") not in _ERROR_STATUSES:
            continue
        match = _REF_TAIL_RE.search(str(verse.get("ref", "")))
        if match is not None:
            ungrammatical_refs.add((int(match.group(1)), int(match.group(2))))

    return ungrammatical_refs
