"""Exports main"""

from pycmn.my_utils import sl_map
from py_misc import my_html
from pyauthor_util import author
from pyauthor import tsinnorit_in_psalm_32v5 as tip_32v5
from pyauthor import tsinnorit_and_oleh_facts as tao_facts


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch, top_dir_old):
    result = author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, _CBODY)
    _gen_redirect_for_old_url(top_dir_old)
    return result


def _gen_redirect_for_old_url(top_dir_old):
    # There is a link to this old URL in the following PDF:
    # https://www.unicode.org/L2/L2025/25242-hebrew-accents.pdf
    # so we want to keep that old URL working.
    out_path_redir = f"{top_dir_old}/{_FNAME}"
    title_redir = f"Redirect for {_TITLE}"
    write_ctx_redir = my_html.WriteCtx(title_redir, out_path_redir)
    anc = my_html.anchor_h("a different location", f"../misc/{_FNAME}")
    cbody_redir = my_html.para(["This page has moved to ", anc, "."])
    my_html.write_html_to_file(cbody_redir, write_ctx_redir)


def _make_row(cells):
    ins_cnt, bibref, hbo_str, div_nam_typ, boi = cells
    # ins_cnt: Instance Count (how many times this word occurs in the Bible)
    # bibref: Bible Reference (e.g., Psalm 32:6)
    # hbo_str: Biblical Hebrew string
    # div_nam_typ: Divine Name Type
    # boi: Bibrefs of Other Instances
    # (e.g., Psalm 81:11 is another instance of the same word as Psalm 80:20)
    return my_html.table_row_of_data(
        [str(ins_cnt), bibref, author.hbo(hbo_str), div_nam_typ, boi]
    )


_TITLE = "Tsinnorit & Oleh on Initial Vocal Shewa"
_H1_CONTENTS = "$Tsinnorit & $Oleh on Initial Vocal $Shewa"
_FNAME = "tsinnorit_and_oleh_on_ivs.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")
_CONT_PARA_01 = [
    "The only primary accents that can appear on an initial vocal $shewa ($IVS)",
    " are prepositives.",
    " And they’re not really “on” that $IVS anyway.",
    " They’re just on a word that happens to start with an $IVS.",
    " I.e., they need a stress helper in such cases.",
    " (Whether they get that helper varies from edition to edition.)",
]
_CONT_PARA_02 = [
    "Speaking of helpers:",
    " a helper for a postpostive cannot appear on an $IVS.",
    " So, we can say that no accent marking the primary stress",
    " ever appears on an $IVS.",
    " This makes sense since the primary stress is never on an $IVS.",
    " But what about accents not marking the primary stress?",
    " Do they ever appear on an $IVS?",
]
_CONT_PARA_03A = [
    "The answer is yes, but rarely.",
    " In the Hebrew Bible dataset called $MAM",
    " (Miqra According to the Masorah),",
    " there are 21 cases where either $tsinnorit or $oleh",
    " appear on an $IVS.",
    " (13 of these 21 have $oleh; the remaining 8 have $tsinnorit.)",
    " They are shown in the table below.",
    " Unless otherwise indicated, all references are to verses in Psalms.",
    " (There is one reference to a verse in Proverbs, Pr 30:9.).",
]
_CONT_TABLE_1A_CELLS = [
    [1, "32:6", "מְ֫צֹ֥א", "", ""],
    [2, "68:5", "שְׁ֫מ֥וֹ", "", "72:17"],
    [1, "68:24", "בְּ֫דָ֥ם", "", ""],
    [1, "72:15", "שְׁ֫בָ֥א", "", ""],
    [1, "142:8", "אֶת־שְׁ֫מֶ֥ךָ", "", ""],
    [2, "27:14", "אֶל־יְ֫הֹוָ֥ה", "DN-A", "130:7"],
    [4, "84:3", "יְ֫הֹוָ֥ה", "DN-A", "85:9, 142:6, Pr 30:9"],
    [1, "104:1", "אֶת־יְ֫הֹוָ֥ה", "DN-A", ""],
    [7, "80:20", "יְ֘הֹוָ֤ה", "DN-A", "81:11, 84:9, 96:10, 99:5, 99:9, 106:47"],
    [1, "109:21", "יֱ֘הֹוִ֤ה", "DN-E", ""],
]
_CONT_TABLE_1A_ROWS = sl_map(_make_row, _CONT_TABLE_1A_CELLS)
_CONT_PARA_03B = "Ignoring prefixes אֶת־ and אֶל־ yields the following:"
_CONT_TABLE_1B_CELLS = [
    [1, "32:6", "מְ֫צֹ֥א", "", ""],
    [2, "68:5", "שְׁ֫מ֥וֹ", "", "72:17"],
    [1, "68:24", "בְּ֫דָ֥ם", "", ""],
    [1, "72:15", "שְׁ֫בָ֥א", "", ""],
    [1, "142:8", "שְׁ֫מֶ֥ךָ", "", ""],
    [7, "27:14", "יְ֫הֹוָ֥ה", "DN-A", "84:3, 85:9, 104:1, 130:7, 142:6, Pr 30:9"],
    [7, "80:20", "יְ֘הֹוָ֤ה", "DN-A", "81:11, 84:9, 96:10, 99:5, 99:9, 106:47"],
    [1, "109:21", "יֱ֘הֹוִ֤ה", "DN-E", ""],
]
_CONT_TABLE_1B_ROWS = sl_map(_make_row, _CONT_TABLE_1B_CELLS)
# XXX TODO mention א!=וְ֘יוֹד֤וּ in Ps 89:6
# XXX TODO mention א!=יְֽכַ֫בְּ֫דָ֥נְנִי in Ps 50:23
# XXX TODO look up note on וְא֘וֹדֶ֤ה in Ps138:2
_ANC_PRE_PRE = "For general info about these accents, see my "
_CONT_PARA_04A = author.paren([_ANC_PRE_PRE, tao_facts.anchor()])
_CONT_PARA_04B = [
    "Note that all 8 of the $tsinnorit cases and 7 of the 13 $oleh cases",
    " are on the divine name יהוה.",
    " Of these 15 divine name cases,",
    " 14 are of type “DN-A” (divine name pointed as Adonai) and",
    " one is of type “DN-E” (divine name pointed as Elohim).",
]
_CONT_PARA_05 = [
    "To summarize, when an accent appears on $IVS it is either:",
]
_CONT_UL_1_LI_1 = [
    "A prepositive, which is not really “on” that $IVS anyway.",
]
_CONT_UL_1_LI_2 = ["One of those weird accents ($tsinnorit or $oleh)."]
_CONT_PARA_06 = [
    ["But what about a vocal $shewa that is not initial?"],
    [" What accents, if any, can appear on that?"],
    [" The answer is: none, except for a misplaced $tsinnorit"],
    [" that is seen in Psalm 32:5 ועוני in some editions."],
    [" ", author.paren(["See my ", tip_32v5.anchor()])],
]
_CBODY = [
    author.heading_level_1(_H1_CONTENTS),
    author.para(_CONT_PARA_01),
    author.para(_CONT_PARA_02),
    author.para(_CONT_PARA_03A),
    author.table_c(_CONT_TABLE_1A_ROWS),
    author.para(_CONT_PARA_03B),
    author.table_c(_CONT_TABLE_1B_ROWS),
    author.para(_CONT_PARA_04A),
    author.para(_CONT_PARA_04B),
    author.para(_CONT_PARA_05),
    author.unordered_list([_CONT_UL_1_LI_1, _CONT_UL_1_LI_2]),
    author.para(_CONT_PARA_06),
]
