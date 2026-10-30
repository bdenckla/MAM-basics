"""The pen-stroke representation of manuscript crops: make, derive, check and show.

A stroke-SVG beside each crop in doc/pen-stroke-snips/ describes the crop's ink
as filled outlines and as pen strokes, under the profile in
doc/pen-stroke-representation.md.  Its medians, groups, frame and judgments are
authored; this program derives the rest from the crop.  It reads only files in
this repository.

Subcommands:
    init CROP [--set KEY=VALUE ...] [--threshold T]
        Write CROP's stroke-SVG beside it, with the provenance given, the crop's
        Otsu threshold unless one is given, nibs fitted to its ink, and the
        derived level-1 parts.  Refuses to overwrite an existing stroke-SVG.
    nibfit CROP-OR-SVG [--threshold T] [--split PIXELS]
        Print the stiff nib that best fits the ink's width against its direction:
        for a crop, the letters and marks told apart by component size; for a
        stroke-SVG, the ink under each nib's strokes.  Writes nothing.
    derive [SVG ...]
        Recompute the derived parts of the stroke-SVGs given, or of all of them.
    check [SVG ...]
        Report every way the stroke-SVGs depart from the profile and their crops,
        as py/tests/test_pen_stroke_svgs.py does.  Writes nothing.
    render
        Write doc/pen-stroke-snips/overlays.html, the stroke-SVGs over their crops.
"""

import argparse
import sys
from pathlib import Path

from pen_stroke import derive as dv
from pen_stroke import raster
from pen_stroke import render
from pen_stroke import tools


def _run_init(args):
    provenance = {}
    for item in args.set or []:
        key, sep, value = item.partition("=")
        if not sep:
            sys.exit(f"--set takes KEY=VALUE, not {item!r}")
        provenance[key] = value
    out = tools.init_file(args.crop, provenance, threshold=args.threshold)
    print(f"wrote {out.as_posix()}")


def _print_fit(name, fit):
    nib, rms, rows, n = fit
    if nib is None:
        print(f"  {name}: {n} samples, too few directions to fit")
        return
    print(
        f"  {name}: width {nib.width:.2f}, angle {nib.angle:.1f}, edge {nib.edge:.2f};"
        f" misfit {rms:.2f} px over {n} samples"
    )
    for centre, count, med in rows:
        print(
            f"      {centre:5.1f} deg  n={count:4d}  median {med:5.2f}  model {nib.thickness(centre):5.2f}"
        )


def _run_nibfit(args):
    path = Path(args.path)
    if path.name.endswith(tools.SVG_SUFFIX):
        fits = tools.nib_fits_by_strokes(path)
    else:
        lum = raster.load_luminance(path)
        t = args.threshold if args.threshold is not None else raster.otsu_threshold(lum)
        print(f"{path.name}: threshold {t}, split at {args.split} pixels")
        fits = tools.nib_fits(lum, t, args.split)
    for name, fit in fits.items():
        _print_fit(name, fit)


def _run_derive(args):
    for svg in args.svgs or tools.all_svgs():
        changed = tools.derive_file(svg)
        print(f"{'derived' if changed else 'unchanged'} {Path(svg).as_posix()}")


def _run_check(args):
    svgs = args.svgs or tools.all_svgs()
    if not svgs:
        sys.exit("no stroke-SVGs to check")
    bad = 0
    for svg in svgs:
        found = dv.problems(svg)
        print(f"{Path(svg).as_posix()}: {len(found)} problems")
        for line in found:
            print("  " + line)
        bad += bool(found)
    if bad:
        sys.exit(1)


def _run_render(_args):
    out = render.write_overlays(tools.all_svgs())
    print(f"wrote {out.as_posix()}")


def build_parser():
    """Return the argument parser, buildable without running the program."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)
    p = sub.add_parser("init", help="write a crop's stroke-SVG")
    p.add_argument("crop")
    p.add_argument("--set", action="append", metavar="KEY=VALUE")
    p.add_argument("--threshold", type=int)
    p = sub.add_parser("nibfit", help="fit a stiff nib to a crop's ink")
    p.add_argument("path")
    p.add_argument("--threshold", type=int)
    p.add_argument("--split", type=int, default=tools.DEFAULT_SPLIT)
    p = sub.add_parser("derive", help="recompute the stroke-SVGs' derived parts")
    p.add_argument("svgs", nargs="*")
    p = sub.add_parser("check", help="check the stroke-SVGs against their crops")
    p.add_argument("svgs", nargs="*")
    sub.add_parser("render", help="write the overlay page")
    return parser


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = build_parser().parse_args()
    {
        "init": _run_init,
        "nibfit": _run_nibfit,
        "derive": _run_derive,
        "check": _run_check,
        "render": _run_render,
    }[args.subcommand](args)


if __name__ == "__main__":
    main()
