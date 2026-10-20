r"""Extract the ordered POETIC *disjunctive* sequence from MAM-simple verses.

This is the cross-check oracle for the poetic scanner+grammar (Phase 2 of
``doc/PLAN-poetic-accent-grammar.md``).  The WLC poetic scanner
(``accgram.poetic_scanner``) matches over a Unicode accent-mark alphabet; MAM-simple
stores fully-pointed Unicode Hebrew with combining accent marks.  To confirm the
trees' segmentation is correct -- not merely parseable -- we reduce each side to its
ordered list of disjunctive accents (the division points) and diff those.  Servus
(conjunctive) signs are deliberately dropped: MAM and the LC often choose different
conjunctive *signs* for the same slot (e.g. the LC has the oleh-weyored servus as
galgal/yerax-ben-yomo while MAM has atnax-hafukh), and Yeivin pins no exact
servus chains, so only the disjunctive skeleton is a meaningful equality check.

Disjunctive markers, MAM Unicode accent -> poetic token (same vocabulary the
scanner emits):

  ETNAHTA (U+0591)        -> ATNAX
  OLE (U+05AB)            -> OLEH_WEYORED  (its yored merkha is folded in, as in the LC)
  GERESH MUQDAM (U+059D)  -> REVIA_MUGRASH (MAM always has the revia dot too,
                            even where the LC omits it under the geresh muqdam -- the
                            geresh muqdam alone is the reliable marker)
  REVIA (U+0597) alone    -> REVIA (generic; reclassified gadol/qatan/mugrash by
                            position, exactly as the scanner's second pass)
  DEHI (U+05AD)           -> DEXI
  ZINOR (U+05AE)          -> TSINNOR
  PAZER (U+05A1)          -> PAZER
  SHALSHELET (U+0593)     -> shalshelet gedolah IFF an ``lp-legarmeih`` paseq node
                            follows (otherwise it is the conjunctive shalshelet
                            qetannah, swallowed -- matching the scanner)
  ``lp-legarmeih`` node   -> LEGARMEH when it follows a conjunctive word (azla /
                            mahapakh + paseq); promotes a preceding SHALSHELET to
                            SHALSHELET_GEDOLAH
  SOF PASUQ (U+05C3)      -> SILLUQ (the final word's meteg; verse end)

Every other mark a poetic word can carry contributes no disjunctive to this
skeleton: the conjunctive accents (servi) -- munax, merkha, mahapakh, azla,
illuy, tarxa, galgal, atnax-hafukh -- and the non-accent marks meteg
and narrow-sense paseq.  (Narrow-sense paseq -- paseq as distinct from
legarmeh -- is the residual ``lp-paseq`` node; the legarmeh-forming paseq is the
``lp-legarmeih`` node resolved above.)

The *servant* of a disjunctive -- the conjunctive sign on the word immediately
preceding it -- IS extractable, via ``servi_before_from_verse_node`` /
``load_servi_before``.  That is the second-witness oracle for vetting servant-
ADJACENCY rules (e.g. Breuer's "the servant next to [dexi] is [munax]"): MAM's servant
*choice* per slot is read in the scanner's own servus vocabulary and compared
word-for-word against the LC.  (The disjunctive cross-check above is silent on servi;
this fills that gap.  The munax/merkha *selection within* a slot is phonological and
still out of a token grammar's scope -- the oracle tells you what the LC and MAM actually
do, not why.)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_punctuation as hpunc
from mb_misc import osis_book_abbrevs as oba

from accgram import mam_simple_verse
from mb_cmn.silluq_before_meteg import validate_silluq_before_meteg
from accgram import poetic_accent_names as pan
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id

_SOF_PASUQ = "׃"

# Hebrew letter block (alef..tav, final forms included): the alignment key that
# lets a MAM chanted word be matched against its WLC counterpart with
# vowels/accents/punctuation stripped (see ``base_letters``).
_HEBREW_LETTER_LO = 0x05D0
_HEBREW_LETTER_HI = 0x05EA


def base_letters(word: str) -> str:
    """The bare letter skeleton of a Hebrew word (vowels/accents/punctuation dropped).

    Used as the alignment key when matching WLC and MAM chanted words: the same
    chanted word carries different points and accents on the two, so only the letters
    are a stable equality key.
    """
    return "".join(
        ch for ch in word if _HEBREW_LETTER_LO <= ord(ch) <= _HEBREW_LETTER_HI
    )


# One in-order traversal event:
# (kind, disjunctive_marker, servus, self_servus, text, chanted_word).
# A WORD carries a (provisional) disjunctive marker XOR a servus (its main accent is
# either a divider or a conjunctive), plus an optional self_servus: a conjunctive sign
# standing on the same chanted word before the disjunctive mark (a long chanted word can
# host its servus -- e.g. galgal then pazer), ``text`` = its base letters (the alignment
# key), and ``chanted_word`` = the marked Hebrew text. SOFPASUQ carries its text and
# chanted word; LP_LEG / LP_PASEQ carry none of the five values.
_Event = tuple[str, str | None, str | None, str | None, str | None, str | None]

# MAM Unicode accent -> intermediate disjunctive marker (REVIA / SHALSHELET stay
# provisional; resolved in the second pass).  Checked in this priority order so
# composite words resolve correctly (geresh muqdam + revia -> mugrash; ole +
# merkha -> oleh-weyored).
_DISJ_PRIORITY: list[tuple[str, str]] = [
    (ha.OLE, pan.OLEH_WEYORED),
    (ha.GER_M, pan.REVIA_MUGRASH),
    (ha.SHA, pan.SHALSHELET),  # provisional: gedolah only if a paseq node follows
    (ha.ATN, pan.ATNAX),
    (ha.DEX, pan.DEXI),
    (ha.Z_OR_TSOR, pan.TSINNOR),
    (ha.PAZ, pan.PAZER),
    (ha.REV, pan.REVIA),  # provisional: reclassified gadol/qatan/mugrash by position
]

# MAM Unicode conjunctive sign -> poetic servus token (poetic_accent_names, the same
# vocabulary the scanner emits), so servant choices compare apples-to-apples across
# the two witnesses.  The oleh-weyored servus is written atnax-hafukh (U+05A2) in MAM
# but coded galgal in the LC (see the disjunctive note above); it is normalized to GALGAL
# so the same structural slot matches.  Priority only disambiguates a word carrying
# more than one conjunctive mark (rare) -- the first match wins.
_SERVUS_SIGNS: list[tuple[str, str]] = [
    (ha.MUN, pan.MUNAX),
    (ha.MER, pan.MERKHA),
    (ha.MAH, pan.MAHAPAKH),
    (ha.QOM, pan.AZLA),  # qadma = azla (the conjunctive)
    (ha.YBY, pan.GALGAL),  # yerax-ben-yomo = galgal
    (
        ha.ATN_H,
        pan.GALGAL,
    ),  # atnax-hafukh: MAM's oleh-weyored servus (the LC has galgal)
    (ha.ILU, pan.ILLUY),
    (ha.TIP, pan.TARXA),  # U+0596 (tipexa in prose) is the poetic tarxa servant
]

# Node types whose subtree carries no cantillated text for our purposes, each standing
# between two atoms: each is a boundary in the fragment list ``_walk`` builds.
_DROP_TYPES = frozenset(
    {
        "good-ending",
        "spi-pe2",
        "spi-pe3",
        "spi-samekh2",
        "spi-samekh3",
        "spi-invnun",
    }
)
# MAM's gray maqaf.  This module reads it as a boundary between two atoms, so the two are two
# chanted words, as it read them in effect before it read whole runs (2026-10-20).
# ``mam_simple_verse`` reads the same node as a maqaf ending the atom before it, so the two are
# one chanted word, and MAM's introduction adds a gray maqaf where two atoms are fit to be
# joined by a maqaf.  Reading it that way here would change the chanted words of 109 more
# poetic verses (measured 2026-10-20), and, since ``_word_servus`` takes a chanted word's
# servus by a fixed priority rather than by position, it would name the wrong servant in
# compounds such as Psalms 117:2's כִּ֥י־גָ֘בַ֤ר, where the mahapakh stands next to the
# legarmeh but the merkha comes first in that priority.  Which reading this oracle takes is
# Ben's to decide.
_GRAY_MAQAF = "implicit-maqaf"
_KETIV_TYPES = frozenset({"ketiv", "kq-k", "kq-k-velo-q"})
_QERE_TYPES = frozenset({"qere", "kq-q", "kq-trivial", "kq-q-velo-k"})
_DIRECT_QERE_TYPES = _QERE_TYPES
_TEXT_TYPES = frozenset({"text", "letter-large", "letter-small", "letter-hung"})
_TRANSPARENT_TYPES = frozenset({"verse", "slh-word", "scrdfftar", "sdt-target"})

_POETIC_DISJUNCTIVES = pan.POETIC_DISJUNCTIVES

# Between an oleh and a yored in separate chanted words, MAM permits only letters,
# points, and meteg. Any other accent, a maqaf, or punctuation refuses the fusion.
_OLE_TO_YORED_CHANTED_WORD_RUN = (
    r"[\u05B0-\u05BC\u05BD\u05BF\u05C1-\u05C2\u05C4-\u05C5\u05C7\u05D0-\u05EA]*"
)
_CROSS_CHANTED_WORD_YORED = re.compile(
    ha.OLE
    + _OLE_TO_YORED_CHANTED_WORD_RUN
    + " "
    + _OLE_TO_YORED_CHANTED_WORD_RUN
    + ha.MER
)


def _word_marker(accents: str) -> str | None:
    """Resolve one word's combining accents to a provisional disjunctive marker."""
    return _word_marker_and_char(accents)[0]


def _word_marker_and_char(accents: str) -> tuple[str | None, str | None]:
    """Like ``_word_marker``, but also return the matching MAM accent char (for position).

    The char lets ``_word_self_servus`` locate the disjunctive mark within the word and
    look for a conjunctive standing before it.
    """
    for accent_char, marker in _DISJ_PRIORITY:
        if accent_char in accents:
            return marker, accent_char
    return None, None


def _word_self_servus(accents: str, marker_char: str) -> str | None:
    """The conjunctive servus on the SAME word, standing before the disjunctive mark.

    A long word can host its own servant: e.g. a yerax-ben-yomo (galgal) and a pazer on
    one word -- the galgal is pazer's adjacent servant, exactly as the scanner emits it
    as a token right before the pazer.  Returns the servus sign closest before the
    disjunctive mark, or None.  Order matters here (not mere membership): a conjunctive
    AFTER the disjunctive mark -- e.g. the yored merkha of an oleh-weyored -- is part of
    the divider, not a preceding servant, so it must not be picked up.
    """
    disj_idx = accents.find(marker_char)
    best_idx = -1
    best_name: str | None = None
    for sign, name in _SERVUS_SIGNS:
        idx = accents.rfind(
            sign, 0, disj_idx
        )  # closest occurrence before the disjunctive
        if idx > best_idx:
            best_idx = idx
            best_name = name
    return best_name


def _word_servus(accents: str) -> str | None:
    """Resolve a no-disjunctive word's combining accents to a poetic servus token, or None.

    Called only for a word with no divider (a divider word's own conjunctive is captured
    separately as its self_servus, via ``_word_self_servus``).
    """
    for sign, name in _SERVUS_SIGNS:
        if sign in accents:
            return name
    return None


def _emit_word_event(word: str, events: list[_Event]) -> None:
    """Append the event of one chanted word: an atom, or the atoms of a maqaf compound.

    The verse's last chanted word carries SOF PASUQ; its meteg is silluq, so it is
    emitted as a ('SOFPASUQ', None, None, None) sentinel the second pass turns into
    SILLUQ.  A chanted word's plain servus is recorded only when it carries no disjunctive
    marker; a disjunctive one instead records any conjunctive standing before
    its divider within the same chanted word as self_servus.
    """
    letters = base_letters(word)
    if _SOF_PASUQ in word:
        events.append(("SOFPASUQ", None, None, None, letters, word))
        return
    marker, marker_char = _word_marker_and_char(word)
    if marker is None:
        events.append(("WORD", None, _word_servus(word), None, letters, word))
        return
    # Oleh-weyored is a two-mark sign (ole + a yored merkha); MAM sometimes
    # encodes the yored merkha BEFORE the ole, so it would masquerade as a
    # same-word servant.  It is part of the divider, and oleh-weyored's true
    # servant always sits on the preceding word, so it has no self_servus.
    self_servus = (
        None if marker == pan.OLEH_WEYORED else _word_self_servus(word, marker_char)
    )
    events.append(("WORD", marker, None, self_servus, letters, word))


class _Boundary:
    """A node that stands between two atoms and contributes no text of its own.

    The counterpart of ``mam_simple_verse._Boundary``: a MAM-simple ``text`` run carries
    its own spaces, and a structural node standing between two runs is often the only thing
    between them, so dropping such a node outright would fuse the atoms either side.
    """

    def __repr__(self) -> str:  # pragma: no cover - debugging aid only
        return "<boundary>"


_BOUNDARY = _Boundary()


def _verse_events(verse_node: dict) -> list[_Event]:
    """The verse's WORD / LP_LEG / LP_PASEQ / SOFPASUQ events, in order.

    ``_walk`` gathers the verse as text fragments, boundaries and paseq events, and the
    text between two of the others is joined into one run before it is split into atoms.
    Splitting each node's text on its own, as this module did until 2026-10-20, splits an
    atom at every node inside it.  A ``letter-large``, ``letter-small`` or ``letter-hung``
    sits with the rest of its atom in an ``slh-word``, and Proverbs 28:17's אָ֭דָם, whose
    dalet is small, came out as three atoms.  A qere is spliced into the run around it, and
    each of the 49 poetic verses where nothing but a maqaf or the sof pasuq stands between a
    qere and the atom beside it lost that join: a verse-final qere left its sof pasuq an
    atom of its own, and the silluq with it.  ``mam_simple_verse._tokens_from_fragments``
    fixed the same defect in the MAM-simple loader under issue wlc-utils#91, and this is
    that idea.

    An atom is what ``mam_simple_verse._split_mam_simple_text`` makes of a run: the text
    between spaces, a maqaf ending its atom.  An atom ending in a maqaf joins the atom read
    after it into one chanted word (issue wlc-utils#81), as
    ``maqaf_nonfinal_accents._join_on_maqaf`` joins MAM-simple's atoms, even where a ketiv
    with no qere stands between the two; a paseq event cannot stand inside a compound, and
    raises if it does.
    """
    fragments: list[object] = []
    _walk(verse_node, fragments)
    events: list[_Event] = []
    pending = ""
    run: list[str] = []

    def take_atoms() -> None:
        nonlocal pending
        for atom in _run_atoms("".join(run)):
            pending += atom
            if not pending.endswith(hpunc.MAQ):
                _emit_word_event(pending, events)
                pending = ""
        run.clear()

    for fragment in fragments:
        if isinstance(fragment, str):
            run.append(fragment)
            continue
        take_atoms()
        if fragment is _BOUNDARY:
            continue
        if pending:
            raise ValueError(f"a paseq inside a maqaf compound, after {pending!r}")
        events.append(fragment)
    take_atoms()
    if pending:
        _emit_word_event(pending, events)
    return events


def _run_atoms(text: str) -> list[str]:
    """The atoms of one run: split at each space, a maqaf ending the atom it follows."""
    atoms: list[str] = []
    for spaced in text.split():
        pieces = spaced.split(hpunc.MAQ)
        atoms.extend(piece + hpunc.MAQ for piece in pieces[:-1])
        if pieces[-1]:
            atoms.append(pieces[-1])
    return atoms


def _walk(node: object, out: list[object]) -> None:
    """In-order DFS collecting text fragments, ``_BOUNDARY`` separators and paseq events.

    ``lp-legarmeih`` and ``lp-paseq`` are sibling structural nodes that sit between
    text runs; pre-order traversal preserves their position relative to the words, and
    ``_verse_events`` passes their LP_LEG / LP_PASEQ events through.  Ketiv halves of a
    qere/ketiv pair are skipped (the qere is what is read).  Each node type is the
    fragment ``mam_simple_verse._mam_simple_fragments`` makes of it, but for MAM's gray
    maqaf (``_GRAY_MAQAF``): a ketiv and the ``_DROP_TYPES`` stand between atoms; a
    ``kq-k-velo-q-maq`` and an ``sdt-note`` are nothing at all, as their atom is the one
    either side; and a qere is spliced into the run around it.
    """
    if not isinstance(node, dict):
        raise TypeError(f"Expected MAM-simple poetic node object, got {node!r}")
    node_type = node.get("type")
    if not isinstance(node_type, str):
        raise ValueError(f"MAM-simple poetic node has no string type: {node!r}")
    if node_type == "lp-legarmeih":
        out.append(("LP_LEG", None, None, None, None, None))
        return
    if node_type == "lp-paseq":
        out.append(("LP_PASEQ", None, None, None, None, None))
        return
    if node_type in _KETIV_TYPES:
        out.append(_BOUNDARY)
        return
    if node_type in {"kq-k-velo-q-maq", "sdt-note"}:
        return
    if node_type == _GRAY_MAQAF:
        out.append(_BOUNDARY)
        return
    if node_type in _DROP_TYPES:
        out.append(_BOUNDARY)
        return
    if node_type == "kq":
        _walk_kq(node, out)
        return
    if node_type == "cant-all-three":
        raise ValueError(
            "Poetic accent projection has no classified dual-cantillation branch"
        )

    contents = node.get("contents")
    if node_type in _TRANSPARENT_TYPES | _DIRECT_QERE_TYPES:
        if contents is None:
            text = node.get("text")
            if isinstance(text, str):
                out.append(text)
                return
            raise ValueError(
                f"MAM-simple poetic {node_type!r} node has neither text nor contents"
            )
        if not isinstance(contents, list):
            raise ValueError(f"MAM-simple poetic {node_type!r} contents is not a list")
        index = 0
        while index < len(contents):
            child = contents[index]
            if child.get("type") == "silluq-before-meteg":
                if set(child) != {"type", "text", "letters-with-silluq"}:
                    raise ValueError(f"Unexpected silluq-before-meteg node: {child!r}")
                validate_silluq_before_meteg(
                    child["text"], child["letters-with-silluq"]
                )
                following = contents[index + 1] if index + 1 < len(contents) else None
                if not (
                    isinstance(following, dict)
                    and set(following) == {"type", "text"}
                    and following["type"] == "text"
                    and isinstance(following["text"], str)
                    and following["text"].startswith(_SOF_PASUQ)
                ):
                    raise ValueError(
                        "silluq annotation lacks its following sof pasuq text"
                    )
                out.append(child["text"] + following["text"])
                index += 2
            else:
                _walk(child, out)
                index += 1
        return

    if node_type == "silluq-before-meteg":
        raise ValueError(
            "silluq annotation must be read with its following sof pasuq text"
        )
    if node_type in _TEXT_TYPES:
        text = node.get("text")
        if not isinstance(text, str):
            raise ValueError(f"MAM-simple poetic {node_type!r} node has no text")
        out.append(text)
        return

    raise ValueError(f"Unclassified MAM-simple poetic node type {node_type!r}")


def _walk_kq(node: dict, out: list[object]) -> None:
    """Walk a ketiv/qere node, reading only its qere half (the accented reading).

    No boundary either side, as ``mam_simple_verse._mam_simple_kq_qere_fragments`` has none:
    the runs around a qere carry their own spacing, and a verse-final qere is followed by a
    ``text`` run holding the sof pasuq alone, which belongs to the qere's last atom.
    """
    contents = node.get("contents")
    if not isinstance(contents, list):
        raise ValueError("MAM-simple poetic kq node has no contents list")

    qere_children = [
        child
        for child in contents
        if isinstance(child, dict) and child.get("type") in _QERE_TYPES
    ]
    if not qere_children:
        raise ValueError("MAM-simple poetic kq node has no recognized qere child")
    for child in qere_children:
        _walk(child, out)


def _first_chanted_word_supplies_yored(
    marker: str | None,
    chanted_word: str | None,
    following_servus: str | None,
    following_chanted_word: str | None,
) -> bool:
    """Whether the following chanted word's merkha is this oleh's yored."""
    return (
        marker == pan.OLEH_WEYORED
        and chanted_word is not None
        and ha.MER not in chanted_word
        and following_servus == pan.MERKHA
        and following_chanted_word is not None
        and _CROSS_CHANTED_WORD_YORED.search(f"{chanted_word} {following_chanted_word}")
        is not None
    )


def _build_word_accents(events: list[_Event]) -> list[list[str | None]]:
    """Reduce traversal events to a per-word ``[disjunctive, servus, self_servus, text]`` list.

    One entry per WORD (and the final SOFPASUQ word, which becomes SILLUQ).  LP_LEG /
    LP_PASEQ promote the preceding word (legarmeh, or shalshelet -> shalshelet
    gedolah); bare shalshelet (qetannah) is swallowed to a None disjunctive; generic
    REVIA is reclassified to gadol/qatan/mugrash by the next disjunctive-bearing word
    (the same rule as ``poetic_scanner._reclassify_revia``).  The servus,
    self_servus, and text (base-letter alignment key) columns are carried through
    untouched.
    """
    events = list(events)
    for index, event in enumerate(events[:-1]):
        kind, marker, _servus, _self_servus, _text, chanted_word = event
        following = events[index + 1]
        (
            following_kind,
            _following_marker,
            following_servus,
            _following_self_servus,
            _following_text,
            following_chanted_word,
        ) = following
        if kind != "WORD" or following_kind != "WORD":
            continue
        if _first_chanted_word_supplies_yored(
            marker, chanted_word, following_servus, following_chanted_word
        ):
            events[index + 1] = (
                following_kind,
                _following_marker,
                None,
                _following_self_servus,
                _following_text,
                following_chanted_word,
            )

    words: list[list[str | None]] = []
    last_word_index: int | None = None
    for kind, marker, servus, self_servus, text, _chanted_word in events:
        if kind == "WORD":
            words.append([marker, servus, self_servus, text])
            last_word_index = len(words) - 1
        elif kind == "SOFPASUQ":
            words.append([pan.SILLUQ, None, None, text])
            last_word_index = len(words) - 1
        elif kind == "LP_LEG":
            # Preceding word is legarmeh (conjunctive + paseq) or, if it carried
            # shalshelet, shalshelet gedolah.
            if last_word_index is None:
                continue
            prev = words[last_word_index][0]
            if prev == pan.SHALSHELET:
                words[last_word_index][0] = pan.SHALSHELET_GEDOLAH
            elif prev is None:
                words[last_word_index][0] = pan.LEGARMEH
            # else: an lp-legarmeih after a real disjunctive -- leave it alone.
        elif kind == "LP_PASEQ":
            # A narrow-sense paseq promotes a preceding shalshelet to gedolah, but does not
            # by itself create a legarmeh.
            if (
                last_word_index is not None
                and words[last_word_index][0] == pan.SHALSHELET
            ):
                words[last_word_index][0] = pan.SHALSHELET_GEDOLAH

    # Bare shalshelet (no paseq) is the conjunctive qetannah -> swallow its disjunctive.
    for word in words:
        if word[0] == pan.SHALSHELET:
            word[0] = None

    disj_positions = [i for i, w in enumerate(words) if w[0] is not None]
    for k, i in enumerate(disj_positions):
        if words[i][0] != pan.REVIA:
            continue
        nxt = words[disj_positions[k + 1]][0] if k + 1 < len(disj_positions) else None
        if nxt == pan.OLEH_WEYORED:
            words[i][0] = pan.REVIA_QATAN
        elif nxt == pan.SILLUQ:
            words[i][0] = pan.REVIA_MUGRASH
        else:
            words[i][0] = pan.REVIA_GADOL
    return words


def word_accents_from_verse_node(
    verse_node: dict,
) -> list[tuple[str | None, str | None, str | None]]:
    """Per-word ``(disjunctive, servus, self_servus)`` for a MAM-simple verse, in order.

    A divider word lists its disjunctive (and, if its own word also has a conjunctive
    before that divider, a self_servus); a conjunctive word lists its servus in the
    scanner's vocabulary; a word with neither (a non-final atom of a compound, or
    meteg-only) is
    ``(None, None, None)``.  At most one of ``disjunctive``/``servus`` is non-None.  The
    final word is ``(SILLUQ, None, None)``.
    """
    return [(w[0], w[1], w[2]) for w in _build_word_accents(_verse_events(verse_node))]


def disjunctives_from_verse_node(verse_node: dict) -> list[str]:
    """Return the ordered poetic disjunctive sequence for one MAM-simple verse."""
    return [
        d
        for d, _servus, _self in word_accents_from_verse_node(verse_node)
        if d is not None
    ]


def word_disj_and_text_from_verse_node(
    verse_node: dict,
) -> list[tuple[str, str | None]]:
    """Per-word ``(base_letters, disjunctive_or_None)`` for a MAM-simple verse, in order.

    The disjunctive is the fully resolved one (legarmeh / shalshelet gedolah / revia
    classified, as in ``word_accents_from_verse_node``); the letters are the word-
    alignment key (see ``base_letters``).  This is the per-word datum the poetic
    ungrammatical-verse report aligns against its WLC counterpart to describe divider differences
    word-for-word rather than over the conjunctive-stripped disjunctive skeleton.
    """
    return [(w[3] or "", w[0]) for w in _build_word_accents(_verse_events(verse_node))]


def servi_before_in_words(
    words: list[tuple[str | None, str | None, str | None]], target: str
) -> list[str | None]:
    """Servus before each ``target`` occurrence in per-word ``(disj, servus, self_servus)``.

    Factored out of ``servi_before_from_verse_node`` so a caller already holding a
    verse's word-accents (e.g. from ``load_word_accents``) need not re-walk it.  One
    entry per occurrence of ``target``, in order.  The adjacent servant is the target
    word's own ``self_servus`` when present (a same-word conjunctive standing before the
    divider, e.g. galgal before pazer -- matching how the scanner emits it as the token
    right before the disjunctive); otherwise the preceding word's servus, or ``None`` when
    there is none (verse-initial, or the preceding word is itself a divider -- a bare
    ``target``).
    """
    out: list[str | None] = []
    for i, (disj, _servus, self_servus) in enumerate(words):
        if disj != target:
            continue
        if self_servus is not None:
            out.append(self_servus)
        elif i == 0 or words[i - 1][0] is not None:
            out.append(None)  # verse-initial, or preceding word is itself a divider
        else:
            out.append(words[i - 1][1])
    return out


def servi_before_from_verse_node(verse_node: dict, target: str) -> list[str | None]:
    """Servus on the word immediately before each occurrence of ``target`` disjunctive.

    ``target`` is a poetic disjunctive token name (e.g. ``pan.DEXI``).  This is the MAM
    side of a servant-adjacency check; the LC side is the servus that stands right before
    the same ``target`` in ``poetic_scanner``'s token stream.
    """
    return servi_before_in_words(word_accents_from_verse_node(verse_node), target)


def _iter_verse_nodes(value: object):
    """Locate every verse in the complete MAM-simple book structure.

    This structural inventory does not flatten text or choose an alternative.
    """
    if isinstance(value, dict):
        if value.get("type") == "verse":
            yield value
            return
        contents = value.get("contents")
        if isinstance(contents, list):
            for child in contents:
                yield from _iter_verse_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_verse_nodes(child)


def _iter_book_verses(mam_simple_dir: Path, books: tuple[str, ...]):
    """Yield ``(ref, verse_node)`` for the poetic books, ``ref`` like ``"Psalms 1:1"``.

    Shared corpus walk for the ``load_*`` functions (reference strings match
    ``poetic_scanner``'s).
    """
    mam_simple_verse.require_mam_simple(mam_simple_dir)
    for bb in books:
        bk39id = wlc_bb_to_bk39id(bb)
        json_path = mam_simple_verse.mam_simple_json_path(mam_simple_dir, bk39id)
        prefix = oba.BOOK_ABBREVS[bk39id]
        with json_path.open("r", encoding="utf-8") as f_in:
            root = json.load(f_in)
        for verse_node in _iter_verse_nodes(root):
            osis_id = verse_node.get("osisID")
            if not isinstance(osis_id, str) or not osis_id.startswith(f"{prefix}."):
                continue
            parts = osis_id.split(".")
            if len(parts) != 3:
                continue
            yield f"{bk39id} {parts[1]}:{parts[2]}", verse_node


def load_poetic_disjunctives(
    mam_simple_dir: Path,
    books: tuple[str, ...] = ("ps", "pr", "jb"),
) -> dict[str, list[str]]:
    """Map ``"<book> <ch>:<vs>"`` -> MAM disjunctive sequence for the poetic books.

    The reference string matches ``poetic_scanner``'s (e.g. ``"Psalms 1:1"``).
    """
    return {
        ref: disjunctives_from_verse_node(vn)
        for ref, vn in _iter_book_verses(mam_simple_dir, books)
    }


def load_poetic_word_disj(
    mam_simple_dir: Path,
    books: tuple[str, ...] = ("ps", "pr", "jb"),
) -> dict[str, list[tuple[str, str | None]]]:
    """Map ``"<book> <ch>:<vs>"`` -> per-word ``(base_letters, disjunctive_or_None)``.

    The word-aligned counterpart of ``load_poetic_disjunctives``: it keeps every word
    (with its letter alignment key), not just the disjunctive-bearing ones, so the
    poetic ungrammatical summary can pair each WLC word against its MAM word.
    """
    return {
        ref: word_disj_and_text_from_verse_node(vn)
        for ref, vn in _iter_book_verses(mam_simple_dir, books)
    }


def load_word_accents(
    mam_simple_dir: Path,
    books: tuple[str, ...] = ("ps", "pr", "jb"),
) -> dict[str, list[tuple[str | None, str | None, str | None]]]:
    """Map ``"<book> <ch>:<vs>"`` -> per-word ``(disj, servus, self_servus)`` for the corpus.

    One corpus walk; ``servi_before_in_words(words, target)`` then derives the servant
    before any number of disjunctive targets without re-reading the JSON (what the
    ``servi-xcheck`` tool does to vet every Breuer adjacency rule in a single pass).
    """
    return {
        ref: word_accents_from_verse_node(vn)
        for ref, vn in _iter_book_verses(mam_simple_dir, books)
    }


def load_servi_before(
    mam_simple_dir: Path,
    target: str,
    books: tuple[str, ...] = ("ps", "pr", "jb"),
) -> dict[str, list[str | None]]:
    """Map ``"<book> <ch>:<vs>"`` -> the servus(es) MAM puts before ``target`` per verse.

    ``target`` is a poetic disjunctive token name (e.g. ``pan.DEXI``).  Each value is
    the list returned by ``servi_before_from_verse_node`` -- one servus token (or None
    = bare/verse-initial) per occurrence of ``target`` in that verse.  Verses with no
    ``target`` map to an empty list.  This is the second-witness oracle for vetting
    Breuer's servant-adjacency rules against MAM; compare to the LC servus that
    precedes the same ``target`` in ``poetic_scanner``'s token stream.
    """
    return {
        ref: servi_before_from_verse_node(vn, target)
        for ref, vn in _iter_book_verses(mam_simple_dir, books)
    }
