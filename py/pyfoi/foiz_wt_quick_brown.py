import re
from dataclasses import dataclass
from py_misc import wt_qere
from py_misc import uni_heb_char_classes as uhc
from pycmn import uni_heb as uh
from pycmn import hebrew_accents as ha
from pycmn import hebrew_letters as hl


@dataclass
class _Counts:
    stress_helpers: dict
    lett: dict
    flett: dict
    vowp: dict

    def __init__(self):
        self.stress_helpers = {}
        self.lett = {}
        self.flett = {}
        self.vowp = {}


def find_fois_wt(mroge):
    verse = wt_qere.get_verse_as_wordstrs(_HANDLERS, mroge)
    return _find_features(verse)


_HANDLERS = {
    **wt_qere.HANDLERS,
    "מ:דחי": wt_qere.hnd_recurse_on_arg_0,
    "מ:צינור": wt_qere.hnd_recurse_on_arg_0,
    "מ:קמץ": wt_qere.hnd_recurse_on_param_dalet,
    "מ:כפול": wt_qere.hnd_recurse_on_param_vals_and_ca,
    #
    "מ:פסק": wt_qere.hnd_return_plain_space,
}


def _find_features(wordstrs):
    counts = _Counts()
    for wordstr in wordstrs:
        _count_stress_helpers(counts.stress_helpers, wordstr)
        for char in wordstr:
            _count(uhc.LETTERS, counts.lett, char)
            _count(_FINAL_LETTERS, counts.flett, char)
            _count(uhc.VOWEL_POINTS, counts.vowp, char)
    foi_path = None
    if len(counts.stress_helpers) > 2:
        foi_path = _get_foi_path("many-stress-helpers", counts, len(wordstrs))
    if len(counts.lett) == 27:
        foi_path = _get_foi_path("many-lett", counts, len(wordstrs))
    if len(counts.flett) == 5:
        foi_path = _get_foi_path("many-flett", counts, len(wordstrs))
    if len(counts.vowp) >= 12:
        foi_path = _get_foi_path("many-vowp", counts, len(wordstrs))
    if foi_path:
        return [(foi_path, " ".join(wordstrs))]
    return []


def _get_foi_path(feature_name, counts: _Counts, len_words):
    llsh = str(len(counts.stress_helpers)) + "-stress-helpers"
    llcs = str(len(counts.lett)) + "-lett"
    llfl = str(len(counts.flett)) + "-flett"
    lvcs = str(len(counts.vowp)) + "-vowp"
    missing_vowps = _missing(uhc.VOWEL_POINTS, counts.vowp)
    mvowps = tuple(map(uh.shunna, missing_vowps))
    rest = {
        "many-lett": (llcs, lvcs, *mvowps),
        "many-flett": (llfl,),
        "many-stress-helpers": (llsh,),
        "many-vowp": (lvcs, *mvowps, llcs),
    }
    foi_path = "quick-brown-fox", feature_name, *rest[feature_name]
    return foi_path


def _count(uhc_class, count_dic, char):
    if char not in uhc_class:
        return
    if char not in count_dic:
        count_dic[char] = 0
    count_dic[char] += 1


_FINAL_LETTERS = (
    hl.FKAF,
    hl.FMEM,
    hl.FNUN,
    hl.FPE,
    hl.FTSADI,
)
STRESS_HELPER_PATTERNS = (
    ha.PASH + r"\S+" + ha.PASH,
    ha.TEL_G + r"\S+" + ha.TEL_G,
    ha.TEL_Q + r"\S+" + ha.TEL_Q,
    ha.SEG_A + r"\S+" + ha.SEG_A,
    ha.ZSH_OR_TSIT + r"\S+" + ha.Z_OR_TSOR,  # non-self-help!
)


def _count_stress_helpers(count_dic, word_chars):
    count = 0
    for sh_patt in STRESS_HELPER_PATTERNS:
        if re.search(sh_patt, word_chars):
            short_name = uh.shunna(sh_patt[0])
            if short_name not in count_dic:
                count_dic[short_name] = 0
            count_dic[short_name] += 1
    return count


def _missing(uhc_class, count_dic):
    uhc_class_set = frozenset(uhc_class)
    count_dic_keys_set = frozenset(count_dic.keys())
    return sorted(uhc_class_set - count_dic_keys_set)
