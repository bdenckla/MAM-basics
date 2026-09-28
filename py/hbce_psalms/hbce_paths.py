"""Where the HBCE Psalms comparison's inputs and outputs are.

Every path is composed from ``mb_cmn.paths``, so the program runs from any working directory
and in a linked worktree. Everything the comparison reads lies in this repository: the HBCE
snapshot under ``hbce-psalms/in/``, and MAM-basics' own MAM-simple, MAM-parsed, mirrored
introduction and UXLC data. Nothing here reaches a sibling repository or the network.
"""

from pathlib import Path

from mb_cmn import paths

import uxlc_paths

RECEIPT_NAME = "hbce-psalms-vs-mam-2026-09-26.md"


def hbce_dir() -> Path:
    """The ``hbce-psalms/`` directory: the snapshot, the outputs and the README."""
    return paths.repo_root() / "hbce-psalms"


def transcriptions_dir() -> Path:
    """HBCE's TEI transcriptions, one file per codex page, byte for byte as served."""
    return hbce_dir() / "in" / "transcriptions"


def metadata_dir() -> Path:
    """The catalogue responses for those documents, and the site's robots.txt."""
    return hbce_dir() / "in" / "metadata"


def out_dir() -> Path:
    """The generated comparison outputs."""
    return hbce_dir() / "out"


def receipt_path() -> Path:
    """The dated report on the comparison, the report of record."""
    return paths.repo_root() / "doc" / RECEIPT_NAME


def mam_simple_psalms_xml() -> Path:
    """MAM's text of Psalms: MAM-simple's XML in MAM's own versification."""
    return paths.repo_root() / "MAM-simple" / "xml-vtrad-mam" / "Ps.xml"


def mpplus_psalms_json() -> Path:
    """Psalms in MAM-parsed/plus/, where MAM's doc-notes are."""
    return paths.require_mam_parsed_plus_dir() / "D1-Psalms.json"


def mam_ws_intro_dir() -> Path:
    """The mirrored introduction to MAM, whose chapters 2 and 5 state MAM's policies."""
    return paths.in_dir() / "mam-ws-intro"


def uxlc_psalms_xml() -> Path:
    """The UXLC's Psalms."""
    return uxlc_paths.uxlc_39_dir() / "Psalms.xml"
