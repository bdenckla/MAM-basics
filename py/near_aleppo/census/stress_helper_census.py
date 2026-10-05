"""Independently count MAM stress helpers and the notes describing them.

The census projects one Scripture stream from MAM-parsed-plus. It counts the
pashta, segolta, telisha qetanah, telisha gedolah and zarqa configurations, with
inclusive Aleppo coverage from the public index. The pashta positional test is
implemented here independently of the build. Source clauses describing doubled
marks retain their sigla and qualifications.
"""

import sys
from collections import Counter

from near_aleppo.census import census_paths
from near_aleppo.census import nusach_aleppo_readings as nar
from near_aleppo.census import nusach_codex_extant as nce
from near_aleppo.census.edition_projection import (
    EDITION_SEPARATOR_TEMPLATE_NAMES,
    edition_parameter_keys,
)
from mb_cmn import bib_locales as tbn
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import ws_tmpl2 as wtp

MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
PASHTA = "\N{HEBREW ACCENT PASHTA}"
SEGOLTA = "\N{HEBREW ACCENT SEGOL}"
TELISHA_QETANA = "\N{HEBREW ACCENT TELISHA QETANA}"
TELISHA_GEDOLA = "\N{HEBREW ACCENT TELISHA GEDOLA}"
ZARQA = "\N{HEBREW ACCENT ZARQA}"
ZINOR = "\N{HEBREW ACCENT ZINOR}"

LETTERS = frozenset(chr(c) for c in range(0x05D0, 0x05EB))
# U+0591 to U+05C7, the CGJ and the varika each belong to the letter before them.
MARKS = frozenset(chr(c) for c in range(0x0591, 0x05C8)) | {
    "\N{COMBINING GRAPHEME JOINER}",
    "\N{HEBREW POINT JUDEO-SPANISH VARIKA}",
}
# The accents whose stress helper is the same codepoint, in the order printed.
REPEATED = (
    (PASHTA, "pashta"),
    (SEGOLTA, "segolta"),
    (TELISHA_GEDOLA, "telisha gedolah"),
    (TELISHA_QETANA, "telisha qetanah"),
)
PHRASES = ("טעם כפול", "הטעמה כפולה")


def render(w):
    """The base text under the edition projection, a separator template as a space."""
    if isinstance(w, str):
        return w
    if isinstance(w, (list, tuple)):
        return "".join(render(x) for x in w)
    if isinstance(w, dict) and wtp.is_template(w):
        if wtp.template_name(w) in EDITION_SEPARATOR_TEMPLATE_NAMES:
            return " "
        keys = edition_parameter_keys(w)
        return "".join(render(wtp.template_param_val(w, k)) for k in keys)
    return ""


def atoms(text):
    """Each atom of ``text`` as a list of its letters' marks, one string per letter."""
    out, current = [], []
    for char in text:
        if char.isspace() or char == MAQAF:
            if current:
                out.append(current)
            current = []
        elif char in LETTERS:
            current.append("")
        elif char in MARKS and current:
            current[-1] += char
    if current:
        out.append(current)
    return out


def where(bkid, bcvt):
    extant = nce.extant(bkid, tbn.bcvt_get_chnu(bcvt), tbn.bcvt_get_vrnu(bcvt))
    return "extant" if extant else "lost"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    counts = Counter()
    notes = []
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=census_paths.mam_parsed_path())
    for bkid in tbn.ALL_BK39_IDS:
        if bkid not in books:
            continue
        for bcvt, minirow in books[bkid]["verses_plus"].items():
            place = where(bkid, bcvt)
            for atom in atoms(render(list(minirow.EP))):
                for mark, name in REPEATED:
                    on = [i for i, marks in enumerate(atom) if mark in marks]
                    if len(on) < 2:
                        continue
                    counts[name, place] += 1
                    if mark == PASHTA and on[0] == len(atom) - 2:
                        counts["pashta, second-to-last", place] += 1
                if any(ZARQA in m for m in atom) and any(ZINOR in m for m in atom):
                    counts["zarqa", place] += 1
            found = []
            nar.each_nusach(list(minirow.EP), found)
            for tmpl in found:
                for clause in nar.clauses(wtp.template_param_val(tmpl, "2")):
                    shape, _, _ = nar.split_clause(clause)
                    if shape == "agree" and any(p in clause for p in PHRASES):
                        bk, ch, vr = tbn.bcvt_get_bcv_triple(bcvt)
                        notes.append(f"{bk} {ch}:{vr}, {place}: {clause.strip()}")

    def line(label, key):
        extant, lost = counts[key, "extant"], counts[key, "lost"]
        print(f"{label}: extant {extant}, lost {lost}, total {extant + lost}")

    line("pashta atoms with a stress helper", "pashta")
    line(
        "  of those, with the stress helper on the second-to-last letter",
        "pashta, second-to-last",
    )
    line("segolta atoms with a stress helper", "segolta")
    line("telisha gedolah atoms with a stress helper", "telisha gedolah")
    line("telisha qetanah atoms with a stress helper", "telisha qetanah")
    line(
        "zarqa atoms with a stress helper, Unicode ZARQA with Unicode ZINOR",
        "zarqa",
    )
    print(f"notes whose agreeing clause speaks of a doubled accent: {len(notes)}")
    for note in notes:
        print(f"  {note}")
