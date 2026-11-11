"""Frozen misc-index consistency and helper probes; run as a py/ entry point."""

import ast
from collections import deque
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from unittest.mock import patch
from urllib.parse import unquote, urljoin, urlsplit

from author_site import site_data
from author_site.entries import Anchor, Entry, EntryGroup, Italic, Section
from mb_cmn import paths

BASE = "068c9256038a98150d75ed3553a64745a49d38fb"
HEAD = "9006ea5ca465642faa60aaf13fdd9391780b57ef"
SITE = "https://bdenckla.github.io/MAM-basics/"
MISC = "MAM-with-doc/misc/"
ROOT = paths.repo_root()
OUT = Path(sys.argv[1])
timer = time.monotonic()


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def source(ref, path):
    return git("show", ref + ":" + path)


def tree(ref, path):
    return ast.parse(source(ref, path))


class DropDocstrings(ast.NodeTransformer):
    def generic_visit(self, node):
        node = super().generic_visit(node)
        if (
            isinstance(
                node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            )
            and node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)
        return node


def canonical(t):
    return ast.dump(DropDocstrings().visit(t), include_attributes=False)


identities = {}
for name in (
    git("diff", "--name-only", "-z", BASE, HEAD).decode().strip("\0").split("\0")
):
    for ref, side in [(BASE, "base"), (HEAD, "head")]:
        raw = source(ref, name)
        identities[side + "/" + name] = dict(
            blob=hashlib.sha1(
                b"blob " + str(len(raw)).encode() + b"\0" + raw
            ).hexdigest(),
            bytes=len(raw),
            sha256=hashlib.sha256(raw).hexdigest(),
        )

doc_only = [
    "py/author_misc/he_ws_intro_to_mam_gaya_text.py",
    "py/author_misc/review_of_hebrew_reader_for_the_pentateuch.py",
    "py/author_misc/urwotm_common.py",
]
for name in doc_only:
    assert canonical(tree(BASE, name)) == canonical(tree(HEAD, name)), name

old_main, new_main = [tree(ref, "py/main_authored.py") for ref in (BASE, HEAD)]
old_fun, new_fun = [
    next(
        n for n in t.body if isinstance(n, ast.FunctionDef) and n.name == "almost_main"
    )
    for t in (old_main, new_main)
]
old_pages = next(
    n
    for n in old_fun.body
    if isinstance(n, ast.Assign)
    and isinstance(n.targets[0], ast.Name)
    and n.targets[0].id == "index_entries"
)
new_pages = next(
    n
    for n in new_fun.body
    if isinstance(n, ast.Assign)
    and isinstance(n.targets[0], ast.Name)
    and n.targets[0].id == "pages"
)
assert (
    ast.dump(old_pages.value) == ast.dump(new_pages.value)
    and len(new_pages.value.elts) == 19
)
new_pages.targets[0].id = "index_entries"
new_fun.body = [
    n
    for n in new_fun.body
    if not (
        isinstance(n, ast.Assign)
        and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id == "linked"
    )
]
assert isinstance(old_fun.body[-1], ast.Expr) and isinstance(new_fun.body[-1], ast.Expr)
new_fun.body[-1] = old_fun.body[-1]
assert canonical(old_main) == canonical(new_main)
old_data, new_data = [tree(ref, "py/author_site/site_data.py") for ref in (BASE, HEAD)]
new_data.body = [
    n
    for n in new_data.body
    if not (isinstance(n, ast.FunctionDef) and n.name == "misc_fnames_linked")
    and not (
        isinstance(n, ast.Assign)
        and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id == "_MWD_MISC_RELATIVE"
    )
]
for n in new_data.body:
    if isinstance(n, ast.ImportFrom) and n.module == "author_site.entries":
        n.names = [x for x in n.names if x.name != "anchors_in"]
assert canonical(old_data) == canonical(new_data)

index_path = "gh-pages/" + MISC + "index.html"
old, new = [source(ref, index_path).decode() for ref in (BASE, HEAD)]
pattern = r'<li><a href="([^"]+)">.*?</a></li>'
old_items = list(re.finditer(pattern, old, re.S))
new_items = list(re.finditer(pattern, new, re.S))
old_names = [x[1] for x in old_items]
new_names = [x[1] for x in new_items]
assert len(old_names) == len(set(old_names)) == 19 and len(new_names) == 8
linked = site_data.misc_fnames_linked()
removed = [x for x in old_items if x[1] not in new_names]
assert len(removed) == 11 and {x[1] for x in removed} == set(old_names) & linked
assert [x.group() for x in new_items] == [
    x.group() for x in old_items if x[1] not in linked
]
reconstructed = old
for x in removed:
    reconstructed = reconstructed.replace(x.group() + "\n", "", 1)
assert reconstructed == new


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.hrefs = []
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == "a" and dict(attrs).get("href"):
            self.hrefs.append(dict(attrs)["href"])


top = Links((ROOT / "gh-pages/index.html").read_text()).hrefs
top_misc = {
    urlsplit(urljoin(SITE, h)).path.removeprefix("/MAM-basics/" + MISC)
    for h in top
    if urljoin(SITE, h).startswith(SITE + MISC)
}
assert set(old_names) & top_misc == {x[1] for x in removed}

# Traverse only committed local pages, prioritizing these targets. This records an
# actual path from the deployed root rather than assuming the misc index is linked.
targets = {MISC + n for n in old_names}
previous = {"index.html": None}
pending = deque(["index.html"])
found = set()
parsed_count = 0
while pending and found != targets:
    page = pending.popleft()
    found.update({page} & targets)
    local = ROOT / "gh-pages" / page
    if not local.is_file():
        continue
    parsed_count += 1
    children = []
    for href in Links(local.read_text(encoding="utf-8")).hrefs:
        url = urljoin(SITE + page, href)
        if not url.startswith(SITE):
            continue
        name = unquote(urlsplit(url).path.removeprefix("/MAM-basics/"))
        dest = ROOT / "gh-pages" / name
        if dest.is_dir():
            name = name.rstrip("/") + "/index.html"
        if (
            not name.endswith(".html")
            or name in previous
            or not (ROOT / "gh-pages" / name).is_file()
        ):
            continue
        previous[name] = page
        children.append(name)
    for child in sorted(children, key=lambda x: x not in targets, reverse=True):
        if child in targets:
            pending.appendleft(child)
        else:
            pending.append(child)
reachability = {}
for target in sorted(targets & set(previous)):
    route = []
    p = target
    while p is not None:
        route.append(p)
        p = previous[p]
    reachability[target] = list(reversed(route))
assert targets <= set(previous), sorted(targets - set(previous))

# Use the original helper with real immutable entry classes; restore the production
# SECTIONS object after each probe. No stand-in anchor walker or source edit.
pub = site_data._MWD_MISC
rel = site_data._MWD_MISC_RELATIVE
cases = [
    ("published", [Section((Entry(Anchor("p", pub + "one.html")),))], {"one.html"}),
    ("relative", [Section((Entry(Anchor("p", rel + "two.html")),))], {"two.html"}),
    (
        "fragments-and-dedup",
        [
            Section(
                (
                    Entry(Anchor("p", pub + "one.html#a")),
                    Entry(Anchor("p", rel + "one.html#b")),
                )
            )
        ],
        {"one.html"},
    ),
    (
        "nested",
        [
            Section(
                (
                    EntryGroup(
                        "g",
                        (
                            Entry(
                                Anchor(("title", Italic("book")), pub + "group.html"),
                                note=("note", Anchor("note", rel + "note.html")),
                            ),
                        ),
                    ),
                ),
                heading=Anchor("heading", pub + "heading.html#x"),
                intro=("lead", Anchor("intro", rel + "intro.html")),
            )
        ],
        {"group.html", "note.html", "heading.html", "intro.html"},
    ),
    (
        "nonmatching",
        [
            Section(
                (
                    Entry(
                        Anchor(
                            "outside", "https://example.org/MAM-with-doc/misc/x.html"
                        )
                    ),
                    Entry(Anchor("sibling", "MAM-with-doc/misc-other/x.html")),
                    Entry(Anchor("up", "../MAM-with-doc/misc/x.html")),
                    Entry(Anchor("local", "#fragment")),
                )
            )
        ],
        set(),
    ),
    ("empty", [], set()),
]
probes = []
original = site_data.SECTIONS
for name, sections, expected in cases:
    with patch.object(site_data, "SECTIONS", sections):
        actual = site_data.misc_fnames_linked()
        assert isinstance(actual, frozenset) and actual == expected, (
            name,
            actual,
            expected,
        )
    assert site_data.SECTIONS is original
    probes.append(dict(name=name, result="PASS", expected=sorted(expected)))

result = dict(
    result="PASS",
    base=BASE,
    head=HEAD,
    identities=identities,
    docstring_only_modules=doc_only,
    unchanged_generator_calls=19,
    old_index_entries=19,
    retained_entries=new_names,
    removed_entries=[x[1] for x in removed],
    retained_raw_entries_exact=True,
    whole_index_reconstructed=True,
    top_index_misc_pages=sorted(top_misc),
    reachability=reachability,
    reachability_pages_parsed=parsed_count,
    helper_probes=probes,
    elapsed_seconds=round(time.monotonic() - timer, 6),
    limits="Offline committed-code/link/byte consistency only; no browser, manuscript, source or editorial adjudication, broad-suite result or historical anchor advance.",
)
(OUT / "independent-check.json").write_text(
    json.dumps(result, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {k: v for k, v in result.items() if k not in {"identities", "reachability"}},
        indent=2,
        ensure_ascii=False,
    )
)
