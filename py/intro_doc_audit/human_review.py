"""Render manually translated comparisons, validating their literal source excerpts."""

import html
import json
import re
from collections import Counter
from functools import cache

import mwparserfromhell

from intro_doc_audit import audit, snapshot
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn.he_wikisource_url import he_page_url
from mb_cmn.mam_bknas_and_std_bknas import he_bk39_name


def read(name):
    return json.loads((audit.OUT / name).read_text(encoding="utf-8"))


def escaped(value):
    return html.escape(value, quote=True)


def prose(value, quotations=()):
    # Isolate Hebrew embedded in English without changing its codepoints.
    if quotations:
        positions = []
        for quote in quotations:
            if not quote or value.count(quote) != 1:
                raise ValueError(
                    "An explicit Hebrew quotation needs one exact occurrence"
                )
            positions.append((value.index(quote), quote))
        rendered, cursor = [], 0
        for start, quote in sorted(positions):
            if start < cursor:
                raise ValueError("Explicit Hebrew quotations must not overlap")
            rendered.append(prose(value[cursor:start]))
            rendered.append(
                '<bdi class="he-quote" lang="he" dir="rtl">' + escaped(quote) + "</bdi>"
            )
            cursor = start + len(quote)
        rendered.append(prose(value[cursor:]))
        return "".join(rendered)
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


def json_node(value, pointer):
    for part in pointer.strip("/").split("/") if pointer else []:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def at_pointer(value, pointer):
    value = json_node(value, pointer)
    if not isinstance(value, str):
        raise ValueError("A displayed source pointer must select a string")
    return value


def strings_in(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        value = list(value.values())
    if not isinstance(value, list):
        return []
    return [text for item in value for text in strings_in(item)]


@cache
def parsed_verse_line(path, pointer):
    """Locate the declared verse in the retained canonical JSON formatting."""
    parts = pointer.split("/")
    if parts[:2] != ["", "book39s"] or parts[3] != "chapters":
        raise ValueError("Verse part pointer must identify a canonical verse")
    wanted_book, wanted_chapter, wanted_verse = int(parts[2]), parts[4], parts[5]
    book_index, chapter = -1, None
    for line, text in enumerate(snapshot.text(path).splitlines(), 1):
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
        self.proposals_checked = 0
        self.applications_checked = 0

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
            lines = snapshot.text(record["path"]).splitlines()
            encoded = json.dumps(literal, ensure_ascii=False)[1:-1]
            line = next(i for i, value in enumerate(lines, 1) if encoded in value)
            record = dict(record, source_url=audit.source_url(record["path"], line))
        elif passage.get("source") == "intro-raw":
            path = passage["path"]
            if not re.fullmatch(r"in/mam-ws-intro/[a-z0-9-]+\.mediawiki", path):
                raise ValueError("Raw Introduction source must be a cached page")
            literal = snapshot.text(path).splitlines()[passage["line"] - 1]
            record = {"source_url": audit.source_url(path, passage["line"])}
        elif passage.get("source") == "verse-parts":
            path = passage["path"]
            if not re.fullmatch(r"MAM-parsed/plus/[A-Za-z0-9-]+\.json", path):
                raise ValueError("Verse parts must come from a parsed cached book")
            data = snapshot.data(path)
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


@cache
def intro_page_titles():
    """The mirrored Introduction pages' Wikisource titles, by page key."""
    pages = json.loads(
        (audit.ROOT / "in/mam-ws-intro/manifest.json").read_text(encoding="utf-8")
    )["pages"]
    return {key: page["title"] for key, page in pages.items()}


@cache
def mirror_headings(path):
    """The current mirror's headings in page order, each with its MediaWiki anchor."""
    seen, headings = Counter(), []
    for line in (audit.ROOT / path).read_text(encoding="utf-8").splitlines():
        if match := audit.HEAD.match(line):
            text = " ".join(match[2].split())
            anchor = text.replace(" ", "_")
            seen[anchor] += 1
            if seen[anchor] > 1:
                anchor += f"_{seen[anchor]}"
            headings.append((text, anchor))
    return headings


# Linked snapshot headings that a later Introduction edit renamed, by page, each with
# the current mirror's heading. 0cb9332a's mirror refresh brought this one: the
# Westminster page's revision 3092678 corrects the spelling of Westminster.
RENAMED_HEADINGS = {
    (
        "in/mam-ws-intro/westminster-typing.mediawiki",
        "רשימת ההערות בהקלדת וסטמינטר ופירושם",
    ): "רשימת ההערות בהקלדת וסטמינסטר ופירושם",
}


def section_link(path, line):
    """Link the live Introduction page at the snapshot heading at or above line.

    The heading comes from the recorded snapshot; its anchor comes from the current
    mirror, which stands in for the live page, through RENAMED_HEADINGS where a later
    edit renamed it. A heading the current mirror lacks stops the build rather than
    leaving a dead anchor.
    """
    if not re.fullmatch(r"in/mam-ws-intro/[a-z0-9-]+\.mediawiki", path):
        raise ValueError("An Introduction link needs a cached Introduction page")
    above = [
        " ".join(match[2].split())
        for text in snapshot.text(path).splitlines()[:line]
        if (match := audit.HEAD.match(text))
    ]
    page_key = path.removeprefix("in/mam-ws-intro/").removesuffix(".mediawiki")
    title = intro_page_titles()[page_key]
    if not above:
        return he_page_url(title.replace(" ", "_")), escaped(title)
    heading = above[-1]
    if re.search(r"[\[\]{}<>'&]", heading):
        raise ValueError(f"Heading markup needs its own anchor rule: {heading}")
    current = RENAMED_HEADINGS.get((path, heading), heading)
    if current != heading and heading in (text for text, _ in mirror_headings(path)):
        raise ValueError(f"A heading listed as renamed is still current: {heading!r}")
    anchors = [a for text, a in mirror_headings(path) if text == current]
    occurrence = above.count(heading)
    if len(anchors) < occurrence:
        raise ValueError(f"The current mirror lacks the heading {current!r} in {path}")
    url = he_page_url(title.replace(" ", "_"), anchors[occurrence - 1])
    return url, prose(heading, (heading,))


def verse_link(title, ref):
    """Link the live MAM chapter page at the verse's anchor."""
    chapter, verse = map(int, ref.rsplit(" ", 1)[1].split(":"))
    chapter_he, verse_he = hvn.INT_TO_STR_DIC[chapter], hvn.INT_TO_STR_DIC[verse]
    if not title.endswith(f" {chapter_he}/טעמים"):
        raise ValueError(f"The chapter page {title} does not hold {ref}")
    url = he_page_url(title.replace(" ", "_"), f"{chapter_he}_{verse_he}")
    return url, escaped(ref)


def wikisource_link(passage, sources):
    """Return the URL and label of the live Wikisource place a passage quotes.

    The link is to the live page, so after a later edit it can show newer text than
    the quotation; Ben chose that on 2026-10-17. Dispatch follows Sources.resolve.
    """
    if "claim" in passage or passage.get("source") == "claim":
        claim = sources.claims[passage.get("claim", passage.get("id"))]
        return section_link(claim["path"], claim["line"])
    if "note" in passage or passage.get("source") in {"note", "note-target"}:
        note = sources.notes[passage.get("note", passage.get("id"))]
        return verse_link(note["chapter_revision"]["resolved_title"], note["ref"])
    if passage.get("source") == "intro-raw":
        return section_link(passage["path"], passage["line"])
    if passage.get("source") == "verse":
        book, location = passage["id"].rsplit(" ", 1)
        chapter_he = hvn.INT_TO_STR_DIC[int(location.split(":")[0])]
        return verse_link(f"{he_bk39_name(book)} {chapter_he}/טעמים", passage["id"])
    raise ValueError(f"No Wikisource link rule for this passage: {passage}")


def panel(passage, sources):
    sources.resolve(passage)
    url, label = wikisource_link(passage, sources)
    if passage.get("entire_note"):
        if passage["quote"] != sources.notes[passage["note"]]["body_text"]:
            raise ValueError("A complete note panel must contain the entire note")
        clauses = passage["translation_clauses"]
        if (
            "\n".join(c["source"] for c in clauses) != passage["quote"]
            or "\n\n".join(c["translation"] for c in clauses) != passage["translation"]
        ):
            raise ValueError(
                "Complete-note clauses must match the displayed translation"
            )
    kind = passage.get("kind", "explanatory")
    if kind not in {"explanatory", "scripture"}:
        raise ValueError(f"Unknown passage kind: {kind}")
    translation = passage.get("translation", "")
    if kind == "explanatory" and not translation.strip():
        raise ValueError(
            "An explanatory passage needs its explanatory prose translated"
        )
    if kind == "scripture" and translation:
        raise ValueError("Scripture-only quotations are not translated in this review")
    quote = passage["quote"]
    return (
        '<div class="passage'
        + (" full-width" if passage.get("full_width") else "")
        + '"><h4>'
        + escaped(passage["label"])
        + '</h4><p class="source-link"><a href="'
        + escaped(url)
        + '">Wikisource: '
        + label
        + '</a></p><div class="he" lang="he" dir="rtl">'
        + escaped(visible_wikitext(quote))
        + "</div>"
        + (
            '<p class="translation">'
            + prose(translation, passage.get("translation_quotes", ()))
            + "</p>"
            if translation
            else ""
        )
        + "</div>"
    )


def membership_table(comparison, sources):
    rows = []
    for row in comparison["rows"]:
        cells = ['<td class="verse">' + escaped(row["ref"]) + "</td>"]
        for side in ("chapter2", "appendix"):
            entry = row[side]
            if entry is None:
                cells.append('<td colspan="2">Not listed</td>')
            else:
                for key in ("ketiv", "qere"):
                    sources.resolve({"claim": entry["claim"], "text": entry[key]})
                    cells.append(
                        '<td class="he" lang="he" dir="rtl">'
                        + escaped(entry[key])
                        + "</td>"
                    )
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return (
        '<div class="membership"><table><caption>'
        + prose(comparison["caption"])
        + '</caption><thead><tr><th rowspan="2">Verse</th><th colspan="2">Chapter 2 — three entries</th><th colspan="2">Appendix — four entries</th></tr><tr><th>Ketiv</th><th>Qere</th><th>Ketiv</th><th>Qere</th></tr></thead><tbody>'
        + "".join(rows)
        + "</tbody></table></div>"
    )


PROPOSED_LABELS = {
    "unapplied": "Ben’s proposed corrected quotation — not applied",
    "applied": "Ben’s proposed corrected quotation — applied",
}


def edited(quote, changes):
    for change in changes:
        if quote.count(change["before"]) != 1:
            raise ValueError("A quotation edit needs one exact source occurrence")
        quote = quote.replace(change["before"], change["after"], 1)
    return quote


def applied_row(entry, sources):
    """Check an applied proposal against the later mirror commit that holds it."""
    record, current = entry["application"], entry["current"]
    expected = edited(
        current["quote"], [entry["changes"][i] for i in record["applied_changes"]]
    )
    if visible_wikitext(record["quote"]) != expected:
        raise ValueError("The applied quotation differs from its recorded edits")
    commit, path = record["mirror_commit"], record["mirror_path"]
    if "note" in current:
        note = sources.notes[current["note"]]
        if path != note["path"]:
            raise ValueError("An applied doc-note is read in its note's parsed book")
        book = json.loads(snapshot.text_at(commit, path))
        texts = strings_in(json_node(book, note["json_pointer"]))
        revisions = json.loads(snapshot.text_at(commit, "in/mam-ws-revisions.json"))
        mirrored = [
            chapter["revision_id"]
            for chapters in revisions["books"].values()
            for chapter in chapters.values()
            if chapter["page_id"] == note["chapter_revision"]["page_id"]
        ]
    elif "claim" in current:
        if path != sources.claims[current["claim"]]["path"]:
            raise ValueError("An applied Introduction edit is read in its own page")
        texts = [snapshot.text_at(commit, path)]
        page = path.removeprefix("in/mam-ws-intro/").removesuffix(".mediawiki")
        manifest = json.loads(snapshot.text_at(commit, "in/mam-ws-intro/manifest.json"))
        mirrored = [manifest["pages"][page]["revid"]]
    else:
        raise ValueError(f"No mirror rule for an applied proposal: {entry['id']}")
    if sum(text.count(record["quote"]) for text in texts) != 1 or any(
        current["quote"] in text for text in texts
    ):
        raise ValueError("The mirror must have the applied text once, the old nowhere")
    if (
        mirrored != [record["mirror_revision_id"]]
        or record["mirror_revision_id"] < record["revision_id"]
    ):
        raise ValueError("The mirror must hold the applying revision or a later one")
    sources.applications_checked += 1
    link = (record["diff_url"], f"Wikisource: revision {record['revision_id']}")
    return record["label"], record["quote"], record["explanation"], link


def adjudication_comparison(case, sources):
    entries = [a for a in read("adjudications.json") if a["id"] == case["adjudication"]]
    if len(entries) != 1:
        raise ValueError("An adjudication must identify one retained research record")
    entry = entries[0]
    if (
        entry["case"] != case["id"]
        or entry["source_base_commit"] != audit.pinned_commit()
    ):
        raise ValueError("Adjudication case or source snapshot does not match")
    sources.resolve(entry["current"])
    proposed = edited(entry["current"]["quote"], entry["changes"])
    if proposed != entry["proposed_quotation"]:
        raise ValueError("The proposed quotation differs from its recorded edits")
    sources.proposals_checked += 1
    status = entry["application_status"]
    if status not in PROPOSED_LABELS:
        raise ValueError(f"Unknown application status: {status}")
    if (status == "applied") != ("application" in entry):
        raise ValueError("Only an applied proposal carries an application record")
    proposed_label = entry.get("proposed_label", PROPOSED_LABELS[status])
    if status == "applied" and "not applied" in proposed_label:
        raise ValueError("An applied proposal's label must not call it unapplied")
    rows = [
        (
            entry.get("current_label", "Current cached doc-note quotation"),
            entry["current"]["quote"],
            entry.get("current_explanation", ""),
            None,
        ),
        (proposed_label, proposed, entry.get("proposed_explanation", ""), None),
    ]
    if status == "applied":
        rows.append(applied_row(entry, sources))
    panels = []
    for label, quote, explanation, link in rows:
        panels.append(
            '<div class="passage"><h4>'
            + escaped(label)
            + "</h4>"
            + (
                '<p class="source-link"><a href="'
                + escaped(link[0])
                + '">'
                + escaped(link[1])
                + "</a></p>"
                if link
                else ""
            )
            + '<div class="he" lang="he" dir="rtl">'
            + escaped(visible_wikitext(quote))
            + "</div>"
            + (
                '<p class="translation">' + prose(explanation) + "</p>"
                if explanation
                else ""
            )
            + "</div>"
        )
    return (
        '<div class="comparison adjudication">'
        + "".join(panels)
        + '</div><p><a href="'
        + escaped(entry["research_note"])
        + '">'
        + escaped(
            entry.get("research_label", "Ben’s adjudication and research context")
        )
        + "</a></p>"
    )


def word_comparison_table(comparison, sources):
    rows = []
    for row in comparison["rows"]:
        forms = []
        entries = row.get("forms")
        if entries is None:
            entries = [
                {"label": label, "passage": row[key]}
                for label, key in (
                    ("Introduction", "introduction"),
                    ("Doc-note", "doc_note"),
                )
            ]
        for entry in entries:
            label, form = entry["label"], entry["passage"]
            record = sources.resolve(form)
            tooltip = (
                ' title="' + escaped(entry["mark_name"]) + '"'
                if entry.get("mark_name")
                else ""
            )
            forms.append(
                '<div class="reading"><span class="reading-label">'
                + escaped(label)
                + '</span><span class="he" lang="he" dir="rtl"'
                + tooltip
                + ">"
                + escaped(form["text"])
                + "</span>"
                + (
                    '<a href="' + escaped(record["source_url"]) + '">Source</a>'
                    if row.get("link_sources")
                    else ""
                )
                + "</div>"
            )
        evidence = escaped(row.get("manuscript", ""))
        if row.get("evidence"):
            evidence = panel(row["evidence"], sources)
        if row.get("evidence_explanation"):
            evidence += "<p>" + prose(row["evidence_explanation"]) + "</p>"
        rows.append(
            '<tr><td class="word-pair">'
            + "".join(forms)
            + '</td><td class="verse">'
            + escaped(row["ref"])
            + "</td><td>"
            + evidence
            + "</td></tr>"
        )
    return (
        '<div class="membership"><table><caption>'
        + prose(comparison["caption"])
        + "</caption><thead><tr><th>Word in each source</th><th>Verse</th><th>"
        + escaped(comparison.get("evidence_heading", "Manuscript"))
        + "</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def card(case, sources):
    for key in ("title", "issue", "decision", "panels"):
        if not case.get(key):
            raise ValueError(f"Incomplete readable case {case.get('id')}: {key}")
    if "introduction_section" in case:
        raise ValueError(
            "Section links are now per passage; remove introduction_section"
        )
    passages = "".join(panel(p, sources) for p in case["panels"])
    membership = (
        membership_table(case["membership_comparison"], sources)
        if case.get("membership_comparison")
        else ""
    )
    forms = []
    words = (
        word_comparison_table(case["word_comparison"], sources)
        if case.get("word_comparison")
        else ""
    )
    for form in case.get("reading_forms", []):
        sources.resolve(form)
        if "gloss" in form:
            raise ValueError(
                "Reading displays must not carry lexical Scripture glosses"
            )
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
            + "</span>"
            + (
                '<span class="annotation">' + prose(form["annotation"]) + "</span>"
                if form.get("annotation")
                else ""
            )
            + "</div>"
        )
    adjudication = (
        adjudication_comparison(case, sources) if case.get("adjudication") else ""
    )
    history = case.get("revision_history")
    history_note = (
        "<p><strong>History.</strong> "
        + prose(history["summary"])
        + " "
        + "; ".join(
            '<a href="' + escaped(link["url"]) + '">' + prose(link["label"]) + "</a>"
            for link in history["links"]
        )
        + ".</p>"
        if history
        else ""
    )
    issue = ""
    if case.get("issue_number"):
        number = case["issue_number"]
        issue = f'<p><a href="https://github.com/bdenckla/MAM-basics/issues/{number}">Tracked in #{number}</a></p>'
    spin_offs = (
        "<p><strong>Spin-off issues.</strong> "
        + "; ".join(
            '<a href="' + escaped(item["url"]) + '">' + prose(item["label"]) + "</a>"
            for item in case.get("spin_off_issues", [])
        )
        + ".</p>"
        if case.get("spin_off_issues")
        else ""
    )
    return (
        f'<details class="case" id="{escaped(case["id"])}"><summary><h3>{prose(case["title"])}</h3></summary><article>'
        + '<div class="explanation"><p><strong>'
        + prose(case["issue"])
        + "</strong> "
        + prose(
            " ".join(
                case.get(key, "")
                for key in ("context", "explanation", "decision")
                if case.get(key)
            ),
            case.get("prose_quotes", ()),
        )
        + "</p></div>"
        + history_note
        + spin_offs
        + membership
        + words
        + '<div class="comparison">'
        + passages
        + "</div>"
        + ('<div class="readings">' + "".join(forms) + "</div>" if forms else "")
        + adjudication
        + issue
        + "</article></details>"
    )


STYLE = """@font-face{font-family:Taamey;src:url(../../gh-pages/woff2/Taamey_D.woff2)}
:root{--he-size:30px;color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#f5f6f4;color:#22332d;font:17px/1.65 Georgia,serif}main{max-width:1220px;margin:auto;padding:28px}h1,h2,h3,h4,label,nav,.reading-label,.source-link{font-family:system-ui,sans-serif}h1{font-size:29px;line-height:1.3}h2{font-size:24px;margin:42px 0 15px}h3{font-size:21px;margin:0 0 12px}h4{font-size:15px;line-height:1.45;margin:0 0 12px;color:#4e645a}.intro{max-width:850px}.toolbar{position:sticky;top:0;background:#f5f6f4f5;border-bottom:1px solid #d5dfd9;padding:12px 0;z-index:2;display:flex;align-items:center;gap:10px;flex-wrap:wrap}.toolbar nav{margin-left:auto;font-size:14px}a{color:#1f5b85}nav a{margin-left:14px}article{background:white;border:1px solid #d7e0da;border-radius:8px;padding:25px;margin:22px 0;scroll-margin-top:85px}.issue{font-weight:bold;font-size:18px}.comparison{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin:22px 0}.passage{border-left:3px solid #bdcfc2;background:#f6f8f5;padding:16px 18px;min-width:0}.he{font:var(--he-size)/1.9 Taamey,'SBL Hebrew',serif;font-weight:400;white-space:pre-wrap;overflow-wrap:anywhere}.translation{font-size:16px;line-height:1.65;white-space:pre-wrap;margin-bottom:10px}.source-link{font-size:13px}.readings{display:flex;gap:20px;flex-wrap:wrap;border-top:1px solid #dce5de;border-bottom:1px solid #dce5de;padding:14px 0}.reading{display:flex;flex-direction:column;min-width:220px;flex:1}.reading-label,.gloss{font-size:14px}.reading .he{align-self:flex-start}.decision{background:#eef4f0;padding:12px 16px}footer{margin-top:40px;border-top:1px solid #d5dfd9;padding-top:20px;font-size:15px}input{vertical-align:middle}@media(max-width:760px){main{padding:16px}.comparison{grid-template-columns:1fr}.toolbar nav{margin-left:0}nav a{margin-left:0;margin-right:12px}article{padding:18px}}"""


THEME_STYLE = """
/* Match the shared document.css serif and light-dark pattern. */
:root{color-scheme:light dark;--review-bg:light-dark(white,black);--review-text:light-dark(black,white);--review-muted:light-dark(#555,#bbb);--review-border:light-dark(#bbb,#555);--review-panel:light-dark(#f6f6f6,#171717);--review-head:light-dark(#eee,#222)}
body{font-family:serif;font-size:14pt;color:var(--review-text);background:var(--review-bg)}
h1,h2,h3,h4,label,nav,.reading-label,.source-link{font-family:serif}
a{color:light-dark(#0000ee,#8ab4f8)}
.toolbar{background:var(--review-bg);border-color:var(--review-border)}
article,.case{background:var(--review-bg);border-color:var(--review-border)}
.case article,.passage,.readings,footer{border-color:var(--review-border)}
.passage,.decision{background:var(--review-panel)}
h4,.reading-label,.annotation{color:var(--review-muted)}
.membership table{width:auto;max-width:100%}
.membership th,.membership td{border-color:var(--review-border)}
.membership th{font-family:serif;background:var(--review-head)}
.membership .verse{font-family:serif}
"""


def reviewed_case_ids(cases):
    """Use recorded substantive Ben decisions, never presentation state."""
    records = {entry["id"]: entry for entry in read("adjudications.json")}
    reviewed = set()
    for case in cases:
        if not (record_id := case.get("adjudication")):
            continue
        entry = records[record_id]
        authority = entry["authority"]
        if (
            authority.get("person") == "Ben"
            and authority.get("kind") != "independently-verified-proposal"
            and "by-Ben" in entry["status"]
        ):
            reviewed.add(case["id"])
    return reviewed


def coverage_report(
    cases, literal_passages, proposed_quotations=0, applied_quotations=0
):
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
    reviewed = reviewed_case_ids(cases)
    return {
        "source_base_commit": audit.pinned_commit(),
        "purpose": "Presentation coverage and exact-quotation verification. User adjudications, proposals and their applications are recorded separately; rendering does not establish semantic consistency.",
        "readable_cases": len(cases),
        "sections": {
            key: sum(case["section"] == key for case in cases)
            for key in ("discrepancies", "questions", "scope", "tracked")
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
        "proposed_quotations_checked": proposed_quotations,
        "applied_quotations_checked": applied_quotations,
        "user_adjudicated_comparisons": len(reviewed),
        "reviewed_cases": [case["id"] for case in cases if case["id"] in reviewed],
        "unevaluated_cases": [
            case["id"] for case in cases if case["id"] not in reviewed
        ],
        "comparison_mapping": covered,
        "methods_only_or_resolved": methods,
        "limits": [
            "Exact substring validation does not establish manuscript truth or translation accuracy.",
            "Source reviewers and root reread translations and decisions; physical-source and quotation-scope questions remain explicit.",
            "Rendering reads the recorded snapshot, and for an applied proposal the later mirror commit that holds it, and writes research outputs only; it changes no source cache, scripture or published file.",
        ],
    }


def main(cases=None, output="review.html"):
    cases = cases if cases is not None else read("human-review.json")
    sources = Sources()
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate readable case IDs")
    reviewed = reviewed_case_ids(cases)
    statuses = [record["application_status"] for record in read("adjudications.json")]
    if unknown := set(statuses) - set(PROPOSED_LABELS):
        raise ValueError(f"Unknown application status: {unknown}")
    applied = statuses.count("applied")
    if applied == 0:
        applied_note = "no approved proposal is recorded as applied."
    elif applied == 1:
        applied_note = "one approved proposal is recorded as applied, with the Wikisource revision that applied it."
    else:
        applied_note = f"{applied} approved proposals are recorded as applied, each with the Wikisource revision that applied it."
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
            "scope",
            "Why these words are outside the list",
            "These words have a different vowel function or a different named source. The examples show the distinction.",
        ),
        (
            "tracked",
            "Already tracked",
            "These discrepancies are recorded in issues #305–307.",
        ),
    ):
        entries = [
            case
            for case in cases
            if case["section"] == key and case["id"] not in reviewed
        ]
        if entries:
            sections.append(
                f'<section id="{key}"><h2>{title}</h2><p>{lead}</p>'
                + "".join(card(case, sources) for case in entries)
                + "</section>"
            )
    if reviewed:
        sections.append(
            '<details class="reviewed" id="reviewed"><summary><h2>Reviewed ('
            + str(len(reviewed))
            + ")</h2></summary><p>These cases have recorded substantive Ben decisions. Any remaining questions stay with their cases.</p>"
            + "".join(card(case, sources) for case in cases if case["id"] in reviewed)
            + "</details>"
        )
    output_html = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MAM Introduction and doc-note discrepancies</title><style>'
        + STYLE
        + ".he-quote{display:inline-block;white-space:pre-wrap}.passage.full-width{grid-column:1/-1}.readings{display:grid;grid-template-columns:minmax(0,max-content)}.reading{min-width:0;flex:initial}.reading .he{align-self:stretch;text-align:right}.comparison.adjudication{grid-template-columns:1fr}.word-pair .reading+.reading{margin-top:12px}.word-pair .he{align-self:flex-end}"
        + ".case{background:white;border:1px solid #d7e0da;border-radius:8px;margin:18px 0;scroll-margin-top:85px}.case>summary{cursor:pointer;padding:20px 25px;list-style-position:outside;margin-left:20px}.case>summary h3{display:inline;margin:0}.case article{border:0;border-top:1px solid #d7e0da;border-radius:0;margin:0;padding-top:5px}bdi{unicode-bidi:isolate}.membership{overflow-x:auto;margin:24px 0}.membership table{width:100%;border-collapse:collapse}.membership caption{text-align:left;margin-bottom:12px}.membership th,.membership td{border:1px solid #d7e0da;padding:8px 12px;vertical-align:middle}.membership th{font:14px/1.5 system-ui,sans-serif;background:#f2f6f3}.membership .verse{white-space:nowrap;font:14px/1.5 system-ui,sans-serif}.annotation{font-size:14px}"
        + THEME_STYLE
        + ".reviewed{margin-top:42px;scroll-margin-top:85px}.reviewed>summary{cursor:pointer}.reviewed>summary h2{display:inline;margin:0}"
        + '</style></head><body><main><h1>MAM Introduction and doc-note discrepancies</h1><p class="intro">The comparison and question precede the quoted evidence. Explanatory Hebrew prose is translated; Scripture is retained in Hebrew.</p><div class="toolbar"><label for="size">Hebrew size <output id="value">30</output> px</label><input id="size" type="range" min="20" max="48" value="30" aria-label="Hebrew size"><nav><a href="#discrepancies">Discrepancies</a><a href="#questions">Questions</a><a href="#tracked">Tracked issues</a><a href="#reviewed">Reviewed</a></nav></div>'
        + "".join(sections)
        + "<footer><p>Ben’s approvals identify proposals for Avi’s review. The Reviewed cases that say “Tracked in” an issue have been submitted to him, and "
        + applied_note
        + '</p><a href="METHODS.md">Methods, evidence and coverage</a></footer></main><script>const slider=document.getElementById("size");slider.addEventListener("input",()=>{document.documentElement.style.setProperty("--he-size",slider.value+"px");document.getElementById("value").textContent=slider.value});</script></body></html>'
    )
    if output == "review.html":
        audit.dump(
            "human-review-coverage.json",
            coverage_report(
                cases,
                sources.checked,
                sources.proposals_checked,
                sources.applications_checked,
            ),
        )
    (audit.OUT / output).write_text(output_html, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "readable_cases": len(cases),
                "literal_passages_checked": sources.checked,
                "proposed_quotations_checked": sources.proposals_checked,
                "applied_quotations_checked": sources.applications_checked,
                "output": output,
            }
        )
    )
