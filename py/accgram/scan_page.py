"""Bring up a page of a book scan, downscaled to something readable.

Usage:
    .venv/Scripts/python.exe py/main_edition_transcription.py scan-page <book-dir> \
        <name> [<name> ...] [--width N] [--crop L T R B] [--name STEM]

<name> is a scan filename with or without the .jpg (e.g. C085, A2-E-113, V-038).  Output is
written to .novc/scans/ -- gitignored, since a rendering is disposable and can be regenerated
from the scan, but stable across sessions unlike a temp directory.

The scans themselves are a personal archive outside the repo (see WLC_SCANS_DIR).  Filename
conventions differ per book: the Simanim Tiqqun's main body is an identity map from printed
page to C<page:03d>.jpg, while the Koren Classic Tanakh numbers the Torah continuously as
A<n>-<letter>-<page:03d>.jpg and gives its appendix a separate V-<page:03d>.jpg sequence.

This only WRITES the PNG.  To put one in front of the reader, hand over a ``file:///`` link
to it -- absolute path, forward slashes, three slashes after ``file:`` -- and open NOTHING:
no Start-Process, no browser pane, no desktop viewer.  The reader often has the page open
already, so a launched copy is a duplicate window (house rule, 2026-07-28).  To verify the
output yourself, Read the PNG rather than opening it anywhere.

The raw scans are ~5100x7100 and 4-13 MB, too big to open comfortably or to hand to the Read
tool, which is the whole reason this exists.

--crop takes four fractions of the page in 0..1, left top right bottom, applied before the
resize -- so cropping to a quarter of the page and keeping --width the same doubles the
effective resolution.  That is what makes a conjunctive legible: a whole Tiqqun page at 1400px
shows the disjunctive skeleton and the maqafs, but merkha vs. meteg needs the zoom.
Right-hand (accented) column of a SimTiq two-column page is roughly --crop 0.5 0 1 1.

--name sets the output stem, so successive crops of one page do not overwrite each other
(a crop otherwise lands on <name>-crop.png regardless of which region it is).  It names ONE
stem, so it refuses to run with more than one page: every page would land on the same file,
the last one silently winning.

The SCANS/OUT constants here are also ``transcription_editor``'s, which imports them from
here: the two tools read the same archive and write to the same scratch directory.

``render_page`` is the one-page unit behind the subcommand, and is what ``zoom_line`` calls to
render its crops -- a function call, where it once ran this file as a subprocess by path.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from PIL import Image

from mb_cmn import paths

# The scans are a personal archive outside any repo, so this is the one machine-specific path
# here; WLC_SCANS_DIR overrides it, in the style of mb_cmn.paths' sibling-repo overrides.
SCANS = Path(
    os.environ.get("WLC_SCANS_DIR", Path.home() / "OneDrive/Documents/ScansOfBooks")
)
# Renderings are disposable and can be large, so they go to gitignored scratch, not out/.
OUT = paths.scans_dir()


def render_page(
    book: str,
    name: str,
    width: int = 1400,
    crop: tuple[float, float, float, float] | list[float] | None = None,
    stem: str | None = None,
) -> Path:
    """Write one downscaled PNG under OUT and return its path.

    Prints nothing: a caller rendering a page per line (``zoom_line``) would otherwise repeat
    a report line under every zoom, which is exactly what the old subprocess call captured
    stdout to suppress.
    """
    OUT.mkdir(parents=True, exist_ok=True)
    out_stem = name.removesuffix(".jpg")
    src = SCANS / book / f"{out_stem}.jpg"
    img = Image.open(src)
    if crop:
        left, top, right, bottom = crop
        img = img.crop(
            (
                round(left * img.width),
                round(top * img.height),
                round(right * img.width),
                round(bottom * img.height),
            )
        )
        out_stem = f"{out_stem}-crop"
    if stem:
        out_stem = stem
    scale = width / img.width
    small = img.resize((width, round(img.height * scale)), Image.LANCZOS)
    dst = OUT / f"{out_stem}.png"
    small.save(dst)
    return dst


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    # repo_root is unused: OUT is a module constant, because ``transcription_editor`` imports
    # it.  The parameter is here so the entry point wires every subcommand the same way.
    del repo_root
    parser.add_argument("book", help="book directory under the scans archive")
    parser.add_argument(
        "names", nargs="+", help="scan filename(s), with or without the .jpg"
    )
    parser.add_argument(
        "--width", type=int, default=1400, help="output width in pixels"
    )
    parser.add_argument(
        "--crop",
        type=float,
        nargs=4,
        metavar=("L", "T", "R", "B"),
        help="fractions of the page in 0..1, applied before the resize",
    )
    parser.add_argument(
        "--name",
        dest="stem",
        help="output stem, so successive crops of one page do not overwrite each other",
    )


def run(args: argparse.Namespace) -> None:
    if args.stem and len(args.names) > 1:
        raise SystemExit(
            "scan-page: error: --name sets ONE output stem, so with more than one page every"
            " page would be written to the same file, the last one silently winning -- the"
            " very overwrite the flag exists to prevent.  Run once per page."
        )
    for name in args.names:
        dst = render_page(args.book, name, args.width, args.crop, args.stem)
        # Image.open parses the header only, so reading the size back off the file just
        # written costs nothing and keeps render_page's return value a plain path.
        with Image.open(dst) as written:
            size = written.size
        src_name = f"{name.removesuffix('.jpg')}.jpg"
        print(f"{src_name} -> {dst}  ({size[0]}x{size[1]})")
