"""The work behind py/main_pen_stroke.py's subcommands."""

from pathlib import Path

import numpy as np

from pen_stroke import derive as dv
from pen_stroke import geometry as geo
from pen_stroke import level5
from pen_stroke import nib as nibmod
from pen_stroke import raster
from pen_stroke import stroke_svg as ssvg

SNIPS_DIR = Path("doc") / "pen-stroke-snips"
SVG_SUFFIX = ".strokes.svg"

DEFAULT_SPECK_SIZE = 8
DEFAULT_HALO_BAND = 24
# Ink components of at least this many pixels are taken for letters, and the
# rest for marks, when a crop's nibs are fitted before any stroke is traced.
DEFAULT_SPLIT = 300


def svg_path_for(png):
    png = Path(png)
    return png.with_name(png.name[: -len(png.suffix)] + SVG_SUFFIX)


def all_svgs(directory=SNIPS_DIR):
    return sorted(Path(directory).glob("*" + SVG_SUFFIX))


def split_by_component(ink, split):
    """Masks of the ink in components of at least ``split`` pixels, and of the rest."""
    big = np.zeros_like(ink)
    for comp in raster.components(ink, 8):
        if comp.sum() >= split:
            big |= comp
    return big, ink & ~big


def nib_fits(lum, threshold, split):
    """Fits for the letters, the marks and all the ink, each (nib, rms, bins, n)."""
    ink = lum < threshold
    big, small = split_by_component(ink, split)
    out = {}
    for name, sel in (("letters", big), ("marks", small), ("all", None)):
        samples = nibmod.width_samples(lum, ink, select=sel)
        nib, rms, rows = nibmod.fit(samples)
        out[name] = (nib, rms, rows, len(samples))
    return out


def samples_by_strokes(svg_path, cls):
    """Width samples of the ink under one nib's strokes, grown by two pixels."""
    sf = ssvg.read(svg_path)
    lum = raster.load_luminance(dv.crop_path(svg_path, sf))
    ink = lum < sf.threshold
    h, w = ink.shape
    polys = []
    for st in sf.strokes:
        if st.nib == cls:
            polys.extend(dv.sweep_polys(sf, st))
    sel = raster.dilate8(raster.dilate8(geo.rasterize(polys, w, h, "nonzero")))
    return nibmod.width_samples(lum, ink, select=sel)


def nib_fits_by_strokes(svg_path):
    """Fits for the ink under the letters' strokes and under the marks' strokes."""
    out = {}
    for cls in (level5.LETTERS, level5.MARKS):
        samples = samples_by_strokes(svg_path, cls)
        nib, rms, rows = nibmod.fit(samples)
        out[cls] = (nib, rms, rows, len(samples))
    return out


def pooled_fit(svg_paths, cls):
    """One fit for one nib's strokes in all the stroke-SVGs together."""
    samples = []
    for p in svg_paths:
        samples.extend(samples_by_strokes(p, cls))
    nib, rms, rows = nibmod.fit(samples)
    return nib, rms, rows, len(samples)


def init_file(
    png,
    provenance,
    threshold=None,
    speck_size=DEFAULT_SPECK_SIZE,
    halo_band=DEFAULT_HALO_BAND,
    split=DEFAULT_SPLIT,
):
    """A new stroke-SVG beside the crop: provenance, parameters, fitted nibs,
    and the derived level-1 parts; no strokes yet."""
    png = Path(png)
    out_path = svg_path_for(png)
    if out_path.exists():
        raise FileExistsError(f"{out_path} exists; derive it instead")
    lum = raster.load_luminance(png)
    if threshold is None:
        threshold = raster.otsu_threshold(lum)
    fits = nib_fits(lum, threshold, split)
    nibs = {}
    for cls in (level5.LETTERS, level5.MARKS):
        nib = fits[cls][0]
        if nib is None:
            raise ValueError(f"too few {cls} samples to fit a nib")
        nibs[cls] = nibmod.Nib(
            round(nib.width, 2), round(nib.angle, 1), round(nib.edge, 2)
        )
    h, w = lum.shape
    sf = ssvg.StrokeFile(
        width=w,
        height=h,
        image=png.name,
        provenance=provenance,
        threshold=threshold,
        speck_size=speck_size,
        halo_band=halo_band,
        nibs=nibs,
    )
    sf = dv.derive(sf, lum)
    ssvg.write(sf, out_path)
    return out_path


def derive_file(svg_path):
    """Recompute the stroke-SVG's derived parts in place.  True if it changed."""
    sf = ssvg.read(svg_path)
    lum = raster.load_luminance(dv.crop_path(svg_path, sf))
    text = ssvg.dumps(dv.derive(sf, lum))
    old = Path(svg_path).read_text(encoding="utf-8")
    if text == old:
        return False
    with open(svg_path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(text)
    return True
