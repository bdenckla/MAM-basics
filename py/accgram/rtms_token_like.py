from __future__ import annotations

from accgram.mam_simple_verse import MAMNativePaseq


def text_from_one_token_like(token: object) -> str:
    """Return one selected token's text, rejecting multi-token containers."""
    texts = texts_from_token_like_payload(token)
    if len(texts) > 1:
        raise ValueError(f"expected one token-like value, got {len(texts)}: {token!r}")
    return texts[0] if texts else ""


def texts_from_token_like_payload(payload: object) -> list[str]:
    """Project a selected Scripture token stream out of the RTMS input shapes.

    WLC and MAM verse records contribute only ``vels``.  UXLC word and separator
    nodes contribute their direct text, while ``x`` note nodes and node metadata do
    not.  MAM's structural paseq/legarmeh marker is punctuation rather than word
    text.  Each recognized container names the child that belongs to the projection;
    an unfamiliar shape raises instead of recursively treating every value as text.
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
            return texts_from_token_like_payload(payload["vels"])

        tag = payload.get("tag")
        if tag == "x":
            return []
        if tag is not None:
            raise ValueError(f"unclassified RTMS XML-ish node tag: {tag!r}")

        keys = set(payload)
        if keys in ({"text"}, {"text", "note"}, {"text", "notes"}):
            text = payload["text"]
            if isinstance(text, str):
                return [text]
        if keys in ({"word"}, {"word", "notes"}):
            word = payload["word"]
            if isinstance(word, str):
                return [word]

        raise ValueError(
            "unclassified RTMS token-like mapping: "
            f"keys={sorted(str(key) for key in payload)}"
        )

    raise TypeError(f"unclassified RTMS token-like payload: {type(payload).__name__}")
