"""Exports mark"""

from py_misc import slh_description
from pycmn import ws_tmpl2 as wtp
from pycmn import template_names as tmpln
from pycmn import shrink


def mark(wtseq):
    """Mark slh words. (slh: small, large, and/or hung)"""
    assert isinstance(wtseq, tuple)
    return tuple(_mark_list(list(wtseq)))


def _mark_list(wtseq):
    assert isinstance(wtseq, list)
    wtseq2 = list(map(_recurse_down_into_tmpls, wtseq))  # depth first
    return _mark_slh_words_shallowly(wtseq2)


def _recurse_down_into_tmpls(wtel):
    if not wtp.is_template(wtel):
        return wtel
    return wtp.mktmpl_mp(_mark_list, wtel)


def _mark_slh_words_shallowly(wtseq):
    assert isinstance(wtseq, list)
    if wtseq == [""]:
        return wtseq  # avoids some problems with [''] turning into []
    edin_wtseqs = []
    for i, wtel in enumerate(wtseq):
        edin_wtseq, del_offsets = _make_edin(wtseq[:i], wtel, wtseq[i + 1 :])
        edin_wtseqs.append(edin_wtseq)
        if del_offsets:
            del_indexes = [i + doff for doff in del_offsets]
            return _do_deletes_and_start_over(wtseq, edin_wtseqs, del_indexes)
    return sum(edin_wtseqs, [])


def _do_deletes_and_start_over(wtseq, edin_wtseqs, del_indexes):
    new_wtseq = []
    for i, edin_wtseq in enumerate(edin_wtseqs):
        if i not in del_indexes:
            new_wtseq.extend(edin_wtseq)
    for i in range(len(edin_wtseqs), len(wtseq)):
        if i not in del_indexes:
            new_wtseq.append(wtseq[i])
    return _mark_slh_words_shallowly(new_wtseq)


def _make_edin(wtseq_pre, wtel, wtseq_post):
    assert isinstance(wtseq_pre, list)
    assert isinstance(wtseq_post, list)
    if wtel is None:  # from a "forward delete"
        return [], []
    if not _is_slh(wtel):
        return [wtel], []
    #
    pre_targ, a_of_abc = _get_pre_targ(wtseq_pre)
    #
    c_of_abc, post_targ = _get_post_targ(wtseq_post)
    #
    wtseq_targ = shrink.shrink([*a_of_abc, wtel, *c_of_abc])
    del_offsets = []
    del_offsets.extend(list(range(-len(a_of_abc), 0)))
    del_offsets.extend(list(range(1, 1 + len(c_of_abc))))
    wtseq_out = shrink.shrink(
        [*pre_targ, _make_tmpl_for_slh_word(wtseq_targ), *post_targ]
    )
    return wtseq_out, del_offsets


def _get_pre_targ(wtseq_pre):
    a_of_abc = []
    for wtel in reversed(wtseq_pre):
        if isinstance(wtel, str) and _my_rpartition(wtel):
            part = _my_rpartition(wtel)
            a_of_abc.insert(0, part[2])
            pre_targ = [part[0] + part[1]]
            return pre_targ, a_of_abc
        if _is_word_ender(wtel):
            return [], a_of_abc
        assert _is_valid_targ_content(wtel)
        a_of_abc.insert(0, wtel)
    return [], a_of_abc


def _get_post_targ(wtseq_post):
    c_of_abc = []
    for wtel in wtseq_post:
        if isinstance(wtel, str) and _my_partition(wtel):
            part = _my_partition(wtel)
            c_of_abc.append(part[0])
            post_targ = [part[1] + part[2]]
            return c_of_abc, post_targ
        if _is_word_ender(wtel):
            return c_of_abc, []
        assert _is_valid_targ_content(wtel)
        c_of_abc.append(wtel)
    return c_of_abc, []


def _my_rpartition(string):
    seps = " =<>,;:"
    partitions = [string.rpartition(sep) for sep in seps]
    shortest_partition = partitions[0]
    for partition in partitions[1:]:
        if len(partition[2]) < len(shortest_partition[2]):
            shortest_partition = partition
    if shortest_partition[2] == string:
        return None
    return shortest_partition


def _my_partition(string):
    seps = " =<>,;:"
    partitions = [string.partition(sep) for sep in seps]
    shortest_partition = partitions[0]
    for partition in partitions[1:]:
        if len(partition[0]) < len(shortest_partition[0]):
            shortest_partition = partition
    if shortest_partition[0] == string:
        return None
    return shortest_partition


def _make_tmpl_for_slh_word(wtseq):
    desc_parts = slh_description.get_parts(wtseq)
    desc0, desc1, desc2, desc3 = desc_parts
    desc3_es = slh_description.desc3_encoded_as_a_str(desc3)
    desc_args = [[desc0], [desc1], [desc2], [desc3_es]]
    return wtp.mktmpl([[tmpln.SLH_WORD], wtseq, *desc_args])


def _is_slh(wtel):
    return (
        wtp.is_template_with_name(wtel, "מ:אות-ק")
        or wtp.is_template_with_name(wtel, "מ:אות-ג")
        or wtp.is_template_with_name(wtel, "מ:אות תלויה")
    )


def _is_valid_targ_content(wtel):
    # Below, מ:פסק is needed:
    #     * only for משלי ל,טו (Proverbs 30:15)
    #     * on top of that, only when processing old versions of MAM
    # I guess at some point that paseq was converted to a legarmeih.
    # Similarly, מ:לגרמיה ("classic" legarmeih) is only needed for old versions of MAM.
    return (
        isinstance(wtel, str)
        or wtp.is_template_with_name(wtel, "מ:לגרמיה-2")
        or wtp.is_template_with_name(wtel, "מ:לגרמיה")
        or wtp.is_template_with_name(wtel, "מ:פסק")
        or _is_slh(wtel)
    )


def _is_word_ender(wtel):
    return wtp.is_template_with_name(wtel, "ר1")
