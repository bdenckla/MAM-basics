"""The pen-stroke and ink-region representations of manuscript crops: make,
derive, check and show.

A stroke-SVG beside each crop in doc/pen-stroke-snips/ describes the crop's ink
as filled outlines and as pen strokes, under the profile in
doc/pen-stroke-representation.md.  Its strokes' medians, their widths or the
crop's nib that sweeps them, its groups, frame and judgments are authored; this
program derives the rest from the crop.  The stroke-SVGs are a frozen record
since 2026-11-01.  A region-SVG beside each crop describes its ink as regions,
under the profile in doc/ink-region-representation.md: its seeds, cuts, strips
of supplied vellum, overlaps' outlines, supplied ink, groups and judgments are
authored, and this program derives the rest from the crop.  Under profile 3, a
region-SVG's glyphs, from the library of glyphs doc/pen-stroke-snips/glyphs.svg,
are fitted to its ink by regions-fit, and its regions derived from them.
It reads only files in this repository, and the page image that regions-fit is
given.

Subcommands:
    init
        Usage: init CROP [--set KEY=VALUE ...] [--threshold T]
        Write CROP's stroke-SVG beside it, with the provenance given, the crop's
        Otsu threshold unless one is given, and the derived level-1 parts.
        Refuses to overwrite an existing stroke-SVG.
    nibfit
        Usage: nibfit CROP-OR-SVG [--threshold T] [--split PIXELS]
        Print the stiff nib that best fits the ink's width against its direction,
        a statistic of the ink: for a crop, the letters and marks told apart by
        component size; for a stroke-SVG, the ink under each pass's strokes.
        Writes nothing.
    derive
        Usage: derive [SVG ...]
        Recompute the derived parts of the stroke-SVGs given, or of all of them.
    check
        Usage: check [SVG ...]
        Report every way the stroke-SVGs depart from the profile and their crops,
        as py/tests/test_pen_stroke_svgs.py does.  Writes nothing.
    render
        Write doc/pen-stroke-snips/overlays.html, the stroke-SVGs over their crops.
    regions-derive
        Usage: regions-derive [SVG ...] [--copy-taamey-d]
        Recompute the library's glyphs of the scribe's, then the derived parts of
        the region-SVGs given, or of all of them, and report what their authored
        parts leave unsettled.  --copy-taamey-d copies Taamey D's glyphs into the
        library afresh from Taamey-D/font-m-TaD/Taamey_D.ttf.  A profile-3
        region-SVG whose glyphs' outlines would change is left as it is.
    regions-check
        Usage: regions-check [SVG ...]
        Report every way the library and the region-SVGs depart from the profile
        and their crops, as py/tests/test_ink_region_svgs.py does, and list,
        without failing, each profile-3 region-SVG's unexplained ink.  Writes
        nothing; never reads Taamey D's font.
    regions-render
        Write doc/pen-stroke-snips/regions.html, the region-SVGs' ink in layers.
    regions-fit
        Usage: regions-fit SVG --page-image PATH
        Fit the library's glyphs to the region-SVG's ink, write its glyphs and
        their parameters, move it to profile 3, and derive it.  PATH is the page
        image the crop was cut from, which the root's data-source-sha256 names.
        Takes minutes.
"""

import argparse
import sys
import time
from pathlib import Path

from pen_stroke import derive as dv
from pen_stroke import glyph_library
from pen_stroke import raster
from pen_stroke import region_derive
from pen_stroke import region_render
from pen_stroke import region_svg
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


def _run_regions_derive(args):
    library = glyph_library.library_path(tools.SNIPS_DIR)
    if library.exists():
        font = glyph_library.TAAMEY_D_FONT if args.copy_taamey_d else None
        changed, found = region_derive.library_derive_file(library, font)
        print(f"{'derived' if changed else 'unchanged'} {library.as_posix()}")
        for line in found:
            print("  " + line)
    elif args.copy_taamey_d:
        lib = glyph_library.copy_taamey_d(
            glyph_library.Library(), glyph_library.TAAMEY_D_FONT
        )
        glyph_library.write(lib, library)
        print(f"wrote {library.as_posix()}")
    for svg in args.svgs or region_svg.all_svgs(tools.SNIPS_DIR):
        changed, found = region_derive.derive_file(svg)
        print(f"{'derived' if changed else 'unchanged'} {Path(svg).as_posix()}")
        for line in found:
            print("  " + line)


def _run_regions_check(args):
    svgs = args.svgs or region_svg.all_svgs(tools.SNIPS_DIR)
    if not svgs:
        sys.exit("no region-SVGs to check")
    bad = 0
    library = glyph_library.library_path(tools.SNIPS_DIR)
    if library.exists():
        found = region_derive.library_problems(library)
        print(f"{library.as_posix()}: {len(found)} problems")
        for line in found:
            print("  " + line)
        bad += bool(found)
    for svg in svgs:
        found, notes = region_derive.check(svg)
        print(f"{Path(svg).as_posix()}: {len(found)} problems")
        for line in found:
            print("  " + line)
        for line in notes:
            print("  note: " + line)
        bad += bool(found)
    if bad:
        sys.exit(1)


def _run_regions_render(_args):
    out = region_render.write_page(region_svg.all_svgs(tools.SNIPS_DIR))
    print(f"wrote {out.as_posix()}")


def _run_regions_fit(args):
    start = time.perf_counter()
    found, notes = region_derive.fit_file(
        args.svg, args.page_image, lambda line: print(line, flush=True)
    )
    minutes = (time.perf_counter() - start) / 60
    print(f"fitted {Path(args.svg).as_posix()} in {minutes:.1f} minutes")
    for line in found:
        print("  " + line)
    for line in notes:
        print("  note: " + line)


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
    p = sub.add_parser(
        "regions-derive", help="recompute the region-SVGs' derived parts"
    )
    p.add_argument("svgs", nargs="*")
    p.add_argument("--copy-taamey-d", action="store_true")
    p = sub.add_parser(
        "regions-check", help="check the region-SVGs against their crops"
    )
    p.add_argument("svgs", nargs="*")
    sub.add_parser("regions-render", help="write the region page")
    p = sub.add_parser("regions-fit", help="fit glyphs to a region-SVG's ink")
    p.add_argument("svg")
    p.add_argument("--page-image", required=True)
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
        "regions-derive": _run_regions_derive,
        "regions-check": _run_regions_check,
        "regions-render": _run_regions_render,
        "regions-fit": _run_regions_fit,
    }[args.subcommand](args)


if __name__ == "__main__":
    main()
