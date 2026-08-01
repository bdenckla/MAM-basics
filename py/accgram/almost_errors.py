"""Generate gh-pages/accgram/almost-errors.html -- the "almost errors" page.

It documents, in one place, both

  * the **editorial charities** -- places where the accgram checkers silently
    *normalize away* a quirk of WLC (sometimes a genuine Leningrad feature,
    sometimes an artifact introduced in BHS or WLC) and read the text charitably
    rather than flagging it; and

  * one **almost-error that is NOT a charity** -- Ezekiel 20:31's
    ``mahapakh!qadma`` same-letter pair, which looks like an error (two accents
    on one letter) but is a genuine, MAM-confirmed masoretic tradition, not
    a leniency specific to LC/BHS/WLC.

The unifying theme is "almost errors": features that a naive checker would flag,
where the right call -- charity or acceptance -- is a *choice*, and this page makes
those choices visible (with, for the telisha gedola + geresh family, the parse
trees of the chosen kept-both sequence alongside the single-mark readings we did
**not** choose).

The page is **generated** rather than hand-authored for one reason: the telisha
gedola exhibit's parse trees, and the live tree for ek20:31, are produced from the
actual grammar at build time (a mode-aware copy of ``uni_to_marks.word_to_marks``
drives the three telg readings -- the kept-both sequence the checker emits and its
two single-mark alternatives), so they can never drift from the checker's real
behaviour.

This module is the CLI shell.  The "real computing" (mode-aware parse trees and
verdicts) lives in ``almost_errors_trees``; the HTML rendering (page sections and
the shared error-tree table renderer) lives in ``almost_errors_html``.

Run via ``main_accgram.py generate-html`` (read-only; no module is
mutated permanently -- the ``word_to_marks`` swap is scoped and restored).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import rtms_data
from accgram import rtms_report
from accgram.almost_errors_html import REPORT_TITLE, render_body_contents
from accgram.prose_ply_grammar import build_parser
from accgram.prose_scanner import HasLegarmeh
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import provenance
from py_html import wlc_utils_html as H

import wlc_paths


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def default_html_out_path(repo_root: Path) -> Path:
    return wlc_paths.gh_pages_dir() / "accgram" / "almost-errors.html"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--wlc422-kq-u-dir",
        type=Path,
        default=rtms_data.default_wlc422_kq_u_dir(repo_root),
        help="Directory of WLC 4.22 ketiv/qere Unicode 1verses_*.json files.",
    )
    parser.add_argument(
        "--html-out",
        type=Path,
        default=default_html_out_path(repo_root),
        help="Output HTML path for the almost-errors page.",
    )


def run(args: argparse.Namespace) -> None:
    index = rtms_data.load_wlc422_index(args.wlc422_kq_u_dir)
    parser = build_parser()
    has_legarmeh = HasLegarmeh()

    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=render_body_contents(index, parser, has_legarmeh),
        write_ctx=H.WriteCtx(
            title=REPORT_TITLE,
            path=str(html_out),
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )
    print(f"HTML: {html_out}")


def main() -> None:
    force_utf8_io()
    repo_root = wlc_paths.wlc_data_root()
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser, repo_root=repo_root)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
