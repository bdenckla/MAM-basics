from pycmn import bib_locales as tbn
from py_misc import vtrad_helpers as mr


_FST_SAM_24_2_SEF = tbn.mk_bcvtsef(tbn.BK_FST_SAM, 24, 2)
_JEREMIAH_31_2_SEF = tbn.mk_bcvtsef(tbn.BK_JEREM, 31, 2)
_EXODUS_20_4_SEF = tbn.mk_bcvtsef(tbn.BK_EXODUS, 20, 4)
_DEUTER_5_8_SEF = tbn.mk_bcvtsef(tbn.BK_DEUTER, 5, 8)
_JOSHUA_21_38_SEF = tbn.mk_bcvtsef(tbn.BK_JOSHUA, 21, 38)
_SHIFTED_SPAN_RECS_FOR_SEF = (  # shift is relative to Sefaria
    # Triples below are Sef span start bcvt, span length, shift
    # span length is measured in verses
    # shift is amount to shift get MAM verse
    (_FST_SAM_24_2_SEF, 22, -1),  # mamv = sefv - 1 for sefv in this range
    (_JEREMIAH_31_2_SEF, 39, -1),  # mamv = sefv - 1 for sefv in this range
    (_EXODUS_20_4_SEF, 20, -1),  # mamv = sefv - 1 for sefv in this range
    (_DEUTER_5_8_SEF, 23, -1),  # mamv = sefv - 1 for sefv in this range
    (_JOSHUA_21_38_SEF, 8, -2),  # mamv = sefv - 2 for sefv in this range
)
_FST_SAM_24_2_BHS = tbn.mk_bcvtbhs(tbn.BK_FST_SAM, 24, 2)
_JEREMIAH_31_2_BHS = tbn.mk_bcvtbhs(tbn.BK_JEREM, 31, 2)
_EXODUS_20_4_BHS = tbn.mk_bcvtbhs(tbn.BK_EXODUS, 20, 4)
_EXODUS_20_17_BHS = tbn.mk_bcvtbhs(tbn.BK_EXODUS, 20, 17)
_DEUTER_5_8_BHS = tbn.mk_bcvtbhs(tbn.BK_DEUTER, 5, 8)
_DEUTER_5_21_BHS = tbn.mk_bcvtbhs(tbn.BK_DEUTER, 5, 21)
_JOSHUA_21_38_BHS = tbn.mk_bcvtbhs(tbn.BK_JOSHUA, 21, 38)
_SHIFTED_SPAN_RECS_FOR_BHS = (  # shift is relative to BHS
    # Triples below are BHS span start bcvt, span length, shift
    # span length is measured in verses
    # shift is amount to shift get MAM verse
    (_FST_SAM_24_2_BHS, 22, -1),
    (_JEREMIAH_31_2_BHS, 39, -1),
    (_EXODUS_20_4_BHS, 9, -1),
    (_EXODUS_20_17_BHS, 10, -4),
    (_DEUTER_5_8_BHS, 9, -1),
    (_DEUTER_5_21_BHS, 13, -4),
    (_JOSHUA_21_38_BHS, 8, -2),
)
_FST_SAM_23_29_MAM = tbn.mk_bcvtmam(tbn.BK_FST_SAM, 23, 29)
_CV_24_1_SEF = tbn.mk_cvtsef(24, 1)
_CV_24_1_BHS = tbn.mk_cvtbhs(24, 1)
_JEREMIAH_30_25_MAM = tbn.mk_bcvtmam(tbn.BK_JEREM, 30, 25)
_CV_31_1_SEF = tbn.mk_cvtsef(31, 1)
_CV_31_1_BHS = tbn.mk_cvtbhs(31, 1)
EXODUS_20_2_MAM = tbn.mk_bcvtmam(tbn.BK_EXODUS, 20, 2)
_CV_20_2_SEF = tbn.mk_cvtsef(20, 2)
_CV_20_3_SEF = tbn.mk_cvtsef(20, 3)
_CV_20_2_BHS = tbn.mk_cvtbhs(20, 2)
_CV_20_3_BHS = tbn.mk_cvtbhs(20, 3)
EXODUS_20_12_MAM = tbn.mk_bcvtmam(tbn.BK_EXODUS, 20, 12)
_CV_20_13_BHS = tbn.mk_cvtbhs(20, 13)
_CV_20_14_BHS = tbn.mk_cvtbhs(20, 14)
_CV_20_15_BHS = tbn.mk_cvtbhs(20, 15)
_CV_20_16_BHS = tbn.mk_cvtbhs(20, 16)
NUMBERS_25_18_MAM = tbn.mk_bcvtmam(tbn.BK_NUMBERS, 25, 18)
NUMBERS_26_1_MAM = tbn.mk_bcvtmam(tbn.BK_NUMBERS, 26, 1)
_CV_25_19_BHS = tbn.mk_cvtbhs(25, 19)
_CV_26_1_BHS = tbn.mk_cvtbhs(26, 1)
DEUTER_5_6_MAM = tbn.mk_bcvtmam(tbn.BK_DEUTER, 5, 6)
_CV_5_6_SEF = tbn.mk_cvtsef(5, 6)
_CV_5_7_SEF = tbn.mk_cvtsef(5, 7)
_CV_5_6_BHS = tbn.mk_cvtbhs(5, 6)
_CV_5_7_BHS = tbn.mk_cvtbhs(5, 7)
DEUTER_5_16_MAM = tbn.mk_bcvtmam(tbn.BK_DEUTER, 5, 16)
_CV_5_17_BHS = tbn.mk_cvtbhs(5, 17)
_CV_5_18_BHS = tbn.mk_cvtbhs(5, 18)
_CV_5_19_BHS = tbn.mk_cvtbhs(5, 19)
_CV_5_20_BHS = tbn.mk_cvtbhs(5, 20)
JOSHUA_21_35_MAM = tbn.mk_bcvtmam(tbn.BK_JOSHUA, 21, 35)
_CV_21_35_BHS = tbn.mk_cvtbhs(21, 35)
_CV_21_36_BHS = tbn.mk_cvtbhs(21, 36)
_CV_21_37_BHS = tbn.mk_cvtbhs(21, 37)
_CV_21_35_SEF = tbn.mk_cvtsef(21, 35)
_CV_21_36_SEF = tbn.mk_cvtsef(21, 36)
_CV_21_37_SEF = tbn.mk_cvtsef(21, 37)
_BCV_DIC_FROM_MAM_TO_SEF_WEIRD = {
    _FST_SAM_23_29_MAM: mr.mk_maprec_1_to_1(_CV_24_1_SEF),
    _JEREMIAH_30_25_MAM: mr.mk_maprec_1_to_1(_CV_31_1_SEF),
    EXODUS_20_2_MAM: mr.mk_maprec_1_to_many(_CV_20_2_SEF, _CV_20_3_SEF),
    DEUTER_5_6_MAM: mr.mk_maprec_1_to_many(_CV_5_6_SEF, _CV_5_7_SEF),
    JOSHUA_21_35_MAM: mr.mk_maprec_1_to_1_and_empties(
        _CV_21_35_SEF, _CV_21_36_SEF, _CV_21_37_SEF
    ),
}
_BCV_DIC_FROM_MAM_TO_BHS_WEIRD = {
    _FST_SAM_23_29_MAM: mr.mk_maprec_1_to_1(_CV_24_1_BHS),
    _JEREMIAH_30_25_MAM: mr.mk_maprec_1_to_1(_CV_31_1_BHS),
    EXODUS_20_2_MAM: mr.mk_maprec_1_to_many(_CV_20_2_BHS, _CV_20_3_BHS),
    EXODUS_20_12_MAM: mr.mk_maprec_1_to_many(
        _CV_20_13_BHS, _CV_20_14_BHS, _CV_20_15_BHS, _CV_20_16_BHS
    ),
    NUMBERS_26_1_MAM: mr.mk_maprec_1_to_many(_CV_25_19_BHS, _CV_26_1_BHS),
    DEUTER_5_6_MAM: mr.mk_maprec_1_to_many(_CV_5_6_BHS, _CV_5_7_BHS),
    DEUTER_5_16_MAM: mr.mk_maprec_1_to_many(
        _CV_5_17_BHS, _CV_5_18_BHS, _CV_5_19_BHS, _CV_5_20_BHS
    ),
    JOSHUA_21_35_MAM: mr.mk_maprec_1_to_1_and_empties(
        _CV_21_35_BHS, _CV_21_36_BHS, _CV_21_37_BHS
    ),
}
_BCV_DIC_FROM_MAM_TO_SEF_FOR_SS = mr.mk_dic_for_shifted_spans(
    _SHIFTED_SPAN_RECS_FOR_SEF
)
_BCV_DIC_FROM_MAM_TO_SEF = {
    **_BCV_DIC_FROM_MAM_TO_SEF_WEIRD,
    **_BCV_DIC_FROM_MAM_TO_SEF_FOR_SS,
}
_BCV_DIC_FROM_MAM_TO_BHS_FOR_SS = mr.mk_dic_for_shifted_spans(
    _SHIFTED_SPAN_RECS_FOR_BHS
)
_BCV_DIC_FROM_MAM_TO_BHS = {
    **_BCV_DIC_FROM_MAM_TO_BHS_WEIRD,
    **_BCV_DIC_FROM_MAM_TO_BHS_FOR_SS,
}
BCV_DIC_FROM_MAM_TO_YYY = {
    tbn.VT_SEF: _BCV_DIC_FROM_MAM_TO_SEF,
    tbn.VT_BHS: _BCV_DIC_FROM_MAM_TO_BHS,
}
