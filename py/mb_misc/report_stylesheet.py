"""Reference or package the authored report base and deploy its reports' Hebrew font."""

from pathlib import Path

from mb_cmn import paths


def prepare_report_stylesheet(
    output_dir: Path,
    *,
    shared_href: str | None,
) -> str:
    """Return a shared href, or copy the base locally when ``shared_href`` is None.

    Published generation and temporary differential generation pass the same logical
    href. Neither writes the hand-authored base at ``gh-pages/report.css``.
    Standalone generation copies that base into its own output directory.
    """
    source = paths.gh_pages_dir() / "report.css"
    content = source.read_bytes()
    if shared_href is not None:
        return shared_href
    relative_path = Path("report-assets") / "report.css"
    destination = output_dir / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return relative_path.as_posix()


def copy_report_font(output_dir: Path) -> None:
    """Copy the canonical Taamey D font, failing if its source is missing."""
    source = paths.repo_root() / "doc" / "woff2" / "Taamey_D.woff2"
    content = source.read_bytes()
    destination = output_dir / "woff2" / source.name
    if destination.is_file() and destination.read_bytes() == content:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
