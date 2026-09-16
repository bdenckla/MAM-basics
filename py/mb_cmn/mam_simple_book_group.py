"""Resolve one MAM-simple book-group file under the incremental-folder rule."""

from collections.abc import Sequence
from pathlib import Path

_FORMAT_SUFFIXES = {
    "json": ".json",
    "xml": ".xml",
}
_DIRECTORY_NAMES = {
    ("json", "mam"): "json-vtrad-mam",
    ("json", "bhs"): "json-vtrad-bhs",
    ("json", "sef"): "json-vtrad-sef",
    ("xml", "mam"): "xml-vtrad-mam",
    ("xml", "bhs"): "xml-vtrad-bhs",
    ("xml", "sef"): "xml-vtrad-sef",
}
_VERSIFICATIONS = ("mam", "bhs", "sef")


def resolve_book_group_path(
    mam_simple_root: Path,
    *,
    fmt: str,
    vtrad: str,
    stems: Sequence[str],
    requested_dir: Path | None = None,
    allow_mam_fallback: bool = True,
) -> Path:
    """Return the first existing requested or MAM-base book-group candidate.

    ``fmt`` and ``vtrad`` dispatch through literal maps. The candidates retain the
    caller's stem order within each directory, while directory priority remains the
    requested tradition first and the MAM base second. A caller-supplied nonstandard
    directory can disable the MAM fallback explicitly; no sibling is inferred from
    that directory's shape or contents.
    """
    try:
        suffix = _FORMAT_SUFFIXES[fmt]
    except KeyError as exc:
        raise ValueError(
            f"Unknown MAM-simple format {fmt!r}; expected one of"
            f" {tuple(_FORMAT_SUFFIXES)}"
        ) from exc
    if vtrad not in _VERSIFICATIONS:
        raise ValueError(
            f"Unknown MAM-simple versification {vtrad!r}; expected one of"
            f" {_VERSIFICATIONS}"
        )
    if (
        isinstance(stems, (str, bytes))
        or not stems
        or any(not isinstance(stem, str) or not stem for stem in stems)
    ):
        raise ValueError("MAM-simple book-group stems must be nonempty strings")

    root = Path(mam_simple_root)
    requested = (
        Path(requested_dir)
        if requested_dir is not None
        else root / _DIRECTORY_NAMES[(fmt, vtrad)]
    )
    directories = [requested]
    if allow_mam_fallback and vtrad in {"bhs", "sef"}:
        directories.append(root / _DIRECTORY_NAMES[(fmt, "mam")])

    attempts = [
        directory / f"{stem}{suffix}" for directory in directories for stem in stems
    ]
    for candidate in attempts:
        if candidate.is_file():
            return candidate

    tried = ", ".join(str(path) for path in attempts)
    raise FileNotFoundError(
        f"No MAM-simple {fmt} book group for {vtrad}; tried {tried}"
    )
