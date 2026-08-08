"""Resolve the wlc-utils DATA root and the sibling repos the wlc code reads.

THIS MODULE IS DELIBERATELY TWO-ROOTED, and that is the whole point of its
existence.  The code that imports it lives in MAM-basics; the corpus it reads and
writes -- ``in/``, ``out/``, ``gh-pages/``, ``data/`` and the gitignored ``.novc/``
-- lives in wlc-utils, which stayed a data-and-docs repo when the Python moved out
of it (``doc/PLAN-evacuate-python-from-wlc-utils.md``).  So:

  * the CODE root is ``mb_cmn.paths.repo_root()``, this repo -- what ``py/`` and
    ``py/tests/`` are under, what the source lints scan, what ``gh`` and
    ``git worktree`` act on;
  * the DATA root is ``wlc_data_root()`` below, the wlc-utils clone.

``repo_root()`` used to answer both questions with one value.  It was renamed
rather than aliased when the two diverged: in a repo whose actual root is
elsewhere the old name is actively misleading, and renaming forced every call site
to be looked at instead of quietly resolving to the plausible wrong tree.

``.novc/`` stays under the DATA root, and MAM-basics keeps its own -- two scratch
dirs, each in the repo whose data it concerns.  Moving it here would break
``accgram.gen_highlight_picker``, whose generated page carries
``img_url = "../gh-pages/accgram/img/<name>"``, a path relative to the picker
page's own ``.novc/`` location; under MAM-basics that resolves to a
``gh-pages/accgram/img`` that does not exist, and it breaks the ordinary
``file://`` open, not just the opt-in ``--serve`` mode.  Keeping it here also
leaves ``accgram.scan_page``'s ``.novc/scans`` and wlc-utils' own ``.gitignore``
line working with no edit.

Sibling-repo resolution (MAM-simple, wlc-utils-private, UXLC-utils, al-hatorah,
and wlc-utils itself) is ``mb_cmn.paths``' job, not a second copy here: the
override chain and ``require_sibling`` originated in this module and were absorbed
there in Phase 2 of that plan, so the fix lives in the module every program
imports.  The three names below delegate.
"""

from __future__ import annotations

from pathlib import Path

from mb_cmn import paths


def wlc_data_root() -> Path:
    """Path to the wlc-utils clone: the corpus this code reads and writes.

    NOT the root of the repo this module lives in -- see the module docstring.  It
    is ``require_sibling``-checked, so a missing or misplaced clone fails naming
    both environment overrides instead of composing a path into nothing.
    """
    return paths.require_sibling("wlc-utils", paths.sibling_repo("wlc-utils"))


def out_dir() -> Path:
    """wlc-utils' generated-output tree (``<wlc_data_root>/out``)."""
    return wlc_data_root() / "out"


def in_dir() -> Path:
    """wlc-utils' committed-input tree (``<wlc_data_root>/in``)."""
    return wlc_data_root() / "in"


def gh_pages_dir() -> Path:
    """wlc-utils' published-HTML tree (``<wlc_data_root>/gh-pages``)."""
    return wlc_data_root() / "gh-pages"


def data_dir() -> Path:
    """wlc-utils' hand-curated data tree (``<wlc_data_root>/data``)."""
    return wlc_data_root() / "data"


def novc_dir() -> Path:
    """wlc-utils' gitignored scratch tree (``<wlc_data_root>/.novc``).

    Named for the ``.gitignore`` entry rather than for what it holds, because what it holds
    is deliberately unclassified: whatever a run wants to write and nobody wants to commit.
    An accessor rather than each caller composing ``wlc_data_root() / ".novc"`` -- four did,
    one of them off its own ``Path(__file__)`` walk -- so the string appears once.
    """
    return wlc_data_root() / ".novc"


def scans_dir() -> Path:
    """Where page renderings from the scan archive are written (``<novc_dir>/scans``).

    NOT the scan archive itself, which is a personal collection outside every repo and is
    resolved by ``accgram.scan_page.SCANS`` off ``WLC_SCANS_DIR``.  These are the
    downscaled, cropped derivatives, which are disposable and can be large.
    """
    return novc_dir() / "scans"


def siblings_root() -> Path:
    """``mb_cmn.paths.repos_root`` under this module's older name."""
    return paths.repos_root()


def sibling(name: str) -> Path:
    """``mb_cmn.paths.sibling_repo`` under this module's older name."""
    return paths.sibling_repo(name)


def require_sibling(name: str, path: Path) -> Path:
    """``mb_cmn.paths.require_sibling``, re-exported so wlc call sites need no edit."""
    return paths.require_sibling(name, path)


def mam_simple_dir() -> Path:
    """MAM-simple's ``json-vtrad-bhs`` subtree: one JSON per book, verse-element streams."""
    return sibling("MAM-simple") / "json-vtrad-bhs"


def require_mam_simple_dir() -> Path:
    """``mam_simple_dir``, checked -- see ``require_sibling`` for why this is not a skip."""
    return require_sibling("MAM-simple", mam_simple_dir())


def mam_simple_vtrad_mam_dir() -> Path:
    """MAM-simple's ``json-vtrad-mam``: the same text in MAM's native versification.

    ``mam_simple_dir`` above is the BHS versification, which is what this repo's surveys read
    because they are keyed to WLC's refs.  A cross-check against another MAM-derived text numbers
    its verses MAM's way, so it wants this flavour and no remap table.  MAM-simple ships three --
    BHS, Sefaria and MAM native -- and picking the wrong one is what makes versification look like
    a difference between two texts rather than between two numberings of one.
    """
    return sibling("MAM-simple") / "json-vtrad-mam"


def require_mam_simple_vtrad_mam_dir() -> Path:
    """``mam_simple_vtrad_mam_dir``, checked -- see ``require_sibling`` for why this is not a skip."""
    return require_sibling("MAM-simple", mam_simple_vtrad_mam_dir())


def mam_parsed_plus_dir() -> Path:
    """MAM-parsed's ``plus`` subtree: one JSON per book24, minirow cells C/D/E."""
    return sibling("MAM-parsed") / "plus"


def require_mam_parsed_plus_dir() -> Path:
    """``mam_parsed_plus_dir``, checked -- see ``require_sibling`` for why this is not a skip."""
    return require_sibling("MAM-parsed", mam_parsed_plus_dir())


def wlc_utils_private_dir() -> Path:
    """The dated 2025-03-21 WLC snapshots and their derived JSONs, which
    ``main_wlc_json_and_unicode.py`` both reads and writes.

    A subdirectory of MAM-private since 2026-08-08, not a sibling clone of its own: the
    private evacuation programme moved every tracked file of ``bdenckla/wlc-utils-private``
    under ``MAM-private\\wlc-utils-private\\`` and emptied that repo to a breadcrumb README
    (`MAM-private\\doc\\PLAN-evacuate-private-repos.md`, phases R.0-R.4).  So the env
    override that moves this tree is now ``REPO_MAM_PRIVATE_DIR``; ``REPO_WLC_UTILS_PRIVATE_DIR``
    no longer reaches it, there being no sibling by that name to resolve.
    """
    return sibling("MAM-private") / "wlc-utils-private"


def mam_basics_dir() -> Path:
    return sibling("MAM-basics")


def require_mam_basics_dir() -> Path:
    """``mam_basics_dir``, checked -- see ``require_sibling`` for why this is not a skip."""
    return require_sibling("MAM-basics", mam_basics_dir())


def al_hatorah_phonetic_dir() -> Path:
    """al-hatorah's ``io/a01-phonetic-std-set``: Phonetic MAM, one JSON per book.

    Each chanted word has a ``jta`` field whose ``!`` immediately precedes the stressed
    syllable, which is what makes this an independent oracle for ``accgram.final_stress``.  The
    engine behind it is al-hatorah's ``py/aht_phon``, which cannot be imported here -- issue wlc-utils#48
    calls consuming these outputs its second path, and this is that path.
    """
    return sibling("al-hatorah") / "io" / "a01-phonetic-std-set"


def require_al_hatorah_phonetic_dir() -> Path:
    """``al_hatorah_phonetic_dir``, checked -- see ``require_sibling`` for why this is not a skip."""
    return require_sibling("al-hatorah", al_hatorah_phonetic_dir())


def uxlc_utils_dir() -> Path:
    return sibling("UXLC-utils")


def require_uxlc_utils_dir() -> Path:
    """``uxlc_utils_dir``, checked -- see ``require_sibling`` for why this is not a skip."""
    return require_sibling("UXLC-utils", uxlc_utils_dir())
