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
