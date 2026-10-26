"""One-off independent census of committed exports versus the rendered page."""

from collections import Counter
import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

from mb_cmn import paths

ROOT = paths.repo_root()
RESULT = {}


class Plain(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.elements = Counter()

    def handle_starttag(self, tag, attrs):
        self.elements[tag, dict(attrs).get("class", "")] += 1

    def handle_data(self, value):
        self.text.append(value)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None
        self.text = []
        self.ids = []
        self.links = []
        self.metas = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "meta":
            self.metas.append(attrs)
        if tag == "table":
            assert self.table is None
            self.table = []
        elif tag == "tr":
            self.row = []
        elif tag in {"td", "th"}:
            assert self.cell is None
            self.cell = {"tag": tag, "attrs": attrs, "text": ""}
        elif tag == "br" and self.cell is not None:
            self.cell["text"] += " "

    def handle_data(self, value):
        self.text.append(value)
        if self.cell is not None:
            self.cell["text"] += value

    def handle_endtag(self, tag):
        if tag in {"td", "th"}:
            self.row.append(self.cell)
            self.cell = None
        elif tag == "tr":
            self.table.append(self.row)
            self.row = None
        elif tag == "table":
            self.tables.append(self.table)
            self.table = None


def norm(value):
    return " ".join(value.split())


def page_data():
    page = Page()
    page.feed(
        (ROOT / "gh-pages/MAM-for-Sefaria/index.html").read_text(encoding="utf-8")
    )
    page.close()
    assert page.table is None and page.cell is None
    return page


def test_census_matches_published_counts_and_inventory():
    data = ROOT / "MAM-for-Sefaria"
    expected = {"csv": Counter(), "csv-ajf": Counter()}
    rows_by_folder = {}
    elements = Counter()
    all_text = []
    for folder in expected:
        files = sorted((data / folder).glob("*.csv"))
        assert len(files) == 39
        count = 0
        dual = 0
        for path in files:
            with path.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.reader(stream))
            if folder == "csv":
                assert len(rows[:5]) == 5 and all(len(row) == 2 for row in rows)
                assert [row[0] for row in rows[:5]] == [
                    "Index Title",
                    "Version Title",
                    "Language",
                    "Version Source",
                    "Version Notes",
                ]
                rows = rows[5:]
                for ref, html in rows:
                    parser = Plain()
                    parser.feed(html)
                    parser.close()
                    text = "".join(parser.text)
                    elements.update(parser.elements)
                    expected[folder].update(text)
                    all_text.append(text)
            else:
                assert all(len(row) == 4 for row in rows)
                for ref, combined, alef, bet in rows:
                    assert bool(alef) == bool(bet)
                    dual += bool(alef)
                    expected[folder].update(combined + alef + bet)
                    all_text.extend((combined, alef, bet))
            count += len(rows)
        rows_by_folder[folder] = count
        if folder == "csv-ajf":
            RESULT["dual_cantillation_rows"] = dual
    page = page_data()
    char_tables = [
        table
        for table in page.tables
        if [norm(cell["text"]) for cell in table[0]]
        == ["Code point", "Unicode name", "In the listings", "csv/", "csv-ajf/"]
    ]
    assert len(char_tables) == 1
    observed = {"csv": Counter(), "csv-ajf": Counter()}
    for row in char_tables[0][1:]:
        char = chr(int(norm(row[0]["text"])[2:], 16))
        for folder, cell in zip(observed, row[-2:]):
            observed[folder][char] = int(norm(cell["text"]).replace(",", ""))
    assert set(observed["csv"]) == expected["csv"].keys() | expected["csv-ajf"].keys()
    assert observed == expected
    markup_tables = [
        table
        for table in page.tables
        if [norm(cell["text"]) for cell in table[0]]
        == ["Element", "Class", "Count", "What it holds"]
    ]
    assert len(markup_tables) == 1
    actual_elements = Counter(
        {
            (norm(row[0]["text"]), norm(row[1]["text"])): int(
                norm(row[2]["text"]).replace(",", "")
            )
            for row in markup_tables[0][1:]
        }
    )
    assert actual_elements == elements
    file_tables = [
        table for table in page.tables if norm(table[0][0]["text"]) == "Folder"
    ]
    assert len(file_tables) == 1
    for row in file_tables[0][1:]:
        folder = norm(row[0]["text"])
        key = "csv-ajf" if "ajf" in folder else "csv"
        assert int(norm(row[2]["text"]).replace(",", "")) == rows_by_folder[key]
    RESULT.update(
        {
            "raw_file_count": 78,
            "rows_by_folder": rows_by_folder,
            "distinct_code_points": len(observed["csv"]),
            "code_point_counts_exact": True,
            "element_class_counts_exact": True,
            "markup_counts": {
                f"{tag} {cls}".strip(): count for (tag, cls), count in elements.items()
            },
        }
    )
    # Mechanical check over rendered Hebrew cells: every displayed two-vowel cluster
    # retains its CGJ and is a cluster that the product itself actually contains.
    cluster_re = re.compile(
        r"[\u05d0-\u05ea][\u0591-\u05bd\u05bf\u05c1-\u05c5\u05c7\u034f]*"
    )
    vowels = set(map(chr, range(0x05B0, 0x05BC))) | {"\N{HEBREW POINT QAMATS QATAN}"}
    allowed = {m.group() for text in all_text for m in cluster_re.finditer(text)}
    he_cells = [
        cell
        for table in page.tables
        for row in table
        for cell in row
        if cell["attrs"].get("lang") == "hbo"
    ]
    assert he_cells
    multi = 0
    for cell in he_cells:
        assert cell["attrs"].get("dir") == "rtl"
        for match in cluster_re.finditer(cell["text"]):
            cluster = match.group()
            if sum(char in vowels for char in cluster) > 1:
                assert "\N{COMBINING GRAPHEME JOINER}" in cluster
                assert cluster in allowed
                multi += 1
    RESULT["rendered_hebrew_cells"] = len(he_cells)
    RESULT["rendered_two_vowel_clusters_with_product_CGJ"] = multi


def test_local_links_viewport_and_canonical_font_copy():
    page = page_data()
    assert len(page.ids) == len(set(page.ids))
    assert [meta for meta in page.metas if meta.get("name") == "viewport"] == [
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
    for href in page.links:
        parts = urlsplit(href)
        if parts.scheme or parts.netloc:
            continue
        target = (
            (ROOT / "gh-pages/MAM-for-Sefaria" / unquote(parts.path)).resolve()
            if parts.path
            else ROOT / "gh-pages/MAM-for-Sefaria/index.html"
        )
        assert target.is_file(), href
        if parts.fragment:
            linked = Page()
            linked.feed(target.read_text(encoding="utf-8"))
            assert unquote(parts.fragment) in linked.ids, href
    names = (
        subprocess.check_output(
            [
                "git",
                "ls-files",
                "-z",
                "--",
                "doc/woff2/Taamey_D.woff2",
                "gh-pages/**/woff2/Taamey_D.woff2",
            ]
        )
        .decode()
        .split("\0")
    )
    names = [name for name in names if name]
    assert len(names) == 17
    hashes = {hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}
    assert hashes == {
        "5cc8df8ae3311b91e506edbb294561f6f0e39ebe4260bdb972c90902186c2474"
    }
    assert "seventeen tracked, byte-identical copies" in (
        ROOT / "DATA-LICENSES.md"
    ).read_text(encoding="utf-8")
    RESULT["local_links_and_fragments_resolve"] = True
    RESULT["font_copies"] = {"count": len(names), "sha256": next(iter(hashes))}
    out = ROOT / ".novc/hourly-sefaria/census-result.json"
    out.write_text(
        json.dumps(RESULT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
