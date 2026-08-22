"""Refresh codex-index-leningrad's UXLC-utils-sparse from the UXLC-utils sibling repo.

Copies the designated sparse subset from UXLC-utils into the sibling
codex-index-leningrad's ``UXLC-utils-sparse/``, removes the legacy
``UXLC-utils-sparse/in/UXLC`` directory if it is still there, and writes
``UXLC-utils-sparse/provenance.md`` with the source repo's git metadata -- but only
when a vendored byte actually moved or a legacy path was actually removed, or
``--force-provenance`` is given.  provenance.md stamps the source repo's HEAD and
today's date, so writing it unconditionally left the file dirty after any UXLC-utils
commit and after any re-run on a later day, with nothing else changed.

THAT SPARSE SUBSET IS DATA ONLY, and has been since 2026-08-03.  It held seventeen
of UXLC-utils' own ``.py`` as well -- ``main_uxlc_estimate_atom_loc.py``, five
``uxlc_lci/`` modules and eleven ``uxlc_misc/`` -- and Ben's decision in Phase 5 of
``doc/PLAN-evacuate-python-from-UXLC-utils.md`` was to DROP them rather than repoint
them at MAM-basics, nothing in codex-index-leningrad having imported one and their
entry point having been unable to run there in any case.  Do not vendor the
seventeen back.  What remains is 39 ``in/UXLC-39/*.xml`` and two ``data/lci_*.json``,
one of which -- ``lci_augrecs.json`` -- is the input to
``main_lenin_wikisource_page.py``.

WHY THE NAME CHANGED.  This was codex-index-leningrad's root
``main_update_vendored_files.py`` until Phase 3 of
``doc/PLAN-evacuate-python-from-codex-index-trio.md``, 2026-08-22.  That name was
held by three repos at once and says nothing about which vendored files are meant;
``main_wlc_vendor_uxlc.py`` beside this file does the same job for this repo's own
vendored UXLC subset, and this file is named after it.

WHY IT DOES NOT SHARE THAT FILE'S BODY, tempting as the symmetry is.  The two sync
different shapes: ``main_wlc_vendor_uxlc`` copies two flat directories filtered to
one suffix each, and this one copies a whole subtree recursively and suffix-blind,
which is what ``_content_digest`` below has to mirror.  Either walk applied to the
other's destination sees no files at all and so reports "unchanged" forever.
"""

import argparse
import datetime
import hashlib
import shutil
from pathlib import Path

from mb_cmn import paths
from mb_cmn import vendoring_sync
from wlc_cmn.utf8_io import force_utf8_io

import lenin_paths

_PROVENANCE_BASENAME = "provenance.md"
"""codex-index-leningrad's breadcrumb has no leading underscore.

It is a tracked file of that repo's, named that way since before
``mb_cmn/vendoring_sync.py`` existed, and the two lines that named it were the
whole of the fork this file's predecessor carried of that module.
"""

_LOCAL_ONLY_PATHS = {
    Path(_PROVENANCE_BASENAME),
}

_LEGACY_DEST_DIRS = [
    Path("in/UXLC"),
]


def almost_main(argv: list[str] | None = None) -> None:
    """The body, callable in-process."""
    args = _parse_args(argv)

    source_repo = paths.require_uxlc_utils_dir()
    sparse_root = lenin_paths.uxlc_sparse_dir()
    if not sparse_root.is_dir():
        raise FileNotFoundError(f"Sparse vendored subtree not found at {sparse_root}")

    commit, tag = vendoring_sync.get_git_info(source_repo)
    date_str = datetime.date.today().isoformat()

    synced_paths, content_changed = _sync(source_repo, sparse_root)
    removed_paths = _remove_legacy_paths(sparse_root)
    # A legacy removal is recorded in provenance.md's own "Legacy paths removed:"
    # section, so it is as much a reason to rewrite the file as a copied byte is.
    changed = content_changed or bool(removed_paths)

    wrote = _maybe_write_provenance(
        sparse_root,
        source_rel="UXLC-utils",
        copied_files=synced_paths,
        commit=commit,
        tag=tag,
        date_str=date_str,
        title="Provenance of UXLC-utils-sparse",
        removed_paths=removed_paths,
        changed=changed,
        force=args.force_provenance,
    )

    _report(sparse_root, synced_paths, changed, wrote)
    if removed_paths:
        print(f"Removed {len(removed_paths)} legacy paths")
    print(f"UXLC-utils commit: {commit}")
    if tag:
        print(f"UXLC-utils tag:    {tag}")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force-provenance",
        action="store_true",
        help=(
            "Rewrite provenance.md even when no vendored file content changed and no "
            "legacy path was removed. By default provenance.md is left untouched (no "
            "date/commit bump) when the sync copied no new content."
        ),
    )
    return parser.parse_args(argv)


def _sync(source_repo: Path, sparse_root: Path) -> tuple[list[str], bool]:
    """Copy existing local vendored files, returning (copied_files, content_changed)."""
    before = _content_digest(sparse_root)
    copied = vendoring_sync.copy_by_intersection(
        source_repo,
        sparse_root,
        include_suffixes=None,
        strict=True,
        recursive=True,
        exclude_rel_paths=[rel_path.as_posix() for rel_path in _LOCAL_ONLY_PATHS],
    )
    changed = _content_digest(sparse_root) != before
    return copied, changed


def _content_digest(dest_dir: Path) -> dict[str, str]:
    """Map each vendored path under dest_dir to a hash of its bytes.

    Recursive and suffix-blind, because the sync it has to mirror is: the
    copy_by_intersection call above runs with recursive=True and
    include_suffixes=None over data/ and in/UXLC-39/. The sibling instance of this
    idiom, main_wlc_vendor_uxlc.py, walks one flat directory and filters to one
    suffix; that walk here would see no files at all and so report "unchanged"
    forever. provenance.md is skipped because it is the file being decided about.
    """
    excluded = {rel_path.as_posix() for rel_path in _LOCAL_ONLY_PATHS}
    digest: dict[str, str] = {}
    for path in dest_dir.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        rel_posix = path.relative_to(dest_dir).as_posix()
        if rel_posix in excluded:
            continue
        digest[rel_posix] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def _remove_legacy_paths(sparse_root: Path) -> list[str]:
    removed: list[str] = []
    for rel_path in _LEGACY_DEST_DIRS:
        dest_path = sparse_root / rel_path
        if not dest_path.exists():
            continue
        if dest_path.is_dir():
            shutil.rmtree(dest_path)
        else:
            dest_path.unlink()
        removed.append(rel_path.as_posix())
    return removed


def _maybe_write_provenance(
    dest_dir: Path,
    *,
    source_rel: str,
    copied_files: list[str],
    commit: str,
    tag: str | None,
    date_str: str,
    title: str,
    removed_paths: list[str],
    changed: bool,
    force: bool,
) -> bool:
    """Write provenance.md only when something changed (or force). Return whether written."""
    if not (changed or force):
        return False
    vendoring_sync.write_provenance(
        dest_dir,
        source_rel=source_rel,
        copied_files=copied_files,
        commit=commit,
        tag=tag,
        date_str=date_str,
        title=title,
        removed_paths=removed_paths,
        basename=_PROVENANCE_BASENAME,
    )
    return True


def _report(dest_dir: Path, copied: list[str], changed: bool, wrote: bool) -> None:
    if wrote:
        provenance = "provenance updated" if changed else "provenance forced"
    else:
        provenance = "unchanged, provenance kept"
    rel = dest_dir.relative_to(lenin_paths.lenin_data_root())
    print(
        f"{lenin_paths.DATA_REPO_NAME}/{rel}: synced {len(copied)} files ({provenance})"
    )


if __name__ == "__main__":
    force_utf8_io()
    almost_main()
