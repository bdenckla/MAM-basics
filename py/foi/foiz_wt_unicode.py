import re
import unicodedata
from mb_cmn import uni_denorm as ud
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import hebrew_letters as hl
from mb_cmn import uni_heb as uh
from mb_cmn import template_names as tmpln
from foi import foi_wikitext_helpers as fwh
from foi import regexp_helpers as rh
from mb_cmn.my_utils import sl_map
from mb_cmn.my_utils import first_and_only


def find_fois_wt(mroge):
    """Find interesting uses of Unicode."""
    return fwh.find_fois_in_minirow_ep(_FOILERS, mroge)


def _find_fois_in_string(stack, string):
    # A documentation note attaches punctuation to the forms it gives, as in a list
    # of sigla, an equals sign and a pointed form.  The forms that fwh.forms finds
    # leave that punctuation out.
    fois = []
    for form in fwh.forms(string):
        fois.extend(_find_fois_in_str(form))
    qual_fois = sl_map((_qualify, stack), fois)
    return qual_fois


def _qualify(stack, unqual_foi):
    unqual_path = unqual_foi[0]
    unqual_targ = unqual_foi[1]
    qualifiers = "doc-part-n", "scrdfftar-note"
    for qualifier in qualifiers:
        if qualifier in stack:
            qual_path = *unqual_path, qualifier
            return qual_path, unqual_targ
    return unqual_path, unqual_targ


_FOILERS = fwh.all_branch_foilers(
    {
        str: _find_fois_in_string,
        tmpln.SLH_WORD: fwh.find_fois_in_slh_word_arg_1,
        "נוסח": fwh.label_args_of_doc,
        tmpln.SCRDFF_TAR: fwh.label_args_of_scrdfftar,
        tmpln.SCRDFF_NO_TAR: fwh.fail_on_unexpected_template_in_plus,
    }
)

###########################################################
###########################################################
###########################################################
###########################################################

_LU = hpu.LODOT + hpu.UPDOT
_DR = hpo.DAGOMOSD + hpo.RAFE
_SPECIALS = (
    _LU,
    _DR,
    _LU[0],
    _LU[1],
    _DR[1],
    ha.G1_TG,
    ha.G2_TG,
)
# Unlike the specials above, which are substrings, alef with mapiq is found through
# the letter that carries the dot, since DAGESH OR MAPIQ alone is no rarity.  It
# joins a word's specials after them, so that _SP_SUMMARY's keys cover it too and a
# combination of it with another special raises.
_ALEF_WITH_MAPIQ = "alef with mapiq"
_SP_SUMMARY = {
    (_LU, _LU[0], _LU[1]): ("rare", "udot-with-ldot"),
    (_DR, _DR[1]): ("rare", "rafeh-with-dagesh"),
    # lower dot doesn't ever appear on its own
    (_LU[1],): ("rare", "udot"),
    (_DR[1],): ("rare", "rafeh"),
    (ha.G1_TG,): ("rare", "geresh-telisha-gedolah"),
    (ha.G2_TG,): ("rare", "gershayim-telisha-gedolah"),
    (_ALEF_WITH_MAPIQ,): ("rare", "alef-with-mapiq"),
    tuple(): None,
}


def _specials_in_str(string):
    specials = tuple(filter(None, (_special_in_str(string, s) for s in _SPECIALS)))
    if _has_alef_with_mapiq(string):
        return *specials, _ALEF_WITH_MAPIQ
    return specials


def _special_in_str(string, special):
    return special if special in string else None


def _has_alef_with_mapiq(string):
    """Whether DAGESH OR MAPIQ is among the nonspacing marks after an alef."""
    letter = None
    for char in string:
        if "א" <= char <= "ת":
            letter = char
        elif char == hpo.DAGOMOSD and letter == hl.ALEF:
            return True
        elif unicodedata.category(char) != "Mn":
            letter = None
    return False


def _letters_with_rafeh(string):
    letters = []
    last_letter = None
    for char in string:
        if "א" <= char <= "ת":
            last_letter = char
            continue
        if char == hpo.RAFE:
            assert last_letter is not None, string
            letters.append(last_letter)
    return tuple(letters)


def _rafeh_fp(word_chars):
    letters = _letters_with_rafeh(word_chars)
    assert letters, word_chars
    letter_set = set(letters)
    if letter_set == {hl.ALEF}:
        return "unicode", "rare", "rafeh", "alef"
    if letter_set == {hl.HE}:
        return "unicode", "rare", "rafeh", "he"
    return "unicode", "rare", "rafeh", "misc"


_QQ_NL_PATTERN = hpo.QAMATS_Q + rh.NLETT  # qq, non-letter
_X_ON_NG_PATTERN = rh.NGUTT + rh.ZM_NL + rh.XATEF
_X_ON_NG_TYPE = {
    (hpo.XPATAX,): "patax",
    (hpo.XPATAX, hpo.XPATAX): "patax×2",
    (hpo.XSEGOL,): "segol",
    (hpo.XQAMATS,): "qamats",
}
_YHVH_IN = rh.par("יֱ.?הֹוִ.?ה")


def _qq_acc_fp(word_chars):  # fp: feature (foi) path
    if match_strings := re.findall(_QQ_NL_PATTERN, word_chars):
        acc_name = uh.shunna(first_and_only(match_strings)[1])
        return "unicode", "qq", acc_name
    return None


def _xatef_on_ng_fp(word_chars):  # fp: feature (foi) path
    yhvh_remap = re.sub(_YHVH_IN, "", word_chars)
    if match_strings := re.findall(_X_ON_NG_PATTERN, yhvh_remap):
        lasts = tuple(m[-1] for m in match_strings)
        x_on_ng_type = _X_ON_NG_TYPE[lasts]
        return "unicode", "xatef-on-non-gutt", x_on_ng_type
    return None


def _my_append(features, foi_path, string):
    features.append((foi_path, string))


def _find_fois_in_str(string):
    features = []
    if not ud.has_std_mark_order(string):
        ns_order_fp = "unicode", "NON_STANDARD_MARK_ORDER"
        _my_append(features, ns_order_fp, string)
    if sp_summary := _SP_SUMMARY[_specials_in_str(string)]:
        if sp_summary == ("rare", "rafeh"):
            sp_fp = _rafeh_fp(string)
        else:
            sp_fp = "unicode", *sp_summary
        _my_append(features, sp_fp, string)
    varika_count = string.count(hpo.VARIKA)
    if varika_count == 1:
        _my_append(features, ("unicode", "varika"), string)
    elif varika_count >= 2:
        _my_append(features, ("unicode", "varika", "two-in-a-word"), string)
    if qq_acc_fp := _qq_acc_fp(string):
        _my_append(features, qq_acc_fp, string)
    if xatef_on_ng_fp := _xatef_on_ng_fp(string):
        _my_append(features, xatef_on_ng_fp, string)
    return features
