"""What a scanned page is, as recorded for every file in every edition.

The vocabulary is chosen so that one question -- "can a bcv lookup land here?" --
is answered by the kind alone.  Exactly two kinds carry text a lookup may return:
BODY and DECALOGUE.  BODY_UNASSIGNED is text a lookup will be able to return once a
later phase says which segment each page belongs to.  Everything else is out.
"""

BODY = "body"  # biblical text in the edition's main run; bkids set
BODY_UNASSIGNED = "body-unassigned"  # biblical text, segment not yet determined
DECALOGUE = "decalogue"  # a Decalogue printed outside the main run; strands set
BOOK_TITLE = "book-title"  # a title page for one book; bkids set
SECTION_TITLE = "section-title"  # a title page for a section or a book24
TOC = "toc"
FRONT_MATTER = "front-matter"
BACK_MATTER = "back-matter"
COVER = "cover"
BLANK = "blank"
APPARATUS = "apparatus"  # study material that is not a running biblical text
UNPOINTED = "unpointed"  # biblical text without pointing -- out of lookup (Ben)

ALL_KINDS = (
    BODY,
    BODY_UNASSIGNED,
    DECALOGUE,
    BOOK_TITLE,
    SECTION_TITLE,
    TOC,
    FRONT_MATTER,
    BACK_MATTER,
    COVER,
    BLANK,
    APPARATUS,
    UNPOINTED,
)

# The kinds a censused page record may sit on.  BODY_UNASSIGNED is excluded: a rec
# needs to know which book it is in, and that is exactly what "unassigned" denies.
RECORDABLE_KINDS = (BODY, DECALOGUE)

# Strand ids.  Prose names these in Hebrew letters (עליון, תחתון); data and code use
# these ASCII ids, as the accgram code in this repo already does.
ELYON = "elyon"
TAXTON = "taxton"
ALL_STRANDS = (ELYON, TAXTON)


def page(file_name, kind, bkids=(), strands=(), note=None):
    """Return one classified page, as it is stored in an edition's index JSON.

    Null-valued fields are omitted rather than stored as nulls: the file is read by
    people as well as by programs, and 5,720 pages carrying four ``null``s each would
    bury the fields that do say something.
    """
    assert kind in ALL_KINDS, f"unknown page kind {kind!r}"
    assert all(strand in ALL_STRANDS for strand in strands), strands
    out = {"file": file_name, "kind": kind}
    if bkids:
        out["bkids"] = list(bkids)
    if strands:
        out["strands"] = list(strands)
    if note:
        out["note"] = note
    return out
