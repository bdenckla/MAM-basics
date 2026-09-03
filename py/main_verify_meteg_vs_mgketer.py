"""Check Holman's meteg suggestions against the mgketer comparison, once, by hand.

Phase 3 of ``doc/PLAN-post-stress-meteg-page-and-holman-m23.md``.  Run from the
repository root:

    .venv/Scripts/python.exe py/main_verify_meteg_vs_mgketer.py \
        --mgketer-root C:/Users/BenDe/GitRepos/MAM-private/mgketer \
        --report-path .novc/meteg-vs-mgketer.txt

THIS ENTRY POINT EXISTS SO THAT NOTHING ELSE DEPENDS ON THE CHECK.  Ben Denckla's
decision, 2026-09-03: *"run it once as a one-time check and don't wire it into the
renderer."*  Items 3 through 7 of ``doc/PLAN-holman-meteg-rollout-programme.md`` remove
the thirty mgketer diffs this check reads, so afterwards it fails for all thirty; as a
required argument of ``py/main_verify_and_render_table.py`` that failure would have
left the public Holman pages unrenderable.  ``py/main_0_mega.py`` reaches no Holman
rendering command, so there is nothing to keep out of the mega either.

``--mgketer-root`` is REQUIRED, with no skip behind it.  mgketer lives in MAM-private,
which not every machine clones, and a check that reported green on a machine without it
would have verified nothing --- the failure this repository's missing-input rule exists
to forbid.

``--report-path`` is optional and writes the same lines the run prints.  The report
holds Hebrew forms, so the file is opened as UTF-8 and stdout is reconfigured before
anything is written.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from hkq_cmn.verify_meteg_suggestions_vs_mgketer import VerificationProblem, verify


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description=(
            "Match each Holman meteg suggestion against one mgketer diff card."
        )
    )
    parser.add_argument(
        "--mgketer-root",
        type=Path,
        required=True,
        help="Checkout of MAM-private/mgketer whose out-reports/ this check reads.",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        help="Also write the report here, as UTF-8. Use a gitignored path such as .novc/.",
    )
    args = parser.parse_args()

    try:
        lines = verify(args.mgketer_root)
    except VerificationProblem as problem:
        _emit(str(problem).splitlines(), args.report_path)
        raise SystemExit(1) from problem
    _emit(lines, args.report_path)


def _emit(lines: list[str], report_path: Path | None) -> None:
    text = "\n".join(lines) + "\n"
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(text, encoding="utf-8", newline="")
        print(f"wrote {report_path.as_posix()}")
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
