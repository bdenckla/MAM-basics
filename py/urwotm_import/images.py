"""Download the series' images, and build the contact sheets used to name them.

The ``docs-images-rt`` URLs in a published Google Doc are **per-render
tokens**: they change every time Google re-renders the document, exactly like
the ``.cN`` class names (see ``fetch.py``). So the URLs are read from the
pinned snapshot and downloaded in the same run, and the bytes are what get
committed -- the URL itself is worthless as a durable identifier.

Images are saved positionally first (``p1-01.png``), because position is the
only name available before a human has looked at them. ``img_names.py``
later maps those to descriptive filenames matching the existing ``misc/img/``
convention (``Deut 12v30 לאמר -- BHS.png``), and the ``rename`` subcommand
applies them to both the files and the emitted ``para_for_img`` strings.
"""

import io
import json

from PIL import Image

from mb_cmn import paths
from urwotm_import import gdoc_parse
from urwotm_import import img_names
from urwotm_import import parts

# The published URLs already end in "=s2048". styles_authored.css sets
# img { max-width: 100% } inside a 40em body, so 2048px is generous; "=s0"
# would risk multi-MB blobs in git for no visible gain.
_SIZE_SUFFIX = "=s2048"

# Displayed width below which an image is a candidate for the width10em
# class -- the only width classes styles_authored.css defines are
# width10em and width5em. 200px is roughly what the existing exemplars use
# (tsinnorit_and_the_xxd_in_bhs marks its 190x93 crops width10em).
_NARROW_PX = 200

# styles_authored.css sets img { max-width: 100% } but never a width, so an
# image renders at its *intrinsic* size. Where the =s2048 download is much
# bigger than the size the Google Doc displayed it at, the ported page will
# show it correspondingly larger than Ben laid it out.
_OVERSIZE_RATIO = 1.3

_MAGIC = (
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"\xff\xd8\xff", "jpg"),
    (b"GIF87a", "gif"),
    (b"GIF89a", "gif"),
    (b"RIFF", "webp"),
)


def collect_refs(docs):
    """Every image in every part, with the prose immediately around it."""
    refs = []
    for part, doc in sorted(docs.items()):
        img_blocks = [
            (i, b) for i, b in enumerate(_flat_blocks(doc)) if b["kind"] == "img"
        ]
        flat = _flat_blocks(doc)
        for ordinal, (index, block) in enumerate(img_blocks, start=1):
            refs.append(
                {
                    "part": part,
                    "ordinal": ordinal,
                    "stem": f"p{part}-{ordinal:02d}",
                    "url": block["src"],
                    "disp_w": block["width"],
                    "disp_h": block["height"],
                    "alt": block["alt"],
                    "before": _neighbour_text(flat, index, -1),
                    "after": _neighbour_text(flat, index, +1),
                }
            )
    return refs


def download(refs, downloader):
    """Fetch each image, detect its format, and write it to the cache."""
    out_dir = parts.img_cache_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    for ref in refs:
        body = downloader.get_bytes(_sized_url(ref["url"]), obey_robots=False)
        ext = _format_of(body)
        with Image.open(io.BytesIO(body)) as image:
            # Pillow confirms the magic-byte guess and supplies real pixels.
            pil_format = (image.format or "").lower()
            ref["px_w"], ref["px_h"] = image.size
        assert _formats_agree(ext, pil_format), (ref["stem"], ext, pil_format)
        ref["format"] = ext
        ref["bytes"] = len(body)
        ref["file"] = f"{ref['stem']}.{ext}"
        (out_dir / ref["file"]).write_bytes(body)
    return refs


def write_manifest(refs):
    path = parts.cache_dir() / "img_manifest.json"
    path.write_text(
        json.dumps(refs, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def read_manifest():
    path = parts.cache_dir() / "img_manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


def cached_refs():
    """The manifest, if it exists and every file it names is still present.

    Re-downloading is 52 throttled requests, so the reports and contact
    sheets are worth regenerating without paying for that again.
    """
    path = parts.cache_dir() / "img_manifest.json"
    if not path.exists():
        return None
    refs = read_manifest()
    img_dir = parts.img_cache_dir()
    if any(not (img_dir / ref["file"]).exists() for ref in refs):
        return None
    return refs


def install(refs, part_nums):
    """Copy the cached bytes into the docs tree under their real names.

    The cache is wiped by ``main_repo_maintenance.py`` step 1, so this is the
    step that turns 52 downloaded blobs into committed bytes.
    """
    out_dir = (
        paths.sibling_repo("MAM-with-doc") / "gh-pages" / "misc" / "img" / "urwotm"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    src_dir = parts.img_cache_dir()
    written = []
    for ref in refs:
        if ref["part"] not in part_nums:
            continue
        name = img_names.descriptive(ref["stem"], ref["file"])
        (out_dir / name).write_bytes((src_dir / ref["file"]).read_bytes())
        written.append(out_dir / name)
    return written


def manifest_report(refs):
    total_kb = sum(r["bytes"] for r in refs) // 1024
    lines = [
        "# Image manifest",
        "",
        f"{len(refs)} images, {total_kb // 1024} MB. `disp` is the size the "
        f"Google Doc displayed the image at; `px` is the downloaded "
        f"`{_SIZE_SUFFIX}` size, which is what the ported page will render "
        "at, since the house stylesheet caps width but never sets it.",
        "",
        f"- **width10em?** -- displayed under {_NARROW_PX}px wide.",
        f"- **x bigger** -- `px / disp`, flagged above {_OVERSIZE_RATIO}: the "
        "ported page shows this one that much larger than the source did.",
        "",
        "| file | part | disp | px | format | KB | width10em? | x bigger |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for ref in refs:
        narrow = "yes" if _is_narrow(ref) else ""
        ratio = _oversize_ratio(ref)
        big = f"{ratio:.1f}x" if ratio and ratio >= _OVERSIZE_RATIO else ""
        lines.append(
            f"| {ref['file']} | {ref['part']} | "
            f"{ref['disp_w']}x{ref['disp_h']} | {ref['px_w']}x{ref['px_h']} | "
            f"{ref['format']} | {ref['bytes'] // 1024} | {narrow} | {big} |"
        )
    lines.append("")
    return lines


def write_contact_sheets(refs):
    """One browsable page per part: each image between its two neighbours.

    Written as plain HTML into the image cache dir so that ``src="img/..."``
    resolves, and opened by Ben from a ``file://`` URL.
    """
    written = []
    by_part = {}
    for ref in refs:
        by_part.setdefault(ref["part"], []).append(ref)
    for part, part_refs in sorted(by_part.items()):
        path = parts.cache_dir() / f"contact_sheet_p{part}.html"
        path.write_text(
            _contact_sheet_html(part, part_refs), encoding="utf-8", newline="\n"
        )
        written.append(path)
    return written


###########################################################


def _flat_blocks(doc):
    """Blocks in reading order, flattening table cells inline."""
    out = []
    for block in doc.blocks:
        if block["kind"] == "table":
            out.append(block)
            for row in block["rows"]:
                for cell in row:
                    out.extend(cell)
            continue
        out.append(block)
    return out


def _neighbour_text(flat, index, step):
    i = index + step
    while 0 <= i < len(flat):
        text = gdoc_parse.block_text(flat[i])
        if text:
            return text
        if flat[i]["kind"] == "img":
            return "(adjacent image)"
        i += step
    return ""


def _sized_url(url):
    if url.endswith(_SIZE_SUFFIX):
        return url
    base = url.split("=s")[0]
    return base + _SIZE_SUFFIX


def _format_of(body):
    for magic, ext in _MAGIC:
        if body.startswith(magic):
            return ext
    raise ValueError(f"unrecognized image magic bytes: {body[:12]!r}")


def _formats_agree(ext, pil_format):
    return pil_format in (ext, {"jpg": "jpeg"}.get(ext, ext))


def _is_narrow(ref):
    return bool(ref["disp_w"]) and ref["disp_w"] < _NARROW_PX


def _oversize_ratio(ref):
    if not ref["disp_w"]:
        return None
    return ref["px_w"] / ref["disp_w"]


def _contact_sheet_html(part, part_refs):
    rows = []
    for ref in part_refs:
        flags = []
        if _is_narrow(ref):
            flags.append("width10em candidate")
        ratio = _oversize_ratio(ref)
        if ratio and ratio >= _OVERSIZE_RATIO:
            flags.append(f"renders {ratio:.1f}x bigger than the source")
        narrow = f" &nbsp;<b>[{'; '.join(flags)}]</b>" if flags else ""
        rows.append(f"""<section>
  <h2>{ref['stem']}</h2>
  <p class="meta">{ref['file']} &middot;
     displayed {ref['disp_w']}x{ref['disp_h']} &middot;
     {ref['px_w']}x{ref['px_h']} px &middot;
     {ref['bytes'] // 1024} KB{narrow}</p>
  <p class="ctx before">{_esc(ref['before'])}</p>
  <p><img src="img/{ref['file']}"></p>
  <p class="ctx after">{_esc(ref['after'])}</p>
</section>""")
    body = "\n".join(rows)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>urwotm Part {part} contact sheet</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ max-width: 55em; margin: 0 auto; padding: 1em;
         font-family: Georgia, serif; }}
  section {{ border-top: 2px solid gray; padding-top: 0.5em;
            margin-top: 2em; }}
  h2 {{ font-family: monospace; margin: 0; }}
  .meta {{ font-size: 85%; color: gray; margin: 0.2em 0 1em 0; }}
  .ctx {{ font-size: 90%; }}
  .before::before {{ content: "\\2191 before: "; color: gray; }}
  .after::before {{ content: "\\2193 after: "; color: gray; }}
  img {{ max-width: 100%; border: 1px solid gray; }}
</style></head><body>
<h1>Undoing and redoing the work of the Masoretes &ndash; Part {part}</h1>
<p>{len(part_refs)} images, in document order, each between the prose that
precedes and follows it.</p>
{body}
</body></html>
"""


def _esc(text):
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
