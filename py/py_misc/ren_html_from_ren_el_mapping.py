"""Exports HT_TAC_FOR_RT_FOR_MAM_WITH_DOC & related"""

from typing import Union


def _dic_of_c_to_tc(tag, classes):
    return {c: (tag, c) for c in classes}


_HT_SPANS_FOR_MAM_WITH_DOC = [
    "mam-doc-target-without-callout",
    "mam-doc-callout",
    #
    "mam-dqq-unstressed",
    "mam-dqq-stressed",
    #
    "mam-kq",
    "mam-kq-k",
    "mam-kq-k-velo-q",
    "mam-kq-k-velo-q-maq",
    "mam-kq-q",
    "mam-kq-q-velo-k",
    #
    "mam-letter-small",
    "mam-letter-large",
    "mam-letter-hung",
    #
    "mam-spi-samekh",
    "mam-spi-pe",
    "mam-spi-invnun",
    #
    "mam-implicit-maqaf",
    "mam-good-ending",
]
_HT_BRS_FOR_MAM_WITH_DOC = [
    "mam-br-before-good-ending",
    "mam-br-after-pe",
]
_HT_TAC_FOR_RT_FOR_SPECIAL_SPACES = {
    "ren-tag-octo-space": ("html-tag-octo-space", None),
    "ren-tag-thin-space": ("html-tag-thin-space", None),
    "ren-tag-no-break-space": ("html-tag-no-break-space", None),
}
_HT_SPANS_FOR_SLH_WORD_FOI = [
    "slh-word",
    "mam-letter-small",
    "mam-letter-large",
    "mam-letter-hung",
    "mam-lp-legarmeih",  # why is legarmeih needed?
]
_HT_SPANS_FOR_KETIV_QERE_FOI = [
    "mam-kq",
    "mam-kq-k",
    "mam-kq-q",
    "mam-kq-trivial",
    "mam-kq-q-velo-k",
    "mam-kq-k-velo-q",
    "mam-kq-k-velo-q-maq",
    "mam-doc",
    "mam-dqq-stressed",
    "mam-dqq-unstressed",
    "mam-lp-legarmeih",
    "mam-lp-paseq",
    "slh-word",
    "mam-letter-small",
]
_HT_SPANS_FOR_RARE_TMPLS_FOI = [
    "scrdfftar",
    "sdt-target",
    "sdt-note",
    "slh-word",
    "mam-letter-small",
    "mam-letter-large",
    "mam-spi-pe",
    "mam-br-after-pe",
]
HT_TAC_FOR_RT_FOR_MAM_WITH_DOC: dict[str, tuple[str, Union[str, None]]] = {
    **_HT_TAC_FOR_RT_FOR_SPECIAL_SPACES,
    **_dic_of_c_to_tc("span", _HT_SPANS_FOR_MAM_WITH_DOC),
    **_dic_of_c_to_tc("br", _HT_BRS_FOR_MAM_WITH_DOC),
    "mam-bold": ("b", None),
    "mam-anchor": ("a", None),
}
HT_TAC_FOR_RT_FOR_SLH_WORD_FOI = {
    **_HT_TAC_FOR_RT_FOR_SPECIAL_SPACES,
    **_dic_of_c_to_tc("span", _HT_SPANS_FOR_SLH_WORD_FOI),
}
HT_TAC_FOR_RT_FOR_KETIV_QERE_FOI = {
    **_HT_TAC_FOR_RT_FOR_SPECIAL_SPACES,
    **_dic_of_c_to_tc("span", _HT_SPANS_FOR_KETIV_QERE_FOI),
}
HT_TAC_FOR_RT_FOR_RARE_TMPLS_FOI = {
    **_dic_of_c_to_tc("span", _HT_SPANS_FOR_RARE_TMPLS_FOI),
}
