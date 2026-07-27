"""Turn a parsed Google Doc into the source of an authored Python module.

This is one-shot tooling -- the plan's Phase 8 deletes it once the emitted
modules are the source of truth -- but the *output* is not throwaway: it is
what Ben will read and hand-edit for years. So it comes out shaped like the
hand-authored modules beside it, ``rocc_1_on_the_provenance_of_ctr.py`` for
the skeleton and long-body constant style, ``tsinnorit_and_the_xxd_in_bhs.py``
for images and mixed-run paragraphs.

Three things here are less obvious than they look.

**A literal ``$`` in the prose is a live grenade.** ``dollar_sub_g`` splits
every string on ``[$][a-zA-Z0-9_]+`` and looks the result up in the dispatch,
so Part 1's "recently sold for $38.1 million" would raise ``KeyError: '$38'``.
Each literal ``$`` therefore becomes its own ``mb_html.raw_html("$")`` piece,
which ``dollar_sub`` skips and which emits a bare ``$`` with no wrapper.

**Whitespace has to leave the styled runs.** Google writes the space *inside*
the italic span (``[italic]'qadma '``), which would emit ``$qadma`` followed
by nothing. Edge whitespace is pushed out to plain neighbours before anything
else looks at a run.

**Adjacent strings get re-merged downstream.** ``mb_html.htel_mk`` runs
``shrink`` before its space asserts, so a paragraph split across several
string literals is checked as one string: a fragment may not end with a space
when the next begins with one, or the double-space assert fires. Wrapping
therefore always puts the space at the *start* of the continuation.
"""

import re
import textwrap

from urwotm_import import dollarize
from urwotm_import import gdoc_parse
from urwotm_import import img_names
from urwotm_import import normalize

# The house body is 40em at 14pt (560pt); Google's published page is 468pt
# (624px) wide. An image displayed full-width in the Doc is therefore
# full-width here, and one displayed half-width is half-width here.
EM_PER_DISP_PX = 40.0 / 624.0

# Width for wrapped string literals. A list element sits at four spaces of
# indent and carries a quote pair and a comma, so 78 keeps black's 88.
_WRAP_IN_LIST = 78
_WRAP_AT_MARGIN = 84

# Google's body size in these documents. Only 24pt and 26pt mean anything,
# and Ben's Phase 0 decision is that house style beats Google's type scale,
# so nothing reproduces a point size; the sizes are only reported.
_BODY_PT = 16.0

_SERIES_LINK_RE = re.compile(r"docs\.google\.com/document/d/[^/]+/edit")

# HAND-AUTHORED, from the Phase 2 review of every distinct italic run.
# Italic runs that are book titles rather than romanized terms.
BOOK_TITLES = frozenset(
    (
        "Keter Yerushalayim",
        "Keter Y",
        "Masorah Thesaurus",
        "A Reader’s Hebrew Bible",
    )
)
# Italic runs that are neither a keyed term nor a book title. Ben's Phase 2
# decision is that these reuse the "romanized" class rather than earning a
# class of their own -- including the one case where the italic is a quoted
# author's rather than Ben's ("one", inside a Wickes quotation), since inside
# a quotation preserving the look beats routing it through author.emphasis,
# which renders bold.
PLAIN_ITALIC = frozenset(
    (
        "mater lectionis",  # Latin phrase, not a romanized Hebrew term
        "jèraḥ",  # BHS's own Latin spelling, quoted as BHS spells it
        "hiriq",  # the source spells it without the x that $xiriq has
        "hafukh",  # a key would collide with mp_cmn_rows_core.py
        "k",  # a variable in the masorah-note formula
        "n",  # likewise
        "one",  # Wickes's italic, for stress, inside a quotation
    )
)


class Notes:
    """What the emitter could not decide on its own, for the review report."""

    def __init__(self, part):
        self.part = part
        self.todo_italic = []
        self.ambiguous = []
        self.retext = []
        self.cap_missing = []
        self.colors = []
        self.strikes = []
        self.sups = []
        self.big_type = []
        self.torn = []


def emit_module(doc, refs) -> tuple[str, Notes]:
    """The full Python source of one part's authored module."""
    ctx = _Ctx(doc.part, refs)
    body = _body_exprs(doc, ctx)
    return _assemble(ctx, body), ctx.notes


def module_stem(part: int) -> str:
    from author_misc import urwotm_common

    return urwotm_common.FNAMES[part][: -len(".html")]


def report_lines(notes: "Notes"):
    """What a human still has to decide about this part."""
    out = [
        f"# Part {notes.part}: what the emitter could not decide",
        "",
        "Block numbers are indices into the parsed block stream, and match "
        "the `_PARA_nnn` / `_LIST_nnn` constant names in the emitted module.",
        "",
    ]
    out += _report_section(
        "Italic runs with no `$` key -- `urwotm_common.TODO_ITALIC`",
        "Each is a book title (`author.book_title`), a term that wants a new "
        "`author.py` key, or genuine stress (`author.emphasis`, which renders "
        "**bold**, not italic). The page renders meanwhile.",
        [f"`{text}` (block {index})" for index, text in _tally(notes.todo_italic)],
    )
    out += _report_section(
        "Capitalized, with no capitalized key in `author.py`",
        "A sentence-initial form whose lowercase key exists but whose "
        "capitalized twin does not. Adding one is a Phase 3 `author.py` change.",
        [f"`{text}` wants `{key}` (block {i})" for i, text, key in notes.cap_missing],
    )
    out += _report_section(
        "Substituted, but the key collides with ordinary English -- REVIEW",
        "`dollar_sub` would raise on the bare word, so something had to be "
        "done; it was substituted. Check that each really is the Hebrew "
        "letter or accent name and not the English word.",
        [f"`{key}`: {context}" for _, key, context in notes.ambiguous],
    )
    out += _report_section(
        "Key renders as DIFFERENT text -- NOT substituted",
        "Substituting would rewrite the prose. These need a new key.",
        [f"`{key}`: {context}" for _, key, context in notes.retext],
    )
    out += _report_section(
        "Colored text",
        "Emitted as `author.span_color`. Color is content in this series "
        '(Part 4 sets red "Galgal" against green "Galfukh").',
        [f"{color} `{text}` (block {i})" for i, text, color in notes.colors],
    )
    out += _report_section(
        "Struck-through text",
        "Emitted as an inline `text-decoration: line-through` span; "
        "`mb_html` has no helper.",
        [f"`{text}` (block {i})" for i, text in _tally(notes.strikes)],
    )
    out += _report_section(
        "Superscripts",
        "Emitted as `mb_html.sup`.",
        [f"`{text}` (block {i})" for i, text in _tally(notes.sups)],
    )
    out += _report_section(
        "Words torn across runs, repaired by the second dollarization pass",
        "Google split a word between two runs and neither half matched on its "
        "own. Repaired, but each one means a run boundary upstream is still "
        "tearing words apart.",
        [f"`{key}`: {context}" for _, key, context in notes.torn],
    )
    out += _report_section(
        "Non-body type sizes, deliberately NOT reproduced",
        "House style beats Google's type scale (Ben, mid-Phase-0). Listed so "
        "that a size carrying real meaning can be spotted.",
        [f"{size}pt `{text[:60]}`" for size, text in notes.big_type],
    )
    return out


def _report_section(title, blurb, rows):
    out = [f"## {title}", ""]
    if not rows:
        return out + ["(none)", ""]
    out += [blurb, ""]
    out += [f"- {row}" for row in rows]
    out += [""]
    return out


def _tally(pairs):
    """Collapse repeats, keeping the first block each was seen in."""
    seen = {}
    for index, text in pairs:
        seen.setdefault(text, index)
    return [(index, text) for text, index in seen.items()]


###########################################################


class _Ctx:
    def __init__(self, part, refs):
        self.part = part
        self.notes = Notes(part)
        self.consts = []  # (name, source) in emission order
        self.urls = {}  # url -> const name
        self.url_counts = {}
        self.imgs = [r for r in refs if r["part"] == part]
        self.img_index = 0
        self.uses_mb_html = False

    def add_const(self, name, source):
        self.consts.append((name, source))
        return name

    def url_const(self, url):
        if url in self.urls:
            return self.urls[url]
        slug = _url_slug(url)
        self.url_counts[slug] = self.url_counts.get(slug, 0) + 1
        name = f"_URL_{slug}_{self.url_counts[slug]}"
        self.urls[url] = name
        return name

    def next_img(self):
        ref = self.imgs[self.img_index]
        self.img_index += 1
        return ref


def _assemble(ctx, body):
    imports = ["from mb_author import author", "from author_misc import urwotm_common"]
    if ctx.uses_mb_html:
        imports.insert(0, "from mb_misc import mb_html")
    body_lines = "\n".join(f"        {expr}," for expr in body)
    url_lines = "".join(
        f"{name} = {_url_literal(url)}\n" for url, name in ctx.urls.items()
    )
    const_lines = "\n".join(f"{name} = {source}" for name, source in ctx.consts)
    return f'''"""Exports gen_html_file.

Ported from the published Google Doc of the same title. The prose is
reproduced verbatim; the only deliberate changes are the ``$`` keys that
``dollar_sub`` requires, and the three intra-series links, which now point at
the sibling pages rather than at the Google Docs.
"""

{chr(10).join(imports)}


def anchor():
    return urwotm_common.anchor_part({ctx.part})


def gen_html_file(tdm_ch):
    cbody = [
{body_lines}
    ]
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, cbody)


_PART = {ctx.part}
_TITLE = urwotm_common.plain_title(_PART)
_FNAME = urwotm_common.FNAMES[_PART]
{"" if not url_lines else chr(10) + url_lines}
{const_lines}
'''


def _body_exprs(doc, ctx):
    out = []
    blocks = [b for b in doc.blocks if b["kind"] != "blank"]
    i = 0
    while i < len(blocks):
        block = blocks[i]
        kind = block["kind"]
        if kind == "list":
            end = _end_of_list_run(blocks, i)
            out.append(_list_expr(blocks[i:end], ctx, i))
            i = end
            continue
        out.append(_block_expr(block, ctx, i))
        i += 1
    return [expr for expr in out if expr is not None]


def _block_expr(block, ctx, index):
    kind = block["kind"]
    if kind == "title":
        return "author.heading_level_1(urwotm_common.heading_1(_PART))"
    if kind == "subtitle":
        return "author.heading_level_2(urwotm_common.heading_2(_PART))"
    if kind == "img":
        return _img_expr(ctx)
    if kind == "para":
        return _para_expr(block, ctx, index)
    if kind == "table":
        return _table_expr(block, ctx, index)
    raise AssertionError(f"unhandled block kind {kind!r}")


def _table_expr(block, ctx, index):
    """Google writes ``<td><p class="cN">``; ``std_table`` takes contents.

    Each cell becomes the list of its own block expressions, so a cell
    holding an image emits the same ``para_for_img`` a top-level image
    would. The blank spacer paragraphs ``gdoc_parse`` keeps so the structural
    tripwire reconciles are dropped here.
    """
    rows = []
    for r, row in enumerate(block["rows"]):
        cells = []
        for c, cell in enumerate(row):
            blocks = [b for b in cell if b["kind"] != "blank"]
            exprs = [
                _block_expr(b, ctx, f"{index:03d}_r{r}c{c}_{k}")
                for k, b in enumerate(blocks)
            ]
            cells.append(exprs)
        rows.append(cells)
    name = ctx.add_const(_const_name("_TABLE", index), _table_source(rows))
    return f"author.std_table({name})"


def _table_source(rows, indent=0):
    pad = "    " * (indent + 1)
    out = ["["]
    for cells in rows:
        out.append(f"{pad}[")
        for exprs in cells:
            if len(exprs) == 1:
                out.append(f"{pad}    {exprs[0]},")
                continue
            out.append(f"{pad}    [")
            for expr in exprs:
                out.append(f"{pad}        {expr},")
            out.append(f"{pad}    ],")
        out.append(f"{pad}],")
    out.append("    " * indent + "]")
    return "\n".join(out)


def _const_name(prefix, index):
    """Constant names, for both top-level blocks and table cells.

    A table cell cannot reuse its table's index: Part 2's two tables hold
    four paragraphs between them, and naming all four after the table made
    each assignment clobber the last, so every cell rendered the same text.
    """
    if isinstance(index, str):
        return f"{prefix}_{index}"
    return f"{prefix}_{index:03d}"


def _para_expr(block, ctx, index):
    _note_type_size(block, ctx)
    pieces = _strip_edge_pieces(_pieces_of_runs(block["runs"], ctx, index))
    text = normalize.norm_block(gdoc_parse.runs_text(block["runs"]))
    if _is_mono(block):
        ctx.uses_mb_html = True
        name = ctx.add_const(_const_name("_CODE", index), _const_source(pieces, ctx))
        return f'author.para(mb_html.code({name}), {{"class": "center"}})'
    if block["align"] == "center" and normalize.is_all_hebrew(text):
        name = ctx.add_const(_const_name("_HBO", index), _const_source(pieces, ctx))
        return f"author.para_hbo({name})"
    if _is_blockquote(block):
        name = ctx.add_const(_const_name("_QUOTE", index), _const_source(pieces, ctx))
        return f"author.blockquote({name})"
    name = ctx.add_const(_const_name("_PARA", index), _const_source(pieces, ctx))
    if block["align"] == "center":
        return f'author.para({name}, {{"class": "center"}})'
    return f"author.para({name})"


def _img_expr(ctx):
    ref = ctx.next_img()
    name = img_names.descriptive(ref["stem"], ref["file"])
    width_em = round((ref["disp_w"] or 0) * EM_PER_DISP_PX, 1)
    path = _q(f"urwotm/{name}")
    if not width_em:
        return f"author.para_for_img({path})"
    return f"author.para_for_img(\n            {path}, width_em={width_em}\n        )"


def _list_expr(list_blocks, ctx, index):
    # Checked before the items are built: converting them would mint URL
    # constants for the three Google Doc links that are about to be discarded.
    if _is_series_list(list_blocks):
        return "author.unordered_list(urwotm_common.other_parts(_PART))"
    items = []
    for block in list_blocks:
        for item in block["items"]:
            pieces = _strip_edge_pieces(_pieces_of_runs(item["runs"], ctx, index))
            items.append((item["level"], pieces))
    tree, _ = _nest(items, 0, _min_level(items))
    name = ctx.add_const(_const_name("_LIST", index), _items_source(tree, ctx))
    return f"author.unordered_list({name})"


def _end_of_list_run(blocks, start):
    """Adjacent ``<ul>`` siblings are one nested list, not several.

    Google flattens nesting into sibling lists distinguished only by
    ``margin-left``, so a list and its sublist arrive as two blocks in a row.
    """
    end = start
    while end < len(blocks) and blocks[end]["kind"] == "list":
        end += 1
    return end


def _min_level(items):
    return min(level for level, _ in items) if items else 0


def _nest(items, pos, level):
    """Build one level of the list tree, returning (nodes, next position)."""
    nodes = []
    while pos < len(items):
        item_level, pieces = items[pos]
        if item_level < level:
            break
        if item_level > level:
            children, pos = _nest(items, pos, item_level)
            if nodes:
                nodes[-1] = (nodes[-1][0], children)
            continue
        nodes.append((pieces, None))
        pos += 1
    return nodes, pos


def _items_source(nodes, ctx, indent=1):
    pad = "    " * indent
    out = ["["]
    for pieces, children in nodes:
        if children is None:
            out.append(f"{pad}{_pieces_source(pieces, ctx, indent)},")
            continue
        out.append(f"{pad}[")
        out.append(f"{pad}    {_pieces_source(pieces, ctx, indent + 1)},")
        sub = _items_source(children, ctx, indent + 2)
        out.append(f"{pad}    author.unordered_list({sub}),")
        out.append(f"{pad}],")
    out.append("    " * (indent - 1) + "]")
    return "\n".join(out)


def _is_series_list(list_blocks):
    """The three links to the other parts that open every document."""
    hrefs = [
        run["href"]
        for block in list_blocks
        for item in block["items"]
        for run in item["runs"]
    ]
    return len(hrefs) == 3 and all(h and _SERIES_LINK_RE.search(h) for h in hrefs)


###########################################################
# Runs to pieces. A piece is ("s", text) or ("e", python_expr).


def _pieces_of_runs(runs, ctx, index):
    pieces = []
    for run in _shed_edge_space(runs):
        pieces.extend(_pieces_of_run(run, ctx, index))
    return _dollarize_leftovers(_merge_strings(pieces), ctx, index)


def _shed_edge_space(runs):
    """Move leading/trailing whitespace out of every styled run.

    ``[italic]'qadma '`` has to become ``[italic]'qadma'`` plus a plain space,
    or the space ends up inside the ``<span class="romanized">`` and the
    ``$`` key it becomes swallows it.
    """
    out = []
    for run in runs:
        text = run["text"]
        if not text.strip():
            # A styled run holding nothing but a space is a Google artifact,
            # not italic content; keeping its styling emits an italic space.
            out.append({**run, **_NO_STYLE})
            continue
        if not _is_styled(run):
            out.append(run)
            continue
        lead = text[: len(text) - len(text.lstrip())]
        trail = text[len(text.rstrip()) :]
        if lead:
            out.append({**run, **_NO_STYLE, "text": lead})
        out.append({**run, "text": text.strip()})
        if trail:
            out.append({**run, **_NO_STYLE, "text": trail})
    return out


_NO_STYLE = {
    "bold": False,
    "italic": False,
    "sup": False,
    "strike": False,
    "mono": False,
    "color": None,
}


def _is_styled(run):
    return any(run[k] for k in ("bold", "italic", "sup", "strike", "color"))


def _pieces_of_run(run, ctx, index):
    text = run["text"]
    pieces = _base_pieces(run, text, ctx, index)
    if run["strike"]:
        # mb_html has no strikethrough helper; Part 2's 23 struck-through "q"
        # runs are content, not decoration, so they get an inline style.
        ctx.notes.strikes.append((index, text))
        ctx.uses_mb_html = True
        style = ', {"style": "text-decoration: line-through"}'
        pieces = [("e", _wrap(pieces, ctx, "mb_html.span", style))]
    if run["sup"]:
        ctx.notes.sups.append((index, text))
        ctx.uses_mb_html = True
        pieces = [("e", _wrap(pieces, ctx, "mb_html.sup"))]
    if run["color"]:
        ctx.notes.colors.append((index, text, run["color"]))
        pieces = [
            ("e", _wrap(pieces, ctx, "author.span_color", f", {_q(run['color'])}"))
        ]
    if run["href"]:
        const = ctx.url_const(run["href"])
        pieces = [("e", _wrap(pieces, ctx, "author.anc_h", f", {const}"))]
    return pieces


def _base_pieces(run, text, ctx, index):
    if run["italic"]:
        return _italic_pieces(text, ctx, index)
    if run["bold"]:
        return [("e", f"author.emphasis({_q(text)})")]
    return _plain_pieces(text, ctx, index)


def _italic_pieces(text, ctx, index):
    """Resolve one italic run, or leave it flagged for review."""
    key = dollarize.key_for_rendered(text)
    if key:
        return [("s", key)]
    if text in BOOK_TITLES:
        return [("e", f"author.book_title({_q(text)})")]
    if text in PLAIN_ITALIC:
        return [("e", f"urwotm_common.romanized({_q(text)})")]
    keys = _keys_for_each_word(text)
    if keys:
        # "mem qadma" is two keyed terms in one italic span; separate spans
        # render identically to one, so this needs no new machinery.
        return [("s", " ".join(keys))]
    word, punctuation = _split_trailing_punctuation(text)
    if punctuation:
        # Google sometimes pulls the closing quote into the italic run
        # (Part 4's `Galfukh”`). Resolving the word and leaving the mark
        # outside changes no text, only which characters are italicized.
        inner = _italic_pieces(word, ctx, index)
        return inner + [("s", punctuation)]
    ctx.notes.todo_italic.append((index, text))
    missing = dollarize.cap_key_missing(text)
    if missing:
        ctx.notes.cap_missing.append((index, text, missing))
    return [("e", f"urwotm_common.TODO_ITALIC({_q(text)})")]


def _split_trailing_punctuation(text):
    """(word, trailing punctuation) -- but only if the word then resolves."""
    stripped = text.rstrip("”\"’'.,;:)]")
    tail = text[len(stripped) :]
    if not tail or not stripped:
        return text, ""
    if not _resolves(stripped):
        return text, ""
    return stripped, tail


def _resolves(text):
    if dollarize.key_for_rendered(text) or text in BOOK_TITLES:
        return True
    return text in PLAIN_ITALIC or bool(_keys_for_each_word(text))


def _keys_for_each_word(text):
    """Every word's own key, but only if *every* word has one.

    A phrase where one word is unkeyed ("ketiv velo qere") is a unit, not a
    run of terms, and must stay a single decision.
    """
    words = text.split()
    if len(words) < 2:
        return None
    keys = [dollarize.key_for_rendered(word) for word in words]
    return keys if all(keys) else None


def _plain_pieces(text, ctx, index):
    """Plain prose: split out any literal ``$``, then dollarize the rest.

    Splitting first, on the *source* text, keeps the two kinds of ``$``
    apart: the ones Ben wrote (Part 1's "$38.1 million") and the ones this
    function is about to introduce.
    """
    _note_dollar_hits(text, ctx, index)
    pieces = []
    for chunk in re.split(r"(\$)", text):
        if chunk == "":
            continue
        if chunk == "$":
            ctx.uses_mb_html = True
            pieces.append(("e", 'mb_html.raw_html("$")'))
            continue
        pieces.append(("s", dollarize.substitute(chunk)))
    return pieces


def _note_dollar_hits(text, ctx, index):
    for key, start, end in dollarize.lint_hits(text):
        bucket = dollarize.classify(key, text[start:end])
        context = normalize.norm_block(text[max(0, start - 40) : end + 40])
        if bucket == "ambiguous":
            ctx.notes.ambiguous.append((index, key, context))
        elif bucket == "retext":
            ctx.notes.retext.append((index, key, context))


def _wrap(pieces, ctx, func, extra=""):
    inner = _pieces_source(pieces, ctx, 1)
    return f"{func}({inner}{extra})"


def _dollarize_leftovers(pieces, ctx, index):
    """Dollarize against exactly what ``_check_no_undollared`` will see.

    That check runs on the *concatenation* of a call's top-level strings, so
    a key can survive per-piece substitution and still fail the build --
    which is what happened when Google split "BHS" into two runs and each
    half was dollarized alone. Doing one more pass over the joined text makes
    the emitter guarantee the same property the checker tests. Anything
    caught here means a run boundary upstream is still tearing words apart,
    so it is reported rather than silently fixed.
    """
    joined = "".join(value for kind, value in pieces if kind == "s")
    hits = dollarize.lint_hits(joined)
    if not hits:
        return pieces
    for key, start, end in hits:
        ctx.notes.torn.append((index, key, joined[max(0, start - 30) : end + 30]))
    return _resubstitute(pieces, hits)


def _resubstitute(pieces, hits):
    """Apply hits, expressed as offsets into the joined string, piece-wise."""
    out = []
    pos = 0
    pending = list(hits)
    for kind, value in pieces:
        if kind != "s":
            out.append((kind, value))
            continue
        end_pos = pos + len(value)
        chunk = []
        cursor = 0
        while pending and pending[0][1] >= pos and pending[0][2] <= end_pos:
            key, start, end = pending.pop(0)
            chunk.append(value[cursor : start - pos])
            chunk.append(key)
            cursor = end - pos
        chunk.append(value[cursor:])
        out.append((kind, "".join(chunk)))
        pos = end_pos
    return out


def _strip_edge_pieces(pieces):
    """Drop the block's own leading and trailing space.

    ``mb_html._do_space_asserts`` forbids either on the contents of an
    element, and Google leaves plenty of both -- Part 1's closing paragraph
    on Oak Tree and Faithlife ends with one.
    """
    out = [(kind, value) for kind, value in pieces]
    if out and out[0][0] == "s":
        out[0] = ("s", out[0][1].lstrip())
    if out and out[-1][0] == "s":
        out[-1] = ("s", out[-1][1].rstrip())
    return [(k, v) for k, v in out if v != ""]


def _merge_strings(pieces):
    out = []
    for kind, value in pieces:
        if kind == "s" and out and out[-1][0] == "s":
            out[-1] = ("s", out[-1][1] + value)
            continue
        out.append((kind, value))
    return [(k, v) for k, v in out if v != ""]


###########################################################
# Pieces to Python source.


def _const_source(pieces, ctx):
    if len(pieces) == 1 and pieces[0][0] == "s":
        return _long_string_source(pieces[0][1])
    return _pieces_source(pieces, ctx, 0)


def _pieces_source(pieces, ctx, indent):
    """A list literal, or a bare string when that is all there is."""
    if len(pieces) == 1 and pieces[0][0] == "s":
        text = pieces[0][1]
        if len(text) <= _WRAP_IN_LIST:
            return _q(text)
    if len(pieces) == 1 and pieces[0][0] == "e":
        return pieces[0][1]
    pad = "    " * (indent + 1)
    lines = ["["]
    for kind, value in pieces:
        if kind == "e":
            lines.append(f"{pad}{value},")
            continue
        for fragment in _wrap_text(value, _WRAP_IN_LIST):
            lines.append(f"{pad}{_q(fragment)},")
    lines.append("    " * indent + "]")
    return "\n".join(lines)


def _long_string_source(text):
    """A whole-paragraph string, in ``rocc_1``'s triple-quoted style."""
    if len(text) <= _WRAP_AT_MARGIN and '"""' not in text:
        return _q(text)
    filled = "\n".join(_wrap_text_hard(text, _WRAP_AT_MARGIN))
    return f'"""{filled}""".replace("\\n", " ")'


def _wrap_text(text, width):
    """Split text so that re-concatenation is exact.

    Every fragment after the first starts with the space that separated it
    from the one before, never ends with one -- ``shrink`` merges them back
    and ``_do_space_asserts`` would fire on a double space otherwise.
    """
    if len(text) <= width:
        return [text]
    lead = " " if text[:1] == " " else ""
    trail = " " if text[-1:] == " " else ""
    body = text.strip()
    out = []
    for i, line in enumerate(_wrap_text_hard(body, width - 1)):
        out.append((lead if i == 0 else " ") + line)
    # textwrap drops the trailing space, which is exactly the space that
    # separates this run from the styled one after it.
    out[-1] += trail
    return out


def _wrap_text_hard(text, width):
    """Wrap so that joining the lines with single spaces is exact.

    ``break_on_hyphens`` would split "southeast-to-northwest" and rejoining
    the halves with a space would silently rewrite the prose;
    ``break_long_words`` would do the same to a long URL.
    """
    lines = textwrap.wrap(
        text,
        width=width,
        break_on_hyphens=False,
        break_long_words=False,
    )
    return lines or [text]


def _q(text):
    body = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{body}"'


def _url_literal(url):
    if len(url) <= 70:
        return _q(url)
    parts = [url[i : i + 66] for i in range(0, len(url), 66)]
    joined = "\n    ".join(_q(p) for p in parts)
    return f"(\n    {joined}\n)"


def _url_slug(url):
    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
    return re.sub(r"[^A-Z0-9]+", "_", host.upper()).strip("_")


###########################################################


def _is_mono(block):
    runs = [r for r in block["runs"] if r["text"].strip()]
    return bool(runs) and all(r["mono"] for r in runs)


def _is_blockquote(block):
    return block.get("indented", False)


def _note_type_size(block, ctx):
    for run in block["runs"]:
        size = run["size_pt"]
        if size and abs(size - _BODY_PT) > 0.01 and run["text"].strip():
            ctx.notes.big_type.append((size, run["text"]))
