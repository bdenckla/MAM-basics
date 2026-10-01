"""Closed display-level contract for the Phonetic MAM public release.

Every payload value must be independently obtainable from the sanctioned pages
and public MAM. This validator is a necessary shape check, not that disclosure
proof: release approval additionally compares the complete output with the
independent public-only projection. Do not add analysis-only alignments or
source-quality fields to avoid decoding the displayed text in a consumer.
"""

from mb_cmn import bib_locales

SCHEMA_ID = "phonetic-mam-public-v1"
PRONUNCIATIONS = ("sephardic", "ashkenazic")
READING_LABELS = (
    "קמץ-ד",
    "קמץ-ס",
    "טעם פשוטה",
    "טעם מדרשית",
    "טעם תחתון",
    "טעם עליון",
    "טעם תחתון, קמץ-ד",
    "טעם עליון, קמץ-ד",
    "טעם תחתון, קמץ-ס",
    "טעם עליון, קמץ-ס",
)
LAYOUT_MARKERS = ("מ:פסק", "סס", "פפ", "ססס", "פפפ")
_FORBIDDEN = frozenset(map(chr, (0x05AF, 0x05C4, 0x05C8, 0x05C9)))


class PublicReleaseError(ValueError):
    """A candidate release violates its closed public display contract."""


def require(condition, label):
    """Raise a persistent validation error, including under optimized Python."""
    if not condition:
        raise PublicReleaseError(label)


def _keys(value, expected, label):
    require(isinstance(value, dict), f"{label}: expected an object")
    require(set(value) == set(expected), f"{label}: unexpected or missing fields")


def _number(value, label):
    require(type(value) is int and value > 0, f"{label}: expected a positive integer")


def _text(value, label):
    require(isinstance(value, str) and bool(value), f"{label}: expected nonempty text")
    require(not (_FORBIDDEN & set(value)), f"{label}: forbidden phonetic mark")
    require("<" not in value and ">" not in value, f"{label}: markup is not text")
    require("\\u" not in value.lower(), f"{label}: escaped codepoint layer")


def validate_tokens(tokens, language, label, *, allow_label=True, allow_stress=True):
    """Validate a closed, explicitly dispatched inline display vocabulary."""
    require(isinstance(tokens, list) and bool(tokens), f"{label}: empty token sequence")
    for index, token in enumerate(tokens):
        here = f"{label}/{index}"
        if isinstance(token, str):
            _text(token, here)
            continue
        require(isinstance(token, dict), f"{here}: unknown token")
        kind = token.get("kind")
        if kind == "implicit-maqaf":
            _keys(token, ("kind",), here)
            require(language == "hebrew", f"{here}: Hebrew-only token")
        elif kind == "superscript-e":
            _keys(token, ("kind",), here)
            require(language == "transcription", f"{here}: transcription-only token")
        elif kind == "stressed":
            _keys(token, ("kind", "content"), here)
            require(
                language == "transcription" and allow_stress, f"{here}: nested stress"
            )
            validate_tokens(
                token["content"], language, here, allow_label=False, allow_stress=False
            )
        elif kind == "reading":
            _keys(token, ("kind", "label", "content"), here)
            require(allow_label, f"{here}: nested reading label")
            require(token["label"] in READING_LABELS, f"{here}: unknown reading label")
            validate_tokens(token["content"], language, here, allow_label=False)
        else:
            raise PublicReleaseError(f"{here}: unknown inline kind {kind!r}")


def validate_book(book):
    """Validate one nonempty canonical book; the release loader checks all books."""
    _keys(book, ("schema", "book", "chapters"), "book")
    require(book["schema"] == SCHEMA_ID, "unknown schema")
    require(book["book"] in bib_locales.ALL_BK39_IDS, "unknown canonical book")
    chapters = book["chapters"]
    require(isinstance(chapters, list) and bool(chapters), "missing or empty chapters")
    for ch_index, chapter in enumerate(chapters, 1):
        _keys(chapter, ("number", "verses"), "chapter")
        _number(chapter["number"], "chapter number")
        require(chapter["number"] == ch_index, "noncanonical chapter order")
        verses = chapter["verses"]
        require(isinstance(verses, list) and bool(verses), "missing or empty verses")
        for vr_index, verse in enumerate(verses, 1):
            _keys(
                verse,
                ("number", "hebrew_columns", "transcription_columns", "rows"),
                "verse",
            )
            _number(verse["number"], "verse number")
            require(verse["number"] == vr_index, "noncanonical verse order")
            h_count, t_counts = verse["hebrew_columns"], verse["transcription_columns"]
            _number(h_count, "Hebrew column count")
            _keys(t_counts, PRONUNCIATIONS, "transcription column counts")
            for t_count in t_counts.values():
                _number(t_count, "transcription column count")
                require(t_count <= 4, "unsupported transcription table shape")
            require(h_count <= 4, "unsupported Hebrew table shape")
            require(
                isinstance(verse["rows"], list) and bool(verse["rows"]), "empty verse"
            )
            for row in verse["rows"]:
                _keys(row, ("hebrew", "transcriptions"), "row")
                require(
                    isinstance(row["hebrew"], list) and len(row["hebrew"]) == h_count,
                    "Hebrew column shape",
                )
                for cell in row["hebrew"]:
                    if cell is not None:
                        validate_tokens(cell, "hebrew", "Hebrew cell")
                _keys(row["transcriptions"], PRONUNCIATIONS, "transcriptions")
                for pronunciation in PRONUNCIATIONS:
                    cells = row["transcriptions"][pronunciation]
                    require(
                        isinstance(cells, list)
                        and len(cells) == t_counts[pronunciation],
                        "transcription column shape",
                    )
                    for cell in cells:
                        if cell is not None:
                            validate_tokens(cell, "transcription", "transcription cell")
                if all(cell is None for cell in row["hebrew"]):
                    markers = []
                    for pronunciation in PRONUNCIATIONS:
                        cells = row["transcriptions"][pronunciation]
                        require(
                            cells[0] in [[marker] for marker in LAYOUT_MARKERS]
                            and all(cell is None for cell in cells[1:]),
                            "unknown layout marker",
                        )
                        markers.append(cells[0])
                    require(
                        markers[0] == markers[1],
                        "layout marker differs by pronunciation",
                    )
    return book


def canonical_bytes(book):
    """Deterministic UTF-8 representation, without Unicode normalization."""
    import json

    validate_book(book)
    return (json.dumps(book, ensure_ascii=False, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )
