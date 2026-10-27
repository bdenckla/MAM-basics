"""Inspect changed HTML and verify endpoint formatting, without regeneration."""

from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys

from lxml import etree, html


def main():
    root = Path.cwd()
    old = "629218d2f44c006f36eeb0dcb16e8eacdd052a41"
    files = subprocess.check_output(
        ["git", "diff", "--name-only", "-z", old, "HEAD"]
    ).split(b"\0")
    pages = [name.decode() for name in files if name.endswith(b".html")]
    assert len(pages) == 6
    result = {}
    for name in pages:
        before = subprocess.check_output(["git", "show", f"{old}:{name}"]).decode()
        after = (root / name).read_text()
        a, b = html.fromstring(before), html.fromstring(after)
        if "MAM-with-doc" in name:
            remove = str.maketrans(
                "", "", "\N{HEBREW ACCENT DEHI}\N{HEBREW ACCENT ZINOR}"
            )
            normalize = lambda text: re.sub(r"\s+", "", text.translate(remove))
            assert normalize(before) == normalize(after), name
            assert [(n.tag, dict(n.attrib)) for n in a.iter()] == [
                (n.tag, dict(n.attrib)) for n in b.iter()
            ], name
            counts_a = Counter("".join(a.itertext()))
            counts_b = Counter("".join(b.itertext()))
            marks = {
                f"U+{ord(mark):04X}": counts_b[mark] - counts_a[mark]
                for mark in ("\N{HEBREW ACCENT DEHI}", "\N{HEBREW ACCENT ZINOR}")
            }
            assert all(value >= 0 for value in marks.values())
            result[name] = {
                "all_markup_and_attributes_equal": True,
                "only_helper_marks_and_line_wrapping_differ": True,
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
