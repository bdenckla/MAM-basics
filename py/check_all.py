#!/usr/bin/env python3
"""
Run all check scripts for this project.

Checks run:
  1. pyspellcheck/spellcheck_quirkrecs.py  (spell check quirk records)
  2. check_function_ordering.py            (public-before-private ordering)
  3. check_qr_consistency.py               (qr filename/record/word-id sync)
  4. check_qr_relations.py                 (cross-record relation validity)
  5. check_mark_order.py                   (Hebrew combining-mark order)
  6. check_escape_sequences.py             (unnecessary \\uXXXX escapes)
  7. check_html_syntax_and_sanity.py       (HTML output lint)

Exit codes:
  0 - All checks passed
  1 - One or more checks failed

Usage:
  python check_all.py [--w3c] [--w3c-strict]

The --w3c and --w3c-strict flags are forwarded to check_html_syntax_and_sanity.py.
"""

import argparse
import sys

import check_escape_sequences
import check_function_ordering
import check_html_syntax_and_sanity
import check_mark_order
import check_qr_consistency
import check_qr_relations
import check_spelling_in_html

_SEPARATOR = "─" * 60


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Run all check scripts for this project.",
    )
    parser.add_argument(
        "--w3c",
        action="store_true",
        help="forward --w3c to check_html_syntax_and_sanity",
    )
    parser.add_argument(
        "--w3c-strict",
        action="store_true",
        help="forward --w3c-strict to check_html_syntax_and_sanity",
    )
    args = parser.parse_args()

    checks = [
        ("Spell check (HTML output)", _run_spellcheck),
        ("Function ordering", _run_function_ordering),
        ("QR filename/record consistency", _run_qr_consistency),
        ("Cross-record relation validity", _run_qr_relations),
        ("Hebrew combining-mark order", _run_mark_order),
        ("Unnecessary \\uXXXX escapes", _run_escape_sequences),
        ("HTML output lint", lambda: _run_html_lint(args)),
    ]

    failures = []
    for label, run_fn in checks:
        print(f"\n{_SEPARATOR}")
        print(f"  {label}")
        print(_SEPARATOR)
        rc = run_fn()
        if rc:
            failures.append(label)

    print(f"\n{'=' * 60}")
    if failures:
        print(f"FAILED ({len(failures)} of {len(checks)}):")
        for f in failures:
            print(f"  - {f}")
        return 1
    else:
        print(f"All {len(checks)} checks passed.")
        return 0


def _run_spellcheck():
    # spellcheck_quirkrecs.main() returns None; treat that as success
    check_spelling_in_html.main()
    return 0


def _run_function_ordering():
    return check_function_ordering.main()


def _run_qr_consistency():
    return check_qr_consistency.main()


def _run_qr_relations():
    return check_qr_relations.main()


def _run_mark_order():
    return check_mark_order.main()


def _run_escape_sequences():
    return check_escape_sequences.main()


def _run_html_lint(args):
    argv = []
    if args.w3c:
        argv.append("--w3c")
    if args.w3c_strict:
        argv.append("--w3c-strict")
    return check_html_syntax_and_sanity.main(argv)


if __name__ == "__main__":
    sys.exit(main())
