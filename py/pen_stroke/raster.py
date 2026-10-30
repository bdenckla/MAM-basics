"""A crop's pixels: luminance, the ink threshold, and connected components."""

import numpy as np
from PIL import Image

# The only channel the profile knows: Pillow's ITU-R 601-2 luma, as convert("L") gives it.
CHANNEL = "luminance"


def load_luminance(png_path):
    """The crop's luminance, 0 (black) to 255 (white), as a uint8 array."""
    with Image.open(png_path) as im:
        if im.mode != "RGB":
            raise ValueError(f"{png_path}: expected an RGB crop, not {im.mode}")
        return np.asarray(im.convert("L"))


def otsu_threshold(lum):
    """Otsu's threshold t on luminance; ink is then lum < t."""
    hist = np.bincount(lum.ravel(), minlength=256).astype(np.float64)
    p = hist / hist.sum()
    omega = np.cumsum(p)
    mu = np.cumsum(p * np.arange(256))
    with np.errstate(divide="ignore", invalid="ignore"):
        between = (mu[-1] * omega - mu) ** 2 / (omega * (1 - omega))
    between[~np.isfinite(between)] = 0
    return int(np.argmax(between)) + 1


_N4 = ((-1, 0), (1, 0), (0, -1), (0, 1))
_N8 = _N4 + ((-1, -1), (-1, 1), (1, -1), (1, 1))


def components(mask, connectivity):
    """The mask's connected components, each a boolean mask, in raster order of
    their first pixel."""
    nbrs = {4: _N4, 8: _N8}[connectivity]
    h, w = mask.shape
    label = np.zeros((h, w), dtype=np.int32)
    out = []
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys.tolist(), xs.tolist()):
        if label[y0, x0]:
            continue
        n = len(out) + 1
        label[y0, x0] = n
        stack = [(y0, x0)]
        while stack:
            y, x = stack.pop()
            for dy, dx in nbrs:
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not label[yy, xx]:
                    label[yy, xx] = n
                    stack.append((yy, xx))
        out.append(label == n)
    return out


def dilate8(mask):
    """The mask grown by one pixel in all eight directions."""
    h, w = mask.shape
    p = np.zeros((h + 2, w + 2), dtype=bool)
    p[1:-1, 1:-1] = mask
    out = np.zeros_like(mask)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            out |= p[1 + dy : 1 + dy + h, 1 + dx : 1 + dx + w]
    return out
