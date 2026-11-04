"""The trial's draft shapes: an outline for each draft region, and the stroke.

Written for the concrete-transcription trial, 2026-11-03.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py shapes
        <work-dir> [<draft>]

Reads level1.json and draft-regions.json; writes draft-shapes.json, the shapes
that the page lets Ben edit, and draft-shapes.png, the shapes over the image;
prints how the shapes share out the ink.  For draft 2, draft2-regions.json and
so on (ct_drafts.py).  Each outline's control points are the joints of the
region's traced outline, a joint where the tracer cut a corner being a corner,
except within the draft's SMOOTH boxes.  A regions file's "rest", the stray
stroke's ink that the stroke does not cover, becomes an outline in the stroke's
group.
"""

import json

import numpy as np
from PIL import Image, ImageDraw

from pen_stroke import geometry as geo
from pen_stroke import region_derive as rd
from concrete_transcription import ct_drafts
from concrete_transcription import ct_geometry as ctg
from concrete_transcription import ct_share

S = rd.SAMPLES


def control_points(d):
    """Each closed subpath of traced path data as control points (x, y, corner)."""
    contours = []
    for start, segs, closed in geo.parse_path(d):
        if not closed:
            raise ValueError("a traced outline is closed")
        pts = [[start[0], start[1], 0]]
        pos = start
        k = 0
        while k < len(segs):
            seg = segs[k]
            if seg[0] == "C":
                # The curve's middle too, so that the Catmull-Rom curve through the
                # points keeps close to the tracer's.
                mid = _bezier_point(pos, seg[1], seg[2], seg[3], 0.5)
                pts.append([mid[0], mid[1], 0])
                pts.append([seg[3][0], seg[3][1], 0])
                pos = seg[3]
                k += 1
                continue
            # The tracer writes a corner as two straight segments: to the corner,
            # then on to the middle of the next edge.
            if k + 1 >= len(segs) or segs[k + 1][0] != "L":
                raise ValueError("a straight segment that is not half of a corner")
            pts.append([seg[1][0], seg[1][1], 1])
            pts.append([segs[k + 1][1][0], segs[k + 1][1][1], 0])
            pos = segs[k + 1][1]
            k += 2
        if pts[-1][:2] == pts[0][:2]:
            pts[0][2] = pts[-1][2]
            pts.pop()
        contours.append([[round(x, 2), round(y, 2), c] for x, y, c in pts])
    return contours


SIMPLIFY_TOLERANCE = 0.4  # pixels


def simplify(contour, traced_d):
    """Drop smooth control points, one at a time, while the Catmull-Rom curve
    through the rest keeps within SIMPLIFY_TOLERANCE of the traced outline, and
    the dropped point within it of the new curve."""
    ref = np.array(
        [p for poly in geo.flatten(geo.parse_path(traced_d), 0.1) for p in poly]
    )
    pts = [list(p) for p in contour]
    changed = True
    while changed and len(pts) > 6:
        changed = False
        k = 0
        while k < len(pts) and len(pts) > 6:
            if pts[k][2]:
                k += 1
                continue
            trial = pts[:k] + pts[k + 1 :]
            n = len(trial)
            # The new curve between the dropped point's second neighbours.
            lo = (k - 2) % n
            local = [trial[(lo + j) % n] for j in range(-1, 5)]
            samples = _local_curve(local)
            if _fits(samples, ref, pts[k]):
                pts = trial
                changed = True
            else:
                k += 1
    return pts


def _local_curve(local):
    """Samples of the closed Catmull-Rom curve's segments local[1]..local[4],
    given one point more on each side for the tangents."""
    out = []
    for i in range(1, 4):
        a, p, q, b = local[i - 1], local[i], local[i + 1], local[i + 2]
        tp = (0.0, 0.0) if p[2] else ((q[0] - a[0]) / 2, (q[1] - a[1]) / 2)
        tq = (0.0, 0.0) if q[2] else ((b[0] - p[0]) / 2, (b[1] - p[1]) / 2)
        c1 = (p[0] + tp[0] / 3, p[1] + tp[1] / 3)
        c2 = (q[0] - tq[0] / 3, q[1] - tq[1] / 3)
        for s in range(9):
            out.append(_bezier_point(p, c1, c2, q, s / 8))
    return np.array(out)


def _fits(samples, ref, dropped):
    d2 = ((samples[:, None, :] - ref[None, :, :]) ** 2).sum(axis=2)
    if np.sqrt(d2.min(axis=1)).max() > SIMPLIFY_TOLERANCE:
        return False
    gap = np.sqrt(((samples - np.array(dropped[:2])) ** 2).sum(axis=1)).min()
    return gap <= SIMPLIFY_TOLERANCE


def _bezier_point(p, c1, c2, q, t):
    u = 1 - t
    return tuple(
        u**3 * p[i] + 3 * u * u * t * c1[i] + 3 * u * t * t * c2[i] + t**3 * q[i]
        for i in (0, 1)
    )


def smoothed(contours, boxes):
    """The contours with every control point inside one of the boxes made smooth."""
    for c in contours:
        for p in c:
            if any(x0 <= p[0] <= x1 and y0 <= p[1] <= y1 for x0, y0, x1, y1 in boxes):
                p[2] = 0
    return contours


def build_shapes(regions, signs, rest=None):
    shapes = []
    smooth = getattr(signs, "SMOOTH", {})

    def contours(sid, d):
        return [
            simplify(c, d) for c in smoothed(control_points(d), smooth.get(sid, []))
        ]

    for gid, kind, owner, label, regs in signs.GROUPS:
        for rid, _seeds in regs:
            if rid == signs.STROKE_REGION:
                continue
            part = signs.PART_NAMES.get(rid, "")
            shapes.append(
                {
                    "id": rid,
                    "group": gid,
                    "kind": kind,
                    "owner": owner,
                    "label": f"{label}, {part}" if part else label,
                    "short": signs.SHORT[gid] + (f", {part}" if part else ""),
                    "type": "outline",
                    "contours": contours(rid, regions[rid]["d"]),
                    "note": "",
                }
            )
        if gid == signs.STROKE["group"]:
            st = signs.STROKE
            shapes.append(
                {
                    "id": st["id"],
                    "group": gid,
                    "kind": kind,
                    "owner": owner,
                    "label": label,
                    "short": signs.SHORT[gid],
                    "type": "stroke",
                    "centerline": [list(p) for p in st["centerline"]],
                    "width": st["width"],
                    "caps": list(st["caps"]),
                    "note": "",
                }
            )
            if rest:
                part = signs.STROKE_REST["part"]
                shapes.append(
                    {
                        "id": rest["id"],
                        "group": gid,
                        "kind": kind,
                        "owner": owner,
                        "label": f"{label}, {part}",
                        "short": f"{signs.SHORT[gid]}, {part}",
                        "type": "outline",
                        "contours": contours(rest["id"], rest["d"]),
                        "note": "",
                    }
                )
    return shapes


def run(work, draft_name):
    signs, prefix = ct_drafts.draft(draft_name)
    l1 = json.loads((work / "level1.json").read_text(encoding="utf-8"))
    regions = json.loads((work / f"{prefix}-regions.json").read_text(encoding="utf-8"))
    w, h = l1["width"], l1["height"]
    shapes = build_shapes(regions["regions"], signs, regions.get("rest"))
    for s in shapes:
        if s["type"] == "outline":
            n = sum(len(c) for c in s["contours"])
            print(
                f"{s['id']:5} {s['short']:28} {len(s['contours'])} contours, {n} points"
            )
    if signs.JUDGMENTS is not ct_share.ct_signs.JUDGMENTS:
        raise SystemExit(
            "ct_share reads draft 1's judgments, and this draft has its own"
        )
    ink = ct_share.ink_mask(l1, signs)
    masks = {s["id"]: ct_share.shape_mask(s, w, h) for s in shapes}
    share, count, near_any = ct_share.share_out(ink, masks)
    ct_share.print_share(f"{prefix}-shapes", share)
    out = {"width": w, "height": h, "shapes": shapes}
    with open(
        work / f"{prefix}-shapes.json", "w", encoding="utf-8", newline="\n"
    ) as fp:
        json.dump(out, fp, ensure_ascii=False, indent=1)
        fp.write("\n")
    _picture(work, l1, shapes, ink, count, near_any, w, h, prefix)


def _picture(work, l1, shapes, ink, count, near_any, w, h, prefix):
    scale = 3
    with Image.open(work / l1["image"]) as im:
        base = im.convert("RGB").resize(
            (w * scale, h * scale), Image.Resampling.BICUBIC
        )
    over = np.zeros((h * S, w * S, 4), dtype=np.uint8)
    over[ink & ~near_any] = (255, 0, 0, 230)
    over[ink & (count >= 2)] = (255, 0, 255, 150)
    pic = Image.alpha_composite(base.convert("RGBA"), Image.fromarray(over, "RGBA"))
    draw = ImageDraw.Draw(pic)
    for s in shapes:
        colour = (0, 90, 255, 255) if s["type"] == "outline" else (0, 160, 0, 255)
        for poly in geo.flatten(geo.parse_path(ctg.shape_d(s))):
            pts = [(x * scale, y * scale) for x, y in poly]
            draw.line(pts + [pts[0]], fill=colour, width=1)
        if s["type"] == "outline":
            for c in s["contours"]:
                for x, y, corner in c:
                    r = 2
                    box = (x * scale - r, y * scale - r, x * scale + r, y * scale + r)
                    if corner:
                        draw.rectangle(box, outline=(255, 120, 0, 255))
                    else:
                        draw.ellipse(box, outline=(0, 0, 0, 255))
    pic.convert("RGB").save(work / f"{prefix}-shapes.png")
