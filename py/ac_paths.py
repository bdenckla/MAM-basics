"""Resolve the Aleppo data that now lives in MAM-basics.

``aleppo/`` holds the Aleppo Codex page index, its annotations, and the retained
line-break, column-coordinate and flat-stream JSON, with the reports and notes that
describe them.  The page scans and every program that worked on them were retired on
2026-09-26 by ``doc/PLAN-retire-codex-index-image-work.md``, so no program here
regenerates that retained JSON.

``CODE_DIR`` is MAM-basics' ``py/`` directory. ``code_paths()`` lists the Aleppo
modules for the source lints, while every other accessor below names the MAM-basics
data tree directly.
"""

from pathlib import Path

from mb_cmn import paths

AC_TOP_LEVEL_MODULES = (
    "ac_paths.py",
    "main_ac_gen_index_flat_annotated.py",
)
"""codex-index-aleppo's modules at the top of this repo's ``py/``: two of the
fifteen that landed here.  Four of the other thirteen were removed on 2026-09-10: the
Wikisource index generator and the column-coordinate plots by Ben's decision that day,
which phase 3 of ``doc/PLAN-mega-coverage.md`` records, the kraken
baseline-segmentation wrapper ``main_ac_kraken_seg_baselines.py`` by phase 6a of the
same plan, and ``check_ac_word_finding.py`` by phase 6b, which first made it pass
again.  Two more, the line-break editor ``main_ac_gen_line_break_editor.py`` and its
merge step ``main_ac_merge_line_markers.py``, were deleted on 2026-09-26 by Ben's
instruction that day to remove both line-break editors.  The last seven went later the
same day with the rest of the codex-index image work, under
``doc/PLAN-retire-codex-index-image-work.md``.  The package ``py_ac_loc`` went with
them, and its one surviving module, the MAM-simple reader, moved to
``py/mb_cmn/mam_xml_verses.py``.

EVERY ONE IS PREFIXED, and the prefix is mechanical: ``main_ac_`` plus the module
stem for an entry point, ``check_ac_`` plus the stem for a check.  Five of the
fifteen had to be renamed because MAM-basics already held the name -- the four
source lints and ``check_all.py``, which is book-of-job's by Ben's decision of
2026-08-19 that ``check_all`` stays per-repo -- and the rest were renamed for the
same reason ahead of time: codex-index-cam1753 held counterparts of six of them,
which its Phase 3 landed as ``main_cam1753_`` plus the same stems.

``main_gen_permission_glob.py`` is not in that list, and was not while it existed: it
moved with this code without belonging to it, generating a Claude Code permission glob
from a shell command and mentioning no manuscript, so it landed unprefixed at the top of
``py/`` as a utility of this repo's rather than inside this per-repo lint scope.  Ben
deleted it on 2026-08-24, once Claude's Auto mode had made the permission globs it wrote
pointless.  It is named here because the trio plan counts it among the files that moved,
so a reader comparing the two would otherwise be a file short.
"""

CODE_DIR = Path(__file__).resolve().parent
"""MAM-basics' ``py/`` directory, which holds the Aleppo modules."""


def ac_data_root() -> Path:
    """Path to the Aleppo corpus under this repository's root."""
    return paths.repo_root() / "aleppo"


def code_paths() -> list[Path]:
    """Every place codex-index-aleppo's Python lives here, for the source lints.

    Fails loudly on an entry that no longer exists, exactly as
    ``boj_paths.code_paths()`` does; only an unlisted ADDITION is silent, and this
    code is being evacuated rather than developed.  ``repo_scopes.code_paths()`` is
    what unions this with the other evacuated repos' lists.
    """
    named = [CODE_DIR / name for name in AC_TOP_LEVEL_MODULES]
    missing = [p for p in named if not p.exists()]
    if missing:
        raise SystemExit(
            "ac_paths.code_paths: no longer present: "
            + ", ".join(str(p) for p in missing)
        )
    return named


def wiki_dir() -> Path:
    """``aleppo-wiki/`` -- J David Stark's index in its source forms under
    ``precursors/``, two snapshots of the Wikisource page built by hand from it, and
    the hand-corrected ``index-flat-corrected.json`` that
    ``main_ac_gen_index_flat_annotated`` reads."""
    return ac_data_root() / "aleppo-wiki"


def flat_index_corrected_path() -> Path:
    """Hand-corrected flat index (``<wiki_dir>/index-flat-corrected.json``).

    Written by no program: it is J David Stark's index as flat JSON, with corrections
    applied by hand, and it is the input to ``gen_index_flat_annotated``.
    """
    return wiki_dir() / "index-flat-corrected.json"


def flat_index_annotated_path() -> Path:
    """Annotated flat index (``<data_root>/index-flat-annotated.json``), written by
    ``main_ac_gen_index_flat_annotated``."""
    return ac_data_root() / "index-flat-annotated.json"
