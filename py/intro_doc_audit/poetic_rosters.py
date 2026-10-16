"""Ordered poetic rosters, complete EP pointers, and reviewed evidence boundaries."""

import json
import re
from collections import Counter, defaultdict

import mwparserfromhell

from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import mam_bknas_and_std_bknas as bn
from mb_cmn import uni_denorm
from near_aleppo.census import edition_projection as projection
from intro_doc_audit import audit, proofs, review, rosters


def implicit_items(claim, book):
    code = mwparserfromhell.parse(claim["text"])
    for template in code.filter_templates(recursive=False):
        if str(template.name) == "הערה":
            code.remove(template)
    text = str(code)
    matches = list(re.finditer(r"(?<![א-ת])([א-ת]+),([א-ת]+)\s*\(", text))
    return [
        {
            "id": f"{claim['id']}/item/{i+1}",
            "index": i + 1,
            "literal_specimen": text[
                m.start() : (
                    matches[i + 1].start() if i + 1 < len(matches) else len(text)
                )
            ].strip(),
            "literal_link": "",
            "strict_ref": [book, hvn.STR_TO_INT_DIC[m[1]], hvn.STR_TO_INT_DIC[m[2]]],
            "book_context": "supplied by reviewed roster heading; not inferred from a verse number",
        }
        for i, m in enumerate(matches)
    ]


def selected_leaves(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [leaf for child in value for leaf in selected_leaves(child)]
    # Use the repository's closed template decisions. Never recurse through
    # arbitrary parameters, which could accidentally include note bodies.
    params = value.get("tmpl_params", {})
    keys = projection.edition_parameter_keys_for(value["tmpl_name"], params.keys())
    return [leaf for key in keys for leaf in selected_leaves(params[key])]


def main():
    adjudication = review.read("poetic-roster-review.json")
    claims = {c["id"]: c for c in review.read("claims.json")}
    notes = defaultdict(list)
    for note in review.read("notes.json"):
        notes[note["ref"]].append(note)
    rows = []
    for entry in adjudication["rosters"]:
        claim = claims[entry["claim"]]
        items = (
            implicit_items(claim, entry["book"])
            if entry.get("book")
            else rosters.literal_items(claim)
        )
        if len(items) != entry["total"]:
            raise ValueError(f"Poetic roster count changed: {claim['id']}")
        correspondence = set(entry.get("correspondence_items", []))
        feature_only = set(entry.get("feature_only_items", []))
        concern = set(entry.get("qualification_items", []))
        if entry.get("default_correspondence"):
            correspondence = set(range(1, len(items) + 1)) - feature_only - concern
        if correspondence | feature_only | concern != set(
            range(1, len(items) + 1)
        ) or len(correspondence) + len(feature_only) + len(concern) != len(items):
            raise ValueError(f"Incomplete item dispositions: {claim['id']}")
        for item in items:
            item["status"] = (
                "central-named-source-correspondence"
                if item["index"] in correspondence
                else (
                    "qualification-or-representation-concern"
                    if item["index"] in concern
                    else "selected-feature-only-pertinent-source-statement-absent"
                )
            )
            item["selected_feature_status"] = "reviewed-central-feature-correspondence"
            candidate = notes[audit.ref_id(item["strict_ref"])]
            item["candidate_note_ids"] = [n["id"] for n in candidate]
            item["candidate_note_source_pointers"] = [
                {
                    "id": n["id"],
                    "source_url": n["source_url"],
                    "json_pointer": n["json_pointer"],
                }
                for n in candidate
            ]
            item["source_form_routing"] = [
                {
                    "note_id": n["id"],
                    "literal_form_present": any(
                        f["literal_form"] in n["body_text"]
                        for f in item.get("forms", [])
                    ),
                    "MAM_order_form_present": any(
                        uni_denorm.give_std_mark_order(f["literal_form"])
                        in uni_denorm.give_std_mark_order(n["body_text"])
                        for f in item.get("forms", [])
                    ),
                }
                for n in candidate
            ]
            item["overlapping_scope_flags"] = adjudication["scope_flags"].get(
                item["id"], []
            )
        rows.append(
            {
                "claim": claim["id"],
                "source_url": claim["source_url"],
                "kind": entry["kind"],
                "reviewed": len(items),
                "total": len(items),
                "items": items,
            }
        )
    wanted = {audit.ref_id(i["strict_ref"]) for row in rows for i in row["items"]}
    edition = {}
    for path in sorted((audit.ROOT / "MAM-parsed/plus").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for book_index, book in enumerate(data["book39s"]):
            book_id = bn.MAM_HBNP_TO_BK39ID[
                (book["book24_name"], book["sub_book_name"])
            ]
            for chapter, verses in book["chapters"].items():
                for verse, cells in verses.items():
                    ref = f"{book_id} {chapter}:{verse}"
                    if ref in wanted:
                        edition[ref] = {
                            "path": path.relative_to(audit.ROOT).as_posix(),
                            "json_pointer": f"/book39s/{book_index}/chapters/{chapter}/{verse}/2",
                            "complete_EP": cells[2],
                        }
    paired = 0
    for row in rows:
        for item in row["items"]:
            ref = audit.ref_id(item["strict_ref"])
            item["edition_evidence"] = edition[ref]
            if row["kind"] == "revia-omission":
                clusters = [
                    cluster
                    for leaf in selected_leaves(edition[ref]["complete_EP"])
                    for atom in proofs.ATOMS.findall(leaf)
                    for cluster in rosters.CLUSTER.findall(atom)
                ]
                if not any(
                    "\N{HEBREW ACCENT GERESH MUQDAM}" in c
                    and "\N{HEBREW ACCENT REVIA}" in c
                    for c in clusters
                ):
                    raise ValueError(f"Selected geresh-muqdam/revia pair absent: {ref}")
                paired += 1
    result = {
        "method": "Ordered AST links for explicit rosters; chapter/verse numeral spans plus reviewed book heading for implicit rosters. Annotation links excluded from main populations. Complete EP retained and current closed EP projection used; no note-body descent. Exact note nodes and full source text remain in notes.json and claims.json. Form presence is routing only; semantic dispositions are reviewer assessments.",
        "limits": adjudication["limits"],
        "reviewed": sum(r["reviewed"] for r in rows),
        "total": 385,
        "explicit_items": 125,
        "implicit_items": 260,
        "selected_paired_geresh_muqdam_revia_items": paired,
        "source_dispositions": dict(
            Counter(i["status"] for r in rows for i in r["items"])
        ),
        "rosters": rows,
    }
    if result["reviewed"] != 385 or paired != 260:
        raise ValueError("Poetic roster denominator changed")
    audit.dump("poetic-rosters.json", result)
    print(
        json.dumps(
            {
                k: v
                for k, v in result.items()
                if k not in {"rosters", "method", "limits"}
            },
            indent=2,
        )
    )
