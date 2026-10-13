"""Supplemental structural populations, with the existing closed EP projection."""

import ctypes
import json
import os
from collections import Counter

from mb_cmn import kq_special_templates as kq
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
    verse_count = 0

    def walk(value, ref, path, pointer):
        if isinstance(value, str):
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
