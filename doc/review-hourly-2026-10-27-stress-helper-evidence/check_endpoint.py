"""Inspect changed HTML and verify endpoint formatting, without regeneration."""

from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

from lxml import etree, html


def main():
    root = Path.cwd()
    old = "629218d2f44c006f36eeb0dcb16e8eacdd052a41"
    files = subprocess.check_output(
        ["git", "diff", "--name-only", "-z", old, "HEAD"]
    ).split(b"\0")
    pages = [name.decode() for name in files if name.endswith(b".html")]
    assert len(pages) == 6
    changed_characters = set()
    meteg_examples = []

    def inventory(value):
        if isinstance(value, list):
            for child in value:
                inventory(child)
        elif isinstance(value, dict):
            if value.get("tmpl_name") in {"מ:דחי", "מ:צינור"}:
                params = value["tmpl_params"]
                left = json.dumps(params["1"], ensure_ascii=False, sort_keys=True)
                right = json.dumps(params["2"], ensure_ascii=False, sort_keys=True)
                a, b = Counter(left), Counter(right)
                changed_characters.update(
                    c for c in a.keys() | b.keys() if a[c] != b[c]
                )
                if (
                    a["\N{HEBREW POINT METEG}"] != b["\N{HEBREW POINT METEG}"]
                    and len(meteg_examples) < 8
                ):
                    meteg_examples.append(
                        {"parameter_1": params["1"], "parameter_2": params["2"]}
                    )
            for child in value.values():
                inventory(child)

    for path in (root / "MAM-parsed/plus").glob("*.json"):
        inventory(json.loads(path.read_text()))
    assert changed_characters
    assert all(
        unicodedata.category(c) == "Mn" for c in changed_characters
    ), changed_characters
    (root / ".novc/hourly/raw-mark-deltas.json").write_text(
        json.dumps(
            {
                "changed_codepoints": sorted(
                    f"U+{ord(c):04X}" for c in changed_characters
                ),
                "meteg_examples": meteg_examples,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    result = {}
    for name in pages:
        before = subprocess.check_output(["git", "show", f"{old}:{name}"]).decode()
        after = (root / name).read_text()
        a, b = html.fromstring(before), html.fromstring(after)
        if "MAM-with-doc" in name:
            remove = str.maketrans("", "", "".join(changed_characters))
            normalize = lambda text: re.sub(r"\s+", "", text.translate(remove))
            if normalize(before) != normalize(after):
                x, y = normalize(before), normalize(after)
                index = next(i for i, (a, b) in enumerate(zip(x, y)) if a != b)
                detail = {
                    "page": name,
                    "index": index,
                    "before": x[max(0, index - 100) : index + 220],
                    "after": y[max(0, index - 100) : index + 220],
                }
                (root / ".novc/hourly/endpoint-diagnosis.json").write_text(
                    json.dumps(detail, ensure_ascii=False, indent=2) + "\n"
                )
                raise AssertionError(str(detail))
            assert [(n.tag, dict(n.attrib)) for n in a.iter()] == [
                (n.tag, dict(n.attrib)) for n in b.iter()
            ], name
            counts_a = Counter("".join(a.itertext()))
            counts_b = Counter("".join(b.itertext()))
            marks = {
                f"U+{ord(mark):04X}": counts_b[mark] - counts_a[mark]
                for mark in sorted(changed_characters)
            }
            result[name] = {
                "all_markup_and_attributes_equal": True,
                "only_raw_parameter_mark_differences_and_line_wrapping": True,
                "mark_count_deltas": marks,
            }
        else:
            rows_a, rows_b = a.xpath("//tr"), b.xpath("//tr")
            assert len(rows_a) == len(rows_b)
            differences = [
                index
                for index, (x, y) in enumerate(zip(rows_a, rows_b))
                if etree.tostring(x) != etree.tostring(y)
            ]
            assert len(differences) == 1
            index = differences[0]
            cells_a, cells_b = rows_a[index].xpath("./td"), rows_b[index].xpath("./td")
            assert len(cells_a) == len(cells_b)
            assert all(
                etree.tostring(x) == etree.tostring(y)
                for x, y in zip(cells_a[1:], cells_b[1:])
            )
            assert "How the edition has the added parameters" in "".join(
                cells_b[0].itertext()
            )
            result[name] = {"only_one_declared_choice_cell_changed": True, "row": index}
    (root / ".novc/hourly/endpoint-result.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))
    changed_python = [name.decode() for name in files if name.endswith(b".py")]
    subprocess.run(
        [sys.executable, "-m", "black", "--check", *changed_python], check=True
    )
    subprocess.run(["git", "diff", "--check", old, "HEAD"], check=True)


if __name__ == "__main__":
    main()
