"""Verify the frozen two-comment endpoint using exact GitHub captures."""
import ast
import hashlib
import io
import json
import re
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "08abd66a1452ba654e19aefc55ea0589fcd936c3"
HEAD = "bc8d7ed3bbbabd0c23a56a76447ca7e76790f45f"
IDENTITIES = {
    "py/foi/foi_finals.py": (
        "5686df0cbfadfd36b27599c4f79123152f11f902",
        "bf8004ad95e51eca3656f7f8040a095d4ae1908d",
    ),
    "py/foi/slh_word_explanations.py": (
        "90e80eb6f2d121a65f398fa82a737bc893c9968d",
        "1b327500fda0057a85747af0fb7d0df57c8cf1e1",
    ),
}


def blob_hash(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def exact_capture(path, sha):
    raw = path.read_bytes()
    # The materialization writer may add one terminal newline. Identify the
    # exact bytes from Git's blob ID; do not normalize any other whitespace.
    for candidate in (raw, raw[:-1] if raw.endswith(b"\n") else raw):
        if blob_hash(candidate) == sha:
            return candidate.decode("utf-8")
    raise AssertionError((str(path), sha, blob_hash(raw)))


def significant_tokens(text):
    ignored = {tokenize.COMMENT, tokenize.NL}
    return [
        (token.type, token.string)
        for token in tokenize.generate_tokens(io.StringIO(text).readline)
        if token.type not in ignored
    ]


def apply_patch(base, patch):
    old = base.splitlines(keepends=True)
    out = []
    cursor = 0
    for line in patch.splitlines():
        if line.startswith("@@"):
            match = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            assert match, line
            start = int(match[1]) - 1
            out.extend(old[cursor:start])
            cursor = start
        elif line.startswith((" ", "-")):
            assert old[cursor] == line[1:] + "\n", (cursor, line)
            if line[0] == " ":
                out.append(old[cursor])
            cursor += 1
        elif line.startswith("+"):
            out.append(line[1:] + "\n")
        else:
            raise AssertionError(line)
    return "".join(out + old[cursor:])


compare = json.loads((ROOT / "compare-full.json").read_text())
assert compare["base_commit"]["sha"] == BASE
assert compare["merge_base_commit"]["sha"] == BASE
assert compare["status"] == "ahead" and compare["total_commits"] == 1
assert [c["sha"] for c in compare["commits"]] == [HEAD]
assert {f["filename"] for f in compare["files"]} == set(IDENTITIES)
results = []
for file in compare["files"]:
    name = file["filename"]
    base_sha, head_sha = IDENTITIES[name]
    before = exact_capture(ROOT / "base" / name, base_sha)
    after = exact_capture(ROOT / "head" / name, head_sha)
    assert file["sha"] == head_sha
    assert apply_patch(before, file["patch"]) == after
    assert ast.dump(ast.parse(before)) == ast.dump(ast.parse(after))
    assert significant_tokens(before) == significant_tokens(after)
    deltas = [line for line in file["patch"].splitlines() if line.startswith(("+", "-"))]
    assert all(line[1:].lstrip().startswith("#") for line in deltas)
    assert all(line[1:] == line[1:].rstrip() for line in deltas if line.startswith("+"))
    assert [c for c in before if "\u0590" <= c <= "\u05ff"] == [
        c for c in after if "\u0590" <= c <= "\u05ff"
    ]
    results.append({
        "path": name,
        "base_blob": base_sha,
        "head_blob": head_sha,
        "patch_reconstructs_exactly": True,
        "ast_equal": True,
        "non_comment_tokens_equal": True,
        "hebrew_codepoints_equal": True,
        "only_comment_lines_changed": True,
        "added_lines_have_no_trailing_whitespace": True,
    })
result = {
    "result": "pass",
    "window": {"base": BASE, "head": HEAD, "commits": 1, "paths": 2},
    "files": results,
    "scope": "Standard-library scratch comparison; no project tests or regeneration.",
}
(ROOT / "result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
