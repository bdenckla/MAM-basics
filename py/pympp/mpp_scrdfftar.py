"""Exports add"""

from pycmn import ws_tmpl2 as wtp
from pycmn import template_names as tmpln
from pycmn import hebrew_punctuation as hpu

# scroll differences (mostly) (entirely?) fall into the following categories:
#    letter differences e.g. yod vs. vav or yod vs. nothing
#    letter size differences e.g. small vs. normal-sized
#    horiz. spacing differences, e.g. two words vs 1 word, e.g. 'x y' vs 'xy'
#    paragraph separation differences, e.g. no separation vs. petuxah
#
# This is displayed on Wikisource as a footnote.
# Don't confuse this template with the much more common
# documentation template (נוסח).


def add(wtseq):
    """
    For each scrdff in wtseq, add a TARGETED scrdff.
    (scrdff: scroll-difference [note])
    (wtseq: Wikitext [element] sequence)
    Normal scrdff notes just have a location, whereas targeted scrdff notes
    have a target. By a "target" I mean a sequence of Wikitext elements
    (e.g. a string) to which the note applies. Another way of putting it: a
    מ:הערה-2 (a targeted scrdff note) is more like a נוסח (documentation
    note), since a נוסח, unlike a מ:הערה, has a target.
    """
    assert isinstance(wtseq, tuple)
    edit_instructions = tuple(
        _make_edit_instructions(wtseq[:i], wtseq[i], wtseq[i + 1 :])
        for i in range(len(wtseq))
    )
    return _execute_edit_instructions(edit_instructions)


def _execute_edit_instructions(edit_instructions):
    del_indexes = []
    for i, edin in enumerate(edit_instructions):
        for del_offset in edin[1]:
            del_indexes.append(i + del_offset)
    out = []
    for i, edin in enumerate(edit_instructions):
        if i not in del_indexes:
            out.append(edin[0])
    return sum(out, tuple())


def _make_edit_instructions(wtseq_pre, wtel, wtseq_post):
    if not wtp.is_scrdff_template(wtel):
        del_offsets = []
        return (wtel,), del_offsets
    scrdff_el1 = wtp.template_element(wtel, 1)
    wtel_post = wtseq_post[0] if wtseq_post else None
    edin = _make_edin_for_scrdff(wtseq_pre, scrdff_el1, wtel_post)
    out_wtseq, del_offsets = edin
    for del_offset in del_offsets:
        assert del_offset != 0 and _sgn(del_offset) == _sgn(del_offsets[0])
    if del_offsets[0] < 0:
        out_wtseq2 = *out_wtseq, wtel
    else:
        out_wtseq2 = wtel, *out_wtseq
    return out_wtseq2, del_offsets


def _sgn(an_int):
    return -1 if an_int < 0 else (1 if an_int > 0 else 0)


def _make_edin_for_scrdff(wtseq_pre, scrdff_el1, wtel_post):
    if wtseq_pre and wtp.is_doc_template(wtseq_pre[-1]):
        # pbd_yes: preceded by doc: yes
        return _make_edin_for_scrdff_pbd_yes(wtseq_pre[-1], scrdff_el1)
    # pbd_no: preceded by doc: no
    return _make_edin_for_scrdff_pbd_no(wtseq_pre, scrdff_el1, wtel_post)


def _make_edin_for_scrdff_pbd_yes(doc_tmpl, scrdff_el1):
    # We assume that the target of an spbd is the target of that doc.
    # (spbd: scrdff preceded by a doc)
    # So, a scrdff preceded by a doc becomes a doc with a scrdfftar
    # as its target. Schematically,
    #     doc(
    #         doc_target,
    #         doc_part1,
    #         doc_part2, ...),
    #     scrdff(scrdff_text)
    # becomes
    #     doc(
    #         scrdfftar(doc_target, scrdff_text),
    #         doc_part1,
    #         doc_part2, ...)
    doc_tmpl_pvs = wtp.template_param_vals(doc_tmpl)
    new_doc_tmpl_els = [
        ["נוסח"],
        [_make_scrdfftar(doc_tmpl_pvs[0], scrdff_el1)],
        *doc_tmpl_pvs[1:],
    ]
    wtseq_out = (wtp.mktmpl(new_doc_tmpl_els, ignore_equals=True),)
    return wtseq_out, [-1]


def _make_edin_for_scrdff_pbd_no(wtseq_pre, scrdff_el1, wtel_post):
    # A scrdff NOT preceded by a doc becomes a scrdfftar.
    # The hard part is figuring out what the target should be.
    # taf: targ and friends
    taf = _get_taf(wtseq_pre, wtel_post)
    scrdfftar = _make_scrdfftar([taf["targ"]], scrdff_el1, taf["mark_is_pre_word"])
    wtseq_out = *taf["pre_targ"], scrdfftar, *taf["post_targ"]
    return wtseq_out, taf["del_offsets"]


def _mk_taf(targ, del_offsets, pre_and_post=None, mipw=False):
    return {
        "targ": targ,
        "del_offsets": del_offsets,
        "pre_targ": pre_and_post[0] if pre_and_post else tuple(),
        "post_targ": pre_and_post[1] if pre_and_post else tuple(),
        "mark_is_pre_word": mipw,
    }


def _get_taf(wtseq_pre, wtel_post):
    wtel_pre = wtseq_pre[-1]
    if isinstance(wtel_pre, str):
        return _get_taf_str(wtseq_pre, wtel_post)
    if _is_double_pe(wtel_pre):
        # wtel_pre is the targ, [wtseq_pre_index] is the del_offsets
        return _mk_taf(wtel_pre, [-1])
    assert False


def _get_taf_str(wtseq_pre, wtel_post):
    wtel_pre = wtseq_pre[-1]
    if wtel_pre.endswith(" "):  # hack to identify pre-word note
        # The only pre-word note is on קַן־צִפּ֣וֹר, in Deut 22:6.
        # wtel_post is the targ, [1] is the del_offsets
        return _mk_taf(wtel_post, [1], mipw=True)
    lenwp = len(wtseq_pre)
    start = lenwp
    # start == n + (-2) + 1 == n - 1
    # for the only interesting case, i.e.
    # the case where wtseq_pre_index == -2.
    # That case happens to have n == 3, yielding
    # start == 3 + (-2) + 1 == 2
    pre_targ = tuple()
    post_targ = wtseq_pre[start:lenwp]
    targ = wtel_pre
    del_offsets = list(range(-1, 0))
    if " " in wtel_pre:
        pre_targ_str, space, targ = wtel_pre.rpartition(" ")
        pre_targ = (pre_targ_str + space,)
    if targ.endswith(hpu.SOPA):
        # Note marker after sof pasuq only happens in D11:21,
        # and only then as an accident of the particular transclusion needs
        # of this verse in the Hebrew Wikisource edition.
        # So, we eject sof pasuq from the scrdfftar target.
        targ = targ[:-1]
        post_targ = hpu.SOPA, *post_targ
    return _mk_taf(targ, del_offsets, (pre_targ, post_targ))


def _make_scrdfftar(target, scrdff_el1, mark_is_pre_word=False):
    starpos = "*אאא" if mark_is_pre_word else "אאא*"
    return wtp.mktmpl([[tmpln.SCRDFF_TAR], target, scrdff_el1, [starpos]])


def _is_double_pe(wtel):
    return wtp.is_template_with_name(wtel, "פפ")
