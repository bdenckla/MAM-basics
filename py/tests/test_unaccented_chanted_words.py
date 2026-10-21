"""Differential check: the chanted words read off a WLC 4.22 mark body, against the -kq-u verse.

``accgram.unaccented_chanted_words`` reads chanted words off the mark body that
``uni_to_marks.verse_to_marks`` writes, because the mark body is all that most verdict paths
have.  The body is a flattening of the ``-kq-u`` verse: a ketiv and its qere are runs of one
fragment, and the ketiv, a petuxah or setumah and a nun inversum are runs that hold no word that
is read.  This test reads every WLC 4.22 verse a second way, from its verse elements, and
requires the two readings to agree on three things:

1. The atoms the body reads, in order, are the words ``prose_run._verse_display_words`` yields,
   which is what lets ``prose_run`` name a chanted word with no accent by ``read_atoms``.
2. The chanted words are the same chanted words, each qere word apart: the body's runs and maqaf
   marks on one side, the maqaf each word of the verse ends with on the other.  A qere of two
   chanted words is two chanted words on both sides, which the body did not say until
   ``uni_to_marks._kq_to_marks`` joined a qere's words as verse elements (2026-10-20).
3. The chanted words with no accent, the silluq's excepted, are the same chanted words.

The oracle here shares no code with the module: it groups the verse's words by the maqaf each
word ends with, and treats a ketiv, a petuxah or setumah and a nun inversum as no words at all.
Like the module, it lets the maqaf before a ketiv with no qere join its word to the next word
that is read (rule 3; Ben's decision of 2026-10-20).
"""

from __future__ import annotations

from accgram import prose_run
from accgram import rtms_data
from accgram import uni_to_marks
from accgram import unaccented_chanted_words as ucw
from mb_cmn import paths

_MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
_SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"


def test_body_reading_agrees_with_the_kq_u_verses():
    index = rtms_data.load_wlc422_index(paths.out_dir() / "wlc422-kq-u")
    assert index, "no WLC 4.22 verses were loaded"
    misaligned: list[str] = []
    disagreeing: list[str] = []
    for bcv, verse in index.items():
        body = uni_to_marks.verse_to_marks(verse)
        words = _read_words(verse["vels"])
        display = list(prose_run._verse_display_words(verse))
        atoms = [atom for cw in ucw.chanted_words(body) for atom in cw.atoms]
        expected = [uni_to_marks.word_to_marks(w).removesuffix("-") for w in display]
        if display != words or [_bare(a.marks) for a in atoms] != expected:
            misaligned.append(bcv)
            continue
        chanted = [
            tuple(words[atom.read_index] for atom in cw.atoms)
            for cw in ucw.chanted_words(body)
        ]
        oracle_chanted = _oracle_chanted_words(words)
        if chanted != oracle_chanted:
            disagreeing.append(
                f"{bcv}: chanted words, body {chanted}, verse {oracle_chanted}"
            )
            continue
        found = [
            tuple(words[atom.read_index] for atom in cw.atoms)
            for cw in ucw.unaccented_chanted_words(body)
        ]
        oracle_unaccented = _oracle_unaccented(oracle_chanted)
        if found != oracle_unaccented:
            disagreeing.append(
                f"{bcv}: no accent, body {found}, verse {oracle_unaccented}"
            )
    assert (
        not misaligned
    ), f"read atoms out of step with the verse's words: {misaligned}"
    assert not disagreeing, "\n".join(disagreeing)


def _has_accent(word: str) -> bool:
    return any(
        "\N{HEBREW ACCENT ETNAHTA}" <= ch <= "\N{HEBREW ACCENT ZINOR}" for ch in word
    )


def _word_of(vel: object) -> str:
    if isinstance(vel, str):
        return vel
    if isinstance(vel, dict) and isinstance(vel.get("word"), str):
        return vel["word"]
    raise ValueError(f"no word in {vel!r}")


def _read_words(vels: list) -> list[str]:
    """The verse's words in reading order: its plain words and each word of each qere."""
    out: list[str] = []
    for vel in vels:
        if isinstance(vel, dict) and "sam_pe_inun" in vel:
            continue
        if isinstance(vel, dict) and "kq" in vel:
            out.extend(_word_of(qere_vel) for qere_vel in vel["kq"][1])
            continue
        out.append(_word_of(vel))
    return out


def _oracle_chanted_words(words: list[str]) -> list[tuple[str, ...]]:
    """The verse's chanted words, each as its words: a word ending in a maqaf joins the next."""
    chanted: list[tuple[str, ...]] = []
    current: list[str] = []
    for word in words:
        current.append(word)
        if not word.endswith(_MAQAF):
            chanted.append(tuple(current))
            current = []
    if current:
        chanted.append(tuple(current))
    return chanted


def _oracle_unaccented(chanted: list[tuple[str, ...]]) -> list[tuple[str, ...]]:
    """Those of ``chanted`` with no accent, the silluq's excepted."""
    silluq = next(
        (i for i, cw in enumerate(chanted) if any(_SOF_PASUQ in w for w in cw)),
        len(chanted) - 1,
    )
    return [
        cw
        for i, cw in enumerate(chanted)
        if i != silluq and not any(_has_accent(w) for w in cw)
    ]


def _bare(atom_marks: str) -> str:
    """An atom's marks without the qere's ``**`` and without its note markers."""
    return atom_marks.removeprefix("**").partition("]")[0]
