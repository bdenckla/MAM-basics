"""The books the Miqra Mevoar converter knows, keyed by the stems of their Word files.

Rabbi David Kokhav's Word files reach Avi one book to a file, named by the book's
transliterated name. A stem missing from BOOKS is an error, never a guess: a new book
is added here with its title row's text, which is copied from its file by script.

A book's entry may declare the first and last chapters that its Word file contributes,
and its tracked JSON then holds those chapters alone. Isaiah's declares chapters 40 to
66, the book's fifth part: Avi asked for that part on 2026-11-25, while chapters 1 to
39 are unfinished in the file and, as he asked, are read past (Stage 16 of
doc/PLAN-miqra-mevoar.md). When the whole book comes, its entry declares no chapters.
Every other book's entry declares none, and its JSON holds the whole book.
"""

import dataclasses

from mb_cmn import mam_bknas


@dataclasses.dataclass(frozen=True)
class Book:
    """One book: its Word file's stem and title, where MAM-simple keeps it, and the
    chapters that its Word file contributes."""

    stem: str
    # The text of the title row's Bible cell with its marks stripped. Judges' and
    # Obadiah's have no vav, unlike MAM's names of the books.
    title: str
    mam_book: tuple[str, str | None]
    mam_simple_file: str
    osis_id: str
    # The first and last chapters that the book's Word file contributes, or None for the
    # whole book, as display_page.Page.chapters gives a page's.
    chapters: tuple[int, int] | None = None

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
        Book("sephershoftim", "שפטים", mam_bknas.BS_JUDGES, "Judg.json", "Judg"),
        Book(
            "yeshayahu",
            "ישעיהו",
            mam_bknas.BS_ISAIAH,
            "Isa.json",
            "Isa",
            chapters=(40, 66),
        ),
        Book("hoshea", "הושע", mam_bknas.BS_HOSEA, "Hos-Mal.json", "Hos"),
        Book("yoel", "יואל", mam_bknas.BS_JOEL, "Hos-Mal.json", "Joel"),
        Book("amos", "עמוס", mam_bknas.BS_AMOS, "Hos-Mal.json", "Amos"),
        Book("ovadya", "עבדיה", mam_bknas.BS_OBADIAH, "Hos-Mal.json", "Obad"),
        Book("yona", "יונה", mam_bknas.BS_JONAH, "Hos-Mal.json", "Jonah"),
        Book("mikha", "מיכה", mam_bknas.BS_MICAH, "Hos-Mal.json", "Mic"),
        Book("nahum", "נחום", mam_bknas.BS_NAXUM, "Hos-Mal.json", "Nah"),
        Book("havaquq", "חבקוק", mam_bknas.BS_XABA, "Hos-Mal.json", "Hab"),
        Book("tzefanya", "צפניה", mam_bknas.BS_TSEF, "Hos-Mal.json", "Zeph"),
        Book("hagay", "חגי", mam_bknas.BS_XAGGAI, "Hos-Mal.json", "Hag"),
        Book("zekharya", "זכריה", mam_bknas.BS_ZEKHAR, "Hos-Mal.json", "Zech"),
        Book("malakhi", "מלאכי", mam_bknas.BS_MALAKHI, "Hos-Mal.json", "Mal"),
        Book("daniyel", "דניאל", mam_bknas.BS_DANIEL, "Dan.json", "Dan"),
    )
}
