"""Publish the selected adaptation and the complete font-license asset set."""

import difflib
from pathlib import Path

from mb_cmn import paths as repo_paths
from py_html.taamey_d_assets import product_font_assets
from yeivin_itm import claim_schema, claims, paths, renderer, source_lint


def assets():
    """Return the shared family stylesheet and licensed font mapping."""
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


def review_claims():
    """Report what the current analysis would change in Ben's approved claims.

    Prints each fraction pin whose projected value differs from its approved one,
    each way a form that Ben's footnotes quote fails of the analysis, and each page
    line whose text would change, before and after, all computed in memory. It
    writes nothing and approves nothing: only Ben approves new pins or footnote edits.
    """
    projected, failures = claims.projection()
    report = []
    for name, (numerator, denominator) in claim_schema.APPROVED_FRACTIONS.items():
        value = projected["measurements"][name]
        if (value["numerator"], value["denominator"]) != (numerator, denominator):
            report.append(
                f"Pin {name}: approved {numerator}/{denominator},"
                f" projected {value['numerator']}/{value['denominator']}."
            )
    report.extend(f"Failing {failure}." for failure in failures)
    current = renderer.page_texts()
    proposed = renderer.page_texts(projected)
    for name in sorted(current):
        report.extend(
            difflib.unified_diff(
                current[name].splitlines(),
                proposed[name].splitlines(),
                f"gh-pages/yeivin-itm/{name} (approved)",
                f"gh-pages/yeivin-itm/{name} (projected)",
                n=0,
                lineterm="",
            )
        )
    if not report:
        report.append("No approved pin, quoted form or page line would change.")
    print("\n".join(report))
