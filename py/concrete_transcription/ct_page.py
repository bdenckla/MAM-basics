"""Write the trial's page: the image, the ink, the draft shapes and the editor.

Written for the concrete-transcription trial, 2026-11-03.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py page
        <work-dir> <out.html> [<draft>]

Reads level1.json, draft-shapes.json (draft2-shapes.json for draft 2, and so on:
ct_drafts.py) and 112-Detail.png from <work-dir>, the template beside this
module, and the change's record from in/UXLC-misc/all_changes.json, whose Hebrew
it copies.  The draft's data module gives the page's draft-specific text.  The
page's ink is level 1's fills and the pieces judged ink; for a draft with strips
of vellum, each fill that a strip touches is traced again from its samples less
the strips', so that the page counts the ink as ct_share.ink_mask does.
"""

import base64
import html
import json
from pathlib import Path

import numpy as np
from PIL import Image

from accgram.rtms_report import expand_uxlc_change_ref
from hkq_cmn.uxlc_manuscript_page import sefaria_image_url
from mb_cmn import paths
from pen_stroke import level5
from pen_stroke import region_derive as rd
from pen_stroke import region_render
from pen_stroke import stroke_svg
from concrete_transcription import ct_area
from concrete_transcription import ct_drafts
from concrete_transcription import ct_share

_HERE = Path(__file__).resolve().parent

RELEASE, CHANGESET, N = "2023.07.04", "2023.03.25", 112
# The clean page's two colours for the letter-and-mark clusters, by turns.
CLUSTER_COLOURS = ["#000000", "#c05800"]
# The clean page's soft edges: a Gaussian blur's standard deviation, in pixels of
# the image, the image's own fade.  ct_edges.py fitted it to draft 3's outlines on
# 2026-11-04: 2.4 px, the outlines left where they are (1.8 px if the vellum about
# the letters may be darker than the median); and Ben asked for it ("Yes, widen
# it").  It was 1.0 px, a first guess, before.
SOFT_EDGE = 2.4
OWNER_NAMES = {
    "this-word": "this atom",
    "other-word": "another atom of this line",
    "this-line": "this line",
    "line-above": "the line above",
    "line-below": "the line below",
}


def change_record():
    recs = json.loads(
        (paths.repo_root() / "in/UXLC-misc/all_changes.json").read_text(
            encoding="utf-8"
        )
    )
    hits = [
        r
        for r in recs
        if r["release"] == RELEASE and r["changeset"] == CHANGESET and r["n"] == N
    ]
    if len(hits) != 1:
        raise SystemExit(f"expected one change record, found {len(hits)}")
    return hits[0]


def fills_d(l1, signs):
    """The path data of level 1's fills, for the page's ink, less the draft's
    strips of vellum: a fill that a strip touches is traced again from its samples
    less the strips', by the tracer and speck size of the draft's regions."""
    fills = l1["fills"]
    w, h = l1["width"], l1["height"]
    strips = ct_share.strips_mask(signs, w, h)
    if strips is None:
        return "".join(f["d"] for f in fills)
    touched = [f for f in fills if (rd.scaled_mask([f["d"]], w, h) & strips).any()]
    kept = "".join(f["d"] for f in fills if f not in touched)
    mask = rd.scaled_mask([f["d"] for f in touched], w, h) & ~strips
    print("fills traced again, less the strips of vellum:", [f["id"] for f in touched])
    return kept + rd.trace_samples(mask, l1["speck_size"])


def image_tones(work, l1):
    """The image's ink and vellum, for the clean page's colours and its difference
    from the image: the median colour and luminance of the pixels two and more
    inside the level-1 threshold, and of those six and more outside it."""
    with Image.open(work / l1["image"]) as im:
        rgb = np.asarray(im.convert("RGB"), dtype=np.float64)
        lum = np.asarray(im.convert("L"), dtype=np.float64)
    ink = lum < l1["threshold"]
    core = ct_area.erode(ink, 2)
    vellum = ct_area.distance_steps(ink, 6) > 6

    def hexcolour(mask):
        return "#" + "".join(
            f"{round(float(np.median(rgb[..., k][mask]))):02x}" for k in range(3)
        )

    return {
        "ink_rgb": hexcolour(core),
        "vellum_rgb": hexcolour(vellum),
        "ink_lum": float(np.median(lum[core])),
        "vellum_lum": float(np.median(lum[vellum])),
    }


def run(work, out, draft_name):
    signs, prefix = ct_drafts.draft(draft_name)
    if set(OWNER_NAMES) != set(stroke_svg.INK_OWNERS):
        raise SystemExit("the owners' names and stroke_svg.INK_OWNERS disagree")
    # A letter may mark several places; each letter has one question's text.
    letters = list(dict.fromkeys(q["letter"] for q in signs.QUESTIONS))
    if letters != [k for k, _t in signs.QUESTION_ITEMS]:
        raise SystemExit("the questions' rings and their text disagree")
    rec = change_record()
    folio = rec["lc"].split()[0].removeprefix("Folio_")
    l1 = json.loads((work / "level1.json").read_text(encoding="utf-8"))
    draft = json.loads((work / f"{prefix}-shapes.json").read_text(encoding="utf-8"))
    pieces = {p["id"]: p for p in l1["pieces"]}
    ink_d = fills_d(l1, signs)
    ink_d += "".join(
        pieces[pid]["d"] for pid, (j, _w) in signs.JUDGMENTS.items() if j == "ink"
    )
    photo = base64.b64encode((work / l1["image"]).read_bytes()).decode("ascii")
    data = {
        "trial": "concrete-transcription-2026-11-03",
        "draft_version": signs.DRAFT_VERSION,
        "store_key": f"concrete-transcription-2026-11-03/{signs.DRAFT_VERSION}",
        "image_name": f"{l1['image']}, {l1['width']} x {l1['height']}",
        "download_name": signs.DOWNLOAD_NAME,
        "width": l1["width"],
        "height": l1["height"],
        "photo": f"data:image/png;base64,{photo}",
        "ink_d": ink_d,
        "shapes": draft["shapes"],
        "palette": list(region_render.REGION_COLOURS),
        "group_short": signs.SHORT,
        "owner_names": OWNER_NAMES,
        "kinds": list(level5.KINDS),
        "questions": signs.QUESTIONS,
        "clusters": getattr(signs, "CLUSTERS", {}),
        "cluster_colours": CLUSTER_COLOURS,
        "soft_edge": SOFT_EDGE,
        **image_tones(work, l1),
    }
    print(
        "tones",
        {k: data[k] for k in ("ink_rgb", "vellum_rgb", "ink_lum", "vellum_lum")},
    )
    text = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    template = (_HERE / "ct_page_template.html").read_text(encoding="utf-8")
    items = "\n".join(
        f'        <li><span class="q">{k}.</span> {t}</li>'
        for k, t in signs.QUESTION_ITEMS
    )
    page = (
        template.replace("@@DATA@@", text)
        .replace("@@MADE@@", getattr(signs, "MADE", "2026-11-03"))
        .replace("@@DRAFT_NOTE@@", signs.DRAFT_NOTE)
        .replace("@@QUESTION_ITEMS@@", items)
        .replace("@@QUESTION_LETTERS@@", signs.QUESTION_LETTERS)
        .replace("@@WORD@@", html.escape(rec["reftext"]))
        .replace(
            "@@CHANGE_URL@@",
            html.escape(expand_uxlc_change_ref(f"{RELEASE}/{CHANGESET}-{N}")),
        )
        .replace("@@LC_URL@@", html.escape(sefaria_image_url(folio)))
    )
    if "@@" in page:
        raise SystemExit("a placeholder is left in the page")
    with open(out, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(page)
    print(out, len(page), "characters")
    print("change", expand_uxlc_change_ref(f"{RELEASE}/{CHANGESET}-{N}"))
    print("page image", sefaria_image_url(folio))
