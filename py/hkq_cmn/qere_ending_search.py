from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path

import hkq_paths
from mb_cmn import paths, template_names
from hkq_cmn.template_name_quotes import canonical_template_name
from hkq_cmn.qere_projection import (
    HOLAM_HE_MAIN_COMPATIBLE_POLICY,
    iter_plus_verses,
    project_qere_atoms,
    to_vowel_only_form,
    word_atoms_from_qere_atoms,
)

# mpu = MAM-parsed-plus.
#
# The path defaults below are None sentinels resolved at CALL time, not module-level
# constants.  The reason was hkq_paths.out_dir(), which went through require_sibling
# and RAISED when no holman-ketiv-qere clone sat beside this one: this module is
# imported by py/tests/test_qere_ending_search.py, so an eager default made the suite
# uncollectable without that sibling.  That reason lapsed with ae663ff2 (2026-09-03),
# since when out_dir() has named this repo's holman/out/ and reaches no sibling.  The
# MAM-parsed and qere-words defaults only compose a path, but they take the same
# sentinel so the signatures read one way.  Same sentinel, and the same reason while
# it held, as read_books_from_mam_parsed_plain.py's (0314c6e).


@dataclass(frozen=True)
class QereEndingSearchSpec:
    slug: str
    label: str
    output_file_name: str
    vowel_only_suffixes: tuple[str, ...]

    def matches_word(self, word: str) -> bool:
        vowel_only_form = to_vowel_only_form(word)
        return any(
            vowel_only_form.endswith(suffix) for suffix in self.vowel_only_suffixes
        )


def load_mpu_hits_for_spec(
    spec: QereEndingSearchSpec,
    mam_parsed_plus_dir: Path | None = None,
) -> list[dict[str, object]]:
    if mam_parsed_plus_dir is None:
        mam_parsed_plus_dir = paths.mam_parsed_plus_dir()
    hits: list[dict[str, object]] = []

    for plus_path in sorted(mam_parsed_plus_dir.glob("*.json")):
        with open(plus_path, encoding="utf-8") as handle:
            plus_json = json.load(handle)

        for verse_info in iter_plus_verses(plus_json, plus_path.name):
            qere_atoms = project_qere_atoms(
                verse_info["ep_payload"],
                source=None,
                policy=HOLAM_HE_MAIN_COMPATIBLE_POLICY,
            )
            tokens = word_atoms_from_qere_atoms(qere_atoms)

            for token in tokens:
                word = token.get("word")
                if not isinstance(word, str) or not spec.matches_word(word):
                    continue

                sources_obj = token.get("sources")
                sources = sources_obj if isinstance(sources_obj, list) else []
                source_templates = sorted(
                    {
                        item["template_name"]
                        for item in sources
                        if isinstance(item, dict)
                        and isinstance(item.get("template_name"), str)
                    }
                )
                source_argument_keys = sorted(
                    {
                        item["argument_key"]
                        for item in sources
                        if isinstance(item, dict)
                        and isinstance(item.get("argument_key"), str)
                    }
                )
                is_trivq_arg1 = any(
                    canonical_template_name(str(item.get("template_name")))
                    == canonical_template_name(template_names.TRIVIAL_QERE)
                    and item.get("argument_key") == "1"
                    for item in sources
                    if isinstance(item, dict)
                )

                hits.append(
                    {
                        "plus_file": verse_info["plus_file"],
                        "book39_index": verse_info["book39_index"],
                        "book24_name": verse_info["book24_name"],
                        "sub_book_name": verse_info["sub_book_name"],
                        "chapter": verse_info["chapter"],
                        "verse": verse_info["verse"],
                        "word": word,
                        "vowel_only_form": to_vowel_only_form(word),
                        "is_trivq_arg1": is_trivq_arg1,
                        "source_templates": source_templates,
                        "source_argument_keys": source_argument_keys,
                        "is_plain_text_hit": len(source_templates) == 0,
                    }
                )

    return hits


def load_wordlist_hits_for_spec(
    spec: QereEndingSearchSpec,
    mam_basics_qere_words_path: Path | None = None,
) -> list[dict[str, str]]:
    if mam_basics_qere_words_path is None:
        mam_basics_qere_words_path = hkq_paths.mam_qere_words_path()
    with open(mam_basics_qere_words_path, encoding="utf-8") as handle:
        words = json.load(handle)
    if not isinstance(words, list):
        raise ValueError("mam-qere-words.json must be a list")

    hits: list[dict[str, str]] = []
    for word in words:
        if isinstance(word, str) and spec.matches_word(word):
            hits.append(
                {
                    "word": word,
                    "vowel_only_form": to_vowel_only_form(word),
                }
            )
    return hits


def summarize_mpu_hits(hits: list[dict[str, object]]) -> dict[str, object]:
    vowel_only_counter = Counter(hit["vowel_only_form"] for hit in hits)
    trivq_hits = [hit for hit in hits if hit["is_trivq_arg1"]]
    other_hits = [hit for hit in hits if not hit["is_trivq_arg1"]]
    plain_hits = [hit for hit in hits if hit["is_plain_text_hit"]]
    templated_non_trivq_hits = [
        hit for hit in hits if not hit["is_trivq_arg1"] and not hit["is_plain_text_hit"]
    ]

    return {
        "hit_count": len(hits),
        "unique_vowel_only_form_count": len(vowel_only_counter),
        "trivq_arg1_hit_count": len(trivq_hits),
        "trivq_arg1_unique_vowel_only_form_count": len(
            {hit["vowel_only_form"] for hit in trivq_hits}
        ),
        "other_hit_count": len(other_hits),
        "other_unique_vowel_only_form_count": len(
            {hit["vowel_only_form"] for hit in other_hits}
        ),
        "plain_text_hit_count": len(plain_hits),
        "templated_non_trivq_hit_count": len(templated_non_trivq_hits),
        "source_template_hit_counts": dict(
            sorted(
                Counter(
                    template_name
                    for hit in hits
                    for template_name in hit["source_templates"]
                ).items()
            )
        ),
        "vowel_only_form_counts": dict(sorted(vowel_only_counter.items())),
    }


def hit_source_category(hit: dict[str, object]) -> str:
    if hit["is_trivq_arg1"]:
        return "trivq_arg1"
    if hit["is_plain_text_hit"]:
        return "plain_text"
    return "templated_other"


def verse_indexed_hits(hits: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[object, ...], dict[str, object]] = {}

    for hit in hits:
        key = (
            hit["plus_file"],
            hit["book39_index"],
            hit["chapter"],
            hit["verse"],
            hit["book24_name"],
            hit["sub_book_name"],
        )
        if key not in grouped:
            grouped[key] = {
                "plus_file": hit["plus_file"],
                "book39_index": hit["book39_index"],
                "book24_name": hit["book24_name"],
                "sub_book_name": hit["sub_book_name"],
                "chapter": hit["chapter"],
                "verse": hit["verse"],
                "hits": [],
            }

        grouped[key]["hits"].append(
            {
                "word": hit["word"],
                "vowel_only_form": hit["vowel_only_form"],
                "source_category": hit_source_category(hit),
                "source_templates": hit["source_templates"],
                "source_argument_keys": hit["source_argument_keys"],
            }
        )

    out = list(grouped.values())
    out.sort(
        key=lambda item: (
            str(item["plus_file"]),
            int(item["book39_index"]),
            int(item["chapter"]),
            int(item["verse"]),
        )
    )
    return out


def build_ending_pattern_report(
    spec: QereEndingSearchSpec,
    mam_parsed_plus_dir: Path | None = None,
    mam_basics_qere_words_path: Path | None = None,
) -> dict[str, object]:
    # None forwards to the two loaders, which resolve it; see the module-top comment.
    mpu_hits = load_mpu_hits_for_spec(spec, mam_parsed_plus_dir=mam_parsed_plus_dir)
    wordlist_hits = load_wordlist_hits_for_spec(
        spec,
        mam_basics_qere_words_path=mam_basics_qere_words_path,
    )

    mpu_vowel_only_forms = {hit["vowel_only_form"] for hit in mpu_hits}
    wordlist_vowel_only_forms = {hit["vowel_only_form"] for hit in wordlist_hits}

    return {
        "search": {
            "slug": spec.slug,
            "label": spec.label,
            "vowel_only_suffixes": list(spec.vowel_only_suffixes),
        },
        "notes": [
            "DEFERRED PROJECTION: this report explicitly preserves the behavior on main.",
            "It uses parameter 1 of the trivial ketiv/qere template and every",
            "declared branch of deḥi, tsinnor, qamats, and dual-cantillation",
            "templates. The replacement population requires Ben's decision; see",
            "doc/PLAN-deferred-template-projection-decisions.md. An unclassified",
            "template or parameter shape raises.",
        ],
        "summary": {
            "mpu": summarize_mpu_hits(mpu_hits),
            "mam_basics_wordlist_hit_count": len(wordlist_hits),
            "mam_basics_wordlist_unique_vowel_only_form_count": len(
                wordlist_vowel_only_forms
            ),
            "vowel_only_forms_only_in_mpu": sorted(
                mpu_vowel_only_forms - wordlist_vowel_only_forms
            ),
            "vowel_only_forms_only_in_wordlist": sorted(
                wordlist_vowel_only_forms - mpu_vowel_only_forms
            ),
            "vowel_only_forms_in_both": sorted(
                mpu_vowel_only_forms & wordlist_vowel_only_forms
            ),
        },
        "mpu_hits_trivq_arg1": [hit for hit in mpu_hits if hit["is_trivq_arg1"]],
        "mpu_hits_other": [hit for hit in mpu_hits if not hit["is_trivq_arg1"]],
        "mpu_hits_plain_text": [hit for hit in mpu_hits if hit["is_plain_text_hit"]],
        "mpu_hits_by_verse": verse_indexed_hits(mpu_hits),
        "mpu_templated_hits_by_verse": verse_indexed_hits(
            [hit for hit in mpu_hits if not hit["is_plain_text_hit"]]
        ),
        "mam_basics_wordlist_hits": wordlist_hits,
    }


def write_ending_pattern_report(
    spec: QereEndingSearchSpec,
    output_dir: Path | None = None,
    mam_parsed_plus_dir: Path | None = None,
    mam_basics_qere_words_path: Path | None = None,
) -> tuple[Path, dict[str, object]]:
    if output_dir is None:
        output_dir = hkq_paths.out_dir()
    report = build_ending_pattern_report(
        spec,
        mam_parsed_plus_dir=mam_parsed_plus_dir,
        mam_basics_qere_words_path=mam_basics_qere_words_path,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / spec.output_file_name
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
    return output_path, report
