"""Rebuild three independently reviewed histories from the local API captures."""

import mwparserfromhell

from intro_doc_audit import audit, human_review, rosters
from intro_doc_audit.history_evidence import (
    CachedHistory,
    capture,
    letters,
    verse_excerpt,
)
from intro_doc_audit.revision_history import diff_url, revision_url
from mb_cmn import ws_tmpl1
from ws import ws_tmpl_parser, ws_unparse


def physical_argument(template, index):
    # Older note calls use leading = and sigil= in physical pipe slots. The
    # generic MediaWiki named-parameter lookup does not identify these clauses.
    parsed = ws_tmpl_parser.parse(str(template))
    assert len(parsed) == 1
    return ws_unparse.unparse(ws_tmpl1.template_element(parsed[0], index))


def note_templates(revision, verse):
    text = verse_excerpt(revision["slots"]["main"]["content"], verse)["text"]
    return [
        t
        for t in mwparserfromhell.parse(text).filter_templates()
        if str(t.name).strip() == "\u05e0\u05d5\u05e1\u05d7"
    ]


def main(cache_dir=".novc/proverbs-history-api"):
    cache = CachedHistory(cache_dir)
    cases = human_review.read("human-review.json")
    byid = {c["id"]: c for c in cases}
    notes = {n["id"]: n for n in human_review.read("notes.json")}
    results, sources = [], []

    cid, key = "deuteronomy-leningrad-spelling", "deuter-6"
    chapter = cache.contents(key)
    before, after = chapter[2759383], chapter[2810192]
    wanted = letters(notes["Deuter 6:21/2/0"]["target_survey_text"])
    old = next(
        t
        for t in note_templates(before, 21)
        if t.has("1") and letters(str(t.get("1").value)) == wanted
    )
    new = next(
        t
        for t in note_templates(after, 21)
        if t.has("1") and letters(str(t.get("1").value)) == wanted
    )
    assert str(old.get("1").value) == str(new.get("1").value)
    assert not physical_argument(old, 2).startswith("=\u05dc,")
    assert physical_argument(new, 2).startswith("=\u05dc,\u05dc1,")
    assert "\u05dc!=" in str(new) and "\u05dc=" in str(old)
    intro = [
        capture(
            cache.revision(r),
            "Introduction",
            needles=(byid[cid]["panels"][0]["quote"],),
        )
        for r in (520551, 520558)
    ]
    assert not intro[0]["excerpts"] and intro[1]["excerpts"]
    sources.append(
        {
            "case": cid,
            "chapter_metadata": cache.metadata(key),
            "introduction": intro,
            "chapter_sources": [
                capture(chapter[r], "chapter", 21)
                for r in (655678, 2759383, 2810192, 2987745)
            ],
        }
    )
    results.append(
        {
            "case": cid,
            "classification": "discrepancy-present-when-doc-note-source-list-expanded",
            "chapter_contents_read": len(chapter),
            "visible_chapter_revisions": len(cache.metadata(key)),
            "introduction_entry": {
                "revid": 520558,
                "parentid": 520551,
                "timestamp": "2013-12-31T06:06:40Z",
            },
            "chapter_change": {
                "revid": 2810192,
                "parentid": 2759383,
                "timestamp": after["timestamp"],
                "url": diff_url(2759383, 2810192),
            },
            "result": "The 2023 list expansion adds bare Leningrad to agreement with the defective-vav main text, while retaining the same main form, the plene-vav alternative and the concluding plene-vav attribution to Leningrad. The original canonical MAM note agrees with the Introduction. This is a conflicting source-list entry when inserted, rather than established Introduction staleness.",
            "limits": [
                "The earlier draft history is not assessed; the 2011 public chapter predates the MAM import.",
                "The != operator means surprisingly equals; bare Leningrad, Firkovich B17 and the Leningrad Masorah reference remain distinct.",
            ],
        }
    )
    byid[cid]["revision_history"] = {
        "summary": "The Introduction’s spelling contrast is present in the adjacent 31 December 2013 entry, and the original canonical MAM note agrees with it. On 19 October 2023 the note’s expanded agreement list adds bare Leningrad while preserving its plene-vav alternative and concluding statement. The conflict is present in that list expansion; the selected spelling does not change. Ben’s approved correction remains unchanged.",
        "links": [
            {"label": "Introduction entry", "url": diff_url(520551, 520558)},
            {"label": "Conflicting list expansion", "url": diff_url(2759383, 2810192)},
        ],
    }

    cid, key = "ALL-HATAF-SONG-1-6", "song-1"
    chapter = cache.contents(key)
    old_intro, new_intro = cache.revision(2706335), cache.revision(2706336)
    before_lines, after_lines = (
        old_intro["slots"]["main"]["content"].splitlines(),
        new_intro["slots"]["main"]["content"].splitlines(),
    )
    marker = "\u05d7\u05d8\u05e4\u05d9\u05dd \u05d1\u05d0\u05d5\u05ea\u05d9\u05d5\u05ea \u05dc\u05d0-\u05d2\u05e8\u05d5\u05e0\u05d9\u05d5\u05ea \u05d1\u05e9\u05d9\u05e8 \u05d4\u05e9\u05d9\u05e8\u05d9\u05dd"
    assert not any(marker in line for line in before_lines)
    list_index = next(i for i, line in enumerate(after_lines) if marker in line)
    list_block = "\n".join(after_lines[list_index : list_index + 2])
    items = rosters.literal_items({"id": "2706336:Song-list", "text": list_block})
    assert [i["strict_ref"][1:] for i in items] == [
        [2, 7],
        [3, 2],
        [3, 3],
        [3, 5],
        [3, 6],
        [8, 2],
    ]
    main_key = letters(notes["Song of Songs 1:6/2/0"]["target_survey_text"])
    observed = []
    for meta in cache.metadata(key):
        r = chapter[meta["revid"]]
        matching = [
            t
            for t in note_templates(r, 6)
            if t.has("1") and letters(str(t.get("1").value)) == main_key
        ]
        observed.append(
            {"revid": r["revid"], "matching_notes": [str(t) for t in matching]}
        )
        if r["revid"] >= 671300:
            assert matching and all(
                "\N{HEBREW POINT HATAF SEGOL}" in str(t) for t in matching
            )
    new_list_source = capture(new_intro, "Introduction", needles=(marker,))
    new_list_source["excerpts"] = [{"line": list_index + 1, "text": list_block}]
    sources.append(
        {
            "case": cid,
            "chapter_metadata": cache.metadata(key),
            "chapter_observations": observed,
            "introduction": [
                capture(
                    old_intro,
                    "Introduction",
                    needles=(
                        "==\u05de\u05e1\u05d5\u05e8\u05ea \u05d4\u05e7\u05d5\u05e8\u05d0\u05d9\u05dd",
                    ),
                ),
                new_list_source,
            ],
            "new_list_refs": [i["strict_ref"] for i in items],
            "chapter_sources": [
                capture(chapter[r], "chapter", 6)
                for r in (671300, 2705674, 2705687, 2988376)
            ],
        }
    )
    results.append(
        {
            "case": cid,
            "classification": "omission-present-when-current-cross-manuscript-list-created",
            "chapter_contents_read": len(chapter),
            "visible_chapter_revisions": len(cache.metadata(key)),
            "introduction_list_added": {
                "revid": 2706336,
                "parentid": 2706335,
                "timestamp": new_intro["timestamp"],
                "url": diff_url(2706335, 2706336),
            },
            "earlier_note": {
                "revid": 671300,
                "timestamp": chapter[671300]["timestamp"],
            },
            "result": "The new six-item list omits Song 1:6 from its first revision, although the canonical MAM note has recorded Leningrad’s shin ḥataf segol since the 2016 import. Later operator and label edits do not add that vowel reading.",
            "limits": [
                "An earlier three-item list within the Aleppo-specific Song section has a narrower scope; its omission of Leningrad 1:6 is not used to establish the later list’s incompleteness.",
                "Historical mark order differs from the parsed form without changing its vowel. Ben’s approved addition is preserved.",
            ],
        }
    )
    byid[cid]["revision_history"] = {
        "summary": "The current six-item list was added on 1 March 2023 with Song 1:6 already absent. The chapter note has recorded Leningrad’s shin ḥataf segol since the 2016 MAM import; the 2023 operator and wording edits leave that reading unchanged. An older three-item Aleppo-specific list has a narrower scope. Ben’s approved addition remains unchanged.",
        "links": [
            {"label": "Six-item list added", "url": diff_url(2706335, 2706336)},
            {"label": "Earlier canonical MAM note", "url": diff_url(408473, 671300)},
            {
                "label": "Operator edit before list creation",
                "url": diff_url(1379872, 2705674),
            },
        ],
    }

    cid, key = "jeremiah-accent", "jeremiah-31"
    chapter = cache.contents(key)
    observations = []
    for meta in cache.metadata(key):
        r = chapter[meta["revid"]]
        matching = [
            t
            for t in note_templates(r, 37)
            if "\u05e7\u05e8\u05d9 \u05d5\u05dc\u05d0 \u05db\u05ea\u05d9\u05d1"
            in str(t)
        ]
        if matching:
            assert len(matching) == 1
            t = matching[0]
            assert "\N{HEBREW ACCENT ETNAHTA}" in str(t.get("1").value)
            assert "\N{HEBREW POINT METEG}" in str(t)
        observations.append(
            {"revid": r["revid"], "matching_notes": [str(t) for t in matching]}
        )
    assert sum(bool(o["matching_notes"]) for o in observations) == 25
    intro = capture(
        cache.revision(2698334),
        "Introduction",
        needles=(
            "\u05dc\u05d0/\u05d8\u05e2\u05de\u05d9\u05dd#\u05dc\u05d0 \u05dc\u05d6",
        ),
    )
    assert (
        intro["excerpts"]
        and "\N{HEBREW ACCENT ETNAHTA}" in intro["excerpts"][0]["text"]
    )
    sources.append(
        {
            "case": cid,
            "chapter_metadata": cache.metadata(key),
            "chapter_observations": observations,
            "introduction_observed_example": intro,
            "chapter_sources": [
                capture(chapter[r], "chapter", 37)
                for r in (407875, 658312, 2988015, 3088451)
            ],
            "formatting_edit_control": [
                capture(
                    cache.revision(r),
                    "Introduction",
                    needles=(
                        "\u05dc\u05d0/\u05d8\u05e2\u05de\u05d9\u05dd#\u05dc\u05d0 \u05dc\u05d6",
                    ),
                )
                for r in (2699150, 2699151)
            ],
        }
    )
    results.append(
        {
            "case": cid,
            "classification": "discrepancy-in-first-retained-canonical-MAM-note",
            "chapter_contents_read": len(chapter),
            "visible_chapter_revisions": len(cache.metadata(key)),
            "first_canonical_note": {
                "revid": 658312,
                "parentid": 407875,
                "timestamp": chapter[658312]["timestamp"],
                "url": diff_url(407875, 658312),
            },
            "recent_restoration": {
                "revid": 3088451,
                "parentid": 2988015,
                "timestamp": chapter[3088451]["timestamp"],
                "url": diff_url(2988015, 3088451),
            },
            "result": "The canonical MAM note already quotes U+05BD and ḥolam in its 2015 import, while selected body text has etnaḥta throughout all 25 MAM revisions. The 2026 restoration adds the missing ne’um atom but retains those marks. A cached Introduction example already has etnaḥta without holam by 3 February 2023. Later body-text changes do not explain the quotation error.",
            "limits": [
                "The earlier MAM draft origin and Ben’s copying hypothesis remain unestablished.",
                "2699151 only removes a space before the masorah circle; it is not the substantive example’s insertion.",
                "The historical comparison preserves Ben’s manuscript adjudication without independently repeating manuscript research.",
            ],
        }
    )
    byid[cid]["revision_history"] = {
        "summary": "The first canonical MAM note in November 2015 already has U+05BD and ḥolam, while selected body text has etnaḥta throughout the 25 MAM revisions. The October 2026 restoration adds the missing atom but retains those marks. The Introduction has its etnaḥta/no-ḥolam example by February 2023. The earlier draft origin and Ben’s copying hypothesis remain unestablished; the February spacing edit does not date the example’s creation.",
        "links": [
            {"label": "First canonical MAM note", "url": diff_url(407875, 658312)},
            {
                "label": "Introduction example by February 2023",
                "url": revision_url(2698334),
            },
            {"label": "Recent restoration", "url": diff_url(2988015, 3088451)},
        ],
    }

    cid = "SPELLING-SOURCE-JEREMIAH"
    selected = cache.selected("selected-history4")
    quote = byid[cid]["panels"][0]["quote"]
    intro = [
        capture(selected[r], "Introduction", needles=(quote,))
        for r in (2707401, 2707405)
    ]
    assert all(source["excerpts"] for source in intro)
    sources.append(
        {
            "case": cid,
            "shared_chapter_metadata": "jeremiah-accent",
            "introduction": intro,
            "chapter_sources": [
                capture(chapter[r], "chapter", 27)
                for r in (658312, 673934, 1289329, 3088451)
            ],
        }
    )
    results.append(
        {
            "case": cid,
            "classification": "insufficient-history-to-resolve-specific-Masorah-attribution",
            "shared_chapter_contents_read": 27,
            "introduction_observed_revisions": [2707401, 2707405, 3087756],
            "result": "The Introduction’s specific Masorah Parva attribution is unchanged in the observed March 2023 and pinned 2026 passages. All 25 MAM-note revisions name the Aleppo Masorah generally; they do not identify the particular short marginal note. The broader attribution is compatible with the narrower one, so no contradiction is demonstrated.",
            "support_gap": "Identify the Aleppo Masorah Parva note or list, or an explicit scholarly attribution. The note’s Breuer citation is a lead whose contents were not inspected in this cached-history task.",
            "limits": [
                "Selected Introduction snapshots establish observed stability, not the origin or continuous history of all 659 revisions.",
                "The spelling choice agrees; a general attribution does not disprove a more specific one.",
            ],
        }
    )
    byid[cid]["revision_history"] = {
        "summary": "The specific Masorah Parva wording is unchanged in the observed March 2023 and pinned 2026 Introduction passages. The 25 canonical MAM-note revisions name the Aleppo Masorah generally, with later discussion but no identified short marginal note. That broader attribution is compatible with the Introduction. The supporting Masorah Parva note or an explicit scholarly attribution still needs identification.",
        "links": [
            {"label": "Introduction in March 2023", "url": revision_url(2707401)},
            {"label": "Expanded chapter discussion", "url": diff_url(658312, 673934)},
            {"label": "Later clarification", "url": diff_url(1288226, 1289329)},
        ],
    }

    audit.dump(
        "history-batch2-sources.json",
        {
            "source_base_commit": audit.pinned_commit(),
            "method": "Independent semantic review followed by literal source-preserving checks. All 61 visible chapter contents across three chapters were read; Jeremiah 31 supports two separate cases. Exact selected excerpts and per-note observations retained here. Introduction snapshots do not imply exhaustive earlier-history coverage.",
            "cases": sources,
        },
    )
    audit.dump(
        "history-batch2-results.json",
        {"source_base_commit": audit.pinned_commit(), "cases": results},
    )
    audit.dump("human-review.json", cases)
    index = human_review.read("revision-history-results.json")
    completed = {r["case"] for r in results}
    index["cases"] = [r for r in index["cases"] if r["case"] not in completed] + [
        {
            "case": r["case"],
            "classification": r["classification"],
            "result": "history-batch2-results.json",
        }
        for r in results
    ]
    audit.dump("revision-history-results.json", index)
    print(
        {
            "compiled_cases": len(results),
            "chapter_contents": sum(r.get("chapter_contents_read", 0) for r in results),
        }
    )
