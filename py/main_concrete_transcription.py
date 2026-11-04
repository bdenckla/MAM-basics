"""The concrete transcription trial: one manuscript image's ink drafted as shapes,
and the pages that show them.

The trial is item 12 of doc/PLAN-ink-regions.md, of the image of UXLC change
2023.03.25-112.  Its record, its one image and Ben's edits of draft 1 are in
doc/concrete-transcription-2026-11-03/, whose README.md gives the order in which
these subcommands rebuild the trial.  Every subcommand but fetch reads only that
directory, other files of this repository and the paths it is given, and writes
only into the work directory or the paths it is given; the work directory and the
pages are not tracked, but the production images are, in that directory's
production/.

Subcommands:
    fetch
        Usage: fetch URL OUT-DIR OUT-NAME
        Download URL, which must be on tanach.us, politely and obeying
        robots.txt, into OUT-DIR, which must not exist yet, with the fetch's
        record beside it.  A download: run it only with Ben's word.
    level1
        Usage: level1 IMAGE WORK-DIR
        Level 1 of the image, by the tracked py/pen_stroke code: its
        threshold, its fills and its residual pieces, written into WORK-DIR.
    draft
        Usage: draft WORK-DIR [DRAFT]
        A draft's regions, by a seeded watershed on the image's luminance.
        DRAFT is 1, 2 or 3, and 1 by default.
    shapes
        Usage: shapes WORK-DIR [DRAFT]
        A draft's shapes: an outline for each region, and the stray stroke.
    fold
        Usage: fold WORK-DIR EDITS OUT
        Fold the edits exported from a draft's editing page into its shapes,
        and report what each edit moved.
    page
        Usage: page WORK-DIR OUT [DRAFT]
        Write a draft's editing page, the development page.
    preview
        Usage: preview WORK-DIR OUT DRAFT
        Write a draft's production preview: one image, whose views a click
        cycles.
    production
        Usage: production WORK-DIR OUT-DIR DRAFT
        Write a draft's production images into OUT-DIR: the preview's views
        of the transcription, with the stray stroke and without it, each an
        SVG file the image's size.
    edges
        Usage: edges WORK-DIR DRAFT [PROFILE]
        Compare the edges of a draft's shapes with the image's, and write
        the profile across them to PROFILE when it is given.
    edges-chart
        Usage: edges-chart PROFILE CHART
        Chart that profile, as a PNG.
    area
        Usage: area WORK-DIR PREFIX [REACH]
        Each draft region's area at the level-1 threshold against its ink.
    measure
        Usage: measure WORK-DIR X0 X1 Y0 Y1 [PREFIX] [--samples]
        A text map of the draft regions' owners in a box of the image.
    look
        Usage: look IMAGE OUT SCALE [X0 Y0 X1 Y1]
        An enlarged copy of an image, or of a box of it, for viewing.
    look2
        Usage: look2 IMAGE OUT SCALE X0 Y0 X1 Y1 [GRID]
        A contrast-stretched, gridded enlargement of a box of an image.
    look3
        Usage: look3 WORK-DIR BEFORE AFTER OUT SCALE X0 Y0 X1 Y1 [ID ...]
               [--draft DRAFT]
        Two sets of shapes over a close-up of the image.
"""

import argparse
import sys
from pathlib import Path

from concrete_transcription import ct_area
from concrete_transcription import ct_draft
from concrete_transcription import ct_edges
from concrete_transcription import ct_edges_chart
from concrete_transcription import ct_fetch
from concrete_transcription import ct_fold
from concrete_transcription import ct_level1
from concrete_transcription import ct_look
from concrete_transcription import ct_look2
from concrete_transcription import ct_look3
from concrete_transcription import ct_measure
from concrete_transcription import ct_page
from concrete_transcription import ct_preview
from concrete_transcription import ct_shapes


def _run_fetch(args):
    ct_fetch.run(args.url, args.out_dir, args.out_name)


def _run_level1(args):
    ct_level1.run(args.image, args.work)


def _run_draft(args):
    ct_draft.run(args.work, args.draft)


def _run_shapes(args):
    ct_shapes.run(args.work, args.draft)


def _run_fold(args):
    ct_fold.run(args.work, args.edits, args.out)


def _run_page(args):
    ct_page.run(args.work, args.out, args.draft)


def _run_preview(args):
    ct_preview.run(args.work, args.out, args.draft)


def _run_production(args):
    ct_preview.production(args.work, args.out_dir, args.draft)


def _run_edges(args):
    ct_edges.run(args.work, args.draft, args.profile)


def _run_edges_chart(args):
    ct_edges_chart.run(args.profile, args.chart)


def _run_area(args):
    ct_area.run(args.work, args.prefix, args.reach)


def _run_measure(args):
    ct_measure.run(args.work, args.box, args.prefix, args.samples)


def _run_look(args):
    if len(args.box) not in (0, 4):
        sys.exit("look takes a box of four numbers, X0 Y0 X1 Y1, or none")
    ct_look.run(args.image, args.out, args.scale, args.box)


def _run_look2(args):
    ct_look2.run(args.image, args.out, args.scale, args.box, args.grid)


def _run_look3(args):
    ct_look3.run(
        args.work,
        args.before,
        args.after,
        args.out,
        args.scale,
        args.box,
        args.ids,
        args.draft,
    )


def build_parser():
    """Return the argument parser, buildable without running the program."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)
    p = sub.add_parser("fetch", help="download one file from tanach.us")
    p.add_argument("url")
    p.add_argument("out_dir", type=Path)
    p.add_argument("out_name")
    p = sub.add_parser("level1", help="level 1 of the image")
    p.add_argument("image", type=Path)
    p.add_argument("work", type=Path)
    p = sub.add_parser("draft", help="a draft's regions")
    p.add_argument("work", type=Path)
    p.add_argument("draft", nargs="?", default="1")
    p = sub.add_parser("shapes", help="a draft's shapes")
    p.add_argument("work", type=Path)
    p.add_argument("draft", nargs="?", default="1")
    p = sub.add_parser("fold", help="fold exported edits into their draft")
    p.add_argument("work", type=Path)
    p.add_argument("edits", type=Path)
    p.add_argument("out", type=Path)
    p = sub.add_parser("page", help="write a draft's editing page")
    p.add_argument("work", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("draft", nargs="?", default="1")
    p = sub.add_parser("preview", help="write a draft's production preview")
    p.add_argument("work", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("draft")
    p = sub.add_parser("production", help="write a draft's production images")
    p.add_argument("work", type=Path)
    p.add_argument("out_dir", type=Path)
    p.add_argument("draft")
    p = sub.add_parser("edges", help="compare the shapes' edges with the image's")
    p.add_argument("work", type=Path)
    p.add_argument("draft")
    p.add_argument("profile", nargs="?")
    p = sub.add_parser("edges-chart", help="chart the profile across the edges")
    p.add_argument("profile")
    p.add_argument("chart")
    p = sub.add_parser("area", help="each region's area against its ink")
    p.add_argument("work", type=Path)
    p.add_argument("prefix")
    p.add_argument("reach", nargs="?", type=int, default=ct_area.REACH)
    p = sub.add_parser("measure", help="a text map of a box's owners")
    p.add_argument("work", type=Path)
    p.add_argument("box", nargs=4, type=int, metavar=("X0", "X1", "Y0", "Y1"))
    p.add_argument("prefix", nargs="?", default="draft")
    p.add_argument("--samples", action="store_true")
    p = sub.add_parser("look", help="an enlarged copy of an image")
    p.add_argument("image")
    p.add_argument("out")
    p.add_argument("scale", type=int)
    p.add_argument("box", nargs="*", type=int, metavar="X0 Y0 X1 Y1")
    p = sub.add_parser("look2", help="a gridded enlargement of part of an image")
    p.add_argument("image")
    p.add_argument("out")
    p.add_argument("scale", type=int)
    p.add_argument("box", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    p.add_argument("grid", nargs="?", type=int, default=10)
    p = sub.add_parser("look3", help="two sets of shapes over a close-up")
    p.add_argument("work", type=Path)
    p.add_argument("before")
    p.add_argument("after")
    p.add_argument("out", type=Path)
    p.add_argument("scale", type=int)
    p.add_argument("box", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    p.add_argument("ids", nargs="*", metavar="ID")
    p.add_argument("--draft")
    return parser


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = build_parser().parse_args()
    {
        "fetch": _run_fetch,
        "level1": _run_level1,
        "draft": _run_draft,
        "shapes": _run_shapes,
        "fold": _run_fold,
        "page": _run_page,
        "preview": _run_preview,
        "production": _run_production,
        "edges": _run_edges,
        "edges-chart": _run_edges_chart,
        "area": _run_area,
        "measure": _run_measure,
        "look": _run_look,
        "look2": _run_look2,
        "look3": _run_look3,
    }[args.subcommand](args)


if __name__ == "__main__":
    main()
