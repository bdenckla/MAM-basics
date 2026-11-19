"""Graphical-object ownership must agree with the independent kq-u source roles."""

from itertools import product

import pytest

from accgram import uni_to_marks
from main_uxlc_grammar_test import joined_atoms, numbered_atoms, splice_atoms


def _source_cases():
    # The roles come from the structured source, independently of the flattened
    # body's separators, placeholders and maqaf joins.
    for ketiv_count, qere_count, preceding_maqaf in product(
        range(3), range(3), (False, True)
    ):
        ketiv = ["כתב", "אחר"][:ketiv_count]
        qere = ["קרא", "שני"][:qere_count]
        verse = {
            "vels": [
                "אב" + ("־" if preceding_maqaf else ""),
                {"kq": [ketiv, qere]},
                "גד",
            ]
        }
        roles = [False] + [True] * ketiv_count + [False] * (qere_count + 1)
        yield verse, roles


def test_numbered_roles_and_roundtrip_agree_with_structured_source():
    for verse, roles in _source_cases():
        body = uni_to_marks.verse_to_marks(verse)
        head, atoms = numbered_atoms(body)
        assert joined_atoms(head, atoms) == body
        assert [atom.in_ketiv for atom in atoms] == roles, (verse, atoms)


def test_splice_cross_role_guard_agrees_with_structured_source():
    for verse, roles in _source_cases():
        body = uni_to_marks.verse_to_marks(verse)
        head, original = numbered_atoms(body)
        for first in range(len(roles)):
            for last in range(first, len(roles)):
                atoms = list(original)
                if len(set(roles[first : last + 1])) > 1:
                    with pytest.raises(ValueError, match="spans a ketiv"):
                        splice_atoms(atoms, first, last, "X")
                    assert joined_atoms(head, atoms) == body
                else:
                    splice_atoms(atoms, first, last, "X")
                    assert len(atoms) == len(original)
