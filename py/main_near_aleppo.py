"""Build or check the local near-Aleppo dataset, census and example edition.

All inputs and outputs live in this checkout. No private repository, comparison
tree, scan archive, or adoption handoff is a runtime dependency.

Run without flags to regenerate the census, the dataset with its population file,
and the HTML, in that order. Use --check to compare all products without writing,
or select one step with --census, --build or --html. --refresh-note-review
refreshes the note-review ledger, and --check-note-review verifies every
changed-note presentation against a fresh enumeration of MAM's notes.
"""

import argparse
import importlib
import subprocess
import sys

from near_aleppo import build_paths
from near_aleppo import main_build
from near_aleppo import main_html_pages

_INSTRUMENTS = (
    "template_inventory",
    "qamats_params",
    "divine_name_split",
    "adonai_census",
    "stress_helper_census",
)


def _census(check):
    """Gather all five results before writing or comparing any of them."""
    outputs = {}
    for name in _INSTRUMENTS:
        result = subprocess.run(
            [sys.executable, __file__, "--instrument", name],
            capture_output=True,
            check=True,
        )
        # Census output is a text baseline with repository-standard LF endings.
        outputs[name + ".txt"] = result.stdout.replace(b"\r\n", b"\n")
    directory = build_paths.input_dir() / "census"
    if check:
        differences = [
            name
            for name, data in outputs.items()
            if (directory / name).read_bytes() != data
        ]
        if differences:
            raise AssertionError(f"Near-Aleppo census differs: {differences}")
        print("All five local MAM census baselines agree")
        return
    for name, data in outputs.items():
        (directory / name).write_bytes(data)
    print("Regenerated five local MAM census baselines")


def almost_main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--census", action="store_true")
    selection.add_argument("--build", action="store_true")
    selection.add_argument("--html", action="store_true")
    selection.add_argument("--instrument", choices=_INSTRUMENTS, help=argparse.SUPPRESS)
    selection.add_argument("--check-note-review", action="store_true")
    selection.add_argument("--refresh-note-review", action="store_true")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare against tracked output; write nothing.",
    )
    args = parser.parse_args(argv)
    if args.instrument:
        importlib.import_module("near_aleppo.census." + args.instrument).main()
        return 0
    if args.check_note_review or args.refresh_note_review:
        flag = (
            "--check-note-review" if args.check_note_review else "--refresh-note-review"
        )
        return main_html_pages.main([flag]) or 0
    selected = args.census or args.build or args.html
    check_args = ["--check"] if args.check else []
    if args.census or not selected:
        _census(args.check)
    if args.build or not selected:
        code = main_build.main(check_args)
        if code:
            return code
    if args.html or not selected:
        return main_html_pages.main(check_args) or 0
    return 0


if __name__ == "__main__":
    sys.exit(almost_main())
