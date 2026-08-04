"""HAND-AUTHORED: the differences between source and generated page that are
deliberate.

Everything not listed here fails ``difftext``. With a verbatim port the list
stays short, and it is meant to: an entry records the exact words on both
sides, so a *new* difference can never hide behind an existing allowance.
There is deliberately no wildcard entry -- an allowance that matched anything
would quietly turn the check off.
"""


def for_part(part: int):
    """The allowed (reason, source words, generated words) for one part."""
    return _heading_split(part)


def match(allowed, tag, got, want):
    """The reason this opcode is allowed, or None."""
    for reason, exp_got, exp_want in allowed:
        if exp_got == got and exp_want == want:
            return reason
    return None


###########################################################


def _heading_split(part: int):
    """Ben's heading decision, as it lands in a word-level diff.

    The four documents share one title, so a verbatim port would give the
    four pages the same h1. Instead each page's h1 takes the part number up
    with it and the subtitle becomes the h2:

        source    Undoing and redoing ... Masoretes / Part 1: The tale ...
        generated Undoing and redoing ... Masoretes – Part 1 / The tale ...

    Same words in the same order. The diff sees only the inserted en dash and
    the colon that moved off the part number.
    """
    reason = "Heading split: the part number joins the h1, the subtitle becomes the h2."
    return (
        (reason, "", "–"),
        (reason, f"{part}:", str(part)),
    )
