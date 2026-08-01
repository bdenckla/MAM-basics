from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from accgram import rtms_focus_diff_expand
from accgram import rtms_focus_highlight
from accgram.hebrew_verse_sanitize import sanitize_verse_text_payload
from accgram import rtms_meteg_witness
from accgram.mam_simple_diff import diff_wlc_mam
from accgram.mam_simple_verse import load_mam_simple_for_refs
from accgram.wlc_uxlc_diff import diff_wlc_uxlc
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id
from py_uxlc import my_uxlc

from accgram import rtms_rows

import wlc_paths

_DIFF_NOTE_KEYS = {"note", "notes"}
_IGNORED_WLC_MAM_DIFF_TOKEN_PAIRS: set[tuple[tuple[str, ...], tuple[str, ...]]] = {
    (("אחר֑יש",), ("אחר֑ש",)),
    (("רב־", "שק֨ה"), ("רבשק֨ה",)),
}


def default_wlc422_kq_u_dir(repo_root: Path) -> Path:
    """Directory of the WLC 4.22 ketiv/qere Unicode ``1verses_*.json`` files."""
    return wlc_paths.out_dir() / "wlc422-kq-u"


def load_wlc422_index(wlc422_kq_u_dir: Path) -> dict[str, dict[str, object]]:
    """Public WLC 4.22 verse index keyed by compact bcv (e.g. "ps31:20")."""
    return _load_wlc422_index(wlc422_kq_u_dir)


def prepare_wlc422_verse_for_render(verse: dict[str, object]) -> dict[str, object]:
    """Interpolate qere + sanitize a raw WLC 4.22 verse for display, the same
    way build_enriched_row does before rendering the pointed-Hebrew paragraph.

    (The meteg-witness pass build_enriched_row also runs feeds the prose SAT
    table, not the plain verse paragraph, so it is omitted here.)
    """
    verse = _interpolate_wlc422_kq_qere(verse)
    verse = sanitize_verse_text_payload(verse)
    if isinstance(verse, dict):
        verse.pop("bcv", None)
    return verse


def verse_unicode_text(
    wlc_index: dict[str, dict[str, object]], bb: str, chnu: int, vrnu: int
) -> str:
    """The verse's normalized pointed-Hebrew text (qere interpolated), or "" if
    the verse is absent from the ``-kq-u`` index.

    The single source for the pointed-Hebrew rendering of a verse: the ungrammatical
    ``content`` field (classify) and the per-verse ``input.unicode`` field of the
    prose JSON outputs (prose_run, issue #20) both draw from it.
    """
    bcv = rtms_rows.to_compact_bcv(bb, chnu, vrnu)
    verse = wlc_index.get(bcv)
    if not isinstance(verse, dict):
        return ""
    prepared = prepare_wlc422_verse_for_render(verse)
    return rtms_focus_diff_expand.normalized_wlc_verse_text_from_payload(prepared)


def load_source_indexes(
    *,
    wlc422_kq_u_dir: Path,
    uxlc_dir: Path,
    mam_simple_dir: Path,
    refs_by_book: dict[str, set[tuple[int, int]]],
) -> tuple[
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
]:
    wlc422_by_bcv = _load_wlc422_index(wlc422_kq_u_dir)
    uxlc_by_bcv = _load_uxlc_for_refs(uxlc_dir, refs_by_book)
    mam_simple_by_bcv = load_mam_simple_for_refs(mam_simple_dir, refs_by_book)
    return wlc422_by_bcv, uxlc_by_bcv, mam_simple_by_bcv


def build_enriched_row(
    *,
    row: dict[str, object],
    bcv: str,
    ref: str,
    wlc422_by_bcv: dict[str, dict[str, object]],
    uxlc_by_bcv: dict[str, dict[str, object]],
    mam_simple_by_bcv: dict[str, dict[str, object]],
    wlc422_kq_u_dir: Path,
    uxlc_dir: Path,
    mam_simple_dir: Path,
    wlc_focus: str | None,
) -> tuple[dict[str, object], object]:
    wlc422_verse = wlc422_by_bcv.get(bcv)
    if wlc422_verse is None:
        raise ValueError(
            f"Missing wlc422-kq-u verse for {ref} ({bcv}) in {wlc422_kq_u_dir}"
        )

    wlc422_verse = _interpolate_wlc422_kq_qere(wlc422_verse)
    wlc422_verse_meteg_witness = sanitize_verse_text_payload(
        wlc422_verse,
        preserve_all_meteg=True,
    )
    wlc422_verse = sanitize_verse_text_payload(wlc422_verse)
    if isinstance(wlc422_verse, dict):
        wlc422_verse.pop("bcv", None)

    _validate_unique_wlc_focus_in_wlc_verse(
        ref=ref,
        wlc422_kq_u_verse=wlc422_verse,
        wlc_focus=wlc_focus,
    )

    uxlc_info = uxlc_by_bcv.get(bcv)
    if uxlc_info is None:
        raise ValueError(f"Missing UXLC verse for {ref} ({bcv}) in {uxlc_dir}")

    uxlc_nodes = uxlc_info["nodes"]
    uxlc_nodes_meteg_witness = sanitize_verse_text_payload(
        uxlc_nodes,
        preserve_all_meteg=True,
    )
    uxlc_nodes = sanitize_verse_text_payload(uxlc_nodes)

    mam_simple_info = mam_simple_by_bcv.get(bcv)
    if mam_simple_info is None:
        raise ValueError(
            f"Missing MAM-simple verse for {ref} ({bcv}) in {mam_simple_dir}"
        )

    mam_simple_verse = mam_simple_info["mam_simple_verse"]
    mam_simple_verse_meteg_witness = sanitize_verse_text_payload(
        mam_simple_verse,
        remove_mam_stress_helper_duplicates=True,
        preserve_all_meteg=True,
    )
    mam_simple_verse = sanitize_verse_text_payload(
        mam_simple_verse,
        remove_mam_stress_helper_duplicates=True,
    )

    wlc422_for_diff = _normalize_payload_for_diff_ignoring_notes(wlc422_verse)
    uxlc_for_diff = _normalize_payload_for_diff_ignoring_notes(uxlc_nodes)
    mam_simple_for_diff = _normalize_payload_for_diff_ignoring_notes(mam_simple_verse)
    diff_wlc_uxlc_for_checks = diff_wlc_uxlc(wlc422_verse, uxlc_nodes)
    diff_wlc_uxlc_for_output = diff_wlc_uxlc(wlc422_for_diff, uxlc_for_diff)
    diff_wlc_mam_for_output = diff_wlc_mam(wlc422_for_diff, mam_simple_for_diff)

    diff_wlc_uxlc_for_output = _expand_subset_diff_to_wlc_focus(
        diff_wlc_uxlc_for_output,
        wlc_focus=wlc_focus,
        rhs_key="uxlc",
    )
    diff_wlc_mam_for_output = _expand_subset_diff_to_wlc_focus(
        diff_wlc_mam_for_output,
        wlc_focus=wlc_focus,
        rhs_key="mam_simple",
    )
    diff_wlc_mam_for_output = _ignore_targeted_wlc_mam_diffs(diff_wlc_mam_for_output)

    enriched_row: dict[str, object] = {
        **row,
        "wlc422_kq_u_verse": wlc422_verse,
        "uxlc_verse": uxlc_nodes,
        "diff_wlc_uxlc": diff_wlc_uxlc_for_output,
        "mam_simple_verse": mam_simple_verse,
        "diff_wlc_mam": diff_wlc_mam_for_output,
    }
    rtms_meteg_witness.attach_internal_meteg_witnesses(
        enriched_row,
        wlc422_witness=wlc422_verse_meteg_witness,
        uxlc_witness=uxlc_nodes_meteg_witness,
        mam_simple_witness=mam_simple_verse_meteg_witness,
    )
    return enriched_row, diff_wlc_uxlc_for_checks


def _normalize_payload_for_diff_ignoring_notes(payload: object) -> object:
    if isinstance(payload, list):
        return [_normalize_payload_for_diff_ignoring_notes(item) for item in payload]

    if isinstance(payload, dict):
        had_note_key = any(key in _DIFF_NOTE_KEYS for key in payload.keys())
        out_payload: dict[str, object] = {}
        for key, value in payload.items():
            if key in _DIFF_NOTE_KEYS:
                continue
            out_payload[key] = _normalize_payload_for_diff_ignoring_notes(value)

        # Collapse only dicts that were explicitly note-bearing wrappers.
        if (
            had_note_key
            and set(out_payload.keys()) == {"word"}
            and isinstance(out_payload.get("word"), str)
        ):
            return out_payload["word"]
        if (
            had_note_key
            and set(out_payload.keys()) == {"text"}
            and isinstance(out_payload.get("text"), str)
        ):
            return out_payload["text"]

        return out_payload

    return payload


def _expand_subset_diff_to_wlc_focus(
    diff_value: object,
    *,
    wlc_focus: str | None,
    rhs_key: str,
) -> object:
    return rtms_focus_diff_expand.expand_subset_diff_to_wlc_focus(
        diff_value,
        wlc_focus=wlc_focus,
        rhs_key=rhs_key,
    )


def _ignore_targeted_wlc_mam_diffs(diff_value: object) -> object:
    entries: list[object]
    if isinstance(diff_value, list):
        entries = [entry for entry in diff_value if entry is not None]
    elif diff_value is None:
        entries = []
    else:
        entries = [diff_value]

    kept_entries = [
        entry for entry in entries if not _is_ignored_wlc_mam_diff_entry(entry)
    ]
    if not kept_entries:
        return []
    if len(kept_entries) == 1:
        return kept_entries[0]
    return kept_entries


def _is_ignored_wlc_mam_diff_entry(entry: object) -> bool:
    if not isinstance(entry, dict):
        return False

    wlc_tokens = _diff_side_tokens(entry.get("wlc422"))
    mam_tokens = _diff_side_tokens(entry.get("mam_simple"))
    if wlc_tokens is None or mam_tokens is None:
        return False

    return (wlc_tokens, mam_tokens) in _IGNORED_WLC_MAM_DIFF_TOKEN_PAIRS


def _diff_side_tokens(side_value: object) -> tuple[str, ...] | None:
    if isinstance(side_value, str):
        return (side_value,)
    if isinstance(side_value, list) and all(
        isinstance(token, str) for token in side_value
    ):
        return tuple(side_value)
    return None


def _validate_unique_wlc_focus_in_wlc_verse(
    *,
    ref: str,
    wlc422_kq_u_verse: object,
    wlc_focus: str | None,
) -> None:
    rtms_focus_diff_expand.validate_unique_focus_occurrence(
        ref=ref,
        wlc422_kq_u_verse=wlc422_kq_u_verse,
        wlc_focus=wlc_focus,
    )
    rtms_focus_highlight.validate_focus_highlightable(
        ref=ref,
        wlc422_kq_u_verse=wlc422_kq_u_verse,
        wlc_focus=wlc_focus,
    )


def _load_wlc422_index(wlc422_kq_u_dir: Path) -> dict[str, dict[str, object]]:
    if not wlc422_kq_u_dir.is_dir():
        raise FileNotFoundError(f"wlc422-kq-u directory not found: {wlc422_kq_u_dir}")

    by_bcv: dict[str, dict[str, object]] = {}
    for in_path in sorted(wlc422_kq_u_dir.glob("1verses_*.json")):
        rows = rtms_rows.read_json(in_path)
        if not isinstance(rows, list):
            raise ValueError(f"Expected list in verses file: {in_path}")
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError(f"Expected object rows in verses file: {in_path}")
            bcv = row.get("bcv")
            if not isinstance(bcv, str):
                raise ValueError(f"Expected string 'bcv' in {in_path}")
            if bcv in by_bcv:
                raise ValueError(f"Duplicate bcv across verses files: {bcv}")
            by_bcv[bcv] = _collapse_wlc_notes_to_string(row)
    return by_bcv


def _collapse_wlc_notes_to_string(node: object) -> object:
    if isinstance(node, list):
        return [_collapse_wlc_notes_to_string(item) for item in node]

    if isinstance(node, dict):
        out_node: dict[str, object] = {}
        for key, value in node.items():
            if (
                key == "notes"
                and isinstance(value, list)
                and all(isinstance(note, str) for note in value)
            ):
                out_node[key] = "".join(value)
            else:
                out_node[key] = _collapse_wlc_notes_to_string(value)
        return out_node

    return node


def _interpolate_wlc422_kq_qere(verse_payload: dict[str, object]) -> dict[str, object]:
    vels = verse_payload.get("vels")
    if not isinstance(vels, list):
        return verse_payload

    out_verse: dict[str, object] = dict(verse_payload)
    out_vels: list[object] = []
    for token in vels:
        if not isinstance(token, dict):
            out_vels.append(token)
            continue

        kq = token.get("kq")
        if not isinstance(kq, list) or len(kq) < 2 or not isinstance(kq[1], list):
            out_vels.append(token)
            continue

        # Inline qere tokens directly into vels in place of the kq wrapper.
        out_vels.extend(kq[1])

    out_verse["vels"] = [_strip_sam_pe_inun_token(token) for token in out_vels]
    out_verse["vels"] = [token for token in out_verse["vels"] if token is not None]
    return out_verse


def _strip_sam_pe_inun_token(token: object) -> object | None:
    if not isinstance(token, dict):
        return token
    if set(token.keys()) == {"sam_pe_inun"}:
        return None
    return token


def _load_uxlc_for_refs(
    uxlc_dir: Path,
    refs_by_book: dict[str, set[tuple[int, int]]],
) -> dict[str, dict[str, object]]:
    if not uxlc_dir.is_dir():
        raise FileNotFoundError(f"UXLC directory not found: {uxlc_dir}")

    by_bcv: dict[str, dict[str, object]] = {}
    for bb, ref_pairs in refs_by_book.items():
        bk39id = wlc_bb_to_bk39id(bb)
        xml_basename = my_uxlc._UXLC_BOOK_FILE_NAMES[bk39id]
        xml_name = f"{xml_basename}.xml"
        xml_path = uxlc_dir / xml_name
        if not xml_path.is_file():
            continue

        tree = ET.parse(xml_path)
        root = tree.getroot()
        target_set = set(ref_pairs)

        for chapter in root.iter("c"):
            ch_attr = chapter.attrib.get("n")
            if ch_attr is None:
                continue
            try:
                chnu = int(ch_attr)
            except ValueError:
                continue
            for verse in chapter.iter("v"):
                v_attr = verse.attrib.get("n")
                if v_attr is None:
                    continue
                try:
                    vrnu = int(v_attr)
                except ValueError:
                    continue
                if (chnu, vrnu) not in target_set:
                    continue
                bcv = rtms_rows.to_compact_bcv(bb, chnu, vrnu)
                nodes = [_to_xmlish_verse_child(child) for child in verse]
                by_bcv[bcv] = {
                    "xml_file": xml_name,
                    "nodes": [node for node in nodes if node is not None],
                }
    return by_bcv


def _to_xmlish_verse_child(element: ET.Element) -> dict[str, object] | str | None:
    if element.tag in {"k", "pe", "samekh"}:
        return None

    tag = "w" if element.tag == "q" else element.tag
    node: dict[str, object] = {"tag": tag}

    # Preserve direct text plus tail text after inline children (e.g. <x>...</x>tail).
    # Do not include inline child text here; it is represented separately in children.
    text_parts = [element.text or ""]
    for child in element:
        text_parts.append(child.tail or "")
    text = "".join(text_parts).strip()
    if text:
        node["text"] = text

    if element.attrib:
        node["attrs"] = dict(element.attrib)

    if tag == "w":
        children = [
            _to_xmlish_inline(child) for child in element if child.tag in {"s", "x"}
        ]
        if children:
            node["children"] = children

    # Compact the common simple case to keep uxlc_verse readable.
    if set(node.keys()) == {"tag", "text"} and node["tag"] == "w":
        return str(node["text"])

    # Flatten the common word+single-note shape.
    if set(node.keys()) == {"tag", "text", "children"} and node["tag"] == "w":
        children = node["children"]
        if (
            isinstance(children, list)
            and len(children) == 1
            and isinstance(children[0], dict)
            and set(children[0].keys()) == {"tag", "text"}
            and children[0]["tag"] == "x"
        ):
            return {"text": str(node["text"]), "note": str(children[0]["text"])}

    return node


def _to_xmlish_inline(element: ET.Element) -> dict[str, object]:
    node: dict[str, object] = {"tag": element.tag}

    text = "".join(element.itertext()).strip()
    if text:
        node["text"] = text

    if element.attrib:
        node["attrs"] = dict(element.attrib)

    return node
