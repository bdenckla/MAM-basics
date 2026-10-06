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
    out.append(
        mb_html.para(
            [
                "For the general GAV explanation, display alternatives, and "
                "Unicode discussion, see ",
                link("GAV notation and display", "reading-json.html#gav-display"),
                ".",
            ],
            {"id": "gav-display"},
        )
    )
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
