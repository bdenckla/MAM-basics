from __future__ import annotations


def texts_from_token_like_payload(payload: object) -> list[str]:
    if isinstance(payload, str):
        return [payload]

    if isinstance(payload, list):
        out: list[str] = []
        for item in payload:
            out.extend(texts_from_token_like_payload(item))
        return out

    if isinstance(payload, dict):
        text = payload.get("text")
        if isinstance(text, str):
            return [text]

        word = payload.get("word")
        if isinstance(word, str):
            return [word]

        out: list[str] = []
        for child in payload.values():
            out.extend(texts_from_token_like_payload(child))
        return out

    return []
