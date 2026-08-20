"""Resolve the book-of-job DATA root, and the places in this repo its CODE now sits.

THIS MODULE IS DELIBERATELY TWO-ROOTED, and that is the whole point of its
existence.  The code is here in MAM-basics since Phase 3 of
``doc/PLAN-evacuate-python-from-book-of-job.md``; the corpus it reads and writes
stayed in the sibling book-of-job, along with the Pages site served out of it:

  * the DATA root is ``boj_data_root()`` -- book-of-job's ``gh-pages/``, ``out/``
    and gitignored ``.novc/``, 701 tracked artifacts between the first two;
  * the CODE is under this repo's ``py/``, and is NOT a subtree: seven packages
    plus seventeen top-level modules, listed in ``BOJ_PACKAGES`` and
    ``BOJ_TOP_LEVEL_MODULES`` below and returned together by ``code_paths()``.

The two were named apart *before* the move, while the code still ran in book-of-job
and that repo's 701 tracked artifacts were an oracle that could prove a path change
harmless (Phase 1 of the same plan).  The move itself then changed the body of
``boj_data_root()`` and nothing else about how data is addressed, because no other
module composes a data path off anything but that function.

What this replaced is of two kinds, and only the first kind is greppable.  Plain
cwd-relative literals -- ``"gh-pages/jobn"``, ``"./out"``, ``Path("author_boj_qr")``,
an argparse ``default="gh-pages"`` -- resolved correctly only while the process ran
from book-of-job's root, and one of them would have overwritten this repo's own
tracked ``gh-pages/index.html`` had a verification run been done from here.  The
second kind is a ``Path(__file__)`` walk that was cwd-independent already and still
conflated the two roots: ``check_spelling_in_html.main`` composed the ``gh-pages``
tree it reads and the custom dictionary that sits beside its own module off one
``Path(__file__).parent``, which is one expression standing for both roots at once.

WHY ``code_paths()`` IS A LIST AND NOT A ROOT.  In book-of-job the four source
lints -- ``check_function_ordering``, ``check_mark_order``,
``check_escape_sequences`` and their ``fix_*`` counterparts -- scanned the repo
root, which held nothing but this code.  Here that same root holds all of
MAM-basics, and none of the three checks has a repo-wide meaning: measured
2026-08-19, function ordering reports 1172 violations across ``py/`` and 0 across
the book-of-job packages, mark order reports violations in ``py/ws/``, and the
escape check reports them in ``py/wlc_cmn/``.  So the lints take their scope from
this module rather than from a ``.git`` walk, and the price is that the two tuples
below are hand-maintained: a book-of-job module added to ``py/`` and not listed
here goes unlinted.  The list is checked for existence by ``code_paths()``, so a
RENAMED or deleted entry fails loudly; only an unlisted ADDITION is silent, and
book-of-job's Python is being evacuated rather than developed.

WHY THIS DELEGATES TO ``mb_cmn.paths`` NOW, having refused to before.  In
book-of-job ``paths.repo_root()`` was ``Path(__file__).resolve().parents[2]``,
correct for a ``py/mb_cmn/`` two levels down and wrong at that repo's root-level
``mb_cmn/``, where the walk landed on ``GitRepos``; that is why the pre-move
version of this file walked up to ``.git`` instead and deliberately vendored
nothing.  Here the depth is the one ``paths.py`` is written for, and
``py/uxlc_paths.py`` and ``py/hkq_paths.py`` are the two worked precedents.

WHERE THE UXLC DATA COMES FROM NOW.  ``uxlc_dir()`` and ``lci_recs_path()`` stood
here until Phase 3 and are gone: the location estimate runs on ``uxlc_misc`` and
``uxlc_lci``, the lineage Ben chose 2026-08-19, which address their own inputs
through ``uxlc_paths``.  Nothing is lost by that, and it was measured rather than
assumed -- book-of-job's ``py_uxlc_loc/UXLC/``, this repo's ``in/UXLC-39/`` and
UXLC-utils' ``in/UXLC-39/`` are one blob in all 39 books, and book-of-job's
``lci_recs.json`` differs from UXLC-utils' ``data/lci_recs.json`` in one line of
the header's column dictionary, the ``body`` that ``unflatten_many`` reads being
identical.
"""

from pathlib import Path

from mb_cmn import paths

BOJ_PACKAGES = (
    "author_boj",
    "author_boj_qr",
    "author_boj_util",
    "boj_render",
    "py_ac_word_image_helper",
    "py_cam1753_word_image",
    "pydiff_mm",
)
"""The seven packages book-of-job's Python landed in, under this repo's ``py/``.

``author_boj_qr`` was ``pyauthor_qr``, ``author_boj_util`` was ``pyauthor_util``,
``author_boj`` was ``pyauthor`` and ``boj_render`` was that repo's own ``py/`` --
four renames Ben settled together 2026-08-19, the fourth because ``py/`` held
``hebrew_letter_words.py`` and ``uni_heb_char_classes.py``, which as top-level
modules here would have collided by meaning with ``mb_misc/hebrew_letter_words.py``:
two module objects for one name, reached with no ``sys.path`` line at all.  The
other three kept their names, ``pydiff_mm`` being distinct from ``mb_diff_mpu`` and
the two word-image packages being one blob each with a codex-index repo's copy.
"""

BOJ_TOP_LEVEL_MODULES = (
    "boj_paths.py",
    "check_all.py",
    "check_escape_sequences.py",
    "check_function_ordering.py",
    "check_html_syntax_and_sanity.py",
    "check_mark_order.py",
    "check_qr_consistency.py",
    "check_qr_relations.py",
    "check_spelling_in_html.py",
    "fix_escape_sequences.py",
    "fix_mark_order.py",
    "main_apply_cam1753_crops.py",
    "main_gen_aleppo_crop_editor.py",
    "main_gen_cam1753_crop_editor.py",
    "main_gen_misc_authored_english_documents.py",
    "main_list_missing_aleppo_imgs.py",
)
"""book-of-job's sixteen runnable modules, which sat at that repo's root and sit at
the top of this repo's ``py/``.

They stay top-level rather than going into a package because every one of them is
an entry point: five ``main_*``, and the ``check_*``/``fix_*`` family that
``check_all`` imports by bare name and that are also run singly.  A package would
make ``python py/<pkg>/check_mark_order.py`` put the package directory on
``sys.path`` instead of ``py/``, which is the import surgery this repo has none of.
"""

BOJ_TOP_LEVEL_DATA_FILES = ("check_spelling_in_html.custom-dict.json",)
"""Non-Python files of book-of-job's that are CODE and travel with the module beside
them.

There is one, and it is here rather than left in the data root because
``check_spelling_in_html`` addresses it off ``Path(__file__).parent``: it is the
half of that module's old single root which follows the Python, the other half
being the ``gh-pages`` tree it reads.  Listed so that ``check_mark_order``, which
scans ``.json`` as well as ``.py``, still sees it.
"""

DATA_REPO_NAME = "book-of-job"

D1D_DIR = "jobn-details"
"""Directory name of the per-quirk detail pages, under ``gh_pages_dir()``.

Defined here rather than in ``author_boj_util.common_titles_etc``, which imports it
from here, because the name is used as a path segment AND as an href segment
(``d1d_detail_href``) and the two must not drift apart.
"""


def code_dir() -> Path:
    """This repo's ``py/`` -- the directory this module and the moved code sit in.

    Spelled off ``__file__`` rather than off ``paths.repo_root() / "py"`` so that it
    stays right if this module is ever moved again, which is the same reasoning the
    pre-move version gave for walking to ``.git`` rather than counting ``parents[N]``.
    """
    return Path(__file__).resolve().parent


def qr_package_dir() -> Path:
    """The quirk-record package (``<code_dir>/author_boj_qr``), 160 one-dict modules.

    ``check_qr_consistency`` scans it for filename/``RECORD_*``/word-id agreement.
    """
    return code_dir() / "author_boj_qr"


def code_paths() -> list[Path]:
    """Every place book-of-job's Python lives here, for the four source lints.

    Fails loudly on an entry that no longer exists -- see the module docstring for
    what this list can and cannot catch.
    """
    named = [code_dir() / name for name in BOJ_PACKAGES]
    named += [code_dir() / name for name in BOJ_TOP_LEVEL_MODULES]
    named += [code_dir() / name for name in BOJ_TOP_LEVEL_DATA_FILES]
    missing = [p for p in named if not p.exists()]
    if missing:
        raise SystemExit(
            "boj_paths.code_paths: no longer present: "
            + ", ".join(str(p) for p in missing)
        )
    return named


def boj_data_root() -> Path:
    """Path to the book-of-job corpus this code reads and writes.

    The one line that changed when the Python moved out -- see the module docstring.
    """
    return paths.require_sibling("book-of-job", paths.sibling_repo("book-of-job"))


def gh_pages_dir() -> Path:
    """Published-HTML tree, 694 tracked files, served at bdenckla.github.io/book-of-job.

    THE DEPLOY ROOT, not any one document under it: ``.github/workflows/pages.yml``
    hands exactly this directory to ``upload-pages-artifact``.  515 of those 694 are
    PNGs that no program in this repo writes, so a full regeneration rewrites a
    minority of this tree; see the plan's Phase 0 record for the split.
    """
    return boj_data_root() / "gh-pages"


def out_dir() -> Path:
    """Generated-JSON tree, 7 tracked files.

    Six are written by ``main_gen_misc_authored_english_documents``; the seventh,
    ``cam1753_crops_path()`` below, is appended to by the manual crop-ingest step
    and is the one file of the 701 whose checkout is still CRLF.
    """
    return boj_data_root() / "out"


def novc_dir() -> Path:
    """Gitignored scratch tree (``<data_root>/.novc``), where the two crop editors write."""
    return boj_data_root() / ".novc"


def jobn_dir() -> Path:
    """The main document's own directory (``<gh_pages_dir>/jobn``).

    Passed down the authoring pipeline as ``jobn_rel_top`` and used there purely as a
    filesystem path -- to delete stale HTML, to write each page, and to test whether an
    optional image exists.  The hrefs that reach the published pages are built from the
    bare filename instead, which is why turning this from a relative string into an
    absolute path leaves every artifact byte-identical.
    """
    return gh_pages_dir() / "jobn"


def jobn_img_dir() -> Path:
    """The main document's image tree (``<jobn_dir>/img``), 485 tracked PNGs."""
    return jobn_dir() / "img"


def aleppo_img_dir() -> Path:
    """Aleppo crops (``<jobn_img_dir>/Aleppo``), 160 tracked PNGs, written by no program here."""
    return jobn_img_dir() / "Aleppo"


def cam1753_img_dir() -> Path:
    """Cam1753 crops (``<jobn_img_dir>/cam1753``), 160 tracked PNGs.

    The only image tree here with even a manual producer: ``main_apply_cam1753_crops``
    writes it from a hand-made crop-editor export it takes as its argument.
    """
    return jobn_img_dir() / "cam1753"


def jobn_details_dir() -> Path:
    """The per-quirk detail pages (``<gh_pages_dir>/jobn-details``), 160 tracked HTML."""
    return gh_pages_dir() / D1D_DIR


def index_html_path() -> Path:
    """The site's landing page (``<gh_pages_dir>/index.html``).

    Spelled ``"gh-pages/index.html"`` until Phase 1, which is the same relative path
    MAM-basics' own landing page has -- so a verification run from MAM-basics, the
    convention the UXLC-utils and holman-ketiv-qere plans both used, would have
    overwritten a tracked file there rather than failing.
    """
    return gh_pages_dir() / "index.html"


def enriched_quirkrecs_path() -> Path:
    """The enriched quirk records (``<out_dir>/enriched-quirkrecs.json``).

    Written by ``main_gen_misc_authored_english_documents`` and read at MODULE IMPORT
    TIME by the two crop editors and by ``main_list_missing_aleppo_imgs``, which is the
    only sequencing among this repo's five entry points.
    """
    return out_dir() / "enriched-quirkrecs.json"


def cam1753_crops_path() -> Path:
    """Hand-made crop coordinates (``<out_dir>/cam1753-crops.json``), read by the authoring
    pipeline and appended to by ``main_apply_cam1753_crops``."""
    return out_dir() / "cam1753-crops.json"
