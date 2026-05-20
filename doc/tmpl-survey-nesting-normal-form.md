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

1. Build a plain grammar lock from plain raw stack counts.
2. Build a plus grammar lock from plus raw stack counts.
3. Commit both lock files.
4. On future runs, assert each dataset against its own lock file grammar.

Runtime wiring:

- Lock file paths:
	- `py/tmpl_survey/expanded_stack_grammar_plain.lock.json`
	- `py/tmpl_survey/expanded_stack_grammar_plus.lock.json`
- Main survey command validates plain stacks against the plain lock and plus
	stacks against the plus lock.
- To create or refresh both lock files from current data, run:

	`.venv/Scripts/python.exe py/main_tmpl_survey.py --write-expanded-stack-grammar-lock`
