"""Driver for the Python port: mirrors `accents -p` on the WLC prose corpus.

Reads the canonical `-kq-u` Unicode source `out/wlc422-kq-u/`, transcodes
each verse into per-book scanner-ready mark text (uni_to_marks, applying the genre
filter so poetic books never reach the prose grammar), scans each verse into a token
stream (prose_scanner), parses it into a tree (prose_ply_grammar), and writes one
JSON record per verse to out/accgram/prose/wlc_422_ps_<bb>_ag.json (issue wlc-utils#20,
replacing the legacy bespoke indented-tree text).  Each record pairs the verse's
``input`` (pointed-Hebrew unicode + raw mark body + token stream) with the full parse
``tree`` -- so "how the input parses" is shown for every verse, not just the handful
of illegal-mark cases the old text format named.

A verse the grammar cannot parse at all (parse_tokens returns None) is a fatal
error: it signals a residual prose-grammar gap that must be surfaced, not silently
skipped. ERROR-trees and location-only (pasuq-level error) verses are not None --
they still emit a record and remain "ungrammatical".
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from accgram import chanted_word_accents
from accgram import dual_cant_detangle
from accgram import lexical_validation
from accgram import mam_simple_verse
from accgram import prose_filter
from accgram import rtms_data
from accgram import uni_to_marks
from accgram.prose_ply_grammar import LOCATION_ONLY, build_parser, parse_tokens
from accgram.prose_scanner import scan_book
from accgram.tree import TN, add_leaves, tree_to_obj
from mb_cmn import file_io
from mb_cmn import paths
from mb_cmn import provenance


def _illegal_mark_tree(
    marks: list[lexical_validation.LexicalUngrammaticalMark], words: list[str]
):
    """Degenerate ERROR tree for a verse carrying lexical ungrammatical mark(s).

    The branch label names each offending code and the pointed-Hebrew word it was
    found in (e.g. ``illegal_mark 82 in יִשְׂרָאֵ֘ל``), so the ungrammatical-verse reports pinpoint
    the word; the single terminal leaf is the bare ``ERROR`` token that
    accgram.ungrammatical keys on.  ``words`` is the offending Unicode word per mark, in
    order (see `_ungrammatical_unicode_words`).  The *structure* is uniform across all such
    verses (one branch + one ERROR leaf) -- only the descriptive label varies -- so the
    error is attributed to the ungrammatical mark itself rather than to whatever the rest of
    the accent sequence would have parsed into.
    """
    detail = "; ".join(f"{mark.code} in {word}" for mark, word in zip(marks, words))
    return add_leaves(f"illegal_mark {detail}", "ERROR")


def _ungrammatical_unicode_words(
    marks: list[lexical_validation.LexicalUngrammaticalMark],
    verse: object,
) -> list[str]:
    """The pointed-Hebrew word bearing each ungrammatical mark, aligned to ``marks``.

    Each illegal mark carries a ``rep_char`` -- a codepoint of the offending word unique
    enough to locate it (``82`` = the zarqa stress-helper U+0598; a same-letter pair =
    its first/distinguishing mark, e.g. mahapakh U+05A4, NOT the tipexa that recurs
    elsewhere in lv25:20).  Collect the words carrying each rep_char in order and pair
    them with ``marks``.  Falls back to a mark's raw M-C atom if the Unicode word cannot
    be located (so the label is always populated)."""
    rep_chars = {mark.rep_char for mark in marks}
    by_char: dict[str, list[str]] = {}
    for word in _verse_display_words(verse):
        for char in rep_chars:
            if char in word:
                by_char.setdefault(char, []).append(word)
    cursor: dict[str, int] = {}
    out: list[str] = []
    for mark in marks:
        char = mark.rep_char
        candidates = by_char.get(char, [])
        i = cursor.get(char, 0)
        if i < len(candidates):
            out.append(candidates[i])
            cursor[char] = i + 1
        else:
            out.append(mark.atom)
    return out


def _verse_display_words(verse: object):
    """The verse's Unicode words in order, descending into ketiv-qere (qere side)."""
    vels = verse.get("vels") if isinstance(verse, dict) else None
    if not isinstance(vels, list):
        return
    for vel in vels:
        if isinstance(vel, str):
            yield vel
        elif isinstance(vel, dict):
            word = vel.get("word")
            if isinstance(word, str):
                yield word
            kq = vel.get("kq")
            if isinstance(kq, (list, tuple)) and len(kq) == 2:
                for qvel in kq[1]:
                    if isinstance(qvel, str):
                        yield qvel
                    elif isinstance(qvel, dict) and isinstance(qvel.get("word"), str):
                        yield qvel["word"]


@dataclass(frozen=True)
class BookRun:
    bb: str
    verse_count: int
    parsed_count: int


def _tree_has_error(tree: TN | None) -> bool:
    """True if any leaf of ``tree`` carries the ERROR token (an ungrammatical verse)."""
    if tree is None:
        return False
    if tree.left is not None:
        return _tree_has_error(tree.left) or _tree_has_error(tree.right)
    return "ERROR" in tree.leaves


def _verse_record(
    verse, bb: str, parser, wlc_index: dict[str, dict] | None
) -> dict[str, object]:
    """Build one verse's JSON record: ref, bcv, status, input, tree, [errors].

    ``status`` is one of ``illegal_mark`` (a lexical/alphabet error, fixed ERROR
    tree), ``location_only`` (a pasuq-level error, no tree), ``ungrammatical`` (a parse
    tree carrying an ERROR leaf), or ``clean``.  The ``input`` block carries the
    pointed-Hebrew ``unicode`` (from the -kq-u source), the ``marks`` body (the scan
    body, whose base-letter placeholder is alef -- see ``accent_marks.LETTER``), and the
    ``tokens`` stream, for every verse -- not just the illegal-mark cases.

    ``chanted_word_accents`` is a diagnostic channel beside the verdict, not part of it: the
    chanted words of this verse carrying two or more accent tokens, each with the ITM section
    that names its token sequence or a null where none does.  It is recorded for every verse,
    whatever its status, and omitted where there is nothing to report -- as ``errors`` is.  The
    verdict itself is untouched, and whether an unnamed pair should be ungrammatical is a
    separate decision (see ``accgram.chanted_word_accents``).
    """
    tail = verse.reference.rpartition(" ")[2]
    chnu_str, _, vrnu_str = tail.partition(":")
    bcv = f"{bb}{tail}"
    record: dict[str, object] = {
        "ref": verse.reference,
        "bcv": bcv,
        "input": {
            "unicode": (
                rtms_data.verse_unicode_text(
                    wlc_index, bb, int(chnu_str), int(vrnu_str)
                )
                if wlc_index
                else ""
            ),
            "marks": verse.body,
            "tokens": [token.type for token in verse.tokens],
        },
    }

    two_accents = chanted_word_accents.classify_verse(verse.body, verse.tokens)
    if two_accents:
        record["chanted_word_accents"] = two_accents

    # Prose lexical layer (divergence from the goerwitz C oracle): an alphabet /
    # word-placement error -- an unpaired stress-helper, a same-letter accent pair, or
    # a misplaced telisha qetanna (full enumeration in lexical_validation.lexical_
    # ungrammatical).  Flag it uniformly with a fixed ERROR tree and skip the grammar
    # entirely -- the context need not be parsed, and all such verses read identically.
    ungrammatical = lexical_validation.lexical_ungrammatical(verse.body)
    if ungrammatical:
        kq_verse = wlc_index.get(bcv) if wlc_index else None
        words = _ungrammatical_unicode_words(ungrammatical, kq_verse)
        record["status"] = "illegal_mark"
        record["errors"] = [
            {"code": mark.code, "word": word, "atom": mark.atom}
            for mark, word in zip(ungrammatical, words)
        ]
        record["tree"] = tree_to_obj(_illegal_mark_tree(ungrammatical, words))
        return record

    tree = parse_tokens(parser, verse.tokens)
    if tree is None:
        raise RuntimeError(f"parser produced no output for {verse.reference}")
    # pasuq-level error verses carry no tree; the C `pasuq : error` actions call
    # free_nodes without print_tree.
    if tree is LOCATION_ONLY:
        record["status"] = "location_only"
        record["tree"] = None
    else:
        record["status"] = "error" if _tree_has_error(tree) else "clean"
        record["tree"] = tree_to_obj(tree)
    return record


def render_book(
    text: str, parser, bb: str, wlc_index: dict[str, dict] | None = None
) -> tuple[list[dict[str, object]], BookRun]:
    """Return (verse_records, stats) for one book's scanner-ready text.

    ``wlc_index`` (the kq-u verse index, keyed by bcv) supplies each verse's
    pointed-Hebrew ``input.unicode`` and the illegal_mark label word; omit it to
    leave unicode empty and fall back to the raw M-C atom.
    """
    verses = scan_book(text, bb)
    records = [_verse_record(verse, bb, parser, wlc_index) for verse in verses]
    stats = BookRun(bb=bb, verse_count=len(verses), parsed_count=len(records))
    return records, stats


def default_input_path(repo_root: Path) -> Path:
    return paths.out_dir() / "wlc422-kq-u"


def default_out_dir(repo_root: Path) -> Path:
    return paths.out_dir() / "accgram" / "prose"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input_path(repo_root),
        help="Directory of the -kq-u Unicode source (wlc422-kq-u/1verses_*.json).",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=default_out_dir(repo_root),
        help="Directory for outputs named wlc_422_ps_<bb>_ag.json.",
    )
    parser.add_argument(
        "--book",
        action="append",
        default=None,
        metavar="BB",
        help="Restrict to these book codes (e.g. --book ob). Repeatable. "
        "Default: all books.",
    )


def run(args: argparse.Namespace) -> None:
    input_path: Path = args.input
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.book) if args.book else None
    parser = build_parser()

    book_texts = uni_to_marks.build_book_texts(
        input_path, keep_line_fn=prose_filter.should_keep_line
    )
    wlc_index = rtms_data.load_wlc422_index(input_path)
    mam_by_bcv = _load_dual_cant_mam()  # None if MAM-simple is absent

    total_parsed = 0
    total_verses = 0
    for bb, text in book_texts.items():
        if only is not None and bb not in only:
            continue
        records, stats = render_book(text, parser, bb, wlc_index)
        folded = _fold_dual_cant_oddities(bb, wlc_index, mam_by_bcv, parser)
        records.extend(folded)
        out_path = out_dir / f"wlc_422_ps_{bb}_ag.json"
        _write_book_json(out_path, records)
        total_parsed += stats.parsed_count
        total_verses += stats.verse_count
        folded_note = f" (+{len(folded)} detangled dual-cant oddity)" if folded else ""
        print(
            f"{bb}: parsed {stats.parsed_count}/{stats.verse_count} verses"
            f"{folded_note} -> {out_path}"
        )

    print(
        f"\nTotal: parsed {total_parsed}/{total_verses} verses across selected books."
    )


def _load_dual_cant_mam() -> dict[str, dict] | None:
    """Load the MAM-simple strands for the dual-cantillation loci, or None if the
    sibling MAM-simple corpus is absent (the normal prose run does not require it; the
    detangled dual-cant fold-in is then simply skipped)."""
    mam_dir = mam_simple_verse.default_mam_simple_dir(paths.repo_root())
    if not mam_dir.is_dir():
        return None
    return mam_simple_verse.load_mam_simple_for_refs(
        mam_dir, dual_cant_detangle.all_refs_by_book(), include_strands=True
    )


def _fold_dual_cant_oddities(
    bb: str, wlc_index: dict[str, dict], mam_by_bcv: dict[str, dict] | None, parser
) -> list[dict[str, object]]:
    """Detangled dual-cantillation oddity records to fold into book ``bb`` (issue wlc-utils#36).

    A dual-cant book's WLC dual verses are excluded from the normal scan; the detangler
    parses each strand's chanted verses and a genuine WLC dual-cant bug surfaces as an
    ungrammatical verse.  Those ungrammatical chanted verses are folded in here so they appear in the
    existing prose ungrammatical-verse report (goerwitz.html), keyed by their numbered verse.
    """
    if mam_by_bcv is None or dual_cant_detangle.passage_for_book(bb) is None:
        return []
    return dual_cant_detangle.folded_ungrammatical_records(
        bb, wlc_index, mam_by_bcv, parser
    )


def _book_summary(records: list[dict[str, object]]) -> dict[str, int]:
    counts = {
        "verses": len(records),
        "oddballs": 0,
        "illegal_marks": 0,
        "location_only": 0,
    }
    for record in records:
        if record["status"] == "error":
            counts["oddballs"] += 1
        elif record["status"] == "illegal_mark":
            counts["illegal_marks"] += 1
        elif record["status"] == "location_only":
            counts["location_only"] += 1
    return counts


def _write_book_json(out_path: Path, records: list[dict[str, object]]) -> None:
    payload: dict[str, object] = {
        "summary": _book_summary(records),
        "verses": records,
    }
    payload = provenance.with_json_provenance(payload, __file__)
    # Dedented (indent=0): drop the indentation to keep the committed corpus
    # small, but keep newlines (one element per line) so git diffs stay per-line
    # rather than collapsing to one giant line. Through file_io for the temp-file
    # write and the PermissionError retry -- this writes a file per book, so it is
    # the widest exposure in the repo to a passing Windows lock.
    file_io.json_dump_to_file_path(payload, str(out_path), indent=0)
