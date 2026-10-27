"""Read exact committed prose/source evidence; no MAM tests or generators."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import unicodedata as ud
import xml.etree.ElementTree as ET

ROOT = Path("/workspace/review-hourly-20261027-zwj/basics-receipts")
OUT = Path("/workspace/scratch/review-hourly-20261027-zwj/basics")
OLD = "3b23037b7e1752fdce2f7d5fa78cc5b9a3476f77"
NEW = "076198c8a4469d08204b9e33c510d5ff02ae7e48"


def blob(path):
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{NEW}:{path}"])


def main():
    OUT.mkdir(parents=True)
    names = (
        subprocess.check_output(
            ["git", "-C", str(ROOT), "diff", "--name-only", "-z", OLD, NEW]
        )
        .decode()
        .split("\0")
    )
    assert list(filter(None, names)) == ["doc/uxlc-potential-corrections.md"]
    paths = (
        subprocess.check_output(
            [
                "git",
                "-C",
                str(ROOT),
                "ls-tree",
                "-r",
                "--name-only",
                "-z",
                NEW,
                "in/UXLC-39",
            ]
        )
        .decode()
        .split("\0")
    )
    sources = {path: blob(path) for path in paths if path.endswith(".xml")}
    assert len(sources) == 39
    counts = Counter()
    contexts = []
    for path, raw in sources.items():
        text = raw.decode()
        counts.update(
            {
                "CGJ": text.count("\u034f"),
                "ZWJ": text.count("\u200d"),
                "ZWNJ": text.count("\u200c"),
            }
        )
        counts["accent_CGJ_vowel"] += len(
            re.findall("[\u0591-\u05af]\u034f[\u05b0-\u05bb\u05c7]", text)
        )
        counts["medial_meteg_ZWJ"] += len(
            re.findall("[\u05b1-\u05b3]\u200d\u05bd", text)
        )
        for match in re.finditer("\u200d", text):
            if (
                text[match.start() - 1] not in "\u05b1\u05b2\u05b3"
                or text[match.end()] != "\u05bd"
            ):
                contexts.append(
                    {"path": path, "context": text[match.start() - 2 : match.end() + 2]}
                )
    assert counts == {
        "CGJ": 1141,
        "ZWJ": 83,
        "ZWNJ": 0,
        "accent_CGJ_vowel": 264,
        "medial_meteg_ZWJ": 80,
    }
    assert len(contexts) == 3 and all(
        row["path"] == "in/UXLC-39/Job.xml" for row in contexts
    )
    job = ET.fromstring(sources["in/UXLC-39/Job.xml"])
    expected = [
        (32, 6, 11, "יְשִׁישׁ֑\u200dִים", "2023.06.10", 39, "2023.10.19", "F406A 1:20"),
        (10, 15, 12, "עָנְי֥\u200dִי׃", "2026.02.05", 35, "2026.04.01", "F400A 1:14"),
        (19, 16, 6, "פִ֗\u200d֝י", "2026.02.05", 65, "2026.04.01", "F402B 1:9"),
    ]
    records = json.loads(blob("in/UXLC-misc/all_changes.json"))
    checks = []
    for chapter, verse, number, atom, changeset, n, release, locator in expected:
        node = job.find(f'.//c[@n="{chapter}"]/v[@n="{verse}"]')
        words = [word for word in node if word.tag in {"w", "q", "k"}]
        word = words[number - 1]
        actual = (word.text or "") + "".join(child.tail or "" for child in word)
        assert actual == atom, (chapter, verse, number, actual)
        matches = [
            row
            for row in records
            if row["changeset"] == changeset and int(row["n"]) == n
        ]
        assert len(matches) == 1
        row = matches[0]
        assert row["citation"] == f"Job {chapter}:{verse}.{number}"
        assert row["release"] == release and row["lc"].replace("Folio_", "F") == locator
        assert "\u200d" in row["changetext"] and "\u200d" not in row["reftext"]
        if n == 35:
            assert (
                "\u05bd\u034f\u05b4" in row["reftext"]
                and "\u05a5\u200d\u05b4" in row["changetext"]
            )
        if n == 65:
            assert any(
                "to achieve the ordering in the display" in note
                for note in row["notes"]
            )
        checks.append(
            {
                "citation": row["citation"],
                "atom": atom,
                "record": f"{changeset}-{n}",
                "release": release,
                "locator": locator,
                "author_names": [author["name"] for author in row["authors"]],
                "reftext": row["reftext"],
                "changetext": row["changetext"],
            }
        )
    reconsidered = [
        row
        for row in records
        if row["changeset"] == "2026.02.05" and int(row["n"]) == 115
    ]
    assert (
        len(reconsidered) == 1
        and reconsidered[0]["citation"] == "Job 32:6.11"
        and "\u200d" in reconsidered[0]["changetext"]
    )
    assert ud.combining("\u034f") == ud.combining("\u200d") == 0
    assert ud.combining("\u0597") == ud.combining("\u059d") == 230
    # Normalization is queried only, never used to produce repository text.
    assert ud.normalize("NFD", "\u05d9\u05a5\u05b4") != "\u05d9\u05a5\u05b4"
    assert ud.normalize("NFD", "\u05d9\u05a5\u034f\u05b4") == "\u05d9\u05a5\u034f\u05b4"
    assert ud.normalize("NFD", "\u05e4\u05b4\u0597\u059d") == "\u05e4\u05b4\u0597\u059d"
    result = {
        "source": NEW,
        "parent": OLD,
        "classification": "Documentation-only screen; no MAM tests or generators",
        "counts": dict(counts),
        "three_atoms_and_records": checks,
        "reconsideration_record_115_matches": True,
        "combining_classes_and_reordering_queries_match": True,
        "source_sha256": {
            **{path: sha256(raw).hexdigest() for path, raw in sources.items()},
            "in/UXLC-misc/all_changes.json": sha256(
                blob("in/UXLC-misc/all_changes.json")
            ).hexdigest(),
        },
        "unicode_primary_sources": [
            "https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-23/#G19082",
            "https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-9/",
        ],
        "unicode_read_disposition": "Read official sections 23.2.2, 23.2.4 and 9.1 Meteg: the described CGJ ordering barrier, ZWJ ligation purpose and medial-meteg request agree. No standard text copied into source.",
        "limits": "Exact archived text/change-record consistency; no new manuscript-image, CLC coverage or private-font behavior claim. Recommendations remain the owner's choice and no report was sent externally.",
    }
    (OUT / "screen-result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {"counts": dict(counts), "atoms_and_records": len(checks), "source": NEW},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
