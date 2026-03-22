"""
Generates a bilingual (Hebrew/English) HTML document about gray maqaf.

The Hebrew text is adapted (with minor editorial changes) from Avi Kadish's
introduction to the Miqra al pi ha-Masora edition, Chapter 2, section
"טעם משני בתיבה הראויה להיות מוקפת". The source is on Hebrew Wikisource:
https://he.wikisource.org/wiki/ויקיטקסט:מבוא_למקרא_על_פי_המסורה/פרק_ב#טעם_משני_בתיבה_הראויה_להיות_מוקפת

A copy of the Wikisource markup is kept in he_ws_intro_to_mam_gray_maqaf.wikisource.txt.

The English translation is original to this project.
"""

from pycmn.my_utils import sl_map
from py_misc import my_html
from pycmn import my_utils
from pycmn import hebrew_punctuation as hpu
from pyauthor_util import author
from pyauthor import he_ws_intro_to_mam_gray_maqaf_footnotes as gmfn


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch, body_class=None):
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, _CBODY, body_class)


# Footnotes are numbered as B+N (N=0,1,...,6). B is the number of the
# first footnote in this document within the larger Kadish introduction.
# Current value: B = 136.
_FN_BASE = 136


def _footnote_marker(n: int, side="h"):
    """Footnote marker for body text, linking to the footnote entry.

    side="h": Hebrew side — carries the anchor id (for the back-link target).
    side="e": English side — link only (no id, to avoid duplicate ids).
    """
    text = f"[B+{n}]"
    if side == "h":
        return my_html.anchor(text, {"id": f"fnref-{n}", "href": f"#fn-{n}"})
    return my_html.anchor_h(text, f"#fn-{n}")


def _ait(contents):
    """Added In Translation, i.e. not in original, i.e. square-bracketed (and gray)"""
    return author.span_gray(["[", contents, "]"])


def _gray_maqaf(string: str):
    split_result = string.split(hpu.MAQ)
    gm = author.span_gray(hpu.MAQ)
    return my_utils.intersperse(gm, split_result)


def _hbo_gray(string: str):
    return author.hbo(_gray_maqaf(string))


_Y_010_H = "טעם משני בתיבה הראויה להיות מוקפת"
_Y_010_E = "A secondary accent in a word that should have a $maqaf"
_Y_011_H = [
    "בתיבות רבות בספרי אמ״ת חסר טעם מובהק.",
    " יש בהן סימן כלשהו של טעם, אך מדובר על סימן שלא בא לציין את ההברה המוטעמת.",
    " לעתים הוא אף נכתב בהברה שאינה יכולה מוטעמת לפי כל הכללים של המסורה והדקדוק.",
    " כל התיבות הללו ראויות להיות מוקפות, ולעתים הן אף מנוקדות כאילו היה בהן מקף.",
    " ולפעמים אנחנו מוצאים שנכתב מקף אחרי תיבות אחדות מהסוג הזה בכתבי־היד.",
    " אבל ברוב המכריע של המקומות אין מקף, למרות שהתיבה ראויה להיות מוקפת.",
]
_Y_011_E = [
    ["Many words in the poetic books lack a primary accent."],
    [" They have an accent,"],
    [" but it is not meant to indicate the stressed syllable."],
    [" Sometimes it is even written on a syllable that cannot be stressed"],
    [" according to all the rules of the Masorah and grammar."],
    [" All of these words should have a $maqaf,"],
    [" and sometimes they are even vowel-pointed as if they had a $maqaf."],
    [" And sometimes we find that"],
    [" a $maqaf is written after some of these words in the manuscripts."],
    [" But in the vast majority of cases, there is no $maqaf,"],
    [" even though the word should have a $maqaf."],
]
_Y_012_H = [
    "מציאות זו מקשה על כל מי שקורא בספרי אמ״ת ורוצה לבטא את הפסוקים כתיקונם.",
    " לכן הוספנו מקף אפור אחרי תיבות מהסוג הזה במהדורתנו.",
]
_Y_012_E = [
    ["This situation makes it difficult for"],
    [" anyone who reads the poetic books and wants to pronounce the verses correctly."],
    [" Therefore, we added a gray $maqaf after words of this type in our edition."],
]
_Y_013_H = "להלן הסבר מפורט של התופעה ושל הביצוע."
_Y_013_E = "Below is a detailed explanation of the phenomenon and its implementation."
_Y_020_H = "א. תיבה הראויה להיות מוקפת: הסבר התופעה"
_Y_020_E = "א. A word that should have a $maqaf: Explanation of the phenomenon"
_K_KAT_H = "כתר ארם צובה: ניקודו וטעמיו"
_Y_021_H = [
    ["הרב מרדכי ברויאר דן באריכות באחד מהממצאים של ישראל ייבין"],
    [" בספרו המונומנטלי ", author.book_title(_K_KAT_H), "."],
    [
        _footnote_marker(0),
        " ייבין הצליח, על־ידי תיאור מדוקדק של הנתונים בכתר ארם צובה,",
    ],
    [" להבחין היטב בין שני סימנים קרובים: קו של געיה וקו של מרכא."],
    [" וכך עלה בידו גם לקבוע את נוכחותה המלאה של המרכא בין הטעמים המשרתים האחרים."],
    [
        _footnote_marker(1),
        " בנוסף, ברויאר טען שעל־פי ממצאיו של ייבין ניתן לגלות",
    ],
    [
        " גילוי נוסף על עצם טיבו של טעם המרכא בספרי אמ״ת:",
        _footnote_marker(2),
    ],
]
_Y_KAT_E = "The Aleppo Codex of the Bible: a study of its vocalization and accentuation"
_Y_021_E = [
    ["Rabbi Mordechai Breuer discusses in detail"],
    [" one of the findings of Israel Yeivin."],
    [" (", _ait("Yeivin presented this finding"), " in his monumental work,"],
    [" ", author.book_title(_Y_KAT_E), ".", _footnote_marker(0, "e"), ")"],
    [" Yeivin was able,"],
    [" through a meticulous description of the data in the Aleppo Codex,"],
    [" to clearly distinguish between two similar marks:"],
    [" a $gaya line and a $merkha line."],
    [" Thus, Yeivin was also able to establish"],
    [" the full presence of the $merkha among the other conjunctive"],
    [" accents.", _footnote_marker(1, "e")],
    [" In addition, Breuer argued that based on Yeivin’s findings,"],
    [" another discovery can be made about"],
    [" the nature of $merkha in the poetic books:", _footnote_marker(2, "e")],
]
_Y_03_H = [
    ["...יש להבדיל, לדוגמה,"],
    [" בין המשרתים השונים,"],
    [" המצויים בתיבת לגרמיה של אמ״ת."],
    [" אתה מוצא שם מהפך ועילוי וגם מרכא."],
    [" אך לא הרי אלו כהרי זה:"],
    [" מהפך ועילוי מצויים רק בהברה האחרונה הראויה לגעיה קלה;"],
    [" והם שכיחים מאוד גם כמשרתים עיקריים בתיבתם;"],
    [
        " והשוה: וְלָ֤רָשָׁ֨ע׀ – נָשְׂא֤וּ נְהָר֨וֹת׀; וַהֲדָ֬רְךָ֨׀ – תְּחַדֵּ֬שׁ עֵדֶ֨יךָ׀."
    ],
    [" כנגד זה מרכא מצויה גם בהברה שאינה ראויה לשום געיה:"],
    [" תַּ֥הְפֻּכ֨וֹת׀; ולעולם אין היא מצויה כטעם עיקרי בתיבתה."],
]
_Y_030_E_1A = [
    ["... One has to distinguish, for example,"],
    [" between the different conjunctive accents"],
    [" found in $legarmeh words in the poetic books."],
    [" You will find there $mahapakh, $iluy, and also $merkha."],
    [" But these ", _ait("three"), " are not all the same."],
    [" $Mahapakh and $iluy ", _ait("have the following features"), ":"],
]
_Y_030_E_1B = [
    [_ait("In $legarmeh words, they"), " are found only on"],
    [" the last syllable that is suitable for a light $gaya ", _ait("($LSSLG)"), "."],
]
_Y_030_E_1C = [
    [_ait("Before $legarmeh words,")],
    [" they are very common as the primary accents of their words."],
]
_Y_030_E_1D = _ait("For example:")
_Y_030_E_2 = [author.hbo("וְלָ֤רָשָׁ֨ע׀"), " – ", author.hbo("נָשְׂא֤וּ נְהָר֨וֹת׀")]
_Y_030_E_3 = [author.hbo("וַהֲדָ֬רְךָ֨׀"), " – ", author.hbo("תְּחַדֵּ֬שׁ עֵדֶ֨יךָ׀")]
_Y_030_E_4A = [
    ["In contrast, $merkha ", _ait("has the following features"), ":"],
]
_Y_030_E_4B = [
    [_ait("In $legarmeh words, it"), " can be found"],
    [" ", _ait("not only on the $LSSLG, but")],
    [" also on a syllable that is not suitable for any $gaya, ", _ait("e.g."), ":"],
    [" ", author.hbo("תַּ֥הְפֻּכ֨וֹת׀"), "."],
]
_Y_030_E_4C = [
    [_ait("Before $legarmeh words,")],
    [" it is never found as the primary accent of its word."],
]
_Y_03_E = [
    author.para(_Y_030_E_1A),
    author.unordered_list([_Y_030_E_1B, _Y_030_E_1C]),
    author.para(_Y_030_E_1D),
    author.para_dr_cc(_Y_030_E_2),
    author.para_dr_cc(_Y_030_E_3),
    author.para(_Y_030_E_4A),
    author.unordered_list([_Y_030_E_4B, _Y_030_E_4C]),
]
_Y_040_H = [
    ["שתי תכונות אלה הופכות את המרכות הללו למשרתים מסוג מיוחד."],
    [" ספק, אם אפשר לקרוא להן משרתים כלל."],
    [" מכל מקום, אין כוחן ככוח שאר המשרתים."],
]
_Y_041_H = "והדבר ניכר בשתיים:"
_Y_040_E = [
    ["These two features make these $merkha marks special conjunctive accents."],
    [" It is doubtful whether they can be called conjunctive accents at all."],
    [" In any case, they are weaker than the other conjunctive accents."],
]
_Y_041_E_1 = "This is evident in two ways: "
_Y_041_E = [
    "(1) the use of $merkha where there is a $maqaf",
    " and",
    " (2) the use of $merkha where there should be a $maqaf.",
    " These two ways are elaborated upon below.",
]
_Y_041_E = [_Y_041_E_1, _ait(_Y_041_E)]
_Y_04_H = author.emphasis(_Y_040_H), " ", _Y_041_H
_Y_04_E = author.para([author.emphasis(_Y_040_E), " ", _Y_041_E])
_Y_05_H = [
    ["א) בדרך כלל משרת ומקף מוציאים זה את זה;"],
    [" ואם תיבה מוקפת ראויה גם למשרת, מיד היא חדלה להיות מוקפת;"],
    [" כגון: וַיַּ֣עֲשׂוּ כֵ֔ן – במקום: וַיַּ֣עֲשׂוּ־כֵ֔ן."],
    [" כנגד זה מרכא מצויה גם בתיבה מוקפת:"],
    [
        " וּ֥תְהִי־ע֨וֹד׀ (איוב ו, י), מַ֥עֲדֶה־בֶּ֨גֶד׀ (משלי כה, כ).",
        _footnote_marker(3),
    ],
]
_Y_050_E = [
    ["(1) Generally, a conjunctive accent and a $maqaf are mutually exclusive;"],
    [" so, ", _ait("for example,")],
    [" if a word ", _ait("part"), " with a $maqaf needed a conjunctive accent,"],
    [" the $maqaf would have to be removed."],
    [" For example:"],
]
_Y_051_E = "וַיַּ֣עֲשׂוּ כֵ֔ן"
_Y_052_E = [
    [_ait("would be the result of adding a $munax to ויעשו־כן")],
    [" instead of"],
    [" ", _ait("the result being simply as follows:")],
]
_Y_053_E = "וַיַּ֣עֲשׂוּ־כֵ֔ן"
_Y_054_E = [
    ["In contrast, $merkha can be found"],
    [" on a word ", _ait("part"), " with $maqaf:"],
]
_Y_055_E = [author.hbo("וּ֥תְהִי־ע֨וֹד׀"), " ", "(איוב ו, י)"]
_Y_056_E = [author.hbo("מַ֥עֲדֶה־בֶּ֨גֶד׀"), " ", "(משלי כה, כ)"]
_Y_057_E = _footnote_marker(3, "e")
_Y_05_E = [
    author.para(_Y_050_E),
    author.para_hbo_es(_Y_051_E),
    author.para(_Y_052_E),
    author.para_hbo_es(_Y_053_E),
    author.para(_Y_054_E),
    author.para_dr_cc(_Y_055_E),
    author.para_dr_cc(_Y_056_E),
    author.para(_Y_057_E),
]
_Y_06_H_EMPH = [
    "אולם ביטול זה של המקף אינו אלא למראית עין:",
    ' התיבה "נמלטה מן ההקפה" – ועדיין דינה כדין תיבה מוקפת.',
]
_Y_06_H = [
    "ב) לפעמים גם מרכא מבטלת את המקף שלאחריה;",
    " כך תמיד בתיבה זעירה: פֶּ֥ן אֶשְׂבַּ֨ע׀ (מש' ל, ט), אִ֥ם חֲרוּצִ֨ים׀ (איוב יד, ה);",
    " וכך תמיד בתיבת הַ֥לְלוּ יָ֨הּ׀. ",
    author.emphasis(_Y_06_H_EMPH),
    ' משום כך תיבות "את",',
    ' "כל",',
    " מנוקדות כגון תיבות מוקפות;",
    " אֶ֥ת גְּא֨וֹן (תה' מז, ה),",
    _footnote_marker(4),
    " כׇּ֥ל עַצְמוֹתַ֨י׀ (שם לה, י).",
]
_Y_060_E = [
    "(2) Sometimes $merkha also cancels out the $maqaf that follows it;",
    " this always occurs in the short word:",
]
_Y_061_E = [author.hbo("פֶּ֥ן אֶשְׂבַּ֨ע׀"), " (מש' ל, ט)"]
_Y_062_E = [author.hbo("אִ֥ם חֲרוּצִ֨ים׀"), " (איוב יד, ה)"]
_Y_063_E = "and this always occurs in the word"
_Y_064_E = author.hbo("הַ֥לְלוּ יָ֨הּ׀")
_Y_065_E_EMPH = [
    "However, this cancellation of the $maqaf is only apparent:",
    " the word “escaped the joining” – and still has the status of a joined word.",
]
_Y_065_E = [
    author.emphasis(_Y_065_E_EMPH),
    " Therefore, the words את and כל are vowel-pointed like joined words;",
    " for example:",
]
_Y_066_E = [
    author.hbo("אֶ֥ת גְּא֨וֹן"),
    " (תה' מז, ה),",
    _footnote_marker(4, "e"),
]
_Y_067_E = [author.hbo("כׇּ֥ל עַצְמוֹתַ֨י׀"), " (שם לה, י)."]
_Y_06_E = [
    author.para(_Y_060_E),
    author.para_dr_cc(_Y_061_E),
    author.para_dr_cc(_Y_062_E),
    author.para(_Y_063_E),
    author.para_dr_cc(_Y_064_E),
    author.para(_Y_065_E),
    author.para_dr_cc(_Y_066_E),
    author.para_dr_cc(_Y_067_E),
]
_Y_07_H = [
    'ניקוד זה של תיבות "את", "כל" היה תמיד חידה למדקדקים.',
    " המסורת הספרדית,",
    ' הקוראת "כל" זה כקמץ רחב רק מעידה על הערבוביה שבאה בעקבותיו.',
    " דומה, שגילויו של ייבין נותן פתרון נאה:",
    " המרכא שבתיבות אלה היא מרכא משנית –",
    " שאינה יכולה לשמש כטעם עיקרי בתיבתה.",
    " הרי היא דומה לשאר מרכות מסוג זה,",
    " שכולן מצויות רק כטעמים משניים. ",
    author.emphasis(
        [
            "משום כך עדיין תיבות אלה נחשבות כמוקפות –",
            " ומנוקדות בהתאם לכך.",
        ]
    ),
    _footnote_marker(5),
]
_Y_07_E = [
    ["This vowel-pointing of the words את and כל"],
    [" has always been a puzzle for grammarians."],
    [" The Sephardic tradition,"],
    [" which pronounces ", _ait("the vowel of"), " this כל as a $qg,"],
    [" only testifies to the confusion that ensued because of it."],
    [" It seems that Yeivin’s discovery provides a nice solution:"],
    [" the $merkha in these words is a secondary $merkha –"],
    [" which cannot serve as a primary accent in its word."],
    [" Thus, it is similar to the other cases of $merkha of this type,"],
    [" all of which are found only as secondary accents. "],
    author.emphasis(
        [
            "Therefore, these words are still considered joined –",
            " and are pointed accordingly.",
        ]
    ),
    _footnote_marker(5, "e"),
]
_Y_080_H = [
    "ברויאר חזר לדון בנושא של טעמים משניים בהרחבה ובאופן מסודר בספרו טעמי המקרא.",
    ' בפרק ט על "סדר פיסוק הטעמים" בספרי אמ"ת,',
    " הוא הקדיש חטיבה שלמה לתיבות הרבות שיש בהן יותר מטעם אחד:",
    " משרת בתיבתו של מפסיק (ט.20, עמ' 225),",
    " ושני משרתים הבאים זה אחר זה בתיבה אחת (ט.21 , עמ' 225-226).",
    " ואז, כהמשך לדיון בשני טעמים בתוך תיבה אחת,",
    " הוא בחן באריכות את התיבות שיש בהן טעם משני,",
    " והן ראויות להיות מוקפות לתיבה שלאחריהן בנסיבות רבות ושונות,",
    " כאילו היו תיבה אחת.",
    " לעתים תיבות מהסוג הזה מוקפות בפועל בכתבי־היד (ט.22-28, עמ' 226-237).",
    _footnote_marker(6),
]
_Y_080_E = [
    "Breuer returned to discuss the topic of secondary accents",
    " at length and in an orderly manner in his book Ta'amei HaMikra.",
    ' In Chapter 9 on "The Order of Accentuation Punctuation" in the poetic books,',
    " he devoted an entire section to the many words that have more than one accent:",
    " a conjunctive accent in a disjunctively accented word (p. 225),",
    " and two conjunctive accents that come one after the other in a single word (p. 225-226).",
    " Then, as a continuation of the discussion on two accents within a single word,",
    " he examined at length the words that have a secondary accent,",
    " and which should be joined to the next word under many and various circumstances,",
    " as if they were a single word.",
    " Sometimes, words of this type are indeed joined in the manuscripts (pp. 226-237).",
    _footnote_marker(6, "e"),
]
_Y_081_H = [
    'התופעה די דומה לשתי תיבות של "עולה" ו"יורד":',
    " כבר דנו בכך לעיל,",
    ' וראינו שתיבת ה"עולה" מנוקדת לעתים כאילו הייתה מוקפת,',
    " ולעתים היא אף מוקפת בפועל בכתבי־היד.",
    " ואילו בשאר המקרים השמיטו כתבי־היד את המקף כדבר המובן מאליו.",
    ' לכן במהדורתנו הוספנו מקף בצבע אפור בין שתי תיבות של "עולה" ו"יורד",',
    " כדי שהקורא ידע לקרוא את אותן כתיבות מוקפות.",
]
_Y_081_E = [
    "The phenomenon is quite similar to the two words עולה and יורד:",
    " we have already discussed this above,",
    " and we have seen that the word עולה is sometimes vowel-pointed as if it were joined,",
    " and sometimes it is indeed joined in the manuscripts.",
    " In the other cases, however, the manuscripts omit the $maqaf as a matter of course.",
    " Therefore, in our edition, we added a gray $maqaf between the two words עולה and יורד,",
    " so that the reader would know to read those words as joined.",
]
####################################
_WS_BASE = "https://he.wikisource.org/wiki/" "ויקיטקסט:מבוא_למקרא_על_פי_המסורה/פרק_ב"
_WS_URL = f"{_WS_BASE}#טעם_משני_בתיבה_הראויה_להיות_מוקפת"
_WS_LINK = my_html.anchor_h("Hebrew Wikisource", _WS_URL)
####################################
_X_01_I = ("Section title and introduction",)
_X_01_H = sl_map(author.para_modhe, [_Y_010_H, _Y_011_H, _Y_012_H, _Y_013_H])
_X_01_E = sl_map(author.para, [_Y_010_E, _Y_011_E, _Y_012_E, _Y_013_E])
_X_01_TRIPLE = _X_01_I, _X_01_H, _X_01_E
#
_X_02_I = "Subsection א title and introduction"
_X_02_H = sl_map(author.para_modhe, [_Y_020_H, _Y_021_H])
_X_02_E = sl_map(author.para, [_Y_020_E, _Y_021_E])
_X_02_TRIPLE = _X_02_I, _X_02_H, _X_02_E
#
_X_03_I = "Breuer blockquote part 1 of 5"
_X_03_H = author.para_modhe(_Y_03_H)
_X_03_E = _Y_03_E
_X_03_TRIPLE = _X_03_I, _X_03_H, _X_03_E
#
_X_04_I = "Breuer blockquote part 2 of 5"
_X_04_H = author.para_modhe(_Y_04_H)
_X_04_E = _Y_04_E
_X_04_TRIPLE = _X_04_I, _X_04_H, _X_04_E
#
_X_05_I = "Breuer blockquote part 3 of 5"
_X_05_H = author.para_modhe(_Y_05_H)
_X_05_E = _Y_05_E
_X_05_TRIPLE = _X_05_I, _X_05_H, _X_05_E
#
_X_06_I = "Breuer blockquote part 4 of 5"
_X_06_H = author.para_modhe(_Y_06_H)
_X_06_E = _Y_06_E
_X_06_TRIPLE = _X_06_I, _X_06_H, _X_06_E
#
_X_07_I = "Breuer blockquote part 5 of 5"
_X_07_H = author.para_modhe(_Y_07_H)
_X_07_E = author.para(_Y_07_E)
_X_07_TRIPLE = _X_07_I, _X_07_H, _X_07_E
#
_X_08_I = "Resume Subsection א after Breuer blockquote"
_X_08_H = sl_map(author.para_modhe, [_Y_080_H, _Y_081_H])
_X_08_E = sl_map(author.para, [_Y_080_E, _Y_081_E])
_X_08_TRIPLE = _X_08_I, _X_08_H, _X_08_E
#
_TITLE = "Gray maqaf"
_H1_CONTENTS = "Gray $maqaf"
_FNAME = "he_ws_intro_to_mam_gray_maqaf.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")
_PROVENANCE = author.para(
    [
        "The Hebrew text below is from Avi Kadish's introduction to the",
        " Miqra al pi ha-Masora edition (Chapter 2) on ",
        _WS_LINK,
        ". The English translation is original to this project.",
    ]
)


def _ftnt_triple(n, ftnt_h, ftnt_e):
    text = f"[B+{n}]"
    marker_h = my_html.anchor(text, {"id": f"fn-{n}", "href": f"#fnref-{n}"})
    marker_e = my_html.anchor_h(text, f"#fnref-{n}")
    return (
        f"Footnote B+{n}",
        author.para_modhe([marker_h, " ", *ftnt_h]),
        author.para([marker_e, " ", *ftnt_e]),
    )


_FTNT_TRIPLES = [
    _ftnt_triple(n, h, e) for n, (h, e) in enumerate(zip(gmfn.FTNTS_H, gmfn.FTNTS_E))
]
_CBODY = [
    author.heading_level_1(_H1_CONTENTS),
    _PROVENANCE,
    author.he_en_table_wct(
        [
            _X_01_TRIPLE,
            _X_02_TRIPLE,
            _X_03_TRIPLE,
            _X_04_TRIPLE,
            _X_05_TRIPLE,
            _X_06_TRIPLE,
            _X_07_TRIPLE,
            _X_08_TRIPLE,
        ]
    ),
    author.heading_level_2(f"Footnotes (B={_FN_BASE})"),
    author.he_en_table_wct(_FTNT_TRIPLES),
]

# file:///C:/Users/BenDe/GitRepos/MAM-with-doc/docs/misc/he_ws_intro_to_mam_gray_maqaf.html
