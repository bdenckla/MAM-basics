"""Helpers shared by the modules that build gh-pages/morphhb-corrections/index.html.

Written by Claude (Opus 5.5) on 2026-11-14 as an untracked scratch script, tracked since
2026-11-15, and revised on 2026-11-16 to Ben's decisions of that day.
morphhb_corrections_index, the page's generator, says in its docstring what the page holds;
this module holds its rules and the verb of Ben's decision 8 (RESOLVE).  F is the folder of the
report's tracked files, in/morphhb-corrections-2026-11-13/, and VERDICTS the file of the
verdicts that the page lists and counts.

The rules the helpers enforce, so that the sections cannot break them:

- Every Hebrew form is copied by script, never typed; it is put in MAM-normal mark order
  (mb_cmn.uni_denorm.give_std_mark_order) and checked so (has_std_mark_order).
- In prose, a pointed run of Hebrew is drawn in lang="hbo" (Taamey D at 140%, from the shared
  sheets) and an unpointed run in a <bdi> with no lang (hebrew-prose, rendered-prose.md,
  "Unpointed Hebrew keeps the surrounding font"), as israel_bible_review_index's
  isolate_hebrew does.
- A form in a table is a form lifted from a text and shown with the forms it is compared with,
  so it is drawn in lang="hbo" whether pointed or not (the same section's one exception).
- Forms compared with each other stand one above the other in one cell (Ben, 2026-10-14), each
  letter whose marks differ highlighted and each atom with no difference in gray, by
  israel_bible_review_index's form_html, whose classes this page's own stylesheet (STYLESHEET)
  draws; morphhb's "/" between morphemes is drawn but takes no part in the comparison, and
  MAM's HEBREW POINT QAMATS QATAN counts as HEBREW POINT QAMATS, which WLC has for it.  A table
  cell holding Hebrew is dir="rtl".
- A verse is named in plain text, linked nowhere.
"""

import html
import re

from author_misc import israel_bible_review_index as ib
from mb_cmn import paths
from mb_cmn import uni_denorm

# F, the report's tracked files; VERDICTS, the verdicts of 2026-11-16; and the page's folder.
F = paths.in_dir() / "morphhb-corrections-2026-11-13"
VERDICTS = paths.in_dir() / "morphhb-verdicts-2026-11-16" / "verdicts.json"
PAGE_DIR = paths.gh_pages_dir() / "morphhb-corrections"

# The verb for the second kind of place: "resolves", Ben's answer to decision 8 of 2026-11-16
# ("8A, resolves is good").  The page writes the verb only from here, and only in its defined
# sense, with "WLC" as its object; the lint fails on any other use of these forms, and on the
# noun.  verdicts.json's name for the verdict, "resolves", is data and stays if the verb changes.
RESOLVE = {
    "base": "resolve",
    "s": "resolves",
    "ing": "resolving",
    "ed": "resolved",
    "noun": "resolution",
}

MORPHHB_URL = "https://github.com/openscriptures/morphhb"
NBSP = "\N{NO-BREAK SPACE}"
MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
CGJ = "\N{COMBINING GRAPHEME JOINER}"
ZWJ = "\N{ZERO WIDTH JOINER}"
ZWNJ = "\N{ZERO WIDTH NON-JOINER}"
INVISIBLE = frozenset({CGJ, ZWJ, ZWNJ})
HEB_LETTER = re.compile("[\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}]")
# Any character of the Hebrew block or of its presentation forms: the page's lint requires each
# to stand inside a lang="hbo" element or a <bdi>.
HEB_ANY = re.compile("[\u0590-\u05ff\ufb1d-\ufb4f]")


class H(str):
    """Trusted HTML.  ht() and the element helpers pass an H through as it is and treat a
    plain str as prose (see prose)."""


# ---------------------------------------------------------------- Hebrew


def mnorm(s):
    """A form in MAM-normal mark order, checked."""
    out = uni_denorm.give_std_mark_order(s)
    assert uni_denorm.has_std_mark_order(out), ascii(s)
    return out


def letters(s):
    """The letters alone, final forms kept."""
    return "".join(HEB_LETTER.findall(s))


# What a form in a table of words is shown without: accents, meteg, paseq, sof pasuq, the
# extraordinary dots and the invisible marks.  Vowels, dagesh and mapiq, the shin and sin dots
# and rafeh stay, since an analysis can turn on any of them.
_NOT_IN_ANALYSIS_FORMS = re.compile(
    "["
    "\N{HEBREW ACCENT ETNAHTA}-\N{HEBREW MARK MASORA CIRCLE}"
    "\N{HEBREW POINT METEG}"
    "\N{HEBREW PUNCTUATION PASEQ}"
    "\N{HEBREW PUNCTUATION SOF PASUQ}"
    "\N{HEBREW MARK UPPER DOT}"
    "\N{HEBREW MARK LOWER DOT}"
    "\N{COMBINING GRAPHEME JOINER}"
    "\N{ZERO WIDTH JOINER}"
    "\N{ZERO WIDTH NON-JOINER}"
    "]"
)


def analysis_form(s):
    """A form as the tables of words show it: without the marks above, and without a maqaf
    after its last atom, which morphhb records apart from the word; morphhb's '/' kept; in
    MAM-normal order."""
    out = _NOT_IN_ANALYSIS_FORMS.sub("", s).strip()
    if out.endswith(MAQAF):
        out = out[: -len(MAQAF)]
    assert HEB_LETTER.search(out), ascii(s)
    return mnorm(out)


def is_pointed(s):
    return bool(ib.POINT_OR_ACCENT.search(s))


def _isolate(text):
    """text (escaped, holding no tags): each Hebrew run in MAM-normal order, a pointed run in
    lang="hbo" and an unpointed one in a bare <bdi>."""

    def wrap(m):
        run = mnorm(m.group(0))
        if is_pointed(run):
            return f'<span lang="hbo" dir="rtl">{run}</span>'
        return f"<bdi>{run}</bdi>"

    return ib.HEB_RUN.sub(wrap, text)


ABBREVIATIONS = {
    "MAM": ib.ABBREVIATIONS["MAM"],
    "WLC": ib.ABBREVIATIONS["WLC"],
    "UXLC": "the Unicode/XML Leningrad Codex",
}
_ABBREVIATION = re.compile(r"\b(" + "|".join(ABBREVIATIONS) + r")\b(?![-\w])")


def explain(s):
    """Each abbreviation outside tags in an <abbr> with its expansion, as the review explains
    its own on hover (the expansions shared with the review are the review's)."""
    parts = re.split(r"(<[^>]+>)", s)
    for k in range(0, len(parts), 2):
        parts[k] = _ABBREVIATION.sub(
            lambda m: f'<abbr title="{html.escape(ABBREVIATIONS[m.group(1)])}">'
            f"{m.group(1)}</abbr>",
            parts[k],
        )
    return "".join(parts)


# The marks' and letters' names as the house romanizes them (hebrew-prose, terminology.md:
# patax, xataf, xiriq, xolam and xet, where x stands for an h with a dot below; qubuts, shuruq,
# mapiq and rafeh), in prose whose data spell them otherwise.  A quotation keeps its own spelling
# (q, and commit's messages), and so does a Unicode name, which is in capitals.
_DOT_H = "\N{LATIN SMALL LETTER H WITH DOT BELOW}"
_ROMAN = {
    "patah": "pata" + _DOT_H,
    "hataf": _DOT_H + "ataf",
    "hiriq": _DOT_H + "iriq",
    "holam": _DOT_H + "olam",
    "het": _DOT_H + "et",
    "qibbuts": "qubuts",
    "shureq": "shuruq",
    "mappiq": "mapiq",
    "rafe": "rafeh",
}
_ROMAN_RX = re.compile(r"(?<!\w)(" + "|".join(_ROMAN) + r")(?!\w)", re.I)


def _romanize(s):
    def fix(m):
        word = m.group(1)
        if word.isupper():
            return word
        out = _ROMAN[word.lower()]
        return out[:1].upper() + out[1:] if word[:1].isupper() else out

    return _ROMAN_RX.sub(fix, s)


def prose(s, verbatim=False):
    """Plain English text, which may hold Hebrew copied by script, as HTML: escaped, each
    Hebrew run isolated as _isolate says, each abbreviation explained, and, unless verbatim
    (a quotation), the vowels' names romanized as the house does.  Never give it HTML.
    """
    assert isinstance(s, str) and not isinstance(s, H)
    if not verbatim:
        s = _romanize(s)
    return H(explain(_isolate(html.escape(s, quote=False))))


def ht(*parts, verbatim=False):
    """Join parts into one H: an H as it is, a plain str as prose (verbatim for a
    quotation), a list or tuple recursively, None as nothing."""
    out = []
    for p in parts:
        if p is None:
            continue
        if isinstance(p, H):
            out.append(p)
        elif isinstance(p, str):
            out.append(prose(p, verbatim))
        elif isinstance(p, (list, tuple)):
            out.append(ht(*p, verbatim=verbatim))
        else:
            raise TypeError(f"not a page part: {p!r}")
    return H("".join(out))


def heb(s):
    """One Hebrew form inline in prose, as prose would draw it, from a form copied by script."""
    assert HEB_LETTER.search(s), ascii(s)
    return prose(s)


# ---------------------------------------------------------------- forms in tables


def units(form):
    """A form as units: a letter with its marks (and any CGJ, ZWJ or ZWNJ among them), a maqaf,
    a space, morphhb's '/' or any other character.  Like israel_bible_review_index's units, but
    keeping the invisible marks on their letter, so that MAM's CGJ neither splits a cluster nor
    counts as a difference.
    """
    out = []
    for ch in form:
        if (
            (ib.is_mark(ch) or ch in INVISIBLE)
            and out
            and out[-1][0] not in " /" + MAQAF
        ):
            out[-1] += ch
        else:
            out.append(ch)
    return out


def unit_key(unit):
    return unit[0] + "".join(sorted(c for c in unit[1:] if c not in INVISIBLE))


# What the highlighting treats as the same mark: MAM has HEBREW POINT QAMATS QATAN for a qamats
# qatan, where WLC has HEBREW POINT QAMATS for both qamats vowels, so that difference of code
# point alone highlights nothing (the review of 2026-11-16, finding 8).
_SAME_FOR_HIGHLIGHT = str.maketrans(
    {"\N{HEBREW POINT QAMATS QATAN}": "\N{HEBREW POINT QAMATS}"}
)


def highlight_key(unit):
    """unit_key, with the marks that the highlighting treats as the same made one."""
    return unit_key(unit.translate(_SAME_FOR_HIGHLIGHT))


def hot_units(forms_units):
    """As israel_bible_review_index's hot_units, with highlight_key above: for each form, the
    indices of its units involved in a difference from any other form, the forms aligned on
    their base characters.  morphhb's '/' between morphemes takes no part: it is never hot,
    and the alignment skips it."""
    from difflib import SequenceMatcher

    kept = [[k for k, u in enumerate(us) if u != "/"] for us in forms_units]
    hot = [set() for _ in forms_units]
    for i, a in enumerate(forms_units):
        ka = kept[i]
        for j, b in enumerate(forms_units):
            if i == j:
                continue
            kb = kept[j]
            sm = SequenceMatcher(
                None, [a[k][0] for k in ka], [b[k][0] for k in kb], autojunk=False
            )
            for tag, i1, i2, j1, _j2 in sm.get_opcodes():
                if tag != "equal":
                    hot[i].update(ka[x] for x in range(i1, i2))
                    continue
                for x in range(i2 - i1):
                    if highlight_key(a[ka[i1 + x]]) != highlight_key(b[kb[j1 + x]]):
                        hot[i].add(ka[i1 + x])
    return hot


def stack(*forms, highlight=True):
    """Forms one above the other, for one cell: each in MAM-normal order and drawn by
    israel_bible_review_index's form_html, its letters that differ from another form's
    highlighted and its atoms with no difference in gray.  highlight=False draws them plain.
    """
    assert forms and all(isinstance(f, str) and HEB_LETTER.search(f) for f in forms)
    us = [units(mnorm(f)) for f in forms]
    hots = hot_units(us) if highlight and len(us) > 1 else [set() for _ in us]
    return H("<br>".join(ib.form_html(u, h) for u, h in zip(us, hots)))


def word(s):
    """One form for a cell, plain: in MAM-normal order, in lang="hbo" and letter-spaced as
    form_html draws forms.  morphhb's '/' between morphemes, where kept, is drawn as it is.
    """
    return stack(s, highlight=False)


# ---------------------------------------------------------------- tables


def td(content, cls=None, rowspan=None, rtl=False, title=None):
    """A cell.  Hebrew content needs rtl=True (and the lint checks that it has it)."""
    attrs = []
    if rtl:
        attrs.append('dir="rtl"')
    classes = ["first"] + ([cls] if cls else [])
    attrs.append(f'class="{" ".join(classes)}"')
    if rowspan and rowspan > 1:
        attrs.append(f'rowspan="{rowspan}"')
    if title:
        attrs.append(f'title="{html.escape(title)}"')
    return H(f"<td {' '.join(attrs)}>{ht(content)}</td>")


def form_td(*forms, highlight=True):
    """A cell of forms one above the other (stack), right-to-left."""
    return td(stack(*forms, highlight=highlight), cls="form", rtl=True)


def note_td(*content):
    return td(ht(*content), cls="note")


def table(headers, rows, caption=None):
    """A table of forms (table.main, which STYLESHEET draws), broken out of the text column and
    centred as document.css's breakout bounds allow.  headers are plain strings or H; rows are
    lists of td() cells."""
    head = "".join(f"<th>{ht(h)}</th>" for h in headers)
    cap = f"<caption>{ht(caption)}</caption>" if caption else ""
    body = "\n".join(f"<tr>{''.join(r)}</tr>" for r in rows)
    return H(
        f'<table class="main breakout">{cap}<thead><tr>{head}</tr></thead><tbody>\n'
        f"{body}\n</tbody></table>\n"
    )


# ---------------------------------------------------------------- elements


def p(*parts):
    return H(f"<p>{ht(*parts)}</p>\n")


def ul(items):
    return H("<ul>\n" + "".join(f"<li>{ht(i)}</li>\n" for i in items) + "</ul>\n")


def ol(items):
    return H("<ol>\n" + "".join(f"<li>{ht(i)}</li>\n" for i in items) + "</ol>\n")


def heading(level, text, id_):
    """A heading with an id, so that the page's contents and its own cross-references link
    to it."""
    assert re.fullmatch(r"[a-z0-9-]+", id_), id_
    return H(f'<h{level} id="{id_}">{ht(text)}</h{level}>\n')


def code(s):
    return H(f"<code>{html.escape(s, quote=False)}</code>")


def q(*parts):
    """A quotation, drawn with its quotation marks.  Only inside one may the page name the
    report's own sections as the report does ("Part 1", "Part 2"), or use a word that the lint
    bans elsewhere; the lint does not read inside one."""
    return H(f"<q>{ht(*parts, verbatim=True)}</q>")


def blockquote(when, text):
    """A quotation of Ben's, set off, with when he wrote it above it."""
    return H(
        f'<blockquote><p class="when">{ht(when)}</p>'
        f"<p>{ht(text, verbatim=True)}</p></blockquote>\n"
    )


def strong(*parts):
    return H(f"<strong>{ht(*parts)}</strong>")


def a(href, text, kind, title=None):
    """A link marked as MAM-basics' link helper marks links (link-presentation.css draws its
    arrow): kind is "external", "down" or "up" (this page)."""
    assert kind in ("external", "down", "up"), kind
    hover = f' title="{html.escape(title)}"' if title else ""
    return H(
        f'<a href="{html.escape(href)}" data-na-link="{kind}"{hover}>{ht(text)}</a>'
    )


def here(id_, text, up=False):
    """A link to a heading of this page."""
    return a("#" + id_, text, "up" if up else "down")


def commit(sha, date=None, message=None):
    """A morphhb commit, linked on GitHub, with its date and message where given; the message
    is a quotation (q)."""
    link = a(f"{MORPHHB_URL}/commit/{sha}", code(sha), "external")
    if date and message:
        return ht(link, f" ({date}, ", q(message), ")")
    if date:
        return ht(link, f" ({date})")
    return link


def issue(n):
    """An issue or pull request of openscriptures/morphhb, named with its repository and
    linked (github-issues: in cross-repository prose, name the repository)."""
    return a(f"{MORPHHB_URL}/issues/{n}", f"openscriptures/morphhb#{n}", "external")


# ---------------------------------------------------------------- verses

_FULL = {full: full for full in ib.SHORT}
_FULL.update({short: full for full, short in ib.SHORT.items()})
_FULL.update({short.replace(" ", ""): full for full, short in ib.SHORT.items()})
_FULL["Ecclesiastes"] = "Qoheleth"
# A reader's name for a book in prose; the review's tables use ib.SHORT's.
_PROSE_NAME = {"Qoheleth": "Ecclesiastes"}


def parse_ref(ref):
    """(book as ib.SHORT's keys name it, chapter, verse) from "Exodus 10:28", "Exod 10:28",
    "2Kgs 6:25" or "Exod.10.28"; anything else raises."""
    if isinstance(ref, (tuple, list)):
        book, c, v = ref
        assert book in ib.SHORT, ref
        return book, int(c), int(v)
    m = re.fullmatch(r"(.+?)[ .](\d+)[:.](\d+)", ref.replace(NBSP, " "))
    if not m or m.group(1) not in _FULL:
        raise ValueError(f"a verse reference this page cannot read: {ref!r}")
    return _FULL[m.group(1)], int(m.group(2)), int(m.group(3))


def verse_short(ref):
    """The verse's short name, as a table's Verse cell writes it: "Exod 10:28", with a no-break
    space."""
    book, c, v = parse_ref(ref)
    return f"{ib.SHORT[book]}{NBSP}{c}:{v}"


def verse_name(ref):
    """The verse's name in prose: "Exodus 10:28", "Ecclesiastes 2:23"."""
    book, c, v = parse_ref(ref)
    return f"{_PROSE_NAME.get(book, book)} {c}:{v}"


def vref(ref, short=False):
    """The verse named in prose, or by its short name."""
    return H(html.escape(verse_short(ref) if short else verse_name(ref)))


def vcell(ref, extra=None):
    """A verse's cell (td.bcv): its short name, and below it any extra text."""
    content = ht(vref(ref, short=True), H("<br>") if extra else None, extra)
    return td(content, cls="bcv")


# ---------------------------------------------------------------- morphhb's codes

# morphhb's morphology codes, as the Open Scriptures Hebrew Bible documents them
# (https://hb.openscriptures.org/parsing/HebrewMorphologyCodes.html).  Closed dispatch: a code
# with any part not listed raises.
_LANG = {"H": "Hebrew", "A": "Aramaic"}
_GENDER = {
    "m": "masculine",
    "f": "feminine",
    "b": "masculine and feminine",
    "c": "common",
}
_NUMBER = {"s": "singular", "p": "plural", "d": "dual"}
_STATE = {"a": "absolute", "c": "construct", "d": "determined"}
_PERSON = {"1": "first person", "2": "second person", "3": "third person", "x": ""}
_STEM = {
    "H": {
        "q": "Qal",
        "N": "Niphal",
        "p": "Piel",
        "P": "Pual",
        "h": "Hiphil",
        "H": "Hophal",
        "t": "Hithpael",
        "o": "Polel",
        "O": "Polal",
        "r": "Hithpolel",
        "m": "Poel",
        "M": "Poal",
        "k": "Palel",
        "K": "Pulal",
        "Q": "Qal passive",
        "l": "Pilpel",
        "L": "Polpal",
        "f": "Hithpalpel",
        "D": "Nithpael",
        "j": "Pealal",
        "i": "Pilel",
        "u": "Hothpaal",
        "c": "Tiphil",
        "v": "Hishtaphel",
        "w": "Nithpalel",
        "y": "Nithpoel",
        "z": "Hithpoel",
    },
    "A": {
        "q": "Peal",
        "Q": "Peil",
        "u": "Hithpeel",
        "N": "Niphal",
        "p": "Pael",
        "P": "Ithpaal",
        "M": "Hithpaal",
        "a": "Aphel",
        "h": "Haphel",
        "s": "Saphel",
        "e": "Shaphel",
        "H": "Hophal",
        "i": "Ithpeel",
        "t": "Hishtaphel",
        "v": "Ishtaphel",
        "w": "Hithaphel",
        "o": "Polel",
        "z": "Ithpoel",
        "r": "Hithpolel",
        "f": "Hithpalpel",
        "b": "Hephal",
        "c": "Tiphel",
        "m": "Poel",
        "l": "Palpel",
        "L": "Ithpalpel",
        "O": "Ithpolel",
        "G": "Ittaphal",
    },
}
_FINITE = {
    "p": "perfect (qatal)",
    "q": "sequential perfect (weqatal)",
    "i": "imperfect (yiqtol)",
    "w": "sequential imperfect (wayyiqtol)",
    "h": "cohortative",
    "j": "jussive",
    "v": "imperative",
}
_PARTICIPLE = {"r": "participle, active", "s": "participle, passive"}
_INFINITIVE = {"a": "infinitive absolute", "c": "infinitive construct"}
_PARTICLE = {
    "a": "affirmation",
    "d": "definite article",
    "e": "exhortation",
    "i": "interrogative",
    "j": "interjection",
    "m": "demonstrative",
    "n": "negative",
    "o": "direct object marker",
    "r": "relative",
}
_PRONOUN = {
    "d": "demonstrative",
    "f": "indefinite",
    "i": "interrogative",
    "p": "personal",
    "r": "relative",
}
_SUFFIX = {"d": "directional he", "h": "paragogic he", "n": "paragogic nun"}
_ADJECTIVE = {
    "a": "adjective",
    "c": "cardinal number",
    "g": "gentilic",
    "o": "ordinal number",
}
_NOUN = {"c": "common", "g": "gentilic"}
_PROPER = {"": "", "m": "masculine", "f": "feminine", "l": "location", "t": "title"}


def _gns(s, where):
    """gender, number and state."""
    if len(s) != 3 or s[0] not in _GENDER or s[1] not in _NUMBER or s[2] not in _STATE:
        raise ValueError(f"morph {where}: {s!r}")
    return f"{_GENDER[s[0]]} {_NUMBER[s[1]]} {_STATE[s[2]]}"


def _pgn(s, where):
    """person, gender and number."""
    if len(s) != 3 or s[0] not in _PERSON or s[1] not in _GENDER or s[2] not in _NUMBER:
        raise ValueError(f"morph {where}: {s!r}")
    person = _PERSON[s[0]]
    return " ".join(x for x in (person, _GENDER[s[1]], _NUMBER[s[2]]) if x)


def _segment(seg, lang, where):
    pos, rest = seg[0], seg[1:]
    if pos == "C" and not rest:
        return "conjunction"
    if pos == "D" and not rest:
        return "adverb"
    if pos == "R" and rest in ("", "d"):
        return "preposition" + (", with the definite article" if rest else "")
    if pos == "T" and len(rest) == 1 and rest in _PARTICLE:
        return f"particle, {_PARTICLE[rest]}"
    if pos == "N" and rest[:1] == "p" and rest[1:] in _PROPER:
        return "noun, proper name" + (f", {_PROPER[rest[1:]]}" if rest[1:] else "")
    if pos == "N" and rest[:1] in _NOUN:
        return f"noun, {_NOUN[rest[0]]}, {_gns(rest[1:], where)}"
    if pos == "A" and rest[:1] in _ADJECTIVE:
        kind = "adjective" if rest[0] == "a" else f"adjective ({_ADJECTIVE[rest[0]]})"
        return f"{kind}, {_gns(rest[1:], where)}"
    if pos == "P" and rest[:1] in _PRONOUN:
        return f"pronoun, {_PRONOUN[rest[0]]}, {_pgn(rest[1:], where)}"
    if pos == "S" and rest[:1] == "p":
        return f"pronominal suffix, {_pgn(rest[1:], where)}"
    if pos == "S" and rest in _SUFFIX:
        return f"suffix, {_SUFFIX[rest]}"
    if pos == "V" and len(rest) >= 2 and rest[0] in _STEM[lang]:
        stem, kind, tail = _STEM[lang][rest[0]], rest[1], rest[2:]
        if kind in _FINITE:
            return f"verb, {stem}, {_FINITE[kind]}, {_pgn(tail, where)}"
        if kind in _PARTICIPLE:
            return f"verb, {stem}, {_PARTICIPLE[kind]}, {_gns(tail, where)}"
        if kind in _INFINITIVE and not tail:
            return f"verb, {stem}, {_INFINITIVE[kind]}"
    raise ValueError(f"morph {where}: segment {seg!r}")


def morph_words(code_):
    """morphhb's morph code in words, e.g. "HC/Vqw3ms": "Hebrew: conjunction + verb, Qal,
    sequential imperfect (wayyiqtol), third person masculine singular"."""
    if not code_ or code_[0] not in _LANG or len(code_) < 2:
        raise ValueError(f"morph: {code_!r}")
    lang = code_[0]
    segs = code_[1:].split("/")
    return f"{_LANG[lang]}: " + " + ".join(_segment(s, lang, code_) for s in segs)


def morph(code_):
    """morphhb's morph code, with its meaning on hover."""
    return H(f'<abbr title="{html.escape(morph_words(code_))}">{code(code_)}</abbr>')


# ---------------------------------------------------------------- the page

# The page's own stylesheet, which morphhb_corrections_index.gen_html_file publishes beside the
# page as STYLESHEET_NAME under a banner naming that generator (doc/html-styles.md: "Generated
# sheets identify their source in their banner").  It holds only what this page alone has: the
# tables of forms that form_html draws and their highlighting, which the page took from the
# review of the Israel Bible's sheet until the review of 2026-11-16 (finding 16) asked that the
# page no longer depend on that sheet; the tables' breakout within document.css's bounds, as
# gh-pages/wlc/style.css's tables break out; and its captions, notes, numbers, hovers,
# contents and quotations.  The rules are those of the two sheets they come from, unchanged
# but for td.code, which no cell of the page has, so the page looks as it did.
STYLESHEET_NAME = "style.css"
STYLESHEET = """\
/* The stylesheet of morphhb-corrections/index.html, "Where morphhb defies or resolves WLC".
   Before it the page loads the shared document.css, for its prose and its width, and
   MAM-with-doc/misc/style.css, for its pointed Hebrew in Taamey D and its caveat box; after
   it, near-aleppo/link-presentation.css, for its arrow links.  So this sheet holds only what
   this page alone has.  Colours that differ in a dark scheme are given by light-dark(), as
   document.css gives its own. */
/* A letter cluster that differs between the forms that one cell compares. */
.diff { color: light-dark(#8f2015, #ffb4a8); background: light-dark(#fff0eb, #40140d);
  border-radius: .12em; }
/* An atom with no such cluster, gray as document.css's gray class is, and not spaced: each
   form is in document.css's extra letter spacing. */
.context { color: gray; letter-spacing: normal; }
table.main { border-collapse: collapse; border: 1px solid light-dark(#c9c9c9, #444);
  margin: 0 auto; }
table.main > thead > tr > th { border: 1px solid light-dark(#c9c9c9, #444);
  background: light-dark(#f4f4f4, #222); padding: 6px 8px; text-align: left; }
table.main > tbody > tr > td { border-left: 1px solid light-dark(#c9c9c9, #444);
  border-right: 1px solid light-dark(#c9c9c9, #444); padding: 0 8px; vertical-align: middle; }
table.main > tbody > tr > td.first { border-top: 1px solid light-dark(#c9c9c9, #444); }
/* The forms that a cell compares stand one above the other; this line height keeps the points
   under one form clear of the points over the next. */
td.form { text-align: right; white-space: nowrap; line-height: 1.7; }
td.bcv { white-space: nowrap; padding: 6px 10px; }
td.note { padding: 6px 8px; max-width: 32em; font-size: 95%; }
td.num { text-align: right; padding: 6px 8px; }
abbr[title] { text-decoration: underline dotted; cursor: help; }
/* A wide table breaks out of the text column within document.css's bounds. */
table.main.breakout { width: max-content; max-width: var(--breakout-table-max-width);
  margin: 1em 0 1em 50%; transform: translateX(var(--breakout-table-shift)); }
table.main caption { caption-side: top; text-align: left; padding: 0 0 .3em; }
nav.contents li { margin: .1em 0; }
blockquote p.when { font-size: 90%; margin-bottom: .2em; }
"""
# The page loads, by relative paths from its folder, gh-pages/morphhb-corrections/: document.css,
# the prose base; MAM-with-doc/misc/style.css, whose @font-face loads
# gh-pages/woff2/Taamey_D.woff2 by its own relative URL and which draws p.ai-caveat; its own
# stylesheet, STYLESHEET above; and near-aleppo/link-presentation.css, for the arrow links
# (doc/html-styles.md).
CSS_HREFS = (
    "../document.css",
    "../MAM-with-doc/misc/style.css",
    STYLESHEET_NAME,
    "../near-aleppo/link-presentation.css",
)


def page(title, body):
    """The whole page: head, title as h1, then body (an H)."""
    links_ = "\n".join(f'<link rel="stylesheet" href="{h}">' for h in CSS_HREFS)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(title)}</title>\n{links_}\n</head>\n<body>\n"
        f"<h1>{ht(title)}</h1>\n{body}\n</body>\n</html>\n"
    )
