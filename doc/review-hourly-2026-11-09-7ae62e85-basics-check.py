"""Independent frozen endpoint checks. Pass the directory containing base/ and head/."""

import ast
from collections import Counter
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
IDENTITIES = {
    "base/book-of-job/out/custom-dict-freqs-ordered-by-count.json": "e19c15090057047a7c291c570fae9aaaac275dce",
    "head/book-of-job/out/custom-dict-freqs-ordered-by-count.json": "0b9d983945bb3c5b25fbf5883a97c0545b0d0ec4",
    "base/book-of-job/out/custom-dict-freqs-ordered-by-entry.json": "170849ef275fb770b77076979e18d9188cf10585",
    "head/book-of-job/out/custom-dict-freqs-ordered-by-entry.json": "94938a70e339fa4d0be5b3617fdefa6fb5589b48",
    "base/book-of-job/out/enriched-quirkrecs.json": "4eb2ee2221e7b3fdbff60e6aadf70de60e43c3ea",
    "head/book-of-job/out/enriched-quirkrecs.json": "13bfac8da442eb2dc6338f67b574489ec076057d",
    "base/gh-pages/book-of-job/jobn-details/3410.html": "c4c3b10297248123556769536aa4de5d3db97342",
    "head/gh-pages/book-of-job/jobn-details/3410.html": "be1f5cf436598879de177171675c76e01afedd3d",
    "base/py/author_boj_qr/qr_34.py": "7e8537e22c9451ef5670b2b9c6d1fbbb14908e7b",
    "head/py/author_boj_qr/qr_34.py": "3252eaeeeb6f804f845049d054b1be8c97bdadc3",
}


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def read(phase, name):
    return (ROOT / phase / name).read_text(encoding="utf-8")


def plain(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", s)).split())


verified = {}
for name, sha in IDENTITIES.items():
    raw = (ROOT / name).read_bytes()
    assert blob(raw) == sha, name
    verified[name] = {
        "blob": sha,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }

src = [read(p, "py/author_boj_qr/qr_34.py") for p in ["base", "head"]]
trees = [ast.parse(s) for s in src]
assigns = [
    {n.targets[0].id: n for n in t.body if isinstance(n, ast.Assign)} for t in trees
]
new_names = {"_COMMENT_PARA4", "_COMMENT_PARA5"}
assert assigns[1].keys() - assigns[0].keys() == new_names
paras = ["".join(ast.literal_eval(assigns[1][n].value)) for n in sorted(new_names)]
record = assigns[1]["RECORD_3410"].value
old_record = assigns[0]["RECORD_3410"].value
idx = [ast.literal_eval(k) for k in record.keys].index("qr-generic-comment")
old_idx = [ast.literal_eval(k) for k in old_record.keys].index("qr-generic-comment")
record.values[idx] = old_record.values[old_idx]
trees[1].body = [
    n
    for n in trees[1].body
    if not (isinstance(n, ast.Assign) and n.targets[0].id in new_names)
]
assert ast.dump(trees[0]) == ast.dump(trees[1])

records = [
    json.loads(read(p, "book-of-job/out/enriched-quirkrecs.json"))
    for p in ["base", "head"]
]
assert len(records[0]) == len(records[1]) == 160
changed = [(a, b) for a, b in zip(*records) if a != b]
assert len(changed) == 1
a, b = changed[0]
assert a["qr-cv"] == b["qr-cv"] == "34:10"
assert {k: v for k, v in a.items() if k != "qr-generic-comment"} == {
    k: v for k, v in b.items() if k != "qr-generic-comment"
}
ac, bc = a["qr-generic-comment"], b["qr-generic-comment"]
assert ac[:3] == bc[:3] and len(ac) == 4 and len(bc) == 5
assert bc[3:] == [{"_htel_tag": "p", "contents": [s]} for s in paras]
assert paras[0].startswith(ac[3])

pages = [
    read(p, "gh-pages/book-of-job/jobn-details/3410.html") for p in ["base", "head"]
]
old_marker = re.search(re.escape(ac[3]).replace(r"\ ", r"\s+"), pages[0])
assert old_marker
paragraphs = re.findall(r"<p>(.*?)</p>", pages[1], re.S)
assert all(sum(plain(p) == s for p in paragraphs) == 1 for s in paras)
added_html = [p for p in re.findall(r"<p>.*?</p>", pages[1], re.S) if plain(p) in paras]
assert len(added_html) == 2
first_start = pages[1].index(added_html[0])
first_end = first_start + len(added_html[0])
second_start = pages[1].index(added_html[1])
second_end = second_start + len(added_html[1])
assert pages[0][: old_marker.start()] == pages[1][:first_start]
assert pages[1][first_end:second_start] == "\n"
assert pages[0][old_marker.end() :] == pages[1][second_end:].removeprefix("\n")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_starttag(self, tag, attrs):
        if tag in {"a", "img", "link", "script"}:
            self.values.append((tag, attrs))


links = [Links(), Links()]
for p, l in zip(pages, links):
    l.feed(p)
assert links[0].values == links[1].values

freqs = [
    json.loads(read(p, "book-of-job/out/custom-dict-freqs-ordered-by-entry.json"))
    for p in ["base", "head"]
]
for p, d in zip(["base", "head"], freqs):
    assert d == json.loads(
        read(p, "book-of-job/out/custom-dict-freqs-ordered-by-count.json")
    )
actual = {
    (group, word): freqs[1][group][word] - count
    for group, words in freqs[0].items()
    for word, count in words.items()
    if freqs[1][group][word] != count
}
assert all(freqs[0][g].keys() == freqs[1][g].keys() for g in freqs[0])
before, after = ac[3], " ".join(paras)


def tokens(s):
    return Counter(
        re.findall(r"\bμ[ALY](?:['’]s)?|[\u05d0-\u05ea]+", s.replace(chr(0x2019), "'"))
    )


delta = tokens(after) - tokens(before)
assert {word: n for (_, word), n in actual.items()} == delta
assert len(actual) == 9

result = {
    "result": "PASS",
    "endpoint": "bc8d7ed3..7ae62e85",
    "exact_blobs": verified,
    "checks": {
        "python_ast": "Only two paragraph constants and their use in the Job 34:10 comment change.",
        "records": 160,
        "changed_records": 1,
        "all_other_record_fields": "Identical",
        "source_json_html_paragraphs": 2,
        "outside_paragraphs": "Byte-identical except the one generated newline after the new final paragraph",
        "links_and_images": "Identical",
        "dictionary_deltas": {g + "/" + w: n for (g, w), n in actual.items()},
    },
    "limits": [
        "Consistency checks do not independently verify Ben's manuscript readings.",
        "Real producers and repository tests belong to the separate execution receipt.",
        "No browser, live-site, manuscript image or broad suite check.",
    ],
}
print(json.dumps(result, ensure_ascii=False, indent=2))
