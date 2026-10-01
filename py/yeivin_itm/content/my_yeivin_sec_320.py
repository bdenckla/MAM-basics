import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp
import yeivin_itm.content.my_yeivin_amisc_sec_320_footnotes as ftnts

_CONT_PARA_WORDS_OF_THE_THREE_PATTERNS = [
    ["Words of the three patterns described in ", hlp.rtn(319)],
    [" are said to have a structure that is not just regular but fully regular."],
    [" As mentioned above, if a word of this structure has a disjunctive accent,"],
    [" $gaya is generally marked,"],
    [" but if the accent is conjunctive,"],
    [" $gaya is generally not marked."],
    [" This general rule holds good in about 90% of the cases"],
    [" but there are ", hlp.ftntjoin("exceptions.", ftnts.FTNT_90_PERCENT)],
    [" In a few dozen cases the accent is disjunctive,"],
    [" but $gaya"],
    [" is not ", hlp.ftntjoin("marked.", ftnts.FTNT_FOR_FEW_DOZEN)],
    [" E.g.:"],
]

_PARA_WORDS_OF_THE_THREE_PATTERNS = sub.para(_CONT_PARA_WORDS_OF_THE_THREE_PATTERNS)
_LEV_AND_DT = hlp.make_dloc("@Lev 11:7", "@Dt 14:8")  # also used in 324
_TABLE_1 = hlp.table_std_rtl(
    [
        [
            *hlp.lns("@Neḥ 1:3", "מִן־הַשְּׁבִי֙", hlp.sy4pe("מִן־-הַ_-שְּׁבִי֙")),
            sub.fr1(),
        ],
        [
            *hlp.lns("@Ex 28:5", "וְאֶת־הַתְּכֵ֖לֶת", hlp.sy4("וְאֶת־-הַ_-תְּכֵ֖-לֶת")),
            sub.fr1(),
        ],
        [*hlp.lns("@Gen 34:3", "וַיֶּאֱהַב֙", hlp.sy4pe("וַ_-יֶּ-אֱהַב֙")), sub.fr3()],
        # MAM has gaʿya on yod; see closed issue https://github.com/bdenckla/trope/issues/374.
        [*hlp.lns("@Jud 16:3", "וַיֶּאֱחֹ֞ז", hlp.sy4pe("וַ_-יֶּ-אֱחֹ֞ז")), sub.fr3()],
        [
            *hlp.lns(_LEV_AND_DT, "וְאֶת־הַ֠חֲזִ֠יר", hlp.sy4pe("וְאֶת־-הַ֠-חֲזִ֠יר")),
            sub.fr3(),
        ],
    ]
)
_CONT_PARA_CONVERSELY = [
    ["Conversely, there are about 200 cases in which the accent is conjunctive, but "],
    ["$gaya is nevertheless ", hlp.ftntjoin("marked.", ftnts.FTNT_200)],
    [" E.g.:"],
]
_PARA_CONVERSELY = sub.para(_CONT_PARA_CONVERSELY)
_IS_AND_MI = hlp.make_dloc("@Is 14:29", "@Mi 7:8")
_TABLE_2 = hlp.table_std_rtl(
    [
        [
            *hlp.lns("@Ez 37:23", "יִֽטַּמְּא֣וּ", hlp.sy4ps("יִֽ_-טַּ_-מְּא֣וּ")),
            sub.fr1(),
        ],
        [
            *hlp.lns(
                "@2C 30:24", "וַיִּֽתְקַדְּשׁ֥וּ", hlp.sy4("וַ_-יִּֽתְ-קַ_-דְּשׁ֥וּ")
            ),
            sub.fr1(),
        ],
        [
            *hlp.lns("@Gen 11:2", "וַֽיִּמְצְא֥וּ", hlp.sy4ps("וַֽ_-יִּמְ-צְא֥וּ")),
            sub.fr2(),
        ],
        [
            *hlp.lns(_IS_AND_MI, "אַֽל־תִּשְׂמְחִ֤י", hlp.sy4ps("אַֽל־-תִּשְׂ-מְחִ֤י")),
            sub.fr2(),
        ],
        [
            *hlp.lns(
                "@Jud 3:28", "אֶֽת־מַעְבְּר֤וֹת", hlp.sy4ps("אֶֽת־-מַעְ-בְּר֤וֹת")
            ),
            sub.fr2(),
        ],
        [
            *hlp.lns(
                "@Nu 11:22", "אֶֽת־כׇּל־דְּגֵ֥י", hlp.sy4ps("אֶֽת־-כׇּל־-דְּגֵ֥י")
            ),
            sub.fr2(),
        ],
        [
            *hlp.lns(
                "@Jos 22:20", "וְעַֽל־כׇּל־עֲדַ֥ת", hlp.sy4ps("וְעַֽל־-כׇּל־-עֲדַ֥ת")
            ),
            sub.fr2(),
        ],
    ]
)
SEC = [_PARA_WORDS_OF_THE_THREE_PATTERNS, _TABLE_1, _PARA_CONVERSELY, _TABLE_2]

# Yeivin Keter 5729 (1968) is shown as being at the Catholic University of America library:
# https://search.worldcat.org/title/4013371
#
# Yeivin Keter 5729 (1968), יב.9 (section 12.9), starting on page 99:
#
# שאר היוצאים מן הכלל מספרם אינו רב, והם מנויים לחלק, לפי הטעמים שהתיבות מוטעמות בהם. על רובם יש הילופים או הסכמות.
#
# פשתא.
#
#     וְנִוַּסְּרוּ֙ (אק יח׳ כג,הח; לש1 מחוקה געיה; ל13 בגיה; הסכמה) bcv Ee23:48
#     אִם־תַּעְצְרֵ֙נִי֙ (שו יג,טז ל מחוקה געיה; הילוף) bcv Ju13:16
#     אֶל־בֶּן־הֲדַד֙ ... bcv 2C16:2
#     מִן־הַשְּׁבִי֙ ... bcv Ne1:3
#
# בדוגמות אחדות בטעם זה מועדפת געיה קלה מן הכבדה, שלא כרגיל:
#
#     וַיֶּֽחֱצֵם֙ ... bcv Ju9:43
#     וַיֶּֽאֱסֹף֙ ... bcv 1C23:2
#     וַיֶּֽאֱהַב֙ ... bcv G34:3
#     וַיֶּֽחֱזַק֙ ... bcv E7:13
#     וַיֶּֽחֱזַק֙ ... bcv E9:35
#     וַיֶּֽחֱזוּ֙ ... bcv E24:11
#     וַיְנַֽאֲפוּ֙ ... bcv Je29:23
#
# בין התיבות שבאה בהן געיה, כדיך, יש חילוף על:
#
#     הַמְדַבְּרִים֙ (ג.7). bcv E6:27
#
# טפחא.
#
# Ju9:43	וַיֶּאֱרֹ֖ב
# Je3:9	וַתֶּחֱנַ֖ף
# 2C8:3	וַיֶּחֱזַ֖ק
# I51:15	וַיֶּהֱמ֖וּ
# I26:8	וּלְזִכְרְךָ֖
# G13:12	וַיֶּאֱהַ֖ל
# 1K7:4	אֶל־מֶחֱזָ֖ה
# E28:5	וְאֶת־הַתְּכֵ֖לֶת
# L13:56	מִן־הַשְּׁתִ֖י
#
# והשווה עוד:
#
# Ec2:17	שֶׁנַּעֲשָׂ֖ה
# Ec1:3	שֶֽׁיַּעֲמֹ֖ל (FR3-disj-with-gtbs)
# Ec1:14	שֶֽׁנַּעֲשׂ֖וּ (FR3-disj-with-gtbs)
# Ec9:6	אֲשֶֽׁר־נַעֲשָׂ֖ה (FR3-disj-with-gtbs)
#
# מבין התיבות שבאה בהן געיה, כדיך, יש חילוף על:
#
# N16:28	כׇּל־הַֽמַּעֲשִׂ֖ים
#
# על:
#
# Ee23:36	אֶֽת־אׇהֳלָ֖ה
#
# יש הסכמה בלי געיה.
#
# ב-2 דוגמות מועדפת געית-שוא מן הגעיה הכבדה (יד.8).
