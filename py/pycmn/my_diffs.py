"""Diff utilities using SequenceMatcher."""

import difflib

__all__ = ["get"]


def get(sidea, sideb, outa=None, outb=None):
    """Provide a different interface to SequenceMatcher"""
    seqmat = difflib.SequenceMatcher(a=sidea, b=sideb, autojunk=False)
    opcodes_ne = filter(_seqmat_opcode_not_equal, seqmat.get_opcodes())
    outa = outa or sidea
    outb = outb or sideb
    diff_pairs = [_to_diff_pair(oc, outa, outb) for oc in opcodes_ne]
    return diff_pairs


def _seqmat_opcode_not_equal(seqmat_opcode):
    return seqmat_opcode[0] != "equal"


def _to_diff_pair(seqmat_opcode, outa, outb):
    _tag, as0, as1, bs0, bs1 = seqmat_opcode
    # Below converts empty lists to None
    return (outa[as0:as1] or None, outb[bs0:bs1] or None)
