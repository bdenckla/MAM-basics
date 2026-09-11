"""Exports mark"""

from mb_misc import slh_description
from mpplus import mpplus_boring_tmpls
from mb_cmn import ws_tmpl2 as wtp
from mb_cmn import ws_tmpl_named_params as wtnp
from mb_cmn import template_names as tmpln
from mb_cmn import shrink


def mark(wtseq):
    """Mark small-, large-, and hung-letter words in classified Scripture branches.

    MAM-parsed-plus retains ketiv and qere and every cantillation, qamats, and
    stress-helper alternative for edition display, so each named Scripture branch
    is visited.  Note prose and descriptive parameters are preserved without being
    searched for letters to mark.  A new template raises until its parameter roles
    are classified.
    """
    assert isinstance(wtseq, tuple)
    return tuple(_mark_list(list(wtseq)))


def _mark_list(wtseq):
    assert isinstance(wtseq, list)
    wtseq2 = list(map(_recurse_down_into_tmpls, wtseq))  # depth first
    return _mark_slh_words_shallowly(wtseq2)


def _recurse_down_into_tmpls(wtel):
    if not wtp.is_template(wtel):
        return wtel
    name = wtp.template_name(wtel)
    if name in mpplus_boring_tmpls._HANDLERS:
        mpplus_boring_tmpls.validate_current_handler_input_template(wtel)
    else:
        tmpln.validate_current_plus_template(wtel)
    selected_keys = _slh_scripture_param_keys(name)
    if not selected_keys:
        return wtel
    params = dict(wtel.get("tmpl_params", {}))
    for key in selected_keys:
        if key not in params:
            raise ValueError(f"{name!r} lacks required Scripture parameter {key!r}")
        marked = _mark_list(wtp.template_param_val(wtel, key))
        params[key] = wtnp.simplify_singleton(marked)
    return {"tmpl_name": name, "tmpl_params": params}


def _slh_scripture_param_keys(name):
    if name in tmpln.STD_KQ_TMPL_NAMES:
        return ("1", "2")
    if name == tmpln.TRIVIAL_QERE:
        return ("1", "3")
    if name == "קרי ולא כתיב":
        return ("1", "2")
    if name == "כתיב ולא קרי":
        return ("1",)
    if name in {"נוסח", tmpln.SCRDFF_TAR}:
        return ("1",)
    if name in tmpln.STRESS_HELPER_TMPL_NAMES:
        return ("1", "2")
    if name == tmpln.QAMATS_VARIANT:
        return ("ד", "ס")
    if name == tmpln.DUAL_CANTILLATION:
        return ("כפול", "א", "ב")
    if name in tmpln.IN_WORD_TMPL_NAMES | {"מודגש", "מ:סיום בטוב", "מ:אות מנוקדת"}:
        return ("1",)
    if name not in mpplus_boring_tmpls.RECOGNIZED_TEMPLATE_NAMES:
        raise ValueError(f"unclassified template in special-letter pass: {name!r}")
    return ()


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
    _assert_desc0_matches_targ(wtseq, desc0)
    desc3_es = slh_description.desc3_encoded_as_a_str(desc3)
    desc_args = [[desc0], [desc1], [desc2], [desc3_es]]
    return wtp.mktmpl([[tmpln.SLH_WORD], wtseq, *desc_args])


_SLH_LETTER_TMPLS = frozenset(("מ:אות-ג", "מ:אות-ק", "מ:אות תלויה"))


def _assert_desc0_matches_targ(wtseq, desc0):
    """Assert that desc0 (param 2) equals the flattened text of wtseq (param 1).

    Verifies that the SLH_WORD synthesis didn't lose any content when
    building the plain-word description from the detailed target.
    """
    stripped = _flatten_targ(wtseq)
    assert stripped == desc0, f"desc0 mismatch: {stripped!r} != {desc0!r}"


def _flatten_targ(wtseq):
    """Flatten the SLH_WORD target to plain text."""
    parts = []
    for wtel in wtseq:
        if isinstance(wtel, str):
            parts.append(wtel)
        elif wtp.template_name(wtel) in _SLH_LETTER_TMPLS:
            parts.append(wtp.template_element(wtel, 1)[0])
        elif wtp.template_name(wtel) in slh_description.PASOLEG_DESC0:
            parts.append(slh_description.PASOLEG_DESC0[wtp.template_name(wtel)])
        else:
            raise ValueError(
                f"unclassified template in special-letter target:"
                f" {wtp.template_name(wtel)!r}"
            )
    return "".join(parts)


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
