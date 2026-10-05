"""Count MAM divine-name atoms by the vowels indicating their reading.

Report the Adonai and Elohim readings, holam on the first he and vowels on yod.
The census preserves MAM's source text and reports the configurations separately.
"""

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
SHEVA = "\N{HEBREW POINT SHEVA}"
HATAF_SEGOL = "\N{HEBREW POINT HATAF SEGOL}"
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
    """[(letter, marks), ...] for the atom."""
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

    reading = Counter()
    yod_vowel = Counter()
    he_holam = Counter()
    by_book_elohim = Counter()
    odd = []

    for bkid in tbn.ALL_BK39_IDS:
        if bkid not in books:
            continue
        for bcvt, mr in books[bkid]["verses_plus"].items():
            bk, ch_, vr = tbn.bcvt_get_bcv_triple(bcvt)
            where = f"{bk} {ch_}:{vr}"
            for atom in render(list(mr.EP)).replace("־", " ").split():
                cls = clusters(atom)
                sk = "".join(c for c, _ in cls)
                if not sk.endswith("יהוה"):
                    continue
                core = cls[-4:]  # yod, he, vav, he
                (y, ym), (h1, h1m), (v, vm), (h2, h2m) = core
                if (y, h1, v, h2) != ("י", "ה", "ו", "ה"):
                    odd.append((where, atom))
                    continue
                if HIRIQ in vm:
                    kind = "Elohim (hiriq on vav)"
                    by_book_elohim[bkid] += 1
                elif QAMATS in vm:
                    kind = "Adonai (qamats on vav)"
                else:
                    kind = f"other ({' '.join(f'{ord(c):04X}' for c in vm)})"
                reading[kind] += 1
                he_holam[(kind, HOLAM in h1m)] += 1
                if HATAF_SEGOL in ym:
                    yv = "hataf segol"
                elif SHEVA in ym:
                    yv = "sheva"
                elif not any(c in ym for c in (SHEVA, HATAF_SEGOL)):
                    yv = "none/other"
                yod_vowel[(kind, yv)] += 1

    print("=== divine-name atoms by reading ===")
    for k, n in reading.most_common():
        print(f"   {k:<26} {n}")
    print(f"   TOTAL {sum(reading.values())}")

    print("\n=== holam on the FIRST HE, by reading ===")
    for (kind, has), n in sorted(he_holam.items()):
        print(f"   {kind:<26} holam={str(has):<5} {n}")

    print("\n=== vowel on the YOD, by reading (step 24) ===")
    for (kind, yv), n in sorted(yod_vowel.items()):
        print(f"   {kind:<26} {yv:<12} {n}")

    print(f"\n=== Elohim reading by book ({len(by_book_elohim)} books) ===")
    for bk, n in by_book_elohim.most_common():
        print(f"   {bk:<12} {n}")

    print(f"\n=== atoms whose last four letters are not י-ה-ו-ה: {len(odd)} ===")
    for where, atom in odd[:10]:
        print(f"   {where} {atom}")
