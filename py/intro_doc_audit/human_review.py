"""Render manually translated comparisons, validating their literal source excerpts."""

import html
import json
import re
from functools import cache

import mwparserfromhell

from intro_doc_audit import audit


def read(name):
    return json.loads((audit.OUT / name).read_text(encoding="utf-8"))


def escaped(value):
    return html.escape(value, quote=True)


def prose(value):
    # Isolate Hebrew embedded in English without changing its codepoints.
    return re.sub(
        r"[\u0591-\u05f4\ufb1e]+(?:[ \u05be][\u0591-\u05f4\ufb1e]+)*",
        lambda match: '<bdi lang="he" dir="rtl">' + match[0] + "</bdi>",
        escaped(value),
    )


def visible_wikitext(value):
    """Hide link/format syntax only; retain the quoted Hebrew codepoints."""
    code = mwparserfromhell.parse(value)
    for link in code.filter_wikilinks():
        code.replace(link, str(link.text or link.title))
    text = str(code).replace("'''", "").replace("''", "")
    return re.sub(r"</?span(?:\s+[^>]*)?>", "", text)


def at_pointer(value, pointer):
    for part in pointer.strip("/").split("/") if pointer else []:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    if not isinstance(value, str):
        raise ValueError("A displayed source pointer must select a string")
    return value


@cache
def parsed_verse_line(path, pointer):
    """Locate the declared verse in the retained canonical JSON formatting."""
    parts = pointer.split("/")
    if parts[:2] != ["", "book39s"] or parts[3] != "chapters":
        raise ValueError("Verse part pointer must identify a canonical verse")
    wanted_book, wanted_chapter, wanted_verse = int(parts[2]), parts[4], parts[5]
    book_index, chapter = -1, None
    for line, text in enumerate(
        (audit.ROOT / path).read_text(encoding="utf-8").splitlines(), 1
    ):
        if text.startswith('      "book24_name":'):
            book_index += 1
            chapter = None
        if match := re.fullmatch(r'        "(\d+)": \{', text):
            chapter = match[1]
        if (
            book_index == wanted_book
            and chapter == wanted_chapter
            and text == f'          "{wanted_verse}": ['
        ):
            return line
    raise ValueError("Declared verse lacks a source line")


class Sources:
    def __init__(self):
        self.claims = {c["id"]: c for c in read("claims.json")}
        self.notes = {n["id"]: n for n in read("notes.json")}
        self.checked = 0

    def resolve(self, passage):
        if "claim" in passage or passage.get("source") == "claim":
            record = self.claims[passage.get("claim", passage.get("id"))]
            literal = record["text"]
        elif "note" in passage or passage.get("source") in {"note", "note-target"}:
            record = self.notes[passage.get("note", passage.get("id"))]
            if passage.get("source") == "note-target":
                literal = at_pointer(record["target_node"], passage.get("pointer", ""))
            else:
                literal = record["body_text"]
        elif passage.get("source") == "verse":
            # This is cached verse context, not a fabricated annotation.
            from intro_doc_audit.review import context

            book, location = passage["id"].rsplit(" ", 1)
            chapter, verse = map(int, location.split(":"))
            record = context([book, chapter, verse])
            literal = record["wikitext"]
            # The faithful raw line is linked; no absent note is manufactured.
            lines = (
                (audit.ROOT / record["path"]).read_text(encoding="utf-8").splitlines()
            )
            line = next(i for i, value in enumerate(lines, 1) if literal in value)
            record = dict(record, source_url=audit.source_url(record["path"], line))
        elif passage.get("source") == "intro-raw":
            path = passage["path"]
            if not re.fullmatch(r"in/mam-ws-intro/[a-z0-9-]+\.mediawiki", path):
                raise ValueError("Raw Introduction source must be a cached page")
            literal = (
                (audit.ROOT / path)
                .read_text(encoding="utf-8")
                .splitlines()[passage["line"] - 1]
            )
            record = {"source_url": audit.source_url(path, passage["line"])}
        elif passage.get("source") == "verse-parts":
            path = passage["path"]
            if not re.fullmatch(r"MAM-parsed/plus/[A-Za-z0-9-]+\.json", path):
                raise ValueError("Verse parts must come from a parsed cached book")
            data = json.loads((audit.ROOT / path).read_text(encoding="utf-8"))
            pieces = []
            for part in passage["parts"]:
                value = at_pointer(data, part["pointer"])
                if part["text"] not in value:
                    raise ValueError("A declared verse part is not literal")
                pieces.append(part["text"])
            literal = "".join(pieces)
            line = parsed_verse_line(path, passage["parts"][0]["pointer"])
            record = {"source_url": audit.source_url(path, line)}
        else:
            raise ValueError(f"Unknown displayed source: {passage}")
        quote = passage.get("quote", passage.get("text"))
        if not quote or quote not in literal:
            raise ValueError(f"Displayed quotation is not literal: {passage}")
        self.checked += 1
        return record


def panel(passage, sources):
    record = sources.resolve(passage)
    translation = passage["translation"]
    if not translation.strip():
        raise ValueError("Every Hebrew passage needs an English translation")
    quote = passage["quote"]
    return (
        '<div class="passage"><h4>'
        + escaped(passage["label"])
        + '</h4><div class="he" lang="he" dir="rtl">'
        + escaped(visible_wikitext(quote))
        + '</div><p class="translation">'
        + prose(translation)
        + '</p><a class="source-link" href="'
        + escaped(record["source_url"])
        + '">Source passage</a></div>'
    )


def card(case, sources):
    for key in ("title", "issue", "context", "explanation", "decision", "panels"):
        if not case.get(key):
            raise ValueError(f"Incomplete readable case {case.get('id')}: {key}")
    passages = "".join(panel(p, sources) for p in case["panels"])
    forms = []
    for form in case.get("reading_forms", []):
        record = sources.resolve(form)
        tooltip = (
            f' title="{escaped(form["mark_name"])}"' if form.get("mark_name") else ""
        )
        forms.append(
            '<div class="reading"><span class="reading-label">'
            + escaped(form["label"])
            + '</span><span class="he" lang="he" dir="rtl"'
            + tooltip
            + ">"
            + escaped(form["text"])
            + '</span><span class="gloss">'
            + escaped(form["gloss"])
            + "</span></div>"
        )
    issue = ""
    if case.get("issue_number"):
        number = case["issue_number"]
        issue = f'<p><a href="https://github.com/bdenckla/MAM-basics/issues/{number}">Tracked in #{number}</a></p>'
    opened = (
        " open"
        if case["id"]
        in {"different-qere-count", "jeremiah-accent", "numbers-yod-label"}
        else ""
    )
    return (
        f'<details class="case" id="{escaped(case["id"])}"{opened}><summary><h3>{prose(case["title"])}</h3>'
        f'<span class="issue">{prose(case["issue"])}</span></summary><article><p>{prose(case["context"])}</p>'
        + '<div class="comparison">'
        + passages
        + "</div>"
        + ('<div class="readings">' + "".join(forms) + "</div>" if forms else "")
        + f'<p>{prose(case["explanation"])}</p>'
        + f'<p class="decision"><strong>Decision:</strong> {prose(case["decision"])}</p>'
        + issue
        + "</article></details>"
    )


STYLE = """@font-face{font-family:Taamey;src:url(../woff2/Taamey_D.woff2)}
:root{--he-size:30px;color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#f5f6f4;color:#22332d;font:17px/1.65 Georgia,serif}main{max-width:1220px;margin:auto;padding:28px}h1,h2,h3,h4,label,nav,.reading-label,.source-link{font-family:system-ui,sans-serif}h1{font-size:29px;line-height:1.3}h2{font-size:24px;margin:42px 0 15px}h3{font-size:21px;margin:0 0 12px}h4{font-size:15px;line-height:1.45;margin:0 0 12px;color:#4e645a}.intro{max-width:850px}.toolbar{position:sticky;top:0;background:#f5f6f4f5;border-bottom:1px solid #d5dfd9;padding:12px 0;z-index:2;display:flex;align-items:center;gap:10px;flex-wrap:wrap}.toolbar nav{margin-left:auto;font-size:14px}a{color:#1f5b85}nav a{margin-left:14px}article{background:white;border:1px solid #d7e0da;border-radius:8px;padding:25px;margin:22px 0;scroll-margin-top:85px}.issue{font-weight:bold;font-size:18px}.comparison{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin:22px 0}.passage{border-left:3px solid #bdcfc2;background:#f6f8f5;padding:16px 18px;min-width:0}.he{font:var(--he-size)/1.9 Taamey,'SBL Hebrew',serif;font-weight:400;white-space:pre-wrap;overflow-wrap:anywhere}.translation{font-size:16px;line-height:1.65;white-space:pre-wrap;margin-bottom:10px}.source-link{font-size:13px}.readings{display:flex;gap:20px;flex-wrap:wrap;border-top:1px solid #dce5de;border-bottom:1px solid #dce5de;padding:14px 0}.reading{display:flex;flex-direction:column;min-width:220px;flex:1}.reading-label,.gloss{font-size:14px}.reading .he{align-self:flex-start}.decision{background:#eef4f0;padding:12px 16px}footer{margin-top:40px;border-top:1px solid #d5dfd9;padding-top:20px;font-size:15px}input{vertical-align:middle}@media(max-width:760px){main{padding:16px}.comparison{grid-template-columns:1fr}.toolbar nav{margin-left:0}nav a{margin-left:0;margin-right:12px}article{padding:18px}}"""


def coverage_report(cases, literal_passages):
    """Account for retained cases; this is presentation coverage, not a verdict."""
    covered = {
        key: [case["id"] for case in cases if key in case["covers"]]
        for case in cases
        for key in case["covers"]
    }
    selection = read("review-selections.json")
    expected = [
        case["id"]
        for group in ("findings", "uncertainty", "tracked")
        for case in selection[group]
    ]
    methods = {
        "PROV-30-5": "Agreement control retained in review-selections.json and the methods appendix.",
        "JOB-11-6": "Agreement control retained in review-selections.json and the methods appendix.",
        "NEXT-NINE-HATAF": "Nine resolved Aleppo agreements retained in next-pass-assessments.json and the methods appendix.",
        "NEXT-IMPLICIT-MS": "The resolved pashta omission appears in IMPLICIT-MS-KINGS-14-7; its proof and quotation scope remain in next-pass-assessments.json.",
    }
    incremental = read("next-pass-review-cases.json")
    navigation = read("navigation-cases.json")
    nav_keys = [
        f"navigation:{case['claim']}:{audit.ref_id(case['intended'])}"
        for case in navigation
    ]
    fragments = read("next-pass-prose-findings.json")["fragment_cases"]
    fragment_keys = ["fragment:" + case["claim"] for case in fragments]
    for population in (expected, nav_keys, fragment_keys):
        if missing := set(population) - set(covered):
            raise ValueError(f"Readable review omits retained results: {missing}")
    if missing := {c["id"] for c in incremental} - set(covered) - set(methods):
        raise ValueError(f"Additional case lacks a readable disposition: {missing}")
    return {
        "source_base_commit": audit.pinned_commit(),
        "purpose": "Presentation coverage and exact-quotation verification; no new semantic consistency verdict.",
        "readable_cases": len(cases),
        "sections": {
            key: sum(case["section"] == key for case in cases)
            for key in ("discrepancies", "questions", "tracked")
        },
        "prior_findings_questions_and_tracked": {
            "covered": len(expected),
            "total": len(expected),
        },
        "additional_case_records": {
            "accounted": len(incremental),
            "total": len(incremental),
        },
        "navigation_source_records": {
            "covered": len(nav_keys),
            "total": len(nav_keys),
            "distinct_record_keys": len(set(nav_keys)),
        },
        "fragment_source_records": {
            "covered": len(fragment_keys),
            "total": len(fragment_keys),
        },
        "literal_passages_checked": literal_passages,
        "comparison_mapping": covered,
        "methods_only_or_resolved": methods,
        "limits": [
            "Exact substring validation does not establish manuscript truth or translation accuracy.",
            "Source reviewers and root reread translations and decisions; physical-source and quotation-scope questions remain explicit.",
            "No cache refresh, manuscript scan, scripture change, issue/comment, main integration or deployment.",
        ],
    }


def main(cases=None, output="review.html"):
    cases = cases if cases is not None else read("human-review.json")
    sources = Sources()
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate readable case IDs")
    sections = []
    for key, title, lead in (
        (
            "discrepancies",
            "Discrepancies to check",
            "These passages make different claims, or contain a concrete wording or reference error.",
        ),
        (
            "questions",
            "Questions about meaning or source",
            "These cases need a scope, attribution or evidence decision before either passage can be called wrong.",
        ),
        (
            "tracked",
            "Already tracked",
            "These discrepancies are recorded in issues #305–307.",
        ),
    ):
        entries = [case for case in cases if case["section"] == key]
        if entries:
            sections.append(
                f'<section id="{key}"><h2>{title}</h2><p>{lead}</p>'
                + "".join(card(case, sources) for case in entries)
                + "</section>"
            )
    output_html = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MAM Introduction and doc-note discrepancies</title><style>'
        + STYLE
        + ".case{background:white;border:1px solid #d7e0da;border-radius:8px;margin:18px 0;scroll-margin-top:85px}.case>summary{cursor:pointer;padding:20px 25px;list-style-position:outside;margin-left:20px}.case>summary h3{display:inline;margin:0}.case>summary .issue{display:block;font:16px/1.6 Georgia,serif;font-weight:400;margin-top:8px}.case article{border:0;border-top:1px solid #d7e0da;border-radius:0;margin:0;padding-top:5px}bdi{unicode-bidi:isolate}#tracked .case>summary .issue{font-size:15px}"
        + '</style></head><body><main><h1>MAM Introduction and doc-note discrepancies</h1><p class="intro">Each comparison gives the relevant Hebrew, an English translation and the decision it raises.</p><div class="toolbar"><label for="size">Hebrew size <output id="value">30</output> px</label><input id="size" type="range" min="20" max="48" value="30" aria-label="Hebrew size"><nav><a href="#discrepancies">Discrepancies</a><a href="#questions">Questions</a><a href="#tracked">Tracked issues</a></nav></div>'
        + "".join(sections)
        + '<footer><a href="METHODS.md">Methods, evidence and coverage</a> · <a href="human-review.json">Translated comparison data</a><p>The source links point to the repository copies used for these comparisons. No manuscript reading has been changed.</p></footer></main><script>const slider=document.getElementById("size");slider.addEventListener("input",()=>{document.documentElement.style.setProperty("--he-size",slider.value+"px");document.getElementById("value").textContent=slider.value});</script></body></html>'
    )
    if output == "review.html":
        audit.dump(
            "human-review-coverage.json", coverage_report(cases, sources.checked)
        )
    (audit.OUT / output).write_text(output_html, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "readable_cases": len(cases),
                "literal_passages_checked": sources.checked,
                "output": output,
            }
        )
    )
