"""Count MAM template names, parameter shapes and selected populations.

The raw walk inventories every parameter. The settled walk uses an explicit
template-child table for its stated population; it is not the edition's single
Scripture projection. Unknown names or missing selected parameters fail.
"""

import sys
from collections import Counter, defaultdict

from mb_cmn import bib_locales as tbn
from near_aleppo.census import census_paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import ws_tmpl2 as wtp

sys.stdout.reconfigure(encoding="utf-8")

LEG = "מ:לגרמיה-2"
NARPAS = "מ:פסק"

# The settled dataset walk, with every current template explicit.  Tuples with
# more than one key are deliberate because this is a template inventory rather
# than a survey of one edition's Scripture stream.  A value of () means that no
# child belongs to the settled walk.
SETTLED_KEYS = {
    "נוסח": ("1",),  # rule 2
    "מ:כפול": ("כפול",),  # rule 6
    "מ:דחי": ("1",),  # step 29
    "מ:צינור": ("1",),  # step 29
    "מ:קמץ": ("ד",),  # step 28
    "מ:אות-מיוחדת-במילה": ("2",),  # rule 3
    "מ:הערה": (),  # mpu-parsing.md: bare note
    "מ:הערה-2": ("1",),  # mpu-parsing.md: param 2 is the note body
    "מ:קישור בהערה": (),
    "מ:קישור פנימי בהערה": (),
    "מ:קו״כ-אם-2": ("1",),  # step 26: the pointed ketiv
    "מ:כו״ק מיוחד": ("1", "2"),  # param 2 is the pointed qere -- real text
    "כו״ק": ("1", "2"),  # dataset inventory: ketiv and qere are both in scope
    "קו״כ": ("1", "2"),  # dataset inventory: ketiv and qere are both in scope
    "קרי ולא כתיב": ("1", "2"),  # dataset inventory, not an edition projection
    "כתיב ולא קרי": ("1", "2"),  # dataset inventory, not an edition projection
    "מ:אות-ג": ("1",),
    "מ:אות-ק": ("1",),
    "מ:אות תלויה": (),
    "מודגש": ("1",),
    "מ:מקף אפור": (),
    "מ:פסק": (),
    "מ:לגרמיה-2": (),
    "ש": (),
    "מ:ששש": (),
    "ששש": (),
    'מ:נו"ן הפוכה': (),
    "מ:נו״ן הפוכה": (),
    "ר0": (),
    "ר1": (),
    "ר2": (),
    "ר3": (),
    "ר4": (),
    "סס": (),
    "ססס": (),
    "פפ": (),
    "פפפ": (),
}


def keys_settled(name, keys):
    selected = SETTLED_KEYS.get(name)
    if selected is None:
        raise AssertionError(f"No settled-dataset rule for template {name!r}")
    missing = [key for key in selected if key not in keys]
    if missing:
        raise AssertionError(
            f"Template {name!r} lacks settled parameter(s) {missing!r}"
        )
    return selected


def main():
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=census_paths.mam_parsed_path())

    raw_counts = Counter()
    raw_keysets = defaultdict(Counter)
    settled_counts = Counter()

    def walk_raw(w):
        if isinstance(w, (list, tuple)):
            for x in w:
                walk_raw(x)
            return
        if isinstance(w, dict) and wtp.is_template(w):
            name = wtp.template_name(w)
            keys = list(wtp.template_param_keys(w))
            raw_counts[name] += 1
            raw_keysets[name][tuple(sorted(keys))] += 1
            for k in keys:
                walk_raw(wtp.template_param_val(w, k))

    def walk_settled(w):
        if isinstance(w, (list, tuple)):
            for x in w:
                walk_settled(x)
            return
        if isinstance(w, dict) and wtp.is_template(w):
            name = wtp.template_name(w)
            settled_counts[name] += 1
            for k in keys_settled(name, list(wtp.template_param_keys(w))):
                walk_settled(wtp.template_param_val(w, k))

    for bkid in tbn.ALL_BK39_IDS:
        if bkid not in books:
            continue
        for bcvt, mr in books[bkid]["verses_plus"].items():
            walk_raw(list(mr.EP))
            walk_settled(list(mr.EP))

    print(f"{'template':<28} {'raw':>7} {'settled':>8}   parameter key sets (raw)")
    for name, n in raw_counts.most_common():
        ks = "; ".join(
            f"{tuple(k) or '()'} x{v}" for k, v in raw_keysets[name].most_common(4)
        )
        print(f"{name:<28} {n:>7} {settled_counts[name]:>8}   {ks}")

    print(f"\ndistinct template names: {len(raw_counts)}")
    print(
        f"\nunder the corrected settled walk: {LEG} = {settled_counts[LEG]}, "
        f"{NARPAS} = {settled_counts[NARPAS]}"
    )
