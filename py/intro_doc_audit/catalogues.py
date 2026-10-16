"""Compare declared catalogue memberships, without changing Masorah definitions."""

from intro_doc_audit import audit, review

CATALOGUES = {
    "ch2:L86": ("כתיב ולא קרי",),
    "ch2:L87": ("קרי ולא כתיב",),
    "ch2:L96": ("k1q2-sr-kqq",),
    "ch2:L97": ("k1q2-sr-qqk",),
    "ch2:L98": ("k1q2-sr-bcom",),
    "ch2:L105": ("k2q1",),
    "ch2:L112": ("k1q2-wr-kqq",),
    "ch2:L113": ("k1q2-ur-qqk",),
    "appendices:L374": ("כתיב ולא קרי",),
    "appendices:L375": ("קרי ולא כתיב",),
    "appendices:L377": ("k1q2-sr-kqq",),
    "appendices:L378": ("k1q2-sr-qqk",),
    "appendices:L379": ("k1q2-sr-bcom",),
    "appendices:L380": ("k2q1",),
    "appendices:L381": ("k1q2-wr-kqq",),
    "appendices:L382": ("k1q2-ur-qqk",),
    "appendices:L383": ("k2q2",),
    "appendices:L384": ("k3q3",),
    "appendices:L385": ("k1q1-mcom",),
}


def main():
    claims = {c["id"]: c for c in review.read("claims.json")}
    corpus = review.read("structural-populations.json")
    rows = []
    for cid, categories in CATALOGUES.items():
        declared = {audit.ref_id(ref) for ref in claims[cid]["refs"]}
        actual = {r["ref"] for r in corpus["records"] if r["category"] in categories}
        # The catalogue's Jeremiah locator is independently wrong; keep it
        # separate from the remaining membership difference.
        adjusted = (declared - {"Jeremiah 31:38"}) | (
            {"Jeremiah 31:37"} if "Jeremiah 31:38" in declared else set()
        )
        rows.append(
            {
                "claim": cid,
                "source_url": claims[cid]["source_url"],
                "categories": categories,
                "declared_refs": sorted(declared),
                "current_template_refs": sorted(actual),
                "literal_locator_adjustment": (
                    {"Jeremiah 31:38": "Jeremiah 31:37"} if declared != adjusted else {}
                ),
                "listed_only_after_locator_check": sorted(adjusted - actual),
                "current_type_only": sorted(actual - adjusted),
                "membership_agrees_after_locator_check": adjusted == actual,
            }
        )
    result = {
        "catalogue_lines": len(rows),
        "matching_membership_lines": sum(
            r["membership_agrees_after_locator_check"] for r in rows
        ),
        "projection": corpus["projection"],
        "rows": rows,
        "semantic_disposition": "The catalogue and current MAM template identities differ at four source units. Traditional Masorah phenomena across manuscripts are not identical to current MAM selected-template populations. No universal manuscript count is asserted.",
        "decisive_notes": [
            "2Samuel 8:3/2/0",
            "2Samuel 21:12/2/0",
            "Jeremiah 31:37/2/0",
        ],
    }
    audit.dump("catalogue-comparison.json", result)
    print(
        f"Compared {len(rows)} catalogue lines; {result['matching_membership_lines']} memberships agree, {len(rows)-result['matching_membership_lines']} differ"
    )
