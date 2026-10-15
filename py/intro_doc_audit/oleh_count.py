"""Retain the thirteen listed oleh cases and their manually selected note evidence."""

from collections import Counter

from intro_doc_audit import audit, human_review, rosters
from mb_cmn import uni_denorm
from sigils import inventory as sigils

OLE = "\N{HEBREW ACCENT OLE}"
MERKHA = "\N{HEBREW ACCENT MERKHA}"
ALEF = "\N{HEBREW LETTER ALEF}"
CLAIMS = {"ch5:L743", "ch5:L745", "ch5:L747"}

# These selections are semantic review dispositions, not keyword-search results.
NOTE_IDS = {
    "Psalms 30:12": "Psalms 30:12/2/0",
    "Psalms 42:3": None,
    "Psalms 55:20": "Psalms 55:20/2/1",
    "Psalms 68:20": "Psalms 68:20/2/1",
    "Psalms 86:2": "Psalms 86:2/2/1",
    "Psalms 109:16": "Psalms 109:16/2/0",
    "Psalms 125:2": "Psalms 125:2/2/0",
    "Proverbs 24:24": "Proverbs 24:24/2/0",
    "Proverbs 30:15": "Proverbs 30:15/2/2",
    "Job 8:6": "Job 8:6/2/0",
    "Job 9:22": "Job 9:22/2/0",
    "Job 29:25": "Job 29:25/2/1",
    "Job 34:20": "Job 34:20/2/0",
}
OTHER_NOTES = {
    "Psalms 55:20/2/0": "paseq",
    "Psalms 68:20/2/0": "paseq",
    "Psalms 86:2/2/0": "qamats alternatives",
    "Proverbs 30:15/2/0": "small bet",
    "Proverbs 30:15/2/1": "paseq",
    "Job 29:25/2/0": "a ḥataf vowel",
}


def has_both(form):
    return any(
        OLE in cluster and MERKHA in cluster
        for cluster in rosters.CLUSTER.findall(form)
    )


def build():
    notes = {n["id"]: n for n in human_review.read("notes.json")}
    groups = [
        g
        for g in human_review.read("poetic-rosters.json")["rosters"]
        if g["claim"] in CLAIMS
    ]
    records = []
    for group in groups:
        for item in group["items"]:
            ref = audit.ref_id(item["strict_ref"])
            note_id = NOTE_IDS[ref]
            intro_form = item["literal_specimen"]
            row = {
                "ref": ref,
                "introduction_item": item["id"],
                "introduction": {"claim": group["claim"], "text": intro_form},
                "introduction_complete_specimen": item["literal_specimen"],
                "relevant_note": note_id,
                "candidate_note_ids": item["candidate_note_ids"],
                "unrelated_notes": [
                    {"id": n, "topic": OTHER_NOTES[n]}
                    for n in item["candidate_note_ids"]
                    if n != note_id
                ],
            }
            if note_id:
                note = notes[note_id]
                assert isinstance(note["target_node"], str)
                matches = [
                    m
                    for m in rosters.SOURCE_FORM.finditer(note["body_text"])
                    if ALEF in sigils._split_expression_tokens(m["sigil"])
                ]
                assert len(matches) == 1, ref
                match = matches[0]
                source_form = match["form"].strip()
                main = note["target_node"]
                assert OLE not in source_form and MERKHA in source_form, ref
                assert uni_denorm.give_std_mark_order(
                    main.replace(OLE, "")
                ) == uni_denorm.give_std_mark_order(source_form), ref
                assert uni_denorm.give_std_mark_order(
                    source_form
                ) in uni_denorm.give_std_mark_order(intro_form), ref
                matches_in_intro = [
                    intro_form[i : i + len(source_form)]
                    for i in range(len(intro_form) - len(source_form) + 1)
                    if uni_denorm.give_std_mark_order(
                        intro_form[i : i + len(source_form)]
                    )
                    == uni_denorm.give_std_mark_order(source_form)
                ]
                assert len(matches_in_intro) == 1, ref
                row["introduction"]["text"] = matches_in_intro[0]
                row.update(
                    {
                        "mam_body": {
                            "source": "note-target",
                            "note": note_id,
                            "text": main,
                        },
                        "aleppo_note_form": {"note": note_id, "text": source_form},
                        "complete_note": {"note": note_id, "quote": note["body_text"]},
                        "note_source_url": note["source_url"],
                        "note_json_pointer": note["json_pointer"],
                        "chapter_revision": note["chapter_revision"],
                        "sigil_expression": match["sigil"],
                        "current_sigil_expressions": sigils._lhs_equals_expressions(
                            note["body_text"]
                        ),
                        "status": (
                            "pointing-pair-supported-but-note-calls-omission-revia"
                            if ref == "Psalms 30:12"
                            else "note-explicitly-names-omitted-oleh"
                        ),
                        "comparison": "MAM body minus OLE equals the explicitly attributed Aleppo form after comparison-only MAM mark ordering.",
                        "mark_delta": {
                            "MAM_additional_codepoint": "U+05AB HEBREW ACCENT OLE",
                            "shared_mark": "U+05A5 HEBREW ACCENT MERKHA (yored in this context)",
                            "REVIA_U0597_present_in_either_form": "\N{HEBREW ACCENT REVIA}"
                            in main + source_form,
                        },
                    }
                )
                if ref == "Job 29:25":
                    row["limit"] = (
                        "The Introduction footnote discusses possible erasure above resh; the source attribution is not an independent scan verdict."
                    )
            else:
                assert not item["candidate_note_ids"] and ref == "Psalms 42:3"
                evidence = item["edition_evidence"]
                candidates = [
                    (i, token)
                    for i, part in enumerate(evidence["complete_EP"])
                    if isinstance(part, str)
                    for token in part.split()
                    if has_both(token)
                ]
                assert len(candidates) == 1
                index, main = candidates[0]
                row.update(
                    {
                        "mam_body": {
                            "source": "verse-parts",
                            "path": evidence["path"],
                            "parts": [
                                {
                                    "pointer": evidence["json_pointer"] + f"/{index}",
                                    "text": main,
                                }
                            ],
                            "text": main,
                        },
                        "status": "MAM-body-feature-only-no-doc-note",
                        "limit": "Aleppo attribution is supplied by the Introduction alone; the parsed verse has no documentation note.",
                    }
                )
            assert has_both(row["mam_body"]["text"]), ref
            row["mam_body_has_oleh_and_yored_on_same_letter"] = True
            records.append(row)
    assert len(records) == len(NOTE_IDS) and {r["ref"] for r in records} == set(
        NOTE_IDS
    )
    candidate_ids = {n for r in records for n in r["candidate_note_ids"]}
    selected_ids = {n for n in NOTE_IDS.values() if n}
    assert candidate_ids == selected_ids | set(OTHER_NOTES)
    return {
        "case": "oleh-omission-count",
        "source_base_commit": audit.pinned_commit(),
        "method": "Start with the parsed ordered chapter 5 list. Select pertinent notes by manual semantic review; reuse the current source-form grammar, sigil-expression parsing and literal note/body pointers. Compare marks only on MAM-order keys; retain all quotations verbatim.",
        "counts": {
            "listed_distinct_verses": len(records),
            "MAM_body_forms_with_both_marks_on_same_letter": sum(
                r["mam_body_has_oleh_and_yored_on_same_letter"] for r in records
            ),
            "candidate_notes_at_listed_verses": len(candidate_ids),
            "pertinent_notes": len(selected_ids),
            "notes_explicitly_naming_omitted_oleh": sum(
                r["status"] == "note-explicitly-names-omitted-oleh" for r in records
            ),
            "pointing_pairs_with_revia_label": sum(
                r["status"] == "pointing-pair-supported-but-note-calls-omission-revia"
                for r in records
            ),
            "verses_without_doc_note": sum(r["relevant_note"] is None for r in records),
            "unrelated_candidate_notes": len(OTHER_NOTES),
        },
        "statuses": dict(Counter(r["status"] for r in records)),
        "limits": [
            "Thirteen listed verses do not imply thirteen supporting doc-notes.",
            "Psalm 30:12's revia label remains the separate open case PS-30-12-NOTE-LABEL.",
            "No manuscript scans or manuscript-wide completeness claim are part of this check.",
            "Historical revision evidence is supplemental; the pinned source caches are unchanged.",
        ],
        "cases": records,
    }


def main():
    result = build()
    audit.dump("oleh-count-evidence.json", result)
    print(result["counts"])
