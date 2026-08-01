from __future__ import annotations

from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hpo
from mb_cmn import uni_heb


def _rm_parens_and_underscore(text: str) -> str:
    return text.translate({ord(ch): None for ch in "()_"})


_ACC_ABBREV_BY_CHAR: dict[str, str] = {
    char: _rm_parens_and_underscore(abbrev)
    for char, abbrev in uni_heb._HE_AND_NONHE_ACC_PAIRS
}

_TOKEN_TO_ACC_CHAR: dict[str, str] = {
    "silluq": hpo.MTGOSLQ,
    "atnax": ha.ATN,
    "segolta": ha.SEG_A,
    "zaqef": ha.ZAQ_Q,
    "zaqefgadol": ha.ZAQ_G,
    "tipexa": ha.TIP,
    "revia": ha.REV,
    "pashta": ha.PASH,
    "yetiv": ha.YET,
    "tevir": ha.TEV,
    "geresh": ha.GER,
    "gershayim": ha.GER_2,
    "munax": ha.MUN,
    "merkha": ha.MER,
    "mahapakh": ha.MAH,
    "darga": ha.DAR,
    "qadma": ha.QOM,
    "azla": ha.QOM,
    "telishagedola": ha.TEL_G,
    "big_telisha": ha.TEL_G,
    "pazer": ha.PAZ,
    "telishaqetanna": ha.TEL_Q,
    "zarqa": ha.Z_OR_TSOR,
}

# Keep vendored mb_cmn mappings untouched; accgram display abbreviations that
# are repo-specific belong here as explicit overrides.
_TOKEN_ABBREV_OVERRIDES: dict[str, str] = {
    "silluq": "slq",
    "zarqa": "zar",
}

_TOKEN_ABBREV: dict[str, str] = {
    token: _ACC_ABBREV_BY_CHAR[accent_char]
    for token, accent_char in _TOKEN_TO_ACC_CHAR.items()
}
_TOKEN_ABBREV.update(_TOKEN_ABBREV_OVERRIDES)
# This appears in parse output but is not a standalone Unicode accent name.
_TOKEN_ABBREV["legarmeh"] = "lgm"

# Accent tokens whose own name contains "_" (currently just "big_telisha").  A
# branch label is tokenized on "_", so these must be re-merged greedily, longest
# first, before lookup.
_COMPOUND_TOKENS: list[str] = sorted(
    (token for token in _TOKEN_ABBREV if "_" in token),
    key=lambda token: token.count("_"),
    reverse=True,
)


def _split_label_tokens(base_label: str) -> list[str]:
    words = [word for word in base_label.split("_") if word]
    tokens: list[str] = []
    i = 0
    while i < len(words):
        for compound in _COMPOUND_TOKENS:
            n = compound.count("_") + 1
            if words[i : i + n] == compound.split("_"):
                tokens.append(compound)
                i += n
                break
        else:
            tokens.append(words[i])
            i += 1
    return tokens


def _abbreviate_acc_token(token: str) -> str | None:
    """Abbreviate one accent token, handling `!`-fused unitary tokens such as
    "mahapakh!qadma" -> "mah!qom". Returns None if any `!`-separated part is
    not a known accent token."""
    parts = token.split("!")
    if all(part in _TOKEN_ABBREV for part in parts):
        return "!".join(_TOKEN_ABBREV[part] for part in parts)
    return None


def abbreviate_branch_label(label: str) -> str:
    base_label = label.strip()
    suffix = ""
    if base_label.endswith("_clause"):
        base_label = base_label[: -len("_clause")]
        suffix = "c"
    elif base_label.endswith("_phrase"):
        base_label = base_label[: -len("_phrase")]
        suffix = "p"

    tokens = _split_label_tokens(base_label)
    abbrevs = [_abbreviate_acc_token(token) for token in tokens]
    if tokens and all(abbrev is not None for abbrev in abbrevs):
        short_base = "".join(abbrevs)
    elif tokens:
        short_base = "_".join(
            abbrev if abbrev is not None else token
            for abbrev, token in zip(abbrevs, tokens)
        )
    else:
        short_base = base_label

    return f"{short_base}{suffix}"


def abbreviate_leaf_text(text: str) -> str:
    stripped = text.strip()
    if stripped == "ERROR":
        return "ERROR"

    tokens = [token for token in stripped.split() if token]
    if not tokens:
        return stripped

    return " ".join(_abbreviate_acc_token(token) or token for token in tokens)
