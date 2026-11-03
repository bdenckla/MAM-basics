"""MAM-parsed atom positions for the first exact scan-page census.

This initial projection accepts Scripture strings, a נוסח target, vowel
alternatives with identical consonantal atoms, and the main one-atom form of
the modern trivial ketiv/qere template, plus explicit paseq/legarmeh and
the named paragraph markers. A written-but-not-read word contributes its
unpointed written atom, following the maintained MAM-simple atom policy.
Ordinary ketiv/qere uses the qere spelling only when both forms are one atom,
so either printed form occupies the same position. Its named vowel-alternative
wrapper may select consonant-identical string forms. The explicitly named
two-word special form likewise preserves two ordered slots in both forms.
Other multi-atom ketiv/qere and alternative strands need source alignment.
The special-letter word wrapper and the small/large-letter templates recurse into
their Scripture parameter without inserting a word boundary or losing a letter.
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
        elif isinstance(element, dict) and element["tmpl_name"] == "כתיב ולא קרי":
            params = template_names.validate_current_plus_template(element)
            if not all(isinstance(params[key], str) for key in ("1", "2")):
                raise ValueError("Written-but-not-read word needs string forms")
            displayed, written = (letters_atoms(params[key]) for key in ("1", "2"))
            if len(written) != 1 or displayed != written:
                raise ValueError("Written-but-not-read forms must share one atom")
            # The maintained written-atom policy in mam_json_verses includes
            # kq-k-velo-q. Parentheses in the display form are not letters.
            parts.append(params["2"])
        elif isinstance(element, dict) and element["tmpl_name"] in {
            template_names.SLH_WORD,
            "מ:אות-ק",
            "מ:אות-ג",
        }:
            params = template_names.validate_current_plus_template(element)
            # These explicit in-word templates contribute their Scripture
            # parameter. Their descriptions are metadata; do not split the word.
            parts.append(_target_text(params["1"]))
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
        elif isinstance(element, dict) and element["tmpl_name"] == "מ:כו״ק מיוחד":
            params = template_names.validate_current_plus_template(element)
            if params["סוג"] != 'כו"ק של שתי מילים בהערה אחת' or not all(
                isinstance(params[key], str) and len(letters_atoms(params[key])) == 2
                for key in ("1", "2")
            ):
                raise ValueError("Special ketiv/qere needs the named two-word form")
            # Maintained projection selects qere parameter 2. Both native
            # editions at Ezekiel 42:9 retain two ordered written/qere slots;
            # no one-to-two or other special subtype is silently flattened.
            parts.append(params["2"])
        elif isinstance(element, dict) and element["tmpl_name"] in {"כו״ק", "קו״כ"}:
            params = template_names.validate_current_plus_template(element)
            _ketiv, qere = (_ordinary_kq_form(params[key]) for key in ("1", "2"))
            # Both template orders store ketiv in 1 and qere in 2. Match
            # MAM-simple's selected qere; each source form has the same slot.
            parts.append(qere)
        elif isinstance(element, dict) and element["tmpl_name"] in {
            "פפ",
            "פפפ",
            "סס",
        }:
            template_names.validate_current_plus_template(element)
            # Maintained NO_ATOM semantics separate the neighboring words.
            # Optional parameter 1 describes the break; it is not Scripture.
            parts.append(" ")
        elif isinstance(element, dict) and element["tmpl_name"] in {
            "מ:לגרמיה-2",
            "מ:פסק",
        }:
            params = template_names.validate_current_plus_template(element)
            if params:
                raise ValueError(
                    "Explicit paseq/legarmeh marker must have no parameters"
                )
            # Maintained NO_ATOM definitions keep both neighboring words apart;
            # omitting a paseq entirely would join the strings around it.
            parts.append(" ")
        else:
            raise ValueError(
                "scan-pages atom projection does not yet support this Scripture "
                f"element: {element!r}"
            )
    return "".join(parts)


def _ordinary_kq_form(form):
    if isinstance(form, str):
        selected = form
    elif (
        isinstance(form, dict)
        and form.get("tmpl_name") == template_names.QAMATS_VARIANT
    ):
        params = template_names.validate_current_plus_template(form)
        if not all(isinstance(params[key], str) for key in ("ד", "ס")):
            raise ValueError("Ketiv/qere vowel alternatives need string forms")
        # Reuse the closed vowel rule: both branches must have identical
        # consonantal atoms. This does not admit other nested template families.
        selected = _body_text([form])
    else:
        raise ValueError("Unsupported ordinary ketiv/qere form")
    if len(letters_atoms(selected)) != 1:
        raise ValueError(
            "Ordinary ketiv/qere needs one atom in each form for scan alignment"
        )
    return selected


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
    """Return a unique phrase's atom interval when confined to the given verse."""
    first, last = locate_phrase_span(verses, chapter, verse, phrase)
    if last[:2] != (chapter, verse):
        raise ValueError("Cross-verse phrase requires its full position span")
    return first[2], last[2]


def locate_phrase_span(verses, chapter, verse, phrase, *, anchor="start"):
    """Locate a unique phrase, anchoring its first or last atom in a verse.

    A source edge cue can cross a verse boundary on the same page. The start
    reference names its first atom's verse; the stop reference names its last
    atom's verse. Neither a repeated short cue nor a missing atom is guessed.
    """
    if anchor not in {"start", "stop"}:
        raise ValueError(f"Unknown phrase anchor: {anchor}")
    needle = letters_atoms(phrase)
    if not needle or " ".join(needle) != phrase:
        raise ValueError(
            f"Cue must contain letters-only atoms separated by spaces: {phrase!r}"
        )
    verses[chapter, verse]  # A nonexistent reference still fails explicitly.
    haystack = tuple(atom for atoms in verses.values() for atom in atoms)
    atom_positions = positions(verses)
    anchored = [
        i
        for i, position in enumerate(atom_positions)
        if position[:2] == (chapter, verse)
    ]
    shift = 0 if anchor == "start" else len(needle) - 1
    starts = [
        i - shift
        for i in anchored
        if i >= shift and haystack[i - shift : i - shift + len(needle)] == needle
    ]
    if len(starts) != 1:
        raise ValueError(
            f"{chapter}:{verse}: cue {phrase!r} has {len(starts)} matches; "
            "supply a longer unique cue"
        )
    return atom_positions[starts[0]], atom_positions[starts[0] + len(needle) - 1]


def positions(verses):
    """All valid atom positions, in the book's actual text order."""
    return tuple(
        (c, v, p) for (c, v), atoms in verses.items() for p in range(1, len(atoms) + 1)
    )
