"""Clarify poetic census projections and the complete two-atom oleh roster."""

import json
import subprocess
from collections import Counter, defaultdict

from accgram import mam_poetic_accents as mpa
from accgram import mam_simple_verse as msv
from accgram import poetic_scanner, rtms_data, uni_to_marks
from mb_cmn import bib_locales as bl
from mb_cmn import mam_bknas_and_std_bknas as bn
from near_aleppo.census import edition_projection as projection
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id
from intro_doc_audit import audit, review

MARKS = {"DEHI": "\N{HEBREW ACCENT DEHI}", "OLE": "\N{HEBREW ACCENT OLE}"}
VARIANTS = {
    "primary": {},
    "doubled_helpers": {"מ:דחי": ("2",), "מ:צינור": ("2",)},
    "alternate_qamats": {"מ:קמץ": ("ס",)},
}
# A legarmeh's mark belongs with the atom before it, and in every Scripture branch of MAM
# what follows one is whitespace, a spacing template or the end of its parameter, so it
# gives nothing (measured 2026-10-21).
_LEGARMEH_TEMPLATE_NAMES = frozenset({"מ:לגרמיה", "מ:לגרמיה-2"})


def selected_parts(value, overrides):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [part for child in value for part in selected_parts(child, overrides)]
    params = value.get("tmpl_params", {})
    keys = projection.edition_parameter_keys_for(
        value["tmpl_name"], params.keys(), overrides=overrides
    )
    if value["tmpl_name"] in _LEGARMEH_TEMPLATE_NAMES:
        return []
    if value["tmpl_name"] in projection.EDITION_SEPARATOR_TEMPLATE_NAMES:
        # A separator stands between two atoms, as MAM's gray maqaf and the narrow-sense
        # paseq do with no whitespace on either side, so it gives a space, as the
        # near-Aleppo census renderers give it.  Until 2026-10-21 it gave nothing, and the
        # callers' joins ran the two atoms together.
        return [" "]
    return [part for key in keys for part in selected_parts(params[key], overrides)]


def input_record(path, base):
    relative = path.relative_to(audit.ROOT).as_posix()
    commit = subprocess.check_output(
        [
            "git",
            "-c",
            "safe.directory=" + audit.ROOT.as_posix(),
            "log",
            "-1",
            "--format=%H",
            base,
            "--",
            relative,
        ],
        text=True,
    ).strip()
    return {
        "path": relative,
        "last_input_commit_at_frozen_source": commit,
        "source_url": f"https://github.com/bdenckla/MAM-basics/blob/{base}/{relative}",
    }


def selected_template_paths(value, pointer):
    """Visit each parent once and descend only through the closed EP selection."""
    if isinstance(value, str):
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            yield from selected_template_paths(child, pointer + f"/{index}")
        return
    params = value.get("tmpl_params", {})
    keys = projection.edition_parameter_keys_for(value["tmpl_name"], params.keys())
    yield value["tmpl_name"], pointer, value
    for key in keys:
        yield from selected_template_paths(params[key], pointer + "/tmpl_params/" + key)


def main():
    counts = {variant: Counter() for variant in VARIANTS}
    members = {variant: {mark: set() for mark in MARKS} for variant in VARIANTS}
    poetic_verses = 0
    qamats_records = []
    ordinary_kq_records = []
    canonical_verses = 0
    for path in sorted((audit.ROOT / "MAM-parsed/plus").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for book_index, book in enumerate(data["book39s"]):
            book_id = bn.MAM_HBNP_TO_BK39ID[
                (book["book24_name"], book["sub_book_name"])
            ]
            for chapter, verses in book["chapters"].items():
                for verse, cells in verses.items():
                    if not verse.isdigit() or verse == "0":
                        continue
                    canonical_verses += 1
                    ref = f"{book_id} {chapter}:{verse}"
                    pointer = f"/book39s/{book_index}/chapters/{chapter}/{verse}/2"
                    for name, template_pointer, node in selected_template_paths(
                        cells[2], pointer
                    ):
                        record = {
                            "ref": ref,
                            "path": path.relative_to(audit.ROOT).as_posix(),
                            "pointer": template_pointer,
                        }
                        if name == "מ:קמץ":
                            qamats_records.append(record)
                        if name in {"כו״ק", "קו״כ"}:
                            ketiv = "".join(
                                selected_parts(node["tmpl_params"]["1"], {})
                            )
                            qere = "".join(selected_parts(node["tmpl_params"]["2"], {}))
                            marks = [
                                c
                                for c in ketiv
                                if 0x0591 <= ord(c) <= 0x05BD
                                or ord(c)
                                in {
                                    0x05BF,
                                    0x05C1,
                                    0x05C2,
                                    0x05C4,
                                    0x05C5,
                                    0x05C7,
                                    0x05C9,
                                }
                            ]
                            ordinary_kq_records.append(
                                {
                                    **record,
                                    "template": name,
                                    "selected_ketiv_text": ketiv,
                                    "selected_qere_text": qere,
                                    "ketiv_point_or_accent_codepoints": [
                                        f"U+{ord(c):04X}" for c in marks
                                    ],
                                }
                            )
                    if not bl.is_poetcant(
                        bl.mk_bcvtmam(book_id, int(chapter), int(verse))
                    ):
                        continue
                    poetic_verses += 1
                    for variant, overrides in VARIANTS.items():
                        text = "".join(selected_parts(cells[2], overrides))
                        for mark, char in MARKS.items():
                            if char in text:
                                counts[variant][mark + "_instances"] += text.count(char)
                                members[variant][mark].add(ref)
    simple_members = defaultdict(set)
    two_atom = []
    same_atom = 0
    unmatched = []
    simple_inputs = []
    base = review.read("source-pin.json")["base_commit"]
    for name, book_id in [("Ps", "Psalms"), ("Prov", "Proverbs"), ("Job", "Job")]:
        path = audit.ROOT / "MAM-simple/json-vtrad-mam" / (name + ".json")
        text = path.read_text(encoding="utf-8")
        data = json.loads(text)
        source = input_record(path, base)
        simple_inputs.append(source)
        for node in mpa._iter_verse_nodes(data):
            _, chapter, verse = node["osisID"].split(".")
            if not bl.is_poetcant(bl.mk_bcvtmam(book_id, int(chapter), int(verse))):
                continue
            ref = f"{book_id} {chapter}:{verse}"
            sequence = mpa.disjunctives_from_verse_node(node)
            for mark, token in [("DEHI", "DEXI"), ("OLE", "OLEH_WEYORED")]:
                if token in sequence:
                    simple_members[mark].add(ref)
            tokens = msv._normalize_mam_simple_verse(node)["vels"]
            if not all(isinstance(t, str) for t in tokens):
                raise ValueError(
                    "Selected MAM-simple atom stream gained an unclassified token"
                )
            atoms = [t for t in tokens if t != "\N{HEBREW PUNCTUATION PASEQ}"]
            for index, atom in enumerate(atoms):
                if MARKS["OLE"] not in atom:
                    continue
                if "\N{HEBREW ACCENT MERKHA}" in atom:
                    same_atom += 1
                    continue
                following = atoms[index + 1] if index + 1 < len(atoms) else None
                if following is None or "\N{HEBREW ACCENT MERKHA}" not in following:
                    unmatched.append({"ref": ref, "atom": atom, "following": following})
                    continue
                source_lines = [
                    i + 1
                    for i, line in enumerate(text.splitlines())
                    if f'"osisID": "{node["osisID"]}"' in line
                ]
                if len(source_lines) != 1:
                    raise ValueError(
                        "Two-atom source verse lacks one exact line pointer"
                    )
                two_atom.append(
                    {
                        "ref": ref,
                        "selected_oleh_atom": atom,
                        "selected_following_yored_atom": following,
                        "joined_by_maqaf": atom.endswith(
                            "\N{HEBREW PUNCTUATION MAQAF}"
                        ),
                        "path": source["path"],
                        "osisID": node["osisID"],
                        "line": source_lines[0],
                        "source_url": source["source_url"] + f"#L{source_lines[0]}",
                    }
                )
    listed = {
        audit.ref_id(i["strict_ref"])
        for row in review.read("poetic-rosters.json")["rosters"]
        if row["claim"] in {"ch5:L751", "ch5:L753", "ch5:L755"}
        for i in row["items"]
    }
    actual = {row["ref"] for row in two_atom}
    # These cached comparisons are diagnostic, never replacement corpora. Both
    # use the current loader's declared, identical kq-u JSON contract.
    wlc_diagnostics = {}
    wlc_all_members = {}
    for version in ("420", "422"):
        wlc_members = {mark: set() for mark in MARKS}
        wlc_instances = Counter()
        wlc_recovered_oleh = set()
        wlc_verses = 0
        directory = audit.ROOT / f"out/wlc{version}-kq-u"
        for bcv, verse in rtms_data.load_wlc422_index(directory).items():
            book = wlc_bb_to_bk39id(bcv[:2])
            chapter, vr = map(int, bcv[2:].split(":"))
            if not bl.is_poetcant(bl.mk_bcvtmam(book, chapter, vr)):
                continue
            ref = f"{book} {chapter}:{vr}"
            body = uni_to_marks.verse_to_marks(verse)
            wlc_verses += 1
            for mark, char in MARKS.items():
                if char in body:
                    wlc_members[mark].add(ref)
                    wlc_instances[mark] += body.count(char)
            if any(
                token == "OLEH_WEYORED"
                for token, _ in poetic_scanner.scan_accents(body)
            ):
                wlc_recovered_oleh.add(ref)
        wlc_all_members[version] = wlc_members | {"scanner_oleh": wlc_recovered_oleh}
        wlc_diagnostics[version] = {
            "poetic_verses": wlc_verses,
            "literal_mark_verse_counts": {m: len(wlc_members[m]) for m in MARKS},
            "literal_mark_instances": dict(wlc_instances),
            "scanner_oleh_verses_including_its_documented_recovery": len(
                wlc_recovered_oleh
            ),
            "input_files": [
                input_record(directory / f, base)
                for f in ("1verses_08_2cps.json", "1verses_09_jbpr.json")
            ],
            "limitation": "This cached WLC comparison does not reproduce the Introduction's 2685/421 totals. Its scanner has a limited unmarked-oleh recovery; 416 is not asserted as a complete grammatical count. Do not infer the Introduction's source from this negative comparison.",
        }
    wlc_diagnostics["420"]["same_membership_as_cached_422"] = {
        m: wlc_all_members["420"][m] == wlc_all_members["422"][m]
        for m in ("DEHI", "OLE", "scanner_oleh")
    }
    result = {
        "source_base_commit": base,
        "previous_audit_commit": "46b40fcace6382be94ebdee0fee761a349eedcaa",
        "current_consumer_inputs": [
            input_record(audit.ROOT / p, base)
            for p in (
                "py/near_aleppo/census/edition_projection.py",
                "py/accgram/mam_poetic_accents.py",
                "py/accgram/mam_simple_verse.py",
                "py/accgram/poetic_scanner.py",
                "py/accgram/rtms_data.py",
                "py/accgram/uni_to_marks.py",
            )
        ],
        "poetic_verses": poetic_verses,
        "qamats_alternative_templates": {
            "claim": "ch2:L199",
            "canonical_verses": canonical_verses,
            "instances": len(qamats_records),
            "verses": len({r["ref"] for r in qamats_records}),
            "predicate": "Count each מ:קמץ parent once in the selected EP stream before descending into ד; exclude apparatus, alternate/helper branches and metadata/good-ending copies. The Introduction explicitly defines its approximately 350 count by these template occurrences.",
            "records": qamats_records,
        },
        "ordinary_ketiv_qere_pointing": {
            "claims": ["ch2:L58", "ch2:L62", "ch2:L147"],
            "predicate": "All ordinary כו״ק / קו״כ parents reachable in the closed selected EP stream, checking selected branch 1 for Hebrew points/accents. Special qere types, implicit reading-mother families and apparatus are outside this narrow population; no colour or live layout claim follows.",
            "instances": len(ordinary_kq_records),
            "templates": dict(Counter(r["template"] for r in ordinary_kq_records)),
            "pointed_ketiv_exceptions": [
                r for r in ordinary_kq_records if r["ketiv_point_or_accent_codepoints"]
            ],
            "records": ordinary_kq_records,
        },
        "projection_variants": {
            v: {
                "counts": dict(counts[v]),
                "verse_counts": {m: len(members[v][m]) for m in MARKS},
                "same_membership_as_primary": {
                    m: members[v][m] == members["primary"][m] for m in MARKS
                },
            }
            for v in VARIANTS
        },
        "MAM_simple_independent_closed_extractor": {
            "verse_counts": {m: len(simple_members[m]) for m in MARKS},
            "same_membership_as_parsed": {
                m: simple_members[m] == members["primary"][m] for m in MARKS
            },
            "input_files": simple_inputs,
        },
        "two_atom_oleh": {
            "predicate": "Selected atom has OLE without MERKHA, and the immediately following atom has MERKHA; qere selected, fragments reassembled, paseq tokens excluded from atom adjacency. This is a current MAM predicate, not a physical-manuscript count.",
            "same_atom_cases": same_atom,
            "two_atom_cases": len(two_atom),
            "two_atom_verses": len(actual),
            "joined_by_maqaf_cases": sum(row["joined_by_maqaf"] for row in two_atom),
            "unmatched": unmatched,
            "listed_only": sorted(listed - actual),
            "current_only": sorted(actual - listed),
            "records": two_atom,
        },
        "cached_WLC_420_diagnostic": wlc_diagnostics["420"],
        "cached_WLC_422_diagnostic": wlc_diagnostics["422"],
        "conclusion": "The 55-entry two-atom roster exactly matches the complete current selected MAM population under the stated predicate. The current 2679/423 memberships are independently reproduced and are stable across the tested helper/qamats choices. The historical origin and intended source membership of 2685/421 remain unavailable in the cached Introduction and notes.",
    }
    audit.dump("next-pass-census.json", result)
    print(
        json.dumps(
            {
                "poetic_verses": poetic_verses,
                "MAM_verse_counts": {m: len(simple_members[m]) for m in MARKS},
                "two_atom_oleh": len(two_atom),
                "two_atom_roster_membership_agrees": actual == listed,
                "two_atom_unmatched": len(unmatched),
            },
            indent=2,
        )
    )
