"""Bound the Deuteronomy vocal-sheva roster against complete cached evidence."""

from collections import Counter, defaultdict
import json
import re
import subprocess

from accgram import mam_poetic_accents, mam_simple_verse
from explicit_xataf import extract
from mb_cmn import kq_special_templates, template_names, uni_denorm
from intro_doc_audit import audit, census_scope, next_pass, review, rosters

WORD = re.compile(
    r"[\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7\u05d0-\u05ea\u034f\ufb1e]+"
)
BASE = re.compile(r"[\u05d0-\u05ea]")


def words(text):
    """Count written words bearing the vowel; maqaf/space delimit words."""
    result = []
    for index, match in enumerate(WORD.finditer(text)):
        features = [h for h in rosters.hatafs(match[0]) if h["non_guttural"]]
        if features:
            result.append(
                {
                    "word": match[0],
                    "offset": match.start(),
                    "written_word_index": index,
                    "unpointed_key": "".join(BASE.findall(match[0])),
                    "features": features,
                }
            )
    return result


def signature(node):
    return json.dumps(node, ensure_ascii=False, sort_keys=True)


def templates(node, pointer):
    if isinstance(node, str):
        return
    if isinstance(node, list):
        for index, child in enumerate(node):
            yield from templates(child, pointer + f"/{index}")
        return
    params = template_names.validate_current_plus_template(node)
    yield pointer, node
    for key, value in params.items():
        yield from templates(value, pointer + "/tmpl_params/" + key)


def main():
    base = json.loads((audit.OUT / "source-pin.json").read_text(encoding="utf-8"))[
        "base_commit"
    ]
    paths = [
        "MAM-parsed/plus/A5-Deuter.json",
        "MAM-simple/json-vtrad-mam/Deut.json",
        "in/mam-ws/A5-Deuter.json",
        "in/mam-ws-intro/ch2.mediawiki",
        "in/mam-ws-intro/ch3.mediawiki",
    ]
    inputs = []
    for path in paths:
        pinned = subprocess.check_output(
            [
                "git",
                "-c",
                "safe.directory=" + audit.ROOT.as_posix(),
                "show",
                base + ":" + path,
            ]
        )
        if pinned != (audit.ROOT / path).read_bytes():
            raise ValueError("Input differs from the retained source snapshot: " + path)
        inputs.append(census_scope.input_record(audit.ROOT / path, base))
    claims = {
        c["id"]: c
        for c in json.loads((audit.OUT / "claims.json").read_text(encoding="utf-8"))
    }
    retained = [
        n
        for n in json.loads((audit.OUT / "notes.json").read_text(encoding="utf-8"))
        if n["ref"].startswith("Deuter ")
    ]
    notes_by_ref = defaultdict(list)
    for note in retained:
        notes_by_ref[note["ref"]].append(note)
    plus = json.loads((audit.ROOT / paths[0]).read_text(encoding="utf-8"))["book39s"][0]
    if plus["good_ending_plus"] is not None:
        raise ValueError("Deuteronomy gained noncanonical repeated-ending evidence")
    body, varika, kq, discovered = [], [], [], Counter()
    canonical = 0
    for chapter, verses in plus["chapters"].items():
        for verse, cells in verses.items():
            ref = f"Deuter {chapter}:{verse}"
            for cell in cells:
                for note_node in extract.find_docnote_tmpls(cell):
                    params = note_node["tmpl_params"]
                    discovered[ref, signature(params["1"]), signature(params["2"])] += 1
            if not verse.isdigit() or verse == "0":
                continue
            canonical += 1
            pointer = f"/book39s/0/chapters/{chapter}/{verse}/2"
            text = "".join(census_scope.selected_parts(cells[2], {}))
            body.extend({"ref": ref, "pointer": pointer, **w} for w in words(text))
            varika.extend(
                {"ref": ref, "pointer": pointer, "word": m[0]}
                for m in WORD.finditer(text)
                if "\ufb1e" in m[0]
            )
            for location, node in templates(cells[2], pointer):
                name = node["tmpl_name"]
                if (
                    name in template_names.STD_KQ_TMPL_NAMES
                    or kq_special_templates.is_special_kq_template_name(name)
                ):
                    params = node["tmpl_params"]
                    kq.append(
                        {
                            "ref": ref,
                            "pointer": location,
                            "template": name,
                            "ketiv_non_guttural_hataf": words(
                                "".join(census_scope.selected_parts(params["1"], {}))
                            ),
                            "qere_non_guttural_hataf": words(
                                "".join(census_scope.selected_parts(params["2"], {}))
                            ),
                        }
                    )
    archived = Counter(
        (n["ref"], signature(n["target_node"]), signature(n["body_node"]))
        for n in retained
    )
    if discovered != archived:
        raise ValueError(
            "Complete current note walk does not match retained note inputs"
        )
    simple = json.loads((audit.ROOT / paths[1]).read_text(encoding="utf-8"))
    simple_body = []
    simple_verses = 0
    for node in mam_poetic_accents._iter_verse_nodes(simple):
        _, chapter, verse = node["osisID"].split(".")
        simple_verses += 1
        tokens = mam_simple_verse._normalize_mam_simple_verse(node)["vels"]
        if not all(isinstance(t, str) for t in tokens):
            raise ValueError("MAM-simple gained an unclassified selected token")
        simple_body.extend(
            {"ref": f"Deuter {chapter}:{verse}", **w} for w in words(" ".join(tokens))
        )
    if [(w["ref"], w["word"]) for w in body] != [
        (w["ref"], w["word"]) for w in simple_body
    ]:
        raise ValueError(
            "Closed plus and independent MAM-simple vowel memberships differ"
        )
    candidates = []
    for note in retained:
        matches = words(note["body_text"])
        if matches:
            candidates.append(
                {
                    "note_id": note["id"],
                    "ref": note["ref"],
                    "body": note["body_text"],
                    "words": matches,
                    "raw_proof": next_pass.raw_note_proof(note),
                }
            )
    scope = {
        "Deuter 3:22/2/0": "uncertain: possible Leningrad ḥataf ḥiriq absent from the roster; the note explicitly allows the blurred sign to be meteg instead, and Dotan/Breuer print ḥiriq with gaʿya without comment",
        "Deuter 5:23/2/0": "in-scope: explicit Leningrad; uncertain Aleppo-photograph report also present",
        "Deuter 8:2/2/0": "in-scope: explicit Leningrad",
        "Deuter 8:15/2/0": "in-scope: explicit Leningrad with other named sources",
        "Deuter 15:20/2/0": "in-scope: explicit Leningrad with Cairo 18",
        "Deuter 15:22/2/0": "in-scope: explicit Leningrad with Cairo 18",
        "Deuter 24:13/2/2": "in-scope: explicit Leningrad with other named sources",
        "Deuter 28:39/2/0": "in-scope: explicit Aleppo",
        "Deuter 29:7/2/1": "in-scope: explicit Aleppo",
        "Deuter 32:10/2/0": "in-scope: explicit Aleppo, two distinct words",
        "Deuter 32:18/2/1": "in-scope: explicit Aleppo",
        "Deuter 32:36/2/0": "in-scope: explicit Aleppo; later Sassoon 1053/EVR-II-B-59 variant is the same word, not a second item",
        "Deuter 32:6/2/0": "excluded: non-guttural yod vowel attributed only to Firkovich B17, not Aleppo or Leningrad; Leningrad's he vowel is guttural",
        "Deuter 32:13/2/0": "excluded: retained morphological ḥataf qamats in the qere, rather than the optional vocal-sheva marking replaced by sheva in the stated policy; contextual classification under ch2:L276",
    }
    unknown = [c["note_id"] for c in candidates if c["note_id"] not in scope]
    if unknown:
        raise ValueError(
            "New non-guttural note candidates need semantic review: " + str(unknown)
        )
    for candidate in candidates:
        candidate["scope_disposition"] = scope[candidate["note_id"]]
    roster = []
    for item in rosters.literal_items(claims["ch3:L1134"]):
        ref = audit.ref_id(item["strict_ref"])
        for form in item["forms"]:
            for word in words(form["literal_form"]):
                bindings = []
                for candidate in candidates:
                    if candidate["ref"] == ref and candidate[
                        "scope_disposition"
                    ].startswith("in-scope"):
                        matches = [
                            w
                            for w in candidate["words"]
                            if w["unpointed_key"] == word["unpointed_key"]
                        ]
                        if matches:
                            for match in matches:
                                match["intro_relation"] = (
                                    "literal"
                                    if match["word"] == word["word"]
                                    else (
                                        "MAM-mark-order-only"
                                        if uni_denorm.give_std_mark_order(match["word"])
                                        == uni_denorm.give_std_mark_order(word["word"])
                                        else "distinct-pointing-or-spelling; requires reviewed source attribution"
                                    )
                                )
                            bindings.append(
                                {"note_id": candidate["note_id"], "note_words": matches}
                            )
                if len(bindings) != 1:
                    raise ValueError("Roster word lacks one reviewed note binding")
                roster.append(
                    {
                        "ref": ref,
                        "sigil": form["sigil"],
                        "intro_word": word,
                        "binding": bindings[0],
                    }
                )
    roster_keys = {(r["ref"], r["intro_word"]["unpointed_key"]) for r in roster}
    note_keys = {
        (c["ref"], w["unpointed_key"])
        for c in candidates
        if c["scope_disposition"].startswith("in-scope")
        for w in c["words"]
    }
    body_scope = {
        "Deuter 3:24": "Divine-name qere pointing, not an optional vocal-sheva vowel",
        "Deuter 9:26": "Divine-name qere pointing, not an optional vocal-sheva vowel",
        "Deuter 28:35": "Retained morphological ḥataf qamats; contextual classification under ch2:L276",
        "Deuter 32:13": "Retained morphological ḥataf qamats in the qere; contextual classification under ch2:L276",
    }
    for word in body:
        word["scope_disposition"] = body_scope[word["ref"]]
    result = {
        "source_base_commit": base,
        "inputs": inputs,
        "scope": "Optional non-guttural-letter ḥataf vowels marking vocal sheva in Aleppo or Leningrad, as distinguished from other manuscripts and retained morphological ḥataf vowels.",
        "scope_claims": [
            {
                "id": key,
                "text": claims[key]["text"],
                "source_url": claims[key]["source_url"],
            }
            for key in ("ch3:L1123", "ch2:L276", "ch2:L281")
        ],
        "word_definition": "One written word between space or maqaf bearing a relevant vowel; two words at 32:10 are separate, the unmarked prefix at 32:36 is not counted, and repeated source quotations of one word are one item.",
        "canonical_verses": canonical,
        "independent_simple_verses": simple_verses,
        "complete_notes_discovered_and_scanned": sum(discovered.values()),
        "note_candidates": candidates,
        "roster_words": roster,
        "roster_word_count": len(roster),
        "roster_verse_count": len({r["ref"] for r in roster}),
        "scoped_note_word_count": len(note_keys),
        "missing_from_roster": sorted(note_keys - roster_keys),
        "extra_in_roster": sorted(roster_keys - note_keys),
        "uncertainty_queue": [
            c for c in candidates if c["scope_disposition"].startswith("uncertain")
        ],
        "edition_body_non_guttural_hataf_words": body,
        "edition_vocal_sheva_marker_words": varika,
        "plain_sheva_controls": [
            {
                "ref": ref,
                "raw_verse": review.context(["Deuter", chapter, verse]),
                "selected_target_node": next(
                    n["target_node"] for n in retained if n["ref"] == ref
                ),
                "disposition": "Roster vowel replaced with sheva; no varika in the faithful raw target or independent edition projections",
            }
            for ref, chapter, verse in [
                ("Deuter 15:22", 15, 22),
                ("Deuter 32:10", 32, 10),
            ]
        ],
        "ketiv_qere_templates": kq,
        "limits": [
            "This is exhaustive within the complete cached edition/annotation evidence and the explicitly reviewed source scope; absence of an unrecorded manuscript occurrence is not established.",
            "Morphological classification of the retained 32:13 qere follows the stated policy context; no manuscript scan or new manuscript interpretation was undertaken.",
            "Original Hebrew strings are retained; raw-note matching uses existing MAM mark-order comparison only, without rewriting captures.",
        ],
    }
    audit.dump("deuter-hataf-scope.json", result)
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "canonical_verses",
                    "complete_notes_discovered_and_scanned",
                    "roster_word_count",
                    "roster_verse_count",
                    "scoped_note_word_count",
                    "missing_from_roster",
                    "extra_in_roster",
                )
            }
            | {
                "body_non_guttural_words": len(body),
                "varika_words": len(varika),
                "note_candidate_records": len(candidates),
            },
            ensure_ascii=False,
        )
    )
