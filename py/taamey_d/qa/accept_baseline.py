"""Taamey D's baseline acceptance, which py/main_taamey_d.py accept-baseline runs.

This module was restructured on 2026-10-29 from hbofonts'
main_bible_words_update_expecteds.py, in the role of hbofonts' ps1_update_expecteds.ps1,
which ran it for Taamey_D.ttf.  It accepts the actual outputs in the shaping checks'
regression reports, under Taamey-D/qa-out/Taamey_D/, as Taamey D's expected outputs in
the test cases of Taamey-D/qa-in/.  It is an explicit baseline operation, not a test:
run it only once Ben has approved the new baseline (Taamey-D/README.md).  hbofonts' font
argument and its --qa-prefix option are gone; that option's one tracked use, the
minitest/ corpus, stays in hbofonts.
"""

import json

from mb_cmn import file_io
from mb_cmn import paths
from taamey_d.qa import fails_filename

_TAAMEY_D_DIR = paths.repo_root() / "Taamey-D"
# Directory-free, as hbofonts' ps1_update_expecteds.ps1 passed it: check_regr looks
# up an expected output by the font's file name, and fails_filename names a report by
# its stem.
_FONT_BASENAME = "Taamey_D.ttf"

# Actuals (regression failures) look like this:
#    {
#       "input": "א֑וֹר",
#       "expected": "[something]",
#       "actual": "resh=4+883|vavxolam=2+484|atnax=0@591,0+0|alef=0+1048"
#    },
# We're using the actual of the (false) failure to update the expected in the
# test cases file.


def _mk_tcase(font_basename, actuals, tcase):
    if actual := actuals.get(_hashable_input(tcase)):
        old_expected = tcase.get("expected", {})
        new_expected = {**old_expected, **{font_basename: actual}}
        return dict(tcase, expected=new_expected)
    return tcase  # no need to update this test cases with a new expected


def _dump(fc, fp):
    json.dump(fc, fp, indent=0, ensure_ascii=False)
    fp.write("\n")


def _make_hashable2(foo):
    if isinstance(foo, list):
        return tuple(map(_make_hashable2, foo))
    return foo


def _hashable_input(foo):
    return _make_hashable2(foo["input"])


def _do_one_tcases_fn(font_basename, tcases_fna, qaoutdir):
    # Printed relative to the repository root, Taamey-D/qa-in/..., rather than as
    # one machine's absolute path.
    print(tcases_fna.relative_to(paths.repo_root()).as_posix())
    with open(tcases_fna, encoding="utf-8") as infp:
        old_fc = json.load(infp)  # old_fc: old (original) file contents
    actuals_fna = fails_filename.fails_filename(
        qaoutdir, font_basename, "regression", tcases_fna
    )
    with open(actuals_fna, encoding="utf-8") as infp:
        actuals_fc = json.load(infp)  # actuals_fc: actuals file contents
    actuals = {_hashable_input(f): f["actual"] for f in actuals_fc}
    new_tcases = [_mk_tcase(font_basename, actuals, t) for t in old_fc["testcases"]]
    new_fc = dict(old_fc, testcases=new_tcases)  # new_fc: new file contents
    file_io.with_tmp_openw(tcases_fna, {"newline": ""}, lambda fp: _dump(new_fc, fp))


def accept_baseline():
    """Accept the regression reports' actual outputs as Taamey D's expected outputs.

    An explicit baseline operation that needs Ben's approval, not a test.  For each test
    case file in Taamey-D/qa-in/, read the regression report that the shaping checks
    wrote for it under Taamey-D/qa-out/Taamey_D/, record each failing test case's actual
    output as its expected output for Taamey_D.ttf, and rewrite the file.
    """
    qaindir = _TAAMEY_D_DIR / "qa-in"
    qaoutdir = _TAAMEY_D_DIR / "qa-out"
    tcases_fnas = list(qaindir.glob("*.testcases.json"))
    for tcases_fna in tcases_fnas:
        _do_one_tcases_fn(_FONT_BASENAME, tcases_fna, qaoutdir)
