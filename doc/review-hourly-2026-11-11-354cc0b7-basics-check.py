"""Read-only artifact accounting. Does not import or run repository code."""
import ast
from collections import Counter
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import posixpath
import re
import time
from urllib.parse import unquote, urlsplit

start = time.monotonic()
root = Path(__file__).resolve().parent
head = root / "head"
source = "354cc0b7077cb46ba5d7cfc8dd9b453ff68c7bf0"
tree = json.loads((root / "tree.json").read_text())
assert not tree["truncated"]
tree = {x["path"]: x for x in tree["tree"]}
inputs = json.loads((root / "sources.json").read_text())
targets = json.loads((root / "targets.json").read_text())
for item in inputs + targets:
    data = (head / item["path"]).read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == item["sha"] == tree[item["path"]]["sha"]
pyfiles = [x["path"] for x in inputs if x["path"].endswith(".py")]
for path in pyfiles:
    ast.parse((head / path).read_bytes())

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.assets, self.forms = [], [], [], []
        self.form = None
        self.tables = self.hovers = 0
        self.note_refs, self.note_defs = [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
            if a["id"].startswith("fnref-"):
                self.note_refs.append(a["id"].removeprefix("fnref-"))
            elif a["id"].startswith("fn-"):
                self.note_defs.append(a["id"].removeprefix("fn-"))
        if tag == "a": self.links.append(a["href"])
        if tag == "link": self.assets.append(a["href"])
        if tag == "img": self.assets.append(a["src"])
        if tag == "table": self.tables += 1
        if tag == "abbr": self.hovers += 1
        if tag == "td" and "form" in a.get("class", "").split():
            assert self.form is None and a.get("dir") == "rtl"
            self.form = []
    def handle_data(self, value):
        if self.form is not None: self.form.append(value)
    def handle_endtag(self, tag):
        if tag == "td" and self.form is not None:
            self.forms.append("".join(self.form))
            self.form = None

page_path = "gh-pages/MAM-with-doc/misc/review_of_israel_bible.html"
page = Page(); page.feed((head / page_path).read_text())
assert len(page.ids) == len(set(page.ids))
assert len(page.note_refs) == len(page.note_defs) == 10
assert page.note_refs == page.note_defs
assert len(page.forms) == 112 and page.tables == 7
assert page.hovers == 143 and len(page.links) == 21
rows = json.loads((head / "in/israel-bible-review/forms.json").read_text())
assert len(rows) == 43
pairs = list(zip(page.forms[::2], page.forms[1::2]))
assert not (Counter((x["israel_bible"], x["mam"]) for x in rows) - Counter(pairs))
md = (head / "in/israel-bible-review/review.md").read_text()
mdrows = [[c.strip() for c in line.strip("|").split("|")]
          for line in md.splitlines() if re.match(r"\| [A-Za-z1-3].* \d+:\d+ \|", line)]
assert len(mdrows) == 13
strip = re.compile("[\u0591-\u05af\u05bd\u05bf\u05c0\u05c3\u05c4\u05c5\u034f\u200c-\u200f\u2060\ufeff]")
norm = str.maketrans({"\u05c7":"\u05b8", "\u05ba":"\u05b9"})
def shown(s): return re.sub(r"\s+", " ", strip.sub("", s).translate(norm)).replace("\u05be ", "\u05be").strip()
expected = Counter((x["israel_bible"],x["mam"]) for x in rows)
expected.update((shown(x[2]), shown(x[3])) for x in mdrows)
assert expected == Counter(pairs)

css_path = "gh-pages/MAM-with-doc/misc/review_of_israel_bible.css"
css = (head / css_path).read_text()
assert css.split("\n",1)[1] == (head / "py/author_misc/review_of_israel_bible.css").read_text()
target_checks = []
def check_link(value, origin):
    u = urlsplit(value)
    if u.netloc:
        if u.hostname != "bdenckla.github.io" or not u.path.startswith("/MAM-basics/"):
            return
        target = "gh-pages/" + unquote(u.path.removeprefix("/MAM-basics/"))
    elif u.path:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(origin), unquote(u.path)))
    else: target = origin
    if target.endswith("/"): target += "index.html"
    assert target in tree and tree[target]["type"] == "blob", (value,target)
    if u.fragment:
        parser = page if target == page_path else Page()
        if parser is not page: parser.feed((head / target).read_text())
        assert unquote(u.fragment) in parser.ids, (value,target)
    target_checks.append(dict(origin=origin, value=value, target=target, blob=tree[target]["sha"]))
for link in page.links + page.assets: check_link(link,page_path)
for link in re.findall(r'url\("([^\"]+)"\)',css): check_link(link,css_path)
index = Page(); index.feed((head / "gh-pages/index.html").read_text())
assert index.links.count("https://bdenckla.github.io/MAM-basics/MAM-with-doc/misc/review_of_israel_bible.html") == 1
module = ast.parse((head / "py/author_misc/review_of_israel_bible.py").read_text())
imports = [ast.unparse(x) for x in module.body if isinstance(x,(ast.Import,ast.ImportFrom))]
assert not any("private" in x.lower() or "subprocess" in x or "requests" in x for x in imports)
result = dict(result="PASS", source=source, independent_check="static artifact accounting only",
    text_blobs_verified=len(inputs)+len(targets), tree_paths=len(tree), python_files_parsed=len(pyfiles),
    displayed_pairs=len(pairs), json_pairs=len(rows), markdown_pairs=len(mdrows), tables=page.tables,
    footnotes=len(page.note_defs), abbreviation_hovers=page.hovers, links=len(page.links),
    internal_targets=target_checks, css="exact source copy after generated banner", imports=imports,
    elapsed_seconds=round(time.monotonic()-start,6),
    limitations="No repository code import, generator, maintained test, browser, live-site, image-pixel, manuscript or source-research verification. No private review material. Focused regeneration and tests deferred to the nightly owner.")
(root / "static-result.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(result,ensure_ascii=False,indent=2))
