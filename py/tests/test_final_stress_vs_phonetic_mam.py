"""``final_stress`` against Phonetic MAM: a differential check with an independent oracle.

``accgram.final_stress`` decides whether a chanted word is stressed on its last syllable by
counting nuclei and locating one syllable, the last. Phonetic MAM's displayed transcription
records the result of a separate stress model -- full syllabification plus a hand-built table
saying which accent of a vector bears the stress -- run over the whole Tanakh. So the two are
independent derivations of one fact, which is the shape of test this repo keeps
(``doc/agent-planning-principles.md`` §"Generated Outputs Are the Tests").  Issue wlc-utils#48 calls
consuming Phonetic MAM's outputs its second path; this is that path, and it is why the rule in
``final_stress`` is measured against the engine rather than standing in for it.

WHAT IS CHECKED: every chanted word of MAM's PROSE verses the maqaf-non-final-accents survey gives
a final-stress verdict for -- the simple two-accent chanted words and the concentrators, minus the
ones the survey excludes, minus the ones whose last mark is written at the chanted word's edge and
so says nothing about stress.  MAM, because Phonetic MAM is MAM; prose, because the page the
measurement is for is about prose verses and because a poetic chanted word's atoms really are
grouped differently on the two sides -- MAM has a gray maqaf in 113 places where Phonetic MAM keeps
two chanted words, and those 113 are nearly the whole of what will not join anywhere in MAM's
Tanakh.  The rest of it, 11 more (issue wlc-utils#91), is outside this test's reach for reasons of its own:
8 dually-cantillated chanted words in the two Decalogues, whose ``cant-combined`` projection is
neither strand; Deuteronomy 32:6, where MAM's large ה stands apart from לְיְהֹוָה֙ and Phonetic MAM
has one entry for the two atoms; and 2 Chronicles 25:17, where Phonetic MAM has לְךָ֖ against the
qere לְכָ֖ה that MAM-simple and WLC 4.22 both have, which is a difference in the text rather than
in the grouping.  The
scan is rerun here rather than read out of the survey's JSON, which keeps counts and not words --
and rerun over MAM's own versification, for which see ``_measured``.

THE ORACLE'S FORM is the tracked Phonetic-MAM display release. The analysis reader
selects every displayed Hebrew branch and the corresponding Sephardic transcription.
Its ASCII spelling retains the visible syllable boundaries and marked primary stress.
No analysis annotation or source audit field is part of this input. The public MAM spelling
is matched through the generic perpetual-qere rules when its displayed reading differs.

A DUAL-CANTILLATION chanted word has one entry per strand and the two can disagree -- Exodus 20's
lo-yihye is stressed differently in each -- so a verdict matching either strand is agreement.  The
survey reads one strand of MAM-simple, and which one is not a fact this test is about.

A word Phonetic MAM has no entry for FAILS, and none does. The complete public
release is required in every environment, including cloud sessions.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_final_stress_vs_phonetic_mam.py
"""

from __future__ import annotations

import re
from collections import defaultdict
from functools import lru_cache

from accgram import final_stress as fs
from accgram import mam_simple_verse
from accgram import maqaf_nonfinal_accents as mpa
from accgram import prose_filter
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id

from mb_cmn import paths
from phonetic_mam import analysis_reader
from phonetic_mam.core import qere_from_implicit_kq

# What a join key drops: the accents (U+0591..U+05AE), masora circle (U+05AF), meteg (U+05BD),
# rafe (U+05BF), the punctuation that can sit inside a chanted word (paseq U+05C0 and sof pasuq
# U+05C3), the two puncta U+05C4..U+05C5, and the two invisibles (CGJ U+034F and varika U+FB1E).
# What is left is letters, points and maqaf, which is what the two sides have to agree on: they are two
# renderings of MAM rather than one file, and the accents are what this test COMPARES rather than
# what it matches on.  Written as numeric escapes because a character class wants range endpoints
# and because a bare combining mark in a literal is unreadable and un-diffable.
_NOT_IN_THE_JOIN_KEY = re.compile(
    "[\u0591-\u05af\u05bd\u05bf\u05c0\u05c3-\u05c5\u034f\ufb1e]"
)

# What separates one syllable of a ``jta`` form from the next: ``.`` within an atom and ``-``
# between the atoms of a maqaf compound.
_SYLLABLE_BREAK = re.compile(r"[.\-]")


def _mam_join_key(word: str) -> str:
    return _NOT_IN_THE_JOIN_KEY.sub("", word)


def _stress_is_final(jta: str, word: str) -> bool:
    """Whether Phonetic MAM has this chanted word stressed on its last syllable.

    Nothing after the ``!`` but the stressed syllable is what final stress looks like -- except
    that Phonetic MAM has a FURTIVE PATAX as a syllable of its own, where ``final_stress`` counts
    no nucleus for it: מזבח is ``miz.!bE.ax`` there and stressed on its last syllable here.  So one
    trailing syllable is what final stress looks like for those, and the difference is one of
    notation, held steady rather than read as a disagreement about the stress.
    """
    assert "!" in jta, f"no stressed syllable marked: {jta!r}"
    _before, _bang, tail = jta.partition("!")
    expected = 1 if fs.ends_in_furtive_patax(word) else 0
    return len(_SYLLABLE_BREAK.findall(tail)) == expected


@lru_cache(maxsize=None)
def _book(bb: str) -> dict[tuple[int, int], dict[str, frozenset]]:
    """Index the independently displayed stress for every displayed branch."""
    per_verse = {}
    for key, verse in analysis_reader.read_book(wlc_bb_to_bk39id(bb)).items():
        verdicts = defaultdict(set)
        for reading in verse.readings():
            verdicts[_mam_join_key(reading.hebrew)].add(
                _stress_is_final(reading.transcription, reading.hebrew)
            )
        per_verse[key] = {key: frozenset(values) for key, values in verdicts.items()}
    return per_verse


def _oracle(bcv: str, word: str) -> frozenset:
    bb, chnu, vrnu = mpa.split_bcv(bcv)
    verdicts = _book(bb).get((chnu, vrnu), {})
    direct = verdicts.get(_mam_join_key(word), frozenset())
    qere = qere_from_implicit_kq.get_qere_from_implicit_kq(word)
    return direct | verdicts.get(_mam_join_key(qere), frozenset())


def _measured() -> list[dict]:
    """The MAM prose chanted words a final-stress verdict can be had for, in MAM's own numbering.

    MAM'S NATIVE VERSIFICATION, not the BHS one the survey reads.  MAM-simple ships all three, and
    Phonetic MAM numbers its verses MAM's way, so reading ``json-vtrad-mam`` here makes the verse
    keys line up on both sides -- where the BHS flavour would have Joshua 21, 1 Samuel 24 and
    Jeremiah 31 looking like a difference between two texts when it is a difference between two
    numberings of one.  The survey itself is right to read BHS: it is keyed to WLC's refs, and all
    three of its corpora have to number alike.

    What is scanned is therefore the same text and the same chanted words, differently grouped
    into verses.  The grouping reaches one thing this test is about: which chanted word is the
    verse's last, and so where a U+05BD is the silluq.  MAM's own numbering is the right answer to
    that for a MAM text.
    """
    mam_dir = paths.require_mam_simple_vtrad_mam_dir()
    words = mpa.mam_words(mam_simple_verse.mam_simple_refs(mam_dir), mam_dir)
    _hits, _verses, _compounds, simple, concentrators = mpa.scan(
        words, prose_filter.should_keep_line, prose=True
    )
    return [
        record
        for record in simple + concentrators
        if record["excluded"] is None and record["final_stress"] is not None
    ]


@lru_cache(maxsize=None)
def _cases() -> tuple[tuple[str, str, bool], ...]:
    return tuple(
        (record["bcv"], record["word"], record["final_stress"])
        for record in _measured()
    )


def test_every_measured_chanted_word_has_a_phonetic_mam_entry():
    """The join itself, checked before the verdicts, so a text mismatch reads as one.

    EXCEPTIONLESS, and it took issue wlc-utils#91 to make it so.  One chanted word was pinned here
    until then -- Exodus 17:16's one-atom כֵּ֣סְיָ֔הּ, read as the two texts dividing two atoms
    differently.  They do not.  MAM's running text there is the two-atom כֵּ֣ס יָ֔הּ that
    Phonetic MAM and WLC 4.22 and UXLC all have, and the one-atom form is a SPECIMEN QUOTED
    IN A MAM EDITORIAL NOTE, of what the Aleppo Codex had, which ``mam_simple_verse`` put
    into the stream as verse text for want of a case for MAM-simple's ``sdt-note``.  It was
    alone there because it was the only note specimen with TWO accents, and so the only one
    a survey of two-accent chanted words could reach.
    """
    assert _cases(), "no chanted word was measured at all"
    unjoinable = [
        f"{bcv} {word}" for bcv, word, _ours in _cases() if not _oracle(bcv, word)
    ]
    assert not unjoinable, (
        f"{len(unjoinable)} of {len(_cases())} chanted words have no Phonetic MAM entry: "
        + ", ".join(unjoinable[:20])
    )


def test_final_stress_agrees_with_phonetic_mam():
    disagreements = [
        f"{bcv} {word}: final_stress {ours}, Phonetic MAM {sorted(_oracle(bcv, word))}"
        for bcv, word, ours in _cases()
        if _oracle(bcv, word) and ours not in _oracle(bcv, word)
    ]
    assert (
        not disagreements
    ), f"{len(disagreements)} of {len(_cases())} disagree: " + "; ".join(
        disagreements[:20]
    )
