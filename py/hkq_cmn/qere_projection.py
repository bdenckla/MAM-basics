from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
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


@dataclass(frozen=True)
class QereProjectionPolicy:
    """One caller's explicit choices among textual alternatives."""

    name: str
    trivial_qere_argument_key: str
    stress_helper_argument_keys: tuple[str, ...]
    qamats_argument_keys: tuple[str, ...]
    dual_cantillation_argument_keys: tuple[str, ...]
    whitespace_text: str = " "
    paseq_legarmeh_text: str = PASOLEG
    gray_maqaf_text: str = MAQ
    excluded_qamats_text: str = " "


# The holam-he search decision is deferred in
# doc/PLAN-deferred-template-projection-decisions.md.  This policy makes the
# behavior on main explicit while retaining it: parameter 1 of the trivial
# ketiv/qere template and every declared variant branch.
HOLAM_HE_MAIN_COMPATIBLE_POLICY = QereProjectionPolicy(
    name="holam-he-main-compatible",
    trivial_qere_argument_key="1",
    stress_helper_argument_keys=("1", "2"),
    qamats_argument_keys=("ד", "ס"),
    dual_cantillation_argument_keys=("כפול", "א", "ב"),
)

# The qamats-variation survey's accepted 2026-09-12 policy: selected qere,
# parameter 1 of a stress-helper template, no text from a qamats-variation
# template, and the combined-cantillation representation.
XATAF_QAMATS_POLICY = QereProjectionPolicy(
    name="xataf-qamats-foi",
    trivial_qere_argument_key="3",
    stress_helper_argument_keys=("1",),
    qamats_argument_keys=(),
    dual_cantillation_argument_keys=("כפול",),
)

# The historical foi-kq-simple pqere field omits separator punctuation.  The
# unresolved question of whether that field should retain a paseq/legarmeh glyph
# is deferred in the same plan document.
FOI_KQ_SIMPLE_MAIN_COMPATIBLE_POLICY = QereProjectionPolicy(
    name="foi-kq-simple-main-compatible",
    trivial_qere_argument_key="3",
    stress_helper_argument_keys=("1",),
    qamats_argument_keys=("ד",),
    dual_cantillation_argument_keys=("כפול",),
    whitespace_text="",
    paseq_legarmeh_text="",
    gray_maqaf_text="",
    excluded_qamats_text="",
)


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


def _project_argument_keys(
    tmpl_name: str,
    tmpl_params: dict[object, object],
    keys: tuple[str, ...],
    *,
    source: dict[str, object] | None,
    policy: QereProjectionPolicy,
) -> list[dict[str, object]]:
    projected = [
        project_qere_atoms(
            _required_param(tmpl_name, tmpl_params, key),
            source=source,
            policy=policy,
        )
        for key in keys
    ]
    if len(projected) == 1:
        return projected[0]
    return [_template_atom(tmpl_name, projected)]


def project_qere_atoms(
    node: object,
    *,
    source: dict[str, object] | None,
    policy: QereProjectionPolicy,
) -> list[dict[str, object]]:
    if isinstance(node, str):
        return [_text_atom(node, source)]

    if isinstance(node, (list, tuple)):
        out: list[dict[str, object]] = []
        for item in node:
            out.extend(
                project_qere_atoms(
                    item,
                    source=source,
                    policy=policy,
                )
            )
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
            _required_param(tmpl_name, tmpl_params, "1"),
            source=source,
            policy=policy,
        )

    if cmp_name in {
        canonical_template_name(template_names.SCRDFF_NO_TAR),
        "כתיב ולא קרי",
        canonical_template_name(template_names.INVERTED_NUN),
    }:
        return []

    qere_arg_key = qere_arg_key_for_template(tmpl_name)
    if cmp_name == canonical_template_name(template_names.TRIVIAL_QERE):
        qere_arg_key = policy.trivial_qere_argument_key
    if qere_arg_key is not None:
        return project_qere_atoms(
            _required_param(tmpl_name, tmpl_params, qere_arg_key),
            source=_with_source(source, tmpl_name, qere_arg_key),
            policy=policy,
        )

    if cmp_name in WHITESPACE_TEMPLATE_NAMES or cmp_name == "ש":
        return [_text_atom(policy.whitespace_text, source)]

    if cmp_name in {"מ:פסק", "מ:לגרמיה-2"}:
        return [_text_atom(policy.paseq_legarmeh_text, source)]

    if cmp_name == "מ:מקף אפור":
        return [_text_atom(policy.gray_maqaf_text, source)]

    if cmp_name in {
        canonical_template_name(item) for item in IN_WORD_RECURSE_TEMPLATE_NAMES
    }:
        return project_qere_atoms(
            _required_param(tmpl_name, tmpl_params, "1"),
            source=source,
            policy=policy,
        )

    if cmp_name in {
        canonical_template_name(item)
        for item in template_names.STRESS_HELPER_TMPL_NAMES
    }:
        return _project_argument_keys(
            tmpl_name,
            tmpl_params,
            policy.stress_helper_argument_keys,
            source=source,
            policy=policy,
        )

    if cmp_name == canonical_template_name(template_names.QAMATS_VARIANT):
        if not policy.qamats_argument_keys:
            return [_text_atom(policy.excluded_qamats_text, source)]
        return _project_argument_keys(
            tmpl_name,
            tmpl_params,
            policy.qamats_argument_keys,
            source=source,
            policy=policy,
        )

    if cmp_name == canonical_template_name(template_names.DUAL_CANTILLATION):
        return _project_argument_keys(
            tmpl_name,
            tmpl_params,
            policy.dual_cantillation_argument_keys,
            source=source,
            policy=policy,
        )

    if cmp_name in {"מ:סיום בטוב", "מודגש"}:
        return project_qere_atoms(
            _required_param(tmpl_name, tmpl_params, "1"),
            source=source,
            policy=policy,
        )

    if cmp_name in {
        canonical_template_name(item) for item in template_names.NO_ATOM_TMPL_NAMES
    } | {"מ:קישור בהערה", "מ:קישור פנימי בהערה"}:
        return [_text_atom(policy.whitespace_text, source)]

    raise ValueError(
        f"Unclassified template {tmpl_name!r} in {policy.name!r} projection"
    )


def flatten_sources(source: dict[str, object] | None) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    current = source
    while isinstance(current, dict):
        out.append(
            {
                "template_name": current.get("template_name"),
                "argument_key": current.get("argument_key"),
            }
        )
        current = current.get("parent_source")
    return out


def _append_unique_sources(
    out: list[dict[str, object]],
    incoming: list[dict[str, object]],
) -> None:
    for source in incoming:
        if source not in out:
            out.append(source)


def _word_atoms_from_text_atoms(
    atoms: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Tokenize after adjoining text fragments that have no delimiter between them."""
    out: list[dict[str, object]] = []
    word_parts: list[str] = []
    word_sources: list[dict[str, object]] = []

    def emit_word() -> None:
        if not word_parts:
            return
        out.append({"word": "".join(word_parts), "sources": list(word_sources)})
        word_parts.clear()
        word_sources.clear()

    for atom in atoms:
        text = atom.get("text")
        if not isinstance(text, str):
            raise TypeError(f"projected text atom has no string text: {atom!r}")
        source = atom.get("source")
        sources = flatten_sources(source if isinstance(source, dict) else None)
        cursor = 0
        for match in TOKEN_SPLIT_RE.finditer(text):
            fragment = text[cursor : match.start()]
            if fragment:
                word_parts.append(fragment)
                _append_unique_sources(word_sources, sources)
            emit_word()
            cursor = match.end()
        fragment = text[cursor:]
        if fragment:
            word_parts.append(fragment)
            _append_unique_sources(word_sources, sources)

    emit_word()
    return out


def word_atoms_from_qere_atoms(
    atoms: list[dict[str, object]],
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    text_run: list[dict[str, object]] = []

    def emit_text_run() -> None:
        if text_run:
            out.extend(_word_atoms_from_text_atoms(text_run))
            text_run.clear()

    for atom in atoms:
        if not isinstance(atom, dict):
            raise TypeError(f"unclassified projected atom: {atom!r}")
        kind = atom.get("kind")
        if kind == "text":
            text_run.append(atom)
            continue
        emit_text_run()
        if kind == "template":
            param_atom_lists = atom.get("param_atom_lists")
            if not isinstance(param_atom_lists, list):
                raise TypeError(f"projected template atom lacks branches: {atom!r}")
            for param_atoms in param_atom_lists:
                if not isinstance(param_atoms, list):
                    raise TypeError(
                        f"projected template branch is not an atom list: {param_atoms!r}"
                    )
                out.extend(word_atoms_from_qere_atoms(param_atoms))
            continue
        raise ValueError(f"unclassified projected atom kind {kind!r}: {atom!r}")
    emit_text_run()
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
