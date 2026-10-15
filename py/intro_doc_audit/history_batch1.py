"""Rebuild the first four history records from retained research API captures.

Requires the local read-only API cache at the supplied path; makes no network calls.
The tracked source evidence retains the selected revision IDs and search traces.
"""

import json
import re
from pathlib import Path
import mwparserfromhell
from intro_doc_audit import audit, human_review
from intro_doc_audit.revision_history import diff_url, revision_url
from mb_cmn import hebrew_verse_numerals as hvn, uni_denorm


def main(cache_dir=".novc/proverbs-history-api"):
    cache = Path(cache_dir)
    cases = human_review.read("human-review.json")
    byid = {c["id"]: c for c in cases}
    notes = {n["id"]: n for n in human_review.read("notes.json")}
    retained = human_review.read("history-batch1-sources.json")
    trans = {
        r["case"]: {
            "before": {
                k: r["introduction_addition"][0][k]
                for k in ("revid", "parentid", "timestamp", "comment")
            },
            "after": {
                k: r["introduction_addition"][1][k]
                for k in ("revid", "parentid", "timestamp", "comment")
            },
            "search_trace": r["adaptive_search_trace"],
        }
        for r in retained["cases"]
    }

    def meta(key):
        return [
            r
            for p in sorted(cache.glob(key + "-metadata-*.json"))
            for r in json.loads(p.read_bytes())["query"]["pages"][0]["revisions"]
        ]

    def content(key):
        return {
            r["revid"]: r
            for p in sorted(cache.glob(key + "-content-*.json"))
            for pg in json.loads(p.read_bytes())["query"]["pages"]
            for r in pg.get("revisions", [])
        }

    def revision(rid):
        return json.loads((cache / f"revision-{rid}.json").read_bytes())["query"][
            "pages"
        ][0]["revisions"][0]

    def letters(s):
        return "".join(c for c in s if "\u05d0" <= c <= "\u05ea")

    def capture(r, kind, verse=None, needles=()):
        text = r["slots"]["main"]["content"]
        if verse:
            number = hvn.INT_TO_STR_DIC[verse]
            pattern = (
                r"<\u05e7\u05d8\u05e2 \u05d4\u05ea\u05d7\u05dc\u05d4="
                + number
                + r"/>(.*?)<\u05e7\u05d8\u05e2 \u05e1\u05d5\u05e3="
                + number
                + r"/>"
            )
            m = re.search(pattern, text, re.S)
            assert m, (r["revid"], verse)
            start = text[: m.start(1)].count("\n") + 1
            excerpts = [{"line": start, "text": m[1]}]
        else:
            excerpts = [
                {"line": i, "text": line}
                for i, line in enumerate(text.splitlines(), 1)
                if any(
                    uni_denorm.give_std_mark_order(needle)
                    in uni_denorm.give_std_mark_order(line)
                    for needle in needles
                )
            ]
        return {
            "kind": kind,
            **{k: r[k] for k in ["revid", "parentid", "timestamp", "comment"]},
            "url": revision_url(r["revid"]),
            "excerpts": excerpts,
        }

    records = []
    sources = []
    results = human_review.read("revision-history-results.json")
    for cid, key, nid, verse, added, imported in [
        ("numbers-yod-label", "numbers-9", "Numbers 9:7/2/0", 7, 2826807, 655590),
        ("deuteronomy-vav-label", "deuter-32", "Deuter 32:34/2/0", 34, 2835959, 655705),
    ]:
        c = byid[cid]
        rows = meta(key)
        rs = content(key)
        assert len(rs) == len(rows)
        wrong = c["panels"][2]["quote"]
        main = notes[nid]["target_node"]
        observations = []
        for m in rows:
            r = rs[m["revid"]]
            templates = [
                t
                for t in mwparserfromhell.parse(
                    r["slots"]["main"]["content"]
                ).filter_templates()
                if str(t.name).strip() == "\u05e0\u05d5\u05e1\u05d7"
                and t.has("1")
                and letters(str(t.get("1").value)) == letters(main)
            ]
            observations.append(
                {
                    "revid": r["revid"],
                    "timestamp": r["timestamp"],
                    "wrong_label_present": any(wrong in str(t) for t in templates),
                    "main_forms": [str(t.get("1").value) for t in templates],
                }
            )
        first = next(x for x in observations if x["wrong_label_present"])
        assert first["revid"] == added
        after = rs[added]
        before = rs[after["parentid"]]
        before_templates = [
            t
            for t in mwparserfromhell.parse(
                capture(before, "chapter", verse)["excerpts"][0]["text"]
            ).filter_templates()
            if str(t.name).strip() == "\u05e0\u05d5\u05e1\u05d7"
            and t.has("1")
            and letters(str(t.get("1").value)) == letters(main)
        ]
        after_templates = [
            t
            for t in mwparserfromhell.parse(
                capture(after, "chapter", verse)["excerpts"][0]["text"]
            ).filter_templates()
            if str(t.name).strip() == "\u05e0\u05d5\u05e1\u05d7"
            and t.has("1")
            and letters(str(t.get("1").value)) == letters(main)
        ]
        assert len(before_templates) == len(after_templates) == 1
        assert str(before_templates[0].get("1").value) == str(
            after_templates[0].get("1").value
        )
        assert wrong not in str(before_templates[0]) and wrong in str(
            after_templates[0]
        )
        tr = trans[cid]
        alt = c["panels"][3]["quote"].split("=")[1].split(" (")[0]
        intro = [
            capture(revision(tr[s]["revid"]), "Introduction", needles=(main, alt))
            for s in ["before", "after"]
        ]
        assert intro[1]["excerpts"]
        selected = [
            capture(rs[rid], "chapter", verse)
            for rid in [imported, before["revid"], after["revid"], rows[-1]["revid"]]
        ]
        sources.append(
            {
                "case": cid,
                "chapter_page": {"page_key": key, "visible_metadata": rows},
                "introduction_addition": intro,
                "chapter_sources": selected,
                "chapter_scan": observations,
                "adaptive_search_trace": tr["search_trace"],
            }
        )
        record = {
            "case": cid,
            "classification": "discrepancy-present-when-doc-note-description-added",
            "introduction_entry": tr["after"],
            "doc_note_description_added": {
                **{k: after[k] for k in ["revid", "parentid", "timestamp"]},
                "url": diff_url(before["revid"], after["revid"]),
            },
            "MAM_main_form_unchanged_at_label_addition": True,
            "chapter_contents_read": len(rs),
            "visible_chapter_revisions": len(rows),
            "result": "The incorrect letter name is present in the first revision adding this descriptive parenthetical; the selected MAM spelling is unchanged across that edit. A later spelling change did not make a once-correct label stale.",
            "limits": [
                "The adaptive Introduction search proves the adjacent observed entry, not absence of all earlier removed or differently phrased entries.",
                "The pre-2015 public chapter is an older imported WLC text; it is not assumed to be the MAM draft consulted for the Introduction.",
                "Ben’s existing approval is preserved; no source correction was submitted or applied.",
            ],
        }
        records.append(record)
        date = after["timestamp"][:10]
        c["revision_history"] = {
            "summary": f"The note’s incorrect letter-name parenthetical was added on {date}; the selected MAM spelling is identical immediately before and after that edit. It was wrong when added, rather than becoming stale after a later spelling change. The Introduction’s spelling contrast is already present in the dated entry linked below. Ben’s approved correction is unchanged.",
            "links": [
                {
                    "label": "Introduction entry",
                    "url": diff_url(tr["before"]["revid"], tr["after"]["revid"]),
                },
                {
                    "label": "Doc-note description added",
                    "url": record["doc_note_description_added"]["url"],
                },
            ],
        }
        print(
            "COMPILED",
            cid,
            len(rs),
            "/",
            len(rows),
            record["doc_note_description_added"],
        )

    cid = "PS-18-2-ATTRIBUTION"
    c = byid[cid]
    rows = meta("psalms-18")
    rs = content("psalms-18")
    assert len(rs) == len(rows) == 41
    tr = trans[cid]
    needle = c["panels"][0]["quote"].split("):")[0].lstrip("(")
    intro = [
        capture(revision(tr[s]["revid"]), "Introduction", needles=(needle,))
        for s in ["before", "after"]
    ]
    assert not intro[0]["excerpts"] and intro[1]["excerpts"]
    source_ids = [671398, 2707445, 2708061, 2964958, 2966768, rows[-1]["revid"]]
    sources.append(
        {
            "case": cid,
            "chapter_page": {"page_key": "psalms-18", "visible_metadata": rows},
            "introduction_addition": intro,
            "chapter_sources": [capture(rs[rid], "chapter", 2) for rid in source_ids],
            "chapter_contents_read": len(rs),
            "adaptive_search_trace": tr["search_trace"],
        }
    )
    record = {
        "case": cid,
        "classification": "insufficient-history-to-resolve-manuscript-attribution",
        "introduction_entry": tr["after"],
        "first_explanatory_note": {
            **{k: rs[2708061][k] for k in ["revid", "parentid", "timestamp"]},
            "url": diff_url(2707445, 2708061),
        },
        "explicit_consulted_manuscripts_added": {
            **{k: rs[2966768][k] for k in ["revid", "parentid", "timestamp"]},
            "url": diff_url(2964958, 2966768),
        },
        "chapter_contents_read": 41,
        "visible_chapter_revisions": 41,
        "result": "The explicit Aleppo attribution entered the Introduction on 2023-03-09, before the explanatory chapter note on 2023-03-10. The consulted-manuscript list entered the note in 2025. The surviving historical notes do not identify an Aleppo source for the missing section, and this chronology does not resolve the attribution or the vowel-function question.",
        "limits": [
            "No manuscript scan, prior transcript or lost-section source was consulted.",
            "A missing explanation in the visible chapter history does not prove that no external source or older draft informed the Introduction.",
            "The question remains open; no new Aleppo attribution or manuscript reading is inferred.",
        ],
    }
    records.append(record)
    c["revision_history"] = {
        "summary": "The explicit Aleppo attribution entered the Introduction on 9 March 2023, one day before the explanatory chapter note. The note’s consulted-manuscript list was added in December 2025. The dated notes do not identify an Aleppo source for this missing section; the chronology leaves that attribution and the vowel-function question unresolved.",
        "links": [
            {
                "label": "Introduction attribution added",
                "url": diff_url(tr["before"]["revid"], tr["after"]["revid"]),
            },
            {
                "label": "Explanatory note added",
                "url": record["first_explanatory_note"]["url"],
            },
            {
                "label": "Consulted manuscripts added",
                "url": record["explicit_consulted_manuscripts_added"]["url"],
            },
        ],
    }
    cid = "PS-1-3"
    c = byid[cid]
    rows = meta("psalms-1")
    rs = content("psalms-1")
    assert len(rs) == len(rows) == 16
    tr = trans[cid]
    needle = c["panels"][0]["quote"]
    key = uni_denorm.give_std_mark_order(needle)
    intro = [
        capture(revision(tr[s]["revid"]), "Introduction", needles=(needle,))
        for s in ["before", "after"]
    ]
    assert not intro[0]["excerpts"] and intro[1]["excerpts"]
    draft_id = next(r for r in retained["cases"] if r["case"] == "PS-1-3")[
        "linked_draft_at_writing"
    ]["revid"]
    draft = revision(draft_id)
    draft_source = capture(draft, "linked MAM draft", needles=(needle,))
    assert draft_source["excerpts"]
    old = rs[904392]
    new = rs[998046]
    assert new["parentid"] == old["revid"]
    old_source = capture(old, "chapter", 3)
    new_source = capture(new, "chapter", 3)
    assert key in uni_denorm.give_std_mark_order(old_source["excerpts"][0]["text"])
    assert key not in uni_denorm.give_std_mark_order(new_source["excerpts"][0]["text"])
    gray = "{{\u05de:\u05de\u05e7\u05e3 \u05d0\u05e4\u05d5\u05e8}}"
    assert uni_denorm.give_std_mark_order(
        needle.replace(" ", gray, 1)
    ) in uni_denorm.give_std_mark_order(new_source["excerpts"][0]["text"])
    sources.append(
        {
            "case": cid,
            "chapter_page": {"page_key": "psalms-1", "visible_metadata": rows},
            "introduction_addition": intro,
            "linked_draft_at_writing": draft_source,
            "chapter_sources": [
                capture(rs[rid], "chapter", 3)
                for rid in [671381, 904392, 998046, rows[-1]["revid"]]
            ],
            "chapter_contents_read": 16,
            "adaptive_search_trace": tr["search_trace"],
        }
    )
    record = {
        "case": cid,
        "classification": "established-staleness",
        "introduction_entry": tr["after"],
        "matched_at_writing": {
            "draft_revision": draft["revid"],
            "timestamp": draft["timestamp"],
            "url": revision_url(draft["revid"]),
        },
        "chapter_change": {
            **{k: new[k] for k in ["revid", "parentid", "timestamp"]},
            "url": diff_url(old["revid"], new["revid"]),
        },
        "chapter_contents_read": 16,
        "visible_chapter_revisions": 16,
        "result": "The layout example was inserted with a space on 2013-05-30, matching the explicitly linked MAM draft revised nine minutes earlier. On 2020-11-10 the canonical MAM chapter acquired a grey maqaf at this boundary. The cached Introduction retains its older spaced form.",
        "limits": [
            "The linked draft was checked at the latest revision before insertion; its full history was not downloaded.",
            "The adjacent Introduction insertion and chapter change establish this sequence, without asserting no earlier deleted or differently phrased example.",
            "The manuscript example in the separate discussion has its own source role; the stale example verdict concerns the illustration of MAM layout.",
        ],
    }
    records.append(record)
    c["revision_history"] = {
        "summary": "The layout example was inserted on 30 May 2013 with a space, matching the linked MAM draft revised nine minutes earlier. The canonical MAM chapter acquired a grey maqaf at that boundary on 10 November 2020. The cached layout example retains the older MAM form; its separate occurrence as a manuscript quotation has a different role.",
        "links": [
            {
                "label": "Layout example inserted",
                "url": diff_url(tr["before"]["revid"], tr["after"]["revid"]),
            },
            {
                "label": "Linked MAM draft at writing",
                "url": revision_url(draft["revid"]),
            },
            {
                "label": "Grey maqaf added to MAM",
                "url": record["chapter_change"]["url"],
            },
        ],
    }
    audit.dump(
        "history-batch1-sources.json",
        {
            "source_base_commit": audit.pinned_commit(),
            "method": "Complete visible canonical chapter contents were read for the four compiled cases; exact selected verse and Introduction source excerpts retained here. Introduction contents were selected adaptively from enumerated metadata. The Psalm 1 linked draft was read at its latest revision before the example insertion.",
            "cases": sources,
        },
    )
    audit.dump(
        "history-batch1-results.json",
        {"source_base_commit": audit.pinned_commit(), "cases": records},
    )
    audit.dump("human-review.json", cases)
    done = {r["case"] for r in records}
    results["cases"] = [r for r in results["cases"] if r["case"] not in done] + [
        {
            "case": r["case"],
            "classification": r["classification"],
            "result": "history-batch1-results.json",
        }
        for r in records
    ]
    audit.dump("revision-history-results.json", results)
    print(
        "Compiled four source histories; existing case dispositions and quotations preserved."
    )
