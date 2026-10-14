"""Independently reproduce the small concrete general-prose findings."""

import json
import re
from importlib.metadata import version

import mwparserfromhell
from mb_cmn import hebrew_verse_numerals as hvn

from intro_doc_audit import audit, census_scope, proofs, review

FRAGMENT_PAIRS = [
    ("ch4:L427", "ch5", "ch5:L280"),
    ("ch5:L294", "ch4", "ch4:L423"),
    ("index-aleppo:L11", "appendices", "appendices:L5"),
    ("index-leningrad:L693", "index-aleppo", "index-aleppo:L452"),
    ("data-sheet-guide:L37", "appendices", "appendices:L339"),
    ("data-sheet-guide:L59", "appendices", "appendices:L339"),
]


def fragment_key(value):
    # MediaWiki space/underscore equivalence only; no Unicode normalization.
    return " ".join(value.replace("_", " ").split())


def declarations(page):
    path = audit.ROOT / "in/mam-ws-intro" / (page + ".mediawiki")
    text = path.read_text(encoding="utf-8")
    declared = {
        fragment_key(m[2].strip())
        for line in text.splitlines()
        if (m := audit.HEAD.match(line))
    }
    for template in mwparserfromhell.parse(text).filter_templates():
        if str(template.name) in {"עוגן", "עוגן בשורה"}:
            declared.update(fragment_key(str(p.value)) for p in template.params)
    return declared


def main():
    # This optional research command uses the already-installed local calendar
    # library; the inventory and other audit commands do not require it.
    from pyluach.dates import GregorianDate, HebrewDate

    claims = {c["id"]: c for c in review.read("claims.json")}
    wlc_path = "in/mam-ws-intro/westminster-typing.mediawiki"
    wlc_lines = (audit.ROOT / wlc_path).read_text(encoding="utf-8").splitlines()
    note_tables = []
    for title_line, total_line, first, last in [(6, 8, 12, 60), (66, 68, 71, 92)]:
        rows = [
            {
                "line": line,
                "literal": wlc_lines[line - 1],
                "count": int(wlc_lines[line - 1].split("\t")[-1]),
            }
            for line in range(first, last + 1)
            if "\t" in wlc_lines[line - 1]
            and wlc_lines[line - 1].split("\t")[-1].isdigit()
        ]
        stated = int(wlc_lines[total_line - 1].split()[0])
        note_tables.append(
            {
                "literal_version_heading": wlc_lines[title_line - 1],
                "heading_line": title_line,
                "stated_total": stated,
                "sum_of_numeric_category_counts": sum(r["count"] for r in rows),
                "matches_stated_total": sum(r["count"] for r in rows) == stated,
                "rows": rows,
            }
        )
    category_rows = []
    declared_books = []
    zero_books = []
    for line in range(1147, 1801):
        literal = wlc_lines[line - 1]
        if literal.startswith("Differences in "):
            declared_books.append(literal.removeprefix("Differences in "))
        if literal.startswith("No differences found in "):
            zero_books.append(
                literal.removeprefix("No differences found in ").removesuffix("!")
            )
        if m := re.fullmatch(r"([A-Za-z0-9 ]+)\t((?:\d+\t){6}\d+)", literal):
            category_rows.append(
                {
                    "book": m[1],
                    "line": line,
                    "literal": literal,
                    "counts": list(map(int, m[2].split("\t"))),
                }
            )
    if len(declared_books) != 39 or set(declared_books) != set(zero_books) | {
        r["book"] for r in category_rows
    }:
        raise ValueError(
            "Historical WLC summary does not account for its 39 declared books"
        )
    totals = [sum(r["counts"][index] for r in category_rows) for index in range(7)]
    old, new = wlc_lines[115].split("\t")[1:3]
    if (
        "\N{HEBREW POINT HOLAM}" not in old
        or "\N{HEBREW POINT HOLAM HASER FOR VAV}" not in new
    ):
        raise ValueError("Historical holam encoding example changed")
    wlc = {
        "framing_claims": [
            "westminster-typing:L3",
            "westminster-typing:L62",
            "westminster-typing:L98",
            "westminster-typing:L1146",
        ],
        "version_label_case": {
            "claim": "westminster-typing:L62",
            "labelled_version": "4.14",
            "quoted_version": "4.16",
            "quoted_heading_claim": "westminster-typing:L66",
            "literal_quoted_heading": wlc_lines[65],
            "verdict": "The Hebrew source label does not name the version in the quotation it introduces.",
        },
        "note_legend_arithmetic": note_tables,
        "holam_encoding_control": {
            "claim": "westminster-typing:L98",
            "source_line": 116,
            "literal_row": wlc_lines[115],
            "old_literal": old,
            "new_literal": new,
            "old_codepoints": proofs.codepoints(old),
            "new_codepoints": proofs.codepoints(new),
            "verdict": "The quoted change includes the claimed HOLAM to HOLAM HASER FOR VAV encoding example; no physical manuscript interpretation follows.",
        },
        "version_412_to_414_summary": {
            "claim": "westminster-typing:L1146",
            "declared_books": declared_books,
            "zero_difference_books": zero_books,
            "numeric_summary_rows": category_rows,
            "column_order": [
                "Verses",
                "GOs",
                "Vowels",
                "Accents",
                "Morphological divisions",
                "Notes",
                "Note values",
            ],
            "category_totals": totals,
            "boundary": "The quoted summary has 60 morphological-division counts, 50 accent counts and 16 vowel counts. These are category counters that may overlap; row filtering and the intended unit of most changes are not defined sufficiently to infer unique-change majority or historical manuscript accuracy. Matching historical machine-readable 4.12/4.14 inputs are unavailable; current 4.22 is a different source/version.",
        },
        "source_url": audit.source_url(wlc_path),
        "boundary": "Historical source versions are explicitly named in this page. Matching machine-readable legacy versions and physical source controls are unavailable here; current cached WLC 4.22 cannot certify those historical tables. The remaining 843 routed Hebrew table units are not individually semantically assessed.",
    }
    manifest = json.loads(
        (audit.ROOT / "in/mam-ws-intro/manifest.json").read_text(encoding="utf-8")
    )["pages"]
    fragments = []
    for cid, target_page, heading_id in FRAGMENT_PAIRS:
        claim = claims[cid]
        links = [
            str(link.title)
            for link in mwparserfromhell.parse(claim["text"]).filter_wikilinks()
            if str(link.title).split("#")[0] == manifest[target_page]["title"]
            and "#" in str(link.title)
        ]
        if len(links) != 1:
            raise ValueError(f"No exact selected fragment relation: {cid}")
        fragment = links[0].split("#", 1)[1]
        declared = declarations(target_page)
        heading_line = int(heading_id.split(":L")[1])
        target_path = f"in/mam-ws-intro/{target_page}.mediawiki"
        literal_heading = (
            (audit.ROOT / target_path)
            .read_text(encoding="utf-8")
            .splitlines()[heading_line - 1]
        )
        heading = audit.HEAD.fullmatch(literal_heading)[2].strip()
        if fragment_key(fragment) in declared or fragment_key(heading) not in declared:
            raise ValueError(f"Selected fragment difference changed: {cid}")
        fragments.append(
            {
                "claim": cid,
                "literal_link_title": links[0],
                "requested_fragment": fragment,
                "target_page": target_page,
                "target_revision": manifest[target_page]["revid"],
                "literal_target_heading": literal_heading,
                "target_heading_source_id": heading_id,
                "source_url": claim["source_url"],
                "target_heading_source_url": audit.source_url(
                    target_path, heading_line
                ),
                "status": "requested target absent from cached headings and explicit anchors; reviewed corresponding current heading supplied",
                "boundary": "No live rendering checked. Unexpanded transclusions and live template-generated aliases could affect site behaviour; this is a cached source-target mismatch.",
            }
        )
    chapter = claims["ch5:L55"]["text"]
    if "שלושת הסוגים הראשונים" not in chapter or "ארבעת המקומות" not in chapter:
        raise ValueError("Isaiah grouping wording changed")
    enumeration = {
        "claims": [
            "ch5:L47",
            "ch5:L48",
            "ch5:L49",
            "ch5:L50",
            "ch5:L51",
            "ch5:L53",
            "ch5:L55",
            "ch5:L56",
            "ch5:L57",
            "ch5:L58",
            "ch5:L59",
        ],
        "first_two_types": [1, 3],
        "third_type": 2,
        "first_two_case_total": 4,
        "first_three_case_total": 6,
        "last_three_case_range": [10, 11],
        "verdict": "The first-three/four phrase disagrees with the five-type enumeration and four following decisions; first-two gives the stated four.",
        "boundary": "Internal grouping wording only; the physical interpretations and Breuer population are not independently verified.",
    }
    date_text = claims["appendices:L476"]["text"]
    if "ז' טבת תשע\"ד (10.12.14)" not in date_text:
        raise ValueError("Historical paired-date source changed")
    greg = HebrewDate(5774, 10, 7).to_greg()
    heb = GregorianDate(2014, 12, 10).to_heb()
    if greg.to_heb() != HebrewDate(5774, 10, 7) or heb.to_greg() != GregorianDate(
        2014, 12, 10
    ):
        raise ValueError("Calendar round trip failed")
    date = {
        "claim": "appendices:L476",
        "literal_date_pair": "ז' טבת תשע\"ד (10.12.14)",
        "method": "Local pyluach Hebrew/Gregorian conversion, both round trips",
        "pyluach_version": version("pyluach"),
        "seven_Tevet_5774_Gregorian": f"{greg.year:04d}-{greg.month:02d}-{greg.day:02d}",
        "ten_December_2014_Hebrew": {
            "year": heb.year,
            "month_number_Nisan_is_one": heb.month,
            "day": heb.day,
        },
        "verdict": "The two written dates do not denote the same civil day.",
        "boundary": "The historical event date is unknown; no choice of corrected date is made.",
    }
    job = []
    revisions = json.loads(
        (audit.ROOT / "in/mam-ws-revisions.json").read_text(encoding="utf-8")
    )["books"]
    for ref in (["Job", 9, 10], ["Job", 10, 9]):
        context = review.context(ref)
        parsed_path = audit.ROOT / "MAM-parsed/plus/D3-Job.json"
        cells = json.loads(parsed_path.read_text(encoding="utf-8"))["book39s"][0][
            "chapters"
        ][str(ref[1])][str(ref[2])]
        selected = census_scope.selected_parts(cells[2], {})
        word_present = any(
            audit.LETTERS.sub("", word) == "ונפלאות"
            for part in selected
            for word in proofs.ATOMS.findall(part)
        )
        raw_present = any(
            audit.LETTERS.sub("", word) == "ונפלאות"
            for word in proofs.ATOMS.findall(context["wikitext"])
        )
        if word_present != raw_present:
            raise ValueError("Job raw/parsed reference control disagrees")
        job.append(
            {
                **context,
                "chapter_revision": revisions["Job"][hvn.INT_TO_STR_DIC[ref[1]]],
                "parsed_path": parsed_path.relative_to(audit.ROOT).as_posix(),
                "parsed_pointer": f"/book39s/0/chapters/{ref[1]}/{ref[2]}/2",
                "complete_EP": cells[2],
                "selected_text_fragments": selected,
                "quoted_letters_present": word_present,
            }
        )
    if not job[0]["quoted_letters_present"] or job[1]["quoted_letters_present"]:
        raise ValueError("Job verse membership control changed")
    claim = claims["ch1:L258"]
    if (
        "באיוב י,ט" not in claim["text"]
        or "Job9:10-9:10" not in claim["text"]
        or "ct/c2709.htm" not in claim["text"]
    ):
        raise ValueError("Job footnote reference and external URL relations changed")
    result = {
        "author": "Codex",
        "date": "2026-10-14",
        "source_base_commit": audit.pinned_commit(),
        "fragment_cases": fragments,
        "fragment_case_count": len(fragments),
        "Isaiah_enumeration": enumeration,
        "historical_date_pair": date,
        "Job_prose_reference": {
            "claim": "ch1:L258",
            "wrong_ref": ["Job", 10, 9],
            "intended_ref": ["Job", 9, 10],
            "contexts": job,
            "source_url": claim["source_url"],
            "verdict": "The prose chapter/verse is reversed relative to the word, external paths and current cached verse membership.",
            "boundary": "Historical Westminster/Mechon Mamre forms and manuscript interpretation remain unverified; links were not fetched.",
        },
        "historical_WLC_framing": wlc,
    }
    audit.dump("next-pass-prose-findings.json", result)
    navigation = review.read("navigation-cases.json")
    if not any(c["claim"] == "ch1:L258" for c in navigation):
        navigation.append(
            {
                "claim": "ch1:L258",
                "wrong": ["Job", 10, 9],
                "intended": ["Job", 9, 10],
                "reason": "The prose reference reverses chapter/verse; the quoted word, two external paths and raw/parsed verse membership identify Job9:10. Historical source forms remain unverified.",
            }
        )
        audit.dump("navigation-cases.json", navigation)
    print(
        json.dumps(
            {
                "new_fragment_cases": len(fragments),
                "new_prose_verse_reference_case": 1,
                "grouping_wording_case": 1,
                "incompatible_date_pair_case": 1,
                "navigation_family_examples": len(navigation),
            },
            indent=2,
        )
    )
