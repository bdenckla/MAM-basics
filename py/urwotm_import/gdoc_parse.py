"""Walk a published Google Doc into a role-tagged block stream.

The published HTML is flat: ``div#contents > div.doc-content`` holds a run of
``<p>``, ``<ul>``/``<ol>`` and ``<table>`` siblings, with all visual role
carried by ``class`` attributes that :mod:`urwotm_import.gdoc_css` resolves.
This module turns that into blocks and runs:

* A **block** is a dict with a ``kind`` of ``title``, ``subtitle``, ``para``,
  ``img``, ``list``, ``table`` or ``blank``.
* A **run** is a dict describing one stretch of uniformly-styled text:
  ``text``, ``bold``, ``italic``, ``sup``, ``strike``, ``color``, ``size_pt``,
  ``href``.

Google splits one sentence across many ``<span>`` elements at arbitrary
points, so adjacent runs with identical styling are merged before anything
downstream looks at them; otherwise a single italic accent name comes back as
two runs and gets emitted as two separate elements.
"""

from urllib.parse import parse_qs, urlsplit

import lxml.html

from urwotm_import import gdoc_css
from urwotm_import import normalize

_RUN_STYLE_KEYS = (
    "bold",
    "italic",
    "sup",
    "strike",
    "mono",
    "color",
    "size_pt",
    "href",
)

# What actually decides whether two adjacent runs are the same run.
#
# Deliberately *not* size_pt. Google splits words at arbitrary points and
# sometimes leaves the halves at different sizes -- Part 4 has "BHS" as "B"
# at the body size plus "HS" at 14pt. Since house style discards Google's
# type scale (Ben, mid-Phase-0), treating a size change as a run boundary
# only serves to tear words in half, and a torn word silently escapes
# dollarization: neither "B" nor "HS" matches the regex for $BHS, so the
# bare "BHS" survives to blow up dollar_sub at build time.
_MERGE_KEYS = tuple(k for k in _RUN_STYLE_KEYS if k != "size_pt")

# Google's own default text colors, which carry no authorial intent.
_DEFAULT_COLORS = ("#000000", "inherit", "")


class Doc:
    """A parsed document: its title, subtitle and block stream."""

    def __init__(self, part, sheet, blocks, gdoc_title):
        self.part = part
        self.sheet = sheet
        self.blocks = blocks
        self.gdoc_title = gdoc_title

    def blocks_of_kind(self, kind):
        return [b for b in self.blocks if b["kind"] == kind]


def parse_html(part: int, html: str) -> Doc:
    doc = lxml.html.fromstring(html)
    sheet = gdoc_css.parse_doc_style(doc)
    gdoc_title = _text_of_first(doc, "//div[@id='title']")
    content = doc.xpath("//div[contains(@class, 'doc-content')]")
    assert len(content) == 1, len(content)
    blocks = []
    for el in content[0].iterchildren():
        blocks.extend(_blocks_of_element(el, sheet))
    return Doc(part, sheet, blocks, gdoc_title)


def block_text(block) -> str:
    """The plain text of a block, for reports and the differential oracle."""
    kind = block["kind"]
    if kind in ("title", "subtitle", "para"):
        return normalize.norm_block("".join(r["text"] for r in block["runs"]))
    if kind == "list":
        return " ".join(
            normalize.norm_block("".join(r["text"] for r in item["runs"]))
            for item in block["items"]
        )
    if kind == "table":
        return " ".join(
            block_text(cell_block)
            for row in block["rows"]
            for cell in row
            for cell_block in cell
        )
    return ""


def runs_text(runs) -> str:
    return "".join(r["text"] for r in runs)


def unwrap_google_url(href: str) -> str:
    """Turn Google's redirect wrapper back into the real target URL.

    Published docs rewrite every external link as
    ``https://www.google.com/url?q=<real>&sa=D&...``. Internal bookmark links
    and already-bare URLs pass through unchanged.
    """
    if href is None:
        return None
    split = urlsplit(href)
    if split.netloc not in ("www.google.com", "google.com"):
        return href
    if split.path != "/url":
        return href
    targets = parse_qs(split.query).get("q")
    if not targets:
        return href
    return targets[0]


###########################################################


def _blocks_of_element(el, sheet):
    if el.tag == "p":
        return _blocks_of_para(el, sheet)
    if el.tag in ("ul", "ol"):
        return [_block_of_list(el, sheet)]
    if el.tag == "table":
        return [_block_of_table(el, sheet)]
    if el.tag in ("style", "script"):
        return []
    # Anything else is unexpected; surface it rather than dropping it.
    return [{"kind": "unknown", "tag": el.tag, "class": el.get("class")}]


def _blocks_of_para(el, sheet):
    classes = el.get("class") or ""
    para_props = sheet.para_props(classes)
    imgs = el.findall(".//img")
    runs = _runs_of(el, sheet)
    text = normalize.norm_block(runs_text(runs))
    kind = _para_kind(classes, para_props, text, imgs)
    if kind == "img":
        # One <p> can in principle hold several images plus a caption; each
        # image becomes its own block so nothing gets silently dropped.
        blocks = [_block_of_img(img, classes) for img in imgs]
        if text:
            blocks.append(_para_block("para", classes, para_props, runs))
        return blocks
    if kind == "blank":
        return [{"kind": "blank", "class": classes}]
    return [_para_block(kind, classes, para_props, runs)]


def _para_kind(classes, para_props, text, imgs):
    names = classes.split()
    if "title" in names:
        return "title"
    if "subtitle" in names:
        return "subtitle"
    if imgs:
        return "img"
    if not text:
        return "blank"
    return "para"


def _para_block(kind, classes, para_props, runs):
    return {
        "kind": kind,
        "class": classes,
        "align": para_props.get("text-align", "left"),
        # One Google indent step. Ben indents block quotations and nothing
        # else, so this is what an <blockquote> is recoverable from: Part 3's
        # "NOTE:" paragraph and Part 4's four Wickes/Breuer quotations.
        "indented": _indent_pt(para_props) >= 36.0,
        "runs": runs,
    }


def _indent_pt(para_props):
    margin = para_props.get("margin-left") or ""
    if not margin.endswith("pt"):
        return 0.0
    return float(margin[:-2])


def _block_of_img(img, classes=""):
    return {
        "kind": "img",
        "class": classes,
        "src": img.get("src"),
        "width": _px(img.get("style"), "width"),
        "height": _px(img.get("style"), "height"),
        "alt": img.get("alt") or "",
    }


def _block_of_list(el, sheet):
    """Recover list nesting from the ``margin-left`` of each ``<ul>``.

    Google flattens nested lists into sibling ``<ul class="lst-kix_...">``
    elements distinguished only by indentation, so depth is
    ``margin-left / 36pt`` -- 36pt being one Google indent step.
    """
    items = []
    for li in el.findall("li"):
        items.append(
            {"level": _indent_level(el, li, sheet), "runs": _runs_of(li, sheet)}
        )
    return {
        "kind": "list",
        "ordered": el.tag == "ol",
        "class": el.get("class"),
        "items": items,
    }


def _indent_level(ul_el, li_el, sheet):
    for el in (li_el, ul_el):
        margin = sheet.resolve(el.get("class")).get("margin-left")
        if margin and margin.endswith("pt"):
            return int(round(float(margin[:-2]) / 36.0))
    return 0


def _block_of_table(el, sheet):
    rows = []
    for tr in el.findall(".//tr"):
        row = []
        for td in tr.findall("td"):
            cell_blocks = []
            for child in td.iterchildren():
                cell_blocks.extend(_blocks_of_element(child, sheet))
            # Blank spacer paragraphs are kept here so the structural
            # tripwire's <p> count reconciles; the emitter drops them.
            row.append(cell_blocks)
        rows.append(row)
    return {"kind": "table", "class": el.get("class"), "rows": rows}


def _runs_of(el, sheet):
    """Collect the styled text runs of one block element, in order."""
    runs = []
    _collect_runs(el, sheet, {"href": None}, runs)
    return _merge_runs(runs)


def _collect_runs(el, sheet, inherited, out):
    ctx = dict(inherited)
    if el.tag == "a":
        ctx["href"] = unwrap_google_url(el.get("href"))
    props = sheet.resolve(el.get("class"))
    style = _style_of(props, ctx, el.tag)
    _add_text(out, el.text, style)
    for child in el.iterchildren():
        if child.tag == "img":
            _add_text(out, child.tail, style)
            continue
        _collect_runs(child, sheet, ctx, out)
        _add_text(out, child.tail, style)


def _style_of(props, ctx, tag):
    color = (props.get("color") or "").lower()
    vertical = (props.get("vertical-align") or "").strip()
    decoration = props.get("text-decoration") or ""
    family = (props.get("font-family") or "").lower()
    return {
        "bold": gdoc_css.is_bold(props),
        "italic": gdoc_css.is_italic(props),
        "sup": vertical == "super" or tag == "sup",
        "strike": "line-through" in decoration,
        # Part 1's Michigan-Claremont code line is distinguished from the
        # prose around it only by its font, so the font has to survive the
        # walk; content-sniffing "L \" / ) M O 63 R" would be guesswork.
        "mono": "courier" in family or "mono" in family,
        "color": None if color in _DEFAULT_COLORS else color,
        "size_pt": gdoc_css.font_size_pt(props),
        "href": ctx["href"],
    }


def _add_text(out, raw, style):
    text = normalize.norm_text(raw)
    if not text:
        return
    out.append({"text": text, **style})


def _merge_runs(runs):
    """Merge adjacent runs whose styling is identical."""
    merged = []
    for run in runs:
        if merged and _same_style(merged[-1], run):
            merged[-1]["text"] += run["text"]
            continue
        merged.append(dict(run))
    out = []
    for run in merged:
        run["text"] = normalize.norm_text(run["text"])
        if run["text"].strip() or (out and run["text"]):
            out.append(run)
    return out


def _same_style(a, b):
    return all(a[k] == b[k] for k in _MERGE_KEYS)


def _text_of_first(doc, xpath):
    found = doc.xpath(xpath)
    return normalize.norm_block(found[0].text_content()) if found else ""


def _px(style_attr, prop):
    if not style_attr:
        return None
    for chunk in style_attr.split(";"):
        name, _, value = chunk.partition(":")
        if name.strip() == prop and value.strip().endswith("px"):
            return int(round(float(value.strip()[:-2])))
    return None
