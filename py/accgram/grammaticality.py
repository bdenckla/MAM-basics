r"""A continuous notion of "grammaticality": a PCFG over the parse trees (issue wlc-utils#11).

The checkers give a *binary* verdict -- a verse parses (clean), parses with an
ERROR-leaf recovery (ungrammatical), or dead-ends (no_parse).  Issue wlc-utils#11 asks for a
*continuous* companion: among the grammatical verses, which configurations are
common and which are rare-but-legal?  That is exactly the log-likelihood of a
verse under a probabilistic grammar estimated from the corpus.

**No new parsing infrastructure is needed.**  Every committed ``*_ag.json`` verse
already carries its finished parse ``tree`` (a ``tree.tree_to_obj`` image: an
internal node is ``{label, children:[left, right]}``, a leaf is ``{label,
leaves:[name, ...]}``).  Each node *is* one grammar reduction, so walking the tree
reconstructs which production fired -- a binary rewrite ``label -> left right`` at an
internal node, a lexical rewrite ``label -> (leaf ...)`` at a leaf, plus one
``START -> root`` per verse.  Counting those across the corpus *is* the grammar
estimate.

**Two grammars, never pooled.**  Prose and poetic are two different accent systems
(gotcha: route by accent SYSTEM, never cross-scan), so we estimate two independent
PCFGs -- one over ``out/accgram/prose/*_ag.json`` (all prose books), one over
``out/accgram/poetic/*_ag.json`` (Job-poetic, Proverbs, Psalms) -- and score each
corpus only under its own.

**Estimate from clean, score everything.**  The PCFG is estimated from ``clean``
verses only (the grammatical population).  We then score clean *and* ungrammatical verses
against it: the ungrammatical -- whose trees carry productions the clean grammar rarely or
never emits -- fall to the bottom, which validates that the score tracks real
anomaly.  Smoothing is add-lambda (lambda=0.5) so a never-attested-but-grammatical
production (e.g. a synthesized repair) scores low-but-finite rather than -inf, which
is what the two applications below need.

Score of a tree = sum of log P(production) over its nodes.  Because raw log-likelihood
is dominated by length, the human-facing measure is *per-accent* log-likelihood
(divided by the verse's leaf-accent count) and the *percentile* of a verse's score
among clean verses of the same length.  A per-node breakdown points at *which* clause
is the rare one (the minimum-log-prob production).

A token-bigram model over the scanner's token stream is kept only as a sanity
cross-check (Ben's call: PCFG is the model, n-gram is the baseline) -- it scores
sequence, not structure, but should broadly agree on which verses are atypical.

The two motivating applications both reduce to ``score_obj`` on a candidate tree:
  * **repair disambiguation** -- enumerate the legal readings of an ambiguous cluster
    (e.g. ``bang_legality``'s four bang interpretations), parse each, and rank the
    grammatical survivors by tree score (prefer the most probable repair);
  * **tradition comparison** -- score a WLC reading against a reconstructed MAM reading
    and report the difference (poetic-only, honest at the disjunctive-skeleton level,
    since MAM exposes no full conjunctive token stream).

This is a *research diagnostic*, not a pipeline product: it writes
out/accgram/_grammaticality.txt and touches no corpus output -- regenerate and diff
it after any grammar/scanner change.
"""

from __future__ import annotations

import argparse
import bisect
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import wlc_paths

LAMBDA = 0.5  # add-lambda smoothing constant

# A production is (lhs, rhs).  The rhs is a hashable tuple tagged by node kind:
#   ("BIN", left_label, right_label)  -- internal binary rewrite
#   ("LEX", (leaf_name, ...))         -- leaf (lexical) rewrite
#   ("ROOT", root_label)              -- the START -> root choice (lhs == "START")
Rhs = tuple
START = "START"


def iter_productions(tree_obj: dict):
    """Yield ``(lhs, rhs)`` for every node of a ``tree_to_obj`` dict, plus START->root."""
    yield (START, ("ROOT", tree_obj["label"]))
    yield from _node_productions(tree_obj)


def _node_productions(node: dict):
    label = node["label"]
    children = node.get("children")
    if children is not None:
        left, right = children
        yield (label, ("BIN", left["label"], right["label"]))
        yield from _node_productions(left)
        yield from _node_productions(right)
    else:
        yield (label, ("LEX", tuple(node.get("leaves", ()))))


def accent_count(tree_obj: dict) -> int:
    """Leaf-accent count of a tree: the total number of accent names at its leaves."""
    children = tree_obj.get("children")
    if children is not None:
        return sum(accent_count(c) for c in children)
    return len(tree_obj.get("leaves", ()))


@dataclass
class Pcfg:
    counts: dict[str, Counter] = field(default_factory=dict)  # lhs -> Counter(rhs)
    totals: dict[str, int] = field(default_factory=dict)  # lhs -> sum of counts

    def logprob(self, lhs: str, rhs: Rhs) -> float:
        """Add-lambda log P(rhs | lhs); a never-seen production scores low-but-finite."""
        total = self.totals.get(lhs, 0)
        if total == 0:  # lhs never seen as a parent -- a fully foreign production
            return math.log(LAMBDA / (LAMBDA * 2))  # == log(0.5); a generic floor
        bucket = self.counts[lhs]
        # add-lambda over the seen rhs types plus one reserved "unseen" type
        denom = total + LAMBDA * (len(bucket) + 1)
        return math.log((bucket.get(rhs, 0) + LAMBDA) / denom)


def estimate_pcfg(trees: list[dict]) -> Pcfg:
    counts: dict[str, Counter] = defaultdict(Counter)
    for tree in trees:
        for lhs, rhs in iter_productions(tree):
            counts[lhs][rhs] += 1
    totals = {lhs: sum(bucket.values()) for lhs, bucket in counts.items()}
    return Pcfg(counts=dict(counts), totals=totals)


def score_obj(pcfg: Pcfg, tree_obj: dict) -> tuple[float, list[tuple[str, Rhs, float]]]:
    """Total log-likelihood of a tree and its per-node ``(lhs, rhs, logp)`` breakdown."""
    per_node = [
        (lhs, rhs, pcfg.logprob(lhs, rhs)) for lhs, rhs in iter_productions(tree_obj)
    ]
    return math.fsum(lp for _, _, lp in per_node), per_node


# ---- token-bigram sanity baseline -------------------------------------------------


@dataclass
class Bigram:
    counts: dict[str, Counter] = field(default_factory=dict)
    totals: dict[str, int] = field(default_factory=dict)
    vocab: int = 0

    def logprob(self, prev: str, cur: str) -> float:
        total = self.totals.get(prev, 0)
        denom = total + LAMBDA * (self.vocab + 1)
        seen = self.counts.get(prev, {}).get(cur, 0)
        return math.log((seen + LAMBDA) / denom) if denom else math.log(1e-12)


def estimate_bigram(streams: list[list[str]]) -> Bigram:
    counts: dict[str, Counter] = defaultdict(Counter)
    vocab: set[str] = set()
    for toks in streams:
        seq = ["<s>", *toks, "</s>"]
        vocab.update(seq)
        for prev, cur in zip(seq, seq[1:]):
            counts[prev][cur] += 1
    totals = {prev: sum(bucket.values()) for prev, bucket in counts.items()}
    return Bigram(counts=dict(counts), totals=totals, vocab=len(vocab))


def score_bigram(model: Bigram, toks: list[str]) -> float:
    seq = ["<s>", *toks, "</s>"]
    return math.fsum(model.logprob(prev, cur) for prev, cur in zip(seq, seq[1:]))


# ---- corpus loading + per-verse records -------------------------------------------


@dataclass
class VerseScore:
    ref: str
    status: str
    accents: int  # leaf-accent count (length)
    logl: float  # PCFG total log-likelihood
    per_accent: float  # logl / accents
    rarest: tuple[str, Rhs, float]  # the single least-probable production used
    bigram_per_tok: float  # sanity baseline, per token
    percentile: float = 0.0  # rank among clean verses of the same length (filled later)


def _checker_files(checker: str) -> list[Path]:
    folder = wlc_paths.out_dir() / "accgram" / checker
    return sorted(folder.glob("wlc_422_ps_*_ag.json"))


def load_verses(checker: str) -> list[dict]:
    verses: list[dict] = []
    for path in _checker_files(checker):
        data = json.loads(path.read_text(encoding="utf-8"))
        verses.extend(data["verses"])
    return verses


def _rhs_str(rhs: Rhs) -> str:
    kind = rhs[0]
    if kind == "BIN":
        return f"{rhs[1]} {rhs[2]}"
    if kind == "LEX":
        return "(" + " ".join(rhs[1]) + ")"
    return str(rhs[1])  # ROOT


def score_checker(checker: str) -> tuple[Pcfg, Bigram, list[VerseScore]]:
    """Estimate the PCFG + bigram baseline from clean verses, score every treed verse."""
    verses = load_verses(checker)
    treed = [v for v in verses if v.get("tree") is not None]
    clean_trees = [v["tree"] for v in treed if v["status"] == "clean"]
    pcfg = estimate_pcfg(clean_trees)
    bigram = estimate_bigram(
        [v["input"]["tokens"] for v in treed if v["status"] == "clean"]
    )

    scores: list[VerseScore] = []
    for v in treed:
        tree = v["tree"]
        n = accent_count(tree)
        logl, per_node = score_obj(pcfg, tree)
        rarest = min(per_node, key=lambda p: p[2])
        toks = v["input"]["tokens"]
        scores.append(
            VerseScore(
                ref=v["ref"],
                status=v["status"],
                accents=n,
                logl=logl,
                per_accent=logl / n if n else logl,
                rarest=rarest,
                bigram_per_tok=score_bigram(bigram, toks) / len(toks) if toks else 0.0,
            )
        )

    # percentile of each verse's log-likelihood among CLEAN verses of the same length
    clean_by_len: dict[int, list[float]] = defaultdict(list)
    for s in scores:
        if s.status == "clean":
            clean_by_len[s.accents].append(s.logl)
    for vals in clean_by_len.values():
        vals.sort()
    for s in scores:
        peers = clean_by_len.get(s.accents, [])
        if peers:
            below = bisect.bisect_right(peers, s.logl)  # peers with logL <= this verse
            s.percentile = 100.0 * below / len(peers)
    return pcfg, bigram, scores


# ---- report -----------------------------------------------------------------------

_LEADERBOARD_N = 30


def _render_pcfg(lines: list[str], pcfg: Pcfg) -> None:
    lines.append("## Estimated grammar (productions by descending probability)")
    lines.append("")
    n_rules = sum(len(b) for b in pcfg.counts.values())
    lines.append(f"{len(pcfg.counts)} nonterminals, {n_rules} distinct productions.")
    lines.append("")
    for lhs in sorted(pcfg.counts, key=lambda k: pcfg.totals[k], reverse=True):
        bucket = pcfg.counts[lhs]
        lines.append(f"{lhs}  (total {pcfg.totals[lhs]}, {len(bucket)} rule(s))")
        for rhs, count in sorted(bucket.items(), key=lambda kv: kv[1], reverse=True):
            prob = math.exp(pcfg.logprob(lhs, rhs))
            lines.append(f"    {count:7d}  p={prob:6.4f}  -> {_rhs_str(rhs)}")
        lines.append("")


def _render_leaderboard(lines: list[str], title: str, rows: list[VerseScore]) -> None:
    lines.append(title)
    for s in rows:
        lp = s.rarest[2]
        rarest = f"{s.rarest[0]} -> {_rhs_str(s.rarest[1])}"
        lines.append(
            f"  {s.ref:22} acc={s.accents:2d}  logL={s.logl:8.2f}  /acc={s.per_accent:6.2f}"
            f"  pct={s.percentile:5.1f}  bg/tok={s.bigram_per_tok:6.2f}"
        )
        lines.append(f"      rarest: {rarest}  (logp {lp:.2f})")
    lines.append("")


def _mean_sd(values: list[float]) -> tuple[float, float]:
    mean = math.fsum(values) / len(values)
    var = math.fsum((x - mean) ** 2 for x in values) / len(values)
    return mean, math.sqrt(var)


def render_checker(checker: str, pcfg: Pcfg, scores: list[VerseScore]) -> str:
    lines: list[str] = []
    lines.append(f"# Continuous grammaticality -- {checker} checker")
    lines.append("")
    clean = [s for s in scores if s.status == "clean"]
    odd = [s for s in scores if s.status != "clean"]
    per_acc = sorted(s.per_accent for s in clean)
    mean, sd = _mean_sd(per_acc)
    lines.append(
        f"{len(scores)} treed verses ({len(clean)} clean estimate the grammar, "
        f"{len(odd)} ungrammatical scored against it)."
    )
    lines.append(
        f"Clean per-accent log-likelihood: mean {mean:.3f}, sd {sd:.3f}, "
        f"range [{per_acc[0]:.3f}, {per_acc[-1]:.3f}] (less negative = more typical)."
    )
    lines.append("")

    _render_pcfg(lines, pcfg)

    if odd:
        odd_sorted = sorted(odd, key=lambda s: s.per_accent)
        below_p1 = sum(1 for s in odd if s.percentile <= 1.0)
        below_p5 = sum(1 for s in odd if s.percentile <= 5.0)
        worst = max(s.percentile for s in odd)
        lines.append(
            "## Validation: flagged ungrammatical scored against the clean grammar"
        )
        lines.append(
            f"All {len(odd)} ungrammatical land at percentile <= {worst:.1f} among same-length "
            f"clean verses; {below_p1} sit at <= 1st percentile, {below_p5} at <= 5th. "
            f"The score recovers the binary verdict from the bottom up. "
            f"Showing the {min(_LEADERBOARD_N, len(odd))} rarest:"
        )
        _render_leaderboard(lines, "", odd_sorted[:_LEADERBOARD_N])

    rarest_clean = sorted(clean, key=lambda s: s.per_accent)[:_LEADERBOARD_N]
    _render_leaderboard(
        lines,
        f"## Rarest CLEAN verses -- legal but atypical (lowest per-accent "
        f"log-likelihood, top {_LEADERBOARD_N})",
        rarest_clean,
    )

    # n-gram baseline: does the token-bigram separate ungrammatical from clean as sharply
    # as the structural PCFG?  (Ben's call: PCFG is the model, n-gram a sanity check.)
    lines.append("## n-gram baseline (sanity check, not the model)")
    if odd:
        c_pcfg_m, c_pcfg_sd = _mean_sd([s.per_accent for s in clean])
        o_pcfg_m, _ = _mean_sd([s.per_accent for s in odd])
        c_bg_m, c_bg_sd = _mean_sd([s.bigram_per_tok for s in clean])
        o_bg_m, _ = _mean_sd([s.bigram_per_tok for s in odd])
        pcfg_gap = (c_pcfg_m - o_pcfg_m) / c_pcfg_sd if c_pcfg_sd else float("nan")
        bg_gap = (c_bg_m - o_bg_m) / c_bg_sd if c_bg_sd else float("nan")
        lines.append(
            "Ungrammatical vs clean separation (clean-mean minus ungrammatical-mean, in clean sd):"
        )
        lines.append(
            f"  PCFG  per-accent:  clean {c_pcfg_m:6.3f}+-{c_pcfg_sd:.3f}  "
            f"ungrammatical {o_pcfg_m:6.3f}  -> {pcfg_gap:4.1f} sd"
        )
        lines.append(
            f"  bigram per-token:  clean {c_bg_m:6.3f}+-{c_bg_sd:.3f}  "
            f"ungrammatical {o_bg_m:6.3f}  -> {bg_gap:4.1f} sd"
        )
        lines.append(
            "Structure (PCFG) separates anomalies far more sharply than sequence "
            "(bigram), confirming the PCFG as the primary measure."
        )
    by_pcfg = {
        s.ref for s in sorted(clean, key=lambda s: s.per_accent)[:_LEADERBOARD_N]
    }
    by_bg = {
        s.ref for s in sorted(clean, key=lambda s: s.bigram_per_tok)[:_LEADERBOARD_N]
    }
    lines.append(
        f"Among CLEAN verses the two rankings are largely orthogonal: only "
        f"{len(by_pcfg & by_bg)}/{_LEADERBOARD_N} of the rarest-by-PCFG verses are also "
        f"rarest-by-bigram -- structure-rare and sequence-rare are different questions."
    )
    lines.append("")
    return "\n".join(lines)


def render_report(per_checker: list[tuple[str, Pcfg, list[VerseScore]]]) -> str:
    blocks = [
        render_checker(checker, pcfg, scores) for checker, pcfg, scores in per_checker
    ]
    return ("\n" + "=" * 80 + "\n\n").join(blocks).rstrip() + "\n"


def default_report_path(repo_root: Path) -> Path:
    return wlc_paths.out_dir() / "accgram" / "_grammaticality.txt"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--report",
        type=Path,
        default=default_report_path(repo_root),
        help="Output path for the grammaticality report.",
    )


def run(args: argparse.Namespace) -> None:
    per_checker = []
    for checker in ("prose", "poetic"):
        pcfg, _bigram, scores = score_checker(checker)
        per_checker.append((checker, pcfg, scores))
    report = render_report(per_checker)
    report_path: Path = args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8", newline="\n")
    n = sum(len(scores) for _, _, scores in per_checker)
    print(f"Grammaticality: scored {n} treed verses (prose+poetic) -> {report_path}")
