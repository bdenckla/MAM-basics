"""Validate template nesting against a rank-based normal form.

We project each observed stack path onto a small set of ranked templates and
require the ranked projection to be strictly increasing in rank.

Regex-like shape for the ranked projection:
    a?b?c?d?e?f?

Where, by default:
- a: מ:כפול
- b: נוסח
- c: ketiv/qere templates (כו״ק, כתיב ולא קרי, קרי ולא כתיב)
- d: מ:קמץ
- e: מ:דחי
- f: מ:אות-מיוחדת-במילה
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

TemplateName = str
StackCounts = Mapping[Tuple[TemplateName, str], int]
RankMap = Mapping[TemplateName, int]

_DEFAULT_RANK_GROUPS: tuple[tuple[str, frozenset[str]], ...] = (
    ("a", frozenset({"מ:כפול"})),
    ("b", frozenset({"נוסח"})),
    ("c", frozenset({"כו״ק", "כתיב ולא קרי", "קרי ולא כתיב"})),
    ("d", frozenset({"מ:קמץ"})),
    ("e", frozenset({"מ:דחי"})),
    ("f", frozenset({"מ:אות-מיוחדת-במילה"})),
)


def _build_rank_map(rank_groups: Sequence[tuple[str, Iterable[str]]]) -> Dict[str, int]:
    rank_map: Dict[str, int] = {}
    for rank, (_label, names) in enumerate(rank_groups):
        for name in names:
            if name in rank_map:
                raise ValueError(f"Template {name!r} appears in multiple rank groups")
            rank_map[name] = rank
    return rank_map


DEFAULT_RANK_MAP: Dict[str, int] = _build_rank_map(_DEFAULT_RANK_GROUPS)


def regex_like_grammar() -> str:
    """Return the rank grammar in compact regex-like notation."""
    return "a?b?c?d?e?f?"


def _ranked_projection(full_path: Sequence[str], rank_map: RankMap) -> List[str]:
    return [name for name in full_path if name in rank_map]


def find_rank_violations(
    stack_counts: StackCounts,
    rank_map: RankMap | None = None,
) -> List[dict[str, object]]:
    """Return aggregated grammar violations from stack_counts.

    A violation is an adjacent pair in the ranked projection where
    rank(caller) >= rank(callee).
    """
    if rank_map is None:
        rank_map = DEFAULT_RANK_MAP

    bad_counts: Dict[Tuple[str, str, str], int] = defaultdict(int)
    examples: Dict[Tuple[str, str, str], str] = {}

    for (callee, stack_str), count in stack_counts.items():
        if count <= 0:
            continue
        full_path = [p for p in stack_str.split("/") if p]
        full_path.append(callee)
        ranked = _ranked_projection(full_path, rank_map)
        for caller, child in zip(ranked, ranked[1:]):
            caller_rank = rank_map[caller]
            child_rank = rank_map[child]
            relation = None
            if caller_rank > child_rank:
                relation = "descending"
            elif caller_rank == child_rank:
                relation = "duplicate-rank"
            if relation is not None:
                key = (caller, child, relation)
                bad_counts[key] += count
                examples.setdefault(key, "/".join(full_path))

    violations: List[dict[str, object]] = []
    for (caller, child, relation), count in sorted(bad_counts.items()):
        violations.append(
            {
                "caller": caller,
                "callee": child,
                "caller_rank": rank_map[caller],
                "callee_rank": rank_map[child],
                "relation": relation,
                "count": count,
                "example_path": examples[(caller, child, relation)],
            }
        )
    return violations


def assert_stack_counts_in_normal_form(
    stack_counts: StackCounts,
    dataset_name: str,
    rank_map: RankMap | None = None,
) -> None:
    """Raise AssertionError when ranked nesting violates grammar order."""
    violations = find_rank_violations(stack_counts, rank_map=rank_map)
    if not violations:
        return

    lines = [
        (
            f"Template nesting normal-form violation in {dataset_name}: "
            f"expected ranked projection to match {regex_like_grammar()}"
        )
    ]
    for v in violations:
        lines.append(
            "  - "
            f"{v['caller']} (rank {v['caller_rank']}) -> "
            f"{v['callee']} (rank {v['callee_rank']}), "
            f"relation={v['relation']}, "
            f"count={v['count']}, example={v['example_path']}"
        )
    raise AssertionError("\n".join(lines))


def merge_stack_counts(*stack_counts_maps: StackCounts) -> Dict[Tuple[str, str], int]:
    """Merge one or more stack-count maps by summing duplicate keys."""
    merged: Dict[Tuple[str, str], int] = defaultdict(int)
    for stack_counts in stack_counts_maps:
        for key, count in stack_counts.items():
            if count > 0:
                merged[key] += count
    return dict(merged)


def _iter_weighted_paths(stack_counts: StackCounts):
    for (callee, stack_str), count in stack_counts.items():
        if count <= 0:
            continue
        full_path = tuple([p for p in stack_str.split("/") if p] + [callee])
        if not full_path:
            continue
        yield full_path, count


def infer_expanded_stack_grammar(stack_counts: StackCounts) -> Dict[str, object]:
    """Infer a reasonably strict grammar over all stack symbols.

    The inferred grammar has two constraint families:
    - allowed_edges: adjacent parent->child transitions seen in the corpus
    - must_precede: ordered pairs (A, B) where A and B co-occur and A is never
      observed after B

    This usually allows many unseen stacks, while still rejecting permutations
    that reverse observed relative order constraints.
    """
    edge_counts: Dict[Tuple[str, str], int] = defaultdict(int)
    order_counts: Dict[Tuple[str, str], int] = defaultdict(int)

    for full_path, count in _iter_weighted_paths(stack_counts):
        for parent, child in zip(full_path, full_path[1:]):
            edge_counts[(parent, child)] += count

        first_pos: Dict[str, int] = {}
        for idx, symbol in enumerate(full_path):
            first_pos.setdefault(symbol, idx)

        symbols_in_order = [k for k, _v in sorted(first_pos.items(), key=lambda kv: kv[1])]
        for idx, before in enumerate(symbols_in_order):
            for after in symbols_in_order[idx + 1 :]:
                if before != after:
                    order_counts[(before, after)] += count

    must_precede = []
    for (before, after), ab_count in sorted(order_counts.items()):
        if ab_count > 0 and order_counts.get((after, before), 0) == 0:
            must_precede.append([before, after])

    allowed_edges = [[p, c] for (p, c) in sorted(edge_counts)]
    return {
        "version": "expanded-stack-grammar-v1",
        "allowed_edges": allowed_edges,
        "must_precede": must_precede,
    }


def _grammar_edges_and_order(grammar: Mapping[str, object]):
    allowed_edges_raw = grammar.get("allowed_edges")
    must_precede_raw = grammar.get("must_precede")
    assert isinstance(allowed_edges_raw, list), "grammar.allowed_edges must be a list"
    assert isinstance(must_precede_raw, list), "grammar.must_precede must be a list"

    allowed_edges = {tuple(x) for x in allowed_edges_raw}
    must_precede = {tuple(x) for x in must_precede_raw}
    return allowed_edges, must_precede


def find_expanded_grammar_violations(
    stack_counts: StackCounts,
    grammar: Mapping[str, object],
) -> List[dict[str, object]]:
    """Return aggregated violations against an expanded all-stack grammar."""
    allowed_edges, must_precede = _grammar_edges_and_order(grammar)

    bad_edges: Dict[Tuple[str, str], int] = defaultdict(int)
    bad_edge_examples: Dict[Tuple[str, str], str] = {}

    bad_orders: Dict[Tuple[str, str], int] = defaultdict(int)
    bad_order_examples: Dict[Tuple[str, str], str] = {}

    for full_path, count in _iter_weighted_paths(stack_counts):
        for parent, child in zip(full_path, full_path[1:]):
            key = (parent, child)
            if key not in allowed_edges:
                bad_edges[key] += count
                bad_edge_examples.setdefault(key, "/".join(full_path))

        first_pos: Dict[str, int] = {}
        for idx, symbol in enumerate(full_path):
            first_pos.setdefault(symbol, idx)

        for before, after in must_precede:
            if before in first_pos and after in first_pos:
                if first_pos[before] > first_pos[after]:
                    key = (before, after)
                    bad_orders[key] += count
                    bad_order_examples.setdefault(key, "/".join(full_path))

    violations: List[dict[str, object]] = []
    for (parent, child), count in sorted(bad_edges.items()):
        violations.append(
            {
                "kind": "unexpected-edge",
                "parent": parent,
                "child": child,
                "count": count,
                "example_path": bad_edge_examples[(parent, child)],
            }
        )
    for (before, after), count in sorted(bad_orders.items()):
        violations.append(
            {
                "kind": "order-permutation",
                "must_precede": [before, after],
                "count": count,
                "example_path": bad_order_examples[(before, after)],
            }
        )
    return violations


def assert_stack_counts_follow_expanded_grammar(
    stack_counts: StackCounts,
    grammar: Mapping[str, object],
    dataset_name: str,
) -> None:
    """Raise AssertionError when stacks violate expanded all-stack grammar."""
    violations = find_expanded_grammar_violations(stack_counts, grammar)
    if not violations:
        return

    lines = [
        (
            f"Expanded stack grammar violation in {dataset_name}: "
            "stacks violate allowed edges and/or required order constraints"
        )
    ]
    for v in violations:
        if v["kind"] == "unexpected-edge":
            lines.append(
                "  - "
                f"unexpected-edge {v['parent']} -> {v['child']}, "
                f"count={v['count']}, example={v['example_path']}"
            )
        else:
            before, after = v["must_precede"]
            lines.append(
                "  - "
                f"order-permutation expected {before} before {after}, "
                f"count={v['count']}, example={v['example_path']}"
            )
    raise AssertionError("\n".join(lines))
