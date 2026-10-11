"""Encoding choices and manuscript readings beside current MAM and NAEE text.

The shared renderer supplies Scripture and MAM notes. The existing closed
dataset walk selects current qere-only source fragments, excluding note bodies
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
_FORMAT = "near-aleppo-qere-without-ketiv-readings-v2"
_QERE_TAG = "mam-kq-q-velo-k"
_QERE_TEMPLATE = "קרי ולא כתיב"
_NOTE_REVIEW_FORMAT = "near-aleppo-qere-without-ketiv-mam-notes-en-v1"
_COMPARISON_LABELS = {
    "discrepancy": "Apparent discrepancy",
    "agreement": "Agreement",
    "no-note": "No attached MAM note",
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
            or not isinstance(row["observation"], str)
            or not row["observation"]
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
            "qere_html": hfr.html_for_ren_el(ctx, qeres[0]),
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


def _near_aleppo_encodings(rows, examples):
    """Read one current Scripture fragment per case through the closed walk."""
    bkids = tuple(dict.fromkeys(row["reference"][0] for row in rows))
    books = plus.read_parsed_plus_bk39s(bkids, str(build_paths.dataset_dir().parent))
    result = {}
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
        # Both parameters are literal text. Preserve their complete source values;
        # the HTML writer escapes this string as text, not raw markup.
        result[reference] = (
            "{{" + _QERE_TEMPLATE + "|" + params["1"] + "|" + params["2"] + "}}"
        )
    return result


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
        if (
            not isinstance(comparison, dict)
            or set(comparison) != {"status", "text"}
            or comparison["status"] not in _COMPARISON_LABELS
            or not isinstance(comparison["text"], str)
            or not comparison["text"]
            or not isinstance(review["notes"], list)
        ):
            raise ValueError(f"Invalid MAM comparison: {identity}")
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
        if (review["comparison"]["status"] == "no-note") != (not source):
            raise ValueError(f"Invalid MAM note availability assessment: {identity}")
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
        if comparison["status"] == "discrepancy":
            differences.append(
                [
                    mb_html.anchor_h(
                        _reference_text(row["reference"]), "#" + row["id"]
                    ),
                    " — ",
                    *_prose(comparison["text"], row["romanized"]),
                ]
            )
    return mb_html.div(
        [
            mb_html.heading_level_2("Apparent discrepancies with MAM"),
            (
                mb_html.unordered_list(differences)
                if differences
                else mb_html.para(
                    "No apparent discrepancy is recorded in the comparisons below."
                )
            ),
        ],
        {"class": "qvlk-mam-summary"},
    )


def _template_name(name):
    return mb_html.bdi(name, {"dir": "rtl", "lang": "hbo", "class": "name"})


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
        "N records whether any niqqud are present in the body text. "
        "H records whether horizontal space is present in the line of letters, "
        "with or without niqqud in or under that space. A plus sign (+) means "
        "present, and a minus sign (−) means absent. Pos. records position: "
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
                    "Current status: every site below uses ",
                    _template_name(_QERE_TEMPLATE),
                    " and will continue to do so. No additional template is applied "
                    "at these sites yet. The additional templates' exact names, "
                    "parameter shapes and call placement remain to be designed. "
                    "Intended additional templates are labelled pending, separately "
                    "from the complete current source notation.",
                ]
            ),
        ],
        {"class": "qvlk-encoding-guide"},
    )


def _encoding(row, source):
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
            mb_html.para(mb_html.bold("Current source notation:")),
            mb_html.para(
                mb_html.code(mb_html.bdi(source, {"dir": "rtl"})),
                {"dir": "rtl", "lang": "hbo", "class": "pointed qvlk-source"},
            ),
        ],
        {"class": "qvlk-encoding"},
    )


def _prose(text, names=()):
    """Isolate Hebrew runs and italicize the record's named romanizations."""
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
                    mb_html.bdi(run, {"lang": "hbo", "dir": "rtl", "class": "pointed"})
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
    encodings = _near_aleppo_encodings(rows, examples)
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
            "Qere without ketiv has no letters for the qere written in the "
            "body text, though these letters are written in a marginal note. "
            "The space and marks in the body text of the manuscript can nevertheless differ."
        ),
        mb_html.para("The verses below show:"),
        mb_html.unordered_list(
            [
                "The page shows the current near-Aleppo example edition (NAEE) contents for the case at hand.",
                "The page includes any MAM notes regarding the case at hand.",
                "The page includes Aleppo images showing the case at hand.",
            ]
        ),
        mb_html.para(
            "The English versions translate the MAM notes and make their "
            "abbreviated wording explicit. For the brief statements of agreement "
            "about a qere, the notes do not specify whether the agreement "
            "concerns the letters in the margin, the niqqud in the body text, or both."
        ),
        mb_html.para(
            "A masorah circle appears to be present in every case below. "
            "Circle presence is noted here once because it does not distinguish "
            "the cases or require different additional templates. MAM's notes "
            "and their complete translations retain their references to circles.",
            {"class": "qvlk-common-observation"},
        ),
        _comparison_summary(rows, reviews),
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
            _encoding(row, encodings[reference]),
            mb_html.heading_level_3("Current NAEE verse"),
            mb_html.para(
                verses[reference],
                {"dir": "rtl", "lang": "hbo", "class": "pointed foi-verse"},
            ),
            mb_html.heading_level_3("MAM qere"),
            mb_html.para(
                example["qere_html"],
                {"dir": "rtl", "lang": "hbo", "class": "pointed qvlk-hebrew-display"},
            ),
            mb_html.heading_level_3("Current MAM doc-note"),
        ]
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
        contents.append(mb_html.heading_level_3("Aleppo manuscript reading"))
        if row["reading"] is None:
            contents.append(
                mb_html.para(
                    "An image reading has not yet been recorded for this entry."
                )
            )
        else:
            contents.append(mb_html.para(_prose(row["observation"], row["romanized"])))
            contents.extend(
                mb_html.para(_prose(note)) for note in row["documentation_notes"]
            )
            marginal_lines = _inferred_marginal_lines(row)
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
        contents.append(_comparison(review, row["romanized"]))
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
