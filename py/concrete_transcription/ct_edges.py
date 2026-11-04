"""How the trial's shapes' edges compare with the image's: whether the difference
image's red inline means too much ink, as Ben asked on 2026-11-04.

Written for the concrete-transcription trial, 2026-11-04.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py edges
        <work-dir> <draft> [<profile.json>]

The page's difference image is each pixel's e = cov - rho: cov the shapes'
coverage as the clean page draws them, each shape whole, with sharp edges or
blurred by the page's soft edge; rho the image's ink, (V - lum) / (V - K), V and
K the medians of the image's vellum and ink (ct_page.image_tones).  For each
pixel within BAND px of an outline and BORDER px or more from the image's edge:
its signed distance d from the outline of all the shapes together, negative
inside, from the shapes at 3 samples a pixel.  Prints, in bins of d, the mean rho
and the mean cov, sharp and soft; the red (e > 0) and the blue (e < 0) in all;
and the least-squares fit of rho near the edges by the shapes moved out by
delta px, blurred by a Gaussian of sigma px, scaled by a: delta < 0 says the
outlines are too big, sigma above the page's soft edge says their edges are too
sharp.  Writes the profile, for a chart, when asked.
"""

import json
import math

import numpy as np
from PIL import Image

from concrete_transcription import ct_drafts
from concrete_transcription import ct_page
from concrete_transcription import ct_share

S = ct_share.S
BAND = 4.0  # px either side of the outline
BORDER = 6  # px from the image's edge, left out
REACH = 6  # px: the farthest distance measured
BIN = 0.25  # px


def blur(a, sigma):
    """A Gaussian blur of standard deviation sigma px, the edges extended."""
    if sigma <= 0:
        return a.copy()
    r = int(math.ceil(4 * sigma))
    x = np.arange(-r, r + 1, dtype=np.float64)
    k = np.exp(-x * x / (2 * sigma * sigma))
    k /= k.sum()
    p = np.pad(a, ((r, r), (0, 0)), mode="edge")
    v = sum(k[i] * p[i : i + a.shape[0], :] for i in range(2 * r + 1))
    p = np.pad(v, ((0, 0), (r, r)), mode="edge")
    return sum(k[i] * p[:, i : i + a.shape[1]] for i in range(2 * r + 1))


def signed_distance(union, h, w, reach):
    """Each pixel centre's signed distance, in px, from the boundary of a mask at S
    samples a pixel, negative inside: the distance to the nearest sample of the
    other side less half a sample; infinite beyond reach."""
    centre = union[S // 2 :: S, S // 2 :: S][:h, :w]
    best = np.full((h, w), np.inf)
    rr = int(reach * S)
    rows, cols = union.shape
    cy = np.arange(h) * S + S // 2
    cx = np.arange(w) * S + S // 2
    for dy in range(-rr, rr + 1):
        ys = cy + dy
        oky = (ys >= 0) & (ys < rows)
        ysc = np.clip(ys, 0, rows - 1)
        for dx in range(-rr, rr + 1):
            d2 = dy * dy + dx * dx
            if d2 == 0 or d2 > rr * rr:
                continue
            xs = cx + dx
            ok = oky[:, None] & ((xs >= 0) & (xs < cols))[None, :]
            other = (union[np.ix_(ysc, np.clip(xs, 0, cols - 1))] != centre) & ok
            np.minimum(best, np.where(other, float(d2), np.inf), out=best)
    d = (np.sqrt(best) - 0.5) / S
    return np.where(centre, -d, d)


def run(work, draft_name, profile):
    signs, prefix = ct_drafts.draft(draft_name)
    l1 = json.loads((work / "level1.json").read_text(encoding="utf-8"))
    shapes = json.loads((work / f"{prefix}-shapes.json").read_text(encoding="utf-8"))[
        "shapes"
    ]
    w, h = l1["width"], l1["height"]
    union = np.zeros((h * S, w * S), dtype=bool)
    for s in shapes:
        union |= ct_share.shape_mask(s, w, h)
    cov = union.reshape(h, S, w, S).mean(axis=(1, 3))
    tones = ct_page.image_tones(work, l1)
    V, K = tones["vellum_lum"], tones["ink_lum"]
    with Image.open(work / l1["image"]) as im:
        lum = np.asarray(im.convert("L"), dtype=np.float64)
    rho = (V - lum) / (V - K)
    d = signed_distance(union, h, w, REACH)
    yy, xx = np.mgrid[0:h, 0:w]
    inner = (yy >= BORDER) & (yy < h - BORDER) & (xx >= BORDER) & (xx < w - BORDER)
    band = inner & (np.abs(d) <= BAND)
    soft = ct_page.SOFT_EDGE
    print(
        f"V {V}, K {K}; {int(band.sum())} pixels within {BAND} px of an outline;"
        f" the page's soft edge {soft} px"
    )
    covs = {"sharp": cov, "soft": blur(cov, soft)}
    for name, c in covs.items():
        e = np.clip(c - rho, -1, 1)[band]
        print(
            f"{name:5}: red {e[e > 0].sum():8.1f}  blue {-e[e < 0].sum():8.1f}"
            f"  net {e.sum():+8.1f} px of ink"
        )
    # The fit: the shapes moved out by delta, by their signed distance, each pixel's
    # coverage a ramp one pixel wide; blurred by sigma; scaled by a.
    rb = rho[band]
    fits = []
    lifted = []  # the fit with a and an offset b free, b the vellum's own darkness
    for delta in np.arange(-1.5, 1.0001, 0.1):
        base = np.clip(0.5 - (d - delta), 0.0, 1.0)
        for sigma in np.arange(0.0, 3.0001, 0.1):
            c = blur(base, sigma)[band]
            a = float((c * rb).sum() / (c * c).sum())
            fits.append(
                (
                    float(((rb - c) ** 2).sum()),
                    float(((rb - a * c) ** 2).sum()),
                    round(float(delta), 2),
                    round(float(sigma), 2),
                    a,
                )
            )
            (a2, b2), *_ = np.linalg.lstsq(
                np.stack([c, np.ones_like(c)], axis=1), rb, rcond=None
            )
            lifted.append(
                (
                    float(((rb - a2 * c - b2) ** 2).sum()),
                    round(float(delta), 2),
                    round(float(sigma), 2),
                    float(a2),
                    float(b2),
                )
            )
    one = min(fits, key=lambda f: f[0])
    free = min(fits, key=lambda f: f[1])
    at0 = [f for f in fits if f[2] == 0.0 and f[3] == round(soft, 2)][0]
    print(
        f"fit, a = 1: delta {one[2]:+.1f} px, sigma {one[3]:.1f} px; residual {one[0]:.1f}"
        f" (the page's shapes and soft edge: {at0[0]:.1f})"
    )
    print(
        f"fit, a free: delta {free[2]:+.1f} px, sigma {free[3]:.1f} px, a {free[4]:.3f};"
        f" residual {free[1]:.1f}"
    )
    lift = min(lifted)
    print(
        f"fit, a and b free: delta {lift[1]:+.1f} px, sigma {lift[2]:.1f} px,"
        f" a {lift[3]:.3f}, b {lift[4]:+.3f}; residual {lift[0]:.1f}"
    )
    best_sigma_at0 = min((f for f in fits if f[2] == 0.0), key=lambda f: f[0])
    print(
        f"the outlines where they are, a = 1: best sigma {best_sigma_at0[3]:.1f} px,"
        f" residual {best_sigma_at0[0]:.1f}"
    )
    edges = np.arange(-BAND, BAND + 1e-9, BIN)
    fitted = blur(np.clip(0.5 - (d - one[2]), 0.0, 1.0), one[3])
    rows = []
    print(f"{'d':>6} {'n':>6} {'image':>6} {'sharp':>6} {'soft':>6} {'fitted':>6}")
    for lo, hi in zip(edges[:-1], edges[1:]):
        sel = band & (d >= lo) & (d < hi)
        if not sel.any():
            continue
        row = {
            "d": round(float((lo + hi) / 2), 3),
            "n": int(sel.sum()),
            "image": float(rho[sel].mean()),
            "sharp": float(covs["sharp"][sel].mean()),
            "soft": float(covs["soft"][sel].mean()),
            "fitted": float(fitted[sel].mean()),
        }
        rows.append(row)
        print(
            f"{row['d']:6.2f} {row['n']:6d} {row['image']:6.3f} {row['sharp']:6.3f}"
            f" {row['soft']:6.3f} {row['fitted']:6.3f}"
        )
    if profile is not None:
        out = {
            "draft": signs.DRAFT_VERSION,
            "V": V,
            "K": K,
            "soft_edge": soft,
            "fit": {"delta": one[2], "sigma": one[3]},
            "profile": rows,
        }
        with open(profile, "w", encoding="utf-8", newline="\n") as fp:
            json.dump(out, fp, indent=1)
            fp.write("\n")
        print(profile)
