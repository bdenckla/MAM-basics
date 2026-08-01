from __future__ import annotations

import json

from mb_cmn import my_diffs


def diff_wlc_uxlc(
    wlc422_verse: object,
    uxlc_nodes: object,
) -> list[dict[str, object]] | dict[str, object] | None:
    if not isinstance(wlc422_verse, dict) or not isinstance(uxlc_nodes, list):
        return None

    wlc_vels = wlc422_verse.get("vels")
    if not isinstance(wlc_vels, list):
        return None

    wlc_keys = [_diff_key(token) for token in wlc_vels]
    uxlc_keys = [_diff_key(token) for token in uxlc_nodes]
    diff_pairs = my_diffs.get(wlc_keys, uxlc_keys, outa=wlc_vels, outb=uxlc_nodes)
    rendered = [_render_diff_pair(left, right) for left, right in diff_pairs]
    if len(rendered) == 1:
        return rendered[0]
    return rendered


def _render_diff_pair(left: list[object], right: list[object]) -> dict[str, object]:
    notes = _wlc_notes_only_delta(left, right)
    if notes is not None:
        return {"wlc_adds_notes": notes}

    note = _uxlc_note_only_delta(left, right)
    if note is not None:
        return {"uxlc_adds_note": note}

    return {
        "wlc422": _collapse_singleton_list(left),
        "uxlc": _collapse_singleton_list(right),
    }


def _collapse_singleton_list(tokens: list[object]) -> object:
    if len(tokens) == 1:
        return tokens[0]
    return tokens


def _wlc_notes_only_delta(left: list[object], right: list[object]) -> object | None:
    if len(left) != 1 or len(right) != 1:
        return None

    left_token = left[0]
    right_token = right[0]
    if not isinstance(left_token, dict) or not isinstance(right_token, str):
        return None

    if set(left_token.keys()) != {"word", "notes"}:
        return None

    word = left_token.get("word")
    if not isinstance(word, str) or word != right_token:
        return None

    return left_token.get("notes")


def _uxlc_note_only_delta(left: list[object], right: list[object]) -> object | None:
    if len(left) != 1 or len(right) != 1:
        return None

    left_token = left[0]
    right_token = right[0]
    if not isinstance(left_token, str) or not isinstance(right_token, dict):
        return None

    if set(right_token.keys()) != {"text", "note"}:
        return None

    text = right_token.get("text")
    if not isinstance(text, str) or text != left_token:
        return None

    return right_token.get("note")


def _diff_key(token: object) -> str:
    if isinstance(token, str):
        return token
    return json.dumps(token, ensure_ascii=False, sort_keys=True)
