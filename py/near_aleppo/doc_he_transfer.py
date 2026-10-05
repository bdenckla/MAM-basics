"""Equal-status manuscript examples of mobile he and patah ownership."""

import json

from near_aleppo import build_paths
from near_aleppo import doc_figures
from near_aleppo.doc_html import (
    HEBREW_CELL,
    he_display,
    he_name,
    he_pointed,
    link,
    table,
    verse_refs,
)
from near_aleppo.editorial_ketiv import ga
from mb_misc import mb_html

_EXAMPLES = (
    ('BA-Samuel שמ"ב', "5", "2", "הייתה מוציא", "samuel0502.png", "2+Samuel"),
    ("C3-Ezekiel", "42", "9", "ומתחתה לשכות", "ezekiel4209.png", "Ezekiel"),
    ("D3-Job", "38", "12", "ידעתה שחר", "job3812.png", "Job"),
)


def assets():
    root = build_paths.asset_dir() / "he-transfer"
    return {
        "img/he-transfer/" + row[4]: (root / row[4]).read_bytes() for row in _EXAMPLES
    }


def _pointings(value, ref):
    for _, template in doc_figures._templates(value, ref, doc_figures._DATASET):
        params = template.get("tmpl_params", {})
        if "כתיב מנוקד" in params:
            yield params


def section():
    out = [
        mb_html.heading_level_3("Mobile he and the patah", {"id": "mobile-he"}),
        mb_html.para(
            [
                "In these word-pairs, “mobile ",
                he_name("ה"),
                "” describes the relationship between a he at the end of the first ketiv "
                "word and a he at the beginning of the second qere word. The consonantal "
                "relationship alone does not determine where the patah belongs.",
            ]
        ),
        mb_html.para(
            [
                "In 2 Samuel 5:2 and Job 38:12, the ",
                he_name("פתח"),
                " belongs to the final mobile ",
                he_name("ה"),
                " of the first ketiv word. In Ezekiel 42:9, however, the ",
                he_name("פתח"),
                " is unattached; despite a seemingly available mobile ",
                he_name("ה"),
                " to attach it to, the naqdan avoids doing so. This word-pair relates the ",
                he_name("כתיב"),
                " of ",
                he_name("ומתחתה לשכות"),
                " to the ",
                he_name("קרי"),
                " of ",
                he_name("ומתחת הלשכות"),
                ".",
            ]
        ),
        mb_html.para(
            "In GAV (guillemet-alef-vav) notation, the unattached patah before the second ketiv word is recorded as:"
        ),
        he_display("«אַ»"),
        mb_html.para(
            [
                "The alef "
                "inside the guillemets is an artificial carrier, not a ketiv consonant. "
                "Near-Aleppo stores it in its existing marks-without-letter template. "
                "A patah belonging to a written he stays on that he, without guillemets.",
            ]
        ),
    ]
    out.extend(_gav_display())
    for book, chapter, verse, ketiv, filename, url_book in _EXAMPLES:
        stem, _, sub = book.partition(" ")
        data = json.loads(
            (build_paths.dataset_dir() / (stem + ".json")).read_text(encoding="utf-8")
        )
        cell = next(b for b in data["book39s"] if b["sub_book_name"] == (sub or None))[
            "chapters"
        ][chapter][verse][2]
        matches = [
            p for p in _pointings(cell, (book, chapter, verse)) if p.get("1") == ketiv
        ]
        if len(matches) != 1:
            raise ValueError(f"Missing mobile-he example: {book} {chapter}:{verse}")
        params = matches[0]
        out.extend(
            [
                mb_html.heading_level_3(verse_refs(((book, chapter, verse),))),
                table(
                    ("Ketiv", "Qere", "Pointed ketiv (GAV)"),
                    [
                        (
                            he_name(ketiv),
                            he_pointed(params["2"]),
                            he_pointed(ga(params["כתיב מנוקד"])),
                        )
                    ],
                    (HEBREW_CELL, HEBREW_CELL, HEBREW_CELL),
                ),
                mb_html.para(
                    mb_html.img(
                        {
                            "src": "img/he-transfer/" + filename,
                            "alt": f"Aleppo Codex crop: {url_book.replace('+', ' ')} {chapter}:{verse}",
                            "style": "max-width:100%;height:auto",
                        }
                    )
                ),
                mb_html.para(
                    link(
                        "View this verse in the Aleppo Codex on Masoretica",
                        f"https://www.masoretica.org/?book={url_book}&chapter={chapter}&manuscript=aleppo&verse={verse}",
                    )
                ),
            ]
        )
    return out


def _gav_display():
    return [
        mb_html.heading_level_3("GAV notation and display in practice"),
        mb_html.para(
            "GAV (guillemet-alef-vav) notation is a human-readable semantic "
            "representation of orphan marks: marks without a written letter. "
            "GA uses an artificial alef carrier generally; GV uses "
            "an artificial vav for holam. The guillemets identify the carrier "
            "as artificial. For example, an orphan holam in GV is:",
            {"id": "gav-display"},
        ),
        he_display("«וֹ»"),
        mb_html.para(
            "This vav is a notation carrier, not a ketiv consonant. The example "
            "explains the notation; it is not an additional reading of the "
            "mobile-he cases. The raw JSON's "
            "marks-without-letter template preserves its original alef-carrier "
            "shape, including its existing holam carriers. New explicitly licensed "
            "GV choices use the separate carrier=holam-male-vav variant with "
            "parameter 1 exactly VAV + HOLAM. GV is not converted to ALEF + HOLAM: "
            "that would lose the chosen holam-male distinction."
        ),
        mb_html.para(
            "For an orphan holam associated with a qere vav where the ketiv has "
            "yod, an edition can choose among these display options:"
        ),
        mb_html.unordered_list(
            [
                "Show GAV directly, retaining the GV carrier before the ketiv yod.",
                "Collapse the holam backwards onto the consonant before the ketiv yod.",
                "Attach U+05B9 HEBREW POINT HOLAM to the ketiv yod as a rendering "
                "accommodation, without asserting that the yod owns the mark.",
            ]
        ),
        mb_html.para(
            "These are late display choices, not changes to the underlying "
            "semantic representation. Their visual acceptability depends on the "
            "font and rendering system. Prepared markup could let CSS select "
            "among display forms or position the dot. CSS alone does not reorder "
            "the Unicode text, and hiding a carrier does not reliably reattach "
            "its combining mark to another letter."
        ),
        mb_html.para(
            [
                "Unicode's ",
                link(
                    "Hebrew specification, “Holam Male and Holam Haser”",
                    "https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-9/",
                ),
                " uses U+05B9 for holam male on vav when the distinction is made. "
                "U+05BA HEBREW POINT HOLAM HASER FOR VAV distinguishes holam on "
                "consonantal vav; its use on other base letters is undefined. "
                "U+05B9 is also the ordinary holam on other letters. Unicode thus "
                "has no separate, letter-independent holam-male dot that would "
                "express the qere-vav role when attached to ketiv yod. Applying "
                "U+05B9 to yod can display the dot, but does not encode that role. "
                "A hypothetical letter-independent holam-male dot could make "
                "that intention explicit even on yod. The mismatch concerns "
                "encoded meaning, not a general Unicode ban on nonstandard "
                "letter-mark sequences.",
            ]
        ),
    ]
