"""Build the offline Introduction/doc-note research inventory; no product writes."""

import sys

from intro_doc_audit import audit, catalogues, proofs, review, structures


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    if sys.argv[1:] == ["review"]:
        review.main()
    elif sys.argv[1:] == ["proofs"]:
        proofs.main()
    elif sys.argv[1:] == ["structures"]:
        structures.main()
    elif sys.argv[1:] == ["catalogues"]:
        catalogues.main()
    elif not sys.argv[1:]:
        audit.main()
    else:
        raise SystemExit(
            "Usage: main_intro_doc_audit.py [review|proofs|structures|catalogues]"
        )


if __name__ == "__main__":
    main()
