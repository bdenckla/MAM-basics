"""Differential checks against independently assembled letter clusters."""

from itertools import product
import xml.etree.ElementTree as ET

import pytest

from mb_cmn.silluq_before_meteg import drop_post_silluq_metegs
from mb_cmn.silluq_before_meteg import validate_silluq_before_meteg
from mb_sefaria import mam4sef_handlers, mam4ajf_handlers
from osis import osis_handlers
from accgram import mam_simple_verse, mam_poetic_accents

_METEG = "\N{HEBREW POINT METEG}"
_VOWEL = "\N{HEBREW POINT PATAH}"
_LETTERS = "אבגדהו"
_SOF = "\N{HEBREW PUNCTUATION SOF PASUQ}"


def _cases():
    for marks in product((False, True), repeat=len(_LETTERS)):
        clusters = [
            letter + _VOWEL + (_METEG if marked else "")
            for letter, marked in zip(_LETTERS, marks)
        ]
        for position in range(len(_LETTERS)):
            scaffold = _LETTERS[: position + 1] + _METEG + _LETTERS[position + 1 :]
            valid = marks[position] and any(marks[position + 1 :])
            expected = "".join(
                cluster if i <= position else cluster.replace(_METEG, "")
                for i, cluster in enumerate(clusters)
            )
            yield "".join(clusters), scaffold, position, valid, expected


def test_cleanup_agrees_with_independent_cluster_oracle():
    checked = 0
    for text, scaffold, position, valid, expected in _cases():
        if valid:
            assert validate_silluq_before_meteg(text, scaffold) == position
            assert drop_post_silluq_metegs(text, scaffold) == expected
        else:
            with pytest.raises(ValueError):
                validate_silluq_before_meteg(text, scaffold)
        checked += 1
    assert checked > 0


def test_noteless_and_osis_projections_agree_with_cluster_oracle():
    checked = 0
    for text, scaffold, _position, valid, expected in _cases():
        if not valid:
            continue
        node = {
            "type": "silluq-before-meteg",
            "text": text,
            "letters-with-silluq": scaffold,
        }
        assert mam4sef_handlers.HANDLERS[(node["type"], None)](node, [], []) == [
            expected
        ]
        for handlers in mam4ajf_handlers.HANDLERS.values():
            assert handlers[(node["type"], None)](node, [], []) == [expected]
        element = ET.Element(
            node["type"], {key: value for key, value in node.items() if key != "type"}
        )
        body, note = osis_handlers.HANDLERS[(node["type"], None)](element, [], [])
        assert body == text
        assert note.attrib == {"type": "x-silluq-before-meteg"}
        checked += 1
    assert checked > 0


def test_annotation_boundaries_preserve_poetic_word_events():
    checked = 0
    for text, scaffold, _position, valid, _expected in _cases():
        if not valid:
            continue
        plain = {"type": "verse", "text": text + _SOF}
        annotated = {
            "type": "verse",
            "contents": [
                {
                    "type": "silluq-before-meteg",
                    "text": text,
                    "letters-with-silluq": scaffold,
                },
                {"type": "text", "text": _SOF},
            ],
        }
        baseline_events, annotated_events = [], []
        mam_poetic_accents._walk(plain, baseline_events)
        mam_poetic_accents._walk(annotated, annotated_events)
        assert annotated_events == baseline_events
        assert mam_simple_verse._normalize_mam_simple_verse(
            annotated
        ) == mam_simple_verse._normalize_mam_simple_verse(plain)
        checked += 1
    assert checked > 0
