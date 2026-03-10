""" Exports strip """


def strip(word):
    """Return a copy of word with attributes stripped according to
    _WORD_KEY_TO_STRIP_DISPOSITION"""
    new_word = dict(word)
    for key, val in word.items():
        strip_dispos = _WORD_KEY_TO_STRIP_DISPOSITION[key]
        if _should_strip(strip_dispos, val):
            del new_word[key]
    return new_word


_PPM_VAL_TO_STRIP_DISPOSITION = {
    "legarmeih": False,
    "sof pasuq": False,
    "maqaf": False,
    #
    "paseq": True,
}
_KQ_VAL_TO_STRIP_DISPOSITION = {
    "trivial_qere": False,
}
_WORD_KEY_TO_STRIP_DISPOSITION = {
    "chars": False,
    "ki_rirq": False,
    "x_velo_y": False,
    "poetic_space": False,
    "shirah_space": False,
    "small_large_hung": False,
    "wd_note": False,
    "render_order": True,
    "maqaf_is_implicit": False,
    #
    "ppm": _PPM_VAL_TO_STRIP_DISPOSITION,
    #
    "ketiv_qere": _KQ_VAL_TO_STRIP_DISPOSITION,
    #
    "sampe": True,
    "wd_good_ending": True,
    # XXX TODO why do some words come up with good ending as empty list?
}


def _should_strip(strip_dispos, val):
    if isinstance(strip_dispos, bool):
        return strip_dispos
    assert isinstance(strip_dispos, dict)
    return strip_dispos[val]
