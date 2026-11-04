"""Write the trial's production preview, and the production images it shows.

Written for the concrete-transcription trial, 2026-11-04.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py preview
        <work-dir> <out.html> <draft>
    ./.venv/Scripts/python.exe py/main_concrete_transcription.py production
        <work-dir> <out-dir> <draft>

Ben asked on 2026-11-04 to 'Prepare a "production preview" page that shows a
single image in the following way: no controls; clicking it just cycles between 3
views: original image, concrete transcription with stray stroke present, and
concrete transcription with stray stroke removed.'  The concrete transcription is
the development page's clean page at the defaults he set the same day: the atom's
own shapes, each whole, without the masora circle, other atoms' and lines' ink or
the red of ink no outline holds, in the image's ink and vellum, with soft edges.
The shapes are the draft's as Claude drew them, not anyone's edits in a browser;
their path data is ct_geometry's, the construction of the development page's
script, outlines filled by the even-odd rule and strokes by the nonzero rule, as
its rule() does.  Reads level1.json, the draft's shapes file (ct_drafts.py) and
the image from <work-dir>, and the template beside this module.

The production images are the preview's two views of the transcription, each a
standalone SVG file the image's size, in its pixels, drawn as the preview draws
that view: Ben asked later that day for the production version's images
"committed to MAM-basics somewhere appropriate", to be shown elsewhere.  The
image's own view is the trial's image itself.  production writes them into
<out-dir>, which for the tracked copies is doc/concrete-transcription-2026-11-03/
production/.
"""

import base64
import html
import json
from pathlib import Path

from pen_stroke import level5
from concrete_transcription import ct_drafts
from concrete_transcription import ct_geometry as ctg
from concrete_transcription import ct_page

_HERE = Path(__file__).resolve().parent
MADE = "2026-11-04"
ZOOM = 1.5  # the development page's sizes since 2026-11-04
RULES = {"outline": "evenodd", "stroke": "nonzero"}
# The views, in the order a click shows them: each one's name, which the image's
# tooltip gives, whether it draws the transcription, and whether the stray stroke.
VIEWS = [
    ("The image", False, False),
    ("The concrete transcription, with the stray stroke", True, True),
    ("The concrete transcription, without the stray stroke", True, False),
]
# Each production image's filename, by whether it draws the stray stroke; {draft}
# is the draft's name.
PRODUCTION_NAMES = {
    True: "concrete-transcription-{draft}-with-stray-stroke.svg",
    False: "concrete-transcription-{draft}-without-stray-stroke.svg",
}


def drawn(s):
    """Whether the clean page at its defaults draws s: the atom's own letters, marks
    and stray mark, but not the masora circle, which the template's meaningOf sets
    aside whosever ink it is, nor other atoms' and lines' ink."""
    if s["kind"] not in level5.KINDS or s["owner"] not in ct_page.OWNER_NAMES:
        raise SystemExit(
            f"{s['id']}: unknown kind {s['kind']!r} or owner {s['owner']!r}"
        )
    return s["owner"] == "this-word" and s["kind"] != "masora circle mark"


def paths(shapes):
    return "".join(
        f'<path d="{ctg.shape_d(s)}" fill-rule="{RULES[s["type"]]}"/>' for s in shapes
    )


def transcription(work, draft_name):
    """The draft's data module, level 1, the transcription's letters and marks and
    its stray stroke, and the image's ink and vellum (ct_page.image_tones)."""
    signs, prefix = ct_drafts.draft(draft_name)
    l1 = json.loads((work / "level1.json").read_text(encoding="utf-8"))
    draft = json.loads((work / f"{prefix}-shapes.json").read_text(encoding="utf-8"))
    if (draft["width"], draft["height"]) != (l1["width"], l1["height"]):
        raise SystemExit("the shapes' size and the image's disagree")
    atom = [s for s in draft["shapes"] if drawn(s)]
    letters = [s for s in atom if s["kind"] != "stray mark"]
    stray = [s for s in atom if s["kind"] == "stray mark"]
    print("letters and marks:", " ".join(s["id"] for s in letters))
    print("the stray stroke:", " ".join(s["id"] for s in stray))
    print("not drawn:", " ".join(s["id"] for s in draft["shapes"] if not drawn(s)))
    tones = ct_page.image_tones(work, l1)
    print("tones", tones)
    return signs, l1, letters, stray, tones


def soft_filter(fid, w, h):
    """The soft edges: one Gaussian blur of ct_page.SOFT_EDGE, the image's own
    fade, over the shapes."""
    return (
        f'<filter id="{fid}" filterUnits="userSpaceOnUse" x="-4" y="-4"'
        f' width="{w + 8}" height="{h + 8}">'
        f'<feGaussianBlur stdDeviation="{ct_page.SOFT_EDGE}"/></filter>'
    )


def transcribed_view(fid, w, h, tones, ink):
    """A view of the transcription: vellum, and over it the ink, softened by the
    filter fid."""
    return (
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="{tones["vellum_rgb"]}"/>'
        f'<g filter="url(#{fid})" fill="{tones["ink_rgb"]}">{ink}</g>'
    )


def run(work, out, draft_name):
    signs, l1, letters, stray, tones = transcription(work, draft_name)
    w, h = l1["width"], l1["height"]
    photo = base64.b64encode((work / l1["image"]).read_bytes()).decode("ascii")
    tips, groups = [], []
    for k, (name, transcribed, with_stray) in enumerate(VIEWS):
        tips.append(html.escape(f"{name} ({k + 1} of {len(VIEWS)})"))
        if transcribed:
            ink = '<use href="#letters"/>' + (paths(stray) if with_stray else "")
            body = transcribed_view("soft", w, h, tones, ink)
        else:
            body = f'<image href="data:image/png;base64,{photo}" x="0" y="0" width="{w}" height="{h}"/>'
        hidden = ' display="none"' if k else ""
        groups.append(f'<g data-name="{tips[k]}"{hidden}>{body}</g>')
    svg = "\n".join(
        [
            f'<svg id="view" viewBox="0 0 {w} {h}" width="{ctg.fmt(w * ZOOM)}"'
            f' height="{ctg.fmt(h * ZOOM)}" role="button" tabindex="0"'
            ' aria-labelledby="view-tip" xmlns="http://www.w3.org/2000/svg">',
            f'<title id="view-tip">{tips[0]}</title>',
            f"<defs>{soft_filter('soft', w, h)}",
            f'<g id="letters">{paths(letters)}</g></defs>',
            *groups,
            "</svg>",
        ]
    )
    template = (_HERE / "ct_preview_template.html").read_text(encoding="utf-8")
    page = template.replace("@@MADE@@", MADE).replace("@@DRAFT@@", signs.DRAFT_VERSION)
    if "@@" in page.replace("@@SVG@@", ""):
        raise SystemExit("a placeholder is left in the page")
    page = page.replace("@@SVG@@", svg)
    with open(out, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(page)
    print(out, len(page), "characters")


def production(work, out_dir, draft_name):
    """Write the draft's production images into out_dir: each view of the preview
    that draws the transcription, as a standalone SVG file the image's size, its
    filter's id its filename's stem, so that the two can share a page."""
    signs, l1, letters, stray, tones = transcription(work, draft_name)
    w, h = l1["width"], l1["height"]
    out_dir.mkdir(parents=True, exist_ok=True)
    for k, (name, transcribed, with_stray) in enumerate(VIEWS):
        if not transcribed:
            continue
        filename = PRODUCTION_NAMES[with_stray].format(draft=draft_name)
        fid = filename.removesuffix(".svg") + "-soft"
        ink = paths(letters) + (paths(stray) if with_stray else "")
        about = (
            f"Made by Claude (Opus 5.5) on {MADE} for the concrete transcription"
            f" trial: view {k + 1} of {len(VIEWS)} of its production preview"
            f" ({signs.DRAFT_VERSION}), at the image's size.  Written by"
            " py/concrete_transcription/ct_preview.py, as"
            " doc/concrete-transcription-2026-11-03/README.md says.  The outlines are"
            " traced from the detail image of UXLC change 2023.03.25-112;"
            " DATA-LICENSES.md gives its terms."
        )
        if "--" in about:
            raise SystemExit("an XML comment may not hold two hyphens together")
        svg = "\n".join(
            [
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"'
                f' width="{w}" height="{h}" role="img">',
                f"<!-- {about} -->",
                f"<title>{html.escape(name)}</title>",
                f"<defs>{soft_filter(fid, w, h)}</defs>",
                transcribed_view(fid, w, h, tones, ink),
                "</svg>",
                "",
            ]
        )
        with open(out_dir / filename, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(svg)
        print(out_dir / filename, len(svg), "characters")
