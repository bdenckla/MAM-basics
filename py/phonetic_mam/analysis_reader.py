"""Read the public display corpus for independent analyses.

The stored input consists only of the displayed cells. Branches, syllable facts,
and scanner inputs below are temporary calculations; none is another release
format or a serialized substitute for the display corpus.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache
from itertools import product

from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from phonetic_mam import display_schema

CANT_ALEF = "cant-alef"
CANT_BET = "cant-bet"
QAMATS_DAL = "qamats-dal"
QAMATS_SAM = "qamats-sam"

_LABELS = {
    "קמץ-ד": (QAMATS_DAL, None),
    "קמץ-ס": (QAMATS_SAM, None),
    "טעם פשוטה": (None, CANT_ALEF),
    "טעם מדרשית": (None, CANT_BET),
    "טעם תחתון": (None, CANT_ALEF),
    "טעם עליון": (None, CANT_BET),
    "טעם תחתון, קמץ-ד": (QAMATS_DAL, CANT_ALEF),
    "טעם עליון, קמץ-ד": (QAMATS_DAL, CANT_BET),
    "טעם תחתון, קמץ-ס": (QAMATS_SAM, CANT_ALEF),
    "טעם עליון, קמץ-ס": (QAMATS_SAM, CANT_BET),
}
_DISPLAY_TO_ASCII = {
    "ḥ": "x",
    "e\N{COMBINING ACUTE ACCENT}": "E",
    "i\N{COMBINING ACUTE ACCENT}": "I",
    "o\N{COMBINING ACUTE ACCENT}": "O",
    "e\N{COMBINING BREVE}": "6",
    "a\N{COMBINING BREVE}": "8",
    "o\N{COMBINING BREVE}": "0",
    "’": "'",
    "‘": "`",
    "·": ".",
}


def _inline_text(tokens):
    parts = []
    for token in tokens:
        if isinstance(token, str):
            parts.append(token)
        elif token["kind"] == "implicit-maqaf":
            parts.append(hpu.NU_GMAQ)
        elif token["kind"] == "superscript-e":
            parts.append("^")
        elif token["kind"] == "stressed":
            parts.append("!" + _inline_text(token["content"]))
        else:
            raise display_schema.PublicReleaseError("unexpected nested reading label")
    text = "".join(parts)
    for displayed, ascii_text in _DISPLAY_TO_ASCII.items():
        text = text.replace(displayed, ascii_text)
    return text


def _cell(tokens):
    if tokens is None:
        return None
    if len(tokens) == 1 and isinstance(tokens[0], dict):
        token = tokens[0]
        if token["kind"] == "reading":
            return _LABELS[token["label"]], _inline_text(token["content"])
    return (None, None), _inline_text(tokens)


@dataclass(frozen=True)
class Reading:
    """One displayed Hebrew form paired with its displayed transcription."""

    hebrew: str
    transcription: str
    qamats: str | None = None
    cantillation: str | None = None

    def decoded(self):
        """A temporary core calculation, uniquely checked against the display."""
        return _decode(self.hebrew, self.transcription)

    def syllables(self):
        """Temporary core syllables aligned to generic displayed Hebrew."""
        from phonetic_mam.core import syllables, vowar_and_accar

        vowel_form, accent_form = vowar_and_accar.vowar_and_accar(self.hebrew)
        triple = (self.hebrew, vowel_form, accent_form)
        return syllables.get_syllables(
            {
                "eudlcw-udlcw": self.decoded(),
                "eudlcw-fva": triple,
                "eudlcw-repeated": None,
            }
        )

    def stress_position(self):
        """The displayed primary stress as an atom/syllable position."""
        positions = [
            (atom_index, syllable_index)
            for atom_index, atom in enumerate(self.transcription.split("-"))
            for syllable_index, syllable in enumerate(atom.split("."))
            if syllable.startswith("!")
        ]
        display_schema.require(len(positions) == 1, "displayed stress is not unique")
        return positions[0]

    def scanner_word(self):
        """Reproduce the established accent-scanner input without storing it."""
        from phonetic_mam.core import deep_latin

        geminate_letters = set()
        letter_index = 0
        for char in self.decoded():
            if char == deep_latin.BLACK_MAQAF:
                continue
            if char in deep_latin.GEMINATES:
                geminate_letters.add(letter_index)
            letter_index += len(deep_latin.get_he_letters_back(char))
        out = []
        letter_index = -1
        for char in self.hebrew:
            if "א" <= char <= "ת":
                letter_index += 1
            if char == hpo.DAGOMOSD and letter_index in geminate_letters:
                char = hpu.UPDOT
            out.append(char)
        return "".join(out)


@dataclass(frozen=True)
class Branch:
    qamats: str | None
    cantillation: str | None
    readings: tuple[Reading, ...]


@dataclass(frozen=True)
class Row:
    branches: tuple[Branch, ...] = ()
    marker: str | None = None
    # The one strand whose layout marker this is, or None for a marker of both.
    marker_cantillation: str | None = None


@dataclass(frozen=True)
class Verse:
    rows: tuple[Row, ...]

    def select(self, *, qamats=None, cantillation=None):
        """Select named displayed alternatives, leaving ordinary rows unchanged.

        A layout marker of one strand is dropped from another strand's selection.
        """
        return Verse(
            tuple(
                replace(
                    row,
                    branches=tuple(
                        branch
                        for branch in row.branches
                        if branch.qamats in (None, qamats) or qamats is None
                        if branch.cantillation in (None, cantillation)
                        or cantillation is None
                    ),
                    marker=(
                        row.marker
                        if row.marker_cantillation in (None, cantillation)
                        or cantillation is None
                        else None
                    ),
                )
                for row in self.rows
            )
        )

    def readings(self):
        return [
            reading
            for row in self.rows
            for branch in row.branches
            for reading in branch.readings
        ]

    def events(self):
        out = []
        for row in self.rows:
            if row.marker is not None:
                out.append(row.marker)
            if any(branch.qamats is not None for branch in row.branches):
                out.append("cb-qamats")
            out.extend(
                reading for branch in row.branches for reading in branch.readings
            )
        return out


def _row(source):
    hebrew_cells = [_cell(cell) for cell in source["hebrew"] if cell is not None]
    trans_cells = [
        _cell(cell)
        for cell in source["transcriptions"]["sephardic"]
        if cell is not None
    ]
    if not hebrew_cells:
        display_schema.require(len(trans_cells) == 1, "layout marker shape")
        (qamats, cantillation), marker = trans_cells[0]
        display_schema.require(qamats is None, "layout marker with a qamats label")
        return Row(marker=marker, marker_cantillation=cantillation)
    transcriptions = dict(trans_cells)
    display_schema.require(
        len(transcriptions) == len(trans_cells), "duplicate transcription labels"
    )
    # A displayed em dash repeats the first qamats transcription.
    for key, value in tuple(transcriptions.items()):
        if value == "—":
            display_schema.require(key == (None, None), "labelled repetition dash")
            display_schema.require(
                (QAMATS_DAL, None) in transcriptions, "unresolved repetition dash"
            )
            transcriptions[(QAMATS_SAM, None)] = transcriptions[(QAMATS_DAL, None)]
            del transcriptions[key]
    branches = []
    for (qamats, cantillation), hebrew in hebrew_cells:
        candidates = [
            text
            for (t_qamats, t_cantillation), text in transcriptions.items()
            if t_qamats in (None, qamats) and t_cantillation in (None, cantillation)
        ]
        display_schema.require(len(candidates) == 1, "unresolved display pairing")
        words, transcripts = hebrew.split(" "), candidates[0].split(" ")
        display_schema.require(len(words) == len(transcripts), "display form count")
        branches.append(
            Branch(
                qamats,
                cantillation,
                tuple(
                    Reading(word, transcript, qamats, cantillation)
                    for word, transcript in zip(words, transcripts, strict=True)
                ),
            )
        )
    return Row(tuple(branches))


def book_verses(book):
    """Construct temporary analysis views of an already validated display book."""
    display_schema.validate_book(book)
    return {
        (chapter["number"], verse["number"]): Verse(
            tuple(_row(row) for row in verse["rows"])
        )
        for chapter in book["chapters"]
        for verse in chapter["verses"]
    }


@lru_cache(maxsize=2)
def read_book(book_id):
    """Load one canonical book from the public release, with no private fallback."""
    from phonetic_mam import release

    return book_verses(release.read_book(book_id))


@lru_cache(maxsize=32768)
def _decode(hebrew, transcription):
    from phonetic_mam.core import deep_latin as dl
    from phonetic_mam.core import jtech_ascii, resolve_ambiguities, syllables
    from phonetic_mam.core import vowar_and_accar

    vowel_form, _accent_form = vowar_and_accar.vowar_and_accar(hebrew)
    ambiguous = dl.get_deeplat_from_cw_ndns_h(vowel_form)
    choices = {
        dl.BET_1DAG_AMB: (dl.BET_1DAG_QAL, dl.BET_1DAG_XAZAQ),
        dl.GIMEL_1DAG_AMB: (dl.GIMEL_1DAG_QAL, dl.GIMEL_1DAG_XAZAQ),
        dl.DALET_1DAG_AMB: (dl.DALET_1DAG_QAL, dl.DALET_1DAG_XAZAQ),
        dl.KAF_1DAG_AMB: (dl.KAF_1DAG_QAL, dl.KAF_1DAG_XAZAQ),
        dl.PE_1DAG_AMB: (dl.PE_1DAG_QAL, dl.PE_1DAG_XAZAQ),
        dl.TAV_1DAG_AMB: (dl.TAV_1DAG_QAL, dl.TAV_1DAG_XAZAQ),
        dl.FKAF_1DAG_AMB: (dl.FKAF_1DAG_QAL, dl.FKAF_1DAG_XAZAQ),
        dl.FPE_1DAG_AMB: (dl.FPE_1DAG_QAL,),
        dl.VAV_1DAGOSD: (dl.SHURUQ, dl.VAV_1DAG),
        dl.SHEVA_AMB: (dl.SHEVA_NAX, dl.SHEVA_NA),
    }
    expected = transcription.replace("!", "")
    matches = set()
    for letters in product(*(choices.get(char, (char,)) for char in ambiguous)):
        decoded = resolve_ambiguities.resolve_ydys_ambiguities_in_adlcw(
            "".join(letters)
        )
        if resolve_ambiguities.find_concerns(decoded):
            continue
        atoms = syllables._get_atoms_as_lists_of_sylrecs(decoded)
        actual = jtech_ascii.get_jtech_ascii(
            "jta-dialect-sefarad",
            {"sas-syls-per-atom": atoms, "sas-isps-two-d": None},
        )
        if actual == expected:
            matches.add(decoded)
    display_schema.require(
        len(matches) == 1,
        f"display decoding is not unique: {hebrew!r} / {transcription!r}",
    )
    return matches.pop()
