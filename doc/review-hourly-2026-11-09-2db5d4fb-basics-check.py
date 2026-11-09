"""Sparse endpoint differential checks, not a repository test or regeneration.

Reads the complete API compare and exact-head source/artifact captures. Probes
extract selected functions, with a deliberately inert table-constructor double.
"""
import ast
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from types import SimpleNamespace

ROOT = Path(__file__).parent
HEAD = ROOT / "head"
BASE = ROOT / "base"
compare = json.loads((HEAD / "compare-full.json").read_text())
base = "0203db8fe6fb816eddc5880bd588c2d6f010a213"
head = "2db5d4fbe24dab0509a4fb5e92511de1535b3a6f"
assert compare["base_commit"]["sha"] == base
assert compare["commits"][-1]["sha"] == head
assert compare["total_commits"] == 2 and len(compare["files"]) == 84
mark = re.compile("[\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7-\u05c9]")
letter = re.compile("[\u05d0-\u05ea]")
counts = Counter()
file_evidence = []
for item in compare["files"]:
    assert item["status"] == "modified"
    patch = item["patch"]
    removed = [line[1:] for line in patch.splitlines() if line.startswith("-")]
    added = [line[1:] for line in patch.splitlines() if line.startswith("+")]
    assert len(removed) == item["deletions"], item["filename"]
    assert len(added) == item["additions"], item["filename"]
    path = item["filename"]
    if not path.endswith(".html"):
        assert path.endswith(".py")
        ast.parse((HEAD / path).read_text())
        counts["changed_python_parses"] += 1
        continue
    assert [line.replace(' lang="hbo"', "") for line in removed] == added, path
    attrs_removed = sum(line.count(' lang="hbo"') for line in removed)
    if "/foi/" in path:
        category = "foi_label_cells"
        for line in removed:
            assert line.startswith('<td lang="hbo" dir="rtl">') and line.endswith("</td>")
            text = re.sub("<[^>]*>", "", line)
            assert letter.search(text) and not mark.search(text), path
    elif path.endswith("sigil-decoding.html"):
        category = "sigla"
        assert all('<bdi lang="hbo">' in line for line in removed)
    else:
        category = "chapter_headings"
        for line in removed:
            assert re.fullmatch('<h2 class="mam-chapter-heading" lang="hbo" dir="rtl">[^<]+</h2>', line)
            assert letter.search(line) and not mark.search(line), path
    counts[category] += attrs_removed
    counts[category + "_files"] += 1
    counts["html_changed_lines"] += len(removed)
    file_evidence.append({"path": path, "attribute_removals": attrs_removed})
assert counts["chapter_headings"] == 1858
assert counts["chapter_headings_files"] == 78
assert counts["foi_label_cells"] == 77
assert counts["sigla"] == 52
assert counts["changed_python_parses"] == 3


class StripDocs(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
            node.body.pop(0)
        return node


old_author = (BASE / "py/mb_author/author.py").read_text()
new_author = (HEAD / "py/mb_author/author.py").read_text()
assert ast.dump(StripDocs().visit(ast.parse(old_author.replace("_is_unpointed_hebrew", "is_unpointed_hebrew")))) == ast.dump(StripDocs().visit(ast.parse(new_author)))
old_mwd = (BASE / "py/py_misc/mwd_utils.py").read_text()
new_mwd = (HEAD / "py/py_misc/mwd_utils.py").read_text()
old_tree, new_tree = ast.parse(old_mwd), ast.parse(new_mwd)
for node in old_tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(n, ast.Name) and n.id == "_h2_attr" for n in node.targets):
        pairs = [(k, v) for k, v in zip(node.value.keys, node.value.values) if k.value != "lang"]
        node.value.keys, node.value.values = map(list, zip(*pairs))
assert ast.dump(old_tree) == ast.dump(new_tree)


def extract(path, names, env):
    tree = ast.parse((HEAD / path).read_text())
    tree.body = [node for node in tree.body if (isinstance(node, ast.FunctionDef) and node.name in names) or (isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id in names for target in node.targets))]
    exec(compile(tree, str(path), "exec"), env)
    return SimpleNamespace(**env)


# is_htel is the exact repository helper; only table construction is doubled.
mb = extract("py/mb_misc/mb_html.py", {"is_htel"}, {})
mb.table_datum = lambda contents, attr=None: {"_htel_tag": "td", "contents": contents, "attr": attr}
author = extract("py/mb_author/author.py", {"is_unpointed_hebrew", "_text_of", "_HEBREW_MARK_RE", "_HEBREW_LETTER_RE"}, {"re": re, "mb_html": mb})
finals = extract("py/foi/foi_finals.py", {"_target_td", "_my_td", "_LABEL_PATHS", "_LIFTED_UNPOINTED_PATHS"}, {"author": author, "mb_html": mb})


class Nodes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = {"_htel_tag": "root", "attr": {}, "contents": []}
        self.stack = [self.root]
        self.nodes = []

    def handle_starttag(self, tag, attrs):
        node = {"_htel_tag": tag, "attr": dict(attrs), "contents": [], "ancestors": self.stack.copy()}
        self.stack[-1]["contents"].append(node)
        self.nodes.append(node)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]["_htel_tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1]["contents"].append(data)


parsed_rows = Counter()
for stem in ["poetic-stress-helpers", "rare-tmpls"]:
    parser = Nodes()
    parser.feed((HEAD / f"gh-pages/MAM-with-doc/foi/foi-{stem}.html").read_text())
    foi_path = None
    for node in parser.nodes:
        node_id = node["attr"].get("id", "")
        if node["_htel_tag"] == "p" and node_id.startswith("intro-"):
            foi_path = (stem, node_id.removeprefix("intro-").removesuffix("-rest"))
        if node["_htel_tag"] == "tr":
            cells = [n for n in node["contents"] if isinstance(n, dict) and n["_htel_tag"] == "td"]
            if not cells:
                continue
            got = finals._target_td(foi_path, cells[0]["contents"])
            assert got["attr"] == cells[0]["attr"], foi_path
            parsed_rows[stem] += 1
            if foi_path in finals._LABEL_PATHS:
                assert not any(n["attr"].get("lang") == "hbo" for n in cells[0]["ancestors"])
                parsed_rows["labels"] += 1
assert parsed_rows["labels"] == 77
parser = Nodes()
parser.feed((HEAD / "gh-pages/MAM-with-doc/sigil-decoding.html").read_text())
sigla = [node for node in parser.nodes if node["_htel_tag"] == "bdi"]
assert len(sigla) == 52
for node in sigla:
    assert author.is_unpointed_hebrew(node["contents"])
    assert "lang" not in node["attr"]
    assert not any(n["attr"].get("lang") == "hbo" for n in node["ancestors"])

bare = chr(0x05d0)
pointed = bare + chr(0x05b7)
for path in finals._LABEL_PATHS:
    assert finals._target_td(path, bare)["attr"] == {"dir": "rtl"}
    try:
        finals._target_td(path, pointed)
    except AssertionError:
        pass
    else:
        raise AssertionError("Pointed label was accepted")
for path in finals._LIFTED_UNPOINTED_PATHS:
    assert finals._target_td(path, bare)["attr"]["lang"] == "hbo"
try:
    finals._target_td(("other", "path"), bare)
except ValueError:
    pass
else:
    raise AssertionError("Undeclared unpointed Hebrew target was accepted")
assert finals._target_td(("other", "path"), pointed)["attr"]["lang"] == "hbo"
try:
    finals._my_td("pqere", bare)
except AssertionError:
    pass
else:
    raise AssertionError("Unpointed qere was accepted")
assert finals._my_td("pqere", pointed)["attr"]["lang"] == "hbo"

report = {
    "repository": "bdenckla/MAM-basics",
    "base": base,
    "head": head,
    "commits": 2,
    "paths": 84,
    "outcome": "No consequential evidenced defect found in the bounded endpoint screen.",
    "counts": dict(counts),
    "parsed_output_rows": dict(parsed_rows),
    "checks": [
        "Every file patch has all additions and deletions promised by API stats.",
        "All 81 HTML patches change only removal of lang=hbo, preserving Hebrew codepoints and anchors.",
        "Changed heading and FOI-label text is unpointed; all 52 sigla are unpointed and retain isolation without inherited hbo styling.",
        "All three changed Python modules parse.",
        "Shared author module is AST-equivalent after helper rename and docstring removal; heading module is AST-equivalent after its one attribute removal.",
        "Extracted exact predicate and new target/qualifier guards match all rows in the two changed FOI pages and reject undeclared unpointed Hebrew; table constructor is an explicit inert double.",
    ],
    "limits": "Connector-backed sparse artifact comparison and extracted-function probes, not actual project tests, imports, browser QA, or regeneration. No broad checks run. Sanctioned git fetch failed for missing credentials; no denial and no objects fetched. Parent is coordinating real focused regeneration separately.",
    "findings": [],
}
(ROOT / "file-evidence.json").write_text(json.dumps(file_evidence, indent=2) + "\n")
(ROOT / "result.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
