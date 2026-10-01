import mb_cmn.hebrew_letters as hl
import mb_cmn.hebrew_punctuation as hpu
import phonetic_mam.core.dualcant_flexword as fw
import phonetic_mam.core.dualcant_arguments as gdc
from mb_cmn.shrink import shrink


def align_dcargs(dcargs):
    # dcargs: dualcant [template] args
    assert len(dcargs) == 3
    super = _process_single_dcarg(dcargs[0], "כפול=")
    alef = _process_single_dcarg(dcargs[1], "א=")
    bet = _process_single_dcarg(dcargs[2], "ב=")
    if not super:
        assert not alef and not bet
        return []
    alef_f = _fit_to_super(super, alef)  # alef_f: alef flexwords
    bet_f = _fit_to_super(super, bet)  # bet_f: alef flexwords
    _do_checks(super, alef_f, bet_f)
    aligned_cantillation = {
        "aligned-cant-superimposed": super,
        "aligned-cant-alef": alef_f,
        "aligned-cant-bet": bet_f,
    }
    return [aligned_cantillation]


def _do_checks(super, alef_f, bet_f):
    assert len(super) == len(alef_f) == len(bet_f)
    super_f = map(_make_flexword, super)
    assert _loao_flexwords(super_f) == _loao_flexwords(alef_f) == _loao_flexwords(bet_f)


def _make_flexword(obj):
    if isinstance(obj, str):
        return {"word-simple": obj}
    if gdc.is_dcargs_qamats(obj):
        return obj
    assert False, obj


def _process_single_dcarg(dcarg, something_eq):
    if not dcarg:
        return []
    assert isinstance(dcarg[0], str)
    if dcarg[0].startswith(something_eq):
        sans_pre = dcarg[0].removeprefix(something_eq)
    else:
        sans_pre = dcarg[0]
    dcarg_1 = [sans_pre, *dcarg[1:]]
    dcarg_2 = shrink(dcarg_1)
    if not dcarg_2:
        return dcarg_2
    out = dcarg_2[0].split(" ")
    for elem in dcarg_2[1:]:
        if out[-1] == "":
            assert gdc.is_dcargs_qamats(elem)
            out[-1] = elem
        elif gdc.is_dcargs_qamats(out[-1]):
            assert isinstance(elem, str)
            elem_words = elem.split(" ")
            assert elem_words[0] == ""
            out.extend(elem_words[1:])
        else:
            assert False, elem
    return out


def _fit_to_super(super, alef_or_bet):
    start_cw_idx = 0  # cw: chanted word
    flexwords = []
    for chanted_word_in_super in super:
        if gdc.is_dcargs_qamats(chanted_word_in_super):
            assert gdc.is_dcargs_qamats(alef_or_bet[start_cw_idx])
            flexwords.append(alef_or_bet[start_cw_idx])
            start_cw_idx += 1
            continue
        loao_cw_in_super = _letters_of_atoms_of_strword(chanted_word_in_super)
        for length_in_cws in (1, 2, 3):
            stop_cw_idx = start_cw_idx + length_in_cws
            list_of_strwords = alef_or_bet[start_cw_idx:stop_cw_idx]
            letters_of_atoms = _letters_of_atoms_of_los(list_of_strwords)
            if letters_of_atoms == loao_cw_in_super:
                flexwords.append(_simplify(list_of_strwords))
                start_cw_idx += length_in_cws
                break
    return flexwords


def _simplify(list_of_strwords):
    if len(list_of_strwords) > 1:
        return {"word-multi": list_of_strwords}
    return {"word-simple": list_of_strwords[0]}


def _letters_of_atoms_of_strword(strword):
    # strword: a chanted word represented as a string
    assert isinstance(strword, str)
    atoms = hpu.split_at_maq(strword)
    return list(map(hl.letters, atoms))


def _letters_of_atoms_of_los(list_of_strwords):
    # los: list of strwords
    assert isinstance(list_of_strwords, list)
    list_of_lists = list(map(_letters_of_atoms_of_strword, list_of_strwords))
    flat_out = sum(list_of_lists, [])
    return flat_out


def _letters_of_atoms_of_qamats_val(qamats_val):
    assert isinstance(qamats_val, list)
    assert len(qamats_val) == 2
    loao_dalet = _letters_of_atoms_of_strword(qamats_val[0])
    loao_samekh = _letters_of_atoms_of_strword(qamats_val[1])
    assert loao_dalet == loao_samekh
    return loao_dalet


def _letters_of_atoms_of_flexword(flexword):
    # A flexword is a singleton dict whose one key-value pair is one of the following:
    #    * 'word-simple' and a chanted word represented as a string
    #    * 'word-multi' and a list of chanted words represented as strings.
    # (In practice the list at key 'word-multi' is always of length 2.)
    return fw.dispatch_on_flexword(
        _letters_of_atoms_of_strword,
        _letters_of_atoms_of_los,  # los: list of strwords
        _letters_of_atoms_of_qamats_val,
        flexword,
    )


def _loao_flexwords(seq_of_flexwords):  # loao: letters of atoms of
    return list(map(_letters_of_atoms_of_flexword, seq_of_flexwords))
