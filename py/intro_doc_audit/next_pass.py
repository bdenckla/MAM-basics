"""Save incremental human assessments and their independently checked cache evidence."""

import json
import re

import mwparserfromhell

from mb_cmn import uni_denorm
from intro_doc_audit import audit, proofs, review


def raw_note_proof(note):
    """Match one retained note body to the faithful raw verse, keeping both copies."""
    # Book names can contain spaces; the retained canonical reference owns parsing.
    book, chapter, verse = re.fullmatch(r"(.+) (\d+):(\d+)", note["ref"]).groups()
    context = review.context([book, int(chapter), int(verse)])
    matches = []
    for template in mwparserfromhell.parse(context["wikitext"]).filter_templates():
        if str(template.name) != "נוסח":
            continue
        raw_body = str(template.get("2").value)
        code = mwparserfromhell.parse(raw_body)
        for child in reversed(code.filter_templates()):
            name = str(child.name)
            if name == "ש":
                code.replace(child, "\n")
            elif name in {"מ:לגרמיה-2", "מ:פסק"}:
                code.replace(child, "\N{HEBREW PUNCTUATION PASEQ}")
            elif name in {"מ:אות-ג", "מ:אות-ק", "מ:אות תלויה", "מודגש"}:
                code.replace(child, str(child.get("1").value))
            elif name in {"מ:קישור בהערה", "מ:קישור פנימי בהערה"}:
                code.replace(child, str(child.get("2").value))
            else:
                raise ValueError(
                    f"Unclassified raw-note comparison template at {note['id']}: {name}"
                )
        comparison = str(code)
        if uni_denorm.give_std_mark_order(comparison) == uni_denorm.give_std_mark_order(
            note["body_text"]
        ):
            matches.append(raw_body)
    if len(matches) != 1:
        raise ValueError(f"Incremental evidence lacks one raw-note match: {note['id']}")
    return {
        "note_id": note["id"],
        "raw_path": context["path"],
        "raw_note_body": matches[0],
        "parsed_path": note["path"],
        "parsed_pointer": note["json_pointer"],
        "parsed_note_body": note["body_text"],
        "chapter_revision": note["chapter_revision"],
        "source_url": note["source_url"],
        "comparison": "MAM mark order plus the current explicit line-separator, legarmeh-2 and special-letter visible serializations; both faithful bodies retained",
    }


def main():
    source = review.read("next-pass-assessment-input.json")
    claims = {c["id"]: c for c in review.read("claims.json")}
    notes = {n["id"]: n for n in review.read("notes.json")}
    uncertainty = {
        c["id"]: c for c in review.read("review-selections.json")["uncertainty"]
    }
    ids = [r["id"] for r in source["uncertainty_assessments"]]
    if len(ids) != len(set(ids)) or set(ids) != set(uncertainty):
        raise ValueError(
            "Incremental pass must account for all original uncertainty groups"
        )
    assessments = []
    for row in source["uncertainty_assessments"]:
        prior = uncertainty[row["id"]]
        claim_ids = list(
            dict.fromkeys(prior["claims"] + row.get("evidence_claims", []))
        )
        note_ids = list(dict.fromkeys(prior["note_ids"] + row.get("note_ids", [])))
        assessments.append(
            {
                **row,
                "claims": [
                    {
                        k: claims[cid][k]
                        for k in ("id", "text", "path", "line", "source_url", "topic")
                    }
                    for cid in claim_ids
                ],
                "notes": [
                    {
                        k: notes[nid][k]
                        for k in (
                            "id",
                            "target_node",
                            "body_text",
                            "path",
                            "json_pointer",
                            "source_url",
                            "chapter_revision",
                        )
                    }
                    for nid in note_ids
                ],
                "remaining_uncertainty": True,
            }
        )
    unsigned = []
    hataf_case = next(
        r for r in source["uncertainty_assessments"] if r["id"] == "HATAF-SOURCE-SCOPE"
    )
    for cid, index in hataf_case["roster_items"]:
        item = review.roster_items()[cid][index - 1]
        counterparts = []
        for candidate in item["candidate_notes"]:
            extraction = candidate["first_xataf_extraction"]
            if (
                extraction
                and (extraction.get("sigla_detail") or {}).get("sigla") == "א"
            ):
                form = extraction["form"]
                literal = re.sub(r" \[[12]\]$", "", item["literal_specimen"][1:-1])
                if uni_denorm.give_std_mark_order(
                    form
                ) == uni_denorm.give_std_mark_order(literal):
                    counterparts.append((candidate["note_id"], form))
        if len(counterparts) != 1:
            raise ValueError(
                f"Unsigled hataf lacks one explicit Aleppo counterpart: {item['id']}"
            )
        nid, form = counterparts[0]
        unsigned.append(
            {
                "item": item["id"],
                "ref": audit.ref_id(item["reviewed_ref"]),
                "intro_literal_specimen": item["literal_specimen"],
                "note_id": nid,
                "note_literal_form": form,
                "source_relation": "explicit Aleppo counterpart in current note; source not supplied by guessing the unsigled item",
                "raw_note_evidence": raw_note_proof(notes[nid]),
            }
        )
    proof_ids = [
        "Deuter 32:6/2/0",
        "2Kings 14:7/2/0",
        "Daniel 2:41/2/1",
        "2Samuel 8:3/2/0",
        "Psalms 6:3/2/0",
        "Proverbs 8:34/2/0",
        "Psalms 68:18/2/0",
        "Psalms 74:5/2/0",
        "Exodus 14:5/2/0",
        "Exodus 14:13/2/1",
        "Psalms 3:1/2/0",
        "Psalms 106:1/2/1",
    ]
    raw_proofs = [raw_note_proof(notes[nid]) for nid in proof_ids]
    prior_hataf = review.read("hataf-rosters.json")["reviewed_item_dispositions"]
    prior_central = prior_hataf["central-source-and-hataf-correspondence"]
    if len(unsigned) != prior_hataf["unlabelled-source-specimen"]:
        raise ValueError(
            "Incremental unsigled overlay no longer matches the prior roster boundary"
        )
    intro_form = claims["ch3:L246"]["text"].split("ל=[", 1)[1].split("]", 1)[0]
    note_form = (
        notes["Deuter 32:6/2/0"]["body_text"].split("\nל=", 1)[1].split(" (", 1)[0]
    )
    intro_yod = next(
        s for s in re.findall(r"[א-ת][^א-ת]*", intro_form) if s.startswith("י")
    )
    note_yod = next(
        s for s in re.findall(r"[א-ת][^א-ת]*", note_form) if s.startswith("י")
    )
    if (
        "\N{HEBREW POINT SHEVA}" in intro_yod
        or "\N{HEBREW POINT SHEVA}" not in note_yod
    ):
        raise ValueError("Deuteronomy incidental yod SHEVA comparison changed")
    result = {
        "author": source["author"],
        "date": source["date"],
        "source_base_commit": audit.pinned_commit(),
        "previous_audit_commit": source["previous_audit_commit"],
        "scope": source["scope"],
        "uncertainty_groups_reviewed": len(assessments),
        "uncertainty_groups_total": len(uncertainty),
        "assessments": assessments,
        "nine_unsigled_hataf_counterparts": unsigned,
        "hataf_incremental_overlay": {
            "original_central_correspondence": prior_central,
            "resolved_unsigled_counterparts": len(unsigned),
            "current_central_correspondence": prior_central + len(unsigned),
            "remaining_item_scope_or_quotation_limits": sum(prior_hataf.values())
            - prior_central
            - len(unsigned),
            "total_items": sum(prior_hataf.values()),
            "method": "Retain the original roster ledger as prior evidence; overlay the nine independently raw-matched named-source counterparts. No full roster rerun.",
        },
        "independent_raw_note_proofs": raw_proofs,
        "deuteronomy_yod_sheva": {
            "intro_claim": "ch3:L246",
            "intro_literal_form": intro_form,
            "note_id": "Deuter 32:6/2/0",
            "note_literal_form": note_form,
            "intro_codepoints": proofs.codepoints(intro_form),
            "note_codepoints": proofs.codepoints(note_form),
            "boundary": "Literal quoted difference established; central joining agrees and complete-quotation intent remains editorial.",
        },
        "catalogue_scope": {
            "line_differences": [
                "ch2:L87",
                "appendices:L375",
                "ch2:L112",
                "appendices:L383",
            ],
            "underlying_verse_cases": ["2Samuel 8:3", "2Samuel 21:12"],
            "repeated_wrong_locator": {
                "linked": "Jeremiah 31:38",
                "intended": "Jeremiah 31:37",
                "already_in_locator_family": True,
            },
            "resolved_internal_count_difference": {
                "claims": [
                    "ch2:L109",
                    "ch2:L112",
                    "appendices:L381",
                    "appendices:L382",
                ],
                "chapter_total": 3,
                "appendix_total": 4,
                "chapter_non_maqaf_members": ["Ezekiel 9:11"],
                "appendix_non_maqaf_members": ["2Samuel 8:3", "Ezekiel 9:11"],
                "note_id": "2Samuel 8:3/2/0",
            },
            "boundary": "2 Samuel 8:3 has a current one-ketiv/two-different-qere typed target and an Aleppo qere clause for both atoms; Leningrad/other-source clauses also describe the traditional qere-only final atom. Traditional atom-level phenomena and unified modern template identity need not be mutually exclusive. 2 Samuel 21:12's three-atom scope is already reviewed; no duplicate new finding.",
        },
    }
    audit.dump("next-pass-assessments.json", result)
    print(
        json.dumps(
            {
                "uncertainty_groups_accounted": len(assessments),
                "unsigled_hataf_counterparts": len(unsigned),
                "independent_raw_note_matches": len(raw_proofs) + len(unsigned),
                "catalogue_line_differences_explained_by_verse_cases": "4 / 2",
            },
            indent=2,
        )
    )
