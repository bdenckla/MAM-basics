from __future__ import annotations

from accgram.mam_simple_verse import MAMNativePaseq


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
            return texts_from_token_like_payload(payload["vels"])

        tag = payload.get("tag")
        if tag == "x":
            return []
        if tag is not None and tag not in {"w", "s"}:
            raise ValueError(f"unclassified RTMS XML-ish node tag: {tag!r}")

        text = payload.get("text")
        if isinstance(text, str):
            return [text]

        word = payload.get("word")
        if isinstance(word, str):
            return [word]

        children = payload.get("children")
        if tag in {"w", "s"} and isinstance(children, list):
            return texts_from_token_like_payload(children)

        raise ValueError(
            "unclassified RTMS token-like mapping: "
            f"keys={sorted(str(key) for key in payload)}"
        )

    raise TypeError(f"unclassified RTMS token-like payload: {type(payload).__name__}")
