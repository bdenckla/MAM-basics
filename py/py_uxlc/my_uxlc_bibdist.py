"""
Exports:
    calc
    make_none
    make_zero
    get_word_count
    add
    subtract
    rekey
"""

import py_uxlc.my_uxlc_cvp as cvp


def calc(uxlc, std_bkid, cvp_range):
    """
    Calculate bibdist of cvp_range in book bkid using uxlc.
    (We use "bibdist" to mean Biblical distance
    (word count).)
    """
    book = uxlc[std_bkid]
    cvp_start, cvp_stop = cvp_range
    cai_start = _cvp_atom_num(cvp_start)
    wd_count = -cai_start
    chnu, vrnu = cvp.chapnver(cvp_start)
    while (chnu, vrnu) < cvp.chapnver(cvp_stop):
        wd_count += len(book[chnu - 1][vrnu - 1])
        chnu, vrnu = _get_next_cv(book, chnu, vrnu)
    cai_stop = _cvp_atom_num(cvp_stop)
    wd_count += cai_stop + 1  # + 1 because stop is inclusive
    bibdist = _make(wd_count)
    return bibdist


def make_none():
    """Construct an "all nones" bibdist."""
    return _make(None)


def make_zero():
    """Construct an "all zeroes" bibdist."""
    return _make(0)


def get_word_count(bibdist):
    """Return the word count"""
    return bibdist["_bibdist_word_count"]


def add(bibdist_a, bibdist_b):
    """Return bibdist a plus bibdist b."""
    wc_sum = _add2(bibdist_a, bibdist_b, "_bibdist_word_count")
    return _make(wc_sum)


def subtract(bibdist_a, bibdist_b):
    """Return bibdist a minus bibdist b."""
    wc_diff = _subtract2(bibdist_a, bibdist_b, "_bibdist_word_count")
    return _make(wc_diff)


def rekey(the_bibdist, wkey):
    """Return a bibdist as a dict with the given keys for the word count"""
    return {wkey: the_bibdist["_bibdist_word_count"]}


def _make(word_count):
    """Construct a bibdist."""
    return {"_bibdist_word_count": word_count}


def _add2(dic_a, dic_b, key):
    return dic_a[key] + dic_b[key]


def _subtract2(dic_a, dic_b, key):
    return dic_a[key] - dic_b[key]


def _cvp_atom_num(the_cvp):
    # location within verse: None, int, 'a', or 'b'
    part_of_verse = cvp.get_povr(the_cvp)
    if isinstance(part_of_verse, int):
        return part_of_verse
    assert part_of_verse is None or part_of_verse in ("a", "b")
    return 1


def _get_next_cv(book, chnu, vrnu):
    if vrnu + 1 > len(book[chnu - 1]):
        return chnu + 1, 1
    return chnu, vrnu + 1
