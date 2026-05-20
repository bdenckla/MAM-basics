"""Validate template nesting against a rank-based normal form.

We project each observed stack path onto a small set of ranked templates and
require the ranked projection to be nondecreasing in rank.

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
    """Return aggregated rank-order violations from stack_counts.

    A violation is an adjacent pair in the ranked projection where
    rank(caller) > rank(callee).
    """
    if rank_map is None:
        rank_map = DEFAULT_RANK_MAP

    bad_counts: Dict[Tuple[str, str], int] = defaultdict(int)
    examples: Dict[Tuple[str, str], str] = {}

    for (callee, stack_str), count in stack_counts.items():
        if count <= 0:
            continue
        full_path = [p for p in stack_str.split("/") if p]
        full_path.append(callee)
        ranked = _ranked_projection(full_path, rank_map)
        for caller, child in zip(ranked, ranked[1:]):
            if rank_map[caller] > rank_map[child]:
                key = (caller, child)
                bad_counts[key] += count
                examples.setdefault(key, "/".join(full_path))

    violations: List[dict[str, object]] = []
    for (caller, child), count in sorted(bad_counts.items()):
        violations.append(
            {
                "caller": caller,
                "callee": child,
                "caller_rank": rank_map[caller],
                "callee_rank": rank_map[child],
                "count": count,
                "example_path": examples[(caller, child)],
            }
        )
    return violations


def assert_stack_counts_in_normal_form(
    stack_counts: StackCounts,
    dataset_name: str,
    rank_map: RankMap | None = None,
) -> None:
    """Raise AssertionError when ranked nesting violates normal-form order."""
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
            f"count={v['count']}, example={v['example_path']}"
        )
    raise AssertionError("\n".join(lines))
