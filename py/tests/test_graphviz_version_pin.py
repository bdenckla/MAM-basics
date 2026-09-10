"""Lint: every tracked SVG rendered by Graphviz carries the pinned stamp.

WHY A LINT AND NOT ONLY A CHECK INSIDE THE GENERATORS. Graphviz writes its own
version into each SVG it renders, so regenerating on a machine with a different
Graphviz rewrites that line in every file touched, silently, alongside whatever
change was actually wanted. `py/mb_cmn/graphviz_pin.py`'s docstring records the
case that prompted this and Ben's decision of 2026-09-09; what that module leaves
to this file is the half its `check_installed` cannot reach:

  * A file committed from a machine that never ran the generator-side check --
    another checkout, another machine, a container -- is caught here and nowhere
    else.

  * A file that no generator owns is caught here and nowhere else, which is what
    this lint was written for. `doc/process-documentation/MAM-process.dot.svg`
    WAS such a file: nothing under `py/` rendered it, so it sat at
    14.1.2 (20260124.0452) while every other tracked SVG here moved to 16.0.0,
    and `a254d450` of 2026-09-09 re-rendered it by hand. THAT GAP HAS BEEN
    CLOSED -- `py/main_pipeline_graph.py` renders it now, so `check_installed`
    fires for it like any other -- but the reading stays, because nothing
    guarantees the next tracked SVG to arrive will have an owner either.

It also needs no Graphviz installed, reading only tracked bytes, so it runs
wherever the suite runs.

THE SHAPE IS A MECHANICAL LINT OVER THE TREE, which is one of the two shapes
`doc/agent-planning-principles.md` admits: a decidable property of tracked text,
not a hand-picked example pinned as behavior.

A MISSING INPUT FAILS, IT DOES NOT SKIP, and there are two ways this scan could
quietly read nothing. `git ls-files` runs with cwd at the repo root, so a wrong
root yields an empty list rather than an error; `_MIN_STAMPED` is the floor that
turns that into a failure. And a Graphviz SVG that somehow lost its stamp would
otherwise pass by looking like the one hand-made SVG here, so the unstamped set
is asserted to be exactly `_EXPECTED_UNSTAMPED` rather than merely tolerated.

Run it inside the suite, or on its own:

  C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -k graphviz_version_pin
"""

import subprocess
import unittest
from pathlib import Path

from mb_cmn import graphviz_pin

# py/tests/test_graphviz_version_pin.py -> tests -> py -> the repo root.
REPO_ROOT = Path(__file__).resolve().parents[2]

# The one tracked SVG that Graphviz did not make. "MAM process original --
# provenance.md" beside it records that it was exported from a Google Drawing
# which is "no longer considered definitive", MAM-process.dot having replaced it
# as the source. It is kept as the historical original, carries no Graphviz
# stamp, and never will.
_EXPECTED_UNSTAMPED = frozenset(
    {
        "doc/process-documentation/MAM process original.svg",
    }
)

# 14 tracked SVGs carried a stamp on 2026-09-09: the 12 call graphs under
# gh-pages/MAM-parsed/**/svg/, doc/process-documentation/pipeline.svg and
# doc/process-documentation/MAM-process.dot.svg. The floor is here to catch a
# scan that read nothing or almost nothing, not to assert a size -- the call
# graphs are written one per column version, so their number is free to move.
_MIN_STAMPED = 10


def _tracked_svg_paths():
    completed = subprocess.run(
        # core.quotepath=false keeps a non-ASCII tracked name spelled as itself
        # rather than C-quoted, which would fail the is_file() guard below and
        # drop the file with nothing said. No tracked .svg has such a name today;
        # the flag is here so that one arriving does not go unlinted.
        ["git", "-c", "core.quotepath=false", "ls-files", "--", "*.svg"],
        cwd=REPO_ROOT,
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    paths = []
    for line in completed.stdout.splitlines():
        rel = line.strip().replace("\\", "/")
        if not rel:
            continue
        if not (REPO_ROOT / rel).is_file():
            continue
        paths.append(rel)
    return paths


class TestGraphvizVersionPin(unittest.TestCase):
    """Every tracked Graphviz-rendered SVG carries graphviz_pin.PINNED_STAMP."""

    @classmethod
    def setUpClass(cls):
        cls.stamps = {}
        for rel in _tracked_svg_paths():
            text = (REPO_ROOT / rel).read_text(encoding="utf-8")
            cls.stamps[rel] = graphviz_pin.stamp_in_svg_text(text)

    def test_every_stamped_svg_matches_the_pin(self):
        offenders = sorted(
            f"{rel}: {stamp}"
            for rel, stamp in self.stamps.items()
            if stamp is not None and stamp != graphviz_pin.PINNED_STAMP
        )
        self.assertEqual(
            offenders,
            [],
            f"Tracked SVGs rendered by a Graphviz other than the pinned "
            f"{graphviz_pin.PINNED_STAMP}. Re-render them with the pinned "
            "version, or -- if the bump is deliberate -- raise PINNED_STAMP in "
            "py/mb_cmn/graphviz_pin.py, regenerate every tracked SVG, and commit "
            f"that regeneration on its own: {offenders}",
        )

    def test_only_the_known_hand_made_svg_lacks_a_stamp(self):
        unstamped = frozenset(
            rel for rel, stamp in self.stamps.items() if stamp is None
        )
        self.assertEqual(
            unstamped,
            _EXPECTED_UNSTAMPED,
            "The set of tracked SVGs carrying no Graphviz stamp has changed. A "
            "newly unstamped file is either a Graphviz SVG that lost its stamp "
            "-- which would otherwise pass this lint by looking hand-made -- or "
            "a new hand-made SVG, which belongs in _EXPECTED_UNSTAMPED with its "
            "reason.",
        )

    def test_the_scan_read_the_tree(self):
        stamped = [rel for rel, stamp in self.stamps.items() if stamp is not None]
        self.assertGreaterEqual(
            len(stamped),
            _MIN_STAMPED,
            f"Only {len(stamped)} stamped SVGs found under {REPO_ROOT} (floor "
            f"{_MIN_STAMPED}); the scan may have read the wrong tree rather than "
            "the tree having shrunk.",
        )


if __name__ == "__main__":
    unittest.main()
