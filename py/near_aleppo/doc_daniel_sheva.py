"""A qualified, documentation-only example from Avi's note on Daniel 5:21."""

import json

from near_aleppo import build_paths
from near_aleppo import doc_figures
from near_aleppo import editorial_ketiv
from near_aleppo.doc_html import (
    HEBREW_CELL,
    he_display,
    he_name,
    he_pointed,
    link,
    table,
)
from mb_misc import mb_html


def assets():
    name = "daniel-5-21-leningrad.png"
    path = build_paths.asset_dir() / name
    return {"img/" + name: path.read_bytes()}


def section():
    source = json.loads(
        (build_paths.mam_parsed_plus_dir() / "F1-Daniel.json").read_text(
            encoding="utf-8"
        )
    )
    note = source["book39s"][0]["chapters"]["5"]["21"][2][3]
    params = note["tmpl_params"]["1"]["tmpl_params"]
    body = note["tmpl_params"]["2"]
    if (
        note["tmpl_name"] != "נוסח"
        or params != {"1": "שוי", "2": "שַׁוִּ֗יו"}
        or body
        != [
            "=ש1,ק-מ,ב1 ובדפוסים וקורן",
            {"tmpl_name": "ש"},
            'ל-כתיב!=שַׁוִּ֗יְ (אות יו"ד שווּאה)',
            {"tmpl_name": "ש"},
            "הערת דותן",
        ]
        or doc_figures._CodexIndex().extant(("F1-Daniel", "5", "21"))
    ):
        raise ValueError("Recheck the Daniel 5:21 documentation against its sources")
    chosen = next(
        r["value"]
        for r in editorial_ketiv.load()["records"]
        if r["id"] == "F1-Daniel:5:21:0"
    )
    return [
        mb_html.heading_level_3(
            "A secondary example: Daniel 5:21", {"id": "daniel-final-sheva"}
        ),
        mb_html.para(
            "Near-Aleppo adopts the following pointed ketiv, without a final sheva:"
        ),
        he_display(chosen),
        mb_html.para(
            [
                "Ben judges the reported sheva a likely "
                "Leningrad peculiarity, unlikely to have been in Aleppo, on the "
                "evidence of its absence in the other manuscripts as represented "
                "by MAM's note. This is an inferred editorial decision following "
                "MAM's body-text choices, not a surviving Aleppo reading.",
            ]
        ),
        mb_html.para(
            "This case has limited relevance to near-Aleppo: the Aleppo Codex is "
            "not extant at Daniel 5:21. It illustrates a question about pointing "
            "the ketiv from MAM's pointed qere, rather than establishing an Aleppo reading."
        ),
        table(
            (
                "MAM ketiv",
                mb_html.abbr("MAM qere", {"title": "MAM's pointed qere"}),
                mb_html.abbr(
                    "Leningrad ketiv",
                    {"title": "Leningrad's pointed ketiv as reported in Avi's note"},
                ),
            ),
            [(he_name(params["1"]), he_pointed(params["2"]), he_pointed("שַׁוִּ֗יְ"))],
            (HEBREW_CELL, HEBREW_CELL, HEBREW_CELL),
        ),
        mb_html.para(
            mb_html.img(
                {
                    "src": "img/daniel-5-21-leningrad.png",
                    "alt": "Leningrad Daniel 5:21: pointed ketiv at right, with sheva beneath the final yod; marginal qere at left",
                    "width": "384",
                    "height": "242",
                    "style": "max-width:100%;height:auto",
                }
            ),
            {"class": "display-example"},
        ),
        mb_html.para(
            "Leningrad, page 442v: the pointed ketiv is at right and the marginal "
            "qere at left. The two dots of the sheva are visible beneath the final "
            "yod. The interpretation of that sheva is discussed below."
        ),
        mb_html.para(
            [
                "English translation of Avi's MAM note: The ketiv of ",
                he_name(params["1"]),
                " with the following pointed qere is consistent with Sassoon 1053, "
                "the Cambridge manuscript, British Library Or. 2375, printed editions, and Koren:",
            ]
        ),
        he_display(params["2"]),
        mb_html.para("The Leningrad ketiv surprisingly reads:"),
        he_display("שַׁוִּ֗יְ"),
        mb_html.para("The yod bears sheva; see Dotan's note."),
        mb_html.para(
            [
                link(
                    "MAM with doc — Daniel 5:21",
                    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/F1-Daniel.html#c5v21",
                ),
                ". “Is consistent with” allows for the difference in presentation: "
                "manuscripts normally have pointed ketiv and unpointed qere, whereas "
                "MAM has pointed qere.",
            ]
        ),
        mb_html.para(
            [
                "Ben proposes that the final sheva reported under the ketiv's yod is "
                "an orphan resting sheva signaling a closed syllable whose final "
                "consonant in the qere is vav. On this hypothesis, the sheva need not "
                "be written under that qere vav. Nonetheless, the implied pointing "
                "can be shown with a sheva under the final vav:",
            ]
        ),
        he_display("שַׁוִּ֗יוְ"),
        mb_html.para(
            "This is a visualization of Ben's hypothesis, not MAM's printed qere. "
            "Producing the reported Leningrad pointed ketiv from "
            "MAM's pointed qere would therefore require a mark absent from that qere. "
            "This proposed explanation concerns the reported Leningrad pointing, "
            "not the pointing adopted by near-Aleppo."
        ),
        mb_html.para(
            [
                "This interpretation is Ben's hypothesis, not an explanation supplied "
                "by Avi's note. The note does not explain the sheva; whether Avi has "
                "an explanation is unknown. ",
                link(
                    "View Daniel 5:21 in Leningrad (page 442v)",
                    "https://www.masoretica.org/?book=Daniel&chapter=5&verse=21&manuscript=leningrad",
                ),
                ". The editorial decision adds no general algorithmic rule.",
            ]
        ),
    ] + _yod_vav()


def _yod_vav():
    records = {r["id"]: r for r in editorial_ketiv.load()["records"]}
    rows = []
    for verse, index, accent in (
        (7, 1, "\N{HEBREW ACCENT MAHAPAKH}"),
        (29, 0, "\N{HEBREW ACCENT MERKHA}"),
    ):
        row = records[f"F1-Daniel:5:{verse}:{index}"]
        expected = "וְהַֽמְנִוכָ" + accent + "א"
        if row["value"] != expected:
            raise ValueError("Recheck the adopted Daniel yod/vav pointings")
        rows.append(
            (
                f"Daniel 5:{verse}",
                he_name("והמנוכא"),
                he_pointed("וְהַֽמְנִיכָ" + accent + "א"),
                he_pointed(expected),
            )
        )
    return [
        mb_html.heading_level_3(
            "Yod and vav in Daniel 5:7 and 5:29", {"id": "daniel-yod-vav"}
        ),
        mb_html.para(
            [
                "These two ketiv/qere pairs differ only in their accents: mahapakh at "
                "5:7 and merkha at 5:29. MAM's ketiv has vav after nun where its qere "
                "has yod. Near-Aleppo adopts the following pointings of MAM's ketiv, "
                "with the qere's marks on the corresponding letters. Aleppo is not "
                "extant at either verse; these are inferred editorial readings.",
            ]
        ),
        table(
            (
                "Verse",
                "MAM ketiv",
                mb_html.abbr("MAM qere", {"title": "MAM's pointed qere"}),
                mb_html.abbr(
                    "Near-Aleppo", {"title": "The pointed ketiv adopted by near-Aleppo"}
                ),
            ),
            rows,
            ({}, HEBREW_CELL, HEBREW_CELL, HEBREW_CELL),
        ),
        mb_html.para(
            [
                "MAM's notes distinguish this spelling from Leningrad's ketiv of ",
                he_name("והמונכא"),
                ", which has vav after mem, before nun. See the Hebrew notes at ",
                link(
                    "MAM with doc — Daniel 5:7",
                    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/F1-Daniel.html#c5v7",
                ),
                " and ",
                link(
                    "MAM with doc — Daniel 5:29",
                    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/F1-Daniel.html#c5v29",
                ),
                ".",
            ]
        ),
        *_note_translations(),
    ]


def _note_translations():
    return [
        mb_html.para(
            [
                "English translation of the MAM note at Daniel 5:7: This reading is "
                "consistent with British Library Or. 2375, the Cambridge manuscript, "
                "the Yemenite manuscript T451, and Leningrad's masorah. The ketiv is:",
            ]
        ),
        he_display("וְהַֽמְנִוכָ֤א"),
        mb_html.para(
            "It has vav after nun in place of the qere's yod; likewise in the Lisbon Bible. Leningrad's ketiv is:"
        ),
        he_display("וְהַֽמְונִכָ֤א"),
        mb_html.para(
            [
                "It has vav after mem, before nun, as also in Koren. "
                "Notes by Breuer and the tanach.us transcription "
                "(version unspecified in the MAM note). ",
                link(
                    "MAM with doc — Daniel 5:7",
                    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/F1-Daniel.html#c5v7",
                ),
                ".",
            ]
        ),
        mb_html.para(
            [
                "In the comparison below, the sequence ",
                he_name("מנו"),
                " abbreviates the full ketiv of ",
                he_name("והמנוכא"),
                ", and the sequence ",
                he_name("מונ"),
                " abbreviates the full ketiv of ",
                he_name("והמונכא"),
                ". Leningrad's masorah is listed separately from its written ketiv.",
                " MAM adopts the spelling with ",
                he_name("מנו"),
                " at both verses.",
            ]
        ),
        *_spelling_tables(),
        mb_html.para(
            [
                "The accent is mahapakh at 5:7 and merkha at 5:29. Both notes cite "
                "Breuer; 5:7 also cites the tanach.us transcription "
                "(version unspecified in the MAM note), and 5:29 names Simanim "
                "and Mechon Mamre. These citations do not assign those sources "
                "a spelling in the notes, so they are not included in the spelling tables. ",
                link(
                    "MAM with doc — Daniel 5:7",
                    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/F1-Daniel.html#c5v7",
                ),
                " and ",
                link(
                    "MAM with doc — Daniel 5:29",
                    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/F1-Daniel.html#c5v29",
                ),
                ".",
            ]
        ),
    ]


def _spelling_tables():
    # One evidence matrix supplies both orientations; do not infer an uncited reading.
    sources = (
        ("Cambridge manuscript", "מנו", "מנו"),
        ("T451", "מנו", "מנו"),
        ("British Library Or. 2375", "מנו", "מונ"),
        ("Leningrad masorah", "מנו", "מנו"),
        ("Leningrad ketiv", "מונ", "מונ"),
        ("Sassoon 1053", "Not cited", "מונ"),
        ("Lisbon Bible", "מנו", "מנו"),
        ("Koren", "מונ", "מונ"),
    )
    spellings = ("מנו", "מונ")
    by_spelling = [
        (
            he_name(s),
            *(
                "; ".join(row[0] for row in sources if row[column] == s)
                for column in (1, 2)
            ),
        )
        for s in spellings
    ]
    return [
        mb_html.heading_level_3("Sources by spelling"),
        table(("Spelling", "5:7", "5:29"), by_spelling, (HEBREW_CELL, {}, {})),
        mb_html.heading_level_3("Spelling by source"),
        mb_html.para(
            "“Not cited” means that the note does not mention the source. "
            "Citation-only references, which assign no spelling, are discussed below."
        ),
        _comparison_table(sources),
    ]


def _comparison_table(sources):
    classes = {"מנו": "spelling-mnu", "מונ": "spelling-mun"}
    body = [mb_html.table_row_of_headers(("Source", "5:7", "5:29"))]
    for name, left, right in sources:
        cells = [mb_html.table_datum(name)]
        shared = left == right and left in classes
        for reading in ((left,) if shared else (left, right)):
            if reading in classes:
                attrs = {"dir": "rtl", "class": classes[reading]}
                if shared:
                    attrs["colspan"] = "2"
                cells.append(mb_html.table_datum(he_name(reading), attrs))
            else:
                cells.append(mb_html.table_datum(reading))
        body.append(mb_html.table_row(cells))
    return mb_html.div(mb_html.table(body), {"class": "table-wrap"})
