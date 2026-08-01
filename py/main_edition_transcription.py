"""Printed-edition transcription workflow.

The interactive, machine-local half of the printed-Decalogue work: it reads a personal scan
archive outside the repo (see WLC_SCANS_DIR) and writes disposable renderings to the
gitignored .novc/scans/.  Kept apart from main_accgram.py deliberately -- that entry point is
corpus runs and page generation, which need no scans and produce tracked output.

Subcommands:
    scan-page
                Render one page (or several) of a book scan, downscaled to something
                readable, to .novc/scans/<stem>.png.  --crop takes four fractions of
                the page in 0..1, left top right bottom, applied before the resize, so
                a quarter-page crop at the same --width doubles the effective
                resolution -- which is what makes merkha vs. meteg legible.  --name
                sets the output stem, so successive crops of one page do not overwrite
                each other, and therefore refuses more than one page.
    editor
                Build a per-line transcription editor over one page, to
                .novc/scans/<stem>-editor.html: the page image with a text field that
                follows the line being transcribed down it, so the eye never leaves
                that line.  --crop's L and R bound the text column, while its T and B
                name the LINES TO TRANSCRIBE -- band detection runs over a region grown
                about a line past them, so a boundary line is never clipped and its
                neighbours come through dimmed as context.  --debug also writes
                <stem>-lines.png with the detected bands drawn on the page.
    zoom-line
                Crop one printed line (or several, or with no line numbers all of
                them) out of the scan a line editor export was read from, padded so
                no accent can be clipped, and echo that line's transcribed text.  The
                band comes from the export's own px_source coordinates, so the zoom is
                anchored to what was transcribed.
    check
                Check a hand transcription against its vendored Wikisource strand, before
                it is committed: name the editor's downloaded export(s) as paths and the
                strand with --key BOOK STRAND KIND, or name an already committed
                transcription with --stem, which takes its strand from the .txt header.
                --site SKELETON NEXT_SKELETON asks a different question -- what every
                strand does at one site, located by the letter skeleton of a word and of
                the word after it.
    build
                Wrap the editor's export(s) into the committed JSON and derive the .txt
                body beneath its hand-written header, which this never rewrites.
                --derive-only re-derives that body from the already-committed JSON, and
                --check writes nothing at all: it re-derives every committed stem and
                exits non-zero if any .txt is not its own derived body.
    highlight-picker
                Build a page for dragging highlight rectangles over a committed scan
                under gh-pages/accgram/img/, to .novc/highlight-picker-<image>.html, and
                export their coordinates for pasting into a page generator.  Authoring
                only: nothing it makes ships, and the page generators hold its output as
                ``mhi.Box`` px boxes.  --boxes-file seeds it with boxes to tweak.

The output is only ever written.  To put a rendering in front of the reader, hand over a
``file:///`` link to it and open nothing -- no Start-Process, no browser pane.

Examples:
    .venv/Scripts/python.exe py/main_edition_transcription.py scan-page \
        "Feldheim Simanim Tiqqun" C246 --width 1100
    .venv/Scripts/python.exe py/main_edition_transcription.py scan-page \
        "Feldheim Simanim Tiqqun" C246 --crop 0.5 0 1 1 --name C246-right
    .venv/Scripts/python.exe py/main_edition_transcription.py editor \
        "Feldheim Simanim Tiqqun" C246 --crop 0.5 0.30 1 0.45 --name C246-v --debug
    .venv/Scripts/python.exe py/main_edition_transcription.py zoom-line \
        in/accgram/edition_transcriptions/simtiq_ex_taxton.json 12 13
    .venv/Scripts/python.exe py/main_edition_transcription.py check \
        --stem simtiq_dt_elyon
    .venv/Scripts/python.exe py/main_edition_transcription.py build --check
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import gen_highlight_picker
from accgram import scan_page
from accgram import transcription_build
from accgram import transcription_check
from accgram import transcription_editor
from accgram import zoom_line
from wlc_cmn.utf8_io import force_utf8_io

import wlc_paths


def _repo_root() -> Path:
    return wlc_paths.wlc_data_root()


def _run_scan_page(args: argparse.Namespace) -> None:
    scan_page.run(args)


def _run_editor(args: argparse.Namespace) -> None:
    transcription_editor.run(args)


def _run_zoom_line(args: argparse.Namespace) -> None:
    zoom_line.run(args)


def _run_check(args: argparse.Namespace) -> None:
    transcription_check.run(args)


def _run_highlight_picker(args: argparse.Namespace) -> None:
    gen_highlight_picker.run(args)


def _run_build(args: argparse.Namespace) -> int:
    # The one subcommand with an exit code to return: --check is an idempotence gate.
    return transcription_build.run(args)


def build_parser() -> argparse.ArgumentParser:
    """The fully-configured parser, so a test can read the subcommands off it."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="subcommand", metavar="SUBCOMMAND")
    subparsers.required = True

    scan_page_parser = subparsers.add_parser(
        "scan-page",
        help=(
            "Render a page of a book scan, downscaled, to .novc/scans/<stem>.png. "
            "--crop L T R B takes fractions of the page in 0..1 and is applied before "
            "the resize; --name sets the output stem and takes one page only."
        ),
    )
    scan_page.add_args(scan_page_parser, repo_root=_repo_root())
    scan_page_parser.set_defaults(func=_run_scan_page)

    editor_parser = subparsers.add_parser(
        "editor",
        help=(
            "Build a per-line transcription editor over one page, to "
            ".novc/scans/<stem>-editor.html. --crop L T R B bounds the text column "
            "left and right and names the lines to transcribe top and bottom; --debug "
            "also writes <stem>-lines.png with the detected bands drawn on."
        ),
    )
    transcription_editor.add_args(editor_parser, repo_root=_repo_root())
    editor_parser.set_defaults(func=_run_editor)

    zoom_line_parser = subparsers.add_parser(
        "zoom-line",
        help=(
            "Crop one printed line out of the scan an export was read from, padded so "
            "no accent can be clipped, and echo its transcribed text. With no line "
            "numbers, every line of the export."
        ),
    )
    zoom_line.add_args(zoom_line_parser, repo_root=_repo_root())
    zoom_line_parser.set_defaults(func=_run_zoom_line)

    check_parser = subparsers.add_parser(
        "check",
        help=(
            "Check a hand transcription against its vendored Wikisource strand. Name the "
            "editor's export(s) as paths with --key BOOK STRAND KIND, or a committed "
            "transcription with --stem; --site SKELETON NEXT_SKELETON instead reports "
            "what every strand does at one site."
        ),
    )
    transcription_check.add_args(check_parser, repo_root=_repo_root())
    check_parser.set_defaults(func=_run_check)

    # Named build_subparser, not build_parser: this function is build_parser().
    build_subparser = subparsers.add_parser(
        "build",
        help=(
            "Wrap the editor's export(s) into the committed JSON and derive the .txt "
            "body under its hand-written header. --derive-only re-derives that body "
            "from the committed JSON; --check writes nothing and exits non-zero if any "
            "committed .txt is not its own derived body."
        ),
    )
    transcription_build.add_args(build_subparser, repo_root=_repo_root())
    build_subparser.set_defaults(func=_run_build)

    highlight_picker_parser = subparsers.add_parser(
        "highlight-picker",
        help=(
            "Build a box-dragging page over a committed scan under gh-pages/accgram/img/, "
            "to .novc/highlight-picker-<image>.html, and export the boxes' coordinates. "
            "--serve runs a local http server; --no-open prints the URL and launches "
            "nothing; --boxes-file seeds the editor with boxes to tweak."
        ),
    )
    gen_highlight_picker.add_args(highlight_picker_parser, repo_root=_repo_root())
    highlight_picker_parser.set_defaults(func=_run_highlight_picker)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    # `or 0` because a subcommand that returns None succeeded; the non-None case is a gate
    # such as transcription_build --check, whose non-zero return has to reach the shell.
    raise SystemExit(args.func(args) or 0)


if __name__ == "__main__":
    force_utf8_io()
    main()
