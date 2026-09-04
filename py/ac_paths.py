"""Resolve the Aleppo data that now lives in MAM-basics.

``aleppo/`` holds the Aleppo Codex scans, annotations, index data, reports, and
procedures. ``MAM-XML/`` holds the one pinned 24-file XML snapshot shared with the
Cambridge 1753 lane. The snapshot preserves the corpus against which this lane's
artifacts were verified; the MAM-simple evacuation later replaces it.

``CODE_DIR`` is MAM-basics' ``py/`` directory. ``code_paths()`` lists the Aleppo
modules for the source lints, while every other accessor below names the
MAM-basics data tree directly.
"""

from pathlib import Path

from mb_cmn import paths

AC_PACKAGES = ("py_ac_loc", "ac_wiki")
"""The two packages codex-index-aleppo's code landed in under this repo's ``py/``.

``py_ac_loc`` kept its name; ``ac_wiki`` was ``aleppo-wiki/py/``, which could not
keep a name it never had -- a directory called ``py`` inside a data directory,
importable as ``py.<module>`` only because that repo was entered two ways.
``py_ac_word_image_helper`` is NOT listed: it arrived here with book-of-job on
2026-08-19 and is one committed blob with codex-index-aleppo's copy, so it belongs
to ``boj_paths.BOJ_PACKAGES``, which lists it, and listing it twice would lint it
twice.
"""

AC_TOP_LEVEL_MODULES = (
    "ac_paths.py",
    "check_ac_all.py",
    "check_ac_word_finding.py",
    "main_ac_check_line_breaks.py",
    "main_ac_download_pages.py",
    "main_ac_find_word_in_images.py",
    "main_ac_gen_col_quad_editor.py",
    "main_ac_gen_flat_stream.py",
    "main_ac_gen_index_flat_annotated.py",
    "main_ac_gen_lb_flat_stream.py",
    "main_ac_gen_line_break_editor.py",
    "main_ac_kraken_seg_baselines.py",
    "main_ac_merge_line_markers.py",
    "main_ac_plot_col_coords.py",
    "main_ac_wikisource_page.py",
)
"""codex-index-aleppo's fifteen modules at the top of this repo's ``py/``.

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
    """Aleppo Codex page scans (37 tracked JPEG), leaves 270-281 recto and verso.

    DOWNLOADED, not generated: ``download_aleppo_pages`` fetches them from
    archive.org, and no check regenerates them.
    """
    return ac_data_root() / "aleppo-pages"


def mam_xml_dir() -> Path:
    """Pinned 24-file MAM-XML snapshot, the word-sequence ground truth."""
    return paths.repo_root() / "MAM-XML"


def ds_flat_stream_dir() -> Path:
    """Derived per-page flat streams (8 tracked JSON) from
    ``py_ac_loc.gen_flat_stream``."""
    return ac_data_root() / "ds-flat-stream"


def plot_col_coords_out_dir() -> Path:
    """The three tracked PNGs ``py_ac_loc.plot_col_coords`` keeps, as against the
    throwaway copies it also writes into ``novc_dir()``."""
    return ac_data_root() / "plot_col_coords-out"


def novc_dir() -> Path:
    """Gitignored scratch tree, where the two editors and the word previewer write
    the HTML they open in a browser."""
    return ac_data_root() / ".novc"


def wiki_dir() -> Path:
    """``aleppo-wiki/`` -- J David Stark's index, its three derived artifacts, and the
    hand-corrected ``index-flat-corrected.json`` that
    ``main_ac_gen_index_flat_annotated`` reads.

    The moved pipeline and the other Aleppo modules use this accessor rather than
    constructing another spelling of the data root.
    """
    return ac_data_root() / "aleppo-wiki"


def wiki_index_csv_path() -> Path:
    """``aleppo-wiki/J David Stark Aleppo Codex Index.csv``, the wikisource
    pipeline's one input.

    Hand-made and written by no program: J David Stark's index of the Aleppo Codex,
    under the licence in ``LICENSE.txt`` beside it.
    """
    return wiki_dir() / "J David Stark Aleppo Codex Index.csv"


def wiki_index_flat_path() -> Path:
    """``aleppo-wiki/index-flat.json``, the pipeline's first artifact: the CSV's rows
    as JSON.

    Distinct from ``flat_index_corrected_path()``, which is this file with
    corrections applied by hand and is the annotator's input rather than this
    pipeline's output.
    """
    return wiki_dir() / "index-flat.json"


def wiki_index_grouped_path() -> Path:
    """``aleppo-wiki/index-grouped-by-book.json``, the pipeline's second artifact:
    those rows grouped by book."""
    return wiki_dir() / "index-grouped-by-book.json"


def wiki_index_wikitext_path() -> Path:
    """``aleppo-wiki/index.wiki``, the pipeline's third artifact and its point -- the
    wikitext of the Wikisource page."""
    return wiki_dir() / "index.wiki"


def flat_index_corrected_path() -> Path:
    """Hand-corrected flat index (``<wiki_dir>/index-flat-corrected.json``).

    Written by no program: it is ``index-flat.json`` with corrections applied by
    hand, and it is the input to ``gen_index_flat_annotated``.
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


def word_finding_test_data_path() -> Path:
    """``<data_root>/test-data-from-book-of-job.json`` -- the minimal extract of
    book-of-job's enriched quirk records that ``check_word_finding`` runs against."""
    return ac_data_root() / "test-data-from-book-of-job.json"
