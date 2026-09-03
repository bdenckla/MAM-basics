"""Refresh codex-index-leningrad's temporary UXLC sparse vendor from MAM-basics.

The Phase 5 UXLC-utils evacuation keeps ``UXLC-utils-sparse/`` temporarily, by
Ben's 2026-09-03 authorization, while the codex-index-leningrad lane remains
outside this phase. The source is MAM-basics' own canonical ``in/UXLC-39/``,
``in/lci_recs.json``, and ``uxlc/data/lci_augrecs.json`` files. The script removes the legacy
``UXLC-utils-sparse/in/UXLC`` directory if it remains and writes
``UXLC-utils-sparse/provenance.md`` only when a vendored byte or legacy path
changes, or ``--force-provenance`` is given.

The sparse subset is data only: 39 XML files and two ``data/lci_*.json`` files.
It must not regain the seventeen Python files retired when the codex-index trio's
Python moved to MAM-basics. ``lci_augrecs.json`` remains the input to
``main_lenin_wikisource_page.py``.
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
import uxlc_paths

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

    source_repo = paths.repo_root()
    sparse_root = lenin_paths.uxlc_sparse_dir()
    if not sparse_root.is_dir():
        raise FileNotFoundError(f"Sparse vendored subtree not found at {sparse_root}")

    commit, tag = vendoring_sync.get_git_info(source_repo)
    date_str = datetime.date.today().isoformat()

    synced_paths, content_changed = _sync(sparse_root)
    removed_paths = _remove_legacy_paths(sparse_root)
    # A legacy removal is recorded in provenance.md's own "Legacy paths removed:"
    # section, so it is as much a reason to rewrite the file as a copied byte is.
    changed = content_changed or bool(removed_paths)

    wrote = _maybe_write_provenance(
        sparse_root,
        source_rel="MAM-basics (in/UXLC-39, in/lci_recs.json and uxlc/data)",
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
    print(f"MAM-basics commit: {commit}")
    if tag:
        print(f"MAM-basics tag:    {tag}")


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


def _sync(sparse_root: Path) -> tuple[list[str], bool]:
    """Copy the two retained canonical inputs into the old sparse-tree shape."""
    before = _content_digest(sparse_root)
    copied = vendoring_sync.copy_by_intersection(
        uxlc_paths.uxlc_39_dir(),
        sparse_root / "in" / "UXLC-39",
        include_suffixes=None,
        strict=True,
        recursive=True,
    )
    copied = [f"in/UXLC-39/{path}" for path in copied]
    data_sources = {
        "lci_augrecs.json": uxlc_paths.data_dir() / "lci_augrecs.json",
        "lci_recs.json": uxlc_paths.lci_recs_path(),
    }
    for basename, source_path in data_sources.items():
        destination = sparse_root / "data" / basename
        if not source_path.is_file():
            raise FileNotFoundError(f"Canonical source data is absent: {source_path}")
        if not destination.is_file():
            raise FileNotFoundError(f"Sparse destination is absent: {destination}")
        shutil.copy2(source_path, destination)
        copied.append(f"data/{basename}")
    changed = _content_digest(sparse_root) != before
    return copied, changed


def _content_digest(dest_dir: Path) -> dict[str, str]:
    """Map each vendored path under dest_dir to a hash of its bytes.

    The source has two different canonical locations: ``in/UXLC-39/`` and the
    two data files. The digest covers the resulting single sparse tree, while
    excluding provenance.md because that file is what this command decides
    whether to rewrite.
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
