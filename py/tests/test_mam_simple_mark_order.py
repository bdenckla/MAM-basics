"""Lint: MAM-simple's hand-authored and published text must be in MAM's mark order.

WHY THIS EXISTS

The corpus was never the problem. ``render_wt/render_wikitext_helpers.py``'s
``uni_check.check`` runs on every element sequence MAM-simple's generator renders and
aborts the run on a violation, so the six output flavours cannot be published in the
wrong order. Everything else in that repo had no check at all, and on 2026-08-09 two
places were found in the wrong order:

  * ``doc/reading-mam-simple-xml.md`` and ``doc/reading-mam-simple-json.md`` -- seven
    lines, including the Job.34.2 and Job.1.1 sample verses the format guide shows as
    XML, and the Ruth.1.1 and Ruth.1.2 examples in the JSON guide. The format
    documentation illustrated the data with bytes the data does not contain, so a
    reader building a fixture by copying an example got a string that never matches.
  * ``gh-pages/versification-and-cantillation.html`` -- generated, from hand-authored
    Hebrew in this repo's ``versification_and_cantillation/doc.py``. That generator
    does not go through ``render_wtseq``, so ``uni_check.check`` never sees it.

Both were found by a scan someone chose to run, which is exactly the state
``MAM-basics/CLAUDE.md`` describes: "There is no lint over hand-authored source here
... so the check is yours to run." This file is that lint.

WHAT IT COVERS, AND WHY NOT THE CORPUS

Every tracked text file of MAM-simple except ``xml-vtrad-*`` and ``json-vtrad-*``. Those
two are excluded on cost, not on trust: the corpus is 84 MB and takes 13 seconds to
check, against 0.01 seconds for everything else, and it is the one part already
guaranteed at generation time by the assert named above. Including it would grow this
repo's suite by a tenth for a second opinion on the only thing already proven.

``misc/`` and ``py-examples-out/`` ARE covered, though both are generated: they are
produced by the vendored copies under ``py-examples/``, which drift from this repo's
originals between re-vendorings, so a check on them is a check on that drift.

WHAT MAM'S MARK ORDER IS, AND WHAT IT IS NOT

``mb_cmn/uni_denorm.py`` is the authority. Four marks come first -- shin dot, sin dot,
dagesh/mapiq, rafe -- and every other mark keeps the relative order it already had, so
only those four have a declared place. A vowel and an accent pass in either order, and
``has_std_mark_order`` says nothing about which of them comes first. This lint is
therefore not a canonical-form check and must not be read as one.

A MISSING SIBLING FAILS RATHER THAN SKIPS -- see ``mb_cmn.paths.require_sibling``.
"""

import subprocess
import unittest
from pathlib import Path

from mb_cmn import paths
from mb_cmn import uni_denorm

# The published corpus. Excluded on cost: 84 MB and 13 seconds, and already asserted at
# generation time by uni_check.check inside render_wtseq.
_EXCLUDE_DIR_PREFIXES = ("xml-vtrad-", "json-vtrad-")

# Fonts and images have no text to order; reading them as UTF-8 would merely raise.
_BINARY_EXTENSIONS = {".woff2", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf"}

# Well under the 64 files in scope on 2026-08-09, and here only to catch an exclusion
# filter that swallowed everything -- not to assert a tree size.
_FLOOR = 20


def _mam_simple_root() -> Path:
    clone = paths.sibling_repo("MAM-simple")
    return paths.require_sibling("MAM-simple", clone)


def _tracked_text_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    in_scope = []
    for line in result.stdout.splitlines():
        rel = line.strip().replace("\\", "/")
        if not rel:
            continue
        if rel.startswith(_EXCLUDE_DIR_PREFIXES):
            continue
        full = root / rel
        if not full.is_file():
            continue
        if full.suffix.lower() in _BINARY_EXTENSIONS:
            continue
        in_scope.append(rel)
    return in_scope


class TestMamSimpleMarkOrder(unittest.TestCase):
    """MAM-simple's text, outside the corpus, is in MAM's mark order."""

    @classmethod
    def setUpClass(cls):
        cls.root = _mam_simple_root()
        cls.in_scope = _tracked_text_files(cls.root)
        found = len(cls.in_scope)
        assert found > _FLOOR, (
            f"Only {found} MAM-simple files in scope (floor {_FLOOR}) -- "
            "the exclusion filter may be too broad."
        )

    def test_every_file_is_in_mam_mark_order(self):
        offenders = []
        for rel in self.in_scope:
            text = (self.root / rel).read_text(encoding="utf-8")
            if uni_denorm.has_std_mark_order(text):
                continue
            for num, line in enumerate(text.split("\n"), 1):
                if not uni_denorm.has_std_mark_order(line):
                    offenders.append(f"{rel}:{num}")
        self.assertEqual(
            offenders,
            [],
            "Found Hebrew not in MAM's mark order. Do NOT fix this by running"
            " unicodedata.normalize, which is what puts it in the wrong order in the"
            " first place: pass the text through uni_denorm.give_std_mark_order, or"
            f" lift it from xml-vtrad-mam. {offenders}",
        )


if __name__ == "__main__":
    unittest.main()
