"""Project transient display inputs into the closed public page model.

Only generic display Hebrew and the existing transcriptions enter this module.
The table widths, labels, and equality-based sharing preserve the old renderer.
No calculation state or adapter input is persisted.
"""

import re

from mb_cmn import bib_locales, hebrew_punctuation
from phonetic_mam import display_schema as schema

ADAPTER_SCHEMA = "phonetic-mam-display-input-v1"
_CANT_NAMES = {
    bib_locales.BK_GENESIS: ("פשוטה", "מדרשית"),
    bib_locales.BK_EXODUS: ("תחתון", "עליון"),
    bib_locales.BK_DEUTER: ("תחתון", "עליון"),
}
_TRANSLATION = str.maketrans(
    {
        "x": "ḥ",
        "E": "e\N{COMBINING ACUTE ACCENT}",
        "I": "i\N{COMBINING ACUTE ACCENT}",
        "O": "o\N{COMBINING ACUTE ACCENT}",
        "6": "e\N{COMBINING BREVE}",
        "8": "a\N{COMBINING BREVE}",
        "0": "o\N{COMBINING BREVE}",
        "'": "\N{RIGHT SINGLE QUOTATION MARK}",
        "`": "\N{LEFT SINGLE QUOTATION MARK}",
    }
)


def _keys(value, keys):
    schema.require(isinstance(value, dict), "adapter input must be an object")
    schema.require(set(value) == set(keys), "unknown or missing adapter fields")


def _compact(tokens):
    result = []
    for token in tokens:
        if token == "":
            continue
        if isinstance(token, str) and result and isinstance(result[-1], str):
            result[-1] += token
        else:
            result.append(token)
    return result


def transcription_tokens(text):
    """Apply the existing technical-transcription display substitutions."""
    schema.require(isinstance(text, str) and text, "missing transcription")
    result = []
    parts = re.split(r"([.\-])", text)
    for index, part in enumerate(parts):
        if index % 2:
            result.append("·" if part == "." else "-")
            continue
        schema.require(bool(part), "empty transcription syllable")
        stressed = part.startswith("!")
        if stressed:
            part = part[1:]
        schema.require(bool(part) and "!" not in part, "invalid transcription stress")
        tokens = _compact(
            [
                {"kind": "superscript-e"} if char == "^" else char
                for char in part.translate(_TRANSLATION)
            ]
        )
        result.extend([{"kind": "stressed", "content": tokens}] if stressed else tokens)
    result = _compact(result)
    schema.validate_tokens(result, "transcription", "transcription")
    return result


def _hebrew_tokens(text):
    schema.require(isinstance(text, str) and text, "missing display Hebrew")
    parts = text.split(hebrew_punctuation.NU_GMAQ)
    tokens = []
    for index, part in enumerate(parts):
        if index:
            tokens.append({"kind": "implicit-maqaf"})
        tokens.append(part)
    tokens = _compact(tokens)
    schema.validate_tokens(tokens, "hebrew", "display Hebrew")
    return tokens


def _word(word, pronunciation):
    _keys(word, ("kind", "hebrew", "transcriptions"))
    schema.require(word["kind"] == "word", "expected a display word")
    _keys(word["transcriptions"], schema.PRONUNCIATIONS)
    return _hebrew_tokens(word["hebrew"]), transcription_tokens(
        word["transcriptions"][pronunciation]
    )


def _words(words, pronunciation):
    schema.require(isinstance(words, list) and 1 <= len(words) <= 2, "reading shape")
    hebrew, transcription = [], []
    for index, word in enumerate(words):
        h_tokens, t_tokens = _word(word, pronunciation)
        if index:
            hebrew.append(" ")
            transcription.append(" ")
        hebrew.extend(h_tokens)
        transcription.extend(t_tokens)
    return _compact(hebrew), _compact(transcription)


def _label(label, content):
    schema.require(label in schema.READING_LABELS, "unknown display reading")
    return [{"kind": "reading", "label": label, "content": content}]


def _dualcant(element, pronunciation):
    _keys(element, ("kind", "first", "second"))
    schema.require(element["kind"] == "dualcant", "expected paired readings")
    ha, ta = _words(element["first"], pronunciation)
    hb, tb = _words(element["second"], pronunciation)
    return ha, hb, ta, tb


def _qamats_reading(book, element, pronunciation, label):
    if isinstance(element, dict):
        ha, hb, ta, tb = _dualcant(element, pronunciation)
        schema.require(ta == tb, "unsupported four-way transcription")
        names = _CANT_NAMES[book]
        return (
            _label(f"טעם {names[0]}, {label}", ha),
            _label(f"טעם {names[1]}, {label}", hb),
            _label(label, ta),
        )
    he, tr = _words(element, pronunciation)
    return _label(label, he), _label(label, tr)


def _row(book, element, pronunciation):
    schema.require(isinstance(element, dict), "unknown display element")
    kind = element.get("kind")
    if kind == "word":
        he, tr = _word(element, pronunciation)
        return {3: he}, {0: tr}
    if kind == "layout":
        _keys(element, ("kind", "label"))
        schema.require(element["label"] in schema.LAYOUT_MARKERS, "unknown layout")
        return {}, {0: [element["label"]]}
    if kind == "dualcant":
        ha, hb, ta, tb = _dualcant(element, pronunciation)
        schema.require(book in _CANT_NAMES, "unexpected paired-reading book")
        names = _CANT_NAMES[book]
        hebrew = {2: _label(f"טעם {names[0]}", ha), 3: _label(f"טעם {names[1]}", hb)}
        transcriptions = (
            {0: ta}
            if ta == tb
            else {0: _label(f"טעם {names[0]}", ta), 1: _label(f"טעם {names[1]}", tb)}
        )
        return hebrew, transcriptions
    if kind == "qamats":
        _keys(element, ("kind", "first", "second"))
        first = _qamats_reading(book, element["first"], pronunciation, "קמץ-ד")
        second = _qamats_reading(book, element["second"], pronunciation, "קמץ-ס")
        schema.require(len(first) == len(second), "unequal reading structure")
        tr_first, tr_second = first[-1], second[-1]
        if tr_first[0]["content"] == tr_second[0]["content"]:
            tr_second = ["\N{EM DASH}"]
        hebrew = (
            {0: first[0], 1: first[1], 2: second[0], 3: second[1]}
            if len(first) == 3
            else {2: first[0], 3: second[0]}
        )
        return hebrew, {0: tr_first, 1: tr_second}
    raise schema.PublicReleaseError("unknown display element kind")


def _verse(book, verse):
    _keys(verse, ("chapter", "number", "elements"))
    schema.require(
        isinstance(verse["elements"], list) and verse["elements"], "empty verse"
    )
    projections = {
        pronunciation: [_row(book, item, pronunciation) for item in verse["elements"]]
        for pronunciation in schema.PRONUNCIATIONS
    }
    first, second = (projections[p] for p in schema.PRONUNCIATIONS)
    schema.require(
        [row[0] for row in first] == [row[0] for row in second],
        "pronunciations disagree on Hebrew display",
    )
    minimum = min(index for hrow, _ in first for index in hrow)
    maxima = {
        p: max(index for _, trow in rows for index in trow)
        for p, rows in projections.items()
    }
    rows = [
        {
            "hebrew": [hrow.get(index) for index in range(minimum, 4)],
            "transcriptions": {
                p: [
                    projections[p][row_index][1].get(index)
                    for index in range(maxima[p] + 1)
                ]
                for p in schema.PRONUNCIATIONS
            },
        }
        for row_index, (hrow, _) in enumerate(first)
    ]
    return {
        "number": verse["number"],
        "hebrew_columns": 4 - minimum,
        "transcription_columns": {p: maxima[p] + 1 for p in schema.PRONUNCIATIONS},
        "rows": rows,
    }


def project_book(value):
    """Consume one transient adapter book and return its closed display model."""
    _keys(value, ("schema", "book", "verses"))
    schema.require(value["schema"] == ADAPTER_SCHEMA, "unknown adapter schema")
    book = value["book"]
    schema.require(book in bib_locales.ALL_BK39_IDS, "unknown adapter book")
    schema.require(
        isinstance(value["verses"], list) and value["verses"], "empty adapter book"
    )
    chapters = []
    for verse in value["verses"]:
        _keys(verse, ("chapter", "number", "elements"))
        number = verse["chapter"]
        schema.require(type(number) is int and number > 0, "invalid chapter")
        if not chapters or chapters[-1]["number"] != number:
            schema.require(number == len(chapters) + 1, "noncanonical chapter sequence")
            chapters.append({"number": number, "verses": []})
        chapters[-1]["verses"].append(_verse(book, verse))
    return schema.validate_book(
        {"schema": schema.SCHEMA_ID, "book": book, "chapters": chapters}
    )
