"""Compare CLC ruby with ordinary text and isolate the two NAEE CSS properties.

Run from the repository root with its interpreter. Supply --baseline with the
pre-fix commit and --browser with a Chromium/Edge executable; optionally supply
--comparison-font with another Hebrew TTF. Writes self-contained HTML, PNG and
JSON evidence only to .novc/clc-ruby-final-mark/. This is a manual differential
instrument, not a product generator or a test-suite entry point.
The current column uses the working checkout's complete stylesheet so spacing
changes are included in the ordinary-text regression comparison.
"""

import argparse
import base64
import html
import io
import json
import platform
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
from PIL import Image, ImageChops, ImageFilter
from playwright.sync_api import sync_playwright

from mb_cmn import paths

ROOT = paths.repo_root()
OUT = paths.novc_dir() / "clc-ruby-final-mark"
CELL_WIDTH = 400
CELL_HEIGHT = 240
VARIANTS = {
    "original": "",
    "display": "display:inline-block;",
    "line": "line-height:normal;",
    "both": "display:inline-block;line-height:normal;",
    "current": "",
}
COLLECT = """selector => [...document.querySelectorAll(selector)].map((r,i) => {
  const rt = r.querySelector('rt');
  const base = [...r.childNodes].filter(n => !['RT','RP'].includes(n.nodeName));
  const row = r.closest('tr');
  const ref = row?.querySelector('.clc-ref')?.textContent || r.closest('[id]')?.id || '';
  return {index:i,ref,html:r.outerHTML,base:base.map(n=>n.outerHTML ?? n.textContent).join(''),annotation:rt.innerHTML,
    qere:base.map(n=>n.textContent).join(''),ketiv:rt.textContent,
    style:[...r.querySelectorAll('span,rt')].map(e=>({tag:e.tagName,class:e.className,display:getComputedStyle(e).display,lineHeight:getComputedStyle(e).lineHeight,fontSize:getComputedStyle(e).fontSize}))};
})"""


def final_marks(text):
    indices = [i for i, c in enumerate(text) if "\u05d0" <= c <= "\u05ea"]
    return (
        [f"U+{ord(c):04X}" for c in text[indices[-1] + 1 :] if unicodedata.combining(c)]
        if indices
        else []
    )


def mask(image):
    result = image.convert("L").point(lambda v: 255 if v < 170 else 0)
    bbox = result.getbbox()
    if not bbox:
        raise AssertionError("empty glyph raster")
    return result.crop(bbox)


def compare(a, b):
    a, b = mask(a), mask(b)
    canvas_size = (max(a.width, b.width) + 12, max(a.height, b.height) + 12)
    ca = Image.new("L", canvas_size)
    ca.paste(a, (6, 6))
    expanded_a = ca.filter(ImageFilter.MaxFilter(3))
    best = None
    # Whole-raster translation registers the letters; 1px dilation tolerates raster rounding.
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            cb = Image.new("L", canvas_size)
            cb.paste(b, (6 + dx, 6 + dy))
            missing = ImageChops.subtract(ca, cb.filter(ImageFilter.MaxFilter(3)))
            extra = ImageChops.subtract(cb, expanded_a)
            count = np.count_nonzero(np.asarray(missing)) + np.count_nonzero(
                np.asarray(extra)
            )
            score = (int(count), abs(dx) + abs(dy), dx, dy)
            if best is None or score < best:
                best = score
    return {
        "outlier_pixels": best[0],
        "translation": list(best[2:]),
        "ink_size": [list(a.size), list(b.size)],
    }


def font_face(family, path, fmt):
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'@font-face{{font-family:"{family}";src:url(data:font/{fmt};base64,{encoded}) format("{fmt}");}}'


def review_html(samples, family, size, family_css, side, comparison_font, current_css):
    selector = {
        "clc-qere": "ruby.clc-kq span.clc-kq-q",
        "clc-ketiv": "ruby.clc-kq span.clc-kq-k",
        "na-qere": "ruby.near-aleppo-kq > rt > span",
    }[side]
    css = (
        ROOT.joinpath("gh-pages/document.css").read_text(encoding="utf-8") + family_css
    )
    current_css = re.sub(r"/\*.*?\*/", "", current_css, flags=re.S)
    current_css = re.sub(r"@font-face\s*\{[^}]*\}", "", current_css)
    css += re.sub(
        r"(^|\})(\s*)([^{}]+)\{",
        lambda m: m[1]
        + m[2]
        + ", ".join(".current " + selector.strip() for selector in m[3].split(","))
        + " {",
        current_css,
    )
    css += font_face(
        "Taamey D WOFF2", ROOT / "gh-pages/uxlc/woff2/Taamey_D.woff2", "woff2"
    )
    if comparison_font:
        css += font_face("Comparison Hebrew", comparison_font, "truetype")
    # Equal black foregrounds make the threshold independent of editorial colors.
    # The other ruby side is hidden without changing its layout or the text.
    css += f'body{{max-width:none;margin:0;width:{CELL_WIDTH * (len(VARIANTS) + 1)}px;color:black;background:white;}} .row{{display:flex;height:{CELL_HEIGHT}px;}} .cell{{box-sizing:border-box;width:{CELL_WIDTH}px;height:{CELL_HEIGHT}px;position:relative;color:black;}} .glyph{{position:absolute;top:75px;right:35px;white-space:nowrap;direction:rtl;line-height:normal;font-family:"{family}";font-size:{size}px;}} .glyph *{{color:black!important;}} .clc-kq-box{{border-color:transparent!important;}} .label{{font:12px sans-serif;position:absolute;top:0;left:4px;}}'
    for name, rule in VARIANTS.items():
        css += f".{name} {selector}{{{rule}}}"
    css += ".ordinary span.clc-kq-none{font-size:70%;}"
    if side == "clc-qere":
        css += ".candidate rt{visibility:hidden;}"
    elif side == "clc-ketiv" or side == "na-qere":
        css += ".candidate ruby > :not(rt){visibility:hidden;}"
    rows = []
    for sample in samples:
        cells = []
        for name in (*VARIANTS, "ordinary"):
            if name == "ordinary":
                content = sample["base"] if side == "clc-qere" else sample["annotation"]
            else:
                content = sample["html"]
                if side.startswith("clc"):
                    content = f'<span class="clc-kq-box">{content}</span>'
            cells.append(
                f'<div class="cell {name}"><span class="label">{sample["id"]} {name}</span><div class="glyph {"candidate" if name != "ordinary" else ""}" dir="rtl">{content}</div></div>'
            )
        rows.append('<div class="row">' + "".join(cells) + "</div>")
    return (
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>CLC ruby comparison</title><style>'
        + css
        + "</style><body>"
        + "".join(rows)
        + "</body></html>"
    )


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="pre-fix MAM-basics commit")
    parser.add_argument("--browser", required=True, help="Chromium/Edge executable")
    parser.add_argument("--comparison-font", type=Path, help="optional Hebrew TTF")
    parser.add_argument("--sizes", nargs="+", type=float, default=[26.1333333333, 48])
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    baseline = subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{args.baseline}^{{commit}}"],
        cwd=ROOT,
        text=True,
    ).strip()
    clc_css = subprocess.check_output(
        ["git", "show", f"{baseline}:gh-pages/uxlc/style.css"],
        cwd=ROOT,
        encoding="utf-8",
    )
    current_clc_css = (ROOT / "gh-pages/uxlc/style.css").read_text(encoding="utf-8")
    current_na_css = (ROOT / "py/near_aleppo/edition.css").read_text(encoding="utf-8")
    na_css = current_na_css
    na_css, removed = re.subn(
        r"ruby\.near-aleppo-kq > rt > span\s*\{[^}]*\}", "", na_css
    )
    assert removed == 1, "expected the single NAEE span repair rule"
    all_results = []
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=args.browser, headless=True)
        page = browser.new_page(
            viewport={"width": CELL_WIDTH * (len(VARIANTS) + 1), "height": 900},
            device_scale_factor=1,
            color_scheme="light",
        )
        page.on("pageerror", lambda error: errors.append(str(error)))
        # Serve tracked bytes through intercepted loopback URLs; no server or
        # external request is needed, including where file: URLs are blocked.
        page.route(
            "http://localhost:8765/**",
            lambda route: route.fulfill(
                path=str(ROOT / urlparse(route.request.url).path.lstrip("/"))
            ),
        )
        corpus = []
        for path in sorted((ROOT / "gh-pages/uxlc/clc").glob("*.html")):
            page.goto("http://localhost:8765/" + path.relative_to(ROOT).as_posix())
            page.evaluate("document.fonts.ready")
            units = page.evaluate(COLLECT, "td.clc-text ruby.clc-kq")
            for unit in units:
                unit["id"] = f'{path.stem}:{unit["ref"]}:{unit["index"]}'
                unit["source"] = path.relative_to(ROOT).as_posix()
                unit["qere_final_marks"] = final_marks(unit["qere"])
                unit["ketiv_marks"] = [
                    f"U+{ord(c):04X}" for c in unit["ketiv"] if unicodedata.combining(c)
                ]
            corpus.extend(units)
        assert corpus, "CLC main pages contain no ruby units"
        # Faithful positive controls from current NAEE main book pages, with only the fix removed.
        na_samples = []
        represented = set()
        for path in sorted((ROOT / "gh-pages/near-aleppo/edition").glob("*.html")):
            if "big-doc" in path.name or path.name == "index.html":
                continue
            content = path.read_text(encoding="utf-8")
            for index, match in enumerate(
                re.finditer(r'<ruby class="near-aleppo-kq".*?</ruby>', content, re.S)
            ):
                unit_html = match.group()
                annotation_match = re.search(r"<rt[^>]*>(.*?)</rt>", unit_html, re.S)
                if not annotation_match:
                    continue
                annotation = annotation_match[1]
                text = html.unescape(re.sub(r"<[^>]*>", "", annotation))
                marks = set(final_marks(text))
                if not marks.difference(represented) and not (
                    "Ruth" in path.name and "קָנִ֔יתָ" in text
                ):
                    continue
                represented.update(marks)
                na_samples.append(
                    {
                        "id": f"{path.stem}:{index}",
                        "source": path.relative_to(ROOT).as_posix(),
                        "html": unit_html,
                        "annotation": annotation,
                        "base": "",
                        "text": text,
                        "final_marks": sorted(marks),
                    }
                )
        assert na_samples, "no NAEE positive controls were found"
        (OUT / "corpus.json").write_text(
            json.dumps(
                {"clc": corpus, "na_positive_controls": na_samples},
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        for side, samples, css in (
            ("clc-qere", corpus, clc_css),
            ("clc-ketiv", corpus, clc_css),
            ("na-qere", na_samples, na_css),
        ):
            families = ["Taamey D WOFF2"]
            if args.comparison_font:
                families.append("Comparison Hebrew")
            for family in families:
                for size in args.sizes:
                    for batch_index in range(0, len(samples), 30):
                        batch = samples[batch_index : batch_index + 30]
                        review = review_html(
                            batch,
                            family,
                            size,
                            css,
                            side,
                            args.comparison_font,
                            (
                                current_clc_css
                                if side.startswith("clc")
                                else current_na_css
                            ),
                        )
                        stem = f"{side}-{family.split()[0]}-{size:g}-{batch_index}"
                        (OUT / f"{stem}.html").write_text(review, encoding="utf-8")
                        page.set_content(review)
                        page.evaluate("document.fonts.ready")
                        assert page.evaluate(
                            """() => [...document.querySelectorAll('.glyph')].every(e => {
                          const g=e.getBoundingClientRect(), c=e.parentElement.getBoundingClientRect();
                          return g.left>=c.left+10 && g.right<=c.right-10 && g.top>=c.top+20 && g.bottom<=c.bottom-10;
                        })"""
                        ), "comparison cell too small for a complete glyph raster"
                        fonts = page.evaluate(
                            "[...document.fonts].map(f=>({family:f.family,status:f.status}))"
                        )
                        assert any(
                            f["family"] == family and f["status"] == "loaded"
                            for f in fonts
                        ), fonts
                        raster = Image.open(io.BytesIO(page.screenshot(full_page=True)))
                        raster.save(OUT / f"{stem}.png")
                        for i, sample in enumerate(batch):
                            # Labels are outside this crop; only the visible glyph side remains.
                            control = raster.crop(
                                (
                                    CELL_WIDTH * len(VARIANTS),
                                    i * CELL_HEIGHT + 20,
                                    CELL_WIDTH * (len(VARIANTS) + 1),
                                    (i + 1) * CELL_HEIGHT,
                                )
                            )
                            for col, name in enumerate(VARIANTS):
                                candidate = raster.crop(
                                    (
                                        col * CELL_WIDTH,
                                        i * CELL_HEIGHT + 20,
                                        (col + 1) * CELL_WIDTH,
                                        (i + 1) * CELL_HEIGHT,
                                    )
                                )
                                result = compare(candidate, control)
                                all_results.append(
                                    {
                                        "id": sample["id"],
                                        "side": side,
                                        "font": family,
                                        "size": size,
                                        "variant": name,
                                        **result,
                                    }
                                )
                    summary = {
                        name: sum(
                            r["outlier_pixels"] > 0
                            for r in all_results
                            if r["side"] == side
                            and r["font"] == family
                            and r["size"] == size
                            and r["variant"] == name
                        )
                        for name in VARIANTS
                    }
                    print(
                        json.dumps(
                            {
                                "side": side,
                                "font": family,
                                "size": size,
                                "count": len(samples),
                                "discrepancies": summary,
                            }
                        ),
                        flush=True,
                    )
        report = {
            "head": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "baseline": baseline,
            "browser": browser.version,
            "platform": platform.platform(),
            "comparison_font": (
                str(args.comparison_font) if args.comparison_font else None
            ),
            "corpus_units": len(corpus),
            "qere_final_mark_units": sum(bool(c["qere_final_marks"]) for c in corpus),
            "ketiv_mark_units": sum(bool(c["ketiv_marks"]) for c in corpus),
            "na_control_units": len(na_samples),
            "na_final_mark_types": sorted(represented),
            "page_errors": errors,
            "results": all_results,
        }
        (OUT / "results.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        browser.close()
    print(
        json.dumps(
            {k: v for k, v in report.items() if k != "results"}, ensure_ascii=True
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
