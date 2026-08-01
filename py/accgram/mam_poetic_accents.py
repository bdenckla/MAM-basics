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
from pathlib import Path

from mb_cmn import hebrew_accents as ha
from mb_misc import osis_book_abbrevs as oba

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


# One in-order traversal event: (kind, disjunctive_marker, servus, self_servus, text).
# A WORD carries a (provisional) disjunctive marker XOR a servus (its main accent is
# either a divider or a conjunctive), plus an optional self_servus: a conjunctive sign
# standing on the SAME word, before the disjunctive mark (a long word can host its own
# servant -- e.g. galgal then pazer on one word), and ``text`` = its base letters
# (the word-alignment key).  SOFPASUQ carries only its text; LP_LEG / LP_PASEQ carry
# none of the four.
_Event = tuple[str, str | None, str | None, str | None, str | None]

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

# Node types whose subtree carries no cantillated text for our purposes.
_DROP_TYPES = frozenset(
    {
        "good-ending",
        "spi-pe2",
        "spi-pe3",
        "spi-samekh2",
        "spi-samekh3",
        "spi-invnun",
        "implicit-maqaf",
    }
)
_KETIV_TYPES = frozenset({"ketiv", "kq-k", "kq-k-velo-q"})
_QERE_TYPES = frozenset({"qere", "kq-q", "kq-trivial", "kq-q-velo-k"})
_KQ_TYPES = frozenset({"kq", "kq-trivial", "kq-q-velo-k"})

_POETIC_DISJUNCTIVES = pan.POETIC_DISJUNCTIVES


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


def _emit_word_events(text: str, events: list[_Event]) -> None:
    """Append a ('WORD', marker, servus, self_servus) event per whitespace-delimited word.

    Whitespace-delimited means CHANTED word: a maqaf compound has no space in it, so it
    comes through whole (issue #81).

    The verse's last chanted word carries SOF PASUQ; its meteg is silluq, so it is
    emitted as a ('SOFPASUQ', None, None, None) sentinel the second pass turns into
    SILLUQ.  A chanted word's plain servus is recorded only when it carries no disjunctive
    marker; a disjunctive one instead records any conjunctive standing before
    its divider within the same chanted word as self_servus.
    """
    for word in text.split():
        letters = base_letters(word)
        if _SOF_PASUQ in word:
            events.append(("SOFPASUQ", None, None, None, letters))
            continue
        marker, marker_char = _word_marker_and_char(word)
        if marker is None:
            events.append(("WORD", None, _word_servus(word), None, letters))
        else:
            # Oleh-weyored is a two-mark sign (ole + a yored merkha); MAM sometimes
            # encodes the yored merkha BEFORE the ole, so it would masquerade as a
            # same-word servant.  It is part of the divider, and oleh-weyored's true
            # servant always sits on the preceding word, so it has no self_servus.
            self_servus = (
                None
                if marker == pan.OLEH_WEYORED
                else _word_self_servus(word, marker_char)
            )
            events.append(("WORD", marker, None, self_servus, letters))


def _walk(node: object, events: list[_Event]) -> None:
    """In-order DFS collecting WORD / LP_LEG / LP_PASEQ / SOFPASUQ events.

    ``lp-legarmeih`` and ``lp-paseq`` are sibling structural nodes that sit between
    text runs; pre-order traversal preserves their position relative to the words.
    Ketiv halves of a qere/ketiv pair are skipped (the qere is what is read).
    """
    if not isinstance(node, dict):
        return
    node_type = node.get("type")
    if isinstance(node_type, str):
        if node_type == "lp-legarmeih":
            events.append(("LP_LEG", None, None, None, None))
            return
        if node_type == "lp-paseq":
            events.append(("LP_PASEQ", None, None, None, None))
            return
        if node_type in _KETIV_TYPES:
            return
        if node_type in _DROP_TYPES:
            return
        if node_type in _KQ_TYPES:
            _walk_kq(node, events)
            return

    contents = node.get("contents")
    if isinstance(contents, list):
        for child in contents:
            _walk(child, events)
        return

    text = node.get("text")
    if isinstance(text, str):
        _emit_word_events(text, events)


def _walk_kq(node: dict, events: list[_Event]) -> None:
    """Walk a ketiv/qere node, reading only its qere half (the accented reading)."""
    contents = node.get("contents")
    if not isinstance(contents, list):
        text = node.get("text")
        if isinstance(text, str):
            _emit_word_events(text, events)
        return

    qere_children = [
        child
        for child in contents
        if isinstance(child, dict) and child.get("type") in _QERE_TYPES
    ]
    chosen = (
        qere_children
        if qere_children
        else [
            child
            for child in contents
            if not (isinstance(child, dict) and child.get("type") in _KETIV_TYPES)
        ]
    )
    for child in chosen:
        _walk(child, events)


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
    words: list[list[str | None]] = []
    last_word_index: int | None = None
    for kind, marker, servus, self_servus, text in events:
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
    events: list[_Event] = []
    _walk(verse_node, events)
    return [(w[0], w[1], w[2]) for w in _build_word_accents(events)]


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
    events: list[_Event] = []
    _walk(verse_node, events)
    return [(w[3] or "", w[0]) for w in _build_word_accents(events)]


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


def _mam_json_path(mam_simple_dir: Path, bk39id: str) -> Path | None:
    prefix = oba.BOOK_ABBREVS.get(bk39id)
    if prefix is None:
        return None
    candidate = mam_simple_dir / f"{prefix}.json"
    return candidate if candidate.is_file() else None


def _iter_verse_nodes(value: object):
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
    if not mam_simple_dir.is_dir():
        raise FileNotFoundError(f"MAM-simple directory not found: {mam_simple_dir}")
    for bb in books:
        bk39id = wlc_bb_to_bk39id(bb)
        json_path = _mam_json_path(mam_simple_dir, bk39id)
        if json_path is None:
            continue
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
