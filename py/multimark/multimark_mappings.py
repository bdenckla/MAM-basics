import functools

from pycmn import hebrew_letters as hl
from pycmn import hebrew_points as hpo
from pycmn import hebrew_punctuation as hpu
from pycmn import str_defs as sd
from pycmn import uni_heb as uh
from py_misc import uni_heb_char_classes as uhc
from pycmn.my_utils import sl_map


def map_uni_to_layerl(uni):
    return _UNI_TO_LAYERL_DICT[uni]


def map_layerl_to_uni(layerl):
    return _LAYERL_TO_UNI_DICT[layerl]


def map_uni_to_layerv(uni):
    return _UNI_TO_LAYERV_DICT[uni]


def map_uni_to_layer_s(uni):
    return _UNI_TO_LAYER_S_DICT[uni]


def _map_layerv_str_to_uni(layerl: str, layerv: str):
    return _LAYERV_TO_UNI_DICT[layerv]


@functools.singledispatch
def map_layerv_to_uni(layerv: str, layerl: str):
    return _map_layerv_str_to_uni(layerl, layerv)


@map_layerv_to_uni.register
def _(layerv: tuple, layerl: str):
    mll = functools.partial(_map_layerv_str_to_uni, layerl)
    return "".join(map(mll, layerv))


def map_uni_to_layera(uni):
    return _UNI_TO_LAYERA_DICT[uni]


def map_layera_to_uni(layera: str):
    return _LAYERA_TO_UNI_DICT[layera]


@functools.singledispatch
def map_layer_s_to_uni(layer_s: str):
    return _LAYER_S_TO_UNI_DICT[layer_s]


@map_layer_s_to_uni.register
def _(layer_s: tuple):
    return "".join(map(map_layer_s_to_uni, layer_s))


def _dagomosd(string):
    return string + hpo.DAGOMOSD


def _shd(string):
    return string + hpo.SHIND


def _sid(string):
    return string + hpo.SIND


def _tuple_reversed(tup):
    return tuple(reversed(tup))


def _uni_and_layerx_pair(uni):
    return uni, uh.join_shunnas(uni)


# lsm: letter, maybe shdsid, maybe middot
# shdsid: shin dot or sin dot
# middot: dagomosd
_LS_LIST = [*uhc.LETTERS, _shd(hl.SHIN), _sid(hl.SHIN)]
_LSM_LIST = _LS_LIST + sl_map(_dagomosd, _LS_LIST)
_UNI_AND_LAYERL_PAIRS = sl_map(_uni_and_layerx_pair, _LSM_LIST)
_UNI_AND_LAYERV_PAIRS = sl_map(_uni_and_layerx_pair, uhc.VOWEL_POINTS)
_UNI_AND_LAYERA_PAIRS = sl_map(_uni_and_layerx_pair, uhc.ACCENTS)
_UNI_AND_LAYER_S_PAIRS = (
    (hpu.UPDOT, "udot"),
    (hpu.LODOT, "ldot"),
    (hpo.RAFE, uh.join_shunnas(hpo.RAFE)),
    (hpo.VARIKA, uh.join_shunnas(hpo.VARIKA)),
    (sd.ZWJ, "ZWJ"),
)
_UNI_TO_LAYERL_DICT = dict(_UNI_AND_LAYERL_PAIRS)
_LAYERL_TO_UNI_DICT = dict(map(_tuple_reversed, _UNI_AND_LAYERL_PAIRS))
_UNI_TO_LAYERV_DICT = dict(_UNI_AND_LAYERV_PAIRS)
_LAYERV_TO_UNI_DICT = dict(map(_tuple_reversed, _UNI_AND_LAYERV_PAIRS))
_UNI_TO_LAYERA_DICT = dict(_UNI_AND_LAYERA_PAIRS)
_LAYERA_TO_UNI_DICT = dict(map(_tuple_reversed, _UNI_AND_LAYERA_PAIRS))
_UNI_TO_LAYER_S_DICT = dict(_UNI_AND_LAYER_S_PAIRS)
_LAYER_S_TO_UNI_DICT = dict(map(_tuple_reversed, _UNI_AND_LAYER_S_PAIRS))
