import py_html.legacy_html as aht_html
import mb_cmn.hebrew_points as hpo
import mb_cmn.str_defs as sd
import yeivin_itm.helpers as hlp
import yeivin_itm.content.my_yeivin_amisc_manuscripts as mss
import yeivin_itm.content.my_yeivin_amisc_substitutions_private as subpriv
import mb_author.dollar_sub_g as dollar_sub_g


def dol(contents):
    return dollar_sub_g.dollar_sub_g(_DOLLAR_SUB_DISPATCH, contents)


def para(contents, attr=None):
    return aht_html.para(dol(contents), attr)


def blockquote(contents, attr=None):
    return aht_html.blockquote(dol(contents), attr)


def blockquote_p(contents, b_attr=None, p_attr=None):
    return aht_html.blockquote(para(contents, p_attr), b_attr)


def ordered_list(liconts, attrs=None):
    return aht_html.ordered_list(list(map(dol, liconts)), attrs)


def unordered_list(liconts, attrs=None):
    return aht_html.unordered_list(list(map(dol, liconts)), attrs)


def para_paren(contents):
    return hlp.para_paren(dol(contents))


def footnote(contents):
    return aht_html.footnote(dol(contents))


def ordered_list_with_lcromnum(liconts):
    """lcromnum: lowercase Roman numerals"""
    return ordered_list(liconts, {"type": "i"})


def ordered_list_with_lcromalpha(liconts):
    """lcromnum: lowercase Roman (Latin) alphabet"""
    return ordered_list(liconts, {"type": "a"})


def ordered_list_with_lcromalpha_ws(weird_start: int, liconts):
    """lcromnum: lowercase Roman (Latin) alphabet. ws: weird start"""
    return ordered_list(liconts, {"type": "a", "start": f"{weird_start}"})


def ordered_list_with_warabnum(liconts):
    """warabnum: Western Arabic numberals"""
    # Usually the default for ordered lists, but just to ask for it explicitly ...
    return ordered_list(liconts, {"type": "1"})


def pseudo_heading(contents):
    return aht_html.span_c(dol(contents), "yeivin-pseudo-heading")


def para_with_initial_uah(uah_contents, rest_of_para_contents, pre=None):
    """paragraph with initial underline as heading"""
    pre = pre or []
    psh = pseudo_heading(uah_contents)
    return para([*pre, psh, ". ", *rest_of_para_contents])


def para_with_romnum_and_initial_uah(romnum, uah_contents, rest_of_para_contents):
    """paragraph with roman numeral and initial underline as heading"""
    pre = [f"({romnum}) "]
    return para_with_initial_uah(uah_contents, rest_of_para_contents, pre=pre)


def emdash():
    return sd.THSP + "\N{EM DASH}" + sd.THSP  # — em dash; nowrap needed?


# def endash(): return '\N{EN DASH}'  # – en dash
def hairsp():
    return subpriv.hairsp()


def thsp():
    return subpriv.thsp()


def thspc():
    return subpriv.thspc()


def thspp():
    return subpriv.thspp()


def thspq():
    return subpriv.thspq()


def saa():
    return "↑"  # U+2191: UPWARDS ARROW (saa: Same As Above)


def plural(contents):
    return contents, hairsp(), "s"  # nowrap needed?


#
def alef(cap=False):
    return hlp.rom("alef", cap)


def bet(cap=False, as_str=False):
    return hlp.rom("bet", cap, as_str)


def vet(cap=False, as_str=False):
    return hlp.rom("vet", cap, as_str)


def gimel(cap=False):
    return hlp.rom("gimel", cap)


def dalet(cap=False):
    return hlp.rom("dalet", cap)


def he(cap=False, as_str=False):
    return hlp.rom("he", cap, as_str)


def waw(cap=False, as_str=False):
    return hlp.rom("waw", cap, as_str)


def zayin(cap=False):
    return hlp.rom("zayin", cap)


def xet(cap=False):
    return hlp.rom("ḥet", cap)


def tet(cap=False):
    return hlp.rom("ṭet", cap)


def yod(cap=False):
    return hlp.rom("yod", cap)


def kaf(cap=False, as_str=False):
    return hlp.rom("kaf", cap, as_str)


def lamed(cap=False, as_str=False):
    return hlp.rom("lamed", cap, as_str)


def mem(cap=False):
    return hlp.rom("mem", cap)


def nun(cap=False):
    return hlp.rom("nun", cap)


def ayin(cap=False):
    return hlp.rom("ayin", cap)


def tsade(cap=False):
    return hlp.rom("ṣade", cap)


def qof(cap=False):
    return hlp.rom("qof", cap)


def resh(cap=False, as_str=False):
    return hlp.rom("resh", cap, as_str)


def shin(cap=False):
    return hlp.rom("shin", cap)


def tav(cap=False):
    return hlp.rom("tav", cap)


#
def shewa(cap=False, as_str=False):
    return hlp.rom("shewa", cap, as_str)


def dagesh(cap=False, as_str=False):
    return hlp.rom("dagesh", cap, as_str)


def mappiq(cap=False, as_str=False):
    return hlp.rom("mappiq", cap, as_str)


def dagesh_xazaq(cap=False, as_str=False):
    return hlp.rom("dagesh ḥazaq", cap, as_str)


def xazaq(cap=False, as_str=False):
    return hlp.rom("ḥazaq", cap, as_str)


def qal(cap=False, as_str=False):
    return hlp.rom("qal", cap, as_str)


def rafe(cap=False, as_str=False):
    return hlp.rom("rafe", cap, as_str)


# slightly surprising that "rafe" lacks a final 'h' (e.g. page 260 #350)
def xatef(cap=False, as_str=False):
    return hlp.rom("ḥaṭef", cap, as_str)


def x_qamets(mwcap="mwcap-type-lower-case"):
    return hlp.mwrom("ḥaṭef qameṣ", mwcap)


def x_patax(mwcap="mwcap-type-lower-case"):
    return hlp.mwrom("ḥaṭef pataḥ", mwcap)


def x_shewa(cap=False):
    return hlp.rom("ḥaṭef shewa", cap)


def x_segol(cap=False):
    return hlp.rom("ḥaṭef segol", cap)


def qamets_g(cap=False):
    return hlp.rom("qameṣ gadol", cap)


def qamets_x_paren_qamets_q():
    return hlp.rom("qameṣ ḥaṭuf"), " ", hlp.paren(hlp.rom("qameṣ qaṭan"))


def xatuf_paren_qatan():
    return hlp.rom("ḥaṭuf"), " ", hlp.paren(qatan())


def qamets(cap=False):
    return hlp.rom("qameṣ", cap)


def qibbuts(cap=False):
    return hlp.rom("qibbuṣ", cap)


def tsere(cap=False):
    return hlp.rom("ṣere", cap)


def patax(cap=False, as_str=False):
    return hlp.rom("pataḥ", cap, as_str)


def segol(cap=False):
    return hlp.rom("segol", cap)


def xolem(cap=False):
    return hlp.rom("ḥolem", cap)


def xireq(cap=False):
    return subpriv.xireq(cap)


def shureq(cap=False, as_str=False):
    return hlp.rom("shureq", cap, as_str)


#
def gaya(cap=False, as_str=False):
    return hlp.rom("gaʿya", cap, as_str)


def metheg(cap=False):
    return hlp.rom("metheg", cap)


def silluq(cap=False):
    return hlp.rom("silluq", cap)


def atnax(cap=False):
    return hlp.rom("atnaḥ", cap)


def pashta(cap=False):
    return hlp.rom("pashṭa", cap)


def tevir(cap=False):
    return hlp.rom("tevir", cap)


def yetiv(cap=False):
    return hlp.rom("yetiv", cap)


def metigah(cap=False):
    return hlp.rom("metigah", cap)


def zaqef(cap=False):
    return hlp.rom("zaqef", cap)


def gershayim(cap=False):
    return hlp.rom("gershayim", cap)


def geresh(cap=False):
    return hlp.rom("geresh", cap)


def geresh_muqdam(cap=False):
    return hlp.rom("geresh muqdam", cap)


def pazer(cap=False):
    return hlp.rom("pazer", cap)


def darga(cap=False):
    return hlp.rom("darga", cap)


def revia(cap=False):
    return hlp.rom("revia", cap)


def revia_gadol(cap=False):
    return hlp.rom("revia gadol", cap)


def revia_qatan(cap=False):
    return hlp.rom("revia qaṭan", cap)


def gadol(cap=False):
    return hlp.rom("gadol", cap)


def qatan(cap=False):
    return hlp.rom("qaṭan", cap)


def tsinnor(cap=False):
    return hlp.rom("ṣinnor", cap)


def merka(cap=False):  # translit-ok
    return hlp.rom("merka", cap)  # both כ and כּ get 'k'  # translit-ok


def illuy(cap=False):
    return hlp.rom("ʿilluy", cap)


# The spelling ʿilluy is attested in section 358, page 264.
def tifxa(cap=False):
    return hlp.rom("ṭifḥa", cap)


def mayela(cap=False):
    return hlp.rom("mayela", cap)


def munax(cap=False):
    return hlp.rom("munaḥ", cap)


def legarmeh(cap=False):
    return hlp.rom("legarmeh", cap)


def paseq(cap=False):
    return hlp.rom("paseq", cap)


def mehuppak(cap=False):  # translit-ok
    return hlp.rom("mehuppak", cap)  # translit-ok


def azla(cap=False):
    return hlp.rom("azla", cap)


def azla_legarmeh(cap=False):
    return hlp.rom("azla legarmeh", cap)


def telisha(cap=False):
    return hlp.rom("telisha", cap)


def telisha_gedolah(mwcap="mwcap-type-lower-case"):
    return hlp.mwrom("telisha gedolah", mwcap)


def telisha_qetannah(cap=False):
    return hlp.rom("telisha qeṭannah", cap)


def zarqa(cap=False):
    return hlp.rom("zarqa", cap)


def maqqef(cap=False, as_str=False):
    return hlp.rom("maqqef", cap, as_str)


#
def mater_lectionis(cap=False):
    return subpriv.mater_lectionis(cap)


def ketiv(cap=False):
    return hlp.rom("ketiv", cap)


def qere(cap=False):
    return hlp.rom("qere", cap)


# The spelling qere (rather than qeri) is attested in section 93, page 52.
def dexiq(cap=False, as_str=False):
    return hlp.rom("deḥiq", cap, as_str)


def dexi(cap=False):
    return hlp.rom("deḥi", cap)


def ate_meraxiq(cap=False):
    return hlp.rom("ate meraḥiq", cap)


def begad_kefat(cap=False):
    return hlp.rom("begad-kefat", cap)


def xillufim(cap=False):
    return hlp.rom("ḥillufim", cap)


def sefer_ha_xillufim():
    return hlp.rom("Sefer ha-Ḥillufim")


def diqduqe():
    return hlp.rom("Diqduqe ha-Ṭeʿamim")


def quntrese():
    return hlp.rom("Qunṭrese ha-Masorah")


def tuv_taam():
    return hlp.rom("Ṭuv Ṭaʿam")


def horayat():
    return hlp.rom("Horayat ha-Qore")


def cet_sofer():
    return hlp.rom("ʿEt Sofer")


def yequtiel_hn():
    return f"{yequtiel()} ha-Naqdan"


def yequtiel():
    return "Yequtiʾel"


def cgaya(as_str=False):
    return gaya(cap=True, as_str=as_str)


def cshewa(as_str=False):
    return shewa(cap=True, as_str=as_str)


def shewas():
    return plural(shewa())


def gayas():
    return plural(gaya())


def methegs():
    return plural(metheg())


def maqclo(cap=False, as_str=False):
    return maqqef(cap=cap, as_str=as_str), "-closed"


def sheclo(cap=False, as_str=False):
    return shewa(cap=cap, as_str=as_str), "-closed"


def mclv(cap=False, as_str=False):
    return (
        *maqclo(cap=cap, as_str=as_str),
        ", ",
        subpriv.maybe_cap(cap, "long-vowelled"),
    )


def sclv(cap=False, as_str=False):
    return (
        *sheclo(cap=cap, as_str=as_str),
        ", ",
        subpriv.maybe_cap(cap, "long-vowelled"),
    )


def sclv_abbr(cap=False, as_str=False):
    return *sheclo(cap=cap, as_str=as_str), ", ", subpriv.maybe_cap(cap, "long-vow.")


def alvb_simshewa():
    return "a long vowel before ", *simshewa()


def slv():
    return "syllable with a long vowel"


def ssv():
    return "syllable with a short vowel"


def gaya_cs(cap=False):
    return gaya(cap), " on a closed syllable"


def gaya_os(cap=False):
    return gaya(cap), " on an open syllable"


def gaya_osr(cap=False):
    return gaya(cap), "-", osr()


def rom_bkl(as_str=False):
    return three_comma_or(bet(as_str=as_str), kaf(as_str=as_str), lamed(as_str=as_str))


def three_comma_or(part1, part2, part3):
    return part1, ", ", part2, ", or ", part3


def three_comma_and(part1, part2, part3):
    return part1, ", ", part2, ", and ", part3


def four_comma_and(part1, part2, part3, part4):
    return part1, ", ", part2, ", ", part3, ", and ", part4


def comma_list_of_heb_ahw_or_y():
    return hlp.comma_list_of_bdis("א", "ה", "ו", "or י")


def comma_list_of_heb_hw_or_y():
    return hlp.comma_list_of_bdis("ה", "ו", "or י")


def pat_mitqatlim():
    return "מִתְקַטְּלִים", "מִתְ-קַ_-טְּלִים"


def pat_mitpalpelim():
    return "מִתְפַּלְפְּלִים", "מִתְ-פַּלְ-פְּלִים"


def pat_mitpaalim():
    return "מִתְפַּעֲלִים", "מִתְ-פַּ-עֲלִים"


def hbostr_pat_mitbarekhim():
    return "מִתְבָּרְכִים"


def hbo_pat_mitbarekhim():
    return hlp.hbo(hbostr_pat_mitbarekhim())


def pat_meqatlim():
    return hlp.hbo("מְקַטְּלִים")


def pat_mefalpelim():
    return hlp.hbo("מְפַלְפְּלִים")


def pat_mefaalim():
    return hlp.hbo("מְפַעֲלִים")


def pat_mevarekhim():
    return hlp.hbo("מְבָרְכִים")


def hbostr_pat_hapoalim():
    return "הַפּוֹעֲלִים"


def hbo_pat_hapoalim():
    return hlp.hbo(hbostr_pat_hapoalim())


def simshewa(as_str=False):
    return "simple ", shewa(as_str=as_str)


def silshewa():
    return "silent ", shewa()


def vocshewa():
    return "vocal ", shewa()


def simvocshewa():
    return "simple ", vocshewa()


def vshewa():
    return "v-", shewa()


def mgaya():
    return "musical ", gaya()


def pgaya():
    return "phonetic ", gaya()


def simple_or_xatef():
    return *simshewa(), " or ", x_shewa()


def fr1():
    return hlp.abbr_tit("FR1", "fully regular pattern #1: " + pat_mitqatlim()[0])


def fr2():
    return hlp.abbr_tit("FR2", "fully regular pattern #2: " + pat_mitpalpelim()[0])


def fr3():
    return hlp.abbr_tit("FR3", "fully regular pattern #3: " + pat_mitpaalim()[0])


def afr1():
    return hlp.abbr_tit("AFR1", "almost fully regular pattern #1")


def afr2():
    return hlp.abbr_tit(
        "AFR2", "almost fully regular pattern #2: " + hbostr_pat_hapoalim()
    )


def afr3():
    return hlp.abbr_tit(
        "AFR3", "almost fully regular pattern #3: " + hbostr_pat_mitbarekhim()
    )


def afr4():
    return hlp.abbr_tit("AFR4", "almost fully regular pattern #4")


def fip():
    return hlp.abbr_tit_sc("FIP", fip_explanation())


def fip_explanation():
    return "first [of an] identical pair [of letters]"


def horayat_d(hpage: int, dpage: int):
    return horayat(), f" p. {hpage} (Dérenbourg, 1870, p. {dpage})"


def diqduqe_baer(num: int):
    return [diqduqe(), f" (Baer-Strack 1879, #{num})"]


def diqduqe_dotan_sec_num(num: int):
    return diqduqe_dotan_sec_str(f"section {num}")


def diqduqe_dotan_sec_str(string: str):
    return [diqduqe(), f" (Dotan 1967, {string})"]


def ms_aleppo():
    return mss.sigil("A")


def ms_b_4445():
    return mss.sigil("B")


def ms_cairo():
    return mss.sigil("C")


def ms_lenin():
    return mss.sigil("L")


def ms_lenin_01():
    return mss.sigil("L1")


def ms_lenin_02():
    return mss.sigil("L2")


def ms_lenin_06():
    return mss.sigil("L6")


def ms_lenin_10():
    return mss.sigil("L10")


def ms_lenin_13():
    return mss.sigil("L13")


def ms_lenin_15():
    return mss.sigil("L15")


def ms_lenin_18():
    return mss.sigil("L18")


def ms_lenin_20():
    return mss.sigil("L20")


def ms_ny_jts():
    return mss.sigil("N")


def ms_p():
    return mss.sigil("P")


def ms_s_507():
    return mss.sigil("S")


def ms_s1_1053():
    return mss.sigil("S1")


def ms_reuch():
    return mss.sigil("R")


def ms_a_and_c(joiner=", "):
    return ms_aleppo(), joiner, ms_cairo()


def ms_a_and_l(joiner=", "):
    return ms_aleppo(), joiner, ms_lenin()


def ms_a_and_l6(joiner=", "):
    return ms_aleppo(), joiner, ms_lenin_06()


def ms_a_and_n(joiner=", "):
    return ms_aleppo(), joiner, ms_ny_jts()


def ms_a_and_s():
    return ms_aleppo(), ", ", ms_s_507()


def ms_a_and_s1():
    return ms_aleppo(), ", ", ms_s1_1053()


def ms_c_and_s1():
    return ms_cairo(), ", ", ms_s1_1053()


def ms_b_and_l():
    return ms_b_4445(), ", ", ms_lenin()


def ms_b_and_s1(joiner=", "):
    return ms_b_4445(), joiner, ms_s1_1053()


def ms_a_x_patax(letter):
    return xxx_hbo_in_parens(ms_aleppo(), letter + hpo.XPATAX)


def xxx_hbo_in_parens(xxx, hbox):
    sxxx = aht_html.flatten_nn(xxx)
    return hlp.span_ltr(hlp.paren_tt([*sxxx, " ", hlp.hbo(hbox)]))


def join_with_paseq(worda, wordb):
    return worda + subpriv.SP_PASEQ_SP + wordb


def end_with_paseq(word):
    return word + subpriv.SP_PASEQ


def explain_paseq():
    we_use = "I use a double vertical bar for "
    to_dist = ", to distinguish it from ", legarmeh(), "."
    return we_use, paseq(), *to_dist


def irrelevant_ketiv(xloc, hbo_contents, the_ketiv: str):
    return subpriv.irrelevant_ketiv(xloc, hbo_contents, the_ketiv, ketiv())


def itm():
    return subpriv.itm()


def alhatorah():
    return subpriv.alhatorah()


def mam():
    return subpriv.mam()


def mamdoc(file_part_of_url):
    return subpriv.mamdoc(file_part_of_url)


def osr():
    return hlp.abbr_tit_sc("OSR", "".join(osr_explanation(as_str=True)))


def osr_case(as_str=False):
    return "[case of a ", *sclv(as_str=as_str), " syllable]"


def osr_explanation(as_str=False):
    return ["[on an] open syllable [or on the] related ", *osr_case(as_str=as_str)]


def superfluous_waw(the_ketiv: str, the_qere: str):
    return subpriv.superfluous_waw(the_ketiv, the_qere, waw(), ketiv(), qere())


def surprising_long_xiriq(hbo_contents):
    return subpriv.surprising_long_xiriq(hbo_contents, yod())


def cmn_347_lcromnum_i():
    return [cgaya(), " on initial ", he(), " with ", patax(), " before ", mem()]


def cmn_347_lcromnum_ii():
    return [cgaya(), " on conjunctive ", waw(), " pointed as ", shureq()]


def cmn_347_lcromnum_iii():
    return [cgaya(), " on other short vowels"]


def cmn_354_lcromnum_i():
    return [cgaya(), " on a Guttural-closed Syllable"]


def cmn_354_lcromnum_ii():
    return [cgaya(), " in Forms of היה and חיה"]


def cmn_388_lcromnum_i():
    return [x_shewa(cap=True), " Used for Morphological Reasons"]


def cmn_388_lcromnum_ii():
    return [x_shewa(cap=True), " Used for Phonetic Reasons"]


def cmn_403_lcromnum_i():
    return [dexiq(cap=True), " after ", segol()]


def cmn_403_lcromnum_ii():
    return [dexiq(cap=True), " after ", qamets()]


def cmn_407_lcromnum_i():
    return ["After ", qamets()]


def cmn_407_lcromnum_ii():
    return ["After long vowels other than ", qamets()]


def cmn_407_lcromnum_iii():
    return ["Other situations"]


def _cap(fn):
    return lambda: fn(cap=True)


PART_2_NAME = "Part II: The Masorah"
PART_3_NAME = "Part III: The Accents"
PART_4_NAME = "Appendix: Shewa and Dagesh"
A_SEC_IN_PART_2 = f"(a section in Yeivin ITM {PART_2_NAME})"
A_SEC_IN_PART_3 = f"(a section in Yeivin ITM {PART_3_NAME})"
A_SEC_IN_PART_4 = f"(a section in Yeivin ITM {PART_4_NAME})"
ITM_TITLE = subpriv.ITM_TITLE
ITM_PRESENTS_KQ_IN_MANU_STYLE = subpriv.itm_presents_kq_in_manu_style(ketiv(), qere())
FK_6_22 = "@1K 6:22", "אֲֽשֶׁר־לַדְּבִ֖יר"
TITSEC_HEADING_319 = [cgaya(), " on a Closed, Short-vowelled Syllable"]
TITSEC_HEADING_319_ORIG = [cgaya(), " on a Closed Syllable"]
_DOLLAR_SUB_DISPATCH = {
    "$alef": alef(),
    "$ayin": ayin(),
    "$Dagesh": _cap(dagesh)(),
    "$dagesh": dagesh(),
    "$dagesh_xazaq": dagesh_xazaq(),
    "$Dexiq": _cap(dexiq)(),
    "$dexiq": dexiq(),
    "$Gaya": _cap(gaya)(),
    "$gaya": gaya(),
    "$Gaya_cs": _cap(gaya_cs)(),
    "$gaya_cs": gaya_cs(),
    "$Gaya_os": _cap(gaya_os)(),
    "$gaya_os": gaya_os(),
    "$Gaya_osr": _cap(gaya_osr)(),
    "$gaya_osr": gaya_osr(),
    "$gayas": gayas(),
    "$itm": itm(),
    "$maqqef": maqqef(),
    "$mem": mem(),
    "$mgaya": mgaya(),
    "$ms_aleppo": ms_aleppo(),
    "$Pashta": _cap(pashta)(),
    "$pashta": pashta(),
    "$pgaya": pgaya(),
    "$qere": qere(),
    "$resh": resh(),
    "$revia": revia(),
    "$Shewa": _cap(shewa)(),
    "$shewa": shewa(),
    "$shewas": shewas(),
    "$silshewa": silshewa(),
    "$simshewa": simshewa(),
    "$vocshewa": vocshewa(),
    "$vshewa": vshewa(),
    "$x_qamets": x_qamets(),
    "$x_shewa": x_shewa(),
    "$xatef": xatef(),
    "$zarqa": zarqa(),
}

# Although ITM uses the digraph sh for ש,
# ITM avoids the digraph ts for צ, using ṣ. E.g. in ṣere.
