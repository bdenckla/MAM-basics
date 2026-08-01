r"""How legal is each same-letter "bang" pair?  A separate poetic diagnostic.

A bang ``a x!y b`` is one base letter carrying two accents ``x`` and ``y`` with no
natural order (e.g. ps56:10's ``merkha!azla`` -- merkha U+05A5 + qadma U+05A8 on one
alef).  The poetic scanner *represents* such a cluster faithfully as one order-less
token (Plan D), but treats the same-letter co-occurrence as a lexical anomaly: the bang
has no ``conj`` terminal, so the verse dead-ends to NO_PARSE and surfaces as an ungrammatical verse
rather than a silently-clean parse.  That a verse "parses with x and y as a sequence"
does NOT establish that x stacked on y is a legal Masoretic configuration -- exactly as
lv25:20's ``mahapakh!tipexa`` (two *below* accents) parses as a sequence yet is
intrinsically impossible on one letter.

This module measures *how legal* a bang pair is, without changing any verdict, by the
four interpretations a reader could give the cluster (``a`` / ``b`` = the verse prefix /
suffix around it):

    a x b      -- keep only x, drop y          (the "choose one accent" reading, as the
    a y b      -- keep only y, drop x           telg + geresh family drops to telg)
    a x y b    -- x then y, as an ordered sequence
    a y x b    -- y then x, the other ordering

Each is built by splicing the bang token's decomposition back into the verse's token
stream and re-parsing; an interpretation is *legal* iff the grammar accepts it with no
ERROR / NO_PARSE.  The count of legal interpretations (0..4) is the "how legal" measure:
4/4 is a fully-legal anomaly (flagged, but harmless however resolved), 0/4 is fully
illegal, in between is partial.

Genre note: built poetic-first (the only attested poetic bang is ps56:10).  The splice
is genre-agnostic, so the same measure can later cover the prose bangs (ek20:31's
mahapakh!qadma, lv25:20's mahapakh!tipexa) under one notion.  This is a *report*, not a
verdict: it writes out/accgram/poetic/_bang_legality.txt and leaves the corpus
output untouched -- regenerate and diff it after any scanner/grammar change.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from accgram import accent_marks as am
from accgram import poetic_filter
from accgram import poetic_accent_names as pan
from accgram import rtms_data
from accgram import uni_to_marks
from accgram.poetic_ply_grammar import build_parser, parse_tokens_accepting_repeats
from accgram.poetic_scanner import scan_verse
from accgram.tree import print_tree
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id

import wlc_paths

# Each bang token -> the two co-equal accents it fuses, in storage order: a
# (token, leaf) pair for x and for y, plus the (mark_x, mark_y) codepoints used to
# locate the bearing word in the raw -kq-u text.  Poetic-first: only merkha!azla.
BANG_DECOMP: dict[str, tuple[tuple[str, str], tuple[str, str], tuple[str, str]]] = {
    pan.MERKHA_AZLA: (
        (pan.MERKHA, "merkha"),
        (pan.AZLA, "azla"),
        (am.MERKHA, am.QADMA),
    ),
}


@dataclass(frozen=True)
class BangVerdict:
    reference: str
    word: str  # the pointed word bearing the bang (best-effort from the raw text)
    bang_leaf: str  # e.g. "merkha!azla"
    x_leaf: str
    y_leaf: str
    legal: dict[str, bool]  # interpretation label -> grammatical?

    @property
    def n_legal(self) -> int:
        return sum(self.legal.values())

    @property
    def category(self) -> str:
        n = self.n_legal
        if n == len(self.legal):
            return "fully legal"
        return "fully illegal" if n == 0 else "partial"


def _is_base(ch: str) -> bool:
    return "א" <= ch <= "ת"


def _raw_words(vel) -> list[str]:
    """Every pointed word string carried by one verse element (ketiv+qere both)."""
    if isinstance(vel, str):
        return [vel]
    if not isinstance(vel, dict):
        return []
    if isinstance(vel.get("sam_pe_inun"), str):
        return []
    kq = vel.get("kq")
    if kq is not None:
        out: list[str] = []
        if isinstance(kq, (list, tuple)) and len(kq) == 2:
            for side in kq:
                if isinstance(side, (list, tuple)):
                    for v in side:
                        out += _raw_words(v)
        return out
    w = vel.get("word")
    return [w] if isinstance(w, str) else []


def _words_with_pair(verse: dict, mark_x: str, mark_y: str) -> list[str]:
    """Pointed words whose text carries ``mark_x`` immediately followed by ``mark_y``
    (same letter -- two adjacent marks, no base letter between)."""
    pair = mark_x + mark_y
    vels = verse.get("vels")
    hits: list[str] = []
    if isinstance(vels, list):
        for vel in vels:
            for w in _raw_words(vel):
                if pair in w:
                    hits.append(w)
    return hits


def _grammatical(parser, stream) -> bool:
    tree, _err = parse_tokens_accepting_repeats(parser, stream)
    return tree is not None and "ERROR" not in print_tree(tree, 0)


def _interpretations(x: tuple[str, str], y: tuple[str, str]):
    """The four readings of a bang, as (label, replacement-token-list)."""
    return {
        f"a x b   ({x[1]})": [x],
        f"a y b   ({y[1]})": [y],
        f"a x y b ({x[1]} {y[1]})": [x, y],
        f"a y x b ({y[1]} {x[1]})": [y, x],
    }


def collect(input_path: Path) -> list[BangVerdict]:
    """One BangVerdict per bang-token occurrence across the poetic corpus."""
    index = rtms_data.load_wlc422_index(input_path)
    parser = build_parser()
    verdicts: list[BangVerdict] = []
    for bcv, verse in index.items():
        bb = bcv[:2]
        ch, _colon, vr = bcv[2:].partition(":")
        ch, vr = int(ch), int(vr)
        if not poetic_filter.should_keep_line(bb, ch, vr):
            continue
        body = uni_to_marks.verse_to_marks(verse)
        if not body:
            continue
        reference = f"{wlc_bb_to_bk39id(bb)} {ch}:{vr}"
        toks = scan_verse(reference, body).tokens
        bang_positions = [i for i, (t, _) in enumerate(toks) if t in BANG_DECOMP]
        if not bang_positions:
            continue
        # Per bang TYPE, pair the k-th bang occurrence with the k-th raw word carrying
        # that mark pair (bangs are rare; usually one per verse), for the report only.
        words_seen: dict[str, list[str]] = {}
        used: dict[str, int] = {}
        for i in bang_positions:
            btype = toks[i][0]
            x, y, (mark_x, mark_y) = BANG_DECOMP[btype]
            if btype not in words_seen:
                words_seen[btype] = _words_with_pair(verse, mark_x, mark_y)
            k = used.get(btype, 0)
            used[btype] = k + 1
            word = words_seen[btype][k] if k < len(words_seen[btype]) else "?"
            legal = {
                label: _grammatical(parser, toks[:i] + repl + toks[i + 1 :])
                for label, repl in _interpretations(x, y).items()
            }
            verdicts.append(
                BangVerdict(
                    reference=reference,
                    word=word,
                    bang_leaf=toks[i][1],
                    x_leaf=x[1],
                    y_leaf=y[1],
                    legal=legal,
                )
            )
    return verdicts


def render_report(verdicts: list[BangVerdict]) -> str:
    lines: list[str] = []
    lines.append("# Bang-pair legality (poetic corpus)")
    lines.append("")
    lines.append(
        "How legal each same-letter `a x!y b` cluster is, measured by which of its four "
        "interpretations parse grammatically (no ERROR / NO_PARSE).  The bang itself is a "
        "flagged lexical anomaly (NO_PARSE ungrammatical verse); this measure records how the cluster "
        "WOULD read if resolved.  NB: the poetic conjunctive grammar is permissive, so for "
        "an all-conjunctive bang every interpretation tends to be legal -- the measure only "
        "gains discriminating power once conjunctive grammaticality is strengthened."
    )
    lines.append("")
    n = len(verdicts)
    fully = sum(1 for v in verdicts if v.category == "fully legal")
    partial = sum(1 for v in verdicts if v.category == "partial")
    illegal = sum(1 for v in verdicts if v.category == "fully illegal")
    lines.append(
        f"{n} bang-pair occurrence(s): {fully} fully legal, {partial} partial, "
        f"{illegal} fully illegal."
    )
    lines.append("")
    for v in verdicts:
        lines.append(f"{v.reference}  {v.word}  {v.bang_leaf}")
        for label, ok in v.legal.items():
            lines.append(f"  {label:24} {'LEGAL' if ok else 'illegal'}")
        lines.append(f"  => {v.n_legal}/{len(v.legal)} legal ({v.category})")
        lines.append("")
    return "\n".join(lines) + "\n"


def default_input_path(repo_root: Path) -> Path:
    return rtms_data.default_wlc422_kq_u_dir(repo_root)


def default_report_path(repo_root: Path) -> Path:
    return wlc_paths.out_dir() / "accgram" / "poetic" / "_bang_legality.txt"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input_path(repo_root),
        help="Directory of the -kq-u Unicode source (wlc422-kq-u/1verses_*.json).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=default_report_path(repo_root),
        help="Output path for the bang-legality report.",
    )


def run(args: argparse.Namespace) -> None:
    verdicts = collect(args.input)
    report = render_report(verdicts)
    report_path: Path = args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8", newline="\n")
    fully = sum(1 for v in verdicts if v.category == "fully legal")
    print(
        f"Bang-pair legality: {len(verdicts)} occurrence(s), {fully} fully legal "
        f"-> {report_path}"
    )
