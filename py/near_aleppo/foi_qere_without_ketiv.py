"""Encoding choices and manuscript readings beside current MAM and NAEE text.

The shared renderer supplies Scripture and MAM notes. The existing closed
dataset walk validates current qere-only source fragments, excluding note bodies
and copied MAM lemmas. Authored intended encodings are documentation, not changes
to the dataset's policy or its current source.
"""

import json
import re
import struct
from pathlib import Path

from hkq_cmn import uxlc_external_links
from mb_cmn import bib_locales as tbn
from mb_cmn import provenance
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import verse_external_links as vel
from mb_misc import mb_html
from mwd import mwd_write_book
from near_aleppo import build_paths, doc_figures
from near_aleppo.phase2_templates import (
    MARKS_WITHOUT_LETTER,
    MARKS_WITHOUT_LETTER_OR_SPACE,
)
from py_misc import mam_doc_utils, mwd_utils
from py_misc import ren_html_for_renel as hfr
from py_misc import ren_html_from_ren_el_mapping as hfrm
from render_wt import render_element as renel
from render_wt import render_wikitext as rwt

PAGE = "foi/qere-without-ketiv.html"
TITLE = "Qere without ketiv in near-Aleppo"
_FORMAT = "near-aleppo-qere-without-ketiv-readings-v3"
_QERE_TAG = "mam-kq-q-velo-k"
_QERE_TEMPLATE = "קרי ולא כתיב"
_NOTE_REVIEW_FORMAT = "near-aleppo-qere-without-ketiv-mam-notes-en-v2"
_COMPARISON_LABELS = {
    "discrepancy": "Discrepancy",
}
_ADDITIONAL_TEMPLATES = {
    "marks-with-space": MARKS_WITHOUT_LETTER,
    "marks-without-space": MARKS_WITHOUT_LETTER_OR_SPACE,
    "space-without-marks": None,
}
_SUMMARY_PRESENCE = {
    "marks-with-space": ("+", "+"),
    "marks-without-space": ("+", "−"),
    "space-without-marks": ("−", "+"),
}
_LINE_POSITIONS = {
    "between written words": "BW",
    "end of a manuscript line": "EOL",
}
_HEBREW = re.compile(r"([\u0590-\u05ff]+)")
# Match the mark classification in accgram/almost_errors_html_shared.py.
# Maqaf, paseq and sof pasuq are spacing punctuation, not pointing.
_HEBREW_MARK = re.compile(r"[\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7-\u05c9]")


def records():
    """Load the maintained selection and observations, without population pins."""
    path = build_paths.input_dir() / "qere-without-ketiv-readings.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if set(data) != {"format", "cases"} or data["format"] != _FORMAT:
        raise ValueError(f"Unexpected qere-without-ketiv record format: {path}")
    rows = data["cases"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("The qere-without-ketiv study requires case records")
    identifiers, references = set(), set()
    for row in rows:
        if set(row) != {
            "id",
            "reference",
            "intended_encoding",
            "reading",
            "observation",
            "romanized",
            "documentation_notes",
            "crop",
        }:
            raise ValueError(f"Unexpected study record fields: {row}")
        identity, reference = row["id"], tuple(row["reference"])
        if not isinstance(identity, str) or not re.fullmatch(
            r"[A-Za-z0-9-]+", identity
        ):
            raise ValueError(f"Invalid study identifier: {identity!r}")
        if (
            len(reference) != 3
            or reference[0] not in tbn.ALL_BK39_IDS
            or any(type(number) is not int or number < 1 for number in reference[1:])
            or identity in identifiers
            or reference in references
        ):
            raise ValueError(f"Invalid or duplicate study reference: {reference}")
        identifiers.add(identity)
        references.add(reference)
        if row["reading"] is None:
            if row["observation"] is not None or row["crop"] is not None:
                raise ValueError(
                    f"Unreviewed case has an image observation: {identity}"
                )
        elif (
            not isinstance(row["reading"], dict)
            or not isinstance(row["reading"].get("qere"), str)
            or (
                row["observation"] is not None
                and (not isinstance(row["observation"], str) or not row["observation"])
            )
        ):
            raise ValueError(f"Incomplete image reading: {identity}")
        if (
            row["reading"] is not None
            and row["reading"].get("line_position") not in _LINE_POSITIONS
        ):
            raise ValueError(f"Invalid or missing line position: {identity}")
        intended = row["intended_encoding"]
        if intended is None:
            if row["reading"] is not None:
                raise ValueError(
                    f"Reviewed case lacks an encoding assessment: {identity}"
                )
        elif (
            row["reading"] is None
            or not isinstance(intended, dict)
            or set(intended) != {"kind", "explanation"}
            or intended["kind"] not in _ADDITIONAL_TEMPLATES
            or not isinstance(intended["explanation"], str)
            or not intended["explanation"]
        ):
            raise ValueError(f"Invalid intended encoding: {identity}")
        for key in ("romanized", "documentation_notes"):
            if not isinstance(row[key], list) or not all(
                isinstance(value, str) and value for value in row[key]
            ):
                raise ValueError(f"Invalid {key}: {identity}")
        crop = row["crop"]
        if crop is not None:
            _validate_crop(crop, identity, allow_marginal_note=True)
        _inferred_marginal_lines(row)
    return rows


def _inferred_marginal_lines(row):
    """Read the explicitly recorded, inferred vertical layout of a marginal note."""
    reading = row["reading"]
    if reading is None or "marginal_qere_note" not in reading:
        return None
    note = reading["marginal_qere_note"]
    if not isinstance(note, dict):
        raise ValueError(f"Invalid marginal qere note: {row['id']}")
    lines = note.get("inferred_lines")
    if (
        not isinstance(lines, list)
        or not lines
        or not all(
            isinstance(line, str) and line and "\n" not in line and "\r" not in line
            for line in lines
        )
    ):
        raise ValueError(f"Invalid inferred marginal lines: {row['id']}")
    return lines


def _validate_crop(crop, identity, *, allow_marginal_note):
    """Validate a body crop and its optional, explicitly named marginal crop."""
    fields = {"filename", "source_screenshot"}
    shapes = (
        (fields, fields | {"marginal_qere_note"}) if allow_marginal_note else (fields,)
    )
    if (
        not isinstance(crop, dict)
        or set(crop) not in shapes
        or not isinstance(crop["filename"], str)
        or not re.fullmatch(r"[A-Za-z0-9._-]+\.png", crop["filename"])
        or not isinstance(crop["source_screenshot"], str)
    ):
        raise ValueError(f"Invalid crop record: {identity}")
    if allow_marginal_note and "marginal_qere_note" in crop:
        _validate_crop(crop["marginal_qere_note"], identity, allow_marginal_note=False)


def _qere_nodes(value):
    """Select a semantic render tag from the rendered Scripture or note lemma."""
    if isinstance(value, str):
        return []
    if isinstance(value, (tuple, list)):
        return [node for child in value for node in _qere_nodes(child)]
    if renel.get_ren_el_tag(value) == _QERE_TAG:
        return [value]
    return _qere_nodes(renel.get_ren_el_contents(value) or ())


def _text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, (tuple, list)):
        return "".join(_text(child) for child in value)
    return _text(renel.get_ren_el_contents(value) or ())


def mam_examples(rows):
    """Render current qere and its attached MAM notes with existing dispatch."""
    bkids = tuple(dict.fromkeys(row["reference"][0] for row in rows))
    books = plus.read_parsed_plus_bk39s(
        bkids, str(build_paths.mam_parsed_plus_dir().parent)
    )
    ctx = hfr.HfrCtx(hfrm.HT_TAC_FOR_RT_FOR_MAM_WITH_DOC)
    rendered = {
        book: rwt.render(book, books, mwd_write_book.RENOPTS_MAM_WITH_DOC, {})
        for book in bkids
    }
    result = {}
    for row in rows:
        book, chapter, verse = row["reference"]
        bcvt = tbn.mk_bcvtmam(book, chapter, verse)
        veraf = rendered[book][bcvt]
        qeres = _qere_nodes(veraf.verse)
        if len(qeres) != 1:
            raise ValueError(
                f"Study reference requires one qere-only reading: {row['reference']}"
            )
        qere_text = _text(renel.get_ren_el_contents(qeres[0]))
        # MAM-with-doc's concrete qere display adds one pair of square brackets.
        if qere_text.startswith("[") and qere_text.endswith("]"):
            qere_text = qere_text[1:-1]
        reading = row["reading"]
        if reading is not None and reading["qere"] != qere_text:
            raise ValueError(
                f"Reconcile the image reading's whole qere at {row['reference']}: "
                f"recorded {reading['qere']!r}, current MAM {qere_text!r}"
            )
        docs = veraf.map_over(mam_doc_utils.extract_docs).map_over(
            lambda notes: tuple(
                note for note in notes if _qere_nodes(note["doc_lemma"])
            )
        )
        nondoc = veraf.map_over(mam_doc_utils.mark_doc_targets)
        ver_ndd = mwd_utils.VerseNdd(bcvt, nondoc, docs)
        note_html = mwd_utils._html_for_docs(
            mwd_utils._DocCtx(book, ctx, ver_ndd),
            mwd_utils._DocType.SELF_CONTAINED,
        ).verse
        result[tuple(row["reference"])] = {
            "qere": qere_text,
            "notes": note_html,
            "note_sources": [
                {
                    "lemma": _text(note["doc_lemma"]),
                    "parts": [_text(part) for part in note["doc_parts"]],
                }
                for note in docs.verse
            ],
        }
    return result


def _validate_near_aleppo_encodings(rows, examples):
    """Validate one current Scripture fragment per case through the closed walk."""
    bkids = tuple(dict.fromkeys(row["reference"][0] for row in rows))
    books = plus.read_parsed_plus_bk39s(bkids, str(build_paths.dataset_dir().parent))
    for row in rows:
        reference = tuple(row["reference"])
        book, chapter, verse = reference
        bcvt = tbn.mk_bcvtmam(book, chapter, verse)
        scripture = books[book]["verses_plus"][bcvt].EP
        matches = [
            template
            for _, template in doc_figures._templates(
                list(scripture), reference, doc_figures._DATASET
            )
            if template["tmpl_name"] == _QERE_TEMPLATE
        ]
        if len(matches) != 1:
            raise ValueError(f"Expected one current qere-only encoding: {reference}")
        (template,) = matches
        params = template.get("tmpl_params")
        if (
            set(template) != {"tmpl_name", "tmpl_params"}
            or not isinstance(params, dict)
            or set(params) != {"1", "2"}
            or not all(isinstance(value, str) and value for value in params.values())
        ):
            raise ValueError(f"Unexpected qere-only source shape: {reference}")
        if params["2"] != examples[reference]["qere"]:
            raise ValueError(f"Reconcile the dataset's whole qere: {reference}")


def _mam_note_reviews(rows, examples):
    """Reconcile translations and explanations with their whole note and description."""
    path = build_paths.input_dir() / "qere-without-ketiv-mam-notes-en.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if set(data) != {"format", "cases"} or data["format"] != _NOTE_REVIEW_FORMAT:
        raise ValueError(f"Unexpected MAM note review format: {path}")
    reviews = data["cases"]
    if not isinstance(reviews, list) or not reviews:
        raise ValueError("The study requires MAM note reviews")
    result = {}
    for review in reviews:
        if not isinstance(review, dict) or set(review) != {
            "id",
            "source_description",
            "notes",
            "comparison",
        }:
            raise ValueError(f"Invalid MAM note review: {review}")
        identity = review["id"]
        if not isinstance(identity, str) or identity in result:
            raise ValueError(f"Invalid or duplicate MAM note review: {identity}")
        result[identity] = review
        comparison = review["comparison"]
        if comparison is not None and (
            not isinstance(comparison, dict)
            or set(comparison) != {"status", "text"}
            or comparison["status"] not in _COMPARISON_LABELS
            or not isinstance(comparison["text"], str)
            or not comparison["text"]
        ):
            raise ValueError(f"Invalid MAM comparison: {identity}")
        if not isinstance(review["notes"], list):
            raise ValueError(f"Invalid MAM notes: {identity}")
        for note in review["notes"]:
            if not isinstance(note, dict) or set(note) != {"source", "translation"}:
                raise ValueError(f"Invalid translated MAM note: {identity}")
            source, translation = note["source"], note["translation"]
            if (
                not isinstance(source, dict)
                or set(source) != {"lemma", "parts"}
                or not isinstance(source["lemma"], str)
                or not isinstance(source["parts"], list)
                or not source["parts"]
                or not all(isinstance(part, str) for part in source["parts"])
                or not isinstance(translation, list)
                or len(translation) != len(source["parts"])
            ):
                raise ValueError(f"Incomplete translated MAM note: {identity}")
            for part in translation:
                if not isinstance(part, list) or not part:
                    raise ValueError(f"Empty translated MAM note part: {identity}")
                for block in part:
                    if (
                        not isinstance(block, dict)
                        or set(block) != {"kind", "text"}
                        or block["kind"] not in {"prose", "hebrew"}
                        or not isinstance(block["text"], str)
                        or not block["text"]
                    ):
                        raise ValueError(f"Invalid MAM translation block: {identity}")
    if set(result) != {row["id"] for row in rows}:
        raise ValueError("Reconcile MAM note reviews with the study selection")
    for row in rows:
        identity = row["id"]
        review = result[identity]
        source = examples[tuple(row["reference"])]["note_sources"]
        if [note["source"] for note in review["notes"]] != source:
            raise ValueError(f"Reconcile the whole translated MAM note at {identity}")
        description = (
            {
                "observation": row["observation"],
                "documentation_notes": row["documentation_notes"],
            }
            if source
            else None
        )
        if review["source_description"] != description:
            raise ValueError(
                f"Reconcile the MAM comparison with the manuscript description at {identity}"
            )
        if not source:
            if review["comparison"] is not None:
                raise ValueError(f"MAM comparison without an attached note: {identity}")
            if row["reading"] is not None and row["observation"] is None:
                raise ValueError(
                    f"Image reading without manuscript remarks: {identity}"
                )
    return result


def _translation_blocks(blocks, names):
    result = []
    for block in blocks:
        if block["kind"] == "prose":
            result.append(mb_html.para(_prose(block["text"], names)))
        elif block["kind"] == "hebrew":
            result.append(
                mb_html.para(
                    block["text"],
                    {
                        "dir": "rtl",
                        "lang": "hbo",
                        "class": "pointed qvlk-hebrew-display",
                    },
                )
            )
        else:
            raise ValueError(f"Unknown MAM translation block: {block['kind']}")
    return result


def _english_note(review, names):
    contents = [
        mb_html.heading_level_3(
            "English translation and explanation of the MAM doc-note"
        )
    ]
    for note in review["notes"]:
        parts = note["translation"]
        contents.extend(_translation_blocks(parts[0], names))
        if len(parts) > 1:
            contents.append(
                mb_html.unordered_list(
                    [_translation_blocks(part, names) for part in parts[1:]]
                )
            )
    return mb_html.div(contents, {"class": "qvlk-mam-english"})


def _comparison(review, names):
    comparison = review["comparison"]
    return mb_html.div(
        [
            mb_html.heading_level_3("Comparison with MAM"),
            mb_html.para(
                [
                    mb_html.bold(_COMPARISON_LABELS[comparison["status"]] + ":"),
                    " ",
                    *_prose(comparison["text"], names),
                ]
            ),
        ],
        {"class": "qvlk-mam-comparison"},
    )


def _comparison_summary(rows, reviews):
    differences = []
    for row in rows:
        comparison = reviews[row["id"]]["comparison"]
        if comparison is not None:
            differences.append(
                [
                    mb_html.anchor_h(
                        _reference_text(row["reference"]), "#" + row["id"]
                    ),
                    " — ",
                    *_prose(comparison["text"], row["romanized"]),
                ]
            )
    if not differences:
        return []
    return [
        mb_html.div(
            [
                mb_html.heading_level_2("Discrepancies with MAM"),
                mb_html.unordered_list(differences),
            ],
            {"class": "qvlk-mam-summary"},
        )
    ]


def _template_name(name):
    return mb_html.bdi(name, {"dir": "rtl", "lang": "hbo", "class": "name"})


def _naee_excerpt(scripture, qere, reference):
    """Keep the QVLK's complete chanted word and neighboring chanted words.

    Project only plain Scripture and the recognized documentation-target spans.
    The validated QVLK box is opaque: its editorial label and ruby annotation
    do not create chanted word boundaries. Slice original nodes without retyping marks.
    """
    marker = "\N{OBJECT REPLACEMENT CHARACTER}"

    def projection(value):
        if isinstance(value, str):
            if marker in value:
                raise ValueError(f"Excerpt marker occurs in Scripture: {reference}")
            return value
        if isinstance(value, (tuple, list)):
            return "".join(projection(child) for child in value)
        if not isinstance(value, dict) or mb_html.htel_get_tag(value) != "span":
            raise ValueError(f"Unsupported excerpt element: {reference}")
        role = value.get("attr", {}).get("class")
        contents = value.get("contents") or ()
        if role == "mam-doc-target-without-callout":
            return projection(contents)
        if role != "near-aleppo-kq-box" or len(contents) != 1:
            raise ValueError(f"Unsupported excerpt span role: {reference}: {role}")
        ruby = contents[0]
        if not isinstance(ruby, dict) or mb_html.htel_get_tag(ruby) != "ruby":
            raise ValueError(f"Excerpt box is not a ruby: {reference}")
        parts = ruby.get("contents") or ()
        if (
            len(parts) != 4
            or any(not isinstance(part, dict) for part in parts)
            or [mb_html.htel_get_tag(part) for part in parts]
            != ["span", "rp", "rt", "rp"]
            or parts[0].get("attr", {}).get("class") != "near-aleppo-kq-none"
        ):
            raise ValueError(f"Excerpt requires a qere-only ruby: {reference}")
        annotation = parts[2].get("contents") or ()
        if (
            len(annotation) != 1
            or not isinstance(annotation[0], dict)
            or mb_html.htel_get_tag(annotation[0]) != "span"
            or annotation[0].get("attr", {}).get("class") != "mam-kq-q"
            or annotation[0].get("contents") != [qere]
            or re.search(r"\s", qere)
        ):
            raise ValueError(f"Reconcile the excerpt's whole qere: {reference}")
        return marker

    def cut(value, start, end):
        text = projection(value)
        if end <= 0 or start >= len(text):
            return []
        if start <= 0 and end >= len(text):
            return value
        if isinstance(value, str):
            return value[max(0, start) : end]
        if isinstance(value, (tuple, list)):
            result, offset = [], 0
            for child in value:
                part = cut(child, start - offset, end - offset)
                if part != [] and part != "":
                    result.append(part)
                offset += len(projection(child))
            return result
        if value["attr"]["class"] != "mam-doc-target-without-callout":
            raise ValueError(f"Excerpt cuts through the QVLK box: {reference}")
        return {**value, "contents": cut(value["contents"], start, end)}

    text = projection(scripture)
    if text.count(marker) != 1:
        raise ValueError(f"Excerpt requires one QVLK: {reference}")
    words = [
        match
        for match in re.finditer(r"\S+", text)
        if marker in match.group() or re.search(r"[\u05d0-\u05ea]", match.group())
    ]
    target = next(index for index, word in enumerate(words) if marker in word.group())
    if target == 0:
        before, after = 0, 2
    elif target == len(words) - 1:
        before, after = 2, 0
    else:
        before, after = 1, 1
    first = max(0, target - before)
    last = min(len(words) - 1, target + after)
    start = words[first].start()
    # Retain punctuation following the final selected chanted word, including
    # a separately spaced paseq glyph. Punctuation is not another chanted word.
    end = words[last + 1].start() if last + 1 < len(words) else len(text)
    while end > start and text[end - 1].isspace():
        end -= 1
    return [
        "… " if text[:start].strip() else "",
        cut(scripture, start, end),
        " …" if text[end:].strip() else "",
    ]


def _case_summary(rows):
    """Summarize recorded body-text features with explicit presence and position roles."""
    header = mb_html.table_row(
        [
            mb_html.table_header("Verse", {"scope": "col"}),
            mb_html.table_header(
                mb_html.abbr("N", {"title": "Niqqud in the body text"}),
                {"scope": "col"},
            ),
            mb_html.table_header(
                mb_html.abbr("H", {"title": "Horizontal space in the line of letters"}),
                {"scope": "col"},
            ),
            mb_html.table_header(
                mb_html.abbr("Pos.", {"title": "Position in the manuscript line"}),
                {"scope": "col"},
            ),
        ]
    )
    table_rows = []
    for row in rows:
        intended = row["intended_encoding"]
        if intended is None:
            niqqud, space, position = "?", "?", "?"
        else:
            niqqud, space = _SUMMARY_PRESENCE[intended["kind"]]
            line_position = row["reading"]["line_position"]
            position = mb_html.abbr(
                _LINE_POSITIONS[line_position], {"title": line_position}
            )
        table_rows.append(
            mb_html.table_row(
                [
                    mb_html.table_header(
                        mb_html.anchor_h(
                            _reference_text(row["reference"]), "#" + row["id"]
                        ),
                        {"scope": "row"},
                    ),
                    mb_html.table_datum(niqqud),
                    mb_html.table_datum(space),
                    mb_html.table_datum(position),
                ]
            )
        )
    legend = (
        'The "N" column records whether any niqqud are present in the body text. '
        'The "H" column records whether horizontal space is present in the line of letters, '
        "with or without niqqud in or under that space. A plus sign (+) means "
        'present, and a minus sign (−) means absent. The "Pos." column records position: '
        "BW means between written words, and EOL means at the end of a manuscript line."
    )
    if any(row["reading"] is None for row in rows):
        legend += " A question mark (?) means that a reading has not yet been recorded."
    return [
        mb_html.heading_level_2("Case summary"),
        mb_html.div(
            mb_html.table(
                [header, *table_rows],
                {
                    "class": "qvlk-case-summary",
                    "aria-label": "Case summary",
                    "aria-describedby": "qvlk-summary-key",
                },
            ),
            {"class": "table-wrap"},
        ),
        mb_html.para(legend, {"id": "qvlk-summary-key", "class": "qvlk-summary-key"}),
    ]


def _encoding_guide():
    return mb_html.div(
        [
            mb_html.heading_level_2("Encoding conventions"),
            mb_html.para(
                [
                    "The intended encoding retains each ",
                    _template_name(_QERE_TEMPLATE),
                    " call and its qere, and supplements that call with one "
                    "additional template describing the body text. The "
                    "additional template records which niqqud, if any, are present and whether "
                    "horizontal space is present. The cases below require "
                    "three kinds of additional template:",
                ]
            ),
            mb_html.unordered_list(
                [
                    [
                        "For niqqud with horizontal space above the marks, a candidate is ",
                        _template_name(MARKS_WITHOUT_LETTER),
                        " (niqqud without a letter).",
                    ],
                    [
                        "For niqqud without horizontal space above the marks, a candidate is ",
                        _template_name(MARKS_WITHOUT_LETTER_OR_SPACE),
                        " (niqqud without a letter and without space).",
                    ],
                    "Horizontal space without niqqud requires an additional template whose "
                    "name and syntax remain open.",
                ]
            ),
            mb_html.para(
                "The phrase “space above the marks” means horizontal space "
                "in the line of letters, left between words or at the end of a "
                "manuscript line. At a line ending, that horizontal space may "
                "have been left on purpose or may be accidental. The end-of-line "
                "cases here are Judges 20:13 and Ruth 3:17. None of the cases "
                "discussed here is at the start of a manuscript line."
            ),
            mb_html.para(
                _prose(
                    "The existing niqqud templates are specific to near-Aleppo. Their payloads use "
                    "artificial carrier letters to hold the marks; those carriers "
                    "are not written manuscript letters. The carrier can be alef, "
                    "vav, or, rarely, dalet. The carrier payload for 2 Kings 19:31 "
                    "remains unsettled because the ḥolam male reading is tentative.",
                    ("ḥolam male",),
                )
            ),
            mb_html.para(
                [
                    "Current status: every site below uses the ",
                    _template_name(_QERE_TEMPLATE),
                    " template and will continue to do so. No additional template is applied "
                    "at these sites yet. The additional templates' exact names, "
                    "parameter shapes and call placement remain to be designed. "
                    "Intended additional templates are labelled pending, separately "
                    "from the current encoding.",
                ]
            ),
        ],
        {"class": "qvlk-encoding-guide"},
    )


def _encoding(row):
    intended = row["intended_encoding"]
    if intended is None:
        intention = [
            mb_html.bold("Intended additional template — assessment open:"),
            " ",
            "A manuscript-based encoding assessment has not yet been recorded.",
        ]
    else:
        name = _ADDITIONAL_TEMPLATES[intended["kind"]]
        intention = [
            mb_html.bold("Intended additional template — pending:"),
            " ",
            (
                ["The proposed additional template is ", _template_name(name)]
                if name is not None
                else "The additional template for horizontal space without niqqud has not yet been named"
            ),
            ". ",
            *_prose(intended["explanation"], row["romanized"]),
        ]
    return mb_html.div(
        [
            mb_html.heading_level_3("Near-Aleppo encoding"),
            mb_html.para(
                [
                    mb_html.bold("Current encoding — implemented:"),
                    " The dataset uses ",
                    _template_name(_QERE_TEMPLATE),
                    ".",
                ]
            ),
            mb_html.para(intention),
        ],
        {"class": "qvlk-encoding"},
    )


def _prose(text, names=()):
    """Isolate Hebrew runs, style marked runs and italicize named romanizations."""
    parts = [text]
    if names:
        pattern = r"(?<!\w)(" + "|".join(re.escape(name) for name in names) + r")(?!\w)"
        parts = re.split(pattern, text)
    result = []
    for part in parts:
        if part in names:
            result.append(mb_html.span(part, {"class": "romanized"}))
        else:
            result.extend(
                (
                    mb_html.bdi(
                        run,
                        {
                            "lang": "hbo",
                            "dir": "rtl",
                            **(
                                {"class": "pointed"} if _HEBREW_MARK.search(run) else {}
                            ),
                        },
                    )
                    if _HEBREW.fullmatch(run)
                    else run
                )
                for run in _HEBREW.split(part)
                if run
            )
    return result


def _reference_text(reference):
    book, chapter, verse = reference
    return f"{uxlc_external_links.book_display_name(book)} {chapter}:{verse}"


def _links(reference):
    labels = {
        "mgketer": "mgketer.org",
        "MwD": "MAM verse and notes",
        "tica": "masoretica-aleppo",
    }
    result = []
    for link in vel.verse_links(*reference):
        if link.label in labels:
            if result:
                result.append(" · ")
            result.append(mb_html.anchor_h(labels[link.label], link.href))
    return mb_html.para(result)


def _crop(crop, reference, outputs, *, label=None):
    filename = crop["filename"]
    raw = (build_paths.asset_dir() / "qere-without-ketiv" / filename).read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Study crop is not PNG: {filename}")
    width, height = struct.unpack(">II", raw[16:24])
    outputs["img/qere-without-ketiv/" + filename] = raw
    subject = label or "the qere-without-ketiv site"
    caption = (
        f"This Aleppo Codex image shows the {label or 'body text'} "
        f"at {_reference_text(reference)}."
    )
    return [
        mb_html.para(
            mb_html.img(
                {
                    "src": "../img/qere-without-ketiv/" + filename,
                    "alt": f"Aleppo Codex crop at {_reference_text(reference)}: {subject}",
                    "width": str(width),
                    "height": str(height),
                    "class": "qvlk-crop",
                }
            )
        ),
        mb_html.para(
            caption,
            {"class": "qvlk-caption"},
        ),
    ]


def render(verses, rows):
    """Return the study page and unchanged crop bytes owned by the HTML build."""
    examples = mam_examples(rows)
    _validate_near_aleppo_encodings(rows, examples)
    reviews = _mam_note_reviews(rows, examples)
    outputs = {}
    body = [
        mb_html.heading_level_1(TITLE),
        mb_html.para(
            [
                mb_html.anchor_h("Features of interest", "index.html"),
                " · ",
                mb_html.anchor_h(
                    "Interesting ketiv/qere cases", "interesting-ketiv-qere.html"
                ),
                " · ",
                mb_html.anchor_h("NAEE book links", "../edition/index.html"),
            ]
        ),
        mb_html.para(
            [
                "Every case of ",
                _template_name(_QERE_TEMPLATE),
                " discussed here has a marginal note containing the qere letters. "
                "As expected, by definition, neither qere nor ketiv letters are "
                "present in the body text. The cases differ in whether, in the body text:",
            ]
        ),
        mb_html.unordered_list(
            [
                "niqqud marks are present (only four of the nine cases have niqqud)",
                "horizontal space is present (only 1 case lacks it: 2 Samuel 18:20)",
                "a masorah circle is present (only 1 case lacks it: 2 Kings 19:31)",
            ]
        ),
        mb_html.para(
            '(By definition, when niqqud marks are present, these are "orphan" niqqud, '
            "i.e. letterless niqqud.)"
        ),
        mb_html.para(
            [
                "For each case of ",
                _template_name(_QERE_TEMPLATE),
                ", we show the following:",
            ]
        ),
        mb_html.unordered_list(
            [
                "Aleppo images of the case.",
                "How the case looks in the near-Aleppo example edition (NAEE).",
                "Any MAM notes about the case.",
            ]
        ),
        mb_html.para(
            [
                "We present the MAM notes not only in their original Hebrew but also "
                "in English translation. This translation also makes the original "
                "notes' abbreviated wording more explicit. Sometimes it is not clear "
                'what a note means when it says, for example "',
                mb_html.bdi("=ל-קרי", {"dir": "rtl", "lang": "hbo"}),
                '". We translate that as "MAM\'s qere agrees with the qere implied '
                'by the Leningrad Codex." But it would be more conservative to say '
                '"is consistent with" rather than the stronger "agrees", i.e. it '
                "would be more conservative to say \"MAM's qere is consistent with "
                "the qere implied by the [body niqqud (if any) and marginal qere "
                'letters] of the Leningrad Codex."',
            ]
        ),
        *_comparison_summary(rows, reviews),
        _encoding_guide(),
        *_case_summary(rows),
    ]
    for row in rows:
        reference = tuple(row["reference"])
        example = examples[reference]
        review = reviews[row["id"]]
        contents = [
            mb_html.heading_level_2(
                mb_html.anchor_h(
                    _reference_text(reference), "../" + vel.near_aleppo_href(*reference)
                )
            ),
        ]
        if row["crop"]:
            crop = row["crop"]
            if "marginal_qere_note" in crop:
                contents.extend(_crop(crop, reference, outputs, label="body text"))
                contents.extend(
                    _crop(
                        crop["marginal_qere_note"],
                        reference,
                        outputs,
                        label="marginal qere note",
                    )
                )
            else:
                contents.extend(_crop(crop, reference, outputs))
        contents.extend(
            [
                _encoding(row),
                mb_html.heading_level_3("NAEE excerpt"),
                mb_html.para(
                    _naee_excerpt(verses[reference], example["qere"], reference),
                    {
                        "dir": "rtl",
                        "lang": "hbo",
                        "class": "pointed foi-verse qvlk-hebrew-display",
                    },
                ),
                mb_html.heading_level_3("MAM doc-note"),
            ]
        )
        if example["notes"]:
            contents.append(
                mb_html.div(
                    example["notes"],
                    {"dir": "rtl", "lang": "hbo", "class": "pointed qvlk-notes"},
                )
            )
        else:
            contents.append(
                mb_html.para(
                    "MAM has no doc-note attached to this qere-without-ketiv site."
                )
            )
        if review["notes"]:
            contents.append(_english_note(review, row["romanized"]))
        marginal_lines = _inferred_marginal_lines(row)
        if (
            row["reading"] is None
            or row["observation"] is not None
            or row["documentation_notes"]
            or marginal_lines is not None
        ):
            contents.append(
                mb_html.heading_level_3(
                    "Additional manuscript remarks"
                    if review["notes"]
                    else "Aleppo manuscript reading"
                )
            )
        if row["reading"] is None:
            contents.append(
                mb_html.para(
                    "An image reading has not yet been recorded for this entry."
                )
            )
        else:
            if row["observation"] is not None:
                contents.append(
                    mb_html.para(_prose(row["observation"], row["romanized"]))
                )
            contents.extend(
                mb_html.para(_prose(note)) for note in row["documentation_notes"]
            )
            if marginal_lines is not None:
                contents.append(
                    mb_html.para(
                        "The marginal qere note is inferred to have one word per line:"
                    )
                )
                contents.append(
                    mb_html.div(
                        [mb_html.div(line) for line in marginal_lines],
                        {
                            "dir": "rtl",
                            "lang": "hbo",
                            "class": "pointed qvlk-marginal-lines",
                            "style": "width: fit-content;",
                        },
                    )
                )
        if review["comparison"] is not None:
            contents.append(_comparison(review, row["romanized"]))
        contents.append(_links(reference))
        body.append(mb_html.div(contents, {"id": row["id"], "class": "qvlk-case"}))
    ctx = mb_html.WriteCtx(
        TITLE,
        PAGE,
        css_hrefs=(
            "../../document.css",
            "../../MAM-parsed/style.css",
            "../style.css",
            "../edition/ketiv-qere.css",
        ),
        html_comment=provenance.generated_html_comment(__file__),
        body_class="qvlk-study",
        head_style=Path(__file__).with_suffix(".css").read_text(encoding="utf-8"),
    )
    outputs[PAGE] = mb_html.html_text(body, ctx).encode("utf-8")
    return outputs
