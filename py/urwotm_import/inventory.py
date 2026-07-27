"""Phase 0 reports: what is actually in the four source documents.

Nothing here generates code. The point is to put every judgment call in front
of Ben before the emitter hard-codes an answer:

* ``class_inventory.md`` -- which ``.cN`` paragraph classes exist, how often,
  and what role each plays. Google emits no ``<h1>``/``<h2>``/``<h3>``, so a
  mis-read heading silently restructures a document.
* ``run_styles.md`` -- the character-level styling (italic, bold, colored,
  superscript, struck-through) with samples. This is where the real ambiguity
  lives: Google italic is three different things in Ben's prose.
* ``link_inventory.md`` -- every link, unwrapped from Google's redirect.
* ``dollar_candidates.md`` -- what ``dollar_sub`` will demand, in buckets.
* ``structure.md`` -- block counts against the plan's expected numbers.

All reports are written to files, never printed: they quote Hebrew, and on
Windows a redirected stdout encodes with cp1252.
"""

import collections

from urwotm_import import dollarize
from urwotm_import import fetch
from urwotm_import import gdoc_css
from urwotm_import import gdoc_parse
from urwotm_import import normalize
from urwotm_import import parts

_SAMPLE_COUNT = 3
_SAMPLE_CHARS = 90


def run(part_nums=None):
    part_nums = part_nums or parts.PART_NUMS
    docs = {}
    for part, html in sorted(fetch.read_all(part_nums).items()):
        docs[part] = gdoc_parse.parse_html(part, html)
    out_dir = parts.report_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    written = [
        _write(out_dir / "structure.md", _structure_report(docs)),
        _write(out_dir / "class_inventory.md", _class_report(docs)),
        _write(out_dir / "run_styles.md", _run_style_report(docs)),
        _write(out_dir / "link_inventory.md", _link_report(docs)),
        _write(out_dir / "dollar_candidates.md", _dollar_report(docs)),
    ]
    for path in written:
        print(f"wrote {path}")


###########################################################


def _structure_report(docs):
    lines = ["# Structure: parsed blocks vs. the plan's expected counts", ""]
    lines.append("| part | title | p | li | table | img | blank | other |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for part, doc in sorted(docs.items()):
        counts = collections.Counter(_all_kinds(doc))
        n_li = sum(len(b["items"]) for b in doc.blocks_of_kind("list"))
        # The expected numbers are raw <p> tag counts, which include the
        # title, the subtitle, the blank spacers, the paragraphs that hold
        # images, and the paragraphs inside Part 2's table cells.
        n_p_equiv = (
            counts["para"]
            + counts["title"]
            + counts["subtitle"]
            + counts["blank"]
            + counts["img"]
        )
        exp = parts.EXPECTED_COUNTS[part]
        lines.append(
            f"| {part} | {doc.gdoc_title} | {n_p_equiv} (exp {exp[0]}) | "
            f"{n_li} (exp {exp[1]}) | {counts['table']} (exp {exp[2]}) | "
            f"{counts['img']} (exp {exp[3]}) | {counts['blank']} | "
            f"{counts['unknown']} |"
        )
    lines.append("")
    lines.append("## List nesting (recovered from margin-left / 36pt)")
    lines.append("")
    for part, doc in sorted(docs.items()):
        lists = doc.blocks_of_kind("list")
        lines.append(f"### Part {part}: {len(lists)} list block(s)")
        for i, block in enumerate(lists):
            levels = [item["level"] for item in block["items"]]
            lines.append(f"- list {i}: {len(levels)} items, levels {levels}")
            for item in block["items"]:
                text = normalize.norm_block(gdoc_parse.runs_text(item["runs"]))
                lines.append(f"    - L{item['level']}: {_clip(text)}")
        lines.append("")
    return lines


def _class_report(docs):
    lines = [
        "# Paragraph-role inventory",
        "",
        "Google emits no `<h1>`/`<h2>`/`<h3>`: every block is a "
        "`<p class=cN>`, so heading level has to be read off the CSS. "
        "A *heading* would show up as a class with `page-break-after: avoid` "
        "and a font size above the 16pt body size.",
        "",
        "Rows are keyed on the **resolved properties**, not on the `.cN` "
        "name -- Google reshuffles those names on every re-render of a "
        "published doc, so a class name is not an identity.",
        "",
    ]
    for part, doc in sorted(docs.items()):
        lines.append(f"## Part {part} -- {doc.gdoc_title}")
        lines.append("")
        lines.extend(_heading_finding(doc))
        lines.append("")
        lines.append("| kind | n | text-align | margin-left | height | pt | samples |")
        lines.append("|---|---|---|---|---|---|---|")
        groups = _para_role_groups(doc)
        for key, (texts, sizes) in sorted(
            groups.items(), key=lambda kv: -len(kv[1][1])
        ):
            kind, align, margin, height = key
            pts = sorted({s for s in sizes if s})
            samples = " / ".join(_clip(t) for t in texts[:_SAMPLE_COUNT])
            lines.append(
                f"| {kind} | {sizes.count(None)} | {align} | {margin} | "
                f"{height} | {', '.join(str(p) for p in pts)} | {samples} |"
            )
        lines.append("")
    return lines


def _run_style_report(docs):
    lines = [
        "# Character-run styling",
        "",
        "Google **bold** maps to `author.emphasis`. Google *italic* is "
        "three-ways ambiguous -- a romanized accent name (a `$token`, which "
        "supplies its own italic), a book title (`author.book_title`), or "
        "genuine stress (`author.emphasis`, which renders bold). Every "
        "distinct italic run is listed so the resolution can be checked.",
        "",
    ]
    for part, doc in sorted(docs.items()):
        lines.append(f"## Part {part}")
        lines.append("")
        by_style = collections.defaultdict(collections.Counter)
        for runs in _all_runs(doc):
            for run in runs:
                key = _style_key(run)
                if key:
                    by_style[key][run["text"].strip()] += 1
        for key, texts in sorted(by_style.items()):
            total = sum(texts.values())
            lines.append(f"### {key} -- {total} run(s), {len(texts)} distinct")
            lines.append("")
            for text, count in texts.most_common():
                extra = ""
                if "italic" in key:
                    dkey = dollarize.key_for_rendered(text)
                    extra = f" -> `{dkey}`" if dkey else " -> **no $key**"
                lines.append(f"- {count}x `{text}`{extra}")
            lines.append("")
    return lines


def _link_report(docs):
    lines = [
        "# Link inventory",
        "",
        "Published docs wrap every external link as "
        "`https://www.google.com/url?q=<real>&sa=D&...`; the target column "
        "is the unwrapped `q` parameter.",
        "",
    ]
    for part, doc in sorted(docs.items()):
        lines.append(f"## Part {part}")
        lines.append("")
        seen = collections.Counter()
        texts = collections.defaultdict(list)
        for runs in _all_runs(doc):
            for run in runs:
                if run["href"]:
                    seen[run["href"]] += 1
                    texts[run["href"]].append(run["text"].strip())
        if not seen:
            lines.append("(none)")
            lines.append("")
            continue
        lines.append("| n | anchor text | target |")
        lines.append("|---|---|---|")
        for href, count in seen.most_common():
            anchor = " / ".join(sorted(set(t for t in texts[href] if t)))
            lines.append(f"| {count} | {_clip(anchor)} | {href} |")
        lines.append("")
    return lines


def _dollar_report(docs):
    lines = [
        "# `$`-substitution candidates",
        "",
        "`dollar_sub_g._check_no_undollared` *raises* if a dispatch key's "
        "undollared form appears bare in prose, so buckets 1-3 are not "
        "optional: something has to be done about every hit or the build "
        "fails. Bucket 4 needs an `author.py` change and is only reported.",
        "",
    ]
    for part, doc in sorted(docs.items()):
        lines.append(f"## Part {part}")
        lines.append("")
        buckets = {
            "auto": collections.defaultdict(list),
            "ambiguous": collections.defaultdict(list),
            "retext": collections.defaultdict(list),
        }
        missing_cap = collections.defaultdict(list)
        for text in _all_block_texts(doc):
            for key, start, end in dollarize.lint_hits(text):
                bucket = dollarize.classify(key, text[start:end])
                buckets[bucket][key].append(_context(text, start, end))
            for word, start, end in _capitalized_words(text):
                cap_key = dollarize.cap_key_missing(word)
                if cap_key:
                    missing_cap[cap_key].append(_context(text, start, end))
        lines.append("### Bucket 1 -- auto: renders as the same text, no collision")
        lines.append("")
        auto = buckets["auto"]
        lines.extend(
            f"- {len(auto[k])}x `{k}`"
            for k in sorted(auto, key=lambda k: -len(auto[k]))
        )
        if not auto:
            lines.append("(none)")
        lines.append("")
        lines.append("### Bucket 2 -- ambiguous (collides with English) **REVIEW**")
        lines.append("")
        lines.extend(_bucket_detail(buckets["ambiguous"]))
        lines.append("")
        lines.append(
            "### Bucket 3 -- key renders as DIFFERENT text **REVIEW** "
            "(substituting rewrites the prose)"
        )
        lines.append("")
        lines.extend(_bucket_detail(buckets["retext"], show_rendered=True))
        lines.append("")
        lines.append("### Bucket 4 -- capitalized, no cap key in `author.py`")
        lines.append("")
        lines.extend(_bucket_detail(missing_cap))
        lines.append("")
    return lines


def _bucket_detail(bucket, show_rendered=False, limit=6):
    if not bucket:
        return ["(none)"]
    lines = []
    for key in sorted(bucket):
        hits = bucket[key]
        suffix = ""
        if show_rendered:
            suffix = f" -- renders as `{dollarize.rendered_text(key)}`"
        lines.append(f"#### `{key}` -- {len(hits)} hit(s){suffix}")
        lines.extend(f"  - {c}" for c in hits[:limit])
        if len(hits) > limit:
            lines.append(f"  - ...and {len(hits) - limit} more")
    return lines


###########################################################


def _para_role_groups(doc):
    """{role signature: ([sample texts], [run font sizes])} over every block.

    Keyed on the *resolved* properties, never on the ``.cN`` name: Google
    reshuffles those names on every re-render of a published document (see
    ``fetch.py``), so a name is not an identity.
    """
    groups = collections.defaultdict(lambda: ([], []))
    for block in doc.blocks:
        class_attr = block.get("class")
        if class_attr is None:
            continue
        props = doc.sheet.para_props(class_attr)
        key = (
            block["kind"],
            props.get("text-align", ""),
            props.get("margin-left", ""),
            props.get("height", ""),
        )
        texts, sizes = groups[key]
        text = gdoc_parse.block_text(block) or block.get("src", "")
        if text:
            texts.append(text)
        for run in block.get("runs", ()):
            if run["size_pt"]:
                sizes.append(run["size_pt"])
        sizes.append(None)
    return groups


def _heading_finding(doc):
    """Report every heading-like class, and which blocks actually use one.

    Google marks its title, subtitle and h1-h6 styles alike with
    ``page-break-after: avoid``. A class carrying that but used by a block
    that is neither the title nor the subtitle would be a real section
    heading.
    """
    heading_classes = {
        name
        for name in doc.sheet.class_names()
        if doc.sheet.props_of_class(name).get("page-break-after") == "avoid"
    }
    used_by = collections.defaultdict(list)
    for block in doc.blocks:
        names = set((block.get("class") or "").split())
        if names & heading_classes:
            used_by[block["kind"]].append(gdoc_parse.block_text(block))
    lines = [
        f"{len(heading_classes)} heading-like class(es) "
        "(`page-break-after: avoid`), used by:",
        "",
    ]
    for kind in sorted(used_by):
        lines.append(f"- **{kind}** x{len(used_by[kind])}: {_clip(used_by[kind][0])}")
    extra = set(used_by) - {"title", "subtitle"}
    if extra:
        lines.append("")
        lines.append(f"**Real section heading(s) found: {sorted(extra)}**")
    else:
        lines.append("")
        lines.append(
            "**No section heading anywhere in this document** -- only the "
            "title and the subtitle."
        )
    return lines


def _font_desc(sheet, class_attr):
    props = sheet.char_props(class_attr)
    size = gdoc_css.font_size_pt(props)
    return f"{size}pt" if size else ""


def _style_key(run):
    bits = []
    if run["bold"]:
        bits.append("bold")
    if run["italic"]:
        bits.append("italic")
    if run["sup"]:
        bits.append("sup")
    if run["strike"]:
        bits.append("strike")
    if run["color"]:
        bits.append(f"color={run['color']}")
    if run["size_pt"] and run["size_pt"] != 16.0:
        bits.append(f"{run['size_pt']}pt")
    return "+".join(bits)


def _all_kinds(doc):
    """Every block's kind, including the ones nested in table cells."""
    for block in doc.blocks:
        yield block["kind"]
        if block["kind"] == "table":
            for row in block["rows"]:
                for cell in row:
                    for cell_block in cell:
                        yield cell_block["kind"]


def _all_runs(doc):
    for block in doc.blocks:
        if "runs" in block:
            yield block["runs"]
        if block["kind"] == "list":
            for item in block["items"]:
                yield item["runs"]
        if block["kind"] == "table":
            for row in block["rows"]:
                for cell in row:
                    for cell_block in cell:
                        if "runs" in cell_block:
                            yield cell_block["runs"]


def _all_block_texts(doc):
    for runs in _all_runs(doc):
        text = normalize.norm_block(gdoc_parse.runs_text(runs))
        if text:
            yield text


def _capitalized_words(text):
    word = ""
    start = 0
    for i, ch in enumerate(text + " "):
        if ch.isalpha():
            if not word:
                start = i
            word += ch
            continue
        if word and word[0].isupper() and len(word) > 1 and word[1:].islower():
            yield word, start, i
        word = ""


def _context(text, start, end, width=40):
    lo = max(0, start - width)
    hi = min(len(text), end + width)
    prefix = "..." if lo > 0 else ""
    suffix = "..." if hi < len(text) else ""
    return f"`{prefix}{text[lo:start]}[[{text[start:end]}]]{text[end:hi]}{suffix}`"


def _clip(text, limit=_SAMPLE_CHARS):
    text = (text or "").replace("|", "\\|")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _write(path, lines):
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path
