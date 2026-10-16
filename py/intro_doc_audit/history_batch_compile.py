"""Compile manually reviewed history plans, retaining literal API source excerpts."""

import json
import re
from collections import defaultdict
from pathlib import Path

import mwparserfromhell

from intro_doc_audit import audit, human_review, snapshot
from intro_doc_audit.history_evidence import (
    CachedHistory,
    capture,
    letters,
    verse_excerpt,
)
from intro_doc_audit.revision_history import revision_url
from mb_cmn import hebrew_verse_numerals as hvn


class RevisionStore:
    """Index the separate research cache; never fetch or alter audit inputs."""

    def __init__(self, directory):
        self.cache = CachedHistory(directory)
        self.records = {}
        for path in Path(directory).glob("*.json"):
            if not (path.name.startswith("revision-") or "-content-" in path.name):
                continue
            for page in json.loads(path.read_bytes()).get("query", {}).get("pages", []):
                for revision in page.get("revisions", []):
                    rid = revision["revid"]
                    if rid in self.records:
                        assert (
                            self.records[rid]["slots"]["main"]["content"]
                            == revision["slots"]["main"]["content"]
                        )
                    self.records[rid] = revision

    def get(self, rid):
        return self.records[rid]


def intro_capture(revision, plan, claims):
    """Select by repository-resolved references or a source-derived list label."""
    wanted = {tuple(ref) for ref in plan.get("refs", [])}
    plain_labels = {
        hvn.INT_TO_STR_DIC[ref[1]] + "," + hvn.INT_TO_STR_DIC[ref[2]] for ref in wanted
    }
    label = None
    if plan.get("list_claim"):
        label = claims[plan["list_claim"]]["links"][0]["label"]
    lines = revision["slots"]["main"]["content"].splitlines()
    selected = {
        i - 1 for i in plan.get("line_numbers", {}).get(str(revision["revid"]), [])
    }
    if any(i < 0 or i >= len(lines) for i in selected):
        raise ValueError("Explicit historical source line is outside the revision")
    headings = {}
    for i, line in enumerate(lines):
        if line.startswith("=="):
            level = len(line) - len(line.lstrip("="))
            headings = {k: v for k, v in headings.items() if k < level}
            headings[level] = i
        found = label is not None and label in line
        found |= any(
            re.match(r"^[#*:;]+\s*" + re.escape(label) + r"[:\s]", line)
            for label in plain_labels
        )
        if wanted and "/\u05d8\u05e2\u05de\u05d9\u05dd#" in line:
            refs = {
                tuple(ref)
                for link in mwparserfromhell.parse(line).filter_wikilinks()
                if (ref := audit.resolve_link(str(link.title)))
            }
            found |= bool(wanted & refs)
        if found:
            selected.add(i)
            selected.update(headings.values())
        if (
            plan.get("scope_caption")
            and line.startswith("==")
            and (
                "\u05d7\u05d8\u05e4\u05d9\u05dd \u05d1\u05d0\u05d5\u05ea\u05d9\u05d5\u05ea"
                in line
            )
        ):
            selected.add(i)
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and not lines[j].startswith("="):
                selected.add(j)
    result = capture(revision, "Introduction")
    result["excerpts"] = [{"line": i + 1, "text": lines[i]} for i in sorted(selected)]
    if not result["excerpts"] and not plan.get("allow_absent"):
        raise ValueError(f"No historical Introduction excerpt at {revision['revid']}")
    return result


def chapter_states(chapter, verse, include_heading=False):
    """Group exact note templates without interpreting source sigils or mark meaning."""
    states = defaultdict(list)
    missing = []
    for rid, revision in chapter.items():
        try:
            text = verse_excerpt(
                revision["slots"]["main"]["content"], verse, include_heading
            )["text"]
        except ValueError:
            missing.append(rid)
            continue
        notes = tuple(
            str(template)
            for template in mwparserfromhell.parse(text).filter_templates()
            if str(template.name).strip() == "\u05e0\u05d5\u05e1\u05d7"
        )
        states[notes].append(rid)
    return {
        "verse": verse,
        **({"includes_verse_heading": True} if include_heading else {}),
        "literal_note_states": [
            {"revisions": sorted(ids), "templates": list(notes)}
            for notes, ids in states.items()
        ],
        "revisions_without_canonical_verse_delimiters": sorted(missing),
    }


def main(batch, cache_dir=".novc/proverbs-history-api"):
    """A successful compile checks provenance, not the correctness of a verdict."""
    plan = human_review.read(f"{batch}-plan.json")
    store = RevisionStore(cache_dir)
    cases = human_review.read("human-review.json")
    byid = {case["id"]: case for case in cases}
    claims = {claim["id"]: claim for claim in human_review.read("claims.json")}
    notes = {note["id"]: note for note in human_review.read("notes.json")}
    metadata, sources, results = {}, [], []
    unique_chapters = {}
    for record in plan["cases"]:
        cid = record["case"]
        assert cid in byid
        chapter_sources = []
        for specification in record.get("chapters", []):
            key = specification["key"]
            if key not in unique_chapters:
                unique_chapters[key] = store.cache.contents(key)
            chapter = unique_chapters[key]
            metadata[key] = store.cache.metadata(key)
            for rid in specification["selected"]:
                assert rid in chapter
            chapter_sources.append(
                {
                    "key": key,
                    "contents_read": len(chapter),
                    "visible_revisions": len(metadata[key]),
                    "states": [
                        chapter_states(
                            chapter, v, specification.get("include_heading", False)
                        )
                        for v in specification["verses"]
                    ],
                    "selected_sources": [
                        capture(
                            chapter[rid],
                            "chapter",
                            verse,
                            include_heading=specification.get("include_heading", False),
                        )
                        for rid in specification["selected"]
                        for verse in specification["verses"]
                    ],
                }
            )
        intro = [
            intro_capture(store.get(rid), record["intro"], claims)
            for rid in record["intro"]["revisions"]
        ]
        for claim_id in record.get("pinned_introduction_claims", []):
            claim = claims[claim_id]
            page_key = claim_id.split(":", 1)[0]
            manifest = snapshot.data("in/mam-ws-intro/manifest.json")["pages"][page_key]
            literal = snapshot.text(claim["path"]).splitlines()
            assert literal[claim["line"] - 1] == claim["text"]
            intro.append(
                {
                    "kind": "pinned Introduction cache",
                    "revid": manifest["revid"],
                    "timestamp": manifest["timestamp"],
                    "url": claim["source_url"],
                    "repository_path": claim["path"],
                    "excerpts": [{"line": claim["line"], "text": claim["text"]}],
                }
            )
        extra = [
            capture(store.get(s["revision"]), s["kind"], s["verse"])
            for s in record.get("extra_verses", [])
        ]
        for specification in record.get("extra_notes", []):
            revision = store.get(specification["revision"])
            key = letters(notes[specification["note"]]["target_survey_text"])
            text = revision["slots"]["main"]["content"]
            templates = [
                str(t)
                for t in mwparserfromhell.parse(text).filter_templates()
                if str(t.name).strip() == "\u05e0\u05d5\u05e1\u05d7"
                and t.has("1")
                and letters(str(t.get("1").value)) == key
            ]
            assert templates, (cid, specification)
            source = capture(revision, "linked draft", needles=templates)
            source["selected_templates"] = templates
            extra.append(source)
        for before, after in record.get("adjacent_pairs", []):
            assert store.get(after)["parentid"] == before, (cid, before, after)
        sources.append(
            {
                "case": cid,
                "chapters": chapter_sources,
                "introduction": intro,
                "extra_sources": extra,
                **(
                    {"introduction_correction": record["introduction_correction"]}
                    if "introduction_correction" in record
                    else {}
                ),
            }
        )
        links = [
            {
                "label": item["label"],
                "url": item.get("url") or revision_url(item["revision"]),
            }
            for item in record["links"]
        ]
        result = {
            "case": cid,
            "classification": record["classification"],
            "result": record["result"],
            "limits": record["limits"],
            "chapter_coverage": [
                {k: item[k] for k in ("key", "contents_read", "visible_revisions")}
                for item in chapter_sources
            ],
            "links": links,
        }
        results.append(result)
        byid[cid]["revision_history"] = {
            "summary": record.get("summary", record["result"]),
            "links": links,
        }
    audit.dump(
        f"{batch}-sources.json",
        {
            "source_base_commit": audit.pinned_commit(),
            "method": plan["method"],
            "chapter_metadata": metadata,
            "unique_chapter_contents_read": sum(map(len, unique_chapters.values())),
            "cases": sources,
        },
    )
    audit.dump(
        f"{batch}-results.json",
        {"source_base_commit": audit.pinned_commit(), "cases": results},
    )
    audit.dump("human-review.json", cases)
    index = human_review.read("revision-history-results.json")
    completed = {r["case"] for r in results}
    index["cases"] = [r for r in index["cases"] if r["case"] not in completed] + [
        {
            "case": r["case"],
            "classification": r["classification"],
            "result": f"{batch}-results.json",
        }
        for r in results
    ]
    audit.dump("revision-history-results.json", index)
    print(
        {
            "compiled_cases": len(results),
            "unique_chapter_contents": sum(map(len, unique_chapters.values())),
        }
    )
