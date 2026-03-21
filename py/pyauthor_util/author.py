import os

import re
from py_misc import my_html
from pycmn import str_defs as sd
from pycmn.my_utils import sl_map
from pycmn.my_utils import sum_of_map
from pycmn.my_utils import dv_map
from pyauthor_util import dollar_sub_g


def help_gen_html_file(py_file, tdm_ch, fname, title, cbody):
    assert_stem_eq(py_file, fname)
    top_dir, css_href = tdm_ch
    out_path = f"{top_dir}/{fname}"
    py_basename = os.path.basename(py_file)
    comment = f"Generated from {py_basename} — do not edit by hand"
    write_ctx = my_html.WriteCtx(
        title, out_path, css_hrefs=(css_href,), html_comment=comment
    )
    my_html.write_html_to_file(cbody, write_ctx)


def dquote(contents):
    """Wrap contents in curly double quotes."""
    if isinstance(contents, str):
        return sd.LDQM + contents + sd.RDQM
    return [sd.LDQM, *contents, sd.RDQM]


def paren(inner):
    return ["(", inner, ")"]


def std_anchor(anchor_proper, quoted_part):
    return [anchor_proper, ", “", quoted_part, ".”"]


def book_title(contents):
    return my_html.span_c(dollar_sub(contents), "book-title")


def span_gray(contents):
    return my_html.span_c(dollar_sub(contents), "gray")


def emphasis(contents):
    return my_html.emphasis(dollar_sub(contents))


def table_datum(contents):
    return my_html.table_datum(dollar_sub(contents))


def stem_eq(path1, path2):
    return _stem(path1) == _stem(path2)


def assert_stem_eq(path1, path2):
    assert stem_eq(path1, path2), (path1, path2)


def para(contents, attr=None):
    return my_html.para(dollar_sub(contents), attr)


def para_cc(contents, attr=None):
    """para with class=center"""
    return para(contents, {"class": "center"})


def para_dr_cc(contents, attr=None):
    """para with dir=rtl, class=center"""
    return para(contents, {"dir": "rtl", "class": "center"})


def blockquote(contents, attr=None):
    return my_html.blockquote(dollar_sub(contents), attr)


def unordered_list(items, attr=None):
    """Create an unordered list with dollar_sub applied to each item"""
    return my_html.unordered_list([dollar_sub(item) for item in items], attr)


def ordered_list(items, attr=None):
    """Create an ordered list with dollar_sub applied to each item"""
    return my_html.ordered_list([dollar_sub(item) for item in items], attr)


def heading_level_1(contents, attr=None):
    """Create a level 1 heading with dollar_sub applied to the contents"""
    return my_html.heading_level_1(dollar_sub(contents), attr)


def heading_level_2(contents, attr=None):
    """Create a level 2 heading with dollar_sub applied to the contents"""
    return my_html.heading_level_2(dollar_sub(contents), attr)


def heading_level_3(contents, attr=None):
    """Create a level 3 heading with dollar_sub applied to the contents"""
    return my_html.heading_level_3(dollar_sub(contents), attr)


def hbo(contents, attr=None):
    return my_html.bdi(contents, _awl(attr, "hbo"))


def para_hbo(contents, attr=None):
    return my_html.para(contents, _awc(_awl(attr, "hbo"), "center"))


def para_hbo_es(contents, attr=None):
    class_val = "center extra-letter-spacing"
    return my_html.para(contents, _awc(_awl(attr, "hbo"), class_val))


def para_modhe(contents, attr=None):
    """Modern Hebrew"""
    return my_html.para(contents, _awl(attr, "he"))


def hbo_big(contents, attr=None):
    return hbo(contents, _awc(attr, "big"))


def hbo_es(contents, attr=None):
    return hbo(contents, _awc(attr, "extra-letter-spacing"))


def hbo_big_es(contents, attr=None):
    return hbo(contents, _awc(attr, "big extra-letter-spacing"))


def para_for_img(img_path, widthclass=None):
    img_class = {"class": widthclass} if widthclass is not None else {}
    img_element = my_html.img({"src": f"img/{img_path}", **img_class})
    return my_html.para(img_element, {"class": "center"})


def table_c(contents, attr=None):
    """Create a centered table"""
    return my_html.table(contents, _awc(attr, "center"))


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
    """Hebrew-English table with centered titles."""
    cg = my_html.colgroup(
        [my_html.col({"width": "40%"}), my_html.col({"width": "60%"})]
    )
    args_to_table = [cg, *sum_of_map(_he_en_table_wci_row_pair, ti_he_en_triples)]
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
    return my_html.anchor_h(dollar_sub(contents), href_val)


def span_color(text, color):
    return my_html.span(text, {"style": f"color: {color}"})


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
    _VT = "vertical-align: top"
    title, hebrew, english = ti_he_en_triple
    return [
        _std_row_of_data(
            [{"colspan": "2", "style": "padding-right: 20%"}],
            [para_cc(title)],
        ),
        _std_row_of_data(
            [{"dir": "rtl", "style": _VT}, {"dir": "ltr", "style": _VT}],
            [hebrew, english],
        ),
    ]


def _de_dict(table_data):
    if isinstance(table_data, dict):
        return [[k, *v] for k, v in table_data.items()]
    return table_data


def _std_row_of_data(tdattrs, cells):
    return my_html.table_row_of_data(sl_map(_std_cell, cells), tdattrs)


def _std_row_of_headers(cells):
    return my_html.table_row_of_headers(sl_map(_std_cell, cells))


def _std_cell(htel):
    if isinstance(htel, str):
        if re.search(r"[א-ת]", htel) and not re.search(r"[A-Za-z]", htel):
            return hbo(htel)
    return dollar_sub(htel)


def _romanized(string: str):
    assert isinstance(string, str)
    return my_html.span_c(string, "romanized")


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
    return my_html.abbr(string, {"class": "small-caps"})


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


def _anc_h(contents, href_val):
    return my_html.anchor_h(contents, href_val)


_AID = "https://www.chabad.org/library/bible_cdo/aid"
_G = "https://docs.google.com/document/u/0"
_URL_PROPOSAL_ALT_YBY = f"{_G}/d/1M7-sVTuKEJLdFRDXLpOeKEjtynSTvY2EM6Lj1uK4ylA/edit"
_URL_PROPOSAL_ZARQA = f"{_G}/d/1qJby64wXq9ueTUHXFlIlYdgohRFlnUqT4SkyNEFWMKU/edit"
_URL_CTR_CDROM_NLI = "https://www.nli.org.il/en/items/NNL_ALEPH990019164710205171/NLI"
_URL_CHABAD = "https://www.chabad.org/"
_URL_CHABAD_TANAKH = f"{_AID}/63255/jewish/The-Bible-with-Rashi.htm"
_URL_CHABAD_PSALM_32 = f"{_AID}/16253/#lt=he"
_URL_JUD_PRESS_NAKH = (
    "https://judaicapress.com/collections/torah-study/products"
    "/judaica-press-prophets-and-writings-24-vol-set"
)
_ANCHORS = {
    "$anc_proposal_alt_yby": _anc_h("proposal", _URL_PROPOSAL_ALT_YBY),
    "$anc_proposal_zarqa": _anc_h("proposal", _URL_PROPOSAL_ZARQA),
    "$anc_record_ctr_cdrom_nli": _anc_h("record", _URL_CTR_CDROM_NLI),
    "$anc_Chabad_website": _anc_h("Chabad website", _URL_CHABAD),
    "$anc_Chabad_CTR": _anc_h("The Complete Tanach with Rashi", _URL_CHABAD_TANAKH),
    "$anc_Chabad_Psalm_32": _anc_h("Psalm 32", _URL_CHABAD_PSALM_32),
    "$anc_Jud_Press_Nakh": _anc_h("Prophets and Writings", _URL_JUD_PRESS_NAKH),
}
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
    "$aliyah": "aliyah",
    "$aliyot": "aliyot",
    "$parashah": "parashah",
    "$parashiyot": "parashiyot",
    "$kohen": "kohen",
    "$levi": "levi",
    "$yisrael": "yisrael",
    "$maftir": "maftir",
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
    "$shalshelet": "shalshelet",
    "$shalshelet_gedolah": "shalshelet gedolah",
    "$shalshelet_qetanah": "shalshelet qetanah",
    "$revmug": "revia mugrash",
    "$qadma": "qadma",
    "$telisha": "telisha",
    "$tevir": "tevir",
    "$tsinnor": "tsinnor",
    "$vav": "vav",
    "$yby": "yeraḥ ben yomo",
    "$ah": "atnaḥ hafukh",
    "$qamats": "qamats",
    "$qq": "qamats qatan",
    "$qg": "qamats gadol",
    "$dexi": "deḥi",
    "$zarqa": "zarqa",
    "$tarxa": "tarḥa",
    "$geresh": "geresh",
    "$tav": "tav",
    "$segol": "segol",
    "$hehe": "he",  # hehe = Hebrew [letter] he (avoids clash with English "he")
    "$tipeha": "tipeḥa",
    "$xolam": "ḥolam",
    "$xolam_xaser_xx": "ḥ. ḥ.",  # a bit like germuq_gm
    "$malei": "malei",
    "$xiriq": "ḥiriq",
    "$xiriq_qatan": "ḥiriq qatan",
    "$kaf": "kaf",
    "$khaf": "khaf",
    "$pasoleg": "paseq/legarmeh",
    "$maqaf": "maqaf",
    "$azla": "azla",
    "$legarmeh": "legarmeh",
    "$legarmeh_leg": "leg.",
    "$yod": "yod",
    "$shin": "shin",
    "$sin": "sin",
    "$pe": "pe",
    "$resh": "resh",
    "$lamed": "lamed",
    "$patax": "pataḥ",
    "$shuruq": "shuruq",
    "$xataf": "ḥataf",
    "$xataf_shewa": "ḥataf shewa",
    "$xataf_patax": "ḥataf pataḥ",
    "$xataf_segol": "ḥataf segol",
    "$nun": "nun",
    "$pashta": "pashta",
    "$xolam_malei": "ḥolam malei",
    "$iluy": "iluy",
}
_UNICODE_NAME_SC = dv_map(_unicode_name_sc, _UNICODE_NAME_SC)
_ABBR_SC = dv_map(_abbreviation_sc, _ABBR_SC)
_ROMANIZED = dv_map(_romanized, _ROMANIZED)
_DOLLAR_SUB_DISPATCH = {
    #
    # "$sub_qm": my_html.sub("?"),
    # "$sub_pe": my_html.sub("פ"),
    # "$sub_lamed": my_html.sub("ל"),
    #
    "$thinsp": sd.THSP,
    "$hairsp": sd.HAIRSP,
    "$hs_sl_hs": f"{sd.HAIRSP}/{sd.HAIRSP}",
    "$almost_equal_to": "\N{ALMOST EQUAL TO}",  # ≈
    #
    "$gaya": "געיה",
    "$parashah_sl_aliyah": _romanized("parashah/aliyah"),
    #
    **_rom_with_cap("$ayin", "ayin"),
    **_rom_with_cap("$oleh", "oleh"),
    **_rom_with_cap("$shewa", "shewa"),
    **_rom_with_cap("$tsinnorit", "tsinnorit"),
    **_rom_with_cap("$xolam_xaser", "ḥolam ḥaser"),
    **_rom_with_cap("$yored", "yored"),
    **_rom_with_cap("$yetiv", "yetiv"),
    **_rom_with_cap("$mahapakh", "mahapakh"),
    **_rom_with_cap("$munax", "munaḥ"),
    **_rom_with_cap("$pazer", "pazer"),
    **_rom_with_cap("$paseq", "paseq"),
    #
    **_ANCHORS,
    **_UNICODE_NAME_SC,
    **_ABBR_SC,
    **_ROMANIZED,
}


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
