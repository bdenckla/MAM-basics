"""Actual mpplus template fragments and their checked near-Aleppo results.

The source lookup uses doc_figures' closed template walk in Scripture-bearing
fields. Every example must identify exactly one named source template at its verse.
Evaluate that fragment through the build's template and representation policies,
then require its result exactly once in the actual near-Aleppo verse. JSON values
are read at generation time; no pointed Hebrew example is retyped here.
"""

import copy
import json
import re
import unicodedata

from near_aleppo import build_paths
from near_aleppo import doc_figures
from near_aleppo.doc_html import HEBREW_CELL
from near_aleppo.doc_html import he_name
from near_aleppo.doc_html import table
from mb_misc import mb_html
from near_aleppo.phase2_templates import Resolver
from near_aleppo.phase3_policies import Policies
from near_aleppo.phase3_policies import _selected_text

_EXAMPLES = (
    ("מ:קמץ", ("A1-Genesis", "9", "21"), None),
    ("מ:דחי", ("D1-Psalms", "1", "1"), None),
    ("מ:צינור", ("D1-Psalms", "13", "6"), None),
    # Exodus 20:12 has several double-cantillation templates. This is its short
    # fifth E element, identified by both its exact position and template name.
    ("מ:כפול", ("A2-Exodus", "20", "12"), 4),
    ("מ:לגרמיה-2", ("D1-Psalms", "1", "1"), None),
    ("מ:פסק", ("A1-Genesis", "1", "5"), None),
    ("מ:מקף אפור", ("D1-Psalms", "1", "1"), None),
    ("מ:אות-מיוחדת-במילה", ("A1-Genesis", "1", "1"), None),
)
_MARKS = frozenset(("מ:לגרמיה-2", "מ:פסק", "מ:מקף אפור"))
_SCRIPTURE_FIELDS = {
    "מ:קמץ": ("ד", "ס"),
    "מ:דחי": ("1", "2"),
    "מ:צינור": ("1", "2"),
    "מ:כפול": ("כפול", "א", "ב"),
    "מ:לגרמיה-2": (),
    "מ:פסק": (),
    "מ:מקף אפור": (),
    "מ:אות-מיוחדת-במילה": ("1", "2"),
    "מ:אות-ג": ("1",),
}
_METADATA_FIELDS = {"מ:אות-מיוחדת-במילה": ("3", "4", "5")}
_HIGHLIGHT_PARAMETERS = {
    "מ:קמץ": ("ד", "ס"),
    "מ:דחי": ("1", "2"),
    "מ:צינור": ("1", "2"),
}
_ABBREVIATED_FIELDS = {"מ:אות-מיוחדת-במילה": ("2", "3", "4", "5")}
_RESULT_HIGHLIGHTS = {
    "מ:לגרמיה-2": frozenset(("\N{HEBREW PUNCTUATION PASEQ}",)),
    "מ:פסק": frozenset(("\N{HEBREW PUNCTUATION PASEQ}",)),
    "מ:מקף אפור": frozenset((" ",)),
}


def examples():
    """One before/after row for each evaluated-template example."""
    rows = []
    for name, verse, index in _EXAMPLES:
        source = _cell(build_paths.mam_parsed_plus_dir(), verse)
        final = _cell(build_paths.dataset_dir(), verse)
        matches = [
            tmpl
            for _, tmpl in doc_figures._templates(source, verse, doc_figures._MAM)
            if tmpl["tmpl_name"] == name and (index is None or tmpl is source[index])
        ]
        if len(matches) != 1:
            raise AssertionError(f"{verse}: expected one example of {name!r}")
        (tmpl,) = matches
        fragment = _mark_fragment(source, tmpl, verse) if name in _MARKS else tmpl
        resolved = Resolver().resolve_e_cell(copy.deepcopy(fragment), verse)
        evaluated = _selected_text(Policies().apply_e_cell(resolved, verse), verse)
        actual = _selected_text(doc_figures._with_mam_names(final, verse), verse)
        if not evaluated or actual.count(evaluated) != 1:
            raise AssertionError(f"{verse}: example result absent or ambiguous")
        highlights = _highlight_clusters(tmpl)
        result_highlights = highlights | _RESULT_HIGHLIGHTS.get(name, frozenset())
        qamats_class = " qamats-example" if name == "מ:קמץ" else ""
        rows.append(
            [
                mb_html.bdi(
                    _wikitext(fragment, highlights),
                    {
                        "lang": "hbo",
                        "class": "pointed template-example" + qamats_class,
                    },
                ),
                mb_html.bdi(
                    _text_parts(evaluated, result_highlights),
                    {"lang": "hbo", "class": "pointed" + qamats_class},
                ),
                "*" if qamats_class else "",
            ]
        )
    return [
        mb_html.para(
            "These examples show MAM templates in compact Wikitext syntax beside "
            "the text near-Aleppo has. The punctuation examples include "
            "adjacent text so the spacing is visible."
        ),
        table(["MAM", "near-Aleppo", ""], rows, [HEBREW_CELL, HEBREW_CELL, None]),
        mb_html.para("* Qamats qatan is shown upside down here for clarity."),
        mb_html.para(
            [
                "In the ",
                he_name("מ:קמץ"),
                " example, evaluation selects parameter ",
                he_name("ד"),
                ". That parameter has HEBREW POINT QAMATS QATAN; the final "
                "near-Aleppo text has HEBREW POINT QAMATS under its ",
                mb_html.anchor("qamats policy", {"href": "#qamats-size"}),
                ".",
            ]
        ),
    ]


def _cell(directory, verse):
    book, chapter, number = verse
    with (directory / (book + ".json")).open(encoding="utf-8") as stream:
        book_data = json.load(stream)
    if len(book_data["book39s"]) != 1:
        raise AssertionError(f"{verse}: example needs one sub-book")
    return book_data["book39s"][0]["chapters"][chapter][number][2]


def _mark_fragment(source, tmpl, verse):
    positions = [index for index, item in enumerate(source) if item is tmpl]
    if len(positions) != 1:
        raise AssertionError(f"{verse}: punctuation example is not a direct element")
    (index,) = positions
    before, after = source[index - 1], source[index + 1]
    if not isinstance(before, str) or not isinstance(after, str):
        raise AssertionError(f"{verse}: punctuation example lacks adjacent text")
    last = re.search(r"\S+\s*$", before)
    first = re.match(r"\s*\S+", after)
    if last is None or first is None:
        raise AssertionError(f"{verse}: punctuation example lacks adjacent words")
    return [last.group(), tmpl, first.group()]


def _hebrew_clusters(text):
    """Keep each base character with all following combining marks."""
    clusters = []
    for char in text:
        if unicodedata.category(char).startswith("M"):
            if not clusters:
                raise AssertionError("example begins with an unattached mark")
            clusters[-1] += char
        else:
            clusters.append(char)
    return clusters


def _highlight_clusters(tmpl):
    """Highlight the declared alternative pairs or the large-letter example."""
    name = tmpl["tmpl_name"]
    if name == "מ:אות-מיוחדת-במילה":
        spelling = tmpl["tmpl_params"]["2"]
        if not isinstance(spelling, str) or not spelling.startswith(
            "\N{HEBREW LETTER BET}"
        ):
            raise AssertionError("large-letter example needs its initial bet")
        return frozenset((_hebrew_clusters(spelling)[0],))
    if name not in _HIGHLIGHT_PARAMETERS:
        return frozenset()
    params = tmpl["tmpl_params"]
    first, second = (params[key] for key in _HIGHLIGHT_PARAMETERS[name])
    if not isinstance(first, str) or not isinstance(second, str):
        raise AssertionError(f"{name!r}: highlighting needs text alternatives")
    before, after = _hebrew_clusters(first), _hebrew_clusters(second)
    if [cluster[0] for cluster in before] != [cluster[0] for cluster in after]:
        raise AssertionError(f"{name!r}: alternative bases differ")
    highlights = {
        cluster for pair in zip(before, after) if pair[0] != pair[1] for cluster in pair
    }
    if not highlights:
        raise AssertionError(f"{name!r}: alternatives have no differing cluster")
    return frozenset(highlights)


def _text_parts(text, highlights):
    """Color complete clusters or punctuation, shading a highlighted space."""
    parts = []
    plain = ""
    for cluster in _hebrew_clusters(text):
        if cluster in highlights:
            if plain:
                parts.append(plain)
                plain = ""
            cls = "example-space" if cluster == " " else "example-difference"
            # An entity keeps this literal space out of source-line wrapping.
            contents = mb_html.raw_html("&#32;") if cluster == " " else cluster
            parts.append(mb_html.span(contents, {"class": cls}))
        else:
            plain += cluster
    if plain:
        parts.append(plain)
    return parts


def _syntax(text):
    return mb_html.span(text, {"class": "template-syntax"})


def _wikitext(value, highlights):
    """Reassemble the examples' named templates with explicit display markup.

    Every recognized template declares its Scripture fields. Special-letter
    metadata is plain text and is never traversed as Scripture. Parameter order
    is the source order; consecutive positional keys need no explicit names.
    Validate all arguments, including the explicitly abbreviated fields. The
    styled ellipsis and tsinnor hair space affect only the example's display.
    """
    if isinstance(value, str):
        return _text_parts(value, highlights)
    if isinstance(value, list):
        return [part for item in value for part in _wikitext(item, highlights)]
    if not isinstance(value, dict):
        raise AssertionError("unexpected Wikitext example element")
    name = value["tmpl_name"]
    if name not in _SCRIPTURE_FIELDS:
        raise AssertionError(f"unknown Wikitext example template: {name!r}")
    scripture = _SCRIPTURE_FIELDS[name]
    metadata = _METADATA_FIELDS.get(name, ())
    expected = set(scripture + metadata)
    params = value.get("tmpl_params", {})
    keys = {"tmpl_name", "tmpl_params"} if expected else {"tmpl_name"}
    if set(value) != keys or not isinstance(params, dict) or set(params) != expected:
        raise AssertionError(f"unexpected Wikitext example shape: {name!r}")
    parts = [_syntax("{{"), mb_html.span(name, {"class": "template-name"})]
    abbreviated = _ABBREVIATED_FIELDS.get(name, ())
    omission_shown = False
    positional = 1
    for key, item in params.items():
        if key in metadata:
            if not isinstance(item, str):
                raise AssertionError(f"{name!r}: metadata {key!r} is not text")
            text = [item]
        else:
            text = _wikitext(item, highlights)
        if key in abbreviated:
            if not omission_shown:
                parts.extend(
                    [
                        _syntax("|"),
                        mb_html.span(
                            "\N{HORIZONTAL ELLIPSIS}",
                            {
                                "class": "template-ellipsis",
                                "title": "Further arguments omitted",
                            },
                        ),
                    ]
                )
                omission_shown = True
            continue
        parts.append(_syntax("|"))
        if key == str(positional):
            positional += 1
        else:
            parts.append(f"{key}=")
        parts.extend(text)
    if name == "מ:צינור":
        parts.append("\N{HAIR SPACE}")
    parts.append(_syntax("}}"))
    return parts
