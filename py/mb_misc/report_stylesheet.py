"""Reference or package the authored report base and the site's Hebrew font."""

from pathlib import Path
import posixpath

from mb_cmn import paths
from py_html import taamey_d_assets


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


def prepare_report_font(output_dir: Path, *, report_css_href: str | None) -> str:
    """Return the Taamey D URL for a report stylesheet that sits beside its page.

    A report that links the shared base at ``report_css_href`` loads the site's one
    font, which sits beside that base under ``woff2/``, so published and temporary
    differential generation get the same URL and neither writes a font. A standalone
    report, whose ``report_css_href`` is None, gets its own copy of the pinned font in
    ``woff2/`` inside ``output_dir``.
    """
    if report_css_href is not None:
        return posixpath.join(posixpath.dirname(report_css_href), taamey_d_assets.FONT)
    content = taamey_d_assets.font_bytes()
    destination = output_dir / taamey_d_assets.FONT
    if not (destination.is_file() and destination.read_bytes() == content):
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    return taamey_d_assets.FONT
