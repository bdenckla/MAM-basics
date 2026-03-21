"""
Generates a bilingual (Hebrew/English) HTML document about paseq and legarmeh.

The Hebrew text is adapted (with minor editorial changes) from Avi Kadish's
introduction to the Miqra al pi ha-Masora edition, Chapter 2, section
"פסק ולגרמיה". The source is on Hebrew Wikisource:
https://he.wikisource.org/wiki/ויקיטקסט:מבוא_למקרא_על_פי_המסורה/פרק_ב#פסק_ולגרמיה

The English translation is original to this project.
"""

from py_misc import my_html
from pyauthor_util import author


def _ait(contents):
    """Added In Translation, i.e. not in original, i.e. square-bracketed (and gray)"""
    return author.span_gray(["[", contents, "]"])


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch, body_class=None):
    author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, _CBODY, body_class)


# Section heading
_Y_SEC_H = "פסק ולגרמיה"
_Y_SEC_E = "$Paseq and $legarmeh"

# ═══════════════════════════════════════════════════════════════════
# Sub-section א: Definition of paseq and legarmeh
# ═══════════════════════════════════════════════════════════════════

_Y_A01_H = [
    author.emphasis("א. פסק ולגרמיה:"),
    " קו מאונך בסוף תיבה בא כדי להפריד אותה קצת מהתיבה שלאחריה.",
    " אם בתיבה הראשונה יש טעם מחבר,",
    " אז הקו בא כדי להורות לקורא",
    " שיש להפסיק במעט בין שתי התיבות",
    " ",
    author.emphasis("למרות"),
    " הטעם המחבר ביניהן.",
    ' במקומות האלה הקו האנכי נקרא "פָּסֵק".',
    " קו של פָּסֵק אינו חלק מהמערכת המוזיקלית של הטעמים אלא תוספת לה.",
]
_INSERT = [
    "can have one of two meanings.",
    " Each meaning calls for its own type of slight audible separation",
    " between the words that the line visually separates",
]
_Y_A01_E = [
    author.emphasis("א. $Paseq and $legarmeh:"),
    " A vertical line at the end of a word",
    [" ", _ait(_INSERT), "."],
    " If the first word has a conjunctive accent,",
    " then the line indicates to the reader",
    " that there should be a slight pause between the two words",
    [" ", author.emphasis("despite")],
    " the conjunctive accent joining them.",
    [" In these places, the vertical line is called ", author.dquote("$paseq.")],
    " A $paseq line is not part of the musical accentuation system",
    " but rather an addition to it.",
]

_Y_A02_H = [
    'אבל אם הקו בא לאחר הטעם "מונח" בכ״א הספרים,',
    ' אז במקומות רבים הוא הופך אותו ל"מֻנָּח לְגַרְמֵיהּ",',
    " כלומר: מונח שהוא טעם מפסיק",
    " (למרות שֶׁמֻּנָּח הוא בדרך כלל טעם מחבר).",
    " בשונה מִפָּסֵק,",
    " במונח לגרמיה הקו המאונך אינו מורה שיש להפסיק מעט",
    " ",
    author.emphasis("למרות"),
    " הטעם המחבר.",
    " אלא הוא מורה ש",
    author.emphasis("הטעם עצמו הוא טעם מפסיק"),
    ".",
    " מונח לגרמיה הוא חלק מובהק מהמערכת המוזיקלית של הטעמים:",
    " יש לו נגינה וטעמים משרתים משלו.",
]
_Y_A02_E = [
    "But if the line comes after a $munax in the 21 books,",
    " then in most places it transforms that $munax",
    [" into a ", author.dquote("$munleg,")],
    " meaning: a $munax that is a disjunctive accent",
    " (even though $munax is usually a conjunctive accent).",
    " Unlike $paseq,",
    " in $munleg the vertical line does not indicate",
    " a slight pause despite",
    " the conjunctive accent.",
    " Rather, it indicates that",
    [
        " ",
        author.emphasis("the accent itself is disjunctive"),
        ".",
    ],
    " $Munax $legarmeh is a distinct part",
    " of the musical accentuation system:",
    " it has its own melody and its own conjunctive accents.",
]

_Y_A03_H = [
    "יוצא שבכל מקום שבו יש קו מאונך לאחר תיבה,",
    " הקורא חייב לדעת תוך כדי קריאתו אם מדובר על פסק או על לגרמיה.",
    " במיוחד אם הקו המאונך בא לאחר תיבה המוטעמת במונח,",
    " לא תמיד ברור מאליו אם מדובר על מונח לגרמיה",
    " או על מונח רגיל (=טעם מחבר) שלאחריו פסק.",
    " אמנם ברוב המכריע של המקומות מדובר על מונח לגרמיה,",
    " כי אם המונח והקו באים לפני עוד מונח ואחר כך בא טעם הרביע",
    " – וכך הוא ברוב הפסוקים שיש בהם מונח וקו –",
    " אז המונח הראשון עם הקו הוא תמיד מונח לגרמיה.",
    " אבל אפילו במקרים נפוצים וברורים כאלה",
    " רצוי לתת יד לקורא ולציין לו במפורש שמדובר על לגרמיה,",
    " ועל אחת כמה וכמה במקרים אחרים שאינם ברורים מאליהם.",
    " מהסיבה הזאת כתבו חכמי המסורה הראשונים והאחרונים",
    ' כללים ורשימות של "לגרמיה" לסוגיו',
    " (בתוך חיבורי המסורה ובהערות המסורה),",
    ' רשימות מלאות של "פסק" בכל ספרי המקרא',
    " (בתוך קונטרסי המסורה),",
    ' ובחלק מכתבי־היד אף ציינו "לג[רמיה]" ו"פס[ק]"',
    " בשוליים של הטקסט",
    " (הציונים משולבים בתוך ההערות של המסורה הקטנה).",
]
_Y_A03_E = [
    "It follows that wherever there is a vertical line after a word,",
    [" the reader must determine ", _ait("...")],
    " whether it is $paseq or $legarmeh.",
    " Especially when the vertical line comes after",
    " a word accented with $munax,",
    " it is not always obvious whether it is $munleg",
    " or a regular $munax (= conjunctive accent) followed by $paseq.",
    " Indeed, in the vast majority of cases it is $munleg,",
    " because when the $munax and the line come before",
    " another $munax and then a $revia follows",
    " — as is the case in most verses with a $munax and a line —",
    " then the first $munax with the line",
    " is always $munleg.",
    " But even in such common and clear cases,",
    " it is desirable to assist the reader",
    " and indicate explicitly that it is $legarmeh,",
    " and all the more so in other cases that are not self-evident.",
]
_Y_A03b_E = [
    "For this reason, early and later Masorah scholars wrote",
    " rules and lists of $legarmeh",
    " of its various types",
    " (within Masorah treatises and Masorah notes),",
    " complete lists of $paseq",
    " for all the books of the Bible",
    " (within Masorah compendiums),",
    " and in some manuscripts they even noted",
    [" ", author.dquote("לג[רמיה]"), " and ", author.dquote("פס[ק]")],
    " in the margins of the text",
    " (the annotations are integrated within the Masorah Parva notes).",
]

# ═══════════════════════════════════════════════════════════════════
# Sub-section ב: Textual basis
# ═══════════════════════════════════════════════════════════════════

_Y_B01_H = [
    author.emphasis(
        "ב. את נוסח הקווים של לגרמיה ופסק"
        " (כלומר מתי יש ומתי אין קו מאונך)"
        " קבענו במהדורתנו לפי כתר ארם צובה,"
        " ובמקומות שהכתר לא קיים קבענו אותו לפי כתי״ל."
    ),
    " הנוסח זהה בדרך כלל בשני כתבי־היד.",
]
_Y_B01_E_EMPH = [
    [
        "ב. ",
        _ait("Regardless of the distinction between them, the presence or absence in"),
    ],
    " the text of the $legarmeh/$paseq lines",
    " (i.e. when there is and when there is no vertical line)",
    " was established in our edition according to the Aleppo Codex,",
    " and where the Aleppo Codex is not extant,",
    " we established it according to the Leningrad Codex.",
]
_LITTLE_DIFF = (
    "I.e., it would have made little difference if we had used Leningrad throughout."
)
_Y_B01_E = [
    author.emphasis(_Y_B01_E_EMPH),
    [" ", _ait("With respect to these lines,")],
    " the text is generally identical in both manuscripts.",
    [" ", _ait(_LITTLE_DIFF)],
]

# ═══════════════════════════════════════════════════════════════════
# Sub-section ג: Distinction between legarmeh and paseq
# ═══════════════════════════════════════════════════════════════════

_Y_C01_H = [
    author.emphasis(
        'ג. את ההבחנה בין "לגרמיה" ל"פסק" בכ״א הספרים קבענו לפי ספרות המסורה.'
    ),
    " להלן הכללים העיקריים העולים מתוך ספרות המסורה,",
    ' כדי להבחין בין "לגרמיה" ל"פסק":',
]
_Y_C01_E = [
    author.emphasis(
        [
            "ג. The distinction between $legarmeh and $paseq",
            " in the 21 books was established according to Masorah literature.",
        ]
    ),
    " Below are the main rules derived from Masorah literature",
    " for distinguishing between $legarmeh",
    " and $paseq:",
]

# Rule 1

_Y_C10_H = [
    author.emphasis('"מונח לגרמיה" בא בדרך כלל לפני מונח ורביע.'),
    " כך סיכם ייבין:",
    ' "לגרמיה משמש בעיקר כמפסיק פחוּת בתחום רביע,',
    " ועל פי רוב בינו ובין הרביע המשרת מונח,",
    " כגון: וְהִנֵּ֣ה ׀ שֶׁ֣בַע שִׁבֳּלִ֗ים (בר' מא, ה),",
    " מִכֹּ֣ל ׀ הַבְּהֵמָ֣ה הַטְּהוֹרָ֗ה (בר' ז, ב).",
    " עתים מפרידים ביניהם שני משרתי הרביע,",
    " כגון: אֶ֣מֶשׁ ׀ אָמַ֧ר אֵלַ֣י לֵאמֹ֗ר (בר' לא, כט)...",
    " הלגרמיה עשוי להתרדף,",
    " כגון: וַיִּ֜מַח אֶֽת־כׇּל־הַיְק֣וּם ׀ אֲשֶׁ֣ר ׀ עַל־פְּנֵ֣י הָֽאֲדָמָ֗ה",
    " (בר' ז, כג).\"",
]
_Y_C10_E = [
    author.emphasis("$Munax $legarmeh usually comes before $munax and $revia."),
    " As Yeivin summarized:",
]
_SEP_DARGA = "here they are separated not only by the usual $munax but also by a $darga before it"
_Y_C11_E = [
    "$Legarmeh serves mainly as a minor disjunctive in the domain of $revia,",
    " and usually between it and the $revia there is a conjunctive $munax, e.g.:",
    my_html.line_break(),
    author.hbo("וְהִנֵּ֣ה ׀ שֶׁ֣בַע שִׁבֳּלִ֗ים"),
    my_html.line_break(),
    "(Gen. 41:5),",
    my_html.line_break(),
    author.hbo("מִכֹּ֣ל ׀ הַבְּהֵמָ֣ה הַטְּהוֹרָ֗ה"),
    my_html.line_break(),
    "(Gen. 7:2).",
    " Sometimes two conjunctive accents of the $revia separate them,",
    [" e.g. ", _ait(_SEP_DARGA), ":"],
    my_html.line_break(),
    author.hbo("אֶ֣מֶשׁ ׀ אָמַ֧ר אֵלַ֣י לֵאמֹ֗ר"),
    my_html.line_break(),
    "(Gen. 31:29) ...",
    " $Legarmeh can be consecutive, e.g.:",
    my_html.line_break(),
    author.hbo("וַיִּ֜מַח אֶֽת־כׇּל־הַיְק֣וּם ׀ אֲשֶׁ֣ר ׀ עַל־פְּנֵ֣י הָֽאֲדָמָ֗ה"),
    my_html.line_break(),
    "(Gen. 7:23).",
]

# Rule 2

_Y_C20_H = [
    author.emphasis(
        "מונח וקו מאונך הסמוכים לרביע הם תמיד מונח לגרמיה,"
        " ואף פָּסֵק הראוי לבוא מיד לפני רביע מתחלף בלגרמיה;"
        " חוץ ממקום אחד בלבד בכל המקרא."
    ),
    ' המקום היחיד הוא ישעיהו מב,ה ("הָאֵ֣ל ׀ יְהֹוָ֗ה").',
    " העדות המפורשת של המסורה קובעת:",
    ' "ולעולם לא תמצא פסק לפני רביע כי אם במקום אחד,',
    ' והוא כֹּה־אָמַ֞ר הָאֵ֣ל ׀ יְהֹוָ֗ה בּוֹרֵ֤א [הַ]שָּׁמַ֙יִם֙"',
    " (משפטי הטעמים ז' ע״ב).",
    " הַפָּסֵק בַּפָּסוּק בישעיהו מודגש במסורה במקומות נוספים,",
    " ובפסוקים האחרים שיש בהם מונח וקו מאונך הסמוכים לרביע",
    ' יש ציונים של "לגרמיה".',
]
_YOU_WILL_NEVER_FIND = [
    "You will never find $paseq before $revia except in one place,",
    " which is: ",
    author.hbo("כֹּה־אָמַ֞ר הָאֵ֣ל ׀ יְהֹוָ֗ה בּוֹרֵ֤א [הַ]שָּׁמַ֙יִם֙"),
]
_Y_C20_E = [
    author.emphasis(
        "$Munax and a vertical line adjacent to $revia"
        " are always $munleg,"
        " and even a $paseq that would be expected"
        " immediately before $revia is replaced by $legarmeh;"
        " except in one place only in the entire Bible."
    ),
    " The sole exception is Isaiah 42:5",
    [" (", author.hbo("הָאֵ֣ל ׀ יְהֹוָ֗ה"), ")."],
    " The explicit testimony of the Masorah states:",
    [" ", author.dquote(_YOU_WILL_NEVER_FIND)],
    " (Mishpetei HaTe'amim 7b).",
    " The $paseq in this verse in Isaiah",
    " is emphasized in the Masorah in several places,",
    " and in the other verses that have $munax and a vertical line",
    " adjacent to $revia there are",
    [" ", _ait("often"), " ", _ait("marginal")],
    " annotations",
    [" of ", author.dquote("לג[רמיה].")],
    # XXX The Hebrew text has "לגרמיה" but I'm guessing that these are
    # abbreviated annotations of the type "לג[רמיה]", not "לגרמיה".
]

# Rule 3: introduction

_Y_C30_H = [
    author.emphasis(
        "לעתים רחוקות בא מונח לגרמיה לפני טעמים מפסיקים אחרים (חוץ מרביע)."
    ),
    " כל המקומות האלה מפורשים בספרות המסורה:",
]
_Y_C30_E = [
    author.emphasis(
        "Rarely, $munleg comes before other disjunctive accents (besides $revia)."
    ),
    " All such cases are specified in the Masorah literature:",
]

# Rule 3.1

_Y_C31_H = [
    author.emphasis("מונח לגרמיה הסמוך לפזר (בתוך יחידה פשוטה בת שתי מילים)."),
    " מדובר על שני מקומות בלבד המצוינים במסורה,",
    " אבל בשאר כל המקומות קו מאונך לפני פזר הוא פסק;",
    " קביעה זאת של המסורה מוזכרת פעמיים בספר משפטי הטעמים.",
    " הפזר מוזכר שם כטעם מפסיק שלגרמיה יכול לבוא לפניו",
    ' (ל״ד ע״א): "',
    author.emphasis("הלגרמיה"),
    " יתכן להיות אחריו ",
    author.emphasis("רביע"),
    "... ",
    author.emphasis("ופזר"),
    ",",
    " כגון: לְמִכְנַ֣שׁ ׀ לַֽאֲחַשְׁדַּרְפְּנַיָּ֡א (דניאל ג,ב);",
    ' וְשֵׁרֵ֥בְיָ֣ה ׀ יָמִ֡ין (נחמיה ח,ז)."',
    " ועוד לפני כן כבר נזכר הפזר",
    " כטעם שלגרמיה יכול לבוא אחריו,",
    " וצויינו שם אותן שתי דוגמאות",
    ' (ל״ג ע״א): "',
    author.emphasis("הפזר"),
    " יתכן להיות אחריו ",
    author.emphasis("התלישא"),
    "... ויתכן אחריו ",
    author.emphasis("לגרמיה"),
    ":",
    " שְׁלַ֡ח לְמִכְנַ֣שׁ ׀ לַֽאֲחַשְׁדַּרְפְּנַיָּ֡א (דניאל ג,ב);",
    ' וְיֵשׁ֡וּעַ וּבָנִ֡י וְשֵׁרֵ֥בְיָ֣ה ׀ יָמִ֡ין (נחמיה ח,ז)."',
]
_LEG_CAN_FOLLOW = [
    [author.emphasis("$legarmeh"), " can follow ", author.emphasis("$revia")],
    ["... and ", author.emphasis("$pazer"), ","],
    [" e.g.: ", author.hbo("לְמִכְנַ֣שׁ ׀ לַֽאֲחַשְׁדַּרְפְּנַיָּ֡א")],
    " (Dan. 3:2);",
    [" ", author.hbo("וְשֵׁרֵ֥בְיָ֣ה ׀ יָמִ֡ין")],
    " (Neh. 8:7).",
]
_PAZ_CAN_FOLLOW = [
    [author.emphasis("$pazer"), " can follow ", author.emphasis("$telisha")],
    ["...", " and ", author.emphasis("$legarmeh"), " can follow it:"],
    [" ", author.hbo("שְׁלַ֡ח לְמִכְנַ֣שׁ ׀ לַֽאֲחַשְׁדַּרְפְּנַיָּ֡א")],
    " (Dan. 3:2);",
    # XXX same ref (Dan. 3:2) is given above; seems unlikely
    [" ", author.hbo("וְיֵשׁ֡וּעַ וּבָנִ֡י וְשֵׁרֵ֥בְיָ֣ה ׀ יָמִ֡ין")],
    " (Neh. 8:7).",
    # XXX same ref (Neh. 8:7) is given above; seems unlikely
]

_Y_C31_E = [
    author.emphasis("$Munax $legarmeh adjacent to $pazer (in a simple two-word unit)."),
    " This occurs in only two places noted in the Masorah,",
    " but in all other places a vertical line before $pazer is $paseq;",
    " this ruling of the Masorah is mentioned twice",
    " in Mishpetei HaTe'amim.",
    " $Pazer is mentioned there as a disjunctive accent",
    [" that $legarmeh can precede (34a): ", author.dquote(_LEG_CAN_FOLLOW)],
    " And earlier, $pazer is mentioned as an accent",
    " that $legarmeh can follow,",
    [" with the same two examples (33a): ", author.dquote(_PAZ_CAN_FOLLOW)],
]

# Rule 3.2

_Y_C32_H = [
    author.emphasis("מונח לגרמיה בתחום שלטונו של גרש"),
    ' (11 מקומות): “',
    author.emphasis("הלגרמיה"),
    " יתכן להיות אחריו ",
    author.emphasis("רביע"),
    "... ",
    author.emphasis("וטרס"),
    " (=גרש) לא יהיה (אחר לגרמיה)",
    " אלא אזיל ואתי (=קדמא ואזלא),",
    ' והוא בי״א מקומות במקרא, והם..."',
    " (משפטי הטעמים ל״ד ע״א-ע״ב).",
    " הפריטים ברשימה של המסורה:",
    " בראשית כח,ט; שמ״א יד,ג; שמ״א יד,מז; שמ״ב יג,לב;",
    " מל״ב יח,יז; ירמיהו ד,יט; ירמיהו לח,יא; ירמיהו מ,יא;",
    " יחזקאל ט,ב; חגי ב,יב; דה״ב כו,טו.",
]
_LEG_CAN_FOLLOW_2 = [
    author.emphasis("$legarmeh"),
    " can follow ",
    author.emphasis("$revia"),
    "... and ",
    author.emphasis("$geresh"),
    " shall not occur (after $legarmeh)",
    " except as $qadma and $azla,",
    " and it occurs in 11 places in the Bible...",
]
_Y_C32_E = [
    author.emphasis("$Munax $legarmeh in the domain of $geresh"),
    [" (11 places): ", author.dquote(_LEG_CAN_FOLLOW_2)],
    " (Mishpetei HaTe'amim 34a–b).",
    " The items in the Masorah's list:",
    " Gen. 28:9; 1 Sam. 14:3; 1 Sam. 14:47; 2 Sam. 13:32;",
    " 2 Kgs. 18:17; Jer. 4:19; Jer. 38:11; Jer. 40:11;",
    " Ezek. 9:2; Hag. 2:12; 2 Chr. 26:15.",
]

# Rule 3.3

_Y_C33_H = [
    author.emphasis("מונח לגרמיה בתחום שלטונו של פשטא"),
    ' (3 מקומות): “',
    author.emphasis("הלגרמיה"),
    " יתכן להיות אחריו ",
    author.emphasis("רביע"),
    "... ויתכן להיות אחר לגרמיה ",
    author.emphasis("פשטא"),
    " בג' מקומות, והם...”",
    " (משפטי הטעמים ל״ד ע״ב).",
    " הפריטים ברשימה של המסורה:",
    " ויקרא י,ו; ויקרא כא,י; רות א,ב.",
]
_LEG_CAN_FOLLOW_3 = [
    author.emphasis("$legarmeh"),
    " can follow ",
    author.emphasis("$revia"),
    "... and ",
    author.emphasis("$pashta"),
    " can follow $legarmeh in 3 places...",
]
_Y_C33_E = [
    author.emphasis("$Munax $legarmeh in the domain of $pashta"),
    [" (3 places): ", author.dquote(_LEG_CAN_FOLLOW_3)],
    " (Mishpetei HaTe'amim 34b).",
    " The items in the Masorah's list:",
    " Lev. 10:6; Lev. 21:10; Ruth 1:2.",
]

# Rule 3.4

_Y_C34_H = [
    author.emphasis("מונח לגרמיה לפני תביר"),
    ", שהוא תחליפו של גרש",
    " (משפטי הטעמים ל״ד ע״ב):",
    ' "ויתכן אחריו ',
    author.emphasis("תביר"),
    " במקום אחד,",
    " והוא: וַיִּשְׁלַ֥ח מֶֽלֶךְ־אַשּׁ֣וּר ׀",
    " אֶת־רַבְשָׁקֵ֨ה מִלָּכִ֧ישׁ יְרוּשָׁלַ֛͏ְמָה",
    " (ישעיהו לו,ב),",
    ' ולא יהיה לו שכן אחד מן הטעמים חוץ ממה שנזכר."',
]
_AND_TEVIR = [
    "and ",
    author.emphasis("$tevir"),
    " can follow it in one place, which is: ",
    author.hbo(
        "וַיִּשְׁלַ֥ח מֶֽלֶךְ־אַשּׁ֣וּר ׀ אֶת־רַבְשָׁקֵ֨ה מִלָּכִ֧ישׁ יְרוּשָׁלַ֛͏ְמָה"
    ),
    " (Isa. 36:2),",
    " and it shall have no other neighboring accent",
    " besides what has been mentioned.",
]
_Y_C34_E = [
    [author.emphasis("$Munax $legarmeh before $tevir"), ","],
    " which is a substitute for $geresh",
    " (Mishpetei HaTe'amim 34b):",
    [" ", author.dquote(_AND_TEVIR)],
]

# Discussion of 3.1 vs 3.2-4

_Y_C40_H = [
    "לגרמיה הסמוך לפזר (3.1)",
    " שונה באופן עקרוני משלושת הסוגים הבאים אחריו (3.2-4),",
    " כי אצלם ",
    author.emphasis("כל"),
    " המקרים בסוג הם לגרמיה,",
    " ואילו לגבי לגרמיה הסמוך לפזר ",
    author.emphasis("רק בשני המקומות האלה"),
    " מדובר על לגרמיה ובכל שאר המקומות הוא פסיק.",
    " אפילו בפסוק בנחמיה שבו יש לגרמיה לפני פזר,",
    " בהמשך יש פָּסֵק באותן נסיבות בדיוק",
    " (כלומר מונח לגרמיה הסמוך לפזר",
    " בתוך יחידה פשוטה בת שתי מילים,",
    " כדי להפריד בין שני פריטים בתוך רשימה של שמות):",
    ' "וְיֵשׁ֡וּעַ וּבָנִ֡י וְשֵׁרֵ֥בְיָ֣ה ׀ יָמִ֡ין עַקּ֡וּב ',
    author.emphasis("שַׁבְּתַ֣י ׀ הֽוֹדִיָּ֡ה"),
    '"',
    " (הקו המאונך האחרון הוא פסק דווקא).",
    " וכבר תהה ברויאר:",
    ' "הלגרמיה של וְשֵׁרֵ֥בְיָ֣ה ׀ יָמִ֡ין',
    " דומה לפסק של שַׁבְּתַ֣י ׀ הֽוֹדִיָּ֡ה שבאותו פסוק...",
    " אין אנחנו יודעים,",
    " על שום מה נשתנו שני השמות הסמוכים לפזר;",
    ' שהאחד מוטעם בלגרמיה וחברו במונח לפני פסק."',
]
_Y_C41_H = [
    'למרות התמיהה יש סימן מובהק שב"וְשֵׁרֵ֥בְיָ֣ה ׀ יָמִ֡ין"',
    " מדובר על מונח לגרמיה,",
    ' והוא טעם המרכא בתיבה "וְשֵׁרֵ֥בְיָ֣ה ׀";',
    " מרכא הוא משרתו של לגרמיה דווקא (ולא משרתו של המונח).",
    " אפילו אהרן דותן,",
    " שדחה לחלוטין את האפשרות",
    " שלגרמיה יבוא בתחום פזר באף מקום,",
    ' ועל עדות המסורה לשני המקומות כתב "ודאי שיבוש הוא",',
    " נימק את עמדתו כך:",
    ' "ואף ממשרתיו של מונח לגרמיה מוכרע הדבר.',
    " בידוע שמשרתו מירכא,",
    ' אך לפני מונח ופסק שאינם לגרמיה לא יימצא מירכא לעולם."',
    ' אך הקו תחת האות רי״ש בתיבה "וְשֵׁרֵ֥בְיָ֣ה ׀"',
    " נוטה במקצת לצד שמאל בכתי״ל ובכתי״ש1, כדין מרכא,",
    " וכך הכריע דותן בעצמו במהדורות של המקרא שהוציא לאור.",
]
_Y_C42_H = [
    "לגבי הפסוק בדניאל שבו יש לגרמיה לפני פזר,",
    " ברויאר הראה שעל פי הפסוקים המקבילים",
    " שיש בהם טעם מפסיק",
    ' (דניאל ג,ג "מִֽתְכַּנְּשִׁ֡ין אֲחַשְׁדַּרְפְּנַיָּ֡א";',
    ' ג,כז "וּ֠מִֽתְכַּנְּשִׁ֠ין אֲחַשְׁדַּרְפְּנַיָּ֞א"),',
    " הלגרמיה רומז לפזר שהיה ראוי לבוא במקום המונח.",
    " בנוסף, יש לזכור שבשני הפסוקים יש ציון מפורש",
    ' של "לגרמיה" בכתי״ל,',
    " ושניהם נעדרים מרשימת הפסק שבו.",
]
_Y_C40_E = [
    "The $legarmeh adjacent to $pazer (3.1)",
    " is fundamentally different from",
    " the three types that follow it (3.2–4),",
    [" because in those cases ", author.emphasis("all")],
    " instances are $legarmeh, whereas for $legarmeh adjacent to $pazer",
    [" ", author.emphasis("only these two places")],
    " are $legarmeh",
    " and in all other places it is $paseq.",
    " Even in the verse in Nehemiah that has $legarmeh before $pazer,",
    " later in the same verse there is $paseq in exactly the same circumstances",
    " (i.e. $munleg adjacent to $pazer in a simple two-word unit,",
    " separating two items in a list of names):",
    [" ", author.hbo("וְיֵשׁ֡וּעַ וּבָנִ֡י וְשֵׁרֵ֥בְיָ֣ה ׀ יָמִ֡ין עַקּ֡וּב")],
    [" ", author.emphasis(author.hbo("שַׁבְּתַ֣י ׀ הֽוֹדִיָּ֡ה"))],
    " (the last vertical line is specifically $paseq).",
    " Breuer already wondered:",
    [
        " ",
        author.dquote(
            [
                "The $legarmeh of ",
                author.hbo("וְשֵׁרֵ֥בְיָ֣ה ׀ יָמִ֡ין"),
                " resembles the $paseq of ",
                author.hbo("שַׁבְּתַ֣י ׀ הֽוֹדִיָּ֡ה"),
                " in the same verse...",
                " We do not know",
                " why the two names adjacent to $pazer differ;",
                " one is accented with $legarmeh",
                " and the other with $munax before $paseq.",
            ]
        ),
    ],
]
_Y_C41_E = [
    "Despite this puzzlement,",
    [" there is a clear sign that in ", author.hbo("וְשֵׁרֵ֥בְיָ֣ה ׀ יָמִ֡ין")],
    " it is $munleg:",
    [" the $merkha accent on the word ", author.hbo("וְשֵׁרֵ֥בְיָ֣ה ׀")],
    ";",
    " $merkha is specifically the conjunctive of $legarmeh",
    " (not the conjunctive of $munax).",
    " Even Aron Dotan,",
    " who completely rejected the possibility",
    " that $legarmeh could occur in the domain of $pazer at all,",
    " and wrote of the Masorah's testimony for these two places",
    [" ", author.dquote("it is certainly an error,")],
    " reasoned as follows:",
]
_Y_C41b_E = [
    "The matter is also decided from the conjunctive accents",
    " of $munleg.",
    " It is known that its conjunctive is $merkha,",
    " but before a $munax and $paseq that are not $legarmeh,",
    " $merkha will never be found.",
]
_Y_C41c_E = [
    "However, the line under the letter $resh",
    [" in the word ", author.hbo("וְשֵׁרֵ֥בְיָ֣ה ׀")],
    " leans slightly to the left",
    " in the Leningrad Codex and the Sassoon 1053 manuscript,",
    " as befits $merkha,",
    " and this is how Dotan himself decided",
    " in the editions of the Bible he published.",
]
_Y_C42_E = [
    "Regarding the verse in Daniel",
    " that has $legarmeh before $pazer,",
    " Breuer showed that based on the parallel verses",
    " with a disjunctive accent",
    [" (Dan. 3:3 ", author.hbo("מִֽתְכַּנְּשִׁ֡ין אֲחַשְׁדַּרְפְּנַיָּ֡א")],
    ";",
    [" 3:27 ", author.hbo("וּ֠מִֽתְכַּנְּשִׁ֠ין אֲחַשְׁדַּרְפְּנַיָּ֞א")],
    "),",
    " the $legarmeh hints at a $pazer",
    " that should have come instead of the $munax.",
    " Additionally, in both verses there is",
    " an explicit $legarmeh",
    " annotation in the Leningrad Codex,",
    " and both are absent from the $paseq list therein.",
]

# Historical discussion + Dotan quotes + Breuer + summary

_Y_C50_H = [
    "ייתכן שבמקור לא היה הבדל מובהק בין לגרמיה ופסק,",
    " שהרי שניהם באים להורות על הפסקה כלשהי",
    " ויש סימן אחד לשניהם (הקו המאונך).",
    " היידנהיים כבר הציע שלגרמיה נחשב סוג של פסק בעיני חכמי המסורה",
    " (משפטי הטעמים ל״א ע״ב):",
    ' "בעבור שהלגרמיה הוא המפסיק בין המונח והטעם שאחריו,',
    ' לכן לא נמנע החכם להכניסו בביאור הפסק."',
    " דותן דחה את דעתו, אך בכל זאת הציע דבר דומה.",
    ' על הדברים ב"ביאור הפסק",',
    " המציעים מטרה ",
    author.emphasis("משותפת"),
    " לדוגמאות של לגרמיה ופסק כאחד,",
    ' דהיינו "להפריד בין הטעמים שיהיו מופרדים איש מאחיו ולא נצמדים",',
    " כתב:",
]
_Y_C50_E = [
    "It is possible that originally there was no clear distinction",
    " between $legarmeh and $paseq,",
    " since both serve to indicate some kind of pause",
    " and share the same sign (the vertical line).",
    " Heidenheim already suggested that $legarmeh",
    " was considered a type of $paseq",
    " in the eyes of the Masorah scholars",
    " (Mishpetei HaTe'amim 31b):",
    [
        " ",
        author.dquote(
            [
                "Since $legarmeh is what separates the $munax",
                " from the accent that follows it,",
                " the sage did not refrain from including it",
                " in the explanation of $paseq.",
            ]
        ),
    ],
    " Dotan rejected this view, yet proposed something similar.",
    [" Regarding the statements in the ", author.dquote("explanation of $paseq,")],
    [" which suggest a ", author.emphasis("shared")],
    " purpose",
    " for examples of $legarmeh and $paseq alike,",
    [
        " namely ",
        author.dquote(
            [
                "to separate the accents so that they are distinct",
                " from one another and not attached,",
            ]
        ),
    ],
    " he wrote:",
]

_Y_C51_H = [
    "אכן זהו תפקידו של הפָסק",
    " בין שהוא בא אחרי מונח בתחום הרביע",
    " והופך אותו לטעם מפסיק – מונח לגרמיה,",
    " ובין שהוא בא אחרי מונח בתחום פזר",
    " וגורם להפסקה שכוחה ככוח טעם מפסיק;",
    " וממונח בתחום פזר רשאים אנו ללמוד גזרה שווה",
    " אף על פסק שאחרי כל משרת אחר ובכל תחום...",
]
_Y_C51_E = [
    "Indeed, this is the function of $paseq:",
    " whether it comes after $munax in the domain of $revia,",
    " transforming it into a disjunctive accent — $munleg,",
    " or whether it comes after $munax in the domain of $pazer,",
    " causing a pause with the force of a disjunctive accent;",
    " and from the $munax in the domain of $pazer",
    " we may infer by analogy to $paseq",
    " after every other conjunctive accent in every domain...",
]

_Y_C52_H = [
    "בכל זאת יש מקום לפשפש בניצניה של תפיסה זו,",
    " שאי אפשר היה לה שתצמח על קרקעה של מערכת המושגים המקובלת",
    " (שהיא גם היחידה הידועה לנו),",
    " שבה מונח לגרמיה ופסק הם עניינים רחוקים זה מזה תכלית ריחוק",
    " – פסק אינו שייך כלל למערכת הטעמים –",
    " ודבר אין להם זה עם זה מלבד שיתוף הסימן.",
    " וסימן הפָסק ",
    author.emphasis("לבדו"),
    " בוודאי אינו סימן טעם, סימן מוסיקאלי,",
    " אלא סימן פיסוק בלבד.",
    " עצם העובדה, ששניהם נכרכו כאן ביחד,",
    " ושמונח לגרמיה הוכלל בקטגוריה של פסק,",
    " מניחה מקום לסברה",
    " שלכתחילה לא היה הבדל מהותי בין השניים,",
    " ושלא תמיד היה מונח לגרמיה נחשב טעם עצמאי במערכת הטעמים.",
    " רישומיה של אותה תקופת בראשית",
    " בהתהוות מערכת הטעמים עדיין ניכרים\u2026",
]
_Y_C52_E = [
    "Yet there is room to investigate the origins of this view,",
    " which could not have grown on the ground",
    " of the accepted conceptual system",
    " (which is also the only one known to us),",
    " in which $munleg and $paseq",
    " are matters far removed from each other",
    " — $paseq does not belong at all to the accentuation system —",
    " and they have nothing to do with each other",
    " besides sharing a sign.",
    [" The sign of $paseq ", author.emphasis("alone")],
    " is certainly not an accentual sign, a musical sign,",
    " but merely a punctuation mark.",
    " The very fact that both were grouped together here,",
    " and that $munleg",
    " was included in the category of $paseq,",
    " leaves room for the conjecture",
    " that originally there was no essential difference between the two,",
    " and that $munleg was not always considered",
    " an independent accent in the accentuation system.",
    " Traces of that early period in the development",
    " of the accentuation system are still discernible\u2026",
]

_Y_C60_H = [
    "ברויאר הדגיש את הדמיון הרב בין פסק",
    " לבין לגרמיה הבא ביחידה פשוטה בת שתי תיבות:",
]
_Y_C60_E = [
    "Breuer emphasized the great similarity between $paseq",
    " and $legarmeh occurring in a simple two-word unit:",
]

_Y_C61_H = [
    "ברוב המקומות, שיש בהם לגרמיה סמוך לרביע, פזר או קדמא,",
    " הרי זה מסתבר, שהלגרמיה איננו אלא תחליף של משרת ופסק.",
    " ולפיכך בכל המקומות שלגרמיה סמוך בהם לרביע או לפזר,",
    " היה זה מתקבל על הדעת לומר, שאין זה לגרמיה כלל,",
    " אלא זהו מונח שלפני פסק;",
    " שהרי מונח משמש כמשרתם הרגיל של רביע ופזר.",
    " אולם המסורה תפסה את כל המונחים האלה כלגרמיה,",
    " ולפיכך לא מנתה אותם ברשימת הפסקים.",
    " וכן מסרו הקדמונים (משפה״ט ז, ע״ב):",
    " ולעולם לא תמצא פסק לפני רביע,",
    " כי אם במקום אחד במקרא",
    " והוא כֹּה־אָמַ֞ר הָאֵ֣ל ׀ ה֗' בּוֹרֵ֤א הַשָּׁמַ֙יִם֙ (יש' מב, ה).",
    " ומכאן, שכל התופעה שנידונה לעיל,",
    " נשענת רק על עדות המסורה, ולא על נוסח הטעמים שבמקרא גופו.",
]
_Y_C61_E = [
    "In most places where $legarmeh is adjacent to $revia, $pazer, or $qadma,",
    " it is plausible that $legarmeh is nothing but",
    " a substitute for a conjunctive accent and $paseq.",
    " Therefore, in all the places where $legarmeh",
    " is adjacent to $revia or $pazer,",
    " it would have been reasonable to say",
    " that it is not $legarmeh at all,",
    " but rather a $munax before $paseq;",
    " since $munax serves as the regular conjunctive",
    " of $revia and $pazer.",
    " However, the Masorah treated all these $munax accents as $legarmeh,",
    " and therefore did not count them in the $paseq lists.",
    " As the ancients transmitted (Mishpetei HaTe'amim 7b):",
    [
        " ",
        author.dquote(
            [
                "You will never find $paseq before $revia,",
                " except in one place in the Bible,",
                " which is: ",
                author.hbo("כֹּה־אָמַ֞ר הָאֵ֣ל ׀ ה֗' בּוֹרֵ֤א הַשָּׁמַ֙יִם֙"),
                " (Isa. 42:5).",
            ]
        ),
    ],
    " Hence, the entire phenomenon discussed above rests solely",
    " on the testimony of the Masorah,",
    " not on the accent text of the Bible itself.",
]

_Y_C70_H = [
    "יוצא לנו שהמסורה מעידה במפורש על לגרמיה",
    " בפסוקים רבים שנראה שיש בהם פסק.",
    " אבל ייתכן שמלכתחילה לא היה הבדל מהותי ביניהם,",
    " ולמעשה הרבה מקרים של לגרמיה",
    " הם בעצם תחליף של משרת ופסק.",
]
_Y_C70_E = [
    "We thus find that the Masorah explicitly testifies to $legarmeh",
    " in many verses that appear to have $paseq.",
    " But it is possible that originally",
    " there was no essential difference between them,",
    " and in practice many cases of $legarmeh",
    " are in fact a substitute for a conjunctive accent and $paseq.",
]

# ═══════════════════════════════════════════════════════════════════
# Sub-section ד: Typographic marking
# ═══════════════════════════════════════════════════════════════════

_Y_D01_H = [
    author.emphasis('ד. דרך הסימון של "פָּסֵק" ושל "לְגַרְמֵיהּ" במהדורתנו:'),
    ' יש רק תו אחד ביוניקוד בשביל "פָּסֵק" ובשביל "לְגַרְמֵיהּ" כאחד,',
    " למרות שמשמעותם שונה.",
    " אבל בגלל המנהג המקובל (בכל הדפוסים והמהדורות)",
    " לסמן את הקו המאונך רק לאחר רווח בסוף התיבה,",
    " ניתן בקלות ובלי סרבול מיותר לעשות הבחנה בעיצובם",
    " על ידי השימוש באחת משתי תבניות שונות בסוף כל תיבה מתאימה:",
]
_Y_D01_E = [
    author.emphasis(
        [
            "ד. The method of marking $paseq",
            " and $legarmeh in our edition:",
        ]
    ),
    " Unicode has only one character",
    " for both $paseq and $legarmeh,",
    " despite their different meanings.",
    " However, because the accepted convention",
    " (in all printed editions)",
    " is to mark the vertical line only after a space at the end of a word,",
    " it is possible — easily and without unnecessary complication —",
    " to visually distinguish them",
    " by using one of two different templates",
    " at the end of each relevant word:",
]

_Y_D10_H = [
    author.emphasis("תבנית לגרמיה:"),
    ' תבנית זו יוצרת קו מודגש של "לגרמיה"',
    " לאחר רווח מיוחד קצר,",
    " ולאחר הקו רווח רגיל.",
    " קו הלגרמיה מהווה חלק מטעם מפסיק של תיבה,",
    " ואינו קשור לתיבה הבאה.",
    " הוא בא לציין שאין כאן מונח רגיל (טעם מחבר)",
    ' אלא מונח שהוא טעם מפסיק ("לגרמיה").',
]
_Y_D10_E = [
    author.emphasis("$Legarmeh template:"),
    " This template creates a bold $legarmeh line",
    " after a short special space (thin space),",
    " followed by a regular space.",
    " The $legarmeh line is part of a disjunctive accent of a word",
    " and is not related to the following word.",
    " It indicates that here there is not",
    " a regular $munax (conjunctive accent)",
    " but rather a $munax that is a disjunctive accent",
    " ($munleg).",
]

_Y_D20_H = [
    author.emphasis("תבנית פסק:"),
    " תבנית זו יוצרת קו מוקטן של פסק בצבע אפור",
    " בתוך שני רווחים מיוחדים וקצרים לפניו ולאחריו.",
    " קו פסק בא להבחין הבחנה קלה בלבד",
    " בין שתי תיבות המחוברות בטעם מחבר",
    " כדי להזכיר לקורא להבחין ביניהם,",
    " ואינו אמור להפריע לרצף של הטעמים בקריאה.",
    " הפסק כשלעצמו אינו טעם,",
    " והוא בא בדרך כלל בין שתי תיבות דומות או מסיבות אחרות.",
]
_Y_D20_E = [
    author.emphasis("$Paseq template:"),
    " This template creates a smaller $paseq line in gray",
    " between two short special spaces (thin spaces)",
    " before and after it.",
    " A $paseq line serves to make only a slight distinction",
    " between two words connected by a conjunctive accent,",
    " to remind the reader to distinguish between them,",
    " and it is not meant to interrupt",
    " the flow of the accents in reading.",
    " $Paseq itself is not an accent,",
    " and it usually comes between two similar words",
    " or for other reasons.",
]

# ═══════════════════════════════════════════════════════════════════
# Sub-section ה: Emet books
# ═══════════════════════════════════════════════════════════════════

_Y_E01_H = [
    author.emphasis("ה. פסק ולגרמיה בספרי אמ״ת:"),
    " בספרי אמ״ת יש שני טעמים של לגרמיה:",
    ' "אָזְלָא לְגַרְמֵיהּ" ו"מַהְפָּךְ לְגַרְמֵיהּ".',
    " הקו המאונך הבא אחרי הטעמים אזלא ומהפך כדי לציין לגרמיה,",
    " הוא לעתים תחליפו של משרת שיש לאחריו פסק,",
    " ויש בו דמיון ללגרמיה בכ״א הספרים הבא בסמיכות לרביע.",
]
_Y_E01_E = [
    author.emphasis("ה. $Paseq and $legarmeh in the poetic books:"),
    " In the poetic books there are two $legarmeh accents:",
    " $azla $legarmeh and $mahapakh $legarmeh.",
    " The vertical line that comes after $azla and $mahapakh",
    " to indicate $legarmeh",
    " is sometimes a substitute",
    " for a conjunctive accent followed by $paseq,",
    " and it resembles $legarmeh in the 21 books",
    " occurring adjacent to $revia.",
]

_Y_E02_H = [
    'ההבחנה בין "פסק" ו"לגרמיה" בספרי אמ״ת',
    " נבדקה מול רשימת הלגרמיה של גינצבורג",
    " ובעיקר מול רשימת הפסק שלו,",
    " המבוססת לא רק על הערות בכתבי־יד",
    " אלא גם על רשימות מסורה מובהקות.",
    " אך יש מספר פריטים של מהפך לגרמיה ואזלא לגרמיה",
    " הנמצאים ברשימת הפסק שלו, ואותם סימנו כלגרמיה;",
    " רובם נמצאים גם כן ברשימת הלגרמיה.",
    " ובמקומות אחרים יש קו מאונך של פסק בכתר ארם צובה",
    " שאינו מובא ברשימת הפסק,",
    ' רובם אחרי התיבה "לַמְנַצֵּ֬חַ ׀" בכותרות של מזמורים.',
]
_Y_E02_E = [
    "The distinction between",
    " $paseq",
    " and $legarmeh",
    " in the poetic books was checked against",
    " Ginsburg's $legarmeh list",
    " and especially against his $paseq list,",
    " which is based not only on annotations in manuscripts",
    " but also on authoritative Masorah lists.",
    " However, there are several",
    " $mahapakh $legarmeh and $azla $legarmeh items",
    " found in his $paseq list,",
    " which we marked as $legarmeh;",
    " most of them are also found in the $legarmeh list.",
    " In other places there is a $paseq vertical line",
    " in the Aleppo Codex",
    " that is not listed in the $paseq list,",
    [" most of them after the word ", author.hbo("לַמְנַצֵּ֬חַ ׀")],
    " in psalm headings.",
]

# ═══════════════════════════════════════════════════════════════════
# Sub-section ו: Shalshelet
# ═══════════════════════════════════════════════════════════════════

_Y_F01_H = [
    author.emphasis("ו. הקו המאונך אחרי שלשלת:"),
    ' גם את הקו המאונך של הטעם המפסיק "שלשלת" (בכ״א הספרים)',
    ' ומקבילו "שלשלת גדולה" (בספרי אמ״ת)',
    " עיצבנו בעיצוב של לגרמיה.",
    " על הקו הזה כתב ברויאר:",
    ' "אחרי תיבת שלשלת יש תמיד קו דמוי פָּסֵק,',
    " כגון: וַיֹּאמַ֓ר ׀ (בר' כד, יב).",
    " קו זה בא להבדיל בין שלשלת גדולה המפסיק",
    " לבין שלשלת קטנה המשרת.",
    " שני הטעמים האלה מצויים באמ״ת, והם שוים בצורתם;",
    " משום כך היה צורך להבדיל ביניהם באמ״ת.",
    ' משם הועבר הקו גם אל כ״א ספרים,',
    ' אף על פי ששלשלת מצויה בהם רק כטעם מפסיק."',
]
_Y_F01_E = [
    author.emphasis("ו. The vertical line after $shalshelet:"),
    " We also styled the vertical line",
    [" of the disjunctive accent ", author.dquote("$shalshelet")],
    " (in the 21 books)",
    [" and its counterpart ", author.dquote("$shalshelet_gedolah")],
    " (in the poetic books)",
    " in the $legarmeh style.",
    " About this line, Breuer wrote:",
]
_Y_F02_E = [
    "After a $shalshelet word there is always a $paseq-like line,",
    " e.g.: ",
    author.hbo("וַיֹּאמַ֓ר ׀"),
    " (Gen. 24:12).",
    " This line serves to distinguish",
    " between the disjunctive $shalshelet_gedolah",
    " and the conjunctive $shalshelet_qetanah.",
    " Both of these accents are found in the poetic books,",
    " and they are identical in form;",
    " therefore it was necessary to distinguish between them",
    " in the poetic books.",
    " From there, the line was transferred also to the 21 books,",
    " even though $shalshelet is found in them",
    " only as a disjunctive accent.",
]

####################################
# Triple assembly
####################################


def _ph(h):
    return author.para_modhe(h)


def _pe(e):
    return author.para(e)


def _bqph(h):
    return my_html.blockquote(author.para_modhe(h))


def _bqpe(e):
    return my_html.blockquote(author.para(e))


# fmt: off
_TRIPLES = [
    # Section heading
    ("Section heading", _ph(_Y_SEC_H), _pe(_Y_SEC_E)),
    # Sub-section א: Definition of paseq and legarmeh
    ("Sub-section א: definition of $paseq and $legarmeh",
     _ph(_Y_A01_H), _pe(_Y_A01_E)),
    ("Sub-section א continued: definition of $legarmeh",
     _ph(_Y_A02_H), _pe(_Y_A02_E)),
    ("Sub-section א continued: reader's need to distinguish",
     _ph(_Y_A03_H), [_pe(_Y_A03_E), _pe(_Y_A03b_E)]),
    # Sub-section ב: Textual basis
    ("Sub-section ב: textual basis",
     _ph(_Y_B01_H), _pe(_Y_B01_E)),
    # Sub-section ג: Distinction between legarmeh and paseq
    ("Sub-section ג: introduction",
     _ph(_Y_C01_H), _pe(_Y_C01_E)),
    ("Sub-section ג: rule 1",
     _ph(_Y_C10_H), [_pe(_Y_C10_E), _bqpe(_Y_C11_E)]),
    ("Sub-section ג: rule 2",
     _ph(_Y_C20_H), _pe(_Y_C20_E)),
    # Rule 3 with sub-rules
    ("Sub-section ג: rule 3",
     _ph(_Y_C30_H), _pe(_Y_C30_E)),
    (None, _ph(_Y_C31_H), _pe(_Y_C31_E)),
    (None, _ph(_Y_C32_H), _pe(_Y_C32_E)),
    (None, _ph(_Y_C33_H), _pe(_Y_C33_E)),
    (None, _ph(_Y_C34_H), _pe(_Y_C34_E)),
    # Discussion of legarmeh adjacent to pazer
    ("Sub-section ג: discussion of $legarmeh adjacent to $pazer",
     _ph(_Y_C40_H), _pe(_Y_C40_E)),
    (None, _ph(_Y_C41_H), [_pe(_Y_C41_E), _bqpe(_Y_C41b_E), _pe(_Y_C41c_E)]),
    (None, _ph(_Y_C42_H), _pe(_Y_C42_E)),
    # Historical perspective and scholarly discussion
    ("Sub-section ג: historical perspective and scholarly discussion",
     _ph(_Y_C50_H), _pe(_Y_C50_E)),
    (None, _bqph(_Y_C51_H), _bqpe(_Y_C51_E)),
    (None, _bqph(_Y_C52_H), _bqpe(_Y_C52_E)),
    (None, _ph(_Y_C60_H), _pe(_Y_C60_E)),
    (None, _bqph(_Y_C61_H), _bqpe(_Y_C61_E)),
    (None, _ph(_Y_C70_H), _pe(_Y_C70_E)),
    # Sub-section ד: Typographic marking
    ("Sub-section ד: typographic marking",
     _ph(_Y_D01_H), _pe(_Y_D01_E)),
    (None, _ph(_Y_D10_H), _pe(_Y_D10_E)),
    (None, _ph(_Y_D20_H), _pe(_Y_D20_E)),
    # Sub-section ה: Emet books
    ("Sub-section ה: $paseq and $legarmeh in Emet books",
     _ph(_Y_E01_H), _pe(_Y_E01_E)),
    (None, _ph(_Y_E02_H), _pe(_Y_E02_E)),
    # Sub-section ו: Shalshelet
    ("Sub-section ו: vertical line after $shalshelet",
     _ph(_Y_F01_H), [_pe(_Y_F01_E), _bqpe(_Y_F02_E)]),
]
# fmt: on

_TITLE = "Paseq and legarmeh"
_H1_CONTENTS = "$Paseq and $legarmeh"
_FNAME = "he_ws_intro_to_mam_pasleg.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")
_WS_URL = (
    "https://he.wikisource.org/wiki/"
    "ויקיטקסט:מבוא_למקרא_על_פי_המסורה/פרק_ב"
    "#פסק_ולגרמיה"
)
_WS_LINK = my_html.anchor_h("Hebrew Wikisource", _WS_URL)
_PROVENANCE = author.para(
    [
        "The Hebrew text below is from Avi Kadish's introduction to the",
        " Miqra al pi ha-Masora edition (Chapter 2) on ",
        _WS_LINK,
        ". The English translation is original to this project.",
    ]
)
_CBODY = [
    author.heading_level_1(_H1_CONTENTS),
    _PROVENANCE,
    author.he_en_table_wct(_TRIPLES),
]

# file:///C:/Users/BenDe/GitRepos/MAM-with-doc/docs/misc/he_ws_intro_to_mam_pasleg.html
