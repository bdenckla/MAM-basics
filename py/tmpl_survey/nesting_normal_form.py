"""Validate template nesting against a rank-based normal form.

We project each observed stack onto a small set of ranked templates and
require the ranked projection to be strictly increasing in rank.

Regex-like shape for the ranked projection:
    rank-1?rank-2?rank-3?rank-4?rank-5?rank-6?rank-7?

Where, by default:
- rank-1: מ:כפול
- rank-2: נוסח
- rank-3: ketiv/qere templates (כו״ק, כתיב ולא קרי, קרי ולא כתיב)
- rank-4: מ:קמץ
- rank-5: מ:דחי
- rank-6: מ:אות-מיוחדת-במילה
- rank-7: terminal note markers
    (מ:לגרמיה-2, מ:פסק, מ:מקף אפור, מ:אות-ק, מ:אות-ג, מ:אות תלויה)
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

TemplateName = str
StackTop = TemplateName
FsStack = str
StackCounts = Mapping[Tuple[StackTop, FsStack], int]
RankMap = Mapping[TemplateName, int]
RankGroups = Sequence[tuple[str, Iterable[str]]]

_DEFAULT_RANK_GROUPS: tuple[tuple[str, frozenset[str]], ...] = (
    ("rank-1", frozenset({"מ:כפול"})),
    ("rank-2", frozenset({"נוסח"})),
    ("rank-3", frozenset({"כו״ק", "כתיב ולא קרי", "קרי ולא כתיב"})),
    ("rank-4", frozenset({"מ:קמץ"})),
    ("rank-5", frozenset({"מ:דחי"})),
    ("rank-6", frozenset({"מ:אות-מיוחדת-במילה"})),
    (
        "rank-7",
        frozenset(
            {
                "מ:לגרמיה-2",
                "מ:פסק",
                "מ:מקף אפור",
                "מ:אות-ק",
                "מ:אות-ג",
                "מ:אות תלויה",
            }
        ),
    ),
)
_COLUMN_LETTERS: tuple[str, str, str] = ("C", "D", "E")


def default_rank_groups() -> tuple[tuple[str, frozenset[str]], ...]:
    """Return the default rank groups used by rank-based normal form."""
    return _DEFAULT_RANK_GROUPS


def _build_rank_map(rank_groups: Sequence[tuple[str, Iterable[str]]]) -> Dict[str, int]:
    rank_map: Dict[str, int] = {}
    for rank, (_label, names) in enumerate(rank_groups):
        for name in names:
            if name in rank_map:
                raise ValueError(f"Template {name!r} appears in multiple rank groups")
            rank_map[name] = rank
    return rank_map


def build_rank_map(rank_groups: RankGroups) -> Dict[str, int]:
    """Build a rank map from ordered rank groups.

    Each group is a tuple of (label, template_names). The label is metadata
    only; rank order is determined by position in the sequence.
    """
    return _build_rank_map(rank_groups)


DEFAULT_RANK_MAP: Dict[str, int] = _build_rank_map(_DEFAULT_RANK_GROUPS)


def default_case_rank_maps() -> Dict[str, Dict[str, int]]:
    """Return default rank maps for plain/plus x C/D/E cases."""
    case_rank_maps: Dict[str, Dict[str, int]] = {}
    for dataset in ("plain", "plus"):
        for column in _COLUMN_LETTERS:
            case_key = f"{dataset}-{column}"
            case_rank_maps[case_key] = dict(DEFAULT_RANK_MAP)
    return case_rank_maps


def regex_like_grammar() -> str:
    """Return the rank grammar in compact regex-like notation."""
    return "rank-1?rank-2?rank-3?rank-4?rank-5?rank-6?rank-7?"


def _ranked_projection(stack: Sequence[str], rank_map: RankMap) -> List[str]:
    return [name for name in stack if name in rank_map]


def _stack_from_fs_stack(top: str, fs_stack: str) -> Tuple[str, ...]:
    """Return stack tuple from fs_stack templates plus top template.

    Here fs_stack means the forward-slash separated stack string.

    Stack strings are prefixed by column letter (C/D/E) in survey data;
    that prefix is removed so coverage reflects only template symbols.
    """
    parts = [p for p in fs_stack.split("/") if p]
    if parts and parts[0] in _COLUMN_LETTERS:
        parts = parts[1:]
    return tuple(parts + [top])


def _is_singleton_stack(stack: Sequence[str]) -> bool:
    return len(stack) <= 1


_CHECKEDNESS_KEYS: tuple[str, str, str] = (
    "fully_checked",
    "partially_checked",
    "totally_unchecked",
)


def _checkedness_bucket(
    stack: Sequence[str],
    rank_map: RankMap,
) -> str | None:
    if _is_singleton_stack(stack):
        return None
    ranked_count = sum(1 for name in stack if name in rank_map)
    if ranked_count <= 1:
        return "totally_unchecked"
    if ranked_count == len(stack):
        return "fully_checked"
    return "partially_checked"


def _fs_stack_with_top(top: str, fs_stack: str) -> str:
    parts = [p for p in fs_stack.split("/") if p]
    return "/".join(parts + [top])


def summarize_rank_coverage_counts(
    stack_counts: StackCounts,
    rank_map: RankMap,
) -> Dict[str, int]:
    """Summarize weighted rank-coverage categories over observed stacks.

    Singleton template stacks are excluded entirely.

    Categories use coverage cov on stack (fs_stack templates + top):
    - totally_unchecked: projected ranked path len <= 1
    - fully_checked: cov = 1
    - partially_checked: projected ranked path len >= 2 and 0 < cov < 1
    """
    fully_checked = 0
    partially_checked = 0
    totally_unchecked = 0

    for (top, fs_stack), count in stack_counts.items():
        if count <= 0:
            continue
        stack = _stack_from_fs_stack(top, fs_stack)
        bucket = _checkedness_bucket(stack, rank_map)
        if bucket is None:
            continue
        if bucket == "fully_checked":
            fully_checked += count
        elif bucket == "totally_unchecked":
            totally_unchecked += count
        else:
            partially_checked += count

    return {
        "fully_checked": fully_checked,
        "partially_checked": partially_checked,
        "totally_unchecked": totally_unchecked,
        "total": fully_checked + partially_checked + totally_unchecked,
    }


def summarize_rank_coverage_top_paths(
    stack_counts: StackCounts,
    rank_map: RankMap,
    max_paths: int = 10,
) -> Dict[str, List[dict[str, object]]]:
    """Return top stacks per checkedness bucket.

    Stacks are emitted as strings that include column prefix and top template,
    for example: E/מ:כפול/נוסח/ש
    """
    if max_paths < 0:
        raise ValueError(f"max_paths must be >= 0, got {max_paths}")

    fs_stack_counts = {
        key: defaultdict(int) for key in _CHECKEDNESS_KEYS
    }
    for (top, fs_stack), count in stack_counts.items():
        if count <= 0:
            continue
        stack = _stack_from_fs_stack(top, fs_stack)
        bucket = _checkedness_bucket(stack, rank_map)
        if bucket is None:
            continue
        stack_key = _fs_stack_with_top(top, fs_stack)
        fs_stack_counts[bucket][stack_key] += count

    top_paths_by_bucket: Dict[str, List[dict[str, object]]] = {}
    for bucket in _CHECKEDNESS_KEYS:
        ranked = sorted(
            fs_stack_counts[bucket].items(),
            key=lambda kv: (-kv[1], kv[0]),
        )
        top_paths_by_bucket[bucket] = [
            {
                "stack": fs_stack_with_top,
                # Backward-compatible alias kept during terminology migration.
                "stack_path": fs_stack_with_top,
                "count": count,
            }
            for fs_stack_with_top, count in ranked[:max_paths]
        ]
    return top_paths_by_bucket


def summarize_rank_coverage_by_case(
    stack_counts: StackCounts,
    dataset_key: str,
    case_rank_maps: Mapping[str, RankMap],
) -> Dict[str, Dict[str, int]]:
    """Summarize coverage categories for C/D/E cases of one dataset."""
    assert dataset_key in ("plain", "plus"), dataset_key

    by_case: Dict[str, Dict[str, int]] = {}
    for column in _COLUMN_LETTERS:
        case_key = f"{dataset_key}-{column}"
        rank_map = case_rank_maps.get(case_key)
        if rank_map is None:
            raise ValueError(
                f"Missing rank map for case {case_key!r}. "
                "Expected case rank maps for all columns C/D/E."
            )
        column_stack_counts = _stack_counts_for_column(stack_counts, column)
        by_case[case_key] = summarize_rank_coverage_counts(
            column_stack_counts,
            rank_map,
        )
    return by_case


def summarize_rank_coverage_top_paths_by_case(
    stack_counts: StackCounts,
    dataset_key: str,
    case_rank_maps: Mapping[str, RankMap],
    max_paths: int = 10,
) -> Dict[str, Dict[str, List[dict[str, object]]]]:
    """Return top stacks per checkedness bucket for C/D/E cases."""
    assert dataset_key in ("plain", "plus"), dataset_key

    by_case: Dict[str, Dict[str, List[dict[str, object]]]] = {}
    for column in _COLUMN_LETTERS:
        case_key = f"{dataset_key}-{column}"
        rank_map = case_rank_maps.get(case_key)
        if rank_map is None:
            raise ValueError(
                f"Missing rank map for case {case_key!r}. "
                "Expected case rank maps for all columns C/D/E."
            )
        column_stack_counts = _stack_counts_for_column(stack_counts, column)
        by_case[case_key] = summarize_rank_coverage_top_paths(
            column_stack_counts,
            rank_map,
            max_paths=max_paths,
        )
    return by_case


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

    for (top, fs_stack), count in stack_counts.items():
        if count <= 0:
            continue
        stack = _stack_from_fs_stack(top, fs_stack)
        if _is_singleton_stack(stack):
            # Normal-order checking is about ordering relations, which require
            # at least two templates in the stack.
            continue
        ranked = _ranked_projection(stack, rank_map)
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
                examples.setdefault(key, "/".join(stack))

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
                "example_stack": examples[(caller, child, relation)],
                # Backward-compatible alias kept during terminology migration.
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
        example_stack = v.get("example_stack", v["example_path"])
        lines.append(
            "  - "
            f"{v['caller']} (rank {v['caller_rank']}) -> "
            f"{v['callee']} (rank {v['callee_rank']}), "
            f"relation={v['relation']}, "
            f"count={v['count']}, example={example_stack}"
        )
    raise AssertionError("\n".join(lines))


def _stack_counts_for_column(
    stack_counts: StackCounts,
    column_letter: str,
) -> Dict[Tuple[str, str], int]:
    """Return a copy of stack_counts restricted to a single column prefix."""
    assert column_letter in _COLUMN_LETTERS, column_letter

    filtered: Dict[Tuple[str, str], int] = {}
    for (top, fs_stack), count in stack_counts.items():
        if count <= 0:
            continue
        parts = [p for p in fs_stack.split("/") if p]
        if parts and parts[0] == column_letter:
            filtered[(top, fs_stack)] = count
    return filtered


def assert_stack_counts_in_normal_form_by_case(
    stack_counts: StackCounts,
    dataset_key: str,
    case_rank_maps: Mapping[str, RankMap],
) -> None:
    """Assert normal form separately for C/D/E using dataset-specific rank maps.

    dataset_key must be "plain" or "plus". Expected case keys in case_rank_maps
    are f"{dataset_key}-C", f"{dataset_key}-D", and f"{dataset_key}-E".
    """
    assert dataset_key in ("plain", "plus"), dataset_key

    for column in _COLUMN_LETTERS:
        case_key = f"{dataset_key}-{column}"
        rank_map = case_rank_maps.get(case_key)
        if rank_map is None:
            raise ValueError(
                f"Missing rank map for case {case_key!r}. "
                "Expected case rank maps for all columns C/D/E."
            )
        column_stack_counts = _stack_counts_for_column(stack_counts, column)
        assert_stack_counts_in_normal_form(
            column_stack_counts,
            dataset_name=f"{dataset_key} survey ({column} column)",
            rank_map=rank_map,
        )


def merge_stack_counts(*stack_counts_maps: StackCounts) -> Dict[Tuple[str, str], int]:
    """Merge one or more stack-count maps by summing duplicate keys."""
    merged: Dict[Tuple[str, str], int] = defaultdict(int)
    for stack_counts in stack_counts_maps:
        for key, count in stack_counts.items():
            if count > 0:
                merged[key] += count
    return dict(merged)


def _iter_weighted_stacks(stack_counts: StackCounts):
    for (top, fs_stack), count in stack_counts.items():
        if count <= 0:
            continue
        stack = tuple([p for p in fs_stack.split("/") if p] + [top])
        if not stack:
            continue
        yield stack, count


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

    for stack, count in _iter_weighted_stacks(stack_counts):
        for parent, child in zip(stack, stack[1:]):
            edge_counts[(parent, child)] += count

        first_pos: Dict[str, int] = {}
        for idx, symbol in enumerate(stack):
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

    for stack, count in _iter_weighted_stacks(stack_counts):
        for parent, child in zip(stack, stack[1:]):
            key = (parent, child)
            if key not in allowed_edges:
                bad_edges[key] += count
                bad_edge_examples.setdefault(key, "/".join(stack))

        first_pos: Dict[str, int] = {}
        for idx, symbol in enumerate(stack):
            first_pos.setdefault(symbol, idx)

        for before, after in must_precede:
            if before in first_pos and after in first_pos:
                if first_pos[before] > first_pos[after]:
                    key = (before, after)
                    bad_orders[key] += count
                    bad_order_examples.setdefault(key, "/".join(stack))

    violations: List[dict[str, object]] = []
    for (parent, child), count in sorted(bad_edges.items()):
        violations.append(
            {
                "kind": "unexpected-edge",
                "parent": parent,
                "child": child,
                "count": count,
                "example_stack": bad_edge_examples[(parent, child)],
                # Backward-compatible alias kept during terminology migration.
                "example_path": bad_edge_examples[(parent, child)],
            }
        )
    for (before, after), count in sorted(bad_orders.items()):
        violations.append(
            {
                "kind": "order-permutation",
                "must_precede": [before, after],
                "count": count,
                "example_stack": bad_order_examples[(before, after)],
                # Backward-compatible alias kept during terminology migration.
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
        example_stack = v.get("example_stack", v["example_path"])
        if v["kind"] == "unexpected-edge":
            lines.append(
                "  - "
                f"unexpected-edge {v['parent']} -> {v['child']}, "
                f"count={v['count']}, example={example_stack}"
            )
        else:
            must_precede = v["must_precede"]
            assert isinstance(must_precede, list) and len(must_precede) == 2
            before, after = must_precede
            lines.append(
                "  - "
                f"order-permutation expected {before} before {after}, "
                f"count={v['count']}, example={example_stack}"
            )
    raise AssertionError("\n".join(lines))
