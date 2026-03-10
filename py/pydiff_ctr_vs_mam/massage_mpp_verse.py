import re
from pycmn import hebrew_accents as ha
from pycmn import hebrew_points as hpo
from pycmn import hebrew_punctuation as hpu
from pycmn import ws_tmpl2 as wtp
from pycmn.my_utils import sum_of_map
from pycmn.shrink import shrink
from pycmn import template_names as tmpln
    

_SPLITS_TUP = " ", hpu.MAQ, hpu.PASOLEG
_SPLITS_STR = "".join(_SPLITS_TUP)
_SPLIT_PATT = f"([{_SPLITS_STR}]+)"


def massage_mpp_verse(mpp_verse_raw):
    wtseq = _massage_mpp_wtseq(mpp_verse_raw.EP)
    assert isinstance(wtseq, list)
    assert len(wtseq) == 1
    assert isinstance(wtseq[0], str)
    out = wtseq[0]
    out = out.translate(MISC_TRANS)
    words = re.split(_SPLIT_PATT, out)
    return words


MISC_TRANS = str.maketrans(
    {
        hpo.VARIKA: None,
        hpo.QAMATS_Q: hpo.QAMATS,
        ha.ATN_H: ha.YBY,
    }
)


def _massage_mpp_wtseq(mpp_wtseq):
    return shrink(sum_of_map(_massage_mpp_ep_wtel, mpp_wtseq))


def _massage_mpp_ep_wtel(wtel):
    if isinstance(wtel, str):
        return [wtel]
    assert wtp.is_template(wtel)
    handler = _HANDLERS[wtp.template_name(wtel)]
    return handler(wtel)


def _massage_arg_1(wtel):
    return _massage_mpp_wtseq(wtp.template_element(wtel, 1))


_HANDLERS = {
    "נוסח": _massage_arg_1,
    "מ:דחי": _massage_arg_1,
    "מ:צינור": _massage_arg_1,
    tmpln.SLH_WORD: _massage_arg_1,
    "מ:אות-ג": _massage_arg_1,
    "מ:מקף אפור": lambda _wtel: " ",
    "מ:לגרמיה-2": lambda _wtel: hpu.PASOLEG,
    "ר0": lambda _wtel: " ",
    "ר1": lambda _wtel: " ",
    "ר2": lambda _wtel: " ",
    "ר3": lambda _wtel: " ",
    "ר4": lambda _wtel: " ",
}
