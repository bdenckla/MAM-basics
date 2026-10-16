"""Account for human-read prose separately from routing-only external table cells."""

import json
import re
import subprocess
from collections import Counter

from intro_doc_audit import audit, review


def previous_json(commit, name):
    data = subprocess.check_output(
        [
            "git",
            "-c",
            "safe.directory=" + audit.ROOT.as_posix(),
            "show",
            f"{commit}:doc/intro-doc-audit/{name}",
        ],
        cwd=audit.ROOT,
    )
    return json.loads(data.decode("utf-8"))


def selected_population(claims, commit):
    seen = {r["claim"] for r in previous_json(commit, "claim-dispositions.json")}
    selection = previous_json(commit, "review-selections.json")
    seen.update(
        cid
        for group in selection.values()
        if isinstance(group, list)
        for case in group
        for cid in case.get("claims", [])
    )
    seen.update(
        c["id"]
        for c in claims
        if c["id"].startswith("ch3:") and 1121 <= c["line"] <= 1430
    )
    return [
        c
        for c in claims
        if not c["refs"]
        and c["id"] not in seen
        and not c["text"].startswith(("#", "*", ":", "|", "!", "=", "{", "<", "[", ";"))
        and re.search("[א-ת]", c["text"])
    ]


def main():
    source = review.read("general-prose-input.json")
    claims = review.read("claims.json")
    by_claim = {c["id"]: c for c in claims}
    by_note = {n["id"]: n for n in review.read("notes.json")}
    eligible = selected_population(claims, source["previous_audit_commit"])
    numeric = {
        c["id"]
        for c in eligible
        if c["id"].split(":")[0] in {"summary", "ch2", "ch3", "ch4", "ch5"}
        and re.search(r"\d|תמיד|לעולם|בלבד|כל המקרא|כל המקומות|עקבי|חובה", c["text"])
    }
    remaining = {
        c["id"]
        for c in eligible
        if c["id"] not in numeric and not c["id"].startswith("westminster-typing:")
    }
    historical_framing = {
        "westminster-typing:L3",
        "westminster-typing:L62",
        "westminster-typing:L98",
        "westminster-typing:L1146",
    }
    table = [
        c
        for c in eligible
        if c["id"].startswith("westminster-typing:")
        and c["id"] not in historical_framing
    ]
    populations = {
        "general-numeric-universal-prose": numeric,
        "remaining-general-prose": remaining,
        "historical-WLC-source-framing": historical_framing,
    }
    records = []
    batches = []
    for batch in source["batches"]:
        assessed = [cid for ids in batch["dispositions"].values() for cid in ids]
        expected = populations[batch["id"]]
        if (
            len(assessed) != len(set(assessed))
            or set(assessed) != expected
            or len(assessed) != batch["total"]
        ):
            raise ValueError(
                f"Human prose ledger does not account for its declared population: {batch['id']}"
            )
        batches.append({**batch, "page": "mixed", "selection": {"claim_ids": assessed}})
        for status, ids in batch["dispositions"].items():
            records.extend(
                {
                    "claim": cid,
                    "status": status,
                    "batch": batch["id"],
                    "source": {
                        k: by_claim[cid][k]
                        for k in ("text", "path", "line", "source_url", "topic")
                    },
                    "limit": "Group disposition is a human-read evidence boundary; narrower operational subclaims receive separate evidence. No universal verdict.",
                }
                for cid in ids
            )
    subclaims = []
    for row in source.get("subclaims", []):
        for path in row["evidence_paths"]:
            if not (audit.ROOT / path).is_file():
                raise ValueError(f"General subclaim evidence path missing: {path}")
        subclaims.append(
            {
                **row,
                "introduction_sources": [
                    {
                        k: by_claim[cid][k]
                        for k in ("id", "text", "path", "line", "source_url", "topic")
                    }
                    for cid in row["claims"]
                ],
                "note_sources": [
                    {
                        k: by_note[nid][k]
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
                    for nid in row["note_ids"]
                ],
                "code_or_structure_source_urls": [
                    audit.source_url(p) for p in row["evidence_paths"]
                ],
            }
        )
    result = {
        "author": source["author"],
        "date": source["date"],
        "source_base_commit": audit.pinned_commit(),
        "previous_audit_commit": source["previous_audit_commit"],
        "routing_selector": "Ordinary non-reference Hebrew units absent from the prior assessed ledger, review case claims and separately read/routed chapter-3 final range. Prefix exclusions avoid headings/list/table/wikitext rubrics. Numeric/universal matching only prioritizes a subset; all remaining ordinary units are separately declared. It supplies no semantic verdict.",
        "declared_numeric_universal_units": len(numeric),
        "declared_remaining_ordinary_units": len(remaining),
        "human_read_units": len(records),
        "historical_WLC_framing_units": len(historical_framing),
        "human_read_units_total": len(numeric)
        + len(remaining)
        + len(historical_framing),
        "status_counts": dict(Counter(r["status"] for r in records)),
        "records": records,
        "batches": batches,
        "routing_only_external_table_cells": {
            "count": len(table),
            "read_as_individual_semantic_claims": False,
            "claims": [c["id"] for c in table],
            "source_url": audit.source_url(
                "in/mam-ws-intro/westminster-typing.mediawiki"
            ),
            "originally_routed_page_units": len(table) + len(historical_framing),
            "separately_read_framing_units": sorted(historical_framing),
            "boundary": "These 843 remaining Hebrew units belong to quoted historical Westminster typing tables. The page explicitly names historical source versions, but their matching machine-readable inputs and physical source controls are unavailable here. Current WLC4.22 and MAM notes cannot certify those historical tables. Four source-framing units receive separate bounded checks; the table units are routed, not added to the human semantic assessment denominator.",
        },
        "subclaims": subclaims,
    }
    audit.dump("general-prose-assessments.json", result)
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "declared_numeric_universal_units",
                    "declared_remaining_ordinary_units",
                    "human_read_units",
                    "human_read_units_total",
                    "status_counts",
                )
            },
            indent=2,
        )
    )
