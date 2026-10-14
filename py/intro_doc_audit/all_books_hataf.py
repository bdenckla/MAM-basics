"""Enumerate all cached non-guttural vowel evidence before contextual review."""

from collections import Counter, defaultdict
import hashlib
import json
import subprocess
import mwparserfromhell

from accgram import mam_poetic_accents, mam_simple_verse
from explicit_xataf import extract
from mb_cmn import bib_locales as bl, mam_bknas_and_std_bknas as bn
from mb_cmn import hebrew_accents, kq_special_templates, template_names, uni_denorm
from mb_misc import osis_book_abbrevs
from intro_doc_audit import audit, census_scope, deuter_hataf_scope, review
from near_aleppo.census import edition_projection


def selected_text(value):
    """Use the closed edition choices while retaining word-separating boundaries."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(selected_text(v) for v in value)
    params = value.get("tmpl_params", {})
    keys = edition_projection.edition_parameter_keys_for(
        value["tmpl_name"], params.keys(), overrides={}
    )
    if (
        not keys
        and value["tmpl_name"] in edition_projection.EDITION_SEPARATOR_TEMPLATE_NAMES
    ):
        return " "
    return "".join(selected_text(params[k]) for k in keys)


def pin(path, base):
    relative = path.relative_to(audit.ROOT).as_posix()
    content = path.read_bytes()
    expected = subprocess.check_output(
        [
            "git",
            "-c",
            "safe.directory=" + audit.ROOT.as_posix(),
            "show",
            base + ":" + relative,
        ]
    )
    if content != expected:
        raise ValueError("Changed evidence input: " + relative)
    return {
        **census_scope.input_record(path, base),
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def parameter_words(node, pointer):
    for location, template in deuter_hataf_scope.templates(node, pointer):
        name = template["tmpl_name"]
        if (
            name in template_names.STD_KQ_TMPL_NAMES
            or kq_special_templates.is_special_kq_template_name(name)
            or name in {"קרי ולא כתיב", "כתיב ולא קרי", "מ:קו״כ-אם-2"}
        ):
            params = template["tmpl_params"]
            for key in ("1", "2", "3"):
                if key in params:
                    text = selected_text(params[key])
                    yield {
                        "pointer": location,
                        "template": name,
                        "parameter": key,
                        "text": text,
                        "words": deuter_hataf_scope.words(text),
                    }


def main():
    base = audit.pinned_commit()
    retained = review.read("notes.json")
    note_counter = Counter(
        (
            n["ref"],
            deuter_hataf_scope.signature(n["target_node"]),
            deuter_hataf_scope.signature(n["body_node"]),
        )
        for n in retained
    )
    discovered = Counter()
    books, body, markers, parameters, inputs, metadata = [], [], [], [], [], []
    for path in sorted((audit.ROOT / "MAM-parsed/plus").glob("*.json")):
        inputs.append(pin(path, base))
        data = json.loads(path.read_text(encoding="utf-8"))
        for book_index, book in enumerate(data["book39s"]):
            book_id = bn.MAM_HBNP_TO_BK39ID[book["book24_name"], book["sub_book_name"]]
            verse_count = 0
            for chapter, verses in book["chapters"].items():
                for verse, cells in verses.items():
                    ref = f"{book_id} {chapter}:{verse}"
                    for cell_index, cell in enumerate(cells):
                        for note in extract.find_docnote_tmpls(cell):
                            p = note["tmpl_params"]
                            discovered[
                                ref,
                                deuter_hataf_scope.signature(p["1"]),
                                deuter_hataf_scope.signature(p["2"]),
                            ] += 1
                        pointer = f"/book39s/{book_index}/chapters/{chapter}/{verse}/{cell_index}"
                        parameters.extend(
                            {
                                "ref": ref,
                                "path": path.relative_to(audit.ROOT).as_posix(),
                                **row,
                            }
                            for row in parameter_words(cell, pointer)
                        )
                    if not verse.isdigit() or verse == "0":
                        continue
                    verse_count += 1
                    pointer = f"/book39s/{book_index}/chapters/{chapter}/{verse}/2"
                    selected = selected_text(cells[2])
                    address = {
                        "ref": ref,
                        "path": path.relative_to(audit.ROOT).as_posix(),
                        "pointer": pointer,
                    }
                    body.extend(
                        {**address, **word}
                        for word in deuter_hataf_scope.words(selected)
                    )
                    markers.extend(
                        {**address, "word": m[0]}
                        for m in deuter_hataf_scope.WORD.finditer(selected)
                        if "\ufb1e" in m[0]
                    )
            books.append(
                {
                    "book": book_id,
                    "canonical_verses": verse_count,
                    "roster_group_hebrew": book["book24_name"],
                }
            )
            if book["good_ending_plus"] is not None:
                extra = book["good_ending_plus"]
                metadata.append(
                    {
                        "book": book_id,
                        "pointer": f"/book39s/{book_index}/good_ending_plus",
                        "path": path.relative_to(audit.ROOT).as_posix(),
                        "node": extra,
                        "note_copies": len(list(extract.find_docnote_tmpls(extra))),
                    }
                )
        print(
            json.dumps(
                {"file": path.name, "books_accounted": len(books)}, ensure_ascii=False
            ),
            flush=True,
        )
    if discovered != note_counter:
        raise ValueError(
            "Complete all-cell note inventory differs from retained evidence"
        )
    if set(b["book"] for b in books) != set(bl.ALL_BK39_IDS):
        raise ValueError("Canonical book inventory is incomplete")
    simple_hits, simple_books = [], Counter()
    osis_map = {v: k for k, v in osis_book_abbrevs.BOOK_ABBREVS.items()}
    for path in sorted((audit.ROOT / "MAM-simple/json-vtrad-mam").glob("*.json")):
        inputs.append(pin(path, base))
        data = json.loads(path.read_text(encoding="utf-8"))
        for node in mam_poetic_accents._iter_verse_nodes(data):
            osis, chapter, verse = node["osisID"].split(".")
            book_id = osis_map[osis]
            if book_id not in bl.ALL_BK39_IDS:
                raise ValueError("Unclassified OSIS name: " + osis)
            tokens = mam_simple_verse._normalize_mam_simple_verse(node)["vels"]
            if not all(isinstance(t, str) for t in tokens):
                raise ValueError(
                    "MAM-simple selected stream gained an unclassified token"
                )
            simple_books[book_id] += 1
            simple_hits.extend(
                {"ref": f"{book_id} {chapter}:{verse}", **w}
                for w in deuter_hataf_scope.words(" ".join(tokens))
            )
    plus_set = Counter((w["ref"], w["word"]) for w in body)
    simple_set = Counter((w["ref"], w["word"]) for w in simple_hits)
    if plus_set != simple_set:
        raise ValueError(
            "Independent body membership differs: "
            + str((plus_set - simple_set, simple_set - plus_set))
        )
    for book in books:
        if book["canonical_verses"] != simple_books[book["book"]]:
            raise ValueError("Independent verse coverage differs: " + book["book"])
    roster_rows = []
    for roster in review.read("hataf-rosters.json")["rosters"]:
        for item in roster["items"]:
            code = mwparserfromhell.parse(item["literal_specimen"])
            for template in code.filter_templates():
                if str(template.name) == "גלגל" and not template.params:
                    code.replace(template, hebrew_accents.YBY)
            projected = str(code)
            for word in deuter_hataf_scope.words(projected):
                roster_rows.append(
                    {
                        "claim": roster["claim"],
                        "item": item["id"],
                        "ref": audit.ref_id(item["reviewed_ref"]),
                        "literal_ref": item["strict_ref"],
                        "reviewed_ref": item["reviewed_ref"],
                        "specimen": item["literal_specimen"],
                        "comparison_projection": projected,
                        "prior_disposition": item["status"],
                        **word,
                    }
                )
    index = defaultdict(list)
    for row in roster_rows:
        index[row["ref"], row["unpointed_key"]].append(row["item"])
    candidates = []
    for note in retained:
        for word in deuter_hataf_scope.words(note["body_text"]):
            matching = index[note["ref"], word["unpointed_key"]]
            candidates.append(
                {
                    "id": f"{note['id']}@{word['offset']}",
                    "note_id": note["id"],
                    "ref": note["ref"],
                    "body": note["body_text"],
                    "pointer": note["json_pointer"],
                    "source_url": note["source_url"],
                    "chapter_revision": note["chapter_revision"],
                    "roster_matches": matching,
                    **word,
                }
            )
    for path in sorted((audit.ROOT / "in/mam-ws").glob("*.json")):
        inputs.append(pin(path, base))
    for path in [
        audit.ROOT / "in/mam-ws-intro" / (name + ".mediawiki")
        for name in ("ch2", "ch3", "ch5")
    ]:
        inputs.append(pin(path, base))
    result = {
        "source_base_commit": base,
        "inputs": inputs,
        "books": books,
        "canonical_books": len(books),
        "canonical_verses": sum(b["canonical_verses"] for b in books),
        "doc_notes_scanned": sum(discovered.values()),
        "metadata_repetitions": metadata,
        "independent_body_check": "Literal non-guttural vowel membership and every book’s verse count agree with MAM-simple",
        "body_candidates": body,
        "vocal_sheva_markers": markers,
        "ketiv_qere_parameters": parameters,
        "note_word_candidates": candidates,
        "roster_word_candidates": roster_rows,
        "unlisted_note_word_candidates": [
            c for c in candidates if not c["roster_matches"]
        ],
        "limits": [
            "A lexical join is candidate routing, not a manuscript/source or vowel-policy verdict.",
            "Every candidate must receive a contextual disposition; faithful captures retain exact codepoints.",
        ],
    }
    audit.dump("all-books-hataf-census.json", result)
    print(
        json.dumps(
            {
                "books": len(books),
                "verses": result["canonical_verses"],
                "notes": result["doc_notes_scanned"],
                "body_words": len(body),
                "note_word_candidates": len(candidates),
                "unlisted_note_words": len(result["unlisted_note_word_candidates"]),
                "roster_words": len(roster_rows),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
