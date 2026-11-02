"""MAM-parsed atom positions for the first exact scan-page census.

This initial projection accepts Scripture strings, a נוסח target, vowel
alternatives with identical consonantal atoms, and the main one-atom form of
the modern trivial ketiv/qere template, plus the explicit legarmeh marker. It
does not assign atom numbers through nontrivial ketiv/qere or alternative
strands: those need an explicit source-alignment policy before a later book
can be censused.
Documentation is never Scripture. Unknown templates fail rather than contribute
guessed text. No pointed text or second Bible corpus is stored in the index.
"""

import re

from mb_cmn import bib_locales as tbn
from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import template_names


def letters_atoms(text):
    """Letters-only atoms between whitespace or maqaf; marks retain their atom."""
    return tuple(
        letters
        for atom in re.split(r"[\s־]+", text)
        if (letters := "".join(ch for ch in atom if "א" <= ch <= "ת"))
    )


def _body_text(elements):
    if not isinstance(elements, (list, tuple)):
        raise TypeError(f"Scripture sequence expected, received {elements!r}")
    parts = []
    for element in elements:
        if isinstance(element, str):
            parts.append(element)
        elif isinstance(element, dict) and element["tmpl_name"] == "נוסח":
            if set(element) != {"tmpl_name", "tmpl_params"}:
                raise ValueError(f"Unexpected נוסח shape: {element}")
            params = element["tmpl_params"]
            if "1" not in params or not set(params) <= {"1", "2"}:
                raise ValueError(f"Unexpected נוסח parameters: {params}")
            target = params["1"]
            parts.append(_target_text(target))
        elif (
            isinstance(element, dict)
            and element["tmpl_name"] == template_names.QAMATS_VARIANT
        ):
            params = template_names.validate_current_plus_template(element)
            dalet, samekh = (_target_text(params[key]) for key in ("ד", "ס"))
            if letters_atoms(dalet) != letters_atoms(samekh):
                raise ValueError("Vowel alternatives have different consonantal atoms")
            parts.append(dalet)
        elif (
            isinstance(element, dict)
            and element["tmpl_name"] == template_names.TRIVIAL_QERE
        ):
            params = template_names.validate_current_plus_template(element)
            if not all(
                isinstance(params[key], str) and len(letters_atoms(params[key])) == 1
                for key in ("1", "2", "3")
            ):
                raise ValueError(
                    "Trivial ketiv/qere must contain one atom in each form"
                )
            # Match the existing MAM-simple kq-trivial body's main form, not
            # an alternative spelling or a reading assembled from other fields.
            parts.append(params["1"])
        elif isinstance(element, dict) and element["tmpl_name"] == "מ:לגרמיה-2":
            params = template_names.validate_current_plus_template(element)
            if params:
                raise ValueError("Explicit legarmeh marker must have no parameters")
            parts.append(" ")
        else:
            raise ValueError(
                "scan-pages atom projection does not yet support this Scripture "
                f"element: {element!r}"
            )
    return "".join(parts)


def _target_text(target):
    if isinstance(target, (str, dict)):
        return _body_text([target])
    if isinstance(target, (list, tuple)):
        return _body_text(target)
    raise TypeError(f"Unsupported Scripture target storage: {target!r}")


def book_atoms(bkid, books=None):
    """Return (chapter, verse) -> atoms, reading the landed parsed product."""
    if books is None:
        books = plus.read_parsed_plus_bk39s(
            [bkid], mam_parsed_path=paths.mam_parsed_path()
        )
    verses = {}
    for bcvt, minirow in books[bkid]["verses_plus"].items():
        cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
        verses[cv] = letters_atoms(_body_text(minirow.EP))
        if not verses[cv]:
            raise ValueError(f"{bkid} {cv}: no Scripture atoms")
    return verses


def locate_phrase(verses, chapter, verse, phrase):
    """Return the unique inclusive atom interval occupied by a source cue."""
    needle = letters_atoms(phrase)
    if not needle or " ".join(needle) != phrase:
        raise ValueError(
            f"Cue must contain letters-only atoms separated by spaces: {phrase!r}"
        )
    haystack = verses[chapter, verse]
    starts = [
        i + 1
        for i in range(len(haystack) - len(needle) + 1)
        if haystack[i : i + len(needle)] == needle
    ]
    if len(starts) != 1:
        raise ValueError(
            f"{chapter}:{verse}: cue {phrase!r} has {len(starts)} matches; "
            "supply a longer unique cue"
        )
    return starts[0], starts[0] + len(needle) - 1


def positions(verses):
    """All valid atom positions, in the book's actual text order."""
    return tuple(
        (c, v, p) for (c, v), atoms in verses.items() for p in range(1, len(atoms) + 1)
    )
