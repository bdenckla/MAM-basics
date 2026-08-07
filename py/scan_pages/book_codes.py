"""Filename book tokens -> bk39 ids.

FOUR OF THE FIVE EDITIONS WERE SCANNED USING THIS REPO'S OWN BOOK CODES, so there is
no bespoke table to write for them.  A token like ``G``, ``Js``, ``1S``, ``Ee`` is
exactly ``bib_locales.short(bk39id)``, and a section token like ``A1``, ``BA``,
``CK``, ``FD`` is exactly ``bib_locales.ordered_short(bk39id)``.  Inverting those two
functions is therefore the whole table, and it cannot drift from the convention the
rest of the repo uses because it *is* that convention, read backwards.

That the koren-family filenames carry both codes is a gift: ``A1-G-001.jpg`` names
Genesis twice, once per code, so a parser can insist the two agree and reject a
filename where they do not.  ``classify`` does insist.

Only bhl needs anything extra.  Its scanner mixed the short family with longforms
(``Isaiah``, ``Ruth``, ``Song``) and used further longforms on its title pages,
including names of book24s and of whole sections, which are not bk39s at all.
Those are the two tables at the bottom.
"""

from mb_cmn import bib_locales as tbn

# ``short`` and ``ordered_short`` are injective over the 39 books; the asserts below
# are what keeps that true if either table is ever edited.
SHORT_TO_BK39 = {tbn.short(bk39id): bk39id for bk39id in tbn.ALL_BK39_IDS}
ORDERED_SHORT_TO_BK39 = {
    tbn.ordered_short(bk39id): bk39id for bk39id in tbn.ALL_BK39_IDS
}
assert len(SHORT_TO_BK39) == len(tbn.ALL_BK39_IDS)
assert len(ORDERED_SHORT_TO_BK39) == len(tbn.ALL_BK39_IDS)

# bhl's longform book tokens, each naming one bk39.  ``Deut`` and ``Exod`` appear only
# on that edition's Decalogue pages; the rest appear on body or title pages.
LONGFORM_TO_BK39 = {
    "Deut": tbn.BK_DEUTER,
    "Exod": tbn.BK_EXODUS,
    "Isaiah": tbn.BK_ISAIAH,
    "Jeremiah": tbn.BK_JEREM,
    "Ezekiel": tbn.BK_EZEKIEL,
    "Daniel": tbn.BK_DANIEL,
    "Esther": tbn.BK_ESTHER,
    "Job": tbn.BK_JOB,
    "Proverbs": tbn.BK_PROV,
    "Psalms": tbn.BK_PSALMS,
    "Ruth": tbn.BK_RUTH,
    "Song": tbn.BK_SONG,
}

# bhl title-page tokens naming something larger than a bk39: a book24 or a section of
# the canon.  These get a section-title classification, never a bkid, precisely
# because "Kings" is not a book39 and pretending otherwise would put a rec on the
# wrong book.
LONGFORM_SECTIONS = (
    "Torah",
    "Prophets",
    "Writings",
    "Samuel",
    "Kings",
    "The-12",
    "Chron",
    "Er-Ne",
)


def bk39_of_token(token: str):
    """Return the bk39 a filename book token names, or None if it names no book."""
    if token in SHORT_TO_BK39:
        return SHORT_TO_BK39[token]
    return LONGFORM_TO_BK39.get(token)


def bk39_of_ordered_short(token: str):
    """Return the bk39 a section token such as ``A1`` or ``FD`` names, else None."""
    return ORDERED_SHORT_TO_BK39.get(token)
