"""
Generate a flat-stream JSON file for a given page and write it
to line-breaks/<page>.json (without line-break markers).
This is the starting point for interactively adding line breaks.

Usage:
    .venv/Scripts/python.exe py/main_ac_gen_lb_flat_stream.py <page> <start_book> <start_c:v> <end_book> <end_c:v>
    .venv/Scripts/python.exe py/main_ac_gen_lb_flat_stream.py <page> --chain <prev_page> <end_book> <end_c:v>

Examples:
    .venv/Scripts/python.exe py/main_ac_gen_lb_flat_stream.py 270r Ps 149:1 Job 1:22
    .venv/Scripts/python.exe py/main_ac_gen_lb_flat_stream.py 270v --chain 270r Job 4:21
"""

import json
import sys

import ac_paths
from py_ac_loc.gen_flat_stream import (
    parse_cv,
    get_page_verses,
    build_flat_stream,
    find_prev_page_endpoint,
    next_verse,
    BOOK_XML,
    LB_DIR,
)

OUT_DIR = ac_paths.line_breaks_dir()


def main():
    # Check for --force flag anywhere in args
    force = "--force" in sys.argv
    if force:
        sys.argv = [a for a in sys.argv if a != "--force"]

    # --chain mode
    if len(sys.argv) >= 4 and sys.argv[2] == "--chain":
        page_id = sys.argv[1]
        prev_page_id = sys.argv[3]
        end_book = sys.argv[4]
        end_cv = parse_cv(sys.argv[5])

        prev_path = LB_DIR / f"{prev_page_id}.json"
        if not prev_path.exists():
            print(f"ERROR: previous page file not found: {prev_path}")
            sys.exit(1)

        book, cv, skip_words, at_boundary = find_prev_page_endpoint(prev_path)

        if at_boundary:
            start_book, start_cv = next_verse(book, cv)
            skip_words = 0
            print(
                f"{page_id}: chained from {prev_page_id}"
                f" (ended at {book} {cv[0]}:{cv[1]} boundary)"
            )
            print(f"  starting at {start_book} {start_cv[0]}:{start_cv[1]}")
        else:
            start_book = book
            start_cv = cv
            print(
                f"{page_id}: chained from {prev_page_id}"
                f" (ended mid {book} {cv[0]}:{cv[1]}, skip {skip_words} words)"
            )

        verses = get_page_verses(start_book, start_cv, end_book, end_cv)
        stream = build_flat_stream(page_id, verses, skip_first_n_words=skip_words)

    elif len(sys.argv) == 6:
        page_id = sys.argv[1]
        start_book = sys.argv[2]
        start_cv = parse_cv(sys.argv[3])
        end_book = sys.argv[4]
        end_cv = parse_cv(sys.argv[5])

        if start_book not in BOOK_XML:
            print(f"ERROR: unknown book '{start_book}' (known: {list(BOOK_XML)})")
            sys.exit(1)
        if end_book not in BOOK_XML:
            print(f"ERROR: unknown book '{end_book}' (known: {list(BOOK_XML)})")
            sys.exit(1)

        print(
            f"{page_id}: {start_book} {start_cv[0]}:{start_cv[1]}"
            f" .. {end_book} {end_cv[0]}:{end_cv[1]}"
        )

        verses = get_page_verses(start_book, start_cv, end_book, end_cv)
        stream = build_flat_stream(page_id, verses)

    else:
        print(
            "Usage:\n"
            "  Manual:  ... <page_id> <start_book> <start_c:v>"
            " <end_book> <end_c:v>\n"
            "  Chained: ... <page_id> --chain <prev_page_id>"
            " <end_book> <end_c:v>\n"
            "\n"
            "Examples:\n"
            "  ... 270r Ps 149:1 Job 1:22\n"
            "  ... 270v --chain 270r Job 4:21"
        )
        sys.exit(1)

    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / f"{page_id}.json"

    if out_path.exists() and not force:
        print(f"ERROR: {out_path} already exists. Use --force to overwrite.")
        sys.exit(1)

    out_path.write_text(
        json.dumps(stream, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="",
    )
    word_count = sum(1 for x in stream if isinstance(x, str))
    verse_count = sum(1 for x in stream if isinstance(x, dict) and "verse-start" in x)
    print(f"  -> {out_path.name}: {verse_count} verses, {word_count} words")


if __name__ == "__main__":
    main()
