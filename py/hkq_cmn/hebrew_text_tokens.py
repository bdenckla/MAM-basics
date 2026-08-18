from __future__ import annotations

import re

HEBREW_TOKEN_CHAR_CLASS = (
    "\u034f"
    "\u0591-\u05bd"
    "\u05bf"
    "\u05c1-\u05c2"
    "\u05c4-\u05c5"
    "\u05c7"
    "\u05d0-\u05ea"
    "\u05f0-\u05f2"
    "\u200c-\u200d"
    "\ufb1d-\ufb4f"
)
HEBREW_TOKEN_PATTERN = re.compile(f"[{HEBREW_TOKEN_CHAR_CLASS}]+")
IGNORABLE_ACCENTS_METEG_AND_JOINERS_RE = re.compile(
    "[" "\u034f" "\u0591-\u05af" "\u05bd" "\u200c-\u200d" "]+"
)


def find_hebrew_tokens(text: str) -> list[str]:
    return HEBREW_TOKEN_PATTERN.findall(text)


def strip_ignorable_token_marks(text: str) -> str:
    return IGNORABLE_ACCENTS_METEG_AND_JOINERS_RE.sub("", text)
