"""Where each of Holman's cases turns up in the UXLC's proposed-changes list.

The UXLC's editor publishes the changes proposed for the next release as one
long page, at ``CHANGES_PAGE_URL``. It is a flat chronological list rather than
a per-book one, and a record's anchor is the date it was entered plus its
sequence number within that date -- ``#2026.08.05-6`` -- so nothing in an anchor
says which verse the record is about. The mapping from a case to its records is
therefore written out here rather than derived.

Four things the table records that a derivation would have got wrong:

  * The change list numbers the atom differently from Holman in four cases.
    His Lev 16:21.6 is the list's Lev 16:21.7, his Lev 25:20.4 is its Lev
    25:20.3, his Joshua 5:1 word 36 is its Josh 5:1.37, and his Ezek 8:6.12 is
    its Ezek 8:6.14. The word is the same one in each -- the same form is quoted
    and the same correction described.

    Three of the four are the two numberings ``uxlc_standard_atoms`` sets out
    rather than a discrepancy: the list numbers a ketiv and its qere separately
    and Holman numbers the pair once, so the list's number runs ahead of his by
    one for every element of a pair earlier in the verse. Ezek 8:6 is where it
    runs ahead by two, that verse's ketiv מהם having two qere atoms, מָ֣ה and
    הֵ֣ם. The card shows the list's number on all three of them.

    Lev 25:20 is the one that ketiv/qere does not explain, that verse having no
    such pair, and the card shows Holman's 4 there. The two indexes are the two
    atoms of the maqaf compound מַה־נֹּאכַ֤֖ל: the list's 3 is מַה־ and Holman's
    4 is נֹּאכַ֤֖ל, the atom whose mahapakh his case asks to remove. The change
    list does this elsewhere too, quoting a maqaf compound whole and citing the
    atom it starts at -- Gen 14:17.9, Ex 5:22.11 and 2Sam 3:30.10 are the
    instances in the change files on disk in the sibling UXLC-utils.

    The keys below are Holman's, because a key is how a case in ``emails/`` is
    named, and ``data/uxlc_standard_atoms.json`` is keyed the same way.

  * Judges 11:24.7 has two records, by two authors. 2026.04.10-7 is Ben
    Denckla's, entered four months before Holman's message, asking about the
    same indistinct mark under the same tav. 2026.08.05-16 is Holman's own, and
    its note says outright that it "follows on Ben Denckla's change of
    2026.04.10 - 7". Both are linked because both are the change list's records
    for that word, which is what a reader of the card wants.

  * Joshua 20:4 has one record, not two. Holman's case asks for the merkha and
    the meteg of זִקְנֵי־הָעִיר to change places, and the list entered only the
    first half, 2026.08.05-15 on זִקְנֵי־, marked "NoAction". Until 2026-08-12
    this module also claimed 2026.08.05-16 for that case, on the reading that
    the list had split it into one record per word; that id is Judges 11:24.7's,
    as the paragraph above says.

  * Two of the Jeremiah records predate Holman's Jeremiah message and one of
    them is not his: 2026.04.10-8 on Jer 10:3.11 is Holman's own, and
    2026.04.10-9 on Jer 46:4.6 is Ben Denckla's. Both are the change list's
    record for the word the case is about.

The six Samuel cases have no record in this list, nor do the Psalms, Proverbs,
Chronicles, Ezra, Nehemiah, Esther and Minor Prophets cases, nor Job 10:6.4 and
Job 32:6.6. That is what the list holds, not a judgement about them.

Two of the list's own records match no case here: 2026.08.05-1 and -2, on Gen
26:7.21 and Gen 40:17.2, are Holman's but belong to a Genesis message this repo
does not have.

The page is versioned by date, so a later one has a different URL. When it
appears, update ``CHANGES_PAGE_URL`` and re-read the ids: a record already
entered keeps its date-and-sequence id, but a case with no record yet may have
gained one.
"""

from __future__ import annotations

from dataclasses import dataclass

CHANGES_PAGE_URL = (
    "https://hcanat.us/Changes/2026.10.19%20-%20Changes/2026.10.19%20-%20Changes.html"
)
CHANGES_PAGE_LABEL = "2026.10.19 - Changes"
CHANGES_PAGE_DESCRIPTION = "the changes proposed for UXLC 2.6"

# Keyed as uxlc_email_extract.CaseRef.key spells a reference: bk39 book id,
# chapter:verse.atom, with the atom numbered as Holman numbers it rather than as
# the card shows it. Leviticus is Levit and Deuteronomy is Deuter there. The
# values are the change list's own ids, which is what its anchors are.
CHANGE_RECORD_IDS_BY_REF = {
    "Exodus 7:20.19": ("2026.08.05-6",),
    "Exodus 11:6.1": ("2026.08.05-3",),
    "Exodus 20:3.2": ("2026.08.05-4",),
    "Exodus 38:12.6": ("2026.08.05-5",),
    "Levit 7:25.6": ("2026.08.05-7",),
    "Levit 15:8.2": ("2026.08.05-8",),
    # The list files this one as Lev 16:21.7, counting the verse's ketiv and its
    # qere as two atoms where Holman counts them as one. See above.
    "Levit 16:21.6": ("2026.08.05-9",),
    # The list files this one as Lev 25:20.3, naming the atom the maqaf compound
    # מַה־נֹּאכַ֤֖ל starts at rather than the one Holman's case is about. See above.
    "Levit 25:20.4": ("2026.08.05-10",),
    "Deuter 33:28.13": ("2026.08.05-11",),
    # The list files this one as Josh 5:1.37, counting the verse's ketiv and its
    # qere as two atoms where Holman counts them as one. See above.
    "Joshua 5:1.36": ("2026.08.05-12",),
    "Joshua 9:23.10": ("2026.08.05-13",),
    "Joshua 19:8.8": ("2026.08.05-14",),
    # Only the merkha under the nun of זִקְנֵי־ was entered, not the meteg under
    # the ayin of הָעִיר that Holman's case asks to exchange it with.
    "Joshua 20:4.12": ("2026.08.05-15",),
    # Ben Denckla's, then Holman's own following on from it. See above.
    "Judges 11:24.7": ("2026.04.10-7", "2026.08.05-16"),
    # Holman's own, entered four months before his Jeremiah message.
    "Jeremiah 10:3.11": ("2026.04.10-8",),
    # Ben Denckla's, on the word Holman's Jer 46:4 case is about.
    "Jeremiah 46:4.6": ("2026.04.10-9",),
    # The list files this one as Ezek 8:6.14, that verse's ketiv מהם having two
    # qere atoms, מָ֣ה and הֵ֣ם, which the list counts separately. See above.
    "Ezekiel 8:6.12": ("2026.07.24-1",),
    "Job 11:6.3": ("2026.08.05-27",),
    "Job 15:35.3": ("2026.08.05-23",),
    "Job 17:3.5": ("2026.08.05-28",),
    "Job 29:25.1": ("2026.08.05-24",),
    "Job 30:1.2": ("2026.08.05-29",),
    "Job 32:12.1": ("2026.08.05-30",),
    "Job 34:20.4": ("2026.08.05-25",),
    "Job 39:28.4": ("2026.08.05-26",),
}


@dataclass(frozen=True)
class ChangeRecordLink:
    record_id: str
    href: str
    title: str


def change_record_links(ref_key: str) -> tuple[ChangeRecordLink, ...]:
    """The change list's records for one case, in the order it lists them."""
    return tuple(
        ChangeRecordLink(
            record_id=record_id,
            href=f"{CHANGES_PAGE_URL}#{record_id}",
            title=(
                f"Change item {record_id} in {CHANGES_PAGE_LABEL}, "
                f"{CHANGES_PAGE_DESCRIPTION}"
            ),
        )
        for record_id in CHANGE_RECORD_IDS_BY_REF.get(ref_key, ())
    )


def require_known_refs(ref_keys: list[str]) -> None:
    """Raise on a table entry naming no case, so a mistyped key is loud.

    There is no check the other way: a case with no entry is the ordinary state
    of one the change list has not reached.
    """
    unmatched = sorted(set(CHANGE_RECORD_IDS_BY_REF) - set(ref_keys))
    if unmatched:
        raise ValueError(
            "CHANGE_RECORD_IDS_BY_REF names cases that no email contains: "
            f"{unmatched}"
        )
