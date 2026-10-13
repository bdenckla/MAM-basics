"""Build the offline Introduction/doc-note research inventory; no product writes."""

import sys

from intro_doc_audit import audit


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    audit.main()


if __name__ == "__main__":
    main()
