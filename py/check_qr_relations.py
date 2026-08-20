#!/usr/bin/env python3
"""
Validate the cross-record relations declared in author_boj_util/qr_relations.py.

This is a *cross-record* check, so it cannot live in check_qr_consistency.py
(which is per-file AST and can't see sibling records). It resolves every
relation against RAW_QUIRKRECS and asserts that:

  * both endpoints exist and share the same qr-cv;
  * the kind is supported and the accent is known;
  * accent is conserved for kind "move" (present on the `from` record's μL
    side and absent from its consensus; present on the `to` record's consensus
    and absent from its μL side).

Exit codes:
  0 - All relations valid
  1 - One or more relations invalid

Usage:
  python check_qr_relations.py
"""

import sys

from author_boj_util.job_quirkrecs import RAW_QUIRKRECS
from author_boj_util.qr_relations import QR_RELATIONS, validate_relations


def main():
    try:
        validate_relations(RAW_QUIRKRECS)
    except AssertionError as exc:
        print(f"Relation validation FAILED: {exc}")
        return 1
    print(f"All {len(QR_RELATIONS)} relation(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
