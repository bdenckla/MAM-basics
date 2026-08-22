import json


def read_json_file(json_in_path):
    with open(json_in_path, encoding="utf-8") as json_in_fp:
        flat_rows = json.load(json_in_fp)
    rows = list(map(_give_shape, flat_rows))
    return {"header": _make_json_header(rows), "body": rows}


def _give_shape(row):
    out = {"startrec": {}, "stoprec": {}}
    for key, val in row.items():
        shaped_key = _SHAPED_KEY[key]
        if len(shaped_key) == 2:
            out[shaped_key[0]][shaped_key[1]] = val
        else:
            out[shaped_key] = val
    return out


_SHAPED_KEY = {
    "page": "page",
    "bkid": "bkid",
    "note": "note",
    #
    "startco": ("startrec", "colnu"),
    "startli": ("startrec", "linenu"),
    "startc": ("startrec", "chnu"),
    "startv": ("startrec", "vrnu"),
    "startp": ("startrec", "wordnu"),
    "startl": ("startrec", "max_wordnu"),
    "start_word_count": ("startrec", "word_count"),
    #
    "stopco": ("stoprec", "colnu"),
    "stopli": ("stoprec", "linenu"),
    "stopc": ("stoprec", "chnu"),
    "stopv": ("stoprec", "vrnu"),
    "stopp": ("stoprec", "wordnu"),
    "stopl": ("stoprec", "max_wordnu"),
    "stop_word_count": ("stoprec", "word_count"),
}


def _get_book(row):
    return row["bkid"]


def _runs(lis):
    runs = []
    for elem in lis:
        if runs and runs[-1] == elem:
            continue
        runs.append(elem)
    return runs


def _non_biblical(row):
    return row["bkid"] is None


def _make_json_header(rows):
    non_bib = list(filter(_non_biblical, rows))
    books = _runs(map(_get_book, rows))
    return {
        "rows_non_bib": non_bib,
        "books": books,
    }
