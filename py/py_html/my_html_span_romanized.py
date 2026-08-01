import py_html.wlc_utils_html as wlc_utils_html


def rmn(string):
    return wlc_utils_html.span(string, {"class": "romanized"})
