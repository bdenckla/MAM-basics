def explanation_for_path(path_parts):
    (label,) = path_parts
    return _EXPLANATIONS_BY_LABEL[label]


_EXPLANATIONS_BY_LABEL = {
    "double-guillemets": "that the form contains a double guillemet",
    "plus": "that the form has a plus sign with a Hebrew letter or mark on each side",
}


OVERALL_EXPLANATION = (
    " ".join(
        (
            "This page lists the forms in MAM's documentation notes that use plus",
            "notation or double guillemets. Each row shows one form, as its note has",
            "it, and links to the note's verse. Each category appears even when it has",
            "no forms, so that its first use will show up here.",
        )
    ),
    " ".join(
        (
            "In plus notation, two sets of marks on one letter are shown by writing",
            "the letter twice, joined by a plus sign, with one set of marks on each",
            "copy.",
        )
    ),
    " ".join(
        (
            "MAM-basics' near-Aleppo example edition has some marks on an artificial",
            "carrier letter between double guillemets (« »). MAM's notes sometimes",
            "quote a form between single guillemets (‹ ›); those are different",
            "characters and do not count here.",
        )
    ),
)
