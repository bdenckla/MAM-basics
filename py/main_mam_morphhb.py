"""Write MAM-morphhb: today's MAM in the 2014 form of morphhb's MAPM/MAPM.xml.

Until 2026-11-10, openscriptures/morphhb's ``MAPM/MAPM.xml`` was David Troidl's OSIS
conversion of MAM from 2014, kept in this repository as ``MAM-OSIS/MAPM-orig/MAPM.xml``;
morphhb then merged this generator's output of ``83caf168`` in its place.  This hand-run
generator writes ``MAM-morphhb/MAPM.xml``: the same form, with today's text from
MAM-simple's BHS JSON and the structure that only ``MAM-parsed/plus/`` holds.
MAM-morphhb/README.md says where the form departs from 2014's, and why.

Run it from the repository root; it takes no arguments:

    ./.venv/Scripts/python.exe py/main_mam_morphhb.py
"""

import sys

from mam_morphhb import morphhb_runner
from mb_cmn import paths

_PATHS = {
    "mam_simple_root": paths.repo_root() / "MAM-simple",
    "mam_parsed_path": paths.mam_parsed_path(),
    "header_path": str(paths.repo_root() / "MAM-morphhb" / "header.xml"),
    "output_path": str(paths.repo_root() / "MAM-morphhb" / "MAPM.xml"),
    "xsd_path": str(paths.in_dir() / "osisCore.2.1.1-cw6.xsd"),
    "xml_xsd_path": str(paths.in_dir() / "xml.xsd"),
}


def main():
    """Write and validate MAM-morphhb/MAPM.xml."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    morphhb_runner.almost_main(_PATHS)


if __name__ == "__main__":
    main()
