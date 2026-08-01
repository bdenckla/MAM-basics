from __future__ import annotations

from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hp
from mb_cmn import hebrew_punctuation as hpunc
from mb_diff_mpu.describe_diff import ACCENT_NAMES

_HEBREW_LETTER_START = ord("\u05d0")
_HEBREW_LETTER_END = ord("\u05ea")
_HEBREW_ACCENT_START = ord("\u0591")
# Accents end at U+05AE: U+05AF (MASORA CIRCLE) is an editorial mark, not an
# accent, so it is excluded. Matches mb_cmn.hebrew_accents.ACCENTS_AND_MTG and
# the mb_cmn.hebrew_accent_strip kernel.
_HEBREW_ACCENT_END = ord("\u05ae")

_ACCENTS_WITH_DESCRIPTORS = (
    ha.ATN,
    ha.SEG_A,
    ha.ZAQ_Q,
    ha.ZAQ_G,
    ha.MUN,
    ha.TEV,
    ha.YET,
    ha.TIP,
    ha.REV,
    ha.Z_OR_TSOR,
    ha.GER,
    ha.MAH,
    ha.MER,
    ha.DAR,
    ha.GER_2,
)
ACCENT_TO_DESCRIPTOR = {
    accent: ACCENT_NAMES[accent].replace("-", "_")
    for accent in _ACCENTS_WITH_DESCRIPTORS
}
SIMPLE_ACCENT_DESCRIPTORS = frozenset(ACCENT_TO_DESCRIPTOR.values())
_OVER_ACCENT_TO_PREFIX = {
    ha.ZSH_OR_TSIT: "zarqa_sh_on_",
    ha.PASH: "pashta_on_",
    ha.QOM: "qadma_on_",
}
_NO_DESCRIPTOR_EXCEPTIONS = {
    "טוב֖ה",
    "ישראל֘",
}


def infer_mark_descriptor(
    text: str,
    *,
    u05bd_is_silluq: bool | None,
) -> str | None:
    atoms_with_descriptors: list[list[str]] = []
    current_atom_descriptors: list[str] = []
    current_hebrew_letter: str | None = None

    def _flush_current_atom_descriptors() -> None:
        if current_atom_descriptors:
            atoms_with_descriptors.append(list(current_atom_descriptors))
            current_atom_descriptors.clear()

    for ch in text:
        cp = ord(ch)

        if ch.isspace():
            _flush_current_atom_descriptors()
            current_hebrew_letter = None
            continue

        if _HEBREW_LETTER_START <= cp <= _HEBREW_LETTER_END:
            current_hebrew_letter = ch
            continue

        if ch == hpunc.MAQ:
            current_atom_descriptors.append("maqaf")
            continue

        if ch == hpunc.SOPA:
            current_atom_descriptors.append("sof_pasuq")
            continue

        if ch == hpunc.PASOLEG:
            current_atom_descriptors.append("pasoleg")
            continue

        if ch == hp.MTGOSLQ:
            current_atom_descriptors.append(
                "silluq" if u05bd_is_silluq is True else "meteg"
            )
            continue

        if not (_HEBREW_ACCENT_START <= cp <= _HEBREW_ACCENT_END):
            # Ignore vowels and ordinary points.
            continue

        descriptor = ACCENT_TO_DESCRIPTOR.get(ch)
        if descriptor is not None:
            current_atom_descriptors.append(descriptor)
            continue

        prefix = _OVER_ACCENT_TO_PREFIX.get(ch)
        if prefix is not None:
            assert (
                current_hebrew_letter is not None
            ), f"Over-accent must follow a Hebrew letter: token={text!r} accent={ch!r}"
            current_atom_descriptors.append(f"{prefix}{current_hebrew_letter}")
            continue

        assert text in _NO_DESCRIPTOR_EXCEPTIONS, (
            "No descriptor for accent token unless explicitly allowlisted: "
            f"token={text!r} accent={ch!r}"
        )
        return None

    _flush_current_atom_descriptors()

    if not atoms_with_descriptors:
        return "no_accent"

    atom_descriptions = [
        "-".join(atom_descriptors) for atom_descriptors in atoms_with_descriptors
    ]
    return " ".join(atom_descriptions)
