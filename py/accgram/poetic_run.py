"""Driver for the POETIC (Three Books) scanner + grammar over the corpus.

The poetic counterpart of accgram.prose_run.  Reads the canonical `-kq-u` Unicode source
``out/wlc422-kq-u/`` (transcoded to scanner-ready M-C text by uni_to_marks), keeps only
the poetic verses (Psalms and Proverbs wholesale plus poetically-cantillated Job, via
poetic_filter), scans each verse with poetic_scanner, reconciles the tokens against MAM
(poetic_reconcile: the legarmeh-vs-paseq and unmarked-oleh corrections the M-C source
cannot express), parses the result with poetic_ply_grammar, then writes one JSON record per
verse to out/accgram/poetic/wlc_422_ps_<bb>_ag.json (issue #39, the poetic analogue of the
prose #20 cutover, replacing the legacy bespoke indented-tree text).  Each record pairs the
verse's ``input`` (pointed-Hebrew unicode + raw mark body + reconciled token stream) with
the full parse ``tree`` -- so "how the input parses" is shown for every verse, not just the
handful of ungrammatical cases the old text format named.

Unlike the prose driver, an unparseable verse is NOT fatal.  The poetic grammar is derived
from Yeivin (no C oracle) and a small fraction of verses are known to be structurally ungrammatical;
making each one fatal would block the whole corpus run.  So a verse the grammar cannot parse
(parse_tokens returns None) is recorded with status ``no_parse`` and a ``stall`` locus (the
offending accent's token type and its 1-based ordinal) in place of a tree, and the run
continues.  This output is the verification surface later phases diff against.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from accgram import poetic_filter
from accgram import rtms_data
from accgram import uni_to_marks
from accgram.mam_poetic_accents import load_poetic_disjunctives
from accgram.mam_simple_verse import default_mam_simple_dir
from accgram.poetic_ply_grammar import (
    ParseError,
    build_parser,
    parse_tokens_accepting_repeats,
)
from accgram.poetic_scanner import scan_book
from accgram.tree import TN, tree_to_obj
from accgram.poetic_reconcile import reconcile_tokens
from mb_cmn import file_io
from mb_cmn import provenance

import wlc_paths


@dataclass(frozen=True)
class BookRun:
    bb: str
    verse_count: int
    parsed_count: int  # clean parses (no ERROR leaf)
    error_count: int  # missing-silluq ERROR-leaf trees
    no_parse_count: int  # unrecoverable failures (no_parse records)


def has_error_leaf(tree: TN) -> bool:
    """True if the tree contains an ERROR leaf (a recovered missing-silluq verse)."""
    if tree.left is None:
        return "ERROR" in tree.leaves
    return has_error_leaf(tree.left) or has_error_leaf(tree.right)


def no_parse_line(
    tokens: list[tuple[str, str]], error: ParseError | None = None
) -> str:
    """A greppable one-line summary of an unparseable verse, naming its token types.

    The TILDE/SOFPASUQ structural bookends are dropped; only the accent token types
    between them are listed, so the failing accent sequence is visible at a glance
    (e.g. ``NO_PARSE: PAZER SILLUQ``).  No longer written by this driver (issue #39
    replaced the bespoke text output with per-verse JSON) -- poetic_oddballs reuses it
    to render the NO_PARSE line for the HTML report.

    When ``error`` (the ParseError from parse_tokens_diagnostic) is supplied, the
    stall accent is bracketed with ``>> <<`` and a trailing ``(stalled at accent
    k/n)`` note is appended, so the line pinpoints where the parse dead-ended rather
    than implicating the whole verse.  The ``NO_PARSE:`` prefix is kept either way so
    the lines stay greppable.
    """
    accents = [t for t, _ in tokens if t not in ("TILDE", "SOFPASUQ")]
    if error is None:
        return "NO_PARSE: " + " ".join(accents) + "\n"
    marked = list(accents)
    i = error.accent_index - 1
    if 0 <= i < len(marked):
        marked[i] = f">>{marked[i]}<<"
    return (
        "NO_PARSE: "
        + " ".join(marked)
        + f"  (stalled at accent {error.accent_index}/{len(accents)}: "
        + f"{error.token_type})\n"
    )


def _verse_record(
    verse, bb: str, parser, mam_disj_by_ref: dict[str, list[str]], wlc_index
) -> dict[str, object]:
    """Build one poetic verse's JSON record: ref, bcv, input, status, [stall], tree.

    The scanned tokens are first reconciled (poetic_reconcile) against the MAM
    disjunctive skeleton -- the legarmeh-vs-paseq and unmarked-oleh corrections WLC's
    M-C source cannot express -- so the recorded ``input.tokens`` and ``tree`` are what
    the grammar actually consumed and produced.  The ``input`` block also carries the
    pointed-Hebrew ``unicode`` (from the -kq-u source) and the ``marks`` body (the scan
    body, whose base-letter placeholder is alef -- see ``accent_marks.LETTER``).
    ``status`` is ``clean`` (parsed, no ERROR leaf), ``ungrammatical`` (a missing-silluq
    ERROR-leaf recovery tree), or ``no_parse`` (no valid tree exists).
    """
    tail = verse.reference.rpartition(" ")[2]
    chnu_str, _, vrnu_str = tail.partition(":")
    bcv = f"{bb}{tail}"
    tokens = reconcile_tokens(
        verse.reference,
        verse.body,
        list(verse.tokens),
        mam_disj_by_ref.get(verse.reference),
        parser,
    )
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
            "tokens": [token_type for token_type, _ in tokens],
        },
    }

    tree, error = parse_tokens_accepting_repeats(parser, tokens)
    if tree is None:
        # No valid parse: in place of a tree, record where the LALR(1) parse dead-ended
        # -- the offending accent's token type and its 1-based ordinal among the verse's
        # accents.  Poetic-only; the prose driver treats an unparseable verse as fatal.
        record["status"] = "no_parse"
        record["stall"] = (
            {"accent_index": error.accent_index, "token_type": error.token_type}
            if error is not None
            else None
        )
        record["tree"] = None
    else:
        record["status"] = "error" if has_error_leaf(tree) else "clean"
        record["tree"] = tree_to_obj(tree)
    return record


def _status_counts(records: list[dict[str, object]]) -> dict[str, int]:
    counts = {"clean": 0, "error": 0, "no_parse": 0}
    for record in records:
        status = record["status"]
        if status == "error":
            counts["error"] += 1
        elif status == "no_parse":
            counts["no_parse"] += 1
        else:
            counts["clean"] += 1
    return counts


def render_book(
    text: str,
    parser,
    bb: str,
    mam_disj_by_ref: dict[str, list[str]],
    wlc_index: dict[str, dict] | None = None,
) -> tuple[list[dict[str, object]], BookRun]:
    """Return (verse_records, stats) for one book's scanner-ready text.

    Each verse's scanned tokens are reconciled (poetic_reconcile) against the MAM
    disjunctive skeleton before parsing, exactly as collect_poetic_ungrammatical does, so the
    driver's records agree with the report's trees.  ``wlc_index`` (the kq-u verse index,
    keyed by bcv) supplies each verse's pointed-Hebrew ``input.unicode``; omit it to leave
    unicode empty.
    """
    verses = scan_book(text, bb)
    records = [
        _verse_record(verse, bb, parser, mam_disj_by_ref, wlc_index) for verse in verses
    ]
    counts = _status_counts(records)
    stats = BookRun(
        bb=bb,
        verse_count=len(records),
        parsed_count=counts["clean"],
        error_count=counts["error"],
        no_parse_count=counts["no_parse"],
    )
    return records, stats


def default_input_path(repo_root: Path) -> Path:
    return wlc_paths.out_dir() / "wlc422-kq-u"


def default_out_dir(repo_root: Path) -> Path:
    return wlc_paths.out_dir() / "accgram" / "poetic"


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
        help="Directory for poetic outputs named wlc_422_ps_<bb>_ag.json.",
    )
    parser.add_argument(
        "--mam-simple-dir",
        type=Path,
        default=default_mam_simple_dir(repo_root),
        help="Directory containing MAM-simple json-vtrad-bhs book files "
        "(the legarmeh-vs-paseq oracle for token reconciliation).",
    )
    parser.add_argument(
        "--book",
        action="append",
        default=None,
        metavar="BB",
        help="Restrict to these book codes (ps, pr, jb). Repeatable. "
        "Default: all three poetic books.",
    )


def _book_summary(records: list[dict[str, object]]) -> dict[str, int]:
    counts = _status_counts(records)
    return {
        "verses": len(records),
        "oddballs": counts["error"],
        "no_parse": counts["no_parse"],
    }


def _write_book_json(out_path: Path, records: list[dict[str, object]]) -> None:
    payload: dict[str, object] = {
        "summary": _book_summary(records),
        "verses": records,
    }
    payload = provenance.with_json_provenance(payload, __file__)
    # Dedented (indent=0): drop the indentation to keep the committed corpus
    # small, but keep newlines (one element per line) so git diffs stay per-line
    # rather than collapsing to one giant line. Through file_io for the temp-file
    # write and the PermissionError retry, as prose_run does.
    file_io.json_dump_to_file_path(payload, str(out_path), indent=0)


def run(args: argparse.Namespace) -> None:
    input_path: Path = args.input
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.book) if args.book else None
    parser = build_parser()
    mam_disj_by_ref = load_poetic_disjunctives(args.mam_simple_dir)

    book_texts = uni_to_marks.build_book_texts(
        input_path, keep_line_fn=poetic_filter.should_keep_line
    )
    wlc_index = rtms_data.load_wlc422_index(input_path)

    total_parsed = 0
    total_ungrammatical = 0
    total_no_parse = 0
    total_verses = 0
    for bb, text in book_texts.items():
        if only is not None and bb not in only:
            continue
        records, stats = render_book(text, parser, bb, mam_disj_by_ref, wlc_index)
        out_path = out_dir / f"wlc_422_ps_{bb}_ag.json"
        _write_book_json(out_path, records)
        total_parsed += stats.parsed_count
        total_ungrammatical += stats.error_count
        total_no_parse += stats.no_parse_count
        total_verses += stats.verse_count
        rate = (
            100.0 * stats.parsed_count / stats.verse_count if stats.verse_count else 0.0
        )
        print(
            f"{bb}: parsed {stats.parsed_count}/{stats.verse_count} ({rate:.1f}%) clean"
            f"; {stats.error_count} missing-silluq ungrammatical verse(s), "
            f"{stats.no_parse_count} no_parse -> {out_path}"
        )

    total_rate = 100.0 * total_parsed / total_verses if total_verses else 0.0
    print(
        f"\nTotal: {total_parsed}/{total_verses} ({total_rate:.2f}%) clean parses"
        f"; {total_ungrammatical} missing-silluq ERROR-leaf ungrammatical verse(s); "
        f"{total_no_parse} no_parse across selected poetic books."
    )
