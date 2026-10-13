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
    intro = "<hr>".join(hbo(intro_display(c)) for c in claims[:1])
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
        bodies.append(prefix + hbo(note["body_text"]))
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
    manifest = json.loads(
        (audit.ROOT / "in/mam-ws-intro/manifest.json").read_text(encoding="utf-8")
    )["pages"]
    revisions = sorted({manifest[c["id"].split(":", 1)[0]]["revid"] for c in claims})
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
    if len(claims) == len(notes) == len(refs) and len(refs) > 1:
        comparison_rows = "".join(
            f'<tr><td class="he" dir="rtl">{hbo(intro_display(c))}</td><td class="he" dir="rtl">{body}</td><td class="bcv">{html.escape(audit.ref_id(ref))}</td></tr>'
            for c, body, ref in zip(claims, bodies, refs)
        )
    else:
        comparison_rows = f'<tr><td class="he" dir="rtl">{intro}</td><td class="he" dir="rtl">{"<hr>".join(bodies)}</td><td class="bcv">{"<br>".join(html.escape(audit.ref_id(r)) for r in refs)}</td></tr>'
    return (
        f"""<article id="{case['id']}"><h3>{html.escape(case['title'])}</h3>
<p class="status">{html.escape(case['status'].replace('-', ' '))}{extra}</p>
<div class="scroll"><table class="comparison"><thead><tr><th>Introduction</th><th>Doc-note</th><th>Verse</th></tr></thead><tbody>{comparison_rows}
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
    other_batches = [read("ch3-pointing-batch.json"), read("ch4-pointing-batch.json")]
    structures = read("structural-populations.json")
    catalogue_comparison = read("catalogue-comparison.json")
    summary = read("summary.json")
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
    audit.dump("claim-dispositions.json", dispositions)
    for batch in other_batches:
        population = [n for group in batch["dispositions"].values() for n in group]
        a, b = batch["range"]
        actual_population = [
            c["line"]
            for c in claims
            if c["id"].startswith(batch["page"] + ":")
            and a <= c["line"] <= b
            and c["text"].startswith("#")
        ]
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
                        "batch": batch["page"] + "-pointing",
                        "status": status,
                        "evidence": by_claim[cid]["evidence"],
                        "supplemental_template_evidence": supplemental,
                    }
                )
    audit.dump("claim-dispositions.json", dispositions)
    coverage = []
    for topic in topics:
        matches = [r for r in routes[topic["page"]] if r[0] <= topic["line"] <= r[1]]
        if len(matches) != 1:
            raise ValueError(f"Topic lacks one coverage route: {topic['id']}")
        route = matches[0]
        coverage.append(
            {
                "topic": topic["id"],
                "heading": topic["heading"],
                "source_url": topic["source_url"],
                "route": route[2],
                "evidence_boundary": route[3],
                "counts": topic["counts"],
                "semantic_status": "bounded-case-dispositions-only; remaining claims unreviewed",
            }
        )
    audit.dump("topic-coverage.json", coverage)
    chapters = read("source-pin.json")["base_commit"]
    all_contexts = []
    sections = []
    for label, key in [
        ("New reviewed discrepancies", "findings"),
        ("Already tracked", "tracked"),
        ("Unresolved cases and limits", "uncertainty"),
        ("Agreement controls", "controls"),
    ]:
        rendered = []
        for case in selection[key]:
            markup, contexts = card(case, by_claim, by_note)
            rendered.append(markup)
            all_contexts.extend(contexts)
        sections.append(f'<section><h2>{label}</h2>{"".join(rendered)}</section>')
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
        '<section><h2>Verse locator family</h2><p>Eight independently checked examples, grouped as one navigation finding. The 3,125 reference joins were inventoried; the complete label/target population has not received semantic review.</p><div class="scroll"><table><thead><tr><th>Introduction</th><th>Linked verse</th><th>Intended verse</th><th>Evidence</th></tr></thead><tbody>'
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
        "all_selected_pointing_rows_reviewed": len(dispositions),
        "catalogue_lines_reviewed": catalogue_comparison["catalogue_lines"],
        "catalogue_membership_matches": catalogue_comparison[
            "matching_membership_lines"
        ],
        "topic_routes": len(coverage),
        "unreviewed_claims_have_no_consistency_verdict": True,
    }
    audit.dump("review-counts.json", counts)
    style = """@font-face{font-family:Taamey;src:url(../woff2/Taamey_D.woff2)}
:root{--he-size:30px;color-scheme:light}body{font:17px/1.6 Georgia,serif;color:#253442;background:#f7f7f3;margin:0}main{max-width:1180px;margin:auto;padding:28px}h1,h2,h3,summary,th,.meta,.status,label{font-family:system-ui,sans-serif}h1{font-size:28px}h2{font-size:23px;margin-top:40px}h3{font-size:19px}article{background:white;border:1px solid #dbe0db;border-radius:8px;padding:20px;margin:18px 0}.he{font:var(--he-size)/1.9 Taamey,'SBL Hebrew',serif;font-weight:400;white-space:pre-wrap;overflow-wrap:anywhere}.latin{font:16px/1.6 Georgia,serif;direction:ltr}.scroll{overflow-x:auto}table{border-collapse:collapse;max-width:100%;background:white}th,td{text-align:left;padding:10px 14px;border-bottom:1px solid #dde3df;vertical-align:top}.comparison td{max-width:430px}.bcv{white-space:nowrap;vertical-align:middle;font:14px/1.5 system-ui,sans-serif}.meta,small{font-size:13px;color:#526359}.status{font-size:13px;color:#49624c}a{color:#215b86}details{margin-top:12px}summary{cursor:pointer;color:#3f5545}.note-target{border-bottom:1px dashed #a1afa5;padding-bottom:8px;margin-bottom:8px}.raw{background:#f7f8f5;padding:16px}input{vertical-align:middle}hr{border:0;border-top:1px solid #dde3df}"""
    intro = f"""<h1>Cached MAM Introduction and doc-notes</h1><p>Source snapshot <code>{chapters}</code>. {len(topics)} topic spans on 13 pages; {summary['explicit_reference_units']:,} verse-linked source units. Pointing batches reviewed {len(dispositions)}/{len(dispositions)} selected rows; 19/19 catalogue memberships were compared. Neither source is presumed authoritative.</p><p class="meta">{counts['new_attributed_form_disagreements']} new attributed-form disagreement groups · {counts['new_other_reviewed_cases']} other reviewed cases · one locator family · 3 tracked issues / 4 verses. Remaining general rules, spelling lists and complete-corpus claims are mapped but not yet fully audited.</p><label for="size">Hebrew size <output id="value">30</output> px </label><input id="size" type="range" min="20" max="48" value="30" aria-label="Hebrew size"><p class="meta"><a href="README.md">Method and limitations</a> · <a href="topic-coverage.json">Coverage data</a> · <a href="review-selections.json">Dispositions</a> · <a href="source-pin.json">Exact source pins</a></p>"""
    output = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cached Introduction audit</title><style>'
        + style
        + "</style></head><body><main>"
        + intro
        + "".join(sections)
        + """</main><script>const slider=document.getElementById('size');slider.addEventListener('input',()=>{document.documentElement.style.setProperty('--he-size',slider.value+'px');document.getElementById('value').textContent=slider.value});</script></body></html>"""
    )
    (audit.OUT / "review.html").write_text(output, encoding="utf-8", newline="\n")
    print(json.dumps(counts, indent=2))
