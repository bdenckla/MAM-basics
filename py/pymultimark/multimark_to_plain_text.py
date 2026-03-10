from pymultimark import multimark_char as splhc
from pymultimark import multimark_mappings as splhm
from pycmn import hebrew_letters as hl


def render_char(char, sep=""):
    return "".join(_render_char2(char, sep))


def render_char_with_placeholders(char):
    layerl, rest = _render_char2(char)
    initial = layerl + rest[:1]
    pholders = tuple(hl.YOD + x for x in rest[1:])
    return initial + "".join(pholders)


def _render_char2(char, sep=""):
    vowels = _uni_for_layerv(char)
    ula = _uni_for_layera(char)
    assert len(vowels) < 3
    post_layerl = "".join(
        (
            _uni_for_layer_s(char, "rafeh"),
            vowels[:1],
            ula[0],
            sep,
            vowels[1:],
            ula[1],
            _uni_for_layer_s(char, "ldot"),
            _uni_for_layer_s(char, "udot"),
        )
    )
    return _uni_for_layerl(char), post_layerl


def _uni_for_layerl(char):
    layer_l = splhc.layerl(char)
    return splhm.map_layerl_to_uni(layer_l)


def _uni_for_layerv(char):
    layer_l = splhc.layerl(char)
    layer_v = splhc.layerv(char)
    return splhm.map_layerv_to_uni(layer_v, layer_l) if layer_v else ""


def _uni_for_layera(char: tuple):
    layerat = splhc.layerat(char)
    uni = list(map(splhm.map_layera_to_uni, layerat))
    if len(uni) == 0:
        return ["", ""]
    if len(uni) == 1:
        return [uni[0], ""]
    assert len(layerat) == 2
    return uni


def _uni_for_layer_s(char: tuple, incl_ascii_str):
    lsas = splhc.layer_s_ascii_strs(char)
    if not lsas or incl_ascii_str not in lsas:
        return ""
    return splhm.map_layer_s_to_uni(incl_ascii_str)
