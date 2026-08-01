"""Exports write."""

import mb_cmn.file_io as file_io


def write(out_path, parsed):
    out_path_for_header = f"{out_path}/0header.json"
    file_io.json_dump_to_file_path(parsed["header"], out_path_for_header)
    chunks = _chunks_init()
    for verse in parsed["verses"]:
        chunk_str = _CHUNK_STR_FOR_BKID[_bkid_of_verse(verse)]
        chunks[chunk_str].append(verse)
    for chunk_str, chunk_verses in chunks.items():
        _write_smallish_file(out_path, chunk_str, chunk_verses)


def _write_smallish_file(out_path, chunk_str, chunk_verses):
    chunk_idx = _CHUNK_IDX_FOR_CHUNK_STR[chunk_str]
    idx_and_bkids = f"{chunk_idx:02}_{chunk_str}"
    out_path = f"{out_path}/1verses_{idx_and_bkids}.json"
    file_io.json_dump_to_file_path(chunk_verses, out_path)


def _bkid_of_verse(verse):
    return verse["bcv"][:2]


def _chunk_str_for_bkid():
    out = {}
    for bkid_tuple in _CHUNK_DEFINTIONS:
        for bkid in bkid_tuple:
            out[bkid] = "".join(bkid_tuple)
    return out


def _chunk_idx_for_chunk_str():
    out = {}
    for chunk_idx, bkid_tuple in enumerate(_CHUNK_DEFINTIONS):
        out["".join(bkid_tuple)] = chunk_idx
    return out


def _chunks_init():
    out = {}
    for bkid_tuple in _CHUNK_DEFINTIONS:
        out["".join(bkid_tuple)] = []
    return out


_CHUNK_DEFINTIONS = [
    ("gn",),
    ("ex", "lv"),
    ("nu", "dt"),
    ("js", "ju", "1s"),
    ("2s", "1k"),
    ("2k", "is"),
    ("je", "ek"),
    ("ho", "jl", "am", "ob", "jn", "mi", "na", "hb", "zp", "hg", "zc", "ma", "1c"),
    ("2c", "ps"),
    ("jb", "pr"),
    ("ru", "ca", "ec", "lm", "es", "da", "er", "ne"),
]
_CHUNK_STR_FOR_BKID = _chunk_str_for_bkid()
_CHUNK_IDX_FOR_CHUNK_STR = _chunk_idx_for_chunk_str()
