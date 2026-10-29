from typing import NamedTuple, Any


class CheckObj(NamedTuple):
    name: str
    shortname: str
    run: Any
    report: Any = None
    report_all_to_html: Any = None
    report_all_to_json: Any = None
    setup: Any = None
    report_summary_to_html: Any = None


class GlyphInfoAndPos(NamedTuple):
    info: Any
    pos: Any


def gips(output_buf):
    ginfos = list(reversed(output_buf.glyph_infos))
    gposs = list(reversed(output_buf.glyph_positions))
    return [GlyphInfoAndPos(inf, pos) for inf, pos in zip(ginfos, gposs)]


def tcase_input_str(tcase):
    return word_chars(tcase["input"])


def word_chars(word):
    if isinstance(word, str):
        return word
    # The only non-str words are SLH (small/large/hung) words,
    # which look like this: ('מֵרְשָׁעִ֣ים', '...ע..', 'ת', 'ע/ת')
    assert len(word) == 4, f"Unexpected word format: {word}"
    return word[0]


def xform_word_chars(word, fun):
    if isinstance(word, str):
        return fun(word)
    # An SLH word (see word_chars): transform its characters, keep the rest.
    return (fun(word_chars(word)),) + tuple(word[1:])


SHPARAM_KEYS = ["script", "language", "direction", "features"]


def _get_fr_tcase(tcase, cfg, key, default=None):
    if key in tcase:
        return tcase[key]
    if cfg_defaults := cfg.get("defaults"):
        if key in cfg_defaults:
            return cfg_defaults[key]
    return default


def get_shaping_parameters(tcase, cfg):
    return {k: _get_fr_tcase(tcase, cfg, k) for k in SHPARAM_KEYS}
