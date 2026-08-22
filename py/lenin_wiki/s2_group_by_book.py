from mb_cmn.my_utils import my_groupby


def s2_group_by_book(rows):
    return my_groupby(rows, _get_book)


def _get_book(row):
    # We treat the note on a non-Biblical row as a kind of pseudo-book.
    key = row["bkid"] or row["note"]
    assert key is not None
    return key
