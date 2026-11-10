"""Check the complete bounded public source/output delta, without source adjudication."""

import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(sys.argv[1])
OUT = Path(sys.argv[2])
BASE = "7ae62e8589f7ce9d7d4e9a05cc5f146ac9294a8f"
HEAD = "73fbf0406b8cf843b2aabcbb8ef0b558d0fa7148"


def git(*args):
    return subprocess.check_output(["git", "-C", str(REPO), *args])


def get(commit, path):
    return git("show", commit + ":" + path)


paths = [
    p.decode() for p in git("diff", "--name-only", "-z", BASE, HEAD).split(b"\0") if p
]
assert len(paths) == 7
identities = {}
for side, commit in (("base", BASE), ("head", HEAD)):
    for path in paths:
        raw = get(commit, path)
        expected = git("rev-parse", commit + ":" + path).decode().strip()
        assert (
            hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            == expected
        )
        target = OUT / "source-snapshots" / side / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        identities[side + "/" + path] = dict(
            blob=expected, sha256=hashlib.sha256(raw).hexdigest()
        )
trees = [ast.parse(get(c, "py/author_boj_qr/qr_34.py")) for c in (BASE, HEAD)]
assignments = [
    {
        n.targets[0].id: n
        for n in t.body
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
    }
    for t in trees
]
old = assignments[0]["_COMMENT_PARA5"].value
new = assignments[1]["_COMMENT_PARA5"].value
assert len(new.elts) == len(old.elts) + 4
addition = "".join(ast.literal_eval(x) for x in new.elts[-4:])
del new.elts[-4:]
assert ast.dump(trees[0]) == ast.dump(trees[1])
article = [get(c, "py/author_boj/job2_main_article.py").decode() for c in (BASE, HEAD)]
assert (
    article[0].replace(
        '"It emphasizes manuscript quantity over quality."',
        '"Its notes emphasize manuscript quantity over quality."',
    )
    == article[1]
)
records = [
    json.loads(get(c, "book-of-job/out/enriched-quirkrecs.json")) for c in (BASE, HEAD)
]
assert len(records[0]) == len(records[1])
changed = [i for i, (a, b) in enumerate(zip(*records)) if a != b]
assert len(changed) == 1 and records[0][changed[0]]["qr-cv"] == "34:10"
old_record, new_record = [copy.deepcopy(records[s][changed[0]]) for s in (0, 1)]
assert old_record.keys() == new_record.keys()
comment_keys = [k for k in old_record if old_record[k] != new_record[k]]
assert comment_keys == ["qr-generic-comment"]
before = json.dumps(old_record["qr-generic-comment"], ensure_ascii=False)
after = json.dumps(new_record["qr-generic-comment"], ensure_ascii=False)
assert after.replace(addition, "", 1) == before
freq_paths = [p for p in paths if "custom-dict-freqs" in p]
frequency_deltas = {}
for path in freq_paths:
    old_freq, new_freq = [json.loads(get(c, path)) for c in (BASE, HEAD)]
    assert old_freq.keys() == new_freq.keys()
    changes = []
    for category in old_freq:
        assert old_freq[category].keys() == new_freq[category].keys()
        for key in old_freq[category]:
            if old_freq[category][key] != new_freq[category][key]:
                changes.append(
                    [category, key, old_freq[category][key], new_freq[category][key]]
                )
    assert len(changes) == 1 and changes[0][2] + 1 == changes[0][3]
    assert changes[0][1] in addition
    frequency_deltas[path] = changes
html_paths = [p for p in paths if p.endswith(".html")]
for path in html_paths:
    a, b = [get(c, path).decode() for c in (BASE, HEAD)]
    for pattern in (r"<a\b[^>]*>", r"<img\b[^>]*>"):
        assert re.findall(pattern, a) == re.findall(pattern, b)
    fold = lambda text: re.sub(r"\s+", " ", text)
    if path.endswith("3410.html"):
        assert fold(a).replace(
            "פתח-like part.</p>", "פתח-like part." + addition + "</p>"
        ) == fold(b)
    else:
        assert (
            a.replace(
                "It emphasizes manuscript quantity over quality.",
                "Its notes emphasize manuscript quantity over quality.",
            )
            == b
        )
result = dict(
    result="PASS",
    window=dict(base=BASE, head=HEAD),
    identities=identities,
    checks=dict(
        paths=len(paths),
        preserved_other_records=len(records[0]) - 1,
        changed_record="34:10",
        changed_fields=comment_keys,
        added_comment=addition,
        dictionary_deltas=frequency_deltas,
        html="Exactly the declared comment addition and article sentence; all link/image tags unchanged.",
        limits="No manuscript/source interpretation or browser claim.",
    ),
)
(OUT / "native-result.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n"
)
(OUT / "endpoint.patch").write_bytes(
    git("diff", "--binary", "--full-index", BASE, HEAD)
)
print(json.dumps(result["checks"], ensure_ascii=False, indent=2))
