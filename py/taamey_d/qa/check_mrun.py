from fontTools.ttLib import TTFont

from typing import NamedTuple, Any
import re
from taamey_d.qa import check_helpers as hlp


class FriendlyGip(NamedTuple):
    codepointname: str
    cluster: int
    pos: Any


def _tcase_input_slh(tcase):
    tinput = tcase["input"]
    if isinstance(tinput, str):
        return None
    # The only non-str words are SLH (small/large/hung) words,
    # which look like this: ('מֵרְשָׁעִ֣ים', '...ע..', 'ת', 'ע/ת')
    assert len(tinput) == 4, f"Unexpected tinput format: {tinput}"
    return tinput


def mrun_split(slh_quad):
    slh_full, slh_spine, slh_types, slh_summary = slh_quad
    clpat = r"([א-ת־][^א-ת־]*)"
    # These raise rather than assert, because the corpus updater also calls this
    # function, to reject an SLH word that the multirun check could not split.
    if not re.fullmatch(f"{clpat}+", slh_full):
        raise ValueError(f"not a sequence of letter clusters: {slh_full}")
    clusters = re.findall(clpat, slh_full)
    if len(clusters) != len(slh_spine):
        raise ValueError(
            f"{len(clusters)} != {len(slh_spine)}, {clusters}, {slh_spine}"
        )
    prev_bone = None
    runs = []
    for cluster, bone in zip(clusters, slh_spine):
        if bone != "." or prev_bone != ".":
            runs.append("")
        runs[-1] += cluster
        prev_bone = bone
    return runs


def _mrun_equal(prgip, ovgip, cluster_offset):  # per-run gip vs. overall gip
    assert prgip.info.cluster == ovgip.info.cluster - cluster_offset
    return (
        prgip.info.codepoint == ovgip.info.codepoint
        and prgip.pos.position == ovgip.pos.position
    )


def run_multirun(ctx3, tcase):
    tinput_slh = _tcase_input_slh(tcase)
    if tinput_slh is None:
        return
    names = ctx3["extra_data"]  # dict from glyph ID to glyph name
    failed_tcases = ctx3["failed_tcases"]
    tinput_str = hlp.tcase_input_str(tcase)
    runs = mrun_split(tinput_slh)
    shparams = hlp.get_shaping_parameters(tcase, ctx3["cfg"])
    overall_output_buf = ctx3["vhb"].shape(tinput_str, shparams)
    per_run_output_bufs = []
    for run in runs:
        per_run_output_bufs.append(ctx3["vhb"].shape(run, shparams))
    overall_gips = hlp.gips(overall_output_buf)
    overall_index = 0
    for run, prob in zip(runs, per_run_output_bufs):
        cluster_offset = overall_gips[overall_index].info.cluster
        for gip in hlp.gips(prob):
            ovgip = overall_gips[overall_index]
            if not _mrun_equal(gip, ovgip, cluster_offset):
                ovfgip = _gip_for_the_record(names, ovgip)
                fgip = _gip_for_the_record(names, gip)
                failed_tcases.append((tinput_str, ovfgip, run, fgip))
            overall_index += 1
    return


def _gip_for_the_record(names, gip):
    return FriendlyGip(names[gip.info.codepoint], gip.info.cluster, gip.pos.position)


def _setup_mrun(font_fna, _):  # _ is cfg
    # I wish I could get name, or at least ttfont, from vharfbuzz
    #
    # # A different way to get name (used by Collidoscope):
    #
    #    glyf = ttfont["glyf"]
    #    name = glyf.getGlyphName(codepoint)
    ttfont = TTFont(font_fna)
    return ttfont.getGlyphOrder()  # a list of glyph names, ordered by glyph ID


def report_mrun_fail(failed_tcase):
    return failed_tcase


def checkobj_for_mrun(font_fna):
    return hlp.CheckObj(
        "multirun", "mrun", run_multirun, report_mrun_fail, setup=_setup_mrun
    )
