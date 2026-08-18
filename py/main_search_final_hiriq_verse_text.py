from __future__ import annotations

import json
from pathlib import Path
import sys

import hkq_paths
from mb_cmn import bib_locales, paths
from mb_cmn.hebrew_points import XIRIQ
from hkq_cmn.hebrew_text_tokens import (
    find_hebrew_tokens,
    strip_ignorable_token_marks,
)
from hkq_cmn.mam_plus_verse_data import verse_texts_by_location

PLUS_DIR = paths.mam_parsed_plus_dir().resolve()
TARGET_VERSE = ("Tsefaniah", 2, 9)
OUTPUT_DIR = hkq_paths.out_dir()
OUTPUT_PATH = OUTPUT_DIR / "final_hiriq_verse_text_report.json"


def book_names_for_plus_file(path: Path, plus_json: dict[str, object]) -> list[str]:
    book39s = plus_json.get("book39s")
    if not isinstance(book39s, list):
        raise ValueError("plus JSON missing list key 'book39s'")

    bk24id = path.stem.split("-", 1)[1]
    names = list(bib_locales.bk39ids_of_bk24(bk24id))
    if len(names) != len(book39s):
        raise ValueError(
            f"book-name mismatch for {path.name}: expected {len(book39s)} names, got {len(names)}"
        )
    return names


def strip_ignorable_marks(token: str) -> str:
    return strip_ignorable_token_marks(token)


def is_final_hiriq_token(token: str) -> bool:
    return strip_ignorable_marks(token).endswith(XIRIQ)


def find_final_hiriq_hits() -> tuple[list[dict[str, object]], list[str]]:
    hits: list[dict[str, object]] = []
    target_tokens: list[str] = []

    for path in sorted(PLUS_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            plus_json = json.load(handle)

        verse_texts = verse_texts_by_location(plus_json)
        book_names = book_names_for_plus_file(path, plus_json)

        for (book39_index, chapter_num, verse_num), verse_text in verse_texts.items():
            book_name = book_names[book39_index]
            tokens = find_hebrew_tokens(verse_text)

            if (book_name, chapter_num, verse_num) == TARGET_VERSE:
                target_tokens = tokens

            for token in tokens:
                if not is_final_hiriq_token(token):
                    continue

                hits.append(
                    {
                        "book": book_name,
                        "chapter": chapter_num,
                        "verse": verse_num,
                        "token": token,
                        "deaccented": strip_ignorable_marks(token),
                        "file": path.name,
                    }
                )

    return hits, target_tokens


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    hits, target_tokens = find_final_hiriq_hits()

    target_verse_str = f"{TARGET_VERSE[0]} {TARGET_VERSE[1]}:{TARGET_VERSE[2]}"
    final_hiriq_target_tokens = [t for t in target_tokens if is_final_hiriq_token(t)]

    report = {
        "total_hits": len(hits),
        "notes": [
            "VARIANT-SELECTION (POSSIBLE MISSED HITS): verse text is rendered by",
            "_collect_text_fragments, which picks ONE canonical param from each",
            "variant-storing template and silently ignores the rest. Tokens present",
            "only in an ignored param will not appear in the search results.",
            "Known selective templates:",
            "  מ:דחי / מ:צינור — use param '1' (canonical accent); ignore param '2' (stress-helper).",
            "                    A token present only in param '2' would be missed.",
            "  מ:קמץ           — use param 'ד' (Ashkenazic); ignore param 'ס' (Sephardic).",
            "                    A vowel distinction only in the Sephardic reading would be missed.",
            "  מ:כפול          — use param 'כפול' (combined); ignore params 'א'/'ב'",
            "                    (alef/bet cantillation — dual-cantillation verses only:",
            "                    Decalogue, Saga of Reuben). A token differing between",
            "                    the two readings might not appear in the combined form.",
        ],
        "hits": hits,
        "target_verse": target_verse_str,
        "target_verse_tokens": target_tokens,
        "target_verse_final_hiriq_tokens": final_hiriq_target_tokens,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)

    print(f"total_hits={len(hits)}")
    for hit in hits:
        print(
            f"{hit['book']} {hit['chapter']}:{hit['verse']}\t"
            f"{hit['token']}\tdeaccented={hit['deaccented']}\tfile={hit['file']}"
        )

    print("target_verse_tokens=")
    print(" ".join(target_tokens))

    print("target_verse_final_hiriq_tokens=")
    print(" ".join(final_hiriq_target_tokens))


if __name__ == "__main__":
    main()
