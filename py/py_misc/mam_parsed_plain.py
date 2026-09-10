"""Build the shared plain-product header and book list."""


def add_header(light_books):
    """Wrap an ordered mapping of Hebrew book-name pairs to chapters."""
    he_bns = {}  # An insertion-ordered set.
    he_sbns = []
    chap_cnts = []
    book39s = []
    for (he_bn, he_sbn), chapters in light_books.items():
        he_bns[he_bn] = True
        if he_sbn is not None:
            he_sbns.append(he_sbn)
        basic = {"book24_name": he_bn, "sub_book_name": he_sbn}
        chap_cnts.append({"sub_book_name": he_sbn, "chapter_count": len(chapters)})
        book39s.append(dict(basic, chapters=chapters))
    assert len(he_bns) == 1
    header = {
        "book24_name": tuple(he_bns.keys())[0],
        "sub_book_names": he_sbns,
        "chapter_counts": chap_cnts,
    }
    return {"header": header, "book39s": book39s}
