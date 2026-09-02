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
# ---------------------------------------------------------------------------
# VARIANT-TEMPLATE MULTIPLICITY WARNING
#
# The four templates below store multiple textual variants as separate params.
# When word_atoms_from_qere_atoms() processes them it recurses into EVERY param
# list, so a single word that appears inside one of these templates will produce
# MULTIPLE word-atom hits — one per variant param — that are otherwise
# INDISTINGUISHABLE in the output (same word text, same sources list).
#
# Known templates and their variant params:
#   מ:דחי   — "1" (canonical accent) + "2" (stress-helper duplicate accent)
#   מ:צינור — "1" (canonical accent) + "2" (stress-helper duplicate accent)
#   מ:קמץ   — "ד" (qamats gadol/qatan, Ashkenazic) + "ס" (Sephardic)
#   מ:כפול  — "כפול" (combined) + "א" (alef cantillation) + "ב" (bet cantillation)
#              (applies to dual-cantillation verses: Decalogue, Saga of Reuben)
#
# Additionally, the fall-through path at the bottom of project_qere_atoms()
# recurses into ALL params of any template not explicitly recognised here,
# so future novel multi-param templates would silently exhibit the same
# multiplicity.
#
# Callers that count or deduplicate hits must account for this behaviour.
# ---------------------------------------------------------------------------
# Per-template extraction rules below mirror those in:
#   MAM-parsed/gh-pages/plus/html/mpplus.html and its siblings, the rendered
#     structure reference, whose source is this repo's py/author_misc/
#   MAM-private/mgketer/documentation/mpu-parsing.md (Template dispatch section)
#   mam_plus_verse_data._collect_text_fragments
# When changing a rule here, check all four locations.
#
# THE FIRST ENTRY NAMED A FILE THAT DOES NOT EXIST, until 2026-09-02: it read
# MAM-parsed/doc-under-readme/reading-mam-parsed-plus.md (extract_text example),
# and that whole directory is gone.
#
# THIS MODULE STILL COLLECTS EVERY PARAMETER OF AN UNRECOGNISED TEMPLATE, where
# mam_plus_verse_data raises instead as of 2026-09-02.  The difference is
# deliberate: this projection is a tolerate-and-skip one, feeding a search for
# ketiv/qere words rather than a count of atoms, so an unrecognised template
# costs it a spurious hit and not a wrong index.  The fall-through warning below
# is the standing statement of that cost.
PARAM_BOUNDARY_TEMPLATE_NAMES = {
    "מ:דחי",
    "מ:צינור",
    "מ:קמץ",
    "מ:כפול",
}


def to_vowel_only_form(text: str) -> str:
    no_joiners = CGJ_AND_JOINERS_RE.sub("", text)
    return ACCENTS_AND_METEG_RE.sub("", no_joiners)


def strip_accents_and_meteg(text: str) -> str:
    """Backward-compatible alias for scratch helpers."""
    return to_vowel_only_form(text)


def qere_arg_key_for_template(template_name: str) -> str | None:
    name = canonical_template_name(template_name)
    if name == 'מ:קו"כ-אם-2':
        return "1"
    if name == "קרי ולא כתיב":
        return "2"
    if name == "כתיב ולא קרי":
        return None
    if 'כו"ק' in name or 'קו"כ' in name:
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
        "is_trivq_arg1": canonical_template_name(template_name) == 'מ:קו"כ-אם-2'
        and argument_key == "1",
        "parent_source": source,
    }


def _text_atom(text: str, source: dict[str, object] | None) -> dict[str, object]:
    return {
        "kind": "text",
        "text": text,
        "source": source,
    }


def _template_atom(
    template_name: str,
    param_atom_lists: list[list[dict[str, object]]],
) -> dict[str, object]:
    return {
        "kind": "template",
        "template_name": template_name,
        "param_atom_lists": param_atom_lists,
    }


def project_qere_atoms(
    node: object,
    *,
    source: dict[str, object] | None,
) -> list[dict[str, object]]:
    if isinstance(node, str):
        return [_text_atom(node, source)]

    if isinstance(node, list):
        out: list[dict[str, object]] = []
        for item in node:
            out.extend(project_qere_atoms(item, source=source))
        return out

    if not isinstance(node, dict):
        return []

    tmpl_name = node.get("tmpl_name")
    tmpl_params = node.get("tmpl_params")
    if not isinstance(tmpl_name, str) or not isinstance(tmpl_params, dict):
        return []

    if tmpl_name in {"נוסח", "מ:הערה-2"}:
        return project_qere_atoms(tmpl_params.get("1"), source=source)

    if canonical_template_name(tmpl_name) in {"מ:הערה", "כתיב ולא קרי", 'מ:נו"ן הפוכה'}:
        return []

    qere_arg_key = qere_arg_key_for_template(tmpl_name)
    if qere_arg_key is not None:
        return project_qere_atoms(
            tmpl_params.get(qere_arg_key),
            source=_with_source(source, tmpl_name, qere_arg_key),
        )

    if tmpl_name in WHITESPACE_TEMPLATE_NAMES:
        return [_text_atom(" ", source)]

    if tmpl_name in {"מ:פסק", "מ:לגרמיה-2"}:
        return [_text_atom(PASOLEG, source)]

    if tmpl_name == "מ:מקף אפור":
        return [_text_atom(MAQ, source)]

    if tmpl_name in IN_WORD_RECURSE_TEMPLATE_NAMES:
        return project_qere_atoms(tmpl_params.get("1"), source=source)

    if tmpl_name in PARAM_BOUNDARY_TEMPLATE_NAMES:
        # NOTE: all variant params are projected and returned as separate atom
        # lists.  word_atoms_from_qere_atoms() will recurse into every one of
        # them, producing one hit per variant (see VARIANT-TEMPLATE MULTIPLICITY
        # WARNING above).  The template name is recorded in the _template_atom
        # wrapper but NOT propagated into the per-word sources chain.
        return [
            _template_atom(
                tmpl_name,
                [
                    project_qere_atoms(value, source=source)
                    for value in tmpl_params.values()
                ],
            )
        ]

    # Fall-through: unrecognised template — recurse into all param values.
    # WARNING: if an unrecognised template stores multiple textual variants as
    # separate params this will silently produce multiple word-atom hits in the
    # same way as PARAM_BOUNDARY_TEMPLATE_NAMES (see warning above).
    out: list[dict[str, object]] = []
    for value in tmpl_params.values():
        out.extend(project_qere_atoms(value, source=source))
    return out


def flatten_sources(source: dict[str, object] | None) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    current = source
    while isinstance(current, dict):
        out.append(
            {
                "template_name": current.get("template_name"),
                "argument_key": current.get("argument_key"),
                "is_trivq_arg1": bool(current.get("is_trivq_arg1")),
            }
        )
        current = current.get("parent_source")
    return out


def _word_atoms_from_text_atom(atom: dict[str, object]) -> list[dict[str, object]]:
    text = atom.get("text")
    if not isinstance(text, str):
        return []

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
        kind = atom.get("kind")
        if kind == "text":
            out.extend(_word_atoms_from_text_atom(atom))
            continue
        if kind == "template":
            param_atom_lists = atom.get("param_atom_lists")
            if not isinstance(param_atom_lists, list):
                continue
            for param_atoms in param_atom_lists:
                if not isinstance(param_atoms, list):
                    continue
                out.extend(word_atoms_from_qere_atoms(param_atoms))
    return out


def iter_plus_verses(
    plus_json: dict[str, object],
    plus_file_name: str,
) -> Iterator[dict[str, object]]:
    # MAM-parsed plus JSON keys chapters/verses by plain numeric strings and no
    # longer carries a header.he_to_int decode map. Non-numeric keys (the
    # "0"/total-row sentinels are a plain-file concern, absent from plus) are
    # skipped, matching this projection's tolerate-and-skip posture.
    book39s = plus_json.get("book39s")
    if not isinstance(book39s, list):
        raise ValueError("plus JSON missing book39s")

    for book39_index, book39 in enumerate(book39s):
        if not isinstance(book39, dict):
            continue
        book_name = book39.get("book24_name")
        sub_book_name = book39.get("sub_book_name")
        chapters = book39.get("chapters")
        if not isinstance(chapters, dict):
            continue

        for chapter_key, verses in chapters.items():
            if not isinstance(chapter_key, str) or not chapter_key.isdigit():
                continue
            if not isinstance(verses, dict):
                continue
            chapter_num = int(chapter_key)

            for verse_key, verse_payload in verses.items():
                if not isinstance(verse_key, str) or not verse_key.isdigit():
                    continue
                if not isinstance(verse_payload, list) or len(verse_payload) < 3:
                    continue
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
