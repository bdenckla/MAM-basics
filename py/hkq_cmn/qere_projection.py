from __future__ import annotations

from collections.abc import Iterator
import re

from mb_cmn.hebrew_punctuation import MAQ, PASOLEG
from mb_cmn import template_names
from hkq_cmn.template_name_quotes import canonical_template_name

ACCENTS_AND_METEG_RE = re.compile(r"[\u0591-\u05AF\u05BD\u05BF\u05C0\u05C4\u05C5]")
CGJ_AND_JOINERS_RE = re.compile(r"[\u034F\u200C\u200D]")
TOKEN_SPLIT_RE = re.compile(r"[\s\u05BE\u05C0\u05C3]+")
WHITESPACE_TEMPLATE_NAMES = {
    "מ:ששש",
    "סס",
    "פפ",
    "ססס",
    "פפפ",
    "ר0",
    "ר1",
    "ר2",
    "ר3",
}
# Shared with mam_plus_verse_data._collect_text_fragments, which recurses into
# param 1 of the same four names.  Declared in mb_cmn/template_names.py so that
# the mirroring the header comment below requires is structural rather than
# asserted; this module held its own copy of the four until 2026-09-02.
IN_WORD_RECURSE_TEMPLATE_NAMES = template_names.IN_WORD_TMPL_NAMES


# This search projection is one coherent MAM reading: qere, parameter 1 of a
# dexi/tsinnor stress-helper template, qamats parameter dalet, and combined
# cantillation.  The alternative branches are data, but they are not additional
# qere-word occurrences for this survey.
# Per-template extraction rules below mirror those in:
#   gh-pages/MAM-parsed/plus/html/mpplus.html and its siblings, the rendered
#     structure reference, whose source is this repo's py/author_misc/
#   MAM-private/mgketer/documentation/mpu-parsing.md (Template dispatch section)
#   mam_plus_verse_data._collect_text_fragments
# When changing a rule here, check all four locations.
#
# THE FIRST ENTRY NAMED A FILE THAT DOES NOT EXIST, until 2026-09-02: it read
# MAM-parsed/doc-under-readme/reading-mam-parsed-plus.md (extract_text example),
# and that whole directory is gone.
#
def to_vowel_only_form(text: str) -> str:
    no_joiners = CGJ_AND_JOINERS_RE.sub("", text)
    return ACCENTS_AND_METEG_RE.sub("", no_joiners)


def strip_accents_and_meteg(text: str) -> str:
    """Backward-compatible alias for scratch helpers."""
    return to_vowel_only_form(text)


def qere_arg_key_for_template(template_name: str) -> str | None:
    name = canonical_template_name(template_name)
    if name == canonical_template_name(template_names.TRIVIAL_QERE):
        return "3"
    if name == "קרי ולא כתיב":
        return "2"
    if name == "כתיב ולא קרי":
        return None
    if name in {
        canonical_template_name(item) for item in template_names.STD_KQ_TMPL_NAMES
    }:
        return "2"
    return None


def _with_source(
    source: dict[str, object] | None,
    template_name: str,
    argument_key: str,
) -> dict[str, object]:
    return {
        "template_name": template_name,
        "argument_key": argument_key,
        "is_trivial_qere": canonical_template_name(template_name) == 'מ:קו"כ-אם-2'
        and argument_key == "3",
        "parent_source": source,
    }


def _text_atom(text: str, source: dict[str, object] | None) -> dict[str, object]:
    return {
        "kind": "text",
        "text": text,
        "source": source,
    }


def _required_param(
    tmpl_name: str,
    tmpl_params: dict[object, object],
    key: str,
) -> object:
    if key not in tmpl_params:
        raise ValueError(
            f"Template {tmpl_name!r} is missing required parameter {key!r}"
        )
    return tmpl_params[key]


def project_qere_atoms(
    node: object,
    *,
    source: dict[str, object] | None,
) -> list[dict[str, object]]:
    if isinstance(node, str):
        return [_text_atom(node, source)]

    if isinstance(node, (list, tuple)):
        out: list[dict[str, object]] = []
        for item in node:
            out.extend(project_qere_atoms(item, source=source))
        return out

    if not isinstance(node, dict):
        raise TypeError(f"Unclassified qere-projection node: {type(node).__name__}")

    tmpl_name = node.get("tmpl_name")
    tmpl_params = node.get("tmpl_params", {})
    if not isinstance(tmpl_name, str):
        raise ValueError(f"Qere-projection mapping has no template name: {node!r}")
    if not isinstance(tmpl_params, dict):
        raise ValueError(f"Template {tmpl_name!r} has non-mapping parameters")
    template_names.validate_current_plus_template(node)

    cmp_name = canonical_template_name(tmpl_name)

    if cmp_name in {"נוסח", canonical_template_name(template_names.SCRDFF_TAR)}:
        return project_qere_atoms(
            _required_param(tmpl_name, tmpl_params, "1"), source=source
        )

    if cmp_name in {
        canonical_template_name(template_names.SCRDFF_NO_TAR),
        "כתיב ולא קרי",
        canonical_template_name(template_names.INVERTED_NUN),
    }:
        return []

    qere_arg_key = qere_arg_key_for_template(tmpl_name)
    if qere_arg_key is not None:
        return project_qere_atoms(
            _required_param(tmpl_name, tmpl_params, qere_arg_key),
            source=_with_source(source, tmpl_name, qere_arg_key),
        )

    if cmp_name in WHITESPACE_TEMPLATE_NAMES or cmp_name == "ש":
        return [_text_atom(" ", source)]

    if cmp_name in {"מ:פסק", "מ:לגרמיה-2"}:
        return [_text_atom(PASOLEG, source)]

    if cmp_name == "מ:מקף אפור":
        return [_text_atom(MAQ, source)]

    selected_key = None
    if cmp_name in {
        canonical_template_name(item) for item in IN_WORD_RECURSE_TEMPLATE_NAMES
    } | {
        canonical_template_name(item)
        for item in template_names.STRESS_HELPER_TMPL_NAMES
    }:
        selected_key = "1"
    elif cmp_name == canonical_template_name(template_names.QAMATS_VARIANT):
        selected_key = "ד"
    elif cmp_name == canonical_template_name(template_names.DUAL_CANTILLATION):
        selected_key = "כפול"
    elif cmp_name in {"מ:סיום בטוב", "מודגש"}:
        selected_key = "1"

    if selected_key is not None:
        return project_qere_atoms(
            _required_param(tmpl_name, tmpl_params, selected_key), source=source
        )

    if cmp_name in {
        canonical_template_name(item) for item in template_names.NO_ATOM_TMPL_NAMES
    } | {"מ:קישור בהערה", "מ:קישור פנימי בהערה"}:
        return [_text_atom(" ", source)]

    raise ValueError(f"Unclassified template {tmpl_name!r} in qere-word projection")


def flatten_sources(source: dict[str, object] | None) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    current = source
    while isinstance(current, dict):
        out.append(
            {
                "template_name": current.get("template_name"),
                "argument_key": current.get("argument_key"),
                "is_trivial_qere": bool(current.get("is_trivial_qere")),
            }
        )
        current = current.get("parent_source")
    return out


def _word_atoms_from_text_atom(atom: dict[str, object]) -> list[dict[str, object]]:
    text = atom.get("text")
    if not isinstance(text, str):
        raise TypeError(f"projected text atom has no string text: {atom!r}")

    source = atom.get("source")
    sources = flatten_sources(source if isinstance(source, dict) else None)
    return [
        {
            "word": part,
            "sources": list(sources),
        }
        for part in TOKEN_SPLIT_RE.split(text)
        if part
    ]


def word_atoms_from_qere_atoms(
    atoms: list[dict[str, object]],
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for atom in atoms:
        if not isinstance(atom, dict):
            raise TypeError(f"unclassified projected atom: {atom!r}")
        kind = atom.get("kind")
        if kind == "text":
            out.extend(_word_atoms_from_text_atom(atom))
            continue
        raise ValueError(f"unclassified projected atom kind {kind!r}: {atom!r}")
    return out


def iter_plus_verses(
    plus_json: dict[str, object],
    plus_file_name: str,
) -> Iterator[dict[str, object]]:
    # MAM-parsed plus JSON keys chapters/verses by plain numeric strings and no
    # longer carries a header.he_to_int decode map. Non-numeric keys (the
    # "0"/total-row sentinels are a plain-file concern, absent from plus) are
    # invalid here rather than silently omitted from the survey.
    book39s = plus_json.get("book39s")
    if not isinstance(book39s, list):
        raise ValueError("plus JSON missing book39s")

    for book39_index, book39 in enumerate(book39s):
        if not isinstance(book39, dict):
            raise TypeError(f"book39 entry {book39_index} is not a mapping: {book39!r}")
        book_name = book39.get("book24_name")
        sub_book_name = book39.get("sub_book_name")
        chapters = book39.get("chapters")
        if not isinstance(chapters, dict):
            raise ValueError(f"book39 entry {book39_index} has no chapter mapping")

        for chapter_key, verses in chapters.items():
            if not isinstance(chapter_key, str) or not chapter_key.isdigit():
                raise ValueError(f"invalid plus chapter key: {chapter_key!r}")
            if not isinstance(verses, dict):
                raise TypeError(f"plus chapter {chapter_key!r} is not a mapping")
            chapter_num = int(chapter_key)

            for verse_key, verse_payload in verses.items():
                if not isinstance(verse_key, str) or not verse_key.isdigit():
                    raise ValueError(f"invalid plus verse key: {verse_key!r}")
                if not isinstance(verse_payload, list) or len(verse_payload) != 3:
                    raise ValueError(
                        f"plus verse {chapter_key}:{verse_key} is not a C/D/E triple"
                    )
                if not isinstance(verse_payload[2], list):
                    raise TypeError(
                        f"plus verse {chapter_key}:{verse_key} E column is not a list"
                    )
                verse_num = int(verse_key)

                yield {
                    "plus_file": plus_file_name,
                    "book39_index": book39_index,
                    "book24_name": book_name,
                    "sub_book_name": sub_book_name,
                    "chapter": chapter_num,
                    "verse": verse_num,
                    "ep_payload": verse_payload[2],
                }
