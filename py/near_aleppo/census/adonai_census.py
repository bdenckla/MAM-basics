"""Throwaway (step 23): MAM's אדני atoms, split into the divine title (qamats on the
nun) and ordinary 'my lord' (hiriq on the nun), with the holam reported for each.
This census distinguishes the divine title from the ordinary expression "my lord"."""

import sys
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

HOLAM = "\N{HEBREW POINT HOLAM}"
HIRIQ = "\N{HEBREW POINT HIRIQ}"
QAMATS = "\N{HEBREW POINT QAMATS}"
LETTERS = set(chr(c) for c in range(0x05D0, 0x05EB))
MARKS = set(chr(c) for c in range(0x0591, 0x05C8)) | {
    "\N{COMBINING GRAPHEME JOINER}",
    "\N{HEBREW POINT JUDEO-SPANISH VARIKA}",
}
SEPS = {
    "ר0",
    "ר1",
    "ר2",
    "ר3",
    "מ:מקף אפור",
    "מ:פסק",
    "מ:לגרמיה-2",
    "ש",
    "מ:ששש",
    "מ:נו״ן הפוכה",
    "פפ",
    "פפפ",
    "סס",
    "ססס",
} | EDITION_SEPARATOR_TEMPLATE_NAMES


def render(w):
    if isinstance(w, str):
        return w
    if isinstance(w, (list, tuple)):
        return "".join(render(x) for x in w)
    if isinstance(w, dict) and wtp.is_template(w):
        name = wtp.template_name(w)
        if name in SEPS:
            return " "
        keys = edition_parameter_keys(w)
        return " ".join(render(wtp.template_param_val(w, k)) for k in keys)
    return ""


def clusters(atom):
    out, base, marks = [], None, ""
    for ch in atom:
        if ch in LETTERS:
            if base is not None:
                out.append((base, marks))
            base, marks = ch, ""
        elif base is not None and ch in MARKS:
            marks += ch
    if base is not None:
        out.append((base, marks))
    return out


def main():
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=census_paths.mam_parsed_path())

    kind_counts = Counter()
    title_holam = Counter()
    no_holam_examples = []
    prefixed = Counter()
    by_book_title = Counter()

    for bkid in tbn.ALL_BK39_IDS:
        if bkid not in books:
            continue
        for bcvt, mr in books[bkid]["verses_plus"].items():
            bk, ch_, vr = tbn.bcvt_get_bcv_triple(bcvt)
            where = f"{bk} {ch_}:{vr}"
            for atom in render(list(mr.EP)).replace("־", " ").split():
                cls = clusters(atom)
                sk = "".join(c for c, _ in cls)
                if not sk.endswith("אדני"):
                    continue
                (a, am), (d, dm), (n, nm), (y, ym) = cls[-4:]
                if (a, d, n, y) != ("א", "ד", "נ", "י"):
                    continue
                if QAMATS in nm:
                    kind = "divine title (qamats on nun)"
                    by_book_title[bkid] += 1
                elif HIRIQ in nm:
                    kind = "ordinary 'my lord' (hiriq on nun)"
                else:
                    kind = f"other ({' '.join(f'{ord(c):04X}' for c in nm)})"
                kind_counts[kind] += 1
                if kind.startswith("divine"):
                    has = HOLAM in dm
                    title_holam[has] += 1
                    prefixed[len(sk) > 4] += 1
                    if not has:
                        no_holam_examples.append((where, atom))

    print("=== atoms whose letters end in אדני, by the vowel on the nun ===")
    for k, n in kind_counts.most_common():
        print(f"   {k:<38} {n}")
    print(f"   TOTAL {sum(kind_counts.values())}")

    print("\n=== the divine title: holam on the dalet ===")
    for has, n in sorted(title_holam.items()):
        print(f"   holam={has}: {n}")
    print(
        f"   bare אדני vs prefixed: {prefixed[False]} bare, {prefixed[True]} prefixed"
    )

    print(f"\n=== divine-title atoms WITHOUT a holam: {len(no_holam_examples)} ===")
    for where, atom in no_holam_examples[:20]:
        marks = " ".join(f"{ord(c):04X}" for c in atom if c in MARKS)
        print(f"   {where}  {atom}   [{marks}]")

    print(f"\n=== divine title by book ({len(by_book_title)} books) ===")
    for bk, n in by_book_title.most_common(10):
        print(f"   {bk:<12} {n}")
