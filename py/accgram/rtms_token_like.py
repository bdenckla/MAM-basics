from __future__ import annotations

from accgram.mam_simple_verse import MAMNativePaseq


def text_from_one_token_like(token: object) -> str:
    """Return one selected token's text, rejecting multi-token containers."""
    texts = texts_from_token_like_payload(token)
    if len(texts) > 1:
        raise ValueError(f"expected one token-like value, got {len(texts)}: {token!r}")
    return texts[0] if texts else ""


def texts_from_token_like_payload(payload: object) -> list[str]:
    """Project the historical RTMS text while rejecting unfamiliar shapes.

    Ben deferred the choice of a selected Scripture stream in
    ``doc/PLAN-deferred-template-projection-decisions.md``.  Until that decision,
    this function explicitly preserves the behavior on main: every declared verse
    stream contributes, a mapping with direct ``text`` or ``word`` contributes that
    field, and metadata contributes nothing.  MAM's structural paseq/legarmeh marker
    contributes nothing.  An unfamiliar shape raises.
    """

    if isinstance(payload, str):
        return [payload]

    if isinstance(payload, MAMNativePaseq):
        return []

    if isinstance(payload, list):
        out: list[str] = []
        for item in payload:
            out.extend(texts_from_token_like_payload(item))
        return out

    if isinstance(payload, dict):
        if "vels" in payload:
            unexpected = set(payload) - {
                "vels",
                "vels_cant_alef",
                "vels_cant_bet",
                "bcv",
            }
            if unexpected:
                raise ValueError(
                    f"unclassified RTMS verse fields: {sorted(unexpected)!r}"
                )
            out: list[str] = []
            for key, value in payload.items():
                if key in {"vels", "vels_cant_alef", "vels_cant_bet"}:
                    out.extend(texts_from_token_like_payload(value))
            return out

        text = payload.get("text")
        if isinstance(text, str):
            unexpected = set(payload) - {"text", "note", "notes", "tag"}
            if unexpected:
                raise ValueError(
                    f"unclassified RTMS text fields: {sorted(unexpected)!r}"
                )
            tag = payload.get("tag")
            if tag not in {None, "x"}:
                raise ValueError(f"unclassified RTMS XML-ish node tag: {tag!r}")
            return [text]

        word = payload.get("word")
        if isinstance(word, str):
            unexpected = set(payload) - {"word", "note", "notes"}
            if unexpected:
                raise ValueError(
                    f"unclassified RTMS word fields: {sorted(unexpected)!r}"
                )
            return [word]

        raise ValueError(
            "unclassified RTMS token-like mapping: "
            f"keys={sorted(str(key) for key in payload)}"
        )

    raise TypeError(f"unclassified RTMS token-like payload: {type(payload).__name__}")
