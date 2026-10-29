"""Taamey D's shaping checks, which py/main_taamey_d.py qa runs.

This package was restructured on 2026-10-29 from hbofonts' main_run_shaping_checks.py
and the my_*.py modules it uses.  Its font is always the tracked
Taamey-D/font-m-TaD/Taamey_D.ttf, its test cases are the corpus in Taamey-D/qa-in/, and
it rewrites the tracked reports in Taamey-D/qa-out/Taamey_D/.  hbofonts' font argument
and its --qa-prefix option are gone; that option's one tracked use, the minitest/ corpus,
stays in hbofonts.
"""

import os

from mb_cmn import paths
from taamey_d.qa import anchor_families
from taamey_d.qa import shaping_checks
from taamey_d.qa import check_mrun as mrun
from taamey_d.qa import check_plac as plac
from taamey_d.qa import check_regr as regr
from taamey_d.qa import check_coll as coll

_TAAMEY_D_DIR = paths.repo_root() / "Taamey-D"


def prefix_progcb(progcb, prefix):
    return lambda s: progcb(f"{prefix}: {s}")


def _shown(text):
    """Show the paths in a printed line relative to the repository root.

    The checks read and write through absolute paths built from paths.repo_root(), so
    they work from any directory, and they name each test-case file in their progress
    lines and results.  hbofonts ran them from its root with relative paths, so it
    printed qa-in/...; this prints Taamey-D/qa-in/... rather than a machine's path.
    """
    return text.replace(f"{paths.repo_root()}{os.sep}", "")


def _print_progress(text):
    print(_shown(text))


def _get_checkobjs(font_fna, one_check):
    all_checkobjs = (
        mrun.checkobj_for_mrun(font_fna),
        plac.checkobj_for_plac(font_fna),
        regr.checkobj_for_regr(font_fna),
        coll.checkobj_for_coll(font_fna),
    )
    if one_check:
        dic = {c.shortname: c for c in all_checkobjs}
        return [dic[one_check]]
    return all_checkobjs


def _run_anchor_family_lint(font_fna):
    """Print the anchor-family lint's result, and return True if it failed.

    hbofonts checked several fonts and skipped this lint for those with no exception
    table.  The one font here has a table, so a missing one means the lint would check
    nothing, and that raises rather than passing.
    """
    outcome = anchor_families.lint(font_fna)
    if outcome is None:
        raise RuntimeError(
            f"anchor families: no exception table for {font_fna.name} in"
            " anchor_families.py, so the lint would check nothing"
        )
    findings, summary = outcome
    for finding in findings:
        print(f"anchor families: {finding}")
    print(("FAIL" if findings else "PASS", f"anchor families: {summary}"))
    return bool(findings)


def run_checks(one_check=None):
    """Run the anchor-family lint and the shaping checks, and print every result.

    one_check, the short name mrun, plac, regr or coll, runs that shaping check alone;
    None runs all four.  Each check rewrites its reports.  A SKIP, an unknown status or
    an anchor-family FAIL raises; a shaping check's FAIL tuple does not, since its
    report is a tracked file.  Return the directory of the reports, qa-out/<font
    stem>/, which the mega's taamey-d-qa step compares with Git's index.
    """
    font_fna = _TAAMEY_D_DIR / "font-m-TaD" / "Taamey_D.ttf"
    qadirs = dict(indir=_TAAMEY_D_DIR / "qa-in", outdir=_TAAMEY_D_DIR / "qa-out")
    progcb = _print_progress
    anchor_families_failed = _run_anchor_family_lint(font_fna)
    checkobjs = _get_checkobjs(font_fna, one_check)
    skipped = False
    for checkobj in checkobjs:
        progcb_sn = prefix_progcb(progcb, checkobj.shortname)
        results = shaping_checks.run_a_check_across_all_tcases(
            font_fna, progcb_sn, checkobj, qadirs
        )
        for res in results:
            print(tuple(_shown(x) if isinstance(x, str) else x for x in res))
            status = res[0]
            if status == "SKIP":
                skipped = True
            elif status not in {"PASS", "FAIL"}:
                raise RuntimeError(f"unknown shaping-check status: {status}")
    # FAIL reports are tracked artifacts; the taamey-d-qa step of py/main_0_mega.py
    # requires them to match the checked-in baseline. A SKIP has no equivalent
    # artifact and is fatal, and so is a FAIL from the anchor-family lint, which
    # writes no report.
    failures = []
    if anchor_families_failed:
        failures.append("the anchor-family lint failed")
    if skipped:
        failures.append("one or more shaping checks skipped")
    if failures:
        raise SystemExit("; ".join(failures))
    # Where shaping_checks and fails_filename put every report.
    return qadirs["outdir"] / font_fna.stem
