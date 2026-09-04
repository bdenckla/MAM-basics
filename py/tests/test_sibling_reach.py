"""Guard: the sibling repos this tree reaches are exactly the ones declared here.

WHAT WENT WRONG, AND WHY A LINT IS THE RIGHT SHAPE OF ANSWER

MAM-basics resolves a sibling clone by more than one mechanism, and the survey method
of record covered only the first.  ``doc/PLAN-evacuate-public-repos-programme.md``, in
its "What still forces a forest" section, recorded the method as
``grep -rn "sibling_repo(\\|require_sibling(" py/`` plus a read of the ``py/*_paths.py``
modules.  That grep cannot see a cwd-relative ``"../<repo>"`` literal at all, and it
reports a variable rather than a repo wherever the name is not spelled at the call.
Since 2026-09-04 that section carries neither the survey nor its eleven-row table: it
points here, and this declaration is the answer it used to state by hand.

The consequence was not hypothetical.  ``mb_misc/write_utils.py``'s ``bkg_path`` builds
``f"../{mam_for_xxx}"`` from ``variant.get("variant-mam-for-xxx") or "MAM-for-Sefaria"``.
It never calls ``mb_cmn.paths``, so ``REPOS_ROOT`` does not reach it, and from a worktree
it resolves under ``.claude/worktrees/``.  ``main_mam_simple.py``'s ``_VARIANT_COMMON``
sets that key to ``"MAM-simple"`` and routes the identical function there, which the
programme's table did not record -- it attributed the literal to MAM-for-Sefaria alone.
On 2026-09-04 a mega run from a worktree wrote 216 MAM-simple and 160 MAM-for-Sefaria
files into ``.claude/worktrees/``, exited 0, and left MAM-OSIS unchanged because the
later steps read the real, stale MAM-simple.  ``py/main_0_mega.py``'s module docstring
records the incident.

So "which siblings does the tree reach?" is a decidable property of the source text --
a mechanical lint over the tree, the second of the two test shapes CLAUDE.md sanctions --
and one declaration replaces a hand-maintained table that goes stale silently.

THE DESIGN DECISION: WHAT COUNTS AS A REACHING SITE, AND WHY NOT A GREP

A naive grep for ``"../<repo>"`` over ``py/`` returns about fifty hits and the great
majority construct no path: 22 ``py/author_misc/*.py`` module docstrings reading
"Output goes to ../MAM-parsed/gh-pages/<name>.html" (measured 2026-09-04, one
occurrence each), ``pipeline_graph/pipeline_graph_spec.py``'s deliberate display
labels, and assorted comments.  A lint that flags those is useless and gets deleted,
so this one is an AST pass with three deliberate narrowings:

1. COMMENTS ARE INVISIBLE TO ``ast`` and docstrings are cheap to drop -- a module,
   class or function whose first statement is a string constant.  That alone removes
   46 of the 109 ``../`` constants in the tree, and every stale ``../masorah-books``
   and ``../al-hatorah`` citation CLAUDE.md leaves standing on purpose.
2. A CWD-RELATIVE LITERAL IS CONSIDERED ONLY WHEN IT STARTS WITH ``../``.  Prose
   mentions a sibling mid-sentence (``argparse`` help in ``subcommands/diff_mpp.py``
   says "Old git revision (in ../MAM-parsed repo)"); a path does not.  The shape this
   deliberately misses is a path built as ``f"{x}/../MAM-parsed"``, which nothing here
   writes.
3. THE VOCABULARY IS DERIVED, NOT DECLARED.  ``../img/``, ``../svg/``, ``../misc/``
   and ``../aleppo-pages/`` are site-relative URLs, not repos, and no list of them is
   maintained: a ``../X`` literal is considered only when X is a repo name already
   known to the tree -- the ``all-repos.code-workspace`` roster, plus every name the
   two recognizers below resolve.  This is NOT derived from ``SIBLINGS_REACHED``, or
   deleting an entry would stop the sites for it being recognized and the removal
   would look consistent with itself.

What this narrowing costs: a brand-new sibling reached ONLY by a cwd-relative literal,
and named in no workspace file and by no ``paths`` call, is not seen.  Such a clone is
on no machine (``in/repo_maintenance_policy.json``'s ``gitrepos_setup_rule``), so the
literal could not resolve there anyway.

A FALSE POSITIVE IS SUPPRESSED BY NAMING THE SITE, NEVER BY WEAKENING THE CHECK.
``_NOT_A_SIBLING_PATH`` below is keyed by (file, literal) rather than by line, so it
does not drift when a file is edited, and every entry carries its reason.  A site the
scan cannot resolve to a repo name is a HARD FAILURE rather than a skip: it names the
site and asks for an entry, so an unrecognized new mechanism cannot pass quietly.

THE FIVE MECHANISMS, ALL OF WHICH THIS COVERS

* ``sibling_repo("X")`` / ``require_sibling("X", ...)`` -- the sanctioned API.
* The same calls with the name in a variable: ``ac_paths.py`` and ``cam1753_paths.py``
  pass ``DATA_REPO_NAME``, ``redirect_stubs/stubs.py`` passes ``repo.source_repo`` from
  its ``REDIRECT_REPOS`` table, and ``main_0_mega.py``'s mega guard passes the ``name``
  of a loop over ``_CWD_RELATIVE_WRITE_TARGETS``.  The survey's grep finds these
  lines and cannot read a repo off them.  Three in-file shapes are resolved here, with
  no import and no dataflow tracing: a module constant's assignment, the keyword
  arguments that build the table being iterated, and the collection a for-loop walks.
* ``repos_root() / "X"``, which honours ``REPOS_ROOT`` but bypasses both the per-repo
  ``REPO_<NAME>_DIR`` override and ``require_sibling``'s message.  ``main_0_mega.py``
  builds five subprocess ``cwd``s this way, naming three repos: MAM-parsed,
  MAM-simple and MAM-private.
* A name arriving from a tracked data file, which no in-file lookup can resolve:
  ``vendoring/`` and ``tests/test_vendoring_policy_paths.py`` take theirs from
  ``in/vendoring_policy.json``.  ``_DYNAMIC_NAME_SOURCES`` names those four sites.
* Cwd-relative ``"../X"``, the mechanism the survey's grep cannot see -- as a plain
  literal, and as an ``f"../{name}"`` whose first segment is interpolated.  For the
  interpolated shape the names come from a declared source (``write_utils.bkg_path``)
  or from the same three in-file shapes, filtered by the vocabulary so that a
  site-relative href interpolating a page name contributes nothing.

WHY THE CWD-RELATIVE SITES ARE NOT DEFECTS TO FIX

CLAUDE.md's "Running tests -- always from the repo root" section names four files that
are vendored verbatim into sibling repos and "intentionally keep their existing
cwd-relative or self-contained ``__file__``-relative logic instead, so they stay
portable when copied elsewhere without also requiring ``mb_cmn/paths.py`` to travel
with them".  Three of the four carry such a literal today, and ``paths.mam_parsed_path``'s
docstring states the doctrine behind the first: "THE CALLER SUPPLIES THIS PATH BECAUSE
THE READER CANNOT."  So the assertion here is NOT "there are no cwd-relative literals".
It is "the siblings reached, by any mechanism, are exactly these" -- and a sanctioned
cwd-relative default contributes its repo to that set like any other route.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_sibling_reach.py
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
from pathlib import Path

from mb_cmn import paths

# ---------------------------------------------------------------------------
# THE DECLARATION.  One entry per sibling repo this tree resolves a path into,
# saying WHY it is reached -- which is the thing a route count cannot tell you.
#
# REMOVING A LANE?  Delete the entry whose last route you removed.  If any route
# survives, the test fails naming the repo and the surviving sites, so a
# half-finished removal cannot be mistaken for a finished one.  Expect this list
# to SHRINK as the third stage's remaining lanes land and, if Ben approves it, a
# fourth stage covering the five MAM data products.
# ---------------------------------------------------------------------------
SIBLINGS_REACHED: dict[str, str] = {
    "MAM-parsed": (
        "The corpus almost everything here reads: paths.mam_parsed_path and"
        " mam_parsed_plus_dir, a main_0_mega subprocess cwd, and"
        " read_books_from_mam_parsed_plus.py's vendored '../MAM-parsed' default."
    ),
    "MAM-simple": (
        "Written by main_mam_simple.py through write_utils.bkg_path's"
        " cwd-relative f'../{mam_for_xxx}', read back by mam4sef_or_ajf.py's"
        " vendored '../MAM-simple' default and by paths.mam_simple_dir, and a"
        " vendoring-audit destination."
    ),
    "MAM-for-Sefaria": (
        "Written by write_utils.bkg_path's 'MAM-for-Sefaria' fallback and by"
        " nothing else -- it has no paths-API route at all, so this cwd-relative"
        " default is its ONLY route."
    ),
    "MAM-OSIS": "Written by the OSIS generators through paths.sibling_repo.",
    "MAM-with-doc": "Holds the change-log and doc trees the diff reports write into.",
    "MAM-private": (
        "paths.al_hatorah_phonetic_dir reads MAM-private/al-hatorah's Phonetic MAM"
        " as the oracle for accgram.final_stress, and main_0_mega runs the"
        " near-aleppo census there.  Its vendoring audit was given up on"
        " 2026-09-04 (abb03ec4), which removed a third route but not these two."
    ),
    "codex-index-aleppo": "ac_paths.DATA_REPO_NAME -- the Aleppo page/word image corpus.",
    "codex-index-cam1753": (
        "cam1753_paths.DATA_REPO_NAME -- the Cambridge 1753 image corpus."
    ),
    "diffable-pointed-hebrew": (
        "A vendoring-audit destination in in/vendoring_policy.json, reached by"
        " vendoring/ and by tests/test_vendoring_policy_paths.py."
    ),
    "wlc-utils": (
        "redirect_stubs/stubs.py only, to publish the frozen redirect stubs."
        "  CLAUDE.md: the clone belongs on no machine, and that one-time program"
        " raises with the git clone command when it is absent."
    ),
    "UXLC-utils": "redirect_stubs/stubs.py only -- as wlc-utils, a redirect host.",
    "holman-ketiv-qere": "redirect_stubs/stubs.py only -- as wlc-utils, a redirect host.",
    "book-of-job": "redirect_stubs/stubs.py only -- as wlc-utils, a redirect host.",
}

# ---------------------------------------------------------------------------
# Suppressions.  Each names a site and says why it constructs no sibling path.
# ---------------------------------------------------------------------------

# (file, literal) -> reason.  Keyed by the literal, not the line, so an edit above
# it does not move the key; one entry covers every occurrence in that file.
_NOT_A_SIBLING_PATH: dict[tuple[str, str], str] = {
    **{
        ("py/pipeline_graph/pipeline_graph_spec.py", label): (
            "a DisplayNode/RawNode label -- the pipeline graph draws these strings,"
            " and nothing opens them"
        )
        for label in (
            "../MAM-parsed/plus/",
            "../MAM-parsed/plain/",
            "../MAM-simple/",
            "../MAM-with-doc/docs/",
            "../MAM-for-Sefaria/",
            "../MAM-OSIS/",
        )
    },
    ("py/author_boj_util/common_titles_etc.py", "f'../{D1D_DIR}/{sid}.html'"): (
        "a site-relative href; D1D_DIR is a directory of the published site"
    ),
    ("py/foi/foi_finals.py", "f'../{book_filename}#{chapnver_id}'"): (
        "a site-relative href to another page of the same site"
    ),
    (
        "py/py_render/rt_suggestion_context.py",
        "f'../{site_data.POST_STRESS_METEG_FNAME}#{site_data.POST_STRESS_METEG_M23_ID}'",
    ): "a site-relative href to another page of the same site",
}

# Files whose sibling_repo/require_sibling calls name no clone.  Only one qualifies,
# and its own docstring says so: it exercises the resolver "without requiring any real
# sibling directory to exist on disk", every call running under a patched os.environ
# and every path it checks built inside a TemporaryDirectory.  Its "wlc-utils" and
# "wlc-utils-private" arguments are fixtures for the REPO_<NAME>_DIR name mapper -- and
# the comment above them says as much -- so counting them would put a repo in the
# reach set on the strength of a string in a mock.
_INERT_RESOLVER_TESTS = frozenset({"py/tests/test_mb_cmn_paths.py"})

# Sites whose repo name comes from a tracked data file rather than from any literal in
# the same file.  Naming the site here is what keeps an unresolved name a hard failure
# everywhere else.
_DYNAMIC_NAME_SOURCES: dict[tuple[str, str], str] = {
    ("py/vendoring/discover.py", "repo_name"): "vendoring-policy",
    ("py/vendoring/compare.py", "dest_repo"): "vendoring-policy",
    ("py/vendoring/provenance.py", "repo"): "vendoring-policy",
    ("py/tests/test_vendoring_policy_paths.py", "repo_name"): "vendoring-policy",
    ("py/mb_misc/write_utils.py", "f'../{mam_for_xxx}'"): "variant-mam-for-xxx",
}

# paths.py IS the resolver: its `repos_root() / name` is the mechanism rather than a
# call site, and its `name` is a parameter no in-file lookup can resolve.  Only the
# repos_root recognizer skips it; its own sibling_repo("MAM-parsed") and
# sibling_repo("MAM-private") calls are real reaches and are counted.
_PATHS_MODULE = "py/mb_cmn/paths.py"

_SELF = "py/tests/test_sibling_reach.py"

_REACH_CALLS = frozenset({"sibling_repo", "require_sibling"})
_CWD_RELATIVE = re.compile(r"^\.\./([A-Za-z0-9][A-Za-z0-9._-]*)")


def _tracked_py() -> list[tuple[str, Path]]:
    root = paths.repo_root()
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "py/*.py"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    rels = [line for line in result.stdout.splitlines() if line]
    assert rels, "git ls-files listed no tracked py/*.py -- the scan has no input"
    return [(rel, root / rel) for rel in rels if rel != _SELF]


def _docstring_ids(tree: ast.Module) -> set[int]:
    """Every Constant node that is a module/class/function docstring."""
    out: set[int] = set()
    holder = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
    for node in ast.walk(tree):
        if not isinstance(node, holder) or not node.body:
            continue
        first = node.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
            if isinstance(first.value.value, str):
                out.add(id(first.value))
    return out


def _module_level_value(tree: ast.Module, ident: str) -> ast.expr | None:
    """What ``ident`` is assigned at module level, if anything."""
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == ident:
                    return node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            if isinstance(node.target, ast.Name) and node.target.id == ident:
                return node.value
    return None


def _string_literals_in(value: ast.expr, tree: ast.Module) -> set[str]:
    """String literals in ``value``, following one level of module-level constant.

    ``("MAM-simple", "MAM-for-Sefaria")`` yields both; ``_CWD_RELATIVE_WRITE_TARGETS``
    yields the same by looking that name up where the module assigns it.
    """
    if isinstance(value, ast.Constant):
        return {value.value} if isinstance(value.value, str) else set()
    if isinstance(value, (ast.Tuple, ast.List, ast.Set)):
        out: set[str] = set()
        for element in value.elts:
            if isinstance(element, ast.Constant) and isinstance(element.value, str):
                out.add(element.value)
        return out
    if isinstance(value, ast.Name):
        assigned = _module_level_value(tree, value.id)
        if assigned is not None and not isinstance(assigned, ast.Name):
            return _string_literals_in(assigned, tree)
    return set()


def _string_literals_bound_to(tree: ast.Module, ident: str) -> set[str]:
    """String literals bound to ``ident`` anywhere in one file.

    Resolves the three shapes this tree actually uses, without importing anything or
    tracing dataflow: ``DATA_REPO_NAME``, a module constant, from its assignment;
    ``repo.source_repo``, a dataclass field, from the ``source_repo="wlc-utils"``
    keyword arguments that build the table being iterated; and a for-loop variable --
    ``main_0_mega.py``'s mega guard iterates ``_CWD_RELATIVE_WRITE_TARGETS`` and calls
    ``sibling_repo(name)`` -- from the collection it walks.  An attribute is looked up
    by its FIELD name; the ``repo`` half is a loop variable and names nothing.
    """
    out: set[str] = set()
    field = ident.rsplit(".", 1)[-1]
    is_attribute = "." in ident

    def add(value: ast.expr) -> None:
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            out.add(value.value)

    if not is_attribute:
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.AsyncFor)):
                target = node.target
                if isinstance(target, ast.Name) and target.id == ident:
                    out |= _string_literals_in(node.iter, tree)

    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == field:
            add(node.value)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not is_attribute:
                    if target.id == ident:
                        add(node.value)
                elif isinstance(target, ast.Attribute) and target.attr == field:
                    add(node.value)
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            target = node.target
            if isinstance(target, ast.Name) and not is_attribute:
                if target.id == ident:
                    add(node.value)
            elif isinstance(target, ast.Attribute) and target.attr == field:
                add(node.value)
    return out


def _ident_of(node: ast.expr) -> str | None:
    """The identifier this expression names, for resolution and for reporting."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return ast.unparse(node)
    return None


def _repos_root_aliases(tree: ast.Module) -> set[str]:
    """Names bound to ``repos_root()`` -- ``_REPOS = paths.repos_root()`` and friends."""
    out: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Call):
            continue
        callee = node.value.func
        if (
            getattr(callee, "attr", None) or getattr(callee, "id", None)
        ) != "repos_root":
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                out.add(target.id)
    return out


def _vendoring_policy_dest_repos() -> set[str]:
    """The un-ignored destination repos of ``in/vendoring_policy.json``."""
    policy = json.loads(
        (paths.in_dir() / "vendoring_policy.json").read_text(encoding="utf-8")
    )
    repos = policy.get("repos", {})
    return {name for name, entry in repos.items() if not entry.get("ignore")}


def _variant_mam_for_xxx_repos(trees: dict[str, ast.Module]) -> set[str]:
    """Every repo that can flow into ``write_utils.bkg_path``'s ``f"../{mam_for_xxx}"``.

    The fallback spelled at that call, plus every value the tree gives the
    ``variant-mam-for-xxx`` key.  Deriving the second half is what makes a new
    ``"variant-mam-for-xxx": "<repo>"`` entry show up here as a reach, which is
    precisely the route that went unrecorded until 2026-09-04.
    """
    found = {"MAM-for-Sefaria"}
    for tree in trees.values():
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            for key, value in zip(node.keys, node.values):
                if not isinstance(key, ast.Constant):
                    continue
                if key.value != "variant-mam-for-xxx":
                    continue
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    found.add(value.value)
    return found


def _roster_names() -> set[str]:
    """Sibling folder names in ``all-repos.code-workspace`` -- the machine roster."""
    workspace = json.loads(
        (paths.repo_root() / "all-repos.code-workspace").read_text(encoding="utf-8-sig")
    )
    out: set[str] = set()
    for folder in workspace["folders"]:
        path = folder.get("path", "")
        if path.startswith("../"):
            out.add(path[len("../") :])
    assert out, "the workspace roster listed no sibling folders"
    return out


def _scan_calls_and_joins(
    trees: dict[str, ast.Module],
    reached: dict[str, set[str]],
    problems: list[str],
) -> None:
    """The paths-API and repos_root recognizers, over every tracked module."""
    dest_repos: set[str] | None = None
    for rel, tree in trees.items():
        aliases = _repos_root_aliases(tree)
        for node in ast.walk(tree):
            name_node = _reaching_name_node(node, rel, aliases)
            if name_node is None:
                continue
            site = f"{rel}:{node.lineno}"
            if isinstance(name_node, ast.Constant) and isinstance(name_node.value, str):
                if rel not in _INERT_RESOLVER_TESTS:
                    reached.setdefault(name_node.value, set()).add(site)
                continue
            ident = _ident_of(name_node)
            if ident is None:
                problems.append(
                    f"{site}: the repo name is {ast.unparse(name_node)!r}, which this"
                    " scan cannot resolve.  Add the site to _DYNAMIC_NAME_SOURCES."
                )
                continue
            source = _DYNAMIC_NAME_SOURCES.get((rel, ident))
            if source == "vendoring-policy":
                if dest_repos is None:
                    dest_repos = _vendoring_policy_dest_repos()
                names = dest_repos
            else:
                names = _string_literals_bound_to(tree, ident)
            if not names:
                problems.append(
                    f"{site}: the repo name comes from {ident!r}, and no string"
                    " literal in that file binds it.  Add the site to"
                    " _DYNAMIC_NAME_SOURCES saying where its names come from."
                )
                continue
            if rel in _INERT_RESOLVER_TESTS:
                continue
            for name in names:
                reached.setdefault(name, set()).add(site)


def _reaching_name_node(node: ast.AST, rel: str, aliases: set[str]) -> ast.expr | None:
    """The expression naming the repo, if ``node`` is a reaching site."""
    if isinstance(node, ast.Call):
        callee = node.func
        fname = getattr(callee, "attr", None) or getattr(callee, "id", None)
        if fname in _REACH_CALLS and node.args:
            return node.args[0]
        return None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        if rel == _PATHS_MODULE:
            return None
        left = node.left
        rooted = (isinstance(left, ast.Name) and left.id in aliases) or (
            isinstance(left, ast.Call)
            and (getattr(left.func, "attr", None) or getattr(left.func, "id", None))
            == "repos_root"
        )
        if rooted:
            return node.right
    return None


def _scan_cwd_relative(
    trees: dict[str, ast.Module],
    vocabulary: set[str],
    reached: dict[str, set[str]],
    problems: list[str],
) -> None:
    """The cwd-relative recognizer -- the mechanism the survey's grep cannot see."""
    dynamic: set[str] | None = None
    for rel, tree in trees.items():
        docstrings = _docstring_ids(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if id(node) in docstrings:
                    continue
                match = _CWD_RELATIVE.match(node.value)
                if match is None or match.group(1) not in vocabulary:
                    continue
                if (rel, node.value) in _NOT_A_SIBLING_PATH:
                    continue
                reached.setdefault(match.group(1), set()).add(f"{rel}:{node.lineno}")
            elif isinstance(node, ast.JoinedStr):
                head = node.values[0] if node.values else None
                if not (isinstance(head, ast.Constant) and head.value == "../"):
                    continue
                text = ast.unparse(node)
                if (rel, text) in _NOT_A_SIBLING_PATH:
                    continue
                site = f"{rel}:{node.lineno}"
                if _DYNAMIC_NAME_SOURCES.get((rel, text)) == "variant-mam-for-xxx":
                    if dynamic is None:
                        dynamic = _variant_mam_for_xxx_repos(trees)
                    for name in dynamic:
                        reached.setdefault(name, set()).add(site)
                    continue
                # An interpolated first segment resolvable in the same file: the mega
                # guard's f"../{name}" over _CWD_RELATIVE_WRITE_TARGETS is this shape.
                # Filtered by the vocabulary, because the identifier interpolated into
                # a site-relative href resolves to a page or directory name, not a repo.
                head_ident = None
                if len(node.values) > 1 and isinstance(
                    node.values[1], ast.FormattedValue
                ):
                    head_ident = _ident_of(node.values[1].value)
                resolved = (
                    _string_literals_bound_to(tree, head_ident) & vocabulary
                    if head_ident
                    else set()
                )
                if not resolved:
                    problems.append(
                        f"{site}: {text} roots a path at the parent directory with an"
                        " interpolated first segment, so it may name a sibling repo."
                        "  Add it to _NOT_A_SIBLING_PATH if it is a site-relative"
                        " href, or to _DYNAMIC_NAME_SOURCES if it is a reach."
                    )
                    continue
                for name in resolved:
                    reached.setdefault(name, set()).add(site)


def _scan() -> tuple[dict[str, set[str]], list[str]]:
    trees: dict[str, ast.Module] = {}
    for rel, path in _tracked_py():
        trees[rel] = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    reached: dict[str, set[str]] = {}
    problems: list[str] = []
    _scan_calls_and_joins(trees, reached, problems)
    vocabulary = _roster_names() | set(reached)
    _scan_cwd_relative(trees, vocabulary, reached, problems)
    return reached, problems


def _sites(reached: dict[str, set[str]], name: str) -> str:
    return ", ".join(sorted(reached.get(name, ())))


def test_sibling_reach_matches_the_declaration() -> None:
    reached, problems = _scan()
    assert not problems, (
        "This scan found a sibling-reaching site it cannot resolve to a repo name,"
        " so the reach set is unknown rather than merely different.  Resolving it is"
        " the fix; weakening the scan is not.\n  " + "\n  ".join(sorted(problems))
    )
    declared = set(SIBLINGS_REACHED)
    found = set(reached)
    added = sorted(found - declared)
    removed = sorted(declared - found)
    lines = []
    for name in added:
        lines.append(
            f"REACHED BUT NOT DECLARED: {name}, at {_sites(reached, name)}."
            " Add an entry to SIBLINGS_REACHED saying why this repo is reached,"
            " or route the site through mb_cmn.paths and drop the reach."
        )
    for name in removed:
        lines.append(
            f"DECLARED BUT NOT REACHED: {name}. Nothing in tracked Python resolves"
            " that clone any more, so delete its SIBLINGS_REACHED entry."
        )
    assert not lines, "\n  ".join(
        ["The declared sibling reach is out of date."] + lines
    )
