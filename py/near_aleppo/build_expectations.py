"""Bind near-Aleppo build populations to current local MAM census results.

The two source inputs must be clean and equal to their HEAD object identities.
The census provenance must name those identities. Only counts independently
reported by the five MAM census instruments may refresh automatically. The build
must reproduce the candidate before any snapshot or dataset is written.

Code-only changes remain guarded by the existing snapshot. Sensitive site lists,
reading dispositions, and the two added-target counts remain pinned for review.
"""

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from near_aleppo import build_paths
from near_aleppo import phase3_policies as phase3
from near_aleppo import phase5_readings as phase5
from near_aleppo import phase6_mam_targets as phase6

_NEAR_ALEPPO = build_paths.input_dir()
EXPECTATIONS_PATH = _NEAR_ALEPPO / "build-populations.json"
_CENSUS_EXPECTED = _NEAR_ALEPPO / "census"
_CENSUS_PROVENANCE = _CENSUS_EXPECTED / "provenance.md"

_SCHEMA_VERSION = 4
_CENSUS_INPUTS = (
    "MAM-parsed/plus",
    "aleppo/index-flat-annotated.json",
)

# The census projects MAM's text before the ketiv/qere apparatus policy. That
# policy supplies forms with qamats at Isaiah 44:17, Ezekiel 24:2 and Psalms 89:29,
# where MAM's qere has qamats qatan. These three no longer reach the qamats-size
# policy. Keep this reviewed difference pinned; a changed difference must fail
# the build rather than be accepted by an automatic input refresh.
_KQ_QAMATS_QATAN_REMOVALS = 3

# These phase-2 counters are the settled column of template_inventory.py. The
# remaining counters in the snapshot describe selected-versus-unselected or
# policy-sensitive subpopulations that the census does not independently print;
# those counters stay pinned across an automatic refresh.
_CENSUS_PHASE2_LABELS = (
    "מ:קמץ",
    "מ:דחי",
    "מ:צינור",
    "מ:לגרמיה-2",
    "מ:פסק",
    "מ:מקף אפור",
    "נוסח",
    "מ:הערה-2",
    "מ:כפול",
    "מ:קו״כ-אם-2",
    "כו״ק",
    "קו״כ",
    "מ:כו״ק מיוחד",
    "כתיב ולא קרי",
    "קרי ולא כתיב",
)


def _git(repo, *args):
    result = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={repo.as_posix()}",
            "--no-optional-locks",
            "-C",
            str(repo),
            *args,
        ],
        capture_output=True,
        check=True,
        encoding="utf-8",
    )
    return result.stdout


def _provenance_prefix(rel):
    return f"MAM-basics {rel}: "


def current_census_input_ids(mam_parsed_plus_dir, *, check_provenance=True):
    """Return current content ids after proving the census sidecar is current.

    Both paths resolve within this checkout. Source inputs must be clean before
    their HEAD identities can identify the bytes being read. Only the census
    regenerator may omit the old sidecar check while preparing a new receipt.
    """
    mam_basics = build_paths.mam_basics_dir()
    input_dir = mam_parsed_plus_dir.resolve()
    if not input_dir.is_relative_to(mam_basics.resolve()):
        raise RuntimeError(
            f"The build reads {input_dir}, which is outside the MAM-basics checkout "
            f"{mam_basics}. The census input object ids come from that checkout's HEAD "
            "and would not identify the bytes being read. Point "
            "REPO_MAM_PARSED_DIR at that checkout's MAM-parsed tree, set "
            "REPO_MAM_BASICS_DIR to its owning checkout, or unset the parsed override."
        )
    dirty = _git(mam_basics, "status", "--porcelain", "-z", "--", *_CENSUS_INPUTS)
    if dirty.strip():
        raise RuntimeError(
            "The near-Aleppo build inputs have uncommitted changes, so their HEAD "
            "object ids do not identify the bytes the build would read:\n"
            + dirty.rstrip()
        )

    current_output = _git(
        mam_basics,
        "rev-parse",
        *(f"HEAD:{rel}" for rel in _CENSUS_INPUTS),
    )
    current = dict(zip(_CENSUS_INPUTS, current_output.split(), strict=True))

    if not check_provenance:
        return current

    text = _CENSUS_PROVENANCE.read_text(encoding="utf-8")
    recorded = {}
    for rel in _CENSUS_INPUTS:
        prefix = _provenance_prefix(rel)
        values = [
            line.removeprefix(prefix)
            for line in text.splitlines()
            if line.startswith(prefix)
        ]
        if len(values) != 1:
            raise RuntimeError(
                f"Expected one {prefix!r} line in {_CENSUS_PROVENANCE}, "
                f"found {len(values)}"
            )
        recorded[rel] = values[0]

    stale = [rel for rel in _CENSUS_INPUTS if recorded[rel] != current[rel]]
    if stale:
        detail = "; ".join(
            f"{rel}: census {recorded[rel]}, current {current[rel]}" for rel in stale
        )
        raise RuntimeError(
            "The near-Aleppo census is not tied to the current MAM-basics inputs "
            f"({detail}). Regenerate the census successfully before the build."
        )
    return current


def load():
    """Load and minimally validate the tracked build-population snapshot."""
    value = json.loads(EXPECTATIONS_PATH.read_text(encoding="utf-8"))
    required = {
        "schema_version",
        "census_input_ids",
        "phase2_counts",
        "phase3_counts",
        "phase3_sites",
        "phase5_counts",
        "phase5_sites",
        "phase6_counts",
        "flag_counts",
        "flag_sites",
    }
    if set(value) != required:
        raise RuntimeError(
            f"Unexpected keys in {EXPECTATIONS_PATH}: {sorted(value)}; "
            f"expected {sorted(required)}"
        )
    if value["schema_version"] != _SCHEMA_VERSION:
        raise RuntimeError(
            f"Unsupported schema_version in {EXPECTATIONS_PATH}: "
            f"{value['schema_version']}"
        )
    if set(value["census_input_ids"]) != set(_CENSUS_INPUTS):
        raise RuntimeError(
            f"Unexpected census_input_ids in {EXPECTATIONS_PATH}: "
            f"{sorted(value['census_input_ids'])}"
        )
    if not all(
        value[key]
        for key in (
            "phase2_counts",
            "phase3_counts",
            "phase5_counts",
            "phase6_counts",
            "flag_counts",
            "flag_sites",
            "phase3_sites",
            "phase5_sites",
        )
    ):
        raise RuntimeError(f"Empty population map in {EXPECTATIONS_PATH}")
    return value


def is_current(snapshot, current_ids):
    return snapshot["census_input_ids"] == current_ids


def _single_int(path, pattern):
    text = path.read_text(encoding="utf-8")
    values = re.findall(pattern, text, flags=re.MULTILINE)
    if len(values) != 1:
        raise RuntimeError(
            f"Expected one match for {pattern!r} in {path}, found {len(values)}"
        )
    return int(values[0])


def _template_inventory():
    path = _CENSUS_EXPECTED / "template_inventory.txt"
    rows = {}
    pattern = re.compile(r"^(.+?)\s{2,}(\d+)\s+(\d+)\s{2,}", re.MULTILINE)
    for name, raw, settled in pattern.findall(path.read_text(encoding="utf-8")):
        rows[name.rstrip()] = {"raw": int(raw), "settled": int(settled)}
    missing = [name for name in _CENSUS_PHASE2_LABELS if name not in rows]
    if missing:
        raise RuntimeError(
            f"{path} lacks build populations: {', '.join(repr(x) for x in missing)}"
        )
    return rows


def _refresh_stress_helper_counts(phase3_counts):
    """Bind census-backed stress-helper populations to the current source data."""
    path = _CENSUS_EXPECTED / "stress_helper_census.txt"

    def total(name):
        return _single_int(
            path,
            rf"^{re.escape(name)} atoms with a stress helper(?:, .*)?: .* total (\d+)$",
        )

    def kept(accent):
        return sum(
            phase3_counts[phase3._stress_helper_label(accent, what)]
            for what in (phase3._KEPT_BY_CODEX, phase3._KEPT_BY_LENINGRAD)
        )

    pashta_total = total("pashta")
    pashta_stripped = _single_int(
        path,
        r"^  of those, with the stress helper on the second-to-last letter: "
        r".* total (\d+)$",
    )
    phase3_counts[phase3._stress_helper_label(phase3.PASHTA, phase3._STRIPPED)] = (
        pashta_stripped
    )
    phase3_counts[phase3._stress_helper_label(phase3.PASHTA, phase3._BETWEEN)] = (
        pashta_total - pashta_stripped - kept(phase3.PASHTA)
    )

    for accent, name in (
        (phase3.SEGOLTA, "segolta"),
        (phase3.TELISHA_GEDOLA, "telisha gedolah"),
        (phase3.TELISHA_QETANA, "telisha qetanah"),
        (phase3.UNICODE_ZINOR, "zarqa"),
    ):
        phase3_counts[phase3._stress_helper_label(accent, phase3._STRIPPED)] = total(
            name
        ) - kept(accent)


def refreshed(snapshot, current_ids):
    """Return a candidate snapshot supported by the current census goldens."""
    candidate = json.loads(json.dumps(snapshot, ensure_ascii=False))
    candidate["census_input_ids"] = current_ids

    inventory = _template_inventory()
    for label in _CENSUS_PHASE2_LABELS:
        candidate["phase2_counts"][label] = inventory[label]["settled"]

    phase3_counts = candidate["phase3_counts"]
    phase3_counts[phase3._QAMATS_QATAN] = (
        _single_int(
            _CENSUS_EXPECTED / "qamats_params.txt",
            r"^U\+05C7 in the whole base text taking ד: (\d+)$",
        )
        - _KQ_QAMATS_QATAN_REMOVALS
    )

    divine_path = _CENSUS_EXPECTED / "divine_name_split.txt"
    adonai_total = _single_int(divine_path, r"^\s*Adonai \(qamats on vav\)\s+(\d+)$")
    phase3_counts[phase3._ELOHIM_SHEVA] = _single_int(
        divine_path, r"^\s*Elohim \(hiriq on vav\)\s+hataf segol\s+(\d+)$"
    )
    phase3_counts[phase3._ELOHIM_BARE_YOD] = _single_int(
        divine_path, r"^\s*Elohim \(hiriq on vav\)\s+none/other\s+(\d+)$"
    )
    adonai_kept = phase3_counts[phase3._ADONAI_HOLAM_KEPT]
    phase3_counts[phase3._ADONAI_HOLAM_STRIPPED] = adonai_total - adonai_kept

    adonai_path = _CENSUS_EXPECTED / "adonai_census.txt"
    title_total = _single_int(
        adonai_path, r"^\s*divine title \(qamats on nun\)\s+(\d+)$"
    )
    candidate_total = _single_int(adonai_path, r"^\s*TOTAL (\d+)$")
    title_kept = phase3_counts[phase3._TITLE_HOLAM_KEPT]
    phase3_counts[phase3._TITLE_HOLAM_STRIPPED] = title_total - title_kept
    phase3_counts[phase3._NOT_TITLE] = candidate_total - title_total
    _refresh_stress_helper_counts(phase3_counts)
    candidate["phase5_counts"][phase5._NOTES] = candidate["phase2_counts"]["נוסח"]
    for name in ("נוסח", "מ:הערה-2"):
        candidate["phase6_counts"][name + phase6._REACHED] = candidate["phase2_counts"][
            name
        ]
    return candidate


def phase3_sites(snapshot):
    """Convert JSON arrays to the tuple shape recorded by the build."""
    return {
        label: [tuple(ref) for ref in refs]
        for label, refs in snapshot["phase3_sites"].items()
    }


def phase5_sites(snapshot):
    """Convert JSON arrays to the tuple shape the build records, like phase3_sites."""
    return {
        label: [tuple(ref) for ref in refs]
        for label, refs in snapshot["phase5_sites"].items()
    }


def flag_sites(snapshot):
    """Convert compact JSON verse names to the tuple shape the flags step records."""
    return {
        label: [tuple(ref.split("|")) for ref in refs]
        for label, refs in snapshot["flag_sites"].items()
    }


def _section_bounds(text, key, next_key):
    start_marker = f"  {json.dumps(key)}: "
    start = text.find(start_marker)
    if start < 0:
        raise AssertionError(f"Serialized snapshot lacks its {key} object")
    if next_key is None:
        if not text.endswith("}\n"):
            raise AssertionError("Serialized snapshot lacks its final object boundary")
        end = len(text) - 2
    else:
        end_marker = f"  {json.dumps(next_key)}: "
        end = text.find(end_marker, start + len(start_marker))
        if end < 0:
            raise AssertionError(
                f"Serialized snapshot lacks {key}'s successor {next_key}"
            )
    return start, end


def write(snapshot):
    """Atomically write a fully validated replacement snapshot."""
    repo = build_paths.mam_basics_dir()
    tracked_text = _git(repo, "show", "HEAD:in/near-aleppo/build-populations.json")
    tracked = json.loads(tracked_text)
    text = json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n"
    for key, next_key in (
        ("phase3_sites", "phase5_counts"),
        ("phase5_sites", "phase6_counts"),
        ("flag_sites", None),
    ):
        if snapshot[key] != tracked[key]:
            raise AssertionError(
                f"An input refresh may not rewrite policy-sensitive {key}"
            )
        tracked_start, tracked_end = _section_bounds(tracked_text, key, next_key)
        start, end = _section_bounds(text, key, next_key)
        text = text[:start] + tracked_text[tracked_start:tracked_end] + text[end:]
    if json.loads(text) != snapshot:
        raise AssertionError("Snapshot serialization changed its JSON value")
    EXPECTATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        prefix=EXPECTATIONS_PATH.name + ".",
        suffix=".tmp",
        dir=EXPECTATIONS_PATH.parent,
        delete=False,
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            handle.write(text)
        os.replace(temp_path, EXPECTATIONS_PATH)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    print(f"Build-population expectations written: {EXPECTATIONS_PATH}")
