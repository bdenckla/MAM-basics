def encoding_is_mdc(wlc_id):
    return RELEASE_INFO["ri-formats"][wlc_id] == "fmt-M-C"


def encoding_is_uni(wlc_id):
    return RELEASE_INFO["ri-formats"][wlc_id] == "fmt-Uni"


_FILENAMES = {
    "wlc420": "wlc420_ps.txt",
    "wlc422": "wlc422_ps.txt",
    "2025-03-21-uni": "wlcubs420.txt",
    "2025-03-21-mdc": "wlcmbs420.txt",
}
_FORMATS = {
    "wlc420": "fmt-M-C",
    "wlc422": "fmt-M-C",
    "2025-03-21-uni": "fmt-Uni",
    "2025-03-21-mdc": "fmt-M-C",
}
RELEASE_INFO = {
    "ri-filenames": _FILENAMES,
    "ri-formats": _FORMATS,
}
