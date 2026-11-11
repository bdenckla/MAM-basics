"""Offline endpoint accounting and real HTML-checker probes; run from py/."""

import ast
from collections import Counter
import copy
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

import check_html_syntax_and_sanity as htmlcheck
from mb_cmn import paths
from ws.ws_revision_metadata import chapter_hash

BASE = "9006ea5ca465642faa60aaf13fdd9391780b57ef"
HEAD = "7542d5636edeec99e7493249130df7a298b1144a"
ROOT = paths.repo_root()
OUT = Path(sys.argv[1])
timer = time.monotonic()


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def raw(ref, name):
    return git("show", ref + ":" + name)


def data(ref, name):
    return json.loads(raw(ref, name))


def changes(a, b, path=()):
    if type(a) != type(b):
        return [dict(path=list(path), before=a, after=b)]
    if isinstance(a, dict):
        if a.keys() != b.keys():
            return [dict(path=list(path), before=a, after=b)]
        return [d for k in a for d in changes(a[k], b[k], (*path, k))]
    if isinstance(a, list):
        if len(a) != len(b):
            return [dict(path=list(path), before=a, after=b)]
        return [
            d for i, (x, y) in enumerate(zip(a, b)) for d in changes(x, y, (*path, i))
        ]
    return [] if a == b else [dict(path=list(path), before=a, after=b)]


def no_docs(node):
    if isinstance(node, list):
        return [no_docs(n) for n in node]
    if not isinstance(node, dict):
        return node
    result = {k: no_docs(v) for k, v in node.items()}
    if result.get("tmpl_name") in {"נוסח", "נוסח עם הקשר מקרא על פי המסורה"}:
        for key in ("2", "הערת מקרא על פי המסורה"):
            if key in result.get("tmpl_params", {}):
                result["tmpl_params"][key] = "DOCUMENTATION BODY OMITTED FOR COMPARISON"
    return result


class DropDocs(ast.NodeTransformer):
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


def code(ref, name):
    return ast.dump(DropDocs().visit(ast.parse(raw(ref, name))))


assert git("rev-parse", "HEAD").decode().strip() == HEAD
inventory = json.loads((OUT / "input.json").read_bytes())
moves = [c for c in inventory["changes"] if c["status"].startswith("R")]
assert len(moves) == 36 and all(c["status"] == "R100" for c in moves)
move_ids = []
for move in moves:
    old, new = move["paths"]
    assert old.startswith("gh-pages/MAM-with-doc/misc/img/")
    assert new == "doc/mam-with-doc-unpublished-img/" + old.removeprefix(
        "gh-pages/MAM-with-doc/misc/img/"
    )
    a, b = raw(BASE, old), raw(HEAD, new)
    assert a == b and not (ROOT / old).exists()
    move_ids.append(
        dict(
            old=old,
            new=new,
            bytes=len(a),
            blob=git("rev-parse", HEAD + ":" + new).decode().strip(),
            sha256=hashlib.sha256(a).hexdigest(),
        )
    )
deleted = [c["paths"][0] for c in inventory["changes"] if c["status"] == "D"]
assert sorted(deleted) == [
    "gh-pages/MAM-with-doc/foi/poetic-verlen.csv",
    "gh-pages/MAM-with-doc/misc/index.html",
]
assert not (ROOT / deleted[1]).exists() and not (ROOT / deleted[0]).exists()

assert code(BASE, "py/main_mam_morphhb.py") == code(HEAD, "py/main_mam_morphhb.py")
for name in (
    "py/author_misc/review_of_hebrew_reader_for_the_pentateuch.py",
    "py/author_misc/urwotm_common.py",
    "py/author_misc/tsinnorit_and_the_xxd_in_bhs.py",
):
    assert code(BASE, name) == code(HEAD, name)


def gen_calls(ref):
    t = ast.parse(raw(ref, "py/main_authored.py"))
    f = next(
        n for n in t.body if isinstance(n, ast.FunctionDef) and n.name == "almost_main"
    )
    calls = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node):
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "gen_html_file"
            ):
                calls.append(ast.dump(node))
            self.generic_visit(node)

    Visitor().visit(f)
    return calls


assert gen_calls(BASE) == gen_calls(HEAD) and len(gen_calls(HEAD)) == 20
groups = [
    ("BB-2Samuel", "BA-Samuel", "כא"),
    ("C2-Jeremiah", "C2-Jeremiah", "לט"),
    ("FD-2Chronicles", "FC-Chronicles", "לה"),
]
corpus = {}
for book, group, chapter in groups:
    inp = "in/mam-ws/" + book + ".json"
    a, b = [data(ref, inp) for ref in (BASE, HEAD)]
    delta = changes(a, b)
    assert len(delta) == 1 and delta[0]["path"][0] == chapter
    metadata = data(HEAD, "in/mam-ws-revisions.json")
    # The authority's existing digest checks only local capture consistency, not live authenticity.
    records = [v for v in metadata.values() if isinstance(v, dict)]

    def find_record(n):
        if isinstance(n, dict):
            if n.get("sha256") == chapter_hash(b[chapter]):
                return [n]
            return [r for v in n.values() for r in find_record(v)]
        return []

    assert len(find_record(metadata)) == 1
    plus = "MAM-parsed/plus/" + group + ".json"
    p, q = [data(ref, plus) for ref in (BASE, HEAD)]
    pd = changes(p, q)
    assert len(pd) == (1 if book == "C2-Jeremiah" else 2)
    assert no_docs(p) == no_docs(q)
    npath = "out/near-aleppo/plus/" + group + ".json"
    assert no_docs(data(BASE, npath)) == no_docs(data(HEAD, npath))
    mirror_deltas = {}
    for prefix in (
        "out/mam-ws-parsed-fmt-2/",
        "out/mam-ws-bot/proto-fmt-2/",
        "out/mam-ws-bot/proto/",
    ):
        mirror_deltas[prefix] = changes(
            data(BASE, prefix + book + ".json"), data(HEAD, prefix + book + ".json")
        )
        assert len(mirror_deltas[prefix]) == (
            1 if prefix.endswith("/proto/") or book == "C2-Jeremiah" else 2
        )
    corpus[book] = dict(
        raw_changes=delta,
        plus_changes=pd,
        mirrored_changes=mirror_deltas,
        scripture_and_other_plus_fields="unchanged after omitting documentation bodies only",
        local_revision_metadata="matches maintained chapter_hash",
    )
ledger_name = "in/near-aleppo/doc-note-review.json"
a, b = [data(ref, ledger_name) for ref in (BASE, HEAD)]
assert [n["id"] for n in a["notes"]] == [n["id"] for n in b["notes"]]
changed = [(x, y) for x, y in zip(a["notes"], b["notes"]) if x != y]
assert len(changed) == 2
for x, y in changed:
    assert all(
        x[k] == y[k]
        for k in (
            "original_target",
            "near_target",
            "candidate_clause",
            "proposal_reason",
            "change_causes",
        )
    )
    assert (
        y["review"]["status"] == "reviewed"
        and x["review"]["presentation"] == "framed-mam"
        and y["review"]["presentation"] == "recast"
    )
assert sorted((n["ref"][0].split()[0], *n["ref"][1:]) for _, n in changed) == [
    ("BA-Samuel", "21", "19"),
    ("C2-Jeremiah", "39", "13"),
]
presentations = Counter(n["review"]["presentation"] for n in b["notes"])
assert presentations == {"recast": 1052, "framed-mam": 506}
special = data(HEAD, "in/mam-ws-special/manifest.json")["pages"]
for key, record in special.items():
    payload = (ROOT / "in/mam-ws-special" / (key + ".mediawiki")).read_bytes()
    assert (
        len(payload) == record["byte_size"]
        and hashlib.sha256(payload).hexdigest() == record["sha256"]
    )
old_log, new_log = [
    data(ref, "gh-pages/MAM-with-doc/change-log/unpinned-latest.json")
    for ref in (BASE, HEAD)
]
old_tree, new_tree = old_log.pop("new_tree"), new_log.pop("new_tree")
assert (
    old_log == new_log
    and new_tree == git("rev-parse", HEAD + ":MAM-parsed/plus").decode().strip()
)
assert raw(BASE, "gh-pages/MAM-with-doc/change-log/unpinned-latest.html").replace(
    old_tree.encode(), new_tree.encode()
) == raw(HEAD, "gh-pages/MAM-with-doc/change-log/unpinned-latest.html")
sigils = [data(ref, "out/sigil-inventory.json") for ref in (BASE, HEAD)]
sigil_counts = [{n["item"]: n["count"] for n in s["prose_tokens"]} for s in sigils]
sigil_delta = {
    k: [sigil_counts[0].get(k, 0), sigil_counts[1].get(k, 0)]
    for k in sigil_counts[0].keys() | sigil_counts[1].keys()
    if sigil_counts[0].get(k, 0) != sigil_counts[1].get(k, 0)
}
assert len(sigil_delta) == 4

probes = []


def probe(name, condition):
    assert condition, name
    probes.append(dict(name=name, result="PASS"))


def info(text):
    result = htmlcheck._HTMLInfo()
    result.feed(text)
    result.close()
    return result


with tempfile.TemporaryDirectory(prefix="html-probes-", dir=OUT) as tmp:
    deploy = Path(tmp) / "deploy"
    sub = deploy / "sub"
    sub.mkdir(parents=True)
    rootpage = deploy / "index.html"
    sourcepage = sub / "source.html"
    links = info(
        '<a href="local.html#p">a</a><a href="https://bdenckla.github.io/MAM-basics/sub/space%20name.html?q=1#f">b</a><a href="https://bdenckla.github.io/MAM-basics/sub/">c</a><a href="https://bdenckla.github.io/MAM-basics/">d</a><a href="https://example.org/sub/alien.html">e</a><a href="https://bdenckla.github.io/MAM-basics-other/sub/alien.html">f</a>'
    )
    targets = htmlcheck._linked_targets({sourcepage: links}, deploy)
    probe("relative href and fragment", sub / "local.html" in targets)
    probe("published href decoding/query/fragment", sub / "space name.html" in targets)
    probe(
        "published directory and root indexes",
        sub / "index.html" in targets and deploy / "index.html" in targets,
    )
    probe("foreign and similar-prefix sites excluded", len(targets) == 4)
    live, dead = sub / "live.html", sub / "dead.html"
    live.write_text("<p>live</p>")
    dead.write_text("<p>dead</p>")
    issue = htmlcheck._check_orphan_html(
        sub,
        [live, dead],
        {
            rootpage: info(
                '<a href="https://bdenckla.github.io/MAM-basics/sub/live.html#x">l</a>'
            )
        },
        deploy,
        recursive=True,
    )
    probe(
        "root-index links suppress only corresponding orphan",
        issue == ["orphan HTML (not linked from any page): dead.html"],
    )
    exempt = deploy / "MAM-with-doc/tsinnorit_oleh/tsinnorit_and_oleh_on_ivs.html"
    exempt.parent.mkdir(parents=True)
    exempt.write_text("<p>stub</p>")
    probe(
        "declared outside-link stub exemption",
        not htmlcheck._check_orphan_html(
            deploy / "MAM-with-doc", [exempt], {}, deploy, recursive=True
        ),
    )
    exempt.unlink()
    missing = htmlcheck._check_orphan_html(
        deploy / "MAM-with-doc", [], {}, deploy, recursive=True
    )
    probe(
        "missing declared exception is reported",
        len(missing) == 1 and "names a missing page" in missing[0],
    )
    probe(
        "exception staleness stays in recursive scope",
        not htmlcheck._check_orphan_html(sub, [], {}, deploy, recursive=True)
        and not htmlcheck._check_orphan_html(deploy, [], {}, deploy, recursive=False),
    )
    for name in ("data.json", "README.md"):
        (sub / name).write_text("nonempty")
    probe(
        "nonempty JSON and Markdown permitted",
        not htmlcheck._check_stale_files(sub, recursive=True),
    )
    (sub / "empty.json").write_text("")
    (sub / "old.csv").write_text("nonempty")
    stale = htmlcheck._check_stale_files(sub, recursive=True)
    probe(
        "empty accepted extension still reported",
        any("0 bytes" in s and "empty.json" in s for s in stale),
    )
    probe(
        "unexpected extension still reported",
        any("unexpected file type" in s and "old.csv" in s for s in stale),
    )
    probe(
        "deploy-relative helper excludes outside paths",
        htmlcheck._deploy_rel(sub / "live.html", deploy) == "sub/live.html"
        and htmlcheck._deploy_rel(Path(tmp) / "elsewhere.html", deploy) is None,
    )

result = dict(
    result="PASS",
    base=BASE,
    head=HEAD,
    change_records=inventory["change_records"],
    retained_image_moves=move_ids,
    removed_unused_files=deleted,
    generation_calls_preserved=20,
    morphhb_executable_ast="unchanged",
    corpus=corpus,
    ledger=dict(
        total=len(b["notes"]),
        unchanged=len(b["notes"]) - 2,
        changed_ids=[y["id"] for _, y in changed],
        presentations=presentations,
        targets="all original/near targets unchanged in the two changed rows; no stored pointing changes",
    ),
    special_manifest=dict(
        entries=len(special),
        byte_sizes_and_hashes="match retained captures; no live authenticity claim",
    ),
    change_log="tree metadata only; all declared changes unchanged",
    sigil_prose_count_deltas=sigil_delta,
    checker_probes=probes,
    elapsed_seconds=round(time.monotonic() - timer, 6),
    limits="Offline consistency and implementation checks only. No manuscript, live revision, upstream PR status, browser or new editorial/source claim; no historical overall anchor advance.",
)
(OUT / "independent-check.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n"
)
print(
    json.dumps(
        {
            k: v
            for k, v in result.items()
            if k not in {"retained_image_moves", "corpus"}
        },
        ensure_ascii=False,
        indent=2,
    )
)
