"""Small documentation comparisons read from the actual two datasets.

Each lookup requires one complete span of chanted words. The source projection
uses the existing phase-2 resolver; final text uses the closed dataset walk.
Pins check the stated difference without normalizing or retyping Hebrew marks.
Note examples also verify the preserved original target and explicit clause roles.
"""

import json
from difflib import SequenceMatcher

from near_aleppo import build_paths
from near_aleppo import doc_figures
from near_aleppo.doc_html import code, he_display, he_name, verse_refs
from near_aleppo.doc_template_examples import _hebrew_clusters
from mb_misc import mb_html
from near_aleppo.phase2_templates import Resolver
from near_aleppo.phase3_policies import _clauses, _selected_text
from near_aleppo.phase6_mam_targets import MAM_TARGET_PARAMETER
from py_misc import near_aleppo_params as nap
from near_aleppo.phase6_rename import RENAMED_NOTES

_HOLAM = "\N{HEBREW POINT HOLAM}"
_SHEVA = "\N{HEBREW POINT SHEVA}"
_VARIKA = "\N{HEBREW POINT JUDEO-SPANISH VARIKA}"
_EXAMPLES = {
    "divine-name": (("C1-Isaiah", "1", "2"), "יהוה", "יהוה", _HOLAM, ""),
    "divine-title": (("C1-Isaiah", "3", "17"), "אדני", "אדני", _HOLAM, ""),
    "elohim": (
        ("C3-Ezekiel", "2", "4"),
        "יהוה",
        "יהוה",
        "\N{HEBREW POINT HATAF SEGOL}",
        _SHEVA,
    ),
    "revia": (
        ("D1-Psalms", "8", "7"),
        "כל",
        "כל",
        "\N{HEBREW ACCENT REVIA}",
        "",
    ),
    "ole": (
        ("D1-Psalms", "30", "12"),
        "לי",
        "לי",
        "\N{HEBREW ACCENT OLE}",
        "",
    ),
    "maqaf": (("D3-Job", "23", "5"), "מה־יאמר לי", "מה־יאמר־לי", " ", "־"),
    "hataf": (
        ("D1-Psalms", "40", "13"),
        "אפפו־עלי׀",
        "אפפו־עלי׀",
        _SHEVA + _VARIKA,
        "\N{HEBREW POINT HATAF PATAH}",
    ),
    "hataf-hiriq": (
        ("D1-Psalms", "14", "1"),
        "השחיתו",
        "השחיתו",
        _VARIKA,
        "\N{HEBREW POINT HIRIQ}",
    ),
}


def _cell(directory, ref):
    book, chapter, number = ref
    stem, _, sub = book.partition(" ")
    data = json.loads((directory / (stem + ".json")).read_text(encoding="utf-8"))
    books = [b for b in data["book39s"] if b["sub_book_name"] == (sub or None)]
    if len(books) != 1:
        raise AssertionError(f"{ref}: missing or repeated example book")
    return books[0]["chapters"][chapter][number][2]


def _spelling(text):
    return "".join(c for c in text if "א" <= c <= "ת" or c in " ־׀")


def _span(cell, ref, spelling, source=False):
    projected = (
        Resolver().resolve_e_cell(cell, ref)
        if source
        else doc_figures._with_mam_names(cell, ref)
    )
    words = _selected_text(projected, ref).split(" ")
    length = len(spelling.split(" "))
    matches = [
        " ".join(words[i : i + length]).removesuffix("\N{HEBREW PUNCTUATION SOF PASUQ}")
        for i in range(len(words) - length + 1)
        if _spelling(" ".join(words[i : i + length])) == spelling
    ]
    if len(matches) != 1:
        raise AssertionError(f"{ref}: missing or ambiguous example span {spelling!r}")
    return matches[0]


def _comparison(before, after, labels=("MAM", "near-Aleppo")):
    left, right = _hebrew_clusters(before), _hebrew_clusters(after)
    changed = (set(), set())
    for tag, start, end, new_start, new_end in SequenceMatcher(
        a=left, b=right, autojunk=False
    ).get_opcodes():
        if tag != "equal":
            changed[0].update(range(start, end))
            changed[1].update(range(new_start, new_end))
    rows = [
        mb_html.table_row(
            [
                mb_html.table_datum(label),
                mb_html.table_datum(
                    he_display(_highlighted(clusters, indices)), {"dir": "rtl"}
                ),
            ]
        )
        for label, clusters, indices in zip(labels, (left, right), changed)
    ]
    return mb_html.div(mb_html.table(rows), {"class": "table-wrap display-table"})


def _highlighted(clusters, indices):
    parts = []
    for index, cluster in enumerate(clusters):
        if index not in indices:
            parts.append(cluster)
            continue
        cls = "example-space" if cluster == " " else "example-difference"
        content = mb_html.raw_html("&#32;") if cluster == " " else cluster
        parts.append(mb_html.span(content, {"class": cls}))
    return parts


def comparison(name):
    ref, first, second, removed, added = _EXAMPLES[name]
    source = _cell(build_paths.mam_parsed_plus_dir(), ref)
    final = _cell(build_paths.dataset_dir(), ref)
    before = _span(source, ref, first, source=True)
    after = _span(final, ref, second)
    if before.count(removed) != 1 or before.replace(removed, added, 1) != after:
        raise AssertionError(f"{ref}: the example has a different policy result")
    if name == "maqaf":
        mam, near = _notes(ref, (first, second))
        if (
            mam["1"] != before
            or near["1"] != after
            or not any(
                clause.startswith(f"א=<{after}>") for clause in _clauses(mam["2"], ref)
            )
        ):
            raise AssertionError("Job example must use the first quoted Aleppo form")
    return [
        mb_html.para(["For example, at ", *verse_refs((ref,)), ":"]),
        _comparison(before, after),
    ]


def _notes(ref, target):
    results = []
    spellings = (target,) if isinstance(target, str) else target
    for directory, mode in (
        (build_paths.mam_parsed_plus_dir(), doc_figures._MAM),
        (build_paths.dataset_dir(), doc_figures._DATASET),
    ):
        cell = _cell(directory, ref)
        matches = [
            tmpl
            for _, tmpl in doc_figures._templates(cell, ref, mode)
            if tmpl["tmpl_name"] in ("נוסח", RENAMED_NOTES["נוסח"])
            and isinstance(tmpl["tmpl_params"]["1"], str)
            and _spelling(tmpl["tmpl_params"]["1"]) in spellings
        ]
        if len(matches) != 1:
            raise AssertionError(f"{ref}: missing or repeated example note")
        results.append(matches[0])
    mam, near = results
    first, second = mam["tmpl_params"], near["tmpl_params"]
    if first["1"] == second["1"] and first["2"] != second["2"]:
        raise AssertionError(f"{ref}: unchanged-target example note body changed")
    if first["1"] != second["1"] and (
        near["tmpl_name"] != RENAMED_NOTES["נוסח"]
        or second[MAM_TARGET_PARAMETER] != first["1"]
    ):
        raise AssertionError(f"{ref}: example lost its MAM target")
    return first, second


def flag_examples():
    applied_ref = ("C3-Ezekiel", "28", "22")
    mam, near = _notes(applied_ref, "בעשותי")
    flag = "applied-and-flagged"
    expected = f'א!={near["1"]} (חסרה נקודת החולם)'
    if near[flag] != expected or expected not in _clauses(mam["2"], applied_ref):
        raise AssertionError("Ezekiel flag must quote the original bang-marked clause")
    if mam["1"].replace(_HOLAM, "", 1) != near["1"]:
        raise AssertionError("Ezekiel example must differ only in its missing holam")
    held_ref = ('BC-Kings מל"א', "20", "29")
    held_mam, held = _notes(held_ref, "נכח־אלה")
    held_flag = "flagged-not-applied"
    clause = held[held_flag]
    quoted, close, _ = clause.removeprefix("א?=<").partition(">")
    if (
        not clause.startswith("א?=<")
        or not close
        or clause not in _clauses(held_mam["2"], held_ref)
        or held["1"] != held_mam["1"]
        or quoted == held["1"]
    ):
        raise AssertionError("Kings example must retain its target and doubtful clause")
    return [
        mb_html.para(
            [
                "At ",
                *verse_refs((applied_ref,)),
                ", one note reports a missing holam as a manifest error in Aleppo. "
                "Near-Aleppo takes that form, with ",
                code(flag),
                ". Parameter 1 has the near-Aleppo form; ",
                he_name(MAM_TARGET_PARAMETER),
                " has the MAM form:",
            ]
        ),
        _comparison(mam["1"], near["1"]),
        mb_html.para(
            "The flag value copies the original clause, including its exclamation "
            "mark. Parameter 2 already contains the reviewed agreement with "
            "near-Aleppo. The remaining original clauses are stored separately "
            "with MAM's target."
        ),
        mb_html.para(
            [
                "At ",
                *verse_refs((held_ref,)),
                ", the ",
                code(held_flag),
                " value copies a doubt-marked clause. Near-Aleppo retains the "
                "target's maqaf and meteg; the alternative has a space and merkha:",
            ]
        ),
        _comparison(
            held["1"], quoted, ("MAM and near-Aleppo", "Doubt-marked alternative")
        ),
        mb_html.para("The alternative remains unresolved and is not applied."),
    ]


def apparatus_example():
    ref = ("A5-Deuter", "32", "13")
    source = _cell(build_paths.mam_parsed_plus_dir(), ref)
    final = _cell(build_paths.dataset_dir(), ref)
    before = _span(source, ref, "על־במתי", source=True)
    after = _span(final, ref, "על־במותי")
    templates = [
        t
        for _, t in doc_figures._templates(source, ref, doc_figures._MAM)
        if t["tmpl_name"] == "קו״כ"
    ]
    if len(templates) != 1 or templates[0]["tmpl_params"]["1"] != "במותי":
        raise AssertionError("Deuteronomy example must identify the source ketiv")
    if any(
        t["tmpl_name"] == "קו״כ"
        for _, t in doc_figures._templates(final, ref, doc_figures._DATASET)
    ):
        raise AssertionError("Deuteronomy example must have no body-text qere template")
    notes = [
        tmpl["tmpl_params"]
        for _, tmpl in doc_figures._templates(final, ref, doc_figures._DATASET)
        if tmpl["tmpl_name"] == RENAMED_NOTES["נוסח"]
        and tmpl["tmpl_params"]["1"] == after
    ]
    if (
        len(notes) != 1
        or notes[0][MAM_TARGET_PARAMETER] != ["עַל־", templates[0]]
        or not any(
            clause.startswith(f"א=<{after}>")
            for clause in _clauses(notes[0][nap.MAM_NOTE], ref)
        )
    ):
        raise AssertionError("Deuteronomy example must quote its retained source note")
    return [
        mb_html.para(
            [
                "At ",
                *verse_refs((ref,)),
                ", MAM's ",
                he_name("קו״כ"),
                " has ketiv letters ",
                he_name(templates[0]["tmpl_params"]["1"]),
                " and the pointed qere below. Near-Aleppo has the note's quoted "
                "Aleppo form as plain text, under the recorded decision to treat "
                "this spelling note as evidence of no qere note:",
            ]
        ),
        _comparison(before, after, ("MAM's pointed qere", "near-Aleppo plain text")),
    ]
