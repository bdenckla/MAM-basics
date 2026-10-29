import collections
import json

from fontTools.ttLib import TTFont

from taamey_d.qa import placement_glyph_classes as mpgc
from taamey_d.qa import check_helpers as hlp


def run_placement(ctx3, tcase):
    shparams = hlp.get_shaping_parameters(tcase, ctx3["cfg"])
    tinput_str = hlp.tcase_input_str(tcase)
    output_buf = ctx3["vhb"].shape(tinput_str, shparams)
    clusters = []
    cur_cluster = None
    for gip in hlp.gips(output_buf):
        if gip.info.cluster != cur_cluster:
            clusters.append([])
            cur_cluster = gip.info.cluster
        clusters[-1].append(gip)
    names = ctx3["extra_data"]  # dict from glyph ID to glyph name
    nto = ctx3["nontest_outputs"]
    if not nto:
        nto["placements"] = collections.Counter()
        nto["ucgs"] = {}
    placements = nto["placements"]
    ucgs = nto["ucgs"]
    for cluster in clusters:
        keytup = _keytup_for_cluster(ucgs, names, cluster)
        if keytup:
            placements[keytup] += 1
    return


def _keytup_for_cluster(ucgs, names, cluster, i_fmoi=1):
    # i_fmoi: index [of] first mark of interest
    if len(cluster) == i_fmoi:
        return None
    fmoi = cluster[i_fmoi]
    fmoi_gid = fmoi.info.codepoint  # this is the glyph ID not Unicode code point
    fmoi_gnm = names[fmoi_gid]
    if fmoi_gnm == "xolam.invis":
        return _keytup_for_cluster(ucgs, names, cluster, i_fmoi + 1)
    fmoi_pos = fmoi.pos.x_offset
    glyph_classes = _classify_nonbases(ucgs, names, fmoi_gnm, cluster[i_fmoi + 1 :])
    base_gid = cluster[0].info.codepoint
    keytup = names[base_gid], fmoi_gnm, fmoi_pos, glyph_classes
    return keytup


def _classify_nonbases(ucgs, names, fmoi_gnm, nonbases):
    raw = tuple(_classify_nonbase(ucgs, names, fmoi_gnm, nb) for nb in nonbases)
    return tuple(filter(None, raw))


_INDEPENDENT_CLS_PAIRS = frozenset(
    (
        ("U", "O"),
        ("U", "eO"),
        ("U", "oO"),
        ("M", "eO"),
        #
        ("hO", "U"),
        ("hO", "M"),
        ("hO", "eU"),
        ("hO", "eO"),
    )
)


def _classify_nonbase(ucgs, names, fmoi_gnm, nonbase):  # ucg: unclassified glyphs
    nonbase_gid = nonbase.info.codepoint
    nonbase_gnm = names[nonbase_gid]
    nonbase_cls = _glyph_class(ucgs, nonbase_gnm)
    fmoi_cls = _glyph_class(ucgs, fmoi_gnm)
    cls_pair = fmoi_cls, nonbase_cls
    return None if cls_pair in _INDEPENDENT_CLS_PAIRS else nonbase_cls


def _glyph_class(ucgs, gnm):
    r = mpgc.GLYPH_CLASSES.get(gnm) or "?"
    if r == "?":
        ucgs[gnm] = True
    return r


def _dump_json_lines(fp, outlines):
    fp.write("[\n")
    for outline in outlines[:-1]:
        fp.write(outline + ",\n")
    fp.write(outlines[-1] + "\n]\n")


def _setup_plac(font_fna, _):  # _ is cfg
    # I wish I could get name, or at least ttfont, from vharfbuzz
    #
    # # A different way to get name (used by Collidoscope):
    #
    #    glyf = ttfont["glyf"]
    #    name = glyf.getGlyphName(codepoint)
    ttfont = TTFont(font_fna)
    gnms = ttfont.getGlyphOrder()  # a list of glyph names, ordered by glyph ID
    names = [mpgc.BASE_FAMILY.get(gnm) or gnm for gnm in gnms]
    return names


def _mk_dumpable(poslist, kv):
    keytup, count = kv
    base_gnm, nonbase_gnm, nonbase_pos, glyph_classes = keytup
    poslistkey = base_gnm, nonbase_gnm, glyph_classes
    posqual = (str(nonbase_pos),) if len(poslist[poslistkey]) > 1 else tuple()
    parts = (nonbase_gnm,) + glyph_classes + posqual
    nbgn_name = "-".join(parts)  # e.g. meteg-2-3 (meteg 2 of 3)
    return {"bgn": base_gnm, "nbgn": nbgn_name, "nbp": nonbase_pos, "c": count}


def report_all_to_json_for_plac(fp, ctx, nontest_outputs):  # _ is ctx
    placements = nontest_outputs["placements"]
    ucgs = nontest_outputs["ucgs"]
    poslist = _mk_poslist(placements)
    dumpables = tuple(_mk_dumpable(poslist, p) for p in placements.items())
    lines = tuple(map(json.dumps, dumpables))
    _dump_json_lines(fp, lines)
    for ucg in ucgs:
        # A glyph named "space" here is not a space character: HarfBuzz draws a
        # joiner the font left in place, a CGJ or ZWJ, with the space glyph at
        # zero width, inside the letter's cluster.
        print(f"unclassified glyph: {ucg}")


def _mk_poslist(placements):
    poslist = collections.defaultdict(list)
    for keytup, count in placements.items():
        base_gnm, nonbase_gnm, nonbase_pos, glyph_classes = keytup
        poslistkey = base_gnm, nonbase_gnm, glyph_classes
        poslist[poslistkey].append(nonbase_pos)
    return poslist


def checkobj_for_plac(font_fna):
    return hlp.CheckObj(
        "placement",
        "plac",
        run_placement,
        report_all_to_json=report_all_to_json_for_plac,
        setup=_setup_plac,
    )
