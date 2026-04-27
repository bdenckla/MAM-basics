"""Unicode denormalization for Hebrew mark ordering."""

import re
from pycmn import hebrew_points as hpo

__all__ = ["give_std_mark_order", "has_std_mark_order", "give_aht_mark_order"]


def give_std_mark_order(string):
    """
    Give the string (our) standard mark order.
    Our standard mark order is not Unicode-normal order,
    but we think it is a more reasonable order than Unicode-normal order.
    Our standard mark order has the following four marks first
    (in the order shown), followed by all other marks:
        shin dot
        sin dot
        dagesh/mapiq/shuruq dot
        rafeh
    """
    # TODO: what about varika? A standard order (combining class) should be given to varika.
    pattclu = r"[א-ת]" + hpo.RE_APCV_STAR  # pattern for a cluster
    return re.sub(pattclu, _repl_cluster, string)


def has_std_mark_order(string):
    """
    Say whether the string has (our) standard mark order.
    """
    return string == give_std_mark_order(string)


def give_aht_mark_order(string):
    """
    Give the string AHT's mark order
    (as dictated to Hillel by the Academy of the Hebrew Language).
    """
    pattclu = r"[א-ת]" + hpo.RE_APCV_STAR  # pattern for a cluster
    return re.sub(pattclu, _repl_cluster_aht, string)


def _repl_cluster(match):
    wmat = match.group()  # the whole match
    lett, marks = wmat[0], wmat[1:]
    return lett + "".join(sorted(marks, key=_ccs_keyfn))


def _repl_cluster_aht(match):
    wmat = match.group()  # the whole match
    lett, marks = wmat[0], wmat[1:]
    return lett + "".join(sorted(marks, key=_ccs_keyfn_aht))


_NS_COMB_CLASSES = {  # nonstandard combining classes
    # Only the order matters, not the specific values. Both the order and
    # specific values below correspond to "SBL2", by which I mean the
    # nonstandard combining classes suggested in the appendix to the manual
    # for the SBL Hebrew Font.
    hpo.SHIND: 10,
    hpo.SIND: 11,
    hpo.DAGOMOSD: 21,
    hpo.RAFE: 23,
}


_NS_COMB_CLASSES_AHT = {
    hpo.SHIND: 10,
    hpo.SIND: 11,
    hpo.DAGOMOSD: 1,  # Here's the weirdness! (Compare to 21 above.)
    hpo.RAFE: 23,
}


def _ccs_keyfn(char):
    return _NS_COMB_CLASSES.get(char) or 300


def _ccs_keyfn_aht(char):
    return _NS_COMB_CLASSES_AHT.get(char) or 300
