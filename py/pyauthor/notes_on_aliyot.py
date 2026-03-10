""" Exports main """

import string

from pycmn import file_io


def _romanized(text):
    return _span("romanized", text)


def _romanized_slash(text1, text2):
    t1_sl_t2 = "/".join((text1, text2))
    return _span("romanized", t1_sl_t2)


def _small_caps(text):
    return _span("small-caps", text)


def _span(spanclass, spantext):
    return f'<span class="{spanclass}">{spantext}</span>'


_ROMANIZATIONS_K = [
    "aliyah",
    "aliyot",
    "parashah",
    "parashiyot",
    "kohen",
    "levi",
    "yisrael",
    "maftir",
]

_ROMANIZATIONS_KV = {k: _romanized(k) for k in _ROMANIZATIONS_K}

_SYMDEFS = {
    "notes_on_aliyot": "Notes on Aliyot",
    #
    **_ROMANIZATIONS_KV,
    #
    "MAM": _small_caps("mam"),
    #
    "parashah_sl_aliyah": _romanized_slash("parashah", "aliyah"),
}


def _write_callback(aliyot_sym_html_in_fp, out_fp):
    for line in aliyot_sym_html_in_fp:
        after_tmpl_sub = string.Template(line).substitute(_SYMDEFS)
        out_fp.write(after_tmpl_sub)


def gen_html_file(top_dir):
    """Generate aliyot.html by making symbols in aliyot.sym.html concrete"""
    in_path = "doc/aliyot.sym.html"
    out_path = f"{top_dir}/aliyot.html"
    with open(in_path, encoding="utf-8", newline="") as aliyot_sym_html_in_fp:
        file_io.with_tmp_openw(
            out_path, {"newline": ""}, _write_callback, aliyot_sym_html_in_fp
        )
