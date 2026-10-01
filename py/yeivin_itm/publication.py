"""Publish the selected adaptation and the complete font-license asset set."""

from pathlib import Path

from mb_cmn import paths as repo_paths
from py_html.taamey_d_assets import product_font_assets
from yeivin_itm import claims, paths, renderer, source_lint


def assets():
    """Return the byte-identical historical stylesheet and licensed font mapping."""
    result = product_font_assets("yeivin-itm")
    result["yeivin-itm/style.css"] = (
        Path(__file__).with_name("assets") / "style.css"
    ).read_bytes()
    return result


def output_bytes():
    """Validate every complete page and asset before permitting any write."""
    source_lint.check()
    pages = renderer.page_texts()
    result = assets()
    result.update(
        {f"yeivin-itm/{name}": text.encode("utf-8") for name, text in pages.items()}
    )
    return result


def render():
    """Write only repository-local pages and their font-source support."""
    outputs = output_bytes()
    root = repo_paths.gh_pages_dir()
    for relative, data in outputs.items():
        destination = root / relative
        if destination.is_file() and destination.read_bytes() == data:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)


def check():
    """Compare claims, pages, and assets with regeneration, without writing."""
    claims.check()
    outputs = output_bytes()
    root = repo_paths.gh_pages_dir()
    for relative, data in outputs.items():
        destination = root / relative
        if not destination.is_file() or destination.read_bytes() != data:
            raise ValueError(f"Yeivin output differs from regeneration: {relative}")
    expected = {
        relative.removeprefix("yeivin-itm/")
        for relative in outputs
        if relative.startswith("yeivin-itm/")
    }
    found = {
        path.relative_to(paths.pages_dir()).as_posix()
        for path in paths.pages_dir().rglob("*")
        if path.is_file()
    }
    if found != expected:
        raise ValueError(f"Unexpected Yeivin output files: {found ^ expected}")
