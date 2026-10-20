"""Differential check: the chanted words read off a WLC 4.22 mark body, against the -kq-u verse.

``accgram.unaccented_chanted_words`` reads chanted words off the mark body that
``uni_to_marks.verse_to_marks`` writes, because the mark body is all that most verdict paths
have.  The body is a lossy flattening of the ``-kq-u`` verse: a ketiv and its qere share one
fragment, and the words of a qere are joined there by maqaf marks whether or not they are a
compound.  This test reads every WLC 4.22 verse a second way, from its verse elements, which
keep each qere word apart, and requires the two readings to agree on two things:

1. The atoms the body reads, in order, are the words ``prose_run._verse_display_words`` yields,
   which is what lets ``prose_run`` name a chanted word with no accent by ``read_atoms``.
2. The chanted words with no accent are the same chanted words.  This is where the qere limit
   in the module docstring would show, if it ever changed a result.

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
        found = [
            tuple(words[atom.read_index] for atom in cw.atoms)
            for cw in ucw.unaccented_chanted_words(body)
        ]
        if found != _oracle(words):
            disagreeing.append(f"{bcv}: body {found}, verse {_oracle(words)}")
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


def _oracle(words: list[str]) -> list[tuple[str, ...]]:
    """The verse's chanted words with no accent, each as its words, the silluq's excepted."""
    chanted: list[tuple[str, ...]] = []
    current: list[str] = []
    for word in words:
        current.append(word)
        if not word.endswith(_MAQAF):
            chanted.append(tuple(current))
            current = []
    if current:
        chanted.append(tuple(current))
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
