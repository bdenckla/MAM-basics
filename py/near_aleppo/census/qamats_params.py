"""Count the qamats template's alternatives in MAM-parsed-plus.

Report parameter shapes, qamats-qatan inventory and differences between the two
alternatives before and after the near-Aleppo qamats-size policy.
"""

import sys
import unicodedata
from collections import Counter

from mb_cmn import bib_locales as tbn
from near_aleppo.census import census_paths
from near_aleppo.census.edition_projection import (
    EDITION_SEPARATOR_TEMPLATE_NAMES,
    edition_parameter_keys,
)
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import ws_tmpl2 as wtp

sys.stdout.reconfigure(encoding="utf-8")

QQ = "\N{HEBREW POINT QAMATS QATAN}"
QAMATS = "\N{HEBREW POINT QAMATS}"
QAMATS_TMPL = "מ:קמץ"
SEPS = EDITION_SEPARATOR_TEMPLATE_NAMES


def render(w, qamats_key=None):
    """Flatten to text; qamats_key picks which מ:קמץ parameter to take."""
    if isinstance(w, str):
        return w
    if isinstance(w, (list, tuple)):
        return "".join(render(x, qamats_key) for x in w)
    if isinstance(w, dict) and wtp.is_template(w):
        name = wtp.template_name(w)
        if name in SEPS:
            return " "
        overrides = None if qamats_key is None else {QAMATS_TMPL: (qamats_key,)}
        keys = edition_parameter_keys(w, overrides=overrides)
        return "".join(render(wtp.template_param_val(w, k), qamats_key) for k in keys)
    return ""


def find(w, out):
    if isinstance(w, (list, tuple)):
        for x in w:
            find(x, out)
        return
    if isinstance(w, dict) and wtp.is_template(w):
        name = wtp.template_name(w)
        if name in SEPS:
            return
        if name == QAMATS_TMPL:
            out.append(w)
            return
        keys = edition_parameter_keys(w)
        for k in keys:
            find(wtp.template_param_val(w, k), out)


def nm(c):
    try:
        return unicodedata.name(c)
    except ValueError:
        return "U+%04X" % ord(c)


def main():
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=census_paths.mam_parsed_path())

    keyshapes = Counter()
    same_after, differ_after = 0, []
    prediff = Counter()
    qq_in_tmpl = 0
    qq_total_d = 0
    n = 0
    for bkid in tbn.ALL_BK39_IDS:
        if bkid not in books:
            continue
        for bcvt, mr in books[bkid]["verses_plus"].items():
            bk, ch, vr = tbn.bcvt_get_bcv_triple(bcvt)
            seq = list(mr.EP)
            qq_total_d += render(seq, "ד").count(QQ)
            hits = []
            find(seq, hits)
            for t in hits:
                n += 1
                keys = tuple(sorted(wtp.template_param_keys(t)))
                keyshapes[keys] += 1
                d = render(wtp.template_param_val(t, "ד")) if "ד" in keys else None
                s = render(wtp.template_param_val(t, "ס")) if "ס" in keys else None
                if d is None or s is None:
                    continue
                qq_in_tmpl += d.count(QQ)
                if d != s:
                    prediff[
                        (tuple(sorted(set(d) - set(s))), tuple(sorted(set(s) - set(d))))
                    ] += 1
                dc, sc = d.replace(QQ, QAMATS), s.replace(QQ, QAMATS)
                if dc == sc:
                    same_after += 1
                else:
                    differ_after.append((f"{bk} {ch}:{vr}", d, s))

    print(f"מ:קמץ templates (settled walk): {n}")
    print("parameter-key shapes:")
    for keys, c in keyshapes.most_common():
        print(f"   {keys}: {c}")
    print(f"\nU+05C7 in the whole base text taking ד: {qq_total_d}")
    print(f"U+05C7 inside a מ:קמץ ד parameter: {qq_in_tmpl}")
    print(f"U+05C7 elsewhere in the base text: {qq_total_d - qq_in_tmpl}")

    print(
        "\nhow ד and ס differ BEFORE the collapse (chars only in ד, chars only in ס):"
    )
    for (only_d, only_s), c in prediff.most_common():
        dd = ", ".join(nm(x) for x in only_d) or "(none)"
        ss = ", ".join(nm(x) for x in only_s) or "(none)"
        print(f"   {c:>4}  only in ד: {dd}   |   only in ס: {ss}")

    print(
        f"\nafter collapsing U+05C7 to U+05B8: identical {same_after}, differing {len(differ_after)}"
    )
    for ref, d, s in differ_after:
        print(f"   {ref}")
        print(f"      ד: {d!r}")
        print(f"      ס: {s!r}")
