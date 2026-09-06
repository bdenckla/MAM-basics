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

The consequence was not hypothetical. Until the 2026-09-06 first and second product
lanes, ``mb_misc/write_utils.py`` built a cwd-relative MAM-simple or MAM-for-Sefaria
destination. The two landed product trees now use ``mb_cmn.paths.repo_root()`` instead,
so neither product creates or writes to a sibling clone.

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

AND A SUPPRESSION WHOSE SITE IS GONE IS ITSELF A WEAKENING -- one nobody can see, since
the lint goes on passing while the table goes on telling its reader about code that no
longer exists.  On 2026-09-04 ``2e66268a`` removed the literal
``"../book-of-job/gh-pages/jobn-details/"`` from ``main_map_changes_to_book_of_job.py``
and had to remove that literal's ``_NOT_A_SIBLING_PATH`` entry by hand; left in, the
entry would have sat there green.  So each consult point records the declared key it
used, and ``test_every_declared_suppression_still_matches_a_site`` fails naming the keys
nothing reached.  All FOUR declaration tables are covered -- see the comment above
``_Consulted`` for why none of them is exempt.

THE FIVE MECHANISMS, ALL OF WHICH THIS COVERS

* ``sibling_repo("X")`` / ``require_sibling("X", ...)`` -- the sanctioned API.
* The same calls with the name in a variable: ``redirect_stubs/stubs.py`` passes
  ``repo.source_repo`` from its ``REDIRECT_REPOS`` table. The survey's grep finds that
  line and cannot read a repo off it, so this test resolves the table's keyword arguments
  without importing the module or tracing data flow.
* ``repos_root() / "X"``, which honours ``REPOS_ROOT`` but bypasses both the per-repo
  ``REPO_<NAME>_DIR`` override and ``require_sibling``'s message.  ``main_0_mega.py``
  builds subprocess ``cwd``s this way for MAM-parsed and MAM-private.
* A name arriving from a tracked data file, which no in-file lookup can resolve:
  ``vendoring/`` and ``tests/test_vendoring_policy_paths.py`` take theirs from
  ``in/vendoring_policy.json``. ``_DYNAMIC_NAME_SOURCES`` names those two sites.
* Cwd-relative ``"../X"``, the mechanism the survey's grep cannot see -- as a plain
  literal or as an interpolated path whose first segment this test can resolve in the
  same file. The vocabulary filter excludes an interpolated site-relative href.

WHY THE CWD-RELATIVE SITES ARE NOT DEFECTS TO FIX

CLAUDE.md's "Running tests -- always from the repo root" section names vendored files
that intentionally keep cwd-relative or self-contained ``__file__``-relative logic so
they stay portable without also requiring ``mb_cmn/paths.py``. ``paths.mam_parsed_path``'s
docstring states the doctrine behind the first: "THE CALLER SUPPLIES THIS PATH BECAUSE
THE READER CANNOT." So the assertion here is NOT "there are no cwd-relative literals".
It is "the siblings reached, by any mechanism, are exactly these" -- and a sanctioned
cwd-relative default contributes its repo to that set like any other route.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_sibling_reach.py
"""

from __future__ import annotations

import ast
import functools
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
# half-finished removal cannot be mistaken for a finished one. Expect this list to
# shrink as the fourth stage's remaining product lanes land.
# ---------------------------------------------------------------------------
SIBLINGS_REACHED: dict[str, str] = {
    "MAM-simple": (
        "redirect_stubs/stubs.py only, to create a temporary clone while publishing the"
        " source repository's frozen redirect stubs."
    ),
    "MAM-parsed": (
        "Optional legacy-history comparisons and the portable reader's external"
        " vendored default. Normal MAM-basics corpus reads use the landed product."
    ),
    "MAM-for-Sefaria": (
        "redirect_stubs/stubs.py only, to create a temporary clone while publishing the"
        " source repository's frozen redirect stubs."
    ),
    "MAM-OSIS": "Written by the OSIS generators through paths.sibling_repo.",
    "MAM-with-doc": "Holds the change-log and doc trees the diff reports write into.",
    "MAM-private": (
        "paths.al_hatorah_phonetic_dir reads MAM-private/al-hatorah's Phonetic MAM"
        " as the oracle for accgram.final_stress, and main_0_mega runs the"
        " near-aleppo census there.  Its vendoring audit was given up on"
        " 2026-09-04 (abb03ec4), which removed a third route but not these two."
    ),
    "codex-index-aleppo": (
        "redirect_stubs/stubs.py only -- the Aleppo Pages redirect host."
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
            "../MAM-with-doc/docs/",
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
        "f'../{site_data.POST_STRESS_METEG_FNAME}'",
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
    ("py/tests/test_vendoring_policy_paths.py", "repo_name"): "vendoring-policy",
}

# paths.py IS the resolver: its `repos_root() / name` is the mechanism rather than a
# call site, and its `name` is a parameter no in-file lookup can resolve.  Only the
# repos_root recognizer skips it; its own sibling_repo("MAM-parsed") and
# sibling_repo("MAM-private") calls are real reaches and are counted.
_PATHS_MODULE = "py/mb_cmn/paths.py"

_SELF = "py/tests/test_sibling_reach.py"

_REACH_CALLS = frozenset({"sibling_repo", "require_sibling"})
_CWD_RELATIVE = re.compile(r"^\.\./([A-Za-z0-9][A-Za-z0-9._-]*)")


# ---------------------------------------------------------------------------
# THE DEAD-ENTRY CHECK.  Every consult point goes through the class below, which
# records the declared key it used, so a declaration excusing a site the tree no
# longer has is reported rather than sitting green.
#
# ALL FOUR TABLES ARE COVERED, not just ``_NOT_A_SIBLING_PATH``.  Each names a file
# or a (file, name) pair, so each goes stale by the one mechanism -- the code it
# names being edited or deleted -- and each is consulted at a point the scan reaches
# whenever the site it names still exists.  So an unused key means a site that is
# gone, never a live one that merely went unvisited, and neither
# ``_INERT_RESOLVER_TESTS``, ``_DYNAMIC_NAME_SOURCES`` nor ``_PATHS_MODULE`` earns an
# exemption.  ``_DYNAMIC_NAME_SOURCES`` is read on two separate paths, the paths-API
# recognizer and the cwd-relative one, and a key hit on either counts.
#
# ``_PATHS_MODULE`` needed its consult point MOVED to earn this.  It used to be read
# before ``_reaching_name_node`` had tested whether the division was rooted at
# ``repos_root()``, so it fired on every division node in ``paths.py`` -- fifteen of
# them on 2026-09-04, of which exactly one, ``repos_root() / name`` in
# ``sibling_repo``, is the mechanism the entry exists to skip.  Recording a hit there
# would have left the entry reading as used even with that line deleted, and a check
# that cannot fail is not evidence.
#
# One ordering is worth knowing when this check does fire.  In the plain-literal
# branch the vocabulary filter runs BEFORE ``_NOT_A_SIBLING_PATH``, so an entry for a
# ``../X`` whose X has left both the roster and the reach set reads as dead -- which
# is correct, nothing consults it any more, and that same removal fires the reach
# assertion below in the same run.
# ---------------------------------------------------------------------------
class _Consulted:
    """The declared suppression keys one scan used, one method per declaration table.

    The methods exist so that no consult point spells a table's name as a free string:
    a typo there would report a live key as dead, which is the very failure this class
    is built to prevent.
    """

    def __init__(self) -> None:
        self._used: set[tuple[str, object]] = set()

    def not_a_sibling_path(self, rel: str, literal: str) -> bool:
        """Is this (file, literal) declared to construct no sibling path?"""
        if (rel, literal) not in _NOT_A_SIBLING_PATH:
            return False
        self._used.add(("_NOT_A_SIBLING_PATH", (rel, literal)))
        return True

    def dynamic_name_source(self, rel: str, ident: str) -> str | None:
        """Where this site's repo names come from, if it is declared to have a source."""
        source = _DYNAMIC_NAME_SOURCES.get((rel, ident))
        if source is not None:
            self._used.add(("_DYNAMIC_NAME_SOURCES", (rel, ident)))
        return source

    def inert_resolver_test(self, rel: str) -> bool:
        """Do this file's reaching calls name no clone?"""
        if rel not in _INERT_RESOLVER_TESTS:
            return False
        self._used.add(("_INERT_RESOLVER_TESTS", rel))
        return True

    def paths_module(self, rel: str) -> bool:
        """Is this the resolver itself, whose ``repos_root() / name`` IS the mechanism?"""
        if rel != _PATHS_MODULE:
            return False
        self._used.add(("_PATHS_MODULE", rel))
        return True

    def dead_entries(self) -> list[str]:
        """Declared keys no site reached -- one line each, naming what to delete."""
        declared: list[tuple[str, set[object]]] = [
            ("_NOT_A_SIBLING_PATH", set(_NOT_A_SIBLING_PATH)),
            ("_DYNAMIC_NAME_SOURCES", set(_DYNAMIC_NAME_SOURCES)),
            ("_INERT_RESOLVER_TESTS", set(_INERT_RESOLVER_TESTS)),
            ("_PATHS_MODULE", {_PATHS_MODULE}),
        ]
        out: list[str] = []
        for table, keys in declared:
            used = {key for name, key in self._used if name == table}
            out.extend(f"{table}: {key!r}" for key in sorted(keys - used, key=repr))
        return out


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

    ``("MAM-parsed", "MAM-private")`` yields both; a named module-level tuple yields
    the same set by looking the name up where the module assigns it.
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
    tracing dataflow: ``repo.source_repo``, a dataclass field, from the
    ``source_repo="wlc-utils"`` keyword arguments that build the table being iterated;
    and a for-loop variable from the collection it walks. An attribute is looked up by
    its FIELD name; the ``repo`` half is a loop variable and names nothing.
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
    """The un-ignored sibling destinations of ``in/vendoring_policy.json``."""
    policy = json.loads(
        (paths.in_dir() / "vendoring_policy.json").read_text(encoding="utf-8")
    )
    repos = policy.get("repos", {})
    return {
        name
        for name, entry in repos.items()
        if not entry.get("ignore") and name != paths.repo_root().name
    }


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
    consulted: _Consulted,
) -> None:
    """The paths-API and repos_root recognizers, over every tracked module."""
    dest_repos: set[str] | None = None
    for rel, tree in trees.items():
        aliases = _repos_root_aliases(tree)
        for node in ast.walk(tree):
            name_node = _reaching_name_node(node, rel, aliases, consulted)
            if name_node is None:
                continue
            site = f"{rel}:{node.lineno}"
            if isinstance(name_node, ast.Constant) and isinstance(name_node.value, str):
                if not consulted.inert_resolver_test(rel):
                    reached.setdefault(name_node.value, set()).add(site)
                continue
            ident = _ident_of(name_node)
            if ident is None:
                problems.append(
                    f"{site}: the repo name is {ast.unparse(name_node)!r}, which this"
                    " scan cannot resolve.  Add the site to _DYNAMIC_NAME_SOURCES."
                )
                continue
            source = consulted.dynamic_name_source(rel, ident)
            if source == "vendoring-policy":
                if dest_repos is None:
                    dest_repos = _vendoring_policy_dest_repos()
                names = dest_repos
                if not names:
                    continue
            else:
                names = _string_literals_bound_to(tree, ident)
            if not names:
                problems.append(
                    f"{site}: the repo name comes from {ident!r}, and no string"
                    " literal in that file binds it.  Add the site to"
                    " _DYNAMIC_NAME_SOURCES saying where its names come from."
                )
                continue
            if consulted.inert_resolver_test(rel):
                continue
            for name in names:
                reached.setdefault(name, set()).add(site)


def _reaching_name_node(
    node: ast.AST, rel: str, aliases: set[str], consulted: _Consulted
) -> ast.expr | None:
    """The expression naming the repo, if ``node`` is a reaching site."""
    if isinstance(node, ast.Call):
        callee = node.func
        fname = getattr(callee, "attr", None) or getattr(callee, "id", None)
        if fname in _REACH_CALLS and node.args:
            return node.args[0]
        return None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left = node.left
        rooted = (isinstance(left, ast.Name) and left.id in aliases) or (
            isinstance(left, ast.Call)
            and (getattr(left.func, "attr", None) or getattr(left.func, "id", None))
            == "repos_root"
        )
        # The resolver's own ``repos_root() / name`` is skipped only once the division
        # is known to be rooted, so that _PATHS_MODULE records a hit on the mechanism
        # rather than on any of paths.py's other divisions.  See _Consulted above.
        if rooted and not consulted.paths_module(rel):
            return node.right
    return None


def _scan_cwd_relative(
    trees: dict[str, ast.Module],
    vocabulary: set[str],
    reached: dict[str, set[str]],
    problems: list[str],
    consulted: _Consulted,
) -> None:
    """The cwd-relative recognizer -- the mechanism the survey's grep cannot see."""
    for rel, tree in trees.items():
        docstrings = _docstring_ids(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if id(node) in docstrings:
                    continue
                match = _CWD_RELATIVE.match(node.value)
                if match is None or match.group(1) not in vocabulary:
                    continue
                if consulted.not_a_sibling_path(rel, node.value):
                    continue
                reached.setdefault(match.group(1), set()).add(f"{rel}:{node.lineno}")
            elif isinstance(node, ast.JoinedStr):
                head = node.values[0] if node.values else None
                if not (isinstance(head, ast.Constant) and head.value == "../"):
                    continue
                text = ast.unparse(node)
                if consulted.not_a_sibling_path(rel, text):
                    continue
                site = f"{rel}:{node.lineno}"
                # Filter by the vocabulary, because an identifier interpolated into a
                # site-relative href is a page or directory name, not a repository name.
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


@functools.lru_cache(maxsize=1)
def _scan() -> tuple[dict[str, set[str]], list[str], list[str]]:
    """The reach set, the sites the scan could not resolve, and the dead declarations.

    Cached because both tests below want the same pass over the tree, and neither
    mutates what it is handed.
    """
    trees: dict[str, ast.Module] = {}
    for rel, path in _tracked_py():
        trees[rel] = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    reached: dict[str, set[str]] = {}
    problems: list[str] = []
    consulted = _Consulted()
    _scan_calls_and_joins(trees, reached, problems, consulted)
    vocabulary = _roster_names() | set(reached)
    _scan_cwd_relative(trees, vocabulary, reached, problems, consulted)
    return reached, problems, consulted.dead_entries()


def _sites(reached: dict[str, set[str]], name: str) -> str:
    return ", ".join(sorted(reached.get(name, ())))


def test_every_declared_suppression_still_matches_a_site() -> None:
    _, _, dead = _scan()
    assert not dead, (
        "A declaration below excuses a site this tree no longer has.  Nothing consults"
        " it, so the lint goes on passing while the table goes on describing code that"
        " is gone -- a weakening of the check rather than a suppression of a false"
        " positive.  Delete the entries:\n  " + "\n  ".join(dead)
    )


def test_sibling_reach_matches_the_declaration() -> None:
    reached, problems, _ = _scan()
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
