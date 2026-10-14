"""Render compact reviewed evidence and an explicit coverage/uncertainty register."""

import html
import json
import re
from functools import cache

import mwparserfromhell

from mb_cmn import bib_locales as bl
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import uni_denorm
from intro_doc_audit import audit


def read(name):
    return json.loads((audit.OUT / name).read_text(encoding="utf-8"))


def hbo(text):
    # Keep bases and combining marks in the same text node for font shaping.
    # Exact mark names are in the explanations and codepoint-proofs.json.
    return html.escape(text)


@cache
def roster_items():
    return {
        r["claim"]: r["items"]
        for r in read("hataf-rosters.json")["rosters"]
        + read("meteg-roster-review.json")["rosters"]
        + read("poetic-rosters.json")["rosters"]
    }


def source_node(value):
    """Serialize retained parsed structure without projecting or interpreting it."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(source_node(v) for v in value)
    # The source inventory validated the current template schema before this
    # structural serialization; parameters remain labeled rather than flattened.
    name = value["tmpl_name"]
    params = value.get("tmpl_params", {})
    return (
        "{{"
        + name
        + "".join(f"|{key}={source_node(child)}" for key, child in params.items())
        + "}}"
    )


@cache
def raw_book(book):
    path = audit.ROOT / "in/mam-ws" / f"{bl.ordered_short_dash_full_39(book)}.json"
    return path, json.loads(path.read_text(encoding="utf-8"))


def context(ref):
    book, chapter, verse = ref
    path, data = raw_book(book)
    rows = data[hvn.INT_TO_STR_DIC[chapter]]
    start = f"<קטע התחלה={hvn.INT_TO_STR_DIC[verse]}/>"
    end = f"<קטע סוף={hvn.INT_TO_STR_DIC[verse]}/>"
    selected = [row for row in rows if start in row]
    if len(selected) != 1:
        raise ValueError(f"No unique cached verse context: {ref}")
    value = selected[0].split(start, 1)[1].split(end, 1)[0]
    return {
        "ref": audit.ref_id(ref),
        "path": path.relative_to(audit.ROOT).as_posix(),
        "wikitext": value,
    }


def intro_display(claim):
    text = claim["text"]
    templates = mwparserfromhell.parse(text).filter_templates()
    if claim["id"] == "ch2:L968":
        note = next(t for t in templates if str(t.name) == "נוסח")
        return str(note.get("1").value)
    if text.startswith("#[["):
        text = text.partition("]] ")[2]
    if claim["id"] == "ch2:L102":
        return text[text.index('("מִן') :]
    code = mwparserfromhell.parse(text)
    for link in code.filter_wikilinks():
        text = text.replace(str(link), str(link.text or link.title))
    for template in code.filter_templates():
        if str(template.name) in {"עוגן בשורה", "הערה"}:
            text = text.replace(str(template), "")
    text = re.sub(r"</?span(?:\s+[^>]*)?>", "", text)
    return text.replace("'''", "").replace("''", "")


def enumeration_pairs(claim, by_note):
    pairs = []
    for link in mwparserfromhell.parse(claim["text"]).filter_wikilinks():
        ref = audit.resolve_link(str(link.title))
        if not ref:
            continue
        tail = claim["text"].split(str(link), 1)[1]
        specimen = re.search(r"\(([^=]+)=([^)]*)\)", tail)
        if not specimen:
            raise ValueError("Roster specimen lacks an explicit source relation")
        normalized = uni_denorm.give_std_mark_order(specimen[2])
        candidates = [
            n
            for n in by_note.values()
            if n["ref"] == audit.ref_id(ref)
            and normalized in uni_denorm.give_std_mark_order(n["body_text"])
        ]
        if len(candidates) != 1:
            raise ValueError(f"Roster form lacks a unique note quotation: {ref}")
        pairs.append(
            {"ref": ref, "intro_specimen": specimen[0], "note_id": candidates[0]["id"]}
        )
    return pairs


def card(case, by_claim, by_note):
    claims = [by_claim[c] for c in case["claims"]]
    notes = [by_note[n] for n in case["note_ids"]]
    refs = case["refs"]
    extra = ""
    if case.get("issue"):
        extra = f' <a href="https://github.com/bdenckla/MAM-basics/issues/{case["issue"]}">MAM-basics #{case["issue"]}</a>'
    intro_cells = [hbo(intro_display(c)) for c in claims]
    intro = intro_cells[0]
    if case.get("intro_literal_excerpts"):
        intro_cells = []
        for excerpt in case["intro_literal_excerpts"]:
            cid, text = excerpt["claim"], excerpt["text"]
            if text not in by_claim[cid]["text"]:
                raise ValueError(
                    "Introduction review excerpt is not a literal source fragment"
                )
            intro_cells.append(hbo(intro_display({"id": cid, "text": text})))
        intro = "<hr>".join(intro_cells)
    if case.get("intro_roster_items"):
        excerpts = []
        for cid, index in case["intro_roster_items"]:
            item = roster_items()[cid][index - 1]
            excerpts.append(
                hbo(
                    intro_display(
                        {
                            "id": cid,
                            "text": item["literal_link"]
                            + " "
                            + item["literal_specimen"],
                        }
                    )
                )
            )
        intro = "<hr>".join(excerpts)
        intro_cells = excerpts
    enumeration = ""
    if case["id"] == "DEUT-HATAF":
        pairs = enumeration_pairs(claims[0], by_note)
        audit.dump("deuter-roster-pairs.json", pairs)
        intro = hbo("ספר דברים " + re.search(r"\(9 [^)]*\)", claims[0]["text"])[0])
        paired_rows = "".join(
            f'<tr><td class="he" dir="rtl">{hbo(p["intro_specimen"])}</td><td class="he" dir="rtl">{hbo(by_note[p["note_id"]]["body_text"])}</td><td class="bcv">{html.escape(audit.ref_id(p["ref"]))}<br><a href="{by_note[p["note_id"]]["source_url"]}">note</a></td></tr>'
            for p in pairs
        )
        enumeration = (
            '<details><summary>Show all eleven Introduction / doc-note pairs</summary><div class="scroll"><table><thead><tr><th>Introduction</th><th>Doc-note</th><th>Verse</th></tr></thead><tbody>'
            + paired_rows
            + "</tbody></table></div></details>"
        )
    bodies = []
    for note in notes:
        target = note["target_node"]
        prefix = (
            '<div class="note-target">' + hbo(target) + "</div>"
            if isinstance(target, str)
            else ""
        )
        excerpts = case.get("note_excerpts", {}).get(note["id"])
        if excerpts:
            if not all(fragment in note["body_text"] for fragment in excerpts):
                raise ValueError("Review excerpt is not a literal note fragment")
            shown = (
                hbo("\n".join(excerpts))
                + '<details><summary class="latin">Full note</summary>'
                + hbo(note["body_text"])
                + "</details>"
            )
        else:
            shown = hbo(note["body_text"])
        bodies.append(prefix + shown)
    if case.get("supporting_intro_claims"):
        bodies = [
            hbo(intro_display(by_claim[cid])) for cid in case["supporting_intro_claims"]
        ]
    if case.get("paired_supporting_intro_excerpts"):
        excerpts = case["paired_supporting_intro_excerpts"]
        if len(excerpts) != len(bodies):
            raise ValueError("Paired Introduction support must align with note rows")
        for index, excerpt in enumerate(excerpts):
            cid, text = excerpt["claim"], excerpt["text"]
            if text not in by_claim[cid]["text"]:
                raise ValueError(
                    "Paired support is not a literal Introduction fragment"
                )
            bodies[
                index
            ] += '<hr><div class="latin">Other Introduction passage</div>' + hbo(
                intro_display({"id": cid, "text": text})
            )
    if case.get("right_literal_excerpts"):
        bodies = []
        for excerpt in case["right_literal_excerpts"]:
            cid, text = excerpt["claim"], excerpt["text"]
            if text not in by_claim[cid]["text"]:
                raise ValueError(
                    "Right-column support is not a literal Introduction fragment"
                )
            bodies.append(hbo(intro_display({"id": cid, "text": text})))
    if case.get("cached_contexts_as_comparison"):
        bodies = [
            f'<div class="latin">{html.escape(audit.ref_id(ref))}</div>'
            + hbo(context(ref)["wikitext"])
            for ref in refs
        ]
    if not bodies:
        bodies = [
            (
                "<p class=latin>All eleven listed verse cases have matching source forms in the notes. Expand the paired evidence below.</p>"
                if enumeration
                else "<p class=latin>This case uses the parsed structure or cached policy as supplemental evidence; see the explanation and context.</p>"
            )
        ]
    cite = " · ".join(
        f'<a href="{c["source_url"]}">{html.escape(c["id"])}</a>' for c in claims
    )
    cite += " · " + " · ".join(
        f'<a href="{n["source_url"]}">note {html.escape(n["ref"])}</a>' for n in notes
    )
    supporting_ids = list(
        dict.fromkeys(
            case.get("supporting_intro_claims", [])
            + [
                e["claim"]
                for e in case.get("paired_supporting_intro_excerpts", [])
                + case.get("right_literal_excerpts", [])
            ]
        )
    )
    if supporting_ids:
        cite += " · " + " · ".join(
            f'<a href="{by_claim[cid]["source_url"]}">support {html.escape(cid)}</a>'
            for cid in supporting_ids
        )
    if case.get("supplemental_sources"):
        cite += " · " + " · ".join(
            f'<a href="{html.escape(s["url"], quote=True)}">{html.escape(s["label"])}</a>'
            for s in case["supplemental_sources"]
        )
    manifest = json.loads(
        (audit.ROOT / "in/mam-ws-intro/manifest.json").read_text(encoding="utf-8")
    )["pages"]
    revisions = sorted(
        {
            manifest[c["id"].split(":", 1)[0]]["revid"]
            for c in claims + [by_claim[cid] for cid in supporting_ids]
        }
    )
    cite += "<br>Introduction revisions: " + " · ".join(
        f'<a href="https://he.wikisource.org/w/index.php?oldid={r}">{r}</a>'
        for r in revisions
    )
    note_revisions = sorted({n["chapter_revision"]["revision_id"] for n in notes})
    if note_revisions:
        cite += " · chapter-note revisions: " + " · ".join(
            f'<a href="https://he.wikisource.org/w/index.php?oldid={r}">{r}</a>'
            for r in note_revisions
        )
    contexts = [context(ref) for ref in refs]
    context_html = "".join(
        f'<details><summary>Cached verse context: {html.escape(c["ref"])}</summary><div class="he raw" dir="rtl">{hbo(c["wikitext"])}</div></details>'
        for c in contexts
    )
    if len(contexts) > 3:
        context_html = f"<details><summary>Cached contexts for {len(contexts)} verses</summary>{context_html}</details>"
    if len(intro_cells) == len(notes) == len(refs) and len(refs) > 1:
        comparison_rows = "".join(
            f'<tr><td class="he" dir="rtl">{cell}</td><td class="he" dir="rtl">{body}</td><td class="bcv">{html.escape(audit.ref_id(ref))}</td></tr>'
            for cell, body, ref in zip(intro_cells, bodies, refs)
        )
    else:
        right_class, right_direction = (
            ("latin", "ltr") if case.get("right_is_latin") else ("he", "rtl")
        )
        comparison_rows = f'<tr><td class="he" dir="rtl">{intro}</td><td class="{right_class}" dir="{right_direction}">{"<hr>".join(bodies)}</td><td class="bcv">{"<br>".join(html.escape(audit.ref_id(r)) for r in refs)}</td></tr>'
    return (
        f"""<article id="{case['id']}"><h3>{html.escape(case['title'])}</h3>
<p class="status">{html.escape(case['status'].replace('-', ' '))}{extra}</p>
<div class="scroll"><table class="comparison"><thead><tr><th>Introduction</th><th>{html.escape(case.get('right_label', 'Doc-note'))}</th><th>Verse</th></tr></thead><tbody>{comparison_rows}
</tbody></table></div><p>{html.escape(case['explanation'])}</p><p class="meta">{cite}</p>{enumeration}{context_html}</article>""",
        contexts,
    )


def main():
    claims = read("claims.json")
    notes = read("notes.json")
    topics = read("topics.json")
    routes = read("coverage-routes.json")
    selection = read("review-selections.json")
    navigation = read("navigation-cases.json")
    ketiv = read("ketiv-batch.json")
    nonketiv = read("nonketiv-batch.json")
    other_batches = [
        read("ch3-pointing-batch.json"),
        read("ch4-pointing-batch.json"),
        read("ch4-spelling-batch.json"),
        read("ch3-spelling-batch.json"),
        read("ch2-secondary-batch.json"),
        read("ch5-earlier-batch.json"),
    ]
    structures = read("structural-populations.json")
    catalogue_comparison = read("catalogue-comparison.json")
    summary = read("summary.json")
    hataf_review = read("hataf-rosters.json")
    meteg_review = read("meteg-roster-review.json")
    policy = read("policy-assessments.json")
    by_claim = {c["id"]: c for c in claims}
    by_note = {n["id"]: n for n in notes}
    ledger = [n for group in ketiv["dispositions"].values() for n in group]
    actual = [
        c["line"]
        for c in claims
        if c["id"].startswith("ch5:") and "א-כתיב" in c["text"]
    ]
    if len(ledger) != len(set(ledger)) or set(ledger) != set(actual):
        raise ValueError("Ketiv review ledger does not cover its declared population")
    nk_ledger = [n for group in nonketiv["dispositions"].values() for n in group]
    nk_actual = [
        c["line"]
        for c in claims
        if c["id"].startswith("ch5:")
        and "א-כתיב" not in c["text"]
        and c["text"].startswith("#")
        and any(a <= c["line"] <= b for a, b in nonketiv["primary_ranges"])
    ] + nonketiv["neighboring_lines"]
    if len(nk_ledger) != len(set(nk_ledger)) or set(nk_ledger) != set(nk_actual):
        raise ValueError(
            "Nonketiv review ledger does not cover its declared population"
        )
    dispositions = []
    for batch_name, batch in [("ketiv", ketiv), ("nonketiv", nonketiv)]:
        for status, population in batch["dispositions"].items():
            for line in population:
                cid = f"ch5:L{line}"
                if cid not in by_claim:
                    raise ValueError(f"Review ledger source missing: {cid}")
                dispositions.append(
                    {
                        "claim": cid,
                        "batch": batch_name,
                        "status": status,
                        "evidence": by_claim[cid]["evidence"],
                    }
                )
    for batch in other_batches:
        population = [n for group in batch["dispositions"].values() for n in group]
        selectors = batch.get("selectors") or [
            {"range": batch["range"], "prefixes": ["#"]}
        ]
        actual_population = sorted(
            {
                line
                for c in claims
                for s in selectors
                if c["id"].startswith(batch["page"] + ":")
                and s["range"][0] <= c["line"] <= s["range"][1]
                and any(c["text"].startswith(p) for p in s["prefixes"])
                for line in range(
                    c["line"], c["line"] + s.get("following_units", 0) + 1
                )
            }
        )
        if len(population) != len(set(population)) or set(population) != set(
            actual_population
        ):
            raise ValueError(f"Incomplete reviewed population: {batch['page']}")
        for status, lines in batch["dispositions"].items():
            for line in lines:
                cid = f"{batch['page']}:L{line}"
                supplemental = (
                    [
                        r
                        for r in structures["records"]
                        if r["category"] == "מ:קו״כ-אם-2"
                        and any(r["ref"] == e["ref"] for e in by_claim[cid]["evidence"])
                    ]
                    if status == "corroborated-structured-template-provenance"
                    else []
                )
                dispositions.append(
                    {
                        "claim": cid,
                        "batch": batch.get("batch", batch["page"] + "-pointing"),
                        "status": status,
                        "evidence": by_claim[cid]["evidence"],
                        "supplemental_template_evidence": supplemental,
                    }
                )
    bounded_list_units = len(dispositions)
    for batch in policy["batches"]:
        population = [n for ns in batch["dispositions"].values() for n in ns]
        a, b = batch["range"]
        expected = {
            c["line"]
            for c in claims
            if c["id"].startswith(batch["page"] + ":") and a <= c["line"] <= b
        }
        if len(population) != len(set(population)) or set(population) != expected:
            raise ValueError(
                "Policy assessment does not account for its declared units"
            )
        for status, lines in batch["dispositions"].items():
            for line in lines:
                cid = f"{batch['page']}:L{line}"
                dispositions.append(
                    {
                        "claim": cid,
                        "batch": "policy-assessment",
                        "status": status,
                        "evidence": by_claim[cid]["evidence"],
                    }
                )
    for row in hataf_review["rosters"]:
        dispositions.append(
            {
                "claim": row["claim"],
                "batch": "hataf-roster",
                "status": "item-ledger-assessed;see-individual-dispositions",
                "evidence": by_claim[row["claim"]]["evidence"],
                "item_statuses": {i["id"]: i["status"] for i in row["items"]},
            }
        )
    for row in meteg_review["rosters"]:
        dispositions.append(
            {
                "claim": row["claim"],
                "batch": "meteg-roster",
                "status": "item-ledger-assessed;see-individual-dispositions",
                "evidence": by_claim[row["claim"]]["evidence"],
                "item_statuses": {i["id"]: i["status"] for i in row["items"]},
            }
        )
    scoped = read("scoped-assessments.json")
    general = read("general-prose-assessments.json")
    for batch in scoped["batches"] + general["batches"]:
        population = [cid for ids in batch["dispositions"].values() for cid in ids]
        selector = batch["selection"]
        expected = (
            {
                c["id"]
                for c in claims
                if c["id"].startswith(batch["page"] + ":")
                and selector.get("min_line", 1)
                <= c["line"]
                <= selector.get("max_line", 100000)
                and (not selector.get("explicit_refs_only") or c["refs"])
                and c["id"] not in selector.get("exclude_claims", [])
            }
            if "claim_ids" not in selector
            else set(selector["claim_ids"])
        )
        if (
            len(population) != len(set(population))
            or set(population) != expected
            or len(population) != batch["total"]
        ):
            raise ValueError(f"Incomplete scoped assessment: {batch['id']}")
        for status, ids in batch["dispositions"].items():
            for cid in ids:
                dispositions.append(
                    {
                        "claim": cid,
                        "batch": batch["id"],
                        "status": status,
                        "evidence": by_claim[cid]["evidence"],
                    }
                )
    unique = {}
    for assessment in dispositions:
        cid = assessment["claim"]
        if cid in unique:
            unique[cid].setdefault("additional_assessments", []).append(
                {
                    key: value
                    for key, value in assessment.items()
                    if key not in {"claim", "evidence"}
                }
            )
        else:
            unique[cid] = assessment
    dispositions = list(unique.values())
    audit.dump("claim-dispositions.json", dispositions)
    pointing_reviewed = (
        len(ledger)
        + len(nk_ledger)
        + sum(
            (
                b["reviewed"]
                if "selectors" not in b
                else b.get("included_pointing_rows", 0)
            )
            for b in other_batches
        )
    )
    reviewed_ids = {d["claim"] for d in dispositions}
    coverage = []
    for topic in topics:
        matches = [r for r in routes[topic["page"]] if r[0] <= topic["line"] <= r[1]]
        if len(matches) != 1:
            raise ValueError(f"Topic lacks one coverage route: {topic['id']}")
        route = matches[0]
        topic_claims = [c for c in claims if c["topic"] == topic["id"]]
        reviewed = [c["id"] for c in topic_claims if c["id"] in reviewed_ids]
        pending_refs = [
            c["id"] for c in topic_claims if c["refs"] and c["id"] not in reviewed_ids
        ]
        coverage.append(
            {
                "topic": topic["id"],
                "heading": topic["heading"],
                "source_url": topic["source_url"],
                "route": route[2],
                "evidence_boundary": route[3],
                "counts": topic["counts"],
                "reviewed_source_units": reviewed,
                "pending_explicit_reference_units": pending_refs,
                "semantic_status": "explicit-reference and selected ordinary-prose source units assessed; broader universals, routing-only cells and other non-reference claims retain the stated evidence boundary",
            }
        )
    audit.dump("topic-coverage.json", coverage)
    chapters = read("source-pin.json")["base_commit"]
    all_contexts = []
    sections = []
    from intro_doc_audit import incremental_review

    incremental, contexts, incremental_counts = incremental_review.render(
        by_claim, by_note
    )
    sections.append(incremental)
    all_contexts.extend(contexts)
    for label, key in [
        ("New reviewed discrepancies", "findings"),
        ("Already tracked", "tracked"),
        ("Unresolved cases and limits", "uncertainty"),
        ("Agreement controls", "controls"),
    ]:
        rendered = []
        for case in selection[key]:
            markup, contexts = card(case, by_claim, by_note)
            if key == "findings":
                markup = f'<details class="finding"><summary>{html.escape(case["title"])} <small>{html.escape(case["status"].replace("-", " "))}</small></summary>{markup}</details>'
            rendered.append(markup)
            all_contexts.extend(contexts)
        body = "".join(rendered)
        if key in {"tracked", "uncertainty", "controls"}:
            body = f"<details><summary>Show {len(rendered)} {label.lower()}</summary>{body}</details>"
        sections.append(f"<section><h2>{label}</h2>{body}</section>")
    nav_rows = []
    for case in navigation:
        c = by_claim[case["claim"]]
        matches = [n for n in notes if n["ref"] == audit.ref_id(case["intended"])]
        nav_rows.append(
            f'<tr><td><a href="{c["source_url"]}">{html.escape(c["id"])}</a></td><td class="bcv">{html.escape(audit.ref_id(case["wrong"]))}</td><td class="bcv">{html.escape(audit.ref_id(case["intended"]))}</td><td>{html.escape(case["reason"])} '
            + " ".join(f'<a href="{n["source_url"]}">note</a>' for n in matches[:1])
            + "</td></tr>"
        )
    sections.append(
        f'<section><h2>Verse locator family</h2><p>{len(navigation)} independently checked examples, grouped as one navigation finding. The 3,125 reference joins were inventoried; the complete label/target population has not received semantic review.</p><div class="scroll"><table><thead><tr><th>Introduction</th><th>Linked verse</th><th>Intended verse</th><th>Evidence</th></tr></thead><tbody>'
        + "".join(nav_rows)
        + "</tbody></table></div></section>"
    )
    rows = "".join(
        f'<tr><td><a href="{c["source_url"]}">{html.escape(c["topic"])}</a></td><td class="he" dir="rtl">{hbo(c["heading"])}</td><td>{html.escape(c["route"])}<br><small>{html.escape(c["evidence_boundary"].replace('-', ' '))}</small></td><td>{c["counts"]["source_units"]} / {c["counts"]["explicit_reference_units"]}</td></tr>'
        for c in coverage
    )
    sections.append(
        f'<section><h2>Complete topic coverage map</h2><p>All {len(coverage)} titled spans are mapped to an evidence boundary. A mapped topic is not a completed semantic audit. Counts below are source units / units with explicit verse references.</p><details><summary>Show all topic routes</summary><div class="scroll"><table><thead><tr><th>Source</th><th>Heading</th><th>Evidence route</th><th>Counts</th></tr></thead><tbody>{rows}</tbody></table></div></details></section>'
    )
    audit.dump(
        "review-contexts.json", list({c["ref"]: c for c in all_contexts}.values())
    )
    counts = {
        "new_attributed_form_disagreements": sum(
            c["status"] == "new-supported-source-disagreement"
            for c in selection["findings"]
        ),
        "new_other_reviewed_cases": sum(
            c["status"] != "new-supported-source-disagreement"
            for c in selection["findings"]
        ),
        "navigation_family_examples": len(navigation),
        "tracked_issues": len(selection["tracked"]),
        "tracked_verse_cases": 4,
        "uncertainty_cases": len(selection["uncertainty"]),
        "ketiv_lines_reviewed": len(ledger),
        "ketiv_lines_total": len(actual),
        "nonketiv_lines_reviewed": len(nk_ledger),
        "nonketiv_lines_total": len(nk_actual),
        "chapter5_selected_lines_reviewed": len(ledger) + len(nk_ledger),
        "chapter3_pointing_lines_reviewed": other_batches[0]["reviewed"],
        "chapter3_pointing_lines_total": other_batches[0]["total"],
        "chapter4_pointing_lines_reviewed": other_batches[1]["reviewed"],
        "chapter4_pointing_lines_total": other_batches[1]["total"],
        "all_selected_pointing_rows_reviewed": pointing_reviewed,
        "chapter4_spelling_units_reviewed": other_batches[2]["reviewed"],
        "chapter4_spelling_units_total": other_batches[2]["total"],
        "chapter3_spelling_units_reviewed": other_batches[3]["reviewed"],
        "chapter3_spelling_units_total": other_batches[3]["total"],
        "chapter2_secondary_units_reviewed": other_batches[4]["reviewed"],
        "chapter2_secondary_units_total": other_batches[4]["total"],
        "chapter5_earlier_entry_anchors_reviewed": other_batches[5][
            "entry_anchors_reviewed"
        ],
        "chapter5_earlier_entry_anchors_total": other_batches[5]["entry_anchors_total"],
        "chapter5_earlier_source_units_reviewed": other_batches[5]["reviewed"],
        "chapter5_earlier_source_units_total": other_batches[5]["total"],
        "all_selected_units_reviewed": len(dispositions),
        "bounded_list_source_units_reviewed": bounded_list_units,
        "policy_units_assessed": sum(b["reviewed"] for b in policy["batches"]),
        "scoped_units_assessed": sum(b["reviewed"] for b in scoped["batches"]),
        "explicit_reference_units_assessed": sum(
            bool(c["refs"]) and c["id"] in reviewed_ids for c in claims
        ),
        "explicit_reference_units_total": summary["explicit_reference_units"],
        "hataf_roster_items_reviewed": sum(
            len(r["items"]) for r in hataf_review["rosters"]
        ),
        "hataf_roster_items_total": read("roster-review.json")["total_items"],
        "meteg_roster_items_reviewed": meteg_review["reviewed"],
        "meteg_roster_items_total": meteg_review["total"],
        "poetic_roster_items_reviewed": read("poetic-rosters.json")["reviewed"],
        "poetic_roster_items_total": read("poetic-rosters.json")["total"],
        "catalogue_lines_reviewed": catalogue_comparison["catalogue_lines"],
        "catalogue_membership_matches": catalogue_comparison[
            "matching_membership_lines"
        ],
        "topic_routes": len(coverage),
        "unreviewed_claims_have_no_consistency_verdict": True,
        "incremental_cached_pass": incremental_counts,
    }
    audit.dump("review-counts.json", counts)
    from intro_doc_audit import human_review

    human_review.main()
