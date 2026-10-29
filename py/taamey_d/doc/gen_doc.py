"""Write Taamey D's documentation pages, Taamey_D.html and Xolam_xaser_for_alef.html.

Both pages go to gh-pages/taamey-d/.  This package was restructured on 2026-10-28
from hbofonts' main_gen_doc.py and its py_gen_doc package.

The comparison images under gh-pages/taamey-d/img/comparison/ were rendered once,
by hbofonts' main_render_comparison_svgs.py, from the records that
comparison_cells() returns.  They are frozen, so write_pages() writes neither page
if a comparison cell's text, highlight or spacing no longer matches its image's
record in that directory's PROVENANCE.json.
"""

import json
import string

from mb_cmn import file_io, paths
from taamey_d.doc import taamey_d_page, xx_for_alef_page
from taamey_d.doc.html_helpers import att, span, xtable_rtl, xtable_row
from taamey_d.doc.html_helpers import xtable_data_cell, to_str


def _romanized(text):
    return span("romanized", text.translate(_ROM_TRANS_TABLE))


def _unicode_code_point(text):
    return _unicode_character_name("u-" + text)


def _unicode_character_name(text):
    return span("unicode-code-point-name", text)


def _small_caps(text):
    return span("small-caps", text)


def _flexwords(oom_fw):
    # oom_fw: one or many flexwords
    # One flexword is a string or a dict with keys 'chars' & 'abbrev'
    # Many flexwords is a list or tuple of flexwords
    if isinstance(oom_fw, (str, dict)):
        return (oom_fw,)
    assert isinstance(oom_fw, (list, tuple))
    return oom_fw


def _flexword_dict(flexword):
    if isinstance(flexword, str):
        return dict(chars=flexword)
    assert isinstance(flexword, dict)
    return flexword


def _four_font_display(variant, display_id, oom_fw):
    header_label = variant["table_header_label"]
    data_rows = tuple(
        _four_font_row(variant, display_id, row_number, fw)
        for row_number, fw in enumerate(_flexwords(oom_fw), start=1)
    )
    sum_of_data_rows = sum(data_rows, tuple())
    header_items = (header_label,) + tuple(hdr for _, hdr in _COMPARISON_FONTS)
    return to_str(xtable_rtl(header_items, sum_of_data_rows))


def _four_font_row(variant, display_id, row_number, flexword):
    css_class = variant["css_class"]
    fw_dic = _flexword_dict(flexword)
    chars = fw_dic["chars"]
    row_attrs = fw_dic.get("attrs") or {}
    cells = tuple(
        _comparison_cell(display_id, row_number, font_key, flexword)
        for font_key, _ in _COMPARISON_FONTS
    )
    rows = (xtable_data_cell(chars, {"class": css_class}),) + tuple(
        xtable_data_cell(_comparison_img(cell), {"class": cell["css_class"]})
        for cell in cells
    )
    rows2 = tuple((row, "\n    ") for row in rows)
    sum_of_rows2 = sum(rows2, tuple())
    return "\n    ", xtable_row(sum_of_rows2, row_attrs)


def _comparison_cell(display_id, row_number, font_key, flexword):
    # One comparison font's cell of a four-font row, which shows an image
    # that hbofonts' main_render_comparison_svgs.py rendered once from this record.
    fw_dic = _flexword_dict(flexword)
    markup = fw_dic.get("abbrev") or fw_dic["chars"]
    pre, opener, rest = markup.partition(_ATTENTION_OPEN)
    if opener:
        mid, closer, post = rest.partition(_ATTENTION_CLOSE)
        assert closer, markup
        highlight = len(pre), len(pre) + len(mid)
    else:
        mid, post = "", ""
        highlight = None
    text = pre + mid + post
    assert not set(text) & set('<>&"'), markup
    row_attrs = fw_dic.get("attrs") or {}
    assert row_attrs in ({}, _WIDE_LETTER_SPACING_ATTRS), row_attrs
    return dict(
        name=f"{display_id}-r{row_number}-{font_key}",
        display_id=display_id,
        row_number=row_number,
        font_key=font_key,
        css_class="comparison-" + font_key,
        text=text,
        highlight=highlight,
        wide_letter_spacing=row_attrs == _WIDE_LETTER_SPACING_ATTRS,
    )


def _comparison_img(cell):
    src = f"img/comparison/{cell['name']}.svg"
    return f'<img src="{src}" alt="{cell["text"]}" lang="he">'


def comparison_cells():
    """Return a record for each comparison cell of Taamey_D.html, in page order.

    hbofonts' one-time main_render_comparison_svgs.py rendered each cell's image from
    its record on 2026-10-28, before the move; the images are frozen since.
    """
    return [
        _comparison_cell(display_id, row_number, font_key, fw)
        for display_id, oom_fw in _comparison_displays().items()
        for row_number, fw in enumerate(_flexwords(oom_fw), start=1)
        for font_key, _ in _COMPARISON_FONTS
    ]


def _check_comparison_images():
    # The images were rendered once and are frozen, so an edit to a display's
    # words would leave its images stale. Refuse to write the page then.
    with open(_COMPARISON_PROVENANCE, encoding="utf-8") as infp:
        records = {rec["file"]: rec for rec in json.load(infp)["images"]}
    cells = comparison_cells()
    assert set(records) == {cell["name"] + ".svg" for cell in cells}
    for cell in cells:
        rec = records[cell["name"] + ".svg"]
        highlight = None if cell["highlight"] is None else list(cell["highlight"])
        found = (
            rec["font"],
            rec["text (code points)"],
            rec["highlighted code points (start, end)"],
            rec["letter spacing at the right of each cluster (font units)"] != 0,
        )
        expected = (
            cell["font_key"],
            [f"U+{ord(c):04X}" for c in cell["text"]],
            highlight,
            cell["wide_letter_spacing"],
        )
        assert found == expected, f"{cell['name']} differs from its frozen image"


def _wide_letter_spacing(chars):
    return (chars, dict(chars=chars, attrs=_WIDE_LETTER_SPACING_ATTRS))


def _displays(variant):
    return {
        display_id: _four_font_display(variant, display_id, oom_fw)
        for display_id, oom_fw in _comparison_displays().items()
    }


def _comparison_displays():
    qupo_panay_qupo_mitaxat = (
        att("פָּנָֽ͏ַ֗י׃", "נָֽ͏ַ֗"),
        att("מִתָּ֑͏ַ֜חַת", "תָּ֑͏ַ֜"),
    )
    overburdened_greatly = dict(chars="תִשְׁתַּחֲוֶ֥֣ה", abbrev="...חֲוֶ֥֣ה")
    return dict(
        dis_qq_with_mer_or_mun="כׇּ֥ קׇ֣",
        dis_geresh_tg_and_gershayim_tg=(
            "שֻׁ֜֠בוּ",
            "וּ֜֠לְאֵ֜֠לֶּה",
            "זֶ֞֠ה",
            "זֹ֞֠את",
            "קִ֞֠רְב֞֠וּ",
        ),
        dis_xolam_xaser=("בְּ֠נֹ֠פֶךְ", "וַיֹּ֩אֶל֩", "וָרֹ֒מַח֒"),
        dis_revia_mugrash="גַּ֝֗ם",
        dis_lamed_ascender=("בְּשַׁלְוָ֞ה", "לְֽיֹ֫דְעָ֥י", "לׅׄוּלֵׅׄ֗אׅׄ"),
        dis_lamed_ascender_indirect="אֱל֙וֹהַּ֙",
        dis_dexi="לֵֽ֭ שֶׁ֣֭",
        dis_stress_helper_dexi=("יָ֭רָ֭ק", "כׇּל־קֹ֭וֶ֭יךָ"),
        dis_ayin_descender_1="עֹזֵֽר",
        dis_ayin_descender_2="עָ֘נִ֤י",
        dis_zizi_zazi=("אָנֹ֘כִי֮", "אָנֹ֮כִי֮"),
        dis_LAIO_pat_ger=_wide_letter_spacing("לִַ֜ם"),
        dis_LAEO_pat_ger="לְַ֜מָה",
        dis_LAOcE_pat_ger="לַ֜͏ְמָה",
        dis_QUPO_panay_QUPO_mitaxat=qupo_panay_qupo_mitaxat,
        dis_other_dualcant="תִּֿגְנֹֽ֔ב",
        dis_overburdened_greatly=overburdened_greatly,
        dis_overburdened=("הֶעֱוָ֣ה", "אֲזֵנֶ֑ךָ", "יָוָ֑ן"),
        dis_descenders=("כַּ֣ף", "זָ֛ךְ"),
    )


_SBL_HEBREW = _small_caps("Sbl") + " Hebrew"
_EZRA_SIL = "Ezra " + _small_caps("Sil")
# Each comparison font's key, which names its images and its cells' class,
# and its column header.
_COMPARISON_FONTS = (
    ("taamey-frank-clm", "Taamey Frank"),
    ("sbl-hebrew", _SBL_HEBREW),
    ("ezra-sil", _EZRA_SIL),
)
_PAGES_DIR = paths.gh_pages_dir() / "taamey-d"
_COMPARISON_PROVENANCE = _PAGES_DIR / "img" / "comparison" / "PROVENANCE.json"
_ATTENTION_OPEN = '<span class="attention">'
_ATTENTION_CLOSE = "</span>"
_WIDE_LETTER_SPACING_ATTRS = {"class": "wide-letter-spacing"}
_ROM_TRANS_TABLE = str.maketrans(
    {
        "_": " ",
        "x": "ḥ",
        "X": "Ḥ",
        "7": "·",  # middle dot aka interpunct
        "8": "-",
        "9": "kh",  # used to be 'ḳ'
    }
)
_ROMANIZATIONS_K = [
    "dexi",
    "yetiv",
    "pashta",
    "qadma",
    "meteg",
    "siluq",
    "pazer",
    "pazer_gadol",
    "qarney_para",
    "etnaxta",
    "atnax",
    "munax",
    "geresh",
    "gershayim",
    "geresh_muqdam",
    "zarqa",
    "tsinor",
    "tsinnorit",
    "revia",
    "revia_mugrash",
    "segolta",
    "telisha_gedolah",
    "telisha_qetana",
    "yerax_ben_yomo",
    "yerax",
    "ben_yomo",
    "galgal",
    "ole_veyored",
    "iluy",
    "zaqef_qatan",
    "mahapa9",
    "maqaf",
    #
    "xataf",
    "qatan",
    "gadol",
    "elyon",
    "taxton",
    "sof_pasuq",
    "sifrei_emet",
    "tiqqunim",
    "siddur",
    "shuvu",
    "ribot",
    "havot",
    "befihu",
    "qere",
    "ketiv",
    "ish",
    "zot",
    "shalosh",
    "sorer",
    "tafus",
    "shosetiy",
    "avonotayv",
    "hayuqax",
    "avono",
    "roxav",
    "shomer",
    "melot",
    "veyom",
    "oholo",
    "yerushalayemah",
    "uleleh",
    "qirvu",
    "mitaxat",
    "panay",
    "ano9iy",
    "shamayim",
    "seyvah",
    "yom",
    #
    "yavo7u",
    "bevo7o",
    "umlo7ah",
    "lero7ey",
    #
    "al8bomotey",
    #
    "mer9a",
    "atnax_hafu9",
    "yissa9ar",
    "roshe9",
    "tipexa",
    "tarxa",
    #
    "dagesh",
    "Dagesh",
    "dagesh_xazaq",
    "rafeh",
    "varika",
    "xolam",
    "xolam_male",
    "xm",
    "xolam_xaser",
    "Xolam_xaser",
    "xx",
    #
    "xiriq",
    "tsere",
    "sheva",
    "sheva_na",
    "patax",
    "Patax",
    "qamats",
    "qamats_gadol",
    "qamats_qatan",
    "Qamats_qatan",
    "xataf_qamats_qatan",
    "xataf_qamats",
    "qubuts",
    #
    "alef",
    "alef_xolam",
    "alef8vav",
    "gimel",
    "dalet",
    "he",
    "vav",
    "vav_xolam",
    "shuruq",
    "zayin",
    "yod",
    "lamed",
    "mem",
    "nun",
    "same9",
    "ayin",
    "qof",
    "resh",
    "shin",
    "sin",
    "kaf",
]
_ROMANIZATIONS_KV = {k: _romanized(k) for k in _ROMANIZATIONS_K}
_SYMDEFS = {
    "h2_title_distinctive_features": "Distinctive features",
    "h2_title_challenging_cases": "Challenging cases",
    "h2_title_alef_xolam": "The " + _ROMANIZATIONS_KV["alef_xolam"] + " vowel",
    "h2_title_floating_xx": "Floating " + _ROMANIZATIONS_KV["xolam_xaser"],
    "h2_title_notes_on_the_limited_corpus": "Notes on the limited corpus",
    "h3_title_qupo_words": _small_caps("Qupo") + " words",
    #
    "Galgal_vel_Jerax": _romanized("Galgal") + " vel " + _romanized("Jèrax"),
    #
    "mer_dot": _romanized("mer."),  # short for mer9a
    "mun_dot": _romanized("mun."),  # short for munax
    #
    "Taamey_D": "Taamey&nbsp;D",
    #
    **_ROMANIZATIONS_KV,
    #
    "MAM": _small_caps("mam"),
    "cap_MAM": _small_caps("Mam"),
    "UXLC": _small_caps("uxlc"),
    "cap_UXLC": _small_caps("Uxlc"),
    "WLC": _small_caps("wlc"),
    "BHS": _small_caps("bhs"),
    "cap_BHS": _small_caps("Bhs"),
    "LC": _small_caps("lc"),
    #
    "TG": _small_caps("tg"),
    "ML": _small_caps("ml"),
    "LPA": _small_caps("lpa"),
    "XML": _small_caps("xml"),
    "CSS": _small_caps("css"),
    #
    "cap_CLM": _small_caps("Clm"),
    "SBL_Hebrew": _SBL_HEBREW,
    "Ezra_SIL": _EZRA_SIL,
    #
    "LAEO": _small_caps("laeo"),
    "LAOcE": _small_caps("lao-e"),
    "LAOcI": _small_caps("lao-i"),
    "QUPO": _small_caps("qupo"),
    "cap_QUPO": _small_caps("Qupo"),
    "QUcPO": _small_caps("qu-po"),
    #
    "u_xxfv": _unicode_code_point("holam haser for vav"),
    "u_xxfv_short": _unicode_code_point("hhfv"),
    "u_zinor": _unicode_code_point("zinor"),  # translit-ok
    "u_tipexa": _unicode_code_point("tipeha"),  # translit-ok
    "u_tsadi": _unicode_code_point("tsadi"),
    "u_tsere": _unicode_code_point("tsere"),
    "u_zarqa": _unicode_code_point("zarqa"),
    "u_qadma": _unicode_code_point("qadma"),
    "u_pashta": _unicode_code_point("pashta"),
    "u_xolam": _unicode_code_point("holam"),
    "u_meteg": _unicode_code_point("meteg"),
    "u_dehi": _unicode_code_point("dehi"),  # translit-ok
    "u_CGJ": _unicode_code_point("cgj"),
    "u_CGJ_expanded": _unicode_code_point("combining grapheme joiner"),
    "u_hypothetical_tarxa": _unicode_code_point("tarha"),  # translit-ok
    "u_hypothetical_tsinor": _unicode_code_point("tsinor"),
    "u_hypothetical_zarqahlp": _unicode_code_point("zarqa stress helper"),
    "u_hypothetical_hhfa": _unicode_code_point("holam haser for alef"),
    "u_hypothetical_hhfml": _unicode_code_point("holam haser for matres lectionis"),
    "u_hypothetical_xxfvoa": _unicode_code_point("holam haser for vav or alef"),
    "u_hypothetical_xm": _unicode_code_point("holam male"),
    "u_hypothetical_xx": _unicode_code_point("holam haser"),
    "u_hypothetical_implicit_yod": _unicode_code_point("implicit yod"),
    "unicode_name_sheva_na_mudgash": _unicode_character_name(
        "HEBREW POINT SHEVA NA MUDGASH"
    ),
    "unicode_name_dagesh_xazaq_mudgash": _unicode_character_name(
        "HEBREW POINT DAGESH HAZAQ MUDGASH"
    ),
    "unicode_name_dagesh_or_mapiq": _unicode_character_name(
        "HEBREW POINT DAGESH OR MAPIQ"
    ),
    "unicode_name_lower_dot": _unicode_character_name("HEBREW MARK LOWER DOT"),
    #
    "LAOcI_pat_ger": "לַ֜͏ִם",
}


def write_pages():
    """Write both pages, after checking the comparison images against their records."""
    variant_d = dict(
        title_in_head_title="The Taamey D font for Biblical Hebrew",
        table_header_label="Taamey D",
        css_class="font-family-taamey-d",
        outpath=_PAGES_DIR / "Taamey_D.html",
        provide_display_symbols=True,
        inlines=taamey_d_page.BIG_STR,
    )
    variant_xx_for_alef = dict(
        title_in_head_title="Xolam xaser for alef".translate(_ROM_TRANS_TABLE),
        title_in_h1=_SYMDEFS["Xolam_xaser"] + " for " + _SYMDEFS["alef"],
        outpath=_PAGES_DIR / "Xolam_xaser_for_alef.html",
        inlines=xx_for_alef_page.BIG_STR,
    )
    variants = (variant_d, variant_xx_for_alef)
    _check_comparison_images()
    #
    for variant in variants:
        if "title_in_h1" not in variant:
            variant["title_in_h1"] = variant["title_in_head_title"]
        displays = {}
        if variant.get("provide_display_symbols"):
            displays = _displays(variant)
        symdefs = {**_SYMDEFS, **variant, **displays}
        file_io.with_tmp_openw(
            variant["outpath"],
            {"newline": ""},
            _write_page,
            variant["inlines"],
            symdefs,
        )


def _write_page(inlines, symdefs, outfp):
    for line in inlines.splitlines(keepends=True):
        after_dollar_subs = string.Template(line).substitute(symdefs)
        outfp.write(after_dollar_subs)
