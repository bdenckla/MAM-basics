"""Exports main"""

from py_misc import my_html
from pyauthor_util import author
from pyauthor_rocc import rocc_212_pj3 as c211
from pyauthor_rocc import rocc_213_ajry as c213
from pyauthor_rocc import rocc_214_la as c214
from pyauthor_rocc import rocc_215_ky as c215
from pyauthor_rocc import rocc_216_yvmm as c216
from pyauthor_rocc import rocc_217_vlylh as c217
from pyauthor_rocc import rocc_219_fkbd as c219
from pyauthor_rocc import rocc_220_v3vny as c220
from pyauthor_rocc import rocc_221_njaf as c221
from pyauthor_rocc import rocc_222_mym as c222
from pyauthor_rocc import rocc_223_fhyv as c223
from pyauthor_rocc import rocc_224_ayn as c224
from pyauthor_rocc import rocc_225_bmfg as c225
from pyauthor_rocc import rocc_227_qrb_qrvb as c227
from pyauthor_rocc import rocc_228_lrj3 as c228
from pyauthor_rocc import rocc_229_jmxv as c229
from pyauthor_rocc import rocc_230_jc_fs_ac_lc as c230
from pyauthor_rocc import rocc_0_review_of_ctr_header as rocc_0

# XXX TODO add/fill in rocc_232_venice_mg.py


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    author.assert_stem_eq(__file__, _FNAME)
    author.help_gen_html_file(tdm_ch, _FNAME, _TITLE, _CBODY)


_TITLE = "CTR Psalm 32: Where Other Sources Stand"
_H1_CONTENTS = "$CTR Psalm 32: Where Other Sources Stand"
_FNAME = "rocc_3_where_other_sources_stand.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")
_X_01_CPARA = [
    ["This document covers more than its"],
    [" ", rocc_0.short_anchor("parent document")],
    [" in the following ways:"],
]
X_02_LIST_ITEMS = [
    [
        ["It shows ", my_html.emphasis("all"), " words where $CTR differs from $MAM,"],
        [" not just those that also differ from $JP."],
    ],
    ["It brings a number of other sources into the comparison."],
]
_X_03_CPARA = [
    ["This document covers ", my_html.emphasis("less")],
    [" than its parent document in the following way:"],
    [" it sometimes ignores $CTR or $JP where their contents are either:"],
]
_X_04_LIST_ITEMS = [
    ["Clearly in error."],
    ["So weird that comparison with these other sources is not meaningful."],
]
_CBODY = [
    author.heading_level_1(_H1_CONTENTS),
    author.para_ul(_X_01_CPARA, X_02_LIST_ITEMS),
    author.para_ul(_X_03_CPARA, _X_04_LIST_ITEMS),
    *author.para_table(*c211.ARGS),
    *author.para_table(*c213.ARGS),
    *author.para_table(*c214.ARGS),
    *author.para_table(*c215.ARGS),
    *author.para_table(*c216.ARGS),
    *author.para_table(*c217.ARGS),
    *author.para_table(*c219.ARGS),
    *author.para_table(*c220.ARGS),
    *author.para_table(*c221.ARGS),
    *author.para_table(*c222.ARGS),
    *author.para_table(*c223.ARGS),
    *author.para_table(*c224.ARGS),
    *author.para_table(*c225.ARGS),
    *author.para_table(*c227.ARGS),
    *author.para_table(*c228.ARGS),
    *author.para_table(*c229.ARGS),
    author.para_table(c230.X01_CPARA_JC_AND_FS_INTRO, c230.X02_TABLE_DATA_AJRY),
    author.std_table(c230.X03_TABLE_DATA_KY),
    author.std_table(c230.X04_TABLE_DATA_LRJ3),
    author.para_table(*c230.X_05_ARGS_MISC_GAYA),
]
