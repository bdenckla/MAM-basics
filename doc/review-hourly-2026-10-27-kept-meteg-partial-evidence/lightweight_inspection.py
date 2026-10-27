"""Inspect committed JSON/HTML and the README record; run no project generator/test."""

from collections import Counter
from datetime import datetime, timezone
from hashlib import sha1
import json
from pathlib import Path
import re
import subprocess
import time

from lxml import html

BASE = Path("/workspace/review-hourly-20261027-kept-meteg")
ROOT = BASE / "source"
SCRATCH = Path("/workspace/scratch/review-hourly-20261027-kept-meteg")
FONT_HOME = Path("/workspace/hbofonts")
OLD = "46f80ecc8b29fdd7f5fdf30c40bc2b3382bbb352"
NEW = "d0cc6752d9820d3038ae0f72c2886190ed431c6e"
DEHI = "\N{HEBREW ACCENT DEHI}"
TSINNOR = "\N{HEBREW ACCENT ZINOR}"
METEG = "\N{HEBREW POINT METEG}"
SLH = "מ:אות-מיוחדת-במילה"


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def word(value):
    if isinstance(value, str):
        return value, False
    assert isinstance(value, (list, dict))
    if isinstance(value, list):
        assert len(value) == 1
        return word(value[0])
    assert value["tmpl_name"] == SLH
    text, nested = word(value["tmpl_params"]["2"])
    assert not nested
    return text, True


def content(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(map(content, value))
    return content(value.get("contents", []))


def main():
    started = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    counts, helpers = Counter(), Counter()
    special = []
    replacements = []
    examples = {}
    aliases = {"D1-Psalms": "Ps", "D2-Proverbs": "Pr", "D3-Job": "Jb"}

    def walk(value, ref):
        if isinstance(value, list):
            for child in value:
                walk(child, ref)
        elif isinstance(value, dict):
            name = value.get("tmpl_name")
            if name in {"מ:דחי", "מ:צינור"}:
                helpers[name] += 1
                params = value["tmpl_params"]
                a, special1 = word(params["1"])
                b, special2 = word(params["2"])
                mark = DEHI if name == "מ:דחי" else TSINNOR
                replaced = [
                    i
                    for i, c in enumerate(a)
                    if c == METEG and a[:i] + mark + a[i + 1 :] == b
                ]
                if replaced:
                    assert len(replaced) == 1 and not (special1 or special2)
                    i = replaced[0]
                    kept = a[: i + 1] + mark + a[i + 1 :]
                    replacements.append(
                        {
                            "reference": ref,
                            "template": name,
                            "parameter_1": a,
                            "parameter_2": b,
                            "independent_kept_form": kept,
                        }
                    )
                    kind = "meteg-on-helper-letter"
                else:
                    added = [
                        i
                        for i, c in enumerate(b)
                        if c == mark and b[:i] + b[i + 1 :] == a
                    ]
                    assert len(added) == 1, (ref, a, b)
                    i = added[0]
                    metegs = [j for j, c in enumerate(a) if c == METEG]
                    assert all(j < i for j in metegs)
                    if not metegs:
                        kind = "no-meteg"
                    elif any(any(c in "־ " for c in a[j:i]) for j in metegs):
                        kind = "meteg-on-earlier-atom"
                    else:
                        kind = "meteg-earlier-in-stressed-atom"
                if name == "מ:דחי":
                    counts[kind] += 1
                    examples.setdefault(
                        kind, {"reference": ref, "parameter_1": a, "parameter_2": b}
                    )
                    if special1 or special2:
                        special.append(
                            {
                                "reference": ref,
                                "kind": kind,
                                "parameter_1": a,
                                "parameter_2": b,
                                "both_wrapped": special1 and special2,
                            }
                        )
            for child in value.values():
                walk(child, ref)

    for path in sorted((ROOT / "MAM-parsed/plus").glob("*.json")):
        data = json.loads(path.read_text())
        for book in data["book39s"]:
            for chapter, verses in book["chapters"].items():
                for verse, cells in verses.items():
                    walk(cells, f"{aliases.get(path.stem, path.stem)}{chapter}:{verse}")
            if ending := book["good_ending_plus"]:
                walk(ending["wikitext_element"], "good-ending:" + path.stem)
    assert len(special) == 3 and all(case["both_wrapped"] for case in special)
    assert len(replacements) == 9 and all(
        case["template"] == "מ:דחי" for case in replacements
    )
    output = ROOT / "gh-pages/MAM-with-doc/foi/foi-dexi-stress-meteg.json"
    previous = json.loads(
        git(ROOT, "show", f"{OLD}:gh-pages/MAM-with-doc/foi/foi-dexi-stress-meteg.json")
    )
    current = json.loads(output.read_text())
    assert len(previous) == len(current) == 9
    by_ref = {case["reference"]: case for case in replacements}
    for old, new in zip(previous, current):
        assert {k: v for k, v in old.items() if k != "note"} == {
            k: v for k, v in new.items() if k != "note"
        }
        expected = by_ref[new["bcv_short"]]["independent_kept_form"]
        lemmas = [
            node
            for node in new["note"]
            if isinstance(node, dict)
            and node.get("attr", {}).get("class") == "mam-doc-lemma"
        ]
        assert len(lemmas) == 1 and content(lemmas[0]) == expected
        assert json.dumps(old["note"], ensure_ascii=False).replace(
            METEG, ""
        ) == json.dumps(new["note"], ensure_ascii=False).replace(METEG, "")
    page = html.fromstring(output.with_suffix(".html").read_bytes())
    centered = page.xpath('//p[contains(@style,"text-align: center")]')
    assert len(centered) == 2
    for paragraph, kind in zip(
        centered, ("meteg-on-earlier-atom", "meteg-earlier-in-stressed-atom")
    ):
        example = examples[kind]
        assert "".join("".join(paragraph.itertext()).split()) == "".join(
            (example["parameter_1"] + example["parameter_2"]).split()
        )
        assert example["reference"] in page.text_content()
    page_text = " ".join(page.text_content().split())
    for number in (sum(counts.values()), *counts.values()):
        assert f"{number:,}" in page_text
    assert "not classified" not in page_text
    deltas = {}
    for book in ("D1-Psalms", "D2-Proverbs", "D3-Job"):
        relative = f"gh-pages/MAM-with-doc/{book}.html"
        before, after = (
            git(ROOT, "show", f"{OLD}:{relative}").decode(),
            (ROOT / relative).read_text(),
        )
        norm = lambda text: re.sub(r"\s+", "", text.replace(METEG, ""))
        assert norm(before) == norm(after)
        deltas[book] = after.count(METEG) - before.count(METEG)
    assert not git(
        ROOT,
        "diff",
        OLD,
        NEW,
        "--",
        "MAM-parsed",
        "Phonetic-MAM",
        "out/near-aleppo",
        "gh-pages/near-aleppo",
        "gh-pages/phonetic-mam",
    )
    out = ROOT / ".novc/hourly"
    out.mkdir(parents=True, exist_ok=True)
    result = {
        "source": NEW,
        "parent": OLD,
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "seconds": round(time.monotonic() - start, 3),
        "raw_helper_counts": dict(helpers),
        "independent_dehi_census": dict(counts),
        "classified_special_letter_calls": special,
        "raw_meteg_replacement_cases": replacements,
        "first_raw_examples": examples,
        "published_nine_raw_pairs_preserved": True,
        "nine_note_lemmas_equal_independent_kept_forms": True,
        "intro_examples_match_first_raw_calls": True,
        "three_book_html_changes_only_meteg_and_wrapping": deltas,
        "raw_phonetic_and_near_aleppo_products_unchanged": True,
        "limits": "File/source inspection only, with no project rendering/classification calls, generators, tests, font build/shaping or Private content read. Runtime validation/isolation/regeneration remain pending parent release.",
    }
    (out / "lightweight-result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
