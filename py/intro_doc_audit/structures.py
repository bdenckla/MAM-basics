"""Supplemental structural populations, with the existing closed EP projection."""

import ctypes
import json
import os
import re
import unicodedata
from collections import Counter

from mb_cmn import kq_special_templates as kq
from mb_cmn import bib_locales as bl
from mb_cmn import mam_bknas_and_std_bknas as bn
from mb_cmn import template_names as tn
from mb_cmn import ws_tmpl2 as wtp
from near_aleppo.census import edition_projection as projection
from intro_doc_audit import audit


def main():
    if os.name == "nt":
        kernel = ctypes.windll.kernel32
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.SetPriorityClass.argtypes = (ctypes.c_void_p, ctypes.c_uint)
        if not kernel.SetPriorityClass(kernel.GetCurrentProcess(), 0x4000):
            raise ctypes.WinError()
    records = []
    character_records = []
    combined_atom_records = []
    verse_count = 0
    poetic_verse_count = 0
    additional_characters = ("\N{HEBREW ACCENT DEHI}", "\N{HEBREW ACCENT OLE}")
    additional_counts = Counter()
    additional_refs = {char: set() for char in additional_characters}
    selected_marks = (
        "\N{HEBREW ACCENT SHALSHELET}",
        "\N{HEBREW ACCENT MERKHA KEFULA}",
        "\N{HEBREW ACCENT QARNEY PARA}",
        "\N{HEBREW ACCENT YERAH BEN YOMO}",
    )

    def walk(value, ref, path, pointer):
        if isinstance(value, str):
            book, cv = ref.rsplit(" ", 1)
            chapter, verse = map(int, cv.split(":"))
            poetic = bl.is_poetcant(bl.mk_bcvtmam(book, chapter, verse))
            for char in additional_characters:
                if char in value:
                    additional_counts[char] += value.count(char)
                    additional_refs[char].add(ref)
            for char in selected_marks:
                if char in value:
                    character_records.append(
                        {
                            "ref": ref,
                            "path": path,
                            "json_pointer": pointer,
                            "literal_text": value,
                            "character_name": unicodedata.name(char),
                            "instances": value.count(char),
                            "is_poetcant": poetic,
                        }
                    )
            for atom in re.findall(
                r"[\u05d0-\u05ea\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7\u034f\ufb1e]+",
                value,
            ):
                if "\N{HEBREW ACCENT TELISHA GEDOLA}" in atom and (
                    "\N{HEBREW ACCENT GERESH}" in atom
                    or "\N{HEBREW ACCENT GERSHAYIM}" in atom
                ):
                    combined_atom_records.append(
                        {
                            "ref": ref,
                            "path": path,
                            "json_pointer": pointer,
                            "literal_atom": atom,
                        }
                    )
            return
        if isinstance(value, list):
            for i, child in enumerate(value):
                walk(child, ref, path, f"{pointer}/{i}")
            return
        tn.validate_current_plus_template(value)
        keys = projection.edition_parameter_keys(value)
        name = wtp.template_name(value)
        category = None
        if name == kq.UNIFIED_SPECIAL_KQ_TEMPLATE_NAME:
            category = kq.canonical_special_kq_type_from_name_and_sug(
                name, value["tmpl_params"]["סוג"]
            )
        elif name in ("קרי ולא כתיב", "כתיב ולא קרי", "מ:מקף אפור", "מ:קו״כ-אם-2"):
            category = name
        if category:
            records.append(
                {
                    "ref": ref,
                    "path": path,
                    "json_pointer": pointer,
                    "category": category,
                    "node": value,
                }
            )
        for key in keys:
            walk(value["tmpl_params"][key], ref, path, f"{pointer}/tmpl_params/{key}")

    for path in sorted((audit.ROOT / "MAM-parsed/plus").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for b, book in enumerate(data["book39s"]):
            bkid = bn.MAM_HBNP_TO_BK39ID[(book["book24_name"], book["sub_book_name"])]
            for chapter, rows in book["chapters"].items():
                for verse, cells in rows.items():
                    if not verse.isdigit() or verse == "0":
                        continue
                    verse_count += 1
                    poetic_verse_count += bl.is_poetcant(
                        bl.mk_bcvtmam(bkid, int(chapter), int(verse))
                    )
                    walk(
                        cells[2],
                        f"{bkid} {chapter}:{verse}",
                        path.relative_to(audit.ROOT).as_posix(),
                        f"/book39s/{b}/chapters/{chapter}/{verse}/2",
                    )
    counts = dict(Counter(r["category"] for r in records))
    verse_counts = {
        cat: len({r["ref"] for r in records if r["category"] == cat}) for cat in counts
    }
    result = {
        "projection": "Existing edition_projection: qere, primary stress, qamats ד, combined cantillation; note target only. Structure counted before selecting its child. No note-body recursion and no all-parameters fallback.",
        "verses_scanned": verse_count,
        "instances": counts,
        "distinct_verses": verse_counts,
        "records": records,
    }
    audit.dump("structural-populations.json", result)
    audit.dump(
        "rare-mark-populations.json",
        {
            "verses_scanned": verse_count,
            "poetic_verses_scanned": poetic_verse_count,
            "additional_literal_mark_populations": {
                unicodedata.name(char): {
                    "instances": additional_counts[char],
                    "distinct_verses": len(additional_refs[char]),
                    "verse_membership": sorted(additional_refs[char]),
                }
                for char in additional_characters
            },
            "projection": result["projection"],
            "poetic_predicate": "bib_locales.is_poetcant(mk_bcvtmam(...)), including Job's prose sections",
            "limits": "Counts describe selected edition strings, not manuscript populations. Combined atoms are literal Hebrew runs inside selected leaf strings; the five qualifying atoms are retained with source pointers.",
            "characters": character_records,
            "combined_telisha_geresh_atoms": combined_atom_records,
        },
    )
    print(
        json.dumps(
            {
                "verses_scanned": verse_count,
                "instances": counts,
                "distinct_verses": verse_counts,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
