"""Literal roster joins and mark counts, with no automatic semantic verdict."""

import ctypes
import json
import os
import re
import unicodedata
from collections import Counter, defaultdict

import mwparserfromhell

from explicit_xataf import extract
from mb_cmn import uni_denorm
from sigils import inventory as sigils
from intro_doc_audit import audit, review

SOURCE_FORM = re.compile(
    r"(?<![א-ת0-9])(?P<sigil>[אל](?:-(?:כתיב|קרי))?[?!*]*(?:,[אל][?!*]*)*)=\s*[\[<\"']*(?P<form>[\u0591-\u05ea\u034f\ufb1e −]+)"
)
CLUSTER = re.compile(r"[\u05d0-\u05ea][^\u05d0-\u05ea]*")
DECLARED = re.compile(r"\((\d+) פריט(?:ים)?\)")


def hatafs(form):
    found = []
    for cluster in CLUSTER.findall(form):
        marks = [c for c in cluster if c in extract.XATAF_VOWELS]
        names = [unicodedata.name(c) for c in marks]
        if "\N{HEBREW POINT SHEVA}" in cluster and "\N{HEBREW POINT HIRIQ}" in cluster:
            names.append("SHEVA + HIRIQ in the same base-letter cluster")
        if names:
            found.append(
                {
                    "literal_cluster": cluster,
                    "base": cluster[0],
                    "non_guttural": cluster[0] not in "אהחע",
                    "marks": names,
                }
            )
    return found


def literal_items(claim):
    code = mwparserfromhell.parse(claim["text"])
    # Explicitly exclude annotation links from the main roster population.
    for template in code.filter_templates(recursive=False):
        if str(template.name) == "הערה":
            code.remove(template)
    text = str(code)
    boundaries = []
    offset = 0
    for node in code.nodes:
        raw = str(node)
        if isinstance(node, mwparserfromhell.nodes.Wikilink) and "/טעמים#" in str(
            node.title
        ):
            boundaries.append((offset, offset + len(raw), node))
        offset += len(raw)
    items = []
    for i, (start, end, link) in enumerate(boundaries):
        next_start = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(text)
        specimen = text[end:next_start].strip().rstrip(";").strip()
        forms = []
        for match in SOURCE_FORM.finditer(specimen):
            literal = match["form"].strip()
            forms.append(
                {
                    "sigil": match["sigil"],
                    "literal_expression": match[0],
                    "literal_form": literal,
                    "hatafs": hatafs(literal),
                }
            )
        items.append(
            {
                "id": f"{claim['id']}/item/{i + 1}",
                "index": i + 1,
                "literal_link": str(link),
                "link_target": str(link.title),
                "link_label": str(link.text or link.title),
                "literal_specimen": specimen,
                "strict_ref": audit.resolve_link(str(link.title)),
                "forms": forms,
                "status": "unreviewed-roster-routing",
            }
        )
    return items


def main():
    if os.name == "nt":
        kernel = ctypes.windll.kernel32
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.SetPriorityClass.argtypes = (ctypes.c_void_p, ctypes.c_uint)
        if not kernel.SetPriorityClass(kernel.GetCurrentProcess(), 0x4000):
            raise ctypes.WinError()
    by_ref = defaultdict(list)
    adjudication = review.read("roster-review.json")
    exception_status = {
        item: status
        for status, items in adjudication["exception_dispositions"].items()
        for item in items
    }
    for note in review.read("notes.json"):
        by_ref[note["ref"]].append(note)
    records = []
    for claim in review.read("claims.json"):
        eligible = (
            claim["id"].startswith("ch3:") and 1121 <= claim["line"] <= 1136
        ) or (claim["id"].startswith("ch5:") and 694 <= claim["line"] <= 730)
        if not eligible:
            continue
        match = DECLARED.search(claim["text"])
        declared = (
            int(match[1])
            if match
            else (
                1
                if "(פריט אחד)" in claim["text"]
                else 0 if "(אין פריטים)" in claim["text"] else None
            )
        )
        if declared is None:
            continue
        items = literal_items(claim)
        for item in items:
            original = item["strict_ref"]
            item["literal_target_note_ids"] = (
                [n["id"] for n in by_ref[audit.ref_id(original)]] if original else []
            )
            item["reviewed_ref"] = adjudication["intended_ref_overrides"].get(
                item["id"], original
            )
            item["status"] = exception_status.get(
                item["id"], adjudication["default_disposition"]
            )
            candidates = (
                by_ref[audit.ref_id(item["reviewed_ref"])]
                if item["reviewed_ref"]
                else []
            )
            item["candidate_notes"] = []
            for note in candidates:
                first_form, kind, detail = extract.extract_xataf_word(note["body_node"])
                matches = []
                for form in item["forms"]:
                    literal = form["literal_form"]
                    relation = (
                        "literal-form-present"
                        if literal in note["body_text"]
                        else (
                            "MAM-order-form-present"
                            if uni_denorm.give_std_mark_order(literal)
                            in uni_denorm.give_std_mark_order(note["body_text"])
                            else "form-not-present"
                        )
                    )
                    matches.append(
                        {
                            "intro_expression": form["literal_expression"],
                            "relation": relation,
                        }
                    )
                item["candidate_notes"].append(
                    {
                        "note_id": note["id"],
                        "source_url": note["source_url"],
                        "json_pointer": note["json_pointer"],
                        "first_xataf_extraction": {
                            "form": first_form,
                            "kind": kind,
                            "sigla_detail": detail,
                        },
                        "current_sigil_expressions": {
                            "lhs_equals": list(
                                sigils._lhs_equals_expressions(note["body_text"])
                            ),
                            "leading_equals": list(
                                sigils._leading_equals_expressions(note["body_text"])
                            ),
                        },
                        "form_routing": matches,
                    }
                )
        records.append(
            {
                "claim": claim["id"],
                "source_url": claim["source_url"],
                "declared_items": declared,
                "literal_link_items": len(items),
                "first_form_non_guttural_hataf_occurrences": sum(
                    sum(
                        h["non_guttural"] * len(h["marks"])
                        for h in i["forms"][0]["hatafs"]
                    )
                    for i in items
                    if i["forms"]
                ),
                "items_without_simple_source_form": [
                    i["id"] for i in items if not i["forms"]
                ],
                "items": items,
            }
        )
    result = {
        "method": "Top-level ordered wiki nodes define each item, including repeated identical links. Annotation templates are excluded from the main population. Literal captures remain unchanged; only routing uses explicit MAM mark-order comparison. Current explicit_xataf extraction and sigil expression inventory are reused.",
        "limits": "Simple A/L form extraction and lexical presence do not establish source attribution or semantic consistency. The existing note extractor returns the first matching hataf expression, which may omit other candidates. Declared items may count non-guttural hataf occurrences rather than forms. All semantic verdicts remain in separately reviewed ledgers.",
        "rosters": records,
        "reviewed_item_dispositions": dict(
            Counter(i["status"] for r in records for i in r["items"])
        ),
    }
    all_ids = {i["id"] for r in records for i in r["items"]}
    if (
        len(all_ids) != adjudication["total_items"]
        or not set(exception_status) <= all_ids
        or not set(adjudication["intended_ref_overrides"]) <= all_ids
    ):
        raise ValueError(
            "Roster assessment does not account for its exact literal population"
        )
    audit.dump("hataf-rosters.json", result)
    print(
        json.dumps(
            [{k: v for k, v in r.items() if k != "items"} for r in records],
            ensure_ascii=False,
            indent=2,
        )
    )
