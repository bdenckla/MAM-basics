from __future__ import annotations

from collections.abc import Iterator

from hkq_cmn.template_name_quotes import canonical_template_name


def _numeric_key(kind: str, key: object) -> int:
    """Convert a numeric-string chapter/verse key to int.

    MAM-parsed plus JSON keys chapters and verses by plain numeric strings
    (e.g. "1", "24"); it no longer carries a header.he_to_int map decoding
    Hebrew-numeral keys. The "0" (superscription) and total-row sentinel
    verse keys are a plain-file concern and never appear in plus files, so no
    sentinel skip is needed here -- a non-numeric key is unexpected data and
    is surfaced as an error rather than silently skipped.
    """
    if not isinstance(key, str):
        raise ValueError(f"{kind} key must be string, got {type(key)}")
    if not key.isdigit():
        raise ValueError(f"{kind} key is not a numeric string: {key!r}")
    return int(key)


def _iter_plus_verse_payloads(
    plus_json: object,
) -> Iterator[tuple[int, int, int, object]]:
    if not isinstance(plus_json, dict):
        raise ValueError("plus JSON root must be an object")

    book39s = plus_json.get("book39s")
    if not isinstance(book39s, list):
        raise ValueError("plus JSON missing list key 'book39s'")

    for book39_index, book39 in enumerate(book39s):
        if not isinstance(book39, dict):
            raise ValueError(f"book39 entry must be object, got {type(book39)}")
        chapters = book39.get("chapters")
        if not isinstance(chapters, dict):
            raise ValueError("book39 entry missing object key 'chapters'")

        for chapter_key, verse_map in chapters.items():
            chapter_num = _numeric_key("chapter", chapter_key)
            if not isinstance(verse_map, dict):
                raise ValueError(f"chapter value must be object, got {type(verse_map)}")

            for verse_key, verse_payload in verse_map.items():
                verse_num = _numeric_key("verse", verse_key)

                yield (book39_index, chapter_num, verse_num, verse_payload)


# ---------------------------------------------------------------------------
# VARIANT-SELECTION (POSSIBLE MISSED HITS) WARNING
#
# This function renders a single flat verse string by picking ONE canonical
# param from each variant-storing template and ignoring the others:
#
#   מ:דחי / מ:צינור — uses param "1" (canonical accent); ignores param "2"
#                      (stress-helper duplicate).  A token that appears ONLY
#                      in param "2" would be silently missed.
#   מ:קמץ            — uses param "ד" (Ashkenazic qamats distinction); ignores
#                      param "ס" (Sephardic).  A vowel difference in the
#                      Sephardic param would not be seen.
#   מ:כפול           — uses param "כפול" (combined form); ignores params "א"
#                      and "ב" (individual alef/bet cantillation readings for
#                      dual-cantillation verses: Decalogue, Saga of Reuben).
#                      A token that differs between the two readings (e.g.
#                      accent-based vowel variants) might not appear in כפול.
#
# Callers that scan the resulting text for specific features should be aware
# that hits present only in the ignored params will not be found.
# ---------------------------------------------------------------------------
# Per-template extraction rules below mirror those in:
#   MAM-parsed/doc-under-readme/reading-mam-parsed-plus.md (extract_text example)
#   MAM-private's mpu-parsing.md (Template dispatch section)
#   qere_projection.py (project_qere_atoms)
# When changing a rule here, check all four locations.
def _collect_text_fragments(node: object, out_parts: list[str]) -> None:
    if isinstance(node, str):
        out_parts.append(node)
        return
    if isinstance(node, list):
        for item in node:
            _collect_text_fragments(item, out_parts)
        return
    if isinstance(node, dict):
        tmpl_name = node.get("tmpl_name")
        # Folded to ASCII quotes for matching the quote-bearing literals below;
        # tmpl_name itself (gershayim) is never stored from this function.
        cmp_name = canonical_template_name(tmpl_name)
        tmpl_params = node.get("tmpl_params")
        if isinstance(tmpl_params, dict):
            if tmpl_name == "נוסח" or tmpl_name == "מ:הערה-2":
                # Param 1 is the in-verse target; param 2 is documentation.
                _collect_text_fragments(tmpl_params.get("1"), out_parts)
                return
            if tmpl_name == "מ:הערה":
                # Suppressed note — no verse text.
                return
            if tmpl_name in ("מ:דחי", "מ:צינור"):
                # Two-param stress-variant template.  Param "1" is the canonical
                # (clean) form; param "2" adds a stress-helper duplicate accent.
                _collect_text_fragments(tmpl_params.get("1"), out_parts)
                return
            if tmpl_name == "מ:קמץ":
                # Two-param qamats template.  Param "ד" (dikduk) is the canonical
                # qamats-gadol/qamats-qatan distinction; param "ס" is Sephardic.
                _collect_text_fragments(tmpl_params.get("ד"), out_parts)
                return
            if tmpl_name == "מ:כפול":
                # "Double-cantillation" template.  Param "כפול" is the combined form.
                _collect_text_fragments(tmpl_params.get("כפול"), out_parts)
                return
            if tmpl_name == "כתיב ולא קרי":
                # Written-but-not-read: contributes nothing to the reading text.
                return
            if tmpl_name == "קרי ולא כתיב":
                # Read-but-not-written: param 2 is the qere text.
                _collect_text_fragments(tmpl_params.get("2"), out_parts)
                return
            if cmp_name == 'מ:קו"כ-אם-2':
                # Trivial qere: param 1 is the word; param 2 is a documentation
                # string (e.g. "א-קרי=..."), not verse text.
                _collect_text_fragments(tmpl_params.get("1"), out_parts)
                return
            if 'כו"ק' in (cmp_name or "") or 'קו"כ' in (cmp_name or ""):
                # Ketiv-qere: param 1 is ketiv (written), param 2 is qere (read).
                _collect_text_fragments(tmpl_params.get("2"), out_parts)
                return
            for value in tmpl_params.values():
                _collect_text_fragments(value, out_parts)


def _render_template_like_text(node: object) -> str:
    if isinstance(node, str):
        return node

    if isinstance(node, list):
        return "".join(_render_template_like_text(item) for item in node)

    if isinstance(node, dict):
        tmpl_name = node.get("tmpl_name")
        tmpl_params = node.get("tmpl_params")
        if isinstance(tmpl_name, str) and isinstance(tmpl_params, dict):
            return _render_template_call(tmpl_name, tmpl_params)

        # Fallback for non-template container nodes.
        return "".join(_render_template_like_text(value) for value in node.values())

    return ""


def _render_template_call(tmpl_name: str, tmpl_params: dict[object, object]) -> str:
    rendered_args: list[str] = []
    for key, value in tmpl_params.items():
        rendered_value = _render_template_like_text(value)
        if isinstance(key, str) and key.isdigit():
            rendered_args.append(rendered_value)
        else:
            rendered_args.append(f"{key}={rendered_value}")

    if not rendered_args:
        return f"{{{{{tmpl_name}}}}}"

    return f"{{{{{tmpl_name}|{'|'.join(rendered_args)}}}}}"


def _collect_nusach_targets(node: object, out_targets: list[str]) -> None:
    if isinstance(node, list):
        for item in node:
            _collect_nusach_targets(item, out_targets)
        return

    if isinstance(node, dict):
        tmpl_name = node.get("tmpl_name")
        tmpl_params = node.get("tmpl_params")
        if isinstance(tmpl_params, dict):
            if tmpl_name == "נוסח":
                target_text = _render_template_like_text(tmpl_params.get("1")).strip()
                if target_text:
                    out_targets.append(target_text)

                # Skip param 2 because it is documentation, not verse text.
                for key, value in tmpl_params.items():
                    if key in {"1", "2"}:
                        continue
                    _collect_nusach_targets(value, out_targets)
                return

            for value in tmpl_params.values():
                _collect_nusach_targets(value, out_targets)


def verse_nusach_targets_by_location(
    plus_json: object,
) -> dict[tuple[int, int, int], list[str]]:
    out: dict[tuple[int, int, int], list[str]] = {}
    for (
        book39_index,
        chapter_num,
        verse_num,
        verse_payload,
    ) in _iter_plus_verse_payloads(plus_json):
        targets: list[str] = []
        _collect_nusach_targets(verse_payload, targets)
        out[(book39_index, chapter_num, verse_num)] = targets
    return out


def _collect_template_argument_records(
    node: object,
    out_records: list[dict[str, str]],
) -> None:
    if isinstance(node, list):
        for item in node:
            _collect_template_argument_records(item, out_records)
        return

    if isinstance(node, dict):
        tmpl_name = node.get("tmpl_name")
        tmpl_params = node.get("tmpl_params")
        if isinstance(tmpl_name, str) and isinstance(tmpl_params, dict):
            for key, value in tmpl_params.items():
                argument_key = str(key)
                # In plus JSON, נוסח param 2 is documentation, not verse text.
                if tmpl_name == "נוסח" and argument_key == "2":
                    continue

                argument_text = _render_template_like_text(value).strip()
                if argument_text:
                    out_records.append(
                        {
                            "template_name": tmpl_name,
                            "argument_key": argument_key,
                            "argument_text": argument_text,
                        }
                    )

                _collect_template_argument_records(value, out_records)
            return

        for value in node.values():
            _collect_template_argument_records(value, out_records)


def verse_template_argument_records_by_location(
    plus_json: object,
) -> dict[tuple[int, int, int], list[dict[str, str]]]:
    out: dict[tuple[int, int, int], list[dict[str, str]]] = {}
    for (
        book39_index,
        chapter_num,
        verse_num,
        verse_payload,
    ) in _iter_plus_verse_payloads(plus_json):
        records: list[dict[str, str]] = []
        _collect_template_argument_records(verse_payload, records)
        out[(book39_index, chapter_num, verse_num)] = records
    return out


def verse_texts_by_location(
    plus_json: object,
) -> dict[tuple[int, int, int], str]:
    out: dict[tuple[int, int, int], str] = {}
    for (
        book39_index,
        chapter_num,
        verse_num,
        verse_payload,
    ) in _iter_plus_verse_payloads(plus_json):
        text_parts: list[str] = []
        _collect_text_fragments(verse_payload, text_parts)
        out[(book39_index, chapter_num, verse_num)] = "".join(text_parts)
    return out
