"""The books the Miqra Mevoar converter knows, keyed by the stems of their Word files.

Rabbi David Kokhav's Word files reach Avi one book to a file, named by the book's
transliterated name. A stem missing from BOOKS is an error, never a guess: a new book
is added here with its title row's text, which is copied from its file by script.
"""

import dataclasses

from mb_cmn import mam_bknas


@dataclasses.dataclass(frozen=True)
class Book:
    """One book: its Word file's stem and title, and where MAM-simple keeps it."""

    stem: str
    # The text of the title row's Bible cell with its marks stripped. Obadiah's has no
    # vav, unlike MAM's name of the book.
    title: str
    mam_book: tuple[str, str | None]
    mam_simple_file: str
    osis_id: str

    def bk39_name(self) -> str:
        """MAM's name of the book, as the titles of the base chapters give it."""
        return mam_bknas.he_bk39_name(*self.mam_book)


def book_of_stem(stem: str) -> Book:
    """The book whose Word file has this stem; raise for any other stem."""
    if stem not in BOOKS:
        raise ValueError(f"No Miqra Mevoar book has the Word file stem {stem!r}")
    return BOOKS[stem]


BOOKS = {
    book.stem: book
    for book in (
        Book("yehoshua", "יהושע", mam_bknas.BS_JOSHUA, "Josh.json", "Josh"),
        Book("hoshea", "הושע", mam_bknas.BS_HOSEA, "Hos-Mal.json", "Hos"),
        Book("yoel", "יואל", mam_bknas.BS_JOEL, "Hos-Mal.json", "Joel"),
        Book("amos", "עמוס", mam_bknas.BS_AMOS, "Hos-Mal.json", "Amos"),
        Book("ovadya", "עבדיה", mam_bknas.BS_OBADIAH, "Hos-Mal.json", "Obad"),
        Book("yona", "יונה", mam_bknas.BS_JONAH, "Hos-Mal.json", "Jonah"),
    )
}
