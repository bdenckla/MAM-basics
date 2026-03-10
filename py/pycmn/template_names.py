"""Exports Latin-alphabet symbols for some template names"""

# SR: strongly related ketiv & qere
# WR: weakly related ketiv & qere
# UR: unrelated ketiv & qere

K1Q1_MCOM = 'מ:כו"ק בין שני מקפים'
K1Q2_SR_KQQ = 'מ:כו"ק כתיב מילה חדה וקרי תרתין מילין'
K1Q2_SR_QQK = 'מ:קו"כ כתיב מילה חדה וקרי תרתין מילין'
K1Q2_SR_BCOM = 'מ:כו"ק כתיב מילה חדה וקרי תרתין מילין בין שני מקפים'
K1Q2_WR_KQQ = 'מ:כו"ק קרי שונה מהכתיב בשתי מילים'
K1Q2_UR_QQK = 'מ:קו"כ קרי שונה מהכתיב בשתי מילים'
K2Q1 = 'מ:כו"ק כתיב תרתין מילין וקרי מילה חדה'
K2Q2 = 'מ:כו"ק של שתי מילים בהערה אחת'
K3Q3 = 'מ:כו"ק של שלוש מילים בהערה אחת'
TWO_ACCENTS_OF_QUPO = "שני טעמים באות אחת קמץ-תחתון-פתח-עליון"
NO_PAR_AT_STA_OF_CHAP21 = "מ:אין פרשה בתחילת פרק"
NO_PAR_AT_STA_OF_CHAP03 = 'מ:אין פרשה בתחילת פרק בספרי אמ"ת'
NO_PAR_AT_STA_OF_WEEKLY = "מ:אין רווח של פרשה בתחילת פרשת השבוע"
SLH_WORD = "מ:אות-מיוחדת-במילה"
SCRDFF_TAR = "מ:הערה-2"
SCRDFF_NO_TAR = "מ:הערה"

LATIN_SHORTS = {
    'כו"ק': "k1q1-kq",  # 1
    'קו"כ': "k1q1-qk",  # 2
    K1Q1_MCOM: "k1q1-mcom",  # 3
    K1Q2_SR_KQQ: "k1q2-sr-kqq",  # 4
    K1Q2_SR_QQK: "k1q2-sr-qqk",  # 5
    K1Q2_SR_BCOM: "k1q2-sr-bcom",  # 6
    K1Q2_WR_KQQ: "k1q2-wr-kqq",  # 7
    K1Q2_UR_QQK: "k1q2-ur-qqk",  # 8
    K2Q1: "k2q1",  # 9
    K2Q2: "k2q2",  # 10
    K3Q3: "k3q3",  # 11
    'קו"כ-אם': "kq-trivial",
    "קרי ולא כתיב": "kq-q-velo-k",
    "כתיב ולא קרי": "kq-k-velo-q",
}
#  1: a normal ketiv/qere.
#  2: a ketiv/qere where template arguments are in kq order but they should be rendered in reverse order (qk order).
#  3: a ketiv/qere that is mid-compound, i.e. b in a-b-c. I26:20.
#  4: a k1q2 that is sr (strongly-related), where the atoms should be presented in kqq order. 13 cases.
#  5: a k1q2 that is sr (strongly-related), where the atoms should be presented in qqk order. Ne2:13.
#  6: a k1q2 that is sr (strongly-related), where the atoms are between two compounds, i.e. c in a-b c d-e read as a-b d-e appears in scroll as a c e i.e. ketiv c maps to qere "b d". 1C9:4.
#  7: a k1q2 that is wr (weakly-related). Ezekiel 9:11.
#  8: a k1q2 that is ur (unrelated): meimei ragleihem. 2K 18:27 & I 36:12.
#  9: a k2q1.
# 10: a k2q2.
# 11: a k3q3.


def map_all_std_kq_to_a_constant(the_constant):
    return {n: the_constant for n in _STD_KQ_TMPL_NAMES}


def map_all_whitespace_to_a_constant(the_constant):
    return {n: the_constant for n in _WHITESPACE_TMPL_NAMES}


_STD_KQ_TMPL_NAMES = (
    'כו"ק',
    'קו"כ',
    K1Q1_MCOM,
    K1Q2_SR_KQQ,
    K1Q2_SR_QQK,
    K1Q2_SR_BCOM,
    K1Q2_WR_KQQ,
    K1Q2_UR_QQK,
    K2Q1,
    K2Q2,
    K3Q3,
)
_WHITESPACE_TMPL_NAMES = {
    "מ:ששש",
    "סס",
    "פפ",
    "ססס",
    "פפפ",
    "ר0",
    "ר1",
    "ר2",
    "ר3",
}
