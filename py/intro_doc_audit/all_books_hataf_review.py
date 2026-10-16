"""Account for the finite all-book evidence using explicit contextual decisions."""

from collections import Counter, defaultdict

from intro_doc_audit import audit, next_pass, review


def main():
    census = review.read("all-books-hataf-census.json")
    assessments = review.read("all-books-hataf-assessments.json")
    notes = {n["id"]: n for n in review.read("notes.json")}
    prior = review.read("hataf-rosters.json")["rosters"]
    claims = {c["id"]: c for c in review.read("claims.json")}
    if (
        not census["source_base_commit"]
        == assessments["source_base_commit"]
        == audit.pinned_commit()
    ):
        raise ValueError("Assessment snapshot differs")
    decisions = {r["note_id"]: r for r in assessments["unlisted_note_dispositions"]}
    candidate_notes = {r["note_id"] for r in census["unlisted_note_word_candidates"]}
    if set(decisions) != candidate_notes:
        raise ValueError("Every unlisted note needs one contextual disposition")
    raw_proofs = {id: next_pass.raw_note_proof(notes[id]) for id in decisions}
    note_rows = []
    for word in census["note_word_candidates"]:
        if word["roster_matches"]:
            decision = {
                "status": "already-listed-position",
                "explanation": "This word joins an existing list position. The complete source clauses and prior semantic item assessments remain available; lexical membership alone does not establish a named-source claim.",
            }
        else:
            decision = decisions[word["note_id"]]
        note_rows.append({**word, "assessment": decision})
    functions = {g["unpointed_key"]: g for g in assessments["body_form_dispositions"]}
    if set(functions) != {w["unpointed_key"] for w in census["body_candidates"]}:
        raise ValueError("Every body form needs one contextual function assessment")
    body_rows = [
        {**w, "assessment": functions[w["unpointed_key"]]}
        for w in census["body_candidates"]
    ]
    parameter_rows = []
    for parameter in census["ketiv_qere_parameters"]:
        for word in parameter["words"]:
            parameter_rows.append(
                {
                    **parameter,
                    "word": word,
                    "assessment": functions[word["unpointed_key"]],
                }
            )
    groups = list(dict.fromkeys(b["roster_group_hebrew"] for b in census["books"]))
    if len(groups) != 24 or len(prior) != 24:
        raise ValueError("Introduction list groups differ from the book inventory")
    books = []
    for group, source in zip(groups, prior):
        members = [b for b in census["books"] if b["roster_group_hebrew"] == group]
        ids = {b["book"] for b in members}
        if any(item["reviewed_ref"][0] not in ids for item in source["items"]):
            raise ValueError("A list item points outside its verified book group")
        for b in members:
            prefix = b["book"] + " "
            books.append(
                {
                    **b,
                    "list_claim": source["claim"],
                    "body_candidates": sum(
                        w["ref"].startswith(prefix) for w in body_rows
                    ),
                    "note_word_candidates": sum(
                        w["ref"].startswith(prefix) for w in note_rows
                    ),
                    "unlisted_note_dispositions": [
                        d for d in decisions.values() if d["note_id"].startswith(prefix)
                    ],
                }
            )
    list_counts = []
    for source in prior:
        # The two alternative specimens at Ps39:13 and Song2:7 are each one item.
        word_count = len(source["items"]) + (source["claim"] == "ch3:L1134")
        list_counts.append(
            {
                "claim": source["claim"],
                "source_url": source["source_url"],
                "declared_items": source["declared_items"],
                "word_items": word_count,
                "verse_positions": len(
                    {tuple(i["reviewed_ref"]) for i in source["items"]}
                ),
                "source_items": len(source["items"]),
            }
        )
    uncertainties = [
        d
        for d in decisions.values()
        if d["status"].startswith("uncertain")
        or d["status"] == "ketiv-qere-attribution-gap"
    ]
    uncertainties += [
        g for g in functions.values() if g["status"].startswith("uncertain")
    ]
    exceptions = [
        i
        for source in prior
        for i in source["items"]
        if i["status"] != "central-source-and-hataf-correspondence"
    ]
    partition = Counter(w["assessment"]["status"] for w in body_rows)
    note_partition = Counter(w["assessment"]["status"] for w in note_rows)
    findings = review.read("all-books-hataf-findings.json")
    if {f["note"] for f in findings["verified_omissions"]} != {
        d["note_id"] for d in decisions.values() if d["status"] == "definite-omission"
    }:
        raise ValueError("Verified findings differ from contextual decisions")
    # Source objects are kept distinct: a pointed ketiv note does not supply qere.
    framing = {
        "item": "ch5:L710/item/17",
        "claim": "ch5:L710",
        "status": "explicit-source-framing-exception",
        "specimen": next(
            i["literal_specimen"]
            for s in prior
            for i in s["items"]
            if i["id"] == "ch5:L710/item/17"
        ),
        "note": "Psalms 17:14/2/0",
        "explanation": "The list expressly names Sassoon1053 (ש1), while its heading names Aleppo or Leningrad. The note quotes those other manuscripts and reconstructed Aleppo practice; Leningrad explicitly has no ḥataf. This is a concrete framing exception, not a new manuscript reading.",
        "raw_proof": next_pass.raw_note_proof(notes["Psalms 17:14/2/0"]),
    }
    result = {
        "source_base_commit": audit.pinned_commit(),
        "state": "All books and finite candidates accounted for; explicit source/function uncertainties retained",
        "coverage": {
            "books": {"accounted": len(books), "total": 39},
            "verses": {"accounted": census["canonical_verses"], "total": 23202},
            "canonical_doc_notes": {
                "scanned": census["doc_notes_scanned"],
                "total": 3905,
            },
            "metadata_note_copies": sum(
                m["note_copies"] for m in census["metadata_repetitions"]
            ),
            "list_groups": {"accounted": len(prior), "total": 24},
            "list_source_items": {
                "accounted": sum(len(s["items"]) for s in prior),
                "total": 667,
            },
            "list_word_items": sum(c["word_items"] for c in list_counts),
            "note_word_candidates": {
                "accounted": len(note_rows),
                "total": len(census["note_word_candidates"]),
            },
            "unlisted_note_words": {
                "accounted": len(census["unlisted_note_word_candidates"]),
                "total": len(census["unlisted_note_word_candidates"]),
            },
            "unlisted_note_bodies": {
                "reviewed": len(decisions),
                "total": len(candidate_notes),
            },
            "body_word_candidates": {
                "accounted": len(body_rows),
                "total": len(census["body_candidates"]),
            },
            "body_form_groups": {"reviewed": len(functions), "total": 63},
            "ketiv_qere_parameters": {
                "scanned": len(census["ketiv_qere_parameters"]),
                "total": len(census["ketiv_qere_parameters"]),
            },
            "ketiv_qere_vowel_hits": len(parameter_rows),
        },
        "books": books,
        "list_counts": list_counts,
        "body_partition": dict(partition),
        "note_partition": dict(note_partition),
        "note_word_reviews": note_rows,
        "body_word_reviews": body_rows,
        "ketiv_qere_vowel_reviews": parameter_rows,
        "raw_unlisted_note_proofs": raw_proofs,
        "verified_omissions": findings["verified_omissions"],
        "phonetic_questions": findings.get("phonetic_questions", []),
        "uncertainty_queue": uncertainties,
        "source_framing_exception": framing,
        "prior_semantic_list_exceptions": exceptions,
        "scope_claims": [
            {
                "id": id,
                "text": claims[id]["text"],
                "source_url": claims[id]["source_url"],
            }
            for id in assessments["scope_claims"]
        ],
        "independent_checker": assessments["independent_checker"],
        "limits": [
            "Five concrete list omissions are established between explicit cached source claims; physical manuscript readings were not reassessed.",
            "Contextual morphology and divine-name/function classifications are identified as inferences and supported by concrete controls. Source certainty, chronology and pointed-ketiv/qere boundaries are retained.",
            "The semantic candidate ledger accounts for the finite evidence; an unrecorded manuscript occurrence is not evidence that can be recovered from the cache.",
        ],
    }
    audit.dump("all-books-hataf-review.json", result)
    findings.update(
        status=result["state"],
        coverage=result["coverage"],
        uncertainty_queue=uncertainties,
        source_framing_exception=framing,
    )
    audit.dump("all-books-hataf-findings.json", findings)
    print(
        {
            "coverage": result["coverage"],
            "body_partition": dict(partition),
            "note_partition": dict(note_partition),
            "uncertainty_cases": len(uncertainties),
        }
    )
