"""MAM-morphhb's English notes on where BHS's numbering differs from MAM's own.

Exports variant_notes and PLACEHOLDER.

Like the 2014 file's four ``type="variant"`` notes, one note stands at the first verse
of each difference; MAM-morphhb has eight because it uses BHS's numbering throughout,
where the 2014 file mixed the two.  The wording follows
gh-pages/MAM-simple/versification-differences.html.  variant_notes checks every
claim against MAM-simple's contents-corresponds-to and osisID-of-MAM-src fields, so a
change to MAM-simple's renumbering raises here rather than leaving a stale note.
"""

FULL = "a full verse in MAM"
PART = "less than a full verse in MAM"
PLACEHOLDER = "no verse in MAM"


def _shift(book, chnu, first, last, by):
    """BHS verses first..last of a chapter, each `by` higher than MAM's."""
    return {
        f"{book}.{chnu}.{v}": (FULL, f"{book}.{chnu}.{v - by}")
        for v in range(first, last + 1)
    }


def _parts(book, chnu, first, last, mam_id):
    return {f"{book}.{chnu}.{v}": (PART, mam_id) for v in range(first, last + 1)}


def _notes(last_verse):
    """(anchor osisID, English note, {BHS osisID: (correspondence, MAM osisID)})."""
    return (
        (
            "1Sam.24.1",
            "1 Samuel 24:1 in this text is 23:29 in MAM's own numbering;"
            " each later verse of chapter 24 is one lower there.",
            {
                "1Sam.24.1": (FULL, "1Sam.23.29"),
                **_shift("1Sam", 24, 2, last_verse("1Sam.24"), 1),
            },
        ),
        (
            "Jer.31.1",
            "Jeremiah 31:1 in this text is 30:25 in MAM's own numbering;"
            " each later verse of chapter 31 is one lower there.",
            {
                "Jer.31.1": (FULL, "Jer.30.25"),
                **_shift("Jer", 31, 2, last_verse("Jer.31"), 1),
            },
        ),
        (
            "Num.25.19",
            "Numbers 25:19 and 26:1 in this text are together 26:1"
            " in MAM's own numbering.",
            {"Num.25.19": (PART, "Num.26.1"), "Num.26.1": (PART, "Num.26.1")},
        ),
        (
            "Josh.21.35",
            "This text has no Joshua 21:36–37: BHS numbers two verses here"
            " that MAM's text does not have. Each later verse of chapter 21"
            " is two lower in MAM's own numbering.",
            {
                "Josh.21.36": (PLACEHOLDER, None),
                "Josh.21.37": (PLACEHOLDER, None),
                **_shift("Josh", 21, 38, last_verse("Josh.21"), 2),
            },
        ),
        (
            "Exod.20.2",
            "Exodus 20:2–3 in this text are together 20:2 in MAM's own numbering;"
            " verses 20:4–12 are each one lower there.",
            {**_parts("Exod", 20, 2, 3, "Exod.20.2"), **_shift("Exod", 20, 4, 12, 1)},
        ),
        (
            "Exod.20.13",
            "Exodus 20:13–16 in this text are together 20:12 in MAM's own"
            " numbering; each later verse of chapter 20 is four lower there.",
            {
                **_parts("Exod", 20, 13, 16, "Exod.20.12"),
                **_shift("Exod", 20, 17, last_verse("Exod.20"), 4),
            },
        ),
        (
            "Deut.5.6",
            "Deuteronomy 5:6–7 in this text are together 5:6 in MAM's own"
            " numbering; verses 5:8–16 are each one lower there.",
            {**_parts("Deut", 5, 6, 7, "Deut.5.6"), **_shift("Deut", 5, 8, 16, 1)},
        ),
        (
            "Deut.5.17",
            "Deuteronomy 5:17–20 in this text are together 5:16 in MAM's own"
            " numbering; each later verse of chapter 5 is four lower there.",
            {
                **_parts("Deut", 5, 17, 20, "Deut.5.16"),
                **_shift("Deut", 5, 21, last_verse("Deut.5"), 4),
            },
        ),
    )


def variant_notes(verses):
    """Return {anchor osisID: note text}, after checking every note's claims.

    ``verses`` is every BHS verse node of MAM-simple, in order.
    """
    last = {}
    found = {}
    for verse in verses:
        osis_id = verse["osisID"]
        last[osis_id.rsplit(".", 1)[0]] = int(osis_id.rsplit(".", 1)[1])
        corr = verse.get("contents-corresponds-to")
        if corr is not None:
            found[osis_id] = (corr, verse.get("osisID-of-MAM-src"))
        elif "osisID-of-MAM-src" in verse:
            raise ValueError(f"MAM source without a correspondence at {osis_id}")
    expected = {}
    notes = {}
    for anchor, text, claims in _notes(last.__getitem__):
        if set(claims) & set(expected):
            raise ValueError(f"Overlapping renumbering claims at {anchor}")
        expected.update(claims)
        notes[anchor] = text
    if found != expected:
        stray = sorted(set(found.items()) ^ set(expected.items()), key=str)
        raise ValueError(f"MAM-simple's renumbering differs from the notes: {stray}")
    return notes
