"""Compare the static Sefaria guide's case table with all MAM-simple annotations.

This is a node inventory, not an edition text walk: every silluq annotation in
canonical MAM-simple XML needs a documented row. The table's input forms are
checked against that inventory, and its output forms against both exporters'
explicit leaf handlers. No case names or populations are pinned in this test.
"""

from collections import Counter
from html.parser import HTMLParser
import subprocess
import xml.etree.ElementTree as ET

from mb_cmn import paths
from mb_cmn.git_process import git_command
from mb_cmn.uni_denorm import has_std_mark_order
from mb_sefaria import mam4ajf_handlers, mam4sef_handlers


class _CaseTable(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.tables = 0
        self.in_table = False
        self.ref = None
        self.cells = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "table" and attrs.get("id") == "meteg-after-silluq-cases":
            assert not self.in_table
            self.tables += 1
            self.in_table = True
        elif self.in_table and tag == "tr" and "data-osis-id" in attrs:
            assert self.ref is None
            self.ref = attrs["data-osis-id"]
            self.cells = []
        elif self.in_table and tag == "td":
            assert self.ref is not None, "A documented case lacks its OSIS reference"
            assert self.cell is None
            if self.cells:
                assert attrs.get("dir") == "rtl"
                assert attrs.get("lang") == "hbo"
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self.cell is not None:
            self.cells.append("".join(self.cell).strip())
            self.cell = None
        elif tag == "tr" and self.ref is not None:
            assert len(self.cells) == 3
            self.rows.append((self.ref, self.cells[1], self.cells[2]))
            self.ref = None
            self.cells = None
        elif tag == "table" and self.in_table:
            assert self.ref is None
            self.in_table = False


def _annotation_rows():
    root = paths.repo_root()
    tracked = subprocess.run(
        git_command(root, "ls-files", "-z", "--", "MAM-simple/xml-vtrad-mam/*.xml"),
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    files = [root / name for name in tracked.stdout.split("\0") if name]
    assert files, "No tracked canonical MAM-simple XML files"
    rows = []
    verses = 0
    for path in files:
        for verse in ET.parse(path).getroot().iter("verse"):
            verses += 1
            for element in verse.iter("silluq-before-meteg"):
                assert set(element.attrib) == {"text", "letters-with-silluq"}
                assert len(element) == 0
                node = {"type": element.tag, **element.attrib}
                projections = [
                    mam4sef_handlers.HANDLERS,
                    *mam4ajf_handlers.HANDLERS.values(),
                ]
                outputs = [
                    handlers[(element.tag, None)](node, [], [])
                    for handlers in projections
                ]
                assert all(output == outputs[0] for output in outputs)
                assert len(outputs[0]) == 1
                rows.append((verse.attrib["osisID"], node["text"], outputs[0][0]))
    assert verses, "No verses in the canonical MAM-simple XML files"
    return rows


def test_sefaria_guide_lists_every_silluq_annotation_with_its_exported_form():
    page = paths.repo_root() / "gh-pages/MAM-for-Sefaria/index.html"
    table = _CaseTable()
    table.feed(page.read_text(encoding="utf-8"))
    table.close()
    assert not table.in_table and table.ref is None
    assert table.tables == 1, "Expected one documented silluq case table"
    for _ref, source, output in table.rows:
        assert has_std_mark_order(source)
        assert has_std_mark_order(output)
    assert Counter(table.rows) == Counter(_annotation_rows())
