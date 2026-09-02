"""The atom index for a case whose message states none.

Every other kind of drift between Holman's messages is absorbed by reading what
the message says: a new label spelling, a heading that carries the word, a
citation split over two lines. This table is for the one thing that cannot be,
an atom index the message never states. ``CaseRef`` requires one, because the
reference it spells is the key everything else is filed under -- the tables in
``uxlc_change_records``, ``uxlc_holman_forms``, ``uxlc_attachment_notes`` and
``uxlc_comments``, and ``data/uxlc_atom_locations.json`` and
``data/uxlc_standard_atoms.json`` besides.

The index is Holman's numbering, which is what ``CaseRef.atom`` holds
everywhere: it counts a ketiv/qere pair once and does not count a mid-verse
samekh, and agrees with the UXLC's count of the verse's child elements on every
verse that has neither before the atom. ``uxlc_standard_atoms`` sets out the
three numberings and the evidence for each.

Keyed by the message and the verse rather than by ``CaseRef.key``, because the
key cannot be spelled until the atom is known. A message may not raise the same
verse twice -- ``_require_distinct_refs`` would reject that -- so the message
and the verse name one case between them.

Two guards, because an entry can go stale in two directions.
``require_known_cases`` raises on an entry naming no case at all, so an email
key that changes spelling is loud rather than silently inert -- the same guard
``uxlc_attachment_notes.require_known_attachments`` gives its two tables.
``_build_case`` raises on an entry for a case whose message states an index of
its own, which is what a re-sent message with the index added would produce.
"""

from __future__ import annotations

# (email key, bk39 id, chapter, verse) -> Holman's atom index.
#
# Holman's 1 Samuel 28:12 message of 2026-08-23 is a single case headed with the
# message's own subject line, which names the verse and stops there; no field of
# it carries an index either. The UXLC's 1 Samuel 28:12 has sixteen child
# elements and no ketiv, qere or samekh among them, so its count and Holman's
# are the same count, and the eleventh is שָׁא֧וּל -- the atom his Change line
# alters, אֶל־ before it being the tenth. He quotes the maqaf compound whole and
# indexes the atom that carries the change, which is what his 2 Samuel 5:21.1
# (וַיַּעַזְבוּ־שָׁ֖ם, indexing the atom the maqaf sits on) and his 2 Samuel
# 7:22.7 (כִּֽי־אֵֽין, indexing the second atom) both do.
ATOM_INDEX_BY_VERSE_CASE = {
    ("uxlc-correction-for-1samuel-28-12", "1Samuel", 28, 12): 11,
}


def atom_index_for_verse_case(
    email_key: str, book: str, chapter: int, verse: int
) -> int | None:
    """Holman's atom index for a case whose message states none, or None."""
    return ATOM_INDEX_BY_VERSE_CASE.get((email_key, book, chapter, verse))


def require_known_cases(case_keys: set[tuple[str, str, int, int]]) -> None:
    """Raise on a table entry naming no case, so a stale key cannot sit inert."""
    unmatched = sorted(set(ATOM_INDEX_BY_VERSE_CASE) - case_keys)
    if unmatched:
        raise ValueError(
            "ATOM_INDEX_BY_VERSE_CASE names cases that no email contains: "
            f"{unmatched}"
        )
