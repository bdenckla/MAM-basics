"""Read-only archive/hash and raw-JSON census; no generator, font build or shaping."""

import ast
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha1, sha256
import io
import json
from pathlib import Path
import re
import subprocess
import time
import unicodedata
import zipfile

from fontTools.ttLib import TTFont

ROOT = Path("/workspace/review-hourly-20261027-dehi-font/source")
FONT_REPO = Path("/workspace/hbofonts")
FONT_TIP = "bb25283c010ea738ee11416edc1eb2faf12419c7"
RELEASE_SOURCE = "68cd629022028ec648c0ee2f36ac0480123d0d47"
DEHI = "\N{HEBREW ACCENT DEHI}"
METEG = "\N{HEBREW POINT METEG}"


def blob(commit, path):
    return subprocess.check_output(
        ["git", "-C", str(FONT_REPO), "show", f"{commit}:{path}"]
    )


def singleton(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
        return value[0]
    return None


def html_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(map(html_text, value))
    return html_text(value.get("contents", []))


def main():
    began = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    out = ROOT / ".novc/hourly"
    out.mkdir(parents=True, exist_ok=True)
    prefix = "gh-pages/downloads/snapshots/1.0-hbofonts-68cd62902202/"
    provenance_bytes = blob(FONT_TIP, prefix + "provenance.json")
    sums_bytes = blob(FONT_TIP, prefix + "SHA256SUMS.txt")
    provenance = json.loads(provenance_bytes)
    assert provenance["source"]["commit"] == RELEASE_SOURCE
    support = ROOT / "in/font-support/taamey-d-1.0"
    inventory = json.loads((support / "SOURCE-INVENTORY.json").read_text())
    assert (
        inventory["release_snapshot"]["provenance_sha256"]
        == sha256(provenance_bytes).hexdigest()
    )
    assert (
        inventory["release_snapshot"]["sha256sums_sha256"]
        == sha256(sums_bytes).hexdigest()
    )
    canonical = (ROOT / "gh-pages/woff2/Taamey_D.woff2").read_bytes()
    assert len(canonical) == inventory["binary"]["size"]
    assert sha256(canonical).hexdigest() == inventory["binary"]["sha256"]
    assert (
        sha1(b"blob " + str(len(canonical)).encode() + b"\0" + canonical).hexdigest()
        == inventory["binary"]["git_blob"]
    )
    binary_zip = blob(FONT_TIP, prefix + "Taamey_D.zip")
    source_zip = (support / "Taamey_D-1.0-sources.zip").read_bytes()
    assert source_zip == blob(FONT_TIP, prefix + "Taamey_D-sources.zip")
    for name, raw in (
        ("Taamey_D.zip", binary_zip),
        ("Taamey_D-sources.zip", source_zip),
    ):
        declared = provenance["files"][name]
        assert declared["sha256"] == sha256(raw).hexdigest()
        assert declared["size"] == len(raw)
        assert f"{sha256(raw).hexdigest()}  {name}\n" in sums_bytes.decode()
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            assert archive.testzip() is None
            actual = [
                {
                    "path": item.filename,
                    "size": item.file_size,
                    "sha256": sha256(archive.read(item)).hexdigest(),
                }
                for item in archive.infolist()
            ]
            assert actual == declared["members"]
            if name.endswith("sources.zip"):
                assert actual == inventory["source_archive"]["members"]
                assert len(actual) == 9
                for item in actual:
                    path = item["path"]
                    assert archive.read(path) == blob(RELEASE_SOURCE, path)
                    assert not path.endswith(".sfd") or path.endswith("-nofea.sym.sfd")
                    assert not path.endswith(".fea") or path.endswith(".sym.fea")
            else:
                assert canonical == archive.read("Taamey_D/Taamey_D.woff2")
                ttf = TTFont(io.BytesIO(archive.read("Taamey_D/Taamey_D.ttf")))
                notice = ttf["name"].getDebugName(0)
                assert (
                    sha256(notice.encode()).hexdigest()
                    == inventory["font_notice"]["extracted_utf8_sha256"]
                )
                formatted = (
                    "\n".join(
                        line.rstrip() if not line.strip() else line
                        for line in notice.splitlines()
                    ).rstrip("\n")
                    + "\n"
                )
                assert formatted.encode() == (support / "FONT-NOTICE.txt").read_bytes()
    archive_records = {
        "font_tip": FONT_TIP,
        "release_source": RELEASE_SOURCE,
        "binary_sha256": sha256(canonical).hexdigest(),
        "source_zip_sha256": sha256(source_zip).hexdigest(),
        "source_members_exact_git_bytes": 9,
        "snapshot_metadata_hashes_equal": True,
        "embedded_notice_matches_recorded_formatting": True,
    }
    for name in ("FONT-NOTICE.txt", "GPL-2.0.txt"):
        previous = subprocess.check_output(
            [
                "git",
                "-C",
                str(ROOT),
                "show",
                f"9302ad04:in/font-support/taamey-d-0.921/{name}",
            ]
        )
        assert previous == (support / name).read_bytes()
    mapping = {
        f"font-sources/taamey-d-1.0/{path.name}": path.read_bytes()
        for path in support.iterdir()
        if path.name not in {"README.md", "PRODUCT-WOFF2-SOURCE.txt"}
    }
    mapping.update(
        {
            "woff2/" + name: (support / name).read_bytes()
            for name in ("FONT-NOTICE.txt", "GPL-2.0.txt")
        }
    )
    mapping["woff2/SOURCE.txt"] = (support / "PRODUCT-WOFF2-SOURCE.txt").read_bytes()
    assert len(mapping) == 9
    for name, data in mapping.items():
        assert (ROOT / "gh-pages" / name).read_bytes() == data
    urls = re.findall(
        r"^  (\.\./\S+)$", (ROOT / "gh-pages/woff2/SOURCE.txt").read_text(), re.M
    )
    assert urls and all((ROOT / "gh-pages/woff2" / href).is_file() for href in urls)
    archive_records["support_mapping_files"] = len(mapping)
    archive_records["same_host_source_links"] = urls
    # Derive categories directly from the two raw strings, by a single exact
    # replacement/deletion. Do not call the FOI's classifier or renderer.
    counts = Counter()
    rows = []
    special_marks = Counter()
    aliases = {"D1-Psalms": "Ps", "D2-Proverbs": "Pr", "D3-Job": "Jb"}

    def walk(value, ref, notes=()):
        if isinstance(value, list):
            for child in value:
                walk(child, ref, notes)
        elif isinstance(value, dict):
            name = value.get("tmpl_name")
            params = value.get("tmpl_params", {})
            if name == "מ:דחי":
                a, b = singleton(params["1"]), singleton(params["2"])
                if a is None or b is None:
                    counts["template-in-parameter"] += 1
                else:
                    replacements = [
                        i
                        for i, char in enumerate(a)
                        if char == METEG and a[:i] + DEHI + a[i + 1 :] == b
                    ]
                    if replacements:
                        assert len(replacements) == 1 and notes
                        counts["meteg-on-helper-letter"] += 1
                        rows.append(
                            {
                                "bcv_short": ref,
                                "r": a,
                                "parameter_2": b,
                                "note_source": notes[-1],
                            }
                        )
                    else:
                        added = [
                            i
                            for i, char in enumerate(b)
                            if char == DEHI and b[:i] + b[i + 1 :] == a
                        ]
                        assert len(added) == 1, (ref, a, b)
                        position = added[0]
                        base = position - 1
                        while unicodedata.category(a[base]) == "Mn":
                            base -= 1
                        metegs = [i for i, char in enumerate(a) if char == METEG]
                        assert all(i < base for i in metegs), (ref, a, b)
                        if not metegs:
                            counts["no-meteg"] += 1
                        elif any(
                            any(char in "־ " for char in a[i:base]) for i in metegs
                        ):
                            counts["meteg-on-earlier-atom"] += 1
                        else:
                            counts["meteg-earlier-in-stressed-atom"] += 1
            for key, child in value.items():
                if key != "tmpl_params":
                    if key != "tmpl_name":
                        walk(child, ref, notes)
                    continue
                for parameter, content in child.items():
                    next_notes = (
                        (*notes, value)
                        if name == "נוסח" and parameter == "1"
                        else notes
                    )
                    walk(content, ref, next_notes)

    files = list((ROOT / "MAM-parsed/plus").glob("*.json"))
    assert len(files) == 24
    for path in sorted(files):
        raw = path.read_text()
        data = json.loads(raw)
        for book in data["book39s"]:
            for chapter, verses in book["chapters"].items():
                for verse, cells in verses.items():
                    walk(cells, f"{aliases.get(path.stem, path.stem)}{chapter}:{verse}")
            if book["good_ending_plus"]:
                good = book["good_ending_plus"]
                walk(good["wikitext_element"], "good-ending:" + path.stem)
        for character in ("\u05c8", "\u05c9"):
            special_marks[f"U+{ord(character):04X}"] += json.dumps(
                data, ensure_ascii=False
            ).count(character)
    published = json.loads(
        (ROOT / "gh-pages/MAM-with-doc/foi/foi-dexi-stress-meteg.json").read_text()
    )
    assert [(row["bcv_short"], row["r"], row["parameter_2"]) for row in rows] == [
        (row["bcv_short"], row["r"], row["parameter_2"]) for row in published
    ]
    for expected, actual in zip(rows, published):
        body = expected["note_source"]["tmpl_params"]["2"]
        assert "קו של געיה להורות על מקום הטעם" in json.dumps(body, ensure_ascii=False)
        assert actual["parameter_2"] in html_text(actual["note"])
    html_page = (
        ROOT / "gh-pages/MAM-with-doc/foi/foi-dexi-stress-meteg.html"
    ).read_text()
    for count in (
        sum(counts.values()),
        counts["no-meteg"],
        counts["meteg-on-earlier-atom"],
        counts["meteg-earlier-in-stressed-atom"],
        counts["meteg-on-helper-letter"],
        counts["template-in-parameter"],
    ):
        assert f"{count:,}" in html_page
    assert html_page.count("<tr>") == len(rows)

    class RemoveDocstrings(ast.NodeTransformer):
        def visit_Expr(self, node):
            return (
                None
                if isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)
                else self.generic_visit(node)
            )

    before = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", "9302ad04:py/py_html/hebrew_letter_spacing.py"]
    ).decode()
    after = (ROOT / "py/py_html/hebrew_letter_spacing.py").read_text()
    assert ast.dump(RemoveDocstrings().visit(ast.parse(before))) == ast.dump(
        RemoveDocstrings().visit(ast.parse(after))
    )
    result = {
        "source": "46f80ecc8b29fdd7f5fdf30c40bc2b3382bbb352",
        "began_utc": began,
        "ended_utc": datetime.now(timezone.utc).isoformat(),
        "seconds": round(time.monotonic() - start, 3),
        "archive_checks": archive_records,
        "independent_raw_census": dict(counts),
        "raw_rows_equal_published": len(rows),
        "raw_refs": [row["bcv_short"] for row in rows],
        "special_mark_counts_in_all_raw_json": dict(special_marks),
        "spacing_executable_ast_unchanged": True,
        "limits": "No generator, project classifier/rendering call, font build, shaping, suite or Private read. Only lightweight file/archive/hash and direct raw-JSON inspection. Regeneration and shared-renderer regression checks await parent release of overlap restriction.",
    }
    (out / "lightweight-result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
