from author_boj_util import author
from author_boj_util.uxlc_change import uxlc_change

_COMPAR1 = [
    "Whereas usually we just baldly and boldly state",
    " what (we think) the consensus is,",
    " here we will try to explain why the transcription’s divergence from consensus",
    " seems so unlikely to reflect the scribal intent.",
]
_PS118 = ["$Ps_118_5 ", author.hbo("הַ֭מֵּצַ֥ר")]
_COMPAR2 = [
    ["In $BHS, a דחי followed by מרכא is probably found only here"],
    [" and in the following three cases:"],
    [" $Ps_86_7 ", author.hbo("צָ֭רָתִ֥י"), ","],
    [" ", *_PS118, ", and"],
    [" $Ps_139_7 ", author.hbo("אָ֭נָ֥ה"), "."],
    [" In those three cases, there is little question about the דחי:"],
    [" the question is only whether the second mark is מרכא or געיה."],
    [" (In the ", *_PS118, " case, there is also a question of"],
    [" whether there should be a second mark at all.)"],
]
_COMPAR3 = [
    ["In contrast, here in $plain_10_6 the דחי is highly questionable"],
    [" because it follows an אתנח,"],
    [" a sequence unprecedented in the consensus"],
    [" and rare even in $BHS, where it is probably found in only two other cases:"],
    [" $Ps_115_3 ", author.hbo("כֹּ֭ל אֲשֶׁר־חָפֵ֣ץ עָשָֽׂה׃"), " and"],
    [" $Ps_119_16 ", author.hbo("לֹ֭א אֶשְׁכַּ֣ח דְּבָרֶֽךָ׃"), "."],
    [" In both of those two cases, טרחא is a better transcription of μL."],
]
_COMPAR4 = [
    ["After אתנח, the consensus sequence here in $plain_10_6 is מרכא and then סילוק:"],
    [" ", author.hbo("וּֽלְחַטָּאתִ֥י תִדְרֽוֹשׁ׃"), "."],
    [" After אתנח, this sequence is found about 194 times in poetic verses,"],
    [" about 38 of which are in Job,"],
    [" e.g. $plain_6_12 ", author.hbo("אִֽם־בְּשָׂרִ֥י נָחֽוּשׁ׃"), ","],
    [" $plain_7_14 ", author.hbo("וּֽמֵחֶזְיֹנ֥וֹת תְּבַעֲתַֽנִּי׃"), ", and"],
    [" $plain_8_11 ", author.hbo("יִשְׂגֶּה־אָ֥חוּ בְלִי־מָֽיִם׃"), "."],
]
_COMPAR5 = [
    "This mark was probably transcribed as a דחי",
    " ignoring context, using only",
    " the mark’s position relative to its letter (early) and",
    " its inclination (twisted somewhat counterclockwise from vertical).",
    " Although in an ideal world we could transcribe using only such criteria,",
    " in practice we must transcribe more charitably, considering context as well.",
    " The relevant context includes both the consensus pointing",
    " and the likelihood of the non-consensus (quirky) pointing under consideration.",
    " Here, a transcription of געיה seems best given that",
    " the consensus is געיה and",
    " דחי seems very unlikely.",
]
# Found 3 verses where ETNAHTA (֑ U+0591) is followed by DEHI (֭ U+05AD):

# Ps 115:3 — וֵֽאלֹהֵ֥ינוּ בַשָּׁמָ֑יִם כֹּ֭ל אֲשֶׁר־חָפֵ֣ץ עָשָֽׂה׃
# Ps 119:16 — בְּחֻקֹּתֶ֥יךָ אֶֽשְׁתַּעֲשָׁ֑ע לֹ֭א אֶשְׁכַּ֣ח דְּבָרֶֽךָ׃
# Job 10:6 — כִּֽי־תְבַקֵּ֥שׁ לַעֲוֺנִ֑י וּ֭לְחַטָּאתִ֥י תִדְרֽוֹשׁ׃
RECORD_1006 = {
    "qr-cv": "10:6",
    "qr-lc-proposed": "וּ֭לְחַטָּאתִ֥י",
    "qr-what-is-weird": "דחי not געיה",
    "qr-consensus": "וּֽלְחַטָּאתִ֥י",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "400A", "column": 1, "line": 2},
    "qr-ac-loc": {"page": "272v", "column": 2, "line": 13, "word": 4},
    "qr-generic-comment": [
        author.para(_COMPAR1),
        author.para(_COMPAR2),
        author.para(_COMPAR3),
        author.para(_COMPAR4),
        author.para(_COMPAR5),
    ],
    "qr-noted-by": "tBHQ-zUXLC",
    "qr-uxlc-change-url": uxlc_change("2023.10.19", "2023.06.10-9"),
}
