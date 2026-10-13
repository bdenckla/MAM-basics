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
        ("DAN-2-17", "ch4:L642", "Daniel 2:17/2/0", ["Daniel", 2, 17]),
        ("DAN-5-7", "ch4:L217", "Daniel 5:7/2/1", ["Daniel", 5, 7]),
        ("PS-39-13", "ch2:L617", "Psalms 39:13/2/0", ["Psalms", 39, 13]),
        ("PS-17-14", "ch2:L649", "Psalms 17:14/2/0", ["Psalms", 17, 14]),
        ("ISA-10-15", "ch5:L130", "Isaiah 10:15/2/0", ["Isaiah", 10, 15]),
        ("JOSH-14-7", "ch5:L304", "Joshua 14:7/2/0", ["Joshua", 14, 7]),
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
            raw_flat = raw_body.replace("{{ש}}", "\n").replace(
                "{{מ:לגרמיה-2}}", "\N{HEBREW PUNCTUATION PASEQ}"
            )
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
        elif name == "DAN-2-17":
            intro_form = next(
                w
                for w in ATOMS.findall(source)
                if audit.LETTERS.sub("", w) == "דניאל"
                and any(unicodedata.category(c) == "Mn" for c in w)
            )
            note_form = next(
                w for w in ATOMS.findall(body) if audit.LETTERS.sub("", w) == "דניאל"
            )
            if (
                "\N{HEBREW POINT METEG}" not in intro_form
                or "\N{HEBREW POINT METEG}" in note_form
            ):
                raise ValueError("Daniel meteg discrepancy changed")
        elif name == "DAN-5-7":
            intro_form = ATOMS.findall(source.split("ל=[", 1)[1])[0]
            note_form = ATOMS.findall(body.split("ל-כתיב=", 1)[1])[0]
            if (
                audit.LETTERS.sub("", intro_form) != "והמוניכא"
                or audit.LETTERS.sub("", note_form) != "והמונכא"
            ):
                raise ValueError("Daniel ketiv YOD discrepancy changed")
        elif name == "PS-39-13":
            intro_form = ATOMS.findall(source.split("ל=", 1)[1])[0]
            note_form = ATOMS.findall(body.split("\nל=", 1)[1])[0]
            # The mark identities occur in opposite base-letter clusters.
            intro_clusters = re.findall(r"[\u05d0-\u05ea][^\u05d0-\u05ea]*", intro_form)
            note_clusters = re.findall(r"[\u05d0-\u05ea][^\u05d0-\u05ea]*", note_form)
            if not (
                "\N{HEBREW ACCENT MERKHA}" in intro_clusters[0]
                and "\N{HEBREW POINT METEG}" in note_clusters[0]
                and "\N{HEBREW POINT METEG}" in intro_clusters[2]
                and "\N{HEBREW ACCENT MERKHA}" in note_clusters[2]
            ):
                raise ValueError("Psalm 39:13 mark placement changed")
        elif name == "PS-17-14":
            intro_forms = [
                s.split("{{", 1)[0]
                for s in re.findall(r'"([^"]+)"', source.split("ל=", 1)[1])
            ]
            note_forms = re.findall(
                r"<([^>]+)>", body.split("\nל=", 1)[1].split("\n", 1)[0]
            )
            if (
                len(intro_forms) != 2
                or len(note_forms) != 2
                or any("\N{HEBREW PUNCTUATION MAQAF}" in f for f in intro_forms)
                or not all("\N{HEBREW PUNCTUATION MAQAF}" in f for f in note_forms)
            ):
                raise ValueError("Psalm 17:14 candidate maqaf difference changed")
            intro_form, note_form = intro_forms[0], note_forms[0]
        elif name == "ISA-10-15":
            intro_form = ATOMS.findall(source)[0]
            note_form = ATOMS.findall(body.split("\nא=", 1)[1])[0]
            if (
                audit.LETTERS.sub("", intro_form) != "מרימו"
                or audit.LETTERS.sub("", note_form) != "מרמיו"
            ):
                raise ValueError("Isaiah missing-yod position changed")
        elif name == "JOSH-14-7":
            intro_form = claims[cid]["forms"][0]["form"]
            note_form = notes[nid]["target_node"]
            if (
                intro_form.count("\N{HEBREW POINT METEG}") != 2
                or note_form.count("\N{HEBREW POINT METEG}") != 1
                or not body.startswith("=א?,ל")
            ):
                raise ValueError("Joshua selected meteg/certainty control changed")
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
                "raw_vs_parsed_relation": "equal after explicit MAM mark-order comparison and known line-separator / legarmeh-2 survey serialization; raw templates remain preserved",
                **(
                    {"intro_candidates": intro_forms, "note_candidates": note_forms}
                    if name == "PS-17-14"
                    else {}
                ),
            }
        )
    audit.dump("codepoint-proofs.json", result)
    print(
        f"Verified {len(result)} selected raw/parsed source pairs and accent identities"
    )
    descriptions = []
    for cid, nid, ref, letters in [
        ("ch3:L853", "Exodus 7:20/2/0", ["Exodus", 7, 20], "ויהפכו"),
        ("ch3:L1002", "Numbers 16:27/2/0", ["Numbers", 16, 27], "קרח"),
        ("ch3:L1008", "Numbers 22:23/2/0", ["Numbers", 22, 23], "הדרך"),
        ("ch3:L1117", "Deuter 28:27/2/0", ["Deuter", 28, 27], "ובטחרים"),
    ]:
        context = review.context(ref)
        body = notes[nid]["body_text"]
        equivalent = []
        for template in mwparserfromhell.parse(context["wikitext"]).filter_templates():
            if str(template.name) != "נוסח":
                continue
            raw_body = str(template.get("2").value)
            if uni_denorm.give_std_mark_order(
                raw_body.replace("{{ש}}", "\n")
            ) == uni_denorm.give_std_mark_order(body):
                equivalent.append(raw_body)
        if len(equivalent) != 1:
            raise ValueError(f"Description note lacks raw-cache agreement: {cid}")
        intro_form = next(
            w
            for w in ATOMS.findall(claims[cid]["text"])
            if audit.LETTERS.sub("", w) == letters
        )
        note_form = next(
            w for w in ATOMS.findall(body) if audit.LETTERS.sub("", w) == letters
        )
        if uni_denorm.give_std_mark_order(intro_form) != uni_denorm.give_std_mark_order(
            note_form
        ):
            raise ValueError(f"Description control's specimen differs: {cid}")
        descriptions.append(
            {
                "claim": cid,
                "note_id": nid,
                "raw_note_body": equivalent[0],
                "parsed_note_body": body,
                "intro_form": intro_form,
                "note_form": note_form,
                "codepoints": codepoints(note_form),
                "result": "Quoted atom forms agree after explicit mark-order comparison; description-name disagreement is separately reviewed.",
            }
        )
    audit.dump("description-proofs.json", descriptions)
    print(
        f"Verified {len(descriptions)} description controls against raw notes and exact quoted forms"
    )
    spelling_prose = []
    for cid, nid, ref, letter, incorrect_label in [
        ("ch3:L153", "Numbers 9:7/2/0", ["Numbers", 9, 7], "י", 'מלא וי"ו'),
        ("ch3:L211", "Deuter 32:34/2/0", ["Deuter", 32, 34], "ו", 'מלא יו"ד'),
        ("ch3:L186", "Deuter 6:21/2/0", ["Deuter", 6, 21], "", ""),
    ]:
        context = review.context(ref)
        note = notes[nid]
        body = note["body_text"]
        raw_matches = [
            t
            for t in mwparserfromhell.parse(context["wikitext"]).filter_templates()
            if str(t.name) == "נוסח"
            and uni_denorm.give_std_mark_order(
                str(t.get("2").value).replace("{{ש}}", "\n")
            )
            == uni_denorm.give_std_mark_order(body)
        ]
        if len(raw_matches) != 1 or not isinstance(note["target_node"], str):
            raise ValueError(f"Spelling prose control lacks unique raw evidence: {cid}")
        target = note["target_node"]
        raw_target = str(raw_matches[0].get("1").value)
        intro_selected = re.search(r"\[([^\]]+)\]\*", claims[cid]["text"])[1]
        if not (
            uni_denorm.give_std_mark_order(raw_target)
            == uni_denorm.give_std_mark_order(target)
            == uni_denorm.give_std_mark_order(intro_selected)
        ):
            raise ValueError(f"Spelling selected form control changed: {cid}")
        if letter:
            opposite = "ו" if letter == "י" else "י"
            if (
                letter not in target
                or opposite in target
                or incorrect_label not in body
            ):
                raise ValueError(f"Spelling prose letter identity changed: {cid}")
        elif not body.startswith("=ל,") or "\nל!=" not in body:
            raise ValueError("Duplicate Leningrad source relation changed")
        spelling_prose.append(
            {
                "claim": cid,
                "note_id": nid,
                "raw_path": context["path"],
                "raw_note_body": str(raw_matches[0].get("2").value),
                "parsed_note_body": body,
                "raw_target": raw_target,
                "parsed_target": target,
                "intro_selected": intro_selected,
                "codepoints": codepoints(target),
                "result": "Raw target, parsed target and Introduction selection agree after explicit MAM mark-order comparison. The note's letter-label or duplicate source relation is separately reviewed.",
            }
        )
    audit.dump("spelling-prose-proofs.json", spelling_prose)
    print(
        f"Verified {len(spelling_prose)} note-prose controls against raw bodies and selected forms"
    )
    letter_sizes = []
    for cid, nid, ref in [
        ("ch5:L215", "2Samuel 21:19/2/0", ["2Samuel", 21, 19]),
        ("ch5:L220", "Jeremiah 39:13/2/0", ["Jeremiah", 39, 13]),
    ]:
        note = notes[nid]
        context = review.context(ref)
        raw_matches = [
            t
            for t in mwparserfromhell.parse(context["wikitext"]).filter_templates()
            if str(t.name) == "נוסח"
            and uni_denorm.give_std_mark_order(
                str(t.get("2").value).replace("{{ש}}", "\n")
            )
            == uni_denorm.give_std_mark_order(note["body_text"])
        ]
        target = note["target_node"]
        if (
            len(raw_matches) != 1
            or target["tmpl_name"] != "מ:אות-מיוחדת-במילה"
            or target["tmpl_params"]["4"] != "ק"
            or "{{מ:אות-ק|" not in claims[cid]["text"]
            or "גדולה" not in note["body_text"]
        ):
            raise ValueError(f"Special-letter size control changed: {cid}")
        raw_target = str(raw_matches[0].get("1").value)
        if "{{מ:אות-ק|" not in raw_target:
            raise ValueError(
                f"Raw target does not confirm small-letter template: {cid}"
            )
        letter_sizes.append(
            {
                "claim": cid,
                "note_id": nid,
                "raw_path": context["path"],
                "raw_target": raw_target,
                "parsed_target": target,
                "raw_note_body": str(raw_matches[0].get("2").value),
                "parsed_note_body": note["body_text"],
                "result": "Both Introduction and raw/parsed edition targets mark a small letter; the note's implicit-edition clause says large.",
            }
        )
    audit.dump("letter-size-proofs.json", letter_sizes)
    print(f"Verified {len(letter_sizes)} raw/parsed special-letter size controls")
