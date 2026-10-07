"""Genesis 43:28: adopted pointing and an explicitly uncertain qere inference."""

import json

from near_aleppo import build_paths
from near_aleppo import doc_figures
from near_aleppo import editorial_ketiv
from near_aleppo.doc_html import he_display, he_name, link, verse_refs
from mb_misc import mb_html

VERSE = ("A1-Genesis", "43", "28")
IDENTIFIER = "A1-Genesis:43:28:0"
CHOSEN = "וַיִּֽשְׁתַּחֲוּֽ"
MAM_QERE = "וַיִּֽשְׁתַּחֲוֽוּ"
ALTERNATIVE_QERE = "וַיִּֽשְׁתַּחֲוּֽוּ"
LENINGRAD_KETIV = "וַיִּֽשְׁתַּחֲוֻּֽ"
# The body of MAM's note at Genesis 43:28, which the section summarizes, copied
# from MAM-parsed-plus by script.
NOTE_BODY = [
    (
        '=ב,ש,ש1,ו ובדפוסים (כתיב חסר וי"ו, ונקודת שורוק בלבד באות וי"ו '
        'האחרונה); לכן ב,ש,ש1,ו=וַיִּֽשְׁתַּחֲוֽוּ קרי (אין נקודה בוי"ו '
        "עיצורית), וכמו כן בדפוסים."
    ),
    {
        "tmpl_name": "ש",
    },
    (
        'ל,לו,ק3=וַיִּֽשְׁתַּחֲוֻּֽ (כתיב חסר וי"ו, וניקוד של קובוץ ונקודת שורוק '
        'ביח באות וי"ו האחרונה); ולכן ל,ל1,ק3=וַיִּֽשְׁתַּחֲוּֽוּ קרי (נקודה '
        'בוי"ו עיצורית).'
    ),
    {
        "tmpl_name": "ש",
    },
    "הערות ברויאר ודותן והמקליד",
]
MAM_URL = "https://bdenckla.github.io/MAM-basics/MAM-with-doc/A1-Genesis.html#c43v28"


def section():
    source = json.loads(
        (build_paths.mam_parsed_plus_dir() / "A1-Genesis.json").read_bytes()
    )
    note = source["book39s"][0]["chapters"]["43"]["28"][2][1]
    chosen = next(
        row["value"]
        for row in editorial_ketiv.load()["records"]
        if row["id"] == IDENTIFIER
    )
    if (
        note["tmpl_name"] != "נוסח"
        or set(note["tmpl_params"]) != {"1", "2"}
        or note["tmpl_params"]["2"] != NOTE_BODY
        or note["tmpl_params"]["1"]["tmpl_params"] != {"1": "וישתחו", "2": MAM_QERE}
        or chosen != CHOSEN
        or doc_figures._CodexIndex().extant(VERSE)
    ):
        raise ValueError("Recheck the Genesis 43:28 decision against its exact sources")
    return [
        mb_html.heading_level_3("Genesis 43:28", {"id": "genesis-pointed-ketiv"}),
        mb_html.para(
            [
                "At ",
                *verse_refs([VERSE]),
                ", near-Aleppo adopts this pointed ketiv:",
            ]
        ),
        he_display(chosen),
        mb_html.para(
            "The final written vav has a shuruq dot and silluq, without qubuts. "
            "This is an individual editorial decision inferred from MAM's somewhat "
            "indirect note. Aleppo is not extant here. MAM describes the deficient "
            "ketiv and its pointing in prose while displaying the expanded qere; "
            "it does not quote this chosen pointed ketiv as a separate complete form."
        ),
        mb_html.heading_level_3("The source note"),
        mb_html.para(
            [
                "English summary of MAM's note: The group ",
                he_name("ב,ש,ש1,ו"),
                " and printed editions have the deficient ketiv spelling with a "
                "shuruq dot alone on the final vav. MAM consequently gives this "
                "qere, with no dot on its consonantal vav:",
            ]
        ),
        he_display(MAM_QERE),
        mb_html.para(
            "MAM reports a different pointed ketiv for Leningrad: the same final "
            "written vav bears both qubuts and a shuruq dot. Its quoted form is:"
        ),
        he_display(LENINGRAD_KETIV),
        mb_html.para(
            "MAM interprets that pointing as a qere with a dot on the consonantal "
            "vav as well as shuruq on the final vav:"
        ),
        he_display(ALTERNATIVE_QERE),
        mb_html.para(
            [
                link("MAM's note at Genesis 43:28", MAM_URL),
                ". Near-Aleppo follows the first group's described ketiv "
                "pointing in this decision; it has no diplomatic Leningrad default.",
            ]
        ),
        mb_html.heading_level_3("The inference remains uncertain"),
        mb_html.para(
            "Ben questions whether the chosen ketiv uniquely favors MAM's "
            "undotted consonantal vav over the dotted alternative. His reasoning "
            "is that a dagesh or another qere mark may lack a suitable ketiv carrier "
            "and be omitted rather than transferred. If that reasoning also applies "
            "to shuruq, the ketiv's single dot need not determine which qere "
            "pointing underlies it. This is reasoned uncertainty, not a demonstrated "
            "historical explanation or a claim that the two qeres are equally likely."
        ),
        mb_html.para(
            "Near-Aleppo retains MAM's current qere unchanged. This individual "
            "choice supplies no general rule for dropping a final shuruq and "
            "does not revise the frozen inference archive."
        ),
    ]
