"""Independent pre-stress-meteg survey of the public Phonetic MAM display corpus.

Reduced syllables are grouped with their following main syllable; the target is
the main part of the grouped syllable two before primary stress. The syllable
grouping, vowel-length convention, structural table, accent buckets and case
selection were written to follow this survey's private predecessor, but no tracked
record compares the two. py/tests/test_meteg_before_stress.py checks the accent
class against accgram's prose and poetic scanners and the target meteg against an
independent nucleus locator.

In a poetic verse, U+05A5 on the stressed syllable is the conjunctive merkha unless
it is the yored of oleh-weyored, which is disjunctive. The yored is identified when
the chanted word's accent vector has U+05AB, the oleh, before its final U+05A5. A
candidate whose U+05A5 follows an unpaired oleh on the previous chanted word, one
with no U+05A5 after it there, is refused rather than classified.

Only generic displayed Hebrew and the visible Sephardic transcription enter the
analysis. Its transient syllable facts are never included in the survey output.
The analysis is an accgram consumer, not part of the Phonetic MAM product.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import re

from mb_cmn import bib_locales
from mb_cmn import cantsys
from mb_cmn import file_io
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import uni_heb as uh
from mb_cmn import paths


@dataclass(frozen=True)
class SyllableFacts:
    """Short-lived facts derived from one displayed syllable; never serialized."""

    onset: str
    reduced: bool
    hataf: bool
    guttural: bool
    long_vowel: bool
    explicitly_closed: bool
    implicitly_closed: bool
    accents: str


@dataclass(frozen=True)
class ChantedWordFacts:
    """The classifier's in-memory input, without a source spelling or audit state."""

    syllables: tuple[SyllableFacts, ...]
    primary_stress: int | None
    primary_accent: str
    cantillation_system: str
    accents: str
    accent_vector: tuple[str, ...]
    primary_index: int
    previous_accent_vector: tuple[str, ...]


@dataclass
class _GroupedSyllable:
    main: SyllableFacts | None = None
    reduced: SyllableFacts | None = None
    primary: bool = False


def classify(facts: ChantedWordFacts) -> dict | None:
    """Return the established FR/AFR classification, or no candidate."""
    if not facts.primary_stress:
        return None
    grouped = []
    for index, syllable in enumerate(facts.syllables):
        if syllable.reduced:
            grouped.append(_GroupedSyllable(reduced=syllable))
            continue
        if grouped and grouped[-1].main is None:
            grouped[-1].main = syllable
        else:
            grouped.append(_GroupedSyllable(main=syllable))
        if index == facts.primary_stress:
            grouped[-1].primary = True
    stress = next(i for i, syllable in enumerate(grouped) if syllable.primary)
    if stress < 2:
        return None
    target, buffer, stressed = grouped[stress - 2 : stress + 1]
    if stressed.reduced is None:
        return None
    if not (target.main.implicitly_closed or target.main.explicitly_closed):
        return None
    if target.main.long_vowel:
        return None
    structure = _structure(buffer, stressed)
    if structure is None:
        return None
    coarse, fine = structure
    meteg_present = hpo.MTGOSLQ in target.main.accents
    other_count = (
        facts.accents.count(hpo.MTGOSLQ)
        - facts.accents.count(hpu.SOPA)
        - int(meteg_present)
    )
    return {
        "pattern": coarse,
        "fine_pattern": fine,
        "accent_class": _accent_class(facts),
        "target_meteg": meteg_present,
        "accent_on_target": _accent(target.main.accents),
        # The former record omitted zero before its output projection restored null.
        "other_meteg_count": other_count or None,
    }


_POETIC = cantsys.get_cantsys_from_is_poetcant(True)


def _accent_class(facts: ChantedWordFacts) -> str:
    """Conjunctive or disjunctive, with the yored of oleh-weyored named explicitly.

    In a poetic verse U+05A5 is merkha, a conjunctive, unless it is the yored of
    oleh-weyored, which is disjunctive. The yored is identified when U+05A5 is the
    last and primary accent of the chanted word's accent vector and U+05AB, the oleh,
    comes before it there: the stress table's (oleh, yored), (atnax hafukh, oleh,
    yored) and (merkha, oleh, yored). A primary U+05A5 after an unpaired oleh on the
    previous chanted word is refused rather than classified.
    """
    vector = facts.accent_vector
    if facts.cantillation_system == _POETIC and facts.primary_accent == ha.MER:
        if facts.primary_index == len(vector) - 1 and ha.OLE in vector[:-1]:
            return "disj"
        previous = facts.previous_accent_vector
        if ha.OLE in previous and ha.MER not in previous[previous.index(ha.OLE) :]:
            raise ValueError(
                "A poetic U+05A5 after an oleh on the previous chanted word needs an"
                " oleh-weyored analysis"
            )
    if facts.primary_accent in ha.CONJUNCTIVES_BCC[facts.cantillation_system]:
        return "conj"
    return "disj"


def _accent(accents: str) -> str | None:
    ignored = "א-ת" + hpo.MTGOSLQ + ha.TEL_G + ha.GER_M
    remaining = re.sub(f"[{ignored}]", "", accents)
    if len(remaining) == 1:
        return uh.shunna(remaining)
    assert not remaining
    return None


def _structure(buffer: _GroupedSyllable, stressed: _GroupedSyllable):
    main = buffer.main
    closure = (
        "implicit"
        if main.implicitly_closed
        else "explicit" if main.explicitly_closed else "open"
    )
    reduced = stressed.reduced
    assert not reduced.guttural or reduced.hataf
    kind = {
        (True, True): "guttural-hataf",
        (False, False): "simple",
        (False, True): "other-hataf",
    }[(reduced.guttural, reduced.hataf)]
    key = (
        "long" if main.long_vowel else "short",
        closure,
        buffer.reduced is not None,
        kind,
        reduced.onset == stressed.main.onset,
    )
    result = _STRUCTURES.get(key)
    if result is not None:
        assert result[0] != "never"
    return result


_EITHER = (True, False)
_STRUCTURE_ROWS = (
    ("short", "implicit", False, "other-hataf", _EITHER, "FR1", "FR1j"),
    ("short", "implicit", False, "simple", _EITHER, "FR1", "FR1m"),
    ("short", "implicit", True, "other-hataf", _EITHER, "AFR1", "AFR1-like-FR1"),
    ("short", "implicit", True, "simple", _EITHER, "AFR1", "AFR1-like-FR1"),
    ("short", "explicit", False, "guttural-hataf", _EITHER, "FR2", "FR2h"),
    ("short", "explicit", False, "other-hataf", _EITHER, "FR2", "FR2j"),
    ("short", "explicit", False, "simple", _EITHER, "FR2", "FR2m"),
    ("short", "explicit", True, "guttural-hataf", _EITHER, "XAFR1", "XAFR1-like-FR2h"),
    ("short", "explicit", True, "other-hataf", _EITHER, "never", "SEPJD"),
    ("short", "explicit", True, "simple", _EITHER, "XAFR1", "XAFR1-like-FR2m"),
    ("short", "open", False, "guttural-hataf", (False,), "FR3", "FR3"),
    ("short", "open", False, "other-hataf", (False,), "never", "SOAJN"),
    ("short", "open", True, "guttural-hataf", (False,), "AFR1", "AFR1-like-FR3"),
    ("short", "open", True, "other-hataf", (False,), "MISC", "SOPJN"),
    ("long", "open", False, "guttural-hataf", (False,), "AFR2", "AFR2"),
    ("long", "open", False, "other-hataf", (False,), "AFR4", "AFR4-LOAJN"),
    ("long", "open", False, "simple", (False,), "AFR3", "AFR3"),
    ("short", "open", False, "guttural-hataf", (True,), "never", "SOAHY"),
    ("short", "open", False, "other-hataf", (True,), "AFR4", "AFR4-SOAJY"),
    ("short", "open", False, "simple", (True,), "AFR4", "AFR4-SOAMY"),
    ("long", "open", False, "guttural-hataf", (True,), "AFR4", "AFR4-LOAHY"),
    ("long", "open", False, "other-hataf", (True,), "AFR4", "AFR4-LOAJY"),
    ("long", "open", False, "simple", (True,), "AFR4", "AFR4-LOAMY"),
)
_STRUCTURES = {}
for _length, _closure, _reduced, _kind, _identicals, _coarse, _fine in _STRUCTURE_ROWS:
    for _identical in _identicals:
        _key = _length, _closure, _reduced, _kind, _identical
        assert _key not in _STRUCTURES
        _STRUCTURES[_key] = _coarse, _fine

PATTERNS = ("FR1", "FR2", "FR3", "AFR1", "AFR2", "AFR3", "AFR4", "XAFR1", "MISC")
FULLY_REGULAR = ("FR1", "FR2", "FR3")


def bucket(case: dict) -> str:
    """The historical four-way count key, with its meaning kept explicit in data."""
    return case["accent_class"][0] + ("w" if case["target_meteg"] else "s") + "g"


def summarize(cases: list[dict]) -> dict:
    """Keep the per-case and reshaped-count projections in one analysis."""
    reshaped = {
        pattern: dict.fromkeys(("cwg", "csg", "dwg", "dsg"), 0) for pattern in PATTERNS
    }
    counts = Counter()
    for case in cases:
        reshaped[case["pattern"]][bucket(case)] += 1
        for key in ("fine_pattern", "accent_on_target", "other_meteg_count"):
            if value := case[key]:
                counts[(key, value)] += 1
    return {
        "cases": cases,
        "counts": [
            {"field": field, "value": value, "count": count}
            for (field, value), count in sorted(counts.items())
        ],
        "reshaped_counts": reshaped,
    }


def select_cases(cases: list[dict]) -> dict:
    """Preserve the five downstream selections and their transcription regexes."""
    eligible = [
        case
        for case in cases
        if case["pattern"] in FULLY_REGULAR and case["accent_class"] == "disj"
    ]
    out = {
        "fully_regular_disjunctive_without_target_meteg": [
            case for case in eligible if not case["target_meteg"]
        ]
    }
    patterns = {
        "mik_kol_ma_al8_khal": r"[.-]".join(
            (r"[^^]", r"kh?ol", r"[^.-]+", r"[^.-]+", r"!")
        ),
        "vay_ye_x6_zak": r"[.-]".join((r"vay", r"ye", r".[068]", r"!")),
    }
    for name, present in product(patterns, (False, True)):
        state = "with" if present else "without"
        out[f"{name}_{state}_target_meteg"] = [
            case
            for case in eligible
            if case["target_meteg"] == present
            and re.search(patterns[name], case["transcription"])
        ]
    return out


def facts_from_reading(reading, bcvt, previous=None) -> ChantedWordFacts:
    """Derive only the classifier's temporary facts from a public display pair.

    ``previous`` is the displayed reading before ``reading`` in its own qamats
    sequence, or None at the start of the verse; only its accent vector is kept.
    """
    from phonetic_mam.core import deep_latin as dl
    from phonetic_mam.core import udl_char_classes as cc
    from phonetic_mam.core import vowar_and_accar
    from phonetic_mam.core import separate_accents
    from phonetic_mam.core import bccvecs_that_are_known as knowns

    atoms = reading.syllables()
    stress_atom, stress_syllable = reading.stress_position()
    stress_index = sum(map(len, atoms[:stress_atom])) + stress_syllable
    system = cantsys.get_cantsys_from_is_poetcant(bib_locales.is_poetcant(bcvt))
    _vowels, accents = vowar_and_accar.vowar_and_accar(reading.hebrew)
    _letters, bccvec = separate_accents.get_sepacc(system, accents)
    accent_index = knowns.CS_GET_STRESS_INFO_FROM_BCCVEC[system][bccvec]
    hatafs = {
        dl.VARIKA_WITH_GENERIC_SHEVA,
        dl.VARIKA_WITH_VOCAL_SHEVA,
        dl.XPATAX,
        dl.XQAMATS,
        dl.XSEGOL,
    }
    reduced = {dl.SHEVA_NA, *hatafs}
    long_vowels = {dl.VAV_XOLAM, dl.XOLAM_HASER, dl.TSERE, dl.QAMATS_G, dl.XIRIQ_G}
    gutturals = {dl.ALEF_0MAPIQ_CON, dl.AYIN_0DAG, dl.XET_0DAG, dl.HE_0MAPIQ_CON}
    syllables = []
    for atom in atoms:
        for syllable in atom:
            decoded = syllable["sylrec-udl"]
            nucleus = decoded[1] if len(decoded) > 1 else None
            syllables.append(
                SyllableFacts(
                    onset=decoded[0],
                    reduced=nucleus in reduced,
                    hataf=nucleus in hatafs or hpo.VARIKA in syllable["sylrec-fva"][0],
                    guttural=decoded[0] in gutturals,
                    long_vowel=nucleus in long_vowels,
                    explicitly_closed=decoded[-1] == dl.SHEVA_NAX
                    or decoded[-1] in cc.UNAMB_CONSONANTS,
                    implicitly_closed=bool(syllable.get("sylrec-next-syl-swp1g")),
                    accents=syllable["sylrec-fva"][2],
                )
            )
    previous_bccvec = ()
    if previous is not None:
        _previous_vowels, previous_accents = vowar_and_accar.vowar_and_accar(
            previous.hebrew
        )
        _previous_letters, previous_bccvec = separate_accents.get_sepacc(
            system, previous_accents
        )
    return ChantedWordFacts(
        tuple(syllables),
        stress_index,
        bccvec[accent_index],
        system,
        accents,
        bccvec,
        range(len(bccvec))[accent_index],
        previous_bccvec,
    )


def _previous_readings(verse) -> dict[int, object]:
    """Each displayed reading's predecessor in its own qamats sequence, or None.

    Keyed by the reading's identity, since one verse can display the same chanted
    word twice and equal readings compare equal. An unlabelled reading belongs to
    both qamats sequences and takes its predecessor from the ordinary one, where a
    qamats-dal alternative stands; a qamats-sam alternative follows the samekh
    sequence, whose readings outside the alternatives are the unlabelled ones.
    """
    from phonetic_mam import analysis_reader

    last = {analysis_reader.QAMATS_DAL: None, analysis_reader.QAMATS_SAM: None}
    previous = {}
    for row in verse.rows:
        for branch in row.branches:
            sequences = (branch.qamats,) if branch.qamats else tuple(last)
            for reading in branch.readings:
                previous[id(reading)] = last[sequences[0]]
                for sequence in sequences:
                    last[sequence] = reading
    return previous


def analyze_books(books) -> dict:
    """Analyze canonical public-book views while retaining their row multiplicity."""
    from phonetic_mam import analysis_reader

    ordinary, samekh = [], []
    seen_books = []
    for book_id, verses in books:
        seen_books.append(book_id)
        for (chapter, verse_number), verse in verses.items():
            bcvt = bib_locales.mk_bcvtmam(book_id, chapter, verse_number)
            bcv = bib_locales.short_bcv_of_bcvt(bcvt)
            selected = verse.select(cantillation=analysis_reader.CANT_ALEF)
            previous_readings = _previous_readings(selected)
            for reading in selected.readings():
                facts = facts_from_reading(
                    reading, bcvt, previous_readings[id(reading)]
                )
                try:
                    result = classify(facts)
                except ValueError as error:
                    raise ValueError(f"{bcv} {reading.hebrew!r}: {error}") from error
                if result is None:
                    continue
                case = {
                    "bcv": bcv,
                    "hebrew": reading.hebrew.split(" ")[0],
                    "transcription": reading.transcription,
                    "qamats_variant": reading.qamats,
                    **result,
                }
                population = (
                    samekh if reading.qamats == analysis_reader.QAMATS_SAM else ordinary
                )
                population.append(case)
    if seen_books != list(bib_locales.ALL_BK39_IDS):
        raise ValueError(
            "The pre-stress-meteg survey requires the complete canonical book sequence"
        )
    return {
        "schema": "meteg-before-stress-v1",
        "projection": {
            "cantillation": "cant-alef",
            "ordinary_qamats": "dalet; includes unlabelled ordinary readings",
            "samekh_qamats": "samekh-labelled alternatives only",
            "target": "main part of the grouped syllable two before primary stress",
            "vowel_length": "the established classifier convention, not a new interpretation",
        },
        "ordinary": summarize(ordinary),
        "samekh": summarize(samekh),
        "selections": select_cases(ordinary),
    }


def build_survey() -> dict:
    """Read the closed public release, never a private source or fallback."""
    from phonetic_mam import analysis_reader, release

    release.require_complete_book_set()
    data_dir = paths.phonetic_mam_dir() / "data"
    if not any(data_dir.glob("*.json")):
        raise FileNotFoundError(f"Missing public Phonetic MAM release: {data_dir}")
    return analyze_books(
        (book_id, analysis_reader.read_book(book_id))
        for book_id in bib_locales.ALL_BK39_IDS
    )


def default_json_out_path() -> Path:
    return paths.out_dir() / "accgram" / "meteg-before-stress.json"


def add_args(parser, *, repo_root: Path) -> None:
    del repo_root
    parser.add_argument("--json-out", type=Path, default=default_json_out_path())


def run(args) -> None:
    result = build_survey()
    output = args.json_out
    file_io.json_dump_to_file_path(result, str(output), indent=1)
    print(f"wrote {output}")
