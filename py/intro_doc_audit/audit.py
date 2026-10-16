"""Research joins, not a semantic consistency checker or a testing gate.

Captures stay literal. Matching keys alone use MAM's mark-order function.
The repository's closed note walk and visible-note renderer own doc-note parsing.
Introduction templates are not expanded: each transclusion remains visible evidence
and receives an explicit limitation. Missing notes never establish manuscript silence.
"""

import ctypes
import hashlib
import json
import os
import re
from collections import Counter
from functools import cache
from pathlib import Path
from urllib.parse import quote

import mwparserfromhell

from explicit_xataf import extract
from mb_cmn import bib_locales as bl
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import mam_bknas_and_std_bknas as bn
from mb_cmn import uni_denorm
from mb_cmn import verse_external_links as links
from sigils import inventory as sigils

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "doc/intro-doc-audit"
HEAD = re.compile(r"^(={2,6})(.*?)\1\s*$")
LETTERS = re.compile(r"[^\u05d0-\u05ea]")
FORMS = re.compile(
    r"(?<![א-ת])(?P<sigil>א(?:-כתיב|-קרי)?[?!*]*)=(?P<form>[^()\[\]{}=;:]+)"
)
WORD = re.compile(r"[\u0591-\u05ea\u034f\ufb1e]+(?:[ −-][\u0591-\u05ea\u034f\ufb1e]+)*")
HE_BOOKS = {bn.he_bk39_name(book): book for book in bl.ALL_BK39_IDS}


def dump(name, value):
    (OUT / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


@cache
def pinned_commit():
    return json.loads((OUT / "source-pin.json").read_text(encoding="utf-8"))[
        "base_commit"
    ]


def source_url(path, line=1):
    return f"https://github.com/bdenckla/MAM-basics/blob/{pinned_commit()}/{quote(path)}#L{line}"


def resolve_link(target):
    # Only explicit canonical Scripture paths; never guess from display labels.
    match = re.fullmatch(r"(.+) ([א-ת]+)/טעמים#([א-ת]+) ([א-ת]+)", target)
    if not match or match[1] not in HE_BOOKS:
        return None
    chapter = hvn.STR_TO_INT_DIC.get(match[2])
    anchor_chapter = hvn.STR_TO_INT_DIC.get(match[3])
    verse = hvn.STR_TO_INT_DIC.get(match[4])
    if chapter is None or verse is None or chapter != anchor_chapter:
        return None
    return [HE_BOOKS[match[1]], chapter, verse]


def ref_id(ref):
    return f"{ref[0]} {ref[1]}:{ref[2]}"


def inventory_intro():
    manifest = json.loads(
        (ROOT / "in/mam-ws-intro/manifest.json").read_text(encoding="utf-8")
    )
    topics, claims = [], []
    for key, metadata in manifest["pages"].items():
        path = f"in/mam-ws-intro/{key}.mediawiki"
        lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
        current = None
        hierarchy = []
        for n, line in enumerate(lines, 1):
            heading = HEAD.match(line)
            if heading or current is None:
                if current:
                    current["end_line"] = n - 1
                level = len(heading[1]) if heading else 1
                title = heading[2].strip() if heading else "Page preamble"
                hierarchy = [x for x in hierarchy if x[0] < level] + [(level, title)]
                current = {
                    "id": f"{key}:{n}",
                    "page": key,
                    "path": path,
                    "line": n,
                    "end_line": len(lines),
                    "heading": title,
                    "hierarchy": [x[1] for x in hierarchy],
                    "revision": metadata,
                    "source_url": source_url(path, n),
                    "claim_ids": [],
                }
                topics.append(current)
            if heading or not line.strip() or line.strip() in {"{|", "|}", "|-"}:
                continue
            code = mwparserfromhell.parse(line)
            wikilinks = []
            for link in code.filter_wikilinks():
                target = str(link.title).strip()
                wikilinks.append(
                    {
                        "target": target,
                        "label": str(link.text or link.title),
                        "ref": resolve_link(target),
                    }
                )
            refs = []
            for link in wikilinks:
                if link["ref"] and link["ref"] not in refs:
                    refs.append(link["ref"])
            transclusions = [
                str(t)
                for t in code.filter_templates()
                if str(t.name).strip().startswith("#קטע:")
            ]
            forms = []
            for m in FORMS.finditer(line):
                form = m["form"].strip().strip('"').strip("<>").strip()
                # A prose continuation after the form is not silently included.
                tokens = WORD.match(form)
                if tokens:
                    forms.append(
                        {
                            "sigil": m["sigil"],
                            "form": tokens[0],
                            "literal_expression": m[0],
                        }
                    )
            cid = f"{key}:L{n}"
            tags = []
            if refs:
                tags.append("explicit-verse-evidence")
            if forms:
                tags.append("Aleppo-form-claim")
            if line.lstrip().startswith(("#", "*", "|")):
                tags.append("enumeration-or-table")
            if transclusions:
                tags.append("unexpanded-transclusion")
            claims.append(
                {
                    "id": cid,
                    "topic": current["id"],
                    "path": path,
                    "line": n,
                    "text": line,
                    "source_url": source_url(path, n),
                    "links": wikilinks,
                    "refs": refs,
                    "forms": forms,
                    "tags": tags,
                    "transclusions": transclusions,
                    "coverage": (
                        "joined-evidence-needs-semantic-review"
                        if refs
                        else "topic-policy-history-or-implicit-evidence-needs-classification"
                    ),
                }
            )
            current["claim_ids"].append(cid)
    return topics, claims


def object_address(container, wanted):
    """Locate an already selected note object, without interpreting its fields."""
    if container is wanted:
        return ""
    items = (
        enumerate(container)
        if isinstance(container, list)
        else container.items() if isinstance(container, dict) else ()
    )
    for key, child in items:
        try:
            suffix = object_address(child, wanted)
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            return f"/{escaped}{suffix}"
        except LookupError:
            pass
    raise LookupError("Selected note not in source container")


def inventory_notes():
    notes, verses, inputs = [], {}, []
    revisions = json.loads(
        (ROOT / "in/mam-ws-revisions.json").read_text(encoding="utf-8")
    )["books"]
    for path in sorted((ROOT / "MAM-parsed/plus").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        positions = [
            m.start()
            for m in re.finditer(
                r'"tmpl_name": "נוסח"', path.read_text(encoding="utf-8")
            )
        ]
        text = path.read_text(encoding="utf-8")
        # Source addressing only: indentation is the generated JSON's hierarchy,
        # not a Scripture/annotation projection. Bind literal note occurrences to
        # their actual book/chapter/verse, excluding good-ending metadata copies.
        line_refs = {}
        book_index, source_chapter, source_verse = -1, None, None
        for number, source_line in enumerate(text.splitlines(), 1):
            if source_line.startswith('      "book24_name":'):
                book_index += 1
                source_chapter, source_verse = None, None
            if match := re.fullmatch(r'        "(\d+)": \{', source_line):
                source_chapter = match[1]
            if match := re.fullmatch(r'          "([^"\n]+)": \[', source_line):
                source_verse = match[1]
            if source_chapter is not None and source_verse is not None:
                source_book = data["book39s"][book_index]
                source_bkid = bn.MAM_HBNP_TO_BK39ID[
                    (source_book["book24_name"], source_book["sub_book_name"])
                ]
                line_refs[number] = f"{source_bkid} {source_chapter}:{source_verse}"
        decoder = json.JSONDecoder()
        source_records = []
        for position in positions:
            node, _ = decoder.raw_decode(text, text.rfind("{", 0, position))
            source_line = text.count("\n", 0, position) + 1
            source_records.append((node, source_line, line_refs.get(source_line)))
        used = set()
        inputs.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
        for book in data["book39s"]:
            bkid = bn.MAM_HBNP_TO_BK39ID[(book["book24_name"], book["sub_book_name"])]
            for chapter, chapter_data in book["chapters"].items():
                for verse, cells in chapter_data.items():
                    key = f"{bkid} {chapter}:{verse}"
                    note_ids = []
                    for cellno, cell in enumerate(cells):
                        for j, note in enumerate(extract.find_docnote_tmpls(cell)):
                            params = note["tmpl_params"]
                            nid = f"{key}/{cellno}/{j}"
                            locations = [
                                i
                                for i, (node, _, source_ref) in enumerate(
                                    source_records
                                )
                                if i not in used and node == note and source_ref == key
                            ]
                            if not locations:
                                raise ValueError(
                                    f"No literal source location for {nid}"
                                )
                            index = locations[0]
                            used.add(index)
                            line = source_records[index][1]
                            body = sigils._note_text(note)
                            try:
                                target_text = extract.flatten_text(params["1"])
                                target_projection_error = None
                            except ValueError as error:
                                if not str(error).startswith(
                                    "Unexpected template in flatten_text:"
                                ):
                                    raise
                                # Known dataset template without this survey's text projection.
                                # Retain the complete node, and do not invent visible Scripture.
                                target_text = None
                                target_projection_error = str(error)
                            notes.append(
                                {
                                    "id": nid,
                                    "ref": key,
                                    "path": path.relative_to(ROOT).as_posix(),
                                    "line": line,
                                    "json_pointer": f"/book39s/{data['book39s'].index(book)}/chapters/{chapter}/{verse}/{cellno}"
                                    + object_address(cell, note),
                                    "target_node": params["1"],
                                    "body_node": params["2"],
                                    "body_text": body,
                                    "target_survey_text": target_text,
                                    "target_projection_notice": "Existing hataf survey projection: qere and primary stress only; structural marks and whitespace may be omitted. Use target_node for evidence.",
                                    "target_projection_error": target_projection_error,
                                    "chapter_revision": revisions[bkid][
                                        hvn.INT_TO_STR_DIC[int(chapter)]
                                    ],
                                    "sigil_expressions": sigils._lhs_equals_expressions(
                                        body
                                    ),
                                    "implicit_MAM_agreement": sigils._leading_equals_expressions(
                                        body
                                    ),
                                    "source_url": source_url(
                                        path.relative_to(ROOT).as_posix(), line
                                    ),
                                }
                            )
                            note_ids.append(nid)
                    if verse not in ("0", "תתת"):
                        verses[key] = {"note_ids": note_ids}
        inputs[-1]["notes_outside_chapter_walk"] = [
            line for i, (_, line, _) in enumerate(source_records) if i not in used
        ]
        print(
            f"Read {path.name}: {len(used)} chapter notes; {len(source_records)-len(used)} outside chapter walk",
            flush=True,
        )
    return notes, verses, inputs


def build_matches(claims, notes, verses):
    by_id = {n["id"]: n for n in notes}
    candidates = []
    for claim in claims:
        evidence = []
        for ref in claim["refs"]:
            key = ref_id(ref)
            row = verses.get(key)
            evidence.append(
                {
                    "ref": key,
                    "verse_exists": row is not None,
                    "note_ids": row["note_ids"] if row else [],
                    "edition_link": links.mam_with_doc_url(*ref),
                    "chapter_link": links.wikisource_url(ref[0], ref[1]),
                }
            )
        claim["evidence"] = evidence
        # This is a triage heuristic, never a contradiction verdict.
        for form in claim["forms"]:
            matching_notes = []
            for item in evidence:
                for nid in item["note_ids"]:
                    note = by_id[nid]
                    literal = form["form"]
                    normalized = uni_denorm.give_std_mark_order(literal)
                    note_order = uni_denorm.give_std_mark_order(note["body_text"])
                    if literal in note["body_text"]:
                        kind = "literal-form-present-at-verse"
                    elif normalized in note_order:
                        kind = "mark-order-only-form-present-at-verse"
                    else:
                        kind = "form-not-found-at-verse"
                    if kind != "form-not-found-at-verse" or LETTERS.sub(
                        "", literal
                    ) in LETTERS.sub("", note["body_text"]):
                        matching_notes.append({"note_id": nid, "match": kind})
            candidates.append(
                {
                    "claim": claim["id"],
                    "form": form,
                    "matches": matching_notes,
                    "status": "unreviewed-literal-triage",
                }
            )
    return candidates


def main():
    if os.name == "nt":
        kernel = ctypes.windll.kernel32
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.SetPriorityClass.argtypes = (ctypes.c_void_p, ctypes.c_uint)
        if not kernel.SetPriorityClass(kernel.GetCurrentProcess(), 0x4000):
            raise ctypes.WinError()
    OUT.mkdir(parents=True, exist_ok=True)
    topics, claims = inventory_intro()
    notes, verses, inputs = inventory_notes()
    candidates = build_matches(claims, notes, verses)
    for topic in topics:
        subset = [c for c in claims if c["topic"] == topic["id"]]
        topic["counts"] = {
            "source_units": len(subset),
            "explicit_reference_units": sum(bool(c["refs"]) for c in subset),
            "form_claims": sum(len(c["forms"]) for c in subset),
        }
    dump("topics.json", topics)
    dump("claims.json", claims)
    dump("notes.json", notes)
    dump("form-triage.json", candidates)
    summary = {
        "pages": 13,
        "topics": len(topics),
        "source_units": len(claims),
        "doc_notes": len(notes),
        "canonical_verse_doc_notes": sum(n["ref"] in verses for n in notes),
        "paratext_doc_notes": sum(n["ref"] not in verses for n in notes),
        "verses": len(verses),
        "explicit_reference_units": sum(bool(c["refs"]) for c in claims),
        "reference_edges": sum(len(c["evidence"]) for c in claims),
        "edges_with_notes": sum(
            bool(e["note_ids"]) for c in claims for e in c["evidence"]
        ),
        "invalid_verse_edges": sum(
            not e["verse_exists"] for c in claims for e in c["evidence"]
        ),
        "Aleppo_form_triage": len(candidates),
        "form_triage": dict(
            Counter(m["match"] for c in candidates for m in c["matches"])
        ),
        "unexpanded_transclusion_units": sum(bool(c["transclusions"]) for c in claims),
        "input_files": inputs,
    }
    dump("summary.json", summary)
    print(
        json.dumps(
            {k: v for k, v in summary.items() if k != "input_files"},
            ensure_ascii=False,
            indent=2,
        )
    )
