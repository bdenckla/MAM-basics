import ast
import collections
import copy
import json
from pathlib import Path

ROOT = Path(__file__).parent
H = ROOT / "head"


def selected(path, names, env):
    tree = ast.parse(path.read_text())
    nodes = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name in names) or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets))]
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), env)


env = {}
selected(H / "py/author_boj_util/short_id_etc.py", {"short_id"}, env)
selected(H / "py/author_boj_util/noted_by.py", {"_STARTSWITH_N", "_STARTSWITH_X", "startswith_n", "startswith_x"}, env)
path = H / "py/author_boj_util/get_qr_groups.py"
tree = ast.parse(path.read_text())
selected(path, {n.name for n in tree.body if isinstance(n, ast.FunctionDef)} | {"_T30", "_FILTER_FNS"}, env)
selected(H / "py/author_boj/job2_main_article.py", {"PRESENTED_IN_PROSE"}, env)
records = json.loads((H / "book-of-job/out/enriched-quirkrecs.json").read_text())
groups = collections.defaultdict(list)
for record in records:
    groups[env["get_pgroup"](record)].append(record)
prose = env["PRESENTED_IN_PROSE"]
listed = set(groups) - set(prose.values())
check = env["check_every_quirkrec_presented"]
outcomes = []


def reject(name, operation, expected):
    try:
        operation()
    except ValueError as error:
        message = str(error)
        assert all(fragment in message for fragment in expected), message
        outcomes.append({"probe": name, "result": "pass: rejected with ValueError", "message": message})
    else:
        raise AssertionError(f"{name}: did not reject")


unmatched = copy.deepcopy(next(r for r in records if env["short_id"](r) == "2908"))
unmatched["nbd"] = dict(env["_STARTSWITH_X"])
reject("no matching presentation group", lambda: env["get_pgroup"](unmatched), ["2908 matches 0 presentation groups", "not 1"])
reject("missing prose declarations", lambda: check(groups, listed, {}), ["2908 (g:tbhq_and_twlc)", "3115 (g:xbhq_and_twlc)"])
unlisted_ids = [env["short_id"](r) for r in groups["g:adm"]]
reject("unlisted existing group", lambda: check(groups, listed - {"g:adm"}, prose), [sid + " (g:adm)" for sid in unlisted_ids])
listed_record = groups["g:adm"][0]
stale_id = env["short_id"](listed_record)
reject("stale prose declaration", lambda: check(groups, listed, {**prose, stale_id: "g:adm"}), ["Declared as presented in prose but not in an unlisted group", stale_id])
(ROOT / "negative-probes-result.json").write_text(json.dumps(outcomes, indent=2) + "\n")
print(json.dumps(outcomes, indent=2))
