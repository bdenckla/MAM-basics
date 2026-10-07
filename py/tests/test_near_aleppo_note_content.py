"""Differential note-content, Scripture and edition checks against sealed evidence."""

import ast
import copy
import json

from near_aleppo import (
    build_paths,
    doc_note_review,
    edition,
    frozen_ketiv,
    phase2_templates,
    main_build,
    reviewed_ketiv,
)
from near_aleppo.note_content import NoteContent
from near_aleppo.phase6_rename import LEGACY_NOTES, RENAMED_NOTES
from py_misc import near_aleppo_params as nap
from mb_cmn import bib_locales as tbn
from mb_cmn import read_books_from_mam_parsed_plus as plus
from render_wt import render_wikitext_kq

_BASELINE = "a9c45ee1ef1c2a4843cb2442840c074fac629d85"
_DATA = "out/near-aleppo/plus/"
_HTML = "gh-pages/near-aleppo/edition/"


def _names(prefix):
    output = edition._git("ls-tree", "-r", "-z", "--name-only", _BASELINE, prefix)
    names = [value.decode("utf-8") for value in output.split(b"\0") if value]
    assert names, f"Missing independent baseline {prefix}"
    return names


def _blobs(paths):
    request = "".join(f"{_BASELINE}:{path}\n" for path in paths).encode("utf-8")
    output = edition._git("cat-file", "--batch", input_bytes=request)
    position, result = 0, {}
    for path in paths:
        end = output.index(b"\n", position)
        header = output[position:end].split()
        assert len(header) == 3 and header[1] == b"blob", path
        size = int(header[2])
        result[path] = output[end + 1 : end + 1 + size]
        position = end + size + 2
    assert position == len(output)
    return result


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


def test_dataset_only_renderer_matches_prior_edition_from_the_same_baseline_inputs():
    paths = [
        path
        for path in _names(_HTML)
        if path.endswith(".html") and path != _HTML + "index.html"
    ]
    data_paths = _names(_DATA)
    review_path = "in/near-aleppo/doc-note-review.json"
    pointing_path = "in/near-aleppo/reviewed-pointed-ketiv.json"
    originals = _blobs([*paths, *data_paths, review_path, pointing_path])
    pointing_orders = _baseline_pointing_order_corrections(
        json.loads(originals[pointing_path])
    )
    ledger = json.loads(originals[review_path])
    for row in ledger["notes"]:
        assert row["review"]["status"] == "reviewed"
        doc_note_review._check_review(row)
    notes = NoteContent(ledger)
    books = {}
    for path in data_paths:
        book = json.loads(originals[path])
        for book39 in book["book39s"]:
            name = path.removeprefix(_DATA).removesuffix(".json")
            if book39["sub_book_name"]:
                name += " " + book39["sub_book_name"]
            for chapter, verses in book39["chapters"].items():
                for verse, cells in verses.items():
                    ref = name, chapter, verse
                    _upgrade_baseline_names(cells[2], ref)
                    for target_path, before, after in pointing_orders.get(ref, []):
                        params = frozen_ketiv.at_path(cells[2], target_path)[
                            "tmpl_params"
                        ]
                        assert params[nap.POINTED_KETIV] == before
                        params[nap.POINTED_KETIV] = after
                    notes.apply(cells[2], ref)
        books[path] = book
    notes.finish()
    books_mpu = plus.read_parsed_plus_bk39s(
        tbn.ALL_BK39_IDS,
        _DATA.removesuffix("/plus/"),
        load_json=books.__getitem__,
    )
    pages = edition.render(edition.NEAR_ALEPPO_MODE, books_mpu)
    assert {
        name for name in pages if name.endswith(".html") and name != "index.html"
    } == {path.removeprefix(_HTML) for path in paths}
    for path in paths:
        assert pages[path.removeprefix(_HTML)].encode("utf-8") == originals[path], path


def _baseline_pointing_order_corrections(baseline):
    """Apply approved source-order corrections to the historical replay input.

    The independent HTML oracle stays untouched. Only mark order may differ:
    source guards, site membership, letters and each letter's marks must agree.
    """
    previous = {row["id"]: row for row in baseline["records"]}
    current = {row["id"]: row for row in reviewed_ketiv.load()["records"]}
    assert set(previous) == set(current)
    corrections = {}
    for identity, row in current.items():
        prior = previous[identity]
        assert {k: v for k, v in prior.items() if k != "value"} == {
            k: v for k, v in row.items() if k != "value"
        }
        before, after = prior["value"], row["value"]
        if before != after:
            assert isinstance(before, str) and isinstance(after, str)
            assert render_wikitext_kq._cluster_inventory(
                before
            ) == render_wikitext_kq._cluster_inventory(after)
            corrections.setdefault(tuple(row["verse"]), []).append(
                (row["path"], before, after)
            )
    return corrections


def _upgrade_baseline_names(value, ref):
    """Adapt only sealed pre-bake names before the real content phase runs."""
    if isinstance(value, str):
        return
    if isinstance(value, list):
        for child in value:
            _upgrade_baseline_names(child, ref)
        return
    name = value["tmpl_name"]
    source = {legacy: original for original, legacy in LEGACY_NOTES.items()}.get(
        name, name
    )
    rule = phase2_templates._RULES.get(source)
    assert rule is not None, (ref, name)
    params = value.get("tmpl_params", {})
    if rule.action == phase2_templates._KEEP_NOTE:
        if name != source:
            value["tmpl_name"] = RENAMED_NOTES[source]
        _upgrade_baseline_names(params["1"], ref)
    elif rule.action == phase2_templates._KEEP_KQ:
        phase2_templates.selected_keys(value, ref)
        for key, child in params.items():
            if key not in phase2_templates._FLAGS:
                _upgrade_baseline_names(child, ref)
    else:
        assert rule.action in (
            phase2_templates._VERBATIM,
            phase2_templates._COLLAPSE_WORD,
            phase2_templates._CARRIERS,
        )


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
