"""
Generates a bilingual (Hebrew/English) HTML document about the געיה marks in MAM.

The Hebrew text is from Avi Kadish's introduction to the Miqra al pi ha-Masora
edition, Chapter 3, section "נוסח הגעיות במהדורתנו". The source is on Hebrew
Wikisource:
https://he.wikisource.org/wiki/ויקיטקסט:מבוא_למקרא_על_פי_המסורה/פרק_ג#נוסח_הגעיות_במהדורתנו

The Hebrew was copied by script from revision 3079273 (2026-08-26) of that page, as
mirrored in in/mam-ws-intro/ch3.mediawiki, and put in MAM-normal mark order. It keeps the
source's wording and drops only its links and its display templates.

The English translation is AI-generated. Claude, an AI model, wrote it on 2026-09-25, at
Ben Denckla's request, and no human has reviewed it yet. The page says so in a box above
everything else, and the site index and the misc index say so beside the link. Remove all
three, and this paragraph, only once a human has reviewed the translation.
"""

from dataclasses import dataclass

from mb_misc import mb_html
from mb_author import author


def gen_html_file(tdm_ch, body_class=None):
    """Write the page and return its misc-index entry.

    The entry's label is the page title followed by the caveat, so that the misc index,
    like the page and the site index, says that the translation is unreviewed.
    """
    fname, title = author.help_gen_html_file(
        __file__, tdm_ch, _FNAME, _TITLE, _CBODY, body_class
    )
    return fname, f"{title} {_CAVEAT_PAREN}"


# Footnotes are numbered as B+N (N=0,1,...,5). B is the number of the first footnote in
# this document within chapter 3 of the Kadish introduction, as Wikisource renders
# revision 3079273: its six footnotes are [94] through [99] there.
_FN_BASE = 94


def _footnote_marker(n: int, side="h"):
    """Footnote marker for body text, linking to the footnote entry.

    side="h": Hebrew side — carries the anchor id (for the back-link target).
    side="e": English side — link only (no id, to avoid duplicate ids).
    """
    text = f"[B+{n}]"
    if side == "h":
        return mb_html.anchor(text, {"id": f"fnref-{n}", "href": f"#fn-{n}"})
    return author.anchor_h(text, f"#fn-{n}")


def _ait(contents):
    """Added In Translation, i.e. not in original, i.e. square-bracketed (and gray)"""
    return author.span_gray(["[", contents, "]"])


def _he(text):
    """Unpointed Hebrew inside English prose, isolated so its direction cannot leak."""
    return mb_html.bdi(text, {"lang": "he"})


def _forms(item, conjunction):
    """The item's form, or its alternative forms joined by the conjunction."""
    parts = [author.hbo(item.forms[0])]
    for form in item.forms[1:]:
        parts.extend([conjunction, author.hbo(form)])
    return parts


def _book_para_h(book):
    """One book's list as the source has it, minus the source's links."""
    parts = [author.emphasis(book.name_he), f" ({book.stated_count} פריטים): "]
    for i, item in enumerate(book.items):
        last = i == len(book.items) - 1
        parts.extend([item.label_he, " (", "ל?=" if item.doubtful else "ל="])
        parts.extend(_forms(item, " או "))
        if item.occurrence is not None:
            parts.append(f" [{item.occurrence}]")
        parts.extend([")", "." if last else ";"])
        if item.footnote is not None:
            parts.append(_footnote_marker(item.footnote))
        if not last:
            parts.append(" ")
    return author.para_modhe(parts)


def _verse_e(item):
    parts = [item.verse_en]
    if item.occurrence is not None:
        parts.append(f" [{item.occurrence}]")
    if item.doubtful:
        parts.append(" (?)")
    if item.footnote is not None:
        parts.extend([" ", _footnote_marker(item.footnote, "e")])
    return parts


def _book_cell_e(book):
    rows = [[_verse_e(item), _forms(item, " or ")] for item in book.items]
    return [
        author.para([author.emphasis(book.name_en), f" ({book.stated_count} items):"]),
        author.std_table(
            rows,
            coldirs=["ltr", "rtl"],
            arg_to_troh=["Verse", "The Leningrad Codex has"],
        ),
    ]


def _ol_h(items):
    return mb_html.ordered_list(items, {"lang": "he"})


def _ftnt_triple(n, ftnt_h, ftnt_e):
    text = f"[B+{n}]"
    marker_h = mb_html.anchor(text, {"id": f"fn-{n}", "href": f"#fnref-{n}"})
    marker_e = author.anchor_h(text, f"#fnref-{n}")
    return (
        f"Footnote B+{n}",
        author.para_modhe([marker_h, " ", *ftnt_h]),
        author.para([marker_e, " ", *ftnt_e]),
    )


def _counts_note():
    """Say how the source's per-book counts compare with its lists, from the lists."""
    lengths = [len(book.items) for book in _BOOKS]
    keys = [
        (book.name_en, item.verse_en, item.forms)
        for book in _BOOKS
        for item in book.items
    ]
    repeated = sorted({key for key in keys if keys.count(key) > 1})
    assert len(repeated) == 1, repeated
    book_en, verse_en, _forms_of_repeat = repeated[0]
    listed = ", ".join(str(n) for n in lengths[:-1]) + f" and {lengths[-1]}"
    return [
        "The counts in parentheses are the source's.",
        f" The lists have {listed} items: {sum(lengths)} in all,",
        f" or {len(set(keys))} places, since {book_en} {verse_en} appears twice.",
    ]


@dataclass(frozen=True)
class _Item:
    """One item of the source's list: a place where MAM did not follow the LC's געיה."""

    label_he: str
    verse_en: str
    forms: tuple[str, ...]
    doubtful: bool = False  # the source's "ל?=": the LC's text there is in doubt
    occurrence: int | None = None  # the source's "[2]": the form's second occurrence
    footnote: int | None = None


@dataclass(frozen=True)
class _Book:
    name_he: str
    name_en: str
    stated_count: int  # the source's count, which is lower than len(items)
    items: tuple[_Item, ...]


# The Hebrew side, lifted from the mirror by script (see the module docstring).
_URL_HEIDENHEIM = "https://archive.org/details/heidenheim-torah-ein-ha-sofer-rodelheim-1818-1821-images/page/n5/mode/2up?view=theater"
_URL_BAER = "https://archive.org/details/baer-delitzsch-masoretic-bible-full/page/n117/mode/2up?view=theater"
_SIGLA_H = "ל1, ב, ש, ש1, ק3, ו"
_SEC_H = "נוסח הגעיות במהדורתנו"
_P1_H = [
    author.emphasis('נוסח הגעיות לפי כתי"ל:'),
    " אין במהדורתנו שיחזור של כל הגעיות במקומות החסרים בכתר (בניגוד למקראות גדולות הכתר), ואין בה הוספת געיה בכל תיבה הראויה לכך (בניגוד לסימון הגעיות ",
    author.emphasis("הקצרות"),
    " במהדורות ברויאר).",
    " אלא העתקנו את הגעיות כמות שהן בכתר (במקומות שהוא קיים)",
    _footnote_marker(0),
    ' ובכתי"ל (ברוב התורה שהכתר חסר).',
    " כתוצאה מכך, סימון הגעיות במהדורתנו מקביל בדרך כלל לסימון הגעיות ",
    author.emphasis("הארוכות"),
    " בתוך מהדורות ברויאר (כך הוא סימן את הגעיות הכתובות בכתבי־\N{RIGHT-TO-LEFT MARK}היד כדי לעשות הבחנה).",
]
_P2_H = [
    author.emphasis("היוצאים מן הכלל:"),
    ' יש מקומות בתורה שבהם נכתבה געיה בכתי"ל, אך היא בלתי צפויה או מופיעה בניגוד לכללים, או שהיא נכתבה באות הלא-נכונה לפי הכללים, או שיש שתי געיות בתיבה אחת (או בתיבות מוקפות); לחלופין יש מקומות שבהם נדרשת געית חובה והיא איננה, או שהגעיה צפויה ברמת סבירות גבוהה בהתאם למקבילות (כגון געית פשטא) והיא איננה.',
    " הרב ברויאר כבר רשם את הגעיות החריגות הללו בתורה בכ-40 מקומות,",
    _footnote_marker(1),
    ' ואת חלקם תיקן במהדורותיו האחרונות (חורב ו"כתר ירושלים"), כל עוד מצא לכך תימוכין בכתי"ל',
    mb_html.sup("מ"),
    ".",
    _footnote_marker(2),
    ".",
    " במהדורתנו בצענו תיקון ",
    author.emphasis("בכל"),
    ' הגעיות החריגות שרשם ברויאר בתורה, אפילו במיעוט המקומות שבהם הנוסח החריג נמצא גם בכתי"ל',
    mb_html.sup("מ"),
    ", ובעוד עשרות מקומות שאותם לא ציין ברויאר.",
    ' בכל מקום כזה ציינו את גרסתו של כתי"ל בתיעוד הנוסח, ועוד השתדלנו לתעד את נוסח הגעיות בכתבי־היד טברנים מובהקים נוספים (ל1, ב, ש, ש1, ק3, ו).',
]
_P3_H = [
    author.emphasis("רשימה של היוצאים מן הכלל:"),
    " להלן רשימה של המקומות בתורה שבהם ",
    author.emphasis("לא"),
    ' קיבלנו את נוסח הגעיות בכתי"ל בתורה.',
    " למידע נוסף לגבי כל פריט, כולל מידע על הנוסח בכתבי־יד טברנים נוספים, ראו בתיעוד הנוסח (בדפי העריכה של הפרקים).",
    _footnote_marker(3),
]
_BOOKS = (
    _Book(
        "ספר בראשית",
        "Genesis",
        36,
        (
            _Item("ב,ז", "2:7", ("וַֽיְהִ֥י",)),
            _Item("ה,ג", "5:3", ("וַֽיְחִ֣י",)),
            _Item("ה,ט", "5:9", ("וַֽיְחִ֥י",)),
            _Item("ה,י", "5:10", ("וַֽיְחִ֣י",)),
            _Item("ה,יב", "5:12", ("וַֽיְחִ֥י",)),
            _Item("ה,טו", "5:15", ("וַֽיְחִ֣י",)),
            _Item("ה,טז", "5:16", ("וַֽיְחִ֣י",)),
            _Item("ה,כו", "5:26", ("וַֽיְחִ֣י",)),
            _Item("ו,טז", "6:16", ("תַּֽעֲשֶׂ֣ה",), doubtful=True),
            _Item("ז,י", "7:10", ("וַֽיְהִ֖י",)),
            _Item("ז,יב", "7:12", ("וַֽיְהִ֥י",)),
            _Item("ח,ו", "8:6", ("וַֽיְהִ֕י",)),
            _Item("ח,יג", "8:13", ("וַֽ֠יְהִי",)),
            _Item("י,יט", "10:19", ("וַֽיְהִ֞י",)),
            _Item("י,ל", "10:30", ("וַֽיְהִ֥י",)),
            _Item("יא,א", "11:1", ("וַֽיְהִ֥י",)),
            _Item("יא,ב", "11:2", ("וַֽיְהִ֖י",)),
            _Item("יא,יג", "11:13", ("וַֽיְחִ֣י",)),
            _Item("יט,יג", "19:13", ("כִּֽי־גָֽדְלָ֤ה",)),
            _Item("יח,טו", "18:15", ("וַיֹּ֥אמֶר ׀ לֹ֖א",)),
            _Item("יט,יג", "19:13", ("כִּֽי־גָֽדְלָ֤ה",)),
            _Item("כה,לא", "25:31", ("אֶת־בְּכֹֽרָתְךָ֖",)),
            _Item("כז,א", "27:1", ("וַיְהִי֙",)),
            _Item("לא,מג", "31:43", ("מָֽה־אֶֽעֱשֶׂ֤ה",)),
            _Item("לא,נב", "31:52", ("לֹֽא־אֶֽעֱבֹ֤ר",), doubtful=True),
            _Item("לב,כו", "32:26", ("בְּהֵֽאָבְק֖וֹ",)),
            _Item("לה,ג", "35:3", ("וַיְהִי֙",)),
            _Item("לו,יח", "36:18", ("אָֽהֳלִיבָמָ֛ה",), occurrence=2),
            _Item("לז,כג", "37:23", ("וַֽיְהִ֕י",)),
            _Item("לח,יח", "38:18", ("הָֽעֵרָבוֹן֮",)),
            _Item("לח,כד", "38:24", ("לֵֽאמֹר֙",)),
            _Item("לט,יא", "39:11", ("וַיְהִי֙",)),
            _Item("לט,יג", "39:13", ("וַיְהִי֙",)),
            _Item("מג,כא", "43:21", ("וַֽיְהִ֞י",)),
            _Item("מד,כד", "44:24", ("וַיְהִי֙",)),
            _Item("מה,יד", "45:14", ("בִנְיָמִֽן־אָחִ֖יו",), doubtful=True),
            _Item("מו,יט", "46:19", ("יַֽעֲקֹ֔ב",), doubtful=True),
            _Item("מט,יח", "49:18", ("לִֽישׁוּעָתְךָ֖",)),
        ),
    ),
    _Book(
        "ספר שמות",
        "Exodus",
        11,
        (
            _Item("א,כא", "1:21", ("כִּֽי־יָֽרְא֥וּ",)),
            _Item("ה,ד", "5:4", ("מִמַּֽעֲשָׂ֑יו",)),
            _Item("ז,יג", "7:13", ("וַיֶּחֱזַק֙",)),
            _Item("ח,כא", "8:21", ("לֵֽאלֹהֵיכֶ֖ם",)),
            _Item("ט,לה", "9:35", ("וַֽיֶּחֱזַק֙",)),
            _Item("יג,ה", "13:5", ("כִֽי־יְבִֽיאֲךָ֣",)),
            _Item("יג,יא", "13:11", ("כִּֽי־יְבִֽאֲךָ֤",)),
            _Item("טו,כו", "15:26", ("כָּֽל־הַמַּֽחֲלָ֞ה",)),
            _Item("כ,ג", "20:3", ("תַֽעֲשֶׂ֨ה־לְךָ֥֣",)),
            _Item("כא,יד", "21:14", ("וְכִי־יָזִ֥ד",), doubtful=True),
            _Item("כד,יא", "24:11", ("וַֽיֶּחֱזוּ֙",)),
            _Item("ל,י", "30:10", ("קֹֽדֶשׁ־קָֽדָשִׁ֥ים",)),
            _Item("לב,ל", "32:30", ("וַיְהִי֙",)),
            _Item("לו,יג", "36:13", ("וַֽיְהִ֥י",)),
        ),
    ),
    _Book(
        "ספר ויקרא",
        "Leviticus",
        8,
        (
            _Item("א,ה", "1:5", ("הַֽכֹּֽהֲנִים֙",)),
            _Item("ג,יז", "3:17", ("מֽוֹשְׁבֹתֵיכֶ֑ם",)),
            _Item("ח,יא", "8:11", ("עַֽל־הַמִּזְבֵּ֖חַ",)),
            _Item("ט,א", "9:1", ("וַיְהִי֙",)),
            _Item("כ,כז", "20:27", ("כִּֽי־יִהְיֶ֨ה",), doubtful=True),
            _Item("כג,ג", "23:3", ("מֽוֹשְׁבֹתֵיכֶֽם",)),
            _Item("כג,לא", "23:31", ("מֹֽשְׁבֹֽתֵיכֶֽם",)),
            _Item("כג,מד", "23:44", ("אֶת־מֹעֲדֵ֖י",)),
            _Item("כה,כח", "25:28", ("לֹֽא־מָֽצְאָ֜ה",)),
            _Item("כז,כח", "27:28", ("קֹֽדֶשׁ־קׇֽדָשִׁ֥ים",)),
        ),
    ),
    _Book(
        "ספר במדבר",
        "Numbers",
        15,
        (
            _Item(
                "ג,ו",
                "3:6",
                (
                    "וְהַֽעֲמַדְתָּ֣",
                    "וְֽהַעֲמַדְתָּ֣",
                ),
                footnote=4,
            ),
            _Item("ג,כז", "3:27", ("הָֽעָזִּיאֵלִ֑י",)),
            _Item("ד,לב", "4:32", ("וִֽיתֵדֹתָם֙",)),
            _Item("ה,כא", "5:21", ("אֶֽת־הָֽאִשָּׁה֮",)),
            _Item("י,ח", "10:8", ("בַּֽחֲצֹצְר֑וֹת",)),
            _Item("יא,כד", "11:24", ("וַֽיַּעֲמֵ֥ד",)),
            _Item("יד,כה", "14:25", ("וְהָֽעֲמָלֵקִ֥י וְהַֽכְּנַעֲנִ֖י",)),
            _Item("יד,לח", "14:38", ("הַֽהֹלְכִ֖ים",)),
            _Item("טו,יד", "15:14", ("אֲשֶֽׁר־בְּתֽוֹכְכֶם֙",)),
            _Item("טו,מ", "15:40", ("לֵֽאלֹהֵיכֶֽם",)),
            _Item("טז,יח", "16:18", ("וַֽיַּעַמְד֗וּ",), doubtful=True),
            _Item("טז,לא", "16:31", ("וַיְהִי֙",)),
            _Item("יז,כא", "17:21", ("כָּֽל־נְשִֽׂיאֵיהֶ֡ם",)),
            _Item("יח,ב", "18:2", ("וִֽישָׁרְת֑וּךָ",)),
            _Item("כה,ב", "25:2", ("לֵֽאלֹהֵיהֶֽן",)),
            _Item("כו,לא", "26:31", ("הָֽאַשְׂרִֽאֵלִ֑י",)),
            _Item("לא,לב", "31:32", ("וַיְהִי֙",)),
            _Item("לג,ג", "33:3", ("הָֽרִאשׁ֔וֹן",), doubtful=True),
            _Item("לה,לג", "35:33", ("וְלֹא־תַחֲנִ֣יפוּ",), doubtful=True),
        ),
    ),
    _Book(
        "ספר דברים",
        "Deuteronomy",
        17,
        (
            _Item("א,ג", "1:3", ("וַיְהִי֙",)),
            _Item("א,כט", "1:29", ("לֹא־תַֽעַרְצ֥וּן וְֽלֹא־תִֽירְא֖וּן",)),
            _Item("א,לג", "1:33", ("לַֽחֲנֹֽתְכֶ֑ם",)),
            _Item("ז,ח", "7:8", ("מֵֽאַהֲבַ֨ת",)),
            _Item("ז,יג", "7:13", ("וְתִֽירֹשְׁךָ֣",)),
            _Item("ח,ג", "8:3", ("וַיַּֽאֲכִֽלְךָ֤",)),
            _Item("ח,טז", "8:16", ("הַמַּֽאֲכִ֨לְךָ֥",)),
            _Item("יא,יד", "11:14", ("וְתִֽירֹשְׁךָ֖",)),
            _Item("יא,כד", "11:24", ("הָֽאַחֲר֔וֹן",)),
            _Item("יא,כה", "11:25", ("וּמֽוֹרַאֲכֶ֜ם",)),
            _Item("יב,יז", "12:17", ("וְתִֽירֹשְׁךָ֣",)),
            _Item("יב,כ", "12:20", ("אֶֽת־גְּבֽוּלְךָ֮",)),
            _Item("יב,ל", "12:30", ("לֵֽאלֹהֵיהֶ֜ם",)),
            _Item("יב,לא", "12:31", ("לֵֽאלֹהֵיהֶֽם",)),
            _Item("יד,כג", "14:23", ("תִּֽירֹשְׁךָ֣",)),
            _Item("יח,ד", "18:4", ("תִּֽירֹשְׁךָ֣",)),
            _Item("כ,יח", "20:18", ("לֵֽאלֹהֵיהֶ֑ם",)),
            _Item("דברים כח,יא", "28:11", ("וְהוֹתִֽרְךָ֤",), doubtful=True),
        ),
    ),
)
_P4_H = [
    'למרות כל היוצאים מן הכלל (למעלה מ-80 פריטים ברשימה), השארנו את נוסח הגעיות שבכתי"ל ברוב המכריע של התורה ובשאר המקומות החסרים בכתר, ולא ניסינו לקרב אותו יותר אל נוסח הגעיות שהיה בכתר (ע"י שחזור מלא לפי כל נטיותיו של כתר בכתיבת הגעיות).',
    " יש שתי סיבות מעשיות להחלטתנו להביא רק את הגעיות הרשומות בכתבי־היד (חוץ מהמקומות החריגים):",
]
_P4_ITEMS_H = [
    [
        "שחזור הגעיות ו/או הוספתן בכל תיבה הראויה לכך במקרא דורשת עבודה רבה, וזה כרגע מעבר ליכולתנו מבחינת התורמים לפרויקט.",
        " ואולם תמיד יהיה ניתן לשדרג את מהדורתנו בעתיד באחת מהדרכים הללו או לבצע אותן במהדורות נגזרות.",
    ],
    [
        "הוספת הגעיות באופן מלא ועקבי בדומה למהדורת ברויאר איננה אפשרית כעת גם מסיבה טכנית, כי אין היום תווים מיוחדים ביוניקוד בשביל געיות שונות (ארוכות וקצרות) כדי לתעד איזו געיה מקורה בכתב־היד שהוא היסוד למהדורה ואיזו נוספה על ידינו.",
    ],
]
_P5_H = [
    'לכן מסומנות הגעיות במהדורתנו לפי שני כתבי־\N{RIGHT-TO-LEFT MARK}היד העיקריים (הכתר וכתי"ל).',
    ' אמנם בעתיד היד נטויה לסימון געיות ע"פ שיטות נוספות.',
    " על ידי השימוש בתבניות אוטומטיות המיועדות לכך, יתאפשר למשתמש לבחור את השיטה המועדפת עליו.",
    " בין השיטות שראוי לבצע אותן ולאפשר את בחירתן על ידי המשתמש:",
]
_P5_ITEMS_H = [
    [
        'סימון געיות ע"פ כתבי־\N{RIGHT-TO-LEFT MARK}היד (הכתר וכתי"ל), אמנם בתיקונים קלים לגבי געיות חריגות בכתי"ל.',
        " זוהי השיטה המתבצעת כעת בספרי התורה.",
    ],
    [
        'סימון געיות ע"פ כתבי־\N{RIGHT-TO-LEFT MARK}היד (הכתר וכתי"ל) בלי תיקונים.',
        " זוהי השיטה המבוצעת כעת בספרי הנביאים והכתובים.",
        " בשיטה זו יש כבר ערך רב (כמו שקבע כהן בבהירות רבה), כי היא מייצגת באופן נאמן את המסורת הכללית המשתקפת בכתבי־היד העתיקים, והוא גם יכול להיות בסיס מצוין עבור פיתוח נוסף או יצירה נגזרת בעתיד (כגון בשיטות הבאות ברשימה זו).",
    ],
    [
        'סימון געיות ע"פ הכתר, וע"פ שחזור הכתר במקומות החסרים בו.',
        _footnote_marker(5),
    ],
    [
        'סימון לפי השיטה של "ריבוי געיות", שמקורה במנהג אשכנז והייתה מקובלת לרוב בדפוסים.',
        ' שיטה זו מתאימה ב"תיקון קוראים", שהרי ברוב העדות היום אין כבר ביצוע מוזיקלי לגעיה ונשאר לה רק תפקיד פונטי, ולכן ראוי לסמן אותה בכל תיבה הראויה לכך.',
        " אפשר לבסס סימון כזה (באופן כללי ובזהירות) על מהדורות ",
        author.anchor_h("היידנהיים", _URL_HEIDENHEIM),
        " (תורה) ו",
        author.anchor_h("בֶּר", _URL_BAER),
        ' (נ"ך), תוך כדי ניסוח כללים מתאימים שאינם בהכרח זהים לגמרי למדיניות שלהם.',
    ],
    [
        'סימון לפי השיטה של "ריבוי געיות", אמנם בדרך מתונה: אין לסמן יותר מגעיה אחת בלבד בתיבה אחת (בדומה למנהג כתבי־היד הטברנים).',
        " יישום זה יהיה דומה לשיטת ברויאר, אמנם יהיה צורך לבצע אותה מחדש.",
        ' גם שיטה זו מתאימה ב"תיקון קוראים" מאותה סיבה בדיוק כמו השיטה הקודמת.',
    ],
]
_BREUER_ARTICLE_H = "ספקות שאין להם הכרע"
_MS_LIST_H = "נוסח כתב היד"
_FTNTS_H = [
    [
        "סימנו געיות שהיו בכתר במקומות החסרים בו, והם ידועים לנו מתוך צילומים של אחדים מהדפים החסרים, או מתוך עדויות שנכתבו בזמן שכתב־היד עדיין היה שלם.",
    ],
    [
        'ראו במאמרו "ספקות שאין להם הכרע", ',
        author.emphasis("לשוננו"),
        ' נ"ח חוברת ד\', אלול תשנ"ד-תשנ"ה (1994), עמ\' 283-296; וברשימת "נוסח כתב היד" ב',
        author.emphasis("כתר ירושלים"),
        ".",
    ],
    [
        'מדובר על כתב־יד שנכתב על ידי הסופר שמואל בן יעקב, הסופר שכתב את נוסח האותיות בכתי"ל.',
        ' כתי"ל',
        mb_html.sup("מ"),
        ' קרוב לשיטתם של כתי"א וכתי"ל בסימון סוגים שונים של געיות, אך בחלק ניכר מהמקומות שטעה בהם בכתי"ל, הוא כתב את הגעיות כהלכתן בכתי"ל',
        mb_html.sup("מ"),
        "; ראו ברויאר, שם (הערה הקודמת).",
    ],
    [
        'מידע על געיות חריגות בכתי"ל בנביאים וכתובים, במקומות החסרים בכתר, משולב בתוך רשימת החריגים בנוסח הניקוד והטעמים בכתי"ל.',
    ],
    [
        'יש געיה בכתי"ל אך לא ברור אם היא שייכת לאות וי"ו או לאות ה"א, והשמטנו אותה ע"פ הרוב המכריע של כתבי־היד הקרובים לכתר.',
    ],
    [
        "לשיטה משוכללת לשחזור הגעיות בכתר, מעבר לשיטת כהן שכבר בא לידי ביצוע מלא ב",
        author.emphasis("מקראות גדולות הכתר"),
        ', ראו את מאמרו של רפאל זר על שחזור הגעיות בכרך תרי עשר במפעל המקרא של האונ\' עברית: Rafael Isaac (Singer) Zer, "The Preparation of the Base Text of the Hebrew University Bible Where It Is Missing in the Aleppo Codex", ',
        author.book_title("Textus"),
        " 25 (2010), pp. 49-71.",
    ],
]

_LM = ["L", mb_html.sup("M")]
_TIQQUN_QORIM = mb_html.span_c("tiqqun qorim", "romanized")
_SEC_E = "The text of the $gaya marks in our edition"
_P1_E = [
    author.emphasis("The $gaya marks according to the Leningrad Codex:"),
    " Our edition does not reconstruct all the $gaya marks in the places where the"
    " Aleppo Codex is missing (unlike Mikra'ot Gedolot ha-Keter).",
    " Nor does it add a $gaya to every word fit for one (unlike the marking of the ",
    author.emphasis("short"),
    " $gaya marks in Breuer's editions).",
    " Rather, we copied the $gaya marks as they are in the Aleppo Codex"
    " (where it survives)",
    _footnote_marker(0, "e"),
    " and in the Leningrad Codex (in most of the Torah, where the Aleppo Codex is"
    " missing).",
    " As a result, the $gaya marking in our edition generally corresponds to the"
    " marking of the ",
    author.emphasis("long"),
    " $gaya marks in Breuer's editions.",
    " (Breuer used the long form for the $gaya marks written in the manuscripts,"
    " to tell them apart.)",
]
_P2_E = [
    author.emphasis("The exceptions:"),
    " There are places in the Torah where the Leningrad Codex has a $gaya that is"
    " unexpected or contrary to the rules, or that is written on the wrong letter"
    " according to the rules.",
    " There are also places where it has two $gaya marks in one word"
    " (or in a $maqaf compound).",
    " Conversely, there are places where an obligatory $gaya is called for and is"
    " absent.",
    " And there are places where a $gaya is highly likely in light of the parallels"
    " (such as the $pashta $gaya) and is absent.",
    " Rabbi Breuer already recorded these anomalous $gaya marks in the Torah,"
    " at about 40 places.",
    _footnote_marker(1, "e"),
    " He corrected some of them in his later editions (Horev and the Jerusalem"
    " Crown), provided that he found support for doing so in ",
    _LM,
    ".",
    _footnote_marker(2, "e"),
    " In our edition we corrected ",
    author.emphasis("all"),
    " the anomalous $gaya marks that Breuer recorded in the Torah.",
    " We did so even in the minority of places where the anomalous text is also"
    " found in ",
    _LM,
    ", and we corrected dozens more places that Breuer did not note.",
    " At every such place we recorded in the documentation of the text what the"
    " Leningrad Codex has.",
    " We also tried to document the $gaya marks of other classic Tiberian"
    " manuscripts (",
    _he(_SIGLA_H),
    ").",
]
_P3_E = [
    author.emphasis("List of the exceptions:"),
    " Below is a list of the places in the Torah where we did ",
    author.emphasis("not"),
    " accept the Leningrad Codex's $gaya marks.",
    " For more on each item, including what other Tiberian manuscripts have,"
    " see the documentation of the text (in the chapters' editing pages).",
    _footnote_marker(3, "e"),
]
_P4_E = [
    "Despite all the exceptions (more than 80 items in the list), we kept the"
    " Leningrad Codex's $gaya marks in the overwhelming majority of the Torah and in"
    " the other places where the Aleppo Codex is missing.",
    " We did not try to bring them any closer to the $gaya marks the Aleppo Codex had"
    " (by a full reconstruction following all of the Aleppo Codex's tendencies in"
    " writing $gaya marks).",
    " There are two practical reasons for our decision to give only the $gaya marks"
    " recorded in the manuscripts (apart from the exceptional places):",
]
_P4_ITEMS_E = [
    [
        "Reconstructing the $gaya marks, or adding them to every word in Scripture fit"
        " for one, or both, takes a great deal of work.",
        " That is currently beyond our means, given the project's contributors.",
        " It will always be possible, however, to upgrade our edition in the future in"
        " one of these ways, or to carry them out in derivative editions.",
    ],
    [
        "Adding $gaya marks fully and consistently, as in Breuer's edition, is also"
        " impossible at present for a technical reason.",
        " Unicode today has no separate characters for the different $gaya marks"
        " (long and short).",
        " Such characters would be needed to record which $gaya comes from the"
        " manuscript that is the edition's base and which one we added.",
    ],
]
_P5_E = [
    "Therefore the $gaya marks in our edition follow the two principal manuscripts"
    " (the Aleppo Codex and the Leningrad Codex).",
    " For the future, however, we intend to mark $gaya marks by further methods"
    " as well.",
    " Automatic templates designed for the purpose will let the user choose the"
    " method they prefer.",
    " Among the methods worth carrying out and offering for the user to choose:",
]
_P5_ITEMS_E = [
    [
        "Marking $gaya marks according to the manuscripts (the Aleppo Codex and the"
        " Leningrad Codex), but with slight corrections to anomalous $gaya marks in"
        " the Leningrad Codex.",
        " This is the method now carried out in the books of the Torah.",
    ],
    [
        "Marking $gaya marks according to the manuscripts (the Aleppo Codex and the"
        " Leningrad Codex), without corrections.",
        " This is the method now carried out in the books of the Prophets and the"
        " Writings.",
        " This method already has great value (as ",
        _ait("Menachem"),
        " Cohen established with great clarity), because it faithfully represents the"
        " general tradition reflected in the ancient manuscripts.",
        " It can also be an excellent basis for further development or derivative"
        " work in the future (such as the methods that follow in this list).",
    ],
    [
        "Marking $gaya marks according to the Aleppo Codex, and according to a"
        " reconstruction of the Aleppo Codex where it is missing.",
        _footnote_marker(5, "e"),
    ],
    [
        "Marking by the method of ",
        author.dquote("abundant $gaya marks"),
        ", which originated in Ashkenazi custom and was generally accepted in the"
        " printed editions.",
        " This method suits a ",
        _TIQQUN_QORIM,
        ", since in most communities today the $gaya no longer has a musical"
        " rendition and keeps only a phonetic function.",
        " It is therefore fitting to mark it on every word fit for one.",
        " Such marking can be based (in general terms, and with caution) on the"
        " editions of ",
        author.anchor_h("Heidenheim", _URL_HEIDENHEIM),
        " (Torah) and ",
        author.anchor_h("Baer", _URL_BAER),
        " (Prophets and Writings).",
        " Suitable rules would have to be formulated along the way, and they need not"
        " match those editions' policies in every respect.",
    ],
    [
        "Marking by the method of ",
        author.dquote("abundant $gaya marks"),
        ", but in a moderate form: no more than a single $gaya is to be marked in one"
        " word (like the practice of the Tiberian manuscripts).",
        " This implementation would resemble Breuer's method, though it would have to"
        " be carried out anew.",
        " This method too suits a ",
        _TIQQUN_QORIM,
        ", for exactly the same reason as the previous one.",
    ],
]
_FTNTS_E = [
    [
        "We marked $gaya marks that the Aleppo Codex had in places now missing from"
        " it.",
        " They are known to us from photographs of some of the missing pages, or from"
        " testimonies written while the manuscript was still complete.",
    ],
    [
        "See his article ",
        author.dquote(_he(_BREUER_ARTICLE_H)),
        " (",
        author.dquote("Doubts That Cannot Be Resolved"),
        "), ",
        author.book_title("Leshonenu"),
        " 58, no. 4, Elul 5754–5755 (1994), pp. 283–296.",
        " See also the list ",
        author.dquote(_he(_MS_LIST_H)),
        " (",
        author.dquote("The Text of the Manuscript"),
        ") in the Jerusalem Crown.",
    ],
    [
        "This is a manuscript written by the scribe Samuel ben Jacob, the scribe who"
        " wrote the consonantal text of the Leningrad Codex.",
        " In marking the various kinds of $gaya, ",
        _LM,
        " is close to the practice of the Aleppo Codex and the Leningrad Codex.",
        " But at a considerable share of the places where he erred in the Leningrad"
        " Codex, he wrote the $gaya marks correctly in ",
        _LM,
        ".",
        " See Breuer, ibid. (previous note).",
    ],
    [
        "Information on the Leningrad Codex's anomalous $gaya marks in the Prophets and"
        " Writings, in the places where the Aleppo Codex is missing, is integrated into"
        " the list of anomalies in the Leningrad Codex's pointing and accents ",
        _ait("in chapter 4"),
        ".",
    ],
    [
        "The Leningrad Codex has a $gaya, but it is unclear whether it belongs to the"
        " $vav or the $hehe.",
        " We omitted it, following the overwhelming majority of the manuscripts close"
        " to the Aleppo Codex.",
    ],
    [
        "For a more refined method of reconstructing the Aleppo Codex's $gaya marks,"
        " beyond Cohen's method (which has already been carried out in full in"
        " Mikra'ot Gedolot ha-Keter), see Rafael Zer's article on reconstructing the"
        " $gaya marks in the Twelve Prophets volume of the Hebrew University Bible"
        " Project: Rafael Isaac (Singer) Zer, ",
        author.dquote(
            "The Preparation of the Base Text of the Hebrew University Bible Where It"
            " Is Missing in the Aleppo Codex"
        ),
        ", ",
        author.book_title("Textus"),
        " 25 (2010), pp. 49–71.",
    ],
]
_TRANSLATION_NOTES = [
    [
        "The source's word for the mark is $gaya.",
        " The heading of the section that contains this one, ",
        _he("סימון הגעיה (המתג)"),
        ", equates it with the $meteg (U+05BD).",
        " The English keeps the Hebrew word, as this site's translation of the"
        " gray-$maqaf section does.",
    ],
    [
        _LM,
        " renders the source's ",
        _he('כתי"ל'),
        " with a superscript ",
        _he("מ"),
        ", Breuer's siglum.",
        " The introduction's appendices identify it as the Lehmann manuscript of the"
        " Torah, formerly manuscript 14 of the Karaite synagogue in Cairo, and say"
        " that its whereabouts are unknown today, so every report of its $gaya marks"
        " comes from Breuer.",
    ],
    [
        "The sigla: ",
        _he("ל1"),
        " is Firkovich B17; ",
        _he("ב"),
        ", British Library Or. 4445; ",
        _he("ש"),
        ", Sassoon 507; ",
        _he("ש1"),
        ", Sassoon 1053; ",
        _he("ק3"),
        ", Cairo 18; and ",
        _he("ו"),
        ", the Washington Pentateuch (Museum of the Bible Ms. 882).",
    ],
    [
        "In the tables, ",
        author.dquote("(?)"),
        " marks the source's ",
        _he("ל?="),
        ".",
        " By the convention the introduction states for its lists of places where"
        " $MAM departs from a manuscript's pointing and accents, the manuscript's text"
        " there is in doubt: blurred, ambiguous, or corrected.",
        " A ",
        author.dquote("[2]"),
        " is the source's too, and means the form's second occurrence in the verse.",
        " At Genesis 18:15 the source has $MAM's narrow-sense $paseq template, shown"
        " here as ",
        _he("׀"),
        ".",
        " The Hebrew column leaves out the source's links to other Wikisource pages,"
        " among them the links from each book and verse to $MAM's chapter pages.",
    ],
    _counts_note(),
]
####################################
_WS_BASE = "https://he.wikisource.org/wiki/" "ויקיטקסט:מבוא_למקרא_על_פי_המסורה/פרק_ג"
_WS_URL = f"{_WS_BASE}#נוסח_הגעיות_במהדורתנו"
_WS_LINK = author.anchor_h("Hebrew Wikisource", _WS_URL)
_WS_REVISION_URL = "https://he.wikisource.org/w/index.php?oldid=3079273"
####################################
# fmt: off
_TRIPLES = [
    ("Section heading", author.para_modhe(_SEC_H), author.para(_SEC_E)),
    ("The Leningrad Codex as the basis",
     author.para_modhe(_P1_H), author.para(_P1_E)),
    ("The exceptions", author.para_modhe(_P2_H), author.para(_P2_E)),
    ("List of the exceptions", author.para_modhe(_P3_H), author.para(_P3_E)),
    *[(None, _book_para_h(book), _book_cell_e(book)) for book in _BOOKS],
    ("Why the rest stays as the manuscripts have it",
     [author.para_modhe(_P4_H), _ol_h(_P4_ITEMS_H)],
     [author.para(_P4_E), author.ordered_list(_P4_ITEMS_E)]),
    ("Methods for the future",
     [author.para_modhe(_P5_H), _ol_h(_P5_ITEMS_H)],
     [author.para(_P5_E), author.ordered_list(_P5_ITEMS_E)]),
]
# fmt: on

_TITLE = "געיה marks in MAM"
_H1_CONTENTS = "$gaya marks in $MAM"
_FNAME = "he_ws_intro_to_mam_gaya_text.html"
_CAVEAT_PAREN = "(AI-generated translation, not yet reviewed by a human)"
_CAVEAT = author.para(
    [
        author.emphasis("AI-generated translation, not yet reviewed by a human."),
        " Claude, an AI model, translated this section into English on 2026-09-25.",
        " No human has reviewed the translation yet, so read it as a draft.",
        " The Hebrew column is the source's text.",
    ],
    {"class": "ai-caveat"},
)
_PROVENANCE = author.para(
    [
        "The Hebrew text below is from Avi Kadish's introduction to the",
        " Miqra al pi ha-Masora edition (Chapter 3) on ",
        _WS_LINK,
        ", as of ",
        author.anchor_h("revision 3079273", _WS_REVISION_URL),
        " (2026-08-26). The English translation is original to this project.",
    ]
)
_FTNT_TRIPLES = [
    _ftnt_triple(n, h, e) for n, (h, e) in enumerate(zip(_FTNTS_H, _FTNTS_E))
]
_CBODY = [
    author.heading_level_1(_H1_CONTENTS),
    _CAVEAT,
    _PROVENANCE,
    author.he_en_table_wct(_TRIPLES),
    author.heading_level_2(f"Footnotes (B={_FN_BASE})"),
    author.he_en_table_wct(_FTNT_TRIPLES),
    author.heading_level_2("Notes on the translation"),
    author.para("These notes are Claude's, not the source's."),
    author.unordered_list(_TRANSLATION_NOTES),
]
