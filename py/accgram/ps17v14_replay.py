"""Shared helper for the two generated Psalms 17:14 deep-dive pages.

Both pages were formerly hand-authored HTML.  Their bodies are now committed as
Python data modules (``TITLE`` + ``BODY``, migrated byte-exactly from the original
JSON sidecars), and these generators replay that body through the shared
(style.css + provenance) shell so the pages match the look and feel of the other
accgram reports.  The per-page modules (``ps17v14_doc_notes``,
``ps17v14_double_tsinnor``) are thin CLI shells over ``write_replayed`` here, each
passing its own body module.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import wlc_paths
from accgram import rtms_report
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import provenance
from py_html import wlc_utils_html as H

_WIDTH_CLASS = "goerwitz-tms-width-limited"


def add_html_out_arg(parser: argparse.ArgumentParser, default_out: Path) -> None:
    parser.add_argument(
        "--html-out",
        type=Path,
        default=default_out,
        help="Output HTML path.",
    )


def write_replayed(html_out: Path, body_module, generator_file: str) -> None:
    """Render the committed htel body module (``TITLE``/``BODY``) into ``html_out``."""
    title, body = body_module.TITLE, body_module.BODY
    wrapper = H.div(tuple(body), {"class": _WIDTH_CLASS})
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=(wrapper,),
        write_ctx=H.WriteCtx(
            title=title,
            path=str(html_out),
            html_comment=provenance.generated_html_comment(generator_file),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )
    print(f"HTML: {html_out}")


def main_for(
    *, body_module, out_name: str, generator_file: str, description: str
) -> None:
    force_utf8_io()
    default_out = wlc_paths.gh_pages_dir() / "accgram" / out_name
    parser = argparse.ArgumentParser(description=description)
    add_html_out_arg(parser, default_out)
    args = parser.parse_args()
    write_replayed(args.html_out, body_module, generator_file)
