"""Compare the static Sefaria guide's case table with all MAM-simple annotations.

This is a node inventory, not an edition text walk: every silluq annotation in
canonical MAM-simple XML needs a documented column. The other-MAM forms are
checked against that inventory, and the Sefaria forms against both exporters'
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
        self.refs = []
        self.versions = {}
        self.tables = 0
        self.in_table = False
        self.version = None
        self.cells = None
        self.cell = None
        self.cell_tag = None
        self.row_label = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "table" and attrs.get("id") == "meteg-after-silluq-cases":
            assert not self.in_table
            self.tables += 1
            self.in_table = True
        elif self.in_table and tag == "tr" and "data-version" in attrs:
            assert self.version is None
            self.version = attrs["data-version"]
            assert self.version in {"sefaria", "other-mam"}
            assert self.version not in self.versions
            self.cells = []
            self.row_label = None
        elif self.in_table and tag == "th" and "data-osis-id" in attrs:
            assert attrs.get("scope") == "col"
            assert self.version is None
            self.refs.append(attrs["data-osis-id"])
        elif self.in_table and tag == "th" and attrs.get("scope") == "row":
            assert self.version is not None
            assert self.cell is None and self.row_label is None
            self.cell = []
            self.cell_tag = tag
        elif self.in_table and tag == "td":
            assert self.version is not None, "A documented form lacks its version row"
            assert self.cell is None
            assert attrs.get("dir") == "rtl"
            assert attrs.get("lang") == "hbo"
            self.cell = []
            self.cell_tag = tag

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if self.cell_tag is not None and tag == self.cell_tag:
            text = "".join(self.cell).strip()
            if tag == "th":
                self.row_label = text
            else:
                self.cells.append(text)
            self.cell = None
            self.cell_tag = None
        elif tag == "tr" and self.version is not None:
            assert self.cell is None
            labels = {"sefaria": "Sefaria", "other-mam": "other versions of MAM"}
            assert self.row_label == labels[self.version]
            assert len(self.cells) == len(self.refs)
            self.versions[self.version] = self.cells
            self.version = None
            self.cells = None
        elif tag == "table" and self.in_table:
            assert self.version is None and self.cell is None
            assert set(self.versions) == {"sefaria", "other-mam"}
            self.rows = list(
                zip(self.refs, self.versions["other-mam"], self.versions["sefaria"])
            )
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


def test_sefaria_guide_lists_every_silluq_annotation_with_its_sefaria_form():
    page = paths.repo_root() / "gh-pages/MAM-for-Sefaria/index.html"
    table = _CaseTable()
    table.feed(page.read_text(encoding="utf-8"))
    table.close()
    assert not table.in_table and table.version is None
    assert table.tables == 1, "Expected one documented silluq case table"
    for _ref, source, output in table.rows:
        assert has_std_mark_order(source)
        assert has_std_mark_order(output)
    assert Counter(table.rows) == Counter(_annotation_rows())
