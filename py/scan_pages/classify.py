"""Classify every scanned filename, or refuse.

One parser per edition, each a pure function of the file name.  A parser that does
not recognize a name returns None, and ``survey`` then fails listing every such name
rather than dropping it: a page that quietly falls out of the listing is a page a
lookup can never reach, and nothing downstream would ever notice.

WHAT THE FILENAMES DO NOT SAY, THIS MODULE SAYS, WITH ITS EVIDENCE.  Three sections
carry no hint of their contents in their names -- koren's ``V``, simanim-tanakh's
``V``, and simanim-tanakh's ``A9`` -- so each was settled by reading a page image on
2026-08-07 and the reading is recorded at the table that encodes it.  Anything not
settled that way is classified from the name alone.
"""

import re

from mb_cmn import bib_locales as tbn
from scan_pages import book_codes
from scan_pages import page_kinds as pk

# Service words that decide a kind wherever they appear in a filename's descriptor.
# Order matters: "inside-front-cover" is a cover, and its "front" must not win first.
_COVER_WORDS = ("front-cover", "back-cover", "cover", "spine")


def _kind_of_descriptor(desc, default):
    """Return the kind a front/back-matter descriptor implies."""
    if any(word in desc for word in _COVER_WORDS):
        return pk.COVER
    if "blank" in desc:
        return pk.BLANK
    if "ToC" in desc:
        return pk.TOC
    return default


def _split(file_name):
    """Return a filename's dash-separated fields, minus the .jpg suffix."""
    assert file_name.endswith(".jpg"), file_name
    return file_name[: -len(".jpg")].split("-")


def _leading_books(fields):
    """Return (bk39ids, remaining fields), consuming the leading book tokens.

    A page carrying two books names them both -- jc1's ``544-A-O.jpg`` is the page
    where Amos ends and Obadiah begins -- and Obadiah in jc1 has no page to itself
    at all, so a parser that took only the first token would lose a whole book.
    """
    bk39ids = []
    index = 0
    while index < len(fields):
        bk39id = book_codes.bk39_of_token(fields[index])
        if bk39id is None:
            break
        bk39ids.append(bk39id)
        index += 1
    return bk39ids, fields[index:]


# --------------------------------------------------------------------------- jc1


def _jc1(file_name):
    fields = _split(file_name)
    if fields[0].startswith("#"):  # front matter, separately numbered
        return pk.page(file_name, _kind_of_descriptor(file_name, pk.FRONT_MATTER))
    if not fields[0].isdigit():
        return None
    rest = fields[1:]
    if rest and rest[0].isdigit():
        return _jc1_supplement(file_name, rest[1:])
    bk39ids, tail = _leading_books(rest)
    if bk39ids:
        # A trailing service word after the books ("316-2S-blank.jpg") describes the
        # unused remainder of a page whose text is still 2Samuel's, so it stays body.
        return pk.page(file_name, pk.BODY, bkids=bk39ids)
    if not tail:
        return None
    kind = _kind_of_descriptor(file_name, None)
    return None if kind is None else pk.page(file_name, kind)


def _jc1_supplement(file_name, desc_fields):
    """Classify a page of jc1's supplements, numbered 01-40 after the body."""
    desc = "-".join(desc_fields)
    if "Decalogue" in desc:
        bk39ids, _ = _leading_books(desc_fields)
        if not bk39ids:
            return None
        # BOTH strands are on this one page, side by side: read 2026-08-07,
        # 876-02-Exod-Decalogue.jpg heads its right column בטעם התחתון (with verse
        # numbers) and its left column בטעם העליון.  So a jc1 Decalogue page belongs
        # to two strand segments at once -- see doc/scan-pages.md.
        return pk.page(
            file_name,
            pk.DECALOGUE,
            bkids=bk39ids,
            strands=(pk.TAXTON, pk.ELYON),
            note="both strands, side by side on the one page",
        )
    return pk.page(file_name, _kind_of_descriptor(desc, pk.BACK_MATTER))


# --------------------------------------------------------------------------- bhl


def _bhl(file_name):
    fields = _split(file_name)
    if fields[0].startswith("#"):
        return pk.page(file_name, _kind_of_descriptor(file_name, pk.FRONT_MATTER))
    if not fields[0].isdigit():
        return None
    rest = fields[1:]
    if not rest:
        # A bare number is a continuation page of one of the five appendices; the
        # shape occurs only after 1229-Appendix-A, which survey's ordering check
        # confirms rather than assumes.
        return pk.page(file_name, pk.BACK_MATTER)
    if rest[0] == "title" and rest[1:2] == ["page"]:
        return _bhl_title_page(file_name, rest[2:])
    if rest[0] == "Appendix":
        return pk.page(file_name, pk.BACK_MATTER)
    bk39ids, tail = _leading_books(rest)
    if bk39ids and tail and tail[0] == "Decalogue":
        # "Upper" is bhl's word for the עליון, and this page has that strand
        # alone: read 2026-08-07, 1227-Exod-Decalogue-Upper.jpg is headed "The
        # Decalogue with Upper Cantillation (טעם עליון) / Exodus 20:2-13 (פרשת יתרו)".
        if tail[1:] != ["Upper"]:
            return None
        return pk.page(file_name, pk.DECALOGUE, bkids=bk39ids, strands=(pk.ELYON,))
    if bk39ids:
        return pk.page(file_name, pk.BODY, bkids=bk39ids)
    kind = _kind_of_descriptor(file_name, None)
    return None if kind is None else pk.page(file_name, kind)


def _bhl_title_page(file_name, name_fields):
    """Classify ``NNNN-title-page-<X>.jpg``, where X may be larger than a book39."""
    name = "-".join(name_fields)
    if name in book_codes.LONGFORM_SECTIONS:
        return pk.page(file_name, pk.SECTION_TITLE)
    bk39id = book_codes.bk39_of_token(name)
    if bk39id is None:
        return None
    return pk.page(file_name, pk.BOOK_TITLE, bkids=(bk39id,))


# ------------------------------------------------- koren and simanim-tanakh


def _koren_family_body(file_name, fields):
    """Classify ``<ordered_short>-<short>-<number>[-blank].jpg``, else return None.

    Both codes name a book, so this insists they name the SAME book.  Nothing else in
    the five editions cross-checks itself; here it comes free.
    """
    if len(fields) < 3:
        return None
    by_section = book_codes.bk39_of_ordered_short(fields[0])
    by_book = book_codes.bk39_of_token(fields[1])
    if by_section is None or by_book is None or not fields[2].isdigit():
        return None
    if by_section != by_book:
        return None
    tail = fields[3:]
    if tail == ["blank"]:
        return pk.page(file_name, pk.BLANK, bkids=(by_book,))
    if tail:
        return None
    if int(fields[2]) == 0:  # "D2-Pr-000.jpg": the book's title page
        return pk.page(file_name, pk.BOOK_TITLE, bkids=(by_book,))
    return pk.page(file_name, pk.BODY, bkids=(by_book,))


def _is_section_front(token):
    """True for ``A0``/``B0``/``D0``: a section's title pages, before its first book."""
    return len(token) == 2 and token[0].isalpha() and token[1] == "0"


# koren's V section: 58 separately numbered pages of back matter, with the scan
# number equal to the printed page number.  Its printed table of contents is on
# V-001.jpg (read 2026-08-07) and gives the whole section: 3 ספר התנ״ך שבהוצאת קורן,
# 9 דברי ברכה, 13 חילופי נוסחאות, 17 and 33 the Hebrew renderings of the Aramaic in
# Daniel and in Ezra, 38 עשרת הדיברות בטעם העליון, 40-42 the Torah readings, 46
# ברכות ההפטרה, 47 סדר ההפטרות, 58 שמות הטעמים.  Pages 38 and 39 were then read
# themselves: V-038 is עשרת הדיברות שבפרשת יתרו / בטעם העליון and V-039 is
# עשרת הדיברות שבפרשת ואתחנן / בטעם העליון.  Only those two hold biblical text.
_KOREN_V_DECALOGUE = {"V-038.jpg": tbn.BK_EXODUS, "V-039.jpg": tbn.BK_DEUTER}


def _koren(file_name):
    fields = _split(file_name)
    body = _koren_family_body(file_name, fields)
    if body is not None:
        return body
    head = fields[0]
    if _is_section_front(head) and len(fields) == 2 and fields[1].isdigit():
        return pk.page(file_name, pk.SECTION_TITLE)
    if head.isdigit():  # "00001-front-cover.jpg" and bare "00002.jpg"
        return pk.page(file_name, _kind_of_descriptor(file_name, pk.FRONT_MATTER))
    if head == "V":
        bk39id = _KOREN_V_DECALOGUE.get(file_name)
        if bk39id is not None:
            return pk.page(
                file_name, pk.DECALOGUE, bkids=(bk39id,), strands=(pk.ELYON,)
            )
        if file_name == "V-001.jpg":
            return pk.page(file_name, pk.TOC, note="the V section's contents page")
        return pk.page(file_name, pk.BACK_MATTER)
    if head == "W":
        return pk.page(file_name, pk.BACK_MATTER, note="colophon")
    if head in ("X", "Y"):
        return pk.page(file_name, _kind_of_descriptor(file_name, pk.COVER))
    return None


# simanim-tanakh's A9: three pages appended after Deuteronomy, whose section title
# page A9-0349.jpg reads עשרת הדברות בטעם עליון (read 2026-08-07).  The book itself
# thus names the strand, and "10C" in the other two names is the Ten Commandments,
# qualified by the section code of the book each is drawn from (A2 Exodus, A5
# Deuteronomy).  A9 is not one of this repo's ordered_short codes; the scanner coined
# it to sort the appendix after A5.
_SIMANIM_TANAKH_A9 = {
    "A9-0349.jpg": None,
    "A9-A2-10C-0350.jpg": tbn.BK_EXODUS,
    "A9-A5-10C-0351.jpg": tbn.BK_DEUTER,
}


# Pages whose codes say "text of this book" but which reading showed to be
# something else.  simanim-tanakh gives the כתובים section its divider under Psalms'
# codes rather than a D0- name, so neither the section-front rule nor the divider pass
# can see it: D1-Ps-0993.jpg is the כתובים divider (בין השנים 2783-3438, read
# 2026-08-07), and Psalms' text begins on 0994.  The Torah and Nevi'im dividers are
# named 3-1/3-2 and B0-0353/B0-0354, which those rules do catch.
_SIMANIM_TANAKH_READ = {"D1-Ps-0993.jpg": (pk.SECTION_TITLE, "כתובים")}


def _simanim_tanakh(file_name):
    read = _SIMANIM_TANAKH_READ.get(file_name)
    if read is not None:
        kind, note = read
        return pk.page(file_name, kind, note=note)
    fields = _split(file_name)
    body = _koren_family_body(file_name, fields)
    if body is not None:
        return body
    head = fields[0]
    if file_name in _SIMANIM_TANAKH_A9:
        bk39id = _SIMANIM_TANAKH_A9[file_name]
        if bk39id is None:
            return pk.page(file_name, pk.SECTION_TITLE, note="עשרת הדברות בטעם עליון")
        return pk.page(file_name, pk.DECALOGUE, bkids=(bk39id,), strands=(pk.ELYON,))
    if _is_section_front(head) and len(fields) == 2 and fields[1].isdigit():
        return pk.page(file_name, pk.SECTION_TITLE)
    if head in ("1", "2"):  # two separately numbered runs of front matter
        return pk.page(file_name, _kind_of_descriptor(file_name, pk.FRONT_MATTER))
    if head == "3":
        # The Torah section's divider, the two leaves immediately before A1-G-0001:
        # 3-1.jpg is the title page תורה and 3-2.jpg its contents page, listing
        # בראשית 1, שמות 87, ויקרא 161, במדבר 213, דברים 287 (both read 2026-08-07).
        if file_name == "3-2.jpg":
            return pk.page(file_name, pk.TOC, note="the Torah section's contents")
        return pk.page(file_name, pk.SECTION_TITLE, note="תורה")
    if head == "V":
        # 83 pages of study apparatus, not biblical text: V-1463.jpg is the section
        # title page מאורעות התנ״ך / כולל סדר ההפטרות and V-1500.jpg has the
        # running head נושאי המאורעות בכתובים over a topical index (both read
        # 2026-08-07).  Out of lookup.
        return pk.page(file_name, pk.APPARATUS, note="מאורעות התנ״ך")
    if head == "W":
        return pk.page(file_name, pk.BACK_MATTER)
    if head in ("X", "Y"):
        return pk.page(file_name, _kind_of_descriptor(file_name, pk.COVER))
    return None


# ------------------------------------------------------------------ simanim-tiqqun

# The five lettered sections, established by reading sample pages on 2026-08-06 and
# 2026-08-07 and written up in doc/scan-pages.md.  Only C holds pointed biblical
# text; which of its pages is Torah, which a haftarah, which one of the three
# full-text megillot and which the notes tail is Phase 3's question, so every C page
# is classified as body whose segment is not yet assigned.
_TIQQUN_SECTIONS = {
    "A": (pk.COVER, None),
    "B": (pk.APPARATUS, "front matter: essays and the per-parasha simanim"),
    "C": (pk.BODY_UNASSIGNED, None),
    "D": (pk.UNPOINTED, "compact unpointed Torah, scanned rotated"),
    "E": (pk.APPARATUS, "colour promotional booklet"),
}

_TIQQUN_RE = re.compile(r"^([A-E])(\d+)(?:-(\d+))?$")


def _simanim_tiqqun(file_name):
    match = _TIQQUN_RE.match(file_name[: -len(".jpg")])
    if match is None:
        return None
    kind, note = _TIQQUN_SECTIONS[match.group(1)]
    return pk.page(file_name, kind, note=note)


PARSERS = {
    "jc1": _jc1,
    "koren": _koren,
    "simanim-tanakh": _simanim_tanakh,
    "simanim-tiqqun": _simanim_tiqqun,
    "bhl": _bhl,
}

_KOREN_FAMILY = ("koren", "simanim-tanakh")
_NUMBERED = re.compile(r"^([A-Z][0-9A-Z])-([^-]+)-(\d+)\.jpg$")


def classify(edition_id, file_name):
    """Return one classified page, or None when the filename is not recognized."""
    return PARSERS[edition_id](file_name)


def classify_listing(edition_id, file_names):
    """Classify a whole sorted listing. Unrecognized names come back as None.

    A LISTING SAYS THINGS ONE FILE NAME CANNOT.  In koren and simanim-tanakh a book
    opens with a divider leaf named with the book's codes, so it looks
    exactly like a page of its text; what gives it away is the *next* number being
    absent, because the divider's blank verso was not scanned.  That signal needs the
    listing, not the name, which is why classification has this second pass.
    """
    pages = [classify(edition_id, name) for name in file_names]
    if edition_id in _KOREN_FAMILY:
        _mark_divider_leaves(pages)
    return pages


def _mark_divider_leaves(pages):
    """Reclassify a book's opening page as its divider where the listing shows one.

    The signal is a missing number straight after a book's first page.  Verified by
    reading, twice, and never yet seen to be wrong in that direction: koren's
    A2-E-081.jpg is a bare שמות divider and simanim-tanakh's A2-E-0085.jpg is the
    Torah contents with שמות 87 picked out, both followed by an absent number, and
    simanim-tanakh's Torah contents page confirms the text of שמות starts at
    printed 87.

    IT MISSES DIVIDERS RATHER THAN INVENTING THEM, AND THAT IS DELIBERATE.  A divider
    whose verso *was* scanned leaves no gap and so is not caught -- simanim-tanakh's
    D1-Ps-0993.jpg is the כתובים divider with 0994 present.  Survey reports every
    book this pass left alone so the census checks those openings first; the cost of
    a miss is a seeded record one leaf early, which the census corrects, whereas a
    false positive would move a book's start off a page that really does hold text.
    """
    numbered = {}
    for index, page in enumerate(pages):
        if page is None or page["kind"] != pk.BODY:
            continue
        matched = _NUMBERED.match(page["file"])
        if matched:
            key = (matched.group(1), matched.group(2))
            numbered.setdefault(key, []).append((int(matched.group(3)), index))
    for (_, _), entries in numbered.items():
        entries.sort()
        if len(entries) < 2 or entries[1][0] == entries[0][0] + 1:
            continue
        index = entries[0][1]
        page = pages[index]
        pages[index] = pk.page(
            page["file"],
            pk.BOOK_TITLE,
            bkids=page["bkids"],
            note="divider leaf: the next printed number was not scanned",
        )


def unadjudicated_book_openings(edition_id, pages):
    """Return the book openings for which no divider leaf was found at all.

    A book whose divider the listing did reveal is settled: the page after it holds
    text.  A book with no divider found is the open case -- either it genuinely has
    none, as a book continuing its book24 does, or it has one whose verso was scanned
    and so left no gap.  Only those are worth the census's attention first.
    """
    if edition_id not in _KOREN_FAMILY:
        return []
    divider_books, first_body, out = set(), {}, []
    for page in pages:
        matched = _NUMBERED.match(page["file"])
        if matched is None:
            continue
        key = (matched.group(1), matched.group(2))
        if page["kind"] == pk.BOOK_TITLE:
            divider_books.add(key)
        elif page["kind"] == pk.BODY:
            first_body.setdefault(key, page["file"])
    for key, name in first_body.items():
        if key not in divider_books:
            out.append(name)
    return sorted(out)
