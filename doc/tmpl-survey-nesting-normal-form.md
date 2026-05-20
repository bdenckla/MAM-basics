# Template Nesting Normal Form (Template Survey)

This document defines an assert-only nesting convention for selected templates in
MAM template-survey data.

## Rank Grammar

We project each observed stack path onto ranked templates and require the
projection to follow this regex-like grammar:

`a?b?c?d?e?f?`

Ranks:

- `a`: `מ:כפול`
- `b`: `נוסח`
- `c`: ketiv/qere templates: `כו״ק`, `כתיב ולא קרי`, `קרי ולא כתיב`
- `d`: `מ:קמץ`
- `e`: `מ:דחי`
- `f`: `מ:אות-מיוחדת-במילה`

Equivalent graph statement: along the ranked projection of each root-to-leaf
path, rank must be strictly increasing (each rank appears at most once).

## Why this is useful

Some nestings are syntactically possible but not desired as project normal form.
Examples considered illegal by this convention:

- descending rank: `מ:דחי -> מ:קמץ` (i.e., `מ:קמץ` inside `מ:דחי`)
- duplicate rank group: `כתיב ולא קרי -> כו״ק` (both are rank `c`)

## Enforcement

The checker is assert-only:

- no auto-normalization
- violations raise `AssertionError` with aggregated counts and an example path

It runs in both plain and plus surveys.

## Expanded All-Stack Grammar

The rank grammar above covers only selected templates. To expand checking to
all stack symbols, use a data-driven grammar inferred from baseline stack data.

The inferred grammar has two parts:

- `allowed_edges`: adjacent parent->child transitions seen in baseline stacks
- `must_precede`: ordered symbol pairs where `A` and `B` co-occur and `A` is
	never observed after `B`

Why this is "reasonably strict":

- It allows many unseen stacks (for example unseen prefixes and novel
	combinations of previously-seen transitions).
- It rejects permutations that reverse stable relative order constraints.
- It rejects transitions that were never observed in the baseline grammar.

Implementation entry points in
`py/tmpl_survey/nesting_normal_form.py`:

- `infer_expanded_stack_grammar(stack_counts)`
- `assert_stack_counts_follow_expanded_grammar(stack_counts, grammar, dataset_name)`
- `find_expanded_grammar_violations(stack_counts, grammar)`
- `merge_stack_counts(*stack_counts_maps)`

Suggested workflow:

1. Build baseline grammar from union of plain and plus raw stack counts.
2. Save grammar JSON as a lock file committed to the repo.
3. On future runs, assert both datasets against the lock file grammar.
