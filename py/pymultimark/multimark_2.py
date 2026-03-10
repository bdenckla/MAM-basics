""" Exports phase_2 """

import collections
import functools
import json

from pycmn import str_defs as sd
from pymultimark import multimark_char as splhc
from pymultimark import multimark_to_plain_text as splhtpt
from pycmn import bib_locales as tbn
from pycmn import file_io


def phase_2(in_path):
    with open(in_path, encoding="utf-8") as json_in_fp:
        raw_data = json.load(json_in_fp)
    gch2ch2ctxs, ch2ctxs, full = _get_gch2ch2ctxs(raw_data)
    gch_rows = tuple(map(_make_gch_row, gch2ch2ctxs.values()))
    ch_rows = tuple(map(_make_ch_row, ch2ctxs.items()))
    full_rows = tuple(map(_make_full_row, full))
    file_io.json_dump_to_file_path(gch_rows, "out/mam-multimarks-gch.json")
    file_io.json_dump_to_file_path(ch_rows, "out/mam-multimarks-ch.json")
    file_io.json_dump_to_file_path(full_rows, "out/mam-multimarks-full.json")


_BCV_CAT_DUALCANT = "dualcant"
_BCV_CAT_POETCANT = "poetcant"


def _bcv_categories(bcvt):
    cats = []
    if tbn.has_dualcant(bcvt):
        cats.append(_BCV_CAT_DUALCANT)
    if tbn.is_poetcant(bcvt):
        cats.append(_BCV_CAT_POETCANT)
    return cats


def _bcv(ctx):
    return tbn.mk_bcvtmam(*ctx[:3])


def _bcv_category_counts(ctxs):
    bcvs = map(_bcv, ctxs)
    cats = map(_bcv_categories, bcvs)
    flat_cats = sum(cats, [])
    return collections.Counter(flat_cats)


def _make_gch_row(ch2ctxs):
    ctxs = sum(ch2ctxs.values(), [])
    counts = {
        "bcv cat counts": _bcv_category_counts(ctxs),
        "num instances this row covers": len(ctxs),
        "num unique chs under this gch": len(ch2ctxs),
    }
    ech, ectxs = tuple(ch2ctxs.items())[0]  # use the 1st as an example
    # Below, we use ectx[0], i.e. we use the 1st as an example
    # This is an example ctx within an example ch_and_ctxs!
    # I.e. this is an example within an example!
    return _make_row(ech, ectxs[0], counts)


def _make_ch_row(ch2ctxs_item):
    char, ctxs = tuple(ch2ctxs_item)
    counts = {
        "bcv cat counts": _bcv_category_counts(ctxs),
        "num instances this row covers": len(ctxs),
    }
    # Below, we use ctx[0], i.e. we use the 1st as an example
    return _make_row(char, ctxs[0], counts)


def _make_full_row(ch_and_single_ctx):
    char, ctx = ch_and_single_ctx
    counts = {
        "bcv cat counts": _bcv_category_counts([ctx]),
    }
    return _make_row(char, ctx, counts)


def _make_row(char, ctx, counts):
    example_nxtch = ctx[3]
    example_prech = ctx[4]
    rnxt = _render_char(example_nxtch)
    rpre = _render_char(example_prech)
    mmc = splhc.mmcat(char)
    mmc_needing_cgj_help = splhc.MMCAT_VUV_LAE, splhc.MMCAT_VUV_LAI, splhc.MMCAT_XUM
    sep = sd.CGJ if mmc in mmc_needing_cgj_help else None
    bcv_cat_counts = counts["bcv cat counts"]
    row = {
        "mmcat": mmc,
        "Vow": _collapse(splhc.layerv(char)),
        "Acc": _collapse(splhc.layera(char)),
        "Spe": splhc.layer_s_raw(char),
        "r": rpre + splhtpt.render_char(char) + rnxt,
        "rs": rpre + splhtpt.render_char(char, sep) + rnxt if sep else None,
        "sa": splhtpt.render_char_with_placeholders(char),
        "bkna": ctx[0],  # book [name]
        "chnu": ctx[1],  # chapter
        "vrnu": ctx[2],  # verse
        "ndualcant": bcv_cat_counts.get(_BCV_CAT_DUALCANT, 0),
        "npoetcant": bcv_cat_counts.get(_BCV_CAT_POETCANT, 0),
    }
    ninst = counts.get("num instances this row covers")
    nuc = counts.get("num unique chs under this gch")
    if ninst:
        row["ni"] = ninst
    if nuc:
        row["nuc"] = nuc
    return row


def _collapse(layerx):
    if layerx is None or isinstance(layerx, str):
        return layerx
    assert isinstance(layerx, tuple)
    return "".join(layerx)


def _render_char(char):
    return "" if char is None else splhtpt.render_char(char)


def _pdd(factory):
    return functools.partial(collections.defaultdict, factory)


def _get_gch2ch2ctxs(raw_data):
    # gch: generic char, i.e. character modulo layer L (letter)
    gch2ch2ctxs = collections.defaultdict(_pdd(list))
    ch2ctxs = collections.defaultdict(list)
    full = []
    for raw_datum in raw_data:
        cwm, short_bcv = _obj_to_tuple(raw_datum)
        bkid, chnu, vrnu = tbn.parse_short_bcv(short_bcv)
        for char, next_char, prev_char in cwm:
            ctx = bkid, chnu, vrnu, next_char, prev_char
            gch = splhc.makebl(char, "σ")
            gch2ch2ctxs[gch][char].append(ctx)
            ch2ctxs[char].append(ctx)
            full.append((char, ctx))
    return gch2ch2ctxs, ch2ctxs, full


def _obj_to_tuple(obj):
    if isinstance(obj, list):
        return tuple(map(_obj_to_tuple, obj))
    if isinstance(obj, dict):
        return tuple((k, v) for k, v in obj.items())
    return obj
