"""Exports the CLC ketiv/qere ruby builder (design doc §7.5 K/Q display).

UXLC encodes a ketiv/qere word as adjacent ``<k>`` (ketiv, the written form,
left unpointed) and ``<q>`` (qere, the read form, pointed) atoms; clc_read tags
them ``kind`` ``"k"`` / ``"q"`` (plain words are ``"w"``). This module turns a
verse's flat atom list into render units and renders each K/Q unit as an HTML
``<ruby>`` with the **qere on the baseline** (the reading) and the **ketiv as
the annotation above it** (cf. MAM-basics mpplus_display).

Two masoretic edge cases lack one member; each shows a small, bracketed,
editorial placeholder in the *missing member's own slot* (so the baseline always
represents the reading):

  * **qere-without-ketiv** (קרי ולא כתיב — read, not written): no ``<k>``; the
    annotation shows ``[אין כתיב]`` ("no ketiv").
  * **ketiv-without-qere** (כתיב ולא קרי — written, not read): no ``<q>``; the
    baseline shows ``[אין קרי]`` ("no qere"), the written word sits above it.

Only the placeholder is small/muted; real Hebrew (incl. the ketiv) is full-size,
set off purely by being unpointed and above (gh-pages/style.css ``clc-kq*``).

A K/Q *unit* is a maximal run of zero-or-more ketiv atoms then zero-or-more qere
atoms, delimited exactly as py/uxlc_fois/fois_kq_foi.py does: a plain ``"w"``
flushes the unit, and a ``"k"`` arriving while a qere is already pending starts a
new one. So ``k,q,k,q`` yields TWO ``(1,1)`` units while ``k,k,q,q`` yields ONE
``(2,2)`` unit — the interleaved-vs-grouped ("kqkq" vs "kkqq") distinction that
the per-unit box (one box = one unit) makes visible.
"""

from dataclasses import dataclass

import uxlc_misc.uxlc_utils_html as H

# Editorial placeholders for the absent member (brackets are part of the text).
_NO_QERE = "[אין קרי]"  # ketiv-without-qere: nothing is read
_NO_KETIV = "[אין כתיב]"  # qere-without-ketiv: nothing is written


@dataclass(frozen=True)
class Word:
    """A single atom in reading order: its 1-based verse position and text.

    Used both for a plain word and for each ketiv/qere member of a KqUnit; the
    position is the note-attachment key (the (ch, v, position) into notes_by_atom).
    """

    position: int
    text: str


@dataclass(frozen=True)
class KqUnit:
    """One ketiv/qere apparatus unit: its ketiv member(s) and qere member(s)."""

    ketivs: tuple  # tuple[Word]; empty for qere-without-ketiv
    qeres: tuple  # tuple[Word]; empty for ketiv-without-qere


def iter_render_units(verse_atoms):
    """Yield Word and KqUnit items, in reading order, for one verse's atoms.

    See the module docstring for the (fois_kq_foi-mirroring) unit-delimiting
    rule. ``verse_atoms`` is the clc_read atom list (dicts with kind/text/types).
    """
    ketivs, qeres = [], []
    for position, atom in enumerate(verse_atoms, start=1):
        kind = atom["kind"]
        if kind == "w":
            if ketivs or qeres:
                yield KqUnit(tuple(ketivs), tuple(qeres))
                ketivs, qeres = [], []
            yield Word(position, atom["text"])
        elif kind == "k":
            if qeres:  # a ketiv after a qere starts a fresh unit
                yield KqUnit(tuple(ketivs), tuple(qeres))
                ketivs, qeres = [], []
            ketivs.append(Word(position, atom["text"]))
        elif kind == "q":
            qeres.append(Word(position, atom["text"]))
        else:
            raise AssertionError(f"unexpected atom kind: {kind!r}")
    if ketivs or qeres:
        yield KqUnit(tuple(ketivs), tuple(qeres))


def join_text(unit):
    """Text whose trailing maqaf governs whether the next word butts on.

    The baseline carries the reading, so the qere's last member decides; with no
    qere the baseline is the (maqaf-free) placeholder, so return "" → a space.
    """
    return unit.qeres[-1].text if unit.qeres else ""


def kq_ruby(unit, notes_by_atom, ch, v):
    """Build the ``<ruby class="clc-kq">`` htel for one K/Q unit."""
    base = _side(unit.qeres, "clc-kq-q", _NO_QERE, notes_by_atom, ch, v)
    annotation = _side(unit.ketivs, "clc-kq-k", _NO_KETIV, notes_by_atom, ch, v)
    contents = [*base, H.rp("("), H.rt(annotation), H.rp(")")]
    # Wrap in an inline-block so the box (gh-pages/style.css) can enclose the
    # WHOLE ruby: a border on the <ruby> itself only hugs the base line, leaving
    # the <rt> annotation outside it.
    return H.span_c(H.ruby(contents, {"class": "clc-kq"}), "clc-kq-box")


def _side(members, real_class, none_text, notes_by_atom, ch, v):
    """One ruby side: real members joined by spaces, or a lone placeholder."""
    if not members:
        return [H.span_c(none_text, "clc-kq-none")]
    pieces = []
    for i, member in enumerate(members):
        if i:
            pieces.append(" ")
        pieces.append(_member_span(member, real_class, notes_by_atom, ch, v))
    return pieces


def _member_span(member, css_class, notes_by_atom, ch, v):
    """A member's span, highlighted (clc-doc-target) if the atom has a note.

    A noted K/Q member is flagged like any other noted word, but not linked: its note
    sits in the same row's doc cell beside it (clc_render dropped same-page note
    anchors), so there is nothing to jump to.
    """
    span = H.span_c(member.text, css_class)
    if (ch, v, member.position) in notes_by_atom:
        return H.span([span], {"class": "clc-doc-target"})
    return span
