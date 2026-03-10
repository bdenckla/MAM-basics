from pycmn import str_defs as sd
from pycmn import hebrew_letters as hl


def sec_yyy_qualifier(word) -> dict:
    raw_qual = _QUALIFIERS.get(word)
    return _sec_yyy_qualifier_2(raw_qual)


def servant_info(word):
    raw_qual = _QUALIFIERS.get(word)
    if isinstance(raw_qual, tuple) and len(raw_qual) == 4:
        return raw_qual[3]
    qual = _sec_yyy_qualifier_2(raw_qual)
    return _SERVANT_INFOS.get(qual["ref_1"]) or _SERVANT_INFOS.get(qual["ref_2"])


_BWD_3_FWD_2 = {"bwd-context": 3, "fwd-context": 2}
_BWD_1 = {"bwd-context": 1}
_FWD_1 = {"fwd-context": 1}
_FWD_2 = {"fwd-context": 2}
_FWD_3 = {"fwd-context": 3}
_SERVANT_INFOS = {
    "09.26.rn1": _FWD_3,
    "09.26.rn2": _FWD_2,
    "09.34.rn1": _FWD_2,
    "11.20.rn1": _FWD_1,
    "11.20.rn2": _FWD_1,
    "11.20.rn3": _FWD_1,
    "11.20.rn4": _FWD_1,
    "11.26.rn1": _FWD_1,
    "11.26.rn2": _FWD_1,
    "11.26.rn3": _FWD_1,
    "11.26.rn4": _FWD_1,
}


def _sec_yyy_qualifier_2(qualifier) -> dict:
    ref_1 = None
    ref_2 = None
    note = None
    if isinstance(qualifier, tuple) and len(qualifier) == 3:
        ref_1 = qualifier[0] and _format_breuer_cos_ref(qualifier[0], 9)
        ref_2 = qualifier[1] and _format_breuer_cos_ref(qualifier[1], 11)
        note = qualifier[2]
    elif isinstance(qualifier, tuple) and len(qualifier) == 4:
        return _sec_yyy_qualifier_2(qualifier[0:3])
    else:
        assert qualifier is None, "Unexpected type for qualifier"
    return {"ref_1": ref_1, "ref_2": ref_2, "note": note}


def _format_breuer_cos_ref(ref: str, expected_chapter: int) -> str:
    """Pad chapter and section numbers with leading zeros for proper sorting."""
    parts = ref.split(".")
    chapter = int(parts[0])
    assert (
        chapter == expected_chapter
    ), f"Unexpected chapter number {chapter} in Breuer/CoS ref {ref} (expected {expected_chapter})"
    new_parts = f"{chapter:02}", f"{int(parts[1]):02}", *parts[2:]
    return ".".join(new_parts)


def _only_cited(cited, not_cited, whom="CoS") -> str:
    return f"Only cited at {cited} by {whom} but also appears at {not_cited}"


def _alap(section) -> str:
    return f"Also appears in {section}"


def _rs(string: str) -> str:
    return string.replace("\n", " ").strip()


def _psq_join(word1: str, word2: str) -> str:
    return word1 + sd.NBSP + sd.DOUB_VERT_LINE + " " + word2


_SECONDARY = "2ndary"
_PRIM_CONJ = "primary (conjunctive)"
_MAH_NOT_SEC = f"The mah is {_PRIM_CONJ}, not {_SECONDARY}"
_MER_NOT_SEC = f"The mer is {_PRIM_CONJ}, not {_SECONDARY}"
_SRTM = "space rather than mqf"
_GAYA = "געיה"
_NO_REF = "I find no reference to this in CoS"
_N_PS_92_8 = f"""
{_alap('11.32.fn17')}, where Breuer calls μA's mqf "inexplicable."
CoS & JC have {_SRTM}.
μA has mqf; μL has space.
(Same situation as Ps12:6.)"""
_N_PS_12_6 = f"""
{_NO_REF}. JC has {_SRTM}. μA has mqf; μL has space. (Same situation as Ps92:8.)"""
_N_PS_65_5 = f"""
{_NO_REF}. Da-at Miqra considers μL to have {_GAYA} not mer; how/why?
(It considers μA to have mer)"""
_N_PS_89_20 = f"""
The reference I find in CoS (11.8) has {_SRTM},
presumably because CoS classifies this mer as {_PRIM_CONJ}, not {_SECONDARY}.
This would make its absence from 11.10 intentional.
Like CoS 11.8, JC has {_SRTM}. μA & μL have mqf."""
_N40_9 = f"""
Why doesn't CoS (1) have a mqf (2) mention μL's {_GAYA} on {hl.SHIN}?
{_alap("9.32 body text and 9.33.rn1")}."""
_MENTIONED_INDIRECTLY = """
Mentioned indirectly in 9.38.fn27.
By “indirectly” I mean via reference to 11.56."""
_AYIN_D_H = "עדה"
_JB_40_10 = f"""
{_rs(_MENTIONED_INDIRECTLY)}
CoS says that {_AYIN_D_H} should be considered to be followed by a mqf."""
_N_PS_66_15 = f"""
9.29 notes that μS1 has azla where μA & μL have {_GAYA} (the opposite of Ps89:46)."""
_N_PS_47_5 = f"""
{_alap("9.30")}, where it is noted that μS1 has {_GAYA} where μA & μL have azla (like Ps89:46)."""
_N_PS_89_46 = f"""
{_alap("9.29")}, where it is noted that μS1 has {_GAYA} where μA & μL have azla (the opposite of Ps66:15)."""
_N_PS_19_15 = f"The mer does not mobilize the shewa? CoS 11.3 has {_SRTM}."
_VOC_OR_AT_LEAST_NFS = "vocal (or at least, “not [...] fully silent” (!))"
_PHI_2 = "φ2 (footnote 2) is commentary by Denckla on ITM, not part of ITM"
_ONLY_1K_2_30 = _only_cited("1K2:30", "G18:15", "Yeivin")
_S79_CONFIRMS = f"11.79 confirms this mah to be {_SECONDARY}, not {_PRIM_CONJ}"
_EXP_VOC_FN_23 = "explicitly called vocal in 9.23.fn23"
_ONLY_CITED_40_9_ETC = _only_cited("40:9", "119:109 and 119:174")
_N46_4 = f"{_alap('9.33.rn1')}."
#
_QUALIFIERS_FOR_SEC_MISC = {
    "בָּ֤רֽוּךְ~יְהֹוָ֨ה": ("9.34.rn1", "11.8.b.rn3", None),  # Ps106:48
    "פָּ֤קַֽדְתָּ~הָאָ֨רֶץ": (None, "11.8.b.rn3", None, _FWD_1),  # Ps65:10
    "הֲתָ֤עִיף~עֵינֶ֥יךָ": ("9.34.rn1", "11.22", f"{_alap('11.17.rn2')}.", _FWD_1),  # Pr23:5
    #
    "יָ֤גֵ֥ל": ("9.24.rn1", "11.20.rn1", None),  # Ps13:6
    "ה֤וֹרֵ֥נִי": ("9.24.rn1", "11.20.rn1", None),  # Ps27:11
    "יָ֤בֹ֥א": ("9.24.rn1", "11.20.rn1", None),  # Ps50:3
    "וְיֹ֤שֵׁ֥ב": (None, "11.20.rn1", None),  # Ps55:20
    "נ֤וֹרָ֥א": (None, "11.20.rn1", None),  # Ps68:36
    "נ֤וֹדֶ֥ה": (None, "11.20.rn1", None),  # Ps79:13
    "ה֤וֹלֵ֥ךְ": (None, "11.20.rn1", None),  # Pr7:22
    #
    "נ֤וֹדַ֨ע׀": ("9.25.rn1", "11.6.rn1", None),  # Ps9:17
    "יֹ֤סֵ֨ר׀": ("9.25.rn1", "11.6.rn1", None),  # Pr9:7
    "אֹ֤מֵ֨ר׀": ("9.25.rn1", "11.6.rn1", None),  # Pr24:24
    #
    "וְלָ֤רָשָׁ֨ע׀": ("9.20", None, f"{_MAH_NOT_SEC}."),  # Ps50:16
    #
    "בָּ֤ר֣וּךְ": ("9.23.rn1", "11.26.rn1", None),  # Ps68:20
    "הָ֤אֵ֣ל" + sd.DOUB_VERT_LINE: ("9.23.rn1", "11.26.rn1", None),  # Ps68:21
    "תָּ֤ב֣וֹא": ("9.23.rn1", "11.26.rn1", None),  # Ps79:11
    "מִ֤י~ה֣וּא": ("9.27.rn1", "11.26.rn1", None),  # Ps24:10
    #
    "בִּ֘ישׁ֤וּעָתֶ֗ךָ": (None, "11.35.rn2", None),  # Ps20:6
    "נֶ֘חָ֤מָתִ֗י": (None, "11.35.rn2", None),  # Jb6:10
    #
    "שֶׁ֤אֵ֣ל": (None, "11.52", None, _FWD_2),  # Ps146:5
    #
    "לֹ֤א~אֵֽל־חָפֵ֘ץ~רֶ֥שַׁע" + sd.DOUB_VERT_LINE: (None, "11.54", None, _FWD_1),  # Ps5:5
    #
    "מָ֤ה~רַֽב־טוּבְךָ֮": ("9.31", None, None),  # Ps31:20
    #
    "שֶׁ֤אֵ֖ין": (
        None,
        "11.64.rn2",
        f"{_alap('11.78')}. {_MAH_NOT_SEC}.",
        _BWD_3_FWD_2,
    ),  # Ps146:3
    #
    "אָ֤דָֽם~וּבְהֵמָ֖ה": ("9.34.rn1", "11.66.rn1", f"{_S79_CONFIRMS}."),  # Ps36:7
    "מ֤וֹצָֽאֵי~בֹ֖קֶר": (None, "11.66.rn1", f"{_S79_CONFIRMS}."),  # Ps65:9
    "יָ֤אֵֽר~פָּנָ֖יו": (None, "11.66.rn1", f"{_S79_CONFIRMS}."),  # Ps67:2
    "תָּ֤כִֽין~בְּטוֹבָתְךָ֖": (None, "11.66.rn1", f"{_S79_CONFIRMS}."),  # Ps68:11
    "הָ֤יֽוּ~זְר֖וֹעַ": (None, "11.66.rn1", f"{_S79_CONFIRMS}."),  # Ps83:9
    "תָּ֤שִֽׁית~לִ֖י": (None, "11.66.rn1", f"{_S79_CONFIRMS}."),  # Jb14:13
    #
    "מֵ֤אִישׁ~מִרְמָ֖ה": (None, "11.66.rn2", f"{_S79_CONFIRMS}."),
    "א֤וֹדֶה~שִּׁמְךָ֖": (None, "11.66.rn2", f"{_S79_CONFIRMS}."),
    "מֵ֤אִיר~עֵינֵ֖י": (None, "11.66.rn2", f"{_S79_CONFIRMS}."),
    #
    "מֵ֖חַטָּאתִֽי׃": ("9.35.rn1", "11.80.rn1", None),  # Ps38:19
    "בְּֽמוֹעֲצ֖וֹתֵיהֶֽם׃": ("9.35.rn1", "11.80.rn1", f"CoS has no {_GAYA}"),  # Ps81:13
    "וּמִמַּ֖עֲמַקֵּי~מָֽיִם׃": ("9.36.rn1", "11.80.rn2", None),  # Ps69:15
    "יַ֖עַמְדוּ~מָֽיִם׃": ("9.36.rn1", "11.80.rn2", None),  # Ps104:6
    "וְיַ֖הַפְכוּ~אָֽרֶץ׃": ("9.36.rn1", "11.80.rn2", None),  # Jb12:15
}
_QUALIFIERS_FOR_SEC_MERK = {
    "אֶשְׁמְרָ֥ה~לְפִ֥י": (None, "11.47.es2.rn2", f"{_alap('11.47.fn27')}.", _FWD_1),  # Ps39:2
    "בְּנִ֥י~אַ֑תָּה": (None, "11.47.es2.rn1", f"{_alap('11.47.fn27')}.", _BWD_1),  # Ps2:7
    #
    "הֵ֥רַֽע לִֽי׃": (None, None, "ITM-354"),  # R1:21
    "וְנֹ֥גַֽהּ ל֖וֹ": (None, None, "ITM-354"),  # Ee1:27
    #
    _psq_join("וַיֹּ֥אמֶֽר", "לֹ֖א"): ("ITM-325", None, f"{_ONLY_1K_2_30}."),  # 1K2:30, G18:15
    _psq_join("וַיֹּ֥אמֶֽר", "לֹֽא׃"): ("ITM-325.φ2", None, _PHI_2),  # Ju12:5
    #
    "עֲבָדֶ֥יךָֽ אֵ֛לֶּה": (None, None, "ITM-332"),  # 2K1:13
    #
    "כְּמ֥וֹ־עֵ֗שֶׂב": (None, "11.32.rn3", _rs(_N_PS_92_8)),  # Ps92:8
    "הַ֥ט~אׇזְנְךָ֗": (None, "11.36.rn2", None),  # Pr22:17
    #
    "יָפִ֥יחַֽ־לֽוֹ׃": (None, None, _rs(_N_PS_12_6)),  # Ps12:6
    #
    "תִּ֥בְﬞחַ֣ר": (None, None, _rs(_N_PS_65_5)),  # Ps65:5
    #
    "דִּבַּ֥רְתָּֽ־בְחָז֡וֹן": (None, "11.8.a.es2.rn1", _rs(_N_PS_89_20)),  # Ps89:20
    #
    "תַּנְח֥וּמֹֽתֵיכֶֽם׃": (None, "11.80.rn3", f"CoS has no {_GAYA}"),  # Jb21:2
    # JC has a full-sized {_GAYA} here.
    # It is interesting that CoS DOES have {_GAYA} in עַד~תְּב֥וּנֹֽתֵיכֶ֑ם in 11.55.rn1 (Jb32:11).
    # It is interesting because he is clearly aware of the analogy between these words
    # since each of their footnotes (30 and 46) are cross-referenced,
    # i.e. each references the other.
    "בְּמַ֥עַלְלֵיהֶֽם׃": ("9.35.rn2", "11.80.rn3", None),  # Ps106:39
    #
    "יִ֥רְעֲשֽׁוּ~הָרִ֖ים": ("9.28.rn2", "11.79.rn2", _N46_4, _FWD_2),
    # Ps46:4
    "אֶ֥עֱשֶֽׂה~בָקָ֖ר": ("9.29.var-rn2", "11.79.rn2", _rs(_N_PS_66_15), _FWD_2),  # Ps66:15
    "אֶ֥ת~גְּא֨וֹן": ("9.27.rn4", "11.79.rn1", _rs(_N_PS_47_5), _FWD_3),  # Ps47:5
    "הֶ֥עֱטִ֨יתָ": ("9.26.rn1", "11.79.rn1", _rs(_N_PS_89_46)),  # Ps89:46
    "אֶ֥חֱסֶ֨ה": ("9.26.rn1", "11.79.rn1", f"{_alap('9.33.rn1')}."),  # Ps61:5
    #
    "מְקִ֥ימִ֣י": (None, "11.56.rn1", _rs(_MENTIONED_INDIRECTLY), _FWD_2),  # Ps113:7
    "עֲדֵ֥ה~נָ֣א": (None, "11.56.rn2", _rs(_JB_40_10), _FWD_2),  # Jb40:10
    #
    "מַ֥עַלְלֵי־אֵ֑ל": ("9.36.rn2", "11.55.rn2", f"{_alap('9.37')}.", _BWD_1),  # Ps78:7
    "עַד־תְּב֥וּנֹֽתֵיכֶ֑ם": (None, "11.55.rn1", None),  # Jb32:11
    "בְּמַ֥עַלְלֵיהֶ֑ם": ("9.35.rn2", "11.55.rn1", None),  # Ps106:29
    "נ֥וֹעֲד֑וּ": ("9.35.rn2", "11.55.rn1", None),  # Ps48:5
    #
    "לַ֥עֲשׂוֹת־רְצוֹנְךָ֣": ("9.28.rn2", "11.53", _rs(_N40_9), _FWD_2),  # Ps40:9
    "וֶ֥אֱֽמוּנָתִ֣י": ("9.32.rn2", "11.53", None, _FWD_2),  # Ps89:25
    "אֶ֥ת~אֲשֶׁ֣ר": ("9.27.rn4", "11.53", None, _FWD_3),  # Pr3:12
    #
    "וְאֶל־בִּ֥֝ינָתְךָ֗": (None, "11.40.es1.rn1", f"{_MER_NOT_SEC}."),  # Pr3:5
    "וּֽ֝מֵעֲוֺ֥נֹתֵיהֶ֗ם": (
        None,
        "11.40.es1.rn1",
        f"{_MER_NOT_SEC}. CoS has no {_GAYA}.",
    ),  # Ps107:17
    # I have verified that indeed Aleppo has {_GAYA} here.
    # https://www.mgketer.org/mikra/27/107/1/mg/106 column 2 line 1.
    # Leningrad agrees with Aleppo; 388B column 2 line 23.
    # This word was changed in UXLC: https://tanach.us/Changes/2023.07.04%20-%20Changes/2023.07.04%20-%20Changes.xml?2023.03.25-99
    # JC agrees with Aleppo here too, having a full-sized {_GAYA} here.
    "תּ֥֝וֹרָתְךָ֗": (None, "11.40.es2.rn1", None),  # Ps119:61
    "וּ֝בִישׁ֥וּעָתְךָ֗": (None, "11.40.es1.rn1", f"{_MER_NOT_SEC}."),  # Ps21:2
    "אֱ֝מ֥וּנָתְךָ֗": (
        "9.20",
        "11.40.es1.rn1",
        f"{_MER_NOT_SEC}. {_only_cited('36:6', '88:12')}.",
    ),
    "וְ֝ת֥וֹרָתְךָ֗": (None, "11.40.es1.rn1", f"{_MER_NOT_SEC}. {_ONLY_CITED_40_9_ETC}."),
    # "וֶ֝אֱמ֥וּנָתְךָ֗": None,  # Ps89:9
    # "וֶ֝אֱמ֥וּנָתְךָ֗": None,  # Ps92:3
    "מִ֝מְּצ֥וּקוֹתֵיהֶ֗ם": (None, "11.40.es2.rn1", None),  # Ps107:6 (es2: example set 2)
    # "מִ֝מְּצֻ֥קוֹתֵיהֶ֗ם": None,  # Ps107:13, 107:19
    # note that the word above is the same as Ps107:6 מִ֝מְּצ֥וּקוֹתֵיהֶ֗ם modulo a malei/haser
    # difference (shuruq vs qubuts).
    "בֵּ֝רַ֥כְנוּכֶ֗ם": (None, "11.41", _MER_NOT_SEC),  # Ps118:26
    "תְּ֝שׁ֥וּעָתְךָ֗": (None, "11.40.es1.rn1", f"{_MER_NOT_SEC}."),  # Ps119:41
    # "מִ֝תּ֥וֹרָתְךָ֗": None,  # Ps119:51
    "וְ֝אֵ֥מָתְךָ֗": (None, "11.40.es2.rn1", None),  # Jb13:21
    "וּ֝תְשׁ֥וּבֹתֵיכֶ֗ם": (None, "11.40.es1.rn1", f"{_MER_NOT_SEC}."),  # Jb21:34
    #
    "בַּ֥מִּדְבָּ֗ר": (None, "11.36.rn1", None),  # Jb24:5
    #
    "לְשֹׁ֥דְﬞדִ֗ים": (None, "11.35.rn1", None),  # Jb12:6
    #
    "אַ֥שְֽׁרֵי~הָאִ֗ישׁ": ("9.34.rn2", "11.28.rn2", None),  # Ps1:1
    "אַ֥שְֽׁרֵי~אָדָ֗ם": (None, "11.28.rn2", None),  # Ps32:2
    "אַ֥שְֽׁרֵי~הַגֶּ֗בֶר": (None, "11.28.rn2", None),  # Ps40:5
    "יַ֥חְפְּֽשׂוּ~עוֹלֹ֗ת": (None, "11.28.rn2", None),  # Ps64:7
    "לִ֥פְֽנֵי~יְהֹוָ֗ה": (None, "11.28.rn2", None),  # Ps98:9
    "נִ֥בְﬞהָֽל~לַה֗וֹן": (None, "11.28.rn2", None),  # Pr28:22
    #
    "וֶ֥אֱֽמוּנָתוֹ֮": ("9.32.rn1", "11.27.rn3", None),  # Ps98:3
    "אַ֥שְֽׁרֵי~אָדָם֮": ("9.28.rn1", "11.27.rn2", f"{_alap('9.33.rn1')}."),
    # Pr8:34
    #
    "אִ֥מְﬞר֣וֹת": ("9.23.rn2", "11.26.rn4", f"{_alap('9.33.rn2')}."),  # Ps12:7
    "אֶ֥קְﬞרָ֣א": ("9.23.rn2", "11.26.rn4", None),  # Ps18:7
    "לִ֥שְׁא֣וֹל": ("9.23.fn23", "11.26.rn4", "חטף חולם"),  # Ps49:15
    "נִ֥דְﬞר֣וּ": (None, "11.26.rn4", None),  # Ps76:12
    "שׇׁ֥מְרָ֣ה": ("9.23.fn23", "11.26.rn4", _VOC_OR_AT_LEAST_NFS),  # Ps86:2
    "תִּ֥לְﬞעַ֣ג": (None, "11.26.rn4", None),  # Pr30:17
    "אֶ֥בְﬞחַ֣ר": (None, "11.26.rn4", None),  # Jb29:25
    #
    "פָּ֥תְח֣וּ": ("9.23.rn2", "11.26.rn3", None),  # Ps37:14
    "תְּה֥וֹתְﬞת֣וּ": (None, "11.26.rn3", None),  # Ps62:4
    "יָ֥עֲצ֣וּ": (None, "11.26.rn3", None),  # Ps62:5
    "שָׁ֥נְﬞנ֣וּ": (None, "11.26.rn3", None),  # Ps140:4
    "שָׂ֥חֲק֣וּ": (None, "11.26.rn3", None),  # Jb30:1
    "לַ֥עֲשׂ֣וֹת": (None, "11.26.rn3", None),  # Ps143:10
    "אֶ֥שְׁמְרָ֣ה": (None, "11.26.rn3", None),  # Ps39:2
    "אֶ֥ת~אֲרַ֣ם": ("9.27.rn1", "11.26.rn3", None),  # Ps60:2
    #
    "תַּ֥עֲלֻמ֣וֹת": (None, "11.26.rn2", None),  # Jb11:6
    "מִ֥י~יִתֵּ֣ן": ("9.27.rn1", "11.26.rn2", None),  # Ps14:7, 53:7
    "אִ֥ם~תִּטֶּ֣ה": ("9.27.rn1", "11.26.rn2", None),  # Jb31:7
    #
    "וַ֥יַּעְזְרֵ֥ם": (None, "11.20.rn2", None),  # Ps37:40
    "הַ֥מְﬞקָרֶ֥ה": (None, "11.20.rn2", None),  # Ps104:3
    "נִ֥פְלְאֹתֶ֥יךָ": (None, "11.20.rn2", None),  # Ps40:6
    #
    "יִ֥שְׂמְח֥וּ": (None, "11.20.rn3", None),  # Ps67:5
    "אֶ֥זְכְּרָ֥ה": ("9.24.rn2", "11.20.rn3", None),  # Ps77:7
    "אֶ֥הֱב֥וּ": ("9.23", "11.20.rn3", None),  # Ps31:24
    "שָׁ֥בְרָ֥ה": ("9.24.rn2", "11.20.rn3", _EXP_VOC_FN_23),  # Ps69:21
    #
    "סַ֥לְעִ֥י": ("9.23.fn23", "11.20.rn4", "חטף חריק"),  # Ps18:3
    "תִּ֥מְﬞחַ֥ץ": ("9.24.rn2", "11.20.rn4", None),  # Ps68:24
    "קִ֥רְﬞבַ֥ת": (None, "11.20.rn4", None),  # Ps73:28
    "אַ֥נְﬞשֵׁ֥י": (None, "11.20.rn4", None),  # Jb34:10
    #
    "אִ֥ם~בְּתוֹרַ֥ת": ("9.27.rn2", "11.20.rn2", None),  # Ps1:2
    #
    "וַיִּ֥שְׁפְּכ֨וּ": ("9.26.rn2", "11.10", None),  # Ps106:38
    "רֵ֥עֲךָ֨": ("9.26.rn2", "11.10", None),  # Pr27:10
    "בַּ֥מַּכְתֵּ֡שׁ": (None, "11.10", None),  # Pr27:22
    #
    "יִ֥תְיַצְּב֨וּ׀": (None, "11.6.rn2", None),  # Ps2:2
    "הַ֥אֲשִׁימֵ֨ם׀": ("9.25.rn2", "11.6.rn2", None),  # Ps5:11
    "וְלִ֥שְׁכֵנַ֨י׀": ("9.25.rn2", "11.6.rn2", None),  # Ps31:12
    "וּ֥לְﬞצִיּ֨וֹן׀": (None, "11.6.rn2", None),  # Ps87:5
    "תַּ֥הְפֻּכ֨וֹת׀": ("9.25.rn2", "11.6.rn2", f"{_alap('9.23')} body text."),  # Pr6:14
    "לַ֥עֲלוּקָ֨ה׀": (None, "11.6.rn2", None),  # Pr30:15
    #
    "יִ֥רַדֹּֽף־אוֹיֵ֨ב׀": ("9.23.fn21", "11.3", f"CoS 11.3 has {_SRTM}."),  # Ps7:6
    "מִ֥מְﬞתִֽים־יָדְךָ֨׀": (None, "11.3", f"CoS 11.3 has {_SRTM}."),  # Ps17:14
    "יִ֥הְיֽוּ־לְרָצ֨וֹן׀": ("9.23.fn22", "11.3", _N_PS_19_15),  # Ps19:15
    "שִׁ֥מְﬞעָֽה~תְפִלָּתִ֨י׀": (None, "11.3", None),  # Ps39:13
    "טָ֥מְנֽוּ־גֵאִ֨ים׀": ("9.23.fn23", "11.3", f"vocal. CoS 11.3 has {_SRTM}."),  # Ps140:6
    "יֶ֥הֶלְמֵֽנִי~צַדִּ֨יק׀": ("9.34.rn2", "11.3", None),  # Ps141:5
    #
    "כׇּ֥ל~עַצְמוֹתַ֨י׀": ("9.27.rn3", "11.6.rn3", None),  # Ps35:10
    "הַ֥לְﬞלוּ~יָ֨הּ׀": ("9.27.rn3", "11.6.rn3", None),
    # Ps106:1, 111:1, 112:1, 113:1, 135:1, 147:1, 148:1, 149:1, 150:1
    "עַ֥ל~נַהֲר֨וֹת׀": ("9.27.rn3", "11.6.rn3", None),  # Ps137:1
    "מַ֥עֲדֶה־בֶּ֨גֶד׀": ("9.27", "11.6.rn2", f"{_alap('9.37')}. Mqf not omitted!"),  # Pr25:20
    "פֶּ֥ן~אֶשְׂבַּ֨ע׀": ("9.27.rn3", "11.6.rn3", None),  # Pr30:9
    "וּ֥תְהִי־ע֨וֹד׀": ("9.27", "11.6.rn2", f"{_alap('9.37')}. Mqf not omitted!"),  # Jb6:10
    "אִ֥ם~חֲרוּצִ֨ים׀": ("9.27.rn3", "11.6.rn3", None),  # Jb14:5
    #
    "אִ֥ם~תִּכְתּֽוֹשׁ־אֶת־הָאֱוִ֨יל׀": ("9.27.rn3", "11.6.rn3", None),  # Pr27:22
    #
    "כׇּ֥ל~אֲחֵי־רָ֨שׁ׀": ("9.27.rn3", "11.6.rn3", None),  # Pr19:7
    #
    "מֵ֥אִתְּךָ֗": (None, "11.19", f"{_MER_NOT_SEC}."),  # Ps22:26
    "תֵּ֥אָלַ֗מְנָה": ("9.20", "11.19", f"{_MER_NOT_SEC}."),  # Ps31:19
    "וְעָ֥דֵיכֶ֗ם": (None, "11.19", f"{_MER_NOT_SEC}."),  # Jb32:12
    #
    "כִּ֥י~גָ֘בַ֤ר": ("9.18", "11.4.rn1", None, _FWD_1),  # Ps117:2
    "כִּ֥י~רָ֘דַ֤ף": (None, "11.4.rn1", None, _FWD_1),  # Ps143:3
    #
    "כִּ֥י~גָ֘ד֤וֹל": ("9.18", "11.50.rn3", None, _FWD_3),  # Ps96:4
    "כִּ֥י~יֹ֘סִ֤יף": ("9.18", "11.14.rn1", None, _FWD_2),  # Jb34:37
    #
    "זִ֥בְחֵ֣י": ("9.23.fn23", None, "חטף צירה"),  # Ps51:19
    #
    "יִ֥רְאַ֣ת": ("9.23.fn23", None, _VOC_OR_AT_LEAST_NFS),  # Pr8:13
}
_QUALIFIERS = {**_QUALIFIERS_FOR_SEC_MERK, **_QUALIFIERS_FOR_SEC_MISC}

# {_GAYA} and then mqf:
#
# (Relevant to Ps12:6 & Ps89:20.)
#
# From the section https://he.wikisource.org/wiki/%D7%95%D7%99%D7%A7%D7%99%D7%98%D7%A7%D7%A1%D7%98:%D7%9E%D7%91%D7%95%D7%90_%D7%9C%D7%9E%D7%A7%D7%A8%D7%90_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A4%D7%A8%D7%A7_%D7%91#%D7%A2%D7%A7%D7%91%D7%99%D7%95%D7%AA_%D7%91%D7%9E%D7%A7%D7%A4%D7%99%D7%9D
#
# אך יש מקומות שהקריאה בהן יותר מורכבת, וייתכן שהמקף המסומן בכתר יעזור לקורא; לדוגמה:
#
# "וָ֥אֶתֵּֽן־נֶ֙זֶם֙" (יחזקאל טז,יב)
#
# להלן רשימה של כל המקומות בכ"א הספרים שבהם מופיע מקף בתיבת משרת בכתר ובמהדורתנו:
#
# 01. שופטים ח,י (א=שֹׁ֥לֵֽף־חָֽרֶב)
# 02.  שופטים כ,ב (א=שֹׁ֥לֵֽף־חָֽרֶב)
# 03.  שופטים כ,לה (א=שֹׁ֥לֵֽף־חָֽרֶב)
# 04.  שמ"ב ז,ט (א=וְעָשִׂ֤תִֽי־לְךָ֙)
# 05.  ישעיהו מ,ז (א=נָ֣בֵֽל־צִ֔יץ)
# 06.  ישעיהו נט,טז (א=וַתּ֤וֹשַֽׁע־לוֹ֙)
# 07.  ישעיהו סג,ה (א=וַתּ֤וֹשַֽׁע־לִי֙)
# 08.  ישעיהו סו,ח (א=אִם־יִוָּ֥לֵֽד־גּ֖וֹי)
# 09.  יחזקאל א,ד (א=וְנֹ֥גַֽהּ־ל֖וֹ)
# 10.  יחזקאל טז,יב (א=וָ֥אֶתֵּֽן־נֶ֙זֶם֙)
# 11.  דה"א כא,ה (א=שֹׁ֥לֵֽף־חָֽרֶב)
# 12.  דה"ב ח,יא (א=אֲשֶׁר־בָּ֥אָֽה־אֲלֵיהֶ֖ם)
# 13.  דה"ב יד,ו (א=וַיָּ֥נַֽח־לָ֖נוּ)

# 01. prose/b-(üslq)/(mer),(ümtg)-(üslq)
# 02. prose/b-(üslq)/(mer),(ümtg)-(üslq)
# 03. prose/b-(üslq)/(mer),(ümtg)-(üslq)
# 04. (mahapakh)
# 05. (munax)
# 06. (mahapakh)
# 07. (mahapakh)
# 08. prose/b-(tip)/-(mer),(ümtg)-(tip)
# 09. prose/b-(tip)/(mer),(ümtg)-(tip)
# 10. prose/b-(pash)/(mer),(ümtg)-(pash),(pash)
# 11. prose/b-(üslq)/(mer),(ümtg)-(üslq)
# 12. prose/b-(tip)/-(mer),(ümtg)-(tip)
# 13. prose/b-(tip)/(mer),(ümtg)-(tip)
