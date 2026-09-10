"""Resolve the Aleppo data that now lives in MAM-basics.

``aleppo/`` holds the Aleppo Codex scans, annotations, index data, reports, and
procedures. ``MAM-simple/xml-vtrad-mam/`` is the MAM-native XML corpus the Aleppo
reader uses as its word-sequence ground truth.

``CODE_DIR`` is MAM-basics' ``py/`` directory. ``code_paths()`` lists the Aleppo
modules for the source lints, while every other accessor below names the
MAM-basics data tree directly.
"""

from pathlib import Path

from mb_cmn import paths

AC_PACKAGES = ("py_ac_loc",)
"""The package codex-index-aleppo's code landed in under this repo's ``py/``.

``py_ac_loc`` kept its name.  A second package held the Wikisource index generator's
modules until 2026-09-10, when Ben's decision that day removed the generator and its
outputs; phase 3 of ``doc/PLAN-mega-coverage.md`` names every file removed.
``py_ac_word_image_helper`` is NOT listed: it arrived here with book-of-job on
2026-08-19 and is one committed blob with codex-index-aleppo's copy, so it belongs
to ``boj_paths.BOJ_PACKAGES``, which lists it, and listing it twice would lint it
twice.
"""

AC_TOP_LEVEL_MODULES = (
    "ac_paths.py",
    "check_ac_all.py",
    "main_ac_check_line_breaks.py",
    "main_ac_download_pages.py",
    "main_ac_find_word_in_images.py",
    "main_ac_gen_col_quad_editor.py",
    "main_ac_gen_flat_stream.py",
    "main_ac_gen_index_flat_annotated.py",
    "main_ac_gen_lb_flat_stream.py",
    "main_ac_gen_line_break_editor.py",
    "main_ac_merge_line_markers.py",
)
"""codex-index-aleppo's modules at the top of this repo's ``py/``: eleven of the
fifteen that landed here.  The other four were removed on 2026-09-10: the Wikisource
index generator and the column-coordinate plots by Ben's decision that day, which
phase 3 of ``doc/PLAN-mega-coverage.md`` records, the kraken baseline-segmentation
wrapper ``main_ac_kraken_seg_baselines.py`` by phase 6a of the same plan, and
``check_ac_word_finding.py`` by phase 6b, which first made it pass again.

EVERY ONE IS PREFIXED, and the prefix is mechanical: ``main_ac_`` plus the module
stem for an entry point, ``check_ac_`` plus the stem for a check.  Five of the
fifteen had to be renamed because MAM-basics already held the name -- the four
source lints and ``check_all.py``, which is book-of-job's by Ben's decision of
2026-08-19 that ``check_all`` stays per-repo -- and the rest were renamed for the
same reason ahead of time: codex-index-cam1753 holds a counterpart of six of them,
against the same manuscript problem on a different manuscript, and its Phase 3 lands
them as ``main_cam1753_`` plus the same stems.

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
    named = [CODE_DIR / name for name in AC_PACKAGES]
    named += [CODE_DIR / name for name in AC_TOP_LEVEL_MODULES]
    missing = [p for p in named if not p.exists()]
    if missing:
        raise SystemExit(
            "ac_paths.code_paths: no longer present: "
            + ", ".join(str(p) for p in missing)
        )
    return named


def line_breaks_dir() -> Path:
    """Hand-annotated per-page word streams (35 tracked JSON), the human-in-the-loop
    output of ``py_ac_loc.gen_line_break_editor``."""
    return ac_data_root() / "line-breaks"


def col_coords_dir() -> Path:
    """Per-page column quadrilaterals (35 tracked JSON), from
    ``py_ac_loc.gen_col_quad_editor``."""
    return ac_data_root() / "column-coordinates"


def pages_dir() -> Path:
    """Aleppo Codex page scans (37 tracked JPEG).

    Twenty-four are leaves 270-281 recto and verso; the other thirteen are
    001r-006r and 148r/148v.

    DOWNLOADED, not generated: ``download_aleppo_pages`` fetches them from
    archive.org, and no check regenerates them.
    """
    return ac_data_root() / "aleppo-pages"


def mam_xml_dir() -> Path:
    """MAM-simple's MAM-native XML, the word-sequence ground truth."""
    return paths.repo_root() / "MAM-simple" / "xml-vtrad-mam"


def ds_flat_stream_dir() -> Path:
    """Derived per-page flat streams (8 tracked JSON) from
    ``py_ac_loc.gen_flat_stream``."""
    return ac_data_root() / "ds-flat-stream"


def novc_dir() -> Path:
    """Gitignored scratch tree, where the two editors and the word previewer write
    the HTML they open in a browser."""
    return ac_data_root() / ".novc"


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
    ``gen_index_flat_annotated`` and read by ``py_ac_word_image_helper.flat_index``."""
    return ac_data_root() / "index-flat-annotated.json"


def check_line_breaks_html_path() -> Path:
    """The line-break check's HTML report (``<data_root>/check_line_breaks.html``),
    tracked, and rewritten by every run of ``py_ac_loc.check_line_breaks``."""
    return ac_data_root() / "check_line_breaks.html"
