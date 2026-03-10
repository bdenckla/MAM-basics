import unicodedata

from pymultimark import multimark_mappings as splhm
from pymultimark import multimark_char as splhc
from pymultimark import multimark_to_plain_text as splhtpt
from py_misc import uni_heb_char_classes as uhc
from pycmn import hebrew_points as hpo
from pycmn import hebrew_punctuation as hpu
from pycmn import str_defs as sd
from pycmn import my_utils


def convert_uw_to_splh(lis_word_as_str):
    return tuple(map(_uni_word_to_splh_word, lis_word_as_str))


def _uni_word_to_splh_word(word_as_str):
    return _uni_to_splh_w(word_as_str)


def _uni_to_splh_w(word_as_str):
    return {"chars": _uni_to_splh_chars(word_as_str)}


def _uni_to_splh_chars(string):
    return tuple(map(_cat_to_splh, _uni_to_cat(string)))


def _uni_to_cat(string):
    out = []
    for char in string:
        if char in uhc.LETTERS:
            if not out or "lett" in out[-1]:
                out.append({"seq": [], "seq_uni": ""})
        _update_cat(out[-1], char)
    return out


def _update_cat(io_cat, char):
    if char in uhc.LETTERS:
        _create(io_cat, "lett", char, splhm.map_uni_to_layerl(char))
        return
    if char in _SHSI_DOTS:
        _create(io_cat, "shsidot", char)
        return
    if char == hpo.DAGOMOSD:
        _create(io_cat, "middot", char)
        return
    if char in uhc.VOWEL_POINTS:
        _create_or_append(io_cat, "vow", char, splhm.map_uni_to_layerv(char))
        return
    if char in uhc.ACCENTS:
        _create_or_append(io_cat, "acc", char, splhm.map_uni_to_layera(char))
        return
    if char in _SPECIALS:
        _create_or_append(io_cat, "specials", char, splhm.map_uni_to_layer_s(char))
        return
    if char == sd.CGJ:
        return  # just ignore CGJ
    assert False, "unrecognized char " + unicodedata.name(char)


def _cat_to_lsm_evas(cat):  # cagetorized Unicode
    lett = cat["lett"]
    shdsid = cat.get("shsidot", "")
    middot = cat.get("middot", "")
    vows = cat.get("vow", "")
    accs = cat.get("acc", "")
    specials = cat.get("specials", "")
    smp = None  # special meteg pos
    lsm = lett + shdsid + middot
    evas = smp, vows, accs, specials
    return lsm, evas


def _cat_to_splh(cat):  # categorized Unicode
    splh_ch = _uni_to_splh_ch(*_cat_to_lsm_evas(cat))
    rendered_seq = _render_to_seq(splh_ch)
    if cat["seq"] != rendered_seq:
        layer_s = splhc.layer_s(splh_ch) or {}
        new_ls = {**layer_s, **{"seq": tuple(cat["seq"])}}
        return splhc.makebs(splh_ch, new_ls)
    return splh_ch


def _render_to_seq(splh_ch):
    inverse_cats = _uni_to_cat(splhtpt.render_char(splh_ch))
    return my_utils.first_and_only(inverse_cats)["seq"]


def _basic_create_or_append(dic, key, val):
    if key in dic:
        dic[key] += val
        return
    dic[key] = val


def _basic_create(dic, key, val):
    assert key not in dic
    dic[key] = val


def _create_or_append(dic, key, uni, seqval=True):
    _basic_create_or_append(dic, key, uni)
    _seq_append(dic, key, uni, seqval)


def _create(dic, key, uni, seqval=True):
    _basic_create(dic, key, uni)
    _seq_append(dic, key, uni, seqval)


def _seq_append(dic, key, uni, seqval):
    dic["seq"] += [(key, seqval)]
    dic["seq_uni"] += uni


def _uni_to_splh_ch(unilsm, evas):
    # lsm: let + shdsid + middot
    # evas: smp, univows, uniaccs, specials
    layer_l = splhm.map_uni_to_layerl(unilsm)
    return _make_splh_ch(layer_l, evas)


def _make_splh_ch(layerl, evas):
    smp, univows, uniaccs, specials = evas
    return splhc.make(
        layerl,
        _univows_to_layerv(univows),
        _uniaccs_to_layera(uniaccs),
        _unispecials_to_layer_s(smp, specials),
    )


def _unispecials_to_layer_s(smp, unispecials):
    tup = tuple(map(splhm.map_uni_to_layer_s, unispecials))
    strs = _simplify_empty_and_singleton(tup)
    out = {}
    if strs:
        out["ascii_strs"] = strs
    return out or None


def _univows_to_layerv(univows):
    tup = tuple(map(splhm.map_uni_to_layerv, univows))
    return _simplify_empty_and_singleton(tup)


def _uniaccs_to_layera(uniaccs):
    tup = tuple(map(splhm.map_uni_to_layera, uniaccs))
    return _simplify_empty_and_singleton(tup)


def _simplify_empty_and_singleton(tup):
    if len(tup) == 0:
        return ""
    if len(tup) == 1:
        return tup[0]
    return tup


def splhw_layerl(word_idx):
    return splhc.layerl(splhw_char_at(word_idx))


def splhw_char_at(word_idx):
    word, index = word_idx
    return word["chars"][index]


def splhw_lenw(word):
    return len(word["chars"]) if "chars" in word else 0


_SHSI_DOTS = (
    hpo.SHIND,
    hpo.SIND,
)
_SPECIALS = (
    hpu.UPDOT,
    hpu.LODOT,
    hpo.RAFE,
    hpo.VARIKA,
    sd.ZWJ,
)
