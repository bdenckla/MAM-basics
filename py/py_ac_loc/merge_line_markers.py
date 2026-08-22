"""
Merge line-break markers from an edited flat-stream export back
into the original flat-stream JSON, preserving original Hebrew strings.

The edited JSON may have been Unicode-normalized during the
clipboard/browser/chat pipeline.  This script:

1. Reads the original JSON (pristine strings from gen_flat_stream).
2. Reads the edited JSON (may have normalized strings).
3. Strips line-start/line-end from the original to get a "base" stream.
4. Walks the edited stream, matching words by NFC-normalized comparison.
5. Records where line-start/line-end dicts appear relative to word indices.
6. Inserts those dicts into the base stream at the matching positions.
7. Writes the result back to the original file.

Usage:
    python py_ac_loc/merge_line_markers.py 270v
    python py_ac_loc/merge_line_markers.py 270v .novc/edited_270v.json
"""

import json
import sys
import unicodedata
from pathlib import Path

import ac_paths

LB_DIR = ac_paths.line_breaks_dir()
NOVC_DIR = ac_paths.novc_dir()


def nfc(s):
    """NFC-normalize a string for comparison."""
    return unicodedata.normalize("NFC", s)


def extract_words(stream):
    """Extract (index, text) of every string/parashah element in order."""
    words = []
    for item in stream:
        if isinstance(item, str):
            words.append(item)
        elif isinstance(item, dict) and "parashah" in item:
            words.append(item)  # parashah is a "word" for indexing
    return words


def extract_line_markers_by_word_idx(edited_stream):
    """Walk the edited stream and record line markers relative to word index.

    Args:
        edited_stream: flat stream list that may contain line-start and
            line-end marker dicts interspersed with word strings.

    Returns:
        before: dict mapping word_idx → list of dicts to insert BEFORE that word.
        after: dict mapping word_idx → list of dicts to insert AFTER that word.
    """
    before = {}  # word_idx -> [marker, ...]
    after = {}  # word_idx -> [marker, ...]
    word_idx = 0
    pending_before = []  # markers seen since last word (to attach to NEXT word)

    for item in edited_stream:
        if isinstance(item, str) or (isinstance(item, dict) and "parashah" in item):
            # This is a word
            if pending_before:
                before.setdefault(word_idx, []).extend(pending_before)
                pending_before = []
            word_idx += 1
        elif isinstance(item, dict):
            if "line-start" in item or "line-end" in item:
                if word_idx == 0:
                    # Before any word
                    pending_before.append(item)
                else:
                    # Decide: line-start goes BEFORE the next word,
                    # line-end goes AFTER the previous word.
                    if "line-end" in item:
                        after.setdefault(word_idx - 1, []).extend([item])
                    else:
                        # line-start: attach to next word
                        pending_before.append(item)
            # other dicts (verse-start, verse-end, page-start, page-end): skip

    return before, after


def verify_words_match(orig_words, edited_words):
    """Verify that original and edited word lists match under NFC normalization.

    Args:
        orig_words: word list extracted from the original (pristine) stream.
        edited_words: word list extracted from the edited stream (may have
            been Unicode-normalized during the clipboard/browser pipeline).
    """
    if len(orig_words) != len(edited_words):
        print(
            f"ERROR: Word count mismatch: original={len(orig_words)}, edited={len(edited_words)}"
        )
        sys.exit(1)

    mismatches = []
    for i, (ow, ew) in enumerate(zip(orig_words, edited_words)):
        # Both might be parashah dicts or strings
        if isinstance(ow, dict) and isinstance(ew, dict):
            if ow != ew:
                mismatches.append((i, repr(ow), repr(ew)))
        elif isinstance(ow, str) and isinstance(ew, str):
            if nfc(ow) != nfc(ew):
                mismatches.append((i, ow, ew))
        else:
            mismatches.append((i, repr(ow), repr(ew)))

    if mismatches:
        print(f"ERROR: {len(mismatches)} word mismatches:")
        for idx, o, e in mismatches[:10]:
            print(f"  [{idx}] original: {o}")
            print(f"       edited:   {e}")
        sys.exit(1)

    # Check if any normalization actually happened
    norm_count = 0
    for ow, ew in zip(orig_words, edited_words):
        if isinstance(ow, str) and isinstance(ew, str) and ow != ew:
            norm_count += 1
    if norm_count:
        print(f"  {norm_count} words differ in raw form (but match under NFC)")
    else:
        print("  All words match exactly (no normalization detected)")


def merge(orig_stream, edited_stream):
    """Merge line markers from edited stream into original stream.

    Args:
        orig_stream: the original flat stream (pristine Hebrew strings,
            possibly with old line markers that will be stripped).
        edited_stream: the edited flat stream containing new line-start
            and line-end marker dicts.

    Returns:
        The merged stream: original strings with line markers from the
        edited stream inserted at the corresponding positions.
    """
    # Strip existing line markers from original
    base_stream = [
        item
        for item in orig_stream
        if not (isinstance(item, dict) and ("line-start" in item or "line-end" in item))
    ]

    # Extract words from both
    orig_words = extract_words(base_stream)
    edited_words = extract_words(edited_stream)
    verify_words_match(orig_words, edited_words)

    # Extract line marker positions from edited
    before, after = extract_line_markers_by_word_idx(edited_stream)

    # Rebuild: walk base_stream, inserting line markers at right positions
    result = []
    word_idx = 0

    for item in base_stream:
        is_word = isinstance(item, str) or (
            isinstance(item, dict) and "parashah" in item
        )
        if is_word:
            # Insert any "before" markers
            if word_idx in before:
                result.extend(before[word_idx])
            result.append(item)
            # Insert any "after" markers
            if word_idx in after:
                result.extend(after[word_idx])
            word_idx += 1
        else:
            result.append(item)

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python py_ac_loc/merge_line_markers.py <page_id> [edited.json]")
        sys.exit(1)

    page_id = sys.argv[1]
    orig_path = LB_DIR / f"{page_id}.json"
    if not orig_path.exists():
        print(f"ERROR: {orig_path} not found")
        sys.exit(1)

    if len(sys.argv) >= 3:
        edited_path = Path(sys.argv[2])
    else:
        edited_path = NOVC_DIR / f"edited_{page_id}.json"

    if not edited_path.exists():
        print(f"ERROR: {edited_path} not found")
        sys.exit(1)

    print(f"Original: {orig_path}")
    print(f"Edited:   {edited_path}")

    orig_stream = json.loads(orig_path.read_text(encoding="utf-8"))
    edited_stream = json.loads(edited_path.read_text(encoding="utf-8"))

    merged = merge(orig_stream, edited_stream)

    # Write back
    orig_path.write_text(
        json.dumps(merged, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="",
    )

    # Stats
    line_starts = sum(1 for x in merged if isinstance(x, dict) and "line-start" in x)
    line_ends = sum(1 for x in merged if isinstance(x, dict) and "line-end" in x)
    print(f"Wrote {orig_path}")
    print(f"  {line_starts} line-start markers, {line_ends} line-end markers")


if __name__ == "__main__":
    main()
