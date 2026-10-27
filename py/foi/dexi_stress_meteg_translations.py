"""English translations of the documentation notes on the dexi-stress-meteg FOI page.

Each translation stores the note it translates, its lemma and parts exactly as
MAM-with-doc shows them, with one English part for each part. A row whose note is not
stored here raises, so that a changed note or a new row gets a revised translation
rather than a stale one or none. Nothing checks for a translation that no row uses:
such a check would pin the population of notes, and a vanished row already shows in
the page's own diff. Each Hebrew word in an English part is quoted from the part it
translates. The English omits the lemma, which the row shows beside the note.

The English names each source rather than giving its siglum, as
in/near-aleppo/qere-without-ketiv-mam-notes-en.json does; ק-מ is Cambridge Add. 1753,
as doc/sigil-decoding.md says. A question mark after a siglum, which MAM's
introduction (in/mam-ws-intro/ch5.mediawiki) uses for a reading that is only in doubt,
becomes "doubtfully"; a question mark after a pair of accents stays. A part that opens
with "=" says that MAM agrees with the sources it names.

The translations are AI-generated. Claude, an AI model, wrote them on 2026-10-27, at
Ben Denckla's request, and no human has reviewed them yet. The page says so in its
introduction and under each translation. Remove those caveats and this paragraph only
once a human has reviewed the translations.
"""

import re

from mb_misc import mb_html

# A run of Hebrew, with the spaces between its words, as near_aleppo's
# foi_qere_without_ketiv defines one.
_HEBREW_RUN = re.compile(r"([\u0590-\u05ff]+(?: +[\u0590-\u05ff]+)*)")
_HEBREW = {"lang": "hbo", "dir": "rtl"}
_CAVEAT = mb_html.para(
    mb_html.emphasis("AI-generated translation, not yet reviewed by a human.")
)


def english_note(note):
    """Return the English translation of the note, a note as MAM-with-doc shows it,
    followed by the caveat that no human has reviewed the translation."""
    lemma, hebrew_parts = _lemma_and_parts(note)
    english_parts = _BY_NOTE.get((lemma, hebrew_parts))
    if english_parts is None:
        raise ValueError(
            f"{__name__} has no translation of the note on {lemma}"
            f" with the parts {hebrew_parts}"
        )
    part_0, *others = (
        _with_hebrew_spans(english, hebrew)
        for hebrew, english in zip(hebrew_parts, english_parts, strict=True)
    )
    if others:
        return (*part_0, mb_html.unordered_list(others), _CAVEAT)
    return (*part_0, _CAVEAT)


def _lemma_and_parts(note):
    """The note's lemma and its parts, as strings. A note is a span of its lemma, a
    space, a span of its part 0 and, if it has other parts, a list of those."""
    if len(note) not in (3, 4) or note[1] != " ":
        raise ValueError(f"unexpected note: {note!r}")
    lemma = _string(note[0], "span", {"class": "mam-doc-lemma"})
    parts = [_string(note[2], "span", {"class": "mam-doc-part-0"})]
    if len(note) == 4:
        parts.extend(_string(item, "li") for item in _items(note[3]))
    return lemma, tuple(parts)


def _items(parts_list):
    """The items of the list of a note's other parts."""
    if not (
        _is_element(parts_list, "ul", {"class": "mam-doc-parts"})
        and parts_list["contents"]
    ):
        raise ValueError(f"unexpected list of a note's parts: {parts_list!r}")
    return parts_list["contents"]


def _string(element, tag, attr=None):
    """The one string that the element, a tag element with attr, holds."""
    if not (
        _is_element(element, tag, attr)
        and len(element["contents"]) == 1
        and isinstance(element["contents"][0], str)
    ):
        raise ValueError(f"unexpected {tag} in a note: {element!r}")
    return element["contents"][0]


def _is_element(obj, tag, attr):
    keys = {"_htel_tag", "contents"} | ({"attr"} if attr else set())
    return (
        mb_html.is_htel(obj)
        and set(obj) == keys
        and mb_html.htel_get_tag(obj) == tag
        and obj.get("attr") == attr
    )


def _with_hebrew_spans(english, hebrew):
    """The English part, with each run of Hebrew in it in a span of its own; each such
    run must be quoted from the Hebrew part."""
    contents = []
    for run in filter(None, _HEBREW_RUN.split(english)):
        if not _HEBREW_RUN.fullmatch(run):
            contents.append(run)
        elif run in hebrew:
            contents.append(mb_html.span(run, _HEBREW))
        else:
            raise ValueError(f"{run} is not quoted from the note's part {hebrew}")
    return contents


def _by_note(translations):
    """The English parts of each note, by the note's lemma and Hebrew parts."""
    by_note = {}
    for lemma, pairs in translations:
        hebrew_parts, english_parts = zip(*pairs)
        if (lemma, hebrew_parts) in by_note:
            raise ValueError(f"{__name__} translates the note on {lemma} twice")
        by_note[lemma, hebrew_parts] = english_parts
    return by_note


# One (lemma, ((hebrew_part, english_part), ...)) for each note, in the order of the
# books.
_TRANSLATIONS = (
    # Ps44:27
    (
        "ק֭וּמָֽ֭ה",
        (
            (
                "=א?,ל ובדפוסים (דחי וקו של געיה להורות על מקום הטעם, וכך הכריעו במג״ה)",
                "MAM agrees with the Aleppo Codex (doubtfully), the Leningrad Codex and the printed editions (deḥi, and a ga'ya stroke to show where the stress is; and so Mikra'ot Gedolot ha-Keter decided).",
            ),
            (
                "א?=ק֭וּמָ֥ה (הקו קצת נטוי כמרכא, וכן הכריע ברויאר בשתי מהדורותיו האחרונות ועל פיו במכון ממרא)",
                "The Aleppo Codex (doubtfully) has ק֭וּמָ֥ה (the stroke slants slightly, like a merkha; and so Breuer decided in his last two editions, and Mechon Mamre follows him).",
            ),
        ),
    ),
    # Ps57:9
    (
        "ע֭וּרָֽ֭ה",
        (
            (
                "=א?,ל? (קו של דחי וקו של געיה להורות על מקום הטעם) וכך במהדורותיו הראשונות של ברויאר (מוסד הרב קוק וחורב) ובמג״ה ובדפוסים וקורן וסימנים. והשוו לפסוק המקביל בתהלים קח,ג (שם הקווים לדחי ולגעיה ברורים).",
                "MAM agrees with the Aleppo Codex and the Leningrad Codex, both doubtfully (a deḥi stroke, and a ga'ya stroke to show where the stress is), as do Breuer's first editions (Mossad HaRav Kook and Horev), Mikra'ot Gedolot ha-Keter, the printed editions, Koren and the Simanim Tanakh. Compare the parallel verse, Psalms 108:3 (there the strokes for the deḥi and the ga'ya are clear).",
            ),
            (
                "א?,ל?=ע֖וּרָ֥ה (טרחא ומרכא?); וראו ברויאר, טעמי המקרא, יא.43 עמ' 285 על טרחא ומרכא כשני המשרתים הסמוכים לרביע. וכך נדפס אצל ברויאר בכתר ירושלים וכמו כן במכון ממרא.",
                "The Aleppo Codex and the Leningrad Codex, both doubtfully, have ע֖וּרָ֥ה (tarḥa and merkha?); see Breuer, Ta'amei HaMiqra, 11.43, p. 285, on tarḥa and merkha as the two conjunctives nearest revia. Breuer's Jerusalem Crown has it so, as does Mechon Mamre.",
            ),
        ),
    ),
    # Ps69:29
    (
        "יִ֭מָּחֽ֭וּ",
        (
            (
                "א?,ל (דחי וקו של געיה להורות על מקום הטעם); הקו קצת נטוי כמרכא אך גם יכול להיות געיה (וכך במג״ה).",
                "MAM agrees with the Aleppo Codex (doubtfully) and the Leningrad Codex (deḥi, and a ga'ya stroke to show where the stress is); the stroke slants slightly, like a merkha, but it could also be a ga'ya (and so Mikra'ot Gedolot ha-Keter has it).",
            ),
            (
                "א?=יִ֭מָּח֥וּ (דחי ומרכא?); וכך הכריע ברויאר ובעקבותיו במכון ממרא",
                "The Aleppo Codex (doubtfully) has יִ֭מָּח֥וּ (deḥi and merkha?); and so Breuer decided, and Mechon Mamre follows him.",
            ),
        ),
    ),
    # Ps86:7
    (
        "צָ֭רָתִֽ֭י",
        (
            (
                "=א?,ל?,ש1? (דחי וקו של געיה להורות על מקום הטעם), וכך במהדורתו הראשונה של ברויאר (מוסד הרב קוק) ובמג״ה, וכמו כן בדפוסים וקורן וסימנים",
                "MAM agrees with the Aleppo Codex, the Leningrad Codex and Sassoon 1053, all doubtfully (deḥi, and a ga'ya stroke to show where the stress is), as do Breuer's first edition (Mossad HaRav Kook) and Mikra'ot Gedolot ha-Keter, and likewise the printed editions, Koren and the Simanim Tanakh.",
            ),
            (
                'א?,ל?,ש1?=צָ֭רָתִ֥י (דחי ומרכא?); הקו די נוטה לשמאל בכתבי־היד הקרובים, חוץ מכתי"ק-מ שאין בו קו בכלל באות תי״ו (צָ֭רָתִי), עובדה שמצביעה על געיה ולא מרכא. במהדורותיו האחרונות של ברויאר (חורב וכתר ירושלים) נדפסה התיבה במרכא, וכן במכון ממרא.',
                "The Aleppo Codex, the Leningrad Codex and Sassoon 1053, all doubtfully, have צָ֭רָתִ֥י (deḥi and merkha?); the stroke leans rather to the left in the closely related manuscripts, except Cambridge Add. 1753, which has no stroke at all on the letter tav (צָ֭רָתִי), a fact that points to ga'ya and not merkha. Breuer's last editions (Horev and the Jerusalem Crown) have the word with merkha, and so does Mechon Mamre.",
            ),
        ),
    ),
    # Ps108:3
    (
        "ע֭וּרָֽ֭ה",
        (
            (
                "=א?,ל (קו של דחי וקו של געיה להורות על מקום הטעם), וכך במהדורותיו הראשונות של ברויאר (מוסד הרב קוק וחורב) ובמג״ה, וכמו כן בדפוסים וקורן וסימנים. והשוו לפסוק המקביל בתהלים נז,ט (שם הקווים לדחי ולגעיה פחות ברורים).",
                "MAM agrees with the Aleppo Codex (doubtfully) and the Leningrad Codex (a deḥi stroke, and a ga'ya stroke to show where the stress is), as do Breuer's first editions (Mossad HaRav Kook and Horev) and Mikra'ot Gedolot ha-Keter, and likewise the printed editions, Koren and the Simanim Tanakh. Compare the parallel verse, Psalms 57:9 (there the strokes for the deḥi and the ga'ya are less clear).",
            ),
            (
                "א?=ע֖וּרָ֥ה (טרחא ומרכא?); וראו ברויאר, טעמי המקרא, יא.43 עמ' 285 על טרחא ומרכא כשני המשרתים הסמוכים לרביע. וכך נדפס אצל ברויאר בכתר ירושלים וכמו כן במכון ממרא.",
                "The Aleppo Codex (doubtfully) has ע֖וּרָ֥ה (tarḥa and merkha?); see Breuer, Ta'amei HaMiqra, 11.43, p. 285, on tarḥa and merkha as the two conjunctives nearest revia. Breuer's Jerusalem Crown has it so, as does Mechon Mamre.",
            ),
        ),
    ),
    # Ps138:3
    (
        "קָ֭רָֽ֭אתִי",
        (
            (
                "=א?,ל (דחי וקו של געיה להורות על מקום הטעם) וכך במג״ה",
                "MAM agrees with the Aleppo Codex (doubtfully) and the Leningrad Codex (deḥi, and a ga'ya stroke to show where the stress is), as does Mikra'ot Gedolot ha-Keter.",
            ),
            (
                "א?=קָ֭רָ֥אתִי (דחי ומרכא?) וכך אצל ברויאר",
                "The Aleppo Codex (doubtfully) has קָ֭רָ֥אתִי (deḥi and merkha?), and Breuer has the same.",
            ),
        ),
    ),
    # Ps139:7
    (
        "אָ֭נָֽ֭ה",
        (
            (
                '=א?,ל?,ק-מ? (דחי וקו של געיה להורות על מקום הטעם), וכך במהדורתו הראשונה של ברויאר (מוסד הרב קוק) ובמג״ה, וכמו כן בדפוסים וקורן וסימנים. הקו די ישר בכתר ובכי"ל, אך נטוי באופן ניכר בכתי"ק-מ. בכתי״ש1 אין קו בכלל באות נו״ן (אָ֭נָה), עובדה שמצביעה על געיה ולא מרכא.',
                "MAM agrees with the Aleppo Codex, the Leningrad Codex and Cambridge Add. 1753, all doubtfully (deḥi, and a ga'ya stroke to show where the stress is), as do Breuer's first edition (Mossad HaRav Kook) and Mikra'ot Gedolot ha-Keter, and likewise the printed editions, Koren and the Simanim Tanakh. The stroke is fairly straight in the Aleppo Codex and the Leningrad Codex, but noticeably slanted in Cambridge Add. 1753. Sassoon 1053 has no stroke at all on the letter nun (אָ֭נָה), a fact that points to ga'ya and not merkha.",
            ),
            (
                "א?,ל?,ק-מ?=אָ֭נָ֥ה (דחי ומרכא?); במהדורותיו האחרונות של ברויאר (חורב וכתר ירושלים) נדפסה התיבה במרכא וכן במכון ממרא.",
                "The Aleppo Codex, the Leningrad Codex and Cambridge Add. 1753, all doubtfully, have אָ֭נָ֥ה (deḥi and merkha?); Breuer's last editions (Horev and the Jerusalem Crown) have the word with merkha, and so does Mechon Mamre.",
            ),
        ),
    ),
    # Pr13:25
    (
        "אֹ֭כֵֽ֭ל",
        (
            (
                "=א?,ש1 (דחי וקו של געיה להורות על מקום הטעם); למרות שקו הגעיה קצת נטוי, אין הכרח לראות בו מרכא (וכן הכריעו ברויאר במהדורתו הראשונה ומג״ה)",
                "MAM agrees with the Aleppo Codex (doubtfully) and Sassoon 1053 (deḥi, and a ga'ya stroke to show where the stress is); although the ga'ya stroke slants slightly, there is no need to read it as a merkha (and so Breuer decided in his first edition, as did Mikra'ot Gedolot ha-Keter).",
            ),
            (
                "אמנם לפי ברויאר א=אֹ֭כֵ֥ל (דחי ומרכא) בשתי מהדורותיו האחרונות (וכן במכון ממרא)",
                "However, according to Breuer in his last two editions, the Aleppo Codex has אֹ֭כֵ֥ל (deḥi and merkha), and Mechon Mamre has the same.",
            ),
            (
                "ל=אֹ֭כֵל (דחי בלבד) וכמו כן בדפוסים ובקורן",
                "The Leningrad Codex has אֹ֭כֵל (deḥi alone), and so do the printed editions and Koren.",
            ),
        ),
    ),
    # Jb29:16
    (
        "אָ֭נֹכִֽ֭י",
        (
            (
                "=א?,ל (דחי וקו של געיה להורות על מקום הטעם); למרות שקו הגעיה קצת נטוי, אין הכרח לראות בו מרכא (וכן הכריעו ברויאר במהדורתו הראשונה ומג״ה)",
                "MAM agrees with the Aleppo Codex (doubtfully) and the Leningrad Codex (deḥi, and a ga'ya stroke to show where the stress is); although the ga'ya stroke slants slightly, there is no need to read it as a merkha (and so Breuer decided in his first edition, as did Mikra'ot Gedolot ha-Keter).",
            ),
            (
                "אמנם לפי ברויאר א=אָ֭נֹכִ֥י (דחי ומרכא) בשתי מהדורותיו האחרונות (וכן במכון ממרא)",
                "However, according to Breuer in his last two editions, the Aleppo Codex has אָ֭נֹכִ֥י (deḥi and merkha), and Mechon Mamre has the same.",
            ),
            (
                "ש1=אָ֭נֹכִי (דחי בלבד) וכן בדפוסים (קורן=אָֽ֭נֹכִי דחי וגעיה באל״ף)",
                "Sassoon 1053 has אָ֭נֹכִי (deḥi alone), and so do the printed editions (Koren has אָֽ֭נֹכִי, deḥi and ga'ya on the alef).",
            ),
        ),
    ),
)
_BY_NOTE = _by_note(_TRANSLATIONS)
