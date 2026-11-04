"""Fold the edits that Ben exported from the page into the trial's shapes.

Written for the concrete-transcription trial, 2026-11-03.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py fold
        <work-dir> <edits.json> <out.json>

Reads level1.json and the shapes of the draft that the export names (for draft
1, draft-shapes.json; ct_drafts.py) from <work-dir>, and the page's export;
checks the export against the draft, and each edited shape's path data, as the
page drew it, against ct_geometry's from the same points; prints what each edit
moved, and how the shapes share out the ink before the edits and after; writes
the shapes with the edits to <out.json>, and a close look at the edited shapes
beside it, the same name with .png for .json.
"""

import json
import math
import re

import numpy as np
from PIL import Image, ImageDraw

from pen_stroke import geometry as geo
from concrete_transcription import ct_drafts
from concrete_transcription import ct_geometry as ctg
from concrete_transcription import ct_share

S = ct_share.S
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
COMMAND = re.compile(r"[MLCZ]")


def check_d(shape):
    """The largest difference between the page's path data and ct_geometry's."""
    mine = ctg.shape_d(shape)
    if COMMAND.findall(mine) != COMMAND.findall(shape["d"]):
        raise SystemExit(
            f"{shape['id']}: the page's path commands differ from ct_geometry's"
        )
    a = [float(v) for v in NUMBER.findall(mine)]
    b = [float(v) for v in NUMBER.findall(shape["d"])]
    if len(a) != len(b):
        raise SystemExit(
            f"{shape['id']}: the page's path has {len(b)} numbers, ct_geometry's {len(a)}"
        )
    return max(abs(x - y) for x, y in zip(a, b))


def describe_outline(old, new):
    if len(old["contours"]) != len(new["contours"]):
        print(f"  contours {len(old['contours'])} -> {len(new['contours'])}")
        return
    for k, (co, cn) in enumerate(zip(old["contours"], new["contours"])):
        if len(co) != len(cn):
            print(f"  contour {k}: {len(co)} points -> {len(cn)}")
            continue
        for i, (p, q) in enumerate(zip(co, cn)):
            moved = math.hypot(q[0] - p[0], q[1] - p[1])
            if moved > 0.005 or p[2] != q[2]:
                corner = "" if p[2] == q[2] else f", corner {p[2]} -> {q[2]}"
                print(
                    f"  contour {k} point {i}: ({p[0]}, {p[1]}) -> ({q[0]}, {q[1]}),"
                    f" moved {moved:.2f} px{corner}"
                )


def describe_stroke(old, new):
    for i, (p, q) in enumerate(zip(old["centerline"], new["centerline"])):
        print(
            f"  centerline point {i}: ({p[0]}, {p[1]}) -> ({q[0]}, {q[1]}),"
            f" moved {math.hypot(q[0] - p[0], q[1] - p[1]):.2f} px"
        )
    if len(old["centerline"]) != len(new["centerline"]):
        print(
            f"  centerline {len(old['centerline'])} points -> {len(new['centerline'])}"
        )
    print(
        f"  width {old['width']} -> {new['width']}; caps {old['caps']} -> {new['caps']}"
    )


def fold(draft, edits):
    by_id = {s["id"]: s for s in draft}
    for s in edits["changed"]:
        if s["id"] not in by_id:
            raise SystemExit(f"a changed shape {s['id']} that the draft lacks")
        if s["type"] != by_id[s["id"]]["type"]:
            raise SystemExit(f"{s['id']}: the edit changes the shape's type")
    for s in edits["added"]:
        if s["id"] in by_id:
            raise SystemExit(f"an added shape {s['id']} that the draft has")
    for sid in edits["deleted"]:
        if sid not in by_id:
            raise SystemExit(f"a deleted shape {sid} that the draft lacks")
    changed = {s["id"]: s for s in edits["changed"]}
    out = [changed.get(s["id"], s) for s in draft if s["id"] not in edits["deleted"]]
    return out + list(edits["added"])


def run(work, edits_path, out_path):
    l1 = json.loads((work / "level1.json").read_text(encoding="utf-8"))
    edits = json.loads(edits_path.read_text(encoding="utf-8"))
    signs, prefix = ct_drafts.draft_of_version(edits["draft"])
    draft = json.loads((work / f"{prefix}-shapes.json").read_text(encoding="utf-8"))
    w, h = l1["width"], l1["height"]
    if edits["image"] != f"{l1['image']}, {w} x {h}":
        raise SystemExit(f"the edits are of {edits['image']!r}")
    by_id = {s["id"]: s for s in draft["shapes"]}
    for s in edits["changed"] + edits["added"]:
        print(
            f"{s['id']}: the page's path data and ct_geometry's differ by at most"
            f" {check_d(s):.4f} px"
        )
    for s in edits["changed"]:
        print(f"{s['id']} ({s['short']}) edited:")
        if s["type"] == "outline":
            describe_outline(by_id[s["id"]], s)
        else:
            describe_stroke(by_id[s["id"]], s)
        if s["note"]:
            print("  note:", s["note"])
    if edits["note"]:
        print("general note:", edits["note"])
    folded = fold(draft["shapes"], edits)
    ink = ct_share.ink_mask(l1, signs)
    before = {s["id"]: ct_share.shape_mask(s, w, h) for s in draft["shapes"]}
    after = {s["id"]: ct_share.shape_mask(s, w, h) for s in folded}
    out_b, _cb, _nb = ct_share.share_out(ink, before)
    out_a, count, near_any = ct_share.share_out(ink, after)
    ct_share.print_share("the draft", out_b)
    ct_share.print_share("with the edits", out_a)
    for sid in ("rg10", "rg15"):
        own = (ink & after[sid]).sum() / (S * S)
        print(f"  {sid}: {round(own, 1)} px of ink inside it")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fp:
        json.dump(
            {
                "width": w,
                "height": h,
                "draft": edits["draft"],
                "edits": edits_path.name,
                "shapes": folded,
            },
            fp,
            ensure_ascii=False,
            indent=1,
        )
        fp.write("\n")
    _look(
        work,
        l1,
        draft["shapes"],
        folded,
        ink,
        count,
        near_any,
        out_path.with_suffix(".png"),
        [s["id"] for s in edits["changed"]],
    )


def _bbox(shapes, ids, margin, w, h):
    xs, ys = [], []
    for s in shapes:
        if s["id"] in ids:
            for poly in geo.flatten(geo.parse_path(ct_share.shape_d(s))):
                xs += [x for x, _y in poly]
                ys += [y for _x, y in poly]
    return (
        max(0, int(min(xs)) - margin),
        max(0, int(min(ys)) - margin),
        min(w, int(max(xs)) + margin + 1),
        min(h, int(max(ys)) + margin + 1),
    )


def _look(work, l1, draft, folded, ink, count, near_any, png, changed_ids):
    """For Claude: the edited shapes over the image, the draft's in grey."""
    scale = 4
    w, h = l1["width"], l1["height"]
    x0, y0, x1, y1 = _bbox(folded, set(changed_ids) | {"rg15"}, 12, w, h)
    with Image.open(work / l1["image"]) as im:
        base = im.convert("RGB").crop((x0, y0, x1, y1))
    base = base.resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.Resampling.BICUBIC)
    over = np.zeros((h * S, w * S, 4), dtype=np.uint8)
    over[ink & ~near_any] = (255, 0, 0, 230)
    over[ink & (count >= 2)] = (255, 0, 255, 120)
    over_im = Image.fromarray(over, "RGBA").crop((x0 * S, y0 * S, x1 * S, y1 * S))
    over_im = over_im.resize(base.size, Image.Resampling.NEAREST)
    pic = Image.alpha_composite(base.convert("RGBA"), over_im)
    draw = ImageDraw.Draw(pic)

    def outline(shape, colour, width):
        for poly in geo.flatten(geo.parse_path(ct_share.shape_d(shape))):
            pts = [((x - x0) * scale, (y - y0) * scale) for x, y in poly]
            draw.line(pts + [pts[0]], fill=colour, width=width)

    by_id = {s["id"]: s for s in draft}
    for sid in changed_ids:
        outline(by_id[sid], (150, 150, 150, 255), 1)
    for s in folded:
        if s["id"] in changed_ids or s["id"] == "rg15":
            colour = (0, 160, 0, 255) if s["type"] == "stroke" else (0, 90, 255, 255)
            outline(s, colour, 2)
    pic.convert("RGB").save(png)
    print(png, f"crop x {x0}..{x1}, y {y0}..{y1}, scale {scale}")
