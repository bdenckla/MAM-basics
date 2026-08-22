"""
Visualizations of column-coordinate data for the Aleppo Codex Book of Job.

Generates three images:
  1. col_coord_scatter.png    — scatter plot of column corners
  2. col_angle_fan.png        — polar histogram of skew angles (exaggerated)
  3. col_linespacing_hist.png — histogram of line spacings

Usage:
    python py_ac_loc/plot_col_coords.py
"""

import json
import math

import matplotlib.pyplot as plt
import numpy as np

import ac_paths

COORD_DIR = ac_paths.col_coords_dir()
OUT_DIR = ac_paths.novc_dir()
PERSISTENT_DIR = ac_paths.plot_col_coords_out_dir()

ANGLE_EXAGGERATION = 20
ANGLE_BINS = 5
SPACING_BINS = 10
LINES_PER_COL = 28


def _load_pages():
    pages = sorted(COORD_DIR.glob("*.json"))
    if not pages:
        raise FileNotFoundError("No coordinate files found.")
    return [json.loads(p.read_text(encoding="utf-8")) for p in pages]


def _save(fig, name):
    OUT_DIR.mkdir(exist_ok=True)
    for d in (OUT_DIR, PERSISTENT_DIR):
        path = d / name
        fig.savefig(str(path), dpi=150)
        print(f"Saved to {path}")


def plot_corners(data):
    """Scatter plot of column corners in relative image space."""
    corners = {
        "r": {"col1": [], "col2": []},
        "v": {"col1": [], "col2": []},
    }
    for d in data:
        page_id = d["page"]
        side = "r" if page_id.endswith("r") else "v"
        for col_key in ("col1", "col2"):
            if col_key not in d["columns"]:
                continue
            rel = d["columns"][col_key]["rel"]
            corners[side][col_key].extend(
                [
                    (rel["tl"][0], rel["tl"][1], "TL"),
                    (rel["tr"][0], rel["tr"][1], "TR"),
                    (rel["bl"][0], rel["bl"][1], "BL"),
                    (rel["br"][0], rel["br"][1], "BR"),
                ]
            )

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title("Column Corners in Relative Image Space", fontsize=13)
    ax.set_xlabel("x (relative)")
    ax.set_ylabel("y (relative)")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(1.02, -0.02)  # invert y so top of image is at top
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)

    markers = {"TL": "^", "TR": ">", "BL": "v", "BR": "<"}
    colors = {
        ("r", "col1"): "red",
        ("r", "col2"): "orange",
        ("v", "col1"): "blue",
        ("v", "col2"): "cornflowerblue",
    }

    for side in ("r", "v"):
        side_label = "recto" if side == "r" else "verso"
        for col_key in ("col1", "col2"):
            col_label = "C1" if col_key == "col1" else "C2"
            color = colors[(side, col_key)]
            pts = corners[side][col_key]
            for corner_type in ("TL", "TR", "BL", "BR"):
                subset = [(x, y) for x, y, ct in pts if ct == corner_type]
                if subset:
                    xs = [p[0] for p in subset]
                    ys = [p[1] for p in subset]
                    ax.scatter(
                        xs,
                        ys,
                        c=color,
                        marker=markers[corner_type],
                        s=40,
                        zorder=3,
                        label=f"{side_label} {col_label} {corner_type}",
                    )

    ax.legend(fontsize=7, loc="lower center", ncol=4)
    fig.tight_layout()
    _save(fig, "col_coord_scatter.png")


def plot_angle_fan(data):
    """Polar histogram of column skew angles (derived from quad corners)."""
    angle_groups = {
        ("col1", "top"): [],
        ("col1", "bot"): [],
        ("col2", "top"): [],
        ("col2", "bot"): [],
    }
    for d in data:
        for col_key in ("col1", "col2"):
            if col_key not in d["columns"]:
                continue
            rel = d["columns"][col_key]["rel"]
            # Compute edge angles from corner positions
            top_angle = math.degrees(
                math.atan2(rel["tr"][1] - rel["tl"][1], rel["tr"][0] - rel["tl"][0])
            )
            bot_angle = math.degrees(
                math.atan2(rel["br"][1] - rel["bl"][1], rel["br"][0] - rel["bl"][0])
            )
            angle_groups[(col_key, "top")].append(top_angle)
            angle_groups[(col_key, "bot")].append(bot_angle)

    colors = {
        ("col1", "top"): ("red", "C1 Top"),
        ("col1", "bot"): ("orangered", "C1 Bot"),
        ("col2", "top"): ("blue", "C2 Top"),
        ("col2", "bot"): ("cornflowerblue", "C2 Bot"),
    }

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    ax.set_title(
        f"Column Skew Angles ({ANGLE_EXAGGERATION}× exaggerated)\n"
        f"{ANGLE_BINS} bins, bar length = count",
        fontsize=13,
        pad=20,
    )

    all_angles = [a for angles in angle_groups.values() for a in angles]
    exag_min = min(all_angles) * ANGLE_EXAGGERATION
    exag_max = max(all_angles) * ANGLE_EXAGGERATION
    margin = max((exag_max - exag_min) * 0.1, 1.0)
    bin_edges_deg = np.linspace(exag_min - margin, exag_max + margin, ANGLE_BINS + 1)
    bin_edges_rad = np.radians(bin_edges_deg)
    bin_centers_rad = (bin_edges_rad[:-1] + bin_edges_rad[1:]) / 2

    bar_width = (bin_edges_rad[1] - bin_edges_rad[0]) * 0.22

    keys = list(colors.keys())
    n_groups = len(keys)
    offsets = np.linspace(
        -bar_width * (n_groups - 1) / 2,
        bar_width * (n_groups - 1) / 2,
        n_groups,
    )

    for offset, key in zip(offsets, keys):
        exag_angles = [a * ANGLE_EXAGGERATION for a in angle_groups[key]]
        counts, _ = np.histogram(exag_angles, bins=bin_edges_deg)
        color, label = colors[key]
        ax.bar(
            bin_centers_rad + offset,
            counts,
            width=bar_width,
            bottom=0,
            color=color,
            alpha=0.7,
            label=label,
            zorder=3,
        )

    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)
    ax.set_thetamin(exag_min - margin - 2)
    ax.set_thetamax(exag_max + margin + 2)

    max_count = max(
        max(
            np.histogram(
                [a * ANGLE_EXAGGERATION for a in angle_groups[k]], bins=bin_edges_deg
            )[0]
        )
        for k in keys
    )
    ax.set_ylim(0, max_count + 1)
    ax.set_yticks(range(0, max_count + 2))
    ax.set_rlabel_position((exag_min + exag_max) / 2)

    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.05), fontsize=9)

    fig.text(
        0.02,
        0.02,
        f"actual range: {min(all_angles):.2f}° to {max(all_angles):.2f}°",
        fontsize=9,
        color="gray",
    )
    fig.tight_layout()
    _save(fig, "col_angle_fan.png")


def plot_linespacing(data):
    """Histogram of line spacings (as % of image height)."""
    spacings = []
    for d in data:
        for col_key in ("col1", "col2"):
            if col_key not in d["columns"]:
                continue
            rel = d["columns"][col_key]["rel"]
            # Column height from quad corners
            col_h = (rel["bl"][1] + rel["br"][1]) / 2 - (
                rel["tl"][1] + rel["tr"][1]
            ) / 2
            spacings.append(col_h / LINES_PER_COL * 100)

    lo, hi = min(spacings), max(spacings)
    margin = (hi - lo) * 0.1
    bin_edges = np.linspace(lo - margin, hi + margin, SPACING_BINS + 1)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_title(f"Line Spacing Distribution ({SPACING_BINS} bins)", fontsize=13)

    counts, _, _ = ax.hist(
        spacings,
        bins=bin_edges,
        color="steelblue",
        alpha=0.8,
        edgecolor="white",
    )

    ax.set_xlabel("Line spacing (% of image height)")
    ax.set_ylabel("Count")
    ax.set_yticks(range(0, int(max(counts)) + 2))

    fig.text(
        0.02,
        0.02,
        f"range: {lo:.3f}% to {hi:.3f}%",
        fontsize=9,
        color="gray",
    )
    fig.tight_layout()
    _save(fig, "col_linespacing_hist.png")


def main():
    data = _load_pages()
    plot_corners(data)
    plot_angle_fan(data)
    plot_linespacing(data)


if __name__ == "__main__":
    main()
