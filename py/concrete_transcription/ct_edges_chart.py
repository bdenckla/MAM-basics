"""A chart of ct_edges.py's profile: the image's ink and the transcription's,
averaged over every edge, against the distance from the outline.

Written for the concrete-transcription trial, 2026-11-04.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py edges-chart
        <profile.json> <chart.png>
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

SURFACE, INK, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#898781", "#e1e0d9", "#c3c2b7"
SECONDARY = "#52514e"
# Categorical slots 1 to 3 of the dataviz skill's palette, in order.
SERIES = [
    ("image", "the image", "#2a78d6"),
    ("soft", "the transcription, the page's soft edge", "#eb6834"),
    ("fitted", "the transcription, an edge softened to fit the image", "#1baf7a"),
]


def run(profile, chart):
    prof = json.loads(Path(profile).read_text(encoding="utf-8"))
    rows = prof["profile"]
    d = [r["d"] for r in rows]
    fig, ax = plt.subplots(figsize=(9.6, 5.6), dpi=100)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.axvline(0, color=SECONDARY, linewidth=1, linestyle=(0, (4, 3)))
    ax.axhline(0.5, color=MUTED, linewidth=0.8, linestyle=(0, (2, 3)))
    ax.text(0.08, 1.02, "the outline", color=SECONDARY, fontsize=10, va="bottom")
    ax.text(
        -3.92, 0.515, "half-way from vellum to ink", color=MUTED, fontsize=9, ha="left"
    )
    for key, label, colour in SERIES:
        ys = [r[key] for r in rows]
        ax.plot(
            d,
            ys,
            color=colour,
            linewidth=2.2 if key == "image" else 2,
            solid_capstyle="round",
        )
    # Direct labels, in text ink beside a swatch of each line's colour.
    for (key, label, colour), (x, y) in zip(
        SERIES, [(0.45, 0.95), (0.45, 0.89), (0.45, 0.83)]
    ):
        ax.plot([x, x + 0.3], [y, y], color=colour, linewidth=2.4)
        ax.text(x + 0.4, y, label, color=INK, fontsize=10, va="center")
    ax.annotate(
        "inside the outline, the page is darker\nthan the image: the red inline",
        xy=(-0.9, 0.71),
        xytext=(-2.7, 0.36),
        color=INK,
        fontsize=10,
        va="center",
        arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 0.8},
    )
    ax.annotate(
        "outside it, the page is lighter than\nthe image: the blue fringe",
        xy=(1.3, 0.22),
        xytext=(1.3, 0.6),
        color=INK,
        fontsize=10,
        va="center",
        arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 0.8},
    )
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 1.08)
    ax.set_xlabel(
        "distance from the outline, in the image's pixels (inside to the left)",
        color=SECONDARY,
        fontsize=10,
    )
    ax.set_ylabel("darkness (0 vellum, 1 ink)", color=SECONDARY, fontsize=10)
    ax.set_title(
        "Across the outlines, averaged over every edge of draft 3",
        color=INK,
        fontsize=12,
        loc="left",
    )
    fig.tight_layout()
    fig.savefig(chart, facecolor=SURFACE)
    print(chart)
