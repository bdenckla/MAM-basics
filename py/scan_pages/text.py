"""MAM-parsed atom positions for the first exact scan-page census.

This initial projection accepts Scripture strings, נוסח and annotation targets, vowel
alternatives with identical consonantal atoms, and the main one-atom form of
the modern trivial ketiv/qere template, plus explicit paseq/legarmeh and
the named paragraph markers. A written-but-not-read word contributes its
unpointed written atom, following the maintained MAM-simple atom policy.
Its exact following-maqaf form preserves the boundary before the next atom.
Ordinary ketiv/qere uses the qere spelling only when both forms are one atom,
so either printed form occupies the same position. Its named vowel-alternative
wrapper may select consonant-identical string forms. Named equal-length special forms preserve two or three ordered slots.
Explicitly verified one-written/two-qere forms select the qere pair and
declare its span indivisible at page boundaries. Eight complete accepted
two-written/one-qere forms supply one canonical position. Other multi-atom ketiv/qere
need source alignment. Named dual representations select combined canonical
text after all three ordered atom arrays and protected traces agree. Paragraph
alternatives can have no atoms; the containing verse still requires Scripture.
Physical source strands are not selected by this projection.
Read-but-not-written words contribute no atom under the maintained written-atom
policy. A named two-word qere may contain a parameterless paseq between its words.
The special-letter wrapper reads its named styling children as a complete pointed
target, including its existing maqaf boundaries and terminal legarmeh separator.
Documentation is never Scripture. Unknown templates fail rather than contribute
guessed text. No pointed text or second Bible corpus is stored in the index.

Poetic-space and gray-maqaf templates are explicit separators. Stress helpers
and vowel variants select one branch only after consonants and atom boundaries
agree across both branches. A leading inverted nun has no Scripture atom; only
its exact sign-plus-space payload is accepted at the start of a verse.
The two Numbers signs retain their exact wrapper, verse context and adjacent
paragraph marker. The silluq-before-meteg wrapper retains its validated atom.
"""

import re
import unicodedata

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


_ADDITIONAL_UNEQUAL_KQ = {
    ("Genesis", 30, 11): {
        "path": (1,),
        "subtype": 'כו"ק כתיב מילה חדה וקרי תרתין מילין',
        "written": "בגד",
        "qere": "בָּ֣א גָ֑ד",
    },
    ("Exodus", 4, 2): {
        "path": (1,),
        "subtype": 'כו"ק כתיב מילה חדה וקרי תרתין מילין',
        "written": "מזה",
        "qere": "מַה־זֶּ֣ה",
    },
    ("Deuter", 33, 2): {
        "path": (3,),
        "subtype": 'כו"ק כתיב מילה חדה וקרי תרתין מילין',
        "written": "אשדת",
        "qere": "אֵ֥שׁ דָּ֖ת",
    },
    ("2Samuel", 8, 3): {
        "path": (1, "tmpl_params", "1"),
        "subtype": 'כו"ק קרי שונה מהכתיב בשתי מילים',
        "written": "בנהר",
        "qere": "בִּֽנְהַר־פְּרָֽת",
    },
    ("2Kings", 18, 27): {
        "path": (5, "tmpl_params", "1"),
        "subtype": 'קו"כ קרי שונה מהכתיב בשתי מילים',
        "written": "שניהם",
        "qere": "מֵימֵ֥י רַגְלֵיהֶ֖ם",
    },
    ("Isaiah", 3, 15): {
        "path": (0,),
        "subtype": 'כו"ק כתיב מילה חדה וקרי תרתין מילין',
        "written": "מלכם",
        "qere": "מַה־לָּכֶם֙",
    },
    ("Isaiah", 36, 12): {
        "path": (3, "tmpl_params", "1"),
        "subtype": 'קו"כ קרי שונה מהכתיב בשתי מילים',
        "written": "שיניהם",
        "qere": "מֵימֵ֥י רַגְלֵיהֶ֖ם",
    },
    ("Job", 38, 1): {
        "path": (3,),
        "subtype": 'כו"ק כתיב מילה חדה וקרי תרתין מילין',
        "written": "מנהסערה",
        "qere": ["מִ֥ן", {"tmpl_name": "מ:פסק"}, "הַסְּעָרָ֗ה"],
    },
    ("Job", 40, 6): {
        "path": (3,),
        "subtype": 'כו"ק כתיב מילה חדה וקרי תרתין מילין',
        "written": "מנסערה",
        "qere": ["מִ֥ן", {"tmpl_name": "מ:פסק"}, "סְעָרָ֗ה"],
    },
    ("Nehemiah", 2, 13): {
        "path": (3, "tmpl_params", "1"),
        "subtype": 'קו"כ כתיב מילה חדה וקרי תרתין מילין',
        "written": "המפרוצים",
        "qere": ["הֵ֣ם", {"tmpl_name": "מ:פסק"}, "פְּרוּצִ֔ים"],
    },
    ("1Chronicles", 9, 4): {
        "path": (1, "tmpl_params", "1"),
        "subtype": 'כו"ק כתיב מילה חדה וקרי תרתין מילין בין שני מקפים',
        "written": "בנימן",
        "qere": "בָּנִ֔י מִן־",
    },
    ("1Chronicles", 27, 12): {
        "path": (1, "tmpl_params", "1"),
        "subtype": 'כו"ק כתיב מילה חדה וקרי תרתין מילין',
        "written": "לבנימיני",
        "qere": ["לַבֵּ֣ן", {"tmpl_name": "מ:פסק"}, "יְמִינִ֑י"],
    },
}

_THREE_ATOM_SPECIAL_KQ = {
    ("2Samuel", 21, 12): {
        "path": (1, "tmpl_params", "1"),
        "subtype": 'כו"ק של שלוש מילים בהערה אחת',
        "written": "תלום שם הפלשתים",
        "qere": "תְּלָא֥וּם שָׁ֙מָּה֙ פְּלִשְׁתִּ֔ים",
    }
}


_TWO_WRITTEN_ONE_QERE_KQ = {
    ("Judges", 16, 25): {
        "path": (1,),
        "subtype": 'כו"ק כתיב תרתין מילין וקרי מילה חדה',
        "written": "כי טוב",
        "qere": "כְּט֣וֹב",
    },
    ("1Samuel", 9, 1): {
        "path": (1,),
        "subtype": 'כו"ק כתיב תרתין מילין וקרי מילה חדה',
        "written": "מבן ימין",
        "qere": "מִבִּנְיָמִ֗ין",
    },
    ("1Samuel", 24, 8): {
        "path": (1,),
        "subtype": 'כו"ק כתיב תרתין מילין וקרי מילה חדה',
        "written": "מן המערה",
        "qere": "מֵֽהַמְּעָרָ֔ה",
    },
    ("Isaiah", 9, 6): {
        "path": (0, "tmpl_params", "1"),
        "subtype": 'כו"ק כתיב תרתין מילין וקרי מילה חדה',
        "written": "לם רבה",
        "qere": "לְמַרְבֵּ֨ה",
    },
    ("Isaiah", 44, 24): {
        "path": (1, "tmpl_params", "1"),
        "subtype": 'כו"ק כתיב תרתין מילין וקרי מילה חדה',
        "written": "מי אתי",
        "qere": "מֵאִתִּֽי",
    },
    ("Lamentations", 1, 6): {
        "path": (1,),
        "subtype": 'כו"ק כתיב תרתין מילין וקרי מילה חדה',
        "written": "מן בת",
        "qere": "מִבַּת־",
    },
    ("Lamentations", 4, 3): {
        "path": (3, "tmpl_params", "1"),
        "subtype": 'כו"ק כתיב תרתין מילין וקרי מילה חדה',
        "written": "כי ענים",
        "qere": "כַּיְעֵנִ֖ים",
    },
    ("2Chronicles", 34, 6): {
        "path": (1,),
        "subtype": 'כו"ק כתיב תרתין מילין וקרי מילה חדה',
        "written": "בחר בתיהם",
        "qere": "בְּחַרְבֹתֵיהֶ֖ם",
    },
}

_EXTERNAL_UNEQUAL_MAQAF = {
    ("2Kings", 18, 27): ("אֶת־", None),
    ("Isaiah", 36, 12): ("אֶת־", None),
    ("Nehemiah", 2, 13): ("אֲשֶׁר־", None),
    ("1Chronicles", 9, 4): ("בֶן־", "בְּנֵי־פֶ֖רֶץ"),
}

_MID_COMPOUND_KQ = {
    ("Isaiah", 26, 20): {
        "path": (5, "tmpl_params", "1"),
        "subtype": 'כו"ק בין שני מקפים',
        "written": "יעבור",
        "qere": "יַעֲבׇר־",
        "previous": "עַד־",
        "following": "זָֽעַם׃",
    }
}

_WRITTEN_ONLY_MAQAF_FORMS = {("(אם)־", "אם"), ("(נא)־", "נא")}


def letters_atoms(text):
    """Letters-only atoms between whitespace or maqaf; marks retain their atom."""
    return tuple(
        letters
        for atom in re.split(r"[\s־]+", text)
        if (letters := "".join(ch for ch in atom if "א" <= ch <= "ת"))
    )


def _body_text(elements, *, protected=None, context=None):
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
            parts.append(_target_text(target, protected=protected, context=context))
        elif (
            isinstance(element, dict)
            and element["tmpl_name"] == template_names.SCRDFF_TAR
        ):
            params = template_names.validate_current_plus_template(element)
            parts.append(
                _target_text(params["1"], protected=protected, context=context)
            )
        elif (
            isinstance(element, dict)
            and element["tmpl_name"] == template_names.SILLUQ_BEFORE_METEG
        ):
            params = template_names.validate_current_plus_template(element)
            if not all(isinstance(params[key], str) for key in ("1", "2")):
                raise ValueError("Silluq wrapper requires scalar string forms")
            parts.append(params["1"])
        elif (
            isinstance(element, dict)
            and element["tmpl_name"] == template_names.DUAL_CANTILLATION
        ):
            params = template_names.validate_current_plus_template(element)
            parts.append(_dual_text(params, protected=protected, context=context))
        elif isinstance(element, dict) and element["tmpl_name"] == "כתיב ולא קרי":
            params = template_names.validate_current_plus_template(element)
            if not all(isinstance(params[key], str) for key in ("1", "2")):
                raise ValueError("Written-but-not-read word needs string forms")
            displayed, written = (letters_atoms(params[key]) for key in ("1", "2"))
            if len(written) != 1 or displayed != written:
                raise ValueError("Written-but-not-read forms must share one atom")
            # The maintained written-atom policy in mam_json_verses includes
            # kq-k-velo-q. Parentheses in the display form are not letters.
            if "3" in params:
                if (
                    params["3"] != "\N{HEBREW PUNCTUATION MAQAF}"
                    or (params["1"], params["2"]) not in _WRITTEN_ONLY_MAQAF_FORMS
                ):
                    raise ValueError("Unverified written-only following-maqaf form")
                # The following maqaf contributes no atom, but omitting its
                # boundary would join the written form to the next atom.
                parts.append(params["2"] + " ")
            else:
                if any("\N{HEBREW PUNCTUATION MAQAF}" in params[k] for k in ("1", "2")):
                    raise ValueError("Written-only maqaf needs its explicit marker")
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
            parts.append(_special_letter_text(params))
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
            if any(isinstance(params[key], dict) for key in ("1", "3")):
                parts.append(_nested_trivial_main(params))
                continue
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
            elif params["סוג"] == 'כו"ק של שלוש מילים בהערה אחת':
                _bcv, _elements, case = _accepted_special_case(
                    params, context, _THREE_ATOM_SPECIAL_KQ
                )
                qere = case["qere"]
            elif params["סוג"] == 'כו"ק בין שני מקפים':
                qere = _mid_compound_qere(params, context)
            elif params["סוג"] == 'כו"ק כתיב תרתין מילין וקרי מילה חדה':
                qere = _two_written_one_qere(params, context)
            elif context is not None and context[0] in _ADDITIONAL_UNEQUAL_KQ:
                qere = _additional_unequal_qere(params, context)
                if protected is not None:
                    protected.append(" ".join(letters_atoms(qere)))
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
            # Every display order selects qere parameter 2. Only the named
            # one-written/two-qere cases above introduce protected pairs.
            parts.append(qere)
        elif isinstance(element, dict) and element["tmpl_name"] in {"כו״ק", "קו״כ"}:
            params = template_names.validate_current_plus_template(element)
            if (
                isinstance(params["1"], dict)
                and params["1"].get("tmpl_name") == template_names.SLH_WORD
            ):
                _ketiv = _ordinary_special_written(params["1"], params["2"])
                qere = _ordinary_kq_form(params["2"])
            else:
                _ketiv, qere = (_ordinary_kq_form(params[key]) for key in ("1", "2"))
            # Both template orders store ketiv in 1 and qere in 2. Match
            # MAM-simple's selected qere; each source form has the same slot.
            parts.append(qere)
        elif isinstance(element, dict) and element["tmpl_name"] in {
            "מ:ששש",
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


def _dual_text(params, *, protected=None, context=None):
    """Select canonical combined text after validating all named alternatives."""
    forms, traces = [], []
    for key in ("כפול", "א", "ב"):
        trace = []
        forms.append(_target_text(params[key], protected=trace, context=context))
        traces.append(trace)
    populations = tuple(map(letters_atoms, forms))
    if populations[0] != populations[1] or populations[0] != populations[2]:
        raise ValueError("Dual alternatives have different canonical atom populations")
    if traces[0] != traces[1] or traces[0] != traces[2]:
        raise ValueError("Dual alternatives have different protected spans")
    if protected is not None:
        protected.extend(traces[0])
    return forms[0]


def _special_letter_text(params):
    """Read only named styling children, retaining the complete pointed target."""
    if not all(isinstance(params[key], str) for key in ("2", "3", "4", "5")):
        raise ValueError("Special-letter descriptions require strings")
    target = params["1"]
    if isinstance(target, (str, dict)):
        children = (target,)
    elif isinstance(target, (list, tuple)):
        children = target
    else:
        raise TypeError("Unsupported special-letter target storage")
    parts, terminal = [], False
    for index, child in enumerate(children):
        if isinstance(child, str):
            parts.append(child)
        elif isinstance(child, dict) and child.get("tmpl_name") in {
            "מ:אות-ק",
            "מ:אות-ג",
            "מ:אות תלויה",
        }:
            parts.append(_body_text([child]))
        elif (
            isinstance(child, dict)
            and child.get("tmpl_name") == "מ:לגרמיה-2"
            and index == len(children) - 1
        ):
            if template_names.validate_current_plus_template(child):
                raise ValueError("Terminal legarmeh must be bare")
            terminal = True
        else:
            raise ValueError("Unsupported special-letter Scripture child")
    body = "".join(parts)
    parallel = body + ("\N{HEBREW PUNCTUATION PASEQ}" if terminal else "")
    if not letters_atoms(body) or parallel != params["2"]:
        raise ValueError("Complete pointed special-letter targets differ")
    return body + (" " if terminal else "")


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


def _nested_trivial_main(params):
    """Read the verified one-slot main forms through their named alternatives."""
    pairs = {"בעינו": "בעיניו", "בשפתו": "בשפתיו", "שרידו": "שרידיו", "ילדו": "ילדיו"}
    written = params["2"]
    if not isinstance(written, str):
        raise ValueError("Unverified nested trivial ketiv/qere")
    if written == "אהלה":
        reading, helper = "אהלו", template_names.QAMATS_VARIANT
        provenance, subtype = "ל-קרי", 'כתיב ה"א בסיומת של חולם'
    else:
        reading, helper = pairs.get(written), "מ:דחי"
        provenance = "א-קרי"
        subtype = 'כתיב חסר יו"ד בסיומת של קמץ ואחריו וי"ו'
    if (
        set(params) != {"1", "2", "3", "מקורות", "סוג"}
        or reading is None
        or params["מקורות"] != provenance
        or params["סוג"] != subtype
    ):
        raise ValueError("Unverified nested trivial ketiv/qere")
    for key, expected in (("1", written), ("3", reading)):
        form = params[key]
        if not isinstance(form, dict) or form.get("tmpl_name") != helper:
            raise ValueError("Unverified nested trivial alternative storage")
        alternatives = template_names.validate_current_plus_template(form)
        for value in alternatives.values():
            if (
                not isinstance(value, str)
                or any(
                    ch.isspace() or ch == "\N{HEBREW PUNCTUATION MAQAF}" for ch in value
                )
                or letters_atoms(value) != (expected,)
            ):
                raise ValueError("Nested trivial form changed letters or boundary")
    return _body_text([params["1"]])


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


def _accepted_special_case(params, context, cases):
    """Validate a complete finite case and its selected Scripture address."""
    if context is None or context[0] not in cases:
        raise ValueError("Unverified special ketiv/qere Scripture reference")
    bcv, elements = context
    case = cases[bcv]
    selected = elements
    try:
        for key in case["path"]:
            selected = selected[key]
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError(
            "Accepted special ketiv/qere Scripture address changed"
        ) from error
    if (
        not isinstance(selected, dict)
        or selected.get("tmpl_name") != "מ:כו״ק מיוחד"
        or selected.get("tmpl_params") is not params
        or params["סוג"] != case["subtype"]
        or params["1"] != case["written"]
        or type(params["2"]) is not type(case["qere"])
        or params["2"] != case["qere"]
    ):
        raise ValueError("Unverified complete special ketiv/qere case")
    return bcv, elements, case


def _mid_compound_qere(params, context):
    """Retain the exact one-slot qere and both pointed compound partners."""
    _bcv, elements, case = _accepted_special_case(params, context, _MID_COMPOUND_KQ)
    index = case["path"][0]
    if index == 0 or index + 1 >= len(elements):
        raise ValueError("Mid-compound qere requires both literal partners")
    previous, following = elements[index - 1], elements[index + 1]
    if (
        not isinstance(previous, str)
        or not previous.split()
        or not previous.endswith(case["previous"])
        or previous.split()[-1] != case["previous"]
        or following != case["following"]
        or not isinstance(params["1"], str)
        or not isinstance(params["2"], str)
        or len(letters_atoms(params["1"])) != 1
        or len(letters_atoms(params["2"])) != 1
    ):
        raise ValueError("Unverified pointed mid-compound context or one-slot forms")
    return params["2"]


def _two_written_one_qere(params, context):
    """Select the exact scalar qere, with no invented protected source pair."""
    bcv, elements, case = _accepted_special_case(
        params, context, _TWO_WRITTEN_ONE_QERE_KQ
    )
    if bcv == ("Lamentations", 1, 6):
        index = case["path"][0]
        if (
            index + 1 >= len(elements)
            or not isinstance(elements[index + 1], str)
            or not elements[index + 1].startswith("צִיּ֖וֹן ")
        ):
            raise ValueError("Accepted one-qere external maqaf context changed")
    if (
        not isinstance(params["1"], str)
        or not isinstance(params["2"], str)
        or len(letters_atoms(params["1"])) != 2
        or len(letters_atoms(params["2"])) != 1
    ):
        raise ValueError("Accepted unequal case must remain two written/one qere")
    return params["2"]


def _additional_unequal_qere(params, context):
    """Read only a complete accepted pair at its named Scripture address."""
    bcv, elements, case = _accepted_special_case(
        params, context, _ADDITIONAL_UNEQUAL_KQ
    )
    if bcv in _EXTERNAL_UNEQUAL_MAQAF:
        previous_atom, following_atom = _EXTERNAL_UNEQUAL_MAQAF[bcv]
        index = case["path"][0]
        if index == 0 or index + 1 >= len(elements):
            raise ValueError("Unequal pair requires its outer compound partners")
        previous, following = elements[index - 1], elements[index + 1]
        if (
            not isinstance(previous, str)
            or not previous.split()
            or not previous.endswith(previous_atom)
            or previous.split()[-1] != previous_atom
            or not isinstance(following, str)
            or not following
            or (
                not following.startswith(following_atom + " ")
                if following_atom is not None
                else not following[0].isspace()
            )
        ):
            raise ValueError("Unequal pair external maqaf context changed")
    qere = _two_word_special_qere(params["2"])
    if len(letters_atoms(params["1"])) != 1 or len(letters_atoms(qere)) != 2:
        raise ValueError("Accepted unequal case must remain one written/two qere")
    return qere


def _verse_text(elements, *, protected=None, bcv=None):
    context = (bcv, elements)
    if bcv in {("Numbers", 10, 35), ("Numbers", 10, 36)} and len(elements) >= 2:
        sign_index, break_index = (0, 1) if bcv[2] == 35 else (-1, -2)
        wrapper = elements[sign_index]
        if isinstance(wrapper, dict) and wrapper.get("tmpl_name") == "נוסח":
            params = template_names.validate_current_plus_template(wrapper)
            sign = params["1"]
            if (
                isinstance(sign, dict)
                and sign.get("tmpl_name") == template_names.INVERTED_NUN
            ):
                sign_params = template_names.validate_current_plus_template(sign)
                neighbor = elements[break_index]
                if (
                    sign_params != {"1": "\N{HEBREW PUNCTUATION NUN HAFUKHA}"}
                    or not isinstance(neighbor, dict)
                    or neighbor.get("tmpl_name") != "ססס"
                ):
                    raise ValueError("Unverified Numbers inverted-nun sign or neighbor")
                break_params = template_names.validate_current_plus_template(neighbor)
                if not all(isinstance(value, str) for value in break_params.values()):
                    raise ValueError("Numbers sign neighbor requires string metadata")
                selected = list(elements)
                selected[sign_index] = sign_params["1"]
                rendered = _body_text(selected, protected=protected, context=context)
                if not letters_atoms(rendered):
                    raise ValueError("Numbers inverted nun requires Scripture")
                return rendered
    if (
        isinstance(elements, (list, tuple))
        and elements
        and isinstance(elements[0], dict)
        and elements[0].get("tmpl_name") == template_names.INVERTED_NUN
    ):
        params = template_names.validate_current_plus_template(elements[0])
        if params != {"1": "\u05c6 "}:
            raise ValueError("Unverified leading inverted-nun payload")
        rendered = _body_text(elements[1:], protected=protected, context=context)
        if not letters_atoms(rendered):
            raise ValueError("Leading inverted nun requires following Scripture")
        return rendered
    return _body_text(elements, protected=protected, context=context)


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


def _ordinary_special_written(form, reading):
    """Validate the accepted Job written styling without adding a qere shape."""
    params = template_names.validate_current_plus_template(form)
    children = params["1"]
    if (
        not isinstance(children, list)
        or len(children) != 3
        or not isinstance(children[1], dict)
        or children[1].get("tmpl_name") != "מ:אות-ק"
        or tuple(params[key] for key in ("3", "4", "5")) != (".ג..", "ק", "ג/ק")
    ):
        raise ValueError("Unverified ordinary written special-letter storage")
    marked = template_names.validate_current_plus_template(children[1])["1"]
    for value, expected in (
        (children[0], "ו"),
        (marked, "ג"),
        (children[2], "יש"),
        (reading, "וגוש"),
    ):
        if (
            not isinstance(value, str)
            or _consonantal_layout(value) != expected
            or any(
                not (
                    "א" <= char <= "ת"
                    or char == "\N{COMBINING GRAPHEME JOINER}"
                    or (
                        0x0591 <= ord(char) <= 0x05C9
                        and (
                            unicodedata.category(char) == "Mn"
                            or ord(char) in (0x05C8, 0x05C9)
                        )
                    )
                )
                for char in value
            )
        ):
            raise ValueError(
                "Ordinary written styling changed its guarded one-slot forms"
            )
    return _body_text([form])


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


def _target_text(target, *, protected=None, context=None):
    if isinstance(target, (str, dict)):
        return _body_text([target], protected=protected, context=context)
    if isinstance(target, (list, tuple)):
        return _body_text(target, protected=protected, context=context)
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
        verses[cv] = letters_atoms(
            _verse_text(minirow.EP, protected=protected, bcv=(bkid, *cv))
        )
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
