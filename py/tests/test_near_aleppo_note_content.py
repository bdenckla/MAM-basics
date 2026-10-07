"""Check near-Aleppo's baked note content against its reviews, and that the
edition renderer depends on no review ledger or recipe."""

import ast
import copy
import json

from near_aleppo import (
    build_paths,
    doc_note_review,
    phase2_templates,
    main_build,
)
from near_aleppo.phase6_rename import LEGACY_NOTES, RENAMED_NOTES
from py_misc import near_aleppo_params as nap


def test_baked_clauses_match_reviews_and_preserve_current_pre_bake_book_content():
    ledger = doc_note_review.load(require_reviewed=True)
    rows = {(tuple(row["ref"]), row["note_ordinal"]): row for row in ledger["notes"]}
    seen = set()
    originals = main_build.build(bake_notes=False)[0]
    current_paths = sorted(build_paths.dataset_dir().glob("*.json"))
    assert {p.name for p in current_paths} == set(originals)
    for path in current_paths:
        current = json.loads(path.read_text(encoding="utf-8"))
        restored = copy.deepcopy(current)
        for book in restored["book39s"]:
            name = path.stem + (
                " " + book["sub_book_name"] if book["sub_book_name"] else ""
            )
            for chapter, verses in book["chapters"].items():
                for number, cells in verses.items():
                    ref = name, chapter, number
                    ordinal = 0

                    def walk(value):
                        nonlocal ordinal
                        if isinstance(value, str):
                            return
                        if isinstance(value, list):
                            for child in value:
                                walk(child)
                            return
                        name = value["tmpl_name"]
                        source = {new: old for old, new in RENAMED_NOTES.items()}.get(
                            name, name
                        )
                        rule = phase2_templates._RULES.get(source)
                        assert rule is not None, (ref, name)
                        params = value.get("tmpl_params", {})
                        if rule.action == phase2_templates._KEEP_NOTE:
                            ordinal += 1
                            identity = ref, ordinal
                            if name in RENAMED_NOTES.values():
                                nap.validate_baked_note(value)
                                row = rows[identity]
                                parts = row["review"]["proposed_parts"]
                                if parts["near_clause"] is None:
                                    assert params["2"] == []
                                    assert params[nap.MAM_NOTE] == row["original_body"]
                                else:
                                    assert doc_note_review._parts(params["2"]) == [
                                        parts["near_clause"]
                                    ]
                                stored_mam = (
                                    doc_note_review._parts(params[nap.MAM_NOTE])
                                    if params[nap.MAM_NOTE]
                                    else []
                                )
                                assert stored_mam == parts["mam_clauses"]
                                assert params[nap.MAM_TARGET] == row["original_target"]
                                assert identity not in seen
                                seen.add(identity)
                                params["2"] = row["original_body"]
                                del params[nap.MAM_NOTE]
                                value["tmpl_name"] = LEGACY_NOTES[source]
                            else:
                                assert identity not in rows
                            walk(params["1"])
                        elif rule.action == phase2_templates._KEEP_KQ:
                            phase2_templates.selected_keys(value, ref)
                            for key, child in params.items():
                                if key not in phase2_templates._FLAGS:
                                    walk(child)
                        else:
                            assert rule.action in (
                                phase2_templates._VERBATIM,
                                phase2_templates._COLLAPSE_WORD,
                                phase2_templates._CARRIERS,
                            )

                    walk(cells[2])
        original = json.loads(originals[path.name])
        assert restored["book39s"] == original["book39s"], path.name
        assert restored == original, path.name
    assert seen == set(rows)


def test_edition_renderer_has_no_review_ledger_or_recipe_dependency():
    root = build_paths.mam_basics_dir()
    paths = [
        root / "py/near_aleppo/edition.py",
        root / "py/py_misc/near_aleppo_params.py",
        root / "py/py_misc/scrdfftar_to_doc.py",
        root / "py/py_misc/trivial_qere_to_doc.py",
        *sorted((root / "py/render_wt").glob("render_wikitext*.py")),
    ]
    assert paths
    forbidden = (
        "doc_note_review",
        "doc_note_presentations",
        "doc-note-review.json",
        "ro_doc_note_recipes",
    )
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                text = (
                    (node.module or "")
                    + " "
                    + " ".join(name.name for name in node.names)
                )
            elif isinstance(node, ast.Import):
                text = " ".join(name.name for name in node.names)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                text = node.value
            else:
                continue
            assert not any(word in text for word in forbidden), (path, text)
