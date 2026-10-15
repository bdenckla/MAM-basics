"""Scope the existing reader cases for supplemental revision-history research."""

from collections import Counter

from intro_doc_audit import audit, human_review

INTERNAL = {
    "different-qere-count": "The requested comparison is between two Introduction category definitions; the MAM qere is corroborating context.",
    "deuteronomy-hataf-count": "The count conflicts with the Introduction's own list items.",
    "lamentations-one-two": "Ben identifies a contradiction within the Introduction.",
    "oleh-omission-count": "Two Introduction enumerations disagree with each other.",
    "isaiah-decision-types": "The Introduction's category enumeration contradicts its own summary.",
    "appendix-date-pair": "The two dates disagree within the appendix.",
    "job-chapter-verse": "The Introduction's reference label reverses its own link destination.",
    "westminster-version-label": "The version label disagrees with its quoted heading, without a MAM body/doc-note comparison.",
    "seder-year-type": "The Introduction's reading-schedule wording disagrees with the Koren passage it quotes.",
    "PS-39-13-HATAF-LABEL": "The Introduction's vowel name contradicts its own quoted vowel.",
    "DESCRIPTION-EXOD-7-20": "The Introduction's accent name contradicts its own specimen; the doc-note agrees with the specimen.",
    "DESCRIPTION-NUM-16-27": "The Introduction's letter name contradicts its own specimen; the doc-note agrees with the specimen.",
    "DEUT-22-6-SIZE": "The Introduction's category marker contradicts its own specimen.",
    "ZARQA-TSINNOR-NAMES": "Two Introduction footnotes reverse their names.",
    "SUMMARY-VISIBILITY": "The Summary conflicts with another Introduction explanation of visibility.",
    "ALL-HATAF-LIST-COUNTS": "The declared headings disagree with the Introduction's own word-item counts.",
}

SUPPLEMENTAL_NOTE_CASES = {
    "EX-7-13-METEG-QUOTATION",
    "LEV-3-17-METEG-LABEL",
    "NUM-10-8-B17-METEG",
    "DEUT-1-33-SASSOON-METEG",
    "PS-53-6-LETTER-NAME",
    "DESCRIPTION-DEUT-28-27",
    "LEV-7-PARASHAH-LOCATOR",
    "SONG-2-17-ACCENT-NAME",
}

LIST_CLAIMS = {
    "ALL-HATAF-SAM-24-16": "ch5:L698",
    "ALL-HATAF-SAM-24-18": "ch5:L698",
    "ALL-HATAF-JER-48-32": "ch5:L704",
    "ALL-HATAF-DAN-12-2": "ch5:L726",
    "ALL-HATAF-NEH-6-19": "ch5:L728",
    "ALL-HATAF-SAM-6-5": "ch5:L698",
}

FIRST_BATCH = [
    "numbers-yod-label",
    "deuteronomy-vav-label",
    "PS-1-3",
    "PS-18-2-ATTRIBUTION",
]

REQUESTED_INTERNAL = {
    "oleh-omission-count": "Ben explicitly requested the count's chronology as an exception to the exclusion of internal Introduction contradictions, together with the thirteen MAM body/doc-note comparisons.",
}


def dictionaries(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from dictionaries(child)
    elif isinstance(value, list):
        for child in value:
            yield from dictionaries(child)


def main():
    cases = human_review.read("human-review.json")
    notes = {n["id"]: n for n in human_review.read("notes.json")}
    claims = {c["id"]: c for c in human_review.read("claims.json")}
    reviewed = human_review.reviewed_case_ids(cases)
    history_results = {
        r["case"]: r
        for r in human_review.read("revision-history-results.json")["cases"]
    }
    records = []
    for case in cases:
        cid = case["id"]
        note_ids, claim_ids, body_sources = set(), set(), []
        for part in dictionaries(case):
            claim = part.get("claim")
            if part.get("source") == "claim":
                claim = part.get("id")
            if claim in claims:
                claim_ids.add(claim)
            note = part.get("note")
            if part.get("source") in {"note", "note-target"}:
                note = part.get("id")
            if note in notes:
                note_ids.add(note)
            if part.get("source") in {"note-target", "verse-parts", "verse"}:
                body_sources.append(
                    {
                        k: part[k]
                        for k in ("source", "id", "path", "pointer", "parts")
                        if k in part
                    }
                )
        if cid in LIST_CLAIMS:
            claim_ids.add(LIST_CLAIMS[cid])
        reason = INTERNAL.get(cid)
        if cid.startswith("NAV-"):
            reason = "Introduction navigation/reference defect, without a contradictory MAM reading or doc-note claim. Follow only if a content-history case needs this locator as context."
        if cid.startswith("SPELLING-COVERAGE-"):
            reason = "An internal Introduction referral points to an absent Introduction decision-list entry. MAM's note corroborates the spelling rather than contradicting it."
        if case["section"] == "scope":
            reason = "Resolved vowel-function control rather than a discrepant Introduction/MAM claim."
        if cid in REQUESTED_INTERNAL:
            reason = None
        scope = "excluded-internal-or-control" if reason else "applicable"
        if not reason:
            reason = (
                "Supplemental MAM note/body defect from the same audit; its source history may explain the mismatch."
                if cid in SUPPLEMENTAL_NOTE_CASES
                else "The Introduction's claim, example, attribution, list membership or coverage can be compared with dated MAM body/doc-note evidence."
            )
        result = history_results.get(cid)
        records.append(
            {
                "case": cid,
                "title": case["title"],
                "scope": scope,
                "scope_reason": reason,
                **(
                    {"explicit_scope_exception": REQUESTED_INTERNAL[cid]}
                    if cid in REQUESTED_INTERNAL
                    else {}
                ),
                "comparison_kind": (
                    "supplemental-MAM-note-body"
                    if cid in SUPPLEMENTAL_NOTE_CASES
                    else "Introduction-MAM"
                ),
                "ben_reviewed": cid in reviewed,
                "adjudication": case.get("adjudication"),
                "introduction_claims": sorted(claim_ids),
                "introduction_pages": sorted({claims[c]["path"] for c in claim_ids}),
                "doc_notes": sorted(note_ids),
                "chapter_pages": sorted(
                    {notes[n]["chapter_revision"]["resolved_title"] for n in note_ids}
                ),
                "body_source_pointers": body_sources,
                "history_status": (
                    "excluded"
                    if scope != "applicable"
                    else result["classification"] if result else "pending"
                ),
                "history_result": result["result"] if result else None,
                "first_batch": cid in FIRST_BATCH,
            }
        )
    counts = Counter(r["scope"] for r in records)
    assert len(records) == len(cases) == len({r["case"] for r in records})
    result = {
        "source_base_commit": audit.pinned_commit(),
        "authorization": "Sentinel_7a1e08b9a994819188a8e42b91fb1795",
        "scope": "Existing report comparisons with MAM body text (including alternatives) or doc-notes, plus Ben's explicit omitted-oleh count-history request. Other pure Introduction contradictions, locator defects and resolved controls are accounted for but outside this content-history pass.",
        "coverage": {
            "report_cases_accounted": len(records),
            "report_cases_total": len(cases),
            **dict(counts),
        },
        "history_partition": dict(Counter(r["history_status"] for r in records)),
        "first_batch": FIRST_BATCH,
        "cases": records,
        "limits": [
            "Pending means no chronology verdict, not evidence of staleness.",
            "A changed chapter alone cannot date the addition or alteration of a particular word or doc-note claim.",
            "Existing Ben approvals and current report statuses are copied as context and are not altered by inventory routing.",
            "Global poetic count questions require historical corpus/count-definition evidence rather than a single chapter's revision history.",
        ],
    }
    audit.dump("revision-history-inventory.json", result)
    print(result["coverage"])
    print(result["history_partition"])
