"""Compact incremental evidence; existing finding totals remain separate."""

import html

from intro_doc_audit import audit, review


def render(by_claim, by_note):
    assessments = review.read("next-pass-assessments.json")
    census = review.read("next-pass-census.json")
    general = review.read("general-prose-assessments.json")
    prose = review.read("next-pass-prose-findings.json")
    rows = {r["id"]: r for r in assessments["assessments"]}
    unsigned = assessments["nine_unsigled_hataf_counterparts"]
    hataf_items = next(r for r in rows.values() if r["id"] == "HATAF-SOURCE-SCOPE")[
        "roster_items"
    ]
    poetic_support = [
        {"claim": cid, "text": by_claim[cid]["text"]}
        for cid in ("ch5:L569", "ch5:L656", "ch2:L334")
    ]
    poetic_support.append(
        {
            "claim": "ch5:L710",
            "text": review.roster_items()["ch5:L710"][66]["literal_specimen"],
        }
    )
    year = by_claim["ch5:L799"]["text"]
    narrative = year.split("{{הערה|", 1)[0]
    quotation = (
        year.split('"סיכומם', 1)[-1]
        if '"סיכומם' in year
        else year[year.index("סיכומם") :]
    )
    quotation = quotation.split('" לדיון', 1)[0]
    if quotation not in year:
        raise ValueError("Year arithmetic quotation must remain a source fragment")
    cases = [
        {
            "id": "NEXT-CATALOGUE",
            "title": "Different-qere total: chapter 2 has three; appendix has four",
            "status": "supported-internal-count-difference",
            "claims": ["ch2:L109", "ch2:L112", "appendices:L381", "appendices:L382"],
            "refs": [["2Samuel", 8, 3]],
            "note_ids": ["2Samuel 8:3/2/0"],
            "explanation": "The appendix includes 2 Samuel 8:3 alongside Ezekiel 9:11 in its two non-maqaf cases; chapter 2 lists only Ezekiel and totals three. The current typed target and note support the added one-ketiv/two-different-qere case. The traditional qere-only final atom can coexist with that unified classification. This resolves an internal list/count difference, not the truth of every traditional masorah catalogue.",
        },
        {
            "id": "NEXT-DEUT-SHEVA",
            "title": "Deuteronomy 32:6: the incidental yod SHEVA difference is literal",
            "status": "quotation-scope-clarified",
            "claims": ["ch3:L246"],
            "refs": [["Deuter", 32, 6]],
            "note_ids": ["Deuter 32:6/2/0"],
            "note_excerpts": {
                "Deuter 32:6/2/0": [
                    "ל="
                    + by_note["Deuter 32:6/2/0"]["body_text"]
                    .split("\nל=", 1)[1]
                    .split("\n", 1)[0]
                ]
            },
            "intro_literal_excerpts": [
                {
                    "claim": "ch3:L246",
                    "text": by_claim["ch3:L246"]["text"]
                    .split(" / ל=", 1)[1]
                    .split(" / ספרי", 1)[0],
                }
            ],
            "explanation": rows["TORAH-SPELLING-SCOPE"]["result"],
        },
        {
            "id": "NEXT-POETIC-QUOTES",
            "title": "Four design specimens differ from other Introduction passages",
            "status": "internal-quotation-and-qualification-differences",
            "claims": ["ch5:L751", "ch5:L753", "ch5:L787"],
            "intro_roster_items": [
                ["ch5:L751", 4],
                ["ch5:L753", 5],
                ["ch5:L787", 56],
                ["ch5:L787", 64],
            ],
            "refs": [
                ["Psalms", 6, 3],
                ["Proverbs", 8, 34],
                ["Psalms", 68, 18],
                ["Psalms", 74, 5],
            ],
            "note_ids": [
                "Psalms 6:3/2/0",
                "Proverbs 8:34/2/0",
                "Psalms 68:18/2/0",
                "Psalms 74:5/2/0",
            ],
            "paired_supporting_intro_excerpts": poetic_support,
            "right_label": "Doc-note and other Introduction passage",
            "explanation": rows["POETIC-SPECIMEN-SCOPE"]["result"],
        },
        {
            "id": "NEXT-NINE-HATAF",
            "title": "Nine unsigled hataf entries have explicit Aleppo counterparts",
            "status": "narrow-source-subclaim-resolved",
            "claims": ["ch5:L706", "ch5:L710"],
            "intro_roster_items": hataf_items,
            "refs": [
                review.roster_items()[cid][index - 1]["reviewed_ref"]
                for cid, index in hataf_items
            ],
            "note_ids": [r["note_id"] for r in unsigned],
            "explanation": rows["HATAF-SOURCE-SCOPE"]["result"],
        },
        {
            "id": "NEXT-IMPLICIT-MS",
            "title": "2 Kings 14:7 explicitly names Aleppo for the missing pashta",
            "status": "narrow-attribution-subclaim-resolved",
            "claims": ["ch5:L412", "ch5:L428"],
            "refs": [["2Kings", 14, 7]],
            "note_ids": ["2Kings 14:7/2/0"],
            "explanation": rows["IMPLICIT-MS"]["result"],
        },
        {
            "id": "NEXT-YEAR-SCOPE",
            "title": "Seder explanation: Hebrew-year narrative and solar-year arithmetic",
            "status": "supported-internal-wording-tension",
            "claims": ["ch5:L799"],
            "refs": [],
            "note_ids": [],
            "intro_literal_excerpts": [{"claim": "ch5:L799", "text": narrative}],
            "right_literal_excerpts": [{"claim": "ch5:L799", "text": quotation}],
            "right_label": "Quotation in the same Introduction paragraph",
            "explanation": "The narrative says an ordinary Hebrew year; the quotation explicitly calculates a 365-day solar year. Its arithmetic, 293 + 71 = 364 plus the excluded day, is internally consistent. The cache establishes the wording tension, not the historical purpose or calendar used by the seder division.",
        },
    ]
    job = by_claim["ch1:L258"]["text"]
    job_excerpt = job[job.index("לדוגמה: באיוב") : job.index("בהקלדת וסטמינטר זה מובן")]
    date_excerpt = by_claim["appendices:L476"]["text"].split(" עוד שלב אחרון", 1)[1]
    cases.extend(
        [
            {
                "id": "NEXT-ISAIAH-GROUPING",
                "title": "Isaiah's four decisions belong to the first two types",
                "status": "supported-internal-grouping-mismatch",
                "claims": ["ch5:L55"],
                "refs": [],
                "note_ids": [],
                "right_label": "Surrounding Introduction enumeration",
                "right_literal_excerpts": [
                    {"claim": cid, "text": by_claim[cid]["text"]}
                    for cid in ("ch5:L47", "ch5:L48", "ch5:L49")
                ],
                "explanation": "The five-type list assigns one case to type 1, three to type 2 and two to type 3. The first two total four; the first three total six. The following four decisions belong to the first two, while the preceding paragraph handles the last three types. This is an internal grouping-wording defect; the manuscript judgments are not reconsidered.",
            },
            {
                "id": "NEXT-DATE-PAIR",
                "title": "An appendix Hebrew/Gregorian date pair denotes different years",
                "status": "supported-incompatible-date-pair",
                "claims": ["appendices:L476"],
                "intro_literal_excerpts": [
                    {"claim": "appendices:L476", "text": date_excerpt}
                ],
                "refs": [],
                "note_ids": [],
                "right_label": "Cached date pair",
                "right_literal_excerpts": [
                    {
                        "claim": "appendices:L476",
                        "text": prose["historical_date_pair"]["literal_date_pair"],
                    }
                ],
                "explanation": "The local Hebrew-calendar conversion gives 2013-12-10 for 7 Tevet 5774; 2014-12-10 corresponds to 18 Kislev 5775. Both conversions round-trip. The pair is incompatible. The actual historical event date is not established, so no corrected event date is chosen.",
            },
            {
                "id": "NEXT-JOB-REFERENCE",
                "title": "Job's prose reference reverses chapter and verse",
                "status": "supported-prose-reference-error",
                "claims": ["ch1:L258"],
                "intro_literal_excerpts": [{"claim": "ch1:L258", "text": job_excerpt}],
                "refs": [["Job", 9, 10], ["Job", 10, 9]],
                "note_ids": [],
                "right_label": "Exact cached verse contexts",
                "cached_contexts_as_comparison": True,
                "supplemental_sources": [
                    source
                    for c in prose["Job_prose_reference"]["contexts"]
                    for source in [
                        {
                            "url": audit.source_url(c["path"]),
                            "label": c["ref"] + " raw cache",
                        },
                        {
                            "url": f'https://he.wikisource.org/w/index.php?oldid={c["chapter_revision"]["revision_id"]}',
                            "label": c["ref"]
                            + " chapter revision "
                            + str(c["chapter_revision"]["revision_id"]),
                        },
                    ]
                ],
                "explanation": "The named prose reference reverses chapter and verse. The quoted word and both external source paths identify Job 9:10; current raw and parsed 9:10 contain that word, while 10:9 does not. No external link was fetched. The footnote's historical transcription and manuscript claims remain unverified.",
            },
        ]
    )
    cases.append(
        {
            "id": "NEXT-WLC-VERSION",
            "title": "A Westminster source label says 4.14; its quotation says 4.16",
            "status": "supported-internal-version-label-mismatch",
            "claims": ["westminster-typing:L62"],
            "refs": [],
            "note_ids": [],
            "right_label": "Heading in the quoted source table",
            "right_is_latin": True,
            "right_literal_excerpts": [
                {
                    "claim": "westminster-typing:L66",
                    "text": by_claim["westminster-typing:L66"]["text"],
                }
            ],
            "explanation": "The historical versions are explicitly named. The Hebrew source label disagrees with its own quotation's version heading. Both quoted note-legend totals are arithmetically consistent: 1034 and 945. The historical 4.12/4.14 category counts do not define unique-change membership or verify manuscript interpretations. Current cached 4.22 is a different source/version; the remaining historical table units are routed with that evidence boundary.",
        }
    )
    audit.dump("next-pass-review-cases.json", cases)
    cards = []
    contexts = []
    for case in cases:
        markup, context = review.card(case, by_claim, by_note)
        cards.append(
            f'<details class="finding"><summary>{html.escape(case["title"])}</summary>{markup}</details>'
        )
        contexts.extend(context)
    counts = {
        "uncertainty_groups_revisited": 24,
        "uncertainty_groups_total": 24,
        "two_atom_roster_memberships": 55,
        "two_atom_current_population": 55,
        "unsigled_hataf_counterparts": 9,
        "current_hataf_central_correspondence": assessments[
            "hataf_incremental_overlay"
        ]["current_central_correspondence"],
        "hataf_total_items": 667,
        "independent_raw_note_comparisons": 21,
        "general_prose_units_read": general["human_read_units"],
        "general_prose_units_total": general["human_read_units_total"],
        "external_Westminster_cells_routed_not_semantically_assessed": general[
            "routing_only_external_table_cells"
        ]["count"],
        "incremental_evidence_cards": len(cases),
        "new_internal_wording_count_date_metadata_groups": 5,
        "new_prose_verse_locator_examples": 1,
        "new_cached_fragment_target_cases": len(prose["fragment_cases"]),
        "new_central_attributed_form_groups": 0,
    }
    table = "<table><thead><tr><th>Population</th><th>Introduction</th><th>Current cache</th><th>Boundary</th></tr></thead><tbody>"
    for label, intro, current, limit in [
        ("Poetic verses", "4465", "4465", "Genre determined per verse"),
        (
            "DEHI verses",
            "2685",
            "2679",
            "Independently reproduced membership; historical source undefined",
        ),
        ("OLEH verses", "421", "423", "368 same-atom + 55 two-atom; zero unmatched"),
        (
            "Two-atom OLEH roster",
            "55",
            "55 / 55 exact verse membership",
            "38 maqaf-joined, 17 spaced; current selected MAM predicate",
        ),
        (
            "Qamats-alternative templates",
            "about 350",
            str(census["qamats_alternative_templates"]["instances"]),
            "357 verses; approximation tolerance/source date undefined",
        ),
        (
            "Ordinary unpointed ketiv objects",
            "Unpointed ketiv policy",
            "1010 / 1010; zero pointed exceptions",
            "Ordinary types only; colour/live rendering and special types excluded",
        ),
    ]:
        table += (
            "<tr>"
            + "".join(
                f"<td>{html.escape(value)}</td>"
                for value in (label, intro, current, limit)
            )
            + "</tr>"
        )
    table += "</tbody></table>"
    uncertainty_rows = "".join(
        f'<tr><td><a href="#{r["id"]}">{html.escape(r["id"])}</a></td><td>{html.escape(r["status"].replace("-"," "))}</td><td>{html.escape(r["result"])}</td></tr>'
        for r in assessments["assessments"]
    )
    prose_rows = "".join(
        f'<tr><td>{html.escape(status.replace("-"," "))}</td><td>{count}</td></tr>'
        for status, count in general["status_counts"].items()
    )
    fragment_rows = "".join(
        f'<tr><td><a href="{r["source_url"]}">{html.escape(r["claim"])}</a></td><td class="he" dir="rtl">{html.escape(r["requested_fragment"])}</td><td class="he" dir="rtl">{html.escape(r["literal_target_heading"])}</td><td><a href="{r["target_heading_source_url"]}">{html.escape(r["target_heading_source_id"])}</a><br>revision {r["target_revision"]}</td></tr>'
        for r in prose["fragment_cases"]
    )
    fragments = f'<details><summary>Six cached internal targets differ from current headings</summary><div class="scroll"><table><thead><tr><th>Link source</th><th>Requested fragment</th><th>Current heading</th><th>Target source</th></tr></thead><tbody>{fragment_rows}</tbody></table></div><p>Requested targets are absent from cached headings and explicit anchors. The corresponding current headings were reviewed individually. Unexpanded transclusions and live template aliases remain outside this check; no live broken-link verdict follows.</p><p class="meta"><a href="next-pass-prose-findings.json">Reproducible reference, fragment, grouping and date evidence</a></p></details>'
    markup = (
        f'<section id="incremental-pass"><h2>Incremental cached-only pass</h2><p>24/24 uncertainty groups revisited; {general["human_read_units"]}/{general["human_read_units_total"]} additional prose units read and given bounded dispositions. Local subclaims are clarified; physical readings, historical source populations and editorial intent remain explicit limits.</p><div class="scroll">{table}</div><p class="meta"><a href="next-pass-census.json">Census predicates and all membership evidence</a> · <a href="next-pass-assessments.json">24-group evidence and uncertainty register</a> · <a href="general-prose-assessments.json">General-prose ledger</a></p>'
        + "".join(cards)
        + fragments
        + f'<details><summary>Show all 24 incremental dispositions</summary><div class="scroll"><table><thead><tr><th>Original group</th><th>Incremental status</th><th>Resolved subclaims and remaining boundary</th></tr></thead><tbody>{uncertainty_rows}</tbody></table></div></details><details><summary>General-prose boundaries</summary><table><thead><tr><th>Human-read disposition</th><th>Units</th></tr></thead><tbody>{prose_rows}</tbody></table><p>639 ordinary prose units and four historical WLC source-framing units receive bounded checks. The remaining 843 historical Westminster table units are routed separately, without individual semantic assessment or a current-MAM consistency verdict. The population selectors and exact claim IDs remain in the linked ledger.</p></details></section>'
    )
    return markup, contexts, counts
