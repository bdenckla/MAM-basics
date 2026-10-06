"""Validate the public presentation ledger for changed MAM notes.

Original source bodies and decisions remain in this ledger. Input hashes and a
pre-bake full-source inventory differential guard the published note content. Refresh
retains dispositions only for unchanged evidence. Unresolved presentations
keep explicit MAM context rather than speculating about a new subject.
"""

import copy
import hashlib
import json
from collections import Counter

from near_aleppo import build_paths
from near_aleppo import doc_figures
from near_aleppo import phase2_templates as phase2
from near_aleppo import phase3_policies as phase3
from near_aleppo import phase5_readings as phase5
from near_aleppo.editorial_ketiv import EditorialPointing
from near_aleppo.reviewed_ketiv import ReviewedPointing
from near_aleppo.frozen_ketiv import FrozenPointing, digest
from near_aleppo.phase6_mam_targets import MAM_TARGET_PARAMETER, _notes
from near_aleppo.phase6_rename import LEGACY_NOTES
from py_misc import unbury_doc_parts as unbury
from render_wt import doc_note_presentations as presentations

_ROOT = build_paths.dataset_dir().parents[2]
_LEDGER = _ROOT / "in/near-aleppo/doc-note-review.json"
_STAGES = (
    "template resolution",
    "representation policies",
    "note-derived readings",
    "frozen inferred pointing",
    "individual editorial pointing",
    "reviewed portable pointing",
)
_BODY = {"נוסח": "2", "מ:הערה-2": "2"}


def input_hashes():
    """Content identities, with portable keys rather than checkout-local paths."""
    paths = {}
    for name, directory in (("MAM-parsed-plus", build_paths.mam_parsed_plus_dir()),):
        books = sorted(directory.glob("*.json"))
        if len(books) != 24:
            raise AssertionError(f"{directory}: expected 24 books, found {len(books)}")
        paths.update({f"{name}/{p.name}": p for p in books})
    paths["aleppo/index-flat-annotated.json"] = build_paths.aleppo_index()
    for path in sorted((build_paths.input_dir()).rglob("*.json")):
        if path != _LEDGER:
            paths[path.relative_to(_ROOT).as_posix()] = path
    for name in (
        "phase2_templates.py",
        "phase3_policies.py",
        "phase5_readings.py",
        "frozen_ketiv.py",
        "editorial_ketiv.py",
        "reviewed_ketiv.py",
        "phase6_mam_targets.py",
    ):
        paths[f"py/near_aleppo/{name}"] = _ROOT / "py/near_aleppo" / name
    paths["py/py_misc/orphan_marks.py"] = _ROOT / "py/py_misc/orphan_marks.py"
    return {
        key: hashlib.sha256(path.read_bytes()).hexdigest()
        for key, path in paths.items()
    }


def _coverage(ref, index):
    name = doc_figures._INDEX_BOOK[ref[0]]
    ranks = {book: n for n, book in enumerate(index["header"]["books"])}
    if name not in ranks:
        return {"category": "missing", "pages": [], "partial_gap_boundaries": []}
    key = (ranks[name], int(ref[1]), int(ref[2]))
    pages, partial = [], []
    for row in index["body"]:
        if not row.get("de_text_range"):
            continue
        ends = [(ranks[b], int(c), int(v)) for b, c, v in row["de_text_range"]]
        if not ends[0] <= key <= ends[1]:
            continue
        pages.append(row["de_leaf"])
        gap = row.get("de_gap")
        sides = (gap,) if isinstance(gap, str) else tuple(gap or ())
        for side, position, whole_key in (
            ("Before", 0, "de_start_whole"),
            ("After", 1, "de_end_whole"),
        ):
            if (
                side in sides
                and key == ends[position]
                and row.get(whole_key) is not True
            ):
                partial.append(
                    {"page": row["de_leaf"], "side": side, "whole": row.get(whole_key)}
                )
    category = "uncertain" if partial else "surviving" if pages else "missing"
    return {"category": category, "pages": pages, "partial_gap_boundaries": partial}


def _parts(body):
    return unbury.unbury_parts([body if isinstance(body, list) else [body]])


def _candidate(note, target):
    """A proposal only: a complete literal alternative, never a semantic verdict."""
    if note["tmpl_name"] != "נוסח" or not isinstance(target, str) or not target.strip():
        return None, "Structured or whitespace target; preserve explicit MAM context."
    parts = _parts(note["tmpl_params"]["2"])
    found = []
    for number, part in enumerate(parts):
        if len(part) != 1 or not isinstance(part[0], str):
            continue
        head, equals, rest = part[0].partition("=")
        # Only a single leading, non-prose source relation. Bracketed source
        # qualifiers remain opaque; no claim is inferred from their spelling.
        if not equals or not head or " " in head or "=" in rest:
            continue
        if rest == target or rest.startswith(target + " "):
            found.append(number)
    if len(found) != 1:
        return (
            None,
            "No unique plain clause quoting the complete target; retain the source note.",
        )
    return (
        found[0],
        "One literal full-target alternative; semantic review of its suffix and other clauses required.",
    )


def _targets(cell, ref):
    return [copy.deepcopy(n["tmpl_params"]["1"]) for n in _notes(cell, ref)]


def _data_notes(value, ref, strip_added=False):
    """Phase 6's closed walk, retaining real dataset names and note objects."""
    found = []

    def walk(node):
        if isinstance(node, str):
            return
        if isinstance(node, list):
            for child in node:
                walk(child)
            return
        name = node["tmpl_name"]
        mam_name = {new: old for old, new in LEGACY_NOTES.items()}.get(name, name)
        rule = phase2._RULES.get(mam_name)
        if rule is None:
            raise AssertionError(f"{ref}: unknown template {name}")
        params = node.get("tmpl_params", {})
        if rule.action == phase2._KEEP_NOTE:
            found.append(node)
            if strip_added:
                node["tmpl_name"] = mam_name
                for key in (MAM_TARGET_PARAMETER, *phase2._FLAGS):
                    params.pop(key, None)
            walk(params["1"])
        elif rule.action == phase2._KEEP_KQ:
            if strip_added:
                for key in phase2._FLAGS:
                    params.pop(key, None)
            for key, child in params.items():
                if key not in phase2._FLAGS:
                    walk(child)
        elif rule.action not in (
            phase2._VERBATIM,
            phase2._COLLAPSE_WORD,
            phase2._CARRIERS,
        ):
            raise AssertionError(f"{ref}: unexpected unresolved template {name}")

    walk(value)
    return found


def inventory():
    """Replay the maintained build for exact per-note phase provenance."""
    # Replay the source build before note-content baking. Published files are
    # outputs of these decisions, never inputs to their provenance validation.
    from near_aleppo import main_build

    corpus = doc_figures._Corpus(main_build.build(bake_notes=False)[0])
    index = json.loads(build_paths.aleppo_index().read_text(encoding="utf-8"))
    resolver, policies, readings = (
        phase2.Resolver(),
        phase3.Policies(),
        phase5.Readings(),
    )
    frozen, editorial, reviewed = (
        FrozenPointing(build_paths.mam_parsed_plus_dir()),
        EditorialPointing(),
        ReviewedPointing(build_paths.mam_parsed_plus_dir()),
    )
    rows = []
    for verse in corpus.verses:
        ref = verse.ref
        original = _notes(verse.mam[2], ref)
        stages = [_targets(verse.mam[2], ref)]
        cell = resolver.resolve_e_cell(copy.deepcopy(verse.mam[2]), ref)
        stages.append(_targets(cell, ref))
        cell = policies.apply_e_cell(cell, ref)
        frozen.check_source(cell, ref)
        stages.append(_targets(cell, ref))
        cell = readings.apply_e_cell(cell, ref)
        stages.append(_targets(cell, ref))
        cell = frozen.apply(cell, ref)
        stages.append(_targets(cell, ref))
        cell = editorial.apply(cell, ref)
        stages.append(_targets(cell, ref))
        cell = reviewed.apply(cell, ref)
        stages.append(_targets(cell, ref))
        data_notes = _data_notes(verse.data[2], ref)
        compare_cell = copy.deepcopy(verse.data[2])
        _data_notes(compare_cell, ref, strip_added=True)
        final_targets = _targets(compare_cell, ref)
        if any(len(stage) != len(original) for stage in stages) or len(
            data_notes
        ) != len(original):
            raise AssertionError(f"{ref}: note identities changed during replay")
        for number, (source, data) in enumerate(zip(original, data_notes), 1):
            params, final = source["tmpl_params"], data["tmpl_params"]
            if stages[-1][number - 1] != final_targets[number - 1]:
                raise AssertionError(f"{ref}/{number}: replay differs from the dataset")
            if params["1"] == final["1"]:
                if MAM_TARGET_PARAMETER in final:
                    raise AssertionError(f"{ref}/{number}: unchanged note has MAM copy")
                continue
            body_key = _BODY[source["tmpl_name"]]
            if (
                final.get(MAM_TARGET_PARAMETER) != params["1"]
                or final[body_key] != params[body_key]
            ):
                raise AssertionError(f"{ref}/{number}: source body or MAM copy changed")
            clauses = phase3._clauses(params[body_key], ref)
            candidate, reason = _candidate(source, final["1"])
            causes = [
                _STAGES[i]
                for i in range(len(_STAGES))
                if stages[i][number - 1] != stages[i + 1][number - 1]
            ]
            row = {
                "id": f"{ref[0]} {ref[1]}:{ref[2]} note {number} {source['tmpl_name']}",
                "ref": list(ref),
                "note_ordinal": number,
                "source_template": source["tmpl_name"],
                "source_note_sha256": digest(source),
                "original_target": params["1"],
                "near_target": final["1"],
                "original_body": params[body_key],
                "clauses": clauses,
                "change_causes": causes,
                "coverage": _coverage(ref, index),
                "candidate_clause": candidate,
                "proposal_reason": reason,
            }
            row["evidence_sha256"] = digest(row)
            rows.append(row)
    frozen.finish()
    editorial.finish()
    reviewed.finish()
    return rows


def refresh():
    """Refresh inventory; preserve reviews only when every row's evidence agrees."""
    old = json.loads(_LEDGER.read_text(encoding="utf-8")) if _LEDGER.exists() else {}
    previous = {row["id"]: row for row in old.get("notes", [])}
    rows = inventory()
    for row in rows:
        prior = previous.get(row["id"], {})
        if prior.get("evidence_sha256") == row["evidence_sha256"]:
            row["review"] = prior["review"]
        else:
            row["review"] = {
                "status": "pending",
                "presentation": "framed-mam",
                "reason": "Shared correction; individual clause review pending.",
            }
    ledger = {
        "version": 1,
        "input_sha256": input_hashes(),
        "inventory_sha256": digest([r["evidence_sha256"] for r in rows]),
        "notes": rows,
    }
    _LEDGER.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"Inventoried {len(rows)} changed notes: {dict(Counter(r['coverage']['category'] for r in rows))}"
    )
    print(
        f"Literal recast proposals: {sum(r['candidate_clause'] is not None for r in rows)}"
    )


def load(require_reviewed=False):
    """Load current evidence, failing on moved inputs or an incomplete final review."""
    ledger = json.loads(_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("version") != 1 or ledger["input_sha256"] != input_hashes():
        raise AssertionError(
            "Doc-note review inputs changed; refresh and re-review affected notes."
        )
    ids = [row["id"] for row in ledger["notes"]]
    if not ids or len(ids) != len(set(ids)):
        raise AssertionError("Empty or duplicate doc-note inventory")
    if (
        digest([r["evidence_sha256"] for r in ledger["notes"]])
        != ledger["inventory_sha256"]
    ):
        raise AssertionError("Doc-note inventory lost or reordered evidence")
    for row in ledger["notes"]:
        evidence = {
            key: value
            for key, value in row.items()
            if key not in ("evidence_sha256", "review")
        }
        if digest(evidence) != row["evidence_sha256"]:
            raise AssertionError(f"{row['id']}: inventory evidence was edited")
        review = row["review"]
        if review["presentation"] not in ("framed-mam", "recast"):
            raise AssertionError(f"{row['id']}: unknown presentation")
        if review["status"] not in ("pending", "reviewed"):
            raise AssertionError(f"{row['id']}: unknown review state")
        if require_reviewed and review["status"] != "reviewed":
            raise AssertionError(f"{row['id']}: review is incomplete")
        if review["presentation"] == "recast" and row["candidate_clause"] is None:
            raise AssertionError(f"{row['id']}: recast without a literal candidate")
        if review["presentation"] == "recast" and review["status"] != "reviewed":
            raise AssertionError(f"{row['id']}: unreviewed recast")
        if review["status"] == "reviewed":
            _check_review(row)
    return ledger


def _sequence(value):
    return value if isinstance(value, list) else [value]


def _check_review(row):
    review = row["review"]
    parts = _parts(row["original_body"])
    near, remaining = None, parts
    promoted_index = None
    if review["presentation"] == "recast":
        promoted_index = row["candidate_clause"]
        near, remaining = presentations.project(
            parts, _sequence(row["near_target"]), promoted_index
        )
    if review["proposed_parts"] != {"near_clause": near, "mam_clauses": remaining}:
        raise AssertionError(f"{row['id']}: reviewed proposal differs from rendering")
    clauses = review["clauses"]
    if len(clauses) != len(parts) or not review.get("reason"):
        raise AssertionError(f"{row['id']}: incomplete review reasoning")
    for index, clause in enumerate(clauses):
        disposition = "near-subject" if index == promoted_index else "mam-context"
        if (
            clause["index"] != index
            or clause["disposition"] != disposition
            or not clause.get("reason")
        ):
            raise AssertionError(f"{row['id']}: inconsistent clause review")


def recipes(ledger):
    """Validate consistent historical review dispositions for identical inputs.

    This accounting runs during build validation; edition rendering never reads it.
    """
    result, dispositions = {}, {}
    for row in ledger["notes"]:
        target = _sequence(row["near_target"])
        parts = _parts(row["original_body"])
        key = presentations.signature(target, _sequence(row["original_target"]), parts)
        presentation = row["review"]["presentation"]
        disposition = presentation, (
            row["candidate_clause"] if presentation == "recast" else None
        )
        if key in dispositions and dispositions[key] != disposition:
            raise AssertionError(
                f"{row['id']}: conflicting presentations of identical inputs"
            )
        dispositions[key] = disposition
        if presentation == "recast":
            index = row["candidate_clause"]
            presentations.project(parts, target, index)
            result[key] = index
    return result


def check():
    """Independent full-build inventory differential and final clause accounting."""
    ledger = load(require_reviewed=True)
    expected = inventory()
    if [r["evidence_sha256"] for r in expected] != [
        r["evidence_sha256"] for r in ledger["notes"]
    ]:
        raise AssertionError(
            "Reviewed inventory differs from a fresh full-source enumeration"
        )
    recipes(ledger)
    print(
        f"All {len(expected)} changed notes agree with a fresh source enumeration and have clause reviews"
    )
    return ledger
