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
Explicitly verified one-written/two-qere forms select the qere pair and
declare its span indivisible at page boundaries. Other multi-atom ketiv/qere
and alternative strands need source alignment.
Read-but-not-written words contribute no atom under the maintained written-atom
policy. A named two-word qere may contain a parameterless paseq between its words.
The special-letter word wrapper and the small/large-letter templates recurse into
their Scripture parameter without inserting a word boundary or losing a letter.
Documentation is never Scripture. Unknown templates fail rather than contribute
guessed text. No pointed text or second Bible corpus is stored in the index.

Poetic-space and gray-maqaf templates are explicit separators. Stress helpers
and vowel variants select one branch only after consonants and atom boundaries
agree across both branches. A leading inverted nun has no Scripture atom; only
its exact sign-plus-space payload is accepted at the start of a verse.
"""

import re

from mb_cmn import bib_locales as tbn
from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import template_names

_UNEQUAL_KQ_FORMS = {
    'כו"ק כתיב מילה חדה וקרי תרתין מילין': {
        (("מהם",), ("מה", "הם")),
        (("מאשתם",), ("מאש", "תם")),
        (("והנהו",), ("והנה", "הוא")),
        (("חלכאים",), ("חל", "כאים")),
        (("ישימות",), ("ישי", "מות")),
        (("לגאיונים",), ("לגאי", "יונים")),
    },
    'כו"ק קרי שונה מהכתיב בשתי מילים': {(("כאשר",), ("ככל", "אשר"))},
}


def letters_atoms(text):
    """Letters-only atoms between whitespace or maqaf; marks retain their atom."""
    return tuple(
        letters
        for atom in re.split(r"[\s־]+", text)
        if (letters := "".join(ch for ch in atom if "א" <= ch <= "ת"))
    )


def _body_text(elements, *, protected=None):
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
            parts.append(_target_text(target, protected=protected))
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
        elif isinstance(element, dict) and element["tmpl_name"] == "קרי ולא כתיב":
            params = template_names.validate_current_plus_template(element)
            if not all(isinstance(params[key], str) for key in ("1", "2")):
                raise ValueError("Read-but-not-written word needs string forms")
            displayed, reading = (letters_atoms(params[key]) for key in ("1", "2"))
            if len(reading) != 1 or displayed != reading:
                raise ValueError("Read-but-not-written forms must share one atom")
            # Ben's maintained written-atom policy in mam_json_verses excludes
            # kq-q-velo-k. Keep neighboring written words separate at its slot.
            parts.append(" ")
        elif (
            isinstance(element, dict)
            and element["tmpl_name"] == template_names.SLH_WORD
        ):
            params = template_names.validate_current_plus_template(element)
            selected = _target_text(params["1"], protected=protected)
            if (
                not all(isinstance(params[key], str) for key in ("2", "3", "4", "5"))
                or len(letters_atoms(selected)) != 1
                or _consonantal_layout(selected) != _consonantal_layout(params["2"])
                or any(ch.isspace() or ch == "\u05be" for ch in selected)
            ):
                raise ValueError("Special-letter word lost a letter or atom boundary")
            parts.append(selected)
        elif isinstance(element, dict) and element["tmpl_name"] in {
            "מ:אות-ק",
            "מ:אות-ג",
            "מ:אות תלויה",
        }:
            params = template_names.validate_current_plus_template(element)
            marked = params["1"]
            if (
                not isinstance(marked, str)
                or len(atoms := letters_atoms(marked)) != 1
                or len(atoms[0]) != 1
                or any(ch.isspace() or ch == "\u05be" for ch in marked)
            ):
                raise ValueError("Marked letter must preserve one in-word letter")
            parts.append(marked)
        elif (
            isinstance(element, dict)
            and element["tmpl_name"] == template_names.QAMATS_VARIANT
        ):
            params = template_names.validate_current_plus_template(element)
            dalet = _variant_text(params["ד"])
            samekh = _variant_text(params["ס"])
            _require_same_layout(dalet, samekh)
            parts.append(dalet)
        elif (
            isinstance(element, dict)
            and element["tmpl_name"] in template_names.STRESS_HELPER_TMPL_NAMES
        ):
            params = template_names.validate_current_plus_template(element)
            forms = []
            for key in ("1", "2"):
                form = params[key]
                if isinstance(form, str):
                    forms.append(form)
                elif (
                    isinstance(form, dict)
                    and form.get("tmpl_name") == template_names.SLH_WORD
                ):
                    forms.append(_body_text([form]))
                else:
                    raise ValueError("Unsupported stress-helper alternative storage")
            _require_same_layout(*forms)
            parts.append(forms[0])
        elif (
            isinstance(element, dict)
            and element["tmpl_name"] == template_names.TRIVIAL_QERE
        ):
            params = template_names.validate_current_plus_template(element)
            forms = tuple(_trivial_form(params[key]) for key in ("1", "2", "3"))
            if any(not isinstance(params[key], str) for key in ("1", "2", "3")):
                if (
                    tuple(map(letters_atoms, forms))
                    != (("דרכו",), ("דרכו",), ("דרכיו",))
                    or not isinstance(params["1"], list)
                    or not isinstance(params["2"], str)
                    or not isinstance(params["3"], list)
                    or set(params) != {"1", "2", "3", "מקורות", "סוג"}
                    or params["מקורות"] != "א-קרי"
                    or params["סוג"] != 'כתיב חסר יו"ד בסיומת של קמץ ואחריו וי"ו'
                ):
                    raise ValueError("Unverified nested trivial ketiv/qere")
            # Match the existing MAM-simple kq-trivial body's main form, not
            # an alternative spelling or a reading assembled from other fields.
            parts.append(forms[0])
        elif isinstance(element, dict) and element["tmpl_name"] == "מ:כו״ק מיוחד":
            params = template_names.validate_current_plus_template(element)
            if params["סוג"] == 'כו"ק של שתי מילים בהערה אחת':
                if (
                    not isinstance(params["1"], str)
                    or len(letters_atoms(params["1"])) != 2
                ):
                    raise ValueError("Special ketiv/qere needs the named two-word form")
                qere = _two_word_special_qere(params["2"])
            elif params["סוג"] in _UNEQUAL_KQ_FORMS:
                if not isinstance(params["1"], str):
                    raise ValueError("Unequal ketiv/qere needs a string written form")
                qere = _unequal_qere_form(params["2"])
                forms = letters_atoms(params["1"]), letters_atoms(qere)
                if forms not in _UNEQUAL_KQ_FORMS[params["סוג"]]:
                    raise ValueError("Unverified unequal ketiv/qere forms")
                if protected is not None:
                    protected.append(" ".join(forms[1]))
            else:
                raise ValueError("Unsupported special ketiv/qere subtype")
            # Maintained projection selects qere parameter 2. A single written
            # word mapped to a pair must keep both qere atoms on the same page.
            parts.append(qere)
        elif isinstance(element, dict) and element["tmpl_name"] in {"כו״ק", "קו״כ"}:
            params = template_names.validate_current_plus_template(element)
            _ketiv, qere = (_ordinary_kq_form(params[key]) for key in ("1", "2"))
            # Both template orders store ketiv in 1 and qere in 2. Match
            # MAM-simple's selected qere; each source form has the same slot.
            parts.append(qere)
        elif isinstance(element, dict) and element["tmpl_name"] in {
            "פפ",
            "פפפ",
            "ר0",
            "ר1",
            "ר2",
            "ר3",
            "ר4",
            "מ:מקף אפור",
            "סס",
            "ססס",
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


def _consonantal_layout(value):
    """Retain consonants and every atom boundary, including the outer edges."""
    letters_and_boundaries = "".join(
        ch for ch in value if "א" <= ch <= "ת" or ch.isspace() or ch == "\u05be"
    )
    return re.sub(r"[\s\u05be]+", " ", letters_and_boundaries)


def _require_same_layout(first, second):
    if not letters_atoms(first) or _consonantal_layout(first) != _consonantal_layout(
        second
    ):
        raise ValueError("Alternatives have different consonants or atom boundaries")


def _variant_text(form):
    if isinstance(form, str):
        return form
    if (
        isinstance(form, dict)
        and form.get("tmpl_name") in template_names.STRESS_HELPER_TMPL_NAMES
    ):
        return _body_text([form])
    if (
        isinstance(form, list)
        and len(form) == 2
        and isinstance(form[0], str)
        and isinstance(form[1], dict)
        and form[1].get("tmpl_name") == "מ:מקף אפור"
    ):
        return _body_text(form)
    raise ValueError("Unsupported vowel-alternative storage")


def _trivial_form(form):
    rendered = form if isinstance(form, str) else _trailing_legarmeh_form(form)
    if len(letters_atoms(rendered)) != 1:
        raise ValueError("Trivial ketiv/qere must preserve one atom per form")
    return rendered


def _trailing_legarmeh_form(form):
    if (
        not isinstance(form, list)
        or len(form) != 2
        or not isinstance(form[0], str)
        or not isinstance(form[1], dict)
        or form[1].get("tmpl_name") != "מ:לגרמיה-2"
    ):
        raise ValueError("Unsupported trailing legarmeh storage")
    return _body_text(form)


def _unequal_qere_form(form):
    return form if isinstance(form, str) else _trailing_legarmeh_form(form)


def _verse_text(elements, *, protected=None):
    if (
        isinstance(elements, (list, tuple))
        and elements
        and isinstance(elements[0], dict)
        and elements[0].get("tmpl_name") == template_names.INVERTED_NUN
    ):
        params = template_names.validate_current_plus_template(elements[0])
        if params != {"1": "\u05c6 "}:
            raise ValueError("Unverified leading inverted-nun payload")
        rendered = _body_text(elements[1:], protected=protected)
        if not letters_atoms(rendered):
            raise ValueError("Leading inverted nun requires following Scripture")
        return rendered
    return _body_text(elements, protected=protected)


def _two_word_special_qere(form):
    if isinstance(form, str):
        rendered = form
    elif (
        isinstance(form, list)
        and len(form) == 3
        and isinstance(form[0], str)
        and isinstance(form[2], str)
        and all(len(letters_atoms(form[i])) == 1 for i in (0, 2))
        and isinstance(form[1], dict)
        and form[1].get("tmpl_name") == "מ:פסק"
    ):
        # The named parent still has two ordered written/qere slots. Only
        # this explicit parameterless separator is admitted inside the qere.
        rendered = _body_text(form)
    else:
        raise ValueError("Unsupported two-word special qere storage")
    if len(letters_atoms(rendered)) != 2:
        raise ValueError("Special qere must preserve exactly two ordered atoms")
    return rendered


def _ordinary_kq_form(form):
    if isinstance(form, str):
        selected = form
    elif isinstance(form, dict) and form.get("tmpl_name") in {
        template_names.QAMATS_VARIANT,
        *template_names.STRESS_HELPER_TMPL_NAMES,
    }:
        params = template_names.validate_current_plus_template(form)
        # Reuse the closed vowel rule: both branches must have identical
        # consonantal atoms. This does not admit other nested template families.
        selected = _body_text([form])
    elif isinstance(form, list):
        selected = _trailing_legarmeh_form(form)
    else:
        raise ValueError("Unsupported ordinary ketiv/qere form")
    if len(letters_atoms(selected)) != 1:
        raise ValueError(
            "Ordinary ketiv/qere needs one atom in each form for scan alignment"
        )
    return selected


def _target_text(target, *, protected=None):
    if isinstance(target, (str, dict)):
        return _body_text([target], protected=protected)
    if isinstance(target, (list, tuple)):
        return _body_text(target, protected=protected)
    raise TypeError(f"Unsupported Scripture target storage: {target!r}")


def book_atoms(bkid, books=None):
    """Return (chapter, verse) -> atoms, reading the landed parsed product."""
    return _book_projection(bkid, books)[0]


def book_alignment_spans(bkid, books=None):
    """Indivisible canonical spans mapped to one source-written word."""
    return _book_projection(bkid, books)[1]


def _book_projection(bkid, books):
    if books is None:
        books = plus.read_parsed_plus_bk39s(
            [bkid], mam_parsed_path=paths.mam_parsed_path()
        )
    verses, spans = {}, []
    for bcvt, minirow in books[bkid]["verses_plus"].items():
        cv = tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt)
        protected = []
        verses[cv] = letters_atoms(_verse_text(minirow.EP, protected=protected))
        if not verses[cv]:
            raise ValueError(f"{bkid} {cv}: no Scripture atoms")
        for phrase in protected:
            # Refuse an ambiguous pair instead of guessing which occurrence
            # corresponds to the mapped source word. Search only this verse.
            first, last = locate_phrase_span({cv: verses[cv]}, *cv, phrase)
            if first[:2] != last[:2] or last[2] != first[2] + 1:
                raise ValueError(
                    "Unequal mapping must cover exactly two adjacent atoms"
                )
            spans.append((first, last))
    return verses, tuple(spans)


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
