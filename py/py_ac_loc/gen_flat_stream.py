"""
Generate flat-stream JSON files for Aleppo Codex pages.

Each page gets a JSON file containing a flat array of:
  - structural markers: {"page-start": "280v"}, {"page-end": "280v"}
  - verse markers: {"verse-start": "Job 38:31"}, {"verse-end": "Job 38:31"}
  - verse-fragment markers: {"verse-fragment-start": ...}, {"verse-fragment-end": ...}
  - parashah markers: {"parashah": "spi-pe2"}, {"parashah": "spi-samekh2"}
  - words: plain Hebrew strings

Column and line markers are NOT pre-populated — the user adds them
interactively via the HTML editor.

Usage:
    .venv/Scripts/python.exe py/main_ac_gen_flat_stream.py <page> <start_book> <start_c:v> <end_book> <end_c:v>
    .venv/Scripts/python.exe py/main_ac_gen_flat_stream.py <page> --chain <prev_page> <end_book> <end_c:v>

Examples:
    .venv/Scripts/python.exe py/main_ac_gen_flat_stream.py 270r Ps 149:1 Job 1:22
    .venv/Scripts/python.exe py/main_ac_gen_flat_stream.py 270v --chain 270r Job 4:21
"""

import json
import sys
from pathlib import Path

import ac_paths
from py_ac_loc.mam_xml_verses import get_verses_in_range
from mb_cmn.uni_denorm import has_std_mark_order

MAM_XML_DIR = ac_paths.mam_xml_dir()
LB_DIR = ac_paths.line_breaks_dir()
OUT_DIR = ac_paths.ds_flat_stream_dir()

BOOK_XML = {
    "Deut": "Deut.xml",
    "Job": "Job.xml",
    "Ps": "Ps.xml",
    "Prov": "Prov.xml",
}

BOOK_ORDER = ["Deut", "Ps", "Job", "Prov"]

# For cross-book pages we need to know where each book ends
# (last chapter, last verse). We'll use large sentinels and
# let the XML parser handle it.
BOOK_END_SENTINEL = (999, 999)
BOOK_START = (1, 1)


def parse_cv(s):
    """Parse 'c:v' into (int, int)."""
    parts = s.split(":")
    return (int(parts[0]), int(parts[1]))


def get_page_verses(start_book, start_cv, end_book, end_cv):
    """Fetch all verses for a page from MAM-XML, handling cross-book ranges.

    Args:
        start_book: e.g. "Ps"
        start_cv: (chapter, verse) tuple, e.g. (149, 1)
        end_book: e.g. "Job"
        end_cv: (chapter, verse) tuple, e.g. (1, 22)

    Returns:
        List of verse dicts, each with keys: book, cv, words,
        ketiv_indices, parashah_after.
    """
    if start_book == end_book:
        xml_path = str(MAM_XML_DIR / BOOK_XML[start_book])
        verses = get_verses_in_range(xml_path, start_book, start_cv, end_cv)
        for v in verses:
            v["book"] = start_book
        return verses

    # Cross-book range
    all_verses = []
    started = False
    for book in BOOK_ORDER:
        if book == start_book:
            started = True
            xml_path = str(MAM_XML_DIR / BOOK_XML[book])
            vs = get_verses_in_range(xml_path, book, start_cv, BOOK_END_SENTINEL)
            for v in vs:
                v["book"] = book
            all_verses.extend(vs)
        elif started and book == end_book:
            xml_path = str(MAM_XML_DIR / BOOK_XML[book])
            vs = get_verses_in_range(xml_path, book, BOOK_START, end_cv)
            for v in vs:
                v["book"] = book
            all_verses.extend(vs)
            break
        elif started:
            # Entire intermediate book (unlikely but handles it)
            xml_path = str(MAM_XML_DIR / BOOK_XML[book])
            vs = get_verses_in_range(xml_path, book, BOOK_START, BOOK_END_SENTINEL)
            for v in vs:
                v["book"] = book
            all_verses.extend(vs)

    return all_verses


def find_prev_page_endpoint(prev_page_path):
    """Read a previous page's line-break JSON to find where it left off.

    Returns (book, cv_tuple, skip_words, at_boundary) where skip_words
    is the number of words into the verse already consumed.  If the page
    ended exactly at a verse boundary, at_boundary is True and skip_words
    is 0.
    """
    data = json.loads(Path(prev_page_path).read_text("utf-8"))

    # Find the last line-end marker
    last_line_end_idx = None
    for i in range(len(data) - 1, -1, -1):
        if isinstance(data[i], dict) and "line-end" in data[i]:
            last_line_end_idx = i
            break

    if last_line_end_idx is None:
        raise ValueError(f"No line-end markers found in {prev_page_path}")

    # Walk backwards from the last line-end to find the last word
    last_word_idx = None
    for i in range(last_line_end_idx, -1, -1):
        if isinstance(data[i], str):
            last_word_idx = i
            break
    if last_word_idx is None:
        raise ValueError(f"No words found before last line-end in {prev_page_path}")

    # Find the verse this word belongs to
    verse_label = None
    for i in range(last_word_idx, -1, -1):
        if isinstance(data[i], dict):
            if "verse-start" in data[i]:
                verse_label = data[i]["verse-start"]
                break
            if "verse-fragment-start" in data[i]:
                verse_label = data[i]["verse-fragment-start"]
                break

    if verse_label is None:
        raise ValueError(
            f"Could not find verse context for last word in {prev_page_path}"
        )

    # Check if the page ended at a verse boundary
    at_verse_end = False
    for i in range(last_word_idx + 1, len(data)):
        if isinstance(data[i], dict):
            if "verse-end" in data[i] and data[i]["verse-end"] == verse_label:
                at_verse_end = True
                break
            if "line-start" in data[i] or "line-end" in data[i]:
                continue
            if "verse-fragment-end" in data[i]:
                break
            break

    # Parse: "Job 1:16" -> ("Job", (1, 16))
    parts = verse_label.split(" ", 1)
    book = parts[0]
    cv = parse_cv(parts[1])

    if at_verse_end:
        return book, cv, 0, True
    else:
        # Count how many words of this verse were consumed
        word_count = 0
        for i in range(last_word_idx, -1, -1):
            if isinstance(data[i], str):
                word_count += 1
            elif isinstance(data[i], dict):
                if "verse-start" in data[i] or "verse-fragment-start" in data[i]:
                    break
        return book, cv, word_count, False


def next_verse(book, cv):
    """Return the next verse reference.  Uses MAM-XML to find it."""
    xml_path = str(MAM_XML_DIR / BOOK_XML[book])
    c, v = cv
    # Try next verse in same chapter
    next_cv = (c, v + 1)
    vs = get_verses_in_range(xml_path, book, next_cv, next_cv)
    if vs:
        return book, next_cv
    # Try first verse of next chapter
    next_cv = (c + 1, 1)
    vs = get_verses_in_range(xml_path, book, next_cv, next_cv)
    if vs:
        return book, next_cv
    # Next book
    idx = BOOK_ORDER.index(book)
    if idx + 1 < len(BOOK_ORDER):
        return BOOK_ORDER[idx + 1], (1, 1)
    raise ValueError(f"No next verse after {book} {c}:{v}")


MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"


def _assert_standard_order(word, verse_label):
    """Assert combining marks on each base letter follow standard order.

    Uses mb_cmn.uni_denorm.has_std_mark_order (SBL2 mark order) to check
    that the word already has the project's standard mark ordering.

    Args:
        word: a single Hebrew word string (base letters + combining marks).
        verse_label: human-readable verse label (e.g. "Job 38:1") for
            error messages.
    """
    if not has_std_mark_order(word):
        marks_str = " ".join(
            f"U+{ord(c):04X}" for c in word if ord(c) > 0x0590 and ord(c) < 0x05F5
        )
        raise AssertionError(
            f"Non-standard combining mark order in {verse_label}, "
            f"word '{word}'. Marks: [{marks_str}]"
        )


def build_flat_stream(page_id, verses, skip_first_n_words=0):
    """Build the flat stream array for a page.

    If skip_first_n_words > 0, the first verse is treated as a fragment
    and the first N words are omitted (they were on the previous page).

    Args:
        page_id: leaf identifier, e.g. "270r".
        verses: list of verse dicts as returned by get_page_verses.
        skip_first_n_words: number of maqaf-split words to skip in the
            first verse (for cross-page continuations).

    Returns:
        The flat stream list (strings and marker dicts).
    """
    stream = []
    stream.append({"page-start": page_id})

    for vi, v in enumerate(verses):
        book = v["book"]
        cv = v["cv"]
        label = f"{book} {cv}"

        is_fragment = vi == 0 and skip_first_n_words > 0

        if v.get("parashah_before") and not is_fragment:
            stream.append(v["parashah_before"])

        # Expand words with maqaf splitting
        all_words = []
        for word in v["words"]:
            _assert_standard_order(word, label)
            parts = word.split(MAQAF)
            for k, part in enumerate(parts):
                if k < len(parts) - 1:
                    all_words.append(part + MAQAF)
                else:
                    all_words.append(part)

        if is_fragment:
            # Fragment: skip words already on previous page
            remaining = all_words[skip_first_n_words:]
            if remaining:
                stream.append({"verse-fragment-start": label})
                stream.extend(remaining)
                stream.append({"verse-fragment-end": label})
            # If no remaining words, skip this verse entirely
        else:
            stream.append({"verse-start": label})
            stream.extend(all_words)
            stream.append({"verse-end": label})

    stream.append({"page-end": page_id})
    return stream


def write_stream(page_id, stream):
    """Write the flat stream JSON file.

    Args:
        page_id: leaf identifier, e.g. "270r".
        stream: flat stream list to serialize.
    """
    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / f"{page_id}.json"
    out_path.write_text(
        json.dumps(stream, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="",
    )
    return out_path


def main():
    # Check for --force flag anywhere in args
    force = "--force" in sys.argv
    if force:
        sys.argv = [a for a in sys.argv if a != "--force"]

    # --chain mode: read previous page's line-break file, auto-determine start
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

    word_count = sum(1 for x in stream if isinstance(x, str))
    verse_count = sum(1 for x in stream if isinstance(x, dict) and "verse-start" in x)

    # Sanity check: a full Aleppo Codex page needs at least ~300 words.
    # Require 300 as a floor to catch too-short verse ranges.
    MIN_WORDS = 300
    if word_count < MIN_WORDS:
        print(
            f"  WARNING: only {word_count} words generated (minimum {MIN_WORDS}).\n"
            f"  The end-point verse is probably too close to the start.\n"
            f"  Try a later end verse (e.g. +3 chapters)."
        )
        if out_path.exists():
            out_path.unlink()
            print(f"  Removed {out_path} — re-run with a later end verse.")
        sys.exit(1)

    out_path.write_text(
        json.dumps(stream, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(f"  -> {out_path.name}: {verse_count} verses, {word_count} words")


if __name__ == "__main__":
    main()
