def encoding_is_mdc(wlc_id):
    return RELEASE_INFO["ri-formats"][wlc_id] == "fmt-M-C"


def encoding_is_uni(wlc_id):
    return RELEASE_INFO["ri-formats"][wlc_id] == "fmt-Uni"


_FILENAMES = {
    "wlc420": "wlc420_ps.txt",
    "wlc422": "wlc422_ps.txt",
}
_FORMATS = {
    "wlc420": "fmt-M-C",
    "wlc422": "fmt-M-C",
}
RELEASE_INFO = {
    "ri-filenames": _FILENAMES,
    "ri-formats": _FORMATS,
}
