"""Regenerate the authored site and independently bound the declared public delta."""

import ast
import copy
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

WORK = Path("/workspace/scratch/screen-e4533ff6-checkout")
OUT = Path("/workspace/scratch/screen-e4533ff6-artifacts")
PYTHON = "/workspace/MAM-basics/.venv/bin/python"
HEAD = "e4533ff6844355d3dcb47f9b7e2e4d3d926e9267"
BASE = "9a0ec239d7f45faff7487e4dfae8369f269a5f2d"


def git(*args):
    return subprocess.check_output(["git", "-C", str(WORK), *args])


def command(label, args):
    started = time.perf_counter()
    p = subprocess.run(args, cwd=WORK, capture_output=True, encoding="utf-8")
    record = dict(
        command=args,
        cwd=str(WORK),
        exit_code=p.returncode,
        elapsed_seconds=round(time.perf_counter() - started, 6),
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


assert git("rev-parse", "HEAD").decode().strip() == HEAD and not git(
    "status", "--porcelain=v1", "-z"
)
command(
    "authored-generator", [PYTHON, "py/main_authored.py", "gen-site", "--trust-surveys"]
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
started = time.perf_counter()
source = "py/author_site/post_stress_meteg_post_silluq_page.py"
before = ast.parse(git("show", BASE + ":" + source))
after = ast.parse(git("show", HEAD + ":" + source))
added = {"_ROM_YORED": "yored", "_ROM_DEXI": "dexi"}
for name, value in added.items():
    matches = [
        n
        for n in after.body
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)
    ]
    assert (
        len(matches) == 1
        and ast.unparse(matches[0].value) == f"_author_romanization('{value}')"
    )
    after.body.remove(matches[0])
tuples = [
    n
    for n in ast.walk(after)
    if isinstance(n, ast.Tuple)
    and n.elts
    and isinstance(n.elts[0], ast.Constant)
    and isinstance(n.elts[0].value, str)
    and n.elts[0].value.startswith("In this document, we set aside the broader set")
]
assert len(tuples) == 1
items = tuples[0].elts
index = next(
    i for i, n in enumerate(items) if isinstance(n, ast.Name) and n.id == "_ROM_YORED"
)
assert ast.literal_eval(items[index + 1]) == ", "
del items[index : index + 2]
index = next(
    i for i, n in enumerate(items) if isinstance(n, ast.Name) and n.id == "_ROM_DEXI"
)
assert ast.literal_eval(items[index - 1]) == ", and "
del items[index - 1 : index + 1]
index = next(
    i for i, n in enumerate(items) if isinstance(n, ast.Name) and n.id == "_ROM_TARHA"
)
assert ast.literal_eval(items[index - 1]) == ", "
items[index - 1] = ast.Constant(value=", and ")
assert ast.dump(before) == ast.dump(after)
path = "gh-pages/post-stress-meteg-post-silluq.html"
old, new = [git("show", c + ":" + path).decode("utf-8") for c in (BASE, HEAD)]
pattern = r"similar stroke can represent:\n(.*?)\. In prose verses,"
oldmatch, newmatch = [re.search(pattern, s, re.S) for s in (old, new)]
assert oldmatch and newmatch
assert re.findall(r'<span class="romanized">(.*?)</span>', newmatch[1]) == [
    "merkha",
    "yored",
    "mayela",
    "tipeḥa",
    "tarḥa",
    "deḥi",
]
assert re.findall(r'<span class="romanized">(.*?)</span>', oldmatch[1]) == [
    "merkha",
    "mayela",
    "tipeḥa",
    "tarḥa",
]
assert old.replace(oldmatch[0], newmatch[0], 1) == new
assert re.findall(r"[\u0590-\u05ff]+", old) == re.findall(r"[\u0590-\u05ff]+", new)
result = dict(
    result="PASS",
    source_ast="Exact base AST recovered after removing only two new romanization assignments and two list elements with their separators.",
    html="Only the declared six-name list replaces the old four-name list; every other HTML byte and all Hebrew codepoints unchanged.",
    generated_html_sha256=hashlib.sha256(new.encode()).hexdigest(),
    elapsed_seconds=round(time.perf_counter() - started, 6),
    output_differences=[],
    owner_test_count="Owner-reported 19 is attributed; actual selected independent test count is in focused-tests.log.",
)
(OUT / "independent-delta.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False, indent=2))
