"""Guard: each entry point's ``Subcommands:`` docstring block matches its parser.

A ``py/main_<x>.py`` that registers subcommands documents them twice: once in the
``argparse`` parser, and once by hand in the module docstring, which is also the
``--help`` description.  Nothing kept the two in step, so they drifted --
``run-printed-decalogue`` was registered but never listed, and ``--help`` therefore
described eleven of ``main_accgram.py``'s twelve subcommands (fixed in ``cb96f55``).
That is the same silent-drift class as a hand-maintained test registry: the
undocumented subcommand still works, so only a reader notices, and only by accident.

This is a mechanical lint over the tree, the second of the two test shapes
``doc/agent-planning-principles.md`` sanctions: both sides are derived from the source,
so adding, renaming or deleting a subcommand never needs this file edited.

WHAT IT CHECKS

* ``test_every_subcommand_is_documented_and_every_entry_registered`` -- the two name
  sets agree in both directions.  A name deleted from the parser but left in the
  docstring is the same defect running the other way.
* ``test_a_pattern_entry_spells_out_every_family_member`` -- an entry ending in
  ``<name>`` is a pattern, not a literal: ``main_accgram.py``'s
  ``generate-html-<name>`` stands for the thirteen subcommands derived from its
  ``_HTML_GENERATORS`` table.  Such an entry covers every registered name sharing its
  prefix, and its own prose then has to name each of them -- that entry spells out
  "The full set: generate-html-poetic, -goerwitz, ...", a second hand-maintained list
  with the same capacity to drift, so each family member must appear there either in
  full or as the ``-<suffix>`` shorthand that list uses.

HOW AN ENTRY POINT IS FOUND, AND WHY NOTHING HERE SKIPS

Discovery reads the source of every ``py/main_*.py`` and keeps the ones calling
``add_subparsers``: an entry point with no subcommands has nothing to check and simply
never enters the parameter list.  Everything past that point FAILS rather than skips --
a discovered entry point with no ``build_parser()`` and one with no ``Subcommands:``
block are both failures, and the ``or [...]`` fallback on the parametrize is what makes
an empty discovery fail too (pytest reports an empty parameter set as a SKIP).  Skips
are a semantic channel in this suite, reserved for reporting that a page diverges from
its strand; an environment-shaped skip mixed in corrupts that signal.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_entry_point_subcommands.py
"""

from __future__ import annotations

import argparse
import importlib
import re

import pytest

from mb_cmn import paths

# The heading that opens the hand-maintained list, and the tail marking an entry as a
# pattern standing for a family of derived subcommands rather than one literal name.
_HEADING = "Subcommands:"
_PATTERN_TAIL = "<name>"

# An entry is a line of exactly four spaces and then the bare name; its description is
# indented further beneath it.
_ENTRY_LINE = re.compile(r" {4}(\S+)")

# Discovery finding nothing is a failure, not a skip; this stem has no module, so the
# import below dies on it.
_NOTHING_DISCOVERED = "(no py/main_*.py registers subcommands -- discovery is broken)"


def _entry_points_with_subcommands() -> list[str]:
    """Module stems of the ``py/main_*.py`` that register subcommands.

    The CODE root, not wlc-utils' data root: this scans the tree the entry points
    now live in.
    """
    py_root = paths.repo_root() / "py"
    return sorted(
        path.stem
        for path in py_root.glob("main_*.py")
        if "add_subparsers(" in path.read_text(encoding="utf-8")
    )


_ENTRY_POINTS = _entry_points_with_subcommands() or [_NOTHING_DISCOVERED]


def _parser_of(stem: str) -> argparse.ArgumentParser:
    module = importlib.import_module(stem)
    build_parser = getattr(module, "build_parser", None)
    if build_parser is None:
        raise AssertionError(
            f"py/{stem}.py registers subcommands but exposes no build_parser():"
            " extract the parser out of main() so it can be read without running the"
            " program, leaving main() as `args = build_parser().parse_args()` plus its"
            " existing dispatch."
        )
    return build_parser()


def _registered_subcommands(stem: str) -> list[str]:
    parser = _parser_of(stem)
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return sorted(action.choices)
    raise AssertionError(
        f"py/{stem}.py's build_parser() returned a parser with no subparsers action,"
        " though its source calls add_subparsers()."
    )


def _documented_entries(stem: str) -> dict[str, str]:
    """Map each ``Subcommands:`` entry name to the text of its own description."""
    module = importlib.import_module(stem)
    lines = (module.__doc__ or "").splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == _HEADING:
            start = index + 1
            break
    if start is None:
        raise AssertionError(
            f"py/{stem}.py registers subcommands but its module docstring has no"
            f" `{_HEADING}` block listing them; --help shows that docstring, so the"
            " subcommands would go undescribed."
        )
    entries: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines[start:]:
        if line.strip() and not line.startswith(" "):  # a following unindented section
            break
        matched = _ENTRY_LINE.fullmatch(line)
        if matched:
            current = matched.group(1)
            entries[current] = []
        elif current is not None:
            entries[current].append(line)
    return {name: "\n".join(body) for name, body in entries.items()}


def _mentions(text: str, name: str) -> bool:
    """Whether ``text`` names ``name`` whole -- not merely as the head of a longer name."""
    return re.search(re.escape(name) + r"(?![\w-])", text) is not None


@pytest.mark.parametrize("stem", _ENTRY_POINTS)
def test_every_subcommand_is_documented_and_every_entry_registered(stem: str) -> None:
    registered = _registered_subcommands(stem)
    entries = _documented_entries(stem)
    literals = {name for name in entries if not name.endswith(_PATTERN_TAIL)}
    patterns = {
        name: name[: -len(_PATTERN_TAIL)]
        for name in entries
        if name.endswith(_PATTERN_TAIL)
    }

    problems = [
        f"{name}: registered by py/{stem}.py's parser but absent from its"
        f" `{_HEADING}` block -- add an entry for it there"
        for name in registered
        if name not in literals
        and not any(name.startswith(prefix) for prefix in patterns.values())
    ]
    problems += [
        f"{name}: listed in py/{stem}.py's `{_HEADING}` block but its parser"
        " registers no such subcommand -- delete the entry, or restore the subcommand"
        for name in sorted(literals)
        if name not in registered
    ]
    problems += [
        f"{name}: listed in py/{stem}.py's `{_HEADING}` block as a pattern, but its"
        f" parser registers no subcommand starting with {prefix!r}"
        for name, prefix in sorted(patterns.items())
        if not any(sub.startswith(prefix) for sub in registered)
    ]
    assert not problems, (
        f"py/{stem}.py's parser and its `{_HEADING}` docstring block disagree"
        " (--help shows that block, so a mismatch misdescribes the program):\n  "
        + "\n  ".join(problems)
    )


@pytest.mark.parametrize("stem", _ENTRY_POINTS)
def test_a_pattern_entry_spells_out_every_family_member(stem: str) -> None:
    registered = _registered_subcommands(stem)
    entries = _documented_entries(stem)
    problems: list[str] = []
    for name, body in sorted(entries.items()):
        if not name.endswith(_PATTERN_TAIL):
            continue
        prefix = name[: -len(_PATTERN_TAIL)]
        for member in registered:
            if not member.startswith(prefix):
                continue
            shorthand = "-" + member[len(prefix) :]
            if _mentions(body, member) or _mentions(body, shorthand):
                continue
            problems.append(
                f"{member}: registered by py/{stem}.py's parser and covered by the"
                f" {name} entry, but that entry's own list of the full set names"
                f" neither {member} nor {shorthand} -- add it there"
            )
    assert not problems, (
        f"py/{stem}.py's `{_HEADING}` block has a pattern entry whose spelled-out list"
        " of its members has drifted from the parser:\n  " + "\n  ".join(problems)
    )
