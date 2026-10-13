"""Independent raw-cache checks for selected findings, with literal codepoints."""

import json
import re
import unicodedata

import mwparserfromhell

from mb_cmn import uni_denorm
from intro_doc_audit import audit, review

ATOMS = re.compile(r"[\u05d0-\u05ea\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7]+")


def codepoints(value):
    return [
        {
            "character": c,
            "codepoint": f"U+{ord(c):04X}",
            "name": unicodedata.name(c, "unnamed"),
        }
        for c in value
    ]


def main():
    claims = {c["id"]: c for c in review.read("claims.json")}
    notes = {n["id"]: n for n in review.read("notes.json")}
    cases = [
        ("JER-31-37", "ch5:L458", "Jeremiah 31:37/2/0", ["Jeremiah", 31, 37]),
        ("PS-108-11", "ch5:L605", "Psalms 108:11/2/0", ["Psalms", 108, 11]),
        ("PS-57-9", "ch5:L583", "Psalms 57:9/2/0", ["Psalms", 57, 9]),
        ("PS-108-3", "ch5:L603", "Psalms 108:3/2/0", ["Psalms", 108, 3]),
    ]
    result = []
    for name, cid, nid, ref in cases:
        context = review.context(ref)
        raw_notes = [
            t
            for t in mwparserfromhell.parse(context["wikitext"]).filter_templates()
            if str(t.name) == "נוסח"
        ]
        body = notes[nid]["body_text"]
        equivalent = []
        for t in raw_notes:
            raw_body = str(t.get("2").value)
            raw_flat = raw_body.replace("{{ש}}", "\n")
            if uni_denorm.give_std_mark_order(
                raw_flat
            ) == uni_denorm.give_std_mark_order(body):
                equivalent.append(raw_body)
        if len(equivalent) != 1:
            raise ValueError(
                f"Selected parsed note not independently matched in raw cache: {name}"
            )
        source = claims[cid]["text"]
        if name == "JER-31-37":
            # The label is selected by its letter spelling, never a typed pointed literal.
            words = ATOMS.findall(source)
            intro_form = next(w for w in words if audit.LETTERS.sub("", w) == "יהוה")
            note_form = next(
                w for w in ATOMS.findall(body) if audit.LETTERS.sub("", w) == "יהוה"
            )
            if (
                "\N{HEBREW ACCENT ETNAHTA}" not in intro_form
                or "\N{HEBREW POINT METEG}" not in note_form
            ):
                raise ValueError("Jeremiah accent identity changed")
        elif name == "PS-108-11":
            intro_form = next(
                w for w in ATOMS.findall(source) if audit.LETTERS.sub("", w) == "יבלני"
            )
            note_form = next(
                w for w in ATOMS.findall(body) if audit.LETTERS.sub("", w) == "יבלני"
            )
            if (
                "\N{HEBREW ACCENT TIPEHA}" not in intro_form
                or "\N{HEBREW ACCENT DEHI}" not in note_form
            ):
                raise ValueError("Psalm 108:11 accent identity changed")
        else:
            intro_form = [
                w for w in ATOMS.findall(source) if audit.LETTERS.sub("", w) == "עורה"
            ][-1]
            note_form = [
                w for w in ATOMS.findall(body) if audit.LETTERS.sub("", w) == "עורה"
            ][-1]
            if (
                "\N{HEBREW ACCENT DEHI}" not in intro_form
                or "\N{HEBREW ACCENT TIPEHA}" not in note_form
            ):
                raise ValueError(f"Psalm alternative accent identity changed: {name}")
        result.append(
            {
                "case": name,
                "intro_claim": cid,
                "note_id": nid,
                "raw_path": context["path"],
                "raw_note_body": equivalent[0],
                "parsed_note_body": body,
                "intro_form": intro_form,
                "note_form": note_form,
                "intro_codepoints": codepoints(intro_form),
                "note_codepoints": codepoints(note_form),
                "raw_vs_parsed_relation": "equal after explicit MAM mark-order comparison and known line-separator serialization",
            }
        )
    audit.dump("codepoint-proofs.json", result)
    print(
        f"Verified {len(result)} selected raw/parsed source pairs and accent identities"
    )
