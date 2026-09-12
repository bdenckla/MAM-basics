"""Guard: the product declaration in py/product_scopes.py still describes this repo.

WHY THIS EXISTS

``py/product_scopes.py`` is the written answer to "what are this repository's
products", which Ben asked for on 2026-09-12.  A written answer that nothing checks
goes stale silently, which is the failure
``py/tests/test_vendoring_policy_paths.py`` was written for after a manifest went
unnoticed-stale for a day.  This lint is what defends it.  It is a mechanical lint
over the tree, the second of the two test shapes CLAUDE.md sanctions.

WHAT IT CHECKS

1. Every declared path exists and is tracked -- the published tree, the five product
   directories, and every tier-3 entry point.  A product directory renamed or dropped
   fails here rather than leaving the declaration quietly describing a tree that is
   gone.
2. The declared tier-3 set equals the set of entry points the runners of ``_STEPS``
   in ``py/main_0_mega.py`` name, with the ``_run_*`` wrappers defined in that file
   resolved through ``product_scopes.mega_wrapper_delegates()``.  A new mega step
   whose entry point nobody has recorded fails here, which is how tier 3 would
   otherwise grow without anyone noticing.
3. Every entry of the wrapper table is still used by a step, so a wrapper deleted
   from ``py/main_0_mega.py`` does not leave a dead entry behind.

HOW IT DIFFERS FROM py/tests/test_mega_coverage.py, WHICH ALSO READS _STEPS

That lint asks whether every PROGRAM in the tree is either run by the mega or
declared in ``NOT_IN_MEGA`` with a reason, and it reads ``py/main_0_mega.py`` by an
AST pass because it must resolve subcommands and script paths out of call sites.
This lint asks the narrower question of which entry points the step table names, and
it reads them by importing the table, so the two do not share a mechanism and do not
fail on the same things: an unjustified new program fails the coverage lint, an
unrecorded new step fails this one.  Neither subsumes the other, and this file is
deliberately not a second copy of that scan.

WHY IMPORTING RATHER THAN PARSING

``_STEPS`` holds function objects, so ``runner.__module__`` and
``runner.__qualname__`` are exact where a parse of the call site would have to infer
them.  The cost is that importing ``main_0_mega`` imports every entry module it
names, which is what the mega itself does before its first step.

A MISSING INPUT FAILS, IT DOES NOT SKIP.  An empty ``_STEPS``, an empty
``git ls-files``, and an entry point whose module has no ``__file__`` each raise or
assert rather than reporting green having verified nothing.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_product_scopes.py
"""

from __future__ import annotations

import functools
import subprocess
import sys
from pathlib import Path

import main_0_mega
import product_scopes
from mb_cmn import paths


@functools.lru_cache(maxsize=1)
def _tracked() -> frozenset[str]:
    """Every tracked path in the repository, repo-relative with forward slashes."""
    result = subprocess.run(
        ["git", "-C", str(paths.repo_root()), "ls-files"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    rels = frozenset(line for line in result.stdout.splitlines() if line)
    assert rels, "git ls-files listed no tracked path -- the lint has no input"
    return rels


@functools.lru_cache(maxsize=1)
def _tracked_dirs() -> frozenset[str]:
    """Every directory holding a tracked file, at every depth, repo-relative."""
    dirs = set()
    for rel in _tracked():
        parts = rel.split("/")
        for depth in range(1, len(parts)):
            dirs.add("/".join(parts[:depth]))
    return frozenset(dirs)


def _rel(path: Path) -> str:
    """``path`` as a repo-relative forward-slash string."""
    return path.resolve().relative_to(paths.repo_root().resolve()).as_posix()


def test_published_tree_exists_and_is_tracked() -> None:
    tree = product_scopes.published_tree()
    rel = _rel(tree)
    assert tree.is_dir(), (
        f"product_scopes.published_tree() names {rel}, which is not a directory."
        " Tier 1 is the tree a push to main deploys; if it has moved, update"
        " py/product_scopes.py to say where it is now."
    )
    assert rel in _tracked_dirs(), (
        f"product_scopes.published_tree() names {rel}, which holds no tracked file."
        " A published tree with nothing tracked in it deploys nothing."
    )


def test_every_product_dir_exists_and_is_tracked() -> None:
    missing = [_rel(d) for d in product_scopes.product_dirs() if not d.is_dir()]
    assert not missing, (
        f"py/product_scopes.py declares {len(missing)} tier-2 product directories that"
        f" do not exist: {missing}. A product renamed or dropped leaves the"
        " declaration describing a tree that is gone; update _PRODUCT_DIR_NAMES."
    )
    untracked = [
        rel
        for rel in (_rel(d) for d in product_scopes.product_dirs())
        if rel not in _tracked_dirs()
    ]
    assert not untracked, (
        f"These declared product directories hold no tracked file: {untracked}."
        " A product consumed by git URL has to be tracked to be consumable."
    )


def test_every_generator_entry_point_exists_and_is_tracked() -> None:
    rels = product_scopes.generator_entry_point_rels()
    assert rels, "py/product_scopes.py declares no tier-3 entry point"
    root = paths.repo_root()
    missing = [rel for rel in rels if not (root / rel).is_file()]
    assert not missing, (
        f"py/product_scopes.py declares {len(missing)} tier-3 entry points that do not"
        f" exist: {missing}. Rename or delete the declaration with the program."
    )
    untracked = [rel for rel in rels if rel not in _tracked()]
    assert not untracked, (
        f"These declared tier-3 entry points are not tracked: {untracked}."
        " A generator the mega runs has to be in the repository."
    )


@functools.lru_cache(maxsize=1)
def _entry_points_the_mega_runs() -> tuple[frozenset[str], frozenset[str]]:
    """The entry points ``_STEPS`` names, and the wrapper names used to resolve them.

    A step whose runner is defined in ``main_0_mega`` itself is a ``_run_*`` wrapper,
    and is resolved through ``product_scopes.mega_wrapper_delegates()``.  A wrapper
    absent from that table raises here rather than being skipped, so tier 3 cannot
    grow by way of a wrapper nobody classified.
    """
    steps = main_0_mega._STEPS
    assert steps, "py/main_0_mega.py's _STEPS is empty -- the lint has no input"
    delegates = product_scopes.mega_wrapper_delegates()
    root = paths.repo_root().resolve()
    found: set[str] = set()
    used: set[str] = set()
    unclassified: list[str] = []
    for step in steps:
        module_name = step.runner.__module__
        if module_name == main_0_mega.__name__:
            wrapper = step.runner.__qualname__
            if wrapper not in delegates:
                unclassified.append(f"{step.step_id} -> {wrapper}")
                continue
            used.add(wrapper)
            found.add(delegates[wrapper])
            continue
        module = sys.modules[module_name]
        module_file = getattr(module, "__file__", None)
        assert module_file, (
            f"step {step.step_id} runs {module_name}, which has no __file__, so the"
            " lint cannot say which entry point it is"
        )
        found.add(Path(module_file).resolve().relative_to(root).as_posix())
    assert not unclassified, (
        f"{len(unclassified)} mega steps run a _run_* wrapper defined in"
        f" py/main_0_mega.py that py/product_scopes.py does not classify:"
        f" {sorted(unclassified)}. Add each wrapper to _MEGA_WRAPPER_DELEGATES,"
        " naming the entry point it drives, and add that entry point to"
        " _GENERATOR_ENTRY_POINTS if it is not already there."
    )
    return frozenset(found), frozenset(used)


def test_declared_tier_three_matches_the_mega_step_table() -> None:
    running, _used = _entry_points_the_mega_runs()
    declared = frozenset(product_scopes.generator_entry_point_rels())
    undeclared = sorted(running - declared)
    assert not undeclared, (
        f"py/main_0_mega.py's step table runs {len(undeclared)} entry points that"
        f" py/product_scopes.py does not declare: {undeclared}. Tier 3 has grown;"
        " add each to _GENERATOR_ENTRY_POINTS, and check whether the change that"
        " added the step also needs saying in CLAUDE.md."
    )
    stale = sorted(declared - running)
    assert not stale, (
        f"py/product_scopes.py declares {len(stale)} tier-3 entry points that"
        f" py/main_0_mega.py's step table no longer runs: {stale}. Either the step"
        " was removed, in which case drop the declaration, or the program is now"
        " hand-run, in which case it belongs in test_mega_coverage.py's NOT_IN_MEGA"
        " with its reason."
    )


def test_no_dead_wrapper_declarations() -> None:
    _running, used = _entry_points_the_mega_runs()
    declared = frozenset(product_scopes.mega_wrapper_delegates())
    dead = sorted(declared - used)
    assert not dead, (
        f"py/product_scopes.py's _MEGA_WRAPPER_DELEGATES has {len(dead)} entries no"
        f" mega step uses: {dead}. Drop each one with the wrapper it named."
    )
