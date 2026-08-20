import os

import re
import boj_paths
from boj_render import boj_html
from mb_cmn import str_defs as sd
from mb_cmn.my_utils import sl_map
from mb_cmn.my_utils import sum_of_map
from mb_cmn.my_utils import dv_map
from author_boj_util import dollar_sub_g


def help_gen_html_file(tdm_ch, fname, title, cbody):
    top_dir, css_href = tdm_ch
    out_path = top_dir / fname
    write_ctx = boj_html.WriteCtx(title, out_path, css_hrefs=(css_href,))
    boj_html.write_html_to_file(cbody, write_ctx)


def paren(inner):
    return ["(", inner, ")"]


def std_anchor(anchor_proper, quoted_part):
    return [anchor_proper, ", “", quoted_part, ".”"]


def book_title(contents):
    return boj_html.span_c(dollar_sub(contents), "book-title")


def span_gray(contents):
    return boj_html.span_c(dollar_sub(contents), "gray")


def span_unpointed_tanakh(contents, attr=None):
    return boj_html.span(contents, _awc(attr, "unpointed-tanakh"))


def emphasis(contents):
    return boj_html.emphasis(dollar_sub(contents))


def table_datum(contents):
    return boj_html.table_datum(dollar_sub(contents))


def stem_eq(path1, path2):
    return _stem(path1) == _stem(path2)


def assert_stem_eq(path1, path2):
    assert stem_eq(path1, path2), (path1, path2)


def para(contents, attr=None):
    return boj_html.para(dollar_sub(contents), attr)


def para_cc(contents, attr=None):
    """para with class=center"""
    return para(contents, {"class": "center"})


def para_dr_cc(contents, attr=None):
    """para with dir=rtl, class=center"""
    return para(contents, {"dir": "rtl", "class": "center"})


def blockquote(contents, attr=None):
    return boj_html.blockquote(dollar_sub(contents), attr)


def unordered_list(items, attr=None):
    """Create an unordered list with dollar_sub applied to each item"""
    return boj_html.unordered_list([dollar_sub(item) for item in items], attr)


def ordered_list(items, attr=None):
    """Create an ordered list with dollar_sub applied to each item"""
    return boj_html.ordered_list([dollar_sub(item) for item in items], attr)


def heading_level_1(contents, attr=None):
    """Create a level 1 heading with dollar_sub applied to the contents"""
    return boj_html.heading_level_1(dollar_sub(contents), attr)


def heading_level_2(contents, attr=None):
    """Create a level 2 heading with dollar_sub applied to the contents"""
    return boj_html.heading_level_2(dollar_sub(contents), attr)


def hbo(contents, attr=None):
    return boj_html.bdi(contents, _awl(attr, "hbo"))


def para_hbo(contents, attr=None):
    return boj_html.para(contents, _awc(_awl(attr, "hbo"), "center"))


def para_hbo_es(contents, attr=None):
    class_val = "center extra-letter-spacing"
    return boj_html.para(contents, _awc(_awl(attr, "hbo"), class_val))


def para_modhe(contents, attr=None):
    """Modern Hebrew"""
    return boj_html.para(contents, _awl(attr, "he"))


def hbo_big(contents, attr=None):
    return hbo(contents, _awc(attr, "big"))


def hbo_es(contents, attr=None):
    return hbo(contents, _awc(attr, "extra-letter-spacing"))


def hbo_big_es(contents, attr=None):
    return hbo(contents, _awc(attr, "big extra-letter-spacing"))


def para_for_img(img_path, widthclass=None, img_prefix="img", scale=None):
    img_attr = {"src": f"{img_prefix}/{img_path}"}
    if widthclass is not None and scale is None:
        img_attr["class"] = widthclass
    if scale is not None:
        # Read natural image dimensions and compute scaled pixel sizes.
        # This avoids CSS percentage pitfalls (percentages are relative
        # to the containing block, not the image's intrinsic size).
        from PIL import Image as _PILImage

        img_file = boj_paths.jobn_dir() / img_prefix / img_path
        with _PILImage.open(img_file) as im:
            nat_w, nat_h = im.size
        w = round(nat_w * scale)
        h = round(nat_h * scale)
        img_attr["style"] = f"width:{w}px;height:{h}px"
    img_element = boj_html.img(img_attr)
    return boj_html.para(img_element, {"class": "center"})


def table_c(contents, attr=None):
    """Create a centered table"""
    return boj_html.table(contents, _awc(attr, "center"))


def para_ul(para_contents, ul_items):
    return [
        para(para_contents),
        unordered_list(ul_items),
    ]


def para_ol(para_contents, ol_items):
    return [
        para(para_contents),
        ordered_list(ol_items),
    ]


def para_table(cpara_before, table_data, cparas_after=None):
    return [
        para(cpara_before),
        std_table(table_data),
        *sl_map(para, cparas_after or []),
    ]


def he_en_table_wct(ti_he_en_triples):
    """Hebrew-English table with centered titles.

    Args:
        ti_he_en_triples: list of (title, hebrew, english) triples,
            each rendered as a two-row block (title row + content row).
    """
    args_to_table = sum_of_map(_he_en_table_wci_row_pair, ti_he_en_triples)
    return table_c(args_to_table)


def dollar_sub(contents):
    return dollar_sub_g.dollar_sub_g(_DOLLAR_SUB_DISPATCH, contents)


def std_table(
    table_data,
    coldirs=None,
    tdattrs=None,
    arg_to_troh=None,
):
    if coldirs:
        assert not tdattrs
        tdattrs = [{"dir": coldir} for coldir in coldirs]
    args_to_table = sl_map((_std_row_of_data, tdattrs), _de_dict(table_data))
    if arg_to_troh:
        header_row = _std_row_of_headers(arg_to_troh)
        args_to_table = [header_row, *args_to_table]
    return table_c(args_to_table)


def anc_h(contents, href_val):
    return boj_html.anchor_h(dollar_sub(contents), href_val)


def span_color(text, color):
    return boj_html.span(text, {"style": f"color: {color}"})


def span_rtl(contents):
    return boj_html.span(contents, {"dir": "rtl"})


def yyy_dash_nothing(contents):
    return [contents, "-אפס"]


def nothing_dash_yyy(contents):
    return ["אפס-", contents]


def consensus_to_ascii(consensus):
    """Convert a Hebrew consensus string to an ASCII word-id.

    Args:
        consensus: Hebrew string from the qr-consensus field.

    Returns:
        ASCII transliteration suitable for use as a word identifier.
    """
    kept = "".join(_KEEP_RE.findall(consensus))
    return kept.translate(_HEBREW_TO_OUR_CODE)


def consensus_to_bare_hebrew(consensus):
    """Return just the bare Hebrew letters (and maqaf) of a consensus string.

    Args:
        consensus: Hebrew string from a qr-consensus / qr-*-proposed field.

    Returns:
        The same Hebrew word(s) with vowel points and accents stripped,
        suitable for display (e.g. עִמּ֣וֹ → עמו).
    """
    return "".join(_KEEP_RE.findall(consensus))


# def pasoleg_pas(string: str):
#     return _pasoleg_xxx(string, "$sub_pe")


# def pasoleg_leg(string: str):
#     return _pasoleg_xxx(string, "$sub_lamed")


# def pasoleg_qm(string: str):
#     return _pasoleg_xxx(string, "$sub_qm")


# def note_on_arabizi_3():
#     return [
#         ["(Above I use “3” for the Hebrew letter $ayin,"],
#         [" following the convention of Arabizi, the Arabic chat alphabet."],
#         [" So, for example, געיה is transliterated as"],
#         [" $gaya rather than more conventional"],
#         [" alternatives such as $gaya_with_half_ring_for_ayin.)"],
#     ]


#############################################################################
#############################################################################


def _he_en_table_wci_row_pair(ti_he_en_triple):
    title, hebrew, english = ti_he_en_triple
    return [
        _std_row_of_data(
            [{"colspan": "2"}],
            [para_cc(title)],
        ),
        _std_row_of_data(
            [{"dir": "rtl"}, {"dir": "ltr"}],
            [hebrew, english],
        ),
    ]


def _de_dict(table_data):
    if isinstance(table_data, dict):
        return [[k, *v] for k, v in table_data.items()]
    return table_data


def _std_row_of_data(tdattrs, cells):
    return boj_html.table_row_of_data(sl_map(_std_cell, cells), tdattrs)


def _std_row_of_headers(cells):
    return boj_html.table_row_of_headers(sl_map(_std_cell, cells))


def _std_cell(htel):
    if isinstance(htel, str):
        if re.search(r"[א-ת]", htel) and not re.search(r"[A-Za-z]", htel):
            return hbo(htel)
    return dollar_sub(htel)


def _romanized(string: str):
    assert isinstance(string, str)
    return boj_html.span_c(string, "romanized")


def _cap(string: str):
    words = string.split(" ")
    return " ".join(word.capitalize() for word in words)


def _abbreviation_sc(string: str, cap=False):
    return _small_caps(string, cap)


def _unicode_name_sc(string: str):
    return _small_caps(string)


def _small_caps(string: str, cap=False):
    if cap:
        # Leave in normal caps (e.g. "BHS") rather than messing around with
        # first letter (e.g. "B") in normal caps followed by rest (e.g. "HS")
        # in small caps.
        return string
    return boj_html.abbr(string, {"class": "small-caps"})


def _awc(attr, class_val):
    """attributes with class"""
    return _add_attr(attr, "class", class_val)


def _awl(attr, lang_val):
    """attributes with lang"""
    return _add_attr(attr, "lang", lang_val)


def _add_attr(attrdic, attrkey, attrval):
    """add key and value to attributes dictionary"""
    attrdic_nn = attrdic or {}  # nn: non-None
    assert attrkey not in attrdic_nn
    return {attrkey: attrval, **attrdic_nn}


def _rom_with_cap(locase_key: str, locase_val: str):
    return {
        locase_key: _romanized(locase_val),
        _upcase_key(locase_key): _romanized(_cap(locase_val)),
    }


# def _rom_with_wpl(locase_key: str, letter_name: str, letter_itself: str):
#     """wpl: with parenthesized letter"""
#     return {
#         locase_key: _rom(letter_name),
#         _wpl_key(locase_key): [_rom(letter_name), f" ({letter_itself})"],
#     }


def _upcase_key(locase_key: str):
    key = locase_key
    assert key.startswith("$")
    assert len(key) > 1
    assert key[1].isalpha()
    assert key[1].islower()
    return "$" + key[1].upper() + key[2:]


# def _wpl_key(key: str):
#     """wpl: with parenthesized letter"""
#     return f"{key}_wpl"


def _stem(path):
    basename = os.path.basename(path)
    return os.path.splitext(basename)[0]


_UNICODE_NAME_SC = {
    "$AH": "ATNAH HAFUKH",
    "$GERESH": "GERESH",
    "$GERMUQ": "GERESH MUQDAM",
    "$HHFV": "HOLAM HASER FOR VAV",
    "$HOLAM": "HOLAM",
    "$TIPEHA": "TIPEHA",
    "$TSERE": "TSERE",
    "$HIRIQ": "HIRIQ",
    "$TSINOR": "TSINOR",
    "$YETIV": "YETIV",
    "$QAMATS": "QAMATS",
    "$QQ": "QAMATS QATAN",
    "$ZARQA": "ZARQA",
    "$ZINOR": "ZINOR",
    "$ZWJ": "ZWJ",
    "$HOLAM_HASER_FOR_VAV": "HOLAM HASER FOR VAV",
    "$MAHAPAKH": "MAHAPAKH",
    "$POINT_SEGOL": "POINT SEGOL",
    "$DEHI": "DEHI",
}
_ABBR_SC = {
    "$CD_ROM": "CD-ROM",
    "$BHS": "BHS",
    "$WLC": "WLC",
    "$UXLC": "UXLC",
    "$KUSATU": "KUSATU",
    "$BHQ": "BHQ",
    "$DM": "DM",
    "$BHL": "BHL",
    "$BHL_A": "BHL-A",
    "$DBG": "DBG",
    "$CTR": "CTR",
    "$CTR_A": "CTR-A",
    "$CTR_B": "CTR-B",
    "$IVS": "IVS",
    "$MAM": "MAM",
    "$JP": "JP",
    "$JP_A": "JP-A",
    "$JP_B": "JP-B",
    "$NLI": "NLI",
    "$SEWG": "SEWG",
    "$KCT": "KCT",
    "$SBB": "SBB",
    "$WMG": "WMG",
    "$MG": "MG",
    "$TM": "TM",
    "$JC": "JC",
    "$FS": "FS",
    "$AC": "AC",
    "$LC": "LC",
    "$LSSLG": "LSSLG",
}
_ROMANIZED = {
    "$alef": "alef",
    "$tsere": "tsere",
    # "$gaya_with_half_ring_for_ayin": "gaʿya",
    "$germuq": "geresh muqdam",
    "$germuq_gm": "g. m.",
    "$mahapakh_metsunneret": "mahapakh metsunneret",
    "$mem": "mem",
    "$merkha": "merkha",
    "$merkha_metsunneret": "merkha metsunneret",
    "$oleh_veyored": "oleh veyored",
    "$qere": "qere",
    "$revia": "revia",
    "$revmug": "revia mugrash",
    "$tsinnor": "tsinnor",
    "$vav": "vav",
    "$yby": "yeraḥ ben yomo",
    "$ah": "atnaḥ hafukh",
    "$qamats": "qamats",
    "$qq": "qamats qatan",
    "$qg": "qamats gadol",
    "$dexi": "deḥi",
    "$zarqa": "zarqa",
    "$tarxa": "tarḥa",
    "$geresh": "geresh",
    "$tav": "tav",
    "$segol": "segol",
    "$hehe": "he",  # hehe = Hebrew [letter] he (avoids clash with English "he")
    "$tipexa": "tipeḥa",
    "$xolam": "ḥolam",
    "$xolam_xaser_xx": "ḥ. ḥ.",  # a bit like germuq_gm
    "$malei": "malei",
    "$xiriq": "ḥiriq",
    "$xiriq_qatan": "ḥiriq qatan",
    "$kaf": "kaf",
    "$khaf": "khaf",
    "$paseq": "paseq",
    "$pasoleg": "paseq/legarmeh",
    "$maqaf": "maqaf",
    "$munax": "munaḥ",
    "$naqdan": "naqdan",
    "$azla": "azla",
    "$legarmeh": "legarmeh",
    "$legarmeh_leg": "leg.",
    "$yod": "yod",
    "$shin": "shin",
    "$sin": "sin",
    "$pe": "pe",
    "$resh": "resh",
    "$lamed": "lamed",
    "$patax": "pataḥ",
    "$shuruq": "shuruq",
    "$xataf": "ḥataf",
    "$xataf_shewa": "ḥataf shewa",
    "$xataf_patax": "ḥataf pataḥ",
    "$xataf_segol": "ḥataf segol",
    "$nun": "nun",
    "$pashta": "pashta",
    "$xolam_malei": "ḥolam malei",
    "$iluy": "iluy",
}
_UNICODE_NAME_SC = dv_map(_unicode_name_sc, _UNICODE_NAME_SC)
_ABBR_SC = dv_map(_abbreviation_sc, _ABBR_SC)
_ROMANIZED = dv_map(_romanized, _ROMANIZED)


def _dlink(cv, sid):
    """Build a detail-page <a> element for a quirkrec short ID."""
    return boj_html.anchor_h(cv, f"../jobn-details/{sid}.html")


_DOLLAR_SUB_DISPATCH = {
    #
    # "$sub_qm": boj_html.sub("?"),
    # "$sub_pe": boj_html.sub("פ"),
    # "$sub_lamed": boj_html.sub("ל"),
    #
    "$thinsp": sd.THSP,
    "$hairsp": sd.HAIRSP,
    "$hs_sl_hs": f"{sd.HAIRSP}/{sd.HAIRSP}",
    "$almost_equal_to": "\N{ALMOST EQUAL TO}",  # ≈
    #
    "$gaya": "געיה",
    #
    **_rom_with_cap("$ayin", "ayin"),
    **_rom_with_cap("$oleh", "oleh"),
    **_rom_with_cap("$shewa", "shewa"),
    **_rom_with_cap("$tsinnorit", "tsinnorit"),
    **_rom_with_cap("$xolam_xaser", "ḥolam ḥaser"),
    **_rom_with_cap("$yored", "yored"),
    **_rom_with_cap("$yetiv", "yetiv"),
    **_rom_with_cap("$mahapakh", "mahapakh"),
    #
    **_UNICODE_NAME_SC,
    **_ABBR_SC,
    **_ROMANIZED,
    #
    # Plain verse references (no link): non-Job bible references
    "$2Kings_4_7": "2 Kings 4:7",
    "$Lamentations_4_16": "Lamentations 4:16",
    "$2Samuel_18_20": "2 Samuel 18:20",
    "$2Samuel_5_2": "2 Samuel 5:2",
    "$1Samuel_12_10": "1 Samuel 12:10",
    "$Isaiah_13_6": "Isaiah 13:6",
    "$Joel_1_15": "Joel 1:15",
    "$Ezekiel_42_9": "Ezekiel 42:9",
    "$Ps_118_5": "Ps 118:5",
    "$Ps_86_7": "Ps 86:7",
    "$Ps_139_7": "Ps 139:7",
    "$Ps_115_3": "Ps 115:3",
    "$Ps_119_16": "Ps 119:16",
    #
    # Plain verse references (no link): Job verses without quirkrec records
    # or self-references
    "$plain_6_12": "6:12",
    "$plain_7_14": "7:14",
    "$plain_8_11": "8:11",
    "$plain_10_6": "10:6",
    #
    # Plain verse references (no link): multi-record Job verses
    "$plain_3_2": "3:2",
    "$plain_42_6": "42:6",
    "$plain_34_33": "34:33",
    #
    # Verse-ref links to single-record quirkrec detail pages
    "$link_3_4": _dlink("3:4", "0304"),
    "$link_4_9": _dlink("4:9", "0409"),
    "$link_4_17": _dlink("4:17", "0417"),
    "$link_5_23": _dlink("5:23", "0523"),
    "$link_6_17": _dlink("6:17", "0617"),
    "$link_6_21": _dlink("6:21", "0621"),
    "$link_9_35": _dlink("9:35", "0935"),
    "$link_11_6": _dlink("11:6", "1106"),
    "$link_16_6": _dlink("16:6", "1606"),
    "$link_18_6": _dlink("18:6", "1806"),
    "$link_19_2": _dlink("19:2", "1902"),
    "$link_19_5": _dlink("19:5", "1905"),
    "$link_21_15": _dlink("21:15", "2115"),
    "$link_22_12": _dlink("22:12", "2212"),
    "$link_22_28": _dlink("22:28", "2228"),
    "$link_24_1": _dlink("24:1", "2401"),
    "$link_24_16": _dlink("24:16", "2416"),
    "$link_26_14": _dlink("26:14", "2614"),
    "$link_27_9": _dlink("27:9", "2709"),
    "$link_27_13": _dlink("27:13", "2713"),
    "$link_31_5": _dlink("31:5", "3105"),
    "$link_31_7": _dlink("31:7", "3107"),
    "$link_32_6": _dlink("32:6", "3206"),
    "$link_32_11": _dlink("32:11", "3211"),
    "$link_34_5": _dlink("34:5", "3405"),
    "$link_34_19": _dlink("34:19", "3419-NKR0"),
    "$link_35_7": _dlink("35:7", "3507"),
    "$link_35_14": _dlink("35:14", "3514"),
    "$link_39_20": _dlink("39:20", "3920"),
    #
    # Verse-ref links to multi-record quirkrec detail pages (disambiguated)
    "$link_18_4_HLM3N5_2_of_2_FTW": _dlink("18:4", "1804-HLM3N5_2_of_2_FTW"),
    "$link_19_16_QRAFY": _dlink("19:16", "1916-QRAFY"),
    "$link_19_16_BMV0PY": _dlink("19:16", "1916-BMV0PY"),
    "$link_22_21_3MV": _dlink("22:21", "2221-3MV"),
    "$link_38_12_YD3F_HJXR": _dlink("38:12", "3812-YD3F_HJXR"),
    "$link_38_12_HMYMY5": _dlink("38:12", "3812-HMYMY5"),
    "$link_34_33_VMH0YD3F": _dlink("34:33", "3433-VMH0YD3F"),
    "$link_34_33_HM3M5": _dlink("34:33", "3433-HM3M5"),
    "$link_34_33_YJLMNH_2_of_2_FTW": _dlink("34:33", "3433-YJLMNH_2_of_2_FTW"),
}


_HEBREW_TO_OUR_CODE_FROM = "אבגדה" + "וזחטי" + "כלמנס" + "עפצקר" + "שת" + "ךםןףץ" + "־ "
_HEBREW_TO_OUR_CODE_TO = "ABGDH" + "VZXEY" + "KLMNO" + "3PCQR" + "JF" + "56789" + "0_"
_HEBREW_TO_OUR_CODE = str.maketrans(
    _HEBREW_TO_OUR_CODE_FROM,
    _HEBREW_TO_OUR_CODE_TO,
)
# ־ is maqaf (U+05BE). 0 (zero) is maqaf because - is invalid in identifiers.
# Space maps to underscore (for multi-word consensus strings).

_KEEP_RE = re.compile(f"[{re.escape(_HEBREW_TO_OUR_CODE_FROM)}]+")


# אבגדה וזחטי כלמנס עפצקר שת
# Our code plus a highlight of unintuitive choices:
# ABGDH VZXEY KLMNO 3PCQR JF plus ISTUW unused
#         XE      O 3 C   JF
# X: ח
# E: ט
# O: ס (the letter O not the digit 0)
# 3: ע (Arabizi)
# C: צ (Michigan-Claremont)
# J: ש (vs O for ס, leaving S unused)
# F: ת (vs E for ט, leaving T unused)
#
# Pairs of note: E/F for ט/ת; O/J for ס/ש (leaving T and S unused).
# I.e. EF for tet/tav, OJ for samekh/shin.
#
# Michigan-Claremont plus where I differ from it:
# )BGDH WZX+Y KLMNS (PCQR $T plus ampersand (&) for sin
# A     V  E      O 3     JF
# (To stay alphanumeric, I use AE3J for אטעש instead of ")+($".)
# (My plain differences are VOF for וסת instead of "WST".)
#
# Another code of ours plus where this one differs (ignoring case):
# αbgdh vzxθy klmnσ 3pcqr $τ
# A        E      O       JF
# Pairs of note: θ/τ for ט/ת; σ/$ for ס/ש (leaving t and s unused).
# I.e. theta/tau for tet/tav, sigma/dollar-sign for samekh/shin.
# (To stay alphanumeric, I use AEOJF for אטסשת instead of "αθσ$τ".)
#
# For another approach, Google SimHebrew (Jonathan Orr-Stav).
