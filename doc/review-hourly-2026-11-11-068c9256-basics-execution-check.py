"""Execute only the maintained page/omission checks at the exact frozen public head."""

import ast
import copy
from collections import Counter
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import time
from urllib.parse import unquote, urlsplit

WORK = Path("/workspace/scratch/basics-068c9256-checkout")
OUT = Path("/workspace/scratch/basics-068c9256-artifacts")
PYTHON = "/workspace/MAM-basics/.venv/bin/python"
BASE = "e4533ff6844355d3dcb47f9b7e2e4d3d926e9267"
HEAD = "068c9256038a98150d75ed3553a64745a49d38fb"
URL = "https://bdenckla.github.io/MAM-basics/MAM-for-Sefaria/#meteg-after-silluq"


def git(*args):
    return subprocess.check_output(["git", "-C", str(WORK), *args])


def command(label, args):
    start = time.perf_counter()
    p = subprocess.run(args, cwd=WORK, capture_output=True, encoding="utf-8")
    record = dict(
        command=args,
        cwd=str(WORK),
        exit_code=p.returncode,
        elapsed_seconds=round(time.perf_counter() - start, 6),
        recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=git("status", "--porcelain=v1", "-z").decode(),
    )
    (OUT / (label + ".log")).write_text(p.stdout + p.stderr, encoding="utf-8")
    (OUT / (label + ".json")).write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    if record["status"]:
        (OUT / (label + "-unexpected.diff")).write_bytes(git("diff", "--binary"))
    print(json.dumps(dict(stage=label, **record)), flush=True)
    assert p.returncode == 0 and not record["status"], label


assert git("rev-parse", "HEAD").decode().strip() == HEAD
assert not git("status", "--porcelain=v1", "-z")
command("authored-site", [PYTHON, "py/main_authored.py", "gen-site", "--trust-surveys"])
command(
    "sefaria-doc-omission", [PYTHON, "py/main_authored.py", "gen-mam-for-sefaria-doc"]
)
command(
    "focused-tests",
    [
        PYTHON,
        "py/main_test.py",
        "py/tests/test_post_stress_meteg_annotations.py",
        "py/tests/test_post_stress_meteg_plain_word.py",
        "py/tests/test_prose_mark_order.py",
        "py/tests/test_prose_conventions.py",
        "py/tests/test_transliterations.py",
        "py/tests/test_sefaria_silluq_documentation.py",
        "-q",
    ],
)
command(
    "source-black",
    [
        PYTHON,
        "-m",
        "black",
        "--check",
        "py/author_site/post_stress_meteg_post_silluq_page.py",
    ],
)
start = time.perf_counter()
source = "py/author_site/post_stress_meteg_post_silluq_page.py"
old_source, new_source = [git("show", c + ":" + source) for c in (BASE, HEAD)]
old_tree, new_tree = map(ast.parse, (old_source, new_source))
added = [
    n
    for n in new_tree.body
    if isinstance(n, ast.Assign)
    and any(
        isinstance(t, ast.Name) and t.id == "_MAM_FOR_SEFARIA_SILLUQ_URL"
        for t in n.targets
    )
]
assert len(added) == 1 and ast.literal_eval(added[0].value) == URL
new_tree.body.remove(added[0])
functions = [
    {n.name: n for n in t.body if isinstance(n, ast.FunctionDef)}
    for t in (old_tree, new_tree)
]
assert functions[0].keys() == functions[1].keys()
changed = [
    name
    for name in functions[0]
    if ast.dump(functions[0][name]) != ast.dump(functions[1][name])
]
assert changed == ["build_post_silluq_body"]
returns = [
    next(
        n
        for n in ast.walk(f["build_post_silluq_body"])
        if isinstance(n, ast.Return) and isinstance(n.value, ast.List)
    )
    for f in functions
]
left, right = [r.value.elts for r in returns]
assert len(right) == len(left) + 1
assert ast.dump(ast.List(elts=left[:-2], ctx=ast.Load())) == ast.dump(
    ast.List(elts=right[:-3], ctx=ast.Load())
)
assert (
    isinstance(right[-3], ast.Call)
    and ast.unparse(right[-3].func) == "mb_html.heading_level_2"
)
assert ast.literal_eval(right[-3].args[0]) == "φ4 — The MAM dataset's use of Aleppo"
assert all(
    isinstance(n, ast.Call) and ast.unparse(n.func) == "mb_html.para"
    for n in right[-2:]
)
returns[1].value.elts[-3:] = copy.deepcopy(left[-2:])
assert ast.dump(old_tree) == ast.dump(new_tree)
assert re.findall(rb"[\xD6\xD7][\x80-\xBF]", old_source) == re.findall(
    rb"[\xD6\xD7][\x80-\xBF]", new_source
)
page = "gh-pages/post-stress-meteg-post-silluq.html"
old_page, new_page = [git("show", c + ":" + page).decode("utf-8") for c in (BASE, HEAD)]
marker = '<h2 id="mam-policy-footnote">'
assert old_page.count(marker) == new_page.count(marker) == 1
assert old_page.split(marker)[0] == new_page.split(marker)[0]
assert old_page[old_page.index("</body>") :] == new_page[new_page.index("</body>") :]
assert re.findall(r"[\u0590-\u05ff]+", old_page) == re.findall(
    r"[\u0590-\u05ff]+", new_page
)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.case_refs = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "href" in attrs:
            self.hrefs.append(attrs["href"])
        if tag == "th" and "data-osis-id" in attrs:
            self.case_refs.append(attrs["data-osis-id"])


pages = []
for raw in (old_page, new_page):
    parser = Links()
    parser.feed(raw)
    parser.close()
    assert len(parser.ids) == len(set(parser.ids))
    pages.append(parser)
assert pages[0].ids == pages[1].ids
assert not Counter(pages[0].hrefs) - Counter(pages[1].hrefs)
assert Counter(pages[1].hrefs) - Counter(pages[0].hrefs) == Counter({URL: 1})
url = urlsplit(URL)
assert url.netloc == "bdenckla.github.io" and url.path.startswith("/MAM-basics/")
relative = unquote(url.path.removeprefix("/MAM-basics/"))
target = WORK / "gh-pages" / relative / "index.html"
assert target.is_file()
target_raw = target.read_bytes()
target_parser = Links()
target_parser.feed(target_raw.decode("utf-8"))
target_parser.close()
assert target_parser.ids.count(url.fragment) == 1
assert target_parser.ids.count("meteg-after-silluq-cases") == 1
assert sorted(target_parser.case_refs) == ["1Kgs.7.37", "Job.4.12"]
assert target_raw == git("show", HEAD + ":gh-pages/MAM-for-Sefaria/index.html")
result = dict(
    result="PASS",
    source_head=HEAD,
    delta="Only the new URL constant and final phi4 heading/two paragraphs differ; every other source AST and HTML byte outside phi4 is unchanged.",
    hebrew_codepoints_preserved=True,
    old_ids_and_links_preserved=True,
    only_added_link=URL,
    target=dict(
        path="gh-pages/MAM-for-Sefaria/index.html",
        blob=git("rev-parse", HEAD + ":gh-pages/MAM-for-Sefaria/index.html")
        .decode()
        .strip(),
        bytes=len(target_raw),
        sha256=hashlib.sha256(target_raw).hexdigest(),
        fragment=url.fragment,
        case_refs=target_parser.case_refs,
    ),
    omission_check="Maintained gen-mam-for-sefaria-doc executes author_misc.mam4sef_survey.survey/_silluq_cases against committed CSV/CSV-AJF and canonical MAM-simple; selected maintained documentation test independently compares all annotation branches/exporter projections to the rendered case table.",
    page_sha256=hashlib.sha256(new_page.encode()).hexdigest(),
    elapsed_seconds=round(time.perf_counter() - start, 6),
    output_differences=[],
    limits="Committed public data/structural consistency only; no manuscript/editorial, live website/browser, fresh export, broad-suite or historical-anchor claim. Owner-reported 20 tests remains attributed; actual selection is recorded separately.",
)
(OUT / "independent-delta-target.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False, indent=2))
