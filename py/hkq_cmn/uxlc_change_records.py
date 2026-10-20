"""Where each of Holman's cases turns up in the UXLC 2.6 change list.

The UXLC's editor publishes each release's change list as one long page; UXLC
2.6's, released on 2026-10-19, is at ``CHANGES_PAGE_URL``. It is a flat
chronological list rather than a per-book one, and a record's anchor is the date
it was entered plus its sequence number within that date -- ``#2026.08.05-6`` --
so nothing in an anchor says which verse the record is about. The mapping from a
case to its records is therefore written out here rather than derived.

Four things the table records that a derivation would have got wrong:

  * The change list numbers the atom differently from Holman in five cases.
    Holman's Lev 16:21.6 is the list's Lev 16:21.7, Joshua 5:1 word 36 is Josh
    5:1.37, Ezek 8:6.12 is Ezek 8:6.14, 2 Sam 24:10.19 is 2Sam 24:10.20, and
    1 Chr 27:21.7 is 1Chr 27:21.8. The word is the same one in each -- the same
    form is quoted and the same correction described.

    All five are the two numberings ``uxlc_standard_atoms`` sets out rather
    than a discrepancy. In the first three, the list numbers a ketiv and its qere separately
    and Holman numbers the pair once, so the list's number runs ahead of his by
    one for every element of a pair earlier in the verse. Ezek 8:6 is where it
    runs ahead by two, that verse's ketiv מהם having two qere atoms, מָ֣ה and
    הֵ֣ם. In 2 Sam 24:10 and 1 Chr 27:21, the list counts
    the samekh earlier in the verse as an atom, and Holman does not. The card
    shows the list's number on all five of them.

    The list proposed for UXLC 2.6 had a fourth, Lev 25:20, which ketiv/qere
    does not explain, that verse having no such pair. The two indexes were the
    two atoms of the maqaf compound מַה־נֹּאכַ֤֖ל: that list's 3 was מַה־ and
    Holman's 4 is נֹּאכַ֤֖ל, the atom whose mahapakh his case asks to remove.
    The installed list cites Lev 25:20.4, Holman's number. Change lists do this
    elsewhere too, quoting a maqaf compound whole and citing the atom it starts
    at. In the change files under ``uxlc/in/UXLC-misc/`` the
    instances are Gen 14:17.9, Ex 5:22.11 and 2Sam 3:30.10, whose records ask
    for a maqaf between the compound's two atoms, and 2Sam 6:7.1 and
    2Sam 8:1.2, whose descriptions begin "Remove maqaf, merging 2 words to 1".

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

  * The two Jeremiah cases have two records each. 2026.04.10-8 on Jer 10:3.11
    and 2026.04.10-9 on Jer 46:4.6 predate Holman's Jeremiah message; the first
    is Holman's and the second Ben Denckla's. Holman's second pass entered
    each correction again, as 2026.08.05-97 and 2026.08.05-100. All four are
    linked, as both of Judges 11:24.7's are.

Four cases have no record in this list: Ps 8:9.6, Ps 18:3.2, Job 10:6.4 and Job
32:6.6. That is what the list holds, not a judgement about them.

Sixteen of the list's records match no case here. Nine are Holman's:
2026.08.05-1 and -2, on Gen 26:7.21 and Gen 40:17.2, and 2026.08.05-120 to
-126, on seven verses of 1 and 2 Kings, books in which this repo has no case.
Seven are Ben Denckla's, 2026.04.10-1 to -6 and -10.

On 2026-10-20 the table was re-read against the installed list, matching each
case's atom in ``data/uxlc_standard_atoms.json`` with each record's citation.
Until then it lacked 96 of the cases that the installed list has records for,
among them six Samuel cases whose records, 2026.08.05-17 to -22, the proposed
list already had; and each of its four Exodus entries named the record of
another Exodus case.

The page is versioned by date, so a later one has a different URL. When it
appears, update ``CHANGES_PAGE_URL`` and re-read the ids: a case with no record
yet may have gained one, and a record can be renumbered, as the proposed list's
2026.07.24-1 became the installed list's 2026.08.05-102.
"""

from __future__ import annotations

from dataclasses import dataclass

CHANGES_PAGE_URL = (
    "https://hcanat.us/Changes/2026.10.19%20-%20Changes/2026.10.19%20-%20Changes.html"
)
CHANGES_PAGE_LABEL = "2026.10.19 - Changes"
CHANGES_PAGE_DESCRIPTION = "the change list for UXLC 2.6"

# Keyed as uxlc_email_extract.CaseRef.key spells a reference: bk39 book id,
# chapter:verse.atom, with the atom numbered as Holman numbers it rather than as
# the card shows it. Leviticus is Levit and Deuteronomy is Deuter there. The
# values are the change list's own ids, which is what its anchors are.
CHANGE_RECORD_IDS_BY_REF = {
    "Exodus 7:20.19": ("2026.08.05-3",),
    "Exodus 11:6.1": ("2026.08.05-4",),
    "Exodus 20:3.2": ("2026.08.05-5",),
    "Exodus 38:12.6": ("2026.08.05-6",),
    "Levit 7:25.6": ("2026.08.05-7",),
    "Levit 15:8.2": ("2026.08.05-8",),
    # The list files this one as Lev 16:21.7, counting the verse's ketiv and its
    # qere as two atoms where Holman counts them as one. See above.
    "Levit 16:21.6": ("2026.08.05-9",),
    # The proposed list filed this one as Lev 25:20.3, naming the atom the maqaf
    # compound מַה־נֹּאכַ֤֖ל starts at rather than the one Holman's case is
    # about. The installed list files it as Lev 25:20.4. See above.
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
    "1Samuel 7:10.10": ("2026.08.05-17",),
    "1Samuel 13:4.11": ("2026.08.05-18",),
    "1Samuel 28:12.11": ("2026.08.05-119",),
    "2Samuel 5:21.1": ("2026.08.05-19",),
    "2Samuel 7:22.7": ("2026.08.05-20",),
    "2Samuel 15:26.11": ("2026.08.05-21",),
    # The list files this one as 2Sam 24:10.20, counting the samekh earlier in
    # the verse as an atom where Holman does not count it. See above.
    "2Samuel 24:10.19": ("2026.08.05-22",),
    "Jeremiah 3:24.2": ("2026.08.05-95",),
    "Jeremiah 8:9.9": ("2026.08.05-96",),
    # Holman's, entered four months before Holman's Jeremiah message, then
    # entered again on Holman's second pass. See above.
    "Jeremiah 10:3.11": ("2026.04.10-8", "2026.08.05-97"),
    "Jeremiah 12:10.8": ("2026.08.05-98",),
    "Jeremiah 28:9.7": ("2026.08.05-99",),
    # Ben Denckla's, on the word Holman's Jer 46:4 case is about, then Holman's,
    # from Holman's second pass. See above.
    "Jeremiah 46:4.6": ("2026.04.10-9", "2026.08.05-100"),
    "Ezekiel 1:4.12": ("2026.08.05-101",),
    # The list files this one as Ezek 8:6.14, that verse's ketiv מהם having two
    # qere atoms, מָ֣ה and הֵ֣ם, which the list counts separately. See above.
    # The proposed list numbered the record 2026.07.24-1.
    "Ezekiel 8:6.12": ("2026.08.05-102",),
    "Ezekiel 8:15.9": ("2026.08.05-103",),
    "Ezekiel 11:1.29": ("2026.08.05-104",),
    "Ezekiel 16:12.1": ("2026.08.05-105",),
    "Ezekiel 23:11.8": ("2026.08.05-106",),
    "Ezekiel 32:21.9": ("2026.08.05-107",),
    "Ezekiel 33:28.9": ("2026.08.05-108",),
    "Ezekiel 36:3.18": ("2026.08.05-109",),
    "Ezekiel 44:6.14": ("2026.08.05-110",),
    "Hosea 5:6.3": ("2026.08.05-111",),
    "Amos 3:10.7": ("2026.08.05-112",),
    "Amos 8:12.8": ("2026.08.05-113",),
    "Obadiah 1:1.17": ("2026.08.05-114",),
    "Micah 1:14.10": ("2026.08.05-115",),
    "Zechariah 12:5.1": ("2026.08.05-116",),
    "Psalms 5:11.1": ("2026.08.05-44",),
    "Psalms 9:1.2": ("2026.08.05-45",),
    "Psalms 12:7.1": ("2026.08.05-46",),
    "Psalms 14:7.1": ("2026.08.05-47",),
    "Psalms 15:5.8": ("2026.08.05-48",),
    "Psalms 17:14.1": ("2026.08.05-49",),
    "Psalms 18:7.3": ("2026.08.05-50",),
    "Psalms 19:15.1": ("2026.08.05-51",),
    "Psalms 31:12.5": ("2026.08.05-52",),
    "Psalms 31:24.1": ("2026.08.05-53",),
    "Psalms 35:10.5": ("2026.08.05-54",),
    "Psalms 37:14.2": ("2026.08.05-55",),
    "Psalms 37:40.1": ("2026.08.05-56",),
    "Psalms 39:2.2": ("2026.08.05-57",),
    "Psalms 40:5.1": ("2026.08.05-58",),
    "Psalms 40:6.6": ("2026.08.05-59",),
    "Psalms 40:13.2": ("2026.08.05-60",),
    "Psalms 42:3.5": ("2026.08.05-61",),
    "Psalms 44:13.5": ("2026.08.05-62",),
    "Psalms 46:12.5": ("2026.08.05-63",),
    "Psalms 47:5.5": ("2026.08.05-64",),
    "Psalms 48:5.4": ("2026.08.05-65",),
    "Psalms 49:15.2": ("2026.08.05-66",),
    "Psalms 50:23.3": ("2026.08.05-67",),
    "Psalms 51:19.1": ("2026.08.05-68",),
    "Psalms 53:3.6": ("2026.08.05-69",),
    "Psalms 53:7.1": ("2026.08.05-70",),
    "Psalms 55:20.6": ("2026.08.05-71",),
    "Psalms 58:10.1": ("2026.08.05-72",),
    "Psalms 59:12.9": ("2026.08.05-73",),
    "Psalms 60:3.5": ("2026.08.05-74",),
    "Psalms 65:10.2": ("2026.08.05-75",),
    "Psalms 69:1.1": ("2026.08.05-76",),
    "Psalms 72:4.7": ("2026.08.05-77",),
    "Psalms 86:9.9": ("2026.08.05-78",),
    "Psalms 93:2.4": ("2026.08.05-79",),
    "Psalms 94:6.4": ("2026.08.05-80",),
    "Psalms 105:40.1": ("2026.08.05-81",),
    "Psalms 106:29.2": ("2026.08.05-82",),
    "Psalms 106:38.1": ("2026.08.05-83",),
    "Psalms 118:17.1": ("2026.08.05-84",),
    "Psalms 119:51.5": ("2026.08.05-85",),
    "Psalms 119:61.4": ("2026.08.05-86",),
    "Psalms 119:77.5": ("2026.08.05-87",),
    "Psalms 119:109.4": ("2026.08.05-88",),
    "Psalms 143:10.2": ("2026.08.05-89",),
    "Proverbs 8:13.1": ("2026.08.05-90",),
    "Proverbs 19:7.1": ("2026.08.05-91",),
    "Proverbs 23:7.2": ("2026.08.05-92",),
    "Proverbs 28:3.1": ("2026.08.05-93",),
    "Proverbs 30:15.1": ("2026.08.05-94",),
    "Job 11:6.3": ("2026.08.05-27",),
    "Job 15:35.3": ("2026.08.05-23",),
    "Job 17:3.5": ("2026.08.05-28",),
    "Job 29:25.1": ("2026.08.05-24",),
    "Job 30:1.2": ("2026.08.05-29",),
    "Job 32:12.1": ("2026.08.05-30",),
    "Job 34:20.4": ("2026.08.05-25",),
    "Job 39:28.4": ("2026.08.05-26",),
    "Esther 8:14.5": ("2026.08.05-130",),
    "Daniel 5:3.8": ("2026.08.05-117",),
    "Daniel 10:19.13": ("2026.08.05-118",),
    "Ezra 6:2.3": ("2026.08.05-127",),
    "Ezra 8:18.15": ("2026.08.05-128",),
    "Nehemiah 7:1.7": ("2026.08.05-129",),
    "1Chronicles 2:46.4": ("2026.08.05-31",),
    "1Chronicles 4:28.1": ("2026.08.05-32",),
    "1Chronicles 5:11.4": ("2026.08.05-33",),
    "1Chronicles 5:16.1": ("2026.08.05-34",),
    "1Chronicles 7:18.5": ("2026.08.05-35",),
    "1Chronicles 14:11.18": ("2026.08.05-36",),
    # The list files this one as 1Chr 27:21.8, counting the samekh earlier in
    # the verse as an atom where Holman does not count it. See above.
    "1Chronicles 27:21.7": ("2026.08.05-37",),
    "2Chronicles 1:10.6": ("2026.08.05-38",),
    "2Chronicles 13:12.13": ("2026.08.05-39",),
    "2Chronicles 16:2.5": ("2026.08.05-40",),
    "2Chronicles 21:19.7": ("2026.08.05-41",),
    "2Chronicles 31:9.4": ("2026.08.05-42",),
    "2Chronicles 33:21.2": ("2026.08.05-43",),
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
