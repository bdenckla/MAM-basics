"""Hebrew footnote content and English translations for the pasleg document.

Footnotes are indexed 0–26, corresponding to B+0 through B+26 in pasleg.py
(where _FN_BASE is defined).
"""

from py_misc import my_html
from pyauthor_util import author


def _ait(contents):
    """Added In Translation, i.e. not in original, i.e. square-bracketed (and gray)"""
    return author.span_gray(["[", contents, "]"])


def _bv(book, verses):
    """Book + verses: li content with book name and nested verse ul."""
    return [book, author.unordered_list(verses)]


FTNT_0_H = [
    "על צורתו של הקו ראו ייבין, המסורה למקרא, פרק תשיעי 305 (עמ' 178):",
    ' "הקו שאחר התיבה המוטעמת לגרמיה הוא קו מאונך.',
    " בכתבי־היד מידתו כחצי גובה אות,",
    " והוא בא על פי רוב בגובה חלקן העליון של האותיות,",
    " אך לעתים גם בגובה אמצען או בגובה חלקן התחתון.",
    ' בדפוסים אורכו כגובה אות."',
    " ולגבי הפסק ראו שם 311 (עמ' 180):",
    ' "פָּסֵק, פְּסִיק, הוא קו מאונך הבא אחרי התיבה,',
    ' ברווח שבינה לבין זו שאחריה."',
]
FTNT_0_E = [
    "On the form of the line see Yeivin,",
    " Introduction to the Tiberian Masorah, ch. 9, 305 (p. 178):",
    ' "The line after the word accented with $legarmeh is a vertical line.',
    " In manuscripts its length is about half the height of a letter,",
    " and it usually appears at the height of the upper part of the letters,",
    " but sometimes at the middle or at the lower part.",
    ' In printed editions its length is the height of a letter."',
    " Regarding $paseq see ibid. 311 (p. 180):",
    [
        ' "$Paseq, ',
        author.span_gray(["[aka]"]),
        " ",
        my_html.span_c("pesiq", "romanized"),
        ", is a vertical line that comes after the word,",
    ],
    ' in the space between it and the following word."',
]
FTNT_1_H = [
    'ראו ייבין, שם, שהפסק "מסומן אחר תיבה המוטעמת בטעם מחבר,',
    " ומורה שיש להפסיק בקריאתה הפסקה כלשהי,",
    " אך לא עד כדי הפיכת הטעם המחבר לטעם מפסיק.",
    " הפָּסֵק הותקן כנראה לאחר התקנת מערכת הטעמים,",
    " המחברים והמפסיקים,",
    " ובא להשלימה במקומות שבהם מערכת זו לא הספיקה.",
    " התקנתו המאוחרת ביחס עשויה להסביר",
    ' את חוסר השיטתיות שבסימונו."',
    " וראו גם את דבריו של ברויאר, טעמי המקרא ו.1 (עמ' 128):",
    ' "המסורה מכירה רק סימן אחד,',
    " המורה על הפסקה בלבד \N{EN DASH} בלא כל משמעות מוסיקלית",
    " \N{EN DASH} והוא הפָּסֵק.",
    " צורת הפסק הוא קו מאונך, המפריד בין שתי תיבות.",
    " עצם מקומו של הפסק מעיד עליו,",
    " שהוא סימן להפסקה, ולא סימן נגינה;",
    " שהרי אין הוא מסומן מתחת לתיבה על מעליה",
    " \N{EN DASH} ככל טעמי המקרא \N{EN DASH}",
    " אלא הוא מסומן אחרי התיבה.",
    " ומכאן, שהפסק מורה על הפסקת הקריאה הבאה אחרי המלה;",
    " ואילו המפסיק והמשרת מורים על הנגינה,",
    ' המלוה את המלה עצמה."',
    " והעיר שם ברויאר על חוסר הנגינה:",
    ' משום כך אמרו על פסק ש"לא נמנה עם הטעמים (=המפסיקים)',
    ' ולא עם המשרתים"',
    " (משפטי הטעמים ח' ע\"א).",
]
FTNT_1_E = [
    ("p", ["See Yeivin, ibid., on $paseq:"]),
    (
        "bq",
        [
            [author.span_gray(["[$Paseq]"]), " is marked after a word"],
            " accented with a conjunctive accent,",
            " and indicates that there should be some kind of pause in its reading,",
            " but not to the extent of turning the conjunctive accent",
            " into a disjunctive accent.",
            " $Paseq was apparently instituted after the accentuation system",
            " \N{EN DASH} both conjunctive and disjunctive \N{EN DASH}",
            " and came to supplement it where the system was insufficient.",
            " Its relatively late institution may explain",
            " the lack of systematicity in its marking.",
        ],
    ),
    ("p", ["See also Breuer, Ta'amei HaMiqra 6.1 (p. 128):"]),
    (
        "bq",
        [
            "The Masorah recognizes only one sign",
            " that indicates a pause alone",
            " \N{EN DASH} without any musical significance",
            " \N{EN DASH} and that is $paseq.",
            " The form of $paseq is a vertical line",
            " separating two words.",
            " The very placement of $paseq testifies to its nature",
            " as a pause sign, not a melodic sign;",
            " for it is not marked beneath or above the word",
            " \N{EN DASH} as are all the biblical accents \N{EN DASH}",
            " but rather after the word.",
            " Hence, $paseq indicates a pause in the reading",
            " that comes after the word;",
            " whereas the disjunctive and conjunctive accents indicate",
            " the melody accompanying the word itself.",
        ],
    ),
    (
        "p",
        [
            "Breuer noted there regarding the lack of melody:",
            ' for this reason they said of $paseq that "it is not counted',
            " among the accents (= disjunctives)",
            ' nor among the conjunctives"',
            " (Mishpetei HaTe'amim 8a).",
        ],
    ),
]
FTNT_2_H = [
    "משרתו של מונח לגרמיה הוא בדרך כלל מרכא,",
    " ורק לעתים רחוקות יש לו שני משרתים",
    " (מונח ומרכא, מרכא ומרכא, אזלא ומרכא).",
    ' על משרתיו של הטעם "מונח לגרמיה"',
    " ראו ברויאר, טעמי המקרא, ג.1 (עמ' 83);",
    " ייבין, המסורה למקרא, פרק תשיעי 309\N{EN DASH}310 (עמ' 180).",
]
FTNT_2_E = [
    "The conjunctive accent of $munleg is usually $merkha,",
    " and only rarely does it have two conjunctive accents",
    " ($munax and $merkha, $merkha and $merkha,",
    " $azla and $merkha).",
    " On the conjunctive accents of $munleg",
    " see Breuer, Ta'amei HaMiqra, 3.1 (p. 83);",
    " Yeivin, Introduction to the Tiberian Masorah,",
    " ch. 9, 309\N{EN DASH}310 (p. 180).",
]
FTNT_3_H = [
    "ראו ייבין, המסורה למקרא, 308 (עמ' 179):",
    ' "ויש כתבי־יד, בייחוד אלו שבניקוד מורחב,',
    " המעירים בגיליון על כל קו מאונך",
    " אם הוא פסק (פס֗, פ֗) או לגרמיה (לגר֗, לג֗).",
    " גם בכתבי־יד שאינם מעירים דרך שיטה,",
    " יש הערות במקומות שעשויים לטעוֹת בהם.",
    ' כך, למשל, במס"ק ל מעירים "ל֗ג֗ר֗"',
    " בשני המקומות שבהם טעם זה בא לפני פזר (עיין למעלה),",
    ' וביש\' מב, ה, מעירים "פ֗ס֗ק֗."',
]
FTNT_3_E = [
    "See Yeivin, Introduction to the Tiberian Masorah,",
    ' 308 (p. 179): "There are manuscripts,',
    " especially those with expanded vocalization,",
    " that annotate in the margin every vertical line",
    [
        " as either $paseq (",
        author.hbo("פס֗"),
        ", ",
        author.hbo("פ֗"),
        ") or $legarmeh (",
        author.hbo("לגר֗"),
        ", ",
        author.hbo("לג֗"),
        ").",
    ],
    " Even in manuscripts that do not annotate systematically,",
    " there are annotations in places prone to error.",
    " Thus, for example, in the Masorah Parva of L",
    [" they annotate ", author.dquote([author.hbo("ל֗ג֗ר֗")])],
    " in the two places where this accent comes before $pazer",
    " (see above),",
    [" and in Isa. 42:5, they annotate ", author.dquote([author.hbo("פ֗ס֗ק֗")]), "."],
]
FTNT_4_H = [
    "לעתים רחוקות הנוסח שונה,",
    " ואז הכרענו לפי כתר ארם צובה.",
    " לדוגמה: ביהושע טו,יח יש קו מאונך של מונח לגרמיה",
    ' בכתר ארם צובה ובמקראות גדולות דפוס ונציה (רפ"ו),',
    " אבל הוא חסר בפסוק המקביל בשופטים א,יד.",
    ' בכתבי־יד אחרים (כתי"ל וכתי"ק וכתי"ש1)',
    " הקו חסר בשני המקומות.",
    " הפסוק ביהושע מובא ברשימת הלגרמיה של גינצבורג",
    " (ראו כאן למקורותיה),",
    " אבל ברשימת ויקס השמיט אותו בכוונה",
    " (ראו שם דיון בהערה 27);",
    " וראו עוד ברשימת ברויאר, טעמי המקרא, ו.11",
    " (עמ' 137\N{EN DASH}140), ושם בהערה 9 (עמ' 138).",
]
FTNT_4_E = [
    "Rarely the text differs,",
    " but when it does we decided according to the Aleppo Codex.",
    " For example: in Joshua 15:18 there is a $munleg vertical line",
    " in the Aleppo Codex and in the Venice Rabbinic Bible (1525\N{EN DASH}1526),",
    " but it is absent in the parallel verse in Judges 1:14.",
    " In other manuscripts (Leningrad, Cairo, and Sassoon 1053)",
    " the line is absent in both places.",
    " The verse in Joshua appears in Ginsburg's $legarmeh list",
    " (see there for its sources),",
    " but in Wickes's list he omitted it intentionally",
    " (see the discussion there in note 27);",
    " see also Breuer's list, Ta'amei HaMiqra, 6.11",
    " (pp. 137\N{EN DASH}140), and note 9 there (p. 138).",
]
FTNT_5_H = [
    "לעתים יש אי-התאמות בין רשימות הפסק השונות,",
    ' ואז בדרך כלל נתנו עדיפות לרשימות הפסק בתוך כתי"ל',
    " (בסוף התורה, בסוף הנביאים, ובסוף הכתובים);",
    " התחשבנו בפריטים המובאים בהן ובפריטים הנעדרים מהן,",
    " ובמיוחד כאשר הנתונים שבהן תואמים לקביעות אחרות של המסורה.",
    " אבל כל מקרה נדון לגופו.",
]
FTNT_5_E = [
    "Sometimes there are discrepancies between the various $paseq lists,",
    " and then we generally gave priority to the $paseq lists",
    " within the Leningrad Codex",
    " (at the end of the Torah, the Prophets, and the Writings);",
    " we considered both the items included and those absent from them,",
    " especially when their data agree",
    " with other determinations of the Masorah.",
    " But each case was judged on its own merits.",
]
FTNT_6_H = [
    "המסורה למקרא, פרק תשיעי 306 (עמ' 178).",
    " וראו גם את רשימת גינצבורג של כל לגרמיה במקרא,",
    ' על סמך הערות "לגרמיה" בשוליים בכתבי־היד.',
]
FTNT_6_E = [
    "Introduction to the Tiberian Masorah, ch. 9, 306 (p. 178).",
    " See also Ginsburg's list of all $legarmeh in the Bible,",
    " based on marginal $legarmeh annotations in manuscripts.",
]
FTNT_7_H = [
    'בכתי"ל יש עליו ציון מפורש "פ֗ס֗ק֗";',
    ' ובכתר ארם צובה יש בו הערת מסורה "ב֗"',
    " שמשווה אותו לַפָּסֵק הברור בביטוי הזהה בתהלים פה,ט",
    " (וגם שם אותה הערה).",
    ' לגבי רשימת הפסק בכתי"ל, שבה הפסוק הזה נעדר,',
    " ראו את רשימת הַפָּסֵק של ויקס עמ' 128 הערה 20;",
    ' רשימת הַפָּסֵק בכתי"ל לישעיהו משובשת היא,',
    " וברשימות אחרות הפסוק מופיע.",
]
FTNT_7_E_MAIN = [
    "In the Leningrad Codex there is an explicit $paseq annotation;",
    ' and in the Aleppo Codex there is a Masorah note "\u200fב\u200f"',
    " comparing it to the clear $paseq",
    " in the identical phrase in Psalms 85:9",
    " (where the same note also appears).",
    " Regarding the $paseq list in the Leningrad Codex,",
    " from which this verse is absent,",
    " see Wickes's $paseq list p. 128 note 20;",
    " the $paseq list in the Leningrad Codex for Isaiah is corrupt,",
    " and in other lists the verse does appear.",
]

FTNT_7_E = [
    ("p", FTNT_7_E_MAIN),
    ("img", "he_ws_intro_to_mam/LC Isa 42v5 paseq.png"),
]
FTNT_8_H = [
    "ראו את רשימת ויקס של לגרמיה הסמוך לרביע,",
    ' שהיא "רשימה מוסמכת למדי" לדעתו של ייבין,',
    " המסורה למקרא, 308 (עמ' 179).",
    " גם ברויאר ערך רשימה כזו,",
    " שבה הוא מקטלג את כל המקומות לפי סוגים",
    " (טעמי המקרא, ו.11 (עמ' 137\N{EN DASH}140).",
    " וגם רשימת גינצבורג של כל לגרמיה במקרא",
    " כוללת את הלגרמיה הסמוך לרביע.",
    " להלן רשימה של לגרמיה הסמוך לרביע,",
    " המבוססת בעיקר על רשימתו של ויקס:",
    " בראשית ג,טו; יז,יד; כג,ו; כט,ט2; מה,ה;",
    " שמות ל,יג;",
    " במדבר ז,יג2, יט2, וכו'; י,כט; י,לה2; כ,כא;",
    " דברים א,לג2; ה,ד; ה,כא2",
    " (אצל ויקס רשום בטעות כב2);",
    " לב,לט;",
    " יהושע ה,יד; ט,יב; טו,יח",
    " (ויקס השמיט את הפסוק הזה לאור הפסוק המקביל",
    " בשופטים א,יד אבל הקו נמצא בכתר ארם צובה);",
    " שופטים יא,מ; טז,ב; יח,ז2; כ,כח;",
    ' שמואל: שמ"א יא,ט; יא,יב2; טז,ה; טז,ז2; כ,כה; כו,טז2;',
    ' שמ"ב יב,כג; טו,כ; טו,ל;',
    ' מלכים: מל"א ו,כט; ז,כג2; יט,ד2;',
    ' מל"ב ב,יב; ה,כב; כה,טז;',
    " ישעיהו ט,טז; יט,טז2; כא,ח2; כב,ב; כב,יא; מט,כא2;",
    " ירמיהו נ,לד; נב,כ;",
    " יחזקאל כד,יז; לה,יב;",
    " זכריה א,ח; ו,טו; י,יב2;",
    " שיר השירים ד,יד; ח,יד;",
    " רות א,יג; ג,ג; ג,יג;",
    " קהלת ט,ג;",
    " דניאל ד,טו2;",
    " נחמיה ב,יב;",
    ' דברי הימים: דה"א ג,א2; יח,י; דה"ב ד,ב2; כא,יט.',
    " בשני מקומות ברשימתו של ויקס",
    ' אין קו של לגרמיה בכתבי־היד (כתי"א וכתי"ל),',
    " אבל יש לגרמיה בחלק מהדפוסים:",
    ' מל"ב יז,לו (ליסר, לטריס, בער, קורן);',
    " ירמיהו כ,ד (ליסר, לטריס).",
    " בנוסף השמיט ויקס מרשימתו את שלושת הפסוקים הבאים",
    " (ראו שם הערה 27):",
    " ישעיהו ז,כה (בער);",
    " דניאל יא,ו (כתבי־יד שונים);",
    ' דה"ב יח,ג (כתבי־יד שונים).',
]
_FTNT_8_E_INTRO = [
    "See Wickes's list of $legarmeh adjacent to $revia,",
    ' which is "a fairly authoritative list"',
    " according to Yeivin, Introduction to the Tiberian Masorah,",
    " 308 (p. 179).",
    " Breuer also compiled such a list,",
    " cataloging all occurrences by type",
    " (Ta'amei HaMiqra, 6.11, pp. 137\N{EN DASH}140).",
    " Ginsburg's list of all $legarmeh in the Bible",
    " also includes $legarmeh adjacent to $revia.",
    " Below is a list of $legarmeh adjacent to $revia,",
    " based mainly on Wickes's list:",
]
# fmt: off
_FTNT_8_E_LIST = [
    _bv("Genesis", ["3:15", "17:14", "23:6", "29:9b", "45:5"]),
    _bv("Exodus", ["30:13"]),
    _bv("Numbers", ["7:13b, 19b, etc.", "10:29", "10:35b", "20:21"]),
    _bv("Deuteronomy", [
        "1:33b", "5:4",
        "5:21b (Wickes erroneously wrote 22b)",
        "32:39",
    ]),
    _bv("Joshua", [
        "5:14", "9:12",
        ["15:18 (Wickes omitted this verse in light of the parallel verse",
         " in Judges 1:14, but the line is found in the Aleppo Codex)"],
    ]),
    _bv("Judges", ["11:40", "16:2", "18:7b", "20:28"]),
    _bv("1 Samuel", ["11:9", "11:12b", "16:5", "16:7b", "20:25", "26:16b"]),
    _bv("2 Samuel", ["12:23", "15:20", "15:30"]),
    _bv("1 Kings", ["6:29", "7:23b", "19:4b"]),
    _bv("2 Kings", ["2:12", "5:22", "25:16"]),
    _bv("Isaiah", ["9:16", "19:16b", "21:8b", "22:2", "22:11", "49:21b"]),
    _bv("Jeremiah", ["50:34", "52:20"]),
    _bv("Ezekiel", ["24:17", "35:12"]),
    _bv("Zechariah", ["1:8", "6:15", "10:12b"]),
    _bv("Song of Songs", ["4:14", "8:14"]),
    _bv("Ruth", ["1:13", "3:3", "3:13"]),
    _bv("Ecclesiastes", ["9:3"]),
    _bv("Daniel", ["4:15b"]),
    _bv("Nehemiah", ["2:12"]),
    _bv("1 Chronicles", ["3:1b", "18:10"]),
    _bv("2 Chronicles", ["4:2b", "21:19"]),
]
# fmt: on
_FTNT_8_E_NOTES = [
    "In two places in Wickes's list",
    " there is no $legarmeh line in the manuscripts",
    " (Aleppo and Leningrad),",
    " but $legarmeh appears in some printed editions:",
    " 2 Kgs. 17:36 (Letteris, Letteris, Baer, Koren);",
    " Jeremiah 20:4 (Letteris, Letteris).",
    " Additionally, Wickes omitted from his list the following three verses",
    " (see note 27 there):",
    " Isaiah 7:25 (Baer);",
    " Daniel 11:6 (various manuscripts);",
    " 2 Chr. 18:3 (various manuscripts).",
]
_FOI_PL = "https://bdenckla.github.io/MAM-with-doc/foi/foi-pasoleg-1.html"
_FOI_PL_0INT = (
    _FOI_PL + "#intro-%E2%85%83-leg...(rev)"
    "%C2%ABspace%C2%BBwith%C2%ABspace%C2%BB0%C2%ABspace%C2%BBintervening"
)
_FTNT_8_E_FOI = _ait(
    [
        "For a listing of this pattern in the $MAM data, see the ",
        author.dquote("features of interest"),
        " list for ",
        author.anc_h(
            "$legarmeh adjacent to $revia",
            _FOI_PL_0INT,
        ),
        ".",
    ]
)
FTNT_8_E = [
    ("p", _FTNT_8_E_INTRO),
    ("ul", _FTNT_8_E_LIST),
    ("p", _FTNT_8_E_NOTES),
    ("p", _FTNT_8_E_FOI),
]
FTNT_9_H = [
    "ראו ויקס, עמ' 118, המבוסס על הערות מסורה.",
]
FTNT_9_E = [
    "See Wickes, p. 118, based on Masorah annotations.",
]
FTNT_10_H = [
    "ראו ויקס, עמ' 120, המבוסס על הערות מסורה.",
]
FTNT_10_E = [
    "See Wickes, p. 120, based on Masorah annotations.",
]
FTNT_11_H = [
    "טעמי המקרא, ו.12 (עמ' 141).",
]
FTNT_11_E = [
    "Ta'amei HaMiqra, 6.12 (p. 141).",
]
FTNT_12_H = [
    "דותן קיבל את דעתו של ויקס בנושא הזה",
    " (עמ' 120 הערה 6).",
]
FTNT_12_E = [
    "Dotan accepted Wickes's view on this matter",
    " (p. 120 note 6).",
]
FTNT_13_H = [
    "ספר דקדוק הטעמים לר' אהרן בן משה בן אשר,",
    " חלק ב: הפירוש והניתוח, שער ט\"ז, עמ' 246.",
]
FTNT_13_E = [
    "Sefer Diqduk HaTe'amim by R. Aharon ben Moshe ben Asher,",
    " Part 2: Commentary and Analysis, Section 16, p. 246.",
]
FTNT_14_H = [
    "לשתי מהדורותיו של דותן ראו בביבליוגרפיה;",
    " וראו עוד ייבין, כז.2 (עמ' 231) על פסוק זה:",
    ' "ושמא הכוונה בדוגמה זו להטעמת מרכא',
    ' עם הלגרמיה בתיבתו."',
]
FTNT_14_E = [
    "For Dotan's two editions see the Bibliography;",
    " see also Yeivin, 27.2 (p. 231) on this verse:",
    ' "Perhaps the intention in this example is the $merkha accent',
    ' with the $legarmeh on its word."',
]
FTNT_15_H = [
    "טעמי המקרא, ו.12 (עמ' 141).",
]
FTNT_15_E = [
    "Ta'amei HaMiqra, 6.12 (p. 141).",
]
FTNT_16_H = [
    "טעמי המקרא, ד.20 (עמ' 119).",
    " וראו גם ייבין, המסורה למקרא, פרק תשיעי 307 (עמ' 179).",
]
FTNT_16_E = [
    "Ta'amei HaMiqra, 4.20 (p. 119).",
    " See also Yeivin, Introduction to the Tiberian Masorah,",
    " ch. 9, 307 (p. 179).",
]
FTNT_17_H = [
    'שם קובע ברויאר ש"יחידה פשוטה המסתיימת ברביע',
    " מתחלקת לעתים קרובותת על ידי לגרמיה",
    ' \N{EN DASH} אפילו שתי תיבותיה קצרות."',
]
FTNT_17_E = [
    'There Breuer states that "a simple unit ending in $revia',
    " is frequently divided by $legarmeh",
    ' \N{EN DASH} even when its two words are short."',
]
FTNT_18_H = [
    "בסוף סעיף ד.20 (עמ' 119) מציע ברויאר",
    ' שגם מנוסח הטעמים באמ"ת ניתן להוכיח',
    " שהטעם ביחידה פשוטה הוא לגרמיה ולא פסק.",
]
FTNT_18_E = [
    "At the end of section 4.20 (p. 119) Breuer suggests",
    " that even from the accent text of the poetic books",
    " one can prove that the accent in a simple unit",
    " is $legarmeh and not $paseq.",
]
FTNT_19_H = [
    "למידע טכני על התו של רווח מיוחד זה,",
    " ושל רווחים אחרים ביוניקוד,",
    " ראו ערך Space (punctuation) בוויקיפדיה.",
]
FTNT_19_E = [
    "For technical information on this special space character",
    " and other spaces in Unicode,",
    " see the Wikipedia article on Space (punctuation).",
]
FTNT_20_H = [
    'לסיכום של הכללים לשתי הצורות של לגרמיה בספרי אמ"ת',
    " ראו ייבין, המסורה למקרא, 333 (עמ' 197).",
]
FTNT_20_E = [
    "For a summary of the rules for the two forms",
    " of $legarmeh in the poetic books",
    " see Yeivin, Introduction to the Tiberian Masorah,",
    " 333 (p. 197).",
]
FTNT_21_H = [
    'על לגרמיה מהסוג הזה בספרי אמ"ת',
    " ראו ברויאר, טעמי המקרא, יד.2 (עמ' 321).",
]
FTNT_21_E = [
    "On this type of $legarmeh in the poetic books",
    " see Breuer, Ta'amei HaMiqra, 14.2 (p. 321).",
]
FTNT_22_H = [
    "למקורותיה של רשימת הלגרמיה של גינצבורג",
    " בספרי אמ\"ת ראו גינצבורג, המסורה, עמ' 438.",
]
FTNT_22_E = [
    "For the sources of Ginsburg's $legarmeh list",
    " in the poetic books see Ginsburg, The Massorah, p. 438.",
]
FTNT_23_H = [
    "למקורותיה של רשימת הפסק של גינצבורג",
    " בספרי אמ\"ת ראו גינצבורג, המסורה, עמ' 445.",
]
FTNT_23_E = [
    "For the sources of Ginsburg's $paseq list",
    " in the poetic books see Ginsburg, The Massorah, p. 445.",
]
FTNT_24_H = [
    "מהפך לגרמיה ואזלא לגרמיה נמצאים",
    " ברשימת הפסק במקומות הבאים:",
    " תהלים ט,יז; יח,נ",
    ' (כנראה שהכוונה לא הייתה ל"עַל־כֵּ֤ן ׀ אוֹדְךָ֖"',
    ' אלא ל"בַגּוֹיִ֥ם ׀ יְהֹוָ֑ה");',
    " לז,ז; נ,א;",
    " נה,כ (שְׁמַ֤ע ׀ אֵ֨ל ׀ וְֽיַעֲנֵם֮",
    " \N{EN DASH} השני נמצא ברשימת הלגרמיה);",
    " סח,לו; עב,יט; פד,ד; קי,ד; קיז,ב; קיח,כז;",
    " איוב ז,כ.",
]
_FTNT_24_E_INTRO = [
    "$Mahapakh $legarmeh and $azla $legarmeh",
    " are found in the $paseq list at the following places:",
]
# fmt: off
_FTNT_24_E_LIST = [
    _bv("Psalms", [
        "9:17",
        ["18:50 (probably the reference was not to ",
         author.hbo("עַל־כֵּ֤ן ׀ אוֹדְךָ֖"),
         " but to ", author.hbo("בַגּוֹיִ֥ם ׀ יְהֹוָ֑ה"), ")"],
        "37:7", "50:1",
        ["55:20 (", author.hbo("שְׁמַ֤ע ׀ אֵ֨ל ׀ וְֽיַעֲנֵם֮"),
         " \N{EN DASH} the second is found in the $legarmeh list)"],
        "68:36", "72:19", "84:4", "110:4", "117:2", "118:27",
    ]),
    _bv("Job", ["7:20"]),
]
# fmt: on
FTNT_24_E = [
    ("p", _FTNT_24_E_INTRO),
    ("ul", _FTNT_24_E_LIST),
]
FTNT_25_H = [
    'על הקו המאונך של תיבת "לַמְנַצֵּ֬חַ ׀"',
    " בטעם עילוי ראו ברויאר, טעמי המקרא, יד.3,",
    " סוף עמ' 321.",
    " קו מאונך של פסק בכתר",
    " שאינו מובא ברשימת הפסק של גינצבורג",
    " נמצא במקומות הבאים:",
    " תהלים לו,א; מד,א; מז,א; מט,א;",
    " נה,כד; סא,א; סט,א; פא,א; פה,א; צב,י.",
    " רק בשני מקומות חסר קו מאונך של פסק בכתר",
    " לעומת רשימתו של גינצבורג:",
    " תהלים פו,א; משלי ד,ז.",
]
FTNT_25_E = [
    "On the vertical line of the word לַמְנַצֵּ֬חַ ׀",
    " with the illuy accent see Breuer, Ta'amei HaMiqra, 14.3,",
    " end of p. 321.",
    " A $paseq vertical line in the Aleppo Codex",
    " that is not listed in Ginsburg's $paseq list",
    " is found at the following places:",
    " Psalms 36:1; 44:1; 47:1; 49:1;",
    " 55:24; 61:1; 69:1; 81:1; 85:1; 92:10.",
    " In only two places is a $paseq vertical line absent",
    " from the Aleppo Codex compared to Ginsburg's list:",
    " Psalms 86:1; Proverbs 4:7.",
]
FTNT_26_H = [
    "טעמי המקרא, א.26.ב (עמ' 18\N{EN DASH}19).",
    " במקום אחד רשם גינצבורג את הקו של שלשלת גדולה כפסק",
    " (תהלים פט,ג).",
]
FTNT_26_E = [
    "Ta'amei HaMiqra, 1.26.b (pp. 18\N{EN DASH}19).",
    " In one place Ginsburg listed the $shalshelet_gedolah line",
    " as $paseq (Psalms 89:3).",
]

FTNTS_H = [
    FTNT_0_H,
    FTNT_1_H,
    FTNT_2_H,
    FTNT_3_H,
    FTNT_4_H,
    FTNT_5_H,
    FTNT_6_H,
    FTNT_7_H,
    FTNT_8_H,
    FTNT_9_H,
    FTNT_10_H,
    FTNT_11_H,
    FTNT_12_H,
    FTNT_13_H,
    FTNT_14_H,
    FTNT_15_H,
    FTNT_16_H,
    FTNT_17_H,
    FTNT_18_H,
    FTNT_19_H,
    FTNT_20_H,
    FTNT_21_H,
    FTNT_22_H,
    FTNT_23_H,
    FTNT_24_H,
    FTNT_25_H,
    FTNT_26_H,
]
FTNTS_E = [
    FTNT_0_E,
    FTNT_1_E,
    FTNT_2_E,
    FTNT_3_E,
    FTNT_4_E,
    FTNT_5_E,
    FTNT_6_E,
    FTNT_7_E,
    FTNT_8_E,
    FTNT_9_E,
    FTNT_10_E,
    FTNT_11_E,
    FTNT_12_E,
    FTNT_13_E,
    FTNT_14_E,
    FTNT_15_E,
    FTNT_16_E,
    FTNT_17_E,
    FTNT_18_E,
    FTNT_19_E,
    FTNT_20_E,
    FTNT_21_E,
    FTNT_22_E,
    FTNT_23_E,
    FTNT_24_E,
    FTNT_25_E,
    FTNT_26_E,
]
