"""Tests for the MAM-simple poetic disjunctive extractor (Phase 2 cross-check).

These pin the disjunctive sequence ``mam_poetic_accents`` extracts from a few
hand-built MAM-simple verse nodes, exercising the tricky encodings: oleh-we-yored
(ole + yored merkha), revia mugrash (geresh muqdam + revia), legarmeh vs shalshelet
gedolah (both ``lp-legarmeih`` paseq nodes, told apart by the preceding sign), the
generic-revia reclassification, and bare shalshelet (qetannah, swallowed).

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_mam_poetic_accents.py -v
"""

from mb_cmn import hebrew_accents as ha

from accgram import poetic_accent_names as pan
from accgram.mam_poetic_accents import (
    base_letters,
    disjunctives_from_verse_node,
    servi_before_from_verse_node,
    servi_before_in_words,
    word_accents_from_verse_node,
    word_disj_and_text_from_verse_node,
)

# Combining-accent helpers; the letter carrier is irrelevant to extraction.
B = "ב"  # an arbitrary base letter (bet)
SOF = "׃"


def _text(*accents: str) -> dict:
    return {"type": "text", "text": "".join(B + a for a in accents)}


def _verse(*nodes: dict) -> dict:
    return {"type": "verse", "osisID": "Ps.1.1", "contents": list(nodes)}


def test_oleh_weyored_and_atnax_and_silluq():
    # ole(+yored merkha) -> oleh-we-yored; etnaxta -> atnax; final word -> silluq.
    node = _verse(
        {"type": "text", "text": B + ha.OLE + B + ha.MER},  # one word: ole + yored
        {"type": "text", "text": B + ha.ATN},
        {"type": "text", "text": B + ha.MER + SOF},
    )
    assert disjunctives_from_verse_node(node) == [
        pan.OLEH_WEYORED,
        pan.ATNAX,
        pan.SILLUQ,
    ]


def test_revia_mugrash_geresh_muqdam():
    node = _verse(
        {"type": "text", "text": B + ha.GER_M + B + ha.REV},  # mugrash on one word
        {"type": "text", "text": B + ha.MER + SOF},
    )
    assert disjunctives_from_verse_node(node) == [pan.REVIA_MUGRASH, pan.SILLUQ]


def test_generic_revia_reclassified_gadol_before_atnax():
    node = _verse(
        _text(ha.REV),
        _text(ha.ATN),
        {"type": "text", "text": B + ha.MER + SOF},
    )
    assert disjunctives_from_verse_node(node) == [
        pan.REVIA_GADOL,
        pan.ATNAX,
        pan.SILLUQ,
    ]


def test_generic_revia_before_oleh_is_qatan():
    node = _verse(
        _text(ha.REV),
        {"type": "text", "text": B + ha.OLE + B + ha.MER},
        {"type": "text", "text": B + ha.ATN},
        {"type": "text", "text": B + ha.MER + SOF},
    )
    assert disjunctives_from_verse_node(node)[:2] == [pan.REVIA_QATAN, pan.OLEH_WEYORED]


def test_legarmeh_is_conjunctive_plus_paseq_node():
    # mahapakh word + lp-legarmeih paseq node -> legarmeh (not a bare conjunctive).
    node = _verse(
        _text(ha.MAH),
        {"type": "lp-legarmeih"},
        _text(ha.ATN),
        {"type": "text", "text": B + ha.MER + SOF},
    )
    assert disjunctives_from_verse_node(node) == [
        pan.LEGARMEH,
        pan.ATNAX,
        pan.SILLUQ,
    ]


def test_shalshelet_gedolah_vs_qetannah():
    # shalshelet + lp-legarmeih -> gedolah (disjunctive); bare shalshelet -> swallow.
    gedolah = _verse(
        _text(ha.SHA),
        {"type": "lp-legarmeih"},
        {"type": "text", "text": B + ha.MER + SOF},
    )
    assert disjunctives_from_verse_node(gedolah) == [pan.SHALSHELET_GEDOLAH, pan.SILLUQ]

    qetannah = _verse(
        _text(ha.SHA),  # no paseq node -> conjunctive, swallowed
        {"type": "text", "text": B + ha.MER + SOF},
    )
    assert disjunctives_from_verse_node(qetannah) == [pan.SILLUQ]


def test_ketiv_skipped_qere_read():
    # The qere half supplies the accent; the ketiv half is ignored.
    node = _verse(
        {
            "type": "kq",
            "contents": [
                {"type": "kq-k", "text": B + B},
                {"type": "kq-q", "text": B + ha.ATN},
            ],
        },
        {"type": "text", "text": B + ha.MER + SOF},
    )
    assert disjunctives_from_verse_node(node) == [pan.ATNAX, pan.SILLUQ]


# --- word-aligned per-word datum: base_letters / word_disj_and_text -----------


def test_base_letters_strips_points_accents_and_punctuation():
    # Only the Hebrew letters survive -- the alignment key the ungrammatical-verse report uses to
    # pair a MAM word with its WLC counterpart despite differing points/accents.
    assert base_letters(B + ha.OLE + B + ha.MER) == "בב"
    assert base_letters(B + ha.ATN + SOF) == "ב"


def test_word_disj_and_text_pairs_letters_with_resolved_divider():
    # mahapakh word + lp-legarmeih -> legarmeh on that word; atnax; silluq.  Every word is
    # kept (not just divider-bearing ones), its base letters paired with its fully
    # resolved disjunctive (None for a conjunctive) -- the datum word-aligned vs WLC.
    node = _verse(
        _text(ha.MER),  # a bare conjunctive word: kept, with disj None
        _text(ha.MAH),
        {"type": "lp-legarmeih"},
        _text(ha.ATN),
        _silluq_word(),
    )
    assert word_disj_and_text_from_verse_node(node) == [
        ("ב", None),
        ("ב", pan.LEGARMEH),
        ("ב", pan.ATNAX),
        ("ב", pan.SILLUQ),
    ]


# --- servant (conjunctive) extraction: servi_before / word_accents ---------------


def _silluq_word() -> dict:
    return {"type": "text", "text": B + ha.MER + SOF}


def test_word_accents_pairs_disjunctive_and_servus():
    # merkha(servus) | dexi(divider) | silluq -- exactly one of disj/servus per word, and
    # no same-word servant here, so self_servus is None throughout.
    node = _verse(_text(ha.MER), _text(ha.DEX), _silluq_word())
    assert word_accents_from_verse_node(node) == [
        (None, pan.MERKHA, None),
        (pan.DEXI, None, None),
        (pan.SILLUQ, None, None),
    ]


def test_word_accents_captures_same_word_galgal_before_pazer():
    # A long word can host its own servant: galgal (yerax-ben-yomo) then pazer on one
    # word (e.g. Ps 32:5 אוֹדִ֪יעֲךָ֡).  The galgal is recorded as the pazer word's
    # self_servus, not lost -- and it is what stands adjacent to the pazer.
    node = _verse(
        _text(ha.MUN), {"type": "text", "text": B + ha.YBY + B + ha.PAZ}, _silluq_word()
    )
    assert word_accents_from_verse_node(node) == [
        (None, pan.MUNAX, None),
        (pan.PAZER, None, pan.GALGAL),
        (pan.SILLUQ, None, None),
    ]
    # The same-word galgal wins over the preceding munax word.
    assert servi_before_from_verse_node(node, pan.PAZER) == [pan.GALGAL]


def test_servi_before_dexi_merkha_and_munax():
    # The servant immediately before dexi is read in the L scanner's vocabulary.
    merkha = _verse(_text(ha.MER), _text(ha.DEX), _silluq_word())
    assert servi_before_from_verse_node(merkha, pan.DEXI) == [pan.MERKHA]

    munax = _verse(_text(ha.MUN), _text(ha.DEX), _silluq_word())
    assert servi_before_from_verse_node(munax, pan.DEXI) == [pan.MUNAX]


def test_servi_before_is_none_when_target_is_bare():
    # Verse-initial dexi (no preceding word) and dexi preceded by a divider both
    # count as servant-less -> None.
    initial = _verse(_text(ha.DEX), _text(ha.MUN), _silluq_word())
    assert servi_before_from_verse_node(initial, pan.DEXI) == [None]

    after_divider = _verse(_text(ha.ATN), _text(ha.DEX), _silluq_word())
    assert servi_before_from_verse_node(after_divider, pan.DEXI) == [None]


def test_servi_before_in_words_operates_on_a_word_list():
    # The factored helper (used by servi-xcheck over load_word_accents) reads a
    # prebuilt (disjunctive, servus) list without re-walking a node.
    words = [
        (None, pan.MAHAPAKH, None),  # distant servant
        (None, pan.MERKHA, None),  # adjacent servant
        (pan.REVIA_QATAN, None, None),
        (pan.OLEH_WEYORED, None, None),  # a divider: the dexi-less target is bare here
        (None, pan.MUNAX, None),
        (pan.DEXI, None, None),  # munax-served dexi
        (pan.SILLUQ, None, None),
    ]
    assert servi_before_in_words(words, pan.REVIA_QATAN) == [pan.MERKHA]
    assert servi_before_in_words(words, pan.DEXI) == [pan.MUNAX]
    assert servi_before_in_words(words, pan.OLEH_WEYORED) == [
        None
    ]  # preceded by a divider


def test_servi_before_in_words_prefers_same_word_self_servus():
    # When the target word carries its own preceding conjunctive (self_servus), that wins
    # over the previous word's servus -- the same-word servant is the adjacent one.
    words = [
        (None, pan.MUNAX, None),
        (pan.PAZER, None, pan.GALGAL),  # galgal on the pazer's own word
        (pan.SILLUQ, None, None),
    ]
    assert servi_before_in_words(words, pan.PAZER) == [pan.GALGAL]


def test_servi_before_normalizes_atnax_hafukh_to_galgal():
    # MAM has the oleh-we-yored servus as atnax-hafukh (U+05A2); L has it as galgal.
    # The extractor normalizes it so the same slot matches across witnesses.
    node = _verse(
        _text(ha.ATN_H),
        {"type": "text", "text": B + ha.OLE + B + ha.MER},  # oleh-we-yored word
        _text(ha.ATN),
        _silluq_word(),
    )
    assert servi_before_from_verse_node(node, pan.OLEH_WEYORED) == [pan.GALGAL]
