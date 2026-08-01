"""Exports make, chapnver, get_povr, decrement_povr, set_povr"""


def make(chnu, vrnu, povr):
    """Construct a cvp"""
    return _HIDE(chnu, vrnu, povr)


def chapnver(cvp):
    """Get chapter and verse pair."""
    return _UNHIDE(cvp)[0:2]


def get_povr(cvp):
    """Get part of verse (atom index, None, 'a', or 'b')"""
    return _UNHIDE(cvp)[2]


def decrement_povr(cvp):
    """
    Construct a new cvp based on the given cvp
    but with povr ("part of verse") set to one less than what was given.
    """
    povr = get_povr(cvp)
    assert povr > 1
    return set_povr(cvp, povr - 1)


def set_povr(cvp, povr):
    """
    Construct a new cvp based on the given cvp
    but with povr ("part of verse") set to the povr given.
    """
    the_chapnver = chapnver(cvp)
    return make(*the_chapnver, povr)


# def _hide_y(*parts):
#     return {'_cvp': parts}


# def _unhide_y(cvp):
#     return cvp['_cvp']


# _HIDE, _UNHIDE = _hide_y, _unhide_y


def _hide_n(*parts):
    return parts


def _unhide_n(cvp):
    return cvp


_HIDE, _UNHIDE = _hide_n, _unhide_n
