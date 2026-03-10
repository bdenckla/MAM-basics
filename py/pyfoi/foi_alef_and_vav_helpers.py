""" Exports find_fois_in_str """

import re
from pycmn import hebrew_letters as hl
from pycmn import hebrew_points as hpo
from pycmn import hebrew_accents as ha
from pyfoi import regexp_helpers as rh


def find_fois_in_str(string):
    """Find "dual mater lectionis" combos in a string."""
    for pattrec in _PATTRECS:
        if matches := re.findall(_pr_patt(pattrec), string):
            # At this point, yes, we've matched a pattern,
            # so now the question becomes:
            # is this a match we want to record?
            # We answer this by asking whether this pattern
            # has a foi path.
            if foi_path := _pr_foi_path(pattrec):
                if len(matches) > 1:
                    foi_path += (str(len(matches)),)
                foi_target = string
                return [(foi_path, foi_target)]
            return []
    return []


def _pr_patt(pattrec):
    return pattrec[0]


def _pr_foi_path(pattrec):
    return pattrec[1]


def _re_or(*alternates):
    return rh.ncpar("|".join(alternates))


def _star(regexp):
    return rh.ncpar(regexp, "*")


def _alef_vav_pattern(prefix="", suffix=""):
    return prefix + _ALEF_VAV_PATTERN + suffix


def _vav_alef_pattern(prefix="", suffix=""):
    return prefix + _VAV_ALEF_PATTERN + suffix


def _alef_vav_pattrec(end_of_path, prefix="", suffix=""):
    top_path_part_av = "avva-alef-vav"
    return (
        _alef_vav_pattern(prefix=prefix, suffix=suffix),
        (top_path_part_av, end_of_path),
    )


def _vav_alef_pattrec(end_of_path, prefix="", suffix=""):
    top_path_part_va = "avva-vav-alef"
    return (
        _vav_alef_pattern(prefix=prefix, suffix=suffix),
        (top_path_part_va, end_of_path) if end_of_path is not None else None,
    )


_VOWEL_MARK_RANGE = "\u05b0-\u05bb\u05c7"
_VAV_XOLAM = hl.VAV + hpo.XOLAM
_SHURUQ = hl.VAV + hpo.DAGOMOSD  # we assume this is not truly vav with dag.
_NOT_DOM_OR_XOLAM = rh.nsqb(hpo.DAGOMOSD + hpo.XOLAM)
_DAGQ = hpo.DAGOMOSD + r"?"
_VOWEL_MARK = rh.sqb(_VOWEL_MARK_RANGE)
_VAV_MALE_VOWEL = _re_or(_VAV_XOLAM, _SHURUQ)
_ACCAM_STAR = _star(rh.sqb(ha.ACCENTS_AND_MTG))
_ACCAM_STAR_THEN_VAV_MALE_VOWEL = _ACCAM_STAR + _VAV_MALE_VOWEL
_NON_LETT_STAR = rh.ZM_NL
#
_PRE_AV_SIN_MEM = hl.SHIN + hpo.SIND + _DAGQ + hpo.SHEVA + hl.MEM
_PRE_AV_XET_TET = hl.XET + hpo.PATAX + hl.TET + hpo.DAGOMOSD
_PRE_AV_MEM_LAM = hl.MEM + rh.sqb(hpo.PATAX + hpo.SHEVA) + hl.LAMED + _DAGQ
_ALEF_VAV_PATTERN = hpo.XOLAM + _NON_LETT_STAR + hl.ALEF + hl.VAV
_VAV_ALEF_PATTERN = hl.VAV + hpo.XOLAM + hl.ALEF
_PATTRECS_AV = (  # Order matters! First one to match "wins"!
    _alef_vav_pattrec("c-smol", prefix=_PRE_AV_SIN_MEM, suffix=hl.LAMED),
    _alef_vav_pattrec("c-xatot", prefix=_PRE_AV_XET_TET, suffix=hl.TAV),
    _alef_vav_pattrec("c-m.lot", prefix=_PRE_AV_MEM_LAM, suffix=hl.TAV),
    _alef_vav_pattrec("b-ot", suffix=hl.TAV),
    _alef_vav_pattrec("a-misc", suffix=_NOT_DOM_OR_XOLAM),
)
_PATTRECS_VA = (  # Order matters! First one to match "wins"!
    # None 1st arg means don't record this
    _vav_alef_pattrec(None, suffix=_ACCAM_STAR_THEN_VAV_MALE_VOWEL),
    _vav_alef_pattrec(None, suffix=_VOWEL_MARK),
    _vav_alef_pattrec("b-not-final", suffix=rh.LETT),
    _vav_alef_pattrec("a-misc"),
)
_PATTRECS = *_PATTRECS_AV, *_PATTRECS_VA
