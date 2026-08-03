"""Exports RECORDS."""

from mb_cmn.he_wikisource_url import he_diff_url


def _mam_diff_url(title: str, diff: int, oldid: int) -> str:
    return he_diff_url(title, diff, oldid)


_MAM_STATUS_CNN_ALREADY_DONE = (
    "Change not needed since change already made on Wikisource."
)
_MAM_STATUS_CNN_FIXED_LONG_AGO = "Change not needed since MAM already fixed this or never had this problem to begin with."
_MAM_STATUS_CNN_NO_METEG = (
    "Change not needed since MAM has no meteg at all on this word."
)
_MAM_STATUS_CNN_MACRO_NOT_AT_ISSUE = (
    "Change not needed since MAM’s corresponding word discards UXLC meteg micro-placement, "
    "and the macro-placement is not at issue here. "
    "I.e. MAM does not preseve the earliness of the meteg, "
    "and which letter it belongs to is not at issue here."
)
_MAM_STATUS_CNN_AC_AGREES = (
    "Change not needed since MAM’s meteg placement agrees with AC."
)
_MAM_STATUS_CNN_OTHER_MSS = (
    "Change not needed since all of the many other manuscripts Avi consulted "
    "reject the idea of a meteg on the first letter. "
    "I.e. they reject the idea of a heavy gaʿya."
)
_MAM_STATUS_CHANGE_MAY_BE_NEEDED = (
    "Change may be needed since MAM’s corresponding word retains UXLC’s meteg macro-placement. "
    "I.e. MAM does not preseve the earliness of the meteg but it does preserve which letter it belongs to."
)
_UNCLEAR = "Unclear from the LC image alone whether this is an early meteg."
_PERHAPS_BETTER_1 = "Perhaps better transcribed as a normal meteg on the first letter."
_BETTER_1 = "Better transcribed as a normal meteg on the first letter."
_BETTER_2 = "Better transcribed as a normal meteg on letter 2."

_RECORD_01 = {
    "word": "וּמֽ͏ַעֲשֵׂ֔ה",
    "uxlc_bcvp": ("1Chr", 23, 28, 17),
    "img": "1Chr23v28.png",
}
_RECORD_02 = {
    "word": "וְנֽ͏ֶחֱלֵ֙יתִי֙",
    "uxlc_bcvp": ("Dan", 8, 27, 4),
    "img": "Dan8v27.png",
}
_RECORD_03 = {
    "word": "הַמּֽ͏ַאֲכִ֨לְךָ֥",
    "uxlc_bcvp": ("Deut", 8, 16, 1),
    "img": "Deut8v16.png",
}
_RECORD_04 = {
    "word": "מִמּֽ͏ַעֲלֵ֣י",
    "uxlc_bcvp": ("Deut", 14, 7, 6),
    "img": "Deut14v7.png",
}
_RECORD_05 = {
    "word": "וְהֽ͏ַעֲבַטְתָּ֞",
    "uxlc_bcvp": ("Deut", 15, 6, 8),
    "img": "Deut15v6.png",
}
_RECORD_06 = {
    "word": "עֲבֽ͏ָדְךָ֖",
    "uxlc_bcvp": ("Deut", 15, 18, 12),
    "img": "Deut15v18.png",
}
_RECORD_07 = {
    "word": "דְּגֽ͏ָנְךָ֜",
    "uxlc_bcvp": ("Deut", 18, 4, 2),
    "img": "Deut18v4.png",
}
_RECORD_08 = {
    "word": "וּפֽ͏ָרְשׂוּ֙",
    "uxlc_bcvp": ("Deut", 22, 17, 14),
    "img": "Deut22v17.png",
}
_RECORD_09 = {
    "word": "וְקֽ͏ָרְבָה֙",
    "uxlc_bcvp": ("Deut", 25, 11, 7),
    "imgs": {
        "LC": "Deut25v11.png",
        "Sassoon 1053": "Deut25v11-Sassoon-1053-page-179-col-2-line-17.png",
    },
    "initial-remark": "Ḥiriq-pataḥ would be the strict transcription (vs. sheva-qamats).",
    "further-remarks": [
        "Seems like there was an erasure under the vav. "
        "IMO the evidence of a qamats dot is too faint to justify transcribing it.",
        "Sassoon 1053 has sheva and qamats, with no meteg in sight.",
    ],
}
_RECORD_10 = {
    "word": "וְלֽ͏ָאַלְמָנָ֔ה",
    "uxlc_bcvp": ("Deut", 26, 12, 16),
    "img": "Deut26v12.png",
}
_RECORD_11 = {
    "word": "יְקֽ͏ִימְךָ֨",
    "uxlc_bcvp": ("Deut", 28, 9, 1),
    "img": "Deut28v9.png",
}
_RECORD_12 = {
    "word": "וְדֽ͏ַאֲב֥וֹן",
    "uxlc_bcvp": ("Deut", 28, 65, 18),
    "img": "Deut28v65.png",
}
_RECORD_13 = {
    "word": "וַיּֽ͏ַהַרְג֣וּ",
    "uxlc_bcvp": ("Esth", 9, 15, 11),
    "img": "Esth9v15.png",
}
_RECORD_14 = {
    "word": "וְאֽ͏ַהֲרֹ֔ן",
    "uxlc_bcvp": ("Ex", 7, 7, 5),
    "img": "Ex7v7.png",
}
_RECORD_15 = {
    "word123p": ("וַ", "יּֽ͏ַ", "עֲשׂ֖וּ"),
    "word": "וַיּֽ͏ַעֲשׂ֖וּ",
    "uxlc_bcvp": ("Ex", 12, 50, 1),
    "imgs": {
        "LC": "Ex12v50.png",
        "BHS": "Ex12v50-ויעשו-in-BHS.jpg",
    },
    "dubious early mtg": _BETTER_1,
    "initial-remark": "See UXLC change proposal 2024.01.29-4.",
    "existing UXLC change proposal": ("2024.04.01", "2024.01.29-4"),
    "MAM-word": "וַֽיַּעֲשׂ֖וּ",
    "MAM-status": _MAM_STATUS_CNN_ALREADY_DONE,
    "MAM-diff-URL": _mam_diff_url("שמות_יב/טעמים", 2839217, 2815126),
}
_RECORD_16 = {
    "word123p": ("וַ", "יּֽ͏ַ", "עֲשׂוּ־"),
    "word": "וַיּֽ͏ַעֲשׂוּ־",
    "uxlc_bcvp": ("Ex", 14, 4, 16),
    "img": "Ex14v4.png",
    "dubious early mtg": _UNCLEAR,
    "MAM-word": "וַיַּֽעֲשׂוּ־",
    "MAM-status": _MAM_STATUS_CNN_OTHER_MSS,
}
_RECORD_17 = {
    "word123p": ("וַ", "יּֽ͏ַ", "עֲמֹ֖ד"),
    "word": "וַיּֽ͏ַעֲמֹ֖ד",
    "uxlc_bcvp": ("Ex", 14, 19, 14),
    "line": 18,
    "img": "17-Ex14v19a14.png",
    "dubious early mtg": _BETTER_1,
    "initial-remark": "The first two pataḥ marks are shifted “late”.",
    "further-remarks": [
        "Despite this shift, if we assume that the meteg tracks with this shift, "
        "the vav rather than the yod “owns” the meteg."
    ],
    "MAM-word": "וַיַּֽעֲמֹ֖ד",
    "MAM-status": _MAM_STATUS_CHANGE_MAY_BE_NEEDED,
}
_RECORD_18 = {
    "word123p": ("וַ", "יּֽ͏ַ", "אֲמִ֙ינוּ֙"),
    "word": "וַיּֽ͏ַאֲמִ֙ינוּ֙",
    "uxlc_bcvp": ("Ex", 14, 31, 14),
    "line": 5,
    "img": "18-Ex14v31a14.png",
    "dubious early mtg": _BETTER_1,
    "MAM-word": "וַיַּֽאֲמִ֙ינוּ֙",
    "MAM-status": _MAM_STATUS_CHANGE_MAY_BE_NEEDED,
}
_RECORD_19 = {
    "word": "וְהֽ͏ַאֲזַנְתָּ֙",
    "uxlc_bcvp": ("Ex", 15, 26, 11),
    "img": "Ex15v26a11.png",
}
_RECORD_20 = {
    "word": "הַמּֽ͏ַחֲלָ֞ה",
    "uxlc_bcvp": ("Ex", 15, 26, 17),
    "img": "Ex15v26a17.png",
}
_RECORD_21 = {
    "word": "וַיּֽ͏ַעַמְד֖וּ",
    "uxlc_bcvp": ("Ex", 20, 18, 17),
    "img": "Ex20v18.png",
}
_RECORD_22 = {
    "word123p": ("וַ", "יּֽ͏ַ", "עֲל֖וּ"),
    "word": "וַיּֽ͏ַעֲל֖וּ",
    "uxlc_bcvp": ("Ex", 24, 5, 6),
    "img": "Ex24v5.png",
    "dubious early mtg": _BETTER_1,
    "initial-remark": "See UXLC change proposal 2024.01.29-3.",
    "existing UXLC change proposal": ("2024.04.01", "2024.01.29-3"),
    "MAM-word": "וַֽיַּעֲל֖וּ",
    "MAM-status": _MAM_STATUS_CNN_ALREADY_DONE,
    "MAM-diff-URL": _mam_diff_url("שמות_כד/טעמים", 2838019, 2837894),
}
_RECORD_23 = {
    "word123p": ("בְּ", "נֽ͏ֵ", "י־"),
    "word": "בְּנֽ͏ֵי־",
    "uxlc_bcvp": ("Ex", 30, 12, 5),
    "img": "Ex30v12.png",
    "dubious early mtg": _BETTER_2,
    "initial-remark": "L has a normal meteg on the 2nd letter (nun).",
    "further-remarks": [
        "BHS agrees with L so this seems like purely a WLC transcription error.",
        "An almost identical error appears in @בְּנֽ͏ֵי־# in UXLC Ex 35:20.",
    ],
    "MAM-word": "בְּנֵֽי־",
    "MAM-status": _MAM_STATUS_CNN_MACRO_NOT_AT_ISSUE,
}
_RECORD_24 = {
    "word123p": ("בְּ", "נֽ͏ֵ", "י־"),
    "word": "בְּנֽ͏ֵי־",
    "uxlc_bcvp": ("Ex", 35, 20, 4),
    "img": "Ex35v20.png",
    "dubious early mtg": _BETTER_2,
    "initial-remark": "L has a normal meteg on the 2nd letter (nun).",
    "further-remarks": [
        "BHS agrees with L so this seems like purely a WLC transcription error.",
        "An almost identical error appears in @בְּנֽ͏ֵי־# in UXLC Ex 30:12.",
    ],
    "MAM-word": "בְּנֵֽי־",
    "MAM-status": _MAM_STATUS_CNN_MACRO_NOT_AT_ISSUE,
}
_RECORD_25 = {
    "word123p": ("וְ", "לֽ͏ָ", "קַחְתָּ֣"),
    "word": "וְלֽ͏ָקַחְתָּ֣",
    "uxlc_bcvp": ("Ezek", 5, 2, 9),
    "line": 16,
    "img": "25-Ezek5v2.png",
    "dubious early mtg": _PERHAPS_BETTER_1,
    "initial-remark": "The sheva has an additional dot below it, but we ignore that dot.",
    "MAM-word": "וְלָקַחְתָּ֣",
    "MAM-status": _MAM_STATUS_CNN_NO_METEG,
}
_RECORD_26 = {
    "word": "וְאֽ͏ֵלַמָּ֔יו",
    "uxlc_bcvp": ("Ezek", 40, 36, 3),
    "wq": "q",
    "line": 9,
    "img": "26-Ezek40v36.png",
}
_RECORD_27 = {
    "word": "וַיּֽ͏ַעֲשׂוּ־",
    "uxlc_bcvp": ("Ezra", 10, 16, 1),
    "line": 3,
    "img": "Ezra10v16.png",
}
_RECORD_28 = {
    "word": "לְהֽ͏ַחֲיֽוֹת׃",
    "uxlc_bcvp": ("Gen", 6, 20, 14),
    "line": 6,
    "img": "Gen6v20.png",
}
_RECORD_29 = {
    "word": "בְּעֽ͏ַנְנִ֥י",
    "uxlc_bcvp": ("Gen", 9, 14, 2),
    "img": "Gen9v14.png",
}
_RECORD_30 = {
    "word": "וְהֽ͏ַכְּנַעֲנִ֖י",
    "uxlc_bcvp": ("Gen", 12, 6, 10),
    "img": "Gen12v6.png",
}
_RECORD_31 = {
    "word": "וְאֽ͏ֶעֱשֶׂ֨ה",
    "uxlc_bcvp": ("Gen", 27, 9, 12),
    "line": 5,
    "img": "Gen27v9.png",
}
_RECORD_32 = {
    "word": "וַיּֽ͏ַעֲל֨וּ",
    "uxlc_bcvp": ("Gen", 50, 7, 6),
    "img": "Gen50v7.png",
}
_RECORD_33 = {
    "word": "וְהֽ͏ַחֲזָקָ֗ה",
    "uxlc_bcvp": ("Isa", 27, 1, 8),
    "line": 20,
    "img": "Isa27v1.png",
}
_RECORD_34 = {
    "word": "בְּרֽ͏ָע׃",
    "uxlc_bcvp": ("Isa", 33, 15, 19),
    "line": 19,
    "img": "Isa33v15.png",
}
_RECORD_35 = {
    "word123p": ("וְ", "קֽ͏ָ", "רָאתָ֩"),
    "word": "וְקֽ͏ָרָאתָ֩",
    "uxlc_bcvp": ("Jer", 3, 12, 2),
    "img": "Jer3v12.png",
    "dubious early mtg": _UNCLEAR,
    "initial-remark": "MAM notes with surprise that Mechon Mamre has meteg on qof.",
    "further-remarks": ["MAM’s note is ממ!=@וְקָֽרָאתָ֩#"],
    "MAM-word": "וְֽקָרָ֩אתָ֩",
    "MAM-status": _MAM_STATUS_CNN_FIXED_LONG_AGO,
}
_RECORD_36 = {
    "word": "הַמּֽ͏ַעֲשִׂ֥ים",
    "uxlc_bcvp": ("Jer", 7, 13, 6),
    "img": "Jer7v13.png",
}
_RECORD_37 = {
    "word": "וְ֝אֽ͏ַחֲוָתִ֗י",
    "uxlc_bcvp": ("Job", 13, 17, 4),
    "img": "Job13v17.png",
}
_RECORD_38 = {
    "word": "הַקּֽ͏ִיקָי֖וֹן",
    "uxlc_bcvp": ("Jon", 4, 6, 18),
    "img": "Jon4v6.png",
}
_RECORD_39 = {
    "word": "בֶּחֽ͏ָרָבָ֛ה",
    "uxlc_bcvp": ("Josh", 3, 17, 7),
    "img": "Josh3v17.png",
}
_RECORD_40 = {
    "word": "וְהֽ͏ַמְאַסֵּ֗ף",
    "uxlc_bcvp": ("Josh", 6, 13, 17),
    "img": "Josh6v13.png",
}
_RECORD_41 = {
    "word": "הָאֽ͏ָהֳלִ֖י",
    "uxlc_bcvp": ("Josh", 7, 21, 22),
    "img": "Josh7v21.png",
}
_RECORD_42 = {
    "word": "וְאֽ͏ַחֲרֵי־",
    "uxlc_bcvp": ("Josh", 8, 34, 1),
    "line": 6,
    "img": "Josh8v34.png",
}
_RECORD_43 = {
    "word": "וְנֽ͏ַהֲלָל֙",
    "uxlc_bcvp": ("Josh", 19, 15, 2),
    "line": 25,
    "img": "Josh19v15.png",
}
_RECORD_44 = {
    "word": "וְהֽ͏ַחִתִּי֙",
    "uxlc_bcvp": ("Josh", 24, 11, 14),
    "line": 11,
    "img": "Josh24v11.png",
}
_RECORD_45 = {
    "word": "וַיּֽ͏ַחֲנ֖וּ",
    "uxlc_bcvp": ("Judg", 20, 19, 5),
    "img": "Judg20v19.png",
}
_RECORD_46 = {
    "word": "וַיּֽ͏ֶחֶרְדוּ֙",
    "uxlc_bcvp": ("1Kings", 1, 49, 1),
    "img": "1Kings1v49.png",
}
_RECORD_47 = {
    "word": "לְהֽ͏ַחֲרִימָ֑ם",
    "uxlc_bcvp": ("1Kings", 9, 21, 11),
    "img": "1Kings9v21.png",
}
_RECORD_48 = {
    "word": "וַיּֽ͏ַאֲבֶל־",
    "uxlc_bcvp": ("Lam", 2, 8, 13),
    "img": "Lam2v8.png",
}
_RECORD_49 = {
    "word": "וְהֽ͏ַעֲבַרְתָּ֞",
    "uxlc_bcvp": ("Lev", 25, 9, 1),
    "img": "Lev25v9.png",
}
_RECORD_50 = {
    "word": "וְהֽ͏ֶעֱמִ֥יד",
    "uxlc_bcvp": ("Lev", 27, 11, 11),
    "img": "Lev27v11.png",
}
_RECORD_51 = {
    "word123p": ("וְ", "הֽ͏ַ", "עֲמַדְתָּ֣"),
    "word": "וְהֽ͏ַעֲמַדְתָּ֣",
    "uxlc_bcvp": ("Num", 3, 6, 5),
    "img": "Num3v6.png",
    "dubious early mtg": _UNCLEAR,
    "initial-remark": "MAM notes the uncertainty of the ownership of this meteg in L.",
    "MAM-word": "וְהַעֲמַדְתָּ֣",
    "MAM-status": _MAM_STATUS_CNN_NO_METEG,
}
_RECORD_52 = {
    "word": "לְטֽ͏ַהֲרָ֔ם",
    "uxlc_bcvp": ("Num", 8, 7, 4),
    "img": "Num8v7.png",
}
_RECORD_53 = {
    "word": "וְהֽ͏ַחֲרַמְתִּ֖י",
    "uxlc_bcvp": ("Num", 21, 2, 13),
    "img": "Num21v2.png",
}
_RECORD_54 = {
    "word": "וְהֽ͏ֶאֱבִ֥יד",
    "uxlc_bcvp": ("Num", 24, 19, 3),
    "img": "Num24v19.png",
}
_RECORD_55 = {
    "word": "וְהֽ͏ַעֲמַדְתָּ֣",
    "uxlc_bcvp": ("Num", 27, 19, 1),
    "img": "Num27v19.png",
}
_RECORD_56 = {
    "word": "תֵדֽ͏ָע׃",
    "uxlc_bcvp": ("Prov", 5, 6, 8),
    "img": "Prov5v6.png",
}
_RECORD_57 = {
    "word": "אֱוֽ͏ִיל׃",
    "uxlc_bcvp": ("Prov", 7, 22, 11),
    "img": "Prov7v22.png",
}
_RECORD_58 = {
    "word": "צַדּֽ͏ִיק׃",
    "uxlc_bcvp": ("Prov", 14, 32, 6),
    "img": "Prov14v32.png",
}
_RECORD_59 = {
    "word": "צָרֽ͏ָה׃",
    "uxlc_bcvp": ("Prov", 25, 19, 8),
    "img": "Prov25v19.png",
}
_RECORD_60 = {
    "word": "צַדּֽ͏ִיק׃",
    "uxlc_bcvp": ("Ps", 7, 10, 11),
    "img": "Ps7v10.png",
}
_RECORD_61 = {
    "word": "עָלֽ͏ָי׃",
    "uxlc_bcvp": ("Ps", 16, 6, 8),
    "img": "Ps16v6.png",
}
_RECORD_62 = {
    "word123p": ("וַ֭", "יּֽ͏ַ", "עֲבֹר"),
    "word": "וַ֭יּֽ͏ַעֲבֹר",
    "uxlc_bcvp": ("Ps", 37, 36, 1),
    "img": "Ps37v36.png",
    "dubious early mtg": _PERHAPS_BETTER_1,
    "MAM-word": "וַֽ֭יַּעֲבֹר",
    "MAM-status": _MAM_STATUS_CNN_FIXED_LONG_AGO,
}
_RECORD_63 = {
    "word": "פָּ֤קֽ͏ַדְתָּ",
    "uxlc_bcvp": ("Ps", 65, 10, 1),
    "img": "Ps65v10.png",
}
_RECORD_64 = {
    "word123p": ("וַ֭", "יּֽ͏ַ", "דְרִיכֵם"),
    "word": "וַ֭יּֽ͏ַדְרִיכֵם",
    "uxlc_bcvp": ("Ps", 107, 7, 1),
    "img": "Ps107v7.png",
    "dubious early mtg": _PERHAPS_BETTER_1,
    "MAM-word": "וַֽ֭יַּדְרִיכֵם",
    "MAM-status": _MAM_STATUS_CNN_FIXED_LONG_AGO,
}
_RECORD_65 = {
    "word": "עָלֽ͏ָי׃",
    "uxlc_bcvp": ("Ps", 142, 8, 12),
    "img": "Ps142v8.png",
}
_RECORD_66 = {
    "word": "וַיּֽ͏ִזְכְּרֶ֖הָ",
    "uxlc_bcvp": ("1Sam", 1, 19, 16),
    "img": "1Sam1v19.png",
}
_RECORD_67 = {
    "word": "הַמְאֽ͏ָרֲרִים֙",
    "uxlc_bcvp": ("Num", 5, 27, 13),
    "img": "Num5v27.png",
}
_RECORD_68 = {
    "word": "וַיִּמּֽ͏ָסְרוּ֙",
    "uxlc_bcvp": ("Num", 31, 5, 1),
    "img": "Num31v5.png",
}
_RECORD_69 = {
    "word": "וּנְתֽ͏ָנְךָ֨",
    "uxlc_bcvp": ("Deut", 28, 13, 1),
    "img": "Deut28v13.png",
}
_RECORD_70 = {
    "word": "הִשְׁתּֽ͏ַעַשְׁע֖וּ",
    "uxlc_bcvp": ("Isa", 29, 9, 3),
    "img": "Isa29v9.png",
}
_RECORD_71 = {
    "word": "קִנְאֽ͏ָתְךָ֙",
    "uxlc_bcvp": ("Isa", 63, 15, 8),
    "img": "Isa63v15.png",
}
_RECORD_72 = {
    "word123p": (
        "בַּצָּ",
        "רֽ͏ָ",
        "ה׃",
    ),
    "word": "בַּצָּרֽ͏ָה׃",
    "uxlc_bcvp": ("Ps", 10, 1, 7),
    "imgs": {
        "LC": "Ps10v1.png",
        "AC": "Ps10v1-AC.png",
    },
    "dubious early mtg": _UNCLEAR,
    "MAM-word": "בַּצָּרָֽה׃",
    "MAM-status": _MAM_STATUS_CNN_AC_AGREES,
}
_RECORD_73 = {
    "word": "רַגְלֽ͏ָיו׃",
    "uxlc_bcvp": ("Ps", 18, 10, 6),
    "img": "Ps18v10.png",
}
_RECORD_74 = {
    "word123p": (
        "עֲנָ",
        "וֽ͏ָ",
        "ה׃",
    ),
    "word": "עֲנָוֽ͏ָה׃",
    "uxlc_bcvp": ("Prov", 18, 12, 8),
    "imgs": {
        "LC": "Prov18v12.png",
        "AC": "Prov18v12-AC.png",
    },
    "dubious early mtg": _UNCLEAR,
    "MAM-word": "עֲנָוָֽה׃",
    "MAM-status": _MAM_STATUS_CNN_AC_AGREES,
}
_RECORD_75 = {
    "word": "מַלְוֽ͏ֶה׃",
    "uxlc_bcvp": ("Prov", 22, 7, 7),
    "img": "Prov22v7.png",
}
_RECORD_76 = {"word": "יַעֲלֽ͏ֶה׃", "uxlc_bcvp": ("Job", 7, 9, 8), "img": "Job7v9.png"}
_RECORD_77 = {
    "word": "הִֽתְהֽ͏ַלְלוּ֙",
    "uxlc_bcvp": ("1Chr", 16, 10, 1),
    "img": "1Chr16v10.png",
}

RECORDS = [
    _RECORD_01,
    _RECORD_02,
    _RECORD_03,
    _RECORD_04,
    _RECORD_05,
    _RECORD_06,
    _RECORD_07,
    _RECORD_08,
    _RECORD_09,
    _RECORD_10,
    _RECORD_11,
    _RECORD_12,
    _RECORD_13,
    _RECORD_14,
    _RECORD_15,
    _RECORD_16,
    _RECORD_17,
    _RECORD_18,
    _RECORD_19,
    _RECORD_20,
    _RECORD_21,
    _RECORD_22,
    _RECORD_23,
    _RECORD_24,
    _RECORD_25,
    _RECORD_26,
    _RECORD_27,
    _RECORD_28,
    _RECORD_29,
    _RECORD_30,
    _RECORD_31,
    _RECORD_32,
    _RECORD_33,
    _RECORD_34,
    _RECORD_35,
    _RECORD_36,
    _RECORD_37,
    _RECORD_38,
    _RECORD_39,
    _RECORD_40,
    _RECORD_41,
    _RECORD_42,
    _RECORD_43,
    _RECORD_44,
    _RECORD_45,
    _RECORD_46,
    _RECORD_47,
    _RECORD_48,
    _RECORD_49,
    _RECORD_50,
    _RECORD_51,
    _RECORD_52,
    _RECORD_53,
    _RECORD_54,
    _RECORD_55,
    _RECORD_56,
    _RECORD_57,
    _RECORD_58,
    _RECORD_59,
    _RECORD_60,
    _RECORD_61,
    _RECORD_62,
    _RECORD_63,
    _RECORD_64,
    _RECORD_65,
    _RECORD_66,
    _RECORD_67,
    _RECORD_68,
    _RECORD_69,
    _RECORD_70,
    _RECORD_71,
    _RECORD_72,
    _RECORD_73,
    _RECORD_74,
    _RECORD_75,
    _RECORD_76,
    _RECORD_77,
]
