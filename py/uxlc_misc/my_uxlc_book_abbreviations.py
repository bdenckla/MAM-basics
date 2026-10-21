"""Re-exports expand_citation and the two UXLC book-abbreviation maps of py_uxlc's table.

py_uxlc.my_uxlc_book_abbreviations holds the one table, so a book added there cannot be missing
for the modules that import this one.  Until 2026-10-20 this module was a second copy of the
table, and had fallen behind it: it lacked Nahum and Habakkuk.  Ben decided that day that it
should re-export the first instead.
"""

from py_uxlc.my_uxlc_book_abbreviations import (
    BKNA_MAP_STD_TO_UXLC,
    BKNA_MAP_UXLC_TO_STD,
    expand_citation,
)

__all__ = ["BKNA_MAP_STD_TO_UXLC", "BKNA_MAP_UXLC_TO_STD", "expand_citation"]
