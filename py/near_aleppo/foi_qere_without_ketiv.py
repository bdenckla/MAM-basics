"""Authored manuscript readings beside current MAM notes and NAEE Scripture.

The shared renderer owns template dispatch. This module selects qere-only render
elements and the documentation whose rendered lemma contains that element; it
does not traverse source-template parameters or change the dataset's policy.
"""

import json
import re
import struct

from hkq_cmn import uxlc_external_links
from mb_cmn import bib_locales as tbn
from mb_cmn import provenance
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import verse_external_links as vel
from mb_misc import mb_html
from mwd import mwd_write_book
from near_aleppo import build_paths
from py_misc import mam_doc_utils, mwd_utils
from py_misc import ren_html_for_renel as hfr
from py_misc import ren_html_from_ren_el_mapping as hfrm
from render_wt import render_element as renel
from render_wt import render_wikitext as rwt

PAGE = "foi/qere-without-ketiv.html"
TITLE = "Qere without ketiv in near-Aleppo"
_FORMAT = "near-aleppo-qere-without-ketiv-readings-v1"
_QERE_TAG = "mam-kq-q-velo-k"
_HEBREW = re.compile(r"([\u0590-\u05ff]+)")
_STYLE = (
    ".pointed.foi-verse { line-height:2.7; }"
    ".qvlk-case { margin:2em 0; }"
    ".pointed.qvlk-notes { line-height:2.2; }"
    ".qvlk-crop { max-width:100%;height:auto; }"
    ".qvlk-caption { font-size:0.9em; }"
    ".romanized { font-style:italic; }"
)


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
        for key in ("romanized", "documentation_notes"):
            if not isinstance(row[key], list) or not all(
                isinstance(value, str) and value for value in row[key]
            ):
                raise ValueError(f"Invalid {key}: {identity}")
        crop = row["crop"]
        if crop is not None and (
            not isinstance(crop, dict)
            or set(crop) != {"filename", "source_screenshot"}
            or not re.fullmatch(r"[A-Za-z0-9._-]+\.png", crop["filename"])
            or not isinstance(crop["source_screenshot"], str)
        ):
            raise ValueError(f"Invalid crop record: {identity}")
    return rows


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
        }
    return result


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


def _crop(row, reference, outputs):
    crop = row["crop"]
    filename = crop["filename"]
    raw = (build_paths.asset_dir() / "qere-without-ketiv" / filename).read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Study crop is not PNG: {filename}")
    width, height = struct.unpack(">II", raw[16:24])
    outputs["img/qere-without-ketiv/" + filename] = raw
    return [
        mb_html.para(
            mb_html.img(
                {
                    "src": "../img/qere-without-ketiv/" + filename,
                    "alt": f"Aleppo Codex crop at {_reference_text(reference)}: the qere-without-ketiv site",
                    "width": str(width),
                    "height": str(height),
                    "class": "qvlk-crop",
                }
            )
        ),
        mb_html.para(
            f"Aleppo Codex — {_reference_text(reference)}.",
            {"class": "qvlk-caption"},
        ),
    ]


def render(verses, rows):
    """Return the study page and unchanged crop bytes owned by the HTML build."""
    examples = mam_examples(rows)
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
            "Qere without ketiv has no written letters for the qere. "
            "The space and marks at the manuscript site can nevertheless differ. "
            "The verses below show the current near-Aleppo example edition (NAEE); "
            "the MAM notes and the recorded Aleppo image readings have their own labels. "
            "Image readings are attributed to Ben Denckla."
        ),
        mb_html.ordered_list(
            [
                mb_html.anchor_h(_reference_text(row["reference"]), "#" + row["id"])
                for row in rows
            ]
        ),
    ]
    for row in rows:
        reference = tuple(row["reference"])
        example = examples[reference]
        contents = [
            mb_html.heading_level_2(
                mb_html.anchor_h(
                    _reference_text(reference), "../" + vel.near_aleppo_href(*reference)
                )
            ),
            mb_html.heading_level_3("Current NAEE verse"),
            mb_html.para(
                verses[reference],
                {"dir": "rtl", "lang": "hbo", "class": "pointed foi-verse"},
            ),
            mb_html.heading_level_3("MAM qere"),
            mb_html.para(
                example["qere_html"], {"dir": "rtl", "lang": "hbo", "class": "pointed"}
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
        reading_title = (
            "Aleppo manuscript reading"
            if row["reading"] is None
            else f"Aleppo manuscript reading — recorded {row['reading']['recorded_date']}"
        )
        contents.append(mb_html.heading_level_3(reading_title))
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
        if row["crop"]:
            contents.extend(_crop(row, reference, outputs))
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
        head_style=_STYLE,
    )
    outputs[PAGE] = mb_html.html_text(body, ctx).encode("utf-8")
    return outputs
