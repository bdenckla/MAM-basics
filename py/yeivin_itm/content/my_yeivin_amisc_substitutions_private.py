import py_html.legacy_html as aht_html
import mb_cmn.str_defs as sd
import yeivin_itm.helpers as hlp


def hairsp():
    return sd.HAIRSP


def thsp():
    return sd.THSP


def thspc():
    return sd.THSP + ","


def thspp():
    return sd.THSP + "."


def thspq():
    return sd.THSP + "?"


def xireq(cap=False):
    return hlp.rom("ḥireq", cap)


def mater_lectionis(cap=False):
    return hlp.rom("mater lectionis", cap)


def itm():
    return hlp.abbr_tit_sc("ITM", ITM_TITLE)


def superfluous_waw(the_ketiv: str, the_qere: str, in_waw, in_ketiv, in_qere):
    return [
        "Most manuscripts and printed texts note this word’s superfluous ",
        in_waw,
        ", either compactly, e.g. ",
        hlp.single_angle_quotes_hh("יתיר ו̇"),
        ", or fully, as a ",
        in_ketiv,
        f" of {the_ketiv} corresponding a ",
        in_qere,
        " of ",
        hlp.hbo(the_qere),
        thspp(),
    ]


def irrelevant_ketiv(xloc, hbo_contents, the_ketiv: str, in_ketiv):
    return [
        "The ",
        in_ketiv,
        " of ",
        hlp.lhbo(xloc, hbo_contents),
        f" is {the_ketiv}. "
        "I note this merely to be thorough; it is irrelevant to the point at hand.",
    ]


def surprising_long_xiriq(hbo_contents, in_yod):
    return [
        "In ",
        hlp.hbo(hbo_contents),
        thspc(),
        " why is ",
        xireq(),
        " without a ",
        in_yod,
        " vowel letter ",
        hlp.paren(mater_lectionis()),
        " considered a long vowel?",
    ]


def maybe_cap(cap, string):
    return string.capitalize() if cap else string


def mam():
    return hlp.abbr_tit_sc("MAM", "Miqra According to the Masorah")


def alhatorah():
    url = "https://mg.alhatorah.org/"
    return aht_html.anchor("Al-Hatorah", {"href": url})


def mamdoc(file_part_of_url):
    url = "https://bdenckla.github.io/MAM-with-doc/" + file_part_of_url
    anc_contents = mam(), " documentation"
    return aht_html.anchor(anc_contents, {"href": url})


def itm_presents_kq_in_manu_style(in_ketiv, in_qere):
    return [
        "In ",
        itm(),
        ", the ",
        _ketiv_qere(),
        " is presented in manuscript style: ",
        in_qere,
        " points on ",
        in_ketiv,
        " letters corresponding to unpointed ",
        in_qere,
        " letters.",
    ]


SP_PASEQ = sd.NBSP + sd.DOUB_VERT_LINE
SP_PASEQ_SP = SP_PASEQ + sd.NBSP
ITM_TITLE = "Introduction to the Tiberian Masorah"


def _ketiv_qere(cap=False):
    return hlp.rom("ketiv/qere", cap)
