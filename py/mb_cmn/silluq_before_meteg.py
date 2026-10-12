"""Validate an explicit silluq position and remove only later meteg marks."""

import unicodedata

METEG = "\N{HEBREW POINT METEG}"


def _letter(char):
    return "\N{HEBREW LETTER ALEF}" <= char <= "\N{HEBREW LETTER TAV}"


def validate_silluq_before_meteg(text, letters_with_silluq, context="atom"):
    """Return the zero-based letter index carrying the explicitly identified silluq.

    Both arguments exclude punctuation. The second contains the same letters,
    exactly one U+05BD, and no other marks. The full atom has that mark and at
    least one meteg on a later letter. Earlier meteg marks remain permitted.
    """

    def fail(reason):
        raise ValueError(
            f"{context}: invalid silluq-before-meteg ({reason}); "
            f"text={text!r}, letters-with-silluq={letters_with_silluq!r}"
        )

    if not isinstance(text, str) or not isinstance(letters_with_silluq, str):
        fail("parameters must be strings")
    if not text or not letters_with_silluq:
        fail("empty parameter")
    if any(not (_letter(c) or c == METEG) for c in letters_with_silluq):
        fail("position parameter contains another mark or punctuation")
    if letters_with_silluq.count(METEG) != 1:
        fail("position parameter must contain exactly one U+05BD")
    if any(
        not (
            _letter(c)
            or (
                (0x0591 <= ord(c) <= 0x05C9 or ord(c) == 0xFB1E)
                # U+05C8 and U+05C9 are Hebrew annotation points in Unicode 17;
                # Python's Unicode database can predate their assignment.
                and (unicodedata.category(c) == "Mn" or ord(c) in (0x05C8, 0x05C9))
            )
        )
        for c in text
    ):
        fail("full atom contains a non-Hebrew mark or punctuation")
    letters = "".join(c for c in text if _letter(c))
    if not letters or letters != letters_with_silluq.replace(METEG, ""):
        fail("letter skeletons differ")
    silluq_index = letters_with_silluq.index(METEG) - 1
    if silluq_index < 0:
        fail("silluq precedes the first letter")
    meteg_indices = []
    letter_index = -1
    for char in text:
        if _letter(char):
            letter_index += 1
        elif letter_index < 0:
            fail("full atom starts with a combining mark")
        elif char == METEG:
            meteg_indices.append(letter_index)
    if len(set(meteg_indices)) != len(meteg_indices):
        fail("multiple U+05BD marks on one letter")
    if silluq_index not in meteg_indices:
        fail("full atom lacks the identified silluq")
    if not any(index > silluq_index for index in meteg_indices):
        fail("full atom has no later meteg")
    return silluq_index


def drop_post_silluq_metegs(text, letters_with_silluq, context="atom"):
    """Keep all characters except U+05BD on letters after the identified silluq."""
    silluq_index = validate_silluq_before_meteg(text, letters_with_silluq, context)
    result = []
    letter_index = -1
    for char in text:
        if _letter(char):
            letter_index += 1
        if char != METEG or letter_index <= silluq_index:
            result.append(char)
    return "".join(result)
