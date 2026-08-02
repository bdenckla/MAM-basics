"""Build a per-line transcription editor for a page of a book scan.

Usage:
    .venv/Scripts/python.exe py/main_edition_transcription.py editor <book-dir> <name> \
        [--crop L T R B] [--width N] [--name STEM] [--debug]

Writes .novc/scans/<stem>-editor.html: the page image with a text field that sits directly
under whichever line is being transcribed, on top of the image.  The field follows the
current line down the page, so the eye never leaves the line it is reading -- the ergonomic
problem with transcribing a whole page in one go.  It covers the NEXT line while it is open,
which costs nothing, since that line is not the one being read.  --debug additionally writes
<stem>-lines.png with the detected line bands drawn on the page, to check the segmentation
before typing into it.

Line finding is a horizontal projection profile, not OCR: the fraction of each pixel row that
is ink, smoothed; rows above a threshold are text and the troughs between them are the gaps.
Nothing here reads a letter or an accent -- it only finds where the lines are.  Binarizing and
then resizing the column to one pixel wide with a BOX filter gives that per-row ink fraction
directly, which is why this needs no numpy.

The projection is taken over the CROPPED region, so crop to a single text column first: a
two-column page profiled whole has no clean troughs, since the columns' lines do not align.

--crop's LEFT and RIGHT bound the text column, as before.  Its TOP and BOTTOM name the LINES
TO TRANSCRIBE, not the region to run band detection over.  When they crop into the page (are
not the full 0..1 height), detection runs over a region grown about a line past them each way,
and only bands whose centre falls within the requested range get a field to type into; the
neighbours are rendered too, dimmed as context, since a Hebrew line's own above-marks are what
tell it apart from the line above's below-marks.  So the crop is set to just the wanted lines,
and the old "reach the middle of the neighbouring line" dead zone -- a bound between the two
good placements that clipped a line or let ``_absorb_slivers`` swallow a sliver of the next --
is unreachable, because the region detected over is no longer the reader's to choose.  See
issue wlc-utils#71.

THAT SPLIT IS ALSO AN EXPORT-FORMAT CHANGE, and the two shapes are distinguished by presence
alone: ``render.crop`` used to mean the region rendered and now means the lines requested,
with ``render.detect_crop`` -- written only when the crop grew -- holding the region.  Every
transcription committed before wlc-utils#71 is of the older shape and was deliberately left alone --
today that is ALL of them, so the first export with a ``detect_crop`` will be the first reader
of one, and there will be no re-vendoring to flush the old shape out.  ``rendered_region`` is the
one place that rule is written down as code; read an export through it rather than reaching
for ``render["crop"]``, which answers the old question for old exports and the new one for new.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

# The scans archive and the .novc/scans scratch directory are ``scan_page``'s constants,
# imported rather than repeated: the two tools read the same archive and write beside each
# other, and the last two copies of this block had already begun as verbatim twins.  The
# editor and its rendering are disposable -- rebuilt from the scan whenever the crop changes
# -- which is why scratch is the right home; what is meant to be KEPT is the JSON the Save
# button exports, committed beside the transcription it records.
from accgram.scan_page import OUT, SCANS

# A row is text when its ink rises this far from the page's own baseline toward a full line's
# density.  Relative, not absolute, because a crop that clips the page's vertical border rule
# carries a constant ink offset in EVERY row, gaps included, which no fixed floor separates.
# Kept small because a closing line of two or three words covers very little of the column
# and anything scaled to a full line's density silently loses it.
INK_CUTOFF = 0.08
INK_LEVEL = 128  # gray below this is ink
SMOOTH_RADIUS = 3  # rows; blurs out the gap between a letter body and its accents
MIN_LINE_FRACTION = (
    0.25  # of median band height -- below this a band is speck, not a line
)
MIN_GAP_FRACTION = (
    0.35  # of median band height -- shorter gaps are within-line, so merge
)
MAX_LINE_UNITS = (
    1.6  # a band taller than this many single lines is holding more than one
)
# Below this fraction of a single line, a band is a fragment or a decorative rule, not a line.
# Safe at half a line because a SHORT line is short horizontally, not vertically: it still
# stands a full line tall, so this cannot swallow one.
SLIVER_FRACTION = 0.5
# A hung closing line (see _recover_trailing_line) carries far less ink than a full line, being
# horizontally short, but far more than a speck.  Below this fraction of a full line's ink, a
# tail run is a smudge, not a word.
TRAIL_INK_FRACTION = 0.03
# How far past the requested lines to grow the detection region, in line pitches each way (see
# the module docstring and issue wlc-utils#71).  One whole pitch puts each neighbour fully in view, so it
# detects as a complete band whose centre lies clearly outside the requested range -- context,
# not a line to type into -- while the requested boundary line sits fully interior and so is
# never clipped nor sliver-absorbed.
DETECT_MARGIN_PITCHES = 1.0
# The grow when a single requested line offers no pitch to measure: a fraction of page height
# safely over one line on every edition transcribed so far.
DETECT_MARGIN_FALLBACK = 0.04


def crop_and_resize(
    src_img: Image.Image, crop: list[float] | None, width: int
) -> tuple[Image.Image, int, float]:
    """Crop by fractions ``[L, T, R, B]`` (or not at all) and resize to ``width`` px wide.

    Returns ``(img, origin, scale)``: ``origin`` is the source-pixel row of the crop's top and
    ``scale`` converts a rendered-image row back to source pixels (``source = origin + row *
    scale``), so a band found in the rendering can be reported against the original scan too.
    """
    sw, sh = src_img.width, src_img.height
    if crop:
        left, top, right, bottom = crop
        img = src_img.crop(
            (round(left * sw), round(top * sh), round(right * sw), round(bottom * sh))
        )
        origin = round(top * sh)
    else:
        img, origin = src_img, 0
    cropped_h = img.height
    img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    return img, origin, cropped_h / img.height


def rendered_region(render: dict) -> list[float] | None:
    """The page region an export's PNG and line coordinates actually cover, or ``None`` if whole.

    READ AN EXPORT'S REGION THROUGH THIS, never off ``render["crop"]``, which does not mean the
    same thing in every export.  Issue wlc-utils#71 gave ``crop`` the narrower job of naming the LINES
    REQUESTED and put the region grown around them in ``detect_crop``, written only when the
    grow happened.  A pre-wlc-utils#71 export has no ``detect_crop`` and its ``crop`` IS the region
    rendered, so the fallback here is not a default standing in for a missing value -- it is the
    older format's own answer, which is why the two formats need no version field to tell apart.

    Left and right never differed between the two, so a caller wanting only the column bounds
    (``zoom_line``) is unaffected either way; it is the vertical pair that moved.
    """
    return render.get("detect_crop") or render["crop"]


def median_pitch(bands: list[tuple[int, int]]) -> int | None:
    """Median top-to-top spacing of consecutive bands, or ``None`` with fewer than two.

    Printed lines are evenly spaced, so this is a stable estimate of one line even when a tight
    crop has clipped a boundary band -- exactly the case the detection grow then fixes -- since
    the median rides over one or two bad bands.
    """
    if len(bands) < 2:
        return None
    tops = [top for top, _ in bands]
    gaps = sorted(b - a for a, b in zip(tops, tops[1:]))
    return gaps[len(gaps) // 2]


def detect_margin(
    probe_bands: list[tuple[int, int]], probe_scale: float, source_height: int
) -> float:
    """Source-height fraction to grow the requested crop by, from a probe over those lines alone.

    One line's pitch where the probe found two lines or more; a single line's own height where it
    found just one (enough that the line is never at an edge, though its neighbours stay out of
    view); a fixed fraction of the page where it found none.  ``probe_scale`` converts the probe's
    rendered pixels back to source pixels, so the grow is expressed against the original scan.
    """
    pitch = median_pitch(probe_bands)
    if pitch is None and probe_bands:  # a single requested line: use its own height
        pitch = probe_bands[0][1] - probe_bands[0][0]
    if pitch is None:
        return DETECT_MARGIN_FALLBACK
    return DETECT_MARGIN_PITCHES * pitch * probe_scale / source_height


def row_profile(img: Image.Image) -> list[float]:
    """Fraction of each pixel row that is ink, 0.0 to 1.0.

    Binarize first, then average: averaging raw gray instead would weight a row by how dark
    it is rather than how much of it is covered, and short lines vanish.
    """
    ink = img.convert("L").point(lambda v: 255 if v < INK_LEVEL else 0)
    column = ink.resize((1, img.height), Image.BOX)
    return [v / 255 for v in column.getdata()]


def smooth(values: list[float], radius: int) -> list[float]:
    out = []
    for i in range(len(values)):
        lo, hi = max(0, i - radius), min(len(values), i + radius + 1)
        out.append(sum(values[lo:hi]) / (hi - lo))
    return out


def _ink_cutoff(profile: list[float]) -> float:
    """The per-row ink fraction at which a row counts as text.

    Relative to the page's own baseline (a 5th-percentile gap row, border rule included) and a
    busy row (90th percentile, a full line), so a crop that clips the vertical border rule -- a
    constant ink offset in every row, gaps included -- does not move it.
    """
    ordered = sorted(profile)
    baseline = ordered[
        int(0.05 * (len(ordered) - 1))
    ]  # a gap row, border rule included
    busy = ordered[int(0.90 * (len(ordered) - 1))]  # a full line of text
    return baseline + INK_CUTOFF * (busy - baseline)


def find_bands(profile: list[float]) -> list[tuple[int, int]]:
    """Contiguous row ranges that hold text, as (top, bottom) pairs."""
    cutoff = _ink_cutoff(profile)

    bands, start = [], None
    for i, value in enumerate(profile):
        if value >= cutoff and start is None:
            start = i
        elif value < cutoff and start is not None:
            bands.append((start, i))
            start = None
    if start is not None:
        bands.append((start, len(profile)))
    if not bands:
        return []

    # Two clean-ups, in this order: close the gaps inside a line first (a row of accents can
    # sit clear of its letters), then drop what is still too short to be a line.
    heights = sorted(b - a for a, b in bands)
    median = heights[len(heights) // 2]
    merged = [list(bands[0])]
    for top, bottom in bands[1:]:
        if top - merged[-1][1] < MIN_GAP_FRACTION * median:
            merged[-1][1] = bottom
        else:
            merged.append([top, bottom])
    heights = sorted(b - a for a, b in merged)
    median = heights[len(heights) // 2]
    kept = [(a, b) for a, b in merged if (b - a) >= MIN_LINE_FRACTION * median]
    return _recover_trailing_line(_split_tall(kept, profile), profile)


def _split_tall(
    bands: list[tuple[int, int]], profile: list[float]
) -> list[tuple[int, int]]:
    """Cut apart bands too tall to be one printed line.

    The cutoff that is low enough to catch a two-word closing line is also low enough to stop
    separating neighbours whose gap is partly filled by accents above and below, so some bands
    arrive holding two or three lines.  Rather than trade one failure against the other by
    tuning, use the regularity of printed text: take the single-line height from the shorter
    quartile of bands (a short line is narrow, not shallow, so it still measures one line
    tall), then repeatedly cut any over-tall band at its emptiest interior row.
    """
    if not bands:
        return bands
    heights = sorted(b - a for a, b in bands)
    unit = heights[max(0, len(heights) // 4)]
    out, todo = [], list(bands)
    while todo:
        top, bottom = todo.pop()
        if bottom - top <= MAX_LINE_UNITS * unit:
            out.append((top, bottom))
            continue
        # Search only the middle, so the cut lands in a gap rather than shaving off an edge.
        margin = max(1, round(0.3 * unit))
        lo, hi = top + margin, bottom - margin
        if hi <= lo:
            out.append((top, bottom))
            continue
        cut = min(range(lo, hi), key=lambda i: profile[i])
        todo.extend([(top, cut), (cut, bottom)])
    return _absorb_slivers(sorted(out), unit)


def _absorb_slivers(bands: list[tuple[int, int]], unit: int) -> list[tuple[int, int]]:
    """Fold anything too short to be a line into the neighbour it sits closest to.

    Splitting can shave a fragment off a band's edge, and the page's decorative rules survive
    as slivers of their own.  Absorb rather than discard: a dropped band is a line with no
    field to type into, which is a silent hole in the transcription, while an absorbed one
    only makes a neighbouring band slightly tall.
    """
    if not bands:
        return bands
    out = [list(bands[0])]
    for top, bottom in bands[1:]:
        if (bottom - top) < SLIVER_FRACTION * unit:
            out[-1][1] = bottom  # nearest neighbour above; gaps here are sub-pixel
        elif (out[-1][1] - out[-1][0]) < SLIVER_FRACTION * unit:
            out[-1][1] = bottom
        else:
            out.append([top, bottom])
    return [(a, b) for a, b in out]


def _recover_trailing_line(
    bands: list[tuple[int, int]], profile: list[float]
) -> list[tuple[int, int]]:
    """Append a genuine trailing short line that the min-height filter discarded.

    Koren routinely hangs a Decalogue's closing word on a line of its own.  Such a word is short
    HORIZONTALLY, so even its densest rows clear the ink cutoff only faintly, and the sub-cutoff
    gaps between its letters' cores break it into fragments each below MIN_LINE_FRACTION of a
    line -- fragments too far apart to merge -- so find_bands drops the whole word as speckle.
    But it is a real printed line with no field to type into: a silent hole in the transcription.

    Recover it, but only from the region BELOW the last kept band, so this is purely additive at
    the tail and can never renumber a line already found.  Bracket the tail's ink and append it
    as a final band only when it is line-like on the three counts that separate a hung word from
    the two false positives the min-height filter exists to suppress, plus a clipped neighbour:

    * tall enough -- at least half a line -- so a thin decorative rule (which survives find_bands
      as a sliver of its own) is not taken for a line;
    * inky enough -- a word-like fraction of a full line's ink -- so a speck or a faint smudge is
      not, even one that happens to span half a line;
    * clear of the crop's bottom edge, so a real next line the crop clipped to a stub at the very
      bottom is not recovered as though it were a whole line.  Declining is ALL this gate does:
      ``crop_warnings`` sees only kept bands, so a stub the min-height filter dropped never
      reaches its band list and the smallest stubs stay silent -- the gate keeps this function
      from compounding that, it does not hand the stub off to anyone.
    """
    if not bands:
        return bands
    height = len(profile)
    heights = sorted(b - a for a, b in bands)
    unit = heights[
        max(0, len(heights) // 4)
    ]  # a single line: short lines are narrow, not shallow
    line_ink = sorted(sum(profile[a:b]) for a, b in bands)[len(bands) // 2]

    cutoff = _ink_cutoff(profile)
    inked = [i for i in range(bands[-1][1], height) if profile[i] >= cutoff]
    if not inked:  # blank bottom margin: the ordinary, correct case
        return bands
    top, bottom = inked[0], inked[-1] + 1
    if bottom - top < SLIVER_FRACTION * unit:  # a thin rule or sliver, not a line
        return bands
    if sum(profile[top:bottom]) < TRAIL_INK_FRACTION * line_ink:  # a speck, not a word
        return bands
    if (
        height - bottom < MIN_LINE_FRACTION * unit
    ):  # jammed on the crop edge: maybe clipped
        return bands
    return bands + [(top, bottom)]


def crop_warnings(bands: list[tuple[int, int]], height: int) -> list[tuple[str, str]]:
    """Complaints about where the vertical crop was placed, as ``(level, message)``.

    Both failures below are SILENT otherwise: the debug overlay draws a plausible band either
    way, so a clipped line and a merged one look like an ordinary line in the picture.

    A Hebrew crop should reach the MIDDLE of the neighbouring printed line, not stop tight at
    the transcribed text -- Hebrew stacks marks above AND below the letters, and a half-line's
    own above-marks are what let them be told apart from the last full line's below-marks.
    That leaves two ways to get the vertical bound wrong, and they pull in opposite directions:

    * Too tight, and the outermost line is clipped.  Koren p. 281's first crop cut the bottom
      four source pixels off line 17, taking part of the under-letter marks with it -- and
      tipexa, merkha and munax all sit under the letter.
    * Not tight enough to clear the next line, but not far enough to include it either.  A
      clipped sliver is shorter than SLIVER_FRACTION of a line, so ``_absorb_slivers`` folds
      it into the last real band, which is right for a fragment shaved off by a split and
      wrong for a genuine neighbour cut by the crop.  On that same page, bottoms of 0.610 and
      0.614 gave the last band a height of 208 and 232 px against a true 127.

    So: clear the next line entirely, or take half of it, and never a sliver.

    LEVELS, and why they differ.  A merged band is unambiguously wrong, so it warns.  A band
    touching the crop edge is NOT: on a correct crop the outermost band IS the half-line of
    context the rule asks for, and it necessarily touches the edge.  Nothing in the geometry
    separates that from a transcribed line cut short -- both are simply short -- so it is a
    note that states both readings rather than a warning that would fire on every correct crop
    and teach the reader to ignore it.
    """
    if not bands:
        return []
    out: list[tuple[str, str]] = []
    heights = sorted(b - a for a, b in bands)
    median = heights[len(heights) // 2]
    for i, (top, bottom) in enumerate(bands, start=1):
        if bottom - top > MAX_LINE_UNITS * median:
            out.append(
                (
                    "WARNING",
                    f"band {i} is {bottom - top}px against a median of {median}px -- it has"
                    " probably absorbed a clipped sliver of a neighbouring line."
                    "  Clear that line or take half of it; a sliver is the one bad choice",
                )
            )
    edges = [
        (name, i)
        for name, i, touching in (
            ("first", 1, bands[0][0] <= 0),
            ("last", len(bands), bands[-1][1] >= height),
        )
        if touching
    ]
    for name, i in edges:
        out.append(
            (
                "note",
                f"the {name} band (band {i}) touches the crop edge: intended if it is the"
                " half-line of context, clipped if it is a line you mean to transcribe",
            )
        )
    return out


def source_fingerprint(src: Path) -> dict:
    """Identify the exact scan file a transcription was read from.

    The scans are not in the repo, so a committed transcription otherwise names a page with
    no way to tell whether the file behind that name is still the same one.  The digest makes
    that checkable.
    """
    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    with Image.open(src) as img:
        size = list(img.size)
    return {"file": src.name, "book": src.parent.name, "sha256": digest, "size": size}


def band_context(
    bands: list[tuple[int, int]],
    crop: list[float],
    origin: int,
    scale: float,
    source_height: int,
) -> list[bool]:
    """Which detected bands are context: centred outside the requested vertical range.

    ``crop`` is the requested ``[L, T, R, B]``; ``origin`` and ``scale`` place a rendered-image
    row in source pixels (see ``crop_and_resize``).  A band whose centre lands outside ``[T, B]``
    in source pixels is a neighbour the detection grow pulled in, not a line to transcribe.  The
    centre, not an edge, so a boundary line that detects a little tall or short still counts as
    requested and its neighbour, sitting a whole pitch away, still counts as context.
    """
    lo, hi = crop[1] * source_height, crop[3] * source_height
    return [
        not (lo <= origin + (top + bottom) / 2 * scale <= hi) for top, bottom in bands
    ]


def band_rows(
    bands: list[tuple[int, int]],
    context: list[bool],
    height: int,
    origin: int,
    scale: float,
) -> tuple[list[dict], list[dict]]:
    """Split detected bands into transcribable rows and context rows.

    Positions are percentages of image height, so any display width works.  A transcribable band
    also carries its pixels twice: ``px`` in the rendered PNG, and ``px_source`` in the original
    scan.  The rendered PNG is disposable -- regenerate at another --width and its coordinates
    mean something different -- so an audit trail that cited only those would decay; ``px_source``
    stays valid for as long as the scan does, which is what the sha256 pins.

    A context band -- a neighbour pulled into view only so its marks help place the boundary
    line's, never typed -- carries just enough to draw its dimmed strip.  Line numbers count the
    transcribable bands alone, 1..k, so what is typed matches what was asked for.
    """

    def coords(top: int, bottom: int) -> dict:
        return {
            "top": 100.0 * top / height,
            "height": 100.0 * (bottom - top) / height,
            "px": [top, bottom],
            "px_source": [round(origin + top * scale), round(origin + bottom * scale)],
        }

    rows, context_rows, n = [], [], 0
    for (top, bottom), is_context in zip(bands, context):
        if is_context:
            context_rows.append(coords(top, bottom))
        else:
            n += 1
            rows.append({"n": n, **coords(top, bottom)})
    return rows, context_rows


def build_html(
    stem: str, image_name: str, rows: list[dict], context_rows: list[dict], meta: dict
) -> str:
    return (
        _HTML.replace("__STEM__", stem)
        .replace("__IMAGE__", image_name)
        .replace("__ROWS__", json.dumps(rows))
        .replace("__CONTEXT__", json.dumps(context_rows))
        .replace("__META__", json.dumps(meta))
    )


_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__STEM__ - line transcription</title>
<style>
  body { margin: 0; font: 14px/1.4 system-ui, sans-serif; background: #1b1b1b; color: #eee; }
  header { padding: 10px 16px; background: #222; position: sticky; top: 0; z-index: 20;
           display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
  button { font: inherit; padding: 5px 12px; border-radius: 5px; border: 1px solid #555;
           background: #333; color: #eee; cursor: pointer; }
  button:hover { background: #444; }
  #status { color: #9a9; }
  #hint { color: #777; font-size: 13px; }
  #wrap { padding: 16px; }
  /* max-width so the page always fits its viewport.  The rendering is wider than a narrow
     window -- 1200px by default -- and without this the document overflows horizontally,
     which reads as the page being split rather than merely scrolled.  Scaling it down costs
     nothing: every line coordinate below is a PERCENTAGE of the container, so the hit targets
     and entry fields follow the image to whatever width it lands at. */
  #sheet { position: relative; display: inline-block; max-width: 100%; }
  #sheet img { display: block; width: 100%; }

  /* One click target per printed line, lying over the image. */
  .hit { position: absolute; left: 0; width: 100%; cursor: text; }
  .hit.on { background: rgba(110, 200, 255, 0.18);
            box-shadow: inset 0 0 0 1px rgba(110, 200, 255, 0.7); }
  /* A line already typed keeps a marker, since its text is hidden once focus moves on. */
  .hit.done { border-left: 6px solid rgba(80, 200, 110, 0.85); }

  /* A context band: a neighbouring line rendered only so its marks help place the boundary
     line's, never transcribed.  Dimmed and inert -- pointer-events none, so a click falls
     through to nothing -- so it reads as off-limits and has no field of its own. */
  .ctx { position: absolute; left: 0; width: 100%; pointer-events: none;
         background: rgba(10, 10, 10, 0.4);
         border-top: 1px dashed rgba(200, 200, 200, 0.35);
         border-bottom: 1px dashed rgba(200, 200, 200, 0.35); }
  .ctx span { position: absolute; right: 6px; top: 2px; font: 11px system-ui, sans-serif;
              color: #bbb; background: rgba(0, 0, 0, 0.55); padding: 1px 6px;
              border-radius: 3px; }

  /* The entry field sits UNDER its line rather than in a side gutter: a gutter is a
     horizontal eye-jump on every single line, which is the thing this is meant to avoid.
     Only the active one is shown, so the line it covers is never a line being read. */
  .entry { position: absolute; left: 0; width: 100%; display: none; z-index: 10;
           align-items: center; gap: 8px; }
  .entry.on { display: flex; }
  .entry .num { flex: 0 0 auto; font: 15px ui-monospace, Consolas, monospace; color: #9cf;
                background: #0b1a22; padding: 4px 8px; border-radius: 4px 0 0 4px;
                border: 1px solid #6cf; border-right: none; }
  /* RTL to match the page: the first token lands under the line's first word, at the right,
     and the caret travels leftward with the reading. */
  .entry input { flex: 1 1 auto; font: 26px/1.25 ui-monospace, Consolas, monospace;
                 background: #0b1a22; color: #eaf6ff; border: 1px solid #6cf;
                 border-radius: 0 4px 4px 0; padding: 4px 10px; text-align: right; }
  .entry input:focus { outline: none; box-shadow: 0 0 0 2px rgba(110, 200, 255, 0.35); }

  #out { width: 100%; height: 160px; font: 13px ui-monospace, Consolas, monospace;
         background: #111; color: #ddd; border: 1px solid #444; }
  #outwrap { padding: 0 16px 24px; }
</style>
</head>
<body>
<header>
  <strong>__STEM__</strong>
  <button id="copy">Copy transcription</button>
  <button id="save">Save JSON</button>
  <button id="clear">Clear</button>
  <span id="status"></span>
  <span id="hint">click a line to start &middot; Enter = next &middot; Shift+Enter = previous
    &middot; Esc = close</span>
</header>
<div id="wrap"><div id="sheet"><img src="__IMAGE__" alt=""></div></div>
<div id="outwrap"><textarea id="out" readonly
  placeholder="Copy transcription puts the text here"></textarea></div>
<script>
const ROWS = __ROWS__;
const CONTEXT = __CONTEXT__;
const META = __META__;
const KEY = "linetx:__STEM__";
const sheet = document.getElementById("sheet");
const saved = JSON.parse(localStorage.getItem(KEY) || "{}");
const hits = [], entries = [], inputs = [];

// Typical distance from one line's top to the next, as a percentage of image height.  Printed
// lines are evenly spaced, so the median is a good estimate of where a line's successor starts
// -- which is what the LAST line needs, having no successor to measure.  Median rather than
// mean because a band that merged two printed lines, or one holding a heading, would drag a
// mean upward; there is at least one such band on a typical page.
//
// With exactly ONE transcribable row there is no spacing to measure at all, and a PITCH of 0
// would drop the entry field ON the very line being transcribed -- the failure the placement
// comment below exists to avoid, met every time on the single-line crop ``detect_margin``
// explicitly supports.  Estimate a pitch from the lone row's own height instead: half a line
// of clearance past its bottom keeps its descenders and below-marks visible, the same reason
// the band's own bottom was rejected as a placement.
const PITCHES = ROWS.slice(1).map((r, i) => r.top - ROWS[i].top).sort((a, b) => a - b);
const PITCH = PITCHES.length ? PITCHES[Math.floor(PITCHES.length / 2)]
            : ROWS.length ? 1.5 * ROWS[0].height : 0;

ROWS.forEach((r, idx) => {
  const hit = document.createElement("div");
  hit.className = "hit";
  hit.style.top = r.top + "%";
  hit.style.height = r.height + "%";
  hit.addEventListener("mousedown", e => { e.preventDefault(); focusLine(idx); });
  sheet.appendChild(hit);
  hits.push(hit);

  const entry = document.createElement("div");
  entry.className = "entry";
  // Always below the line, the last one included.  Sit at the NEXT line's top, so the field
  // covers the next line -- never the one being read -- and the whole inter-line gap below
  // the current line stays visible, descenders and lower accents included.
  //
  // The last line has no next band, so estimate one at the median pitch.  Two earlier tries
  // were worse: putting the field above the last line (to avoid the page's bottom edge)
  // covered the very line being read, and putting it at the band's own bottom clipped that
  // line's descenders.  The bottom edge is not a real constraint anyway -- the page's own
  // bottom margin leaves room under the last band.
  const next = ROWS[idx + 1];
  entry.style.top = (next ? next.top : r.top + PITCH) + "%";
  const num = document.createElement("span");
  num.className = "num";
  num.textContent = r.n;
  const input = document.createElement("input");
  input.type = "text";
  input.dir = "rtl";
  input.spellcheck = false;
  input.autocapitalize = "off";
  input.value = saved[r.n] || "";
  input.addEventListener("input", save);
  input.addEventListener("keydown", e => {
    if (e.key === "Escape") { input.blur(); close(); return; }
    if (e.key !== "Enter") return;
    e.preventDefault();
    focusLine(idx + (e.shiftKey ? -1 : 1));
  });
  entry.append(num, input);
  sheet.appendChild(entry);
  entries.push(entry);
  inputs.push(input);
});

// Dim each context band and label it, so the reader sees why the image runs past the lines to
// transcribe: the neighbours give the boundary lines their above/below-mark context.  Inert.
CONTEXT.forEach(c => {
  const ctx = document.createElement("div");
  ctx.className = "ctx";
  ctx.style.top = c.top + "%";
  ctx.style.height = c.height + "%";
  const tag = document.createElement("span");
  tag.textContent = "context";
  ctx.appendChild(tag);
  sheet.appendChild(ctx);
});

function close() {
  hits.forEach(h => h.classList.remove("on"));
  entries.forEach(e => e.classList.remove("on"));
}

function focusLine(idx) {
  if (idx < 0 || idx >= ROWS.length) return;
  close();
  hits[idx].classList.add("on");
  entries[idx].classList.add("on");
  const input = inputs[idx];
  input.focus();
  input.setSelectionRange(input.value.length, input.value.length);
  hits[idx].scrollIntoView({ block: "center", behavior: "smooth" });
  save();
}

function save() {
  const data = {};
  inputs.forEach((inp, i) => {
    const text = inp.value.trim();
    if (text) data[ROWS[i].n] = text;
    hits[i].classList.toggle("done", !!text);
  });
  localStorage.setItem(KEY, JSON.stringify(data));
  document.getElementById("status").textContent =
    Object.keys(data).length + " of " + ROWS.length + " lines - saved";
}

document.getElementById("copy").addEventListener("click", () => {
  // One printed line per output line: keeps the transcription checkable against the page.
  const text = inputs.map(i => i.value.trim()).filter(Boolean).join("\\n");
  const out = document.getElementById("out");
  out.value = text;
  navigator.clipboard.writeText(text).then(
    () => document.getElementById("status").textContent = "copied to clipboard",
    () => { out.select(); document.getElementById("status").textContent = "select and copy"; }
  );
});

document.getElementById("save").addEventListener("click", () => {
  // The audit trail: what was typed, on which line, at which coordinates of which scan.
  // Only lines with text are written -- a blank field means not yet transcribed, which is
  // not the same claim as a line that carries no accent.
  const record = {
    stem: META.stem,
    source: META.source,
    render: META.render,
    transcribed_utc: new Date().toISOString(),
    line_count: ROWS.length,
    lines: ROWS.map((r, i) => ({
             n: r.n, px: r.px, px_source: r.px_source, text: inputs[i].value.trim()
           })).filter(l => l.text)
  };
  const blob = new Blob([JSON.stringify(record, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = META.stem + "-transcription.json";
  a.click();
  URL.revokeObjectURL(a.href);
  document.getElementById("status").textContent =
    "saved " + a.download + " to your downloads";
});

document.getElementById("clear").addEventListener("click", () => {
  if (!confirm("Clear all typed lines?")) return;
  localStorage.removeItem(KEY);
  inputs.forEach(i => { i.value = ""; });
  close();
  save();
});

save();
</script>
</body>
</html>
"""


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    # repo_root is unused: OUT and SCANS are ``scan_page``'s module constants, imported above.
    # The parameter is here so the entry point wires every subcommand the same way.
    del repo_root
    parser.add_argument("book", help="book directory under the scans archive")
    parser.add_argument("name", help="scan filename, with or without the .jpg")
    parser.add_argument(
        "--width", type=int, default=1200, help="rendered image width in pixels"
    )
    parser.add_argument(
        "--crop",
        type=float,
        nargs=4,
        metavar=("L", "T", "R", "B"),
        help="fractions of the page in 0..1; L and R bound the text column, T and B name"
        " the lines to transcribe (see the module docstring)",
    )
    parser.add_argument(
        "--name",
        dest="stem",
        help="output stem, defaulting to the scan filename's own",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="also write <stem>-lines.png with the detected line bands drawn on the page",
    )


def run(args: argparse.Namespace) -> None:
    debug, width, crop = args.debug, args.width, args.crop

    stem = args.stem if args.stem else args.name.removesuffix(".jpg")
    src = SCANS / args.book / f"{args.name.removesuffix('.jpg')}.jpg"
    src_img = Image.open(src)
    source_height = src_img.height
    # A crop that reaches INTO the page vertically (not the full 0..1 height) names the lines to
    # transcribe; detection then runs over a grown region so those lines never sit at an edge.  A
    # horizontal-only crop -- the two-column case -- leaves detection over the whole height as
    # before, there being no vertical dead zone to avoid.
    crops_vertically = bool(crop) and (crop[1] > 1e-4 or crop[3] < 1 - 1e-4)

    detect_crop = None
    if crops_vertically:
        # Pass 1, over the requested lines alone, only to size the grow.  The median pitch holds
        # even if this tight crop clipped a boundary band -- the very failure the grow removes --
        # so a bad requested crop does not spoil the estimate.
        probe, _, probe_scale = crop_and_resize(src_img, crop, width)
        probe_bands = find_bands(smooth(row_profile(probe), SMOOTH_RADIUS))
        margin = detect_margin(probe_bands, probe_scale, source_height)
        left, top, right, bottom = crop
        detect_crop = [left, max(0.0, top - margin), right, min(1.0, bottom + margin)]

    img, origin, scale = crop_and_resize(src_img, detect_crop or crop, width)
    bands = find_bands(smooth(row_profile(img), SMOOTH_RADIUS))

    # With no vertical crop every band is a line to transcribe; otherwise the grow pulled in
    # neighbours that must be told apart by where their centres fall.
    context = (
        band_context(bands, crop, origin, scale, source_height)
        if crops_vertically
        else [False] * len(bands)
    )
    rows, context_rows = band_rows(bands, context, img.height, origin, scale)

    OUT.mkdir(parents=True, exist_ok=True)
    image_name = f"{stem}.png"
    img.save(OUT / image_name)

    # Enough to redo the exact rendering the line coordinates refer to.  ``crop`` names the lines
    # requested; ``detect_crop``, present only when the crop grew, is the region detection and
    # the PNG actually cover.  Its absence marks a pre-wlc-utils#71 export, whose ``crop`` instead means
    # "the region rendered".
    # ``rendered_region`` below is the reading half of this rule; keep the two together.
    render = {"crop": crop, "width": width, "size": [img.width, img.height]}
    if detect_crop is not None:
        render["detect_crop"] = detect_crop
    meta = {"stem": stem, "source": source_fingerprint(src), "render": render}

    if debug:
        marked = img.convert("RGB")
        draw = ImageDraw.Draw(marked, "RGBA")
        for r in context_rows:  # gray and unnumbered: not a line to type into
            top, bottom = r["px"]
            draw.rectangle([0, top, marked.width - 1, bottom], fill=(150, 150, 150, 40))
            draw.line([0, top, marked.width, top], fill=(140, 140, 140), width=1)
            draw.line([0, bottom, marked.width, bottom], fill=(140, 140, 140), width=1)
            draw.text((6, top + 2), "ctx", fill=(120, 120, 120))
        for r in rows:  # the transcribable lines, numbered as the editor numbers them
            top, bottom = r["px"]
            draw.rectangle([0, top, marked.width - 1, bottom], fill=(255, 40, 40, 40))
            draw.line([0, top, marked.width, top], fill=(255, 0, 0), width=2)
            draw.line([0, bottom, marked.width, bottom], fill=(0, 120, 255), width=2)
            draw.text((6, top + 2), str(r["n"]), fill=(200, 0, 0))
        marked.save(OUT / f"{stem}-lines.png")
        print(f"debug overlay -> {OUT / f'{stem}-lines.png'}")

    html = OUT / f"{stem}-editor.html"
    html.write_text(
        build_html(stem, image_name, rows, context_rows, meta), encoding="utf-8"
    )
    if context_rows:
        print(
            f"{src.name}: {len(rows)} lines to transcribe, {len(context_rows)} context"
        )
    else:
        print(f"{src.name}: {len(rows)} lines detected")
    heights = [r["px"][1] - r["px"][0] for r in rows]
    if heights:
        print(
            f"  line height min/median/max: {min(heights)}/"
            f"{sorted(heights)[len(heights) // 2]}/{max(heights)} px"
        )
    for level, message in crop_warnings([tuple(r["px"]) for r in rows], img.height):
        print(f"  {level}: {message}")
    print(f"editor -> {html}")
