"""Exports read_book: UXLC book -> chapters of verses of atoms, with <x> codes.

This mirrors the FOIs reader pattern (see py/main_fois.py), but keeps only what
the CLC skeleton needs: each atom's text plus the one-letter ``<x>`` note codes
UXLC attached to it. Atoms are dicts so downstream code reads clearly:

    {"kind": "w" | "q" | "k", "text": str, "types": [note_code, ...]}
"""

import uxlc_misc.my_uxlc as my_uxlc


def read_book(book_id):
    """Read a UXLC book into chapters -> verses -> atoms (see module docstring)."""
    return my_uxlc.read(book_id, _VERSE_CHILD_HANDLERS)


def _stripped(value):
    return value.strip() if value else ""


def _append_text(atom, value):
    text = _stripped(value)
    if text:
        atom["text"] += text


def _append_inner_text(accum, element, handlers):
    _append_text(accum[-1], element.text)
    for child in element:
        my_uxlc.dispatch_on_tag(accum, child, handlers)
        _append_text(accum[-1], child.tail)


def _handle_word(kind, accum, verse_child):
    accum.append({"kind": kind, "text": "", "types": []})
    _append_inner_text(accum, verse_child, _WORD_CHILD_HANDLERS)


def _handle_wc_s(accum, word_child_s):
    # <s> implements small/large/suspended letters, e.g. <s t="large">וֹ</s>.
    _append_inner_text(accum, word_child_s, _WORD_CHILD_HANDLERS)


def _handle_wc_x(accum, word_child_x):
    note_code = _stripped(word_child_x.text)
    if note_code:
        accum[-1]["types"].append(note_code)


_WORD_CHILD_HANDLERS = {
    "x": _handle_wc_x,
    "s": _handle_wc_s,
}
_VERSE_CHILD_HANDLERS = {
    "w": lambda accum, child: _handle_word("w", accum, child),
    "q": lambda accum, child: _handle_word("q", accum, child),
    "k": lambda accum, child: _handle_word("k", accum, child),
    "x": my_uxlc.handle_xc_ignore,
    "pe": my_uxlc.handle_xc_ignore,
    "samekh": my_uxlc.handle_xc_ignore,
    "reversednun": my_uxlc.handle_xc_ignore,
}
